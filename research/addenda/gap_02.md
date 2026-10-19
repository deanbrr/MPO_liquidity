# Gap 02 addendum: is the Tier-1 survival set feasible on the working book?

**One canonical stress, a joint T1–T9 study in six models, a priced tolerance frontier, a recovery mode and a regression test**

- **Date:** 2026-10-18. **Closes:** critic gap 02. **Amends:** `00_SYNTHESIS.md` §1 (finding 5, first 90 days), §2.3(d), §2.4, §4.8–4.9, §5.3 (G0), §10; C1 T1.4 and the C1 §5.7 cushion.
- **SYNTHETIC.** All balances, probabilities and costs come from the working allocation (context §1A, G7/GC2 census) and six **stylised proxy models**. They are not ADIC data.
- **Reproducibility.** `research/addenda/gap_02_calcs/` (fixed seeds): `gap02_study.py` → `gap02_frontier.py` → `gap02_premium_frontier.py` → `gap02_certify_extra.py`; `phase1_demo.py`; `pytest test_no_pinned_duals.py` (8/8 pass). Results in the `*.json` files there.
- **Tags** as in the synthesis; [I-calc] = computed here.

---

## 0. Answer in brief

1. **The headline "$3–19bn" is not a T4 result.** §2.3(d) took it from C3's mild DB→SG→SG path (net private flows −$4.5bn, 0, 0; facilities at 80%; 8% floor unusable).
   - T4 as specified needs **$25–92bn of committed facilities (14–52% of NAV)**, depending on the reading [I-calc]; the critic found $30–90bn and GC2 $25–42bn.
   - That exceeds T5's debt limits ($17.7bn / $26.6bn at today's NAV; $11.6bn / $17.4bn on the stressed month-24 NAV of $116bn) and the market precedent of a $15bn revolver for an A1/A+ sovereign fund (PIF, August 2024) [S].
2. **Most of the spread is conventions, not severity.** With the conventions fixed (§1.1), literal-severity T4 needs **$32bn**. The canonical stress s\* needs **$13.9bn** on the do-nothing book, **$6.1bn** with stage-triggered pacing cuts, and **$0** with owner-agreed band use (§1.3).
3. **Literal T4 lies outside the ensemble.** Its 24-month funding gap is exceeded by no more than 1 in 10,000 paths in M1–M5 and sits at P99.87 in the stressed model M6. s\* is calibrated to the **worst-model quantile matching T6's 24-month share**, so the deterministic row and the probabilistic gate say the same thing.
4. **The binding gate is T6, not T4.** From today's drought + Gulf-war state, ε_R = 1% per model is **reachable and certified in M1–M5**; below ≈0.8% it needs the owner-agreed band. **No mix in a 2,880-mix grid reaches 1% in M6**: its floor is 2.4% with the band (one-sided 95% Clopper–Pearson bound 2.5%, 50k paths) and 5–6% without. G7's single-model best (1.2%, which its verifier called optimistic) lies inside this range.
5. **Prices** (bp of NAV a year, M1–M5): the **CE price** of the 1% gate, against the certainty-equivalent-best mix without gates, is **8bp**. The cheapest certified mix has an exposure-neutral premium of **21bp with the band and 62bp without it**. Committed revolvers are the cheapest protection per dollar but capacity-capped; NAV facilities, pre-emptive amber sales and pre-emptive hedge-fund (HF) notices are dominated.
6. **Recalibrate, then guard.** T4 → T4′ = s\*(θ\* = 0.76), with literal T4 as a capacity-band reverse stress; T6 tolerance bands by model class; a Phase-I recovery mode that computes λ only from the restored problem; and a CI test that fails any decision card priced off a penalty-pinned dual.

---

## 1. One canonical named stress (item 1)

### 1.1 Conventions

