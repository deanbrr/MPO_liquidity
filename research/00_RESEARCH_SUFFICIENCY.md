# Research sufficiency: did the research find enough to answer the ADIC task?

*Lead research reviewer, 2026-10-18, about 18:30. This review synthesizes the 16 audits and 16 skeptic challenges in `research/sufficiency/`. It checks them against the brief, the context file, synthesis v1.1, groups synthesis v1.1, the addenda and the literature synthesis. It is read-only, and no engine was re-run.*

> **SYNTHETIC – NOT ADIC DATA.** Every ADIC-like figure comes from the synthetic book (allocation v1, census v1.0, seven groups) and the six proxy models M1–M6, unless it is tagged [S] or "public data".

**Conventions**
- **Tags:**
  - [S] sourced and verifier-confirmed;
  - [C] corrected or checked;
  - [I] inference or default;
  - [I-calc] computed by the research;
  - *arithmetic* means a reviewer's own derivation, not a research result.
- **File keys:**
  - *main* = `research/00_SYNTHESIS.md`;
  - *groups* = `research/groups/01_GROUPS_SYNTHESIS.md`;
  - *gap_0x* and *G-gap_0x* = the main and groups addenda;
  - *lit* = `research/literature/00_LITERATURE_SYNTHESIS.md`;
  - *brief* = `design/00_DESIGN_BRIEF.md`;
  - *Qnn-A* and *Qnn-C* = the audit and the challenge for question nn.
- **Readiness levels:**
  - **DESIGN:** enough to design the component.
  - **BUILD:** codable and testable now, leaving only choices an ADR can settle.
  - **IC:** a defensible answer today, on synthetic data, with stated uncertainty. *Directional* means the direction is robust but no level can be quoted.
  - **DATA:** the answer for the real portfolio needs ADIC data.

## 1. Verdict

**The research is enough to design the framework and to argue its main conclusions directionally, but not enough to give the IC numbers or to solve the problem for ADIC's real portfolio.** *Design* is ready in all sixteen areas: for the seven original groups, every component has equations, defaults, validation tests and literature-checked mechanisms with the verifiers' corrections applied, and the literature sweep changes conventions, not the architecture (lit §1, §4); Real Assets, added at about 17:40, has only the brief's interim rules (§8). *Build* is ready for four components only (the return bridge, the liquidity ladder with contingency-funding stages, the Phase-1 owner-draw engine and the probability-certification harness); the optimizer H, scenario engine E, stochastic private engine, opportunistic overlay book and belief-fusion estimands need more specification, and `design/BUILD_SPEC.md` does not exist yet. *The IC* can be given robust directions on eight of sixteen requirements (§3): 10% is a stretch, the upper half of the payout band is real decumulation, the liquid book must fund the drought, doing nothing breaches the 1% red-event tolerance, leverage is a liquidity tool, P(10%) must never be maximized, and the v8 deck's architecture survives while its numbers do not. No figure is IC-grade yet, because every result sits on inputs the user has since replaced (allocation v1, census v1.0, seven groups), uses conventions the literature overturned (the revolver credited at 80% in a crisis, an owner band always granted, a fixed waterfall), and comes from five or more prototypes rather than one engine; the research's own rule keeps such results out of IC use until they are replicated (main §9.2 item 10). *Solving it for the real portfolio* needs ADIC's data (§6), the Real Assets research and the build. As a case-study answer of the kind the v8 deck gave, the research is more than sufficient; as the basis for an IC decision on the real book, it is a complete design with indicative synthetic numbers.

**Tally:**

| Measure | Count |
|---|---|
| Final verdict: mostly sufficient | 3 (Q05, Q11, Q13) |
| Final verdict: partial | 13 |
| DESIGN ready | 16 of 16 |
| BUILD ready | 4 of 16 |
| IC answer, directional or better | 8 of 16 |
| Needs ADIC data | 14 of 16 |

## 2. Sufficiency matrix

