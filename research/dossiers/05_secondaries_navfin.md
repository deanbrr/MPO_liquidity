# Stream 05: Liquidity tools for private holdings and the economics of SELL and REFINANCE

**Scope.** This stream covers LP-led secondaries, deferred-payment sales, GP-led continuation vehicles (CVs), NAV financing at LP and fund level, preferred equity, collateralized fund obligations (CFOs) and rated note feeders, the Temasek Astrea template, and subscription lines. It ends with an action-economics library, implied cost-of-liquidity formulas and a marginal-cost-of-liquidity (MCL) curve for the ADIC multi-period framework.

**As of:** 2026-10-18. **Evidence tags:** **[S]** sourced fact (citation given); **[C]** practitioner consensus or a secondary summary that I could not check against the primary document; **[I]** my own inference or design default, which must be calibrated before use.

**Research caveats.** The shared web-search budget ran out several times during this work. Where a primary PDF could not be parsed by the fetch tool, I decompressed it locally and read the text layer: Evercore H1-2026, Evercore FY-2025, Lazard Interim-2026, Jefferies Jan-2025 and Jul-2025, Proskauer, ILPA, Nadauld et al., Bollen-Sensoy and WilmerHale. The Jefferies July-2026 PDF is image-only, so its H1-2026 strategy splits come from secondary summaries and are tagged [C]. The following are flagged as unverified wherever they appear:

- whether the Yale and Harvard 2025 sales completed, and on what terms;
- Harvard's 2008 bond issuance and swap losses;
- current NAIC treatment of CFOs;
- the 2023 SEC adviser-led-secondary rule and its vacatur;
- preferred-equity market pricing.

---

## 1. Executive summary

1. **The market is deep enough for a programmatic ADIC seller, but not instantly and not at any price.**
   - Volume: 2025 secondary volume was US$225-240bn depending on the advisor, of which LP-led was about US$117-125bn [S: Jefferies; Evercore; Lazard; Campbell Lutyens]. H1-2026 set a first-half record at US$118-124bn [S: Evercore; Lazard; C: Jefferies].
   - LP-portfolio pricing: about 87% of NAV across strategies in 2025 and H1-2026. Buyout is about 90-92%, tail-end about 70% (stable since 2022), venture/growth about 78-79% and real estate about 68-71% [S/C].
   - Cushion is thinner. Evercore's capital-overhang multiple fell from about 1.2x (2025) to about 1.0x (H1-2026). Jefferies' dedicated-capital measure was 1.5x at H1-2025, against a five-year average of about 2.2x [S]. The two definitions differ, so compare trends, not levels.
   - Sovereign sellers are the fastest-growing seller group. SWFs went from 2% of LP-led volume in 2024 to 12% in 2025 and 21% in H1-2026 [S: Evercore].
2. **The cost of liquidity is a ladder, and its rungs move with the regime.** Approximate H2-2026 conditions, cheapest first:
   - committed balance-sheet borrowing (an assumption; another stream covers it);
   - CFO senior notes: average SOFR+295 bp on 2025 CFOs; Astrea 9 note weighted coupon about 4.5% in mixed SGD/USD [S];
   - LP-level NAV and secondaries-style facilities: SOFR+300-500 bp plus 1-2% OID, about 7-9% all-in at an assumed SOFR of 3.75% [S/I];
   - LP-led sales of quality buyout: buyers target mid-to-high-teens gross; the implied cost against ADIC's own forecasts is typically 8-15% [S/I];
   - preferred equity: 12-20%, path-dependent [I];
   - tail-end, venture and real-estate sales: implied cost about 15-25% [I];
   - forced sales in a crisis: H2-2008 average high bids were 61% of NAV, and some unfunded-heavy interests could not be given away [S].

   In 2023 the NAV-loan rung sat at SOFR+533-982 bp depending on LTV [S: Proskauer]. The ordering is therefore state-dependent and has to be modeled, not hard-coded.
3. **Three conceptual corrections for the IC and the optimizer.**
   - (a) The discount to stale NAV is not the economic cost. In H2-2008 Cogent's average high bid was 61% of NAV, but 83.5% after adjusting for public-market moves since the reference date [S]. Most of the headline discount was NAV staleness.
   - (b) Transferring unfunded commitments is a liquidity asset. The relevant quantity is liquidity released under stress (price plus avoided stressed calls), not price alone [S: Nadauld et al.; I].
   - (c) Financing keeps the risk and adds a covenant-triggered fire-sale option, much like a margin call. Sales and financings must be compared on a common valuation kernel, not on IRRs alone [I].
4. **Design deliverable.** Each instrument is reduced to a common cash-flow signature: proceeds, give-ups, financing flows, retained exposure, unfunded transfer, lag, capacity, regime-conditional price and availability, signaling cost, and irreversibility. From these the framework computes the instrument's IRR of liquidity raised and its value cost per dollar. It then builds an MCL curve whose clearing price equals the optimizer's shadow price of liquidity λ. That λ gives Gap 8 in the context file (no shadow prices) an explicit, auditable number.
5. **Policy recommendations [I].**
   - Pre-build liquidity capacity in benign regimes: CFO and NAV-facility documentation, pre-cleared GP consents, and a standing programme of tail and non-core sales.
   - Set encumbrance caps and covenant chance constraints inside Tier 1.
   - Sell from strength, in mosaic or strip formats, slicing large programmes across semesters.
   - Keep a reserve price at least as high as MCL(λ), as GIC did when it was ready to withdraw a 2025 process if bids fell short [C].
   - Never be a forced seller. Harvard in 2008-09 is the canonical counter-example [S/C].

---

## 2. Core concepts and theory

### 2.1 What "cost of liquidity" means

Let instrument $k$ deliver state-contingent cash to ADIC $L^k_t$ (liquidity raised) in exchange for a give-up stream $G^k_t$: forgone distributions net of avoided calls, interest and principal, preferred distributions, or note coupons. Three measures are useful and are not interchangeable:

