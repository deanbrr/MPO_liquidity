# C2 Cluster Synthesis: private book, liquidity instruments, leverage, action economics and return-belief fusion

*ADIC multi-period robust TPA framework · Cluster 2 of 4 · As of 2026-10-18.*

*Integrates five research streams, after adversarial verification:*
- *04: PE cash flows and the DPI decline*
- *05: secondaries, NAV finance, CVs, preferred equity and CFOs*
- *06: portfolio leverage*
- *07: return-belief fusion*
- *08: SELL / HOLD / REFINANCE / LEVER valuation*

**Evidence tags.**
- **[S]** sourced and confirmed by the verifier.
- **[S\*]** sourced or computed, then corrected by the verifier. The value shown is the corrected one.
- **[P]** practitioner consensus.
- **[I]** inference, design default or illustrative calculation. Calibrate on ADIC data before use.
- **[U]** could not be verified in-session. Never show it to the IC as fact.

**Conventions.** Money is in USD and rates are annual unless noted. "Private NAV ≈ $106bn, liquid ≈ $71bn" is a 60/40 split of the client-stated $177bn, not ADIC data.

**Reliability.**
- The empirical layer is rated HIGH in all five streams. No headline number was refuted, and several hundred figures were traced to primary documents.
- The design layer is rated MEDIUM in every stream.
- This synthesis applies all of the verifiers' must-fix items. Where it differs from a dossier, the synthesis takes precedence.

---

## 0. Executive summary

### 0.1 The DPI decline is lopsided, and at ADIC's scale it is as large as the payout

MSCI's global PE distribution rate has collapsed while the contribution rate has not [S]:

| Period | Distribution rate | Contribution rate |
|---|---|---|
| 2017–20 | 17–24% | 27–31% |
| 2021 | 27% | 39% |
| 2022–25 | 9–11% | 27–31% |
| H1-2026 | 9% | 31% |

- **Calls are sticky; distributions take the whole shock.**
- **What counts as "normal" depends on the provider.** H1-2026's 9% is 33–45% of the norms the providers state (MSCI ~20–27%, Jefferies 25%, PitchBook 23.4%) [S].

**Illustrative ADIC cash budget [I, recomputed here].** Assume an $11bn/yr commitment pace.

| Regime | Net private cash flow | Liquid-book funding of the $8.85–17.7bn payout | Share of the $71bn liquid book |
|---|---|---|---|
| Normal year | ≈ +$10.6bn | −$1.8bn to $7.1bn | ≤10% per year |
| Drought | ≈ $0 | $8.6–17.5bn (the whole payout) | 12–25% per year |
| Crisis year | ≈ −$2.6bn | $11.5–20.3bn (more than the payout) | 16–29% per year, on a shrinking base |

**Persistent three-year drought, 7.5% payout [I].**
- The private share drifts from 60% to about 75%.
- The liquid book falls from $71bn to about $44bn.
- Private NAV plus unfunded commitments passes 80% of NAV within the first year (§5.2).

### 0.2 One decision currency prices every action

**Two primitives [I, from stream 08].** SELL, HOLD, REFINANCE and LEVER combine two decisions:
- **exposure:** sell, hold or add;
- **financing:** borrow b ≥ 0 against the asset.

**One deflator prices every action.** Each action is a bundle of state-contingent cash flows and resource usages, priced by $\pi_{s,t}=p_s\,m_{s,t}\prod_{k<t}(1+\ell^q_{s,k})^{-1}$ (quarterly premia ℓ^q; §3):
- **m prices market risk.** It is calibrated so that the deck's α\* funding basket prices at par.
- **ℓ is ADIC's own liquidity premium.** It comes from the duals of *every* optimizer row that contains cash.
- **The score is the full reduced cost.**

This one construction repairs four separate unit and kernel errors that the verifiers found in streams 04, 05, 06 and 08.

**The kernel choice changes decisions.** In stream 08's Example 1, a kernel with no risk premium turns SELL into KEEP by $72m [S\*].

### 0.3 Whether, which, what

| Input | Decides |
|---|---|
| Level of ℓ | *Whether* to raise liquidity at all |
| Term structure of ℓ | *Which* source: borrow or sell |
| The asset's fused forward belief | *What* to sell |

- **With a flat ℓ, ℓ cancels between selling and borrowing**, per dollar raised. At stream 06's inputs:
  - a NAV loan beats selling only if repaid within about 2.0 years;
  - AA term debt beats selling if repaid within about 5.8 years [S, recomputed].
- **With a humped ℓ (high for one to two years), short bridges win.** In stream 08's Example 1, a two-year NAV loan adds $2.3m, although the same loan destroys $7.9m when ℓ = 0 [S].

### 0.4 Liquidity is cheapest when bought before it is needed

In a crisis, bids are lowest exactly when ℓ is highest (the H2-2008 average high bid was 61% of stale NAV) [S], NAV-facility capacity shrinks, spreads widen (+140bp in 2022) [S] and sale processes fail. So the option to sell later is worth least in the very states where it would be used. Pre-arranged facilities, a debt-funded reserve combined with a payout band that responds to conditions, and routine sales from strength all dominate crisis selling. Yale's 2025 sale, reported at a discount of less than 10% (completion unverified), is the model; Harvard's 2008 forced selling is the counter-example.

### 0.5 Leverage is a liquidity and implementation tool, not a route to 10%

- **The beta-leverage arithmetic [S\*].** Take an illustrative portfolio with μ = 8% and σ = 11%. Levering it to 10% log-growth needs about 2.36× at 4.05% funding, which is 0.72 Kelly. It becomes infeasible once funding exceeds about 4.28%, or about 4.52% for a 10% compounded target.
- **Lever the liquid book and the overlay, not PE.**
- **Asset-level LEVER for return needs all three of:**
  - financing at roughly 3% or less over SOFR;
  - high-conviction α\*;
  - a moderate ℓ.

  At Rede's 4.8% secured average it is never optimal in stream 08's Example 2 [S\*].
- **Present ADIC's limits as deliberately below peers [S\*].** CPP's own recourse-leverage measure is 36% of net assets, against a 45% Board limit. The often-quoted 9.7% is DBRS's debt-only ratio.

### 0.6 The liquidity ladder depends on market state

The ladder must be modeled, not hard-coded. Approximate H2-2026 order, cheapest first: cash above the floor; liquid rebalancing; physical-to-synthetic (futures financing ~SOFR+30–80bp, peaks >140bp); committed lines and AA term debt (T+55–99bp, partly [U]); a diversified LP-portfolio facility (~SOFR+300bp [I]); CFO senior notes (~SOFR+295bp, 2025, one law firm's deals [S]); single-fund NAV loans (4.8–6.1% margins [S]); preferred equity (12–20% [I]); LP secondary sales (cost depends on beliefs); deferred sales; pacing cuts; payout flexibility; tail-hedge monetization (§4.3, §4.5). Every rung carries capacity, a lag, execution risk correlated across rungs, encumbrance and, for financings, a covenant that acts like a written put on NAV.

### 0.7 Beliefs: only the forward, net-of-fee return on current NAV drives actions

Since-inception IRR is sunk. A deterministic Forward Belief Engine (FBE) translates underwritten, actual and forecast returns onto that common forward basis, debiases them against ADIC's own forecast–outcome history (in the style of weather-service Model Output Statistics, MOS), and fuses them by constrained GLS. Corrections built in: fund interests use Bornhuetter–Ferguson/Benktander maturity credibility with an outside-view prior frozen at inception and no separate underwriting signal; calibration carries an outcome-noise term shared across sources; simulation carries a common group-bias shock, so forecast risk is not falsely diversified away; thresholds use expected values, not plug-in means.

### 0.8 Corrected headline examples

Stream 08's 2018 buyout: expected SELL advantage **$3.3m, not $10.75m**; reservation price **87.3%, not 85.9%**. Stream 07's late-life fund flips at a bid of **86.9%** of NAV, so at realistic tail-end bids of 70–80% HOLD wins unless ℓ ≥ 8.6–24% [S\*] (§5.3). Near coin-flips are normal; the IC should debate prices and marginal assets, not every line.

### 0.9 What the IC gets, and what ADIC must supply

The IC gets one generated decision card per holding, a marginal-cost-of-liquidity (MCL) curve by horizon and market state, an agenda of "marginal" assets (at most one per binding portfolio constraint) and scenario cards whose probabilities it can override. The binding data gaps are ADIC's own (§9): fund-level cash flows and unfunded commitments by strategy, vintage and sector; a point-in-time archive of underwriting memos and forecasts (start it now); actual bids and financing quotes; LPA transfer and pledge terms; the exact payout rule and ADIC's borrowing capacity.

---

## 1. Verification ledger: what changed after fact-checking

| # | Topic (stream) | Dossier position | After verification | Consequence |
|---|---|---|---|---|
| V1 | Fees (04) | Fused α is net, yet E2 subtracts fees again | Double count. It biases every operator toward SELL by ~2–4pp/yr in good states | Beliefs and drift net; no separate fee drag |
| V2 | Alpha runway (04) | Runway on effective (drought-slowed) age | The current drought extends the full-alpha window by ~1.8 years | Runway on calendar holding period; effective age drives distributions only |
| V3 | Shadow-price units (04, 05, 06, 08) | Dual added to rates; SELL test omits the base value of cash; ℓ = μ/(π−μ) | Units are wrong. A slack constraint would reject every sale. ℓ ignores the IG+cash row; the score ignores ΔHQLA and ΔU | One deflator, full reduced cost, ℓ from all cash rows (§3) |
| V4 | Exit pricing (04) | 75% of exits clear the prior mark, applied to all inventory | The statistic is conditional on exit. It overstates unsold value and fixes exit value twice | Endogenous mark gap plus selection hazard; 75% used only as an exit moment |
| V5 | Kernel (08) | "One currency" with an unspecified objective | A linear objective prices no market risk; Example 1 flips to KEEP by $72m | Hybrid kernel plus reconciliation tests T1–T5 |
| V6 | Plug-in values (08) | SELL wins by $10.75m; reservation price 85.9% | On expected values: $3.3m; 87.3% | Every threshold on E[LAPV] |
| V7 | LEVER (08) | LEVER is optimal at SOFR+250 | Never optimal at SOFR+480/560. Rede margins are for GP fund-level loans and exclude fund-of-funds and secondary portfolios | LEVER needs financing at or below ~3%; separate financing curve per product |
| V8 | Late-life bid (07) | 88% bid for a 9.5-year fund called "consistent with ~90%" | Tail-end funds price at 70–75%; the decision switches at 86.9% | Bid distribution conditioned on age and quality |
| V9 | BF prior (07) | U₀ is debiased underwriting or a reference class, then fused again with u and the prior | Double count; Mack requires U₀ independent of development | U₀ = outside view frozen at inception; no u-signal for fund interests |
| V10 | Ω calibration (07) | Errors measured against outcomes | Outcome noise shared across sources inflates ω and ρ | Asset random effect, or identification from cross-source differences |
| V11 | Mack t (07) | t = 0.5 presented as a sourced default | t = 0.5 is a BF/chain-ladder switching rule; Mack's estimates are 0.31–0.35 | Estimate t; use 0.3–0.5 as an [I] range |
| V12 | Recap gate (07) | Levered equity return compared with debt cost | Modigliani–Miller bias toward LEVER | Separate gates for NAV loans and asset recaps |
| V13 | Overhang (05) | Benign ≥1.8×, crisis <1.0× | **Refuted.** The multiple rises when volume collapses (3.1× in 2020) | Use as a depth input only |
| V14 | Execution (05) | p = 0.85–0.95 in benign markets | Lazard's 27% failed-or-paused rate implies ≈0.73. Expected-value coverage is not a chance constraint | Correlated execution indicators; chance constraint on realized liquidity |
| V15 | Crisis prices (05, 08) | 0.60–0.65 headline plus a separate staleness term; 61/87 multiplier | Double counts staleness. 61% is an average high bid; 83.5% after market adjustment | Residual crisis level against economic NAV; staleness applied separately |
| V16 | Objective (05, 06) | Simulated wealth minus liquidity and fire-sale costs | Double count. It also adds a probability to dollar amounts without scaling | Penalize only items outside the cash flows |
| V17 | MCL program (05) | min Σ c_j x_j | Units error (per-dollar cost times a tranche fraction) | min Σ c_j Δq_j x_j |
| V18 | Peer leverage (06) | "Peers run ≤10%" | CPP is 36% on its own measure (45% limit); 9.7% is debt-only | Harmonized table; ADIC limits set below peers on purpose |
| V19 | 10% via leverage (06) | "Cannot reach" 10%; infeasible ≥4.65% | Reachable at 2.36× with 4.05% funding; threshold ≈4.28% / 4.52% | Restated |
| V20 | HOLD/SELL/LEVER formula (06) | λ added per $ of NAV | Implies 100% LTV; λ cancels in the choice of source | Compare per dollar raised, including encumbrance |
| V21 | Drawdown barrier (06) | Barrier on total exposure | Forces a net-short overlay at ≈14% drawdown with 60% illiquids | Barrier on the liquid-sleeve budget, with a feasibility check |
| V22 | LCR/NSFR analogs (06) | Credit for committed lines; 50% RSF on equities; unfunded commitments omitted | Basel gives 0% inflow for facilities received; non-HQLA equities carry 85% RSF | Corrected (§4.5) |
| V23 | Ruin (06) | "≈58% ruin" | That is the infinite-horizon figure: ≈0% within 5 years, ≈0.2% within 10, ≈20% within 20 | Always state the horizon |

**Market-fact corrections to carry forward [S\*].**
- MSCI's "restrained calls" sentence describes *all private capital*, not PE.
- MSCI revisions between the May-2026 deck and the October report are +1 to +3pp, not 1–4pp.
- PitchBook's $27.6bn is "IPO value", equal to 26.9% of exit value (the source's 30.5% is internally inconsistent).
- Sorensen–Wang–Yang is *RFS* 27(7):1977–2021, not 27(2).
- WilmerHale's "could not be given away" is a hypothetical, not an observed event. The source is "Trends in the Private Equity Secondary Market", ABA *Business Law Today* 18(4), March/April 2009; stream 05's reference gave the wrong title [corrected 2026-10-18].
- Bollen–Sensoy's 5–10pp comes from the 2015 working paper. The published version (*Financial Management* 51(2):501–538, 2022) reports instead that breakeven returns roughly equal observed returns for moderately risk-tolerant LPs with up to 40% in PE, so never cite the 5–10pp to the journal article [corrected 2026-10-18].
- ILPA's LPAC-consent recommendation for distribution use is in Part III of its guidance.
- The Jefferies July-2026 figures are readable from the primary report, so the dossiers' [C] tags become [S].
- Published BGG estimates: β ≈1.0 for buyout and ≈1.4 for VC; total risk ≈33% and ≈40%.
- Nadauld et al.'s transaction data cover 2006–2014.
- Bain's distribution series covers buyout, not all PE.
- Harvard's 2025 sale was reported as "planning" or "agreed", not as completed.
- The ~200bp over fed funds is equity-repo financing, not futures-implied financing.
- "Sweeteners" are a seller tactic, not a buyer one.