| Q | Requirement | Audit → challenge | **Final** | DESIGN | BUILD | IC | DATA | One-line answer |
|---|---|---|---|---|---|---|---|---|
| Q01 | R1 multi-period optimizer | partial → partial | **Partial** | Yes | Partly (P, F, Phase I/II; not H) | No | No | The formulation is sound. H as specified (≈1.2–1.8M variables per model) is untimed and probably misses the 2-minute HiGHS target |
| Q02 | R2 robust scenario analysis | mostly → partial | **Partial** | Yes | No | No | Yes | E is designed but never built. Scenario numbers come from quarterly Gaussian proxies with no oil path, and differ 2.6–70× by engine |
| Q03 | R3 probabilities of outcomes | mostly → partial | **Partial** | Yes | Yes (harness only) | No | Yes | The certification harness is code-ready. No probability comes from E, and red-event levels move up to ≈70× between engines |
| Q04 | R4 owner's 5–10% draw | mostly → partial | **Partial** | Yes | Yes (Phase 1, after six ADR choices) | Directional | Yes | The structure is credible; the calibration is priors on UAE-level anchors. The upper half of the band is real decumulation in all six models |
| Q05 | R5 10% nominal target | mostly → mostly | **Mostly sufficient** | Yes | Yes (`bridge.py`) | Directional | Yes | Expect ≈8.1–8.3%. 10% needs leverage at the cap plus above-median levers, and is a robust plan in no model |
| Q06 | R6 leverage | mostly → partial | **Partial** | Yes | No | Directional | Yes | The doctrine holds: lever the liquid book and overlay, never PE or single assets, and add none in recovery. Facility sizing is stale |
| Q07 | R7 private book, declining DPI | mostly → partial | **Partial** | Yes | No | Directional | Yes | Distributions halve while calls hold [S]. The drought sign, PE's share of the drain and pacing relief depend on the census and the engine |
| Q08 | R8 SELL / HOLD / REFI / LEVER | mostly → partial | **Partial** | Yes (7 groups) | No | No | Yes | One kernel per group. Card verdicts conflict across files, are not kernel valuations, and flip on the undecided revolver convention |
| Q09 | R9 fusion of the return marks | mostly → partial | **Partial** | Yes (7 groups) | No | No (method only) | Yes | Specified at equation level. Group bias and credibility are priors, the test hands estimators the true noise, and the market anchor is unidentified |
| Q10 | R10 OTC overlay | mostly → partial | **Partial** | Yes | No (equity tail slice close) | Directional | Yes | SIMM netting is not an economic offset; cash beats options as liquidity insurance. The opportunistic book is a prior |
| Q11 | R11 agentic architecture | mostly → mostly | **Mostly sufficient** | Yes | No (no BUILD_SPEC, no drills) | Yes (scoped) | No | Grounded in the paper's failure evidence. The controls are specified, not demonstrated, and the paper does not validate them |
| Q12 | R12 IC discussion | mostly → partial | **Partial** | Yes | No | No | Yes | Designed, with strong failure-mode evidence. No remedy has positive efficacy evidence in a committee, and nothing has run |
| Q13 | R13 build on deck v8 | mostly → mostly | **Mostly sufficient** | Yes | No | Directional | Yes | The skeleton survives; the floor, objective, lights and +3.5pp do not. The replacement floor fails at t0 in three of six models |
| Q14 | R14 groups + CF capital market | mostly → partial | **Partial** | Yes (Real Assets interim) | No | No (qualitative) | Yes | Designed for seven groups. Prices restate assumed lever costs and exist only under the contested band; Real Assets is missing |
| Q15 | R15 synthetic data | mostly → partial | **Partial** | Yes | No (truth engines, labels only) | Yes (role, limits) | Yes | The O1 term, estimand map, stylized-fact thresholds and SBC mode are missing. It may test correctness, never choose estimators |
| Q16 | Liquidity survival, CF funding | mostly → partial | **Partial** | Yes | Yes (narrowly) | No | Yes | T4′ needs ≈$14bn of revolver at 80% credit but ≈$22bn at the brief's 50% (arithmetic). Nothing has been run on the current book |

### Where the reviewers disagreed

Four systematic findings drive almost every downgrade from "mostly sufficient" to "partial". I checked each against the brief and the context file.
1. **Superseded inputs.**
   - The user chose census v1.1: PE unfunded $16.4bn, not $27.4bn.
   - Allocation v2 moves $18bn from PE to Real Assets.
   - None of the seven-group numbers has been re-run (context §1A; brief §8).
