# G13 — Real Assets marks: underwritten, appraisal-based current, forecast and market-implied

## Smoothing, bias and credibility for the Forward Belief Engine

**Date:** 2026-10-18 · **Stream:** G13 (Real Assets, the eighth group) · **Status:** research dossier, design-grade · **Companions:** main report §4.2–4.4 (FBE), groups synthesis §5–§6, literature synthesis §4.10, and the Real Assets streams G10 (real-estate engine), G12 (energy and natural resources), G14 (actions and financing) and G15 (cash map and book).

> **SYNTHETIC-DATA NOTICE.** Every ADIC holding, parameter default and simulation result here is synthetic or a working assumption. None is ADIC data, and none may be presented as ADIC data. Simulation tables end with *SYNTHETIC – NOT ADIC DATA*. Public market figures are dated and sourced.

**Scope (context §1A, re-read before finalizing).** The user has confirmed the sectors: **real estate, infrastructure, and energy & natural resources. Agriculture and timber are excluded.**
- *Vehicles:* funds, co-investments, and direct assets or joint ventures.
- *Allocation:* part of the ≈60% private allocation. No size was given, so the working figure stays at $18bn of NAV with ≈$4bn unfunded.
- *Oil link:* energy and natural-resource holdings add oil exposure that is wrong-way with the owner's draw.
- *Still open:* whether "funds" include open-end vehicles (G14 open question 1).
- *Census:* G13 uses G15's synthetic sleeve book (§6.7).

**Tags.** [S] sourced, read in session · [S-sec] via secondary summary or abstract · [P] practitioner consensus · [I] inference or default · [I-calc] synthetic arithmetic (`research/groups/addenda/G13_calcs/`) · [U] unverified.

**Calculations.** `g13_ra_marks_sim.py` (venv, `python -I -B`, fixed seeds) holds the generator, the estimators, tests R1–R9 and V-RA1, and illustrations P1–P4, and writes `g13_ra_marks_results.json`. `g13_part2.py` re-runs V-RA1, R4–R9 and P with the same seeds and writes `…_part2.json`.

---

## 1. Executive summary

The Real Assets group's "current actual" mark is an **appraisal**, and an appraisal is a filter of value, not a price. It lags, smooths and carries calendar noise, and it is most wrong at turning points. G13 specifies the **Real-Assets Mark Engine (RAME)**, the part of the Forward Belief Engine (FBE) that:
- turns the four real-asset marks into one nowcast of economic value $V^*$ and one fused forward return;
- generates and tests those marks in SYN-ADIC-177.

**Eight findings**

1. **Smoothing is large and it hides risk.**
   - *Private real-estate funds:* on 66 NCREIF funds (1994–2017), fund-level first-order autocorrelation is 0.45 and the aggregate's is 0.75. Volatility rises from 13.1% to 24.1% after unsmoothing; beta to listed real estate rises from 0.07 to 0.34; one-factor alpha falls from 4.3% to 1.6% (Couts, Gonçalves & Rossi 2024, "CGR") [S].
   - *Unlisted infrastructure:* NAV indices show 3.1–3.3% volatility over ten years, with a 0.00% maximum drawdown on MSCI's index (SIPA report for GPIF, 2024) [S].
   - *Appraisals against sales:* NCREIF sale prices differ from the appraisal two quarters earlier by 12.5% on average, by −12.0% in 2008 and by up to +14.7% in booms. More than half of the signed error is predictable (Cannon & Cole 2011) [S].
2. **Smoothing, lag and noise are three separate problems.**
   - AR unsmoothing removes smoothing but not the reporting lag.
   - Appraisal-calendar noise biases OLS smoothing estimates down: 0.64 against a true 0.75 in SYN [I-calc].
   - Fund-by-fund unsmoothing leaves the aggregate smoothed (CGR).
   - RAME therefore uses a seven-state Kalman *appraisal model*, observed through appraisals, unlevered listed proxies, transaction-negotiated indices and secondary bids. It is estimated by MLE with QMLE (sandwich) errors, with CGR's three-step method for the cross-section.
3. **Market-implied anchors disagree with appraisals, by sector, today.**
   - REITs trade at a 9.35% median discount to NAV (30 Jul 2026; 16–18% around year-end).
   - Green Street's CPPI is 16% below its 2022 peak (office −35%) and +4.7% over 12 months.
   - NFI-ODCE made +1.49% in 2Q-2026 after a 7-quarter, −18.8% drawdown that trailed REITs, with −$8.7bn of net flows in the year.
   - LP stakes price at 68% of NAV for real estate and 91% for infrastructure (Jefferies H1-2026) [S]. That implies economic-to-reported NAV of ≈0.74–0.78 for traded real-estate stakes and ≈1.0 for infrastructure, which are upper bounds on staleness.
   - HICL's 24% discount implies an 11.3–12.2% discount rate, against the 8.5% used [I-calc].
4. **Bias differs by level.**
   - *Deal underwriting is optimistic.* 2Q-2022 multifamily underwriting assumed 4.3% a year rent growth; rents then grew ≈1% and values fell 19%. Toll-road traffic averages 23% below forecast; electricity projects overrun by 66% on average.
   - *Market consensus is smoothed.* It underestimates booms and overestimates busts, and fails mainly on yields [S].
   - *Re-forecasts anchor on stale appraisal cap rates.*
   - So the bias model is component-level, stateful and controlled for the desmoothed common shock.
5. **Stale NAVs are a SELL option for leavers and a cost for stayers.**
   - Before queues, NAV-timing strategies in open-end real-estate funds earned 18.2% a year of alpha (2004–15). Queues remove it; cash buffers amplify it (Couts 2025) [S].
   - BREIT's NAV was up ≈8.5% to October 2022 while comparable REITs were down ≈30%, and redemptions hit its 2%-a-month limit [S].
   - Leverage multiplies staleness at equity level: $\theta^{eq}-1=(\theta-1)/(1-L)$. A 10% asset overstatement is a 25% equity overstatement in G15's 60%-LTV value-add sleeves [I-calc].
6. **The estimators work on SYN-ADIC-177** [I-calc].
   - *The generator matches the evidence:* aggregate autocorrelation of 0.47 after one-step and 0.00 after three-step (CGR: 0.46, −0.02); appraisal-to-sale mean absolute error 12.5%, and −11.5% in crash quarters.
   - *Recovery:* with listed and transaction signals, the Kalman model recovers smoothing within 0.01 and cuts nowcast error from 8.8–10.8% to 2.5–3.1% (5.3–7.3% with listed data alone). Three-step desmoothing recovers 75–85% of true fund beta, against 25–48% observed.
   - *Bias estimation:* forecast bias is unidentifiable from one cycle without a desmoothed common-shock control. Its dispersion is ±6.6–8.3pp per 8 quarters naive and ±1.5–2.6pp with the control.
   - *Scoring and fusion:* appraisal-based scoring rewards stale forecasters. GLS weights estimated on 40 pairs lose 8% MSE to equal weights.
   - *Closed-end funds:* incurred Benktander on economic TVPI is best or tied at every age, and paid-triangle BF fails for exit-driven funds.
7. **Design.** RAME:
   - desmooths appreciation only, unlevered, segment by segment;
   - translates every mark onto $V^*$ using the *economic* cap rate;
   - scores components against unsmoothed outcomes (NOI, sales, completions, traffic);
   - fuses with 50% shrinkage toward equal weights and recalibrates pools;
   - feeds $V^*$, $\theta^{eq}$ and desmoothed betas to SELL / HOLD / REFINANCE / LEVER, to Corporate Finance's covenant-cure ladder and to the overlay's hedge ratios (§6).
8. **Data ADIC must supply:**
   - appraisal histories with valuation dates and valuer type;
   - quarterly NOI and debt tapes;
   - underwriting components and a point-in-time forecast archive;
   - sale-versus-last-appraisal records;
   - open-end queue positions, if any;
   - energy price decks (§6.8).

## 2. Core concepts and theory

### 2.1 Four marks, four different objects

| Mark | What it is | Dominant distortion | Role in RAME |
|---|---|---|---|
| **Underwritten** | IC plan at entry: price, yield-on-cost, NOI path, exit cap, capex, schedule, IRR | Inside-view optimism, winner's curse, strategic misrepresentation (development, demand) | A belief: debias, then translate to the remaining-plan return on $V^*$ |
| **Current (appraisal NAV)** | Valuer estimate: external about yearly, otherwise internal or carried forward | Smoothing λ, lag ℓ, calendar noise, seasonality, regime asymmetry | A *measurement* of value inside a state-space model; never a return signal on its own |
| **Group forecast** | Business-plan re-forecast: NOI, capex, exit cap, sale date | Anchoring on appraisal cap rate and plan; optimism; "defend the holding" | A belief: debias, translate onto $V^*$ |
| **Market-implied** | Listed REIT or infrastructure prices, transaction-negotiated indices, secondary bids, commodity strips | Sentiment premium, liquidity and fee premia, sector mismatch, selection | A timely noisy *price*: a level anchor for $V^*$ and a yield-based forward return |

Only the beliefs enter the forecaster-bias model. Appraisals and market signals enter the measurement model that produces the nowcast every belief is translated onto.

### 2.2 Value identity and return decomposition

$$V_t=\frac{N_t}{c_t},\qquad v_t=n_t-\kappa_t,\qquad r_{t+1}\approx y_t+\Delta n_{t+1}-\Delta\kappa_{t+1},\qquad y_t=c_t(1-\text{capex share}).$$

