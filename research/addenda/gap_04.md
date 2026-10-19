# Gap 04 addendum: the state and fragility engine — F_t defined and tested, k* renamed, the October-2026 initial state, and the IC state panel

**Date:** 2026-10-18 · **Closes:** gap 04, "v8's state + fragility engine was dropped, yet the design still uses it" · **Amends:** synthesis §3 L11, §4.1 (E), §4.6 (convex sleeve), §4.8 (P), §4.10 R7, §5.3 G2, §5.5, §6.7, §8; C1 §5.7, D5, D15; C3 §5.1, R12 · **Tags:** as synthesis §0 · **Data:** public only; no ADIC data. Scripts, outputs and the monthly panel are in `research/addenda/gap_04_calcs/` (`g4_signals.py`, `g4_oos.py`, `g4_valuation.py`, `g4_initial_state.py`, `g4_current_F.py` and their JSON outputs).

> Every number below is [I-calc] on public data unless tagged otherwise. ADIC figures are working assumptions [A].

---

## 1. Decisions

1. **F_t is the calibrated three-month stress probability read off the regime filter:** $F_t=\sigma(a+b\,\mathrm{logit}\,\hat\pi^{c}_t)$ (§4).
   - Neither Kritzman–Li turbulence nor the absorption ratio enters F_t.
   - Both were tested out of sample over 1990–2026, with purge and embargo. Neither adds significant information beyond the regime posterior on any target: all 12 Holm-adjusted p-values are 1.0.
   - Both remain on the panel as display-only diagnostics.
2. **k\* becomes "misspecification sensitivity" k_MS.** "Fragility" now means F_t and nothing else (§5).
3. **The initial state is produced by a seven-step, G2-frozen procedure** (§6). As of October 2026:
   - the market regime is calm (posterior ≥ 0.99 in both filters);
   - the exit window is in drought (D 0.87);
   - the shock type is Gulf war (GW ≈ 0.85);
   - the 12-month owner draw is expected at **$9.9–10.8bn**.

   The initial state, not the market regime, drives the first year. It moves expected PE distributions by **≈$9bn** against a normal start.
4. **Valuation and mean-reversion signals do not enter the PolicySpec** (§7). Evidence:
   - the CAPE timing signal has an out-of-sample R² between −5% and −56% since 1990;
   - contrarian timing costs 48bp of certainty equivalent (CE).

   Momentum stays in the existing trend sleeve. A 12-month trend tilt may enter only through the lab's sealed plane.
5. **v8's eight lights become a 12-row IC state panel fed by the engine** (§8).

## 2. Why it mattered

- C1 §5.7's standing policy uses F_t in three rules: reserve (θ₃), leverage (−θ₁₁) and tail hedge (θ₁₃).
- C3's convex-sleeve budget scales up only when "fragility is rising".
- Yet F_t was never defined. The only specified "fragility" was R7's Aumann–Serrano index, a property of the scenario distribution rather than a market state. P could not be built.
- The engine had no starting state beyond "start in drought". It therefore could not reflect the 2026 Gulf-war state documented by C3 and the G7 verifier:
  - Brent at $126.55 EIA spot on 14 Oct 2026 [S], with ICE futures around $105–110 [S→G7];
  - the UAE outside OPEC since 1 May 2026 [S].
- Design brief R13 requires the design to build on v8's state/fragility engine. This addendum rebuilds that engine and tests it.

## 3. Candidates and the test

### 3.1 Formulations

