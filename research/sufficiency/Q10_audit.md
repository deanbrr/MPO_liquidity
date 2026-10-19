# Q10 audit: is the OTC overlay modelled well enough?

**Question (R10).** The OTC overlay has two books: a tail hedge and an opportunistic book. Is it modelled well enough on six counts: the position/Greek layer, pricing, collateral VM/IM, monetization, net-vega limits, and value against a cash buffer?

**Verdict: mostly sufficient.**
- The overlay is ready to design.
- The equity slice is nearly ready to build.
- Value against cash is answered in direction only.

Every number comes from public market data or the SYNTHETIC ADIC-like book; none is ADIC data.

## 1. Answer today

**What the research specifies.**
- **One position layer** with two representations:
  - Level 1: factor exposures for each strategy family, used until ADIC's blotter arrives;
  - Level 2: about 15 trade templates, once it does.
- **One set of SIMM-defined sensitivities feeds five consumers** (gap_03 §2; synthesis §4.6):
  - P&L, from a Taylor expansion that a P&L-explain test gates;
  - VM by CSA (threshold, MTA, T+1 settlement), with recognition φ = 1 / 0.7 / 0;
  - SIMM-like initial margin (IM);
  - economic net-vega limits OV1–OV3;
  - the λ liquidity ledger.
- **Pricing.** Equity options use an SSVI surface anchored to the VIX term structure. Rates, FX, Brent, CDX and hybrids each have a named model, none calibrated.

**On value, every line of evidence agrees.**
- As liquidity insurance, cash and committed lines beat options.
- Convexity is kept only at an IC-owned budget floor. It is held for enabling value, gap and decision-latency protection, and protection against model misspecification. None of these has been measured.

| Number | Meaning | Source; tag |
|---|---|---|
| IM $609.7m → $418.9m (−31%); offset ratio 1.77 | SIMM treats a short 1-month straddle book (vega −$10m) as exactly offsetting long 6-month puts (+$10m). In a vega-only 2020 replay, the short book loses $690m while the puts gain $389m | gap_03 §7.4; [I-calc]; SYNTHETIC positions on public moves |
| ≈$1.1–1.4m per vol point | OV1 requires overlay VIX-equivalent vega ≥ 0.75× the tail sleeve's. It caps that short book at this size. OV2 caps the offset ratio at 25%. Both thresholds are judgment | gap_03 §8; [I] |
| 0.64 / 0.42 / 0.26 | Move in 3-, 6- and 12-month implied vol per VIX point on spike days, which SIMM's expiry netting ignores | gap_03 §1; [I-calc]; public data |
| Sharpe 1.4–2.0 at entry; −0.57 in transitions | Short-vol Sharpe is positive on entry into every VIX state. Its losses sit in regime transitions (17% of blocks), so templates keyed to the VIX level are rejected | gap_03 §4; [I-calc]; public data |
| 3.74% a year; $7.1bn; $1.18bn | Cost of the 90/72 put-spread ladder per $ of notional; the notional the 0.15% floor ($0.27bn a year) buys; its payoff in stress S1. Priced with a simplified pricer (linear skew, c_ATM = 0.90 [I]) | groups gap_03 §1, §5; [I-calc]; SYNTHETIC |
| −$4.0bn vs −$6.0bn | Overlay cash use over the first 12 months of S1: reconciled vs as published | groups gap_03 §5; [I-calc]; SYNTHETIC |
| ≈7.5% of NAV vs corner solutions | Jeanne–Rancière optimum for HQLA at 1.5% carry. Puts and collars costing 0.28–0.94 per $ of crisis payoff hit the "do not insure" corner | C3 §5.7; [I-calc]; one-shot model |
| ≈1–1.4 vs ≈9 months | Runway added by a 0.25%-of-NAV-a-year convex sleeve vs a committed facility of 10% of NAV | C3 §5.7; [I-calc]; SYNTHETIC |
| 0.62–0.64 per $; ≈−$96m a year | Ex-ante credit per $ of premium; IC policy residual at the floor | groups gap_03 §4; [I-calc]; SYNTHETIC |
| 0.65 vs 0.11 | Payoff per $ of premium over a 2010–25 replay. "Monetize" sells at 3× premium or VIX ≥ 35; "hold" keeps to expiry. Annual DVA is negative in 11 of 16 years | groups gap_03 §4; [I-calc]; public SPX, model-priced premiums |
| ≈$300bn | Rise in cleared IM in March 2020, while non-cleared IM "remained relatively stable". SIMM recalibration lags a stress by ≈6–12 months [I] | gap_03 §1; [S] |

## 2. Evidence

**Strongest.**
- **Stream 09 verifier** (09 verify §1, §6):
  - 42 claims checked: 38 confirmed, 3 corrected, 0 refuted.
  - Rating: facts HIGH; design layer MEDIUM until R1–R7 were fixed.
- **Fixes adopted** (C3 §2.2 D14–D24; synthesis §4.6):
  - spot–vol slopes −1.35 / −0.94 [C];
  - an SSVI surface anchored at several tenors;
  - VM signed across books, crediting only incremental usable liquidity ΔL^use;
  - the IM jump treated as a stress quantile;
  - the hindsight cost-per-crisis table rejected.
- **Literature check:** 29 of 29 citations found, none mismatched (09 lit §1).
- **Reproducibility:** the gap_03 and groups gap_03 figures match their results JSON files.

