# Gap 01 addendum: the group layer, folded into §2.2, §4 and §6

**Date:** 2026-10-18. **Closes:** critic gap 01, "group layer missing from `00_SYNTHESIS.md`".

**Companions:** per-group detail is in clusters GC1 and GC2, which the groups workflow consolidates into `research/groups/01_GROUPS_SYNTHESIS.md`. This addendum is self-contained and aligned with both as of 13:35, with one conflict flagged (private-credit LGD, §4).

**Inputs, read in full:** dossiers G1–G9 and their nine verification logs (G3, G4, G5, G7 verified after the 12:14 synthesis); clusters GC1, GC2; context §1A. Tags as in the synthesis.

**New computations [I-calc]** in `research/addenda/gap_01_calcs/`: `hf_ladder.py` (hedge-fund state machine, 20,000 paths); `t14_hf_swap.py` (GC2's T1.4 ladder with the state machine replacing G7's hedge-fund buckets; unswapped, it reproduces GC2 exactly).

> **SYNTHETIC – NOT ADIC DATA.** All figures use the context §1A working allocation.

## 0. Fold-in map

- §1 → §0 inputs (add G1–G9, GC1, GC2) and §9.1.
- §2 → §2.2 (replace the lens column), §2.3(b) (add the group table), §4.2 (add four engines).
- §3 → §4.4 (replace the PE-only library). §4 → §4.3.
- §5 → §2.1, §2.3(d), §4.6 ledger, §4.9 T3/T4, §1 finding 5, §9.2 item 6 (restate survival).
- §6 → §3 L1, §4.4, §4.11, §6.1. §7 → §6.1–§6.3 (replace the seats). §8 → §7.2, §8, §10 Phase 0.

## 1. Verifier must-fix ledger (applied throughout)

| Stream | Correction applied |
|---|---|
| G1 | **R1:** the pacing cut's "≈10.5–11% implied financing rate" is the engine's growth G restated; cost a cut as forgone net alpha after overlay beta replacement. **R2:** access penalties κ^GP are upper bounds (overstated ×1.3–2.6 buyout, ×1.8–5.0 VC). **R4:** stressed calls = λ(U − B^SL) + c^SL·B^SL. **R5:** "≈99% of FMV" is the price of credit GP-leds; PE single-asset CVs (SACVs) price 52% at par, 14% above, 34% below [S: Evercore, H1-26] |
| G2 | **R1:** ℓ is a per-period rate; against a deal NPV use the one-off L_s = π_{s,0}/π̄ − 1 ≈ 17.5–23.7%. **R2–R5:** θ_tail ≈ 0.78–0.83; hold a reserve iff p_S·E[(NPV_S − L_S)⁺] > carry + forgone NPV; accretion A₀ = (1 − p)N^ref; SACV σ 45–50% at β ≈ 2 [corrected 2026-10-18: β ≈ 2 is the 2018-WP figure of Boyer et al.; the 2021 version of the paper, published as *JF* 78(2):835–885 (2023), gives β ≈ 1.8 (1.9 with log returns), so σ_SA is somewhat below 45–50%; the inconsistency with σ_SA = 35% stands (G2 verification log, R5)] |
| G3 | **R1:** the break-even is ≈(1 + r_h)(1 + ℓ̄) − 1 over the capital outstanding: 13.3% at the 9/9/4 fallback, 8.3% at a 1.83% dual (GC1 D8), superseding the flat-ℓ 13% and the verifier's r_f-based 10.5%. **R2:** use loss-adjusted, cash-basis RoE (bank leverage 10.2% vs 9.25% unlevered; alternative lender 8.9%; −2.3% cash carry per $ of debt at 30% PIK); add a cash-carry constraint. **R3:** price ADIC's REFINANCE off LP-portfolio comparables, with per-fund consent flags |
| G4 | **R1–R5:** the bid comes from the buyer model (56–79% of NAV for an average asset); single-asset REFI breach risk is ≈50% (normal) / 63% (drought) with quarterly tests (62–73% if LTV were monitored continuously); LEVER raises drought wipe-out at exit from 7.0% to 22.8% (7.6% → 22.9% with G4's E3 write-off barrier, V ≤ 0.75D, applied at any time) [re-checked 2026-10-18: neither figure is changed by the Broadie–Glasserman–Kou sign fix; `research/groups/addenda/G4_barrier_rerun/RESULTS.md` §5]; post-recap hazard ≈×1.1 (OLS) to ×1.7 (IV) at φ = 0.25 [corrected 2026-10-18: ×1.4–3.4 is Bhardwaj–Gupta–Howell's effect for their average recap, which adds 84% to total debt; scaled linearly to recaps adding 25% debt it is ≈×1.1–1.7 (literature synthesis §2.4 item 2)]; CV elections and strips are GP-triggered offer events |
| G5 | **R1:** Form PF buckets are notice capacity, not cash, so cash comes from the terms τ (§5). **R2–R4, R8:** NAV-weighted leverage (multi-strategy 4.5×); separate P2S variables y^p2s and y^add; long-only Z(5y) 0.10 / 0.17; notices irrevocable; consents recorded in τ |
| G6 | **R1:** run-off only where ADIC controls reinvestment (SMAs; other funds only with waivers): ≈$0.8–0.9bn in year 1, not $2.2bn. **R2–R4:** λ* per wrapper (SMA loan sales beat HOLD in Normal and Tight); direct-lending recoveries 33–55%; PIK-cohort hazard ×1.3–1.7 vs ≈×9 in code, both reported (5-year P99 loss 12.2% vs 17.2%) |
| G7 | **R1–R3:** ADIC-LCR(30d) 2.1× with Basel caps, not 4.5×; SH_TP with the buffer usable down to 4%; both draw conventions shown |
| G8 | **R1:** bands are free for releases only; increases on binding rows are priced at the dual, with Σ_g a^k_g δ_g⁺ ≤ slack_k. **R2–R5:** no price floor (c_buf is a ceiling); contingent liquidity charged once; DVA in dollars; c_buf 1.5% (1–3%) |
| G9 | **R1:** PE unfunded/NAV is 0.53, above the steady state (0.37 normal, 0.24 drought). **R2–R6:** loss-consistent PD (§4); vintage α −0.05 a year; BGK's 2.6pp is symmetric; fund-level smoothing; LP-accessible actions only |

