# G2: Secondaries group, as buyer and investor (secondary funds and direct secondary deals)

**Stream:** G2 of the group research programme. **As of:** 2026-10-18.

**Scope.** This dossier covers ADIC's Secondaries group as a *buyer and investor*. Its working NAV is about US$14bn (synthetic). It covers:
- commitments to third-party secondary funds;
- direct secondary deals: LP-portfolio purchases and continuation-vehicle (CV) stakes;
- cash-flow and return models;
- the regime-dependent opportunity set;
- the group's SELL / HOLD / REFINANCE / LEVER levers;
- its links to the rest of ADIC.

**Related streams.** ADIC as a *seller* is stream 05. PE cash-flow mechanics are stream 04. Liquidity-adjusted valuation (LAPV) is stream 08. Leverage is stream 06. Belief fusion is stream 07. This dossier reuses their notation and adds group-specific depth.

**Evidence tags.**
- **[S]** sourced fact, with citation in §10.
- **[C]** practitioner consensus, or a secondary summary not checked against the primary document.
- **[I]** my inference, design default or synthetic calculation.

**Research notes.**
1. **Sources.** The session's shared web-search budget ran out twice. I therefore downloaded primary PDFs and extracted their text layers locally with pypdf:
   - Jefferies Jul-2026, Jan-2025 and Jul-2025;
   - Evercore H1-2026 and FY-2025;
   - Lazard Interim-2026;
   - the Campbell Lutyens FY-2025 flash report;
   - the CFA Institute continuation-fund report (Sep-2025);
   - the IPEV Valuation Guidelines (Dec-2025);
   - NBER working papers 22404 and 25207.

   I did not retrieve the Setter Capital, PJT Park Hill, Preqin or PitchBook reports named in the brief, nor vintage-level secondary-fund benchmarks.
2. **Consensus.** The consensus.app tools were authentication stubs only, so I did not call them. Academic metadata came from Crossref, IDEAS/RePEc, NBER and AEA pages instead.
3. **Chart values.** Values read from PDF text layers are used only where the mapping is unambiguous. Uncertain readings are flagged.
4. **Notation.**
   - $p$ is the price as a fraction of reference-date NAV (stream 05 calls this π).
   - $\pi_{s,t}$ is the cash-balance dual and $\ell_{s,t}$ the liquidity premium (stream 08). Stream 05's λ is the same quantity as $\ell$.
   - $\theta$ is economic value divided by reference NAV.
