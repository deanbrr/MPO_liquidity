# Dossier 02: Endowment Model, Distribution Policy, SWF Peer Practice and the Total Portfolio Approach

**Project:** ADIC multi-period robust TPA framework (agentic) · **Stream:** 02 · **As of:** 18 Oct 2026 · **Audience:** design/architecture stage, quant team, IC secretariat

**Evidence tags:**
- **[S]** sourced fact, with a citation in §10.
- **[P]** practitioner consensus.
- **[I]** our own inference or calculation.
- **[I-MC]** results from our own Monte Carlo, specified in §3.3. These are stylized and assumption-driven. They are not forecasts.

Seed references in the brief were checked before use. Anything we could not check in-session is flagged "(unverified)". A shared session cap on web searches cut off searching partway through this stream. Several peer details therefore come from primary pages fetched directly, and a few are flagged as unverified.

---

## 1. Executive summary

1. **The 10% target only works as a gross, pre-distribution nominal total return.** [I]
   - **Net reading fails.** Taking it as "NAV grows 10% after distributions" requires gross returns of 15.8% / 18.9% / 22.2% at payouts of 5% / 7.5% / 10% of opening NAV, since $(1+R)=1.10/(1-d)$. No peer comes close: 20-year records run from 5.6% (GIC, USD nominal) to about 10% (NZ Super) [S].
   - **Gross reading.** Real NAV is preserved only if $d \le d^* = 1-(1+\pi)/(1+g)$, where $g$ is the geometric return. With $\pi=2.5\%$:
     - $d^*\approx 6.8\%$ if 10% is the geometric return;
     - $d^*\approx 6.2$–$6.3\%$ if 10% is the arithmetic mean at 12% volatility;
     - $d^*\approx 4.5\%$ at a peer-realistic 7.4% geometric return.
   - **So the mandated 5–10% band straddles sustainability.** The lower half preserves real NAV. The upper half is planned real decumulation.

2. **Hitting 10% is a coin-flip at best.** [I-MC]
   - If the expected arithmetic return is exactly 10% at 12% volatility, P(20-year annualized return ≥10%) is only **42%**. At an 8% expected return it is **17%**.
   - **Payout of 7.5% of current NAV:**
     - median real NAV after 20 years is **0.78×** if the target is met in expectation, with P(real erosion) 69%;
     - median real NAV is **0.53×** under peer-realistic returns, with P(erosion) 89% and P(halving) 45%.
   - The IC should see these as probabilities, not as a single "10%" headline.

3. **Rule design is a four-way trade-off, not a free lunch.** The four dimensions are cumulative distributions, terminal real NAV and its tails, distribution stability, and *liquidity stress*. [I-MC]
   - **Fixed % of current NAV.** Terminal NAV is path-independent and gives the best liquidity behaviour. Payouts are volatile: real distribution growth has an SD of about 11% a year, and P(some year with a >10% real cut) is 88–98%.
   - **Smoothing (Yale-type, Alaska POMV).** Payouts are about 3× smoother for the same cumulative payout. The price is sequence risk, a fatter NAV left tail and a **higher probability of forced secondary sales**. In our base liquidity case at a 7.5% target, that probability is 15.6% versus 4.8% for fixed %.
   - **Fixed real amounts.** These deplete the fund below 5% of starting NAV in 31–52% of 20-year paths, and in 70% of paths in the low-return case. Reject.
   - **No-decline ratchets.** These are infeasible at 5–10% payouts: Dybvig shows perpetual protection needs payout ≤ the real riskless rate [S].

4. **Distribution policy and private-markets pacing are one problem.** [I-MC]
   - **The cash gap.** With ~60% private and PE distributions at about 14% of NAV, the lowest rate since 2008–09 per Bain [S], a 7.5% payout (≈US$13bn a year) exceeds net private cash flow under plausible capital calls. The liquid book fills the gap and the private share ratchets up.
   - **Forced-sale probabilities.** In our stylized two-bucket model with a 25% liquidity floor, P(forced secondary sale within 10 years) is:
     - ≈5% at a 7.5% payout in the base case;
     - ≈60% under a DPI drought (10% distribution yield);
     - 100% at a 10% payout in a drought.

5. **Owner demand is wrong-way risk.** [S]/[I]
   - **US endowments cut payouts** after shocks and do not raise them after gains ("endowment hoarding", Brown et al. 2014) [S].
   - **A sovereign owner's need rises** when oil and risk assets fall. Kuwait in 2020: the Treasury had about KD2bn of liquidity, roughly one month's General Reserve Fund (GRF) drawdown, and the automatic 10% transfer to the Future Generations Fund (FGF) was removed [S].
   - **Model it as stochastic, regime-correlated exogenous demand.**

6. **How to model ADIC's requirement: a three-layer hybrid.** [I]
   - **(i) Strategic layer.** Policy parameters θ: target rate $r^*$, smoothing λ, funded-ratio feedback κ, NAV basis, and the size of the liquidity reserve. Choose them by *simulation-based policy search* across robust scenario sets.
   - **(ii) Exogenous layer.** Owner-demand shocks inside the 5–10% band, correlated with oil, the market regime and the fiscal state.
   - **(iii) Recourse layer.** Annual discretionary choice within the band, used only where the mandate gives ADIC discretion.
   - **Shadow prices.** Report the shadow price of the 5% floor and the 10% cap as the "value of mandate flexibility". Dimmock–Wang–Yang find that a 5.2% minimum-spending constraint costs about 2% of certainty-equivalent wealth and cuts the optimal illiquid allocation from 34.5% to 27.8% [S].