- **Cap rates predict.** They are persistent and predict both returns and rent growth (Plazzi, Torous & Valkanov 2010) [S]. So $E_t r_{t+h}\approx h(\bar y+g)+(1-\phi_\kappa^h)(\kappa_t-\bar\kappa)$ [I].
- **Infrastructure** uses the equity discount rate in place of the cap rate. On a 30-year project, a 100bp discount-rate error matters more than a 20% cash-flow error (SIPA for GPIF) [S].
- **Energy** replaces N with reserve netbacks under the strip (G12 §2.4).

Two design consequences [I]:
- *Income is observed and value is not,* so desmooth appreciation only. NCREIF's 2Q-2026 income return of 1.02% is cash [S].
- *The decomposition is scoreable:* NOI, capex, completion dates and traffic are observed unsmoothed.

### 2.3 Why appraisals smooth, lag and mislead at turning points

**The model.** An appraiser who receives noisy transaction signals optimally weights the prior value against new evidence (Quan & Quigley 1991) [S]. Geltner (1991, 1993) gives the partial-adjustment model; the 1993 paper drops the efficient-market assumption [S]. Smoothing appears in individual appraisals, not only in indices (Clayton, Geltner & Hamilton 2001), and valuers anchor on prior values (Diaz & Wolverton 1998) [S].

$$a_t=(1-\lambda)v_{t-\ell}+\lambda a_{t-1}+e_t,\qquad \frac{\operatorname{Var}\Delta a}{\operatorname{Var}\Delta v}=\frac{1-\lambda}{1+\lambda}\ \ (\text{i.i.d. }\Delta v,\ e=0).$$

**Five refinements:**
1. **Lag is not smoothing.** Inversion recovers $r^V_{t-\ell}$, not $r^V_t$.
2. **Aggregate and idiosyncratic news are smoothed differently.** Weights are φ on relative returns and π on aggregate returns, so fund-by-fund unsmoothing leaves the aggregate smoothed (CGR 2024) [S].
3. **Smoothing switches with the regime** (Lizieri, Satchell & Wongwachara 2012) [S].
4. **Calendars add noise and seasonality.** About half of NCREIF properties sold in 1984–2010 had no appraisal in the two quarters before sale (Cannon & Cole) [S].
5. **Liquidity is cyclical.** Constant-liquidity values lead both transaction and appraisal indices (Fisher, Gatzlaff, Geltner & Haurin 2003) [S].

### 2.4 Price discovery runs from listed to private

- **Securitized markets discover first.** Price discovery happens in securitized markets, and information takes "a year or more" to reach US unsecuritized markets (Barkham & Geltner 1995) [S-sec: abstract].
- **REITs carry fundamental information.** REITs transmit it to private markets; passive unlevered core REITs beat their private benchmark by ≈49bp a year, 1994–2012 (Ling & Naranjo 2015) [S: abstract].
- **Other indices are late.** Green Street notes that appraisal and closed-transaction indices reflect prices "from several months earlier" [S].
- **But listed prices carry a premium.** They are the timeliest signal, but carry a persistent, sentiment-driven premium or discount $p_t$ to private value [I].

### 2.5 Stale NAVs move wealth in open-end funds

$$W=\sum_t \text{paid}_t\Big(\frac{NAV_t}{V_t}-1\Big)\quad(\text{gain to leavers when }NAV>V,\text{ paid by stayers}).$$

Open-end private real-estate fund returns are stale and predictable, so NAV-timing moves wealth and creates fragility. Discretionary queues protect stayers; buffers do not, and amplify the transfer when added to queues (Couts 2025) [S]. ADIC holds an option on staleness as a redeemer and writes one as a stayer.

### 2.6 Bias channels with opposite signs

- **Deal-level underwriting is optimistic.** Causes are the inside view (Kahneman–Lovallo, via stream 07), the winner's curse in concession auctions (Oxera 2012) [S], and strategic misrepresentation, "lie" rather than "error" (Flyvbjerg, Holm & Buhl 2002) [S-sec].
- **Market-level consensus is smoothed.** UK real-estate forecasts underestimate booms and overestimate recessions (Papastamos, Matysiak & Stevenson 2018). Yield forecasts drive capital-growth errors, and the IPF consensus shows a pessimism bias (McAllister & Nase 2020) [S: abstracts].
- **Re-forecasts anchor on the appraisal.** A plan's exit cap is typically the appraisal cap rate plus a spread [P], so it inherits the lag: too optimistic after cap rates rise, too pessimistic after they fall [I].

### 2.7 Market-implied marks as identities

- **Listed proxy:** $\Delta\ell^U_t=\beta_L\Delta v_t+\Delta p_t+\varepsilon_t$ after unlevering [I].
- **Secondary bid** (stream 05): $\theta=V^*/NAV=p\,[(1+y_P)/(1+y_V)]^D$. Here p is price ÷ NAV, $y_P$ the buyer target, $y_V$ the fund's expected return and D the remaining duration [I].
- **Listed infrastructure trust:** $r^{mkt}\approx r^A+\text{gap}/S$, where S is the NAV sensitivity per 1% of discount rate (P1 also uses a convex form) [I].
- **Energy:** SEC reserves use a 12-month average price, so PV-10 lags the strip by about six months; the strip is the market-implied mark (G12) [S via G12].

## 3. Methods and models: trade-offs

### 3.1 Desmoothing and nowcasting methods

| Method | Strength | Weakness | Role |
|---|---|---|---|
| Geltner 1-step AR (1991, 1993) | Simple, IC-legible | Leaves lag; λ biased low by calendar noise (R1); aggregate smoothing survives per-fund use | Challenger, reported |
| Fisher–Geltner–Webb (1994); Getmansky–Lo–Makarov (2004) MA(k) | Classic index reverse engineering; unconstrained MA weights | Judgmental "confidence factor" [P]; long series; same aggregation gap | Historical calibration; hedge-fund parity |
| **CGR 3-step (2024)** | Removes aggregate autocorrelation; better betas and alphas | Needs ≥10 funds per segment; no lag correction | **Cross-sectional step** |
| Regime TAR (Lizieri et al. 2012) | Asymmetric smoothing | Regime choice | Variant M_regime |
| Dimson (1979) lagged betas | No unsmoothing needed | Inefficient with many factors (CGR) | Beta cross-check |
| Transaction / repeat-sales indices (Fisher, Geltner & Pollakowski 2007) | Unsmoothed | Sparse, noisy; liquidity selection | **Observation** in the state-space model |
| Bayesian structural time series (Bokhari & Geltner 2012) | High frequency from scarce trades | Model choice | Builds τ where none exists |
| **State-space appraisal model** (Kalman; cf. Brown, Ghysels & Gredil 2023 for PE) | Lag, smoothing, noise and staleness in one likelihood; dynamic credibility; nowcast with a band | Model risk; needs priors and robust SEs | **Core of RAME** |

### 3.2 The state-space appraisal model

The state per segment is $\alpha_t=[v_t,v_{t-1},v_{t-2},v_{t-3},p_t,s_t,e_t]'$:

$$\begin{aligned}
v_t&=\mu+v_{t-1}+\eta_t, & p_t&=\phi_p p_{t-1}+\zeta_t,\\
s_t&=\lambda(z_t,q_t)\,s_{t-1}+(1-\lambda(z_t,q_t))\,v_{t-\ell}, & e_t&=0.75\,e_{t-1}+\xi_t,\\
a_t&=s_t+e_t\ \ (\text{appraisal index}), & \ell^U_t-c_L&=\beta_Lv_t+p_t+\varepsilon^L_t\ \ (\text{listed}),\\
\tau_t&=v_t+\varepsilon^\tau_t\ \ (\text{transactions}), & \ln q_{j,t}&=v_{j,t}-a_{j,t}-D_j(y_P-y_V)+\varepsilon^q\ \ (\text{bids}).
\end{aligned}$$

- **Estimation.** MLE (MAP with weak priors in production) over $(\lambda,\mu,\sigma_v,\sigma_\xi,\beta_L,\phi_p,\sigma_p,\sigma_L,\sigma_\tau,c_L)$, with bounded transforms and three starts.
- **Lag.** ℓ ∈ {0,…,3} by profile likelihood.
- **Uncertainty.** QMLE sandwich errors (Newey–West J), because the random-walk state deliberately simplifies mean-reverting cap rates and regimes. Even so, λ-interval coverage reaches only 0.73–0.87 in R1, so production uses a parametric bootstrap.
- **Variants.** λ may depend on the regime $z_t$ and on the Q4 external-appraisal quarter $q_t$ (variants M_regime, M_season).
- **Missing data.** Missing observations are skipped, so annual appraisals, monthly listed prices and sparse trades mix freely.
- **Calendar noise as a state.** Treating $e_t$ as a state is what removes the downward bias in λ (§7).

### 3.3 Bias and credibility methods

**Component bias model** (extends groups synthesis §5). For component c ∈ {NOI growth, exit cap, capex, schedule, demand}:

$$e^c_{i,t}=\text{outcome}-\text{forecast}=-b^c_s-b^c_D\mathbb1\{D_t\}-w^c_a(\text{trailing appraisal signal}-\hat m_{i,t})+\delta^c\,\widehat{CS}_{s,t}+\varepsilon_{i,t},$$

where $\widehat{CS}_{s,t}$ is the realized *desmoothed* common segment shock over the horizon.

- **The common-shock control is essential.** In R4 (40 assets, 8 annual forecast dates) the naive intercept is unbiased across worlds, but its dispersion is ±6.6–8.3pp per 8 quarters.
  - With a nowcast-quality control: ±1.5–2.6pp.
  - With the *appraisal* index as control: ±5.0–6.6pp.
  - Coverage of nominal-90% intervals: 16–28% with iid errors; 59–68% date-clustered; 74–81% with control plus a small-cluster t. The anchoring weight is biased up without the control (0.33–0.41 against 0.30) and recovered with it (0.30–0.31) [I-calc].