2. **Literature conventions not applied.**
   - Brief §7 items 1–3 require ≤50% revolver credit in the joint oil–crisis state, the band only with written agreement, and a state-dependent waterfall.
   - `t1_engine.py` instead credits 80–90%, always grants the band and keeps the fixed waterfall (Q03-C, Q16-C).
3. **No single engine.** There are five or more prototypes with different conventions, a closed-form bridge, and no engine E.
4. **The research's own rule.** Unreplicated [I] results stay out of IC use (main §9.2 item 10; gap_05 §10).

| Q | Decision | Why |
|---|---|---|
| Q02 | Skeptic | E is unbuilt. The M6 "floor" is an engine artefact: Mix B goes from 6.4% to 0.09% once the playbooks run (G-gap_04 §2). The audit was too harsh on world assignment, which ARCHITECTURE §4.1 and §7.5 settle |
| Q03 | Skeptic | Mix A certifies by 2bp (CP 0.979% in M5) and fails at 10k paths (1.14–1.16%). Mix B breaches gap_02's own M6 band (6.46%) |
| Q04 | Skeptic | With ρ_d = 0.5, the 2027 draw cannot pass 7.9% without an override, so the near-term tail restates the override prior. The engines' year-1 draws differ: ≈7.7% vs 5.6–6.1% |
| Q06 | Skeptic | Sizing uses census v1.0 at 80% credit. Doctrine test 3 relies on ΔP(10%), which the framework rejects. "Not a route to 10%" holds only at the [I] 1.30× cap |
| Q07 | Skeptic | On v1.0, the engine's own drought rates plus MSCI's 9% PE rate put net cash at ≈−$0.3bn, not +$2.2bn. A two-quarter pacing lag lifts the need with the cut from $6.1bn to ≈$8–9bn. Both are arithmetic |
| Q08 | Skeptic | The same fund is priced at 87.7%, a SELL (main §4.4), and at 90.7%, a HOLD (groups §4.8). No card comes from the production kernel |
| Q09 | Skeptic | The prototype gives estimators the true noise SDs and never estimates κ. With δ\* corrected (≈91bp), "pay design is a precondition" fails |
| Q10 | Skeptic | The opportunistic book gets +0.37pp a year, conditional on a DSR gate its own example fails (DSR 0.86). The joint engine hard-codes OV1 |
| Q12 | Skeptic | The audit's own flags (BUILD no, IC no) contradict "mostly sufficient". The blind pre-vote's source study found no accuracy gain |
| Q14 | Skeptic | The R0 and R1 duals equal assumed lever costs (0.243, 0.011). FTP exists only under Mix B; Mix A is infeasible at appetite |
| Q15 | Skeptic | The O1 equation was withdrawn and not replaced. Without an estimand map, SBC is ill-posed. The sealed truth is printed in research files |
| Q16 | Skeptic | "Literal T4 cannot be bought, T4′ can" compares 50% with 80% credit. At 50%, T4′ also exceeds PIF's $15bn precedent |

**Where the audit stands:**
- **Q01.** A single-process run of 10k paths × 20 quarters took 6.5 s (`g04_validate_results.json`), so the 60-second evaluation target is likely met. Tuning is the bottleneck: CMA-ES needs ≈52 core-hours.
- **Q05.** Its direction survived every perturbation the challenger tried.
- **Q11.** ARCHITECTURE §7 already settles most of the build defaults.

## 3. What we can tell the IC today

Every row is SYNTHETIC unless tagged [S] or "public data".

