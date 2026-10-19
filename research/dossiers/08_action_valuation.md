# Dossier 08: One decision currency for SELL / HOLD / REFINANCE / LEVER

**Real options, liquidity shadow prices and decision theory for asset-level actions that stay consistent with the portfolio-level multi-period optimizer**

- **Stream:** 08, action valuation
- **As of:** 2026-10-18
- **Evidence tags:**
  - **[S]** sourced fact, cited and dated
  - **[P]** practitioner consensus
  - **[I]** our own inference or design choice
- **Reproducibility:** `research/verification/08_action_valuation_examples.py` produces every worked-example number. It uses fixed seeds and writes its results to `08_action_valuation_examples_results.json`. All amounts are in US$ millions unless stated otherwise.

---

## 1. Executive summary

### The problem
ADIC must make hundreds of asset-level choices: sell a fund interest, hold it, borrow against it, or add exposure, with or without borrowing. Those choices sit inside a portfolio that:
- must distribute 5–10% a year;
- must keep a 7% robust floor and pass a liquidity survival gate;
- carries a ~60% private book whose distributions have collapsed.

The asset-level metrics in common use cannot get these choices right. Since-inception IRR, discount to NAV and hurdle-rate NPV all treat a fund's value as one number. In fact the value of an illiquid cash-flow stream depends on who holds it and in what state. A $1 distribution in year 1 is worth more to a fund whose liquidity constraint binds than to a secondary buyer with dry powder.

### Proposal: one currency, priced by the portfolio optimizer
Every action is treated as a bundle of state-contingent cash flows and resource usages. The bundle is priced with the duals of the portfolio-level multi-period program:

$$
\mathrm{Score}(i,a)=\underbrace{\sum_{s,t}\pi_{s,t}\,\Delta CF^{(i,a)}_{s,t}}_{\text{LAPV}}
-\lambda_R\,\Delta\mathrm{CVaR}^{(i,a)}-\lambda_{Lev}\,\Delta Lev^{(i,a)}-\sum_k\rho_k\,\Delta\mathrm{Floor}^{(i,a)}_k-\kappa^{irr}_{i,a}-\kappa^{GP}_{i,a}-\kappa^{tc}_{i,a}
$$

| Symbol | Meaning |
|---|---|
| $\pi_{s,t}$ | Dual of ADIC's cash balance in scenario $s$, quarter $t$, normalised so that $\pi_0=1$. Whenever the survival constraint binds, it already contains the one-period liquidity premium $\ell_{s,t}=\mu_{s,t}/(\pi_{s,t}-\mu_{s,t})$. |
| $\lambda_R$ | Price of the risk budget |
| $\lambda_{Lev}$ | Price of leverage capacity |
| $\rho_k$ | Price of the robust-floor constraint for model $k$ |
| $\kappa^{irr}, \kappa^{GP}, \kappa^{tc}$ | Charges for irreversibility (the waiting option given up), the GP relationship, and transaction costs |

We call the cash-flow term the **liquidity-adjusted present value (LAPV)**.
- It is an internal funds-transfer-pricing (FTP) curve in the bank-treasury sense [S: BCBS 2008; FSI 2011].
- Unlike a bank's FTP curve, it is derived from the optimizer rather than set administratively [I].

### Main results

**1. Two primitives, not four [I].** Every action combines two decisions:
- an *exposure* decision: sell / hold / add;
- a *financing* decision: borrow $b\ge0$ against the asset.

Under linear pricing the identity **LEVER ≡ ADD + REFI** holds exactly, apart from a small covenant interaction term. Here REFI's value already includes the leverage-capacity charge $\lambda_{Lev}\,b$. That gives four simple tests:

| Action | Choose it when |
|---|---|
| REFI | The all-in financing spread over $r_f$, plus $\lambda_{Lev}$, is below the life-weighted $\bar\ell$. |
| ADD | The forward $\alpha^*$ (versus the risk-matched funding basket) exceeds $\bar\ell$ plus the risk-budget charge. |
| LEVER | Both of the above hold. |
| SELL | The cash-equivalent bid exceeds the reservation price, i.e. LAPV(hold) + κ + option value. |

This decomposes the brief's rule ("lever if forward return − all-in cost − risk and liquidity penalties > 0") into parts the IC can check.

**2. Scale and explainability come from price decomposition.** The problem is *weakly coupled*: assets interact only through a few portfolio constraints.
- Everett's generalised-multiplier theorem shows that price-based choices are optimal for the resources they actually consume, even for discrete actions [S: Everett 1963].
- LP basic-solution theory and Shapley–Folkman-type bounds show that at most *m* assets (m = number of binding coupling constraints) are "split" in the convexified problem. The gap is bounded independently of the number of assets [S: Udell & Boyd 2016].

In a 40-asset test with four coupling constraints (Ex. 3):
- three binding prices reproduced 36 of the 40 exact-MILP decisions;
- the LP relaxation split exactly 3 assets;
- the gap was $2.9m on a $13.8bn book.

The pure price rule was feasible but $24.7m worse than the exact MILP. So the design keeps an exact MILP for the recommendation. Prices are used to explain it, and the few "marginal" assets become the IC's agenda [I].

**3. Worked example 1: 2018 buyout fund.**
- **Inputs:** NAV $500m; unfunded $50m; fused forward IRR 11% ± 6%; bid 88% of NAV; NAV loan at SOFR+600 and 15% LTV; liquidity price ℓ = 9% p.a. in years 1–2 and 4% thereafter.
- **HOLD** has a LAPV of **$421.4m** (84.3% of NAV). With free liquidity it would be worth $535.3m (107.1%). ADIC's liquidity state alone therefore moves the value by about 23% of NAV.
- **SELL for cash** nets **$434.5m**.
- **Best REFI:** a $75m loan with a 50% cash sweep, repaid inside two years, adds only **+$2.3m**. With ℓ = 0 the same loan would destroy $7.9m.
- **Verdict:** SELL beats HOLD+REFI by **$10.8m** (2.2% of NAV). The cash reservation price is **85.9%**.
- **What would flip it to keep:**
  - ℓ in years 1–2 below **7.4%**; or
  - fused forward IRR above **11.75%**; or
  - 50% of the price deferred 12 months. In that case the headline must reach **93.5%** to match 88% cash; 88% with that deferral is worth only $408.7m.
- **It is a close call.**
  - P(keeping turns out better) = **45%**.
  - The expected value of perfect information (EVPI) is about **$33m**. A competitive bid process and a bottom-up re-underwrite are worth paying for before executing.
- **Waiting a year** carries **$9.9m** of option value, but it is still **$8.5m worse** than selling now.
  - In stress paths only 11% would sell a year later, against 42% in normal paths.
  - The option to sell is weakest exactly when liquidity is needed.

**4. Worked example 2: LEVER is optimal.**
- **Asset:** a core-plus infrastructure interest. NAV $400m, forward return 11% ± 4%, cash yield 6.5%, β 0.5, hurdle 6.0%.
- **Financing:** a $120m asset-backed facility at SOFR+250; combined LTV 23%.
- **Ranking at ℓ = 4%** (Example 1's state from year 3 onward):

  | Action | Value vs HOLD |
  |---|---|
  | LEVER | **+$7.3m** |
  | REFI | +$5.8m |
  | ADD | +$1.5m |
  | HOLD | 0 |
  | SELL | −$44m |

- **The best action depends on ℓ:**

  | Flat ℓ | Best action |
  |---|---|
  | below ≈3.0% | ADD |
  | ≈3.0–4.4% | LEVER |
  | ≈4.5–8.4% | REFI |
  | ≥8.5% | SELL |

- In today's 9/9/4/4/4 state the same asset should be REFI'd (+$15.7m).
- Actions are properties of *asset × portfolio state*, not of assets alone [I].

**5. Market calibration (October 2026) [S].**

| Item | Value |
|---|---|
| LP portfolio pricing, H1 2026 (all strategies) | 87% of NAV |
| Buyout / infrastructure / credit / venture / real estate | 91% / 91% / 89% / 79% / 68% |
| Tail-end funds (10+ years) | 25%+ discounts |
| LP sales using deferrals | 26% |
| Source for the rows above | Jefferies, Jul-2026 |
| Fund-level NAV-loan target margins | 4.8% secured, 6.1% recourse-light, typically at 5–20% LTV (Rede, Jun-2026) |
| PE distributions | 14% of NAV in 2025, the fourth straight year below 15% (Bain 2026) |
| LP distribution yield | ~10% in H1 2026, against a 25% average since 2001 (Jefferies) |
| SOFR | 3.89% on 15-Oct-2026 (FRED) |

- Secondary buyers have outperformed sellers by about 5 pp/yr, or about 3 pp for funds aged 4–9 years [S: Nadauld et al. 2019; the 4–9-year figure is from the NBER WP 22404 abstract].
- That is consistent with the 5.7% implied liquidity spread in Example 1 [I].

**6. Behaviour and IC.**
- Since-inception IRR, paid-in capital and "discount to NAV" are sunk-cost or anchoring quantities.
- Each **decision card** instead shows:
  - the re-buy test;
  - the LAPV waterfall;
  - flip thresholds;
  - regret on both sides;
  - EVPI.
- The IC debates the prices and the few marginal assets, not every line.

---

## 2. Core concepts & theory

### 2.1 Illiquid holdings have investor-specific value

**The theory**
- **Longstaff (2001)** restricts investors to trading strategies of bounded variation.
  - They then behave as if they faced borrowing and short-sale constraints.
  - The model can sustain large illiquidity discounts and solves for the shadow cost of illiquidity [S].
- **Kahl, Liu & Longstaff (2003)** show that sale restrictions reshape investment and consumption. Holders must hedge the locked position and smooth spending before the restriction lapses [S].
- **Longstaff (2009)** studies assets that become untradeable for a blackout period: "Agents abandon diversification and choose polarized portfolios instead." Liquidity can be a large part of the equilibrium price [S].
- **Ang, Papanikolaou & Westerfield (2014)** find that *uncertainty* about how long illiquidity lasts is "a primary determinant of the cost of illiquidity". They add: "Investors are willing to forego 2% of their wealth to hedge against illiquidity crises occurring once every ten years." [S]

**Applied to private equity**
- **Sorensen, Wang & Yang (2014)** solve the limited partner's (LP's) portfolio problem with unspanned PE risk.
  - Fees, carry and illiquidity are all costly: "On average, LPs may just break even, net of management fees, carry, risk, and costs of illiquidity."
  - The authors' summary splits the LP's total costs as roughly 50% illiquidity, 25% management fees and 25% carry [S].
- **Dimmock, Wang & Yang (2024)** model an endowment whose locked alternatives can be sold at a proportional cost [S]. They find:
  - staggered lock-ups raise welfare;
  - the rebalancing boundaries are endogenous and move over time;
  - crisis illiquidity can push holdings far from targets.