| Item | §2.3(d) / C3 path | T4 (C1 T1.4) | G7 S1 | **Canonical s\*** | Basis |
|---|---|---|---|---|---|
| **Draw basis** | Fixed $17.7bn a year | Cap, basis unstated | 10% of opening NAV, fixed for 24 months | **10% of opening-of-fiscal-year reported NAV, annual reset** (year 2 ≈ $12.2bn) | §4.7 $D_y=d_yB_y$; §9.3 working assumption |
| **Facility credit** | 80% | 50% | 75% in crisis | **By instrument and horizon** (see list below) | Basel LCR40.82 [S]; Reg YY §252.35(a)(5)(iii) [S]; Ivashina–Scharfstein 2010; Chodorow-Reich–Falato 2022; Sufi 2009 |
| **IG + cash** | 8% unusable ($14.2bn) | 8% hard (T2) | Usable to 0 | **8% target (elastic, M^IG) + 4% hard (M^M)**, restored within 4 quarters of exiting stress | Basel LCR20.5 [S]; GC2 D10 |
| **Credit / Capital Solutions cash** | Netted inside −$4.5bn | Unstated | Crisis rates | **Private Credit 10%, Capital Solutions 7% of NAV a year** (cash yield and amortisation) | G7 crisis rates [I] |
| **Hedge funds** | Blended 22%, or 50% / 100% haircuts | Unstated | Time-to-cash ladder + flat 50% gate | **Whole book noticed at t0**, then queued (see list below) | OFR Form PF, 30 Jun 2026 [S→G7]; GC2 D1/D3 |
| **New commitments** | None | None | $12bn a year | **$12bn a year base** (a lever) | GC2 census |
| **Overlay** | Margin 3.5 / 1 / 1 | VM P99.5 | VM; IM 4%→10% | **$10bn synthetic beta**: VM on the shock; IM 4%→10%; tail-hedge monetisation; opportunistic loss 1.5% of NAV | GC2 D22 |
| **Shock timing** | — | Vertex | 6-month path | **Vertex**: the shock hits marketable assets at t0 | C1 T1.4 "worst case at a vertex" |

**Canonical facility credit.** 30-day rows (T3): 0% for every facility received. Committed unsecured revolver at 12–24 months: (1 − h_cpty) = 80%, provided covenant headroom holds under s\*, the syndicate has at least 10 banks with none above 12.5%, and a test draw happens yearly. NAV facility: the stressed loan-to-value (LTV) of 5% (10% normal) on a pledge pool capped at 20% of private NAV, less forced paydowns. Uncommitted lines: 0%.

**Canonical HF queue.** Form PF buckets are notice capacity; 30-day payment lag; 5% holdback; crisis pass-through 0.83 (GC2 state-machine P5), with 0.5 and 0 as brackets.

Why a rule rather than one flat factor: in 2008 banks that co-syndicated more lines with Lehman cut lending more, and new loans to large borrowers fell 47% in Q4-2008 [S]. About one-third of loans breached a covenant in 2008–09, and weaker lenders cut commitments after breaches [S]. Lines are reliable only with covenant headroom [S]. Hence the headroom and syndicate-concentration conditions.

### 1.2 Severity family and calibration

$$s^\*(\theta):\ \text{equity }{-}(30+10\theta)\%\text{ at }t_0;\ \ \text{PE/Sec/Co distributions}=0.45(1-\theta)\times\text{drought rates};\ \ \text{calls}=(1+0.5\theta)\times28\%;\ \ \text{24 months; cap draws for two fiscal years}$$

θ = 0 is a C3-type path (year-1 net private flow −$9.4bn here, because all five private groups and new commitments are included; C3 counted −$4.5bn); θ = 1 is literal T4 (−$18.7bn). The calibration statistic is the facility-free 24-month funding gap

$$G^\*=\max_{h\le24}\big[\mathrm{NCO}(h)+0.04\,W(h)-\mathrm{CBC}_{TP}(h)\big],$$

computed on every Monte Carlo path by an action-free ladder replica, starting in drought with Z₀ = GW at probability 0.7. **Rule:** θ\* sets G\*(s\*) equal to the worst model's quantile at 1 − ε₂₄, where ε₂₄ = 1 − (1 − ε_R)^{8/20} = 0.40% for ε_R = 1%. Result: **G\* = $11.1bn (M6, P99.6), θ\* = 0.76** [I-calc]. Alternatives: mixture P99.6 → $4.1bn (θ = 0.42); worst of M1–M5 at P99.6 → $2.6bn (θ = 0.35).

| Named stress (do-nothing book) | G\* ($bn) | Percentile M1 / M5 / M6 / mixture |
|---|---|---|
| C3-like (θ = 0) | −4.7 | 99.5 / 97.8 / 93.6 / 98.1 |
| G7 S1, canonical conventions | 0.0 | 99.9 / 99.2 / 96.4 / 99.1 |
| **s\*(0.76)** | **11.1** | >99.99 / 99.96 / 99.6 / 99.92 |
| T4 literal, canonical conventions | 16.1 | >99.99 / >99.99 / 99.87 / 99.98 |

