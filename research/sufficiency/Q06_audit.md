# Q06 audit: leverage at portfolio and asset level

**Question (R6, R8).** Is leverage analysed well enough to decide on it: costs, availability in stress, limits, when it helps or hurts?

**Verdict: mostly sufficient.** The research is ready for design and close to ready for build. The IC can get a qualified answer today. Sizing still needs two re-runs and ADIC data.

**Keys.**
- SYN = `research/00_SYNTHESIS.md`
- GS = `research/groups/01_GROUPS_SYNTHESIS.md`
- D06, V06, L06 = the stream-06 dossier, verification log and literature check
- LS = `research/literature/00_LITERATURE_SYNTHESIS.md`
- C2 = `research/clusters/C2_private_liquidity.md`
- V08 = `research/verification/08_action_valuation.verify.md`
- gap_02 = `research/addenda/gap_02.md`, with its engine `gap_02_calcs/t1_engine.py`
- G4 verifier = `research/groups/verification/G4_coinvest.verify.md`
- G6 lit = `research/literature/G6_private_credit.lit.md`

Every [I-calc] figure is **SYNTHETIC** (working book), not ADIC data.

## 1. Answer today

For ADIC, leverage is a tool for liquidity and implementation. It is not a route to the 10% target.

**When it helps or hurts.**
- An 8%-mean, 11%-vol portfolio reaches 10% log growth only at 2.36× with 4.05% funding. Above ≈4.28% funding it cannot reach it at all (SYN §2.3(e) [C]).
- On the working book, the 1.30× cap adds ≈0.8pp of expected return in M1 (8.84% → 9.66%). But it lifts volatility from 14.4% to 18.2% and lowers E[R] in M6 (6.06% → 5.88%). The M1 break-even, 1.42×, is above the cap. Stress financing at 175bp lowers the 1.30× row by ≈0.44pp (SYN §4.12 [I-calc], SYNTHETIC).
- In M6, the large-revolver mixes without the owner band fail the covenant gate, at 1.6–2.4% (gap_02 §2.3 [I-calc], SYNTHETIC).

**Where to lever.**
- Lever the liquid book and the overlay, never PE (SYN §1 finding 8 [C]).
- Asset-level LEVER needs financing at about SOFR+300bp or less, plus high-conviction α\*. At Rede's SOFR+480bp it is never optimal (V08 R4 [C]).
- A NAV loan beats a sale only if it is repaid within ≈2 years; AA term debt only within ≈5.8 years (SYN L6 [C]).
- Single-asset leverage fails along the path (GS §1 finding 8 [C], SYNTHETIC):
  - a 12% holdco PIK lifts co-investment drought wipe-out from 7.0% to 22.8%;
  - single-asset NAV facilities breach a 1.5× trigger on 50–63% of quarterly-tested paths;
  - alternative-lender back-leverage cuts Capital Solutions RoE to 8.9%, against 9.25% unlevered.
- The press-reported $15bn HF-TRS would cost ≈2 survival months (SYN §1 [I-calc]).

**Costs.**
- Committed revolver: SOFR+85bp drawn, 15bp undrawn (SYN §4.5 [I], anchored on BXP 8-K [S]).
- Equity-index futures financing: ≈30bp on average, with a peak above 140bp (D06 §4.2 [S]).
- AA term debt: T+55–99bp in normal markets (partly [U]); T+335bp in 2008 (C2 §4.5 [S]).
- LP-portfolio NAV facility: SOFR+300bp (range 250–400), +140bp in stress (C2 §4.5 [I]).

**Availability and sizing** (SYN §2.3(d) [I-calc; S], SYNTHETIC).
- Literal T4 needs $25–92bn of facilities. That is above the $26.6bn hard debt limit and above PIF's $15bn revolver precedent.
- The calibrated T4′ needs $13.9bn: $6.1bn with the stage pacing cut, and $0 with an owner band.
- Recommendation (GS §1, §2.3 [I-calc], SYNTHETIC):
  - Request indications for $10–15bn of committed unsecured revolver capacity.
  - Drop the NAV facility as a Tier-1 lever. It is pledge-capped at $2.1bn and costs ≈6× the revolver per credited dollar.

**Limits** (SYN §4.5 [I/C]). These are defaults for IC ratification, set deliberately below peers:
- recourse debt ≤10% (target) and ≤15% (hard);
- economic exposure ≤1.30×;
- encumbrance ≤15% (target) and ≤20% (hard) of total assets;
- covenant trigger probability ≤2% within 12 months;
- half-Kelly on discretionary leverage;
- facilities count 0% in 30-day rows.

The peer anchors are now like-for-like. CPP is 9.7% on DBRS's debt-only basis but 36% on its own measure (45% limit). OTPP is 17%, at ≈1.32× gross exposure.

**Doctrine** (SYN §4.5 [I]). Portfolio LEVER goes ahead only if all four tests pass:
1. Tier 1 passes with the debt included.
2. α\* beats the shadow costs.
3. ΔP(10%)/ΔP(breach) beats the IC's exchange rate.
4. Rating proxies hold with ≥95% probability.

## 2. Evidence