7. **Peer practice to adopt** [S]/[P]:
   - a board-owned reference portfolio plus a risk budget (NZ Super, CPP "market risk targets", GIC's 2026 Strategic Portfolio);
   - total-fund leverage as a "balance sheet risk stabiliser", gated by multi-horizon liquidity coverage ratios (CPP);
   - competition for capital and cost-of-capital hurdles (TPA);
   - **spending from *expected*, not realized, returns** (Norway's 3% real rule; Singapore's ≤50% of expected long-term real returns);
   - multi-year NAV averaging (Alaska POMV) and explicit floor/cap bands (Yale 4.0–6.5%).

   **Peer practice to avoid:**
   - importing Norway's rule wholesale, since NBIM is overwhelmingly liquid (unlisted real estate ≤7%, unlisted infrastructure ≤2% [S]);
   - fixed-amount fiscal claims;
   - asset-class quotas;
   - treating promotional TPA performance claims (adopters "+1.3% p.a." [S]) as causal evidence.

---

## 2. Core concepts and theory

### 2.1 Intergenerational equity and the sustainable payout

Tobin (1974, *AER* 64(2)) framed endowment trustees as guardians of the future against the claims of the present [S]. The operational form is real-value preservation. Let $W_t$ be NAV, $D_t=d_tW_t$ distributions paid at the start of year $t$, and $R_{t+1}$ the nominal return:

$$W_{t+1}=(W_t-D_t)(1+R_{t+1}),\qquad \frac{W_T}{W_0}=\prod_{t=0}^{T-1}(1-d_t)(1+R_{t+1}).$$

Real preservation in the median requires $d\le d^*=1-(1+\pi)/(1+g)$, where $g$ is the median geometric return. Two consequences matter for ADIC [I]:

- **Constant payout removes sequence risk.** With a constant percentage of *current* NAV, terminal wealth is a commutative product: return ordering does not matter. Sequence risk comes back only through smoothing, lags, fixed amounts or ratchets (§3.2).
- **Volatility drag is first-order.** $g\approx\mu-\sigma^2/2$, so drag is 0.72pp at 12% volatility and 1.28pp at 16%. Desmoothed volatility matters, because about 60% of ADIC's NAV is appraisal-based.

### 2.2 Merton (1993): the endowment as part of total resources

Merton (NBER WP 3820, 1991; chapter in Clotfelter & Rothschild, eds., 1993) argues that treating the endowment as the institution's only asset produces near-identical advice for every school [S]. Spending and investment rules should reflect total resources and objectives, and the endowment can hedge unexpected changes in the costs of the activities it funds [S].

**ADIC transfer [I].** The relevant balance sheet is the *sovereign owner's*: hydrocarbon revenue, other sovereign funds and the fiscal budget. Distribution demand is a function of the owner's other income. Oil-revenue shocks and global risk assets are positively correlated in recession states. ADIC's payout demand therefore has the *opposite* sign of the hedge Merton recommends, which is why wrong-way demand must be modelled explicitly.

### 2.3 Dybvig: protecting spending (ratchets)

Dybvig (1995, *RES*; 1999, *FAJ* 55(1):49–62) derives the no-decline policy [S]:

- Hold $s_t/r$ (perpetual current spending at the riskless rate $r$) in the safe asset.
- Invest $K(W_t-s_t/r)$ in risky assets.
- Raise spending only as needed to keep $s_t\ge \underline r\,W_t$.

Dybvig's own example: with a 5% riskless rate, the most a $100m fund can commit in perpetuity is $5m a year [S]. Allowing spending to fall 5% a year permits a higher starting rate, but the protection "is not worth much" [S].

**ADIC implication [I].** A non-declining distribution at 5–10% of NAV is infeasible when real riskless rates are about 1–2%. What *is* feasible is protecting a finite horizon: a distribution reserve covering 18–36 months, in the style of a bank liquidity buffer.

### 2.4 Dimmock, Wang & Yang (DWY): illiquidity, spending and alternatives

DWY (*Management Science* 70(3):1554–1579, 2024; NBER WP 25559) solve a Merton-style problem with these features [S]:
- an illiquid alternative with lock-ups, natural liquidity events and proportional secondary-sale costs;
- unspanned risk;
- Epstein–Zin preferences.

The numbers below are from the NBER version (rev. 2022) and may differ slightly in print [S]:

- **Calibration.** Risk aversion γ=2, EIS 0.5, risk-free 4%, unspanned volatility ε=15%, correlation 0.625, payout yield 4%.
- **Alpha drives the allocation.** With α=2% net, the optimal allocation is 53.9% public equity, 11.6% bonds and 34.5% alternatives, with a no-trade band of [27.5%, 64.9%] and target spending of 5.32%. At α=1% alternatives fall to 12.7%. At α=3% they rise to 60.2% (band [51.0%, 88.5%]).
- **The minimum-spending constraint bites.** A 5.2% minimum barely changes desired spending (5.32%→5.30%) but cuts alternatives from 34.5% to 27.8% and costs about 2% of certainty-equivalent wealth. The paper notes that even if the constraint "rarely binds", the states where it binds are high-alternatives states.
- **Crisis states.** Higher calls, lower distributions and a liquidation cost of 25% versus 10% in normal times cause large deviations from targets.
- **Borrowing.** The model allows borrowing against liquidation value, but "borrowing is rare".

**ADIC implication [I].** A ~60% private allocation plus a hard 5% distribution floor is consistent with DWY only if private alpha is ≥ about 3% net and liquidity diversification is strong (staggered vintages, secondaries capacity). The framework must price the floor as a constraint with a shadow price.

### 2.5 Gilbert & Hrdlicka (2015) and Campbell (2012): flexibility and buffers

Gilbert & Hrdlicka (*RFS*, doi:10.1093/rfs/hhv031) model the university jointly choosing internal projects and endowment size and risk [S]:
- payout constraints such as the 7% UPMIFA presumption remove internal investment options, push institutions toward large, risky endowments and stop the endowment working as a buffer stock;
- "universities need cash in recessions just as everyone else does" (white paper) [S].

Campbell (Forum Futures 2012; slides 2011) sets out the tension between *immortality*, spending no more than the real return, and *vigor*, spending enough to matter (about 5%) [S]. He concludes that institutions need flexibility to cope with downturns and that diversification fails in global shocks [S].

### 2.6 Behaviour after shocks, and the performance critique

Brown, Dimmock, Kang & Weisbenner (*AER* 104(3):931–62, 2014) find that endowments cut payouts *below* stated policy after negative shocks but do not raise them after positive shocks [S]. They call this "endowment hoarding"; it is strongest near the benchmark set at a president's arrival, and the cuts reach operations, including staff [S].

**For ADIC [I]:**
- rules should be pre-committed, because discretion is asymmetric and procyclical;
- the asymmetry runs the other way for a sovereign, whose owner demands *more* after shocks.

Ennis (2021a) finds alphas of −1.1% to −1.8% (t-stats −2.7 to −4.9) for six fund-size cohorts of endowments over the 11 fiscal years to June 2019. Of the 43 largest endowments, none outperformed with statistical significance and one in four underperformed with statistical significance. He puts costs at 1–2% of assets [S]. A later Ennis paper reports negative excess returns of 1.87% versus passive for endowments of more than $1bn over the 12 years to June 2020; the source does not say whether the figure is annualized (Ennis 2021b; attribution inferred, see §10) [S]. [corrected 2026-10-18: the alpha range belongs to size cohorts, not to the 43 endowments; the −1.87% comes from a separate 2021 paper and is not stated as a yearly figure.] **Implication [I]:** the "endowment-model premium" should enter as an uncertain prior with a wide band, not as a constant. Cejnek, Franz, Randl & Stoughton (*JOIM* 12(3):90–117, 2014) conclude that governance and the asset-allocation/spending link are the least developed areas of the literature [S].

### 2.7 Cross-disciplinary lenses that transfer directly

- **Insurance dividend theory** (de Finetti 1957; the original is not indexed, so its title and venue come from a citing reference, see §10). Maximizing discounted dividends subject to ruin gives a *barrier* policy: pay out surplus above a reserve level. This is the template for funded-ratio rules (§3.1, R9/R12).
- **Actuarial funding** (Dufresne 1988; Owadally & Haberman 1999, 2004). Spreading gains and losses in pension contributions creates an efficient frontier between contribution volatility and fund volatility. This is the same frontier endowment smoothing trades along, and the amortization period maps to the smoothing half-life.
- **Control theory.** A Yale-type rule is a first-order low-pass filter, with half-life $h=\ln 0.5/\ln\lambda$: 1.9 years at λ=0.7, 3.1 at λ=0.8 and 6.6 at λ=0.9 [I]. Minimizing a quadratic cost on payout changes and funded-ratio deviations gives a *linear state-feedback* rule in $(D_{t-1},F_t)$. That is exactly the R12 family below [I]. It holds after linearization; with multiplicative return noise the gains come from a modified Riccati equation.
- **Public-finance fiscal rules.**
  - Norway and Singapore spend from *expected* real returns, not realized returns, which smooths political demand [S].
  - Alaska averages five of the last six years [S].
  - Kuwait 2020 shows that savings can be legally inaccessible exactly when needed [S].
- **Bank ALM.** Liquidity coverage ratios, survival horizons, contingency funding plans and *funds-transfer pricing*: charging illiquid uses the internal shadow price of liquidity. That shadow price should feed the deck's α* hurdle [I].
- **Real options.** The band itself is an option for the owner and for ADIC. DWY's ~2% CE welfare cost of a spending floor is an external benchmark for its value [S].

---

## 3. Methods, models and trade-offs

### 3.1 Taxonomy of distribution rules

$B_t$ is the NAV basis, $\pi_t$ inflation, $F_t=W_t/(W_0\,\mathrm{CPI}_t\,e^{g^*t})$ the funded ratio against an intergenerational path, and $\Pi_{[a,b]}$ clipping to the band.

| ID | Rule | Equation | Peer analogue |
|---|---|---|---|
| R1–R3 | Fixed % of current NAV | $D_t=dW_t$ | Simple payout policies |
| R4 | Moving average | $D_t=d\cdot\frac{1}{3}\sum_{k=0}^{2}W_{t-k}$ | 12-quarter rules (NACUBO-style) |
| R5 | Hybrid (Yale/Stanford) | $D_t=\Pi_{[5\%,10\%]W_t}\big(\lambda D_{t-1}(1+\pi_{t-1})+(1-\lambda)r^*W_{t-1}\big)$ | Yale: λ=0.8, $r^*$=5.25%, band 4.0–6.5% [S]. Stanford 2020: 70/30, 5.5%, 4–6% [S] |
| R6 | POMV | $D_t=r^*\cdot\frac{1}{5}\sum_{k=1}^{5}W_{t-k}$ (first 5 of prior 6 years) | Alaska: $r^*$=5% (AS 37.13.140(b)) [S] |
| — | Expected-return rule | $D_t=\theta\,\mathbb{E}[r^{real}]\,W_t$ | Norway θ=1, E=3% real; Singapore θ≤0.5 [S] |
| R7 | Fixed real amount | $D_t=d_0W_0\,\mathrm{CPI}_t$ | Fiscal claims or entitlements |
| R8 | Ratchet (capped) | $D_t=\min(\max(D_{t-1},r^*W_t),\,10\%W_t)$ | Dybvig-type [S] |
| R9 | Surplus barrier | $D_t=\min(5\%W_t+\kappa(W_t-B^{path}_t)^+,\,10\%W_t)$ | de Finetti barrier |
| R12 | State-contingent hybrid | $D_t=\Pi\big(\lambda D_{t-1}(1+\pi_{t-1})+(1-\lambda)\,r_t^*W_t\big)$, with $r^*_t=\Pi_{[5,10]}(r_0+\kappa(F_t-1))$ | Dutch conditional indexation (unverified); LQ-optimal form |
| R10/R11 | Exogenous owner demand | $D_t=\Pi_{[5\%,10\%]}(\bar d+\beta\,\mathbb 1_{crisis,t-1}+\sigma_d\xi_t)\,W_t$ | Kuwait 2020, Norway 2020 |

### 3.2 Dynamic properties

- **Path dependence.** Pure % rules give an order-independent $W_T$. Smoothing adds "fixed-amount content" and therefore sequence risk.
- **Deterministic test** [I-MC]. Twenty years at +10% with one −25% year, terminal real NAV:

  | Rule | Crash in year 1 | Crash in year 10 | Crash in year 20 |
  |---|---|---|---|
  | 7.5% of current NAV | 0.589 | 0.589 | 0.589 |
  | Yale-type (7.5%) | 0.452 | 0.483 | 0.576 |
  | POMV (7.5%) | 0.554 | 0.558 | 0.644 |
  | Fixed real amount (7.5% of NAV₀) | 0.000 | 0.111 | 0.470 |

- **Stale-NAV leak** [I]. If the band applies to *reported* NAV and private marks lag, a 25% economic shock with private marks down only 10% leaves reported NAV at 0.84 against economic NAV of 0.75 (60% private). A 7.5% payout on reported NAV is then 8.4% of economic NAV.
- **Denominator arithmetic** [I]. That same shock lifts the reported private share from 60% to 64%. Paying one year's distribution from liquid assets lifts it to about 69.5%.

### 3.3 Monte Carlo specification ([I-MC])

**Return process.** Annual log-returns follow a two-regime lognormal mixture:
- crisis regime with probability 8% a year, log-return ~N(−0.22, 0.08²);
- normal-regime parameters calibrated so the arithmetic mean and SD hit the case targets.

The mixture gives negative skew and avoids the infinite moment-generating function of a Student-t.

**Inflation.** CPI follows an AR(1): mean 2.5%, φ=0.5, σ=1%.

**Run settings.** 100k paths, horizon 20 years, common random numbers across rules.

**Cases.**
- A: 10% mean, 12% SD (target met in expectation).
- B: 8%, 12% (peer-realistic).
- C: 6.5%, 14%.
- D: 10%, 16% (desmoothed).

**Two-bucket liquidity model** (10 years, 50k paths):
- **Starting position.** 40% liquid (mean 7%, SD 11%) and 60% private (mean 9.5%; log-beta 0.9 to liquid; idiosyncratic SD 7%).
- **PE cash flows.** Distribution yield 14% of private NAV (crisis 6%). Calls 25% of unfunded commitments (crisis 30%). Unfunded starts at 15% of NAV.
- **Pacing.** New commitments 6% of NAV while the private share is below 60%, otherwise 2%.
- **Liquidity floor.** 25% of NAV. Breaches force secondary sales at a 10% discount (25% in crisis), and buyers take over a proportional share of unfunded commitments.
- **Owner distributions.** Paid from liquid assets.

**Table 1: Feasibility under alternative return cases, T=20 years**

| Case | Median 20-yr annualized | P(≥10%) | Rule | Avg payout | Median real NAV₂₀ | P(real NAV₂₀<NAV₀) | P(<0.5) | SD real dist. growth | P(real cut>10%) |
|---|---|---|---|---|---|---|---|---|---|
| A | 9.44% | 42.2% | 5% fixed | 5.0% | 1.33 | 30% | 5% | 11.2% | 88% |
| A | | | 7.5% fixed | 7.5% | 0.78 | 69% | 21% | 11.2% | 94% |
| A | | | 10% fixed | 10.0% | 0.45 | 95% | 58% | 11.2% | 98% |
| A | | | Yale-type 80/20, 7.5% | 7.7% | 0.73 | 67% | 30% | 3.3% | 45% |
| A | | | POMV 7.5% | 7.5% | 0.80 | 63% | 26% | 4.2% | 40% |
| A | | | Fixed real 7.5% | 11.8% | 0.47 | 68% | 51% (P(NAV<5%·NAV₀) 31%) | 0% | 26% |
| A | | | State-contingent (R12) | 6.8% | 0.93 | 57% | 12% | 6.7% | 72% |
| B | 7.38% | 17.1% | 7.5% fixed | 7.5% | 0.53 | 89% | 45% | 11.2% | 98% |
| B | | | Yale-type 7.5% | 8.3% | 0.44 | 89% | 58% | 4.4% | 65% |
| B | | | Fixed real 7.5% | 14.7% | 0.00 | 88% | 75% (P(NAV<5%·NAV₀) 52%) | — | — |
| C | 5.62% | 8.4% | 7.5% fixed | 7.5% | 0.38 | 95% | 67% | 12.9% | 99.9% |
| D | 8.87% | 37.7% | 7.5% fixed | 7.5% | 0.70 | 70% | 31% | 14.4% | 99.5% |

**Table 2: Frontier sweep, Case A (excerpt)**

The right comparison is at equal cumulative payout.

| Rule | Avg payout | Median cumulative real dist./NAV₀ | Median real NAV₂₀ | P(real NAV₂₀<0.7) | SD dist. growth | P(cut>10%) |
|---|---|---|---|---|---|---|
| Fixed 7.0% | 7.00% | 1.34 | 0.87 | 34.5% | 11.2% | 92.0% |
| Yale-type 80/20, $r^*$=6.5% | 6.67% | 1.29 | 0.96 | 33.7% | 3.2% | 20.4% |
| POMV 7.5% | 7.46% | 1.34 | 0.81 | 41.9% | 4.2% | 39.5% |
| State-contingent 80/20, $r_0$=6.5%, κ=10% | 7.06% | 1.34 | 0.89 | 31.9% | 5.8% | 40.8% |
| Yale-type 80/20, $r^*$=7.5% | 7.74% | 1.37 | 0.73 | 47.3% | 3.3% | 44.0% |
| Fixed 7.5% | 7.50% | 1.37 | 0.78 | 41.8% | 11.2% | 93.3% |
| State-contingent 80/20, $r_0$=7.5%, κ=10% | 7.58% | 1.34 | 0.80 | 39.8% | 5.6% | 61.4% |

**Table 3: Two-bucket liquidity stress, 10 years, 25% liquid floor**

Cells are P(any forced secondary sale) and, in brackets, P(private share >70% at some year-end).

| Owner rule | DPI recovery (20% yield) | Base (14%) | Drought (10%) | High unfunded (25% NAV) |
|---|---|---|---|---|
| 5% of NAV | 0.0% (0%) | 0.4% (5%) | 4.1% (24%) | 1.7% (12%) |
| 7.5% of NAV | 0.4% (3%) | 4.8% (24%) | 60.4% (92%) | 12.4% (41%) |
| 10% of NAV | 3.2% (13%) | 27.4% (60%) | 100% (100%) | 70.0% (98%) |
| Yale-type 80/20, 7.5% | 1.4% (6%) | 15.6% (39%) | 67.2% (90%) | 27.6% (49%) |
| State-contingent, payout-matched 7.5% | 1.0% (5%) | 10.3% (33%) | 66.4% (94%) | 20.8% (45%) |
| State-contingent R12 (avg ≈6.6–6.9%) | 0.4% (2%) | 4.4% (19%) | 30.5% (67%) | 7.9% (31%) |
| Owner demand, wrong-way | 0.8% (4%) | 8.8% (30%) | 65.0% (92%) | 20.7% (46%) |
| Owner demand, independent | 0.5% (3%) | 5.7% (26%) | 68.8% (94%) | 17.0% (46%) |

**Reading the results** [I]:
- **(a) Payout level dominates everything.**
- **(b) Smoothing roughly triples payout stability** for nearly the same cumulative distributions. But it pays relatively *more* after drawdowns, so it worsens NAV tails and *raises* forced-sale risk. This is the central tension between the owner's budget stability and ADIC's liquidity.
- **(c) Funded-ratio feedback (R12)** recovers part of the NAV and liquidity tail at a given payout. Its main lever is lowering average payout in bad states.
- **(d) Wrong-way demand** adds about 3–4pp of forced-sale probability in the base and high-unfunded cases. It makes little difference in a drought, where the binding constraint is the DPI collapse itself.
- **(e) DPI regime and unfunded commitments matter as much as the rule.** PE cash-flow modelling in the sister stream is load-bearing for this module.

### 3.4 Gross versus net, and required returns

Required geometric return for real preservation is $R_{req}=(1+\pi)/(1-d)-1$, with π=2.5% [I]:

| Payout $d$ | 5% | 6% | 7% | 7.5% | 8% | 9% | 10% |
|---|---|---|---|---|---|---|---|
| $R_{req}$ (gross, geometric) | 7.9% | 9.0% | 10.2% | 10.8% | 11.4% | 12.6% | 13.9% |
| Gross needed if "10% net" | 15.8% | 17.0% | 18.3% | 18.9% | 19.6% | 20.9% | 22.2% |
| Real NAV growth if 10% geometric is achieved | +1.95% | +0.88% | −0.19% | −0.73% | −1.27% | −2.34% | −3.41% |

**Reading [I].** The 10% target is internally consistent with sustaining about a 6.8% payout in real terms. It is less if 10% is arithmetic (subtract roughly 0.7pp of drag at 12% volatility) or net of fees and taxes. As a cross-check, US endowments' 4.9% effective spending rate (FY2025) [S] is close to the break-even implied by their 7.7% 10-year return, $1-1.025/1.077\approx4.8\%$.

### 3.5 Three ways to model ADIC's distribution requirement

| Formulation | Pros | Cons | Use |
|---|---|---|---|
| **A. Deterministic rule inside the band**, $D_t=f_\theta(\text{state})$ | Transparent and testable; matches peers; parameters θ become the strategic decision | Ignores the owner's actual fiscal needs; ADIC may not own θ | Policy layer: θ chosen by policy search |
| **B. Stochastic exogenous demand** $d_t\sim$ owner model (oil, budget, regime) | Realistic stress tests; captures wrong-way risk (Kuwait 2020) | Needs an owner model; not optimizable by ADIC | Scenario layer for stress and Tier 1 gates |
| **C. Decision variable** $d_t\in[5\%,10\%]$ chosen each year | Gives shadow prices; finds state-contingent optima (DWY-type) | Can "game" the floor; governance legitimacy; needs an owner utility | Recourse layer, only where the mandate allows discretion |

**Recommendation [I]:**

$$D_t=\Pi_{[5\%B_t,\,10\%B_t]}\Big(\underbrace{f_\theta(D_{t-1},W_t,F_t,\pi_t)}_{\text{policy}}+\underbrace{\omega_t(O_t,s_t)}_{\text{owner shock}}+\underbrace{u_t}_{\text{discretion}}\Big)$$

- θ is optimized out of sample across multi-model scenario sets (the deck's Tier 1 robustness logic).
- $\omega_t$ is drawn from a regime-correlated owner-demand model.
- $u_t$ is a bounded recourse variable whose multipliers are reported.

---

## 4. Empirical evidence and current market data

**US endowments.** All figures are [S].
- **NACUBO-Commonfund FY2025** (released 12 Feb 2026; 657 institutions, $944.3bn):
  - 1-year return 10.9%, 3-year 10.0%, 5-year 10.2%, 10-year 7.7%;
  - the >$5bn cohort returned 11.8% with 62.5% in alternatives and 8.2% in fixed income;
  - effective spending rate 4.9% (private institutions 5.4%);
  - withdrawals $33.4bn; endowments fund 15.2% of operating budgets (largest cohorts 18–19%).
- **Early FY2026 results** (year to 30 Jun 2026):
  - Harvard 27.1% to $68bn, distributing $2.6bn (about 39–40% of operating revenue) under a framework of a 5% payout and an 8% return objective;
  - Stanford 31.7%; MIT 10.3%; Cambridge Associates average 15.5%.
  - Yale FY2026 was not verified. Yale FY2025: 11.1%, $44.1bn after $2.1bn of distributions (secondary source).

**Tax and liquidity shocks, 2025–26** [S]:
- **Endowment excise tax.** Tiered rates of 1.4% / 4% / 8% by endowment per student, for tax years after 31 Dec 2025, covering institutions with ≥3,000 tuition-paying students. Harvard expects about $300m a year at 8% and held its FY2027 distribution flat.
- **Yale.** A "mosaic" secondary sale of up to about $2.5bn (June 2025), with the discount expected below 10% and up to 15% on parts.
- **Harvard.** About $1bn of PE stakes to Lexington (April 2025) and $1.2bn of bonds in March–April 2025.

**2008–09 stress** [S]:
- **Harvard.** Fell from $36.9bn to about $26bn (−27.3%). It issued $2.5bn of taxable bonds in December 2008 and paid about $500m to terminate swaps. A reported $1.3–1.5bn PE secondary sale was attempted; the outcome is unclear in the sources. Unfunded commitments were $11bn through 2018. The endowment supplied 56% of the Faculty of Arts and Sciences' (FAS) income in FY2008.
- **Yale.** Returned −24.6% to $16.3bn, cut distributions 6.7% for FY2010 and planned a further 13% cut.
- **Lesson [I].** Losses on illiquid assets, collateral calls and committed calls arrived at the same time. The fix was borrowing plus distribution cuts, a lever a sovereign owner may *refuse* to pull.
- **2022 denominator effect.** Qualitatively well documented. Specific FY2022 figures were not re-verified in-session.

**PE liquidity regime** (Bain, *Global PE Report 2026*) [S]:
- distributions are about 14% of NAV (12 months to Q3 2025), "not seen since 2008–09", and have stayed below 15% for four years, an industry record;
- about 32,000 unsold companies worth $3.8tn;
- holding periods at exit are about 7 years, versus 5–6 in 2010–21;
- buyout exit value was $717bn (+47%);
- continuation vehicles grew 62%.

**Endowment-model performance** [S]. Ennis: significantly negative alphas, as summarized in §2.6. Swensen-model defenders point to elite-endowment persistence (Lerner, Schoar & Wang 2008).

**Peer return reference set (latest)** [S]:

| Fund | Return | Period/as-of |
|---|---|---|
| NBIM | 6.64% nominal (basket); 4.34% real net | 1998–2025 |
| GIC | 5.6% USD nominal; 3.4% real | 20 years to 31 Mar 2026 |
| CPP Investments | 8.8% net (C$); FY2026 7.8% vs reference 13.2% | 10 years to 31 Mar 2026 |
| Temasek | 8.0% USD (6.8% S$) TSR; 10-year 7.5% USD | 20 years to 31 Mar 2026 |
| NZ Super | FY2026 14.17%; Reference Portfolio since 2010 8.65% vs actual 10.09% (June 2026 report) | to 30 Jun 2026 |
| Alaska PF | FY2026 12.42%; $91.9bn | to 30 Jun 2026 |
| NACUBO all | 7.7% | 10 years to FY2025 |

---

## 5. Peer practice and case studies

**Norway (NBIM/GPFG)** [S]:
- **Fiscal rule.** Spending of fund assets over time tracks the expected real return, cut from 4% to 3% in February 2017 alongside the move to a 70% equity share.
- **Countercyclical by design.** Spending may rise in downturns and fall in upturns.
- **Size and mandate.** NOK 21,268bn at end-2025. Strategic mix 70/30. Expected tracking-error limit 1.25pp. Unlisted real estate ≤7%; unlisted renewable infrastructure ≤2%.
- **Flows.** Inflows of NOK 411bn (2024) and NOK 327bn (2025), with no withdrawals. Before 2020, net outflows had occurred only in 2016–2017.
- **Rebalancing.** Rule-based around the 70% benchmark. NBIM proposed a narrower ±2pp band with gradual adjustment (2018). The current mandate parameters are unverified.
- **Transferable [I]:** spend from *expected* returns; rule-based rebalancing; a clear Ministry/Norges Bank split.
- **Not transferable [I]:** the 3% rule assumes a liquid fund with net inflows. ADIC has the reverse on both counts.

**Alaska Permanent Fund** [S]:
- POMV draw of 5% of average market value for the first five of the preceding six fiscal years (2018 law; 5.25% until 2021).
- FY2026 draw $3.8bn; $4.0bn committed for FY2027 from the Earnings Reserve Account (ERA).
- The FY2026 inflation-proofing transfer ($1.5bn) was skipped "given the lack of appropriation".
- SB 274 would phase the rate to 4.5% from FY2029 (status unverified).
- **Lessons [I].**
  - The averaging lag dampens the draw.
  - The ERA works as a distribution buffer.
  - Intergenerational protections can be overridden politically, so model political override as a scenario.

**Singapore** [S]:
- NIRC = up to 50% of Net Investment Returns on net assets managed by GIC, MAS and Temasek (net of government liabilities), based on expected long-term real returns concurred by the President. The framework dates from 2008.
- FY2025 NIRC was estimated at S$27.14bn.
- **Transferable [I].** A *two-key rule*: spend a fraction θ<1 of an independently certified expected return. This aligns closely with an IC-endorsed $r^*$ in R12.

**Kuwait (KIA), 2020** [S]:
- The Treasury held about KD2bn of liquidity while the GRF was being drawn at about KD1.7bn a month.
- Parliament removed the automatic 10% FGF transfer, and about KD2.05bn was moved to the GRF.
- The debt law stalled, and Fitch flagged imminent depletion of GRF liquid assets.
- The FGF (about 400% of GDP) could not be drawn without parliamentary approval.
- **Lesson [I].** Owner demand is regime-correlated and lumpy, and institutional constraints can block "obvious" liquidity sources. ADIC's scenario library must include owner fiscal stress plus a market crash plus DPI drought.

**CPP Investments** [S]:
- FY2026 7.8% net, 10-year 8.8%, C$793.3bn.
- Reference portfolios were relabelled "market risk targets" in FY2025.
- Recourse debt was 9.7% of adjusted net assets (FY2025), with investment liabilities of C$222.5bn. S&P cites a board recourse-leverage limit of 45% of net assets (from FY2023).
- TPA rests on five pillars: relative value, factors, liquidity, leverage and currency. Since 2016 there is a liquid passive "balancing portfolio".
- Leverage is managed at total-fund level as a "balance sheet risk stabiliser": it falls when private exposure rises. Multi-horizon LCRs tie leverage capacity to stressed coverage.
- Public and private investments "compete explicitly on a common risk-adjusted basis". The same test applies to *resizing or selling* existing positions, which maps directly to ADIC's SELL/HOLD lens.

**NZ Super** [S]:
- Reference Portfolio is 80:20 growth/fixed income (75% global equities, 5% NZ equities, 20% global fixed income), 100% hedged to NZD.
- The 2026 review (effective 1 July 2026) weights current valuations more and lowered the equity risk premium. The value-add expectation was cut from 1.0% to 0.9% a year.
- FY2026 return 14.17%, size NZ$94.4bn. Strategic tilting is used inside TPA.

**GIC** [S]:
- 20-year real return of 3.4% is "the primary metric".
- A new framework from 2026 introduces a **Strategic Portfolio** of three asset groups (equities for growth, fixed income for income, real assets for inflation resilience). The GIC Portfolio aims to beat it "within approved risk parameters".
- An overlay portfolio run by the CIO's office handles short-term funding and thematic exposures (CAIA/TAI 2025).

**Temasek and ADIA** [S]:
- **Temasek.** S$518bn net portfolio value (31 Mar 2026); 20-year TSR 6.8% S$ / 8.0% USD. The Astrea PE-bond series (nine issues since 2006, Astrea 9 in 2025) securitizes PE fund portfolios. That is a REFINANCE precedent, and the structure belongs to the sister stream.
- **ADIA.** The 2025 Review widened ranges to 15–20% for private equity and 7–12% for financial alternatives, and narrowed real estate to 2–7%.
- **Future Fund (Australia).** Per CAIA/TAI, it deliberately allocates more to PE, VC and infrastructure than peers, supported by a portfolio-integration team. Mandate return-target details were not verified in-session.

**TPA, operationally** [S]/[P]:
- **Four dimensions** (CAIA/TAI, *From Vision to Execution*, Oct 2025): empowering governance, single-portfolio culture, competition for capital, and investing through a factor lens. Exemplars: Future Fund, GIC, NZ Super, CPPIB.
- **Funding baskets become opportunity cost.** Firms start by mapping funding assets ("selling public equity to fund private equity"); mature TPA "decouples the concept of funding" toward opportunity cost and portfolio improvement.
- **Reference portfolio role** (Urwin & Hayman, CFA Institute guide, July 2026). It sets risk guardrails and is "not intended as a benchmark to be closely tracked". Typical tracking error is about 4–5% a year. Cost-of-capital hurdle models are central.
- **Urwin (WTW):** "SAA is comfortable governance but clunky portfolio management. TPA is efficient portfolio management but stretchy governance."
- **Pitfalls [P]:**
  - weak board/CIO accountability causes drift back to silos;
  - incentives must be rewritten;
  - attribution is harder;
  - claimed performance edges (1.3% a year for adopters) are not causal, since adopters are larger and better governed.

**Adopt / adapt / avoid for ADIC [I]:**

| Practice | Verdict | Rationale |
|---|---|---|
| Board-owned reference portfolio plus risk budget | Adopt | Gives α* a funding basket and the IC a risk anchor |
| Expected-return-based distribution anchor (Norway/Singapore) | Adapt | Use IC-certified $r^*$ with θ<1; distinguish ADIC's illiquidity |
| Multi-year averaging (POMV) and floor/cap bands (Yale) | Adapt | Within 5–10%, test lags of 1–5 years |
| Total-fund leverage as stabilizer plus LCR gates (CPP) | Adopt | Matches "leverage allowed"; caps tied to coverage |
| Opportunity-cost test for existing holdings (CPP) | Adopt | Core of SELL/HOLD/REFINANCE/LEVER |
| Distribution reserve / buffer account (Alaska ERA) | Adopt | Finite-horizon protection (Dybvig-consistent) |
| Fixed real or nominal distribution amounts | Avoid | 31–52% depletion in 20 years (70% in low-return case) [I-MC] |
| Asset-class quotas, SAA silo benchmarks | Avoid | TPA evidence; Ennis critique |
| Smoothing for its own sake | Use cautiously | Raises forced-sale risk in illiquid books [I-MC] |

---

## 6. Design implications for the ADIC framework

### 6.1 State variables (annual core, quarterly liquidity sub-step)

- **Wealth and buckets:** $W_t=L_t+P_t+C_t-B^{debt}_t$, where $L$ is liquid unencumbered, $P$ private (by strategy and vintage), and $C$ overlay collateral. Track both *reported* $P^{rep}_t$ and *economic* $P^{eco}_t$.
- **Commitments:** $U_t$, unfunded.
- **Distribution memory:** $D_{t-1}$ and the NAV history $W_{t-1..t-6}$.
- **Funded ratio:** $F_t=W_t/(W_0\mathrm{CPI}_te^{g^*t})$.
- **Regime:** $s_t$, from the deck's HMM.
- **Owner fiscal state:** $O_t$ (oil price, budget balance).
- **Inflation:** $\pi_t$.
- **Other:** facility headroom and leverage ratio.

### 6.2 Decision variables

**Strategic θ:**
- $r_0$ (default 6.5%; test 5.5–8.5%);
- λ (0.8; test 0.6–0.9);
- κ (10%; test 0–20%);
- NAV basis $B_t$ (current reported, 3-year average, economic);
- $g^*$ (0%; test −1% to +1%);
- reserve horizon $H_R$ (24 months; test 12–36);
- pacing parameters.

**Tactical:**
- $u_t$ (discretion within the band);
- commitments $X_t$;
- secondary sales $S_t$;
- borrowing $\Delta B^{debt}_t$;
- overlay hedge notional;
- rebalancing.

### 6.3 Constraints (Tier 1 additions)

- **Band:** $5\%B_t\le D_t\le10\%B_t$ (hard; shadow prices $\mu^{floor}_t,\mu^{cap}_t$ reported).
- **Distribution coverage ratio** (bank-LCR analog):

  $$\text{DCR}_t=\frac{\sum_i h_iL_{i,t}+\text{committed facilities}}{\sum_{\tau=1}^{H_R}\big(\hat D_{t+\tau}+\widehat{\text{calls}}^{stress}_{t+\tau}-\widehat{\text{dists}}^{stress}_{t+\tau}\big)+\text{P99 margin}}\ge1$$

  The constraint must hold with probability ≥95% at all $t\le$5 years. Haircuts $h_i$ follow regime.
- **Forced-sale chance constraint:** P(forced secondary sale within 5 years) ≤ ε_L (default 5%).
- **Private-share ceiling:** P($P^{rep}/W$ > 70%) ≤ 10%.
- **Leverage:** recourse debt ≤ ℓ_max·W. Default 10–20%, policy-set. For reference, CPP's board recourse-leverage limit is 45% of net assets [S], while actual recourse debt is about 9.7% of adjusted net assets (FY2025) [S].
- **Intergenerational chance constraint:** P($W^{real}_{10}<\kappa_{IG}W_0$) ≤ ε_IG (default κ_IG=0.8, ε_IG=20%), or an explicit owner-endorsed decumulation path.
- **Deck constraints kept:** 7% robust floor, IG+cash ≥8%.

### 6.4 Objective terms (Tier 2)

$$\max_\theta\ \mathbb E\Big[\sum_{t}\beta^t u\big(D^{real}_t-hD^{real}_{t-1}\big)\Big]+\beta^T\mathbb E[v(W^{real}_T)]-\lambda_L\,\mathbb E[\text{sale losses}]-\lambda_{\Delta}\,\mathbb E\big[\textstyle\sum(\Delta\ln D^{real}_t)^2\big]$$

- **Defaults:** CRRA γ=2 (DWY), habit h=0.8, β=0.97.
- **Alternatives.** A multi-criteria Pareto set for the IC, or "maximize P(10%)" subject to the constraints above, consistent with the deck's TAP.
- **Liquidity price.** The shadow price of the DCR constraint, $\lambda^{liq}_t$, is the internal liquidity transfer price that enters α*:

  $$\alpha^*_j=\mathbb E[r_j]-r_{\text{funding basket}}-\lambda^{liq}\cdot\text{LAR}_j-\text{risk charges}$$

### 6.5 Candidate rules to test (minimum set)

1. Fixed 5% / 6.5% / 7.5% / 10% of current NAV (baselines).
2. Yale-type hybrid, λ∈{0.7,0.8,0.9}, $r^*$∈{5.5,6.5,7.5}%.
3. POMV $r^*$∈{6.5,7.5}%, lag 1–5.
4. State-contingent R12, $(\lambda,r_0,\kappa)$ grid.
5. Expected-return rule $D=\theta\hat r^{real}_{IC}W$, θ∈{0.5,0.75,1.0}, adding inflation.
6. Owner-demand overlays, independent versus wrong-way, β∈{0,2.5,5}pp.
7. Each rule crossed with a distribution reserve of $H_R$∈{12,24,36} months, and with an economic-versus-reported NAV basis.

### 6.6 Calibration targets and data needs

**Targets [S]:**
- NACUBO effective spending 4.9% and 10-year return 7.7%;
- Yale 5.25% target, band 4.0–6.5%, λ=0.8;
- Alaska 5% POMV;
- Norway 3% real;
- Singapore θ=0.5;
- Harvard 5% payout with an 8% objective;
- Bain distribution yield 14% (current), crisis 4–8%;
- secondary discounts <10% normal (Yale 2025), 25% crisis (DWY);
- DWY welfare cost of a floor, about 2% CE.

**ADIC data needs:**
- the legal text of the distribution mandate: base, timing, cash vs in-kind, discretion, carry-forward;
- the owner's fiscal sensitivity to oil;
- cash-flow history by fund (calls, distributions, NAV);
- unfunded commitments by vintage;
- facility terms and leverage limits;
- overlay margin history;
- secondary pricing history;
- reported versus economic NAV series.

### 6.7 IC deliberation artifacts

Each artifact is computed deterministically. LLM agents only narrate and challenge.
1. **Mandate interpretation memo:** gross vs net; NAV basis.
2. **Distribution-capacity fan chart:** sustainable $d^*$ with uncertainty.
3. **Four-dimension frontier:** cumulative distributions, NAV tail, stability, P(forced sale), with the IC choosing the point.
4. **Stress narratives:** owner fiscal stress, DPI drought, crash.
5. **Liquidity waterfall:** liquid → facility → overlay de-risking → secondary → NAV loan or CFO, with marginal costs.
6. **Shadow prices** of the floor and cap.

Agents to add:
- Mandate & Policy Registry agent;
- Owner-Demand Scenario agent;
- Peer Calibration agent. Refresh calendar: NACUBO in February; CPP in May; GIC and Temasek in July; NBIM in February and August; Harvard and NZ Super in October.

---

## 7. Implementation notes

- **Python stack:**
  - `numpy`/`numba` for vectorized path simulation (paths × years × rules);
  - `scipy`, `nevergrad`/`cma` (CMA-ES) or `optuna` for policy search over θ;
  - `cvxpy` for per-period allocation with CVaR chance-constraint approximations;
  - `pyomo` for short-horizon (3–5 year) scenario-tree recourse models;
  - `hmmlearn`/`statsmodels` for regimes;
  - `pandas`/`xarray` for path cubes;
  - `SALib` for global sensitivity.
- **Algorithms.**
  - Use Powell's taxonomy (Powell 2019, *EJOR*). Prefer **policy-function approximation**: parameterized rules optimized by simulation. These stay interpretable for the IC.
  - Add a **direct lookahead** stochastic program for the first 3–5 years.
  - Use LQ linearization to seed R12 gains.
  - Deep RL only as an exploratory challenger.
- **Cost.** Our C# prototype ran 12 rules × 4 cases × 100k paths × 20 years in about 6 seconds. A 6-parameter CMA-ES search with about 300 evaluations at 50k paths is minutes in numba.
- **Numerical pitfalls:**
  - **Timing conventions.** Beginning-of-year payment *before* a same-year crash artificially rewards wrong-way demand. We hit this and moved the demand to lag the crisis.
  - **Burn-in.** Initialize the pre-history for averaging rules.
  - **Two NAVs.** Keep reported and economic NAV separate and desmooth.
  - **Fat tails.** Avoid Student-t exponentials (infinite moment-generating function); use regime mixtures or truncation.
  - **Rare events.** Tail probabilities below 1% need ≥100k paths or importance sampling. Report binomial standard errors.
  - **Common random numbers** across rules.
  - **Overfitting θ** to one generator: evaluate across multi-model ensembles, consistent with the deck's misspecification gate.
- **Reproducibility.** Prototype code: `spendsim.ps1` and `run_sweep.ps1`. Absolute paths are in the structured output; the results tables are reproduced in §3.3.

## 8. Risks, pitfalls and limitations

- **Mandate ambiguity.** The base, timing and discretion of the 5–10% band dominate results. Wrong assumptions invalidate everything downstream.
- **Stylized simulations.** Two regimes, iid annual returns, constant yields and calls, and assumed unfunded commitments. No serial correlation, fees, taxes, FX or overlay P&L. Treat the [I-MC] numbers as orders of magnitude and directional.
- **Peer transplant risk.** Norway (liquid, net inflows), US endowments (tuition and gifts) and Alaska (political ERA) differ structurally from ADIC.
- **Performance-claim risk.** TPA and endowment-model claims carry survivorship and selection bias. Ennis finds negative alphas.
- **Political override.** Alaska's skipped inflation-proofing and Kuwait's legal blockages show rules can be set aside.
- **Smoothing paradox.** Smoothing protects the owner's budget but increases ADIC's liquidity stress.
- **Data gaps in this dossier.** Not verified in-session: FY2022 denominator figures, Future Fund mandate details, NBIM's current rebalancing band, Yale FY2026, and the original of de Finetti (1957), whose title and venue are known only from a citing reference. [corrected 2026-10-18: the Dufresne and Owadally–Haberman details have since been verified via Crossref and OpenAlex; see §10.]

## 9. Open questions

1. Is the 10% target geometric or arithmetic, gross of distributions, net of fees, and over what horizon? Is it an objective or a hurdle?
2. Does the 5–10% apply to opening, average, reported or economic NAV? Who chooses the point in the band? Can over- and under-distribution carry forward? Are in-kind transfers allowed?
3. Does the owner provide inflows in surplus years, so the question is net versus gross flows? Is ADIC the marginal liquidity provider to the budget?
4. Is the owner's intergenerational objective real preservation, real growth, or planned decumulation?
5. What are current unfunded commitments, call and distribution histories, facility headroom and leverage limits?
6. What political or legal mechanisms could override the distribution rule (Kuwait or Alaska analogues)?
7. Should the distribution rule be owned by the owner (Norway, Singapore) or by ADIC's board (Yale, Alaska)?

## 10. References

**Theory and literature**
1. Tobin, J. (1974). What is permanent endowment income? *AER* 64(2):427–432. RePEc: https://ideas.repec.org/e/c/pto4.html
2. Merton, R.C. (1993). Optimal investment strategies for university endowment funds. In Clotfelter & Rothschild (eds.), *Studies of Supply and Demand in Higher Education*, ch. 7, pp. 211–242, U. Chicago Press. https://www.nber.org/chapters/c6102 ; NBER WP 3820 (Aug 1991) https://www.nber.org/papers/w3820
3. Dybvig, P.H. (1999). Using asset allocation to protect spending. *FAJ* 55(1):49–62. DOI 10.2469/faj.v55.n1.2241. https://rpc.cfainstitute.org/research/financial-analysts-journal/1999/using-asset-allocation-to-protect-spending ; draft https://phildybvig.com/research/papers/ratchet2p.pdf
4. Dybvig, P.H. (1995). Dusenberry's ratcheting of consumption: optimal dynamic consumption and investment given intolerance for any decline in standard of living. *Review of Economic Studies* 62(2):287–313. DOI 10.2307/2297806.
5. Dimmock, S.G., Wang, N., Yang, J. (2024). The endowment model and modern portfolio theory. *Management Science* 70(3):1554–1579. DOI 10.1287/mnsc.2023.4759. NBER WP 25559: https://www.nber.org/papers/w25559
6. Gilbert, T., Hrdlicka, C. (2015). Why are university endowments large and risky? *RFS*, doi:10.1093/rfs/hhv031. White paper: https://faculty.washington.edu/gilbertt/docs/University%20endowments%20-%20White%20Paper%20-%20Gilbert%20Hrdlicka%20-%2012%20November%202017.pdf
7. Brown, J.R., Dimmock, S.G., Kang, J.-K., Weisbenner, S.J. (2014). How university endowments respond to financial market shocks: evidence and implications. *AER* 104(3):931–962. DOI 10.1257/aer.104.3.931. https://www.aeaweb.org/articles?id=10.1257/aer.104.3.931
8. Campbell, J.Y. (2012). Investing and spending: the twin challenges of university endowment management. *Forum Futures 2012*. https://dash.harvard.edu/bitstream/handle/1/22423613/ff1205s.pdf ; slides https://scholar.harvard.edu/sites/scholar.harvard.edu/files/campbell/files/investingspending_slides_20110606.pdf
9. Cejnek, G., Franz, R., Randl, O., Stoughton, N. (2014). A survey of university endowment management research. *JOIM* 12(3):90–117. https://joim.com/article/a-survey-of-university-endowment-management-research
10. Ennis, R.M.: two separate papers. Until 2026-10-18 both findings were cited to the single SSRN 3614875 entry.
    - (a) Ennis, R.M. (2021a). Endowment performance. *The Journal of Investing* 30(3):6–20. DOI 10.3905/joi.2021.1.166. Working paper: Endowment performance and the demise of the multi-asset-class model, SSRN 3614875 (2020), DOI 10.2139/ssrn.3614875. Swedroe summary: https://hedgefundalpha.com/strategies/the-enduring-futility-of-the-endowment-model/
    - (b) Ennis, R.M. (2021b). Failure of the endowment model. *The Journal of Portfolio Management* 47(5):128–143. DOI 10.3905/jpm.2021.1.217. Coverage in *Institutional Investor* (1 Apr 2021): https://www.institutionalinvestor.com/article/2bswtbayp11p67nyfj3ls/portfolio/its-time-to-replace-the-grossly-inefficient-endowment-model-says-richard-ennis [unverified: the −1.87% figure (endowments over $1bn, "over the 12 years ending in June 2020") appears in the *Institutional Investor* coverage of Ennis's "third and concluding paper". That coverage does not name the paper, and the literature audit found the figure is not in this paper's abstract. The match rests on date and topic.]

Further theory references. These were listed as "not verified in-session" until 2026-10-18; they are now verified via Crossref or OpenAlex unless flagged:
- de Finetti, B. (1957). Su un'impostazione alternativa della teoria collettiva del rischio. *Transactions of the XVth International Congress of Actuaries* 2:433–443. [unverified: the original is not indexed in Crossref. The title, venue and pages come from reference 8 of Loeffen (2008), *Ann. Appl. Probab.* 18(5):1669–1680, DOI 10.1214/07-AAP504; that reference's misspellings ("impostazion … dell teoria collecttiva") are corrected here.]
- Dufresne, D. (1988). Moments of pension contributions and fund levels when rates of return are random. *Journal of the Institute of Actuaries* 115(3):535–544. DOI 10.1017/s0020268100042815. [unverified: Crossref and Cambridge Core index the title as "Movements of …"; "Moments" follows the literature audit and citing references.]
- Owadally, M.I., Haberman, S. (1999). Pension fund dynamics and gains/losses due to random rates of investment return. *North American Actuarial Journal* 3(3):105–117. DOI 10.1080/10920277.1999.10595837.
- Owadally, M.I., Haberman, S. (2004). Efficient gain and loss amortization and optimal funding in pension plans. *North American Actuarial Journal* 8(1):21–36. DOI 10.1080/10920277.2004.10596126.
- Lerner, J., Schoar, A., Wang, J. (2008). Secrets of the academy: the drivers of university endowment success. *Journal of Economic Perspectives* 22(3):207–222. DOI 10.1257/jep.22.3.207.
- Powell, W.B. (2019). A unified framework for stochastic optimization. *European Journal of Operational Research* 275(3):795–821. DOI 10.1016/j.ejor.2018.07.014.
- Constantinides, G.M. (1990). Habit formation: a resolution of the equity premium puzzle. *Journal of Political Economy* 98(3):519–543. DOI 10.1086/261693.
- Kydland, F.E., Prescott, E.C. (1977). Rules rather than discretion: the inconsistency of optimal plans. *Journal of Political Economy* 85(3):473–491. DOI 10.1086/260580.

**Spending rules and peers**

11. Yale Policy 2202, Endowment Spending and Distributions (effective 1 Mar 2023; revised 1 Jul 2026). https://your.yale.edu/policies-procedures/2202-endowment-spending-and-distributions
12. Stanford payout process (2020 guide; parameters changed Oct 2021, unverified). https://fingate.stanford.edu/managing-funds/endowment-payout-process ; https://doresearch.stanford.edu/documents/endowment-process-tutorialpdf/download
13. APFC, FY26 audit and budget proposal (2 Sep 2026). https://apfc.org/fund-news/fy26-audit-and-budget-proposal/ ; SB 274 (AS 37.13.140(b)): https://www.akleg.gov/pdf/34/F/SB0274-1-2-040126-REV-Y.PDF
14. Norway Ministry of Finance (16 Feb 2017). https://www.regjeringen.no/en/aktuelt/increased-equity-share-in-the-government-pension-fund-global-and-adjustment-to-the-expected-rate-of-return-in-the-fiscal-policy-guidelines/id2539303/ ; https://norskpetroleum.no/en/economy/management-of-revenues ; NBIM Annual Report 2025: https://www.nbim.no/en/news-and-insights/reports/2025/annual-report-2025/web-report-annual-report-2025/ ; NBIM rebalancing note (2018): https://www.nbim.no/en/news-and-insights/the-press/press-releases/2018/new-discussion-note-on-rebalancing-rules/
15. Singapore MOF, NIRC. https://www.mof.gov.sg/policies/reserves/net-investment-returns-contribution/ ; Budget 2025 overview: https://mof.gov.sg/docs/librariesprovider3/budget2025/download/pdf/02-overview-of-the-budget-for-financial-year-2025.pdf
16. Kuwait 2020: https://gulfnews.com/world/gulf/kuwait/kuwait-cant-pay-salaries-beyond-october-minister-tells-parliament-1.1597852565530 ; https://gulfnews.com/business/banking/kuwait-to-transfer-2b-dinars-to-general-reserve-fund-1.73368385 ; Fitch: https://www.cbk.gov.kw/en/images/fitch-press-release-1_v00_tcm10-153300.pdf ; S&P: https://gulfnews.com/business/banking/standard--poors-revises-kuwaits-rating-outlook-to-negative-1.72677162
17. CPP Investments FY2026 release: https://www.newswire.ca/news-releases/cpp-investments-net-assets-total-793-3-billion-at-2026-fiscal-year-end-814459989.html ; Morningstar DBRS (3 Jul 2025): https://dbrs.morningstar.com/research/457796/morningstar-dbrs-confirms-cpp-investments-at-aaa-and-cppib-capital-inc-at-aaa-and-r-1-high-stable-trends ; S&P (Jan 2025): https://www.cppinvestments.com/wp-content/uploads/2025/04/SP-RatingsDirect_CPPIB_3310933_Jan-20-2025.pdf ; TPA engine: https://pensionpulse.blogspot.com/2026/05/inside-cpp-investments-tpa-engine.html
18. NZ Super: https://nzsuperfund.nz/how-we-invest/reference-portfolio/ ; https://nzsuperfund.nz/news-and-media/strong-all-round-performance-sees-super-fund-grow-by-9-3-billion/ ; https://www.top1000funds.com/investor-profile/nz-super-cuts-benchmark-return-expectation-on-us-valuation-concerns/
19. GIC (24 Jul 2026): https://www.gic.com.sg/newsroom/all/gic-delivers-steady-long-term-returns-within-its-mandate-and-stays-focused-on-portfolio-resilience-in-a-structurally-changed-world/
20. Temasek (8 Jul 2026): https://www.temasek.com.sg/en/news-and-resources/news-room/news/2026/temasek-net-portfolio-value-grows-to-518b-up-49b-from-last-year ; Azalea/Astrea: https://www.azalea.com.sg/
21. ADIA Review 2025: https://www.adia.ae/en/pr/2025a/index.html

**Market data and case history**

22. NACUBO FY2025 press release (12 Feb 2026): https://www.nacubo.org/Press-Releases/2026/US-Higher-Education-Endowments-Report-Stable-Returns-Increase-Spending-to-33-4-Billion-in-FY25
23. *Harvard Magazine* (15 Oct 2026), FY2026: https://www.harvardmagazine.com/university-finances/harvard-endowment-financial-report-fiscal-year-2026 ; Quartz: https://qz.com/harvard-endowment-return-spacex-ai-gains-101526
24. *Harvard Magazine* (Jul 2009), Liquidity and Leverage: https://www.harvardmagazine.com/2009/07/liquidity-leverage ; Yale 2009: https://harvardmagazine.com/breaking-news/yale-endowment-losses-spending-cuts ; https://investments.yale.edu/wp-content/uploads/2024/10/2009YaleEndowment.pdf
25. Yale 2025 secondary: https://www.bloomberg.com/news/articles/2025-06-04/yale-nears-deal-to-sell-2-5-billion-of-private-equity-stakes ; https://www.privateequitywire.co.uk/yale-nears-2-5bn-secondary-sale-of-pe-and-vc-stakes/ ; Harvard: https://www.thecrimson.com/article/2025/4/25/private-equity-stake-sales/ ; Yale FY2025 (secondary): https://www.universalassetowners.com/registry/institution/yale-investments-office/
26. Endowment tax (Foley, Jul 2025): https://www.foley.com/insights/publications/2025/07/changes-to-the-college-and-university-endowment-tax/
27. Bain, *Global PE Report 2026*: https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ ; 2025: https://www.bain.com/insights/topics/global-private-equity-report/2025/

**Total Portfolio Approach**

28. Filbeck, A., Bok, J. (CAIA/TAI, Oct 2025). *From Vision to Execution: How Investors Are Operationalizing the TPA*. https://www.thinkingaheadinstitute.org/content/uploads/2025/10/2025-TPA-Report-from-Vision-to-Execution.pdf ; TAI TPA hub: https://www.thinkingaheadinstitute.org/research-papers/total-portfolio-approach-tpa-hub/
29. Urwin, R., Hayman, G. (2026). *The Total Portfolio Approach (TPA): A Practical Guide for Navigating the Transition to TPA*. CFA Institute Research and Policy Center (28 Jul 2026). DOI 10.56227/26.1.20. https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/fti_tpa-report_online.pdf
30. CAIA (27 May 2026), TPA podcast: https://caia.org/content/total-portfolio-approach

## Citation corrections (2026-10-18)

Sources: the literature audit (`research/literature/00_LITERATURE_SYNTHESIS.md` §2) and its stream-02 table (`research/literature/02_endowment_swf.lit.md` §2). Metadata was re-confirmed on 2026-10-18 via Crossref, OpenAlex and NBER.

- §2.6: The Ennis alphas (−1.1% to −1.8%, t −2.7 to −4.9) are now attributed to six fund-size cohorts, not the 43 endowments. Added the 43-largest result: none outperformed significantly, and one in four underperformed significantly.
- §2.6: The −1.87% is moved to a separate paper (Ennis 2021b, attribution inferred) and limited to endowments over $1bn. "A year" is dropped, because the source does not say the figure is annualized.
- §2.7: de Finetti (1957): "unverified" replaced by a note that its title and venue come from a citing reference (§10).
- §2.7: "unverified details" removed for Dufresne (1988) and Owadally & Haberman (1999, 2004).
- §4: "unverified details" removed for Lerner, Schoar & Wang (2008).
- §5: The CFA Institute TPA guide is now attributed to Urwin & Hayman.
- §7: "unverified details" removed for Powell (2019).
- §8: Data-gap list updated. Dufresne and Owadally–Haberman are now verified; de Finetti's original is still not indexed. Marked [corrected 2026-10-18].
- §10 ref 2 (Merton 1993): added ch. 7, pp. 211–242 (NBER chapter PDF cover) and the WP 3820 date (Aug 1991).
- §10 ref 3 (Dybvig 1999): added DOI 10.2469/faj.v55.n1.2241.
- §10 ref 4 (Dybvig 1995): added the full title and DOI 10.2307/2297806; dropped "bibliographic details unverified".
- §10 ref 5 (Dimmock, Wang & Yang 2024): added DOI 10.1287/mnsc.2023.4759.
- §10 ref 7 (Brown et al. 2014): added the subtitle ("evidence and implications") and DOI 10.1257/aer.104.3.931.
- §10 ref 10 (Ennis): split into two entries:
  - (a) *J. Investing* 30(3):6–20 (2021), DOI 10.3905/joi.2021.1.166, with SSRN 3614875 (2020) as its working paper;
  - (b) *JPM* 47(5):128–143 (2021), DOI 10.3905/jpm.2021.1.217, with the −1.87% attribution marked [unverified].
- §10, former "not verified in-session" list: replaced by full entries with DOIs for:
  - Dufresne (1988; title discrepancy flagged [unverified]);
  - Owadally & Haberman (1999, 2004);
  - Lerner, Schoar & Wang (2008);
  - Powell (2019);
  - Constantinides (1990);
  - Kydland & Prescott (1977).
- §10, de Finetti (1957): added the venue and pages (*Trans. XVth International Congress of Actuaries* 2:433–443); still marked [unverified].
- §10 ref 29: the CFA Institute guide is now cited as Urwin, R., Hayman, G. (2026), DOI 10.56227/26.1.20. OpenAlex confirms these two authors; the audit's "Urwin et al." reflects index truncation.
- Not applicable to this dossier: none of the following works or figures appears here, so nothing was changed:
  - the G4 co-investment barrier (Broadie–Glasserman–Kou) re-run values;
  - the re-check results for topics 10, 11, 13, 14 and G3;
  - the cross-file items in audit §2.6.
