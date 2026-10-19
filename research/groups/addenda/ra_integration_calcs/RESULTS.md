# Real Assets integration re-run: results

**Date:** 2026-10-19 · **Status:** SYNTHETIC prototype on SYN-ADIC-177; no ADIC data · **Results:** `ra_integration_results.json` (stage files `ri_*_results.json`, console logs `ri_*_stdout.txt`) · **Interpreter:** project `.venv` Python 3.12, `-I -B`, seed 20261018.

**Code:** this folder. The `ri_*.py` drivers sit on copies of the original engines; no original was modified:
- gap_02's `t1_engine.py` and `gap02_study.py`, byte-identical. `phase1_demo.py` is copied for reference only; the group Phase I in `ra_ladder` supersedes its single-row version.
- Adapted copies (marked `ri:`): groups gap_01 `g01_core.py` (reproduction reference), GS `gs_group_cashmap.py`, and ra_gap_01's `ra_book` / `ra_ladder` / `ra_module` / `ra_engine`.
- Unmodified copies: stream-G7, and groups gap_02 `rfta_v2_book.py` with the sealed history.

> **SYNTHETIC – NOT ADIC DATA.** Every figure comes from the working allocation (context §1A), the census of record and design defaults [I]. M1–M6 are stylised proxy models. Context §1A was re-read at the end of the run and is unchanged: Real Assets $18bn is still a working size, the user chose census v1.1 ($16.4bn PE unfunded), and both PE-unfunded readings are reported.

## Books and θ\*