- **Learning speeds differ by component** [I].
  - NOI growth: Bühlmann–Straub on quarterly NOI reaches $n_{eff}\ge20$ in 1–2 years.
  - Exit cap: observed only at sales, so shrink hard to the reference-class prior.
  - Capex, schedule and demand: reference-class priors (Green Book, Flyvbjerg, Sovacool, Bain), updated at each completion.
- **Overconfidence:** $\kappa=w_{80}(\text{true})/w_{80}(\text{stated})$ (groups synthesis §5), estimated from coverage after debiasing. R5 recovers it within 0.06 (1.66, 1.94, 1.69, 1.95 against 1.67, 2.0, 1.67, 2.0) [I-calc].

### 3.4 Fusion and scoring

**Fusion.** The literature synthesis (§4.10) contradicts pure constrained-GLS fusion. RAME's rules:
- keep covariances in the predictive variance;
- shrink weights 50% toward equal until $n_{eff}\ge20$;
- adopt GLS only if it beats equal and screened averages out of sample;
- recalibrate pools with a beta-transformed linear pool (Ranjan & Gneiting 2010);
- cap credibility beyond about 8 quarters;
- use parameter-free Benktander until t is estimated (Neuhaus 2025).

In R7, GLS weights estimated on 40 pairs give an out-of-sample MSE 8% above equal weights (P90 13% above); 50% shrinkage matches equal weights. With the full sample, all weightings sit within 1%. GLS gives the appraisal-yield view a negative weight (−0.16), and constrained GLS gives it zero, which is why RAME excludes that view from fusion [I-calc].

**Scoring.** Never score real-asset forecasts against appraisal-based returns.
- In R6, a forecaster who predicts the *appraisal* process halves the MSE of an honest forecaster against appraisal outcomes (0.0033 vs 0.0066), but loses against true outcomes (0.0132 vs 0.0107) and transaction-index outcomes (0.0142 vs 0.0118) [I-calc].
- Score each component against its unsmoothed outcome, and total return against the desmoothed nowcast with its variance added to the target noise.
- Use WIS as the headline score, with autocorrelation-robust PIT tests for overlapping horizons (Knüppel 2015).

## 4. Empirical evidence and current market data

### 4.1 Smoothing and lag

| Evidence | Value | Sample, as-of | Source |
|---|---|---|---|
| Private CRE fund autocorrelation | Fund AC1 0.45 (63.6% significant); aggregate AC1 0.75, AC4 0.31; aggregate AC1 0.46 after 1-step (Geltner AR(2)), −0.02 after 3-step | 66 NCREIF funds, 1994–2017 | CGR 2024, Table 6 [S] |
| Fund risk and performance: observed → 1-step → 3-step | Volatility 13.1 → 25.3 → 24.1%; β to public CRE 0.07 → 0.22 → 0.34; 1-factor α 4.3 → 2.7 → 1.6%; 2-factor α 4.0 → 2.4 → 0.8% | Same | CGR, Table 7 [S] |
| Unlisted infrastructure NAV indices | 10-year return 10.41% / 13.42%, volatility 3.11% / 3.26% (Preqin / MSCI); MSCI maximum drawdown 0.00%. Fund appraisal-NAV volatility 2.7–2.9% (13 funds, ≈$23.4bn) | To 2024 | SIPA for GPIF, Sep 2024 [S] |
| ODCE against REITs | ODCE 2022 +7.5%, 2023 −12.0%, 2024 −1.4%, 2025 +3.8%; peak-to-trough −18.8% over 7 quarters (3Q-22 to 2Q-24). REITs 2022 −24.95%, 2023 +11.4%, 2025 +2.27% | 2022–25 | NCREIF webinar, 16 Sep 2026 [S]; Nareit [S-sec]; P3 [I-calc] |
| Latest quarter | 2Q-2026: FTSE Nareit +10.7%, NFI-ODCE +1.5%, NPI +1.3% | 30 Jun 2026 | NCREIF [S] |

### 4.2 Appraisals against transactions

- **Cannon & Cole (2011): NCREIF NPI sales, 1984–2010, against the appraisal two quarters earlier** [S].
  - Size: mean absolute difference 12.5% (median 8.1%); 4–5% at portfolio level.
  - Cycle: signed error −12.0% (2008), −8.9% (2009) and −2.5% to −8.9% (1988–93); +2.9% to +14.7% in the 1996–99 and 2002–07 booms.
  - External appraisals were no better: −15.6% in 1990, −20.2% in 2008, +16.2% in 2006, and a mean absolute error of 11.7% against 10.8% for internal ones.
  - More than half of the signed error is explained by observables.
- **EDHEC survey, *Fair Value or Fair Guess?* (Jun 2025).** Most respondents exited above internal valuations, "predominantly" at premiums of 6–20%. Only a third adjust valuations in stress [S-sec]. Exit premia are *selected*.
- **HICL Infrastructure, year to 31 Mar 2026** [S].
  - Valuation: weighted-average discount rate 8.5% (8.4% a year earlier), equity risk premium 3.5%; ±0.5% on the discount rate moves NAV by −6.8p / +7.4p on 160.2p.
  - Market: share discount narrowed from 28% to 24%.
  - Transactions: a PPP portfolio sold at carrying value, and the A63 at a 21% premium to the September 2025 valuation.
- **UK FCA multi-firm review (5 Mar 2025).** Most firms had no formal ad hoc revaluation process and waited for the next cycle in market events. The FCA asks for defined triggers "to mitigate the risk of stale valuations" and finds exit backtesting useful. Infrastructure valuers use the income approach [S].

### 4.3 Market-implied marks, October 2026

| Signal | Value | As of | Source |
|---|---|---|---|
| US equity REITs, median discount to consensus NAV | 9.35% (industrial 9.87%, office 22.37%) | 30 Jul 2026 | S&P Global MI via *Commercial Property Executive* [S] |
| Same series earlier | 16.2% (end-Jan 2026; page title); 18.3% at 31 Dec 2025 | Feb 2026 | S&P Global [S-sec: page returned 403] |
| Green Street CPPI | −0.1% in September; +4.7% over 12 months | 6 Oct 2026 | Green Street [S] |
| CPPI from the 2022 peak | All property −16% (−15.5%); apartment −19%; industrial −12%; office −35%; data center −9%; self-storage −22% | 6 May 2026 | Green Street [S] |
| NFI-ODCE | +1.49% gross (income 1.02%, appreciation 0.47%); 1-year +4.45%; leverage 27.1% (average since 2000: 22.4%); 25 funds, $280.4bn gross / $223.7bn net | 2Q-2026 | NCREIF, 30 Jul 2026 [S] |
| NFI-ODCE flows | Net −$2.8bn in the quarter; year: contributions $10.4bn, redemptions and distributions $19.1bn, net −$8.7bn (≈−3.9% of NAV) | Year to Jun 2026 | NCREIF [S] |
| LP secondary pricing (% NAV) | Real estate 68 (83 in 2019, 71 in 2022, 70 in 2025); infrastructure and energy 91; all strategies 87. Real estate "settled at 68%"; energy volatility raised upstream-fund pricing | H1-2026 | Jefferies, Jul 2026 [S] |
| LP-led discounts | Infrastructure 5.0%; real estate "significant", improved 6.0%; energy improved 9.2% | H1-2026 | Campbell Lutyens, via G14 §4.1 |
| Listed infrastructure (HICL) | 24% discount → market-implied discount rate 11.3% (linear) to 12.2% (convex), against 8.5% appraisal | 31 Mar 2026 | HICL [S]; P1 [I-calc] |

**P2, secondary-implied staleness** [I-calc].
- *Real estate:* θ = 0.68 × (1.14/1.09)³ ≈ 0.78 with a 5-point buyer premium over the fund's expected return, or 0.74 with a 3-point premium (D = 3 years).
- *Infrastructure:* θ ≈ 0.97 (2-point premium) to 1.03 (4-point premium; D = 3.5 years).
- *Reading:* these are upper bounds, because price-to-NAV also prices liquidity and the buyer's selection, and the traded stock is not ADIC's stock.

### 4.4 Underwriting and forecast bias

| Channel | Evidence | Source |
|---|---|---|
| Rent growth and exit cap at the peak | 2Q-2022 prime multifamily underwriting: 4.3% a year rent growth over 3 years (1.8% in the 2020 survey); going-in cap 3.76%, exit 4.43% | CBRE, 21 Jul 2022 [S] |
| Outcome | US asking-rent growth "just above 1%" a year from mid-2023 into 2025; apartment values −19% from the 2022 peak | CoStar via BusinessWire [S-sec]; Green Street [S] |
| Exit-cap arithmetic | At c = 5%, a 75bp exit-cap error costs ≈−3.0pp a year over 5 years ($\Delta c/c/H$) | [I] |
| Toll-road demand | Actual traffic on average 23% below forecast, more than 100 concessions; earlier S&P studies give first-year ratios of 0.73–0.77 with no improvement in years 1–5 | Bain 2009 via Oxera 2012 [S]; BITRE/TRB [S-sec] |
| Transport capex | Average overrun 28% across 258 projects worth $90bn | Flyvbjerg, Holm & Buhl 2002 [S-sec] |
| Electricity capex | 401 projects in 57 countries: mean overrun 66.3%; hydro and nuclear worst, solar and wind least | Sovacool, Gilbert & Nugent 2014 [S-sec: abstract] |
| Megaprojects | About 1 in 200 of 16,000+ projects met budget, schedule and benefits | Flyvbjerg & Gardner 2023, via WSJ review [S-sec] |
| Institutional uplifts | Upper-bound works-duration / capex optimism: standard buildings 4% / 24%; non-standard civil engineering 25% / 66%; equipment and development 54% / 200% | HM Treasury Green Book, via stream 07 [S] |
| Consensus forecasts | Smoothed (boom under, bust over); yields the main failure; IPF pessimism bias | Papastamos et al. 2018; McAllister & Nase 2020 [S: abstracts] |
| Fund-level outcomes | Infrastructure fund cash flows as volatile and cyclical as PE (633 funds); strip-based profit −17¢ per $ for real estate and −10¢ for infrastructure (working paper) | Andonov, Kräussl & Rauh 2021 [S-sec]; Gupta & Van Nieuwerburgh, via stream 04 [S] |

