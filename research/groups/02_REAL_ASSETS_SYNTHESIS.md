# ADIC Real Assets Group Synthesis

## How Real Assets, the eighth investment group, plugs into the total-portfolio, multi-period decision framework

**Date:** 2026-10-19 (v1.1: 2026-10-18) · **Version:** 1.2 (revises v1.1, which revised v1.0) · **Companion to:** the main report `research/00_SYNTHESIS.md` (v1.1) and the groups report `research/groups/01_GROUPS_SYNTHESIS.md` (v1.1), both carrying the ra_gap_01 eight-group patches; the integration memo `research/groups/03_REAL_ASSETS_INTEGRATION.md`; addenda `research/groups/addenda/ra_gap_01.md` to `ra_gap_04.md` · **Audience:** CIO, Investment Committee (IC), Real Assets head, Corporate Finance (CF), quant and data-science team · **Status:** design-grade synthesis. No ADIC data was used.

> **SYNTHETIC-DATA NOTICE.** Every ADIC balance, position, cash flow, debt figure, queue payout, oil delta and decision example here comes from working allocation v2 (context §1A), the G10–G15 synthetic books or design defaults. None of it is ADIC data or may be presented as such. Tables with [I-calc] figures end with *SYNTHETIC – NOT ADIC DATA*.

> **Version note (v1.2, 2026-10-19).** This version folds in four addenda and resolves the ten contradictions the critic found. Context §1A was re-read and is unchanged: scope and access are confirmed, and $18bn is still a working size.
> - **ra_gap_01, total-portfolio integration:**
>   - θ\* is 0.835 / 0.877 on the eight-group book.
>   - RA's Tier-1 T4′ drain is −$4.49bn over 24 months, so its relief against PE is negative.
>   - Prices come from the restored problem: FTP_RA, the hurdle, CLC_RA on CVaR95, B_RA and L8.
>   - 8–12% becomes a judgment band, and the binding quantity is a $1.8bn infrastructure-led pacing envelope.
>   - DVA_RA is paid on V\*, and RA is the tenth Shapley player.
>   - The ENR SELL is NOT ESTABLISHED in the sealed run.
> - **ra_gap_02, engine reference and sealed debt tape:**
>   - a financing window f taken from the SLOOS;
>   - a 198-tranche tape;
>   - the structural cash row (T4′ −$1.64bn, or −$0.55bn with structural calls);
>   - cures, LTV, and the gates G-ODCE, G-Jiang and G-Chen.
> - **ra_gap_03, oil inside the canonical generator:**
>   - L_eff is 4.7% of NAV;
>   - a barrel ledger (RA 11.2m bbl, of which ENR 10.4m);
>   - a barrel price, a Tier-1 backstop and a recovery rule replace the 5m / 10m cap;
>   - an exploratory ENR card.
> - **ra_gap_04, estimators brought to the R15 standard:**
>   - RAME under the canonical ensemble;
>   - R2 needs a contemporaneous index;
>   - bids enter only leave-one-out;
>   - FBE-R-RA with one κ_g;
>   - V-RA1 passes on the adjusted basis, and V-RE2 fails;
>   - a sealed closed-end history and external gates.
> - **Fixed in place** (reconciliations RA14–RA24):
>   - The open-end ladder rows now run on the engine of record, so base 12-month SELL capacity is $6.5bn, not $9.0bn.
>   - The oil delta is measured at the canonical state.
>   - The Tier-1 RBL reserve uses a tail quantile, and cure risk is CVaR95.
>   - Self-reproducing gates are retired.
>   - The ground-lease cost is now a lower bound.
>   - [U/I] values are re-tagged.

---

## 0. Scope, inputs and relationship to the other reports

**Scope.** The user added Real Assets (RA) after the seven-group work closed. This report specifies the eighth group in the groups report's format. It changes no engine; the addenda ran copies. Main- and groups-report conventions govern:
- **Canonical stress.** T4′ = s\*(θ\*) is the canonical 24-month stress, and literal T4 a reverse stress. θ\* is 0.76 on the seven-group v1 book. On the eight-group v2 book it is 0.835 with PE unfunded at $16.4bn ("U16") and 0.877 at $10.9bn ("U11") (ra_gap_01).
- **Pricing.** Phase I runs before any price is read, and every card and envelope carries `priced_on`. One kernel, one state-contingent λ, quantity envelopes.
- **Forecasts.** The FBE has a single forward basis and one κ_g per group. The §8.4 segment values are prior means for empirical-Bayes random effects, not separately scored κs.
- **Gates.** The SYN-ADIC-177 gates apply.

The integration memo `research/groups/03_REAL_ASSETS_INTEGRATION.md` now exists; it was written with ra_gap_01. Its APPLIED edits are in place:
- `00_SYNTHESIS.md` and `01_GROUPS_SYNTHESIS.md` carry eight groups, 13 seats, ten Shapley players and gate V-RA-CTRL.
- ra_gap_03 restated the put-spread lines in 00 §4.6 item 9 and 01 §3.7 in spot-equivalent delta.
- The groups report keeps "seven groups" only where it describes its own scope (memo item 6, still PROPOSED).

**Inputs and verification.** Six streams, each with an adversarial log. Only corrected values appear, tagged [C]. Other tags:
- [S] sourced and confirmed; [P] practitioner; [A] client statement or working assumption.
- [I] inference or default; [I-calc] synthetic arithmetic; [I-MC] synthetic Monte Carlo on a side model.
- [U] unverified evidence, never load-bearing on its own.
- [U/I] an [I] default whose only external support is unverified. It is used only with a stated sensitivity and is listed in §5 (in v1.2, the crisis LP prices).

| Stream | Claims: confirmed / corrected / refuted / unverifiable |
|---|---|
| G10 real estate | 32: 26 / 4 / 0 / 2 |
| G11 infrastructure | 35: 32 / 3 / 0 / 0 |
| G12 energy & natural resources (ENR) | 29: 26 / 2 / 0 / 1 |
| G13 marks and valuation | 30: 26 / 2 / 0 / 2 |
| G14 actions and financing | 29: 25 / 3 / 0 / 1 |
| G15 portfolio role | 40: 31 / 5 / 2 / 2 |
| **Total** | **195: 166 / 19 / 2 / 8** |

All six rate HIGH on sourced evidence and MEDIUM on design; every design must-fix is applied where [C] appears, and the RA rows below record the reconciliations. Both refutations concern G15's own analysis, not its sources. §15 corrects the citation errors: the Fisher & Hartzell DOI, the Neuhaus title, and the Elliott & Liao and Blanc-Brude et al. author lists.

**Addenda (v1.2).** Four gap-fills closed the RA critic's gaps. Each keeps its scripts and JSON results beside it in `research/groups/addenda/`:
- ra_gap_01: total-portfolio decisions, prices and attribution (`ra_gap_01_calcs/`);
- ra_gap_02: engine reference spec, sealed debt tape and structural run (`ra_gap_02_calcs/`);
- ra_gap_03: oil wrong-way risk inside the canonical generator (`ra_gap_03_calcs/`);
- ra_gap_04: estimators brought to the R15 standard (`ra_gap_04_calcs/`).

All are SYNTHETIC, on SYN-ADIC-177 under allocation v2.

**New computations** [I-calc].
1. The unmodified G10 engine (scratchpad copy), re-run with the US open-end queue starting at the last observed ≈10% (not 8%) and the stale gap G₀ at 2% (not 5–8%), answering two G10 must-fixes; tables quote this run (10,000 paths, same seed): `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\ra_synth\compare_g10.json`.
2. T4′ reported-mark capture under RAME's segment smoothing, by the G15 verifier's method (all else is arithmetic on verified outputs): `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\ra_synth\scripts\t4_capture_rame.py`.
3. *(v1.2)* The open-end ladder rows on the engine of record (§6.2):
   - A scratch copy of ra_gap_02's engine reproduces its stored q4 payout shares exactly. It was extended to q1 and q8 P5 shares (5,000 paths, seed 20261019): `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\ra_v12\run_queue_ladder.py` → `queue_ladder_results.json`.
   - The totals are restated on G15's per-row values by `restate_ladder.py` → `restated_ladder.json` in the same folder.
4. *(v1.2)* Tail quantiles of G12's RBL cure calls (§9.3). G12's `simulate()` was run unmodified on a scratch copy, which reproduces the stored 73% call probability and 18% conditional mean: `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\ra_v12\g12_cure_tail.py` → `g12_cure_tail_results.json`.
5. *(v1.2)* Ground-lease and sale-leaseback headroom costs (§7.3): the G14 verifier's 10-year figure, scaled by annuity factors at SOFR.