**[U] items: do not present these as fact.**
- Temasek debt of S$25.5bn (≈5% of NPV).
- PIF's May-2026 spreads of T+95–99.
- Mubadala's 10-year at T+55.
- AllianceBernstein's NAV-loan LTV of 5–30% and OID of 1–3%.
- CME's "+38bp in Q2-2025".
- PitchBook's interim-versus-final R² of 0.40 and 0.54.
- The survey claim that "two-thirds of LPs prefer to hold out for a higher MOIC".
- Harvard-2008 discount levels and completion.
- GIC, CIC and KIC process details.
- Current NAIC treatment of CFOs.
- The content of ILPA's 2026 draft CV guidance.
- "Yale's first secondary sale".

**Removed from the [U] list** [corrected 2026-10-18]. The stream-07 literature audit confirmed both items against indexed abstracts:
- Jenkinson, Sousa & Stucke (2013, SSRN 2229547): 761 CalPERS fund investments; NAVs understate subsequent distributions by about 35%; a Q4 jump; inflation during fundraising.
- Barber & Yasuda (2017, *JFE* 124(1):172–194): low-reputation GPs with low realization rates show performance peaks, then erosion after fundraising.

Stream 06's stylized balance-sheet Monte Carlo is internally consistent but cannot be reproduced from its specification. Treat its numbers as illustrations until the code is published.

**One cross-stream resolution.** Stream 04 gave no source for "53% of LPs say undrawn commitments limit new commitments". Stream 08's verifier confirmed it as a PEI survey cited by Bain 2026 [S].

---

## 2. Reconciled design decisions