### 4.5 Stale NAVs and flows

- **Couts (2025; working paper Nov 2022), NCREIF NFI-OE, 2004–15** [S].
  - Before queues, NAV timing earned 18.2% (index vs T-bills) and 5.9% (quintiles) of annual alpha.
  - Subscription requests rise 18%, 21% and 43% of an SD per 1-SD rise in lagged public, private and fund returns.
  - Queue-adjusted returns equal buy-and-hold, and lock-ups and one-quarter notice do not protect.
  - Median cash was 3.6%; a 1-SD rise in cash raised outflows by 25.8% of an SD.
- **BREIT and SREIT, 2022** [S: *Financial Advisor*, 6 Dec 2022].
  - Returns to October were ≈8.5% and 10.2%, against ≈−30% for similar public REITs.
  - In November BREIT paid its 2%-of-NAV limit (≈$1.3bn, ≈43% of each request); SREIT paid 63%.
  - P4 [I-calc]: if true value fell by half to all of the unlevered REIT move, NAV was 20–35% overstated, and each 2% monthly redemption moved 0.4–0.7% of NAV to leavers. Illustration only.

## 5. Practitioner practice and case studies

1. **Calendars and triggers** [S/P]. Carried-forward values drive most appraisal bias: when either an internal or external appraisal was made, the bias fell by more than two-thirds (Cannon & Cole). Good practice since the FCA review is defined ad hoc revaluation triggers plus exit backtesting.
2. **Green Street CPPI** [S]. An unlevered, value-weighted index from NAV models of REIT portfolios, driven by market cap rates and NOI. It is RAME's τ for US core sectors.
3. **Market-based infrastructure pricing** [S/P]. SIPA's GPIF work prices unlisted infrastructure with a Kalman filter on factor risk premia from 1,000+ deals. Segment-level average pricing errors run from −2.1% to +0.6%, and the indices show no serial correlation. This is τ for infrastructure; note the vendor's interest.
4. **HICL, 2025–26: two market signals disagree** [S/I]. The listed discount implies a discount rate 2.8–3.7pp above the one used, yet disposals cleared at book or +21%. Read this as selection plus a listed-vehicle discount (gearing, fees, sentiment). Weight trades for held assets *like those sold*; keep the listed signal as the direction-of-travel input.
5. **ODCE 2022–24 and BREIT 2022** [S/I-calc]. A REIT-informed nowcast would have marked ODCE's fall 3–6 quarters early (§4.1). That was the window in which redeeming at stale NAV paid, queues formed and BREIT's limits bit. For funds that deal at NAV, the queue is the stayers' only protection.
6. **Energy decks** [S via G12]. Lending decks sit "at a discount to the current NYMEX futures curve" and SEC reserves use a 12-month average price. A deck-based NAV can run 6–12 months behind the strip in either direction.
7. **Multifamily 2021–22 vintages** [S/I]. A component registry would have flagged these deals from observed NOI by 2023, before any appraisal caught up (§4.4).

## 6. Design implications for the ADIC framework

### 6.1 RAME's place and outputs

RAME is an FBE sub-module (main §4.3; groups synthesis §5) and changes no engine. G10, G11 and G12 simulate *true* values. RAME produces what ADIC *observes* and *believes*. Per holding and quarter it returns:
- $V^*$ with an 80% band;
- $\hat\theta=V^*/NAV^{rep}$ at asset and equity level;
- desmoothed returns and betas;
- fused $\hat\mu,\hat\sigma$ on $V^*$, with P(forecast optimistic);
- component bias states and flags F-RA1–F-RA10 (§6.3).

### 6.2 State, data and decision variables

| Symbol | Meaning | Source, frequency |
|---|---|---|
| $a_{i,t}$, $NAV^{rep}$ | Log appraisal; reported equity NAV | Valuer, GP, administrator; quarterly, external yearly; bitemporal |
| $n_{i,t}$ | Log forward NOI (cash yield for infrastructure and energy) | Operating reports; quarterly |
| $D$, DSCR, $LTV^A$, $LTV^*$ | Asset-level debt, coverage, appraisal and economic leverage | Debt tape (G14); quarterly |
| $\kappa^A=n-a$; $\kappa^*=n-\hat v$; $\kappa^L$ | Appraisal, economic and listed-implied cap rates | Derived |
| $\ell^U_{s,t}$, $\tau_{s,t}$, $q_{j,t}$, $F_t(k)$ | Unlevered listed proxy; transaction index; secondary bid ÷ NAV (desk quotes with conflict flags); strip | Market and vendors; daily to event |
| $u_i$, $f_{i,t}$ | Plan components $(g,\kappa_{exit},K,T,Q,H)$ at entry; current plan | IC memo, frozen; RA registry, quarterly |
| $\hat v,\hat P,\lambda,\ell,\beta_L,p$ | Nowcast, variance and appraisal-model parameters | RAME; re-estimated yearly, filtered quarterly |
| $b^c_s, w^c_a, \kappa$ | Component bias, anchoring, overconfidence | Bias model; yearly posterior |
| Decisions | SELL (sale, LP secondary, open-end redemption), HOLD, REFINANCE (cash-out refi, recap, sale-leaseback, JV sell-down, NAV facility), LEVER (acquisition or development debt) | Group proposes; one kernel scores (main §4.4) |

### 6.3 RAME procedure

1. **Normalize.** Split income from appreciation; unlever fund returns, $r^U=(1-L)r^E+Lr^D$, and REIT returns at reported LTV; timestamp each mark by valuation and report date.
2. **Segment nowcast** (§3.2) for core RE, value-add RE, GCC RE, core infrastructure, value-add / digital / energy-transition infrastructure, and energy & natural resources. Inputs are ADIC's appraisal index (pooled with the external benchmark for length), the listed proxy, τ and bids. Re-estimate yearly; filter quarterly.
3. **Holding nowcast.** Take the holding's appraisal plus the loading-scaled segment correction $(\hat v_s-\hat s_s)$, then apply CGR step 2.
   - An own trade or bid updates $\hat v\leftarrow\hat v+K(\ln S-\hat v)$, $K=\hat P/(\hat P+\sigma_S^2)$, with $\sigma_S$ = 0.08–0.12.
   - Equity staleness is levered: $\theta^{eq}=(\theta A-D)/(A-D)$.
4. **Translate onto $V^*$.**
   - *Underwritten:* $\rho^u$ solves $V^*_t=\sum_kCF^u_ke^{-\rho^u(k-t)}+(N^u_T/c^u_{exit})e^{-\rho^u(T-t)}$; in logs $\rho^u\approx y^*_t+g^u-(\kappa^u_{exit}-\kappa^*_t)/H^{rem}$, with the economic cap rate $\kappa^*$, not $\kappa^A$. It expires at $T^u+1$.
   - *Forecast:* the same with current-plan components.
   - *Valuation view:* $\rho^*\approx y^*+\bar g_s+(\kappa^*-\bar\kappa_s)(1-\phi_\kappa^{4H})/H$. The appraisal-yield view is shown but not fused.
   - *Market-implied:* the same with $\kappa^L$, the listed-implied discount rate, or the strip NPV.
   - *Closed-end funds:* $\hat U=c^*\,TVPI^{eco}_aLDF^{eco}_a+(1-c^*)U_0$, $c^*=1-(1-1/LDF^{eco}_a)^2$, $\rho=\ln[(\hat U-DPI)/RVPI^{eco}]/D^{rem}$. $U_0$ is the debiased outside view frozen at inception. Paid BF is a cross-check only (R8).
5. **Debias** with the component posteriors, including the anchoring and regime terms.
6. **Fuse** with precision $1/(\kappa^2\hat\sigma^2)$ shrunk 50% toward equal, keeping covariances in the predictive variance.
7. **Recalibrate** with a beta-transformed linear pool on PIT history, widening by κ until scored.
8. **Learn.** Kalman belief updates (main §4.3) run on desmoothed returns and NOI, never on appraisal changes, with credibility capped beyond 8 quarters.

**Flags:**
- F-RA1: $|\hat\theta-1|>10\%$.
- F-RA2: appraisal cap rate more than 75bp from the market-implied rate.
- F-RA3: exit cap below today's economic cap rate.
- F-RA4: NOI growth above the reference P75.
- F-RA5: capex or schedule beyond contingency.
- F-RA6: demand ramp below the reference class.
- F-RA7: open-end queue above 10% of NAV.
- F-RA8: DSCR below 1.3×, or LTV headroom below 10% on $V^*$.
- F-RA9: energy deck more than 15% from the strip.
- F-RA10: valuation older than two quarters after a trigger.

### 6.4 Bias and credibility defaults