**History supports this.** Across the dot-com and GFC downturns, buyout calls fell about 50% from peak to trough while distributions fell 60–82% (Preqin data on 844 buyout funds) [S]. Calls ×1.5 is therefore a practitioner stress ("capital calls double, distributions stop", Cambridge Associates, 2008 [S→G7]), not an empirical one. s\*(0.76) still carries calls ×1.38 because the family moves all components together; an IC preferring empirical calls can re-fit calls ×1.0 with lower distributions at the same G\*.

### 1.3 What each reading needs (do-nothing book unless stated)

| Reading | G\* ($bn) | Survival on T + P (months) | Facility for 24 months ($bn) | + stage pacing cut | + owner band | cut + band |
|---|---|---|---|---|---|---|
| **s\*(0.76), canonical (80% credit)** | 11.1 | 17 | **13.9** | 6.1 | 0 | 0 |
| T4 literal, canonical conventions (50% credit) | 16.1 | 15 | 32.2 | 18.7 | 4.3 | 0 |
| T4 as written (8% hard floor) | 20.7 | 12 | 41.5 | 28.1 | 14.7 | 1.3 |
| T4, critic reading (fixed USD, HF gated, no Credit/Capital Solutions cash, 8% floor) | 45.8 | 8 | 91.7 | — | — | — |

Single convention changes move literal T4 to $24.9bn (current-NAV draws), $42.9bn (fixed-USD draws) or $64.9bn (HF fully gated). **T2 as written already fails at t0.** Usable IG + cash excluding encumbered initial margin (IM) is $13.6bn, against an 8% requirement of $14.2bn: a shortfall of $0.56bn.

---

## 2. Joint T1–T9 study and minimum-cost mixes (item 2)

### 2.1 Set-up

**Engine** (`t1_engine.py`): quarterly, 5 years, 10k paths per model to screen and 50k to certify, from today's state. It extends G7's Monte Carlo with the G7 verifier's fixes: R3 (opening, annually reset draw basis), R5 (standby and upfront fees, regime-dependent availability, LTV-cut forced paydowns, owner cost) and R8 (P2S futures legs, capped at $15bn). It adds a gated HF queue, encumbered IM, owner overrides at 0.25–2% a year (C3), and front-loaded crisis returns (about −30% over 4 quarters, then a rebound).

**Six stylised proxies of the C1 ensemble.** CMA anchors are from dossier 10 §4.1 [S], with a 3.5pp PE fee haircut. M5 levels and M6's ACWI figure are [I] derivations (M6 from BlackRock's "risk premia rise" scenario: US large cap 2.02%, buyout 9.36% gross). Structures are [I].

| Model | 10-year ACWI / PE (net) | Structure | Crisis share | P(red event, 5y), do nothing |
|---|---|---|---|---|
| M1 | JPM 2027: 7.5% / 9.6% | Base | 14% | 7.8% |
| M2 | BlackRock, fee-adjusted: 9.0% / 12.4% | Base | 13% | 6.1% |
| M3 | AQR nominal: 6.6% / 6.6% | Base | 16% | 10.1% |
| M4 | JPM | Drought persistence 0.95 per quarter; Φ = 0.75 | 16% | 20.8% |
| M5 | JPM stagflation: 6.0% / 8.0% | Higher crisis entry; bonds fall with equities | 19% | 18.6% |
| M6 | BlackRock "risk premia rise": 3.0% / 5.9% | 6-quarter repricing; drought 0.93; calls do not fall in crises; margin outflows ×1.5 | 18% | 37.2% |

**Levers and prices** [I unless tagged]:

| Lever | Grid values | Pricing and constraints |
|---|---|---|
| Committed unsecured revolver | $0–20bn | SOFR + 85bp drawn; 15bp undrawn; 15bp upfront per 3 years. Anchor: an IG 2025 revolver at SOFR + 85bp with a 0.10–0.30% facility-fee grid [S, BXP 8-K] |
| NAV facility | $0 or $2bn | SOFR + 300bp, +140bp in stress [I/S]. Capped near $2bn by the 20% pledge limit |
| Pacing | $12bn, $9bn or $6bn a year, ± a stage-triggered cut to 25% | Cost beyond the horizon: 2 × (PE − liquid CMA) per $ forgone [unsupported G1 rate struck 2026-10-18; see Citation corrections] |
| Owner-agreed band | On/off | Draws at 5% in Red stage or crisis. Cost: the 10% accrual inside W̃ plus a 2% fiscal-stress premium |
| Reserve | 8–14% of NAV | Funded by selling developed-market (DM) equities |
| Pre-emptive amber sales | $0–6bn | At 89% / 85% of NAV. Private credit priced at 89% in H1-2026 [S→G7] |
| Pre-emptive HF notices | $0–5bn | — |