- **Nadauld, Sensoy, Vorkink & Weisbach (2019)** use secondary-market data [S]:
  - buyers' PME averages 1.023, against 0.976 for sellers, a gap of about 5 pp a year (JFE abstract; the 2016 NBER WP 22404 abstract gives 0.974);
  - for the commonest trade, funds aged 4–9 years, the gap is about 3 pp (WP 22404 abstract; the JFE abstract gives no age split);
  - discounts relate to asymmetric information and market depth (WP 22404 abstract). The JFE abstract says "relatively flexible buyers earn returns by supplying liquidity to investors wishing to exit".

**Implication [I].** A fund interest has no single value. Its value to ADIC is the market-risk-adjusted value, adjusted again by ADIC's own path of liquidity premia. Buyers with low liquidity premia value the same cash flows more highly, so there are gains from trade precisely when ADIC's liquidity premium is high. The decision rule must therefore compare the bid with ADIC's *own* LAPV, never with NAV.

### 2.2 Real options and optimal stopping: why the textbook rule needs re-wiring

**The classics**
- **McDonald & Siegel (1986)** derive optimal timing for an irreversible investment. Under reasonable parameters, they show it can pay to wait until benefits are about twice the cost [S].
- **Dixit & Pindyck (1994)** generalise the logic: irreversibility plus uncertainty makes the option to wait valuable [S].
- **Brennan & Schwartz (1985)** add switching and mothballing, which produce hysteresis bands [S].
- **Abandonment.** Suppose the asset value $V$ follows GBM with volatility $\sigma$ and payout yield $\delta$, the discount rate is $r$, and the asset can be sold at a fixed price $P$. Then the standard result is to sell when $V\le V^*=\tfrac{\beta_2}{\beta_2-1}P$, where $\beta_2<0$ solves $\tfrac12\sigma^2\beta(\beta-1)+(r-\delta)\beta-r=0$. You sell only once value has fallen well below the price. That margin is the "irreversibility discount."

**Why it does not transfer directly [I]**
Secondary bids are quoted as a fraction $p_t$ of NAV. If NAV moves with economic value, fluctuations in $V$ create little option value. The real option is on three other things:
- **(a) the discount $p_t$.** It is procyclical and mean-reverting. The average high bid was 61% of NAV in the five months to November 2008 (Cogent, via PERE); LP pricing was 87–91% in H1 2026 [S].
- **(b) ADIC's own liquidity price $\ell_t$.**
- **(c) learning** about the forward IRR.

The correct formulation is an optimal-stopping problem on the state $X_t$ = (belief about the forward IRR, NAV, age, regime $z_t$, $p_t$, $\ell_t$):

$$
V_i(X_0)=\sup_{\tau}\ \mathbb{E}\Big[\sum_{t<\tau}\tilde\pi_t\,(D_{i,t}-C_{i,t})+\tilde\pi_\tau\big(p_{i,\tau}\,NAV_{i,\tau}(1-c)-\kappa^{GP}_i\big)\Big],
$$

where $\tilde\pi$ are the normalised state prices that already embed $\ell$.

**How to solve it**
- Use least-squares Monte Carlo (LSMC) on the simulator paths [S: Longstaff & Schwartz 2001].
- Bound the answer from above with duality-based upper bounds [S: Andersen & Broadie 2004; Brown, Smith & Sun 2010].

**The key qualitative finding (quantified in Example 1)**
- Bids are low in the same states in which ADIC's liquidity price is high.
- So the put-like option to sell later is worth least exactly where it would be exercised for liquidity.
- This argues for pre-emptive liquidity (sales in good markets, committed facilities) rather than reliance on crisis sales [I; consistent with Shleifer & Vishny 2011 and Dimmock, Wang & Yang 2024].
- Proportional costs create no-trade bands, in the spirit of Davis–Norman (1990) and of Dimmock, Wang & Yang's endogenous rebalancing boundaries [S for the latter].
- The irreversibility ranking is SELL (irreversible) > LEVER (partly reversible) > REFI (prepayable).
- $\kappa^{irr}$ equals the waiting option given up, which is what LSMC computes.

### 2.3 The shadow price of liquidity

**The scenario program.** Take a here-and-now scenario program with these constraints and duals:

| Constraint | Dual |
|---|---|
| Cash balance | $\pi_{s,t}$ |
| Liquidity-survival constraint | $\mu_{s,t}$ |
| IG + cash floor | $\phi_{s,t}$ |
| Distribution floor | $\nu_{s,t}$ |
| CVaR budget | $\lambda_R$ |
| Leverage cap | $\lambda_{Lev}$ |
| Robust floors (one per misspecification model) | $\rho_k$ |

**Deriving ℓ.** Cash can be carried forward at $r_f$. Complementary slackness on that carry gives
$\pi_{s,t}=(1+r_f)\sum_{s'\in\mathcal C(s)}\pi_{s',t+1}+\mu_{s,t}$, so the one-period liquidity premium is

$$
\ell_{s,t}=\frac{\mu_{s,t}}{\pi_{s,t}-\mu_{s,t}}.
$$

- Pricing cash flows with $\pi$ therefore compounds the liquidity premium along each path.
- The annualised average $\ell_t:=\mathbb E[\ell_{s,t}]$ is ADIC's internal FTP term-premium curve.
- The brief's "9% in years 1–2, falling to 4%" is exactly such a curve [I].

**Corporate-finance counterpart.** Bolton, Chen & Wang (2011) derive a double-barrier policy [S]:
- cash is paid out only at an upper cash-to-capital barrier;
- external funds are raised only once cash is exhausted;
- in between, the firm adjusts investment, asset sales and hedging.

In their notation $\ell=p'(w)-1$, the marginal value of liquid wealth above one [I]. The mapping to ADIC [I]:
- ADIC's distribution corresponds to their payout.
- Secondary sales and NAV loans correspond to their external finance and asset sales.
- The distribution within the 5–10% band should therefore be state-contingent: near 10% when $\ell\approx0$, near 5% when $\ell$ is high.

**Supporting evidence**
- Faulkender & Wang (2006) find the marginal value of cash "declines with larger cash holdings, higher leverage" and with better market access. That is direct evidence that liquidity's shadow value depends on state [S].
- Holmström & Tirole (1998) frame liquidity as a scarce, partly privately supplied good [S].
- Acharya & Pedersen (2005) show that required returns depend on how an asset's return and illiquidity covary with the market [S]. In scenario LAPV this is automatic: assets whose distributions dry up when $\ell$ spikes are penalised through the covariance of $\pi$ with cash flows [I].
- Brunnermeier & Pedersen (2009) show that margins and market liquidity can be "mutually reinforcing" [S]. Overlay margin calls and secondary discounts therefore spike in the same states.

**Bank treasury practice**
- **BCBS (2008)** calls for "allocating liquidity costs, benefits and risks to all significant business activities" [S].
- **The FSI's 2011 survey of 38 banks** criticised the use of "one average rate" [S]. It recommended:
  - marginal funding costs "matched to the maturity of the product or business activity at origination";
  - charging activities "based on their expected usage of contingent liquidity".
- **The ADIC translation [I]:**
  - the term structure of $\ell$ is the funding-maturity curve;
  - contingent-liquidity charges apply to unfunded commitments, overlay margin and NAV-loan covenant triggers.

**Basel LCR**
- The ratio must stay at or above 100% under a 30-day stress [S].
- Assumed drawdowns of undrawn committed facilities (LCR40.64) [S]:

  | Counterparty | Credit facility | Liquidity facility |
  |---|---|---|
  | Retail | 5% | 5% |
  | Non-financial corporates | 10% | 30% |
  | Banks | 40% | 40% |
  | Other financial institutions | 40% | 100% |
  | SPVs | 100% | 100% |

- Inflows are capped at 75% of outflows (LCR40.1) [S].
- Unfunded PE commitments are, economically, committed facilities extended *by* ADIC *to* GPs. The Basel table gives a conservative prior for stress drawdown rates, to be replaced by ADIC's own call data [I].

**Insurance.** Directive (EU) 2025/2 cuts the Solvency II risk-margin cost-of-capital rate from 6% to 4.75%, applying from 30 January 2027 [S]. That gives an external anchor for the annual price of tying up risk capital, $\lambda_R$ [I].

### 2.4 Decision theory: actions as priced bundles

**The bundle.** Each action is
$\mathcal B_{i,a}=(\Delta CF_{s,t},\ \Delta HQLA_{s,t},\ \Delta\mathrm{CVaR},\ \Delta Lev,\ \Delta U_{s,t},\ \text{irreversibility},\ \text{governance})$,
where $U$ is unfunded commitments, and it is valued by Score(·).

**Shortcut used in the worked examples.**
- Risky flows: $\tilde\pi_t\approx(1+r_h)^{-t}\prod_{k\le t}(1+\ell_k)^{-1}$.
- Contractual flows: $(1+r_f)^{-t}\prod(1+\ell_k)^{-1}$.
- $r_h$ is the expected return of the risk-matched funding basket, i.e. the deck's α\* benchmark.
- The full engine replaces this shortcut with scenario $\pi_{s,t}$.

**Primitives and the identity [I].**
- Exposure $e\in\{-\phi,0,+x\}$; financing $b\ge0$.
- Valuation: $V(e,b)=V_E(e)+V_F(b)-\lambda_{Lev}\,b\,\bar A+I(e,b)$.
  - $\bar A$ is the annuity factor over the loan's life.
  - $I$ captures covenant risk on the combined position. It is small at low LTV: P(LTV>40%) = 0.7% in Example 2.
- The actions are then: REFI = $(0,b)$, ADD = $(+x,0)$, LEVER = $(+x,b)$. Hence LEVER = ADD + REFI + I.

**Decision rules.** These are exact in LAPV; the annualised forms are approximations shown for intuition.
- **SELL** when $p^{\text{cash-eq}}_i\ge p^*_i=\big[\mathrm{LAPV}_i(\text{hold})+\kappa^{GP}_i+\kappa^{irr}_i-\lambda_R|\Delta\mathrm{CVaR}_i|\bar A\big]/NAV_i+c$.
  - Deferred consideration enters at $\tilde\pi^f_\tau$, not at face value.
- **REFI** when $s_B+f/T_{\text{eff}}+\lambda_{Lev}+\text{covenant charge}<\bar\ell_{[0,T_{\text{eff}}]}$.
  - $s_B=r_B-r_f$ is the borrowing spread, $f$ the upfront fee.
  - $T_{\text{eff}}$ is the weighted-average life after the cash sweep.
- **ADD** when $\alpha^*_i-\bar\ell_{[0,D_i]}-\lambda_R m_i-(p^{buy}_i-1)/D_i>0$.
  - $D_i$ is the cash-weighted life; $m_i$ is the marginal CVaR per dollar.
- **LEVER** when both ADD and REFI hold.
  - ADD alone: buy with cash.
  - REFI alone: borrow and keep the cash.

**The KKT interlock [I].** For a loan with $0\le b_i\le LTV_i\,NAV_i$ and $\sum b\le\bar B$, stationarity gives
$\bar\ell-s_B-f/T=\lambda_{Lev}+\eta_i-\zeta_i$.
If $\ell$ stays above the loan spread, then either the asset's LTV cap ($\eta_i$) or the portfolio leverage cap ($\lambda_{Lev}$) is binding. The optimizer therefore explains *why* cheap financing was not used more. In Example 1, ℓ = 9% sits above the 6.8% loan spread, so the 15% LTV cap binds.