| Book | PE NAV / unfunded ($bn) | Real Assets | Total unfunded | θ\* (worst model, P99.6 G\*) | SAA range (pooled) | Oct-2026 state |
|---|---|---|---|---|---|---|
| v1 as published (census v1.0, anchor) | 52 / 27.4 | – | 38.0 | 0.759 (M6, 11.10) | 0.759–0.802 (0.782) | – |
| **v1: seven groups, census v1.1** | 52 / 16.4 | – | 27.0 | **0.830** (M6, 5.34) | 0.830–0.878 (0.851) | 0.618 |
| **v2 U16** (user's $16.4bn kept) | 34 / 16.4 | 18 / 4.0 | 31.0 | **0.835** (M6, 9.30) | 0.835–0.869 (0.850) | 0.643 |
| **v2 U11** (v1.1 U/NAV 0.32 rescaled) | 34 / 10.9 | 18 / 4.0 | 25.5 | **0.877** (M6, 6.62) | 0.877–0.916 (0.897) | 0.674 |

*SYNTHETIC – NOT ADIC DATA.* θ\* follows the canonical rule: the worst model's quantile of the action-free 24-month gap at 1 − 0.40%, with 50,000 paths per model, inverted on each book's own ladder curve. The v1 census-v1.1 θ\* is new. The v2 values reproduce ra_gap_01.

**Validation (all pass):**
- Seven copies are byte-identical to the originals.
- Ladder replica against `g01_core` and `t1_engine.ladder`: maximum difference 0.0 on 48 cases.
- Published v1 T4′ reproduced: SH_TP 17, G\* 11.1, facility 13.9, pacing rule 6.1 / 20 months, band 0 / 29 months, d₀ 11.3.
- ra_gap_01's v2 ladder, d₀ and Monte Carlo runs reproduced exactly.
- G15 Real Assets row reproduced: +0.40 / −0.16 / −1.32 / −2.46.
- Cash map: census v1.0 and sealed v1.1 legs exact; published T4′ column reproduced (−16.4 / −28.7).
- Engine in t1 mode is identical to `t1_engine.simulate`. gap_02's certified mixes reproduced: Mix A 0.98% / 5.80%, Mix B 0.79% / 6.46%.
- `dcr_t0` reproduced (1.653).

## 1. Cross-group cash map (net $bn, 12 / 24 months; + = cash to Corporate Finance)

| Group | v1 base | v1 drought | v1 T4′ (0.830) | v2 U16 base | v2 U16 drought | v2 U16 T4′ (0.835) | v2 U11 base | v2 U11 drought | v2 U11 T4′ (0.877) |
|---|---|---|---|---|---|---|---|---|---|
| PE funds | +3.62 / +7.10 | −0.85 / −1.37 | −7.54 / −14.77 | +0.46 / +0.96 | −2.44 / −4.61 | −7.45 / −14.19 | +2.31 / +4.53 | −0.61 / −1.01 | −5.42 / −10.98 |
| Secondaries | +2.19 / +4.38 | +1.17 / +2.64 | −1.90 / −3.22 | +2.19 / +4.38 | +1.17 / +2.64 | −1.90 / −3.23 | +2.19 / +4.38 | +1.17 / +2.64 | −1.96 / −3.34 |
| Co-investment | +3.02 / +5.48 | +1.74 / +3.23 | −1.68 / −3.13 | +3.02 / +5.48 | +1.74 / +3.23 | −1.69 / −3.14 | +3.02 / +5.48 | +1.74 / +3.23 | −1.72 / −3.21 |
| Capital Solutions | +0.58 / +0.96 | +0.51 / +0.84 | −0.19 / −0.56 | +0.58 / +0.96 | +0.51 / +0.84 | −0.19 / −0.56 | +0.58 / +0.96 | +0.51 / +0.84 | −0.20 / −0.58 |
| Private Credit | +1.22 / +2.41 | +1.12 / +2.21 | −0.67 / −0.77 | +1.22 / +2.41 | +1.12 / +2.21 | −0.67 / −0.78 | +1.22 / +2.41 | +1.12 / +2.21 | −0.69 / −0.81 |
| **Real Assets** | – | – | – | **+0.40 / +0.89** | **−0.16 / −0.20** | **−2.50 / −4.49** | +0.40 / +0.89 | −0.16 / −0.20 | −2.60 / −4.64 |
| **Private book** | **+10.64 / +20.34** | **+3.70 / +7.54** | **−11.98 / −22.46** | **+7.87 / +15.07** | **+1.95 / +4.11** | **−14.40 / −26.39** | **+9.72 / +18.65** | **+3.78 / +7.70** | **−12.60 / −23.54** |
| Overlay (same in v1, v2) | +0.31 / +0.62 | +0.31 / +0.62 | −3.01 / −1.40 | +0.31 / +0.62 | +0.31 / +0.62 | −3.01 / −1.41 | +0.31 / +0.62 | +0.31 / +0.62 | −3.05 / −1.46 |
| Before payout | +10.77 / +20.60 | +3.83 / +7.81 | −15.16 / −24.22 | +8.00 / +15.34 | +2.08 / +4.37 | −17.59 / −28.15 | +9.85 / +18.91 | +3.91 / +7.97 | −15.82 / −25.36 |
| Liquid-book funding: 7.5% payout; T4′ at canonical draws | 2.5 / 6.0 | 9.4 / 18.7 | 32.9 / 54.3 | 5.3 / 11.2 | 11.2 / 22.2 | 35.3 / 58.3 | 3.4 / 7.6 | 9.4 / 18.6 | 33.5 / 55.5 |

*SYNTHETIC – NOT ADIC DATA.*

- **How each state is built.**
  - *Base and drought:* the stream-G7 engine for the non-PE groups, the RFT-TA v2 vintage leg for PE (own pace: $5.34bn for v1 and U16, $3.55bn for U11), and G15's engine for Real Assets.
  - *T4′:* the canonical ladder at each book's θ\*.
  - *T4′ at the common θ = 0.76:* private book −11.42 / −21.47 (v1), −13.69 / −25.18 (U16), −11.57 / −21.79 (U11).
- **v2 minus v1, private book:**
  - U16: base −2.77, drought −1.75, T4′ −2.42 (12 months) / −3.93 (24 months).
  - U11: base −0.92, drought +0.08, T4′ −0.62 / −1.08.
- **Why v2 changes.**
  - Under T4′, Real Assets drains far more than the PE it replaces: RA is −4.49 over 24 months, while PE's drain falls by only $0.58bn.
  - With the user's $16.4bn kept on a $34bn PE bucket (U/NAV 0.48), PE drought distributions fall by a third ($4.63bn → $3.03bn) while calls stay at $5.47bn.

## 2. T4′ facility need, survival on Treasury + Public Markets, hard-row gap ($bn; months)

| Book @ θ | G\* | SH_TP | Facility: do nothing | + pacing rule (SH_TP) | + owner band (SH_TP) | Rule + band | Hard-row gap d₀ | Mix A / Mix B 24m headroom |
|---|---|---|---|---|---|---|---|---|
| v1 published @0.759 | 11.1 | 17 (Red) | 13.9 | 6.1 (20) | 0 (29) | > 36 | 11.3 | +12.0 / +10.8 |
| **v1 census v1.1 @0.830** | 5.3 | 21 (Amber) | **6.7** | 0 (30) | 0 (> 36) | > 36 | **5.5** | +17.3 / +11.0 |
| **v2 U16 @0.835** | 9.3 | 18 (Amber edge) | **11.6** | 3.7 (22) | 0 (32) | > 36 | **9.5** | +14.0 / +10.8 |
| **v2 U11 @0.877** | 6.6 | 20 (Amber) | **8.3** | 0.2 (24) | 0 (> 36) | > 36 | **6.8** | +16.8 / +10.9 |
| v1 / U16 / U11 @0.76 (common θ) | 4.1 / 7.8 / 4.4 | 22 / 19 / 21 | 5.1 / 9.8 / 5.5 | 0 (33) / 2.0 (23) / 0 (31) | 0 (> 36) / 0 (35) / 0 (> 36) | > 36 | 4.2 / 8.0 / 4.6 | Mix A +17.5 / +15.3 / +17.5; Mix B +11.2 / +11.0 / +11.2 |
| v1 / U16 / U11 @pooled θ (0.851 / 0.850 / 0.897) | 5.7 / 9.6 / 7.0 | 20 / 18 / 20 | 7.1 / 12.0 / 8.7 | 0 (28) / 4.0 (22) / 0.65 (24) | 0 (> 36) / 0 (32) / 0 (> 36) | > 36 | 5.9 / 9.8 / 7.2 | – |

*SYNTHETIC – NOT ADIC DATA.* Mix A and Mix B survive beyond 36 months on T + P + F in every book.

- **Definitions.** The facility need is the maximum 24-month gap ÷ 0.80. d₀ is max(0, −min headroom) with nothing signed and no top-up. Its binding month is 24 in every book.
- **Phase I.** u\* = 0 in every book and state (R0x / R0 / R1): group levers alone restore T4′, so the book is in execution recovery, not structural recovery.
- **L8 at t0.** v1 0.751 ($8.6bn headroom); U16 0.774 ($4.6bn); U11 0.743 ($10.1bn).
- **Bridge for the do-nothing facility need:**
  - published v1, $13.9bn → census v1.1, $6.7bn: the census change alone gives −$7.2bn and moves readiness from Red (17 months) to Amber (21);
  - → v2 U16, $11.6bn: the Real Assets carve-out at constant PE unfunded adds **+$4.95bn**, or +$4.7bn at θ 0.76, and survival falls from 21 to 18 months;
  - v2 U11: at constant PE U/NAV the carve-out adds only **+$0.4bn at θ 0.76, or +$1.6bn at its own θ\***. Most of U16's deterioration comes from keeping $16.4bn of PE unfunded on the smaller bucket.
  - ra_gap_01's "Red → Amber" was the census change, not Real Assets.
- **v2 U16 sensitivities at θ\*.**
  - G15's RA leg (reproduction mode): facility $9.2bn.
  - RA calls ×1.0: $10.75bn.
  - Extension 0: $11.73bn.
  - First-order, with ra_gap_02's structural RA row in place of the Tier-1 row: fac′ ≈ fac − (R^T1₂₄ − R^struct₂₄)/0.80, valid because month 24 binds. That gives 11.63 − (4.49 − 1.64)/0.80 ≈ **$8.1bn** (≈ $6.7bn with structural calls); for U11, ≈ $4.5bn. This is not an engine run: the structural row was computed at θ 0.76 conventions.

## 3. Red-event probability, 5 years (%, P(red); M6 is the stressed class)

| Book | Playbook-free (gap_02 engine, 50k): do nothing M1 / M6 | Mix A M1 / M6 (CP); max CP M1–M5 | Mix B M1 / M6 (CP); max CP M1–M5 | Integrated with playbooks (20k): do nothing / Mix A / Mix B, M1 / M6 |
|---|---|---|---|---|
| v1 published | 7.77 / 37.18 | 0.20 / 5.80 (5.97); 0.98 | 0.15 / 6.46 (6.64); 0.79 | 1.52 / 14.74; 0.00 / 0.07; 0.00 / 0.07 |
| **v1 census v1.1** | 4.95 / 28.83 | 0.05 / **3.30** (3.44); 0.39 | 0.06 / **4.05** (4.20); 0.32 | 0.50 / 7.94; 0.00 / 0.01; 0.00 / 0.02 |
| **v2 U16** | 8.36 / 36.20 | 0.23 / **5.37** (5.53); 0.94 | 0.17 / **6.16** (6.34); 0.81 | 1.41 / 11.73; 0.00 / 0.03; 0.00 / 0.04 |
| **v2 U11** | 6.77 / 31.98 | 0.13 / **4.08** (4.23); 0.61 | 0.10 / **4.95** (5.12); 0.52 | 0.79 / 8.14; 0.00 / 0.01; 0.00 / 0.03 |
| v2 U16, RA playbook off (integrated) | – | – | – | 2.23 / 15.51; 0.00 / 0.12; 0.00 / 0.11 |

*SYNTHETIC – NOT ADIC DATA.* CP is the one-sided 95% Clopper–Pearson bound.

- **M1–M5 gate (≤ 1%).** Both mixes certify in every book. v2 U16 Mix A is within 0.06pp of the gate.
- **M6-class 5% capacity.**
  - v1 on census v1.1 passes with either mix.
  - The carve-out at U16 makes both mixes fail again (5.37% / 6.16%).
  - At U11, Mix A passes (4.08%) and Mix B passes on the point estimate but not on the CP bound (5.12%).
- **Integrated engine.** The group playbooks (including Real Assets' notices and JV sell-downs) keep Mixes A and B at or below 0.04% in M6 for every book. Real Assets' own playbook is worth 0.8 / 3.8pp of do-nothing P(red) in M1 / M6 at U16.

## 4. Oil sensitivity: Tier-1 oil-crisis state (OC, G12 §6.9) and Real Assets oil loadings

**The OC state never binds.**
- Headroom stays ≥ +$19.8bn in every book and variant, including −5% equities and 50% facility credit; facility 0; SH_TP > 36.
- The relevant shortfall is therefore the cash that Treasury + Public Markets must fund over 24 months (NCO24): v1 $31.8bn; v2 U16 $35.0bn with RA oil loadings off and $35.5bn with them on; U11 $32.6bn / $33.1bn.

| Change from RA oil loadings (same for U16 and U11) | RA 24m OC cash | of which RBL cures | ΔNCO24, ladder | Δ month-24 headroom | ΔT8 DCR, SG+PS, do nothing | OC×DB: Δ T4′ facility |
|---|---|---|---|---|---|---|
| **With ENR** (all RA oil loadings) | **−0.62** | 0.37 | **+0.54** | −0.49 | −0.018 (1.784 → 1.766; U11 1.896 → 1.876) | **+0.42** (11.63 → 12.05; U11 8.28 → 8.70) |
| **Without ENR** (GCC real estate + infrastructure midstream only) | **−0.015** | 0 | **+0.004** | ≈ 0 | −0.0001 | 0 |
| ENR only | −0.61 | 0.37 | +0.53 | −0.50 | −0.018 | – |
| With ENR, RBL at P90 / conditional-mean floor | −0.60 / −0.49 | 0.34 / 0.20 | +0.51 / +0.40 | – | – | – |

*SYNTHETIC – NOT ADIC DATA.*

- **Ladder versus cash.** ΔNCO24 is smaller than the RA cash change because lower RA marks cut the year-2 draw by $0.09bn and the floor by $0.04bn.
- **T8 still passes.** DCR is ≥ 1.25 (green) in every book: v1 1.856; under Mix B 2.95 / 2.75 / 2.99.
- **First-order check:** ΔS₂₄ ≈ Σ_j V_j y_s(1 − m_j)·2 + V_CE·real_d·[1 − 0.3(1 − u_CE)]·2 + C_RBL + V_GCC·y_GCC·(0.05 + 0.15) + 0.10·V_INF·y_INF·0.05·2
  - With ENR: 0.119 + 0.163 + 0.371 + 0.011 + 0.003 = **$0.67bn**, against the engine's $0.62bn (the engine also nets a $0.06bn call offset).
  - Without ENR: $0.014bn, against the engine's $0.015bn.
- **Before any oil loading.** The v2 book already needs +$3.2bn (U16) / +$0.8bn (U11) more 24-month funding than v1 in OC.
- **Stochastic cross-check** (playbook-free engine, 50k paths, M1–M6, U16 and U11; RA oil channels on against off):
  - P(red) moves by −0.004 to +0.08pp under do-nothing and by −0.004 to +0.04pp under Mix B.
  - On wrong-way paths (supply glut or demand bust within 8 quarters, 52% of paths) it rises by +0.04 to +0.21pp under do-nothing and by 0.00 to +0.10pp under Mix B.
  - G\* P99.6 moves within ±$0.06bn, which is noise.
  - E[W̃ | wrong-way] falls by $0.52–0.60bn over five years.
  - ENR's oil channels account for most of the P(red) change. This matches ra_gap_03's ≤ 0.004pp per m bbl × 11.2m bbl. This engine has no RBL cures, so it understates the ENR tail that the OC row carries.

## Assumptions (all [I] unless stated)

1. **Census.**
   - Census v1.1 is used for v1 and v2 U16 (context §1A); U11 rescales v1.1's U/NAV of 0.32 to the $34bn bucket.
   - The non-PE unfunded split is census v1.0's (Secondaries 3.5 + 0.4 deferred, Co-investment 1.5, Capital Solutions 1.2, Private Credit 3.0 + 1.0), unchanged in v1.1.
   - Private NAV stays at $106bn.
2. **Real Assets book.**
   - The ten census sleeves of record (RA §11: $18bn / $4bn; real estate / infrastructure / ENR 50 / 36 / 14%).
   - Plan pacing of $1.2bn a year (10% of the $12bn plan), taken out of PE's share (60% → 50%).
3. **Canonical T4′ and the Tier-1 RA row.**
   - T4′ = s\*(θ\*) on the gap_02 conventions, with the published draw, credit, floor, hedge-fund and overlay conventions.
   - The RA leg is ra_gap_01's θ-indexed Tier-1 row, which RA14 says governs: RAME marks; lender availability 0.97 − 0.52θ; extension 0.35(1 − θ); fund-level waterfall; calls (1 + 0.5θ) × 28%; exits 0.45(1 − θ) × drought; 17% a year of debt maturing.
4. **Cash map.**
   - Base and drought use the G7 rates. PE uses RFT-TA v2 cohorts from the sealed history, with NAV rescaled to $34bn and unfunded to $16.4bn or $10.9bn in v2; the T4′ PE leg is rate-based, as published.
   - The overlay and Corporate Finance opex lines are the published reconciled 12-month values, doubled for 24 months. They are identical in v1 and v2.
5. **P(red).**
   - Policies are gap_02's: Mix A = revolver $15bn, pacing $6bn + rule, reserve 14%; Mix B = revolver $10bn, rule, band, reserve 8%, $5bn hedge-fund notice. Seed 20261018 throughout.
   - In the playbook-free runs, RA follows the pacing rule, but its notices, JV sell-downs, cash-outs and ENR SELL are off.
   - The integrated v1 census-v1.1 runs use the sealed v1.1 PE vintage profile. This adapts the original, which fell back to the U 27.4 history.
6. **OC state.**
   - Specification from G12 §6.9 and RA §6.3: Brent −45% over six months, then $40–50; equities flat; drought exits; calls ×1.0; draws at the 10% cap for two fiscal years; no VM, no equity-tail monetisation and no opportunistic loss.
   - ENR sub-sleeves (RA §9.3 split) with cash multipliers: levered upstream 0 (swept), royalties 0.63, fee midstream 0.95, other 0.90. ENR exits ×0.30.
   - RBL cure at the Tier-1 SG/DB tail: CVaR95 = 41% of levered equity, with fund-held cures capped at $0.26bn of unfunded, paid 70% in months 6–11 and 30% in months 12–17. Direct non-upstream ENR debt refinances at LTV^max 0.40.
   - GCC real estate follows G15's supply-glut state; 10% of infrastructure is midstream (income ×0.95).
7. **DCR and OC×DB.**
   - The SG+PS DCR adapts `gap02_study.dcr_t0`, with book-specific NAV, unfunded and RA terms.
   - OC×DB is T4′ at θ\* plus the RBL cures and the further ENR income cut, added to the T4′ RA leg (approximate, additive).

## Caveats

- All figures are SYNTHETIC, and the Monte Carlo models are stylised proxies. The single-seed θ\* sits at the low end of each book's SAA band; pooled θ\* is about 0.02 higher. The pooled readings are in the table.
- The Tier-1 RA row is the conservative convention (RA14). The structural engine on the sealed tape would lower v2's facility need by ≈ $3.6–4.9bn (first-order estimate above). Re-anchoring the RA θ components on the tape remains open.
- Most of the v2 U16 penalty is the census choice: $16.4bn of PE unfunded kept on $34bn gives a young book (U/NAV 0.48). Under U11 the RA carve-out costs $0.4–1.6bn of facility.
- The OC state is a cash-funding stress, not a Tier-1 breach. The Tier-1-relevant oil reading is OC×DB. The stochastic module lacks RBL cures, and ra_gap_03's canonical oil generator was not re-run here.
- research/addenda/gap_01_calcs (the hedge-fund state-machine ladder) was not needed. The canonical T4′ uses gap_02's hedge-fund queue, and that ladder affects only the S1 and literal-T4 reverse-stress readings.

## Files

| Path | Contents |
|---|---|
| `ri_common.py` | Shared helpers |
| `ri_validate.py` | Reproduction checks → `ri_validate_results.json` |
| `ri_calib.py` | θ\* → `ri_calib_results.json` |
| `ri_cashmap.py` | Item 1 → `ri_cashmap_results.json` |
| `ri_ladder.py` | Item 2 → `ri_ladder_results.json` |
| `ri_mc.py` | Item 3 → `ri_mc_results.json` |
| `ri_oil.py` | Item 4 → `ri_oil_results.json` |
| `ri_summarize.py` | Collector → `ra_integration_results.json` |
