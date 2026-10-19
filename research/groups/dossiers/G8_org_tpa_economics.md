# Dossier G8: Organizational economics of ADIC's seven-group TPA

**Internal capital markets, transfer pricing from optimizer duals, forecast incentives, decision rights and internal transfers**

- **Project:** ADIC multi-period robust TPA framework (agentic) · **Stream:** G8 · **As of:** 18 Oct 2026
- **Audience:** design/architecture team, TPA and treasury desk, IC secretariat, HR/compensation committee
- **Evidence tags:**
  - **[S]** sourced; read in-session from the URL in §10.
  - **[S\*]** sourced via another stream's verification log (stream named).
  - **[P]** practitioner consensus.
  - **[I]** my inference or design choice.
  - **[I-calc]** synthetic computation in `research/groups/verification/G8_org_calcs.py` (results in `G8_org_calcs_results.json`). All inputs are **SYNTHETIC**, not ADIC data.
  - **[M]** cited from memory; not re-verified in-session. Never load-bearing.
- **Research constraints.** The session's shared WebSearch budget ran out early in this stream, so most sources were read by fetching primary URLs directly (NBER, RePEc, arXiv, BIS, EBA, regulators, fund reports and agenda papers). The Consensus connector exposed only interactive authentication tools, which were not called.
- **Scope boundary.** Stream 08 already derives asset-level liquidity prices from duals, stream 07 the forward-belief fusion, and C4/14 the IC protocol and decision tiers. This dossier adds the *group* layer: budgets, charges, credibility, decision rights, transfers and pay. It cross-links rather than repeats.

---

## 1. Executive summary

1. **ADIC is an internal capital market (ICM), and theory predicts both its value and its failure modes.**
   - **Value [S].** Headquarters can "winner-pick", actively shifting funds between competing projects (Stein 1997). Internal reallocation is worth most when outside capital is dislocated: conglomerates' internal capital markets became *more* valuable in 2007–09 (Kuppuswamy & Villalonga 2016). For ADIC, outside capital means secondary sales and NAV loans, which are dearest exactly in a DPI drought.
   - **Failure modes [S].** Divisional rent-seeking leads headquarters to buy managers off with capital, producing a "kind of socialism" in which strong divisions subsidize weak ones (Scharfstein & Stein 2000). Funds flow toward the least efficient divisions, and the distortion grows with the diversity of opportunities (Rajan, Servaes & Zingales 2000). ADIC's seven groups, from tail hedges to buyout funds, are about as diverse as an organization gets.
   - **Shock propagation [S].** A segment's investment responds to the *other* segments' cash flow, whatever its relative opportunities (Shin & Stulz 1998). After the 1986 oil collapse, oil companies cut non-oil investment by significantly more than their industries' median firms (Lamont 1997). ADIC's owner is oil-exposed, so owner-demand shocks will spread to every group unless budgets are state-contingent and pre-committed [I].

2. **Design principle: groups are price-takers inside quantity envelopes [I].**
   - **Budgets come from the optimizer.** C1's here-and-now program (H) yields group budgets: commitment pacing, NAV envelope, liquidity-at-risk by horizon, CVaR contribution and leverage. Each is an aggregate of the solution. Transfer prices are the program's duals.
   - **Prices alone cannot decentralize.** In many cases "there exist no prices which will lead divisions to make independent decisions that are optimal" (Baumol & Fabian 1964) [S]. Hence a hybrid: quantity envelopes for the plan, dual prices for marginal proposals and for buying capacity beyond the envelope.
   - **[I-calc] Synthetic example.** Eight strategies, two binding rows (crisis 12-month liquidity at 1.83%, CVaR at 0.81%):
     - groups facing the duals reproduce the central allocation to within 10⁻⁵ $bn;
     - envelope bands of ±$0.8–1.3bn cost under $5m a year each;
     - coupling through the shared liquidity row makes deviation 1.1–3.5× more costly than each group's own curvature suggests.

3. **Liquidity transfer pricing, imported from banking and derived from duals [S/I].**
   - **The template.** BCBS Principle 4 (2008), the CEBS liquidity cost-benefit allocation guidelines (27 Oct 2010) and FSI (2011) set out the practice:
     - charge on the liquidity tenor;
     - charge committed lines for contingent liquidity;
     - "compensate the providers of liquidity and charge the users";
     - have the board approve the methodology;
     - run price-setting from a unit with no profit target.
   - **ADIC mapping.**
     - Unfunded commitments are committed lines that ADIC has extended to GPs, so they carry a contingent-liquidity charge.
     - The charge is the buffer's carry: funding-basket return minus HQLA yield, default 3.0% a year per $ of stressed draw [I].
     - Cash-generative books and the tail hedge earn credits for their stressed inflows.
   - **Two price sets.**
     - *Decision prices* are today's duals. They drive SELL/HOLD/REFINANCE/LEVER.
     - *Performance charges* are locked at origination ("vintage FTP"). Treasury holds the repricing mismatch, so groups are not punished for legacy books when prices spike.

4. **Risk charges [S/I].**
   - Euler allocation of a homogeneous risk measure (CVaR) gives additive group risk budgets and RAROC/EVA-style hurdles (Tasche 2008; Stoughton & Zechner 2007).
   - Liquidity metrics such as the path-maximum deficit are not homogeneous. They get marginal dual charges plus an explicit unallocated residual, consistent with verifier finding 11-R6 [S\*].

