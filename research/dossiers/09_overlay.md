# Stream 09: Derivatives overlay (tail protection, opportunistic trading, collateral and margin liquidity)

*ADIC multi-period robust TPA framework. Dossier prepared 2026-10-18.*

**Evidence labels.** **[S]** = sourced fact with citation. **[C]** = practitioner consensus. **[I]** = our inference or design proposal. **[nrv]** = classic reference cited from memory and *not re-verified in this session*; these carry no URL.

**Data note.** We computed market statistics from Cboe's published daily index files (VIX, VIX3M, VVIX, SKEW, SPX, PPUT, CLL, CLLZ, VXTH). The files were downloaded on 2026-10-18; the last observation is 2026-10-16. They are labelled "Cboe data". All SPX figures use the **price** index. The Cboe strategy indices are total-return. To compare them with S&P 500 total return we add an assumed 1.5–2.5% p.a. dividend yield, and we report the sensitivity.

**Process note.** The session's shared web-search quota ran out early. After that, evidence came from fetching primary documents directly (BIS/FSB/BoE/IMF/NBER/arXiv/Cboe/US rule text).

---

## 1. Executive summary

1. **The overlay is ADIC's fast actuator, and its binding currency is liquidity.**
   - About 60% of NAV sits in slow, stale-marked private assets, and the fund must distribute 5–10% a year. The overlay (synthetic beta, tail hedge, opportunistic book) is the only lever that can change total exposure and contingent liquidity within days.
   - Every derivative therefore enters the model twice: as P&L, and as a state-contingent stream of premium, variation margin (VM), initial margin (IM) and financing cash flows in the liquidity ledger.
   - The prior deck's single "P99 overlay margin" scalar should be replaced by a full VM/IM distribution conditioned on regime.

2. **On its own, tail protection reliably loses money.**
   - One-month at-the-money (ATM) S&P 500 puts returned **−7.4% p.a.** in excess of cash over 1985–2018, even though they paid off in all eight major drawdowns [S: Harvey et al. 2019].
   - Cboe PPUT (S&P 500 plus monthly 5% out-of-the-money (OTM) puts) compounded **7.97%** p.a. from 30 Jun 1986 to 16 Oct 2026. That is about **2.3–3.3 pp p.a. behind** S&P 500 total return, depending on the dividend assumption [Cboe data].
   - Implied minus subsequent realized volatility (VIX minus 21-day realized) averaged **4.1 vol points** and was positive on **86%** of days over 1990–2026 [Cboe data].
   - Sized for equal expected return, divesting beats puts on drawdown, volatility and Sharpe ratio [S: Israelov 2019].

3. **ADIC's case for protection rests on three non-alpha channels.**
   - The channels are: (i) state-contingent liquidity; (ii) **enabling value**, meaning it relaxes the Tier-1 floor and liquidity constraints so that more beta or illiquidity can be held elsewhere; (iii) rebalancing capital.
   - Formally, a hedge with premium $P_0$ and payoff $X_s$ is worth holding if $\mathbb E^P[(1+\lambda_s)X_s] + \text{enabling} + \text{rebalancing} \ge P_0(1+r)$, where $\lambda_s$ is the liquidity shadow price in state $s$.
   - Crisis λ is large. The average secondary-market discount to NAV was about **35%** in 2009, against about **13%** in 2025 (LP portfolios at 87% of NAV) [S, via Wikipedia citing WSJ/Jefferies].
   - Investors would give up about **2% of wealth** to hedge once-a-decade illiquidity crises [S: Ang, Papanikolaou & Westerfield 2014].

4. **Choose instruments by *cost per unit of crisis payoff*, and diversify across crisis types.**
   - Our Cboe-based estimates, in $ of expected carry per year per $ of average crisis-window payoff, are:
     - monthly 5% OTM puts ≈ **0.29**;
     - zero-cost put-spread collar ≈ **0.49**;
     - 95/110 collar ≈ **0.58**;
     - VIX-call tail overlay (VXTH) ≈ **0.09**, but ≈0.30 excluding COVID.
   - Hedges are crisis-type specific. VXTH returned **+27.6%** while the S&P 500 fell **−33.9%** (Feb–Mar 2020), but **−29.2% vs −25.4%** in 2022.
   - 1–3-month trend following performed well in the 1985–2018 drawdowns at 0.6–0.8% p.a. trading cost [S: Harvey et al.].
   - **Recommendation [I]:** build a *defensive stack*:
     - a state-conditioned dynamic beta overlay plus trend as the core;
     - a small convex sleeve (put spreads and VIX calls bought when the variance risk premium (VRP) and skew are cheap, laddered, with pre-agreed monetization rules);
     - CDX protection against private-credit marks;
     - duration only when the stock–bond correlation regime supports it.

5. **In a crisis, collateral is the binding constraint.**
   - March 2020 [S: FSB 2020]:
     - same-day VM calls dwarfed the incremental IM demand;
     - IM at some CCPs rose **>100%** against the prior quarter;
     - anti-procyclicality tools delayed IM increases by only a few days.
   - Sept–Oct 2022:
     - the 30-year gilt yield rose **>270 bp** (1 Aug to 14 Oct) to above 5%, "more than twice" the March 2020 move;
     - the Bank of England bought £19.3bn of gilts;
     - the FPC now requires LDI resilience to "around 250 basis points, at a minimum" [S: BoE].
   - **ADIC needs** a VM/IM stress engine (99%/ES plus a Basel-style historical look-back), a pre-positioned collateral pool and deliberate CSA and venue design.
   - Whether ADIC is a "sovereign entity" (excluded from the US "financial end user" definition) decides whether two-way regulatory IM applies [S: 12 CFR 237.2].

6. **Opportunistic book.**
   - Treat a live Sharpe of ≤0.5 as the prior. Backtest Sharpe ratios of 1–1.5 (diversified carry 1.49; diversified time-series momentum (TSMOM) >1) [S] must be deflated.
   - Harvey–Liu haircuts usually exceed 50% when SR < 0.4, and are at most 25% when SR > 1 [S].
   - Simulate funding-liquidity and crowding crashes and their crisis correlation.
   - Rank strategies by **liquidity-adjusted return** $\mathbb E[(1+\lambda_s) r^O_s]$, not by raw Sharpe.

7. **Conditions as of 16 Oct 2026 [Cboe data].**
   - S&P 500 at **7,659**, 2% below its 6 Oct 2026 record close.
   - VIX **19.99** (intraday 22.31).
   - Our 4-state VIX HMM puts **0.64 / 0.36** probability on the "normal" and "elevated" states.
   - SKEW **168.6**, against a long-run mean of 123.3 and a record of 183.1 on 18 Feb 2025. Downside wings are rich relative to ATM. This favours put spreads (which *sell* the rich wing), trend and CDX over outright deep-OTM puts right now.

8. **§6 delivers the build specification:**
   - state and decision variables, constraints, and objective terms with shadow prices;
   - default parameters and calibration targets, including a 4-state HMM fitted to 1990–2026;
   - simulation-ready equations for tail-hedge P&L and collateral, opportunistic returns and margin, synthetic beta financing and VM, and a recourse LP that produces λ path by path.

---

## 2. Core concepts and theory

### 2.1 Three roles, one currency

The overlay plays three roles:

- **exposure management**: synthetic beta, completion, and rebalancing while private NAVs are stale;
- **insurance**: tail protection;
- **return generation**: opportunistic trading.

Each role generates P&L, financing cost, VM, IM or independent amounts, counterparty exposure and operational load. These interact with distributions $D_t$, capital calls $K_t$ and PE distributions received $P_t$ through one constraint, the liquidity ledger. The overlay is therefore best seen as a **control input to a liquidity-constrained dynamic system**, not as three separate return streams [I].

### 2.2 Why negative-EV insurance can be optimal

| Discipline | Result | Transfer to ADIC |
|---|---|---|
| **Corporate finance** | Froot, Scharfstein & Stein (1993) [S]: hedging adds value when external finance costs more than internal funds, because it keeps internal funds available for good investments. | ADIC's crisis "external finance" is selling PE in secondaries at a discount, dumping liquid assets near troughs, drawing expensive lines, or deferring a sovereign distribution. |
| **Corporate finance** | Bolton, Chen & Wang (2011) [S]: optimal cash policy is a double barrier. Cash, hedging, asset sales and credit lines are substitutes. The value of liquidity rises as cash falls. | Same substitution set applies to ADIC's buffer, hedges, secondary sales and facilities. |
| **Corporate finance** | Rampini & Viswanathan (2010) and Rampini, Sufi & Viswanathan (2014) [nrv]: hedging competes with investment for scarce collateral, so constrained firms hedge less. | Premiums and posted IM consume the same high-quality liquid assets (HQLA) that fund capital calls. Insure while liquidity is plentiful, and **precommit**. |
| **Portfolio choice** | Ang, Papanikolaou & Westerfield (2014) [S]: illiquidity of uncertain duration raises effective risk aversion. Investors would give up about 2% of wealth to hedge crises that occur once every ten years. | Supports valuing protection against illiquidity crises. |
| **Portfolio choice** | Dimmock, Wang & Yang (2024) [S]: lock-ups plus secondary-sale costs produce time-varying rebalancing boundaries. Crisis illiquidity pushes holdings well away from targets. | This is the denominator effect the overlay must offset. |
| **Goal-based investing** | Browne (1999) [nrv]: maximizing the probability of reaching a goal by a deadline produces a *digital-option-like* terminal payoff. | ADIC's Tier-2 objective, P(5-yr return ≥ 10%) subject to a 7% robust floor, is a threshold objective. Its optimal payoff is non-linear, so options are natural instruments for *shaping the distribution*, not merely for insurance [I]. |

**Valuation identity (linearized Lagrangian) [I].**

Let ADIC solve $\max \mathbb E[U(W_T)]$ subject to:

- per-state liquidity constraints with multipliers $\mu_{t,s}$;
- the Tier-1 floor constraint with multiplier $\eta$.