5. **Worked examples (§4.6).** All are synthetic and were computed with numpy/scipy (quarterly cash flows, IRR by Brent's method). The inputs are stated with each result.

---

## 1. Executive summary

1. **What "direct deals" means, and the working book.**
   - **Most plausible meaning [I]:**
     - (a) direct purchases of LP portfolios and single LP positions;
     - (b) lead or syndicate tickets in GP-led CVs, single-asset (SACV) or multi-asset (MACV).
   - **Other meanings for ADIC to confirm:**
     - secondary co-investments alongside a lead buyer;
     - "secondary directs" (portfolios of direct company stakes);
     - venture direct secondaries;
     - GP-led preferred equity, tender offers and strip sales;
     - structured LP-portfolio solutions, which overlap with Capital Solutions.
   - **Market classification [S: Evercore]:** H1-2026 GP-led volume split into SACV 53%, MACV 33%, preferred equity 8%, "directs" 5% and tenders 1%.
   - **Working book (synthetic) [I]:** US$14bn NAV, made up of about 40% secondary-fund interests, about 33% direct LP-portfolio purchases, about 24% CV stakes and about 3% other. About US$3.9bn of unfunded commitments plus deferred payables sit on top.

2. **The market is at a record and increasingly funded by retail and evergreen capital.**
   - **Volume [S]:** 2025 was US$226-240bn, depending on advisor. H1-2026 was US$118-124bn, with GP-led the majority for the first time since 2021. Forecasts for 2026 are US$250-275bn.
   - **Buyer capital [S: Jefferies]:** dedicated capital of US$290bn, down from US$327bn. The capital-overhang multiple is 1.2x, against 3.1x in 2020.
   - **Concentration [S: Campbell Lutyens]:** 14 players did 70% of 2025 volume.
   - **Evergreen capital [S]:** semi-liquid AUM is about US$500bn, more than US$130bn of it at secondary firms (Evercore). Evergreen buyers' lower return thresholds have supported LP-led prices (Lazard; CFA Institute).
   - **2026 showed this capital is pro-cyclical:** "elevated redemptions" and 5% NAV gates at several managers [S: Jefferies].

3. **Prices are firm but bifurcated (H1-2026) [S].**
   - **LP portfolios:** 87% of NAV overall. Buyout 91%, venture 79%, credit 89%, infrastructure 91%, real estate 68%.
   - **By age:** funds younger than 5 years trade at single-digit discounts. Tail-end funds (10+ years) trade at discounts of 25% or more.
   - **CVs (Lazard, buyout):** about 87% of SACV volume priced above 90% of NAV, and 23% above par. 40% of MACV volume priced below 90%.
   - **Buyer targets:** gross 1.7x (diversified LP) to 2.3x (SACV) over about 4 years.
   - **Deferral:** 26% of LP sales (Jefferies). 34% of LP-led volume had some deferral, and 9% deferred more than 18 months (Evercore).

4. **Buyers earn a real but modest premium, concentrated where liquidity is scarce.**
   - **Nadauld et al. (2006-2014 broker data; figures from NBER WP 22404, 2016) [S]:**
     - Buyers' annualised PME is 1.023 against sellers' 0.974 (0.976 in the published *JFE* abstract), a gap of about 5pp a year. For funds aged 4-9 years the gap is about 3pp.
     - The gap is about 25pp a year on young-fund sales, which clustered in 2008-09.
     - The gap is about zero on tail-end funds, where sellers out-earn buyers on PME.
   - **Transaction-price indices [S: Boyer et al. 2023]:** a secondary-transaction buyout index has a beta of about 1.8 and a CAPM alpha of about zero. Cash-flow-based measures (GPME) for the same funds are large and positive because they omit a discount-rate risk premium. [corrected 2026-10-18: "beta above 2" is the 2018 WP 25207 figure; NBER WP 28691 (2021), the readable version of the *JF* paper, gives 1.79 (1.94 with log returns); *JF* full text not accessed]
   - **Secondary funds against primaries [S: Callan]:** similar IRRs; pooled TVPI 0.38x lower; lower dispersion; NAV peaks at about 65% of commitment by year 4, against about 95% for primaries.
   - **CV evidence is early and mostly unrealised [S/C]:** TVPI is roughly in line with buyout funds, and SACV outcomes are narrower.

5. **Most of the headline "discount capture" is a reporting artifact unless NAV is right.**
   - **Accounting [S: IPEV 2025, §4]:** US GAAP lets a holder mark a fund interest at NAV (the ASC 820 practical expedient). Buying at 87% therefore books a +14.9% day-one gain. One quarter after purchase, the annualised since-purchase IRR is about 90% [I].
   - **Economic gain:** the true gain is $(\theta-p)N$.
   - **Worked example [I]:** asset return 9%, purchase at p = 0.87. The buyer's IRR is:
     - 14.3% if NAV is fair;
     - 12.3% if NAV is 5% stale or overstated;
     - 8.2% if NAV is overstated by 15%, which is *below* the asset's own return.
   - **Rule:** report accretion separately, and compute all three return series (underwritten, actual, forecast) on an economic basis.

6. **Buyer-side deferral and leverage add little in the base case and hurt in the downside [I].**
   - **Deferral:** paying 91% with 50% deferred for 12 months, instead of 87% cash, lifts IRR from 14.3% to 15.3% but cuts MOIC from 1.47x to 1.41x. After a −30% mark-down it lowers IRR from 2.5% to 1.3%.
   - **Treatment for ADIC:** a deferred payable is debt. It belongs in ADIC's leverage budget (stream 06) and in Tier-1 liquidity as a hard outflow.

7. **The opportunity is countercyclical; ADIC's liquidity is procyclical.**
   - **Discounts peak when buyer capital is scarce [S]:**
     - the average high bid fell to 61% of NAV in H2-2008;
     - the 2009 broker-sample mean price was 54%;
     - 2020 LP-led volume fell 47%.
   - **ADIC's position:** that is also when ADIC's distributions, payout and overlay margin squeeze it (streams 04 and 09).
   - **Value of dry powder [I]:** in a stylised grid, idle reserve capacity only adds value when stress is likely (20% a year), the stress-deal NPV is large (25%) *and* ADIC's stress liquidity premium is low (ℓ_S = 0). There it adds +2.0% per dollar per year. This agrees with stream 06's estimate of about 20bp a year.

8. **In a DPI drought, the group's main value is duration rotation and price discovery, not volume buying [I].**
   - **The rotation trade:** sell young, back-ended interests near par (a stream 05 decision) and selectively buy mature interests at deep discounts. This turns the private book toward cash.
   - **Cash effect:** for each 100 of NAV, 3-year cumulative net cash flow is +65 for the mature profile and +0.2 for the young one.
   - **LAPV effect:** under stream 08's liquidity curve (9% / 9% / 4%), a mature buyout interest is worth about 83% of NAV to ADIC. That is **below** the 87-91% market price. While ADIC's ℓ is high, the group should buy only deep-discount, complex or structured deals.

9. **Pricing desk and internal crosses.**
   - **The desk:** the group should publish calibrated, time-stamped predictive distributions of clearing prices for every PE-group holding, scored with CRPS.
   - **Internal crosses:** a transfer from the PE group to the Secondaries group is zero-sum at the total-portfolio level, apart from costs. It must never count as liquidity. Price it only through an external competitive process, under governance modelled on SEC Rule 17a-7, ILPA CV guidance and bank independent price verification [S/I].

10. **Specification.** §6 ends with a specification card. It covers:
    - three position templates: purchased LP interest, secondary-fund commitment, CV stake;
    - the return decomposition;
    - the regime table;
    - the LAPV buy rule and reserve rule;
    - the pricing-desk protocol;
    - defaults with sources.

---

## 2. Core concepts and theory

### 2.1 Taxonomy of the book

| Sub-book | What ADIC owns | Cash-flow signature | Key risks |
|---|---|---|---|
| **S1** Secondary-fund commitments | LP interest in funds that buy LP stakes and CVs | Calls over ~4 years; early distributions; two fee layers | Vintage-regime price; manager selection; fund leverage |
| **S2** Evergreen units (optional) | Units with periodic redemption | Fully funded; about 5% of NAV per quarter, gated in stress [S] | Incentive fees on accretion; gating |
| **S3** Direct LP-interest purchases | Single positions or diversified portfolios | Immediate NAV; small unfunded; deferred payables | Information asymmetry; tail quality; GP consent and ROFR |
| **S4** SACV stakes | Lead or syndicate equity in one company | Bullet exit at 3-6 years; follow-on reserve | Concentration; GP on both sides; winner's curse |
| **S5** MACV stakes | 3-10 companies | Earlier DPI than SACVs [S] | Adverse selection on mixed-quality assets |
| **S6** Other | Preferred equity, tenders, strips, secondary directs | Varies | Legal and structuring; overlap with Capital Solutions |

Evercore's definitions [S]:
- **LP-led** = LP portfolio sales, managed funds and LP preferred equity.
- **GP-led** = SACVs, MACVs, GP-led preferred equity and tender offers.
- **Volume** = purchase price plus unfunded commitments.

### 2.2 Buyer economics: price, NAV and value

A buyer pays $P^{ce}=p\,N^{ref}+\sum_{\tau\in(ref,0]}(C_\tau-D_\tau)$ (cash-equivalent), assumes unfunded $U$, and then receives $D_t-C_t$.

- **Economic value:** $V_0=\mathbb E^m[\sum_t m_t(D_t-C_t)]$, with $\theta=V_0/N^{ref}$.
- **Economic gain at purchase:** $G_0=(\theta-p)N^{ref}$.
- **The headline discount** $(1-p)$ overstates the gain whenever $\theta<1$.

**Decomposing θ [I]:**

$$\theta=\underbrace{e^{\beta r^m_{ref\to0}}}_{\text{staleness}}\times\underbrace{q}_{\text{mark quality}}\times\underbrace{(1-f)}_{\text{fee/carry not in NAV}}$$

- **Staleness** had a factor of about 0.73 in the GFC: the 61% average high bid against 83.5% on a public-market-adjusted basis [S: Cogent via Unquote; stream 05].
- **Quality** is lower than 1 for tail-end funds. Sellers of 10+ year funds beat buyers on PME, consistent with overstated residual NAVs [S: Nadauld et al.].

**Expected excess return.** With cash-flow duration $D$:

$$y_P-y_V\approx(\theta/p)^{1/D}-1 .$$

For p = 0.87 and D ≈ 3.4 years, this is +4.2% a year at θ = 1 and +2.6% a year at θ = 0.95. The full projections in §4.6 agree to within about 0.7pp [I].

### 2.3 Why discounts exist

- **Cash-in-the-market and fire sales.** With limited participation, small liquidity shocks can cause large price moves [S: Allen & Gale 1994]. Forced sellers meet buyers who are themselves constrained [S: Shleifer & Vishny 2011].
- **Microstructure [S: Nadauld et al.].**
  - Discounts and the buyer-seller return gap are larger for small funds and small deals, which points to information costs.
  - Both are also larger when P/E ratios are low and capital is scarce, which points to market depth.
  - Tail-end discounts of about 10% persist under time fixed effects.
- **Liquidity provision.** In a broker's bid data, the demand response to aggregate liquidity shocks is negatively related to contemporaneous bids, more so for funds likely to be offered when liquidity is low, and unrelated to future NAV returns. The authors conclude that discounts track liquidity provision [S: Albuquerque, Cassel, Phalippou & Schroth 2018, SSRN abstract]. The further specifics (2009-2016 bid data; stronger effects for young funds, in high-VIX and high-funding-cost periods, and among non-specialised buyers) are not in the abstract and were not checked against the paper [C: search excerpt].
- **Equilibrium with heterogeneous LPs.** In Maurin, Robinson & Strömberg's theoretical model, funds with more illiquidity-tolerant LPs earn higher returns, and a secondary market narrows dispersion in fund returns but not in investor returns. These are model predictions, not empirical findings [S: Maurin, Robinson & Strömberg 2023].
- **Screening.** GPs use transfer restrictions to screen for "deep-pocket" LPs [S: Lerner & Schoar 2004].

**Implication [I].** A discount has two parts:
- a **liquidity premium**, which a long-horizon sovereign can harvest if its own ℓ is low. Outside stress it is probably small: in Bollen & Sensoy's LP valuation model, breakeven returns match observed average fund returns for moderately risk-tolerant LPs with PE allocations up to 40% [S: Bollen & Sensoy 2022, abstract];
- an **information or quality component**, which compensates for lemons and is not alpha.

The tail-end segment is mostly the second. The young-fund crisis segment is mostly the first.

### 2.4 Reported versus economic returns

**Accounting [S: IPEV 2025, §4.1-4.3].**
- ASC 820-10-35-59 to 62 lets an investor use NAV as fair value for an interest in a fund.
- Exceptions apply if the interest is actively traded, or if management has decided to sell it at an amount other than NAV.
- IPEV adds that buying at a discount "does not necessarily mean" the underlying fair values need to be adjusted.

**Consequences.**
- **Day-one gains.** Gains of $1/p-1$ are booked at once: +14.9% at p = 0.87 and +43% at 0.70.
- **Inflated early IRRs.** Since-purchase IRRs are extreme in the first quarters.
- **Incentive problems.** In evergreen vehicles, incentive fees on NAV gains are partly paid on accretion [I].
- **Researchers adjust for it.** Nadauld et al. drop transactions within four quarters of liquidation to avoid "a mechanically large 'paper' return" [S].
- **Press coverage.** The practice is called "NAV squeezing" and is described as permissible under GAAP [S: Fortune 2025].
- **Risk is understated.** A buyout index built on secondary transaction prices has a beta of about 1.8 and volatility of about 34%, against "quite low" betas and 14-20% volatility for NAV-based indices. NAVs are too smooth because they fail to reflect variation in discount rates [S: Boyer et al. 2023; figures from NBER WP 28691]. A book marked at NAV understates the risk in the group's exit values. [corrected 2026-10-18: "betas above 2, against below 0.5" are 2018 WP 25207 figures; the conclusion stands]

### 2.5 Leverage and deferred consideration (buyer side)

- **Deferral is a zero-coupon vendor loan.** Evercore says it "acts as a form of leverage, supporting buyer returns" and is usually settled within 12 months [S]. The implied rate solves $p_{cash}=\phi p_d+(1-\phi)p_d(1+r_v)^{-t_d}$ (stream 05).
- **Fund-level lines and facilities.** These raise IRR and add covenant risk.
  - ILPA asks for net IRR with and without the subscription line, a cap of 15-25% of uncalled capital and at most 180 days outstanding [S].
  - Secondaries-fund NAV facilities price at spreads mostly below 3%, with closing LTV of 25-50% in 57% of facilities and above 50% in 43%, and LTV sweeps in 83% [S: Proskauer FY-2025, via stream 05 verification].
- **CV-level leverage.** Subscription lines in CVs are used "alongside, or in certain instances in place of" syndicate capital [S: Jefferies].
- **For ADIC [I].** Every deferred payable or facility draw:
  - is debt in the leverage budget;
  - is a hard outflow in liquidity survival;
  - raises the volatility of equity in the position by about $1/(1-\text{LTV})$.

### 2.6 GP-led CVs: agency structure

- **The GP is on both sides.** Its incentives are crystallised carry, equitised carry and fee extension. It picks assets that price near NAV. Failed processes are dropped quietly, which creates survival bias [S: CFA Institute].
- **Process.**
  - The lead investor sets the price; syndicate investors are price takers.
  - The GP seeks LPAC approval and may obtain a fairness or valuation opinion [S].
  - The SEC's adviser-led secondaries rule was struck down by the Fifth Circuit on 5 June 2024 [S: CFA Institute].
- **Alignment terms [S].**
  - GP commitment is about 10% of commitments in North American CVs and about 5% in Europe (Jefferies).
  - The GP rolls 100% of accrued carry "in almost all cases" (ILPA 2023).
  - Super-carry appears in more than one-third of GP-led deals (Evercore).
  - Fees can be low. In the CFA Institute report's own example, the lead pays 60bp in management fees against 75bp for the syndicate (p. 21). The report then cites Rode, Poldauf & Fuentes Perez (2025, p. 5) for overall CV fees that "can be significantly less than those for primary funds" [C: CFA Institute; Schroders Capital, ref 39]. Schroders' web summary puts CV management fees at "roughly half of those of traditional buyouts" and gives no basis-point figures [unverified: the 60bp / 75bp split was not found at source; the 15-page report cited at p. 5 was not read].
- **Status-quo options are rare.** A true status-quo option appeared in 22% of 2024 CVs and a modified one in 19%; the reinvestment option appeared in 59% [S: William Blair via CFA Institute].
- **Guidance is in flux.** ILPA's draft new CV guidance was published on 2026-06-24, with comments closing 2026-08-05; final guidance is "to be published later this year" [S].
- **For the buyer [I].** The economics combine positive selection (assets GPs "wish to 'buy again'" [S: Evercore/HEC]), a winner's curse in competitive leads, and concentration risk.

### 2.7 Dry powder as a real option

Buying opportunity $j$ in state $s$ creates value iff

$$\sum_{s',t}\pi_{s',t}CF_{j,s',t}\ge\pi_{s,0}P^{ce}_j ,$$

which is roughly $NPV_{j,s}\ge\ell_s$. The value of holding one more dollar of capacity is

$$OV_t=\mathbb E_t\Big[m_{t,t+1}\sum_k\big(NPV^k_{s_{t+1}}-\ell_{s_{t+1}}\big)^+\mathbf 1\{\text{capacity binds}\}\Big]-\text{carry}_t .$$

- **Corporate analogue.** Constrained firms hoard cash and time markets when financing costs vary [S: Bolton, Chen & Wang 2013].
- **ADIC's difficulty [I].** For ADIC, $\ell_s$ and $NPV_s$ are positively correlated, so the option is worth less than it is to a dedicated secondary fund, whose LPs bear the calls.

### 2.8 Internal transfers are near zero-sum

A PE-to-Secondaries transfer changes ADIC's total wealth and liquidity only by its costs. Advisory, legal and transfer costs are typically 0.5-1% of price [I]; intermediary fees are about 1%, paid by the seller [S: Nadauld et al.]. What it does change is group attribution, which invites transfer-pricing manipulation. It is a miniature of the GP-led CV conflict [I].

---

## 3. Methods and models, with trade-offs

### 3.1 Position engines (built on stream 04's RFT-TA)

**(a) Purchased LP interest.** Initialise stream 04's regime-switching, factor-driven, time-changed Takahashi-Alexander (RFT-TA) engine at purchase with:
- age $a_0$ and effective age $a^e_0$;
- $V_0=\theta N^{ref}$;
- $U_0$ and quality $q_0$;
- the deferral schedule $B^{def}$.

$$V_{t+1}=V_te^{r_{t+1}}+C_{t+1}-D_{t+1},\quad C_{t+1}=(1-e^{-\lambda^C_t\Delta})U_t,\quad D_{t+1}=(1-e^{-\delta_t\Delta})V_te^{r_{t+1}}\zeta_{t+1}$$

$$\delta_t=\bar\delta(a^e_t)\,m^D(s_t)\,e^{\kappa^DX_t+\varsigma(q_t)},\qquad \Delta q=-\chi D/V .$$

- Exit proceeds for funds older than 10 years sit below marks ($\mu_e<0$; stream 04, E7).
- Never-called commitment rises with age.

**(b) Secondary-fund commitment (two layers).**
- *Fund layer:*
  - calls $C^F_t=c\,U^F_t+\text{Fee}_t$, with $c$ about 45% a year of remaining unfunded for 4 years;
  - fees about 1% on commitments, then on NAV [C];
  - European waterfall with an 8% pref, catch-up and 10-12.5% carry [C];
  - subscription-line delay ≤180 days; recycling allowed.
- *Asset layer:* purchases at $p_{s(t)}$, so **the vintage regime fixes the discount**. Each purchase then follows engine (a).
- *Calibration:* NAV peaks at about 65% of commitment [S: Callan].

**(c) CV stake.**
- Exit hazard with a median of about 4.5 years. Buyers underwrite to a 4-year horizon [S: Evercore]. SACV companies were acquired in 2019 on average [S: Jefferies].
- Exit multiple:

$$M=\exp\big((\mu-\tfrac12\sigma^2)T+\sigma\sqrt T\varepsilon\big),\quad \mu=r_f+\beta\,\mathrm{ERP}+\alpha_{CV}$$

  - $\sigma_{SA}$ is 30-40% a year. BGG fund-level total risk is about 33% for buyout, and single assets are riskier [S/I].
  - Follow-on calls are $u\times$commitment.
  - Fees are 0.6-0.75% (as in the CFA Institute example, §2.6 [C]), with tiered carry of 12.5-20% [S/C].
- *MACV:* $\sigma_{MA}=\sigma_{SA}\sqrt{\rho+(1-\rho)/k}$, with earlier partial exits.

### 3.2 Pricing models

1. **Hedonic bid model** (stream 05): log price on regime, age, strategy, GP tier, PME, $U/N$, size, geography, software share and months since the reference date. Fit it with monotone constraints and hierarchical shrinkage. **The group's own deal-flow log is the decisive training set:** bids made, bids lost (with the clearing price when known) and deals won.
2. **Consensus index** (stream 05): a Kalman filter across Jefferies, Evercore, Lazard and Campbell Lutyens, with advisor-specific bias terms.
3. **Transaction-based risk index** for the risk of exit values [S: Boyer et al.].
4. **Winner's-curse haircut [I].** If $\hat V=V+e$ with $e\sim N(0,\sigma_e^2)$ and the group wins against $n$ similar bidders, then $\mathbb E[e\mid\text{win}]\approx\sigma_e\mathbb E[\max_{i\le n}Z_i]$. That is $0.85\sigma_e$ for $n=3$; about three bids per transaction were seen in 2010-14 [S: Nadauld et al.]. With $\sigma_e=5\%$ of NAV, the haircut is about 4.2%.

### 3.3 Return decomposition

Compute IRRs on the same cash-flow vector under different time-0 prices and financing:
- $y_N$: price $=N^{ref}$;
- $y_V$: price $=V_0$;
- $y_P$: price $=P^{ce}$;
- $y_{lev}$: with deferral and facility flows;
- $y_{gross}$ and $y_{net}$ for fund commitments.

Attribute:
- **headline discount** $=y_P-y_N$;
- **NAV error** $=y_V-y_N$;
- **economic discount** $=y_P-y_V$;
- **financing** $=y_{lev}-y_P$;
- **fees** $=y_{net}-y_{gross}$;
- **alpha**: direct alpha with transaction-based β.

IRR attribution is not additive, so ΔLAPV in dollars is the canonical decomposition. IRR deltas are shown for intuition [I].

### 3.4 Opportunity set

For each segment $k$ (diversified LP, single LP, tail-end, SACV, MACV, credit, infrastructure, venture), define regime-conditional:
- volume $Vol^k_s$;
- price $p^k_s$;
- θ;
- excess return $\alpha^k_s$;
- execution probability $e^k_s$.

ADIC capacity is $Q^k=\omega^kVol^k$, with $\omega^k$ = 3-5% [I]. Prices respond to depth and evergreen flow:

$$\log p^k_t=\log\bar p^k(s_t)+\gamma_K\log(K_t/Vol_t)+\gamma_EE_t+\varepsilon_t .$$

The ratio $K_t/Vol_t$ is a depth input, never a regime classifier, because it *rises* when volume collapses (3.1x in 2020; stream 05 verification, R1).

**Lag structure [I].** The opportunity peaks 2-6 quarters after a shock: H1-2020 volume was US$18bn, against US$42bn in H2-2020 [S].

### 3.5 Decision models

| Problem | Method | Trade-off |
|---|---|---|
| Buy and maximum bid | Scenario LAPV using stream 08 duals | Needs a solved portfolio LP; duals can be noisy |
| Secondary-fund pacing | MPC on linearised cohorts (Luxenberg et al.) | Misses the waterfall; validate by simulation |
| Reserve sizing | Dynamic programme or LSMC on (regime, ℓ, capacity) | Few crisis episodes; prior-driven |
| Tertiary sale or CV re-trade | Optimal stopping on $p$ paths (streams 05 and 08) | Price-path model risk |
| Pricing desk | Probabilistic forecasts scored with CRPS | Sparse ground truth |

---

## 4. Empirical evidence and current market data

### 4.1 Volume, US$bn

| Year | Evercore total (LP / GP) | Evercore start-of-year dry powder | Jefferies (H1 / H2) | Lazard | Campbell Lutyens |
|---|---|---|---|---|---|
| 2016 | 37 (26 / 11) | 65 | – | – | – |
| 2017 | 54 (37 / 17) | 90 | 58 | – | – |
| 2018 | 72 (49 / 23) | 77 | 74 | 75 | – |
| 2019 | 79 (53 / 26) | 77 | 88 | 83 | – |
| 2020 | 60 (28 / 32) | 96 | 60 (18 / 42) | 60 | – |
| 2021 | 134 (66 / 68) | 113 | 132 (48 / 84) | 126 | 135 |
| 2022 | 103 (55 / 48) | 105 | 108 (57 / 51) | 102 | 106 |
| 2023 | 114 (63 / 51) | 131 | 112 (43 / 69) | 109 | 111 |
| 2024 | 160 (89 / 71) | 166 | 162 (68 / 94) | 152 | 155 |
| 2025 | 226 (120 / 106) | 216 | 240 (103 / 137) | 233 | 225 |
| H1-2026 | 121 (56 / 65) | ~215 → 194 | 118 (56 LP / 62 GP) | 124 | – |

Sources [S]: Evercore FY-2025 and H1-2026; Jefferies Jan-2025 and Jul-2026; Lazard Interim-2026; Campbell Lutyens flash report.

**Forecasts and records [S].**
- 2026 forecasts: Evercore US$250-260bn; Jefferies about US$260bn; Lazard US$275bn (range US$255-295bn), with about US$305bn for 2027.
- Jefferies H1-2026 records: 15 LP deals above US$1bn, a record 5 above US$2bn, and more than 25 CVs above US$1bn.
- Ardian closed a record US$30bn secondary fund in January 2025 [S: CFA Institute].

### 4.2 Buyer capital

| Jefferies | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | H1-26 |
|---|---|---|---|---|---|---|---|---|---|---|
| Dedicated capital, US$bn | 125 | 192 | 155 | 188 | 236 | 225 | 255 | 288 | 327 | 290 |
| Overhang (capital ÷ LTM volume) | 2.2x | 2.6x | 1.8x | 3.1x | 1.8x | 2.1x | 2.3x | 1.8x | 1.4x | 1.2x |

**H1-2026 composition [S: Jefferies].** Equity dry powder US$143bn, near-term closed-end fundraising US$97bn, retail fundraising US$12bn and leverage US$38bn (estimated at 15% of dry powder plus fundraising) make up the US$290bn. Adding US$38bn of traditional LP capital gives US$328bn in total.

**Evercore [S].** Dry powder is US$194bn: LP-led US$90bn (−15% YTD) and GP-led US$104bn. The overhang multiple is about 1.0x, "healthy, but not abundant". H2 fundraising target: US$154bn.

**Concentration and entrants [S].**
- Top 10 buyers hold more than 50% of dry powder (Jefferies Jan-2025).
- 6% of investors hold about 43% of H2-2026 GP-led capital (Lazard).
- New entrants did 16% of 2025 volume and hold 21% of dry powder (Evercore).

**Evergreen [S].**
- Jefferies: FMV US$120bn, with 46% in secondaries; "nearly one-third" of 2024 secondary fundraising.
- Adoption: 53% of buyers run evergreen vehicles (Evercore); 40% (Lazard).
- Evercore notes they "typically invest alongside flagship funds" and that managers are capping subscriptions.
- 2026: redemptions and 5% gates (Jefferies).

**Institutional direct buyers [S: Jefferies].** Pensions, SWFs, insurers and endowments are "allocating internal resources to evaluate and underwrite continuation vehicles directly". This is ADIC's peer set.

### 4.3 Pricing

**LP-portfolio pricing (% of NAV, Jefferies averages):**

| Strategy | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | H1-26 |
|---|---|---|---|---|---|---|---|
| All | 86 | 92 | 81 | 85 | 89 | 87 | 87 |
| Buyout | 90 | 97 | 87 | 91 | 94 | 92 | 91 |
| Venture | 75 | 88 | 68 | 68 | 75 | 78 | 79 |
| Credit | 78 | 83 | 72 | 77 | 91 | 91 | 89 |
| Real estate | 76 | 79 | 71 | 71 | 72 | 70 | 68 |
| Infrastructure / energy | 82* | 93* | 83* | 87* | 90* | 90* | 91 |

Source [S]: Jefferies, cross-checked against stream 05's verified panel. *Read from chart text; the mapping is probable.

**By age and geography [S].**
- Buyout by age in 2024: 0-3 years 99%; 4-6 years 96%; 7-9 years 88%; 10-12 years 79%; 13+ years 70%.
- 2025: under 5 years 95%; over 10 years 73%.
- H1-2026: tail-end discounts of 25% or more; Asia and EM 35% or more; North America and Europe 86-88%.
- Weighted-average vintage sold: 2018.
- Evercore's H1-2026 LP-led vintage split: pre-2015 9%, 2015-17 17%, 2018-20 40%, 2021-23 30%, post-2023 4%.
- Evercore: tail-end "roughly 70% since 2022". Campbell Lutyens: value-weighted LP-led discount of 13.9% in 2025.

**GP-led pricing [S]:**

| Measure | SACV | MACV |
|---|---|---|
| Lazard, buyout CVs, 1H-26: share of volume at ≤80 / 81-90 / 91-95 / 96-100 / >100% of NAV | 1 / 12 / 5 / 59 / 23% (2025: 4 / 9 / 20 / 59 / 8%) | 13 / 26 / 10 / 43 / 8% (2025: 5 / 11 / 15 / 68 / 1%) |
| Evercore H1-26: below / at / above par | 34 / 52 / 14% | 71 / 22 / 8% |
| Campbell Lutyens 2025: average discount | 3.1% | 4.2% (2024: 9.0%) |

GP-led credit secondaries priced at about 99% of fair market value [S: Evercore].

**Buyer targets [S].**
- Evercore gross multiples over 4 years: SACV ~2.3x, MACV ~1.9x, single LP ~1.8x, diversified LP ~1.7x.
- Lazard 2024 SACV targets: 2.2x MOIC and 21.3% net IRR (via CFA Institute).
- Net-IRR targets: credit and infrastructure mostly 13-15%; venture mostly above 20% (Evercore).

### 4.4 Deferral and leverage

| Evercore H1-26 | None | 1-6m | 7-12m | 13-18m | >18m |
|---|---|---|---|---|---|
| LP-led (share of volume) | 66% | 3% | 20% | 2% | 9% |
| GP-led (share of volume) | 84% | 6% | 10% | 1% | 0% |

- **Deferred share of price, LP-led [S]:** 26-50% in 16% of volume; 51-75% in 12%; 76-100% in 5%.
- **Jefferies [S]:** 33% of H1-2026 LP sales were structured, 26% with deferral. Deferral raised prices by about 400bp in 2024.
- **Leverage [S: Evercore]:** use of third-party leverage by GP-led buyers rose from 7% of survey respondents (2024) to 14% (2025).

### 4.5 Return evidence

**Nadauld, Sensoy, Vorkink & Weisbach (700 fund-quarter transactions, 2006-2014; figures from NBER WP 22404, 2016) [S]:**

| Measure | All | Funds aged 4-9 years | Note |
|---|---|---|---|
| Buyer IRR, mean / median | 22.3% / 16.7% | 19.8% / 15.6% | ≥20% mean in every age group |
| Seller IRR, mean / median | 1.3% / 3.3% | 2.1% / 2.4% | Young funds −30% (49 of 92 sold in 2008-09) |
| Annualised PME, buyer / seller | 1.023 / 0.974 (*JFE* abstract: 0.976) | 1.013 / 0.983 | Tail-end: sellers > buyers |
| Price, % of NAV | mean 86.2%, median 85.6% | ~91% | 2009: mean 54% (213 deals) |

- 85.7% of buyers were funds of funds or secondary vehicles.
- The median deal was US$4.6m of NAV.
- A one-standard-deviation higher PME goes with a 2.5% higher price.
- **ADIC-scale caveat [I].** ADIC trades in tickets of US$100m to US$1bn, and larger deals carry lower costs, so ADIC should expect a smaller premium.

**Other evidence.**
- **Boyer et al. [S].** In NBER WP 28691 (2021), the readable version of the published *JF* paper, the all-ages secondary-market buyout index has a beta of 1.79 (1.94 with log returns) and averaged 14% a year (22% for funds aged 4-9 years), with volatility of about 34%. NAV-based indices averaged 11-14% with 14-20% volatility and "quite low" betas (0.73-0.85 even with seven Dimson lags). The index's CAPM alpha is about zero (−2% a year; near zero with log returns), as the *JF* abstract states, while cash-flow-based GPMEs are large and positive. [corrected 2026-10-18: "a beta above 2, against below 0.5 for NAV-based indices" and "about 20% a year" are 2018 WP 25207 figures; *JF* full text not accessed]
- **Callan, Mar-2025 (LSEG/Cambridge data) [S].**
  - Pooled TVPI for primaries exceeds secondaries by 0.38x; IRRs are similar.
  - Secondaries did better around dot-com and COVID and show lower dispersion.
  - NAV peaks at about 65% of commitment for secondaries, against about 95% for primaries.
  - In a 20-year simulation, an all-primary programme reaches 1.65x and an all-secondary one 1.35x.
  - 2024 secondary fundraising was about US$100bn.
- **Funds of funds [S: Harris, Jenkinson, Kaplan & Stucke 2018].** Buyout FoFs beat public markets but trail direct fund investing. This is the double-fee analogue for S1.
- **CVs.**
  - HEC/Gottschalg [S]: 386 CVs (2018-23), 297 with performance data. Little difference by industry, market or type; single-asset CVs show "a narrower spread of outcomes". These are non-peer-reviewed HEC research papers based on interim, mostly unrealised marks.
  - Fourth HEC study [S: Evercore FY-2025]: 387 CVs. Simulated portfolios of SACVs ("portfolio sampling", N = 112) have a median TVPI of 1.48x and a normalised Gini of 0.280, against 1.26x and 0.581 for 2021-vintage buyout funds (N = 185). MACVs show earlier DPI.
  - Fifth HEC study [S: Evercore H1-2026]: TVPI variation "remains relatively limited", and top SACVs show upside from positive selection.
  - Morgan Stanley (2018-24) [C: CFA Institute, citing Buyouts]: median MOIC of 1.4x for CVs, against 1.3x for buyout. An earlier 71-CV Morgan Stanley study had about 85% of MOIC unrealised [C].
  - CFA Institute: "unaware of published rigorous studies" comparing GP expectations with CV outcomes [S].

### 4.6 Worked examples (synthetic, [I])

**Example A: what the discount buys.** Inputs: NAV 100; unfunded 8, called at 30% a year; asset return 9%; distribution intensities 22-85% over years 1-9; duration about 3.4 years.

| Buyer IRR (MOIC) | θ = 1.00 | θ = 0.95 | θ = 0.85 |
|---|---|---|---|
| p = 0.87 | 14.3% (1.47x) | 12.3% (1.41x) | 8.2% (1.27x) |
| p = 0.80 | 17.8% (1.59x) | 15.6% (1.52x) | 11.2% (1.37x) |
| p = 0.70 | 23.9% (1.80x) | 21.5% (1.71x) | 16.5% (1.54x) |

- Benchmark at p = θ = 1: 9.0%.
- Reported IRR one quarter after buying at 0.87 and marking to NAV: 90% annualised (166% at 0.80).

**Examples B and C: structures (θ = 1).**

| Structure | Base IRR / MOIC | After −30% in quarter 2 |
|---|---|---|
| 87% cash | 14.3% / 1.47x | 2.5% / 1.08x |
| 91%, 50% deferred 12 months (implied vendor rate 9.6%) | 15.3% / 1.41x | 1.3% / 1.03x |
| 87% cash plus 30% LTV at 6.75%, 100% sweep | 15.0% / 1.52x (equity) | 2.1% / 0.97x (equity) |

**Example D: secondary-fund commitment.** Inputs: purchases at p = 0.88 with θ = 0.97; calls 45% a year for 4 years; fees 1% / 1%; 12.5% carry over an 8% pref.
- Net IRR **11.0%**; gross before fund fees 14.2%; net TVPI **1.31x**.
- DPI reaches 1.0x in **year 6**. NAV peaks at **65% of commitment** in year 3.
- θ = 1: 12.3% net IRR, 1.35x.
- Stress-vintage purchases (p = 0.80, θ = 0.95): 14.2%, 1.40x.
- **Drought** (distribution intensities halved): net IRR 9.6%, DPI 1.0x only in **year 8**, NAV peak 90% of commitment. The faster-DPI advantage largely disappears.

**Example E: SACV.** Price = NAV; median hold 4.5 years; fees 0.75% plus 15% carry over 8%.

| μ, σ | Median gross MOIC | Median net MOIC | P(net < 1x) | P(net < 0.5x) | Share reaching 2.3x gross |
|---|---|---|---|---|---|
| 14%, 25% | 1.63x | 1.52x | 19% | 2% | 27% |
| 14%, 35% | 1.42x | 1.36x | 33% | 9% | 26% |
| 10%, 35% | 1.19x | 1.16x | 42% | 14% | 19% |

The 2.3x target is roughly a top-quartile outcome, not an expectation.

**Example F: reserve.** Gain from holding $1 of capacity for one year rather than deploying it now at a 4% NPV, with a 2% a year carry cost:

| | ℓ_S = 0 | ℓ_S = 10% | ℓ_S = 20% |
|---|---|---|---|
| p_S = 10%, NPV_S = 15% | −1.2% | −2.2% | −2.7% |
| p_S = 10%, NPV_S = 25% | −0.2% | −1.2% | −2.2% |
| p_S = 20%, NPV_S = 15% | −0.0% | −2.0% | −3.0% |
| p_S = 20%, NPV_S = 25% | **+2.0%** | −0.0% | −2.0% |

**Example G: duration rotation.** Two interests, each with NAV 100 and asset return 9%: a young one (40 unfunded, back-ended) and a mature one (8 unfunded).
- **LAPV at a 9% hurdle** under ℓ = 9%, 9%, then 4%: young **70.0**, mature **82.6**. With ℓ = 0, both are 100.
- **Rotation.** Sell young at 97, buy mature at 87, 1% costs on each leg. Gain: +20.8 per 100 of NAV with ℓ > 0, and +8.2 with ℓ = 0. The ℓ = 0 gain exists only if both NAVs are fair; with θ_mature = 0.90 it becomes −1.8.
- **Three-year cumulative net cash flow:** young +0.2, mature +65.4.
- **Reading.** The value is mostly in the sale leg, which belongs to stream 05. At ℓ > 0 the purchase leg alone has negative LAPV.

### 4.7 Stress episodes

| Episode | Volume | Pricing | Buyer behaviour |
|---|---|---|---|
| 2008-09 | Fell sharply [C]; the broker sample kept 213 deals in 2009 at deep discounts [S] | Average high bid 84.7% → 61% (H1 → H2-2008), 83.5% adjusted [S]; 2009 mean 54% [S]; average discount 35% [C: WSJ via Wikipedia] | MAC walk-aways; 3+ month transfers [S: WilmerHale] |
| 2020 | LP-led US$28bn vs US$53bn (−47%); GP-led up to US$32bn [S] | All 86%, buyout 90% [S] | Overhang 3.1x [S] |
| 2022-23 | LP-led US$55bn / US$63bn [S] | 81% / 85%; venture 68% [S] | Reset, then recovery |
| Apr-2025 | – | −300 to −500bp, recovered within the quarter [S: Jefferies] | Transient |
| 2026 software repricing | Records continue | ~60% of buyers say GP marks moved only modestly [S: Lazard] | ~27% of GP-led processes failed or paused; evergreen gates [S] |

LP portfolios' distribution yield was about 10% in H1-2026. It has been below 20% since 2023, against an average of 25% since 2001 [S: Jefferies].

### 4.8 The tertiary market (the group as seller)

- Funds of funds and secondary funds supplied 27% of H1-2026 LP sell-side volume [S: Jefferies]. FoFs were 23% of 2025 LP-led sellers [S: Evercore].
- FoF and secondary interests were about 7% of H1-2026 LP volume by strategy [S: Jefferies; chart reading probable], and about US$3.2bn in 2025 [S: Campbell Lutyens; chart reading].
- CV-to-CV exits are emerging as a "credible realization path for trophy assets" [S: Lazard].

---

## 5. Practitioner and peer practice; case studies

1. **The dedicated-fund model.** Funds deploy over about 4 years, use deferrals and facilities, and target 1.7-2.3x gross [S]. They are increasingly multi-strategy: available capital for credit is US$37bn, infrastructure US$20bn and venture US$10bn [S: Evercore FY-2025]. For S1, manager and vintage selection dominate, and fees cost about 3pp of IRR (Example D) [I].
2. **The evergreen model.** Evergreen vehicles need to deploy immediately and want "exposure to seasoned assets" with "predictable cash flow profiles" [S: Jefferies]. 2026 showed the reverse side: redemptions and gates. **Lessons for ADIC [I]:** LP-led diversified buyout is crowded and priced by low-hurdle capital, and stress depth is thinner than headline capital suggests.
3. **Institutional LPs as direct buyers.** Sovereigns and pensions are building internal CV underwriting [S: Jefferies]. **Lesson [I]:** ADIC can lead CVs only with sector-specialist underwriting, shared with the Co-investment group.
4. **Sovereigns on both sides.** SWFs were 21% of H1-2026 LP-led supply [S: Evercore]. A sovereign that sells primaries at auction while buying elsewhere is coherent only as a **net seller of duration**, selling young and back-ended interests and buying mature, discounted ones (Example G) [I].
5. **GP-led practice.** Competitive lead selection, LPAC review, and a fairness or valuation opinion or partial third-party price discovery are standard [S]. Status-quo options are a minority [S]. Stapled primary commitments are accepted, but taking a lower lead bid in exchange for a staple is regarded as unethical [S: CFA Institute].
6. **Case: 2008-09.** Buyers with capital earned the largest premia (young-fund PME gaps of about 25pp a year), but some signed deals failed under MAC clauses and pricing came off stale NAVs [S]. **Lesson [I]:** stress buying needs pre-arranged capital, pricing on staleness-adjusted value and legal readiness (GP consent, ROFR).
7. **Case: 2020.** LP-led volume collapsed while GP-led grew. H2 volume was 2.3x H1 [S]. **Lesson [I]:** the opportunity rotates *within* secondaries, so segment allocation should be dynamic.
8. **Governance analogues for internal crosses [S].**
   - SEC Rule 17a-7: cross trades only at an "independent current market price", for cash, with no remuneration, under board procedures and at least quarterly review.
   - BCBS (2009): independent verification of fair values.
   - ILPA: price checks for GP-conflicted transfers.

   No public description of peer sovereigns' internal-cross policies was found (§9).

---

## 6. Design implications for the ADIC framework

### 6.1 Book representation (SYNTHETIC; replace with ADIC data)

| Sub-book | NAV (US$bn) | Unfunded (US$bn) | Ages | Template |
|---|---|---|---|---|
| S1 Secondary-fund commitments (10 funds, vintages 2017-25) | 5.6 | 2.6 | Fund ages 1-9 | (b) |
| S3 Direct LP-interest purchases | 4.6 | 0.5, plus 0.4 deferred payables | Underlying ages 4-12 | (a) |
| S4 SACVs | 2.0 | 0.2 follow-on | CV ages 0-5 | (c) |
| S5 MACVs | 1.4 | 0.1 | CV ages 0-5 | (c), k = 5-8 |
| S6 Other | 0.4 | 0.1 | – | Case by case |
| **Total** | **14.0** | **3.5 + 0.4** | | |

Default annual deployment: US$3-4bn, about 1.5% of market volume [I].

### 6.2 State variables

**Per position:**
- $N^{ref}$ and reference date;
- $V$ and θ;
- $U$;
- age $a$ and effective age $a^e$;
- quality $q$;
- cost $P^{ce}$;
- deferral schedule $B^{def}$;
- strategy, GP, vintage, geography and look-through (software share);
- CV alignment: GP commitment percentage, carry roll, status-quo option, super-carry;
- fee and carry terms;
- underwritten, actual and forecast cash flows (UW / ACT / SG);
- bid distribution $F(p)$ and execution probability $e$.

**Book level:** facility balance $B^{fac}$, LTV and covenant headroom; reserve $R$.

**Global:**
- regime $s_t\in\{B,N,D,C\}$ (stream 04), plus a post-shock window flag $W_t$ (quarters 2-6 after entering C);
- exit factor $X_t$;
- consensus price index $\Pi^k_t$;
- buyer capital $K_t$ and evergreen flow $E_t$;
- ADIC's duals $\pi_{s,t}$ and $\ell_{s,t}$.

### 6.3 Decision variables (per quarter)

- $n^{SF}_t$: secondary-fund commitments.
- $x^{buy}_{j,t}$: share of opportunity $j$ taken, with bid $b_j$ and structure (cash, or deferral $\phi$ and $t_d$).
- $x^{sell}_{i,t}$: tertiary or strip sale.
- $b^{fac}_t$: facility draw or repayment.
- $R_t$: reserve for the stress window.

Internal crosses are governance events, not optimiser variables.

### 6.4 Key equations

**G2-E1. Price.** $p_{j,t}=\Pi^{k}_t\,g(\text{age},\text{geo},q,\text{size},U/N,\text{software})\,h(s_t)e^{\varepsilon}$, and $p^{ce}=\phi p_d+(1-\phi)p_d(1+r_v)^{-t_d}$.

**G2-E2. Entry value.** $V_{j,0}=N^{ref}_je^{\beta r^m_{ref\to0}}q_j$. Use either de-smoothing or a staleness-inclusive crisis price, never both (stream 05 verification, R5).

**G2-E3 to E5.** Templates (a)-(c) in §3.1.

**G2-E6. Accretion.**
- Book value: $N^{book}=N^{GP}$.
- Day-one accretion: $A_0=N^{ref}-P^{ce}$.
- Report the accretion share of cumulative reported gain, alongside the economic mark $\hat V$ and the exit mark $\hat pN$.

**G2-E7. Three return series.**
- **UW** $=\mathrm{IRR}(-P^{ce},CF^{UW})$.
- **ACT:** three versions, each the IRR of actual cash flows plus a terminal mark:
  - reported, with $+N^{book}$;
  - economic, with $+\hat V$;
  - exit, with $+\hat pN$.
- **SG forward:** solve $\sum CF^{SG}_\tau(1+y)^{-(\tau-t)}=\hat V_t$.
- **Buyer-implied** $y^{MKT}$: the same with $\hat p_tN_t$.

**G2-E8. Decomposition.** As in §3.3; ΔLAPV is canonical.

**G2-E9. Deferral and facility.** Deferred payables are scheduled hard outflows. Facility LTV follows stream 05's corrected recursion.

**G2-E10. Opportunity set.** $Q^k_{s,t}=\omega^kVol^k_{s,t}$, with the price equation of §3.4. Execution outcomes are Bernoulli draws correlated within a regime (stream 05 verification, R2).

**G2-E11. Buy rule.**

$$b^*_j=\frac{\sum_{s,t}\pi_{s,t}CF_{j,s,t}-\lambda_R\Delta\mathrm{CVaR}_j-\lambda_{Lev}\Delta Lev_j-\kappa^{conc}_j-\kappa^{wc}_j}{\pi_0N^{ref}_j}$$

Buy iff $b^*_j\ge p^{ce}_j$.

**G2-E12. Reserve.** Deploy now iff $NPV_{now}-\ell_{now}\ge OV_t$. Pace secondary-fund commitments by MPC, with stressed calls priced at $\pi_{s,t}$.

**G2-E13. Pricing desk.** For each PE holding, publish $F_{i,t}(p)$. Score with $\mathrm{CRPS}=\int(F(x)-\mathbf 1\{x\ge p^{obs}\})^2dx$, and report skill against the consensus-only benchmark and the bias $\mathbb E[\hat p-p^{obs}]$.

**G2-E14. Internal cross.** $\Delta W=\Delta\text{Liquidity}=-c_{tx}$. Attribute at the external clearing price.

### 6.5 Constraints (defaults for IC calibration [I])

1. **Group size.** NAV of 6-10% of total.
2. **Market capacity.** Deployment ≤ 3-5% of LTM segment volume, haircut in stress.
3. **Look-through concentration (PE + Co-investment + Secondaries):**
   - per GP ≤ 5% of private NAV;
   - per company ≤ 1% of total NAV;
   - SACVs ≤ 25% of group NAV.
4. **Deferred payables** ≤ 10% of group NAV, counted as debt (stream 06).
5. **Unfunded plus deferred** ≤ 35% of group NAV. Unfunded commitments also carry a priced commitment risk that a deeper secondary market does not remove. In Gourier, Phalippou & Westerfield's model, investors would pay more to adjust commitment amounts than to remove timing uncertainty or limited tradability, and the risk premium rises with secondary-market liquidity and persists across many funds [S: Gourier, Phalippou & Westerfield 2024, abstract].
6. **Tier-1 survival** includes:
   - secondary-fund calls at stress multipliers (acute 0.7x, window 1.3x);
   - CV follow-ons;
   - deferred payables at 100%;
   - facility sweeps.
7. **Facility covenant chance constraint** (stream 05).
8. **CV gates:**
   - GP commitment ≥ 5% of CV equity, or a 100% carry roll;
   - competitive price discovery, or a fairness or valuation opinion;
   - LPAC process followed;
   - no price concession in exchange for a staple.
9. **Internal crosses** are excluded from liquidity sources and need IC approval with an external price.

### 6.6 Objective

- Group actions enter only through total-portfolio wealth and the Tier-1/Tier-2 objectives (streams 01 and 11).
- Add no separate discount or liquidity penalties (stream 05 verification, R3). Only non-cash penalties are added: relationship, signalling, concentration.
- **Reported KPIs, not optimised:** economic IRR, accretion share, direct alpha (transaction β), DPI speed, LAPV contribution, desk CRPS skill.

### 6.7 Regime-dependent opportunity set

All values are defaults [I]; anchors in brackets.

| Regime | LP-led volume vs 2025 | p, diversified buyout | p, tail-end | θ, diversified / tail | Excess α (annual, on economic value) | Execution probability | ω |
|---|---|---|---|---|---|---|---|
| B (window open) | 1.0-1.2x | 0.94-0.97 [2021: 97%] | 0.80 | 1.00 / 0.92 | 0-1% | 0.85 | 3% |
| N (normal) | 0.8-1.0x | 0.90-0.93 | 0.75 | 0.98 / 0.90 | 1-2% | 0.80 | 3% |
| D (drought, now) | 1.0-1.1x | 0.87-0.91 [91%] | 0.70-0.75 [S] | 0.96 / 0.88 | 2-3% diversified; 3-5% complex | 0.70-0.75 [27% failed or paused] | 4% |
| C (acute, 1-3 quarters) | 0.4-0.6x [−47% / −60%] | 0.55-0.70 on stale NAV [61%; 54%] | 0.40-0.50 | 0.80 / 0.70 | High ex post; small capacity | 0.40-0.55 | 2% |
| W flag (quarters 2-6 after C) | 0.8-1.0x, rising [H2/H1-2020 = 2.3x] | 0.75-0.85 | 0.60 | 0.92 / 0.82 | 4-8% | 0.65 | 5% |

**Group cash-flow multipliers (relative to N):**

| Regime | Secondary-fund calls | Mature distributions | CV exit hazard |
|---|---|---|---|
| B | 1.2 | 1.2 | 1.3 |
| D | 1.0 | 0.5 [10% vs 25% yield, S] | 0.7 |
| C | 0.7 | 0.35 | 0.4 |
| W | 1.3 | 0.6 | 0.8 |

### 6.8 Calibration targets

1. Secondary-fund NAV peak about 65% of commitment; pooled TVPI gap about −0.38x [S: Callan].
2. Buyer-seller PME gaps: about 3pp for funds aged 4-9; about 0 for tail-end; about 25pp for young funds in crisis [S].
3. Jefferies pricing panel by strategy, age and geography; Lazard, Evercore and Campbell Lutyens GP-led buckets [S].
4. Crisis anchors: 61% (83.5% adjusted) in H2-2008; 54% mean in 2009; LP-led −47% in 2020 [S].
5. Deferral incidence of 26-34% and its tenor and amount mix [S].
6. CV dispersion: simulated SACV portfolios' Gini about 0.28 against 0.58 for buyout funds; MACV DPI earlier than SACV [S].
7. Transaction-based buyout β of about 1.8-1.9 [S: Boyer et al., NBER WP 28691; corrected 2026-10-18 from "above 2", a 2018 WP 25207 figure].
8. Distribution yield of about 10%, against 25% long-run [S].
9. ADIC data: realised against underwritten returns ($b_{UW}$), and desk quotes against later prices.

### 6.9 Data needs (from ADIC)

- Position holdings with reference NAVs, cash-equivalent cost, deferral schedules, unfunded, cash-flow history and company look-through.
- Dated underwriting models (base, downside, upside).
- The deal-flow log: every opportunity seen, bids, outcomes, clearing prices if learned, number of bidders, structures.
- Secondary-fund LPAs: fees, carry, recycling, leverage.
- CV documents: GP commitment, carry roll, status-quo option, fairness opinions, LPAC minutes.
- Facility terms.
- Internal-cross history and current policy.

### 6.10 SPECIFICATION CARD (G2 Secondaries)

| Item | Specification |
|---|---|
| **Data fields** | id; sub-book S1-S6; GP; fund; vintage; strategy; geography; ref-NAV and date; quarterly GP NAV; cost $P^{ce}$; deferral schedule; unfunded; dated cash flows; look-through; fees and carry; CV alignment (GP commitment %, carry roll, status quo, super-carry); UW and SG cash-flow vectors with dates; bid distribution $F$; execution probability; encumbrance |
| **Cash-flow equations** | (a) RFT-TA from purchase state; (b) two-layer fund: calls 45% a year of remaining unfunded for 4 years, fees 1% / 1%, European 8% pref with 10-12.5% carry, over engine (a); (c) CV: exit hazard with median 4.5 years, lognormal multiple (μ = r_f + βERP + α, σ_SA = 35%, MACV $\sigma\sqrt{\rho+(1-\rho)/k}$), 10% follow-on reserve, fees 0.6-0.75% plus 12.5-20% tiered carry |
| **Return equations** | $y_N, y_V, y_P, y_{lev}, y_{gross}, y_{net}$; accretion $A_0=N^{ref}-P^{ce}$; excess ≈ $(\theta/p)^{1/D}-1$; alpha via direct alpha with transaction β (≈1.8-1.9 for buyout exit values [S: Boyer et al.; corrected 2026-10-18 from ≈2]; cash-flow β 1.05-1.25 [S, stream 04]) |
| **Parameter defaults** | Price, H1-26: buyout 0.91 / venture 0.79 / credit 0.89 / infrastructure 0.91 / real estate 0.68; <5 years ≈0.93-0.97; 10+ years ≤0.75; Asia/EM ≤0.65 [S: Jefferies]. SACV ≈1.00, MACV ≈0.95 [S: Evercore, Campbell Lutyens, Lazard]. θ: 0.96 (4-9 years), 0.88 (10+ years) [I, anchored on Nadauld et al.]. Mature distribution intensity: 22-25% normal, ~10-12% drought [S/I]. Buyer targets 1.7 / 1.8 / 1.9 / 2.3x over 4 years [S]. Deferral vendor rate ≈9.6% [I]. Winner's-curse haircut 0.85σ_e, σ_e = 5% [I]. ω = 3-5% [I] |
| **Liquidity and stress** | Transfers need GP consent and ROFR, 3-6+ months [S]. Tertiary price = hedonic minus FoF discount. Crisis multiplier about 0.85 on staleness-adjusted value, never stacked with de-smoothing [I]. Deferred payables: 100% hard outflow. Secondary-fund calls: acute 0.7x, window 1.3x. Evergreen units: 5% a quarter, gated [S]. Facility: LTV covenants and sweeps |
| **SELL** | Tertiary sale of fund interests; re-sale of LP interests; CV stake sale or CV-to-CV exit; strips. Sell iff cash-equivalent bid ≥ LAPV(hold) + κ + waiting option (stream 08). Counts as liquidity only if the buyer is external |
| **HOLD** | Baseline paths; report economic and exit marks and accretion share |
| **REFINANCE** | Book-level secondaries facility (LTV 15-35%; secondaries-fund deals mostly <300bp spread [S: Proskauer]); preferred equity; Astrea-style CFO on a seasoned pool (stream 05); renegotiate deferral timing. Test: spread + $\lambda_{Lev}$ < life-weighted $\bar\ell$ (stream 08) |
| **LEVER** | Deploy above base pacing; accept buyer-side deferral; acquisition or subscription lines. Test: $b^*\ge p^{ce}$ (G2-E11) within the leverage cap; LEVER ≡ ADD + REFI |
| **PACE** | MPC for secondary-fund commitments. Reserve $R_t$ from $OV_t$; zero when ℓ_S ≥ NPV_S − carry |
| **Forecasts** | Deal underwriting (base, downside, upside) gives IRR and MOIC; GP projections plus look-through for funds; quarterly reforecast on economic value |
| **Typical biases** | (1) Targets used as expectations (about 26% of SACVs reach 2.3x, Example E). (2) Timing optimism. (3) Accretion counted as return. (4) Winner's curse (≈4% of NAV). (5) Gross vs net (≈3pp). (6) Anchoring on GP marks (software [S]). Correct by shrinking toward $y^{MKT}$ with stream 07 credibility weights |
| **Synthetic defaults** | Book as in §6.1; S1 vintages uniform 2017-25; S3 underlying ages 4-12; CV ages 0-5; stream 04 regime chain plus Table 6.7; every output labelled SYNTHETIC |
| **Links to other groups** | **PE:** pricing desk for SELL, rotation partner, cross governance, GP look-through. **Co-investment:** SACV overlap and single-name limits. **Capital Solutions:** owns preferred equity and NAV structures. **Private Credit:** credit secondaries booking. **Public Markets:** stress funding. **Overlay:** hedge exit-value β; tail-hedge payouts fund window deployment. **Treasury:** deferred payables and facility |

---

## 7. Implementation notes

**Libraries.**
- `numpy` and `pandas`; `numba` or `JAX` for paths.
- IRR: `scipy.optimize.brentq` on NPV with bracket search. Report NPV at the hurdle and MIRR too, because cash flows with calls produce multiple roots.
- `cvxpy` (Clarabel, HiGHS, MOSEK) for MPC and LAPV; OR-Tools for lumpy CV tickets.
- `PyMC` or `NumPyro` for the hierarchical hedonic model; `LightGBM` (monotone constraints) plus `MAPIE` for price intervals.
- `statsmodels` `UnobservedComponents` for the consensus index; `QuantLib` for facilities.

**Algorithms.**
- 5-10k common-random-number paths for decisions; cohorts for the 50k-path portfolio Monte Carlo (stream 04).
- Entropy pooling to apply IC scenario probabilities.
- LSMC for waiting and tertiary-sale options.
- CRPS: closed form for Gaussian forecasts, quantile-based otherwise.

**Pitfalls.**
1. Never mix since-purchase reported IRR with forward IRR. Exclude positions under 4 quarters old from performance tables (as Nadauld et al. do).
2. Apply reference-date adjustments, and measure θ from the reference date.
3. Use crisis prices on staleness-adjusted value or de-smoothing, never both.
4. Build one look-through exposure graph across PE, Co-investment, SACVs and secondary funds.
5. Book deferred payables as liabilities. They are not optional unfunded commitments.
6. Model selection: CV data are mostly unrealised, and failed processes (about 27%) are invisible.
7. Buyer targets are gross; S1 returns are net of two fee layers.
8. Do not deploy the reserve by rule in the acute quarter; use the W flag.

**Agent hooks (LLMs extract evidence; code computes the numbers):**
- deal-log extractor;
- accretion auditor;
- CV-alignment checker against the §6.5 gates;
- winner's-curse challenger;
- quarterly pricing-desk scorer reporting to the IC.

---

## 8. Risks, pitfalls and limitations

- **Illusory alpha.** Accretion inflates reported returns. With overstated NAVs (tail-end, software), economic returns can fall below the asset's own return (Example A).
- **Crowding and evergreen pro-cyclicality.** Low-hurdle capital compresses discounts, then withdraws through gates in stress [S]. Headline depth overstates stress depth.
- **Opportunity and need are correlated.** ADIC is tightest when discounts are widest. Dry powder pays only if funded by instruments that pay off in stress, such as tail hedges or committed lines.
- **Adverse selection and the winner's curse**, strongest in CVs and tail-end deals.
- **Concentration.** SACV P(net MOIC < 1) is 19-42% depending on σ (Example E).
- **Model and data risk.** Crisis calibration rests on 2008-09 and 2020. Advisor surveys are unaudited and use different definitions.
- **Governance and reputation.** If ADIC is both seller and buyer, internal crosses or round-trip perceptions can damage GP relationships.
- **Regulatory drift.** ILPA's final CV guidance is pending, the SEC rule was vacated, and evergreen valuation practice may change.
- **Limits of this dossier.** No Setter, PJT Park Hill, Preqin or PitchBook data, and no vintage-level secondary-fund benchmarks. Albuquerque et al. was read at abstract level. Several CV figures are second-hand [C].

---

## 9. Open questions (ADIC to supply or confirm)

1. What exactly are the group's "direct deals"? Where are the boundaries with Capital Solutions and Co-investment?
2. What is the actual book (S1-S6 NAV, unfunded, deferred payables, vintages, GPs)? Does the group hold evergreen units?
3. Does a deal-flow log exist with bids, outcomes, clearing prices and bidder counts?
4. What is the internal-cross policy? Have any PE-to-Secondaries transfers happened, at what price, and how were they attributed?
5. What is the group's leverage mandate (deferral, facilities, CV lines), and who owns that budget (stream 06)?
6. What is the appetite for SACV concentration, and how do single-name limits apply across groups?
7. Are secondary-fund LPA terms available for the S1 waterfall?
8. Should the group be ADIC's official pricing desk for SELL, and under what independence controls?
9. What reserve policy does the IC want, given that ℓ_S is high exactly when discounts are wide?
10. What are the realised outcomes of past purchases against underwriting, needed to estimate $b_{UW}$ and $b_F$?
11. Can Consensus access be authorised interactively for a systematic peer-reviewed sweep, for example on secondary-fund vintage returns?

---

## 10. References

**Market reports (primary; text-extracted locally unless noted)**
1. Jefferies (Jul-2026). *Global Secondary Market Review, July 2026.* https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
2. Jefferies (10-Feb-2026). *2025 Global Secondary Market Review: Another Record-Breaking Year* (figures via stream 05 verification). https://www.jefferies.com/insights/the-big-picture/2025-global-secondary-market-review-another-record-breaking-year/
3. Jefferies (Jan-2025). *Global Secondary Market Review, January 2025.* https://www.jefferies.com/wp-content/uploads/sites/4/2025/02/Jefferies-Global-Secondary-Market-Review-January-2025.pdf
4. Jefferies (Jul-2025). *Global Secondary Market Review, July 2025.* https://www.jefferies.com/wp-content/uploads/sites/4/2025/08/Jefferies-Global-Secondary-Market-Review-July-2025.pdf
5. Evercore PCA (Jul-2026). *H1 2026 Secondary Market Review.* https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
6. Evercore PCA (Feb-2026). *2025 Secondary Market Report.* https://www.evercore.com/wp-content/uploads/2026/02/Evercore-PCA-2025-Secondary-Market-Report.pdf
7. Lazard PCA (Aug-2026). *Interim Secondary Market Report 2026.* https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf
8. Campbell Lutyens (2026). *2025 Secondary Market Flash Report.* https://campbell-lutyens.com/media/qwydmsgy/2025-secondary-market-flash-report_campbell-lutyens.pdf
9. Proskauer (2026). *Insights on the NAV Financing Market, Full Year 2025* (via stream 05 verification). https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025
10. Callan, A. Davison (20-Mar-2025). *Secondary Investments: Key Issues for Institutional Investors.* https://www.callan.com/?p=29041

**Academic**

11. Nadauld, T. D., Sensoy, B. A., Vorkink, K., & Weisbach, M. S. (2019). The liquidity cost of private equity investments: Evidence from secondary market transactions. *Journal of Financial Economics* 132(3), 158-181 (DOI 10.1016/j.jfineco.2018.11.007). NBER WP 22404 (2016), the source of all figures quoted in this dossier (the *JFE* abstract gives seller PME 0.976, the WP 0.974): https://www.nber.org/papers/w22404
12. Boyer, B. H., Nadauld, T. D., Vorkink, K. P., & Weisbach, M. S. (2023). Discount-Rate Risk in Private Equity: Evidence from Secondary Market Transactions. *Journal of Finance* 78(2), 835-885. https://doi.org/10.1111/jofi.13202. Earlier versions: NBER WP 28691 (Apr-2021, same title; source of the β, return and volatility figures quoted here), https://www.nber.org/papers/w28691 ; NBER WP 25207 (Nov-2018), *Private Equity Indices Based on Secondary Market Transactions* (source of the superseded β > 2 / < 0.5 figures), https://www.nber.org/papers/w25207
13. Albuquerque, R., Cassel, J., Phalippou, L., & Schroth, E. (2018, WP). *Liquidity Provision in the Secondary Market for Private Equity Fund Stakes.* SSRN working paper; no journal version found. https://doi.org/10.2139/ssrn.3182481 (read at abstract level).
14. Maurin, V., Robinson, D. T., & Strömberg, P. (2023). A Theory of Liquidity in Private Equity. *Management Science* 69(10), 5740-5771. https://doi.org/10.1287/mnsc.2022.4612
15. Bollen, N. P. B., & Sensoy, B. A. (2022). How much for a haircut? Illiquidity, secondary markets, and the value of private equity. *Financial Management* 51(2), 501-538. https://doi.org/10.1111/fima.12375 ; https://ideas.repec.org/a/bla/finmgt/v51y2022i2p501-538.html
16. Lerner, J., & Schoar, A. (2004). The illiquidity puzzle: theory and evidence from private equity. *Journal of Financial Economics* 72(1), 3-40. https://ideas.repec.org/a/eee/jfinec/v72y2004i1p3-40.html
17. Allen, F., & Gale, D. (1994). Limited Market Participation and Volatility of Asset Prices. *American Economic Review* 84(4), 933-955. https://ideas.repec.org/a/aea/aecrev/v84y1994i4p933-55.html
18. Shleifer, A., & Vishny, R. (2011). Fire Sales in Finance and Macroeconomics. *Journal of Economic Perspectives* 25(1), 29-48. https://www.aeaweb.org/articles?id=10.1257/jep.25.1.29
19. Bolton, P., Chen, H., & Wang, N. (2013). Market Timing, Investment, and Risk Management. *Journal of Financial Economics* 109(1), 40-62. NBER WP 16808: https://www.nber.org/papers/w16808
20. Harris, R. S., Jenkinson, T., Kaplan, S. N., & Stucke, R. (2018). Financial intermediation in private equity: How well do funds of funds perform? *Journal of Financial Economics* 129(2), 287-305. https://ideas.repec.org/a/eee/jfinec/v129y2018i2p287-305.html
21. Gottschalg, O. (2024). *Continuation Funds: Performance and Determinants, 2018-2022 Vintages.* HEC Paris RP 1515 (not peer-reviewed). https://doi.org/10.2139/ssrn.4752652 ; https://ideas.repec.org/p/ebg/heccah/1515.html
22. Gottschalg, O. (2025). *"Continuation Funds" Performance and determinants 2018-2023 vintages.* HEC Paris RP 1584 (not peer-reviewed). https://ebslgwp.hhs.se/heccah/abs/heccah1584.htm
23. Takahashi, D., & Alexander, S. (2002). Illiquid Alternative Asset Fund Modeling. *Journal of Portfolio Management* 28(2), 90-100. https://doi.org/10.3905/jpm.2002.319836
24. Brown, G. W., Ghysels, E., & Gredil, O. (2023). Nowcasting Net Asset Values: The Case of Private Equity. *Review of Financial Studies* 36(3), 945-986. https://doi.org/10.1093/rfs/hhac045
25. Gourier, E., Phalippou, L., & Westerfield, M. M. (2024). Capital Commitment. *Journal of Finance* 79(5), 3407-3457. https://doi.org/10.1111/jofi.13382
26. Luxenberg, E., Boyd, S., van Beek, M., Cao, W., & Kochenderfer, M. J. (2022). Strategic Asset Allocation with Illiquid Alternatives. *Proceedings of the Third ACM International Conference on AI in Finance (ICAIF '22)*, 249-256. https://doi.org/10.1145/3533271.3561769. Preprint: arXiv:2207.07767, https://arxiv.org/abs/2207.07767

**Guidance, regulation and practice**

27. IPEV (11-Dec-2025). *International Private Equity and Venture Capital Valuation Guidelines*, §4. https://www.privateequityvaluation.com/Portals/0/Documents/Guidelines/2025%20IPEV%20Valuation%20Guidelines.pdf
28. ILPA (May-2023). *Continuation Funds: Considerations for Limited Partners and General Partners.* https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf ; 2026 draft status: https://ilpa.org/industry-guidance/principles-best-practices/continuation-funds/
29. ILPA (Jun-2017). *Subscription Lines of Credit and Alignment of Interests.* https://ilpa.org/wp-content/uploads/2017/06/ILPA-Subscription-Lines-of-Credit-and-Alignment-of-Interests-June-2017.pdf
30. Deane, S., & Robinson, K. (Sep-2025). *Continuation Funds: Ethics in Private Markets, Part I.* CFA Institute. https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/rpc_deane_continuationfunds-ethicsinprivatemarkets_pti_online.pdf
31. 17 CFR § 270.17a-7 (cross trades among affiliated funds). https://www.law.cornell.edu/cfr/text/17/270.17a-7
32. BCBS (Apr-2009). *Supervisory guidance for assessing banks' financial instrument fair value practices.* https://www.bis.org/publ/bcbs153.htm

**Press and secondary sources**

33. McKenna, G. (15-Jun-2025). "NAV squeezing" and the Harvard and Yale sales. *Fortune.* https://www.fortune.com/2025/06/15/harvard-yale-private-equity-holdings-sale-net-asset-value-discounts-nav-squeezing
34. Unquote (26-Jan-2009). *Secondaries pricing dips to a five-year low* (Cogent data; via stream 05 verification). https://www.unquote.com/uk/news/85756/secondaries-pricing-dips-to-a-five-year-low
35. Beaudoin, T. A., Berrent, J. C., Evans, S. C., & Rothermel, S. (2009). Trends in the Private Equity Secondary Market. *ABA Business Law Today* 18(4) (WilmerHale reprint). https://www.wilmerhale.com/-/media/files/wilmerhale_shared_content/files/editorial/publication/blt_ma09_secondarymarket.pdf
36. Wikipedia (accessed 2026-10-18). *Private equity secondary market* (2009 and 2013 discounts citing WSJ). https://en.wikipedia.org/wiki/Private_equity_secondary_market
37. HarbourVest (via search summary). Summary of HEC (Mar-2024) and Morgan Stanley (Aug-2024) CV studies [C]. https://harbourvest.com/?p=10347
38. Secondaries Investor (21-Apr-2025; 4-Nov-2025). Morgan Stanley and Evercore/HEC CV articles (paywalled; ledes only) [C]. https://www.secondariesinvestor.com/continuation-fund-performance-begins-to-solidify-morgan-stanley/ ; https://www.pei-secondariesinvestor.com/top-quartile-cvs-continue-to-prove-their-outperformance-over-buyout-funds-evercore/
39. Rode, N., Poldauf, P., & Fuentes Perez, E. (Aug-2025). *Redefining Private Equity: How Continuation Investments Are Disrupting the Buyout Market.* Schroders Capital. Practitioner note, cited through the CFA Institute report (ref 30, p. 21; reference list p. 45, dated 18 August); the web summary is dated 19-Aug-2025, and the 15-page report it cites at p. 5 was not read [C]. https://www.schroders.com/en-us/us/institutional/insights/redefining-private-equity-how-continuation-investments-are-disrupting-the-buyout-market/

**Internal project documents.** `inputs/00_CONTEXT_AND_PRIOR_WORK.md`; dossiers 04, 05 (with its verification log), 06, 07 and 08 in `research/dossiers/` and `research/verification/`.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 and `research/literature/G2_secondaries_group.lit.md` §1-2. Metadata was confirmed via Crossref and OpenAlex. Boyer et al. was re-checked against the *JF* abstract and NBER WP 28691, and "Rode et al." was traced through the CFA Institute report's reference list.

1. §1 item 4, §4.5 and ref 11 (Nadauld et al.): the figures are labelled as NBER WP 22404 (2016) figures, and the *JFE* abstract's seller PME of 0.976 is shown beside the WP's 0.974.
2. §1 item 4, §2.4, §4.5, §6.8 item 7 and §6.10 (Boyer et al., synthesis §2.4 item 6): transaction-index β "above 2" and NAV-index β "below 0.5" are replaced by the 2021 values: β 1.79 (1.94 with log returns), "quite low" NAV betas, volatility ~34% vs 14-20%, and an average of 14% a year rather than ~20%. The *JF* abstract confirms a CAPM alpha of about zero; the *JF* full text was not accessed. No conclusion changes: NAV marks still understate exit-value risk.
3. Ref 12 now cites *Journal of Finance* 78(2):835-885 (2023), DOI 10.1111/jofi.13202 (Crossref), with NBER WP 28691 (2021) and WP 25207 (2018) as earlier versions.
4. §2.3 (Albuquerque et al., synthesis §2.4 item 16): the abstract-level result is tagged [S]; the 2009-2016, young-fund, VIX, funding-cost and non-specialist details are tagged [C] as not in the abstract.
5. Ref 13: the dead Tuck forum link is replaced by SSRN DOI 10.2139/ssrn.3182481 (Crossref).
6. §2.3 (Maurin, Robinson & Strömberg): its claims are labelled as theoretical model predictions.
7. §2.3 and ref 15 (Bollen & Sensoy, orphan, synthesis §2.5): now cited for the abstract's breakeven-return result, with the full title and DOI 10.1111/fima.12375 added (Crossref).
8. §6.5 item 5 (Gourier, Phalippou & Westerfield, orphan, synthesis §2.5): now cited for the commitment-risk result (OpenAlex abstract; literature file A13).
9. §2.6, §3.1(c) and new ref 39 ("Rode et al.", not found, synthesis §2.2 item 11): the full citation is taken from the CFA Institute report's reference list (Rode, Poldauf & Fuentes Perez 2025, Schroders Capital). The 60bp / 75bp split is re-attributed to the CFA report's own example, tagged [C] and marked [unverified] at source.
10. Ref 21: SSRN DOI 10.2139/ssrn.4752652 added (Crossref). Refs 21-22 and §4.5 are marked as non-peer-reviewed evidence based on interim marks.
11. Ref 26 (Luxenberg et al.): the peer-reviewed ICAIF '22 version is added (pp. 249-256, DOI 10.1145/3533271.3561769; Crossref and OpenAlex), and the arXiv preprint is kept.
12. Checked, no change needed: none of the BGK barrier re-run values, the re-checked works of topics 10, 11, 13, 14 and G3, or the five §2.6 cross-file items appear in this dossier.
