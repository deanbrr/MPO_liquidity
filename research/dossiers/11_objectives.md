# Stream 11 — Objective design for ADIC's multi-period optimizer
## Target attainment with mandatory distributions, leverage and illiquidity

*As of 2026-10-18. Provenance tags: **[S]** sourced fact (full citation in §10); **[P]** practitioner consensus; **[I]** own inference or own computation (illustrative only, not calibrated to ADIC data). Research note: the workflow's shared web-search budget ran out partway through this stream. Later checks used direct fetches of primary pages plus Crossref/RePEc metadata. Items not verified are flagged and are not load-bearing.*

---

## 1. Executive summary

**The core problem.** The brief asks the optimizer to "meet distributions with near-certainty, survive liquidity stress, preserve long-run value, and pursue a 10% return". These are four different mathematical objects. Collapsing them into one scalar (e.g., "maximize P(10%)") causes most of the pathologies discussed below.

| Goal (IC language) | Right mathematical object | Tractable surrogate | Horizon |
|---|---|---|---|
| Meet distributions with near-certainty | Joint **chance constraint** on a cash-coverage process: a liability-reliability constraint | CVaR of the path-maximum liquidity deficit ≤ 0, robust across model variants | Rolling 5y for the minimum payout; 12m for the planned payout |
| Survive liquidity stress | **Robust feasibility**: stay in a "safe set" (viability) under a named stress set, plus a bound on hard breaches | Linear robust counterpart over a polyhedral stress set; scenario CVaR on forced-sale volume | 30 days (margin), 12 months (calls), 24 months (distribution drought) |
| Preserve long-run value | **Fractional-Kelly growth** of *real* NAV net of distributions, plus a drawdown/ruin bound | CRRA (γ≈3) power-cone objective; risk-constrained Kelly bound $E[G^{-\lambda}]\le 1$ | 10y rolling, with a terminal value |
| Pursue 10% | An **aspiration level** inside a shortfall-aware criterion. It is *reported* as P(10%), never maximized as an indicator | Lower partial moment (Fishburn α=2) of the log-return shortfall versus ln 1.10 | 10y rolling (5y secondary) |

**Critique of the user's two-tier design. Keep the architecture, fix the content.**
"Robust floor and liquidity gate first, stretch second" is the right shape. Control engineers would call it a *safety filter* wrapped around a performance controller [S: Wabersich & Zeilinger; Ames et al.]. Five problems need fixing:

1. **The Tier-1 floor is numerically infeasible as written.** "Worst-case 5-year annualized return ≥ 7% with ≤ 5% breach probability" requires annual log-volatility of **≤ 3.8%** if the median return is 10%. Even at the deck's 11.6% expected return it requires ≤ 5.7% [I]. The 10-year version requires ≤ 5.3% (median 10%). A de-smoothed endowment-model portfolio with ~60% PE runs at roughly 11–17% volatility. At that level, with expected arithmetic returns of 8.5–10%, P(5-yr annualized < 7%) is about 31–49% [I]. The deck's "≈2% breach" implies about 5% volatility and should be re-derived. The broad endowment universe's 10-year average return was **6.8% (FY2024)** and **7.7% (FY2025)** [S: NACUBO-Commonfund via ai-CIO]. A 7% floor sits *inside* the central range of outcomes, not in the tail.
2. **P(10%) is the most risk-seeking criterion possible below target.** It is Fishburn's α=0 case. Browne's continuous-time solution maximizes $P(W_T\ge b)$ by replicating a *digital option*: $P^*=\Phi(\Phi^{-1}(xe^{rT}/b)+\theta\sqrt T)$ [S]. With Sharpe 0.42 over 5 years, $P^*\approx 94\%$, bought with a ~6% chance of near-total loss [I, from the S formula]. In our discrete dynamic program (leverage capped at 3×), the P-maximizing policy lifts P(5y ≥ 10% p.a.) from **34.5% to 67.5%**. But P(a >40% five-year loss) rises from **0.0% to 4.6%**, and leverage stays pinned at 3× whenever wealth is on or below the target path [I].
3. **Distributions, illiquidity creep and margin are missing from the constraint set.** These are what actually break an endowment-model fund. Harvard's 2025 secondary talks (~$1bn) and $1.2bn of contingency bond issuance [S] show these levers being pulled under stress.
4. **The design is not time-consistent.** End-of-horizon floors and P(target at T) change meaning as the horizon approaches [S: Shapiro 2009]. They invite gambling near deadlines and de-risking once "safe".
5. **Strict lexicographic ordering hides the price of safety.** The IC should see what each unit of reliability costs in growth and P(10%).

**Recommended specification: "safety-filtered, shortfall-aware growth" (SSG).**
$$\max_{\pi\in\Pi}\; E_{\hat P}\Big[U_\gamma\big(W^{real}_{H}/W^{real}_0\big)\Big]\;-\;\lambda_T\Big\|\big(\ln 1.10-\tfrac1H\ln \mathrm{TWR}_H\big)_+\Big\|_{L^2(\hat P)}$$
subject to:
- **(C1)** robust distribution reliability: $\max_{m\in\mathcal M}\mathrm{CVaR}^{P_m}_{1-\varepsilon_D}\big(\max_{t\le 5y}\Delta_t\big)\le 0$;
- **(C2)** 24-month survival under named stress with no forced private sales;
- **(C3)** real drawdown bound via $E[G^{-\lambda}]\le1$;
- **(C4)** a re-specified robust floor: worst-model $\mathrm{CVaR}_{10\%}$ of the 10-year annualized nominal TWR ≥ 0%, with the robust *median* reported against 7%;
- **(C5)** structural limits: leverage, NAV-loan LTV, overcommitment, overlay margin coverage;
- **(C6)** the payout rule.

**Starting numbers (IC-adjustable, with rationale in §6.5):**

| Parameter | Default |
|---|---|
| Joint 5-year probability of failing the 5% minimum distribution without forced sales | 1% (≈0.2%/yr), in **every** model variant |
| Planned-payout reliability over 12 months | 97.5% |
| Survival horizon under named stress | ≥ 24 months |
| P(forced secondary sale within 5y) | ≤ 1% (robust) |
| Real drawdown | ≤ 30% with ≥ 95% probability over 10y (λ=8.4) |
| Economic leverage | ≤ 1.3× |
| Overlay initial margin plus P99 variation margin | Covered by unencumbered HQLA |
| Private NAV + unfunded | ≤ 80% of NAV |

**How the 10% target relates to the 5–10% payout band.** Real NAV is preserved if and only if $(1+g)(1-d)=1+\pi$. At 2.5% inflation, a 10% *geometric* nominal return sustains a payout of **d ≈ 6.8%** [I]. The other ends of the band need: d=5% → 7.9%; d=7.5% → 10.8%; d=10% → 13.9% [I].
- J.P. Morgan's 2026 assumptions put PE at 10.2%, global equities at 7.0% and a USD 60/40 at 6.4% [S].
- A 60% private / 40% liquid mix therefore lands near 8.5–9% *arithmetic* [I]. In our models, P(10-yr ≥ 10%) is about 30–40%.
- Payouts above ~7% of NAV are, in expectation, transfers from future to current owners.

**Leverage.** Leverage adds P(10%) slowly but adds tail and liquidity risk quickly.
- In a lognormal model, 10-year P(≥10%) rises from 28% (1.0×) to 45% (1.5×) [I].
- In a toy ALM with PE cash-flow regimes, 1.4× overlay leverage with a thin reserve raised P(10y ≥ 10%) by about 5pp, with *no* change in the median. It raised P(forced secondary sale within 5y) from ~0% to **11%** (21% under stagflation) [I].
- A tail hedge cut that to 4% (12%). **The tail hedge's value shows up in the constraints, not in expected return.** It must be priced through shadow prices, not on standalone carry.

**Market context (dated).** MSCI reports closed-end PE funds returned **12% of asset value in 2025**, just over half the ~20% 20-year average. Buyout distributions were **12% in H1 2026** against a ~27% historical average, despite series-high top-quartile exit multiples (18.2× EBITDA, highest since the series began in 2016) [S].

**For the IC.** Replace a single target-attainment number with:
- a four-panel frontier: P(10%) vs P(hard breach); robust floor vs P(10%); real NAV vs payout; survival horizon;
- a price-of-safety table taken from the duals;
- a fragility index (robust satisficing);
- a gambling detector.