**Implied cost of liquidity.** For any source:
- compute the IRR of the action's incremental cash flows;
- subtract the matching base rate ($r_h$ for forgone risky flows, $r_f$ for contractual debt).

Sorting sources by implied spread and capacity gives the **marginal-cost-of-liquidity (MCL) curve**, a merit order like power dispatch. At the optimum, $\ell$ equals the spread of the marginal source [I].

### 2.5 Price decomposition at scale (operations research)

**The decomposition**
- The asset problem is a weakly coupled program: each asset has its own discrete action set, and the assets are joined only by a few portfolio rows.
- Everett (1963) showed that multipliers work for arbitrary functions and sets. The method is "fail-safe" and well suited to allocating resources among independent activities [S].
- Adelman & Mersereau (2008) compare Lagrangian and approximate-LP relaxations for weakly coupled stochastic dynamic programs [S]. This is the dynamic case: timing sales across many funds.
- In the restless-bandit tradition of Whittle (1988), the multiplier acts as a subsidy and each project's break-even multiplier works as an index.
- Our analogue is a **liquidity index** $\ell^*_i$: the liquidity premium at which SELL ties HOLD+REFI. It is 7.4% in Example 1. Ranking funds by $\ell^*_i$ gives an *asset-level* MCL curve [I].

**How small the gap stays**
- In a basic optimal solution of the convexified LP, at most *m* assets, the number of binding coupling constraints, take mixed actions.
- Udell & Boyd show the suboptimality "is bounded by a term proportional to the maximal number of active constraints in the problem", and does not depend on the number of variables [S].

**Design consequences [I]**
1. Keep the *asset-level* coupling rows few. Aggregate scenario liquidity into expectation and CVaR rows per quarter; the full scenario detail stays in the portfolio LP and in simulation.
2. Implement split assets as **strip sales** or partial facilities. Jefferies reports that LPs strip-sold co-investments in H1 2026 [S].
3. Treat diversified portfolio sales as extra **columns**. Their price is not the sum of their parts: buyers pay for diversification and use recent vintages as "sweeteners" [S: Jefferies]. Asset scoring is then the pricing subproblem of column generation.

**Analogy [I].** Electricity markets price network constraints with locational marginal prices and handle unit-commitment non-convexities with uplift. $\ell_{s,t}$ is a "temporal LMP for cash", and the marginal assets are the uplift-eligible units.

### 2.6 Behavioural economics of divestment

| Bias | Evidence | How it shows up at ADIC |
|---|---|---|
| **Sunk cost** | Arkes & Blumer (1985) [S] | Arguing from since-inception IRR, TVPI, paid-in capital or "we've waited eight years". All are sunk and irrelevant. |
| **Disposition effect** | Shefrin & Statman (1985) [S] | The LP version [I]: selling near-NAV winners while riding tail-end losers to avoid "booking a loss versus NAV". Jefferies notes strip sales "to crystallize gains" in concentrated co-investments [S]. |
| **Anchoring** | Tversky & Kahneman (1974), classic | NAV is lagged and model-based. Fortune (Jun-2025) reports "NAV squeezing": buyers mark stakes up to the prior NAV for day-one gains [S]. The anchor should be the reservation price, not NAV. |
| **Status quo / escalation** | HOLD (or a re-up) is treated as the free default. | Lerner, Schoar & Wongsunwai (2007) find endowments are better at predicting which follow-on funds will perform [S]. Access is valuable, but it should be priced forward-looking ($\kappa^{GP}$), not inferred from history. |
| **Fire sales** | A fire sale is a "forced sale of an asset at a dislocated price" (Shleifer & Vishny 2011) [S]. | In 2008 HMC "shedded $1 billion in private equity at a loss" (Crimson) [S], while average high bids fell to 61% of NAV (Cogent) [S]. |

### 2.7 Portfolio interplay

**Tail-end versus core funds**
- *The market data [S: Jefferies H1 2026]:*
  - Tail-end funds (10+ years) traded at 25%+ discounts.
  - Funds in years 4–8 are the market's "sweet spot": buyout pricing averaged 91%, and the weighted-average vintage sold was 2018.
- *What follows [I]:*
  - Tail-end interests usually carry a much higher implied liquidity spread.
  - They are worth selling mainly when three things hold:
    - the remaining forward return is low;
    - per-position monitoring costs are material (26% of LP sellers cite wind-down / clean-up);
    - they can be bundled.
- *Bundling:*
  - Buyers use recent vintages as "sweeteners" to lift aggregate pricing [S], so bundle value is not additive.
  - Each candidate bundle therefore enters the MILP as its own column with its own quoted price [I].
  - A tail-end fund paired with an attractive core fund may clear when neither would alone.

**Diversification and vintage concentration [I]**
- Selling 2018–2020 vintages cuts exposure to the cohorts most stuck on DPI. It also tilts the remaining book toward 2021–2023 vintages, which carry the largest unfunded balances.
  - That raises calls, and hence $\ell$, in years 3–5.
  - The scenario duals capture this, because each action's future $\Delta CF$ is priced at future $\pi_{s,t}$.
  - The deterministic shortcut does not capture it. That is one reason production scoring uses scenario duals.
- Longstaff (2009) shows illiquidity pushes investors toward polarised, concentrated portfolios [S]. Concentrated co-investments earn CVaR relief through $\lambda_R$ when sold.
  - That relief is $3.8–11.5m in Example 1 at $\lambda_R$ = 1–3%.

**Unfunded transfer**
- In an LP sale the buyer assumes the unfunded commitment.
  - Its LAPV at $r_f+\ell$ is ADIC's liquidity relief: $27.7m in Example 1, on $30m of expected calls.
  - In stress the relief is larger. Calls are procyclical, though less so than distributions [S: Robinson & Sensoy 2016]. Basel-style drawdown priors apply.
- Buyers increasingly avoid unfunded-heavy positions; Jefferies notes "reducing demand for unfunded capital" in GP-led deals [S].
  - The bid model should therefore penalise unfunded share.
  - A bid with a high unfunded share may still be attractive to ADIC because the transfer is worth most when $\ell$ is high [I].

**GP relationships and re-up rights**
- *Why access matters:*
  - Endowments have shown skill in re-up decisions [S: Lerner, Schoar & Wongsunwai 2007].
  - Access to a top GP's next fund is a real option on future α\*.
- *Modelling it [I]:* treat it as $\kappa^{GP}_i=\Pr(\text{access loss}\mid\text{sale})\times\mathrm{LAPV}(\text{future }\alpha^*\text{ on planned re-ups})$.
- *Mitigants:*
  - sell to GP-approved buyers;
  - sell strips and keep a stub;
  - avoid selling during the GP's fundraise;
  - pre-clear transfers (consent and ROFR clauses are hard constraints).
- *GP-led choices.* For CV elections and GP-level NAV facilities, ADIC applies the same LAPV test as an LPAC member. The GP's choice is then priced at ADIC's own $\ell$.

---

## 3. Methods/models and trade-offs

| # | Method | What it delivers | Strengths | Weaknesses | Role at ADIC |
|---|---|---|---|---|---|
| 1 | Closed-form real options (GBM abandonment/waiting) | Irreversibility premium, intuition | Transparent | Wrong state variable for bids quoted as % of NAV; no portfolio constraints | Teaching, sanity checks |
| 2 | Hurdle-rate NPV vs NAV / discount-to-NAV | Quick screen | Familiar | Ignores ADIC's liquidity state; anchors on NAV | **Not** for decisions |
| 3 | LAPV with a deterministic ℓ term structure (Ex. 1–2) | Value per action, flip thresholds | Fast, explainable, spreadsheet-auditable | Ignores how ℓ covaries with cash flows | Screening, decision cards |
| 4 | Scenario LAPV with $\pi_{s,t}$ from the here-and-now LP | Values consistent with the optimizer; liquidity-risk covariance included | One currency everywhere | Duals are noisy or degenerate; needs a solved LP | Production valuation |
| 5 | LSMC optimal stopping on simulator paths, with dual bounds | Timing, option to wait, $\kappa^{irr}$ | Path-dependent, multi-factor | Regression bias; compute cost | Near-threshold assets only |
| 6 | Exact MILP on aggregated coupling rows | The recommended action set, including bundles | HiGHS handles ~10³ binaries in seconds | Needs aggregation of scenario rows | Recommendation engine |
| 7 | Lagrangian / price decomposition (Everett, Whittle-style indices) | Explanation, liquidity index, MCL | Decentralised and IC-friendly | ≤ m split assets; the price rule alone can be suboptimal (Ex. 3: −$24.7m) | Explanation, candidate generation |
| 8 | SDF-based PE valuation (strips; GPME) | Risk-adjusted base rate $r_h$ and betas by strategy | Market-consistent [S: Gupta & Van Nieuwerburgh 2021; Korteweg & Nagel 2016] | Data-hungry | Calibrating $r_h$, β |
| 9 | Robust duals (worst case over the misspecification ensemble) | Prices weighted toward the binding model | Aligned with the Tier-1 7% floor | Conservative | Tier-1 consistency |
| 10 | Decision analysis (EVPI, flip thresholds, tornado charts) | Value of more diligence; what would change the decision | IC-native | Needs predictive distributions | Decision cards |

**Trade-offs [I]**
- Methods 3, 4 and 6 form the production core:
  - 4 prices;
  - 6 decides;
  - 3 explains;
  - 5 is added only where a decision is within roughly the EVPI of the threshold.
- Method 2 is kept only as a *contrast column*, so the IC can see how much the liquidity state moves value; in Example 1 that is $114m.
- Method 9 matters because asset decisions should be robust to the same misspecification ensemble as the Tier-1 floor. Using worst-case-weighted duals keeps the two consistent.

---

## 4. Empirical evidence & current market data

