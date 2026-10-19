# Real Assets integration memo

## How the eighth group folds into the main report, the groups report and the design documents

**Date:** 2026-10-19 · **Status:** seeded by the Real Assets gap-fill step `research/groups/addenda/ra_gap_01.md` (total-portfolio decisions and attribution). The workflow's Integrate step extends §2–§4 with its own re-run (`research/groups/addenda/ra_integration_calcs/`) and the remaining edits. Edits marked **APPLIED** are already in the documents; all others are **PROPOSED** and are for the step that applies this memo, after the design workflow and the citation fixes. · **Inputs:** `02_REAL_ASSETS_SYNTHESIS.md` v1.1; `research/groups/addenda/ra_gap_01.md` and `ra_gap_01_calcs/` (JSON results); `01_GROUPS_SYNTHESIS.md` v1.1; `research/00_SYNTHESIS.md` v1.1.

> **SYNTHETIC-DATA NOTICE.** Every number below is computed on SYN-ADIC-177 under allocation v2 (context §1A: PE $34bn, Real Assets $18bn / $4.0bn unfunded; PE unfunded $16.4bn "U16" or $10.9bn "U11"). None is ADIC data. *SYNTHETIC – NOT ADIC DATA.*

---

## 1. Headline changes

| Item | Before (v1 seven-group book, or RA synthesis v1.1) | After (v2 eight-group book; ra_gap_01) |
|---|---|---|
| Groups / seats / Shapley players | 7 / 12 / 9 | **8 / 13 / 10** |
| θ\* (worst-model P99.6 rule) | 0.76 (pooled 0.79) | **0.835 at U16** (pooled 0.850); **0.877 at U11** (pooled 0.897) |
| SH_TP under T4′, do-nothing | 17 months (Red readiness) | 18 (U16, Amber) / 20 (U11) |
| Facility for 24 months: do-nothing / pacing rule / band | $13.9bn / $6.1bn / 0 | $11.6bn / $3.7bn / 0 (U16); $8.3bn / $0.2bn / 0 (U11) |
| Real Assets T4′ drain, 24 months | −$2.46bn (−$3.00bn upper) | **−$4.5bn** at θ\* (−$4.0bn with extension 0.35; −$3.8bn with calls ×1.0) |
| RA T4′ relief against PE | "−$0.3bn to +$0.2bn, includes zero" | **Negative**: RA drains more than PE at the same NAV |
| FTP_RA on holdings | "≈3–4bp or ≈66–81bp" (v1 duals, cures included) | Scheduled flows: **2.0bp** (revolver signed, μ 0.0113) / **20.5bp** (group levers, μ 0.124); 5.4 / 55.5bp if cures are included |
| Hurdle on new RA commitments | not published | 13bp (R1) / 144bp (R0) |
| CLC_RA | $5–14m a year (deterministic cures) | **$36–38m a year** (1.5% × CVaR95 of joint-path cures, $2.4bn; ≈20bp of RA NAV); cures are priced here once, never also in FTP |
| B_RA (24 / 12 months) | do-nothing drain 2.5–3.0 / 1.3–1.5 | L4 pool-row output: **4.26 / 2.36** (R1 plan), 4.03 / 2.22 (R0 plan), 3.95 / 2.38 (Mix B) |
| L8 at t0 | per dollar only ("RA adds $22bn vs $23.8bn") | **0.774, headroom $4.6bn** (U16); 0.743, $10.1bn (U11) |
| RA size 8–12% and split 45/45/10 | hand-set [I] | 8–12% is a judgment band (objective flat ±13bp a year over 6–14%); optimizer pacing envelope **$1.8bn a year, ≈33/67/0** |
| Asset-level cash-outs | "dominated" (conditional on unpublished duals) | Dominated in both states: 0.157 per $ of headroom on $0.03bn of t0 capacity |
| RA attribution basis | none | **DVA_RA on V\*** with a desmoothed basket; reported-NAV DVA disclosed, never paid (T4′ year 1: −$3.8bn on V\* vs +$0.6bn reported) |
| RA Shapley credit (M1 / M4 / M6) | none (nine players) | **−2.3 / −4.3 / −5.2pp** of P(red); **+$0.26 / 0.50 / 1.09bn** of CE; fourth of ten on both; stand-alone attribution would overstate it 2–4× |
| P(red), do-nothing, M1 / M6 | 1.60% / 14.5% | 1.45% / 11.6% (U16); 0.83% / 7.9% (U11); Mix B 0.04% in M6 |
| ENR SELL | Tier A on exploratory cards | **NOT ESTABLISHED** in the sealed run: −1.6 to −2.8bp a year of CE at a 0.80 bid in all six worlds; Tier-1 neutral; oil delta 12.2 → 5.8m bbl; break-even bid 0.95–1.10 of reported NAV |

