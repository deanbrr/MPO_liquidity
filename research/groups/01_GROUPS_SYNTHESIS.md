# ADIC Seven-Group Synthesis

## How PE, Secondaries, Capital Solutions, Co-investment, Public Markets, Private Credit and the Overlay plug into one total-portfolio, multi-period decision framework

**Date:** 2026-10-18 · **Version:** 1.1. It revises v1.0 of the same day: it folds in the four groups addenda (`research/groups/addenda/gap_01.md` to `gap_04.md`) and resolves the fifteen contradictions the critic found, plus six that surfaced while folding them in (§0) · **Companion to:** `research/00_SYNTHESIS.md` (the main report, v1.1) and its group-layer addendum `research/addenda/gap_01.md` · **Audience:** CIO, Investment Committee (IC), group heads, Corporate Finance, quant and data-science team · **Status:** design-grade synthesis. No ADIC data was used.

> **SYNTHETIC-DATA NOTICE.** Every ADIC balance, position count, cash flow, survival horizon and facility need in this report comes from the working allocation in context §1A, census v1.0, the proposed census v1.1 or design defaults. None of it is ADIC data, and none of it may be presented as ADIC data. Tables that carry [I-calc] figures end with *SYNTHETIC – NOT ADIC DATA*.

> **EIGHTH GROUP (patch, ra_gap_01, 2026-10-19).** ADIC has **eight** investment groups. Real Assets, added by the user after this report closed, is specified in `research/groups/02_REAL_ASSETS_SYNTHESIS.md`; its total-portfolio integration (θ\* recalibrated on the eight-group book, Real Assets FTP, CLC, L4 budget and envelopes, DVA on the nowcast V\*, the tenth Shapley player, gate V-RA-CTRL) is in `research/groups/addenda/ra_gap_01.md`, and the edit list in `research/groups/03_REAL_ASSETS_INTEGRATION.md`. Tables here are on the seven-group v1 book unless marked otherwise; for the eight-group v2 book ra_gap_01 governs. The shadow IC has 13 seats (§7.1) and attribution has ten players (§4.3).

---

## 0. Scope, inputs and relationship to the main report

**Scope.** The main report designs the engines: the scenario generator, the private-markets engine, the Forward Belief Engine (FBE), the liquidity kernel, the optimization core (H, P, F), the overlay, the owner-draw engine, the agentic lab and the IC Deliberation Module. This report does three things it does not:
- it specifies each of ADIC's seven investment groups as an implementable module (§3);
- it specifies the mechanisms that couple the groups (§4);
- it maps the groups onto forecast scoring (§5), synthetic data (§6) and the IC (§7).

It changes no main-report engine; where gap_01 has decided, gap_01 governs. Where a groups addendum has decided, it governs here. Groups gap_01 §5 drafts replacement text for the main report (finding 5, §2.3(d), §4.9, §6.2); that text is for the main report's owner and is not applied to it here.

**Inputs and verification.**

| Cluster | Streams | Claims checked (confirmed / corrected / refuted / unverifiable) |
|---|---|---|
| GC1, private groups | G1 PE, G2 Secondaries, G3 Capital Solutions, G4 Co-investment, G6 Private Credit | 156 (128 / 20 / 0 / 8) |
| GC2, liquidity, organization, data | G5 Public Markets, G7 liquidity ladder, G8 organizational economics, G9 synthetic data | 133 (117 / 12 / 0 / 4) |
| **Total** | 9 streams | **289 (245 / 32 / 0 / 12)** |

All nine streams rate HIGH on evidence and MEDIUM on design; no claim was refuted and no citation was hallucinated. Only corrected values appear here, tagged [C], and unverifiable items are never load-bearing. The corrections that changed group design: a PE pacing cut is not a "10.5–11% financing rate"; tail-end θ is 0.78–0.83; Capital Solutions break-evens are not r_f-discounted; co-investment bids come from a buyer model; Form PF measures notice capacity, not cash; the private-credit run-off uplift is ≈$0.8–0.9bn, not $2.2bn; ADIC-LCR(30d) is 2.10×, not 4.5× (1.91× on CF-controlled assets); transfer prices have no floor; vintage α is −0.05 a year, not −0.5.

Groups gap_03 adds a tenth, G-stream-equivalent dossier for the Overlay ("G10, Overlay organization") with its own adversarial log. Of its 12 checks, 8 were confirmed and 1 corrected. Two v1.0 claims were refuted: that a ≈$25bn tail stack fits the 0.15% floor, and that a 1.5%-of-NAV opportunistic stress loss is admissible. One check (the Consensus literature sweep) could not run.

**Groups addenda folded in (v1.1).** Each is integrated into the sections named, not appended.

| Addendum | Content | Sections |
|---|---|---|
| Groups gap_01 | Re-bases the group layer on T4′ = s\*(0.76) with gap_02's conventions; adds a group RECOVERY mode (Phase I over group-tagged levers, glide path, Phase-II prices, t0 table with `priced_on` flags) and a reconciled IC decision list | §1, §2.2–2.4, §4.3–4.4, §4.8, §7, §9 |
| Groups gap_02 | Proposes census v1.1 (PE unfunded $27.4bn → $16.4bn, a sealed vintage history); re-runs the cash map, ladders, PACE and co-investment flow; adds a misspecification ensemble with pre-registered gates, a deterministic O3 module, one κ, and an overlap graph with gate V24 | §1, §2.2–2.4, §3.1, §4.7, §5, §6 |
| Groups gap_03 | Puts the Overlay at parity with the other groups (S/H/R/L by book), sets a services transfer-pricing convention, ex-ante tail DVA and pay, and one reconciled sizing | §2.2, §3.7, §3.8, §4.3, §6, §7 |
| Groups gap_04 | Simulates the seven groups, CF and the overlay jointly; measures trigger frequencies and the value of contingent budgets; derives envelopes and FTP from a reduced H; computes nine-player Shapley values; reprices gap_02's mixes with the group PACE cost | §1, §2.4, §3.1–3.4, §4.3–4.7, §4.9 |

**Reconciliations made here.**

| # | Issue | Decision |
|---|---|---|
| R1 | Private-credit PD/LGD split. GC2: PD 1.8% with LGD 0.40. GC1: 1.5% with 50% recovery. gap_01: LGD 0.67 with PD_N 1.1% | The FBE and Tier 1 use the severity-anchored pair (gap_01). GC1's pair is a truth variant. GC2's pair is retired (§3.6) |
| R2 | Census and unfunded split (G7, G9 and GC2 differ) | Census v1.0 is the working census until the user confirms census v1.1 (groups gap_02), which seals PE unfunded at $16.4bn. Results that change are shown on both (§2.2, §2.4, §3.1, §4.7, §6). gap_01's G7-split table is kept as a reproduction check (§2.2) |
| R3 | Hedge-fund liquidity: static buckets vs the state machine | The state machine's φ is the engine of record. Static buckets bracket it. ADIC's terms τ decide |
| R4 | Shadow-IC seats: 7 (main v1.0 §6.2) vs 12 (gap_01) | gap_01's 12 seats, defined by mandate, with no personality personas (§7). Main v1.1 §6.2 now adopts the same twelve seats |
| R5 | GC1's requests to GC2 | Adopted: PC smoothing 0.5–0.7; a BJS-anchored co-investment generator; an SMA loan-sale rung; a protected core sleeve; Secondaries' stress calls ≥ 1.0× |
| R6 | Numbering of the Tier-1 rows | The main report's numbering, with C1's in brackets: T3 (T1.3) 30-day coverage; T4′ (T1.4) the 24-month canonical stress s\*(θ\*), with literal T4 a reverse stress; T5 (T1.5) structural limits; T6 (T1.6) red event |

**Contradictions resolved in v1.1.** C1–C15 are the critic's; C16–C21 surfaced while folding in the addenda.

| # | Contradiction | Resolution | Where |
|---|---|---|---|
| C1 | IC ask: scope an LP-portfolio NAV facility vs gap_02's "drop the NAV-facility route" | Request $10–15bn of committed unsecured revolver indications; drop the NAV facility as a liquidity lever. A 20% pledge cap supports $2.1bn, of which $1.1bn is credited, at ≈6× the revolver's cost per credited $ (groups gap_01 §4) | §1, §2.3, §3.1, §9 |
| C2 | "No policy meets the ≤ 1% red-event gate" vs gap_02's certified mixes | Mixes A and B certify ≤ 1% in M1–M5 (one-sided CP bounds 0.98% and 0.79%). Only the M6 class fails: 2.4% with the band, 5.2–5.8% without, against its 5% capacity | §2.4 |
| C3 | Literal T4 kept in decision 1, the CFP indicator and the §2.2 column | T4′ = s\*(θ\* = 0.76) everywhere; literal T4, T4 as written and the critic reading are reverse stresses (groups gap_01 §1) | §1, §2.2, §2.4, §3 |
| C4 | Facility need: $3–19bn (main v1.0) vs $23–49bn (group v1.0) vs gap_02 | One figure: $13.9bn under T4′ ($14.6bn at the pooled θ\* of 0.79), $6.1bn with the pacing rule, $0 with the band. All are inside T5's $26.6bn hard debt limit. Literal-T4 readings need $32.2–91.7bn, above that limit, which is why they are reverse stresses | §1, §2.4 |
| C5 | "KKT caps duals at buffer carry" vs penalty-pinned duals at an infeasible t0 | The cap holds only for a restorable row, and then at the cheapest spare lever. The book fails T4′ by $11.3bn at t0, so prices come only from the Phase-II restored problem, with `priced_on` flags | §4.3, §4.8 |
| C6 | PE baseline: U/NAV 0.53, an 11% rate with a $7.2bn pace, and a $5.1bn PACE pace | One vintage-resolved PE leg (RFT-TA v2) for the cash map, PACE and co-investment flow. Proposed census v1.1: U $16.4bn, U/NAV 0.32, pace $5.34bn, H1-2026 rates 9.0% / 29.0%. v1.0's combination comes from no commitment history and is kept as a reproduction check only | §1, §2.2, §3.1, §4.7, §6 |
| C7 | η < 0 and "monetization funds contingent budgets", but the gate blocks deployment in Red | The gate is redesigned: confirmed d̂ > 20% ∧ Tier 1 green, in any stage but Black; sized to T4′ headroom; funded from general liquidity. On the do-nothing book Tier 1, not the stage, switches it off. Tail cash is supplementary and never ring-fenced (groups gap_04 §4) | §1, §3.2, §4.4–4.6 |
| C8 | Overlay sizing: $20bn at 0.4%, a 0.15% floor, a ≈$25bn stack; beta $0–10bn vs $10bn / $15bn | One sizing: the 0.15% floor ($0.27bn) buys $7.1bn of a 90/72 ladder; $10bn of TPA completion beta at t0 and in stress; a +$5bn P2S is a Public Markets Red lever booked with its proceeds; the ≈$25bn stack is a test fixture (groups gap_03 §5) | §2.2, §3.7 |
| C9 | Exact Shapley over 9 players vs main §4.11 (exact only over ≤ 6) | Exact over all 512 coalitions when each is a policy simulation on common random numbers; when coalitions need H re-solves, main §4.11 applies (antithetic sampling, P ≥ 32, with path and permutation errors) | §4.3 |
| C10 | "A group that follows its prices cannot hurt the total portfolio" | Restated: price-following reproduces x\* inside envelopes only by construction (G8 R14). A price-only rule did $24.7m worse in main §4.4's 40-asset test, so the split marginal assets go to the IC | §1 |
| C11 | gap_02 cites G1's "≈10.5–11% implied financing rate" | Withdrawn; it should be struck from gap_02 §2.1. Pacing cuts are priced by c^PACE in kernel currency (groups gap_04 §7) | §1, §2.3, §3.1 |
| C12 | ADIC-LCR(30d) "adequate" at 2.10× | L1 is defined on CF-controlled HQLA: 1.91×, which is Amber. 2.10× counts assets outside CF's operational control. Main v1.1 §4.9 (T3, LR1) still shows 2.10×; flagged for its owner | §1, §2.4 |
| C13 | Seven seats (main) vs twelve (group) | Main v1.1 §6.2 has adopted the twelve mandate seats, with ≥ 3 model families and 4 the target. Groups gap_01 adds recovery-mode evidence slices | §7.1 |
| C14 | κ (median 1.75, a widening factor) vs κ_conf (0.45–0.7, stated ÷ true SD) | One κ_g = w₈₀(true) ÷ w₈₀(stated) ≥ 1; κ_conf = 1/κ is retired (groups gap_02 §5) | §5, §6 |
| C15 | Treasury ÷ NAV ≥ 8% shown as Green at t0 | The indicator becomes usable IG + cash net of encumbered IM: 7.7% at t0 (Amber), 8.0% after a $0.56bn top-up | §2.4 |
| C16 | Groups gap_01's t0 stage table shows 30-day coverage as Green at 2.10× | Corrected to 1.91×, Amber (C12) | §2.4 |
| C17 | Groups gap_02's restated finding 9 calls the pause's 9.8% implied IRR a financing cost | It is RFT-TA v2's NAV growth path restated (G1 verifier R1's telescoping result). Shown as an IRR only; pricing uses c^PACE (C11) | §1, §3.1 |
| C18 | Groups gap_01's T4′ overlay line (−$2.94bn) uses the canonical overlay conventions that groups gap_03 rejects: a ladder paying $4.05bn, and a 1.5%-of-NAV opportunistic loss that breaches L2 | At the reconciled floor the 12-month T4′ overlay use is ≈$0.9bn larger (≈−$3.9bn) [I, component substitution, not an engine run]. Re-run t1_engine with the reconciled overlay convention (open item) | §2.2 |
| C19 | Groups gap_04's PE cohort engine reaches $27.4bn with 12.6% a year commitment growth, a history that fails V6's contribution half | Its PE fans, trigger frequencies and Shapley shares are on census v1.0 and are re-run on the confirmed census (open item) | §4.9 |
| C20 | Groups gap_03 makes the opportunistic book a mandatory SELL "at Red"; groups gap_01 prices its IM release as the dearest Phase-I lever, unused at t0 | Mandatory at event-Red only. At readiness-Red it is a priced lever (69% PV per $ of headroom) | §2.4, §3.7 |
| C21 | Groups gap_02's restated finding 3 quotes literal T4 on census v1.1 ($12.2bn), now a reverse stress; T4′ on v1.1 is not computed | Finding 3 reports T4′ on census v1.0 and the literal-T4 reverse stress on v1.1, each labelled | §1, §2.2 |

**New computation.** `research/groups/addenda/GS_calcs/gs_group_cashmap.py` (project venv, `python -I`) writes `gs_group_cashmap_results.json`. It loads the unmodified stream-G7 ladder module, as GC2 does; reproduces gap_01's group table to within $0.01bn; and computes the census v1.0 cash map (§2.2), the private-credit loss of four PD/LGD pairs (§3.6) and the co-investment flow arithmetic (§4.7). The groups addenda add, all in `research/groups/addenda/`:
- `gap_01_calcs/`: `g01_core.py`, a group-resolved replica of gap_02's `t1_engine.ladder`. `g01_verify_replica.py` asserts exact reproduction on six readings × eight policies. `g01_run.py` writes `g01_results.json`. `test_no_pinned_duals_groups.py` passes 18/18, and gap_02's own test still passes 8/8.
- `gap_02_calcs/`: nine scripts with `*_results.json` (`python -I -B`): the RFT-TA v2 book, the history search and LP bounds, the seal (`sealed_pe_history_v1_1.csv`), the re-runs, the misspecification prototype, `perf_module.py` and `overlap_graph.py`. The re-runs first reproduce the GS, GC2 and gap_01 numbers exactly.
- `gap_03_calcs/gap03g_overlay_calcs.py` → `gap03g_overlay_results.json`. It reuses the unmodified stream-G7 module and the GS results, and reads Cboe index files to 16 Oct 2026 and the Fama–French T-bill series.
- `gap_04_calcs/`: `g04_engine.py`, which imports gap_02's `t1_engine.py` unmodified and reproduces it path for path in compatibility mode; `g04_run.py` (stages `bridge`, `main`, `rh`, `shapley`, `pace`); 10,000 paths per model and policy, M1–M6, fixed seeds.

All outputs are SYNTHETIC. **Research note:** the Consensus searches requested for all four addenda could not run, because the account's monthly quota of 500 searches was exhausted (it resets on 1 November 2026). Sources were verified on publisher, repository and press pages instead, and Consensus records already verified in the corpus were reused. Re-run the sweeps after 1 November.

