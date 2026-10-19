# Q08 challenge: the SELL / HOLD / REFINANCE / LEVER lens (R8)

Skeptic review of `Q08_audit.md`, 2026-10-18. Every ADIC figure is **SYNTHETIC** (proxy models on the working book). Tags: [S] sourced, [C] checked, [I] inference, [I-calc] synthetic arithmetic. "Challenger I-calc" marks my own arithmetic.

**Verdict: partial (audit: mostly sufficient). Not upheld.** The design survives for seven of eight groups. The build and IC-answer claims do not.

## 1. Number checks

All ten numbers checked are on disk with the stated meaning.

| Value | Location |
|---|---|
| 0.9% → 76.8%; dual 0.237 | gap_02 §4 table; main §1 f7, L15, §4.4, §4.8 |
| μ 0.243 / 0.0113 | groups §4.8 t0 table; groups gap_01 §3 |
| 70.6% → 90.7%; 75.2% → 90.9% | groups §4.8 |
| 1.1 / 4.8 / 5.4 / 7.0 / 21.9%; $2.1bn | groups §2.3 [I] |
| ≈2.0 / 5.8 years | main L6, §4.4; C2 §4.4 |
| SOFR+300 / +480 | 08 log R4 (one worked example) |
| $3.3m; 87.3% | 08 log R1; main §4.4 |
| $11.3bn | groups §4.3, §4.8 |
| 36 of 40; $24.7m | main §4.4 (tagged [S]); 08 log §5 |
| 80% vs ≤ 50% | main §2.3(d); lit §4.3; brief §7.2 |

Two small corrections: the 18/18 pass count sits in groups §0 and §4.3, not §4.8, and stream 08's citations are 35 checked, 0 not found and 1 mismatched (lit §2.1), not "34 of 35 found".

## 2. Where the audit overstates

1. **"Every group."** Context §1A lists eight groups. Real Assets ($18bn, ≈$4bn unfunded, oil wrong-way risk) was added after the seven-group research. Brief §8.3 gives only an interim action list, and streams G10–G15 are not on disk. Nothing in the corpus prices cash-out refinancing, sale-leasebacks, JV sell-downs, open-end queues or development debt, or gives their lags.
2. **Superseded inputs.** Context §1A says allocation v2 (PE $34bn) "supersedes" v1, and the user chose census v1.1 ($16.4bn). Yet T4′ has not been computed on v1.1 (groups C21; it runs on gap_02's unfunded split, groups §2.2), and the t0 cards use census v1.0's U/NAV of 0.53 (groups §4.8), which groups C6 keeps "as a reproduction check only". The audit's "census is unconfirmed" is out of date, and closing it needs a re-run, not ADIC data.
3. **The flagship card contradicts itself.** With the revolver signed under T4′, main §4.4 and gap_02 §4 price the 2018 buyout fund at 87.7%: a marginal SELL at an 88% bid (y_IG 0.072). Groups §4.8 prices the same card at 90.7%: a HOLD (y_IG 0.033) [both I-calc]. No file reconciles the two IG duals, and the audit quotes both without noting the conflict.
4. **The cards are not kernel valuations.** Every Phase-I/II card fixes the hold value at 0.95 × NAV (groups §4.8; gap_02 §4). The production kernel (m, ℓ from H, FBE beliefs) has never produced a card. C2 §3.4's tests T1–T5 have not run. The LEVER ≡ ADD + REFI identity has so far held only by construction (08 log R4c). Consistency is a property of the design, not something the outputs show.
5. **The ≈2-year rule rests on a rejected input.** Dossier 06 §6.8(c) assumes c − r_f ≈ 5.5% (a GP-level margin), which main §4.4 rejects for LP borrowing. On main's LP default (SOFR+300, 1–2% OID), C2's own formula gives ≈3.2 years (2.2–4.0), or ≈2.2 years at the +140bp stress [challenger I-calc, before encumbrance cost].
6. **The LEVER threshold comes from one example.** It is 08's Example 2, one asset at a flat ℓ. Even at SOFR+300, LEVER wins only for ℓ between 3.5% and 4.25% (08 log R4).
7. **R1 sits on a knife edge.** At the pooled θ\* of 0.79, T4′ needs $14.6bn of revolver (groups gap_01 §0; groups C4), $0.4bn below the $15bn cap where μ jumps four- to five-fold (groups §4.8). The open overlay correction (C18) adds ≈$0.9bn of 12-month use [I], or ≈$1.1bn of facility at 80% credit [challenger I-calc]. The audit rates this Low. At ≤ 50% credit (brief §7.2), the $11.1bn credited need would take ≈$22bn of facility, above the cap. Nothing is signed at t0, and new facilities count at zero.
8. **No price under the recommended policy.** Under Mix A or Mix B, T4′ goes slack and the binding price becomes T6's, still an open item (groups §4.4). The audit rates this Medium; it should be High.

## 3. Gaps the audit missed

- **Pacing refinements.** Brief §7.14 says a pacing cut gets no liquidity credit for two quarters, values the corridor as an option and counts unfunded commitments in leverage. Brief §7.8 adds a fund-size penalty on up-sizes. Neither is applied to the PE PACE and LEVER rows (groups §3.1; main §4.4).
- **Band default.** Brief §7.3 makes Mix A the default unless there is a written agreement. The gap_04 §5 envelopes and FTP that the audit cites as support assume Mix B, and Mix A is infeasible at appetite.
- **Regime availability.** Only PE sales, PE · REFI and the hedge-fund state machine have numbers, and C2 §4.3(d) contradicts the PE · REFI figure. Other rows are either on/off ("benign/normal only") or say just "thin" or "queues" in a crisis. Building the lens needs an instrument × regime × shock-type matrix.
- **Per asset.** Enumerating every asset's actions is a Phase-3 deliverable (main §10). The MVP covers only the top-20 cards.
- **PE REFINANCE pricing.** SOFR+300 is an analogue taken from secondaries-fund facilities at 25–75% LTV (C2 §4.3(d)). Lit §4.17 finds no literature on NAV loans, preferred equity or PIK.

## 4. Revised readiness

| Level | Audit | Revised |
|---|---|---|
| DESIGN | Yes | **Yes** for seven groups; Real Assets undesigned |
| BUILD | Nearly | **No.** H is not built, and the kernel, duals and FBE are not joined. T1–T5 have not run. Still missing: the availability matrix, Real Assets, the v2/v1.1 re-runs, and decision records on revolver credit, the recourse waterfall and the band |
| IC ANSWER | Yes, qualified | **No**, beyond a briefing on method. The card verdicts conflict across files, run on superseded inputs and turn on an undecided convention. Main §9.2 item 10 bars unreplicated [I] toy results from IC use |
| NEEDS ADIC DATA | Yes | **Yes**, plus Real Assets debt tapes, leases and open-end fund terms |