## 2. (a) Group engines and the cash-generation map

| Group | Engine | Corrected defaults [I unless tagged] |
|---|---|---|
| **PE funds** | RFT-TA cohorts plus G1 mechanics: subscription lines, GP NAV loans, CVs, extensions, recycling, explicit fees. MPC on exposure E = U + N^e | k_E clipped to the stage corridor; stressed calls 0.30–0.35 of U; unfunded $27.4bn |
| **Secondaries** | Three templates: purchased LP interest (V₀ = θN^ref); two-layer secondary fund (calls 45% a year; NAV peaks at ≈65% of commitment [S: Callan]); CV stake (median exit 4.5 years) | Deferred payables are hard outflows; Tier-1 calls tested at ≥1.0× |
| **Co-investment** | Deal engine: EV jump-diffusion, E = max(V − D, 0), write-off at V ≤ κD, monitored continuously (a quarterly simulation checks κD·e^{+0.5826σ√Δ}, σ the diffusive EV volatility; G4 barrier re-run, RESULTS.md §1); Weibull exits (k 1.447, η 7.70 years) × 1.3 / 1.0 / 0.5 / 0.3 by regime; recaps exogenous | Cause-specific hazards; entry leverage L₀ = 0.40 as a sensitivity |
| **Capital Solutions** | Monthly state machine {performing, PIK, amended, default, workout, redeemed}. Accrual q = CrΔ; cash = q(1 − a); C ← C + qa, with a ≤ ā(age) and a cumulative cap. NAV loan: B′ = B + (I − D)⁺ − σ(ℓ)(D − I)⁺, with default, maturity and extension. Redemption = max{κC, m^min·I₀ − Σcash, MW} | By regime (expansion / drought / crisis / recovery): PIK share 15 / 30 / 60–80 / 20%; loss-relevant default 1.0 / 2.5 / 6–8 / 1.5%; recovery ×1.0 / 0.9 / 0.7 / 1.0 |
| **Private Credit** | Cohort competing risks over {cash-pay, PIK, non-accrual, resolved, repaid}. Cash income = 1{C}·PcΔ(1 − π⁰); PIK income = 1{C}·PcΔπ⁰ + 1{P}·P(c + δ^PIK)Δ. h^def = φ·Φ(−ln ICR̄/σ_ICR)·ξ_t·e^{β′x}. Separate hazards for the PIK switch and for extension (a selective default; 0.2–0.6). Refinancing-driven CPR. DDTL/revolver draws U(1 − (1 − d)^Δ), with d = 15 / 20 / 30 / 60% (front-loaded in crisis). Wrapper layer: SMA, CEF, evergreen queue, listed BDC | LGD_DL 0.67 and PD_N 1.1% (§4). Hazards calibrated **by state** to Fitch's 47/41/8/4 event mix [S/C]. An evergreen holder receives E[min(1, c̄·NAV/ΣR)] × its request |
| **Public Markets** | Hedge funds: factor + put + skew-t + jumps, GLM smoothing, state machine (§5). Long-only: benchmark + tracking error; impact Yσ√(Q/V) up to a few % of ADV | Long-only net IR −0.05 |
| **Overlay** | §4.6 books, plus synthetic beta supplied to other groups | Synthetic beta $10bn at t0 ($15bn in stress) |