**Strongest sources.**
- D06 rates HIGH on facts, arithmetic and citations, and MEDIUM on design (V06 §1). Of 34 claims, 26 were confirmed, 3 corrected and 0 refuted; every example was recomputed.
- L06 §1 found 25 of 26 references, with none mismatched or hallucinated.
- LS §4.12 rates the leverage module "supported, refined".
- V06's fixes R1–R6 carry through to C2 §1 (V16, V18–V22) and SYN §4.5: peer comparability, the "cannot reach 10%" overclaim, SELL-vs-LEVER normalization, a drawdown barrier that forced a net-short overlay, Basel-consistent LCR/NSFR, and double counting.
- Facility sizing comes from a tested engine (gap_02, `t1_engine.py`).

**Weakest source.** Stream 06's balance-sheet Monte Carlo cannot be reproduced (V06 §3).

**Contradictions between files.**
1. **Revolver availability in stress (material).**
   - SYN §2.3(d) and gap_02 credit the revolver at 80%, and the Monte Carlo engine credits it at 80–90% in crisis (`t1_engine.py` l.594).
   - LS §4.3 and the design brief (§7 item 2) require ≤50% in the joint oil–crisis state, zero for new facilities, and a ≈1.1pp tightening premium. The C1 and GC2 clusters used 50%.
   - Nothing was re-run at 50%. The need equals G\*/credit (11.1/0.8 = 13.9). At 50%, T4′ therefore needs ≈$22.2bn, which is above the $15bn precedent. With the pacing cut it needs ≈$9.8bn, still within the $10–15bn request [auditor arithmetic, SYNTHETIC].
   - The Mix A and Mix B certifications are unverified at 50%.
2. **30-day coverage.** SYN §4.5 shows ADIC-LCR(30d) at 2.10×. GS C12 corrects this to 1.91× (Amber) on HQLA that Corporate Finance controls. The correction has not reached SYN.
3. **Bridge leverage.** SYN §4.12 credits +0.18pp from central leverage of 1.05×. GS §2.2 puts economic exposure at t0 at ≈0.97×, on a book that is already in recovery.
4. **Labels and hurdles.**
   - The holdco PIK quoted as LEVER evidence is a cash-out, which is REFINANCE under the user's definitions (G4 verifier R9).
   - The private-credit LEVER hurdle is ≈4.0% in SYN §4.4, but ≈2.9% once the tightening premium is included (G6 lit §4.4).

**Citation-audit errors that touch Q06.**
- **LS §2.4 #1.** The Broadie–Glasserman–Kou barrier shift in the co-investment work has the wrong sign, and the script applied none. The wipe-out and LTV-breach rates are therefore understated and provisional (brief §7 item 15). Correcting them strengthens the "do not lever single assets" conclusion.
- **LS §2.4 #14.** Credit lines met the 2020 draws with Fed support, which an oil–fiscal stress may lack. This makes 80% credit optimistic.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | Variables, dynamics, regime cost curves, metric variants, limits, the four-test doctrine and a group instrument library with regime availability are all specified (SYN §4.4–4.5; D06 §6; C2 §4.5) |
| BUILD | No (close) | Stress availability is unresolved; the cost-curve convexity η_k(z) and the rollover model have no parameters; commitment-adjusted leverage is missing; leverage has never run through the T4′/T6 engine |
| IC ANSWER | Yes, qualified | The doctrine, the no-route-to-10% result, the asset-level verdicts and the limits are defensible on synthetic data. Facility sizing must carry a 50%-availability sensitivity |
| NEEDS ADIC DATA | Yes | Issuer, rating and legal capacity; owner debt limit; facility and ISDA/CSA terms; quotes; look-through leverage; commitments by vintage; HF-TRS terms |

## 4. Gaps

| # | Gap | Impact | Close by |
|---|---|---|---|
| 1 | Facility need, Mix A/B and covenant risk not re-run at ≤50% revolver credit, zero new facilities and the tightening premium | High | build_experiment; user_decision |
| 2 | Economic leverage of 1.05–1.30× (with any HF-TRS) never tested against T4′/T6 with VM, so doctrine test 1 has not been run | High | build_experiment |
| 3 | Borrowing capacity, issuer, rating, owner debt limit, existing facilities, real quotes | High | adic_data |
| 4 | Cyclical vs structural DPI split, which decides whether bridging with debt is rational | Medium | adic_data |
| 5 | Commitment-adjusted and look-through leverage missing from the metrics (L06 §4.1; LS §4.5) | Medium | adic_data; build_experiment |
| 6 | Cost-curve convexity η_k(z), endogenous rollover and segment-specific haircuts unparameterized | Medium | build_experiment; adic_data |
| 7 | Limits ratified; ΔP(10%)/ΔP(breach) exchange rate elicited | Medium | user_decision |
| 8 | The reserve-versus-invested-debt trade-off rests on the non-reproducible Monte Carlo | Medium | build_experiment |
| 9 | Co-investment barrier corrections; private-credit and Capital Solutions hurdles with the tightening premium | Low | build_experiment |
| 10 | Contested BAB evidence; each levered sleeve needs a backtest that includes frictions | Low | build_experiment |
