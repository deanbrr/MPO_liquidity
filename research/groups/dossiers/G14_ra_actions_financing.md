# G14 · Real Assets actions and financing

## SELL / HOLD / REFINANCE / LEVER instruments, pricing, regime availability, execution lags, and links to Corporate Finance

**Stream:** G14 (Real Assets, the eighth group) · **Date:** 2026-10-18 · **Status:** research dossier, design-grade · **Companion to:** main report `research/00_SYNTHESIS.md` (§2.3, §4.4–4.7), groups report `research/groups/01_GROUPS_SYNTHESIS.md` (§2–4), design brief §8 · **Calculations:** `research/groups/addenda/G14_calcs/g14_ra_actions.py` → `g14_ra_actions_results.json` (summary: `g14_summarize.py`).

> **SYNTHETIC-DATA NOTICE.** Every ADIC balance, Real Assets book, hidden capital call, merit-order cost and decision example below is computed on a synthetic book built from the working allocation v2 (Real Assets $18bn NAV, ≈$4bn unfunded) and design defaults. None of it is ADIC data. Tables carrying [I-calc] values end with *SYNTHETIC – NOT ADIC DATA*.

**Tags.** [S] sourced and checked in-session (primary or reputable secondary page read); [S-sec] sourced via a search summary or secondary relay, not read at the primary; [P] practitioner or advisory material (weak evidence); [I] inference or design default; [I-calc] synthetic computation; [A] client statement or working assumption; [U] unverified, never load-bearing. **Research note:** the session's shared web-search budget ran out part-way through; later facts were verified only by fetching known pages and the Crossref API. Gaps this left are flagged in §8.

**Symbols** follow the groups report: ℓ is the per-period liquidity premium from H's duals, ℓ̄ its term average, π the deflator, κ₂₄ = 0.825 the month-24 headroom bought by $1 of t0 cash (groups report §4.8). New here: θ = economic value ÷ appraisal NAV; GAV gross asset value; D asset-level debt; E = V − D equity; ϖ ∈ [0,1] the probability that ADIC honours an underwater non-recourse loan (reputation parameter); Λ lost lock-in value; ŝ the all-in REFINANCE spread; κ the one-off value cost per $ raised; ℓ\* the break-even liquidity premium at which SELL ties HOLD.

---

## 1. Executive summary

1. **Real assets raise liquidity at the asset, not the fund.** Most REFINANCE capacity is property- or project-level non-recourse debt.
   - It is encumbrance-efficient: mortgaging an unlevered asset to 50% LTV pledges $2 of GAV per $ raised, and an already-mortgaged asset pledges nothing new, against $3.3–20 per $ for LP NAV facilities (main §4.4).
   - It sits outside CF's facilities.
   - It is procyclical: banks' net CRE tightening peaked at 68% (2023:Q3 in FRED's dating) and reads −11% for 2026:Q3 [S: FRED].
2. **Merit order.** In the groups report's units (PV cost per $ of month-24 T4′ headroom), normal-regime Real Assets levers are mid-cost [I-calc]:
   - core direct-asset sales ≈0.04;
   - infrastructure LP secondaries ≈0.065 (91–95% of NAV [S]);
   - maturity cash-outs ≈0.07–0.08;
   - JV sell-downs and ground leases ≈0.08–0.10.

   That is comparable to SMA sales (0.054) and NAV facilities (0.070), and cheaper than PE pacing cuts (0.219). Real-estate LP secondaries (68% of NAV [S]; ≈0.37) and early refinancing of cheap legacy debt (≥ 0.32) are near the bottom. In a crisis every lever costs 0.15–0.55 and availability roughly halves.
3. **Borrow or sell.** A maturity cash-out beats the cheapest sale only for needs shorter than T\* ≈ 1.8 years in normal markets, matching main §4.4's "≈2 years". In stress T\* stretches to 5–8 years, but lenders' capacity shrinks [I-calc]. Arrange stress capacity in benign regimes.
4. **Never refinance cheap legacy debt early.** Lock-in value Λ = D(r_new − r_old)A(τ) is 2.1–4.8% of GAV at 40% LTV, and the marginal rate on an early 40%→55% cash-out is ≈14% [I-calc]. Bridge with a JV sell-down or junior capital instead.
5. **Time to cash.**
   - Direct sales: median 135 days (UK [S-sec]); 7–12 months in stress with 30–50% failure [I].
   - LP sales: 3–6 months.
   - Open-end redemptions: ODCE funds paid ≈71% of queues a quarter after 2007, but ≈5% in 2023 [S]. Queues peaked at 19.3% of NAV (Q1-2024) and are ≈10% now [S].
6. **Hidden capital calls.** Non-recourse debt is non-recourse only if ADIC hands back keys. The synthetic levered direct book is $22.8bn of GAV: 40% of its debt matures within 24 months, and every energy borrowing base is redetermined. A credit crisis calibrated to the observed 44% office and 14% all-CRE negative-equity shares [S target], and an oil-down regime, give these 24-month equity cures [I-calc]:

   | Regime | Walk away when optimal: mean / comonotone P95 | Never walk away: mean / comonotone P95 |
   |---|---|---|
   | Credit crisis | $0.47bn / $2.05bn | $0.70bn / $2.79bn |
   | Oil-down | $0.33bn / $1.59bn | $0.47bn / $2.02bn |

   In the oil-down regime, energy borrowing-base cuts and Gulf assets supply ≈55–70% of the mean. Floating-rate sub-books cash-trap in 3–59% of crisis paths depending on sector (0–30% in normal regimes; residential highest), which cuts Real Assets distributions in the drought.
7. **Look-through debt ≈ the recourse budget.** ≈$15.5bn (LTV 46%, 8.8% of fund NAV), against T5's $17.7bn recourse target [I-calc].
   - Keep it out of T5's recourse limit, but add a T5-RA row.
   - Count guarantees as recourse.
   - Measure exposure Δ-adjusted.
   - Precedent: NBIM caps unlisted real-estate debt at 25% of the portfolio and 70% per investment [S].
8. **Corporate Finance links.** Cures, capex and development calls, cap replacements and covenant cures are contingent outflows in the L4 budgets and the CLC. With the revolver signed (≈23bp a year per $ of headroom), asset-level cash-outs for liquidity are dominated; Real Assets levers become marginal only past the revolver cap, or without it.
9. **Rate hedges:** Overlay-run, Δ-adjusted, option-based. A 3-year SOFR cap costs ≈0.2–1.1% of notional [I-calc]. In 2023 one large CRE-CLO cap's cost rose 348% in a year, and ≈40% of sampled caps expired before loan maturity [S]. Central payer swaps would post VM in demand busts.
10. **Transfer taxes.** Seller taxes lift κ from 3.3% to 6.9% (NYC) or 8.8% (Saudi Arabia). Rebuilding exposure pays buyer taxes again (UK 5%, Netherlands 10.4%, Germany 3.5–6.5%, Dubai 4%) [S].
11. **Internal transfers raise zero liquidity and transfer zero risk.** Financing from Private Credit or Capital Solutions also removes non-recourse protection at the total-portfolio level.
12. **Oil states cut both ways.** Energy and natural resources are confirmed in scope.
    - Gulf war, today's state: energy-fund pricing improved 9.2% in 1H-2026 [S], so energy is a SELL source. Gulf-located assets fall (≈−33% synthetic).
    - Oil-down (SG/DB), which raises the owner draw: energy LP bids fell to 61–76% of NAV in the 2015 oil slump [S-sec]. Most respondents to a spring-2020 industry survey expected borrowing-base cuts of ≥ 20% [S]. Deficiencies are cured in 3–6 monthly installments [S]. Real Assets therefore delivers hidden calls exactly when the draw peaks.

---

## 2. Core concepts and theory

### 2.1 Two primitives, three financing levels

Main §4.4 reduces every action to exposure (sell, hold, add) and financing (borrow b ≥ 0 against the asset), with LEVER ≡ ADD + REFI. Real assets add a twist: financing exists at three levels with different recourse, encumbrance, covenants and owners.

| Level | Instruments | Recourse to ADIC | Owner of the decision |
|---|---|---|---|
| Asset (propco, opco, project SPV) | Mortgage, project finance, construction loan, ground lease, sale-leaseback, mezzanine, preferred | None, except guarantees (completion, carve-out "bad-boy", payment) and reputation | Real Assets group, under the CF envelope |
| Holdco or fund | Infra holdco debt, fund-level NAV loan, subscription line | Usually none; structurally subordinated | GP, or Real Assets for ADIC-controlled vehicles |
| LP portfolio | LP-level NAV facility, preferred equity on a portfolio of fund interests | Full (ADIC borrows) | CF (main §4.4: PE · REFI row) |

Only asset-level debt lets ADIC keep the asset, raise cash and cap its loss at the equity. That option is worth something only if ADIC is willing to use it (§2.4).

### 2.2 Why real assets are illiquid, and why illiquidity is state-dependent

- **Search and marketing-period risk.** Real estate trades in decentralized search markets, so the expected time to sell and its uncertainty are first-order risks that make appraisal-based risk understate true risk (Lin & Vandell 2007; Bond, Hwang, Lin & Vandell 2007) [S: citations verified]. Time to sell varies with market state, asset quality and participant type (Devaney & Scofield 2015; §4.5).
- **Liquidity is procyclical.** Turnover and the reservation-price gap move with the cycle, so transaction-based indices must control for variable liquidity (Fisher, Gatzlaff, Geltner & Haurin 2003) [S: citation verified]. For ADIC this means sale lags and discounts are regime variables, not constants.
- **Liquidation values set debt capacity.** When industry peers are distressed, assets sell below value to outsiders (Shleifer & Vishny 1992) [S]. Commercial loans on properties with more redeployable use (looser zoning) get larger, longer and cheaper credit (Benmelech, Garmaise & Moskowitz 2005) [S: citation verified]. Specialized infrastructure and single-use property therefore carry lower stressed LTV caps and higher sale discounts.

