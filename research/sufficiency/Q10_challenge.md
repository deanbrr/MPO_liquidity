# Q10 challenge: the OTC overlay (R10)

*Adversarial review of `Q10_audit.md`, 2026-10-18. Read-only on the corpus.*

**Revised verdict: partial (the audit said mostly sufficient). Audit not upheld; its four readiness flags survive.**
- Design-ready: yes.
- Build-ready: no.
- IC answer: no (direction only).
- Needs ADIC data: yes.

> **SYNTHETIC – NOT ADIC DATA.** [I-calc] figures come from synthetic positions, SYN-ADIC-177 or stylised engines. Public-data figures are labelled as such.

## 1. Number checks

All ten numbers checked are present, with the stated meaning.

| Value | Found | Location and note |
|---|---|---|
| IM $609.7m → $418.9m; 1.77; +$389m / −$690m | Yes | gap_03 §7.4; `simm_offset_example_results.json` (31.3%) [I-calc], SYNTHETIC positions |
| ≈$1.1–1.4m per vol point | Yes | gap_03 §8; synthesis §4.6. Re-derived as 0.25 × $4.24–5.64m [I-calc, challenger] |
| 0.64 / 0.42 / 0.26 | Yes | gap_03 §1; greek-layer JSON spike slopes 0.638 / 0.424 / 0.265 [I-calc, public data] |
| Sharpe 1.43–1.97; −0.57 (17%); −1.43 | Yes | gap_03 §4; JSON (73.2 of 440 blocks). −0.57 and −1.43 condition on the future (gap_03's caveat), which the audit drops |
| 3.74%; $7.1bn; $1.18bn; $23.6bn | Yes | groups gap_03 §1, §5; JSON `B_sizing` [I-calc], SYNTHETIC |
| −$4.00bn vs −$6.03bn | Yes | groups gap_03 §5 [I-calc], SYNTHETIC. The opportunistic term (−$0.294bn) is the OV2 cap itself, not a modelled loss |
| ≈7.5% of NAV; corners at 0.28–0.94 | Yes | C3 §5.7 [I-calc]. VIX calls are interior at σ = 5–10 (1.1–9.1% of NAV) |
| 0.65 vs 0.11; 11 of 16 | Yes | groups gap_03 §4; JSON `F_replay` [I-calc], public SPX, model premiums |
| $1.5–1.8bn vs $1.77bn; $1.1–2.0bn vs $1.2–2.1bn | Yes | groups gap_04 §4.3 [I-calc], SYNTHETIC |
| 42 claims: 38 / 3 / 0 | Yes, incomplete | 09 verify §1 also lists 1 unverifiable and 4 C* |

## 2. Where the audit overstates

1. **Half of R10 is barely modelled.** The audit judges the opportunistic book only through its offsets against the tail. The book's own economics are a prior.
   - The bridge credits it +0.37pp a year in every model, as much as all eight sleeves' α* combined (synthesis §4.12) [I-calc], SYNTHETIC.
   - gap_05 §1 item 7 says this holds only if the deflated-Sharpe (DSR) gate passes. C3 §5.3(f)'s own example fails that gate: a backtest Sharpe of 1.0 gives DSR 0.86 [S-c].
   - At the floor, OV1 and OV2 cap the book's short VIX vega at ≈$1.0m per point and its named-stress loss at $0.29bn, ≈0.17% of NAV (groups gap_03 §1 item 8) [I-calc], SYNTHETIC. Its volatility budget is 1.0–1.5% of NAV.
   - No file tests whether a compliant book can earn the +0.37pp. Literature cuts the prior: dealer strategies lose a median 73% of their Sharpe ratio live (lit §4.13) [S].
2. **The joint engine does not implement gap_03.** In `g04_engine.py`, lines 1278–1293:
   - Carry, relative-value and short-vol P&L are fixed steps at crisis onset. Only trend uses simulated returns.
   - The "L1 vega floor" is a constant 0.15 multiplier on short vol whenever the Overlay player is on.
   - So the Overlay's Shapley CE gain of +$1.7–6.7bn (groups gap_04 §6) [I-calc], SYNTHETIC, partly prices a baseline that runs short vol uncapped. The audit's "every line of evidence agrees" ignores this result.
3. **OV2 is ill-defined as written.** It divides by tail P&L "in every named stress", but C3 §5.3(a)'s list includes the Mar–May 2009 reversal, where the sleeve loses. With a zero or negative denominator the ratio is undefined or passes trivially. Groups gap_03 quietly uses a fixed cap instead: 25% of the S1 payoff.
4. **Contradiction 2 is not like-for-like.**
   - *Replay:* a 3/6/12-month 90/72 ladder; exits at 3× premium or VIX ≥ 35; a linear-skew pricer.
   - *Engine:* 12-month 90/70 tranches at a 0.20% budget; exits when MTM reaches 50% of the maximum payoff (25% from Red); Black–Scholes with a 1.5 skew multiplier.
   - With the designed but uncalibrated SSVI, the corpus carries three pricers and three monetization-rule variants.
5. **The −$96m residual has no band.**
   - Groups gap_03 §4 labels KV "market-kernel value" but uses a P-measure carry convention of 0.55. Under the market SDF, E[mX] − P ≡ 0 (09 verify R10).
   - At KV 0.65 (the replay ratio) the residual is ≈−$69m; at 0.45 it is ≈−$122m [I-calc, challenger], SYNTHETIC.
6. **The runway comparison favours debt.**
   - The facility is credited at 80%, but lit §4.3 allows ≤50% in the joint oil-crisis state. It must also be repaid (L6).
   - At 50% it adds ≈5.6 months, not 9 [I-calc, challenger], SYNTHETIC. The direction survives.

## 3. Gaps the audit missed

| # | Gap | Impact | Close by |
|---|---|---|---|
| 1 | Opportunistic return not reconciled with OV1/OV2 limits, and conditional on an unmet DSR gate | High | build_experiment |
| 2 | Level-1 templates never run on E's factor paths; OV1 hard-coded in the only joint engine; Overlay Shapley value not decomposed | High | build_experiment |
| 3 | Brief §8 (added after the audit): rate and inflation hedges for real-asset debt; the oil hedge must net ADIC's own energy assets | Medium | more_research |
| 4 | OV2 needs a rule for stresses where the tail does not pay | Medium | user_decision |
| 5 | One pricer and one monetization rule across replay, engine and C3 | Medium | build_experiment |
| 6 | Cheaper alternatives (defensive equity, naive futures hedge, LASH) absent from C3 §9's baselines (09 lit §4.6; lit §4.13) | Medium | build_experiment |
| 7 | OV1's β choice (all-days or spike) and its cross-asset aggregation unspecified; HLBA max vs additive (09 R15) unresolved | Low | user_decision |
| 8 | "G10" names both the Overlay dossier and the Real Assets streams | Low | user_decision |

## 4. Revised readiness

- **DESIGN: yes.** The position layer, SIMM engine, VM formula and limits are specified. The defects above can be fixed.
- **BUILD: no.**
  - The equity tail slice is close.
  - Not close: the opportunistic book, monetization (no λ^w estimator), OV2 and calibrated surfaces.
- **IC ANSWER: no, direction only.**
  - Defensible: SIMM netting is not an economic offset, and on measured channels cash and committed lines beat options.
  - Not defensible: any opportunistic-return or floor-residual figure.
- **NEEDS ADIC DATA: yes.** The audit's list, plus Real Assets debt and energy exposures.