**Gates:**

| Gate | Test |
|---|---|
| T1/T7 | Clopper–Pearson (CP) bound on a 12-month payout shortfall ≤ 2.5% |
| T2 | 4% hard floor enforced in the engine; 8% restoration reported |
| T3 | Basel-capped LCR(30d) ≥ 1 |
| T4′ | s\*(0.76) headroom ≥ 0 |
| T5 | Enforced at decision time; passive drift reported |
| T6 | Red event, per model or mixture |
| T8 | DCR ≥ 1 for DB, GW and SG + PS |
| T9 | NAV-facility trigger ≤ 2%; revolver covenant at 25% debt/NAV ≤ 1% |

**Cost measures.** The *CE price* is the CRRA(3) certainty-equivalent growth of distribution-inclusive wealth, against the CE-best mix without gates, plus costs outside NAV. The *premium* is the expected gross outlay, neutral to exposure. They can disagree because CRRA(3) also credits the de-risking that the reserve and pacing levers carry.

### 2.2 Single levers (10k paths)

| Lever alone | P(red) M1 / M4 / M6 (%) | CE vs do-nothing, M1–M5 (bp/yr) | Premium (bp/yr) | s\*(0.76) headroom ($bn) |
|---|---|---|---|---|
| Do nothing | 8.2 / 21.2 / 37.3 | 0 | 1 | −11.1 |
| Revolver $15bn | 3.0 / 9.9 / 22.0 | −14.1 | 5 | +0.8 |
| NAV facility $2bn | 7.6 / 19.7 / 35.6 | +1.1 | 3 | −10.1 |
| Stage pacing cut | 2.4 / 7.3 / 21.2 | −15.2 | 18 | −4.9 |
| Pacing $6bn + cut | 1.5 / 4.8 / 17.1 | −10.1 | 28 | −3.2 |
| Owner band | 3.3 / 9.6 / 25.5 | +5.6 | 7 | +2.3 |
| Reserve 14% | 6.8 / 19.6 / 33.4 | −28.3 (mostly de-risking) | 28 | −7.9 |
| Amber sales $6bn at t0 | 7.1 / 19.0 / 34.8 | +7.5 | 10 | −6.6 |

### 2.3 Certified mixes (50k paths per model; one-sided 95% CP bounds)

| Target | Mix | Max CP P(red), M1–M5 | M6 P(red) | CE vs do-nothing, M1–M5 | Premium, M1–M5 | P(band used ≤ 12m) |
|---|---|---|---|---|---|---|
| ε_R 1%, **no band** | **A:** revolver $15bn; pacing $6bn + stage cut; reserve 14% | 0.98% (M5) | 5.8% | −32bp (CE price 8bp) | 62bp | — |
| ε_R 1%, **band** | **B:** revolver $10bn; pacing $12bn + stage cut; band; reserve 8%; $5bn HF notice | 0.79% (M5) | 6.5% | −8bp | 21bp | 12–22% |
| ε_R 0.5%, band | revolver $15bn; pacing $9bn + cut; band; $5bn HF notice | 0.45% (M5) | 4.6% | −4bp | 27bp | 12–21% |
| Mixture 1%, band | revolver $10bn; pacing $12bn + cut; band; reserve 14% | 0.39% (mixture 0.87%) | 4.5% | −30bp (CE price 9.5bp, mixture) | 54bp | 16–31% |
| M6 floor | revolver $15bn; pacing $6bn + cut; band; reserve 14%; $5bn HF notice | 0.15% | **2.4% (CP 2.5%)** | −21bp | 64bp | 12–21% |

