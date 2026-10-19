# Stream 01: Multi-Period Portfolio Optimization and Sequential Decision Methods for ADIC

**Project:** ADIC Robust Target-Attainment TPA Lab | **Stream:** 01 (MPO core) | **As of:** 2026-10-18 | **Version:** 1.0

**Evidence tags:** **[S]** sourced fact (citation in section 10) | **[P]** practitioner or academic consensus | **[I]** our inference or design proposal.

**Verification note:** the session's shared web-search quota ran out partway through this stream. After that, all checks used direct fetches of primary pages (arXiv/ar5iv, RePEc/IDEAS, publisher pages, Bain, FRED, BIS). References not verified in this session are marked *(unverified)*. ADIC figures come from the client brief and the v8 deck, not from public sources. Any arithmetic about ADIC is illustrative and tagged [I].

---

## 1. Executive summary

1. **The problem class.** [I] ADIC faces a sequential decision problem with these features:
   - risk-averse and only partially observed;
   - quarterly decisions over 20-40 stages;
   - hundreds of private positions whose cash flows are lagged, outside ADIC's control, and dependent on the market regime;
   - mixed-integer asset actions (SELL / HOLD / REFINANCE / LEVER, with fixed costs and minimum sizes);
   - portfolio leverage subject to margin and collateral;
   - a derivatives overlay with convex payoffs;
   - hard requirements: the 5-10% annual distribution, liquidity survival, IG + cash >= 8% of NAV, and a robust 7% floor.

   Exact dynamic programming is intractable. A full scenario tree with 5 branches per quarter over 20 quarters would have about 10^14 leaves. Deep reinforcement learning is unsuitable as a fiduciary decision engine.

2. **Recommended architecture.** [I] A three-layer hybrid of Powell's policy classes:
   - **L1, Here-and-now Decision Program (HDP).** A direct lookahead (DLA): a three-stage stochastic MILP/LP. Stage 1 is today. Stage 2 is a regime-branching node around one year out. Stage 3 is a fan of paths out to year three.
     - First-stage decisions are asset-level SELL/HOLD/REFINANCE/LEVER actions. Recourse is modelled at strategy-group level.
     - Tier-1 limits enter as CVaR constraints. The terminal value comes from L2's cuts.
     - It returns today's actions, a contingent playbook, dual prices, and VSS/EVPI diagnostics. The key dual is a **shadow price of liquidity** indexed by scenario, quarter and regime.
   - **L2, Strategic value layer.** A value-function approximation (VFA): Markov-regime SDDP on an aggregated 15-30-dimensional state over 40 quarters. Its cost-to-go cuts are the fund's analogue of the hydro-power "water value": they put a price on liquidity and on illiquid NAV.
   - **L3, Policy simulator.** 10k-50k paths over 40 quarters, written in JAX/numba.
     - It tunes interpretable parametric policies (PFA/CFA) using common random numbers with CMA-ES or Bayesian optimization.
     - It benchmarks those policies against certainty-equivalent MPC and against the HDP itself, re-solved quarterly on a subsample of paths.
     - It validates on fresh seeds and on alternative scenario generators.
     - It reports outcome probabilities. Information-relaxation bounds certify how far any policy is from the best achievable.

