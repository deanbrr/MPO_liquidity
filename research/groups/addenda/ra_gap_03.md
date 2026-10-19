# RA gap 03 addendum: oil wrong-way risk inside the canonical generator

**L_eff,t from the owner-draw engine, a total-portfolio barrel ledger, a barrel price and backstop derived from Tier 1 and Tier 2, and the ENR SELL card**

**Date:** 2026-10-19 · **Closes:** Real Assets critic gap 3 · **Amends:** `02_REAL_ASSETS_SYNTHESIS.md` §1 (finding 8, decision 2), §2.3, §3, §9.3, §11 (V-RA-OIL), §12, specification card; main §4.1, §4.6 item 9 (patched), §4.7; groups §3.7 (patched); BUILD_SPEC §4.10 · **Status:** SYNTHETIC, allocation v2, no ADIC data · **Code:** `research/groups/addenda/ra_gap_03_calcs/` (`ra03_lib.py`, `ra03_gen_run.py`, `ra03_ledger_run.py`, `ra03_t1oil.py`, which imports gap_02's `t1_engine.py` unmodified, `ra03_tier1_run.py`, `ra03_tier1_sens.py`, `ra03_mechanism_check.py`, `ra03_budget_run.py`, `ra03_card_run.py`, `ra03_card_deploy_check.py`; each writes `*_results.json`). Runs use `python -I`, fixed seeds, 30–40k paths and common random numbers.

> **SYNTHETIC-DATA NOTICE.** Balances, paths, deltas, probabilities and prices come from the synthetic book, stream 03's priors and gap_02's proxy models M1–M6 [I]. Market inputs are public and dated [S]. Every table is *SYNTHETIC – NOT ADIC DATA*.

---

## 0. Answer in brief

1. **The canonical re-run changes the state probabilities, not the sign of the problem.** It uses the monthly chain coupled to S, a Gulf-war dwell conditioned on 7.5 months elapsed, and oil started from the 15-Oct-2026 strip. On that basis the wrong-way states (SG + DB) hold 37% of 2027 and of 2028, against G12's stationary 22.5%. GW holds 25% of 2027, and 71% of war exits go into a glut.
2. **L_eff,t is 4.7% of NAV today and 4.9–5.1% for shocks one to three years out, not 9.3%.** The first-year draw delta is ≈22m bbl (≈56m in band), not ≈100m.
3. **The asset side carries ≈21m bbl of spot-equivalent delta (≈27m with the opportunistic book).** Real Assets carries 11.2m, of which ENR is 10.4m, above the 10m hard cap. RA rises to 15–17m bbl in the SG and DB states. Kink put spreads of 20–40m bbl notional would carry only 1.1–3.1m bbl.
4. **Tier 1 does not bind.** Per m bbl, the top-1% G\* paths move by $1–10m and P(red) by ≤ 0.004pp. Under Mix B, P(red) stays below 1% at 227m bbl, ≈8× today's book.
5. **Tier 2 sets the price: ≈$1.4–3.2 per bbl a year for the current ledger.** The cost comes from oil's co-movement with ADIC's crisis risk. The owner draw adds nothing to J and ≈$0.06–0.14 per bbl through the λ-weighted haircut.
6. **The budget.** Replace RA's 5m / 10m cap with three controls: a per-barrel price charged through H_j in every group, a total-portfolio Tier-1 backstop (≥ ≈170m bbl under Mix B), and a recovery rule (no rise in total delta while a Tier-1 gate is violated, as today). RA's envelope becomes its post-SELL delta: 5.7m bbl at the canonical state.
7. **ENR SELL: sell now, before the funding mix is signed.** With nothing signed, p\* on V\* is 0.76, so a bid of 0.82–0.90 clears. The sale cuts G\* by ≈$0.6bn and the asset-side delta by 5.5m bbl. Under Mix B, p\* is 0.87 and the sale is break-even.
8. **00 §4.6 item 9 and 01 §3.7 now state the put spreads in spot-equivalent delta.**

---

## 1. The re-run inside the canonical generator

**Formulation** (main §4.1 and §4.7; gap_04 §6.1; ARCHITECTURE §4.1). Parameters are stream 03's priors [I] unless tagged.

$$P(Z_{t+1}=j\mid Z_t=i,S_{t+1}=s)\propto P^Z_{m,ij}\kappa_{sj},\quad P^Z_m=\arg\min_R\lVert R^{12}-P^Z_a\rVert;\qquad h_{GW}(d)=1-e^{(d/\lambda)^k-((d+1)/\lambda)^k}$$

$$x_{t+1}=x_t+\kappa_m(\ln70-x_t)+\tfrac{\mu_Z}{12}+\tfrac{\sigma_Z\varepsilon}{\sqrt{12}}+J\mathbb 1_{GW},\quad \ln P=x+\chi;\qquad d_y=\Pi\big(0.5d_{y-1}+0.5\,\Pi(7.5-0.625FB_y)\big)$$

- **Coupling.** κ is fitted: DB ×10.7 in crisis and ×0.17 outside; SG ×1.6 and booms ×0.94 in crisis; SS ×0.60 outside crisis. This gives P(CRIS | DB) = 0.85 and P(CRIS | SG) = 0.14, with stationary shares within 0.01 of the prior's.
- **Gulf-war dwell.** The mean λΓ(1+1/k) is set to 7.6 months, the prior's monthly dwell; k = 1.3 [I]. The war began on 28 Feb 2026 [S], and past disruptions lasted months, not years (1991: four months) [S-sec].
- **Oil start.** x₀ = ln 105.92, the Dec-26 settle on 15 Oct 2026 [S-sec]. χ₀ = ln(126.55/105.92) = 0.178, using EIA spot [S]. The Dec-2030 strip price of $69.16 anchors $70.
- **Fiscal balance.** FB_y = h_y(P̄_y q_y − P^BE)/P^ref + w_Z + ε, with EIA's 2027 UAE volumes (5.20 vs 4.34 mb/d) [S]. The IMF-fused 2027 balance is frozen at t₀.
- **L_eff,t** = −∂PV(draws)/∂x_t, from ±1% bumps at r = 6%.

**Table 1. G12's side model against the canonical generator**

| Quantity | G12 | Canonical, today's state |
|---|---|---|
| Shock-type dynamics | Annual, memoryless, stationary start | Monthly, coupled to S, duration-conditioned GW, Z₀ = GW 0.85 |
| Share of 2027 in GW | — (gap_04's linearised chain: 49%) | **29%** (k 0.8 / 2.2: 44 / 13%; memoryless monthly 35%; the IMF's March-2027 reopening as a point: 17%) |
| SG + DB share | 22.5% (stationary) | **37 / 37 / 29%** (2027 / 2028 / 2029); 30% over 2027–31 |
| Oil start | $95 proxy | Strip $105.92 / $85.08 / $69.16 (Dec-26 / Dec-27 / Dec-30); model median $83.6 (Dec-27), $73.0 (Dec-28; strip $76.8) |
| 12-month draw | — | $10.3bn (P90 $11.6bn); gap_04: $9.9–10.8bn |
| P(d\* in band) | 0.64 | 0.38 / 0.35 / 0.46 / 0.51 (2027–30) |
| L_eff | 9.3% (formula) | **4.7%** at t₀; 4.9 / 5.0 / 5.1% at 12 / 24 / 36 months; 3.6–5.9% for P^BE $45–65 |
| First-year draw delta | ≈100m bbl (in band) | **22m bbl** expected; 56m in band |

*SYNTHETIC – NOT ADIC DATA.*

**Readings.**
- **The linearisation I + (P − I)/12 overstated the war, more than memorylessness did.** It doubles 12-month GW persistence (0.44 vs 0.20) and the mean dwell (15 vs 7.6 months). Conditioning on elapsed duration then cuts 2027's GW share from 35% to 29%, with the median exit in March 2027. That matches the IMF's reopening date [S→03] and EIA's 4Q26→1Q27 shut-in path of 4.5→2.7 mb/d [S].
- **L_eff is lower than G12's** because the 2027 rate is set on the 2027 average price, smoothing halves the first response, and the draw is at its floor in 62–65% of 2027–28 paths. It barely depends on the war law (4.7–5.0%).
- **G12's 9.3%/L_eff,t budget scaling mixes a formula with an engine.** On one engine the stationary L_eff is also 4.7%, so the factor is ≈1.0, not 2.0.

**Defects found by running the canonical specification.**
1. **Stream 03's annual prior is not embeddable.** The clipped principal root misses it by 0.19, and the best monthly chain by 0.097 (SS and DB rows; the GW row is within 0.02). BUILD_SPEC's ≤ 0.01 test fails; re-elicit a monthly generator.
2. **χ's half-life must fit the strip.** At Schwartz–Smith's half-life (κ = 1.49, ≈6 months [S]), the expected spot sits 16% above the Dec-26 contract; the fitted half-life is 0.4 months.
3. **The IMF fusion must be frozen at t₀.** Re-fitted inside bumped runs, it absorbs common oil shocks, giving L_eff 2.5% instead of 4.7%.

---

## 2. Total-portfolio oil-delta ledger

**Convention.** Δ_j = (∂V_j/∂x)/F₁, with F₁ = $105.92 and the curve moving by the generator's impulse 0.6^{m/12}. Hedges count at delta, never notional. SG and DB are the generator's state-conditional curves, with NAVs re-marked: the front month is $76 / $80 at month 12 and $61 / $63 at month 24.

**Table 2. Spot-equivalent oil delta, m bbl (positive = long oil)**

| Holding | NAV, $bn | ε | Now | SG / DB, m12 | SG / DB, m24 | Basis |
|---|---|---|---|---|---|---|
| RA ENR levered upstream (funds 0.80, direct 0.27) | 1.07 | 0.84 | 8.44 | 8.88 / 8.85 | 9.79 / 9.80 | G12 split; DCF on the strip |
| RA ENR royalties, fee midstream, other | 0.18, 0.85, 0.40 | 0.41, 0.13, 0.07 | 1.97 | 2.44 / 2.38 | 2.88 / 2.85 | G12 |
| RA infrastructure midstream (`energy_link`) | 0.65 | 0.13 | 0.78 | 1.02 / 0.99 | 1.23 / 1.21 | RA §2.1; G11 |
| RA GCC real estate (fiscal channel) | 1.20 | 0 now; 0.18 | 0.00 | 2.69 / 2.59 | 3.23 / 3.14 | BIS/FRED β 0.12–0.14 |
| **Real Assets** | | | **11.19** | **15.03 / 14.81** | **17.13 / 17.00** | |
| PE, co-investment, Secondaries look-through | 0.68, 0.54, 0.28 | 0.38 | 5.36 | 6.58 / 6.39 | 7.57 / 7.41 | PIN 2.0% [S-sec]; 3%, 2% [I] |
| Capital Solutions, Private Credit | 0.24, 0.28 | 0.12, 0.05 | 0.40 | 1.15 / 1.11 | 1.38 / 1.34 | Shares [I]; NB credit β [S] |
| Public Markets (long-only equity, FI, HF) | 1.11, 0.64, 0.24 | 0.24, 0.05, 0.24 | 3.34 | 4.89 / 4.72 | 5.84 / 5.69 | ACWI 3.96% [S]; NB 0.40 [S] |
| Overlay completion beta | 0.40 | 0.24 | 0.90 | 1.15 / 1.12 | 1.37 / 1.34 | ACWI 3.96% [S] |
| **Asset side** | | | **21.19** | **28.80 / 28.15** | **33.29 / 32.78** | |
| Overlay opportunistic trend + carry (templates) | | | +5.5 | short | short | groups §3.7 [I] |
| Kink put spreads, 20–40m bbl, 1-year, if held | | | −1.6 to −3.1 | −3.4 to −7.6 | −5.0 to −10.5 | §5 |
| Owner draw, PV / first year | | | 79 / 22 | | | §1 |

*SYNTHETIC – NOT ADIC DATA.* ε is the elasticity to x. Sector weights: MSCI ACWI 3.96% (30 Sep 2026) [S]; Pantheon International 2% (31 Aug 2026) [S-sec]. Betas to 12-month futures: Norges Bank 0.40 (oil and gas equities) and 0.08 (energy bonds) [S via G12].

**Readings.**
- **The ENR sleeve carries 10.4m bbl at the canonical state, not 9.2m.** Averaging the impulse over each production year, where G12 used year-end points, raises elasticities by ≈25%.
- **RA is half the asset side.** The rest is PE, co-investment and Secondaries look-through (5.4m bbl), Public Markets and the completion overlay (4.2m), and credit (0.4m).
- **Barrel deltas grow as oil falls.** NAV falls less than price, leverage rises and the GCC fiscal channel switches on: by month 24 of a glut, RA is up 53% and the asset side 57%.
- **GCC real estate is wrong-way in every stress state but has no single delta.**
  - Fiscal channel, long oil in SG and DB: BIS UAE prices regressed on Brent give β 0.12–0.14 (Newey–West s.e. 0.05; 2003Q1–2024Q1). G15's stress implies ≈3× that.
  - War wedge, short oil today: −6m bbl if the wedge is read as a price delta.
  - It needs H_j, not a cap.
- **The opportunistic trend and carry families are long oil today and short in a glut.** Right-way, but they double the near-term delta, so they belong in the ledger.

---

## 3. Marginal costs and the derived budget

**Price per barrel**, measured on the oil-aware Tier-1 engine with pure-risk bumps (zero expected excess return):

$$p_{bbl}=-\frac{\partial CE}{\partial\Delta}+\frac{\mu}{a_5}\frac{\partial G^*_{99.6}}{\partial\Delta}+c_{red}\frac{\partial P(red)}{\partial\Delta},\qquad H_j=p_{bbl}\,\delta_j/V_j$$

- μ is the restored-problem dual (groups §4.8): 0.0113 with the revolver signed (R1), 0.243 on group levers (R0); ra_gap_01 finds 0.124 for R0 on the v2 book.
- a₅ = 4.33.
- c_red is gap_02's frontier slope near 1%: 4–8bp a year per pp of P(red).

**Table 3. Marginal cost per barrel, $ a year** (M1–M5; M6 in brackets)

| Channel | Tier 2 (CE) | Tier 1 G\*, μ 0.0113 / 0.243 | Tier 1 P(red) | ΔP(red) per m bbl |
|---|---|---|---|---|
| ENR fund interest (ε 0.84) | 2.9–3.2 [4.3] | 0.00 / 0.02–0.06 | 0.02–0.33 | ≤ 0.002pp |
| PE / co-investment look-through | 2.2–2.5 [3.5]; Mix B 1.8–2.1 | 0.01 / 0.08–0.14 | 0.02–0.61 | ≤ 0.004pp |
| Direct levered upstream (RBL, cures) | 0.9–1.2 [1.8]; Mix B 0.5–0.8 | 0.01 / 0.09–0.13 | 0.05–0.57 | ≤ 0.004pp |
| Public energy equity | 0.3–0.5 [0.4] | 0.02 / 0.43–0.58 | 0.02–0.43 | ≤ 0.003pp |
| Current ledger | 1.8–2.1 [3.2]; Mix B 1.4–1.7 [2.4] | 0.01–0.02 / 0.24–0.33 | 0.03–0.55 | ≤ 0.004pp |
| λ-weighted haircut (horizon) | 0.06–0.14 | | | |
| Draw-utilisation haircut, κ_d = 1 | 0.36–0.39 | | | |
| G12 surplus hurdle on canonical L_eff, γ 2–4 | 0.74–1.54 | | | |

*SYNTHETIC – NOT ADIC DATA.* P^BE $65, no IMF fusion, and war law k 0.8 or 2.2 each move every entry by less than its model range.

**What drives Tier 2.**
- **Coupling, not the draw.** With κ = 1, the CE cost of 10m bbl falls by 80–100% (M1: −1.26 → −0.27bp; the M6 sign flips). An oil-blind draw changes it by < 0.05bp.
- **So the cost is oil's co-movement with crises:** 85% of demand busts are crises.
- **J counts distributions as wealth, so the draw's oil link reaches J only through liquidity.** There it adds 0.4–1.3pp to do-nothing P(red), which is liability-side.
- **IC question.** Under G12's surplus framing, the draw would add ≈$0.7–1.5 per bbl.

**Quantity.**
- **Backstop = slack ÷ marginal.** Under Mix B, M5 binds: 0.28pp ÷ 0.0017pp per m bbl (+2 s.e.) gives ≥ 166m bbl. Directly, P(red) is 0.88% (M5) and 0.85% (M4) at 227m bbl. Mix A gives ≥ 525m bbl. On T4′, ΔG\* is ≈$4–6m per m bbl against $11–12bn of headroom.
- **Recovery.** With nothing signed, T6 is breached in every model (P(red) 4.7–31.6%), and the ledger adds 0.04–0.10pp in M1–M5 (2–3.5 s.e.). Phase II admits no action that worsens a violated gate.

**The budget (replaces RA's 5m / 10m).**
1. **Price.** Every oil-linked holding, in every group, pays H_j = p_bbl·δ_j/V_j as its one pricing channel (Table 4).
2. **Backstop.** Total-portfolio delta ≤ the Tier-1-derived level: ≥ 170m bbl under Mix B, to be re-derived on the integrated engine. It is a model-risk guardrail, checked at the canonical state and at the month-24 SG and DB states.
3. **Recovery rule.** No rise in total delta while any Tier-1 gate is violated.
4. **RA envelope.** Δ_RA ≤ 5.7m bbl after the SELL at the canonical state (9.0–9.2m in the month-12 SG/DB states; 10.6–10.7m at month 24). It is raised only by cards that clear H_j. RA holds 53% of today's asset-side delta.

**Table 4. H_j implied by the barrel price, % of NAV a year**

| Holding | δ/V, m bbl per $bn | H_j | G12 hurdle (γ 2–4) |
|---|---|---|---|
| Levered upstream, fund interest | 7.9 | 2.4–2.9 [3.4] | 2.4–4.8 |
| Levered upstream, direct (RBL, cures) | 7.9 | 0.8–1.5 | 2.4–4.8 |
| Royalties | 3.8 | 0.8–1.2 | 0.9–1.9 |
| Fee midstream (ENR, infrastructure) | 1.2 | 0.3–0.4 | 0.3–0.6 |
| PE / co-investment energy look-through | 3.6 | 0.8–1.1 | — |
| Public energy equity | 2.3 | 0.1–0.3 | — |
| GCC real estate (state exposure, CE) | — | 0.4–0.9 [0.9–1.9] | none |

*SYNTHETIC – NOT ADIC DATA.* The hurdles survive roughly intact, now justified by crisis co-movement rather than the draw, and GCC real estate gains one.

---

## 4. ENR SELL decision card

**Method.**
- **p\*** is the bid × θ (per $ of V\*) that equalises CRRA(3) certainty-equivalent wealth under SELL and HOLD (M1–M5 mixture).
- **HOLD** keeps β_eq 0.6, the canonical oil elasticity, oil-elastic distributions, and calls on its $0.26bn unfunded, plus α̂ − τ_j + g_PQ. α̂ is measured against the implementable beta-matched basket.
- **SELL** rebuilds the beta in futures, and its proceeds land after the t₀ reserve top-up.
- **The deployment rule matters.** Holding proceeds as cash lowers p\* by 0.11–0.13. Landing them before the top-up, which keeps $0.56bn more DM equity, raises it by ≈0.15.

**Table 5. SELL $0.6–0.8bn of the $0.80bn fund-held levered upstream** (Tier A; LP cell: SELL admissible, hedging overlay-only)

| Item | Do nothing (recovery) | Mix B signed |
|---|---|---|
| p^ce, per $ of reported NAV | 0.82 (G15 ladder) to 0.86–0.90 (Gulf-war bid) [I]; Jefferies H1-26: upstream pricing up, no level [S] | Same |
| p\* on V\*, α̂ −2 / 0 / +2% | 0.69 / **0.76** / 0.83 [M6 0.60–0.70] | 0.79 / **0.87** / 0.96 [M6 0.61–0.77] |
| ΔCE at a 0.85 bid (α̂ 0) | +0.9bp a year | −0.1bp a year |
| H_j; τ_j; g_PQ | 2.4–2.9% a year [3.4]; 0.25%; −1.4% (−0.7 / −1.9 at k 0.8 / 2.2) | Same |
| Δbbl | −4.7 to −6.3m now; −5.5 to −7.3m at m24 SG/DB | Same |
| ΔG\*(P99.6) | −$0.62 to −0.65bn | −$0.53 to −0.65bn |
| ΔP(red) | −0.16 to −0.43pp [M6 −0.60] | 0 to −0.04pp [M6 −0.15] |
| E[W_SELL − W_HOLD] at 0.85 | +$0.01–0.04bn | +$0.03–0.10bn |
| Regret of SELL / of HOLD | $0.14–0.16bn / $0.17–0.19bn | $0.14–0.15bn / $0.18–0.24bn |
| E[ΔW]: war persists to Jul-27 (19%) / glut in 2028 (45%) | +$0.02–0.06 / +$0.07–0.10bn | +$0.04–0.12 / +$0.08–0.15bn |
| Flip thresholds at a 0.86 bid: bid (α̂ 0); α̂; θ | 0.76; +2.8%; 0.88 | 0.87; −0.3%; 1.01 |
| War law k 0.8 / 2.2 | p\* +0.02 / −0.02 | p\* +0.03 / −0.02 |

*SYNTHETIC – NOT ADIC DATA.* V\* is valued on the strip; θ = V^A/V\* = 1.0 base.

**LAPV cross-check.** h = 1 + D(α̂ − τ_j + g_PQ − H_j), with D = 4.1 years, gives 0.83 at α̂ = 0. Subtracting the liquidity value μΔG\*/V\* (0.01 at R1; 0.11 at μ 0.124; 0.22 at 0.243) gives p\* of 0.83 / 0.72 / 0.61, which brackets the engine. Oil risk (≈0.11) and the glut drift (≈0.06) dominate.

**Verdict: SELL now, while nothing is signed.**
- The sale clears at 0.82 and is robust to α̂ ≤ 2.8% a year, θ ≥ 0.88 and either war law.
- If Mix B is signed first, sell only at bids ≥ 0.88 or on evidence that α̂ < 0.
- Conditions: ra_gap_01's confirmatory sealed run, θ̂ from the strip-based nowcast, and proceeds kept liquid while in recovery.
- The sale removes half of RA's barrels.

---

## 5. Overlay put-spread sizing, restated

Patched in main §4.6 item 9 and groups §3.7.
- **Delta.** At the 15-Oct-2026 strip a 1-year 64/31 spread has an option delta of −0.17 against the $85.08 Dec-27 forward, which is ≈0.078 bbl of spot-equivalent delta per bbl of notional. So 20–40m bbl of notional carries 1.6–3.1m bbl.
  - 2-year spreads: 1.1–2.3m bbl.
  - Linear kinks, 67/23: 1.9–3.8m bbl.
  - Canonical kinks at P^BE $55 and 2027 volumes, 65/26: 1.7–3.4m bbl.
  - In the SG and DB states: 3.4–7.6m bbl at month 12 and 5.0–10.5m at month 24.
- **Cost.** Premia at OVX-anchored vols are $3.86 (1-year) and $7.02 (2-year) per bbl of notional (OVX 49.13 on 15 Oct 2026 [S]; term structure [I]). That is $46–59 per bbl of delta a year, 15–40× the barrel price.
- **Payback.** On the generator's P-measure, a 3m-bbl-delta programme repays ≈0.5 of its ≈$0.27bn annual premium and raises do-nothing P(red) by 0.1–0.7pp. This is model-dependent: the generator's oil vol is below OVX.
- **Reading.** It is crash protection, judged by enabling value (L5), not a delta hedge. A SELL removes barrels at the bid. Asset-level swaps cost near-zero premium, but post margin in GW and boom tails.

---

## 6. Design implications

1. **RA §9.3, §2.3 and the specification card.** Replace 5m / 10m and the 9.3%/L_eff,t scaling with the price, backstop and recovery design. Report Δ_RA at the canonical state and at the month-24 SG and DB states.
2. **New IC card, the oil ledger.** Table 2 by group and state, the liability in barrels, and every group's H_j.
3. **Generator (BUILD_SPEC §4.10).**
   - Least-squares monthly matrix with a logged error, from a re-elicited monthly prior.
   - Weibull GW dwell started from the as-of elapsed duration.
   - χ's half-life fitted to the front of the strip.
   - IMF fusion frozen in bump and stress runs, with a new test.
   - L_eff,t by bump-and-revalue in the owner-draw engine.
4. **H_j = p_bbl·δ_j/V_j from the Tier-1 engine.** The draw-surplus hurdle is reported, not charged. GCC real estate and every group's energy look-through carry H_j.
5. **V-RA-OIL restated.** ENR 10.4m bbl ± 5% and RA 11.2m at the 15-Oct-2026 strip; ledger rows reconcile to group NAVs; hedges count at delta.
6. **The ENR card fixes the proceeds-deployment rule** and feeds ra_gap_01's confirmatory sealed run.
7. **IC question.** Should the owner's oil exposure enter Tier 2 (surplus framing), or only Tier 1?

---

## 7. Limitations

- **Proxy census.** The Tier-1 engine uses gap_02's proxies and the v1 census, with RA as oil blocks rather than in ra_gap_01's v2 engine. The marginals are robust to this; the levels are not.
- **Oil vols.** Stream 03's priors (GW 30%) sit below OVX and 2026 realised vol. A higher vol raises both the Tier-2 costs and the put-spread payoffs.
- **Assumed inputs.** The energy shares for co-investment, Secondaries, Capital Solutions and Private Credit, the opportunistic templates, and the card's α̂, θ and bid are all [I].
- **GCC fiscal loading** rests on 80 overlapping quarters to 2024Q1.

---

## Sources

**Market and official** (accessed 18–19 Oct 2026)
- CME Daily Bulletin #199 (NYMEX BZ settlements, 15 Oct 2026), as relayed by Baratelli Institute, "Oil Forward Curve" (17 Oct 2026) [S-sec]. https://baratelliinstitute.com/oil-futures-curve
- HDFCSky weekly review (17 Oct 2026): Dec-26 Brent $105.92 [S-sec]. https://hdfcsky.com/news/brent-holds-above-105-as-hormuz-attacks-cut-gulf-flows-68percent-wti-jumps-5-81percent-on-record-us-inventory-draw
- EIA Brent spot (RBRTE), via FRED DCOILBRENTEU: $126.55 on 14 Oct 2026. https://fred.stlouisfed.org/series/DCOILBRENTEU
- Cboe OVX, via FRED OVXCLS: 49.13 on 15 Oct 2026. https://fred.stlouisfed.org/series/OVXCLS
- EIA, *Short-Term Energy Outlook*, October 2026: Table 1 (shut-ins); Table 2 (Brent 4Q26 $104.69, 2027 $83.74); Table 3b (UAE liquids). https://www.eia.gov/outlooks/steo/archives/oct26.pdf
- MSCI ACWI Index factsheet, 30 Sep 2026: Energy 3.96%. https://www.msci.com/documents/10199/255599/msci-acwi-net.pdf
- Pantheon International factsheet, 31 Aug 2026: Energy 2%, via ticker.app [S-sec]. https://funds.ticker.app/investment-trusts/PIN
- Reuters via Khaleej Times (22 Apr 2026), on past supply disruptions [S-sec]. https://www.khaleejtimes.com/world/mena/how-the-iran-war-oil-and-gas-supply-shock-compares-with-past-disruptions
- BIS UAE residential property prices (FRED QAEN628BIS) and FRED quarterly Brent, as downloaded by G15 on 18 Oct 2026.

**Academic**
- Schwartz, E. & Smith, J. E. (2000). Short-term variations and long-term dynamics in commodity prices. *Management Science* 46(7), 893–911; Table 2. https://doi.org/10.1287/mnsc.46.7.893.12034

**Project** [C]
- G12 dossier and verification log.
- RA synthesis §4.3, §9.3, §11.
- Main §4.1, §4.6, §4.7, §4.9; gap_02; gap_04 §6.
- Groups §2.3, §3.7, §4.3, §4.8.
- Stream 03 §6.3–6.6; G15.
- ra_gap_01.