| Item | Status |
|---|---|
| Real estate, infrastructure and ENR (no agriculture or timber); funds, co-investments, JVs and directs; inside the ~60% private allocation; ENR oil exposure wrong-way with the draw | Confirmed (context §1A) |
| Marks archived quarterly as net IRR/MOIC per holding, with cases | Confirmed (design brief §9) |
| $18bn (10.2% of NAV) carved from PE funds ($52bn → $34bn); ≈$4bn unfunded | Working assumption (allocation v2); context §1A re-read on 2026-10-19 confirms no size |
| PE unfunded $16.4bn (census v1.1, user's choice) or ≈$10.9bn at the v2 bucket's U/NAV of 0.32 | Both carried in re-runs ("U16", "U11") |
| Open-end holdings; sector, region, vehicle and control mix; asset-level debt; default policy ϖ | Open (§14); a sealed synthetic debt tape (ra_gap_02) stands in for asset-level debt |

**Reconciliations made here.**

| # | Issue | Decision |
|---|---|---|
| RA1 | Three synthetic books (G15 $18.0bn; G11 infrastructure $7.2bn; G14 $33.5bn GAV) | G15's ten sleeves are the census of record (§11); G11 and G14 per-dollar results carry over |
| RA2 | JV sell-down filed under REFINANCE (brief §8.3; G14) | Any disposal of common equity is a SELL of fraction φ, per the user's definition |
| RA3 | Asset-level actions on holdings ADIC does not control | A vehicle × control matrix gates every card (§7.2) |
| RA4 | Look-through limits that bind on fund debt and break under T4′ | Origination tests on controllable debt; fund debt charged, not constrained; no forced sales (§7.5) |
| RA5 | ϖ = 1 called "economically recourse" yet counted only as P95 cures | ϖ is declared; non-recourse debt stays out of T5 limit 1; cures enter O^stress and the CLC |
| RA6 | Open-end credit at P5 (G10, G14), P50 (G15) or zero (G13) | Zero in T3 and the T4′ hard row, as for private-credit evergreen units (Couts 2025); φ at P5 in P |
| RA7 | Four smoothing parameterisations | G13's two-component appraisal model governs; the others are validation targets. Under it, a third of a T4′ loss reaches reported marks within a year, not G15's two-thirds (§6.3) |
| RA8 | A 5–8% starting gap presented as fact | The nowcast Ĝ replaces it; SYN default 2%, with 0 and 5–8% as sensitivities |
| RA9 | Stress calls ×1.38 (G15) vs a structural slowdown (G10) | Tier 1 keeps T4′; the call multiplier and fund-level refinancing are misspecification axes |
| RA10 | G11's stress figures come from an engine without indexation or resets | Labelled reduced-form; G11's structural durations are the loadings of record (§9.1) |
| RA11 | Oil delta at an unstated price; hedges at notional | Spot-equivalent barrels at the current state; hedges at spot-equivalent delta; one pricing channel. v1.2 measures them at the canonical state, the 15-Oct-2026 strip (RA16) |
| RA12 | RA sales amber (G14) or red (G15) | Red under T4′ and outside Phase I; amber in P only while the financing window f is N or T and S ≠ CRIS. f comes from the SLOOS (ra_gap_02); v1.1's "N or T" was undefined |
| RA13 | Three queue machines (G10, G14, G15) | G10's is the engine of record (§4.6); G14's payout ratios (0.71 a quarter is a full-cycle average) and G15's hand-set paths are cross-checks. v1.2 runs the ladder's open-end rows on it (RA21) |

**Reconciliations added in v1.2** (from the addenda and the critic's ten contradictions):

| # | Issue | Decision |
|---|---|---|
| RA14 | Two RA T4′ drains: −$4.49bn (ra_gap_01's θ-indexed Tier-1 row at θ\*) against −$1.64bn (ra_gap_02's structural engine on the sealed tape; −$0.55bn with structural calls) | The Tier-1 row governs θ\*, survival, B_RA and prices. The structural row is reported beside it. The θ components are re-anchored on the tape before certification (§4.7) |
| RA15 | ENR SELL: NOT ESTABLISHED in the sealed run (ra_gap_01) against "sell now" on the exploratory card (ra_gap_03) | The pre-registered verdict governs. The card is a new hypothesis for a fresh sealed run on the canonical generator (§9.3) |
| RA16 | Oil budget: a 5m / 10m cap justified by protecting the overlay's put spreads, with deltas quoted at a $95 or $70 basis (critic) | Barrel price H_j, Tier-1 backstop and recovery rule; deltas at the canonical state; the put spreads carry only 1.6–3.1m bbl (§9.3) |
| RA17 | One κ_g (§0, groups §5) against eight segment κs (§8.4) (critic) | One κ_g with empirical-Bayes segment effects; the table gives prior means (§8.4) |
| RA18 | Smoothing: G-ODCE's trough lag wants core-RE λ_agg ≈ 0.60, while V-RA1's crash error wants λ + 0.10 in downturns | Engine runs use 0.60 / 0.55 / 0.65 (core / value-add / GCC RE). RAME carries regime-dependent λ (model M1, which it passes). Joint recalibration happens before the gates freeze (§5, §11) |
| RA19 | V-RA-CF and V-RA-OIL reproduce their own prototypes, so they cannot fail (critic) | Retired as validation and kept as regression tests. External gates replace them: G-ODCE, G-Jiang, G-Chen, CF-X1–X6, OIL-X1–X3 (§11) |
| RA20 | CLC_RA on deterministic cures while §10 asks for CVaR95; the Tier-1 RBL reserve at a mean (critic) | CLC_RA on CVaR95 of joint-path cures (ra_gap_01); RBL reserve at the SG / DB CVaR95 (§9.3, §10) |
| RA21 | The ladder used G15's queue machine (2% start) while RA13 names G10's (critic) | Open-end rows restated on the engine of record (§6.2) |
| RA22 | Ground-lease cost "≈0.34 over 10 years, priced as permanent" (critic) | 0.34 is a lower bound. ≈0.47 (15 years) to ≈0.73 (30 years), ≈1.1 if perpetual (§7.3) |
| RA23 | [U] is "never load-bearing", yet [U/I] crisis LP prices set ladder prices and crisis SELL economics (critic) | Re-tagged [U/I] with a sensitivity. They drive only Red rows (≈$0.13bn of T4′ 12-month cash) and crisis cards, which must show the flip bid (§0, §5) |
| RA24 | The integration memo was missing; 00 and 01 said seven groups, 12 seats and nine players (critic) | Memo written; patches applied (§0) |

---

## 1. Executive summary

Real Assets adds a fourth private engine (income assets with an appraisal-smoothed NAV) and an asset-level debt module. For ADIC it is:
- a stress-income floor that slightly hurts drought cash. Under the Tier-1 stress convention it drains more than PE;
- a partial, contract-dependent inflation hedge, carried by indexed infrastructure;
- a leverage and refinancing risk that ADIC mostly does not control;
- through energy and Gulf real estate, an oil and fiscal exposure. It co-moves with ADIC's crises and is wrong-way with the owner's draw.

It is not a liquidity reservoir.

**Twelve findings** (synthetic book: $18bn NAV, $4bn unfunded; all figures SYNTHETIC)

1. **Mix and size.**
   - The synthetic census is 50 / 36 / 14% real estate / infrastructure / ENR.
   - The optimizer's binding output is a pacing envelope of **$1.8bn a year ($1.5–2.1bn), split ≈33 / 67 / 0** (RE / infrastructure / ENR), with the infrastructure cap binding [I-calc].
   - 45 / 45 / 10 stays a pacing direction [I]. Peers are cutting real estate, infrastructure LP interests trade at 91% of NAV against 68%, and the barrel price weighs on ENR (§2.3, §9.3).
   - Size is a judgment call. Across 6–14% of NAV, five-year CE moves by at most ±$1.2bn, with a sign that depends on the model, and no Tier-1 row binds. So 8–12% is a judgment band, and $18bn sits inside it [I-calc].
2. **Cash.**
   - RA distributes ≈6.3% of NAV in the drought against PE's 9–11%, netting −$0.16bn in year 1. The structural engine on the sealed tape gives −$0.14bn, and the canonical base −$0.15bn (P5 −$0.43bn).
   - Relabelling $18bn from PE to RA costs $0.5–0.9bn of drought cash a year.
   - Under the Tier-1 convention at θ\*, the T4′ drain is **−$2.50bn over 12 months and −$4.49bn over 24** (U16; −$4.64bn at U11), not G15's −$2.46bn. The synthesis's own lender-availability and extension terms and the fund-level module add $1.8bn.
   - The same NAV at PE rates drains −$2.69bn to −$3.76bn, so **RA's T4′ relief against PE is negative**.
   - The structural engine on the sealed tape drains −$1.64bn, or −$0.55bn with structural calls. Tier 1 keeps the conservative row until its θ components are re-anchored on the tape (§4.7) [I-calc].
3. **Integration and prices.**
   - With RA's components indexed to θ, θ\* on the eight-group book rises from 0.76 to **0.835** (U16; pooled 0.850) and **0.877** (U11; pooled 0.897).
   - Doing nothing survives 18 / 20 months, which moves readiness from Red to Amber on U16. Lasting 24 months needs $11.6bn / $8.3bn of facilities.
   - Priced on the restored Phase-II problem (there is no structural recovery):
     - RA pays FTP of **2.0bp a year on scheduled flows with the revolver signed and 20.5bp without**;
     - new commitments face a 13 / 144bp hurdle;
     - cures are priced once, in CLC_RA: **$36–38m a year** on a CVaR95 of joint-path cures of $2.37bn;
     - B_RA from the L4 pool row is $4.26bn (revolver plan) / $4.03bn (group-lever plan) over 24 months;
     - L8 is 0.774 with $4.6bn of headroom (U16) (§4.7, §10) [I-calc].
4. **Liquidity.**
   - On one queue machine (the engine of record, starting from today's 10% RE and 5% infrastructure queues, at P5 cash shares), twelve-month SELL capacity is **$6.5 / 4.8 / 1.4 / 4.0bn** (base / drought / T4′ / oil crisis).
   - v1.1's $9.0bn base came from G15's machine, started at a 2% queue.
   - A full redemption of open-end real estate returns 30–37% within a year at P50 (P5 26–34%), and 18% under T4′. For infrastructure the figures are 54–68% and 36%.
   - The machine overstates GFC queues (40% of NAV against 15–21% published), so these are lower bounds. Open-end units still get zero Tier-1 credit (§4.6, §6.2) [I-calc].
5. **Marks.**
   - Appraisals trough ≈3 quarters after true value (5 in a credit crunch). Under RAME's smoothing, reported marks show ≈32% of a T4′ true loss after 12 months ($2.3bn of $7.35bn) and ≈80% after 24 [I-calc].
   - G10's large reported-versus-true wedge came from its assumed 5–8% starting gap. At the 2% the evidence supports, the base case's 3-year reported drawdown is −4.0% against −3.4% true [I-calc].
   - RAME passes the canonical ensemble except under appraisal-contaminated indices, valuers who resist markdowns, strategic marks, and the world where all mechanisms act together.
   - Its transaction index helps only if it is contemporaneous. Until the lag test passes, IC figures use the listed-only grade (index RMSE ≈5.3–6.3%), and bids enter only leave-one-out.
   - Price every action and pay every DVA on the nowcast V\*, and report V^A. A 68% LP bid implies an economic discount of ≈13–32% [C] (§8).
6. **Leverage.**
   - Look-through debt is $17.4bn (49% LTV).
   - On the sealed tape, 12.1% matures within 12 months and 28.0% within 24. For ADIC-controllable debt it is 6.4% / 17.5%, and for closed-end value-add real estate 35% / 54%. G15's uniform 17% a year is therefore wrong in both directions.
   - Under T4′, LTV stays at 45–51% on the actual debt path. With debt fixed it reaches 55% (P95 59.5%), or 58% if rates do not fall. G15's ≈62% is a tail outcome.
   - GPs set the maturities and hedges of the 58% of real-estate debt held in funds. So limits are origination tests on controllable debt, with no forced sales in stress [C].
   - The controllable book already fails three of those tests: the 45% portfolio-LTV target (47.8%), hedged-to-maturity, and the 2% covenant-trigger test (§7.5) [I-calc].
7. **Control.** For fund interests (63% of RA NAV) ADIC can SELL and HOLD, and pledge only through CF. Asset-level REFINANCE, LEVER and HEDGE exist only with control or consent rights [C]; gate V-RA-CTRL enforces this (test 4/4). A JV sell-down is a partial SELL.
8. **Asset-level economics** [C].
   - LEVER fails for core real estate today: levered cash yields of 3.35–5.8% at 60% LTV against debt at ≈6.8–7.1%.
   - Never refinance cheap legacy debt early: lock-in is worth ≈2.3–5.3% of GAV, and the marginal rate on new cash is ≈15.5%.
   - Borrowing at maturity beats selling only for needs shorter than ≈2.4 / 6.7 / 9.2 years (N / T / C); in stress an outright sale beats a JV sell-down.
   - Selling open-end units at a 25% stress bid beats queuing only above ℓ̄ ≈ 17%.
   - As a source of liquidity, asset-level cash-outs are dominated whether or not the revolver is signed (0.157 per $ of headroom on $0.03bn of capacity) [I-calc].
9. **Oil.**
   - On the canonical generator, the owner's draw gives ADIC an effective oil exposure L_eff of **4.7% of NAV** (4.9–5.1% for shocks one to three years out), not 9.3%. The first-year draw delta is ≈22m bbl, not ≈100m.
   - Wrong-way states (glut and demand bust) hold 37% of 2027 and of 2028.
   - RA carries **11.2m bbl** of spot-equivalent delta at the canonical state. Of that, ENR is 10.4m, above the old 10m cap. RA is half of the asset side's 21.2m and rises to 15–17m in glut and bust states.
   - The overlay's 20–40m bbl of put spreads carry only 1.6–3.1m bbl of delta.
   - Replace the 5m / 10m cap with three controls (§9.3) [I-calc]:
     - a barrel price charged as H_j in every group (≈$1.4–3.2 per bbl a year, from oil's co-movement with ADIC's crises);
     - a total-portfolio Tier-1 backstop (≥ ≈170m bbl under Mix B);
     - a recovery rule: no rise in total delta while any Tier-1 gate is violated, as one is today.
10. **ENR SELL.**
    - Selling $0.6–0.8bn of fund-held levered upstream at 0.80 of NAV is **NOT ESTABLISHED** in the sealed confirmatory run. It costs 1.6–2.8bp a year of CE in all six worlds, has no effect on P(red), and breaks even only at bids of 0.95–1.10.
    - An exploratory card on the canonical generator clears at 0.82–0.90 while nothing is signed (p\* 0.76; 0.87 under Mix B).
    - The sealed run used the retired linearised oil chain. So the SELL is contingent on a fresh sealed run with a live bid and a strip-based θ̂. Do not sell at 0.80 (§9.3) [I-calc].
11. **Inflation.**
    - Pass-through is partial and contract-dependent. Per +1pp of expected inflation, regulated equity gains ≈13% and availability PPPs ≈23%, while fixed-escalator renewables, towers and data centres lose 23–27% [I-calc].
    - G11's stress figures lack that indexation and are labelled reduced-form [C].
    - The reference engine has the indexation. It shows infrastructure value ≈0 under T4′ when the 10-year rallies, and −6% to −9% when it does not.
12. **Forecasts and attribution.**
    - Biases are component-level (exit cap, rent growth, capex, schedule, demand, price deck) and stateful.
    - Estimate them with a desmoothed common-shock control, and never score against appraisals.
    - Use one κ_g per group, with segment effects as empirical-Bayes random effects; a segment κ needs 8–40+ annual resolutions. Fuse with 50% shrinkage toward equal weights.
    - The robust engine passes the canonical ensemble except under strategic marks, so the pay remedy is a precondition for RA forecast precision.
    - DVA_RA is paid on V\*. In T4′ year 1, reported NAV would show +$0.6bn against −$3.8bn on V\*.
    - As the tenth Shapley player, RA removes 2.3 / 4.3 / 5.2pp of P(red) and adds $0.26 / 0.50 / 1.09bn of CE (M1 / M4 / M6). It ranks fourth of ten (§8.4–8.5, §12) [I-calc].

**Decisions for the IC this quarter**
1. Ratify the control-gated action matrix (gate V-RA-CTRL) and the partial-SELL classification.
2. Re-ratify T4′ on the eight-group book: θ\* 0.835 at U16 / 0.877 at U11, with RA's θ components as hashed convention fields. Adopt the restored-problem RA prices: FTP_RA on scheduled flows, CLC_RA on CVaR95 of joint-path cures, and B_RA from the L4 pool row.
3. On oil:
   - Replace the 5m / 10m oil cap with the barrel price H_j, the Tier-1 backstop and the recovery rule.
   - Stop new unhedged oil-linked commitments.
   - Do not sell ENR at 0.80. Register a new confirmatory protocol on the canonical generator for the ENR SELL, which is a Tier-A action.
4. Declare the default policy ϖ as a pre-committed contingent plan; large owners do walk away (Brookfield on two Los Angeles towers; Thames Water's owners, ADIA's Infinity among them). Calibrate GP extension, cure and sale behaviour alongside it, because the cure tail sits mostly in GP-controlled funds, beyond ϖ's reach.
5. Adopt origination-test leverage limits and the stress-breach protocol; the tape already fails three of the tests.
6. Give open-end units zero Tier-1 credit, and lodge notices at Amber.
7. Publish the $1.8bn infrastructure-led pacing envelope as the binding quantity. Keep 45 / 45 / 10 as a direction and 8–12% of NAV as a judgment band. Pay RA on DVA at V\*, never on reported NAV.
8. Request the data in §14, starting with debt tapes, control rights, GP behaviour, closed-end commitments by vintage and the ENR price decks.

---

## 2. Mandate interpretation and sub-strategy structure

### 2.1 Mandate and boundaries

- **Mandate [A].** Real estate, infrastructure and ENR, through funds, co-investments, JVs and direct assets, inside the private allocation. Agriculture and timber exist only as disabled taxonomy entries (`RA.AG`, `RA.TIM`); agricultural exposure inside ENR funds defaults to excluded [I].
- **Boundaries** (decisions to confirm, §14):
  - real-estate and infrastructure *debt* goes to Private Credit, preferred equity and NAV financing to Capital Solutions, and purchases of real-asset fund interests to Secondaries;
  - real-asset *co-investments* belong to RA;
  - midstream sits in infrastructure with an `energy_link` flag and counts in the oil delta;
  - listed REITs and infrastructure belong to Public Markets and serve RA only as the market-implied mark;
  - an "infrastructure" label needs ≥ 50% contracted or regulated revenue and leverage ≤ 65%; otherwise the asset is PE, so labels cannot arbitrage envelopes [I].

### 2.2 Sub-strategies

| Strategy | Sub-strategies | Vehicles | Engine (§4) | Mark segment (§8) |
|---|---|---|---|---|
| Real estate | Core open-end; closed-end value-add and opportunistic; JV and direct by sector (logistics, residential, office, retail, data centres, hotels, alternatives); GCC real estate; development; co-investments | OE, CE, JV, DIR, CO | Property layer + debt module; closed-end on RFT-TA v2 | CORE_RE, VA_RE, GCC_RE |
| Infrastructure | Regulated; contracted indexed (PPPs, take-or-pay); contracted fixed (fixed-PPA renewables); toll roads; airports; ports; towers and fibre; data centres; merchant power; greenfield | CE, OE, CO, DIR, JV, CV | Structural archetypes + project or holdco debt; closed-end on RFT-TA v2 | CORE_INFRA, VA_INFRA |
| ENR | Upstream; minerals and royalties; oilfield services; midstream (fee, commodity); metals and streams; gas-linked power; transition assets | CE, CO, DIR, JV | Curve-driven DCF + reserve-based lending (RBL); closed-end with oil-elastic distributions | ENERGY |

### 2.3 Recommended working allocation within Real Assets

| Bucket | SYN census, $bn (% of RA) | Target, 3–5 years [I] | Range [I] | Binding limits [I] |
|---|---|---|---|---|
| Real estate | 9.0 (50%) | 45% (≈$8.1bn) | 40–55% | Open-end ≤ 30% of RA; closed-end value-add ≤ 2% of NAV; GCC ≤ 1.0% of NAV; development ≤ 10% of RE NAV |
| Infrastructure | 6.5 (36%) | 45% (≈$8.1bn) | 35–50% | Data centres + towers ≤ 30% of infrastructure NAV; merchant ≤ 25% of its CFADS |
| ENR | 2.5 (14%) | 10% (≈$1.8bn) | ≤ 15% of RA, ≤ 1.5% of NAV | Barrel price H_j; RA delta held at today's 11.2m bbl while Tier 1 is violated (5.7m after any SELL) (§9.3) |
| **Total** | **18.0** | **10.2% of NAV** | **8–12% of NAV** (judgment band) | Single asset ≤ 1% of NAV; single partner ≤ 20% of RA; optimizer pacing envelope $1.8bn a year, ≈33 / 67 / 0 (§10) |

*SYNTHETIC – NOT ADIC DATA.*

**Rationale.**
- **Size.**
  - Payout-constrained sovereigns hold 4–14% in real estate plus infrastructure (ADIA's ranges), US endowments above $3bn ≈9% in real assets (the peer average fell 2pp in three years), and NBIM ≈2% [S].
  - The integrated re-run (ra_gap_01) moves RA from 6% to 14% of NAV, with PE absorbing the difference. Five-year CE changes by at most ±$1.2bn (≤ 13bp a year), and the sign depends on the model: M2 wants less RA, while M3, M5 and M6 want more. Mix B's P(red) moves by ≤ 0.02pp, and no Tier-1 row binds [I-calc].
  - Under the Tier-1 convention RA buys no T4′ relief, since it drains more than PE (§4.7), while its drought cost scales linearly.
  - So 8–12% is a judgment band, not an optimizer output, and a range above ≈12% is still hard to defend [I].
  - G15's ≈26bp-a-year return cost uses core CMAs that fit neither the book's leverage nor its mix, so it is probably overstated [C].
- **Toward infrastructure.** ADIA's 2025 Review lowered real estate from 5–10% to 2–7% (infrastructure 2–7%), GIC's new 22% Real Assets bucket added infrastructure, and real-estate target allocations fell in 2025 for the first time in 13 years [S]. Infrastructure LP interests trade at 91% against 68%; its operating yield mostly persists in stress (3.3–4.7% of NAV; −23% in a demand bust); its risk-adjusted profit per $ committed is −10¢ against −17¢ (Gupta & Van Nieuwerburgh) [S; I-calc]; and it carries the only partial inflation pass-through, if the tilt favours indexed and regulated segments over fixed-escalator digital and renewables (§9.2). Caveats: closed-end PME is 0.93 against 0.94 for real estate, and forward-return estimates differ by ≈4pp before fee and mix adjustments [S; C]. The optimizer agrees on direction [I-calc]:
  - its year-1 envelope is RE $0.60bn [0.30–0.90], infrastructure $1.20bn (at its cap) and ENR $0.00 [0–0.13];
  - risk charges are 116 / 71 / 33bp per NAV-year;
  - over five years the split barely matters: 45 / 45 / 10 against the census split changes CE by ≤ $0.005bn.
- **ENR at ≈10%.** No new unhedged oil-linked commitments, plus run-off, moves the sleeve toward 10%. The §9.3 SELL would take it to $1.7–1.9bn (9–11% of RA) at once, but it is NOT ESTABLISHED at 0.80 [I-calc]. Private energy returned 3.2% a year over 2013–23 against 15.2% for PE, and its barrels co-move with ADIC's crises [S; I-calc].
- **Vehicles.** Tilt new commitments toward controlled JVs and directs with operating partners: internal real-estate management costs less and nets more (Andonov, Eichholtz & Kok 2015) [S], and only controlled holdings carry REFINANCE, LEVER and HEDGE (§7.2). Keep funds for value-add, ENR and new sectors.
- **Implementation.** Plan pacing of ≈$1.2bn a year, inside an infrastructure-led optimizer envelope of $1.8bn ($1.5–2.1bn). The §9.3 SELL happens only if its triggers fire. Never fire sales.

---

## 3. Holdings and data schema

**Hierarchy.** `holding → group (RA) → strategy (RE / INF / ENR) → sub-strategy (segment)`, with `vehicle` {OE, CE, CO, JV, DIR, CV} and `control` {sole, joint, minority, LP} as orthogonal keys. Every holding inherits the groups-report fields (§3.0): `is_synthetic`, look-through and GP ids, consent/ROFR/pledge flags, bitemporal u/a/f series and an encumbrance flag.

| Field family | Fields |
|---|---|
| Taxonomy | `segment`, `business_model` {regulated, contracted, merchant}, `stage`, `region`, `gcc_flag`, `gulf_volume_flag`, `energy_link`, ownership ω |
| Fund terms | Commitment, unfunded, vintage, call schedule, fees, transfer consent; commitment period, lapse and recycling terms (callable unfunded beside contractual); open-end notice, pro rata or FIFO, caps, revocability, queue position, ADIC share of fund; CV offers |
| JV and direct rights | Board seats, reserved matters, ROFO/ROFR, buy–sell, drag/tag, cash-call and dilution terms |
| Operations | Appraisal (date, valuer {EXT, INT, CARRY}, method, cap or discount rate); WALT, expiries, escalators, occupancy, opex, capex; infrastructure index, lag, caps, reset date, RAB, contract expiry, volume plan; ENR reserves, decline, costs, contracts, GP price deck |
| Debt tape, per tranche | Lender, balance, maturity, amortisation, fixed/floating, spread, cap (strike, expiry, reserve), covenants (LTV, DSCR, debt yield, trap), extensions, prepayment, assumability, opco/holdco, recourse and guarantees; RBL base, advance rate, deck, redetermination date; collateral id and sibling debt (for V^mat), controllable flag, cap expiry. Schema of record: the sealed tape's `ra_gap_02_calcs/ra_tape_tranches_v1.csv` |
| Marks | Underwritten, actual and forecast IRR/MOIC with P10/P50/P90 cases, bitemporal; plan components where archived (NOI growth, exit cap, capex, schedule, demand, hold, deck); `q_bid` with a conflict flag |
| Risk tags | `oil_delta_bbl` (spot-equivalent, at the canonical state and the month-24 SG and DB states), `beta_pi`, `H_j` (barrel price p_bbl·δ_j/V_j, §9.3), `tau_j` (transition charge) |

---

## 4. Return, NAV and cash-flow models

### 4.1 Engine map

Truth engines simulate economic value V^T and cash; RAME (§8) produces what ADIC observes (V^A, marks, bids). Paths are keyed by market, asset and oil state, so RA equity and Private Credit's real-estate loans share one property draw per path (gate V-RE5). By vehicle: closed-end funds in all three sectors run on RFT-TA v2 (§4.2); open-end units on a fund-level property or structural engine plus the queue machine (§4.6); minority co-investments on the asset engine × ω, on the sponsor's exit clock; JVs and directs on the asset engine × ω with the debt module, cures, capex and development (ENR: curve-driven DCF with RBL).

The reference implementation is ra_gap_02's engine (`ra_gap_02_calcs/ra_engine.py`) on the sealed tape. It runs quarterly on the canonical (S, e, Z) plus the financing window f (§9.1). The total-portfolio Monte Carlo carries RA as `ra_module.RAState` on a dedicated random stream, so common random numbers hold everywhere else (ra_gap_01).

### 4.2 Closed-end funds: the PE engine with real-asset parameters

$$C_t=\big(1-e^{-\lambda(a)m^C(e_t)\Delta}\big)U_t,\quad D_t=y^{inc}_sf^{inc}_{s,Z}(t)N_t\Delta+\big(1-e^{-\delta(a^e_t)m^D(e_t)\Delta}\big)NAV^T_t,\quad a^e_{t+1}=a^e_t+\kappa(e_t)\Delta$$

- **Real estate (G10):** calls 25/30/35/40% of unfunded by age; m^C 1.2/1.0/0.75/0.6 and m^D 1.3/1.0/0.45/0.25 (O/N/D/F); exits δ 3/12/22/30/35% by effective age. Income is 80% of positive property cash flow after debt service and fees, so negative leverage cuts distributions. The sealed vintage history needs the canonical drought exit multiplier 6% / 18% = 0.33. G10's 0.45 meets Ares's 7% distribution point only with +29% to +56% a year of commitment growth in 2023–26 (ra_gap_04).
- **Infrastructure (G11):** calls 20/25/30/35%; income Y_k on reported NAV; exits 14/10/4/1.5% a year at 1.06/1.03/0.98/0.90 of economic NAV.
- **ENR (G12):** δ = δ̄(a^e)·exp(κ_D X_t + η_oil ln(F⁽³⁾_t/F̄)), η_oil ≈ 1.2; income ≈4% of NAV in N.
- **Canonical cash-map rates (G15),** income + exits in N / D: real estate 1.0% + 18% / 6%; infrastructure 4% + 8% / 4%; ENR 4% + 10% / 6%. T4′ scales exit-driven distributions by 0.108 and calls by 1.38; S1 uses ×0.318 for 18 months and calls ×1.25 for 12. External gates (ra_gap_04) change two inputs:
  - CF-X3 fails G15's real-estate drought NAV growth (3.0% against MSCI's −0.15% for closed-end RE in 2024–25), so closed-end RE drought appreciation is set to ≈0%.
  - CF-X2 fails infrastructure calls (a 21.7% contribution rate against MSCI's 29% ± 5pp), so infrastructure call rates are under review.
- **Fund-level refinancing module [C, G15 R1].** A sleeve's maturity shortfall S = (D^mat − LTV^max·V^mat)⁺ is met by protective calls up to unfunded, then a distribution stop, then NAV loss.
  - Under T4′ it adds $0.22bn (12 months) and $0.54bn (24 months), mostly in closed-end value-add real estate.
  - In the Tier-1 row at θ 0.76 it adds $0.20bn and $0.38bn (ra_gap_01).
  - On the sealed tape, the fund-level need under T4′ averages $0.37bn over 24 months (CVaR95 $0.71bn). In the base run ≈85% of it sits in closed-end value-add real estate, which needs ≈$0.23bn of protective calls over 24 months even in steady state (ra_gap_02).
- **Lapse, recycling and the seal (ra_gap_04).**
  - Unfunded lapses after age-year 6 (RE, ENR) or 7 (infrastructure). Only 69–71% of the census unfunded is ever called in a drought (74–76% under T4′). Without a lapse model, callable unfunded is overstated by 30–39%. Report callable beside contractual unfunded, and model recycling.
  - The sealed RA closed-end vintage history reproduces the census of record (NAV $6.7bn, unfunded $3.1bn; SHA-256 `5ed8acfd735f0d6b0425f0762ee61805f5b4d0654e44c59f72f0b51a897171a3`).
  - The R15 recovery test recovers pace and callable unfunded within 1–3%. But its 90% intervals cover only 0.76–0.90, so V17 fails on width. Recallable distributions and unannounced call multipliers break the test structurally.

### 4.3 Core, open-end and direct assets: income yield plus appraisal-smoothed NAV

**Real estate (G10).**

$$NOI_t=(R_tO_t-E_t)(1-h_k(Z_t)\mathbb 1_{GCC}),\qquad R_{t+1}=R_t(1+e_k\Delta)+\rho_k[M_{t+1}-R_t(1+e_k\Delta)],\qquad \rho_k=\min(1,\Delta/\text{WALT}_k)$$

$$c_{t+1}=c_t+\kappa_c(c^*_{t+1}-c_t)+\sigma_c\varepsilon,\quad c^*_t=c_0+\beta_y\Delta y^{10}_t+\beta_s\Delta s_t+\Delta\lambda^{liq}(S_t)+\delta_kt+\Delta\phi(Z_t)\mathbb 1_{GCC},\quad V^T_t=\frac{NOI_t(1+\hat g_t)}{c_t}$$

- Market rent M moves with inflation and growth while opex E reprices every quarter, so short-run NOI pass-through is below one. Returns are r^U ≈ NOI/V − capex + NOI growth − Δc/c, levered as r^E = r^U + (D/E)(r^U − r_D).
- Gulf add-ons h_k and φ are differenced against the initial Gulf-war state, which appraisals may reflect [C]. Office cap-rate deviations route through rent growth, not price reversion, because office cap rates do not forecast office returns (Plazzi, Torous & Valkanov 2010) [C].

**Infrastructure (G11, with the verifier's fix).**

$$\mathrm{ECF}_t=\mathbb 1\{\mathrm{DSCR}_t\ge\underline d_k\}(\mathrm{CFADS}_t-\mathrm{DS}_t)^+,\qquad \Delta\ln P_t=\theta_k\pi_{t-L_k}\Delta\ \text{(capped)},\qquad R^{reg}_t=(\omega_t+\delta)\mathrm{RAB}_t+O^{allow}_t$$

- The RAB is CPI-indexed and ω resets every T^reg to r_t + ERP^reg. Floating coupon legs reset on the short rate; fixed legs roll to forward rates at maturity [C].
- Value is structural at decision dates (V^E = V^A − V^D, each on its own curve) and follows the §9.1 loadings in between. Volume jumps arrive on regime entry and decay (airports −55% in a mobility crisis, half-life 3 quarters): distributions see the whole transitory shock, value mostly the permanent part.
- The prototype `g11_infra_mc.py` lacks indexation, resets and segment-specific smoothing, so its outputs are *reduced-form* until refit [C].
- ra_gap_02's engine implements the structural form:
  - revenue follows Δln R = θ_kπ_{t−L_k}/4 + (1 − θ_k)ē_k/4 + g_k/4 + β^g_k g_t/400 + ΔJ + m_kΔx^p;
  - regulated cash flow is ω·RAB, with ω reset every 20 quarters;
  - debt is sculpted, with DSCR lock-ups.

  Under T4′ it gives infrastructure value of −2% to +2% when the 10-year rallies, and −6% to −9% when rates stay flat, against G15's hand-set −12% [I-calc].

**ENR (G12).** The curve is $\ln F_t(k)=\bar x+\phi^k(x_t-\bar x)+\sum_{i\le k}\phi^{k-i}(P_Z^i\mu)_{z_t}$, replaced in production by the ICE strip plus a P-measure premium. Upstream value is $V_t=\sum_kq_{t,k}[F_t(k)\nu(1-\tau)-c]^+D_k+\mathcal O^{PUD}_t+\mathrm{MTM}^{hedge}_t$ with Arps decline; royalties pay s·q·P·(1 − τ), with a drilling response; midstream pays f·max(v, MVC). PV-10 marks are corrected for both the SEC price lag and the flat-price curve-shape bias (spot $126.55 against an ≈$84 2027 strip proxy) [C].

In the reference engine, the C3 curve's mean reversion damps ENR stress. Under T4′ spot falls 42%, but the model strip falls only 23% in year 1 and 4% in year 3; unhedged upstream falls 16% and the sleeve 8–9%. Production therefore moves to the ICE strip. The spot premium χ's half-life must be fitted to the front of the strip: 0.4 months, not Schwartz–Smith's ≈6 (ra_gap_02, ra_gap_03).

### 4.4 Development

Real-estate development draws ≈1/8 of its unfunded a quarter, overruns 15% in crisis and adds units at a 1.25× yield-on-cost (G10); data-centre development capex is 6% of direct data-centre NAV a year (G11). Priors: electricity projects overrun 66.3% on average (Sovacool et al. 2014) [S]; Green Book uplifts run from 4% (duration) and 24% (capex) for standard buildings to 25% and 66% for non-standard civil engineering [S]. Completion and cost-overrun guarantees count as recourse.

### 4.5 Asset-level debt and refinancing

$$L^{max}_{i,t}=a_{i,t}\min\Big\{LTV^{max}_fV^{mat}_{i,t},\ \frac{NOI_{i,t}}{DSCR^{min}_f\,k(r^{new}_t)},\ \frac{NOI_{i,t}}{DY^{min}_f}\Big\},\qquad S_{i,T}=(D_{i,T}+D^{sib}_i-L^{max}_{i,T})^+,\qquad V^{mat}_{i,T}=\omega_iV^*_{i,T}$$

- **Terms keyed to the financing window f ∈ {N, T, C}** (ra_gap_02; §5, §9.1). LTV^max, DSCR^min, DY^min, availability and the spread add-on follow f, not the S regime.
- **V^mat.**
  - V^mat is the economic value of tranche i's own collateral at its (possibly extended) maturity, taken from that collateral's path. D^sib is other debt on the same collateral.
  - Maintenance covenants test appraisal V^A; refinancing tests V^mat.
  - G15's implicit V^mat = (D^mat/LTV₀)(1 + ΔV^sleeve) is the special case where every loan sits at the sleeve LTV. Since E[(D − L^max)⁺] ≥ (E[D] − E[L^max])⁺, that rule understates gaps whenever the mean loan is inside capacity, which is the census case [I-calc].
- **Lender availability.** a draws on one factor per path-quarter, shared with CF's facilities (copula ρ ≈ 0.5) [I]. The two engines read it differently:
  - The reference engine makes a a Bernoulli lender draw, with P(a = 1) = 0.97 / 0.85 / 0.60 (N / T / C) and forbearance for up to two no-lender quarters at +200bp.
  - ra_gap_01's Tier-1 row applies a(θ) = 0.97 − 0.52θ (0.575 at θ 0.76) as a multiplier on every maturing loan's capacity.

  The second reading is harsher, and it explains most of the gap between the two T4′ rows (§4.7).
- **Resolution order** (ra_gap_02):
  1. refinance, if S = 0;
  2. contractual extension, if its tests pass;
  3. discretionary extension, with probability p_ext(f);
  4. forbearance;
  5. cure: always for controlled assets under ϖ = 1, otherwise iff V − D − ℓ̄S > max(0, V(1 − d) − D);
  6. sale;
  7. hand-back.

  Pricing cures at ℓ̄ makes walking away likelier in crises. Over five years the base / T4′ outcomes are: refinance 51 / 49%, contractual extension 8 / 8%, discretionary extension 13 / 15%, cure 20 / 15%, sale 4 / 2.5%, hand-back 0.4 / 2.0%, forbearance 4 / 8% [I-calc].
- **Extension.** P(extension | gap) is a misspecification axis between zero and G10's 0.35 / 0.50 / 0.50 (N / T / C), less 5pp for non-recourse loans and 7pp for debt yields below 8%. G14's 0.55–0.70 is retired: Glancy's "roughly half" is an unconditional large-bank share, and risky and non-recourse loans were *less* likely to be extended after 2022 [C]. The Tier-1 row uses p_ext(θ) = 0.35(1 − θ), which is zero at literal T4.
- **Traps and caps.** A cash trap stops distributions below DSCR 1.10 without any default. Caps expiring before maturity are cliffs: ≈40% of 682 sampled CRE-CLO loans had them [S], and so do 40% of the capped value-add loans on the tape.
- **RBL.** The base is 0.60 × NPV at 0.85 × the curve (the engine uses 0.55–0.65, cut 10pp in SG and DB). It is redetermined semi-annually and on curve jumps ≥ 20%, and deficiencies are cured in 3–6 monthly instalments [S]. Add amortisation, treat the cure as an option, and cap fund-level cures at unfunded [C].
- **Rollover sales (G-Chen).**
  - Near maturity, each 1pp of rate gap cuts the refinance share of transactions by 11.1pp, and rollover sales clear 12–13% below refinance appraisals [C].
  - The capacity mechanism alone gives at most −0.019 per pp, because seasoned loans rarely fail capacity. The effect is therefore behavioural.
  - Sponsor-owned real estate sells with hazard 0.111·(r^new − r^cur)⁺ per pp, damped ×1 / 0.6 / 0.2 by f. That is a calibration, not a validation; Glancy's ≈20% stress-period office payoff is the candidate hold-out [I-calc].
- **Dispersion.** Asset-level σ_id is 8 / 15 / 28% a year by f (office ×1.5), as G-Jiang requires (§9.1). It raises ADIC's T4′ cure CVaR95 from $0.42bn to $0.54bn.

### 4.6 Open-end queue state machine

Per fund, with the standing queue Q as a share of NAV (G10; notation de-collided [C]):

$$R_t=r_0+b(G^{MI}_{t-1})^+,\ \ W_t=wQ_t\mathbb 1\{G^{MI}\le3\%\},\ \ L_t=l_0+d(e^{RE})\tfrac{GAV}{NAV}+c^{in}_t-\tfrac{\text{cures}+\text{shortfalls}}{NAV},\ \ P_t=\min(Q_t+R_t-W_t,L_t),\ \ Q_{t+1}=Q_t+R_t-W_t-P_t$$

- ADIC receives P_t·q^ADIC/(Q_t + R_t − W_t), pro rata, at NAV^A. Defaults [I]: r₀ 0.6% a quarter, b 0.12, w 0.08, l₀ 0.25%, d 1.0 / 0.6 / 0.4 / 0.2% of GAV (O/N/D/F), c^in 1.2%, or 0.4% while the stale premium G^MI > 3% or Q > 5%.
- Variants: retail REITs with 2%-a-month and 5%-a-quarter caps the manager may cut; infrastructure evergreen funds (Stonepeak-Plus terms) at 5% a quarter, pro rata and without carry-over, so ADIC resubmits [S].
- b and w were fitted to the 2024–26 path, so the old gate V-RE2 could not fail. **Out of sample it fails** (ra_gap_04) [I-calc]:
  - Driven by the GFC stale-NAV gap, the queue peaks at 40% of NAV in 2010Q1 (23–45% across sensitivities). The published figures are ≈15% (Callan) and ≈21% of core NAV (Townsend via PREA), so the error is in the conservative direction.
  - The 2023 payout speed passes: 7.6% of the queue a quarter against ≈5%.
  - Matching fund dispersion (Callan's 4Q24 P5–P95 of 4–39%) needs a redemption-sensitivity spread s ≈ 0.3–0.5, which is a calibration.
  - Markdown cancellations lower the GFC peak to 28–32% and improve the 2022–26 fit (RMSE 0.94 → 0.61pp). Raw REIT gaps of 60–80% overstate the premium investors perceived, so requests should read RAME's filtered Ĝ.
  - Outputs are labelled upper bounds on queues, and so lower bounds on payouts. Zero Tier-1 credit stands.

**From the last observed ≈10% queue**, ADIC redeeming all its units at t0 [I-calc]:

| Scenario | Paid by q4 / q8 / q12, P50 (P5) | Queue peak P50 / P95, % of NAV |
|---|---|---|
| base_mc | 32 / 58 / 80% (24 / 41 / 55%) | 9.0 / 22.5 |
| higher_for_longer | 31 / 56 / 76% (26 / 44 / 57%) | 9.1 / 20.9 |
| demand_bust | 24 / 39 / 58% (20 / 33 / 46%) | 16.0 / 25.9 |
| credit_crunch | 22 / 34 / 46% (19 / 29 / 39%) | 27.3 / 40.6 |
| benign | 42 / 86 / 100% (33 / 66 / 88%) | 7.8 / 10.1 |

*SYNTHETIC – NOT ADIC DATA.* Run with q₀ 10% and G₀ 2%. Against G10's 8% start (itself an extrapolation, giving 34 / 62 / 83% in base_mc), the 10% start lowers payouts by up to 5pp; G₀ moves them by ≤ 1pp.

**In the reference engine** (ra_gap_02: the G10 machine on the census, queues of 10% for RE and 5% for infrastructure, 5,000 paths), a full t0 redemption pays [I-calc]:

| Scenario | Open-end RE by q4, P50 (P5) / by q8, P50 | Open-end infrastructure by q4, P50 (P5) / by q8, P50 |
|---|---|---|
| Normal | 37% (34%) / 72% | 68% (67%) / 100% |
| Drought | 30% (27%) / 59% | 54% (54%) / 100% |
| Canonical base | 31% (26%) / 59% | 54% (43%) / 100% |
| Supply glut | 32% (27%) / 62% | 54% (46%) / 100% |
| T4′ | 18% (14%) / 29% | 36% (31%) / 74% |

*SYNTHETIC – NOT ADIC DATA.* Infrastructure evergreen terms (5% a quarter, pro rata), starting from a 5% queue, pay faster than real estate. These shares feed the ladder (§6.2).

### 4.7 The Real Assets row of the cash map

Three rows now exist: G15's (the v1.1 basis), the Tier-1 row at θ\* (ra_gap_01), and the structural engine on the sealed tape (ra_gap_02). Reconciliation RA14 below says which governs.

**G15 engine** (v1.1 basis, now a reproduction-mode regression test). Canonical conventions (groups §2.2), $bn, first 12 months unless stated [I-calc]:

| | Normal: dist / calls / net | Drought | S1 net | T4′: dist / calls + cures / net | T4′, 24 months | Glut / Gulf war: 12 (24) months |
|---|---|---|---|---|---|---|
| Real Assets | 1.73 / 1.33 / **+0.40** | 1.13 / 1.28 / **−0.16** | **−1.14** | 0.58 / 1.78 + 0.13 / **−1.32** | **−2.46** | −0.30 / −0.12 (−0.54 / −0.11) |
| + fund-level shortfall, upper bound [C] | | | | **−1.54** | **−3.00** | |
| Same NAV and unfunded at PE rates | 3.73 / 1.33 / +2.40 | 2.05 / 1.28 / +0.76 | −1.07 | 0.22 / 1.78 / −1.55 | −2.69 | |
| By sector: RE / infrastructure / ENR | | −0.07 / −0.07 / −0.02 | | −0.60 / −0.45 / −0.28 | | Glut: −0.08 / −0.07 / −0.15 |

*SYNTHETIC – NOT ADIC DATA.* At PE's census-v1.1 U/NAV of 0.32 the PE-rate row is +0.30 (drought) and −2.23 / −3.76 (T4′). RA's T4′ drain is −0.84 / −1.70 with calls ×1.0, and −1.65 over 24 months with no new RA commitments; RA's $1.2bn a year comes out of T4′'s canonical $12bn. In v1 mode, ra_gap_01 reproduces this row exactly (V-RA-CF as a regression test).

**Tier-1 row at θ\*** (ra_gap_01). Each RA component is affine in θ and passes through G15's T4′ values at θ₀ = 0.76 (gate V-RA-θ):

$$m_s(\theta)=1-\tfrac{\theta}{0.76}(1-m^{T4'}_s),\quad v_s(\theta)=v^{T4'}_s\tfrac{0.30+0.10\theta}{0.376},\quad L_s(\theta)=L^N_s-\tfrac{\theta}{0.76}(L^N_s-L^S_s),\quad a(\theta)=0.97-0.52\theta,\quad p_{ext}(\theta)=0.35(1-\theta)$$

Calls are (1 + 0.5θ) × 28% and exits 0.45(1 − θ) × drought rates. a(0.76) = 0.575 sits inside v1.1's crisis range (0.50–0.60); the f-keyed value for window C is 0.60 (§5).

| Step ($bn) | 12m | 24m |
|---|---|---|
| G15 published row | −1.32 | −2.46 |
| + θ-indexing and RAME marks (θ 0.76) | −1.30 | −2.49 |
| + fund-level module | −1.50 | −2.87 |
| + lender availability and extension (θ 0.76) | −2.33 | −4.21 |
| **Canonical at θ\*: U16 (0.835) / U11 (0.877)** | **−2.50 / −2.60** | **−4.49 / −4.64** |
| Axes at θ\* U16: extension 0 / 0.35; calls ×1.0; fund shortfall all to cash; no new RA commitments | | −4.57 / −4.02; −3.79; −5.05; −3.62 |

*SYNTHETIC – NOT ADIC DATA.* At θ\* (U16) the 24 months hold income 1.13, exits 0.10, distribution stops −0.32, calls 2.91, protective calls 1.36 and direct cures 1.12. The same NAV at PE rates drains −$2.69bn (U = 4.0) to −$3.76bn (U/NAV 0.32). So under this convention **RA's T4′ relief against PE is negative**, not a range that includes zero.

**Structural engine on the sealed tape** (ra_gap_02; canonical generator plus f, 5,000 paths, 20 quarters; $bn) [I-calc]:

| Run | 12m net (P5) | 24m net (P5, P95) | 24m cure CVaR95: ADIC / + protective calls | 24m fund-level need, mean (CVaR95) |
|---|---|---|---|---|
| Normal | +0.30 (+0.21) | +0.61 (+0.41, +0.82) | 0.24 / 0.48 | 0.31 (0.39) |
| Drought | −0.14 (−0.22) | −0.25 (−0.43, −0.07) | 0.25 / 0.50 | 0.32 (0.41) |
| **Canonical base** | **−0.15 (−0.43)** | **−0.28 (−0.91, +0.35)** | 0.33 / 0.62 | 0.37 (0.53) |
| Rate shock (2022-type) | −0.23 (−0.46) | −0.51 (−0.94, −0.08) | 0.34 / 0.71 | 0.45 (0.60) |
| Gulf war persists | −0.12 (−0.35) | −0.27 (−0.78, +0.31) | 0.30 / 0.62 | 0.38 (0.54) |
| Supply glut | −0.26 (−0.47) | −0.40 (−0.90, +0.15) | 0.30 / 0.61 | 0.38 (0.52) |
| **T4′, calls ×1.38** | **−0.99 (−1.18)** | **−1.64 (−1.97, −1.32)** | **0.54 / 0.70** | 0.37 (0.71) |
| T4′, rates flat | −1.02 | −1.72 (−2.05, −1.39) | 0.56 / 0.73 | 0.42 (0.78) |
| T4′, structural calls | −0.28 | −0.55 (−0.89, −0.22) | 0.54 / 0.71 | 0.37 |

*SYNTHETIC – NOT ADIC DATA.* Under T4′, ADIC's own 24-month cure cash (controlled assets, shortfalls and co-investment participation) averages $0.28bn, with a CVaR95 of $0.54bn, or $0.70bn including protective calls. G15 had $0.36bn direct plus up to $0.54bn at fund level. T4′ axes (net; ADIC CVaR95; + protective calls) [I-calc]:
- no discretionary extension: −1.73; 0.61; 0.85;
- ϖ = 0: −1.58; 0.35; 0.53;
- fund module off: −1.40; 0.54; 0.54;
- co-investment not cured: −1.58; 0.46; 0.63.

The steady-state rows nearly match G15 (+0.30 against +0.40; −0.14 against −0.16). The normal-state gap comes mainly from $0.15bn of protective calls for cash-in refinancing of value-add bridge loans at today's rates, partly offset by calls and development draws $0.08–0.09bn lower.

**Reconciliation [RA14].** Both rows start from the same census and the same T4′ label, but:
- *Availability:* the Tier-1 row multiplies every maturing loan's capacity by a(θ). The reference engine draws a lender per loan, with forbearance and contractual extensions that push cures past month 24; its 60-month ADIC cures reach $0.45bn under T4′. This is the $1.34bn step in the Tier-1 table.
- *Maturities:* the Tier-1 row matures 17% of debt a year with G15's implicit V^mat. The tape matures $2.12bn / $4.89bn within 12 / 24 months (controllable $0.28bn / $0.76bn), against G15's implied $2.96bn / $5.93bn.
- *Values and distributions:* G15's hand-set haircuts (infrastructure −12%, ENR −30%) sit against structural paths (≈0% and −8%). Structural distributions run $0.65bn above G15's over 24 months (income $1.38bn against $1.10bn; window-based exits and sales $0.50bn against $0.13bn). The Tier-1 row stays close to G15 here (income $1.13bn, exits $0.10bn).
- *Calls:* both use ×1.38, which G15 also applied to direct unfunded. Empirical calls cut the structural T4′ drain from −$1.64bn to −$0.55bn.
- *Result:* over 24 months the Tier-1 row carries $2.48bn of direct cures and protective calls, against $0.65bn of ADIC cures plus fund-level need on the tape.

**Decision.**
- Tier 1 keeps the conservative θ-indexed row. It sets θ\*, survival, B_RA and the restored-problem prices, and the IC should read RA as giving no T4′ relief.
- Report the structural row beside it under both call conventions, and keep the fund module on.
- Before the 10,000-path certification run, re-anchor the RA θ components on the tape and the reference engine: Bernoulli availability, tape maturities, structural values. That will lower the RA leg, θ\* and the RA prices, by an amount not yet computed.

**L4 and L8** (ra_gap_01; U16 at θ\*; $bn, 24 / 12 months). B_RA is now the RA row of the restored plan, read from the L4 pool row Σ_g B_g + B_OVL ≤ Pool_h:

| Plan | B_RA | B_PE | Pool₂₄ | Slack₂₄ |
|---|---|---|---|---|
| Do nothing | 4.49 / 2.50 | 14.19 / 7.45 | 18.5 | −9.3 |
| Minimum T4′ plan R1: revolver, SMA $0.23bn, RE LP card | **4.26 / 2.36** | 14.19 / 7.45 | 27.6 | 0.0 |
| Minimum T4′ plan R0: co-investment pause, PC levers, SMA $5.6bn, RA JV $0.39bn, cards | **4.03 / 2.22** | 14.04 / 7.36 | 25.3 | 0.0 |
| Mix A | 3.80 / 2.32 | 10.68 / 6.54 | 33.6 | +14.0 |
| Mix B | 3.95 / 2.38 | 11.44 / 6.82 | 39.9 | +18.5 |

*SYNTHETIC – NOT ADIC DATA.*
- U11 runs from 4.64 / 2.60 (do nothing) to 4.09 / 2.48 (Mix B). The 24-month row binds in both minimum plans. v1.1's B_RA of 2.5–3.0 / 1.3–1.5 was the G15 do-nothing drain.
- **L8** (private NAV plus unfunded over W) is 0.774 at U16 ($4.6bn of headroom) and 0.743 at U11 ($10.1bn), against 0.751 ($8.6bn) for the seven-group v1.1 book. RA uses $22bn of the cap, against $23.8bn for the same NAV held as PE.
- On the T4′ path L8 reaches 1.02 at month 12 and 1.16 at month 24. It is therefore an allocation guard at t0, not a stress constraint.

**Reading.**
- A perpetual income asset returns less cash per NAV dollar than a self-liquidating fund, so RA hurts while exits merely slow.
- Under the conservative Tier-1 convention it also drains more than PE when exits collapse, because maturing asset debt meets thin lender capacity. Structurally, the drain is mostly the call convention.
- Real estate drives most of the T4′ drain and the cure tail, and within it GP-controlled closed-end value-add funds.

---

## 5. Parameters: defaults, sources, dates, confidence

Defaults are [I] unless tagged. Full sector and segment tables are in G10 §6.3, G11 §6.10 and G12 §6.13; where they differ, the values below govern.

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Real-estate cap-rate target | β_y 0.45 (0.30–0.60) on Δ10y; β_s 0.50 on ΔBaa; κ_c 0.15 a quarter; credit-availability premium 0 / 10 / 75bp keyed to f (N / T / C; v1.1 keyed it to S) | G10; Chervachidze et al. 2009 [S]; the 2022–24 check mixed fund and asset levels and does not validate β_y [C] | Medium |
| Appraisal-basis cap rates | Logistics 4.1%, residential 4.3%, office 6.2% (+10bp a year drift), retail 5.4%, data centres 4.8%, hotels 7.5%; Europe +25bp, Gulf +150bp | G10 [I], weighted to NPI's ≈4.7% income yield [S]; office drift per Gupta, Mittal & Van Nieuwerburgh [S] | Medium |
| Drought distributions, % of NAV a year | Closed-end RE 1% + 6% exits; open-end RE 3.25%; open-end infrastructure 5.5%; closed-end infrastructure 4% + 4%; ENR 4% + 6%. Closed-end RE drought appreciation ≈0% (CF-X3); infrastructure call rates under review (CF-X2) | G15; Ares Feb-2026 (7%, global RE funds; closed-end use is [I]); NCREIF; bfinance [S] | Medium |
| Refinancing terms, keyed to f = N / T / C | LTV^max 62.5 / 57.5 / 52.5%; DSCR^min 1.25 / 1.35 / 1.40; debt yield 8.5 / 9.5 / 10.5%; availability 0.97 / 0.85 / 0.60; spread add-on +0 / 75 / 175bp. Infrastructure: +10pp LTV, −0.05 DSCR, no debt-yield test, +0.05 availability, −25bp. ENR: −5pp LTV (a further −10pp in SG or DB), −0.10 DSCR. GCC lending on max(f, floor(Z)), so GW → T (GCC 45% LTV in stress) | G14, G15, ra_gap_02; CBRE Q2-26: LTV 59.6%, DSCR 1.43, spread 204bp [S], stale against October rates | Medium |
| Financing window f | L_{t+1} = c + φL_t + b_rec·1{CRIS} + b_y(Δ4 10y)⁺ + b_s·Δ4 Baa + a_Z + σε on the SLOOS CRE tightening index: φ 0.79, b_rec 7.8, b_y 6.4 and b_s 6.6 per pp, σ 10.1. f = N / T / C below 20 / from 20 to 50 / from 50; N / T / C in 69 / 19 / 12% of 1990–2026 quarters; today N (L₀ −11.3) | FRED DRTSCREL spliced to SUBLPDRCSN, 1991Q1–2026Q3, n = 143 [S]; OLS [I-calc]; a_Z [I] | Medium |
| Debt-tape maturities | 12.1% / 28.0% of debt within 12 / 24 months (RE 21% / 43%; controllable 6.4% / 17.5%; closed-end value-add RE 35% / 54%); open-end RE debt 79% fixed; 40% of capped value-add loans have caps expiring early | Sealed synthetic tape on MBA's 2026 maturity shares by holder, CBRE, CRED iQ, Accordant, project-finance norms and the OCC [S]; seed rule fixed before any run [I-calc] | Medium |
| Appraisal smoothing λ_agg | Engine (G-ODCE): core RE 0.60, value-add RE 0.55, GCC RE 0.65 (G13's 0.75 / 0.70 / 0.80 fail the ODCE trough lag). Core infrastructure 0.85, value-add infrastructure 0.80. ENR 0.50 with **no** deck lag for fund NAVs (OIL-X2). λ_idio 0.30–0.50; lag 1 quarter. +0.10 in downturns (V-RA1), pending a joint recalibration [RA18] | G13; Couts et al. 2024 [S]; ra_gap_02, ra_gap_04. λ ≥ 0.85 for infrastructure assumes true volatility of ≈9.5–11.6% [C] | Medium |
| Infrastructure gearing | By archetype as in §9.1 (merchant 40%); lock-up DSCR 1.15–1.20 | G11; EDHECinfra senior leverage 77–78% [S] | Medium |
| RBL and upstream | Advance 0.60 at a 0.85 deck; LTV ≤ 40% of deck PV; PDP decline 12% a year | G12; OCC 2018 (advance 50–65%) [S] | Medium |
| LP secondary price, % of NAV | RE 68 (crisis 45–50 [U/I]); infrastructure 91; ENR 40–70 in busts [U/I] | Jefferies H1-26 [S]. The [U/I] levels set the T4′ / SG ladder prices (0.475 / 0.55 / 0.60) and the crisis SELL economics (RE LP κ 45%, break-even ℓ\* 9.0%). They drive only Red rows (≈$0.13bn of T4′ 12-month cash, so ±30% moves it by ≈±$0.04bn and moves Tier 1 not at all) and crisis cards, which must show the flip bid [RA23] | High; Low |
| Oil (canonical generator) | L_eff 4.7% of NAV at t0 (4.9–5.1% at 12–36 months); barrel price ≈$1.4–3.2 per bbl a year; H_j 0.1–2.9% of NAV a year by holding (§9.3) | ra_gap_03 [I-calc] on stream 03 priors [I] and the 15-Oct-2026 strip [S] | Medium |

*SYNTHETIC defaults are not ADIC data.*

---

## 6. Liquidity terms and stress behaviour

### 6.1 Ladder conventions

- RA holds no HQLA: zero weight in ADIC-LCR(30d), and every RA lever counts 0 in 30-day rows.
- Open-end units count zero in T3 and the T4′ hard row. In P and the informational rows they count at φ(h, S), the P5 cash share from the engine of record (§4.6). Notices go in at CFP Amber; take the better of redemption and unit secondary, never both [RA6].
- Closed-end LP and asset sales are Red under T4′ and outside Phase I; in P they are Amber only while f ∈ {N, T} and S ≠ CRIS [RA12]. JV sell-downs and cash-outs count only if pre-arranged, in Green or Amber, on controlled holdings [C].
- ADIC sells at most 20% of annual segment volume (2025 LP-led core open-end volume: $2.65bn [S]). Prices are per $ of *reported* NAV.
- "Base" is the normal regime; the oil-crisis column is G15's supply glut (T8's SG case), and G12's OC row (§6.3) is its severe variant.

### 6.2 Ladder rows

| Route | Base: months / price | Drought | T4′ | Oil crisis (SG) | 12-month cash, $bn: base / D / T4′ / SG | Tier |
|---|---|---|---|---|---|---|
| Open-end RE (redemption or secondary) | Queue at NAV, 34% by 12m (P5); secondary 3 / 0.96 | 27% by 12m; secondary 0.94 | 14% by 12m; secondary 4 / 0.82 | 27% by 12m; secondary 0.94 | 0.92 / 0.73 / 0.38 / 0.72 | Notice Amber; secondary Red |
| Open-end infrastructure | Queue at NAV, 67% by 12m (P5); secondary 0.97 | 54%; 0.96 | 31%; 0.86 | 46%; 0.96 | 1.35 / 1.07 / 0.63 / 0.93 | Same |
| Closed-end RE LP sale | 5 / 0.71 | 0.68 | 7 / 0.475 | 0.68 | 0.25 / 0.23 / 0.07 / 0.23 | Red |
| Closed-end infrastructure LP sale | 4 / 0.91 | 0.90 | 7 / 0.72 | 0.90 | 0.92 / 0.86 / 0.24 / 0.86 | Red |
| Closed-end ENR LP sale | 5 / 0.82 | 0.80 | 8 / 0.55 | 8 / 0.60 | 0.23 / 0.21 / 0.05 / 0.06 | Red |
| Global RE JV/direct sale | 6 / 0.95 | 7 / 0.90 | 12 / 0.73 | 7 / 0.90 | 0.81 / 0.44 / 0.02 / 0.44 | Red |
| GCC RE JV/direct sale | 6 / 0.93 | 0.90 | 12 / 0.70 | 12 / 0.75 | 0.56 / 0.31 / 0.01 / 0.01 | Red |
| RE co-investment stake | GP-controlled exit | | | | 0.25 / 0.15 / 0.00 / 0.15 | Red |
| Infrastructure direct sale | 6 / 0.96 | 0.94 | 12 / 0.82 | 0.94 | 0.97 / 0.58 / 0.03 / 0.58 | Red |
| ENR direct sale | 6 / 0.90 | 0.88 | 12 / 0.62 | 12 / 0.65 | 0.29 / 0.27 / 0.01 / 0.01 | Red |
| **SELL total, 3 / 12 / 24 months** | 0.61 / **6.55** / 12.47 | 0.48 / **4.84** / 11.19 | 0.33 / **1.44** / 3.84 | 0.48 / **3.98** / 9.26 | | |
| JV sell-down (partial SELL), controlled only | $1.1–2.2bn at 0.95 | 0.92 | 20% at 0.80 | GCC and ENR impaired | | Amber, pre-arranged |
| Cash-out at maturity, controlled only | $0.53–0.90bn | Same | $0 (cures instead) | ≤ $0.53bn | | Green/Amber |

*SYNTHETIC – NOT ADIC DATA.* G15 §6.5 with its omitted co-investment row restored and the control gate applied: ≈$0.30bn of G15's $2.51bn JV capacity sat on GP-controlled co-investments and up to ≈$1.1bn on mixed sleeves, as did ≈$0.37bn of its $0.90bn cash-out capacity [C].

- **Open-end rows in v1.2** [RA13, RA21]. They are restated on the engine of record, using P5 cash shares at q1 / q4 / q8 from the reference engine (§4.6; new computation 3).
- **v1.1's rows** used G15's machine. In the normal state it starts from a 2% queue and paid all $2.7bn of open-end real estate and all $2.0bn of infrastructure within a year. Its totals were 1.59 / 9.02 / 13.46 (base), 0.34 / 4.31 / 10.07 (drought), 0.13 / 0.92 / 3.21 (T4′) and 0.34 / 3.60 / 8.50 (SG).
- **Why drought and stress capacity rises.** Infrastructure evergreen funds pay faster than v1.1 assumed.
- **Reading the T4′ column.** Open-end units still count zero in the T4′ hard row, so the column is informational. V-RE2 makes all queue payouts lower bounds.
- **Crisis prices.** Crisis LP prices (0.475, 0.55, 0.60) are [U/I] defaults (§5).

**Availability by regime** (G14) [I]. Lender and buyer availability roughly halves in a credit crisis, and lags lengthen ×1.5. In the Gulf-war state Gulf-located assets sell at 0.3–0.5 availability and ≈33% lower values, while energy sales improve; in oil-down states energy availability falls to 0.3–0.5 (2015 energy LP bids: 61–76% of NAV [S-sec]). G14's oil-down RBL capacity (≈0.4 of the prior base) is harsher than the 2020 survey's expected 20–30% cuts: a tail beyond the evidence [C]. With the 5-year Treasury ≈80bp above the Q2 lending anchors, "today" sits nearer T than N for rates [C]. The SLOOS-based window reads credit differently: f₀ = N (index −11.3), but the real-estate transaction window starts in D because the 10-year is above 4.75% (ra_gap_02).

### 6.3 Stress behaviour

- **T4′ (G15).** Income ×0.85 / 0.92 / 0.60 (RE / infrastructure / ENR); true value −25% / −12% / −30% (GCC RE −30%) over 12 months; LTV^max 50 / 55 / 45%. True RA equity falls ≈$7.35bn (41% of NAV). Reported marks show ≈$2.3bn (32%) of it after 12 months under RAME's λ_agg with its 1-quarter lag (2 for the ENR deck), and ≈80% after 8 quarters; G15's own φ without a lag would show ≈$4.9bn (67%) [I-calc; C]; ra_gap_01 reproduces $2.32bn (31.6%). With debt fixed, G15's haircuts take look-through LTV from 49% to ≈62%.
- **T4′ at θ\* on the v2 book** (ra_gap_01; U16, 0.835). Equity −38.3%, PE-type distributions at 7.4% of drought, calls ×1.42 and 23 crisis months. For RE / GCC RE / infrastructure / ENR: income ×0.84 / 0.78 / 0.91 / 0.56; true value −25.5 / −30.6 / −12.2 / −30.6%; LTV^max 49 / 44 / 54 / 44%. Lender availability is 0.54.
- **T4′ in the reference engine** (ra_gap_02) [I-calc].
  - Values at q4 / q8:
    - RE funds −18% to −20% / −27% to −29%;
    - global JV and direct −10% / −13%;
    - GCC −30% / −5% (the scenario forces Z to DB, then N);
    - infrastructure −2% to +2% (−6% to −9% with rates flat);
    - ENR closed-end −9% / −8%.
  - GAV falls 9.6% (P5 −14.4%), against G15's −20.7%.
  - On the actual debt path, look-through LTV stays at 45–51% (peak P95 52–54%), because debt amortises, is swept and is cured down.
  - With debt fixed, LTV is 55% at q4 and q8 (P95 58% / 59.5%), and 57% / 58% if rates do not fall (P95 60% / 63%).
  - G15's ≈62% is therefore a tail outcome. Pair T4′ with a rates-flat variant.
- **Credit crunch (G10, GFC-type).** Real-estate true drawdown −39% over 3 years (P50); refinancing gap $0.81bn, 23% of 24-month maturities; peak true LTV 62% (P95 64%); queues as in §4.6 [I-calc].
- **Oil glut, stochastic (G15).** GCC RE income ×0.95 then 0.85, value −10% then −15%; ENR income ×0.68, exits ×0.3, value −20%. RA loses ≈$1.0bn of true value (5.6% of NAV) and $0.7bn of 12-month ladder capacity against the drought. In the reference engine a supply glut nets −$0.26bn over 12 months and −$0.40bn over 24.
- **Oil crisis, deterministic (G12's OC row).** Brent −45% from the curve over six months, then $40–50 for 18 more; equities −5% to +5%; exits in drought; draws at the 10% cap for two fiscal years. Marks: unlevered upstream −35%, levered equity −65%, royalties −30%, midstream −10%, oilfield services −50%, base metals −40%. Borrowing bases −38%, then −20% on ≈41% of borrowers (survey expectations, not realised cuts) [C]; fund calls unchanged; secondary bids 40–60% [U/I]; overlay oil hedges pay.
- **Gulf war (today).** GCC RE income ×0.90, exits ×0.5. Dubai's Q3-2026 home sales fell 47% by value while prices fell only 5–15% from end-2025, so time-to-cash suffers before price [S]. ENR income rises ×1.25 and energy LP pricing rose 9.2% in H1-2026 [S]: a transient hedge. On the canonical generator the war's median exit is March 2027. It holds 25–29% of 2027, and 71% of exits go into a glut (§9.3).

---

## 7. SELL / HOLD / REFINANCE / LEVER

### 7.1 Definitions

Per the user: SELL disposes of a holding wholly or partly; HOLD keeps it and funds calls, capex and, under the declared ϖ, cures; REFINANCE raises cash keeping all common equity; LEVER borrows to add exposure. A JV sell-down is thus a partial SELL with a retained-control premium [RA2]; a production payment carved from a retained asset is REFINANCE and look-through debt. HEDGE is a fifth lens for ENR and floating-rate debt. Cards are scored by C2's full reduced cost on the one kernel, on common random numbers, at V\*, with `priced_on`. ra_gap_01's integrated v2 re-run is a prototype, so RA cards stay exploratory until the certification run on the re-anchored RA leg (§4.7), and Tier-A RA actions need a confirmatory sealed run (main §6.4).

### 7.2 Admissibility by vehicle and control [C]

| Action | Fund interest (LP) | Co-investment (minority) | JV, joint control | Direct or JV, sole control |
|---|---|---|---|---|
| SELL | LP secondary (GP consent; buyer assumes unfunded); open-end redemption or unit sale; CV election when offered | Stake sale, sponsor consent | Stake sale or sell-down via ROFO/ROFR or buy–sell | Asset, portfolio or partial sale |
| HOLD | Fund calls; no call default | Optional pro-rata cure, else dilution | Joint cure decision | Cure or hand-back under ϖ |
| REFINANCE | LP-level NAV facility only (CF-owned, dominated) | None | Asset-level, with consent | Full menu |
| LEVER | None; influence via manager selection, LPA caps, side letters, LPAC votes | None | With consent | Full menu |
| HEDGE | Overlay only (margined; CF collateral) | Overlay only | Asset-level, with consent | Asset-level first, Overlay residual |

Gate V23 rejects any RA card outside its cell. Gate V-RA-CTRL extends it to these cells (`ra_gap_01_calcs/test_v_ra_ctrl.py`, 4/4 pass): no REFINANCE, LEVER or HEDGE card on LP or minority holdings, and JV sell-downs and cash-outs only on the controlled share. Fund interests are 63% of the census's RA NAV.

### 7.3 Instrument economics in liquidity-price units

κ is the one-off value cost per $ raised; ŝ the all-in REFINANCE spread; headroom cost is PV per $ of month-24 T4′ headroom (groups §2.3), at G14's normal-regime prices [I-calc, corrected].

| Instrument | Economics, N → C | Headroom cost | Time; availability N / T / C | Tier |
|---|---|---|---|---|
| Core direct sale | Discount 2 / 8 / 15–20%; κ 3.3% (US), 6.9% (NYC), 8.8% (KSA), 14–18% in C | ≈0.04 | 4.5 / 7 / 10+ months (UK median 135 days [S]); 0.85 / 0.70 / 0.50 | Red under T4′; amber in P in N/T |
| Infrastructure LP sale | κ 5% (N), 15% (C) | ≈0.065 | 3–6 months; 0.75 / 0.6 / 0.45 | Same |
| RE LP sale | κ 31% (N), 45% (C) | ≈0.37 | 3–6 months | Red |
| JV sell-down | κ 7.7 / 26.7 / 58.5% with the asset discount levered onto equity [C] | ≈0.10–0.12 (rescaled); 0.124 at θ\* on the v2 book | 4–8 months | Amber, pre-arranged |
| Cash-out at maturity | ŝ 3.2 / 4.4 / 7.2% | ≈0.07–0.08; 0.157 at θ\* on the v2 book, on $0.03bn of t0 capacity | 2–6 months; 0.97 / 0.85 / 0.60 (keyed to f) | Amber at maturity |
| Early cash-out | Lock-in Λ ≈2.3–5.3% of GAV; marginal rate ≈15.5% [C] | ≥ 0.32 | — | Inadmissible while Λ > 0.5% of GAV |
| Junior capital on cheap senior | 13–16% [P]; keeps Λ | — | 6–12 weeks | Amber |
| Ground lease; sale-leaseback | g ≈ 0.35 of value at a 7.4% economic yield; leaseback cap 6.6–7.3%; ŝ ≈3.5–4.7% for ever | ≥ 0.34, the G14 verifier's 10-year lower bound [C]. ≈0.47 for a 15-year leaseback and ≈0.73 for a 30-year ground lease; ≈1.1 if perpetual [I-calc, RA22] | 3–6 months | Amber; near-irreversible |

*SYNTHETIC – NOT ADIC DATA.* Comparators on the seven-group v1 duals (v2 values below): revolver 0.011, SMA loan sales 0.054, PE pacing cut 0.219, and CF's LP NAV facility ≈0.070 (RE S+450–650bp at 5–15% LTV; infrastructure S+300–450bp at 10–25%), which is not a primary lever. In a crisis every RA lever costs 0.15–0.55 and availability roughly halves. REFINANCE and LEVER hurdles add the ≈1.1pp stressed-lending tightening premium (brief §7.2). ŝ is quoted over SOFR on Q2-2026 terms, so it includes the 5-year term spread; on October rates it is ≈0.3pp higher [C].

- **Ground lease and leaseback.** Their headroom costs scale the verifier's ŝ·A(SOFR, T)/κ₂₄ at ŝ 3.5% and SOFR 3.89%; at ŝ 4.7% they are a third higher.
- **Lever costs on the eight-group book** (ra_gap_01; θ\*, U16). The restored problem prices levers per $ of month-24 headroom:

  | Lever | Cost |
  |---|---|
  | Revolver | 0.011 |
  | SMA run-off / sale | 0.048 / 0.054 |
  | Band | 0.072 |
  | Private Credit pacing | 0.091 |
  | Co-investment pause | 0.123 |
  | RA JV sell-down | 0.124 |
  | RA pacing stop | 0.150 |
  | RA cash-out at maturity | 0.157, on $0.03bn of capacity |
  | PE pacing | 0.213 |
  | Treasury top-up | 0.244 |

### 7.4 Decision rules

- **SELL** iff p^ce ≥ p\*, the reservation price on V\* with lock-in, transfer taxes, re-entry costs and the control premium.
  - *Fund interest at 68%* [C]: at θ = 0.85, a 4% forward return and ℓ = 5%, HOLD is worth 69.4%, so SELL loses ≈1.4pp; break-even needs θ < ≈0.83 or ℓ > 5%. Shedding unfunded calls (U/NAV 0.46 in the closed-end RE book) favours selling young funds in a drought. Once the buyer assumes the unfunded, the restored problem's value-add LP card sells at a 0.68 bid in both funding states: reservation 0.666 with the revolver and 0.574 without, against a HOLD value of 0.70 (ra_gap_01) [I-calc].
  - At a 68% bid the economic discount lies between ≈13% (an assumption-driven lower bound) and 32%: 20% at θ = 0.85, 24% at 0.90.
  - θ̂ comes from the appraisal, listed and transaction nowcast, and bids enter only leave-one-out [C].
  - Using the bid being priced biases θ̂ by −2.3 to −5.3pp in a drought, because the wider buyer premium reads as value. It also lifts ENR drought SELLs from 0.7% to 5.6%. Leave-one-out removes the bias, and bids then add almost no information.
  - A bad transaction index does more damage: under the worst τ, drought SELLs run at 4–14× the true rate (ra_gap_04) [I-calc].
  - For holdings under a SELL flag or card, valuation governance is RAME's G-E: external valuation, no carry-forward or internal marks, and a capped appraisal weight.
  - *Infrastructure* (5-year hold, 5% yield, 0.91 bid): HOLD ties SELL at forward returns of 3.7% (ℓ = 0), 7.6% (ℓ = 4%) and 9.7% (9/9/4/4/4 path) [I-calc, reproduced by the verifier]; stale NAV moves the true boundary toward SELL in a downturn [C]. Break-even ℓ\*: core direct sale 1.0% (N) / 3.6% (C); infrastructure LP 1.4% / 3.5%; RE LP 6.4% / 9.0%.
- **Open-end.** The queue's value cost at ℓ = 10% is 3.6 / 10.3 / 16.2% (N / T / C), and 28.0% at ℓ = 20% in C, so a ≈25% stress bid beats the queue only above ℓ̄ ≈ 17% [C]. Timing stale NAVs against co-investors is an IC policy choice, with relationship costs, not a default [C].
- **REFINANCE** iff ŝ + f/T + λ_Lev + covenant charge + h/T < ℓ̄ over the need, at maturity only unless Λ ≈ 0. Borrow rather than sell only for needs shorter than T\* ≈ 2.4 / 6.7 / 9.2 years (maturity cash-out) or ≈0.7 years in N (junior capital); a need arising before maturity gets junior capital, a sell-down or a sale [C].
- **LEVER** iff ADD and REFINANCE both pass, (1 − κ)c > i at P95 rates, and covenants hold at T4′ values.
  - Core real estate fails: cap rates of 5.6–6.4% against debt at ≈6.8–7.1% give levered cash yields of 3.35–5.8% at 60% LTV, before capex [C].
  - Contracted infrastructure passes modestly at S+200bp (α\* ≈ +0.4% after charges); at α\* ≈ 2.6% financing must cost ≲ S+150bp, i.e. investment-grade opco debt [C].
  - ENR: only with ≥ 70% of 3-year output hedged, RBL LTV ≤ 40% of deck PV and a cleared barrel-price hurdle H_j (§9.3); never in a glut or demand bust.

### 7.5 Non-recourse debt and look-through leverage [C]

- **Three measures.** (1) *T5 limit 1, recourse:* CF debt plus guarantees (completion at maximum exposure, payment at face, carve-outs at 10–25% [I]); non-recourse asset debt stays out, whatever ϖ. (2) *T5-RA, look-through at ADIC share:* reported for the whole book ($17.4bn, 49%), limited only on controllable debt. (3) *Economic exposure:* X = [ϖ + (1 − ϖ)N(d₁)]V, with N(d₁) 1.00 / 0.95 / 0.70 / 0.53 at LTV 0.40 / 0.70 / 1.00 / 1.15 [I-calc].
- **Controllable-debt tests at origination and refinancing, on V\*** [I]: single asset ≤ 65% (≤ 70% for contracted or regulated infrastructure; RBL ≤ 40% of deck PV); portfolio ≤ 45% target, 55% hard; ≤ 25% maturing in any 12 months and ≤ 40% in 24; unhedged floating ≤ 25%, hedged to maturity; development LTC ≤ 60%; P(covenant trigger within 12 months) ≤ 2% per loan.
- **The tests on the sealed tape** (ra_gap_02; controllable debt $4.34bn on $9.08bn of GAV, 22 tranches) [I-calc]:

  | Test | Result |
  |---|---|
  | Portfolio LTV | 47.8%: **fails** the 45% target; passes the 55% hard limit |
  | Maturities within 12 / 24 months | 6.4% / 17.5%: pass |
  | Unhedged floating | 17.3%: passes |
  | Hedged to maturity | **Fails**: 29.6% unhedged once caps that expire early count |
  | Single-asset LTV; development LTC | No breach; 55%: pass |
  | P(covenant trigger) ≤ 2% per loan | **Fails for 4 of 22 loans** (maximum 10.8%: three GCC bank loans and an airport holdco lock-up); 10 loans under T4′ (maximum 56%) |

  They stay origination and monitoring tests under RA4's no-forced-sale protocol. T5 limit-1 recourse inputs on the tape: completion guarantees $0.51bn at maximum exposure, GCC corporate guarantees $0.53bn, carve-outs $0.02bn.
- **Fund look-through** is charged through λ_Lev and desmoothed CVaR and enforced at commitment (manager selection, LPA caps); it never forces a sale.
- **Stress-breach protocol.** A breach triggers the cure-or-hand-back decision under ϖ, never a forced SELL, and true LTV is reported. Under T4′, hard limits would make the optimiser infeasible or sell at 0.475–0.86 of NAV.
- **ϖ is declared, not estimated.** The liquidity base case pays every cure (ϖ = 1), the policy variant none (ϖ = 0); cures enter O^stress and the CLC. Precedents: Brookfield defaulted on two Los Angeles office towers in 2023 ($784m), and Thames Water's shareholders, ADIA's Infinity among them, declined a conditional £500m tranche in March 2024 [C]. The cure tail sits mostly in GP-controlled closed-end value-add funds, beyond ϖ's reach. In the reference engine, ϖ = 0 cuts ADIC's T4′ cure CVaR95 from $0.54bn to $0.35bn. Removing discretionary extensions lifts the version with protective calls from $0.70bn to $0.85bn. So GP extension, cure and sale behaviour (2023–25 history) is calibrated alongside ϖ (ra_gap_02) [I-calc].
- **Encumbrance and peers.** Mortgages pledge ring-fenced SPV assets, so the 15% / 20% encumbrance limit applies to ADIC-level pledges only. NBIM caps unlisted real-estate debt at 25% of the portfolio and 70% per investment [S]; the census sits far above 25% because uncontrolled value-add funds run at 60% LTV, a gap the IC should see.

---

## 8. The four marks, desmoothing, bias and credibility

### 8.1 Four marks, four objects

| Mark | Object | Main distortion | Role in the FBE |
|---|---|---|---|
| Underwritten | IC plan at entry: price, yield-on-cost, NOI path, exit cap, capex, IRR/MOIC | Inside-view optimism; vintage price deck (ENR) | Belief: debias, translate to the remaining-plan return on V\*; expires at T^u + 1 |
| Current | Appraisal NAV, external about yearly | Smoothing, lag, calendar noise, regime asymmetry | Measurement in the state-space model; never a return signal |
| Forecast | Business-plan re-forecast with P10/P50/P90 cases | Anchoring on appraisal cap rates; defend-the-holding | Belief: debias, translate onto V\* |
| Market-implied | Unlevered listed proxies, transaction indices, secondary bids, strips | Sentiment premium; sector mismatch; selection | Timely, noisy price: level anchor and yield-based return |

### 8.2 RAME: observation model and nowcast

$$a_t=s_t+e_t,\quad s_t=\lambda s_{t-1}+(1-\lambda)v_{t-\ell},\quad e_t=0.75e_{t-1}+\xi_t,\quad \ell^U_t-c_L=\beta_Lv_t+p_t+\varepsilon^L_t,\quad \tau_t=v_t+\varepsilon^\tau_t,\quad \ln q_{j,t}=v_{j,t}-a_{j,t}-D_j(y_P-y_V)+\varepsilon^q$$

- Geltner's (1991) partial adjustment with two components, λ_agg on segment news and λ_idio on idiosyncratic news, because fund-by-fund unsmoothing leaves the aggregate smoothed (Couts, Gonçalves & Rossi 2024) [S]. MLE with QMLE errors and a parametric bootstrap; lag by profile likelihood; only appreciation is desmoothed, unlevered, then re-levered on the actual debt path.
- Holding nowcast: appraisal + scaled segment correction + CGR step 2 + a Kalman update on own trades. Equity staleness is levered, θ^eq = (θA − D)/(A − D): a 10% asset overstatement is 13.7–25.0% of equity on the census sleeves.
- Ĝ replaces an assumed G₀: at 2026Q3 the listed-implied gap was ≈+1% and NPI sales cleared within ±4% of marks, while a cap-rate nowcast gives up to ≈8% [C].
- **Recovery on SYN** [I-calc, G13]. λ is recovered within 0.01 with listed and transaction signals; OLS on appraisals is biased down (0.64 / 0.60 / 0.75 against true 0.75 / 0.70 / 0.85). Three-step desmoothing recovers 75–85% of true fund beta (observed: 25–48%). Nowcast RMSE is 8.8–10.8% on raw appraisals, 5.3–7.3% with listed data, 4.4–6.4% with yearly transactions, and 2.5–3.1% with an ideal quarterly index built to the filter's own assumption [C].
- **Canonical ensemble** (ra_gap_04; five segments, 100 worlds of 80 quarters each; the production filter fixed) [I-calc].
  - RAME passes the G-A metrics in 5/5 segments and SBC in 4/5. CORE_RE's plug-in bands cover only 0.725, so λ needs the parametric bootstrap.
  - G-B passes under M1 (λ + 0.10 in downturns), M3 (fat tails), M5 (mild defend-the-holding marks) and M6 (rarer external appraisals).
  - G-B fails under M4 (a transaction index contaminated by appraisals, 0/5), M2 (valuers resisting markdowns, 2/5) and M5s (strategic marks, 2/5). G-C, with all mechanisms together, fails (0/5).
  - Every pre-registered τ axis fails G-B except a drought-only level bias (3/5).
  - G-D: a lagged-τ likelihood test detects lags with power 0.99–1.00 and no false positives. AR smoothing (power ≤ 0.29) and drought-only bias (≤ 0.49) go undetected.
- **R2 and the index lag.**
  - R2 (nowcast RMSE ≤ 50% of appraisal RMSE) passes for a contemporaneous, mildly smoothed or level-biased τ (0.27–0.49). It fails with a one- or two-quarter lag (0.53–0.74), where adding τ is worse than listed-only (0.59–0.69).
  - So τ becomes a state, τ\*_t = ρτ\*_{t−1} + (1 − ρ)v_{t−ℓ}, with an optional appraisal-contamination loading, estimated with the rest.
  - Prefer transaction-based indices and test them for contamination (M4); model direction-dependent smoothing (M2).
  - Until the lag test passes, **interim IC figures use the listed-only grade** (index RMSE ≈5.3–6.3%, where ra_gap_01's 5.5% nowcast error sits).
- **Starting gap.** Ĝ keeps 7–23% of an imposed 2–8% starting gap with τ (mean 16%) and 17–40% without it (mean 30%), whatever the gap's size. Its bands cover 0.57–0.81 at the census date, so t0 bands are widened ≈1.25×.
- **Bids** enter only leave-one-out, with a regime-dependent premium (§7.4). The fourth mark is the listed proxy plus τ; bids serve as a diagnostic and a premium-regime signal.

### 8.3 Translation onto V\*

- ADIC's archived marks are net IRR/MOIC since inception with downside/base/upside cases (brief §9). RAME reads the cases as P10/P50/P90, greys out since-inception IRR as sunk and translates each case onto V\*, so κ measures true error widths against the stated range.
- Underwritten and forecast returns use the economic cap rate: ρ^u ≈ y\* + g^u − (κ^u_exit − κ\*)/H^rem.
- Components are corrected before residual bias: NOI growth halfway to consensus; exit cap ≥ max(plan, entry + 10bp a year, market-implied forward); capex ≥ sector norm; hold +0/2/4/6 quarters (O/N/D/F); refinancing at forwards; E's inflation path through θ_k; volume reference classes (greenfield toll roads mean 0.80, SD 0.30 [I], informed by Bain's 23%-below-forecast average); exit multiples shrunk 50% toward entry; energy re-struck from the GP deck to the strip.
- Valuation view: ρ\* ≈ y\* + ḡ + (κ\* − κ̄)(1 − φ^{4H})/H, office deviations through ḡ. The appraisal-yield view is shown, not fused.
- Closed-end funds: parameter-free incurred Benktander (Neuhaus 2025) on economic TVPI with a prior frozen at inception; paid Bornhuetter–Ferguson fails for exit-driven funds.

### 8.4 Bias and credibility

Components are estimated with a desmoothed common-shock control; without it one cycle cannot identify bias (±6.6–8.3pp per 8 quarters naive, ±1.5–2.6pp controlled) [I-calc]. Anchoring weight on the trailing appraisal: w_a = 0.30.

| Segment | b^u, pp a year (late cycle) | b^f | Residual b^f, components archived | κ prior mean (stated-80% coverage) |
|---|---|---|---|---|
| Core RE | +1.5 (+3.0) | +1.0 | +0.5 | 1.67 (56%) |
| Value-add / opportunistic RE | +4.0 (+5.5) | +2.5 | +2.0 / +2.5 | 2.00 (48%) |
| RE development | +6.0 | +3.5 | +2.5 | 2.22 (44%) |
| GCC RE | +2.0 (+3.5 oil weak) | +1.5 | +1.0 | 2.00 (48%) |
| Core infrastructure | +1.0 (+2.0) | +0.75 | +0.75 | 1.67 (56%) |
| Value-add, digital, transition infrastructure | +3.0 (+4.0) | +2.0 | +2.0 | 2.00 (48%) |
| Greenfield infrastructure | +4.0 | +3.0 | +3.0 | 2.22 (44%) |
| ENR | +3.0 | +2.0; +2 to +4 when oil falls, ≈0 when it rises | Regime-dependent after re-strike | 2.22 (44%) |

All [I]: totals from G13; residuals from G10 and G11, capped at the totals; ENR regime terms from G12. **These are prior means, not parameters to score** [RA17]. The group has one κ_g, with ln κ_g ~ N(ln 1.75, 0.25²), and the segment values enter as empirical-Bayes random effects around it. b^u and b^f likewise become segment random effects around a pooled group shift (ra_gap_04) [I-calc]:
- **Power.** Detecting the table's own κ differences (ratio 1.33 or 1.20) at 80% power needs 8–40+ annual resolutions. Per-segment bias n_eff accrues at only 1.5–3.1 a year (20.5 for the group), so a segment reaches n_eff 20 only after 6–13 years. A per-segment n_eff ≥ 20 rule cannot be met.
- **Estimator.** At eight years, random effects beat raw segment κs at every heterogeneity level (RMSE of ln κ_s 0.064–0.116 against 0.123). They also beat a single κ_g once segments differ (τ ≥ 0.10).
- **Reporting.** A segment κ is shown only once it clears the power line (≈8–12 years for segments with ≥ 16 positions); GCC_RE, RE_DEV and greenfield infrastructure stay pooled. Under one κ_g, 80% coverage is honest in every segment (0.790–0.806).

Credibility is capped beyond ≈8 quarters. At group level, NOI bias reaches n_eff 20 in 1–2 years and exit cap in 3–5; capex and demand rarely do so within a decade. Archives without plan components (IRR/MOIC plus cases only) cost ≈2pp of CRPS (brief §9).

**Scoring.** Never against appraisal returns: an appraisal-mimicking forecaster halves its MSE against appraisals but loses against true and transaction outcomes [I-calc]. Score components against unsmoothed outcomes (NOI, sales, completions, traffic, production) and total return against V\*, with WIS as headline and autocorrelation-robust PIT tests.

### 8.5 Fusion and downstream use

- Precision is 1/(κ_g²σ̂²), shrunk 50% toward equal weights until the group's n_eff ≥ 20. Covariances enter only the predictive variance, and recalibration uses a beta-transformed linear pool (Ranjan & Gneiting 2010). Tier 2 uses posterior means, Tier 1 the posterior P10 with group bias +2 sd.
- **GLS is rejected.** It was allowed only if it beat equal and screened averages out of sample (Elliott & Liao 2026; on 40 pairs it lost 8% in MSE). With an estimated u–f covariance and unknown segment κ it amplifies errors and fails every variant (+16.7% to +57% CRPS) (ra_gap_04).
- **Production engine: FBE-R-RA** [I-calc, ra_gap_04; 2,000 worlds].
  - Design: regime, gap and flag terms pooled across the other seven groups (the regime term relative); RA Huber regression with segment random effects; one κ_g; the fusion above.
  - It passes G-A, G-B in every variant but M5s, and G-C (all mechanisms: +5.7% CRPS, coverage 0.76).
  - FBE-B-RA, §8.4–8.5 as v1.1 wrote them, fails M5, M5s and G-C (+29%, coverage 0.63).
  - Under M5s even FBE-R-RA fails (+19.8% CRPS, SELL bias 1.84pp, regret +42%), and status-quo pay costs ≈9pp of CRPS. So **G-E binds**: RA forecasts get non-trivial precision only after the pay remedy (b ≤ 0.005, s ≥ 50).
  - Within RA alone, the regime, gap and SELL-flag terms are detected with power 0.27 / 0.42 / 0.53, and anchoring with only 0.15–0.24, so w_a keeps its prior.
- REFINANCE capacity uses appraisal LTV and DSCR, the lenders' basis; risk uses D/V\*. Covenants tested on appraisals breach 2–6 quarters after a listed shock, so CF's cure ladder carries a lagged profile.
- Overlay REIT or infrastructure TRS hedges sized on desmoothed betas (0.57 true against 0.22 observed for core RE) post margin at once while NAV moves 2–6 quarters later; CF's collateral pool carries that timing [C].
- Flags F-RA1–F-RA10 follow G13 §6.3 (stale gaps, cap-rate and exit-cap gaps, queues, DSCR, decks).
- **DVA_RA on V\*** (ra_gap_01):

  $$\mathrm{DVA}_{RA,t}=\sum_{i\in RA}\big[V^*_{i,t}-V^*_{i,t-1}+CF_{i,t}\big]-\sum_iV^*_{i,t-1}\big[r_f+\hat\beta^{d}_{i,t}\,(r^{FB}_t-r_f)\big]-\mathrm{FTP}^{vint}_{RA}-\lambda_R\mathrm{RC}_{RA}-\mathrm{CLC}_{RA}+\mathrm{CR}_{RA}$$

  - CF is external cash. Sales and redemptions count at transaction price, and intra-ADIC transfers at fair value on both legs.
  - β̂^d is the three-step desmoothed equity beta, re-levered on the actual debt path.
  - FTP prices scheduled flows and CLC prices cures, each charged once.
  - Pay stays linear (b ≤ 0.005) with multi-year vesting. Reported-NAV DVA is disclosed, never paid.
  - On the T4′ path at θ\*, reported-NAV DVA would pay +$0.64bn in year 1 against −$3.82bn on V\*, then −$4.90bn against −$1.19bn in year 2.
  - In base worlds the reported basis books beta as alpha: the five-year mean gap is +$1.1bn in M1 and −$0.6bn in M6 [I-calc].

---

## 9. Oil, inflation and rate linkages

### 9.1 Scenario-generator loadings by regime

**Regime map** (ra_gap_02). Every RA parameter set keys to the canonical (S, e, Z) plus an explicit **financing window f ∈ {N, T, C}** (§5).
- **Why f is a separate state.** Credit tightens without recessions. Window C covers 1990, 2007Q4–2009Q2, 2020Q2–Q4 and 2022Q4–2023Q4, the last with no recession.
- **Outlook.** Four quarters ahead, f is N / T / C on 66.5 / 28.6 / 4.9% of base paths, against a 14.8% crisis share.
- **Retired:** G11's private 4×4 chain and its macro means, G14's regime base yields and GW / OD term sets, G10's private S chain, and RA12's undefined "N or T".
- **Two generator findings.**
  - C3's annual P^Z_a cannot be embedded quarterly: its principal fourth root has entries as low as −0.16, and the best stochastic root misses by 0.09. ARCHITECTURE §4.1's embedding test therefore fails until P^Z_a is re-estimated monthly.
  - The start-state Baa spread is 1.44%, not 2.0%.

**Real estate.**
- **Keyed to f** (N / T / C): financing terms, the new-loan spread add-on (+0 / 75 / 175bp) and the credit-availability premium (0 / 10 / 75bp). The listed wedge stays on S (0 / −2 / −12 / +3%, EXP / LATE / CRIS / RECV).
- **Transaction window e^RE:** F if f = C; D if f = T, or LATE with the 10-year above 4.75%; O if f = N, EXP and Baa below 1.6%; otherwise N. Today it is D.
- **Gulf hits,** relative to the initial state: in a Gulf war hotels −25%, retail −10%, office −6%, other NOI −4%, cap rates +75bp; in a demand bust 1.5× those plus 5%, and +150bp.
- **G-Jiang** (the negative-equity target) fails as specified [I-calc]:
  - A CMBS replica at 2023Q4 puts 34% of office loans and 8.6% of all loans above 100% LTV, against 44.6% and 14.3%.
  - Fitting three parameters (pre-2022 drift +3.0 / +4.5% a year for non-office / office; repricing dispersion σ 0.40) passes the held-out all-loan > 80% moment (27.0% against 29.0%).
  - Office still fails: 47.5% against 56.0% above 80% LTV, and 28.6% against 44.6% above 100%.
  - The engine understates office negative-equity tails. It needs a sector trend factor and bimodal office dispersion.

**Infrastructure: structural archetype durations** (−Δln V^E per +100bp; negative means a gain) [I-calc, G11]:

| Archetype (gearing) | Cash flows fixed | Permanent real shock | Real shock, 5y half-life | +1pp expected inflation | +1pp asset ERP |
|---|---|---|---|---|---|
| Regulated utility (65%) | 12.9 | 0.8 | 0.7 | −13.2 | 37.9 |
| Availability PPP (80%) | 11.0 | 14.7 | 6.1 | −23.1 | 58.3 |
| Fixed-PPA renewables (75%) | 7.8 | 11.5 | 5.4 | +26.7 | 35.2 |
| Toll road (60%) | 8.5 | 26.6 | 8.0 | +0.4 | 36.1 |
| Airport (55%) | 9.9 | 29.8 | 7.7 | +3.7 | 38.2 |
| Towers / fibre (55%) | 9.6 | 22.8 | 7.3 | +23.3 | 29.3 |
| Data centre (50%) | 9.3 | 24.0 | 8.3 | +23.3 | 27.1 |
| Midstream (50%) | 6.8 | 12.9 | 5.1 | +14.5 | 18.3 |

*SYNTHETIC – NOT ADIC DATA.* Cash-flow-fixed values sit inside EDHECinfra's 7.4–11.6 band [S]. A rate shock is applied once, through discount rates and refinancing coupons; G11's §2.4 add-on double counts [C]. The G11 state now derives from the canonical one: C if S = CRIS; else G if Z ∈ {GW, SS}; else I if LATE; else N.
- Risk-premium means stay 0 / 0.20 / 1.00 / 0.40pp (N / I / C / G), the crisis value an upper bound [C]. Power-price loadings are 0 / +0.15 / −0.30 / +0.35 (SG −0.15).
- Refinancing failure is no longer an input. The share of maturing infrastructure debt left unrefinanced emerges at 2.3 / 1.2 / 8.8 / 2.9% (base, five years), against the retired 0 / 1 / 15 / 3%, and reaches 10.9% in state C under T4′.
- Unrefinanced debt recovers at distressed-sale levels (≈48–50%), not the 77.9% workout figure [C; I-calc].

**ENR** (β_oil to the 1–3-year strip; cash multiplier in glut / bust / Gulf war / supply shock) [I-MC, G12]: unlevered upstream 0.9–1.1, 0.45 / 0.5 / 1.25 / 1.7; 40%-LTV upstream 1.5–1.8, −0.3 / −0.3 / 1.25 / 2.2 (a defend-every-cure bound); royalties 0.75–0.9, 0.63 / 0.69 / 1.17 / 1.5; fee midstream 0.2–0.3, ≈0.95–1.04; oilfield services 1.2–1.5, 0.4 / 0.3 / 1.3 / 1.6; precious-metal streams and transition assets ≈0. Anchors: Norges Bank's relative oil betas to 12-month WTI futures (services 0.61, E&P 0.54, integrated 0.36, pipelines 0.27) [S]. On the canonical strip, averaging the curve impulse over each production year raises these elasticities by ≈25% over G12's year-end points (ra_gap_03).

**Gulf real estate** loads on Z and on oil through fiscal and bank-credit channels. UAE residential prices fell 36.5% (2008–10) and 30.2% (2014–20); 4-quarter changes correlate 0.32–0.36 with Brent at 0–1-quarter lags, none significant (n_eff ≈ 20). The lag is a 0–6-quarter prior centred on 0–2, not G15's 2–6 [C].

- **Fiscal channel.** BIS UAE prices regressed on Brent give a β of 0.12–0.14 (Newey–West s.e. 0.05; 2003Q1–2024Q1); G15's stress implies ≈3× that. So GCC real estate is long oil in SG and DB.
- **War wedge.** Today it is short oil through the war wedge: −6m bbl if the wedge is read as a price delta.
- **Pricing.** It needs H_j, not a cap (§9.3).
- **Lending.** GCC lending terms take max(f, floor(Z)), with floors N / N / T / C / T / T for N / B / SG / DB / SS / GW (C for GW as an axis).

### 9.2 Inflation and rates

- **Pass-through is contract-dependent and partial.** Listed infrastructure hedges no better than equities except firms with pricing power (Rödel & Rothballer 2012); only direct infrastructure is a partial short-run hedge (Wurstbauer & Schäfers 2015); real estate tracks expected, not unexpected, inflation in the long run (Hoesli et al. 2008) [S]. β_π defaults: indexed infrastructure 0.8, long-lease RE 0.4, short-lease RE 0.7, ENR 0 (it loads on oil).
- **What 2023–25 shows.** Private infrastructure funds returned +19.1% real, against −14.2% for MSCI private RE funds and −17.6% for ODCE [I-calc on S]; with inflation at 2.7–3.4%, that measures the rate shock (≈20% of value per unoffset 100bp at a 4.6% cap rate), not hedging. "Inflation hedge" fits legacy indexed infrastructure, not current deal flow, where renewables took ≈2/3 of 2025 sector fundraising [S].
- **Rates.** The 10-year was 5.10% on 15 October (peak close 5.31% on 5 October), ≈68bp above its Q2 average; floating debt resets on SOFR (3.89%); a 3-year 4.5%-strike cap costs ≈1.0–1.3% of notional off the forward curve [C]. Infrastructure's worst value state is supply-shock stagflation: sleeve year-1 P05 −11.8% from today against −6.6% in a demand bust (reduced-form) [RA10]; a deterministic supply shock (real rates +0.6–1.0pp, expected inflation +1.0–1.5pp, ERP +0.2–0.4pp) costs ≈10.6–17.7% before coupon effects, reported separately [C]. Under T4′ the reference engine shows infrastructure value ≈0 when the 10-year rallies and −6% to −9% when it does not, so T4′ is paired with a rates-flat variant (ra_gap_02).
- **No explicit inflation-hedge credit**: infrastructure earns it through supply-shock scenario P&L.

### 9.3 Recommendation: oil-linked real assets and wrong-way risk

**The canonical oil state** (ra_gap_03; main §4.1, §4.7). The re-run uses:
- the monthly shock-type chain coupled to S (P(CRIS | DB) 0.85, P(CRIS | SG) 0.14);
- a Weibull Gulf-war dwell (k 1.3, mean 7.6 months), conditioned on 7.5 months elapsed since 28 Feb 2026;
- oil started from the 15-Oct-2026 NYMEX BZ strip (Dec-26 $105.92, Dec-27 $85.08, Dec-30 $69.16; spot $126.55);
- the owner-draw engine, with the IMF fusion frozen at t0 [S; I].

What it finds:
- **Wrong-way states** (glut SG, demand bust DB) hold **37 / 37 / 29%** of 2027 / 2028 / 2029, against G12's stationary 22.5%.
- **The Gulf war** holds 25–29% of 2027. gap_04's linearised chain gave 49%, because linearisation doubles 12-month war persistence and the mean dwell. The war's median exit is March 2027, matching the IMF's reopening date, and 71% of exits go into a glut.
- **Three defects** surfaced:
  - Stream 03's annual prior is not embeddable at monthly frequency (best-fit error 0.097), so BUILD_SPEC's ≤ 0.01 test fails. Re-elicit a monthly generator.
  - The spot-premium half-life must be fitted to the strip (0.4 months).
  - The IMF fusion must be frozen in bump runs. Re-fitted, it absorbs common oil shocks and roughly halves L_eff.

**Exposure** [C; I-calc].
- The draw is a NAV-scaled vertical put spread on fiscal need: ≈$200m per $1/bbl inside the band (kinks ≈$67 and $23, linear map).
- **L_eff,t = −∂PV(draws)/∂x_t**, by bump-and-revalue at r = 6%, is **4.7% of NAV at t0**. It is 4.9 / 5.0 / 5.1% at 12 / 24 / 36 months, and 3.6–5.9% for breakevens of $45–65.
  - Why it is low: the 2027 rate is set on the 2027 average price, smoothing halves the first response, and the draw sits at its floor on 62–65% of 2027–28 paths.
  - v1.1's formula values (7.5 / 9.3 / 9.9%) and G12's 9.3%/L_eff,t budget scaling are retired; on one engine the scaling factor is ≈1.0.
- The first-year draw delta is ≈22m bbl expected (56m in band), not ≈100m. The draw's PV delta is ≈79m bbl.
- In the wrong-way states, unlevered upstream pays 0.43–0.49× normal cash. 40%-LTV upstream faces over-advances in ≈72% of SG and DB years, averaging 18–20% of equity when called. The tail is P90 32% and CVaR95 41% of levered equity [I-MC, G12 side model; new computation 4].

**Total-portfolio barrel ledger** (spot-equivalent m bbl, positive = long oil; Δ_j = (∂V_j/∂x)/F₁ with F₁ = $105.92; hedges at delta, never notional) [I-calc]:

| Holding | Now | SG / DB, month 12 | SG / DB, month 24 |
|---|---|---|---|
| RA ENR levered upstream ($1.07bn: funds 0.80, direct 0.27) | 8.44 | 8.88 / 8.85 | 9.79 / 9.80 |
| RA ENR royalties, fee midstream, other | 1.97 | 2.44 / 2.38 | 2.88 / 2.85 |
| RA infrastructure midstream (`energy_link`) | 0.78 | 1.02 / 0.99 | 1.23 / 1.21 |
| RA GCC real estate (fiscal channel) | 0.00 | 2.69 / 2.59 | 3.23 / 3.14 |
| **Real Assets** | **11.19** | **15.03 / 14.81** | **17.13 / 17.00** |
| PE, co-investment and Secondaries look-through | 5.36 | 6.58 / 6.39 | 7.57 / 7.41 |
| Capital Solutions, Private Credit, Public Markets, overlay completion beta | 4.64 | 7.19 / 6.95 | 8.59 / 8.37 |
| **Asset side** | **21.19** | **28.80 / 28.15** | **33.29 / 32.78** |
| Overlay opportunistic trend and carry (templates) | +5.5 | short | short |
| Kink put spreads, 20–40m bbl notional, 1-year | −1.6 to −3.1 | −3.4 to −7.6 | −5.0 to −10.5 |
| Owner draw, PV / first year | 79 / 22 | | |

*SYNTHETIC – NOT ADIC DATA.* Elasticities ε to x: levered upstream 0.84, royalties 0.41, fee midstream 0.13, other 0.07; GCC real estate 0 now and 0.18 in SG / DB. Sector weights from MSCI ACWI (energy 3.96%, 30 Sep 2026) and Pantheon International (2%) [S; S-sec].
- **ENR carries 10.4m bbl at the canonical state.** v1.1 had ≈9.2m at a $95 basis (12.2m at $70); averaging the impulse over each production year raises elasticities by ≈25% [RA16].
- **RA is half the asset side** (53%). The rest is PE-family look-through (5.4m), Public Markets plus the completion overlay (4.2m) and credit (0.4m).
- **The opportunistic trend and carry families** are long oil today and short in a glut. That is right-way, but they double the near-term delta, so they belong in the ledger.
- **Barrel deltas grow as oil falls.** NAV falls less than price, leverage rises and the GCC fiscal channel switches on. By month 24 of a glut, RA is up 53% and the asset side 57%.
- **The overlay's put spreads carry little delta** [RA16].
  - At the strip, a 1-year 64/31 spread has an option delta of −0.17 against the $85.08 Dec-27 forward: ≈0.078 bbl per bbl of notional.
  - So 20–40m bbl of notional carries 1.6–3.1m bbl (2-year spreads 1.1–2.3m). That rises to 3.4–7.6m at month 12 and 5.0–10.5m at month 24 of a glut or bust.
  - Premia at OVX-anchored vols ($3.86 a bbl of notional for one year; OVX 49.13) cost $46–59 per bbl of delta a year, 15–40× the barrel price.
  - The spreads are crash protection, judged by enabling value (L5), not a delta hedge. The oil budget does not exist to protect them.

**The barrel price.** Measured on the oil-aware Tier-1 engine with pure-risk bumps (M1–M6, three funding mixes, common random numbers) [I-calc]:

$$p_{bbl}=-\frac{\partial CE}{\partial\Delta}+\frac{\mu}{a_5}\frac{\partial G^*_{99.6}}{\partial\Delta}+c_{red}\frac{\partial P(red)}{\partial\Delta},\qquad H_j=p_{bbl}\,\delta_j/V_j$$

- **Tier 1 does not bind.** Per m bbl, the top-1% G\* paths move $1–10m and P(red) moves ≤ 0.004pp. Under Mix B, P(red) stays below 1% at 227m bbl, ≈8× today's book.
- **Tier 2 sets the price.** For the current ledger it is ≈$1.8–2.1 per bbl a year in M1–M5 ($3.2 in M6), or $1.4–1.7 under Mix B.
  - It comes from oil's co-movement with ADIC's crises, not from the draw: 85% of demand busts are crises, and removing the Z–S coupling cuts it by 80–100%.
  - J counts distributions as wealth, so the draw reaches J only through liquidity. It adds ≈$0.06–0.14 per bbl through the λ-weighted haircut.
- **H_j by holding** (% of NAV a year):
  - levered upstream fund interests 2.4–2.9 (M6 3.4);
  - direct levered upstream 0.8–1.5;
  - royalties 0.8–1.2;
  - fee midstream 0.3–0.4;
  - PE and co-investment energy look-through 0.8–1.1;
  - public energy equity 0.1–0.3;
  - GCC real estate 0.4–0.9 (0.9–1.9).

  The old draw-surplus hurdles (γ 2–4: levered upstream 2.4–4.8%, royalties 0.9–1.9%, fee midstream 0.3–0.6%) survive roughly intact, now justified by crisis co-movement. G12's surplus framing is reported, not charged. GCC real estate gains a charge. Private energy has not earned these hurdles recently (§2.3; 2004–14 energy funds trailed PE by 0.56× net MOIC) [S].

**Budget** (replaces v1.1's 5m soft / 10m hard cap) [RA16]:
1. **Price.** Every oil-linked holding, in every group, pays H_j as its one pricing channel.
2. **Backstop.** Total-portfolio delta must stay ≤ a Tier-1-derived level: ≥ ≈170m bbl under Mix B (slack 0.28pp ÷ 0.0017pp per m bbl in M5; Mix A ≥ 525m). It is checked at the canonical state and at the month-24 SG and DB states, and re-derived on the integrated engine. It is a model-risk guardrail.
3. **Recovery rule.** No rise in total delta while any Tier-1 gate is violated. With nothing signed, T6 is breached in every model (P(red) 4.7–31.6%), and today's ledger adds 0.04–0.10pp. Phase II admits no action that worsens a violated gate.
4. **RA envelope.** Today's 11.2m bbl may not rise while Tier 1 is violated. After any ENR SELL, the envelope is the post-SELL delta: 5.7m bbl at the canonical state (9.0–9.2m in the month-12 SG / DB states, 10.6–10.7m at month 24). It rises only through cards that clear H_j.

**Rule.** Hold oil-linked holding j only if α̂^net_j ≥ H_j + FTP_j + τ_j and the budget holds; new levered upstream also needs ≥ 70% of 3-year output hedged.

**The synthetic sleeve.** $2.5bn: levered upstream $1.07bn ($0.80bn fund-held, $0.27bn direct), royalties $0.18bn, fee midstream $0.85bn, other $0.40bn. At $45 in a glut the sleeve loses $0.68–0.9bn, 0.9–2.4× the put spreads' $0.38–0.76bn payoff [C].

**ENR SELL** ($0.6–0.8bn of the $0.80bn fund-held levered upstream; Tier A; in the LP cell SELL is admissible and hedging is overlay-only) [RA15]:

| | Sealed confirmatory run (ra_gap_01) | Exploratory card (ra_gap_03) |
|---|---|---|
| Engine and setting | Integrated Monte Carlo (gap_04 copy, with t1_engine's linearised oil chain); Mix B, ten players, U16, survival proxy at θ\*; six worlds × 50,000 fresh paths; protocol SHA-256 `d01d542d…3a1eee` | Oil-aware Tier-1 engine on the canonical generator; CRRA(3) CE over the M1–M5 mixture (M6 shown); V\* on the strip; beta rebuilt in futures; proceeds land after the t0 top-up |
| Nothing signed (do-nothing / recovery) | ΔCE −1.8 to −3.2bp a year; ΔP(red) −0.05 to −0.29pp | p\* 0.76 on V\* (0.69–0.83 for α̂ of −2% to +2%); ΔCE +0.9bp at a 0.85 bid; ΔG\* −$0.62–0.65bn; ΔP(red) −0.16 to −0.43pp |
| Mix B signed | ΔCE −1.6 to −2.8bp a year at 0.80 in every world; ΔP(red) 0.00; break-even bid 0.95–1.10 | p\* 0.87; ΔCE −0.1bp at 0.85; break-even |
| Wrong-way benefit | +$0.06–0.14bn on glut / bust paths in M1–M5; −$0.03bn in M6 | +$0.07–0.15bn if a glut arrives in 2028 |
| Barrels removed | 12.2 → 5.8m at $70 | 4.7–6.3m now; 5.5–7.3m at month 24 of SG / DB |
| Verdict | **NOT ESTABLISHED**: CE non-inferiority fails in all six worlds | SELL while nothing is signed (bid 0.82–0.90); robust to α̂ ≤ 2.8%, θ ≥ 0.88 and either war law; LAPV cross-check 0.72–0.83 |

*SYNTHETIC – NOT ADIC DATA.*

- **Where they agree.** Once Mix B is signed, 0.80 does not clear on either engine (exploratory p\* 0.87).
- **Where they differ.** With nothing signed, the sealed run still finds a CE cost.
  - Its engine carries t1_engine's linearised oil-state chain (P^Z_q = I + (P^Z_a − I)/4). That roughly doubles Gulf-war persistence against the canonical generator, and so favours HOLD.
  - It also books proceeds without the card's futures beta rebuild, and requires all six worlds to pass.
  - A pre-registered verdict cannot be overturned by an exploratory re-screen.
- **Decision.** Do not sell at 0.80.
  - Register a new confirmatory protocol on the canonical generator, with fresh seeds, both funding states, the card's deployment rule, RAME's strip-based θ̂ for these funds (it needs the GP price decks) and a live bid.
  - Execute only if the bid is at least both the confirmed p\* and θ̂. If Mix B is signed first, sell only at bids ≥ 0.88 or on evidence that α̂ < 0.
  - Keep proceeds liquid while in recovery.

**Actions** (LP-feasible, restated):
1. No new unhedged oil-price-linked commitments (upstream, oilfield services, oil-weighted royalties) while the draw sits in its band or any Tier-1 gate is violated. New ENR commitments tilt to fee midstream with MVCs, precious-metal streams and transition assets, each paying H_j.
2. ENR SELL only as above.
3. Hedge at asset level only where ADIC controls. The $0.27bn direct position carries ≈2.1m bbl (7.9m bbl per $bn). For funds, hedged leverage is a manager-selection and side-letter criterion.
4. Overlay hedges cover any residual at spot-equivalent delta, with collateral sized on the boom-state tail (P05 −20.3% of hedged value a year) from CF's pool. Asset-level swaps cost little premium but post margin in Gulf-war and boom tails.
5. RBL cures are options, and fund-level cures are GP decisions capped at unfunded. **The Tier-1 reserve uses the SG / DB tail** [RA20]:
   - CVaR95 is 41% of levered equity (P90 32%). On the census that is ≈$0.37bn, with fund-held cures capped at their ≈$0.26bn unfunded (≈$0.34bn at P90).
   - The conditional-on-call mean, $0.19–0.21bn, becomes a floor.
   - The reference engine shows only ≈$0.03bn of ADIC-funded RBL cures under T4′ because its C3 strip mean-reverts. It understates ENR stress until the ICE strip replaces C3.
6. Arrange ENR REFINANCE in normal, boom or Gulf-war states; never count on it in a glut or bust.
7. Cap ENR at 1.5% and GCC real estate at 1.0% of NAV; Gulf-volume-dependent ENR counts double.
8. Transition: a drift on the long-run oil factor; a reserve-life charge of 0.5% a year for oil reserves over 10 years (0.25% for gas); ≤ 30% of ENR NAV with more than half its value beyond 2035.
9. Report Δ_RA at the canonical state and at the month-24 SG and DB states, on a new IC oil-ledger card (barrels by group and state, the liability in barrels, every group's H_j). Re-size automatically when the owner module re-estimates breakeven, slope or mandate mode. Norway is no benchmark: it excluded E&P by label, kept higher-beta services (0.61) and ≈4.6% of equities in other oil and gas [C].

---

## 10. Interactions with other groups and Corporate Finance

| Counterparty | Boundary and link | Control | Liquidity |
|---|---|---|---|
| Private Credit | Senior RE and infrastructure loans; one property draw per path shared with RA equity | Lends to RA assets only with ≥ 50% external syndication or an external quote; one ADIC position in workouts, behind information barriers | Zero; internal debt strips limited liability, so it counts as equity in Δ and leverage |
| Capital Solutions | Preferred equity and NAV financing on RA assets or interests | Reserve price behind ≥ 3 RFQs | Zero unless refinanced externally; gate V2 extends to REFINANCE [C] |
| Secondaries | Buys RE and infrastructure LP interests; forecasts external clearing prices | Never quotes where it may bid; its bids enter RAME flagged and never price themselves | A purchase raises zero |
| Co-investment, PE | Real-asset co-investments belong to RA; portfolio companies' sale-leasebacks are look-through debt; infrastructure label rule (§2.1); shared GPs on one overlap graph (V24) | Recusal from rival envelopes | Transfers raise zero |
| Overlay | SPV caps with the Overlay as execution agent (≥ 3 quotes); a central book hedges the residual at [ϖ + (1 − ϖ)N(d₂)] × floating share, with N(d₂) 0.77 / 0.59 / 0.41 at LTV 0.85 / 1.00 / 1.15 [C]; caps and swaptions rather than payer swaps, which post margin in a demand bust; oil residual and put spreads at spot-equivalent delta (§9.3) | Services transfer pricing; OV1–OV3 | Contingent margin charged at the CLC |
| Corporate Finance | T5-RA reporting, guarantee policy, any NAV facility on RA interests, collateral, FTP, CLC; RA maturities planned with the revolver | Tail cash never ring-fenced for cures | Cures, calls and draws are L4 outflows |

**Envelope** (seven components):
1. a NAV band around the §2.3 target. It is a judgment band; the objective is flat across it.
2. closed-end pacing (η > 0, procyclical like PE; no liquidity credit for two quarters after a cut). This component binds: **$1.8bn a year [1.5–2.1]**, split RE $0.60bn [0.30–0.90], infrastructure $1.20bn (at its cap) and ENR $0.00 [0–0.13]. It comes from the reduced H at θ\* (pooled M1–M5, Mix B, 10 replications). There the liquidity rows are slack, and the risk dual (0.43–0.58) sets risk charges of 116 / 71 / 33bp per NAV-year.
3. 12- and 24-month liquidity budgets (calls, cures, draws), with B_RA from the L4 pool row (§4.7).
4. look-through leverage on controllable debt.
5. the oil delta: the barrel price H_j, the Tier-1 backstop and the recovery rule (§9.3).
6. the open-end share.
7. an inflation-beta floor (infrastructure ≥ 35% of RA).

Envelopes come from the Phase-II restored problem with `priced_on`; increases on binding rows pay the dual.

**Charges** [I-calc; ra_gap_01, `priced_on: restored_problem`, hashes R1 `e24d499958e3bb6d` and R0 `e6f07f422fbb60e3`]. Phase I returns u\* = 0 in every state, with a t0 execution deficit of $9.5bn at U16 and $6.8bn at U11. So there is no structural recovery, and the duals come only from the restored problem. They are unchanged at ten times the penalty tiers.

| At θ\*, U16 / U11 | R1: revolver signed (μ 0.0113) | R0: group levers + top-up (μ 0.124) |
|---|---|---|
| **FTP_RA on holdings**, scheduled flows (calls less distributions), bp a year | **2.0 / 2.1** | **20.5 / 15.2** |
| FTP_RA with cures included (v1.1's basis, then 3–4 / 66–81bp on v1 duals) | 5.4 / 5.5 | 55.5 / 42.2 |
| **Hurdle on new RA commitments**, bp a year | 13 / 13 | 144 / 105 |
| PE FTP, for comparison | 9.4 / 7.3 | 102 / 57 |

*SYNTHETIC – NOT ADIC DATA.* μ without the revolver halves against v1 (0.124 against 0.243), because RA's JV sell-down becomes the marginal lever.

- **FTP_RA prices scheduled flows only.** Cures, protective calls and distribution stops go to CLC_RA, so each contingent outflow is charged once (main §4.11).
- **CLC_RA = c_buf × CVaR95 of 24-month joint-path cure cash** (direct cures + protective calls + distribution stops), from the integrated Monte Carlo.
  - The CVaR95 is $2.37bn pooled over M1–M6 under Mix B ($2.44bn group-off; worst model M6 $2.44–2.52bn; mean $0.79bn).
  - At c_buf 1.5% that is **$36–38m a year**, ≈20bp of RA NAV ($24–76m at 1–3%). That is 2.6–7× v1.1's $5–14m, which used deterministic cures without availability.
  - With c_buf at the marginal lever's carry μ/5 (≈0.2% with the revolver, ≈2.5% without), CLC_RA is ≈$5m or ≈$60m. That is close to the dual-based cure prices of $6m and $63m, so the two routes agree when c_buf follows the state.
  - Gate V-RA-CLC: CVaR95 of joint-path cures, never a sum of cohort P95s. G14's $24–42m rested on a larger book and such a sum, which bounds nothing [C].
  - The reference engine on the sealed tape has a thinner tail (T4′: ADIC cures CVaR95 $0.54bn, or $0.70bn with protective calls; fund-level need CVaR95 $0.71bn). CLC_RA will fall once the integrated engine adopts the tape [RA20].
- **Risk charges** use leverage-adjusted equity betas (value-add RE 0.77; infrastructure 0.5–0.7), not MSCI's 0.6, which is an unlevered sleeve's beta to a multi-asset portfolio [C].
- **Asset-level cash-outs are dominated in both states:** 0.157 per $ of headroom, on only $0.03bn of t0 capacity, because only Q4-2026 maturities on controlled debt qualify while lock-in exceeds 0.5% of GAV. Without the revolver, the RA JV sell-down (0.124) is the marginal lever and clears before PE pacing (0.213). Ground leases and sale-leasebacks (≥ 0.34) do not [I-calc].

---

## 11. Synthetic-data block for SYN-ADIC-177

**Census v2, Real Assets** (sizes lognormal within each sleeve, σ 0.8 [I], rescaled to sleeve totals):

| Sleeve | NAV / unfunded, $bn | LTV | Positions | Control | Mark segment |
|---|---|---|---|---|---|
| RE open-end core | 2.7 / 0 | 27% | 6 | LP | CORE_RE + queue |
| RE closed-end value-add/opportunistic | 2.6 / 1.2 | 60% | 14 | LP | VA_RE |
| RE JV/direct: global; GCC | 1.7 / 0.2; 1.2 / 0.2 | 45% | 8 | Sole or joint | CORE_RE, VA_RE; GCC_RE |
| RE co-investment | 0.8 / 0 | 60% | 3 | Minority | VA_RE |
| Infrastructure open-end core | 2.0 / 0 | 50% | 6 | LP | CORE_INFRA + queue |
| Infrastructure closed-end | 2.5 / 1.3 | 55% | 25 + 9 CV stakes | LP | VA_INFRA |
| Infrastructure direct/co-investment | 2.0 / 0.3 | 55% | 20 | Mixed | CORE_INFRA, VA_INFRA |
| ENR closed-end | 1.6 / 0.6 | 35% | 16 | LP | ENERGY |
| ENR direct/co-investment | 0.9 / 0.2 | 40% | 8 | Mixed | ENERGY |
| **Total** | **18.0 / 4.0** | **49%** | **115** | | |

*SYNTHETIC – NOT ADIC DATA.* Mixes [I]: real-estate sectors (G10) logistics 26%, residential 27%, office 21%, retail 8%, data centres 4%, hotels 6%, alternatives 8%; regions US 60%, Europe 21%, Asia 6%, Gulf 13%. Infrastructure segments (G11 weights on $6.5bn): regulated 18%, contracted indexed 8%, contracted fixed 14%, toll 12%, airports 8%, midstream 10%, towers 10%, data centres 12%, merchant 8%. ENR as §9.3; vintages 2012–25; GP decks from the vintage curve ±10%. Counts are G11's (infrastructure) and mid-points of G12's ranges (ENR).

**Sealed inputs** (v1.2).
- *Debt tape* (ra_gap_02):
  - 198 tranches on 188 assets carry the census's $17.43bn at ADIC share. They are calibrated to MBA's 2026 maturity shares by holder, CBRE, CRED iQ, Accordant, project-finance norms and the OCC RBL handbook.
  - The seed is 20261059, chosen by a rule fixed before any engine run.
  - SHA-256: assets `79e9c5a0…`, tranches `6637ce25…`; the full hashes are in `ra_gap_02_calcs/ra_tape_manifest.json`, and `load_tape()` refuses a broken seal. The schema is `ra_tape_tranches_v1.csv`.
  - The tape retires G15's MATURITY_PA and its implicit V^mat.
- *Closed-end vintage history* (ra_gap_04):
  - File `ra_gap_04_calcs/sealed_ra_ce_history_v1.csv`, SHA-256 `5ed8acfd735f0d6b0425f0762ee61805f5b4d0654e44c59f72f0b51a897171a3`.
  - Commitments: RE flat ($0.33bn, then $0.43bn from 2021); infrastructure +6.2% a year ($0.15bn → $0.45bn); ENR −3.2% a year ($0.25bn → $0.20bn).

**Truth, observation and variants.**
- *Truth:* G10's property markets; G11's structural archetypes with indexation, resets and jumps; G12's curve and asset engines; G14's debt machine with a common lender factor; the fund-level refinancing module.
- *Start state:*
  - late cycle, Gulf war (≈0.85, 7.5 months elapsed), exit drought (0.87);
  - financing window f₀ = N (SLOOS −11.3), with the RE transaction window in D;
  - 10y 5.10%, short rate 3.90%, CPI 3.7%; Baa − 10y 1.44% (FRED, 15 Oct 2026; v1.1's ≈2.0% corrected);
  - oil from the 15-Oct-2026 strip (Dec-26 $105.92; spot $126.55);
  - queues 10% (US) and 5% (Europe and infrastructure evergreen); G₀ 2%.
- *Observation (G13):* two-component smoothing with calendar noise (§5); listed proxies with an AR(1) premium; transaction indices, carrying a lag state and an optional appraisal-contamination loading (§8.2); secondary bids, used leave-one-out; sales selected on (v − a) plus forced sales in the down state; underwriting and forecasts with the §8.4 biases, w_a 0.30 and κ. Marks are net IRR/MOIC with P10/P50/P90 cases, archived quarterly and bitemporally; the agriculture-and-timber template stays disabled.
- *Pre-registered axes:* call multiplier ×1.0 / ×1.38; fund-level shortfall to cash or to NAV; extension at G10 values or zero; ϖ 0 or 1; G₀ 0 / 2 / 5–8%; a transaction index lagged 1–2 quarters, AR-smoothed 0.3–0.5 or level-biased; regime and Q4-seasonal λ; regime-dependent optimism (M1), which binds hardest in a real-estate drought. Results so far [I-calc]:
  - Calls ×1.0 instead of ×1.38 move the structural T4′ drain from −$1.64bn to −$0.55bn, and the Tier-1 row to −$3.79bn.
  - Sending all fund shortfalls to cash takes the Tier-1 row to −$5.05bn.
  - Extension at zero against G10's values moves the Tier-1 row from −$4.02bn to −$4.57bn, and the structural cure CVaR95 with protective calls from $0.70bn to $0.85bn.
  - ϖ = 0 cuts the structural T4′ cure CVaR95 to $0.35bn.
  - Ĝ keeps 7–23% of any starting gap.
  - A lagged index fails R2 and G-B; AR smoothing fails G-B; a drought-only level bias passes 3/5.
  - Downturn λ (M1) passes.

**Gates**, frozen and hashed with G-A–G-E before the first scored release [RA19]:

| Gate | Check | Status on SYN (v1.2) |
|---|---|---|
| V-RA1 | Appraisal vs sale on Cannon & Cole's adjusted basis (sale price rolled back by appraisal-based NPI appreciation); \|z\| ≤ 2 on boom and crash; MAE band 10–14% (CORE_RE), 12.5–16.5% (VA_RE) | CORE_RE passes with λ + 0.10 in downturns: MAE 10.9%; crash −9.1% (z +1.7); boom +12.1% (z +0.6). At G13 defaults the crash is too shallow (z +2.4). VA_RE's 17.1% was a basis artefact: 14.8% sits inside its band (ra_gap_04) |
| V1, R1, R3 | Fund AC1 0.45 ± 0.05; λ bias ≤ 0.03; three-step β ≥ 75% of true | Pass (0.42; ≤ 0.01; 75–85%); λ intervals need the bootstrap |
| R2 | Nowcast RMSE ≤ 50% of appraisal error under a misspecified τ | Passes only for a contemporaneous τ (0.27–0.49); fails with a 1–2-quarter lag (0.53–0.74). It keeps its τ condition, and IC figures stay listed-only until the lag test passes |
| G-A–G-E (RAME) | Canonical ensemble, five segments | G-A 5/5; SBC 4/5 (CORE_RE 0.725); G-B passes M1, M3, M5 and M6 and fails M4, M2 and M5s; G-C fails; G-D lag power 0.99–1.00 |
| R4–R8 and G-A–G-E (forecasts) | Controlled-bias coverage (R4 gives way to G-A / G-B two-sided bands); κ (R5 becomes the random-effects coverage error); honest forecaster wins on true outcomes; shrinkage ≤ GLS; incurred Benktander best | FBE-R-RA passes G-A, G-B (except M5s) and G-C; G-E binds; GLS fails every variant; R6 and R8 pass |
| V-RE1, V-RE3 | Same-store NOI within ±1pp of 0.78% (not overall NPI NOI, 2.2%) [C]; desmoothed 2022–24 drawdown within ±5pp of relevered REITs | Pass |
| G-ODCE | 2021Q4–2026Q2 replay of the RE layer: appraisal drawdown −18.8% ± 3pp; true −25.7% ± 5pp; trough lag 3 ± 1 quarters | Drawdowns pass (−16.6%; −22.4%). The lag fails at λ_agg 0.75 (5 quarters) and passes at 0.55–0.70, so the engine uses 0.60 (ra_gap_02) |
| G-Jiang | CMBS replica at 2023Q4: shares above 80% / 100% LTV, all loans and office, ± 4pp | Fails as specified (office > 100%: 34.3% vs 44.6%; all: 8.6% vs 14.3%). After a 3-parameter fit, the all-loan > 80% hold-out passes and office fails |
| G-Chen | Refinance share falls 0.111 per pp of rate gap (Chen & Chen) | The capacity channel alone gives ≤ −0.019 ✗. A sponsor hazard matches by construction (calibration, not validation); an independent hold-out is needed |
| CF-X1–X6 | External cash targets: RE distributions (Ares); contribution rates and drought NAV growth (MSCI); open-end income; queue | CF-X1 passes (7.8% vs 7%; 17.4% vs ≈21%). CF-X2 fails for infrastructure (21.7% vs 29% ± 5pp). CF-X3 fails for RE (+3.2pp). X4–X5 are identities; X6 = V-RE2 |
| OIL-X1–X3 | ENR marks 2014–16; mark timing in the 2026 spike; sleeve elasticity | OIL-X1 passes (−14.7% vs −20.5% ± 7pp). OIL-X2 rejects the 2-quarter deck lag for fund NAVs. OIL-X3 passes at the low end (0.34 vs 0.33–0.71) |
| V-RE2 (CF-X6) | Queue out of sample: GFC peak, payout speeds, fund dispersion | GFC peak fails (40% vs 15–21%, conservative); 2023 payout passes (7.6%); dispersion is a calibration |
| RA-R15 | Sealed closed-end history (hash above): pace and callable unfunded; V17 coverage 0.85–0.95 and \|bias\| ≤ 5% | Bias −1% to −3% passes; coverage 0.76–0.90 fails on width; an estimator without lapse overstates callable unfunded by 30–39% |
| V-RE4–7 | GAV = D + E; one property draw shared with PC; reported NAV never in the kernel; open-end credit only via φ | Engine tests |
| V-RA-CTRL | No REFINANCE, LEVER or HEDGE card on LP or minority holdings (extends V23) | Pass (`test_v_ra_ctrl.py`, 4/4) |
| V-RA-θ; V-RA-CLC | RA θ components pass through G15's values at θ 0.76; CLC on CVaR95 of joint-path cures, never summed cohort P95s | By construction; implemented (ra_gap_01) |
| Invariants | Cures ≤ maturing debt; intra-ADIC flows net to zero on cash and DVA ledgers | Engine tests |
| V-RA-CF, V-RA-OIL (retired as validation) | Reproduce G15's cash row (+0.40, −0.16, −1.32 / −2.46); pin G12's delta | They could not fail, so they are kept only as regression tests. ra_gap_01 reproduces G15's row exactly; ENR 10.4m ± 5% and RA 11.2m bbl at the 15-Oct-2026 strip |

**Labels.** L1–L8 as in groups §6: `SYN-` ids, `is_synthetic=true`, provenance flags, the footer, taint propagation, sealed truth and a claim validator. SYN-ADIC-177 tests correctness and robustness, not the choice between estimator variants (Advani, Kitagawa & Słoczyński 2019).

---

## 12. IC implications

**The Real Assets seat.** It is a mandate seat, not a personality persona (groups §7.1). With it the shadow IC has 13 seats, as the main report (§6.2) and the groups report (§7.1) now state, still with ≥ 3 model families and ≤ 40% of seats per family.

| Loss emphasis | Evidence slice | Standing question |
|---|---|---|
| Stale marks mistaken for value; refinancing walls and cures; queue illiquidity; owner-correlated oil and Gulf exposure | Marks panel (V^A, V\*, Ĝ, θ̂^eq with bands); debt-wall card (controllable maturities, LTV and DSCR headroom on V\*, cap expiries, cure CVaR95 under ϖ); queue card (positions, φ); oil-ledger card (barrels by group and state at the canonical strip, the liability in barrels, H_j by group, against the RA envelope and the Tier-1 backstop); cash row (Tier-1 and structural) and L4 budget; DVA on V\* | Is it priced and paid on V\*, is the action in the holding's control cell (V-RA-CTRL), and what does it do to the oil delta, H_j and the 24-month cure tail? |

The seat recuses on RA envelopes, is scored on total-portfolio regret, not group P&L, and discloses its home-market conflict on GCC real estate; in recovery it adds its catalogue rows (RA pacing stop; pre-arranged cash-outs and sell-downs) and delivery against φ_RA.

**Attribution** (ra_gap_01; exact values over 1,024 coalitions × 10,000 paths; U16, Mix B) [I-calc].
- **Credit.** RA is the tenth Shapley player: −2.3 / −4.3 / −5.2pp of P(red) and +$0.26 / 0.50 / 1.09bn of CE in M1 / M4 / M6. It ranks fourth of ten on both, with 8–9% of the P(red) reduction and 6–8% of the CE gain.
- **Stand-alone attribution** would credit it 2–4× more, because notices and JV sell-downs substitute for CF and Public Markets levers.
- **The CE gain is insurance.** RA's φ on E[W̃] is −$0.21 / −0.02 / +0.17bn, and its playbook trims the cure CVaR95 by $0.07–0.08bn.
- **Cash.** Without its playbook RA is a net cash user in year 1 on 73–84% of paths. With it (open-end notices of $3.3–4.1bn over five years, plus the ENR SELL as then modelled) it is a cash source.
- **P(red).** Do-nothing P(red) on the v2 book is 1.45% (M1) / 11.6% (M6) at U16, and 0.83% / 7.9% at U11. Mix B gives 0.00% in M1–M5 and 0.04% in M6.

**KPIs.** Ĝ and θ̂^eq by segment; the cash row against plan; controllable LTV, 12- and 24-month maturities, unhedged floating share and cure CVaR95; queue positions and φ; oil delta by group and state against the RA envelope and the Tier-1 backstop, with H_j charged; callable beside contractual unfunded; the owner-correlation metric (the glut's loss of cash and true value); the indexed share of infrastructure; forecast information value by component, against RA's own reference class and only when n_eff ≥ 20.

**Discussion** (groups §7.2). Block A shows RA in the cash map, L4, L8 and the Tier-1 board, never as liquidity. Block B carries envelope use and decision cards (P(best), regret both ways, the LAPV waterfall at V\*, flip thresholds, the four marks, the control cell, `priced_on`). Block C covers PC and CS financing of RA assets, Secondaries purchases of RA stakes, Overlay hedges and PE boundary cases.

**Decision rights.** The group decides in-envelope deals and asset-level debt on controlled holdings, inside CF's envelope and guarantee policy. Tier A adds:
- any change of ϖ, the barrel price, the backstop or the recovery rule;
- sleeve LTV rises above 5pp;
- GCC real-estate acquisitions;
- actions ≥ 0.25% of NAV, including any ENR SELL, which also needs a passing confirmatory sealed run.

The Board sets ϖ and the RA range.

---

## 13. Consolidated calibration table

| Quantity | Value | As of | Source |
|---|---|---|---|
| NFI-ODCE | 1.49% gross in 2Q-26; leverage 27.1% (average 22.4% since 2000); year-to-June flows −$8.7bn | Jul 2026 | NCREIF |
| ODCE repricing | −18.8% over 7 quarters to 2Q-24; relevered REITs −25.7%; AC1 0.72; trough lag 3 quarters (one episode) | 2022–26 | NCREIF; Nareit [I-calc on S] |
| ODCE queues | 19.3% (1Q24); just above 10% (Q1-26); GFC ≈15% (Callan) or ≈21% of core NAV (Townsend) | 2009–26 | Callan; Accordant; Kochis & Moné |
| Cap rates | NPI appraisal ≈4.4%; transactions 5.6% (apartments) to 8.3% (hotels) | 2026 | NCREIF; MSCI RCA |
| LP pricing | RE 68%; infrastructure 91%; all strategies 87% | H1-26 | Jefferies |
| Lending terms | Spread 204bp; LTV 59.6%; DSCR 1.43 (stale against October rates) | Q2-26 | CBRE |
| Maturities; delinquency | $875bn (17%) maturing in 2026; CMBS office 12.16% | 2026 | MBA; Trepp (relay) |
| Negative equity (CMBS) | Above 100% LTV: 14.3% of CRE loans, 44.6% of office; above 80%: 29.0 / 56.0%; current LTV 66.2 / 86.0% | 2023Q4 (rev. 2024) | Jiang et al. |
| Maturity-wall behaviour | Refinance share −0.111 (s.e. 0.019) per pp of rate gap; rollover-sale discount 11.5–12.7%; about half of maturing loans extended in 2023–25, 5pp / 7pp less for non-recourse / low debt yield; office payoff ≈20% in stress | 2003–19; 2023–25 | Chen & Chen; Glancy |
| CRE prices | Green Street CPPI −22% from the March-2022 peak, office −35% | Nov 2023 | Green Street via Bisnow [S-sec] |
| RE fund alpha | Closed-end −165bp vs REITs; non-core −285 to −326bp vs levered core | 2019–21 | Arnold et al.; Bollinger & Pagliari |
| Appraisal error | Adjusted basis: mean absolute 12.5%; 2006 boom +11.6% (s.e. 0.8%); 2008 crash −11.0% (s.e. 1.1%); property increments levered +1.0pp, office +1.5pp, no recent appraisal +2.2pp | 1984–2010 | Cannon & Cole |
| Smoothing | Fund AC1 0.45; aggregate 0.75 | 1994–2017 | Couts et al. |
| Infrastructure | Appraisal volatility 2–3% vs 7–12% market-implied; duration 7.4–11.6; PME 0.93 | 2021 | EDHECinfra; Andonov et al. |
| Private energy | 3.2% a year (2013–23); 0.56× MOIC gap to PE | 2023; 2020 | Meketa/CA; CA |
| Private-capital flows | Contribution rate 29% ± 5pp (H1-26); closed-end NAV growth 2024–25: RE −0.15%, infrastructure +9.5%, natural resources +4.3%; natural resources Q1-26 +6.9%, Q2-26 +3.6% | Q2 2026 | MSCI |
| RE fund distributions | 7% of NAV in the year to Q3-25, about a third of the 10-year average | Feb 2026 | Ares |
| RBL | Advance 50–65%; cures in 3–6 instalments; expected base cut −38% (2016) | 2015–20 | OCC; Latham; Haynes Boone |
| Gulf property | UAE −36.5% (2008–10); Dubai Q3-26 sales −47% by value; UAE prices' fiscal β to Brent 0.12–0.14 (Newey–West s.e. 0.05) | 2003–26 | BIS via FRED [I-calc on S]; The National |
| Macro state | 10y 5.10% (15 Oct); SOFR 3.89%; Baa − 10y 1.44% (15 Oct); Brent $126.55 spot (14 Oct) against futures ≈$105–110 | Oct 2026 | FRED; EIA; ICE |
| Lending standards (SLOOS, CRE) | Net tightening −11.3 (2026Q3); N / T / C in 69 / 19 / 12% of 1990–2026 quarters at thresholds 20 / 50 | 1991–2026 | FRED DRTSCREL, SUBLPDRCSN |
| Brent strip and volatility | Dec-26 $105.92, Dec-27 $85.08, Dec-30 $69.16 (15 Oct); OVX 49.13; EIA 2027 Brent $83.74 | Oct 2026 | CME via Baratelli [S-sec]; FRED OVXCLS; EIA STEO |
| Energy weights | MSCI ACWI energy 3.96%; Pantheon International 2% | Sep / Aug 2026 | MSCI; ticker.app [S-sec] |

---

## 14. Questions for the user

1. **Size and vehicles.** Is $18bn right? It is still a working figure (context §1A, re-read 2026-10-19). The objective is flat across 6–14% of NAV, so size is a governance choice. What is the split across open-end, closed-end, JV/direct and co-investment, and ADIC's share of any open-end or evergreen fund?
2. **Sectors and regions.** Sub-sector weights; GCC real estate; Gulf-located or Gulf-volume-dependent assets. Is domestic real estate in scope, and are any holdings strategic and outside the optimiser?
3. **Control rights.** For each holding: sole, joint, minority or LP, and JV terms (ROFO/ROFR, buy–sell, consents, cash calls); they set the admissibility matrix.
4. **Debt tapes and GP behaviour.** Asset-level debt by tranche (maturity, fixed/floating, caps, covenants, extensions, guarantees), in the sealed tape's schema; who funds cures, the group or CF; and GP extension, cure and sale history for 2023–25. The cure tail sits mostly in GP-controlled funds, beyond ϖ's reach.
5. **Default policy.** Will ADIC ever hand back keys on non-recourse debt (ϖ)?
6. **Open-end terms.** Notice and payment rules (pro rata or FIFO), revocability, caps, queue positions, side letters and fund-level queue statements. These decide whether notices at Amber redeem $3–4bn over five years, as modelled.
7. **Forecast archive.** Do archived plans store components (exit cap, NOI growth, capex, hold, traffic, price deck), or only IRR/MOIC with cases? Absent components cost ≈2pp of CRPS. Are declined deals kept?
8. **Valuation policy.** Appraisal frequency, external share, valuer rotation, GCC valuers and ad hoc triggers. Does ADIC adjust GP NAVs? What applies to holdings under a SELL flag? What were ADIC's RA sales against the last appraisal? Which transaction index is licensed, and with what lag?
9. **ENR.**
   - Holdings by sub-sleeve; asset-level and overlay oil-hedging permissions and size; RBL terms.
   - Live secondary bids and the GP price decks for fund-held upstream; the SELL needs a strip-based θ̂.
   - Any oil exposure the owner wants held deliberately.
   - Should the owner's oil exposure enter Tier 2 (the surplus framing, ≈$0.7–1.5 per bbl more) or only Tier 1?
10. **Classification.** Confirm partial-SELL treatment of sell-downs, midstream in infrastructure, RE and infrastructure debt in Private Credit, RA co-investments in RA, and the infrastructure-versus-PE label rule.
11. **Limits.** Existing RA leverage, maturity, development, merchant or digital limits. Do you accept the 8–12% judgment band, the $1.8bn pacing envelope with 45 / 45 / 10 as a direction, the barrel price and backstop, and the sub-limits?
12. **Links and conventions.** Do Private Credit or Capital Solutions lend to RA holdings? Is NAV net of purchaser's costs? Are Islamic-finance structures used? Which benchmarks can be licensed (Green Street, MSCI/NCREIF, RCA, SIPA)?
13. **Closed-end commitments.** RA commitments by fund and vintage, with commitment periods and recycling terms. Callable unfunded is only ≈70% of contractual.
14. **Funding state and census.** Which funding state should price next quarter's RA envelopes? FTP_RA is 2bp once the revolver signs and 21bp before. Which PE unfunded figure governs, $16.4bn or $10.9bn? θ\*, the facility need and L8 differ materially between them.

---

## 15. Bibliography

*Deduplicated across G10–G15 and ra_gap_01–04, in corrected form. [S-sec] marks secondary relays.*

**Academic**
- Advani, Kitagawa & Słoczyński (2019). Mostly harmless simulations? *J. Applied Econometrics*. https://doi.org/10.1002/jae.2724
- Andonov, Eichholtz & Kok (2015). Intermediated investment management in private markets. *J. Financial Markets* 22, 73–103. https://doi.org/10.1016/j.finmar.2014.11.002
- Andonov, Kräussl & Rauh (2021). Institutional investors and infrastructure investing. *RFS* 34(8), 3880–3934. https://doi.org/10.1093/rfs/hhab048
- Arnold, Ling & Naranjo (2021). Private equity real estate fund performance. Nareit-hosted paper. https://www.reit.com/sites/default/files/2021-07/PERE_Fund_Performance_Arnold_Ling_Naranjo_Final_Version.pdf
- Bain (2009). Error and optimism bias in toll road traffic forecasts. *Transportation* 36(5), 469–482. https://doi.org/10.1007/s11116-009-9199-7
- Blanc-Brude, Gupta, Lu & Wee (2021). The volatility of unlisted infrastructure investments. EDHECinfra. https://www.edhecinfraprivateassets.com/wp-content/uploads/2021/05/P74_EDHEC-LTIIA_Volatility.pdf
- Bollinger & Pagliari (2019). Another look at private real estate returns by strategy. *JPM* 45(7), 95–112. https://doi.org/10.3905/jpm.2019.1.098
- Brown, Gredil & Kaplan (2019). Do private equity funds manipulate reported returns? *JFE* 132(2), 267–297. https://doi.org/10.1016/j.jfineco.2018.10.011
- Cannon & Cole (2011). How accurate are commercial real estate appraisals? *JPM* 35(5), 68–88. https://doi.org/10.3905/jpm.2011.35.5.068 (eq. 1–4; Tables 2A, 4A, 4B and 8; MPRA 32589, https://mpra.ub.uni-muenchen.de/32589/1/MPRA_paper_32589.pdf)
- Castro, Gómez & Tejada (2009). Polynomial calculation of the Shapley value based on sampling. *Computers & Operations Research* 36(5), 1726–1730. https://doi.org/10.1016/j.cor.2008.04.004
- Chen & Chen (2025). The writing on the maturity wall. Working paper. https://haas.berkeley.edu/wp-content/uploads/archive/The-Writing-on-the-MAturity-Wall.pdf
- Chervachidze, Costello & Wheaton (2009). Determinants of capitalization rates. *JPM* 35(5), 50–69. https://doi.org/10.3905/JPM.2009.35.5.050
- Couts (2025). Liquidity transformation risks and stabilization tools. *REE* 53(5), 1009–1044. https://doi.org/10.1111/1540-6229.12532
- Couts, Gonçalves & Rossi (2024). Unsmoothing returns of illiquid funds. *RFS* 37(7), 2110–2155. https://doi.org/10.1093/rfs/hhae006
- Devaney & Scofield (2015). Liquidity and the drivers of search, due diligence and transaction times for UK commercial real estate. *J. Property Research* 32(4), 362–383. https://doi.org/10.1080/09599916.2015.1089924
- Elliott & Liao (2026). Combining forecasts: on why averaging beats optimal linear weights. *JBES*. https://doi.org/10.1080/07350015.2026.2661980
- Fisher, L. M. & Hartzell (2016). Class differences in real estate private equity fund performance. *JREFE* 52(4), 327–346. https://doi.org/10.1007/s11146-015-9526-z
- Geltner (1991). Smoothing in appraisal-based returns. *JREFE* 4(3), 327–345. https://doi.org/10.1007/BF00161933
- Glancy (2026). Pretend or amend? On evergreening in CRE. FEDS 2026-025. https://doi.org/10.17016/FEDS.2026.025
- Gupta, Mittal & Van Nieuwerburgh (2026). Work from home and the office real estate apocalypse. *AER* 116(2), 674–709. https://doi.org/10.1257/aer.20231619
- Gupta & Van Nieuwerburgh (2021). Valuing private equity investments strip by strip. *JF* 76(6), 3255–3307. https://doi.org/10.1111/jofi.13073
- Hoesli, Lizieri & MacGregor (2008). Inflation hedging characteristics of US and UK investments. *JREFE* 36(2), 183–206. https://doi.org/10.1007/s11146-007-9062-6
- Jiang, Matvos, Piskorski & Seru (2023, rev. 2024). Monetary tightening, CRE distress and US bank fragility. NBER w31970. https://www.nber.org/papers/w31970
- Neuhaus (2025). The Benktander golden stairs and other parameter-free credibility methods in loss reserving. *SAJ* 2026(4), 392–411. https://doi.org/10.1080/03461238.2025.2536811
- Plazzi, Torous & Valkanov (2010). Expected returns and expected growth in rents. *RFS* 23(9), 3469–3519. https://doi.org/10.1093/rfs/hhq069
- Ranjan & Gneiting (2010). Combining probability forecasts. *JRSS-B* 72(1). https://doi.org/10.1111/j.1467-9868.2009.00726.x
- Rödel & Rothballer (2012). Infrastructure as hedge against inflation: fact or fantasy? *JAI* 15(1), 110–123. https://doi.org/10.3905/jai.2012.15.1.110
- Schwartz & Smith (2000). Short-term variations and long-term dynamics in commodity prices. *Management Science* 46(7), 893–911. https://doi.org/10.1287/mnsc.46.7.893.12034
- Sovacool, Gilbert & Nugent (2014). Construction cost overruns for electricity infrastructure. *ERSS* 3, 152–160. https://sussex.figshare.com/articles/journal_contribution/An_international_comparative_assessment_of_construction_cost_overruns_for_electricity_infrastructure/23424974
- Wurstbauer & Schäfers (2015). Inflation hedging of infrastructure and real estate. *JPIF* 33(1), 19–44. https://doi.org/10.1108/JPIF-04-2014-0026

**Official, sovereign and peer**
- ADIA (2026). ADIA Review 2025. https://www.adia.ae/en/pr/2025a/index.html
- Cambridge Associates (2026). FY2025 Annual Review of Endowments. https://publishedresearch.cambridgeassociates.com/fiscal-year-2025-annual-review-of-endowments-asset-allocation-and-implementation/
- EIA (Oct 2026). Short-Term Energy Outlook (Tables 1, 2 and 3b). https://www.eia.gov/outlooks/steo/archives/oct26.pdf
- FRED: DGS10, CPIAUCNS, CPIAUCSL, GDPC1, QAEN628BIS (BIS UAE prices), DCOILBRENTEU, DRTSCREL, SUBLPDRCSN, BAA10Y, OVXCLS (downloaded 18–19 Oct 2026). https://fred.stlouisfed.org/
- GIC (2026). GIC Report 2025/26. https://www.gic.com.sg/uploads/2026/07/GIC_AR_2025-26_PRINT.pdf
- HM Treasury. Green Book supplementary guidance: optimism bias. https://www.gov.uk/government/publications/green-book-supplementary-guidance-optimism-bias
- NBIM. Investment mandate, amended 9 Dec 2025. https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/
- Norges Bank (26 Apr 2018). Energy stocks in the GPFG. https://www.nbim.no/contentassets/5beb197aa8c544b39fe547e2d6eb3b13/2018-04-26-nb-to-mof-energy-stocks-in-the-gpfg.pdf
- OCC (2018). Comptroller's Handbook: Oil and Gas E&P Lending. https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/files/oil-gas-exploration-prod-lending/pub-ch-oil-and-gas.pdf

**Market and practitioner**
- Accordant (25 Jun 2026). Q1 2026 NFI-ODCE insights. https://www.accordantinvestments.com/knowledge-center/private-real-estate-enters-a-new-cycle-q1-2026-nfi-odce-index-insights
- Ares (11 Feb 2026). Real estate secondary market volume hits record $20 billion in 2025. https://www.ares.com/us/news-and-insights/real-estate-secondary-market-volume-hits-record-20-billion-2025
- Arthur Cox (2021). Project-finance covenants [P]. https://www.arthurcox.com/wp-content/uploads/2021/05/Article-11-Buckley.1.pdf
- Baratelli Institute (17 Oct 2026). Oil forward curve, relaying CME Daily Bulletin #199 (NYMEX BZ settlements, 15 Oct 2026) [S-sec]. https://baratelliinstitute.com/oil-futures-curve
- Bisnow (2023). Brookfield defaults on Gas Company Tower and 777 Tower. https://www.bisnow.com/news/los-angeles/commercial-real-estate/brookfield-default-downtown-los-angeles-gas-tower-777-figueroa-117640
- Callan (20 Feb 2025). Private real estate valuations may have bottomed; REITs fall. https://www.callan.com/blog/4q24-real-estate/
- Cambridge Associates (2020). Real asset dynamics: PE energy. https://www.cambridgeassociates.com/insight/real-asset-dynamics-pe-energy/
- Campbell Lutyens (Aug 2026). 1H 2026 secondary market full report. https://campbell-lutyens.com/media/keapzv55/campbell-lutyens-1h-2026-secondary-market-full-report_august-2026.pdf
- CBRE (3 Aug 2026). CRE lending fundamentals, Q2 2026. https://www.cbre.com/press-releases/commercial-real-estate-lending-fundamentals-remain-strong-q2-2026-cbre
- CBRE Investment Management. Infrastructure Quarterly, Q4 2025 (Dec 2025) and Q3 2026 (Oct 2026). https://mediaassets.cbre.com/-/media/project/cbre/bussectors/cbreim/insights/articles/2025/december/infrastructure-quarterly-q4-2025/infrastructure-quarterly-q4-2025.pdf ; https://www.cbreim.com/insights/articles/infrastructure-quarterly-q3-2026
- Commercial Observer (27 Mar 2023). CRE CLO interest rate cap agreements (CRED iQ). https://commercialobserver.com/2023/03/cre-clo-interest-rate-cap-agreements-spotlight
- Green Street (6 Feb 2024). Commercial Property Price Index, January 2024. https://ca.greenstreet.com/commercial-property-price-index-january-2024/ ; November-2023 data via Bisnow (8 Dec 2023) [S-sec]. https://www.bisnow.com/national/news/capital-markets/green-street-cre-prices-fell-another-3-but-may-well-have-hit-bottom-121991
- Haynes and Boone (2016; 2020). Borrowing-base redetermination surveys. https://www.haynesboone.com/press-releases/spring-2016-borrowing-base-redeterminations ; https://www.haynesboone.com/news/press-releases/spring-2020-oil-and-gas-industry-surveys
- HDFCSky (17 Oct 2026). Weekly review: Dec-26 Brent $105.92 [S-sec]. https://hdfcsky.com/news/brent-holds-above-105-as-hormuz-attacks-cut-gulf-flows-68percent-wti-jumps-5-81percent-on-record-us-inventory-draw
- ION Analytics / Infralogic (5 Jun 2026). Open-ended funds' appeal endures despite lull (bfinance data). https://ionanalytics.com/insights/infralogic/open-ended-funds-appeal-endures-despite-lull/
- Jefferies (Jul 2026). Global Secondary Market Review. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- J.P. Morgan Asset Management (2026). Long-Term Capital Market Assumptions. https://am.jpmorgan.com/us/en/asset-management/adv/insights/portfolio-insights/ltcma/
- KBRA (20 Oct 2023). CRE CLO refinance challenges ahead for 2021–22 vintage loans [S-sec]. https://www.businesswire.com/news/home/20231020398101/en/KBRA-Releases-Research-CRE-CLO-Refinance-Challenges-Ahead-for-2021-22-Vintage-Loans
- Kochis & Moné (2024). Negative fundraising: redemption queues. *PREA Quarterly*. https://www.prea.org/publications/quarterly/negative-fundraising/
- Latham & Watkins (2015). E&P liquidity Q&A (J. Michael Chambers). https://www.lw.com/admin/Upload/Documents/Are-You-an-E-and-P-Company-Facing-a-Liquidity-Crunch-and-Considering-Restructuring.pdf
- MBA NewsLink (9 Feb 2026). 17% of commercial mortgage balances mature in 2026. https://newslink.mba.org/?p=270033
- Meketa (Mar 2024). Private natural resources. https://meketa.com/wp-content/uploads/2024/03/MEKETA_Private-Natural-Resources.pdf
- Moody's Investors Service (10 Jun 2020). Infrastructure & project finance – global: defaults & recoveries. https://ma.moodys.com/rs/961-KCJ-308/images/Default%20Reports%20-%20Infrastructure-Project-Finance-Global%20-%2010Jun20.pdf
- MSCI (30 Sep 2026). MSCI ACWI Index factsheet. https://www.msci.com/documents/10199/255599/msci-acwi-net.pdf
- MSCI (2026). Private Capital Benchmarks Summary, Q2 2026 (pp. 7, 12, 13, 16). https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
- MSCI (2026). Real Assets in Focus: trends for 2026. https://www.msci.com/downloads/web/msci-com/research-and-insights/blog-post/real-assets-in-focus-trends-to-watch-for-2026/Real-Assets-in-Focus-Trends-to-Watch-for-2026.pdf
- MSCI (Mar 2026). US RCA Capital Trends, February 2026. https://www.msci.com/downloads/web/msci-com/data-and-analytics/real-estate/us-rca-capital-trends-report/2603-usct-bigpic-rca-msci-pg1.pdf
- Nareit. Monthly index values and returns. https://www.reit.com/data-research/reit-indexes/monthly-index-values-returns
- NCREIF (2026). NFI-ODCE 2Q2026 release (30 Jul) and 2Q-2026 webinar slides. https://ncreif.org/__static/jdj5jdewjhb0mxrsum1ysdnxmwxqmzv6/NFI-ODCE-Press-Release-2Q2026(2).pdf ; https://ncreif.org/__static/jdj5jdewjfhaei55n3y0ehq3dxyyqvpj/NCREIF-Indices-Review-Webinar-Slides-2Q-2026.pdf
- Pantheon International factsheet (31 Aug 2026), via ticker.app [S-sec]. https://funds.ticker.app/investment-trusts/PIN
- Reuters via Khaleej Times (22 Apr 2026). How the Iran war oil and gas supply shock compares with past disruptions [S-sec]. https://www.khaleejtimes.com/world/mena/how-the-iran-war-oil-and-gas-supply-shock-compares-with-past-disruptions
- Safehold Q2-2026 results, via Investing.com [S-sec]. https://www.investing.com/news/company-news/safehold-q226-slides-multifamily-focus-drives-growth-amid-valuation-gap-93CH-4826424
- *Secondaries Investor* (29 Feb 2016). Energy and venture pricing fell further in H2 (Harken Capital data; paywalled) [S-sec]. https://www.pei-secondariesinvestor.com/energy-and-venture-pricing-fall-further-in-h2/
- SIPA (Jan 2026). Expected returns: 2026 capital market assumptions. https://publishing.sipametrics.com/papers/20260115_capital_market_assumptions.pdf
- Stonepeak-Plus Infrastructure Fund (2026). Form 10-K, FY2025. https://www.sec.gov/Archives/edgar/data/0002045458/000204545826000012/sp-20251231.htm
- Thames Water (2024). Shareholder update. https://thameswater.co.uk/news/shareholder-update
- The National (7 Oct 2026). Dubai home sale transactions fall in Q3. https://www.thenationalnews.com/business/property/2026/10/07/dubai-home-sale-transactions-fall-in-third-quarter-due-to-regional-uncertainty/
- Trepp September 2026 delinquency, via Yieldpro [S-sec]. https://yieldpro.com/2026/10/multifamily-cmbs-delinquency-rate-leads-overall-rate-higher-in-september

---

## SPECIFICATION CARD: Real Assets (Group 8)

**Mandate.** Real estate, infrastructure and energy & natural resources (no agriculture or timber), through funds, co-investments, JVs and direct assets, inside the ~60% private allocation [A]. Working NAV $18bn, still a working figure (context §1A re-read 2026-10-19); unfunded ≈$4bn [A]. The group sources, underwrites, forecasts and executes, often through operating partners; control rights decide which actions exist.

| Item | Specification |
|---|---|
| **Holdings and schema** | As §3: holding → RA → {RE, INF, ENR} → segment, keyed by `vehicle` and `control`; fund terms, JV rights, operations, per-tranche debt tape, bitemporal IRR/MOIC marks with cases and plan components, risk tags, `is_synthetic` |
| **State and decisions** | Per path and quarter: property (rent, occupancy, NOI, cap rate, V^T, V^A, Ĝ, listed wedge ν); infrastructure (CFADS, DSCR, lock-ups, RAB and reset clock, volume jump); ENR (curve, borrowing base); debt (sealed-tape tranches, hedges, V^mat and LTV on V\*, trap, extension and forbearance flags); vehicle (queue, ADIC request, contractual and callable unfunded, effective age); global S, e, Z, the financing window f, e^RE and the oil strip. Within each control cell: SELL fraction by route; open-end notices; HOLD with cure-or-hand-back under declared ϖ; REFINANCE and LEVER on controlled holdings; HEDGE; closed-end pacing |
| **Model** | Reference engine: ra_gap_02 on the sealed tape, keyed to (S, e, Z, f). Closed-end: RFT-TA v2 with real-asset income terms, drought exit multiplier 0.33, lapse and recycling, and the fund-level refinancing module. Perpetual: RE property layer (lease roll, sticky opex, partial-adjustment cap rate); infrastructure structural archetypes with indexation, RAB resets and DSCR lock-ups; ENR curve-driven DCF with RBL (ICE strip in production). Debt: capacity a·min(LTV, DSCR, debt yield) on each tranche's V^mat, terms keyed to f; gaps go to extension, forbearance, cure, sale or hand-back; a sponsor rollover hazard. Observation: RAME's two-component appraisal Kalman model, with τ as a lagged state; V\* drives risk, the kernel and pay, and V^A drives covenants and bids |
| **Liquidity and stress** | No HQLA; 30-day credit 0. Open-end: zero Tier-1 credit; φ at P5 in P from the engine of record (RE 26–34% within a year, 14% under T4′; infrastructure 43–67%, 31%); queue outputs are lower bounds on payouts (V-RE2). Closed-end and asset sales Red under T4′. 12-month SELL capacity $6.5 / 4.8 / 1.4 / 4.0bn (base / drought / T4′ / oil crisis). Reported marks show ≈32% of a T4′ loss after 12 months. θ\* 0.835 (U16) / 0.877 (U11); SH_TP 18 / 20 months. Cash row: drought −0.14 to −0.16; T4′ Tier-1 row at θ\* −2.50 / −4.49 (12 / 24 months, U16); structural −0.99 / −1.64 (−0.55 with structural calls). Look-through LTV under T4′ 45–51% on the actual debt path, 55% (P95 59.5%) with debt fixed. B_RA 4.26 / 4.03 (R1 / R0 plans, 24 months); L8 0.774 |
| **Forecasts and bias** | Plans → component corrections (exit cap, NOI growth, capex, hold, volume classes, deck re-strike, forward refinancing) → residual bias. Total priors b^u / b^f run from +1.0 / +0.75 (core infrastructure) to +6.0 / +3.5 (RE development), with late-cycle uplifts, as segment random-effect means. One κ_g (ln κ_g ~ N(ln 1.75, 0.25²)), with segment priors 1.67–2.22 as empirical-Bayes effects. Desmoothed common-shock control; scored on unsmoothed outcomes, never appraisals. Production engine FBE-R-RA with 50% shrink-to-equal fusion; GLS rejected; G-E binds (pay remedy first). IC figures on the listed-only nowcast grade until the τ lag test passes; DVA paid on V\* |
| **Synthetic defaults** | Ten sleeves, $18.0bn NAV, $4.0bn unfunded, $17.4bn look-through debt (49%), 115 positions; RE 9.0, infrastructure 6.5, ENR 2.5; open-end 26%, closed-end 37%, JV/direct/co-investment 37%. Sealed debt tape (198 tranches; 12.1% / 28.0% maturing within 12 / 24 months) and sealed closed-end vintage history. G₀ 2%; queues 10% / 5%; f₀ = N, e^RE₀ = D, Baa − 10y 1.44%, oil from the 15-Oct-2026 strip. `SYN-` ids and SYNTHETIC footers |

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Cap-rate loadings | β_y 0.45, β_s 0.50, κ_c 0.15 a quarter | G10 [I]; Chervachidze et al. [S] | Medium |
| Refinancing terms, f = N / T / C | LTV^max 62.5 / 57.5 / 52.5%; DSCR 1.25 / 1.35 / 1.40; availability 0.97 / 0.85 / 0.60; spread add-on +0 / 75 / 175bp | G14 [I]; CBRE Q2-26 [S]; ra_gap_02 | Medium |
| Financing window f | SLOOS CRE index, AR(1) with φ 0.79 plus crisis and rate-change terms; N / T / C below 20 / from 20 to 50 / from 50; today N | FRED 1991–2026 [S]; fit [I-calc] | Medium |
| Debt maturities | 12.1% / 28.0% of debt within 12 / 24 months; controllable 6.4% / 17.5% | Sealed tape [I-calc] on MBA, CBRE, CRED iQ [S] | Medium |
| Smoothing λ_agg | Engine: core RE 0.60, value-add RE 0.55, GCC RE 0.65 (G-ODCE); infrastructure 0.80–0.85; ENR 0.50 without a deck lag for fund NAVs (OIL-X2); +0.10 in downturns (V-RA1), joint recalibration pending | G13 [I]; Couts et al. [S]; ra_gap_02, ra_gap_04 | Medium |
| Open-end queue | r₀ 0.6% a quarter, b 0.12, w 0.08; start 10% (RE), 5% (infrastructure); markdown cancellations and Ĝ-driven requests to add; outputs are upper bounds on queues | G10 [I]; Accordant Q1-26 [S]; V-RE2 fails out of sample | Medium |
| LP pricing | RE 0.68 (crisis 0.45–0.50 [U/I]); infrastructure 0.91; ENR 0.40–0.70 in busts [U/I] | Jefferies H1-26 [S]; crisis levels drive only Red rows and crisis cards (§5) | High / Low |
| Infrastructure inflation duration | Regulated −13.2; PPP −23.1; fixed PPA +26.7; towers and data centres +23.3 per +1pp | G11 [I-calc] | Medium |
| Oil | L_eff 4.7% of NAV (canonical; 4.9–5.1% for later shocks); barrel price ≈$1.4–3.2 per bbl a year; H_j 0.1–2.9% of NAV a year (levered upstream funds 2.4–2.9%); Tier-1 backstop ≥ ≈170m bbl (Mix B); RA delta 11.2m bbl today | ra_gap_03 [I-calc]; G12 [I-MC] | Medium |

| Action | Economics and rule |
|---|---|
| **SELL** | By control cell: LP secondary, open-end redemption or unit sale (the better, never both), stake or asset sale, partial sell-down. SELL iff p^ce ≥ p\* on V\*, with lock-in, taxes, re-entry and the control premium; bids enter θ̂ only leave-one-out. A fund at 68% sells only if θ < ≈0.83 or ℓ > 5% before unfunded relief; with the buyer assuming the unfunded, the value-add LP card sells (reservation 0.666 / 0.574). ENR: the $0.6–0.8bn sale of fund-held levered upstream is NOT ESTABLISHED at 0.80. It waits for a new confirmatory sealed run on the canonical generator, and executes only at a live bid ≥ the confirmed p\* (exploratory 0.76 with nothing signed, 0.87 under Mix B) and ≥ θ̂ (Tier A). Intra-ADIC sales raise zero |
| **HOLD** | Continuation on V\* with fused beliefs, FTP_RA (2.0 / 20.5bp on scheduled flows), CLC for cures, the barrel price H_j and the transition charge; fund calls, never call default; cure iff V − D − ℓ̄S > max(0, V(1 − d) − D) under declared ϖ |
| **REFINANCE** | Controlled holdings only: cash-out at maturity (ŝ 3.2 / 4.4 / 7.2%), junior capital, ground lease or sale-leaseback (≥ 0.34 per $ of headroom; ≈0.47–0.73 on their terms), holdco debt, RBL in N/B/GW. Rule ŝ + f/T + λ_Lev + covenant + h/T < ℓ̄; never early while Λ > 0.5% of GAV; borrow only for needs shorter than T\* ≈ 2.4 / 6.7 / 9.2 years. The LP NAV facility is CF's and dominated |
| **LEVER** | Controlled holdings only: ADD and REFI, (1 − κ)c > i at P95 rates, covenants at T4′ values. Fails for core RE today; contracted infrastructure modest (≲ S+150bp at α\* 2.6%); ENR only hedged, never in a glut or bust |
| **HEDGE** | Rates: SPV caps via the Overlay; central residual at [ϖ + (1 − ϖ)N(d₂)] × floating share. Oil: asset-level where controlled; overlay residual at spot-equivalent delta, collateral on the boom-state tail; put spreads counted at spot-equivalent delta (1.6–3.1m bbl for 20–40m notional) |
| **PACE** | Plan ≈$1.2bn a year of closed-end commitments inside T4′'s $12bn. Optimizer envelope $1.8bn [1.5–2.1], ≈33 / 67 / 0, with the infrastructure cap binding. Hurdle on new commitments 13 / 144bp (R1 / R0); η > 0. 45 / 45 / 10 and controlled JV/direct are directions. No liquidity credit for two quarters. An RA pacing stop costs 0.150 per $ of headroom and cuts the Tier-1 24-month T4′ drain to −$3.62bn (G15 basis −$1.65bn) |

**Constraints** [I]: oil: H_j charged on every oil-linked holding, total-portfolio delta ≤ the Tier-1 backstop (≥ ≈170m bbl under Mix B), no rise in total delta while any Tier-1 gate is violated, RA delta ≤ today's 11.2m bbl (5.7m after any SELL); ENR ≤ 1.5% and GCC RE ≤ 1.0% of NAV; infrastructure ≥ 35% of RA; open-end ≤ 30% of RA and ADIC ≤ 10% of any open-end fund; closed-end value-add RE ≤ 2% of NAV; controllable debt: single asset ≤ 65% (70% contracted or regulated infrastructure; RBL ≤ 40% of deck PV), portfolio ≤ 45% target and 55% hard, ≤ 25% maturing in 12 months, unhedged floating ≤ 25% (origination and monitoring tests; the tape fails the 45% target, hedged-to-maturity and covenant-trigger tests today); development ≤ 10% of RE NAV with ≥ 50% pre-leasing; RA unfunded ≤ 30% of RA NAV; single asset ≤ 1% of NAV; no call default, no non-consented transfer or pledge, no card outside its control cell; intra-ADIC transfers raise zero.

*SYNTHETIC defaults throughout; none is ADIC data.*