*SYNTHETIC – NOT ADIC DATA.*

## 2. Edits to the groups report (`01_GROUPS_SYNTHESIS.md`)

**APPLIED (2026-10-19, marked "patch, ra_gap_01"):**
1. A banner after the synthetic-data notice: eight groups; RA in `02`, integration in `ra_gap_01` and this memo; 13 seats; ten players.
2. §4.3 Attribution: Real Assets uses V\* and a desmoothed basket; reported-NAV DVA never paid.
3. §4.3 Shapley protocol: ten players, 1,024 coalitions, and the RA group-off baseline.
4. §6 Validation gates: a V-RA-CTRL row extending V23.
5. §7.1: 13 seats, plus a Real Assets row in the group-head seat table.

**PROPOSED:**
6. **Title and §0–§2 wording.** Keep the title ("Seven-Group Synthesis": it specifies seven groups). Change "seven groups" to "eight groups" where the text describes ADIC rather than this report's scope (§1 opening, §2 heading and §2.1 table "Assets" row).
7. **§1 decision 1.** Re-ratify T4′ on the eight-group book: θ\* 0.835 (U16) / 0.877 (U11), pooled 0.850 / 0.897, with the RA θ components (income, value, LTV^max, availability, extension) as hashed convention fields (ra_gap_01 §2).
8. **§2.2 cash map.** Add the Real Assets row from RA §4.7, with the T4′ column restated at θ\* (−$2.5bn at 12 months, −$4.5bn at 24) and footnoted to the ra_gap_01 §2 bridge.
9. **§2.4 ladder.** Add a v2 block to the T4′ table (ra_gap_01 §2), the RA row to the L4 budget table (ra_gap_01 §3), and the v2 L8 values.
10. **§4.8 t0 table.** Add a Real Assets row (FTP on scheduled flows 2.0 / 20.5bp, plus CLC_RA ≈20bp for cures; hurdle 13 / 144bp; B_RA 4.26 / 4.03; ENR card HOLD / SELL), and note that in R0 the RA JV sell-down sets μ at 0.124.
11. **§4.4.** Add RA to the reduced-H envelope list (RA $1.8bn, infrastructure-led; RE 116 / infrastructure 71 / ENR 33bp risk charges).
12. **§4.9.** Add the eight-group P(red) line, the ten-player Shapley table (ra_gap_01 §6) and the RA fan.
13. **§9 questions.** Add "confirm Real Assets size, open-end terms and control rights" (pointing to RA §14).

## 3. Edits to the main report (`research/00_SYNTHESIS.md`)

**APPLIED:** a banner; eight groups in §1; thirteen seats in §1 finding 12, the architecture diagram, §3 L13, §5.7, §6.2 (text and a Real Assets seat row), §9 and §10; ten players in §4.11; DVA_RA on V\* in §4.11; V-RA-CTRL in §4.2 and §8.

**PROPOSED:**
1. **Finding 5 and §2.3(d).** Add the v2 survival row: SH_TP 18 / 20 months; facility $11.6bn / $8.3bn; pacing rule $3.7bn / $0.2bn; band 0.
2. **§4.9 T4′.** Add the RA components of s\*(θ) and θ\*(v2); keep literal T4 as a reverse stress.
3. **§4.4 instrument library.** Add the RA lever rows with costs per $ of headroom: JV sell-down 0.124, RA pacing stop 0.150, cash-out 0.157 on $0.03bn.
4. **§4.11.** Add the DVA_RA formula (ra_gap_01 §5).
5. **§7.1 calibration.** Add θ\*(v2), CLC_RA and the RA T4′ row.
6. **L3 (oil wrong-way).** Cite the ENR confirmatory result (ra_gap_01 §7): the wrong-way benefit of selling fund-held upstream is real ($0.06–0.14bn on wrong-way paths) but smaller than a 20% bid discount. The W̃-based CE does not weight owner fiscal need, so the draw-surplus hurdle must stay in the objective.