| # | Question | Where the dossiers differed | Recommendation |
|---|---|---|---|
| D1 | Decision currency | 04: hurdle + shadow price. 05: IRR, value cost and dual test. 06: V_H/V_S/V_L. 08: LAPV | One deflator and the full reduced-cost score (§3). IRRs are for display only |
| D2 | Risk pricing in the kernel | 08: r_h shortcut versus an unspecified program objective | Hybrid: a market-calibrated m (funding basket at par under C1's CMA ensemble) combined with liquidity premia from the here-and-now program (HDP). Utility-implied duals run as a diagnostic |
| D3 | Expected vs robust duals | 08: robust duals for SELL/LEVER, expected for REFI | One robust (ρ-weighted) dual set for every action, so LEVER = ADD + REFI stays intact. Expected-dual scores shown as a sensitivity column. Irreversibility enters through κ^irr |
| D4 | Fees | 04 mixes gross and net | Net LP cash flows throughout. Gross underwriting is converted through the LPA waterfall. No separate fee drag |
| D5 | Age effects | 04: runway; 07: age-declining prior | Apply once. The FBE prior carries the age decline; the runway only shapes the time profile, on calendar holding period |
| D6 | Cash-flow regimes | 04: B/N/D/C multipliers *and* X_t. 05/06: HMM. C1: four macro regimes | Two layers. (1) An exit-window state e_t governs distributions, calls and the age clock; its effect enters only through the mean of X_t, so it is not specified twice. (2) The macro regime z_t from C1 governs secondary prices, financing terms and execution |
| D7 | Calibration source | 04 mixes Cambridge Associates DPI curves with MSCI rates | One provider per quantity (MSCI for rates and D/C, with the data vintage recorded). Fit age and calendar effects jointly on vintage panels. ADIC's own data takes precedence |
| D8 | Secondary prices | Crisis: 04 assumed 60–75%; 05 0.60–0.65; 08 ×0.70 | Hedonic model on economic NAV with an explicit staleness term. Crisis residual 0.80–0.84 for buyout and 0.75–0.80 for LP portfolios overall [I] |
| D9 | Dry powder, overhang, depth | 05 used overhang as a regime signal | Capacity input only, conditioned on z. Haircut evergreen buyer capital in stress |
| D10 | Execution and price impact | 05: expected coverage; impact form inconsistent | Correlated binary execution with a chance constraint. Impact factor exp(−κ_z (q/Depth)^γ), γ = 1 (sensitivity 0.5). Sales capped at 5% of the strategy's LP-led volume per half-year [I] |
| D11 | Committed lines in the 30-day test | 05: ≥50% haircut. 06: counts lines "surviving stress" | 0% credit in the hard ratio; haircut credit only in the soft target |
| D12 | NAV-loan pricing for ADIC | 05/06 applied GP fund-level margins to ADIC's LP-level borrowing | Treat as separate products. LP-portfolio facility ≈ SOFR+300 (quote needed). GP fund-level loans at Rede's 4.8% / 6.1%, used when ADIC votes as an LPAC member |
| D13 | When to LEVER | 06: infrastructure example. 08: Example 2 | At asset level only with financing ≲3% over SOFR, high-conviction α\* and a moderate ℓ. Judge recaps on the unlevered return. Levering the aggregate book is a risk-budget decision, never an α decision |
| D14 | Bridge or structural shortfall | 06: tax smoothing. 04: Φ sensitivity | Borrow only against the cyclical share of the DPI shortfall. Adjust payout, pacing and allocation for the structural share. NAV loans are bridges of ≤~2 years |
| D15 | Leverage and encumbrance limits | 06: 10%/15%, 1.30×, 15% encumbrance. 05: 25% of private NAV | Recourse debt ≤10% target / 15% hard. Economic exposure ≤1.30×, delta-adjusted. Total encumbrance ≤15% / 20% of total assets. Private pledges ≤20% of private NAV |
| D16 | Covenant chance constraint | 05: ≤5% over the facility's life. 06: ≤2% within 12 months | P(trigger within 12 months) ≤ 2% and P(default level over life) ≤ 1%, both tested on lagged reported NAV |
| D17 | Drawdown control | 06: barrier on total exposure | Barrier on the liquid-sleeve and overlay budget, using de-smoothed equity and a feasibility check |
| D18 | Fusion estimator | 04: credibility form. 07: GLS | GLS with non-negative weights in code. Credibility "votes" only as the IC explanation. Actual returns shrunk for limited persistence |
| D19 | Fund interests vs single deals | 07: same signals for all | Fund interests: the BF/Benktander estimate acts as the prior and is fused with the forecast. Single deals: prior plus forecast, underwriting and actual |
| D20 | Thresholds | 08 used plug-in means | Expected LAPV over predictive draws. The reported "fused IRR" is the IRR of expected cash flows |
| D21 | Objective coupling | 05/06 subtracted costs already in wealth | Simulated wealth carries all cash economics. Penalize only signalling, relationships, rating migration and covenant-cure frictions, in normalized units |
| D22 | Payout-coverage gate | 04: open question | Hard, path-wise and robust: the cluster-C1 distribution-reliability constraint (labelled C1 in stream 11). Report quantiles |
| D23 | Scenario set | 04: four or five scenarios? | V/U/L/Crisis are mutually exclusive. AI-bifurcation is an overlay applied within each. IC probabilities applied by entropy pooling, with effective sample size monitored |
| D24 | Tail-end, deferred and GP-led deals | 05: tail-end sales cost 15–25% | Tail-end cost depends on beliefs; sellers of 10+-year funds out-earned buyers [S]. Deferred sales priced at the cash-equivalent value. CV elections and GP NAV-loan votes scored with the same kernel |

---

## 3. Canonical notation and the valuation kernel

### 3.1 Notation

The streams used π, λ and ℓ for different objects. In stream 04, π_t behaved like a rate; streams 05 and 06 used a single λ; C3's overlay stream uses λ_s. From here on:

| Symbol | Meaning |
|---|---|
| $s,t$ | Scenario path; quarter (Δ = ¼) |
| $p_s$ | Scenario probability, after entropy pooling to IC views; reweighted by ρ_k for robust duals |
| $m_{s,t}$ | Market risk deflator relative to t = 0 |
| $\ell^q_{s,t}$, $\ell_{s,t}$ | One-quarter liquidity premium; annualized $\ell=(1+\ell^q)^4-1$ |
| $\pi_{s,t}$ | ADIC deflator, with $\pi_0=1$ |
| $1+\lambda_{s,t}$ | $\prod_{k=t}^{T-1}(1+\ell^q_{s,k})$: how much more a dollar at (s,t) is worth than at the horizon |
| $y_r$ | Dual of HDP row r, normalized by the date-0 cash dual. Tildes mark normalized duals: $\tilde\mu,\tilde\phi$ |
| $\mu_{s,t},\phi_{s,t},\nu_{s,t}$ | Duals on the survival, IG+cash and distribution-floor rows |
| $\lambda_R,\lambda_{Lev},\lambda_{Enc},\rho_k$ | Duals on the risk budget, leverage, encumbrance and robust-floor rows |
| $V,N,U,C,D$ | Economic NAV, reported NAV, unfunded commitment, calls, distributions |
| $a,a^e,h$ | Calendar fund age; effective (distribution) age; holding-period clock |
| $e_t$, $X_t$, $z_t$ | Exit-window state (O, N, D, F); exit factor; macro regime from C1 |
| $\mu_i,\hat\mu_i,\hat\sigma_i$ | True, posterior-mean and posterior-sd forward net log-return on nowcast NAV |
| $r_h$ | Return on the risk-matched funding basket (the α\* benchmark), $r_f+\beta\,\mathrm{ERP}$ |

Stream 05's corrected SELL test, Σ(m + λ)L, stream 04's "deflator × (1 + π_τ)" and C3's hedge test E[(1 + λ_s)X_s] all use the same object in different normalizations.

### 3.2 The deflator

**Step 1: the HDP's cash dual.** Take the stationarity condition on the HDP's cash-carry variable:

$$\pi^{H}_{s,t}=(1+r^q_f)\sum_{s'\in\mathcal C(s)}\pi^{H}_{s',t+1}+M_{s,t},\qquad M_{s,t}=\mu_{s,t}+(1-w_{IG})\,\phi_{s,t}+\sum_{r\in\mathcal R_c}a_r\,y_{r,s,t}$$

Here:
- $w_{IG}=0.08$. A dollar of cash raises the IG+cash row's left side by 1 and its right side by 0.08.
- $\mathcal R_c$ is the set of other rows containing cash, such as encumbrance and NSFR-style rows.

**Step 2: extract the liquidity premium.**

$$\ell^q_{s,t}=\frac{M_{s,t}}{\pi^H_{s,t}-M_{s,t}}$$

The earlier ℓ = μ/(π − μ) understates ℓ, and reads zero whenever only the IG floor binds (fixes 08-R3).

**Step 3: the production deflator.**

$$\pi_{s,t}=p_s\,m_{s,t}\prod_{k<t}\big(1+\ell^q_{s,k}\big)^{-1},\qquad \frac{m_{s,t+1}}{m_{s,t}}=\exp\!\big(-r^q_f-\tfrac12\|\theta_t\|^2-\theta_t'\varepsilon_{t+1}\big)$$

- ε are the shocks to C1's scenario-generator factors.
- θ is set so that each strategy's risk-matched basket earns $r_h$.
- For screening, a deterministic shortcut applies: discount risky flows at $(1+r_h)(1+\ell)$ and contractual flows at $(1+r_f)(1+\ell)$.

### 3.3 Score: the full reduced cost

$$\mathrm{Score}(i,a)=\sum_{s,t}\pi_{s,t}\,\mathbb E_b[\Delta CF^{(i,a)}_{s,t}]+\sum_{s,t}\tilde\mu_{s,t}(h\,\Delta HQLA-\Delta SC)_{s,t}+\sum_{s,t}\tilde\phi_{s,t}(\Delta IGC-0.08\,\Delta NAV)_{s,t}-\lambda_R\Delta\mathrm{CVaR}-\lambda_{Lev}\Delta Lev-\lambda_{Enc}\Delta Enc-\sum_k\rho_k\Delta\mathrm{Floor}_k-\kappa^{irr}-\kappa^{GP}-\kappa^{tc}$$

The first term is the liquidity-adjusted present value (LAPV).

**Terms.**
- $\mathbb E_b$ is the expectation over FBE predictive draws.
- ΔSC is the change in stressed 12-month calls.
- The $\tilde\mu$ and $\tilde\phi$ terms apply only to the column's *direct* coefficients (HQLA held, stressed calls, NAV). They never apply to its cash flows, which π already prices. That is what prevents double counting.

**λ_R is an internal scarcity charge.**
- It is non-zero only when a risk row binds. Market risk is priced in m.
- If λ_R is anchored on the Solvency II cost-of-capital rate (4.75% from 30 January 2027 [S]), rescale first. That rate applies to a 99.5% VaR capital requirement, not to CVaR95.

### 3.4 Reconciliation tests (rubric gates)

- **T1. Degenerate case.** With one scenario and a deterministic ℓ, the engine reproduces stream 08's spreadsheet values.
- **T2. Frictionless case.** With every liquidity row slack, ℓ ≡ 0 and a public-equity-like stream prices at market.
- **T3. Kernel gap.**
  - Report scores under the utility-implied duals of C1's objective (CRRA γ≈3 plus a shortfall penalty) next to the hybrid kernel.
  - A persistent gap is a calibration issue for the IC to resolve (ADIC's risk aversion versus the CMA premia). It must not be absorbed silently.
- **T4. Interlock.** In each quarter, ℓ̄ is close to the implied spread of the marginal MCL source actually used.
- **T5. Identity.** LEVER − ADD − REFI equals the simulated covenant-interaction term. Stream 08's script made the identity hold by construction, so this must be checked on real outputs.

---

## 4. Component specifications

### 4.1 Private cash-flow and NAV engine (RFT-TA v2)

The engine is a regime-switching, factor-driven, time-changed Takahashi–Alexander model (RFT-TA).

**Runs [I].**

| Purpose | Grain | Paths |
|---|---|---|
| Portfolio simulation | Cohorts: strategy × vintage × region × sector (~300–500) | 50k |
| Action scoring | Individual assets (~2,000) | 5–10k, with common random numbers |

**Global state.**
- **Macro regime $z_t$** comes from C1's scenario generator: expansion, inflationary late-cycle, crisis or recovery.
- **Shock type** comes from C3: supply glut, demand bust or Gulf-war volume.
- **Exit-window state $e_t\in\{O,N,D,F\}$** (open, normal, drought, frozen) is semi-Markov with duration $d_t$, with transitions $P(e_{t+1}\mid e_t,d_t,z_{t+1})$.
- **Exit factor (dynamic factor model; fixes 04-R17):**

$$X_{t+1}=\mu_X(e_{t+1})+\phi_X\big(X_t-\mu_X(e_t)\big)+\sigma_X\eta_{t+1},\qquad y^{obs}_{k,t}=a_k+b_kX_t+\varepsilon_{k,t}$$

The observables $y^{obs}$ are:
- PE-backed IPO value;
- sponsor and strategic M&A volume;
- high-yield OAS;
- leveraged-loan issuance;
- base rates;
- secondary buyout pricing;
- the gap between inventory entry multiples and current exit multiples.

**Asset state.**
- $V,N,U,a,a^e,h$;
- inventory quality $q$;
- the mark gap $G=\ln N-\ln V$;
- the facility balance $B$;
- the belief $(\hat\mu,\hat\sigma)$.

**E2′. Economic NAV, net of fees and carry (fixes 04-R1, R2).**

$$r_{i,t+1}=\big[r_f+\beta_i\mathrm{ERP}_t+\bar\alpha_i\,\tilde g(h_{i,t})-\tfrac12\sigma_i^2\big]\Delta+\beta_i\varepsilon^m_{t+1}+\gamma_i\Delta cs_{t+1}+\omega_i'\varepsilon^{sec}_{t+1}+\sigma^{id}_i\sqrt\Delta\,\varepsilon_{i,t+1}+J_{i,t+1}$$

- **Alpha level.** $\bar\alpha_i=\hat\mu_i-r_f-\beta_i\overline{\mathrm{ERP}}+\tfrac12\sigma_i^2$ comes from the FBE. There is no separate fee term.
- **Runway shape $\tilde g$** runs on the calendar holding period h [I]:
  - 1 up to year 6;
  - linear down to 0 at year 10;
  - then a drag of 1–2% a year.

  It is normalized to average 1 over the expected remaining life, so μ̂ is preserved.
- **Jumps J.** Write-down intensity is highest in F, with a lagged mark of −15% to −25% [I].
- **Cohorts.** Scale idiosyncratic variance by $1/N_{eff}$.

**E4′. Distribution clock.**
- $a^e_{t+1}=a^e_t+\kappa(e_t)\Delta$, with κ = 1.2 / 1.0 / 0.6 / 0.5 for O / N / D / F [I].
- A term-extension event fires when calendar age exceeds the LPA term.

**E5. Calls.**
- $C_{i,t+1}=(1-e^{-\lambda_{i,t}\Delta})U_{i,t}$, with $\lambda_{i,t}=\bar\lambda_s(a_{i,t})\,m^C(e_t)\,e^{u^C_i}$.
- New commitments are called at $\lambda^0_sn_{s,t}$.
- Undrawn commitments expire at rate ξ_s after the investment period. About 5% are never called [S].
- Recallable distributions return to U.
- In F, add stress calls $c^{stress}_sU$ for follow-ons and subscription-line clean-ups [I].

**E6′. Distributions (fixes 04-R4, R5).**

$$D_{i,t+1}=(1-e^{-\delta_{i,t}\Delta})V_{i,t}e^{r_{i,t+1}}\zeta_{i,t+1},\quad \delta_{i,t}=\bar\delta_s(a^e)\exp\!\big(\kappa^D_sX_t+\varsigma_s(q)-\theta_GG+u^D_i\big),\quad \bar\delta_s(a)=-\ln\!\big[1-\min\!\big(0.95,\max(Y_s,(a/L_s)^{B_s})\big)\big]$$

- **End of fund life.** When $a^e\ge L_s$, switch to a liquidation hazard of ≈35% a year with tail-end pricing [I].
- **Lumpiness.** ζ is zero-inflated noise with mean 1 (hurdle-lognormal or Tweedie).
- **IPO exits** are staged over 4–8 quarters, partly in kind, with public-equity beta during the sell-down.
- **CV events** are elective. The probability of electing cash rises with ℓ.
- **Quality drift.** $\Delta q=-\chi D/V$, because the best assets leave first.
- **Selection.** θ_G makes assets whose value exceeds their mark exit sooner. Calibrate θ_G so that, *among exiting buyout assets*, P(proceeds > the mark two quarters earlier) ≈ 0.75 [S fact; exit-only moment].
- **Regime effects** enter only through $\exp(\kappa^D\mu_X(e))=m^D(e)$.

**E7′. Reported NAV (fixes 04-R13).**
- $r^N_{i,t}=(1-\lambda_s)r_{i,t-\ell}+\lambda_sr^N_{i,t-1}+\eta_{i,t}$.
- Fit λ_s and the lag jointly to the autocorrelation of reported returns.
- For buyout, target a first-order autocorrelation of about 0.66–0.71. BGG's weekly λ of 0.951 implies ≈0.66, and their quarterly AR(2) of (0.5, 0.3) implies ≈0.71 [S\*]. Both inputs are working-paper figures that the published *RFS* 36(3) abstract does not report [corrected 2026-10-18; unverified against the journal text].
- A quarterly AR(1) with λ = 0.5 understates smoothing.
- Covenants and bids reference N; risk and value use V.

**Exit-window regime table [I, anchored on MSCI global PE data, S].**

| e | Empirical anchor | m^D | m^C | κ | NAV drift |
|---|---|---|---|---|---|
| O, open | 2021: distributions 27%, contributions 39% | 1.25 | 1.3 | 1.2 | + |
| N, normal | 2017–20: distributions 17–24%, contributions 28–31% | 1.0 | 1.0 | 1.0 | 0 |
| D, drought | 2022–H1-26: distributions 9–11%, contributions 27–31% | 0.45–0.50 | 0.95–1.0 | 0.6 | slightly − |
| F, frozen | 2008–09 type; no MSCI analogue | 0.30–0.35 | 0.8 plus stress calls | 0.5 | −15% to −25%, lagged |

**Transitions [I].** Default quarterly rows (O, N, D, F), to be re-estimated as a hidden semi-Markov model (HSMM):
- O: 0.85 / 0.12 / 0.02 / 0.01
- N: 0.04 / 0.88 / 0.06 / 0.02
- D: 0.03 / 0.06 / 0.88 / 0.03
- F: 0.02 / 0.08 / 0.15 / 0.75

**Duration dependence.** Under p_DD = 0.88, the current 18-quarter drought has probability ≈0.11. That is weak evidence from a single spell, so duration-dependent exit from D rests on priors and on IC elicitation [S\*].

**Structural-shift sensitivity [I].** Scale δ̄ by Φ ∈ [0.75, 1.0] to cover a permanently lower distribution rate.

**Strategy defaults** (from stream 04 §6.4, corrected; [I] unless tagged).

*Buyout*
- Call schedule: 20/25/30/35/40% of remaining unfunded in years 1–5. That gives ≈90% called by year 6, matching Ljungqvist–Richardson [S].
- Bow: L = 16, B = 2.0, Y = 0. This was fitted to a *benign* end-2019 Cambridge Associates cross-section whose fund ages run 0.5–1 year lower than the dossier assumed, so refit on age × calendar panels before use [S\*].
- Net growth 11% in the normal regime.
- β ≈1.0 (published BGG); VC ≈1.4.
- Fund-level total risk ≈33% (VC ≈40%) [S].

*Other strategies (bow L, B, Y)*

| Strategy | L | B | Y |
|---|---|---|---|
| Private credit | 6 | 1.0 | 8% |
| Real estate | 12 | 2.0 | 3% |
| Infrastructure | 15 | 1.5 | 4% |
| Secondary funds | 8 | 1.5 | 0 |

Co-investments use an exit hazard with a median hold of ≈5.5 years [S]. Never run the whole book on buyout parameters (04-R10).

### 4.2 Forward Belief Engine (FBE v2)

**Target.**
- $\mu_i$ is the expected forward annualized log-return on nowcast NAV, net of fees and carry, over the remaining life $H_i$.
- The FBE also produces an exit-timing distribution.
- The IC-facing "fused IRR" is the IRR of *expected* cash flows, shown together with σ̂.

**Translation layer (with timestamps; fixes 07-R6).**
- **Nowcast NAV.**
  - $V^*_t=N_{t-s}\exp(\tilde\beta_k\Delta m_{t-s\to t}-\psi_k)$.
  - In production, use a BGG-style state space.
- **Forecast.**
  - $\rho_f=\frac1{H_f}\ln\big(R_fe^{\tilde\beta_k\Delta m_{t_f\to t}}/V^*_t\big)$.
  - The forecast's remaining value is nowcast from its own as-of date, exactly as the NAV is.
  - H is floored at 1 year.
- **Underwriting** (single deals only).
  - $\rho_u=\ln M_u/T_u$, converted from gross to net.
  - It expires when τ > T_u + 1.
- **Actual** (single deals).
  - $\rho_a=\beta_k\mathbb E[r_m]+\hat\alpha_i$, where $\hat\alpha_i=[\ln TVPI_i-\beta_k\ln(M_t/M_{t_0})]/\tau$.
  - Then shrink for persistence: $s_a=m+\varphi_a(\rho_a-m)$, with φ_a ≈ 0.5 for buyout and higher for VC [I]. Post-2000 buyout persistence is weak; VC persistence survives [S].
  - Ignore it when τ < 3.
- **Market-implied.**
  - $\rho_\pi=\frac1H\ln(\hat R/\pi V)$.
  - This is a diagnostic only, because bids are adversely selected.

**Fund interests: maturity credibility (fixes 07-R2, R4).**

1. **Outside-view prior.** $U_0$ is the outside-view ultimate TVPI for the strategy and vintage regime, *frozen at the interest's inception*. That keeps it independent of the fund's development, as Mack requires.
2. **Credibility-weighted ultimate.** With $p_\tau=1/LDF_\tau$ taken from MSCI or ADIC triangles:
   - $U_{CL}=C/p$;
   - $U_{BF}=C+(1-p)U_0$;
   - $U_{c^*}=c^*U_{CL}+(1-c^*)U_{BF}$, with $c^*=p/(p+t)$.

   Estimate t. Mack's examples give 0.31–0.35; use 0.3–0.5 [I] until triangles exist.
3. **Forward return.** $\rho_{dev}=\frac1H\ln\big((U_{c^*}-DPI)PI/V^*\big)$, with variance from Mack's formula or a bootstrap.
4. **Fusion.** $\rho_{dev}$ replaces both the prior and the actual signal, and is fused only with the forecast. The underwriting signal is not used separately.
5. **Pre-check.** Test first whether DPI or TVPI triangles satisfy Mack's variance model. TVPI contains a GP mark, not a partial realization.

**Single deals.**
- **Prior:** $\mu_i\sim N(m_k(h,z),\sigma_k^2)$, with an age decline after about year 7 [S] and a regime tilt.
- **σ_k:**
  - ≈5.5% for buyout (Korteweg–Sorensen: 6.0% in their baseline, 5.2–5.6% in the vintage-fixed-effect, late-sample and US cuts [S\*]);
  - a skewed mixture for VC;
  - 2–3% for core infrastructure and real estate [I].

**Fusion (GLS).**
- **Signal equation:** $s_j=\alpha_j+\beta_j\mu_i+\varepsilon_j$, with $\Omega_{jl}=\rho_{jl}\omega_j\omega_l$.
- **Standardized signals:** $\tilde s_j=(s_j-\alpha_j)/\beta_j$ and $\tilde\Omega=D^{-1}\Omega D^{-1}$.
- **Posterior:**

$$\Lambda=\sigma_k^{-2}+\mathbf 1'\tilde\Omega^{-1}\mathbf 1,\qquad \hat\mu=\Lambda^{-1}\big(m\sigma_k^{-2}+\mathbf 1'\tilde\Omega^{-1}\tilde s\big),\qquad \hat\sigma^2=\Lambda^{-1}$$

- **Weights:** $w_0=\sigma_k^{-2}/\Lambda$ on the prior and $w=\tilde\Omega^{-1}\mathbf 1/\Lambda$ on the signals.
  - If any weight is negative, solve the constrained minimum-variance combination with w ≥ 0 and report the binding constraint.
  - Shrink estimated weights toward simple defaults (the forecast-combination puzzle).

**Buyout defaults [I]** (to be replaced by ADIC estimates):

| Parameter | Default |
|---|---|
| α_f, forecast optimism | +3%/yr, prior N(0.03, 0.02²); +4% late in fund life |
| α_u, underwriting optimism | +5% for in-house deals; +2% for core infrastructure |
| ω_f | 6%, with heteroscedastic spread $\omega_f^2=c+dS_f^2$ in the EMOS style |
| ω_u(τ) | $\sqrt{0.06^2+0.0006\tau}$ |
| ω_a(τ) | $\sqrt{\sigma_{id}^2/\tau+(\sigma_{mark}/\tau)^2+\sigma_{np}^2}$; σ_id 25% for funds and 40–60% for single deals; σ_mark 15%; σ_np 5% |
| ρ_fu, ρ_fa, ρ_ua | 0.5, 0.3, 0 |
| Outcome noise σ_e | 15%/yr for funds; 30%/yr for single deals |

Stream 07's examples used inconsistent σ_e values; one value per class fixes 07-R10 and R11.

**Calibration on the 18-year memo corpus (fixes 07-R3, R7).**

*Error model.*

$$e_{ij}=y_i-s_{ij}=-\alpha_{j,g}-x_i'\gamma_j-\delta_v-\upsilon_i+\eta_{ij},\qquad \upsilon_i\sim N(0,\sigma^2_{y\mid\mu}),\ \eta\sim N(0,\Omega)$$

- $\upsilon_i$ is the asset's outcome noise, which all of its sources share.
- Alternatively, identify Ω from cross-source differences and revisions, where outcome noise cancels.

*Covariates x:*
- entry leverage (the deck's memo mining flagged >6× EBITDA);
- the share of value creation that came from multiple expansion;
- GP fundraising status;
- holding period versus plan;
- plan shortfall;
- revision history.

*Data handling.* Censored deals enter through developed ultimates; memos must be point-in-time (bitemporal); old vintages are down-weighted with an 8-year half-life [I]. Group credibility is $Z=n_{eff}/(n_{eff}+\sigma_e^2/\tau_g^2)$ with $n_{eff}=n/(1+(m-1)ICC)$. Downside-case breaches cluster by vintage, so traffic-light backtests use a vintage-clustered (beta-binomial) test. Stated 80% ranges covering 52% of outcomes need ×1.81 widening, and ×2.74 at Ben-David et al.'s 36% coverage [S arithmetic].

**Simulation coupling.**
- Draw μ_i once per path, not per period.
- Add a common group-bias shock $\varepsilon_g\sim N(0,\mathrm{sd}(\alpha_g)^2)$, loaded on each asset of group g in proportion to $w_{f,i}$.
- Update beliefs quarterly with a Kalman recursion: $\mu_{t+1}=m+\phi(\mu_t-m)+\eta_t$. This learning is what gives HOLD option value when σ̂ is large.
- Impose views on C1's scenario matrix by entropy pooling rather than re-simulating.

**Outputs.**
- μ̂, σ̂ and an 80% band.
- **P_opt = Φ((ρ_f − μ̂)/σ̂)**, labeled as model-conditional, with its sensitivity to m, σ_k and α_f. Stream 07's Example 1 shows P_opt ≈ 94% even with zero assumed optimism, from shrinkage alone (fixes 07-R8).
- P_miss, the forecast's percentile in the reference class, and the exit-timing distribution.
- Stream 07's flags F1–F10 (optimism, hockey stick, stale NAV, fundraising window, low-credibility forecaster, market disagreement above 400bp, and others).

**Use in the two tiers.** Tier 2 uses posterior means. Tier 1 uses the posterior 10th percentile, with group bias stressed by +2 standard deviations.

### 4.3 Liquidity-instrument library

**Common signature.** Each instrument k reduces to:
- proceeds $L^k_{s,t}$ and give-ups $G^k_{s,t}$;
- retained exposure and the unfunded commitment transferred (ΔU);
- lag τ_k and capacity $Q_k(z)$;
- an execution indicator $E_{k,s}$, correlated across instruments;
- encumbrance and irreversibility;
- a signalling or relationship charge.

**Ranking unit.**
- Rank instruments by value cost per dollar: $c_k=[V^\pi(G^k)-V^\pi(L^k)]/V^\pi(L^k)$.
- IRRs, computed with quarterly compounding under one convention, are for display only.

**(a) LP-led secondary sale.**

$$P_{i,t}=N^{ref}_iS_{i,t}\exp\!\big(\mu_k(z_t)+\beta'f_i-\kappa_z(q_t/\mathrm{Depth}_{k,t})^\gamma+\varepsilon_i\big)+\sum_{\tau\in(ref,t]}(C_\tau-D_\tau)$$

*Price components.*
- **Staleness.** $S_{i,t}=V^e_{i,t}/N^{ref}_i$. A shortcut is $\exp(\beta_ir^{mkt}_{ref\to t})$.
- **Base level.** $\mu_k(z)$ is calibrated to *staleness-adjusted* price levels (fixes 05-R5 and 08-R7).
- **Features $f_i$:**
  - fund age;
  - quality: +1 sd of PME (≈50bp) goes with ≈ +2.5% on price [S];
  - unfunded share;
  - size;
  - Asia/EM (35%+ discounts [S]);
  - software exposure;
  - GP tier.
- **Negative prices.** Allow P < 0 for unfunded-heavy interests in stress, as a model possibility only.

*Market conditions.*
- **Depth.** Trailing LP-led volume in the strategy, haircut to 0.7 in stress and 0.4 in crisis. The haircut includes evergreen buyer capital, which faced redemptions and 5% gates in 2026 [S].
- **Capacity.** Sales per strategy per half-year ≤ 5% of depth [I].
- **Execution.**
  - A one-factor copula: $Y_k=\sqrt{\rho_E}Z_z+\sqrt{1-\rho_E}\varepsilon_k$, with success when $Y_k\le\Phi^{-1}(p_k(z))$.
  - Defaults: p = 0.75–0.85 benign, 0.6 stress, 0.4–0.5 crisis; ρ_E = 0.5 [I].
  - Lazard's 27% failed-or-paused rate for GP-led processes in a record half implies ≈0.73 [S].

**Secondary price anchors [I, anchored on S]** (first three columns: executed levels against lagged reference NAV; crisis column: residual against economic NAV, with staleness applied separately).

| Strategy | Benign (2021) | Normal (2024–H1-26) | Moderate stress (2022) | Crisis residual (2008-type) |
|---|---|---|---|---|
| Buyout | 0.97 | 0.91–0.94 | 0.87 | 0.80–0.84 |
| All LP portfolios | 0.92 | 0.87–0.89 | 0.81 | 0.75–0.80 |
| Venture/growth | 0.88 | 0.75–0.79 | 0.68 | 0.55–0.65 |
| Real estate | 0.79 | 0.68–0.72 | 0.71 | 0.55–0.60 |
| Credit | 0.83 | 0.89–0.91 | 0.72 | 0.65–0.70 |
| Infrastructure | n/a | 0.91 | n/a | 0.75–0.80 |

**Buyout age multipliers (2024) [S]:** 0–3 years 0.99; 4–6 years 0.96; 7–9 years 0.88; 10–12 years 0.79; 13+ years 0.70.

**How the table was built.** The first three columns are Jefferies levels against lagged reference NAV [S]; staleness matters even in normal markets (Q2-2026: ACWI +15.1%, buyout marks +2.5%), so estimate μ_k(z) from executed prices with the market move since the reference date as a regressor. The crisis anchor is Cogent's H2-2008 average high bid, 61% of stale NAV or 83.5% market-adjusted [S], an upper bound on clearing prices; 0.835 × 0.73 staleness = 0.61 reproduces the headline. Non-buyout crisis values are scaled from 2022 ratios [I]. Regime dependence must be estimated (buyout held 87–94% through the drought), and Jefferies warns its aggregates are "not appropriate for the valuation of individual fund interests" [S], so ADIC's own bids drive production.

**Spread conventions (fixes 08-R5).**
- **Decision spread:** $(1+y_{sale})/(1+r_h)-1$. Compare it with ℓ̄ over the asset's cash-weighted life.
- **Transfer-to-buyer spread:** $(1+y_{sale})/(1+\hat\mu)-1$. Compare it with Nadauld et al.'s buyer-minus-seller PME gap by fund age, from 2006–2014 data [S\*]:

  | Fund age | Buyer advantage (pp/yr) |
  |---|---|
  | 0–3 years | +24.5 |
  | 4–9 years | +3.0 |
  | 10+ years | −0.8 (buyout tail −2.2) |

- **The ratio of the two is the forgone α\*.**
- **Stream 08's Example 1:** decision spread 5.7%, transfer spread 3.8%, close to the 4–9-year bucket.

**(b) Deferred consideration.**
- **Cash-equivalent price:** $p^{ceq}=\phi p_d+(1-\phi)p_d\,\pi^f_{t_d}$, where π^f includes a buyer credit spread of 2–4% [I].
- **Only φP is liquidity today.** Book the rest as a receivable.
- **Equivalent headlines [S\*].** At ℓ = 9%, deferring 50% for 12 months needs a 93.5% headline to match an 88% cash bid. With a buyer credit spread of 2% or 4%, it needs 94.3% or 95.2%.
- **Deferral depth in H1-2026 [S]:**
  - about half of deferred LP-led volume deferred more than 50% of the price;
  - 9% of LP-led volume deferred beyond 18 months.

**(c) CV election.**
- **Rule:** sell iff $p^{ceq}_{CV}N\ge V^\pi(\text{flows under roll terms})$.
- **Roll alternatives** include ILPA's status-quo option: no change to fees, carry or hurdle, and no carry crystallization [S].
- **Market behavior.** Average LP rollover was 14% in H1-2026 [S].
- **Information asymmetry.** GPs keep the assets they most want, so the roll-side belief carries an asymmetry penalty [I].

**(d) LP-portfolio NAV facility (fixes 05-R11).**

*Interest and sweep.*
- Interest: $I_t=B_tr_t\Delta$, with $r_t=\mathrm{SOFR}_t+s(\ell_t,z_t)$.
- Cash interest: $I^c_t=\min(I_t,D^{pool}_t)$.
- Sweep: $Sw_t=\sigma(\ell_t)(D^{pool}_t-I^c_t)^+$.

*Balance and LTV.*

$$B_{t+1}=B_t+(I_t-I^c_t)-Sw_t+\text{draw}_t-\text{repay}_t,\qquad \ell_{t+1}=B_{t+1}/N^{pool}_{t+1}$$

The LTV is tested on lagged reported NAV.

*Covenant levels [I].*
- The sweep rate σ rises from 25% at the starting LTV ℓ₀ to 100% at the trigger.
- Trigger: 1.5 ℓ₀.
- Default: 2 ℓ₀, which forces monetization at crisis prices.
- Compute cost and fire-sale loss path by path (first passage).

*Pricing defaults.*
- **Spread:** SOFR+300 (range 250–400). This is anchored on Proskauer FY-2025 secondaries facilities, where 67% priced at ≤3% and 33% at 3–4% [S as an analog, I for ADIC].
- **ADIC LTV:** 10–20% [I]. Secondaries funds borrow at 25–75% [S].
- **OID:** 1–2%.
- **Consent:** GP pledge consent is required.
- **Stress:** +140bp, as in 2022 [S], and the LTV cap falls by 5–10pp.
- **Crisis:** the market closes, or spreads exceed 1,000bp [I].

*Encumbrance per dollar raised [S\*].*
- At 5–30% LTV, each $1 raised pledges $3.3–20 of NAV.
- Selling at 91% gives up only $1.10 of NAV per $1 raised.

**(e) GP fund-level NAV loans (ADIC votes as an LPAC member).**
- **Terms [S].**
  - Rede 2026 target margins: 4.8% secured and 6.1% recourse-light (banks: 3.0% and 4.2%). LTVs "rarely exceed 20%".
  - Proskauer FY-2025: 23% of primary facilities close below 5% LTV, and 9% at 25% or more.
- **Synthetic DPI.** Distributions funded by NAV loans are borrowed and often recallable (ILPA Part II).
- **Consent.** ILPA Part III recommends LPAC approval for distribution use, and before any NAV facility the LPA does not permit.
- **Scoring rule.** The GP's proposal adds value to ADIC only if its all-in spread is below ADIC's ℓ̄ over the facility's life.

**(f) Preferred equity (fixes 05-R12).**
- **Advance:** $A_0=aNAV^{pool}$, with a = 20–35% in benign markets [I]. Cash funding goes up to ~50% LTV [S].
- **Accrual:** $Acc_t=(Acc_{t-1}-X_{t-1})(1+r_p)^\Delta$.
- **Payments:** $X_t=\min\{\sigma_pD_t,\max(Acc_t,m_{min}A_0-\mathrm{Paid}_t)\}$, plus an upside share after redemption.
- **Defaults [I]:** r_p = 12% (14% in stress); m_min = 1.3× (1.4× in stress). No verified 2026 benchmark exists.
- **Its convexity is the opposite of a NAV loan's:** expensive when the pool does well, cheap when it does badly.

**(g) CFO or rated note feeder.**
- **Mechanics:**
  - Issuance is binary.
  - It needs a seasoned pool of at least ~$1bn [C/I] and 6–12 months of lead time.
  - Issue at most once every 12–24 months.
  - LTV and liquidity tests divert cash away from the equity.
- **2025 market [S]:**
  - Senior notes cost SOFR+295bp on average (one law firm's deals).
  - The notes are rated single-A and bought by US insurers.
  - Maturities run 12–15 years.
- **Template: Temasek/Azalea's Astrea 9 [S].**
  - Weighted coupon 4.52%.
  - Class A LTV 35.2%.
  - Fitch upgraded the notes on 7 August 2026.
  - Its SGD tranches would need a cross-currency basis adjustment for a USD sponsor.
- **NAIC treatment of CFO notes is [U].**

**(h) Subscription lines.**
- Shift LP call timing by 0–180 days.
- In stress, calls bunch as lines are cleared or not renewed.
- ILPA caps lines at 15–25% of uncalled capital and 180 days [S].

**(i) Strips, tenders and mosaic sales.**
- Strips implement the assets that the LP relaxation splits.
- Diversified portfolio sales enter as separate columns with their own quoted prices. Sellers use recent vintages as sweeteners to lift aggregate pricing, so bundle prices are not additive [S\*].

**MCL curve (fixes 05-R6).**

$$\min_{x\in[0,1]^J}\sum_jc_j\Delta q_jx_j\quad\text{s.t.}\quad \mathrm{CVaR}_\alpha\Big(L^*_{H,s}-\sum_j\Delta q_jx_jE_{j,s}\mathbb 1\{\tau_j\le H\}\Big)\le0,\ \text{plus encumbrance and exclusivity rows}$$

- **Lumpy items.** CFOs and bundles take binary x.
- **The coverage dual** is the value cost of the last dollar raised.
- **Display.** Plot MCL_H(Q) for horizons of 30 days and 6, 12 and 24 months under each macro state, and mark today's need $L^*_H$.
- **Check.** Run test T4: ℓ̄ should be close to the cost of the marginal source.

### 4.4 Action valuation and selection

**Decision variables.**
- **Per asset:**
  - HOLD;
  - SELL-φ, with φ ∈ {0.25, 0.5, 1};
  - REFI-b;
  - ADD-x;
  - LEVER-(x, b);
  - CV roll or sell;
  - membership in a bundle;
  - sale timing.
- **Portfolio level:**
  - commitments n_{k,t};
  - facility draws;
  - CFO issuance;
  - term debt;
  - the reserve;
  - synthetic exposure, via the overlay in C3;
  - the payout within its band, also in C3.

**Rules.** Each rule is exact in the score; the annualized forms are for intuition.

- **SELL** when $p^{ceq}_i>p^*_i=[\mathbb E\,\mathrm{LAPV}_i(\text{HOLD}+\text{best REFI})+\kappa^{GP}+\kappa^{irr}-\text{relief}]/NAV_i+c$.
  - The relief terms are unfunded relief (μ̃·ΔSC), CVaR relief, and leverage and floor terms.
  - Compare with HOLD *plus* the best financing, not with HOLD alone (fixes 08-R9).
  - Transaction cost c ≈ 0.75% of NAV [P/I].
- **REFI** when $s_B+f/T_{eff}+\lambda_{Lev}+\text{covenant charge}<\bar\ell_{[0,T_{eff}]}$, with ℓ̄ averaged over the loan's term, and the LTV and covenant chance constraints pass.
- **ADD** when $\alpha^*_i-\bar\ell_{[0,D_i]}-\lambda_Rm_i+(1-p^{buy})/D_i>0$.
  - D_i is the cash-weighted life.
  - The buyer's historical 3–5pp advantage is an upper bound today, with ~$290bn of dedicated secondary capital [S\*].
- **LEVER** when both ADD and REFI hold.
  - **Asset recaps:** compare the unlevered return $r_A\approx w_Er_E+w_Dr_D(1-t)$ with the after-tax cost of debt, and charge λ_R·ΔCVaR for the added equity risk (fixes 07-R5).
  - **NAV loans against LP interests:** compare the forward NAV return with the loan cost, and require $P(\mu<c)<10\%$ [I] plus a downside-LTV pass.
- **Flat-ℓ source choice (fixes 06-R3).** Per dollar raised, SELL beats borrowing iff $e^{\alpha^*T}/(1-d)-1<(c-r_f)\tau+\text{covenant/encumbrance cost}$. At stream 06's inputs (α\* = 0.2%, T = 5, d = 9%), the break-even τ\* is ≈2.0 years for a NAV loan and ≈5.8 years for AA term debt.

**Expected values and information (fixes 08-R1, R8).**
- Every value averages over FBE draws and scenario paths.
- **Reported outputs:**
  - P(action is ex-post best);
  - expected regret for each alternative;
  - ΔP(10%) and ΔP(floor breach), from re-simulation.
- **EVPI** bounds only the value of information about the forward return.
- **An asset re-underwrite** yields the expected value of sample information (EVSI), which is less than EVPI.
- **Competitive tension improves the price, not the information.**

**Timing (fixes 05-R8).** Least-squares Monte Carlo on (N, a^e, q, X, z, ℓ, belief), with information-relaxation upper bounds, run only where the score gap is smaller than EVPI; κ^irr is the waiting value given up. Stream 08's illustration (an upper bound, since it assumes perfect learning): waiting a year is worth $9.9m but is still $8.5m worse than selling now, and only 11% of stress paths would sell a year later, against 42% of normal paths.

**Selection loop.**
1. Solve the HDP (C1) and extract ℓ and π.
2. Score every action on a scenario subsample, for example 500 paths × 12 quarters.
3. Run a mixed-integer program (MILP, solved with HiGHS) over at most 20–30 aggregated coupling rows, plus bundle columns. The rows are:
   - expected liquidity and CVaR of shortfall for quarters 1–8;
   - risk;
   - leverage;
   - encumbrance;
   - market capacity.
4. Re-solve the HDP with the selected actions fixed. Iterate 2–5 times with damping.
5. Bootstrap 20 scenario subsets to get 90% bands on the duals.
   - Flag actions whose sign flips inside the band.
   - Apply hysteresis of about EVPI/NAV and minimum holding periods.
6. Validate on held-out scenarios and on the misspecification ensemble.

**Why the exact MILP decides and prices explain.** The LP relaxation splits at most m assets (m = binding coupling rows); these are the IC's marginal assets. The duality gap does not grow with the number of assets but scales with m times the largest single-asset non-convexity, so going from 3 to ~20 rows multiplies the worst case by about 7 and the largest positions dominate it [S\*]. In stream 08's 40-asset synthetic test, three prices reproduced 36 of 40 exact-MILP decisions, while a price-only rule was feasible but $24.7m worse [S]. Solves with 1,500 binaries and 30 rows took 1.7–39 seconds at a 1e-6 gap [S].

**KKT interlock.** $\bar\ell-s_B-f/T=\lambda_{Lev}+\eta_i-\zeta_i$. This shows why cheap financing went unused: either the asset's LTV cap or the portfolio leverage cap is binding.

**Liquidity index.**
- ℓ\*_i is the flat ℓ at which SELL ties HOLD plus the best REFI.
- Cumulative sale proceeds, sorted by ℓ\*_i, give an asset-level MCL curve.

**Decision card (one per holding, generated, never hand-edited).** It merges streams 05, 07 and 08: recommendation with P(best), expected regret both ways and EVPI; the LAPV waterfall (base value at r_h, liquidity value, unfunded relief, risk and leverage charges, κ^GP, costs, waiting value); flip thresholds (reservation price p\*, break-even forward return, break-even ℓ, break-even κ^GP, deferral-equivalent headline); the belief card (u, a, f on the forward basis, credibility votes, P_opt, flags, "what you need to believe", the bid's implied buyer IRR); market evidence and capacity; liquidity released under stress and covenant-breach probability; consent, ROFR and re-up flags; alternatives considered; and since-inception IRR shown only greyed out, with NAV always beside economic NAV.

### 4.5 Leverage and financing policy

**Metrics.** Agency definitions differ, so compute every variant: recourse debt / (NAV + recourse debt) (DBRS basis); (debt + repo) / (NAV + debt + repo); Moody's-style adjusted leverage netting repo and derivatives (pin the denominator); delta-adjusted economic exposure net of hedges (so the tail hedge is not penalized); look-through leverage; encumbrance / total assets.

**Harmonized peer anchors [S\*].**

| Institution | Measure | Value |
|---|---|---|
| CPP | Recourse debt / adjusted net assets (DBRS, debt-only) | 9.7% (10.7% of plain NAV) |
| CPP | Own recourse leverage, incl. repo and leverage-generating notionals | 36% of net assets (18% in F2021); Board limit 45% |
| CPP | Stressed 1-month LCR | 6.9× (minimum 1.0) |
| OTPP | Moody's adjusted leverage | 17%; upgrade trigger <10%, downgrade trigger >25% sustained |
| OTPP | Gross exposure | ≈1.32× (2025), 1.43× (2024) |
| OTPP | Derivative notional / total assets | 3.13× |
| NBIM | Leverage limit | ≤5% |
| Temasek | Debt / NPV | ≈5% (debt figure [U]) |

**Limits** (defaults for IC ratification; deliberately below peers because of the mandated outflow and 60% illiquids) [I]:

1. **Recourse debt:** ≤10% of adjusted NAV (target), 15% (hard). P(adjusted leverage > 20% at any point within 3 years) ≤ 5%.
2. **Economic exposure:** ≤1.30×. C1's objective stream proposes the same.
3. **Encumbrance:**
   - total encumbrance ≤15% (target) and 20% (hard) of total assets;
   - private-asset pledges ≤20% of private NAV.

   Stream 05's 25% of private NAV equals 15% of total assets at a 60% private share.
4. **Covenants:** P(trigger within 12 months) ≤ 2% per facility, and P(default level over the facility's life) ≤ 1%.
5. **Maturity:** ≤20% of debt matures in any rolling 12 months.
6. **30-day coverage:** unencumbered haircut HQLA ÷ stressed outflows ≥ 1.0 (hard), 1.5 (soft).
   - Stressed outflows include payout, stressed calls, maturities, interest, P99 variation margin plus the change in initial margin (IM), repo haircut add-ons and NAV-loan cures.
   - Committed facilities *received* get 0% credit in the hard ratio, following Basel LCR40.82.
   - Over 12 months, survival must be ≥1.0 under the joint stress, with a survival horizon of at least 24 months (36 targeted).
7. **Stable funding (NSFR-style):** equity plus debt longer than one year ≥ Σ RSF × assets + RSF_U × unfunded + the next 12 months' payout.
   - RSF factors [S\*]:

     | Asset class | RSF |
     |---|---|
     | Level 1 HQLA | 0–5% |
     | Level 2A | 15% |
     | Level 2B, incl. eligible equities | 50% |
     | Other listed equities | 85% |
     | Private assets and assets encumbered ≥1 year | 100% |
   - RSF_U ≥ 50% for LP commitments [I]. Basel's 5% for undrawn facilities ignores near-certain drawdown.
8. **Discretionary leverage:** ≤ max(0, f(μ̂ − c)/σ̂²), with f ≤ 0.5, shrunk further for SE(μ̂) and illiquidity.
9. **Drawdown barrier:** applied to the liquid-sleeve and overlay budget, using de-smoothed equity, a decayed high-water mark and a feasibility check. Applied to total exposure (α = 0.75, k = 4.8), the barrier hits the 0.6× illiquid floor at ≈14.3% drawdown.
10. **Rates-overlay collateral buffer:** a 1-in-100 five-day shock plus a 99.8th-percentile ten-year look-back, recalibrated for each USD instrument and tenor. The BoE's ~250bp was calibrated on 30-year index-linked gilts [S\*]. Collateral must be mobilizable within 5 days.

**Funding cost curves.**
- Use $c_k(B,z)=r_t+\sigma_k(z)+\eta_k(z)(B/\bar B_k)^2$.
- Total cost is then cubic in B, so implement it as a power cone or with piecewise-linear segments (fixes 06-R7).

| Source | Normal | Stress | Basis |
|---|---|---|---|
| UST repo ≤3 months | SOFR to +10bp; ~2% haircut | +25bp; 5% haircut | [P] |
| CP/ECP | +5–25bp | closed, or +200bp | [P] |
| AA sovereign-related, 5–10 years | T+55–99bp | T+300–350bp | PIF 10-year T+85, Jan-2026 [S]; Mubadala [U]; Harvard Dec-2008 T+335 [S] |
| Equity-index futures | ~30bp average 2021–23; Jun-2026 roll +81bp over 3m SOFR | >140bp (Dec-2024 peak) | D. E. Shaw [S]; CME (excerpt) |
| LP-portfolio facility | SOFR+300 (250–400) | +140bp; LTV cap −5 to −10pp | [I], Proskauer analog |
| Single-fund NAV loan | 4.8–6.1% plus 1–2% fee | +140bp | Rede [S] |

**Base rates [S].**
- SOFR 3.89% (15 October 2026).
- Fed funds target 3.75–4.00% (raised 16 September 2026).
- UST yields (16 October 2026): 3-month 4.26%, 2-year 4.74%, 10-year 5.09%, 30-year 5.43%.
- 3-month bills sit about 32bp above SOFR on a like-for-like basis [S\*].

**Decision doctrine.**

- **Portfolio LEVER.** Proceed only if all four hold:
  1. Tier 1 passes with the debt included.
  2. $\alpha^*_{use}=\hat\mu_{use}-c_k-\beta_{use}\pi_p$ exceeds the shadow costs.
  3. ΔP(10%) / ΔP(floor breach) beats the IC's elicited exchange rate.
  4. Rating proxies stay within bounds with ≥95% probability.

  For the aggregate book, α\*_use = r_f − c_k < 0 by construction.
- **Lever the low-volatility, high-Sharpe exposures** (betting-against-beta logic) through the liquid book and the overlay.
  - PE already embeds leverage.
  - Anything that may need to be cut quickly should sit where cutting is cheap.
- **Tax smoothing.**
  - Debt absorbs transitory DPI shortfalls.
  - Permanent shortfalls require changes to payout, pacing or allocation.
  - The cyclical/structural split (Φ and the HSMM's duration dependence) is shown explicitly to the IC.
- **Fixed claims [S\*].** With μ = 8%, σ = 12% and fixed-dollar payouts of 7.5% of initial wealth:

  | Horizon | Ruin probability |
  |---|---|
  | 5 years | ≈0% |
  | 10 years | ≈0.2% |
  | 20 years | ≈20% |
  | 30 years | ≈40% |
  | Eventual (infinite horizon) | ≈58% (15.5% at a 5% payout) |

  So express payouts proportionally, ideally to a smoothed NAV, and budget debt service.
- **Reserve.** In stream 06's stylized simulation:

  | Policy | P(forced sale) |
  |---|---|
  | No contingent liquidity, 7.5% payout | 6.4% |
  | Debt-funded reserve of 5–10% of NAV, alone or with a stress payout cut (~5–10bp/yr carry) | 0.1–0.2% |
  | Payout band alone (cost borne by the owner) | 2.7% |
  | 10% payout, no contingent liquidity | 26.9% |

  These results are [I] and not reproducible as specified; replicate them before IC use.

  Expected forced-sale losses are small. The case for a reserve rests on:
  - Tier-1 tail constraints;
  - fire-sale costs the simulation does not capture;
  - dry-powder value: deploying 5% of NAV at a 25% stress discount captures ≈1.7% of NAV per episode, or ≈20bp/yr at one episode every ~8 years, assuming fair marks.

### 4.6 Liquidity metrics

- **Net private cash flow:** $NCF_{s,t:t+H}=\sum(D-C)$ plus cash-equivalent sale proceeds (lagged and execution-weighted) plus facility draws, minus debt service and preferred-equity and CFO payments.
- **Cash flow at risk:** CFaR_q(H) = −Q_q(NCF).
- **Path-wise payout coverage (fixes 04-R9):**
  - $PCR_{s,t}=(\text{unencumbered haircut HQLA}+NCF_{t:t+12m})/(\text{payout}+\Delta IM+VM+\text{maturities})$.
  - Report quantiles of the path-wise ratio. Never divide an expectation by a P99.
- **Survival horizon:** the first quarter in which a path would need a forced sale.
- **Liquidity released under stress:** $LR_{i,H}=P^{ceq}_i+\sum_{t\le H}(C^{stress}-D^{stress})$.
  - This favors young, unfunded-heavy interests when calls bind.
  - Temper it with the historical +24.5pp buyer advantage on 0–3-year funds, an average dominated by the crisis years [S].
- **Over-commitment ratio:** (unfunded + NAV) ÷ target allocation, on both reported and economic NAV. ERSRI's pacing plan ran at 1.48–1.93× [S].
- **Backlog turnover** (inventory ÷ annualized exits ≈ 9.6 years for US PE): present it as a stock-to-flow ratio, not a residence time.

---

## 5. Scenario arithmetic and corrected examples

### 5.1 Private-book scenarios (stream 04 toy, reframed)

| 2027–29 | Average distribution rate | Cumulative net cash flow | NAV at end-2029 |
|---|---|---|---|
| V: exit window reopens | 24% | +$47bn | $103bn |
| U: gradual recovery | 19% | +$34bn | $114bn |
| L: drought persists | 11% | +$7.5bn | $133bn |
| Crisis in 2027 | 13% | +$5bn | $98bn |

**Reframing [S\*].**
- **Commitment pace.** The toy commits $11.2bn a year against ≈$14.5bn needed to replace NAV at normal rates. That run-off inflates its net cash flows.
- **Parameters.** The whole book uses buyout parameters.
- **Normal run-rate.** At the stated rates it is ≈ +$14.7bn a year.
- **V against the payout.** +$47bn is 177% of the $26.6bn three-year minimum payout and 89% of the $53.1bn maximum.

**Starting probabilities for the IC to override [I]:** V 20%, U 40%, L 25%, Crisis 15%.

**AI-bifurcation** applies as an overlay within each scenario:
- software-heavy buyout marks fall 15–25%;
- AI-linked VC and growth NAV rises;
- distributions concentrate in staged IPOs.

### 5.2 Drought arithmetic for ADIC [I, recomputed in-session; replace with ADIC data]

**Assumptions.**
- Private NAV $106.2bn and unfunded $27bn.
- Commitments of $11bn a year.
- MSCI-definition contribution rate of 28% of (unfunded + new commitments), so calls ≈ $10.6bn a year.
- Distribution rates: 20% normal, 10% drought, 6% crisis.
- In a crisis, calls fall to 0.8× plus $0.5bn of stress calls.

| $bn a year | Normal | Drought | Crisis |
|---|---|---|---|
| Distributions | 21.2 | 10.6 | 6.4 |
| Calls | 10.6 | 10.4 | 9.0 |
| Net private cash flow | +10.6 | +0.2 | −2.6 |
| Payout (5–10%) | 8.85–17.7 | 8.85–17.7 | 8.85–17.7 |
| Funded from the liquid book | −1.8 to 7.1 | 8.6–17.5 | 11.5–20.3 |
| Share of the $70.8bn liquid book | ≤10% | 12–25% | 16–29% |

**Persistent-drought path** (7.5% payout, 8% private growth, 6% liquid return):

| Year | Private share | Liquid book | Private + unfunded |
|---|---|---|---|
| 0 | 60.0% | $70.8bn | 75.3% of NAV |
| 1 | 65.0% | $61.8bn | 80.5% |
| 2 | 69.9% | $53.0bn | 85.6% |
| 3 | 74.7% | $44.4bn | 90.6% |

**Three lessons.**
- **The replacement pace depends on the regime.** Stream 04's toy runs off at normal rates. In the drought, the same commitment pace *grows* private NAV by 8–11% a year if marks hold, while the payout drains the liquid book.
- **Pacing is first-order.** C1's limit of "private NAV + unfunded ≤ 80% of NAV" is breached within a year.
- **Pacing is also slow.** Each $1bn a year cut in commitments lowers steady-state calls by ≈$0.95bn a year. But the effect arrives gradually: unfunded commitments run off with a half-life of ≈2.1–2.5 years. The cuts also cost vintage diversification (Dimmock–Wang–Yang) and GP access.

### 5.3 Corrected action examples

**Stream 08, Example 1: 2018 buyout fund, NAV $500m, 88% cash bid, ℓ at 9% then 4%.**
- **Liquidity state [S].** The point HOLD value is $421.4m against $535.3m when ℓ = 0. ADIC's liquidity state alone moves value by ≈$114m.
- **Expected values [S\*].**
  - E[HOLD + REFI] = $431.2m.
  - SELL advantage = $3.3m.
  - Reservation price = 87.3%.
  - P(keeping turns out better) = 44.7%.
  - EVPI = $32.9m.
- **Kernel sensitivity.** With no risk premium in the kernel, HOLD = $506.5m, and KEEP wins by $72m.

**Stream 08, Example 2: core-plus infrastructure.** The best action depends on the financing spread and on ℓ [S\*]:

| Financing | ADD | LEVER | REFI | SELL |
|---|---|---|---|---|
| SOFR+250 | ℓ < 3.0% | 3.0% ≤ ℓ < ≈4.3% | ≈4.3% ≤ ℓ < 8.5% | ℓ ≥ 8.5% |
| SOFR+300 | | only 3.5–4.25% | | |
| SOFR+480 or +560 | | never | | |

**Stream 07, Example 3: late-life buyout fund, NAV 400.**
- PV_hold = 347.6 at a 9% hurdle, so the decision switches at a bid of 86.9% of NAV [S\*].
- At bids of 80%, 75% and 70%, HOLD wins unless ℓ is at least 8.6%, 15.9% or 24%.
- Nowcasting the forecast from its as-of date would cut the forecast return by ≈2.5pp and μ̂ by ≈1pp, strengthening SELL.

**Stream 07, Example 1** (hockey-stick co-investment): posterior 13.6% (80% band 7.8–19.7%) against a 22.2% forecast; P_opt of 96% is model-conditional [S\*].

**Implied cost of selling** (risk-neutral shortcut, T = 5, IC intuition only) [S]: buyout or infrastructure at 91% costs 5.0/8.0/11.1/14.1% for forward growth of 3/6/9/12%; real estate at 68% costs 11.3–21.0%. Beliefs dominate: at 91%, ±10% on forecast cash flows moves the cost from 6.3% to 14.5% [S]; the tail-end example is 9.0–13.3% depending on timing, not 12.1% [S\*]. These comparisons ignore risk transfer; decisions use §3.

---

## 6. Calibration targets

| Parameter | Value | As of | Source | Confidence |
|---|---|---|---|---|
| PE distribution rate (% of prior NAV) | 24/21/18/17 (2017–20); 27 (2021); 11/9/11/11 (2022–25); 9 (H1-26) | Data to Q2-2026; published Oct-2026 | MSCI Private Capital Benchmarks Summary Q2-2026 | High. The May-2026 vintage was 1–3pp higher, so record the data vintage |
| PE contribution rate | 31/30/28/29/39/31/27/28/29/31 (2017→H1-26) | Oct-2026 | MSCI | High |
| PE net cash flow ($bn) | +58/+18/−16/−49/+38/−127/−133/−52/−2/−16.5 | Oct-2026 | MSCI | High |
| LP-portfolio distribution yield | ~10% in H1-26; below 20% since early 2023; 25% average since 2001 | Jul-2026 | Jefferies | High |
| Buyout distributions / NAV | 14% (2025); below 15% for four years; 2014–17 average 29% | Feb-2026 | Bain GPER 2026 | High (buyout series) |
| US distribution yield | 14.8% vs 23.4% long-run | 30-Jun-2026 | PitchBook via Cherry Bekaert | Medium (source not named) |
| DPI by vintage | 2010: 1.27 (RVPI 0.48); 2012: 0.64; 2014: 0.36; 2016: 0.11 | 31-Dec-2019 | Cambridge Associates | High as data; Medium as a "normal" curve |
| Investment pace | 90% invested by year 6; median 4 years to 80%; ~5% never called | 2003 | Ljungqvist–Richardson (NBER 9454) | High |
| Cyclicality (buyout) | Elasticities to ln(P/D): distributions 0.37, calls 0.33; 92.1% idiosyncratic | 1984–2010 data | Robinson–Sensoy (NBER WP) | High as estimates; Medium for use after the rate shock |
| NAV smoothing | Quarterly reported-return AC1 ≈0.66–0.71 | WP figures | Derived by the stream-04 verifier from Brown–Ghysels–Gredil working-paper figures (weekly λ 0.951; AR(2) 0.5, 0.3), which the *RFS* 36(3) abstract does not report [corrected 2026-10-18] | Medium (working-paper source) |
| β and total risk | Buyout ≈1.0, ≈33%; VC ≈1.4, ≈40% | 2023 | BGG (published) | High |
| Exits above prior mark | ~75% of buyout exits (exit moment only) | Jun-2026 | Bain midyear, citing MSCI | High fact; Medium use |
| CV flows | 20% of 10+-year fund distributions (2021–Q3-25) vs ~6% (2016–20) | Jan-2026 | MSCI | High (a ratio, not a share) |
| Inventory | ~32k unsold companies worth $3.8tn; ~7-year buyout hold; ~40% held >5 years | YE-2025 | Bain 2026 | High |
| Secondary pricing | LP portfolios 87%; buyout 91; infra 91; credit 89; VC 79; RE 68; tail-end 25%+ discount; Asia/EM 35%+ | H1-2026 | Jefferies | High |
| Buyout price by age | 99/96/88/79/70%; 2025: under 5 years 95%, over 10 years 73% | 2024–25 | Jefferies | High |
| Tail-end pricing | ~70% since 2022; select high-quality funds into the 80s | H1-2026 | Evercore | High |
| Deferral | 26% of LP sales; 33% structured; about half of deferred volume defers >50% of price | H1-2026 | Jefferies; Evercore | High |
| Buyer capital | $290bn dedicated; overhang 1.2× (depth input only) | H1-2026 | Jefferies | High |
| Buyer target multiples | 1.7× / 1.8× / 1.9× / 2.3× over 4 years → 14.2 / 15.8 / 17.4 / 23.1% | H1-2026 | Evercore | High (IRR conversion assumes a bullet) |
| Crisis bids | Average high bid 61% of NAV; 83.5% market-adjusted; H1-08 84.7% | Jan-2009 | Cogent via Unquote | High (upper bound on clearing) |
| Buyer–seller PME gap | ~5pp/yr overall; by age +24.5 / +3.0 / −0.8pp | 2006–14 data | Nadauld et al., JFE 132(3) | High |
| Transient shock | −300 to −500bp, recovered within the quarter | Apr-2025 | Jefferies | High |
| Process failure | ~27% failed or paused (GP-led) → p ≈ 0.73 | 1H-2026 | Lazard | Medium for LP sales |
| NAV-loan margins (GP fund-level) | 4.8% secured / 6.1% recourse-light; LTV rarely >20%; +140bp in 2022 | Jun-2026; Jun-2025 | Rede | High fact; Medium as a proxy for LP-level loans |
| Secondaries facilities | 67% priced ≤3%, 33% at 3–4%; LTV 25–75% | FY-2025 | Proskauer | High (analog for ADIC) |
| CFO senior cost | SOFR+295bp; single-A; 12–15 years | Sep-2025 | Octus | Medium (narrow sample) |
| Astrea 9 | Weighted coupon 4.52%; Class A LTV 35.2% | Aug-2026 | Azalea / Fitch | High |
| Base rates | SOFR 3.89%; fed funds 3.75–4.00%; 10-year UST 5.09% | 15–16 Oct 2026 | NY Fed; FOMC; Treasury | High |
| AA term spread | PIF 10-year T+85; stress analog T+335 | Jan-2026; Dec-2008 | Emirates NBD; Harvard Magazine | High |
| Futures financing | ~30bp average; >140bp peak; +81bp in Jun-2026 | 2021–26 | D. E. Shaw; CME | High / Medium |
| Peer leverage | CPP 9.7% (debt-only) and 36% (own measure; 45% limit); OTPP 17%, 1.32×; NBIM ≤5% | 2025–26 | DBRS; CPP AR; Moody's; OTPP; NBIM | High |
| Skill dispersion σ_k (buyout) | 5.2–6.0% | 2017 | Korteweg–Sorensen, JFE 124(3) | High |
| Persistence | 57% of top-quartile-at-fundraise funds end top quartile; none post-2000 for buyout; VC persists | 2020 | Harris et al. (NBER 28109) | High |
| Time to settle quartile | 6–8 years | 2018 | Cambridge Associates | High |
| Forecaster calibration | 80% intervals contain outcomes 36% of the time | 2013 | Ben-David–Graham–Harvey | High |
| Mack credibility | c\* = p/(p+t); t ≈ 0.31–0.35 in Mack's examples | 2000 | Mack, ASTIN Bulletin 30(2) | High |
| Entry economics | 2.5× in 5 years now needs 10–12% EBITDA growth (vs ~5% in 2015) | Feb-2026 | Bain | High |
| CMAs | US large cap 7.5%; global core RE 7.9%; global infrastructure 7.1% | Data Sep-2026 | J.P. Morgan 2027 LTCMA | High |
| Unfunded stress prior | 30-day drawdown 40% (credit) to 100% (liquidity facility); a bound, not a 12-month prior | Basel text | BCBS LCR40.64 | Medium |

---

## 7. Strongest cross-disciplinary insights

1. **Actuarial reserving is the natural mathematics of fund interests** (streams 04 and 07 reached it independently). Paid ↔ DPI, incurred ↔ TVPI, ultimate ↔ final TVPI; BF/Benktander give credibility that rises with maturity, Mack or a bootstrap gives prediction intervals, and development triangles separate age from calendar effects, removing the "benign Cambridge Associates curve" problem.
2. **Bank funds-transfer pricing turns ℓ into an internal price list.** The term structure of ℓ is ADIC's FTP curve: marginal, maturity-matched, centrally owned (the FSI's 2011 survey criticized "one average rate"), with contingent-liquidity charges on unfunded commitments, overlay margin and covenant triggers.
3. **Electricity dispatch gives the merit order and the IC agenda.** Liquidity sources clear like generators; ℓ is a "temporal locational marginal price of cash"; lumpy sources need uplift-style treatment; Everett and Shapley–Folkman imply at most one marginal asset per binding constraint, and prices explain the rest.
4. **Real options with a wrong-way strike.** The right to sell is an American put whose strike (the bid) falls exactly when the value of exercise (ℓ) rises: the formal case for buying liquidity in advance, and against "we can always sell secondaries".
5. **Two primitives, one kernel, three questions.** LEVER ≡ ADD + REFI; the level of ℓ decides *whether*, its term structure *which* source, beliefs *what*. Bolton–Chen–Wang's double-barrier cash policy maps onto paying near 10% when ℓ ≈ 0 and near 5% when ℓ is high.
6. **Weather MOS/EMOS for strategy-group forecasts.** Treat the forecast as raw model output: correct level, slope and spread against outcomes, score with proper rules (CRPS, PIT), shrink combination weights, and widen ranges ×2–3 by default.
7. **Public-finance tax smoothing settles bridge versus structural.** Following Barro, borrow against transitory shocks and adjust the "tax" (payout, pacing, allocation) for permanent ones; the cyclical/structural split of the DPI decline decides REFINANCE versus SELL.
8. **Actuarial ruin theory: fixed claims change the shape of risk.** Proportional payouts cannot ruin the fund; fixed claims create an absorbing barrier (Dufresne). Leverage converts part of a proportional system into a fixed-claim one, so debt and payout policy must be set together.
9. **Operational time, with two clocks.** Distributions run on drought-slowed effective age; value creation runs on calendar time. Separating them removes both the Takahashi–Alexander catch-up artifact and the spurious alpha extension.
10. **Fire sales and margin spirals.** A NAV facility is a written path-dependent put on NAV (a private margin call); covenant triggers, haircuts and discounts jump together (Brunnermeier–Pedersen); adverse selection explains tail-end discounts (sellers of 10+-year funds out-earned buyers), so tail sales are a belief question, not automatically an expensive liquidity transfer.
11. **Measurement-error models from survey statistics.** Adviser price series are biased, noisy readings of one latent index; a Kalman filter with adviser-specific bias terms yields a dated consensus index with bands.

---

## 8. Links to the other clusters

### C1: optimization core, scenario and robustness layer, objective design

**C2 provides:**
- cohort cash-flow and NAV tensors, plus linearized per-cohort dynamics (in Luxenberg's form) for the HDP and for stochastic dual dynamic programming (SDDP);
- `ActionBundle` columns: ΔCF[S,T], ΔHQLA, ΔU, ΔCVaR, ΔLev, ΔEnc, κ terms and provenance;
- cost and capacity curves for each instrument, by macro state;
- three factors for C1's scenario generator: the exit factor X_t, the drought state and a secondary-discount factor;
- FBE predictive draws with group-bias shocks;
- covenant and encumbrance states for the Tier-1 rows.

**C2 needs:**
- **The scenario matrix:** 50k paths, monthly steps, 10 years, four macro regimes, ~20 factors.
- **HDP duals on *all* rows,** normalized and with bootstrap bands.
- **The objective specification** for test T3: CRRA γ≈3 plus a shortfall penalty.
- **Worst-case weights** for robust duals.
- **Entropy-pooling machinery.**
- **SDDP "water values"** to serve as terminal values in the timing model.
- **The re-specified Tier 1.** C1 found the 7% / 5% floor infeasible as written, so C2's action tests use C1's replacement constraints:
  - robust distribution reliability;
  - 24-month survival without forced sales;
  - a robust CVaR floor;
  - structural limits, including private + unfunded ≤ 80% of NAV, which §5.2 shows binds quickly in a drought.
- **Cross-check.** Stream 11's toy ALM [I] found that 1.4× overlay leverage with a thin reserve raises P(forced secondary sale within 5 years) from ~0% to 11% (a tail hedge cuts it to 4%). That agrees in direction with C2's reserve finding; both are illustrative until replicated in one engine.

### C3: distribution policy and sovereign liabilities, peers/TPA, derivatives overlay

- **The owner's draw.**
  - C3 models it as a NAV-scaled short put spread on oil.
  - In C3's triple-wrong-way "demand bust" state, C2's ℓ spikes, bids fall to crisis residuals, NAV facilities close and executions fail. Instrument availability must therefore follow C3's shock type.
  - C3's Gulf-war state (oil up, owner needs up) must also feed C2's liquidity rows.
- **The payout band as a liquidity source.**
  - C3 supplies the owner's marginal value of a distribution dollar, the payout base and the discretion within the band.
  - C2 supplies ℓ. With both, the state-contingent rule (pay near 10% when ℓ ≈ 0, near 5% when ℓ is high) and the tax-smoothing split can be evaluated.
- **The overlay.**
  - ℓ_s prices the tail hedge's liquidity value and enabling value, E[(1 + λ_s)X_s].
  - The variation-margin and initial-margin distribution enters C2's survival rows and encumbrance.
  - "Lever the liquid" routes discretionary leverage to the overlay.
  - Shared tasks: recalibrate collateral buffers for USD instruments, and keep futures financing separate from equity repo.
- **Peers and TPA.**
  - C2 contributes the harmonized peer leverage table.
  - It also contributes sovereign secondary-sale practice: Yale as the seller from strength, Harvard 2008 as the forced seller, GIC's reserve price, and the Astrea template.

### C4: agentic architecture and IC deliberation

**Deterministic tools** (numbers live only here):
- `rft_ta_simulate`, `nowcast_nav`
- `fbe_posterior`, `fbe_calibrate`
- `price_secondary`, `instrument_cashflows`, `mcl_curve`
- `score_actions`, `flip_thresholds`, `select_actions_milp`, `lsmc_timing`
- `covenant_sim`, `leverage_metrics`

**Agent roles proposed by the streams:** a translator (units, gross/net, dates); a reference-class librarian that reports sensitivity to the class chosen; a calibration agent; a timing-optimism challenger comparing GP exit projections with model hazards; a liquidity-tool librarian that turns adviser reports into tagged numbers and rejects untagged ones; a structuring agent whose programmes the engine prices; a covenant and facility parser with human verification; a relationship and governance agent (consent, ROFR, ILPA windows); a funding-market scout that suggests but never sets parameters; a red-team stress agent; and a behaviour challenger that flags sunk-cost and NAV-anchoring language.

**IC artefacts:**
- decision cards and belief cards;
- MCL charts;
- scenario cards;
- the marginal-asset agenda;
- group forecast scorecards.

IC members' views enter the FBE as scored signals. This implements C4's principle "aggregate beliefs, not verdicts" and its forecast registry.

**Rubric gates** (verification at every stage, in the Sakana style):
- no untagged numbers;
- unit checks: levels versus rates, quarterly versus annual;
- tests T1–T5;
- no plug-in thresholds;
- sign-flip flags within the dual bands;
- ablations:
  - with and without leverage, the reserve and payout flexibility;
  - FBE versus raw forecasts;
  - robust versus expected duals.

---

## 9. Open questions and data ADIC must supply

### 9.1 Open design and policy questions

1. **Kernel choice:** if test T3 shows a large gap between utility-implied and CMA-implied risk pricing, which governs? (C1 and the IC.)
2. **Payout band:** is it discretionary and countercyclical, and what is the owner's marginal value of a distribution dollar? (C3 and the owner.)
3. **Permitted instruments:** does the investment policy allow ADIC-level NAV facilities, CFOs and preferred equity, and is an Astrea-like vehicle acceptable to the owner?
4. **Cyclical versus structural DPI decline:** how to estimate Φ and the drought-exit hazard from one boom and one drought in MSCI's series, and what IC prior to elicit?
5. **Reserve price:** λ-based or fixed discount caps, and who may accept bids within the band?
6. **Relationship cost κ^GP:** estimable from ADIC's re-up history?
7. **Stress capacity:** what price impact applies to $2–10bn programmes in stress? Fifteen H1-2026 deals above $1bn do not establish it.
8. **Forecast scoring:** should strategy-group and IC forecasts be scored and weighted, and under what governance?
9. **Triangle fit:** do DPI or TVPI triangles satisfy Mack's assumptions, and how are errors correlated between a co-investment and a same-GP fund?
10. **Regulation:** current NAIC treatment of CFOs; the content of ILPA's 2026 CV guidance.

### 9.2 Data, in priority order

1. **Holdings, interest by interest:** calls (including fees) and distributions (including recallable and in-kind); reported NAV with reference dates; unfunded commitments by strategy, vintage, region and sector; look-through entry multiples, leverage and software/AI tags.
2. **A point-in-time, bitemporal archive** of underwriting memos (base, downside and upside cases, marked gross or net), strategy-group forecasts and revisions, and exited-deal outcomes. Start it now: without it, forecaster credibility cannot be learned free of look-ahead bias.
3. **Bids:** ADIC's own bid history and adviser indications, quarterly indicative bids from at least two advisers, and CV election history.
4. **Financing:** LP-portfolio facility quotes; CFO and preferred-equity indications; ADIC's own unsecured and committed funding cost and capacity; the legal borrowing entity and its rating.
5. **LPA terms:** transfer and pledge terms (consent, ROFR, pledge permissions), side letters and existing encumbrances.
6. **GP look-through leverage:** fund NAV facilities, subscription lines and NAV-financed distributions, via the ILPA template.
7. **The payout rule:** its base, timing, discretion and the owner's tolerance.
8. **The overlay:** CSA terms, eligible collateral, initial-margin models, and how tail-hedge payoffs correlate with margin calls.
9. **Unfunded drawdowns:** ADIC's empirical stress drawdown rates by strategy and vintage, to replace the Basel bounds.
10. **Relationships:** re-up history and access outcomes after past sales.
11. **History:** ADIC's experience in 2008–09, 2020 and 2022, for backtests.
12. **External licences:**
    - MSCI/Burgiss vintage-by-age panels;
    - adviser reports;
    - exit-factor observables (IPO and M&A pipelines, leveraged-loan issuance), with their latency.

---

## 10. Implementation notes

- **Stack:** numpy/numba/JAX and xarray (simulation); statsmodels state space (nowcast, exit factor); PyMC or NumPyro (calibration); `chainladder`, lifelines, `scoringrules`; cvxpy with CLARABEL or MOSEK (conic duals) and HiGHS (MILP); pydantic `ActionBundle`/`DualSet` schemas; bracketed `brentq` or pyxirr for IRRs.
- **Scale:**
  - simulation: 50k paths × 40 quarters × 400 cohorts ≈ 8×10⁸ state updates, minutes on one GPU;
  - scoring: ≈10⁷ multiply-adds;
  - FBE: microseconds per asset;
  - MILP: seconds to tens of seconds.
- **Pitfalls:** keep calls and distributions in intensity form and enforce U, V ≥ 0; never mix log and simple returns or quarterly and annual rates; convert smoothing between frequencies by matching autocorrelations; order HMM regimes on m^D to stop label switching; bracket IRRs with multiple roots; unit-test dual sign conventions with RHS perturbations and report degenerate duals with left and right derivatives; damp scenario noise and decision churn; convert non-USD funds; never feed the posterior back into valuation marks; charge every re-scoring against a counted evaluation budget.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2, and the citation-integrity tables in `research/literature/04_pe_cashflows.lit.md`, `05_secondaries_navfin.lit.md`, `06_leverage.lit.md`, `07_return_fusion.lit.md`, `08_action_valuation.lit.md` and `G9_synthetic_data.lit.md`.

- §1, market-fact corrections: added the pages to Sorensen–Wang–Yang, *RFS* 27(7):1977–2021 (synthesis §2.3, stream 04).
- §1, market-fact corrections: named the WilmerHale source correctly, "Trends in the Private Equity Secondary Market", ABA *Business Law Today* 18(4), 2009 (synthesis §2.3, stream 05).
- §1, market-fact corrections: added that the published Bollen & Sensoy (*Financial Management* 2022) finds breakeven returns close to observed returns for moderately risk-tolerant LPs, so the 5–10pp belongs only to the 2015 working paper (synthesis §2.4 #5).
- §1, [U] list: moved the Jenkinson–Sousa–Stucke specifics and the Barber–Yasuda mechanism out of [U], since indexed abstracts confirm both (07 table, verification-log rows 5 and 29).
- §4.1, E7′: labelled BGG's weekly λ 0.951 and quarterly AR(2) (0.5, 0.3) as working-paper figures that the *RFS* abstract does not report (synthesis §2.4 #8; G9 table row 14; stream-04 dossier §2.5).
- §6, NAV-smoothing row: re-sourced the 0.66–0.71 target to the stream-04 verifier's conversion of BGG working-paper figures, and lowered the confidence from High to Medium. No downstream value changes.
- Checked and left unchanged:
  - Nadauld et al. is already cited to *JFE* 132(3), and the 0.974/0.976 seller PME does not appear;
  - the BGG β and total-risk values are already the published 1.0/1.4 and 33%/40%;
  - Ljungqvist–Richardson already carries NBER WP 9454.
- Not applicable to this file: the Cooke 26/33, Mincer–Zarnowitz, Nordhaus, Gribik–Hogan–Pope, Jeet et al., Getmansky–Lo–Makarov, Giommetti, Bühlmann, Albertus–Denes, Geltner and Gredil–Liu–Sensoy items, which this file does not cite.
- Not applicable: the G4 barrier re-run (`research/groups/addenda/G4_barrier_rerun/RESULTS.md`). No re-run statistic appears here. The LP-facility covenant in §4.3(d) and D16 is tested on lagged reported NAV. A covenant that is itself tested quarterly needs no Broadie–Glasserman–Kou shift when it is simulated at that quarterly test frequency. The shifted barrier κD·e^{+0.5826σ√Δ} is needed only when a continuously monitored barrier is simulated with quarterly checks.