**Weaker.**
- **gap_03, the layer everything rests on, has no adversarial log.**
  - Its SIMM and pricing sources (SIMM v2.8+2512; Hagan et al. 2014; Antonov et al. 2015; Pedersen 2003; Morini–Brigo) were not swept, and Gatheral–Jacquier remains unchecked.
  - Its [S] tags therefore mean "sourced", not "verifier-confirmed" as synthesis §0 defines [S].
  - The groups gap_03 literature sweep did not run (V12).
- **The worked examples are simplified:** one risk factor, first-order vega only.

**Contradictions.**
1. **The engines use three different overlay conventions.**
   - Canonical T4′ uses +$4.05bn of tail monetization and an opportunistic loss of 1.5% of NAV (synthesis §2.3(d); groups synthesis §2.2). That loss breaches OV2 at every budget (groups gap_03 V5, refuted).
   - Synthesis §2.2 and §2.3(b) still quote a −$6bn crash year, $15bn of synthetic beta and ≈$0.7bn of premium.
   - Groups gap_04 uses a 0.20% premium with 12-month equity and Brent tranches.
   - Groups synthesis C18 puts the reconciled T4′ overlay at ≈−$3.9bn, against −$2.94bn canonical. That figure comes from substituting components, not from an engine run, and the item is open.
2. **The value of monetization.**
   - The groups gap_03 replay finds it decisive: 0.65 vs 0.11 per $ of premium.
   - The groups gap_04 engine finds that early monetization "moves cash forward but does not raise it": $1.1–2.0bn, against $1.2–2.1bn held to expiry.
   - My inference: quarterly steps miss vol spikes, which revert within about 35 days.
3. **The trigger for raising the budget above the floor.** Synthesis §4.6 and main gap_04 trigger on a variance risk premium (VRP) at or below its 30th percentile. The literature synthesis (§4.13) and design brief §7.9 say to trigger on the left-tail premium instead.
4. **The cash test.**
   - The literature synthesis (§3.10, §4.13) and design brief §7.9 require the sleeve to beat an equal-cost cash buffer.
   - C3 §9 lists a "cash reserve only" baseline, but synthesis v1.1 never states the test.

**Citation-audit items** (literature synthesis §2.4, item 7), none of which changes the architecture:
- The Jeanne–Rancière benchmark is 9.1% in the 2011 *Economic Journal* version, not 10.1%; C3 §6 still says 10.1%.
- Lo (2002): serial correlation can overstate Sharpe ratios by up to 65%.
- Moreira–Muir is disputed out of sample.
- Kaminski–Lo, behind the drawdown stop, is unchecked.

## 3. Readiness

- **DESIGN: yes.**
  - Every sub-component has a formulation and a list of rejected alternatives.
  - Tests T1–T6 have pass criteria (gap_03 §9; synthesis §8).
- **BUILD: not yet, but close.**
  - The equity slice can be coded and tested now (synthesis §10): Level-1 templates, SSVI with the tenor map β(T), SIMM-like equity IM, OV1–OV3 and the 2020 replay.
  - Still missing:
    - one overlay convention shared by every engine;
    - option-surface data: equity risk reversals and butterflies, FX, CDX, the swaption cube and Brent;
    - an estimator for λ^w, which the LSM monetization rule needs (SDDP is a Phase-2 item);
    - a SIMM licence, needed for test T4;
    - a delta-hedging policy for the sleeve.
- **IC ANSWER: directional only, no numbers yet.**
  - Defensible today: SIMM netting is not an economic offset, so govern on OV1–OV3; cash and committed lines dominate options as liquidity insurance; hold the floor only as an explicit premium against misspecification.
  - Not yet: synthesis §9.2 item 10 requires [I] toy results to be replicated in one engine first; the equal-cost cash run is not done; C18 is open.
- **NEEDS ADIC DATA: yes.**
  - the blotter in CRIF;
  - CSA terms;
  - the IM regime (the US sovereign exclusion covers central governments only [S]);
  - daily VM and IM history;
  - dealer overlap between the books;
  - opportunistic P&L, with every variant ever tested;
  - financing history;
  - permissions: net short volatility, oil options, hybrids.

## 4. Gaps

| Gap | Impact | Close via | Detail |
|---|---|---|---|
| Convex sleeve never tested against an equal-cost cash buffer; enabling value unmeasured | High | build_experiment | Run the C3 §9 baselines on common random numbers. The ≈−$96m residual is exactly this unmeasured value |
| No single overlay convention across the T1 engine, groups gap_04 and synthesis §2.3 | High | build_experiment | Re-run t1_engine with the reconciled overlay (C18), then restate the T4′ facility need |
| ADIC overlay data | High | adic_data | Synthesis §7.2, item 8 |
| gap_03 unverified | Medium | more_research | Check SIMM parameters against the ISDA text; run T4 against a licensed calculator |
| Option-surface data | Medium | more_research | Equity risk reversals and butterflies; FX; CDX option vols; swaption cube; ICE Brent options |
| Monetization thresholds [I]; replay and engine conflict | Medium | build_experiment | Daily-step policy search with DSR/PBO guards; a λ^w estimator |
| Literature refinements not yet folded in | Medium | user_decision | Left-tail-premium trigger; VM receipt delays; one funding-stress state; trend decay after crises; provenance haircuts |
| Short-put exposure embedded in the hedge-fund book sits outside OV1 | Medium | build_experiment | Per Agarwal–Naik and Jurek–Stafford, net it into economic vega |
| OV thresholds, φ, the budget floor and net-short-vol permission | Medium | user_decision | All are [I] or set by the IC |
| No delta-hedging policy for the sleeve | Low | user_decision | Israelov et al. 2023; run both choices as ablations |