| Candidate | Definition (all inputs available at month-end t) |
|---|---|
| **Turbulence** (Kritzman & Li 2010) | $d_\tau=(y_\tau-\mu)^\top\Sigma^{-1}(y_\tau-\mu)$ on daily returns $y$ = {US equity excess, SMB, HML, 2/5/10-year Treasury zero returns from Gürkaynak–Sack–Wright yields}. μ and Σ come from the trailing 1,260 days (minimum 750); the monthly feature is the log of the mean over the last 21 days. Variant TURB_X adds developed ex-US equity and Brent (from 1993) |
| **Absorption ratio** (Kritzman, Li, Page & Rigobon 2011) | $AR_\tau=\sum_{i\le n}\lambda_i/\sum_j\sigma^2_j$, with n = N/5, on the exponentially weighted covariance (500-day window, 250-day half-life) of 47 Fama–French industries. Standardized shift $\Delta AR=(\overline{AR}_{15d}-\overline{AR}_{1y})/\sigma_{1y}$ |
| **Regime crisis posterior** | 3-state Gaussian HMM (calm, elevated, crisis) on monthly equity excess return, log realized volatility, excess bond premium (EBP, lagged one month) and Δ10y. The crisis state is the highest-volatility state. Refit each January on an expanding window from 1973; **forward-filtered only**, with no smoothing or Viterbi. Variant K4 adds CPI inflation (lagged one month) and a fourth state |
| **Composite** | Logistic regression on any subset of the above |

### 3.2 Targets, from month-end t (base rates over 1990–2026)

- **DD3:** a ≥ 10% US equity drawdown within 3 months (19.5%).
- **VM1:** within 1 month, a 10-day equity excess loss ≥ 7% *or* a 10-day rise of ≥ 40bp in the 10-year yield (15.7%). This proxies synthetic-beta and duration variation margin (VM).
- **CRED6:** EBP rises by ≥ 0.5pp within 6 months (15.9%).
  - This proxies secondary-discount widening and NAV-loan stress. Secondary prices exist only semiannually from 2019, plus the 2008 anchors.
  - EBP is the credit-supply component of spreads (Gilchrist & Zakrajšek 2012).
- **EXIT6:** the IPO window closes within 6 months, given it is open now (22.4%).
  - "Closes" means the 3-month count of net IPOs (Ritter) falls below half its 36-month average.
  - This proxies e_t transitions.

### 3.3 Protocol (pre-registered)

- **Origins.** Monthly, from 1990-01 to the last month with a label.
- **Training rows.** Rows s ≤ t − h − 3, which purges overlapping labels and adds a 3-month embargo (López de Prado 2018, ch. 7). Training starts in 1975; nested models share identical rows.
- **Estimation.** L2 logistic regression, refit monthly. The regime feature at each row comes from the refit of year(t), filtered.
- **Scores.** Brier score, log score and AUC.
- **Tests.**
  - HAC (Newey–West) t-statistics on paired log-score differences;
  - 12-month block-bootstrap intervals on ΔBrier and ΔAUC;
  - Holm adjustment over the 12 primary tests (4 targets × 3 additions).
- **Keep rule.** Holm p < 0.05 on at least 2 targets, *and* same-sign gains in 1990–2007 and in 2008–2026.

## 4. Results and the definition of F_t

### 4.1 Out-of-sample results

**Brier skill vs climatology (AUC), with the 3-state filter as baseline (C):**

| Target (h) | RV only | C | C + turbulence | C + AR | ΔLogScore: C+T vs C (HAC t) | ΔLogScore: C+AR vs C (HAC t) |
|---|---|---|---|---|---|---|
| DD3 (3m) | 7.3% (0.69) | **8.1% (0.70)** | 8.3% (0.70) | 7.1% (0.69) | +0.002 (0.31) | −0.007 (−1.11) |
| VM1 (1m) | 5.2% (0.69) | 4.8% (0.65) | 3.6% (0.68) | 3.6% (0.65) | +0.001 (0.18) | −0.004 (−0.59) |
| CRED6 (6m) | 4.3% (0.65) | 2.4% (0.63) | 4.8% (0.66) | −0.9% (0.59) | +0.011 (1.28) | −0.023 (−1.19) |
| EXIT6 (6m) | 4.2% (0.61) | **7.0% (0.65)** | 2.5% (0.63) | 2.5% (0.66) | −0.018 (−1.84) | −0.016 (−0.75) |

Holm-adjusted p-values for all 12 additions (T, AR, T+AR) are 1.0.