**Conventions.**
- *Tags:* [S] sourced and verifier-confirmed; [C] corrected; [P] practitioner consensus; [I] inference or default; [I-calc] synthetic arithmetic; [A] client statement or working assumption; [U] unverifiable.
- *Corporate Finance (CF)* owns Treasury, the liquidity pool, facilities, VM/IM collateral, owner distributions, the contingency funding plan (CFP) and the funds-transfer-pricing (FTP) curve.
- *Symbols:* ℓ is the liquidity premium from the optimizer's duals; π is the C2 deflator; LAPV is liquidity-adjusted present value.
- *Regimes:* exit regimes O/N/D/F (open, normal, drought, frozen); macro regimes EXP/LATE/CRIS/RECV.
- *Naming:* "Group 7 (Overlay)" is the investment group; "stream G7" is the liquidity research stream.
- *Addenda:* an unqualified "gap_0x" is a main-report addendum in `research/addenda/` (gap_01, the group layer; gap_02, Tier-1 feasibility, T4′ and recovery mode; gap_03, the overlay's position layer). The groups addenda in `research/groups/addenda/` are cited as "groups gap_01" to "groups gap_04".
- *Stresses:* T4′ = s\*(θ\*) is the canonical 24-month Tier-1 stress (θ\* = 0.76; gap_02 §1.1 conventions). "Literal T4" (θ = 1), "T4 as written" and the critic reading are reverse stresses. S1 is G7's demand bust.
- *Census:* v1.0 is the working census of context §1A. v1.1 is the proposed revision (groups gap_02), pending the user's confirmation.
- *CFP stage:* *readiness-Red* means only the forward-looking survival indicator is Red; *event-Red* means a current indicator is Red (§2.4).

---

## 1. Executive summary

ADIC's seven groups are best modelled as an **internal capital market** competing for one scarce resource: unencumbered liquidity, which Corporate Finance owns and prices. The framework keeps every decision at total-portfolio level and uses the groups for what only they can do: source, underwrite, forecast and execute.
- **Groups are price-takers inside quantity envelopes.**
- **Envelopes and prices both come from the same optimizer, and a group that wants more capacity pays the shadow price for it.**
  - Inside its envelope, a group that follows its prices reproduces the optimizer's choice, but only by construction. That is a consistency check, not evidence of decentralization in practice, because α and q are private and CVaR is not linear (G8 R14).
  - Prices alone are not enough. In main §4.4's 40-asset test, three prices reproduced 36 of 40 exact decisions, yet a price-only rule did $24.7m worse. The assets the LP relaxation splits, at most one per binding row, go to the IC as its marginal-asset agenda.
- **Prices exist only for a feasible problem.** The synthetic book fails the T4′ hard row by $11.3bn at t0. Every envelope, FTP charge and hurdle therefore comes from the Phase-II restored problem and carries a `priced_on` flag (§4.8).

**Eleven findings**

1. **Seven groups, three private engines, one kernel.**
   - *Fund interests* run on RFT-TA v2: PE funds, secondary funds and closed-end credit funds.
   - *Single companies* run on one enterprise-value engine, with one draw per company per path: co-investments, continuation-vehicle (CV) stakes, Capital Solutions equity kickers and PE look-through.
   - *Contractual claims* run on one competing-risks credit engine: Capital Solutions debt and preferred equity, and private-credit loans.
   - Public Markets adds a factor model with a liquidity-term state machine. The Overlay uses the main report's position and collateral layer.
   - Every action is scored with the same deflator; group P&L is attribution only.
2. **Control rights define which actions exist.** GPs trigger CV elections and recaps and decide closed-end recycling; delayed-draw funding is contractual; transfers and pledges need GP consent; portfolio facilities belong to CF. Every action carries a feasibility flag, a consent probability and a lead time, and gate V23 rejects instruments an LP cannot access.
3. **The drought book's sign depends on PE vintage structure. It is positive for every history that passes V6, because four non-PE groups carry PE.**
   - On the proposed census v1.1 (PE unfunded $16.4bn, pace $5.3bn) the private book nets **+$3.7bn** over 12 months. PE contributes −$0.9bn (distributions $4.6bn, 8.9% of NAV; calls $5.5bn), against +$4.5bn from the other four groups [I-calc].
   - Across truth variants it nets +$5.3bn (mature) to +$2.6bn (10% then flat). It turns negative only for histories that fail V6: −$0.1bn for the history that reproduces v1.0's $27.4bn (which needs a $13.9bn pace), and −$3.0bn for 20% growth.
   - v1.0's +$2.2bn paired U = $27.4bn with a $7.2bn pace and a flat 11% rate. No commitment history produces that combination.
   - A 7.5% payout draws $9.6bn, 14% of the $71bn liquid book (v1.0: $11.1bn, 16%).
   - Under T4′ (census v1.0, canonical conventions) the private book consumes $16.4bn in year 1, 70% of it PE. No private group is a net cash source, and the overlay adds $2.9bn of net use. At canonical draws the liquid book funds $37.2bn in 12 months, 52% of itself [I-calc].
   - On census v1.1 the literal-T4 reverse stress falls from $18.4bn to $12.2bn of private drain. T4′ on v1.1 is not yet computed.
4. **No private group hedges the drought's cash channel, and the franchise hedge needs committed liquidity.**
   - Capital Solutions and private-credit cash move *with* PE distributions: NAV loans repay from distributions, and preferreds switch to PIK.
   - The only natural DPI that ADIC can switch on is the private-credit SMA run-off, worth ≈$0.8–0.9bn in year 1 [C].
   - Secondaries and Capital Solutions hedge opportunity, not liquidity. Their budgets are ℓ-conditional, never fixed, and sit behind a deployment gate.
   - On the do-nothing book that gate fires in 0.1–1.2% of quarters. Tier 1 switches it off (T4′ survival with facilities is below 24 months), not the CFP stage [I-calc].
   - With Mix A's revolver or Mix B's band it fires in 71–87% of paths and adds $0.2–0.8bn of five-year wealth: 15–22¢ per dollar deployed at θ = 0.92, 0.5–9¢ at θ = 0.75. Tail cash ($1.5–1.8bn per crisis path) cannot fund the budget, and ring-fencing it raises P(red) [I-calc].
5. **Public Markets is the reservoir, and it fails where liquidity is dearest.**
   - Long-only is market liquidity, settling at T+1/T+2.
   - Hedge funds are contractual liquidity. About $4.9bn of cash arrives within 90 days, not $7.1bn, and ≈42% of NAV sits beyond a year [I-calc].
   - Physical-to-synthetic replacement (P2S) is the cheapest non-cash liquidity in normal regimes, at 0.40–0.70% a year per $ freed. In a crash it becomes a VM liability: $1.65bn on a $5bn conversion in a −33% month.
6. **Thirty-day coverage is Amber on Corporate Finance's own basis. The canonical 24-month stress fails without committed liquidity, and the mandate clears it.**
   - ADIC-LCR(30d) is 1.91× on CF-controlled, Basel-capped HQLA, the basis L1 defines: Amber. The 2.10× figure counts assets outside CF's operational control [C].
   - Under T4′ = s\*(0.76) the do-nothing book survives 17 months on Treasury + Public Markets (18 on census v1.0's split). The stage-triggered pacing rule lifts this to 20 months, the owner band to 29 [I-calc].
   - Clearing 24 months needs $13.9bn of committed facilities ($14.6bn at the pooled θ\* of 0.79), $6.1bn with the pacing rule and none with the band, all inside T5's $26.6bn hard debt limit. Literal T4 and the other readings need $32.2–91.7bn, above that limit, so they are reverse stresses [I-calc].
   - Group levers alone can restore T4′ (Phase I u\* = 0, with no fire sales). They price month-24 headroom at 24% PV per dollar with SMA and Capital Solutions sales admitted, and 69% without. A signed revolver cuts the price to 1.1%. It also turns the PE and Secondaries t0 cards from SELL to HOLD and shrinks Private Credit's SMA sale from $5.6bn to $0.58bn (§4.8).
   - The book fails the hard row by $11.3bn today, so it is in *execution* recovery, priced on the restored problem. The stage is readiness-Red on survival alone; the current indicators are Amber, including usable IG + cash at 7.7% of NAV, $0.56bn short of 8% [I-calc].
   - The red-event gate is reachable: Mixes A and B certify ≤ 1% in M1–M5, and only the stressed M6 class fails. On census v1.1 every T4′ figure must be recomputed; the literal-T4 need at G7 conventions roughly halves at the fixed-USD draw, from $40–41bn to $19.5–21bn.
   - In nine-player Shapley values, CF and Public Markets each remove 26–30% of red-event risk at little or negative CE. The overlay playbook and TPA's beta rule earn 69–89% of the CE gain [I-calc].
7. **Discounts are not value, and in-house quotes are evidence, not prices.** Tail-end θ is ≈0.78–0.83, so tail discounts mostly pay for overstated NAV; an average co-investment bids at 71–79% of NAV in normal markets and 56–65% in a drought [C]. The Secondaries desk publishes scored forecasts of external clearing prices but never quotes where it may bid; Capital Solutions' quote is a reserve price behind third-party RFQs. Transfers between groups raise zero liquidity.
8. **Asset-level leverage rarely survives losses, PIK and path-wise covenants** [C].
   - A 12% holdco PIK on a co-investment adds no return and lifts drought wipe-out at exit from 7.0% to 22.8% (7.6% → 22.9% if the G4 dossier's default barrier V ≤ 0.75D applies at any time).
   - Single-asset NAV facilities breach a 1.5× LTV trigger on 50–63% of quarterly-tested paths (62–73% if LTV were monitored continuously).
   - Both rates stand after the Broadie–Glasserman–Kou sign correction. The wipe-out is measured at exit and the covenant is tested quarterly, so the correction does not apply to either (`research/groups/addenda/G4_barrier_rerun/RESULTS.md` §5) [re-checked 2026-10-18].
   - Alternative-lender back-leverage cuts Capital Solutions' loss-adjusted RoE to 8.9%, from 9.25% unlevered.

   LEVER belongs to the liquid book, the overlay and senior non-software SMA credit in benign states.
9. **PE pacing is the slowest big lever, it is priced in kernel currency, and co-investment rides on it.**
   - On the sealed v1.1 pace, a one-year pause in 2027 returns $0.7bn in year 1 and $3.5bn by 2030 (66% of the amount forgone), then costs $4.4bn over 2027–40 [I-calc].
   - Its cost is c^PACE ≈ 8.6¢ per PE dollar forgone in M1 (net α\* 1.35¢, κ^GP 5.12¢ at its upper bound, lost co-investment flow 2.12¢), and 5.6–12.3¢ across models. The pause's 9.8% "implied IRR" and G1's 10.5–11% are the engine's NAV growth restated, never financing rates [C; I-calc].
   - Repriced this way, gap_02's 1% gate costs 11–21bp of NAV a year in CE terms (it was 8bp); Mix A's premium is 66–76bp and Mix B's 23–29bp. The ranking stands. The CE-best policy *without* gates drops the stage-triggered cut, so the cut is bought for Tier 1, not for return [I-calc].
   - Co-investment flow from lagged commitments is $0.6–1.2bn a year ($0.4–1.0bn after a pause), against ≈$3bn needed to sustain an $18bn book. Sustaining it would take a PE pace of $15–30bn a year, which no V6-compliant history supports. Sourcing must extend beyond ADIC's fund GPs, which the offer log will show, or the book shrinks [I-calc].
10. **One forecast registry, one bias model, one precision weight, and a presentation that survives politics.**
    - Groups file P10/P50/P90 forecasts in a bitemporal registry scored by the weighted interval score (WIS).
    - Group bias enters the FBE once.
    - One overconfidence parameter, κ_g ≥ 1 (true ÷ stated 80% width; prior median 1.75), replaces κ and κ_conf.
    - The estimator is tested on generators it does not assume, against pre-registered gates. A production-style FBE fails four gates. A robust FBE fails only when forecasters face status-quo pay, so pay design is a precondition for deployment [I-calc].
    - Credibility is shown only against each group's own reference class, and only when n_eff ≥ 20. It is never shown as a league table, and sandbagging is penalized like optimism.
    - Pay is linear in dollar value added (b ≤ 0.005, s ≥ 50), and nothing scales with budget.
11. **The Overlay is a service group with an IC-owned tail budget.**
    - At the 0.15% floor ($0.27bn a year) the budget buys $7.1bn of a 90/72 put-spread ladder, which costs 3.74% of notional a year on 16 Oct 2026 prices. It pays ≈$1.2bn in S1; the 0.5% cap buys $23.6bn [I-calc].
    - Services book exposure and the liquidity charge to the client, execution and basis to the Overlay, and funding to CF. The ledgers net to zero on 2,000 paths, where the naive booking double counts −$7.05bn in S1.
    - Tail value is credited ex ante (kernel, liquidity and enabling value of ≈0.62–0.64 per dollar of premium). That leaves a predictable IC policy residual of ≈−$96m a year at the floor. Ex-post crediting would have shown negative DVA in 11 of 16 years over 2010–25 [I-calc].
    - Reconciled, the overlay's stress use falls from $6.0bn to $4.0bn.

**Decisions for the IC this quarter** (reconciled with groups gap_01 §4).
1. **Ratify T4′ = s\*(θ\*).**
   - Ratify the calibration rule: the worst model's P99.6 on pooled SAA replications (θ\* 0.76 canonical; 0.79 pooled), with the canonical conventions as hashed fields.
   - Literal T4 becomes a reverse stress, a Board item only if SH_TPF < 24 months.
   - Settle the opening-reset draw convention.
   - Open the band conversation with the owner. The band is needed for the M6-class T6 capacity row, not for T4′.
2. **Request revolver indications; drop the NAV facility.**
   - Request indications for $10–15bn of committed unsecured revolving capacity: 3 + 2 years; at least 10 banks, none above 12.5%; covenants tested under s\*; a yearly test draw; at least $6.1bn firm.
   - The precedents support the floor more than the top: PIF's $15bn (August 2024, 23 banks), Mubadala's $2bn (2019, 28 arrangers) and Danantara's reported $1bn (2025).
   - The NAV facility is not a liquidity lever: pledge-capped at $2.1bn, it relieves T4′ by $1.0bn at ≈6× the revolver's cost per credited dollar, and it forces paydowns in the stress.
3. **Adopt the stage-triggered pacing rule now.**
   - It moves SH_TP from 17 to 20 months and the facility need from $13.9bn to $6.1bn.
   - Set the PE corridor and its protected core sleeve.
   - Publish group envelopes, FTP and hurdles from Phase II with `priced_on` flags, at tolerance and at appetite.
   - Until the revolver signs, run the Q1 glide path: the co-investment pause and PC run-off.
4. **Confirm census v1.1 or supply PE commitments by vintage.** This is decisive: T4′, θ\*, the facility need and every envelope are then re-run on the confirmed census.
5. **Hold the tail budget at the 0.15% floor**, in a listed-first $7.1bn ladder. Credit it ex ante against a reference ladder, and adopt the services transfer-pricing convention, with V2 run on DVA ledgers.
6. **Adopt the redesigned contingent-budget gate:** a confirmed discount above 20% ∧ Tier 1 green, in any stage but Black; sized to T4′ headroom; funded from general liquidity, with tail cash never ring-fenced.
7. **Make the pay remedy a precondition for forecast precision.** Set b ≤ 0.005 and s ≥ 50, with nothing scaling with budget. Freeze and hash the misspecification gates before the first scored release.
8. **Data requests:** hedge-fund terms (τ) per lot; private-credit wrapper rights, including SMA sale and run-off rights (the cheapest group levers in recovery); look-through company and sponsor IDs; PC loan tapes with sponsor IDs; co-investment offer logs; CSA terms and sovereign IM status.
9. **Unchanged:** start a point-in-time forecast archive in every group, including declined deals; confirm the boundaries between Capital Solutions, Private Credit and Secondaries.

---

## 2. ADIC as an internal capital market of seven groups

### 2.1 Total-portfolio view versus group view

| Layer | Owner | Decides | Priced or bounded by |
|---|---|---|---|
| Total portfolio | IC / Total Portfolio Committee. The TPA desk runs H, P and F | Accepted actions, group envelopes, decision prices, Tier-1 status | Tier 1, the robust floor, objective J |
| Funding and liabilities | Corporate Finance (Treasurer) | Facilities, repo, term debt, VM/IM collateral, payout timing, CFP stage, FTP publication | Liquidity duals λ, published as the FTP curve |
| Assets | The seven groups | Sourcing, selection, execution, forecasts; asset-level SELL / HOLD / REFINANCE / LEVER and PACE proposals | Envelopes Λ_g, decision prices, consent rights |
| Validation | CRO office | Forecast registry, scoring, model validation, transfer-pricing committee | — |

**Three rules hold the structure together.**
1. **Liquidity raised means external cash only.** A Secondaries purchase of a PE-group stake is a relabelling that raises nothing.
2. **One kernel prices every proposal.** Group P&L is attribution, never a decision criterion.
3. **Groups are price-takers inside quantity envelopes.**
   - Prices alone may fail to decentralize: "in many cases there exist no prices which will lead divisions to make independent decisions that are optimal" [S: Baumol–Fabian 1964].
   - Pairing prices with envelopes is our inference [C].
   - Divisional rent-seeking (Scharfstein & Stein 2000) is why a group cannot win capacity by lobbying, only by paying the dual.

**What the group layer adds:** feasible actions (instruments and control rights), group forecasts and their biases, market intelligence (Secondaries for SELL, Capital Solutions for REFINANCE) and accountability.

### 2.2 Cash-generation map by group

**Assumptions** ([I] unless tagged; first 12 months). Normal, Drought and S1 use the stream-G7 engine with monthly steps. T4′ uses gap_02's canonical conventions on groups gap_01's group-resolved replica of `t1_engine.ladder`.

| Input | Normal | Drought (today) | S1 demand bust | T4′ = s\*(0.76), canonical |
|---|---|---|---|---|
| Exit regime | Normal | Drought | Crisis for 18 months | Crisis for 23 months |
| Distributions, % of NAV a year: PE / Secondaries / Co-investment / Capital Solutions / Private Credit | 20 / 25 / 19.3 / 13 / 17 | 11 / 18 / 12.4 / 12 / 16 | 3.5 / 7 / 2.5 / 7 / 10 | PE, Secondaries, Co-investment at 10.8% of drought rates / 7 / 10 |
| Calls, % of unfunded a year | 29 | 28 | 30 × 1.25 | 28 × 1.38 |
| Market path | Benign | Benign | Equity −39% over 6 months | Equity −37.6% at the vertex (t0) |
| Owner draw | Payout rates shown | Payout rates shown | Payout rates shown | 10% of opening fiscal-year NAV ($17.7bn in year 1) |

- **Rates.** PE rates are anchored on MSCI (distributions 17–24% in 2017–20 and 9–11% in 2022–25; calls 27–31% [S]). Secondaries distribute faster, reflecting secondary funds' ≈65% NAV peak vs ≈95% for primaries [S: Callan]. Capital Solutions and Private Credit carry contractual yields; co-investment yields are GC1's G4-engine values [I-calc].
- **Flows.** Unfunded follows census v1.0; new commitments run at $12bn a year, split 60/10/10/10/10 (PE, Secondaries, Private Credit, Capital Solutions, Co-investment). In S1, half of private credit's undrawn DDTL/revolver lines are drawn within three months. T4′ runs on gap_02's unfunded split; census v1.0 moves G\* from $11.12bn to $10.85bn and SH_TP from 17 to 18 months.
- **Overlay (reconciled, groups gap_03 §5).** $10bn of TPA completion beta in every column (economic exposure ≈0.97×), with IM rising from 4% to 10%. A $7.1bn 90/72 put-spread ladder at the 0.15% floor ($0.27bn a year, listed first) pays $1.18bn in S1. Opportunistic IM is $1.0bn; its stress loss is capped by L2 at $0.29bn, plus a $0.5bn cleared-IM step. A +$5bn P2S in S1 is a Red lever booked to Public Markets *with* its proceeds, not to the Overlay.
- **T4′ overlay (canonical, unreconciled).** The T4′ column keeps gap_02's canonical overlay conventions: $10bn of beta, tail monetization of $4.05bn by month 6, and an opportunistic loss of 1.5% of NAV (C18).

**Results** ($bn, first 12 months unless stated).

| Group | NAV | Unfunded (v1.0) | Normal: distributions / calls / **net** | Drought: distributions / calls / **net** | S1: **net** | T4′: distributions / calls / **net** | T4′: net, 24 months |
|---|---|---|---|---|---|---|---|
| PE funds | 52 | 27.4 | 11.6 / 9.0 / **+2.6** | 6.3 / 8.7 / **−2.3** | **−9.8** | 0.56 / 11.97 / **−11.4** | −20.9 |
| Secondaries | 14 | 3.9 | 3.8 / 1.6 / **+2.2** | 2.7 / 1.5 / **+1.2** | **−1.0** | 0.18 / 2.66 / **−2.5** | −3.5 |
| Co-investment | 18 | 1.5 | 3.6 / 0.6 / **+3.0** | 2.3 / 0.6 / **+1.7** | **−0.4** | 0.16 / 1.78 / **−1.6** | −3.0 |
| Capital Solutions | 8 | 1.2 | 1.1 / 0.5 / **+0.6** | 1.0 / 0.5 / **+0.5** | **−0.2** | 0.52 / 0.69 / **−0.2** | −0.5 |
| Private Credit | 14 | 4.0 | 2.6 / 1.3 / **+1.2** | 2.4 / 1.3 / **+1.1** | **−0.6** | 1.31 / 2.03 / **−0.7** | −0.8 |
| **Private book** | **106** | **38.0** | 22.6 / 13.0 / **+9.6** | 14.8 / 12.6 / **+2.2** | **−12.0** | 2.72 / 19.14 / **−16.4** | −28.7 |
| Public Markets (hedge funds 20, long-only 36) | 56 | — | 0 | 0 | 0 | 0 | 0 |
| Overlay, net (services / own books) | notional | — | +0.31 (+0.58 / −0.27) | +0.31 (+0.58 / −0.27) | −4.00 (−4.12 / +0.12) | −2.94, canonical (≈−3.9 reconciled [I]) | −1.32 |
| CF opex | — | — | −0.2 | −0.2 | −0.2 | −0.2 | −0.4 |
| **Before payout** | | | **+9.75** | **+2.37** | **−16.16** | **−19.54** | |
| Liquid-book funding at a 5 / 7.5 / 10% payout | | | −0.9 / 3.5 / 8.0 | 6.5 / 10.9 / 15.3 | 25.0 / 29.4 / 33.9 | 28.4 / 32.8 / 37.2 | |
| Share of the $71bn liquid book | | | −1 / 5 / 11% | 9 / 15 / 22% | 35 / 41 / 48% | 40 / 46 / 52% | |

*SYNTHETIC – NOT ADIC DATA.* Public Markets' returns stay in NAV: it generates no free cash and is the payout's reservoir. The script reproduces gap_01's G7-split table (drought +$0.86bn, PE −$1.95bn; S1 −$12.76bn). T4′ overlay detail: VM −3.76, ΔIM −0.22, tail monetization +4.05, premium −0.35, opportunistic −2.66.

**Reverse-stress library.** v1.0's literal-T4 column (G7 conventions: distributions zero, calls ×1.5) is retired from the cash map. On census v1.0 it gave a private book of −$18.4bn (PE −$14.0bn), an overlay of −$6.0bn as published (−$4.0bn reconciled) and −$24.6bn before payout.

**Census v1.1 (proposed): the vintage-resolved PE leg** (groups gap_02, Table 2). Only the PE leg changes; every other group is as above, and the scripts first reproduce the v1.0 numbers exactly. The forward PE pace is each history's own 2026 pace.

| First 12 months, $bn | v1.0 (rate leg) | **Sealed v1.1** | Mature | 10% → flat | 20% growth | v1.0 reproduction |
|---|---|---|---|---|---|---|
| PE unfunded; 2026 pace | 27.4; 7.2 | **16.4; 5.34** | 13.9; 4.95 | 18.4; 6.60 | 31.9; 15.3 | 27.4; 13.9 |
| V6 (distribution / contribution) | — | **pass / pass** | pass / fail | pass / fail | fail / fail | pass / fail |
| Drought PE: distributions / calls / net | 6.34 / 8.65 / −2.32 | **4.63 / 5.48 / −0.85** | 5.37 / 4.64 / +0.73 | 4.15 / 6.10 / −1.95 | 3.02 / 10.53 / −7.52 | 4.40 / 9.09 / −4.68 |
| Drought private book, net | +2.23 | **+3.69** | +5.28 | +2.60 | −2.97 | −0.14 |
| Liquid funding at a 7.5% payout (share of $71bn) | 11.1 (16%) | **9.6 (14%)** | 8.0 (11%) | 10.7 (15%) | 16.3 (23%) | 13.4 (19%) |
| S1: PE net / private net | −9.81 / −11.98 | **−3.89 / −6.07** | −2.41 / −4.58 | −4.96 / −7.14 | −11.14 / −13.31 | −8.50 / −10.67 |
| Literal T4 (reverse stress): PE net / private net | −13.97 / −18.40 | **−7.72 / −12.15** | −6.55 / −10.97 | −8.62 / −13.04 | −14.98 / −19.40 | −12.93 / −17.36 |

*SYNTHETIC – NOT ADIC DATA.* At GS's $7.2bn pace, the sealed book's drought PE net is −$1.06bn (private book +$3.49bn). S1 PE distributions use v2's F multiplier (5.4% of NAV); at G7's 3.5% convention the sealed book's S1 PE net is −$4.89bn. T4′ on census v1.1 is not yet computed (open item).

**Reading the map.**
1. **The drought direction holds for every V6-compliant history; the level depends on vintage.**
   - On the sealed v1.1 book, four groups (+$4.5bn) carry PE (−$0.9bn), for +$3.7bn. Across V6-compliant variants the net is +$2.6bn to +$5.3bn.
   - The sign turns negative only for histories that fail V6: −$0.1bn for the history that reproduces v1.0, −$3.0bn for 20% growth.
   - Either way, the liquid book funds the payout: a 7.5% payout draws $9.6bn on v1.1.
2. **A rate-based engine cannot see vintage; RFT-TA v2 can.**
   - v1.0's PE unfunded/NAV of 0.53 is reachable only by smooth histories growing commitments 17–29% a year through the 2022–26 drought, all of which fail V6's contribution half, or by V-shaped and two-spike histories. Plan-consistent histories top out at $19.3bn; linear programs establish both bounds exactly (groups gap_02 §1.2).
   - Industry cross-check: MSCI's H1-2026 figures imply (dry powder + newly raised) ÷ prior valuation ≈0.31. The sealed book sits at 0.40; the v1.0 reproduction at 0.64 [derived].
   - PE commitments by vintage remain the single most valuable data item ADIC can supply.
3. **PE is 70% (T4′, 12 months; 73% over 24 months) to 82% (S1) of the stressed private drain.** Private Credit and Capital Solutions keep paying ($1.8bn under T4′), but their calls and DDTL draws exceed it.
4. **The overlay swings from a small cost to a large use, and its services, not its own books, drive the use.**
   - In calm years it nets +$0.31bn at the floor: completion beta earns +$0.58bn and the own books cost $0.27bn of premium.
   - In S1 it uses $4.0bn: services (beta VM less ΔIM) −$4.12bn; own books +$0.12bn (tail +$1.18bn, premium −$0.27bn, opportunistic −$0.29bn, IM step −$0.50bn).
   - v1.0's −$6.0bn had four inconsistencies: $15bn of beta against the stated $10bn; a missing $5bn of P2S proceeds (the Red tranche nets +$2.74bn and belongs on Public Markets' line); an opportunistic loss breaching L2; and a ladder at 2.7× the IC floor. At the 0.25% budget and the 0.50% cap the S1 use is $3.6bn and $2.6bn.

### 2.3 Liquidity levers by group

| Lever (group) | Year-1 cash | Cost or economics | Cost per $ of month-24 T4′ headroom (5-year PV) [I] | Time to cash | CFP stage; decides |
|---|---|---|---|---|---|
| Treasury above the 4% hard floor (CF) | $15bn less 4% of NAV and encumbered IM | ≈0 | — (inside CBC_TP) | T+0 | Any; CF |
| Treasury top-up from DM equities (CF; Public Markets executes) | Up to $10.6bn | Sale costs as for long-only | 0.249: it relieves only 0.30 per $, because the year-2 draw and the 4% floor are NAV-linked | T+1/T+2 | Any; CF |
| Tail monetization; IM released by opportunistic de-risking (Overlay) | Path-dependent; the floor ladder pays ≈$1.2bn in S1 | Negative | Tail: inside the T4′ convention. Opportunistic IM release ($1.0bn): 0.690, the dearest lever | 1–7 days | Event-Red; pre-approved rules |
| P2S on DM equity (Public Markets proposes, Overlay executes, CF funds VM) | $4.1bn per $5bn (normal); $2.75bn (stress) | Per $ freed per year: 0.40–0.70% (normal), 0.80–1.11% (Jun-2026), 2.24–3.33% (stress) [I-calc] | ≤ 0 on T4′ (VM; no credit for the rebound). The cheapest source for the 8% T2 target: 3.4% PV per $ | 1–7 days | Red, Tier B; IC |
| Long-only sales (Public Markets) | Up to $36bn | 4–13bp (US large cap) to 23–40bp (EM, incl. taxes) on a $1–5bn basket [I-calc] | — | T+1/T+2 | Red; IC |
| Committed unsecured revolver (CF) | $10–15bn requested; credited at 80% from month 2 with covenant headroom | SOFR + 85bp drawn, 15bp undrawn, 15bp upfront per 3 years [I; S anchor: BXP 8-K]; counts 0% in 30-day rows | **0.011** | Month 2+ | Red; CF |
| Hedge-fund redemptions (Public Markets) | ≈$4.9bn of cash within 90 days | Forgone α; queue and gates | 0: by convention the whole book is noticed at t0 inside CBC_TP | 3–24+ months | Notices at Amber; IC |
| LP-portfolio NAV facility (CF owns; Capital Solutions prices) | **Dominated.** A 20% pledge cap on $106bn of private NAV supports $2.1bn at 10% LTV, of which $1.1bn is credited at the 5% stressed LTV | SOFR + 300bp (250–400) + 1–2% OID, +140bp in stress; forced paydowns in the stress; $1 raised encumbers $3.3–20 of NAV [C] | 0.070, ≈6× the revolver per credited $ | 6–12 weeks | Not a primary lever (groups gap_01); CF |
| SMA run-off switch (Private Credit) | +$0.8–0.9bn [C] | Forgone reinvestment value net of losses | 0.048 (run-off at 6.5% a year, the crisis rate) | Quarterly | Amber; group |
| SMA performing-loan sales (Private Credit) | SMA book × price; a $5.6bn sleeve shared with run-off | 1–4% discount (N/T); beats run-off once ℓ̄ > 0.8–1.0% at a 0.99 price [I-calc] | 0.054 (sale at 0.96, the T-regime price) | Weeks | Amber; group / IC |
| PE pacing cut | $0.67bn (one-year pause at the sealed $5.34bn pace, census v1.1); $3.5bn by 2030 [I-calc] | c^PACE ≈8.6¢ per PE $ forgone in M1 (5.6–12.3¢ across models): net α\*, κ^GP and lost co-investment flow [I-calc] | 0.219 (stage cut with a protected 25% core) | 1–4 quarters | Amber 0.25–0.5×; Red re-ups only; CIO / IC |
| Co-investment pause | Up to accepted flow: $0.6–1.2bn a year on census v1.1 | Forgone selection value (≈ the avoided fee, 3–4% a year) | 0.123 | Immediate | Amber; CIO |
| Contingent budgets off (Secondaries / Private Credit / Capital Solutions) | Up to $1.2bn a year each | Forgone franchise value: 15–22¢ per $ deployed when the gate is open (§4.5) | 0.299 / 0.093 / 0.426 | Immediate | Amber; group |
| Private Credit / Capital Solutions sales | Partial; Capital Solutions syndication or sell-down at 0.90, up to $2.0bn | 11–30% discount | 0.243 (Capital Solutions at 0.90) | 3–4 months | Red; IC |
| PE / Secondaries / Co-investment LP and single-asset sales | ≤ 5% of strategy depth per half-year | 9–45%; success 0.4–0.5 in crisis [I] | Excluded from Phase I: recovery never presumes a fire sale | 3–9 months | Black; Board + owner |
| Owner band use | $8.85bn a year (5% vs 10% of $177bn) | The owner's deferral cost | 0.072 (binary; 13.4 of relief) | Per mandate | Requested at Red; Board + owner |

*SYNTHETIC – NOT ADIC DATA.* The cost column is groups gap_01's lever catalogue at s\*(0.76). Cost bases [I]: pacing is α\*·D per $ forgone; sales are the discount plus 2% a year of carry where α\* > 0; P2S is 0.40–0.70% a year per $ freed; the revolver and the band follow gap_02. SMA run-off and sales are the cheapest group levers, at 4.8–5.4% PV per $ of headroom.

### 2.4 The cross-group liquidity ladder

**Ownership.** CF holds one pool under its own operational control, as Basel LCR30.18 requires of HQLA [S]. Groups receive a ladder-contribution target and a consumption budget B_g.

**Mechanics.**
- Buckets run B0 (T+0) to B7 (> 24 months). Committed lines count from B3 and never in 30-day ratios [S: Reg YY]. Intra-ADIC transfers count zero.
- Survival is computed as:

  $$\mathrm{NCO}_s(h)=\sum_{t\le h}(O_{s,t}-I_{s,t}),\quad \mathrm{CBC}^R_s(h)=\sum_{k\in R}\sum_{t\le h}q_{k,s,t}P_{k,s,t}(1-\eta_{k,s,t})+F^R_s(h),\quad \mathrm{SH}^R_s=\min\{h:\mathrm{NCO}_s(h)>\mathrm{CBC}^R_s(h)\}$$

- Recourse tiers nest: T (Treasury) ⊂ TP (+ Public Markets) ⊂ TPF (+ facilities) ⊂ TPFA (+ amber sales: Private Credit, Capital Solutions) ⊂ ALL (+ red sales: PE, Secondaries, Co-investment).
- One recourse LP, priced per state on cost and reach, replaces any fixed merit order. Repo is a route, not a source. Pacing cuts and owner band use run in parallel from Amber.

**Ladder rows.**
- **L1 (= T3):** 30-day coverage on CF-controlled, Basel-capped HQLA with facilities at 0%. On this basis the synthetic book is at 1.91×; 2.10× counts assets outside CF's operational control (Basel LCR30.18) [C].
- **L2:** rows at 3, 12 and 24 months under T4′. The 24-month row on T + P + F is hard, and its duals give ℓ_h.
- **L3 (= T2):** usable IG + cash, net of encumbered IM, at 8% elastic and 4% hard (Basel LCR20.5: buffers are for use [S]). At t0 it is $13.6bn against $14.2bn, or 7.7% of NAV [I-calc, gap_02].
- **L4:** group budgets on the binding horizons (groups gap_01 §1.4),

  $$\textstyle\sum_g B_{g,h}+B_{\mathrm{OVL},h}\le \mathrm{Pool}_h=\mathrm{CBC}_{TP}(h)+F(h)-D(h)-\mathrm{opex}(h)-\mathrm{fees}(h)-0.04\,W(h),\qquad h\in\{12,24\},$$

  with $LC_g=\sum_{i\in g}(\kappa_g^{s^*}U_i+c^{s^*}_i-\delta^{s^*}_gV_i)\le B_g+u_g$, whose dual is the group's hurdle. The 24-month row is hard. The 12-month row is reported but is slack in every configuration.
- **L5–L7:** encumbrance, facility availability (with forced paydowns) and hedge-fund notice dates.
- **L8:** private NAV + unfunded ≤ 0.80W. Census v1.0 is at 0.81, a breach of $2.4bn; the proposed census v1.1 is at 0.75, a pass with $8.6bn of headroom [I-calc].

**Results on T4′** [I-calc; SYNTHETIC]. Groups gap_01's group-resolved replica of gap_02's ladder reproduces `t1_engine.ladder` exactly on six readings × eight policies. It runs on gap_02's unfunded split; census v1.0 moves SH_TP from 17 to 18 months.

| s\*(0.76), canonical conventions | SH_TP (months) | SH_TPF (months) | Minimum 24-month headroom ($bn) | Facility for 24 months ($bn) |
|---|---|---|---|---|
| Do nothing | 17 | 17 | −11.1 | **13.9** (SAA 13.9–15.1; pooled 14.6) |
| Stage-triggered pacing rule | 20 | 20 | −4.9 | 6.1 |
| Owner band | 29 | 29 | +2.3 | 0 |
| Rule + band | > 36 | > 36 | +8.6 | 0 |
| Revolver $13.9bn | 17 | 24 | 0.0 | — |
| Mix A: revolver $15bn, $6bn pacing + rule, reserve 14% | 24 | > 36 | +12.0 (+0.0 without the revolver) | — |
| Mix B: revolver $10bn, rule, band | > 36 | > 36 | +10.8 | — |
| NAV facility $2.1bn | 17 | 18 | −10.1 | 12.6 |

*SYNTHETIC – NOT ADIC DATA.* θ\* is slightly understated: ten 50k-path replications of the M6 calibration give 0.76–0.81, and the pooled 500k-path estimate is 0.79 ($14.6bn). gap_02's single seed was the lowest of the ten.

**L4 group budgets B_g, 24 months / 12 months, $bn** [I-calc; SYNTHETIC].

| | Do nothing | Minimum T4′ plan: revolver $13.6bn + SMA sale $0.58bn | Mix A | Mix B |
|---|---|---|---|---|
| PE | 20.9 / 11.4 | 20.9 / 11.4 | 16.8 / 10.4 | 17.7 / 10.7 |
| Secondaries | 3.5 / 2.5 | 3.5 / 2.5 | 2.8 / 2.3 | 3.0 / 2.4 |
| Co-investment | 3.0 / 1.6 | 3.0 / 1.6 | 1.0 / 0.7 | 1.5 / 0.9 |
| Capital Solutions | 0.5 / 0.2 | 0.5 / 0.2 | −0.1 / 0.0 | 0.0 / 0.1 |
| Private Credit | 0.8 / 0.7 | 0.9 / 0.8 | 0.1 / 0.6 | 0.3 / 0.6 |
| Overlay | 1.3 / 2.9 | 1.3 / 2.9 | 1.3 / 2.9 | 1.3 / 2.9 |
| Pool | 18.9 / 25.4 | 30.1 / 36.7 | 33.9 / 40.9 | 40.2 / 41.9 |
| **Slack** | **−11.1** / +6.1 | 0.0 / +17.2 | +12.0 / +24.1 | +16.5 / +24.4 |

*SYNTHETIC – NOT ADIC DATA.*

**Other ladder metrics** [I-calc; SYNTHETIC].

| Metric | Value | Source |
|---|---|---|
| ADIC-LCR(30d), Basel-capped | 1.91× on CF-controlled HQLA (L1); 2.10× in total | GC2 [C] |
| Hedge-fund cash | $4.9bn within 90 days with static buckets ($7.1bn if notice capacity is misread as cash); $10.7bn by month 6 under the state machine, front-loaded | GC2; gap_01 |
| S1 SH_TP, fixed-USD draw (static / state machine P5) | 17 / 21 months on census v1.0; 35 / 31 on census v1.1 | GC2; gap_01; groups gap_02 |
| P(red event within 5 years) from today's drought + Gulf-war state | Do nothing 8.2 / 21.2 / 37.3% (M1 / M4 / M6). Mix A ≤ 0.98% and Mix B ≤ 0.79% in M1–M5 (one-sided 95% CP bounds) | gap_02 §2 |
| Same, on the integrated engine with group playbooks | Do nothing 1.6 / 6.3 / 14.5%; Mix B 0.00 / 0.00 / 0.09%, assuming no playbook slippage | groups gap_04 §2 |
| 12-month LaR99 | $28.4–38.3bn across M1–M6 (mean $31.2bn), replacing G7's single-model $33.9bn | groups gap_01 |
| **Reverse stresses**, canonical conventions: literal T4 / T4 as written / critic reading | SH_TP 15 / 12 / 8 months; minimum 24-month headroom −16.1 / −20.7 / −45.8; facility $32.2 / 41.5 / 91.7bn, against T5's $26.6bn hard debt limit | gap_02 §1.3; groups gap_01 |
| **Reverse stress**, literal T4 at G7 conventions | SH_TP 12 / 15 months (static; fixed-USD / current-NAV), 15 / 18 (state machine). Facility $42–49bn / $25–31bn (static) and $40.6bn / $23.2bn (state machine) on census v1.0; $20.9 / 19.5bn (fixed-USD) and $3.7 / 2.3bn (current-NAV) on census v1.1 | GC2; gap_01; groups gap_02 |

- **What drives what.** Hedge-fund terms drive the stage metrics; the draw rule and the stress vertex drive the facility need. P5 and P50 differ by at most a month, so ADIC's documents matter more than gate randomness.
- **The red-event gate is reachable.**
  - Mixes A and B certify ≤ 1% in M1–M5, with Clopper–Pearson bounds of 0.98% and 0.79% (gap_02 §2.3).
  - In the M6 class the floor is 2.4% with the band and 5.2–5.8% without it, against the 5% M6-class capacity level.
  - On groups gap_04's integrated engine, the group playbooks (PC run-off, co-investment pause, overlay de-risking, TPA's beta cut) take Mix B's M6 rate to ≈0.1%. gap_02's 2.4% floor is therefore a property of a playbook-free engine. Re-certify on the integrated engine with playbook-slippage stresses before relying on that.

**Contingency-funding stages** (SR 10-6, Reg YY and FSB 2024 practice [S]). The last column reads the do-nothing book at t0 (groups gap_01 §1.3, with the L1 basis corrected).

| Indicator | Green | Amber | Red | Black | t0 reading |
|---|---|---|---|---|---|
| SH_TP under T4′ | ≥ 24m | 18–24m | 12–18m | < 12m | 17m (18 on census v1.0): **Red** (readiness). 20m with the pacing rule (Amber); 29m with the band (Green) |
| ADIC-LCR(30d), CF-controlled, Basel-capped | ≥ 2.0 | 1.5–2.0 | 1.0–1.5 | < 1.0 | 1.91×: Amber |
| Usable IG + cash (net of encumbered IM) ÷ NAV | ≥ 8% | 6–8% | 4–6% | < 4% | 7.7%: Amber. 8.0% after a $0.56bn top-up |
| Liquid share | ≥ 28% | 24–28% | 20–24% | < 20% | 30.8%: Green |
| LaR99 ÷ CBC_TP (12 months) | ≤ 0.6 | 0.6–0.8 | 0.8–1.0 | > 1.0 | 0.65 (M1–M6 mean); 0.80 (M6): Amber |
| Pre-approved actions | Normal pacing; dry powder within budget (Treasurer) | Commitments cut to 25–50% with a protected core sleeve; co-investment paused; hedge-fund notices lodged; SMA run-off switched on; revolver availability confirmed by a test draw; owner dialogue opened (CIO) | *Event-Red:* lines drawn; P2S and long-only sales; hedges monetized; opportunistic book cut; amber sales; formal band request (IC, weekly) | Red sales; non-contractual outflows suspended (Board and owner) | — |

*SYNTHETIC – NOT ADIC DATA.*

- Any hard trigger escalates the stage; de-escalation needs two consecutive better readings. Indicators are computed both gross and net of drawn facilities (groups gap_04).
- **Readiness-Red versus event-Red** (groups gap_01 §1.3).
  - When the only Red indicator is forward-looking (SH_TP under a hypothetical stress), the stage triggers the Phase-II plan, not the Red event playbook. That plan is: adopt the pacing rule, request the revolver, request the band.
  - Event-Red comes only from 30-day coverage, usable IG + cash, liquid share and LaR. The Red column's actions are event-Red actions.
- **Where the synthetic book starts** [I-calc; groups gap_01, gap_04].
  - Under T4′ it is readiness-Red at the Red/Amber boundary (17–18 months), and its current indicators are Amber.
  - It reaches Amber after one calm quarter, or once the pacing rule is adopted and the 8% target restored.
  - Mix A starts Green. Mix B starts Green, or Amber in 47–66% of paths on the Treasury-share indicator.
  - v1.0's "starts in Red" held only under literal T4.
- Early-warning indicators include ADIC's *own* sale-failure rate (replacing Lazard's survey figure), LP pricing below 85%, a PE distribution rate below 6%, calls ÷ distributions above 1.5, gate notices and DDTL utilization spikes.