**Group-resolved §2.3(b)** (stream G7 engine, 12 months, $12bn a year of pacing; [I-calc], reproduced by G7's verifier):

| $bn | PE | Secondaries | Co-investment | Capital Solutions | Private Credit | Private book | Single 10% rate |
|---|---|---|---|---|---|---|---|
| Drought: distributions / calls / **net** | 6.31 / 8.26 / **−1.95** | 2.77 / 2.36 / **+0.41** | 1.68 / 0.44 / **+1.24** | 1.04 / 1.00 / **+0.04** | 2.40 / 1.28 / **+1.12** | 14.2 / 13.3 / **+0.86** | 10.6 / 10.4 / +0.2 |
| S1 demand bust: net | **−9.29** | −1.71 | −0.19 | −0.81 | −0.76 | **−12.76** | Crisis −2.7 |

**Reading.**
- Drought neutrality survives only because the four non-PE groups (+$2.8bn) offset PE (−$1.95bn).
- With calls stressed *up* (×1.25, Cambridge Associates' 2008 practice) and distributions ×0.3, the private book uses $12.8bn: ≈$10bn more than the §2.3(b) crisis column, which lets calls fall.

## 3. (b) Instrument library by group (replaces §4.4's table)

Only external counterparties raise liquidity. Every action is priced on the one kernel, and LEVER ≡ ADD + REFI.

| Group · lens | Instrument | Pricing rule / defaults | Time to cash · capacity | Regime availability | Consent | Encumbrance |
|---|---|---|---|---|---|---|
| PE · SELL | LP-led sale or strip; deferred consideration | Hedonic price on economic NAV: buyout 91%, tail-end ≥25% discount [S: Jefferies H1-26]. Crisis 0.80–0.84 of economic NAV [C]. Deferral: p^ce = φp_d + (1 − φ)p_d(1 + r_v)^−t_d | 3–6 months · ≤5% of depth per half-year; only the upfront share counts now | Success 0.75–0.85 / 0.6 / 0.4–0.5 [I, GC1 D6] | GP consent, ROFR | Buyer assumes unfunded |
| PE · HOLD | CV election | GP-triggered offer; sell iff cash price ≥ value of rolling | ≥30 days [S: ILPA] | GP decides | Status-quo option in 22% of CVs [S] | — |
| PE · REFI | LP-portfolio NAV facility (owned by Corporate Finance); preferred equity | SOFR+300bp (250–400); LTV 10–20%; stress +140bp. Preferred: 12% (14% in stress), 1.3× minimum multiple [I] | 6–12 weeks (0 if pre-arranged) | Availability 100 / 100 / 50% | Per-fund pledge consent | $3.3–20 of NAV per $ raised |
| PE · LEVER / **pacing** | Up-sized re-ups; commitment cuts | Add only if fused α̂ beats ℓ̄ plus charges. A cut costs forgone net alpha; cash returns 20% in year 1 and 40% (ERSRI) to 69% (engine) by year 4, then turns negative [S/I-calc] | 1–4 quarters | Corridor: Green 0.75–1.25×; Amber 0.25–0.5× with a protected core sleeve (GC1 D9) | Access bound | Vintage hole |
| Sec · HOLD | **Deferred payables** | Debt in the leverage budget, ≤10% of group NAV | Mostly ≤12 months [S: Evercore] | Hard outflow at 100% | — | Tier-1 outflow |
| Sec · ADD / SELL | Discount purchases; tertiary sales | Buy iff b* ≥ p^ce, after a 4.2–5.1% winner's-curse haircut | 3–5% of segment volume | Contingent budget only if discount > 20% **and** Tier 1 green **and** stage Green/Amber | Firewall | Deferral counts as debt |
| Co · SELL | **Single-asset sale** or strip | Bid = E_b[X]/(1 + y_b)^τ − tc, with y_b 20–25% gross. SACV prices (≈87% of volume above 90% of NAV [S: Lazard]) apply only to CV-grade assets | 3–9 months | Bid cut in drought and crisis | GP consent; partial-transfer flag | — |
| Co · REFI / LEVER | Pool facility; **SPV holdco PIK** | Pool: SOFR+450–750bp, LTV ≤10–20%. Holdco PIK 10–13% [I] (Verisure benchmark 5.625% cash / 6.375% PIK [S: IFR]). At 12% PIK and 25% LTV, IRR 6.0% vs 6.3% unlevered in drought, wipe-out at exit 7.0% → 22.8% [I-calc G4]; with the E3 write-off barrier (V ≤ 0.75D) at any time 7.6% → 22.9% (unchanged by the Broadie–Glasserman–Kou fix; G4 barrier re-run, RESULTS.md §5.2) | — | Normal and benign regimes only | Per-GP pledge consent | Junior; LTV ≤20% |
| CapSol · SELL | **Syndication**; secondaries | Sell down and keep fees: 31% of NAV lenders syndicate, about half of what they underwrite [S: Rede, Jun 2026]. Secondaries at the yield mark less 8–12% (normal) or 20–30% (crisis) [I] | At close to 6 months | Thin in crisis | Co-lender | — |
| CapSol · REFI / LEVER | Back-leverage; CFO | Loss-adjusted cash RoE; CFO senior ≈ SOFR+250–300bp at 35–45% LTV, 6–12-month lead time | D/E ≤ 0.5 | Arrange in benign/normal | P(LTV breach) ≤ 5% | ≤40% of the book |
| PC · HOLD | **Run-off switch** ρ = 0 | No discount; forgone value = V^reinv net of losses | SMA sleeve ≈$0.8–0.9bn extra in year 1 | By wrapper | GP controls CEFs in their investment period | — |
| PC · SELL | Loans; LP interests; BDC shares; evergreen tender | Loans at 0.99 / 0.96 / 0.85 of par [I]; LP interests 89% [S]; evergreen tenders prorated, ≈38% filled (5% cap ÷ ≈13% requests [S: VRC Q3-26]) | Days to 4 months | Queue in crisis | Evergreen manager | — |
| PC · REFI / LEVER | **SMA back-leverage**; fund leverage ≤1.0× | Start LTV ≤40–45% at a 65% advance rate, S+200–275bp; P(deficiency within 3 years) 1.0 / 3.0 / 12.8% (an upper bound). Lever only if EL < y_A − c_B ≈ 4.0% [S: Cliffwater YE-25 inputs] | Lender lead time | Lever in benign/normal only | SMAs only | Cure tail |
| PM-HF · SELL | **Redemption = queued SELL**; secondary | Redeem iff α̂^net + κ^reentry < ℓ̄(T^cash). Secondary discount 15–25% (quarterly funds, crisis) to 30–50% (gated funds) [I; Hedgebay S] | φ(P5): 19% by month 3, 55% by month 6, 66% by month 12 | Gates in crisis | Irrevocable notices; manager consent | — |
| PM-HF · LEVER | Portable alpha; **HF-TRS** | Net α > financing spread + CVaR, leverage, VM and mismatch charges; HQLA-only collateral | — | — | ISDA/CSA | Independent amount |
| PM-LO · REFI | **Physical-to-synthetic** | Cost per $ freed per year = (f̄ + α̂ + TC/τ)/(1 − m − b) + leverage and VM charges: 0.40–0.70% (normal), 0.80–1.11% (Jun 2026), 2.2–3.3% (stress) [I-calc GC2] | 1–7 days, inside the 1.30× exposure cap | Contingent VM | Tier B (cross-group) | IM |
| Overlay · SELL | Tail-hedge monetization | Monetize iff V(1 − ba) + λ^wΔL ≥ continuation value | 1–7 days | Pays in stress | — | Releases IM |
| CF · REFI | Revolver; repo; term debt | 0% credit in 30-day rows; a NAV loan beats a sale only if repaid within ≈2 years [C] | Up to 3 months | 50% availability in T1.4 | — | Fixed claims |

## 4. (c) Forward-basis translations for the FBE (§4.3)

The basis is the forward log return on nowcast economic NAV, net of fees. Shared bias priors (GC2 §4.6) are applied, and the forecast enters with precision 1/(κ_g²σ̂²), without a further Z multiplier [C].

| Group | Translation | Prior / checks |
|---|---|---|
| PE funds | Benktander credibility (as now). Use PME or direct alpha; report IRR with and without the subscription line [S: ILPA] | Timing slip +2–4 quarters (normal), +4–8 (drought) |
| Secondaries | V̂ = N^ref·e^{βr^m}·q·(1 − f), with N^ref rolled to closing. Use economic actuals (accretion removed). (1 + y_P) ≈ (1 + y_V)(θ/p)^{1/D}. Desk bids give a second, buyer-implied signal y^MKT | p 0.87, θ 0.95, D 3.4 years → y_P ≈ 11.9% at y_V 9% [I-calc] |
| Co-investment | Deal model → (μ, σ, τ). Add 1.5–2 years to the hold; shrink the exit multiple 50% toward entry and EBITDA growth 30% toward the reference class | Flags: growth above the reference P75; exit multiple above entry; leverage > 6× or ICR < 2.0×; near-term exit an implausible base case. GP effect shared with the PE fund (ρ 0.6) |
| Capital Solutions | **Contract plus kicker:** E[r] = y^cash + y^PIK + OID/WAL(S) + ρE[kicker]/WAL(S) − PD(S)·LGD(S) − δ^ext(S), with ρ ≈ 0.5. Losses apply once, to the accreted claim. Extension drag is annualized | Realized net ≈9–11% [S: Tactical Opportunities 10-Q; Böni–Manigart]; net alpha ≈0 once equity risk is priced [S: EFW] |
| Private Credit | **LAY = r̄^fwd + s + o/T_e − PD·LGD − fees**, with cash and PIK separated (PIK = 11.3% of interest income [S: Lincoln Q2-26]). **LGD_DL = 0.67:** post-default value is ≈33% for direct loans vs 52% for syndicated loans and 39% for HY [S: Fed FEDS Note, 23 Feb 2024, Fig. 15, KBRA DLD data] | **PD_N ≈1.1%,** so that regime-weighted PD × LGD equals CDLI's 1.0% long-run loss (shares 70/20/10, multipliers 1/1.5/3, crisis recovery ×0.7) [I-calc]. **Conflict:** GC2 (1.8%, LGD 0.40) and GC1 D16 (1.5%, 50% recovery) give the same ≈1.0–1.15% loss with a different split. The FBE anchors on LGD 0.67, the only verified direct-loan figure; SYN-ADIC-177 carries GC1's pair as a truth variant. Example: S+520, SOFR 3.89%, 1pt OID over 3 years, loss-relevant PD 2.2%, fees 1% → LAY ≈6.9%. Syndicated recoveries would understate the loss by ≈0.4pp a year |
| Hedge funds | r_f + β′E[F] + α̂ from a hierarchical posterior on de-smoothed residuals, net of pass-through fees (median 4.53%) and an effective incentive fee of ≈50% [S] | α priors: multi-strategy 2.0%; macro, credit, RV and trend 1.0%; equity long/short and event 0.5% |
| Long-only | CMA benchmark + (β − 1)·ERP + α̂, after a credit-beta term for fixed income | Net IR −0.05; Z shown for display only |
| Overlay | Opportunistic: Sharpe prior N(0.3, 0.25²), gated on a deflated Sharpe ≥ 0.95. Tail hedge: payoffs by named scenario | (VaR, ES) scored jointly [S: Fissler–Ziegel] |

## 5. (d) Hedge-fund liquidity-term state machine, in C1's transition and the ledger

**State (added to §2.1).** Per hedge-fund lot: X ∈ {LOCK, SOFT, OPEN, NOTICE, QUEUE, SUSP, PAY, SP, LIQ, DONE, TRS_TERM}; the outstanding request; times gated k; receivables; holdback; side-pocket units; and each fund's queue of other investors' requests R^oth. The terms τ carry `notice_revocable` (default false) and the transfer and pledge consents. The decision variable is the noticed share u^red, lodged only on notice dates.

**Transition at each dealing date:**
1. Other investors' requests: R^oth = NAV·clip(ρ_S + ρ₁[−r^rel]⁺ + ρ₂·1{p̂^gate > p*}), with the quarterly rate converted to the dealing frequency.
2. If R > gNAV, a gate is imposed: always if mandatory, otherwise with a logit hazard on regime, drawdown, the flow ratio, mismatch and leverage.
3. Payout: π = min(1, gNAV/R) only when a gate is imposed. Pay = min(qπ, γ^inv·B⁰), and payment is in full once k = K^max.
4. Suspensions and side pockets; cash (1 − h)·Pay after the payment lag, holdback after audit; liquidation pays 50/30/20% by months 3/12/36.

**Ledger (§4.6).** Hedge-fund sales are replaced by Σ_i(Pay^cash + SP + LIQ). The ladder rows use only **φ_i(h, S)**, the machine's P5 cash share by horizon h.

**HF-TRS.**
- **What is reported.** ADIC is reportedly considering up to $15bn of leveraged hedge-fund exposure via total return swaps with local banks, mainly on large multi-strategy funds, against an internal target of at least 10% [S: Hedgeweek, 12 Jun 2026, citing Bloomberg]. It is *under consideration*, not ADIC data; terms unknown.
- **How the engine treats it.** A TRS_TERM branch covers margin on reference-NAV moves, the independent amount (10% [I]) and bank termination. The sleeve adds no redemption liquidity.

**Ladder rows L1–L8 and the CFP** (G7, corrected):

| Row | Constraint |
|---|---|
| L1 = T3 | 30-day coverage on CF-controlled HQLA, Basel-capped, with facilities at 0%. Any slack escalates the stage |
| L2 | Ladder rows at 3, 12 and 24 months under s* = T1.4. The 24-month row on Treasury + Public Markets + facilities is hard. Duals give ℓ_h |
| L3 | IG + cash 8% elastic and 4% hard, restored within 4 quarters |
| L4 | Group budgets LC_g ≤ B_g |
| L5 | Encumbrance |
| L6 | Facilities, including forced paydowns |
| L7 | Hedge-fund notice dates; proceeds follow φ |
| L8 | Private NAV + unfunded ≤ 0.80W. The synthetic book is at 0.81 |

The CFP has four stages:

| Stage | SH_TP (months) | ADIC-LCR(30d) | Pre-approved actions |
|---|---|---|---|
| Green | ≥ 24 | ≥ 2.0 | — |
| Amber | 18–24 | 1.5–2.0 | Hedge-fund notices filed |
| Red | 12–18 | 1.0–1.5 | Lines drawn |
| Black | < 12 | < 1.0 | — |

**Results** [I-calc; SYNTHETIC]. Survival in months; [24-month facility need] where computed.

| Stress | Static haircuts / G7 buckets (G7 split) | State machine, G5 terms: P5 (P50) | Adverse terms P5 |
|---|---|---|---|
| C3 path, 8% floor unusable | 21.9 (22% haircut) / 18.1 (50%) / 11.8 (all gated) | **20.9** (21.3) | 17.8 |
| C3 path, usable to 4% | 26.5 / 22.7 / 16.3 | **26.0** (26.3) | 23.6 |
| G7 S1, fixed-USD draw | 17 | **21** | 18 |
| T1.4, fixed-USD draw | 12 [$42.0bn] | **15** [$40.6bn] | 14 [$46.1bn] |
| T1.4, current-NAV draw | 15 [$24.6bn] | **18** [$23.2bn] | 16 [$28.8bn] |
| T1.4, current NAV + CFP | 16 [$13.7bn] | **20** [$12.3bn] | 17 [$17.8bn] |

Settings: GC2's seven-strategy mix, full notices lodged at t0. Adverse terms add investor gates, semi-annual dealing (credit, event, RV) and hazards ×2.

**Sensitivities** (C3 path, 8% floor, P50):

| Change | Survival (months) |
|---|---|
| Gate hazard ×2 | 21.2 |
| Notices lodged at month 6 | 20.3 |
| Book 55% multi-strategy | 19.4 |
| $15bn HF-TRS (independent amount $1.5bn, VM $1.56bn) | 19.3 |

**Conclusions.**
- The static "all gated" case needs a book that pays nothing for a year. It is a reverse-stress bound, not the base case.
- The machine front-loads hedge-fund cash: $10.7bn by month 6, against $2.7bn under G7's buckets. That adds 3–5 months to SH_TP and moves S1 from Red to Amber, but cuts the 24-month facility need by only ≈$1.4bn.
- GC2 now takes SEC's more conservative split as its base; across both splits its range is $42–49bn / $25–31bn. G5's default terms land at or just below the low end; the adverse terms, which match SEC's one-year share, land toward the top.
- Hedge-fund terms therefore drive the stage metrics; the draw rule and the T1.4 vertex drive the facility need.
- P5 and P50 differ by ≤1 month, so ADIC's documents (τ) matter more than gate randomness.

## 6. (e) Quantity envelopes, dual prices and vintage FTP

- **Envelopes.** Λ^k_g = Σ_{i∈g} a^k_i(x*), from a pooled re-solve across sample-average-approximation replications, reported with ranges. Releases are free; increases on binding rows are priced at the dual, with Σ_g a^k_g δ_g⁺ ≤ slack_k. No band exceeds the Tier-A size (≈$0.44bn); up to +20% above the envelope is Tier B, beyond that Tier A; no ratchet.
- **State-contingent pacing.** P_{g,t} = P*_g·Π(1 − η_g(ℓ_t − ℓ̄)/ℓ̄), with η > 0 for PE and Co-investment and η < 0 for Secondaries and Capital Solutions.
- **Decision prices.** Current robust duals (HQLA and borrowing endogenous; no floor; λ_R the optimizer's dual): charge_i = Σμa − Σμc + λ_R·∂CVaR/∂x_i + λ_Lev·b_i + Σρ_kΔFloor^k, levied on each asset's liquidity tenor. The published FTP curve is an EWMA with a ±50% collar.
- **Performance charges.** Vintage-locked at origination; Corporate Finance holds the repricing mismatch. CLC_g = c_buf·Σ_hω_hO^stress_{g,h}, with c_buf = 1.5%: ≈$0.2bn a year ($38bn × 30–35% × 1.5%), charged once [I-calc GC2]. Contractual inflows (Private Credit, Capital Solutions) and Overlay crisis payoffs earn credits; Overlay margin use is charged.
- **Attribution in dollars.** DVA_g = Σ NAV_i(r_i − r^FB_i) − FTP_g^vint − λ_R·RC_g + CR_g. Every charge reappears in a TPA or Corporate Finance line.
- **E1 illustration** (unfloored) [I-calc G8]: duals 1.83% (crisis liquidity) and 0.81% (CVaR); charges 58–212bp; Private Credit's net α* of −41bp gives a zero budget; the tail hedge enters only at a 10.85% dual, so hedges are valued by liquidity plus enabling value (L5).

## 7. (f) Group-organized IC: seats and agenda (replaces §6.2; extends §6.3)

Seats are defined by mandate, not persona. AI seats flag but never vote. With 12 seats, the ≤40%-per-family rule needs at least 3 model families, with 4 as the target.

| Seat | Mandate | Replaces |
|---|---|---|
| CIO | Tier-2 objective J; α* vs funding baskets; coherence of the envelopes | New |
| CRO | Tier 1, robust floor, model ranges | New |
| Treasurer / CF, also the owner's advocate | Payout, CFP stage, FTP, facilities, collateral | Treasurer + Fiduciary Steward |
| PE, Secondaries, Capital Solutions, Co-investment and Private Credit heads | Group decision cards. The Secondaries pricing desk and the Capital Solutions quote function are firewalled | Private-Markets Underwriter |
| Public Markets head | Hedge-fund queue, P2S, manager credibility | New |
| Overlay head | Two briefs: convexity per unit of carry; deflated alpha and margin | Tail-Hedge + Opportunistic seats |
| Outside-View Forecaster | Base rates; drift between u, a and f | Unchanged |
| Red Team (independent challenger) | Strongest case against; conflicts between groups | Unchanged |

**Group-head seats** recuse on their own envelopes, are scored on total-portfolio regret rather than group P&L, and may challenge but never veto another group.

**Human agenda:**
- **A. Total portfolio:** stage, Tier-1 board, SH_TP, λ curve, mandate.
- **B. Group blocks,** ordered by the marginal-asset agenda: envelope use and priced requests above it, decision cards, net α* after charges, forecast information value (own reference class only, shown when n_eff ≥ 20).
- **C. Cross-group items:** internal transfers (zero liquidity; fair value on both legs), contingent budgets, desk quotes via the pricing committee, P2S and HF-TRS collateral.
- **D. Ballot,** after the locked blind pre-vote; minority reports; signposts.

**Decision rights (add to §6.1):** in-envelope deals by the group; up to +20% above the envelope by CIO + CRO; envelopes and FTP by the TPC/IC quarterly, with the methodology approved annually by the Board; internal transfers at Tier B (Tier A if ≥0.25% of NAV or conflicted).

## 8. (g) SYN-ADIC-177 in the Phase-0 plan (§10)

**Design.** G9's three-layer generator (world, sealed truth, observation), with GC2's and GC1's fixes.
- **Census v1.0:** ≈395 positions plus ≈1,500 loans and ≈250 overlay trades; $177bn of NAV. Unfunded $38bn: PE 27.4, Secondaries 3.9, Co-investment 1.5, Capital Solutions 1.2, Private Credit 4.0.
- **Truth fixes:** vintage alpha −0.05z a year; truncated or NIG shocks; α net of write-down drift; co-investment deals drawn from BJS Table 4 quartiles, P(MOIC < 1) ≈0.35–0.40 (GC1 D19); private-credit smoothing 0.5–0.7 (GC1 D17); private-credit loss pairs (LGD 0.67 / PD_N 1.1% and GC1's pair); hedge-fund τ calibrated to Form PF on its own definition; an optional HF-TRS scenario.
- **Labelling:** every row carries `is_synthetic` and the footer "SYNTHETIC – NOT ADIC DATA".

| Month | Deliverable | Gates |
|---|---|---|
| 0–1 | Schemas (τ consent fields, quote conflict flag, wrapper type); census; R0 snapshot; sealed truth store; labelling enforced in CI | V1–V2, V20–V23 |
| 1–2 | R1: 1,000 worlds × 40 quarters, with common random numbers across SELL / HOLD / REFI / LEVER | V3–V13 (V11: Form PF on its own definition; V12: regime-weighted loss of 0.8–1.2%) |
| 2–3 | R2: 200 history worlds; simulation-based calibration (SBC) and parameter recovery for the FBE, nowcast and bias model; time-travel scoring; regret vs oracle | V16–V19 |

**Phase-0 exit adds:** V16–V18 passed; regret against the oracle reported for each group; labelling audit at 100%.

## 9. Changes to the headline findings

- **Finding 5:** C3-path survival ≈21 months, not "12–22"; T1.4 SH_TP 14–15 / 16–18 months; facility need ≈$41–46bn / $23–29bn (G5 to SEC-like terms).
- **New finding:** the press-reported HF-TRS would cost ≈2 survival months and needs HQLA collateral.
- **§9.3 item 4:** each fund's τ is the decisive data request.

## Sources (new or load-bearing; full lists in the G1–G9 dossiers and their logs)
- Hedgeweek (12 Jun 2026). ADIC weighs $15bn leveraged hedge fund push via swap structures. https://www.hedgeweek.com/abu-dhabis-adic-weighs-15bn-leveraged-hedge-fund-push-via-swap-structures/
- Cai & Haque (23 Feb 2024). Private Credit: Characteristics and Risks. FEDS Notes. https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html. DOI 10.17016/2380-7172.3462.
- OFR Hedge Fund Monitor, Form PF data to 30 Jun 2026. https://www.financialresearch.gov/hedge-fund-monitor/
- Jefferies (Jul 2026). https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- Evercore (Jul 2026). https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
- Lazard (Aug 2026). https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf
- Rede Partners (Jun 2026). https://www.rede-partners.com/s/NAV-Financing-Market-Report-2026_FINAL.pdf
- Lincoln International (Q2 2026). https://www.lincolninternational.com/news/the-lincoln-private-market-index-earnings-growth-drove-a-q2-rebound-while-private-markets-became-more-selective/
- Cliffwater, CDLI release (19 Aug 2026). https://www.prnewswire.com/news-releases/private-credit-shows-resilience-in-cliffwater-direct-lending-index-data-302854703.html
- IFR (2025). Verisure Holdco PIK. https://www.ifre.com/ifr-awards/2332504/europe-high-yield-bond-verisure-holdcos-1bn-pik-notes
- CEBS (27 Oct 2010). https://www.eba.europa.eu/sites/default/files/documents/10180/16094/da61d4c3-3937-4612-9584-e6136cb98191/cebs18_Guidelines.pdf

*SYNTHETIC – NOT ADIC DATA (all [I-calc] figures).*

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2, the per-topic reviews in `research/literature/`, the G3 re-check (`research/literature/recheck/G3_cap_solutions.recheck.md`) and the G4 barrier re-run (`research/groups/addenda/G4_barrier_rerun/RESULTS.md`).

- §1, G2 row: added that β ≈ 2 for SACVs is the 2018-WP figure of Boyer et al. The 2021 version of the paper published as *JF* 78(2):835–885 (2023) gives β ≈ 1.8, so σ_SA is somewhat below 45–50% (synthesis §2.4 item 6; G2 verification log R5).
- §1, G4 row: post-recap hazard "×1.4–3.4" changed to "≈×1.1 (OLS) to ×1.7 (IV) at φ = 0.25". The ×1.4–3.4 range belongs to Bhardwaj–Gupta–Howell's average +84% debt increase (synthesis §2.4 item 2; G4 review).
- §1, G4 row: REFI breach ≈50% / 63% and drought LEVER wipe-out 7.0% → 22.8% re-checked against the barrier re-run. Both are unchanged: the first is a quarterly-tested covenant, the second an at-exit statistic. Added the continuous-monitoring range (62–73%), the "at exit" label and the E3-consistent 7.6% → 22.9% (RESULTS.md §5).
- §2, co-investment engine: the write-off barrier V ≤ κD is now stated as continuously monitored, with quarterly checks at κD·e^{+0.5826σ√Δ} (RESULTS.md §1 and the optional wording in §6.1).
- §3, Co · REFI / LEVER row: wipe-out labelled "at exit", and the E3-consistent 7.6% → 22.9% added; unchanged by the fix (RESULTS.md §5.2).
- Sources, Cai & Haque (2024): added DOI 10.17016/2380-7172.3462 (G3 re-check, ref 41; G6 review). §4 already credits the recovery figures to KBRA DLD (Fig. 15), as the re-check requires.
