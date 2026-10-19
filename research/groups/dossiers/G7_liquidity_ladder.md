# G7 Dossier: Total-portfolio liquidity across the seven groups

**Ladder, stress behaviour and contingency funding for ADIC's endowment-model book**

- **Stream:** G7 (cross-group liquidity). Main-program streams 05 (instruments), 06 (leverage) and 08 (shadow price of liquidity) are referenced, not repeated.
- **As of:** 2026-10-18.
- **Evidence tags:**
  - **[S]** sourced; primary document fetched and read in this session.
  - **[S→0X]** sourced and verified by stream 0X or cluster C1; cited through that dossier.
  - **[P]** practitioner consensus.
  - **[I]** our inference or design choice.
  - **[I-calc]** computed on the synthetic book by the G7 script.
  - **[nrv]** classic reference from memory, not re-verified.
- **Synthetic data.** All ADIC balances are the working allocation of context §1A plus G7 splits. They are **SYNTHETIC** and must never be presented as ADIC data.
- **Reproducibility.** `research/groups/addenda/G7_calcs/g7_liquidity_ladder_calcs.py` (fixed seeds) writes `g7_liquidity_ladder_results.json`. Every [I-calc] number comes from that file.
- **Process note.**
  - The session's web-search quota was exhausted when this stream began. Evidence came from fetching primary documents directly (regulators, CPP, CalPERS, NZ Super, the OFR Form PF API, MSCI, Lazard, Evercore, NBER, IMF, ESMA, EUR-Lex), with PDF text extracted locally.
  - Consensus.app was not authenticated and was not used.
  - Unverifiable items are flagged.

---

## 1. Executive summary

### 1. The binding risk is structural (12–36 months), not 30-day

**Short-horizon coverage is ample.**
- On the synthetic book, ADIC-LCR(30d) is **4.5×**, using Basel haircuts and a first-month crisis outflow. On cash, Treasuries and IG alone it is **1.9×** [I-calc].
- CPP reported a one-month LCR of **6.9×** against a 1.0× minimum at 31 Mar 2025 [S].

**The run-rate is the problem.** In today's distribution drought, the base case consumes **US$12.4bn** of liquid assets in 12 months [I-calc]:

| 12-month flow (base case) | US$bn |
|---|---|
| Owner draw at 7.5% | 13.3 |
| Calls, including new commitments | 13.4 |
| Private distributions received | 14.2 |

A 2008/2020-style demand bust, with the owner drawing at the 10% cap, needs **$36.7bn in 12 months and $54.1bn in 24** [I-calc].

### 2. Survival is achievable, but the price is the portfolio

Survival horizons in the demand bust (no facilities, no private sales) [I-calc]:

| Liquidity used | Survival | What it costs |
|---|---|---|
| Treasury alone | **3 months** | — |
| Treasury plus all Public Markets (long-only, plus hedge funds behind notice and gates) | **28 months** | The liquid share falls from 40% to **18% at 12 months** and **10% at 24 months** |
| Same, but the 8% IG + cash floor treated as untouchable | **14 months** | — |

The IC's question is less "can we pay?" than "what does paying do to the book?"

### 3. The binding horizon is 24 months, and failure is usually a slow burn

A 96-cell reverse-stress grid tests Treasury plus Public Markets [I-calc]:
- **12-month failures** occur only in extreme cells: equity −50%, distributions at no more than 30% of drought rates, a 10% draw, and calls of at least 1.25×.
- **24-month failures** occur in 60% of cells, even with only a −20% equity move. Examples:
  - distributions at 30% of drought rates with a 10% draw (cover 0.95);
  - distributions stopping with a 7.5% draw (cover 0.97).

This supports C1's 24-month named stress as the right Tier-1 test [S→C1].

### 4. Policy levers dominate asset levers

Monte Carlo on the synthetic book: 20,000 paths over 5 years, starting in drought [I-calc]. A red event is a liquidity-driven private sale or a payout shortfall.

| Policy | P(red event within 5 years) |
|---|---|
| No facilities | **18.1%** |
| Plus a $5bn committed revolver and a pre-arranged portfolio NAV facility | **11.5%** |
| Plus stage-based pacing cuts and early hedge-fund redemptions | **4.5%** |
| Plus owner-agreed draw flexibility (5% in crisis) | **1.5%** |
| Plus a 12% Treasury target | **1.2%** |

- No tested policy meets C1's ≤1% gate from today's drought start.
- **86–99% of first red events fall in crisis quarters after 2–4 years of drought depletion.**
- The drought loads the gun; the crisis pulls the trigger.

### 5. Report distributions, not a P99 scalar

- 12-month liquidity-at-risk (net need before management actions) [I-calc]:
  - mean $11.5bn;
  - **LaR95 $24.0bn**;
  - **LaR99 $33.9bn**.
- Show the IC LaR, survival by recourse tier and the liquid-share path.

### 6. Hedge funds are far less liquid than their label

Form PF data for qualifying hedge funds, 30 Jun 2026 [S]:

| Who can get out, and how fast | Share |
|---|---|
| Investors: ≤7 days | **8.4%** of NAV |
| Investors: 8–90 days | **27.3%** of NAV |
| Investors: more than 90 days | **64.4%** of NAV |
| Managers: portfolio liquidatable within a day | **41.2%** of gross assets |

- In 2008, gated redemptions "could take as long as several years" [S: Cambridge Associates].
- Model hedge-fund liquidity as a queue, not a bucket.

### 7. Uses co-move in the worst states

- **Owner draw.** A clipped option on the fiscal state [S→03].
- **PE calls.** They fall less than distributions [S: Robinson & Sensoy].
- **Credit lines.** Corporates draw them in a dash for cash: US C&I loans rose **$482bn in three weeks** in March 2020 [S: Li, Strahan & Zhang].
- **Margin.** Variation margin hits first [S→09].
- **Contractual items.** Cures and deferrals.
- **Gulf war.** 2026 shows "oil up" ≠ "owner flush" [S→03].

### 8. Deliverables (§6)

- a ladder data model;
- a simulation design;
- optimizer constraints:
  - hard 30-day margin coverage;
  - 3/12/24-month ladder rows;
  - a usable-buffer rule;
  - group budgets;
  - encumbrance and facility rules;
- survival-metric definitions;
- a four-stage contingency funding plan (CFP) with triggers, playbooks, decision rights and testing.

### 9. Governance

- Corporate Finance, which owns the Treasury function, owns the pool and the CFP [corrected 2026-10-18: was "a central Treasury"; organization user-confirmed].
- Groups hold liquidity budgets priced at the optimizer's ℓ.
- Secondaries and Capital Solutions quotes for ADIC's own actions run under conflict controls.
- Counter-cyclical dry powder deploys only in the Green or Amber stage.

---

## 2. Core concepts & theory

### 2.1 What liquidity risk means here

**CPP's definition [S].** Liquidity risk is the risk of unacceptable losses while obtaining funds to:
- (i) meet obligations as they fall due;
- (ii) fund new investments;
- (iii) rebalance in stress.

ADIC adds a fourth [I]: **(iv) honour the sovereign distribution without disorderly portfolio distortion.**

**Four layers [I]:**

| Layer | What it covers |
|---|---|
| Market liquidity | Time and haircut to convert an asset |
| Funding liquidity | Repo, revolver and NAV facility |
| Contingent liquidity | Calls, DDTL and revolver draws, VM/IM, covenant cures, owner draw |
| Policy liquidity | Distribution band, pacing, hedge budget |

**Unfunded commitments are written options: committed facilities extended to GPs.**
- Basel assumes 30-day drawdowns of 40% (credit facilities) and 100% (liquidity facilities) for undrawn commitments to other financial institutions (LCR40.64) [S→08].
- This is a conservative prior, to be replaced by ADIC's call history.

### 2.2 Ladder, counterbalancing capacity and survival

For scenario $s$ and horizon $h$ (months):

$$
\mathrm{NCO}_s(h)=\sum_{t\le h}(O_{s,t}-I_{s,t}),\qquad
\mathrm{CBC}^{R}_s(h)=\sum_{k\in R}\sum_{t\le h} q_{k,s,t}P_{k,s,t}(1-\eta_{k,s,t})+F^{R}_s(h),\qquad
\mathrm{SH}^{R}_s=\min\{h:\mathrm{NCO}_s(h)>\mathrm{CBC}^{R}_s(h)\}.
$$

| Symbol | Meaning |
|---|---|
| $O, I$ | Contractual plus behavioural flows |
| $q$ | Units monetisable per month, given time-to-cash (ttc), capacity and gates |
| $P$ | Path market value |
| $\eta$ | Execution haircut |
| $F^R$ | Facility capacity |
| $R$ | Recourse set |

Recourse sets nest by cost:
- **T** Treasury;
- **TP** plus Public Markets;
- **TPF** plus facilities;
- **TPFA** plus amber private sales (Private Credit, Capital Solutions);
- **ALL** plus red private sales (PE, Secondaries, Co-investment).

This is the bank maturity ladder with counterbalancing capacity. The IMF's framework reports the "cumulated counterbalancing capacity at the end of each maturity bucket" after haircuts and roll-over rates [S: Schmieder et al. 2012].

**Ratio forms [I]:**
- $\mathrm{LCR}^{ADIC}_h=\mathrm{CBC}^{R_h}(h)/\mathrm{NCO}(h)$.
- At 30 days, use Basel conventions:
  - inflows capped at 75% of outflows [S: LCR40];
  - no credit for received lines. Regulation YY bars a line of credit as a cash-flow source for horizons ≤30 days [S: 12 CFR 252.35(a)(5)(iii)], and Basel gives facilities held at other institutions a 0% inflow [S→06 verification].
- $\mathrm{LaR}_{\alpha,h}=q_\alpha(\mathrm{NCO}(h))$.
- Headroom-at-risk $=q_{1-\alpha}(\min_{t\le h}[\mathrm{CBC}-\mathrm{NCO}])$.

### 2.3 Buffers must be usable