---

## 3. Group specifications

### 3.0 What every group shares

- **Fields.** Every position carries `group`, `is_synthetic`, look-through company and GP ids, consent/ROFR/pledge flags, bitemporal u/a/f series (underwritten, actual, forecast) and an encumbrance flag.
- **Scoring.** Every action is scored by C2's full reduced cost on the one kernel, on common random numbers (main §4.4):
  - **SELL** iff $p^{ceq}>p^*=[\mathbb E\,\mathrm{LAPV}(\text{HOLD}+\text{best REFI})+\kappa^{GP}+\kappa^{irr}-\text{relief}]/NAV+c$.
  - **REFINANCE** iff $s_B+f/T+\lambda_{Lev}+\text{covenant charge}<\bar\ell_{[0,T]}$. The one-period case pays iff ρ > s, not ρ > r_f + s [C].
  - **ADD** iff $\alpha^*-\bar\ell_{[0,D]}-\lambda_Rm+(1-p^{buy})/D>0$.
  - **LEVER** iff ADD and REFINANCE both pass.
- **Regimes** have two layers:
  - the exit window $e_t$ drives cash flows, exits, recaps and prepayments;
  - the macro regime $z_t$ drives prices, financing terms, execution and spreads;
  - the credit state is $f(z_t,e_t)$ plus frailty.

  Today is LATE × D, with credit tight.
- **Liquidity premium.** ℓ is quarterly, from H's duals. Against a deal NPV, use $L_s=\pi_{s,0}/\bar\pi-1$: stream 08's illustrative 9%/9%/4% path gives one-off equivalents of ≈17.5/20.3/23.7% for 2.5/3.4/4.5-year durations [C]. Decision cards show break-even ℓ.
- **Concentration** is one exposure graph across groups (sponsors → funds → companies → every ADIC claim; §6, gate V24). Hard limits: company ≤ 1% of NAV; GP ≤ 5% of private NAV + unfunded (≈$7.2bn on census v1.0; ≈$6.7bn on v1.1). Counted on the graph, the largest GP averages 4.7% (p95 6.6%), and 35% of sampled censuses breach the 5% limit [I-calc, groups gap_02 §6].
- **Inadmissible actions:** call default (ILPA remedies reach 100% forfeiture [S]); excuse-right abuse; non-consented transfers or pledges; counting intra-ADIC transfers as liquidity; refusing contractual DDTL draws; MNPI flows between groups.

### 3.1 PE funds (Group 1)

**Mandate.** The group makes primary LP commitments to third-party buyout, growth, venture and sector funds [A]. Its controllable object is the commitment program, a delayed control system.

| Item | Specification |
|---|---|
| **Holdings and schema** | *Fund:* GP, strategy, region, vintage, commitment K, unfunded U (recallables separate), dated flows, reported and economic NAV, fee and carry state, subscription-line and GP NAV-loan balances, LPA term and extensions, LPAC seat, transfer/pledge/ROFR terms, side letter (fee tier, MFN, co-investment rights, line opt-out). *GP:* belief $(\mu_g,\sigma^2_g)$, tier, next fundraise, offer log |
| **State and decisions** | Per fund: K, U, $N^{rep}$, V, age a and effective age $a^e$, line and NAV-loan balances. Program: exposure $E=U+N^e$ and overcommitment $E/(w^*W)$. Decisions: the commitment budget inside the stage corridor; tickets; re-ups; SELL fraction; CV elections when offered; LPAC votes; proposals to CF |
| **Model** | RFT-TA v2: $C=(1-e^{-\lambda\Delta})U$, $\lambda=\bar\lambda_s(a)m^C(e_t)e^{u^C}$, with distributions on the effective-age clock (κ(e) = 1.2/1.0/0.6/0.5). G1 mechanics: (1) line-financed investment, with stressed 12-month calls $=\lambda^{str}(U-B^{SL})+c^{SL}B^{SL}$ [C]; (2) GP NAV loans, $D\mathrel{+}=\ell V$, partly recallable, swept from later distributions; (3) GP-triggered CV offers arriving at $e_t$-dependent rates; (4) extensions with a fee step; (5) sales in which the buyer assumes the unfunded; (6) recycling ≤ 110%; (7) fees inside net flows. Pacing: MPC on E with the corridor as a hard constraint |
| **Liquidity and stress** | Calls are sticky at 27–31% of unfunded. Tier 1 uses T4′: PE-type distributions at 10.8% of drought rates and calls ×1.38 over 23 crisis months. Literal T4 (distributions zero, calls ×1.5) is a reverse stress. Pacing acts with 1–4-year lags. *Cash map:* drought −$2.3bn on census v1.0's rate leg, −$0.9bn on census v1.1; T4′ −$11.4bn in 12 months and −$20.9bn in 24 (census v1.0) |
| **Forecasts and bias** | *Filed:* call and distribution quantiles (4 and 8 quarters), terminal TVPI, exit timing for the top holdings. *Fusion:* the FBE fund-interest path, Bornhuetter–Ferguson/Benktander with a prior frozen at inception, fused with the forecast only [C]. *Bias priors:* b^u +5.0, b^f +3.0pp a year (+4.0 after age 8). *Timing slip:* +2–4 quarters normally, +4–8 in a drought [I]. *Also:* fundraising-window marks [S: BGK]; IRR reported with and without lines [S: ILPA] |
| **Synthetic defaults** | 120 interests, ≈70 GPs. *Strategy:* large buyout 40%, mid buyout 25, growth 12, VC 8, sector 10, special situations 5. *Region:* US 60, Europe 28, Asia 12. NAV $52bn. *Unfunded:* $27.4bn on census v1.0, which only V6-failing histories reproduce. The proposed census v1.1 seals $16.4bn (U/NAV 0.32; 2026 pace $5.34bn) from a vintage-by-strategy history (§6). *Truth variants:* mature $13.9bn, 10%-then-flat $18.4bn, 20% growth $31.9bn, v1.0 reproduction $27.4bn. *GP tiers:* elite 10% of GPs (20% of NAV), core 50% (60%), other 40% (20%) |

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Call schedule | 20/25/30/35/40% of remaining unfunded by age; ≈90% called by year 6 | Ljungqvist–Richardson 2003 [S] | High |
| Contribution / distribution rates | 27–31% / 9% (H1-26), 9–11% (2022–25), 17–24% (2017–20). Definitions: distributions ÷ previous valuation; contributions ÷ (starting dry powder + newly raised capital), both annualized | MSCI Q2-2026, Oct 2026, pp. 13, 16 [S] | High |
| Census-history fit (census v1.1, proposed) | Commitments +1.44% a year to 2020, 1.5× in 2021–22, −5.75% a year from 2023. H1-2026 rates 9.0% / 29.0%; largest vintage 2021 at 13.1% of NAV | RFT-TA v2 linear-program fit, groups gap_02 [I-calc] | Medium, until ADIC's vintages arrive |
| Exit-window multipliers (O/N/D/F) | m^D 1.25 / 1.0 / 0.45–0.50 / 0.30–0.35; m^C 1.3 / 1.0 / 0.95–1.0 / 0.8, plus stress calls | MSCI-anchored [I] | Medium |
| Risk; smoothing | β ≈1.0 (VC 1.4); total risk 33% (40%) [S]; reported AC1 0.66–0.71, implied by Brown–Ghysels–Gredil's smoothing estimates (weekly λ 0.951, a working-paper figure not in the *RFS* abstract; quarterly AR(2) 0.5/0.3) [I-calc on S] | Brown–Ghysels–Gredil 2023, *RFS* abstract (β, total risk); AC1 derived in main cluster C2 [corrected 2026-10-18: AC1 is a derivation, not a published figure] | High |
| GP skill and persistence | σ_γ 4.8–5.3%, S/N per fund 0.12–0.14 (large buyout). Post-2000 buyout persistence: none beyond avoiding the bottom quartile | Korteweg–Sorensen 2017; Harris et al. 2023 [S] | High |
| Subscription lines | 26.6% usage; 5.8% of called capital; IRR +2.6pp | Albertus–Denes, 2014–19 data [S] | High |

| Action | Economics and rule |
|---|---|
| **SELL** | LP-led sale at C2's hedonic price: buyout 0.91–0.94 of lagged NAV in normal markets; age multipliers 0.99/0.96/0.88/0.79/0.70; a crisis residual of 0.80–0.84 of *economic* NAV [S/I]. A late-life fund flips at an 86.9% bid; at 80/75/70% bids, HOLD wins unless ℓ ≥ 8.6/15.9/24% [C]. A forced PE sale is a red event (T6). A sale to Secondaries raises nothing |
| **HOLD** | Continuation value. Approve extensions only with a fee step-down |
| **REFINANCE** | Proposed to CF. *LP-portfolio NAV facility:* SOFR + 300bp (250–400); LTV 10–20%; OID 1–2%; sweep trigger at 1.5× opening LTV, default at 2×; per-fund pledge consent. As a liquidity lever it is dominated by the committed revolver: pledge-capped at ≈$2.1bn, it costs ≈7.0% vs 1.1% PV per credited dollar, so it is not a primary CFP lever (§2.3). *LP-portfolio preferred:* advance 20–35%; 12% (14% in stress); MOIC floor 1.3×. Consent to a GP NAV loan only if its all-in spread is below ℓ̄ over its life, and strip its often-recallable "synthetic DPI" from forecasts |
| **LEVER** | Up-size a re-up only where the posterior option value clears hurdle + ℓ + risk charges. Borrowing to fund calls is CF's decision; never default on a call |
| **PACE** | *Corridor:* Green 0.75–1.25× plan; Amber 0.25–0.5× with a protected core-franchise sleeve; Red protected re-ups only. The stage-triggered cut (protected 25% core) is a recovery lever at 21.9% PV per $ of T4′ headroom. *Cost of a cut,* in kernel currency (groups gap_04 §7): $c^{PACE}=\sum_gw_g(\alpha^*_g-\mathrm{FTP}_g)^+D^{>T}_g+w_{PE}\big[\kappa^{GP}+\theta a(\alpha^*_{co}-\mathrm{FTP}_{co})^+D_{co}\big]$. In M1 a PE dollar forgone costs 8.6¢: net α\* 1.35¢, κ^GP 5.12¢ (upper bound; central 2.3¢) and lost co-investment flow 2.12¢ (θa = 0.149 per PE $). It is 5.6–12.3¢ across models [I-calc]. The beta can be rebuilt with overlay futures, booked to TPA. *Cash effect* (census v1.1, RFT-TA v2, drought to 2029): a 2027 pause at the sealed $5.34bn pace returns $0.67bn in year 1 (12.5%) and $3.51bn by 2030 (66%), then costs $4.38bn over 2027–40, with NAV 7.5% lower in 2031. Pausing 2027–28 returns $6.22bn by 2030 and costs $8.13bn; halving 2027–28 returns $3.11bn and costs $4.06bn. The 66% four-year share is pace-invariant. G1's mature-pace figures ($1.0bn, $3.6bn, −$4.1bn) remain a cross-check [I-calc]. The pause's implied IRR (9.8%) is the engine's NAV growth restated (G1 verifier R1), never a financing rate [C]. Each $1bn a year of cuts lowers steady-state calls by ≈$0.95bn; the unfunded half-life is ≈2.1–2.5 years [C] |

**Constraints.** No call default (hard); OC band 1.25–1.6× on economic NAV, tightened in a drought; vintage ≤ 15% of PE NAV; ADIC ≤ 15–20% of any fund [P]; Σ(private NAV + unfunded) ≤ 0.80W (0.81 on census v1.0; 0.75 on v1.1).

**GP access.** Value the re-up option on the *posterior*, $\mathbb E[(\mu_{g,k}-h)^+]$, by preposterior least-squares Monte Carlo. G1's prior-based formula overstates it by ×2.6/1.5/1.3 for buyout GPs with 1/5/10 funds of history, and by ×5.0/2.4/1.8 for VC [C].

### 3.2 Secondaries (Group 2)

**Mandate.** A hybrid book, confirmed by the user: LP commitments to secondary funds, plus direct deals (LP-portfolio purchases and GP-led continuation-vehicle stakes) [A]. The group is also ADIC's secondary-pricing intelligence.

| Item | Specification |
|---|---|
| **Holdings and schema** | *Sub-books:* S1 secondary-fund commitments; S2 evergreen units; S3 purchased LP interests; S4 single-asset CVs (SACV); S5 multi-asset CVs (MACV); S6 other (preferred, tender, strip). *Fields:* reference NAV and date; cash-equivalent cost P^ce; deferral schedule; unfunded; look-through; fees and carry; CV alignment (GP commitment %, carry roll, status-quo option); underwritten and forecast cash flows; bid distribution; consent flags |
| **State and decisions** | Per position: $N^{ref}$, V, θ (true value ÷ reference NAV), U, a, quality q, P^ce, deferred balance. Book: facility, LTV, contingent reserve $R_t$. Decisions: S1 commitments; purchase share, bid and structure (cash or deferral); tertiary or strip sales; CV elections when offered. Internal crosses are governance events, never optimizer variables |
| **Model** | *Price:* $p_{j,t}=\Pi^k_t\,g(\text{age},\text{geo},q,\text{size},U/N,\text{software})\,h(z_t)e^{\varepsilon}$, with depth instrumented. *Cash equivalent:* $p^{ce}=\phi p_d+(1-\phi)p_d(1+r_v)^{-t_d}$. *Entry value:* $V_0=N^{ref}e^{\beta r^m}q(1-f)$, de-smoothed or staleness-inclusive but never both. *Templates:* LP interests run on RFT-TA v2 from the purchase state; the fund layer calls ≈45% a year of remaining unfunded for 4 years [P]; CV stakes run on the shared EV engine, with median exit ≈4.5 years, equity β ≈1.5–1.6 and volatility 54–59% [I-calc]. *Returns:* accretion $A_0=(1-p)N^{ref}$ and $(1+y_P)\approx(1+y_V)(\theta/p)^{1/D}$ [C]. Accretion is reported separately |
| **Liquidity and stress** | Transfers need GP consent and ROFR: 3–6+ months. Deferred payables are debt and a 100% hard outflow. In a drought the secondary-fund DPI edge largely vanishes: net IRR 11.0% → 9.6%; DPI reaches 1.0× in year 8, not year 6 [I-calc]. Tier-1 calls are tested at ≥ 1.0×. Cash map: drought +$1.2bn; T4′ −$2.5bn in 12 months and −$3.5bn in 24 |
| **Forecasts and bias** | *Filed:* underwriting cases plus a quarterly reforecast on economic value. *Fusion:* S1/S3 take the FBE fund path, S4/S5 the single-deal path. *Bias priors:* b^u +2.0, b^f +1.5. *Specific biases:* targets used as expectations (≈26% of SACVs reach 2.3× gross [I-calc]); accretion booked as return; the winner's curse; gross vs net (≈3pp for S1). *Pricing desk:* registered distributions $F_{i,t}(p)$ of *external* clearing prices, scored against later prints and a consensus-only benchmark |
| **Synthetic defaults** | 40 positions, $14.0bn: S1 5.6 (10 funds, vintages 2017–25), S3 4.6, S4 2.0, S5 1.4, S6 0.4. Unfunded $3.5bn plus $0.4bn of deferred payables. Contingent budget only, behind the §4.5 gate. In groups gap_04's engine a purchase at 1 − d acquires θ·(N^econ/N^rep)·N^ref, with θ = 0.92 (0.75 as a sensitivity) |

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| LP pricing (% NAV) | All 87; buyout 91; venture 79; credit 89; real estate 68; Asia 66; tail-end discount ≥ 25% | Jefferies, Jul 2026 [S] | High |
| Buyout price by fund age | 99/96/88/79/70% | Jefferies, Jan 2025 [S] | High |
| GP-led pricing (completed deals) | SACV 34/52/14% below/at/above par; MACV 71/22/8% | Evercore, H1-2026 [S] | High |
| Buyer–seller PME gap | ≈3pp a year at ages 4–9; +24.5pp young funds; −0.8pp tail-end | Nadauld et al., NBER w22404 (2016) age-group tables [S]; not re-checked against the 2019 *JFE* tables, whose abstract gives buyer PME 1.023 vs seller 0.976 [corrected 2026-10-18: source version] | High |
| Tail-end θ | 0.78–0.83 (N), 0.75–0.80 (D), 0.65–0.70 (F) | [I], anchored on Nadauld's 82.2% tail-end price (NBER w22404, Table 3) | Medium |
| Execution; winner's curse | Sales succeed 0.75–0.85 benign, 0.4–0.5 crisis; P(win) ≈0.25–0.35. Curse ≈5.1% with 3 competitors at σ_e = 5% | [I]; [C] | Low / Medium |
| Capacity | ≤ 3–5% of segment volume (2025: $226–240bn) | [I]; Jefferies, Evercore, Lazard [S] | Medium |

| Action | Economics and rule |
|---|---|
| **SELL** | Tertiary sale, resale, or a CV-stake sale or strip, each with consent and ROFR flags. Counts as liquidity only with an external buyer |
| **HOLD** | Economic and exit marks, with the accretion share shown. Never mix since-purchase IRR with forward IRR |
| **REFINANCE** | LP-level facility on S1/S3 (pledge consent; SOFR + 300bp; LTV 10–20%), not secondaries-fund acquisition-line terms; or a CFO on a seasoned pool. Decided with CF |
| **ADD / LEVER** | Buy iff $b^*_j=[\sum\pi CF-\lambda_R\Delta\mathrm{CVaR}-\lambda_{Lev}\Delta Lev-\kappa^{conc}-\kappa^{wc}]/(\pi_0N^{ref})\ge p^{ce}_j$. *Buyer deferral is a vendor loan:* buying at 91% with half deferred for 12 months lifts base IRR from 14.3% to 15.3% but cuts MOIC from 1.47× to 1.41× [I-calc]. *Reserve:* none unless $p_S\mathbb E[(NPV_S-L_S)^+]>$ carry + forgone NPV. *Deploy* (redesigned gate, §4.5) only if the desk's discount forecast exceeds 20%, confirmed by a second reading or an external print, **and** Tier 1 is green, in any stage but Black. Size to min(budget, T4′ headroom less a buffer) and re-test T4′ after deploying. On the do-nothing book the gate almost never opens; under Mix A or B it adds 15–22¢ per dollar deployed at θ = 0.92 [I-calc] |
| **Rotation with PE** | Sell young PE interests near par and buy mature ones at a discount. With fair NAVs and ℓ = 0 the pair gains +8.2 per 100, but −1.8 if θ_mature = 0.90 [I-calc]. Two scored actions, never netted as liquidity |

**Constraints** [I]: group NAV 6–10% of the fund; deferred payables ≤ 10% of group NAV, counted as debt; SACVs ≤ 25%; CV gates (GP commitment ≥ 5% or a full carry roll; competitive price discovery or a fairness opinion). Boyer et al.'s β > 2 measures discount-rate risk in fund-stake prices; it is never a hedge ratio [C] [unverified against the 2023 *JF* version: β > 2 is the 2018 NBER w25207 figure, and the *JF* abstract reports no betas].

### 3.3 Capital Solutions (Group 3)

**Mandate.** The user describes the group as doing "interesting financial deals"; context §1A confirms this as structured and hybrid capital [A]. The working families:

| Family | Content |
|---|---|
| A | Fund finance (as lender) |
| B | GP and LP solutions |
| C | Corporate structured equity |
| D | Junior capital |
| E | Rescue and special situations |
| F | ABF mezzanine and equity tranches |
| G | Preferred claims on LP portfolios |

Two boundaries are for ADIC to confirm (§9): senior/unitranche loans and senior ABF belong to Private Credit; LP-interest equity purchases belong to Secondaries. The group is also ADIC's REFINANCE pricing intelligence.

| Item | Specification |
|---|---|
| **Holdings and schema** | Family, counterparty, GP and company ids, commitment, funded, unfunded, claim C, coupon and margin, PIK window and cap, step-ups, calls and make-whole, MOIC floor, puts, warrants $(n_w,K,T)$ or conversion θ, seniority, collateral, LTV, ICR with a negative-EBITDA flag, covenants, status, amendment log, syndication share, related-party flag |
| **State and decisions** | Status ∈ {performing, PIK, amended, extended, default, workout, redeemed}. Decisions: contingent-budget commitments; syndication share at origination; secondary sale; back-leverage; CFO (6–12-month lead); amendment response (grant PIK or extension, enforce, sell), chosen by least-squares Monte Carlo |
| **Model** | *Income:* $q=Cr\Delta$, cash $q(1-a)$, accrual $C_{t+\Delta}=C+qa$ with $a\le\bar a(\text{age})$. *NAV loan* [C]: $B_{t+1}=B_t+(I_t-D_t)^+-\sigma(\ell_t)(D_t-I_t)^+$ on reported NAV, with an LGD branch $\min(B,hN^{fire})$. *Redemption:* $R=\max\{\kappa(\text{age})C,\ m^{min}I_0-\sum\text{cash},\ MW\}$. *Hazard:* $\lambda^d=\exp(\alpha_{f,z,e}+\beta_1\ln\text{Cov}+\beta_2g(\text{ICR})+\beta_3\mathbb 1\{\text{EBITDA}\le0\}+\beta_4\text{OAS})$; LGD ~ Beta. *Kickers* on the shared EV engine: $\Pi_T=(V-D)^+-(V-D-C)^++\frac{n_w}{n_0+n_w}(E-n_0K)^+$. Crisis recoveries ×0.7 |
| **Liquidity and stress** | Exits via redemption, refinancing, syndication or credit secondaries (89% of NAV in H1-2026 [S]; 20–30% discount in a crisis [I]). *LATE × D:* PIK ×2, prepayment ÷2.5, cash velocity ×0.6. *Crisis:* PIK share 60–80%. A 15%-LTV NAV loan's IRR barely moves (10.8% → 10.3%), but cash back by year 2 falls from 114% to 78% of outlay [S, reproduced]. Cash map: drought +$0.5bn; T4′ −$0.2bn in 12 months and −$0.5bn in 24 |
| **Forecasts and bias** | The group forecasts contractual yield. *Debiased forward return* [C]: $\mathbb E[r]\approx y^{cash}+y^{PIK}(1-p^L_{PIK})+OID/\text{WAL}+\rho\,\mathbb E[\text{kicker}]/\text{WAL}-PD\cdot LGD^{ex\text{-}PIK}-\delta^{ext}/\text{WAL}$, with ρ ≈0.5. *Biases:* WAL too short; kicker optimism; PD understated ×0.7; PIK at face; MOIC floors treated as certain. *Bias priors:* b^u +2.0, b^f +1.5 |
| **Synthetic defaults** | 40 positions, $8.0bn: A 30%, C 20, D 15, E 10, F 15, B 10. Unfunded $1.2bn. Lognormal sizes, median $150m ($50–600m); vintages 2019–26. Three positions in PIK or amendment, one in workout |

**Instrument library** (base LATE × D; [I] unless tagged): senior NAV loan as lender, margin 5.6% (alternative lenders) vs 3.0% (banks) [S, GP-level], LTV 10–15%, PD 0.5%; hybrid fund preferred, 12–14% accrual, MOIC floor 1.3×; GP stake, 6–8% cash yield; structured preferred, 11–13%, warrants 10–20% (≈50% in a crisis [S: Expedia]), PD 3%, recovery 25% of face; holdco PIK, 12–14%, PD 3.5%; mezzanine, 7–9% cash + 2–4% PIK, recovery 18–28% [S]; rescue, 15–20% gross; ABF mezzanine, 10–12%; CFO for the book, senior LTV 35–45% at ≈SOFR + 250–300bp [S].

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Loss-relevant default (EXP / LATE×D / CRIS / RECV) | 1.0 / 2.5 / 6–8 / 1.5% | Fitch PCDR 6.3%, Aug-2026 mix (47/41/8/4) [C/I] | Medium |
| PIK share (families C, D) | 15 / 30 / 60–80 / 20% | [I] | Low |
| NAV-margin stress add-on | +140bp (2022) to +300bp | Rede [S]; [I] | Medium |
| Realized hybrid returns | Tactical Opportunities net IRR 11%; Böni–Manigart mezzanine 9.04%, special situations 12.62% mean (8.0% median); EFW net risk-adjusted ≈0 | Blackstone 10-Q Jun 2026; FAJ 2022; NBER 2024 [S] | High |
| Preferred recoveries | 35.9% / 15.9% without / with a bond default | Moody's, 1983–2008 [S] | High (dated) |
| Crisis-vintage IRR | 14–18% net: optimistic, above every Böni–Manigart mean | [I], flagged | Low |

| Action | Economics and rule |
|---|---|
| **SELL** | Syndication at origination (31% of NAV lenders syndicate, about half of what they underwrite [S: Rede]); secondary sale with copula execution |
| **HOLD** | LAPV under regime hazards; amendment policy max(grant, enforce, sell). Expedia-type stress recoveries on face: −28.5% (0.37×) and −45.5% (0.16×) [C] |
| **REFINANCE / LEVER** | Bank back-leverage (≈SOFR + 300bp) only for cash-pay families (A, F, performing D). D/E ≤ 0.5 at a common 50% trigger, plus a cash-carry row: stressed cash income ≥ interest + fees. At D/E 0.5, a 2.5% loss rate and LGD 0.7, RoE is 10.2% with a bank and 8.9% with an alternative lender, against 9.25% unlevered; cash carry at a 30% PIK share is +0.3% vs −2.3% per $ of debt [C]. Encumbrance ≤ 40% of the book |
| **ADD (now or wait)** | Break-even IRR ≈(1 + r_h)(1 + ℓ̄) − 1 over the capital outstanding. With an ERP of 5%: four-year structured equity needs 13.3% under the 9/9/4 fallback vs 8.3% at ℓ = 1.83%; a drought senior NAV loan needs 14.9% vs 8.1% [I-calc]. Contingent budgets only, behind the §4.5 gate. In recovery, switching the budget off is a priced lever (42.6% PV per $ of T4′ headroom), and syndication or sell-down at 0.90 relieves $0.82 per $ (24.3% PV) |
| **Pricing service** | A P10/P50/P90 quantile model of LP-portfolio facility, preferred and CFO pricing, by LTV, structure, consent and regime. It is trained on term sheets, bids and external RFQs; Rede and Proskauer serve only as priors. Output: a reserve price (CF and the pricing committee own it). Each 10% internal anchor removes 10% of external liquidity [I-calc] |

**Constraints** [I]:
- PIK accounting: accrued-but-unpaid PIK ≤ 15% of NAV; PIK-by-design instruments ≤ 25% of the book.
- Book mix: rescue ≤ 25% outside a crisis; ABF ≥ 15% as ballast.
- Related-party lending: only with ≥ 80% external funding, an independent price check and IC approval.

**Natural-hedge test.** Regress the group's cash on PE distributions, with HAC errors and a regime dummy. Accept a cash hedge only if b < 0 at 90%; the prior is b > 0.

### 3.4 Co-investment (Group 4)

**Mandate.** Minority equity co-investments alongside GPs, deal by deal [A]. Value comes from avoided fees on selected deals; the risks are adverse selection and concentration.

