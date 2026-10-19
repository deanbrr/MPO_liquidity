# Q03 challenge: probabilities of outcomes (R3)

**Skeptic's verdict: partial** (auditor: mostly_sufficient). Readiness flags unchanged: DESIGN yes, BUILD yes (narrower), IC ANSWER no, ADIC DATA needed. The machinery can be designed and built, but today's probabilities cannot yet be stated, for more reasons than the audit gives.

All P(red), P(10%), liquidity and drawdown figures are SYNTHETIC [I-calc] unless tagged otherwise.

## 1. Number checks

| # | Figure | Found | Location |
|---|---|---|---|
| 1 | P(10y ≥ 10%) 40.0 / 54.1 / 24.4 / 38.0 / 41.5 / 19.6%, mean 36% | Yes | gap_05 §6 l.125; bridge_results.json, mixture mean 0.3627 |
| 2 | P(μ ≥ 10%) at 1.05×: M1 1–16%, M2 66–83%, M3 and M6 0% | Yes | gap_05 §6 l.126 |
| 3 | Do-nothing P(red) 7.8 / 6.1 / 10.1 / 20.8 / 18.6 / 37.2% | Yes (50k paths) | gap_02 §2.1; gap02_results.json, calibration.mc |
| 4 | Mix A CP 0.98%, Mix B CP 0.79%; M6 5.8 / 6.5%; M6 floor 2.4% (CP 2.5%) | Yes | gap_02 §2.3; certified_50k; gap02_certify_extra.json |
| 5 | Group engine: do nothing 1.6 / 6.3 / 14.5%; Mix B 0.00 / 0.00 / 0.09% | Yes (10k paths, uncertified) | groups gap_04 §2, steps S6–S7; g04_bridge_results.json |
| 6 | Model dispersion 3–4pp against MC error ≈0.2pp [C] | Yes | C1 §1 item 6; §2 row 10-1 |
| 7 | KL worst case: nominal 1% → 2.70%; a 2.5% cap needs nominal ≤ 0.88% [I-new] | Yes | C1 §5.11 |
| 8 | Survival 17 months; ADIC-LCR(30d) 1.91× (2.10× in total) | Yes | gap_02 §1.3; groups synthesis §2.4. Main synthesis l.1737 still shows 2.10× |
| 9 | Owner-band activation 12–22% | Yes, but rounded up | gap_02 §2.3. The JSON maximum is 21.48% (gap02_certify_extra.json, p_band12) |
| 10 | i.i.d. P(10y max drawdown > 40%) 0.5 / 3.5 / 7.6% [I-new, stylised] | Yes | C1 §13, labelled as lower bounds |

## 2. Where the audit overstates

**1. "A certified 1% mix exists in M1–M5" holds only under engine assumptions the literature rejects.**
- The audit omits three literature verdicts that design brief §7 items 1–3 mandate: the owner band is Contested (§4.2); the revolver counts at ≤ 50% in the joint oil–crisis state (§4.3); the fixed waterfall is Contradicted (§4.4).
- The engine credits the revolver at 80–90% in crisis (`t1_engine.py` l.594), assumes the owner always grants the band, and keeps the fixed waterfall (C1 §5.7).
- Mix A passes by 2bp: its M5 bound is 0.979% (gap02_results.json). At 10k paths it fails, with CP 1.14% in M4 and 1.16% in M5 (g04_bridge_results.json, step S0).
- It also fails the optional KL cap, which needs nominal ≤ 0.88% at η = 0.01 (C1 §5.11). Mix A's 0.906% in M5 gives a worst case of 2.54% [I-calc, this review].
- Halving revolver credit would likely break certification.

**2. The recommended Mix B breaches gap_02's own M6 band.**
- Mix B's M6 rate is 6.46% (CP 6.64%), above the 5% M6-class capacity, so recovery mode is triggered (gap_02 §2.3, §3). Only the 64bp "M6 floor" mix reaches tolerance (2.37%, CP 2.48%).
- "Without the band, M6 breaches capacity" (gap_02 §3; groups synthesis l.373) implies the band fixes M6. For Mix B it does not.

**3. The "≈70× between engines" comes mostly from crediting management actions, not from the engine.**
- Engine changes (S0–S4) move Mix B's M6 rate only from 6.4% to 4.8%; slippage-free playbooks (S5) take it to 0.12% (groups gap_04 §2).
- Red events exclude crisis-priced Private Credit and Capital Solutions sales (`t1_engine.py` l.241, l.610–621), which the playbooks rely on (PC SMA loans at 0.85). Part of the drop moves fire sales outside the definition.
- The "0.00%" cells are 0 of 10,000 paths (CP 0.03%), below the research's own 50k standard.

**4. "Today" is not defined consistently, and the book has since changed.**
- The two engines start from different states. Groups gap_04's October-2026 state alone lowers do-nothing P(red) by 2–6pp against gap_02's "today", to 6.1 / 16.2 / 31.7% (step S1).
- Design brief §8 (edited 18:12, after this audit at 17:31) records that the user chose census v1.1. It also adds Real Assets as an eighth group: $18bn carved out of PE, with oil wrong-way risk against the owner's draw.
- Every P(red), survival figure and θ\* is still on census v1.0, and P(10%) uses the seven-group weights. Audit gap 2 is now a re-run, not a user decision.

**5. P(μ ≥ 10%) understates uncertainty.**
- τ covers lever priors only (gap_05 §2), so the "0%" in M3 and M6 treats each provider's beta as exact, although AQR quotes ±3% error at 50% (C1 §7 [S]).
- The priors are judgment syntheses (gap_05 §10), yet the synthesis's own anchor finds 80% intervals contain 36% of outcomes (synthesis §7 [S]).

**6. F_t is weak evidence for R3, not "strong".**
- Brier skill is 8.1% (AUC 0.70); a 0.17 forecast verified at 0.24; DD3 hit 48.9% of amber months but 36.1% of red (gap_04 §4.1–4.2 [I-calc, public data]).
- It scores a US-equity drawdown, not an ADIC outcome.
- The 35% end of P(stress within 12 months) comes from K4, which failed the harness, yet E keeps a 4-state chain for generation (gap_04 §4.3).

**7. Smaller points.**
- The equal-weight 36% gives JPM three of six seats: M1, M4 and M5 share its means (gap_05 §3).
- At the 1.30× cap, volatility is 18.2% (gap_05 §7), above the 17.7% row whose i.i.d. *lower* bound on P(10y max DD > 40%) is already 7.6%, against 10% capacity (C1 §13, D8).

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | |
| BUILD | Yes, for the harness only | CP, IS, KL/W∞, reporting and the claim validator are code-ready (C1 §5.7, §5.11; synthesis l.1553). E is structure only: K ∈ {3, 4, 5} open, liquidity drivers with "no defaults asserted", owner demand a "hypothesis" (C1 §5.10). Waterfall, facility credit and band need re-specifying (brief §7) |
| IC ANSWER | No | More firmly than the audit says: the numbers predate the user's decisions and the literature corrections |
| ADIC DATA | Yes | Add the owner's written band terms and the revolver term sheets |

## 4. Missed gaps

- **High:** re-certify with brief §7 items 1–3; get an IC decision on Mix B's M6 breach; re-run on census v1.1, the v2 allocation and Real Assets.
- **Medium:** report P(amber sale) next to P(red); use one hashed initial state; add CMA beta error to τ; revalidate F_t and the generator's regime chain.
- **Low:** decide whether the KL cap binds; balance mixture weights by provider.
