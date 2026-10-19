# RA gap 01 addendum: Real Assets decided at total-portfolio level

**Date:** 2026-10-19 · **Closes:** Real Assets critic gap 1 (Real Assets not decided at total-portfolio level; no attribution layer; integration memo missing) · **Amends:** RA synthesis §1, §2.3, §4.7, §6.3, §8.5, §10–§12; groups §2.4, §4.3, §4.8, §6, §7.1; main §4.9, §4.11, §6.2 · **Status:** SYNTHETIC prototype on SYN-ADIC-177, allocation v2; no ADIC data · **Code:** `research/groups/addenda/ra_gap_01_calcs/` holds `ra_book.py`, `ra_ladder.py`, `ra_module.py`, `ra_engine.py` (a copy of gap_04's engine; the original is untouched), `ra_run.py`, validators, `test_v_ra_ctrl.py` and `ra_*_results.json`. Runs use `python -I -B` with fixed seeds.

> **SYNTHETIC-DATA NOTICE.** Every figure comes from synthetic data and gap_02's stylised proxy models M1–M6. Tags follow the RA synthesis; [I-calc] marks figures computed here. Every table is *SYNTHETIC – NOT ADIC DATA*.

---

## 0. Answer in brief

1. **The integrated v2 re-run is anchored.** In v1 mode it reproduces `t1_engine`, the gap_04 engine, the gap_02 / groups gap_01 ladder, G15's cash row and RAME's 32% capture (§1).
2. **θ\* rises on the eight-group book**, from 0.76 to 0.835 at PE unfunded $16.4bn (pooled 0.850) and 0.877 at $10.9bn (pooled 0.897). Do-nothing survives 18 / 20 months on Treasury + Public Markets. It needs $11.6bn / $8.3bn of facilities, $3.7bn / $0.2bn with the pacing rule and none with the band (§2).
3. **Real Assets' canonical T4′ drain is −$4.5bn over 24 months, not −$2.46bn.** The synthesis's own lender-availability term and the fund-level module add $1.8bn, and the higher θ\* $0.2bn. RA drains more than the same NAV at PE rates (§2).
4. **Prices from the restored problem** (§3):
   - **FTP_RA** on scheduled flows is 2bp a year with the revolver signed and 21bp without; with cures included it is 5 / 55bp, against RA §10's 3–4 / 66–81bp. The hurdle is 13 / 144bp.
   - **μ without the revolver** halves against v1 (0.124 vs 0.243), because RA's JV sell-down becomes the marginal lever.
   - **CLC_RA** prices cures once: $36–38m a year (≈20bp of RA NAV) on CVaR95 of joint-path cures ($2.4bn), not $5–14m.
   - **B_RA**, from the L4 pool row, is $4.3bn (revolver plan) / $4.0bn (group-lever plan) over 24 months.
   - **L8** is 0.774 / 0.743, headroom $4.6bn / $10.1bn.
5. **Sizing.** Over 6–14% of NAV, five-year CE moves by at most ±$1.2bn, with a sign that depends on the model, and no Tier-1 row binds. So 8–12% is a judgment band. The optimizer outputs the increment price and the pacing envelope: $1.8bn a year split ≈33 / 67 / 0 (RE / infrastructure / ENR), not 45 / 45 / 10. Cash-outs are dominated (§3–4).
6. **DVA_RA is paid on V\*** with a desmoothed funding basket. On the T4′ path, reported-NAV DVA shows +$0.6bn in year 1 against −$3.8bn on V\*, and reverses in year 2 (§5).
7. **Tenth player.** Real Assets' exact Shapley value is −2.3 / −4.3 / −5.2pp of P(red) and +$0.26 / 0.50 / 1.09bn of CE (M1 / M4 / M6). That is 6–9% of each total, fourth of ten on both. Stand-alone attribution would credit it 2–4× more (§6).
8. **ENR SELL: NOT ESTABLISHED.** In the pre-registered sealed run (6 worlds × 50,000 fresh paths), selling $0.7bn at 0.80 costs 1.6–2.8bp a year of CE in every world. It is Tier-1 neutral and halves the oil delta at $70 (12.2 → 5.8m bbl). CE breaks even only at bids of 0.95–1.10 of reported NAV. Today's delta (≈9.2m bbl) is inside the hard budget, so the sale becomes contingent (§7).
9. **Patched in place:** eight groups, 13 seats, ten players and V-RA-CTRL in 00 and 01. The 03 memo is written; `test_v_ra_ctrl.py` passes 4/4 (§8).

## 1. The integrated v2 re-run

**Book.** PE $34bn with unfunded $16.4bn (the user's census v1.1 figure, "U16") or $10.9bn (v1.1's U/NAV rescaled, "U11"), both on the sealed v1.1 vintage profile (groups gap_02); Real Assets $18bn / $4.0bn in the ten census sleeves of record (RA §11); all else census v1.0. The canonical $12bn a year of plan commitments splits 50/10/10/10/10/10, Real Assets' $1.2bn coming out of PE (G15).

**Engines.**
- **(i) Ladder:** a monthly ladder for s\*(θ) with an RA leg, built from G15's sleeve engine plus RAME marks, lender availability, extensions and the fund-level module.
- **(ii) Monte Carlo:** groups gap_04's quarterly integrated Monte Carlo, with an RA state machine per path and sleeve:
  - true, reported (RAME) and nowcast values, V\* = true × e^ε (asset RMSE 5.5%, AR(1) 0.5);
  - asset debt maturing at 17% a year, refinanced at a(state) × LTV^max(state) × true value, with gaps cured under ϖ = 1 or through the fund waterfall (protective call → distribution stop → NAV loss at a 20% discount);
  - G10's open-end queue, oil-elastic ENR and GCC fiscal drag.

RA draws use a dedicated stream, so common random numbers hold elsewhere.

| Validation | Result |
|---|---|
| Ladder replica vs groups gap_01 / gap_02, 6 readings × 8 policies | max difference 0.0 |
| Monte Carlo in v1 mode vs `t1_engine` (9 configs) and the gap_04 engine (4 configs) | identical |
| v1 bridge: P(red) do-nothing M1 / M6; group-off M1 / M6 | 1.60 / 14.52 / 24.78 / 66.24% (gap_04: 1.6 / 14.5 / 24.8 / 66) |
| V-RA-CF: normal, drought, T4′ 12m / 24m, pacing stop, calls ×1.0 | +0.40, −0.16, −1.32 / −2.46, −1.65, −0.84 / −1.70 (exact) |
| RAME capture of the T4′ true loss after 12 months | $2.32bn of $7.35bn (31.6%) |
| Survival proxy vs ladder at t0, v2, θ 0.76 / 0.85 | equal SH_TP |

*SYNTHETIC – NOT ADIC DATA.*

## 2. Real Assets inside s\*(θ), and θ\* recalibrated

**θ-indexed components.** Each is affine in θ. Income, value and LTV^max pass through G15's T4′ values at θ₀ = 0.76. Lender availability and extension, which RA §4.5 specifies but G15's row omitted, are new:

$$m_s(\theta)=1-\tfrac{\theta}{0.76}\,(1-m^{T4'}_s),\quad v_s(\theta)=v^{T4'}_s\,\tfrac{0.30+0.10\theta}{0.376},\quad L_s(\theta)=L^N_s-\tfrac{\theta}{0.76}\,(L^N_s-L^S_s),\quad a(\theta)=0.97-0.52\theta,\quad p_{ext}(\theta)=0.35(1-\theta)$$

Calls (1 + 0.5θ) × 28% and exits 0.45(1 − θ) × drought rates are the family's own. a(0.76) = 0.575 sits mid-way in RA §5's crisis range (0.50–0.60) [I]. p_ext uses G10's lower value (0.35) and falls to zero at literal T4, since risky and non-recourse loans were extended less often after 2022 (Glancy 2026, via RA §4.5) [S].

**The RA T4′ row** ($bn):

| Step | 12m | 24m |
|---|---|---|
| G15 published row | −1.32 | −2.46 |
| + θ-indexing and RAME marks (θ 0.76) | −1.30 | −2.49 |
| + fund-level module | −1.50 | −2.87 |
| + lender availability and extension, canonical (θ 0.76) | −2.33 | −4.21 |
| Canonical at θ\*: U16 (0.835) / U11 (0.877) | −2.50 / −2.60 | −4.49 / −4.64 |
| Axes at θ\* U16: extension 0 / 0.35; calls ×1.0; fund shortfall all cash; no new RA commitments | | −4.57 / −4.02; −3.79; −5.05; −3.62 |

*SYNTHETIC – NOT ADIC DATA.* At θ\* (U16) the 24 months hold income 1.13, exits 0.10, distribution stops −0.32, calls 2.91, protective calls 1.36 and direct cures 1.12. The same NAV at PE rates drains −$2.69bn (U = 4.0) to −$3.76bn (U/NAV 0.32) (RA §4.7), so **RA's T4′ relief against PE is negative**, not a range that includes zero.

**θ\* recalibration.** The rule is the worst model's P99.6 of the action-free 24-month gap G\* (50,000 paths, gap_02's initial state); θ\* inverts each book's own ladder curve G\*(θ):

| Book | Worst model, P99.6 G\* ($bn) | θ\* | SAA, 6 seeds (pooled) | October-2026 state |
|---|---|---|---|---|
| v1, gap_02 split | M6, 11.10 | 0.759 | 0.76–0.81 (0.79; groups gap_01) | — |
| v1, census v1.0 split | M6, 10.52 | 0.749 | 0.749–0.787 (0.765) | — |
| **v2 U16** | M6, 9.30 | **0.835** | 0.835–0.869 (0.850) | 0.643 |
| **v2 U11** | M6, 6.62 | **0.877** | 0.877–0.916 (0.897) | 0.674 |

*SYNTHETIC – NOT ADIC DATA.* The v1 row reproduces the published 0.76. On v2 the tail gap falls less than the family's gap at fixed θ (ladder G\*(0.76): $7.8bn U16, $4.4bn U11), so θ\* rises. The canonical v2 stress s\*(0.835) has equity −38.3%, PE-type distributions at 7.4% of drought, calls ×1.42 and 23 crisis months. For RE / GCC / infrastructure / ENR it has income ×0.84 / 0.78 / 0.91 / 0.56, true value −25.5 / −30.6 / −12.2 / −30.6%, LTV^max 49 / 44 / 54 / 44% and availability 0.54. The mixture P99.6 would give θ 0.50.

**Survival** (do-nothing with the 8% top-up):

| Reading | SH_TP / SH_TPF (months) | Facility for 24m ($bn) | + pacing rule | + band | Mix A / Mix B: 24m headroom ($bn) |
|---|---|---|---|---|---|
| v1 at 0.76 (published) | 17 / 17 | 13.9 | 6.1 (20m) | 0 (29m) | +12.0 / +10.8 |
| **v2 U16 at 0.835** | **18 / 18** | **11.6** (12.0 pooled) | 3.7 (22m) | 0 (32m) | +14.0 / +10.8 |
| **v2 U11 at 0.877** | **20 / 20** | **8.3** (8.7 pooled) | 0.2 (24m) | 0 (> 36m) | +16.8 / +10.9 |

*SYNTHETIC – NOT ADIC DATA.* Readiness moves from Red (17 months) to Amber (18) on U16. With G15's RA leg instead, U16's G\* would be $7.4bn; the canonical leg adds $1.9bn.

## 3. Phase-II prices, CLC, the L4 pool row and L8

The t0 execution deficit (nothing signed, no top-up) is d₀ = $9.5bn (U16) / $6.8bn (U11). Phase I returns u\* = 0 in every state, so there is no structural recovery. Duals come only from the restored problem (`priced_on: restored_problem`; hashes R1 `e24d499958e3bb6d`, R0 `e6f07f422fbb60e3`) and are unchanged at ten times the penalty tiers.

| At θ\* | R1: revolver signed | R0: group levers + top-up |
|---|---|---|
| μ, 5-year PV per $ of month-24 headroom | 0.0113 (carry; revolver $11.0bn + SMA $0.23bn) | 0.124 (marginal: RA JV sell-down; v1 0.243) |
| **FTP_RA on holdings**, bp a year, scheduled flows (cures in CLC_RA): U16 / U11 | **2.0 / 2.1** | **20.5 / 15.2** |
| FTP_RA with cures (RA §10 basis: 3–4 / 66–81bp) | 5.4 / 5.5 | 55.5 / 42.2 |
| **Hurdle on new RA commitments**, bp a year | 13 / 13 | 144 / 105 |
| PE FTP, for comparison | 9.4 / 7.3 | 102 / 57 |
| ENR SELL card (bid 0.80; hold 0.84 net of H_j) | reservation 0.802: HOLD | 0.724: SELL |
| RE value-add LP card (bid 0.68; hold 0.70; buyer assumes unfunded) | 0.666: SELL | 0.574: SELL |

*SYNTHETIC – NOT ADIC DATA.* The published 3–4 / 66–81bp priced RA's drain with v1 duals. Main §4.11 charges contingent outflows once, so FTP_RA covers scheduled flows (calls less distributions) and cures go to CLC_RA.

**Lever costs per $ of month-24 headroom** (U16, θ\*): revolver 0.011; SMA run-off / sale 0.048 / 0.054; band 0.072; Private Credit pacing 0.091; co-investment pause 0.123; **RA JV sell-down 0.124**; **RA pacing stop 0.150**; **RA cash-out at maturity 0.157 on $0.03bn of capacity**; PE pacing 0.213; Treasury top-up 0.244. Only Q4-2026 maturities on controlled debt can be cashed out, since early refinancing is barred while lock-in exceeds 0.5% of GAV. **Asset-level cash-outs are therefore dominated in both states.**

**CLC_RA** = c_buf × CVaR95 of 24-month joint-path cure cash (direct cures + protective calls + distribution stops) from the integrated Monte Carlo. Pooled over M1–M6 it is $2.37bn under Mix B ($2.44bn group-off; worst model M6 $2.44–2.52bn; mean 24-month cures $0.79bn).
- At c_buf 1.5% that is **$36–38m a year**, ≈20bp of RA NAV ($24–76m at 1–3%). That is 2.6–7× RA §10's $5–14m, which used deterministic cures without availability.
- Setting c_buf to the marginal lever's annual carry, μ/5 (≈0.2% with the revolver, ≈2.5% without), gives ≈$5m or ≈$60m.
- Those figures are close to the dual-based cure prices of $6m and $63m (3.3bp and 35bp of RA NAV), so the two pricing routes agree when c_buf follows the state.

**B_RA from the L4 pool row** (Σ_g B_g + B_OVL ≤ Pool_h; U16, θ\*; $bn, 24 / 12 months):

| Plan | B_RA | B_PE | Pool₂₄ | Slack₂₄ |
|---|---|---|---|---|
| Do nothing | 4.49 / 2.50 | 14.19 / 7.45 | 18.5 | −9.3 |
| Minimum T4′ plan R1: revolver, SMA $0.23bn, RE LP card | **4.26 / 2.36** | 14.19 / 7.45 | 27.6 | 0.0 |
| Minimum T4′ plan R0: co-investment pause, PC levers, SMA $5.6bn, RA JV $0.39bn, cards | **4.03 / 2.22** | 14.04 / 7.36 | 25.3 | 0.0 |
| Mix A | 3.80 / 2.32 | 10.68 / 6.54 | 33.6 | +14.0 |
| Mix B | 3.95 / 2.38 | 11.44 / 6.82 | 39.9 | +18.5 |

*SYNTHETIC – NOT ADIC DATA.* U11: 4.64 / 2.60 (do nothing) to 4.09 / 2.48 (Mix B). B_RA is now the RA row of the restored plan; the 24-month row binds in both minimum plans.

**L8.** Private NAV plus unfunded over W is **0.774 at U16 (headroom $4.6bn)** and **0.743 at U11 ($10.1bn)**, against 0.751 ($8.6bn) for the seven-group v1.1 book; RA uses $22bn of the cap. On the T4′ path the ratio reaches 1.02 at month 12 and 1.16 at month 24 (true RA marks barely change it), so L8 is an allocation guard at t0, not a stress constraint.

## 4. Sizing and pacing: what the optimizer outputs

**NAV band.** RA scale 0.6–1.4 (6.1–14.2% of NAV), with PE absorbing the difference, private NAV fixed at $106bn and PE unfunded scaling with PE NAV; U16, Mix B, 10,000 paths per model, paired:

| RA share | ΔCE, $bn over 5y: M1 / M2 / M3 / M4 / M5 / M6 | Equal-weight ΔCE | ΔE[W̃], M1 | G\* at θ\* | L8 headroom, U16 / U11 |
|---|---|---|---|---|---|
| 6.1% | −0.03 / +1.13 / −1.06 / −0.16 / −0.45 / −0.62 | −0.20 | +1.47 | 9.94 | 2.7 / 9.4 |
| 8.1% | −0.02 / +0.57 / −0.52 / −0.06 / −0.22 / −0.31 | −0.09 | +0.73 | 9.62 | 3.7 / 9.7 |
| 10.2% | — | — | — | 9.30 | 4.6 / 10.1 |
| 12.2% | 0.00 / −0.58 / +0.52 / +0.05 / +0.22 / +0.32 | +0.09 | −0.74 | 8.98 | 5.5 / 10.5 |
| 14.2% | −0.02 / −1.17 / +1.04 / +0.08 / +0.44 / +0.61 | +0.16 | −1.49 | 8.67 | 6.5 / 10.8 |

*SYNTHETIC – NOT ADIC DATA.* Paired SEs are $0.01–0.03bn. Under Mix B, P(red) moves by ≤ 0.02pp; under do-nothing a 14% share cuts M6's P(red) by 0.8pp. The objective is flat (≤ 13bp a year either way) and its sign depends on the model: M2 wants less RA, while M3, M5 and M6 want more. No Tier-1 row binds. **The 8–12% range is not contradicted, but it is a judgment band, not an optimizer output.**

**Pacing envelope** (reduced H, pooled M1–M5, Mix B, θ\*, 10 SAA replications). Liquidity rows are slack; the risk dual is 0.43–0.58, so charges are risk charges.

| Year-1 envelope ($bn [range]) | Real estate | Infrastructure | ENR | RA total (plan 1.20) |
|---|---|---|---|---|
| Envelope | 0.60 [0.30–0.90] | 1.20 [cap] | 0.00 [0–0.13] | **1.80 [1.50–2.10]** |
| Charge / α, bp per NAV-year | 116 / 75 | 71 / 162 | 33 / −7 (after a 150bp draw-surplus hurdle) | |

*SYNTHETIC – NOT ADIC DATA.* **The optimizer's RA split is ≈33 / 67 / 0, not 45 / 45 / 10.** It confirms the direction (indexed infrastructure, no new unhedged ENR), and the infrastructure cap binds. Over five years the split barely matters: against the census split, 45/45/10 changes CE by ≤ $0.005bn and 30/60/10 by +$0.002–0.010bn. Publish the envelope as the binding quantity and keep 45/45/10 as a pacing direction.

## 5. Attribution: DVA_RA on V\*

$$\mathrm{DVA}_{RA,t}=\sum_{i\in RA}\big[V^*_{i,t}-V^*_{i,t-1}+CF_{i,t}\big]-\sum_iV^*_{i,t-1}\big[r_f+\hat\beta^{d}_{i,t}\,(r^{FB}_t-r_f)\big]-\mathrm{FTP}^{vint}_{RA}-\lambda_R\mathrm{RC}_{RA}-\mathrm{CLC}_{RA}+\mathrm{CR}_{RA}$$

- **V\*** is RAME's nowcast (RA §8.2).
- **CF** is external cash: income, exits, redemptions and sale proceeds, less calls, protective calls and cures. Sales and redemptions count at transaction price, so selling below V\* is a loss and redeeming above it a gain. Intra-ADIC transfers carry fair value on both legs (V2).
- **β̂^d** is the three-step desmoothed equity beta (Couts, Gonçalves & Rossi 2024), re-levered on the actual debt path. The funding basket is cash plus β̂^d × equity, plus unlevered listed REIT and infrastructure legs once licensed.
- **Charges:** FTP^vint_RA prices scheduled flows; CLC_RA prices cures, protective calls and distribution stops. Each is charged once (main §4.11).
- **Pay** stays linear (b ≤ 0.005) on DVA_RA with multi-year vesting; reported-NAV DVA is disclosed, never paid.

**Why V\*, quantified** ($bn; NAV-weighted desmoothed β 0.49, observed β 0.21):

| | On V\*, desmoothed β | Reported NAV, observed β | Reported NAV, desmoothed β |
|---|---|---|---|
| T4′ at θ\* (U16), year 1 | −3.82 | +0.64 | +2.53 |
| T4′ at θ\* (U16), year 2 | −1.19 | −4.90 | −6.30 |
| Monte Carlo M1, Mix B: year-1 mean; 5-year P50 | +0.36; +2.34 | +0.47; +3.68 | +0.29; +2.27 |
| Monte Carlo M6, Mix B: same | −0.03; +1.09 | +0.17; +0.58 | +0.68; +1.16 |

*SYNTHETIC – NOT ADIC DATA.* The year-1 T4′ gap is $4.5bn with consistent betas and $6.3bn with a desmoothed basket on reported marks. It reverses in year 2, so annual pay on reported NAV would pay for the stale year. In base worlds the reported basis also books beta as alpha: the five-year mean gap is +$1.1bn in M1 and −$0.6bn in M6, and the year-1 gap runs from −$2.8bn to +$3.1bn (P5–P95). Some under-performing private-fund managers also inflate reported returns around fundraising (Brown, Gredil & Kaplan 2019) [S]. The mark that drives pay must therefore be V\*.

## 6. The tenth Shapley player and the RA fan

**Players.** PE, SEC, CS, CO, PM, PC, OVL, TPA, CF and RA.
- **RA on:** the stage pacing corridor (1.0 / 0.375 / 0.25); open-end notices at Amber; pre-arranged JV sell-downs in the amber step (controlled share only, ≤ 40% of controlled NAV, 20% in crisis, at 0.95 / 0.92 / 0.80); cash-outs at maturity (controlled direct debt, Amber, not crisis); the t0 ENR SELL.
- **RA group-off baseline:** HOLD plus plan pacing ($1.2bn a year), with none of the above. Cures are paid under ϖ = 1, and forced RA sales (after co-investment in the red step) and the emergency pro-rata sale remain.

**Exact ten-player values.** Book U16 at θ\*, Mix B, current triggers. Each model runs 1,024 coalitions × 10,000 CRN paths, 25–27 minutes on 23 workers.

| Player | ΔP(red), pp: M1 / M4 / M6 | ΔCE, $bn: M1 / M4 / M6 |
|---|---|---|
| CF | −7.4 / −13.5 / −18.0 | +0.06 / +0.17 / +0.11 |
| Public Markets | −7.0 / −12.7 / −16.9 | −0.67 / −0.64 / −1.60 |
| PE | −3.3 / −6.3 / −8.0 | +0.61 / +1.08 / +2.06 |
| **Real Assets** | **−2.3 / −4.3 / −5.2** | **+0.26 / +0.50 / +1.09** |
| Private Credit | −1.9 / −3.4 / −4.3 | −0.02 / +0.11 / +0.29 |
| Overlay | −1.1 / −1.1 / −3.6 | +1.66 / +2.31 / +6.23 |
| Co-investment | −1.5 / −2.5 / −3.1 | +0.18 / +0.40 / +0.94 |
| TPA | −0.5 / −0.4 / −3.0 | +0.97 / +1.93 / +8.00 |
| Capital Solutions | −1.2 / −2.2 / −2.7 | −0.05 / −0.06 / +0.07 |
| Secondaries | −0.8 / −1.5 / −1.9 | +0.16 / +0.23 / +0.46 |
| **Total v(N) − v(∅)** | **−26.9 / −48.0 / −66.8** | **+3.17 / +6.03 / +17.65** |

*SYNTHETIC – NOT ADIC DATA.* Σφ equals v(N) − v(∅) to 10⁻¹⁴. Path SEs are 0.02–0.18pp on P(red) and $0.01–0.35bn on CE (Real Assets: ≤ 0.06pp, ≤ $0.04bn).
- **Rank and share.** Real Assets is fourth on both metrics, with 8–9% of the P(red) reduction and 6–8% of the CE gain. Against gap_04's nine players on the v1 book (−24.8 / −48.3 / −66.2pp), PE's and co-investment's credits fall most (M6: −9.7 → −8.0 and −4.3 → −3.1pp).
- **Stand-alone credit would be 2–3× larger** on P(red) and 2.5–4× larger on CE, because notices and JV sell-downs substitute for CF and Public Markets levers. The interaction index is 0.9–1.6 on P(red) and 1.2–2.1 on CE.
- **The CE gain is insurance.** RA's φ on E[W̃] is −$0.21 / −0.02 / +0.17bn, and it includes the ENR SELL, whose last-in cost is $0.18–0.25bn of CE (§7). The playbook trims CVaR95 of 24-month cures by $0.07–0.08bn.
- **P = 32 antithetic permutations** (Castro et al. 2009; 290 of 1,024 evaluations) cover the exact value 90–98% of the time for the worst-covered player (RMSE ≤ 0.63pp and ≤ $0.10bn).

**RA fan** (U16, Mix B; $bn):

| | P(RA net cash < 0), years 1→5 | 5y cash P5 / P50 / P95 | NAV y5 P50 | 5y DVA on V\* P5 / P50 / P95 |
|---|---|---|---|---|
| M1 | 8 / 14 / 15 / 16 / 15% | 0.06 / 5.76 / 9.45 | 19.7 | −3.38 / 2.34 / 6.49 |
| M6 | 15 / 21 / 21 / 21 / 20% | −1.20 / 3.64 / 7.48 | 17.0 | −4.59 / 1.09 / 5.26 |
| M1 / M6, group-off | 73 / 53 / 39 / 28 / 22%; 84 / 73 / 59 / 43 / 31% | | | |

*SYNTHETIC – NOT ADIC DATA.*
- **Without its playbook** RA is a net cash user in year 1 on 73–84% of paths (−$0.26bn to −$0.46bn). Open-end notices ($3.3–4.1bn over five years) and the ENR SELL ($0.56bn) make it a source.
- **Do-nothing P(red)** is 1.45% (M1) / 11.6% (M6) at U16 and 0.83 / 7.9% at U11 (v1: 1.60 / 14.5%).
- **Mix B** gives 0.00% in M1–M5 and 0.04% in M6 (0.10% with RA off).

## 7. Confirmatory sealed run for the ENR SELL

**Protocol.** Registered and hashed before the run (`ra_enr_protocol.json`, SHA-256 `d01d542d…3a1eee`).
- **Action and control:** SELL $0.70bn of fund-held levered upstream at t0 at 0.80 of reported NAV (the buyer assumes the unfunded), against HOLD with everything else identical.
- **Setting:** Mix B, ten players, book U16, the survival proxy at θ\*; six worlds × 50,000 fresh paths, with seeds disjoint from every screening run.
- **Decision rule (intersection–union across worlds):** (i) CE non-inferiority, the lower 95% bound of ΔCE ≥ −0.5bp of NAV a year in every world; (ii) Tier-1 non-inferiority, the upper bound of ΔP(red) ≤ +0.10pp; (iii) purpose, the oil delta inside the 10m-bbl hard budget and ΔE[W̃ | glut or demand bust within 8 quarters] > 0, with its lower bound > 0, in at least two worlds. The 15bp materiality hurdle for return claims (main §5.4) cannot apply to a 0.4%-of-NAV action and is not used.

| Variant | ΔCE, bp of NAV a year, M1–M6 (lower 95%) | ΔP(red), pp | ΔE[W̃ \| wrong-way], $bn | Oil delta at $70 | Label |
|---|---|---|---|---|---|
| **Base: $0.70bn at 0.80** | −1.6 to −2.8 (−1.8 to −3.0) | 0.00 (upper ≤ 0.006) | +0.06 to +0.14 in M1–M5; −0.03 in M6 | 12.2 → 5.8m bbl | **NOT ESTABLISHED** |
| Bid 0.75 / 0.85 | −2.1 to −3.2 / −1.1 to −2.3 | 0.00 | −0.06 (M6) to +0.09 / +0.02 to +0.20 | 5.8m | NOT ESTABLISHED |
| Size $0.6bn / $0.8bn | −1.4 to −2.4 / −1.7 to −2.7 | 0.00 | | 6.7 / 4.9m | NOT ESTABLISHED |
| Plan = do-nothing | −1.8 to −3.2 | **−0.05 to −0.29** (upper < 0) | | 5.8m | NOT ESTABLISHED |
| Extension 0 | −1.6 to −2.8 | 0.00 | | 5.8m | NOT ESTABLISHED |

*SYNTHETIC – NOT ADIC DATA.* Criteria (ii) and (iii) pass in every variant; (i) fails in all six worlds.

**Reading.**
- **Why it loses.** The sale gives up $0.14–0.25bn of five-year CE by locking in a 20% discount on a position carried at reported NAV. In RA §7.4's notation that is an economic-value ratio θ̂ = 1, which is not the stress index θ. The wrong-way benefit, $0.06–0.14bn on the half of paths with a glut or demand bust, does not repay it, and in M6 it is negative.
- **Break-even bid.** Interpolating the bids, CE breaks even at 0.95–1.10 of reported NAV. The sale pays only at a bid at least equal to the funds' strip-based θ̂, which RAME has not yet estimated.
- **Liquidity.** It lowers P(red) only without the revolver and band, and at a CE cost. That matches the ladder card: SELL under R0, HOLD under R1 (reservation 0.802).
- **Owner need.** The W̃-based CE does not weight the owner's fiscal need. The draw-surplus hurdle H_j (RA §9.3) does, in the card but not in the Monte Carlo.

**Decision.** Do not execute at 0.80. The budget is measured at the generator's current state (RA §9.3). Today's Gulf-war delta (≈9.2m bbl [C]) is inside the 10m hard budget. It breaches only if oil returns toward $70 (12.2m), and hedging the $0.27bn direct position alone leaves ≈10.7m.
- (a) Re-submit under the hashed protocol with RAME's strip-based θ̂ for these funds and a live bid. Execute if the bid is at least about θ̂.
- (b) Pre-authorise a budget-restoring sale, plus the asset-level hedge on direct upstream, if the current-state delta crosses 10m. This run prices that constraint at 1.6–2.8bp a year per $0.7bn sold at 0.80.
- (c) Make no new unhedged oil-linked commitments.

## 8. Patches, memo and design implications

**Applied in place** (marked "patch, ra_gap_01") in `00_SYNTHESIS.md` and `01_GROUPS_SYNTHESIS.md`. `03_REAL_ASSETS_INTEGRATION.md` lists them, plus the edits proposed for the Integrate step.

**Design implications** (by target section):
1. **RA §1 finding 2, §4.7, §6.3:** a T4′ drain of −$4.5bn over 24 months at θ\*; relief against PE is negative.
2. **Main §4.9, groups §2.4:** θ\*(v2) is 0.835 / 0.877, with the RA θ components as hashed convention fields; SH_TP is 18 / 20 months; IC decision 1 is re-ratified on the eight-group book.
3. **RA §10:** FTP_RA of 2 / 21bp on scheduled flows; hurdle 13 / 144bp; CLC_RA for cures, with c_buf following the state's marginal-lever carry; B_RA from the pool row.
4. **RA §2.3:** 8–12% is a judgment band; the $1.8bn infrastructure-led envelope binds.
5. **RA §8.5, groups §4.3:** DVA_RA on V\*; reported-NAV DVA is never paid.
6. **Groups §4.3, main §4.11:** ten players, the §6 baseline, exact enumeration (≈26 minutes per model).
7. **RA §1 decision 2:** the ENR SELL becomes contingent on a bid ≥ θ̂ (re-tested under the hashed protocol), a breach of the 10m hard budget, or R0. No new unhedged oil-linked commitments.
8. **Gates:** V-RA-CTRL (`test_v_ra_ctrl.py`); V-RA-θ (RA components pass through G15's values at θ 0.76); V-RA-CLC (CVaR95 of joint-path cures, never summed cohort P95s).

## 9. Limitations

- **Assumed dynamics.** The models are proxies. RA betas, premia, crisis drags, availability and extension are [I], and θ\* and the RA row move with them (§2 bridge).
- **Nowcast.** V\* is truth plus noise. A lagging nowcast would shrink the DVA gap but not close it.
- **Scope of the optimizer outputs.** The NAV band and split rest on premia set to M1 CMAs, and the reduced H is a one-year LP. Shapley values are exact for M1, M4 and M6 on U16 only.
- **Fund behaviour.** The fund-level module treats GPs mechanically, and ϖ = 1 throughout.
- **Census.** U16 on $34bn implies a young PE book (U/NAV 0.48), close to the v1.0 history that failed V6; U11 is the internally consistent figure. The user's choice between them stands.

## Sources

Accessed 2026-10-19; Consensus was not used.
- Brown, G. W., Gredil, O. R. & Kaplan, S. N. (2019). Do private equity funds manipulate reported returns? *Journal of Financial Economics* 132(2), 267–297. https://doi.org/10.1016/j.jfineco.2018.10.011 (checked on Crossref; NBER WP 22493, 2016, https://www.nber.org/papers/w22493).
- Couts, S., Gonçalves, A. S. & Rossi, A. (2024). Unsmoothing returns of illiquid funds. *RFS* 37(7), 2110–2155. https://doi.org/10.1093/rfs/hhae006 (via RA §15).
- Glancy, D. (2026). Pretend or amend? On evergreening in CRE. FEDS 2026-025. https://doi.org/10.17016/FEDS.2026.025 (via RA §4.5 and G10).
- Castro, J., Gómez, D. & Tejada, J. (2009). Polynomial calculation of the Shapley value based on sampling. *Computers & Operations Research* 36(5), 1726–1730. https://doi.org/10.1016/j.cor.2008.04.004 (via groups gap_04).
- Internal: RA synthesis v1.1; G10–G15 dossiers and verification logs; groups gap_01 (Phase I/II, L4), gap_02 (census v1.1), gap_04 (engine, Shapley); main gap_02 (s\*(θ), θ\* rule) and §5.4.