**Further findings.**
1. **Optimism gap.**
   - In sample (1975–2026, HAC logit), turbulence is significant given the crisis posterior: z = 2.4 for DD3, 3.2 for VM1 and 3.9 for CRED6.
   - The gain does not survive real-time estimation. This is the optimism-gap lesson of synthesis L8 and L12.
2. **Turbulence is volatility in disguise.**
   - Against the weaker K4 filter, whose crisis posterior has Brier skill −0.9% on DD3, adding turbulence helps: t = 1.70 for DD3 and 2.05 for VM1.
   - Adding realized volatility alone helps as much: t = 1.99 and 2.91.
   - After Holm, the best p-value is 0.24.
3. **No robustness win.** The cross-asset variant TURB_X (1998–2026) shows no significant gain on any target; the best is CRED6, at t = 1.10.
4. **The absorption ratio hurts.** Its level and standardized shift lower the log score in all 8 target × baseline pairs.
5. **Episodes.** F_t conditions on stress; it does not foresee exogenous shocks.

   | Date | P(DD3) | Base | Note |
   |---|---|---|---|
   | end-Jun-2008 | 0.46 | 0.15 | Drawdown followed |
   | end-Feb-2020 | 0.26 | 0.16 | Drawdown under way |
   | end-Jun-2022 | 0.32 | 0.17 | Drawdown followed |
   | end-Jan-2020 | 0.09 | 0.16 | Covid unforeseen |
   | end-Feb-2026 | 0.12 | 0.18 | Eve of the war; no 10% drawdown followed |
6. **Secondary markets (descriptive).**
   - P(CRED6) was 0.27, about twice the base rate, at end-Jun-2008, before Cogent's average high bid fell from 84.7% to 61% in H2-2008 [S].
   - It was 0.25 at end-Jun-2022, while Jefferies' all-strategy pricing fell from 92 to 81 [S].
   - It was at base (0.14) at end-Dec-2021.
   - F_t therefore *confirms* secondary stress rather than anticipating it. The panel must carry direct quotes as well.

### 4.2 Definition

$$F_t=\sigma\big(a+b\,\mathrm{logit}\,\hat\pi^{c}_t\big),\qquad \hat\pi^{c}_t=P\big(S^{str}_t=\text{crisis}\mid x_{1:t}\big)$$

- **Stress filter.** $S^{str}$ is the 3-state stress filter of §3.1, forward recursion only. Its labels are anchored on the realized volatility and credit of the crisis state.
- **Calibration.**
  - (a, b) are refit annually on realized DD3 events, with purge and embargo. F_t is therefore a calibrated P(≥10% drawdown within 3 months).
  - Reliability out of sample: forecasts of 0.08, 0.12 and 0.17 verified at 0.10, 0.14 and 0.24.
  - The top bin is overconfident (0.60 forecast vs 0.46 observed). Hence annual recalibration and Brier scoring in the forecast registry.
- **Bands.**
  - Green below 1.25× the base rate; red at or above 2×.
  - Out of sample, DD3 occurred in 13.8% of green, 48.9% of amber and 36.1% of red months; VM1 in 12.1%, 18.3% and 41.7%.
- **Now.**
  - $\hat\pi^c$ = 0.0001 at end-Sep 2026, so F = **0.10** against a 0.17 base rate.
  - The model-internal 3-month crisis probability is 0.029, at the 10th–25th percentile since 1990.

### 4.3 Use in the standing policy P (C1 §5.7, amended)

| Rule | Form | Change |
|---|---|---|
| Reserve | $\mathrm{HQLA}^\star_t/W_t=\theta_1+\theta_2P(e_t\in\{D,F\})+\theta_3F_t$ | The drought indicator becomes the exit-window posterior |
| Leverage | $\mathrm{clip}(\theta_9+\theta_{10}c_t-\theta_{11}F_t,1,1.3)$ | Unchanged form; F now defined |
| Tail hedge | $\mathrm{clip}(\theta_{12}+\theta_{13}F_t-\theta_{14}c_t,0,H^{\max})$ | Unchanged form |
| Convex sleeve | Rises toward 0.5% of NAV only if: VRP ≤ its 30th percentile, **F_t − F_{t−3} ≥ 0.05**, SKEW below its 90th percentile, and robust marginal value > 0 (thresholds are design defaults [I], tuned in P) | Defines "fragility rising" |

