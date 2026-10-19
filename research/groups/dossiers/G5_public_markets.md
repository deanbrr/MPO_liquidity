# G5 · Public Markets group: hedge funds and long-only managers as return source and liquidity reservoir

*ADIC multi-period robust TPA framework · group stream G5 · prepared 2026-10-18 · market data dated where shown*

**Evidence labels.** **[S]** sourced fact read in this session (often at abstract level), with date. **[ss]** figure seen only in a search-engine result summary; the page itself was not opened. **[C]** practitioner consensus, not independently verified. **[I]** our inference, calculation or design choice. **[nrv]** recalled from memory and not re-verified; check before external use. **SYNTHETIC** marks defaults for the synthetic book. They are not ADIC data and must be labelled synthetic in every output.

**Process note.**
- The session-wide web-search quota ran out several times. Most evidence therefore comes from direct fetches of primary sources: the OFR Hedge Fund Monitor API (SEC Form PF aggregates), the Federal Reserve FSR, Lovdata (Norway's GPFG mandate), NBER and RePEc/IDEAS abstracts, arXiv, Cambridge Associates PDFs, BarclayHedge index pages and HFR-sourced trade press.
- Consensus (consensus.app) needed interactive authentication and was not used.
- Most journal full texts were paywalled. Magnitudes that do not appear in an abstract are marked [nrv].
- HFR's site terms restrict machine use, so HFRI figures come from press coverage of HFR releases.
- Every worked example can be reproduced with `research/groups/verification/G5_public_markets_examples.py` (fixed seed; output in `G5_public_markets_examples_results.json`).

---

## 1. Executive summary

1. **The group holds two reservoirs that behave differently.**
   - **Long-only ($36bn working, SYNTHETIC).** This is market liquidity: cash at T+1/T+2.
     - Square-root impact puts the all-in cost of selling a $1–5bn US large-cap basket at about 4–13bp, developed ex-US at about 9–23bp, EM at about 23–40bp, and US small cap at about 21–65bp [I, §4.9].
   - **Hedge funds ($20bn).** This is contractual liquidity: cash arrives on a schedule and is subject to manager discretion.
     - SEC Form PF aggregates for 30 Jun 2026 show 8.4% of hedge-fund NAV redeemable within 7 days, 27.3% in 8–90 days and 64.4% beyond 90 days [S: OFR]. The beyond-90-days share was 55.7% in 2013.
     - On that profile, ADIC's HF book yields about $1.7bn within a week and about $7.1bn within a quarter. With crisis gating the quarter figure falls to about $5.8bn [I].
   - **Implication:** hedge funds are a second-line source over 3–24 months. They cannot be relied on to fund distributions or variation margin (VM).

2. **Hedge-fund liquidity fails in the states where its shadow price λ is highest.**
   - 2008 net redemptions were $399bn, 20% of assets [S: Hennessee via Hedgeweek, Jan 2009]. December 2008 alone saw more than $100bn of redemption outflows [S: Paul Weiss/Bloomberg, Apr 2009].
   - Managers "liberally exercised" gates and suspensions [S: Cambridge Associates (CA), Jan 2009]. Secondary bids for gated interests reached discounts of up to 50% in extreme cases (Oct 2008). The Hedgebay index average was 79.8% of NAV in Dec 2009 [S: trade press].
   - About $100bn was still locked up in 2011 [S].
   - Redemptions crowd together:
     - Institutions redeemed hedge funds to meet private-fund capital calls [S: CA].
     - Gated funds pushed investors to redeem their best liquid funds instead [S: Hennessee].
     - The mere possibility of a gate triggers preemptive runs [S: Cipriani et al. 2014].
   - Hedge-fund positions therefore need a **liquidity-term state machine** with regime-conditional gate and suspension hazards and a pro-rata redemption queue (§6.5).

3. **Return model: factors plus option-like payoffs plus liquidity plus smoothing plus fat tails.**
   - The composite's crisis loss ratio to equities was about 0.5 in 2008 and Q1 2020, but about 0.2 in 2022's grind. Event-driven reached 0.78 in Q1 2020 [I from S].
   - Macro and trend were convex. HFRI Macro returned +9.3% in 2022. The Barclay CTA Index returned +14.1% in 2008 and +7.1% in 2022, but averaged only 1.9% a year over 2009–2025 [S; mean computed, I].
   - Smoothing with contemporaneous weight θ₀ = 0.85–0.55 understates volatility by 14–36% and inflates Sharpe ratios 1.16–1.55× [I, Getmansky–Lo–Makarov (GLM) algebra].

4. **The gross-to-net wedge is first-order.**
   - In 2024 the median management fee was 1.50% (2.00% for macro). Multi-manager pass-through expenses ranged 0.87–12.99% of NAV, with mean 5.93% and median 4.53% [S: CA, 10 Oct 2025].
   - The effective incentive fee has been about 50%, 2.5× the contractual rate [S: Ben-David, Birru & Rossi].
   - Investors in the largest pass-through multi-managers kept about 42% of gains [S: Barclays via Reuters, Aug 2024].
   - Dollar-weighted investor returns trail fund returns by 3–7% a year [S: Dichev & Yu].
   - Peer databases overstate returns. TASS hidden survivorship bias exceeded 5% a year over 1994–2001 [S: Aggarwal & Jorion].

5. **Multi-strategy platforms have shifted the risk.**
   - Their gross leverage (gross-asset-weighted) was 12.3× in Jun 2026, against 6.5× in Mar 2020 and 4.1× in 2013. Unencumbered cash fell from 26.8% to 20.3% of NAV [S: OFR].
   - The Fed describes hedge-fund leverage as "stable at record-high levels" [S: FSR, May 2026].
   - Investor-level gates stretch a full exit to 16–20 quarters [S: Bloomberg, Dec 2021].
   - ADIC reportedly leads a plan to put up to $15bn into leveraged HF strategies [S: press, 11 Jun 2026]. That sleeve needs its own state machine, a double-leverage stress and a 50–100% liquidity haircut (cross-link C3).

6. **Long-only managers deliver close to zero average net alpha, and their outperformance persists weakly.**
   - Alphas of 4,617 institutional products are statistically indistinguishable from zero [S].
   - About 75% of mutual funds have zero net alpha [S].
   - Plan sponsors hire after strong excess returns that then fail to persist [S: Goyal & Wahal].
   - Active fixed-income "alpha" is mostly credit beta [S: Brooks et al.].
   - So for most long-only mandates, the forgone return in REFINANCE is just the financing spread plus net alpha (which is between −fee and 0).

7. **Physical-to-synthetic is the cheapest non-cash liquidity in normal regimes, and a contingent liability in crises.**
   - **Market levels:**
     - S&P 500 implied financing averaged about 30bp over risk-free in 2021–23 and peaked above 140bp in Dec 2024 [S: D. E. Shaw].
     - It was +81bp over 3m SOFR at the Jun 2026 roll [S, via Stream 06], and about 200bp over fed funds on one metric on 26 Jun 2026 [S: Reuters].
     - Listed EUR financing via box spreads ran about 13bp over €STR [S: Eurex].
   - **Worked example ($5bn US large-cap mandate):**
     - It frees $4.1bn (82%) at about 0.4–0.7% a year in a normal regime and 0.8–1.1% in a Jun-2026-like regime.
     - In stress it frees only 55%, at 2.9–3.3% a year.
     - Comparators: about 5.8% a year for a NAV loan and about 4.6% for a 12%-discount secondary [I].
   - **The catch:** a −33% month turns the position into a $1.65bn VM call. It also consumes leverage capacity [I].

8. **Portable alpha is a valid LEVER only under two conditions:** alpha must be positive net of pass-through fees, and beta-leg margin must never depend on HF liquidity. In a −33% month, $2bn of futures beta needs about $0.78bn within days. A $2bn HF sleeve can return only $0.3–0.65bn within 90 days [I].

9. **Rebalancing.**
   - GPFG rebalances when the equity share deviates more than 2pp from 70%, tested at month-end [S: Lovdata].
   - Mechanical rebalancing is short convexity. A monthly-rebalanced 60/40 portfolio's maximum drawdown was 1.2× buy-and-hold's in 2007–09, while trend-aware "strategic rebalancing" improves drawdowns by 2–3pp [S: Man].
   - For ADIC: a λ-gated band on de-smoothed economic weights, executed synthetically first.

10. **Forecasts.**
    - The group's manager-alpha forecasts are structurally optimistic. Default priors are net α ≈ 0 for long-only and small positive for hedge funds.
    - Credibility on realised alpha after five years is about 0.36 for long-only and 0.47 for hedge funds [I].
    - Grade alpha, crisis-beta and liquidity forecasts separately. Benchmark hire/fire decisions against the "keep the fired manager" counterfactual (§6.14).

---

## 2. Core concepts and theory

### 2.1 Liquidity as a triple; two reservoirs
Define each holding's liquidity profile $\Lambda_i(h,s)=$ cash received within horizon $h$ when a full exit starts now in regime $s$, net of costs, at a chosen quantile [I]. It has three dimensions:
- **time-to-cash;**
- **haircut** (market impact, discount, fees);
- **probability**, meaning discretionary restrictions such as gates, suspensions, side pockets and in-kind payment.

The two halves of the group sit at opposite corners:
- **Long-only:** time ≈ 0, haircut grows with size and volatility, probability ≈ 1.
- **Hedge funds:** time = notice + dealing date + payment lag + gate deferrals; haircut ≈ 0 at NAV, though NAV may itself be stale or realised through fire sales; probability < 1 in stress.

Analogues from other fields:
- **Bank ALM:** the Basel counterbalancing-capacity ladder and LCR inflow rates (cross-links 06/09).
- **Insurance:** surrender charges and dynamic-lapse models. A soft lock-up fee is a surrender charge, and redemption waves are lapse spikes.

### 2.2 The hedge-fund return-generating process
- **Linear asset-based style factors.**
  - Fung & Hsieh's seven factors explain "up to 80 percent" of monthly variation for diversified hedge-fund portfolios [S: FAJ 2004]. The factors are equity, size spread, bond and credit-spread changes, and bond/FX/commodity trend factors.
  - An emerging-markets factor was added later [S: Hsieh data page].
- **Option-like payoffs.**
  - Equity-oriented strategies resemble short index puts. Mean-variance analysis underestimates their tail risk [S: Agarwal & Naik 2004].
  - Risk arbitrage behaves like selling uncovered index puts, with about 4% a year of excess return after costs [S: Mitchell & Pulvino 2001].
  - Trend followers resemble lookback straddles [S: Fung & Hsieh 2001]. Their convexity comes from long-horizon variance exceeding short-horizon variance [S: Dao et al. 2016].
- **Liquidity risk premium.** Funds with significant liquidity-risk loadings beat low-loading funds by about 6% a year over 1994–2008, but did badly in liquidity crises [S: Sadka 2010].
- **Contagion.** Worst returns are contagious across styles. Adverse liquidity shocks raise the probability; the named shocks include credit spreads, the TED spread, prime-broker stock prices and fund flows [S: Boyson, Stahel & Stulz 2010].
- **Measurement distortions.**
  - Reported returns are smoothed (GLM, 908 TASS funds) [S].
  - Lagged pricing hides beta. After correcting for it, the broad index added no value beyond its average market exposure over 1994–2000 [S: Asness, Krail & Liew 2001].
  - Small gains far outnumber small losses in reported returns, consistent with temporary overstatement [S: Bollen & Pool 2009].

**GLM smoothing.** Reported returns are a weighted average of true returns:

$$r^{o}_{t}=\sum_{k=0}^{K}\theta_k r_{t-k},\quad \theta_k\ge0,\ \sum\theta_k=1$$

This gives:

$$\sigma_o=\sigma\sqrt{\textstyle\sum\theta_k^2},\qquad \rho_1=\frac{\sum\theta_k\theta_{k+1}}{\sum\theta_k^2},\qquad \beta^{o}_{0}=\theta_0\beta$$

| θ profile [I, SYNTHETIC] | σ_o/σ | Sharpe inflation | Contemporaneous β/true β | ρ₁ (reported) |
|---|---|---|---|---|
| (1.0) macro/CTA | 1.00 | 1.00× | 1.00 | 0.00 |
| (0.85, 0.15) equity L/S | 0.86 | 1.16× | 0.85 | 0.17 |
| (0.70, 0.20, 0.10) event/credit | 0.74 | 1.36× | 0.70 | 0.30 |
| (0.55, 0.30, 0.15) illiquid credit/RV | 0.64 | 1.55× | 0.55 | 0.51 |

### 2.3 Redemption terms: real options and agency
- **Ang & Bollen (2010).** A redemption right is a real option.
  - A two-year lock-up with three-month notice costs about 1% of the initial investment for a CRRA-3 investor.
  - If the manager can suspend redemptions at will, the cost "can easily exceed 10%" [S].
  - Implication: **discretionary clauses are worth far more to the manager than lock-ups** [I].
- **Agarwal, Daniel & Naik (2009).** Funds with more discretion (longer lock-up, notice and redemption periods) perform better [S].
- **Hombert & Thesmar (2014).** Funds protected from withdrawals recover faster after a bad year and have more volatile returns [S].
- **Aragon (2007).** Lock-up funds earn higher returns because they can hold illiquid assets. The premium is about 4–7% a year [S: abstract, "approximately 4-7% per year higher", confirmed in the verification log, A31].
- **Teo (2011).** Among nominally liquid funds, high-inflow funds outperformed low-inflow funds by 4.79% a year. The effect is strongest when funds take liquidity risk and funding is tight. It is consistent with agency-driven liquidity risk-taking [S].
- **Aiken, Clifford & Ellis (2015).** Funds that imposed discretionary liquidity restrictions (DLRs) did not slow their sales of illiquid stocks, and they underperformed a control group. Their fund families later struggled to raise capital and cut fees [S].
- **Conclusion:** terms are priced, and gates do not reliably protect remaining investors.

### 2.4 Runs, queues and gates
- **Strategic complementarity.** Outflows are more sensitive to poor performance in funds holding illiquid assets. The effect vanishes when large investors dominate the shareholder base [S: Chen, Goldstein & Jiang 2010].
- **Gates trigger preemptive runs** [S: Cipriani, Martin, McCabe & Parigi 2014].
- **2008 evidence.**
  - Hedge funds sold about 29% of their aggregate equity portfolio in 2008 Q3–Q4, driven by redemptions and margin calls.
  - Hedge-fund investors withdrew about 3× as intensely after poor returns as mutual-fund investors [S: Ben-David, Franzoni & Moussawi 2012].
- **Gate mechanics** [S: Paul Weiss, Apr 2009]:
  - A fund-level gate (e.g., 20% of NAV) pays all requests pro rata.
  - Gates may be mandatory.
  - Investor-level gates cap each investor at 10–15% per dealing date.
  - Some documents force full payment after an investor has been gated 2–4 times.
  - Suspensions became common, and payment in kind or liquidating SPVs were used.
- **Queue algebra.** The queue behaves like a processor-sharing server with capacity $G_d=g\cdot NAV_d$. The payout ratio is $\pi_d=\min(1,G_d/R_d)$, where $R_d$ is total requests.
- **Reflexivity [I].** ADIC's own request is part of $R_d$. Where ADIC owns a large share of a fund, its redemption can trigger the gate.

### 2.5 The gross-to-net wedge
$$r^{net}_t=r^{gross}_t-m-e^{PT}_t-\kappa\big[V_t-\max(HWM_{t-1},\,H_t)\big]^+/V_{t-1}$$

| Symbol | Meaning |
|---|---|
| $m$ | Management fee |
| $e^{PT}$ | Pass-through expenses. At multi-manager platforms these are mostly compensation, charged "in addition to a fund level incentive fee", which exposes investors to netting risk [S: CA] |
| $\kappa$ | Incentive rate |
| $HWM$ | High-water mark |
| $H_t$ | Hurdle |

Asymmetry, return-chasing and the closure of underwater funds push the effective incentive rate to about 50% [S: Ben-David et al.].

### 2.6 Long-only active management
Active return decomposes as

$$r_p-r_b=\alpha+(\beta-1)(r_b-r_f)+\varepsilon,\qquad IR=\alpha/TE$$

By the fundamental law, IR ≈ IC·√breadth [nrv: Grinold–Kahn].

Evidence:
- Aggregate active equity closely tracks the market. Few funds cover their costs, but gross returns show skill in the tails [S: Fama & French 2010].
- Value added averages about $3.2m per fund per year. Skill shows up in fund size and fees rather than in gross alpha [S: Berk & van Binsbergen 2015].
- Returns to scale decrease at the industry level [S: Pástor, Stambaugh & Taylor].

Implication: a long-only mandate's portfolio role is **beta delivery plus a small, uncertain alpha option**. The beta can be held synthetically.

### 2.7 Synthetic exposure, REFINANCE and portable alpha
- **Futures pricing.** $F=S(1+r+s)-E[D]$, where $s$ is the spread to borrow against the index [S: D. E. Shaw]. A long future is the index financed at $r+s$.
- **REFINANCE.** Selling physical and holding futures or a total return swap (TRS) is "sell + buy on margin". This is the **REFI primitive** of Stream 08: exposure is unchanged and financing changes. It also raises economic leverage (C4 cap in 06/09).
- **Liquidity flows.** Cash is released now. VM equals the daily P&L, and IM rises with volatility (09 §2.5).
- **Portable alpha.** Return is $r_m+\alpha^{net}-s$.
  - The classic failure is an illiquid alpha sleeve at the moment beta margin is due [C, 09].
  - Pennsylvania SERS's fund-of-funds-based programme was the 2008 "poster child" [S: Institutional Investor, Dec 2008, headline level].

### 2.8 Rebalancing as control with negative convexity
- Rebalancing equals buy-and-hold plus a short straddle on relative performance. It magnifies drawdowns when assets diverge persistently [S: Granger et al. 2014, via Man 2020].
- Transaction costs create a no-trade region [nrv: Leland 1999; Davis–Norman 1990].
- Lock-ups with costly early sale create time-varying bands [S: Dimmock, Wang & Yang 2024, via 06].
- In control terms, this is a deadband (hysteresis) controller whose band width is set by costs and by the liquidity shadow price [I].

---

## 3. Methods and models: trade-offs

| Need | Options | Strengths | Weaknesses | Recommendation [I] |
|---|---|---|---|---|
| Manager returns | (a) Linear Fung–Hsieh 7/8-factor + residual; (b) regime-switching betas; (c) option factors (put, lookback straddle) + liquidity factor; (d) block bootstrap of manager history; (e) hierarchical Bayesian alpha | (a) transparent; (b, c) crisis behaviour; (d) keeps real tails; (e) small-sample discipline | (a) misses convexity; (d) bound to short, smoothed histories; (e) prior choice | Use (b)+(c) for factors, a skew-t residual, a contagion jump, (e) for alpha, and GLM smoothing on top |
| De-smoothing | GLM MLE on MA(K); Geltner (1993, *JRER*) AR(1) [nrv]; Kalman state space; summed lagged betas (Asness et al.) | GLM gives θ directly; Kalman handles missing data | Explosive when θ₀ is small; MA order choice | GLM with θ ≥ 0, Σθ = 1, K ≤ 2, θ₀ floored at 0.5 and shrunk to strategy priors |
| HF liquidity | Contractual ladder; ladder + stochastic gate hazard; Markov-modulated queue with other investors; agent-based run model; survival model for liquidation | Ladder is simple; the hazard+queue captures stress | Sparse gating data; behavioural parameters | **Hazard + queue state machine (§6.5)**, with a survival-model liquidation hazard |
| Liquidity waterfall | Priority heuristic; per-bucket LP/convex program; multistage SP | LP gives duals per horizon | Needs expected or quantile cash per bucket | Convex program per scenario (§6.8); duals feed the 08 MCL curve |
| Transaction costs | Square-root impact; Almgren–Chriss (2001) schedule [nrv]; dealer risk transfer or TRS "synthetic sale" | Square-root has a solid empirical basis | Y and V need ADIC data | Square-root with regime σ and V; risk-transfer quotes for > 5% of ADV |
| Rebalancing | Calendar; threshold; hybrid (GPFG); optimal no-trade band; trend-aware "strategic" | — | Mechanical rules are short convexity | λ-gated hybrid band, synthetic first (§6.9) |
| Forecast grading | MZ regression, CRPS/PIT, rank IC, hit rates, Brier, hierarchical credibility, false-discovery control | Proper scoring | Overlapping horizons; factor-model dependence | Stream 07 engine plus the group-specific metrics in §6.14 |

---

## 4. Empirical evidence and current market data

### 4.1 Hedge-fund performance in stress and recovery

| Window | HF composite | Strategy detail | Equities | Source |
|---|---|---|---|---|
| 2008 | HFRI FWC −19.03% (worst year; Sep −6.12%, Oct −6.44%; ~70% of YTD losses in the 6 weeks after Lehman) | Equity Hedge −26.03%, Distressed −20.77%, Convertible arbitrage −35.50% (YTD Nov) | S&P 500 TR −37.0% [nrv] | [S] InvestmentNews 16 Feb 2010; CA Jan 2009 |
| 2009 | +20.04% | Fund of Funds +11.16% | — | [S] InvestmentNews |
| Q1 2020 | HFRI FWC −9.4% | Equity Hedge −12.9%, Event Driven −15.3%, Macro +0.1% | S&P 500 −19.6% | [S] CA Q1-2020 update |
| 2022 | HFRI FWC −4.2%; capital $3.83trn | Macro +9.3%, HFRI 500 Trend +14.4%, Equity Hedge −10.2% | S&P 500 TR −18.1% [nrv] | [S] HFR releases via Mondo Visione, 10 and 20 Jan 2023 |
| 2025 | HFRI FWC +12.6% (best since 2009) | Equity Hedge +17.3%, Event Driven +11%; Macro +7.2% [ss] | — | [S] WealthBriefing 9 Jan 2026 |
| H1 2026 | +7.5% | Equity Hedge +9.6%, Event Driven +7.4%, Macro +6.1% (systematic +9.7%), RV +3.7% | — | [S] Hedgeweek 24 Jul 2026 |
| Mar–Apr 2026 | Barclay HF Index −3.53% / +4.41% | (a stress month: Stream 09 dates a VIX S3 episode 6 Mar–7 Apr 2026) | — | [S] BarclayHedge, as of 18 Oct 2026 |
| Sep 2026 | HFRI FWC −0.67% (est.), YTD +7.13% | Macro +2.7%, CTA +4.6%, Equity Hedge −1.9%, Multi-Manager/Pod Shop −0.9% | — | [ss] HFR via Connect Money |

**Crisis loss ratios** (HF loss ÷ equity loss) [I from S]:

| Episode | Composite | Equity Hedge | Event Driven |
|---|---|---|---|
| 2008 | 0.51 | — | — |
| Q1 2020 | 0.48 | 0.66 | 0.78 |
| 2022 | 0.23 | 0.56 | — |

Crisis betas depend on the type of crisis: the gap crashes of 2008 and 2020 versus the inflation grind of 2022.

**Trend and macro convexity.** Barclay CTA Index annual returns [S: BarclayHedge]:

| Year | Return |
|---|---|
| 1987 | +57.3% |
| 2008 | +14.09% |
| 2020 | +5.43% |
| 2022 | +7.13% |
| 2026 YTD | +8.69% |
| 2009–2025 mean | 1.89% (sd 3.79%) [I] |

Convexity is real but expensive to carry, consistent with 09's live Sharpe-ratio prior of about 0.3.

### 4.2 Industry size, leverage and liquidity (SEC Form PF via OFR, data to 30 Jun 2026, updated 16 Sep 2026)

**Investor liquidity**, % of NAV redeemable within each window [S]:

| Window | Jun 2026 | Dec 2022 | Mar 2020 | Mar 2013 |
|---|---|---|---|---|
| ≤ 7 days | 8.4 | 8.1 | 13.0 | — |
| 8–90 days | 27.3 | 29.5 | 30.8 | — |
| > 90 days | 64.4 | 62.4 | 56.2 | 55.7 |

**Portfolio liquidity**, % of gross assets that can be liquidated within each window, Jun 2026 [S]:

| Window | Share |
|---|---|
| ≤ 1 day | 41.2 |
| 2–7 days | 23.6 |
| 8–90 days | 15.9 |
| > 90 days | 19.3 |

**Leverage** (gross assets ÷ NAV) [S]:

| Strategy | GAV-weighted, Jun 2026 | GAV-weighted, Mar 2020 | GAV-weighted, Mar 2013 | NAV-weighted, Jun 2026 |
|---|---|---|---|---|
| Multi-strategy | 12.3 | 6.5 | 4.1 | 4.5 |
| Macro | 12.7 | 11.6 | 4.4 | 6.8 |
| Relative value | 23.3 | 23.3 | 18.2 | 8.1 |
| Equity | 2.7 | 1.7 | 1.9 | 1.8 |
| Credit | 2.3 | 2.5 | 2.1 | 1.7 |
| Managed futures | 4.3 | 1.6 | 1.1 | — |
| Event-driven | 1.6 | 1.6 | 1.6 | — |

**Unencumbered cash**, % of NAV [S]:

| Strategy | Jun 2026 | Mar 2020 |
|---|---|---|
| Multi-strategy | 20.3 | 26.8 |
| Macro | 35.1 | 43.9 |

**Other industry data** [S]:
- **Fed FSR (May 2026):**
  - Hedge-fund leverage was "stable at record-high levels" (Form PF data through Q3 2025).
  - Leverage is skewed towards the largest funds.
  - Basis-trade leverage fell, but swap-spread trades offset the decline.
  - Dealers in the March 2026 SCOOS reported hedge funds' use of leverage unchanged.
- **HFR (Q2 2026):** record capital of $5.6trn, up $409.3bn in the quarter ($364bn from performance, $45.2bn from inflows). In H1, managers above $5bn took $77.2bn of inflows, versus $2.2bn for small managers [S: Hedgeweek, 24 Jul 2026].

### 4.3 Fees
| Item | Value | Source |
|---|---|---|
| Median management fee, 2024 | L/S 1.50%, credit 1.50%, multi-strategy 1.50%, macro 2.00%, fund of hedge funds (FoHF) 0.95% | [S] CA, 10 Oct 2025 (159 funds) |
| Median discretionary expense ratio | 0.15–0.27% (FoHF 0.04%) | [S] CA |
| Multi-manager pass-through, 2024 | 0.87–12.99% of NAV; mean 5.93%, median 4.53% | [S] CA |
| Average fees, Q3 2022 | Management 1.35%, incentive 16.01%, the lowest since HFR began publishing in 2008 | [S] HFR via TheWealthAdvisor, 6 Jan 2023 |
| Effective incentive rate, 22 years, 5,917 funds | About 50% (2.5× contractual); investors kept about 36¢ of each $ earned above the risk-free hurdle | [S] Ben-David, Birru & Rossi (NBER w27454; RCFS 2026) |
| Investor share of gross gains | About 42% at the largest pass-through multi-managers (Barclays); multi-strategies retained 59% of earnings in 2023, against 46% two years earlier (BNP) | [S] Reuters/Kitco 2 Aug 2024; Hedgeweek 12 Feb 2025 |
| Examples, 2023 | Balyasny Atlas Enhanced 15.2% gross vs 2.8% net; ExodusPoint 8.4% pass-through; Citadel's three largest funds $12.5bn pass-through (2022–Sep 2024) | [S] Bloomberg (Form ADV) via Hedgeweek |
| Allocator willingness | 15% willing to pay pass-through fees, down from > 20% | [S] Goldman Sachs survey via Reuters 2024 |

### 4.4 Liquidity terms and stress behaviour
| Evidence | Value | Source |
|---|---|---|
| 2008 industry | Assets −$782bn (−39%) to $1.21trn; net redemptions $399bn (20%); performance −$382bn | [S] Hennessee via Hedgeweek, 21 Jan 2009 |
| Year-end 2008 redemption estimates | 20–25% of global capital; Morgan Stanley: 15–20% US, 25–30% Europe and Asia | [S] CA Jan 2009 |
| Named drivers | Fund-of-funds asset/liability mismatches; "capital calls in the institutional investment community"; rebalancing; switching to reopened top managers; discontent | [S] CA Jan 2009 |
| December 2008 | > $100bn of redemption outflows | [S] Paul Weiss/Bloomberg, Apr 2009 |
| Gates as a cause of redemptions elsewhere | Gates and side pockets on illiquid holdings led investors to redeem strong long/short funds instead | [S] Hennessee |
| Secondary market | Discounts "as high as 50 per cent in extreme cases" (Oct 2008); Hedgebay average 79.8% of NAV, range 56–97% (Dec 2009); Illiquid Asset Index 67% (Jul 2010); mid-2009 average discount about 8% after a 20% March peak [ss] | [S] FWR 23 Oct 2008; WealthBriefing 1 Feb 2010; Hedgeweek 25 Aug 2010 |
| Tail of the stock | About $100bn still locked in a "sliver" of funds | [S] InvestmentNews via HedgeCo, 30 May 2011 |
| 2026 analogue (semi-liquid credit) | Most managers capped redemptions at 5% of NAV after requests "well above 5%"; perpetual BDC redemptions exceeded inflows for the first time | [S] Fed FSR May 2026; cross-link G6 |

### 4.5 Multi-strategy liquidity terms
- **Bloomberg, 6 Dec 2021** [S]:
  - Citadel limits quarterly withdrawals to 6.25% "under certain circumstances", so a full exit takes 16 quarters unless a fee is paid.
  - Millennium raised $10bn for a fund that takes at least five years to exit. Its shorter-term fund held about a quarter of assets.
  - Point72 allowed 25% a quarter.
  - Schonfeld and Hudson Bay used fee breaks or mandatory multi-year classes.
- **2020 reporting** that Millennium capped withdrawals at 5% a quarter [ss].
- **Interpretation [I]:** platform liquidity is a fixed amortisation schedule. It does not respond to the market regime.

### 4.6 Database biases, persistence and alpha decay
| Finding | Source |
|---|---|
| Hidden survivorship from the 1999–2001 Tremont–TASS merger: about 60% of added funds were survivors; bias > 5% a year over 1994–2001 | [S] Aggarwal & Jorion 2010 |
| Backfill and survivorship "may be far greater" than earlier estimates | [S] Malkiel & Saha 2005 |
| Classic estimates: survivorship ≈ 3% a year, instant-history (backfill) ≈ 1.4% a year; funds of funds proposed as a cleaner aggregate | [nrv] numbers; [S] FoF proposal: Fung & Hsieh 2000 |
| FoF alpha only Oct 1998–Mar 2000; alpha producers attract inflows that erode alpha | [S] Fung, Hsieh, Naik & Ramadorai 2008 |
| Inflows preceded alpha declines in 4 of 8 strategies (1995–2004) | [S] Naik, Ramadorai & Stromqvist 2007 |
| Capacity constraints confirmed with secondary-market demand data | [S] Ramadorai 2013 |
| Persistence among superior funds; little among inferior ones | [S] Jagannathan, Malakhov & Novikov 2010 |
| Dollar-weighted returns 3–7% a year below buy-and-hold; investor alpha ≈ 0 | [S] Dichev & Yu 2011 |

### 4.7 Long-only evidence
| Finding | Source |
|---|---|
| 4,617 institutional products (1,448 firms, 1991–2008): four-factor alphas ≈ 0; persistence weak to none | [S] Busse, Goyal & Wahal 2010 |
| 3,400 plan sponsors (1994–2003) hire after large positive excess returns, which do not continue; fired managers do as well as new hires | [S] Goyal & Wahal 2008 |
| About 75% of funds are zero-alpha net; the skilled share fell to almost none by 2006 | [S] Barras, Scaillet & Wermers 2010 |
| Active fixed-income returns are mostly passive risk-premium (credit) exposure | [S] Brooks, Gould & Richardson 2020 |
| Consultant-recommended products (US active equity): "no evidence that these recommendations add value" | [S] Jenkinson, Jones & Martinez 2016 (abstract confirmed in the verification log, A32) |
| Only about a fifth of top-quintile large-cap managers outperformed again over the following 12 years (eVestment, data to Sep 2025) | [ss] AllianceBernstein |

### 4.8 Implied financing for physical-to-synthetic (2024–2026)
| Market | Level | Source |
|---|---|---|
| S&P 500 futures | About 30bp over risk-free on average in 2021–23; > 140bp peak in Dec 2024 (20-day average) | [S] D. E. Shaw, c. 23 Jan 2025 |
| S&P 500 futures, Jun 2026 roll | +81bp over 3m SOFR, the richest June roll since at least 2007; +38bp in Q2 2025 | [S] CME, via Stream 06 verification (search excerpt) |
| US equity financing | About 200bp over fed funds on 26 Jun 2026 (highest since Dec 2024), then 89bp on a quarterly-maturity metric; dealer equity financing about $211bn; market about $10trn | [S] Reuters via Kitco, 9 Jul 2026 |
| EUR listed financing | EURO STOXX 50 3m box-spread yield 223bp vs €STR 210.1bp (2 Jan 2025–31 May 2026), i.e. +12.9bp; typically "12–20 basis points above €STR". This is a near-risk-free benchmark, not equity repo | [S] Eurex, Jun 2026 |
| MSCI EM/EAFE total return futures (TRFs) | Buyer pays SOFR + spread, quoted ± in bp; current levels not verified | [ss] ICE |
| Base rates | SOFR 3.89% (15 Oct 2026); 10y UST 5.09% (16 Oct 2026) | [S] via Stream 06 verification |

### 4.9 Execution costs
- **Square-root law** [S: Tóth et al. 2011]: $\Delta(Q)=Y\sigma\sqrt{Q/V}$ with $Y$ "of order unity". It holds from about $10^{-4}$ to a few percent of daily volume.
- **Live costs.** Trading costs from $1.7trn of live trades are "an order of magnitude smaller" than earlier studies suggested [S: Frazzini, Israel & Moskowitz 2018].
- **Our estimates** [I, SYNTHETIC; assumptions: V and σ as listed, plus spread, fees and sell taxes]:

| Basket ($bn) | ADV assumed | σ_daily | $1bn | $2bn | $5bn |
|---|---|---|---|---|---|
| US large cap | $400bn | 1.0% | 4–7bp | 5–9bp | 7–13bp |
| Developed ex-US | $150bn | 1.0% | 9–13bp | 11–17bp | 14–23bp |
| EM (incl. ~12bp taxes) | $150bn | 1.2% | 23–28bp | 25–32bp | 29–40bp |
| US small cap | $40bn | 1.6% | 21–33bp | 26–44bp | 36–65bp |

- **Duration.** Under the square-root law, impact depends on Q relative to daily volume, not on how long execution takes. Spreading a trade lowers neither expected impact nor cost much, and it adds timing risk [I].
- **Realised example.** An EM transition realised 48bp against a 38bp ± 64bp ex-ante estimate [ss: PGIM].

---

## 5. Practitioner and peer practice: case studies
1. **2008: the reservoir drains to fund capital calls.**
   - Institutions redeemed hedge funds to meet private commitments, while gates trapped their illiquid holdings [S: CA; Hennessee].
   - Lesson [I]: ADIC's own waterfall (PE calls → HF redemptions) is a crowded trade in the states where it matters. Price it with queue dynamics, not contractual terms.
2. **Platform terms after 2021.** Multi-year investor-level gates in exchange for steady returns [S: Bloomberg].
   - Lesson [I]: contractually, a multi-strategy allocation sits closer to a 4–5-year amortising note than to a liquid asset. It should never be counted in 90-day liquidity beyond its scheduled tranche.
3. **Pass-through economics.** Balyasny's 2023 return was 15.2% gross and 2.8% net [S].
   - Lesson [I]: underwrite on net-of-all-fees alpha, with a pass-through cap or fee budget.
4. **Portable alpha in 2008.** Pennsylvania SERS combined funds of hedge funds with beta overlays [S: II headline].
   - In 2025, Iowa PERS reportedly allocated $2.3bn to a portable-alpha programme, with absolute-return managers including AQR Helix and Brevan Howard [ss].
   - Lesson [C/I]: the beta leg's collateral must be HQLA, never the alpha sleeve.
5. **GPFG rebalancing.** There is a rules-based trigger: deviation > 2pp from the 70% equity share at the last trading day of the month (§1-6 of the mandate). Details are set by the Ministry [S: Lovdata, mandate last amended 5 Oct 2026].
   - The relative-risk limit is an expected tracking error ≤ 1.25pp (§2-4(6)). NBIM's internal mandate adds an annualised relative ES(97.5%) limit of 3.75% (amended 9 Dec 2025) [S].
6. **Sovereign redemption waves.** Sovereign wealth funds pulled ≥ $46.5bn from asset managers in 2015 [S: via Stream 03]. Owner-driven liquidity needs hit external managers in falling markets, which is the same mechanism as case 1.
7. **ADIC press context.** ADIC reportedly leads a plan to deploy up to $15bn in leveraged HF strategies, in support of its >10% long-term goal [S: Jawlah, 11 Jun 2026, citing Bloomberg]. Structure and terms are not public; we make no inference about internal matters.

---

## 6. Design implications for the ADIC framework

### 6.1 Placement
- **Public Markets Engine.** Deterministic code with four modules:
  - Manager Return Model;
  - Liquidity-Term State Machine;
  - Execution and Synthetic Replacement;
  - Rebalancing and Waterfall.
- **Interfaces.** It emits per-path cash flows to the liquidity ledger (09 §6.4E, G7 ladder). It emits per-holding action bundles to the Stream 08 pricer.
- **Time steps.** Decisions are quarterly; the engine steps monthly, with daily sub-steps around dealing dates and in VIX-stress months (C1 conventions).
- **Regimes.** Master regime $S_t\in\{$EXP, LATE, CRIS, RECV$\}$ (Stream 10), with VIX labels $V_t$ from 09 for margin.

### 6.2 State variables (per holding $i$, path, month $t$)
- **Market and manager:**
  - true and reported NAV $(V_{i,t},V^{o}_{i,t})$, smoothing buffer $(r_{i,t-1},r_{i,t-2})$;
  - high-water mark $HWM_{i,t}$ and accrued incentive;
  - posterior alpha $(\hat\alpha_{i,t},\hat s_{i,t})$;
  - fund AUM $A_{i,t}$ (capacity) and ADIC's share of the fund $\omega_{i,t}$.
- **Liquidity:**
  - state $X_{i,t}\in\{$LOCK, SOFT, OPEN, NOTICE, QUEUE, SUSP, PAY, SP, LIQ, DONE$\}$;
  - outstanding request $q_{i,t}$; times gated $k_{i,t}$; receivables by date; holdback; side-pocket units $U^{SP}_{i,t}$;
  - others' request backlog $R^{oth}_{i,t}$.
- **Synthetic:**
  - replacement notional $N^{syn}_{i,t}$ per benchmark;
  - IM; VM buffer; financing spread state $f_{b,t}$.
- **Group:**
  - economic weights (de-smoothed privates, from 04/07) vs targets;
  - group liquidity ladder $\Lambda^{PM}(h,s)$.

### 6.3 Decision variables (quarterly)
- Redemption notices $u^{red}_{i,t}\in[0,1]$, including pre-emptive notices where rescindable.
- Secondary sale $u^{sec}_{i,t}$.
- Long-only sale $u^{sell}_{i,t}$.
- Physical-to-synthetic $u^{p2s}_{i,t}$, and reversal $u^{s2p}_{i,t}$.
- Synthetic beta add $b_{t}$ (overlay).
- Portable-alpha overlay $N^{PA}_{i,t}$ on alpha sleeve $i$.
- HF leverage $\ell^{HF}_{i,t}$ (financing against HF units, or levered share classes).
- New allocations and hires $a_{i,t}$; terminations.
- Rebalancing band $\delta$ and execution mode.

### 6.4 Return equations (monthly)

**Hedge fund, true return:**

$$r_{i,t}=r_{f,t}+\boldsymbol\beta_{i,S_t}^{\top}\mathbf F_t+\gamma_i\,P_t+\alpha_{i,t}+\sigma_{i,S_t}\,\epsilon_{i,t}+J_{i,t}$$

| Term | Specification |
|---|---|
| $\mathbf F_t$ | Fung–Hsieh 8 factors (equity, size, Δ10y, Δcredit spread, EM, three trend lookback-straddle factors) plus a liquidity factor |
| $P_t$ | Out-of-the-money (OTM) index-put return (Agarwal–Naik); $\gamma_i<0$ for short-put strategies |
| $\epsilon$ | Hansen skew-t$(\nu_i,\lambda_i)$ |
| $J_{i,t}$ | Crowding or contagion jump, Bernoulli$(p^J_{S_t})\times(-k_i\sigma_i)$ |

**Alpha decay:**

$$\alpha_{i,t}=\alpha_{i,0}\,e^{-\delta\,age}\,(A_{ref}/A_{i,t})^{\eta}$$

**Reported return.** Apply GLM to $r_{i,t}$, then the fee waterfall (§2.5). Gross is simulated and net is reported.

**Long-only:**

$$r_{i,t}=r_{b,t}+(\beta_i-1)(r_{b,t}-r_f)+\alpha_i+TE_i\,\epsilon_{i,t}$$

Fixed-income mandates carry an extra credit-beta term $\beta^{cr}_i\,(r^{cr}_t)$, because their reported alpha is largely credit beta (Brooks et al.).

### 6.5 Liquidity-term state machine (per HF lot)

**Terms vector**

$$\tau_i=\{freq,\,n,\,L,\,lock\_type,\,\phi^{soft},\,g,\,mandatory,\,\gamma^{inv},\,K^{max},\,h,\,p,\,sp^{max},\,susp,\,PIK\}$$

| Symbol | Meaning |
|---|---|
| freq | Redemption frequency |
| $n$ | Notice days |
| $L$, lock_type | Lock-up end and type |
| $\phi^{soft}$ | Soft-lock fee |
| $g$ | Fund-level gate (% NAV per dealing date) |
| mandatory | Mandatory-gate flag |
| $\gamma^{inv}$ | Investor-level gate (fraction of the balance at the first redemption date, per date) |
| $K^{max}$ | Maximum number of times an investor can be gated |
| $h$ | Holdback until audit |
| $p$ | Payment lag |
| $sp^{max}$ | Side-pocket allowance |
| susp | Suspension clause |
| PIK | Payment-in-kind or SPV clause |

**Steps at each dealing date $d$:**

1. **Others' requests.**
$$R^{oth}_{i,d}=NAV_{i,d}\,\mathrm{clip}\big(\rho_{S}+\rho_1[-r^{rel}_{i,\,d-2q:d}]^{+}+\rho_2\,\mathbb 1\{\hat p^{gate}_{i,d}>p^{*}\},\,0,\,1\big)$$
   The last term is preemption. Unpaid requests carry forward.

2. **Gate.** Let $R_d=q^{ADIC}_{i,d}+R^{oth}_{i,d}$.
   - If $R_d>g\,NAV_d$, a gate is imposed: always if mandatory, otherwise with probability $p^{gate}_{i,d}$.
   - The hazard is
$$\mathrm{logit}\,p^{gate}_{i,d}=a_{c(i),S}+b_1DD^{3m}_i+b_2R^{oth}_{i,d}/NAV+b_3M_i+b_4(Lev_i-1)$$
   - $M_i$ is the mismatch: investor liquidity within 90 days minus portfolio liquidity within 90 days, using OFR definitions.

3. **Payout.**
$$Pay^{ADIC}_{i,d}=\min\Big(q\,\pi_d,\ \gamma^{inv}B^{0}_i\Big),\qquad \pi_d=\min\big(1,\,gNAV_d/R_d\big)$$
   - Set $k\mathrel{+}=1$ if gated. Pay in full once $k=K^{max}$.

4. **Suspension.** Occurs with probability $p^{susp}_{i,d}$. Duration is geometric with mean $D_S$. A share $\varsigma$ of suspensions ends in LIQ.

5. **Side pocket.** Occurs with probability $p^{sp}_{c,S}$. A fraction $sp\le sp^{max}$ of NAV moves to SP. SP pays cash with quarterly hazard $\psi_S$ at a recovery $\mu^{SP}$ of carried value.

6. **Cash.** $(1-h)Pay$ arrives at $d+p$. $h\cdot Pay$ arrives after the audit (fiscal year-end + about 90 days [C]). A soft-lock exit pays $(1-\phi^{soft})$.

7. **Liquidation.** The hazard is a logit of drawdown, flows and regime (survival model). Cash schedule (SYNTHETIC [I]):

| Within | Share of NAV |
|---|---|
| 3 months | 50% |
| 12 months | 30% |
| 36 months | 20% |

   Recovery is 0.85–1.0 of last NAV.

**Default gate/suspension probability per quarter** (SYNTHETIC [I]; calibrate to ADIC documents and 2008/2020 history):

| Strategy class | EXP | LATE | CRIS (first two quarters) | RECV |
|---|---|---|---|---|
| Macro / CTA | 0.1% | 0.2% | 1% | 0.2% |
| Equity L/S | 0.2% | 0.4% | 4% | 0.5% |
| Multi-strategy (fund-level; investor gates are contractual) | 0.1% | 0.2% | 3% | 0.3% |
| Event-driven | 0.3% | 0.6% | 10% | 1% |
| Credit, RV/FI arbitrage, FoHF | 0.5% | 1% | 20% | 2% |

**Other defaults** (SYNTHETIC [I]):

| Parameter | Value | Anchor |
|---|---|---|
| Others' requests $\rho_S$, % of NAV per quarter | EXP 3, LATE 4, CRIS 15, RECV 6 | Year-end 2008: 20–25% of capital |
| Side-pocket creation, credit/event/RV in CRIS | 10% per quarter, 10–30% of NAV | — |
| Suspension mean duration | 3 quarters | 2–3-year work-outs [ss] |

**Sanity check.** A two-quarter crisis gates about 36% of illiquid-strategy funds. With about 40% of NAV in illiquid strategies, 30% in equity L/S and multi-strategy, and 30% in macro/CTA, that puts roughly 17% of the book gated, with a tail that is still locked years later. This is consistent in order of magnitude with 2008 [I].

**Ledger recognition.** $\varphi_i(h,S)$ is the 5th-percentile cash received within $h$, as a share of NAV, simulated by the machine. Stream 07/G7 ladders consume $\varphi$. G7's bucket caps then become outputs rather than inputs.

### 6.6 Group cash-flow equations
**Group cash flow per month:**

$$CF^{PM}_t=\sum_i\Big[Pay^{cash}_{i,t}+SP_{i,t}+LIQ_{i,t}\Big]+\sum_j u^{sell}_{j,t}V_{j,t}\big(1-c_j(Q,S)\big)-\sum_k a_{k,t}+\sum_m\Big[u^{p2s}_{m,t}V_m(1-c_m)-\Delta IM_{m,t}+VM_{m,t}-f_{m,t}N^{syn}_{m,t}\Delta t\Big]$$

**Impact cost:**

$$c_j(Q,S)=Y\sigma_S\sqrt{Q/V_S}+\tfrac12 spread_S+tax_j$$

In CRIS, $\sigma$ and spreads are 2–3× normal [I].

**Rule [I].** Transfers between ADIC groups are never counted as liquidity raised.

### 6.7 SELL / HOLD / REFINANCE / LEVER: definitions and economics
All actions are priced in Stream 08's currency:

$$\mathrm{Score}(i,a)=\sum_{s,t}\pi_{s,t}\Delta CF_{s,t}-\lambda_R\Delta CVaR-\lambda_{Lev}\Delta Lev-\sum_k\rho_k\Delta Floor_k-\kappa$$

Here $\bar\ell$ is the life-weighted liquidity premium.

| Action | Hedge funds | Long-only | Choose when [I] |
|---|---|---|---|
| **HOLD** | Keep | Keep | Default |
| **SELL** | Redeem through the state machine; or secondary sale at $(1-d^{HF}_S)$ | Liquidate with impact $c_j$; or move in kind to passive | **Redeem:** $\hat\alpha^{net}_i+\kappa^{reentry}_i<\bar\ell_{T^{cash}}$. Cash arrives at $T^{cash}$, so it is the *future* λ that matters. Notices are options: ladder them early when rescindable. **Secondary:** $(1-d^{HF}_S)$ ≥ the λ-priced value of the redemption schedule. |
| **REFINANCE** | Borrow against HF units (LTV by liquidity class); or redeem and replicate the HF's factor betas with futures (keeps β, loses α) | **Physical-to-synthetic:** sell physical (or transfer to a TRS dealer) and hold futures/TRS. Exposure is unchanged and the financing source changes | $\bar\ell\ge\bar f+\hat\alpha^{net}_i+\frac{c^{sell}+c^{rebuy}}{\tau}+\lambda_{Lev}\frac{N}{NAV}+\kappa^{VM}$, where $\kappa^{VM}=\frac{1}{N\tau}\sum_{s,t}\pi_{s,t}\ell_{s,t}E[VM^-_{s,t}+\Delta IM^+_{s,t}]$ |
| **LEVER** | Portable alpha (HF + futures beta); levered HF exposure (financing, levered class, TRS on NAV) | Synthetic beta add; extension strategies | Portable alpha: $E[\hat\alpha^{net}_{HF}]-\bar f>\lambda_R\Delta CVaR+\lambda_{Lev}\Delta Lev+\kappa^{VM}+\kappa^{mis}$, where $\kappa^{mis}$ charges P(gate∣CRIS)×(VM need − HF cash available). Beta add: $ERP_S-f_S>$ the same charges |

**HF secondary discount $d^{HF}_S$** (SYNTHETIC [I], anchored on [S] Hedgebay):

| Holding / regime | Discount |
|---|---|
| Liquid funds, normal | 0–5% (redeem instead) |
| Quarterly funds, CRIS | 15–25% |
| Gated or side-pocketed, CRIS | 30–50% |

**Worked example: REFINANCE a $5bn US large-cap mandate** (SYNTHETIC [I]; fee 25bp; round-trip cost 16bp over 2 years; IM 6/8/12%; VM buffer 11.7% normal, the 21-day p1 [S: Stream 09], or 33% stress, the worst 21-day):

| Regime | f | Cash freed | Cost, % a year of cash freed (α_net = −fee … 0) |
|---|---|---|---|
| Normal | 50bp | $4.1bn (82%) | 0.40–0.70% |
| Jun-2026-like | 81bp | $4.0bn (80%) | 0.80–1.11% |
| Stress | 175bp | $2.75bn (55%) | 2.87–3.33% |

- Comparators: about 5.8% a year for a NAV loan (SOFR+545bp mid, plus fee) and about 4.6% for a 12%-discount LP secondary amortised over 3 years [I; inputs from 06/08].
- REFINANCE through the overlay therefore ranks as step 3 on the 08 MCL curve in normal regimes, with the regime-dependent costs above.

**Portable-alpha stress check** [I]: $2bn of beta in a −33% month needs $0.66bn of VM plus $0.12bn of extra IM, or $0.78bn within days. A $2bn HF sleeve marks down about $0.2bn and can return $0.65bn, $0.52bn or $0.32bn within 90 days for P(gate) = 0, 0.2 or 0.5.

### 6.8 Liquidity waterfall (which managers to redeem first)
For each scenario node, solve a convex program [I]:

$$\min_{x,y\ge0}\sum_i\Big[\hat\alpha^{net}_i\tau_i x_iV_i+C_i(x_iV_i)+\phi_i x_iV_i+\kappa^{reentry}_i z_i\Big]+\sum_m\big(\bar f_m+\kappa^{VM}_m\big)y_m$$

subject to:
- **Cumulative cash per bucket:** $\sum_i\varphi_i(h_b)x_iV_i+\sum_m(1-m_m-b_m)y_m\ge Need^{PM}_{b}$ for $b\in\{7d,30d,90d,1y\}$.
- **Exposure drift:** $|\sum_i\beta_ix_iV_i-\sum_m y_m|\le\delta^{\beta}$.
- **Concentration:** ADIC share of a fund after the trade $\le\bar\omega$.
- **Leverage:** synthetic notional fits within the gross-exposure cap.
- **Re-entry indicator:** $z_i\ge x_i$, binary only in the MILP variant.

Other details:
- $C_i\propto Q^{1.5}$ is convex (power cone or piecewise linear).
- The duals per bucket are the **group's marginal cost of liquidity by horizon**, and they feed 08's MCL curve.

Default priority this tends to produce:
1. Treasury cash above the floor.
2. Overlay physical-to-synthetic on long-only beta.
3. Passive or enhanced-index sleeves.
4. Lowest-posterior-alpha long-only mandates.
5. Short-notice, ungated HFs with low posterior alpha. Lodge notices early for quarterly funds.
6. Never break up capacity-constrained top managers, which carry a high $\kappa^{reentry}$.
7. Secondary sales of HF interests only for gated or illiquid interests when λ is high.

The program explicitly penalises the 2008 pattern of redeeming the best liquid funds [S: Hennessee].

### 6.9 Rebalancing policy
- **Trigger.** Monthly test on **economic** weights (de-smoothed privates). Band $\delta=2$pp (GPFG-style) around the liquid-equity target.
- **Step 1.** Re-centre with overlay futures. The cost is $f$; VM is covered by the C2 collateral rule.
- **Step 2.** Physical execution over 1–3 months.
- **λ-gate.** Risk-adding rebalances proceed only if $\ell_t<\ell^{*}$, or synthetically with VM coverage.
- **Option to test.** Man-style trend delay: postpone equity-buying rebalances while the 12-month stock-bond trend is negative.
- **Evaluation.** Score the policy in simulation on drawdown, P(10%) and forced-sale probability [I].

### 6.10 Constraints and objective terms (group level)

| ID | Constraint |
|---|---|
| C-PM1 | Ladder: $\sum_i\varphi_i(h,\mathrm{CRIS},P5)V_i\ge Need^{PM}(h)$ at 7d, 30d, 90d and 1y. This is the group's share of the Distribution & Collateral Reserve (C3) |
| C-PM2 | ADIC share of any fund $\le$ 10–20% (reflexive gate risk) [I] |
| C-PM3 | Synthetic notional (REFINANCE and LEVER) counts in the gross-exposure cap and in λ_Lev (06/09) |
| C-PM4 | Beta-overlay IM plus the 99% 10-day VM are backed by unencumbered HQLA. HF NAV never counts (09 C2) |
| C-PM5 | Fee budget: pass-through capped, or $\hat\alpha^{net}\ge$ hurdle |
| C-PM6 | Minimum convex (trend/macro) allocation if the IC places it in the defensive stack (09) |
| C-PM7 | Rebalancing band |

**Objective contributions:**
- returns net of all fees;
- liquidity costs via the duals;
- execution costs;
- CVaR of time-to-cash shortfall;
- concentration penalties.

### 6.11 Parameter defaults (SYNTHETIC; sources and rationale shown)

**Hedge-fund strategies** [I unless noted; betas anchored on §4.1 ratios, fees on CA, terms on §4.4–4.5]:

| Strategy | β_eq (EXP/LATE) | β_eq (CRIS) | Residual σ (ann.) | ν, skew | θ (GLM) | Net α prior: mean (sd) | Fees: management / pass-through or expense ratio / incentive (%) | Default terms |
|---|---|---|---|---|---|---|---|---|
| Multi-strategy platform | 0.10 | 0.30 | 4% | 5, −0.3 | (0.90, 0.10) | 2.0% (2.5%) | 0–1.5% / 4.5% (0.9–13%) / 20% | Quarterly; 60–90d notice; investor gate 1/16–1/20 per quarter |
| Equity L/S | 0.45 | 0.65 | 7% | 5, −0.2 | (0.85, 0.15) | 0.5% (2.5%) | 1.5 / 0.15 / 20 | Monthly–quarterly; 45d; 1y soft lock (3%); fund gate 25% |
| Event-driven | 0.35 | 0.75 | 6% | 4, −0.8 | (0.75, 0.20, 0.05) | 0.5% (2.5%) | 1.5 / 0.2 / 20 | Quarterly; 60–90d; 1y lock; gate 20–25% |
| Credit / distressed | 0.25 | 0.55 | 6% | 4, −1.0 | (0.70, 0.20, 0.10) | 1.0% (2.5%) | 1.5 / 0.27 / 20 | Quarterly or semi-annual; 90d; 1–2y lock; gate 10–25%; side pocket ≤ 20% |
| RV / FI arbitrage | 0.10 | 0.30 | 4% | 3.5, −1.5 | (0.75, 0.20, 0.05) | 1.0% (2.0%) | 1.5–2 / 0.2 / 20 | Quarterly; 60–90d; gate 25% |
| Discretionary macro | 0.05 | 0.00 | 7% | 6, 0 | (1.0) | 1.0% (2.5%) | 2.0 / 0.18 / 20 | Monthly; 30d |
| Systematic trend | 0.00 | −0.20 (convex) | 11% | 6, +0.3 | (1.0) | 1.0% (2.0%) (Sharpe ≈ 0.3, 09) | 1–2 / 0.1 / 20 | Monthly or daily (managed account / UCITS); 5–30d |
| FoHF | 0.35 | 0.55 | 4% | 5, −0.5 | (0.80, 0.15, 0.05) | 0.0% (2.0%) | 0.95 + underlying | Quarterly; 90d; double mismatch |

**Jumps** (SYNTHETIC [I]): $p^J_{CRIS}$ = 0.3 per quarter for multi-strategy, RV, credit and event; $k$ = 2–3. Anchor: in Q3 2008 the GS VIP index of hedge-fund favourite longs fell 19.07%, more than twice the S&P 500's decline [S: CA].

**Long-only** (SYNTHETIC; split aligned with G7: DM equity $22bn, EM equity $6bn, FI $8bn):

| Sleeve | TE default (range) | Net IR prior mean (sd of true IR) | Fee [C, unverified] | Liquidity and cost model |
|---|---|---|---|---|
| US / DM large cap | 3% (2–4) | 0.00 (0.15) | 20–40bp | T+1/T+2; square-root with V $150–400bn, σ 1.0% |
| EM equity | 5% (4–7) | 0.10 (0.20) | 50–75bp | T+2; taxes ~10–20bp; σ 1.2% |
| Small cap | 5% (4–7) | 0.10 (0.20) | 50–80bp | Multi-day; V ~$40bn |
| Core FI | 1% (0.5–1.5) | 0.00 after a credit-beta term (Brooks) | 10–20bp | Bid–ask 1–15bp normal, ×3–5 in CRIS [C] |
| HY / EMD | 3% (2–4) | 0.05 (0.15) | 30–45bp | Bid–ask 25–75bp normal [C] |

**Financing and margin** (SYNTHETIC):

| Item | Normal | Tight | CRIS |
|---|---|---|---|
| S&P 500 futures/TRS spread over SOFR | 30–50bp | 80–140bp | 150–200bp+ (spikes) |
| Non-US index futures/TRS | Desk to supply; placeholder 20–50bp | — | — |
| Equity futures IM | 5–8% | 8–10% | 10–15% |
| HF-unit financing LTV | 20–50% by liquidity class [nrv] | — | Halved in CRIS [I] |

- S&P 500 anchors: [S] §4.8. Non-US placeholder: [I]; Eurex box +13bp is a risk-free floor only. IM: [P] 06/09. HF-unit financing spread: SOFR+150–300bp [nrv].

### 6.12 Calibration targets (the simulator must reproduce these)
1. **Industry-like synthetic HF book:** investor liquidity 8.4 / 27.3 / 64.4% (Jun 2026). Multi-strategy GAV-weighted leverage of about 12×.
2. **Crisis loss ratios:** composite about 0.5 (2008, Q1 2020) and about 0.2 (2022); Equity Hedge 0.66; Event Driven 0.78 (Q1 2020).
3. **CTA:** positive in 2008 (+14%) and 2022 (+7%); 2009–2025 mean about 1.9% a year.
4. **Smoothing:** reported ρ₁ ≈ 0 (macro) to 0.3–0.5 (credit/RV).
5. **Crisis liquidity:**
   - 20–25% of capital requested within a year;
   - about 7–8% of industry capital in a single month (Dec 2008: > $100bn against roughly $1.2–1.5trn) [I from S];
   - Hedgebay average discount about 20% (Dec 2009), extremes about 50%;
   - illiquid index at 67% of NAV (Jul 2010).
6. **Fees:** median management 1.5%; pass-through median 4.5%; effective incentive about 50%; investor share of gross about 41–42% at pass-through platforms.
7. **Long-only:** cross-sectional mean net alpha ≈ 0; top-quintile repeat rate about 20%.
8. **Financing spread distribution:** mean about 30–50bp, tail events of 140–200bp [S], about 1–2 spikes a year around quarter-ends [I].

### 6.13 Data needs (ADIC to supply)
- **Documents:** offering documents, side letters and most-favoured-nation (MFN) terms → the terms vector τ (extraction agent, human-verified).
- **Exposure:** ADIC share of each fund; investor-base composition (FoF/HNW share).
- **Returns:** monthly net and, where possible, gross returns; manager-reported exposures; Form PF-style leverage.
- **Fees:** pass-through history and caps; fee schedules.
- **History:** 2008/2020/2022/2026 experience (requests, gates, payment dates).
- **Long-only holdings:** holdings, benchmarks, ADV coverage, transition-manager costs.
- **Overlay:** desk data on futures and TRS financing history by index, IM schedules and CSA terms.
- **Forecasts:** the group's point-in-time forecast archive.
- **Leveraged HF programme:** financing terms, LTV, triggers.
- **Tax:** physical vs synthetic treatment for a sovereign. US §892 and §871(m) interactions can move the economics by tens of bp [nrv; tax counsel].

### 6.14 How the group forecasts, and how to grade it
**Production.** Three return series per holding (Stream 07):
- **Underwritten:** at hire, the target net return, alpha, TE or volatility, crisis beta and expected terms.
- **Actual:** since inception, TWR and DWR, de-smoothed and factor-adjusted; realised liquidity behaviour.
- **Group forecast:** the forward net-alpha distribution and liquidity outlook. Inputs are due diligence, manager targets (multi-strategies market "steady" 12%+ [S: Bloomberg via Hedgeweek]), peer percentiles and factor CMAs.

**Typical biases and corrections:**

| Bias | Evidence | Correction |
|---|---|---|
| Selection on past outperformance | Goyal & Wahal | Shrink underwritten α heavily; carry a bias term from the archive |
| Optimistic analyst or consultant ratings | Jenkinson et al. [S; the evidence covers US active equity] | Score raters (Cooke/CRPS weights, 07) |
| Biased peer data | Aggarwal & Jorion; Fung & Hsieh | Use FoF-based or bias-adjusted benchmarks |
| Smoothed risk | GLM; Asness et al. | Forecast on de-smoothed returns |
| Short-put tails ignored | Agarwal & Naik | Regime betas plus option factors |
| Gross-vs-net confusion | CA; Ben-David et al. | Forecast net of all fees |
| Capacity | Naik et al.; Pástor et al. | Make α a function of AUM |
| FI credit beta read as alpha | Brooks et al. | Factor-adjust before scoring |
| Contractual liquidity assumed | CA 2009; Aiken et al. | State-machine forecasts |

**Credibility on realised alpha.** $Z=n/(n+k)$ with $k=(\sigma_\epsilon/\tau)^2$:
- Long-only (TE 3%, τ 1%): Z = 0.25 / 0.36 / 0.53 at 3 / 5 / 10 years.
- Hedge funds (residual σ 6%, τ 2.5%): Z = 0.34 / 0.47 / 0.64 [I].

**Grading metrics:**
- Stream 07's engine (CRPS, PIT, MZ slope, coverage, CUSUM).
- **Group-specific additions:**
  - (i) rank IC (Spearman) between forecast and realised factor-adjusted net alpha across managers;
  - (ii) top-quartile hit rate against the 25% base rate;
  - (iii) Brier score on P(beat benchmark net over 12m);
  - (iv) crisis-beta forecast error in each stress window;
  - (v) liquidity forecast error: predicted vs realised time-to-cash and gate incidence;
  - (vi) **decision regret against the Goyal–Wahal baseline**, i.e. the return from keeping the fired manager;
  - (vii) false-discovery control when declaring skill [S: Barras et al.].

### 6.15 IC artifacts and agent roles
**Artifacts:**
1. Group liquidity ladder: contractual vs CRIS-P5, by bucket.
2. Manager evidence card per holding:
   - u/a/f series and credibility votes;
   - de-smoothed Sharpe and crisis beta;
   - the gross→net fee waterfall;
   - capacity, terms and time-to-cash;
   - SELL/HOLD/REFI/LEVER scores, in MAP-scorecard form (14).
3. REFINANCE monitor: implied financing vs history, IM, VM-at-risk, and cost per $ freed against the MCL curve.
4. Portable-alpha stress card.
5. Rebalancing monitor.
6. Forecaster scorecards.

**Agents** (Agentic Scientist pattern; LLMs never compute numbers):
- A quarantined **Terms Extractor**: dual extraction of τ from offering documents, with every field tied to its source clause.
- A **Terms Verifier** applying rubric gates.
- A **Waterfall Planner**, which calls the deterministic LP.
- A **Challenge agent**, which looks for:
  - adverse-selection redemptions;
  - preemptive-run exposure;
  - double leverage;
  - unpriced pass-through fees;
  - VM backed by HF liquidity.
- A **Calibration agent**, which refits quarterly.

### 6.16 SPECIFICATION CARD (Public Markets, G5)

| Item | Specification |
|---|---|
| **Data fields** | holding_id; group=PublicMarkets; sub∈{HF, LO}; strategy; manager; vehicle (fund/SMA/commingled/MA/UCITS); share class; NAV; ADIC share ω; fees (m, κ, hurdle, HWM, crystallisation, pass-through cap); terms τ (freq, notice, lock, soft fee, fund gate g and mandatory flag, investor gate γ, K_max, holdback h, payment lag p, side-pocket max, suspension, PIK); leverage (gross/NAV); factor betas; monthly net (and gross) returns; benchmark; fund AUM; investor-base mix; prime brokers; u/a/f return series with dates and authors |
| **Return equations** | HF: $r=r_f+\beta_S^\top F+\gamma P+\alpha(age,AUM)+\sigma_S\epsilon_{skew\text{-}t}+J$. Reported: GLM MA(2). Net: fee waterfall. LO: $r=r_b+(\beta-1)(r_b-r_f)+\alpha+TE\,\epsilon$ (+ credit-beta term for FI) |
| **Cash-flow equations** | §6.6: redemption payouts (gate π, investor cap, holdback, side pocket, liquidation), LO sales net of $c(Q,S)=Y\sigma\sqrt{Q/V}+$spread+tax, synthetic legs (IM, VM, financing) |
| **Parameter defaults** | §6.11 tables (SYNTHETIC). Key: HF crisis betas −0.2 (trend) to 0.75; θ₀ 0.55–1.0; pass-through median 4.53%; financing 30–50 / 80–140 / 150–200bp; IM 5–8% → 10–15%; Y = 0.5–1.0 |
| **Liquidity terms and stress** | State machine §6.5: gate hazard logit (regime, drawdown, others' requests, mismatch, leverage); queue $\pi=\min(1,gNAV/R)$; preemption; suspension (mean 3 quarters); side pockets; liquidation schedule; ledger factor φ(h,S) at P5. Industry anchor: 8.4 / 27.3 / 64.4% |
| **SELL** | HF: redeem if $\hat\alpha^{net}+\kappa^{reentry}<\bar\ell(T^{cash})$; secondary if $1-d^{HF}_S$ ≥ λ-priced schedule value ($d$: 0–5% / 15–25% / 30–50%). LO: liquidate at $c(Q,S)$ |
| **HOLD** | Default; value = NAV + PV(α_net) − terms value (Ang–Bollen) |
| **REFINANCE** | LO physical→synthetic if $\bar\ell\ge\bar f+\hat\alpha^{net}+TC/\tau+\lambda_{Lev}N/NAV+\kappa^{VM}$. Example: 0.4–0.7%/yr per $ freed (normal), 2.9–3.3% (stress). HF: borrow vs units or redeem + factor replication |
| **LEVER** | Synthetic beta ($ERP-f>$ charges); portable alpha ($\alpha^{net}_{HF}-f>$ charges + κ^mis; collateral = HQLA only); levered HF (double-leverage stress; LTV halves in CRIS) |
| **Forecasts and biases** | Analyst/manager alpha expectations: optimistic (selection, ratings), gross/net, biased peers, smoothing, capacity, contractual-liquidity assumption. Corrections in §6.14. Credibility Z(5y) ≈ 0.36 (LO), 0.47 (HF) |
| **Synthetic-data defaults** | Generate managers per strategy from the §6.11 priors. Draw α ~ N(mean, sd); apply decay and capacity; skew-t residuals; regime betas; crisis jumps; GLM smoothing; the fee waterfall; terms per strategy row; gate hazards per §6.5. Label every file SYNTHETIC |
| **Links to other groups** | **Overlay (G7):** synthetic beta, VM/IM, trend in the defensive stack, ladder φ. **Treasury:** HQLA and IM collateral. **PE / Secondaries / Co-investment:** capital calls drive redemptions; internal transfers carry no liquidity credit. **Capital Solutions:** quotes for HF-unit financing. **Private Credit (G6):** semi-liquid gates (the 2026 analogue); HY/loan managers. **Stream 08:** Score/MCL. **Stream 07:** fusion and scoring. **Stream 10:** regimes |

---

## 7. Implementation notes
- **Libraries:**
  - numpy/numba or JAX for vectorised paths;
  - `arch` (Hansen skew-t) and statsmodels (MarkovRegression; MA fits) for returns;
  - scipy.optimize for GLM MLE with simplex constraints;
  - PyMC or NumPyro for hierarchical alpha;
  - `lifelines` for liquidation hazards;
  - cvxpy (CLARABEL/MOSEK power cone) and HiGHS (MILP) for the waterfall;
  - `scoringrules` for CRPS;
  - pydantic v2 for the terms schema (C4 contracts).
- **State machine:**
  - Encode states as int8 arrays of shape (paths × lots).
  - Step the vectorised machine only on dealing-date months and keep a daily calendar for notice cut-offs.
  - Avoid per-path Python loops.
  - Others' backlog is per fund, not per lot.
- **Dealing calendars:** business-day and month-end conventions, holiday shifts, notice measured in calendar vs business days, and the fiscal year-end that releases holdbacks.
- **Pitfalls:**
  - **De-smoothing:** θ₀ → 0 is explosive, so floor and shrink it.
  - **Fees:** HWM and incentive accruals are path-dependent; crystallise on the documented frequency.
  - **Pass-through netting:** pod-level pay is charged even when the fund is flat.
  - **Double counting:** do not count the same cash in G7's ladder and in this engine. φ is the single interface.
  - **Regime probabilities:** decisions use filtered, not smoothed, regime probabilities.
  - **Rare events:** use importance sampling of CRIS paths for P5 ladders, and common random numbers for policy comparisons.
  - **Time-step alignment:** align monthly HF returns with daily VM.
  - **FX:** hedge non-USD long-only mandates; forward roll costs sit outside this dossier.
- **Reproducibility:** worked examples are in `research/groups/verification/G5_public_markets_examples.py`.

---

## 8. Risks, pitfalls and limitations
- **Sparse gating data.** The §6.5 hazards are [I] priors. Use wide ambiguity sets and report how sensitive the results are to $p^{gate}_{CRIS}\in[5\%,40\%]$.
- **Reflexivity and signalling.** Large ADIC redemptions can trigger gates and be observed by others. Redemption notices can carry information content.
- **Adverse selection.** Redeeming the best liquid managers degrades the remaining book (2008).
- **Crowding and leverage.** Multi-strategy leverage at about 12× (GAV-weighted) with common pod positions means a deleveraging spiral would hit many "diversifying" managers at once (Q3 2008 VIP-index pattern; Aug 2007 quant episode per 09).
- **Double leverage.** A leveraged HF programme stacks ADIC-level financing on fund leverage. Lenders can call margin while redemptions are gated.
- **Financing-spread spikes.** These hit REFINANCE and portable alpha exactly when used (Dec 2024; 26 Jun 2026). Synthetic beta also raises gross leverage and VM exposure.
- **Basis risk.** Futures benchmarks differ from mandate benchmarks. FX and tax effects can differ between physical and synthetic holdings.
- **Data quality.** Smoothing, misreporting near zero, and survivorship in peer data.
- **Evidence limits in this dossier:**
  - Fung–Hsieh (2000) bias sizes remain [nrv]. Aragon's premium and Jenkinson et al.'s finding are now abstract-verified [corrected 2026-10-18: both were listed here as [nrv]; the verification log (A31, A32) confirmed them from the abstracts].
  - Some 2025–26 index figures are [ss].
  - Long-only TE/IR distributions are practitioner ranges, not verified datasets.
  - Non-US implied financing levels are unverified.
- **Synthetic data.** It must never be presented as ADIC data.

---

## 9. Open questions (what ADIC must supply or confirm)
1. Actual HF and long-only holdings: terms τ from offering documents and side letters; ADIC's share of each fund; investor-level preferences or MFNs.
2. Structure of the reported leveraged-HF programme: financing provider, LTV and margin triggers, look-through leverage, and its liquidity in a CRIS regime.
3. Overlay capacity and mandate to hold physical-to-synthetic beta for long-only sleeves; whether that notional counts against the gross-exposure cap; CSA and IM status (09 Q1).
4. Desk history of implied financing for S&P 500, EURO STOXX 50, MSCI EAFE/EM and UST futures, and TRS quotes, 2024–2026.
5. Tax treatment of physical vs synthetic exposure for a sovereign (US §892/§871(m), treaties).
6. The group's point-in-time forecast archive. Who forecasts, at what horizon, and gross or net?
7. Which managers are capacity-constrained or closed (re-entry option value $\kappa^{reentry}$)?
8. ADIC's own 2008/2020/2022/2026 redemption experience: requests, gates, payment timing.
9. Rebalancing policy: targets on reported vs economic weights; band; who owns execution (group or overlay).
10. Whether the group's liquidity-reserve share (C-PM1) is set centrally (C3/G7) or by the group.

---

## 10. References

**Read in this session (URL given)**
1. Agarwal, V., Daniel, N.D., Naik, N.Y. (2009). Role of managerial incentives and discretion in hedge fund performance. *Journal of Finance* 64(5), 2221–2256. https://ideas.repec.org/a/bla/jfinan/v64y2009i5p2221-2256.html
2. Agarwal, V., Naik, N.Y. (2004). Risks and portfolio decisions involving hedge funds. *Review of Financial Studies* 17(1), 63–98. https://ideas.repec.org/a/oup/rfinst/v17y2004i1p63-98.html
3. Aggarwal, R.K., Jorion, P. (2010). Hidden survivorship in hedge fund returns. *Financial Analysts Journal* 66(2), 69–74. https://ideas.repec.org/a/taf/ufajxx/v66y2010i2p69-74.html
4. Aiken, A.L., Clifford, C.P., Ellis, J.A. (2015). Hedge funds and discretionary liquidity restrictions. *Journal of Financial Economics* 116(1), 197–218. https://ideas.repec.org/a/eee/jfinec/v116y2015i1p197-218.html
5. Ang, A., Bollen, N.P.B. (2010). Locked up by a lockup: Valuing liquidity as a real option. *Financial Management* 39(3), 1069–1096. https://ideas.repec.org/a/bla/finmgt/v39y2010i3p1069-1096.html
6. Aragon, G.O. (2007). Share restrictions and asset pricing: Evidence from the hedge fund industry. *Journal of Financial Economics* 83(1), 33–58 (bibliographic record only in the drafting session; the verification log, A31, later confirmed the abstract's 4–7% figure). https://ideas.repec.org/a/eee/jfinec/v83y2007i1p33-58.html
7. Asness, C., Krail, R., Liew, J. (2001). Do hedge funds hedge? *Journal of Portfolio Management* 28(1), 6–19. https://doi.org/10.3905/jpm.2001.319819 ; https://www.aqr.com/Insights/Research/Journal-Article/Do-Hedge-Funds-Hedge
8. Barras, L., Scaillet, O., Wermers, R. (2010). False discoveries in mutual fund performance: Measuring luck in estimated alphas. *Journal of Finance* 65(1), 179–216. https://ideas.repec.org/a/bla/jfinan/v65y2010i1p179-216.html
9. Ben-David, I., Birru, J., Rossi, A. (2020/2026). The performance of hedge fund performance fees. NBER WP 27454; *Review of Corporate Finance Studies* 15(3), 704–747. https://doi.org/10.1093/rcfs/cfag015 ; https://www.nber.org/papers/w27454
10. Ben-David, I., Franzoni, F., Moussawi, R. (2012). Hedge fund stock trading in the financial crisis of 2007–2009. *Review of Financial Studies* 25(1), 1–54. https://ideas.repec.org/a/oup/rfinst/v25y2012i1p1-54.html
11. Berk, J.B., van Binsbergen, J.H. (2015). Measuring skill in the mutual fund industry. *Journal of Financial Economics* 118(1), 1–20. https://ideas.repec.org/a/eee/jfinec/v118y2015i1p1-20.html
12. Bollen, N.P.B., Pool, V.K. (2009). Do hedge fund managers misreport returns? Evidence from the pooled distribution. *Journal of Finance* 64(5), 2257–2288. https://ideas.repec.org/a/bla/jfinan/v64y2009i5p2257-2288.html
13. Boyson, N.M., Stahel, C.W., Stulz, R.M. (2010). Hedge fund contagion and liquidity shocks. *Journal of Finance* 65(5), 1789–1816. https://ideas.repec.org/a/bla/jfinan/v65y2010i5p1789-1816.html
14. Brooks, J., Gould, T., Richardson, S.A. (2020). Active fixed income illusions. *Journal of Fixed Income* 29(4), 5–19. https://doi.org/10.3905/jfi.2020.1.086 ; https://www.aqr.com/Insights/Research/Journal-Article/Active-Fixed-Income-Illusions
15. Busse, J.A., Goyal, A., Wahal, S. (2010). Performance and persistence in institutional investment management. *Journal of Finance* 65(2), 765–790. https://ideas.repec.org/a/bla/jfinan/v65y2010i2p765-790.html
16. Chen, Q., Goldstein, I., Jiang, W. (2010). Payoff complementarities and financial fragility: Evidence from mutual fund outflows. *Journal of Financial Economics* 97(2), 239–262. https://ideas.repec.org/a/eee/jfinec/v97y2010i2p239-262.html
17. Cipriani, M., Martin, A., McCabe, P., Parigi, B.M. (2014). Gates, fees, and preemptive runs. FRBNY Staff Report 670. https://www.newyorkfed.org/research/staff_reports/sr670.html
18. Dao, T.-L., Nguyen, T.-T., Deremble, C., Lempérière, Y., Bouchaud, J.-P., Potters, M. (2016). Tail protection for long investors: Trend convexity at work. arXiv:1607.02410. https://arxiv.org/abs/1607.02410. Published version: *Journal of Investment Strategies* 7(1), 61–84 (2017). https://doi.org/10.21314/jois.2017.093
19. Dichev, I.D., Yu, G. (2011). Higher risk, lower returns: What hedge fund investors really earn. *Journal of Financial Economics* 100(2), 248–263. https://ideas.repec.org/a/eee/jfinec/v100y2011i2p248-263.html
20. Fama, E.F., French, K.R. (2010). Luck versus skill in the cross-section of mutual fund returns. *Journal of Finance* 65(5), 1915–1947. https://ideas.repec.org/a/bla/jfinan/v65y2010i5p1915-1947.html
21. Frazzini, A., Israel, R., Moskowitz, T.J. (2018). Trading costs. AQR working paper. https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs
22. Fung, W., Hsieh, D.A. (2000). Performance characteristics of hedge funds and commodity funds: Natural vs. spurious biases. *JFQA* 35(3), 291–307. https://ideas.repec.org/a/cup/jfinqa/v35y2000i03p291-307_00.html
23. Fung, W., Hsieh, D.A. (2001). The risk in hedge fund strategies: Theory and evidence from trend followers. *Review of Financial Studies* 14(2), 313–341. https://ideas.repec.org/a/oup/rfinst/v14y2001i2p313-41.html
24. Fung, W., Hsieh, D.A. (2004). Hedge fund benchmarks: A risk-based approach. *Financial Analysts Journal* 60(5), 65–80. https://ideas.repec.org/a/taf/ufajxx/v60y2004i5p65-80.html; factor data: https://people.duke.edu/~dah7/HFRFData.htm
25. Fung, W., Hsieh, D.A., Naik, N.Y., Ramadorai, T. (2008). Hedge funds: Performance, risk, and capital formation. *Journal of Finance* 63(4), 1777–1803. https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1777-1803.html
26. Getmansky, M., Lo, A.W., Makarov, I. (2004). An econometric model of serial correlation and illiquidity in hedge fund returns. *JFE* 74(3), 529–609; NBER WP 9571. https://www.nber.org/papers/w9571
27. Getmansky, M., Lee, P.A., Lo, A.W. (2015). Hedge funds: A dynamic industry in transition. *Annual Review of Financial Economics* 7(1), 483–577. https://doi.org/10.1146/annurev-financial-110311-101741 ; NBER WP 21449. https://www.nber.org/papers/w21449
28. Goyal, A., Wahal, S. (2008). The selection and termination of investment management firms by plan sponsors. *Journal of Finance* 63(4), 1805–1847. https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1805-1847.html
29. Hombert, J., Thesmar, D. (2014). Overcoming limits of arbitrage: Theory and evidence. *JFE* 111(1), 26–44. https://ideas.repec.org/a/eee/jfinec/v111y2014i1p26-44.html
30. Jagannathan, R., Malakhov, A., Novikov, D. (2010). Do hot hands exist among hedge fund managers? An empirical evaluation. *Journal of Finance* 65(1), 217–255. https://ideas.repec.org/a/bla/jfinan/v65y2010i1p217-255.html
31. Malkiel, B.G., Saha, A. (2005). Hedge funds: Risk and return. *Financial Analysts Journal* 61(6), 80–88. https://ideas.repec.org/a/taf/ufajxx/v61y2005i6p80-88.html
32. Mitchell, M., Pulvino, T. (2001). Characteristics of risk and return in risk arbitrage. *Journal of Finance* 56(6), 2135–2175. https://ideas.repec.org/a/bla/jfinan/v56y2001i6p2135-2175.html
33. Naik, N.Y., Ramadorai, T., Stromqvist, M. (2007). Capacity constraints and hedge fund strategy returns. *European Financial Management* 13(2), 239–256. https://ideas.repec.org/a/bla/eufman/v13y2007i2p239-256.html
34. Pástor, Ľ., Stambaugh, R.F., Taylor, L.A. (2015). Scale and skill in active management. *JFE* 116(1), 23–45. https://doi.org/10.1016/j.jfineco.2014.11.008 ; NBER WP 19891. https://www.nber.org/papers/w19891
35. Ramadorai, T. (2012). The secondary market for hedge funds and the closed hedge fund premium. *Journal of Finance* 67(2), 479–512 (bibliographic record only). https://ideas.repec.org/a/bla/jfinan/v67y2012i2p479-512.html
36. Ramadorai, T. (2013). Capacity constraints, investor information, and hedge fund returns. *JFE* 107(2), 401–416. https://ideas.repec.org/a/eee/jfinec/v107y2013i2p401-416.html
37. Sadka, R. (2010). Liquidity risk and the cross-section of hedge-fund returns. *JFE* 98(1), 54–71. https://ideas.repec.org/a/eee/jfinec/v98y2010i1p54-71.html
38. Teo, M. (2011). The liquidity risk of liquid hedge funds. *JFE* 100(1), 24–44. https://ideas.repec.org/a/eee/jfinec/v100y2011i1p24-44.html
39. Tóth, B., Lempérière, Y., Deremble, C., de Lataillade, J., Kockelkoren, J., Bouchaud, J.-P. (2011). Anomalous price impact and the critical nature of liquidity in financial markets. *Physical Review X* 1, 021006. https://arxiv.org/html/1105.1694v3
40. Office of Financial Research, Hedge Fund Monitor and API (SEC Form PF aggregates; updated 16 Sep 2026). https://www.financialresearch.gov/hedge-fund-monitor/ ; https://data.financialresearch.gov/hf/v1/metadata/mnemonics?dataset=fpf
41. Board of Governors of the Federal Reserve System (2026). *Financial Stability Report*, May 2026 (leverage; funding risks). https://www.federalreserve.gov/publications/2026-may-financial-stability-report-leverage.htm ; https://www.federalreserve.gov/publications/2026-may-financial-stability-report-funding-risks.htm
42. Cambridge Associates (2025). *2024 Hedge Fund Discretionary Expense Summary*, 10 Oct 2025. https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2025/10/2025-10-Hedge-Fund-Discretionary-Expense-Summary-2024.pdf
43. Cambridge Associates (2009). *Is the "Hedge Fund Business Model" Broken?*, Jan 2009. https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2014/10/Is-the-Hedge-Fund-Business-Model-Broken-Jan-2009.pdf
44. Cambridge Associates (2020). *Hedge Fund Update: First Quarter 2020*. https://publishedresearch.cambridgeassociates.com/hedge-fund-update-first-quarter-2020/
45. Spiegel, J.A. (Paul, Weiss) (2009). Handling mass redemptions: A primer (Bloomberg reprint, Apr 2009). https://www.paulweiss.com/media/1517346/pw_spgl_apr09.pdf
46. Hedgeweek (21 Jan 2009). Redemptions and performance losses cut hedge fund assets USD782bn, says Hennessee. https://www.hedgeweek.com/redemptions-and-performance-losses-cut-hedge-fund-assets-usd782bn-says-hennessee/
47. Family Wealth Report (23 Oct 2008). Hedge fund investors use secondary market to pull out money (citing WSJ). https://www.familywealthreport.com/article.php/Hedge-Fund-Investors-Use-Secondary-Market-To-Pull-Out-Money-_dash_-Report
48. WealthBriefing (1 Feb 2010). Hedge funds trading at historic discounts: Hedgebay. https://www.wealthbriefing.com/html/article.php/hedge-funds-trading-at-historic-discounts-_dash_-hedgebay
49. Hedgeweek (25 Aug 2010). Illiquid trading dominates secondary market as it awaits locked funds. https://www.hedgeweek.com/illiquid-trading-dominates-secondary-market-awaits-locked-funds/
50. HedgeCo/InvestmentNews (30 May 2011). Some $100 billion locked up in "sliver" of hedge funds. https://www.hedgeco.net/news/?p=22752
51. InvestmentNews (16 Feb 2010). Hedge funds have best year since 1999. https://investmentnews.com/alternatives/hedge-funds-have-best-year-since-1999/26328
52. Mondo Visione / HFR (10 and 20 Jan 2023). 2022 HFRI results. https://mondovisione.com/media-and-resources/news/hfri-500-macro-gains-in-december-leads-industry-to-record-outperformance-in-202-2023110/ ; https://mondovisione.com/media-and-resources/news/hedge-fund-capital-rises-to-conclude-volatile-2022-as-managers-position-for-risk-2023120/
53. WealthBriefing (9 Jan 2026). Hedge funds log strongest calendar-year returns since 2009 (HFR). https://www.wealthbriefing.com/html/printarticle.php?id=206626
54. Hedgeweek (24 Jul 2026). Hedge fund assets surge by record $409bn to $5.6tn in Q2 (HFR). https://www.hedgeweek.com/hedge-fund-assets-surge-by-record-409bn-to-5-6tn-in-q2/
55. BarclayHedge. Barclay Hedge Fund Index and Barclay CTA Index (accessed 18 Oct 2026). https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=Barclay-Hedge-Fund-Indices&indexName=Barclay-Hedge-Fund-Index ; https://portal.barclayhedge.com/cgi-bin/indices/displayCtaIndex.cgi?indexCat=Barclay-CTA-Indices&indexName=Barclay-CTA-Index
56. TheWealthAdvisor (6 Jan 2023). Hedge fund fees fall to lowest level since 2008 financial crisis: HFR. https://www.thewealthadvisor.com/article/hedge-fund-fees-fall-lowest-level-2008-financial-crisis-hfr
57. Reuters via Kitco (2 Aug 2024). Hedge fund investor appetite hit by high fees and private credit, says Goldman Sachs. https://www.kitco.com/news/off-the-wire/2024-08-02/hedge-fund-investor-appetite-hit-high-fees-and-private-credit-says
58. Hedgeweek (12 Feb 2025). Hedge funds charging billions in "no limit" passthrough fees (Bloomberg/Form ADV). https://www.hedgeweek.com/hedge-funds-charging-billions-in-no-limit-passthrough-fees/
59. Resonanz Capital (9 Mar 2026). The multi-manager pass-through audit. https://resonanzcapital.com/insights/the-multi-manager-pass-through-audit-how-to-underwrite-the-real-fee-load
60. Burton, K., Kumar, N. (Bloomberg, 6 Dec 2021). Millennium, Citadel winning the war to keep client cash longer (republished). https://www.thewealthadvisor.com/article/millennium-citadel-winning-war-keep-client-cash-longer
61. Jawlah (11 Jun 2026). ADIC-led plan for up to $15bn in leveraged hedge fund strategies (citing Bloomberg). https://jawlah.co/en/58501
62. D. E. Shaw (c. 23 Jan 2025). Imbalance Sheet: Supply, demand, and S&P 500 financing. https://www.deshaw.com/library/imbalance-sheet
63. CME Group (2026). Funding the U.S. equity market to new heights (via Stream 06 verification). https://www.cmegroup.com/articles/2026/funding-the-us-equity-market-to-new-heights.html
64. Reuters via Kitco (9 Jul 2026). US markets brace for renewed funding pressure as leverage rises. https://www.kitco.com/news/off-the-wire/2026-07-09/us-markets-brace-renewed-funding-pressure-leverage-rises
65. Eurex (Jun 2026). EURO STOXX 50 index options box spreads (research paper). https://www.eurex.com/resource/blob/5356176/37f5745e27e9eb4f6d033f92c825b610/data/research-paper_eurostoxx50-index-options-box-spreads.pdf
66. Man Group (1 Jun 2020). Strategic rebalancing. https://www.man.com/maninstitute/strategic-rebalancing
67. Lovdata. Mandat for forvaltningen av Statens pensjonsfond utland (GPFG mandate), §1-6, §2-4 (last amended 5 Oct 2026). https://lovdata.no/dokument/INS/forskrift/2010-11-08-1414
68. NBIM. Investment mandate, Government Pension Fund Global (last amended 9 Dec 2025). https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/
69. Denmark, F. (Institutional Investor, 23 Dec 2008). An alpha bet gone bad (headline and opening only). https://inv.institutionalinvestor.com/article/2btfkig3d6xyf8jerma68/premium/an-alpha-bet-gone-bad

**Search-summary only [ss] (pages not opened):** HFR Sep-2026 estimates via Connect Money/AlphaMaven; HFRI Macro 2025 +7.2%; Millennium 5%/quarter cap (Bloomberg 2020); Iowa PERS portable alpha (Markets Group); ICE MSCI TRF FAQ (https://www.ice.com/publicdocs/MSCI_Total_Return_Futures_Contracts_FAQ.pdf); PGIM EM transition case; AllianceBernstein top-quintile persistence; Hedgebay mid-2009 discount path.

**Cited from memory [nrv] (no URL):** Fung–Hsieh (2000) bias magnitudes; Grinold & Kahn, *Active Portfolio Management* (2000); S&P 500 total returns 2008 (−37.0%) and 2022 (−18.1%); HF-unit financing LTVs and spreads; US §892/§871(m) tax interaction.

**Cited from memory; bibliographic records verified after drafting** (Crossref, 2026-10-18; `research/literature/G5_public_markets.lit.md`, Tables A–B). Content claims attached to these works stay [nrv] unless the entry says otherwise.
- Almgren, R., Chriss, N. (2001). Optimal execution of portfolio transactions. *Journal of Risk* 3(2), 5–39. https://doi.org/10.21314/jor.2001.041 [corrected 2026-10-18: previously cited as 2000]
- Aragon (2007) lock-up premium size: now [S]. The verification log (A31) confirmed the abstract's "approximately 4-7% per year". Full entry: ref 6.
- Davis, M.H.A., Norman, A.R. (1990). Portfolio selection with transaction costs. *Mathematics of Operations Research* 15(4), 676–713. https://doi.org/10.1287/moor.15.4.676
- Geltner, D. (1993). Estimating market values from appraised values without assuming an efficient market. *Journal of Real Estate Research* 8(3), 325–345. https://doi.org/10.1080/10835547.1993.12090713. This is the paper meant by "Geltner AR(1)" in §3, not Geltner's 1991 *JREFE* paper.
- Granger, N., Greenig, D., Harvey, C.R., Rattray, S., Zou, D. (2014). Rebalancing risk. SSRN working paper. https://doi.org/10.2139/ssrn.2488552 (cited in §2.8 as summarised by Man 2020).
- Jenkinson, T., Jones, H., Martinez, J.V. (2016). Picking winners? Investment consultants' recommendations of fund managers. *Journal of Finance* 71(5), 2333–2370. https://doi.org/10.1111/jofi.12289. The finding is now [S]: the verification log (A32) confirmed the abstract's "no evidence that these recommendations add value" (US active equity).
- Kosowski, R., Naik, N., Teo, M. (2007). Do hedge funds deliver alpha? A Bayesian and bootstrap analysis. *Journal of Financial Economics* 84(1), 229–264. https://doi.org/10.1016/j.jfineco.2005.12.009
- Leland, H.E. (1999; the SSRN record is dated 2000). Optimal portfolio management with transactions costs and capital gains taxes. Working paper. https://doi.org/10.2139/ssrn.206871
- Rattray, S., Granger, N., Harvey, C.R., Van Hemert, O. (2020). Strategic rebalancing. *Journal of Portfolio Management* 46(6), 10–31. https://doi.org/10.3905/jpm.2020.1.150

**Sibling ADIC dossiers used for cross-links:** 03_sovereign_alm, 06_leverage, 07_return_fusion, 08_action_valuation, 09_overlay, 10_scenarios_robustness; clusters C1, C3; groups G2, G6, G7 calcs.

---

## Citation corrections (2026-10-18)

The corrections come from `research/literature/00_LITERATURE_SYNTHESIS.md` §2 (2.3, the G5 mismatch; 2.5, "four titles in G5"; 2.6 item 4, Geltner) and from the G5 citation-integrity tables in `research/literature/G5_public_markets.lit.md` (Tables A and B). All metadata was re-checked against Crossref on 2026-10-18. No number or conclusion changes, except the §8 evidence-limits bullet.

- §3 table and §10: Almgren & Chriss is now dated 2001, not 2000, with a full entry (*J. Risk* 3(2), 5–39, DOI 10.21314/jor.2001.041). This was the audit's only G5 mismatch.
- §10 ref 8: completed the Barras, Scaillet & Wermers title (": Measuring luck in estimated alphas").
- §10 ref 12: completed the Bollen & Pool title ("Evidence from the pooled distribution").
- §10 ref 16: completed the Chen, Goldstein & Jiang title (": Evidence from mutual fund outflows").
- §10 ref 30: completed the Jagannathan, Malakhov & Novikov title ("An empirical evaluation").
- §10 ref 7, Asness, Krail & Liew: added *JPM* 28(1), 6–19 and DOI 10.3905/jpm.2001.319819.
- §10 ref 9, Ben-David, Birru & Rossi: added pages 704–747 and DOI 10.1093/rcfs/cfag015.
- §10 ref 14, Brooks, Gould & Richardson: added *JFI* 29(4), 5–19 and DOI 10.3905/jfi.2020.1.086.
- §10 ref 27, Getmansky, Lee & Lo: added *ARFE* 7(1), 483–577 and DOI 10.1146/annurev-financial-110311-101741.
- §10 ref 34, Pástor, Stambaugh & Taylor: added *JFE* 116(1), 23–45 and DOI 10.1016/j.jfineco.2014.11.008.
- §10 ref 18, Dao et al.: added the published version, *J. Investment Strategies* 7(1), 61–84 (2017), DOI 10.21314/jois.2017.093.
- §3 table and §10: the Geltner citation now names the paper it means, Geltner (1993), *JRER* 8(3), 325–345, DOI 10.1080/10835547.1993.12090713, not the 1991 *JREFE* paper. This applies the cross-file fix "say which one each citation means".
- §10 [nrv] list: split it into memory-only items and items whose records are now verified. Added full entries with DOIs for Davis & Norman (1990), Granger et al. (2014), Jenkinson et al. (2016), Kosowski et al. (2007), Leland (SSRN record dated 2000) and Rattray et al. (2020).
- §2.3, Aragon (2007) 4–7% premium: [nrv] → [S]. The abstract was confirmed in verification log A31 (lit table A6). Ref 6 is annotated to match.
- §4.7 and §6.14, Jenkinson et al.: [nrv] → [S], with the scope stated as US active equity. The abstract was confirmed in verification log A32 (lit table A25).
- §8 evidence limits: only the Fung–Hsieh (2000) bias sizes stay [nrv]; marked [corrected 2026-10-18].
- Checked, but nothing in this dossier needed changing:
  - The G4 barrier re-run does not apply: this dossier has no barrier, BGK, LTV-breach, write-off or wipe-out statistic.
  - The re-check results for topics 10, 11, 13, 14 and G3 do not apply, because none of those works is cited here. The §6.15 mentions of the "Agentic Scientist pattern" and the "MAP-scorecard form" make no claim that the re-check corrects.