| # | Message | Numbers | Range | Source [tag] | Firmness |
|---|---|---|---|---|---|
| 1 | **10% is a stretch, not the plan; the upper half of the band is real decumulation** | E[R] 8.3% (mixture); P(10-year TWR ≥ 10%) 36% (equal-weight mean). Holding real NAV needs ≈7.9 / 10.8 / 13.9% at a 5 / 7.5 / 10% payout | E[R] 6.1–10.5% and P 19.6–54.1% across M1–M6. Real-preserving payout ≈3.4–7.2% (arithmetic) | gap_05 §6; main §2.3(a), §1 f1 [I-calc]; lit §4.1 | **Firm direction.** M2's lone "Plan" (10.47%) drops to 9.93% on a v2 proxy (Q05-C) |
| 2 | **Model choice, not sampling, drives uncertainty** | Mean returns disperse 3–4pp across CMA providers, against ≈0.2pp of Monte Carlo error | P(10y ≥ 10%) spans 20–54% across models | main §1 f2 [C] | **Firm.** Lead every probability with its model range |
| 3 | **The DPI drought is a liquidity regime that the liquid book must fund** | PE distributions ≈9% of NAV (H1-26) vs 17–24% (2017–20); calls 27–31% [S]. Private-book drought net cash +$3.7bn over 12 months on v1.1 | +$2.6bn to +$5.3bn across truth variants; ≈−$0.3bn possible on v1.0 | main §7.1 [S]; groups §1 f3 [I-calc]; Q07-C | **Firm** on distributions and calls. **Not firm** on the net-cash sign |
| 4 | **Doing nothing breaches the 1% red-event tolerance** | P(red event within 5 years) on the do-nothing book | 6.1–37.2% (gap_02 engine, M1–M6); 1.6–14.5% (group engine, M1 / M4 / M6) | gap_02 §2.1; G-gap_04 §2 [I-calc] | **Firm direction**; levels differ 2.6–4.9× by engine |
| 5 | **Clearing the 24-month stress needs committed liquidity, a pacing rule or the band** | Survival 17 months under T4′; 30-day coverage 1.91× (Amber); usable IG + cash 7.7% of NAV, $0.56bn short of 8% | Facility need: $13.9bn at 80% credit, ≈$22bn at 50%; with the pacing cut, $6.1bn and ≈$9.8bn; $0 with the band. The 50% figures are arithmetic | main §2.3(d); gap_02 §1.3; groups §1 f6, C12 [I-calc; C] | **Firm direction**; no size until the re-run |
| 6 | **The owner mandate is the most valuable unknown** | Certified mixes cost 21bp a year with a crisis band (Mix B) and 62bp without (Mix A); repriced, 23–29 vs 66–76bp. The band activates in 12–22% of paths within a year | M1–M5 only. In M6, Mix B scores 6.46% in gap_02 but 0.09% in the group engine (no slippage) | gap_02 §2.3; G-gap_04 §7 [I-calc]; lit §4.2 (contested) | **The question is firm**; the ranking is not (Mix A passes by 2bp) |
| 7 | **Lever the liquid book and the overlay, never PE or single assets** | At the 1.30× cap, M1 E[R] goes 8.84% → 9.66% and volatility 14.4% → 18.2%; M6 E[R] falls 6.06% → 5.88%. A holdco PIK lifts co-investment wipe-out 7.0% → 22.8% | M1 break-even 1.42× (peer level). Asset-level LEVER needs ≲SOFR+300bp (one example) | main §4.12 [I-calc]; groups §1 f8 [C]; 08 verify R4 [C] | **Doctrine firm**; ≤1.0× while in recovery |
| 8 | **Never maximize P(10%)** | With leverage, a toy model doubles P(target) from ≈34% to ≈68%, at a ≈4.6% chance of losing more than 40% | — | main §1 f9 [I]; Browne [S]; lit §4.7 | **Mechanism firm**; the toy numbers are illustrative |
| 9 | **Deck v8: the architecture survives, its numbers do not** | The +3.5pp uplift falls to +0.35–0.61pp: ≈29% was path knowledge, ≈54% unevidenced. The v8 floor needs a 15.8–17.9% expected return. Turbulence and absorption are not shown to add information (public data) | The replacement floor (worst-model CVaR₁₀ ≥ 0) fails in M3 (−0.78%), M6 (−1.54%) and M5 (−0.03%) | gap_05 §8; verify-10 #7 [C]; gap_04 §4 [I-calc]; Q13-C (arithmetic) | **Firm direction**; the floor must be re-specified |
| 10 | **Govern overlay offsets on economic vega; cash beats options as liquidity insurance** | SIMM cuts IM 31% for short 1-month straddles against long 6-month puts. In a 2020 replay the straddles lost $690m while the puts gained $389m. The 0.15% floor buys a $7.1bn ladder paying ≈$1.2bn in S1 | Runway ≈1–1.4 months from a convex sleeve, against ≈5.6–9 months from a facility | gap_03 §7.4; G-gap_03 §1, §5; C3 §5.7 [I-calc] | **Firm direction**; the opportunistic return cannot be quoted |
| 11 | **Read the state in layers: markets calm, exit and owner layers stressed** | F_t 0.10 against a 0.17 base rate; drought posterior 0.87; Gulf-war posterior 0.85 (elicited) | P(stress within 12 months) 13–35% across filters | gap_04 §4.2, §6.2 [I-calc, public data] | **Moderate.** Brier skill is only 2.4–8.1% |
| 12 | **The lab is grounded in the paper's failure evidence; its controls are undemonstrated** | In 2 of 3 Kimi K3 + Pi runs, the agent changed the evaluation protocol and no gate flagged it. Worker scaling was tested with 1, 2 and 4 workers on one task (3 seeds) | — | paper l.1224–1234, l.1159–1169 [S] | **Firm on grounding.** No lab output exists |