| Segment | $b^u$ pp/yr (late cycle) | $b^f$ pp/yr | Component priors | κ (stated-80% coverage) |
|---|---|---|---|---|
| Core RE | +1.5 (+3.0) | +1.0 | NOI +0.5pp; exit cap +25bp (+50bp late) | 1.67 (56%) |
| Value-add / opportunistic RE | +4.0 (+5.5) | +2.5 | NOI +1.5pp; exit cap +50bp (+75bp); lease-up +2q; capex ln-overrun N(0.10, 0.20²) | 2.00 (48%) |
| RE development | +6.0 | +3.5 | Capex and schedule N(0.15, 0.25²) (Green Book building bands) | 2.22 (44%) |
| GCC RE (JV, direct) | +2.0 (+3.5 when oil is weak) | +1.5 | Local appraisals λ ≈ 0.80, ℓ 1–2; weak listed proxy; oil and fiscal loading | 2.00 (48%) |
| Core infrastructure | +1.0 (+2.0) | +0.75 | Appraisal discount rate closes ≈15% of the gap a quarter (λ ≈ 0.85); demand ≈0 (brownfield) | 1.67 (56%) |
| Value-add / digital / energy-transition infrastructure | +3.0 (+4.0) | +2.0 | Greenfield transport demand N(ln 0.77, 0.30²); renewables capex N(0.05, 0.15²); grid and data-centre connection +2–4q | 2.00 (48%) |
| Energy & natural resources | +3.0 | +2.0 | Deck ≈2 quarters behind the strip (G12); reserve revisions | 2.22 (44%) |

All [I]. $w_a$ = 0.30 everywhere (Campbell–Sharpe-type anchoring, groups synthesis O4).
- *Levels:* scaled from the groups synthesis priors (PE +5.0/+3.0; private credit +0.75) by leverage and exit dependence.
- *Component anchors:* §4.4.
- *Estimation:* the groups synthesis machinery (FBE-R Huber, κ ≥ 1, inverse-propensity weights for declined deals), plus the desmoothed common-shock control.

**Credibility** is prior precision plus $n_{eff}/\sigma^2_c$, with $n_{eff}=n/(1+(m-1)\rho)$ clustered by date. By component:
- NOI bias passes $n_{eff}$ 20 in 1–2 years;
- exit-cap bias in 3–5 years;
- capex, schedule and demand bias rarely within a decade.

### 6.5 What the marks change in SELL / HOLD / REFINANCE / LEVER