| Metric | Value | As of | Source |
|---|---|---|---|
| Secondary volume, H1 2026 | $118bn total (LP-led $56bn, 47%; GP-led $62bn, 53%); FY2026E ~$260bn vs FY2025 record $240bn | 30-Jun-2026 | Jefferies Global Secondary Market Review, Jul-2026 [S] |
| Average LP portfolio pricing | 87% of NAV (flat vs YE2025) | H1 2026 | Jefferies [S] |
| Pricing by strategy | Buyout 91%; infrastructure 91%; credit 89% (from 91%); venture 79%; real estate 68% | H1 2026 | Jefferies [S] |
| Age / geography | Tail-end (10+ yrs) at 25%+ discounts; recent vintages at single-digit discounts; NA/Europe 86–88%; Asia/EM 35%+ discounts; weighted-average vintage sold 2018 | H1 2026 | Jefferies [S] |
| Structures | ~33% of LP sales structured; deferrals in 26% of LP sales; pref equity / managed funds / CFOs 7% | H1 2026 | Jefferies [S] |
| LP seller motives | Liquidity 45%; wind-down / clean-up 26%; rebalancing 16%; non-core 13% | H1 2026 | Jefferies [S] |
| LP supply | Pensions & SWFs 48%; FoF / secondary funds 27%; endowments & foundations 16% | H1 2026 | Jefferies [S] |
| Buyer capital | $290bn dedicated (from $327bn); overhang 1.2x | H1 2026 | Jefferies [S] |
| CV rollover | Average LP rollover 14%; CVs ~14% of sponsor-backed exits | H1 2026 | Jefferies [S] |
| Distribution yield | ~10% in H1 2026; below 20% since 2023; 25% average since 2001 | H1 2026 | Jefferies [S] |
| Distributions / NAV | 14% in 2025, the fourth year below 15%; 2014–17 average 29%, versus 11% annualised through Q3-2024 | 2025 / 2024 | Bain GPER 2026; Bain GPER 2025 [S] |
| Unsold inventory | ~32,000 companies worth $3.8tn; ~40% held more than 5 years; average hold ~7 years | YE2025 | Bain GPER 2026 [S] |
| LP constraint | 53% of LPs say undrawn commitments limit new commitments | 2025 | Bain GPER 2026 [S] |
| NAV-loan margins (fund level) | Weighted target 4.8% secured (5.2% prior) and 6.1% recourse-light (6.6% prior); banks 3.0% secured; 36% of lenders expect rises vs 17% falls | Jun-2026 | Rede NAV Report 2026 [S] |
| NAV-loan LTV | Conventional facilities "rarely exceed 20% LTV", and are seldom below 5% | Jun-2026 | Rede 2026 [S] |
| NAV-loan terms | Spreads mostly <5% over 3m Term SOFR; closing LTV mostly <25%; fees 1–2%, modal 1–1.5%; 5-year maturities common but WAL shorter because of sweeps; 63% LTV-based sweeps | FY2025 (pub. 2026) | Proskauer NAV survey [S] |
| Secondaries-fund facilities (diversified LP-interest collateral) | Spreads ≤3% (67%) or 3–4% (33%); closing LTV 25–50% (57%) or 50–75% (43%) | FY2025 | Proskauer [S] |
| Crisis pricing | Average high bid 61% of NAV in the five months to Nov-2008 | 2008 | Cogent, via PERE [S] |
| Buyer vs seller performance | PME 1.023 vs 0.976 (~5 pp/yr); ~3 pp for 4–9-yr funds per the NBER WP 22404 abstract, which gives 0.974 | sample to 2010s | Nadauld et al. 2019 [S] |
| Cash-flow cyclicality | Calls and distributions procyclical; distributions more so, so net flows are procyclical; funds calling in bad times outperform | 1984–2010 | Robinson & Sensoy 2016 [S] |
| Base rate | SOFR 3.89% (14-Oct: 3.88%) | 15-Oct-2026 | FRED [S] |

**Reading the evidence [I]**
- **Dispersion is the signal, not the average.** A 2018 buyout fund sits in the market's "sweet spot", while a tail-end real-estate fund faces a 25–35% discount. Implied liquidity costs therefore differ by more than 10 pp a year across a typical book. Jefferies itself warns: "Aggregate pricing data enclosed herein is not appropriate for the valuation of individual fund interests." [S]
- **Deferrals are disguised seller financing.** At ℓ = 9%, deferring half the consideration by 12 months costs about 5.5 points of headline: 93.5% is needed to match 88% cash (Ex. 1).
- **Capacity matters.** A $5bn ADIC programme would be about 9% of H1-2026 LP volume, so the price impact should be modelled as a concave function of size per half-year [I].
- **NAV-loan pricing is now bifurcated.** Banks price secured deals at ~3% and alternative lenders at ~5.6% [S]. Diversified LP-interest collateral prices tighter still [S]. For ADIC, a portfolio-level facility (a secondaries-fund-style SPV) is likely the cheapest REFI step on the MCL curve. The ADIC-specific terms are unknown and must be quoted [I].

---

## 5. Practitioner/peer practice & case studies

**Endowments as sellers**

*Harvard (HMC)*

| Year | What happened | Source |
|---|---|---|
| 2008 | Shed $1bn of PE "at a loss" | Crimson 2017 [S] |
| 2017 | Sold over $2bn of PE and real-estate interests (Lexington among buyers) | Crimson 2017 [S] |
| 2021 | Sold ~$1bn to Ardian | Crimson 2025 [S] |
| 2025 | Sold ~$1bn to Lexington, about 5% of the PE portfolio, with Jefferies advising. PE is ~40% of a $53bn endowment; planning began in 2024 amid a general decline in PE liquidity. | Crimson, 25-Apr-2025; Fortune, 15-Jun-2025 [S] |

*Yale (2025)*
- A sale of "select private equity fund interests" after a months-long review, reported at up to $2.5bn and later at nearly $3bn.
- Priced at a discount of "less than 10% to net asset value", with Evercore advising [S: PE Wire, 5-Jun-2025; Fortune, 15-Jun-2025].
- A spokesperson said Yale remains committed to PE and is still making new commitments [S: Institutional Investor].
- Press reports describe it as Yale's first secondary sale. We could not re-read that source this session.
- Unfunded PE commitments were $6.51bn at FY23 on a $41.4bn endowment [S: Institutional Investor].

*Lessons [I]*
- Sell routinely and in strong markets, in slices of about 5%.
- Prefer diversified, quality-first packages.
- Avoid deferrals when liquidity is the objective.
- Frame sales as portfolio management rather than distress. The 2008 losses came from selling into the trough.

**Market practice [S: Jefferies H1-2026]**
- Pensions and SWFs supply 48% of LP volume.
- 45% of LP sellers cite liquidity.
- One-third of LP deals are structured.
- Most LPs sell rather than roll in continuation vehicles: average rollover is 14%.
- Sell-versus-roll is exactly the SELL/HOLD decision, with the CV's new fee and carry terms included in the HOLD cash flows [I].

**NAV financing practice**
- Most facilities fund new and follow-on investments rather than distributions [S: Rede 2026].
- Lenders expect more DPI-motivated deals in 2026 [S].
- ILPA's July-2024 guidance [S, as summarised by Rede 2025]:
  - LPAC consent if the LPA is silent;
  - LPAC consent if proceeds fund distributions;
  - standardised disclosure.
- ADIC sits on LPACs, so the same LAPV test should score GP-level NAV-loan proposals [I]. A GP facility that accelerates distributions adds value to ADIC only if its all-in spread is below ADIC's ℓ over the facility's life.

**Bank treasury.** The FSI survey of 38 banks found deficient practice ("one average rate", manual updates, weak oversight) [S]. The recommended practice, which ADIC adopts directly [I], has three parts:
- central treasury ownership;
- marginal, maturity-matched rates;
- charges for contingent liquidity.

**Stochastic-programming ALM**
- The Russell–Yasuda Kasai multistage model added an estimated 42 bp of income, about ¥8.7bn (US$79m), in its first two years [S: Cariño et al. 1994].
- Kouwenberg (2001) addresses scenario generation for ALM stochastic programs [S].
- These are the lineage of the here-and-now LP whose duals price ADIC's actions.

**Insurance.** The cost-of-capital approach charges a fixed annual rate on required capital: 6% falling to 4.75% under Directive (EU) 2025/2 [S]. That is the template for $\lambda_R$ when ADIC lacks a binding risk constraint in the optimizer [I].

---

## 6. Design implications for the ADIC framework

### 6.1 Placement
The `action_economics` module has the following inputs and outputs [I].

**Consumes:**
1. Scenario cash flows from the private engine: $D_{i,s,t}, C_{i,s,t}, NAV_{i,s,t}$. Stream 04 builds that engine on the Takahashi & Alexander (2002) fund cash-flow model.
2. Fused forward beliefs, as predictive distributions.
3. Duals from the here-and-now optimizer: $\pi,\mu,\nu,\phi,\lambda_R,\lambda_{Lev},\rho$.
4. Instrument quotes: bids, deferral terms, facility term sheets.

**Produces:**
- `ActionBundle`s, Scores and flip thresholds;
- the MCL curve;
- decision cards.

These feed the MILP selector and the IC pack. The module creates no numbers outside deterministic tools (design principle P1).

### 6.2 State variables (per scenario s, quarter t)

| Variable | Symbol | Notes |
|---|---|---|
| Liquid / HQLA holdings, by haircut class | $L^k_{s,t}$ | Feeds the survival and IG+cash rows |
| Economic and reported NAV per holding | $NAV^{e}_{i,s,t}, NAV^{r}_{i,s,t}$ | Reported NAV lags. Bids reference the reported NAV. |
| Unfunded commitment | $U_{i,s,t}$ | Stress drawdown rates, with a Basel-style prior |
| Debt balance per facility | $B_{f,s,t}$ | With LTV, sweep and covenant state |
| Overlay margin / collateral | $M_{s,t}$ | From the overlay stream; contingent-liquidity charge |
| Regime | $z_{s,t}$ | Drives $p$, spreads, availability and $\ell$ |
| Secondary price | $p_{i,s,t}=\bar p_{\text{strat}}\cdot g(\text{age},\text{geo},\text{sector})\cdot h(z)$ | H1-2026 levels; stress $h\approx0.70$ (61/87) |
| Facility spread and availability | $s_{B,s,t}, A_{s,t}$ | Stress: +140 bp (the 2022 widening) [S: Rede 2025] and availability haircuts [I] |
| Distribution demand within the band | $Dist_{s,t}\in[5\%,10\%]\times NAV$ | Oil-linked demand comes from the liabilities stream |
| Risk and leverage usage | $\mathrm{CVaR}_{t}, Lev_{s,t}$ | Includes look-through fund-level leverage |

### 6.3 Decision variables

| Level | Variable | Domain |
|---|---|---|
| Asset | $x_{i,a}$ (HOLD, SELL‑φ, REFI‑b, ADD‑x, LEVER‑(x,b), ROLL/SELL in a CV, bundle membership) | Binary or SOS1; strips as fractional φ ∈ {0.25, 0.5, 1} |
| Asset | Sale timing τ | LSMC policy for near-threshold assets |
| Portfolio | Liquid rebalancing, commitments pacing, overlay notional, credit-line draws, distribution level within the band | Continuous, non-anticipative |

### 6.4 Constraints (portfolio rows that couple assets)

- **Cash balance** (dual $\pi_{s,t}$):
  $c_{s,t}=(1+r_f)c_{s,t-1}+\sum_{i,a}x_{i,a}\Delta CF^{(i,a)}_{s,t}+\text{liquid flows}+\Delta B-\text{interest}-Dist_{s,t}-\Delta M_{s,t}$.