**Not quotable yet:**
- facility size and the Mix A/B certification or ranking;
- the card verdicts;
- the drought sign on v1.0 and PE's share of the drain;
- over-commitment;
- FTP and envelope levels, and the Shapley shares;
- the per-model Plan / Stretch labels;
- "pay precondition" and "FBE-R is robust";
- the opportunistic +0.37pp and the floor residual;
- the co-investment LTV-breach rates (§5).

## 4. What the research could not settle (ranked)

| # | Gap (questions affected) | Impact | How to close | Owner |
|---|---|---|---|---|
| 1 | **Superseded inputs:** every number uses allocation v1, census v1.0 and seven groups (Q02–Q08, Q14, Q16) | **High.** T4′, θ\*, the facility need, Mixes A/B, envelopes, FTP, Shapley values and the bridge all move. Literal T4's need roughly halves on v1.1 | **Build-time experiment:** re-run on census v1.1 (report $16.4bn and the ≈$10.9bn v2 rescale) and on allocation v2 | The build; the user confirms the $18bn Real Assets size |
| 2 | **Revolver availability** in the oil–crisis state (80% vs ≤50%), with brief §7's other conventions: no band by default, a state-dependent waterfall, a two-quarter pacing lag, the ≈1.1pp tightening premium (Q03, Q06, Q08, Q14, Q16) | **High.** The T4′ need goes from $13.9bn to ≈$22bn; Mix A's 2bp margin likely breaks | **Build-time experiment:** a 0–80% sweep with GCC-lender wrong-way risk. **ADIC data:** existing lines. **ADR** on availability | Corporate Finance; the build |
| 3 | **No single validated engine:** E is unbuilt, and M6's red-event rate is 6.5% in one engine and 0.09% in another (Q01–Q03, Q07, Q10, Q16) | **High.** No probability or price is IC-grade | **Build-time experiment:** E plus one integrated simulator; re-certify at 50k paths with playbook slippage | The build; Risk (MRM) |
| 4 | **The owner mandate:** band agreement and the owner's acceptance in a demand bust; draw convention and history; Abu Dhabi breakeven; ω (Q04, Q16) | **High.** Mix A vs Mix B is ≈40–50bp a year. The draw convention moves literal T4 between $25bn and $43bn | **User decision**; **ADIC data** from the owner | User / CIO with the owner; Corporate Finance |
| 5 | **Real Assets:** no engine parameters, bias priors, action pricing, CMA line or oil coupling (Q04, Q06–Q09, Q14–Q16) | **High.** Oil wrong-way risk with the owner's draw now sits in ADIC's own book | **Further research** (G10–G15 in progress); **ADIC data** | Real Assets group; the build |
| 6 | **Hedge-fund terms τ and PE vintages** (Q07, Q08, Q16) | **High.** τ sets the stage metrics; vintages set over-commitment and T4′ | **ADIC data** | Public Markets; PE |
| 7 | **A narrow ensemble:** one factor architecture, JPM risk everywhere, one private-markets model, ambiguity on means only (Q02, Q03, Q11) | **High.** Tail ambiguity is understated | **Build-time experiment:** provider vols, dwell-time variants, a second private engine | The build; Risk |
| 8 | **Optimizer H:** unbenchmarked; decision-rule form undefined; no rule for when the P–H loop has converged; the T6 tail rests on ≈6 leaves; the T6 dual is open (Q01, Q08, Q14) | **High** for the build | **Build-time benchmark** of three H variants; **user decision** on which is interactive | The build; user |
| 9 | **The Tier-1 floor:** v8's floor is infeasible, and its replacement fails at t0 in three of six models (Q13, Q03) | **High.** It gates every action | **User decision**, then a build-time test | User; Risk (CRO) |
| 10 | **Group forecast credibility** is priors; FBE-R was chosen on synthetic evidence (Q09, Q14, Q15) | **High** for R9 | **ADIC data:** a bitemporal archive, started now. **Build-time experiment** with estimated noise | Each group; the build |
| 11 | **Overlay:** the cash test has not run; the opportunistic return is a prior; three pricers; no λ^w estimator (Q10) | Medium–high | **Build-time experiment**; **ADIC data** (blotter, trial list) | Overlay group; Corporate Finance |
| 12 | **Governance parameters:** model weights (JPM holds 3 of 6 seats), M6's weight, the T6 bands, θ\*, η, the leverage cap, the target, the 8% floor. A hard 8% floor adds ≈$4.7bn to the gap (Q02, Q03, Q05, Q06, Q16) | Medium–high | **User decision** (IC ratification) | User / IC; Risk |
| 13 | **The lab and the IC module have never run:** no drills, no shadow IC, no BUILD_SPEC, no threat model (Q11, Q12) | Medium | **Build-time experiment**, then 6–12 months of shadow mode | The build; Risk; user |
| 14 | **Citations:** errors unfixed; 12 G3 works unchecked (all questions) | Low–medium | **Further research:** fixes running now; Consensus after 1 November | The build (research) |