- **Non-anticipativity.** In simulation, P computes F_t by running the frozen filter and calibration on *simulated* factor paths; it never sees the true S_t.
- **Observation lags.**
  - Market inputs: lag 0.
  - EBP and CPI: lag 1 month.
  - The PolicySpec variable `F` carries the filter's version hash.
- **Value of the leverage rule.** A rule exposing US equity at 1 − 0.3·P(crisis), which de-risks only, earns +46bp of CE (90% CI −53 to +161) over 1990–2026 and cuts maximum drawdown from 50% to 40%. This supports θ₁₁, tuned in P, but it is not a large effect.

**Governance.**
- F_t is an inventoried model. The harness reruns annually.
- A new signal (turbulence, AR, dealer positioning, others) is promoted only by passing the same harness.
- The production 4-state macro HSMM of synthesis §4.1 replaces the stress filter only if its crisis posterior passes the harness. Our K4 proxy did not. Until then, E keeps the 4-state chain for generation and P reads F_t from the stress filter.

## 5. Renaming k\*

- **R7 "fragility k\*" becomes "misspecification sensitivity k_MS".**
  - Formula unchanged: $k_{MS}=\inf\{k>0:\sum_ip_ie^{(f_i-\tau)/k}\le1\}$, the Aumann–Serrano riskiness of the surplus over the floor.
  - IC unit: basis points of guaranteed floor lost per 0.01 nat of model error. The prototype figure was 76bp per 0.05 nats, ≈15bp per 0.01 nat.
  - Long, Sim & Zhou (2023) call this quantity "fragility". ADIC keeps the citation but drops the word.
- **Edit list:**
  - synthesis L11 ("fragility index k\*"), §4.9 Tier 1B, §4.10 R7, §6.7 ("fragility" → "misspecification sensitivity"), and the mermaid R box;
  - C1 D5, D15, §5.11 R7, §9 item 6 and §11 item 8.
- **Other F clashes:**
  - C3's R12 funded ratio $F_y$ becomes $FR_y$;
  - the safety filter is always written "module F", never with a subscript.

## 6. Initial state as of October 2026

### 6.1 Procedure

The procedure runs monthly. Its output is hashed at G2 with bitemporal data timestamps.

1. **Snapshot.** Market data to the last close (equity and VIX 16 Oct; Gürkaynak–Sack–Wright yields 9 Oct; Brent 14 Oct). EBP and CPI to September. MSCI cash-flow rates to Q2. EIA STEO and IMF WEO vintages for October.
2. **π0, the macro regime.**
   - Forward-filter the production regime filter with the latest parameters. Report the posterior, its 12-month projection $\pi_0A^{12}$, and P(stress visited within 12 months).
   - Give the range across filter specifications and parameter bootstraps.
   - IC disagreement enters as an entropy-pooling view, never as an edit to data.
3. **F_t.** Apply the §4.2 mapping.
4. **e0, the exit window.**
   - In production: the stream-04 Kalman exit factor on IPO volume, sponsor M&A, HY OAS, loan issuance and secondary pricing, feeding the HSMM over {O, N, D, F}.
   - In the interim: a Bayesian filter on annualized PE distribution rates, with lognormal likelihoods (σ = 0.15) centred on the synthesis §4.2 exit multipliers × a 20% normal rate.
5. **Z0, the shock type.**
   - The A2 nowcaster multiplies the chain prior by elicited likelihoods from:
     - structural data: EIA shut-ins and Hormuz status;
     - owner fiscal data: the IMF wedge;
     - curve shape: spot vs futures;
     - a market decomposition, admitted only after it passes historical back-checks.
   - It publishes a disagreement alarm.