- **Survival** (dual $\mu_{s,t}$): $c_{s,t}+\sum_k h_k L^k_{s,t}\ \ge\ \mathrm{P99}(M)+\text{stressed 12m net calls}$.
- **IG + cash ≥ 8% of NAV** (dual $\phi_{s,t}$).
- **Distribution floor** (dual $\nu_{s,t}$): $Dist_{s,t}\ge5\%$; cap at 10%.
- **Risk** (dual $\lambda_R$): CVaR$_{95}$ ≤ budget, using the Rockafellar–Uryasev linearisation.
- **Robust floor** (dual $\rho_k$): for each misspecification model $k$, the 5-year floor shortfall stays within the 5% tolerance.
- **Leverage** (dual $\lambda_{Lev}$): gross and look-through leverage ≤ cap.
- **Per asset:** $\sum_a x_{i,a}=1$, $b_i\le LTV_i\,NAV_i$ (dual $\eta_i$), GP-consent flags, and a minimum position size.
- **Market capacity:** sales per half-year ≤ $\kappa_{mkt}\times$ LP volume, with a concave price impact.
- **Aggregation for the asset MILP [I]:** use quarterly expected-liquidity rows plus CVaR-of-shortfall rows for quarters 1–8. That keeps *m* at 20 or fewer and the Shapley–Folkman gap small.

### 6.5 Dual extraction and normalisation

- Normalise $\tilde\pi_{s,t}=\pi_{s,t}/\pi_0$.
- Report the forward liquidity premium per quarter as $\ell^q_{s,t}=\mu_{s,t}/(\pi_{s,t}-\mu_{s,t})$, annualised as $(1+\ell^q)^4-1$.
- **Robust duals:** when the robust-floor rows bind, $\rho_k>0$ re-weights the scenarios toward model $k$. Asset scores then automatically favour actions that help in the binding model [I].
- **Stabilisation:**
  - Bootstrap K = 20 scenario subsets.
  - Report mean and 90% band for $\ell_t$, $\lambda_R$ and $\lambda_{Lev}$.
  - Score on the mean.
  - Flag actions whose sign flips within the band.
  - Prefer interior-point (CLARABEL) duals for explanation. They sit near the analytic centre of the optimal dual face, whereas simplex returns vertex duals [I].

### 6.6 Scoring, rules and flip thresholds

- **Score:** as defined in §1. Store each term separately for the waterfall.
- **Flip thresholds** are found by root-finding on Score(SELL) − Score(best keep), and stored with every recommendation (design principle P14):
  - reservation price $p^*$;
  - break-even forward IRR;
  - break-even $\ell$ (level shift over years 1–2);
  - break-even $\kappa^{GP}$;
  - deferral-equivalent headline.
- **Liquidity index** $\ell^*_i$ ranks SELL candidates. The asset-level MCL is the cumulative proceeds sorted by $\ell^*_i$.
- **Probabilities:** draw from the fused predictive distribution (and regimes). Report:
  - P(action is ex-post best);
  - expected regret for each alternative;
  - EVPI;
  - the action's ΔP(10% target) and ΔP(7% floor breach), from re-simulation.

### 6.7 MCL curve: sources and default parameters

Capacities come from ADIC data.

| Step | Source | Implied spread over base (default) | Stress behaviour | Basis |
|---|---|---|---|---|
| 1 | Cash/T-bills above the 8% floor | 0 | Available | [I] |
| 2 | Liquid public sales / rebalancing | Transaction cost; raises future ℓ by depleting the buffer | Prices fall; crystallises drawdowns | [I] |
| 3 | Physical-to-synthetic (sell physical, hold futures/TRS) | Implied futures financing spread over SOFR (desk to supply) + initial margin | Margin calls; contingent-liquidity charge | [I]; overlay stream |
| 4 | Committed lines / repo | Facility margin + commitment fee (ADIC terms) | Uncommitted lines can vanish | [P] |
| 5 | Diversified LP-portfolio facility (SPV) | ~SOFR+300–400; LTV 25–50% | Spreads widen; availability falls | Proskauer (secondaries-fund analogue) [S]; ADIC quote needed |
| 6 | Single-fund NAV loan | SOFR+480–610 + 1–1.5% fee; LTV 5–20% | +~140 bp, as in 2022 | Rede 2025/2026; Proskauer [S] |
| 7 | Preferred equity / structured secondary | Above step 6 (no verified 2026 benchmark) | Scarce | [P]; quotes needed |
| 8 | Secondary sale, cash | IRR(forgone) − $r_h$; Ex. 1: 5.7%; tail-end / RE / EM: much higher | Bids ~30% lower (2008: 61% average high bid) | Jefferies; Cogent [S] |
| 9 | Secondary sale with deferral | Step 8 plus ℓ × deferral share × deferral period | Same | [I] |
| 10 | Commitment pacing | Forgone vintage α\* plus relationship cost; affects calls only in years 2–5 | Pro-cyclical value | [I] |
| 11 | Distribution flexibility within the 5–10% band | Owner's marginal value of funds $\nu^{own}$ (policy input) | Hits the 5% floor | [I] |
| 12 | Tail-hedge monetisation | Negative cost in stress; carry in normal states | Pays when ℓ spikes | [I]; overlay stream |

### 6.8 Parameters with default values