The IC owns ε, horizons, drawdown limits and the payout rule, fixed per review cycle (cf. CPP's triennial reference-portfolio review [S/P]).

---

## 2. Core concepts & theory

### 2.1 Why "maximize the probability of hitting the target" fails

**Browne's digital-option result [S].** Browne (1999, *Adv. Appl. Probab.* 31(2):551–577) studies wealth split between n risky stocks and a risk-free asset. Maximizing the probability of reaching a wealth level by a deadline is "equivalent to simply buying a European digital option". In the multi-asset case the log-optimal portfolio replaces the stock. Nielsen (2013, arXiv:1311.2550) restates the value function and policy:
$$J(\pi,t)=\Phi\!\Big(\Phi^{-1}(\pi/b)+\tfrac{\mu-r}{\sigma}\sqrt{T-t}\Big),\qquad \alpha(\pi,t)=\frac{\varphi(\nu)}{\sigma\sqrt{T-t}\,\Phi(\nu)},\ \ \nu=\Phi^{-1}(\pi/b).$$
Here α is the fraction in the risky asset. It **diverges as t→T**. Nielsen notes: "A strategy with finitely capped leverage would have J(π,T) = 0 for π < b." With discounting, the time-0 maximum is $P^*=\Phi(\Phi^{-1}(xe^{rT}/b)+\theta\sqrt T)$. The residual $1-P^*$ is the probability of ending near zero, because the payoff is all-or-nothing.

**Discrete-time evidence [S].** Das, Ostrov, Radhakrishnan & Srivastav maximize P(goal) by dynamic programming over a set of efficient portfolios. MathWorks' implementation of their method notes that when wealth is low the optimal choice is the higher-return portfolio "even at the cost of increasing the volatility". Near the horizon, choices become more extreme, either very aggressive or very conservative (paraphrase).

**Same failure in hedging and risk management [S].**
- Föllmer & Leukert's *quantile hedging* (F&S 1999) maximizes the probability of a successful hedge under a budget. Their follow-up, *efficient hedging* (Föllmer & Leukert 2000, F&S 4(2)), calls it a dynamic version of VaR that ignores shortfall *size*, and replaces it with expected loss-weighted shortfall.
- Basak & Shapiro (2001) find that "VaR risk managers often optimally choose a larger exposure to risky assets than non-risk managers". They "consequently incur larger losses when losses occur". An expected-loss constraint mitigates this.
- Lesson: probability constraints or objectives on *wealth outcomes* must be replaced by, or accompanied by, expectation-of-shortfall terms.

**Fishburn's α–t family [S; standard definitions].** Fishburn (1977, *AER* 67(2)) measures risk as $\rho_\alpha(t)=E[(t-R)_+^\alpha]$.
- α=0 gives the shortfall *probability*.
- α=1 gives expected shortfall below target.
- α=2 gives below-target semivariance.
- In Fishburn's mean-risk model, α<1 implies risk-seeking below target and α>1 implies risk aversion below target.
- **P(target) is the extreme α=0 case**, so any objective built on it rewards gambling when behind.

Behavioral finance gives the same warning. Prospect theory (Kahneman & Tversky 1979) documents risk-seeking in the loss domain relative to a reference point [S]. IC discussions framed as "are we on track for 10%?" invite exactly that response. This is a presentation problem as much as a model problem [I].

**Shortfall-aware aspiration criteria [S].** Chen & Sim's *goal-driven optimization* (OR 2009) "maximizes the shortfall-aware aspiration-level criterion". It combines the probability of success with expected shortfall, and it reduces to CVaR linear programs (SOCP under robust decision rules). This is the right family for ADIC's target term.

### 2.2 Floors, cushions and ratchets: the opposite policy shape

**Dybvig's protected spending [S].** Dybvig (1999 FAJ; working draft Oct 1998) splits the portfolio into:
- a riskless reserve worth the perpetuity value of current spending, $s_t/r$;
- a risky cushion: $\alpha_t=K(w_t-s_t/r)$, with spending increased only to keep $s_t\ge r^*w_t$.

Two of his propositions matter directly for ADIC:
- No fund can guarantee a perpetual spending level above (current endowment × riskless rate).
- "Capital preserved on average" is not preservation. With a 10% mean, 30% standard deviation, 3% inflation and 4.5% spending, the real endowment tends to zero almost surely.

The strategy outperforms in persistent trends and loses in whipsaw markets, which is the cost of protection. Grossman & Zhou (1993) obtain the drawdown analogue: invest in proportion to $W_t-\alpha M_t$ where $M_t$ is the running maximum [S]. Browne (1997, *Math. OR*) shows that with a fixed withdrawal stream, state space splits into a **"danger zone"** where ruin is possible and a **"safe region"** where ruin can be avoided with certainty [S]. Dybvig's 1995 ratchet is extreme habit formation (cf. Constantinides 1990) [S].

**The design principle [I].** Floor-protecting policies set *risk ∝ cushion*: they cut risk as the fund approaches the floor. Target-chasing policies set *risk ∝ shortfall to goal*: they add risk when behind. ADIC's risk budget, leverage and illiquid pacing should be **monotone non-decreasing in the cushion**, defined as the distance above the protected-distribution floor. That monotonicity can be imposed as a constraint on decision rules (§6.9).

### 2.3 Coherent tail measures, chance constraints and drawdown surrogates

- **CVaR [S].** Rockafellar & Uryasev (2000, 2002):
  $$\mathrm{CVaR}_\beta(L)=\min_\eta\{\eta+(1-\beta)^{-1}E[(L-\eta)_+]\}.$$
  It is linear-programmable on scenarios, and β-VaR ≤ β-CVaR. CVaR is coherent (Artzner et al. 1999) [S].
- **Chance constraints [S].**
  - The concept originates with Charnes & Cooper (1959). Its antecedents are Roy's (1952) safety-first and Leibowitz & Henriksson's (1989) shortfall-constraint "confidence-limit" approach.
  - $\mathrm{CVaR}_{1-\varepsilon}(\Delta(x,\xi))\le0 \Rightarrow P(\Delta(x,\xi)>0)\le\varepsilon$, because VaR ≤ CVaR. This is the standard convex conservative surrogate for a chance constraint. Nemirovski & Shapiro (SIAM J. Optim. 17(4), 2006/07) develop such convex conservative approximations, whose feasible sets lie inside the chance-constrained set, including a Bernstein approximation.
  - The **scenario approach** (Calafiore & Campi 2006), with the exact bound of Campi & Garatti (2008, Thm 2.4), certifies the violation probability ε of a convex program solved on N sampled scenarios with d decision variables, via $\sum_{i<d}\binom{N}{i}\varepsilon^i(1-\varepsilon)^{N-i}\le\beta$. Required sample sizes [I]:

    | ε | d | β | N |
    |---|---|---|---|
    | 1% | 10 | 10⁻⁶ | 3,260 |
    | 1% | 50 | 10⁻⁶ | 9,086 |
    | 1% | 200 | 10⁻⁶ | 27,418 |
    | 5% | 50 | 10⁻⁶ | 1,801 |
- **Joint versus per-period [I].** A joint 5-year reliability of 99% requires about 0.2% per year: the union bound gives ε/H and independence gives $1-(1-\varepsilon)^{1/H}$; both equal 0.0020. Over 10 years it requires 0.1% per year. Per-year statements to the IC must be translated.
- **Drawdown [S].**
  - Chekhlov, Uryasev & Zabarankin (2005) define Conditional Drawdown (CDD/CDaR): the mean of the worst (1−α) drawdowns. It is CVaR-like and includes max and average drawdown as limits.
  - Busseti, Ryu & Boyd (2016): for any α, β with λ = log β / log α, $E[(r^Tb)^{-\lambda}]\le1 \Rightarrow \mathrm{Prob}(W_{\min}<\alpha)<\beta$. The resulting risk-constrained Kelly problem is convex.
  - For ADIC, set $r^Tb\to G_t=(1+R_t)(1-d_t)/(1+\pi_t)$, the gross real growth of NAV net of distributions. With α=0.7, β=0.05, λ = 8.40 [I]. The bound is conservative and derived for i.i.d. bets, so it should be used per regime, or as a screen validated by simulation.

### 2.4 Satisficing and robust satisficing

- **Brown & Sim (2009) [S].** Satisficing measures are "dual to classes of risk measures". Aspiration levels, whether competing benchmarks or fixed targets, are easier to specify than risk-aversion parameters. The measures carry an ambiguity interpretation.
- **Long, Sim & Zhou (2023, OR 71(1)) [S].** Their robust-satisficing model is
  $$\kappa_\tau=\min_{x,k\ge0}\;k\quad\text{s.t.}\quad E_P[f(x,\tilde z)]-\tau\le k\,\Delta(P,\hat P)\ \ \forall P,$$
  with target τ ≥ Z₀ (the empirical optimum). It "minimizes the fragility of the system". It asks the decision maker for a *target* rather than an ambiguity radius, and it reduced the optimizer's curse out of sample in their portfolio study.
- **Mapping to ADIC [I].**
  - τ = the IC's tolerance on the 10% shortfall measure, or on constraint slack.
  - κ = a **fragility index**: how much expected target violation can occur per unit of Wasserstein distance between the true and the modeled distribution.
  - It answers the question the IC actually asks: "how wrong can our forecasts be before we miss?"
  - Dispersion between underwritten, actual and forecast returns for an asset is natural evidence for that asset's ambiguity radius.

### 2.5 Time consistency, horizon, and how "10%" is measured

- **Time consistency [S].**
  - Shapiro (2009, ORL 37(3)) asks whether optimal decisions planned now remain optimal when the problem is re-solved later.
  - Nested (composite) risk measures built from conditional risk mappings (Ruszczyński & Shapiro 2006) and risk-averse DP (Ruszczyński 2010) are time-consistent.
  - CVaR of *terminal* wealth and P(target at T) are generally not.
- **Practical resolution [I].**
  - (i) Impose liquidity and distribution risk **per period** (nested or rolling), so each year's constraint is re-imposed on the conditional distribution.
  - (ii) Pursue growth and target goals by **rolling-horizon MPC** with a terminal value function. The deadline then never arrives and Browne-type explosion cannot occur.
  - (iii) Treat parameter stability as **IC pre-commitment** for a review cycle.
- **Horizon arithmetic [I].** Under i.i.d. returns, the volatility of the annualized return is σ/√T: about 8.7% (3y), 6.7% (5y) and 4.7% (10y) for σ=15%. P(T-yr ≥ 10%) is near 50% at any horizon when the median is 10%. The horizon mostly changes the *floor* probabilities. Regime persistence (PE droughts, stagflation) makes long-horizon dispersion shrink more slowly than √T, which our toy model reproduces.
- **Measurement conventions [I/P].**
  - P(5-yr annualized ≥ 10%) and P(cumulative ≥ 61%) are the same event.
  - "Average annual return ≥ 10%" (arithmetic) is easier.
  - "≥ 10% every year" is far harder.
  - The geometric target needs roughly μ − σ²/2 ≥ 10%, about 11.1% arithmetic at σ=15%.
  - Recommend: target = **10-yr rolling geometric time-weighted return, nominal USD, gross of distributions** (peer-comparable: NACUBO and Yale report 10-yr figures). Sustainability = **real NAV net of distributions**.

### 2.6 Distributions, illiquidity and the owner's balance sheet

- **Payout identity [I].** $W^{real}_{t+1}=W^{real}_t(1+R_{t+1})(1-d_t)/(1+\pi_{t+1})$. Long-run real growth is $E\ln(1+R)+\ln(1-d)-E\ln(1+\pi)$.
- **Intergenerational equity [S/P].** Tobin (1974) framed the endowment-income question this way (full text not accessed in-session). Yale makes it explicit: its rule "creates a cushion when endowment returns fall and instructs discipline when they rise" [S].
- **Total-wealth view [S].** Merton (1993) criticizes treating the endowment "as if it were the only asset". For a sovereign owner, the owner's other revenues define the *liability correlation* of distribution demand. Fiscal needs that rise when commodity revenue falls would make ADIC's payouts wrong-way risk [I, to be tested with ADIC data].
- **Illiquidity [S].**
  - Ang, Papanikolaou & Westerfield (2014) show illiquidity induces "increased and state-dependent risk aversion". Investors would give up ~2% of wealth to hedge illiquidity crises occurring once a decade.
  - Gourier, Phalippou & Westerfield (2024, JF 79(5)) find commitment risk leaves investors under-allocated to private funds. They would pay more to adjust committed quantities than to remove timing uncertainty or limited tradability.
- **Dividend and ruin analogues from actuarial science [S].**
  - The de Finetti dividend problem (reviewed by Avanzi 2009) maximizes expected discounted dividends until ruin; on its own it does not control ruin. As a template for ADIC's payout problem (pay the owner while controlling ruin), it needs an added ruin constraint or penalty, such as the Gerber–Shiu penalty below [I].
  - Barrier and band strategies (pay more only above a cushion barrier), surveyed by Avanzi (2009), are natural rules for the 5–10% band. Paying a protected minimum below the barrier is ADIC's adaptation; the classic barrier strategy has no minimum payout [I]. Ratcheting variants (Dybvig 1995) are a further candidate.
  - Gerber & Shiu (1998) penalize ruin by *timing and severity* (expected discounted penalty), which is better than a bare probability.
- **Behavior [S].** Brown, Dimmock, Kang & Weisbenner (2014) find endowments cut payouts below stated policy after negative shocks but do not raise them after positive shocks ("hoarding"). Real-world payout policies flex. Whether ADIC's 5% minimum can flex is the single most important constraint-design question (§9).

---

## 3. Methods/models and trade-offs

### 3.1 Objective families compared

| Family | Captures | Pathology | Tractability | Time-consistent? | IC readability |
|---|---|---|---|---|---|
| Max P(target) (Browne; GBWM DP) | Aspiration | Digital payoff; gambling below target; de-risk when ahead | DP in low dimension | No | High but misleading |
| Expected shortfall / LPM (Fishburn α≥1) | Size of misses | α=1 is risk-neutral below target; needs a concave partner | LP/SOCP | Partly (if rolling) | Medium |
| CVaR constraints / objectives (R–U) | Tail of losses or deficits | Ignores beyond-tail shape; level choice | LP on scenarios | Nested CVaR: yes | Medium |
| Utility with floor/habit (Dybvig, Constantinides, HARA) | Protect commitments; risk ∝ cushion | Whipsaw cost; floors can be infeasible | Power cone / DP | Yes (expected utility) | Low unless translated |
| Drawdown control (Grossman–Zhou; CDaR; RCK) | Path losses | Over-conservative after peaks | LP (CDaR), convex (RCK) | Mostly | High ("max loss from here") |
| Satisficing / robust satisficing | Target plus model error | Needs τ; conservative in calm data | LP/SOCP under Wasserstein | Rolling only | High ("how wrong can we be?") |
| Lexicographic two-tier | Priorities | Boundary-hugging; hidden prices | Sequence of LPs | Depends | High |
| ε-constraint Pareto sweeps | Explicit trade-offs and duals | Many solves | Parallel LPs | Rolling | Highest |
| Nested risk / risk-averse SDDP | Multistage consistency | Opaque; stagewise independence assumptions | SDDP (Pereira & Pinto 1991; Philpott & de Matos 2012) | Yes | Low |

### 3.2 Quantitative illustrations [I]

Own computations: lognormal annual returns, cash 3.5%, borrowing 4.0%. These are not ADIC numbers.

**(a) Attainable set under leverage.** Unlevered portfolio μ₀ = 8.5%, σ₀ = 12% (Sharpe 0.42), consistent with JPM-style CMAs for a 60% PE mix. Columns "Real NAV ≥ start" give P(real NAV at 10y ≥ start) by payout rate d.

| Leverage | P(5y≥10%) | P(10y≥10%) | P(5y<7%) | 10y annualized q05 | 10y annualized CVaR₀₅ | Real NAV ≥ start, d=5% | d=7.5% | d=10% |
|---|---|---|---|---|---|---|---|---|
| 1.0× | 34% | 29% | 44% | +1.8% | +0.4% | 49% | 22% | 6% |
| 1.5× | 47% | 45% | 38% | +0.5% | −1.6% | 60% | 40% | 21% |
| 2.0× | 52% | 53% | 37% | −0.9% | −3.6% | 64% | 49% | 33% |
| 3.0× | 56% | 59% | 36% | −3.9% | −7.5% | 67% | 56% | 44% |

Kelly leverage is $(\mu_0-r_b)/\sigma_0^2\approx3.1$×. That is a theoretical ceiling, not a target. Illiquidity raises effective risk aversion (§2.6).

**(b) Dynamic versus constant-mix bounds (5y, 10% target).**
- Browne's unconstrained-leverage maximum P* = 90.4% / 94.2% / 96.9% for Sharpe 0.30 / 0.42 / 0.55.
- The best *constant* leverage gets only 45.6% / 56.3% / 67.3%, at about 35% volatility.
- The gap between the two is bought entirely with digital-like tails.

**(c) The gambling pathology in a discrete DP** (annual steps, leverage menu 0.5–3.0×, grid DP):

| Policy | P(5y≥10%) | 5y annualized q05 | 5y annualized CVaR₀₅ | P(W₅ < start) | P(W₅ < 0.6) |
|---|---|---|---|---|---|
| P-max dynamic | 67.6% | −9.2% | −14.2% | 15.8% | 4.6% |
| Constant 1.0× | 34.1% | −0.6% | −2.6% | 6.3% | 0.0% |
| Constant 1.5× | 46.3% | −3.0% | −5.8% | 11.0% | 0.4% |
| P-max + shortfall penalty (λ=10) | 51.8% | −1.4% | −3.9% | 10.6% | — |

The P-max policy holds 3× at every date whenever wealth is ≤ 100% of the target path. When 15–30% ahead in years 3–4 it drops to 0.5–0.75×. A shortfall penalty on $E[(1-W)_+]$ restores sensible tails at a visible cost in P(10%).

**(d) Feasibility of the deck's floor.** The table gives the maximum annual log-volatility at which P(T-yr annualized < 7%) ≤ 5%:

| Median annualized return | T=5 | T=10 | T=20 |
|---|---|---|---|
| 9% | 2.5% | 3.6% | 5.0% |
| 10% | 3.8% | 5.3% | 7.5% |
| 11.6% | 5.7% | 8.1% | 11.4% |

Only a 20-year horizon with an 11.6% median approaches realistic volatility.

**(e) Toy ALM frontier with PE cash flows, overlay margin and payouts.** Payout d=7.5% of prior NAV; 20,000 paths; 10 years; common random numbers.

Model set-up:
- Regime-switching equity: Normal 11%/14%, Stress −15%/20%; P(N→S)=12%, P(S→S)=40%.
- PE economic return = exp(0.022 + 1.1·ln(1+r_E) + 0.07z) − 1.
- PE distribution rates: 17%/6% of NAV (base); 12%/5% (drought variant); 14%/5% with more frequent stress and bond losses (stagflation variant).
- Capital calls: 25%/20% of unfunded.
- Pacing ≤ k·NAV, capped at P+U ≤ 78% of NAV and halved in stress.
- Overlay: initial margin 10% of notional; variation margin paid from the reserve.
- Tail hedge: 50%-of-NAV put spread from −15% to −35%, premium 0.75% of NAV per year.
- Opportunistic overlay: mean 0.4%, vol 1.5% of NAV.
- Facility: 5% of NAV.
- Secondary discount: 30% in stress, 10% otherwise.
- Liquidity waterfall: reserve → sell liquid → facility → PE secondary → payout cut.

| Policy (reserve, leverage, hedge) | P(10y≥10%) base / stag | Median 10y | 10y annualized q05 | 5y annualized CVaR₀₅ | P(hard breach in 5y) base / drought / stag | Median real NAV₁₀ |
|---|---|---|---|---|---|---|
| A static (10%, 1.0×, none) | 35.1% / 25.1% | 7.7% | −4.2% | −13.7% | 0.0 / 0.0 / 0.2% | 0.79 |
| **B robust (10%, 1.2×, tail hedge)** | 36.6% / 26.2% | 7.7% | −4.7% | −14.3% | 0.0 / 0.1 / 0.6% | 0.79 |
| C chase (5%, 1.4×, none) | 40.1% / 28.5% | 7.7% | −12.4% | −30.0% | 10.7 / 14.8 / 21.3% | 0.78 |
| D chase + hedge (5%, 1.4×, hedge) | 39.1% / 28.1% | 7.7% | −8.3% | −21.0% | 4.1 / 7.1 / 11.6% | 0.78 |
| E defensive (15%, 1.0×, hedge) | 32.1% / 23.0% | 7.5% | −2.0% | −9.3% | 0.0 / 0.0 / 0.0% | 0.78 |

Reads [I]:
- **(i)** Target-chasing (C) buys +3.5pp of P(10%) over B for +10.7pp of hard-breach probability, with no change in the median. The rate of substitution (~0.33pp of P(10%) per pp of breach risk) is a bad trade the IC should see explicitly.
- **(ii)** The hedge's main contribution is to liquidity reliability (C→D), not to return.
- **(iii)** The robust-feasible set (hard breach ≤ 1% in *all* variants) shrinks as payout rises: 18, 16 and 8 of 36 policies at d = 5%, 7.5% and 10%.
- **(iv)** Payout dominates real value. Median real NAV₁₀ is ~1.00 at d=5%, ~0.79 at 7.5% and ~0.62 at 10%.
- **(v)** Funding payouts from liquid assets drives *illiquidity creep*: P+U rises from ~0.65 to ~0.75 of NAV by year 5 as d rises. This is why pacing must be a control coupled to the distribution constraint.
- The toy is deliberately severe (high volatility, persistent regimes), so its negative 10-year q05 values overstate realistic long-horizon dispersion.

---

## 4. Empirical evidence & current market data (dated, sourced)

- **PE cash drought [S].**
  - MSCI (chart dated 2026-06-11; data to Q4-2025): closed-end PE funds returned **12% of asset value in 2025**, "just over half the 20-year average". "Private-equity distributions have stayed near decade lows for four straight years."
  - MSCI (2026-10-13; data to Q2-2026): buyout distribution rate **12% in H1-2026**, down from 15% in 2025, versus a ~27% historical average. Top-quartile exit multiple **18.2× EBITDA**, median 12.5×, net cash flow +USD 21bn in H1-2026. Their verdict: "the distribution drought is unlikely to end simply because exit conditions have become more favorable."
  - Implication [I]: DPI-based liquidity assumptions should centre on 10–15% distribution rates with multi-year persistence, not the 20–27% historical norm.
- **Endowment returns [S].**
  - NACUBO-Commonfund FY2025 (published 2026-02-12): average **10.9%**; annualized 3y 10.0%, 5y 10.2%, **10y 7.7%** (6.8% a year earlier), 15y 8.5%, 20y 7.3%, 25y 6.6%; $944bn across 657 institutions.
  - The $5bn+ cohort averaged **11.8%** in FY2025 (TIFF). The largest endowments' top concerns are "federal funding cuts and liquidity". Endowments funded 15.2% of operating budgets.
- **Yale [S].**
  - FY2025 return 11.1%; 10y 9.4% p.a.; $15.3bn spent over 10 years (60% of starting value).
  - Spending rule: **0.80 × last year's spending + 0.20 × (5.25% × endowment value)**.
  - Without investment growth the endowment "would be entirely depleted in less than 30 years".
- **Capital-market assumptions [S].** J.P. Morgan 2026 LTCMA (released 2025-10-20; 10–15y horizon): USD 60/40 **6.4%**; 60/40 + 30% alternatives 6.9%; US large cap 6.7%; global equities 7.0%; **private equity 10.2%**; US core real estate 8.2%; intermediate Treasuries 4.0%; IG credit 5.2%; high yield 6.1%. (A 2027 edition may have been published around this date but was not retrieved.)
- **Liquidity actions under stress [S].** In April 2025, Harvard Management Company was in talks to sell ~$1bn of PE fund stakes (~5% of its PE book) to Lexington. PE was nearly 40% of the $53bn endowment. Harvard borrowed $1.2bn in two bond sales in March–April 2025 as "part of ongoing contingency planning for a range of financial circumstances". Yale said it was considering a similar sale. Secondary sales usually clear at a discount to NAV (Rutgers' Longo, quoted in the same article).
- **Sovereign draw rules [S].**
  - Alaska Permanent Fund POMV: draw capped at **5.0%** of average market value over "the first five of the preceding six fiscal years". The FY28 draw is $4.1bn, and it provides "more than 66%" of the state's general fund revenue.
  - Norway: government spending averages the fund's expected real return of about 3%.
- **Reliability standards [S].**
  - Solvency II Art. 101(3): the Solvency Capital Requirement equals the VaR of basic own funds at **99.5% over one year**.
  - Basel III LCR: HQLA must cover a **30-calendar-day** stress, 100% minimum since 2019.
  - Dutch pension FTK solvency test: **97.5%** confidence, a "once-in-40-year" standard (IPE, 2004). FTK funds averaged 131.4% funding in Q2-2026, with transition to the new system due by 2028-01-01 (DNB).
- **Peer risk appetite [S].** CPP Investments benchmarks against an 85/15 global-equity / Canadian-bond Reference Portfolio (CRR 2024). A search summary of CPP's site additionally reports a 55/45 portfolio for the additional CPP because of greater shortfall sensitivity; the page itself was not retrievable in-session.

---

## 5. Practitioner / peer practice & case studies

**How serious long-horizon investors state objectives [S/P].**
- *Norway* and *Alaska* express the payout as a smoothed fraction of fund value, i.e., a sustainability rule rather than a return target.
- *Yale* ties spending to an inertial rule designed to protect budgets and future generations.
- *CPP* expresses risk appetite as a passive **reference portfolio** with a defined equity/bond mix and re-examines it every three years. This is a pre-commitment device that turns "how much risk?" into a one-number choice.
- *Insurers and banks* express reliability as **confidence levels over horizons**: 99.5%/1y for Solvency II, 97.5% for FTK (once-in-40-year), and survival over 30 days for the LCR.

ADIC needs both kinds of statement: a sustainability rule for payouts and confidence-level statements for reliability [I].

**Case: Harvard 2025 [S] as a template for recourse modelling [I].**
- Harvard used two recourse actions: SELL (secondary at a discount) and portfolio-level REFINANCE (bonds).
- In ADIC's optimizer both are *priced recourse variables* in the liquidity waterfall. Secondary sales carry regime-dependent discounts and capacity limits. Borrowing carries spread, tenor and capacity limits.
- A breach is defined by *which* recourse had to be used, not by any recourse at all. Selling liquid assets in a drawdown is "amber"; a forced PE secondary is "red".

**Case: stochastic-programming ALM heritage [S].**
- Multistage stochastic programming with nested risk measures underpins hydro-energy planning (Pereira & Pinto's SDDP, 1991) and its risk-averse extension (Philpott & de Matos 2012).
- Model-predictive control for multi-period portfolios is mature in convex form: Boyd et al. (2017) plan a trade sequence and "only the first one executed".
- This is the computational template for ADIC: plan five years, act on the first quarter, re-plan.

**Case: endowment payout behavior [S].** Brown et al. (2014): payouts were cut after negative shocks but not raised after positive ones. If ADIC's owner tolerates no cut below 5%, ADIC must hold more protection than U.S. endowments typically do. Yale's smoothing illustrates how a rule can intentionally raise the payout *rate* after declines [I].

**Cross-industry transferable ideas [I]:**
- **Bank treasury.** Survival horizon and contingency funding plan map to ADIC's 24-month survival and named recourse ladder. LCR maps to an ADIC-LCR on stressed 12-month outflows.
- **Insurance.** ORSA and risk-appetite statements map to IC-owned (ε, horizon) pairs. The appetite / tolerance / capacity triad maps to amber and red bands.
- **Actuarial science.** Gerber–Shiu severity-and-timing penalties replace bare breach probabilities. The de Finetti barrier gives the payout band rule.
- **Control.** Safety filters and probabilistic reachability: Abate et al. (2008) compute the probability of staying in a safe set under control. This gives the "probability ADIC remains inside its viability kernel".
- **Decision science.** Robust satisficing gives the fragility index. Pre-commitment handles time inconsistency.
- **Machine learning.** The optimizer's curse means frontiers need out-of-sample validation and calibrated probability reporting.

---

## 6. Design implications for the ADIC framework

### 6.1 State variables $s_t$ (quarterly decision epochs; annual distribution epochs)

| Block | Variables |
|---|---|
| Wealth & composition | NAV $W_t$; liquid sleeves $x_{j,t}$ (cash/T-bills, IG, public equity, credit, HF); HQLA after haircuts |
| Private book (asset-level) | NAV $P_{i,t}$; unfunded $U_{i,t}$; vintage/age; three return tracks (underwritten $u_i$, actual $a_{i,t}$, forecast $f_{i,t}$); asset leverage; NAV-loan balance $N_{i,t}$ and LTV; secondary bid/discount $\phi_{i,t}$ |
| Funding | Facility drawn/available $B_t,\bar B_t$; bonds; maturities |
| Overlay | Tail-hedge notional/strikes/expiries; opportunistic risk budget; initial margin $IM_t$; variation margin history; CSA terms |
| Distribution | Last payout $D_{t-1}$; rule state (smoothing window, ratchet level); protected floor $F_t$ |
| Beliefs | Regime posterior $\pi_t$ (HMM/HSMM), fragility; model-variant weights; ambiguity radii $r_i$ |
| Reporting-only | Rolling TWR vs 10%; cushion $c_t=W_t-F_t$ |

### 6.2 Decision variables $a_t$

- **Liquid allocation** $x_t$, rebalancing trades.
- **Commitment pacing** $k_{s,t}$ by strategy.
- **Per-asset lens:**
  - SELL: fraction $q_{i,t}\in[0,1]$ sold at $(1-\phi_{i,t})P_{i,t}$;
  - HOLD (default);
  - REFINANCE: cash-out $n_{i,t}$ via NAV loan or recap, raising $N_{i,t}$;
  - LEVER: add-on exposure $\ell_{i,t}$ at asset-level cost $c_i$.
- **Portfolio borrowing** $b_t$.
- **Overlay:** beta notional $L_t-1$; tail-hedge notional $h_t$; opportunistic risk budget $o_t$.
- **Distribution** $D_t\in[0.05\bar W_t,0.10\bar W_t]$ if ADIC has discretion. Otherwise $D_t$ is a stochastic, state-dependent liability.

### 6.3 Dynamics and liquidity accounting

The cash balance $C$ is HQLA (cash, T-bills, IG, minus haircuts):
$$C_{t+1}=C_t(1+r^c)+\textstyle\sum_i\mathrm{Dist}_{i,t+1}-\sum_i\mathrm{Call}_{i,t+1}-D_t-VM_{t+1}-\Delta IM_{t+1}-\mathrm{Int}_{t+1}-\mathrm{Prem}_t+\mathrm{Payoff}_{t+1}+\sum_i q_{i,t}(1-\phi_{i,t})P_{i,t}+\sum_i n_{i,t}+b_t$$

The liquidity deficit is $\Delta_t=\underline C_t-C_t$, where the floor $\underline C_t$ = encumbered IM + operational minimum. Recourse is ordered: liquid sales (amber) → facility (amber) → PE secondary (red) → payout shortfall (critical).

The 12-month **ADIC-LCR** is HQLA^haircut divided by the sum of:
- the minimum payout;
- P95 calls;
- P99 VM;
- debt service;
- less P5 distributions.

The **survival horizon** $\tau_{surv}$ is the first month in which cumulative stressed net outflows exceed HQLA plus committed facilities.

### 6.4 Recommended program (P)

$$\max_{\theta}\; J(\theta)=E_{\hat P}\!\big[U_\gamma(W^{real}_{H}/W^{real}_{0})\big]-\lambda_T\big(E_{\hat P}[(\ln1.10-\tfrac1H\ln\mathrm{TWR}_H)_+^2]\big)^{1/2}$$
Notation:
- $U_\gamma(w)=(w^{1-\gamma}-1)/(1-\gamma)$, with γ=3 (≈1/3 Kelly). γ→1 recovers log/Kelly.
- H = 10y rolling, with a terminal value.
- θ = parameters of decision rules (or first-stage decisions in a scenario tree).
- Both terms are concave in θ when wealth is affine in θ, so (P) is a power-cone/SOC program.

Subject to:
- **(C1) Distribution reliability, robust:** for every model variant m ∈ 𝓜,
  $$\eta_m+\tfrac{1}{\varepsilon_D}E_{P_m}\big[(z-\eta_m)_+\big]\le0,\qquad z\ge\Delta_t\ \ \forall t\le 5y.$$
  This is the CVaR of the path-maximum deficit. Add the per-year version for the next 12 months at the planned payout with ε=2.5%.
- **(C2) Survival:** $\Delta_t(\xi)\le 0$ for all $\xi\in\Xi_{stress}$ and $t\le 24$ months. $\Xi_{stress}$ is a polyhedral set: PE distribution rate ∈ [0, 5%], calls ∈ [1.0, 1.5]× base, equity ∈ [−40%, 0], VM at P99.5, facility availability ≥ 50%, secondary discount ∈ [25%, 40%]. No PE secondary is allowed in this test.
- **(C3) Real drawdown:** $E_{\hat P}[G_t^{-\lambda}]\le1$ with λ = ln 0.05 / ln 0.7 = 8.40, per regime. Validate by simulation: P(min real NAV < 0.7 W₀) ≤ 5%. The CDaR alternative is $\mathrm{CDaR}_{0.95}\le 25\%$.
- **(C4) Robust floor (re-specified):** $\max_m \mathrm{CVaR}^{P_m}_{0.90}(-R^{ann}_{10})\le 0$, i.e., no nominal lost decade in the 10% tail even under the worst variant. *Report* the robust median of $R^{ann}_{10}$ against 7%, which keeps the deck's 7% as a central-tendency test rather than a tail floor.
- **(C5) Structural limits:**
  - economic leverage ≤ 1.3×;
  - overlay notional ≤ 30% of NAV;
  - $IM_t+q_{0.99}(VM_{t+1})\le$ unencumbered HQLA;
  - NAV-loan LTV ≤ 15% per fund and ≤ 5% of total NAV;
  - $\sum P+\sum U\le 0.80W$;
  - concentration and counterparty limits.
- **(C6) Payout rule:** $D_t\ge 0.05\bar W_t$, and top-ups above 5% only when $c_t\ge b^*$ (a de Finetti-type barrier). Optionally add a ratchet floor $D_t\ge(1-\rho)D_{t-1}$.

**Reported KPIs, not optimized:**
- P(10y ≥ 10%) and P(5y ≥ 10%);
- E-shortfall below 10%;
- median real NAV₁₀;
- P(real NAV₁₀ ≥ start);
- P(amber) and P(red) recourse;
- $\tau_{surv}$ fan;
- fragility κ.

**Mapping to the deck.** Tier 1 becomes the robust feasible set {C1–C6}. Tier 2 becomes max J over that set. Lexicographic ordering is replaced by ε-constraint sweeps that expose duals $\lambda_k$.

### 6.5 Setting the numbers

| Parameter | Default | IC sweep | Justification |
|---|---|---|---|
| ε_D (joint, 5y, minimum 5% payout, no red recourse) | **1%** (≈0.2%/yr) | 0.5–5% | Minimum payout behaves like senior debt to the sovereign. 0.2%/yr sits between Solvency II (0.5%/yr) and stricter bank-capital practice [P]. With 50k paths, relative standard error ≈ √((1−p)/(np)) ≈ 4.5% at p=1% [I]. |
| Planned-payout reliability, 12m | **97.5%** | 95–99% | Mirrors the FTK 97.5% ("once-in-40-year") solvency standard, which secondary sources describe as one-year. Top-ups are discretionary. |
| Survival horizon | **24 months** | 18–36 | MSCI shows four straight years of low distributions. A 24-month near-zero-distribution stress is severe but plausible. LCR's 30 days reflects deposit-run speed, and ADIC's outflows run at quarterly and annual speed [I]. |
| P(red recourse, 5y), worst variant | **≤1%** | 0.5–5% | Toy shows two orders of magnitude of separation between policies at nearly equal medians. |
| Real drawdown (α, β) | **30%, 5% over 10y** | 25–40%, 2.5–10% | If payout is computed on lagged or average NAV (Alaska-style), a 30% fall lifts the effective rate to d/0.7. A 5% minimum then becomes ~7.1%, above the ~6.8% sustainable at a 10% return, so the payout is no longer sustainable in expectation [I]. In Browne's (1997) terms, ruin has positive probability under every policy (the "danger zone") whenever the fixed payout exceeds what the riskless asset alone can fund, which is already true at 5% [unverified in Browne's own text: the MOR full text is paywalled; the c/r boundary comes from Bayraktar & Young's description of Browne (1997), arXiv:math/0703824]. [corrected 2026-10-18: was "The fund enters Browne's danger zone"; Browne's boundary is set by the riskless rate, so the 30% fall moves the fund deeper into the zone, not into it] |
| Robust floor | worst-model CVaR₉₀ of R¹⁰ ≥ **0%**; report robust median vs 7% | −2% to +3% | The 7%@95% floor is infeasible (§3.2d). In an i.i.d. lognormal model (μ=8.5%) this constraint binds at σ≈14.3% (CVaR₁₀ = +1.5% at σ=12%, −1.7% at σ=17%) [I]. |
| Target-shortfall exponent | α=**2** | 1–3 | α ≥ 1 is never risk-seeking below target (Fishburn). |
| γ (CRRA) | **3** | 2–5 | Fractional Kelly. Accounts for illiquidity-induced risk aversion (Ang et al.). |
| Target metric | 10y rolling geometric TWR, nominal | 5y secondary | Peer-comparable. A 3-year horizon is too noisy. |
| Leverage | ≤**1.3×** economic | 1.0–1.5× | Toy: 1.4× with a thin reserve gives 10–21% red-breach probability. |
| Ambiguity set 𝓜 | Base + PE-drought + stagflation + overlay-stress (+ Wasserstein radius on asset forecasts) | — | Robust satisficing / DRO (Mohajerin Esfahani & Kuhn 2018). |

**Use governance bands rather than single cut-offs [I].** Each constraint gets three nested levels:
- *capacity* (hard; e.g., ε=2%);
- *tolerance* (amber trigger; ε=1%);
- *appetite* (target operating zone; ε=0.5%).

Hysteresis between bands prevents chattering re-optimization, a standard device in control.

### 6.6 From the global optimizer to SELL / HOLD / REFINANCE / LEVER

- **Reduced cost (column-generation logic) [I].** Each candidate action j changes scenario cash flows and wealth. Its value is
  $$r_j=\Delta J_j-\sum_k\lambda_k\,\Delta g_{k,j}-c_j,$$
  where $g_k$ are the constraint functions of C1–C5, $\lambda_k$ their duals, and $c_j$ transaction cost or discount.
  - Approve if $r_j>0$ under every model variant and the safety filter passes.
  - Rank by $r_j$ per unit of irreversibility. SELL is irreversible; HOLD keeps the option; REFINANCE adds liquidity but also leverage and covenant risk; LEVER adds exposure.
  - Agents propose actions ("columns"). The deterministic master problem prices them.
- **Tail contributions [S/I].** CVaR is positively homogeneous, so Euler allocation (Tasche 2007) gives additive contributions $E[L_i\mid L\ge \mathrm{VaR}]$. An asset's contribution to the *deficit* CVaR in C1 is its liquidity-tail cost, and the IC can read it directly.
- **Return-track fusion → ambiguity [I].** Fuse underwritten, actual and forecast returns into $\hat P$ (handled by another stream). Use their *disagreement* to size asset-level ambiguity radii. Optimistic forecasts then cannot dominate decisions: the robust objective discounts them automatically. This also targets the memo-corpus blind spot that distribution timing was too optimistic.

### 6.7 The safety filter (real-time Tier 1)

Any proposed action (from the IC, an agent or the opportunistic desk) is projected onto the safe set [I, after Wabersich & Zeilinger; Ames et al.]:
$$a^{safe}_t=\arg\min_a\|a-a^{prop}_t\|_Q^2\ \ \text{s.t.}\ \ \hat g_k(s_t,a)\le-\delta_k\ \ \forall k.$$
$\hat g_k$ are linearized scenario surrogates of C1–C5 and $\delta_k$ are amber buffers. This is a small QP. The deviation $a^{prop}-a^{safe}$ is reported to the IC as "what the gate changed and why". Probabilistic safe-set reachability [S: Abate et al. 2008] gives the "probability of staying viable" KPI.

### 6.8 Presenting trade-offs to the IC

1. **Frontier A:** P(10y ≥ 10%) vs P(red recourse, 5y), worst variant.
   - Colour = payout d; marker = robust-feasible or not.
   - Annotate the marginal rate of substitution: pp of P(10%) per pp of breach.
2. **Frontier B:** robust floor (worst-model CVaR₉₀ of 10y return) vs P(10%).
3. **Sustainability frontier:** median real NAV₁₀ and P(real preservation) vs payout d, with iso-return curves from the identity.
4. **Liquidity panel:** survival-horizon fan, ADIC-LCR fan, and margin-coverage ratio, each drawn against its constraint line.
5. **Price-of-safety table** (duals): e.g., moving ε_D from 1% to 2.5% buys +x bp of expected log-growth and +y pp of P(10%).
6. **Fragility index** κ, plus a regret table across model variants.
7. **Decision cards** for each proposal: ΔJ, Δ constraint slack, $r_j$, fragility, reversibility, and the safety-filter adjustment.

All probabilities are shown as ranges across 𝓜 (e.g., "P(10%) = 37% [26–38%]") to make ambiguity visible (Hansen & Sargent 2001 [S]).

### 6.9 Avoiding target-chasing: enforceable rules

1. No indicator-of-target terms in J. Use α ≥ 1 shortfall terms only, plus concave utility.
2. **Monotonicity constraint:** leverage, risk budget and pacing must be non-decreasing in the cushion. In affine rules $L_t=L_0+k_c c_t+\dots$, require $k_c\ge0$.
3. Rolling horizon with a terminal value: no fixed deadlines.
4. Constraints must hold in every model variant, not just the base model.
5. **Gambling detector** (rubric for the challenge agent) flags any of:
   - risk rising after losses;
   - a bimodal or digital-like terminal distribution;
   - P(10%) rising while the median is flat and CVaR worsens (policy C vs B).
6. Pre-commitment: (ε, α_DD, β_DD, L_max, payout rule) are set by the IC per cycle. Overrides are logged with rationale.

### 6.10 Calibration targets and data needs

- **Calibration:**
  - PE distribution rate 10–15% base with multi-year persistence; 20–27% only in recovery states (MSCI).
  - Endowment 10y return 7.7% and $5bn+ FY25 11.8% as outcome sanity checks.
  - CMA anchors: PE 10.2%, global equities 7.0%, IG 5.2% (JPM 2026).
  - Payout identity: d* ≈ 6.8% at 10% and 2.5% inflation.
  - Secondary discounts by regime.
  - Survival under 2025-type stress (Harvard pattern).
- **Data:**
  - fund-level cash-flow histories (calls, distributions, NAV) and unfunded by vintage;
  - the three return tracks per asset;
  - NAV-loan and facility terms;
  - CSA/IM models and VM history;
  - tail-hedge payoff grids;
  - opportunistic P&L;
  - the owner's payout rule and history (and any correlation with the owner's revenues);
  - inflation;
  - regime indicators.

---

## 7. Implementation notes

- **Stack (present in the project venv):** numpy/scipy/pandas/statsmodels, numba, hmmlearn, arch, cvxpy 1.9.3 with Clarabel/ECOS/HiGHS/OSQP. Power-cone CRRA and SOC shortfall norms are native to cvxpy with Clarabel. CVaR constraints are LP rows.
- **Three-layer solution approach [I]:**
  - **L1, policy search (primary).** Parametric decision rules: reserve ratio, cushion-linked leverage, pacing, hedge ratio, payout barrier. Evaluate on 50k simulated quarterly paths under each variant, with common random numbers. Constraints use sample-average CVaR. Optimize by convex surrogates where wealth is affine in θ, else by derivative-free search with constraint penalties.
  - **L2, scenario LP/SOCP (for duals and frontiers).** A reduced tree (3–4 stages × 10–20 branches, or 5–10k paths with affine recourse). Run ε-constraint sweeps in parallel and extract $\lambda_k$ for §6.6. Size check: S=10⁴ scenarios × 20 periods with affine rules (θ ~ 10²–10³) gives ~2×10⁵ CVaR rows, which is tractable for HiGHS or Clarabel.
  - **L3, low-dimensional DP diagnostics.** State (cushion, regime), Das-style grid DP, used to reveal policy shape and detect gambling regions.
  - Risk-averse SDDP with nested CVaR (Philpott & de Matos) is optional for full time-consistency. It assumes stagewise independence, which conflicts with regime persistence unless the regime is added to the state.
- **Numerical pitfalls:**
  - **Rare-event estimation.** 0.2%/yr needs ≥50k paths, or importance sampling via tilted drawdown regimes.
  - **Scenario-approach sample sizes** (§2.3).
  - **Overflow.** $G^{-8.4}$ overflows when G is small; evaluate via log-sum-exp.
  - **CVaR LP degeneracy.** Use a small ridge.
  - **PE smoothing** understates volatility. De-smooth before risk calculations.
  - **Path dependence** (smoothing windows, ratchets) requires state augmentation.
  - **Integer tickets** for SELL turn the problem into a MILP; relax, then round with a repair step.
  - **Price impact.** Convex discounts keep convexity; fixed haircuts with thresholds do not.
  - **Optimizer's curse.** Validate frontiers out of sample and on unseen variants.
  - **Monte Carlo noise.** Use common random numbers across policies, as in the toy.
- **Interface for the agentic layer [I].** The optimizer emits a typed "objective report": J, constraint values and slacks, duals, robust ranges, fragility κ, gambling flags. Rubric checks follow the Agentic-Scientist pattern:
  - monotonicity of P(10%) and breach probability in leverage;
  - agreement of the union bound with joint estimates;
  - stability of results under seed changes.
  LLM agents may propose actions and scenarios. They may not change IC-owned parameters.
- **Illustrative scripts** (session scratchpad, not part of the repo; seeded and reproducible):
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\s11\tools\s11_attainable.py`
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\s11\tools\s11_gbwm_dp.py`
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\s11\tools\s11_toy_alm.py`
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\s11\tools\s11_toy_summary.py`

---

## 8. Risks, pitfalls & limitations

- **Model risk dominates probability statements.** A "99%" is only as good as 𝓜. Always report worst-variant values and ranges. The toy shows stagflation doubling hard-breach rates.
- **Surrogate conservatism.** CVaR and the risk-constrained-Kelly bound are conservative. Over-tight surrogates can make the feasible set look empty. Calibrate surrogate levels so that *simulated* probabilities meet the targets.
- **Lexicographic boundary-hugging.** Without buffers, solutions sit on the constraint edge and churn. Use bands and hysteresis.
- **Owner behavior.** If the owner's demand is state-dependent (fiscal stress), modelling it as a fixed percentage underestimates wrong-way risk.
- **Smoothed marks** make P(breach) and drawdown look safer than they are, and shift timing of the denominator effect.
- **Measurement confusion.** Mixing TWR (gross), NAV growth (net), nominal and real terms in one dashboard misleads. Label every metric.
- **Behavioral.** IC framing around "on track for 10%" can reintroduce gambling even if the optimizer does not.
- **Toy limitations.** No fees, taxes or FX; stylized PE dynamics; annual steps; a single equity factor; tail hedge priced heuristically. Its numbers illustrate *shapes*, not ADIC levels.
- **Verification gaps.** Some seed references could not be verified in-session (§10 log). None is load-bearing.

## 9. Open questions

1. Is the 5% minimum a hard legal or fiscal obligation, or a soft norm? Who chooses within 5–10%, and on what NAV basis (current, lagged, averaged)?
2. Is owner demand correlated with the owner's other revenues (e.g., commodity cycles)? Can ADIC defer payouts or receive injections?
3. Which recourse counts as a "breach": liquid sales in drawdowns, facility use, PE secondaries above X% discount, NAV loans?
4. Borrowing capacity and constraints: sovereign/rating considerations, covenant appetite for NAV loans at fund and portfolio level.
5. Is the 10% target meant as TWR (gross) or as NAV growth (net)? Over which horizon will the owner judge it?
6. Tail-hedge monetization rules and collateral mechanics: does hedge P&L arrive as cash in stress, and how fast?
7. Ambiguity set: which variants does the IC accept as "plausible"? How should Wasserstein radii be set per asset from return-track disagreement?
8. What parameter-change cadence (annual or triennial) balances pre-commitment with adaptivity?

---

## 10. References

*Verification status: (✓) = page or metadata read in-session; (meta) = bibliographic metadata only; (⚠) = not verified, not relied upon.*

**Goal attainment, floors, behavior**
- Browne, S. (1999). Reaching goals by a deadline: digital options and continuous-time active portfolio management. *Advances in Applied Probability* 31(2):551–577. https://doi.org/10.1239/aap/1029955147 (✓ abstract)
- Browne, S. (1999). Beating a moving target: optimal portfolio strategies for outperforming a stochastic benchmark. *Finance and Stochastics* 3:275–294. https://drupalgsb-test.paas.cc.columbia.edu/sites/default/files-efs/pubfiles/839/finasto_sb.pdf (✓)
- Browne, S. (1997). Survival and growth with a liability: optimal portfolio strategies in continuous time. *Mathematics of Operations Research* 22(2):468–493. https://doi.org/10.1287/moor.22.2.468 (✓ meta+abstract)
- Nielsen, M. (2013). The Kelly growth optimal strategy with a stop-loss rule. arXiv:1311.2550. https://arxiv.org/abs/1311.2550 (✓)
- Das, S., Ostrov, D., Radhakrishnan, A., Srivastav, D. (2020). Dynamic portfolio allocation in goals-based wealth management. *Computational Management Science* 17(4):613–640 (online 2019). https://doi.org/10.1007/s10287-019-00351-7 (meta); SSRN 3211951 (2018); MathWorks implementation: https://www.mathworks.com/help/finance/dynamic-portfolio-allocation-in-gbwm-for-multiple-periods.html (✓).
- Das, S., Markowitz, H., Scheid, J., Statman, M. (2010). Portfolio optimization with mental accounts. *JFQA* 45(2):311–334. https://ideas.repec.org/a/cup/jfinqa/v45y2010i02p311-334_00.html (✓)
- Föllmer, H., Leukert, P. (1999). Quantile hedging. *Finance and Stochastics* 3(3):251–273. https://doi.org/10.1007/s007800050062 ; https://ideas.repec.org/a/spr/finsto/v3y1999i3p251-273.html (✓)
- Föllmer, H., Leukert, P. (2000). Efficient hedging: cost versus shortfall risk. *Finance and Stochastics* 4(2):117–146. https://doi.org/10.1007/s007800050008 (meta); author preprint https://www2.mathematik.hu-berlin.de/~foellmer/papers/hedges_57.pdf (✓ preprint)
- Basak, S., Shapiro, A. (2001). Value-at-risk-based risk management: optimal policies and asset prices. *Review of Financial Studies* 14(2):371–405. https://ideas.repec.org/a/oup/rfinst/v14y2001i2p371-405.html (✓)
- Fishburn, P.C. (1977). Mean-risk analysis with risk associated with below-target returns. *AER* 67(2):116–126. https://ideas.repec.org/a/aea/aecrev/v67y1977i2p116-26.html (meta)
- Kahneman, D., Tversky, A. (1979). Prospect theory. *Econometrica* 47(2):263–291. https://doi.org/10.2307/1914185 (meta)
- Dybvig, P.H. (1995). Dusenberry's ratcheting of consumption. *Review of Economic Studies* 62(2):287–313. https://ideas.repec.org/a/oup/restud/v62y1995i2p287-313..html (✓ abstract)
- Dybvig, P.H. (1999). Using asset allocation to protect spending. *Financial Analysts Journal* 55(1):49–62; draft: https://phildybvig.com/research/papers/ratchet2p.pdf (✓)
- Grossman, S., Zhou, Z. (1993). Optimal investment strategies for controlling drawdowns. *Mathematical Finance* 3(3):241–276. https://ideas.repec.org/a/bla/mathfi/v3y1993i3p241-276.html (✓)
- Constantinides, G. (1990). Habit formation: a resolution of the equity premium puzzle. *JPE* 98(3):519–543. https://ideas.repec.org/a/ucp/jpolec/v98y1990i3p519-43.html (✓)
- Cvitanić, J., Karatzas, I. (1995). On portfolio optimization under "drawdown" constraints (⚠). Brunel, J., *Goals-Based Wealth Management* (⚠).

**Risk measures, chance constraints, robustness, time consistency**
- Artzner, P., Delbaen, F., Eber, J.-M., Heath, D. (1999). Coherent measures of risk. *Mathematical Finance* 9(3):203–228. https://doi.org/10.1111/1467-9965.00068 (meta)
- Rockafellar, R.T., Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk* 2(3):21–41. https://doi.org/10.21314/jor.2000.038 (meta); draft https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf (✓)
- Rockafellar, R.T., Uryasev, S. (2002). Conditional value-at-risk for general loss distributions. *JBF* 26(7):1443–1471. https://doi.org/10.1016/S0378-4266(02)00271-6 (meta)
- Charnes, A., Cooper, W.W. (1959). Chance-constrained programming. *Management Science* 6(1):73–79. https://doi.org/10.1287/mnsc.6.1.73 (meta)
- Roy, A.D. (1952). Safety first and the holding of assets. *Econometrica* 20(3):431–449. https://doi.org/10.2307/1907413 (meta)
- Leibowitz, M., Henriksson, R. (1989). Portfolio optimization with shortfall constraints. *FAJ* 45(2):34–41. https://doi.org/10.2469/faj.v45.n2.34 (meta)
- Nemirovski, A., Shapiro, A. (2006/07). Convex approximations of chance constrained programs. *SIAM J. Optim.* 17(4):969–996. https://doi.org/10.1137/050622328 (meta+abstract)
- Calafiore, G., Campi, M. (2006). The scenario approach to robust control design. *IEEE TAC* 51(5):742–753. https://doi.org/10.1109/TAC.2006.875041 (meta)
- Campi, M., Garatti, S. (2008). The exact feasibility of randomized solutions of uncertain convex programs. *SIAM J. Optim.* 19(3):1211–1230. https://doi.org/10.1137/07069821X (meta+abstract)
- Chekhlov, A., Uryasev, S., Zabarankin, M. (2005). Drawdown measure in portfolio optimization. *IJTAF* 8(1):13–58. https://ideas.repec.org/a/wsi/ijtafx/v08y2005i01ns0219024905002767.html (✓)
- Busseti, E., Ryu, E., Boyd, S. (2016). Risk-constrained Kelly gambling. *The Journal of Investing* 25(3):118–134. https://doi.org/10.3905/joi.2016.25.3.118 (meta); preprint arXiv:1603.06183. https://arxiv.org/abs/1603.06183 (✓)
- Kelly, J.L. (1956). A new interpretation of information rate. *Bell System Technical Journal* 35(4):917–926. https://doi.org/10.1002/j.1538-7305.1956.tb03809.x (meta)
- Brown, D., Sim, M. (2009). Satisficing measures for analysis of risky positions. *Management Science* 55(1):71–84. https://ideas.repec.org/a/inm/ormnsc/v55y2009i1p71-84.html (✓)
- Chen, W., Sim, M. (2009). Goal-driven optimization. *Operations Research* 57(2):342–357. https://ideas.repec.org/a/inm/oropre/v57y2009i2p342-357.html (✓)
- Long, D.Z., Sim, M., Zhou, M. (2023). Robust satisficing. *Operations Research* 71(1):61–82. https://doi.org/10.1287/opre.2021.2238 ; preprint https://iora.nus.edu.sg/wp-content/uploads/2022/02/SSRN-id3478930.pdf (✓)
- Mohajerin Esfahani, P., Kuhn, D. (2018). Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. *Mathematical Programming* 171(1–2):115–166. https://doi.org/10.1007/s10107-017-1172-1 (meta); arXiv:1505.05116. https://arxiv.org/abs/1505.05116 (✓)
- Glasserman, P., Xu, X. (2014). Robust risk measurement and model risk. *Quantitative Finance* 14(1):29–58. https://doi.org/10.1080/14697688.2013.822989 (meta)
- Hansen, L.P., Sargent, T. (2001). Robust control and model uncertainty. *AER* 91(2):60–66. https://doi.org/10.1257/aer.91.2.60 (meta)
- Shapiro, A. (2009). On a time consistency concept in risk averse multistage stochastic programming. *Operations Research Letters* 37(3):143–147. https://doi.org/10.1016/j.orl.2009.02.005 (meta)
- Ruszczyński, A., Shapiro, A. (2006). Conditional risk mappings. *Math. of OR* 31(3):544–561. https://doi.org/10.1287/moor.1060.0204 (meta)
- Ruszczyński, A. (2010). Risk-averse dynamic programming for Markov decision processes. *Math. Programming* 125(2):235–261. https://doi.org/10.1007/s10107-010-0393-3 (meta)
- Pereira, M., Pinto, L. (1991). Multi-stage stochastic optimization applied to energy planning. *Math. Programming* 52:359–375. https://doi.org/10.1007/BF01582895 (meta)
- Philpott, A., de Matos, V. (2012). Dynamic sampling algorithms for multi-stage stochastic programs with risk aversion. *EJOR* 218(2):470–483. https://doi.org/10.1016/j.ejor.2011.10.056 (meta)
- Boyd, S. et al. (2017). Multi-period trading via convex optimization. *Foundations and Trends in Optimization* 3(1):1–76. https://doi.org/10.1561/2400000023 (meta); preprint arXiv:1705.00109. https://arxiv.org/abs/1705.00109 (✓)
- Tasche, D. (2007). Capital allocation to business units and sub-portfolios: the Euler principle. arXiv:0708.2542. https://arxiv.org/abs/0708.2542 (✓)

**Control, actuarial, endowment economics, illiquidity**
- Wabersich, K., Zeilinger, M. (2018/21). A predictive safety filter for learning-based control of constrained nonlinear dynamical systems. arXiv:1812.05506. https://arxiv.org/abs/1812.05506 (✓)
- Ames, A. et al. (2019). Control barrier functions: theory and applications. arXiv:1903.11199. https://arxiv.org/abs/1903.11199 (✓)
- Abate, A., Prandini, M., Lygeros, J., Sastry, S. (2008). Probabilistic reachability and safety for controlled discrete time stochastic hybrid systems. *Automatica* 44(11):2724–2734. https://doi.org/10.1016/j.automatica.2008.03.027 (meta)
- Gerber, H., Shiu, E. (1998). On the time value of ruin. *NAAJ* 2(1):48–72. https://doi.org/10.1080/10920277.1998.10595671 (meta)
- Avanzi, B. (2009). Strategies for dividend distribution: a review. *NAAJ* 13(2):217–251. https://doi.org/10.1080/10920277.2009.10597549 (meta)
- Tobin, J. (1974). What is permanent endowment income? *AER* 64(2):427–432. https://ideas.repec.org/a/aea/aecrev/v64y1974i2p427-32.html (meta)
- Merton, R.C. (1993). Optimal investment strategies for university endowment funds. In Clotfelter & Rothschild (eds.), *Studies of Supply and Demand in Higher Education*, U. Chicago Press. https://www.nber.org/books-and-chapters/studies-supply-and-demand-higher-education/optimal-investment-strategies-university-endowment-funds (✓)
- Brown, J., Dimmock, S., Kang, J.-K., Weisbenner, S. (2014). How university endowments respond to financial market shocks. *AER* 104(3):931–962. https://www.aeaweb.org/articles?id=10.1257/aer.104.3.931 (✓)
- Ang, A., Papanikolaou, D., Westerfield, M. (2014). Portfolio choice with illiquid assets. *Management Science* 60(11):2737–2761. https://doi.org/10.1287/mnsc.2014.1986 (meta); NBER w19436. https://www.nber.org/papers/w19436 (✓)
- Gourier, E., Phalippou, L., Westerfield, M. (2024). Capital commitment. *Journal of Finance* 79(5):3407–3457. https://doi.org/10.1111/jofi.13382 (meta+abstract)

**Market data, peers, regulation (dated)**
- MSCI (2026-06-11). The distribution drought in private equity persists. https://www.msci.com/data-and-analytics/private-asset-solutions/visualizations/the-distribution-drought-in-private-equity-persists (✓)
- MSCI (2026-10-13). The best exit pricing in a decade, and LPs are still waiting for cash. https://www.msci.com/data-and-analytics/private-asset-solutions/visualizations/the-best-exit-pricing-in-a-decade-and-lps-are-still-waiting-for-cash (✓)
- ai-CIO (2026-02-12). University endowments report average 10.9% return (NACUBO-Commonfund FY2025). https://www.ai-cio.com/news/turbulent-year-university-endowments-report-average-return/ (✓)
- TIFF (2026-02-17). FY2025 NACUBO results. https://www.tiff.org/fy2025-nacubo-results-show-strong-returns-but-rising-pressures-on-institutions-budgets/ (✓)
- Yale News (2025-10-24). Yale reports investment return for fiscal 2025. https://news.yale.edu/2025/10/24/yale-reports-investment-return-fiscal-2025 (✓); Yale endowment overview (spending rule): https://www.yale.edu/funding-yale-home/overview-yales-endowment (✓)
- J.P. Morgan AM (2025-10-20). 2026 Long-Term Capital Market Assumptions press release. https://am.jpmorgan.com/us/en/asset-management/adv/about-us/media/press-releases/jp-morgan-releases-2026-long-term-capital-market-assumptions/ (✓)
- The Harvard Crimson (Apr 2025). Harvard private equity stake sales. https://www.thecrimson.com/article/2025/4/25/private-equity-stake-sales/ (✓)
- APFC. The Fund (POMV). https://apfc.org/the-fund/ (✓); NBIM. About the fund. https://www.nbim.no/en/the-fund/about-the-fund/ (✓)
- Directive 2009/138/EC (Solvency II), Art. 101. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32009L0138 (✓)
- BCBS (2013). Basel III: The Liquidity Coverage Ratio. https://www.bis.org/publ/bcbs238.htm (✓)
- IPE (2004-10-25). Dutch regulator unveils supervisory framework. https://ipe.com/dutch-regulator-unveils-supervisory-framework/9992.article (✓); DNB (2026-07-28). Pension fund funding ratios 2026Q2. https://www.dnb.nl/en/general-news/news-2026/pension-transition-and-pension-fund-funding-ratios-2026q2/ (✓)
- Center for Retirement Research (2024). Canada Pension Plan falls short of indexed benchmark. https://crr.bc.edu/canada-pension-plan-fall-short-of-indexed-benchmark/ (✓)
- Lange, R.T. et al. (2026). The Agentic Scientist. arXiv:2610.18933 (from project context; not re-fetched).

---

## Citation corrections (2026-10-18)

*Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.5; `research/literature/11_objectives.lit.md` §1–2; `research/literature/recheck/11_objectives.recheck.md`. Added volume, issue, page and DOI data were checked against Crossref on 2026-10-18.*

- §2.1: the "follow-up" to quantile hedging is now cited as Föllmer & Leukert (2000), *efficient hedging*, which is added to §10.
- §2.3: the scenario-approach formula is now credited as "(Calafiore & Campi 2006), with the exact bound of Campi & Garatti (2008, Thm 2.4)".
- §2.3: a β column (10⁻⁶) is added to the N table. Recomputation confirms that 3,260 / 9,086 / 27,418 / 1,801 are the exact minimal N at β = 10⁻⁶.
- §2.6: the Avanzi/de Finetti bullets are reworded. The de Finetti criterion controls ruin only with an added ruin constraint or penalty (Gerber–Shiu). The protected minimum is marked as ADIC's adaptation. Ratcheting is sourced to Dybvig (1995).
- §6.5 "Real drawdown" row: the Browne (1997) "danger zone" sentence is reworded. Browne's boundary is set by the riskless rate (c/r), so a fixed 5% payout is already inside the zone at the 3.5% cash rate. Marked [unverified in Browne's own text].
- §6.5 "Ambiguity set" row: "Esfahani & Kuhn 2018" now reads "Mohajerin Esfahani & Kuhn 2018".
- §10 Das et al.: the ⚠ is replaced by *Computational Management Science* 17(4):613–640 (2020), DOI 10.1007/s10287-019-00351-7.
- §10 Föllmer & Leukert (1999): DOI 10.1007/s007800050062 added.
- §10: missing entry added for Föllmer & Leukert (2000), *Efficient hedging: cost versus shortfall risk*, *F&S* 4(2):117–146, DOI 10.1007/s007800050008.
- §10 Rockafellar & Uryasev (2000): "journal details from memory" is replaced by 2(3):21–41 and DOI 10.21314/jor.2000.038.
- §10 Busseti, Ryu & Boyd (2016): journal version added, *The Journal of Investing* 25(3):118–134, DOI 10.3905/joi.2016.25.3.118.
- §10 Mohajerin Esfahani & Kuhn (2018): surname corrected; full title, issue (1–2) and DOI 10.1007/s10107-017-1172-1 added.
- §10 Boyd et al. (2017): journal version added, *Foundations and Trends in Optimization* 3(1):1–76, DOI 10.1561/2400000023.
- §10 Ang, Papanikolaou & Westerfield (2014): volume, pages and DOI added, 60(11):2737–2761, DOI 10.1287/mnsc.2014.1986.