6. **Oil and duration state.**
   - Initialize the two-factor oil state from the **futures curve**: χ₀ = ln spot − ln front month; ξ₀ from the back of the curve. Do not start from spot.
   - Set GW dwell from the HSMM duration distribution, conditioned on elapsed duration. Official reopening assumptions enter as a stated-confidence IC view.
7. **Draw.**
   - Fuse the model's fiscal balance (FB) with the latest IMF projection, precision-weighted.
   - Run C3 §5.2 from the actual $d_{2026}$, which is client data.
   - Report the 12-month cash draw: the Q4-26 instalment plus three 2027 instalments.

### 6.2 Illustrative outputs

| Quantity | Reading | Evidence |
|---|---|---|
| π0, stress filter | calm 0.991 / elevated 0.009 / crisis 0.0001 (end-Sep 2026) | September equity −0.4% and realized volatility ≈10.6%; EBP −0.23 (August) |
| π0, 4-state with inflation | "low-inflation calm" 0.997 | CPI 3.74% y/y in Sep, up from 2.39% in Jan [multpl/BLS]: not yet an inflation regime |
| P(stress regime within 12m) | **13% (K3) – 35% (K4)**; 27–43% from a stationary start | The initial state halves the K3 figure |
| e0 | D **0.87**, N 0.08, F 0.05; after 12 months D 0.61, N 0.27 | MSCI PE distribution rate 24/21/18/17/27% (2017–21), 11/9/11/11% (2022–25), 9% H1-26 [S] |
| E[PE distributions, next 12m] | **$11.8bn** vs $20.7bn from a normal start | On $106bn private NAV [A]; off-diagonal exit transitions [I] |
| Z0 | GW ≈ 0.85, SS 0.10, other 0.05 [I, elicited] | Gulf shut-ins 4.8 mb/d in Sep; IMF: UAE 2026 GDP −3.9% and net lending +1.5% despite ≈40% higher oil [S→03] |
| 12-month draw | **$9.9–10.8bn (5.6–6.1% of NAV)**; P90 $10.0–12.7bn; P(2027 rate ≥ 9.5%) ≈ 1.2%, almost all owner override | With $d_{2026}$ = 5.8%, the reduced form's smoothed value on IMF net lending 2024–26 |
| First-year liquid-book need (draws − net private cash) | **≈$8.5bn**, vs ≈−$0.3bn from a normal start | Calls ≈$10.4bn in drought (synthesis §2.3) |

**Readings.**
1. **The three state layers disagree, and that is the finding.**
   - The market layer reads calm, with F_t green.
   - The exit and owner layers read stressed: D and GW.
   - A single "fragility" light would show green today and miss the binding first-year risk, which is the liquid-book draw.
2. **The draw is anchored in year 1.**
   - The 2027 target sits near the 5% floor in most paths. EIA's 2027 UAE liquids forecast of 5.20 mb/d, against 4.34 in 2025, offsets lower prices [S→03].
   - $d_{2026}$ ± 0.8pp moves the 12-month draw by ±$0.9bn.
   - Starting from Z0 = GW rather than N adds $0.15–0.35bn to the mean and $0.3–1.3bn to the P90.
   - The liability risk is in 2028–29: a post-war glut with the UAE outside OPEC (stream 03).
3. **Three calibration defects surfaced.**
   - *Oil start.* C3's one-factor oil equation started at spot gives a 2027 Brent average of $111 (P10–P90 $85–140), against EIA's $84 [S→03]. Starting at $105 gives $97.5. Hence step 6.
   - *War persistence.* The memoryless chain spends 49% of 2027 in GW. The IMF assumes Hormuz reopens in March 2027, ≈17% [S→03].
   - *Shock decomposition.* A Ready (2018)-style decomposition, using US oil-producer returns as a proxy, attributes 64% of the war-period Brent rise to supply. But it also labels 83% of 2008-H2 and 85% of 2020-Q1 as supply, both demand-dominated episodes. It fails its back-check and gets near-zero weight until it is rebuilt on global producers.

## 7. Valuation, mean reversion and momentum: decision and evidence