3. **Design insights.** [I]
   - (a) **Liquidity shadow prices put all four actions in one currency.** Each action is a source or use of cash with a time profile. Valued at the cash dual $\lambda_t^s$, the actions line up in a *liquidity merit order*, like generators in power dispatch. The same prices give an internal funds-transfer-pricing curve, as in bank treasury. SELL wins when the secondary discount is smaller than the gap between cash today and the asset's continuation value at shadow prices. REFINANCE wins when the implied liquidity rate exceeds SOFR plus the facility spread.
   - (b) **IRR targets are linear.** For the owner's cash flows, $P(\mathrm{IRR}\ge r)=P(\mathrm{NPV}_r\ge 0)$. So the 7% floor and the 10% target become CVaR and shortfall constraints in an LP, which scale to thousands of scenarios.
   - (c) **Optimize convex surrogates; report the probability.** Maximizing $P(\text{return}\ge 10\%)$ directly rewards target-chasing.
   - (d) **Use the scenario approach only where it is cheap.** At ε = 5% and β = 1%, the exact Campi-Garatti bound needs 631 scenarios for a convex program with 20 decision variables, and 31,785 for a 1,500-variable asset-level program. So L1 uses CVaR approximations. The guarantee also requires a convex scenario program in which the constraint is enforced on all $N$ scenarios. An L3 policy tuned by CMA-ES through a non-convex simulator meets neither condition, so L3 certifies a fixed, already-tuned policy with out-of-sample binomial (Clopper-Pearson) bounds on held-out seeds and generators. [corrected 2026-10-18: the dossier gave roughly 1,000 and about 60,000, which come from the looser sufficient condition, and concluded that "L3 uses scenario-approach certification"; see verification #18 and R3]

4. **Evidence base.** [S]
   - Multistage stochastic programming has a long applied record. Russell-Yasuda Kasai reported +42 bp, about US$79m, of extra income over FY1991-92. InnoALM has been used at Siemens since 2000. Towers Perrin built CAP:Link/OPT:Link.
   - In simulation, stochastic programming dominates fixed-mix (Fleten, Hoyland and Wallace 2002), but only with good scenario generation (Kouwenberg 2001).
   - MPC with illiquid commitments comes close to a fictional fully liquid benchmark over 20 periods (Luxenberg et al. 2022).
   - MPC that raises risk aversion with drawdown controls drawdowns at little cost in mean-variance efficiency (Nystrup et al. 2019).

5. **Calibration warning.** [S] PE distributions have been below 15% of NAV for four straight years. In the 12 months to Q3 2025 they were about 14%, the lowest since 2008-09 (Bain, Feb 2026). [I] A stationary pacing calibration from 2021, such as mean distribution intensity $\bar\delta=0.33$/yr, would overstate private cash generation by roughly 2-2.5x. The low-DPI regime must be an explicit Markov state.

---

## 2. Core concepts and theory

### 2.1 Powell's unified framework, applied to ADIC

Powell writes every sequential decision problem in five elements [S Powell 2019; Powell 2021, preprint arXiv:1912.03513]:

- state $S_t$;
- decision $x_t=X^\pi(S_t)$;
- exogenous information $W_{t+1}$;
- transition $S_{t+1}=S^M(S_t,x_t,W_{t+1})$;
- objective $\max_\pi \mathbb{E}\{\sum_t C(S_t,X^\pi(S_t))\mid S_0\}$, or a general risk operator $\rho$ in place of the expectation.

The state has three parts: physical ($R_t$), informational ($I_t$) and belief ($B_t$).

Policies fall into two strategies with four classes:

- **Policy search:**
  - *PFA* (policy function approximation): parametric rules.
  - *CFA* (cost function approximation): a deterministic optimization whose costs or constraints are modified by tunable parameters, such as buffers or slack.
- **Lookahead:**
  - *VFA* (value function approximation): Bellman recursion with an approximate value function.
  - *DLA* (direct lookahead approximation): optimization over an approximate model of the future, such as MPC or a scenario tree.

Powell holds that the "vast majority" of real problems are solved with the policy-search classes [S]. He warns that stochastic lookaheads make simulation-based tuning hard and urges "caution" with neural networks. He notes that the classes can be hybridized, and the architecture below relies on that.

**Mapping to ADIC** [I]:

| Element | ADIC content |
|---|---|
| $R_t$ (physical state) | Liquid holdings by sleeve. For each private position: NAV, unfunded commitment, age, asset-level debt. Fund-level debt and its maturity ladder. Overlay book: tail-hedge notionals, strikes and expiries; opportunistic-sleeve risk usage. Collateral posted and received. Cash. Year-to-date distributions. |
| $I_t$ (information) | Prices, curves, volatility surfaces, credit spreads, secondary discount by strategy, NAV-loan spreads and availability, macro factors |
| $B_t$ (beliefs) | Regime posterior $\pi_t$ (the v8 HMM/HSMM engine). Fused forward-return beliefs per asset $(\mu_{i,t},\sigma_{i,t})$, built from underwritten, actual and forecast returns. Ambiguity radius (model confidence). |
| $x_t$ (decisions) | Liquid trades; new commitments by group; asset-level sell fraction, refinance draw or lever amount (with binaries); fund borrowing; overlay notional and strikes; opportunistic risk budget; distribution within the 5-10% band, if ADIC has discretion |
| $W_{t+1}$ (exogenous) | Public returns; private NAV marks (smoothed and lagged); calls and distributions; secondary discounts; spread and margin shocks; option payoffs and variation margin; regime transitions; the owner's cash demand |
| Objective | Lexicographic. Tier 1 is a set of robust constraints. Tier 2 is growth or target attainment net of shadow costs. |

### 2.2 Dynamic programming and what it teaches

The Bellman equation is

$V_t(S_t)=\max_{x\in\mathcal{X}_t(S_t)}\{C_t(S_t,x)+\mathbb{E}[V_{t+1}(S^M(S_t,x,W_{t+1}))\mid S_t,x]\}$.

- **Merton (1969) and Samuelson (1969)** [S]. With i.i.d. returns and CRRA utility, the optimal policy is myopic and constant-mix, $\pi^*=(\mu-r)/(\gamma\sigma^2)$, so the horizon does not matter. [P] Long-horizon structure comes only from three sources, and all three are first-order at ADIC:
  - investment opportunities that change over time, which create intertemporal hedging demands (Campbell and Viceira 2002);
  - liabilities or consumption;
  - frictions.
- **Illiquidity.** [S]
  - Ang, Papanikolaou and Westerfield (2014): non-trading intervals of uncertain length raise effective risk aversion and make it state-dependent, lowering allocations to both liquid and illiquid risky assets. The uncertainty of the non-trading interval, more than its length, drives the cost. Investors would give up about 2% of wealth to hedge illiquidity crises that occur once a decade.
  - Dimmock, Wang and Yang (2024): with lock-ups and proportional liquidation costs, rebalancing boundaries are endogenous and time-varying. Liquidity diversification across staggered lock-ups raises welfare. In crises, holdings deviate sharply from targets.
  - [I] Implications for ADIC:
    - SELL/HOLD has a no-trade band whose width scales with the secondary discount.
    - Laddering vintages and lock-ups is a liquidity asset in its own right.
    - Penalties for tracking target weights should relax in crisis regimes.
- **Approximate DP by simulation and regression.** [S] Brandt, Goyal, Santa-Clara and Stroud (2005) solve discrete-time portfolio choice by simulating paths and recursing backward, regressing conditional expectations on state variables. The method handles many state variables, path dependence, constraints and learning. It is the portfolio counterpart of Longstaff-Schwartz (2001) least-squares Monte Carlo for optimal stopping. [I] For ADIC it is the natural tool for estimating each asset's *continuation value*: HOLD versus SELL is an optimal-stopping problem with a liquidity-adjusted payoff.
- **Curse of dimensionality.** [P/I] A 10-point grid on 20 aggregated state variables has 10^20 cells, and ADIC's raw state has thousands of dimensions. Exact DP is useful only for intuition and for validating approximations, on toy models with 1-3 states (for example liquid wealth × regime × unfunded ratio).

### 2.3 Stochastic programming: recourse, trees and diagnostics

The two-stage problem is

$\max_{x\in X}\ c^\top x+\mathbb{E}_\xi[Q(x,\xi)]$, where $Q(x,\xi)=\max_y\{q(\xi)^\top y : Wy=h(\xi)-T(\xi)x,\ y\ge 0\}$.

The multistage version adds non-anticipativity: a decision at node $n$ may depend only on the history up to $n$. With sample average approximation (SAA) over $S$ scenarios, the deterministic equivalent is an LP or MILP of size $O(S\cdot H\cdot n)$ [P].

**Here-and-now vs recourse decisions.** Only the first-stage $x$ is implemented. The recourse $y$ is a *contingent plan*. [I] Aggregated by regime, it gives the IC a playbook. For example: "if a crisis regime arrives in Q3, draw the NAV facility first and pause commitments; sell LP interests only if the regime lasts beyond two quarters."

**Fan vs tree pitfall.** [P/I] A two-stage *fan* branches once and then follows deterministic paths, so recourse can see the future along each path. This overstates flexibility and pushes the first stage toward aggressive choices. Three remedies:
- a short multistage tree for the first 4-8 quarters;
- recourse restricted to decision rules (section 3.5);
- SDDP.

**IC diagnostics** [S Birge 1982]. For a maximization problem:
- WS is the wait-and-see value (perfect information);
- RP is the value of the recourse problem;
- EEV is the expected value of the mean-value solution;
- they satisfy $\mathrm{WS}\ge\mathrm{RP}\ge\mathrm{EEV}$, with $\mathrm{EVPI}=\mathrm{WS}-\mathrm{RP}$ and $\mathrm{VSS}=\mathrm{RP}-\mathrm{EEV}$.

[I] How the IC reads them:
- **VSS** is the value of planning for uncertainty instead of planning on the strategy groups' point forecasts.
- **EVPI** caps the value of better forecasting or regime detection, which helps set research priorities.
- **Value of an option class** generalizes the idea. Re-solve without the NAV facility, without the overlay, or without secondary-market access. The difference in objective, and in floor-breach probability, prices that capability.

### 2.4 Risk measures and time consistency

**CVaR** (Rockafellar and Uryasev 2000, standard formula; the PDF was fetched but could not be machine-read):

$\mathrm{CVaR}_\alpha(L)=\min_\eta\{\eta+\tfrac{1}{1-\alpha}\mathbb{E}[(L-\eta)^+]\}$.

It is LP-representable with one auxiliary variable per scenario.

**Time consistency.** [S Shapiro 2009] A policy is time consistent if decisions optimal today remain optimal at later states without reference to states that can no longer happen. Nested (recursive) coherent risk measures are time consistent and compatible with SDDP [S Philpott and de Matos 2012]. A CVaR of terminal wealth, or a five-year chance constraint fixed at $t=0$, is not.

[I] Choices for ADIC:
- Use static CVaR and chance constraints in L1. L1 is re-solved every quarter, so time inconsistency shows up as plan revisions, which the IC should expect.
- Use nested EAVaR (a mix of expectation and AVaR) sparingly in L2.
- In L3, judge every policy on the IC's own metrics, not on the optimizer's internal risk measure.
- If losses make the 7% floor infeasible, switch Tier 1 to "minimize breach probability" (a recovery mode) rather than declaring the problem infeasible.

### 2.5 Chance constraints and convex approximations

The Tier-1 requirement $P_Q(\text{floor breach})\le\varepsilon$ for every $Q$ in an ambiguity set is non-convex. There are four ways to handle it:

1. **CVaR approximation.** [P] $\mathrm{CVaR}_{1-\varepsilon}(g(x,\xi))\le 0$ implies $P(g>0)\le\varepsilon$. It is convex and conservative.
   - [S] Nemirovski and Shapiro (2006) construct a general class of convex conservative approximations. Their "Bernstein" approximation requires the constraint to be affine in independent perturbations.
   - [I] ADIC's risks are correlated, so CVaR is the default.
2. **Scenario approach.** [S] The scenario approach (Calafiore and Campi 2006), with the exact bound of Campi and Garatti (2008, Thm 2.4).
   - Enforce the constraint on $N$ i.i.d. scenarios. For a convex program with $d$ decision variables, $P^N\{V(x_N^*)>\varepsilon\}\le\sum_{i=0}^{d-1}\binom{N}{i}\varepsilon^i(1-\varepsilon)^{N-i}$, and the bound is exact for "fully supported" problems. Calafiore and Campi's original bound, $\binom{N}{d}(1-\varepsilon)^{N-d}$, is looser.
   - The guarantee requires a convex scenario program in which the constraint is enforced on all $N$ scenarios. Integer actions, or a policy tuned through a non-convex simulator, break it.
   - A commonly quoted sufficient condition is $N\gtrsim(2/\varepsilon)(d+\ln(1/\beta))$; the constant is quoted from memory.
   - [I] With $\varepsilon=5\%$ and $\beta=1\%$, the exact bound gives $N=631$ for $d=20$ policy parameters and $N=31{,}785$ for $d=1{,}500$ asset-level variables. [corrected 2026-10-18: the dossier gave about 1,000 and about 60,000, which are the sufficient condition's 984 and 60,184; recomputed, matching verification #18]
3. **Distributionally robust CVaR over a Wasserstein ball.** [S] Mohajerin Esfahani and Kuhn (2018): finite convex reformulations, often LPs, with finite-sample guarantees. This formalizes the v8 gate on "plausible misspecification" (cross-link: robust/scenario stream).
4. **Model-set robustness.** [I] Take the worst-case CVaR over a few generators, for example a Student-t HMM, an empirical block bootstrap and a crisis-overweighted mixture. This is the easiest version for an IC to understand.

### 2.6 Duals, shadow prices and bounds

[P] In an LP, a constraint's dual equals the marginal objective value of relaxing it. [S] SDDP's cuts are built from these duals: Pereira and Pinto (1991) assemble piecewise-linear cost-to-go functions from stage duals. [P] In hydro scheduling, the dual of the reservoir balance is the marginal "water value".

[I] The ADIC analogue is $\lambda_t^s$: the dual of the cash balance at quarter $t$ in scenario $s$, divided by $p_s$. It is the marginal value of $1 of cash. From it, define the **implied liquidity rate**

$\rho_t^s=\lambda_t^s/\mathbb{E}[\lambda_{t+1}\mid s_t]-(1+r^f_t)$.

The rate is near zero when liquidity is ample and spikes at stressed nodes.

**Bounds** [S] (Brown, Smith and Sun 2010; Haugh, Kogan and Wang 2006). Information relaxation gives an upper bound on any policy: let the decision maker see the future, but charge a penalty for using it. The penalized perfect-information problem bounds the optimal value, so the gap certifies how good a heuristic policy is. Boyd et al. (2014) build an SDP-based quadratic bound for multi-period investment, and the ADP policy that falls out of it is "typically close" to the bound.

---

## 3. Methods, models and trade-offs

### 3.1 Multistage stochastic programming for ALM

- **Russell-Yasuda Kasai** [S]. A multistage stochastic LP for a Japanese insurer.
  - Five explicit years, then an infinite-horizon steady-state period to handle end effects.
  - Regulatory, tax and cash-flow constraints, with penalties for violations.
  - Reported +42 bp, ¥8.7bn or about US$79m, of extra income in FY1991-92.
- **InnoALM** [S]. A multistage stochastic LP for Siemens Austria's pension fund.
  - Period lengths can vary, and correlation matrices depend on the market state.
  - It solves fast enough for interactive use and has been in use since 2000.
- **Towers Perrin** [S]. Three components: CAP:Link, a scenario generator projecting 10-40 years; OPT:Link, the optimizer; and FIN:Link, the reporting module. [I] This generator / optimizer / reporter split is the decomposition the agentic layer needs.
- **Dantzig and Infanger (1993)** [S]. Multistage portfolio stochastic LPs solved with Benders decomposition plus importance sampling, allowing inter-period dependence.
- **Scenario generation matters.** [S]
  - Kouwenberg (2001) found that stochastic programming performance "could be improved drastically" with a better tree, for example moment-matched instead of randomly sampled.
  - Hoyland and Wallace (2001) match moments with a nonlinear program. A published comment (Klaassen 2002) shows that matching statistics alone can create arbitrage, so no-arbitrage constraints should be added.
  - Pflug and Pichler's (2012) nested distance is the right metric for reducing multistage trees.
- **Bank ALM** [S]. Kusy and Ziemba (1986) built a 5-year stochastic LP for a credit union. It outperformed the deterministic LP with comparable effort.

[P/I] **Trade-off.** Explicit trees allow any constraint, any risk measure and integer first-stage decisions. But they grow exponentially with the number of stages, so they suit 2-4 stages, not 40 quarters.

### 3.2 SDDP and its variants

[S] SDDP (Pereira and Pinto 1991) approximates each stage's cost-to-go with Benders cuts. It alternates sampled forward passes with backward passes that add cuts from the duals, so no state discretization is needed. The original paper solved a 39-reservoir system. A 2025 *SIAM Review* survey covers theory, extensions and computation (Füllner and Rebennack 2025).

- **Markov-chain (regime) SDDP.** Cuts are indexed by regime $j$: $V_{t+1}(x,j)$.
  - [S] Valladão, Silva and Poggi (2019) solve a time-consistent portfolio problem with per-period CVaR limits, transaction costs and a Markov factor model, with up to 100 assets and 5 factors.
  - [S] Dowson's (2020) *policy graph* generalizes linear, Markovian and cyclic (infinite-horizon) structures. He shows that end-of-horizon effects in finite models disappear with an infinite-horizon graph.
- **Risk aversion.**
  - [S] Philpott and de Matos (2012) bring time-consistent coherent risk measures into SDDP.
  - [S] SDDP.jl provides Expectation, AVaR, CVaR, EAVaR, ConvexCombination, Entropic, ModifiedChiSquared, Wasserstein and WorstCase. Its documentation warns that the lower bound is no longer valid with non-expectation risk measures.
  - [S] Kozmík and Morton (2015) show that the standard upper-bound estimator performs poorly under risk aversion and propose importance-sampling estimators, tested on multistage asset allocation.
- **Integers.** [S] SDDiP (Zou, Ahmed and Sun 2019) uses Lagrangian cuts that are tight for binary states. [I] For ADIC, keep integers in the first stage only.
- **Software.** [S] SDDP.jl runs about 30% slower than a C++ implementation on the New Zealand hydro benchmark. msppy (Python, using Gurobi) implements SDDP and SDDiP and discretizes continuous processes into Markov chains.

[I] **Trade-off.** SDDP scales easily in stages (40 is easy) and handles state dimensions in the tens. It requires stagewise independence or a Markov chain, convexity, and a moderate state dimension. It is therefore suited to an *aggregated* ADIC model (groups, not 300 assets), and its cuts become L1's terminal value. Random returns that multiply state variables are allowed: each realization stays an LP, so the cuts remain valid.

### 3.3 Decomposition at scale (hundreds of assets × thousands of scenarios)

- **Benders / L-shaped.** [P] A first-stage master problem at asset level, possibly with integers, plus scenario subproblems solved in parallel. It fits ADIC's structure: an integer first stage with LP recourse.
- **Progressive hedging (PH).** [S] (Rockafellar and Wets 1991)
  - Each scenario is solved with an augmented-Lagrangian penalty pulling it toward the implementable average, and the multipliers are updated by $w_s\leftarrow w_s+\rho(x_s-\bar x)$.
  - It converges for convex problems and is a strong heuristic for MIPs.
  - Watson and Woodruff (2011): variable-specific $\rho$, acceleration and oscillation handling matter in practice.
  - mpi-sppy (built on Pyomo) runs PH with asynchronous bound and heuristic "spokes" around a hub. It reached tight optimality gaps within minutes on the largest known stochastic unit-commitment MIPs (Knueven et al. 2023).
- **Price decomposition across assets.** [I]
  - Dualize the coupling cash-balance constraint. Each asset then picks the action $a$ that maximizes $\text{value}(a)-\lambda\cdot\text{cash used}(a)$, and $\lambda$ is updated until liquidity clears.
  - With about 300 nearly separable assets, the duality gap caused by each asset's non-convexity is small relative to the total. This is a Shapley-Folkman-type argument (standard, *not re-verified in-session*).
  - The clearing price is the "liquidity price" an IC can reason about.
- **Structure-exploiting interior-point methods.** [S] Gondzio and Grothey solved a quadratic financial-planning problem with more than 10^9 variables on 1,280 processors (2006). That scale is possible but unnecessary for ADIC.

### 3.4 Model predictive control (rolling horizon)

[S] Boyd et al. (2017) cast trading as convex optimization in two forms:
- **Single-period (SPO).** The objective is forecast return, minus γ × risk, minus transaction cost (including a $|x|^{3/2}$ market-impact term), minus holding cost.
- **Multi-period (MPO).** Plan $H$ periods with plug-in forecasts and execute only the first.
- Hyperparameters are tuned by back-testing, and the authors note they "can greatly affect" performance.
- Their S&P 500 example uses $H=2$. Solves took about 0.15 s per period, and MPO cost grows roughly linearly in $H$.

**Drawdown control.** [S] Nystrup, Boyd, Lindström and Madsen (2019) run MPC on HMM forecasts and raise risk aversion as realized drawdown grows. Out of sample over about two decades, this controlled drawdowns with little or no loss of efficiency. In their sample, adding leverage raised returns without raising the maximum drawdown.

**Illiquid commitments.** [S] Luxenberg et al. (2022) model each illiquid class as a random linear system:

$K_{t+1}=K_t+n_t-C_t,\quad I_{t+1}=R_tI_t+C_t-D_t,\quad C_t=\lambda^0_t n_t+\lambda^1_t K_t,\quad D_t=\delta_t R_t I_t$.

- **Calibration.** Mean intensities $\bar\lambda^0=0.128$, $\bar\lambda^1=0.26$ and $\bar\delta=0.33$ per year. The 15.8% mean return comes from BlackRock's 2021 buyout assumptions. Committing $1/yr sustains $3.685 of NAV.
- **Policy.** Certainty-equivalent MPC with $H=10$, discount $\gamma=0.97$, and a Gaussian second-order-cone chance constraint $P(\text{insolvency})\le 2\%$.
- **Results.**
  - Over 20 periods, performance is close to a fictional benchmark in which the illiquid assets are fully liquid.
  - Over 10 periods, the gap is larger because illiquid exposure peaks only after about 4 periods.
  - MPC reaches targets faster than a steady-state heuristic, and it cuts delayed RMS tracking error by 11% versus open loop.
- **Extensions sketched.** Secondary sales with a haircut, liabilities, time-varying forecasts, and vintage-indexed states.

**Trading partway toward an aim portfolio.** [S] Gârleanu and Pedersen (2013): with predictable returns and quadratic costs, the optimal policy trades partway toward an "aim portfolio", which blends the current and expected future Markowitz portfolios. [I] This supports pacing rules that close a fraction κ of the gap each quarter, with κ smaller when illiquidity costs are higher.

**Certainty-equivalent vs scenario MPC.** [P/I]
- Certainty-equivalent MPC is cheap (milliseconds to under a second per solve). But it ignores the value of recourse and the way tail events arrive together: liquidity crises, margin calls and distribution halts.
- Two fixes recover much of the gap: tightening constraints (chance or CVaR terms in the lookahead) and a small scenario lookahead of 20-100 scenarios.
- Powell's warning applies: stochastic lookaheads are expensive to tune by simulation.

### 3.5 Decision rules (LDR / AARC)

[S] Decision rules restrict recourse to affine functions of the uncertainty observed so far, $y_t(\xi)=y_t^0+Y_t\xi_{[t]}$, which preserves non-anticipativity.
- The affinely adjustable robust counterpart (AARC; Ben-Tal, Goryashko, Guslitzer and Nemirovski 2004) is a tractable LP or SDP in important cases. The fully adjustable version is NP-hard.
- Kuhn, Wiesemann and Georghiou (2011) bound the loss from linear decision rules by applying them to both the primal and the dual problem.
- The Georghiou, Kuhn and Wiesemann (2019) survey stresses that decision rules avoid the curse of dimensionality: they approximate the feasible region instead of discretizing the uncertainty.
- Finance precedents: linear control policies for multi-period portfolios (Calafiore 2008) and linear rebalancing rules, which are near-optimal in execution problems (Moallemi and Sağlam 2017).

[I] **Uses at ADIC.**
- Recourse inside the L1 tree after the branching node, which removes the clairvoyance problem.
- Auditable policy rules (PFAs), for example:
  - commitments $n_{g,t}=a_g+b_g^\top(\text{signals})$;
  - NAV-facility draws $b_t=\max(0,c+d\cdot\text{liquidity gap})$.
- Piecewise-linear "lifted" rules can capture the kinks that matter: the floor and loan covenants.

### 3.6 Policy search and simulation-optimization

[P] Policy search tunes the parameters θ of a policy $X^\pi(S\mid\theta)$ to maximize simulated performance, $\max_\theta\hat F(\theta)=\tfrac1N\sum_n F(\theta,\omega_n)$.

- **Common random numbers.** Evaluate every candidate θ on the same paths. This is essential for ranking policies reliably.
- **Optimizers.**
  - [S] CMA-ES: a covariance-adaptive randomized search for non-convex continuous problems (Hansen).
  - [S] Bayesian optimization is "best-suited" to continuous domains with fewer than 20 dimensions and to expensive, noisy evaluations (Frazier 2018).
  - [S] Optuna offers define-by-run search spaces with pruning.
  - [P] Cross-entropy methods and SPSA / Robbins-Monro stochastic approximation are alternatives.
- **Differentiable simulation.** [S] Chain parametric or neural policies through the simulated dynamics and train them directly on the objective (Han and E 2016). Deep hedging adds convex risk measures and trading frictions (Bühler et al. 2018). [I] In JAX, gradients flow through vectorized paths. Indicator-type events (floor breach, covenant breach) must be smoothed during training, so final evaluation must use the unsmoothed simulator.
- **Overfitting.** [P/I] In-sample optimism grows with policy flexibility and with search effort. Remedies:
  - hold out both seeds and *scenario generators*;
  - report the gap between in-sample and out-of-sample performance;
  - use replication-based confidence intervals;
  - use combinatorially symmetric cross-validation in the spirit of the "probability of backtest overfitting" (Bailey et al. 2017).

### 3.7 Reinforcement learning

[S] The finance RL literature is broad. The Hambly, Xu and Yang (2023) survey covers execution, portfolio optimization, hedging and market making. But Dulac-Arnold, Mankowitz and Hester list nine challenges for real-world RL, and every one applies to ADIC:
1. offline training;
2. learning from limited samples;
3. high-dimensional continuous states and actions;
4. safety constraints;
5. partial observability and non-stationarity;
6. multi-objective, underspecified rewards;
7. explainability;
8. real-time inference;
9. system delays.

[I] ADIC makes about 40-80 real quarterly decisions per decade, faces regime breaks, must respect hard fiduciary constraints, and must explain its decisions to an IC. Model-free RL on real data is inappropriate. RL inside a simulator is just policy search with an opaque policy class, and it inherits all of the simulator's model risk. Deep or differentiable policies have one use here: an R&D challenger that reveals policy structure. Distill that structure into interpretable PFA/CFA rules, then re-verify them in L3 against the bounds.

### 3.8 Discrete actions and fixed costs

SELL, REFINANCE and LEVER each carry fixed costs (legal, process, facility set-up), minimum sizes and lumpy execution.

**Formulation.** [P/I]
- Binaries $y_i^a\in\{0,1\}$ for each asset $i$ and action $a$, with $\sum_a y_i^a\le 1$.
- Semi-continuous sizes, $m_i^a y_i^a\le u_i^a\le M_i^a y_i^a$, with bounds tightened using NAV instead of a generic big-M.
- A fixed cost $F_i^a y_i^a$ in the cash balance. ($K$ is reserved for unfunded commitments.)
- Secondary price impact as a convex piecewise-linear discount on the volume sold per strategy per quarter. Sales of ADIC's size move prices.

**Solution ladder, from simplest to most specialized:**
1. Extensive-form MILP. This works because integers sit only in the first stage, and hundreds of binaries are routine for HiGHS or Gurobi.
2. Benders decomposition with an integer master problem.
3. LP relaxation, then rank, relax-and-fix rounding, and re-solve.
4. ℓ1 or reweighted-ℓ1 penalties to make actions sparse.
5. Price decomposition across assets (section 3.3).
6. PH heuristics in mpi-sppy, only if integers appear in recourse.

[I] Keep recourse continuous: its job is valuation, not execution.

### 3.9 Comparison

| Method (Powell class) | Discrete actions | Illiquid lags | Regimes | Practical scale | Duals | Time-consistent | IC interpretability | ADIC role |
|---|---|---|---|---|---|---|---|---|
| Exact DP (VFA) | yes | yes | yes | ≤3-4 state dimensions | value gradients | yes | medium | toy validation |
| Simulation-regression ADP / LSM (VFA) | stopping problems | yes | yes | ~10-20 dimensions | approximate | yes | medium | asset continuation values |
| Multistage SP tree (DLA) | first stage | yes | via tree | 2-4 stages, 10^3-10^5 nodes | yes, per node | if nested | high (playbook) | **L1 HDP** |
| SDDP / MSDDP (VFA + DLA) | limited (SDDiP) | yes (linear) | yes (Markov) | 40+ stages, tens of states | cuts are values | with nested risk | medium | **L2 values** |
| PH / Benders (algorithms) | heuristic / exact | yes | yes | 10^2 assets × 10^3-10^4 scenarios | yes | n/a | n/a | L1 solver |
| CE-MPC (DLA) | with MILP | yes | via forecasts | ms to s per solve | yes | by re-solving | high | L3 benchmark |
| Scenario MPC (DLA) | with MILP | yes | yes | s to min per solve | yes | by re-solving | high | L3 final check |
| LDR / AARC (PFA) | no | yes | via signals | large | yes | yes | high | recourse and rules |
| Parametric policy search (PFA/CFA) | yes | yes | yes | 10-30 parameters, 10^4-10^5 paths | no | yes | very high | **L3 production rules** |
| Deep RL (PFA/VFA) | yes | yes | yes | needs a lot of data | no | n/a | low | R&D challenger |
| Information-relaxation bounds | n/a | n/a | n/a | per path | n/a | n/a | medium | gap certificate |

---

## 4. Empirical evidence and current market data (dated)

### 4.1 Evidence on methods

- **Stochastic programming vs fixed-mix.** [S]
  - In simulated ALM tests, multistage SP dominated fixed-mix because it adapts to information in the tree (Fleten, Hoyland and Wallace 2002).
  - Kouwenberg (2001) used rolling-horizon simulations for a Dutch pension fund. Scenario-generation quality was decisive.
- **Deployments.** [S]
  - Russell-Yasuda Kasai: +42 bp, about US$79m, over two years.
  - InnoALM: used for Siemens Austria and Siemens worldwide, and to evaluate Austrian pension regulation.
  - Kusy-Ziemba: the stochastic LP outperformed the deterministic LP.
- **MPC and approximate DP.** [S]
  - Drawdown control at little or no efficiency cost (Nystrup et al. 2019).
  - Illiquid allocation close to the liquid benchmark over long horizons (Luxenberg et al. 2022).
  - ADP/MPC policies "typically close" to SDP bounds (Boyd et al. 2014).
  - Linear rebalancing rules near-optimal (Moallemi and Sağlam 2017).
- **Endowment payout behaviour.** [S] Brown, Dimmock, Kang and Weisbenner (2014) found that endowments cut payouts below their stated policy after negative shocks but do not raise them after positive shocks, which the authors link to "endowment hoarding". [I] An optimizer that assumes a fixed spending rule will misstate what actually happens. The distribution policy has to be modelled explicitly and chosen by the IC.
- **Cost of illiquidity.** [S] About 2% of wealth to hedge illiquidity crises that occur once a decade (Ang et al. 2014).

### 4.2 Computational evidence and sizing for ADIC

**Published benchmarks** [S]
- Boyd et al. (2017):
  - SPO with 1,500 assets and 50 factors solves in under 0.5 s on one core at 1 GFLOP/s.
  - About 80,000 problems (a 5-year backtest × 64 settings) ran in under 10 minutes on 32 cores.
- SDDP.jl is about 30% slower than C++.
- Valladão et al. solved a 100-asset, 5-factor Markov-chain SDDP problem.
- mpi-sppy closed optimality gaps within minutes on the largest known stochastic unit-commitment MIPs.
- Gondzio and Grothey solved a QP with more than 10^9 variables.

**Sizing for ADIC** [I]. Assumptions: 300 private positions aggregated into 15 groups for recourse, 20 liquid sleeves, quarterly steps.

| Component | Size | Expected solve |
|---|---|---|
| L1 HDP, extensive form. First stage at asset level: about 1,500 continuous variables and about 900 binaries. Recourse at group level: about 150 variables per node. Tree of 1 × 40 × 25 = 1,000 leaves over 12 quarters. | About 1.8M variables and 1.5-2M rows | LP: minutes with a commercial barrier solver; tens of minutes with HiGHS. MILP: minutes to an hour with tight bounds. Parallel Benders gives similar wall-clock time with less memory. |
| L1 what-if re-solve (warm start, 200 reduced scenarios) | About 0.4M variables | Seconds to about a minute, fast enough for live IC what-ifs |
| L2 Markov SDDP: 40 stages, 4 regimes, 20-30 states, 20-50 noise draws per stage | Small LPs of 10^2-10^3 variables | 10^3-10^4 iterations, minutes to hours |
| L3 certainty-equivalent MPC policy at group level, $H=8$ quarters | 1-2k variables per solve, 10-50 ms each | 10k paths × 40 quarters = 400k solves, about 1-6 CPU-hours, or minutes on 64 cores |
| L3 parametric policy in JAX/numba | Vectorized | 50k paths × 40 quarters × 300 assets in seconds. 200 CMA-ES iterations on 50k paths take minutes. |

### 4.3 Current market data for calibration

- **Funding base rate.** [S] SOFR was 3.89% on 2026-10-15 (FRED, updated 2026-10-16).
- **PE liquidity.** [S] Bain Global Private Equity Report 2026, published 2026-02-22:
  - Distributions were about 14% of NAV in the 12 months Q4 2024-Q3 2025, flat on the prior year and the lowest since 2008-09.
  - Distributions have been below 15% of NAV for four straight years (2022-2025).
  - DPI for 2017-2021 vintages trails the historical benchmark.
  - About 32,000 unsold companies are worth about $3.8tn.
  - The average holding period at exit is about 7 years, versus 5-6 years in 2010-21.
  - Buyout exit value rose 47% to $717bn in 2025.
  - Secondary transaction value rose 41% year on year, and GP-led continuation-vehicle value rose 62%.
  - 53% of LPs say undrawn commitments are limiting new commitments.
- **LBO financing.** [S] Bain 2026, Figure 1 notes:
  - Borrowing costs are 8-9% at 30-40% leverage, versus 6-7% at about 50% in 2015.
  - About 10-12% annual EBITDA growth is now needed for a 2.5x MOIC over five years ("12 is the new 5").
- **Illustrative ADIC liquidity arithmetic.** [I] These are illustrations, not ADIC data.
  - Assumptions:
    - NAV of $177bn, with 60% private, or $106bn.
    - Unfunded commitments of about 21% of NAV, or about $37bn, scaled from the v8 case ($18bn on $85bn).
    - Calls at 26% of unfunded per year, per Luxenberg's calibration.
  - At a 14% distribution rate, private distributions are about $14.8bn/yr and calls about $9.6bn/yr, so net private cash is about +$5bn/yr.
  - The required distribution is $8.9-17.7bn/yr. That leaves a gap of about $4-13bn/yr, which falls on a liquid book of roughly $71bn: about 5-18% of it each year, before income.
  - At a 10% distribution rate, the gap widens to about $8-17bn.
  - A 10% nominal return with a 10% payout means zero nominal NAV growth. So the target is roughly the return needed to fund the maximum payout without eroding NAV in nominal terms.

---

## 5. Practitioner and peer practice: case studies

- **Insurance (Russell-Yasuda).** [S] Risk defined in operational terms, regulatory constraints priced with penalty costs, and a 5-year horizon followed by a steady-state end-effects period. [I] Transferable lessons:
  - soft constraints with priority-weighted penalties;
  - a steady-state terminal period, which becomes our L2 cuts or a cyclic policy graph.
- **Pensions (InnoALM; Dutch pension SP).** [S] Correlations that depend on the market state (regimes); interactive use by decision makers; rolling-horizon tests against fixed-mix.
- **Consulting (Towers Perrin).** [S] Separate scenario-generator, optimizer and reporting modules: an industrial ALM pipeline.
- **Banks.** [S] Kusy and Ziemba's stochastic LP. Basel III's Liquidity Coverage Ratio requires an adequate stock of unencumbered high-quality liquid assets for a 30-day stress, with a 100% minimum from 2019 (BIS 2013). [I] Transferable lessons:
  - Frame ADIC's survival gate as a *fund LCR*, computed per scenario and per regime:
    - numerator: haircut liquid assets, net of initial margin;
    - denominator: stressed outflows over 30 days and over 12 months, covering margin, calls, distributions and debt service;
    - gate: the ratio must stay at or above 1.
  - Bank funds-transfer pricing charges each business line for the liquidity it consumes. The equivalent here is a hurdle for each strategy group derived from $\lambda$.
- **Energy.** [P] Hydro-thermal scheduling has used SDDP operationally for decades, for example in Brazil and New Zealand (practitioner consensus, *not re-verified in-session*). [S] Risk-averse CVaR variants exist and have been tested on the New Zealand system (Philpott and de Matos 2012). [I] Transferable lessons:
  - liquidity-value curves, the counterpart of water values;
  - cyclic, infinite-horizon policies;
  - Markov regimes for distributions, the counterpart of inflow regimes.
- **Illiquid-asset modelling.**
  - [S] Luxenberg et al. use MPC calibrated with an asset manager's buyout assumptions.
  - [S] Cao and van Beek (2025, FAJ) extend Takahashi-Alexander with systematic economic factors and fund-specific randomness, for stress tests and commitment design.
  - [S] Takahashi-Alexander is deterministic and remains the dominant LP pacing tool:
    - contributions $=RC\times(\text{commitment}-\text{paid-in})$;
    - distributions $=RD\times NAV_{t-1}(1+G)$, with $RD=\max[Y,(t/L)^B]$.
    - Sources: Karatas, Klinkert and Hirsa 2021; Luxenberg et al. 2022.
- **Endowment governance.** [S] Tobin (1974) on permanent endowment income and intergenerational equity. Merton (1993) criticizes managing the endowment as if it were the institution's only asset. [I] For ADIC, the owner's wider fiscal position matters. If the owner's cash needs rise when markets fall, distributions behave like a liability that is negatively correlated with returns, and the scenario generator should reflect that.

---

## 6. Design implications for the ADIC framework

### 6.1 Architecture and interactions [I]

```
 +--------------- Belief and scenario engines (other streams) ----------------+
 | regime HMM/HSMM | U/A/F return fusion | PE cash-flow model | market ESG     |
 +--------+-------------------------+------------------------------+----------+
          | reduced 3-stage tree     | aggregated Markov model      | 10k-50k paths
          v                          v                              v
 L1 HDP (DLA)                 L2 Markov SDDP (VFA)           L3 policy simulator
 asset-level stochastic MILP  cuts V_t(x, j): the          PFA/CFA tuning (CRN + CMA-ES/BO)
 Tier-1 CVaR, recourse        "liquidity water value"       CE-MPC, HDP-in-the-loop
 -> actions, duals, VSS/EVPI  <------ terminal value        baselines, ablations, bounds
          |------ distil actions and duals into rule parameters ------>|
          |<----- tuned buffers (CFA), stress failures, policy params --|
          v                                                             v
     IC pack: actions + playbook + shadow prices + outcome probabilities + optimality gap
```

**Quarterly cycle:**
1. **Update beliefs and scenarios.** Use the regime posterior, the fused returns and the cash-flow model. Generate 50k simulation paths. Reduce them to an L1 tree using regime-stratified k-medoids plus moment matching, then check the tree for arbitrage.
2. **Refresh L2.** Run SDDP warm-started from the previous cuts. Export cuts at the end of L1's horizon.
3. **Solve L1.** Outputs:
   - first-stage actions;
   - the recourse playbook;
   - duals;
   - VSS, EVPI and option values;
   - decision stability across M = 10 SAA replications.
4. **Evaluate in L3.** Run four sets of policies:
   - (a) the HDP-implied policy, re-solved inside 500-2,000 paths;
   - (b) the tuned parametric policy on 50k paths;
   - (c) the v8 comparators: static SAA and target-chasing;
   - (d) ablations: no overlay, no refinancing, no secondaries.

   Report fan charts, outcome probabilities and the information-relaxation gap.
5. **Run machine-checkable rubric checks.** These map onto the agentic layer's verification stage:
   - $\mathrm{WS}\ge\mathrm{RP}\ge\mathrm{EEV}$;
   - SAA lower bound ≤ upper bound;
   - every dual has the expected sign;
   - L1 actions fall inside the tuned policy's region, or the difference is explained;
   - out-of-sample degradation stays below a set threshold.
6. **Produce the IC pack** and support live what-ifs with warm-started re-solves.

**Distillation loop.**
- L1's actions and duals update the parametric rules, for example the liquidity-price thresholds.
- L3's tuned buffers return to L1 as CFA constraints, for example a minimum liquidity buffer.
- L2's cuts remove short-horizon myopia from L1.

### 6.2 State variables

[I] Per private position $i$ (in group $g$):
- NAV $I_{i,t}$;
- unfunded commitment $K_{i,t}$;
- age $a_{i,t}$;
- pledged flag;
- fused return belief $(\mu_{i,t},\sigma_{i,t})$;
- the three return marks: underwritten $r^U_i$, actual-to-date $r^A_{i,t}$ and forecast $r^F_{i,t}$.

Portfolio level:
- liquid holdings $h_t\in\mathbb{R}^{20}$;
- cash $c_t$;
- NAV facility balance $b_t$ and fund debt $D_t$, with maturities;
- tail-hedge book $\{N_k,K_k,T_k\}$;
- opportunistic-sleeve exposure $e_t$;
- initial margin $IM_t$ and collateral;
- year-to-date distributions $d^{YTD}_t$;
- running peak of distribution-adjusted NAV, needed for drawdown;
- regime $j_t$ and posterior $\pi_t$;
- secondary discount $\delta^{sec}_{g,t}$, NAV-loan spread $s_t$ and availability flag;
- SOFR $r^f_t$.

L2 uses group aggregates $(I_g,K_g)$ for about 6 groups, plus liquid, cash, debt, hedge notional and regime: about 20 states.

### 6.3 Decision variables (stage 1 at asset level, recourse at group level)

[I]
- **Liquid trades:** $z_t$.
- **New commitments:** $n_{g,t}\ge 0$, with minimum tickets.
- **SELL:** fraction $\phi_{i,t}\in[0,1]$, plus binary.
- **LEVER:** add-on or co-investment $\ell_{i,t}\ge 0$, plus binary.
- **REFINANCE:** NAV facility draw $\Delta b^+_t$ and repayment $\Delta b^-_t$. Asset-level recapitalization proceeds $q_{i,t}$ where the GP permits.
- **Fund leverage:** $\Delta D_t$.
- **Tail hedge:** notional $N_{k,t}$ by strike and expiry bucket.
- **Opportunistic sleeve:** risk budget $e_t$.
- **Distribution:** $d_t$.

### 6.4 Transitions (beginning-of-quarter actions; flows realize during the quarter)

Private position $i$ in group $g$, regime $j$, gross return $R_{i,t+1}$:

$I^+_{i,t}=(1-\phi_{i,t})I_{i,t}+\ell_{i,t},\qquad K^+_{i,t}=(1-\phi_{i,t})K_{i,t}$ (a buyer takes over the unfunded commitment)

$C_{i,t}=\lambda^1_{g,j}K^+_{i,t}+\lambda^0_{g,j}n_{i,t},\qquad D_{i,t}=\delta_{g,j,a}R_{i,t+1}I^+_{i,t}$

$I_{i,t+1}=R_{i,t+1}I^+_{i,t}+C_{i,t}-D_{i,t},\qquad K_{i,t+1}=K^+_{i,t}+n_{i,t}-C_{i,t}$

Cash (quarterly rates):

$c_{t+1}=(1+r^f_t)\big[c_t-\mathbf{1}^\top z_t-\textstyle\sum_i\ell_{i,t}+\sum_i(1-\delta^{sec}_{g,t}(v_{g,t}))\phi_{i,t}I_{i,t}-\sum F^a y^a+\Delta b^+_t-\Delta b^-_t+\Delta D_t-d_t-\pi^{tail}_t\big]$
$\qquad+\textstyle\sum_i(D_{i,t}-C_{i,t})-(r^f_t+s_t)b_t-(r^f_t+s^D)D_t+\sum_kN_{k,t}P_{k,t+1}-VM_{t+1}+\text{liquid income}$

Liquid sleeves: $h_{t+1}=(\mathbf{1}+r^L_{t+1})\circ(h_t+z_t)$.

Debt: $b_{t+1}=b_t+\Delta b^+_t-\Delta b^-_t$.

The regime follows a Markov chain $P(j_{t+1}\mid j_t)$ estimated by the state engine. The regime drives $\lambda^0,\lambda^1,\delta,\delta^{sec},s$, the haircuts $\eta$, the margin rates and the return distributions.

Net asset value: $NAV_t=c_t+\mathbf{1}^\top h_t+\sum_iI_{i,t}+MTM^{ovl}_t-b_t-D_t$.

Every term is linear in the decisions for a given scenario, except the price-impact discount $\delta^{sec}(v)$, which is convex piecewise-linear.

### 6.5 Constraints (enforced in every scenario $s$ and quarter $t$ unless noted)

| # | Constraint | Formulation |
|---|---|---|
| C1 | Distribution band | $0.05\,NAV_{y}\le\sum_{t\in y}d_t\le 0.10\,NAV_{y}$ (beginning-of-year NAV), or the owner's scenario demand $d^{own}_{y,s}$ as a lower bound |
| C2 | IG + cash floor (v8) | $c_t+h^{IG}_t\ge 0.08\,NAV_t$ |
| C3 | Fund LCR (30-day and 12-month) | $\sum_k(1-\eta_{k,j})h_{k,t}+c_t-IM_t\ge VM^{30d}_{99}+\text{stressed calls}+\text{distributions due}+\text{debt service}$ |
| C4 | Leverage and covenants | $b_t+D_t\le\ell^{max}NAV_t$; $b_t\le LTV^{max}\sum_{i\in\text{pledged}}I_{i,t}$ (forces repayment as recourse) |
| C5 | Overlay | $IM_t=\sum_k m_k\lvert N_k\rvert$ (linearized); $IM_t+VM^{stress}_t\le$ unencumbered high-quality liquid assets; annual premium $\le B^{tail}NAV$; $\mathrm{ES}_{97.5}(\text{opportunistic P\&L})\le B^{opp}NAV$ |
| C6 | Allocation and overhang | group bands, concentration limits, $\sum K_{i,t}\le\kappa\cdot(\text{liquid assets})$ |
| C7 | Tier-1 robust floor (rolling 5 years) | for every model $m\in\mathcal{M}$: $\mathrm{CVaR}^m_{0.95}(-\mathrm{NPV}_{7\%})\le 0$ |
| C8 | 12-month liquidity breach | $\mathrm{CVaR}^m_{0.99}(\text{LCR shortfall})\le 0$, so breach probability ≤ ~1% |
| C9 | Structure | non-anticipativity; integrality in stage 1 only |

Here $\mathrm{NPV}_r=-NAV_0+\sum_{t=1}^{20}d_t(1+r)^{-t/4}+NAV_{20}(1+r)^{-5}$. For the owner's cash flows (one outflow, then non-negative inflows), $\mathrm{IRR}\ge r\iff\mathrm{NPV}_r\ge 0$, and $\mathrm{NPV}_r$ is linear per scenario [I]. Keep reporting time-weighted returns as well, since they are the standard performance measure.

### 6.6 Objective (Tier 2, subject to C1-C9)

$\max\ \mathbb{E}_P\Big[\textstyle\sum_{t\le T_1}d_t(1+r^*)^{-t/4}+(1+r^*)^{-T_1/4}\,\theta_{T_1}\Big]-\kappa^{SF}\,\mathbb{E}_P[(\Gamma_{T_1}-\tilde W_{T_1})^+]-\text{transaction and fixed costs}-\kappa^{u}\sum_i\sigma_i\ell_i$

The terms are defined as follows:
- $r^*=10\%$.
- $\theta_{T_1}\le\alpha_k+\beta_k^\top x_{T_1}$ for every L2 cut $k$ in regime $j_{T_1}$.
- $\tilde W$ is distribution-adjusted wealth and $\Gamma$ is the 10% target path.
- The last term is an uncertainty haircut that stops the optimizer from exploiting optimistic forecasts in LEVER decisions.

The objective is an LP: every term is linear or piecewise-linear. $P(\mathrm{IRR}\ge 10\%)$ is *reported*, not maximized. A log-utility variant (exponential cone, CLARABEL or MOSEK) can serve as a growth-optimal cross-check.

### 6.7 From shadow prices to SELL / HOLD / REFINANCE / LEVER economics [I]

Let $\mu_t^s=\lambda_t^s$ be the probability-normalized cash duals. Position $i$ consists of its current NAV $I_i$ and its unfunded commitment $K_i$. Its **liquidity-adjusted continuation value** is

$CV_i=\mathbb{E}\big[\sum_{t\ge 1}\mu^s_t\,(D^s_{i,t}-C^s_{i,t})+\mu^s_{T_1}\,\theta'_g\,I^s_{i,T_1}\big]$,

where $\theta'_g=\partial\theta/\partial I_g$ is the slope of the L2 cut, i.e. the terminal value of $1 of group-$g$ NAV. Future capital calls enter with a negative sign, so a position with a large unfunded commitment has a low $CV$ exactly when future $\mu$ is high (stress). The marginal value of each action:
- **SELL** (whole position; the buyer takes over the unfunded commitment): $\mu_0(1-\delta^{sec}_i)I_i-CV_i-F_i$. Relief from future calls is already inside $CV_i$.
- **REFINANCE** (draw $1 and repay at $\tau$): $\mu_0-\mathbb{E}[\sum_{t\le\tau}\mu_t^s(r^f+s)/4+\mu^s_\tau]$. This is positive exactly when the implied liquidity rate $\rho$ exceeds $r^f+s$ over the loan's life.
- **LEVER** (add $\Delta$ of exposure): $\Delta\,[-\mu_0+cv_i-\kappa^u\sigma_i]$, where $cv_i$ is the per-dollar continuation value of the new exposure under fused (shrunk) return beliefs.
- **HOLD:** zero by construction.

**Plain-language rule:** *sell when cash today, after the secondary discount and fixed costs, is worth more at shadow prices than the position's future distributions minus its future calls.*

Duals are marginal values, so discrete actions also need *forced-action re-solves*: compute $\Delta J$ with action $a$ forced on asset $i$, warm-started over about 300 assets in parallel. Report ranges across SAA replications. Sorting candidate cash sources by all-in cost per marginal dollar gives the **liquidity merit order**: buffer, liquid rebalancing, overlay de-risking to release collateral, NAV facility, LP secondary sale, GP-led solution. The marginal source sets the clearing price $\rho$. The tail hedge's value at shadow prices, $\mathbb{E}[\mu^s P^s]-\text{premium}\cdot\mathbb{E}[\mu]$, exceeds its expected payoff because it pays out exactly when $\mu$ spikes. The opportunistic sleeve is penalized if its losses cluster in high-$\mu$ states.

### 6.8 IC-facing outputs from this stream [I]

1. **Recommended actions** with a stability score: the share of replications and generators that select each action.
2. **Liquidity-value curve** $\mu_t$ by regime and the implied liquidity rate $\rho_t$, compared with SOFR plus the facility spread and with the cost implied by secondary discounts. Together these give the merit order.
3. **Shadow-cost table**, in bp of expected IRR and pp of floor-breach probability, for:
   - the IG floor;
   - the leverage cap;
   - the distribution floor ("+1pp of payout costs X bp and Y pp");
   - the Tier-1 CVaR constraint;
   - the commitment overhang.
4. **VSS, EVPI and capability values:** the overlay, the NAV facility, secondary-market access and the opportunistic sleeve.
5. **L3 policy comparison** across generators, shown as ranges:
   - 5-year and 10-year IRR and TWR;
   - $P(\mathrm{IRR}\ge 10\%)$ and $P(\mathrm{IRR}<7\%)$;
   - $P(\text{12-month LCR breach})$;
   - distribution reliability;
   - the drawdown distribution;
   - peak leverage;
   - P99 margin.
6. **Optimality gap:** the information-relaxation bound versus the achieved value.
7. **Contingent playbook by regime,** derived from the recourse decisions.

### 6.9 Default parameters

| Parameter | Default | Status |
|---|---|---|
| Stage length | quarter (monthly sub-steps for margin) | [I] |
| L1 horizon and tree | 12 quarters; stages Q1 / Q2-Q4 / Y2-Y3; 1×40×25 = 1,000 leaves, regime-stratified | [I] |
| SAA replications | M = 10 (decision-stability and bound CIs) | [I] |
| L2 | 40 quarters plus a cyclic/steady-state node; 3-4 regimes (normal, low-DPI, crisis, recovery) | [I] |
| L3 paths | 10k for tuning, 50k for reporting (v8 used 50k); common random numbers | [I]/[S deck] |
| Tier-1 floor | IRR ≥ 7% over a rolling 5 years, ε = 5%, via CVaR95 under the worst model in $\mathcal{M}$ | [S deck] |
| Liquidity breach | 12-month breach ε ≈ 1% via CVaR99 (the v8 dashboard showed 0.6% at 12 months) | [I]/[S deck] |
| IG + cash floor | ≥ 8% of NAV | [S deck] |
| Distribution band | 5-10% of NAV per year | [S brief] |
| Call intensity $\lambda^1$ / $\lambda^0$ | 0.26 / 0.128 per year (regime range 0.20-0.35) | [S Luxenberg] / range [I] |
| Distribution intensity δ | normal 0.20-0.25; low-DPI ≈ 0.14; crisis 0.05-0.10 per year | ≈0.14 [S Bain]; others [I], calibrate |
| Secondary discount | placeholder: buyout normal 5-15%, stress 20-35%, plus convex size impact | [I], calibrate with the secondaries stream |
| Funding base rate | SOFR 3.89% (2026-10-15); facility spread from ADIC terms | [S FRED] |
| Leverage cap, LTV, tail and opportunistic budgets | ADIC policy inputs (placeholder: start with ℓ^max = 10% of NAV for sensitivity runs) | [I] |
| MPC | $H=8$ quarters; certainty-equivalent with CVaR-tightened liquidity; smoothing penalty on commitment changes | [I] (Luxenberg used $H=10$ yearly, γ = 0.97) |
| Pacing gap-closure κ | 0.25-0.5 per quarter, tuned | [I] |
| Shortfall penalty $\kappa^{SF}$, uncertainty haircut $\kappa^u$ | tuned so that L1 and L3 metrics agree; $\kappa^u\approx 0.5$-1 | [I] |

### 6.10 Calibration targets and data needs

**Targets** [I]
- Reproduce 2022-2025 distribution yields (about 14% of NAV) and holding periods (about 7 years).
- Reproduce crisis-period secondary discounts and NAV-loan spreads, using data from the secondaries stream.
- Check v8 deck outputs as code regression tests only. For example, the stylized scenario's static-SAA mean of 7.3% and $P(\ge 10\%)$ of 31.7%.

**Data needs**
- Asset level: quarterly NAVs, calls, distributions, unfunded commitments, vintage, strategy, the U/A/F return marks with forecast vintages, leverage, and secondary indications.
- Market: SOFR curve, CSA terms, option surfaces, margin model, and secondary price history.
- Owner: rules for distribution timing and flexibility, and how the owner's cash needs co-move with markets.

---

## 7. Implementation notes

- **Modelling and solvers.**
  - [S] cvxpy works with CLARABEL (LP/QP/SOCP/SDP/EXP/POW), SCS (general fallback), OSQP (QP), HiGHS, MOSEK and Gurobi. By default it calls the most specialized solver for the problem type.
  - [S] Clarabel is an interior-point conic solver with quadratic objectives. Its authors report it is faster and more robust than competing solvers.
  - [S] HiGHS (MIT licence) provides dual simplex and interior-point LP, active-set QP, and branch-and-cut MIP.
  - [I] Use Pyomo plus mpi-sppy for the MILP and decomposition. Read duals from `constraint.dual_value` in cvxpy or from a dual Suffix in Pyomo.
  - [I] Prefer interior-point solutions without crossover for "central" duals, which are more stable under degeneracy. Cross-check duals with finite-difference re-solves.
- **SDDP.** [S] SDDP.jl offers Markovian and infinite-horizon policy graphs, objective and belief states, integrality handling and nine risk measures. [I] Call it from Python via juliacall. msppy is the pure-Python alternative, but its extensive-form path requires Gurobi.
- **Simulation.** [I]
  - Use JAX (jit/vmap) or numba in float64.
  - Generate keyed random streams for common random numbers.
  - De-smooth private NAV marks before computing risk, but keep reported NAV for covenants.
  - Track running maxima for drawdown.
- **Policy search.** [S/I] pycma, nevergrad, Optuna (define-by-run, pruning), BoTorch for problems with fewer than 20 dimensions. Run every candidate on a fixed CRN block and hold out a separate block.
- **Scenario reduction.** [I] Regime-stratified k-medoids plus moment matching (Hoyland-Wallace), followed by an arbitrage check. Measure in-sample versus out-of-sample stability by solving on tree A and evaluating on simulation set B.
- **Complexity.** [I]
  - L1 extensive form is $O(S\cdot H\cdot n)$.
  - Benders typically needs 10-100 iterations.
  - SDDP needs 10^3-10^4 iterations.
  - Certainty-equivalent MPC is $O(H)$ per step.
  - Memory, not CPU, is the usual extensive-form bottleneck above about 10^7 nonzeros. Decompose beyond that.
- **Numerical pitfalls.** [P/I]
  - Scale by NAV, since mixing $bn and bp units ruins conditioning.
  - Use tight bounds instead of a generic big-M.
  - CVaR over many scenarios needs one auxiliary variable per scenario; a cutting-plane CVaR can help.
  - Degenerate LPs give non-unique duals.
  - Be consistent about quarterly compounding and sign conventions.
  - Make runs reproducible: record seeds and solver versions.
- **Tests.** [I]
  - Invariants: $\mathrm{WS}\ge\mathrm{RP}\ge\mathrm{EEV}$; VSS and EVPI ≥ 0.
  - Exact DP on a 2-3-state toy model compared against SDDP and MPC.
  - Monotonicity checks: tightening the floor must never raise the expected return.
  - Golden regression runs.

---

## 8. Risks, pitfalls and limitations

1. **Error maximization.** [P] The optimizer amplifies forecast errors, and strategy-group forecasts are likely optimistic. Mitigations: shrink fused forecasts, add uncertainty haircuts (Boyd et al.'s robust return term), use turnover penalties and action bands, and require an uncertainty-adjusted hurdle for LEVER.
2. **Model risk outweighs optimization error.** [I] Every probability is conditional on a model. Report ranges across generators, and never a single "P(10%)" without its model spread.
3. **Clairvoyant fans, end-of-horizon effects and time inconsistency.** [P] Use the tree-plus-decision-rule recourse, L2 terminal cuts (otherwise the optimizer stops committing near the horizon), and a rolling Tier-1 constraint with a recovery mode.
4. **Unstable duals.** [I] Duals are local and depend on the scenario sample. Show confidence intervals across replications and back them with forced-action re-solves. Never present a single dual as an exact price.
5. **Coupled stress.** [I] Margin calls, capital calls, hedge-fund gates, covenant tests, closed secondary windows and the owner's demand must all be driven by the same regime. A generator that treats them as independent understates liquidity risk badly.
6. **Market capacity.** [I] A $177bn fund's secondary sales and facility draws affect their own prices. Model convex price impact and annual capacity caps.
7. **Leverage path dependence.** [I] Forced deleveraging after a NAV drop is pro-cyclical. Covenant constraints must hold in every scenario, not on average.
8. **Terminal valuation of illiquid NAV.** [I] Lagged marks inflate terminal wealth in downturns. Apply regime-dependent haircuts to terminal NAV.
9. **Overfitting and false precision.** [P] Tuned policies can look excellent in-sample. Mitigations: held-out generators, a reported optimism gap and overfitting diagnostics.
10. **Governance.** [S deck/I] Keep the v8 boundary: LLM agents never produce numbers. Deterministic code owns optimization and simulation, and the IC owns decisions. Every IC override and its outcome is logged.

---

## 9. Open questions

1. Who sets the distribution rate within the 5-10% band, ADIC or the owner? What is the basis: beginning-of-year NAV or a trailing average? How flexible is the timing? Do the owner's needs co-move with markets?
2. What are ADIC's actual unfunded commitments, NAV-facility terms (LTV, spread, covenants, tenor), fund-level leverage limits and CSA terms?
3. Is the 10% target measured as a TWR or an IRR, over what horizon, and is it net of leverage cost? Is the 7% floor an IRR or a TWR?
4. What secondary volume can ADIC sell each year without a material extra discount, by strategy and regime?
5. Should Tier 2 maximize expected owner value with a shortfall penalty, as proposed here, or must it target an explicit $P(\ge 10\%)$ threshold the IC wants to see?
6. How should the misspecification set $\mathcal{M}$ be defined (which generators, what Wasserstein radius), and who approves it?
7. Is asset-level history (cash flows, forecast vintages) available to calibrate the fusion bias and the regime-dependent intensities?
8. Is GP consent needed for asset-level REFINANCE or LEVER, and how should that constraint and its delays be represented?

---

## 10. References

1. Ang, A., Papanikolaou, D., and Westerfield, M. (2014). Portfolio choice with illiquid assets. *Management Science* 60(11):2737-2761. https://ideas.repec.org/a/inm/ormnsc/v60y2014i11p2737-2761.html
2. Bain & Company (2026, 22 Feb). Global Private Equity Report 2026, "Outlook: gaining traction". https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/
3. Bain & Company (2026). "Welcome to a new era" (GPER 2026). https://www.bain.com/insights/welcome-to-a-new-era-global-private-equity-report-2026/
4. Bailey, D., Borwein, J., López de Prado, M., and Zhu, Q. (2017). The probability of backtest overfitting. *Journal of Computational Finance* 20(4):39-69 (first published 19 Sep 2016). https://doi.org/10.21314/jcf.2016.322 ; SSRN preprint: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
5. Basel Committee on Banking Supervision (2013). Basel III: The Liquidity Coverage Ratio and liquidity risk monitoring tools. https://www.bis.org/publ/bcbs238.htm
6. Ben-Tal, A., Goryashko, A., Guslitzer, E., and Nemirovski, A. (2004). Adjustable robust solutions of uncertain linear programs. *Mathematical Programming* 99(2):351-376. https://www.iaorifors.com/paper/46581
7. Birge, J.R. (1982). The value of the stochastic solution in stochastic linear programs with fixed recourse. *Mathematical Programming* 24:314-325. https://doi.org/10.1007/bf01585113
8. Boyd, S., Busseti, E., Diamond, S., Kahn, R.N., Koh, K., Nystrup, P., and Speth, J. (2017). Multi-period trading via convex optimization. *Foundations and Trends in Optimization* 3(1):1-76. https://arxiv.org/abs/1705.00109
9. Boyd, S., Mueller, M., O'Donoghue, B., and Wang, Y. (2014). Performance bounds and suboptimal policies for multi-period investment. *Foundations and Trends in Optimization* 1(1):1-69. https://web.stanford.edu/~boyd/papers/port_opt_bound.html
10. Brandt, M., Goyal, A., Santa-Clara, P., and Stroud, J. (2005). A simulation approach to dynamic portfolio choice with an application to learning about return predictability. *Review of Financial Studies* 18(3):831-873. https://doi.org/10.1093/rfs/hhi019 ; working paper: https://www.nber.org/papers/w10934
11. Brown, D.B., Smith, J.E., and Sun, P. (2010). Information relaxations and duality in stochastic dynamic programs. *Operations Research* 58(4):785-801. https://dukespace.lib.duke.edu/items/7684784b-5d4c-471a-9336-5044dd2a4bef
12. Brown, J., Dimmock, S., Kang, J.-K., and Weisbenner, S. (2014). How university endowments respond to financial market shocks: evidence and implications. *American Economic Review* 104(3):931-962. https://doi.org/10.1257/aer.104.3.931 (working-paper version: NBER w15861)
13. Bühler, H., Gonon, L., Teichmann, J., and Wood, B. (2018). Deep hedging. arXiv:1802.03042. https://arxiv.org/abs/1802.03042
14. Calafiore, G.C. (2008). Multi-period portfolio optimization with linear control policies. *Automatica* 44(10):2463-2473. https://doi.org/10.1016/j.automatica.2008.02.007 ; author copy: https://staff.polito.it/giuseppe.calafiore/Home_Page/Publications_files/Automatica_Multi-period%20portfolio%20optimization%20with%20linear%20control%20policies.pdf
15. Calafiore, G.C., and Campi, M.C. (2006). The scenario approach to robust control design. *IEEE Transactions on Automatic Control* 51:742-753. https://doi.org/10.1109/TAC.2006.875041
16. Campbell, J.Y., and Viceira, L.M. (2002). *Strategic Asset Allocation: Portfolio Choice for Long-Term Investors*. Oxford University Press. https://doi.org/10.1093/0198296940.001.0001
17. Campi, M.C., and Garatti, S. (2008). The exact feasibility of randomized solutions of uncertain convex programs. *SIAM Journal on Optimization* 19(3):1211-1230. https://optimization-online.org/2007/07/1727/
18. Cao, W., and van Beek, M. (2025). A latent factor cash flow model for alternative investment funds. *Financial Analysts Journal* 81(3). https://rpc.cfainstitute.org/research/financial-analysts-journal/2025/latent-factor-cash-flow-model
19. Cariño, D.R., Kent, T., Myers, D.H., Stacy, C., Sylvanus, M., Turner, A.L., Watanabe, K., and Ziemba, W.T. (1994). The Russell-Yasuda Kasai model: an asset/liability model for a Japanese insurance company using multistage stochastic programming. *Interfaces* 24(1):29-49. https://doi.org/10.1287/inte.24.1.29 ; https://ideas.repec.org/a/inm/orinte/v24y1994i1p29-49.html
20. Cariño, D.R., and Ziemba, W.T. (1998). Formulation of the Russell-Yasuda Kasai financial planning model. *Operations Research* 46(4):433-449. https://ideas.repec.org/a/inm/oropre/v46y1998i4p433-449.html
21. CVXPY solver documentation (accessed 2026-10-18). https://www.cvxpy.org/tutorial/solvers/index.html
22. Dantzig, G.B., and Infanger, G. (1993). Multi-stage stochastic linear programs for portfolio optimization. *Annals of Operations Research* 45:59-76. https://www.doi.org/10.1007/BF02282041
23. Dimmock, S.G., Wang, N., and Yang, J. (2024). The endowment model and modern portfolio theory. *Management Science* 70(3):1554-1579. https://www.nber.org/papers/w25559
24. Ding, L., Ahmed, S., and Shapiro, A. (2019). A Python package for multi-stage stochastic programming (msppy). https://optimization-online.org/wp-content/uploads/2019/05/7199.pdf ; https://msppy.readthedocs.io/en/latest/
25. Dowson, O. (2020). The policy graph decomposition of multistage stochastic programming problems. *Networks* 76(1):3-23. https://doi.org/10.1002/net.21932 ; preprint: https://optimization-online.org/?p=15496
26. Dowson, O., and Kapelevich, L. (2021). SDDP.jl: a Julia package for stochastic dual dynamic programming. *INFORMS Journal on Computing* 33(1):27-33. https://ideas.repec.org/a/inm/orijoc/v33y2021i1p27-33.html ; docs: https://sddp.dev/stable/
27. Dulac-Arnold, G., Mankowitz, D., and Hester, T. (2019). Challenges of real-world reinforcement learning. arXiv:1904.12901. https://arxiv.org/abs/1904.12901
28. Fleten, S.-E., Høyland, K., and Wallace, S.W. (2002). The performance of stochastic dynamic and fixed mix portfolio models. *European Journal of Operational Research* 140(1):37-49. https://ideas.repec.org/a/eee/ejores/v140y2002i1p37-49.html
29. FRED, Federal Reserve Bank of St. Louis. Secured Overnight Financing Rate (SOFR), observation 2026-10-15. https://fred.stlouisfed.org/series/SOFR
30. Frazier, P.I. (2018). A tutorial on Bayesian optimization. arXiv:1807.02811. https://arxiv.org/abs/1807.02811
31. Füllner, C., and Rebennack, S. (2025). Stochastic dual dynamic programming and its variants: a review. *SIAM Review* 67(3):415-539. https://epubs.siam.org/doi/10.1137/23M1575093
32. Gârleanu, N., and Pedersen, L.H. (2013). Dynamic trading with predictable returns and transaction costs. *Journal of Finance* 68(6):2309-2340. https://www.nber.org/papers/w15205
33. Georghiou, A., Kuhn, D., and Wiesemann, W. (2019). The decision rule approach to optimization under uncertainty: methodology and applications. *Computational Management Science* 16(4):545-576. https://spiral.imperial.ac.uk/entities/publication/7ff93cf4-1145-418f-96ed-d7cde88b08e8
34. Geyer, A., and Ziemba, W.T. (2008). The Innovest Austrian pension fund financial planning model InnoALM. *Operations Research* 56(4):797-810. https://ideas.repec.org/a/inm/oropre/v56y2008i4p797-810.html
35. Gondzio, J., and Grothey, A. (2006). Solving nonlinear financial planning problems (Technical Report MS 2006-002; WIT Transactions on Modelling and Simulation 43). Abstract reports a quadratic financial-planning problem with more than 10^9 decision variables solved on 1,280 processors. https://webhomes.maths.ed.ac.uk/~gondzio/reports/compfin06.html
36. Hambly, B., Xu, R., and Yang, H. (2023). Recent advances in reinforcement learning in finance. *Mathematical Finance* 33(3):437-503. https://ideas.repec.org/a/bla/mathfi/v33y2023i3p437-503.html
37. Han, J., and E, W. (2016). Deep learning approximation for stochastic control problems. arXiv:1611.07422. https://arxiv.org/abs/1611.07422
38. Hansen, N. (2016/2023). The CMA evolution strategy: a tutorial. arXiv:1604.00772. https://arxiv.org/abs/1604.00772
39. Haugh, M., Kogan, L., and Wang, J. (2006). Evaluating portfolio policies: a duality approach. *Operations Research* 54(3):405-418. https://ideas.repec.org/a/inm/oropre/v54y2006i3p405-418.html
40. HiGHS (accessed 2026-10-18). https://highs.dev/
41. Høyland, K., and Wallace, S.W. (2001). Generating scenario trees for multistage decision problems. *Management Science* 47(2):295-307. https://ideas.repec.org/a/inm/ormnsc/v47y2001i2p295-307.html
42. Karatas, T., Klinkert, F., and Hirsa, A. (2021). Supervised neural networks for illiquid alternative asset cash flow forecasting. arXiv:2108.02853. https://arxiv.org/abs/2108.02853
43. Knueven, B., Mildebrath, D., Muir, C., Siirola, J.D., Watson, J.-P., and Woodruff, D.L. (2023). A parallel hub-and-spoke system for large-scale scenario-based optimization under uncertainty. *Mathematical Programming Computation* 15(4):591-619. https://optimization-online.org/2020/11/8088/
44. Kouwenberg, R. (2001). Scenario generation and stochastic programming models for asset liability management. *European Journal of Operational Research* 134(2):279-292. https://repub.eur.nl/pub/66451
45. Kozmík, V., and Morton, D.P. (2015). Evaluating policies in risk-averse multi-stage stochastic programming. *Mathematical Programming*, pp. 275-300 (volume not verified in-session). https://doi.org/10.1007/s10107-014-0787-8
46. Kuhn, D., Wiesemann, W., and Georghiou, A. (2011). Primal and dual linear decision rules in stochastic and robust optimization. *Mathematical Programming* 130(1):177-209. https://optimization-online.org/?p=10666
47. Kusy, M.I., and Ziemba, W.T. (1986). A bank asset and liability management model. *Operations Research* 34(3):356-376. https://ideas.repec.org/a/inm/oropre/v34y1986i3p356-376.html
48. Longstaff, F.A., and Schwartz, E.S. (2001). Valuing American options by simulation: a simple least-squares approach. *Review of Financial Studies* 14(1):113-147. https://ideas.repec.org/a/oup/rfinst/v14y2001i1p113-47.html
49. Luxenberg, E., Boyd, S., Kochenderfer, M., van Beek, M., Cao, W., Diamond, S., Ulitsky, A., Menda, K., and Vairavamurthy, V. (2022). Strategic asset allocation with illiquid alternatives. arXiv:2207.07767. https://arxiv.org/abs/2207.07767 . Proceedings version (five authors): Luxenberg, E., Boyd, S., van Beek, M., Cao, W., and Kochenderfer, M. (2022). Strategic asset allocation with illiquid alternatives. *Proceedings of the Third ACM International Conference on AI in Finance (ICAIF '22)*, pp. 249-256. https://doi.org/10.1145/3533271.3561769
50. Merton, R.C. (1969). Lifetime portfolio selection under uncertainty: the continuous-time case. *Review of Economics and Statistics* 51(3):247-257. https://ideas.repec.org/a/tpr/restat/v51y1969i3p247-57.html
51. Merton, R.C. (1993). Optimal investment strategies for university endowment funds. In Clotfelter, C.T., and Rothschild, M. (eds.), *Studies of Supply and Demand in Higher Education*, ch. 7, pp. 211-242. University of Chicago Press. NBER chapter c6102; earlier version NBER Working Paper 3820 (1991). https://www.nber.org/books-and-chapters/studies-supply-and-demand-higher-education/optimal-investment-strategies-university-endowment-funds
52. Moallemi, C.C., and Sağlam, M. (2017). Dynamic portfolio choice with linear rebalancing rules. *Journal of Financial and Quantitative Analysis* 52(3):1247-1278. https://ideas.repec.org/a/cup/jfinqa/v52y2017i03p1247-1278_00.html
53. Mohajerin Esfahani, P., and Kuhn, D. (2018). Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. *Mathematical Programming* 171(1-2):115-166 (online 7 Jul 2017). https://doi.org/10.1007/s10107-017-1172-1 ; preprint arXiv:1505.05116, https://arxiv.org/abs/1505.05116
54. Mulvey, J.M., Gould, G., and Morgan, C. (2000). An asset and liability management system for Towers Perrin-Tillinghast. *Interfaces* 30(1):96-114. https://ideas.repec.org/a/inm/orinte/v30y2000i1p96-114.html (companion: "Generating scenarios for the Towers Perrin investment system", *Interfaces* 26(2):1-15, 1996, https://ideas.repec.org/a/inm/orinte/v26y1996i2p1-15.html)
55. Nemirovski, A., and Shapiro, A. (2006). Convex approximations of chance constrained programs. *SIAM Journal on Optimization* 17(4):969-996. https://optimization-online.org/2004/12/1033/
56. Nystrup, P., Boyd, S., Lindström, E., and Madsen, H. (2019). Multi-period portfolio selection with drawdown control. *Annals of Operations Research* 282:245-271. https://stanford.edu/~boyd/papers/multiperiod_portfolio_drawdown.html
57. Optuna: Akiba, T., Sano, S., Yanase, T., Ohta, T., and Koyama, M. (2019). Optuna: a next-generation hyperparameter optimization framework. KDD 2019; arXiv:1907.10902. https://arxiv.org/abs/1907.10902
58. Pereira, M.V.F., and Pinto, L.M.V.G. (1991). Multi-stage stochastic optimization applied to energy planning. *Mathematical Programming* 52:359-375. https://www.iaorifors.com/paper/6581
59. Pflug, G.Ch., and Pichler, A. (2012). A distance for multistage stochastic optimization models. *SIAM Journal on Optimization* 22(1):1-23. https://doi.org/10.1137/110825054
60. Philpott, A.B., and de Matos, V.L. (2012). Dynamic sampling algorithms for multi-stage stochastic programs with risk aversion. *European Journal of Operational Research* 218(2):470-483. https://ideas.repec.org/a/eee/ejores/v218y2012i2p470-483.html
61. Powell, W.B. (2019). A unified framework for stochastic optimization. *European Journal of Operational Research* 275(3):795-821. https://collaborate.princeton.edu/en/publications/a-unified-framework-for-stochastic-optimization/
62. Powell, W.B. (2021). From reinforcement learning to optimal control: a unified framework for sequential decisions. In *Handbook of Reinforcement Learning and Control* (Studies in Systems, Decision and Control), Springer, Cham, pp. 29-74. https://doi.org/10.1007/978-3-030-60990-0_3 ; preprint arXiv:1912.03513, https://arxiv.org/abs/1912.03513
63. Rockafellar, R.T., and Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk* 2(3):21-41. https://doi.org/10.21314/JOR.2000.038 ; author copy: https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf
64. Rockafellar, R.T., and Wets, R.J.-B. (1991). Scenarios and policy aggregation in optimization under uncertainty. *Mathematics of Operations Research* 16(1):119-147. https://pubsonline.informs.org/doi/fpi/10.1287/moor.16.1.119
65. Samuelson, P.A. (1969). Lifetime portfolio selection by dynamic stochastic programming. *Review of Economics and Statistics* 51(3):239-246. https://ideas.repec.org/a/tpr/restat/v51y1969i3p239-46.html
66. Shapiro, A. (2009). On a time consistency concept in risk averse multistage stochastic programming. *Operations Research Letters* 37(3):143-147. https://optimization-online.org/2008/12/2171/
67. Tobin, J. (1974). What is permanent endowment income? *American Economic Review* 64(2):427-432. https://ideas.repec.org/a/aea/aecrev/v64y1974i2p427-32.html
68. Valladão, D., Silva, T., and Poggi, M. (2019). Time-consistent risk-constrained dynamic portfolio optimization with transactional costs and time-dependent returns. *Annals of Operations Research* 282. https://ideas.repec.org/a/spr/annopr/v282y2019i1d10.1007_s10479-018-2991-z.html
69. Watson, J.-P., and Woodruff, D.L. (2011). Progressive hedging innovations for a class of stochastic mixed-integer resource allocation problems. *Computational Management Science* 8(4):355-370. https://link.springer.com/article/10.1007/s10287-010-0125-4
70. Zou, J., Ahmed, S., and Sun, X.A. (2019). Stochastic dual dynamic integer programming. *Mathematical Programming*, pp. 461-502 (volume not verified in-session). https://optimization-online.org/2016/05/5436/
71. Goulart, P.J., and Chen, Y. (2024). Clarabel: an interior-point solver for conic programs with quadratic objectives. arXiv:2405.12762. https://arxiv.org/abs/2405.12762
72. Klaassen, P. (2002). Comment on "Generating scenario trees for multistage decision problems". *Management Science* 48(11):1512-1516. https://doi.org/10.1287/mnsc.48.11.1512.261

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2, `research/literature/01_mpo.lit.md` §2, and the 10 and 11 re-check files (Campi and Garatti; Rockafellar and Uryasev). Metadata was confirmed on Crossref unless another source is named. The G4 barrier re-run does not apply: this dossier quotes no barrier or covenant-breach statistic.

1. §1.3(d): the scenario counts are now 631 and 31,785 (exact Campi-Garatti bound, ε 5%, β 1%), replacing roughly 1,000 and about 60,000. The convexity requirement is stated, and L3 certification is now out-of-sample binomial bounds, not the scenario approach [corrected].
2. §2.5 item 2: the attribution now reads "the scenario approach (Calafiore and Campi 2006), with the exact bound of Campi and Garatti (2008, Thm 2.4)". Calafiore and Campi's looser bound is noted, the convexity requirement is explicit, and N is 631 / 31,785 [corrected].
3. §2.5 item 3 and ref 53: Mohajerin Esfahani and Kuhn (2018), *Mathematical Programming* 171(1-2):115-166, with the full title and DOI 10.1007/s10107-017-1172-1. Replaces the arXiv-only entry marked "journal version not verified".
4. §2.2 and ref 16: Campbell and Viceira (2002) is confirmed (OUP, DOI 10.1093/0198296940.001.0001); "(unverified)" removed.
5. §3.1 and new ref 72: Klaassen (2002) is named as the "published comment" and added to §10: *Management Science* 48(11):1512-1516, DOI 10.1287/mnsc.48.11.1512.261.
6. §3.1 and ref 59: Pflug and Pichler (2012), *SIAM J. Optim.* 22(1):1-23, DOI 10.1137/110825054; "(unverified)" removed.
7. §3.2 and ref 25: Dowson (2020), *Networks* 76(1):3-23, DOI 10.1002/net.21932. The dossier's title is the journal title and is kept.
8. §3.5 and ref 14: Calafiore (2008), *Automatica* 44(10):2463-2473, DOI 10.1016/j.automatica.2008.02.007; "venue details unverified" removed.
9. §3.6 and ref 4: Bailey et al. (2017), *Journal of Computational Finance* 20(4):39-69 (first published 19 Sep 2016; publisher page), DOI 10.21314/jcf.2016.322; "(unverified)" removed.
10. Ref 63: Rockafellar and Uryasev (2000), *Journal of Risk* 2(3):21-41, DOI 10.21314/JOR.2000.038; the "from memory" note is removed.
11. §2.1 and ref 62: Powell's arXiv:1912.03513 now cites its published chapter (2021), *Handbook of Reinforcement Learning and Control*, Springer, pp. 29-74, DOI 10.1007/978-3-030-60990-0_3. The arXiv ID is kept as the preprint.
12. Ref 10: Brandt, Goyal, Santa-Clara and Stroud (2005): DOI 10.1093/rfs/hhi019 added; the NBER link is kept as the working paper.
13. Ref 12: Brown, Dimmock, Kang and Weisbenner (2014) is cited through the *AER* (DOI 10.1257/aer.104.3.931), not NBER w15861. The subtitle "evidence and implications" is restored.
14. Ref 19: Cariño et al. (1994): full title restored; DOI 10.1287/inte.24.1.29 added.
15. Ref 49: Luxenberg et al.: the ICAIF '22 version is added (five authors confirmed; pp. 249-256; DOI 10.1145/3533271.3561769).
16. Ref 51: Merton (1993): ch. 7, pp. 211-242 (from the NBER chapter PDF cover page), NBER chapter c6102, earlier version NBER WP 3820.