## 5. Evidence-quality caveats

1. **Synthetic data.**
   - All ADIC-like numbers are SYNTHETIC: allocation v1; census v1.0, whose history fails the research's own gate V6; and stylised proxy models.
   - The targets are mostly US proxies, with one drought spell and no analogue for the frozen state or a Gulf war.
2. **The decision-critical addenda are unverified.**
   - gap_02 (T4′, T6), gap_03, gap_04, gap_05 and the groups addenda have no adversarial logs.
   - The challengers' replications from the results JSON check arithmetic, not realism.
3. **Unchecked citations.**
   - The quota left 69 works unchecked (lit §2.1).
   - `research/literature/recheck/` has since checked 57 through Crossref, OpenAlex and arXiv: none fabricated or missing, 4 metadata mismatches, and 6 usage problems, none of which changes a number.
   - One of those six matters: Fogliato found no accuracy gain from human-first ordering, which undercuts the blind pre-vote.
   - The 12 G3 works remain unchecked; a Consensus pass is due after 1 November.
4. **Errors still to fix.**
   - **Count.** lit §2 lists 24 mismatches, 16 usage errors and 5 cross-file inconsistencies. No fix log existed at 18:30.
   - **Co-investment barrier.** The Broadie–Glasserman–Kou shift in G4 has the wrong sign, and the script applied none.
     - The re-run is in progress, with no `RESULTS.md` yet.
     - Preliminary, unreviewed output (`G4_barrier_rerun/check_decisions_bgk_results.json` [I-calc]): wipe-out barely moves. In drought it goes from ≈7.2% to ≈7.5% unlevered, and from ≈22.9% to ≈23.0% with the PIK.
     - The 1.5× LTV-trigger breach rate rises from 49.6% / 62.5% to ≈62% / ≈73% if the covenant is monitored continuously. It is unchanged if the covenant is tested quarterly.
     - Either way, single-asset leverage stays rejected.
   - **Other errors that change a method, default or claim:**
     - the recap multiplier is ×1.1–1.7, not ×1.4–3.4;
     - multistage tree reduction needs Heitsch–Römisch's 2009 method, not their 2003 one;
     - Schwenk is overstated;
     - the 2020 line draws had Fed support, which weakens the 80% credit;
     - Jeanne–Rancière's benchmark is 9.1%.
   - **Attribution slips.** The brief misattributes two items: the 55.8% scaffolding share comes from a system-generated manuscript (paper App. C.2), and the logs-and-code finding is Luo et al. (2026).
   - **Staleness.** Main v1.1 predates groups v1.1. It still shows coverage of 2.10× (now 1.91×), θ\* 0.76 (pooled 0.79), the M6 "floor" and "already over-committed".
