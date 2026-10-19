# Q07 challenge: the private book with declining PE DPI

*Adversarial review of Q07_audit.md, 2026-10-18. ADIC figures are SYNTHETIC unless tagged [S]. **Revised verdict: partial** (the audit said mostly_sufficient). The readiness flags survive; the audit's robustness claims do not.*

## 1. Number checks

All ten load-bearing values sit where the audit cites them. Two carry the wrong meaning.

| Value | Found | Note |
|---|---|---|
| MSCI distributions 9% / 9–11% / 17–24%; calls 27–31% [S] | Yes | main §7.1; C2 §6 |
| m^D and κ by exit window [I] | Yes | main §4.2; C2 §4.1 |
| D 0.87; $11.8bn vs $20.7bn [I-calc] | Yes, mislabelled | gap_04 §6.2 calls it "E[PE distributions]" but applies PE rates to all $106bn. That is the single-rate method main §4.2 rejects |
| +$2.2bn / +$3.7bn; +$2.6–5.3bn "V6-compliant" [I-calc] | Yes, wrong meaning | §2.1 |
| −$16.4bn (70% PE); −$28.7bn (T4′, census v1.0) | Yes | groups §2.2 |
| 0.81 → 0.97; 0.75; U/NAV 0.53 / 0.32 | Yes | main §2.3(c) and finding 4; groups gap_02 §0, §1.2 |
| Pause $0.67 / $3.51 / −$4.38bn; 66% vs ≈40% | Yes | groups §3.1, §8 |
| 8.6¢ (5.6–12.3¢) | Yes | groups §3.1 |
| $13.9bn → $6.1bn; 8.2% → 2.4% (M1) | Yes | main §2.3(d), §2.4 |
| $0.8–0.9bn SMA run-off; half-life 2.1–2.5 years | Yes | main §4.2; G6 verify R1; C2 §5.2 |

## 2. Claims that do not survive

**2.1 "Positive for every V6-compliant history."**
- groups gap_02 §1.2 Table 1, and the V6 row in groups §2.2, mark the Mature and 10%-then-flat histories "pass / fail". That is the same status as the v1.0 reproduction, which the research rejects for failing the contribution half.
- Only the sealed v1.1 history passes both halves. The +$2.6–5.3bn range therefore spans two histories that fail the gate.
- Two-spike and V-shaped histories with ≥ $27.4bn of unfunded pass V6, or its averaged band (gap_02 §1.2). Their drought net cash is never reported.
- The sign therefore rests on a plausibility prior (the "plan-consistent" family), not on V6.

**2.2 On the working census, the sign depends on which engine you use.**
- **Two sets of drought rates.** The cash map puts Secondaries at 18% and Co-investment at 12.4% (groups §2.2; `gs_group_cashmap.py`). `t1_engine.py` uses 12.5% and 9%, the same 0.5× cut as PE (`DROUGHT_DIST`, line 766; Monte Carlo lines 408–415).
- **Mismatched conditioning.** The 12.4% is G4's mean from a drought *start*, so it includes paths that leave the drought (G4 dossier; G7's own default was 9%). PE, by contrast, is held in a persistent drought.
- **Effect.** t1's rates remove ≈$1.4bn. Main §2.3(b) itself shows that MSCI's 9% PE rate cuts the book to +$1.1bn. Together they put census v1.0 at ≈ −$0.3bn [skeptic's arithmetic, SYNTHETIC]. Census v1.1 stays positive at ≈ +$2.3bn.

**2.3 "Robust across models."**
- M1–M6 are CMA-provider structures, and all six share one factor architecture (main §4.1; §9.2 item 3).
- `g04` reproduces `t1` path for path (groups §0).
- No challenger to the private engine exists, so its structural uncertainty is unmeasured.

**2.4 Pacing relief is overstated.**
- The ladder cuts commitments from month 2, and calls new commitments at the seasoned stressed rate, 28% × 1.38 (`t1_engine.py` lines 858–875). This is the rate-based logic that main §2.3(c) says cannot see vintage.
- Literature §4.5's rule of no liquidity credit for two quarters, on its own, lifts the facility need with the cut from $6.1bn to ≈$8bn.
- Adding Ljungqvist–Richardson's 20% first-year call rate (C2 §4.1) gives ≈$9bn [skeptic's first-order recomputation, SYNTHETIC, not an engine run].
- The 8.2% → 2.4% red-event result uses the same logic.

**2.5 Part of the "direction" is census-specific.** PE's 70–82% share of the stressed drain holds on census v1.0. On v1.1 it is ≈64% (S1 −3.89/−6.07; literal T4 −7.72/−12.15; groups §2.2).

**2.6 The pacing cost is mostly judgment.** κ^GP at its upper bound supplies 5.12¢ of the 8.6¢; its central value is 2.3¢ (groups §3.1). No paper measures the access an LP loses after skipping a re-up (G1 literature review; literature §4.17).

## 3. BUILD is not "nearly" ready

- **Exit window vs macro regime.** C2 §4.1 writes P(e | e, d, z), and main §4.1 calls the chains coupled. Only the shock-type coupling has parameters. `t1` hard-codes "crisis → F with probability 0.8" (line 375). The joint tail that T4′ and T6 measure depends on this coupling.
- **The drought enters twice.** C2 E6′ says regime effects enter "only through" m^D, yet the κ clock also lowers δ̄(a^e), and gap_02 applies both. The census fit absorbs any resulting bias, so census v1.1 depends on the engine:
  - the distribution curve is flagged for refit (C2 §4.1);
  - the engine runs 4–5pp high in 2019–20 (gap_02 §1.3);
  - Mature and 10%-flat miss the contribution band by only 0.3–0.7pp.
- **Five prototypes, five conventions.** G7/GS (cash map), the `t1` ladder (T4′), the `t1` Monte Carlo (T6), `rfta_v2_book` (v1.1) and G4 (co-investment).
- **Still unspecified.** X_t dynamics and loadings, the lumpiness term ζ, the quality-drift rate χ, the random-effect variances, the semi-Markov durations and the pacing MPC.

## 4. Gaps the audit missed

- **Liquidity order.** Literature §4.4 contradicts the fixed waterfall. The T4′ ladder admits no private sales in stress, and the state-dependent orders with planned early tail-end and LP-interest sales are never run.
- **Private Credit drought cash.** The cash map applies 16% in drought to the whole $14bn, although 55% sits in CEF, evergreen or BDC wrappers (groups §3.6); the canonical T4′ convention uses 10%. The mild non-PE multipliers (0.64–0.94) contradict main §2.3(b), which says this cash "moves *with* PE distributions".
- **No literature sweep.** The groups addenda ran without a Consensus sweep (groups §0), and they include the census and the PACE cost.
- **Missing data items.** ADIC's own over-commitment limit and pacing corridor (groups §9 Q4) are not in the audit's data list.

## 5. Revised readiness

| Level | Verdict |
|---|---|
| DESIGN | Yes |
| BUILD | No: integration, coupling and the stochastic layer are still open |
| IC ANSWER | Yes, but directional only. **Defensible:** distributions halve while calls hold [S]; the liquid book funds the payout on both censuses; no private group hedges the drought; pacing is slow. **Not defensible today:** the drought sign on v1.0, PE's share of the drain, the over-commitment breach, facility levels, and pacing's rank and cost |
| NEEDS ADIC DATA | Yes |