- **IRR of liquidity raised.** This is the metric the IC finds intuitive. Under belief $b$:
$$\sum_{t\ge 0}\frac{\mathbb E^b[L^k_t-G^k_t]}{(1+y_k^b)^t}=0.$$
- **Value cost per dollar.** This is the theoretically consistent measure. Using one pricing kernel $m$ for all instruments (ADIC's scenario deflators or a risk-adjusted hurdle by asset):
$$c_k=\frac{PV_m(G^k)-PV_m(L^k)}{PV_m(L^k)}.$$
  A sale transfers risk, so its give-up stream is risky. A loan's give-up stream is near-riskless, apart from the embedded covenant put. The IRR measure cannot tell these apart; $c_k$ under a common kernel can.
- **Shadow-price test.** This is the measure the optimizer uses. With $\lambda_{t,s}$ the dual price of the liquidity constraint at date $t$ in state $s$, execute $k$ at scale $q$ iff
$$\sum_{t,s}\lambda_{t,s}\,L^k_{t,s}(q)\;\ge\;PV_m\!\big(G^k(q)\big)+\text{Signal}_k(q)+\text{Irrev}_k(q).$$
  Liquidity that arrives after the crunch is worth little, so time and state weighting is essential [I].

### 2.2 Decomposing the observed secondary discount

Write the transaction price relative to reference-date NAV as
$$\pi=\underbrace{\frac{V^{mkt}_t}{NAV^{ref}}}_{\text{staleness}}\times\big(1-d^{liq}-d^{qual}-d^{unf}-d^{fee}\big).$$

- **Staleness.** NAVs lag public markets by one or two quarters. In the GFC the staleness factor was about 0.73 (61/83.5) [S: Unquote/Cogent; I]. Buyers price off the reference date and adjust dollar-for-dollar for subsequent calls and distributions [S: WilmerHale 2009].
- **Liquidity and market depth ("cash-in-the-market").** Nadauld, Sensoy, Vorkink and Weisbach use intermediary data for 2006-2014. Discounts and the buyer-seller return gap are larger when the economy is weak and less buyer capital is available, and larger for smaller funds and smaller deals [S]. Bollen and Sensoy model a risk-averse LP hit by liquidity shocks that force sales at a state-dependent haircut. In their 2015 working paper, when secondary markets are relatively inefficient, so haircuts are large, annual required returns on PE assets are as much as 5-10 pp higher than when haircuts are small, especially for more risk-averse LPs [S: Bollen-Sensoy 2015 WP, p.2]. The published version (*Financial Management* 2022) reports a different headline: model-implied breakeven returns match observed average fund returns for moderately risk-tolerant LPs with PE allocations up to 40%, while highly risk-averse LPs allocate only a few percent to PE [S: published abstract]. Whether the published paper keeps the 5-10 pp magnitude is unverified (full text paywalled) [corrected 2026-10-18: the 5-10 pp figure was presented as a published result; it is from the 2015 WP]. Albuquerque, Cassel, Phalippou and Schroth (2018, SSRN working paper) study liquidity provision by secondary buyers using a broker's bid data. Per their abstract, the demand response to aggregate liquidity shocks is negatively related to contemporaneous bids, more strongly for funds likely to be offered in low-liquidity periods, and unrelated to future NAV-to-NAV returns and future bidding, so discount variation tracks variation in liquidity provision [S: SSRN abstract as summarized by the 2026-10-18 literature check; full text not read]. Maurin, Robinson and Strömberg's "A Theory of Liquidity in Private Equity" (*Management Science* 69(10), 2023) formalizes equilibrium secondary pricing; the authorship is confirmed by Crossref.
- **Quality and adverse selection.** Funds that performed better trade higher: a one-standard-deviation higher PME, about 50 bp, goes with roughly 2.5% higher price relative to NAV [S: Nadauld et al.]. Sellers often add their best funds as sweeteners [S: Jefferies Jul-2025; Moonfare/HSBC].
- **Unfunded burden.** The discount applies only to the drawn portion. An LP selling a 5%-drawn fund at a 50% discount pays only 2.5% of commitment to shed the remaining call liability [S: Nadauld et al.]. In 2008 some interests could not be given away because no buyer would assume the unfunded commitment, so their effective price was below zero [S: WilmerHale 2009].
- **Fee drag.** Management fees on commitments reduce NAV over time. Cogent estimated about 50 bp of NAV under its assumptions [S: Unquote].
- **Tail-end age.** Interests of ten years or older traded at about a 10% discount even after controlling for time fixed effects, so the tail discount is structural [S: Nadauld et al.].

### 2.3 Selling is exercising an abandonment option

Selling kills the option to wait. If discounts mean-revert, waiting has value. The "Liberation Day" tariff shock of April 2025 cut average LP pricing by 300-500 bp, and pricing recovered within the quarter [S: Jefferies Jul-2025]. With irreversibility (Dixit and Pindyck 1994), a sale should clear the hurdle $\pi>V_{hold}+\text{OV}_{wait}$, not just $\pi>V_{hold}$ [I]. Bollen and Sensoy solve a related backward-recursion problem on a 3-D lattice of public and private values with forced-sale nodes, which is a direct template for this valuation [S].

### 2.4 Financing as a short put on NAV

A NAV facility has a borrowing base tied to NAV. If LTV exceeds the covenant, the borrower must repay or the facility sweeps cash. Facilities can cross-collateralize portfolio companies, and lenders can foreclose on holdco equity or force a monetization plan [S: ILPA Part I]. Economically, the borrower has written a path-dependent put. The trigger is $LTV_t=B_t/NAV_t>\ell^{trig}$, and the payoff is forced deleveraging at the worst prices. This is the private-markets version of a margin call, and it is the bank-treasury reason to treat committed NAV revolvers as contingent rather than certain liquidity [I].

### 2.5 Agency and governance

- **GP-led CVs.** The GP sits on both sides. ILPA's 2023 guidance asks for:
  - at least 30 calendar days or 20 business days for elections, with non-responses defaulting to sell;
  - 10 business days of LPAC review;
  - a status-quo option: no increase in fee rate or base, no carry or hurdle changes, and no carry crystallization for rolling LPs;
  - 100% roll of GP carry in almost all cases;
  - fairness opinions or partial third-party sales as price checks [S].

  ILPA published draft updated CV guidance on 2026-06-24, with comments closing 2026-08-05 [S]. A secondary source says the draft lengthens elections to 30 business days and adds an option to remain in the existing fund [C].
- **Fund-level NAV loans used for distributions** create "synthetic DPI." ILPA states that NAV facilities are fund-level leverage and should count toward LPA borrowing limits. It recommends LPAC consent for any distribution-purpose use, and it warns that such distributions are often recallable and carry interest cost [S: ILPA Parts I-II]. Per the Fund Finance Association, about 80% of NAV facilities have supported portfolio companies and 20% have funded distributions [S: ILPA Part I].

---

## 3. Methods and models, with trade-offs

### 3.1 The action-economics library: one signature per instrument

| Instrument | Immediate proceeds | Future CFs given up | Financing cost | Retained up/downside | Unfunded transfer | Execution time [C] | Regime sensitivity | Signaling/relationship | Irreversibility |
|---|---|---|---|---|---|---|---|---|---|
| LP-led sale (cash) | $\pi\cdot NAV^{ref}$ ± post-reference CFs | All future $D_t-C_t$ | none | none | yes, buyer assumes | 3-6 months to sign plus 1-3+ months transfer (GP consent, ROFR) [S: WilmerHale] | high: price, depth, failure risk | medium; mitigated by mosaic or strip sales | full |
| Deferred-payment sale | $\phi\pi_d NAV$ now, rest within ≤12 months typical [S] | as above | implicit vendor loan to buyer | none; buyer credit risk | yes | as above | medium | as above | full |
| CV election (sell) | $\pi_{CV}NAV$, near par for SACVs | upside on GP's "best" asset | none | none | n/a | set by GP; 20 business days to decide [S] | low-medium | low | full |
| CV election (roll) | 0 | none | fee and carry reset unless status quo | full | n/a | as above | n/a | positive | reversible later |
| LP-level NAV facility | $\ell\cdot NAV_{pool}(1-\text{OID})$ | none, but sweeps | SOFR+s(ℓ) | full and levered | no | 6-12 weeks [C] | spreads and LTV capacity cyclical | low-medium (GP consent to pledges) | low; covenant risk |
| Preferred equity (LP portfolio) | $a\cdot NAV_{pool}$ | priority share of distributions until accrual or MOIC floor met | accrual 12% plus MOIC floor (illustrative) [I] | common equity upside | no | 2-4 months [C] | medium | low-medium | medium |
| CFO / securitization | Σ notes − costs | none; coupons and principal | coupons ~SOFR+250-300 bp [S] plus costs | levered equity, cash-trap risk | no; SPV funds calls via reserves or liquidity facility | 6-12 months [C] | rating and insurer demand cyclical | low | medium (long notes, scheduled calls) |
| Fund-level NAV loan (GP's decision) | recallable early distributions | reduced future distributions | SOFR+~400-500 bp borne pro rata [S] | full and levered | n/a | GP-driven | high | n/a | recall risk |
| Pacing cut | avoided future calls | vintage diversification | none | n/a | n/a | immediate decision, slow cash effect | none | high (re-ups) | partial |
| Strip or tender sale | slice of many interests | pro-rata future CFs | none | partial | pro rata | GP-led tenders follow GP timetable | medium | lowest | partial |

### 3.2 Formulas for each instrument

**(1) LP-led sale.**
- Price (hedonic, Section 6):
$$P_0=\pi(s_t,\text{age},\text{strat},\text{qual},U/NAV,q)\cdot NAV^{ref}+\textstyle\sum_{\tau\in(ref,0]}(C_\tau-D_\tau).$$
- Implied cost: $y_{sell}^b=\mathrm{IRR}\{P_0,-(D^b_1-C^b_1),\dots,-(D^b_T-C^b_T)\}$.
- Liquidity released over horizon $H$ in stress state $s^\*$: $LR_H=P_0+\sum_{t\le H}\big(C^{s^\*}_t-D^{s^\*}_t\big)$.
- Market-implied cost from buyer targets: $y_{mkt}\approx M^{1/\bar d}-1$. Evercore targets $M$ of about 1.7x for diversified LP portfolios, 1.8x for single LP positions, 1.9x for MACVs and 2.3x for SACVs, on about a four-year horizon [S]. These imply roughly 14%, 16%, 17% and 23% gross IRRs [I].
- **Belief gap:** $\Delta y=y_{sell}^{SG}-y_{mkt}$. A large positive gap means either the strategy group's forecast is too optimistic (the memo-corpus blind spot in the prior deck) or ADIC holds private information.

*Worked example [I].* An interest has NAV 100 and forgone net cash flows of 22, 28, 30, 25, 15 (1.20x remaining). Selling at 91 gives $y_{sell}=10.5\%$. If the forecast is scaled by 0.9x, 1.0x or 1.1x, $y$ is 6.3%, 10.5% or 14.5%. At a price of 87, $y=12.3\%$; at 70, $y=22.1\%$. A tail interest with stale NAV 100 and forgone flows of 0.90x sold at 70 gives $y=12.1\%$. The implied cost is therefore more sensitive to belief dispersion than to the headline discount.

**(2) Deferred consideration.**
- Implied vendor-finance rate, solving the cash-equivalent identity:
$$\pi_{cash}=\phi\,\pi_d+\frac{(1-\phi)\,\pi_d}{(1+r_v)^{t_d}}.$$
- Deferral raised LP prices by about 400 bp on average in 2024 [S: Jefferies]. With $\pi_{cash}=87$, $\pi_d=91$ and $t_d=1$, a 50% deferred share implies $r_v=9.6\%$, 33% implies 15.4% and 25% implies 21.3% [I].
- Evercore describes deferral as "a form of leverage" for buyers, typically settled within 12 months [S]. ADIC is making an unsecured loan to the buyer, and only $\phi P$ is liquidity today. The IC should always see the cash-equivalent price.

**(3) CV election.**
- Sell iff $\lambda\,P_{CV}\ge PV_m(\text{asset CFs net of new fees and carry})$.
- Roll terms are a vector $(f',c',h')$. Under ILPA's status-quo option $(f',c',h')=(f,c,h)$ [S].
- Market evidence on elections: average LP rollover was about 17% in H1-2025 (Jefferies) [S], about 14% in a later Jefferies figure [C], and Lazard reports LPs "continue to favor selling over rolling" [S]. Sellers face informed counterparties [I]. Evercore, summarizing the fourth HEC Paris continuation-vehicle performance study by Prof. Oliver Gottschalg's team, reports SACVs performing largely in line with buyout funds so far ("still early days"), with top performers showing outperformance potential associated with "a positive selection bias of best-performing assets that GPs wish to 'buy again' for another investment cycle" [S: Evercore FY-2025 (ref 6), p.13].

**(4) LP-level NAV facility.**
- Proceeds: $L_0=\ell_0 NAV_{pool}(1-\text{OID}-\text{fees})$.
- LTV recursion:
$$\ell_{t+1}=\frac{B_t(1+r_t\Delta)-\sigma(\ell_t)\,D^{pool}_t+\text{PIK}_t}{NAV^{pool}_{t+1}},\qquad r_t=\text{SOFR}_t+s(\ell_t,s_t).$$
- Covenants: cash sweep $\sigma(\ell)$, trigger $\ell^{trig}$ (sweep goes to 100%, cure required) and default $\ell^{def}$ (forced monetization).
- Cost: $y_{NAV}\approx\text{SOFR}+s+\text{OID}/\text{WAL}+\mathbb E[\text{fire-sale loss}]/B_0$, where the last term is computed by Monte Carlo on de-smoothed NAV paths.
- *Worked example [I]:* with SOFR at 3.75%, 450 bp spread and 1.25% OID, a three-year all-in cost is about 8.7% (9.0% with sweep amortization). With 300 bp and 1.0% OID it is about 7.1-7.4%. On 2023 terms (SOFR 5.30%, +681 bp, 2% OID) it is about 13.0-13.4%.

**(5) Fund-level NAV loan, from ADIC's side as an LP.** Model the early distribution $D^{NAV}_0$ as borrowed DPI. Future distributions become $D_t^{post}=D_t-\text{debt service}_t$, with recall probability $p^{recall}(s)$ in stress. Compute "synthetic DPI" excluding NAV-financed distributions, as ILPA effectively requires [S]. Treat the outcome of LPAC consent votes as a decision input.

**(6) Preferred equity.**
- Advance $A_0=a\cdot NAV_{pool}$. Clifford Chance (2020) cites cash funding up to about 50% LTV [S].
- Investor cash flow: $X_t=\min\{\sigma_p D_t,\;\max(\text{Acc}_t,\,m_{min}A_0-\text{Paid}_t)\}$ plus any upside share θ after redemption, with $\text{Acc}_t=\text{Acc}_{t-1}(1+r_p)-X_{t-1}$.
- Cost: $y_{pref}=\mathrm{IRR}\{A_0,-X_t\}$.
- *Worked example [I]:* $a=30\%$, $r_p=12\%$, $m_{min}=1.30$x. If distributions are fast and repay the preferred in two years, $y=18.7\text{-}20.4\%$ with an 80-100% sweep. With a 50% sweep, $y=13.8\%$. With slow distributions, $y\approx12.0\%$. The MOIC floor makes preferred equity expensive exactly when the portfolio does well, and cheap (the accrual rate, with no LTV default) when it does badly. Its convexity is the opposite of a NAV loan's.
- Davis Polk describes the instrument as SPV equity senior to the sponsor's common equity, with a liquidation preference and enforcement through controlled accounts and contractual monetization rights, not asset foreclosure [S].

**(7) CFO.**
- Proceeds: $L_0=\sum_jN_j-\text{upfront costs}-\text{reserve funding}$.
- Give-ups: $G_t=\sum_j(\text{coupon}_{j,t}+\text{principal}_{j,t})+\text{liquidity-facility fee}+\text{running costs}$.
- Retained equity is $NAV_{pool}-\sum_jN_j$. LTV or liquidity tests divert cash away from equity, and senior interest can be deferred [S: Morgan Lewis].
- Astrea 9 note weighted average coupon is about 4.5% (S$615m at 3.40%, US$200m at 5.70%, US$107m PIK at 7.35%), ignoring FX [S/I]. The SGD tranche needs a cross-currency adjustment for a USD sponsor [I].

**(8) Subscription lines (timing only).** ILPA recommends:
- a cap of 15-25% of uncalled capital and at most 180 days outstanding;
- hurdles computed from the draw date;
- reporting of net IRR with and without the line [S].

For ADIC, model LP call timing as the fund's call shifted by $\tau^{sub}\in[0,180\text{d}]$. In stress, add a catch-up probability: lines are cleared or not renewed, so calls bunch. Measure performance on unlevered IRR or PME.

### 3.3 Pricing models

- **Hedonic or ML bid model.** Fit $\log\pi=f(\text{regime},\text{age},\text{strategy},\text{GP tier},\text{TVPI/PME},U/NAV,\text{size},\text{geography},\text{software share},\text{months since ref})+\varepsilon$ with monotonic constraints: price rises with PME and falls with age beyond about 6 years. Use hierarchical shrinkage (GP inside strategy inside market). Quantile outputs feed the MCL curve.
- **Consensus secondary-price index (state-space).** Each advisor publishes a noisy, methodologically biased measurement of a latent index. Jefferies reports simple averages of % of NAV. Campbell Lutyens reports value-weighted discounts including unfunded: 13.9% in 2025 and 13.3% in 2024 [S]. Evercore reports reference-date NAV and qualitative bands. A Kalman filter or smoother with advisor-specific bias and noise, plus a regime-switching drift, produces a dated index with uncertainty bands. This is a measurement-error idea from survey statistics [I].
- **Regime map.** Link the index to the prior deck's HMM states. The anchors [S] are: benign (2021: all strategies 92%, buyout 97%); moderate stress (2022: 81% and 87%); acute-but-transient shock (April 2025: −300 to −500 bp); crisis (H2-2008: average high bid 61%).

### 3.4 Building the marginal-cost-of-liquidity curve and the pecking order

1. Enumerate instrument tranches $j=(k,\text{pool},\Delta q)$. Each has a cost $c_j(s)$ (value cost per dollar, or IRR spread over the hurdle), capacity $\Delta q_j(s)$, lag $\tau_j$ and execution probability $p_j(s)$. Lazard's survey reports about 27% of transactions failed or paused in 1H-2026 [S].
2. Effective liquidity by horizon $H$: $q^{eff}_{j,H}=p_j(s)\,\Delta q_j\,\mathbf 1\{\tau_j\le H\}$.
3. Price impact for sales: $\pi(q)=\pi_0(s)-\kappa_s\,q/\text{Depth}_s$, where $\text{Depth}_s$ is LTM LP-led volume in the strategy. By default ADIC should absorb at most θ=5% of it per year [I].
4. Mutual exclusivity and encumbrance: an asset sold cannot be pledged; NAV-facility capacity depends on the pool left after sales; a CFO needs a seasoned pool of at least about US$1bn [C/I].
5. Solve $\min\sum_j c_j x_j$ s.t. $\sum_j q^{eff}_{j,H}x_j\ge L^\*_H$, encumbrance and exclusivity constraints, $x_j\in[0,1]$ (binary for lumpy CFOs). The dual of the coverage constraint is $\lambda_H$, the marginal cost of the last dollar.
6. Plot $\text{MCL}_H(Q)$ for H = 30 days, 6 months, 12 months and 24 months under each regime. Show the IC where today's need $L^\*_H$ intersects the curve and how far that point moves in a crisis.

**Trade-offs.** IRR is intuitive but ignores risk transfer and has multiple-root problems. Common-kernel value cost is consistent but kernel-dependent. MILP gives clean duals but discretizes concave price impact. Stochastic programming captures timing but is costly; Section 7 covers the hybrid.

---

## 4. Empirical evidence and current market data

### 4.1 Volumes (US$bn)

| Year | Jefferies total (LP / GP) | Evercore total (LP / GP) | Lazard total (LP / GP) |
|---|---|---|---|
| 2018 | 74 (50/24) | 72 (49/23) | 75 (51/24) |
| 2019 | 88 (62/26) | 79 (53/26) | 83 (55/28) |
| 2020 | 60 (25/35) | 60 (28/32) | 60 (30/30) |
| 2021 | 132 (64/68) | 134 (66/68) | 126 (63/63) |
| 2022 | 108 (56/52) | 103 (55/48) | 102 (58/44) |
| 2023 | 112 (60/52) | 114 (63/51) | 109 (61/48) |
| 2024 | 162 (87/75) | 160 (89/71) | 152 (80/72) |
| 2025 | 240 (125/115) | 226 (120/106) | 233 (117/116) |
| H1-2026 | 118 (56/62) [C] | 121 (56/65) | 124 (~63/~61) |

Sources [S]: Jefferies Jan-2025, Feb-2026 and Jul-2026 (H1-2026 via summaries [C]); Evercore Feb-2026 and Jul-2026; Lazard Aug-2026. Campbell Lutyens reports 2025 at US$225bn with LP-led at 54% [S]. FY-2026 forecasts are Evercore US$250-260bn, Jefferies about US$250-260bn [C], and Lazard US$275bn [S]. Evercore notes about 55% of annual volume historically closes in H2 [S]. Note the 2020 contraction and the 2022 dip: volume is cyclical, and LP-led volume fell about 60% in 2020 on Jefferies' series [S].

### 4.2 LP-portfolio pricing (% of NAV, Jefferies average by strategy)

| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | H1-25 | 2025 | H1-26 |
|---|---|---|---|---|---|---|---|---|---|
| All | 88 | 86 | 92 | 81 | 85 | 89 | 90 | 87 | 87 [C] |
| Buyout | 93 | 90 | 97 | 87 | 91 | 94 | 94 | 92 | ~91 [C] |
| Venture/Growth | 77 | 75 | 88 | 68 | 68 | 75 | 78 | 78 | ~79 [C] |
| Real estate | 83 | 76 | 79 | 71 | 71 | 72 | 71 | 70 | ~68 [C] |
| Credit | 85 | 78 | 83 | 72 | 77 | 91 | 92 | 91 | n/a |

Sources [S]: Jefferies Jan-2025 Fig. 3 (series mapped from the extracted chart values and cross-checked against the text), Jul-2025 and Feb-2026; H1-2026 values via secondary summaries [C]. Corroborating data:

- Evercore H1-2026: quality buyout "consistently in the 90s"; tail-end about 70% since 2022 with select tails in the 80s; senior credit at par or better; VC/growth softer in early 2026; software buyout and large-cap funds softer [S].
- Campbell Lutyens: value-weighted LP-led discount of 13.9% in 2025 vs 13.3% in 2024; top mid-market buyout in the mid-90s; blue-chip mega-buyout at par or a premium [S].
- Hamilton Lane: buyout LP interests at 91% of NAV [C].

**Fund age (buyout, 2024)** [S: Jefferies]: 0-3 years 99%; 4-6 years 96%; 7-9 years 88%; 10-12 years 79%; 13+ years 70%. Tail-end (>10 years) was 72% and 9% of volume in 2024. In 2025, funds under five years old traded at 95% and funds over ten years at 73% [S: Jefferies Feb-2026]. Asia funds trade at 30%+ discounts [S: Jefferies Jul-2025].

**History and crisis anchors** [S]:

- Cogent average high bid: 84.7% in H1-2008 and 61% in H2-2008 (83.5% after adjusting for public markets); 22% of buyout funds bid above 80%; 15% of funds drew high bids of 30% or less of NAV.
- Pre-YE-2008-NAV transactions: discounts averaged about 40% and reached 50%+; HarbourVest walked from a signed deal in October 2008 (WilmerHale).
- Trade press reports H2-2009 at 72% and H1-2010 at 79.6% (buyout 86.4%) [C].
- Academic sample, 2006-2014: average discount 13.8%; about 9% for 4-9-year funds; about 10% for 10+-year funds [S: Nadauld et al.].

### 4.3 Deal mechanics

- **Deferral.**
  - 2024: 20% of LP deals used deferral, about +400 bp vs cash [S: Jefferies].
  - 2025: about 23% of LP deals and about 29% of GP-led volume [S: Jefferies Feb-2026]. Evercore's FY-2025 report says deferral use declined year on year [S].
  - H1-2026 (Evercore): 66% of LP-led volume had no deferral; 3% deferred 1-6 months, 20% 7-12 months, 2% 13-18 months and 9% more than 18 months. 84% of GP-led volume had no deferral [S].
- **Intermediation and buyers.** 88% of H1-2026 LP-led volume was advisor-run and multi-bidder [S: Evercore]. Transactions averaged 1.9 buyers in H1-2025, down from 2.3 [S: Jefferies]. 63% of 2024 LP deals were single-buyer [S].
- **Structured share.** Structured transactions were about 8% of volume in H1-2025 [S: Jefferies]. Preferred equity was about 7% of total volume in 2024 [S: Jefferies] and 5% in 2025 on Campbell Lutyens' series (7-10% in 2021-2024) [S]. Preferred equity and other structured solutions were 14% of GP-led volume in 1H-2026, up from 10% [S: Lazard].
- **Seller mix (Evercore, LP-led volume)** [S]. In 2024 vs 2025: public pensions 31%→21%; FoFs 13%→23%; endowments and foundations 10%→12%; SWFs 2%→12%. In H1-2026, SWFs reached 21%. Jefferies puts endowments and foundations at 16% of H1-2025 LP volume (7% in H1-2024), linked to the expected excise-tax increase, and pensions at 48% [S]. Jefferies also reported effectively no distressed or forced sellers in H1-2025 [S].

### 4.4 GP-led continuation vehicles

- **Pricing.**
  - Lazard 1H-2026: about 87% of SACV volume priced above 90% of NAV; 23% above par (8% in 2025); MACVs about 60% above 90% (84% in 2025), and the MACV share below 90% rose to 40% from 16%; premium carry tiers in about 39% of deals [S].
  - Campbell Lutyens 2025 average discounts: SACV 3.1% and MACV 4.2% (2024: 3.6% and 9.0%) [S].
  - Evercore H1-2026: my reading of the chart is SACV 34% below par, 52% at par and 14% above; MACV 71% below, 22% at, 8% above. A third-party summary reads it as 71% of SACVs at par [C]. Treat this as ambiguous and use Lazard and Campbell Lutyens figures.
- **Buyer targets** (gross, about four years) [S: Evercore]: SACV about 2.3x; MACV about 1.9x; single LP about 1.8x; diversified LP about 1.7x. LP-led deals target mid-to-high-teens gross. Net-IRR targets: credit mostly 13-15% (55% of respondents); infrastructure mostly 13-15% (62%); venture mostly above 20% (81%) [S: Evercore FY-2025].
- **Scale.** CVs exited about 19% of sponsor-backed exit volume in H1-2025 (Jefferies) [S]. Nearly 80% of the top-100 sponsors have completed a CV [S: Jefferies Feb-2026]. Third-party leverage use by GP-led buyers rose from 7% to 14% in 2025 [S: Evercore].

### 4.5 Buyer capital and depth

| Metric | Value | Source |
|---|---|---|
| Dedicated capital (Jefferies) | US$288bn (2024), US$302bn (H1-25), US$327bn (2025); ~US$477bn incl. LP capital and leverage | [S] |
| Leverage assumption in capital stock | ~15% of equity dry powder + near-term fundraising | [S: Jefferies] |
| Capital overhang (Jefferies def.) | 1.8x (2024), 1.5x (H1-25) vs ~2.2x 5-yr avg | [S] |
| Dry powder (Evercore) | US$215bn (start 2026) → US$194bn (H1-26); LP-led US$90bn (−15% YTD) | [S] |
| Overhang (Evercore def.) | ~1.2x (2025) → ~1.0x (H1-26) | [S] |
| Evergreen | Evercore: ~US$500bn semi-liquid AUM, >US$130bn at secondary managers (~45% to secondaries); Jefferies: ~US$113bn 2025 evergreen inflows, ~41% to secondaries | [S] |

### 4.6 NAV financing

- **Size.** The Fund Finance Association estimates about US$100bn today, growing to US$600bn by 2030. ILPA (2024) cites this from 17Capital (Mar-2024) [S]. 17Capital now cites a US$700bn opportunity by 2030 (about US$150bn deployed a year) on Preqin data plus its own assumptions [S]. In 2023 Proskauer found most lenders closed fewer than six facilities a year, and noted the market "may indeed be smaller than some reports suggest" [S].
- **Pricing and terms, Proskauer FY-2023** [S]:
  - spreads over 3M Term SOFR by closing LTV: 5-10% → 533 bp; 11-25% → 681 bp; 26-50% → 764 bp; >50% → 982 bp;
  - secondaries facilities mostly 300-400 bp;
  - tenor 4-5 years in 66% of facilities;
  - closing LTV 11-25% most common (51%);
  - OID mostly 1-2.5%;
  - LTV-based sweeps 57%, fixed 29%, none 14%;
  - minimum MOICs below 1.30x prevalent.
- **Pricing and terms, Proskauer FY-2025** [S]:
  - primary spreads mostly below 5%, concentrated at 4-5%, with a meaningful share below 4%;
  - secondaries spreads below 4%, mostly below 3%;
  - primary closing LTV mostly below 25%, largest share 5-10%;
  - secondaries LTV 25-50% (57%) and 50-70% (43%);
  - upfront fees 1-2%;
  - maturities 3-5 years, with WAL shorter because of sweeps;
  - LTV-based sweeps common in primary and in 83% of secondaries facilities;
  - many deals have no minimum MOIC;
  - about 80% of respondents expect volume growth in 2026, and more than 70% expect stable LTVs;
  - significant use of CFOs and rated note feeders in 2025, especially by secondaries funds.

  A 2026 Rede Partners survey quoted margins of 4-7% [C].
- **Collateral.** Typically cash accounts plus preferred economic interests, extending to direct or indirect equity pledges. Structures use a dual SPV. Lenders call full foreclosure rare and prefer workouts [S: ILPA Part I].

### 4.7 CFOs and the Astrea template

- **Market** [S: Octus]: KBRA rated 14 US CFOs worth US$7.8bn in 2024; 2022 was the record year with 25 deals worth US$13.1bn. Average cost of debt on 2025 CFOs was SOFR+295 bp (one law firm's deals). Senior notes are usually single-A and bought by US insurers. The GP typically retains the equity. Maturities run 12-15 years. Examples: Coller US$2.4bn (April 2025); Churchill US$750m with a US$70m liquidity facility (March 2025). The 2024 UK matching-adjustment reform admits "predictable" cash flows.
- **US regulation** [S: Morgan Lewis 2023]: the NAIC appeared set to presume that debt backed solely by equity interests is not a bond-like creditor relationship. The current status of the principles-based bond definition and SVO discretion is unverified here.

**Astrea programme (Azalea / Temasek; nine issues since 2006)** [S: azalea.com.sg, accessed 2026-10-18]:

| Issue (prospectus) | Notes | Coupon | Call / maturity | Latest NAV & LTV | Latest half-year CFs | Ratings (Fitch, 2026) |
|---|---|---|---|---|---|---|
| Astrea 7 (May-2022) | A-1 S$526m (US$380m); A-2 US$175m; B US$200m | 4.125% / 5.35% / 6.00%; +1% step-up | 2027/2028 call; 2032 final | US$1,160m; LTV 24.5% | dist. US$152m; calls US$10m | AA-sf / AA-sf / A+sf |
| Astrea 8 (Jul-2024) | A-1 S$520m (US$385m); A-2 US$200m | 4.35% / 6.35%; +1% step-up | 2029/2030 call; 2039 final | US$1,149m; LTV 35.1% | dist. US$137m; calls US$12m | AA-sf / A+sf |
| Astrea 9 (Jul-2025) | A-1 S$615m (US$480m); A-2 US$200m; B PIK US$107m | 3.40% / 5.70% / 7.35% PIK; +1% step-up (A) | 2030 call; 2040 final | US$1,654m; Class A LTV 35.2%, B 41.4% | dist. US$104m; calls US$44m | AA-sf / AA-sf / Asf |

Astrea 9 was about 3.4x subscribed, with more than S$3.4bn of demand [S]. **Template lessons [I]:**

- A sovereign can turn a seasoned, diversified LP portfolio into long-dated, investment-grade, partly retail funding while keeping the equity.
- Ratings improve as LTV falls through distributions, as the 2026 upgrades show.
- Step-ups and scheduled calls create a refinancing option, and a refinancing risk.

---

## 5. Practitioner and peer practice: case studies

1. **Harvard, 2008-09: the forced-seller archetype.**
   - In October 2008 Harvard hired Cogent Partners to market a portfolio with an asking price above US$1bn. In December it was reported in talks to sell about US$1.5bn of LP stakes, including a Bain Capital fund. At the same time, stakes in KKR, Madison Dearborn and Terra Firma funds were being offered at discounts of at least 50%. Later reports say Harvard sold "more than US$1bn" at steep discounts and only part of what it intended [S/C: search-result excerpts of Buyouts, Bloomberg via NakedCapitalism, Yale Daily News 2012; full texts paywalled or blocked].
   - The endowment fell about US$8bn (~22%) amid a cash squeeze and losses from interest-rate, derivative and leveraged positions. HMC cut about 25% of staff and liquidated hedge-fund positions [S: Wikipedia citing NYT 20-Feb-2009]. That Harvard also issued about US$2.5bn of bonds in December 2008 is from memory and unverified.
   - *Lessons [I]:* liquidity was sought at the trough, when π was lowest and execution probability fell (buyers walked away). Unfunded commitments amplified calls. Liability-side leverage (swaps) and asset-side illiquidity compounded each other. Pre-arranged facilities and earlier pacing cuts would have been far cheaper.
2. **Yale, 2025: selling from strength.**
   - Reported at up to US$6bn in May [S: Moonfare]; by June it was up to US$2.5bn of PE and VC interests ("Project Gatsby"). Evercore advised, the expected overall discount was below 10%, Lexington and HarbourVest evaluated the book, and the "mosaic" format let buyers pick selected interests [S: Private Equity Wire 5-Jun-2025]. Yale said it remained committed to PE and was still making commitments [C]. Final terms and completion are unverified. Yale's endowment was US$44.1bn at FY-2025 with an 11.1% return [S: Wikipedia citing P&I].
   - *Lessons [I]:* sell in high-price regimes (buyout 92-94% in 2024-25); use mosaic structures to raise competition across heterogeneous interests; announce continued primary commitments to limit relationship cost.
3. **Harvard, 2025.** Reported talks to sell about US$1bn of PE to Lexington [S: Moonfare; Business Standard headline]. Completion and pricing are unverified. Endowments and foundations rose to 16% of LP volume in H1-2025, which Jefferies links partly to the excise tax [S].
4. **Pensions.** CalPERS reportedly sold "billions" of PE stakes to Ardian, AlpInvest and Partners Group in early 2025 while planning to grow PE exposure [C: Moonfare]. Pensions were 54% of 2024 LP volume, often selling partial commitments to core GPs together with mature or lower-quality funds [S: Jefferies].
5. **Sovereign peers, 2025-26.**
   - GIC, October 2025: at least US$1bn of NAV across about 30 funds, Evercore advising, ready to withdraw if bids missed expectations [C: BGOV/pe-insights, via search excerpt].
   - CIC, November 2025: about US$1bn of US PE stakes, Ardian among the final bidders, after signaling a pause in July [C: Bloomberg, via search excerpt].
   - KIC, 2026: weighing more than US$1bn with PJT [C: DealStreetAsia, via search excerpt].

   These are routine rebalancing trades of about US$1bn each, with reserve-price discipline. In aggregate they explain the SWF share rising to 21% [S].
6. **Temasek/Azalea Astrea.** Refinancing rather than selling, with the sponsor keeping the equity. This is the closest template for a sovereign endowment-model fund to monetize a seasoned PE book without crystallizing discounts (Section 4.7).
7. **GP-led practice.** About 75% of the 50 largest GPs have used CVs [S: Jefferies Jul-2025]. GP cross-fund commitments appeared in 34% of CVs [S]. Super-carry appears in more than a third of GP-leds [S: Evercore].

**Synthesis for ADIC [I].** Be the Yale-style planned seller with GIC-style reserve-price discipline. Use the Astrea-style refinancing channel for core, seasoned, high-quality pools. Never become the 2008 Harvard-style forced seller, whose 40-50% discounts were mostly paid to buyers holding dry powder in a cash-in-the-market regime.

---

## 6. Design implications for the ADIC framework

**Sizing context [I].** At US$177bn with about 60% private, private NAV is about US$106bn. The 5-10% payout is about US$8.9-17.7bn a year. A US$5bn-a-year secondary programme would be about 4% of 2025 LP-led volume. Annualizing H1-2026, it would also be about 20% of the SWF seller segment (21% × ~US$112bn ≈ US$24bn). That makes price impact and signaling first-order.

### 6.1 State variables

| Symbol | Description | Default / source |
|---|---|---|
| $NAV^{rep}_{i,t}$, $\widehat V_{i,t}$ | reported and de-smoothed value per interest | de-smoothing via public-factor beta and lag (stream on PE cash flows) |
| $U_{i,t}$ | unfunded commitment | holdings data |
| $a_i$, strat, GP tier, geo, software share | hedonic features | holdings data |
| $\mathcal B_{i}$ | belief set {UW, ACT, SG, MKT} for future $D,C$ | fused in belief stream; MKT = buyer-target-implied |
| $e_{i,t}\in\{\text{free},\text{pledged},\text{CFO},\text{pref},\text{sold}\}$ | encumbrance status | – |
| $g_i$ | transferability: consent standard, ROFR, pledge consent probability | LPA review [S: WilmerHale on consent/ROFR] |
| $s_t$ | regime (HMM) | prior deck |
| $\Pi^{strat}_t$ | consensus secondary price index by strategy (Kalman) | Section 4.2 anchors |
| $O_t$ | capital overhang multiple | 1.0-1.2x (Evercore H1-26) [S] |
| $S_t(\ell)$, SOFR$_t$ | NAV-loan spread curve by LTV | Proskauer 2023/2025 [S] |
| $\kappa^{CFO}_t$ | CFO senior spread | ~SOFR+295 bp (2025) [S] |
| $B_{k,t},\ell_{k,t},h_{k,t}$ | facility balance, LTV, covenant headroom | – |
| $L_t$, $M_t$, $d_t$ | liquid assets, overlay margin, payout due (5-10%) | other streams |

### 6.2 Decision variables (per period)

- $x_i\in[0,1]$: fraction of interest $i$ sold. Binary per interest for mosaic packaging, continuous for strip sales.
- $\phi_i$: upfront share if a deferral is accepted.
- $z_i\in\{\text{sell},\text{roll},\text{SQ}\}$: CV elections.
- $b_{k,t}$: LP-level NAV draw or repay.
- $p_{P,t}$: preferred-equity advance on pool $P$.
- $c_{P,t}\in\{0,1\}$: CFO issuance, lumpy, at most one per 12-24 months.
- $n_t$: new commitments (pacing).
- Hand-offs to the LEVER and overlay streams.

### 6.3 Constraints (to sit inside Tier 1)

1. **Liquidity survival:** $\Pr\big(L_t+\sum\text{proceeds}_t-C_t-\text{payout}_t-M_t\ge L^{min}_t\big)\ge1-\alpha$, with α=5% to match the prior deck. Only liquidity with $\tau_j\le H$ and $p_j(s)$ applied counts toward horizon $H$.
2. **30-day bucket:** committed undrawn NAV revolvers count at a haircut $h^{rev}\ge50\%$ [I]. Lenders can block draws through LTV or eligibility tests in stress. By analogy, Basel's LCR gives banks no credit for committed facilities they receive [I].
3. **Covenant chance constraint:** $\Pr(\ell_{k,t}\ge\ell^{trig}_k)\le\alpha_{cov}$ for each facility over its life under the misspecification set. Default $\alpha_{cov}=5\%$, with $\ell^{trig}=1.5\ell_0$ and $\ell^{def}=2\ell_0$ [I].
4. **Encumbrance cap:** $\sum_{i:e_i\neq\text{free}}\widehat V_i\le E^{max}=25\%$ of private NAV [I] (cf. bank asset-encumbrance monitoring). No double pledging.
5. **Market capacity:** $\sum_{i\in\text{strat}}x_i\widehat V_i\le\theta\cdot\text{Depth}^{strat}_t$, with θ=5% of LTM LP-led strategy volume per year [I].
6. **Relationship:** at most two exits per GP per three years, and preserve tier-1 GP primary access [I]. Tie to $g_i$.
7. **Governance:** CV decisions within ILPA windows (20 business days) [S]. Use LPAC votes to steer fund-level NAV loans used for distributions [S].

### 6.4 Objective terms (Tier 2)

$$\max\;\Pr\big(R^{ann}_{5y}\ge10\%\big)\;\text{or}\;\mathbb E[U(W_T)]\;-\;\sum_{t,k}\underbrace{PV_m(G^k_t)-PV_m(L^k_t)}_{\text{liquidity cost}}\;-\;\eta\,\text{Irrev}\;-\;\zeta\,\text{Signal}\;-\;\xi\,\mathbb E[\text{fire-sale loss}]$$

- $\text{Irrev}_i=\max(0,\mathbb E[\pi_{t+1}\mid s_t]-\pi_t)\cdot\widehat V_i$ is the expected discount recovery from waiting one semester.
- Signal is a per-GP relationship cost: probability of losing access times the value of future primary alpha.

### 6.5 Key equations to implement

- **Price:** $\pi_{i,t}=\frac{\widehat V_{i,t}}{NAV^{ref}_i}\exp\!\big(\mu_{s_t}+\beta^\top f_i-\kappa_{s_t}q_t/\text{Depth}_t+\varepsilon_i\big)$, with $\widehat V/NAV^{ref}=\exp(\beta^{PE}r^{mkt}_{ref\to t})$ for staleness.
- **Liquidity released:** $LR_{i,H}=P_i+\sum_{t\le H}(C^{s^\*}_{i,t}-D^{s^\*}_{i,t})$. Favor selling young, unfunded-heavy, low-conviction interests when calls are the binding risk.
- **MCL clearing:** $\lambda_H=\text{MCL}_H(L^\*_H)$. Reserve price: sell $i$ only if $c_i\le\lambda_H$ and $y^{SG}_i-\lambda\le\delta^{belief}$ [I].
- **NAV covenant dynamics:** see Section 3.2(4). $\mathbb E[\text{fire-sale}]=\sum_t\Pr(\ell_t>\ell^{def})\cdot(1-\pi^{crisis})\cdot\text{forced amount}$.

### 6.6 Calibration table (defaults as of 2026-10; recalibrate semiannually)

| Parameter | Benign | Stress | Crisis | Basis |
|---|---|---|---|---|
| π buyout | 0.92 | 0.87 | 0.60-0.65 | 2024-25 / 2022 / H2-08 [S]; crisis = normal × 61/89 [I] |
| π all strategies | 0.88 | 0.81 | 0.55-0.61 | [S/I] |
| π VC/growth | 0.78 | 0.68 | 0.45-0.50 | [S/I] |
| π real estate | 0.71 | 0.70 | 0.45-0.50 | [S/I] |
| π credit (senior) | 0.92-1.00 | 0.72-0.77 | 0.55 | [S/I] |
| π tail (>10y) | 0.70-0.73 | 0.60 | 0.40-0.45 | [S/I] |
| Age gradient (buyout, benign) | 0.99/0.96/0.88/0.79/0.70 | ×0.93 | ×0.70 | Jefferies 2024 [S]; [I] |
| Transient shock | −3 to −5 pp, half-life <1 quarter | | | Apr-2025 [S] |
| Deferral uplift / share / tenor | +4 pp / 26-50% / ≤12m | – | rare | [S] |
| NAV spread (LTV ≤10 / 10-25 / 25-50%) | 400-450 / 450-500 / 550-650 bp | 533 / 681 / 764 bp | unavailable or >1,000 bp | Proskauer 2025 [S]; 2023 [S]; crisis [I] |
| OID; tenor; sweep σ(ℓ) | 1-1.5%; 3-5y; 25%→100% as ℓ rises | 2-2.5% | – | [S]; σ schedule [I] |
| LP-level LTV cap (diversified, at NAV) | 15-25% | 10-15% | 0-10% | [I], benchmarked to primary 5-25% [S] |
| CFO senior LTV; cost; lead time | 35-45%; SOFR+250-300 bp; 6-12m | 25-35%; +150 bp | closed | Astrea, Octus [S]; [I] |
| Pref: advance; accrual; MOIC floor | 20-35%; 12%; 1.3x | 15-25%; 14%; 1.4x | scarce | illustrative [I]; ≤50% LTV [S] |
| Buyer target IRR (gross) | div. LP 14%; single LP 16%; MACV 17%; SACV 23% | +3-5 pp | +10 pp | Evercore [S]; [I] |
| Execution probability $p_j$ | 0.85-0.95 | 0.70 | 0.40-0.50 | ~27% failed or paused 1H-26 [S]; [I] |
| Overhang $O_t$ | ≥1.8x | 1.0-1.5x | <1.0x | Jefferies, Evercore [S]; [I] |
| SWF seller share of LP-led | 21% (H1-26) | | | Evercore [S] |
| Forced-sale hazard prior (lattice) | 1%/qtr base, +1% per net public-equity down-move; two-state haircut, more likely after declines | | | Bollen-Sensoy 2015 WP [S] (model assumption, not an estimate) |

### 6.7 Data needs

1. Interest-level holdings: NAV and reference dates, unfunded, cash-flow history, GP, vintage, strategy, sector and software look-through, LPA transfer terms (consent standard, ROFR, pledge permissions), side letters, existing encumbrances.
2. Bid data: ADIC's own process bids and indications (the most valuable input), plus semiannual advisor reports (Jefferies, Evercore, Lazard, Campbell Lutyens, PJT) captured with methodology metadata.
3. Financing quotes: quarterly indicative term sheets from NAV lenders, CFO arrangers and preferred providers. This makes S(ℓ) and capacity observable.
4. Market state: public-factor returns since each NAV reference date, credit spreads, secondary fundraising and dry powder, and IPO and M&A exit volumes.

### 6.8 Agentic and IC integration

- **Liquidity-Tool Librarian agent:** ingests new advisor reports and extracts every number with source, date and methodology tags. It rejects untagged numbers under a rubric gate and updates the Kalman consensus index.
- **Structuring agent:** proposes candidate programmes, for example "US$2bn tail mosaic + US$3bn LP-level NAV facility + defer US$1.5bn of commitments." It never computes numbers itself; the deterministic engine prices each programme and returns the MCL position.
- **Red-team agent:** runs crisis transitions (NAV −25% de-smoothed, distributions −50%, execution probability 0.5) through the covenant recursions and recomputes $LR_H$.
- **Relationship and Governance agent:** checks GP consent and ROFR, ILPA windows, and LPAC votes.
- **IC "Action Economics Card"** per holding or programme:
  - proceeds today and by horizon;
  - $y^{UW},y^{ACT},y^{SG},y^{MKT}$ and $c_k$;
  - λ and the reserve price;
  - liquidity released under stress;
  - covenant-breach probability;
  - irreversibility (expected recovery from waiting a semester);
  - signaling cost;
  - a regret table showing what happens if we wait one semester in each regime.

---

## 7. Implementation notes

- **Libraries:**
  - cash flows: `numpy`, `pandas`; IRR via `scipy.optimize.brentq` on NPV with bracket search (avoid `numpy_financial.irr` on sign-changing flows);
  - optimization: `cvxpy` (Clarabel, HiGHS or MOSEK) for the convex inner MCL problem; `pyomo` or `OR-Tools` CP-SAT for mosaic packaging and lumpy CFO decisions;
  - pricing: `PyMC` or `NumPyro` for hierarchical price models; `LightGBM` with `monotone_constraints` plus `MAPIE` for conformal bid intervals;
  - consensus index: `statsmodels` `UnobservedComponents` or `MarkovRegression`;
  - note and swap pricing for CFO tranches and SGD/USD conversion: `QuantLib`;
  - simulation: `numba` or `JAX`.
- **Algorithms:**
  - Inner problem: per scenario and date, an MCL LP or MILP with about $10^3$-$10^4$ tranche variables. Solves in seconds; duals give λ.
  - Outer problem: either (a) scenario-tree MPC with re-solve each semester, or (b) SDDP-style cuts on aggregate state ($L_t$, encumbrance, regime) with asset detail handled by the inner MCL. That is decomposition by time scale, as in control-theory hierarchies [I].
  - Optimal-stopping "sell now vs wait": Longstaff-Schwartz (2001) least-squares Monte Carlo on regime-switching π paths.
  - Covenant risk: path simulation with de-smoothed NAV at $O(N_{paths}\times T\times K)$, which is cheap.
- **Numerical pitfalls:**
  1. IRR multiple roots from unfunded calls: report NPV at the hurdle, MIRR or $c_k$ alongside IRR.
  2. Staleness: compute discounts against de-smoothed value, not reported NAV; keep reference-date adjustments [S: WilmerHale].
  3. Survivorship: failed or paused processes (about 27% in 1H-26 [S]) are missing from price data, so model a selection equation (Heckman 1979).
  4. Advisor heterogeneity: volume includes unfunded commitments (Evercore definition [S]); Campbell Lutyens weights by value including unfunded; Jefferies uses simple averages. Never mix series without the state-space bias terms.
  5. Negative-price states for unfunded-heavy interests: allow $P<0$ in the model.
  6. Lumpiness: a CFO needs a minimum pool and lead time, so use binary variables with a lag.
  7. Currency: Astrea's SGD tranches need cross-currency basis.
  8. Path-dependent preferred and MOIC floors are non-convex in $a$: grid-search $a$.

---

## 8. Risks, pitfalls and limitations

- **Pro-cyclicality.** NAV facilities and CFO triggers tighten exactly when liquidity is scarce, and LTV-based sweeps divert distributions [S]. Over-reliance converts a liquidity problem into a forced-sale problem. Encumbrance caps and covenant chance constraints are mandatory [I].
- **Belief bias.** The implied cost of a sale is dominated by forecast dispersion (Section 3.2 example: 6-15% across ±10% forecasts). Strategy-group forecasts have historically been too optimistic on distribution timing (prior deck memo-corpus). Always show $y^{MKT}$ and the belief gap.
- **Information asymmetry.** In GP-led sales, the GP and buyers know more. Selling LPs systematically leave upside on the table where buyers underwrite about 2.3x [S/I].
- **Relationship and signaling.** These are unquantified in the literature, and large sovereign sales are visible. Mitigate with strip or mosaic formats and continued primaries [C/I].
- **Data quality.** Advisor data are survey-based, non-audited and methodologically inconsistent. Volume estimates differ by about 6% for 2025 and pricing by about 1-2 pp [S].
- **Regulatory drift.** NAIC and SVO treatment of CFOs, ILPA's 2026 CV guidance and SEC rules for adviser-led secondaries are moving targets; some are unverified here.
- **Model risk.** Regime-conditional price parameters for "crisis" come from a single episode (2008-09) and are extrapolated [I].
- **Execution risk.** About 27% of transactions failed or paused in 1H-2026 [S]. Buyers walked from signed deals in 2008 [S]. GPs can refuse consent.

---

## 9. Open questions

1. Does ADIC hold proprietary bid history, or past advisor indications, sufficient to fit an ADIC-specific hedonic model? If not, can we run a confidential pricing-indication exercise on a test portfolio?
2. What is ADIC's own unsecured or committed funding cost and capacity? This is the anchor rung of the pecking order (LEVER stream).
3. Which LPAs permit pledges and SPV transfers without GP consent? This determines eligible pools for LP-level NAV facilities, preferred equity and CFOs.
4. Could ADIC sponsor an Astrea-like vehicle? Questions include its legal domicile, rating appetite, investor base, and whether a sovereign-retained-equity CFO is politically and reputationally acceptable to the owner.
5. How should the relationship cost of exiting a GP be parameterized? Candidate approach: elicit from the PE team the probability of losing access times the value of alpha.
6. What reserve-price policy should apply (λ-based vs fixed discount caps), and who is delegated to accept bids within the band?
7. How do NAV-loan-financed distributions in ADIC's existing funds affect forecast distributions (synthetic DPI) and recall risk? This needs a GP survey using the ILPA disclosure template.
8. What are current NAIC and SVO positions on equity-backed CFO notes, and how do they affect insurer demand and pricing? Verify against primary NAIC sources.
9. What were the actual terms and completion of the Yale and Harvard 2025 sales and of the GIC, CIC and KIC processes? This is useful for peer calibration of sovereign execution.

---

## 10. References

1. Jefferies (10-Feb-2026). *2025 Global Secondary Market Review: Another Record-Breaking Year.* https://www.jefferies.com/insights/the-big-picture/2025-global-secondary-market-review-another-record-breaking-year/
2. Jefferies (Jan-2025). *Global Secondary Market Review, January 2025.* https://www.jefferies.com/wp-content/uploads/sites/4/2025/02/Jefferies-Global-Secondary-Market-Review-January-2025.pdf
3. Jefferies (Jul-2025). *H1 2025 Global Secondary Market Review.* https://www.jefferies.com/wp-content/uploads/sites/4/2025/08/Jefferies-Global-Secondary-Market-Review-July-2025.pdf
4. Jefferies (Jul-2026). *Global Secondary Market Review, July 2026* (image-only; figures via summaries). https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
5. Evercore Private Capital Advisory (Jul-2026). *H1 2026 Secondary Market Review.* https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
6. Evercore Private Capital Advisory (Feb-2026). *2025 Secondary Market Report.* https://www.evercore.com/wp-content/uploads/2026/02/Evercore-PCA-2025-Secondary-Market-Report.pdf . Its p.13 (PDF p.14) summarizes the fourth HEC Paris continuation-vehicle performance study by Prof. Oliver Gottschalg's team (methodology note, p.17), the source of the "buy again" quote in §3.2(3).
7. Lazard Private Capital Advisory (Aug-2026). *Interim Secondary Market Report 2026.* https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf
8. Campbell Lutyens (2026). *2025 Secondary Market Flash Report.* https://campbell-lutyens.com/media/qwydmsgy/2025-secondary-market-flash-report_campbell-lutyens.pdf
9. Proskauer (2024). *Insights on the NAV Lending Market, Full Year 2023.* https://www.proskauer.com/uploads/insights-on-the-nav-lending-market-2023
10. Proskauer (2026). *Insights on the NAV Financing Market, Full Year 2025.* https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025
11. ILPA (25-Jul-2024). *NAV-Based Facilities guidance, Parts I-V.* https://ilpa.org/resource/nav-based-facilities-guidance/ ; Part I: https://ilpa.org/wp-content/uploads/2024/11/Part-I-Nav-Based-Facilities-Guidance.pdf ; Part II: https://ilpa.org/wp-content/uploads/2024/11/Part-II-Nav-Based-Facilities-Guidance.pdf ; Roadmap: https://ilpa.org/industry-guidance/principles-best-practices/nav-based-facilities-guidance-roadmap/
12. ILPA (May-2023). *Continuation Funds: Considerations for Limited Partners and General Partners.* https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf ; 2026 draft CV guidance page: https://ilpa.org/industry-guidance/principles-best-practices/continuation-funds/
13. ILPA (Jun-2017). *Subscription Lines of Credit and Alignment of Interests.* https://ilpa.org/wp-content/uploads/2017/06/ILPA-Subscription-Lines-of-Credit-and-Alignment-of-Interests-June-2017.pdf ; ILPA (Jun-2020) *Enhancing Transparency Around Subscription Lines of Credit*: https://ilpa.org/resources-tools/resource-library/enhancing-transparency-around-subscription-lines-of-credit/
14. Nadauld, T. D., Sensoy, B. A., Vorkink, K., & Weisbach, M. S. (2019). The liquidity cost of private equity investments: Evidence from secondary market transactions. *Journal of Financial Economics* 132(3), 158-181 (DOI 10.1016/j.jfineco.2018.11.007); NBER WP 22404 (2016). https://www.nber.org/papers/w22404
15. Bollen, N. P. B., & Sensoy, B. A. (2022). How much for a haircut? Illiquidity, secondary markets, and the value of private equity. *Financial Management* 51(2), 501-538 (DOI 10.1111/fima.12375). https://ideas.repec.org/a/bla/finmgt/v51y2022i2p501-538.html ; WP (2015): https://ilpa.org/wp-content/uploads/2015/09/Bollen-How-Much-For-A-Haircut-Illiquidity-The-Secondary-Market-And-The-Value-Of-Private-Equity-2015.05.pdf . The "5-10 pp" figure in §2.2 is from the 2015 WP (p.2), not the published paper.
16. Albuquerque, R., Cassel, J., Phalippou, L., & Schroth, E. (2018). *Liquidity Provision in the Secondary Market for Private Equity Fund Stakes.* Working paper, Cass Business School; SSRN, DOI 10.2139/ssrn.3182481 (Crossref). Citation also verified via the reference list at https://pubsonline.informs.org/doi/references/10.1287/mnsc.2022.4612 ; abstract-level findings in §2.2.
17. Maurin, V., Robinson, D. T., & Strömberg, P. (2023). A Theory of Liquidity in Private Equity. *Management Science* 69(10), 5740-5771 (DOI 10.1287/mnsc.2022.4612). https://pubsonline.informs.org/doi/10.1287/mnsc.2022.4612 . Authors, volume and pages confirmed via Crossref (2026-10-18).
18. Unquote (26-Jan-2009). *Secondaries pricing dips to a five-year low* (Cogent Partners data). https://www.unquote.com/uk/news/85756/secondaries-pricing-dips-to-a-five-year-low
19. Beaudoin, T. A., Berrent, J. C., Evans, S. C., & Rothermel, S. (2009). Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets. *Business Law Today* (American Bar Association) 18(4), March/April 2009. WilmerHale reprint: https://www.wilmerhale.com/-/media/files/wilmerhale_shared_content/files/editorial/publication/blt_ma09_secondarymarket.pdf ; WilmerHale page: https://www.wilmerhale.com/en/insights/publications/trends-in-the-private-equity-secondary-market-march-april-2009 . Cited in the text as "WilmerHale". Title, authors and venue confirmed from the reprint's text layer (2026-10-18).
20. Private Equity Wire (5-Jun-2025). *Yale nears $2.5bn secondary sale of PE and VC stakes.* https://www.privateequitywire.co.uk/yale-nears-2-5bn-secondary-sale-of-pe-and-vc-stakes/
21. Moonfare (26-May-2025). *Endowments and private equity secondaries.* https://www.moonfare.com/blog/endowments-private-equity-secondaries
22. Harvard 2008-09 (excerpts only): NakedCapitalism (Dec-2008) https://www.nakedcapitalism.com/2008/12/harvard-yale-other-big-endowments.html ; Buyouts PE Week Wire (14-Oct-2008) https://www.buyoutsinsider.com/pe-week-wire-tuesday-october-14-2008/ ; Yale Daily News (13-Mar-2012) https://yaledailynews.com/blog/2012/03/13/harvard-struggles-to-get-rid-of-illiquid-assets/ ; Wikipedia, Harvard Management Company (citing NYT 20-Feb-2009) https://en.wikipedia.org/wiki/Harvard_Management_Company
23. Bloomberg Government (Oct-2025). *Singapore's GIC Seeks to Sell $1 Billion of Stakes in PE Funds.* https://news.bgov.com/private-equity/singapores-gic-seeks-to-sell-1-billion-of-stakes-in-pe-funds ; PE Insights: https://pe-insights.com/gic-tests-booming-secondaries-market-with-1bn-private-equity-stake-sale/
24. Bloomberg (28-Nov-2025). *CIC Close to Selling $1 Billion in US Private Equity Stakes.* https://www.bloomberg.com/news/articles/2025-11-28/cic-close-to-selling-1-billion-in-us-private-equity-stakes
25. DealStreetAsia (2026). *Korean wealth fund weighs sale of more than $1b of PE stakes.* https://www.dealstreetasia.com/stories/kic-private-equity-stake-sale-495810
26. Azalea Asset Management (accessed 18-Oct-2026). Astrea programme pages: https://www.azalea.com.sg/ ; https://www.azalea.com.sg/products/astrea-7 ; https://www.azalea.com.sg/products/astrea-8 ; https://www.azalea.com.sg/products/astrea-9
27. Octus (9-Sep-2025). *Demand for collateralized fund obligations surges amid UK Solvency II reforms.* https://octus.com/resources/articles/demand-for-collateralized-fund-obligations-surges-amid-uk-solvency-ii-reforms/
28. Morgan Lewis (8-Nov-2023). *Collateralised fund obligations and rated note feeders.* https://www.morganlewis.com/de/pubs/2023/11/collateralised-fund-obligations-and-rated-note-feeders-options-for-structuring-investment-into-private-funds
29. Loan Market Association (Apr-2026). *Fund Finance Insights: The Growing Focus on CFOs.* https://www.lma.eu.com/application/files/8217/7486/6513/LMA_Fund_Finance_Insights_-_CFOs_-_April_2026.pdf
30. Davis Polk (23-Jan-2026). *The continuing use of preferred equity in private equity NAV facilities* (GLI Fund Finance 2026, ch. 9). https://www.davispolk.com/insights/articles-books/continuing-use-preferred-equity-private-equity-net-asset-value-facilities
31. Clifford Chance (May-2020). *Decoding the secondary market, Part II: preferred equity.* https://www.cliffordchance.com/content/dam/cliffordchance/briefings/2020/05/decoding-the-secondary-market-part-ii-preferred-equity.pdf (via search excerpt)
32. 17Capital (accessed 18-Oct-2026). Homepage and NAV-finance claims. https://www.17capital.com/
33. AI-CIO (31-Jul-2025). *LP-, GP-led secondaries grow to record volumes in 2025.* https://www.ai-cio.com/news/lp-gp-led-secondaries-grow-to-record-volumes-in-2025/
34. Augment (1-Oct-2026). *Exit, Voice and the Continuation Fund* (secondary summary; [C]). https://augment.market/pulse/exit-voice-and-the-continuation-fund
35. Wikipedia, *Yale Investments Office* (citing Pensions & Investments, 24-Oct-2025). https://en.wikipedia.org/wiki/Yale_Investments_Office
36. Angel Investors Network (2026), aggregator of H1-2026 advisor data ([C], low reliability). https://angelinvestorsnetwork.com/market-analysis/private-equity-secondaries-record-250-billion-2026
37. Dixit, A. K., & Pindyck, R. S. (1994). *Investment under Uncertainty.* Princeton University Press. DOI 10.1515/9781400830176 (e-book).
38. Longstaff, F. A., & Schwartz, E. S. (2001). Valuing American Options by Simulation: A Simple Least-Squares Approach. *Review of Financial Studies* 14(1), 113-147 (DOI 10.1093/rfs/14.1.113).
39. Heckman, J. J. (1979). Sample Selection Bias as a Specification Error. *Econometrica* 47(1), 153-161 (DOI 10.2307/1912352).

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 and `research/literature/05_secondaries_navfin.lit.md` §1-2. Metadata confirmed via Crossref, OpenAlex, IDEAS/RePEc and the source PDFs' text layers.

- §2.2 Bollen-Sensoy: "5-10 pp" re-attributed to the 2015 WP (p.2, quoted wording), and the published *Financial Management* (2022) headline added (breakeven returns match observed returns for moderately risk-tolerant LPs with up to 40% in PE); published magnitude marked unverified.
- §2.2 Albuquerque et al.: "I could not retrieve their estimates" replaced by their abstract-level findings (literature check B3).
- §2.2 Maurin et al.: "authorship as I recall it and not re-verified" replaced by *Management Science* 69(10), 2023, authorship confirmed by Crossref.
- §2.3 "Dixit-Pindyck" now "Dixit and Pindyck 1994" (new ref 37).
- §3.2(3) "[S: Evercore/HEC]": source identified as Evercore FY-2025 (ref 6), p.13, summarizing the fourth HEC Paris CV study by Prof. Oliver Gottschalg's team; the claim is reworded to the source's wording, with "informed counterparties" tagged [I].
- §7 "Longstaff-Schwartz" now "Longstaff-Schwartz (2001)" (new ref 38); "Heckman-style" now "Heckman 1979" (new ref 39).
- Ref 6: note added locating the HEC study summary (p.13; methodology p.17).
- Ref 14 (Nadauld et al.): added *JFE* 132(3), 158-181.
- Ref 15 (Bollen & Sensoy): note added that "5-10 pp" is from the 2015 WP, not the published paper.
- Ref 16 (Albuquerque et al.): added SSRN DOI 10.2139/ssrn.3182481; "findings not retrieved" removed.
- Ref 17: authors (Maurin, Robinson & Strömberg), 2023, 69(10), 5740-5771 added; "authors from memory; not re-verified" removed.
- Ref 19: title corrected from "Secondary market for private equity interests" to "Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets"; authors Beaudoin, Berrent, Evans & Rothermel added; venue *Business Law Today* 18(4), March/April 2009 confirmed; WilmerHale page URL added.
- Refs 37-39 added: Dixit & Pindyck (1994); Longstaff & Schwartz (2001), *RFS* 14(1):113-147; Heckman (1979), *Econometrica* 47(1):153-161.