Write $\lambda_{t,s}=\mu_{t,s}/\mathbb E[U']$ for the scaled multipliers. Adding a marginal hedge with premium $P_0$ and payoffs $X_{t,s}$ (counting VM inflows) changes the objective by:

$$
\Delta\mathcal L \approx \underbrace{\mathbb E^P[m_tX_t]-P_0}_{\text{carry / VRP}\,<\,0}\;+\;\underbrace{\mathbb E^P[\lambda_tX_t]}_{\text{liquidity}}\;+\;\underbrace{\eta\,(-\Delta \Pr\{\text{floor breach}\})}_{\text{enabling}}\;+\;\underbrace{\mathbb E^P[X_t\,\Delta\alpha^{reb}_t]}_{\text{rebalancing}}
$$

The hedge is worth holding when $\mathrm{Cov}(\lambda,X)+\mathbb E[\lambda]\mathbb E[X]+\text{enabling}+\text{rebalancing}\ \ge\ P_0-\mathbb E[mX]$.

The covariance term is the whole story. A hedge that pays in an equity-only crash while PE distributions continue and the owner's fiscal position is strong earns little λ. A hedge that pays in a joint "markets down, DPI zero, margin up, fiscal draw up" state can justify substantial carry.

**Worked example [I], illustrative round numbers.**

- **Set-up:**
  - expected carry 0.25% NAV/yr;
  - cost per unit crisis payoff $c=0.2$, so the crisis payoff is 1.25% NAV;
  - crisis probability $\pi=10\%$/yr;
  - $\lambda_{crisis}=0.5$ (equivalent to selling PE at a 33% discount, since $d/(1-d)=0.5$).
- **Value by channel:**
  - liquidity value ≈ $0.1\times0.5\times1.25\%$ = 0.06% NAV/yr;
  - enabling value: if the payoff permits +3% NAV more equity beta at the same breach probability with a 4% equity risk premium (ERP), 0.12%;
  - rebalancing value: reinvesting at a +15 pp post-crisis excess return, about 0.02%.
- **Result:** the total of about 0.20% is *below* the 0.25% carry, so the hedge is marginal.
- **Sensitivity:** at VXTH-like efficiency ($c\approx0.09$) the same budget buys a crisis payoff of about 2.8% NAV, and the total rises to about 0.45%. The answer turns on instrument efficiency and timing, which is why §4.3 matters.

### 2.3 A transferable buffer formula from international-reserves economics

**The model [S].** Jeanne & Rancière (IMF WP/06/229; published as Jeanne & Rancière 2011, *Economic Journal* 121(555)) model a country holding reserves at carry cost δ (a term premium) against a sudden stop. The parameters are:

- the sudden stop occurs with annual probability π;
- it removes short-term financing λ and causes an output loss γ (both as fractions of GDP);
- utility is constant relative risk aversion (CRRA) with coefficient σ.

At the optimum, the crisis-to-normal marginal-utility ratio is

$$p=\frac{u'(C^d)}{u'(C^b)}=1+\frac{\delta}{\pi(1-\delta-\pi)},$$

and optimal reserves as a share of output are approximately

$$\rho\approx\lambda+\gamma-\left(1-p^{-1/\sigma}\right).$$

In the working paper, the benchmark π=0.1, δ=1.5%, σ=2, λ≈11%, γ=6.5% gives **10.1% of GDP**. The published 2011 version reports a benchmark optimum of **9.1% of output** [unverified: figure as reported by Mihailov & Nasir (2022); the *Economic Journal* text was not accessed] [corrected 2026-10-18: only the working-paper figure was given].

**Mapping to ADIC [I].**

- *Sudden stop* = the joint state {DPI collapse, secondary discounts widen, VM and IM spike, distributions unchanged or rising}.
- λ = 12-month net liquidity gap in that state (% NAV).
- γ = deadweight loss from forced sales and forgone opportunities.
- δ = carry per unit of crisis liquidity of the insurance instrument.
- σ = curvature of the IC's penalty for crisis shortfalls.

**Illustration.**

- With π=0.10, λ+γ=15% NAV and σ=2:
  - δ=1.5% gives about 7.5% NAV of crisis liquidity;
  - δ=5% gives $1-p^{-1/2}\approx0.21$, a **corner solution in which you do not insure with that instrument**;
  - raising σ to 5 restores about 6% NAV.
- **Lesson for the IC:** whether to insure at all depends on the instrument's carry relative to crisis probability *and* on the curvature of the IC's penalty. That curvature is a governance parameter the IC must own.
- **Caveat:** this is a one-shot CRRA model. Use it for intuition only; sizing should come from the multi-period simulation.

### 2.4 Option-market structure that matters for hedging

- **VRP.** Index options carry a variance risk premium (Carr & Wu 2009 [nrv]). The VRP predicts equity returns, most strongly at roughly quarterly horizons (Bollerslev, Tauchen & Zhou 2009; paper retrieved, horizon detail [nrv]).
  - Israelov & Nielsen (2015) [S] show it is the VRP, not the VIX level, that makes protection cheap or dear. They report the realized VRP was positive in every VIX decile, per a secondary summary.
  - Our data show mean VRP of 2.8 vol points when VIX < 15, rising to 6.5 at VIX 30–40 (§4.4). Protection is least expensive in VRP terms when VIX is low, but it is never free.
- **Skew.** Downside strikes trade at higher implied vol. The SKEW index is currently very high (168.6), so OTM puts are rich relative to ATM.
- **Term structure.** The VIX3M/VIX ratio has a median of 1.13 and is below 1 on 7.5% of days. At VIX ≥ 40 its median is 0.90 (backwardation). After spikes, longer tenors are *relatively* cheap, which suggests "monetize short-dated, re-buy longer-dated" [I].
- **Spot–vol coupling.** ΔVIX ≈ −1.16 points per +1% move in SPX, and −1.70 on days with SPX < −2% [Cboe data]. Vega gains amplify put payoffs in crashes, so constant-vol models understate both hedge payoffs and mark-to-market (MTM) collateral inflows.
- **Path dependence.** Harvey et al. (2019) found that put performance "appears to be earned in short periods of time". They note that "subsequent rolls of the options become more expensive as implied volatility rises" [S].
  - Our HMM shows PPUT overlay carry of −1.8%/yr for months entered in the calm state, against −5.1%/yr for months entered in the stress state.
  - Israelov (2019) [S]: "Put options are only effective in reducing drawdowns in the unusual circumstance" that drawdowns coincide with the option holding period and there is no VRP.

### 2.5 Collateral mechanics

- **VM.** VM is daily cash or collateral transfer of MTM. It is zero-sum system-wide but highly unequal across participants.
  - ADIC's *long* hedges under a two-way CSA produce VM **inflows** as they gain.
  - A long synthetic beta position produces **outflows** in sell-offs.
- **IM.** IM covers potential future exposure over a margin period of risk (MPOR). The BCBS–IOSCO uncleared standard is a 10-day, 99% horizon [nrv for the exact paragraph]. IM must be segregated, cannot be reused, and is procyclical.
  - ISDA SIMM is the sensitivity-based industry model. Its public infohub lists v2.6 (Sep 2023) and a move to semiannual calibration from 2025 [S]; later versions may exist.
- **Schedule IM and haircuts (US rule, mirroring BCBS–IOSCO) [S].**

  | Item | Schedule IM, % of notional |
  |---|---|
  | Equity | 15% |
  | Commodity | 15% |
  | Other | 15% |
  | FX | 6% |
  | Interest rate (0–2 / 2–5 / 5+ yr) | 1% / 2% / 4% |
  | Credit (0–2 / 2–5 / 5+ yr) | 2% / 5% / 10% |

  - Netting adjustment: $IM=(0.4+0.6\,NGR)\times$ gross IM, where NGR is the net-to-gross ratio.
  - Collateral haircuts:
    - government securities 0.5% / 2% / 4% (<1 / 1–5 / >5 yr);
    - S&P 500 equities 15%;
    - S&P 1500 equities outside the S&P 500 25%;
    - gold 15%;
    - plus 8% for a currency mismatch.
- **Scope.**
  - Under the US rule, "financial end user" excludes a *sovereign entity*, defined as a central government or one of its agencies, departments, ministries, or central bank.
  - The material-swaps-exposure threshold is $8bn of average daily aggregate notional, and the IM threshold is $50m [S: 12 CFR 237.2].
  - ADIC's classification under US, EU and UK dealer rules is an open legal question with first-order liquidity consequences.
- **Venue [C].**
  - Listed long options are fully paid: no IM and no VM. Gains are realized only by selling.
  - OTC options under a CSA give VM inflows on gains but may require two-way IM or an independent amount.
  - Cleared IRS and CDX carry CCP IM plus daily cash VM.
- **CSA levers:**
  - threshold, minimum transfer amount (MTA), independent amount (IA);
  - eligible collateral, haircuts and currency;
  - reuse rights (title transfer vs pledge);
  - settlement timing, dispute process and rating triggers.
- **Bank-treasury analogues (Basel LCR) [S].**

  | Paragraph | Treatment |
  |---|---|
  | LCR40.49 | Net derivative outflows at 100% |
  | LCR40.52 | 20% of posted non-Level-1 collateral |
  | LCR40.53–55 | Excess, uncalled and substitutable collateral at 100% |
  | LCR40.51 | 3-notch downgrade triggers at 100% |
  | LCR40.56 | The historical look-back approach (HLBA): "the largest absolute net 30-day collateral flow realised during the preceding 24 months" |

### 2.6 Statistics of trading skill

- **Standard error of the Sharpe ratio.** For i.i.d. returns, $SE(\widehat{SR})\approx\sqrt{(1+\widehat{SR}^2/2)/T}$ (Lo 2002 [nrv]). Ten years at SR = 1 gives a standard error of about 0.39. Lo's headline result, however, concerns serially correlated returns: monthly Sharpe ratios cannot be annualized by multiplying by √12 "except under very special circumstances", and in his empirical example, because of serial correlation in monthly returns, a hedge fund's annual Sharpe ratio "can be overstated by as much as 65 percent" [S; corrected 2026-10-18: only the i.i.d. formula was quoted].
- **Deflated Sharpe ratio (DSR) [S: Bailey & López de Prado 2014].** Non-normality and multiple trials both inflate the Sharpe ratio. The DSR corrects for both:

  $$
  DSR=\Phi\!\left(\frac{(\widehat{SR}-SR_0)\sqrt{T-1}}{\sqrt{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right),
  $$

  $$
  SR_0=\sqrt{V[\{\widehat{SR}_n\}]}\Big((1-\gamma_E)\Phi^{-1}(1-\tfrac1N)+\gamma_E\Phi^{-1}(1-\tfrac1{Ne})\Big).
  $$

- **Haircuts [S: Harvey & Liu 2015].** Haircuts are non-linear in the initial Sharpe ratio; a flat 50% rule is wrong in both directions.
- **Crowding and funding liquidity [S].**
  - Carry trades are negatively skewed because they "suddenly unwind" when risk appetite and funding liquidity fall (Brunnermeier, Nagel & Pedersen 2009).
  - Coordinated deleveraging of similar portfolios produced the August 2007 quant losses (Khandani & Lo 2011).
  - Momentum crashes are documented by Daniel & Moskowitz (2016) [nrv] for cross-sectional momentum strategies. They bear on trend (time-series momentum) only by analogy [corrected 2026-10-18: scope added].
- **Risk budgeting.**
  - Volatility scaling improves Sharpe ratios for risk assets only, but cuts left-tail events and vol-of-vol across all assets [S: Harvey et al. 2018]. Moreira & Muir (2017) [S] report higher Sharpe ratios for volatility-managed factor portfolios, but that gain is disputed out of sample. Cederburg et al. (2020) find that, across 103 equity strategies, real-time implementable versions do not systematically beat the unmanaged portfolios. Barroso & Detzel (2021) find no abnormal returns after transaction costs for factors other than the market [corrected 2026-10-18: Moreira & Muir had been cited as unqualified support].
  - Under a maximum-drawdown constraint the optimal risky exposure is proportional to $W_t-\alpha M_t$, where $M$ is the running maximum (Grossman & Zhou 1993 [nrv]).
  - Under a random walk, all-or-nothing stop-loss rules always lower a strategy's expected return; in the presence of price momentum they can add value (Kaminski & Lo 2014 [S: abstract of the 2010 SSRN version; the journal abstract was not accessible]) [corrected 2026-10-18: was "add value only when returns are serially correlated"; the source's condition is price momentum].

---

## 3. Methods, models and trade-offs

### 3.1 Scenario generation for the overlay

| Approach | Strengths | Weaknesses | Use |
|---|---|---|---|
| Regime-switching lognormal or Student-t (RSLN; Hardy 2001 [nrv], the actuarial standard for variable-annuity guarantees) | Interpretable, fast, regime-conditional correlation | Weak implied-vol (IV) dynamics | Backbone of the state engine |
| Regime-switching stochastic vol with jumps (Heston/Bates family) | Internally consistent spot–vol–skew | Calibration drift, slow | Validation and hedge-design studies |
| Filtered historical simulation (FHS) / regime-conditioned block bootstrap of joint daily moves (SPX, VIX, rates, CDX, FX, oil) | Keeps the real crisis co-movement and skew | Bound to the historical sample | **Within-regime innovations** |
| Generative ML (conditional VAEs, diffusion models) | Flexible joint tails | Opaque, hard to defend at IC | Challenger only |

**Recommendation [I].** Use a hybrid.

- The state engine (regime stream) generates regime paths.
- Daily innovations are bootstrapped from historical days *of the same filtered regime*.
- Named synthetic stresses are overlaid on top: a 1987-type gap, the 2020 crash, the 2022 rate–equity grind, a 2022 gilt-style rate spike, and an oil collapse.

### 3.2 Pricing options along simulated paths

Every node needs an IV surface $\sigma_t(k,\tau)$, where $k=\ln(K/F)$.

**Option A: VIX-anchored sticky-moneyness surface.** Recommended for the production simulator.

$$
\sigma^{ATM}_t(\tau)=c_{ATM}\frac{VIX_t}{100}\Big[1+(\rho_{s_t}-1)\min\!\big(1,\tfrac{\tau-1/12}{2/12}\big)\Big],\qquad
\sigma_t(k,\tau)=\sigma^{ATM}_t(\tau)\Big[1-a_{s_t}\tfrac{k}{\sqrt\tau}+b_{s_t}\tfrac{k^2}{\tau}\Big]
$$

- $\rho_s$ is the regime's VIX3M/VIX ratio.
- $a_s$ and $b_s$ are skew and curvature parameters, calibrated to option surfaces (25-delta risk reversals and butterflies), with SKEW as a regime cross-check.
- The surface is clipped to the no-butterfly and no-calendar arbitrage region.

**Option B: SVI/SSVI with regime-dependent parameters** (Gatheral & Jacquier 2014 [nrv]). Arbitrage-free by construction; more parameters to drive.

**Option C: full stochastic vol plus jumps.** Use only to stress Option A's IV dynamics.

**Pricing and Greeks.** Value positions with Black–Scholes–Merton (Black-76 for futures-style underlyings), using the simulated surface. Compute Greeks for SIMM inputs. Variance swaps are valued by static replication, with fair strike ≈ VIX² for 30 days (Demeterfi et al. 1999 [nrv]).

### 3.3 Hedge-program design: dimensions and evidence

| Dimension | Evidence | Default design [I] |
|---|---|---|
| **Strike** | ATM 1m puts: reliable (8/8 drawdowns) but −7.4% p.a. 5–10% OTM puts: cheaper, but drawdown performance "no longer consistently positive" and they fail in gradual drawdowns [S: Harvey et al., broker OTC data 1996–2018]. | Put spreads (long ~90%, short ~70–75% forward) when SKEW is high. Outright deep-OTM puts only when the wing is cheap. |
| **Tenor** | Short tenors carry gamma for fast crashes. Long tenors carry vega, lower theta per day and less expiry mismatch (Israelov). | A 3/6/12-month ladder, weighted toward 6m. Shift to longer tenors after spikes (backwardation). |
| **Roll and timing** | Rolls are expensive once a drawdown has begun [S]. VRP is lowest at low VIX. | Staggered monthly rolls. Increase the budget when VRP is low *and* the fragility signal rises. Never "catch up" in the stress state. |
| **Monetization** | VIX mean-reverts: the stress state's expected duration is about 35 trading days, with 0.61 monthly persistence [Cboe data/HMM]. | Partial monetization when any trigger fires: put delta ≤ −0.5; value ≥ 3× premium; regime = stress and VIX ≥ 35. Re-strike lower (roll down) with 30–50% of proceeds. Optimize thresholds by policy search with DSR/PBO (probability of backtest overfitting) guards. |
| **Instrument mix** | Crisis types differ: crash (1987, 2020), grind (2000–02, 2022), credit (2008), oil or stagflation shock. Diversification across defensive strategies is the robust choice [S: Harvey et al.]. | A stack: dynamic beta overlay, trend, put spreads, VIX calls, CDX HY/IG protection, and oil puts or hybrids if fiscal draws are oil-linked. |

**Monetization as optimal stopping [I].** Treat the decision as an American-style choice written on a European option. Monetize at $t$ if

$$V_{j,t}(1-\text{ba}_s)+\lambda_t V_{j,t}\ \ge\ \mathbb E_t[\text{continuation value}].$$

When λ is high (liquidity is scarce), monetize earlier. Approximate the continuation value by Longstaff–Schwartz regression on (VIX, regime, moneyness, τ) across simulated paths.

### 3.4 Valuing protection inside the total portfolio

Five complementary methods; report all five to the IC.

1. **Shadow-price valuation.** Use the duals of per-path liquidity and floor constraints from the recourse LP (§6.4 E) and compute $\sum_t\mathbb E[\lambda_tX_t]$.
2. **Avoided forced-sale cost.** Merit-order accounting of the recourse actions avoided, such as secondary sales at discount $d_s$ and liquid sales near troughs.
3. **Outcome deltas** against an *Israelov baseline* (divest to equal expected return) and against no hedge. Measure Δ in:
   - P(distribution shortfall);
   - P(5-yr return ≥ 10%);
   - P(Tier-1 floor breach);
   - ES, maximum drawdown, and E[$ secondary sales].
4. **Cost per unit of crisis liquidity**, $c_j=-\mathbb E[\text{annual P\&L}_j]\,/\,\mathbb E[\text{payoff}_j\mid\text{crisis}]$, as an instrument screen (§4.3).
5. **Robust valuation.** Take the worst case over an ambiguity set covering crisis probability π, λ calibration and the crisis-type mix: a Wasserstein or φ-divergence ball around the regime transition matrix (Mohajerin Esfahani & Kuhn 2018 [nrv]). Hedges whose value survives this ambiguity are preferred.

### 3.5 Opportunistic-strategy return model

$$
r^O_t=\ell_t\big[\mu^O_{s_t}\Delta t+\sigma^O_{s_t}\sqrt{\Delta t}\,\xi_t\big]+J^O_t,\qquad
\ell_t=\min\!\Big(\ell^{max},\frac{v_t}{\hat\sigma^O_t}\Big)\,g(DD_t),\quad g(DD)=\Big(1-\frac{DD}{DD^{max}}\Big)^+
$$

- **Innovations.** $\xi_t$ is skew-t with family-specific skew. Trend is positively skewed, consistent with Sepp & Lucic (2026) [S], who show analytically that trend-system skewness is positive at every horizon under white noise. Carry, relative value (RV) and short-vol are negatively skewed.
- **Crowding jump.** $J^O_t\sim\text{Bernoulli}(\lambda^J_s\Delta t)\times(-k^J\sigma^O_s)$, active mainly in stress regimes. $\hat\sigma^O$ is an EWMA forecast.
- **Mean.** $\mu^O_s=SR^{post}_s\sigma^O_s$, where the posterior Sharpe ratio comes from normal–normal shrinkage:

  $$SR^{post}=SR_{prior}+w(\widehat{SR}-SR_{prior}),\qquad w=\frac{\tau^2}{\tau^2+SE^2}.$$

  *Example:* $\widehat{SR}=1.0$ over 8 years with skew −0.5 and kurtosis 5 gives SE ≈ 0.56. With prior 0.3 and τ = 0.25, the posterior is ≈ **0.42**. With N = 50 trials and cross-trial SR dispersion 0.25, the DSR is ≈ 0.86, which fails a 0.95 gate.
- **Margin.**
  - Futures: $IM^O_t=\sum_i|N_i|m_i(s_t)$.
  - OTC: SIMM-like sensitivities.
  - VM equals P&L, so losses are cash outflows.
- **Liquidity-adjusted ranking [I].** Rank strategies by $\mathbb E[(1+\lambda_s)r^O_s]/\sigma^O$.
  - Strategies that lose in high-λ states (carry, short vol, crowded RV) are penalized.
  - Trend and long-convexity RV are rewarded.

### 3.6 Synthetic beta and portable alpha with stale private NAVs

- **True exposure.** Estimate the private book's exposure by de-smoothing reported NAV returns, e.g. Getmansky–Lo–Makarov θ-weights [nrv], in coordination with the PE stream.
- **Overlay notional.**

  $$N^\beta_{a,t}=\frac{(\beta^*_{a,t}-\hat\beta^{phys,true}_{a,t})\,NAV_t}{\beta^{inst}_a}.$$

- **Costs and flows.**
  - P&L: $N^\beta_{a,t}(r_{a,t}-f_{a,t}\Delta t)$, where $f$ is the futures-implied or total return swap (TRS) financing spread over cash.
  - VM equals daily P&L.
  - IM: $m^\beta_a(s)|N^\beta_a|$ with $m^\beta_a(s)=\max\big(m^{floor}_a,\;z_{0.99}\sigma_{a,s}\sqrt{MPOR/252}\big)$.
- **Portable alpha [C].** The classic failure is an "alpha" pool that is illiquid (hedge funds, private credit) just when the beta leg's margin is due.
  - Rule: keep the collateral backing synthetic beta in HQLA.
  - Rule: never count illiquid alpha assets as margin capacity.
- **The fast lever.** The overlay is the "hedge versus amplify" lever of the prior deck. The dynamic beta overlay is the *cheapest* way to reduce beta: its cost is the forgone ERP, not the VRP. Short futures are also state-contingent liquidity providers, generating VM inflows in sell-offs [I].
  - What linear hedges cannot do is protect against gaps and decision latency. Equities fell 34% in 23 trading days in 2020 and 20% in one day in 1987, while the IC meets monthly or quarterly.
  - That gap is the residual job of the convex sleeve.

### 3.7 The margin and collateral engine

- **VM path.** Compute daily in stress windows and monthly otherwise. Monthly steps understate peak intra-month needs.
- **IM models:**
  - CCPs: EWMA volatility with an anti-procyclicality (APC) floor. The EU EMIR options are a 25% buffer, ≥25% stressed weight, or a 10-year look-back [nrv: Del. Reg. 153/2013 Art. 28]. The FSB found APC tools slowed March 2020 IM increases "only for a short time period" [S].
  - Uncleared: SIMM-like delta/vega/curvature, or schedule IM as a fallback.
- **Collateral waterfall:** cash → T-bills → UST by maturity → other government bonds (with regime haircuts) → repo of non-HQLA → facility draws.
- **HLBA tracker.** The trailing 24-month maximum of |net 30-day collateral flow|.
  - Note its procyclicality. In Oct 2026 the window still contains April 2025 (S&P −18.9%, VIX close 52.33), which drops out in April 2027.

### 3.8 Optimization approaches

| Method | Pros | Cons | Role [I] |
|---|---|---|---|
| Parametric policy search: hedge budget, strike/tenor weights, monetization thresholds, vol target, DD scaling; CMA-ES or Bayesian optimization over Monte Carlo with common random numbers | Explainable rules the IC can approve. Handles path dependence and chance constraints. | Local optima. Overfitting risk, so use DSR/PBO and out-of-sample regimes. | **Primary** |
| Multi-stage stochastic programming on scenario trees | Explicit recourse, duals give λ | Tree explosion; IV paths are hard to embed | Strategic studies, λ calibration |
| Stochastic dual dynamic programming (SDDP) | Scales in stages | Needs convexity and stagewise independence; regimes are Markov states | Liquidity and commitment pacing with linearized overlay |
| Model predictive control (MPC) with chance constraints | Matches the IC cadence (re-optimize monthly); feedforward from DPI and call forecasts | Myopia unless a terminal value is used | **Operational loop** |
| Deep hedging (Buehler et al. 2018 [S]) | Instrument-level hedging under frictions with convex risk measures | Data hungry, opaque | Execution research |
| Distributionally robust optimization (DRO) / robust optimization | Guards against π and λ misspecification | Conservative | Tier-1 gate |

---

## 4. Empirical evidence and current market data

### 4.1 Defensive strategies in the 8 worst S&P 500 drawdowns, 1985–2018 [S: Harvey et al. 2019]

| Strategy | Evidence |
|---|---|
| Long 1m ATM S&P 500 puts | Positive in 8/8 drawdowns; full-sample excess return −7.4% p.a. An equal-weight equity-plus-put mix had a negative excess return in every crisis. |
| Short credit risk (IG vs duration-matched UST, scaled to 10% vol) | −3.6% p.a. full sample; +128% in 2007–09. CDX implementation cost <0.1% p.a. |
| Long 10y UST | +10.6% p.a. in drawdowns and +3.1% in normal periods, but effective only post-2000. The negative stock–bond correlation is a "historical rarity". |
| Gold | Positive in 7/8 drawdowns, +9.0% p.a. in drawdowns, negative otherwise. |
| TSMOM (50 futures) | 1m and 3m signals performed well in crises. 12m was negative in the three most recent drawdowns. Capping equity exposure at zero improved crisis returns but cost 1.1% (3m) and 0.9% (12m) p.a. Trading costs 0.6–0.8% p.a. |
| Quality long/short (beta-neutral) | Among the most promising crisis hedges. Costs 1.0–2.0% p.a. |

14% of days since 1985 were equity-drawdown days.

### 4.2 Cboe hedged-equity indices, through 16 Oct 2026 [Cboe data]

| Index | Period | CAGR | Vol | Max DD | Oct–Nov 2008 | 19 Feb–23 Mar 2020 | 2022 (3 Jan–12 Oct) | 19 Feb–8 Apr 2025 |
|---|---|---|---|---|---|---|---|---|
| SPX (price) | 30 Jun 1986– | 8.85% | 18.4% | −56.8% | −35.5% | −33.9% | −25.4% | −18.9% |
| PPUT (5% OTM monthly puts) | 30 Jun 1986– | 7.97% | 13.5% | −42.0% | −9.7% | −11.8% | −21.7% | −10.8% |
| CLLZ (zero-cost put-spread collar) | 30 Jun 1986– | 8.11% | 14.6% | −47.2% | −32.1% | −30.9% | −19.0% | −14.6% |
| CLL (95/110 collar) | 26 Aug 2008– | 6.87% (SPX 10.41%) | 13.1% | −26.3% | −2.7% | −14.9% | −17.1% | −12.8% |
| VXTH (S&P 500 + VIX calls) | 31 Mar 2006– | 9.85% (SPX 9.04%) | 16.4% | −43.3% | −16.9% | **+27.6%** | **−29.2%** | −9.5% |

- In SPX's worst months, PPUT returned:
  - −0.3% when SPX fell −16.9% (Oct 2008);
  - +2.2% when SPX fell −12.5% (Mar 2020);
  - −10.6% when SPX fell −21.8% (Oct 1987).
- PPUT had 18 monthly declines of ≥6%, against 35 for the S&P 500 [S: Cboe 2021].

### 4.3 Cost per unit of crisis payoff, our estimate [Cboe data; I]

The annual gap is measured against S&P 500 total return, with the dividend yield at 2.0% (range 1.5–2.5%). Crisis windows:

- 1987, 2000–02, 2007–09, 2011, 2018Q4, 2020, 2022 and 2025;
- CLL and VXTH cover only the windows after their launch.

| Index | Annual gap | Mean crisis-window excess | Cost per $ crisis payoff per yr |
|---|---|---|---|
| PPUT | −2.8% (−2.3 to −3.3) | +9.6% (8 windows; COVID +22.0, 2022 +2.1) | **0.29** (0.23–0.36) |
| CLLZ | −2.7% (−2.2 to −3.2) | +5.5% | 0.49 (0.37–0.62) |
| CLL | −5.3% (−4.8 to −5.8); includes capped upside in a bull market | +9.1% | 0.58 (0.52–0.65) |
| VXTH | −1.25% (−0.75 to −1.75) | +13.7% (COVID +61.3; 2022 −5.4) | **0.09** (0.05–0.13); ≈0.30 ex-COVID |

**Reading.**

- On these numbers, convexity costs roughly $0.1–0.6 of expected carry per year for each $1 of crisis-window payoff.
- Divesting a liquid risk asset into cash costs the forgone ERP (perhaps 3–6% p.a.) and "pays" the avoided drawdown (about 30% in a crash). That is about 0.1–0.2 per $, consistent with Israelov's dominance result.
- Options therefore earn their place only through (a) non-linear objectives and constraints (§2.2), (b) gap and decision-latency protection, or (c) buying in cheap regimes [I].
- Small samples: a single episode (COVID) drives the VXTH figure.

### 4.4 Option-market regime calibration, 1990–16 Oct 2026 [Cboe data]

**VIX level and VRP.**

- VIX mean 19.42, median 17.56.
- Percentiles: p90 28.50, p95 32.88, p99 46.70; maximum close 82.69 (16 Mar 2020).
- Share of days with VIX > 30: 7.9%; VIX > 40: 2.2%.
- VRP (VIX minus subsequent 21-day realized vol) by VIX bucket:

  | VIX bucket | <15 | 15–20 | 20–30 | 30–40 | ≥40 |
  |---|---|---|---|---|---|
  | Mean VRP (vol pts) | 2.8 | 4.1 | 4.9 | 6.5 | 5.8 |

  The 5th percentile of the VRP is −4.9, so long-vol positions win only in the tail.

**Term structure (VIX3M/VIX median by VIX level).**

| VIX level | <15 | 15–20 | 20–30 | 30–40 | ≥40 |
|---|---|---|---|---|---|
| Median VIX3M/VIX | 1.18 | 1.13 | 1.08 | 1.01 | 0.90 |

**Skew and vol-of-vol.**

- SKEW long-run mean 123.3. Since 2025: mean 146.1, record 183.1 (18 Feb 2025). Latest 168.6.
- VVIX mean 93.9 since 2007, maximum 207.6 (16 Mar 2020), latest 109.9.

**Spot–vol beta.** −1.16 VIX points per 1% SPX move; −1.70 on days with SPX < −2%; −1.01 on up days.

**VIX shocks.**

- +115.6% on 5 Feb 2018 (17.31 → 37.32), the short-vol unwind.
- 5 Aug 2024: intraday 65.73, close 38.57.
- 8 Apr 2025: close 52.33.
- 2026 year to date: maximum close 31.05 (27 Mar).

**4-state Gaussian HMM on daily log VIX** (n = 9,262; our fit; Viterbi labels):

| State | VIX level (p10–p90) | Stationary share | Expected duration | SPX vol | p1 daily SPX | VRP | VIX3M/VIX | SKEW |
|---|---|---|---|---|---|---|---|---|
| S0 calm | 12.5 (10.9–14.0) | 27.6% | 41 days | 8.6% | −1.46% | 2.9 | 1.18 | 124.8 |
| S1 normal | 16.3 (14.7–18.0) | 27.5% | 19 days | 12.2% | −2.09% | 4.1 | 1.15 | 126.1 |
| S2 elevated | 21.1 (18.7–23.9) | 26.2% | 20 days | 17.0% | −2.78% | 4.4 | 1.10 | 121.4 |
| S3 stress | 30.7 (24.9–41.8) | 18.6% | 35 days | 31.7% | −5.41% | 5.5 | 1.04 | 119.5 |

- **21-day (monthly) transition matrix**, rows "from" S0..S3:

  |  | to S0 | to S1 | to S2 | to S3 |
  |---|---|---|---|---|
  | from S0 | 0.664 | 0.257 | 0.067 | 0.011 |
  | from S1 | 0.258 | 0.442 | 0.238 | 0.061 |
  | from S2 | 0.073 | 0.255 | 0.468 | 0.204 |
  | from S3 | 0.014 | 0.083 | 0.298 | 0.605 |

- **PPUT overlay carry by state at month entry** (dividends at 2%):

  | Entry state | S0 | S1 | S2 | S3 |
  |---|---|---|---|---|
  | Carry, %/yr | −1.8 | −3.8 | −3.2 | −5.1 |

- **S3 episodes** include 2008-09-09 to 2009-09-08 (252 days), 2020-02-24 to 07-28, several in 2022, 2025-04-03 to 04-28 and 2026-03-06 to 04-07.
- **Current state (16 Oct 2026):** smoothed probabilities S1 0.635, S2 0.364.
- **Caveat:** S3 mixes "elevated-stress" with true crisis days. Add a fifth state or a jump overlay for VIX > 45.

### 4.5 Tail moves for margin sizing [Cboe data]

**SPX price returns since 1975:**

| Horizon | p1 | p0.1 | Worst | Worst since 2000 |
|---|---|---|---|---|
| 1-day | −2.95% | −6.63% | −20.47% (19 Oct 1987) | −11.98% |
| 10-day | −8.49% | −20.14% | −31.47% | −25.88% |
| 21-day | −11.70% | −26.09% | −32.97% (23 Mar 2020) | −32.97% |

**SPX longer horizons (overlapping windows):**

- 3-month p2.5: −13.7%.
- 1-year: p2.5 −23.3%, p1 −36.2%.

**Forward 12-month SPX price return by VIX at entry (overlapping, few independent episodes):**

| VIX at entry | <15 | 30–40 | ≥40 |
|---|---|---|---|
| Mean | 11.1% | 18.1% | 33.0% |

This is the empirical basis for "rebalancing value". Treat it with great caution.

### 4.6 Margin and collateral stress episodes

- **March 2020 [S].**
  - Most of the IM increase came 6–13 March.
  - Some CCPs' IM rose >100% against the prior quarter.
  - Daily incremental IM was "notably smaller" than same-day VM calls.
  - Foreign holders sold almost $300bn of Treasuries in March (FSB 2020).
  - Average peak VM per CCP was $2.5bn, 1.6× the previous peak (June 2016) and 2.3× the prior quarter. An aggregate figure of about $150bn was reported across 59 clearing services, which the author cautions is not the maximum margin call (Clarus, 15 Jul 2020).
  - VM in cleared and uncleared markets was "significantly higher than in February", while uncleared IM stayed relatively stable (BCBS–CPMI–IOSCO 2022).
- **UK LDI, Sept–Oct 2022 [S].**
  - 30-year gilt yields rose >270 bp between 1 Aug and the 14 Oct peak, briefly above 5%.
  - The FSR describes "a vicious spiral of collateral calls and forced gilt sales". It says buffers were "too low and less usable in practice than expected" (BoE FSR Dec 2022).
  - The BoE bought £19.3bn of gilts and later sold them for £23.1bn (Wikipedia, citing BoE).
  - The FPC set LDI resilience at "around 250 basis points, at a minimum", on top of day-to-day buffers (FPC, Mar 2023).
- **Commodities 2022 [S].**
  - Oil rose >30%; European gas and industrial metals roughly doubled.
  - Margin calls spiked, especially in Europe. LME nickel was the one market-functioning failure (FSB 2023).
  - Widely reported but not verified here [nrv]: the LME cancelled nickel trades, and an energy-industry estimate put European margin needs at about €1.5tn.
- **Archegos, Mar 2021.** Prime-broker losses on bilateral TRS; Credit Suisse lost about $5.5bn [nrv]. FSB (2024) lists Archegos among the motivating episodes [S].
- **Policy response [S].**
  - FSB Dec 2024: eight recommendations (liquidity-risk governance, extreme-but-plausible margin stress tests, sufficient cash and liquid assets, collateral operations, counterparty engagement).
  - BCBS–IOSCO Jan 2025: eight recommendations on VM processes and IM-model responsiveness (as referenced on the BIS 2022 review page).

### 4.7 Opportunistic-strategy evidence

- **Carry [S: Koijen et al. 2018].** Annualized Sharpe of 0.6–0.9 within each asset class and **1.49** for the diversified portfolio (backtest). Carry strategies across asset classes can do poorly at the same time, in periods that "coincide with global recessions".
- **TSMOM [S: Moskowitz, Ooi & Pedersen 2012].**
  - Diversified Sharpe >1 (gross backtest), about 2.5× the equity market's.
  - Large profits in Oct–Dec 2008.
  - 1966–85 out-of-sample Sharpe 1.1.
  - Hurst, Ooi & Pedersen (2017) extend this to 1880 and flag rising correlations and AUM after 2008 [S].
- **Implication [I].** Live institutional macro, RV and CTA books should be underwritten at SR ≈ 0.3–0.5 net unless ADIC's own track record survives shrinkage and the DSR.

### 4.8 Private-market liquidity costs (for λ)

- Secondary pricing [S, via Wikipedia]:
  - average discount to NAV 35% in 2009 and 7% in 2013 (WSJ);
  - 2025 LP-portfolio pricing at 87% of NAV: buyout 92%, venture/growth 78% (Jefferies, 10 Feb 2026).
- Harvard's endowment fell about $8bn (about 22%) in 2008–09 amid a "cash squeeze", with errant interest-rate, derivatives and leveraged positions (NYT via Wikipedia) [S].

### 4.9 Tail-fund claims and critiques

- **Universa [S, Wikipedia]:**
  - +3,612% on invested capital in March 2020 (investor letter);
  - >100% in 2008;
  - a WSJ-reported hypothetical: a 3.3% Universa / 96.7% S&P portfolio returned 12.3% CAGR over the 10 years to Feb 2018.
- **AQR's critique (2020, via press summaries) [S]:** the biggest crash-month winners tend to lose most of their allocated capital in good times. Other managers alleged cherry-picking.
- **Read-across [I]:** headline tail-fund returns are on *allocated* capital, not on hedged notional. Evaluate any program on total-portfolio, λ-weighted terms.

---

## 5. Practitioner and peer practice: case studies

1. **CalPERS, 2019–20 [S, press summaries].**
   - CalPERS told Universa in Oct 2019 to unwind its tail hedge, citing cost, scalability and "better alternatives". The unwind was done by Jan 2020, and press estimates say it missed about $1bn of gains in March 2020.
   - A second program (LongTail Alpha) was held to 31 Mar and earned several hundred million dollars.
   - *Lesson:* "hedge fatigue" is the main way tail programs fail. The cure is a precommitment rule, a cumulative-carry tracker and IC-level ownership of the hedge budget [I].
2. **UK LDI, 2022.**
   - Leveraged rate hedges were collateralized with assets that had to be sold into a falling market.
   - Buffers had been sized on historical yield moves and were operationally slow to replenish.
   - *Lessons:*
     - size buffers to extreme-but-plausible moves (≥250 bp in gilts);
     - pre-agree collateral-raising waterfalls;
     - test operations at speed.
3. **March 2020, the dash for cash.**
   - VM, not IM, hit first and hardest. IM followed within days.
   - Even Treasuries became hard to liquidate.
   - *Lesson:* hold the first line of margin liquidity in cash or T-bills, not longer bonds [I].
4. **Harvard, 2008–09.** An endowment-model portfolio with derivatives and leverage met a liquidity squeeze with an illiquid private book. This is the template ADIC's ledger must stress.
5. **NZ Super [S].**
   - Uses derivatives for "completing the portfolio" (delivering Reference Portfolio exposures), to rebalance drift, and for contrarian, value-based strategic tilting.
   - Holds a collateral pool behind the exposures; closing a derivative position is described as an immediate source of cash.
   - The closest public analogue to ADIC's "overlay as fast lever".
6. **Defensive stacks [C].** Large pensions increasingly run diversified "risk-mitigating" sleeves (trend, long duration, macro, and sometimes explicit tail options) rather than single-instrument tail programs. This is consistent with Harvey et al.'s conclusion that "diversification across a number of promising defensive strategies may be most prudent" [S].

---

## 6. Design implications for the ADIC framework

### 6.1 Placement in the architecture [I]

The **Overlay Engine** is deterministic code with four modules:

1. Hedge Book
2. Opportunistic Book
3. Synthetic Beta
4. Collateral and Liquidity Ledger, which emits per-path λ

It feeds the multi-period optimizer and the Tier-1 gate.

LLM agents wrap it but never compute numbers. Following the *Agentic Scientist* pattern:

- **Overlay-Design agent:** proposes candidate programs.
- **Meta-controller:** runs them in parallel in the sandboxed simulator with common random numbers. It always includes these **baselines**:
  - no hedge;
  - the Israelov divest-equivalent;
  - a static put ladder;
  - trend only.

  It also runs these **ablations**:
  - no monetization;
  - no regime timing;
  - no VM recognition.
- **Overlay-Challenge agent** looks for:
  - crisis-type coverage gaps;
  - offsetting trades between the hedge and opportunistic books;
  - hedge fatigue;
  - CSA and legal issues.
- **Rubric checks:**
  - surface no-arbitrage;
  - margin backtest against realized VM (Kupiec test);
  - DSR ≥ 0.95 for new rules;
  - significance of liquidity-metric improvements across seeds.

### 6.2 State variables $\mathbf x_t$

The model steps monthly, with daily sub-steps whenever the regime is S3 or |daily return| > 2%.

- **Regime:** $s_t$ and filtered posterior $\hat{\mathbf p}_t$ (from the state engine).
- **Markets:**
  - equity $S_t$ (SPX/ACWI);
  - curve $y_t$; CDX spreads $c_t$; FX $f_t$; oil $o_t$;
  - cash rate $r_t$; dividend yield $q_t$.
- **Vol state:**
  - $VIX_t$;
  - term ratio $\rho_t$;
  - skew $\kappa_t$ (SKEW or 25-delta risk reversal);
  - $VVIX_t$;
  - VRP estimate.
- **Hedge book:**
  - $\{(\text{type},K_j,T_j,N_j,\text{cpty}_j,\text{venue}_j,P^{paid}_j)\}$, with MTM $V^H_t$ and Greeks;
  - cumulative carry $\Sigma^{carry}_t$.
- **Opportunistic book:** equity $E^O_t$, high-water mark $M^O_t$, drawdown $DD_t$, leverage $\ell_t$, margin $IM^O_t$.
- **Synthetic beta:** $N^\beta_{a,t}$ for $a$ ∈ {EQ, DUR, CRD, FX, CMD}.
- **Collateral and liquidity:**
  - cash $C_t$;
  - HQLA by type $Q_{q,t}$;
  - encumbered IM $E_t$;
  - collateral received $R_t$, with reuse flag;
  - undrawn facilities $F_t$;
  - trailing HLBA window.
- **Liabilities and private flows (other streams):**
  - distributions due $D_t$ (possibly fiscal- or oil-linked);
  - calls $K_t$;
  - PE distributions received $P_t$;
  - secondary discount $d_{s,t}$.
- **Counterparties:** net exposure $X_{c,t}$ and dealer stress indicator.

### 6.3 Decision variables $\mathbf u_t$

- $b_{a,t}$: synthetic beta notional (% NAV, signed): the *hedge versus amplify* lever.
- $h_t$: convex-sleeve budget (% NAV per year), with weights $w_{i}(s,\text{VRP},\text{skew})$ over instrument buckets:
  - put spreads by strike and tenor;
  - deep-OTM puts;
  - VIX calls;
  - CDX protection;
  - oil puts or hybrids.
- $\theta^{mon}=(\delta^*,m^*,v^*,f,\rho^{reset})$: monetization policy.
- $\omega_t$: trend allocation (defensive stack).
- $v_t$ (opportunistic vol budget), $DD^{max}$, re-risk speed; strategy weights after the DSR gate.
- $c^*_t$: collateral-pool target and mix. $F$: committed facility size (structural).
- Structural or legal: venue per instrument (listed or OTC); CSA terms (threshold, MTA, eligible collateral, reuse).

### 6.4 Simulation-ready model equations

**A. Market and vol dynamics** (daily Δt = 1/252).

$$r_t=\mu_{s}\Delta t+\sigma_{s}\sqrt{\Delta t}\,\varepsilon_t+J_t,\quad \varepsilon\sim t_{\nu}\ (\nu=5)$$

$$\Delta VIX_t=\kappa_s(\bar V_s-VIX_{t-1})\Delta t+\beta^-\min(100r_t,0)+\beta^+\max(100r_t,0)+\eta_s\sqrt{\Delta t}\,z_t$$

- Defaults: $\beta^-=-1.7$, $\beta^+=-1.0$.
- $\bar V_s$ from §4.4.
- The IV surface is as in §3.2. Alternatively, draw $(r_t,\Delta VIX_t,\Delta\text{skew}_t,\Delta c_t,\Delta y_t)$ jointly by regime-conditioned bootstrap.

**B. Tail-hedge book.**

$$V^H_t=\sum_j N_j\,\mathrm{BS}\big(S_t,K_j,T_j-t,r_t,q_t,\sigma_t(k_j,\tau_j)\big)$$

- **Purchases:** $N_{new}=h_t NAV_t\,w_i/(12\,V_{i,0})$.
- **Monetization:** sell fraction $f$ when a trigger fires; cash $+fN_jV_{j,t}(1-\text{ba}_{s_t})$; reset with $\rho^{reset}$ of the proceeds.
- **OTC CSA:**
  - collateral held $R_t=\lfloor\max(0,V^{c}_t-H_c)\rfloor_{MTA}$;
  - VM inflow $\Delta R_{t}$, settled T+1;
  - recognized liquidity $\phi^{OTC}R_t$ (φ = 0.7).
- **UMR IM if in scope:** $IM^H_t=\mathrm{SIMM}(\Delta,\mathcal V,\text{CVR})$, encumbered.
- **Listed options:** no VM or IM; recognized liquidity $\phi^{L}V^L_t$ (φ = 0.85).
- **Counterparty default:** probability $p_{c,s}\Delta t$, loss $LGD\cdot\max(0,V^c_t-R^c_t)$.

**C. Opportunistic book.** As in §3.5. Margin is $IM^O_t=\sum_i|N_i|m_i(s_t)$, and VM is $-$P&L.

Family templates for $SR^{post}_s$ in S0/S1/S2/S3:

| Family | S0 | S1 | S2 | S3 |
|---|---|---|---|---|
| Trend | 0.3 | 0.3 | 0.4 | 0.6 |
| Carry and RV | 0.6 | 0.5 | 0.2 | −1.0 |
| Short-vol | 0.9 | 0.6 | 0.0 | −2.0 |

These templates are [I] placeholders and must be calibrated to ADIC's P&L history.

**D. Synthetic beta.**

$$\text{P\&L}^\beta_t=\sum_aN^\beta_{a,t}(r_{a,t}-f_{a,t}\Delta t),\qquad VM^\beta_t=\text{P\&L}^\beta_t,\qquad IM^\beta_t=\sum_a m^\beta_a(s_t)|N^\beta_{a,t}|$$

**E. Liquidity ledger and recourse LP** (produces λ).

$$L_{t+1}=L_t+P_t+\Delta R_t+\text{Mon}_t-D_t-K_t-VM^{out}_t-\Delta IM_t-\text{Prem}_t-\text{Fin}_t$$

If $L_{t+1}<L^{min}$, solve

$$\min_{y\ge0}\sum_kc_k(s)y_k\quad\text{s.t.}\quad\sum_ky_k\ge L^{min}-L_{t+1},\quad y_k\le\bar y_k(s).$$

The recourse sources are:

| Source | Cost $c_k(s)$ |
|---|---|
| Facility draw | Spread |
| Repo of bonds | Haircut carry |
| Sell liquid equities | Impact plus opportunity cost |
| Cut the opportunistic book | Unwind cost |
| Slow commitments | Forgone α* |
| PE secondary sale | $d_s/(1-d_s)$ |
| Defer distribution (if permitted) | Penalty $\Pi_D$ |

$\lambda_t$ is the LP dual, i.e. the cost of the marginal source. Store it per path. The hedge's liquidity value is then $\sum_t\mathbb E[\lambda_tX_t]$.

### 6.5 Constraints

- **C1 Liquidity survival (chance constraint):** $\Pr\{\min_{\tau\le t+36m}L_\tau\ge L^{min}\}\ge1-\epsilon_L$ with $\epsilon_L$ = 1%. The prior deck reported 0.6% 12-month breach risk.
- **C2 Stressed collateral coverage**, checked daily:

  $$
  \text{HQLA}^{unenc}(1-h)\ \ge\ \max\big(\text{HLBA}_t,\ VM^{99\%,10d}_t+\Delta IM^{stress}_t\big)+D_{t:t+3m}+K^{stress}_{t:t+3m}-P^{stress}_{t:t+3m}
  $$

- **C3** IG plus cash ≥ 8% NAV, excluding encumbered IM.
- **C4 Leverage and risk:**
  - gross notional/NAV ≤ $G^{max}$;
  - net beta within its band;
  - overlay ES$_{97.5}$ ≤ budget.
- **C5 Counterparty:**
  - net exposure per dealer ≤ 0.5% NAV;
  - at least 5 dealers;
  - CSA mandatory for OTC hedges.
- **C6 Precommitment:** $h_t\ge h^{min}$ unless the IC overrides with a logged rationale.
- **C7 Opportunistic book:**
  - $v_t\le v^{max}$;
  - drawdown stop;
  - DSR ≥ 0.95 to add a strategy;
  - ADV-based capacity caps.
- **C8 Tier-1 robust floor:** $\sup_{Q\in\mathcal Q}\Pr_Q(R^{ann}_{5y}<7\%)\le5\%$.

### 6.6 Objective (Tier 2)

$$
\max_{\mathbf u}\ \Pr(R^{ann}_{5y}\ge10\%)+\kappa_\alpha\mathbb E[\alpha^*]-\kappa_{DD}\,\text{CVaR}_{95}(DD)-\mathbb E\Big[\sum_t\sum_kc_k(s_t)y_{k,t}\Big]-\Pi_D\,\mathbb E[\#\text{shortfalls}]
$$

- Overlay P&L enters returns directly.
- The hedge's benefit appears *endogenously*, as lower recourse costs, fewer shortfalls and a looser C8. There is no separate "hedge value" term, which prevents double counting.
- Report the ex-post decomposition into carry, liquidity, enabling and rebalancing via Shapley values over overlay components (prior deck, slide 6).

### 6.7 Default parameters

| Parameter | Default | Basis |
|---|---|---|
| Regimes | 4 (S0–S3) from §4.4; add a 5th for VIX > 45 | Cboe data / [I] |
| Equity vol by state | 8.6 / 12.2 / 17.0 / 31.7% | Cboe data |
| $\bar V_s$ | 12.5 / 16.3 / 21.1 / 30.7 | Cboe data |
| $\rho_s$ (VIX3M/VIX) | 1.18 / 1.15 / 1.10 / 1.04; 0.90 if VIX ≥ 40 | Cboe data |
| Spot–vol $\beta^-$ / $\beta^+$ | −1.7 / −1.0 VIX pts per 1% | Cboe data |
| $c_{ATM}$ (ATM IV / VIX) | 0.90 | [I], calibrate |
| 3m 90% put IV minus ATM | +5–7 vol pts (normal states) | [C, nrv] |
| Convex-sleeve budget $h$ | 0.25–0.5% NAV/yr; 0.15% floor $h^{min}$ | [I] from §2.2 and §4.3 |
| Put-spread strikes / tenors | 90/72% fwd; 3/6/12m ladder (25/50/25) | [I] |
| Monetization | Δ ≤ −0.5, or 3× premium, or (S3 and VIX ≥ 35); f = 50%; reset 40% | [I], optimize |
| Liquidity recognition φ | OTC 0.7; listed 0.85 | [I] |
| Opportunistic vol budget | 1.0–1.5% NAV; $DD^{max}$ = 2× budget | [I] |
| Sharpe prior | mean 0.3, sd 0.25 | [I] with [S] haircuts |
| Crowding jump | S3 intensity 0.5/yr, size −1.5 monthly σ | [I] |
| Futures IM | $\max(m^{floor},2.326\,\sigma_s\sqrt{5/252})$, i.e. ≈4% (S1), ≈10% (S3) | [I], calibrate to exchange margins |
| Schedule IM / haircuts | §2.5 | [S] |
| Secondary discount $d_s$ | 6 / 8 / 15 / 30% (S0–S3) | Anchored on 2025 13% and 2009 35% [S]; mapping [I] |
| Distribution penalty $\Pi_D$ | 1.0 per $ (or hard constraint) | IC-set |
| $\epsilon_L$, horizon | 1%, 36 months | Prior deck / [I] |

### 6.8 Calibration targets (the simulator must reproduce these)

- VIX: mean ≈ 19.4; p95 ≈ 33; share of days > 30 ≈ 8%.
- VRP: mean ≈ 4.1 vol pts; share of days positive ≈ 86%.
- HMM monthly persistence ≈ 0.66 / 0.44 / 0.47 / 0.61.
- SPX tail moves: 10-day p1 ≈ −8.5% and p0.1 ≈ −20%; 21-day worst ≈ −33%.
- PPUT: carry ≈ −2.8%/yr, COVID-window excess ≈ +22 pp.
- VXTH: COVID-window excess ≈ +61 pp, 2022 ≈ −5 pp.
- Long ATM puts: ≈ −7.4% p.a.
- Trend: positive in fast crises.
- IM response: a >100% IM jump within about 1 week of a VIX regime shift into S3.
- VM: VM ≫ ΔIM on peak days.
- Gilt-type rate shock: ≥250 bp.

### 6.9 Data needs

- **Overlay trades:** OTC blotter (instrument, strike, tenor, notional, counterparty, CSA terms, IA, thresholds, collateral eligibility).
- **Collateral history:** daily VM and IM history (for the HLBA and margin backtests); collateral inventory and encumbrance.
- **Market data:**
  - option surfaces for SPX/SX5E/NKY/HSI and the VIX futures and options term structure (OptionMetrics, Cboe DataShop, Bloomberg OVDV);
  - CDX spreads;
  - swaption and FX vols; oil vols.
- **Opportunistic book:** daily P&L by strategy, positions, margin, costs, and the full list of tested strategy variants (for the DSR's N).
- **Synthetic beta:** futures roll and TRS financing history.
- **From other streams:**
  - de-smoothed private betas;
  - DPI and call paths and secondary bids;
  - distribution rule and fiscal or oil linkage.

### 6.10 IC deliberation artifacts

1. **Defensive-stack frontier.** Annual carry (bp NAV) against Δ P(liquidity shortfall), Δ P(floor breach) and Δ P(10%), for no hedge, the Israelov baseline, puts only, trend only and stacks.
2. **Cost-per-crisis-$ league table**, by crisis type.
3. **Monetization playbook**, pre-approved.
4. **VM/IM heatmap** by scenario against the collateral pool and HLBA.
5. **Hedge-fatigue tracker**: cumulative carry against modeled value.
6. **Opportunistic evidence card**: posterior SR, DSR, crowding, capacity, crisis beta, λ-adjusted return.
7. **"What we are paying for" decomposition**: carry, liquidity, enabling, rebalancing.

---

## 7. Implementation notes

- **Libraries:**
  - numpy with numba or JAX for vectorized path simulation and Black–Scholes;
  - py_vollib_vectorized for fast implied vol;
  - QuantLib-Python for hybrids, SABR and calibration;
  - hmmlearn or statsmodels (MarkovRegression) for regimes;
  - arch for EWMA/GARCH and the skewed-t (SkewStudent);
  - cvxpy for per-step recourse and CVaR LPs (Rockafellar–Uryasev [nrv]);
  - Pyomo with HiGHS or Gurobi for scenario trees;
  - SDDP.jl (Julia) for SDDP;
  - Optuna, BoTorch or nevergrad (CMA-ES) for policy search;
  - PyTorch or JAX for deep hedging;
  - Open Source Risk Engine (ORE) with Python bindings for exposure, collateral and SIMM simulation [nrv; SIMM use requires an ISDA licence].
- **Complexity.** 50k paths × 36 months × 21 days ≈ 3.8×10⁷ path-days. Repricing about 200 options on every node is about 7.6×10⁹ Black–Scholes calls. Ways to cut this:
  - (i) full revaluation monthly, with delta–gamma–vega Taylor VM daily in between;
  - (ii) daily stepping only in S3 or large-move windows;
  - (iii) GPU batches, where 10⁹ Black–Scholes evaluations take seconds to minutes;
  - (iv) Chebyshev or neural surrogates for SIMM.
- **Rare events.** P(liquidity breach) is around 1%. Estimate it with importance sampling: tilt transitions toward S3 and reweight by likelihood ratios. Use common random numbers for policy comparisons.
- **Numerical pitfalls:**
  - arbitrage in parametric surfaces (check butterflies and calendars; deep-OTM extrapolation);
  - monthly steps understate peak VM, so use daily sub-steps or a Brownian-bridge extreme correction;
  - decision rules must use *filtered* regime probabilities, never Viterbi or smoothed ones (look-ahead);
  - HMM label switching;
  - T+1 VM settlement lags and weekend gaps;
  - currency of collateral versus exposure (8% FX haircut);
  - monetization rules are easy to overfit, so select with DSR/PBO on held-out regimes.

---

## 8. Risks, pitfalls and limitations

- **Basis and crisis-type risk.** VIX calls failed in 2022, duration hedges failed when the stock–bond correlation turned positive, and puts underpay in slow grinds. Diversify, and stress each crisis type.
- **Counterparty and wrong-way risk.** Dealers are stressed exactly when hedges pay (2008). Mitigate with a CSA, zero thresholds, cash VM, dealer diversification, and listed options for the core convexity.
- **Monetization liquidity.** Bid–ask widens in stress, and valuation disputes delay collateral. Hence haircuts on recognized liquidity (φ).
- **Procyclicality and look-backs.** IM rises after the shock, and the HLBA falls mechanically once crises leave the window. Keep a through-the-cycle floor.
- **Model risk in IV dynamics.** Spot–vol and skew behaviour differs across crises (S3 SKEW is lower than calm-state SKEW). Validate against Option C (§3.2).
- **Governance.** Hedge fatigue (CalPERS) and pro-cyclical cutting of budgets after long calm periods. Precommit and track cumulative carry.
- **Double counting and offsets.** Opportunistic short-vol against hedge long-vol pays dealer spreads twice. Aggregate net Greeks and scenario P&L at overlay level.
- **Crowding.** Short-vol unwinds (5 Feb 2018: VIX +115.6% in a day) and trend crowding.
- **Legal and UMR uncertainty.** IM obligations and collateral eligibility hinge on ADIC's status.
- **Sample limitations.** All empirical figures use US equity history with few independent crises. The cost-per-unit metric depends on index methodology and our dividend assumption. The HMM is fitted in-sample.
- **Fiscal linkage.** If distributions rise when oil falls, equity-only hedges mis-target the high-λ states.

---

## 9. Open questions

1. ADIC's regulatory status: sovereign entity or financial end user (US), and its EU/UK classification. Are there two-way IM obligations? What are the current CSA terms (thresholds, eligible collateral, reuse)?
2. The actual overlay: size, instrument mix, venues and dealer panel. Historical daily VM and IM, to calibrate the HLBA and margin models.
3. Is the distribution fixed in USD, set as a % of NAV, or linked to the owner's fiscal or oil position? What does the IC consider the penalty $\Pi_D$, and the penalty curvature σ (§2.3)?
4. May the opportunistic book run net short volatility? How will the opportunistic and hedge books be netted for governance?
5. Committed liquidity options: dealer repo lines, home-central-bank facilities, and the cost of committed facilities.
6. Correct de-smoothed private betas (from the PE stream), and whether synthetic beta should target "true" or "reported" exposure.
7. The hedge budget's governance: an IC-owned, precommitted line item, or embedded in Tier-2 optimization?
8. Should a fifth "extreme" regime or a jump layer be added, and how to validate tail calibration out of sample (non-US crises)?

---

## 10. References

**Sourced and fetched or verified in this session**

1. Harvey, C.R., Hoyle, E., Rattray, S., Sargaison, M., Taylor, D., Van Hemert, O. (2019). "The Best of Strategies for the Worst of Times: Can Portfolios Be Crisis Proofed?" *Journal of Portfolio Management* 45(5). https://people.duke.edu/~charvey/Research/Published_Papers/P140_The_best_of.pdf
2. Israelov, R. (2019). "Pathetic Protection: The Elusive Benefits of Protective Puts." *Journal of Alternative Investments*, Winter 2019 (AQR page dated 31 Dec 2018). https://www.aqr.com/Insights/Research/White-Papers/Pathetic-Protection-The-Elusive-Benefits-of-Protective-Puts
3. Israelov, R., Nielsen, L.N. (2015). "Still Not Cheap: Portfolio Protection in Calm Markets." *Journal of Portfolio Management* 41(4), 108–120. DOI 10.3905/jpm.2015.41.4.108. https://www.aqr.com/Insights/Research/Journal-Article/Still-Not-Cheap-Portfolio-Protection-in-Calm-Markets. CFA digest: https://rpc.cfainstitute.org/research/cfa-digest/2015/12/still-not-cheap-portfolio-protection-in-calm-markets-digest-summary
4. Hamill, C., Rattray, S., Van Hemert, O. (2016). "Trend Following: Equity and Bond Crisis Alpha." Man AHL working paper. https://www.man.com/maninstitute/trend-following-equity-and-bond-crisis-alpha
5. Hurst, B., Ooi, Y.H., Pedersen, L.H. (2017). "A Century of Evidence on Trend-Following Investing." *Journal of Portfolio Management* 44(1), 15–29 (Fall). DOI 10.3905/jpm.2017.44.1.015. https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
6. Moskowitz, T., Ooi, Y.H., Pedersen, L.H. (2012). "Time Series Momentum." *Journal of Financial Economics* 104, 228–250. https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf
7. Koijen, R., Moskowitz, T., Pedersen, L.H., Vrugt, E. (2018). "Carry." *Journal of Financial Economics* 127(2), 197–225, DOI 10.1016/j.jfineco.2017.11.002 (published version); NBER WP 19325. https://www.nber.org/papers/w19325; https://pages.stern.nyu.edu/~lpederse/papers/Carry.pdf
8. Harvey, C.R., Hoyle, E., Korgaonkar, R., Rattray, S., Sargaison, M., Van Hemert, O. (2018). "The Impact of Volatility Targeting." *Journal of Portfolio Management*, Fall. https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf
9. Moreira, A., Muir, T. (2017). "Volatility-Managed Portfolios." *Journal of Finance* 72(4), 1611–1644. https://www.nber.org/papers/w22208
10. Bailey, D.H., López de Prado, M. (2014). "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality." *Journal of Portfolio Management* 40(5), 94–107. DOI 10.3905/jpm.2014.40.5.094. https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
11. Bailey, D.H., Borwein, J., López de Prado, M., Zhu, Q.J. (2017). "The Probability of Backtest Overfitting." *Journal of Computational Finance* 20(4), 39–69 (first published 19 Sep 2016). DOI 10.21314/JCF.2016.322. https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf
12. Harvey, C.R., Liu, Y. (2015). "Backtesting." *Journal of Portfolio Management* 42(1), 13–28 (Fall 2015). DOI 10.3905/jpm.2015.42.1.013. https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF
13. Brunnermeier, M., Nagel, S., Pedersen, L.H. (2009). "Carry Trades and Currency Crashes." *NBER Macroeconomics Annual 2008*, 23. https://www.nber.org/papers/w14473
14. Khandani, A., Lo, A. (2011). "What Happened to the Quants in August 2007?" *Journal of Financial Markets* 14(1), 1–46. https://www.nber.org/papers/w14465
15. Bollerslev, T., Tauchen, G., Zhou, H. (2009). "Expected Stock Returns and Variance Risk Premia." *Review of Financial Studies* 22(11). https://public.econ.duke.edu/~boller/Published_Papers/rfs_09.pdf
16. Froot, K., Scharfstein, D., Stein, J. (1993). "Risk Management: Coordinating Corporate Investment and Financing Policies." *Journal of Finance* (NBER WP 4084). https://www.nber.org/papers/w4084
17. Bolton, P., Chen, H., Wang, N. (2011). "A Unified Theory of Tobin's q, Corporate Investment, Financing, and Risk Management." *Journal of Finance* 66(5), 1545–1578. https://www.nber.org/papers/w14845
18. Ang, A., Papanikolaou, D., Westerfield, M. (2014). "Portfolio Choice with Illiquid Assets." *Management Science* 60(11), 2737–2761. https://www.nber.org/papers/w19436
19. Dimmock, S., Wang, N., Yang, J. (2024). "The Endowment Model and Modern Portfolio Theory." *Management Science* 70(3), 1554–1579. https://www.nber.org/papers/w25559
20. Jeanne, O., Rancière, R. (2006). "The Optimal Level of International Reserves for Emerging Market Countries: Formulas and Applications." IMF WP/06/229. https://www.imf.org/external/pubs/ft/wp/2006/wp06229.pdf. Published version: Jeanne, O., Rancière, R. (2011). "The Optimal Level of International Reserves for Emerging Market Countries: A New Formula and Some Applications." *Economic Journal* 121(555), 905–930. DOI 10.1111/j.1468-0297.2011.02435.x.
21. Buehler, H., Gonon, L., Teichmann, J., Wood, B. (2018). "Deep Hedging." arXiv:1802.03042. https://arxiv.org/abs/1802.03042
22. Sepp, A., Lucic, V. (2026). "The Science and Practice of Trend-Following Systems." arXiv:2607.19497. https://arxiv.org/abs/2607.19497
23. FSB (2020). *Holistic Review of the March Market Turmoil*, 17 Nov 2020. https://www.fsb.org/wp-content/uploads/P171120-2.pdf
24. BCBS–CPMI–IOSCO (2022). *Review of Margining Practices*, 29 Sep 2022. https://www.bis.org/bcbs/publ/d537.htm
25. FSB (2024). *Liquidity Preparedness for Margin and Collateral Calls: Final Report*, 10 Dec 2024. https://www.fsb.org/2024/12/liquidity-preparedness-for-margin-and-collateral-calls-final-report/
26. FSB (2023). *The Financial Stability Aspects of Commodities Markets*, 20 Feb 2023. https://www.fsb.org/2023/02/the-financial-stability-aspects-of-commodities-markets/
27. Bank of England (2022). *Financial Stability Report*, December 2022. https://www.bankofengland.co.uk/financial-stability-report/2022/december-2022
28. Bank of England FPC (2023). *Financial Policy Summary and Record*, March 2023. https://www.bankofengland.co.uk/financial-policy-summary-and-record/2023/march-2023
29. Wikipedia, "September 2022 United Kingdom mini-budget" (BoE purchase and sale totals). https://en.wikipedia.org/wiki/September_2022_United_Kingdom_mini-budget
30. Basel Committee, Basel Framework LCR40 (in force 15 Dec 2019). https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30
31. 12 CFR §237.2, Regulation KK definitions. https://www.law.cornell.edu/cfr/text/12/237.2
32. Federal Register (30 Nov 2015). "Margin and Capital Requirements for Covered Swap Entities," final rule, Appendices A–B. https://www.govinfo.gov/content/pkg/FR-2015-11-30/html/2015-28671.htm
33. ISDA, ISDA SIMM infohub. https://www.isda.org/isda-solutions-infohub/isda-simm/
34. Barnes, C. (2020). "Margin Calls During COVID-19." Clarus FT, 15 Jul 2020. https://www.clarusft.com/margin-calls-during-covid-19/
35. Huang, W., Takáts, E. (2020). "The CCP-bank nexus in the time of Covid-19." BIS Bulletin 13. https://www.bis.org/publ/bisbull13.pdf
36. Cboe Global Indices, daily history files (VIX, VIX3M, VVIX, SKEW, SPX, PPUT, CLL, CLLZ, VXTH), accessed 2026-10-18. Pattern: https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv
37. Cboe (2021). "Benchmark Indices Series: Hedging Downside Exposure with PPUT, CLL and CLLZ Indices," 15 Jul 2021. https://www.cboe.com/insights/posts/benchmark-indices-series-hedging-downside-exposure-with-pput-cll-and-cllz-indices
38. Wikipedia, "Universa Investments." https://en.wikipedia.org/wiki/Universa_Investments
39. Institutional Investor (2020). "CalPERS' Abandoned Tail Hedge Starts a War of Words" (via search summary). https://www.institutionalinvestor.com/article/b1l7lrcp6tnwlm/CalPERS-Abandoned-Tail-Hedge-Starts-a-War-of-Words
40. Financial Planning (2020). "CalPERS missed a $1B payday by scrapping market hedge" (via search summary). https://www.financial-planning.com/articles/calpers-missed-a-1-billion-payday-by-scrapping-market-hedge-ahead-of-the-coronavirus-outbreak
41. Advisor Perspectives (6 May 2020). "An AQR Warning and a 3,612% Return Fire Up the Black Swan Debate" (via search summary; direct fetch returned 403). https://www.advisorperspectives.com/articles/2020/05/06/an-aqr-warning-and-a-3-612-return-fire-up-the-black-swan-debate
42. Wikipedia, "Private equity secondary market" (citing WSJ 2014; Jefferies *2025 Global Secondary Market Review*, 10 Feb 2026). https://en.wikipedia.org/wiki/Private_equity_secondary_market
43. Wikipedia, "Harvard Management Company" (citing NYT, Feb 2009). https://en.wikipedia.org/wiki/Harvard_Management_Company
44. NZ Super Fund, "Strategic tilting" and "Derivatives." https://www.nzsuperfund.nz/how-we-invest/actual-portfolio/how-we-add-value/strategic-tilting/; https://www.nzsuperfund.nz/how-we-invest/actual-portfolio/how-we-add-value/derivatives/
45. CXO Advisory, summary of Israelov (2017) PPUT statistics (via search summary). https://www.cxoadvisory.com/equity-options/do-protective-equity-index-puts-work-well/

**Cited from memory, not re-verified this session [nrv]; no URL given**

*[Citation corrections 2026-10-18: the literature check (`research/literature/09_overlay.lit.md`) has since confirmed 11 of these works: Browne; Carr & Wu; Coval & Shumway; Daniel & Moskowitz; Getmansky, Lo & Makarov; Grossman & Zhou; Hardy; Lo; Mohajerin Esfahani & Kuhn; Rampini & Viswanathan; Rampini, Sufi & Viswanathan. The corrections pass also checked Kaminski & Lo. Their missing titles, pages and DOIs are added below from Crossref records (Lo's pages from OpenAlex). Demeterfi et al., Gatheral & Jacquier, Rockafellar & Uryasev and the two books remain unchecked.]*

- Browne, S. (1999). "Reaching goals by a deadline: digital options and continuous-time active portfolio management." *Advances in Applied Probability* 31(2), 551–577. DOI 10.1239/aap/1029955147.
- Carr, P., Wu, L. (2009). "Variance Risk Premiums." *Review of Financial Studies* 22(3), 1311–1341. DOI 10.1093/rfs/hhn038.
- Coval, J., Shumway, T. (2001). "Expected Option Returns." *Journal of Finance* 56(3), 983–1009. DOI 10.1111/0022-1082.00352.
- Daniel, K., Moskowitz, T. (2016). "Momentum Crashes." *Journal of Financial Economics* 122(2), 221–247. DOI 10.1016/j.jfineco.2015.12.002.
- Demeterfi, K., Derman, E., Kamal, M., Zou, J. (1999). "A Guide to Volatility and Variance Swaps." *Journal of Derivatives* 6(4).
- Gatheral, J., Jacquier, A. (2014). "Arbitrage-free SVI volatility surfaces." *Quantitative Finance* 14(1).
- Getmansky, M., Lo, A., Makarov, I. (2004). "An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns." *Journal of Financial Economics* 74(3), 529–609. DOI 10.1016/j.jfineco.2004.04.001.
- Grossman, S., Zhou, Z. (1993). "Optimal Investment Strategies for Controlling Drawdowns." *Mathematical Finance* 3(3), 241–276. DOI 10.1111/j.1467-9965.1993.tb00044.x.
- Hardy, M. (2001). "A Regime-Switching Model of Long-Term Stock Returns." *North American Actuarial Journal* 5(2), 41–53. DOI 10.1080/10920277.2001.10595984.
- Kaminski, K.M., Lo, A.W. (2014). "When Do Stop-Loss Rules Stop Losses?" *Journal of Financial Markets* 18, 234–254. DOI 10.1016/j.finmar.2013.07.001.
- Lo, A. (2002). "The Statistics of Sharpe Ratios." *Financial Analysts Journal* 58(4), 36–52. DOI 10.2469/faj.v58.n4.2453.
- Mohajerin Esfahani, P., Kuhn, D. (2018). "Data-Driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations." *Mathematical Programming* 171(1–2), 115–166. DOI 10.1007/s10107-017-1172-1.
- Rampini, A., Viswanathan, S. (2010). "Collateral, Risk Management, and the Distribution of Debt Capacity." *Journal of Finance* 65(6), 2293–2322. DOI 10.1111/j.1540-6261.2010.01616.x.
- Rampini, A., Sufi, A., Viswanathan, S. (2014). "Dynamic Risk Management." *Journal of Financial Economics* 111(2), 271–296. DOI 10.1016/j.jfineco.2013.10.003.
- Rockafellar, R.T., Uryasev, S. (2000). *Journal of Risk* 2(3).
- Bhansali, V. (2014). *Tail Risk Hedging*. McGraw-Hill.
- Spitznagel, M. (2021). *Safe Haven*. Wiley.
- Commission Delegated Regulation (EU) No 153/2013, Art. 28 (CCP anti-procyclicality).
- Open Source Risk Engine (ORE).

**Added by the citation corrections of 2026-10-18 (metadata confirmed via Crossref)**

- Barroso, P., Detzel, A. (2021). "Do limits to arbitrage explain the benefits of volatility-managed portfolios?" *Journal of Financial Economics* 140(3), 744–767. DOI 10.1016/j.jfineco.2021.02.009.
- Cederburg, S., O'Doherty, M.S., Wang, F., Yan, X. (2020). "On the performance of volatility-managed portfolios." *Journal of Financial Economics* 138(1), 95–117. DOI 10.1016/j.jfineco.2020.04.015.
- Mihailov, A., Nasir, H. (2022). "Sudden Stops, Productivity and the Optimal Level of International Reserves for Small Open Economies." *Open Economies Review* 33(5), 825–851. DOI 10.1007/s11079-022-09678-2.

---

## Citation corrections (2026-10-18)

*Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.4 item 7 and §2.5; `research/literature/09_overlay.lit.md` (citation-integrity table and content flags); `research/literature/recheck/10_scenarios_robustness.recheck.md` (Carr & Wu). New metadata was confirmed via Crossref, and for ref 11 on the publisher's page.*

- §2.3, Jeanne & Rancière: added the published *Economic Journal* (2011) version and its benchmark of 9.1% of output beside the working paper's 10.1% (9.1% per Mihailov & Nasir 2022, unverified in the EJ text). The ADIC illustration and the IC lesson use neither figure and are unchanged.
- §2.6, Lo (2002): added the paper's headline result (serial correlation can overstate an annual Sharpe ratio "by as much as 65 percent"; √12 annualization holds only "under very special circumstances") beside the i.i.d. formula.
- §2.6, Moreira & Muir (2017): no longer cited as unqualified support for Sharpe gains from volatility scaling; the out-of-sample dispute (Cederburg et al. 2020; Barroso & Detzel 2021) is added. No parameter in §3.5 or §6 assumes a Sharpe uplift from vol scaling, so nothing downstream changes.
- §2.6, Kaminski & Lo (2014): checked (previously unchecked). "Add value only when returns are serially correlated" is replaced by the abstract's conditions (random walk: always lower expected return; price momentum: can add value); tag [nrv] → [S].
- §2.6, Daniel & Moskowitz (2016): scope added (cross-sectional momentum; bears on trend only by analogy).
- §4.7, Koijen et al.: in-text year 2018 added.
- §10 refs 3, 5, 10 and 12 (Israelov & Nielsen; Hurst, Ooi & Pedersen; Bailey & López de Prado, now with its full subtitle; Harvey & Liu): volume(issue), pages and DOI added.
- §10 ref 7 (Koijen et al., *Carry*): *Journal of Financial Economics* 127(2), 197–225 (2018), DOI 10.1016/j.jfineco.2017.11.002.
- §10 ref 11 (Bailey et al., PBO): *Journal of Computational Finance* 20(4), 39–69 (2017; online 19 Sep 2016), DOI 10.21314/JCF.2016.322.
- §10 ref 20: published version added, *Economic Journal* 121(555), 905–930 (2011), DOI 10.1111/j.1468-0297.2011.02435.x.
- §10 [nrv] list: status note added. Titles added for Getmansky–Lo–Makarov, Grossman & Zhou, Hardy, Kaminski & Lo, Mohajerin Esfahani & Kuhn, Rampini & Viswanathan and Rampini–Sufi–Viswanathan; pages and DOIs added for these and for Browne, Carr & Wu, Coval & Shumway, Daniel & Moskowitz and Lo.
- §10: new block with full entries for Barroso & Detzel (2021), Cederburg et al. (2020) and Mihailov & Nasir (2022).
- Checked, no change: the co-investment barrier (BGK) re-run affects no figure or formula here, and the only discrete-monitoring remark (§7, Brownian-bridge correction for monthly VM steps) already points the right way. Of the re-check results for streams 10, 11, 13, 14 and G3, only Carr & Wu applies (pages and DOI above).
