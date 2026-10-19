# Q04 (R4) audit: the owner-set 5–10% distribution as an oil-linked stochastic liability

**Verdict: mostly sufficient.** The component is ready to design; its Phase-1 reduced form is ready to build; the IC can be given a qualified answer today. Calibration, the Abu Dhabi basis and owner behaviour rest on priors until ADIC and the owner supply data. SYNTHETIC means the working book or stylised proxy runs, not ADIC data.

## 1. Answer today

**Structure: credible.**
- **The draw.** It is a clipped, smoothed function of the owner's *pre-transfer* financing need (synthesis §4.7; C3 §5.1–5.2).
  - Drivers: oil price × UAE volume, and a six-state oil-shock type Z coupled to the macro regime.
  - Features: an override; quarterly instalments on opening-of-fiscal-year reported NAV; a mandate switch whose default is the owner's call.
- **Option shape.** A NAV-scaled vertical put spread: the 5% floor above ≈$67 Brent and the 10% cap below ≈$23 on the linear map (≈$64/≈$31 on the log map), ≈$200m of draw per $1/bbl (synthesis L3; C3 §5.1c) [I-calc].
- **Wrong-way risk depends on the shock type** (dossier 03 §2.4): supply gluts raise draws while markets stay fine; demand busts are the triple wrong-way state; Gulf wars raise needs while oil is up. Oil–equity correlation was −0.14 before 2008, +0.43 in 2008–19 and +0.32 since 2020 (dossier 03 §4.1) [I-calc rep.].

**Calibration: not yet credible.**
- **The only sourced fiscal anchors are UAE-level** (dossier 03 §4.5) [S]: the IMF consolidated breakeven of $44.8/bbl, and hydrocarbon revenue falling from 11.3% to 9.1% of GDP over 2026–30.
- **The owner-side parameters are assumed and rated low confidence** (C3 §5.8) [I]: the rule (c 7.5%, b 0.625, ρ_d 0.5); override probability (0.25%, 1% or 2% a year); ADIC's share ω; the breakeven prior (median $55, 90% range $45–70).
- **The Gulf-war wedge** of ≈−5 to −7pp of GDP rests on one projected IMF year. It cannot be separated from the breakeven (C3 §5.1c) [I-calc].
- **No ADIC draw history** exists in the research.

**Abu Dhabi vs UAE: unresolved.**
- No Abu Dhabi-specific data were used (dossier 03 §8).
- The IMF's caveat on partial Abu Dhabi coverage attaches to the adjusted-balance line, so how much of Abu Dhabi the breakeven covers is unclear.
- Headline revenue may include SWF income, possibly including ADIC's own payouts. That is why the owner's state was redefined before fund transfers (verify 03 F1, issue 4).
- The $55 prior is a judgment standing in for Abu Dhabi's effective breakeven.

**Owner behaviour in crises: peer evidence only.**
- Sovereign precedents (dossier 03 §4.6) [S]: SWFs withdrew at least $46.5bn from asset managers in 2015; Norway made its first-ever withdrawal in 2016; Kuwait borrowed instead of drawing on its funds.
- Governments withdrew more than $211bn from SWFs in 2020–21 (lit 03 §4) [S, abstract-level].
- The override rate, ω and the owner's response to a band request have not been estimated.

**Payout sustainability (SYNTHETIC or stylised).**
- **Real value.**
  - The band straddles sustainability. Real NAV holds at a payout of ≈5.3% at the 8.3% mixture return [I-calc], 6.8% at a 10% return and 4.6% at 7.4% [C] (synthesis §2.3a).
  - Mean draws under the priors are 6.0%, 6.6–6.7% and 7.2–7.3% at breakevens of $44.8, $55 and $65 (synthesis §4.7; C3 §5.2) [I-MC rep.].
  - Draws therefore exceed the real-preserving rate by ≈0.7–2.0pp a year, which is planned real decumulation [I, my arithmetic].
- **Liquidity binds first.**
  - In today's drought, the $71bn liquid book pays out 9–25% of its own value each year to meet the draw (synthesis §1, finding 3) [I-calc].
  - The 12-month draw is $9.9–10.8bn (5.6–6.1% of NAV), P90 $10.0–12.7bn, assuming a 5.8% draw in 2026, a figure not yet known (gap_04 §6.2) [I-calc].
  - Higher forecast UAE output keeps the 2027 draw near the floor. The risk comes in a 2028–29 glut [I].
- **Tail.**
  - P(three consecutive years with draws ≥ 9.5%) rises from 0.8–1.4% to 10.2–15.3% as the breakeven moves from $44.8 to $65 (C3 §5.2) [I-MC rep.].
  - The breakeven matters roughly ten times more than the slope (dossier 03 §6.6) [I].
- **Red-event gate.**
  - The 1% red-event gate can be met in M1–M5 for a premium of 21bp a year if the owner pre-agrees 5% draws in crisis, and 62bp without that agreement (gap_02 §2.3) [I-calc].
  - Groups gap_04 §7 reprices these at 23–29bp and 66–76bp [I-calc].
  - The band activates in 12–22% of paths within 12 months and withholds $3.2–7.0bn of draws over five years (gap_02 §2.3) [I-calc].

## 2. Evidence