**Out of sample, US equity, 1990 onward** (expanding OLS from 1929; Campbell–Thompson R²; Clark–West t):

| Predictor | 1 month | 12 months | 36 months | 60 months |
|---|---|---|---|---|
| log CAPE | −4.8% (t −0.5) | −47% (−0.3) | −56% (0.2) | −51% (0.5) |
| 36-month reversal | −0.1% | −0.3% | +2.8% (0.9) | +2.2% (0.7) |
| 12-month momentum | +0.1% (0.5) | −0.6% | +0.4% | +2.2% (1.1) |

- Sign- and positivity-restricted CAPE forecasts remain negative: −1.7% at 1 month to −51% at 60 months. Results are negative in both halves.

**Timing rules** (exposure 0.7–1.3, monthly, 1990-01 to 2026-07; static benchmark: CE 8.69%, maximum drawdown 50%):

| Rule | ΔCE vs static (90% block-bootstrap CI) | Maximum drawdown |
|---|---|---|
| Valuation, expanding z | −44bp (−161, +81) | 45% |
| Valuation, 30-year z | −8bp (−90, +79) | 49% |
| Contrarian on drawdown | −48bp (−121, +21) | **55%** |
| 12-month momentum | +60bp (−12, +137) | 42% |
| Valuation + momentum | +14bp (−62, +99) | 44% |
| Regime de-risking | +46bp (−53, +161) | 40% |

Seven variants were tested and none clears zero at 90%.

**Literature agrees.**
- Of the predictors that survive in sample, about half fail out of sample (Goyal, Welch & Zafirov 2024).
- Value timing is "directionally right but weak", and adding momentum helps (Asness, Ilmanen & Maloney 2017).
- Trend persists for about a year (Moskowitz, Ooi & Pedersen 2012).
- AQR's 2026 CMA: valuations are useful over 5–10 years, while at shorter horizons "returns are largely unpredictable and any predictability has tended to mainly reflect momentum and the macro environment" [S].

**v8's +0.8pp of mean-reversion attribution is an artefact.** It came from a scripted path (equities −10%, +10%, +32%), on which buying after the fall wins by construction.

**Decision.**
- **Valuation is excluded from P.** It already enters E strategically through the CMA anchors, so adding it to P would double-count:
  - AQR's equity anchor uses 1/CAPE [S];
  - J.P. Morgan's 2026 LTCMA decomposes equity returns with an explicit valuation term (Exhibit 6) [S].

  It is shown on the panel for information only: CAPE was 40.5 on 16 Oct 2026, and September's reading sits at the 98.8th percentile of monthly values since 1881 (AQR: 96th since 1980 [S]). Option-implied cheapness (VRP, SKEW) remains in the convex-sleeve rule.
- **Mean reversion is excluded.** It loses money, deepens drawdowns, and raises risk after losses. That breaks cushion-monotonicity and would trigger gambling flag G1.
  - Its legitimate content is rebalancing: the pre-committed monetization and reinvestment rule, bounded by the cushion.
  - New PolicySpec type rule: no size rule may increase in past losses unless the increase passes through c_t.
- **Momentum.** The 1–3-month trend sleeve stays in the defensive stack. A 12-month tilt on synthetic beta is a lab candidate (G3–G6, deflated over the seven variants above), not a default.

## 8. IC state panel (replaces v8's lights and the §6.7 early warnings)