## 3A. Edits to the Real Assets synthesis (`02_REAL_ASSETS_SYNTHESIS.md`) (PROPOSED)

These are listed by target section in ra_gap_01 §8.
1. **§1 finding 2, §4.7, §6.3.** The T4′ drain is −$4.5bn over 24 months at θ\*, and relief against PE is negative.
2. **§2.3.** 8–12% is a judgment band; the binding quantity is the $1.8bn infrastructure-led envelope.
3. **§8.5.** DVA_RA on V\*.
4. **§10.** FTP_RA 2 / 21bp on scheduled flows, CLC_RA for cures and B_RA from the pool row.
5. **§1 decision 2, §9.3 and the specification card.** Replace "sell $0.6–0.8bn … (Tier A, after a confirmatory run)" with: the ENR SELL is NOT ESTABLISHED at 0.80 (ra_gap_01 §7). It becomes contingent on any one of:
   - a live bid ≥ θ̂, re-tested under the hashed protocol;
   - the current-state delta crossing the 10m hard budget;
   - liquidity priced at R0.

## 4. Edits to `design/ARCHITECTURE.md` and `design/BUILD_SPEC.md` (PROPOSED)

1. **Taxonomy and config.** Eight groups in configuration. The Shapley module stays generic over N players: exact over 2^N coalitions when each is a policy simulation (N = 10 → 1,024), otherwise antithetic sampling with P ≥ 32.
2. **Real Assets engine.** Port `ra_module.RAState`: true, reported (RAME) and nowcast values; asset-level debt with availability, extension and cures under declared ϖ; the fund-level waterfall; the open-end queue; oil and GCC links; a dedicated SeedSequence child for CRN.
3. **Stress module.** Make s\*(θ) carry the RA θ components and recalibrate θ\* with the RA leg inside both the Monte Carlo replica and the ladder. Acceptance test: at θ = 0.76 the RA leg reproduces G15's row in reproduction mode (V-RA-CF).
4. **Attribution module.** DVA_RA on V\*, with β̂^d from the FBE/RAME, re-levered on the debt path. Store reported-NAV DVA for disclosure only, and test that pay ledgers never read it.
5. **Pricing.** FTP_RA, hurdle and B_RA from the Phase-II restored problem with `priced_on`. CLC_RA uses CVaR95 of joint-path cures (gate V-RA-CLC).
6. **Gates and tests.** V-RA-CTRL (`ra_gap_01_calcs/test_v_ra_ctrl.py` as the template); V-RA-θ; V-RA-CLC; a v1-mode reproduction test of the integrated engine.
7. **Shadow IC roster.** 13 seats with the Real Assets head, its evidence slices and its standing question (RA §12).

## 5. Questions for the user

1. **Real Assets size.** $18bn is still a working figure (context §1A). The objective is flat over 6–14% of NAV, so the size is a governance choice.
2. **PE unfunded at $34bn.** $16.4bn gives U/NAV 0.48 on the smaller bucket, close to the v1.0 history that failed V6; $10.9bn is the internally consistent figure. θ\*, the facility need and L8 differ materially between them.
3. **Extension policy and ϖ.** Will ADIC's lenders extend in stress (P(extension) 0 vs 0.35 moves the RA T4′ row by $0.55bn), and will ADIC ever hand back keys?
4. **Revolver timing.** FTP_RA is 2bp once the revolver signs and 21bp before, plus CLC for cures. Which state should price the next quarter's RA envelopes?
5. **Open-end terms.** Revocability and pro-rata rules decide whether "notices at Amber" redeem $3–4bn over five years, as modelled.
6. **ENR.** Can ADIC obtain live secondary bids and the GP price decks for its fund-held upstream positions? The SELL pays only if the bid is at least the strip-based economic value θ̂, which RAME cannot estimate without the decks. Does the owner want any oil exposure held deliberately?