### 2.3 Rollover risk and debt overhang

Debt overhang (Myers 1977) worsens under rollover risk, because short maturities transfer value to creditors when refinancing terms deteriorate (Diamond & He 2014) [S]. Chen & Chen (2025) find causal evidence in CMBS-financed CRE [S, read]:
- properties near rollover lose NOI and occupancy and cut capex;
- a 1pp rate gap cuts the refinancing probability by 11.1%;
- rollover-risk sales clear ≈12–13% below refinance valuations.

These anchor a refinancing-probability elasticity and a near-maturity sale discount in the engine.

### 2.4 Non-recourse debt as an option, and the reputation constraint

With non-recourse debt the equity is a call on asset value struck at the debt (Merton). Mortgage termination is a competing-risks problem between prepayment and default (Ciochetti, Deng, Gao & Yao 2002) [S]. Securitized and portfolio loans renegotiate differently: CMBS workouts are more rigid (Black, Krainer & Nichols 2017) [S]. Large sponsors do use the option (Brookfield, Los Angeles, 2023; §5).

A sovereign investor may not, for reputational or relationship reasons. The model therefore carries ϖ, the probability that ADIC honours an underwater non-recourse loan:
- equity exposure is $X=\Delta V$, with $\Delta=\varpi+(1-\varpi)N(d_1)$;
- with ϖ = 1 the debt is economically recourse, and every refinancing gap becomes a capital call.

### 2.5 Open-end vehicles: stale NAV, first movers and queues

Redemptions at a stale NAV in a falling market give early redeemers a first-mover advantage, which produces run-like flows (Chen, Goldstein & Jiang 2010, on mutual funds) [S]. Open-end real-estate funds respond with notice periods and pro-rata payment from available cash. Most have moved away from first-in-first-out, which encouraged a "run on the bank" [S: Townsend/PREA]. Open-end infrastructure funds meet redemptions "from cash yield or queued capital", not by selling assets [S: IFM 2023]. The redemption right is therefore a claim on other investors' new money and on income, both of which vanish in stress.

### 2.6 Lock-in value

A borrower with fixed debt at r_old below today's r_new holds an asset worth

$$\Lambda=D\,(r_{new}-r_{old})\,A(r_{new},\tau),\qquad A(r,\tau)=\frac{1-(1+r)^{-\tau}}{r}.$$

Early refinancing or a sale with payoff surrenders Λ, unless the loan is assumable, in which case the buyer pays for it. For a cash-out that replaces D_old with L_new ahead of maturity, the marginal rate on the incremental cash is

$$r^{marg}=r_{new}+\frac{D_{old}}{L_{new}-D_{old}}\,(r_{new}-r_{old}),$$

which reaches ≈14% for a 40%→55% cash-out with a 3.75% legacy coupon and a 6.6% new rate [I-calc].

### 2.7 Consistency with the main report's pricing