| # | Light | Engine metric and bands | Oct-2026 reading | Policy link |
|---|---|---|---|---|
| 1 | Market stress | F_t vs base rate: green < 1.25×, red ≥ 2× | **Green**: 0.10 vs 0.17 | θ₃, θ₁₁, θ₁₃; convex budget |
| 2 | Macro regime | π0 with filter range; P(stress within 12m) | **Green**, with a range flag: calm ≥ 0.99; 13–35%. Watch: CPI 2.4% → 3.7% | E initial weights |
| 3 | Credit and funding | EBP; P(CRED6); NAV-loan spreads; facility availability | **Green**: EBP −0.39; 0.10 vs 0.14 | REFI pricing; ℓ |
| 4 | Margin and VM | P(VM1); max 10-day moves vs 7% / 40bp; margin use vs unencumbered HQLA (ledger); gap-03 V-state | **Green**, with a rates watch: 0.13 vs 0.18; 10y +46bp in Sep, max 10-day +37bp; VIX 19.99 | Collateral ladder; opportunistic budget |
| 5 | Exit window | e posterior; distribution/call ratio | **Red**: D 0.87; 9% rate | θ₂; pacing brake; cash-flow multipliers |
| 6 | Secondary market | Group-sourced bids (with conflict controls); Jefferies anchors | **Amber**: 87% LP / ≈91% buyout, H1-26 [S/C] | SELL reservation prices |
| 7 | Shock type | Z posterior; Brent vs both kink pairs | **Red**: GW ≈ 0.85; Brent above the floor kink | Owner-draw engine; T8 DCR by state |
| 8 | Owner draw | E and P90 of the 12-month draw; P(≥ 9.5%) | **Green** for year 1: $9.9–10.8bn; 1.2%. **Amber** watch for 2028–29 (SG hazard) | T1, T7; payout rule library |
| 9 | Liquidity gate | T3 coverage; T4 survival months; λ level | **Red**: 12–22 months against the 24-month test (synthesis §2.3d) | Waterfall; facilities |
| 10 | Model confidence | Filter disagreement, decomposition back-check, CMA dispersion, k_MS | **Amber** | Size-down rule; DEFER |
| 11 | Diagnostics (no policy link) | Turbulence and AR percentiles, with OOS evidence attached | Info | None |
| 12 | Valuation (no policy link) | CAPE percentile, VRP, SKEW | Info: CAPE 98.8th percentile | Convex timing via VRP/SKEW only |

**Rules for the panel.**
- Lights carry hysteresis: alarm 0.5σ on the safe side, re-arm after a 0.25σ retreat (synthesis §6.5).
- Probabilistic lights are Brier-scored at 1, 4 and 8 quarters.
- **Moved to decision cards:** α\* and QDD (action evidence, not state) and private-credit defaults (group panel).
- **Dropped:** "mean reversion".

## 9. Design changes

1. **§4.8 P and C1 §5.7:** the §4.3 table; F_t defined; the reserve keyed to the exit-window posterior.
2. **§4.1 E:**
   - the stress filter alongside the 4-state HSMM;
   - the §6.1 initialization: futures-curve oil state and duration-conditioned GW dwell;
   - non-anticipative F_t on simulated paths.
3. **§4.6:** define "fragility rising" as F_t − F_{t−3} ≥ 0.05.
4. **§5.3 G2:** freeze and hash π0, e0, Z0, F_t, the draw expectation and their data timestamps.
5. **§5.5:** the `F` variable with its version hash; the loss-monotonicity type rule.
6. **§4.10 R7, L11, §4.9, §6.7:** rename to k_MS. **C3 R12:** F_y → FR_y.
7. **§6.7:** replace "early warnings" with the §8 panel.
8. **§8 validation:**
   - the F_t harness as an annual model-risk test (purge, embargo, Holm, both halves);
   - the back-check gate on Z decompositions.
9. **§7.2:** add ADIC's own VM history, bid history and draw history as harness targets, replacing the US proxies.

## 10. Limitations

- **Targets are US proxies.** CRED6 and EXIT6 proxy secondary discounts and exits; VM1 is a stylized book rather than ADIC's CSAs.
- **Overlap shrinks the sample.** DD3's 85 events form roughly 30 independent episodes.
- **The production filter is richer.** It will have about 20 factors, and the harness must be rerun on it.
- **Elicited and assumed inputs.** The exit-chain off-diagonals and the Z0 likelihoods are [I]. The draw model uses C3 defaults, and $d_{2026}$ is unknown.
- **Narrow valuation test.** It covers one market over one regime of rising multiples. AQR and Asness–Ilmanen–Maloney report the same weakness across markets.

## Sources