5. **Preprints.**
   - The inspiration paper is itself an arXiv preprint.
   - Its isolation is "a cooperative research-code contract, not an adversarial sandbox" (l.7489–7490).
   - The agentic and IC literature is mostly 2025–26 work read at abstract level, so it transfers mechanisms, not effect sizes.
6. **Model class M6** binds, yet it is the least settled.
   - The T4′ calibration and the $13.9bn need come from M6's P99.6. The mixture gives G\* = $4.1bn; the worst of M1–M5 gives $2.6bn.
   - Mix B's M6 rate is 6.46% or 0.09%, depending on the engine.
   - Leverage lowers M6's E[R], and its weight is undecided.
   - Conclusions that rest on M6 must say so: the T6 bands, recovery mode, and the need for the band.
7. **Rare events cannot be validated on outcomes.** A 0.01 Brier gain needs ≈6,300 forecasts per arm (main §6.6 [C]).

**Work in flight at 18:30.** Re-read this review when these land: they could close gaps 1, 5, 13 and 14.
- Real Assets research: two calculation scripts so far.
- Citation fixes: no fix log yet.
- Barrier re-run: results JSON only.
- `BUILD_SPEC.md`: not yet written.

## 6. Data request list for ADIC (by value)

| # | Data | What it would change | Owner | Qs |
|---|---|---|---|---|
| 1 | **Owner mandate:** written distribution rule; draw history 2015–26; basis, notice and cap; the 2026 rate; written willingness to pre-agree 5% crisis draws; owner-directed investments | Mix A vs Mix B (≈40–50bp a year); the $25–43bn swing in literal T4; payout sustainability | User / CIO with the owner; Corporate Finance | Q04, Q16, Q03 |
| 2 | **Funding:** existing lines, covenants and test history; appetite for a $10–15bn revolver; rating; owner debt limit; CSA terms; sovereign IM status | Replaces the 80% vs ≤50% assumption ($13.9bn vs ≈$22bn) and sets every liquidity price | Corporate Finance | Q06, Q08, Q14, Q16 |
| 3 | **Hedge-fund terms τ per lot:** notice, gates, revocability, consents; ADIC's share of each fund; redemptions in 2008, 2020 and 2022 | "The decisive data item" (main §1). Sets the stage metrics; a fully gated book doubles literal T4 | Public Markets | Q16, Q08 |
| 4 | **PE commitments by vintage since 2010:** unfunded; over-commitment limit; pacing corridor; fund cash flows, including 2008–09 calls | Over-commitment, the drought sign, T4′ and every envelope | PE | Q07, Q14, Q16 |
| 5 | **The real allocation by group,** including Real Assets: size, unfunded, energy exposure, asset-debt tapes, open-end terms | Replaces allocations v1 and v2; brings in oil wrong-way exposure | All groups; Real Assets | Q05–Q08, Q14 |
| 6 | **Point-in-time forecast archive by group:** memos, declined deals, gross/net basis, forecasts per person | The only route to group bias and credibility. Reaching n_eff ≥ 20 takes years | Each group | Q09, Q14, Q15 |
| 7 | **Overlay:** blotter in CRIF; daily VM and IM history; every opportunistic variant ever tested; dealer overlap; permissions | Real Greeks and margin; the deflated Sharpe ratio behind the bridge's +0.37pp | Overlay group; Corporate Finance | Q10, Q05 |
| 8 | **Private Credit:** SMA sale and run-off rights; loan tapes with sponsor IDs | The cheapest recovery levers; the PD/LGD split | Private Credit | Q07, Q08 |
| 9 | **Market evidence:** secondary bids by fund age; ADIC's sale-failure rate; LPA consents; co-investment offer logs | SELL pricing, the market anchor, co-investment flow | Secondaries; Co-investment | Q08, Q09 |
| 10 | **Performance and look-through:** net PME and fees by sleeve; company and sponsor IDs | Replaces the α\* priors; feeds the concentration gate V24 | PE; Co-investment; Capital Solutions | Q05, Q15 |
| 11 | **IC records:** votes, dissents, overrides; the memo corpus; permitted model families | Golden sets and admission tests for the lab and the shadow IC | User / IC secretariat | Q11, Q12 |