- **Basel LCR20.5:** in stress "it would be entirely appropriate for banks to use their stock of HQLA, thereby falling below the minimum" [S].
- **UK LDI, 2022:** buffers proved "too low and less usable in practice than expected" [S→09].
- **ADIC's floor.** A hard 8% IG + cash floor is capital, not liquidity: the $15bn Treasury holds only ~$0.8bn above it. Synthetic demand-bust survival falls from 28 to 14 months if the floor is unusable [I-calc].
- **Design [I]:**
  - 8% *target* in normal states;
  - 4% *hard* minimum in stress;
  - a restoration plan;
  - consistent with C1's elastic IG + cash row [S→C1].

### 2.4 The pecking order is a two-dimensional merit order (cost × speed)

**Cost.**
- Stream 08 sorts sources by implied spread and capacity into a marginal-cost-of-liquidity (MCL) curve. ℓ equals the marginal source's spread [S→08].
- C1's merit order: buffer → liquid rebalancing → overlay de-risking → NAV facility → LP secondary → GP-led solution [S→C1].

**Speed (G7's addition) [I].**
- A source counts only at horizons it can reach. A cheap facility arranged from scratch in six months cannot meet a 30-day VM call.
- ℓ therefore has a **term structure**, steepest at the short end in crash states.
- Corporate analogues:
  - Bolton, Chen & Wang's double barrier [S→08/09];
  - the Miller–Orr (1966) cash band [reference verified 2026-10-18; reading not re-checked against the text], which argues for a Treasury *band* with replenishment, not a point target.

### 2.5 Spirals and joint states

**Mechanisms.**
- Margins and market liquidity are "mutually reinforcing" [S→08: Brunnermeier & Pedersen].
- Repo haircuts rose in the 2007–08 run in *bilateral* repo [S: Gorton & Metrick]. In tri-party repo, "the level of margins and the amount of funding were surprisingly stable for most borrowers", with a sharp funding drop at Lehman (Copeland, Martin & Walker 2014; abstract via Crossref) [corrected 2026-10-18: haircut spike scoped to bilateral repo].
- In March 2020 Treasury evidence "points to forced selling" by leveraged investors [S: Schrimpf, Shin & Sushko].
- PE funds are "liquidity providers (sinks) when market valuations are high (low)" [S: Robinson & Sensoy].

**ADIC's dangerous state is joint [I].** It combines:
- owner draw up (stream 03's demand-bust, supply-glut and Gulf-war states);
- distributions collapsing while calls continue;
- VM and IM spiking;
- secondary discounts widening;
- facilities shrinking;
- hedge-fund gates closing.

The generator must produce these as named regimes, not rely on unconditional correlations.

### 2.6 Liquidity management is managing a net option book [I]

**ADIC is short:**
- the owner's draw option [S→03];
- GPs' calls;
- managers' gates;
- lenders' availability (LTV, MAC);
- dealers' procyclical IM.

**ADIC is long:**
- commitment pacing;
- physical-to-synthetic conversion;
- tail-hedge monetisation;
- facility draws;
- secondary-sale timing (stream 08's optimal stopping);
- a request to use the 5–10% band, where the owner agrees.

Investors would give up ~2% of wealth to hedge once-a-decade illiquidity crises [S→09: Ang, Papanikolaou & Westerfield].

**Other lenses:**
- **Actuarial ruin:** survival horizon = time-to-ruin; Gerber–Shiu (1998) severity budgets [S→C1].
- **Queueing:** hedge-fund redemptions are served on notice dates; secondary-market throughput follows Little's law (Little 1961) [I]. The law is proved for strictly stationary processes, so use it for normal-state throughput only, not inside a crisis [I].
- **(s,S) inventory control:** replenishment of the Treasury band [nrv].
- **Supervisory control:** stage machine with hysteresis [S→C1].
- **Bank and insurance practice:**
  - contingency funding plans and funds-transfer pricing [S: SR 10-6; S→08: FSI 2011];
  - Solvency II's new liquidity risk management plan (Art. 144a) [S].

---

## 3. Methods/models and trade-offs

| Method | Delivers | Strengths | Weaknesses | ADIC role [I] |
|---|---|---|---|---|
| Deterministic maturity ladder | Gaps by bucket | Transparent; SR 10-6 "liquidity gap analysis" [S] | Single path | Data spine; reporting |
| Named stresses | Survival horizon by tier | Explainable; Reg YY requires market, idiosyncratic and combined scenarios over overnight, 30-day, 90-day and 1-year horizons [S] | Scenario choice | CFP; Tier-1 T1.4 |
| Ratios (ADIC-LCR, NSFR analogue) | 30d / 90d / 12m coverage; structural funding | Peer-comparable (CPP) [S] | Static; conventional haircuts | Limits; early-warning indicators |
| Monte Carlo liquidity-at-risk | Quantiles; P(red); fans | Joint states; path dependence | Model risk; rare events | Policy design (P) |
| Reverse liquidity stress | Breaking points | Blind spots. ESMA: it "starts from the identification of the pre-defined outcome" [S] | Many solutions | Annual IC item |
| Recourse LP / waterfall (09 §6.4E) | Pecking order; per-path ℓ | Consistent with the MCL curve | Needs cost curves | Inside the simulator |
| Stochastic program (H) with ladder rows | Actions; duals $\ell_h$ | Term structure of ℓ | Scale; dual noise | Decisions; stream 08 pricing |
| Time-to-liquidity vs liquidation cost | Asset-side liquidity | ESMA's two principal approaches [S] | Liability side separate | Bucket calibration |
| Hedge-fund queue model | Proceeds timing | Notice lags, gates | Term data | Public Markets sub-model |
| Secondary market-depth model | Concave proceeds | Finite depth | Thin data | Red-tier capacity |

**One data model feeds three uses, so the numbers reconcile [I]:**
- ladder plus named stresses → governance;
- Monte Carlo plus reverse stress → design;
- program rows plus duals → decisions.

---

## 4. Empirical evidence & current market data (dated, sourced)

### 4.1 Time-to-cash and haircuts by instrument

| Instrument | Normal | Stress | Source |
|---|---|---|---|
| Cash, T-bills, MMF | T+0 | An MMF "broke the buck" in 2008 | CA 2008 [S] |
| US Treasuries | T+1 sale; same-day repo; Basel L1 0% haircut | Mar-2020: 5y/10y book depth fell to ~**10%** of post-crisis averages; price impact rose **5–6×**; 30y bid-ask exceeded 6× its average. Leveraged forced selling. | Fleming & Ruela 2020 [S]; BIS Bulletin 2 [S]; LCR30 [S] |
| IG corporates | T+1 to T+3 | Basel L2A haircut **15%**; L2B (BBB−) **50%** | LCR30.43–45 [S] |
| DM equities | **T+1** (US, since 28 May 2024) | Basel L2B haircut 50% (eligible only if the 30-day stress price fall ≤ 40%). Model as market path plus 1–2% execution haircut. | SEC [S]; LCR30.45 [S] |
| Long-only commingled funds | T+0 to T+30 | Suspensions or in-kind payment; 2008 securities-lending collateral problems hit index funds | CA 2008 [S] |
| Hedge funds (investor terms) | ≤7d **8.4%**, 8–90d **27.3%**, >90d **64.4%** of NAV (Jun-2026). >90d was 53.9% at end-2019. | Gates; side pockets. Full exit could take "several years" (2008). Funds of funds were 43% of HF assets (Mar-2008). | OFR/Form PF API [S]; CA 2008 [S] |
| Hedge-fund portfolios (manager side) | ≤1d **41.2%**; 8–90d 15.9%; >90d **19.3%** (Jun-2026) | The mismatch protects funds, not LPs | OFR/Form PF [S] |
| PE and Secondaries LP interests | ~3–6 months: auction, signing, consent/ROFR, closing [P]. H1-2026: 87% of NAV average; buyout 91%; VC 79%; RE 68%; tail-end 25%+ discounts; deferrals in 26% of deals. High-quality buyout ~90%. | ~**27%** of processes failed or paused in H1-2026. H2-2008 average high bid **61%** (83.5% after public-market adjustment). Pre-YE-2008-NAV deals ~**40%** discounts (up to 50%+). MAC walk-aways. Some funds "given away". | Jefferies [S→08]; Evercore [S]; Lazard [S]; Cogent [S→05]; WilmerHale 2009 [S] |
| Private Credit LP interests | 1–4 months [P]; 89% of NAV (H1-2026) | IMF: fund liquidity tools untested in a severe run-off (paraphrased) | Jefferies [S→08]; IMF 2024 [S] |
| Co-investments | 3–9 months; GP consent [P] | Strip sales (H1-2026); deeper discounts [P] | [S→08] |
| Capital Solutions | 1–6 months via syndication or secondary [P] | PIK toggles cut cash yield [P] | None verified |
| Portfolio NAV facility | 6–12 weeks to arrange; spread mostly <5% over 3m Term SOFR; LTV mostly <25%; margins 4.8% secured / 6.1% recourse-light | LTV caps cut; spreads ~+140bp (as in 2022) | Lead time [P→05]; Proskauer [S→05/08]; Rede [S→08] |
| Overlay collateral | Daily VM; IM | Cash was **68.3%** of non-cleared VM received (end-2024; 80% in 2020). CCP VM must be cash. Non-cleared IM + VM $1.5tn; CCP IM $389.8bn. Mar-2020: IM >100% at some CCPs; same-day VM dominated. | ISDA 2026 [S]; FSB 2020 [S→09] |

### 4.2 Uses in stress

**1. Owner draw.**
- Stream 03's default rule makes the draw a vertical put spread on log oil: 5% floor above ~$64/bbl Brent, 10% cap below ~$31.
  - The rule is stream 03's inference, calibrated on the IMF's consolidated UAE breakeven of $44.8/bbl (2026) [S→03].
- SWFs pulled at least $46.5bn from managers in 2015 [S→03].
- In 2026's Gulf-war state, Brent was $126.55 (14 Oct) while UAE 2026 real GDP is put at −3.9% [S→03].
- Endowments cut payouts after losses: Yale cut 6.7% for FY2010 [S→02].

**2. Calls and distributions (MSCI global PE).**

| Year | Contribution rate | Distribution rate | Distribution/contribution ratio |
|---|---|---|---|
| 2017 | 31% | 24% | 1.2 |
| 2018 | 30% | 21% | 1.1 |
| 2019 | 28% | 18% | 1.0 |
| 2020 | 29% | 17% | 0.9 |
| 2021 | 39% | 27% | 1.1 |
| 2022 | 31% | 11% | 0.8 |
| 2023 | 27% | 9% | 0.7 |
| 2024 | 28% | 11% | 0.9 |
| 2025 | 29% | 11% | 1.0 |
| H1 2026 | 31% | **9%** | 0.9 |

- Source: MSCI Q2-2026 [S]. MSCI calls 9% "about one-third of the historical average". All private capital runs ~10–11% against a historical ~20% [S].
- Calls fall less than distributions [S: Robinson & Sensoy].
- Practitioners stress calls *upward*:
  - Cambridge Associates (Oct 2008) advised assuming calls "at or above their long-term average" and tested a scenario in which "capital calls double, and distributions stop" [S].
  - Partners Capital: "calls usually are accelerated … and distributions dry up" [S].
- **Not verified:** aggregate 2008–09 call and distribution rates. C1's crisis distribution yield of 5–10% of NAV remains an assumption [S→C1; I].

**3. Revolver and DDTL draws.**
- US C&I loans rose **$482bn from 11 Mar to 1 Apr 2020**, against a 45-year average weekly growth of 0.12% [S: Li, Strahan & Zhang]:
  - all of it came through drawdowns of existing commitments;
  - lending also rose ~6% in three weeks after Lehman.
  - The paper's own abstract attributes banks' capacity to meet these draws to coincident inflows from the Federal Reserve's liquidity programs and from depositors, plus strong pre-shock bank capital. An oil- or fiscal-specific ADIC stress may lack that backstop, so ADIC's own facility assumptions (tier TPF, policy B) should not rest on 2020 line performance [I] [corrected 2026-10-18: condition carried over from Li, Strahan & Zhang].
- All firms drew first; later only the highest-rated tapped markets [S: Acharya & Steffen].
- Direct-lending revolvers and DDTLs are assumed to behave alike. Default: 50% drawn in the first stress quarter [I].

**4. Overlay (stream 09 in depth) [S→09].** G7 adds three points [I-calc]:
- **Synthetic beta.** Freed cash becomes contingent VM. $15bn of futures lose $5.9bn of VM in our bust's first year, while tail-hedge monetisation recoups $2.8bn.
- **FX forwards.** Hedges on illiquid non-USD assets pay out in "USD-down" states. Australian super funds rank hedge rollover and settlement among their main liquidity drivers [S: ISDA 2026].
- **Initial margin.** IM steps from ~4% to ~10% of notional [S→09].

**5. Cures and deferrals.**
- LTV sweeps and cures tighten as NAVs fall [S→05/06].
- Deferred consideration "typically settles within twelve months" [S: Evercore]. It is a contractual outflow when ADIC buys and a receivable when ADIC sells.

### 4.3 Conditions, October 2026

- **Rates:** SOFR 3.89% (15 Oct). FOMC target range 3.75–4.00% (16 Sep). 10y UST 5.09% [S→06].
- **Volatility:** VIX 19.99; SKEW 168.6 (16 Oct) [S→09].
- **Distributions and constraints:** PE distribution rate 9% in H1 [S]. 53% of LPs say undrawn commitments limit new commitments [S→04].
- **Secondary market (H1):**
  - volume $118bn (Jefferies) or ~$124bn (Lazard) [S];
  - LP-led ~51% (Lazard) [S];
  - ~27% of processes failed or paused [S];
  - pensions and SWFs supplied 48% of LP volume [S→08];
  - GIC, CIC and KIC each ran ~$1bn sale processes [S→05, from search excerpts].
- **Oil and geopolitics:**
  - the Gulf war began 28 Feb 2026 and Hormuz was effectively closed;
  - the UAE left OPEC on 1 May;
  - the larger forward risk is a post-war oil-down state [S→03].

---

## 5. Practitioner/peer practice & case studies

**CPP Investments [S]: a multi-horizon LCR with a 1.0× floor, linked to leverage capacity.**
- An LCR limit governs short-term liquidity. Effective 1 Apr 2024 its horizon moved from **10 days to one month**.
- The ratio compares available cash and liquid assets with "CPP and investment obligations", calibrated to stressed outflows: **6.9×** (31 Mar 2025), up from 5.0× a year earlier, against 1.0×.
- It "acts as a minimum level of liquidity" and feeds the "strategic liquidity target".
- DBRS: liquid assets are mainly listed equities, money-market securities and marketable bonds, plus a $1.5bn unsecured facility at CPPIB Capital [S].
- Recourse leverage: 36% of net assets against a 45% limit [S→06].

**CalPERS [S]: track forecast accuracy and review the CFP yearly.** Its semi-annual Treasury and Liquidity report (17 Feb 2026) covers:
- LCR by fund in normal and stressed environments ("Level I liquidity" in a crisis);
- cash-flow forecast accuracy (90th percentile);
- the annual Funding Contingency Plan review (Jan 2026).

**NZ Super [S].**
- Describes itself as a "long-term, sovereign investor with low liquidity requirements".
- Uses derivatives because "closing the derivative position allows us to access an immediate source of cash".
- Its Reference Portfolio is 100% NZD-hedged.
- **Read-across [I]:** ADIC can borrow the derivative-liquidity logic, but not NZ Super's liquidity tolerance.

**NBIM and GIC.**
- NBIM's leverage cap is 5% [S→06].
- GIC ran a ~$1bn PE sale in 2025, ready to withdraw if bids fell short [S→05, search excerpts].
- Future Fund and GIC liquidity frameworks could not be verified.

**Endowments, 2008–09: never become the forced seller [S→05].**
- **Harvard [S]:**
  - endowment projected to fall from $36.9bn to ~$24bn;
  - $11bn of unfunded commitments through 2018;
  - distributions supplied 56% of FAS income;
  - Moody's warned commitments "may not be funded from previously expected distributions";
  - Dec-2008: $1.5bn taxable bonds at ~T+335–337.5bp (5.03%, 6.06% and 6.53%) plus $1bn tax-exempt, partly for swap terminations (liability $330.4m at Jun-2008).
- **Cambridge Associates (Oct 2008) [S]:**
  - normal time-to-cash: cash T+0; listed securities T+1–3; commingled funds T+0–30; hedge-fund LPs T+90–365–730; non-marketables T+5–10 years;
  - a credit line is "a liquidity insurance policy, with the annual commitment fee as the premium", yet lines "are not necessarily guaranteed to be available when needed".
- **Partners Capital (Q3 2023) [S]:**
  - "We budget for base level liquidity to fund 7 years of spending";
  - 40% illiquid becomes ~50% in a GFC-style shock before markdowns.
  - ADIC comparison [I-calc]: its $71bn of liquid assets, including all hedge funds, covers 5.3 years of draws at 7.5% and 4.0 years at 10%. Partners' rule would need ~$93bn (53% of NAV).

**UK LDI, 2022.**
- The Pensions Regulator's guidance (24 Apr 2023) expects [S]:
  - a ≥**250bp** market-stress buffer replenishable within five days;
  - an operational buffer on top (e.g. 100bp, for 350bp in total);
  - collateral met "within five working days";
  - documented waterfalls;
  - stress tests finding "how large a market move would trigger the next call".
- The FPC's ~250bp is ~170bp for a 1-in-100 five-day shock plus ~80bp for the 99.8th-percentile five-day shock over a 10-year look-back [S→06].

**Banks: the CFP template.**
- **SR 10-6 (17 Mar 2010) [S].** A CFP must:
  - "delineate policies to manage a range of stress environments";
  - identify stress events;
  - define severity stages;
  - assess sources and needs (gap analysis, stress tests);
  - pre-arrange contingent sources with "periodic testing";
  - set event-management processes;
  - monitor early-warning indicators and triggers.
  - Time buckets run "daily … out to weekly, monthly, and quarterly".
- **Addendum (28 Jul 2023) [S]:** "during times of stress, contingency lines may become unavailable". Test lines regularly and plan collateral mobility.
- **Regulation YY [S]:**
  - 30-day buffer;
  - overnight, 30-day, 90-day and 1-year horizons;
  - CFP triggers tied to minimum requirements;
  - operational simulations;
  - weekly collateral monitoring by entity and currency.

**Insurers.** Directive (EU) 2025/2 [S]:
- **Art. 144a** requires a liquidity risk management plan: short-term cash-flow projections, optional medium- and long-term analysis, and liquidity risk indicators.
- **Art. 144b** allows suspending redemption rights as a "last resort", for up to three months, renewable.

**Non-bank margin preparedness.** FSB (10 Dec 2024) made eight recommendations [S]:
- tolerance-setting and CFPs;
- "extreme but plausible" stress tests;
- diverse liquid assets;
- collateral operations;
- counterparty engagement.

**Australian super.** ISDA (Mar 2026) urges "early-warning indicators, stress testing, fire drills and actionable liquidity and default playbooks", plus repo and committed facilities [S].

**Synthesis for ADIC [I]:**
1. Multi-horizon coverage.
2. Usable buffers with restoration rules.
3. Pre-arranged *and tested* contingent sources.
4. Queue- and depth-limited hedge-fund and secondary liquidity.
5. Stages with pre-approved playbooks and clear decision rights.
6. Measured forecast accuracy.

---

## 6. Design implications for the ADIC framework

### 6.1 Placement

A deterministic **Liquidity Engine** sits beside the private cash-flow engine (04), the collateral ledger (09) and the owner-draw module (03). It feeds:

| Consumer | What the engine provides |
|---|---|
| E (scenario engine) | Ladder state |
| P (policy simulator) | Waterfall, chance constraints, stage machine |
| H (here-and-now program) | Ladder rows and group budgets; returns duals $\ell_h$ |
| F (safety filter) | Hard 30-day rows; usable buffer |
| IC pack | Survival, LaR, ladder heatmap, stage |

LLM agents may draft playbooks and parse term sheets, CSAs and LPAs. Deterministic code owns the numbers.

### 6.2 Ladder data model

**Buckets.** Time-to-cash is scenario-conditional. Committed credit lines count only beyond 30 days (from B3), never in 30-day ratios [S: Reg YY]. Repo against Treasuries is B0.

| Bucket | Horizon | Contents |
|---|---|---|
| B0 | T+0 | Cash, T-bills, MMF, overnight UST repo |
| B1 | 1–7d | Government bonds, DM equities, futures close-outs, listed options, tail-hedge monetisation |
| B2 | 8–30d | IG/HY bonds, commingled funds, EM equities |
| B3 | 1–3m | Quarterly hedge funds, pre-arranged NAV facility, opportunistic wind-down |
| B4 | 3–6m | LP-interest secondaries (PE, Secondaries, Private Credit, Capital Solutions) |
| B5 | 6–12m | Co-investment sales, structured secondaries, gated hedge funds |
| B6 | 12–24m | Lock-ups, side pockets, tail-end funds |
| B7 | >24m | GP-discretion distributions |

**Entities [I]:**

| Entity | Key fields |
|---|---|
| `Position` | group (one of 7 + Treasury), instrument, legal entity, currency, custodian, NAV (reported / economic, date), unfunded, vintage, GP, consent/ROFR, **counterparty type (external / intra-ADIC)** |
| `LiquidityProfile` (per regime) | ttc (min / mode / max), haircut (mean / sd), monthly capacity, gate probability and %, suspension flag, settlement lag, notice calendar, market-depth function |
| `Encumbrance` | pledged to (IM / NAV facility / repo / securities lending), amount, release, substitution |
| `Obligation` | owner draw, call, DDTL/revolver, deferred payment, VM, IM, debt service, LTV cure, fees; schedule or intensity; regime multipliers; currency; entity |
| `Facility` | committed, size, drawn, availability by regime, lead time, pledge pool, LTV/MAC, cost curve, last test draw |
| `CollateralEligibility` | per CSA/CCP: eligible assets, haircuts, currency, mobility days |
| `StageState` | indicators, thresholds, stage, hysteresis, actions |

**Rule:** intra-ADIC transfers (e.g. Secondaries buying a PE-group stake) contribute **zero** to CBC.

### 6.3 Default ladder parameters

All defaults are synthetic, to be replaced by ADIC data.

| Bucket (group) | Normal ttc (months) / haircut | Stress ttc / haircut | Capacity per month | Tier | Basis |
|---|---|---|---|---|---|
| Cash (Treasury) | 0 / 0 | 0 / 0 | 100% net of encumbered IM | T | [S] Basel L1 |
| UST (Treasury) | 0 / 0.5% | 0 / 2% | 100% | T | [S] Mar-2020; [I] |
| IG (Treasury) | 0 / 1% | 0 / 10% (Basel 15% as cap) | 50% | T | [S] LCR30 |
| DM equities (Public Markets, LO) | 0 / 0.2% | 0 / 1.5% plus market path | 50% | P | [S] T+1; [I] |
| LO fixed income | 0 / 0.5% | 0 / 5% | 50% | P | [I] |
| EM / small-cap commingled | 1 / 1% | 1 / 5%; suspension risk | 50% | P | [S] CA 2008; [I] |
| HF ≤7d / 8–90d / 91–365d / >365d | 1 / 4 / 12 / 24; 0% | Same; 50% gated in crisis | 80 / 25 / 10 / 10% | P | [S] OFR; [I] |
| Private Credit LP interests | 4 / 11% | 6 / 25% | 10% | A | [S→08]; [I] |
| Capital Solutions | 6 / 10% | 8 / 30% | 8% | A | [I] |
| Secondaries-fund interests | 6 / 10% | 8 / 35% | 6% | R | [I] |
| PE LP interests | 6 / 9% | 8 / 35% | 2% (~$1bn), capped by depth | R | [S→08] 91%; [S→05] 61% in 2008 |
| Co-investments | 9 / 15% | 11 / 45% | 3% | R | [P]/[I] |
| Committed revolver | From month 2 | 75% available | — | F | [S] Reg YY; [I] |
| Portfolio NAV facility | Lead 0 if pre-arranged, else 3 months; LTV 10% | LTV 5% | — | F | [S→05/06]; [I] |

### 6.4 Simulation design

- **Clock.** Monthly steps, with daily overlay sub-steps in stress (09). Quarterly decisions (H), as in C1.
- **State.**
  - Regime (K=4 plus exit factor) × oil/fiscal shock type (N, B, SG, DB, SS, GW) [S→03/C1].
  - Market paths.
  - Position NAVs (economic and lagged reported).
  - Unfunded commitments by group.
  - Hedge-fund redemption queue (requests, notice dates, gates).
  - Encumbrance ledger.
  - Facility balances and availability.
  - Treasury band.
  - Stage.
- **Flows by group:**

  | Group | Flow model |
  |---|---|
  | PE | Calls $\kappa_g(S,a)U$ plus stress add-ons (subscription-line clean-ups); distributions $\delta_g(S,x^{exit},a)\,$NAV (04) |
  | Secondaries | Faster distributions; deferred payments |
  | Co-investment | Exit hazard; follow-ons |
  | Capital Solutions | Coupons (PIK toggle) and repayments |
  | Private Credit | Net interest; repayments; revolver/DDTL spikes in DB states |
  | Public Markets | Income; queued hedge-fund proceeds |
  | Overlay | VM, IM, premia, monetisation, opportunistic P&L (09) |
  | Treasury | Interest, owner draw (03), debt service, cures |

- **Policy.** Either a stage-permissioned waterfall over §6.9, or the stream-09 recourse LP $\min_y\sum_k c_k(s)y_k$ subject to capacity and time-to-cash, which yields per-path $\lambda_t$.
- **Outputs.**
  - Survival horizon by tier.
  - LaR and headroom fans.
  - P(red), P(black), time to red.
  - Stage occupancy.
  - Liquid-share and IG + cash paths.
  - Group contributions.
  - $\ell_h$ by regime.
- **Rare events.** Importance-sample crisis transitions and report Clopper–Pearson (1934) bounds (C1 D12).

### 6.5 Survival metrics: definitions for the IC

| Metric | Definition | Default limit (IC to ratify) [I] |
|---|---|---|
| SH_TP(s*) | Survival under the 24-month named stress s*, recourse T + P, usable buffer to 4% | Green ≥ 24m; Amber 18–24; Red 12–18; Black < 12 |
| SH_TPF(s*) | Same, plus committed and pre-arranged facilities | ≥ 36m |
| ADIC-LCR(30d) | Unencumbered L1 + L2A + L2B after Basel haircuts ÷ 30-day stressed net outflow; inflow cap 75%; no lines | Hard ≥ 1.0; target ≥ 2.0 |
| ADIC-LCR(12m) | CBC_TP(12m) ÷ NCO_s*(12m) | ≥ 1.25 |
| LaR99(12m) | 99th percentile of 4-quarter net need before management actions | ≤ 0.8 × CBC_TP(12m) |
| P(red, 5y) | P(liquidity-driven PE / Secondaries / Co-investment sale, or payout below minimum) | ≤ 1% per model (C1 T1.6) |
| Time-to-red | First red quarter (median / IQR) | Report |
| Liquid share | (Treasury + LO + HF ≤ 90d) ÷ NAV, current and stressed | Green ≥ 28%; Black < 20% |
| Treasury band | (cash + UST + IG) ÷ NAV | Target 8%; hard 4% |
| Unfunded / liquid | U ÷ (Treasury + LO + HF ≤ 90d) | ≤ 0.75 (synthetic: 38/58.1 = 0.65) |
| Overcommitment | (private NAV + U) ÷ NAV | ≤ 0.80 (C1); synthetic 0.81 |
| Encumbrance | Encumbered ÷ liquid assets | ≤ 15% (06) |
| Distribution coverage | CBC_TP(12m) ÷ (12m draw + stressed net calls) | ≥ 1.5 |
| NSFR analogue | (Equity + term debt > 1y) ÷ Σ RSF_k A_k | ≥ 1.0 (06) |
| Group consumption LC_g | Stressed 12m net outflow attributable to group g | ≤ budget B_g |

### 6.6 What the ladder says about the synthetic book [I-calc; all synthetic]

**Named stresses (36-month ladder, US$bn).**

| Scenario | 12m need | 24m need | SH_T | SH_TP | SH_TP, 8% floor unusable | SH_TPF | Liquid share t0 → 12m → 24m | LCR(12m) TP / TPF |
|---|---|---|---|---|---|---|---|---|
| B0: drought continues, draw 7.5% | 12.4 | 22.8 | 14 | >36 | >36 | >36 | 40.1 → 35.8 → 32.6% | 4.6 / 5.5 |
| S1: demand bust | 36.7 | 54.1 | **3** | **28** | **14** | >36 | 40.1 → **17.6 → 9.5%** | **1.29 / 1.47** |
| S1 with CFP pacing cut | 35.5 | 50.4 | 3 | >36 | 15 | >36 | 40.1 → 18.6 → 12.8% | 1.33 / 1.52 |
| S2: owner draw at cap for 36m | 19.7 | 35.9 | 8 | >36 | >36 | >36 | 40.1 → 32.0 → 25.2% | 2.65 / 3.24 |
| S3: 2022-type rates/collateral shock, draw 5% | 13.0 | 20.6 | 12 | >36 | >36 | >36 | 40.1 → 33.5 → 31.0% | 4.07 / 4.92 |

- **S1 specification:** equity −39%; distributions ×0.3 for 18 months; calls ×1.25; draw 10% for 24 months; IM 4% → 10%.
- **S1 at 24 months:** CBC_TP/NCO = 54.9/54.1 = **1.01**.
- **ADIC-LCR(30d) at t0 = 4.5×** (1.9× on L1 + L2A). Numerator $29.6bn; net outflow $6.6bn:

  | 30-day outflow component | US$bn |
  |---|---|
  | Draw at cap | 1.47 |
  | Stressed calls | 1.34 |
  | Revolver/DDTL draws | 0.25 |
  | P99 VM | 1.76 |
  | IM spike | 0.90 |
  | Opportunistic loss | 0.89 |
  | Deferred payment | 0.38 |
  | Premium | 0.06 |
  | Less crisis distributions | −0.45 |

**Sources and uses by group, 12 months (US$bn; + = net source).**

| Group | B0 sources / uses / net | S1 sources / uses / net |
|---|---|---|
| PE | 6.31 / 8.26 / **−1.95** | 1.80 / 11.09 / **−9.29** |
| Secondaries (incl. $1.5bn deferred) | 2.77 / 2.36 / +0.41 | 0.95 / 2.66 / −1.71 |
| Co-investment | 1.68 / 0.44 / +1.24 | 0.41 / 0.60 / −0.19 |
| Capital Solutions | 1.04 / 1.00 / +0.04 | 0.54 / 1.35 / −0.81 |
| Private Credit (incl. revolver/DDTL) | 2.40 / 1.28 / +1.12 | 1.37 / 2.13 / −0.76 |
| Overlay | +0.2 | **−6.1** (VM −5.9, IM −0.3, opportunistic −2.7, tail hedge +2.8) |
| Owner draw | −13.3 | −17.7 |
| **Total net need** (incl. $0.18bn opex) | **12.4** | **36.7** |

Reading:
- In the drought the private book is roughly cash-neutral at $12bn/yr of commitments, so the liquid book funds the draw.
- In the bust, PE swings by $7.3bn and the overlay by $6.3bn.

**Monte Carlo: 20,000 paths, 20 quarters, starting in drought.** Uses the stream-04 regime matrix and a 3% quarterly owner fiscal-shock onset.

| Policy | P(red, 5y) [95% CI] | P(payout shortfall) | P(Treasury < 8%, any quarter) | LaR95 / LaR99, 4q ($bn) | Median of max illiquid share | Mean distribution-inclusive wealth ($bn) |
|---|---|---|---|---|---|---|
| A: no facilities; pacing $12bn/yr; draw 7.5% (10% in crisis/fiscal shock) | 18.1% [17.6–18.7] | 6.7% | 37.9% | 24.0 / 33.9 | 83.7% | 249.9 |
| B: A + $5bn revolver + pre-arranged NAV facility | 11.5% [11.0–11.9] | 5.2% | 37.9% | 24.0 / 33.9 | 83.7% | 250.2 |
| C: B + stage-based pacing cut (×0.25) + early HF redemptions | 4.5% [4.2–4.7] | 1.7% | 34.6% | 23.1 / 32.0 | 76.4% | 250.1 |
| D: C + owner-agreed draw of 5% in crisis/Red | 1.5% [1.3–1.7] | 0.44% | 31.3% | 19.9 / 25.3 | 76.3% | 250.4 |
| E: D + 12% Treasury target | 1.2% [1.1–1.4] | 0.29% | 15.8% | 20.0 / 25.3 | 76.1% | 250.0 |

**Sensitivities, P(red):**

| Change | Policy A | Policy D |
|---|---|---|
| Start in normal regime | 12.3% | 0.95% |
| Base draw 5% | 14.0% | 1.3% |
| Base draw 10% | 27.2% | 1.8% |
| Pacing $8bn | 14.1% | 1.2% |
| Pacing $16bn | 23.4% | 2.1% |

First red events: 86% (A) to 99% (C, D) fall in crisis quarters; median first red quarter 13–15.

**Lessons [I]:**
- Facilities, pacing discipline and owner-agreed band use do most of the work.
- A bigger reserve mainly buys floor compliance: P(Treasury < 8%) falls from 31% to 16%.
- Mean wealth varies by less than 0.2% across policies, so **the price of safety is low.** Forced-sale signalling and governance costs are ignored, which understates the benefit.

**Reverse stress (96 cells; T + P; no facilities).**
- **12-month breach:** 3 cells only, all with equity −50%, distributions ≤30% of drought rates, draw 10% and calls ≥1.25×.
- **24-month breach:** 58 of 96 cells.
  - Even at equity −20%, breaches occur with distributions at 30% and a 10% draw (cover 0.95), or with distributions stopped and a 7.5% draw (0.97).
  - With drought distributions unchanged, equity −20% always passes (cover 1.21–1.84).
- **Most plausible failure:** a deepening drought plus a moderate bear market over two years. The production engine should rank such worlds by KL-minimal tilting (C1).

### 6.7 Liquidity constraints for the optimizer

These extend C1 T1.3–T1.5 [S→C1] with group detail [I].

**(L1) 30-day margin coverage (hard; H and F):**

$$
\mathrm{HQLA}^{unenc}_t\ \ge\ \sum_b v_{b,S}H_{b,t}+v_{X,S}(X^+_t+X^-_t)+v_{e,S}e_t+\Delta IM^{stress}_t+O^{30d}_t-u^M_t
$$

- $O^{30d}$ includes: draw instalment, stressed calls, revolver/DDTL draws, deferred payments, debt service, cures.
- Credit lines are excluded.

**(L2) Ladder rows** for $h\in\{3,12,24\}$ under the named stress $s^*$ (vertex form, linear in holdings):

$$
\sum_k \phi_{k,s^*}(h)A_{k,t}+F_{s^*}(h)-\mathrm{NCO}_{s^*}(h\mid a_t)\ \ge\ -u^{L}_{h,t},\qquad
\phi_{k,s}(h)=(1-\eta_{k,s})\min\{1,\mathrm{cap}_k(h-\mathrm{ttc}_{k,s})^+\}\gamma_{k,s}
$$

- $\gamma$ is the gate pass-through; $F(h)=0$ for $h\le1$ month.
- Duals $\mu_h$ give the **term structure** $\ell_h$, which feeds stream 08's LAPV.
- $h=24$ with T + P + F is **hard** (the C1 T1.4 analogue). $h$ = 3 and 12 are soft, at a penalty tier between $M^S$ and $M^{red}$.

**(L3) Usable Treasury band:**
- $C+h^{UST}+h^{IG}\ge0.08W-u^{IG}$ (elastic, $M^{IG}$);
- $\ge0.04W$ (hard);
- restore to 8% within 4 quarters of stress exit.

**(L4) Group liquidity budgets (soft):**

$$
LC_{g,t}=\sum_{i\in g}\big(\kappa^{s^*}_gU_{i,t}+c^{s^*}_{i,t}-\delta^{s^*}_gV_{i,t}\big)\le B_{g,t}+u_{g,t},\qquad
\sum_gB_{g,t}\le\mathrm{CBC}_{TP}(12)-\text{draw}_{12}-\mathrm{VM}^{99}_{12}-\text{buffer}
$$

The dual of (L4) is group $g$'s liquidity hurdle.

**(L5) Encumbrance.**
- Encumbered ÷ liquid ≤ 15%.
- IM, pledged NAV and repo'd assets never count in (L1)–(L3).
- Collateral must be eligible under the receiving CSA/CCP.

**(L6) Facilities.**
- Draws ≤ availability$_S$.
- Chance constraint P(LTV > LTV^max within 12m) ≤ 2% (06).

**(L7) Hedge-fund queue.**
- Requests $r_{j,t}\le$ redeemable on notice dates.
- Proceeds arrive at $t+L_j$, scaled by gate state.
- SOS1 per dealing date.

**(L8) Pacing.**
- $(V+U)\le0.80W$ (C1).
- New commitments enter calls through the age curve (04).

**Probabilistic, verified in P:**
- P(red, 5y) ≤ 1% (T1.6);
- planned payout ≥ 97.5% over 12m (T1.7);
- P(SH_TP < 12m | regime posterior) ≤ 5%.

### 6.8 Objective terms and shadow prices

- **Recourse cost.** Add $-\mathbb E[\sum_t\sum_k c_k(S_t)y_{k,t}]$ (09) plus C1's lexicographic penalties. Add no separate "liquidity value" term; it would double count.
- **Dry powder.** Model scenario-contingent opportunity columns (e.g. Secondaries buying at stress discounts), enabled only in Green or Amber, so their value emerges endogenously. Stream 06 estimates ~20bp/yr for 5% of NAV deployed every ~8 years [S→06].
- **Funds-transfer pricing (FTP).**
  - Charge group $g$ $\sum_h\ell_h LC_{g,h}$ and credit liquidity it provides (better hedge-fund terms, Private Credit coupons).
  - Use marginal, maturity-matched rates, not "one average rate" [S→08: FSI 2011].

### 6.9 Two-dimensional pecking order (default)

| Step | Source (group) | Speed | Cost driver | Stress caveat |
|---|---|---|---|---|
| 1 | Treasury above 4% hard minimum | B0–B1 | ≈0 | Depth (Mar-2020) |
| 2 | Tail-hedge monetisation; opportunistic de-risking releases IM (Overlay) | B1 | Negative in stress | 09 monetisation rules |
| 3 | Physical-to-synthetic on DM equities (LO + Overlay) | B1 | Futures financing plus IM | Creates contingent VM |
| 4 | Other long-only sales | B1–B2 | Impact; crystallises losses | EM suspensions |
| 5 | Repo of Treasuries (B0); committed revolver (counted from B3) | B0 / B3 | Spread plus fee | Lines "may become unavailable" [S] |
| 6 | Hedge-fund redemptions | B3–B6 | Forgone HF alpha | Gates; queue |
| 7 | Pre-arranged portfolio NAV facility | B3 | SOFR + 300–600bp | LTV cuts |
| 8 | **Policy:** pacing cut; owner-agreed band use | 1–4 quarters | Forgone vintage α*; owner value | Owner decides |
| 9 | Private Credit / Capital Solutions sales or syndication (amber) | B3–B4 | Discount 11–30% | Buyer retreat |
| 10 | PE / Secondaries LP-interest sales (red) | B4 | Discount 9–35%; κ^GP | ~27% fail; MAC [S] |
| 11 | Co-investment single-asset sales (red) | B5 | Discount 15–45% | GP consent |

**Deviations [I]:**
- In Green markets, a planned tail-end sale, ranked by stream 08's liquidity index ℓ*, may precede step 5: selling from strength is cheaper.
- In a Gulf-war state with orderly equities, step 3 may precede step 2.

### 6.10 Contingency funding plan for the IC

Elements follow SR 10-6, Reg YY and the FSB [S]; content is [I].

**Structure:**
1. Scope.
2. Appetite and limits (§6.5).
3. Scenario library: B0; S1 demand bust; S2 owner-draw cap; S3 rates/collateral; S4 private-credit default wave; S5 Gulf-war volume shock; the annual reverse stress.
4. Stages, early-warning indicators (EWIs) and triggers.
5. Funding-source inventory: capacity, lead time, cost, documentation, last test.
6. Group playbooks.
7. Decision rights.
8. Owner, GP and counterparty communications.
9. Testing.
10. Reporting.
11. Post-event review.

**Stages.** Any hard trigger escalates. De-escalation needs two consecutive better readings.

| Indicator | Green | Amber | Red | Black |
|---|---|---|---|---|
| SH_TP(s*) | ≥ 24m | 18–24m | 12–18m | < 12m |
| ADIC-LCR(30d) | ≥ 2.0 | 1.5–2.0 | 1.0–1.5 | < 1.0 |
| Treasury ÷ NAV | ≥ 8% | 6–8% | 4–6% | < 4% |
| Liquid share | ≥ 28% | 24–28% | 20–24% | < 20% |
| LaR99(12m) ÷ CBC_TP(12m) | ≤ 0.6 | 0.6–0.8 | 0.8–1.0 | > 1.0 |

**Soft EWIs [I]:**
- **Markets:** P(crisis) > 0.5; VIX > 30.
- **Secondaries and financing:** LP pricing < 85% of NAV or failed processes > 35%; NAV-loan spread > SOFR + 700bp.
- **Private cash flows:** trailing PE distribution rate < 6%; calls ÷ distributions > 1.5.
- **Hedge funds, dealers and FX:** HF gate notices; dealer IM or haircut hikes; FX hedge roll costs.
- **Owner:** Brent below fiscal breakeven, or owner requests above plan [S→03].
- **Credit:** revolver/DDTL utilisation spikes; private-credit default or PIK rates.
- **Process:** forecast accuracy < 80%.

**Pre-approved actions:**

| Stage | Owner | Actions |
|---|---|---|
| Green | Treasurer | Normal pacing; dry-powder deployment within budget; quarterly test rotation; annual secondary sounding |
| Amber | CIO; IC informed | Daily reporting; cut new commitments to 25–50% of plan; pause new co-investments; file HF notices per queue plan; pre-position a secondary tranche (data room, advisers, reserve prices from 08); activate NAV-facility documents; arm monetisation rules; open owner dialogue on draw timing |
| Red | IC, weekly | Draw lines; physical-to-synthetic and long-only sales; monetise hedges; cut opportunistic book; launch amber sales; formal owner request to use the band; prepare PE strips at reserve; GP and counterparty communications |
| Black | CEO / Board / owner | Red sales; suspend non-contractual outflows; owner-level liaison; asset-backed financing |

**Decision rights:**
- Treasurer: Green and operational Amber.
- CIO: strategic Amber.
- IC: Red.
- Board and owner: Black and any distribution change.

**Testing** [S: SR 10-6; 2023 addendum; LCR30.15; ISDA 2026]:
- annual fire drill (tabletop plus quantitative);
- quarterly test draws or small trades on every facility and repo line;
- periodic monetisation of a representative slice of each Treasury and long-only tier;
- collateral-mobility tests;
- HF notice-calendar audit;
- annual secondary indication on a test tranche;
- owner-protocol test.

### 6.11 Governance: who owns the pool

**Corporate Finance, which owns the Treasury function [I; organization user-confirmed].** [corrected 2026-10-18: was "Central Treasury … reports to the CIO and IC"]
- Owns the pool, CFP, facilities, collateral and ladder.
- Independent of the return-seeking groups; the Treasurer holds Corporate Finance's seat on the shadow IC.
- Basel requires HQLA to be "under the control of the function charged with managing the liquidity" [S: LCR30.18]. Group-owned buffers fragment and double count.

**Groups.**
- Liquidity-consumption budgets $B_g$, set annually by the IC.
- Charged at $\ell_h$ (FTP); credited for liquidity provided.
- Secondaries and Capital Solutions hold a counter-cyclical dry-powder sub-budget, released only in Green or Amber.
- When their pricing intelligence informs ADIC's own SELL or REFINANCE decisions, it runs under conflict controls (context §1A):
  - independent quotes;
  - Corporate Finance owns the decision;
  - rationale is logged.

### 6.12 Calibration targets and data needs

**Calibration targets:**

| Target | Value | Source |
|---|---|---|
| HF investor-liquidity split | 8.4 / 27.3 / 64.4% | [S] |
| PE contribution rate | 27–31% | [S] |
| PE distribution rate | 9–11% drought; 17–27% normal/boom | [S] |
| LP pricing | 87% average, 91% buyout (H1-2026); 61% average high bid (H2-2008) | [S→05/08] |
| Failed or paused processes | ~27% | [S] |
| Revolver-draw spike in DB states | Comparable to Mar-2020 | [S] |
| Margin on peak days | VM ≫ ΔIM | [S→09] |
| Treasury market depth | Collapses in a dash for cash | [S] |
| Owner draw | At cap in DB, SG and GW states | [S→03] |

**ADIC must supply:**
- hedge-fund notice, gate and lock-up calendars;
- LPA transfer clauses;
- unfunded commitments by fund, with DDTL/revolver detail;
- 15+ years of call and distribution history (2008–09, 2020, 2022);
- encumbrance register;
- CSA/CCP eligibility;
- facility terms;
- the draw rule and its history;
- Treasury forecast vs actual;
- past secondary bids.

### 6.13 SPECIFICATION CARD

| Item | Specification |
|---|---|
| **Data fields** | `Position`{id, group, instrument, legal_entity, ccy, custodian, nav_rep, nav_econ, nav_date, unfunded, vintage, gp, consent/ROFR, cpty_type ∈ {external, intra}}. `LiquidityProfile`{regime, ttc_min/mode/max, haircut_mean/sd, cap_per_month, gate_prob, gate_pct, notice_calendar, settle_lag, depth_fn}. `Encumbrance`{pledged_to, amt, release}. `Obligation`{type, schedule \| intensity, regime_mult, ccy}. `Facility`{committed, size, drawn, avail_by_regime, lead_time, pledge_pool, ltv_max, cost_curve, last_test}. `Collateral`{venue, eligible, haircut, mobility_days}. `Stage`{indicators, thresholds, stage, hysteresis}. |
| **Core equations** | $\mathrm{NCO}_s(h)=\sum_{t\le h}(O-I)$. $\mathrm{CBC}^R_s(h)=\sum_{k\in R}\sum_{t\le h}qP(1-\eta)+F^R(h)$. SH $=\min\{h:\mathrm{NCO}>\mathrm{CBC}\}$. LCR$_h$ = CBC/NCO (30d: inflow cap 75%; no lines). LaR$_{\alpha,h}=q_\alpha(\mathrm{NCO}(h))$. Ladder row $\sum_k\phi_{k,s}(h)A_k+F(h)\ge\mathrm{NCO}(h)$, with $\phi=(1-\eta)\min\{1,\mathrm{cap}(h-\mathrm{ttc})^+\}\gamma$. Calls $=\kappa_g(S)U$ (+ DB add-ons); distributions $=\delta_g(S,x^{exit})$NAV; VM $=Nr$; ΔIM $=(m_S-m_{S'})N$; draw $=d(\text{fiscal state})\bar W$. |
| **Parameter defaults** | §6.3. HF split 8.4 / 27.3 / 64.4% [S]. PE call rate 28–31%/yr [S]. Distribution rates by group (PE / Secondaries / Co-investment / Capital Solutions / Private Credit): drought 11 / 18 / 9 / 12 / 16%; crisis 3.5 / 7 / 2.5 / 7 / 10% [I, anchored on S]. Secondary price normal 0.90, crisis 0.65 [S→05/08]. NAV-facility LTV 10% normal, 5% stress [I]. Futures IM 4% → 10% [S→09]. Draw 7.5% base, 10% in DB/SG/GW [S→03; I]. Treasury target 8%, hard 4% [I]. |
| **Liquidity terms and stress behaviour** | Treasury: B0–B1; small haircuts; depth risk. Long-only: B1–B2; market path + 1–5%. Hedge funds: queue + gates (50% in crisis). PE / Secondaries LP interests: B4; discount 9% → 35%; ~27% failure; consent. Co-investment: B5; 15% → 45%. Private Credit / Capital Solutions: B3–B4; 11% → 30%. Overlay: VM out on synthetic beta, in on hedges; IM ×2.5. Facilities: zero credit ≤30d; availability falls in stress. Intra-ADIC transfers count as zero. |
| **SELL / HOLD / REFINANCE / LEVER (liquidity lens)** | **SELL:** adds (1−η)Pq to CBC at the bucket's ttc; removes future inflows; transfers unfunded (relief ≈ κ^{s*}U). Worth it when bid ≥ LAPV(hold) at ℓ_h (08). **HOLD:** keeps δ inflows and κ outflows in NCO. **REFINANCE:** adds F(h) from lead time onward; adds debt service and cure contingencies; encumbers pledged NAV. Choose it when spread < ℓ over the effective life (C1: ρ > s). **LEVER:** raises NCO (calls/IM) and lowers CBC (encumbrance); allowed only if (L1)–(L4) still hold. **Group mapping:** HF redemption = queued SELL. Long-only physical-to-synthetic = SELL physical + LEVER synthetic (IM, contingent VM). Private Credit back-leverage = REFINANCE. Co-investment holdco financing = REFINANCE. |
| **Forecasts and biases** | Calls / distributions come from GP projections and the 04 regime model. The memo corpus shows distribution timing "repeatedly too optimistic" after spread shocks (deck), so apply regime-conditional haircuts and stress call add-ons. HF liquidity comes from contract terms; the bias is to ignore gates. The owner draw comes from 03 plus elicitation; the bias is to equate oil-up with low draws. Treasury forecasts: track accuracy (CalPERS reports the 90th percentile) [S]. |
| **Synthetic defaults** | NAV $177bn. Treasury: cash 6 / UST 4 / IG 5. Long-only: DM 22 / EM 6 / FI 8. HF 20 (Form PF split). Private Credit 14; Capital Solutions 8; Secondaries 14; PE 52; Co-investment 18. Unfunded 38: PE 26; Secondaries 2.5 + 1.5 deferred; Private Credit 2.5 + 1.5 revolver/DDTL; Capital Solutions 3; Co-investment 1. Synthetic beta $15bn; hedge notional $20bn at 0.4% NAV/yr; opportunistic IM $1bn; revolver $5bn (assumed); pacing $12bn/yr. **All SYNTHETIC.** |
| **Links** | 03: draw and shock types. 04: κ, δ, exit factor. 05: pricing, depth, NAV facilities. 06: leverage, encumbrance, covenants. 08: ℓ_h → LAPV; liquidity index ℓ*. 09: VM/IM ledger, monetisation, recourse LP. 10/C1: regimes, T1.3–T1.7, reverse-stress tilting. Group-specific G-streams in `research/groups/` (e.g. G4 co-investment): position terms and playbooks. 14: IC deliberation on the CFP. |

---

## 7. Implementation notes

**Libraries:**
- numpy, with numba or JAX, for vectorised paths (the G7 script runs 20k paths × 20 quarters × 5 policies in seconds);
- pandas for ladder tables;
- pydantic for the data model;
- cvxpy with HiGHS or Clarabel for the recourse LP and ladder rows;
- Pyomo with mpi-sppy for H (C1);
- scipy for Clopper–Pearson intervals;
- simpy or a custom event queue for hedge-fund notice calendars.

**Algorithms:**
- **Ladder:** cumulative sums over bucket × month, with capacity clipping.
- **Survival horizon:** first crossing.
- **Reverse stress:** grid or Bayesian optimisation over stress multipliers; KL-minimal tilting on Monte Carlo paths (C1/10); Glasserman–Kang–Kang (2015) conditional means [S→10].
- **Rare events:** importance sampling for P(red) ≤ 1%.

**Pitfalls:**
- **Double counting:**
  - intra-ADIC transfers;
  - the same asset in CBC and as collateral;
  - credit lines in 30-day rows;
  - stress haircuts plus stressed prices on the same move (separate the path from the execution haircut);
  - VM/IM netting errors.
- **Conventions:** mixing annual and monthly intensities (use $1-(1-x)^{1/12}$).
- **Timing:** within-month ordering (VM same-day, distributions lumpy).
- **Behaviour:** deterministic gates.
- **Information:**
  - smoothed (look-ahead) regime probabilities in triggers; use filtered ones;
  - stale reported NAVs as haircut bases; use economic NAV.
- **Market and penalty design:**
  - uncapped secondary depth;
  - penalty tiers that make red recourse look cheap.

---

## 8. Risks, pitfalls & limitations

- **Synthetic book.**
  - Results depend on assumed splits (Treasury mix, revolver, pacing, overlay) and regime parameters. They show mechanisms and magnitudes, not ADIC's position.
  - The Monte Carlo is quarterly, uses a capacity approximation for hedge funds, and has no owner elicitation.
- **2008–09 private cash-flow rates** are unverified; crisis multipliers are assumptions anchored on C1 and 04.
- **Behaviour dominates outcomes:** GP calls, gates, lenders ("lines may become unavailable" [S]) and the owner.
- **Secondary depth data** are surveys with survivorship bias: the ~27% of failed processes is missing from price data [S].
- **Joint-state model risk.** Oil–equity correlation flips by shock type, and duration fails in supply shocks [S→03].
- **Governance.**
  - Unusable floors become hidden constraints.
  - Stages without pre-approved actions stall decisions.
  - Buffer "fatigue" in calm years mirrors hedge fatigue.
- **Operations and legal.**
  - Collateral mobility, cut-offs and FX settlement; Mar-2020 VM was same-day [S→09].
  - LPA restrictions and MAC clauses [S: WilmerHale].
  - UMR status for overlay IM [S→09].

---

## 9. Open questions (what ADIC must supply or confirm)

1. **The draw rule.** Fixed USD, % of trailing NAV, or discretionary within 5–10%? Will the owner pre-agree band use in stress (policy D)? Is there an injection or deferral option?
2. **Treasury.** Its composition and the 8% definition (does it include encumbered IM?). Which committed facilities and repo lines exist, and when were they last tested?
3. **Hedge funds.** Terms by fund: notice, frequency, gates, lock-ups, side pockets, investor concentration.
4. **Commitments.** Unfunded by fund, with DDTL/revolver detail; deferred-payment schedules; GP sub-line usage.
5. **History.** ADIC's own call and distribution history for 2008–09, 2020 and 2022.
6. **Collateral.** Encumbrance register, CSA/CCP eligibility and UMR status.
7. **Overlay.** Synthetic-beta notional, FX-hedge book, opportunistic IM.
8. **Structure.** Legal-entity and currency layout, and any trapped liquidity.
9. **Appetite.** SH thresholds, the red-event ε, the Treasury band and group budgets.
10. **NAV facility.** Appetite for a pre-arranged portfolio facility: lenders and terms.
11. **Governance.** Corporate Finance's Treasury mandate, FTP in attribution and dry-powder rules.

---

## 10. References

Access date 2026-10-18 unless noted. [S] = fetched and read this session; [S→] = cited through the named stream dossier.

**Peer and practitioner**
1. CPP Investments (2025). *F2025 Annual Report* (p. 44; Note 10.1). https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-F2025-Annual-Report-English.pdf
2. Morningstar DBRS (18 Sep 2025). *Credit Rating Report: CPP Investments & CPPIB Capital*. https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-DBRS-Rating-Report-091825.pdf.pdf
3. CalPERS (17 Feb 2026). *FAC Agenda Item 5c: Treasury Analysis and Liquidity Status Report*. https://www.calpers.ca.gov/documents/202602-finance-agenda-item5c-00-a/download
4. NZ Super Fund. *Derivatives*; *Reference Portfolio*. https://www.nzsuperfund.nz/how-we-invest/actual-portfolio/how-we-add-value/derivatives/ ; https://www.nzsuperfund.nz/how-we-invest/reference-portfolio/
5. Cambridge Associates (Oct 2008). *Liquidity Considerations in Today's Environment*. https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2014/12/Liquidity-Considerations-in-Todays-Environment-Oct-2008.pdf
6. Miranda, S., & Patel, A. (Q3 2023). *Setting a Portfolio's Long-term Illiquidity Budget*. Partners Capital. https://partners-cap.com/wp-content/uploads/Setting-a-Portfolios-Long-term-Illiquidity-Budget-2.pdf
7. Harvard Magazine (Jul 2009). "Liquidity and Leverage." https://www.harvardmagazine.com/2009/07/liquidity-leverage
8. Harvard Magazine (Dec 2008). "Harvard Borrows $2.5 Billion." https://www.harvardmagazine.com/print/3822?page=all
9. ISDA (Mar 2026). *Managing Liquidity Risk: Opportunities and Challenges for Australian Superannuation Funds*. https://www.isda.org/a/RZtiE/Managing-Liquidity-Risk-Opportunities-and-Challenges-for-Australian-Superannuation-Funds.pdf

**Market data**
10. OFR Hedge Fund Monitor (SEC Form PF, qualifying hedge funds), liquidity series to 2026-06-30. https://www.financialresearch.gov/hedge-fund-monitor/categories/liquidity/ ; API, e.g. https://data.financialresearch.gov/hf/v1/series/timeseries?mnemonic=FPF-ALLQHF_INVESTORLIQUIDITYGT90_PERCENT
11. MSCI (Sep/Oct 2026). *Private Capital Benchmarks Summary Q2 2026*. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
12. MSCI (2026). *The distribution drought in private equity persists*. https://www.msci.com/data-and-analytics/private-asset-solutions/visualizations/the-distribution-drought-in-private-equity-persists
13. Lazard (2026). *Interim Secondary Market Report 2026*. https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf
14. Evercore (Jul 2026). *H1 2026 Secondary Market Review*. https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
15. Jefferies (Jul 2026). *Global Secondary Market Review* [S→08/05]. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
16. Beaudoin, T. A., Berrent, J. C., Evans, S. C., & Rothermel, S. (WilmerHale) (Mar/Apr 2009). "Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets." ABA *Business Law Today* 18(4). https://www.wilmerhale.com/-/media/files/wilmerhale_shared_content/files/editorial/publication/blt_ma09_secondarymarket.pdf
17. Unquote (26 Jan 2009). "Secondaries pricing dips to a five-year low" (Cogent) [S→05]. https://www.unquote.com/uk/news/85756/secondaries-pricing-dips-to-a-five-year-low
18. Proskauer (2026). *NAV Financing Market, Full Year 2025* [S→05/08]. https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025
19. Fleming, M., & Ruela, F. (17 Apr 2020). "Treasury Market Liquidity during the COVID-19 Crisis." *Liberty Street Economics*. https://libertystreeteconomics.newyorkfed.org/2020/04/treasury-market-liquidity-during-the-covid-19-crisis.html
20. Schrimpf, A., Shin, H. S., & Sushko, V. (2 Apr 2020). "Leverage and margin spirals in fixed income markets during the Covid-19 crisis." *BIS Bulletin* 2. https://www.bis.org/publ/bisbull02.htm ; SSRN record (2021), DOI 10.2139/ssrn.3761873

**Academic**
21. Robinson, D. T., & Sensoy, B. A. (2016). "Cyclicality, performance measurement, and cash flow liquidity in private equity." *JFE* 122(3), 521–543. DOI 10.1016/j.jfineco.2016.09.008; NBER WP 17428. https://www.nber.org/papers/w17428
22. Li, L., Strahan, P. E., & Zhang, S. (2020). "Banks as Lenders of First Resort: Evidence from the COVID-19 Crisis." *RCFS* 9(3), 472–500. DOI 10.1093/rcfs/cfaa009; NBER WP 27256. https://www.nber.org/papers/w27256
23. Acharya, V. V., & Steffen, S. (2020). "The Risk of Being a Fallen Angel and the Corporate Dash for Cash in the Midst of COVID." *RCFS* 9(3), 430–471. DOI 10.1093/rcfs/cfaa013; NBER WP 27601. https://www.nber.org/papers/w27601
24. Gorton, G., & Metrick, A. (2012). "Securitized banking and the run on repo." *JFE* 104(3), 425–451. DOI 10.1016/j.jfineco.2011.03.016; NBER WP 15223. https://www.nber.org/papers/w15223
25. Schmieder, C., Hesse, H., Neudorfer, B., Puhr, C., & Schmitz, S. W. (2012). *Next Generation System-Wide Liquidity Stress Testing*. IMF WP/12/3. DOI 10.5089/9781475502466.001 (the Crossref record adds two names; the PDF title page lists these five). https://www.imf.org/external/pubs/ft/wp/2012/wp1203.pdf
26. Brunnermeier, M., & Pedersen, L. H. (2009). "Market Liquidity and Funding Liquidity." *RFS* 22(6), 2201–2238. DOI 10.1093/rfs/hhn098 [S→08]. https://ideas.repec.org/a/oup/rfinst/v22y2009i6p2201-2238.html
27. Bolton, P., Chen, H., & Wang, N. (2011). "A Unified Theory of Tobin's q, Corporate Investment, Financing, and Risk Management." *JF* 66(5), 1545–1578. DOI 10.1111/j.1540-6261.2011.01681.x [S→08/09]. https://www.nber.org/papers/w14845
28. Ang, A., Papanikolaou, D., & Westerfield, M. (2014). "Portfolio Choice with Illiquid Assets." *Management Science* 60(11), 2737–2761. DOI 10.1287/mnsc.2014.1986 [S→09]. https://www.nber.org/papers/w19436
29. Nadauld, T., Sensoy, B., Vorkink, K., & Weisbach, M. (2019). "The liquidity cost of private equity investments: Evidence from secondary market transactions." *JFE* 132(3), 158–181. DOI 10.1016/j.jfineco.2018.11.007 [S→08]. https://www.nber.org/papers/w22404
30. Miller, M. H., & Orr, D. (1966). "A model of the demand for money by firms." *QJE* 80(3), 413–435. DOI 10.2307/1880728. Reference verified 2026-10-18 (Crossref; pages per Semantic Scholar, as Crossref gives only the first page), formerly [nrv]; the §2.4 reading was not re-checked against the text.

**Regulatory and official**
31. Basel Committee. *Basel Framework, LCR standard* (LCR20.5; LCR30.13–30.46; LCR40). https://www.bis.org/committees/bcbs/basel-framework/LCR/standard.pdf ; LCR40.64 [S→08]: https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30
32. Basel Committee (Sep 2008). *Principles for Sound Liquidity Risk Management and Supervision*. https://www.bis.org/publ/bcbs144.htm
33. FSI (Dec 2011). *Liquidity transfer pricing: a guide to better practice* [S→08]. https://www.bis.org/fsi/fsipapers10.htm
34. Federal Reserve et al. (17 Mar 2010). *Interagency Policy Statement on Funding and Liquidity Risk Management* (SR 10-6). https://www.federalreserve.gov/boarddocs/srletters/2010/sr1006.htm ; https://www.federalreserve.gov/boarddocs/srletters/2010/sr1006a1.pdf
35. Federal Reserve, FDIC, NCUA & OCC (28 Jul 2023). *Addendum: Importance of Contingency Funding Plans*. https://www.federalreserve.gov/newsevents/pressreleases/files/bcreg20230728a1.pdf
36. 12 CFR §252.34–252.35 (Regulation YY). https://www.law.cornell.edu/cfr/text/12/252.34 ; https://www.law.cornell.edu/cfr/text/12/252.35
37. ESMA (16 Jul 2020). *Guidelines on liquidity stress testing in UCITS and AIFs* (ESMA34-39-897). https://www.esma.europa.eu/sites/default/files/library/esma34-39-897_guidelines_on_liquidity_stress_testing_in_ucits_and_aifs_en.pdf
38. Directive (EU) 2025/2 (OJ 8 Jan 2025), Arts. 144a–144b. https://eur-lex.europa.eu/eli/dir/2025/2/oj/eng
39. The Pensions Regulator (24 Apr 2023). *Liability-driven investment* guidance. https://www.thepensionsregulator.gov.uk/en/document-library/scheme-management-detailed-guidance/funding-and-investment-detailed-guidance/liability-driven-investment
40. Bank of England (Dec 2022). *Financial Stability Report*; FPC (Mar 2023) record [S→09/06]. https://www.bankofengland.co.uk/financial-stability-report/2022/december-2022 ; https://www.bankofengland.co.uk/financial-policy-summary-and-record/2023/march-2023
41. FSB (10 Dec 2024). *Liquidity Preparedness for Margin and Collateral Calls*. https://www.fsb.org/2024/12/liquidity-preparedness-for-margin-and-collateral-calls-final-report/
42. FSB (9 Jul 2025). *Leverage in Nonbank Financial Intermediation*. https://www.fsb.org/2025/07/leverage-in-nonbank-financial-intermediation-final-report/
43. FSB (17 Nov 2020). *Holistic Review of the March Market Turmoil* [S→09]. https://www.fsb.org/wp-content/uploads/P171120-2.pdf
44. Cohen, C., Ferreira, C., Natalucci, F., & Sugimoto, N. (8 Apr 2024). IMF Blog on private credit. https://www.imf.org/en/Blogs/Articles/2024/04/08/fast-growing-USD2-trillion-private-credit-market-warrants-closer-watch
45. SEC (15 Feb 2023). T+1 settlement rule (compliance 28 May 2024). https://www.sec.gov/newsroom/press-releases/2023-29

**Internal** (program documents, not external evidence)
46. `inputs/00_CONTEXT_AND_PRIOR_WORK.md`; dossiers 02, 03, 04, 05, 06, 08, 09, 10; `clusters/C1_portfolio_math.md`; `research/groups/addenda/G7_calcs/`.

**Academic: entries added 2026-10-18** (literature audit: methods named in the body, and the tri-party repo source cited in §2.5. Numbered from 47 so refs 1–46 keep their numbers. Metadata confirmed via Crossref.)
47. Glasserman, P., Kang, C., & Kang, W. (2015). "Stress scenario selection by empirical likelihood." *Quantitative Finance* 15(1), 25–41 (online 10 Jul 2014). DOI 10.1080/14697688.2014.926019 [S→10]. Cited in §7.
48. Gerber, H. U., & Shiu, E. S. W. (1998). "On the Time Value of Ruin." *North American Actuarial Journal* 2(1), 48–72. DOI 10.1080/10920277.1998.10595671 [S→C1]. Cited in §2.6.
49. Little, J. D. C. (1961). "A Proof for the Queuing Formula: L = λW." *Operations Research* 9(3), 383–387. DOI 10.1287/opre.9.3.383. Cited in §2.6.
50. Clopper, C. J., & Pearson, E. S. (1934). "The use of confidence or fiducial limits illustrated in the case of the binomial." *Biometrika* 26(4), 404–413. DOI 10.1093/biomet/26.4.404. Cited in §6.4 and §7.
51. Copeland, A., Martin, A., & Walker, M. (2014). "Repo Runs: Evidence from the Tri-Party Repo Market." *Journal of Finance* 69(6), 2343–2380. DOI 10.1111/jofi.12205. Cited in §2.5.

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.4 item 14 and §2.5, plus its §2.3 WilmerHale correction (listed under stream 05; the same work is ref 16 here); `research/literature/G7_liquidity_ladder.lit.md` §2 (citation-integrity table and "Fixes for §10"). Metadata was re-confirmed via Crossref, with Miller–Orr's pages from Semantic Scholar and the WilmerHale byline from the publisher PDF. The barrier re-run (`research/groups/addenda/G4_barrier_rerun/RESULTS.md`), the 2026-10-18 re-check results and the §2.6 cross-file items touch no work or number in this dossier.

- §1.9: "A central Treasury owns the pool and the CFP" → Corporate Finance, which owns the Treasury function, owns them (synthesis §2.4 #14).
- §6.11: "Central Treasury … reports to the CIO and IC" → Corporate Finance, independent of the return-seeking groups, with the Treasurer's seat on the shadow IC (synthesis §2.4 #14; lit file, organizational mapping).
- §6.11 conflict controls: "Treasury owns the decision" → "Corporate Finance owns the decision", for consistency with the rename.
- §9 Q11: "Central-Treasury mandate" → "Corporate Finance's Treasury mandate".
- §2.5: Gorton–Metrick's haircut rise scoped to bilateral repo, and tri-party repo's "surprisingly stable" margins and funding added from Copeland, Martin & Walker (2014) (synthesis §2.4 #14; lit fix 4).
- §4.2(3): added Li–Strahan–Zhang's own condition (Fed liquidity programs, deposit inflows, strong pre-shock capital) and its [I] implication for ADIC's facilities (synthesis §2.4 #14; lit fix 5).
- §2.4: Miller–Orr "[nrv]" → reference verified (*QJE* 80(3):413–435, DOI 10.2307/1880728); the reading is still not checked against the text (lit fix 3).
- §2.6: years added for Gerber–Shiu (1998) and Little (1961), with the stationarity caveat on Little's law from its abstract (lit table, Little row).
- §6.4 and §7: years added for Clopper–Pearson (1934) and Glasserman–Kang–Kang (2015).
- §10 ref 16: untitled WilmerHale entry → Beaudoin, Berrent, Evans & Rothermel, "Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets", ABA *Business Law Today* 18(4).
- §10 ref 20: title "Leverage and margin spirals in fixed income markets during the Covid-19 crisis" and SSRN DOI 10.2139/ssrn.3761873 added.
- §10 refs 21 and 26–29: omitted titles added (Robinson–Sensoy, Brunnermeier–Pedersen, Bolton–Chen–Wang, Ang–Papanikolaou–Westerfield, Nadauld et al.), plus Nadauld et al.'s volume and pages, 132(3):158–181.
- §10 refs 22–23: truncated titles completed (Li–Strahan–Zhang "…: Evidence from the COVID-19 Crisis"; Acharya–Steffen "… in the Midst of COVID").
- §10 refs 21–30: missing pages and DOIs added throughout (lit fix 1); ref 25 notes that the Crossref record adds two author names.
- §10 refs 47–51 added: Glasserman–Kang–Kang (2015), Gerber–Shiu (1998), Little (1961), Clopper–Pearson (1934) and Copeland–Martin–Walker (2014) (synthesis §2.5; lit fix 2).