Notes:
- Mix B withholds $3.2–7.0bn of draws in expectation over five years.
- The cheapest screened no-band candidate (revolver $20bn, reserve 12%) fails certification (CP 1.02% in M5).
- A and B pass T4′ with $11–12bn of headroom; A also passes literal T4 under canonical conventions, so in M1–M5 T6 is the binding row.
- Other gates in M1–M5: covenant risk ≤ 0.2%; T7 ≤ 0.01%; T3 2.7–5.0×; T8 ≥ 1.8. In M6 the large-revolver mixes without the band also fail T9 (covenant risk 1.6–2.4%).
- The CE-best mix without gates (revolver $10–15bn, stage cut, reserve 14%) already sits at 1.5–2.2% in M4–M5. The M1–M5 CE-price frontier is therefore 0.2bp at 2%, 8bp at 1%, 10bp at 0.5% and 14bp at 0.25%; the band is needed below about 0.8%.

**Recommended for IC discussion: Mix B if the owner agrees, Mix A otherwise.** Mix A buys the gate largely through reserve carry and slow pacing. Mix B buys it through the mandate, at a third of the premium. L4 is confirmed and now priced.

---

## 3. Frontier and recalibration (item 3)

**Frontier.** The ε_R–cost frontier is flat and cheap down to about 1% in M1–M5. It steepens below 0.8%, where it needs the band, and is vertical for M6 at about 2.4%.

**Per-model gates hand M6 a veto.** A per-model gate at tolerance makes the most pessimistic structure the binding one. The synthesis already rejects max-min for IC members (§6.5) for exactly this reason. M6 also stacks three stresses at once (repricing, persistent drought and overlay stress), so gating at 1% inside it double-counts stress.

Proposed bands (IC to ratify):

| Metric | Appetite | Tolerance (amber) | Capacity (hard; Board) |
|---|---|---|---|
| T6, base and drought models (M1–M5 class), per model | 0.5% | 1.0% | 2.0% |
| T6, mixture (IC weights) | 0.5% | 1.0% | 2.0% |
| T6, stressed structures (M6 class), per model | — | 2.5% | 5.0% |
| T4′ = s\*(0.76), canonical conventions | SH_TPF ≥ 36m | ≥ 24m (hard row in H and F) | — |
| T4 literal (θ = 1) | — | — | Reverse stress; Board item if SH_TPF < 24m |
| Critic reading / HF fully gated | — | — | Reverse-stress bound only |

Recalibrate θ\* annually with the same quantile rule. A tolerance breach triggers the CFP Amber playbook; a capacity breach triggers recovery mode. **Without the band, M6 breaches its capacity level** (5.2–5.8% against 5%), so ADIC enters recovery today unless the owner agrees, or until pacing works through (1–4 years [S→G1]).

---

## 4. Phase-I / recovery mode (item 4)

**Why penalties fail.** For an elastic row (max c′x − Mu s.t. a′x + u ≥ b, u ≥ 0), LP duality gives 0 ≤ y ≤ M and complementary slackness gives u\* > 0 ⇒ y\* = M. A structurally infeasible row therefore prices at its tier (M_S = 10², against a marginal utility of wealth of ≈1), and the kernel denominator π^H − M turns negative. An ℓ₁ penalty is exact only for M > ‖λ\*‖∞ (Nocedal–Wright 2006, Thm 17.3); with no feasible point, no finite M is exact and the solver returns an infeasible stationary point (eq. 17.27).

**Phase I.** A lexicographic minimum violation by tier: the sum-of-infeasibilities Phase I of Boyd–Vandenberghe §11.4. Gurobi's `feasRelax` with `minrelax=True` implements both stages (minimum violation, then the original objective among minimum-violation solutions).

$$u^\*_{k}=\min\sum_{r\in\mathcal T_k}w_ru_r\ \ \text{s.t.}\ \ Ax+u\ge b,\ \ x\in\mathcal X_{\text{rev}},\ \ \text{T5/legal rows hard},\ \ u_{\mathcal T_j}\le u^\*_j+\delta\ \ (j<k)$$

- $\mathcal X_{\text{rev}}$ contains only reversible, non-red levers: facilities, pacing, a band *request*, reserve, amber sales and HF notices.
- **PE sales are excluded**, so the structural deficit u\* never presumes a fire sale.
- Phase I also reports an irreducible infeasible subsystem (IIS; Chinneck 2008) and the levers sitting at capacity.

**Phase II (restored problem).**

$$\max J(x)\ \ \text{s.t.}\ \ A_rx\ge b_r-g_{r,t},\quad g_{r,t}=u^\*_r\,(1-t/T_{rec})^+,\quad \text{no slack on pricing rows }r\in\mathcal R_c$$