All rules use main §4.4's kernel and its full reduced cost. Four metrics put Real Assets instruments in the same units as PE:
1. **REFINANCE metric** (main §4.4): pass iff $\hat s=s_B+f/T+\lambda_{Lev}+\text{covenant charge}+h/T<\bar\ell_{[0,T]}$, with h the hedge cost.
2. **One-off value cost per $ raised**, $\kappa=(\text{value given up})/(\text{cash raised})$, used to rank sources (main §4.4 "value cost per $ raised").
3. **Encumbrance per $ raised**, comparable with main §4.4's $3.3–20 for NAV loans and $1.10 for a sale at 91%.
4. **Break-even premium ℓ\***, the liquidity index at which SELL ties HOLD (stream 08's ℓ\*_i).

They combine in the SELL-versus-REFINANCE test: $\kappa_{REFI}(T)=\kappa^{1\text{-}off}_{REFI}+\hat s\,A(r_f,T)$ against κ_SELL, for a liquidity need of T years.

---

## 3. Methods, models and trade-offs

### 3.1 Instrument cash-flow formulas

Each instrument is a bundle (main §4.4): proceeds, give-ups, ΔU, lag, capacity, a correlated execution indicator, consents, encumbrance and irreversibility. Notation per asset i in regime z; j is the jurisdiction.

**SELL: direct asset or portfolio sale.**

$$P^{cash}_i=N_i\,\theta_z(1-d_z)(1-f^s-\tau^s_j)-D_i-pp_i,\qquad \kappa_i=\frac{V_i-N_i\theta_z(1-d_z)(1-f^s-\tau^s_j)+pp_i+\Lambda_i}{P^{cash}_i}.$$

- Cash arrives at $t+L$, with $L\sim\text{LN}(\ln m_z,0.35)$ and $m_z$ = 4.5, 7 and 10 months (N, T, C).
- Success follows a correlated Bernoulli with $\pi_z$ = 0.85, 0.70 and 0.50.
- An assumable loan removes $\Lambda_i$ and $pp_i$ and transfers them into the price.
- For a temporary liquidity need, add the re-entry charge $\kappa^{re}=\tau^b_j+f^b$ (buyer-side taxes and fees when the exposure is rebuilt).

**SELL: JV stake.** $P=\omega_iE_i(1-d_z)(1-\delta^m_z)(1-f)$, where δ^m is the minority and lack-of-control discount. A partner ROFR or ROFO adds 30–90 days, and a buy–sell clause can force a sale or purchase. In crises the partner is often the only buyer.

**SELL: LP interest in a closed-end real-estate or infrastructure fund.** This reuses the PE hedonic (main §4.4, PE · SELL) with segment levels $\Pi^{RE}_z$, $\Pi^{INF}_z$ and the same age, quality, unfunded-share and geography terms. The buyer assumes the unfunded commitment, so the unfunded relief counts as liquidity.

**SELL: open-end redemption (queue machine).** For fund f, the payout ratio is set by cash available against the queue:

$$q_{f,t}=\min\!\Big(1,\frac{C_{f,t}}{Q_{f,t}}\Big),\quad C_{f,t}=\text{income}+\text{subscriptions}+\text{disposals}-\text{capex}-\text{debt service},\quad \text{ADIC cash}_t=q_{f,t}R^{ADIC}_{f,t},$$

with $R_{t+1}=R_t(1-q_t)+u^{red}_t$. Notices $u^{red}$ are lodged 45–90 days before quarter end. Other investors' requests follow the hedge-fund machine's form, $R^{oth}=NAV\cdot\mathrm{clip}(\rho_S+\rho_1[-r^{rel}]^++\rho_2\mathbb 1\{Q/NAV>q^\*\})$. The only interface to the ladder is φ_f(h, S), the P5 cumulative cash share by horizon, exactly as for hedge funds (main §4.6).

**SELL: open-end unit secondary.** $P=NAV(1-d^{OE}_z)$, executed in 2–6 weeks with manager transfer approval.

**REFINANCE: cash-out at maturity.**

$$L^{max}_{i,t}=a_{i,t}\cdot\min\Big\{LTV^{max}_zV_{i,t},\ \frac{NOI_{i,t}}{DSCR^{min}_z\,k(r_t+s_z)},\ \frac{NOI_{i,t}}{DY^{min}_z}\Big\},\qquad P=(L_{new}-D_i)-fL_{new}-h_i.$$

- $a_{i,t}$ is lender availability: Bernoulli with a common factor shared across assets.
- k is the loan constant (interest-only or amortizing).
- Infrastructure uses gearing and DSCR without a debt-yield test, and a higher gearing cap.
- $\hat s=(r_t+s_z-r_f)\frac{L_{new}-D_i}{P}+\frac{f+h}{T}+\text{cov}+\lambda_{Lev}\frac{\Delta Lev}{P}$.
- Before maturity, add Λ to the one-off cost.

**REFINANCE: junior capital on top of cheap senior debt** (mezzanine or preferred equity). $P=(LTV^{stack}-LTV^{sr})V(1-f)$ at rate $r^{jr}_z$. It keeps Λ, needs intercreditor or senior-lender consent, and makes a cure harder later.

**REFINANCE: ground lease** (sell the land, lease it back). $P=gV$, with rent $G_t=y^{cash}_0P(1+e)^t$. The cost is the economic yield $y^{econ}$, including escalators; the cash cost starts lower. The leasehold is worth $V^{LH}=V-PV(G)$, and $PV(G)$ counts as debt-like. It is a near-irreversible 99-year senior claim.

**Other REFINANCE instruments** (formulas in §6.1):
- sale-leaseback: $P=V$, with lease $cP(1+e)^t$, an IFRS 16 liability;
- JV sell-down: a partial SELL with small δ^m;
- LP-level NAV facility: main §4.4's PE row with segment LTVs;
- infrastructure holdco debt: structurally subordinated, so opco lock-ups can stop its debt service.

**Energy and natural resources.** The borrowing base is $BB_t=\alpha_z\,PV(\text{reserves}\mid\text{bank price deck}_t)$, redetermined semi-annually. A deficiency $(D_t-BB_t)^+$ must be cured in 3–6 monthly installments [S], which makes it a hidden call in oil-down states.

**LEVER.** Acquisition debt is $D=LTV\cdot V$; development debt is $D=LTC\cdot\text{cost}$, with completion guarantees that are recourse. Main §4.4's LEVER ≡ ADD + REFI identity is a reconciliation test.

### 3.2 Asset-level debt state machine (the stress mechanics)

| State variable | Equation | Consequence |
|---|---|---|
| DSCR, LTV, debt yield | $DSCR_t=NOI_t/(I_t+A_t)$, $LTV_t=D_t/V_t$, $DY_t=NOI_t/D_t$ | Maintenance tests and cash management |
| Cash trap | $Dist_t=(NOI_t-I_t-A_t-\text{reserves})^+\cdot\mathbb 1\{DSCR_t\ge DSCR^{trap}\}$ | Distributions to ADIC stop without any default (G15's cash map must use this) |
| Floating rate and cap | $r^{eff}_t=\min(r_t,K)+s$ while the cap is live; then $r_t+s$ | A cap that expires before maturity is a cliff; replacement cost is a cash use (cap reserve escrow) |
| Maturity gap | $S_{i,T}=\max(0,D_{i,T}-L^{max}_{i,T})$ | Equity cure, extension (lender's choice, with fee and sweep), sale, or handing back the keys |
| Cure decision | Ruthless: cure iff $V-D-\bar\ell S>\max(0,V(1-d_z)-D)$; walk away iff the sale value is ≤ 0. Reputation-bound (ϖ = 1): always cure; with no lender and no extension, sell if equity is positive, else repay in full | Hidden capital call $H=S\cdot\mathbb 1\{\text{cure}\}+D\cdot\mathbb 1\{\text{take-out}\}$ |
| Covenant breach | LTV or DSCR below its trigger | Cure by paydown (cash use), cash trap, or default |

Pricing the cure at ℓ̄ matters. A dollar injected in a high-λ state costs (1 + ℓ), so a ruthless policy walks away more often in crises. The engine records which policy ADIC has declared.

### 3.3 Calibration of the stress regime

The crisis regime is fitted to an observed cross-section, not to a narrative. On a bank-loan-like book (LTV 62% ± 12%, 3-year horizon), the office cap-rate shock that reproduces the 44% office negative-equity share is **+242bp with NOI −3% a year**. The shock that reproduces the 14% all-CRE share is **+113bp with flat NOI** [I-calc; target: Jiang et al.]. The synthetic book's crisis regime uses these shocks (office +242bp; other sectors +100–150bp). Cross-checks:
- Trepp's September-2026 CMBS delinquency is 12.16% for office and 8.02% overall [S-sec: Yieldpro relay];
- a vendor sample reports that 34% of recently resolved maturities needed a cash-in refinancing averaging 12–18% of the original balance [U: LoanBoss, unaudited].

### 3.4 Trade-offs

| Choice | Option A | Option B | Recommendation |
|---|---|---|---|
| Granularity | Asset by asset (gaps, covenants and caps are asset-specific) | Cohorts (sector × vintage × LTV bucket) | Cohorts for path simulation; assets for action scoring on common random numbers, as for PE (main §4.2) |
| Lender availability | Deterministic terms by regime | Stochastic availability with a common factor | Stochastic. Availability is the binding constraint in C, and correlation across assets drives P95 cures |
| Default policy | Ruthless | Reputation-bound | Run both. The policy is ADIC's choice and must be declared (open question 3); its value is the cure-cost difference |
| Queue | Static haircut | State machine | State machine (main R3 logic: documents matter more than averages) |

---

## 4. Empirical evidence and current market data

### 4.1 Secondary markets for real-asset fund interests

| Item | Value (as of) | Source |
|---|---|---|
| LP-portfolio pricing, % of NAV, H1-2026 | All 87; buyout 91; venture 79; credit 89; **real estate 68**; **infrastructure 91** | Jefferies, *Global Secondary Market Review*, Jul-2026 [S, read] |
| Real-estate LP pricing history | 83 (2019), 76 (2020), 79 (2021), 71 (2022), 71 (2023), 72 (2024), 70 (2025), 68 (H1-26) | Jefferies via main dossier 05 [S/C] |
| Jefferies on real estate | Pricing "settled at 68% of NAV" as "liquidity conditions remained challenged" | Jefferies Jul-2026 [S] |
| Jefferies on energy | Commodity volatility "significantly increased the pricing and demand of upstream and natural resources funds" | Jefferies Jul-2026 [S] |
| LP-led discounts, 1H-2026 | Average 13.3%; infrastructure **5.0%**; credit 5.1%; venture 32%. Real estate "remains at significant discounts" but improved 6.0%; energy improved 9.2% on higher-for-longer oil views | Campbell Lutyens 1H-2026, Aug-2026 [S, read] |
| Infrastructure secondaries volume | $9bn (2022) → $20bn (2025); $10bn in 1H-26 (78% GP-led, against 55% in 2025); CL forecasts $26bn for 2026, Jefferies ≈$30bn | Campbell Lutyens [S]; Jefferies insight page [S-sec] |
| Structure in LP sales | 33% of LP sales structured: deferrals in 26%; preferred equity, managed funds and CFOs in 7% | Jefferies Jul-2026 [S] |
| Real-assets continuation vehicles | Sponsors use CVs to keep trophy logistics, data-centre, senior-housing and residential assets; infrastructure CVs for "cash-generative assets" | Jefferies Jul-2026 [S] |

**Reading.** Infrastructure interests are near-cash in normal markets (5–9% discounts). Real-estate interests are not (32%), partly because NAVs lag (θ < 1; G13). Infrastructure liquidity increasingly comes through GP-led processes: 41% of volume in 2023, 78% in 1H-2026 [S].

### 4.2 Open-end vehicles: queues, payouts and unit secondaries

| Item | Value (as of) | Source |
|---|---|---|
| NFI-ODCE size | 25 funds; $280.4bn gross and $223.7bn net real-estate assets (Q2-2026) | NCREIF press release, 30 Jul 2026 [S, read] |
| ODCE leverage | 27.1% of total assets (Q2-26); range 15–34% since 2000; average 22.4% | NCREIF [S] |
| ODCE flows | Year to Jun-2026: contributions $10.4bn, distributions and redemptions $19.1bn, net −$8.7bn | NCREIF [S] |
| Queue, % of NAV | 9.2% (Q4-2020, COVID); 19.3% (Q1-2024); ≈12% (Q3-2025); just above 10% (Q1-2026). GFC peak 15% (Meketa) or ≈21% of core NAV in 2009 (Townsend) | Meketa, Jul-2024 [S, read]; Accordant [S/S-sec]; PREA Quarterly, Winter 2024 [S, read] |
| Payout speed and notice | Since 2007 ODCE funds paid ≈71% of queues a quarter on average (cleared ≈60% of the time); ≈5% a quarter in 2023; redemptions averaged < 1.5% of NAV a quarter. Notice most commonly 90 days before quarter end (some 45–60); payment mostly pro-rata | PREA / Townsend [S] |
| Unit secondaries | Normal: −8% to +3% of NAV; 2–6 weeks to execute. UK stress (Nov-2022): bids −25%, offers −15% for two of the most liquid diversified funds. Mid-2021: bids −5.0% to +3.5% | Alliance Global Advisors, 2020 [S]; DTZ Investors, Dec-2023 [S] |
| UK deferrals | Managers defer when net outflows exceed thresholds and "generally have up to two years to pay out" | DTZ Investors [S] |
| Private REIT limits | 2% of NAV a month and 5% a quarter. BREIT met 43% of requests (Nov-22), ≈25% (Jan-23), 35% (Feb-23), 15% (Mar-23), 29% (Apr-23 and Sep-23); 100% from Feb-2024, exceeding its quarterly limit in Jun-2024 | Bisnow relays [S-sec]; Morningstar on pro-rata fills [S-sec] |
| Open-end infrastructure | Redemptions met "from cash yield or queued capital"; units trade on the secondary market at prices set by market conditions, not NAV | IFM Investors, 2023 [S, read] |

### 4.3 Asset-level debt markets, the 2023 crunch, and today

| Item | Value (as of) | Source |
|---|---|---|
| Fixed-rate permanent loans, Q2-2026 | Commercial spread 204bp (−21bp YoY), multifamily 162bp, over Treasuries for 5–10-year loans. LTV 59.6% commercial, 63.3% multifamily. DSCR 1.43; debt yield 10.2%; average rate 5.7% | CBRE press release, 3 Aug 2026 [S, read] |
| Lender mix, Q2-2026 (non-agency) | Alternative lenders 38%, banks 30%, life companies 21%, CMBS 11% | CBRE [S] |
| 2023 crunch, Q3-2023 | LTV 61.4% (58.3% in Q2); underwritten cap rate 5.68%; loan constants 6.72% (+79bp); life companies 33.5% of volume; alternative lenders 27.5%; CMBS conduits < 1% of non-agency volume | CBRE, 13 Nov 2023 [S-sec] |
| Net % of banks tightening CRE (nonfarm nonresidential), FRED quarter dating | 41.5 (Q3-22), 52.9, 57.6, 66.7, **68.3 (Q3-23)**, 67.2, 42.4 (Q1-24) … 3.3 (Q4-25), −3.6, −3.3, **−11.3 (Q3-26)** | FRED SUBLPDRCSN (Fed SLOOS) [S, read] |
| Maturity wall | $875bn (17% of $5.0tn) matures in 2026, after $957bn in 2025. Shares maturing in 2026: hotel 30%, industrial 23%, office 17%, multifamily 13%. CMBS/CLO/ABS $200bn (25% of their book); depositories $396bn | MBA, 9 Feb 2026 [S, read via MBA Newslink] |
| CMBS delinquency, Sep-2026 | Overall 8.02%; office 12.16%; multifamily 8.04%; retail 6.58%; lodging 6.18%; industrial 1.14% | Trepp via Yieldpro, 4 Oct 2026 [S-sec] |
| Negative equity | 14% of CRE loans and 44% of office loans have values below debt | Jiang, Matvos, Piskorski & Seru, NBER w31970 (Dec-2023, rev. Dec-2024) [S, read] |
| Rollover effects | 1pp rate gap → −11.1% refinancing probability; rollover-risk sales ≈12–13% below refinance valuations; ≈$2.26tn of CRE mortgages mature by end-2028 | Chen & Chen, Jun-2025 [S, read] |
| Cap costs, 2023 | A $337.5m, 4%-strike cap expiring Feb-2024 rose from ≈$0.78m to ≈$3.5m (+348% YoY); ≈40% of 682 CRE-CLO loans had caps expiring before maturity; uncapped note rates ≈200bp above capped ones | CRED iQ via Commercial Observer, 27 Mar 2023 [S, read] |
| Mezzanine and preferred pricing, 2026 | Mezzanine 11–15% current pay plus PIK (13–18% all-in); preferred 12–18%; preferred enforcement takes 6–18 months | Advisory and marketplace pages [P, weak] |

### 4.4 Alternative REFINANCE markets

| Item | Value (as of) | Source |
|---|---|---|
| Ground leases, new originations | $150m in Q2-2026 at GLTV 35%, rent coverage 3.0×, economic yield 7.4% (7.2% in Q1-26) | Safehold Q2-2026 results via Investing.com, 30 Jul 2026 [S-sec] |
| Ground leases, portfolio | GLTV 52%; coverage 3.4×; cash yield 3.8% (5.5% GAAP); economic yield 6.0% including escalators and 2% inflation | Same [S-sec] |
| Net-lease cap rates, Q2-2026 | Single-tenant 6.82%; industrial 7.25%; retail 6.60% | Boulder Group via ConnectCRE [S-sec] |
| NAV financing margins | Cluster at 4–7%, falling year on year; most NAV loans still fund new investment | Rede Partners, 23 Jun 2026 [S, read] |
| NAV LTVs | Typically 10–25% for PE and infrastructure funds; infrastructure tenors longer | White & Case, via search summary [S-sec] |
| Subscription lines | Average margin ≈1.85% in H1-2026 (1.96% in Q4-2025) | Maples Group, 2026 update [S-sec] |
| Infrastructure gearing | Ofwat PR24 notional gearing 55% (60% at PR19), set for BBB+/Baa1 | Ofwat and company submissions [S-sec] |

### 4.5 Transfer taxes and transaction costs (illustrative; verify per deal)

| Jurisdiction | Tax on transfer of commercial property | Usual payer | Source |
|---|---|---|---|
| UK (England) | SDLT non-residential: 0% to £150k, 2% to £250k, 5% above | Buyer (valuations are usually net of purchaser's costs) | gov.uk [S-sec] |
| Netherlands | 10.4% non-residential (2026); 8% for investor-held residential from 1 Jan 2026 | Buyer | Deloitte; Norton Rose Fulbright [S-sec] |
| Germany | 3.5% (Bavaria) to 6.5% by state. Share deals taxed at ≥ 90% over a 10-year look-back | Buyer (contractual) | Tax calculators; A&O Shearman [S-sec] |
| New York City | RPTT 2.625% above $500k, plus New York State tax for conveyances ≥ $2m (0.65% [U]) | Seller | nyc.gov [S] |
| Los Angeles | Measure ULA 4% / 5.5% above ≈$5.4m / $10.9m (indexed), on top of 0.45% city and 0.11% county tax | Seller | Hanson Bridgett [S-sec] |
| Saudi Arabia | RETT 5% on transfers (regulations reissued Apr-2025) | Seller, generally | ZATCA; King & Spalding [S-sec] |
| Dubai | DLD transfer fee 4% | Customarily buyer | Brokerage guides [P] |
| Abu Dhabi | Registration fee ≈2%, often split | Negotiable | Brokerage guides [P] |

Seller-borne taxes enter κ directly. Buyer-borne taxes are capitalized into bids when NAV is quoted gross (US). Where valuations are net of purchaser's costs (UK, much of Europe), they are already in NAV, but they return as κ^re if ADIC later rebuilds the exposure. Transaction times: median 135 days to sell and 104 days to buy, on 578 UK deals in 2004–13 [S-sec: Devaney & Scofield 2015].

### 4.6 Energy and natural resources (confirmed in scope)

| Item | Value (as of) | Source |
|---|---|---|
| Reserve-based lending (RBL) mechanics | Borrowing base redetermined semi-annually, with interim redeterminations on request. A deficiency is cured by equal monthly installments, "usually between three and six". Production payments are a bankruptcy-remote asset sale. Unwinding in-the-money hedges "will almost certainly result in a borrowing base redetermination" | Latham & Watkins Q&A, 22 Apr 2015 [S, read] |
| Oil-down stress, spring 2020 | A large majority of respondents expected borrowing-base cuts of at least 20%, and 45% expected 30% or more; banks' base-case oil price deck was 15.6% below fall 2019 | Haynes Boone surveys, 1 Apr 2020 [S, read] |
| Energy LP pricing in an oil slump | Median energy-fund bids 61–76% of NAV in 2H-2015 (up to 80% in 1H), the lowest of all strategies | Harken Capital via *Secondaries Investor*, 29 Feb 2016 [S-sec; article paywalled] |
| Energy LP pricing in an oil-up shock | Energy LP pricing +9.2% in 1H-2026; upstream demand up on commodity volatility | Campbell Lutyens; Jefferies [S] |

**Reading.** Energy financing is the most oil-procyclical in the group. The borrowing base is a price-deck function, so an oil-down state cuts debt capacity mechanically and turns deficiencies into short-fuse cash calls (3–6 months) on ADIC's energy co-investments and direct assets. That happens exactly when the owner's draw rises (main L3).

---

## 5. Practitioner and peer practice, and case studies

**Peer leverage limits on real assets.**
- **NBIM** (Executive Board investment mandate, amended 9 Dec 2025 [S, read]):
  - unlisted real estate: "The debt ratio of the unlisted real estate portfolio shall not exceed 25 per cent", and "No single investment shall be financed with more than 70 per cent debt", measured at acquisition or refinancing;
  - unlisted renewable infrastructure: the portfolio debt ratio "over time shall not exceed 60 per cent", with 70% per investment;
  - NBIM measures leverage "both at portfolio level and for each individual investment" [S: NBIM letter, 3 Nov 2025].
- **CalPERS** real estate: LTV < 50% and DSCR > 1.5 (policy guidelines reported in 2020-era board documents). A 2012 interim schedule allowed 50% core, 65% value-add and 75% opportunistic, with 50% long-term for all [S-sec: CalPERS board items].
- **CPP Investments** reports recourse debt (debt guaranteed by the parent) at 9.7% of adjusted net assets in FY2025, against a Board recourse-leverage limit of 45% of net assets [S-sec: DBRS, S&P]. How it treats non-recourse subsidiary debt was not verified here [U].

The pattern: peers separate recourse leverage (agency-facing) from asset-level debt limits written into the real-asset mandate. ADIC should do the same (§6.3).

**Open-end managers in stress.** ODCE managers pay pro rata from available cash and hold modest reserves; Townsend suggests ≈2% of NAV [S]. At 2023's ≈5% of queues a quarter, clearing takes years. BREIT's caps produced 15 months of pro-rata partial fills [S-sec].

**Sponsors and non-recourse debt.**
- *Brookfield, Los Angeles (2023).* Brookfield did not repay the Gas Company Tower's $350m mortgage and $65m + $50m mezzanine loans at the 9 February 2023 maturity, and the court appointed a receiver. A second default, on 777 Tower ($319m), brought the total to $784m [S-sec]. An institutional sponsor exercised the walk-away option on office assets where a cure would have been value-negative.
- *Thames Water (2023–26),* a Gulf-relevant case: ADIA's Infinity Investments is a listed shareholder [S-sec: Wikipedia summary of press reports].
  - Shareholders injected £750m in July 2023 (£1bn sought), then withheld the first payment of a larger plan in March 2024.
  - OMERS (31.7%) wrote its stake to zero in May 2024.
  - Debt reached ≈£20bn by January 2026, and creditors proposed write-offs of more than £13bn.

  The lesson: high opco gearing plus holdco debt makes equity cures recurring hidden calls, and politics cut against a ruthless policy.

**Other practice.**
- Real-assets continuation vehicles mean GPs, not LPs, increasingly decide when infrastructure and trophy real-estate assets are refinanced or sold; LPs get an election, as in PE (main §4.4) [S].
- The lender mix is a regime variable: life companies took a third of volume in Q3-2023 while CMBS conduits nearly vanished, and alternative lenders and banks lead in 2026 [S].

---

## 6. Design implications for the ADIC framework

### 6.1 Real Assets instrument library (main §4.4 format)

Defaults are [I] unless tagged. κ is the one-off value cost per $ raised; ŝ the all-in REFINANCE spread over SOFR; "Enc." the NAV or GAV pledged or given up per $ raised. Only external counterparties raise liquidity.

| Group · lens | Instrument | Pricing rule / defaults | Time to cash · availability (N / T / C) | Consent · encumbrance |
|---|---|---|---|---|
| RA · SELL | Direct asset or portfolio sale | §3.1 formula. θ, d by regime: 1.00, 2% / 0.95, 8% / 0.90, 15–20% (rollover-risk discount 12–13% [S: Chen & Chen]); fees 1–1.5%; τ^s by jurisdiction (§4.5). κ 3.3% (US low-tax, N), 6.9% (NYC), 8.8% (KSA) → 14–18% (C). ℓ\* 1.0% (N) → 3.6–4.4% (C). Add κ^re if the exposure will be rebuilt | Median 4.5 / 7 / 10+ months (135-day UK median [S]); success 0.85 / 0.70 / 0.50 | JV, lender and ground-lessor consents; loan assumption removes Λ; Enc. $1.03 per $ (N) |
| RA · SELL | JV stake sale | ωE(1−d)(1−δ^m)(1−f); δ^m 3–7% / 8–12% / 15–25% (valuation-practice range 10–25% as upper bound [P]). κ 8.5% (N), 42% (C) | ROFR/ROFO 30–90 days, then 4–6 months; in C often only the partner bids | Partner consent, buy–sell, drag/tag |
| RA · SELL | LP-interest secondary | PE hedonic with Π^RE = 0.68 (H1-26 [S]), Π^INF = 0.91–0.95 [S], energy rising in oil-up states [S]. C: RE 0.55–0.60, infrastructure 0.80–0.85 [I]. θ^RE 0.82–0.88 → κ 31% (N), 45% (C); infrastructure 5% (N), 15% (C) | 3–6 months; success 0.75 / 0.6 / 0.45 | GP consent, ROFR; buyer assumes unfunded; Enc. $1.49 (RE), $1.09 (infra) per $ |
| RA · SELL | Open-end redemption | At NAV through the queue machine, q = 0.71 / 0.20 / 0.05 a quarter (N and C anchored [S]). P5 cash share 0.43 / 0.85 at 1 / 4 quarters (N); 0.04 / 0.18 at 4 / 8 quarters (C). Value cost at ℓ = 10%: 5.0% (N), 13.9% (T), 21.7% (C) [I-calc] | Notice 45–90 days before quarter end; pro rata | Manager discretion, gates; none |
| RA · SELL | Open-end unit secondary | 0.92–1.03 × NAV (N); bid 0.75, offer 0.85 in stress [S]. Sell units iff 1 − p^OE < value cost of the queue at ℓ̄ | 2–6 weeks [S] | Manager transfer approval |
| RA · SELL | Private-REIT repurchase | 2% a month and 5% a quarter caps; fills of 15–43% in a run [S-sec] | Monthly | Board discretion |
| RA · REFI | Cash-out at maturity | §3.1 L^max. N: LTV 60–65%, DSCR 1.25×, DY 8.5%, spread 160–204bp over Treasuries [S anchor], fees 1–1.5%; infrastructure gearing cap +10pp, no DY test. ŝ 3.2% / 4.4% / 7.2% [I-calc] | 2–4 / 4–5 / 6 months; availability 0.97 / 0.80–0.85 / 0.50–0.60, with a common factor | Lender; Enc. $2.0 per $ if unlevered, 0 if already mortgaged (ring-fenced) |
| RA · REFI | Early cash-out | Adds Λ = 2.1–4.8% of GAV; marginal rate on new cash ≈14%; κ 21% (N) | As above | **Inadmissible by default** while Λ > 0.5% of GAV, unless the IC overrides |
| RA · REFI | Mezzanine or preferred on cheap senior | 13% / 14.5% / 16% [P]; ŝ 10.0% (N), 13.6% (C); keeps Λ | 6–12 weeks; 0.9 / 0.75 / 0.5 | Intercreditor; complicates later cures |
| RA · REFI | JV sell-down (control kept) | As JV stake with δ^m 3% / 8% / 15%: κ 6.3% / 19% / 40% for 49% [I-calc] | 4–8 months | Lender change-of-control; partner selection |
| RA · REFI | Ground lease | P = gV, g ≈ 0.35 [S-sec]; economic yield 7.2–7.4% with escalators [S-sec]; ŝ ≈ 3.5–3.6%, perpetual; PV(G) counts as debt | 3–6 months; US and select sectors, 0.8 (N) | Leasehold-mortgage consent; near-irreversible |
| RA · REFI | Sale-leaseback (owner-operated) | Cap rate 6.6–7.3% [S-sec] plus escalators; ŝ ≈ 4.7% | 3–6 months | IFRS 16 debt |
| RA · REFI | LP-level NAV facility (CF owns) | RE fund interests: S + 450–650bp, LTV 5–15%; infrastructure: S + 300–450bp, LTV 10–25% [I; 4–7% margin cluster S]. ŝ 6.5% (RE), 4.4% (infra), 9.7% (RE, C) | 6–12 weeks; RE 0.7 (N) → 0.3 (C) | Per-fund pledge; Enc. $5–20 per $ |
| RA · REFI | Infrastructure holdco debt or opco recap | Holdco S + 400–550bp, PIK toggle; opco within rating and regulatory gearing (Ofwat notional 55% [S-sec]); ŝ ≈ 5.5% | 2–4 months; benign regimes only | Opco lock-ups; structural subordination |
| RA · REFI / LEVER (energy) | Reserve-based lending (RBL) or project debt | Borrowing base = advance rate × PV(reserves at the bank price deck); semi-annual redetermination; a deficiency is cured in 3–6 monthly installments [S]. Synthetic advance rate 0.575 (N) → ≈0.38–0.40 (C and OD) | Weeks if pre-arranged; oil-down cuts ≥ 20% widely expected (2020 [S]) | Hedging and reserve-report covenants; a cut is a hidden call |
| RA · SELL (energy, partial) | Volumetric production payment or royalty sale | Bankruptcy-remote sale of future production [S]; priced off the strip less a risk premium [I] | 2–4 months; strongest in oil-up states | Counts as debt-like in look-through leverage while production is owed [I] |
| RA · REFI (energy) | Commodity-hedge monetization or reset | Unwind or reset in-the-money hedges for cash; this triggers a redetermination [S] | Days, with counterparty consent | Raises cash and lowers the borrowing base at the same time |
| RA · LEVER | Acquisition debt | LTV 55–65%, DSCR ≥ 1.25–1.43×; LEVER iff ADD and REFI both pass | 2–3 months | T5-RA row (§6.3) |
| RA · LEVER | Development or construction loan | LTC 50–60%, S + 300–500bp; completion and cost-overrun guarantees **count as recourse** | 3–6 months | Guarantees in T5 limit 1 |
| RA · LEVER | Subscription line (club and JV vehicles) | ≈S + 185bp [S-sec]; shifts calls 0–180 days | Days | Counts as look-through debt |
| RA · HOLD | Hold, cure or hand back keys | §3.2 cure rule at ℓ̄ under ADIC's declared ϖ | — | — |

*SYNTHETIC – NOT ADIC DATA.*

### 6.2 Regime availability and lags

| Instrument | N | T (LATE × D) | C (credit crisis, DB) | GW (Gulf war, today) | OD (oil-down: SG/DB) |
|---|---|---|---|---|---|
| Direct sale, non-Gulf | 1.0 · 4.5m | 0.85 · 7m | 0.5 · 10–12m | as T | as T (as C if DB) |
| Direct sale, Gulf-located | 1.0 · 5m | 0.8 · 7m | 0.4 · 12m | 0.3–0.5 · 9–12m; value ≈−33% [I-calc] | 0.45 · 10m; value ≈−29% [I-calc] |
| Energy real assets, sale | 1.0 | 0.9 | 0.5 | **1.0+**: pricing improving [S] | **0.3–0.5**, wrong-way with the draw [I]. LP bids 0.61–0.76 of NAV (2015 analogue [S-sec]) |
| Energy RBL capacity | 1.0 | 0.95 | 0.6–0.7 | 1.0+ | 0.6–0.8 of the prior borrowing base (≥ 20% cuts expected in 2020 [S]) |
| LP secondary, RE / infrastructure | 0.75 / 0.85 | 0.6 / 0.8 | 0.45 / 0.55 | as T | as T |
| Open-end payout q | 0.71 | 0.20 | 0.05 | as T | as T |
| Cash-out at maturity, non-Gulf | 0.97 | 0.80–0.85 | 0.50–0.60 | 0.85 | 0.85 |
| Cash-out, Gulf lenders | 0.97 | 0.80–0.85 | 0.50–0.60 | 0.50–0.55 | 0.60–0.65 |
| Junior capital | 0.9 | 0.75 | 0.5 | 0.6 | 0.6 |
| JV stake sale or sell-down | 0.8 · 6m | 0.7 · 8m | 0.4 · 12m | as T; Gulf JVs 0.3 | as T; Gulf JVs 0.4 |
| Ground lease, sale-leaseback | 0.8 · 4m | 0.6 · 6m | 0.3 · 9m | as T (not offered for Gulf assets [I]) | as T |
| Infrastructure holdco debt | 0.85 · 3m | 0.6 · 4m | 0.2 · 6m | as T | 0.5 (energy-linked 0.3) |
| Development loans, subscription lines | 0.9 / 1.0 | 0.6 / 0.95 | 0.2 / 0.8 (committed lines drawn) | as T | as T |
| NAV facility on RE funds | 0.7 | 0.5 | 0.3 | 0.5 | 0.5 |

All values are [I] except the queue anchors and the energy-pricing direction [S]. Lags are multiplied by 1.5 in C. Availability draws share a lender factor across assets and with CF's facilities (2008 lines evidence, main §2.3(d)).

### 6.3 Constraints, leverage accounting and Corporate Finance

**Three leverage measures, one per purpose.**
1. **Recourse leverage (T5 limit 1, agency-facing).** CF debt, plus guarantees: completion at maximum exposure, payment guarantees at face, carve-out guarantees at 10–25% of the guaranteed loan [I]. If ADIC declares ϖ = 1, add the reputation-implied contingent recourse, P95 of the 24-month refinancing cures.
2. **New row T5-RA: look-through Real Assets leverage at ADIC share.**
   - Portfolio GAV-LTV ≤ 45% (target) and ≤ 55% (hard).
   - Single asset ≤ 65%, or 70% for contracted or regulated infrastructure (NBIM's 70% per-investment cap is the precedent).
   - Development LTC ≤ 60%.
   - ≤ 25% of Real Assets look-through debt maturing in any rolling 12 months (mirrors T5 limit 5).
   - Unhedged floating-rate share ≤ 30% [I].
   - The synthetic book sits at 46% LTV, between target and hard [I-calc].
3. **Economic exposure (T5 limit 2, 1.30×).** Count Real Assets at Δ-adjusted GAV, $X=[\varpi+(1-\varpi)N(d_1)]V$. Δ is 1.00 / 0.99 / 0.95 / 0.85 / 0.70 / 0.53 at LTV 0.40 / 0.55 / 0.70 / 0.85 / 1.00 / 1.15 (σ = 18%, 3 years) [I-calc], so it matters only once assets are distressed.

**Encumbrance (T5 limit 3).** Asset-level mortgages pledge ring-fenced SPV assets, not ADIC's balance sheet. Apply the 15%/20% limit to ADIC-level encumbrance only (IM, repo, LP pledges) and track asset-level encumbrance inside T5-RA. Otherwise ≈$23bn of mortgaged GAV would consume most of the limit.

**Covenant chance constraints** (main 06 limit 7 extended):
- P(DSCR or LTV trigger within 12 months) ≤ 2% per loan;
- P(maturity gap > 20% of D | regime T) ≤ 10% for loans maturing within 24 months [I].

**Phase I eligibility.** Maturity cash-outs, JV sell-downs, infrastructure LP sales and core direct sales in N or T are *amber* levers (tier TPFA). RE LP secondaries and any sale in C are *red* or *black* and excluded from Phase I, like PE sales. A 30-day row credits every Real Assets lever at 0.

**Ladder, budgets and FTP.** Real Assets contributes contingent outflows:

$$O^{stress}_{RA,h}=Q_{95}\Big[\sum_{i:T_i\le h}H_i+\text{capex}_h+\text{DevCalls}_h+\text{CapRepl}_h+\text{CovCures}_h\Big]-\text{credited income}_h.$$

- It enters the L4 group-budget row as $LC_{RA}=\sum_i(\kappa^{s^\*}U_i+c^{s^\*}_i-\delta^{s^\*}_{RA}V_i)+O^{stress}_{RA,24}\le B_{RA,24}+u_{RA}$, and the contingent-liquidity charge as $CLC_{RA}=c_{buf}\sum_h\omega_hO^{stress}_{RA,h}$. Real Assets earns c_buf on stressed income it reliably pays up, net of cash traps.
- On the synthetic book, cures alone over 24 months are $2.05–2.79bn at P95 in C and $1.59–2.02bn in OD, a CLC of ≈$24–42m a year at c_buf = 1.5% [I-calc].
- FTP on holdings follows groups §4.8, $\text{FTP}^{hold}_{RA}=\sum_h\mu_h\mathrm{NCO}_{RA}(h)/(5\,\mathrm{NAV}_{RA})$, with cures and cash traps inside NCO. New deployment pays the hurdle φ^new_RA/D_RA, plus the T2 dual on cash paid at closing.

**CF's revolver versus Real Assets debt.** With the revolver signed (R1), μ ≈ 0.011 PV per $ of headroom (≈23bp a year), far below Real Assets' ŝ ≥ 3.2%. Asset-level cash-outs *for liquidity* are then dominated, and Real Assets debt must earn its place through LEVER economics. Real Assets levers become marginal when the $15bn revolver cap binds (the θ = 0.82 signpost, where μ jumps to 4.8–5.5% PV), or in R0 (no revolver, μ = 0.243), where every lever at ≤ 0.10 clears before pacing cuts (0.219) [I; needs the integrated re-run].

### 6.4 Decision rules priced by the liquidity shadow price

These rules give intuition; H scores exactly (main §4.4). The Score gains Real Assets terms:

$$\Delta\mathrm{Score}_{RA}=-\kappa^{tax}-\kappa^{re}\mathbb 1\{\text{rebuild}\}-\Lambda-\kappa^{ctrl}-h-\text{cov}-\lambda_{LT}\Delta D^{LT}-\lambda_{Mat}\Delta Mat_{12}$$

where λ_LT and λ_Mat are the duals of the T5-RA rows.

1. **SELL** iff $p^{ce}\ge p^\*$, the main-report reservation price with Λ, κ^tax and κ^re added; equivalently iff ℓ̄ ≥ ℓ\*_i when feasible. Synthetic ℓ\*:

   | Instrument | ℓ\* (N) | ℓ\* (C) |
   |---|---|---|
   | Core direct sale (US) | 1.0% | 3.6% |
   | Same, with UK-type κ^re 6.8% | 2.6% | — |
   | Infrastructure LP | 1.4% | 3.5% |
   | Real-estate LP | 6.4% | 9.0% |
   | JV stake | 2.2% | 8.9% |

   *SYNTHETIC – NOT ADIC DATA* [I-calc].
2. **REFINANCE at maturity** iff $\hat s<\bar\ell_{[0,T]}$: 3.2% (N), 4.4% (T), 7.2% (C). **Never early** while Λ > 0.5% of GAV. Bridge instead with a JV sell-down (κ 6.3% in N) or junior capital (ŝ ≈ 10%).
3. **Borrow or sell.** Borrow iff the cash need is shorter than T\*: refinancing at maturity against the cheapest sale gives T\* = 1.8 / 5.3 / 7.7 years (N / T / C); junior capital gives 0.5 / 1.7 / 3.4 years [I-calc]. In C, prefer borrowing *if available*. Plan the capacity in N, because availability halves.
4. **Open-end.** Lodge redemption notices at CFP Amber; in past cycles many investors rescinded requests as markets stabilized [S: Meketa], so confirm revocability in each fund's documents. Sell units in the secondary market iff the bid discount < the queue's value cost at ℓ̄: ≈21.7% at ℓ = 10% and 32.4% at ℓ = 20% in C, against a ≈25% stress bid [I-calc; S anchor].
5. **Cure** iff V − D − ℓ̄S > max(0, V(1 − d) − D) under a declared ϖ. The IC pre-commits the policy as a contingent plan (brief §7, item 11), not case by case.
6. **LEVER** iff μ̂_A − r_D − β_Aπ_p − κ·SE − SC > 0 (main 06 rule) *and* the covenant chance constraints hold. At r_D ≈ 6.6%, core real estate at an unlevered 6.5–7.5% fails; contracted infrastructure at 8.5% with S + 200bp passes modestly (main 06).
7. **Structure.** Prefer share deals, fund-unit transfers and partial stakes where lawful; price κ^re whenever the exposure will be rebuilt.

**Worked example** (core logistics: GAV $500m, debt $200m at 3.75% with 2 years left, NOI yield 5%) [I-calc; SYNTHETIC]:

| Regime | Cheapest for a 1-year need | Cheapest for a 2-year need | Cheapest for a 5-year need | Avoid |
|---|---|---|---|---|
| N | Maturity cash-out, κ 4.2% ($74m) | JV sell-down 49%, κ 6.3% ($138m); maturity cash-out 6.8% | JV sell-down 6.3% | Early cash-out, κ 26% at 2 years (Λ = $10.5m) |
| T | Maturity cash-out 5.2% ($49m) | Maturity cash-out 8.7% | Maturity cash-out 18.5% ≈ JV sell-down 19.3% ($123m) | Early cash-out 46% |
| C | Maturity cash-out 7.1% ($25m, P = 0.5) | Maturity cash-out 12.5% | Maturity cash-out 27.6% (only $25m); JV sell-down 40% for size | SELL 100%, 46%; early cash-out > 100% |

### 6.5 Overlay and other groups

**Overlay** (rate and inflation hedging of Real Assets debt).
- Keep lender-required caps at the SPV, with the Overlay as execution agent (≥ 3 quotes; novation consents).
- Run a central book for the Δ-adjusted residual, $h^\*_i=\Delta_i\cdot(\text{floating share}_i)$. Non-recourse walk-away makes a 1:1 hedge over-hedge underwater assets.
- Prefer caps and swaptions to payer swaps. A central payer swap posts VM when rates fall in a demand bust, exactly when λ peaks, while the SPV's interest saving stays trapped behind cash management.
- Cap reserve escrows and replacement caps are CF cash uses and enter O^stress.

| Group | Channel with Real Assets | Rule |
|---|---|---|
| Private Credit | Lends to Real Assets holdings | Zero liquidity, **and no limited-liability value for the total portfolio**; counts as equity in Δ and leverage; information barriers in workouts; external quote or ≥ 50% syndication |
| Capital Solutions | Preferred or NAV loans | Internal, so zero liquidity; reserve-price intelligence only (groups §4.2) |
| Secondaries | Buys fund stakes; forecasts clearing prices | Zero liquidity if it buys; its desk forecasts RE and infrastructure prices behind a firewall |
| Co-investment | Portfolio companies' real estate | Their sale-leasebacks are Co-investment's REFINANCE; the leases count as look-through debt |
| Corporate Finance | Envelopes, FTP, CLC, guarantees | §6.3; tail cash is never ring-fenced for cures |

### 6.6 SPECIFICATION CARD (Real Assets actions and financing)

| Block | Specification |
|---|---|
| **Data fields** (per asset, JV or fund) | `group=RA`, `is_synthetic`, sector, jurisdiction, structure (asset or share deal; SPV), ω, control rights (ROFR/ROFO, buy–sell, drag/tag, consent list), appraisal NAV N, θ prior, V, NOI, cap or discount rate, capex plan. **Debt tape:** lender type, balance, maturity, amortization, fixed or floating, spread, floor, hedge (cap K, expiry, notional, reserve), covenants (LTV, DSCR, DY, trap and sweep triggers), extension options, prepayment terms (yield maintenance or defeasance), assumability, recourse flags and guarantees. **Fund units:** LP transfer consent and ROFR; open-end notice, gate, queue position, dealing dates. Bitemporal u/a/f marks (G13) |
| **Return, NAV, cash flow** | V from NOI/cap with regime shocks (crisis calibrated: office +242bp with NOI −3% a year; all CRE +113bp). NAV appraisal-smoothed (G13). Distributions $(NOI-I-A-\text{reserves})^+$ gated by the trap; maturity gap S = (D − L^max)^+; cures H; fund flows via RFT-TA v2 with RE and infrastructure parameters (brief §8) |
| **Parameter defaults** | §6.1–6.2 tables. q = 0.71 / 0.20 / 0.05; LTV^max 62.5 / 57.5 / 52.5% (infrastructure +10pp); DSCR^min 1.25 / 1.35 / 1.40; DY^min 8.5 / 9.5 / 10.5%; availability 0.97 / 0.85 / 0.60; extension 0.70 / 0.65 / 0.55; floating share 25% [I], with caps expiring before maturity on 40% of floating loans [S: CRED iQ]; ϖ = 1 until ADIC confirms |
| **Liquidity terms and stress** | φ(h, S) from the queue machine; time-to-cash distributions; 30-day credit 0; amber levers in Phase I; cures, traps, cap replacements and covenant cures in O^stress; Gulf-located assets on GW/OD lending terms |
| **S/H/R/L economics** | SELL: direct, JV, LP, open-end (queue or unit sale), energy production payments. HOLD: cure decision under ϖ, including borrowing-base deficiencies. REFINANCE: cash-out at maturity, junior capital, JV sell-down, ground lease, sale-leaseback, LP NAV facility (CF), holdco, RBL draws, hedge monetization. LEVER: acquisition, development (recourse guarantees), subscription lines. Rules §6.4; metrics κ, ŝ, ℓ\*, T\*, Enc. |
| **Forecasts and biases** | Business plans assume refinancing at underwriting terms and NAV exits. Priors [I]: refinancing proceeds overstated by the gap between plan LTV and regime L^max; exit cap rate optimism +25–50bp; sale-timing slip +2–4 quarters (T), +4–8 (C); cap costs understated. Score refinancing and sale forecasts in the registry (WIS) |
| **Synthetic defaults** | Levered direct and JV sleeves at ADIC share ($bn GAV, LTV): office 2.4, 50%; logistics 4.2, 42%; residential 3.6, 48%; retail and hotel 1.6, 50%; Gulf mixed-use 2.0, 45%; core infrastructure 6.2, 55%; energy and natural resources 2.77, 35% (RBL, redetermined semi-annually). Closed-end funds $4bn NAV at fund LTV 50%; open-end core $2bn at 27.1%. Totals: GAV $33.5bn, look-through debt $15.5bn, equity $18.0bn. 40% of non-energy debt matures within 24 months. Jurisdiction mix [I]: US 45%, Europe 25%, GCC 15%, APAC 15%. No agriculture or timber (excluded by the user) |
| **Links** | CF: T5-RA rows, envelopes, FTP, CLC, guarantees, revolver substitution. Overlay: Δ-adjusted option hedges. PC, CS, Secondaries: internal flows count as zero liquidity and carry no limited liability. G10–G13: value and NOI engines, marks; G15: cash map and ladder |

*SYNTHETIC – NOT ADIC DATA* for every number not tagged [S].

---

## 7. Implementation notes

- **Modules.** `ra/instruments.py` holds vectorized κ, ŝ, ℓ\*, T\* and encumbrance functions, with parameters in a hashed table. `ra/debt.py` runs the debt state machine on (paths × assets) arrays. `ra/queue.py` runs the queue machine and returns φ(h, S). `ra/hedges.py` revalues caps and swaptions in full under Bachelier. The prototype is `g14_ra_actions.py`.
- **Integration with H.** Each Real Assets action is a bundle column with coefficients on the L4 liquidity rows, the T5-RA rows, CVaR and encumbrance. The cure is a stage-2 recourse variable under the *declared* ϖ. It is not optimized, so H cannot game the walk-away option, and it is horizon-free (P15).
- **Lender availability.** Draw one common factor per regime-quarter and map assets through a Gaussian copula (ρ ≈ 0.5 [I]), shared with CF facility availability. The comonotone sum of cohort P95s used in §1 is an upper bound; production computes book-level quantiles on joint paths.
- **Numerical guards.**
  - Bracket the ℓ\* root on [0, 5] and return 0 when SELL already wins at ℓ = 0.
  - Handle annuities at r → 0.
  - Implement the three-way minimum in L^max as piecewise-linear in the LP.
  - Floor cap rates (≥ 3%) under shocks.
  - Clip LTVs to [0.05, 0.95].
- **Double-counting traps.**
  - Count the stale-NAV premium once: either in θ or as the open-end redemption transfer, not both.
  - Count lock-in once per decision: in SELL with payoff, or in early REFI.
  - Deduct cash traps from G15's cash map, not twice.
  - Book internal PC or CS loans to Real Assets as zero on the ladder (gate V2) and as equity in Δ.
- **Tests.** LEVER ≡ ADD + REFI; queue conservation (cash ≤ requests; φ monotone and ≤ 1); cures monotone in ℓ̄; Δ ∈ [0, 1], with Δ = 1 at ϖ = 1; the calibration reproduces 44% and 14% within ±1pp; T\*(N) ∈ [1.5, 2.2] years; every Real Assets card carries `priced_on`, and `test_no_pinned_duals` covers them.
- **Performance.** 20k paths × ≈300 assets × 40 quarters is 2.4·10⁸ asset-quarters. Run cohorts for paths and assets only for scoring, using numba if needed.

## 8. Risks and limitations

- **Evidence gaps.** The web-search budget ran out mid-session, so several facts are [S-sec].
  - Not found: 2008–09 pricing of RE and infrastructure LP interests; open-end infrastructure queue data; Gulf banks' real-estate lending in oil shocks. The oil-state values in §6.2 are therefore inference.
  - Mezzanine and preferred pricing is [P]. The NYS 0.65% rate and CPP's non-recourse treatment are [U].
- **Transferability.** CMBS and bank-loan evidence (Jiang et al.; Chen & Chen; Trepp) describes higher-LTV, more securitized books than a sovereign's core portfolio. The negative-equity calibration fits a cross-section, not dynamics. Infrastructure refinancing is simplified to property-style tests with a gearing uplift.
- **Market structure.** Ground-lease capacity is concentrated in few originators. JV discounts borrow tax-valuation ranges. GP-led processes increasingly decide infrastructure exits, which limits LP control.
- **Governance.** ϖ is a choice, not a parameter to estimate. Real Assets business plans tend to assume refinancing at underwriting terms. Internal financing is tempting because it looks like liquidity.
- **Synthetic dependence.** Every [I-calc] number depends on the assumed book. Re-run with ADIC's debt tape and the G10–G13 engines before any IC use.

## 9. Open questions (for ADIC to supply or confirm)

1. **Size and vehicles.** Sectors are confirmed: real estate, infrastructure, and energy & natural resources, with agriculture and timber excluded. Confirm size (working $18bn NAV, ≈$4bn unfunded), regional mix, and whether "funds" include open-end and evergreen vehicles; the queue machine matters only if they do.
2. **Debt tape.** Loan by loan, per the specification card: guarantees, cash-management triggers, cap strikes and expiries, assumability, extension options.
3. **Default policy ϖ.** Will ADIC ever hand back keys on non-recourse debt? It decides whether asset-level debt is economically recourse, and therefore T5 treatment, CLC and the hedge ratio.
4. **JV documents.** ROFR, ROFO and buy–sell clauses; cash-call and dilution provisions (partners' calls are hidden calls); consent rights.
5. **Fund documents.** LP transfer consents; open-end and private-REIT holdings, notice periods and queue positions.
6. **Jurisdictions and structures.** Asset versus share deals; tax positions; whether Islamic-finance structures (ijara, murabaha) finance GCC assets, which changes the REFINANCE economics.
7. **Corporate Finance policy.** Adopt T5-RA and the ADIC-level encumbrance basis? Set the guarantee policy, who arranges asset-level debt in benign regimes, and whether the Overlay hedges centrally.
8. **Gulf and energy exposure.** Local assets, lenders and government-linked tenants; energy debt (RBL or project) and hedge books, with G12.
9. **Conventions and internal links.** Is NAV gross or net of purchaser's costs (this moves κ by up to the local tax)? Do Private Credit or Capital Solutions already lend to Real Assets holdings?

## 10. References

**Academic** (metadata checked on Crossref or the publisher page unless marked).
- Benmelech, E., Garmaise, M. J. & Moskowitz, T. J. (2005). Do liquidation values affect financial contracts? Evidence from commercial loan contracts and zoning regulation. *Quarterly Journal of Economics* 120(3), 1121–1154. https://doi.org/10.1162/003355305774268200
- Black, L., Krainer, J. & Nichols, J. (2017; online 2016). From origination to renegotiation: a comparison of portfolio and securitized commercial real estate loans. *Journal of Real Estate Finance and Economics* 55(1), 1–31. https://doi.org/10.1007/s11146-016-9548-1
- Bond, S. A., Hwang, S., Lin, Z. & Vandell, K. D. (2007). Marketing period risk in a portfolio context: theory and empirical estimates from the UK commercial real estate market. *JREFE* 34(4), 447–461. https://doi.org/10.1007/s11146-007-9022-1
- Chen, J. & Chen, Y. (2025). The writing on the maturity wall: commercial real estate performance and rollover risk. Working paper, 9 June 2025. https://haas.berkeley.edu/wp-content/uploads/archive/The-Writing-on-the-MAturity-Wall.pdf
- Chen, Q., Goldstein, I. & Jiang, W. (2010). Payoff complementarities and financial fragility: evidence from mutual fund outflows. *Journal of Financial Economics* 97(2), 239–262. https://doi.org/10.1016/j.jfineco.2010.03.016
- Ciochetti, B. A., Deng, Y., Gao, B. & Yao, R. (2002). The termination of commercial mortgage contracts through prepayment and default: a proportional hazard approach with competing risks. *Real Estate Economics* 30(4), 595–633. https://doi.org/10.1111/1540-6229.t01-1-00053
- Devaney, S. & Scofield, D. (2015). Liquidity and the drivers of search, due diligence and transaction times for UK commercial real estate investments. *Journal of Property Research* 32(4), 362–383. https://centaur.reading.ac.uk/43823 (abstract-level check only)
- Diamond, D. W. & He, Z. (2014). A theory of debt maturity: the long and short of debt overhang. *Journal of Finance* 69(2), 719–762. https://doi.org/10.1111/jofi.12118
- Fisher, J., Gatzlaff, D., Geltner, D. & Haurin, D. (2003). Controlling for the impact of variable liquidity in commercial real estate price indices. *Real Estate Economics* 31(2), 269–303. https://doi.org/10.1111/1540-6229.00066
- Jiang, E. X., Matvos, G., Piskorski, T. & Seru, A. (2023, revised 2024). Monetary tightening, commercial real estate distress, and US bank fragility. NBER Working Paper 31970. https://www.nber.org/papers/w31970
- Lin, Z. & Vandell, K. D. (2007). Illiquidity and pricing biases in the real estate market. *Real Estate Economics* 35(3), 291–330. https://doi.org/10.1111/j.1540-6229.2007.00191.x
- Myers, S. C. (1977). Determinants of corporate borrowing. *Journal of Financial Economics* 5(2), 147–175. https://doi.org/10.1016/0304-405X(77)90015-0 (metadata from memory; not re-checked)
- Shleifer, A. & Vishny, R. W. (1992). Liquidation values and debt capacity: a market equilibrium approach. *Journal of Finance* 47(4), 1343–1366. https://doi.org/10.1111/j.1540-6261.1992.tb04661.x

**Secondary markets and open-end vehicles.**
- Jefferies (Jul-2026). *Global Secondary Market Review*. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- Jefferies (2026). Infrastructure secondaries hit their stride. https://www.jefferies.com/insights/markets/infrastructure-secondaries-hit-their-stride-a-once-niche-corner-of-the-market-could-reach-30-billion-in-2026/
- Campbell Lutyens (Aug-2026). *1H 2026 Secondary Market Full Report*. https://campbell-lutyens.com/media/keapzv55/campbell-lutyens-1h-2026-secondary-market-full-report_august-2026.pdf
- NCREIF (30 Jul 2026). NFI-ODCE 2Q2026 press release. https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf
- Accordant Investments (2026). Q1 2026 NFI-ODCE index insights. https://www.accordantinvestments.com/knowledge-center/private-real-estate-enters-a-new-cycle-q1-2026-nfi-odce-index-insights
- Kochis, R. & Moné, N. (Winter 2024). Negative fundraising: redemption queues in open-end commingled funds. *PREA Quarterly*. https://www.prea.org/publications/quarterly/negative-fundraising/
- Meketa Investment Group (Jul-2024). Current state of core real estate. https://meketa.com/wp-content/uploads/2024/07/MEKETA_Current-State-of-Core-Real-Estate.pdf
- Berry, S. (8 Dec 2023). Breaking through the noise: the viability of open-ended real estate funds. DTZ Investors. https://www.dtzinvestors.com/en/news/2023/december/breaking-through-the-noise-the-viability-of-open-ended-real-estate-funds-in-the-wake-of-ongoing-redemption-deferrals
- Rzoski, M. (2020). Transacting in the open-end fund secondary market. Alliance Global Advisors. https://alliance-globaladvisors.com/blog/transacting-on-the-open-end-fund-secondary-market
- Bisnow (2023–24), BREIT repurchase reports. https://www.bisnow.com/news/national/capital-markets/breit-fulfills-29-of-aprils-45b-withdrawal-requests-marking-a-sixth-limited-month-118746 ; https://www.bisnow.com/news/national/investment/breit-fulfills-repurchase-requests-pushing-past-quarterly-withdrawal-limit-124951
- IFM Investors (2023). Open and closed-ended funds in infrastructure investment. https://www.ifminvestors.com/siteassets/shared-media/news--insights-pdfs/tl_ifm065_infra_oce_funds_v8.pdf

**Debt markets.**
- CBRE (3 Aug 2026). Commercial real estate lending fundamentals remain strong in Q2 2026. https://www.cbre.com/press-releases/commercial-real-estate-lending-fundamentals-remain-strong-q2-2026-cbre
- CBRE (13 Nov 2023). Commercial real estate lending market shows signs of stabilizing in Q3 2023. https://www.cbre.com/press-releases/commercial-real-estate-lending-market-shows-signs-of-stabilizing-in-q3-2023
- Federal Reserve via FRED. SUBLPDRCSN (net % of banks tightening, nonfarm nonresidential CRE). https://fred.stlouisfed.org/data/SUBLPDRCSN
- Mortgage Bankers Association (9 Feb 2026). 17 percent of commercial and multifamily mortgage balances to mature in 2026. https://newslink.mba.org/mba-newslinks/2026/february/mba-newslink-tuesday-feb-10-2026/17-of-commercial-and-multifamily-mortgage-balances-to-mature-in-2026/
- Rudy, M. (4 Oct 2026). Multifamily CMBS delinquency rate leads overall rate higher in September (Trepp data). Yieldpro. https://yieldpro.com/2026/10/multifamily-cmbs-delinquency-rate-leads-overall-rate-higher-in-september
- McDevitt, M. (CRED iQ) (27 Mar 2023). CRE CLO interest rate cap agreements in the spotlight. *Commercial Observer*. https://commercialobserver.com/2023/03/cre-clo-interest-rate-cap-agreements-spotlight
- LoanBoss (2026). The 2026 maturity wall: a data-driven update [U]. https://insights.loanboss.com/articles/research/2026-maturity-wall-data
- Latham & Watkins (22 Apr 2015). Are you an E&P company facing a liquidity crunch and considering restructuring? (Q&A). https://www.lw.com/admin/Upload/Documents/Are-You-an-E-and-P-Company-Facing-a-Liquidity-Crunch-and-Considering-Restructuring.pdf
- Haynes Boone (1 Apr 2020). Spring 2020 oil and gas industry surveys (borrowing-base redeterminations; price decks). https://www.haynesboone.com/news/press-releases/spring-2020-oil-and-gas-industry-surveys
- *Secondaries Investor* (29 Feb 2016). Energy and venture pricing fell further in H2 (Harken Capital data; paywalled, figures via search summary). https://www.pei-secondariesinvestor.com/energy-and-venture-pricing-fall-further-in-h2/
- Commercial Observer (Apr-2023). Brookfield's Gas Company Tower moves to receivership after default. https://commercialobserver.com/2023/04/brookfield-gas-company-tower-recievership/ ; Bisnow: https://www.bisnow.com/news/los-angeles/commercial-real-estate/brookfield-default-downtown-los-angeles-gas-tower-777-figueroa-117640

**REFINANCE alternatives, fund finance, infrastructure.**
- Safehold Q2-2026 results via Investing.com (30 Jul 2026). https://www.investing.com/news/company-news/safehold-q226-slides-multifamily-focus-drives-growth-amid-valuation-gap-93CH-4826424
- ConnectCRE (2026). Net lease cap rates tick upward in Q2 2026 (Boulder Group). https://www.connectcre.com/stories/net-lease-cap-rates-tick-upward-in-q2-2026/
- Rede Partners (23 Jun 2026). Rede NAV 2026. https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026
- White & Case. Net asset value finance gains ground with infrastructure managers. https://debtexplorer.whitecase.com/leveraged-finance-commentary/net-asset-value-finance-gains-ground-with-infrastructure-managers
- Maples Group (2026). Cayman Islands fund finance market update 2026. https://maples.com/knowledge/cayman-islands-fund-finance-market-update-2026
- Economic Insight for Southern Water (PR24). Gearing and capital structures. https://www.southernwater.co.uk/media/3oxmuk0r/srn-ddr-055-economic-insight-gearing-and-capital-structures-report.pdf
- PeerSense (2026). Best mezzanine lenders 2026 [P]. https://peersense.com/best-mezzanine-lenders-2026
- Marks Paneth. Valuation discounts applicable to real estate holding companies [P]. https://www.markspaneth.com/insights/industry/name/valuation-discounts-applicable-to-real-estate-holding-companies

**Peers and case studies.**
- NBIM. Investment mandate – Government Pension Fund Global (last amended 9 Dec 2025). https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/
- NBIM (3 Nov 2025). Review of Norges Bank's management of the GPFG. https://www.nbim.no/en/news-and-insights/submissions-to-ministry/2025/review-of-norges-banks-management-of-the-government-pension-fund-global/
- CalPERS board documents (2013, 2020). https://www.calpers.ca.gov/documents/201304-invest-item03c-03/download ; https://www.calpers.ca.gov/docs/board-agendas/202004/invest/item10a-04_a.pdf
- Morningstar DBRS (2025). Confirms CPP Investments at AAA. https://dbrs.morningstar.com/research/457796/morningstar-dbrs-confirms-cpp-investments-at-aaa-and-cppib-capital-inc-at-aaa-and-r-1-high-stable-trends
- Wikipedia (accessed 18 Oct 2026). Thames Water (summary of press reports). https://en.wikipedia.org/wiki/Thames_Water

**Transfer taxes.**
- UK SDLT: https://gov.uk/stamp-duty-land-tax/nonresidential-and-mixed-rates
- Netherlands: https://www.deloitte.com/nl/en/services/tax/blogs/pakket-belastingplan-2026-aangenomen-door-eerste-kamer.html
- Germany: https://www.steuerschroeder.de/Steuerrechner/Grunderwerbsteuer.html ; https://www.aoshearman.com/de-de/insights/the-end-of-the-signing-closing-issue-the-new-rules-on-german-real-estate-transfer-tax-in-share-deals
- New York City: https://www.nyc.gov/site/finance/property/property-real-property-transfer-tax-rptt.page
- Los Angeles: https://www.hansonbridgett.com/publications/260812_7087_ula-ordinance-updates
- Saudi Arabia: https://zatca.gov.sa/en/MediaCenter/News/Pages/RETT-Implementing-Regulations.aspx
- Dubai and Abu Dhabi [P]: https://www.propertyfinder.ae/blog/dld-fees-dubai/ ; https://www.bayut.com/mybayut/fees-buying-property-abu-dhabi

**Internal.** `research/00_SYNTHESIS.md` (§2.3, §4.2–4.7); `research/groups/01_GROUPS_SYNTHESIS.md` (§2–4); `design/00_DESIGN_BRIEF.md` §8; `research/dossiers/06_leverage.md`, `08_action_valuation.md`, `05_secondaries_navfin.md`; `research/groups/dossiers/G2_secondaries_group.md`.
