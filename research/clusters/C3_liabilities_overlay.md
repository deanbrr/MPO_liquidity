# Cluster C3: distribution policy and sovereign liabilities, peers/TPA, and the derivatives overlay

*Integrated synthesis of Streams 02, 03 and 09 for the ADIC multi-period robust TPA framework (agentic). As of 18 Oct 2026.*

**Inputs.**
- The dossiers and adversarial verification logs for:
  - Stream 02: endowment model, distribution policy, SWF peers and TPA;
  - Stream 03: sovereign ALM, with the owner's draw treated as a stochastic liability;
  - Stream 09: the derivatives overlay (tail protection, opportunistic trading, collateral and margin).
- The project context file.
- Streams 01, 04, 05, 06, 10, 11, 12 and 14, consulted only to align notation and hand-offs.

**Evidence tags.**

| Tag | Meaning |
|---|---|
| [S] | Sourced and confirmed by the verifier |
| [S-c] | Sourced but corrected by the verifier; the corrected value is the one shown |
| [S*] | Confirmed only via the dossier's secondary source |
| [U] | Unverified or unverifiable |
| [I] | Design inference |
| [I-calc] | Computation. "rep." = reproduced by the verifier; "C3" = arithmetic re-checked for this synthesis |
| [I-MC] | Stylised simulation: assumption-driven, not a forecast |

**Client facts are not public.** The US$177bn size, the 5–10% band, the 10% target, the leverage permission and the ~60% private share cannot be checked against public sources. Bloomberg (4 Feb 2026) described a "US$160bn" endowment-style fund targeting ≥10% [S, headline and summary only].

**Status.** The verifiers rated facts HIGH in all three streams and the design layers MEDIUM. Every verifier correction is applied in §2. Every design question gets a recommendation in §3.

---

## 1. Executive summary

1. **This is one problem, not three.**
   - The owner's draw, the private book's net cash flows and the overlay's collateral flows all settle in one liquidity ledger.
   - In stress, the binding currency is unencumbered liquidity.
   - Its price, the liquidity shadow price λ, makes distribution policy, hedge design and SELL/HOLD/REFINANCE/LEVER comparable.
   - Every component below emits or consumes λ in one unit: present-value US$ per US$ of liquidity.

2. **The mandate arithmetic is tight.**
   - The 10% target is coherent only as a gross, pre-distribution, nominal, geometric return.
   - Real NAV is preserved only if $d\le d^*=1-(1+\pi)/(1+g)$. That gives 6.8% at g = 10% and π = 2.5%, and ≈4.5–4.6% at a peer-realistic 7.4% [I-calc rep.].
   - The 5–10% band therefore straddles sustainability. Its upper half is planned real decumulation.
   - With E[R] = 10% at 12% volatility, P(20-year annualised return ≥ 10%) is only ≈42% [I-MC rep.].

3. **Who owns the band is the most decision-relevant unknown.**
   - If ADIC sets the rate within 5–10%, the band is valuable flexibility.
   - If the owner calls draws according to its fiscal needs, ADIC is short a NAV-scaled put spread on the owner's fiscal state.
   - We specify a mandate switch that simulates both regimes and prices the difference with finite-difference shadow prices.
   - This replaces the dossier's use of DWY's ~2% certainty-equivalent figure as the "value of flexibility", which the verifier called a category error.