- **λ comes only from Phase II.** Phase-I duals are shown to the IC as "infeasibility prices" and never written to the FTP curve or to cards.
- **Glide path:** T_rec defaults to 4 quarters, extendable to 8 with Board approval and withdrawn if a quarterly progress test fails. This mirrors Solvency II Art. 138 [S]: a plan within 2 months, restoration within 6 months (+3), and up to 7 years in exceptional market-wide conditions with quarterly progress reports.
- **Cushion:** $c_t=\min_{h\le24}\big[\mathrm{CBC}^{TPF}_{s^\*}(h)-\mathrm{NCO}_{s^\*}(h)-0.04W(h)+g_t\big]/W_t$. It is ≥ 0 on the glide path, so cushion-monotone pacing, leverage and top-up rules stay interior.
- **G0** replaces "every gate feasible under HOLD and static SAA" with: Phase I over the contract's reversible levers returns u\* = 0 for every hard row, *or* the contract is signed in RECOVERY with u\*, the IIS, the glide path and owner/Board sign-off. HOLD and static SAA remain controls.

**Demonstration** (`phase1_demo.py`). The T4 row's coefficients are finite differences of the ladder. Test funds carry a hold value of 95% of NAV.

| Reading | Elastic (penalty) solve | Phase I and restored solve |
|---|---|---|
| **Critic reading** | u_S = $23.0bn; **y = 100** (1,000 at 10× penalties); reservation price 0.9% of NAV, so bids of 88%, 80% and 70% all say SELL | u\* = $24.2bn (Mode B), $7.8bn (Mode H); restored y = 0.237 (amber sales marginal); reservation price 76.8%: SELL at 88 and 80, HOLD at 70 |
| **T4 as written** | Feasible only with every lever at its corner; y = 0.29; reservation price 74% | Mode B: u\* = $0.46bn once PE sales are excluded. Mode H: y = 0.065; reservation price 85% |
| **s\*(0.76)** | Met by a $13.4bn revolver; y_T4 = 0.011, y_IG = 0.072; reservation price 87.7% | The 2018 buyout fund at 88% is a marginal SELL, matching the report's 87.3% (§4.4) |

---

## 5. Regression test (item 5)