**Strongest sources.**
- **Stream 03 verification** (verify 03 §1): 28 of 32 claims confirmed, 4 corrected in scope, none refuted; 18 of 18 citations correct; scripts reproduce exactly. Facts rate high, design medium.
- **C3** applies every verifier correction.
- **The sustainability arithmetic** is [C], and the literature supports it (lit synthesis §4.1).

**Weaker sources.** gap_02, gap_04 and groups gap_04 are unverified [I-calc].

**Contradictions.**
1. **Draw levels in stress.**
   - Dossier 03 expects draws near the cap in a supply glut. Its own model gives 6.8–6.9% mean draws in gluts and demand busts (verify issue 1) [I-MC rep.].
   - gap_02's engine, which groups gap_04 imports, uses fixed targets of 10% (demand bust) and 8.75% (glut) with no oil simulation (t1_engine.py l.87; gap_02 §7) [I].
   - So the priced gate results do not use the §4.7 oil-linked draw.
2. **The §4.7 draw grid uses an older specification.** It comes from the log-form script: h is fixed at 11.0, and there is no override, fiscal noise or declining h. It is not the adopted linear, pre-transfer default.
3. **Is the cap hard?**
   - The user's clip at 5–10% and constraint T1 ("annual total ≤ 10% of B_y", synthesis §4.9) conflict with override paths that pay 12–15% (C3 §5.2) [I].
   - The override uplift is U(2, 5%) in C3 but U(2, 3.5%) in the engine.
   - P(2027 draw rate ≥ 9.5%) equals P(override) in every stored run (initial_state_results.json) [I-calc].
4. **The owner band.**
   - The synthesis calls it the cheapest route to the red-event gate (finding 6). The literature synthesis calls that contested, because the owner's cost peaks in demand busts (§4.2).
   - Mix A is the default without written agreement (design brief §7.3).
   - No engine models whether the owner accepts. The owner's cost is a placeholder 2% premium (synthesis §4.7) [I].
5. **Contested premises.**
   - Rosen et al. (2019) contradict the endowment-"hoarding" contrast.
   - Mork (2022) finds that smoothing raises depletion risk.
6. **The M6 floor.** The 2.4% floor with the band (synthesis §4.9) disappears once group playbooks are added: Mix B's M6 red-event rate falls to 0.09–0.12% (groups gap_04 §2) [I-calc].

**Citation audit.**
- Moutanabbir & Noureldin is superseded by the *IREF* 2020 version. Re-check the 0.01–0.07pp hedging-demand figure against it (lit synthesis §2.3).
- de Finetti (1957) is not indexed (§2.2).
- No usage error affects streams 02 or 03.
- Fixed by the verifier: the misattached IMF footnote, and SAMA→PIF wrongly labelled a fiscal draw.

## 3. Readiness

| Level | Ready | Reason |
|---|---|---|
| DESIGN | Yes | Complete, evidence-backed architecture: shock-type × regime chains, futures-started oil, pre-transfer fiscal state, clipped draw, override, NAV basis, mandate switch, rule library, constraints T1/T7/T8, IC panels |
| BUILD | Yes (Phase 1) | Equations, defaults, ranges and interval targets are code-ready (C3 §5.1–5.2, §5.8, §6), with three prototypes to reconcile. The Phase-2 structural form and the owner-acceptance and obligation extension are not specified |
| IC ANSWER | Yes, qualified | Credible structure with prior-driven calibration. The upper half of the band is real decumulation, liquidity binds, and the band is cheapest only if the owner agrees. The ranges come from inconsistent draw implementations |
| NEEDS ADIC DATA | Yes | Draw history 2015–26; rule text, basis, notice and cap; the 2026 rate; ω; the Abu Dhabi pre-transfer breakeven; willingness to pre-agree crisis draws |

## 4. Gaps

| Gap | Impact | Close | Detail |
|---|---|---|---|
| Draw history and rule text | High | adic_data | Calibrates b, ρ_d, ω and the override. ±0.8pp on the 2026 rate moves the 12-month draw by ±$0.9bn (gap_04 §6.2) |
| Effective breakeven and ω | High | adic_data | The breakeven dominates draw risk. Elicit it with SHELF on a pre-transfer basis |
| Band acceptance; owner-directed investments | High | user_decision | Decides Mix B vs Mix A (23–29bp vs 66–76bp). Needs written agreement and an elicited probability that the owner accepts in a demand bust |
| Abu Dhabi public fiscal data | Medium | more_research | Department of Finance releases, the IMF adjusted balance, the October 2026 REO and the 2026 Article IV |
| One draw engine | Medium | build_experiment | Re-run the adopted specification and replace the engine's fixed shock-type targets |
| Long-horizon depletion test | Medium | build_experiment | P(real NAV depletion over 20–30 years) under the oil-linked draw on the working book |
| Shock-type chain | Medium | build_experiment | Stationary shares miss targets: N 49% vs 55–65%, demand bust 7% vs 2–6% (C3 §5.1a). Re-estimate with identification uncertainty |
| Owner response that depends on its buffers | Medium | build_experiment | Make b and ω depend on the owner's buffers; let the spending reaction switch regimes (Shah 2026; Bjørnland 2026) |
| Cap hardness and override | Medium | user_decision | Reconcile the clip and T1 with override paths; unify the uplift |
| Verify the addenda | Medium | build_experiment | gap_04's volume index (5.20/4.34, g4_initial_state.py) may conflict with the IMF basis for h and the breakeven |
| Citation fixes | Low | more_research | Moutanabbir's journal version; the de Finetti title |
