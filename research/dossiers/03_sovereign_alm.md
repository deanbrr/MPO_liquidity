# Stream 03: Sovereign ALM — oil-fiscal linkage and owner distribution demand as a stochastic liability

**Project:** ADIC multi-period robust TPA framework (agentic) · **Stream:** 03 · **As of:** 18 Oct 2026 · **Audience:** design/architecture, quant team, IC secretariat

**Evidence tags:**
- **[S]** sourced fact, cited in §10.
- **[P]** practitioner consensus.
- **[I]** our inference or design proposal.
- **[I-calc]** our own computation on public data.
- **[I-MC]** our own stylized simulation. Results are assumption-driven and are not forecasts.
- **[U]** a citation or number we could not verify in-session.

**Reproducibility.** All [I-calc] and [I-MC] numbers come from scripts and JSON outputs in `C:\users\dean\ai_envs\adic_tpa_lab\research\addenda\03_sovereign_alm_calcs\`. The scripts are `oil_equity_regimes.py`, `regimes_and_hybrids.py` and `draw_model_demo.py`. Data come from EIA Brent spot (daily), the Ken French data library (US and developed-market factors) and CBOE VIX.

**Session caveats.**
- A shared web-search cap was exhausted partway through this stream. Most evidence therefore comes from primary documents fetched directly: EIA STEO PDFs, IMF Article IV reports and the IMF DataMapper API.
- Client-provided facts are labelled as such: AUM of US$177bn, the 5–10% distribution band, the 10% target, leverage permission and ~60% private assets. We found no public source for them.

---

## 1. Executive summary

1. **The owner's draw is a short, clipped option on the sovereign's fiscal state.** [I]
   - Write the draw rate as a clipped linear function of the owner's fiscal balance. Because the fiscal balance is roughly linear in log oil, the dollar draw is exactly a NAV-scaled vertical put spread on (log) oil, and ADIC is the writer.
   - **Calibration** uses the IMF's consolidated UAE fiscal breakeven of US$44.8/bbl for 2026 and hydrocarbon revenue of ≈11.3% of GDP [S]. Our default rule then puts the draw at the 5% floor when Brent is above ≈US$64 and at the 10% cap when it is below ≈US$31.
   - **Sensitivity.** Between the kinks, each US$1/bbl moves the draw by ≈US$1.5m per US$1bn of NAV. For a US$177bn fund that is about US$266m, or ≈266m barrels of put-spread notional [I-calc]. That is the same order of magnitude as Mexico's annual sovereign hedge, whose volumes we infer from its reported payouts [I].

2. **Liability wrong-way risk depends on the type of oil shock, not on the oil price.**
   - **Monthly Brent–US equity correlation** is −0.14 over 1988–2007, +0.43 over 2008–19 and +0.32 over 2020–26. It is ≈0 in 2022 and in 2023–25, and −0.58 during the March–August 2026 war months [I-calc].
   - **Lower-tail dependence** rose from 0.08 to 0.30 after 2008 [I-calc].
   - Of the six calendar years since 1988 with Brent down ≥30% (1991, 1997, 1998, 2008, 2014, 2015), **only 2008 had falling US equities** [I-calc].
   - **"Oil down" therefore splits into two states:**
     - *supply gluts*: owner draws rise, markets are fine and exits stay open;
     - *demand busts*: draws rise, equities fall and exits close. This is the **triple wrong-way state**.
   - **Statistical regimes do not separate the two.** Our 2-state HMM's turbulent regime has an oil–equity correlation of only 0.16 [I-calc]. The generator needs a shock-type layer that is identified structurally, not by statistics alone.

3. **2026 shows that "oil up" does not mean "owner flush".**
   - **The shock:** US and Israeli strikes on Iran began on 28 Feb 2026, and the Strait of Hormuz was effectively closed [S].
     - Gulf crude shut-ins peaked at ≈10.9 mb/d in May [S].
     - UAE shut-ins were 1.10–1.45 mb/d over March–May. EIA later revised them to a 0.74 mb/d average for March–July, and to zero in August and September [S].
     - The UAE was reportedly hit harder by Iranian retaliation than Israel and all other GCC states combined [S].
     - The UAE left OPEC effective 1 May 2026 [S].
   - **Prices:** Brent spot was US$126.55 on 14 Oct 2026 [S].
   - **The IMF nevertheless projects for the UAE** [S]:
     - 2026 real GDP of −3.9%;
     - a general-government surplus of 1.5% of GDP, down from 3.9% in 2025, even though oil averages ≈40% higher.
   - **Implied war wedge:** about −6 to −7pp of GDP relative to an oil-price-only mapping [I-calc].
   - **Design consequence:** a separate *Gulf-war / export-volume* state is required, in which oil up coincides with higher owner needs.

4. **The larger liability risk ahead is a post-war oil-down, not the war itself.**
   - **Price path.** EIA's pre-war baseline (Feb 2026) was US$58/bbl for 2026 and US$53 for 2027. The current path is US$105 in 4Q26 falling to US$74 in 4Q27 as Gulf flows normalise [S].
   - **Glut drivers.** Several factors raise the odds of a supply-glut or price-war state in 2027–29 [S]/[I]:
     - the UAE's OPEC exit, with 4.8–5.0 mb/d of capacity against a former 3.2 mb/d quota;
     - inventory rebuilding;
     - reported Saudi–UAE friction.
   - **Analogue: 2014–16.**
     - Brent stayed below 70% of its trailing 36-month average for 22 months, the longest such spell since 1988 [I-calc].
     - The UAE fiscal balance swung from +1.7% to −6.4% of GDP, or ≈US$32bn [S].
     - The same 8.1pp swing at 2026 GDP (US$661bn) is ≈US$53bn. That is about **6× ADIC's entire 5→10% band width** of US$8.85bn [I-calc]. The owner draws from many pockets in such states, and ADIC should expect to sit near the cap.

5. **The most decision-relevant unknown is the owner's *effective* breakeven** (Abu Dhabi-specific, including off-budget spending), together with the fiscal-gap→draw mapping.
   - Raising the effective breakeven from US$44.8 to US$65 has two effects in our illustrative model [I-MC]:
     - P(≥3 consecutive years with a draw ≥9.5%) over 10 years rises from ≈1% to 10–15%;
     - the mean draw rises from 6.0% to 7.3%.
   - **Elicit and monitor these two parameters first.**

6. **Oil sovereigns do draw on their funds in busts. Endowments behave the opposite way.**
   - **2015 redemptions:** SWFs pulled at least US$46.5bn from asset managers in 2015 (eVestment) [S]. Middle Eastern oil SWFs alone withdrew a record US$19bn in Q3 2015 [S]. SAMA withdrew ≈US$70bn [S].
   - **Norway** made its first-ever withdrawal in January 2016 [S].
   - **Saudi Arabia:** SAMA moved US$40bn to the PIF in March–April 2020 [S].
   - **Kuwait** stopped transfers to its Future Generations Fund (FGF). It now issues debt under a March 2025 law, partly to replenish the General Reserve Fund (GRF) [S].
   - **Endowments cut payouts after losses** ("hoarding", Brown et al. 2014) [S]. On payout dynamics, ADIC is structurally an *anti-endowment*.

7. **Theory: hedge the owner's fiscal surplus, not the oil price, and size buffers by what hedging releases.**
   - *Bodie–Brière:* the hedging target is the fiscal-surplus flow, not the oil price itself [S].
   - *Gintschel–Scherer and Scherer:* tilt away from assets that co-move with the owner's resource income [S].
   - *van den Bremer–van der Ploeg–Wills:* spend out of total wealth, and hold precautionary buffers against risk that cannot be hedged [S].
   - *Borensztein–Jeanne–Sandri:* the largest welfare gain from hedging comes from *reducing precautionary buffers* [S]. ADIC's hedge yardstick should therefore be:

     > buffer released × illiquidity premium, versus premium paid.

   - *Mexico's oil hedge* [S]:
     - premium ≈0.1% of GDP a year;
     - payouts ≈0.5%, 0.6% and 0.3% of GDP in 2009, 2015 and 2016;
     - borrowing costs ≈19bp lower than without the hedge.

8. **Design recommendations.** [I]
   - **(i) Two-layer regime model.**
     - The macro-financial regime $S_t$ comes from Stream 10.
     - It is crossed with an oil/fiscal shock type $Z_t\in\{N,B,SG,DB,SS,GW\}$.
     - Two overlays sit on top: a slow energy-transition (ET) drift and peg/financial stress (PS).
   - **(ii) Owner fiscal module:** fiscal gap → financing hierarchy → a clipped, smoothed draw, with a small probability of a band override.
   - **(iii) Tier-1 constraints:**
     - a stressed Distribution Coverage Ratio (DCR) of at least 1.25 in DB, GW and SG+PS;
     - three-year "drought" survival at cap draws;
     - chance constraints on the liquidity floor.
   - **(iv) Objective:** an owner-state-weighted term, with an "owner beta" for every asset and action.
   - **(v) Hedge stack, in order:**
     1. underweight owner-correlated assets (energy, GCC, domestic strategic stakes);
     2. partial oil put spreads struck at the draw kinks;
     3. joint-state hybrids, bought when *priced* oil–equity correlation is low, as it is now;
     4. committed contingent liquidity.
   - **Hybrid illustration** [I-calc]: a 1-year equity put knocked in by oil <80% costs 0.14–1.16% of notional, against 1.63% for the vanilla put, depending on the correlation priced in (calm vols).

9. **Agentic layer.** [I]
   - Components: a Sovereign Liability agent, an Oil Shock-Type agent, an Owner-Draw simulator, a Hedge Designer, a reverse-stress red team, and an IC elicitation module (SHELF plus entropy pooling).
   - LLMs extract, challenge and narrate. Deterministic code owns every number.

---

## 2. Core concepts and theory

### 2.1 The owner's balance sheet and ADIC's place in it

**The owner's balance sheet.** The owner's comprehensive wealth is
$$W^{own}_t=\underbrace{\textstyle\sum_k F_{k,t}}_{\text{financial pockets}}+V^{oil}_t+V^{tax}_t-V^{G}_t-B_t .$$
- The financial pockets are ADIA, Mubadala (which owns ADIC), L'imad/ADQ, central-bank reserves and others.
- $V^{oil}$ is the present value of hydrocarbon revenue and $V^{tax}$ that of non-hydrocarbon revenue.
- $V^{G}$ is the present value of committed spending and $B$ is debt.

**ADIC's position.** ADIC is one pocket, and its outflow $D_t$ is a *policy* draw. The relevant risk for ADIC is therefore not oil-in-the-ground *per se*. It is the owner's need to finance $V^G$ when $V^{oil}$ disappoints [I].

**Bodie–Brière formalisation** [S].
- **Global Sovereign Surplus.** They maximise CRRA utility over $GSS=FA+FS-FL-DL$: financial assets plus the fiscal surplus, minus foreign and domestic liabilities.
- **Optimal weights.** The financial weights split into four parts:
  - a speculative portfolio $\frac{1}{\gamma\alpha}\Sigma^{-1}\mu$, where α is the financial share of assets;
  - a fiscal-surplus hedge $\propto-\frac{1-\alpha}{\alpha}\Sigma^{-1}\sigma_{FA,FS}$;
  - two liability-hedge terms.
- **Key point (their footnote 11):** the *variability of the revenue flow* must be hedged, not the commodity price, because the fiscal surplus need not have unit sensitivity to the commodity.
- **Chile application.**
  - The paper estimates fiscal-flow sensitivities of 1.05 to inflation, 0.15 to copper and 0.10 to the Chilean equity index (1991–2009). Its text attaches them to the expenditure growth rate but uses them to index receipts.
  - Developed equities had a −7% correlation with the fiscal surplus.

### 2.2 Hedging demand with non-tradable resource wealth

**Static form** [S].
- Gintschel & Scherer (2008, *JAM* 9:215–238) and Scherer (2009, 2011) treat the fund as an investor whose main wealth is untradable oil.
- Optimal portfolios combine a speculative ("optimal growth") demand with a hedging demand. The hedging demand depends on the ratio of financial to resource wealth and on how well each asset hedges oil shocks.
- In mean–variance form:
$$w^*=\tfrac{1}{\gamma}\Sigma^{-1}(\mu-r\mathbf 1)-\tfrac{V^{oil}}{F}\,\Sigma^{-1}\sigma_{r,o}.$$

**Intertemporal form** [S].
- Van den Bremer, van der Ploeg & Wills (2016, *EER* 82:113–131) integrate extraction and fund management. Their results:
  - optimal spending is a share of total wealth, including oil below ground;
  - subsoil oil warrants extra leverage and hedging in the fund;
  - volatility that cannot be hedged calls for precautionary saving;
  - if oil prices are procyclical, extraction should run faster than Hotelling implies.
- Merton (1993) is the endowment analogue: the endowment should hedge the university's other income and cost exposures rather than be managed as the only asset [S].

**Empirical counterpoint** [S].
- Moutanabbir & Noureldin (2020, *International Review of Economics & Finance* 69:708–730) use annual data for 1976–2016 in their working-paper version (ERF WP 1172, 2018).
- They find equity shocks *negatively* correlated with oil-income shocks, and an oil-hedging demand of only ≈0.01–0.07 percentage points of portfolio weight except at extreme risk aversion (WP Table 5).
- [unverified: these figures were checked against WP 1172 only. The 2020 journal abstract reports no sample period, correlation sign or hedging-demand size, and its full text is paywalled.]
- Unconditional, covariance-based hedging demand is therefore small and sample-dependent.

**Why ADIC still needs an explicit liability model** [I]:
- (a) the correlation sign flips by era and shock type (§4.1);
- (b) the draw is clipped, and so non-linear in oil;
- (c) the cost of a draw depends on ADIC's liquidity state, which is worst in demand busts;
- (d) the binding constraint is cash at specific dates, not variance.

Covariance hedging demand is the right *first-order* tilt. Liquidity-timing is where the money is lost.

### 2.3 The draw as a short put spread on the owner's fiscal state

**The draw rule.** Let the owner's fiscal balance, in pp of GDP, be
$$FB_t=h_t\cdot 100\,(\ln P_t-\ln P^{BE}_t)+w_t ,$$
where:
- $h_t$ is hydrocarbon revenue as a share of GDP;
- $P^{BE}_t$ is the effective breakeven;
- $w_t$ collects non-oil shocks (war, spending, volumes).

The target draw rate is
$$d^*_t=\Pi_{[d_{lo},d_{hi}]}\big(c-b\,FB_t\big).$$

**Kinks.** For $w_t=0$, $d^*_t$ is piecewise-linear in $\ln P_t$:
$$K_H=P^{BE}e^{(c-d_{lo})/(100\,b\,h)},\qquad K_L=P^{BE}e^{-(d_{hi}-c)/(100\,b\,h)} .$$

**Option equivalence.**
$$D^*_t=d^*_tNAV_t=d_{lo}NAV_t+100\,b\,h\,NAV_t\,\big[(\ln K_H-\ln P_t)^+-(\ln K_L-\ln P_t)^+\big] .$$
- ADIC is therefore **short a NAV-scaled log-put spread**.
- With smoothing, $d_t=\rho d_{t-1}+(1-\rho)d^*_t$, the option becomes Asian-style.
- Because NAV co-moves with the regime, the option behaves like a quanto [I].

**Uses of the representation** [I]:
1. It yields a *market-consistent liability value*: the Q-price of the put spread × $100bhNAV$.
2. It identifies the *natural hedge strikes*.
3. It shows why the cap matters: beyond $K_L$, extra oil downside adds no draw. The remaining damage then comes from ADIC's *asset* side (NAV, exits).

### 2.4 Liability-side wrong-way risk, by shock type

**Definition.** Wrong-way risk (WWR) in counterparty-credit language means exposure rising as the counterparty deteriorates. Here, *outflows* rise exactly when ADIC's assets and liquidity deteriorate, but only for some shock types [I].

**Structural shock decomposition.** These papers separate shocks:
- Kilian (2009, *AER* 99:1053–69): supply, global-demand and oil-specific demand shocks [S];
- Baumeister & Hamilton (2019, *AER* 109:1873–1910): Bayesian SVAR in which supply disruptions explain more of history and supply shocks hit activity with a lag [S];
- Känzig (2021, *AER* 111:1092–1125): OPEC-announcement supply-news shocks [S];
- Ready (2018, *RoF* 22:155–176): a daily market-based demand/supply/risk split using oil-producer equities and VIX [S].

**Bernanke (2016)** applied a Hamilton-style regression to the 2014–16 decline [S]:
- ≈40–45% of the fall was demand-driven;
- the demand-plus-risk component had a 0.68 average correlation with stocks, against 0.05 for the residual (mostly supply).

**State signs (proposal [I]; episodes [S]/[P]):**

| State $Z$ | Episodes | Oil | Global equities | Credit | PE exits / distributions | Owner fiscal | Owner draw | Duration hedge |
|---|---|---|---|---|---|---|---|---|
| **N** normal | 2017–19, 2023–25 | ~ | + | ~ | normal | sound | low | modest |
| **B** demand boom | 2004–07, 2021 | ↑ | ↑ | tight | strong | strong | floor | n/a |
| **SG** supply glut or price war | 1986 [P], 1998, 2014–16, 2027–29 risk | ↓↓ | ~/+ | energy-HY wider | open | weak for 1–3 years | rises toward cap | works |
| **DB** demand bust | 2008–09, H1 2020 | ↓↓ | ↓↓ | wide | **shut** | weak | cap | works |
| **SS** global supply spike / stagflation | 1990, 2022 | ↑↑ | ↓ | wider | slowing | strong if volumes intact | floor | **fails** (2022) |
| **GW** Gulf war / export-volume shock | 2026 | ↑↑, volatile | ↓ then mixed | mixed | slowing | **ambiguous to weak** (volumes, damage, spending) | up | unreliable |
| Overlays: **ET** (structural demand decline), **PS** (peg / financial stress) | — | slow drift down | — | — | — | erodes $h_t$ and $V^{oil}$ | trend up | — |

**Bond hedges in supply-shock states.** The IMF's April 2026 GFSR notes that frequent supply shocks have weakened the equity–bond hedge and raised the risk of simultaneous sell-offs [S]. This confirms that duration is unreliable in SS and GW.

### 2.5 Stabilisation vs savings funds and the owner's financing hierarchy

**IMF framing** [S].
- Das, Lu, Mulder & Sy (2009, IMF WP/09/179) set out SWF objectives and funding, withdrawal and spending rules. The IMF listing orders the authors Mulder, Sy, Lu, Das.
- The IMF's 2014 *Sovereign Asset-Liability Management—Guidance for Resource-Rich Economies* argues for managing risk on the whole sovereign balance sheet.

**The financing hierarchy.** In practice owners finance a gap $G_t$ in roughly this order [P]/[S]:
1. cash and stabilisation balances;
2. debt issuance;
3. draws on savings funds;
4. asset sales or transfers.

Kuwait's 2025 Financing and Liquidity Law is a clear case: debt is issued to finance deficits and *replenish the GRF* [S]. ADIC's share $\omega_t$ of the residual gap is a political-economy parameter. It is unobservable from public data and must be elicited [I].

### 2.6 Owner behaviour vs endowment behaviour

**Endowments** cut payouts after negative shocks and do not raise them after positive ones (Brown, Dimmock, Kang & Weisbenner 2014, *AER* 104:931–62) [S].

**Oil sovereigns.**
- The IMF's 2025 UAE Article IV states: "In the past, the general government fiscal stance has been generally procyclical" [S].
- Erbil (2011, IMF WP/11/171) studies 28 developing oil producers over 1990–2009 [S]:
  - fiscal variables are strongly procyclical in the full sample;
  - expenditure is countercyclical in the high-income group.
- The UAE's 2025–27 budgets use conservative revenue assumptions. The IMF argues this acts like an automatic stabiliser [S].

**Implication** [I]: the owner's *spending* may be smoothed by buffers, but *financing needs* still rise in busts. ADIC's band is the transmission belt.

### 2.7 Cross-disciplinary transfers [I]

- **Hydro-reservoir operations (SDDP).** The fund is a reservoir:
  - stochastic inflows are returns and PE distributions;
  - releases are owner draws and capital calls;
  - minimum storage is the liquidity floor;
  - spill is fire-sale loss.
  Regime-dependent inflow models with Markov-chain SDDP transfer directly (Pereira & Pinto 1991 [U]).
- **Bank treasury ALM.** Behavioural run-off and contingent credit-line drawdowns, where drawdowns rise in stress, are the template for regime-conditional draw-down rates. The LCR/NSFR logic gives haircut-weighted coverage ratios (BCBS 2013 [U]).
- **Insurance.** "Mass-lapse" stresses map to a "mass-draw" stress: an owner override above 10%. Dynamic lapse maps to a regime-dependent draw.
- **Actuarial ruin theory.** Liquidity survival is a ruin problem with a stochastic, regime-dependent premium and claim process. Survival horizon is the natural IC metric.
- **Real options.** The owner holds the draw option. ADIC can *buy back* part of it with oil options, or with committed liquidity: NAV facilities and secondary forward-sale options.
- **Control.** Chance-constrained, tube-based model-predictive control (MPC) handles hard liquidity floors under regime uncertainty.
- **Decision science.** Structured expert elicitation (SHELF, Cooke's classical model) supplies priors for unobservable owner parameters.
- **Machine learning.** Real-time shock-type nowcasting combines market-based decomposition with LLM event flags from news (OPEC decisions, attacks, ceasefires).

---

## 3. Methods, models and trade-offs

### 3.1 Oil price and shock-type models

| Model | Strengths | Weaknesses | Use in ADIC |
|---|---|---|---|
| GBM / log-OU | simple, closed forms | no regimes, no shock type | sanity checks only |
| Schwartz–Smith two-factor (short-term OU + long-run random walk) [S] | matches futures term structure; separates transitory from permanent shocks | regime-free | **core price dynamics**, with regime drifts and jumps added |
| Markov-switching VAR (Hamilton 1989 [S]) on oil, equity, credit | regime-dependent covariances | states capture volatility, not cause; label switching | macro regime $S_t$ (Stream 10) |
| SVAR shock decomposition (Kilian 2009; Baumeister–Hamilton 2019) [S] | economically identified demand vs supply | monthly, revised, needs global activity data | **historical labelling** of $Z_t$; priors on loadings |
| Market-based daily decomposition (Ready 2018; Bernanke 2016) [S] | real time, uses producer equities, copper, rates, VIX | reduced form; breaks when sector composition shifts | **nowcast** of $P(Z_t)$ |
| News shocks (Känzig 2021) [S] | clean supply-expectation shocks | OPEC-specific; UAE now outside OPEC | event study of OPEC+ and UAE policy |
| Narrative event flags (LLM-extracted) [I] | catches wars, closures, ceasefires the moment they happen | needs governance and verification | **GW and PS triggers** |

### 3.2 Owner fiscal and draw models

| Approach | Description | Pros | Cons |
|---|---|---|---|
| **A. Reduced-form clipped regression** | $d_t=\Pi(c-b\,FB_t+\rho\,\Delta d_{t-1}+\eta_t)$ | transparent; maps to a put spread | needs draw history; misses volume and war channels |
| **B. Structural fiscal module plus financing hierarchy** | revenue (price×volume), spending reaction, gap, hierarchy, ADIC share | captures GW (volume) and debt substitution | many unobservables |
| **C. Bayesian hierarchical** | B with priors from elicitation, partially pooled with peer episodes (Saudi 2015–16, Kuwait 2020, Norway 2016, Alaska FY15–17) | honest uncertainty; learns from each observed draw | heavier compute; relies on elicitation quality |
| **D. Policy-rule overlay** | Tobin/Yale smoothing, POMV averaging, override probability | represents governance explicitly | assumes the rule is followed |

**Recommendation** [I]: use B for structure, estimated as C, with D as the outer layer and A as the IC-facing summary (the put-spread representation).

### 3.3 Calibration with limited data

1. **Anchor to official tables** [S]:
   - IMF Article IV fiscal tables: breakeven path, hydrocarbon share and balances;
   - IMF DataMapper fiscal-balance history, used for the **swing** calibration (2014→15, 2019→20, 2025→26);
   - EIA STEO volume and price paths for the current shock.
2. **Use peer episodes as pseudo-data.** Pool response elasticities (draw or redemption per unit fiscal swing) hierarchically across Saudi Arabia, Kuwait, Norway, Alaska and Oman, with country effects [I].
3. **Structured elicitation** (SHELF protocol; Cooke performance weights using seed questions with known answers, e.g. "UAE 2015 fiscal balance") covers [I]:
   - $P^{BE}$, $b$, $\omega$, $\rho$;
   - override probability;
   - GW persistence;
   - DB distribution haircut.
4. **Entropy pooling** (Meucci 2008 [S]) reweights simulated paths to match EIA/IMF anchor paths and IC views without re-simulating. Cross-link: Stream 10 §6.10.
5. **Sequential Bayesian updating.** Every realised draw and fiscal release updates $(b,\omega,\rho,P^{BE})$, using a particle filter on a latent "owner stress" state [I].
6. **Reverse stress test.** Search for the most plausible factor path that breaches the DCR, by minimising Mahalanobis distance subject to the breach (Breuer et al. 2009 [S]). Report it as a narrative.

### 3.4 Hedge-design methods

| Method | Objective | Comments |
|---|---|---|
| Minimum-variance cross-hedge $h^*=\mathrm{Cov}(\Delta D,\Delta F)/\mathrm{Var}(\Delta F)$ | variance of draw surprise | unstable: the sign flips across eras |
| **CVaR-optimal static hedge (LP)** over a scenario × instrument payoff matrix (Rockafellar–Uryasev 2000 [S]) | minimise $\mathrm{CVaR}_\alpha$ of the *liquidity shortfall*, not of NAV | **recommended**: targets the state that costs money |
| Replicating the draw put spread with listed or OTC oil options | match liability convexity | capacity- and tenor-limited; basis to Murban [U] |
| Joint-state hybrids: dual digitals, best-of puts, oil-conditional equity puts (Stulz 1982 closed forms [S]) | pay only in DB-type states | cheap when *priced* correlation is low; correlation-skew model risk |
| Natural hedge (Bodie–Brière term) | underweight owner-correlated assets | no premium, but tracking and opportunity cost |
| Contingent liquidity: committed NAV facility, secondary forward-sale option, repo lines | convert illiquid assets into cash in DB | commitment fees; counterparty WWR. Cross-link: Stream 05 |

---

## 4. Empirical evidence and current market data

### 4.1 Oil–equity co-movement by era [I-calc]

**Method.** Monthly log returns of EIA Brent spot (end-of-month from the daily series) against the US market total return (Ken French Mkt−RF+RF), developed-market returns and month-end ΔVIX. Data run to 14 Oct 2026 for Brent and Aug 2026 for equities.

| Window | n (oil months) | ρ(oil, US eq) | ρ(oil, Dev eq) | ρ(oil, ΔVIX) | Oil vol (ann.) |
|---|---|---|---|---|---|
| 1988–2007 | 240 | −0.14 | −0.08 | +0.08 | 37% |
| 2008–2019 | 144 | **+0.43** | +0.47 | −0.33 | 35% |
| 2020–Aug 2026 | 82 | +0.32 | +0.33 | −0.31 | 69% |
| GFC, Jul 08–Mar 09 | 9 | +0.35 | +0.34 | −0.20 | 67% |
| Oil bust, Jul 14–Feb 16 | 20 | +0.40 | +0.50 | −0.43 | 42% |
| Covid, Jan–Jun 20 | 6 | **+0.81** | +0.85 | −0.57 | 220% |
| 2022 | 12 | −0.01 | 0.00 | 0.00 | 35% |
| 2023–2025 | 36 | +0.01 | −0.06 | −0.06 | 24% |
| War, Mar–Aug 26 | 6 | **−0.58** | −0.63 | +0.46 | 119% |

**Rolling and tail measures.**
- The rolling 36-month correlation was positive in 40% of months before 2008 and in 90% after 2008.
- Its latest value (Aug 2026) is **−0.28**. Its range is −0.60 (May 1993) to +0.71 (Dec 2021).
- Empirical lower-tail dependence (joint 10% quantile) is 0.08 for 1988–2007 and **0.30** for 2008–2026.

**Caveat.** Windows of n≤12 are noisy. They describe episodes, not estimates.

### 4.2 Joint tails and shock-type frequencies [I-calc]

**Calendar years 1988–2025 (38 years), sign of Brent change vs US equity return:**

| | Equities down | Equities up |
|---|---|---|
| **Oil down** | 4 years: 2000, 2001, 2008, 2018 | 13 years |
| **Oil up** | 4 years: 1990, 1994, 2002, 2022 | 17 years |

Brent fell ≥30% in 1991, 1997, 1998, 2008, 2014 and 2015, and equities fell only in 2008. Annual aggregation hides intra-year joint crashes. In 2020, for example, Brent was −24% and equities +24% for the year. Liquidity modelling must therefore be monthly or quarterly.

**Overlapping 12-month windows, 1988–2026:**

| Event | Probability |
|---|---|
| Oil −30% or worse | 11.7% |
| Oil −40% or worse | 6.1% |
| Oil +50% or more | 15.2% |
| Equities −10% or worse | 11.3% |
| **Equities ≤ −10%, given oil ≤ −30%** | **26%** (pre-2008: 18%; post-2008: 30%) |
| Equities ≤ −20%, given oil ≤ −30% | 18.5% |
| Oil ≤ −30%, given equities ≤ −20% | 53% (n=19 overlapping months, essentially one episode) |

**Shock-type shares of 12-month windows** (sign rules: DB = oil≤−20% and eq≤−10%; SG = oil≤−20% and eq>0; SS = oil≥+30% and eq<0; B = oil≥+30% and eq≥+10%):

| Label | Share |
|---|---|
| Normal | 59.6% |
| Demand boom | 17.8% |
| Supply glut | 13.5% |
| Supply spike | 5.0% |
| Demand bust | 4.1% |

**Sign rules mislabel some episodes:**
- windows ending around May 2020 read as "glut", because equities rebounded on policy support;
- 2026 windows read as "boom", because equities rose on AI.

This is why the design needs structural plus narrative identification (§3.1).

**Low-price spells** (Brent month-average below 70% of its trailing 36-month mean):
- Dec 2014 onward: **22 months**;
- Nov 2008: 6 months;
- Mar 2020: 4 months;
- 1998: several short spells.

### 4.3 Statistical regimes [I-calc]

**Specification.** Gaussian HMM on monthly (oil, US equity) log returns, Jun 1987–Aug 2026, with oil winsorised at the 1st/99th percentile. An unwinsorised 3-state fit collapsed onto the April 2020 outlier (see §7).

| State | Share | Expected duration | Oil vol | Equity vol | ρ | Equity mean (ann.) |
|---|---|---|---|---|---|---|
| Calm | 69% | 18.6 months | 25% | 10.6% | 0.01 | +18% |
| Turbulent | 31% | 8.9 months | 52% | 22.8% | 0.16 | −6% |

**Transitions.** Monthly P(calm→turbulent) is 5.4% and P(turbulent→calm) is 11.2%.

**Conclusion.** Volatility regimes are well identified. *Shock type* is not, so a separate $Z_t$ layer is needed.

### 4.4 The 2026 Gulf war shock [S]

| Item | Value | Source |
|---|---|---|
| Onset | Military action began **28 Feb 2026**; Hormuz shipping "extremely limited" | EIA STEO Jun 2026; Al Jazeera 29 Apr 2026 |
| Brent | 2025 avg US$69; Mar 2026 settle US$94 (9 Mar); monthly avg Apr US$117, May US$107, Sep US$114; daily peak US$131 (15 Sep, STEO); EIA spot US$135.51 (2 Oct), US$126.55 (14 Oct) | EIA STEO Mar/Jun/Oct 2026; EIA RBRTE |
| Gulf crude shut-ins | peak ≈10.9 mb/d (May; earlier estimate 11.3); 5.8 (Aug); 4.8 (Sep); forecast 4.5 (4Q26) and 2.7 (1Q27) | EIA STEO Oct 2026, Table 1 |
| UAE shut-ins | Feb-26 output 3.60 mb/d; Mar 1.45, Apr 1.10, May 1.35 mb/d (Jun STEO); revised to Mar–Jul avg 0.74 and Aug/Sep 0 (Oct STEO) | EIA STEO |
| UAE liquids output | 2025 4.34 mb/d; 2Q26 3.40; 2026 4.12; 2027F 5.20 | EIA STEO Oct 2026, Table 3b |
| UAE OPEC exit | effective **1 May 2026**; EIA cut its 2027 OPEC spare-capacity estimate from 3.8 to 2.5 mb/d | EIA STEO May 2026 |
| UAE capacity vs quota | capacity 4.8 mb/d vs 3.2 mb/d OPEC quota; target 5 mb/d by 2027; Fujairah exported 1.7 mb/d of crude and products in 2025 | Al Jazeera 29 Apr 2026 (figures vary across sources) |
| Bypass capacity | Hormuz 20 mb/d in 2024 (≈20% of global liquids use); Saudi East-West 5 mb/d (7 temporarily); UAE line to Fujairah 1.8 mb/d; ≈2.6 mb/d unused bypass | EIA *Today in Energy*, 16 Jun 2025 |
| New UAE bypass capacity | expected mid-2027 | EIA STEO Sep 2026 |
| Price outlook | Pre-war Feb STEO: US$58 (2026), US$53 (2027). Now: 2026 US$96, 4Q26 US$105, 2Q27 US$87, 4Q27 US$74, 2027 US$84 | EIA STEO Feb/Oct 2026 |
| Inventories | OECD stocks expected at their lowest since 2003 | EIA STEO Jun 2026 |
| Macro | ME&CA 2026 GDP −0.3% (April forecast: +1.9%); Kuwait −16.7%, Iraq −16.0%, Qatar −15.6%, Bahrain −11.3%, Iran −7.6%, Saudi −3.3%. UAE 2026 −3.9%, 2027 +7.7% | IMF WEO Oct 2026 via Al Jazeera 13 Oct 2026; IMF DataMapper |
| Markets | US equities −4.9% in March, +10.2% in April 2026; VIX 19.99 (16 Oct 2026); Brent daily realised vol 77% since 1 Mar 2026 vs 36% in 2015–19 | [I-calc] Ken French, CBOE, EIA |

### 4.5 UAE fiscal anchors [S]

**IMF 2025 Article IV (8 Dec 2025, pre-war):**
- **Fiscal breakeven** (US$/bbl): 54.0 (2023), 48.3 (2024), 45.7 (2025), 44.8 (2026), 44.8 (2027), 45.2, 45.6, 45.9 (2030).
- **Hydrocarbon revenue** (% of GDP): 13.4, 14.8, 12.5, 11.3 (2026), then 9.1 in 2030.
- **Hydrocarbon share of general-government revenue**: 47% (2023), 53% (2024), 44% (2025), 41% (2026), 32% (2030) [I-calc from Table 3a].
- **Coverage.** Figures exclude SWF investment income and cover Abu Dhabi accounts only partially.
- **Fiscal stance.** A general-government surplus of ≈5% of GDP was projected for 2025–26. The dirham's peg to the US dollar "continues to provide a credible policy anchor".

**IMF DataMapper** (accessed 18 Oct 2026): general-government net lending, % of GDP.

| Year | Net lending (% of GDP) |
|---|---|
| 2014 | +1.7 |
| 2015 | −6.4 |
| 2016 | −3.0 |
| 2017 | −0.2 |
| 2018 | +3.7 |
| 2019 | +2.5 |
| 2020 | −2.4 |
| 2021 | +4.0 |
| 2022 | +9.8 |
| 2023 | +5.8 |
| 2024 | +6.2 |
| 2025 | +3.9 |
| **2026** | **+1.5** |
| 2027 | +4.4 |

GDP was US$425bn (2014), US$382bn (2015), US$614bn (2025) and US$661bn (2026).

**Comparators** (net lending, % of GDP):
- Saudi Arabia: −14.9 (2015), −13.2 (2016), −10.2 (2020), −6.5 (2026).
- Kuwait, including investment income: 29.8 (2014), 0.2 (2020), 15.8 (2026).

**Back-of-envelope calibration** [I-calc].
- The mapping $FB\approx 11\ln(P/44.8)$ gives +4.75pp at 2025's US$69, close to the IMF's 3.9.
- At 2026's ≈US$96 it gives +8.4pp, against the IMF's 1.5. The implied GW wedge is **≈−6 to −7pp of GDP**.
- The 2014→15 swing of −8.1pp on a −47% move in average Brent (log change −0.64) implies $h\approx13\%$ at the time, consistent with higher oil dependence then.

### 4.6 Oil-sovereign withdrawals in busts [S]

- **2015 redemptions.** SWFs redeemed at least US$46.5bn from asset managers (eVestment, via FTfm). Middle Eastern oil SWFs withdrew US$19bn in Q3 2015 alone, described as the fastest withdrawal pace on record (FT/eVestment, via IR Impact).
- **SAMA and BlackRock.** SAMA withdrew ≈US$70bn from managers in 2015. BlackRock saw ≈US$31bn of withdrawals by government institutions in Q2–Q3 2015 (Morgan Stanley).
- **Moody's** expected oil funds to raise redemptions "to plug fiscal deficits".
- **Norway:** first-ever withdrawal in January 2016. NBIM's published figures for recent years show only inflows and no withdrawals: NOK 1,090bn (2022), ≈711bn (2023, derived from cumulative totals), 409bn (2024), 327bn (2025) and 94bn (H1 2026). The fund was worth NOK 22,683bn at 30 Jun 2026.
- **Saudi Arabia:** SAMA transferred SAR150bn (US$40bn) to the PIF in March–April 2020. PIF's governor later described receiving "tens of billions of dollars" from the central bank for its early-2020 stock purchases.
- **Kuwait:**
  - transfers to the FGF have been ≈zero in recent years (0.0–0.1 in the IMF fiscal table);
  - the March 2025 Financing and Liquidity Law allowed the first debt issuance since 2017;
  - 2025 issuance was 4.6% of GDP domestic plus 7.2% external, used to finance deficits and replenish the GRF;
  - KIA AUM was ≈640% of GDP at end-2025 (IMF Article IV, Feb 2026).
  - Stream 02 documents the 2020 liquidity crunch.
- **Alaska:**
  - the North Slope oil price fell from US$107.57 (FY2014) to US$50.05 (FY2017), and state revenue fell by about 80%;
  - legislation (SB 26) set a draw of 5.25% of the average balance over the first 5 of the last 6 years, an effective draw of about 4.2%.
- **Endowments** behave the opposite way (Brown et al. 2014).

### 4.7 Private-markets liquidity [S]

Bain's *Global PE Report 2026* (MSCI data) reports for 2025:
- distributions ≈14% of NAV;
- distributions below 15% for four consecutive years, a record, and last this low in 2008–09;
- average holding period at exit ≈7 years;
- ≈32,000 unsold companies worth ≈US$3.8trn;
- 53% of LPs say undrawn commitments constrain new commitments;
- buyout exit value up 47% to US$717bn.

**Cyclicality.** Distributions are more procyclical than calls (Robinson & Sensoy 2016, *JFE* 122(3) [S, DOI verified]).

**Starting point** [I]: the private book enters any new demand bust from an *already* depressed distribution base.

### 4.8 Hedging evidence [S]

**Mexico** (IMF blog, Valencia, March 2018; academic companion: Ma & Valencia 2018, IMF WP/18/35):
- annual Asian puts on Maya crude, struck near the budget oil price;
- ≈29% of production hedged on average over ten years;
- cost ≈0.1% of GDP a year since 2001;
- exercised in 2009, 2015 and 2016, paying ≈0.5%, 0.6% and 0.3% of GDP;
- main benefit: sovereign borrowing costs ≈19bp lower;
- political economy explains why few countries copy it.
- Press reports put the payouts at US$5.1bn (2009), US$6.4bn (2015, strike US$76.40) and US$2.7bn (2016). 2020 details were classified.

**Borensztein, Jeanne & Sandri** (IMF WP/09/229): reducing the need for precautionary foreign assets can yield welfare gains "amounting to several percentage points of annual consumption", much larger than the gains from smoothing alone.

### 4.9 Joint-state hedge pricing illustration [I-calc]

**Set-up.** Risk-neutral bivariate GBM, r=4%, 1-year tenor. Oil strike at 80% of spot, equity strike at 90%. Premia are % of notional (puts normalised by strike); 400k paths.

| Structure | Calm vols (35%/16%) ρ=−0.4 | ρ=0 | ρ=+0.6 | 2026 vols (70%/20%) ρ=−0.4 | ρ=0 | ρ=+0.6 |
|---|---|---|---|---|---|---|
| Oil put 80% | 4.95 | 4.95 | 4.95 | 17.78 | 17.78 | 17.78 |
| Equity put 90% | 1.63 | 1.63 | 1.64 | 2.81 | 2.82 | 2.82 |
| Worst-of put | 6.47 | 6.22 | 5.56 | 20.01 | 19.35 | 18.25 |
| Best-of ("dual-down") put | 0.11 | 0.36 | 1.02 | 0.58 | 1.24 | 2.34 |
| Dual digital (both below) | 2.25 | 5.55 | 12.08 | 7.43 | 12.51 | 20.36 |
| Equity put, live only if oil <80% | **0.14** | 0.47 | 1.16 | **0.68** | 1.39 | 2.43 |
| Q-prob(joint down) | 2.35 | 5.78 | 12.57 | 7.74 | 13.02 | 21.19 |

**Reading** [I].
- Joint-state protection is cheap when the *priced* correlation is low or negative. That is the current supply-shock regime: rolling ρ −0.28, war months −0.58.
- It pays in demand busts, where realised correlation jumps (Covid +0.81).
- The opportunity is real only if dealers' correlation marks and correlation skew are below our physical-measure DB probability. This must be tested against dealer quotes.
- Oil-strike structures are currently expensive (realised oil vol 77%). Equity-strike structures conditioned on oil are not.

---

## 5. Peer practice and case studies

**Norway (GPFG)** [S].
- The government may withdraw up to the fiscal-rule amount (3% expected real return).
- Even this most rules-based oil fund turned to its first net withdrawal in January 2016 during the slump.
- On 8 Mar 2019 the government proposed removing exploration-and-production companies from the benchmark "based on an overall assessment". The rationale is widely read as reducing oil-price exposure of national wealth [P]. Norges Bank's 2017 advice could not be fetched [U].
- **Lesson** [I]: marginal underweighting of owner-correlated assets is accepted peer practice. It is cheap, but small relative to below-ground exposure.

**Saudi Arabia** [S].
- Deficits of 14.9% and 13.2% of GDP in 2015–16 coincided with large SAMA redemptions from external managers.
- In 2020 SAMA moved reserves to the PIF.
- 2026 shows a 6.5%-of-GDP deficit despite higher prices [S]. The likely drivers are volume shut-ins (EIA estimates ≈2.75 mb/d on average over March–July) and dependence on the East-West bypass, which was itself attacked in September 2026 [I].
- **Lesson** [I]: export-route fragility can make the "oil-up" state fiscally negative.

**Kuwait** [S].
- Legally ring-fenced long-term savings (the FGF) were inaccessible, and the liquid pocket (the GRF) ran low in 2020 (Stream 02).
- The response was to stop FGF transfers and later legislate debt issuance (March 2025) to replenish the GRF.
- **Lesson** [I]: owners substitute debt for fund draws when they can. The share ω is endogenous to debt-market access and to legal plumbing.

**Alaska Permanent Fund** [S].
- An oil-revenue collapse of about 80% (FY2014→17) led to a statutory percent-of-market-value (POMV) draw on 5-year average balances.
- Stream 02 covers the override history.
- **Lesson** [I]: averaging smooths draws but shifts risk into sequence and liquidity.

**Mexico** (§4.8).
- The only long-running large sovereign oil hedge.
- **Lesson** [I]: a programme struck at the budget price and sized as a minority of exposure is politically sustainable and credit-positive. Full hedging is not.

**Chile** (Bodie–Brière application) [S].
- An integrated ALM view recommends more diversification.
- Copper exposure enters via the fiscal surplus with sensitivity 0.15, not 1.

### Abu Dhabi landscape and ADIC (public sources only)

**ADIC** [S].
- Began operating in April 2007 as a spin-off from ADIA, taking over ADIA's local subsidiaries (Wikipedia citing archived ADIC pages).
- A March 2018 law restructured ADIC under Mubadala's ownership (WAM, 21 Mar 2018; Official Gazette, 30 Apr 2018).
- The National (21 Mar 2018) reported:
  - ADIC at ≈US$123bn and Mubadala at ≈US$127bn (SWFI estimates);
  - stakes in FAB (33.4%), ADCB (62.5%), Union National Bank (50%) and Al Hilal Bank, among others.
- **2026 reporting.**
  - Bloomberg (4 Feb 2026) described a "US$160 billion" endowment-style fund. Per search-snippet text, it is an independently run unit of Mubadala targeting at least 10%, and has added secondaries, Bitcoin exposure and an insurance push under a CEO appointed in late 2023. The article is paywalled and was not read in full.
  - Jawlah (11 Jun 2026, citing Bloomberg) reported that ADIC leads a plan to deploy up to US$15bn in leveraged hedge-fund strategies.
- **Client figures vs public figures.** The client-stated US$177bn and the 5–10% distribution band are not publicly reported, as far as we found. The difference from ≈US$160bn may reflect date or measurement.
- We make no inference about internal matters.
- **Domestic stakes** [I]: whether the 2018-era domestic bank stakes are still held is unknown. If they are, they are likely the most owner-correlated, least saleable assets in a fiscal stress.

**Other Abu Dhabi entities** [S].
- Mubadala: AUM ≈US$330bn (2024, per Wikipedia citing Mubadala).
- L'imad Holding:
  - launch reported as late 2025, though one report says 15 January;
  - chaired by Crown Prince Sheikh Khaled bin Mohamed since January 2026;
  - ADQ's assets (≈US$263bn AUM as of January 2026, per AsiaAsset) consolidated under it from January 2026 (Circuit, 30 Jan 2026).
- ADIA's size was not verified in-session.

**UAE energy policy** [S].
- OPEC exit effective 1 May 2026.
- An Ember analyst quoted by Al Jazeera framed the exit as preparing for lower demand by selling as much oil as possible before fossil-fuel demand declines.
- Combined with the IMF's projected fall in hydrocarbon revenue share to 9.1% of GDP by 2030, this suggests [I]:
  - $h_t$ falls structurally, which lowers the draw-beta to oil;
  - the price-war (SG) hazard rises.

---

## 6. Design implications for the ADIC framework

### 6.1 Placement

The liability module ("Owner Draw Engine", ODE) sits inside the scenario generator (Stream 10) [I].
- **Inputs:** the joint regime $(S_t,Z_t)$, oil and volume paths, and macro factors.
- **Output:** draw paths $D_t$ that feed:
  - the liquidity engine;
  - the Tier-1 gate (Streams 01 and 02);
  - the overlay margin engine (Stream 09);
  - SELL/HOLD/REFINANCE/LEVER valuation (Streams 05 and 08).

### 6.2 State variables (quarterly liquidity step; annual draw decisions) [I]

| Symbol | Meaning | Default or initialisation (18 Oct 2026) |
|---|---|---|
| $S_t$ | macro-financial regime (Stream 10) | filtered posterior |
| $Z_t$ | oil/fiscal shock type ∈ {N, B, SG, DB, SS, GW} | GW with high posterior; next-year transition prior from row GW (Table 6.3) |
| $\chi_t,\xi_t$ | short- and long-run log Brent factors | $\ln 126.55$ split by curve backwardation; long-run anchor US$70 nominal [I] |
| $\beta^{M}_t$ | Murban–Brent basis | from ICE Futures Abu Dhabi [U]; default 0 ± 2 US$/bbl |
| $q_t$ | owner export-volume index (share of capacity available) | 2026 average ≈0.95 of 2025 (4.12 vs 4.34 mb/d); 2Q26 trough ≈0.75 of 4Q25 (3.40 vs 4.52); path from EIA |
| $FB_t$ | owner fiscal balance, pp of GDP | IMF 2026: +1.5 |
| $h_t$ | hydrocarbon revenue / GDP | 11.3% (2026) → 9.1% (2030) [S] |
| $P^{BE}_t$ | effective breakeven | prior lognormal, median US$55, 90% CI US$45–70 [I] (IMF consolidated value 44.8 as lower anchor) |
| $B^{own}_t$ | owner's liquid buffers and debt capacity | latent; elicited |
| $d_{t-1}$ | last draw rate | client data |
| $NAV_t, L_t, U_t$ | NAV, haircut liquidity, unfunded commitments | client data |
| $\gamma_{d,t},\gamma_{c,t}$ | PE distribution and call rates (Stream 10 notation) | baseline γ_d ≈14% of NAV [S] |
| $m_t$ | overlay margin requirement | Stream 09 |
| $\mathcal H_t$ | liability-hedge book (oil spreads, hybrids, facilities) | none |

### 6.3 Shock-type layer $Z_t$: dynamics and default priors

**Annual transition prior** (rows are the current state) [I]. It is designed to roughly reproduce the 12-month-window shares in §4.2 and plausible durations. **It must be re-estimated on labelled history and elicited.**

| From \ To | N | B | SG | DB | SS | GW | Expected duration (years) |
|---|---|---|---|---|---|---|---|
| N | 0.62 | 0.15 | 0.10 | 0.05 | 0.04 | 0.04 | 2.6 |
| B | 0.40 | 0.40 | 0.05 | 0.06 | 0.07 | 0.02 | 1.7 |
| SG | 0.38 | 0.12 | 0.42 | 0.04 | 0.02 | 0.02 | 1.7 |
| DB | 0.35 | 0.30 | 0.20 | 0.10 | 0.03 | 0.02 | 1.1 |
| SS | 0.30 | 0.05 | 0.10 | 0.35 | 0.15 | 0.05 | 1.2 |
| GW | 0.30 | 0.05 | **0.35** | 0.05 | 0.05 | 0.20 | 1.25 |

- **Stationary distribution:** N 49%, B 20%, SG 16%, DB 7%, SS 5%, GW 4% [I-MC].
- **Row GW** encodes the post-war glut thesis (§1.4).
- **Row SS** encodes stagflation turning into a bust, as in 2008.

**Coupling to Stream 10's $S_t$** [I]:
- $P(S_t=\text{crisis}\mid Z_t=DB)\ge0.8$;
- $P(S_t=\text{crisis}\mid Z_t=SG)\approx0.15$;
- otherwise use a sparse coupling matrix, estimated jointly.

**Overlays** [I]:
- **ET:** a drift on the long-run factor of $\mu_\xi=-2\%$ a year real from 2030 (high-transition scenario), with $h_t$ declining. Calibrate to the latest IEA and NGFS scenarios, which were not verified here.
- **PS** (peg / financial stress): Bernoulli with $p=1\%$ a year in N/B and $p=5\%$ in GW/SG/DB. It triggers higher owner USD demand and a band-override probability.

### 6.4 Oil and market factor equations (annual form; monthly analogue for liquidity)

$$\ln P_{t+1}=\ln P_t+\kappa(\ln P^{LR}_t-\ln P_t)+\mu_{Z_{t+1}}+\sigma_{Z_{t+1}}\varepsilon^{o}_{t+1}+J_{t+1}\mathbb 1\{Z_{t+1}=GW\}$$

- $\kappa=0.40$;
- $P^{LR}$ = US$70, nominal, with the ET drift applied;
- $(\mu,\sigma)_Z$ by state:

| State | (μ, σ) |
|---|---|
| N | (0, 0.20) |
| B | (+0.20, 0.20) |
| SG | (−0.35, 0.20) |
| DB | (−0.45, 0.25) |
| SS | (+0.30, 0.25) |
| GW | (+0.10, 0.30) |

- Jumps $J$: ±30% with probability 0.25 in GW.

These defaults give P10/P50/P90 Brent of US$60/90/137 one year ahead and US$41/71/114 three years ahead, starting from GW at US$126 [I-MC]. That illustrative run excludes jumps. The one-year median is slightly above EIA's 2027 average of US$84.

**Equity and credit loadings** (state-conditional correlation with oil) [I]:
$$r^{eq}_{t+1}=\mu^{eq}_{Z}+\sigma^{eq}_{Z}\big(\rho_Z\varepsilon^{o}_{t+1}+\sqrt{1-\rho_Z^2}\,\varepsilon^{e}_{t+1}\big).$$

| State | $\rho_Z$ | $\mu^{eq}_Z$ | $\sigma^{eq}_Z$ |
|---|---|---|---|
| N | 0.0 | +7% | 15% |
| B | 0.2 | +15% | 14% |
| SG | 0.1 | +5% | 16% |
| DB | **0.6** | −25% | 25% |
| SS | −0.4 | −10% | 22% |
| GW | −0.5 | −5% | 20% |

**Calibration targets.** The mixture must reproduce §4.1:
- unconditional correlations by era of −0.14, +0.43 and +0.32;
- tail dependence of about 0.3 post-2008;
- 12-month conditional probabilities of 26% and 18.5%.

### 6.5 Owner fiscal module [I]

**Revenue.**
- Hydrocarbon revenue: $HR_t=HR_0\,(P_t e^{\beta^M_t}/P_0)^{\eta_P}(q_t/q_0)^{\eta_Q}$, with $\eta_P\approx\eta_Q\approx1$.
- Non-hydrocarbon revenue $NHR_t$ grows with non-oil GDP, and is lower in GW and DB.

**Spending.**
$$\Delta\ln G_t=\psi_0+\psi_1\Delta\ln P_{t-1}+\psi_2\mathbb 1\{GW\}+\psi_3\mathbb 1\{DB,SG\}.$$
- $\psi_1\approx0.3$ captures procyclicality [S: IMF].
- $\psi_2$ covers defence, reconstruction and support for tourism, aviation and real estate.

**Balance:** $FB_t=(HR_t+NHR_t-G_t)/GDP_t$.

**Reduced form for simulation:** $FB_t=100\,h_t\ln(P_t/P^{BE}_t)+w_{Z_t}+\epsilon^{FB}_t$, with $w_Z$ in pp of GDP:

| State | $w_Z$ |
|---|---|
| N, B | 0 |
| SG | −0.5 |
| DB | −1.5 |
| SS | −0.5 |
| **GW** | **−6** (from the 2026 wedge, §4.5) |

$\sigma_{\epsilon^{FB}}=1.0$pp.

**Financing hierarchy.**
1. The gap is $G^+_t=\max(0,-FB_t\cdot GDP_t)$.
2. Cash and debt cover $\min(G^+_t,\ \text{Cap}^{debt}_t+\text{Cash}_t)$. Debt capacity shrinks in PS.
3. The residual is allocated to funds, and ADIC's share is $\omega_t$, with an elicited prior.

### 6.6 Draw model (the ODE core)

$$d^*_t=\Pi_{[5\%,10\%]}\big(c-b\,FB_t\big),\qquad d_t=\Pi_{[5\%,10\%]}\big(\rho d_{t-1}+(1-\rho)d^*_t\big),\qquad D_t=d_t\,NAV^{basis}_t$$

- **Defaults** [I], all to be replaced by elicitation and client data:
  - $c=7.5\%$ and $b=0.625$ %NAV per pp of GDP, so the draw is at the floor when FB ≥ +4pp and at the cap when FB ≤ −4pp;
  - $\rho=0.5$;
  - $NAV^{basis}$ = opening NAV, unless the mandate specifies trailing averaging.
- **Structural variant:** $d^*_t=\Pi\big(d_{lo}+\omega_t\,\text{residual gap}_t/NAV_t\big)$.
- **Band override:** with probability $p^{ov}_Z$ the draw is $10\%+u$, where $u\sim U(2\%,5\%)$:
  - $p^{ov}$ = 0.25% a year in N/B/SS;
  - 1% in SG/DB;
  - 2% in GW or PS.
  - Precedents are Kuwait's legal changes and Alaska's political overrides.
- **Kinks under the defaults:** $K_H$≈US$64.4 and $K_L$≈US$31.1 [I-calc]. Re-derive them whenever $P^{BE}$ or $h$ updates, and publish them to the IC.

**Illustrative outputs** [I-MC]. These use 100k paths per cell over 10 years, start from GW at US$126 and use the Table 6.3 transitions. The base run uses 200k paths; jumps are excluded.

| Assumption set ($P^{BE}$, $b$) | Mean draw | P(draw ≥9.5%), avg of years 4–10 | P(≥3 consecutive years ≥9.5%) within 10y | Mean draw in DB / SG |
|---|---|---|---|---|
| 44.8, 0.625 | 6.0% | 1.1% | 0.8% | 6.9% / 6.8% |
| 44.8, 1.0 | 6.0% | 1.8% | 1.4% | 6.9% / 6.8% |
| 55, 0.625 | 6.7% | 4.1% | 3.6% | 7.6% / 7.6% |
| 55, 1.0 | 6.6% | 6.1% | 5.8% | 7.6% / 7.6% |
| 65, 0.625 | 7.3% | 10.0% | 10.2% | 8.1% / 8.2% |
| 65, 1.0 | 7.2% | 14.0% | 15.3% | 8.2% / 8.2% |

**Interpretation** [I].
- The breakeven matters roughly an order of magnitude more than the slope.
- Smoothing ($\rho$) delays cap hits by about one year. That is valuable warning time, but it also makes multi-year cap runs persistent.

### 6.7 Coupling to private-market cash flows (Stream 10 notation) [I]

$$\gamma_{d,t}=\bar\gamma_d\,m^{d}_{Z_t}\,e^{\beta_{d}r^{eq}_{t-1:t}},\qquad \gamma_{c,t}=\bar\gamma_c\,m^{c}_{Z_t},\qquad \delta^{sec}_t=\delta_0+\Delta\delta_{Z_t}+\delta_2(-r^{eq}_{t-3:t})^+ .$$

| State | $m^d$ | $m^c$ | $\Delta\delta$ (pp of NAV) |
|---|---|---|---|
| N | 1.0 | 1.0 | 0 |
| B | 1.2 | 1.1 | −2 |
| SG | 0.95 | 1.0 | +2 |
| DB | **0.45** | 0.85 | **+15 to +25** |
| SS | 0.85 | 0.95 | +5 |
| GW | 0.9 | 1.0 | +3 |

- $\bar\gamma_d$ ≈14% (2025 drought level [S]).
- The DB multipliers are elicitation targets, consistent with distributions being more procyclical than calls [S: Robinson–Sensoy].
- $\delta$ and NAV-loan spreads must be harmonised with Stream 05.

**Illustrative one-year net liquidity need** [I]. Assumptions:
- NAV US$177bn: 60% private (US$106bn) and 40% liquid (US$71bn);
- unfunded commitments 20% of NAV (US$35bn), base calls 30% of unfunded (US$10.6bn);
- base distributions 14% of private NAV (US$14.9bn).

| State | Draw | Calls | Distributions | Overlay margin | Net need |
|---|---|---|---|---|---|
| N | 6% | 10.6 | 14.9 | 0 | ≈US$6bn (3.6% NAV) |
| SG | 8% | 10.6 | 14.2 | 1 | ≈US$11.6bn (6.5% NAV) |
| DB | 10% (US$17.7bn) | 9.0 | 6.7 | 3.5 | **≈US$23.5bn (13% NAV)**, while liquid assets fall ≈20% |

A DB→SG→SG sequence consumes on the order of US$50–60bn. Without pre-arranged liquidity or hedges, that implies secondary sales at crisis discounts.

### 6.8 Constraints (Tier-1 additions) [I]

1. **Stressed Distribution Coverage Ratio, 12 months, for each stress state.**
$$DCR^{(Z)}_t=\frac{\sum_i(1-\eta^{(Z)}_i)L_{i,t}+\mathbb E^{(Z)}[\text{PE dist}_{t:t+4}]+\text{Committed facilities}_t+\mathbb E^{(Z)}[\text{hedge payoff}]}{D^{cap}_{t:t+4}+\text{Calls}^{(Z)}_{t:t+4}+\text{Margin}^{P99,(Z)}_{t:t+4}+\text{Debt service}_t}\ \ge\ 1.25$$
   - Apply for $Z\in\{DB, GW, SG\!+\!PS\}$, with $D^{cap}$ = 10% of NAV.
   - Default haircuts $\eta$: cash/T-bills 0; DM govts 3%; IG credit 10%; listed equity 30% (DB) or 20% (other states); HY and EM debt 35%; hedge funds 50–100% depending on gates (relevant to the reported leveraged-HF plan).
2. **Drought survival.** Cumulative sources ≥ cumulative uses under DB→SG→SG at cap draws, with no private sales below NAV×(1−δ_DB). Equivalently, the survival horizon at cap draws is ≥36 months.
3. **Chance constraint.**
   - $P\big(\min_{k\le8}L_{t+k}<L_{min}\big)\le1\%$ overall;
   - ≤5% conditional on $Z_t=DB$, evaluated under the ambiguity set (Stream 10 §6.8).
4. **Override reserve.** Additional HQLA of $p^{ov}_Z\times\mathbb E[u]\times NAV$, scaled up when $Z\in\{GW,PS\}$, or an equivalent committed facility.
5. **Hedge budget.** Liability-linked premium ≤ 25–50bp of NAV a year, unless the buffer-release test (§6.11) shows positive net value.
6. **Concentration.** Owner-correlated exposures (energy, GCC, domestic strategic stakes) ≤ X% of NAV, or carried with an owner-beta charge (§6.9).

### 6.9 Objective terms (Tier 2) [I]

**Owner-state weight.**
$$m^{own}_t=1+\kappa_{own}\,\frac{(FB^*-FB_t)^+}{\sigma_{FB}}\qquad(FB^*=+2\text{pp},\ \kappa_{own}=1\text{ default}).$$

**Owner-weighted return.**
$$J=\mathbb E\Big[\sum_t\beta^t m^{own}_t\,\Delta W_t\Big]-\lambda_{FS}\,\mathbb E[\text{fire-sale loss}]-\lambda_H\,\text{premia}-\lambda_{sh}\,\mathbb E[m^{own}_t(D_t-\text{paid}_t)^+].$$
This sits alongside the deck's P(10%) and α* terms.

**Owner beta**, reported for every asset and every SELL/HOLD/REFINANCE/LEVER action:
$$\beta^{own}_j=\mathrm{Cov}(r_j,d_t)/\mathrm{Var}(d_t).$$
- Positive (pays when draws are high) is valuable.
- Negative means the asset fails exactly when the owner calls. Domestic banks and energy credit are likely examples.

**Shadow prices.** Report the duals of the DB-DCR constraint and the drought constraint as **"liquidity shadow price, US$ per US$1 of buffer"**.

### 6.10 SELL / HOLD / REFINANCE / LEVER playbook by liability state [I]

| State | SELL | HOLD | REFINANCE | LEVER |
|---|---|---|---|---|
| N / B | sell selectively while secondary discounts are tight; harvest owner-correlated stakes | default | **arrange committed NAV facilities and repo while cheap** (option value) | allowed if DB-DCR passes with margin |
| SG | sell liquid and overvalued assets; exits still open, so accelerate continuation and secondary exits | hold privates | modest | no new structural leverage; draws rise for 1–3 years |
| DB | sell only liquid assets; avoid forced private sales | **hold privates**; slow pacing | draw pre-committed facilities only | only pre-arranged, cheap lines; monetise hedges first |
| SS | rebalance away from duration-dependent hedges | hold | normal | cautious: margin spikes |
| GW | check owner volumes and domestic exposures; sell owner-correlated liquid assets | hold | normal | limited: rising override risk |

### 6.11 Hedge design [I]

1. **Natural hedge first.** Underweight assets with negative $\beta^{own}$:
   - energy equity and credit;
   - GCC and EM oil-exporter assets;
   - domestic strategic stakes, if held and tradable.
   This is the cheapest liability hedge, and it follows peer precedent (Norway's E&P exclusion).
2. **Oil put spread struck at the kinks.**
   - Strikes: long $K_H$ (≈US$64), short $K_L$ (≈US$31), on Brent, or Murban for basis [U].
   - Size: hedge ratio 20–40% of the 266m-barrel equivalent. A full hedge would be on the order of Mexico's entire programme [I].
   - Tenor: 1–2 years, rolled. Long-dated oil options are thin.
   - **Timing:** today's oil vol (77% realised) makes this expensive. Prefer to stage purchases as vol normalises, or finance with short-dated call spreads.
   - **Warning:** in a GW state with UAE volume loss, sold calls lose exactly when owner needs rise. Cap call-selling tenor and size.
3. **Joint-state hybrids for DB.**
   - Instruments: oil-conditional equity puts, dual digitals, best-of puts. Optionally use proxies for "exits closed", such as listed alternative managers and HY CDX.
   - **Buy when priced oil–equity correlation is low** (now).
   - Monitor dealer correlation marks against the physical DB probability from the $Z_t$ posterior.
4. **Contingent liquidity.** Committed NAV facilities, secondary forward-sale options and repo lines (Stream 05). These are often cheaper per unit of DB-state cash than options.
5. **Avoid** relying on duration in SS and GW (2022; GFSR 2026). Use duration as a DB hedge only.
6. **Evaluation metric** (Borensztein–Jeanne–Sandri logic):
$$\text{Net value}_{yr}\approx\Delta L^{req}\,(\mu_{illiq}-r_{cash})-\text{Premium}+\mathbb E^P[\text{payoff}]-\text{margin cost},$$
   where $\Delta L^{req}$ is the reduction in the DCR-required buffer. With $\mu_{illiq}-r_{cash}\approx4$–6%, releasing US$5bn of buffer is worth ≈US$200–300m a year, or 11–17bp of NAV.

### 6.12 Calibration targets (the simulator must reproduce these)

| # | Target | Value | Source |
|---|---|---|---|
| 1 | ρ(oil, equity), monthly, by era | −0.14 / +0.43 / +0.32 | [I-calc] |
| 2 | Lower-tail dependence (q=10%) | 0.08 pre-2008; 0.30 post-2008 | [I-calc] |
| 3 | 12-month frequencies | P(oil ≤−30%) 11.7%; P(oil ≥+50%) 15.2%; P(eq ≤−10% given oil ≤−30%) 26% | [I-calc] |
| 4 | Shock-type shares of 12-month windows | N 60, B 18, SG 13.5, SS 5, DB 4% | [I-calc] |
| 5 | Longest low-price spell | 22 months (2014–16) | [I-calc] |
| 6 | Oil vol | calm 25%, turbulent 52%; 2026 realised 77% | [I-calc] |
| 7 | UAE fiscal swings | −8.1pp (2014→15); −4.9pp (2019→20); −2.4pp (2025→26, oil up) | [S] IMF DataMapper |
| 8 | UAE breakeven and $h$ path | 44.8–45.9 US$/bbl; 11.3% → 9.1% of GDP | [S] IMF Article IV 2025 |
| 9 | Brent path | 4Q26 US$105, 2027 US$84, 4Q27 US$74 (pre-war 2027: US$53) | [S] EIA STEO |
| 10 | Gulf shut-in path | 10.9 → 4.8 → 4.5 → 2.7 mb/d | [S] EIA STEO |
| 11 | PE distribution rate | ≈14% of NAV (2025) | [S] Bain 2026 |
| 12 | SWF redemption intensity in a bust | ≥US$46.5bn in 2015 (SAMA ≈US$70bn) | [S] |
| 13 | Hedge benchmark | 0.1% of GDP a year; payouts 0.3–0.6% of GDP; 19bp funding benefit | [S] IMF blog |

### 6.13 Data needs

**Client data:**
- ADIC draw history (amount, date, basis, notice period, in-kind?) and the legal text of the 5–10% rule;
- the owner's financing plan and debt issuance;
- domestic strategic holdings;
- overlay ISDA/CSA terms and counterparties, including whether any are GCC banks (WWR);
- PE cash flows by fund and vintage;
- facility terms.

**Market data:**
- Brent, WTI and Murban futures and options surfaces;
- dealer quotes for hybrids with correlation marks;
- HY energy spreads;
- listed-alternatives equity;
- secondary pricing.

**Official data:**
- IMF REO (due 22 Oct 2026; will update breakevens);
- IMF Article IV 2026;
- Abu Dhabi DoF releases;
- EIA STEO monthly;
- IEA WEO 2026 and NGFS for ET calibration.

**News flow:** OPEC+ decisions, Hormuz status, attacks on export infrastructure, ceasefire milestones.

### 6.14 Agentic components and IC artifacts [I]

The design maps onto the Sakana-style pipeline: idea → plan → sandboxed experiments → aggregation → baselines and ablations → analysis → report, run under a meta-controller with rubric verification at every stage.

| Agent | Role | Deterministic core | Rubric gate |
|---|---|---|---|
| **A1 Sovereign Liability** | extracts fiscal, volume and policy facts (IMF, EIA, ADNOC, budgets, news) into dated evidence cards | parsers, unit and vintage checks | every number has source, unit, as-of date and vintage. Flags conflicts, e.g. UAE quota 3.2 vs capacity figures, or pre-war vs post-war breakevens |
| **A2 Oil Shock-Type** | nowcasts $P(Z_t)$ | Ready-style daily decomposition, monthly BH-SVAR, HMM | disagreement alarm when structural, statistical and narrative labels diverge |
| **A3 Owner-Draw Simulator** | generates $D_t$ paths | the §6.5–6.6 equations | reproduces §6.12 targets; posterior predictive checks against observed draws |
| **A4 Hedge Designer** | proposes the liability hedge stack | CVaR LP over a payoff library; buffer-release metric | no proposal without basis-risk, margin and counterparty analysis |
| **A5 Red Team** | reverse stress: most plausible DCR breach | plausibility-constrained optimisation | must beat a "GW→SG→DB, exits shut, override" benchmark narrative |
| **A6 IC Elicitation and Deliberation** | SHELF forms for $P^{BE}$, $b$, $\omega$, $\rho$, override, GW persistence; captures IC views | entropy pooling reweights paths | records views, deltas and decisions for audit |

**Baselines and ablations to show the IC:**
- no hedge;
- equity-only hedge (which mis-targets SG and GW, Stream 09);
- oil-only hedge;
- hybrid stack;
- facility-only.

**IC artifacts:**
1. **Liability Weather Map:**
   - $Z_t$ posterior;
   - Brent against the published kinks;
   - $FB$ nowcast;
   - the $P^{BE}$ prior and its update;
   - a draw fan chart (P10/50/90, three years);
   - DCR under DB, GW and SG+PS.
2. **Joint-state coverage meter:** months of survival at cap draws with exits shut.
3. **Hedge menu:** cost, payoff by $Z$, buffer released, basis, margin.
4. **Views panel:** the IC sets P(SG in 2027–28), P(war persists) and $P^{BE}$. Entropy-pooled metrics update live.
5. **Owner-beta league table** for proposed actions.
6. **Reverse-stress narrative**, with an early-warning checklist:
   - Brent below $K_H$;
   - FB nowcast below +2pp;
   - Hormuz or Fujairah incidents;
   - OPEC+ market-share rhetoric;
   - secondary discounts widening;
   - AED forward points (PS).

---

## 7. Implementation notes

**Python stack.**
- numpy and scipy for vectorised Monte Carlo;
- statsmodels (`MarkovRegression`, VAR/SVAR) and arch (GARCH filters);
- hmmlearn, which needs restarts, `min_covar` and winsorisation (our unwinsorised 3-state fit degenerated);
- PyMC or NumPyro for the Bayesian SVAR, the hierarchical draw model and particle filters;
- PreliZ for prior elicitation [U];
- cvxpy for the CVaR LP and hedge selection;
- pyomo with mpi-sppy for multistage SP; SDDP via SDDP.jl through juliacall [U];
- QuantLib-Python for vanilla and Asian oil options; custom MC or Stulz (1982) closed forms for two-asset max/min options [U];
- SALib for Sobol sensitivity on ($P^{BE},b,\omega,\rho$);
- pandas for data.

**Complexity.**
- The ODE itself is $O(NT)$ and negligible.
- Hybrid valuation inside paths (nested) is the bottleneck. Options:
  - closed forms for two-asset options;
  - least-squares regression proxies;
  - a pre-computed price grid over (spot, vol, ρ, τ) with interpolation.
- SDDP with a Markov $Z_t$ needs cuts per Markov state. With 6 Z-states × 4 S-states = 24 nodes per stage, convergence over 40 quarterly stages is tractable with aggregated assets (Stream 01).

**Numerical pitfalls.**
1. **Clipping** is non-differentiable. Use a smooth clip, $\Pi_\tau(x)=d_{lo}+\tau\ln\frac{1+e^{(x-d_{lo})/\tau}}{1+e^{(x-d_{hi})/\tau}}$, for gradient-based policy search, or binaries in MILP.
2. **Overlapping windows** inflate apparent sample size. Report effective n.
3. **Spot vs futures.** Physical (Dated) Brent spot reached US$135.51 on 2 Oct 2026. In physical squeezes spot can diverge from futures, while hedges settle on futures or averages, so model the basis. We did not check futures prices in-session.
4. **Monthly averages vs month-end.** EIA monthly averages smooth returns and bias correlations. Use month-end from daily data.
5. **Measures.** Price under Q, simulate under P. Never use Q-probabilities as event probabilities without a risk-premium adjustment.
6. **Data vintages.** Pre-war IMF breakevens are a different object from post-war ones. Store every parameter with a vintage tag.
7. **Time consistency.** Chance constraints per stage are not time-consistent. Use nested CVaR or a rolling MPC with fixed tube parameters (Stream 01).
8. **Units.** Draws are % of NAV and fiscal figures are % of GDP; enforce the conversion explicitly.

---

## 8. Risks, pitfalls and limitations

**Data and calibration**
- **No ADIC draw data in hand.** Every owner parameter is a prior. The breakeven uncertainty dominates the results (§6.6).
- **Small joint-tail samples.** There are about four DB episodes in 38 years. Priors and peer pooling carry real weight, and the IC should see wide bands.

**Model specification**
- **Shock-type misclassification.** Sign rules mislabel 2020 and 2026. Structural identification is revised ex post, and narrative flags need governance.
- **Structural breaks** shift every elasticity:
  - the UAE's OPEC exit;
  - a declining hydrocarbon share;
  - possible persistent Hormuz tolling or insecurity;
  - the transition.

**Owner and governance**
- **Political override and legal plumbing.** Kuwait and Alaska show band rules can change. Draws above 10% have non-zero probability.
- **Sovereign coordination.** The IMF urges fiscal coordination across GREs and SWFs. ADIC hedging oil may duplicate or offset hedges elsewhere on the sovereign balance sheet. Owner-level optics of a fund "shorting oil" need IC and owner alignment.

**Hedging and counterparties**
- **Hedge model risk:**
  - correlation skew;
  - liquidity of long-dated oil options;
  - Murban–Brent basis;
  - margin procyclicality;
  - counterparty WWR if dealers or collateral are GCC-linked.
- **Leveraged hedge-fund sleeve.** The publicly reported plan for leveraged HF strategies [S] would add gate risk exactly in DB states. Treat it with heavy haircuts in the DCR.

**Scope**
- Abu Dhabi-specific fiscal data are sparse in public sources. We rely on consolidated UAE figures.

---

## 9. Open questions (for ADIC)

1. **The rule itself.** What is the exact distribution rule (opening NAV or trailing average)? Who sets the rate within the band, and on what notice? Are in-kind or AED payments possible? Can the 10% cap be exceeded?
2. **History.** What are ADIC's annual draws for 2015–2026? These would directly calibrate $b$, $\rho$ and $\omega$ against IMF fiscal history.
3. **Financing hierarchy.** Where does ADIC rank against ADIA, Mubadala, L'imad and debt issuance? Is it called early (more liquid) or late?
4. **Breakeven.** Which effective breakeven governs the owner's calls (Abu Dhabi-specific, including off-budget GRE and SWF capex)? Does the owner publish or share one?
5. **Domestic exposures.** Does ADIC still hold domestic strategic stakes (e.g. banks)? Are they saleable in stress?
6. **Mandate.** May the overlay trade oil options and hybrids? Are there policy constraints on short-oil positions?
7. **Counterparties.** What are the overlay CSA terms, eligible collateral and counterparty mix (GCC banks)?
8. **Committed liquidity.** Can ADIC put in place committed NAV facilities, repo, or sovereign-backed lines?
9. **HF liquidity.** What liquidity and gate terms apply to the reported leveraged hedge-fund programme in a DB state?
10. **Risk appetite.** What is the IC's tolerance for an owner shortfall: zero, or a stated probability? This sets $\lambda_{sh}$ and the DCR threshold.
11. **Owner-level hedging.** Is there appetite to coordinate a sovereign-level oil hedge, Mexico-style, rather than ADIC-level hedging?

---

## 10. References

**Theory and methods**
1. Gintschel, A. & Scherer, B. (2008). Optimal asset allocation for sovereign wealth funds. *Journal of Asset Management* 9, 215–238. Citation verified via the reference list of item 6.
2. Scherer, B. (2009). A note on portfolio choice for sovereign wealth funds. *Financial Markets and Portfolio Management* 23, 315–327. Verified via item 6.
3. Scherer, B. (2011). Portfolio choice for oil-based sovereign wealth funds. *Journal of Alternative Investments* 13(3), 24–34 (Winter 2011 issue; Crossref dates it 31 Dec 2010). https://doi.org/10.3905/jai.2011.13.3.024. EDHEC WP (Oct 2009): https://climateinstitute.edhec.edu/publications/portfolio-choice-oil-based-sovereign-wealth-funds
4. van den Bremer, T., van der Ploeg, F. & Wills, S. (2016). The elephant in the ground: managing oil and sovereign wealth. *European Economic Review* 82, 113–131. CEPR DP10188: https://ideas.repec.org/p/cpr/ceprdp/10188.html
5. Bodie, Z. & Brière, M. (2014). Sovereign wealth and risk management: a framework for optimal asset allocation of sovereign wealth. *Journal of Investment Management* 12(1). https://joim.com/?p=1220 ; Amundi WP-011-2011 (rev. 2013): https://research-center.amundi.com/files/nuxeo/dl/1ff3c6f5-2e14-4633-a55a-5379b02dc112
6. Moutanabbir, K. & Noureldin, D. (2020). Optimal asset allocation and consumption rules for commodity-based sovereign wealth funds. *International Review of Economics & Finance* 69, 708–730. https://doi.org/10.1016/j.iref.2020.06.014. Working-paper version: ERF WP 1172 (Feb 2018), https://erf.org.eg/app/uploads/2018/03/1172_Final.pdf; the §2.2 figures were verified against the WP only.
7. Balding, C. & Yao, Y. (2011). Portfolio allocation for sovereign wealth funds in the shadow of commodity-based national wealth. *International Finance Review* 12, 293–312. Verified via item 6.
8. Lessmann, Tahri & Yanovski (2024). Portfolio allocation bias of oil-based sovereign wealth funds. *Strategic Behavior and the Environment* 10(1–2). https://nowpublishers.com/article/Details/SBE-109 (abstract only)
9. Das, U.S., Lu, Y., Mulder, C. & Sy, A. (2009). Setting up a sovereign wealth fund: some policy and operational considerations. IMF WP/09/179. https://www.imf.org/en/Publications/WP/Issues/2016/12/31/Setting-Up-a-Sovereign-Wealth-Fund-Some-Policy-and-Operational-Considerations-23205
10. IMF (2014). *Sovereign Asset-Liability Management—Guidance for Resource-Rich Economies*. Policy Paper, 11 Jun 2014. https://www.imf.org/en/publications/policy-papers/issues/2016/12/31/sovereign-asset-liability-management-guidance-for-resource-rich-economies-pp4876
11. Merton, R.C. (1993). Optimal investment strategies for university endowment funds. In Clotfelter & Rothschild (eds), *Studies of Supply and Demand in Higher Education*, ch. 7, pp. 211–242 (one listing gives 211–236). U. Chicago Press. NBER chapter c6102: https://www.nber.org/books-and-chapters/studies-supply-and-demand-higher-education/optimal-investment-strategies-university-endowment-funds. Preceded by NBER WP 3820 (Aug 1991).
12. Brown, J.R., Dimmock, S.G., Kang, J.-K. & Weisbenner, S.J. (2014). How university endowments respond to financial market shocks. *AER* 104(3), 931–62. https://www.aeaweb.org/articles?id=10.1257/aer.104.3.931
13. Kilian, L. (2009). Not all oil price shocks are alike. *AER* 99(3), 1053–69. https://www.aeaweb.org/articles?id=10.1257/aer.99.3.1053
14. Baumeister, C. & Hamilton, J.D. (2019). Structural interpretation of vector autoregressions with incomplete identification: revisiting the role of oil supply and demand shocks. *AER* 109(5), 1873–1910. https://www.aeaweb.org/articles?id=10.1257/aer.20151569
15. Känzig, D.R. (2021). The macroeconomic effects of oil supply news: evidence from OPEC announcements. *AER* 111(4), 1092–1125. https://www.aeaweb.org/articles?id=10.1257/aer.20190964
16. Ready, R.C. (2018). Oil prices and the stock market. *Review of Finance* 22(1), 155–176. https://doi.org/10.1093/rof/rfw071 (DOI resolves to academic.oup.com)
17. Robinson, D.T. & Sensoy, B.A. (2016). Cyclicality, performance measurement, and cash flow liquidity in private equity. *JFE* 122(3). https://doi.org/10.1016/j.jfineco.2016.09.008 (DOI resolves to the Elsevier JFE record)
18. Bernanke, B.S. (2016). The relationship between stocks and oil prices. Brookings, 19 Feb 2016. https://www.brookings.edu/articles/the-relationship-between-stocks-and-oil-prices/
19. Borensztein, E., Jeanne, O. & Sandri, D. (2009). Macro-hedging for commodity exporters. IMF WP/09/229. https://www.imf.org/external/pubs/ft/wp/2009/wp09229.pdf. The *J. Development Economics* (2013) version is [U].
20. Valencia, F. (2018). To hedge or to self-insure? The benefits of Mexico's oil hedging program. IMF Blog (Diálogo a fondo), Mar 2018. https://www.imf.org/external/np/blog/dialogo/032618.pdf. Academic companion: Ma, C. & Valencia, F. (2018). Welfare gains from market insurance: the case of Mexican oil price risk. IMF WP/18/35. https://doi.org/10.5089/9781484344163.001. The §4.8 figures were verified against the blog and were not checked in the WP.
21. Erbil, N. (2011). Is fiscal policy procyclical in developing oil-producing countries? IMF WP/11/171. https://www.imf.org/external/pubs/ft/wp/2011/wp11171.pdf
22. Standard citations. Those marked (verified) were confirmed by the literature review (`research/literature/03_sovereign_alm.lit.md` §2) or the topic-10 re-check (`research/literature/recheck/10_scenarios_robustness.recheck.md`); those marked [U] remain unverified:
    - Hamilton (1989) *Econometrica* 57(2), 357–384, DOI 10.2307/1912559 (verified);
    - Schwartz & Smith (2000) *Mgmt Sci* 46(7), DOI 10.1287/mnsc.46.7.893.12034 (verified);
    - Stulz (1982) *JFE* 10(2), DOI 10.1016/0304-405X(82)90011-3 (verified);
    - Rockafellar & Uryasev (2000) *J. Risk* 2(3), 21–41, DOI 10.21314/JOR.2000.038 (verified);
    - Meucci (2008) "Fully flexible views: theory and practice", *Risk* 21(10), 97–102; preprint arXiv:1012.2848, whose journal reference gives this venue (verified);
    - Breuer, Jandačka, Rheinberger & Summer (2009) *IJCB* 5(3), Sept 2009 (verified on the ijcb.org issue page);
    - Kilian & Park (2009) *IER* 50(4), DOI 10.1111/j.1468-2354.2009.00568.x (verified);
    - Dybvig (1999) "Using asset allocation to protect spending", *FAJ* 55(1), DOI 10.2469/faj.v55.n1.2241 (verified);
    - O'Hagan, Buck, Daneshkhah, Eiser, Garthwaite, Jenkinson, Oakley & Rakow (2006) *Uncertain Judgements: Eliciting Experts' Probabilities*, Wiley, DOI 10.1002/0470033312 (verified);
    - [U] Tobin (1974) *AER* 64(2);
    - [U] Dybvig (1995) *RES* 62(2);
    - [U] Pereira & Pinto (1991) *Math. Prog.* 52 (the original was not found; Rebennack (2015, *Mathematical Programming*) attributes SDDP to it);
    - [U] Cooke (1991) *Experts in Uncertainty*;
    - [U] Gray, Merton & Bodie (2007) *JOIM* 5(4) (only the companion 2006 NBER WP, "A New Framework for Analyzing and Managing Macrofinancial Risks of an Economy", DOI 10.2139/ssrn.936661, was found);
    - [U] Ang, Goetzmann & Schaefer (2009), Norway active-management review;
    - [U] BCBS (2013) LCR.

**Official data and reports**

23. IMF (2025). *United Arab Emirates: 2025 Article IV Consultation* (Country Report, 8 Dec 2025), Table 3a. https://www.imf.org/en/publications/cr/issues/2025/12/08/united-arab-emirates-2025-article-iv-consultation-press-release-staff-report-and-statement-572397
24. IMF (2026). *Kuwait: 2025 Article IV Consultation* (24 Feb 2026). https://www.imf.org/en/publications/cr/issues/2026/02/24/kuwait-2025-article-iv-consultation-press-release-and-staff-report-574216
25. IMF DataMapper API, accessed 18 Oct 2026: https://www.imf.org/external/datamapper/api/v1/GGXCNL_NGDP/ARE ; …/GGXCNL_NGDP/SAU ; …/GGXCNL_NGDP/KWT ; …/NGDP_RPCH/ARE ; …/NGDPD/ARE
26. IMF (2026). *World Economic Outlook*, Oct 2026 (13 Oct). https://www.imf.org/en/publications/weo/issues/2026/10/13/world-economic-outlook-october-2026 ; *GFSR*, Apr 2026: https://www.imf.org/en/publications/gfsr/issues/2026/04/14/global-financial-stability-report-april-2026
27. Mirzoev, T. et al. (2020). *The Future of Oil and Fiscal Sustainability in the GCC Region*. IMF Departmental Paper, 6 Feb 2020. https://www.imf.org/en/Publications/Departmental-Papers-Policy-Papers/Issues/2020/01/31/The-Future-of-Oil-and-Fiscal-Sustainability-in-the-GCC-Region-48934
28. EIA. *Short-Term Energy Outlook*, Feb, Mar, May, Jun, Sep and Oct 2026. https://www.eia.gov/outlooks/steo/ ; archives, e.g. https://www.eia.gov/outlooks/steo/archives/may26.pdf and https://www.eia.gov/outlooks/steo/archives/jun26.pdf
29. EIA. Europe Brent spot price FOB (RBRTE), daily. https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=D
30. EIA (2025). Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint. *Today in Energy*, 16 Jun 2025. https://www.eia.gov/todayinenergy/detail.php?id=65504
31. Kenneth R. French Data Library (US and developed-market factors, through Aug 2026). https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html ; CBOE VIX history: https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv
32. NBIM. The fund's market value and capital flows. https://www.nbim.no/en/the-fund/market-value/

**Practitioner and press**

33. Bain & Company (2026). *Global Private Equity Report 2026*, "The industry gains traction". https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/
34. Al Jazeera (29 Apr 2026). UAE quits OPEC: what that means for the Gulf, energy markets and beyond. https://www.aljazeera.com/news/2026/4/29/uae-quits-opec-what-that-means-for-the-gulf-energy-markets-and-beyond
35. Al Jazeera (13 Oct 2026). Middle East and Central Asia's economy to shrink in 2026 amid war, IMF says. https://www.aljazeera.com/economy/2026/10/13/middle-east-and-central-asias-economy-to-shrink-in-2026-amid-war-imf-says
36. Gulf News / FTfm. Sovereign wealth funds pull at least $46.5b from asset managers (2015 data). https://gulfnews.com/business/markets/sovereign-wealth-funds-pull-at-least-465b-from-asset-managers-1.1677026
37. IR Impact (7 Dec 2015). Gulf governments pull cash from SWFs at record pace. http://www.ir-impact.com/2015/12/gulf-governments-pull-cash-swfs-record-pace/
38. Bloomberg (24 Nov 2015). Mexico reaps record $6.4 billion in oil hedge win. https://www.bloomberg.com/news/articles/2015-11-24/mexico-reaps-record-6-4-billion-in-oil-hedge-win-minister-says (search snippet; paywalled)
39. The National (21 Mar 2018). Abu Dhabi Investment Council to join forces with Mubadala. https://www.thenationalnews.com/business/abu-dhabi-investment-council-to-join-forces-with-mubadala-1.714997
40. Wikipedia, "Abu Dhabi Investment Council" (last edited 15 Jun 2026; cites WAM 21 Mar 2018 and the Official Gazette 30 Apr 2018). https://en.wikipedia.org/wiki/Abu_Dhabi_Investment_Council
41. Bloomberg (4 Feb 2026). $160 Billion Abu Dhabi Fund Eyes Bolder Bets for 10% Returns. https://www.bloomberg.com/news/articles/2026-02-04/abu-dhabi-s-160-billion-endowment-style-fund-eyes-bolder-bets (headline and snippet only)
42. Jawlah (11 Jun 2026). ADIC-led plan for up to $15bn in leveraged hedge fund strategies. https://jawlah.co/en/58501
43. Circuit (30 Jan 2026). Abu Dhabi moves ADQ assets under L'imad. https://circuit.news/2026/01/30/abu-dhabi-moves-adq-assets-under-limad-in-major-overhaul-of-wealth-funds/ ; AsiaAsset, L'imad to take over US$263bn ADQ: https://www.asiaasset.com/sovereign-wealth-funds/abu-dhabis-newly-minted-wealth-fund-limad-to-take-over-us263-billion-peer-adq/ (snippet)
44. Wikipedia, "Saudi Central Bank" (SAMA→PIF US$40bn, 2020; cites SWFI https://www.swfinstitute.org/news/79948/sama-had-transferred-40-billion-to-pif-more-firepower-for-market-opportunities). https://en.wikipedia.org/wiki/Saudi_Central_Bank ; "Public Investment Fund": https://en.wikipedia.org/wiki/Public_Investment_Fund
45. Wikipedia, "Government Pension Fund of Norway" (first withdrawal 2016, citing Reuters 3 Mar 2016; E&P proposal of 8 Mar 2019 citing the Ministry of Finance white paper). https://en.wikipedia.org/wiki/Government_Pension_Fund_of_Norway
46. Wikipedia, "Alaska Permanent Fund" (POMV, SB 26; ANS prices). https://en.wikipedia.org/wiki/Alaska_Permanent_Fund
47. Wikipedia, "Mubadala Investment Company". https://en.wikipedia.org/wiki/Mubadala_Investment_Company

*Cross-links:*
- Stream 01: MPO, shadow prices, MPC.
- Stream 02: distribution rules, Kuwait 2020, Alaska.
- Stream 05: secondaries and NAV finance.
- Stream 06: leverage.
- Stream 08: action valuation.
- Stream 09: overlay, margin, hybrids.
- Stream 10: scenario generator, entropy pooling, reverse stress.
- Stream 11: objectives.
- Stream 12: agentic architecture.
- Stream 14: IC deliberation.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2, `research/literature/03_sovereign_alm.lit.md` §2 and `research/literature/recheck/10_scenarios_robustness.recheck.md`. Added metadata was confirmed via Crossref, OpenAlex, RePEc, arXiv or the NBER chapter PDF, as noted. No BGK barrier statistic, §2.6 cross-file inconsistency or other re-checked work appears in this dossier.

- §2.2, §10 item 6 (Moutanabbir & Noureldin): ERF WP 1172 (2018) → published version (2020), *IREF* 69:708–730, DOI 10.1016/j.iref.2020.06.014 (Crossref, RePEc). The WP is kept as the source of the figures. The re-check against the journal version could not be done (its abstract gives no figures; ScienceDirect returned 403), so an [unverified] note was added.
- §10 item 11 (Merton 1993): added ch. 7, pp. 211–242 (NBER chapter PDF cover page; one listing gives 211–236), NBER chapter c6102 and the precursor NBER WP 3820 (Aug 1991).
- §10 item 3 (Scherer 2011): added issue 13(3) and DOI 10.3905/jai.2011.13.3.024 (Crossref date 31 Dec 2010, the Winter 2011 issue).
- §10 item 14 (Baumeister & Hamilton 2019): restored the subtitle ": revisiting the role of oil supply and demand shocks" (Crossref).
- §10 item 15 (Känzig 2021): restored the subtitle ": evidence from OPEC announcements" (Crossref).
- §2.4, §10 item 16 (Ready 2018): pages 155– → 155–176 (Crossref).
- §4.8, §10 item 20 (Valencia 2018 blog): added the academic companion Ma, C. & Valencia, F. (2018), IMF WP/18/35, DOI 10.5089/9781484344163.001 (Crossref). The blog remains the source of the §4.8 figures, which were verified against it and not checked in the WP.
- §10 item 22: split into verified works and works still [U] (details in the lines below).
- §3.1, §10 item 22 (Hamilton 1989): [U] → [S]; added pp. 357–384 and DOI 10.2307/1912559 (lit review #21; topic-10 re-check #18).
- §3.1, §10 item 22 (Schwartz & Smith 2000): [U] → [S]; added DOI 10.1287/mnsc.46.7.893.12034 (lit review #20).
- §3.3, §10 item 22 (Meucci 2008): [U] → [S]; added the title, pp. 97–102 and preprint arXiv:1012.2848, whose journal reference gives *Risk* 21(10) 97–102 (lit review #23; arXiv).
- §3.3, §10 item 22 (Breuer, Jandačka, Rheinberger & Summer 2009): [U] → [S]; *IJCB* 5(3), Sept 2009 confirmed on ijcb.org (lit review #24).
- §3.4, §10 item 22 (Rockafellar & Uryasev 2000): [U] → [S]; added pp. 21–41 and DOI 10.21314/JOR.2000.038 (lit review #22; topic-10 re-check #34).
- §3.4, §10 item 22 (Stulz 1982): [U] → [S]; added DOI 10.1016/0304-405X(82)90011-3 (lit review #25). The [U] at the end of the §7 QuantLib/Stulz bullet was left, because it may mark the tool claim rather than the citation.
- §10 item 22 (Kilian & Park 2009): [U] → verified; added DOI 10.1111/j.1468-2354.2009.00568.x (lit review #19).
- §10 item 22 (Dybvig 1999): [U] → verified; added the title and DOI 10.2469/faj.v55.n1.2241 (lit review, additional checks).
- §10 item 22 (O'Hagan et al. 2006): [U] → verified; added the full author list, subtitle and DOI 10.1002/0470033312 (topic-10 re-check #29).
- §10 item 22 (Gray, Merton & Bodie 2007; Pereira & Pinto 1991): kept [U]; noted the companion 2006 NBER WP and Rebennack's (2015) attribution (lit review, additional checks).