`test_no_pinned_duals.py` runs in CI on every H release (in production, on H's full dual set). It asserts:

1. **Detection.** If any pricing row r ∈ $\mathcal R_c$ has u_r > 0, or y_r ≥ (1 − 10⁻³)M_r, the card is invalid and the build fails. The critic-reading fixture must trigger this.
2. **Penalty invariance.** In the restored problem, duals and card actions are unchanged when every tier is multiplied by 10. Pinned duals scale with M; genuine prices do not.
3. **Reservation-price floor.** No card's reservation price falls below (1 − δ^crisis_max) × hold value: 0.60 on the fixture.
4. **Cushion.** c_t ≥ 0 on the glide path after restoration.
5. **Phase-I closed form.** u\* equals the residual gap with every reversible lever at capacity.

Status: **8/8 pass** on the fixture. In production, cards produced in recovery carry `priced_on: restored_problem` and the recovery-target hash.

---

## 6. Design implications

1. **§1 finding 5 and §2.3(d).** Replace "$3–19bn" with: "T4 as written is infeasible on the working book ($25–92bn of facilities); canonical s\* needs $13.9bn, $6bn with stage pacing cuts, or none with an owner-agreed band; the binding gate is T6."
2. **§4.9 table and C1 T1.4.** T4 → T4′ = s\*(θ\*), with the §1.1 conventions as hashed contract fields and the HF queue; T2 becomes 8% target / 4% hard; T6 gets the §3 bands; facility credit by instrument and horizon replaces "50% facility". C1 §5.7 takes the new cushion definition.
3. **Mandate (L4).** Ask for pre-agreed 5% draws in Red stage or crisis. Disclose activation of 12–22% within 12 months and $3–7bn withheld over five years.
4. **First 90 days.** Request indications for **$10–15bn of committed unsecured revolving capacity** (3+2 years; at least 10 banks; covenant headroom tested under s\*), not generic "committed facilities". Adopt the stage-triggered pacing rule now. Drop the NAV-facility route (pledge-capped near $2bn).
5. **Owner draw convention.** Settle fixed-USD, opening-reset or current-NAV: that choice alone moves literal T4 between $25bn and $43bn.
6. **Agentic layer.** Add a G0 RECOVERY state, an infeasibility-price panel in the IC pack, and the regression test as an evaluator-owned rubric.

## 7. Limitations

The models are proxies, not engine E; draw targets come from shock type without an oil simulation; the search is a grid, not an optimiser. The pacing cost beyond the horizon, the owner premium, revolver availability and the 25% covenant are [I]. CE metrics reward de-risking, hence the second (premium) measure. M6's design sets the vertical part of the frontier; a milder stressed structure moves it left.

## Sources (accessed 2026-10-18)

**Market and regulatory**
- Gulf News (28 Aug 2024). *Saudi wealth fund PIF gets new $15 billion revolving credit facility*: 23 institutions, 3 + 2 years, A1/A+, replaces the 2021 $15bn facility. https://gulfnews.com/business/markets/saudi-wealth-fund-pif-gets-new-15-billion-revolving-credit-facility-1.1724830841938
- BXP, Inc. Form 8-K (event 28 Mar 2025): $2.25bn revolver, SOFR + 85bp, facility fee 0.10–0.30% (0.20% currently). https://www.sec.gov/Archives/edgar/data/1037540/000165642325000014/bxp-20250328.htm
- Rede Partners (18 Jun 2025). *NAV Financing Market Report 2025*: spreads 4–7%; secured 5.2%, recourse-light 6.6%. https://www.rede-partners.com/news-insights-database/nav-financing-report-2025
- AltamarCAM (30 May 2023). *Private Equity Cash Flows in Times of Upheaval*: Preqin data, 844 buyout funds; calls −50%, distributions −60–82% from peak to trough. https://www.altamarcam.com/?p=98739
- EIOPA Single Rulebook. Solvency II Directive 2009/138/EC, Art. 138. https://www.eiopa.europa.eu/rulebook/solvency-ii-single-rulebook/article-2225_en
- Basel LCR20.5 and LCR40.82; 12 CFR 252.35; OFR Form PF (30 Jun 2026); Jefferies (Jul 2026); Cambridge Associates (Oct 2008) [S→G7 verification log].

**Academic**
- Ivashina, V. & Scharfstein, D. (2010). Bank lending during the financial crisis of 2008. *JFE* 97(3), 319–338. https://corpgov.law.harvard.edu/2010/04/26/bank-lending-during-the-financial-crisis-of-2008/
- Chodorow-Reich, G. & Falato, A. (2022). The loan covenant channel. *JF* 77(1), 85–128. https://nber.org/papers/w23879
- Sufi, A. (2009). Bank lines of credit in corporate finance. *RFS* 22(3), 1057–1088. https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1057-1088..html
- Clopper, C. J. & Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4), 404–413. https://doi.org/10.1093/biomet/26.4.404 (the source of the CP bounds in §0 and §2).

**Optimization**
- Nocedal, J. & Wright, S. (2006). *Numerical Optimization*, 2nd ed., Springer, Thm 17.3, eq. (17.23). https://pages.mtu.edu/~struther/Courses/OLD/Other/LessOld/5630_11/NocedalAndWright/Chpt17.pdf
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*, §11.4. https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
- Chinneck, J. W. (2008). *Feasibility and Infeasibility in Optimization*. Springer ISOR 118.
- Gurobi Optimizer Reference Manual: `Model.feasRelax`. https://gurobi.com/documentation/9.5/refman/py_model_feasrelax.html

**Internal**
- `00_SYNTHESIS.md`; C1 §5.4/§5.7; C3 §5.1/§5.5/§5.7; G1; G7 and its verification log; GC2 D1–D24; critic script `t14_check.py`.

## Citation corrections (2026-10-18)

- §2.1, levers table, Pacing row: struck "G1's implied financing rate is ≈10.5–11% [I, G1]". The figure is unsupported: the G1 verification log (R1) shows it is the cohort engine's growth rate G restated, not a financing rate, and the groups report withdraws it (`research/groups/01_GROUPS_SYNTHESIS.md`, C11). The engine's pacing cost, 2 × (PE − liquid CMA) per $ forgone, is unchanged, so no result in this addendum moves.
- Sources, Academic: added Clopper & Pearson (1934), *Biometrika* 26(4):404–413, DOI 10.1093/biomet/26.4.404, for the Clopper–Pearson bounds used in §0 item 4 and the §2 gates and mixes. These bounds had no reference entry, the same gap the audit found in G7 (`research/literature/00_LITERATURE_SYNTHESIS.md` §2.5; metadata as confirmed on Crossref in `research/literature/G7_liquidity_ladder.lit.md` §2).