5. **Forecasts from interested parties: proper scoring is not enough [S/I].**
   - **The problem.** When a forecaster has a stake in the decision the forecast drives, standard scoring rules stop being proper. Compensation must offset that stake (Boutilier 2012) [S].
   - **A simple model [I].** With a quadratic score, the optimal inflation is $\delta^*=bZB'/(2s)$. It rises with how far pay or prestige depends on budget size ($b$), with the credibility weight ($Z$) and with the budget's sensitivity to the forecast ($B'$). It falls with the strength of scoring ($s$).
   - **Evidence [S].**
     - Executives' 80% intervals contained realized market returns only 36% of the time (Ben-David, Graham & Harvey 2013). That implies intervals about 2.7× too narrow [I-calc].
     - In a conglomerate study, all unit managers systematically over-budgeted capital expenditure (Glaser, Lopez-de-Silanes & Sautner 2013; wording from the abstract on the RePEc/IDEAS page, §10 #9).
     - Budget-linked pay invites misreporting (Jensen 2003).
   - **Design.**
     - Elicit P10/P50/P90. Quantiles are elicitable; CVaR is not (Gneiting 2011).
     - Score with the weighted interval score (Bracher et al. 2021).
     - Estimate selection-corrected biases by group and strategy.
     - Feed the credibility weight $Z$ into stream 07's fusion.
     - Shadow-track declined deals.
     - Decouple pay from budget size.
   - **[I-calc] Cost of inflation.** One group inflating its forecast by 200 bp:
     - with raw forecasts driving budgets, it gains $2.1bn and crowds others out by $2.3bn;
     - at Z = 0.4 the crowding-out falls to $0.7bn and the deadweight loss from $21m to $3.7m a year;
     - the loss scales roughly with Z².

6. **Peer practice converges on central capital allocation with delegated selection [S].**
   - **CPP Investments.**
     - Total Fund Management designs targets and capital allocations "in conjunction with the CIO".
     - Departments act within delegated approval authorities and risk limits, and a Balancing Portfolio fills exposure gaps.
     - Incentives weight total fund, department and individual 30/30/40 (50% total fund for senior management). The total fund is measured over five years.
     - In FY2024 the five-year dollar value-added was −C$63.7bn, which zeroed the value-added multiplier.
   - **CalPERS.**
     - At first reading on 17 Nov 2025, staff proposed a 75/25 Reference Portfolio and a 400 bp active risk limit, replacing 11 asset-class benchmarks with one.
     - Trade press reports the framework effective 1 Jul 2026.
   - **Others.**
     - NZ Super's Reference Portfolio sets "hurdles" net of all costs.
     - GIC moved to a three-group Strategic Portfolio from 2026.
     - NBIM caps variable pay at 100% of fixed pay and defers at least 50% for three years or more, indexed to the fund's return.
     - Harvard Management Company tied pay to the whole endowment in 2017.

7. **Internal transfers are relabelings [I/S].**
   - Total-portfolio liquidity changes only by fees.
   - Price each transfer against an independent market test. Analogues: Rule 17a-7's "independent current market price"; ERISA's cross-trade conditions; the "market terms" test of Federal Reserve Act §23B; ILPA's fairness opinion or partial third-party sale.
   - Book both legs at fair value. Any wedge is a centre item, never group alpha.

8. **IC norms [I].**
   - The total portfolio is the decision unit.
   - Groups own sourcing, selection and execution inside their envelopes.
   - Requests beyond the envelope are priced and escalated.
   - Calibration is shown as *information value* against each group's own reference class: selection-adjusted, multi-year, and never as a league table.

---

## 2. Core concepts and theory

### 2.1 ADIC as an internal capital market

| ICM concept | ADIC counterpart |
|---|---|
| Headquarters (HQ) | TPA team, optimizer, IC, CIO/CRO |
| Divisions | Seven groups: PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets, Private Credit, Overlay |
| Division managers' private benefits | AUM, headcount, GP access, deal flow, prestige |
| External capital market | Secondary market, NAV and fund-finance lenders, owner transfers |
| Value of the ICM | Redeploying liquidity and risk capacity across groups without paying secondary discounts |

**Theory [S].**
- **Winner-picking.** HQ creates value by "winner-picking", and internal capital markets may work better in relatively focused firms (Stein 1997).
- **Socialism.** Rent-seeking managers are paid off through "preferential capital budgeting allocations", which yields socialism (Scharfstein & Stein 2000).
- **Diversity.** Misallocation rises with the diversity of investment opportunities, in a 1979–93 panel of US diversified firms (Rajan, Servaes & Zingales 2000).
- **Cash-flow pass-through.** A segment invests out of other segments' cash flow, but less than out of its own. The sensitivity does not depend on whether its opportunities are better (Shin & Stulz 1998).
- **Agency.** Unrelated conglomerate segments are less sensitive to Tobin's Q than stand-alone firms, mainly by under-investing in high-Q industries. The gap is larger where top management owns little equity (Ozbas & Scharfstein 2010).
- **Oil shocks.** In 1986, oil companies cut non-oil investment by significantly more than their industries' median firms. The decline was concentrated in units the parent had subsidized in 1985 (Lamont 1997).

**ADIC translation [I].**
- *Socialism* shows up as pro-rata pacing cuts in a DPI drought, and as commitment budgets treated as entitlements.
- *Winner-picking* means redeploying dry powder to Secondaries and Capital Solutions when discounts and structured yields widen (context §1A, item 5).
- *Lamont-type propagation* runs from the owner's oil-linked distribution demand into every group's budget. This is why budget rules must be state-contingent and pre-committed rather than negotiated in a crisis.

### 2.2 Influence activities and the case for rigidity

- **Lobbying [S].** When decisions mainly redistribute among employees, people waste effort lobbying whoever has discretion. Efficient design limits "the discretion of decision makers" (Milgrom 1988).
- **Decline [S].** The possibility of decline creates extra influence costs in multi-unit firms (Meyer, Milgrom & Roberts 1992).
- **Practice [S].**
  - Using data on more than 1,000 CEOs and CFOs, capital allocation leaned on "gut feel" and the division manager's reputation. Internal politics and support for weaker divisions mattered in European and Asian firms (Graham, Harvey & Puri 2015).
  - More powerful unit managers captured larger shares of cash windfalls and raised investment about 40% more than less powerful peers (Glaser et al. 2013; RePEc/IDEAS abstract page, §10 #9).

**For ADIC [I].**
- Influence costs peak in the group facing structural decline. Today that could be primary PE in a distribution drought.
- Remedies:
  - published budget formulas;
  - changes that require new evidence, not advocacy;
  - group heads present but do not vote on their own budgets;
  - every override logged.

### 2.3 Mechanism design for capital budgeting

**Theory [S].**
- **Budgeting under private information.** Decentralized information and incentive problems produce under-investment when capital productivity is high and over-investment when it is low (Harris & Raviv 1996). The structure "initial budget, then requests for more that trigger audits" is that paper's mechanism as I recall it [M].
- **Hurdles above the cost of capital.**
  - With private information, the optimal rule uses a hurdle "strictly in excess of the cost of capital", trading capital rationing against slack (Antle & Eppen 1985).
  - In practice, firms' hurdle rates are about twice their cost of capital, partly to ration scarce managerial capacity (Jagannathan, Matsa, Meier & Tarhan 2016).
- **RAROC and EVA.** Optimal mechanisms map to EVA-based pay and RAROC-based measurement with position limits. "Hurdle rates reflect capital allocation through a division-specific capital structure" (Stoughton & Zechner 2007).
- **Groves-type evaluation.** Evaluate each manager on the division's *contribution to firm profit*, net of the reported effect on other divisions. Honest reporting is then the best choice whatever others report (Groves & Loeb 1979; Groves 1973).
- **Plan targets.** Under piecework rewards, managers argue expected performance is low to secure easy targets. The Soviet reform tied bonuses to both the plan and its fulfilment (Weitzman 1976). Targets based on past performance create the ratchet effect (Weitzman 1980).
- **Forecast contracts.** For forecast contracts, competition between agents is worth much more than self-screening (Osband 1989).
- **Soft information.** Hierarchies do well when information can be hardened. Decentralization wins when it is soft (Stein 2002).
- **Delegation.** "Decentralization can dominate centralization" even when coordination matters greatly (Alonso, Dessein & Matouschek 2008).

**Synthesis for ADIC [I].**
- Centralize the coupled resources: liquidity, risk, leverage and the denominator. Decentralize sourcing and selection, where soft information lives.
- Hurdles should be the *true* shadow prices. Correct forecast optimism in the forecast (stream 07). Do not also inflate the hurdle à la Antle–Eppen, or the same bias is penalized twice.

### 2.4 Prices, quantities and decomposition

Write the group-indexed program as

$$\max_{x}\ \sum_{g}\sum_{i\in g}V_i(x_i)\quad\text{s.t.}\quad \sum_{g}\sum_{i\in g}a^k_i(x_i)\le b^k\ \ (k\in\mathcal K),\qquad x_i\in X_i .$$

$\mathcal K$ holds the liquidity rows (by horizon and scenario), the CVaR budget, leverage, the private-share cap and the IG + cash floor.

The Lagrangian separates by group:

$$\mathcal L=\sum_g\Big[\sum_{i\in g}\big(V_i(x_i)-\textstyle\sum_k y_k\,a^k_i(x_i)\big)\Big]+\sum_k y_k b^k .$$

At the optimal duals $y^*$, group $g$'s subproblem is "maximize value net of transfer charges $\sum_k y^*_k a^k_i$".

**Three caveats [S/I].**
1. **Non-uniqueness.** If $V_i$ is linear, groups are indifferent at $y^*$ across many plans (Baumol & Fabian 1964). [I-calc] E3: two strategies with equal economics both show zero reduced cost at the liquidity dual, so any split is optimal.
2. **Integer actions.** Discrete actions have no duals. Fix the integers and re-solve for prices, or use Everett's generalized multipliers [S\* 08].
3. **Locality.** Duals are local. Lumpy proposals need with-and-without re-solves.

Hirshleifer (1956) set the classic benchmark: transfer at marginal cost, or at market price when a competitive outside market exists [M for content; DOI checked].

### 2.5 The bank funds-transfer-pricing (FTP) template

- **BCBS Principle 4 [S].** A bank should incorporate liquidity costs, benefits and risks in internal pricing, performance measurement and new-product approval "for all significant business activities (both on- and off-balance sheet)". This aligns business lines' risk-taking with the liquidity risk they create for the bank as a whole.
- **CEBS guidelines, 27 Oct 2010 [S].**

  | Rule | Content |
  |---|---|
  | Two cost components | Direct funding cost plus indirect liquidity costs: mismatch cost on the *liquidity* tenor (not the interest-rate tenor), contingent liquidity cost including the buffer, and other costs |
  | Approval | Board approves the methodology; ALCO-type body approves "at least annually" (¶6) |
  | Independence | Independent control (¶8); the price-setting function "should be service-oriented and not have a profit target" (¶10) |
  | Use | Prices used for pricing, performance measurement and new products; incentive overrides need separate formal approval (¶9) |
  | Users and providers | "compensate the providers of liquidity and charge the users" (¶13) |
  | Committed lines | Charged for the liquid funds they require; once drawn, charged at the expected maturity (¶17) |
  | Contingent costs | Allocated to the units that generate them (¶20) |
  | Marginal cost | Prices reflect marginal cost, with the contingent element recalculated as the buffer changes (¶25) |
  | Buffer cost | Funding cost of the buffer plus the opportunity cost of low-yield liquid assets (Annex 2) |
  | Practice | One surveyed bank had each division run its own stress test, including undrawn commitments, and charged buffer cost by division (Annex 1) |

- **FSI 2011 [S].** In a survey of 38 large banks in nine countries, the most striking poor practice was not attributing liquidity costs at all. Others used a single average rate. Recommended practice is marginal cost matched to maturity, charging expected contingent-liquidity usage, run centrally by treasury.

### 2.6 Risk-capital allocation

- **Euler allocation [S].**
  - For a positively homogeneous measure $\rho$, Euler's theorem gives $\rho(x)=\sum_i x_i\,\partial\rho/\partial x_i$. The Euler principle "has been adopted by many financial institutions" (Tasche 2008).
  - For CVaR, the contribution is $E[L_i\mid L\ge \mathrm{VaR}_\beta]$.
  - Euler is the allocation consistent with marginal (RORAC) performance measurement; that statement is from the paper body [M].
- **Credit-quality view [S].** Marginal default values give "a full and unique allocation of risk capital" (Erel, Myers & Read 2015).
- **Pricing unhedgeable risk [S].** Firm-level risk management should affect how unhedgeable risks are priced (Froot & Stein 1998). For ADIC, this is why hurdles depend on the fund's own state through $\lambda_R$.
- **Limits [S\*].** The path-maximum deficit is not homogeneous, so Euler contributions do not add up (verifier 11-R6).

### 2.7 Forecasting under budget stakes

- **Proper scoring rules [S].** Under a proper rule, honest reporting is optimal (Brier 1950; Savage 1971; Gneiting & Raftery 2007).
- **Elicitability [S].** Point forecasts must name the functional: mean, quantile or expectile. Quantiles are elicitable through generalized piecewise-linear scores, but conditional value-at-risk "is not elicitable" (Gneiting 2011). *Implication:* ask groups for P10 and P90, never for an expected shortfall to be scored.
- **Interval scores [S].** The interval score and weighted interval score (WIS) are proper for interval and quantile formats. WIS approximates the CRPS (Bracher, Ray, Gneiting & Reich 2021).
- **Decision stakes [S].** If the expert's utility depends on the decision, compensation rules must offset that utility. Where the stake is unknown, the misreport can only be bounded (Boutilier 2012). A related impossibility: honest elicitation for decisions needs randomized decision rules with full support (Chen, Kash, Ruberry & Shnayder 2014) [S; abstract confirmed in the G8 literature review]. The underlying problem is strategic communication: a better-informed sender reveals only which element of a partition its information lies in, and in the most informative equilibrium, signalling is more informative the more similar the sender's and receiver's preferences (Crawford & Sobel 1982) [S; abstract via OpenAlex, DOI 10.2307/1913390].
- **Weitzman scheme as a quantile score [I-calc, derived].**
  - Bonus: $B=\bar B+\beta(\hat y-\bar y)+\alpha(y-\hat y)^+-\gamma(\hat y-y)^+$ with $\alpha<\beta<\gamma$.
  - Setting the derivative of expected bonus to zero: $\beta-\alpha(1-F(\hat y))-\gamma F(\hat y)=0$, so $F(\hat y^*)=(\beta-\alpha)/(\gamma-\alpha)$.
  - With (0.2, 0.6, 1.0) the manager reports the median; E6 checks this numerically. A plan bonus of this shape is a proper quantile score and directly counters sandbagging.
- **Selection and practice [S].**
  - Choosing the alternative with the highest estimate causes post-decision disappointment even with unbiased estimates (Smith & Winkler 2006, "optimizer's curse").
  - Training, teaming and tracking improved forecasters' calibration and resolution (Mellers et al. 2014).

---

## 3. Methods, models and trade-offs

### 3.1 How to set group budgets

| Mechanism | How it works | Strengths | Weaknesses | Verdict [I] |
|---|---|---|---|---|
| Fixed SAA weights by group | Policy weights with ranges | Simple; legible | Ignores coupling and state; invites entitlement and socialism | Reject as primary |
| Pure internal market | Groups bid for liquidity and risk at posted prices | Decentralized; reveals willingness to pay | Non-uniqueness (Baumol–Fabian); price whiplash; gaming of resource metrics | Use only at the margin |
| Optimizer quantity envelopes | Budgets = resource use at $x^*$ | Coherent with total-portfolio optimum | Rigid; loses soft information if bands are tight | Core |
| **Hybrid: envelopes + dual prices + audited requests** | Envelope ± no-regret band; purchases beyond it at the dual price via Tier B | Combines Harris–Raviv-style audits with price signals | Needs price governance | **Adopt** |
| State-contingent rule distilled from P | E.g. pacing multiplier as a function of $(\ell_t,\text{regime})$ | Pre-committed; lowers influence costs | Rules drift from the optimum between reviews | Adopt for pacing (C1 D2) |

### 3.2 Transfer-price families

| Family | Additive? | Incentive-compatible at the margin? | Stability | Use [I] |
|---|---|---|---|---|
| Administrative FTP curve | Yes | Only if calibrated to marginal cost | High | Fallback, and floor when duals are about 0 |
| **Dual-based (LP/QP/stochastic program)** | Yes, for linear rows | Yes, locally | Low unless smoothed | **Decision prices** |
| Euler marginal risk | Yes, for homogeneous $\rho$ | Yes (RORAC-consistent) | Medium (tail noise) | Risk budgets and charges |
| With/without re-solve | No | Yes, for lumpy items | Medium | Proposals above about 0.25% of NAV |
| Shapley / Aumann–Shapley | Yes (Shapley); Aumann–Shapley equals Euler for homogeneous measures | Fair, but not marginal | High | Attribution of group interactions |
| Vintage-locked FTP | Yes | Fair for performance; wrong for decisions | High | **Performance charges** |

### 3.3 Forecast scoring and credibility

| Component | Options | Recommendation [I] |
|---|---|---|
| Format | Point; P10/P50/P90; full distribution | **P10/P50/P90** plus 4- and 8-quarter cash flows and exit timing; full distributions for overlay P&L |
| Score | Squared error (mean only); pinball; interval score; WIS; CRPS; log score | **WIS** (K = 1, α = 0.2) plus a coverage test; Brier for binary events |
| Bias model | Per-group averages; hierarchical model; EMOS | Hierarchical Bayesian model, partial pooling by group × strategy × author (complements stream 07's EMOS) |
| Selection | Approved deals only; inverse-propensity weighting; shadow-tracking of declined deals | **Shadow-track declined deals** plus IPW; never estimate bias on approved deals alone |
| Weight in fusion | Equal; Bühlmann $Z=n/(n+k)$; stacking | Bühlmann $Z$ with clustered $n_{\rm eff}$, shrunk toward stream 07 defaults |
| Display | League tables; anonymized; information value | **Information value against own reference class**, multi-year, with uncertainty bands |

### 3.4 Attribution

- **Return.** DVA against each holding's funding basket, net of transfer charges (CPP measures departments against public-index blends [S]).
- **Risk.** Euler contributions on CVaR or volatility.
- **Liquidity.** Dual-weighted stressed outflows, with an unallocated residual.
- **Interactions.** Exact Shapley across 7–8 groups: $2^8=256$ coalitions, so it is cheap.
- **Trade-off.** Shapley is fair but not marginal. Duals are marginal but not fair for lumpy legacy books [I].

---

## 4. Empirical evidence and current market data

| Topic | Evidence | Source and date |
|---|---|---|
| ICM misallocation | Funds flow to least efficient divisions; worse with diversity (US firms, 1979–93) | Rajan, Servaes & Zingales 2000 [S] |
| Cross-subsidy | Segment investment depends on other segments' cash flow, not on relative opportunities | Shin & Stulz 1998 [S] |
| Oil-shock propagation | Oil firms cut non-oil capex by more than industry medians in 1986, mostly in previously subsidized units | Lamont 1997 [S] |
| Agency | Unrelated segments less sensitive to Q; worse with low management ownership | Ozbas & Scharfstein 2010 [S] |
| Power and over-budgeting | All unit managers over-budget capex; powerful managers obtain larger shares of cash windfalls and raise investment about 40% more than less powerful peers | Glaser et al. 2013 [S; RePEc/IDEAS abstract page, §10 #9] |
| ICM in crises | Internal capital markets more valuable in 2007–09 | Kuppuswamy & Villalonga 2016 [S] |
| Hurdle inflation | Hurdles about 2× cost of capital | Jagannathan et al. 2016 [S] |
| Miscalibration | 13,300+ forecasts; 80% intervals cover 36% of outcomes | Ben-David, Graham & Harvey 2013 [S] |
| Manager selection | 3,400 plan sponsors (1994–2003) hire after large excess returns; no positive post-hire excess returns; post-firing returns about zero | Goyal & Wahal 2008 [S] |
| Co-investment | Co-investments under-perform their funds; solo deals out-perform (7 institutions, 20 years) | Fang, Ivashina & Lerner 2015 [S] |
| Co-investment (contrary) | No adverse selection; similar gross returns; net out-performance | Braun, Jenkinson & Schemmerl 2020 [S] |
| Private debt | Typical fund earns an insignificant abnormal return net of fees, but a positive one against debt-only benchmarks (it carries equity risk) | Erel, Flanagan & Weisbach 2024 [S] |
| PE deal metrics | 79 investors (>$750bn) rely mainly on IRR and multiples | Gompers, Kaplan & Mukharlyamov 2016 [S] |
| TPA adoption | 26-fund peer study: 35% (9) adopted TPA, 54% anticipating; SAA users halved since 2017 | Filbeck & Bok, Oct 2025 [S] |
| TPA prevalence | Top-100 asset owners: 8 TPA, 66 SAA, 26 hybrid | Urwin & Hayman, Jul 2026 [S] |
| TPA barriers (N=10) | Culture 5; team coordination 4; governance 4; identifying market factors in competition for capital 3 | Urwin & Hayman 2026 [S] |
| TPA performance claims | +1.3% a year (TAI, 26 funds); about 150 bp (Garmash 2025). Adopters are larger, better governed and alternatives-heavy, so not causal | Urwin & Hayman 2026; Filbeck & Bok 2025 [S] |
| Bank FTP practice | 38 banks in 9 countries; missing or single-rate attribution common | FSI 2011 [S] |
| Secondary pricing | LP portfolios at 87% of NAV in H1 2026; buyout 91%; tail-end funds 25%+ discount; deferrals in 26% of LP sales | Jefferies, Jul 2026 [S\* 08] |
| Distributions | PE distributions about 14% of NAV, below 15% for four years; LP distribution yield about 10% in H1 2026 vs 25% average since 2001 | Bain 2026 [S\* 02]; Jefferies [S\* 08] |
| Financing | NAV-facility target margins 4.8% secured, 6.1% recourse-light | Rede, Jun 2026 [S\* 08] |
| Rates | SOFR 3.89% on 15 Oct 2026 | FRED [S\* 08] |
| Stress draw priors | Basel LCR40.64 drawdown on undrawn committed facilities: 40% to banks and other FIs (credit), 100% to SPVs | Basel Framework [S\* 08] |
| Cost of capital anchor | Solvency II cost-of-capital rate 4.75% from 30 Jan 2027 (was 6%) | Directive (EU) 2025/2 [S\* 08] |

**Reading [I].**
1. The academic ICM evidence is about corporations. Its mechanisms (soft information, private benefits, propagation) carry over to an asset owner, but its magnitudes do not.
2. Group forecasts at ADIC are made by people whose budgets depend on them. Every documented bias points toward optimism on returns and timing, with too-narrow ranges.
3. The DPI drought raises the shadow price of liquidity and the value of internal reallocation together, which is exactly when socialism is most tempting.

---

## 5. Peer practice and case studies

**CPP Investments (FY2024 annual report; Apr 2026 TPA paper) [S].**
- **Structure.**
  - Total Fund Management designs strategic and tactical targets and "capital allocations to investment strategies in conjunction with the CIO". It manages exposures, leverage and liquidity, and runs the Balancing Portfolio as a completion portfolio.
  - The CIO's annual strategy reviews translate into each strategy's "capital budget and expected growth trajectory".
  - Departments propose and resize strategies "within their delegated approval authorities, mandates and risk limits". "Active strategies are never used to simply bridge a gap"; the Balancing Portfolio does that.
- **Committees.** The CEO-chaired ISRC oversees the Total Portfolio Investment Framework, supported by:
  - the Portfolio Execution Committee (CIO chair): new investments and dispositions;
  - the Portfolio Strategy Committee (chaired by the head of Total Fund Management): portfolio design targets;
  - the Investment Risk Committee (CRO chair): market, credit, liquidity and leverage limits.
- **Benchmarks.** Departments are judged mainly on net value-added against public-index blends. Private equity uses a *levered* developed-market large/mid-cap equity index, which is a funding basket in the deck's α\* sense.
- **Pay.** All employees except senior management: total fund 30% (value-added and total return, equally weighted, five-year trailing), department and group 30%, individual 40%. Senior management: 50/50. Each factor pays 0–2× target. Senior employees defer part of the award over three years, notionally invested in the fund.
- **FY2024 outcome.** The five-year absolute return of 7.73% beat its 6.23% target (multiplier 1.24×). Five-year DVA was −C$63.7bn against a +C$10.1bn target (0×), giving a total-fund multiplier of 0.62. A relative component can zero out bonuses for years, which is a retention risk.
- **Liquidity.** The 10-day liquidity coverage ratio was 3.8 against a 1.0 minimum (31 Mar 2024). It feeds a five-year liquid-capital target.
- **TPA paper (via Pension Pulse).** Strategies are judged on "alpha excluding all costs", adjusted for liquidity consumption and balance-sheet capacity. Leverage is a "balance sheet risk stabiliser".

**CalPERS (Investment Committee item 5a, 17 Nov 2025) [S].**
- Replace SAA with "a Reference Portfolio and Active Risk Limit": 75/25 equities and bonds, 400 bp limit, discount rate kept at 6.8%.
- Current active risk is about 230 bp; the expected operating range is 250–350 bp. Consolidating the old SAA ranges gave about 450 bp.
- Eleven asset-class benchmarks become one total-fund benchmark.
- Workstreams include building "a cohesive active risk budgeting framework" that synthesizes "cost of liquidity", and a treasury framework for liquidity and leverage.
- The Board's oversight role is unchanged.
- A 1 Jul 2026 trade brief reports TPA effective that day, with a CIO value-add aim of 50–60 bp. The same aim appears in the CIO's interview quote in Urwin & Hayman 2026 [S].

**NZ Super [S].** The Board sets a passive Reference Portfolio (since 2010; 75% global equity, 5% NZ equity, 20% fixed income, 100% NZD-hedged). It sets "hurdles" for active investments and benchmarks value-add "net of all costs". The Board governs risk allocation; management adds value.

**GIC [S].** From 2026 the Strategic Portfolio (equities, fixed income, real assets) "represents the Client's risk appetite". The GIC Portfolio aims to beat it "within approved risk parameters". The 20-year real return (3.4%; 5.6% USD nominal to 31 Mar 2026) is the primary metric. Risk is managed in three layers: policy portfolio, 10-year strategy buckets and 3–5-year overlays, with a CIO-office overlay for funding (Filbeck & Bok 2025; this description predates the 2026 refresh).

**Future Fund [S].** It avoids "my portfolio" and "benchmarks", is organized in four "pillars" rather than asset classes, and runs a portfolio-integration team. It still reports a "gravitational pull" back to SAA under stress (Filbeck & Bok 2025).

**Other organizational patterns [S].**
- TCorp and Railpen run matrixed teams competing on marginal portfolio impact. Railpen softened its reference portfolio after tracking error pulled behaviour back toward SAA (Filbeck & Bok 2025).
- Urwin & Hayman (2026) report that the IC "operationalizes competition for capital". The reference portfolio "guides the competition for capital framework by providing the notional funding for deals". Remuneration is moving toward "more flexible, balanced, and judgment-driven" schemes with "less volatility in incentives".

**NBIM pay principles (amended 21 May 2026) [S].**
- Variable pay reflects the individual, the unit and the fund's relative return, measured over "at least two years".
- At least 50% is deferred over three or more years and adjusted with the fund's absolute return.
- The cap is 100% of fixed pay (exceptions up to 200%). The Leader Group gets no variable pay.
- Variable pay is cut or stopped when relative return is "severely negative".

**Harvard Management Company (Jan 2017) [S].** Moved to a "generalist model" and tied pay to the whole endowment instead of siloed benchmarks.

**Bank FTP case (CEBS Annex 1) [S].** In four of five surveyed banks the pricing unit was a cost centre. Three of five allowed incentive adjustments to prices. Prices were updated daily (1), weekly (3) or monthly (1).

---

## 6. Design implications for the ADIC framework

### 6.1 Organizing principle and roles [I]

| Role | Owns | Peer analogue |
|---|---|---|
| Board | Reference portfolio, risk and liquidity appetite, distribution policy, FTP methodology (annual), pay design | CalPERS "Formal Total Fund Risk"; CEBS ¶6 |
| Total Portfolio Committee (TPC; CIO chair, CRO, head of TPA/Treasury; group heads present but recuse on their own budgets) | Quarterly budgets and prices; contingent "if-then" budgets; over-envelope approvals | CPP PSC/ISRC |
| TPA and Treasury desk (cost centre, no profit target) | Runs H/P, computes duals, publishes FTP, holds vintage mismatch and buffer P&L, runs balancing and overlay completion | CPP TFM; CEBS ¶10 |
| Groups 1–7 | Sourcing, selection, execution, monitoring, forecasts (P10/P50/P90), within envelope | CPP departments |
| Validator / CRO office | Forecast registry integrity, score computation, model validation, transfer pricing committee | CPP IRC |

### 6.2 Group state and decision variables

**State per group $g$ and quarter $t$:**
- $NAV_{g,t}$ (reported and economic);
- unfunded $U_{g,t}$ by vintage;
- stressed outflow and inflow profiles $O^{s}_{g,h}$, $I^{s}_{g,h}$ for horizons $h\in\{30\text{d},12\text{m},24\text{m}\}$ and scenarios $s$;
- Euler CVaR contribution $RC_g$;
- leverage used $B_g$;
- envelope utilization;
- vintage-FTP ledger;
- forecast-registry state (bias $\hat\beta_g$, dispersion multiplier $\hat\kappa_g$, credibility $Z_g$, effective sample size $n_{{\rm eff},g}$);
- internal-transfer ledger.

**Decisions:**
- envelopes: pacing $P_g$, NAV band $[N^{lo}_g,N^{hi}_g]$, liquidity budgets $\Lambda_{g,h}$, risk budget $R_g$, leverage $B_g$;
- contingent budgets $P_g(s)$;
- within-group asset actions, from 08 and C1.

### 6.3 Deliverable (i): group budgets as optimizer outputs

1. **Solve and aggregate.** Solve H (C1) across its 10 sample-average-approximation (SAA) replications. Each envelope is the group's share of every coupling row at the mean solution:

   $$\Lambda^{k}_{g}=\sum_{i\in g}a^{k}_{i}(x^*_i)\qquad(k=\text{liquidity rows, CVaR, leverage, pacing}).$$

2. **No-regret band.** Fix $x_g$ at $x^*_g\pm d$, let the other groups re-optimize, and estimate the effective curvature $H_g=2\,\overline{\text{loss}}/d^2$. The band is

   $$\delta_g=\sqrt{2\varepsilon/H_g},\qquad \varepsilon=\$5\text{m a year (default)}.$$

   - **Budget elasticity.** Group $g$'s budget elasticity is $\partial x_g/\partial\alpha_g=1/H_g$. Show it to groups as "a credible +100 bp of fused α\* buys about \$X bn of budget".
   - **[I-calc] E10.**

     | Group | $x^*$ ($bn) | Band ($bn) | Curvature vs own | +100 bp buys ($bn) |
     |---|---|---|---|---|
     | PE | 1.00 | ±1.06 | 3.5× | 1.13 |
     | SEC | 2.07 | ±1.11 | 1.35× | 1.24 |
     | COI | 0.96 | ±1.22 | 1.7× | 1.48 |
     | CAP | 1.80 | ±0.83 | 1.5× | 0.68 |
     | OVL | 0.84 | ±1.33 | 1.1× | 1.78 |

     A check: E4 predicts ΔPE = 0.008/0.00883 = 0.91bn against 0.91bn re-solved.

3. **State-contingent rules (distilled by P).**

   $$P_{g,t}=P^*_g\cdot\Pi_{[m^{lo}_g,m^{hi}_g]}\big(1-\eta_g(\ell_t-\bar\ell)/\bar\ell\big).$$

   - $\eta_g>0$ for PE funds and co-investment.
   - $\eta_g<0$ for Secondaries and Capital Solutions, whose opportunities widen when liquidity is scarce. Their extra crisis capacity is pre-approved as **contingent budgets**: if the secondary discount exceeds 20% and the Tier-1 gate is green, release $X$.
4. **Purchases beyond the envelope.** Up to +20% at the current dual price (Tier B). Larger amounts go to Tier A.
5. **No ratchet.** Unused envelope is released without penalty. Next year's envelope comes from the re-solve, never from this year's usage (Weitzman 1980).

### 6.4 Deliverable (ii): transfer prices from optimizer duals

**Decision price per $ of holding or proposal $i$** (current duals, smoothed for publication):

$$\text{charge}_i=\underbrace{\sum_{h,s}\mu_{h,s}\,a^{h,s}_i}_{\text{liquidity}}+\underbrace{\lambda_R\,\frac{\partial\,\mathrm{CVaR}}{\partial x_i}}_{\text{risk}}+\underbrace{\lambda_{Lev}\,b_i}_{\text{leverage}}+\sum_k\rho_k\,\Delta\text{Floor}^k_i-\underbrace{\sum_{h,s}\mu_{h,s}\,c^{h,s}_i}_{\text{provider credits}}.$$

- $a$ is stressed consumption and $c$ is stressed inflow (contractual coupons and amortization, hedge payoffs), both haircut.
- Net α\* for the IC is $\alpha^*_i-\text{charge}_i$.

**Term structure.** The liquidity premium is $\ell_{s,t}=\mu_{s,t}/(\pi_{s,t}-\mu_{s,t})$ (stream 08). Define the curve $LP(\tau)=\tau^{-1}\sum_{t\le\tau}E[\ell_t]$, and charge each asset on its liquidity tenor $\tau_i$: the cash-weighted remaining life of its projected distributions (stream 04). Per CEBS footnote 2, this is the liquidity tenor, not the rate tenor.

**Contingent liquidity charge on unfunded commitments (CEBS ¶17, ¶20; Annex 2):**

$$CLC_g=c_{buf}\sum_{h}\omega_h\,O^{stress}_{g,h},\qquad c_{buf}=E[r_{FB}]-r_{HQLA}.$$

- Default $c_{buf}=3.0\%$: a funding basket at about 7% minus SOFR of 3.89% [S\*], rounded [I].
- Default stressed 12-month draw on unfunded PE: 30% (range 25–40%; Basel's 40% for committed facilities to financial institutions as a conservative prior [S\*]).
- *Order of magnitude [I]:* $38bn of unfunded × 30% × 3% ≈ $0.34bn a year. That is the carry cost of the dry powder the IC must see.

**Credits.**
- Private Credit and Capital Solutions earn $c_{buf}$ on stressed contractual inflows.
- Overlay margin consumption is charged.
- The tail hedge earns its crisis-payoff and CVaR credits.
- [I-calc] E1 credits the hedge 895 bp per $ of premium, against an expected carry of −4,500 bp. It would enter only at a crisis dual of 10.85%; the actual dual is 1.83%.
- E9 break-even: the forced-sale discount at which the hedge pays its way is $d^*=(c-\lambda_R r)/(kp)$. That is 32.8% at a 20% carry, and above 100% (never) at a 45% carry. Tail-hedge sizing must rest on explicit forced-sale and distribution-floor costs (stream 09), not on deployment alpha alone.

**[I-calc] E1 synthetic prices.** Duals: crisis-12m liquidity 1.83%, CVaR 0.81%.

| Group | Charge (bp) | Net α\* (bp) | Budget ($bn) | Crisis-12m liquidity budget ($bn) | CVaR budget ($bn) |
|---|---|---|---|---|---|
| PE | 125 | +25 | 1.00 | 0.55 | 0.30 |
| SEC | 176 | +124 | 2.07 | 1.76 | 0.52 |
| COI | 212 | +38 | 0.96 | 0.96 | 0.34 |
| CAP | 171 | +180 | 1.80 | 1.53 | 0.32 |
| PCR | 141 | −41 | 0 | 0 | 0 |
| OVL opportunistic | 58 | +42 | 0.84 | 0.21 | 0.13 |
| TAIL hedge | −895 (credit) | −3,605 | 0 | 0 | 0 |

At an interior optimum, net α\* equals $q_g x^*_g$: the marginal deal just pays its charges.

**Price governance [I].**
- **Smoothing and collars.** Publish quarterly. Use an EWMA with a two-quarter half-life and a ±50% quarter-on-quarter collar.
- **Floor.** Floor the liquidity price at the buffer carry. Zero duals must never read as "free liquidity"; FSI 2011 called missing attribution the worst practice. Zero duals across all scenarios instead signal an oversized buffer.
- **Which duals.** Use the mixture-weighted duals across C1's model set. Report the dual dispersion across SAA replications.
- **Vintage locking.** Lock performance FTP at origination. Treasury books the difference between locked and current charges.
- **Approval.** The Board approves the methodology annually. Incentive overrides need separate approval (CEBS ¶9).

**Decentralization test.** [I-calc] E2: each group maximizing $\alpha_gx-\tfrac12q_gx^2-\text{charge}_g\,x$ reproduces $x^*$ to within $10^{-5}$ $bn. In a linear problem (E3) prices leave the split indeterminate, so the envelope decides.

### 6.5 Deliverable (iii): per-group forecast scoring and credibility system

**Registry.** A bitemporal, append-only registry (stream 07). Each record holds:
- asset or strategy, group, author, date and horizon;
- the target variable (see the table below);
- P10/P50/P90;
- the conditioning snapshot: underwritten, actual, NAV, regime;
- a flag for whether the forecast supported a budget or proposal;
- for declined deals, a shadow-tracking identifier.

| Group | What it forecasts | Fast-resolving companion | Typical bias prior (median, pp a year; *synthetic* [I]) |
|---|---|---|---|
| PE funds | Forward IRR on nowcast NAV (GP projections, look-through) | 4/8-quarter distributions | −2.0 (optimism on exits and timing) |
| Secondaries | Deal IRR; distribution curve | 4/8-quarter distributions | −1.0 |
| Co-investment | Deal IRR and MOIC (deal models) | Exit timing, EBITDA path | −3.0 (hockey stick; stream 07 case) |
| Capital Solutions | Contracted yield, loss, equity-kicker value | Coupon and covenant events | −1.5 |
| Private Credit | Loss-adjusted net yield | Default and loss events | −1.0 (Erel et al.: equity risk mistaken for alpha) |
| Public Markets | Manager alpha (hedge funds); active return (long-only) | 12-month alpha | −2.0 (Goyal & Wahal return-chasing) |
| Overlay | Opportunistic: 12-month P&L distribution. Hedge: payoff in named scenarios | Monthly P&L; scenario payoffs | −2.0 (backtest overfitting) |

**Scoring.**

$$\mathrm{WIS}=\tfrac{1}{1.5}\big[\tfrac12|y-q_{50}|+0.1\,IS_{0.2}(q_{10},q_{90};y)\big],$$

$$IS_\alpha=(u-l)+\tfrac{2}{\alpha}(l-y)\mathbb 1\{y<l\}+\tfrac{2}{\alpha}(y-u)\mathbb 1\{y>u\}.$$

Skill against the outside view is $S_g=1-\sum\mathrm{WIS}_g/\sum\mathrm{WIS}_{ref}$.

[I-calc] E7: a hockey-stick co-invest forecast (12/20/26%) against a realized 7% scores WIS 0.086, versus 0.023 for the reference class (0/10/20%). Skill is −2.69.

**Bias and dispersion model.**

$$y_j-q_{50,j}=\beta_{g(j)}+\beta_{s(j)}+\beta_{a(j)}+\gamma\,(u_j-a_j)^+ +\varepsilon_j,\qquad \varepsilon_j\sim t_\nu\big(0,\kappa_{g}\hat\sigma_j\big),\qquad \hat\sigma_j=\frac{q_{90,j}-q_{10,j}}{2.563}.$$

- **Dispersion prior.** $\kappa_g$ is lognormal with median 1.75 (range 1.2–2.7). Ben-David et al.'s 36% coverage implies κ = 2.74 for market forecasts [I-calc].
- **Credibility.** $Z_g=n_{\rm eff}/(n_{\rm eff}+k)$ with $k=20$ and $n_{\rm eff}=n/(1+(m-1)\rho)$, $\rho=0.3$ within vintage × regime clusters.
- **Fusion.** The debiased group forecast enters stream 07's fusion with precision scaled by $Z_g/\kappa_g^2$.

**Selection correction.** Estimate bias on *all* registered forecasts. That includes declined deals, shadow-tracked to their outcomes from fund reports or commercial data, plus inverse-propensity weights on approval. Approved-only estimates carry the optimizer's curse (Smith & Winkler 2006).

**Incentive layer [I].** With group utility $U=b\,B(\mu_{post}(f))-s\,E[(f-y)^2]$ and $\mu_{post}=Zf+(1-Z)m$, the first-order condition gives

$$\delta^*=f-E[y]=\frac{bZB'}{2s}.$$

Levers:
- **Make $b$ small.** No pay or status scales with AUM or budget (Jensen 2003). This is the main lever.
- **Make $s$ meaningful.** A forecast-quality KPI, or a Weitzman-shaped plan bonus that elicits the median.
- **Let $Z$ fall automatically** when bias appears. Inflation then becomes self-defeating.
- [I-calc] E5: quartering $b$, or quadrupling $s$, cuts the inflation incentive by 4×. Moving from Z = 1 to Z = 0.4 cuts it by 2.5×.

**Display threshold.** Credibility is shown only when $n_{\rm eff}\ge20$. At $n=20$ the standard error of 80% coverage is ±8.9pp; at 50 it is ±5.7pp; at 100, ±4.0pp [I-calc].

### 6.6 Deliverable (iv): IC presentation and decision-rights norms

**Decision-rights matrix** (it integrates the C4/14 tiers [S\*]):

| Decision | Board | TPC / IC | CIO + CRO (Tier B) | Group (Tier C) | Desk / validator |
|---|---|---|---|---|---|
| Reference portfolio; risk, liquidity and leverage appetite | Approves | Recommends | — | Consulted | Analyses |
| FTP methodology | Approves annually | Recommends | — | Consulted | Builds; independent control |
| Quarterly envelopes and prices; contingent budgets | Informed | **Approves** | — | Presents (recused) | Computes |
| Deals inside envelope and mandate | — | — | — | **Decides** | Logs and scores |
| Beyond envelope, ≤ +20% | — | Informed | **Approves**, priced at dual | Requests | Prices |
| Tier-A items (≥0.25% of NAV, about $0.44bn; discount >10%; LTV +5 pp; hedge budget) | Escalations | **Decides** | Recommends | Proposes | Packs |
| Internal transfers | — | Tier A if ≥0.25% NAV or conflicted | Tier B otherwise | Proposes | Pricing committee |
| Forecast and registry rules; calibration release | — | Informed | Approves | Comply | **Owns** |

**IC pack per proposal [I].**
- α\* against the funding basket;
- charges itemized (liquidity, contingent, risk, leverage, credits) and net α\*;
- raw versus fused forecast and the group's $Z$;
- total-portfolio deltas: P(10% over 10 years), red-event probability, survival months (C1);
- envelope status;
- the asset decision card (stream 08).

**Norms for discussing calibration without destructive politics [I].**
1. Credibility is a *weight on information*, not a grade on people. Show the group's information value in dollars (forecast precision × decision sensitivity), not ranks.
2. Compare each group with its own reference class and its own trend. Never publish league tables across groups.
3. Show scores selection-adjusted, multi-year and with bands. Show "insufficient evidence" below the threshold.
4. Penalize sandbagging as much as optimism. Coverage and width both count.
5. Keep individual-level scores private and show group-level scores at the IC.
6. Hold blame-free forecast post-mortems that feed the memo corpus (deck slide 8).
7. Any member may challenge any group's numbers, but no group may veto another group's proposal. Conflicts are settled through prices and envelopes.

### 6.7 Deliverable (v): internal transfers

| Transfer | Total-portfolio economics | Liquidity treatment | Pricing rule | Approval |
|---|---|---|---|---|
| PE-group fund stake sold to the Secondaries group | Relabeling; fees, GP consent and tax only | **Zero liquidity raised** (−fees) | (1) contemporaneous third-party strip sale (≥20%); (2) ≥2 external bids; (3) fairness opinion (mandatory ≥$250m or if conflicted) | Tier B, or Tier A |
| Capital Solutions lends against an ADIC-held co-investment (holdco or NAV loan) | Internal leverage; no outside cash | Zero (unless refinanced externally) | External lender quote or Rede-type margin band | Tier B; leverage budget |
| Capital Solutions lends to a GP fund in which the PE group is an LP | Partly internal: net cash out = $L(1-s)$ ($s$ = ADIC's LP share); exposure rises in seniority | Counts $-L(1-s)$ | External syndication of ≥50%, or third-party quote | Tier A (conflict) |
| Overlay physical-to-synthetic replacement of long-only | Real liquidity: physical sold for cash; futures added | +proceeds − stressed initial and variation margin buffer | Market prices | Tier C within overlay mandate |
| Secondaries group buys an outside LP stake in a fund the PE group holds | External; concentration rises | Normal | Market | Normal tiers |

**Rules [S/I].**
1. **Pricing analogues.**
   - Rule 17a-7 requires cash settlement at the "independent current market price", no commissions, board procedures with quarterly review, and six-year records [S].
   - ERISA §408(b)(19) requires independent-fiduciary authorization, plans of at least $100m, quarterly reports, written policies and an annual compliance report [S].
   - FRA §23B requires terms "substantially the same, or at least as favorable" as with unaffiliated parties [S].
   - ILPA's 2023 continuation-fund guidance uses a fairness opinion or partial third-party sale as the price check [S\* 05].
   - Fund stakes lack quoted prices, so the market test must be manufactured through strips or outside bids.
2. **Attribution.** Book both legs at fair value $v$. The wedge $(p-v)$ is a centre item. [I-calc] E8: a $1bn transfer at 85% against 90% fair value would otherwise hand $50m of fake alpha to the buyer.
3. **Benefit test.** A transfer must show net total-portfolio benefit: lower fees, better stewardship or mandate fit, net of costs. Pure P&L shifting is prohibited.
4. **Firewall.** A group that may bid cannot supply the reference quote. The Secondaries and Capital Solutions groups' quotes count as *market intelligence* only through the pricing committee.
5. **No window dressing.** No transfers within 30 days of a measurement date without CRO sign-off.

### 6.8 Attribution and compensation

**Attribution identity:**

$$R_P-R_{RP}=\sum_g\underbrace{\Big[\sum_{i\in g}NAV_i(r_i-r^{FB}_i)-FTP^{vint}_g-CLC_g-RC_g+CR_g\Big]}_{DVA_g}+DVA_{TPA}^{\text{budgets, balancing}}+DVA_{Treasury}^{\text{mismatch, buffer}}+\text{residual}.$$

- **Risk.** Euler contributions on CVaR.
- **Liquidity.** Dual-weighted stressed outflows plus the residual.
- **Interactions.** Shapley across groups (deck slide 6 formula).

**Default pay architecture [I].**

| Population | Total portfolio | Group | Individual | Other terms |
|---|---|---|---|---|
| Group heads | 40% (5-year absolute return vs 10% and DVA vs reference) | 35% (vintage-FTP-adjusted DVA vs funding baskets, 5-year) | 25% (≤10 points on forecast quality: WIS skill, coverage) | — |
| CIO / senior management | 50% | 50% department and individual | | CPP mirror |
| All variable pay | | | | ≥50% deferred over 3 years, indexed to total-portfolio return (NBIM/CPP style). Nothing scales with AUM. Overlay hedge staff judged on mandate delivery and total-portfolio contribution, never on stand-alone P&L |

### 6.9 Parameters, calibration targets and data needs

| Parameter | Default | Range | Source |
|---|---|---|---|
| Re-solve / budget cycle | Quarterly / annual | — | C1 D1, D17 [S\*] |
| Envelope tolerance ε | $5m a year per group | $2–10m | [I-calc] |
| Purchase cap beyond envelope | +20% | 10–30% | [I] |
| Price smoothing | EWMA, 2-quarter half-life; ±50% collar | — | [I] |
| Buffer carry $c_{buf}$ | 3.0% | 2–4% | SOFR 3.89% [S\*]; funding-basket 7% [I] |
| Stressed 12m draw on PE unfunded | 30% | 25–40% | Basel 40% prior [S\*]; stream 04 |
| External λ_R anchor | 4.75% | 4.75–6% | Directive (EU) 2025/2 [S\*] |
| WIS spec | K = 1, α = 0.2, w0 = ½, w1 = 0.1 | — | Bracher et al. 2021 [S] |
| Credibility k / correlation ρ | 20 / 0.3 | 10–40 / 0.1–0.5 | [I] |
| κ prior median | 1.75 | 1.2–2.7 | [I]; Ben-David et al. [S] |
| Display threshold | n_eff ≥ 20 | — | [I-calc] |
| Fairness-opinion trigger | ≥$250m or conflicted | — | [I] |
| Tier-A threshold | 0.25% of NAV | — | C4 [S\*] |

**Calibration targets [I].**
- P10–P90 coverage 80% (70–90% acceptable at n ≥ 50).
- Median hit rate 50% ± 7pp at n = 50.
- Group WIS skill > 0.
- Charges reconcile to dual-valued constraint totals plus buffer carry within 5%.
- Envelope utilization 70–100%.
- Peer anchors: operating active risk 250–350 bp (CalPERS); reference-portfolio tracking error 4–5% (CFA guide); LCR minimum 1.0 (CPP).

**ADIC data needs.**
- group mandates, current budgets and delegated authorities;
- pacing history;
- the historical forecast archive with authorship (or a start date for the registry);
- declined-deal list;
- unfunded schedules and stress draws;
- contractual inflows;
- overlay margin history;
- the current pay plan and its legal constraints;
- history of internal transfers;
- the group-to-Treasury reporting lines.

### 6.10 SPECIFICATION CARD

| Item | Specification |
|---|---|
| **Data fields** | holding_id, group_id (1–7), strategy, vintage, NAV_rep/NAV_eco, unfunded, liquidity_tenor τ, stressed outflow/inflow by (h, s), funding_basket_id, Euler CVaR contribution, leverage, vintage_FTP_rate, envelope_id; registry: forecast_id, author, as_of, horizon, target, q10/q50/q90, snapshot(u, a, NAV, regime), decision_link, declined_flag, outcome, resolve_date; transfer: transfer_id, seller/buyer group, p, v, evidence type, fees, approvals |
| **Return / cash-flow equations** | $DVA_g$ identity (§6.8); $\text{charge}_i$ (§6.4); $CLC_g=c_{buf}\sum_h\omega_hO^{stress}_{g,h}$; credits $c_{buf}\,I^{stress}$; envelopes $\Lambda^k_g=\sum_{i\in g}a^k_i(x^*_i)$; band $\delta_g=\sqrt{2\varepsilon/H_g}$ |
| **Parameter defaults** | Table §6.9, with sources |
| **Liquidity terms and stress behaviour** | Liquidity prices rise in the drought and crisis scenarios. Duals are mixture-weighted, floored at the buffer carry and collared. Contingent budgets (Secondaries, Capital Solutions) activate in stress when the gate is green. Vintage FTP shields groups; decisions use current prices |
| **SELL / HOLD / REFINANCE / LEVER routing** | SELL: proposed by the owning group, priced with intelligence from Secondaries through the firewall; an internal buyer makes it a transfer (no liquidity). HOLD: vintage FTP and CLC continue. REFINANCE: external lender = liquidity; Capital Solutions as lender = internal leverage (no liquidity). LEVER: draws on the TPC leverage budget at $\lambda_{Lev}$. Economics per stream 08 at current duals |
| **Forecast production and biases** | Table §6.5; P10/P50/P90; WIS; hierarchical bias; $Z_g$ feeds stream 07 |
| **Synthetic defaults** | E1 parameter set (α\*, q, consumption rows) in `G8_org_calcs.py`; bias priors §6.5. All labeled SYNTHETIC |
| **Links** | 01/C1 (H duals, P rules); 04 (draws, tenors); 05 (secondary pricing, ILPA); 07 (fusion); 08 (ℓ, LAPV, MCL); 09 (tail-hedge valuation, margin); 11 (Euler limits); 14/C4 (tiers, IC protocol); G1–G7 group dossiers (group-specific forecasts, action sets) |

---

## 7. Implementation notes

- **Duals.**
  - cvxpy `constraint.dual_value` with Clarabel; HiGHS (`highspy`, or `scipy.optimize.linprog(method="highs")` `.ineqlin.marginals`) for LP duals and ranging; Pyomo `Suffix(direction=IMPORT)`; mpi-sppy for progressive-hedging multipliers.
  - MILPs have no duals: fix the integers at the incumbent and re-solve the LP ("fix-and-price"), or use Lagrangian relaxation.
- **Unique, stable prices.**
  - Use interior-point (central-path) duals or a small proximal term $\tfrac{\epsilon}{2}\|x-x_{prev}\|^2$.
  - Average across the 10 SAA replications and report the dispersion.
  - Degenerate LPs have multiple dual vertices, so check by perturbing the right-hand side.
- **Avoid double counting.** Stream 08's LAPV already embeds ℓ in its state prices π. Use *either* LAPV discounting *or* explicit FTP charges with risk-matched discounting in any one report, never both.
- **Euler contributions.** Estimate as $E[L_i\mid L\ge \mathrm{VaR}]$ on 50k paths, with importance sampling in the tail. Contributions are noisy below 1% tail mass, so use kernel smoothing.
- **Hierarchical model.** PyMC, NumPyro or Stan (cmdstanpy), with non-centred parameterization. As a quick check, `statsmodels` MixedLM on $y-q_{50}$. Cluster-robust standard errors by vintage × regime.
- **Scores.** WIS and the interval score are a few lines of numpy (see `G8_org_calcs.py`). Third-party packages (properscoring, scoringrules) are optional; pin versions after review.
- **Shapley.** Exact enumeration over 7–8 groups (256 coalitions). Use common random numbers across coalition re-runs.
- **Audit.** Hash each price vector and envelope set, and store it with the C1 scenario hash. Every published price must trace to a run_id (C4 provenance rule).

## 8. Risks, pitfalls and limitations

1. **Goodhart and metric gaming [I].**
   - Groups may structure deals to look liquid: deferred consideration, fund-level NAV loans that hide leverage, side letters.
   - *Mitigation:* the desk measures stressed consumption on look-through terms; the validator audits it.
2. **The zero-dual trap.** Slack constraints yield zero prices and a "free liquidity" illusion. *Mitigation:* the buffer-carry floor and stressed duals.
3. **Price whiplash and legitimacy.** Unsmoothed duals jump between quarters. *Mitigation:* collars, vintage locking and an annual methodology review.
4. **Over-centralization.** Tight envelopes discard soft information (Stein 2002; Alonso et al. 2008). *Mitigation:* no-regret bands and contingent budgets.
5. **Relative-pay volatility.** CPP's FY2024 value-added multiplier was 0×. Relative components can wipe out pay for years and drive talent away. Hence blended absolute and relative measures, deferral and judgment (CFA 2026 trend).
6. **Thin forecast samples.** PE outcomes settle over 6–8 years (stream 07 [S\*]). Score fast-resolving companions (cash flows, timing) first. Interim NAVs used as outcomes invite NAV management.
7. **Internal-transfer abuse.** Laundering losses into a group with an easier benchmark; window dressing. *Mitigation:* fair-value booking, the benefit test and blackout periods.
8. **Transplant risk.** The ICM evidence is corporate, and peer pay plans are Canadian, Norwegian or US. ADIC's sovereign HR and legal context is unknown. All numbers in §6 marked [I] or [I-calc] are illustrative.
9. **Evidence quality.** Several peer facts come from trade press: the CalPERS effective date, the CPP FY2025 pay change (not used), CPP's 2026 paper via a blog. TPA performance claims are not causal.

## 9. Open questions (ADIC to supply or confirm)

1. The legal and HR constraints on pay design, deferral and clawback. Can pay be decoupled from AUM?
2. Current budget process: who sets pacing, envelopes and delegated authorities today? Do groups have benchmarks or funding baskets?
3. Is Treasury (cash + IG, $15bn) central? Who owns overlay margin and collateral? Can a desk hold the FTP mismatch P&L?
4. Does a forecast archive with authorship and timestamps exist? Is there a declined-deal list that can be shadow-tracked?
5. History of internal transfers between groups, and the legal-entity, SPV and tax frictions involved.
6. The IC's composition and recusal practice. Do group heads vote on budgets?
7. The owner's view on decision rights (Board versus management) and on publishing group calibration internally.
8. The tolerance for contingent crisis budgets in Secondaries and Capital Solutions, and the signposts the IC will pre-approve.

## 10. References

**Internal capital markets, influence and organization**
1. Stein, J.C. (1997). Internal capital markets and the competition for corporate resources. *Journal of Finance* 52(1):111–133. NBER WP 5101. https://www.nber.org/papers/w5101
2. Scharfstein, D.S., Stein, J.C. (2000). The dark side of internal capital markets: divisional rent-seeking and inefficient investment. *JF* 55(6):2537–2564. https://www.nber.org/papers/w5969
3. Rajan, R., Servaes, H., Zingales, L. (2000). The cost of diversity: the diversification discount and inefficient investment. *JF* 55(1):35–80. https://www.nber.org/papers/w6368
4. Shin, H.-H., Stulz, R.M. (1998). Are internal capital markets efficient? *QJE* 113(2):531–552. https://doi.org/10.1162/003355398555676
5. Lamont, O. (1997). Cash flow and investment: evidence from internal capital markets. *JF* 52(1):83–109. https://doi.org/10.1111/j.1540-6261.1997.tb03809.x ; WP: https://www.nber.org/papers/w5499
6. Milgrom, P.R. (1988). Employment contracts, influence activities, and efficient organization design. *JPE* 96(1):42–60. https://ideas.repec.org/a/ucp/jpolec/v96y1988i1p42-60.html
7. Meyer, M., Milgrom, P., Roberts, J. (1992). Organizational prospects, influence costs, and ownership changes. *JEMS* 1(1):9–35. https://ideas.repec.org/a/bla/jemstr/v1y1992i1p9-35.html
8. Ozbas, O., Scharfstein, D.S. (2010). Evidence on the dark side of internal capital markets. *RFS* 23(2):581–599. https://ideas.repec.org/a/oup/rfinst/v23y2010i2p581-599.html
9. Glaser, M., Lopez-de-Silanes, F., Sautner, Z. (2013). Opening the black box: internal capital markets and managerial power. *JF* 68(4):1577–1631. https://doi.org/10.1111/jofi.12046 ; https://ideas.repec.org/a/bla/jfinan/v68y2013i4p1577-1631.html (the wording "all unit managers systematically over-budget capital expenditures" and "about 40% more" is from the abstract on this RePEc/IDEAS page, re-checked 18 Oct 2026; the abstract Crossref holds omits it)
10. Graham, J.R., Harvey, C.R., Puri, M. (2015). Capital allocation and delegation of decision-making authority within firms. *JFE* 115(3):449–470. https://ideas.repec.org/a/eee/jfinec/v115y2015i3p449-470.html
11. Kuppuswamy, V., Villalonga, B. (2016). Does diversification create value in the presence of external financing constraints? Evidence from the 2007–2009 financial crisis. *Management Science* 62(4):905–923. https://doi.org/10.1287/mnsc.2015.2165 ; https://ideas.repec.org/a/inm/ormnsc/v62y2016i4p905-923.html
12. Stein, J.C. (2002). Information production and capital allocation: decentralized versus hierarchical firms. *JF* 57(5):1891–1921. https://ideas.repec.org/a/bla/jfinan/v57y2002i5p1891-1921.html
13. Alonso, R., Dessein, W., Matouschek, N. (2008). When does coordination require centralization? *AER* 98(1):145–179. https://ideas.repec.org/a/aea/aecrev/v98y2008i1p145-79.html . Corrigendum: *AER* 98(3):1195–1196. https://doi.org/10.1257/aer.98.3.1195

**Capital budgeting, mechanisms and transfer pricing**

14. Harris, M., Raviv, A. (1996). The capital budgeting process: incentives and information. *JF* 51(4):1139–1174. https://ideas.repec.org/a/bla/jfinan/v51y1996i4p1139-74.html (mechanism details [M])
15. Antle, R., Eppen, G.D. (1985). Capital rationing and organizational slack in capital budgeting. *Management Science* 31(2):163–174. https://ideas.repec.org/a/inm/ormnsc/v31y1985i2p163-174.html
16. Jagannathan, R., Matsa, D.A., Meier, I., Tarhan, V. (2016). Why do firms use high discount rates? *JFE* 120(3):445–463. https://ideas.repec.org/a/eee/jfinec/v120y2016i3p445-463.html
17. Stoughton, N.M., Zechner, J. (2007). Optimal capital allocation using RAROC and EVA. *JFI* 16(3):312–342. https://ideas.repec.org/a/eee/jfinin/v16y2007i3p312-342.html
18. Froot, K.A., Stein, J.C. (1998). Risk management, capital budgeting, and capital structure policy for financial institutions. *JFE* 47(1):55–82. https://ideas.repec.org/a/eee/jfinec/v47y1998i1p55-82.html
19. Groves, T. (1973). Incentives in teams. *Econometrica* 41(4):617–631. https://ideas.repec.org/a/ecm/emetrp/v41y1973i4p617-31.html
20. Groves, T., Loeb, M. (1979). Incentives in a divisionalized firm. *Management Science* 25(3):221–230. https://ideas.repec.org/a/inm/ormnsc/v25y1979i3p221-230.html
21. Weitzman, M.L. (1976). The new Soviet incentive model. *Bell Journal of Economics* 7(1):251–257. https://ideas.repec.org/a/rje/bellje/v7y1976ispringp251-257.html
22. Weitzman, M.L. (1980). The "ratchet principle" and performance incentives. *Bell J. Econ.* 11(1):302–308. https://ideas.repec.org/a/rje/bellje/v11y1980ispringp302-308.html
23. Osband, K. (1989). Optimal forecasting incentives. *JPE* 97(5):1091–1112. https://ideas.repec.org/a/ucp/jpolec/v97y1989i5p1091-1112.html
24. Crawford, V.P., Sobel, J. (1982). Strategic information transmission. *Econometrica* 50(6):1431–1451. https://doi.org/10.2307/1913390 ; https://ideas.repec.org/a/ecm/emetrp/v50y1982i6p1431-51.html
25. Jensen, M.C. (2003). Paying people to lie: the truth about the budgeting process. *European Financial Management* 9(3):379–406. https://ideas.repec.org/a/bla/eufman/v9y2003i3p379-406.html
26. Baumol, W.J., Fabian, T. (1964). Decomposition, pricing for decentralization and external economies. *Management Science* 11(1):1–32. https://ideas.repec.org/a/inm/ormnsc/v11y1964i1p1-32.html
27. Hirshleifer, J. (1956). On the economics of transfer pricing. *Journal of Business* 29(3):172–184. https://doi.org/10.1086/294110 (content [M])

**Risk capital and bank FTP**

28. Tasche, D. (2008). Capital allocation to business units and sub-portfolios: the Euler principle. arXiv:0708.2542. https://arxiv.org/abs/0708.2542
29. Erel, I., Myers, S.C., Read, J.A. (2015). A theory of risk capital. *JFE* 118(3):620–635. https://ideas.repec.org/a/eee/jfinec/v118y2015i3p620-635.html
30. BCBS (2008). *Principles for Sound Liquidity Risk Management and Supervision* (Principle 4). https://www.bis.org/publ/bcbs144.htm
31. CEBS (27 Oct 2010). *Guidelines on Liquidity Cost Benefit Allocation* (CEBS 2010 198). https://www.eba.europa.eu/sites/default/files/documents/10180/16094/da61d4c3-3937-4612-9584-e6136cb98191/cebs18_Guidelines.pdf
32. FSI (30 Dec 2011). *Liquidity transfer pricing: a guide to better practice*. Occasional Paper 10. https://www.bis.org/fsi/fsipapers10.htm
33. Basel Framework LCR40 (drawdown rates) [S\* 08]. https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30
34. Directive (EU) 2025/2 (Solvency II cost-of-capital rate 4.75%) [S\* 08]. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025L0002

**Forecasting, scoring and elicitation**

35. Brier, G.W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review* 78(1):1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
36. Savage, L.J. (1971). Elicitation of personal probabilities and expectations. *JASA* 66(336):783–801. https://doi.org/10.1080/01621459.1971.10482346
37. Gneiting, T., Raftery, A.E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102(477):359–378. https://ideas.repec.org/a/bes/jnlasa/v102y2007p359-378.html
38. Gneiting, T. (2011). Making and evaluating point forecasts. *JASA* 106(494):746–762. https://doi.org/10.1198/jasa.2011.r10138 ; arXiv:0912.0902. https://arxiv.org/abs/0912.0902
39. Bracher, J., Ray, E.L., Gneiting, T., Reich, N.G. (2021). Evaluating epidemic forecasts in an interval format. *PLoS Comput Biol* 17(2):e1008618. https://arxiv.org/abs/2005.12881
40. Boutilier, C. (2012). Eliciting forecasts from self-interested experts: scoring rules for decision makers. *AAMAS 2012* (International Conference on Autonomous Agents and Multiagent Systems), pp. 737–744. https://doi.org/10.65109/jsvv3990 . Preprint: arXiv:1106.2489 (v1 13 Jun 2011). https://arxiv.org/abs/1106.2489
41. Chen, Y., Kash, I.A., Ruberry, M., Shnayder, V. (2014). Eliciting predictions and recommendations for decision making. *ACM TEAC* 2(2):1–27. https://doi.org/10.1145/2556271
42. Ben-David, I., Graham, J.R., Harvey, C.R. (2013). Managerial miscalibration. *QJE* 128(4):1547–1584. https://www.nber.org/papers/w16215
43. Mellers, B. et al. (2014). Psychological strategies for winning a geopolitical forecasting tournament. *Psychological Science* 25(5):1106–1115. https://doi.org/10.1177/0956797614524255
44. Smith, J.E., Winkler, R.L. (2006). The optimizer's curse: skepticism and postdecision surprise in decision analysis. *Management Science* 52(3):311–322. https://doi.org/10.1287/mnsc.1050.0451 ; https://ideas.repec.org/a/inm/ormnsc/v52y2006i3p311-322.html

**Investment-specific evidence**

45. Goyal, A., Wahal, S. (2008). The selection and termination of investment management firms by plan sponsors. *JF* 63(4):1805–1847. https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1805-1847.html
46. Fang, L., Ivashina, V., Lerner, J. (2015). The disintermediation of financial markets: direct investing in private equity. *JFE* 116(1):160–178. https://ideas.repec.org/a/eee/jfinec/v116y2015i1p160-178.html
47. Braun, R., Jenkinson, T., Schemmerl, C. (2020). Adverse selection and the performance of private equity co-investments. *JFE* 136(1):44–62. https://ideas.repec.org/a/eee/jfinec/v136y2020i1p44-62.html
48. Erel, I., Flanagan, T., Weisbach, M.S. (2024). Risk-adjusting the returns to private debt funds. NBER WP 32278 (March 2024). https://doi.org/10.3386/w32278 ; https://www.nber.org/papers/w32278
49. Gompers, P., Kaplan, S.N., Mukharlyamov, V. (2016). What do private equity firms say they do? *JFE* 121(3):449–476. https://ideas.repec.org/a/eee/jfinec/v121y2016i3p449-476.html
50. Market data via stream 08 verification: Jefferies *Global Secondary Market Review* (Jul 2026) https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf ; Rede *NAV Financing Market Report 2026* https://www.rede-partners.com/s/NAV-Financing-Market-Report-2026_FINAL.pdf ; FRED SOFR https://fred.stlouisfed.org/series/SOFR ; Nadauld, Sensoy, Vorkink & Weisbach (2019), *JFE* 132(3):158–181, https://doi.org/10.1016/j.jfineco.2018.11.007 (NBER WP 22404: https://www.nber.org/papers/w22404)

**Peer practice and TPA**

51. Filbeck, A., Bok, J. (CAIA/TAI/WTW, Oct 2025). *From Vision to Execution: How Investors Are Operationalizing the TPA*. https://www.thinkingaheadinstitute.org/content/uploads/2025/10/2025-TPA-Report-from-Vision-to-Execution.pdf
52. Urwin, R., Hayman, G. (CFA Institute RPC, Jul 2026). *The Total Portfolio Approach (TPA): A Practical Guide for Navigating the Transition to TPA*. https://doi.org/10.56227/26.1.20 ; https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/fti_tpa-report_online.pdf
53. CPP Investments (2024). *Annual Report F2024* (Total Fund Management, committees, benchmarks, compensation, LCR). https://cppinvestments.com/wp-content/uploads/2024/05/CPP-Investments-F2024-Annual-Report.pdf
54. Shen, S., Walker, D., Rubin, G. (CPP Investments Insights Institute, Apr 2026). *Investing in Uncertain Times: Achieving Disciplined Flexibility in the TPA*, via Pension Pulse (May 2026). https://pensionpulse.blogspot.com/2026/05/inside-cpp-investments-tpa-engine.html
55. CalPERS Investment Committee (17 Nov 2025). Agenda Item 5a: ALM first reading (TPA, 75/25 Reference Portfolio, 400 bp Active Risk Limit). https://www.calpers.ca.gov/documents/202511-invest-agenda-item05a-00-a/download
56. Universal Asset Owners (1 Jul 2026). *The End of the Allocation Bucket* (CalPERS effective date; secondary). https://www.universalassetowners.com/intelligence/uao-daily-brief-2026-07-01/
57. NZ Super Fund. Reference Portfolio. https://nzsuperfund.nz/how-we-invest/reference-portfolio/
58. GIC (24 Jul 2026). Annual results release (Strategic Portfolio from 2026). https://www.gic.com.sg/newsroom/all/gic-delivers-steady-long-term-returns-within-its-mandate-and-stays-focused-on-portfolio-resilience-in-a-structurally-changed-world/
59. NBIM. Compensation principles for NBIM employees (amended 21 May 2026). https://www.nbim.no/en/organisation/governance-model/executive-board-documents/compensation-principles-for-norges-bank-investment-management-employees
60. Harvard Gazette (25 Jan 2017). Course change for Harvard Management Company. https://news.harvard.edu/gazette/story/2017/01/course-change-for-harvard-management-company

**Internal-transfer analogues**

61. 17 CFR §270.17a-7 (affiliated cross trades). https://www.law.cornell.edu/cfr/text/17/270.17a-7
62. 29 U.S.C. §1108(b)(19) (ERISA cross-trading exemption). https://www.law.cornell.edu/uscode/text/29/1108
63. 12 U.S.C. §371c-1 (Federal Reserve Act §23B, market terms). https://www.law.cornell.edu/uscode/text/12/371c-1
64. ILPA (May 2023). *Continuation Funds: Considerations for LPs and GPs* [S\* 05]. https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf

**Background only (not cited in the text; existence and metadata confirmed in the G8 literature review, 18 Oct 2026):**
- Tetlock (2005). *Expert Political Judgment*. Princeton University Press. https://doi.org/10.1515/9781400830312 (the 2009 digital edition).
- Denault (2001). Coherent allocation of risk capital. *Journal of Risk* 4(1):1–34 (Aumann–Shapley allocation). https://doi.org/10.21314/jor.2001.053
- Holmström & Milgrom (1991). Multitask principal–agent analyses: incentive contracts, asset ownership, and job design. *JLEO* 7 (special issue):24–52 (multitask incentives). https://doi.org/10.1093/jleo/7.special_issue.24
- Jenkinson, Jones & Martinez (2016). Picking winners? Investment consultants' recommendations of fund managers. *JF* 71(5):2333–2370. https://doi.org/10.1111/jofi.12289 (its abstract is now available).
- Matvos & Seru (2014). Resource allocation within firms and financial market dislocation: evidence from diversified conglomerates. *RFS* 27(4):1143–1189. https://doi.org/10.1093/rfs/hhu005

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 (2.3, 2.4 item 16, 2.5); `research/literature/G8_org_tpa_economics.lit.md` §1–2; `research/literature/recheck/10_scenarios_robustness.recheck.md` (Smith & Winkler); `research/literature/recheck/G3_cap_solutions.recheck.md` (Erel, Flanagan & Weisbach). New metadata was confirmed in Crossref or OpenAlex on 18 Oct 2026.

- Lamont (1997), §10 #5: pages 57–82 → 83–109; DOI 10.1111/j.1540-6261.1997.tb03809.x added (57–82 is Carhart 1997; Crossref).
- Shin & Stulz (1998), §10 #4: dropped "(WP: NBER 5639)", which is a different 1996 paper; the *QJE* citation is unchanged.
- Glaser et al. (2013), §1 item 5, §2.2, §4 table, §10 #9: the "systematically over-budget" and "about 40% more" wording is now sourced to the RePEc/IDEAS abstract page, where both phrases were re-checked; *JF* DOI added.
- Glaser et al. (2013), §4 table: "invest about 40% more of windfalls" → "obtain larger shares of cash windfalls and raise investment about 40% more than less powerful peers", as the source says.
- Crawford & Sobel (1982), §2.7 and §10 #24: the orphan reference is now cited for strategic communication (abstract via OpenAlex); DOI 10.2307/1913390 added.
- Stein (1997), §2.1: "which works best in focused firms" → "internal capital markets may work better in relatively focused firms", restoring the source's hedge (verification F1).
- Boutilier, §1 item 5, §2.7, §10 #40: the "(2011/2012)" arXiv-only entry → the 2012 AAMAS proceedings version, pp. 737–744, DOI 10.65109/jsvv3990 (OpenAlex), with arXiv:1106.2489 kept as the preprint; in-text year 2011 → 2012.
- Chen, Kash, Ruberry & Shnayder (2014), §2.7 and §10 #41: [M] removed, since the abstract confirms the claim; pages 1–27 added.
- Gneiting (2011), §10 #38: [M] removed; DOI 10.1198/jasa.2011.r10138 added.
- Kuppuswamy & Villalonga (2016), §10 #11: subtitle "Evidence from the 2007–2009 financial crisis" and DOI 10.1287/mnsc.2015.2165 added.
- Alonso, Dessein & Matouschek (2008), §10 #13: corrigendum *AER* 98(3):1195–1196, DOI 10.1257/aer.98.3.1195, added (Crossref).
- Smith & Winkler (2006), §10 #44: subtitle "skepticism and postdecision surprise in decision analysis" and DOI 10.1287/mnsc.1050.0451 added.
- Erel, Flanagan & Weisbach (2024), §10 #48: version (March 2024) and DOI 10.3386/w32278 added. The G3 re-check's GPME/RAP label fix does not apply, because this dossier quotes no EFW numbers.
- Nadauld et al. (2019), §10 #50: journal version *JFE* 132(3):158–181, DOI 10.1016/j.jfineco.2018.11.007, added; NBER WP 22404 kept.
- Urwin & Hayman (2026), §10 #52: full title "…A Practical Guide for Navigating the Transition to TPA" and DOI 10.56227/26.1.20 added (Crossref).
- Background list: "not verified in-session" → verified titles, venues and DOIs for Tetlock, Denault, Holmström & Milgrom, Jenkinson et al. and Matvos & Seru.
- Not applicable here: the Broadie–Glasserman–Kou barrier re-run (this dossier has no barrier statistics) and the other re-checked works (none is cited in this dossier).