**Literature**
- Kritzman & Li (2010), "Skulls, financial turbulence, and risk management," *FAJ* 66(5):30–41. DOI 10.2469/faj.v66.n5.3. https://ideas.repec.org/a/taf/ufajxx/v66y2010i5p30-41.html
- Kritzman, Li, Page & Rigobon (2011), "Principal components as a measure of systemic risk," *JPM* 37(4):112–126 (Summer 2011). DOI 10.3905/jpm.2011.37.4.112. https://globalmarkets.statestreet.com/research/portal/insights/article/2a8e282a-343b-443c-b362-1634c71d2d26
- Kritzman, Page & Turkington (2012), "Regime shifts: implications for dynamic strategies," *FAJ* 68(3):22–39. https://ideas.repec.org/a/taf/ufajxx/v68y2012i3p22-39.html
- Gilchrist & Zakrajšek (2012), *AER* 102(4):1692–1720. https://www.nber.org/papers/w17021
- López de Prado (2018), *Advances in Financial Machine Learning*, Wiley, ch. 7. https://www.lehmanns.de/isbn/978-1-119-48208-6
- Clark & West (2007), *J. Econometrics* 138(1):291–311. https://ideas.repec.org/p/fip/fedkrw/rwp05-05.html
- Campbell & Thompson (2008), *RFS* 21(4):1509–1531. https://nber.org/papers/w11468
- Goyal, Welch & Zafirov (2024), *RFS* 37(11):3490–3557. https://sfi.ch/en/publications/a-comprehensive-2022-look-at-the-empirical-performance-of-equity-premium-prediction
- Asness, Ilmanen & Maloney (2017), "Market timing: sin a little," *JOIM* 15(3):23–40. https://www.aqr.com/library/journal-articles/market-timing-sin-a-little
- Moskowitz, Ooi & Pedersen (2012), *JFE* 104(2):228–250. https://papers.ssrn.com/abstract=2089463
- Ready (2018), *Review of Finance* 22(1):155–176. https://doi.org/10.1093/rof/rfw071
- Long, Sim & Zhou (2023); Aumann & Serrano (2008): as in the synthesis bibliography.

**Industry and official documents**
- AQR (Jan 2026), *2026 Capital Market Assumptions*, pp. 2–4. https://www.aqr.com/Insights/Research/Alternative-Thinking/2026-Capital-Market-Assumptions-for-Major-Asset-Classes
- J.P. Morgan AM, *2026 LTCMA*, Exhibit 6. https://am.jpmorgan.com/us/en/asset-management/institutional/insights/portfolio-insights/ltcma
- MSCI (Oct 2026), *Private Capital Benchmarks Summary Q2 2026*, pp. 12–13. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
- EIA STEO and the IMF WEO/DataMapper (October 2026), via stream 03 and its verifier.

**Data**, accessed 18 Oct 2026
- Ken French Data Library: factors and 49 industries, daily, built from 202608 CRSP. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- Federal Reserve Board: Gürkaynak–Sack–Wright yield curve (feds200628) and the EBP file.
- Ritter IPO data. https://site.warrington.ufl.edu/ritter/files/IPOALL.xlsx
- Cboe VIX and SPX histories. https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv
- EIA Brent spot (RBRTE). https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=D
- multpl.com: Shiller CAPE and CPI, by month. https://www.multpl.com/shiller-pe/table/by-month and https://www.multpl.com/cpi/table/by-month

## Citation corrections (2026-10-18)

- Sources, Kritzman & Li (2010): added DOI 10.2469/faj.v66.n5.3. The metadata was already correct (`research/literature/recheck/10_scenarios_robustness.recheck.md`, row 21).
- Sources, Kritzman, Li, Page & Rigobon (2011): "*JPM*, Summer 2011" is now "*JPM* 37(4):112–126 (Summer 2011)", with DOI 10.3905/jpm.2011.37.4.112 (same re-check, row 22).
- In stream 10 both works are orphan references. Here they are cited where they are used (§1, §3.1, §4.1 and panel row 11), which is the resolution that re-check recommends. No change to the text.