| Action | Rule with RAME [I] |
|---|---|
| **SELL** | Price the bid against $V^*$: an LP sale at p of NAV gives up $\hat\theta$ of NAV in value, so the kernel's $p^*$ (groups synthesis §3.0) scales by $\hat\theta$. At 68% with $\hat\theta$ ≈ 0.78, the economic discount is 13%, not 32%. **Open-end redemption** carries a staleness option worth $E[\sum_tf_t\,\text{paid}_t(1/\hat\theta_t-1)]$ less queue-delay carry, where $f_t$ is the fill rate (G10/G14 queue machine). It is positive early in downturns and gone once queues ration fills |
| **HOLD** | Continuation value on $V^*$ with fused $\hat\mu$. A stale NAV never makes HOLD look cheaper |
| **REFINANCE** | Lenders size on $D^{max}=\min(LTV^{max}A,\;N/(DSCR^{min}k))$. Appraisal lag *temporarily inflates* LTV capacity in a downturn. DSCR on observed NOI and current rates binds first in a rate shock. Covenants tested on appraisals breach 2–6 quarters after a listed shock (G10's median trough lag is 3 quarters). Price risk on $LTV^*=D/V^*$ |
| **LEVER** | Size on Kalman or three-step σ and β, never appraisal σ; half-Kelly on desmoothed σ (literature synthesis §4.12). Development debt carries the capex and schedule priors |

**Links to other groups and Corporate Finance.**
- **CF:** look-through leverage on both A and $V^*$. Covenant-cure demand follows the appraisal lag (λ, ℓ), so CF's ladder needs a lagged profile.
- **Overlay:** REIT or infrastructure TRS and rate hedges use desmoothed betas. Observed fund betas understate them: 0.22 vs 0.57 for core RE in R3.
- **Secondaries:** bids enter RAME as observations, with conflict flags.
- **Capital Solutions:** NAV facilities on real-asset funds are priced on $V^*$ and $\theta^{eq}$.
- **Private Credit:** real-estate loans share the LTV lag.
- **Transfers:** intra-ADIC transfers raise no liquidity.

### 6.6 Open-end holdings: the queue prices staleness

G15's book holds $4.7bn of open-end vehicles (real estate $2.7bn, infrastructure $2.0bn). Each needs:
- a queue state;
- $\hat\theta$;
- a SELL-option value;
- a stay cost when others redeem.

In R9, redemptions respond to lagged listed returns, as in Couts. On common random numbers [I-calc]:
- with no queue, leavers gain 21.9bp a year of fund value from stayers;
- a 2%-a-quarter queue cuts this to 9.2bp;
- adding a 5% cash buffer raises it to 15.0bp, reproducing Couts' sign.

Peak queues average 9.1% of NAV (P90 14.9%). Rules:
- lodge notices when $\hat\theta<0.9$ and queues are short;
- give open-end units no Tier-1 liquidity (literature synthesis §4.11);
- treat manager cash buffers as transfers to early redeemers.

### 6.7 Synthetic ground truth and recovery tests (SYN-ADIC-177, Real Assets)

**Generator.** The code header has the full equations; all values [I].
- *World:* real rate AR(1) (1.5%, φ 0.95, σ 25bp); inflation AR(1) (2.5%, 0.80, 50bp); log-Brent OU (ln 75, 0.97, σ 16% a quarter); a two-state regime (normal → down 4% a quarter, down → normal 15%). The down state adds +1.5% a quarter to log cap rates, ×1.5 to cap-rate volatility and −0.5% a quarter to NOI.
- *Truth:* $v=n-x$ per segment plus an idiosyncratic random walk.
- *Observation:* CGR-type appraisal (λ_agg, λ_idio, ℓ), calendar noise σ_e redrawn at each asset's yearly external appraisal, a listed proxy with an AR(1) premium, a transaction index, sales selected on $(v-a)$ plus forced sales in the down state, and underwriting and forecasts with bias, anchoring ($w_a$ 0.30, noise 2–3% a year) and κ.

| Segment | $\bar c$ | $\phi_x$ | $b_r$ | $\sigma_x$/q | g | π-pass | $\sigma_n$/q | $\beta_{oil}$ | $\sigma_i$/q | $\lambda_{agg}$ | $\lambda_{idio}$ | ℓ | $\sigma_e$ | $\phi_p$; $\sigma_p$/q | $\sigma_\tau$/q |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CORE_RE | 5.0% | 0.95 | 12 | 0.040 | 2.5% | 0.5 | 0.015 | 0 | 0.040 | 0.75 | 0.35 | 1 | 0.05 | 0.85; 0.05 | 0.025 |
| VA_RE | 5.75% | 0.95 | 12 | 0.050 | 3.0% | 0.4 | 0.025 | 0 | 0.070 | 0.70 | 0.35 | 1 | 0.07 | 0.85; 0.05 | 0.030 |
| CORE_INFRA | 6.0% | 0.96 | 10 | 0.035 | 2.5% | 0.8 | 0.010 | 0 | 0.030 | 0.85 | 0.50 | 1 | 0.03 | 0.88; 0.06 | 0.035 |
| VA_INFRA | 6.5% | 0.95 | 10 | 0.050 | 4.0% | 0.6 | 0.030 | 0 | 0.080 | 0.80 | 0.45 | 1 | 0.05 | 0.88; 0.06 | 0.040 |
| ENERGY | 10.0% | 0.93 | 6 | 0.060 | 0% | 0.3 | 0.020 | 0.70 | 0.100 | 0.50 | 0.30 | 1 | 0.08 | 0.80; 0.07 | 0.060 |

*SYNTHETIC – NOT ADIC DATA.*
- $b_r$ is the change in log cap rate per unit change in the real rate (12 means +100bp moves 5.0% to 5.6%).
- An `AGRI_TIMBER` template in the code predates the user's exclusion; no test or sleeve uses it.
- *To add:* a GCC RE segment (CORE_RE plus an oil and fiscal loading, λ ≈ 0.80, β_L ≈ 0.5).
- *To align:* set ENERGY's β_oil to G12's sub-segment elasticities (unlevered PDP 0.39, 40%-LTV equity 0.64, royalties 0.31).
- *Reconciliation with G10:* G10 smooths each position with one Geltner weight (0.55–0.70, lag 1, 0.4% noise). That is the special case $\lambda_{agg}=\lambda_{idio}$ with negligible calendar noise, which misses CGR's aggregate gap and the attenuation of λ and β. G10 should adopt the two-component form.

**Census: G15's sleeve book with mark segments** ($18.0bn NAV, $4.0bn unfunded). The last column is the equity-NAV overstatement implied by a 10% asset overstatement, $(\theta-1)/(1-L)$ [I-calc]:

| G15 sleeve | NAV / unfunded ($bn) | LTV | Mark segment | Equity overstatement |
|---|---|---|---|---|
| RE open-end core | 2.7 / 0 | 0.27 | CORE_RE; queue state | 13.7% |
| RE closed-end value-add / opportunistic | 2.6 / 1.2 | 0.60 | VA_RE; incurred Benktander | 25.0% |
| RE JV / direct, global | 1.7 / 0.2 | 0.45 | CORE_RE / VA_RE | 18.2% |
| RE JV / direct, GCC | 1.2 / 0.2 | 0.45 | GCC RE | 18.2% |
| RE co-investment | 0.8 / 0 | 0.60 | VA_RE | 25.0% |
| Infrastructure open-end core | 2.0 / 0 | 0.50 | CORE_INFRA; queue state | 20.0% |
| Infrastructure closed-end core-plus / value-add | 2.5 / 1.3 | 0.55 | VA_INFRA | 22.2% |
| Infrastructure direct / co-investment | 2.0 / 0.3 | 0.55 | CORE_INFRA / VA_INFRA | 22.2% |
| Energy & natural resources, closed-end | 1.6 / 0.6 | 0.35 | ENERGY; strip anchor | 15.4% |
| Energy & natural resources, direct / co-investment | 0.9 / 0.2 | 0.40 | ENERGY | 16.7% |

*SYNTHETIC – NOT ADIC DATA.* G12's $2.5bn energy split matches G15.

**Calibration (V-gates) and recovery tests** [I-calc; SYNTHETIC; 200 worlds (60 for MLE), T = 80 quarters]. Triplets read core RE / value-add RE / core infrastructure unless stated. R4 comes from `g13_part2.py`, which added the nowcast-quality control; all other tests use identical seeds in both runs.

| Test | Measure | Result | Verdict |
|---|---|---|---|
| V1 smoothing pattern, core RE | Fund / aggregate AC1; aggregate AC1 after 1-step / 3-step; fund volatility observed ÷ 3-step | 0.42 / 0.63; 0.47 / 0.00; 0.53 (CGR: 0.45 / 0.75; 0.46 / −0.02; 0.54) | Pass. Aggregate AC1 sits below target because of calendar noise |
| V-RA1 appraisal vs sale | Mean absolute; signed; crash quarters; boom quarters; sold above prior mark | 12.5%, +3.4%, −11.5%, +16.3%, 56% / 17.1%, +6.2%, −11.4%, +20.0%, 58% / 11.1%, +4.2%, −9.8%, +15.5%, 61% (Cannon & Cole: 12.5%, +4.9%, −12.0%, up to +14.7%) | Pass |
| R1 λ (true 0.75 / 0.70 / 0.85) | OLS on index; Kalman A / AL / ALT / ALT4 (A appraisal; L listed; T transactions; T4 yearly transactions) | OLS 0.64 / 0.60 / 0.75; A 0.71 / 0.64 / 0.81; AL 0.74 / 0.67 / 0.83; **ALT 0.745 / 0.701 / 0.842**; ALT4 0.74 / 0.68 / 0.84 | Pass (ALT bias ≤ 0.01) |
| R1 90% CI coverage of λ (ALT) | Hessian / sandwich | 0.73 / 0.87; 0.70 / 0.82; 0.73 / 0.73 | Partial: bootstrap in production |
| R1 lag | Profile likelihood picks the true ℓ | 100% / 98% / 100% | Pass |
| R2 nowcast RMSE (index level) | Appraisal; A; AL; ALT; ALT4 | 8.8; 7.0; 5.5; **2.5**; 4.4% / 10.8; 9.7; 7.3; **3.0**; 6.4% / 9.5; 6.3; 5.3; **3.1**; 4.5% | Pass with τ (28–33% of appraisal RMSE); listed alone gives 56–68% |
| R2 80% band coverage | AL / ALT | 0.66 / 0.79; 0.55 / 0.77; 0.64 / 0.77 | ALT pass; widen AL bands ×1.3–1.7 |
| R2 down-regime level error | Appraisal / AL / ALT | +2.5 / +0.9 / +0.1%; +4.0 / +2.5 / +1.2%; +2.6 / +1.5 / +0.7% | Pass |
| R3 fund β (Dimson, lags 0–2) | Observed / 1-step / 3-step / true | 0.22 / 0.32 / 0.45 / 0.57; 0.32 / 0.43 / 0.56 / 0.66; 0.10 / 0.18 / 0.30 / 0.40 | Pass (3-step 75–85% of true) |
| R3 misspecification (M_regime, M_season, M_all) | λ̂ (ALT); nowcast RMSE | λ̂ tracks the time-average λ (0.698 under a Q4 reset averaging 0.70); RMSE 2.2–3.6% in every variant; fixed-λ CIs miss the base λ (coverage 0.13–0.73) | Nowcast robust. Model λ(z, q) where λ itself matters |
| R4 forecast bias (4 segments, 8q horizon) | Dispersion: naive / nowcast control / appraisal control. CI coverage: iid / clustered / control + cluster-t. $w_a$: naive / control | ±6.6–8.3 / ±1.5–2.6 / ±5.0–6.6pp; 0.16–0.28 / 0.59–0.68 / 0.74–0.81; 0.33–0.41 / 0.30–0.31 (true 0.30) | Control required; coverage borderline |
| R5 κ | Coverage estimator | 1.66 / 1.94 / 1.69 / 1.95 (true 1.67 / 2.0 / 1.67 / 2.0) | Pass |
| R6 scoring, core RE | MSE honest vs appraisal-mimic, scored against appraisal / true / τ | 0.0066 vs 0.0033 / 0.0107 vs 0.0132 / 0.0118 vs 0.0142 | Pass: honest wins on true and τ |
| R7 fusion, value-add RE | MSE at n = 40 (P90): equal / GLS / constrained GLS / shrink 50% | 0.0662 (0.0710) / 0.0715 (0.0800) / 0.0667 (0.0710) / 0.0662 (0.0708) | Pass |
| R8 closed-end ultimates, value-add RE | RMSE of ln U at 12 / 20 / 28 quarters: prior; reported CL; economic CL; paid GB; incurred GB | 0.233; 0.216 / 0.149 / 0.054; 0.193 / 0.122 / 0.037; 0.218 / 0.257 / 0.202; **0.191 / 0.122 / 0.037** | Pass. Down-regime bias at 12q: reported +7.3% vs economic +3.7% |
| R9 open-end transfer | bp a year to leavers: none / 2% queue / queue + 5% buffer; peak queue | 21.9 / 9.2 / 15.0; mean 9.1% of NAV (P90 14.9%) | Pass |

*SYNTHETIC – NOT ADIC DATA.*

### 6.8 Calibration targets and data needs

| Target | Value | Source |
|---|---|---|
| Core RE fund / aggregate AC1 | 0.45 / 0.75 | CGR |
| True ÷ observed fund volatility | ≈1.8–1.9× | CGR |
| Unlisted infrastructure NAV volatility | 2.7–3.3% (implies λ_infra ≥ 0.85) | SIPA / GPIF |
| Appraisal against sale | Mean absolute 12.5%; cyclical signed error | Cannon & Cole |
| ODCE lag | Trough 7 quarters after the peak; 2022 REITs −24.95% vs ODCE +7.5% | NCREIF, Nareit |
| Listed premium state | REIT discount 9.35% (Jul 2026), 16–18% (Dec–Jan) | S&P Global |
| τ level check | CPPI −16% from peak; office −35% | Green Street |
| θ priors | Secondary pricing: RE 68%, infrastructure 91% | Jefferies |
| Unlevering; queue state | ODCE leverage 27.1%; flows −$8.7bn a year | NCREIF |
| Infrastructure discount-rate stickiness | HICL discount rate 8.4 → 8.5% while its share discount moved 28 → 24% | HICL |
| Demand and capex priors | Actual ÷ forecast traffic 0.77; electricity overrun 66.3% | Bain; Sovacool |

**Data ADIC must supply** (by value):
1. Appraisal histories: valuation date, valuer type, method, cap or discount rate; 10+ years.
2. Quarterly NOI or cash yield.
3. The asset-level debt tape (with G14).
4. The underwriting archive with plan components.
5. A point-in-time plan archive, including declined and sold deals.
6. Sale price against last appraisal.
7. Open-end queue statements.
8. Secondary quotes received.
9. Energy decks against the strip, and reserve reports.

### 6.9 SPECIFICATION CARD — Real-Assets Mark Engine (RAME)

| Item | Specification |
|---|---|
| **Data fields** | `holding_id, group=RA, segment, vehicle {CE, OE, CO, JV, DIR}, valuation_date, report_date, appraisal_value, valuer_type {EXT, INT, CARRY}, appraisal_cap_or_DR, noi_fwd, capex, debt, dscr, ltv_A, ltv_econ, uw{g, κ_exit, K, T, Q, H, price}, bp{same}, q_bid, queue_pos, is_synthetic`. Per segment: `appraisal_index, listed_unlev, txn_index, reit_nav_premium, strip`. All bitemporal |
| **Return and value** | $V=N/c$; $r\approx y+\Delta n-\Delta\kappa$; desmooth appreciation only; $r^U=(1-L)r^E+Lr^D$ |
| **Appraisal (NAV) model** | $a=s+e$; $s_t=\lambda s_{t-1}+(1-\lambda)v_{t-\ell}$; $e_t=0.75e_{t-1}+\xi_t$; two-component smoothing ($\lambda_{agg},\lambda_{idio}$). Reported NAV feeds covenants, bids and LP statements; $V^*$ feeds risk and the kernel |
| **Nowcast** | Segment Kalman (appraisal, unlevered listed, τ, bids); MLE with sandwich SE; ℓ by profile likelihood. Holding: segment correction + CGR step 2 + own-trade update. $\theta^{eq}=(\theta A-D)/(A-D)$ |
| **Cash flows** | Distributions from NOI (unsmoothed) and exits at true value. Closed-end funds on RFT-TA v2 with real-asset parameters (design brief §8); income earlier than PE |
| **Parameter defaults** | λ_agg 0.70–0.85, λ_idio 0.30–0.50, ℓ = 1, σ_e 0.03–0.08, φ_p 0.80–0.88 (§6.7). Bias and κ (§6.4). Sources: CGR, Cannon & Cole, SIPA/GPIF, Couts, NCREIF, Green Street, Jefferies, HICL |
| **Forecasts and biases** | Group files P10/P50/P90 for NOI growth, exit cap, capex, schedule, demand, hold date and total return on $V^*$ at 4 and 8 quarters. Biases: deal optimism, market smoothing, appraisal anchoring, defend-the-holding. Component model with a desmoothed common-shock control; κ ~ LN(ln 1.75, 0.25²) until scored; 50% shrink-to-equal fusion; BLP recalibration |
| **Scoring** | Components against unsmoothed outcomes; total return against $V^*$ with target noise; WIS headline; Knüppel PIT. Never against appraisal returns |
| **Liquidity and stress** | Open-end: queue fill $f_t$, zero Tier-1. Closed-end: LP sale at p, economic discount $1-p/\hat\theta$. Directs and JVs: 2–4 quarters to sell (G14). In stress, reported NAV and covenants fall 2–6 quarters after listed prices, and $\theta^{eq}$ grows with leverage |
| **SELL / HOLD / REFINANCE / LEVER** | SELL against $V^*$, plus the open-end staleness option net of queue carry. HOLD on $V^*$. REFINANCE capacity on appraisal LTV and DSCR, risk on $LTV^*$. LEVER on desmoothed σ. One kernel (main §4.4) |
| **Synthetic defaults** | §6.7 generator and G15 census. V-gates: fund AC1 0.45 ± 0.05; appraisal–sale mean absolute 10–14%; crash-quarter signed error ≤ −8%; 3-step aggregate AC1 within ±0.05 |
| **Recovery gates** (status on SYN) | R1 λ bias ≤ 0.03 with listed + τ: pass (≤ 0.01). R1 λ CI coverage ≥ 0.85: partial (sandwich 0.73–0.87), so bootstrap. R2 nowcast RMSE ≤ 50% of appraisal with τ: pass (28–33%). R2 band coverage 0.75–0.85: pass with τ, AL needs widening. R3 3-step fund β ≥ 75% of true: pass. R4 controlled-bias CI coverage ≥ 0.75: borderline (0.74–0.81), so wild-cluster bootstrap. R5 κ within ±0.25: pass. R6 honest wins on true and τ: pass. R7 shrink ≤ GLS at n = 40: pass. R8 incurred Benktander best or tied at every age: pass. R9 buffer raises the transfer over a queue alone: pass. Freeze and hash gates before the first scored release (groups synthesis §6) |
| **Links** | G10/G11/G12 truth engines; G14 debt tape and actions; G15 cash map; Secondaries bids; Capital Solutions NAV facilities on $V^*$; Private Credit LTV lag; Overlay desmoothed-β hedges; CF dual leverage, lagged covenant-cure demand, FTP on $V^*$ |

## 7. Implementation notes

- **Code.** `g13_ra_marks_sim.py` contains:
  - the generator, Geltner 1-step and CGR 3-step (AR form, eqs. 21–23);
  - a numba-jitted seven-state Kalman filter with missing data and per-period log-likelihoods;
  - bounded L-BFGS-B with three starts and lag profiling;
  - the R4–R9 tests.

  Production can port it to `statsmodels` `MLEModel`.
- **Identification.**
  - Appraisals alone identify λ only under a random-walk truth. Mean-reverting cap rates, regimes and calendar noise bias it.
  - A timely signal identifies λ and ℓ.
  - $\beta_L$ trades off against the premium variance, so put a prior on $\sigma_p$ from the REIT NAV-discount history (≈5–7pp a quarter).
- **Calendar noise.** Model it as a state ($e_t$, φ ≈ 0.75), not white noise. OLS on the noisy index gives λ̂ ≈ 0.64 / 0.60 / 0.75 against true 0.75 / 0.70 / 0.85 (R1).
- **Numerics.**
  - Bound λ below 0.98, since desmoothed variance scales with $(1-\lambda)^{-2}$.
  - Unsmooth log returns, as CGR and Geltner do.
  - Initialize noise and premium states at their stationary variance.
  - Symmetrize P after each update, and use a Cholesky log-determinant.
  - Clip per-fund AR coefficients to [0, 0.97].
  - With fewer than 10 funds per segment, use the segment Kalman plus a 1-step idiosyncratic correction.
- **Seasonality.** Under a Q4 external-appraisal reset, a fixed-λ model returns the calendar-average λ (0.698 against 0.75 in Q1–Q3 and 0.55 in Q4) and the nowcast is unaffected (RMSE 2.2%). Add a Q4 λ dummy for return timing, not for levels (R3).
- **Interval honesty.** The sandwich SE lifts λ-interval coverage from 0.70–0.73 (Hessian) to 0.73–0.87, still short of 0.90; use a parametric bootstrap in production. Without a transaction signal, widen nowcast bands by 1.3–1.7× (R2).
- **Leverage and fees.** Desmooth unlevered property returns, then re-lever with the actual debt path. Equity staleness uses gross asset values.
- **Aggregation.** CGR needs time-invariant weights: equal or start-of-window NAV weights.
- **Cost.** One segment fit (T = 80) takes ≈0.1–0.5 s, negligible against the 50k-path simulation.
- **Labelling.** RAME outputs from SYN inputs carry `is_synthetic=true` and the footer *SYNTHETIC – NOT ADIC DATA* (groups synthesis §6, L1–L8).

## 8. Risks and limitations

1. **Truth is never observed.** Desmoothing rests on models of valuer behaviour, which can change (for example after the FCA review). Re-estimate yearly, and monitor with V-RA1 on ADIC's own sales.
2. **Listed proxies are imperfect.** Sector mix, leverage, management and sentiment differ, and β_L < 1 is real. Proxies are weak for GCC real estate, digital infrastructure and private energy.
3. **Transaction evidence is selected.** Exit premia (EDHEC 6–20%, HICL +21%) are owners' choices. ADIC's unsold stock is not the sold sample; the main report rejects applying exit statistics to unsold inventory.
4. **Secondary prices mix staleness with liquidity and selection.** P2 is an upper bound.
5. **Bias estimation needs cycles.** Even with the control, coverage is 74–81% against a nominal 90% with eight dates. Capex, schedule and demand bias stay prior-driven for years.
6. **Goodhart.** Once θ̂ drives SELL and marks are scored, valuers and groups adapt. Score unsmoothed outcomes, and keep pay linear in DVA (groups synthesis §5).
7. **Simulation checks correctness, not variant choice** (literature synthesis §3.13).
8. **Evidence gaps.** Several 2023–25 returns, the S&P year-end discount and some bias figures are [S-sec]. No real-estate-specific evidence on NAV inflation around fundraising was found in this session, so PE evidence (stream 07) is transferred as a prior [I]. The web-search budget ran out mid-session (§10 note).

## 9. Open questions for ADIC

1. Size and regional mix, and whether "funds" include open-end or evergreen vehicles (queue machine, staleness option).
2. Valuation policy: frequency, external share, valuer rotation, local valuation of GCC assets, and ad hoc triggers.
3. If open-end funds are held: queue positions, notice terms and buffer policies.
4. Does the underwriting archive hold plan *components*, or only IRR and multiple? Without components the bias model falls back to total return.
5. Which benchmarks can be licensed: Green Street CPPI and NAV discounts, MSCI/NCREIF, RCA, SIPA infraMetrics?
6. Is a dual (reported and economic) NAV acceptable in IC and owner materials?
7. Energy: which price deck sets NAV, and how often?
8. Asset-level covenants: tested on appraisals? Who funds cures, the group or CF?

## 10. References

*Process note:* academic metadata were verified on Crossref, OpenAlex and publisher or repository pages. OpenAlex and Semantic Scholar rate-limited mid-session, and the shared web-search budget was exhausted near the end, so a few items rest on abstracts or secondary summaries and are tagged [S-sec] in the text.

*Academic*
- Andonov, A., Kräussl, R. & Rauh, J. (2021). Institutional investors and infrastructure investing. *Review of Financial Studies* 34(8), 3880–3934. https://doi.org/10.1093/rfs/hhab048
- Ang, A., Chen, B., Goetzmann, W. N. & Phalippou, L. (2013/2018). Estimating private equity returns from limited partner cash flows. SSRN 2356553 (*Journal of Finance* 2018). https://doi.org/10.2139/ssrn.2356553
- Bain, R. (2009). Error and optimism bias in toll road traffic forecasts. *Transportation* 36(5), 469–482. https://doi.org/10.1007/s11116-009-9199-7
- Barkham, R. & Geltner, D. (1994). Unsmoothing British valuation-based returns without assuming an efficient market. *Journal of Property Research* 11(2), 81–95. https://doi.org/10.1080/09599919408724107
- Barkham, R. & Geltner, D. (1995). Price discovery in American and British property markets. *Real Estate Economics* 23(1), 21–44. https://doi.org/10.1111/1540-6229.00656
- Bokhari, S. & Geltner, D. (2012). Estimating real estate price movements for high frequency tradable indexes in a scarce data environment. *Journal of Real Estate Finance and Economics* 45(2), 522–543. https://doi.org/10.1007/s11146-010-9261-4
- Brown, G., Ghysels, E. & Gredil, O. (2023). Nowcasting net asset values: The case of private equity. *Review of Financial Studies* 36(3), 945–986. https://doi.org/10.1093/rfs/hhac045
- Cannon, S. E. & Cole, R. A. (2011). How accurate are commercial real estate appraisals? Evidence from 25 years of NCREIF sales data. *Journal of Portfolio Management* 35(5), 68–88. https://doi.org/10.3905/jpm.2011.35.5.068 (working paper: https://mpra.ub.uni-muenchen.de/32589/)
- Clayton, J., Geltner, D. & Hamilton, S. W. (2001). Smoothing in commercial property valuations: Evidence from individual appraisals. *Real Estate Economics* 29(3), 337–360. https://doi.org/10.1111/1080-8620.00014
- Couts, S. J. (2025). Liquidity transformation risks and stabilization tools: Evidence from open-end private equity real estate funds. *Real Estate Economics* 53(5), 1009–1044. https://doi.org/10.1111/1540-6229.12532 (working paper: https://lusk.usc.edu/sites/default/files/working_papers/SSRN-id3445622.pdf)
- Couts, S. J., Gonçalves, A. S. & Rossi, A. (2024). Unsmoothing returns of illiquid funds. *Review of Financial Studies* 37(7), 2110–2155. https://doi.org/10.1093/rfs/hhae006 (accepted version: https://uncipc.org/wp-content/uploads/2024/12/Couts_Goncalves_Rossi_2024RFS_UnsmoothingReturns.pdf)
- Diaz, J. & Wolverton, M. L. (1998). A longitudinal examination of the appraisal smoothing hypothesis. *Real Estate Economics* 26(2), 349–358. https://doi.org/10.1111/1540-6229.00749
- Dimson, E. (1979). Risk measurement when shares are subject to infrequent trading. *Journal of Financial Economics* 7, 197–226 (as cited in CGR 2024).
- Elliott, G. et al. (2026). Combining forecasts: on why averaging beats optimal linear weights. *Journal of Business & Economic Statistics*. https://doi.org/10.1080/07350015.2026.2661980 (as verified in the literature synthesis)
- Fisher, J., Gatzlaff, D., Geltner, D. & Haurin, D. (2003). Controlling for the impact of variable liquidity in commercial real estate price indices. *Real Estate Economics* 31(2), 269–303. https://doi.org/10.1111/1540-6229.00066
- Fisher, J., Geltner, D. & Pollakowski, H. (2007). A quarterly transactions-based index of institutional real estate investment performance and movements in supply and demand. *Journal of Real Estate Finance and Economics* 34(1), 5–33. https://doi.org/10.1007/s11146-007-9001-6
- Fisher, J. D., Geltner, D. M. & Webb, R. B. (1994). Value indices of commercial real estate: A comparison of index construction methods. *Journal of Real Estate Finance and Economics* 9(2), 137–164. https://doi.org/10.1007/BF01099972
- Flyvbjerg, B., Holm, M. S. & Buhl, S. (2002). Underestimating costs in public works projects: Error or lie? *Journal of the American Planning Association* 68(3), 279–295. Summary: https://ppp.worldbank.org/index.php/library/underestimating-costs-public-works-projects-error-or-lie
- Flyvbjerg, B. & Gardner, D. (2023). *How Big Things Get Done*. Review used: https://marclevinson.net/HowBigThingsGetDone020723.pdf
- Geltner, D. (1991). Smoothing in appraisal-based returns. *Journal of Real Estate Finance and Economics* 4(3), 327–345. https://doi.org/10.1007/BF00161933
- Geltner, D. (1993). Estimating market values from appraised values without assuming an efficient market. *Journal of Real Estate Research* 8(3), 325–345. https://doi.org/10.1080/10835547.1993.12090713
- Geltner, D., MacGregor, B. D. & Schwann, G. M. (2003). Appraisal smoothing and price discovery in real estate markets. *Urban Studies* 40(5–6), 1047–1064. https://doi.org/10.1080/0042098032000074317
- Getmansky, M., Lo, A. W. & Makarov, I. (2004). An econometric model of serial correlation and illiquidity in hedge fund returns. *Journal of Financial Economics* 74(3), 529–609. https://doi.org/10.1016/j.jfineco.2004.04.001
- Gupta, A. & Van Nieuwerburgh, S. (2019). Valuing private equity strip by strip. NBER WP 26514. https://doi.org/10.3386/w26514
- Knüppel, M. (2015). Evaluating the calibration of multi-step-ahead density forecasts using raw moments. *Journal of Business & Economic Statistics* 33(2). https://doi.org/10.1080/07350015.2014.948175
- Ling, D. C. & Naranjo, A. (2015). Returns and information transmission dynamics in public and private real estate markets. *Real Estate Economics* 43(1), 163–208. https://doi.org/10.1111/1540-6229.12069
- Lizieri, C., Satchell, S. & Wongwachara, W. (2012). Unsmoothing real estate returns: A regime-switching approach. *Real Estate Economics* 40(4), 775–807. https://doi.org/10.1111/j.1540-6229.2012.00331.x
- Mack, T. (2000). Credible claims reserves: The Benktander method. *ASTIN Bulletin* 30(2), 333–347. https://www.casact.org/library/astin/vol30no2/333.pdf
- McAllister, P. & Nase, I. (2020). The accuracy of consensus real estate forecasts revisited. *Journal of Property Research* 37(2), 147–170. https://doi.org/10.1080/09599916.2020.1720784
- Neuhaus, W. (2025). Parameter-free Benktander-type reserving. *Scandinavian Actuarial Journal*. https://doi.org/10.1080/03461238.2025.2536811 (as verified in the literature synthesis)
- Papastamos, D., Matysiak, G. & Stevenson, S. (2018). A comparative analysis of the accuracy and uncertainty in real estate and macroeconomic forecasts. *Journal of Real Estate Research* 40(3), 309–346. https://doi.org/10.1080/10835547.2018.12091503
- Plazzi, A., Torous, W. & Valkanov, R. (2010). Expected returns and expected growth in rents of commercial real estate. *Review of Financial Studies* 23(9), 3469–3519. https://doi.org/10.1093/rfs/hhq069
- Quan, D. C. & Quigley, J. M. (1991). Price formation and the appraisal function in real estate markets. *Journal of Real Estate Finance and Economics* 4(2). https://doi.org/10.1007/BF00173120
- Ranjan, R. & Gneiting, T. (2010). Combining probability forecasts. *Journal of the Royal Statistical Society B* 72(1). https://doi.org/10.1111/j.1467-9868.2009.00726.x
- Sovacool, B. K., Gilbert, A. & Nugent, D. (2014). An international comparative assessment of construction cost overruns for electricity infrastructure. *Energy Research & Social Science* 3, 152–160. https://sussex.figshare.com/articles/journal_contribution/An_international_comparative_assessment_of_construction_cost_overruns_for_electricity_infrastructure/23424974

*Industry, regulatory and market data*
- CBRE (21 Jul 2022). Prime multifamily underwriting reacts to market volatility. https://www.cbre.com/insights/briefs/prime-multifamily-underwriting-reacts-to-market-volatility
- Commercial Property Executive (25 Aug 2026; updated 16 Sep 2026). 2026 REIT trading trends (S&P Global MI data). https://www.commercialsearch.com/news/2026-reit-trading-trends/
- CoStar / Apartments.com (2 Apr 2025). Multifamily rent report, Q1 2025. https://www.businesswire.com/news/home/20250402768234/en/Apartments.com-Releases-Multifamily-Rent-Report-for-the-First-Quarter-of-2025 [S-sec]
- EDHEC Infrastructure & Private Assets (Jun 2025). *Fair Value or Fair Guess?* (press summary). https://mondovisione.com/media-and-resources/news/edhec-infra-and-private-assets-survey-reveals-serious-flaws-in-private-asset-valua-202579/
- FCA (5 Mar 2025). Private market valuation practices. https://www.fca.org.uk/publications/multi-firm-reviews/private-market-valuation-practices
- Financial Advisor (6 Dec 2022). Blackstone, Starwood limit redemptions as investors seek liquidity. https://www.fa-mag.com/news/blackstone--starwood-limit-redemptions-as-investors-seek-liquidity-70935.html
- Green Street (6 May 2026). Commercial property plods along. https://info.greenstreet.com/hubfs/GSCPPI-20260506press.pdf ; (6 Oct 2026) CPPI release. https://www.greenstreet.com/waiting-for-price-clarity/
- HICL Infrastructure PLC (2026). Annual Report 2026. https://www.hicl.com/wp-content/uploads/2026/05/HICL-Annual-Report-2026.pdf
- HM Treasury (2003; online 2013). Supplementary Green Book guidance: optimism bias. https://www.gov.uk/government/publications/green-book-supplementary-guidance-optimism-bias
- Jefferies (Jul 2026). Global Secondary Market Review. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- Nareit media fact sheets (Apr 2025; Dec 2025). https://www.reit.com/sites/default/files/2025-05/MediaFactSheet_Apr-2025.pdf ; https://www.reit.com/sites/default/files/2026-01/MediaFactSheet_Dec-2025.pdf [S-sec]
- NCREIF (30 Jul 2026). NFI-ODCE 2Q-2026 press release. https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf ; (16 Sep 2026) webinar slides. https://ncreif.org/__static/jdj5jdewjc9ybldynw1nwu1tm3u2qnkw/NFI-ODCE-2026q2-Performance-Attribution-Webinar-Slides.pdf
- Oxera (Sep 2012). Sold to the slyest bidder: optimism bias, strategy and overbidding. https://www.oxera.com/wp-content/uploads/2018/03/Optimism-bias-strategy-and-overbidding2-3.pdf
- Scientific Infra & Private Assets (Sep 2024). The fair value of investments in unlisted infrastructure equity (report for GPIF). https://gpif.go.jp/investment/research_20241213_en.pdf
- S&P Global MI (Feb 2026). NAV Monitor: US REITs end January at median 16.2% discount. https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/2/nav-monitor-us-reits-end-january-at-median-16-2-discount-to-net-asset-value-97852413 [S-sec: title]

*Project documents (read, not edited):* context §1A; design brief §8; main synthesis §4.2–4.4; groups synthesis §2–§6; literature synthesis §3.8 and §4.10; dossiers 04, 05, 07; G12 and G14 dossiers; G10 and G15 calcs.