| Parameter | Default | Basis |
|---|---|---|
| $r_f$ | SOFR 3.89% (15-Oct-2026); forward curve in production | FRED [S] |
| Funding-basket ERP | 4.25% (placeholder until the capital-market-assumptions (CMA) stream sets it) | [I] |
| β (to listed equity) | Buyout 1.2; growth 1.3; VC 1.5; core-plus infrastructure 0.5; private credit 0.4; RE value-add 0.8 | [I] placeholders; calibrate via strips / GPME |
| Secondary price $\bar p$ | 0.91 BO, 0.91 infrastructure, 0.89 credit, 0.79 VC, 0.68 RE; tail-end ≤ 0.75; Asia/EM −35%; stress multiplier ≈ 0.70 | Jefferies; Cogent [S] |
| Deferral | 26% incidence; model as a share at t+12m priced at $\tilde\pi^f$ | Jefferies [S] |
| Sale transaction cost $c$ | 0.75% of NAV | [P]/[I] |
| NAV loan | Spread 4.8% (secured) to 6.1% (recourse-light); fee 1.5%; LTV ≤ 15–20%; 50% sweep; maturity 4–5 years | Rede 2026; Proskauer [S] |
| $\kappa^{GP}$ | 0 for non-core tail-end; 0.3–1% of NAV for core GPs with re-up intent | [I] |
| $\lambda_R$ fallback | 3–5% p.a. per $ of CVaR (anchored on insurers' 4.75–6% cost of capital) | Directive (EU) 2025/2 [S] / [I] |
| $\ell$ fallback | 9%/9%/4% (brief) until optimizer duals are available | Brief |
| Unfunded stress drawdown prior | 40% (credit) to 100% (liquidity-type) per Basel LCR40.64; replace with ADIC call data | BCBS [S] / [I] |
| Base distribution yield | 10–14% of NAV p.a. (drought); normal 25–29% | Jefferies; Bain [S] |

### 6.9 Calibration targets
1. **Secondary prices** by strategy, age and geography (H1 2026), plus the stress level (61% in 2008).
2. **Deferral incidence** of 26%.
3. **NAV-loan terms:**
   - margins of 4.8% and 6.1%;
   - LTV of 5–20%;
   - fees of 1–1.5%;
   - LTV-linked sweeps in 63% of facilities.
4. **Distribution yields:** ~10% and 14% now, against a historical 25–29%.
5. **Implied liquidity cost check:** the median implied spread of executed LP sales should land near the 3–5 pp a year buyer–seller gap.
6. **Cash-flow cyclicality:** net flows should be procyclical, with distributions more cyclical than calls.
7. **Internal consistency:** in every quarter, ℓ should be close to the implied spread of the marginal MCL source actually used. A persistent gap means a missing constraint or a mis-specified source.

### 6.10 Data needs

**Per holding**
- Strategy, vintage, GP, geography and sector look-through, including software exposure, which buyers currently discount [S: Jefferies].
- Reported NAV and its date, plus an economic-NAV estimate.
- Unfunded commitment, cash-flow history, fee and carry terms.
- The three return series: underwritten, actual, forecast.
- Fund-level leverage: NAV facilities and subscription lines (ILPA disclosures).
- LPA transfer clauses: consent, ROFR, fees.
- GP tier and re-up intent.
- Quarterly indicative bids from at least two advisers, with deferral terms.
- Facility term sheets.
- CV election windows.

**Portfolio level**
- Liquidity sources and capacities.
- Credit lines and CSA terms.
- Overlay margin model.
- Distribution-policy parameters and the owner's $\nu^{own}$.
- Risk and leverage policy definitions.
- Scenario-set hashes (P2).

### 6.11 Worked example 1: 2018-vintage buyout fund (brief inputs)

**Assumptions** (beyond the brief; all [I])

| Assumption | Value |
|---|---|
| $r_f$ | SOFR 3.89% |
| β, so $r_h$ | 1.2, so $r_h=3.89\%+1.2\times4.25\%=8.99\%$ |
| Distribution rates (% of NAV, years 1–6) | 15/20/25/30/40/100%, calibrated to the drought (~17% of NAV in year 1, versus ~10% for the whole market) |
| Expected calls from the $50m unfunded | $15m / $10m / $5m at t = 0 / 1 / 2 |
| NAV compounding | At the fused 11%, so the forward IRR on NAV is exactly 11% |
| Sale costs | 0.75% of NAV; $\kappa^{GP}$ = $1.8m |
| NAV loan | $75m (15% LTV) at SOFR+600 = 9.89%, 1.5% fee, cash sweep of distributions net of calls |

**Expected cash flows** ($m; cash-weighted life 4.0 years)

| t | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Distributions D | 0 | 85.7 | 110.1 | 123.6 | 123.5 | 127.9 | 213.0 |
| Calls C | 15.0 | 10.0 | 5.0 | 0 | 0 | 0 | 0 |
| $DF_h$ ($r_h$+ℓ) | 1 | 0.842 | 0.709 | 0.625 | 0.551 | 0.487 | 0.429 |
| $DF_f$ ($r_f$+ℓ) | 1 | 0.883 | 0.780 | – | – | – | – |

**Values (LAPV, $m)**

| Action | Value | Comment |
|---|---|---|
| HOLD | **421.4** (84.3% NAV) | $\sum D\cdot DF_h-\sum C\cdot DF_f=449.2-27.7$ |
| HOLD if ℓ ≡ 0 | 535.3 (107.1%) | The liquidity state is worth −$114m |
| SELL, 88% cash | **434.5** | 440 − 3.75 − 1.8. The buyer assumes unfunded calls worth $27.7m in LAPV. |
| SELL, 88% with 50% deferred 12m | 408.7 | Deferral costs $25.7m at ℓ = 9% |
| SELL, 92% with 50% deferred 12m | 427.6 | Needs **93.5%** to match 88% cash |
| REFI, sweep 100% / 50% / 25% | +1.3 / **+2.3** / +2.0 | 50% sweep repays 37.9 + 48.9 by year 2. A 25% sweep runs into the 4% years. |
| REFI if ℓ ≡ 0 | −7.9 | Borrowing at 9.89% destroys value when liquidity is free |
| HOLD + best REFI | 423.7 | |
| **SELL − (HOLD+REFI)** | **+10.75** | Recommendation: SELL |

**Implied cost of each source**
- Sale: IRR 15.2%, i.e. 5.7% over $r_h$.
- NAV loan: IRR 11.0%, i.e. 6.8% over $r_f$.
- Against ℓ = 9% in years 1–2 and 4% later, the loan is cheap for its two-year life.
- The sale's 5.7% sits between the 9% and 4% regimes. That is why its sign depends on the term structure.

**Flip thresholds**
- Reservation price 85.9% (cash), or 108.2% if ℓ ≡ 0.
- Break-even ℓ for years 1–2: 7.4%.
- Break-even forward IRR: 11.75%.
- Break-even $\kappa^{GP}$: about $12.6m, i.e. SELL still wins by $2.55m at κ = $10m.

**Sensitivity: SELL minus best keep ($m)**

Only ℓ for years 1–2 varies; years 3+ stay at 4%.

| Price \ ℓ₁₋₂ | 0% | 4% | 6% | 9% | 12% |
|---|---|---|---|---|---|
| 80% | −102.9 | −66.8 | −50.2 | −29.3 | −10.9 |
| 84% | −82.9 | −46.8 | −30.2 | −9.3 | +9.1 |
| 86% | −72.9 | −36.8 | −20.2 | +0.7 | +19.1 |
| **88%** | −62.9 | −26.8 | −10.2 | **+10.7** | +29.1 |
| 91% | −47.9 | −11.8 | +4.8 | +25.7 | +44.1 |
| 94% | −32.9 | +3.2 | +19.8 | +40.7 | +59.1 |

**Probabilities** (forward IRR ~ N(11%, 6%), 50k draws)
- HOLD LAPV: P10 / P50 / P90 = 324.6 / 420.9 / 543.3.
- P(keeping is ex-post better) = 44.7%.
- Expected regret: SELL $32.9m; KEEP $36.2m.
- EVPI: $32.9m.

**Option to wait one year** (illustrative)
- Set-up:
  - 15% stress probability, with a 15% mark-down, exits halved, bids at 72% and ℓ spiking to 15% then 8%;
  - perfect learning of g by t+1, which makes this an upper bound on the option.
- Value with the option: $426.0m. Never selling, in the same scenarios: $416.1m. Option value: $9.9m.
- Selling now ($434.5m) still beats waiting by $8.5m.
- Share of paths that would sell at t+1: 42% in normal paths, 11% in stress paths.

**Portfolio duals**
- If the CVaR budget binds at $\lambda_R$ = 1% or 3%, SELL gains a further $3.8m or $11.5m.

**Recommendation for the IC.**
1. **SELL for cash**, ideally inside a diversified portfolio sale where 2018 vintages are the market's sweet spot.
2. **Fallback to REFI + HOLD if any of these holds:**
   - the cash-equivalent bid is below 85.9%;
   - the bid carries material deferral;
   - the optimizer's ℓ for years 1–2 falls below about 7.4%.
3. **Before signing:**
   - spend part of the ~$33m EVPI on competitive tension (≥ 3 bidders) and an asset-level re-underwrite of the forward IRR;
   - log the decision with its flip thresholds.

### 6.12 Worked example 2: a case where LEVER is optimal

**Assumptions** (illustrative)

| Item | Value |
|---|---|
| Asset | Core-plus infrastructure interest |
| NAV | $400m |
| Fused forward return | 11% ± 4% |
| Cash yield | 6.5% |
| β | 0.5, so $r_h=6.0\%$ and α\* = 5.0% |
| Increment | +$120m bought at NAV (co-invest top-up) |
| Financing | Asset-backed facility at SOFR+250 (6.39%), 0.75% fee, 5-year bullet; combined LTV 23% |
| Portfolio prices | $\lambda_R m$ = 0.45% p.a.; $\lambda_{Lev}$ = 0.25% p.a. |
| SELL reference | 91% bid |

**Value versus HOLD across portfolio states ($m)**

| Liquidity state (flat ℓ, 5 years) | SELL | REFI | ADD | LEVER | **Best** |
|---|---|---|---|---|---|
| 0% | −122.4 | −15.6 | +25.0 | +9.4 | ADD |
| 2% | −81.0 | −4.3 | +12.6 | +8.3 | ADD |
| 3% | −62.0 | +0.9 | +6.9 | +7.8 | **LEVER** |
| **4%** | −44.0 | +5.8 | +1.5 | **+7.3** | **LEVER** |
| 5% | −27.0 | +10.5 | −3.6 | +6.9 | REFI |
| 6% | −10.9 | +14.9 | −8.4 | +6.5 | REFI |
| 9% | +32.4 | +26.8 | −21.4 | +5.4 | SELL |
| Ex. 1 term structure (9/9/4/4/4) | −8.6 | +15.7 | −9.1 | +6.6 | REFI |

**Region boundaries:** ADD below ≈3.0%; LEVER ≈3.0–4.4%; REFI ≈4.5–8.4%; SELL ≥ 8.5%.

**Annualised decomposition at ℓ = 4%**

| Action | Calculation | Net |
|---|---|---|
| LEVER | α\* 4.99% − spread 2.50% − fee 0.15% − risk 0.45% − leverage 0.25% | ≈ 1.6% p.a. on $120m (exact LAPV: +$7.3m) |
| ADD | 4.99 − 4.00 − 0.45 | ≈ 0.5% |
| REFI | 4.00 − 2.50 − 0.15 − 0.25 | ≈ 1.1% |

LEVER beats both, as the identity requires.

**Other results**
- **Liquidity profile:** LEVER is self-funding. Net flows are +0.1, +0.5, +0.9, +1.2 and then +31.2 at exit, because the 6.5% yield exceeds the 6.39% coupon.
- **Break-even forward return:** 9.5% versus HOLD; 10.7% versus REFI.
- **Probabilities:**
  - P(LEVER beats HOLD) = 65%; P(LEVER beats REFI) = 53%.
  - LEVER value P10 / P50 / P90 = −16.0 / +7.5 / +35.0.
  - P(LTV > 40% at any point) = 0.7%.

**IC message.** LEVER needs three conditions together:
- a high-conviction α\*;
- financing cheaper than ADIC's internal liquidity price;
- a liquidity price that is moderate rather than acute.

Under acute scarcity the same asset should be financed (REFI) without adding exposure. Under abundance it should be bought with cash (ADD).

### 6.13 Worked example 3: price decomposition on 40 assets

**Set-up** (synthetic)
- 40 holdings, $13.8bn of NAV.
- Actions: HOLD, SELL, REFI (15% LTV, SOFR+600, 2-year bullet), LEVER (+30% at SOFR+300, only for 12 eligible low-β, high-return assets).
- Coupling rows: raise $3.8bn in year 1; year-2 surplus of $0.9bn; cut CVaR by $0.8bn; leverage ≤ $1.2bn.

**Results**

| Item | Result |
|---|---|
| Exact MILP (HiGHS) | 15 HOLD, 13 SELL, 2 REFI, 10 LEVER; objective −$104.9m |
| LP relaxation | Objective −$102.1m; gap **$2.86m** (0.02% of NAV) |
| Shadow prices | Year-1 liquidity **$0.161 per $**; risk **$0.103 per $** of CVaR cut; leverage **$0.033 per $**; year-2 liquidity 0 |
| Split assets in the LP | **3**, equal to the number of binding rows |
| Price-only rule | Feasible (raises $3.91bn, cuts CVaR by $0.88bn) but **$24.7m** worse; 4 disagreements, including both REFIs |
| Marginal assets | #3 (age 11, bid 0.868, β 1.39; LP 69% HOLD / 31% SELL); #14 (age 11, bid 0.888, forward 7.2%; 59/41); #33 (age 7, β 0.59; 26% HOLD / 74% LEVER) |

The marginal assets are the IC's agenda; the other 37 are explained by three prices [I].

### 6.14 IC decision card (one per asset; generated, never hand-edited)

1. **Recommendation and confidence:** P(best), regret on both sides, EVPI.
2. **LAPV waterfall:**
   - base value difference at $r_h$;
   - liquidity value;
   - unfunded relief;
   - risk relief or charge;
   - leverage charge;
   - $\kappa^{GP}$;
   - transaction costs;
   - option value.
3. **Flip thresholds:** $p^*$, IRR\*, ℓ\*, κ\*, and the deferral-equivalent price.
4. **Re-buy test:** "Would we buy this position today at the bid, given our liquidity state?"
5. **Market evidence:** bids, comparable pricing by strategy and age, capacity.
6. **Relationship and legal:** consent, ROFR, re-up plan.
7. **Behaviour flags:**
   - since-inception IRR shown only greyed out;
   - NAV shown only alongside economic NAV.
8. **Alternatives considered:** strip sale, deferral, NAV loan, preferred equity, CV roll.

### 6.15 Agentic integration (summary; detail in the architecture stream)
- **Deterministic tools:** `score_actions`, `flip_thresholds`, `mcl_curve`, `select_actions_milp`, `lsmc_timing`.
- **LLM agents:**
  - extract LPA transfer clauses and GP notes;
  - challenge narratives for sunk-cost or NAV-anchoring language;
  - build the devil's-advocate case from the flip thresholds;
  - draft cards that cite registry metric IDs only (P7).
- The IC owns the decision (P1, P8). Overrides are logged together with the flip thresholds the IC accepted.

---

## 7. Implementation notes

**Pipeline (per quarterly run)**
1. Solve the portfolio here-and-now LP to get $\pi,\mu,\lambda$. Use CLARABEL for central duals and HiGHS for speed or ranging.
2. Vectorise $\Delta CF^{(i,a)}_{s,t}$ for all actions on a scenario subsample (e.g. 500 × 12 quarters).
3. Compute scores: `einsum('st,ast->a', pi, dCF)` minus the resource terms.
4. Run the MILP over the aggregated coupling rows and bundle columns.
5. Re-solve the LP with the selected actions fixed. Iterate the duals 2–5 times with damping.
6. Validate on the *held-out final* scenario set and the misspecification ensemble (P3).
7. Run LSMC timing only for assets whose score is within the EVPI of zero.
8. Compute flip thresholds with `scipy.optimize.brentq`.

**Libraries**
- numpy, scipy (`linprog` and `milp` with HiGHS; `brentq`);
- cvxpy 1.9 with CLARABEL/HiGHS for `constraint.dual_value`;
- numba for LSMC regressions;
- pydantic for `ActionBundle` and `ActionScore` schemas.

All are present in the lab environment.

**Interface contract (proposal)**
- `ActionBundle`:

  | Field | Type / shape |
  |---|---|
  | `holding_id` | – |
  | `action` | enum |
  | `params` | – |
  | `dCF` | float64 [S, T] |
  | `dHQLA` | float64 [S, T] |
  | `dCVaR` | float |
  | `dLev` | float |
  | `dUnfunded` | [S, T] |
  | `irreversible` | bool |
  | `kappa_gp`, `kappa_tc` | float |
  | `provenance` | quote IDs and dates |

- `DualSet`:

  | Field | Shape / type |
  |---|---|
  | `pi` | [S, T] |
  | `mu` | [S, T] |
  | `lambda_R`, `lambda_Lev` | float |
  | `rho` | [K] |
  | `bands` | – |
  | `scenario_hash` | – |
  | `engine_hash` | – |

- Units: US$ millions; quarterly grid; rates annualised at the interface.

**Complexity**
- Scoring is O(A·S·T): 1,500 actions × 500 × 12 ≈ 9×10⁶ multiply-adds, i.e. milliseconds.
- A full [S, T] cube at 2,000 × 40 for 1,500 actions would be about 1 GB. Score on a subsample and validate in the simulator instead.
- A MILP with ~1,500 binaries and ≤ 30 coupling rows solves in seconds (Ex. 3: 160 binaries, instant).
- LSMC costs O(paths·T·K²) per asset, so restrict it to candidates.

**Numerical pitfalls**
1. **Sign conventions.**
   - scipy `ineqlin.marginals` are ≤ 0 for ≤-rows in a minimisation; negate them for a maximisation written as `min −f`.
   - cvxpy duals have their own sign conventions; unit-test them with a ±δ RHS perturbation.
2. **Degeneracy.** Duals may not be unique. Report left and right finite-difference derivatives and HiGHS ranging.
3. **Scenario noise.** Bootstrap the bands, and do not act on actions whose sign flips inside them.
4. **Level versus rate.** $\mu/\pi$ is per period. Annualise consistently, and never mix quarterly ℓ with annual $r_h$.
5. **Double counting.** $r_h$ already prices market risk. $\lambda_R$ is ADIC's *internal* surcharge and is non-zero only when the risk row binds. Likewise, the secondary discount is a market price and ℓ is an internal value; both enter, without overlap.
6. **Deferred consideration** is buyer credit risk. Price it at $r_f$ + ℓ + a buyer spread.
7. **Churn.** Re-optimising quarterly with noisy duals can flip decisions. Use hysteresis bands of about EVPI / NAV and minimum holding periods, in the spirit of Dimmock, Wang & Yang's no-trade boundaries.
8. **Overfitting.** Repeated re-scoring against the same scenarios inflates apparent value. Charge every evaluation to the counted budget (P4).
9. **Stale NAV.** Bids reference a lagged reported NAV. Model $NAV^r$ as a smoothed $NAV^e$, and compute $p$ against the correct one.

---

## 8. Risks, pitfalls & limitations

**Model risk**
- **Belief risk.** Forward IRRs come from the fusion stream. In Example 1 an upward revision of just +0.75 pp (to 11.75%) flips the decision from SELL to keep.
- **Endogenous ℓ.** ℓ is produced by the model, so mis-specified liquidity sources or constraints propagate into every asset decision. Calibration target 7 in §6.9 is the guardrail.
- **Close calls are normal.** Many asset decisions are near coin-flips: P = 45% in Example 1. The *portfolio* outcome is still reliable because many partly independent decisions aggregate [I]. The IC should judge the process and the prices, not individual hits.

**Market**
- **Reflexivity and capacity.** If many LPs sell into the same window, prices fall. ADIC-scale programmes need explicit price impact.
- **Adverse selection.** Discounts reflect asymmetric information [S: Nadauld et al., NBER WP 22404 abstract]. Buyers may cherry-pick, so bundle design matters.
- **Information leakage.** A sale process can signal distress. Keep sales routine, and frame them as portfolio management, as Yale did by stressing its continued commitment to PE.

**Governance**
- **Relationships.** GP consent, ROFR and relationship damage are hard to price, and $\kappa^{GP}$ is judgmental. Show the break-even κ rather than pretend precision.
- **Misuse.** "Liquidity premium" could become an excuse for selling good assets cheaply to fund distributions. Requiring the KKT interlock (ℓ ≈ marginal source cost) and the market-capacity check guards against this [I].

**Legal and tax.** Transfer restrictions and tax leakage on sales or financing (jurisdiction-specific) are outside the model's scope. They enter as $\kappa$ terms or hard constraints.

**Limitations of the worked examples**
- The examples use a deterministic ℓ term structure and CAPM-style $r_h$, not scenario duals.
- Distribution schedules, β, $\kappa^{GP}$, costs and stress parameters are illustrative.
- Example 3 is synthetic.
- Waiting-option values assume perfect learning, so they are upper bounds.

---

## 9. Open questions

1. **Owner's value of distributions.** What is the sovereign owner's marginal value of a distribution dollar ($\nu^{own}$), and is the 5–10% band a decision variable or a fixed rule set by the owner?
2. **ADIC's own facility terms.** What would ADIC obtain for a diversified LP-interest facility (spread, LTV, recourse, sweep), given its sovereign status? A quote is needed to place MCL step 5.
3. **Unfunded stress drawdowns.** What are ADIC's empirical stress drawdown rates on unfunded commitments by strategy and vintage, to replace the Basel prior?
4. **Market impact.** How much can ADIC sell per half-year before it moves prices? A price-impact curve from advisers' data is needed.
5. **Which duals decide.** Should asset decisions use expected or robust (worst-case-weighted) duals? We recommend robust duals for SELL and LEVER, the irreversible or levered actions, and expected duals for REFI [I]. This needs IC policy sign-off.
6. **Margin in ℓ.** How should overlay margin needs (tail hedge versus opportunistic book) enter the survival row: one P99 add-on or scenario-wise collateral flows? This is shared with the overlay stream.
7. **Co-investments.** Concentrated single assets need asset-level, not fund-level, belief fusion and bid models. What data exists?
8. **Scoring $\kappa^{GP}$.** Can GP-relationship value be estimated from ADIC's own re-up history (access outcomes after past sales)?
9. **Bundle prices.** Can bundle (portfolio-sale) pricing be learned from adviser books, given the diversification premium and sweetener effects?
10. **GP-level proposals.** Should GP-level NAV facilities and CV proposals routinely run through the same scoring before ADIC votes on LPACs?

---

## 10. References

Access dates are 2026-10-18 unless noted. Items marked † were first written from memory. The 2026-10-18 citation check confirmed their bibliographic details against Crossref records, and each now carries its DOI.

**Academic: valuation, liquidity, real options**
- Acharya, V. V., & Pedersen, L. H. (2005). Asset pricing with liquidity risk. *Journal of Financial Economics*, 77(2), 375–410. https://ideas.repec.org/a/eee/jfinec/v77y2005i2p375-410.html
- Ang, A., Papanikolaou, D., & Westerfield, M. M. (2014). Portfolio choice with illiquid assets. *Management Science*, 60(11), 2737–2761. NBER WP 19436: https://www.nber.org/papers/w19436
- Bolton, P., Chen, H., & Wang, N. (2011). A unified theory of Tobin's q, corporate investment, financing, and risk management. *Journal of Finance*, 66(5), 1545–1578. NBER WP 14845: https://www.nber.org/papers/w14845
- Brennan, M. J., & Schwartz, E. S. (1985). Evaluating natural resource investments. *Journal of Business*, 58(2), 135–157. https://ideas.repec.org/a/ucp/jnlbus/v58y1985i2p135-57.html
- Brunnermeier, M. K., & Pedersen, L. H. (2009). Market liquidity and funding liquidity. *Review of Financial Studies*, 22(6), 2201–2238. https://ideas.repec.org/a/oup/rfinst/v22y2009i6p2201-2238.html
- Dimmock, S. G., Wang, N., & Yang, J. (2024). The endowment model and modern portfolio theory. *Management Science*, 70(3), 1554–1579. NBER WP 25559: https://www.nber.org/papers/w25559
- Dixit, A. K., & Pindyck, R. S. (1994). *Investment under Uncertainty*. Princeton University Press. https://press.princeton.edu/books/hardcover/9780691034102/investment-under-uncertainty
- Faulkender, M., & Wang, R. (2006). Corporate financial policy and the value of cash. *Journal of Finance*, 61(4), 1957–1990. https://ideas.repec.org/a/bla/jfinan/v61y2006i4p1957-1990.html
- Gupta, A., & Van Nieuwerburgh, S. (2021). Valuing private equity investments strip by strip. *Journal of Finance*, 76(6), 3255–3307. https://ideas.repec.org/a/bla/jfinan/v76y2021i6p3255-3307.html
- Holmström, B., & Tirole, J. (1998). Private and public supply of liquidity. *Journal of Political Economy*, 106(1), 1–40. https://ideas.repec.org/a/ucp/jpolec/v106y1998i1p1-40.html
- Kahl, M., Liu, J., & Longstaff, F. A. (2003). Paper millionaires: How valuable is stock to a stockholder who is restricted from selling it? *Journal of Financial Economics*, 67(3), 385–410. NBER WP 8969: https://www.nber.org/papers/w8969
- Korteweg, A., & Nagel, S. (2016). Risk-adjusting the returns to venture capital. *Journal of Finance*, 71(3), 1437–1470. DOI 10.1111/jofi.12390.†
- Lerner, J., Schoar, A., & Wongsunwai, W. (2007). Smart institutions, foolish choices: The limited partner performance puzzle. *Journal of Finance*, 62(2), 731–764. https://ideas.repec.org/a/bla/jfinan/v62y2007i2p731-764.html
- Longstaff, F. A. (2001). Optimal portfolio choice and the valuation of illiquid securities. *Review of Financial Studies*, 14(2), 407–431. https://ideas.repec.org/a/oup/rfinst/v14y2001i2p407-31.html
- Longstaff, F. A. (2009). Portfolio claustrophobia: Asset pricing in markets with illiquid assets. *American Economic Review*, 99(4), 1119–1144. https://www.aeaweb.org/articles?id=10.1257/aer.99.4.1119
- McDonald, R., & Siegel, D. (1986). The value of waiting to invest. *Quarterly Journal of Economics*, 101(4), 707–727. NBER WP 1019: https://www.nber.org/papers/w1019
- Nadauld, T. D., Sensoy, B. A., Vorkink, K., & Weisbach, M. S. (2019). The liquidity cost of private equity investments: Evidence from secondary market transactions. *Journal of Financial Economics*, 132(3), 158–181 (online 2018). DOI 10.1016/j.jfineco.2018.11.007. Earlier version: NBER WP 22404 (July 2016), https://www.nber.org/papers/w22404. The WP abstract gives a seller PME of 0.974, the 4–9-year split and the asymmetric-information wording; the JFE abstract gives 0.976.
- Robinson, D. T., & Sensoy, B. A. (2016). Cyclicality, performance measurement, and cash flow liquidity in private equity. *Journal of Financial Economics*, 122(3), 521–543. https://ideas.repec.org/a/eee/jfinec/v122y2016i3p521-543.html
- Shleifer, A., & Vishny, R. (2011). Fire sales in finance and macroeconomics. *Journal of Economic Perspectives*, 25(1), 29–48. https://www.aeaweb.org/articles?id=10.1257/jep.25.1.29
- Sorensen, M., Wang, N., & Yang, J. (2014). Valuing private equity. *Review of Financial Studies*, 27(7), 1977–2021. NBER WP 19612: https://www.nber.org/papers/w19612. Cost split from the authors' summary: https://corpgov.law.harvard.edu/2014/01/12/valuing-private-equity/
- Takahashi, D., & Alexander, S. (2002). Illiquid alternative asset fund modeling. *Journal of Portfolio Management*, 28(2), 90–100. DOI 10.3905/jpm.2002.319836.†

**Academic: optimisation, decomposition, stopping, decision analysis**
- Adelman, D., & Mersereau, A. J. (2008). Relaxations of weakly coupled stochastic dynamic programs. *Operations Research*, 56(3), 712–727. https://ideas.repec.org/a/inm/oropre/v56y2008i3p712-727.html
- Andersen, L., & Broadie, M. (2004). Primal-dual simulation algorithm for pricing multidimensional American options. *Management Science*, 50(9), 1222–1234. https://ideas.repec.org/a/inm/ormnsc/v50y2004i9p1222-1234.html
- Brown, D. B., Smith, J. E., & Sun, P. (2010). Information relaxations and duality in stochastic dynamic programs. *Operations Research*, 58(4-part-1), 785–801. https://ideas.repec.org/a/inm/oropre/v58y2010i4-part-1p785-801.html
- Cariño, D. R., et al. (1994). The Russell–Yasuda Kasai model: An asset/liability model for a Japanese insurance company using multistage stochastic programming. *Interfaces*, 24(1), 29–49. DOI 10.1287/inte.24.1.29. https://ideas.repec.org/a/inm/orinte/v24y1994i1p29-49.html
- Everett, H. (1963). Generalized Lagrange multiplier method for solving problems of optimum allocation of resources. *Operations Research*, 11(3), 399–417. https://ideas.repec.org/a/inm/oropre/v11y1963i3p399-417.html
- Howard, R. A. (1966). Information value theory. *IEEE Transactions on Systems Science and Cybernetics*, 2(1), 22–26. DOI 10.1109/TSSC.1966.300074.†
- Kouwenberg, R. (2001). Scenario generation and stochastic programming models for asset liability management. *European Journal of Operational Research*, 134(2), 279–292. https://ideas.repec.org/a/eee/ejores/v134y2001i2p279-292.html
- Longstaff, F. A., & Schwartz, E. S. (2001). Valuing American options by simulation: A simple least-squares approach. *Review of Financial Studies*, 14(1), 113–147. https://ideas.repec.org/a/oup/rfinst/v14y2001i1p113-47.html
- Udell, M., & Boyd, S. (2016). Bounding duality gap for separable problems with linear constraints. *Computational Optimization and Applications*, 64(2), 355–378 (online 25 Jan 2016). DOI 10.1007/s10589-015-9819-4. Preprint: arXiv:1410.4158 (v2, Jan 2016). https://arxiv.org/abs/1410.4158
- Whittle, P. (1988). Restless bandits: Activity allocation in a changing world. *Journal of Applied Probability*, 25(A), 287–298. DOI 10.2307/3214163.†

**Academic: behaviour**
- Arkes, H. R., & Blumer, C. (1985). The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*, 35(1), 124–140. https://ideas.repec.org/a/eee/jobhdp/v35y1985i1p124-140.html
- Shefrin, H., & Statman, M. (1985). The disposition to sell winners too early and ride losers too long: Theory and evidence. *Journal of Finance*, 40(3), 777–790. https://ideas.repec.org/a/bla/jfinan/v40y1985i3p777-90.html
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131. DOI 10.1126/science.185.4157.1124.†

**Regulatory and official**
- Basel Committee on Banking Supervision (2008). *Principles for Sound Liquidity Risk Management and Supervision* (25 Sep 2008). https://www.bis.org/publ/bcbs144.htm
- Basel Committee on Banking Supervision (2013). *Basel III: The Liquidity Coverage Ratio and liquidity risk monitoring tools* (7 Jan 2013). https://www.bis.org/publ/bcbs238.htm. Drawdown rates are in Basel Framework LCR40.64, with the inflow cap in LCR40.1: https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30
- Financial Stability Institute (2011). *Liquidity transfer pricing: a guide to better practice*. FSI Occasional Paper No. 10 (30 Dec 2011). https://www.bis.org/fsi/fsipapers10.htm. The landing page names no individual author.
- Directive (EU) 2025/2 (Solvency II amendments): cost-of-capital rate cut from 6% to 4.75%, applying from 30 Jan 2027. As summarised by William Fry: https://www.williamfry.com/knowledge/solvency-ii-reform-key-changes/
- Federal Reserve Bank of St. Louis, FRED: SOFR series (obs. 15-Oct-2026: 3.89%). https://fred.stlouisfed.org/series/SOFR

**Practitioner and market data**
- Bain & Company (2026). *Global Private Equity Report 2026*. https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/
- Bain & Company (2025). *Global Private Equity Report 2025*. https://www.bain.com/insights/outlook-is-a-recovery-starting-to-take-shape-global-private-equity-report-2025/
- Jefferies (Jul 2026). *Global Secondary Market Review*. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf. Corroborated by Abbott Capital, *H1 2026 PE Market Overview*: https://www.abbottcapital.com/h1-2026-private-equity-market-overview/
- Rede Partners (Jun 2026). *NAV Financing Market Report 2026*. https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026 (PDF linked there).
- Rede Partners (Jun 2025). *NAV Financing Market Report 2025*. https://www.rede-partners.com/news-insights-database/nav-financing-report-2025
- Proskauer (2026). *Insights on the NAV Financing Market, Full Year 2025*. https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025
- PERE / PEI (archived article). "Study: Secondaries pricing falls 28%" (Cogent Partners; 61% average high bid in the five months to Nov-2008). https://www.pei-privaterealestate.com/equity/study-secondaries-pricing-falls-28/

**Case studies**
- The Harvard Crimson (25 Apr 2025). HMC planning ~$1bn PE stake sale to Lexington. https://www.thecrimson.com/article/2025/4/25/private-equity-stake-sales/
- The Harvard Crimson (2 Jul 2017). HMC selling private equity; 2008 sale "at a loss". https://www.thecrimson.com/article/2017/7/2/HMC-selling-private-equity
- Fortune (15 Jun 2025). Harvard and Yale PE stake sales; NAV discounts and "NAV squeezing". https://www.fortune.com/2025/06/15/harvard-yale-private-equity-holdings-sale-net-asset-value-discounts-nav-squeezing
- Private Equity Wire (5 Jun 2025). Yale nears $2.5bn secondary sale. https://www.privateequitywire.co.uk/yale-nears-2-5bn-secondary-sale-of-pe-and-vc-stakes/
- Institutional Investor (2025). Yale's potential PE sale won't solve liquidity challenges. https://www.institutionalinvestor.com/article/2eplivly10nvujo3sqzuo/corner-office/yales-potential-pe-sale-wont-solve-liquidity-challenges

**Named for completeness only (verified 2026-10-18).** These four works are cited only conceptually, and no claims depend on them.
- Davis, M. H. A., & Norman, A. R. (1990). Portfolio selection with transaction costs. *Mathematics of Operations Research*, 15(4), 676–713. DOI 10.1287/moor.15.4.676. Topic: transaction-cost no-trade regions.
- Gribik, P., Hogan, W., & Pope, S. (2007). Market-clearing electricity prices and energy uplift. Harvard Electricity Policy Group working paper, December 2007. https://www.hks.harvard.edu/publications/market-clearing-electricity-prices-and-energy-uplift. Topic: convex-hull pricing. The literature check's index record dates it 2008; the Harvard Kennedy School publication page gives December 2007.
- Hawkins, J. T. (2003). A Lagrangian decomposition approach to weakly coupled dynamic optimization problems and its applications. PhD thesis, MIT, Operations Research Center and Sloan School of Management. http://hdl.handle.net/1721.1/29599. Topic: Lagrangian decomposition of weakly coupled DPs. The repository record spells the title "Langrangian".
- Myers, S. C., & Majd, S. (1990). Abandonment value and project life. *Advances in Futures and Options Research*, 4, 1–21 [unverified: these publication details come from a citing bibliography found by the literature check; Crossref has no record, OpenAlex was unavailable, and the full text was not read]. Working-paper version: Myers, S. C., & Majd, S. (1983). Calculating abandonment value using option pricing theory. MIT Sloan School of Management Working Paper 1462-83. https://ideas.repec.org/p/mit/sloanp/2056.html. Topic: abandonment value.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 and `research/literature/08_action_valuation.lit.md` ("fix N" is item N of that file's §1 "Fixes" list; "row N" is its §2 table). Metadata was checked against Crossref, IDEAS/RePEc, NBER, MIT DSpace and Harvard Kennedy School pages on 2026-10-18.
- §2.1, Ang, Papanikolaou & Westerfield (2014): "drives most of its cost" → "a primary determinant of the cost of illiquidity", the abstract's wording (fix 1; verification #19).
- §2.1, Nadauld et al. (2019): seller PME 0.974 → 0.976, per the cited JFE abstract (fix 2; synthesis §2.3 makes the same fix for streams 04 and 07). The ~3 pp split for 4–9-year funds and the asymmetric-information and market-depth wording are now attributed to the 2016 NBER WP 22404 abstract, which gives 0.974; the JFE abstract's liquidity-supply sentence is quoted.
- §4 table, Nadauld et al.: "PME 1.023 vs 0.974" → "PME 1.023 vs 0.976", with the 4–9-year figure attributed to WP 22404.
- §1 item 5 and §8 "Adverse selection", Nadauld et al.: the citations now name WP 22404 for the 4–9-year figure and for the asymmetric-information claim.
- §10, Nadauld et al.: added 132(3), 158–181 and the WP date (July 2016), and noted which version gives which figure.
- §10, Udell & Boyd (2016): added the journal version, *Computational Optimization and Applications* 64(2):355–378, DOI 10.1007/s10589-015-9819-4 (Crossref); arXiv:1410.4158 kept as the preprint (fix 3; row 30).
- §10, Takahashi & Alexander (2002): orphan resolved by citing it in §6.1 as the base model of stream 04's private engine; pages 90–100 added from Crossref (fix 5; row 21).
- §10, † note: all five † items (Korteweg & Nagel, Takahashi & Alexander, Howard, Whittle, Tversky & Kahneman) confirmed against Crossref (fix 7). Added DOI 10.1111/jofi.12390 to Korteweg & Nagel and DOI 10.1126/science.185.4157.1124 to Tversky & Kahneman, and removed "metadata from memory" from the §2.5 Whittle mention.
- §10, Cariño et al. (1994): added the subtitle and DOI 10.1287/inte.24.1.29 from Crossref (row 25).
- §10, named-only works: "Not verified this session" replaced by full entries for Davis & Norman (Crossref), Hawkins (MIT DSpace) and Gribik, Hogan & Pope (HKS page). Myers & Majd's 1990 details are marked [unverified]; their 1983 MIT working paper is confirmed on IDEAS (fix 6; rows 35–38).
- Gribik, Hogan & Pope, the audit's one mismatch for this stream (synthesis §2.3; fix 4; row 38): title added; year kept at 2007, now confirmed by the HKS publication page (December 2007); 2008 is the index record year.
- §2.2: added the year to the in-text Davis–Norman mention.
- No change needed: the co-investment barrier (Broadie–Glasserman–Kou) re-run, the Gredil, Liu & Sensoy cross-file item (synthesis §2.6 item 5, which concerns the literature file) and the re-check lists for streams 10, 11, 13, 14 and G3 touch no work, number or claim in this dossier.