| Item | Specification |
|---|---|
| **Holdings and schema** | GP and linked-fund ids, vintage, sector (software/AI flag), ownership ω, cost incl. follow-ons, dated cash flows, marks, entry EV/EBITDA, net debt/EBITDA, ICR, recaps, exit route, fees (vehicle and company level), rights (tag, drag, ROFR, pledge, CV participation), bitemporal deal models u and f. Plus an offer log by GP: offered, accepted, declined |
| **State and decisions** | V, D, SPV debt, cost, age, mark, ω, ICR, belief $(\hat\mu,\hat\sigma,\hat\tau)$. Decisions: SELL fraction (single-asset sale or strip, if feasible); CV election when offered; pool-facility proposal to CF; ADD; pacing ≤ accepted offered flow |
| **Model** | *EV:* $\ln(V_{t+\Delta}/V_t)=(\alpha-\tfrac12\sigma_{id}^2)\Delta+\beta_Ar_m+\sigma_{id}\sqrt\Delta\varepsilon+\sum J$, with Kou jumps. *Default:* hazard $h_0e^{b(\text{ICR}^*-\text{ICR})^+}$ plus a barrier at V ≤ κD, monitored continuously. A quarterly simulation checks $\kappa D\,e^{+0.5826\sigma\sqrt\Delta}$ (Broadie–Glasserman–Kou's continuity correction, shifted toward the current value; σ the diffusive EV volatility, Δ = 0.25) or steps weekly or finer; monthly checks alone miss ≈13–14% of write-offs [corrected 2026-10-18: `research/groups/addenda/G4_barrier_rerun/RESULTS.md` §1, §7]. *Exits:* Weibull (k 1.447, η 7.70 years, before a refit that excludes bankruptcies) × m_X(e) = 1.3/1.0/0.5/0.3. *Recaps:* exogenous; a post-recap distress multiplier of about ×1.1 (OLS) to ×1.7 (IV) for recaps that add 25% debt (φ = 0.25) [I: Bhardwaj, Gupta & Howell's 10-year distress estimates, which go with an 84% average debt increase, scaled linearly to φ] [corrected 2026-10-18: was 1.4–3.4 (central 2.0), the range for the paper's average +84% recap]. *Marks:* $M_{t+\Delta}=\lambda M_t+(1-\lambda)E_{t-\Delta}+b_g+e_t$, with a Kalman nowcast. Deal-by-deal carry. Equity β ≈ β_A·V/E |
| **Liquidity and stress** | Exits on the GP's clock; SELL takes 3–6 months. Tickets are funded at close. Drought: exit hazard ×0.5; crisis ×0.3, no recaps. From a drought start: 3-year distributions $9.2bn (P10 $3.6bn), net +$3.4bn (P10 −$1.3bn) [I-calc]. Cash map: drought +$1.7bn; T4′ −$1.6bn in 12 months and −$3.0bn in 24 |
| **Forecasts and bias** | *Filed:* deal models (5-year gross IRR and MOIC); 16% of firms set the exit multiple equal to entry [S: Gompers–Kaplan–Mukharlyamov]. *Correction order:* structural corrections first (hold +1.5–2 years; exit multiple shrunk 50% toward entry; EBITDA growth shrunk 30% toward the median), then the residual b^u +6.0 / b^f +3.5, with a GP effect shared with PE funds (ρ_GP 0.6). *Flags:* growth above the reference P75; exit multiple above entry; leverage > 6× or ICR < 2.0×; near-term exit at < 15% regime probability |
| **Synthetic defaults** | 90 positions, $18bn; lognormal σ 0.8 (effective N ≈45; largest $1.2bn); start in D; unfunded $1.5bn. On the overlap graph (groups gap_02 §6), 0.67 of deals by count (0.69 by value) sit in PE look-through, and ≈7 deals (0.08) also carry an ADIC private-credit loan: the recap-netting set. Deal generator on BJS quartiles with ≈10% zero returns, so P(MOIC < 1) ≈0.35–0.40 (G9's 0.22 is a sensitivity) |

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Deal outcomes (buyout gross PME) | Mean 1.76; P25 0.26, median 1.16, P75 2.45; SD 2.10 (N = 365) | Braun–Jenkinson–Schemmerl 2020 [S] | High |
| Net-of-fee portfolios | Buyout beats funds from 5–10 deals at 0/0, ≈30 at 0/20; VC never | BJS 2020, Table 8 [S] | High |
| LP direct-deal record | TVPI 1.20; 2006/07/08 vintages 1.18/1.10/0.78; −0.59 correlation with fund commitments | Fang–Ivashina–Lerner 2015 [S] | High |
| Base rates | ≈1 in 10 returns nothing; 42/58/76% exited by years 5/7/10 | Lopez-de-Silanes et al. 2015 [S] | High |
| Structure; offered flow | Debt/EV ≈36%; offered median 33¢ per fee-bearing $ (GP level) | Bain GPER 2026 [S]; LP use [I] | Medium |
| EV dynamics | β_A 0.9; σ_id 0.25; L0 0.40; exit uplift so ≈75% of exits clear the prior mark [S] | [I], fitted | Medium |

| Action | Economics and rule |
|---|---|
| **SELL** | Bid $p=\mathbb E_b[X]/(1+y_b)^{\tau}-tc$ with a 20–25% gross buyer hurdle: 71–79% of NAV in normal markets, 56–65% in a drought [C]. Realistic use: strip sales of appreciated, high-quality positions. Red tier |
| **HOLD** | LAPV under fused beliefs, less concentration CVaR and κ^GP |
| **REFINANCE** | *Pool facility* proposed to CF: LTV ≤ 10/15/20% for effective N < 10 / 10–25 / > 25; SOFR + 450–750bp; per-deal GP consent. *Single-asset REFINANCE is inadmissible:* quarterly tests breach the trigger on 49.6% (normal) and 62.5% (drought) of paths [C]; 62.2% / 73.4% if LTV were monitored continuously, 54.6% / 67.0% with monthly tests [re-checked 2026-10-18: a quarterly-tested covenant needs no Broadie–Glasserman–Kou shift; `research/groups/addenda/G4_barrier_rerun/RESULTS.md` §5.1] |
| **LEVER** | A 12% holdco PIK at 25% LTV: IRR 9.2% vs 9.2% unlevered (normal), 6.0% vs 6.3% (drought); wipe-out at exit 2.1% → 11.8% and 7.0% → 22.8% [C]; with the G4 dossier's barrier V ≤ 0.75D at any time, 2.2% → 11.8% and 7.6% → 22.9% [re-checked 2026-10-18: at-exit figures, so the Broadie–Glasserman–Kou fix does not apply; RESULTS.md §5.2]. Exception: listed-stake collateral (Verisure-type 5.625% cash / 6.375% PIK [S]) |
| **PACE** | Deployment ≤ accepted offered flow (§4.7): $0.6–1.2bn a year on census v1.1. Within ±30% of NAV target ÷ average life; vintage budget; paused in Amber. In recovery the pause costs 12.3% PV per $ of T4′ headroom and carries 56% of the Q1 glide-path delivery (§4.8) |

**Constraints** [I]: effective N ≥ 40; single position ≤ 4%; entry debt/EBITDA ≤ 6.0×, ICR ≥ 2.0×; SPV LTV ≤ 20%; software ≤ 25%. "No-fee" vehicles still carry company-level fees [S: Torys 2026].

### 3.5 Public Markets (Group 5)

**Mandate.** External hedge funds and long-only equity and fixed-income managers [A]. The group has two roles: a return source (net alpha mostly small) and the liquidity reservoir, which fails differently in each sleeve.

| Item | Specification |
|---|---|
| **Holdings and schema** | *Hedge-fund lot:* strategy, manager, vehicle (commingled, SMA, managed account, HF-TRS basket); reported and de-smoothed NAV; ADIC share ω. *Terms τ:* frequency, notice, lock-up, gates, holdback, payment lag, side pocket, suspension; `notice_revocable` (default false), `transfer_consent`, `pledge_consent` [C]. *Also:* fees incl. pass-through; NAV-weighted leverage. *Long-only:* benchmark, TE target, ADV coverage, tax, and vehicle type (SMA vs commingled decides T+1 sale, P2S feasibility and LCR control [C]) |
| **Return model** | *Hedge funds:* $r_{i,t}=r_{f,t}+\boldsymbol\beta_{i,S_t}^{\top}\mathbf F_t+\gamma_iP_t+\alpha_{i,t}+\sigma_{i,S_t}\epsilon_{i,t}+J_{i,t}$, with alpha decaying in age and size. **F** is Fung–Hsieh plus liquidity: seven factors explain "up to 80 percent" of diversified portfolios [S]. Crisis jumps occur 0.3 times a quarter at 2σ [I], anchored on the GS VIP index's −19.07% in Q3 2008 [S]. *Reporting:* smoothing with fund-level θ (θ₀ ≥ 0.5); the effective incentive fee is ≈50% [S]. *Long-only:* $r=r_b+(\beta-1)(r_b-r_f)+\alpha+TE\,\epsilon$, plus credit beta for fixed income [S]. *Impact:* $Y\sigma\sqrt{Q/V}$ + half-spread + tax, valid up to a few % of ADV [C] |
| **Liquidity state machine** | *States:* LOCK, SOFT, OPEN, NOTICE, QUEUE, SUSP, PAY, SP, LIQ, DONE, TRS_TERM. *At each dealing date:* other investors' requests $R^{oth}=NAV\,\mathrm{clip}(\rho_S+\rho_1[-r^{rel}]^++\rho_2\mathbb 1\{\hat p^{gate}>p^*\})$; a gate if requests exceed gNAV (always if mandatory, otherwise a logit on regime, drawdown, flows, mismatch, leverage); payout min(1, gNAV/R) only when gated; geometric suspensions; side pockets; cash (1 − h)·Pay after the lag; liquidation 50/30/20% by months 3/12/36 [I]. **φ_i(h, S), the P5 cash share by horizon, is the only interface to the ladder** |
| **Forecasts and bias** | *u:* target net α, TE, crisis beta. *a:* de-smoothed, factor-adjusted returns plus realized liquidity. *f:* net-α P10/P50/P90 and a liquidity outlook. *Biases:* selection on past returns; survivorship; smoothing; short-put tails; assumed contractual liquidity. *Bias priors:* hedge funds b^u +3.0 / b^f +2.0; long-only +1.0 / +0.75. *Long-only net IR prior:* −0.05 [C]. *Display-only Z at 5 years:* long-only 0.10 (DM) / 0.17 (EM); multi-strategy 0.66; event/credit 0.32 de-smoothed; trend 0.14 [I-calc] |
| **Synthetic defaults** | 40 hedge-fund lots (σ 0.6) on the mix below, terms drawn to Form PF on its own definition; 24 long-only mandates (DM equity $22bn, EM $6bn, fixed income $8bn); optional HF-TRS scenario |

| Strategy (weight) | β_eq normal / crisis | Net α (sd) | Terms | Crisis gate hazard a quarter |
|---|---|---|---|---|
| Multi-strategy (30%) | 0.10 / 0.30 | 2.0% (2.5%) | Quarterly; 60–90-day notice; investor gate 1/16–1/20 a quarter | 3% |
| Equity long/short (15%) | 0.45 / 0.65 | 0.5% (2.5%) | Monthly–quarterly; 1-year soft lock | 4% |
| Event (10%) | 0.35 / 0.75 | 0.5% (2.5%) | Quarterly; gate 20–25% | 10% |
| Credit (15%) | 0.25 / 0.55 | 1.0% (2.5%) | Quarterly/semi-annual; side pocket ≤ 20% | 20% |
| Relative value (10%) | 0.10 / 0.30 | 1.0% (2.0%) | Quarterly; gate 25% | 20% |
| Macro (10%) | 0.05 / 0.00 | 1.0% (2.5%) | Monthly; 30 days | 1% |
| Trend (10%) | 0.00 / −0.20 | 1.0% (2.0%) | Monthly or daily | 1% |

*All [I]; fees per Cambridge Associates 2024 [S]; results reported across crisis gate probabilities of 5–40%.*

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Investor liquidity (notice-based, gates assumed) | 8.4% ≤ 7d; 27.3% 8–90d; 64.4% > 90d | OFR (Form PF), 30 Jun 2026 [S] | High (definition caveat) |
| Cumulative redeemable | 19.1 / 35.0 / 58.2% at 30 / 90 / 365 days | SEC Private Funds Statistics, Q3 2025 [S] | High |
| Split used | 8.4 / 27.3 / 23.0 / 41.4% at ≤ 7d / 8–90d / 91–365d / > 365d | SEC curve [I-calc] | Medium |
| NAV-weighted leverage | Multi-strategy 4.5×; macro 6.8×; RV 8.1×; equity 1.8×; credit 1.7× | OFR, Jun 2026 [S] | High |
| 2008 stress | Net redemptions $399bn (20%); gates "liberally exercised"; Hedgebay 79.8% of NAV | Hennessee; CA; WealthBriefing [S] | High |
| Fees; long-only alpha | Pass-through median 4.53%; long-only alpha ≈0 across 4,617 products | Ben-David–Birru–Rossi; Busse–Goyal–Wahal [S] | High |
| Equity financing | ≈30bp (2021–23); > 140bp peak (Dec 2024); +81bp (Jun 2026 roll) | D. E. Shaw; CME [S] | High / Medium |

| Action | Economics and rule |
|---|---|
| **SELL (redeem)** | A queued SELL: redeem iff $\hat\alpha^{net}_i+\kappa^{reentry}_i<\bar\ell(T^{cash}_i)$. Keep ADIC ≤ 10–20% of any fund. Penalize redeeming the best liquid funds, the 2008 pattern [S] |
| **SELL (secondary)** | At (1 − d) if that beats the redemption schedule's kernel value; d is 15–25% for quarterly funds in a crisis and 30–50% for gated interests [I] |
| **HOLD** | NAV + PV(α^net) − the value of the terms to the investor (≈1% for a 2-year lock-up, > 10% with discretionary suspension [S: Ang–Bollen]) |
| **REFINANCE** | *Long-only P2S:* exposure unchanged, financing changed. Do it when $\bar\ell_\tau\ge\frac{\bar f+\hat\alpha^{net}+(c^{sell}+c^{rebuy})/\tau}{1-m-b}+\frac{\lambda_{Lev}\Delta Lev}{C}+\kappa^{VM}_{>b}$, with C = (1 − m − b)N the cash freed. *Hedge funds:* unit loans at 20–50% LTV with pledge consent |
| **LEVER** | *Portable alpha* only if net α beats financing plus CVaR, leverage, VM and mismatch charges, with HQLA collateral: $2bn of beta needs $0.70–0.78bn within days in a −33% month, against $0.32–0.65bn returnable within 90 days [I-calc]. *HF-TRS:* a plan for up to $15bn via bank TRS is reported as *under consideration* [S: Hedgeweek, 12 Jun 2026]. It is not ADIC data; modelled as a TRS_TERM branch, it adds no redemption liquidity and costs ≈2 survival months [I-calc] |

**Waterfall and rebalancing.** Priority: Treasury above its floor → P2S on long-only beta → passive sleeves → lowest-α mandates → short-notice, low-α hedge funds → hedge-fund secondaries (gated interests at high λ only). P2S ($y^{p2s}$) and beta additions ($y^{add}$) are separate variables under a 1.30× exposure cap. Rebalance monthly on economic weights with a 2pp band (GPFG uses 2pp [S]), re-centring with futures.

**In recovery** (§4.8). By T4′ convention the whole hedge-fund book is noticed at t0 inside CBC_TP, so notices add no further relief. P2S is the cheapest source for the 8% T2 target (3.4% PV per $), though it gives T4′ no credit. Public Markets contributes $40.6bn of 24-month CBC_TP. At t0 a hedge-fund secondary is a HOLD at 91.9% (revolver signed) or 93.6% (group levers only) [I-calc].

### 3.6 Private Credit (Group 6)

**Mandate.** Funds and SMAs in direct lending, asset-based finance, mezzanine and opportunistic credit [A]. The cash yield is contractual, but how much liquidity it delivers depends on the wrapper.

| Item | Specification |
|---|---|
| **Holdings and schema** | *Loan or cohort:* segment {DL, ABF, MEZZ, OPP}, vintage, sponsor and software flags, par incl. capitalized PIK, spread, floor, PIK flags, OID, maturity, undrawn DDTL/revolver, EBITDA, leverage, ICR, status {cash-pay, PIK-amended, extended, non-accrual, resolved, repaid}, mark. *Vehicle:* wrapper {SMA, CEF, evergreen, listed BDC}, investment-period end, recycling rule, facility terms, fees, unfunded, redemption cap and backlog, P/NAV. *Series:* y^UW, y^ACT, y^GRP |
| **Decisions by wrapper** | *SMA:* reinvestment switch ρ ∈ [0, 1], loan sales, back-leverage, commitments. *CEF:* SELL fraction, LP-level financing. *Evergreen:* tender request. *BDC:* sale at q_t·NAV. *Not decisions:* DDTL funding (contractual); CEF recycling in the investment period (the GP's); fund leverage in CEF, evergreen and BDC wrappers |
| **Model** | *Income:* cash and PIK separate, with δ^PIK 25–50bp [S]. *Competing risks:* $h^{def}=\phi_k\Phi(-\ln\overline{\text{ICR}}/\sigma_{ICR})\xi_te^{\beta'x}$, with $\overline{\text{ICR}}=\text{ICR}_0\frac{E_t}{E_0}\frac{r_0+s}{r_t+s}$ adjusted for PIK and floors. Separate hazards for the PIK switch, maturity extension (probability 0.2/0.3/0.5/0.6) and loss, each calibrated to the series that measures it, never one hazard to a mixture. *Prepayment:* stochastic CPR tied to refinancing incentive and $X_t$. *Draws:* d = 15/20/30/60%, front-loaded in a crisis. *Marks:* catch-up κ 0.5/0.45/0.4/0.3. *Evergreen:* proceeds $\mathbb E[\min(1,\bar c\,NAV/\sum R^{req})]R^{req}_{ADIC}$ [C]. A stagflationary crisis variant is mandatory |
| **Liquidity and stress** | SMA run-off returns 22–30% of principal a year in N. In stress the pattern is wrong-way with PE DPI: prepayments collapse, draws spike, PIK and extensions rise, recoveries fall, gates bind. Run-off counts at the P05 of a stochastic-CPR simulation (deterministic CPR gives 97–99% of the mean [C]). Cash map: drought +$1.1bn; T4′ −$0.7bn in 12 months and −$0.8bn in 24 |
| **Forecasts and bias** | *Group forecast:* $\text{LAY}=\bar r^{fwd}+s+o/T_e-PD\cdot LGD-\text{fees}$, cash and PIK separate (PIK = 11.3% of interest income [S: Lincoln Q2-26]). *Corrections:* direct-loan recoveries, not syndicated; selective-default states; stress-dependent extensions; de-smoothing; a 2021–22 vintage factor. *Priors:* α shrunk toward 0 (EFW); b^u = b^f = +0.75. *Example:* S+520, 1pt OID, PD 2.2%, fees 1% → LAY ≈6.9% [I-calc] |
| **Synthetic defaults** | $14bn: DL 60% (S+550), ABF 15%, mezzanine 10% (⅓ PIK), opportunistic 15%. Wrappers SMA 40%, CEF 45, evergreen 10, BDC 5. ≈1,500 loans in 35 vehicles; undrawn DDTL/revolver $1.0bn; fund unfunded $3.0bn. Start in T. Smoothing 0.5–0.7, replacing G9's 0.3. Overlap graph: 75% of borrowers sponsored; ≈190 loans (0.13) to PE look-through companies |

**Loss calibration (reconciliation R1)** [I-calc].

| Pair | PD | LGD | Long-run loss |
|---|---|---|---|
| GC2 | 1.8% (N) | 0.40 | 1.02% a year |
| GC1 | 1.1 / 1.5 / 2.4 / 6.0% (B/N/T/C) | 0.45 / 0.50 / 0.55 / 0.65 | 1.15% |
| gap_01 | 1.1% (N; ×1.5 in D, ×3 in C) | 0.67 (crisis recovery ×0.7) | 0.99% |

All three pass V12 (0.8–1.2%), but they cannot all be right:
- KBRA's observed payment-default incidence (1.4% in 2025; 2.5% forecast for 2026 [S]) supports GC1's PDs.
- The only observed direct-loan recovery, a post-default value of ≈33% against 52% for syndicated loans [S: Cai & Haque 2024, KBRA DLD data], supports LGD 0.67.
- Together the two observations imply 1.40–1.45% a year, above CDLI's 1.0% realized loss.
- ECB's 50% LGD is a stress assumption, not an observation [S].

**Decision.** The FBE and every Tier-1 stress use the severity-anchored pair, as gap_01 decided. SYN-ADIC-177 carries it and GC1's incidence-anchored pair as truth variants, and estimators must pass SBC on both. GC2's 60% recovery is retired, because it is the value the G6 verifier rejected. ADIC's loan tapes settle the split. Report both PIK multipliers, ×1.5 and ×9: the 5-year P99 loss from T is 12.2% vs 17.2% [C].

| Parameter (B / N / T now / C) | Default | Source, as-of | Conf. |
|---|---|---|---|
| New-issue unitranche | S+470–500 / S+525 / S+525–600 / S+700–900 | KBRA S+510–528; VRC (Oct 2026) [S] | High |
| Payment default | 1.0–1.2 / 1.4–1.6 / 2.3–2.5 / 5–7% | KBRA; Proskauer 2.51% (broad) [S] | High |
| Selective default | 3–4 / 4.5–5 / 6–6.5 / 11–18% | Fitch PCDR 6.3% TTM, Aug 2026 [S] | High |
| DL CPR | 30–35 / 22–26 / 14–22 / 5–8% (≈22% today) | CDLI repayments > 6% a quarter [S] | Medium |
| PIK share of income | 6–7 / 7–9 / 10–12 / 15–20% | Lincoln, Q2-2026 [S] | High |
| Prices | Performing loans 1.00 / 0.99 / 0.95–0.97 / 0.80–0.88; credit LP 0.97–1.00 / 0.92–0.95 / 0.85–0.89 / 0.70–0.78 | Jefferies 89% [S]; [I] | Medium |
| Evergreen queues | Requests 13.9% (Q2) and 13.0% (Q3) of NAV against 5% caps | VRC, Q3-2026 [S] | High |
| ICR | Average ≈2.0×; +300bp with −20% EBITDA multiplies the stressed share ×4.3 | Fed FEDS Note 2024 [S]; [C] | Medium |

| Action | Economics and rule |
|---|---|
| **SELL** | By wrapper. SMA performing loans (α* ≈ 0) beat run-off once ℓ̄ > 0.8–1.0% at a price of 0.99, 2.3–3.1% at 0.96 and 8.7–11.8% at 0.85 [I-calc]; at a SOFR + 5% discount, λ* is −2.9 / −1.4 / +6.6% (N/T/C) [C]. **In Amber and Red, SMA loans near par are among the cheapest private liquidity.** In Phase I, SMA sales (5.4% PV per $ of T4′ headroom) and run-off (4.8%) are the cheapest group levers. They share one $5.6bn sleeve, so run-off and sales cannot use the same loans (EBA/GL/2023/06 ¶30). The minimum T4′ plan's $0.58bn SMA sale restores the 8% T2 target |
| **HOLD** | Reinvest (ρ = 1) or run off (ρ = 0, SMAs only). Forgone value $V^{reinv}=\mathbb E[PV(s^{new}-c^{opp}-EL^{new})]$ [C]. Run-off is the default T/C lever: ≈$0.8–0.9bn in year 1 |
| **REFINANCE** | *SMA back-leverage:* starting LTV ≤ 40–45% against a 65% advance rate, under covenant chance constraints. *CEF interests:* an LP-level loan at LTV 10–20%. *Rated feeder or CFO:* set up 6–12 months before it is needed |
| **LEVER** | SMAs only: senior, non-software, benign or normal states, D/E ≤ 1.0×, and EL < y_A − c_B under P95 losses (≈4.0%; 3.25–3.75% at T-regime cost) [C]. Credit-secondary buying is deployment, not leverage. H1-2026's $20bn market at ≈99% of FMV is a seller's market [C] |

**Constraints:** software ≤ 15%; single borrower ≤ 2%; evergreen ≤ 10%; look-through D/E ≤ 1.0×; 5-year P99 loss ≤ 20% of PC NAV (stress recoveries reach ≈19.4% [C]).

### 3.7 Overlay (Group 7)

**Mandate.** Listed and OTC derivatives in three books [A; groups gap_03]:
- a tail hedge and an opportunistic book, the two strategies of R10;
- synthetic beta, which provides services to other groups and the total portfolio and is the home of rebalancing.

The group sources, prices, executes and monitors. It does not own the service exposures (the clients do), the tail budget (the IC does) or collateral (CF does). The main report specifies the books, market model, surfaces, monetization, margin and hedge valuation (§4.6; C3 §5.3–5.6; gap_03). Groups gap_03 is the group's G-stream-equivalent dossier (G10) and verification log, and brings it to parity with §3.1–§3.6.

| Item | Specification |
|---|---|
| **Holdings and schema** | **`overlay_trade`** (G9, extended): book {tail, opp, beta}; `service_id`; `client_group` {TPA, PUB, PE, COI, PCR}; gap_03 template; strikes and expiry; premium; venue {listed, cleared, bilateral}; csa_id; rung; `s_lock`; hedged-position ids; trigger state; `is_synthetic`. **`crif_row`** (ISDA Risk Data Standards [S]): keys ProductClass, RiskType, Qualifier, Bucket, Label1, Label2; amounts Amount, AmountCurrency, AmountUSD; also TradeID, PortfolioID (netting set), IMModel, EndDate. A blank PostRegulations / CollectRegulations entry exempts the row, which encodes a sovereign-exempt one-way CSA. **`csa`**: threshold, MTA, IA, eligible collateral, reuse right (sets φ), IM regime {two-way SIMM, IA-only}, documents (2016 VM CSA; 2018 IM CSA [S]). **`service`**: client, notional, reference index, s_lock, CLC basis |
| **State** | *Tail:* budget use; rungs; delta; $NV^{eq}(s)$; scenario payoffs; triggers; a fatigue tracker of premium, ex-ante credit and experience. *Opportunistic:* exposures or trades; vol and IM use; posterior Sharpe and DSR with trial count; drawdown; $OR(s)$; curvature-IM share. *Beta:* notional by client; β\* against de-smoothed β̂; realized basis against s_lock; IM; economic exposure |
| **Model** | Main §4.6 plus gap_03's position layer: templates → CRIF → VM by CSA, SIMM-like IM, net-Greek limits, ledger. The tail follows C3 §5.3(e). The opportunistic book uses exposure templates plus a DSR-gated residual α |
| **Liquidity and stress** | *Tail:* a stress source, recognized at φ = 1 / 0.7 / 0, with listed value at 0.85 in ratios only. *Opportunistic:* IM ≈ 0.46 × annual P&L vol, ×1.0–1.5 for netting-set fragmentation; cleared IM can double in stress (FSB P95). *Beta:* P99 30-day VM of 11.7% of notional, plus IM rising from 4% to 10%. *Cash map (§2.2):* +$0.31bn in calm years; −$4.0bn in S1 at the floor |

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Tail budget | Floor 0.15%, cap 0.5% of NAV a year; t0 at the floor | C3 DQ22; GC2 D25 [I] | IC-set |
| Ladder | 90/72%-of-forward put spreads; 3/6/12M rungs weighted 25/50/25; listed first | C3 §5.3(e) [I] | Low |
| Market state | SPX 7,659.44; VIX 19.99; VIX3M 20.50; VIX6M 21.67; VIX1Y 22.61. SKEW 168.59 (mean 123.26; record 183.12 on 18 Feb 2025) | Cboe, 16 Oct 2026 [S rep.] | High |
| Surface | ATM vol = 0.90 × VIX_τ; skew linear in strike, calibrated to the variance-swap identity. 90% / 72% vols: 23.7 / 33.0% (3M), 23.3 / 30.2% (6M), 23.2 / 28.2% (12M) | C3 c_ATM [I]; [I-calc] | Medium |
| Ladder economics | Premium 1.02 / 1.97 / 3.16% of notional (3 / 6 / 12M); **3.74% a year on outstanding notional** (3.47–3.96% across skew assumptions, against G7's implied 3.54%); S1 payoff 0.166 per $ (4.4× annual premium) | [I-calc] | Medium |
| Spot–vol; VIX tenor betas | −1.35 / −0.94. Betas 0.64 / 0.45 / 0.30 for 3M / 6M / 1Y | 09 verifier [S-c]; gap_03 [I-calc] | High / Medium |
| Monetization; recognition | Triggers: Δ ≤ −0.5, value ≥ 3× premium, or V3+ with VIX ≥ 35; sell 50%, reinvest 40%. φ = 1 / 0.7 / 0; listed 0.85 | C3 [I] | Low |
| SIMM | Equity-index delta RW 15; vega margin ≈5.35 × vega per vol point; curvature scaling 23.0 / 3.8 / 1.9% at 1 / 6 / 12M | ISDA SIMM v2.8+2512, effective 11 Jul 2026 [S] | High |
| Schedule IM; UMR | Equity 15%; MSE $8bn; IM threshold $50m; the sovereign exclusion covers central governments only | 12 CFR 237 [S] | High |
| Futures financing | ≈30bp (2021–23); > 140bp (Dec 2024); +81bp (Jun 2026 roll) | D. E. Shaw; CME [S] | High / Medium |
| Opportunistic | Vol 1.0–1.5% of NAV; drawdown stop at 2×; DSR ≥ 0.95; IM $1.0bn within a $1.5bn budget | C3; 09 [I/S-c]; [I-calc] | Medium |
| L1–L3; dealers | L1: $NV^{eq}_{ovl}\ge0.75\,NV^{eq}_{tail}$. L2: OR ≤ 25%. L3: curvature-IM share set by the IC. Dealers: ≤ 0.5% of NAV each; at least 5 | gap_03; C3 [I] | IC-set |
| Contingent-liquidity charge (CLC) on services | c_buf 1.5% × (P99 VM + ΔIM) = **≈27bp a year** of notional (18–53bp at c_buf of 1–3%) | §4.3 [C]; [I-calc] | Medium |

**Actions.** Every action is scored with main §4.4, plus overlay terms (X is hedge inflows, O is VM/IM outflows):

$$\mathrm{Score}(a)=\textstyle\sum\pi\,\mathbb E[\Delta CF_a]+\sum_{h,s}\tilde\mu_{h,s}(\varphi\,\Delta X^{h,s}_a-\Delta O^{h,s}_a)+\sum_k\rho_k\Delta\mathrm{Floor}_k-\lambda_R\Delta\mathrm{CVaR}-\lambda_{Lev}\Delta Lev-\lambda_{Enc}\Delta IM_a-\kappa^{tc}_a$$

An action is admissible only if its score is positive and, after the trade, L1–L3 hold and the safety filter F accepts. The robust variant evaluates the same score on the worst-model duals. REFINANCE reads as "raise cash, keep the exposure".

| Book · action | Instruments | Rule | Lead time; consents | Regime; CFP stage | Encumbrance |
|---|---|---|---|---|---|
| **Tail · SELL** | Monetize; restrike (sell 50%, reinvest 40% lower and longer) | $V(1-ba)+\lambda^w\Delta L^{use}\ge\hat E[\text{cont}]$, with $\Delta L^{use}=V(1-ba)-\varphi R^c$ under a CSA. Restrikes scored as a bundle; L1 must hold | Listed: T+0. OTC: T+0–2 after ≥ 3 RFQs. Novation: consent of all three parties [S] | All; OTC capacity thins in crisis [I]. Pre-approved at event-Red | Releases IM and collateral |
| **Tail · HOLD** | Monthly roll | Mandatory up to the floor, with no score test. Above the floor, only if the robust score > 0 | Monthly; ISDA + CSA for OTC | All; after spikes, roll longer and lower | Listed: premium only. OTC: SIMM ≈$0.19bn at the floor, unless IA-only |
| **Tail · REFINANCE** | Sell a lower strike against a held put; post UST as IM; repo collateral received under reuse | $\sum\tilde\mu\Delta HQLA-\text{cost}-(\Delta KV+\Delta LV+\Delta EV)_{lost}>0$; coverage targets and L1 kept | Days; CSA amendments need dealer consent | Repo haircuts widen in crisis | Changes which assets are encumbered |
| **Tail · LEVER** | More notional; CDX; VIX calls; Brent spreads (need the mandate and the owner); hybrids (≥ 3 quotes within 0.15 implied correlation; Q-vs-P test, m = 25%) | Robust score > 0, with VRP low, fragility rising and SKEW not extreme; ≤ 0.5% | T+0; hybrids take weeks | Green or Amber | Premium plus IM; hybrids may need an IA |
| **Opp · SELL** | Cut | Mandatory at the drawdown stop, on any L1–L3 breach, at DSR < 0.95, or at event-Red. At readiness-Red it is a priced recovery lever (C20). Otherwise cut if $\mathbb E[(1+\lambda^w)r^O]/\sigma^O<$ charges | T+0 listed or cleared; days for OTC | Crowding raises exit costs | Releases ≈$1bn of IM |
| **Opp · HOLD** | Keep | Within vol and IM budgets and L1–L3; DSR ≥ 0.95 at entry; trial ledger current | Monthly | Green, Amber | IM |
| **Opp · REFINANCE** | Compression, novation, clearing, CSA reallocation, non-cash collateral | $\tilde\mu\Delta IM-\text{cost}>0$, only if L1–L3 hold before **and** after; otherwise the saving is hidden short volatility | Weeks. Novation needs three parties; transfers need written consent (ISDA 2002 §7 [S]) | All | Frees IM |
| **Opp · LEVER** | Scale up | DSR ≥ 0.95 and $SR^{post}\sigma>$ financing $+\lambda_R\Delta\mathrm{CVaR}+\tilde\mu\Delta IM$; within budgets and L1–L3 | T+0 | Green, Amber | IM rises |
| **Beta · SELL** | Cut completion beta; reverse a P2S | Cushion-monotone hedge rule. $\tilde\mu$(avoided VM + IM) + CVaR relief − forgone ERP − tc > 0. Reverse a P2S when $\bar\ell$ falls below its break-even | T+0; a TRS ends per its confirmation | All | Releases IM |
| **Beta · HOLD** | Quarterly roll | The client pays s_lock; the Overlay bears realized basis | Quarterly | All | IM 4% → 10% |
| **Beta · REFINANCE** | Futures ↔ TRS ↔ ETF; term TRS; UST posted as IM | Δfinancing $+\tilde\mu\Delta IM-$ switching cost > 0. An index TRS carries ≈15% IM, against 4–10% on exchange | ISDA and FCM agreements | All | Changes the IM |
| **Beta · LEVER** | Completion beta; P2S (exposure-neutral; Public Markets' REFINANCE, Tier B); PE rebuild on the de-smoothed β | ERP − f − $\lambda_R\Delta$CVaR − $\lambda_{Lev}\Delta Lev$ − CLC > 0. Exposure ≤ 1.30× and monotone in the cushion; gross overlay ≤ 0.30W | T+0 | Green or Amber; P2S also at Red | IM plus contingent VM |

**Constraints.**
1. **Tail budget.** 0.15% ≤ B ≤ 0.50% of NAV a year. The floor changes only at the annual Board-approved budget. Moves within the band are Tier-A IC decisions, and terminating a layer needs a disclosed Tier-A record.
2. **L1–L3 always hold.** Named stresses are tested by full revaluation; the red team searches unnamed ones. The overlay stays net long VIX-equivalent vega in stress.
3. **Opportunistic book.** $\mathrm{ES}_{97.5}\le B^{opp}W$; IM ≤ $1.5bn; no additions in Red.
4. **Synthetic beta.** Economic exposure ≤ 1.30×; gross overlay ≤ 0.30W. Whether P2S counts toward 0.30W is for ADIC to confirm.
5. **Execution and collateral.** Listed first for the floor sleeve (no IM, φ = 0.85, no CSA consents). Each dealer ≤ 0.5% of NAV. Overlay IM counts toward the 15% / 20% encumbrance limits.

**The tail budget and the opportunistic book are one decision.** Through L1 and L2, moving the tail from the floor to the cap raises the opportunistic book's short VIX-vega allowance from ≈$1.0m to $3.4m per point, and its named-stress loss cap from $0.29bn to $0.98bn [I-calc].

**Collateral, which Corporate Finance owns.**
- **Charges and credits.** Margin is funded from CF's pool. The Overlay is *charged* for margin and for contingent collateral use via the contingent-liquidity charge (c_buf = 1.5% of stressed outflows; ≈27bp a year of notional on services). It is *credited* ex ante for tail value (§4.3).
- **Recognition.** φ = 1 for cash VM, 0.7 for OTC collateral with reuse rights and 0 for pledged collateral; listed option value counts at 0.85 in coverage ratios only. Posted IM is encumbered and excluded from the 8% test.
- **30-day need.** The larger of a through-the-cycle look-back (the P95 of 30-day net collateral flows over 2008, 2020, 2022 and 2025) and P99 VM + ΔIM. The FSB's ≥ 100% IM jump is a stress quantile, not a central case [C].
- **IM regimes.** Model both, because the US sovereign exclusion covers only central governments and their agencies [S]. Non-cleared IM is sticky: in March 2020 it "remained relatively stable" while cleared IM rose ≈$300bn [S]. Model a deferred IM step at each SIMM recalibration (≈6–12 months; +$0.25bn if one falls within the year) and keep VM stress binding.
- **CSA rule.** Govern offsets on economics first, then allocate trades to CSAs within dealer limits (≤ 0.5% of NAV per dealer; ≥ 5 dealers). The economic tests:
  - L1: overlay net vega ≥ 0.75× the tail sleeve's in named stresses;
  - L2: offset ratio ≤ 25%;
  - L3: a short-dated gamma budget.

  Until L1–L3 hold, a shared-CSA IM saving (31% in gap_03's example) is a hidden short-volatility position: SIMM read the books as offsetting while the short book lost $1.77 per $1 the sleeve gained in a 2020-type spike [I-calc].

**Services to other groups.** Services are booked to the client at FTP; the transfer-pricing convention is in §4.3.

| Client | Service | Rule |
|---|---|---|
| Total portfolio (TPA) | Completion beta, which equitizes Treasury cash | $10bn at t0 and in a do-nothing stress (economic exposure ≈0.97×), inside the 0.30W cap. TPA's stage rule runs $12.5 / 10 / 5 / 0bn from Green to Black (groups gap_04). Economic leverage stays in [1, 1.3], monotone in the cushion |
| Public Markets | P2S; rebalancing; portable-alpha and HF-TRS collateral | Tier B; the Overlay executes and CF funds VM; exposure is kept in simulation; VM is contingent ($1.65bn on $5bn in a −33% month). The +$5bn Red tranche is booked to Public Markets *with* its sale proceeds, netting +$2.74bn over the S1 year. Counts against the 1.30× exposure cap; the 0.30W treatment is for ADIC to confirm. Collateral is HQLA only |
| TPA, after PE pacing cuts | Futures rebuild of forgone vintage beta | Booked to TPA, not PE: pacing is a CIO/IC decision and κ^GP already prices the forgone vintage, so charging PE would double count. Sized on the engine's de-smoothed cash-flow β, never a transaction β; basis risk disclosed |
| Co-investment, Private Credit | Index-futures and CDX hedges | The same β discipline. The client keeps the risk-charge relief and the *hedge basis* (instrument against its private exposure); the Overlay keeps the *implementation basis* (roll, financing against the lock, on-the-run against reference). A group hedge proceeds only if its total-portfolio score is positive |

**Liability-aware hedging.**
- **The liability.** The owner's draw is a NAV-scaled vertical put spread on fiscal need: the 5% floor above ≈$67 Brent and the 10% cap below ≈$23 on the linear map (≈$64/$31 on the log map), with ≈$200m of draw per $1/bbl [I-calc]. Equity-only hedges miss the supply-glut and Gulf-war stresses, the likeliest in 2027–29.
- **Coverage by shock type.** The 12-month stressed DCR must be ≥ 1.0 (hard) and ≥ 1.25 (green) for demand bust, Gulf war, and supply glut with peg stress.
- **Oil put spreads**, if permitted: at the published kinks; 1–2-year strips; sized in spot-equivalent (front-month) delta, never notional. At the 15-Oct-2026 strip, 20–40m bbl of notional carries ≈1.1–3.1m bbl of delta (≈3.4–7.6m in the SG and DB states). Set that against the ≈22m bbl first-year draw delta from today (≈56m if in band; not ≈100m) and the ≈21–27m bbl asset-side delta on the total-portfolio oil ledger (`addenda/ra_gap_03.md`) [I-calc, SYNTHETIC]. No short calls in a Gulf-war state.
- **Joint-state hybrids** only after ≥ 3 dealer quotes with implied correlations within 0.15, and a Q-vs-P test $P^Q(\text{joint down})<(1-m)P^{P,adj}$ with m = 25% [I].
- **Valuation.** Hedges are valued by carry + liquidity value + enabling value, never standalone return. The convex floor is 0.15% of NAV a year, IC-owned, rising toward 0.5% only when the robust marginal value is positive. At t0 the budget sits at the floor: SKEW at 168.6 fails the scale-up test, and the E1 score is negative.

**Forecasts and bias.**
- **Tail book.** Payoffs are filed by named scenario. (VaR, ES) are scored jointly [S: Fissler–Ziegel]. Bias prior: carry understated 30%, crisis payoff overstated 20%.
- **Opportunistic book.** Families are exposure templates: premia live in the scenario engine, skill in a residual α. The Sharpe prior is N(0.3, 0.25²), and a strategy needs a deflated Sharpe ratio ≥ 0.95: an 8-year backtest Sharpe of 1.0 shrinks to 0.50 and fails at a DSR of 0.86 [C]. The full list of variants ever tested is required data.

**Synthetic defaults.**
- **Policy book, drawn from the budget:** a floor ladder of $7.1bn (3M $1.6bn, 6M $3.4bn, 12M $2.1bn), listed first; $10bn of completion beta; $1.0bn of opportunistic IM (vol ≈1.0–1.2% of NAV) within a $1.5bn budget.
- **Engine-test fixture:** the ≈250-trade blotter on 12 CSA archetypes, used for gap_03's tests T1–T6 only:
  - a tail stack of ≈70 trades and ≈$25bn: put spreads, VIX calls, CDX, Brent put spreads;
  - an opportunistic book of ≈150 trades and ≈$45bn of notional: trend, FX carry, rates RV, short volatility;
  - ≈30 synthetic-beta trades.

  At ≈0.53% of NAV the fixture's tail stack is above the cap, so its premium is rescaled to the budget in decision runs.
- Both IM regimes; two GCC dealers carrying wrong-way risk.

**Reconciled sizing** (groups gap_03 §5) [I-calc; SYNTHETIC].

| Item | v1.0 | Reconciled base (t0) | Band or stress |
|---|---|---|---|
| Tail premium | 0.4% (cash map); 0.15% floor (§3.7) | **0.15%, $0.27bn** | 0.15–0.50% ($0.27–0.89bn); moves are Tier A |
| Tail notional (90/72) | $20bn; ≈$25bn | **$7.1bn** (6.7–7.6) | $23.6bn at the cap (22.4–25.5) |
| S1 tail payoff; L2 cap on opportunistic loss | $3.5bn; none | $1.18bn; $0.29bn | $3.92bn; $0.98bn at the cap |
| Tail IM | — | $0 listed; $0.19bn OTC under UMR | $0.62bn OTC at the cap |
| Synthetic beta | $0–10bn; $10bn at t0, $15bn in stress | **$10bn of TPA completion**; economic exposure ≈0.97× | $10bn in a do-nothing stress. A +$5bn P2S is a Public Markets Red lever, booked *with* its proceeds |
| Opportunistic | ≈$1bn IM; vol 1.0–1.5% | **IM $1.0bn** (vol ≈1.0–1.2%); budget $1.5bn | +$0.5bn cleared-IM step in stress; +$0.25bn if a SIMM recalibration falls within the year |

*SYNTHETIC – NOT ADIC DATA.*

### 3.8 Interactions by group

| Group | Gives to other groups | Depends on |
|---|---|---|
| PE funds | Co-investment deal flow (§4.7); look-through exposure for Capital Solutions and Private Credit; SELL candidates (zero liquidity if sold internally) | Secondaries' price forecasts; Capital Solutions' reserve quotes; Overlay beta replacement; CF facilities |
| Secondaries | External-price forecasts for PE SELL; counter-cyclical deployment | Tier-1 headroom, which needs committed facilities or the band (§4.5); PE rotation; LP-level facilities |
| Capital Solutions | Reserve-price quotes for REFINANCE; contractual cash | PE distributions, which repay its NAV loans (wrong-way); look-through exposure |
| Co-investment | Shared-GP information (ρ_GP 0.6) for PE forecasts | PE commitments; recap netting with Private Credit; Overlay hedges |
| Public Markets | The liquidity reservoir (TP tier); beta for P2S | Overlay execution; CF funding of VM; HQLA for portable alpha |
| Private Credit | Contractual cash; SMA run-off and loan sales as early Amber rungs | Shared sponsors with PE and Co-investment; CF facilities |
| Overlay | Synthetic beta, P2S and rebalancing, booked to clients at FTP (exposure and liquidity to the client, execution and basis to the Overlay, funding to CF); tail cash, credited to the Overlay and supplementary to contingent budgets, never ring-fenced for them | CF collateral pool (charged the CLC, credited ex ante for tail value) |

---

## 4. Cross-group mechanisms

### 4.1 Netting of internal transfers

**Rule.** Liquidity raised is external cash only.
- The ladder flags every position's counterparty as external or intra-ADIC and counts intra-ADIC flows at zero.
- Both legs are booked at fair value, and any wedge goes to a centre line. Without this, a $1bn transfer at 85% against a 90% fair value would create $50m of fake alpha [I-calc].
- Synthetic-data gate V2 checks that intra-ADIC transfers net to zero. It runs on DVA ledgers as well as on cash, because a naive booking of Overlay services nets to zero in cash yet double counts −$7.05bn of value in S1 (§4.3).

| Transfer | Liquidity raised | Pricing evidence | Approval |
|---|---|---|---|
| PE stake sold to Secondaries | Zero, minus fees | A ≥ 20% third-party strip or ≥ 2 external bids; a fairness opinion if ≥ $250m or conflicted | Tier B or A |
| Capital Solutions lends against an ADIC co-investment | Zero unless refinanced externally | External quote or margin band; uses the leverage budget | Tier B |
| Capital Solutions lends to a GP fund in which PE is an LP | −L(1 − s), with s ADIC's LP share | ≥ 50% external syndication or a third-party quote | Tier A |
| P2S of long-only | Real: proceeds minus stressed IM/VM | Market | Tier B |

**Governance.** A group that may bid cannot quote (firewall); no transfers within 30 days of a measurement date (blackout); every transfer must show a net total-portfolio benefit. Rule 17a-7, ERISA §408(b)(19) and FRA §23B cover only quoted securities [S], so strips and outside bids are the primary market test [C].

### 4.2 In-house pricing desks with conflict controls

- **Secondaries desk.** It registers distributions of *external* clearing prices for ADIC's PE holdings, scored against later prints and against a consensus-only benchmark. It never sets the reference quote on a deal it may bid for.
- **Capital Solutions quote function.** It produces a reserve price, never a transaction price. Controls:
  - financings need ≥ 3 RFQs;
  - sales need ≥ 2 external bids or a ≥ 20% third-party strip;
  - internal participation is capped at 20% and counted at zero;
  - information barriers separate the desks;
  - the pricing committee, owned by CF, decides.

  Anchoring is costly: each 10% internal anchor removes 10% of external liquidity, so $3bn becomes $2.4bn at 20% [I-calc].
- **Records.** Quotes land in the `quote` table with a conflict flag.

### 4.3 Liquidity and risk transfer prices from the optimizer's duals

**Decision price** per $ of holding or proposal:

$$\text{charge}_i=\sum_{h,s}\mu_{h,s}a^{h,s}_i+\lambda_R\frac{\partial\mathrm{CVaR}}{\partial x_i}+\lambda_{Lev}b_i+\sum_k\rho_k\Delta\mathrm{Floor}^k_i-\sum_{h,s}\mu_{h,s}c^{h,s}_i$$

- **μ are robust duals from H, and only from a feasible problem.**
  - HQLA and borrowing are decisions. Once a row is restorable, the KKT conditions cap μ at the cheapest *spare* lever per unit of headroom: $\sum_h\mu_hs_{\ell h}+y_{IG}\iota_\ell\le c_\ell$ for every lever below its cap (groups gap_01 §2.3). A Treasury top-up therefore caps μ at 25% PV per $ of month-24 headroom, not at 1.5% a year, because it relieves only 0.30 per $.
  - There is no floor [C]. Zero duals in every scenario signal an oversized buffer, not free liquidity.
  - **Violated rows never price.** An elastic row left violated at the solution (u > 0) prices at its penalty tier, y\* = M (gap_02 §4). The synthetic book fails T4′ by $11.3bn at t0 with nothing signed, so pricing the current book would pin μ. Duals, FTP and hurdles come instead from the Phase-II restored problem (§4.8), and every card carries `priced_on`. `test_no_pinned_duals_groups.py` (18/18) refuses cards and envelopes from a pinned solve or a reverse stress.
- **Which Tier-1 level is priced** (groups gap_04 §5, a reduced H under Mix B, pooled M1–M5).
  - At tolerance the liquidity and T4′ duals are zero, and FTP is a pure risk charge (λ_R 0.36–0.42): PE 136bp per NAV-year, Secondaries 71, Capital Solutions 138, Co-investment 306, Private Credit 94. That is an oversized buffer once the band exists, not free liquidity.
  - At the CFP-Green appetite (T + P only) the T4′ dual is 0.046–0.051 per $ of headroom. FTP rises to 135–201bp, of which the liquidity component is ≈100–185bp (PE ≈155), and PE's net α\* shrinks to ≈20bp per NAV-year. Mix A is infeasible at appetite (headroom −$0.05bn, consistent with its +$0.0bn without the revolver in §2.4).
  - FTP is published at both levels, with envelope ranges across replications. The IC states which level it prices [I-calc].
- **Tenor:** $\ell_{s,t}=\mu_{s,t}/(\pi_{s,t}-\mu_{s,t})$, charged on each asset's cash-weighted life [S: CEBS]. The published FTP curve is an EWMA with a 2-quarter half-life and a ±50% collar.
- **Performance charges** are vintage-locked, and CF holds the mismatch. The contingent-liquidity charge is $CLC_g=c_{buf}\sum_h\omega_hO^{stress}_{g,h}$:
  - c_buf = 1.5% (range 1–3%), giving ≈$0.2bn a year ($0.1–0.5bn) [I-calc];
  - it is charged once per price set [C];
  - Private Credit and Capital Solutions earn c_buf on stressed inflows, and the Overlay is credited ex ante for tail value (below).
- **Illustration** (G8, unfloored) [I-calc]: duals of 1.83% (crisis-liquidity row) and 0.81% (CVaR) give group charges of 58–212bp. Private Credit's net α* of −41bp earns a zero budget. The tail hedge would need a 10.85% dual to pay its carry, so hedges are valued by liquidity and enabling value instead (main L5). For the synthetic book at t0, groups gap_01's restored-problem table (§4.8) supersedes this illustration.
- **Services transfer pricing** (groups gap_03 §3). For an Overlay service j with notional N, reference return $r_B$, realized financing basis $b_t$ and a lock $s^{lock}$ set at each roll:

  | Line | Client group | Overlay | CF |
  |---|---|---|---|
  | Exposure pass-through | $+Nr_B$ | $-Nr_B$ | |
  | Locked financing | $-N(r_f+s^{lock})$ | $+N(r_f+s^{lock})$ | |
  | Deposit interest (funded services) | $+Nr_f$ | | $-Nr_f$ |
  | Contingent-liquidity charge, $CLC_j=c_{buf}\sum_h\omega_hO^{stress}_{j,h}$ | $-CLC$ | | $+CLC$ |
  | Credit on cash released (P2S), at FTP | $+LPC$ | | $-LPC$ |
  | External: VM and execution | | $N(r_B-r_f-b_t)-TC$ | |
  | External: interest on collateral cash | | | $+r_fC_t$ |
  | **Net** | $N(r_B-s^{lock})-CLC+LPC$ | $N(s^{lock}-b_t)-TC$ | $CLC-LPC$ |

  - The client bears exposure and the liquidity charge, the Overlay bears execution and basis, and CF bears funding.
  - On a test book ($10bn completion, $5bn P2S, $1bn PE rebuild, a −$1bn co-investment hedge, $1bn of CDX HY protection), internal transfers net to zero and entity P&Ls equal external P&L at machine precision, on the benign path, the S1 path and 2,000 Student-t paths. On S1 both sides are −$7.671bn.
  - The naive booking (the client keeps its "as if physical" benchmark; the Overlay keeps the VM) double counts −$7.05bn on S1 and +$0.88bn on the benign path. **Gate V2 therefore runs on DVA ledgers, not only on cash** [I-calc].
- **Tail credit, ex ante** (groups gap_03 §4). For each live rung j, with premium $P_j$, coverage period $\tau_j$ and duals vintage-locked at purchase:

  $$DVA^{tail}_t=\sum_{j\ \text{live}}(A_j-P_j)\frac{\Delta t}{\tau_j}+w\,E_t,\qquad A_j=KV_j+LV_j+EV_j$$

  - KV is the market-kernel value of the payoffs, LV is $\sum\tilde\mu\,\varphi\,\Delta X$, EV is $\sum_k\eta_k\Delta\mathrm{slack}_k$ over T3, T6, T8 and the Tier-1B floor, and $E_t$ is experience.
  - The reference ladder's accrual and all experience go to the TPA policy line, which the IC owns. The desk books implementation against the reference ladder, and w = 0 in pay.
  - At the floor, KV is 0.55 per $ of premium and LV/EV 0.067–0.090. That leaves a predictable IC policy residual of ≈−$96m a year (−36% of premium; −$319m at the cap). The residual is the unmodelled EV the IC must believe in to hold the floor, measured on common random numbers. Where EV falls short, the floor is an explicit premium against model misspecification [S: Drechsler 2013].
  - The fatigue replay (floor ladder, 2010–25) shows why ex-post crediting fails: negative annual DVA in 11 of 16 years with a 3×-premium/VIX-35 exit rule, including a four-year run (2021–24) and a drawdown of 6.2 years of budget. Held to expiry, it is negative in 16 of 16 years [I-calc]. Peers agree: CalPERS's tail programme "did not have a customized benchmark" before it was cut in 2019; NZ Super and CPP judge completion portfolios on implementation [S].
- **Attribution** is in dollars:

  $$NAV_0(R_P-R_{RP})=\sum_gDVA_g+DVA_{TPA}+DVA_{CF}+\text{residual}$$

  with $DVA_g=\sum_{i\in g}NAV_i(r_i-r^{FB}_i)-FTP^{vint}_g-\lambda_RRC_g+CR_g$.
  - *Real Assets (patch, ra_gap_01 §5):* $NAV_i$ is the RAME nowcast $V^*_i$ and $r^{FB}_i$ uses desmoothed betas re-levered on the actual debt path. Reported-NAV DVA is disclosed but never paid: on the canonical T4′ path it shows +$0.6bn in year 1 against −$3.8bn on $V^*$, and reverses in year 2.
- **Shapley protocol** (groups gap_04 §6).
  - Interactions are split by Shapley values over nine players (the seven groups, TPA and CF) on common random numbers. The baseline is a defined group-off book: HOLD plus plan pacing, with no facilities, band, notices, P2S, run-off, contingent budgets or amber sales; forced sales remain.
  - *Ten players with Real Assets (patch, ra_gap_01 §6):* 2¹⁰ = 1,024 coalitions. Real Assets' group-off baseline is HOLD plus plan pacing ($1.2bn a year) with no open-end notices, JV sell-downs, cash-outs or ENR SELL; cures are paid under the declared ϖ = 1 and forced RA sales remain. Exact values (M1 / M4 / M6, Mix B): Real Assets −2.3 / −4.3 / −5.2pp of P(red) and +$0.26 / 0.50 / 1.09bn of CE, fourth of ten on both; P = 32 covers the exact value 90–98% of the time.
  - Exact values need all 2⁹ = 512 coalitions. That is affordable when each coalition is a policy simulation: 54 minutes on 22 cores for six models.
  - When each coalition needs an H re-solve, main §4.11 applies: exact over ≤ 6 action groups, otherwise antithetic permutation sampling with P ≥ 32 (258 evaluations), reporting path and permutation errors. P = 32 covered the exact value 90–99% of the time for the worst-covered player; P = 16 covered 82–95%.
  - Stand-alone attribution is wrong by more than the effect, with index values of 0.7–2.6, because liquidity levers substitute for one another [I-calc].

### 4.4 Group budgets as optimizer outputs

- **Envelopes.** $\Lambda^k_g=\sum_{i\in g}a^k_i(x^*)$ for each coupling row (liquidity by horizon and scenario, CVaR, leverage, pacing).
  - They come from the Phase-II restored problem, never from a pinned or reverse-stress solve. They are pooled across sample-average-approximation replications and reported with ranges and `priced_on`.
  - In RECOVERY the envelope is $B^{rec}_{g,t}=\Lambda_g(x^*)+\varphi_{g,t}\,g_t$: the Phase-II envelope plus the group's share of the tolerated deficit (§4.8).
  - Liquidity envelopes obey the L4 pool row on the binding horizons (§2.4): $\sum_gB_{g,h}+B_{\mathrm{OVL},h}\le\mathrm{Pool}_h$, h ∈ {12, 24}.
- **Elasticity.** Each group sees its budget elasticity $1/H_g$. Coupling makes a deviation 1.1–3.5× costlier than the group's own curvature implies [I-calc].
- **Bands.** Bands are free for releases only [C]. Increases on binding rows pay the dual, with $\sum_ga^k_g\delta^+_g\le\text{slack}_k$; no free band exceeds the Tier-A size (≈$0.44bn); up to +20% above the envelope is Tier B, beyond that Tier A; there is no ratchet [S: Weitzman 1980].
- **Contingent pacing.** $P_{g,t}=P^*_g\,\Pi_{[m^{lo},m^{hi}]}(1-\eta_g(\ell_t-\bar\ell)/\bar\ell)$, with η > 0 for PE and Co-investment and η < 0 for Secondaries and Capital Solutions. Negative η acts only while the §4.5 gate is open (Tier 1 green), and those budgets are sized to T4′ headroom.
- **Quantities lead while T4′ is slack.**
  - Under the certified mixes T4′ goes slack and its dual falls to ≈0. The binding price becomes T6's, which H must carry through its 12-quarter CVaR surrogate under the same guard (an open item).
  - Until then the pacing corridor comes from P: Mix A's base pacing gives PE $3.6bn a year, Mix B's $7.2bn. T4′ prices act as a floor (Baumol–Fabian).
  - In the reduced H, at tolerance under Mix B, envelopes are PE $6.75bn, Secondaries $2.40bn (cap), Capital Solutions $1.80bn, Co-investment $0.99bn and Private Credit $2.11bn for year 1, with a protected PE sleeve of ≥ $1.8bn [I-calc, groups gap_04 §5].

### 4.5 Option value of dry powder

- **The hurdle.** Counter-cyclical deployment clears only if its IRR beats ≈(1 + r_h)(1 + ℓ̄) − 1 over the capital outstanding: 13.3% vs 8.3% for structured equity, and 14.9% vs 8.1% for a drought NAV loan, at the fallback ℓ vs a 1.83% dual [I-calc].
- **No idle reserve.** Hold no reserve while $p_S\mathbb E[(NPV_S-L_S)^+]$ ≤ carry + forgone NPV [C]. At the 9/9/4 fallback, no idle reserve pays.
- **Contingent budgets, not fixed deployment.**
  - Secondaries buying, Capital Solutions new money and credit-secondary purchases have no fixed deployment default.
  - **Gate** (redesigned, groups gap_04 §4.3): the desk's discount forecast d̂ > 20%, confirmed by a second reading or an external print, ∧ Tier 1 green (usable IG + cash ≥ 8%, LCR30 ≥ 1, SH_TPF ≥ 24 months with facilities at 80%), in any stage but Black. v1.0's extra stage condition (Green or Amber) changes nothing, because Tier 1 is what binds.
  - **Size:** min(budget, T4′ headroom less a buffer), re-testing T4′ after deployment.
  - The value enters H as contingent columns, with no separate liquidity-value term.
- **What the gate is worth** [I-calc; census v1.0; 10,000 paths per model, paired on common random numbers].
  - The discount itself is common: d̂ exceeds 20% in 15–22% of quarters under every policy, and desk noise adds 2–3pp of false triggers.
  - On the do-nothing book the trigger fires in only 0.1–1.2% of quarters (2–17% of paths over five years). Tier 1 fails in 92–99.5% of hot quarters, mostly because T4′ survival with facilities is below 24 months.
  - Under Mix A or Mix B it fires in 71–87% of paths. It adds $0.62–0.81bn (Mix A) or $0.17–0.37bn (Mix B) of five-year expected wealth at no measurable P(red) cost: 15–22¢ per $ deployed at θ = 0.92, 0.5–9¢ at θ = 0.75. Deployment discounts average 23–29%.
  - Gating on Tier 1 alone, in any stage but Black, adds $0.2–0.4bn over the v1.0 gate under Mix A.
  - **Without committed facilities or the band, the franchise hedge does not exist.**
- **Funding.** Fund opportunity budgets from general liquidity. Tail cash is credited to the Overlay and never ring-fenced.
  - It is too small: $1.5–1.8bn per crisis path, under half of one year's $3.9bn budget. Early monetization moves cash forward but does not raise it.
  - Ring-fencing it backfires: deploying it in Red raises P(red) by 0.2–0.9pp on the do-nothing book. ADIC becomes its own sidelined natural buyer, the fire-sale mechanism of Shleifer & Vishny (2011). Liquidity held to buy fire-sold assets pays only for institutions that come through the crisis with spare liquidity (Acharya, Shin & Yorulmazer 2011), and ADIC's spare liquidity is Tier-1 headroom. Cash-in-the-market pricing (Allen & Gale 1994) is why discounts peak when cash is scarcest [S].
- **Evidence is mixed, so treat these as priors.**
  - In Böni–Manigart (Table 5), funds launched when ex-ante BB credit spreads are higher earn higher net multiples and beat IG and HY bond benchmarks; the IRR coefficient is positive but insignificant. A higher ex-ante TED spread (funding illiquidity) lowers outperformance, an effect more than twice the size of persistence [S] [corrected 2026-10-18: the spread effect is not significant for IRR].
  - EFW find net risk-adjusted alpha of ≈0 [S].
  - Credit secondaries are currently a seller's market [C].

### 4.6 Natural hedges between groups: real and false

| Pair | Channel | Verdict | Treatment |
|---|---|---|---|
| Capital Solutions and Private Credit cash vs PE DPI | NAV loans repay from distributions; PIK switches; DDTL draws in stress | False: cash co-moves (prior b > 0) | Hedge regression on ADIC data; no Tier-1 credit until b < 0 at 90% |
| SMA run-off vs PE DPI | Principal return that ADIC controls | Partial real hedge, ≈$0.8–0.9bn | Counted at the P05 of a stochastic-CPR simulation |
| Secondaries / Capital Solutions opportunity vs ADIC liquidity | Discounts and structured yields widen as liquidity tightens | Real *franchise* hedge, not a liquidity hedge, and real only with Tier-1 headroom | ℓ-conditional budgets (η_g < 0) behind the §4.5 gate |
| Trend and macro vs equity | Convex in gap crashes (CTA +14.09% in 2008, +7.13% in 2022 [S]); weak in grinds (composite loss ratio 0.23 in 2022 [S]) | Partial | Defensive stack |
| Tail hedge vs deployment | Monetization pays when discounts are widest | Real only with Tier-1 headroom | Tail cash of ≈$1.5–1.8bn per crisis path is supplementary and never ring-fenced (§4.5) |
| Recap: co-investment equity vs ADIC credit in the same company | Value moves from ADIC's credit to its equity | Internal | Recap cash netted against ADIC's own credit claims; one draw per company (V24a). ≈7 co-investments carry an ADIC PC loan; recap dividends total $0.5–0.7bn over five years, 12% of them funded by ADIC's own credit [I-calc] |

### 4.7 Co-investment flow depends on primary commitments

Offered flow follows past PE commitments:

$$O_t=\theta\sum_{k=0}^4d_kC_{t-k}$$

with d = 0.15/0.25/0.25/0.20/0.15. θ = 0.33 is Bain's GP-level median, used here at LP level [I], and acceptance a is 0.3–0.6 [I]. The flow is computed from lagged commitments, not from a steady-state pace. On the proposed census v1.1 the $C_{t-k}$ come from the sealed vintage history (groups gap_02 §2) [I-calc]:

| Case | Accepted flow ($bn a year) |
|---|---|
| 2026, sealed v1.1 (offered $1.98bn) | 0.60–1.19 |
| 2027, pace held | 0.57–1.13 |
| 2027, after a 2027 pause | 0.49–0.97 |
| 2028, after a 2027 pause | 0.41–0.83 |
| 2026, v1.0 reproduction history | 0.93–1.85 |
| 2026, 20%-growth history | 1.09–2.18 |

*SYNTHETIC – NOT ADIC DATA.* The steady-state shortcut θ·C·a remains a cross-check: 0.50–1.01 at $5.1bn, 0.71–1.43 at $7.2bn and 0.99–1.98 at $10bn.

Sustaining an $18bn book needs ≈$3bn a year (G4), which would take a PE pace of $15–30bn [I-calc]. Four consequences follow:
1. **The book is not self-sustaining.** No V6-compliant PE history makes the synthetic co-investment book self-sustaining. Sourcing must extend beyond ADIC's fund GPs, or the book shrinks; the offer log by GP shows which.
2. **PE pacing cuts reach co-investment.** A PE cut reduces co-investment flow with a 1–5-year lag, so κ^GP includes the lost flow: θa = 0.149 of co-investment per PE dollar forgone, worth 2.12¢ in M1 (§3.1). Simulated jointly on census v1.0 (groups gap_04), accepted flow falls from $1.3bn a year to $0.4–0.5bn by year 5 under Mix A, and to $0.7–0.9bn under Mix B. In the engine acceptance a comes from the offer log (0.45 in the prototype).
3. **Deal flow is procyclical.** Co-investment TVPI correlates −0.59 with fund commitments [S], hence the vintage budget.
4. **Errors are shared.** The shared GP effect (ρ_GP 0.6) correlates PE and co-investment forecast errors, so the FBE's group-bias shock is shared too. It applies only to holdings that share a GP on the overlap graph (V24d). In groups gap_04, GP effects are drawn once per path and shared by PE and co-investment, which sets their correlation at ≈0.6.

### 4.8 Group RECOVERY mode: feasibility before prices

**Why the group layer needs it** (groups gap_01 §2–3). At t0 the book fails the T4′ hard row by $d_0=\max(0,-\min_h\mathrm{hd}_h(x_0))=\$11.3$bn: nothing is signed, and the 8% top-up is not done. Priced as it stands, with the deficit carried as elastic slack, the row would price at its penalty tier (§4.3). The group layer therefore runs gap_02's two-phase recovery mode, resolved by group. Phase I separates a structural deficit (none on T4′) from an execution deficit; Phase II prices the restored problem.

**Phase I over group-tagged reversible levers.** A linearised H block has monthly T + P + F rows (h = 1…24) under s\*(θ\*) and the t0 T2 row:

$$\mathrm{hd}_h(x,q)=\mathrm{hd}^0_h+\textstyle\sum_\ell s_{\ell h}x_\ell+\sum_c s_{ch}q_c\ \ge -r_S,\qquad \sum_\ell \iota_\ell x_\ell+\sum_c b_cq_c\ \ge\ 0.08W_0-U_0\ (=\$0.56\text{bn})-r_{IG}$$

- Slopes s come from finite differences on the replica. q are SELL cards for PE, Secondaries, Co-investment and hedge-fund lots, at bid b and a hold value of 0.95.
- A shared-sleeve row requires $x_{sell}+x_{ro}\le\$5.6$bn, so run-off and SMA sales cannot use the same loans. EBA/GL/2023/06 ¶30 makes the same demand for mutually exclusive recovery options [S].
- Phase I is gap_02's lexicographic minimum violation: $u^\*=\min u$ s.t. $\mathrm{hd}_h+u\ge0\ \forall h$, with x restricted to the levers available in the state and **q = 0**, so recovery never presumes a fire sale; then the same for IG.
- The lever catalogue and its costs per dollar of headroom are in §2.3.

**u\* by state** ($bn) [I-calc; SYNTHETIC].

| Reading | R0x: group levers only | R0: + Treasury top-up | R1: + revolver (Mode B) | R2: + band (Mode H) |
|---|---|---|---|---|
| **T4′ = s\*(0.76)** | **0** | **0** | **0** | **0** |
| Literal T4 (reverse) | 1.65 | 0 | 0 | 0 |
| Critic reading (reverse) | 30.1 | 26.4 | 19.0 | 2.65 |

- **No structural recovery on T4′.** Its irreducible infeasible subsystem (IIS) is empty.
- For the critic reading in R1, the IIS names levers by owning group: the T4′ row at month 24; every PE, Co-investment, Secondaries, PC and CS pacing lever at capacity; the SMA sleeve; CS syndication; Overlay IM; the Treasury top-up; the revolver at $15bn; and the band unavailable.

**Execution deficit, glide path and group shares.** Recovery has a structural part, u\*, owned by CF and the Board through the band request and Board sign-off (zero on T4′). It also has an execution part, $d_0-u^\*$, delivered on a glide path:

$$g_t=d_0\,(1-t/T_{rec})^+,\quad T_{rec}=4\text{ quarters};\qquad e_t=d_0-g_t-R^{CF}_t;\qquad \varphi_{g,t}=\frac{\sum_{\ell\in\mathcal L_g}s_{\ell,24}\,x^{(t)}_\ell}{\sum_{\ell}s_{\ell,24}\,x^{(t)}_\ell}$$

- $R^{CF}_t$ is the relief from CF levers signed by t. $x^{(t)}$ is the least-cost solution at t over the reversible group levers, with no sales. $\varphi_{g,t}$ is group g's share of the interim deficit $e_t$.
- gap_02's T_rec of 4 quarters (8 with Board approval) is longer than the 6 months over which EBA/GL/2023/06 accumulates liquidity recovery capacity [S]. Hence the quarterly progress test, which withdraws the glide path if it fails.
- **RECOVERY envelopes** are $B^{rec}_{g,t}=\Lambda_g(x^\*)+\varphi_{g,t}\,g_t$. The tolerance covers the legacy book only; new deployment pays the terminal Phase-II price. A group behind its delivery schedule loses envelope one for one, or buys it back at the dual.
- **Synthetic result** [I-calc], assuming the revolver signs at t = 2 quarters [I]:
  - In Q1 the groups must deliver $e_1$ = $2.8bn. A co-investment pause of 82% of flow supplies 56%, and PC run-off with its contingent budget off supplies 44%. The interim price is 12.3% PV.
  - From Q2 the revolver carries the deficit (φ_CF = 96%), and PC's $0.58bn SMA sale restores the 8% T2 target (φ_PC = 4%). The interim levers are then released.
  - If the revolver never signed, reversible group levers alone would still close T4′ by T_rec, at a marginal price of 69% PV. That takes every pacing lever and the Treasury top-up at capacity, plus a partial opportunistic de-risk. With SMA and CS sales admitted (R0) the price is 24%.

**Phase II: duals, FTP and hurdles only from the restored problem.** Maximize $\sum_c(b_c-h_c)q_c-\sum_\ell c_\ell x_\ell$ subject to hard rows relaxed by u\* only, with sales re-admitted. The duals are μ_h ≥ 0 and y_IG ≥ 0:

$$y_{cash}=\textstyle\sum_h\mu_h\kappa_h+y_{IG},\qquad p^\*_c=\dfrac{h_c-\sum_h\mu_h\rho_{ch}}{1+y_{cash}}\ \ (\text{SELL iff }b_c\ge p^\*_c)$$

$$\phi^{new}_g=\textstyle\sum_h\mu_h a_{gh}+y_{IG}\mathbb 1_{g=\text{Co}},\qquad \text{hurdle}_g=\phi^{new}_g/D_g,\qquad \text{FTP}^{hold}_g=\sum_h\mu_h\,\mathrm{NCO}_g(h)/(5\,\mathrm{NAV}_g)$$

- κ₂₄ = 0.825: a dollar of t0 cash buys only $0.83 of month-24 headroom, because the year-2 draw and the 4% floor are NAV-linked.
- ρ is group-specific relief beyond the proceeds; for PE, the buyer assumes 0.53 of unfunded per $ of NAV (census v1.0). a_g is the headroom consumed by $1 of new commitment.

**t0 envelopes, charges and hurdles by group** (groups gap_01 §3). Both states are `priced_on: restored_problem`, with recovery-target hashes R1 `684473e1b79d4f75` and R0 `95b61fae526726ba`. Brackets give the range across 10 SAA replications of θ\* (M6, 50k paths each; θ\* 0.76–0.81).

| Group | 24-month envelope B_g, $bn: R1 [SAA] / R0 | Pacing in stress, $bn a year: R1 / R0 | FTP on holdings, bp a year: R1 / R0 | Hurdle on new deployment, bp a year of α\*: R1 [SAA] / R0 [SAA] | Card or lever at t0: R1 / R0 |
|---|---|---|---|---|---|
| PE | 20.9 [20.9–21.4] / 17.6 | 7.2 / 1.8 | 9 / 164 | 14 [14–14] / 299 [299–303] | HOLD 90.7% / SELL 70.6% |
| Secondaries | 3.5 [3.5–3.6] / 3.4 | 1.2 / 1.2 | 6 / 119 | 20 [20–21] / 439 [439–445] | HOLD 90.9% / SELL 75.2% |
| Co-investment | 3.0 [3.0–3.1] / 0.9 | 1.2 / 0 | 4 / 25 | 96\* [96–97] / 498 [498–499] | HOLD 91.0% / HOLD 76.1% (bid 75%) |
| Capital Solutions | 0.53 [0.53–0.55] / 0.54 | 1.2 / 1.2 | 1.5 / 33 | 16 [16–16] / 349 [349–353] | — / syndicate $0.34bn |
| Private Credit | 0.85 [0.85–0.88] / 1.03 | 1.2 / 0 | 1.4 / 36 | 21 [21–21] / 450 [450–455] | SMA sale $0.58bn / $5.6bn |
| Public Markets | CBC_TP(24m) contribution 40.6 | — | — | — | HF secondary HOLD 91.9% / 93.6% |
| Overlay | 1.3 (net use) | — | — | — | IM release unused |
| CF | Revolver $13.6bn [13.6–14.8] | — | — | — | Glide share 96% / 0% |
| **Duals** | μ: R1 0.0113 [flat]; R0 0.243 [0.242–0.243]. y_IG: R1 0.033; R0 0 | | | | |

*SYNTHETIC – NOT ADIC DATA.* R1 has the revolver signed; R0 has group levers plus the Treasury top-up. \* Co-investment deploys cash at t0, so it also pays the T2 dual. In H's multi-period form, every group's calls pay the T2 dual of the quarter in which they land.

- **R1 prices are flat at revolver carry**, ≈23bp a year per $ of month-24 headroom, while the revolver has spare capacity. That holds in all ten SAA replications (revolver $13.6–14.8bn).
- **θ = 0.82 is a signpost.** There the $15bn market cap binds, and μ jumps four- to five-fold, to SMA run-off and sales at 4.8–5.5% PV.
- **Prices depend on whether the revolver exists.** Before it is signed, $1 of month-24 headroom is worth 24% PV, group hurdles are 3.0–5.0% a year, and a 2018 buyout fund at 88% is a SELL. With it signed, the figures are 1.1%, 0.13–0.97% and HOLD (reservation price 90.7%).
- **Penalty-pinned duals still appear on reverse stresses.** The critic reading pins μ at the penalty tier (100, or 1,000 at ten times the tier). Every group's SELL card then fires, and the PE card's reservation price is *negative*.

**Test extension.** `test_no_pinned_duals_groups.py` runs seven checks (18 tests):
1. pinned group cards are caught (μ = M scales with M; every card says SELL below 2%; envelopes refused);
2. restored-problem duals, cards, envelopes, FTP, hurdles and glide shares are invariant to ten times the penalty tiers, with reservation prices above 60%;
3. reverse stresses never price;
4. the KKT spare-lever cap holds;
5. the Phase-I closed form holds, and the IIS names levers by owning group;
6. envelopes add up to NCO(24), and glide shares sum to 1;
7. the interim path is feasible without sales.

### 4.9 Joint simulation of the group layer

**The prototype** (groups gap_04 §1).
- `g04_engine.py` imports gap_02's `t1_engine.py` unmodified and adds:
  - the October-2026 initial state;
  - cohort engines for all seven groups (PE vintages, Secondaries sub-books, Capital Solutions claims, a 90-company co-investment EV engine, Private Credit wrappers);
  - the §4.7 lagged co-investment flow running on simulated PE commitments;
  - GP effects drawn once per path and shared by PE and co-investment (correlation ≈0.6);
  - company overlap with Private Credit (24% of companies), with recap netting and shared default draws;
  - desk-quote noise on the discount;
  - Level-1 overlay templates;
  - a discount process anchored on four dated secondary-market prints;
  - the CFP stage machine, using a per-path T4′ survival test that reproduces gap_02's 17-month ladder exactly.
- There are nine players and a defined group-off baseline (§4.3).
- In compatibility mode the engine reproduces `t1_engine` path for path. Runs use 10,000 paths per model and policy, M1–M6, over 20 quarters.

**Bridge from gap_02's engine.** P(red), %, on 10,000 paths [I-calc; SYNTHETIC].

| Step | Do-nothing levers, M1 / M4 / M6 | Mix B, M1 / M4 / M6 |
|---|---|---|
| S0 gap_02 engine as published | 8.2 / 21.2 / 37.3 | 0.08 / 0.55 / 6.4 |
| S1 + October-2026 state | 6.1 / 16.2 / 31.7 | 0.07 / 0.51 / 6.0 |
| S2 + cohort engines | 6.6 / 14.4 / 30.9 | 0.04 / 0.39 / 5.5 |
| S3 + flow, shared GP and company draws | 6.4 / 14.2 / 30.7 | 0.04 / 0.36 / 5.4 |
| S4 + Level-1 overlay, static book | 6.5 / 14.8 / 33.0 | 0.04 / 0.25 / 4.8 |
| S5 + group playbooks | 2.0 / 7.0 / 17.3 | 0.00 / 0.00 / 0.12 |
| S6 + CFP stage drives policy | 1.6 / 6.3 / 14.5 | 0.00 / 0.00 / 0.09 |
| S7 + contingent budgets (current gate) | 1.6 / 6.3 / 14.5 | 0.00 / 0.00 / 0.09 |

*SYNTHETIC – NOT ADIC DATA.* The October-2026 state (a 5.7% year-1 draw, the Gulf-war posterior and the drought mix) is worth 2–6pp on the do-nothing book. The playbooks move P(red) most; they are assumed to execute at quarter-end readings without slippage.

**Per-group fans** (Mix B, current triggers) [I-calc; SYNTHETIC]. P5 / P50 / P95 in $bn; DVA is return less the beta-matched funding basket, before FTP.

| Group | P(net cash < 0), years 1 → 5: M1 | Same: M6 | 5-year cash, M1 | 5-year DVA, M1 |
|---|---|---|---|---|
| PE | 63 / 34 / 23 / 18 / 13% | 87 / 74 / 49 / 31 / 21% | −4.5 / 16.1 / 46.0 | −0.9 / 6.2 / 15.3 |
| Secondaries | 44 / 17 / 11 / 10 / 10% | 78 / 31 / 19 / 14 / 12% | 1.1 / 6.5 / 14.3 | 0.2 / 2.6 / 6.5 |
| Capital Solutions | 4 / 13 / 12 / 12 / 14% | 3 / 7 / 6 / 6 / 8% | 2.3 / 4.4 / 6.1 | −1.0 / 1.1 / 3.6 |
| Co-investment | 18 / 22 / 14 / 9 / 7% | 26 / 23 / 13 / 8 / 6% | 2.0 / 7.7 / 18.6 | −0.9 / 4.6 / 12.1 |
| Private Credit | 4 / 4 / 3 / 2 / 2% | 5 / 3 / 1 / 1 / 1% | 4.2 / 5.6 / 7.0 | −0.8 / 1.6 / 4.2 |
| Public Markets (proceeds) | 0 / 0 / 0 / 7 / 13% | 0 / 0 / 0 / 4 / 15% | 18.5 / 26.6 / 36.7 | −1.0 / 0.7 / 2.7 |
| Overlay | 37 / 40 / 41 / 41 / 40% | 43 / 44 / 48 / 48 / 49% | −4.2 / 1.9 / 7.7 | −4.3 / 1.8 / 7.6 |
| TPA (beta deviations) | 37 / 39 / 36 / 37 / 36% | 72 / 60 / 46 / 43 / 41% | −6.6 / 2.3 / 9.6 | −1.8 / 0.3 / 1.7 |

- **PE is the cash sink early and a source late.** Year 1 is the squeeze: PE and Secondaries are net users in 78–90% of year-1 paths in M4 and M6. Capital Solutions and Private Credit are cash-positive in 95–97% of year-1 paths.
- **The group-off baseline fails over time.** Hedge funds are never redeemed and long-only runs out, so red events reach 24.8% by year 5 in M1 and 66% in M6.
- **Nine-player Shapley values** (Mix B, exact over 512 coalitions; Σφ = v(N) − v(∅) to 10⁻¹⁴).

  | Player | ΔP(red), pp: M1 / M4 / M6 | ΔCE, $bn: M1 / M4 / M6 |
  |---|---|---|
  | CF (facilities, band, reserve) | −7.1 / −14.3 / −18.5 | +0.02 / +0.17 / +0.05 |
  | Public Markets (P2S, notices) | −6.7 / −13.6 / −17.5 | −0.85 / −0.82 / −2.23 |
  | PE (pacing corridor) | −3.6 / −7.6 / −9.7 | +0.79 / +1.55 / +2.95 |
  | Co-investment (pause) | −1.9 / −3.6 / −4.3 | +0.31 / +0.71 / +1.57 |
  | Private Credit (run-off, loan sales) | −1.8 / −3.5 / −4.3 | −0.03 / +0.14 / +0.40 |
  | Capital Solutions | −1.1 / −2.3 / −2.7 | −0.06 / −0.08 / +0.11 |
  | Secondaries | −0.8 / −1.6 / −2.0 | +0.17 / +0.26 / +0.53 |
  | Overlay (monetization, de-risking) | −1.2 / −1.3 / −3.9 | +1.68 / +2.45 / +6.66 |
  | TPA (beta rule) | −0.6 / −0.6 / −3.3 | +1.17 / +2.49 / +9.36 |
  | **Total v(N) − v(∅)** | **−24.8 / −48.3 / −66.2** | **+3.2 / +6.9 / +19.4** |

  *SYNTHETIC – NOT ADIC DATA.* Path standard errors are 0.02–0.19pp on P(red) and $0.01–0.43bn on CE. CF and Public Markets are insurance: each removes 26–30% of red-event risk but adds little or negative CE, because P2S and redemptions cost return. The overlay playbook and TPA's beta rule earn 69–89% of the CE gain. v(∅) itself carries ±0.40–0.50pp on P(red); common random numbers shrink the error of the total change in E[W̃] to ±$0.06–0.13bn.

**Limits.**
- All dynamics are stylised [I] on gap_02's proxies.
- Crises occupy 12–18% of quarters and all reach a discount above 20%, which favours deployment.
- Playbooks execute without slippage.
- The co-investment write-off barrier (V < 0.85D) is checked quarterly with no Broadie–Glasserman–Kou shift, so write-offs are understated. The equivalent quarterly barrier is ≈0.92D in calm quarters and higher in crisis. Outputs move only through lost recovery options and private-credit overlap defaults. Apply the shift at the next re-run [`research/groups/addenda/G4_barrier_rerun/RESULTS.md` §6.3; not re-run; added 2026-10-18].
- The H used is a one-year LP, not H itself.
- Shapley shares depend on the baseline.
- The PE cohort history reaches census v1.0's $27.4bn with 12.6% a year commitment growth to $11.6bn in 2026, a history that fails V6's contribution half (C19). PE fans, trigger frequencies and Shapley shares are therefore re-run on the confirmed census.

---

## 5. Forecast credibility and scoring per group

**One mechanism for every group.**
- **Registry.** Bitemporal and append-only. Each record holds author, as-of date, horizon, target, quantiles, a snapshot (u, a, NAV, regime), the decision link and a shadow id for declined deals.
  - Quantiles are P10/P50/P90, adding P5/P25/P75/P95 for PE, Co-investment and the opportunistic overlay [C].
  - Groups also file 4- and 8-quarter cash flows and exit timing.
- **Score.** The weighted interval score:

  $$\mathrm{WIS}=\tfrac{1}{1.5}\big[\tfrac12|y-q_{50}|+0.1\,IS_{0.2}\big],\qquad IS_\alpha=(u-l)+\tfrac2\alpha(l-y)\mathbb1\{y<l\}+\tfrac2\alpha(y-u)\mathbb1\{y>u\}$$

  It is proper, but only a coarse CRPS proxy at K = 1 [C]. Example: a 12/20/26% co-investment forecast against a realized 7% scores 0.086, against 0.023 for the reference class, a skill of −2.69 [I-calc].
- **Bias model.**

  $$y_j-q_{50,j}=\beta_g+\beta_s+\beta_a+\beta_D\mathbb 1\{D\}+\gamma(u_j-a_j)^++\beta_F\mathbb 1\{\text{SELL}_{j,t-1}\}+\varepsilon_j,\qquad \varepsilon_j\sim t_\nu(0,\kappa_g\hat\sigma_jc_\nu)$$

  with $\hat\sigma_j=(q_{90}-q_{10})/2.563$ and $c_\nu=1.2816/t_{\nu,0.9}$ (c₄ = 0.836), which keeps κ's meaning under any tail.
  - Effective sample size is $n_{eff}=n/(1+(m-1)\rho)$, with ρ = 0.3.
  - The model is estimated on all forecasts, including declined deals tracked in shadow, with inverse-propensity weights. Approved-only samples carry the optimizer's curse [S].
  - **Production uses the robust estimator FBE-R** (groups gap_02 §3). It runs a Huber bias regression on [1, D, gap, flag], with slopes pooled across groups, because one group's n = 40 cannot detect the strategic term. The u–f error covariance is estimated from the test cross-section as cov(u − a, f − a) − σ_a², and bias uncertainty is propagated. Its covariates include the optimizer's own outputs: SELL flags and envelope status. Robustness costs about 7pp of CRPS when the model is right.
- **Overconfidence: one parameter** (groups gap_02 §5).
  - κ_g := w₈₀(true) ÷ w₈₀(stated), where w₈₀ is the width of the 80% central interval. κ_g ≥ 1 means overconfidence; for Gaussian errors κ = σ_true ÷ σ_stated.
  - The generator sets q₁₀, q₉₀ = f ∓ 1.2816·σ_true/κ_g. This retires κ_conf, which equals 1/κ_g.
  - The prior is κ_g ~ LN(ln 1.75, 0.25²), a 90% range of 1.16–2.64. A stated 80% interval covers 2Φ(1.2816/κ) − 1 of outcomes: 54% at the prior median, or 48% with a half-SD bias. κ = 2.74 reproduces the 36% coverage found by Ben-David, Graham and Harvey [I-calc].
  - Until a group is scored, stated ranges are widened ×1.81–2.74 [S]. SBC mode draws κ_g from the prior; recovery mode pins it to the table below.
- **Feed into return fusion.**
  - One hierarchical FBE model, with forecast precision $1/(\kappa_g^2\hat\sigma^2)$ and no extra Bühlmann Z multiplier [C].
  - Tier 2 uses posterior means. Tier 1 uses the posterior P10, with group bias stressed by +2 sd.
  - Each simulation path draws μ_i once, plus a common group-bias shock.
- **Display and pay.** Scores are shown only when n_eff ≥ 20 (at n = 20 the standard error on 80% coverage is ±8.9pp). The inflation incentive is δ* = bZB′/(2s): keep b small and make s real [C]. Pay is linear in vintage-FTP DVA, with ≤ 10 points for WIS skill; nothing scales with budget or AUM.
- **Pay design is a precondition for deployment** (gate G-E, §6). The misspecification ensemble now generates strategic bias: $b^f_{i,t}=b^f_g+b_gZ_{g,t-1}B'_{g,t}/(2s_g)+u_{def}\mathbb 1\{\text{SELL}_{i,t-1}\}$, with B′ = 1/H_g when the envelope row binds, and a "defend-the-holding" uplift u_def = +2pp a year after a SELL flag [S direction: Staw, Barsade & Koput 1997].
  - Under status-quo pay (b = 0.02, δ\* = 320bp) even FBE-R fails the CRPS gate.
  - A group that fails under that variant gets non-trivial forecast precision only after the pay remedy: b ≤ 0.005, s ≥ 50, and nothing that scales with budget (designed pay gives δ\* = 80bp) [I-calc].

| Group | Forecast filed | FBE path | b^u / b^f (pp a year) | κ (coverage of a stated 80% interval) | Group-specific checks | Primary score |
|---|---|---|---|---|---|---|
| PE | Call/distribution quantiles; terminal TVPI; exit dates | Fund interest (BF/Benktander) | +5.0 / +3.0 (+4.0 late) | 2.00 (48%) | Timing slip; fundraising marks; line IRR | WIS; Mincer–Zarnowitz; timing-centroid shift |
| Secondaries | Deal cases; external-price distributions (desk) | Fund (S1/S3); single deal (S4/S5) | +2.0 / +1.5 | 1.67 (56%) | Accretion; targets as expectations; winner's curse | WIS; desk vs consensus benchmark |
| Capital Solutions | Contractual yield → debiased E[r] | Single deal | +2.0 / +1.5 | 2.00 (48%) | PD ×0.7; PIK at face; kickers | WIS; PD/LGD calibration |
| Co-investment | Deal-model IRR, MOIC, exit date | Single deal, GP effect shared with PE | +6.0 / +3.5 | 2.22 (44%) | Structural corrections; leverage and ICR flags | WIS |
| Private Credit | LAY, cash vs PIK | Fund path / loan cohorts | +0.75 / +0.75 | 1.67 (56%) | Recovery basis; default definition | WIS; loss gate V12 |
| Hedge funds | Net-α quantiles; liquidity outlook | Hierarchical factor model | +3.0 / +2.0 | 1.67 (56%) | Selection; smoothing; terms | Rank IC; Brier; time-to-cash error |
| Long-only | Net IR | Benchmark + β + α̂ (prior −0.05) | +1.0 / +0.75 | 1.43 (63%) | — | Rank IC |
| Overlay | Tail: scenario payoffs and carry. Opportunistic: Sharpe | Scenario; DSR-gated residual α | Carry −30%, payoff +20%; Sharpe +0.6 / +0.4 | — | Roll costs; trials counted | Joint (VaR, ES); DSR ≥ 0.95 |

κ values are the old κ_conf inverted (κ = 1/κ_conf), so the evidence behind them is unchanged.

---

## 6. Synthetic dataset specification: SYN-ADIC-177

**Architecture.**
- **Layers.** Three: world (regimes, factors, exit factor X_t, valuation gap z_t); sealed truth (skill, economic NAV, true μ, bias draws, outcomes); observation (reported NAV, cash flows, u/a/f, terms, quotes, loan tapes, overlay trades, CSAs).
- **Releases.**
  - R0: the 2026-10-18 snapshot, with history from 2008.
  - R1: 1,000 worlds × 40 quarters, on common random numbers across SELL / HOLD / REFINANCE / LEVER.
  - R2: 200 history worlds covering 2000–2040.
- **Format.** US$m, quarterly (monthly for hedge funds, daily overlay sub-steps in stress); Parquet with a SeedSequence hierarchy. The generator is structural, so θ is known and counterfactual action cash flows exist.

**Census v1.0, with the proposed v1.1** (SYNTHETIC; sizes lognormal and rescaled to the group totals). v1.1 changes only PE unfunded. It revises a working assumption, so it takes effect only once the user confirms it.

| Group | Positions | NAV ($bn) | Unfunded ($bn): v1.0 / v1.1 proposed | Size σ; mix |
|---|---|---|---|---|
| PE funds | 120 (≈70 GPs) | 52 | 27.4 / **16.4** | 1.0; §3.1 |
| Secondaries | 40 | 14 | 3.9 (incl. 0.4 deferred) | 0.8; S1–S6 |
| Co-investment | 90 | 18 | 1.5 | 0.8; BJS deal generator |
| Capital Solutions | 40 | 8 | 1.2 | median $150m; families A–G |
| Private Credit | 35 vehicles + ≈1,500 loans | 14 | 4.0 (1.0 DDTL/revolver) | 0.8; DL 60, ABF 15, mezzanine 10, opportunistic 15 |
| Hedge funds | 40 | 20 | — | 0.6; §3.5 mix |
| Long-only | 24 | 36 (DM 22, EM 6, FI 8) | — | 0.7 |
| Treasury (CF) | 6 sleeves | 15 (cash 6, UST 4, IG 5) | — | — |
| Overlay | Policy book: $7.1bn floor ladder, $10bn completion beta, $1.0bn opportunistic IM. Test fixture: ≈250 trades on 12 CSAs | $50–90bn notional (fixture) | — | §3.7 |
| **Total** | **≈395 + loans + trades** | **177** | **38.0 [A] / 27.0** | |

**PE history: census v1.1, proposed** (groups gap_02 §1) [I-calc; SYNTHETIC].
- **Engine and method.** RFT-TA v2 at its mean path on a quarterly grid; census date 2026-09-30. Census quantities are linear in vintage commitments, so feasibility is a linear program: maximize unfunded subject to NAV = $52bn, both MSCI H1-2026 rates in V6's ±2pp band, and a growth corridor on commitments.
- **Rule** (`seal_history.py`). Within the plan-consistent family, require a distribution rate of exactly 9.0% and a contribution rate of at least 29.0%, and take the member with the largest unfunded, which is the liquidity-conservative choice.
- **Sealed history.** Commitments grow +1.44% a year over 2010–20 ($3.80bn → $4.39bn); boom 1.5× in 2021–22 ($6.67bn, $6.77bn); and fall 5.75% a year over 2023–26 ($6.38bn → $5.34bn, ¾ committed by the census date). Commitment shares by strategy: large buyout 39.9%, mid buyout 25.0%, growth 12.7%, VC 6.5%, sector 10.0%, special situations 5.9%.
- **The book at the census date.**
  - NAV $52.0bn by vintage: 2010–15 $7.3bn; 2016–20 $22.5bn; 2021–22 $12.8bn; 2023–26 $9.5bn.
  - Unfunded $16.4bn: pre-2021 $0.6bn; 2021–22 $2.5bn; 2023–24 $5.6bn; 2025–26 $7.7bn.
  - The largest vintage is 2021, at 13.1% of NAV.
  - The distribution-rate history tracks MSCI within ±2pp, except in 2019–20, where the engine's normal-regime calibration runs 4–5pp high.
- **Seal.** `sealed_pe_history_v1_1.csv` holds commitments by vintage and strategy plus census NAV and unfunded by vintage. Its SHA-256 is `4346dc249e83bff8d952588715a69ec038b9725ab436e0b24b8bb4227f2f54a9`. In production it moves to the sealed truth store (L6), and estimators see only observation-layer data.
- **Truth variants** (same engine and NAV): mature $13.9bn; 10%-then-flat $18.4bn; 20% growth $31.9bn, which fails V6 by construction and is kept as the stress truth; v1.0 reproduction $27.4bn, kept for continuity.
- **R15 recovery test.** Estimators must recover the pace and unfunded by vintage within V17's ±5pp coverage tolerance under every variant.

**Overlap graph** (groups gap_02 §6). One graph links sponsors → funds → companies and every ADIC claim: PE look-through, co-investments, Capital Solutions (family A fund finance; families C/D/E company exposure) and Private Credit loans. Each company's EV path is keyed by company_id in the SeedSequence hierarchy, giving one draw per company per path.

| Parameter | Value | Anchor |
|---|---|---|
| s_PC, sponsored share of PC borrowers | 0.75 | KBRA DLD: ≈1,700 sponsored and 600 non-sponsored borrowers (74%; Mar 2024). US private-debt capital in sponsored deals: mean 78% (Europe 42%) [Block, Jang, Kaplan & Schulze]. US direct-lending deals: 57.9% sponsored in Q1-2026 [PitchBook LCD] [S] |
| Lender clubs | 61% of upper-middle-market issuers in ≥ 2 portfolios (20% lower middle market); average BDC overlap 9.2% (portfolios > $5bn) to 1.4% (< $1bn) | Cliffwater via Future Standard (Q1-2026); LFI/SOLVE (Jun 2025) [S] |
| Sponsor concentration | Top decile backs ≈50% of borrowers | S&P (Dec 2023), seen only in search summaries **[U]**; not load-bearing |
| p_co / h_co; h | 0.70 / 0.90; ≈0.6 | Census [A]; co-investment rights attach to fund LPs [I]; 120 funds across 70 GPs [I] |

Sampler results over 20 censuses [I-calc]:
- co-investments in PE look-through: 0.67 by count, 0.69 by value;
- PC loans to look-through companies: 0.13 (≈190 of 1,500);
- Capital Solutions C/D/E in look-through: 0.33; family A lending to ADIC-held funds: 0.47;
- co-investments that also carry an ADIC PC loan: 0.08 (≈7 deals);
- the largest GP averages 4.7% of private NAV + unfunded (p95 6.6%), so 35% of sampled censuses breach the 5% hard limit.

**Truth process, with the verifier fixes.**
- **Skill:** $a_v=-0.05z_v+u_v$ per year (a vintage SD of ≈1%), a GP effect of 3% and an idiosyncratic 2.5%, for a total σ_α ≈4%.
- **PE NAV:** shocks truncated or NIG, because $E[e^{t_5}]$ is infinite; α net of ≈1% a year of write-down jumps; calibration *within* each world (pooling worlds gave a vintage ICC of 0.78, against 0.12 empirically).
- **Group engines:** as specified in §3, with private credit carrying both loss pairs.

**Observation layer.**
- **O1, reported NAV.**
  - Smoothing: 0.5 buyout, 0.6 VC, 0.5–0.7 private credit, 0.5 Capital Solutions (GC1 D17; G9's 0.4 is a sensitivity), 0.5 co-investment; a 1-quarter lag; noise N(0, 0.04²).
  - Manipulation (BGK model ii): a symmetric peer reversion of ≈2.6pp per SD, plus ≈+5pp at 2 SD below peers after five years without a new fund.
  - Exit uplift ~ N(0.10, 0.15²).
- **O2, underwriting:** $u=\bar\mu+0.3(\alpha-\alpha_s)+b^u+\gamma'x$, where leverage above 6× and a multiple-expansion share above 50% each add +2pp.
- **O3, actuals:** a deterministic performance module, `perf_module.py` (`perf-0.1.0`), that passes 17/17 golden tests (groups gap_02 §4).
  - It takes observation-layer inputs only, so actuals inherit every O1 reporting bias.
  - Conventions: ACT/365F; Brent root-finding with a sign-change check that returns *None* rather than extrapolating; residual NAV treated as a terminal flow. The benchmark is a registry field per strategy, and outputs are hashed with the input snapshot. The same code will run on ADIC data.
  - **Metrics by holding type.**
    - *Fund interests and deal flows:* XIRR, TVPI with DPI and RVPI, KS-PME [S: Kaplan & Schoar 2005] and direct alpha [S: Gredil, Griffiths & Stucke 2023].
    - *Hedge funds and long-only:* TWR chained from Modified Dietz returns; any flow above 10% of start value must coincide with a valuation.
    - *Private Credit and Capital Solutions debt:* realized cash yield, PIK share, realized loss rate and loss-adjusted cash yield.
    - *Overlay:* book P&L = ΔMTM + cash − FTP × IM × Δt.
- **O4, forecasts:** $f_t=\rho_ff_{t-1}+(1-\rho_f)[w_uu+w_aa+(1-w_u-w_a)f^*+b^f]+\eta$ with ρ_f = 0.6. Campbell–Sharpe's ≈30% anchoring maps to w_a or ρ_f [C]. Timing optimism lasts 5 quarters after a high-yield spread shock above +150bp. The ensemble below varies b^f, w and the error law.

**Calibration and robustness are separate tests.**
- SBC (V16) still runs with generator and estimator sharing the §5 bias priors, as simulation-based calibration requires. It is the computational check only.
- Robustness is tested by a **misspecification ensemble** (groups gap_02 §3): only the generator changes, and the estimator stays fixed.

| Id | Mechanism | Specification [I] |
|---|---|---|
| M0 | Well specified | The SBC case |
| M1 | Regime-dependent optimism | b^f × (1 + 1{D}); training 30% D, test 100% D (today is LATE × D) |
| M2 | Nonlinear anchoring | f = (1 − w)f₀ + w·u, with w = 0.15 + 0.45·tanh((u − a − 0.05)⁺/0.04): the forecast clings to the underwriting after bad news [S direction: Easterwood & Nutt 1999] |
| M3 | t3 tails | η_u, η_f and outcome noise are t3, rescaled to the Gaussian 80% width |
| M4 | Correlated u–f errors | corr(η_u, η_f) = 0.6 |
| M5 / M5s | Strategic bias | The §5 formula, under designed pay (δ\* = 80bp) and status-quo pay (δ\* = 320bp), with u_def = +2pp. B′ uses G8 E5's own-curvature $400bn per unit; with G8 R13's 1/H_g correction δ\* is ≈3.5× smaller, so M5 and M5s are conservative stresses |
| M6 | Prior shift | True b^f = prior mean + 2 prior SD |
| MALL | All of M1–M6 | — |

**Gates** (pre-registered; no tuning on release data).
- The metrics are excess CRPS over a *variant-aware oracle*, which knows the generator and so separates estimator failure from a harder world; 80% interval coverage; mean error on true SELL candidates (μ < 8%); and excess SELL-decision regret.
- **G-A (M0):** SBC passes; coverage 0.75–0.85; excess CRPS ≤ 15%.
- **G-B (each of M1–M6):** excess CRPS ≤ 15%; coverage 0.72–0.88; SELL bias ≤ 1.5pp; excess regret ≤ 35%.
- **G-C (MALL):** ≤ 25%; ≥ 0.70; ≤ 2.0pp; ≤ 50%.
- **G-D (detection):** the pooled bias regression detects the regime, gap and flag terms with power ≥ 0.70, with false positives under M0 ≤ 0.05.
- **G-E (pay):** a group that fails G-B under M5s gets non-trivial forecast precision only after the pay remedy (§5).
- **Prototype** [I-calc]: 2,000 worlds; a PE-like group with n = 40 resolved forecasts (320 pooled across 8 groups) and 120 test assets.
  - The production-style FBE-B fails four gates: G-B for M1, M4 and M5s, and G-C (MALL: excess CRPS +46.9%, coverage 0.545).
  - The robust FBE-R fails only the M5s CRPS gate (+15.8%), which triggers G-E.
- **Freezing.** The gate values were set after one prototype run. They must be frozen and hashed before the first scored release.

**Validation gates.**

| Gate | Check |
|---|---|
| V1–V2 | Accounting identities; group totals equal §1A; intra-ADIC flows net to zero, on DVA ledgers as well as on cash (groups gap_03: the naive services booking double counts −$7.05bn in S1) |
| V3–V9 | PE dispersion vs BGK (USD sample); vintage component 0.10–0.18; DPI by age; distribution rates vs MSCI ±2pp; exits above prior mark 0.70–0.80; buyout AR(1); secondary prices vs Jefferies ±3pp |
| V10–V13 | Hedge-fund θ at fund level; liquidity vs Form PF on its own definition ±5pp; private-credit loss 0.8–1.2%; VIX/MOVE quantiles ±10% |
| V14–V20 | Bias realism; classifier two-sample test AUC ≤ 0.60 once ADIC data exist; SBC; parameter recovery ±5pp, including R15 (PE pace and unfunded by vintage under every truth variant); time-travel CRPS skill > 0; regret vs oracle; labelling at 100% |
| V21–V23 | Census and NAV-weighted leverage within ±20% of OFR; Basel caps in every coverage ratio; no LP-inaccessible SELL or REFINANCE instrument |
| V-RA-CTRL (patch, ra_gap_01) | Extends V23 to Real Assets: no REFINANCE, LEVER or HEDGE card on LP or minority holdings; JV sell-downs and cash-outs only on the controlled share (`research/groups/addenda/ra_gap_01_calcs/test_v_ra_ctrl.py`, 4/4 pass) |
| V24 (new) | Overlap. **a)** Every claim on company k in world w reads one EV draw; defaults and recaps hit every claim in the same quarter, with waterfall-consistent payoffs; intra-ADIC recap flows net to zero (extends V2). **b)** Realized overlap shares sit inside binomial 90% bands at census size: Co-investment ∩ PE 0.59–0.76; PC ∩ PE 0.115–0.143; Capital Solutions C/D/E ∩ PE 0.15–0.51; Capital Solutions A → ADIC funds 0.26–0.74; co-investments with an ADIC PC loan 0.03–0.13. Each parameter must also sit inside its anchor range. **c)** GP ≤ 5% is computed on the graph; breaching draws are rejected unless the run is a labelled concentration stress. **d)** The FBE's ρ_GP = 0.6 shock applies only to holdings that share a GP on the graph |
| G-A–G-E (new) | Misspecification gates (above), frozen and hashed before the first scored release |

The prototype SBC caught a fusion posterior that ignored the correlation between forecast and underwriting errors (χ²₁₉ = 207 against a critical value of 30.1). Cluster-blind bias intervals covered 76% instead of 90% [I-calc, G9].

**Labelling (L1–L8), enforced in code:** `SYN-` identifiers, `is_synthetic=true` and a provenance flag on every row; Parquet metadata; the footer "SYNTHETIC – NOT ADIC DATA" on every chart, table and IC page; taint propagation (any output computed from a synthetic input is synthetic); truth tables sealed from agents and estimators; a claim validator that rejects text attributing synthetic numbers to ADIC; synthetic sets frozen and kept separate once ADIC data arrive.

---

## 7. IC implications

### 7.1 Group-head seats in the shadow IC

The shadow IC has 12 seats defined by mandate (gap_01), and **13 with the Real Assets head** (`02_REAL_ASSETS_SYNTHESIS.md` §12; patch, ra_gap_01). Main v1.1 §6.2 carries the same seats, so the two reports agree (v1.0's seven-seat design is retired):
- CIO;
- CRO;
- Treasurer / CF, who is also the owner's advocate;
- the five private-group heads, plus the Real Assets head;
- the Public Markets head;
- the Overlay head, carrying two briefs;
- an Outside-View Forecaster;
- a Red Team.

AI seats flag but never vote. With ≤ 40% of seats per model family, at least three families are needed, and four is the target. Seats carry a mandate, a loss emphasis and an evidence slice. **Personality personas are excluded because of caricature risk** (C4).

| Group-head seat | Loss emphasis | Evidence slice | Standing question |
|---|---|---|---|
| PE | Lost GP access; vintage holes | Belief cards; pacing MPC; κ^GP break-evens; vintage census | Is the cut priced by c^PACE (forgone net α\*, κ^GP and co-investment flow), not as a financing rate? |
| Secondaries | Winner's curse; accretion booked as alpha | Hedonic model; θ; scored desk forecasts | Is θ/p > 1 after staleness, is the discount confirmed, and is Tier 1 green? |
| Capital Solutions | PIK and kicker optimism | Credit engine; reserve-price quotes | Does the deal clear (1 + r_h)(1 + ℓ̄) − 1 on drought cash income? |
| Co-investment | Adverse selection; concentration | Deal engine; "what you need to believe" flags; offer log | Which growth and exit multiple must hold, is effective N ≥ 40, and does deployment stay within accepted flow? |
| Private Credit | PIK, extensions, recoveries | Loan tapes; λ* by wrapper | Which sleeves can run off or sell (the cheapest recovery levers), and which LGD pair drives the card? |
| Public Markets | Gates; adverse-selection redemptions | State machine; P2S cards | Which notices go in at Amber, and what VM does P2S create in a −33% month? |
| Overlay | Hedge fatigue; hidden short volatility | Offset card; DSR card; collateral ladder; services ledger; fatigue tracker | Do L1–L3 hold? What policy residual is the IC paying, and what robust enabling value offsets it? |
| Real Assets (patch, ra_gap_01) | Stale marks mistaken for value; refinancing walls and cures; queue illiquidity; owner-correlated oil and Gulf exposure | Marks panel (V^A, V\*, Ĝ); debt-wall and cure-CVaR card; queue card; oil-delta card; RA cash row and L4 budget B_RA | Is it priced and paid on V\*, is the action in the holding's control cell (V-RA-CTRL), and what does it do to the oil delta and the 24-month cure tail? |

Group-head seats recuse on their own envelopes. They are scored on total-portfolio regret, not group P&L, and they may challenge another group but never veto it.

**Recovery-mode evidence slices** (groups gap_01 §5).

| Seat | Slice added while the book is in RECOVERY |
|---|---|
| CIO | The t0 envelope table; glide shares |
| CRO | T4′ headroom with its SAA band; T6 bands; the reverse-stress panel (literal T4, critic reading) |
| Treasurer / CF (owner's advocate) | Phase-I u\* and the IIS; the infeasibility-price panel, which never reaches cards; revolver indications; the recovery hash |
| Five private-group heads | Their catalogue rows and delivery against φ_g, scored on delivery and total-portfolio regret |
| Public Markets head | Hedge-fund queue; P2S as the T2 source |
| Overlay head | Two briefs: convexity per unit of carry; deflated alpha and margin |
| Outside-View Forecaster | Base rates |
| Red Team | Must run the literal-T4 and critic reverse stresses |

A non-voting AI Validator rejects any pack in which a card or envelope lacks `priced_on` or derives from a reverse stress.

### 7.2 How group results are discussed

The human agenda runs in four blocks:
- **A. Total portfolio:** CFP stage (readiness and event indicators separately), the Tier-1 board, SH_TP under T4′, the λ curve at tolerance and at appetite, the mandate. In RECOVERY it adds u\*, the IIS, the glide path and delivery against it, and the infeasibility-price panel.
- **B. Group blocks,** ordered by the marginal-asset agenda (the LP relaxation splits at most one asset per binding row). Each block shows:
  - envelope use and priced requests above it;
  - decision cards: P(best), regret both ways, the LAPV waterfall, flip thresholds, the belief card and consents, each with its `priced_on` flag and recovery-target hash;
  - net α* after charges;
  - forecast information value.

  The Group 7 block adds (groups gap_03 §6): budget use; S/H/R/L cards for each book; the L1–L3 offset card; the services ledger; the fatigue tracker; the coverage matrix.
- **C. Cross-group items:** internal transfers, contingent budgets (gate state and T4′ headroom), desk quotes via the pricing committee, P2S and HF-TRS collateral.
- **D. The ballot,** after a locked blind pre-vote, followed by minority reports and signposts.

### 7.3 Decision rights

| Decision | Who decides |
|---|---|
| Deals inside the envelope | Group |
| Up to +20% above the envelope; P2S; internal transfers below the Tier-A size | CIO + CRO (Tier B) |
| Actions ≥ 0.25% of NAV (≈$0.44bn), conflicted transfers, opportunistic limits | Full IC (Tier A) |
| Envelopes and FTP each quarter | Total Portfolio Committee / IC; the methodology is approved annually by the Board |
| Portfolio LEVER (facilities, repo, term debt) and collateral | CF |
| Tail budget within 0.15–0.50% of NAV; terminating a tail layer | Full IC (Tier A), with a disclosed record. The floor changes only at the annual Board-approved budget |
| CFP actions | Green: Treasurer. Amber: CIO. Readiness-Red: the Phase-II plan (pacing rule, revolver request, band request; CIO / IC). Event-Red: IC weekly. Black: Board and owner |
| RECOVERY: the structural deficit u\*, the glide path and any extension to 8 quarters | CF and the Board (band request; Board sign-off). Groups deliver against φ_g |
| Payout-rate changes; value splits | Board and owner |

### 7.4 Politics-aware presentation of forecast calibration

- Credibility is a weight on information, not a grade on people. Show the *information value* of a group's forecast (how far it moved the FBE), not its "bias".
- Compare each group only with its own reference class, selection-adjusted, multi-year, with bands and only when n_eff ≥ 20; never publish league tables.
- Penalize sandbagging as much as optimism; keep individual scores private; hold blame-free post-mortems.
- No group vetoes another: prices and envelopes settle conflicts.

---

## 8. Consolidated calibration targets

The parameter defaults are in §3. This table lists the targets the engines must reproduce.

| Quantity | Value | As of | Source | Conf. |
|---|---|---|---|---|
| PE distribution / contribution rate | 9% / 31% (H1-26); 9–11% / 27–31% (2022–25); 17–24% (2017–20) | Data to Q2-26 | MSCI Private Capital Benchmarks | High |
| No-new-commitment cash release | ≈40% of forgone commitments in 4 years. The engines release more: 66% on RFT-TA v2 (groups gap_02, pace-invariant) and 69% on G1's engine. The gap is open | Dec 2023 | Cliffwater for ERSRI | High (check only) |
| LP-portfolio pricing | 87% (buyout 91, venture 79, credit 89, real estate 68) | H1-2026 | Jefferies | High |
| Buyout price by fund age | 99/96/88/79/70% | 2024 | Jefferies | High |
| Crisis bids | 61% of NAV (83.5% market-adjusted) | H2-2008 | Cogent via Unquote | High (upper bound) |
| Tail-end price; buyer PME | 82.2% mean; ≈1.00 (buyout tail-end) | 2006–14 data | Nadauld et al., NBER w22404 Tables 3 and 6 (not re-checked against the 2019 *JFE* tables) | High |
| NAV-loan margins (GP level) | 4.8% secured / 6.1% recourse-light | FY2025 | Rede Partners | High (proxy) |
| NAV facility LTV | Modal primary bucket 10–25% (36%) | FY2025 | Proskauer | High |
| Hybrid-capital returns | Mezzanine 9.04%; special situations 12.62% mean; net alpha ≈0 | Data to 2020; 2024 | Böni–Manigart; EFW | High |
| Co-investment deal PME | P25 0.26 / median 1.16 / P75 2.45 | 1981–2010 deals | Braun–Jenkinson–Schemmerl | High |
| PC default incidence | Fitch 6.3% (broad); Proskauer 2.51%; KBRA 1.4% (2025), 2.5% (2026F) | Aug–Oct 2026 | Fitch; Proskauer; KBRA DLD | High |
| Direct-loan recovery | ≈33% post-default value vs 52% syndicated | Feb 2024 | Cai & Haque (KBRA DLD data) | High |
| Direct-lending realized loss | 1.0% a year long-run; ≈0.5% in H1-26 | Aug 2026 | Cliffwater CDLI | High |
| PIK prevalence | 11.3% of interest income; bad PIK 6.2% of loans | Q2-2026 | Lincoln International | High |
| Evergreen requests | 13.9% / 13.0% of NAV vs 5% caps | Q3-2026 | VRC | High |
| Hedge-fund investor liquidity | 8.4 / 27.3 / 64.4% (≤ 7d / 8–90d / > 90d); 58.2% within a year | Jun 2026; Q3 2025 | OFR; SEC | High |
| Hedge-fund leverage (NAV-weighted) | Multi-strategy 4.5×; RV 8.1× | Jun 2026 | OFR | High |
| Crisis loss ratios | 0.51 (2008), 0.48 (Q1 2020), 0.23 (2022) | — | HFRI via CA/HFR | High |
| Long-only alpha | ≈0 across 4,617 products | 1991–2008 | Busse–Goyal–Wahal | High |
| Equity financing | ≈30bp average; > 140bp peak; +81bp (Jun 2026) | 2021–26 | D. E. Shaw; CME | High / Medium |
| Forecaster calibration | 80% intervals cover 36% | 2013 | Ben-David–Graham–Harvey | High |
| SIMM version | v2.8+2512, effective 11 Jul 2026 | Jun 2026 | ISDA | High |
| Base rates | SOFR 3.89%; 10y UST 5.09–5.10% | 15–16 Oct 2026 | NY Fed; US Treasury | High |
| PE rate definitions; implied commitment intensity | Distributions ÷ previous valuation; contributions ÷ (starting dry powder + newly raised), annualized. H1-2026 implies (dry powder + newly raised) ÷ prior valuation ≈0.31 | Q2-2026 | MSCI, pp. 13, 16; derived (groups gap_02) | High; Medium (derived) |
| Secondary-discount anchors | 87% in drought with no drawdown; 81% (2022); 61% (H2-2008); 54% (2009) | Jul 2026; 2022; 2009 | Jefferies; Cogent via Unquote; Nadauld et al. | High |
| Equity-option market state | SPX 7,659.44; VIX 19.99; VIX3M 20.50; VIX6M 21.67; VIX1Y 22.61; SKEW 168.59 (mean 123.26) | 16 Oct 2026 | Cboe | High |
| 90/72 put-spread ladder cost | 3.74% of notional a year (3.47–3.96% across skew assumptions) | 16 Oct 2026 | [I-calc] on Cboe data (groups gap_03) | Medium |
| Sponsored share of direct-lending borrowers | 74% of KBRA DLD borrowers; 78% of US private-debt capital (Europe 42%); 57.9% of US deals in Q1-2026 | Mar 2024; survey; Q1-2026 | KBRA DLD; Block et al.; PitchBook LCD | High / Medium |
| Lender-club overlap | 61% of upper-middle-market issuers in ≥ 2 portfolios; average BDC overlap 9.2% (> $5bn) to 1.4% (< $1bn) | Mar 2026; Jun 2025 | Cliffwater via Future Standard; LFI/SOLVE | Medium |
| Sovereign revolver precedents | PIF $15bn (23 banks, 3 + 2 years); Mubadala $2bn five-year (28 MLAs); Danantara $1bn three-year at SOFR + 95bp after an approach for up to $10bn | Aug 2024; May 2019; Nov 2025 | Gulf News; AidData; Bloomberg / IDN Financials (snippet level) | High / High / Low |
| Liquidity recovery capacity | Accumulated over 6 months; mutually exclusive options counted once (¶30) | Jul 2023 | EBA/GL/2023/06 | High |
| Peer tail and completion programmes | CalPERS ended its tail programme (Oct 2019) without a customized benchmark; NZ Super judges completion against benchmarks; CPP shows no benchmark for its completion portfolio | 2015–2024 | Institutional Investor; NZ Super white papers; CPP F2024 AR | High |
| System gates | PC loss 0.8–1.2%; co-investment P(MOIC < 1) 0.35–0.40; PE AC1 0.66–0.71; exit-uplift share 0.75; P10–P90 coverage 80%; WIS skill > 0; charges reconcile within 5%; V24 overlap bands; misspecification gates G-A–G-E (to be frozen) | — | GC1; GC2; groups gap_02 | [I] |

---

## 9. Questions for the user

1. **Capital Solutions scope.** Confirm families A–G and the boundaries: do senior or unitranche loans and senior ABF sit in Private Credit, and do GP stakes sit here or elsewhere?
2. **Secondaries "direct deals".** Do they cover LP-portfolio purchases and GP-led CV stakes only, or also preferred, strips and secondary directs? What is the leverage mandate?
3. **Co-investment sourcing.** What share comes from ADIC's own fund GPs, and what are the offer and acceptance rates by GP (§4.7)? The offer logs set acceptance a and κ^GP's lost-flow term.
4. **PE program (decisive).** Do you confirm census v1.1's PE unfunded of $16.4bn (total unfunded $27.0bn), which revises a working assumption? Better still, supply PE commitments by vintage and strategy since 2010, unfunded by vintage, ADIC's own overcommitment limit and pacing corridor. T4′, θ\*, the facility need, the envelopes and groups gap_04's runs are re-run on whichever census is confirmed.
5. **Private Credit.** Wrapper mix; SMA reinvestment, sale and run-off rights (the cheapest group levers in recovery); facility terms; and loan tapes with sponsor IDs, which settle the PD/LGD split, the PIK multiplier and the overlap rates.
6. **Hedge funds.** Terms τ per lot (notice, gates, revocability, consents), ADIC's share of each fund, and redemption experience in 2008, 2020 and 2022.
7. **Mandate and stress.** Will the IC ratify the T4′ calibration rule and the pooled θ\* (0.79)? Is the draw fixed in USD, reset on opening NAV or a share of current NAV, and who sets it? Can band use be pre-agreed?
8. **Funding.** What are the existing lines, their covenant terms and test history? Is there appetite for a $10–15bn syndicated committed revolver (3 + 2 years, at least 10 banks)? Are LP-level preferred equity and CFOs permitted? The NAV-facility question is dropped.
9. **Overlay.** CSA terms and sovereign IM status; dealer allocation; futures and TRS financing history; the blotter in CRIF; records of past hedge changes; whether net short volatility is allowed; whether P2S counts against the 0.30W cap; every opportunistic variant ever tested.
10. **Organization and pay.** Envelopes, authorities and recusal practice; history of internal transfers; whether CF can hold the FTP mismatch; the forecasters' pay parameters b and s, which gate G-E makes a precondition for forecast precision.
11. **Forecasts.** Does a point-in-time archive exist by group? Declined-deal lists; each group's format and gross/net basis.
12. **Look-through data.** Company and sponsor IDs for every private holding, which gate V24 and the graph-based GP ≤ 5% limit need.

---

## 10. Bibliography

*Deduplicated; corrected forms; full lists are in the G1–G9 dossiers and verification logs. [U] = not verified in-session.*

**Private equity, secondaries and co-investment**
- Albertus & Denes (2020). Private equity fund debt: capital flows, performance, and agency costs. NBER conference paper (26 May 2020). https://conference.nber.org/conf_papers/f141738/f141738.pdf. Same paper as SSRN 3410076 (2019 title "Distorting Private Equity Performance: The Rise of Fund Debt"), https://doi.org/10.2139/ssrn.3410076. Probable published successor [Inference]: Albertus & Denes (2026), "Private Equity Fund Debt: Agency Costs and Cash Flow Management", *JFQA*, online 7 May 2026, pp. 1–64, https://doi.org/10.1017/s0022109026102890 (confirmed in Crossref; the record carries no abstract or preprint link) [unverified: whether the 2014–19 figures in §3.1 are unchanged in the *JFQA* version].
- Bain & Company (2026). Global Private Equity Report 2026. https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/
- Bhardwaj, Gupta & Howell (2025). Capital structure & firm outcomes: evidence from dividend recapitalizations in private equity. NBER w33435. https://www.nber.org/papers/w33435 (DOI 10.3386/w33435). Its distress effect of "2.4 times the targeted firm mean" goes with an 84% average debt increase (§3.4).
- Boyer, Nadauld, Vorkink & Weisbach (2023). Discount-rate risk in private equity: evidence from secondary market transactions. *JF* 78(2):835–885. https://doi.org/10.1111/jofi.13202. It supersedes NBER w25207 (2018), "Private equity indices based on secondary market transactions" (https://www.nber.org/papers/w25207), the source of the β figure in §3.2. An intermediate version is NBER w28691 (2021).
- Braun, Jenkinson & Schemmerl (2020). Adverse selection and co-investments. *JFE* 136(1). https://ideas.repec.org/a/eee/jfinec/v136y2020i1p44-62.html
- Brown, Gredil & Kaplan (2019). Do PE funds manipulate reported returns? *JFE* 132(2):267–297. https://doi.org/10.1016/j.jfineco.2018.10.011 (NBER w22493: https://www.nber.org/papers/w22493)
- Brown, Ghysels & Gredil (2023). Nowcasting net asset values: the case of private equity. *RFS* 36(3):945–986. https://doi.org/10.1093/rfs/hhac045
- Callan (2025). Secondary investments. https://www.callan.com/?p=29041
- Cliffwater for ERSRI (2023). Pacing plan. https://data.treasury.ri.gov/dataset/40fb544c-65c5-464f-ba49-e3f65d1adc36/resource/7783fe26-a966-4850-82e0-f3f931812015/download/1a-cliffwater-pe-pc-ra-pacing-plan-dec-2023-final.pdf
- Evercore (Jul 2026). H1 2026 Secondary Market Review. https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
- Fang, Ivashina & Lerner (2015). Direct investing in PE. *JFE* 116(1). https://ideas.repec.org/a/eee/jfinec/v116y2015i1p160-178.html
- Gompers, Kaplan & Mukharlyamov (2016). What do PE firms say they do? *JFE* 121(3). https://www.nber.org/papers/w21133
- Harris, Jenkinson, Kaplan & Stucke (2023). Has persistence persisted? *JCF* 81. https://www.nber.org/system/files/working_papers/w28109/w28109.pdf
- ILPA (2017). Subscription lines of credit. https://ilpa.org/wp-content/uploads/2017/06/ILPA-Subscription-Lines-of-Credit-and-Alignment-of-Interests-June-2017.pdf
- ILPA (2023). Continuation funds. https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf
- ILPA (2024). NAV-based facilities. https://ilpa.org/wp-content/uploads/2024/11/Part-I-Nav-Based-Facilities-Guidance.pdf
- Jefferies (Jul 2026). Global Secondary Market Review. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- Jefferies (Jan 2025). Global Secondary Market Review. https://www.jefferies.com/wp-content/uploads/sites/4/2025/02/Jefferies-Global-Secondary-Market-Review-January-2025.pdf
- Korteweg & Sorensen (2017). Skill and luck in PE. *JFE* 124(3). https://research-api.cbs.dk/ws/files/55394727/morten_soerensen_skill_and_luck_in_private_equity_performance_acceptedversion.pdf
- Lazard (Aug 2026). Interim Secondary Market Report. https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf
- Ljungqvist & Richardson (2003). Cash flow, return and risk of PE. NBER w9454. https://www.nber.org/papers/w9454
- Lopez-de-Silanes, Phalippou & Gottschalg (2015). Giants at the gate: investment returns and diseconomies of scale in private equity. *JFQA* 50(3):377–411. https://doi.org/10.1017/s0022109015000113 ; https://ideas.repec.org/a/cup/jfinqa/v50y2015i03p377-411_00.html
- MSCI (Oct 2026). Private Capital Benchmarks Summary Q2 2026. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
- Nadauld, Sensoy, Vorkink & Weisbach (2019). The liquidity cost of private equity investments: evidence from secondary market transactions. *JFE* 132(3):158–181. https://doi.org/10.1016/j.jfineco.2018.11.007. The age-group and tail-end figures in §3.2 and §8 come from the NBER w22404 (2016) tables: https://www.nber.org/papers/w22404
- Takahashi & Alexander (2002). Illiquid alternative asset fund modeling. *JPM* 28(2). https://doi.org/10.3905/jpm.2002.319836
- Torys (2026). When "no fee" means "yes fee". https://www.mondaq.com/unitedstates/fund-management-reits/1821370/when-no-fee-means-yes-fee-the-hidden-costs-of-co-investing
- Unquote (2009). Secondaries pricing dips (Cogent). https://www.unquote.com/uk/news/85756/secondaries-pricing-dips-to-a-five-year-low
- Kaplan & Schoar (2005). Private equity performance: returns, persistence and capital flows. *JF* 60(4). https://dspace.mit.edu/handle/1721.1/5050
- Gredil, Griffiths & Stucke (2023). Benchmarking private equity: the direct alpha method. *JCF* 81, 102360 (seen via a secondary summary). https://altss.com/glossary/direct-alpha

**Capital Solutions and private credit**
- Blackstone (2026). Form 10-Q, Q2 2026. https://www.sec.gov/Archives/edgar/data/0001393818/000119312526340208/d158269d10q1.pdf
- Böni & Manigart (2022). Private debt fund returns, persistence, and market conditions. *FAJ* 78(4):121–144. https://doi.org/10.1080/0015198X.2022.2092384 ; https://rpc.cfainstitute.org/research/financial-analysts-journal/2022/private-debt-fund-returns-persistence-market-conditions
- Cai & Haque (2024). Private credit: characteristics and risks. FEDS Notes, 23 Feb 2024. https://doi.org/10.17016/2380-7172.3462 ; https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html. The recovery figures (Figure 15) are KBRA DLD data, not S&P.
- Cliffwater (Aug 2026). CDLI release. https://www.prnewswire.com/news-releases/private-credit-shows-resilience-in-cliffwater-direct-lending-index-data-302854703.html
- ECB (May 2026). Stress in global private credit markets. https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202605_04~3f2135af91.en.html
- Erel, Flanagan & Weisbach (2024). Risk-adjusting the returns to private debt funds. NBER w32278 (March 2024). https://www.nber.org/papers/w32278 (DOI 10.3386/w32278). An April 2026 draft revises most of the numbers; its conclusion, net risk-adjusted performance indistinguishable from zero, is unchanged.
- Expedia Group (2020). Form 8-K, preferred and warrants. https://www.sec.gov/Archives/edgar/data/1324424/000119312520117346/d913320d8k.htm
- Global Finance (Sep 2026). Fitch PCDR. https://gfmag.com/private-credit/fed-rate-hike-squeezes-an-already-stressed-private-credit-sector/
- IFR (2025). Verisure holdco PIK notes. https://www.ifre.com/ifr-awards/2332504/europe-high-yield-bond-verisure-holdcos-1bn-pik-notes
- KBRA DLD (Oct 2026). Monthly insights. https://www.kbra.com/analytics/products/dld/insights/monthly-insights-and-outlook-at-a-glance-october-14-2026
- Lincoln International (2026). Private Market Index, Q2. https://www.lincolninternational.com/news/the-lincoln-private-market-index-earnings-growth-drove-a-q2-rebound-while-private-markets-became-more-selective/
- Moody's Analytics (2009). Preferred stock default recoveries. https://ir.moodys.com/press-releases/news-details/2009/Moodys-Analytics-Preferred-Stock-Default-Recoveries-Approach-Those-of-Senior-Unsecured-Bonds/default.aspx
- Proskauer (2026). NAV financing market, FY2025. https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025
- Proskauer (2026). Private Credit Default Index, Q2 2026. https://www.proskauer.com/report/proskauers-private-credit-default-index-reveals-rate-of-251-for-q2-2026
- Rede Partners (Jun 2026). NAV Financing Market Report. https://www.rede-partners.com/s/NAV-Financing-Market-Report-2026_FINAL.pdf
- VRC (Oct 2026). Private market trends Q3 2026. https://www.valuationresearch.com/insights/private-credit-trends-q3-2026/
- Block, Jang, Kaplan & Schulze (2023/2024). A survey of private debt funds. NBER w30868, Table 3; *RCFS* 13(2). https://www.nber.org/papers/w30868
- Future Standard (7 Aug 2026). Unique issuers by market segment (Cliffwater data at 31 Mar 2026). https://www.futurestandard.com/insights/chart-of-the-week/private-credit-unique-issuers-market-segment
- KBRA DLD (22 Mar 2024), via SFNet. Sponsored vs non-sponsored defaults. https://sfnet.com/home/chapters/canada/news-detail/2024/03/25/kbra-dld-report-direct-lending-defaults-low-sponsored-at-1.5-non-sponsored-at-3.5
- KBRA (22 Jan 2025), via ai-CIO. An index of ≈2,400 borrowers. https://www.ai-cio.com/news/direct-lending-default-rate-expected-to-rise-to-3-in-2025/
- KBRA (27 Mar 2026). Private credit: deep dive on AI and software. https://www.kbra.com/publications/KztddwRk/kbra-releases-research-private-credit-deep-dive-on-ai-and-software
- LevFin Insights via CreditSights (21 Oct 2025). BDC portfolio overlap. https://know.creditsights.com/us-insight-lps-look-to-diversify-direct-lending-exposure-as-larger-deals-drive-bdc-portfolio-overlap/
- PitchBook LCD via Yahoo Finance (29 May 2026). Sponsored share of direct-lending deals. https://finance.yahoo.com/markets/stocks/articles/pe-backed-companies-losing-direct-223251276.html
- S&P Global Ratings (8 Dec 2023). Sponsor diversity can mitigate private markets risk [U: full text returned 403; not load-bearing]. https://www.spglobal.com/ratings/en/research/articles/231208-credit-trends-sponsor-diversity-can-mitigate-private-markets-risk-12940947

**Public markets and liquidity**
- Ang & Bollen (2010). Locked up by a lockup. *Fin. Mgmt* 39(3). https://ideas.repec.org/a/bla/finmgt/v39y2010i3p1069-1096.html
- Ben-David, Birru & Rossi (2020/2026). Performance of hedge fund performance fees. NBER w27454; *RCFS* 15(3):704–747 (2026). https://doi.org/10.1093/rcfs/cfag015 ; https://www.nber.org/papers/w27454
- Brooks, Gould & Richardson (2020). Active fixed income illusions. *J. Fixed Income* 29(4):5–19. https://doi.org/10.3905/jfi.2020.1.086 ; https://www.aqr.com/Insights/Research/Journal-Article/Active-Fixed-Income-Illusions
- Busse, Goyal & Wahal (2010). Institutional investment management. *JF* 65(2). https://ideas.repec.org/a/bla/jfinan/v65y2010i2p765-790.html
- Cambridge Associates (2008). Liquidity considerations. https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2014/12/Liquidity-Considerations-in-Todays-Environment-Oct-2008.pdf
- Cambridge Associates (2009). Is the "hedge fund business model" broken? https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2014/10/Is-the-Hedge-Fund-Business-Model-Broken-Jan-2009.pdf
- CME Group (2026). Funding the U.S. equity market. https://www.cmegroup.com/articles/2026/funding-the-us-equity-market-to-new-heights.html
- Cipriani, Martin, McCabe & Parigi (2014). Gates, fees and preemptive runs. FRBNY SR 670. https://www.newyorkfed.org/research/staff_reports/sr670.html
- D. E. Shaw (2025). Imbalance sheet. https://www.deshaw.com/library/imbalance-sheet
- Fung & Hsieh (2004). Hedge fund benchmarks. *FAJ* 60(5). https://ideas.repec.org/a/taf/ufajxx/v60y2004i5p65-80.html
- Gerakos, Linnainmaa & Morse (2021). Asset managers' returns. *JF*. https://consensus.app/papers/details/0212f272b5cf5989a5a878405e42c2d3/
- Getmansky, Lo & Makarov (2004). An econometric model of serial correlation and illiquidity in hedge fund returns. *JFE* 74(3):529–609. https://doi.org/10.1016/j.jfineco.2004.04.001 (NBER w9571: https://www.nber.org/papers/w9571)
- Hedgeweek (2009). Hennessee: 2008 redemptions. https://www.hedgeweek.com/redemptions-and-performance-losses-cut-hedge-fund-assets-usd782bn-says-hennessee/
- Hedgeweek (12 Jun 2026). ADIC weighs leveraged hedge fund push. https://www.hedgeweek.com/abu-dhabis-adic-weighs-15bn-leveraged-hedge-fund-push-via-swap-structures/
- Li, Strahan & Zhang (2020). Banks as lenders of first resort: evidence from the COVID-19 crisis. *RCFS* 9(3):472–500. https://doi.org/10.1093/rcfs/cfaa009 (NBER w27256: https://www.nber.org/papers/w27256). The abstract credits Fed liquidity programs, deposit inflows and strong capital for banks' ability to meet the March 2020 line draws. An oil–fiscal stress may lack that support.
- NBIM. GPFG investment mandate (rebalancing band). https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/
- OFR. Hedge Fund Monitor (Form PF). https://www.financialresearch.gov/hedge-fund-monitor/
- SEC (2025). Private Funds Statistics, Q3 2025. https://www.sec.gov/files/investment/private-funds-statistics-2025-q3.pdf
- Tóth et al. (2011). Anomalous price impact. *PRX* 1. https://arxiv.org/html/1105.1694v3
- WealthBriefing (2010). Hedgebay discounts. https://www.wealthbriefing.com/html/article.php/hedge-funds-trading-at-historic-discounts-_dash_-hedgebay

**Overlay, margin and regulation**
- BCBS. Basel Framework, LCR. https://www.bis.org/committees/bcbs/basel-framework/LCR/standard.pdf
- BCBS–CPMI–IOSCO (2022). Margining in March 2020. https://www.bis.org/press/p220929.htm
- Federal Reserve et al. (2010). SR 10-6, funding and liquidity risk. https://www.federalreserve.gov/boarddocs/srletters/2010/sr1006.htm
- FSB (2024). Liquidity preparedness for margin and collateral calls. https://www.fsb.org/2024/12/liquidity-preparedness-for-margin-and-collateral-calls-final-report/
- ISDA (2026). SIMM v2.8+2512. https://www.isda.org/a/hhkiE/ISDA-SIMM_v2.82512_PUBLIC.pdf
- 12 CFR §252.35 (Regulation YY). https://www.law.cornell.edu/cfr/text/12/252.35
- 17 CFR §270.17a-7. https://www.law.cornell.edu/cfr/text/17/270.17a-7
- 29 U.S.C. §1108(b)(19) (ERISA cross-trading). https://www.law.cornell.edu/uscode/text/29/1108
- 12 U.S.C. §371c-1 (Federal Reserve Act §23B). https://www.law.cornell.edu/uscode/text/12/371c-1
- AIMA. Revisiting issues involved in transferring positions (novation). https://www.aima.org/journal/aima-journal---edition-125-/article/revisiting-issues-involved-in-transferring-positions.html
- Cboe. Daily index files: SPX, VIX, VIX3M, VIX6M, VIX1Y, SKEW (data to 16 Oct 2026); Kenneth French data library, Fama–French factors (CRSP 202608).
- CPP Investments (2024). Annual Report F2024, pp. 20, 49–50. https://cppinvestments.com/wp-content/uploads/2024/05/CPP-Investments-F2024-Annual-Report.pdf
- Drechsler (2013). Index-option premia as a hedge against model misspecification (Consensus record verified in stream 09; title as recorded there not given). https://consensus.app/papers/details/71219fa7e399578680a3b58da1c70e3c/
- Fennell & Dunstan (Jun 2020). Portfolio completion. NZ Super Fund. https://fallback.nzsuperfund.nz/assets/Uploads/How-we-Invest-Portfolio-completion.pdf
- Haynes Boone (2016). ISDA publishes 2016 credit support annex for variation margin. https://www.haynesboone.com/news/alerts/isda-publishes-2016-credit-support-annex-for-variation-margin
- ISDA (1 Feb 2017). Risk Data Standards v1.36 (CRIF fields). https://www.isda.org/a/owEDE/risk-data-standards-v1-36-public.pdf
- ISDA. Credit-support documentation (2018 IM CSA). https://www.isda.org/book-taxonomy/credit-support-books/page/4/
- ISDA 2002 Master Agreement §7 (transfer), via Jolly Contrarian. https://jollycontrarian.com/index.php/Transfer_-_ISDA_Provision
- Iverson (31 Aug 2015). Managing investment risk and liquidity. NZ Super Fund. https://fallback.nzsuperfund.nz/assets/documents-sys/NZS180-Managing-Investment-Risk-Liquidity-White-Paper.pdf
- McElhaney (15 Apr 2020). Board member says CalPERS kept quiet about cutting tail hedge strategy. *Institutional Investor.* https://www.institutionalinvestor.com/article/b1l6npn5lqyd8g/Board-Member-Says-CalPERS-Kept-Quiet-About-Cutting-Tail-Hedge-Strategy
- Rampini, Sufi & Viswanathan (2014). Dynamic risk management. *JFE* 111(2) (Consensus record verified in stream 09). https://consensus.app/papers/details/e86c89b63aeb51dcaea2c9919a32ce73/
- Rampini et al. Risk management in financial institutions. NBER working paper (Consensus record verified in stream 09). https://consensus.app/papers/details/57b5729c2197580ea311659a6e2d3970/
- Segal (14 Apr 2020). The inside story of CalPERS' untimely tail hedge unwind. *Institutional Investor.* https://www.institutionalinvestor.com/article/2bsxabrnayd009kkvsd1c/portfolio/the-inside-story-of-calpers-untimely-tail-hedge-unwind

**Funding, recovery and fire sales**
- Acharya, Shin & Yorulmazer (2011). Crisis resolution and bank liquidity. *RFS* 24(6). https://www.nber.org/papers/w15567
- AidData. Mubadala $2bn five-year revolving credit facility, 28 MLAs, committed 1 May 2019. https://china.aiddata.org/projects/98914
- Allen & Gale (1994). Limited market participation and volatility of asset prices. *AER* 84(4). https://ideas.repec.org/a/aea/aecrev/v84y1994i4p933-55.html
- Bloomberg (19 Nov 2025). Indonesia's Danantara taps banks for $1 billion credit line. https://www.bloomberg.com/news/articles/2025-11-19/indonesia-s-danantara-taps-banks-for-1-billion-credit-line ; IDN Financials (20 Nov 2025). https://www.idnfinancials.com/news/58899/danantara-partners-with-four-global-banks-for-us1-bn-credit-facility. Read at snippet level; terms unconfirmed.
- Boyd & Vandenberghe (2004). *Convex Optimization*, §11.4 (Phase I). https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
- BXP, Inc. Form 8-K (event 28 Mar 2025): revolver at SOFR + 85bp. https://www.sec.gov/Archives/edgar/data/1037540/000165642325000014/bxp-20250328.htm
- Chinneck (2008). *Feasibility and Infeasibility in Optimization.* Springer ISOR 118.
- Clopper & Pearson (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4):404–413. https://doi.org/10.1093/biomet/26.4.404 (the CP bounds in §0, §2.4)
- EBA (19 Jul 2023). Guidelines on overall recovery capacity in recovery planning, EBA/GL/2023/06. https://www.dirittobancario.it/wp-content/uploads/2023/07/Final-Report-on-GLs-on-overall-recovery-capacity-in-recovery-planning.pdf
- EIOPA. Solvency II Directive 2009/138/EC, Art. 138. https://www.eiopa.europa.eu/rulebook/solvency-ii-single-rulebook/article-2225_en
- Gulf News (28 Aug 2024). Saudi wealth fund PIF gets new $15 billion revolving credit facility. https://gulfnews.com/business/markets/saudi-wealth-fund-pif-gets-new-15-billion-revolving-credit-facility-1.1724830841938
- Nocedal & Wright (2006). *Numerical Optimization*, 2nd ed., Thm 17.3. https://pages.mtu.edu/~struther/Courses/OLD/Other/LessOld/5630_11/NocedalAndWright/Chpt17.pdf
- Shleifer & Vishny (2011). Fire sales in finance and macroeconomics. *JEP* 25(1). https://www.nber.org/papers/w16642

**Organizational economics, forecasting and synthetic data**
- Baumol & Fabian (1964). Decomposition and pricing for decentralization. *Mgmt Sci.* 11(1). https://ideas.repec.org/a/inm/ormnsc/v11y1964i1p1-32.html
- Ben-David, Graham & Harvey (2013). Managerial miscalibration. *QJE* 128(4). https://www.nber.org/papers/w16215
- Bracher, Ray, Gneiting & Reich (2021). Evaluating forecasts in interval format. https://arxiv.org/abs/2005.12881
- Campbell & Sharpe (2007). Anchoring bias in consensus forecasts. FEDS 2007-12. https://www.federalreserve.gov/pubs/feds/2007/200712/200712pap.pdf. Published in *JFQA* 44(2):369–390 (2009), https://doi.org/10.1017/s0022109009090127
- CEBS (2010). Guidelines on liquidity cost–benefit allocation. https://www.eba.europa.eu/sites/default/files/documents/10180/16094/da61d4c3-3937-4612-9584-e6136cb98191/cebs18_Guidelines.pdf
- FSI (2011). Liquidity transfer pricing. https://www.bis.org/fsi/fsipapers10.htm
- Gneiting & Raftery (2007). Strictly proper scoring rules. *JASA* 102. https://ideas.repec.org/a/bes/jnlasa/v102y2007p359-378.html
- Scharfstein & Stein (2000). The dark side of internal capital markets. *JF* 55(6). https://www.nber.org/papers/w5969
- Smith & Winkler (2006). The optimizer's curse: skepticism and postdecision surprise in decision analysis. *Mgmt Sci.* 52(3):311–322. https://doi.org/10.1287/mnsc.1050.0451 ; https://ideas.repec.org/a/inm/ormnsc/v52y2006i3p311-322.html
- Talts et al. (2018). Simulation-based calibration. https://arxiv.org/abs/1804.06788
- Weitzman (1980). The ratchet principle. *Bell J. Econ.* 11(1). https://ideas.repec.org/a/rje/bellje/v11y1980ispringp302-308.html
- Bailey & López de Prado (2014). The deflated Sharpe ratio: correcting for selection bias, backtest overfitting, and non-normality. *JPM* 40(5). https://doi.org/10.3905/jpm.2014.40.5.094 ; https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- Castro, Gómez & Tejada (2009). Polynomial calculation of the Shapley value based on sampling. *Computers & Operations Research* 36(5). https://doi.org/10.1016/j.cor.2008.04.004
- Easterwood & Nutt (1999). Inefficiency in analysts' earnings forecasts. *JF* 54(5). https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1777-1797.html
- Mitchell, Cooper, Frank & Holmes (2022). Sampling permutations for Shapley value estimation. *JMLR* 23(43). https://www.jmlr.org/papers/v23/21-0439.html
- Staw, Barsade & Koput (1997). Escalation at the credit window. *J. Applied Psychology* 82(1). https://experts.arizona.edu/en/publications/escalation-at-the-credit-window-a-longitudinal-study-of-bank-exec/

**Verified in the G8 literature review (2026-10-18):** Fissler & Ziegel (2016). Higher order elicitability and Osband's principle. *Annals of Statistics* 44(4):1680–1707. https://doi.org/10.1214/16-aos1439. It shows that (VaR, ES) is jointly elicitable.

**Consensus.** For all four groups addenda the Consensus tool returned its monthly-quota message ("You've used all 500 included searches this month; resets on November 1st."). No new academic sources came from it. The entries above were verified on publisher, repository and press pages, or are Consensus records already verified in the corpus.

*SYNTHETIC – NOT ADIC DATA (all [I-calc] figures).*

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2, the per-topic files `research/literature/*.lit.md`, the recheck files in `research/literature/recheck/`, and the barrier re-run `research/groups/addenda/G4_barrier_rerun/RESULTS.md`. One line per change.

- §1 finding 8: wipe-out labelled "at exit" with the E3-barrier sensitivity 7.6% → 22.9%; LTV breach gains "62–73% if monitored continuously"; new line records that the barrier re-run leaves both rates unchanged (RESULTS.md §5).
- §3.1 parameter table, "Risk; smoothing": AC1 0.66–0.71 re-attributed as a derivation from Brown–Ghysels–Gredil's working-paper smoothing estimates (weekly λ 0.951; quarterly AR(2)), not a published-abstract figure; β and total risk stay [S] (literature synthesis §2.4 items 4 and 8).
- §3.2 parameter table: Nadauld buyer–seller PME gaps cited to the NBER w22404 (2016) age-group tables, not the 2019 *JFE* version; the 82.2% tail-end price is sourced to w22404 Table 3 (G2 lit, ref 11).
- §3.2 constraints: Boyer et al.'s β > 2 marked unverified against the 2023 *JF* version, whose abstract reports no betas (literature synthesis §2.4 item 6).
- §3.4 model row: the barrier V ≤ κD is monitored continuously, and a quarterly simulation checks $\kappa D\,e^{+0.5826\sigma\sqrt\Delta}$ or steps weekly or finer (literature synthesis §2.4 item 1; RESULTS.md §1, §7).
- §3.4 model row: post-recap distress multiplier 1.4–3.4 (central 2.0) → about ×1.1 (OLS) to ×1.7 (IV) at φ = 0.25; 1.4–3.4 belongs to the paper's +84% debt recap (literature synthesis §2.4 item 2).
- §3.4 REFINANCE row: 49.6% / 62.5% kept as correct for a quarterly-tested covenant; continuous 62.2% / 73.4% and monthly 54.6% / 67.0% added (RESULTS.md §5.1).
- §3.4 LEVER row: wipe-out labelled "at exit"; E3-barrier values 2.2% → 11.8% and 7.6% → 22.9% added (RESULTS.md §5.2).
- §4.5: Böni–Manigart's spread effect restated per Table 5 (significant for net multiples and IG/HY bond-benchmark outperformance, insignificant for IRR); the TED effect is kept (G3 recheck, ref 43).
- §4.9 limits: new bullet on gap_04's quarterly co-investment write-off barrier (V < 0.85D, no shift; ≈0.92D equivalent), which was not re-run (RESULTS.md §6.3).
- §8 calibration targets: Nadauld tail-end price and buyer PME sourced to NBER w22404 Tables 3 and 6, labelled buyout tail-end (G2 lit; G2 verification log).
- §10 Albertus & Denes: full 2020 title, SSRN 3410076 version, and the Crossref-confirmed *JFQA* record (online 7 May 2026, DOI 10.1017/s0022109026102890) added as the probable successor; figure carry-over marked unverified (literature synthesis §2.6 item 3; G1 lit).
- §10 Bhardwaj, Gupta & Howell: exact title, DOI 10.3386/w33435, and the +84% debt scope of "2.4 times the targeted firm mean" (G4 lit).
- §10 Boyer et al.: now *JF* 78(2):835–885 (2023), DOI 10.1111/jofi.13202 (Crossref), with NBER w25207 (2018) and w28691 (2021) as earlier versions (literature synthesis §2.4 item 6; G2 lit).
- §10 Brown, Gredil & Kaplan: pages 267–297 and DOI 10.1016/j.jfineco.2018.10.011 (G1 and G9 lit).
- §10 Brown, Ghysels & Gredil: full title and pages 945–986 (G2 and G3 lit).
- §10 Lopez-de-Silanes, Phalippou & Gottschalg: full title, pages 377–411, DOI 10.1017/s0022109015000113 (literature synthesis §2.4 item 3; G4 lit).
- §10 Nadauld et al.: full title, pages 158–181, DOI 10.1016/j.jfineco.2018.11.007; w22404 named as the source of the §3.2 and §8 figures (literature synthesis §2.3; G2 and G7 lit).
- §10 Böni & Manigart: full title, pages 121–144, DOI 10.1080/0015198X.2022.2092384 (G3 recheck).
- §10 Cai & Haque: date, DOI 10.17016/2380-7172.3462, and the KBRA DLD source of the recovery figures (G3 recheck; G6 lit).
- §10 Erel, Flanagan & Weisbach: full title, March 2024 version, DOI 10.3386/w32278, and the April 2026 draft note (G3 recheck).
- §10 Ben-David, Birru & Rossi: *RCFS* 15(3):704–747 (2026), DOI 10.1093/rcfs/cfag015 (G5 lit).
- §10 Brooks, Gould & Richardson: *J. Fixed Income* 29(4):5–19, DOI 10.3905/jfi.2020.1.086 (G5 lit).
- §10 Getmansky, Lo & Makarov: full title, pages 529–609, DOI 10.1016/j.jfineco.2004.04.001 (literature synthesis §2.2 item 4).
- §10 Li, Strahan & Zhang: full title, pages 472–500, DOI 10.1093/rcfs/cfaa009, and the abstract's Fed-support condition for the 2020 line draws (literature synthesis §2.4 item 14; G7 lit).
- §10 Clopper & Pearson (1934): new entry for the CP bounds used in §0 and §2.4, *Biometrika* 26(4):404–413, DOI 10.1093/biomet/26.4.404 (Crossref) (literature synthesis §2.5).
- §10 Campbell & Sharpe: FEDS number and the published version, *JFQA* 44(2):369–390 (2009), DOI 10.1017/s0022109009090127 (G9 lit).
- §10 Smith & Winkler: full title, pages 311–322, DOI 10.1287/mnsc.1050.0451 (stream-10 recheck).
- §10 Bailey & López de Prado: full title, *JPM* 40(5), DOI 10.3905/jpm.2014.40.5.094 (stream-09 lit).
- §10 Fissler & Ziegel: the [U] line replaced by the verified record, *Annals of Statistics* 44(4):1680–1707, DOI 10.1214/16-aos1439 (G8 lit).