4. **Today's private-cash regime matches the dossier's "drought" case, not its "base".**
   - Distribution rates are 9–12% of NAV: MSCI global PE was 11% in 2025 and 9% in H1 2026, and Jefferies puts LP portfolios near 10% in H1 2026 [sourced in Streams 04/06; outside this cluster's verification].
   - The 14% figure used in Streams 02/03 is Bain's buyout ratio, built on MSCI data.
   - Stream 02's model at a 10% distribution yield and a 7.5% payout gives:
     - P(forced secondary sale within 10 years) of **10.9% with a 15% liquidity floor and 60.4% with a 25% floor**;
     - P(private share > 70%) of 92% (25% floor);
     - but a mean cumulative sale loss of only ≈0.64% of starting NAV [I-MC rep.].
   - Forced-sale frequency is an artifact of the chosen floor, and the severity is small. The real cost is the *denominator ratchet*: payouts drawn from the liquid book push the private share up.

5. **Owner demand is wrong-way only in some oil states.**
   - The monthly oil–equity correlation changes sign by era: −0.14 before 2008, +0.43 in 2008–19 and +0.32 in 2020–Aug 2026, all with wide confidence intervals [I-calc rep.].
   - "Oil down" splits into two states:
     - supply gluts (SG): draws rise, but markets are fine and exits stay open;
     - demand busts (DB): draws rise, equities fall and exits shut. This is the triple wrong-way state.
   - 2026 adds a Gulf-war state (GW) in which oil is up but owner needs rise. The IMF projects the UAE surplus falling from 3.9% to 1.5% of GDP despite higher oil; this is a projection [S].
   - A shock-type layer $Z_t$, identified from economic structure plus news events, is required, because statistical regimes do not separate these types.

6. **Draw levels are lower than the dossier's prose and depend heavily on the owner's breakeven oil price.**
   - Under the default priors, mean draws in DB/SG are 6.9%/6.8% at a US$44.8 breakeven, 7.6%/7.6% at US$55 and 8.1–8.2% at US$65.
   - P(≥3 consecutive years at draws ≥9.5%) rises from ≈1% to 10–15% as the breakeven goes from 44.8 to 65 [I-MC rep.].
   - These runs exclude override, peg stress, energy-transition drift, the declining hydrocarbon share and oil jumps.
   - Cap draws in coverage ratios are therefore a *stress assumption*, not an expectation.

7. **The fiscal mapping and the oil-hedge size are corrected.**
   - The kink strikes depend on the functional form:
     - log form: draw at the 5% floor above ≈US$64 Brent and at the 10% cap below ≈US$31;
     - linear-in-price form ($P^{ref}$ = 62.5): ≈US$67 and ≈US$23 [I-calc C3].
   - We default to the linear form, because revenue = price × volume.
   - Under the linear form the target draw is a plain vertical put spread worth ≈US$200m of draw per US$1/bbl at US$177bn NAV.
   - With draw smoothing $\rho_d$ = 0.5, same-year exposure is ≈100m bbl, not 266m. A 20–40% hedge is therefore ≈20–40m bbl in year 1.

8. **As liquidity insurance, cash buffers dominate options. Options have to earn their place on other grounds.**
   - In the Jeanne–Rancière reserves model (§5.7), at ADIC-scale crisis gaps (≈15% of NAV), high-quality liquid assets (HQLA) at a 1.5% carry cost give an interior optimal buffer of ≈7.5% of NAV.
   - Measured option costs are 0.28–0.94 per $ of crisis payoff on a common 2008–26 window (≈0.4–0.9 excluding COVID). These are corner solutions ("do not insure"), except VIX-call (VXTH-like) structures at very high IC penalty curvature [S/I-calc rep.+C3].
   - Convexity is justified only by three things:
     - enabling value, meaning it relaxes Tier-1 constraints;
     - protection against price gaps and decision latency;
     - pre-committed rebalancing.
   - Two dossier parameters biased the case toward convexity: the spot–vol slope (−1.7 against a verified −1.35) and hindsight trough dating.

9. **Recommended defensive stack, ordered by cost per unit of liquidity delivered in high-λ states:**
   1. mandate design (notice, smoothing, deferral rights);
   2. a Distribution & Collateral Reserve in HQLA, possibly funded with term debt (recourse debt ≤ 10% of NAV);
   3. committed contingent liquidity, arranged in benign regimes;
   4. a natural hedge: underweight assets with negative owner-beta;
   5. the dynamic beta overlay;
   6. 1–3-month trend following;
   7. a small, pre-committed convex sleeve;
   8. CDX protection;
   9. oil put spreads, if the mandate permits and owner-level coordination is agreed;
   10. joint-state hybrids, only after dealer quotes are tested against risk-adjusted P-measure probabilities.

   Equity-only tail hedges mis-target SG and GW, which are the likeliest liability stresses in 2027–29.

10. **Collateral binds first.**
    - March 2020: daily increases in initial margin (IM) were "notably smaller" than same-day variation margin (VM) calls, and some CCPs' IM rose more than 100% against the prior quarter [S-c].
    - UK LDI, 2022: 30-year gilts moved more than 270bp, and the FPC now requires resilience to ≥250bp [S].
    - The ledger specified here:
      - signs VM across all books;
      - recognises received collateral consistently;
      - uses one 30-day horizon;
      - treats the FSB's IM jump as a stress quantile, not a central target.

11. **Underwrite the opportunistic book at a Sharpe ratio of 0.3–0.5.**
    - Shrinking a backtested Sharpe of 1.0 over 8 years, at one consistent frequency, gives a posterior of ≈0.50 and a deflated Sharpe ratio (DSR) of ≈0.86, which fails a 0.95 gate [S-c, C3].
    - Rank strategies by λ-adjusted return.
    - Govern net Greeks at overlay level, so that short volatility in this book cannot silently offset the tail sleeve.

12. **Illustrative liquidity runway, to be replaced with ADIC data [I-calc C3].**
    - 12-month net liquidity need:
      - ≈0 when exits are open;
      - ≈US$14bn (7.8% of NAV) in today's drought at a 7.5% draw;
      - ≈US$21.5bn (12%) in a demand bust at mean draws;
      - ≈US$25.7bn (14.5%) at cap draws.
    - A DB→SG→SG path at cap draws consumes ≈US$63bn, against ≈US$41bn usable above the 8% IG+cash floor. That is ≈22 months of survival.
    - Adding a committed facility of 10% of NAV takes survival to ≈31 months.
    - The 24-month survival constraint binds, and it is cleared by committed liquidity, not by tail options.

13. **Governance: hedge fatigue is the main way tail programmes fail.**
    - Precedent: CalPERS unwound its tail hedges in 2019–20, shortly before the March 2020 crash. The LongTail payout is contested: US$150–175m per Institutional Investor, "several hundred million" per Bloomberg [S-c].
    - Make the convex budget an IC-owned, pre-committed line item, reviewed annually against a cumulative-carry tracker.
    - Pre-approve the monetisation playbook.

---

## 2. Verification ledger

### 2.1 Factual corrections (do not reuse the "As written" column)

| Stream | As written | Corrected (used here) |
|---|---|---|
| 02 | Kuwait 2020: automatic 10% FGF transfer "removed"; FGF ≈400% of GDP | Transfer **temporarily halted in deficit years / contingent on a surplus**. "FGF needs legislation" rests only on Bloomberg snippets. Fitch's "imminent depletion" is from Feb 2021. Use KIA ≈640% of GDP at end-2025 (IMF) [S]. |
| 02 | Ennis: alphas of −1.1% to −1.8% for 43 endowments | These are for **six size cohorts**. None of the 43 largest outperformed significantly; about one in four underperformed significantly (Ennis 2021, "Endowment Performance", *J. Investing*, DOI 10.3905/joi.2021.1.166, which replaces the stream's citation of the 2020 SSRN paper 3614875). The −1.87% (>$1bn endowments, 12 years to June 2020) belongs to a separate paper, probably Ennis (2021), "Failure of the Endowment Model", *JPM* 47(5):128–143, DOI 10.3905/jpm.2021.1.217 [I; unverified: the figure is not in that abstract, Institutional Investor (1 Apr 2021) attributes it only to an unnamed 2021 Ennis paper, and the full text was not accessed] [corrected 2026-10-18]. Costs of 1–2% are confirmed. |
| 02 | Harvard 2008–09: −27.3% to $26bn; taxable bonds; ~$500m swap cost | Cited source: *projected* −30%, "$24bn or so", $2.5bn of borrowings, swap losses "in the hundreds of millions", $11bn of commitments. Stream 09's ~$8bn (~22%) is [S*]. |
| 02 | CPP "reference portfolio" 13.2% | The **benchmark portfolios'** FY2026 return was 13.2%, against the Fund's 7.8%. |
| 02 | Stanford 70/30, 5.5%, 4–6% | Since Oct 2021: 80/20, 5.25% plus a 4% growth factor, with 4.25–6.25% boundaries that switch to fixed 4.75%/5.75% formulas. |
| 02 | NBIM 2024 inflow NOK 411bn; ADIA ranges "widened/narrowed" | NOK **409bn**. ADIA ranges **shifted**: PE 12–17→15–20%, financial alternatives 5–10→7–12%, real estate 5–10→2–7%. |
| 02 | NZ Super since 2010: 8.65% (Reference Portfolio) vs 10.09% (actual); Yale 2025 discount "up to 15%"; Temasek returns | Use the NZ Super 20-year figures: 9.68% vs 8.19% (Reference Portfolio). The value-add cut is unverified. "Up to 15%" is not in the Yale source. Temasek returns are [U]. |
| 02 | Singapore spends from expected returns | True only of the NIR half. The NII half spends **realised** income. |
| 03 | IMF footnote: the breakeven excludes SWF income | The footnote attaches to the *adjusted non-hydrocarbon primary balance*. Headline revenue, and possibly the 44.8 breakeven, may **include** fund income. |
| 03 | All PE statistics are "MSCI data" (Bain) | The 14% distributions/NAV is MSCI. The ~7-year holds and the 32k companies / $3.8trn are PitchBook/Preqin. |
| 03 | HMM degenerated on April 2020; 22-month low-price spell is "longest since 1988" | It degenerated on **March 2020** (log return −1.24). The spell is the longest **since mid-1990**; the 1986 price war is outside the sample. |
| 03 | SAMA→PIF US$40bn treated as a fiscal draw; "only 2008" had falling equities | It was a **reserve reallocation**. "Only 2008" holds only because 2015 US total return was +0.21% (the S&P price index fell 0.7%). |
| 09 | CalPERS LongTail "held to 31 Mar, several hundred million" | **Contested.** Institutional Investor: unwound between 1 Jan and 31 Mar, ≈US$150–175m. Bloomberg: "several hundred million". |
| 09 | Spot–vol β⁻ = −1.7, β⁺ = −1.0 | −1.70 is the slope *within* SPX < −2% days, with an intercept. The piecewise all-days fit is **−1.34 to −1.37 / −0.93 to −0.95**. |
| 09 | Sharpe example: posterior 0.42, DSR 0.86 | Mixed frequencies. Monthly-consistent: **SE 0.39, posterior 0.50, DSR 0.86**. |
| 09 | "Same-day VM dwarfed IM"; trend costs 0.6–0.8% for "1–3m"; 270bp gilt move cited to the FPC | VM exceeded *daily* IM increments ("notably smaller"). The cost is for **3-month** TSMOM only. The 270bp is in the **BoE FSR, Dec 2022**; the 250bp resilience standard is FPC, Mar 2023. |
| 09 | 2009 secondary discount 35%; forward 12m SPX return by VIX of 11/18/33% | 35% is an **annual average** [S*]. The omitted buckets (10.3% at VIX 15–20, 5.9% at 20–30) make the pattern non-monotone, and it rests on about two episodes. The AQR tail-fund critique is [U]. |

### 2.2 Design-layer corrections adopted

| ID | Problem flagged by verifier | Fix adopted (section) |
|---|---|---|
| D1 | 02: additive habit utility (h=0.8, γ=2) is undefined on ~75–78% of 20-year paths | Habit utility dropped. Owner stability becomes a reported frontier dimension. The master objective is Stream 11's SSG (§5.6). |
| D2 | 02: forced-sale probabilities are artifacts of the floor and report frequency only | Liquidity failure is defined against **external obligations**. The self-imposed floor triggers recourse costs (λ), not a constraint. Report frequency, E[loss], CVaR and a 10/15/20/25% floor sweep (§5.5). |
| D3 | 02: DWY over-extended | 3% α is a *lower bound*. DWY's α includes risk and illiquidity premia. The ~2% CE is not a calibration target. Re-solve a DWY-type model at ADIC parameters (DQ25). |
| D4 | 02/09: shadow prices have no estimator; units are mixed | Spot λ comes from recourse costs $c_k$ stated as present value per $ raised. The water value comes from SDDP cuts. Constraint shadow prices come from finite differences with common random numbers (CRN) and confidence intervals (§5.4). |
| D5 | 02: default constraints are infeasible at a 7.5% payout | Detect infeasibility and report the minimal relaxation, or an owner-endorsed decumulation path (§5.5). |
| D6 | 03: "near the cap" | Report mean draws by state conditional on $P^{BE}$ and ω. Cap draws are a stress assumption (§5.2). |
| D7, D8 | 03: hedge sized at 266m bbl; log mapping asserted | Size against simulated draw strips. Default to the linear-in-price mapping and publish both kink pairs (§5.1–5.3). |
| D9 | 03: circularity (the fiscal balance may contain fund transfers) | The owner state is the financing need **before** fund transfers; $P^{BE}$ is defined on the same basis (§5.1). |
| D10 | 03: "buy hybrids now" | Run a dealer RFQ and compare Q-implied with risk-adjusted P-measure joint-down probabilities. The priced structure is terminal-conditional, not a knock-in (§5.3). |
| D11 | 03: targets over-precise; an annual time-homogeneous Markov chain cannot fit the era-specific correlations | Targets become intervals with effective n. Monthly $Z_t$; era effects come through the shock-type mix (§5.1, §6). |
| D12 | 03: DCR mixes means with P99 values; override reserve is an expected loss | Stressed P10 inflows, a counterparty haircut on facilities and CSA netting. Override is folded into the chance constraint and a named stress (§5.5). |
| D13 | 03: SDDP convexity | Discretise $(S,Z)$ and the draw state into Markov nodes, or use SDDiP/Lagrangian cuts (§8). |
| D14, D19 | 09: spot–vol slope; IV surface flat beyond 3 months | $s^-$ = −1.35, $s^+$ = −0.94, plus a convexity term fitted to return buckets. SSVI surface with VIX/VIX3M/VIX6M/VIX1Y anchors (§5.3). |
| D15, D16 | 09: cost-per-crisis league table is fragile; J–R not tied to the dossier's own costs | Common-window and ex-COVID variants plus an in-model $c^\lambda$; explicit corner analysis (§5.6–5.7). |
| D17, D21, D22 | 09: IM target overreads the FSB; UMR scope; C2 mixes horizons | IM jump becomes a stress quantile. Both legal regimes are modelled. One 30-day horizon, with the max(lookback, model) form justified (§5.4–5.5). |
| D18 | 09: units and double counting ($\Pi_D$, $c_k$, ΔR at 100% vs φ, monetisation credit) | Signed VM; one φ convention; only incremental usable liquidity is credited; recourse frictions are not double counted in the objective (§5.4, §5.6). |
| D20, D23 | 09: Viterbi look-ahead; VIX−RV used as the ATM put cost | Decisions use filtered probabilities only. The 4.1-point VRP is presented as variance-swap-style (§5.3, §6). |
| D24 | 09: P(10%) maximised in the overlay objective | Reported, never maximised (§5.6). |

---

## 3. Decision register

| # | Design question | Positions in the dossiers | Recommendation |
|---|---|---|---|
| DQ1 | What does "10% target" mean? | 02: only a gross, pre-distribution reading is feasible | Gross, pre-distribution, nominal USD, geometric. Report the arithmetic figure alongside. Rolling 10 years, with 5 years secondary (Stream 11). A mandate-interpretation memo confirms. |
| DQ2 | Who owns the band? | 02: ADIC rule plus owner shock. 03: owner calls on fiscal need. 10: reduced-form oil clip | **Mandate switch** (A = ADIC rule, B = owner call, H = hybrid). Default **B** for scenarios and Tier 1. ADIC proposes an R12 rule to the owner, and the framework prices A−B. |
| DQ3 | Owner-draw model | 03: structural (B), Bayesian (C), rule overlay (D), IC summary (A) | **Phase 1:** reduced form with elicited priors, override and budget timing (the only form with verified outputs). **Phase 2:** structural fiscal model plus financing hierarchy, Bayesian-hierarchical, once draw history exists. |
| DQ4 | Fiscal mapping form | 03 text: log. 03 revenue equation: linear | **Linear in price × volume** by default, log as the alternative. Publish both kink pairs at every update. |
| DQ5 | Owner state variable | 03: headline fiscal balance | Pre-transfer financing need (adjusted balance concept). $P^{BE}$ on the same basis. |
| DQ6 | NAV basis | 02: options. 03: opening NAV | The band uses the mandate basis (default: opening reported NAV). Sustainability and liquidity are measured on economic NAV. Report the stale-NAV leak $D/W^{eco}$. |
| DQ7 | ADIC-proposed rule | 02: R12 family | R12, payout-matched (λ=0.8, κ=10%), compared against fixed %, POMV (k=2..6), Yale-literal and a two-key expected-return rule. Reject fixed real amounts and ratchets. |
| DQ8 | Owner welfare in the objective | 02: additive habit. 03: owner-weighted wealth | No habit utility. Stability is measured by frontier metrics. The owner-state weight applies only to the shortfall penalty. |
| DQ9 | Regime structure | 02: 2-state annual. 03: S×Z. 09: 4-state daily VIX HMM. 10: K=4 monthly | **Master $S_t$** (Stream 10). $Z_t$ is a coupled monthly chain. $V_t$ is a set of labels on simulated VIX. ET and PS are overlays. A 24-node $(S,Z)$ chain feeds SDDP. |
| DQ10 | Liquidity failure and constraints | 02: 25% floor. 03: DCR ≥ 1.25, 36-month drought test. 09: 1% over 36m. 10: 1% over 24m, forced sale ≤ 2%. 11: 1% joint over 5y | H1–H5 (§5.5): failure against external obligations, a forced-sale bound, stressed coverage ratios and a survival horizon. The self-imposed floor is a cost trigger, not a constraint. |
| DQ11 | Reserve | 02: 24-month reserve horizon. 06: debt-funded reserve | **Distribution & Collateral Reserve** = 12 months of planned draws + 30-day collateral need + stressed 12-month net calls. Separately, require ≥24 months of survival at cap draws counting haircut facilities. |
| DQ12 | Hedge valuation | 09: endogenous, plus Shapley. 03: buffer release (no risk adjustment) | Endogenous in simulation. Decompose with the water value $\lambda^w$, finite-difference η and Shapley values. Value buffer release at the α* of the asset it funds. |
| DQ13 | Stack composition | 09: dynamic beta + trend core, small convex sleeve. 03: natural hedge → oil spreads → hybrids → facilities | The ordered stack in exec item 9. Add each layer only if its robust marginal value is > 0. |
| DQ14 | Instrument screen | 09: index-history cost per crisis $ | In-model cost per λ-weighted payoff, $c^\lambda$. Show the index metric only as common-window and ex-COVID variants. |
| DQ15 | Oil liability hedge | 03: 20–40% of 266m bbl, struck at the kinks | 20–40% of the simulated first-year delta (≈100m bbl) at re-derived kinks. Stage purchases. No short calls in GW. Requires mandate approval and owner coordination. |
| DQ16 | Joint-state hybrids | 03: buy now | Defer until a dealer RFQ passes the Q-vs-P test (§5.3). |
| DQ17 | Spot–vol and surface | 09: −1.7/−1.0, sticky moneyness. 10: SVI | $s^-$ = −1.35, $s^+$ = −0.94, plus a convexity fit. SSVI with tenor anchors. |
| DQ18 | Opportunistic underwriting | 09 | Sharpe prior 0.3 (sd 0.25), shrinkage at one consistent frequency, DSR ≥ 0.95, λ-ranking, crowding and trend-reversal jumps, net-Greek governance. |
| DQ19 | Margin and collateral | 09 | Daily sub-steps in stress. Anti-procyclicality blend. SIMM, schedule IM or independent amount (IA) depending on legal status. Through-the-cycle HLBA floor. IM jump treated as a stress quantile. |
| DQ20 | Liquidity recognition | 09: ΔR at 100% vs φ = 0.7 | VM outflows at 100%. VM inflows: cash VM 100%, OTC collateral with reuse 70%, pledged 0%. Listed option MTM counts only in coverage ratios (0.85). |
| DQ21 | Shadow prices | 02: none from policy search. 09: single-period LP | $\lambda^{spot}$ from the merit order (later an LP). $\lambda^w$ from SDDP or least-squares Monte Carlo (LSM) regression. Constraint duals by finite differences with CIs. |
| DQ22 | Hedge budget governance | 09: open | IC-owned, pre-committed line with a floor of 0.15% of NAV a year. Annual review, fatigue tracker, pre-approved monetisation. |
| DQ23 | Time grid | Various | Monthly master. Daily overlay sub-steps. Quarterly PE flows and decisions. Annual draw rate set ex ante, paid quarterly. |
| DQ24 | Peer practice | 02 adopt/adapt/avoid table | **Adopt:** reference portfolio plus risk budget; CPP-style total-fund leverage gated by multi-horizon LCRs; an opportunity-cost test for existing holdings; a reserve account (Alaska ERA). **Adapt:** a two-key expected-return anchor (Norway; Singapore NIR); averaging and bands. **Avoid:** fixed amounts; asset-class quotas; smoothing for its own sake; reading the TPA "+1.3% p.a." as causal (the CFA Institute guide, Urwin & Hayman 2026, DOI 10.56227/26.1.20, flags confounders). |
| DQ25 | Role of DWY | 02: ≥3% α threshold; 2% CE as value | Qualitative use only. Re-solve a DWY-type model (lock-ups, secondary costs, payout floor) at ADIC parameters to value flexibility. |
| DQ26 | Owner override | 03: expected-loss reserve | Fold into the chance constraint (p^ov 2% > ε) plus a named stress (+3.5% of NAV in GW). |

---

## 4. Cluster architecture

### 4.1 Data flow

```
Stream 10 generator: S_t, factor VAR ──► Oil and shock-type layer: Z_t, P_t, q_t ──► owner pre-transfer need FN_y ──► Owner Draw Engine ──┐ D_y
        ├──► daily disaggregation: equity, VIX, curve, CDX, oil (V_t labels) ──► Overlay Engine (synthetic beta | defensive stack | opportunistic) ──┤ VM, IM, premia, payoffs
        └──► private book (Stream 04 RFT-TA): calls K, distributions, reported and economic NAV ──────────────────────────┤ K, PE distributions
                                                                                                                       ▼
                Collateral & Liquidity Ledger ──► recourse merit order (Stream 05 MCL curve) ──► λ^spot ; SDDP cuts / LSM ──► λ^w
                                                                                                                       ▼
   Tier-1 metrics H1–H5 · owner-beta, λ-beta · hedge decomposition · draw fan ──► optimiser (Stream 01 HDP / SDDP / policy simulator) and IC
```

### 4.2 Time grid

- **Monthly master grid,** following Stream 10.
- **Daily overlay sub-steps** (full option revaluation, VM/IM and monetisation checks) whenever the VIX label is V3 or above, a daily equity move exceeds 2% in absolute value, or a named stress is active.
  - Daily equity and VIX paths are generated for every path, so these windows can be detected.
  - Outside them, daily VM uses a delta–gamma–vega approximation.
- **Private cash flows and optimiser epochs quarterly** (Streams 01 and 04).
- **The owner's draw rate is set annually, ex ante,** from the budget-basis fiscal state at the start of the fiscal year.
  - It is paid in quarterly instalments.
  - The remaining instalments are reset mid-year if the realised financing need deviates by more than 2pp of GDP [I].
  - This avoids the timing artifact Stream 02 found: paying in full at the start of the year, before a same-year crash, makes wrong-way demand look harmless.

### 4.3 Regime hierarchy (resolves DQ9)

- **$S_t\in\{1..4\}$**, the macro-financial regime, is the master chain (Stream 10: hidden semi-Markov, negative-binomial dwell times). It drives every conditional moment.
- **$Z_t\in\{N,B,SG,DB,SS,GW\}$**, the oil/fiscal shock type, evolves monthly and is *coupled* to $S_t$ (§5.1).
- **$V_t\in\{V0..V4\}$** is *not* a third chain. It is a label on the simulated VIX level, with thresholds 14.3 / 18.4 / 24.4 / 45 derived from the HMM state ranges.
  - Stream 09's 4-state HMM becomes a calibration target: monthly persistence of 0.664 / 0.443 / 0.468 / 0.605 and durations of 41 / 19 / 20 / 35 days.
  - This keeps equity, VIX and margin internally consistent.
- **Overlays:**
  - ET: energy-transition drift on long-run oil, plus a declining hydrocarbon share $h$;
  - PS: peg or financial stress, a Bernoulli event.
- **SDDP uses a joint 24-node $(S,Z)$ chain.**

### 4.4 Notation (β is not overloaded)

| Symbol | Meaning |
|---|---|
| $t$, $y$ | Month index; fiscal year |
| $W_t$, $W^{rep}_t$ | Economic and reported NAV |
| $B_y$ | Distribution NAV basis |
| $d_y$, $D_y$ | Draw rate and amount |
| $P_t$, $b^M_t$, $q_t$ | Brent (US$/bbl); Murban basis (additive, US$/bbl); export-volume index |
| $h_y$, $P^{BE}$, $P^{ref}$ | Hydrocarbon revenue share of GDP; effective breakeven (pre-transfer basis); reference price for $h$ |
| $FN_y$ | Owner pre-transfer financing need, pp of GDP ($=-FB^{pre}_y$) |
| $c$, $b$, $\rho_d$ | Draw at $FN=0$; draw slope; draw smoothing |
| $\lambda^{spot}_t$, $\lambda^w_t$ | Recourse dual; water value of liquidity |
| $\eta_k$ | Shadow price of Tier-1 constraint $k$ |
| $s^-$, $s^+$ | Spot–vol slopes |
| $\delta^{rep}$, $\delta^{eco}$ | Secondary discount to reported and to economic NAV |
| $\varphi$ | Liquidity-recognition factors |
| $\beta^{own}_j$, $\beta^\lambda_j$ | Owner-beta and liquidity-beta of asset or action $j$ |

---

## 5. Model formulations

### 5.1 Oil, shock type and the owner's fiscal state

**(a) Shock-type chain.**
- *Annual prior,* from Stream 03 [I]. Rows give the current state.

  | From \ To | N | B | SG | DB | SS | GW |
  |---|---|---|---|---|---|---|
  | N | .62 | .15 | .10 | .05 | .04 | .04 |
  | B | .40 | .40 | .05 | .06 | .07 | .02 |
  | SG | .38 | .12 | .42 | .04 | .02 | .02 |
  | DB | .35 | .30 | .20 | .10 | .03 | .02 |
  | SS | .30 | .05 | .10 | .35 | .15 | .05 |
  | GW | .30 | .05 | .35 | .05 | .05 | .20 |

- *Monthly generator.* $P^Z_m=I+(P^Z_a-I)/12$. This preserves expected durations.
- *Coupling to the master regime:*
  $$P(Z_{t+1}=j\mid Z_t=i,S_{t+1}=s)=\frac{P^Z_{m,ij}\,\kappa_{sj}}{\sum_l P^Z_{m,il}\,\kappa_{sl}}.$$
  Calibrate the compatibility weights $\kappa_{sj}$ so that P(S=crisis | DB) ≥ 0.8 and P(S=crisis | SG) ≈ 0.15.
- *Stationary distribution.* The prior's stationary shares (N 49%, DB 7%) miss the targets. Re-estimate by constrained MLE on labelled history plus elicitation, with stationary shares inside these intervals:
  - N 0.55–0.65;
  - B 0.13–0.22;
  - SG 0.10–0.17;
  - SS 0.03–0.07;
  - DB 0.02–0.06;
  - GW elicited, with no historical analogue.
- *Starting state.* Initialise $Z_0$ = GW with probability ≥ 0.7, replaced by the nowcaster's posterior when available [I].
- *Overlays:*
  - ET: $\mu_\xi$ = −2% a year real from 2030 in the high-transition scenario;
  - PS: 1% a year in N/B and 5% a year in GW/SG/DB [I].

**(b) Oil price** (monthly; reduced form compatible with Schwartz–Smith):
$$\ln P_{t+1}=\ln P_t+\kappa_m(\ln P^{LR}_t-\ln P_t)+\tfrac{\mu_{Z}}{12}+\tfrac{\sigma_{Z}}{\sqrt{12}}\,\varepsilon^o_{t+1}+J_{t+1}\mathbb 1\{Z=GW\},\qquad \varepsilon^o=\rho_Z\tilde e^{eq}+\sqrt{1-\rho_Z^2}\,e^\perp .$$
- $\kappa_m=1-0.6^{1/12}$, equivalent to an annual κ of 0.40.
- $P^{LR}$ = US$70 nominal, plus the ET drift.
- Annual $(\mu,\sigma)_Z$ and the oil–equity correlation $\rho_Z$ by state:

  | State | (μ, σ) | $\rho_Z$ |
  |---|---|---|
  | N | (0, .20) | 0 |
  | B | (+.20, .20) | .2 |
  | SG | (−.35, .20) | .1 |
  | DB | (−.45, .25) | .6 |
  | SS | (+.30, .25) | −.4 |
  | GW | (+.10, .30) | −.5 |

- $J$ is a Bernoulli(0.25/12) jump of ±0.26 in log terms.
- $\tilde e^{eq}$ is Stream 10's standardised equity-factor innovation, so the equity marginal is preserved.
- $P^{eff}=P+b^M$, with $b^M\sim N(0,2^2)$ US$/bbl [I/U].
- *Checks* [I-MC, annual version, excluding jumps]: the dossier's P10/P50/P90 Brent was US$60/90/137 one year ahead from GW at US$126. The joint model must land inside the era-correlation intervals in §6.

**(c) Owner fiscal state on a pre-transfer basis** (fixes D9):
$$FB^{pre}_y=100\,h_y\,\frac{\bar P^{eff}_y\,\bar q_y-P^{BE}_y}{P^{ref}}+w_{Z_y}+\epsilon_y\quad\text{(linear; default)},$$
$$FB^{pre}_y=100\,h_y\ln\!\big(\bar P^{eff}_y\bar q_y/P^{BE}_y\big)+w_{Z_y}+\epsilon_y\quad\text{(log; alternative)},$$
$$FN_y=-FB^{pre}_y .$$

- **Defaults:**
  - $h_y$: 11.3% (2026), falling linearly to 9.1% (2030) [S IMF]. Afterwards flat, or −0.4pp a year under ET.
  - $P^{ref}$ = US$62.5 (range 60–65) [I].
  - $P^{BE}$: lognormal, median US$55, 90% interval US$45–70. The IMF consolidated figure of 44.8 is the lower anchor.
  - $w_Z$ (pp of GDP): N and B 0; SG −0.5; SS −0.5; DB −1.5.
  - $w_{GW}\sim N(-5,2^2)$, truncated to [−9, −1].
  - $\sigma_\epsilon$ = 1pp.
  - $q$: EIA path. The 2026 average is 0.95 of 2025; the 2Q26 trough was ≈0.75 of 4Q25 [S].
- **The war wedge is mostly non-volume.** Even with explicit 2026 volumes, the linear map at ≈US$96 Brent gives +8.4pp, against the IMF's projected +1.5pp. The wedge of ≈−6.9pp is therefore mostly non-hydrocarbon, but it rests on one projected year.
- **$P^{BE}$ and $w_{GW}$ are not separately identified from 2026.** At $P^{BE}$ = 55 the wedge is ≈−5pp. Elicit them jointly.
- **Kinks** ($c$ = 7.5%, $b$ = 0.625, $h$ = 11.3%, $P^{BE}$ = 44.8, $w=0$) [I-calc C3]:
  - linear: floor at US$66.9, cap at US$22.7 (66.0–67.8 and 23.6–21.8 for $P^{ref}$ 60–65);
  - log: US$63.8 and US$31.4.
  - Re-derive and publish both pairs whenever $P^{BE}$, $h$ or $b$ updates.

### 5.2 Distribution Demand Engine

**(a) Owner reduced form** (Phase 1 default):
$$d^{tgt}_y=\Pi_{[d_{lo},d_{hi}]}\big(c+b\,FN^{bud}_y\big),\qquad d_y=\Pi_{[d_{lo},d_{hi}]}\big(\rho_d\,d_{y-1}+(1-\rho_d)\,d^{tgt}_y\big),$$
- **Override:** with probability $p^{ov}(Z_y,PS_y)$, set $d_y\leftarrow d_{hi}+u_y$ with $u_y\sim U(2\%,5\%)$.
- **Amount:** $D_y=d_yB_y$, paid in four instalments.
- **Defaults** [I; client band]:
  - $d_{lo}$ = 5% and $d_{hi}$ = 10%;
  - $c$ = 7.5% and $b$ = 0.625 %NAV per pp of GDP, so the draw is at the floor when FN ≤ −4 and at the cap when FN ≥ +4;
  - $\rho_d$ = 0.5;
  - $p^{ov}$ = 0.25% a year in N/B/SS, 1% in SG/DB, 2% in GW or PS.
- **Smooth clip for gradient-based search:** $\Pi_\tau(x)=d_{lo}+\tau\ln\frac{1+e^{(x-d_{lo})/\tau}}{1+e^{(x-d_{hi})/\tau}}$ with τ = 0.1%.
- **Report mean draws by state conditional on $P^{BE}$ and ω,** using the verified grid as the starting point:

  | $P^{BE}$ | Mean draw | Mean in DB / SG | P(≥3 consecutive years ≥ 9.5%) over 10y |
  |---|---|---|---|
  | US$44.8 | 6.0% | 6.9% / 6.8% | 0.8–1.4% |
  | US$55 | 6.6–6.7% | 7.6% / 7.6% | 3.6–5.8% |
  | US$65 | 7.2–7.3% | 8.1–8.2% | 10.2–15.3% |

  Ranges span $b$ = 0.625–1.0 [I-MC rep.; override, PS, ET, declining $h$ and jumps excluded].

**(b) Structural form** (Phase 2):
$$G_y=\max(0,FN_y)\,GDP_y,\qquad R_y=\max\big(0,\;G_y-Cash^{own}_y-DebtCap_y(1-\delta_{PS}\mathbb 1\{PS\})\big),\qquad d^{tgt}_y=\Pi\big(d_{lo}+\omega_yR_y/B_y\big).$$
- Estimate $(b,\rho_d,\omega,P^{BE})$ hierarchically, partially pooled with four peer episodes: Saudi Arabia 2015–16, Kuwait 2020, Norway 2016 and Alaska FY15–17.
- Update with a particle filter after each realised draw and fiscal release.

**(c) Mandate switch.**
- **Mode B (owner call):** default for scenarios and Tier 1.
- **Mode A (ADIC rule):** $d_y=\Pi(f_\theta(\cdot)+u_y)$. θ is chosen by policy search and $u_y$ is bounded discretion. Owner shocks enter only via override.
- **Mode H (hybrid):** $d_y=\max(f_\theta,d^{own}_y)$, or the documented combination.
- **Value of mandate design** = $J^*_A-J^*_B$ (objective and Tier-1 metrics), with CRN.
- **Shadow prices of the floor and cap:** re-optimise at $d_{lo}\pm50$bp and $d_{hi}\pm50$bp, with bootstrap CIs.

**(d) ADIC rule library** (Mode A and proposals to the owner).
- **Yale-literal:** $D_y=[\lambda D_{y-1}+(1-\lambda)r^*W_{y-1}](1+\pi_{y-1})$. The band is measured on the start-of-prior-year value.
- **POMV:** $D_y=r^*\tfrac15\sum_{k=2}^{6}W_{y-k}$.
- **Two-key expected return:** $D_y=\theta\,\hat r^{real}_{IC}W_y$ plus inflation, with θ ∈ {0.5, 0.75, 1}.
- **Surplus barrier:** $D_y=\min(5\%W_y+\kappa(W_y-B^{path}_y)^+,10\%W_y)$.
- **R12, linearised LQ form:**
  $$D_y=\Pi_{[5\%B_y,10\%B_y]}\big(\lambda D_{y-1}(1+\pi_{y-1})+(1-\lambda)r^*_yW_y\big),\qquad r^*_y=\Pi_{[5,10]}\big(r_0+\kappa(F_y-1)\big),\qquad F_y=\frac{W^{eco}_y}{W_0\,CPI_y\,e^{g^*y}}$$
  - λ = 0.8;
  - $r_0$ payout-matched, starting at 6.5%;
  - κ = 10%;
  - g* = 0.
- **Rejected:**
  - fixed real amounts, which deplete below 5% of starting NAV in 31–52% of 20-year paths (70% in the low-return case) [I-MC rep.];
  - ratchets, which Dybvig shows are infeasible at a 5–10% payout.
- **Compare rules at equal average payout,** across floor sweeps, on the four-dimension frontier:
  - cumulative real distributions;
  - real NAV tail;
  - stability (SD of real distribution growth, and P(real cut > 10%));
  - E[sale loss] and P(obligation failure).
- **Payout-matched evidence:** at a 25% floor and a 7.5% payout, the forced-sale probability is 10.3% for payout-matched R12 against 4.8% for fixed % [I-MC rep.].

### 5.3 Overlay Engine

**(a) Daily paths.**
- Monthly factor draws come from Stream 10.
- Daily patterns of $(r,\Delta VIX,\Delta skew,\Delta CDX,\Delta y,\Delta oil)$ come from a regime-conditioned block bootstrap: historical months with the same $S$ and $V$ label and the nearest monthly return, rescaled.
- Named stresses are overlaid:
  - a 1987-type gap;
  - the 2020 crash;
  - the 2022 grind with positive stock–bond correlation;
  - a +250bp gilt-type rate move;
  - an oil collapse;
  - a trend reversal (Mar–May 2009);
  - a short-volatility unwind (5 Feb 2018).

**(b) VIX dynamics** (corrected):
$$\Delta VIX_d=\kappa_V(\bar V_{S}-VIX_{d-1})\Delta+s^-\min(100r_d,0)+s^+\max(100r_d,0)+s^q\min(100r_d,0)^2+\eta_V\sqrt\Delta\,z_d .$$
- $s^-$ = −1.35 and $s^+$ = −0.94 [S-c].
- $s^q$ starts at 0. Fit it jointly with $s^-$ to the bucket targets in §6.
- $\bar V_S$ is the regime-conditional VIX mean from Stream 10's factor model, where log VIX is one of the factors. The V-state means 12.5 / 16.3 / 21.1 / 30.7 bracket the plausible range.
- Calibrate $\kappa_V$ and $\eta_V$ to the HMM persistence and duration targets.

**(c) Implied-volatility surface: SSVI.**
$$w(k,\tau)=\tfrac{\theta_\tau}{2}\Big[1+\rho_V\phi(\theta_\tau)k+\sqrt{(\phi(\theta_\tau)k+\rho_V)^2+1-\rho_V^2}\Big],\qquad \phi(\theta)=\eta\,\theta^{-\gamma}(1+\theta)^{\gamma-1}$$
$$\theta_\tau=\tau\,(c_{ATM}\,VIX_\tau/100)^2 .$$
- $VIX_\tau$ is interpolated in total variance across VIX (30 days), VIX3M, VIX6M and VIX1Y. This fixes the flat-tenor problem (D19).
- $c_{ATM}$ = 0.90, to be calibrated.
- Term ratios by VIX bucket follow the medians 1.18 / 1.13 / 1.08 / 1.01 / 0.90.
- Calibrate $\rho_V,\eta,\gamma$ by V-label to 25-delta risk reversals and butterflies. SKEW is a cross-check.
- **No-arbitrage:**
  - $\theta_\tau$ must be non-decreasing in τ;
  - the sufficient condition η(1+|ρ|) ≤ 2 with 0 < γ ≤ ½ follows Gatheral–Jacquier 2014 (verify the constants at implementation);
  - numerical butterfly and calendar checks are a rubric gate in any case.
- **Pricing:** Black-76/BSM on this Q-surface, evaluated along P-measure paths.

**(d) Synthetic beta.**
$$N^\beta_{a,t}=(\beta^*_{a,t}-\hat\beta^{true}_{a,t})W_t/\beta^{inst}_a,\qquad P\&L=N^\beta(r_a-f_a\Delta),\qquad VM=P\&L,\qquad IM=m_a(V)\,\lvert N^\beta\rvert .$$
- $m_a(V)=\max(m^{floor},2.326\,\sigma\sqrt{5/252})$: ≈4% in V1 and ≈10% in V3.
- σ blends 75% EWMA with 25% stressed volatility (anti-procyclicality).
- The target is **true** exposure, using de-smoothed private betas from Stream 04 [I].
- Futures financing is SOFR + 30–140bp; the June 2026 roll was +81bp over 3m SOFR [Stream 06; the roll figure is via a search excerpt].

**(e) Defensive stack: the tail book.**
- *Value:* $V^H_t=\sum_jN_j\,\mathrm{Price}_j(\cdot,\sigma_t(k_j,\tau_j))$.
- *Purchases:* $N^{new}_i=h\,W\,w_i/(12V_{i,0})$, on a 3/6/12-month ladder weighted 25/50/25.
- *Budget:*
  - $h^{min}$ = 0.15% of NAV a year, pre-committed;
  - scale up toward 0.5% only when VRP is low, fragility is rising and SKEW is not extreme, *and* the robust marginal value is > 0.
- *Strikes:*
  - put spreads at 90/72% of forward while SKEW is rich (168.6 now, against a mean of 123.3);
  - outright deep-OTM puts only when the wing is near its long-run level.
- *Monetisation triggers:* Δ ≤ −0.5, or value ≥ 3× premium, or (label ≥ V3 and VIX ≥ 35).
  - Sell f = 50%.
  - Reinvest 40% of proceeds longer-dated and lower-struck.
- *LSM refinement:* monetise if
  $$V_{j,t}(1-ba_V)+\lambda^w_t\,\Delta L^{use}_{j,t}\ \ge\ \hat E_t[\text{continuation}],$$
  - $\Delta L^{use}=V(1-ba)$ for listed options;
  - $\Delta L^{use}=V(1-ba)-\varphi^{in}R^{c}_j$ for OTC options under a CSA, which counts only incremental liquidity.
  - Tune thresholds by policy search, with DSR and PBO guards on held-out regimes.
- *Oil put spreads* (only if permitted):
  - strikes at the published kinks;
  - 1–2-year strips;
  - notional ≤ 20–40% of the simulated first-year draw delta (≈20–40m bbl);
  - staged as oil volatility normalises (76.8% realised since 1 Mar 2026);
  - no short calls in GW.
- *Hybrids:* buy only if $P^Q(\text{joint down})<(1-m)\,P^{P,adj}(\text{joint down}\mid Z\text{ posterior})$, with a margin m = 25% [I] and an explicit risk-premium adjustment.
- *CDX:* P&L $=-N\cdot RPV01\cdot\Delta s-$ carry. Use cleared IM; the schedule fallback is 2/5/10% by duration.

**(f) Opportunistic book.**
- **Return model:**
  $$r^O_t=\ell_t[\mu^O_V\Delta+\sigma^O_V\sqrt\Delta\,\xi_t]+J^O_t,\qquad \ell_t=\min\big(\ell^{max},v_t/\hat\sigma^O_t\big)\Big(1-\tfrac{DD_t}{DD^{max}}\Big)^+ .$$
  - ξ is skew-t by strategy family.
  - $\mu^O_V=SR^{post}_V\sigma^O_V$.
- **Posterior Sharpe:** $SR^{post}=SR_0+w(\widehat{SR}-SR_0)$, with $w=\tau^2/(\tau^2+SE^2)$.
  - SE is computed at the sampling frequency of the data: $SE_{per}=\sqrt{(1-\hat\gamma_3SR+\frac{\hat\gamma_4-1}{4}SR^2)/(T-1)}$, then annualised.
  - Prior: $SR_0$ = 0.3, τ = 0.25.
- **Add a strategy only if DSR ≥ 0.95.**
  - Worked example: monthly data, backtest Sharpe 1.0 over 8 years, skew −0.5, kurtosis 5, 50 trials, cross-trial dispersion 0.25.
  - Result: SE 0.39, posterior 0.50, DSR 0.86, so the strategy fails the gate [S-c, C3].
- **Family Sharpe templates** by V0/V1/V2/V3 [I placeholders; calibrate to ADIC P&L]:

  | Family | V0 | V1 | V2 | V3 |
  |---|---|---|---|---|
  | Trend | 0.3 | 0.3 | 0.4 | 0.6 |
  | Carry/RV | 0.6 | 0.5 | 0.2 | −1.0 |
  | Short-vol | 0.9 | 0.6 | 0.0 | −2.0 |

- **Jumps:**
  - crowding: intensity 0.5 a year in V3+, size −1.5 monthly σ;
  - trend-reversal jump on V3→V2 transitions, calibrated to Mar–May 2009.
- **Ranking score:** $E[(1+\lambda^w)r^O]/\sigma^O$.
- **Limits:**
  - volatility budget 1.0–1.5% of NAV, with $DD^{max}$ = 2× budget;
  - net overlay vega in V3 scenarios must stay ≥ a floor share of the tail sleeve's vega.
- **Hedge-fund sleeve:** the reported leveraged programme of up to US$15bn [U: press report via Jawlah citing Bloomberg; not verified] takes a 50–100% liquidity haircut, depending on gates.

**(g) Counterparty.**
- Exposure: $X_c=\max(0,V_c-R_c)$.
- Default intensity rises with the V-label, and for GCC-linked dealers in GW/PS (wrong-way risk). LGD 60% [I].
- Limits: ≤ 0.5% of NAV per dealer, ≥ 5 dealers, CSA mandatory.
- Under the US rule the sovereign-entity exclusion covers only central governments and their agencies, departments, ministries and central banks. A government guarantee alone does not qualify, and an independent amount can be required by contract. **Model both IM regimes.**

### 5.4 Collateral and liquidity ledger, recourse and λ

**(a) Ledger.** Stepped daily in stress windows and monthly otherwise.
$$L_{t+1}=L_t+PE^{dist}_t-K_t-D_t-DS_t+Debt^{new}_t+\sum_p\varphi^{in}_p VM^{in}_{p,t}-\sum_pVM^{out}_{p,t}-\Delta IM^{post}_t-Prem_t-Fin_t+Mon_t+Sales^{liq}_t+\sum_ky_{k,t}$$
- $\varphi^{in}$ = 1 for cash VM (futures and cleared), 0.7 for OTC collateral with reuse rights, and 0 for pledged collateral.
- Posted IM is encumbered. It is excluded from $L$ and from the 8% IG+cash test.
- Breaching $L^{min}$ (8% IG+cash plus the Distribution & Collateral Reserve) triggers recourse. It is not a failure.

**(b) Recourse merit order.** All costs are present value per $ raised [I; inputs from Streams 05 and 06].

| Source $k$ | Lag | Capacity | $c_k$ formula | Illustrative normal / stress |
|---|---|---|---|---|
| Cash above $L^{min}$ | 0 | $L-L^{min}$ | 0 | 0 / 0 |
| UST repo | T+1 | (1−h_r) × UST | spread × tenor | ≈0–0.2% / 0.3% |
| Committed revolver or repo line | ~3 days | undrawn × (1 − $h^{cpty}$) | (spread + fees) × E[τ] | ≈0.5–1.5% / 1–3% [I] |
| Committed NAV facility | days–weeks | LTV cap × eligible NAV × (1 − $h^{cpty}$) | (spread + OID) × E[τ] + covenant option | ≈4–9% / higher (SOFR+300–500bp + 1–2% OID; Streams 05/06) |
| Sell liquid assets | T+2 | holdings | impact only (exposure effect is endogenous) | 0.1–0.3% / 0.5–2% |
| Cut opportunistic book | days | IM released + cash | unwind cost | 0.2% / 1% |
| Term debt | 2–6 weeks | market access | (spread over reinvestment) × duration | UST+55–99bp / closed or wide |
| Slow commitments | 1–4 quarters | avoided calls | endogenous (α* forgone) | — |
| LP-led secondary | 3–6 months | depth by $V$ | $(W^{eco}-P^{sec})/P^{sec}$, with $P^{sec}=W^{rep}(1-\delta^{rep}_V)$ | ≈9% / ≈20% economic (headline 64% at 61% of NAV) |
| Defer draw (if permitted) | — | mandate | $\Pi_D$, owner/IC-set | else infeasible |

- **Spot price.** $\lambda^{spot}_t$ is the cost of the marginal source used, and zero with no deficit.
- **Phase 2.** Replace the merit order with a per-path multi-period LP with lags and a terminal water value; its duals give λ.
- **Secondary-sale cost is measured against economic NAV.** H2 2008 high bids were 61% of NAV but 83.5% after adjusting for public-market moves [S, Stream 05]. Much of the headline discount was stale marks.

**(c) Water value.** $\lambda^w_t(s,L)=-\partial\hat E\big[\sum_{\tau>t}\delta_\tau\sum_kc_ky_{k,\tau}\mid L_t,S_t,Z_t\big]/\partial L_t$.
- Source: SDDP cut slopes (Stream 01, L2), or an LSM regression in the simulator.
- Hedge valuation, monetisation and action valuation all use $\lambda^w$. A payoff that arrives before the deficit still has value.
- $\lambda^{spot}$ is reported as the "cash-crunch price".

**(d) Margin.**
- **Cleared IM:** EWMA with the anti-procyclicality blend.
- **Uncleared IM:**
  - if UMR applies: SIMM (licensed), with schedule IM $(0.4+0.6NGR)\times\sum$ gross × schedule % as the fallback;
  - if the exclusion applies: the IA only.
- **Historical look-back (HLBA):** $HLBA^{TTC}_t=\max(HLBA_t,\ P95$ of 30-day net collateral flows over the 2008, 2020, 2022 and 2025 windows). The floor matters because April 2025 drops out of the 24-month window in April 2027.
- **FSB stress quantile:** at V3 entries, the quarterly IM increase for the most procyclical products should reach ≥ +100% at the P95 level.

### 5.5 Tier-1 constraints and coverage metrics contributed by this cluster

**H1 Obligation failure** (robust chance constraint):
$$\sup_{Q\in\mathcal Q}P_Q\big(\exists t\le60m:\ Oblig_t>Src^{adm}_t\big)\le\varepsilon_H=1\%\ \text{(5-year joint)},$$
plus a 12-month planned-payout reliability ≥ 97.5% (Stream 11).
- $\mathcal Q$ = model ensemble × a KL ball with η = 0.10 (Stream 10).
- Obligations, within their settlement windows:
  - draw instalments on schedule;
  - capital calls (≈10 business days);
  - VM and IM (T+1);
  - debt service.
- Admissible sources:
  - unencumbered liquid assets after V-haircuts;
  - facility headroom × (1 − $h^{cpty}$);
  - monetisable hedges: listed at φ = 0.85; OTC net of collateral returned.

**H2 Forced sale.**
- $\sup_Q P_Q$(secondary sale under duress at $\delta^{rep}$ > 20% within 5 years) ≤ 1% (Stream 11). Also report it at 2% (Stream 10).
- Report E[loss], CVaR₉₅[loss], P(any sale) and a 10/15/20/25% floor sweep.

**H3a 30-day collateral coverage** (checked daily; one horizon):
$$HQLA^{unenc,h}_t+0.85\,V^{listed}_t\ \ge\ \max\big(HLBA^{TTC}_t,\ VM^{out,99}_{30d}+\Delta IM^{stress}_{30d}\big)+D_{30d}+K^{stress}_{30d}-PE^{P10}_{30d}+DS_{30d}.$$
The max is justified: both terms estimate the same net collateral outflow, one historically and one with a model. Non-derivative flows are additive.

**H3b 12-month stressed DCR** for Z ∈ {DB, GW, SG+PS}:
$$DCR^{(Z)}=\frac{\sum_i(1-\eta^{(Z)}_i)L_i+(1-h^{cpty}_Z)F^{undrawn}+Q^{(Z)}_{10\%}[PE^{dist}_{12m}]+Q^{(Z)}_{10\%}[\text{net usable hedge payoff}]}{D^{cap}_{12m}+Q^{(Z)}_{90\%}[K_{12m}]+CN^{(Z)}_{12m}+DS_{12m}+O^{(Z)}}\ \ge1.0\ \text{hard};\ \ge1.25\ \text{green}.$$
- Haircuts $\eta_i$:
  - cash and T-bills 0;
  - DM government bonds 3%;
  - IG credit 10%;
  - listed equity 20% (30% in DB);
  - HY and EM 35%;
  - hedge funds 50–100%.
- $h^{cpty}$ = 20% in DB/GW/PS and 10% otherwise.
- Hedge payoffs are netted against margin within the same CSA.
- $O^{(GW)}$ = 3.5% of NAV (override stress) [I].

**H3c Survival horizon.**
- Named path: DB→SG→SG with exits shut, cap draws and an override in year 2.
- Requirement: ≥ 24 months hard, 36 months target.

**H4** IG + cash ≥ 8% of NAV, excluding encumbered IM.

**H5 Structural limits** (Streams 06 and 11):
- recourse debt ≤ 10% of adjusted NAV;
- economic leverage ≤ 1.3×;
- overlay gross notional ≤ $G^{max}$;
- dealer limits as in §5.3(g).

**Infeasibility (D5).** If no policy satisfies H1–H5 at the mandated draw, report the minimal relaxation: the smallest ε, the smallest draw reduction, or an owner-endorsed decumulation path. Shadow prices of the binding constraints are reported with CIs.

### 5.6 Objective interface and hedge valuation

**Master objective.** Stream 11's "safety-filtered, shortfall-aware growth" (SSG): CRRA utility of real NAV, minus a shortfall penalty against ln 1.10. P(10%) is **reported, never maximised**. Maximising it buys digital-like payoffs, which is target-chasing through the overlay (Browne).

This cluster adds:

1. **Constraints H1–H5.**
2. **Only costs not already in NAV.** Sale discounts and frictions already reduce simulated wealth, so adding $\sum c_ky_k$ again would double count; this fixes Stream 09's §6.6. The additions are:
   - signalling and irreversibility costs (Stream 05);
   - if deferral is permitted, $\lambda_{sh}E[\sum_y m^{own}_y(D_y-Paid_y)^+]$, where
     - $m^{own}_y=1+\kappa_{own}(FB^*-FB^{pre}_y)^+/\sigma_{FB}$;
     - $FB^*$ = +2pp;
     - $\kappa_{own}$ = 1 (sensitivity 0–2).
3. **Owner-stability metrics on the Pareto frontier,** for Mode A.

**Hedge decomposition ("what we are paying for")** for overlay component $j$:
$$Carry_j=\frac{E^P[X_j]}{1+r}-P_j,\qquad LV_j=E^P\Big[\sum_t\delta_t\lambda^w_t\Delta L^{use}_{j,t}\Big],\qquad EV_j=\sum_k\eta_k\,\Delta slack_k(j).$$
- $\eta_k$ comes from finite differences with CRN and a bootstrap CI. It is measured against whichever re-specified Tier-1 floor Cluster 1 adopts. The deck's "≤5% breach of 7%" gate is infeasible (Streams 10/11).
- Rebalancing value is the residual of a with/without-reinvestment ablation. Do not assume the "+15pp post-crisis" return: the evidence is non-monotone.
- Totals are Shapley values over overlay components, with CRN.
- **Screen:** $c^\lambda_j=-Carry_j/E[\sum_t\delta_t\lambda^w_tX_{j,t}]$.

**Per asset or action $j$** (feeds Cluster 2):
- $\beta^{own}_j=\mathrm{Cov}(r_j,d)/\mathrm{Var}(d)$;
- $\beta^\lambda_j=\mathrm{Cov}(r_j,\lambda^w)/\mathrm{Var}(\lambda^w)$.

### 5.7 Illustrative runway and buffer economics [I-calc C3; replace with ADIC data]

**Assumptions:**
- NAV US$177bn, 40% liquid;
- net PE flows from Stream 04's toy programme: +US$11bn (exits open), ≈0 (drought), −US$4.5bn (crisis);
- overlay margin placeholders from Stream 03.

| 12-month state | Draw | Net PE | Margin | Net need, US$bn (% NAV) |
|---|---|---|---|---|
| Normal, exits open | 6.0% (10.6) | +11.0 | 0 | −0.4 (−0.2%) |
| Drought (today) | 7.5% (13.3) | ≈0 | 0.5 | 13.8 (7.8%) |
| DB, mean draw ($P^{BE}$ 55) | 7.6% (13.5) | −4.5 | 3.5 | 21.5 (12.1%) |
| DB, cap draw (stress) | 10% (17.7) | −4.5 | 3.5 | 25.7 (14.5%) |
| DB→SG→SG, 3 years | cap / mean | −4.5, 0, 0 | 3.5, 1, 1 | 63.1 / 50.4 |

**Runway at cap draws:**

| Step | US$bn |
|---|---|
| Liquid assets | 70.8 |
| After a blended DB haircut of ≈22% | 55.2 |
| Less the 8% IG+cash floor = usable | 41.1 |

- Usable liquidity alone gives **≈22 months** of survival on the DB→SG→SG path.
- Adding a 10%-of-NAV committed facility recognised at 80% gives **≈31 months**.
- By comparison, a 0.25% NAV-a-year convex sleeve paying 1.25% of NAV in the crisis (Stream 09's worked example) adds ≈1–1.4 months. At VXTH-like efficiency it adds ≈2.3–3.1 months.
- Stream 06 costs a 10%-of-NAV term-debt reserve at ≈10bp a year.
- **Committed liquidity buys roughly an order of magnitude more runway per unit of carry.** But it adds fixed claims and counterparty wrong-way risk, so the debt and payout policies must be co-optimised.

**Jeanne–Rancière corners.** Optimal buffer $\rho^*\approx\lambda+\gamma-(1-p^{-1/\sigma})$, with $p=1+\delta/(\pi(1-\delta-\pi))$, π = 10% and λ+γ = 15% of NAV, consistent with the DB need above. σ is the curvature of the IC's crisis penalty.

| Insurance (δ = annual carry per $ of crisis liquidity) | σ = 2 | σ = 5 | σ = 10 |
|---|---|---|---|
| HQLA, δ = 1.5% (debt-funded or displacing bonds) | 7.5% | 11.9% | 13.4% |
| HQLA, δ = 5% (displacing equities) | corner | 6.2% | 10.5% |
| VIX calls, common window (0.07) / own sample (0.09) | corner | 3.5% / 1.1% | 9.1% / 7.8% |
| PPUT puts (0.28–0.29); CLL (0.59); CLLZ (0.94); PPUT/VXTH ex-COVID (0.44/0.42) | corner | corner | corner |

This is a one-shot model for IC intuition only. Sizing comes from the multi-period simulation.

### 5.8 Parameter registry (seed values; every entry stored with a vintage tag)

| Parameter | Default (range) | Source | Confidence |
|---|---|---|---|
| Band $d_{lo}$ / $d_{hi}$ | 5% / 10% | client | high |
| $c$; $b$; $\rho_d$ | 7.5% (6.5–8.5); 0.625 (0.4–1.0); 0.5 (0.3–0.7) | [I], to be elicited | low |
| $P^{BE}$ | LN median 55 (45–70) | IMF 44.8 anchor [S]; [I] | low |
| $h_y$; $P^{ref}$ | 11.3%→9.1% (2026–30); 62.5 (60–65) | IMF [S]; [I] | medium; low |
| $w_Z$; $\sigma_\epsilon$ | see §5.1; 1pp | [I]; IMF projection | low |
| $p^{ov}$; $u$ | 0.25/1/2%; U(2,5%) | [I] | low |
| Oil κ, $P^{LR}$, $(\mu,\sigma,\rho)_Z$, jumps | §5.1 | [I] | low–medium |
| PS probability; ET drift | 1%/5%; −2%/yr after 2030 | [I] | low |
| R12 λ, κ, $r_0$, g* | 0.8 (0.6–0.9), 10% (0–20%), payout-matched, 0 | 02 [I] | medium |
| $s^-$, $s^+$ | −1.35, −0.94 | [S-c] | high |
| $c_{ATM}$; term ratios | 0.90; 1.18…0.90 | [I]; Cboe [S] | medium; high |
| Convex budget | floor 0.15%; 0.15–0.5% NAV/yr | [I] | low |
| Put spread; ladder | 90/72% fwd; 3/6/12m at 25/50/25 | [I] | low |
| Monetisation | Δ ≤ −0.5, 3× premium, V3+ & VIX ≥ 35; f 50%; reset 40% | [I], optimise | low |
| φ: cash VM / OTC reuse / pledged / listed | 1.0 / 0.7 / 0 / 0.85 | [I] | low |
| Futures IM; anti-procyclicality | max(floor, 2.326σ√(5/252)); 25% stressed weight | [I]; EMIR option (unverified) | medium |
| $\delta^{rep}$ by V0–V4 | 8 / 10 / 13 / 25 / 39%, plus strategy add-ons | Jefferies 2025 87% [S]; H2 2008 61% [S, Stream 05]; [I] | medium |
| $h^{cpty}$ | 10% (20% in DB/GW/PS) | [I] | low |
| Opportunistic book | Sharpe prior N(0.3, 0.25²); budget 1.0–1.5% NAV; crowding 0.5/yr at −1.5σ | [I] + [S] haircuts | medium |
| Tier-1 thresholds | ε_H 1% (5y); 97.5% (12m); forced sale 1% at 20%; survival ≥ 24m; DCR 1.0/1.25 | Streams 10/11 [I] | IC-set |

---

## 6. Calibration targets

| Target | Value | As of | Source | Confidence |
|---|---|---|---|---|
| Sustainable payout at 10% geometric, π 2.5% | 6.8% (4.5–4.6% at 7.4%) | — | 02 [I-calc rep.] | high (arithmetic) |
| P(20-year annualised ≥10%), E=10%, σ=12% | 42% | — | 02 [I-MC rep.] | medium |
| US endowment effective spending; 10-year return | 4.9%; 7.7% (>$5bn: 62.5% alternatives) | FY2025 | NACUBO, 12 Feb 2026 [S] | high |
| Yale rule | 80/20, 5.25%, band 4.0–6.5% | rev. 1 Jul 2026 | Yale Policy 2202 [S] | high |
| Stanford rule | 80/20, 5.25% + 4% growth, 4.25–6.25% | since Oct 2021 | Fingate [S-c] | high |
| Alaska POMV | 5% of first 5 of prior 6 years; FY26 draw $3.8bn | 2 Sep 2026 | APFC [S] | high |
| Norway rule; flows | 3% expected real; inflows NOK 409bn (2024), 327bn (2025) | end-2025 | MoF, NBIM [S] | high |
| Harvard | 5% payout, 8% objective; FY26 27.1%, $68bn | FY2026 | Harvard Magazine [S] | high |
| CPP leverage | recourse debt 9.7% of adjusted net assets; board limit 45% | FY2025 | DBRS; S&P [S] | high |
| DWY outputs (model, not ADIC) | α 2%: 34.5% alternatives, 5.32% spending; 5.2% floor: 27.8% | NBER rev. 2022 | [S] | high as outputs |
| Buyout distributions/NAV | ≈14% (MSCI) | 12m to Q3 2025 | Bain 2026 [S] | high |
| PE distribution rate (global) | 11% (2025), 9% (H1 2026); contributions 27–31% | H1 2026 | MSCI via Stream 04 | medium |
| LP-portfolio pricing | 87% of NAV; buyout 92%; VC/growth 78% | FY2025 | Jefferies, 10 Feb 2026 [S] | high |
| Crisis secondary pricing | 2009 average discount ≈35% [S*]; H2 2008 high bids 61% (83.5% adjusted) | 2008–09 | WSJ via Wiki; Stream 05 | medium |
| UAE breakeven; hydrocarbon share | 44.8 (2026–27) → 45.9 (2030); 11.3% → 9.1% of GDP | 8 Dec 2025 | IMF Art. IV [S] | high (number); medium (basis) |
| UAE net lending | +1.7 (2014), −6.4 (2015), −2.4 (2020), +3.9 (2025), +1.5 (2026p) | 18 Oct 2026 | IMF DataMapper [S] | high |
| UAE real GDP | −3.9% (2026), +7.7% (2027) | WEO Oct 2026 | IMF [S] | high |
| Brent path | 2026 $96; 4Q26 $105; 2027 $84; 4Q27 $74 (pre-war 2027: $53) | STEO 6 Oct 2026 | EIA [S] | high |
| Gulf shut-ins | 10.9 (May) → 4.77 (Sep) → 4.47 (4Q26F) → 2.68 mb/d (1Q27F); UAE 0.74 (Mar–Jul), 0 (Aug–Sep) | Oct 2026 | EIA [S] | high |
| Oil–equity correlation, monthly | −0.14 (−0.26, −0.01); +0.43 (0.29, 0.56); +0.32 (0.11, 0.51) | 1988–Aug 2026 | 03 [I-calc rep.] | medium |
| Lower-tail dependence | 0.08 (2/24) vs 0.30 (7/23), p≈0.07 | 2026 | 03 [I-calc rep.] | low |
| P(eq ≤ −10% given oil ≤ −30%, 12m) | 26% (14/54 months, 11 from GFC) | 2026 | 03 [I-calc rep.] | low |
| Shock-type window shares | N 59.6, B 17.8, SG 13.5, SS 5.0, DB 4.1% | 1988–2026 | 03 [I-calc rep.] | low–medium |
| Oil volatility | calm 25%, turbulent 52%; 76.8% realised since 1 Mar 2026 | 14 Oct 2026 | 03 [I-calc rep.] | high |
| SWF redemptions in a bust | ≥$46.5bn (2015); ME oil SWFs $19bn in Q3 2015 | 2015 | eVestment/FT [S] | medium-high |
| Mexico hedge | premium ≈0.1% GDP/yr; payouts 0.5/0.6/0.3% GDP; ≈19bp funding benefit | Mar 2018 | IMF blog [S] | high |
| ATM 1m put excess return | −7.4% p.a.; positive in 8/8 drawdowns | 1985–2018 | Harvey et al. 2019 [S] | high |
| PPUT vs SPX | 7.97% vs 8.85% (price); gap to total return 2.3–3.3pp | 30 Jun 1986–16 Oct 2026 | Cboe [S rep.] | high |
| VRP (variance-swap style) | mean 4.10 pts; positive 85.9% of days; by bucket 2.8 / 4.1 / 4.9 / 6.5 / 5.8 | 1990–2026 | Cboe [S rep.] | high |
| VIX distribution | mean 19.42; p95 32.88; p99 46.70; >30 on 7.9% of days | 16 Oct 2026 | Cboe [S rep.] | high |
| Spot–vol | piecewise −1.34 to −1.37 / −0.93 to −0.95; bucket ΔVIX 2.61 / 3.95 / 6.34 / 10.40 | 2026 | 09 verify [S-c] | high |
| Term structure | VIX3M/VIX median 1.13; <1 on 7.5% of days; 0.90 at VIX ≥ 40 | since Sep 2009 | Cboe [S rep.] | high |
| VIX HMM persistence and durations | 0.664 / 0.443 / 0.468 / 0.605; 41 / 19 / 20 / 35 days | 1990–2026 | 09 [S rep.] (in-sample) | medium |
| SPX tails | 10-day p1 −8.49%, p0.1 −20.14%; 21-day worst −32.97% | since 1975 | Cboe [S rep.] | high |
| Crisis-type payoffs | VXTH +27.6% (COVID) vs −29.2% (2022); short credit +128% (2007–09) | — | Cboe; Harvey et al. [S] | high |
| Cost per crisis $, common 2008–26 window | PPUT 0.28, CLLZ 0.94, CLL 0.59, VXTH 0.07; ex-COVID 0.44 / 0.86 / 0.81 / 0.42 | 2026 | 09 verify [I-calc] | low (hindsight) |
| March 2020 margin | some CCPs' IM >100% vs prior quarter; peak VM per CCP $2.5bn (1.6× prior peak) | 2020 | FSB; Clarus [S] | high, as stress quantile |
| Rate shock | 30y gilts >270bp; resilience ≥250bp | 2022 / Mar 2023 | BoE FSR; FPC [S] | high |
| Schedule IM; UMR thresholds | equity 15%, FX 6%, IR 1/2/4%, credit 2/5/10%; MSE $8bn; IM threshold $50m | 2015 rule | 12 CFR 237 [S] | high |
| Sharpe haircuts | >50% if SR < 0.4; ≤25% if SR > 1 | 2015 | Harvey–Liu [S] | medium |
| J–R benchmark | 10.1% of GDP (exact eq.) and 9.97% (approx.), both from the 2006 working paper. The published version (*Economic Journal* 121(555):905–930, 2011, DOI 10.1111/j.1468-0297.2011.02435.x) puts the benchmark at 9.1% of output, per a citing abstract; the EJ abstract itself does not state it [corrected 2026-10-18] | 2006; 2011 | IMF WP/06/229 [S]; EJ 2011 | high (WP); medium (EJ figure) |
| Market levels | VIX 19.99; SKEW 168.6; VVIX 109.9; SPX 7,659 | 16 Oct 2026 | Cboe [S rep.] | high |

---

## 7. Strongest cross-disciplinary insights

1. **The liability is a written option** (option pricing applied to public finance).
   - The owner's draw is a NAV-scaled put spread on the fiscal state.
   - This gives a market-consistent liability value (the Q-price of the spread) and natural hedge strikes.
   - It also explains why the cap matters: beyond the lower kink, further damage comes from the asset side.
   - With the linear fiscal map it is a plain vertical spread. Smoothing makes it Asian-style; NAV co-movement makes it quanto-like.
   - The band is itself an option. Who owns it decides its sign, which is why mandate design is the zero-premium hedge.

2. **Reserves economics applied to endowment liquidity** (Jeanne–Rancière; Borensztein–Jeanne–Sandri).
   - At ADIC's crisis parameters, buffers dominate option insurance.
   - The welfare gain from hedging comes mainly from *reducing precautionary buffers*.
   - Hedges are therefore worth their enabling value: the buffer they release, priced at the α* of what that buffer funds.
   - This converges with three other results:
     - Stream 06: a debt-funded reserve is the cheapest protection;
     - Ang–Papanikolaou–Westerfield: investors would pay ≈2% of wealth to hedge once-a-decade illiquidity crises;
     - DWY: crisis illiquidity pushes holdings well away from targets.

3. **Counterparty wrong-way risk applied to liabilities, through oil-shock identification** (Kilian; Baumeister–Hamilton; Ready).
   - Liability wrong-way risk depends on the *type* of oil shock.
   - A hedge's value is $\mathrm{Cov}(\lambda,X)$ over the $(S,Z,V)$ λ-surface.
   - So equity puts fail exactly in SG and GW, where draws rise.

   **Coverage matrix** [I, from S evidence]:

   | Instrument | Fast crash | Slow grind or rates-up (2022) | Credit (2008) | SG | GW | DB |
   |---|---|---|---|---|---|---|
   | Cash and facilities | yes | yes | yes | yes | yes | yes (facility WWR) |
   | Dynamic beta | partial (latency) | yes | yes | no | partial | yes |
   | Trend 1–3m | yes | partial | yes | possible | possible | yes, then reversal |
   | Puts / put spreads | yes | weak | yes | no | weak | yes |
   | VIX calls | strong | adverse | yes | no | uncertain | yes |
   | CDX | partial | partial | strong | energy HY only | partial | yes |
   | Duration | yes (post-2000) | adverse | yes | yes | unreliable | yes |
   | Oil put spreads | no | adverse | partial | yes | adverse | yes |

4. **Corporate-finance hedging theory** (Froot–Scharfstein–Stein; Bolton–Chen–Wang).
   - Hedging pays when external finance is costly.
   - Cash, hedges, asset sales and credit lines are substitutes under a double-barrier policy.
   - That is exactly the recourse merit order, and its marginal cost is λ.

5. **Bank funds-transfer pricing (FTP) and hydro-reservoir water values.**
   - λ is the internal liquidity transfer price that belongs in the α* hurdle.
   - The distinction between $\lambda^{spot}$ and $\lambda^w$ fixes the single-period LP's understatement of intertemporal value.
   - The HLBA brings the bank-LCR discipline to overlay collateral.

6. **Actuarial ruin and pension-funding theory.**
   - Percentage-of-NAV payouts cannot cause ruin.
   - Fixed claims create absorbing barriers. These include fixed real distributions, debt service and margin.
   - Smoothing adds fixed-amount content, and with it sequence risk.
   - So payout rule, leverage and overlay sizing must be co-designed.
   - The insurance "mass-lapse" stress maps to a "mass-draw" override stress.

7. **Control theory.**
   - R12 is a linearised LQ state-feedback rule.
   - The owner's smoothing hands ADIC *lead information*, which the MPC can use as feedforward.
   - The Tier-1 layer is a safety filter (Stream 11).

8. **Behavioural political economy.**
   - Endowments hoard after losses. Oil sovereigns draw more. ADIC is an "anti-endowment", so US spending-rule evidence transfers only in part.
   - Overrides and hedge fatigue are time-inconsistency problems (in the Kydland–Prescott sense). They need precommitment devices: pre-arranged facilities, pre-approved monetisation, and IC-owned hedge budgets.

---

## 8. Links to the other clusters

**Cluster 1: optimisation core, scenario and robustness layer, objective design (Streams 01, 10, 11).**
- **Regimes:** $S_t$ is the master chain (Stream 10). $Z_t$ is coupled to it, $V_t$ is a set of labels, and SDDP uses 24 nodes.
- **SDDP convexity:** the bilinear smoothed-draw × NAV term and the clip binaries are non-convex. Discretise them into the Markov nodes, or use SDDiP/Lagrangian cuts.
- **λ:**
  - $\lambda^{spot}$ comes from this cluster's recourse model;
  - $\lambda^w$ comes from Stream 01's L2 cuts;
  - Stream 01's L1 here-and-now decision program (HDP) must emit duals in PV-$ units.
- **Constraints:** H1–H3 map onto Stream 11's C1/C2.
- **Floor:** the 7%/5% gate is replaced by Cluster 1's re-specified floor, and enabling value is measured against it.
- **Robust metrics:** KL/W1 robust metrics (Stream 10, R1–R8) apply to obligation-failure probability and hedge value.
- **Scenario generator:** this cluster's Owner Draw Engine replaces Stream 10 §6.4's reduced-form demand.
- **Views:** entropy pooling carries IC views on P(SG in 2027–28), $P^{BE}$ and war persistence.

**Cluster 2: private book, liquidity instruments, leverage, action economics, return fusion (Streams 04–08).**
- **PE distribution hazards:** Stream 04's RFT-TA hazards take $Z$ multipliers (DB 0.45, SG 0.95, GW 0.9, B 1.2) on a 9–12% base rate.
- **Secondary pricing:** follows Stream 05's MCL curve, with $\delta^{rep}$ against stale NAV and losses measured against economic NAV.
- **Leverage (Stream 06):** reserve funding, the ≤10% recourse limit and covenant chance constraints.
- **Action cards (Stream 08):** carry $\beta^{own}$, $\beta^\lambda$ and the liability-state playbook:
  - in N/B, arrange REFINANCE capacity while it is cheap;
  - in DB, hold privates and draw pre-arranged lines.
  - SELL wins when λ exceeds the buyer's expected excess return.
- **α* (Stream 07):** includes an FTP charge of λ × LAR and an owner-beta charge.

**Cluster 4: agentic architecture and IC deliberation (Streams 12–14).**
- The agents, rubric gates and artifacts are listed in §9.
- **Stream 12's warning applies directly.** In *The Agentic Scientist*, agents changed the evaluation protocol in 2 of 3 runs. Overlay timing rules are the easiest place to overfit a simulator, so the evaluation protocol must be immutable and hashed.
- **Shadow-IC seats (Stream 14)** for this cluster: Owner's Advocate, Treasurer, Hedge Skeptic and Opportunist.

---

## 9. Agentic components and IC artifacts

| Agent | Role | Deterministic core | Rubric gate |
|---|---|---|---|
| Mandate & Policy Registry | parses the legal text and versions rule parameters | rule library (§5.2) | every parameter carries citation, version and vintage |
| Sovereign Liability | builds evidence cards from IMF, EIA, budget releases and news | parsers; unit and vintage checks | source, unit, as-of date and vintage on every number; conflict flags |
| Oil Shock-Type Nowcaster | estimates the posterior P(Z_t) | Ready-style decomposition, BH-SVAR, HMM, LLM event flags | alarm when structural, statistical and narrative labels disagree |
| Owner-Draw Simulator | generates draw paths | §5.1–5.2 equations | §6 intervals; posterior predictive checks |
| Overlay Designer | proposes programmes in parameter space | Overlay Engine | CRN; baselines always run |
| Hedge Designer | builds the liability hedge stack | CVaR LP over a payoff library | no proposal without basis, margin and counterparty analysis |
| Overlay Challenger / Red Team | looks for coverage gaps, book offsets, fatigue, CSA issues; reverse stress | plausibility-constrained search | must beat the GW→SG→DB, exits-shut, override benchmark |
| Peer Calibration | keeps peer data current | scrapers | refresh calendar: NACUBO Feb; CPP May; GIC/Temasek Jul; NBIM Feb/Aug; Harvard/NZ Super Oct |
| IC Elicitation | runs SHELF forms for $P^{BE}$, $b$, ω, $\rho_d$, override, GW persistence and the DB distribution haircut | entropy pooling | records views, deltas and decisions |

**Baselines and ablations.**
- *Baselines:*
  - no hedge;
  - the Israelov divest-equivalent;
  - a static put ladder;
  - trend only;
  - facility only;
  - cash reserve only;
  - oil only;
  - the status-quo book.
- *Ablations:*
  - no monetisation;
  - no regime timing;
  - no VM recognition;
  - spot–vol slope of −1.7 vs −1.35;
  - hindsight vs rule-based costs.
- *Gates:*
  - surface no-arbitrage;
  - Kupiec margin backtest;
  - spot–vol bucket fit;
  - DSR ≥ 0.95;
  - significance across seeds.

**IC artifacts.** All are computed deterministically; LLMs only narrate and challenge.
1. Mandate-interpretation memo.
2. Liability Weather Map: Z posterior, Brent against both kink pairs, FN nowcast, $P^{BE}$ update, 3-year draw fan (P10/50/90), DCR by stress state.
3. Four-dimension distribution frontier, payout-matched, with a floor sweep.
4. Liquidity waterfall and runway: months of survival at cap draws with exits shut, plus λ curves.
5. Defensive-stack frontier: carry against Δ P(obligation failure), Δ forced-sale probability and the robust floor metric, plus the coverage matrix.
6. VM/IM heatmap against the collateral pool and HLBA.
7. "What we are paying for" decomposition and hedge-fatigue tracker.
8. Opportunistic evidence card: posterior Sharpe, DSR, crowding, crisis beta, λ-adjusted return.
9. Owner-beta / λ-beta league table for proposed actions.
10. Views panel, with live entropy-pooled updates.
11. Reverse-stress narrative and early-warning list:
    - Brent below the upper kink;
    - FN nowcast above −2pp;
    - Hormuz or Fujairah incidents;
    - OPEC+ market-share rhetoric;
    - widening secondary discounts;
    - AED forward points.

---

## 10. Open questions and data ADIC must supply

**Mandate**
1. Is the 5–10% basis opening, average, reported or economic NAV?
2. Who sets the rate within the band, and with what notice?
3. Are carry-forward, in-kind or AED payment, deferral, or exceeding the cap possible?
4. Is the 10% target gross or net, geometric or arithmetic, and over what horizon?
5. Is the owner's objective real preservation, growth or planned decumulation?
6. Does the owner make inflows in surplus years?

**Owner fiscal**
7. ADIC's draw history for 2015–26 (amount, date, basis, notice period).
8. ADIC's rank in the financing hierarchy relative to ADIA, Mubadala, L'imad/ADQ and debt.
9. The effective Abu Dhabi breakeven on a pre-transfer basis, if the owner can share it.
10. Whether domestic strategic stakes are still held, and whether they could be sold in stress.

**Private book**
11. Cash flows by fund and vintage; unfunded commitments (the dossiers assume US$27–35bn); reported vs economic NAV; secondary pricing history.

**Overlay**
12. The blotter: size, instruments, venues and dealers.
13. CSA terms: thresholds, MTA, IA, eligible collateral, reuse rights.
14. Daily VM/IM history.
15. ADIC's regulatory status under US, EU and UK margin rules.
16. Whether the opportunistic book may run net short volatility.
17. The full list of strategy variants tested, needed for N in the DSR.
18. Whether oil options and hybrids are permitted, and whether there are short-oil optics constraints.

**Liquidity and financing**
19. Existing facilities and their terms; the ability to arrange committed NAV facilities, repo or sovereign-backed lines; leverage limits; gate terms of the reported hedge-fund programme.

**Risk appetite**
20. The IC's tolerance for missing an owner payment, which sets ε_H.
21. The penalty curvature σ.
22. Who owns the hedge budget.
23. Appetite for a coordinated sovereign-level oil hedge (Mexico-style).

**Research gaps (not data):**
- re-solve a DWY-type model at ADIC parameters;
- estimate the fiscal-mapping form;
- filtered (not Viterbi) carry-by-state contrast;
- dealer RFQs for hybrids;
- the IMF Regional Economic Outlook due 22 Oct 2026 and the 2026 Article IV, to update $h$, $P^{BE}$ and $w_{GW}$.

---

## 11. Implementation notes (Python)

**Module map:**

| Module | Contents |
|---|---|
| `liab/shock_chain.py` | `monthly_generator(P_a)`, `couple(Pz, kappa_SZ)` |
| `liab/oil.py` | `simulate_brent(P0, Z, S_eps, params, rng)` → `[paths, months]` |
| `liab/fiscal.py` | `fb_pre(P, q, h, P_BE, w_Z, form)` |
| `liab/owner_draw.py` | `draw_rate(FN, d_prev, c, b, rho_d, band, p_ov)`; `kinks(params, form)` |
| `liab/rules.py` | R1–R12, POMV with `k=2..6`, Yale-literal |
| `overlay/vix.py` | VIX dynamics |
| `overlay/ssvi.py` | SSVI surface with no-arbitrage checks |
| `overlay/books.py` | beta, tail and opportunistic books |
| `overlay/margin.py` | EWMA + anti-procyclicality, schedule IM, HLBA with TTC floor |
| `ledger/ledger.py` | signed VM, φ conventions |
| `ledger/recourse.py` | `merit_order(deficit, sources, state)` → `(y, lam_spot)`; LP later |
| `ledger/water_value.py` | LSM regression |
| `metrics/tier1.py` | H1–H5 metrics, binomial standard errors |
| `metrics/decompose.py` | Shapley with CRN |

**Stack:**
- numpy/numba or JAX for simulation;
- cvxpy/HiGHS for recourse LPs;
- Pyomo/mpi-sppy, or SDDP.jl via juliacall, for SDDP;
- QuantLib-Python for Asian oil options and two-asset options;
- PyMC/NumPyro for the Bayesian draw model;
- SALib for global sensitivity;
- Optuna or CMA-ES for policy search.

**Compute.**
- 50k paths × 120 months on the monthly grid.
- Daily equity and VIX for all paths (cheap).
- Option books revalued daily by delta–gamma–vega Taylor approximation, with full revaluation monthly and at triggers.
- Importance sampling toward S-crisis/DB/V3+ for tail events below 1%. Report binomial standard errors on every probability.

**Pitfalls:**
- decisions use filtered probabilities only;
- common random numbers across policies;
- store every parameter with a vintage tag (pre-war vs post-war IMF figures);
- convert units explicitly (% of NAV vs % of GDP);
- monthly averages bias correlations, so use month-end data;
- price under Q, simulate under P;
- winsorise and restart HMMs;
- archive input data snapshots, and pin script versions to their outputs (verifier hygiene finding).

---

## 12. Source pointers

- **Full references:** the three dossiers' §10 lists. Verified URLs and corrections are in the three verification logs.
- **Primary sources behind corrected values:**
  - IMF CR 25/327 (UAE Article IV, Table 3a);
  - IMF DataMapper API;
  - EIA STEO (Feb, May, Jun and Oct 2026);
  - Cboe daily index files (to 16 Oct 2026);
  - FSB *Holistic Review* (Nov 2020);
  - BoE FSR (Dec 2022) and FPC (Mar 2023);
  - 12 CFR 237.2 and FR 2015-28671;
  - Basel LCR40;
  - Jeanne–Rancière IMF WP/06/229, published as *Economic Journal* 121(555):905–930 (2011), DOI 10.1111/j.1468-0297.2011.02435.x;
  - Harvey et al. (2019);
  - Israelov (2019);
  - Bailey & López de Prado (2014);
  - Harvey & Liu (2015);
  - NACUBO FY2025;
  - Yale Policy 2202;
  - Stanford Fingate;
  - APFC (2 Sep 2026);
  - NBER w25559 (DWY);
  - Institutional Investor and Bloomberg/Financial Planning (CalPERS, 2020).
- **Reproducible computations:**
  - Stream 03 scripts in `research/addenda/03_sovereign_alm_calcs/`;
  - the Stream 09 verifier's scripts in the session scratchpad;
  - this synthesis's arithmetic check: `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\c3_checks\c3_arith.py`. It is session scratch; archive it with the run.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2, and the citation-integrity tables in `research/literature/02_endowment_swf.lit.md`, `03_sovereign_alm.lit.md` and `09_overlay.lit.md`. Metadata was confirmed via OpenAlex.

- §2.1, Ennis row: named the published source of the size-cohort result, Ennis (2021), *J. Investing*, DOI 10.3905/joi.2021.1.166, and separated the −1.87% figure (synthesis §2.3).
  - The figure is attributed, as an inference, to Ennis (2021), "Failure of the Endowment Model", *JPM* 47(5):128–143, DOI 10.3905/jpm.2021.1.217.
  - It is marked unverified: it is absent from that abstract, and press coverage does not name the paper.
- §3, DQ24: identified the CFA Institute TPA guide as Urwin & Hayman (2026), DOI 10.56227/26.1.20 (synthesis §2.3; OpenAlex lists the two authors).
- §6, J–R benchmark row: added the published *Economic Journal* (2011) version and its 9.1% benchmark next to the working paper's 10.1% (synthesis §2.4 #7).
  - The 9.1% comes from a citing abstract and is marked medium confidence.
  - No conclusion changes, because the §5.7 corner analysis uses ADIC parameters, not the 10.1% benchmark.
- §12, source pointers: added the *Economic Journal* 121(555):905–930 citation and DOI for Jeanne–Rancière.
- Not applicable to this file, which does not cite these works: de Finetti (1957), Merton (1993), Moutanabbir & Noureldin, Lo (2002), Moreira & Muir, Kaminski & Lo, Koijen et al.'s *Carry*, Brown–Dimmock–Kang–Weisbenner and Carr & Wu.
- Not applicable: no statistic from the G4 barrier re-run appears in this file.
- Left as is, outside the §2 corrections:
  - the "WSJ via Wiki" source for the 2009 discount (§6);
  - the IMF blog source for the Mexico hedge (§6). The companion IMF working paper (Valencia et al. 2018) is not confirmed to carry the blog's premium and payout figures.
