# Q16 audit: liquidity survival and Corporate Finance funding

**Scope.** The 24-month stress (literal against calibrated), the facility need, the IG floor, the hedge-fund (HF) queue, the owner band and facility reliability in a joint oil–crisis state, each tested against the literature sweep. Read-only; no new engine runs. Every [I-calc] figure is **SYNTHETIC** (SYN-ADIC-177, census v1.0, six stylised proxy models M1–M6), not ADIC data.

## 1. Answer today

The research answers the question in structure and in synthetic numbers.
- **Literal T4** (equity −40%, PE-type distributions 0, calls ×1.5, 24 months, cap draws) cannot be bought, so it is demoted to a reverse stress.
- **T4′ = s\*(θ\*) replaces it.** Its 24-month funding gap equals the worst model's P99.6, so the deterministic row and the 1% red-event gate (T6) agree.
- **Under T4′** the do-nothing book survives 17 months on Treasury + Public Markets and needs about $14bn of committed revolver. A stage-triggered pacing cut lowers that to about $6bn; an owner-agreed 5% draw in stress removes it.
- **T6, not T4′, binds.**

**The gap.** Every facility figure credits the revolver at 80%. None was re-run at the literature's ≤50% availability in the joint oil–crisis state, which the design brief now requires (§7 item 2).

**Key numbers** (SYNTHETIC unless tagged [S]):

- **Literal T4.**
  - It needs $25–92bn of facilities across conventions (14–52% of NAV); $32.2bn at canonical conventions with 50% credit; survival 15 months. That exceeds T5's debt limits ($17.7bn target, $26.6bn hard) and PIF's $15bn revolver, the largest precedent [S] (`00_SYNTHESIS.md` §1 finding 5, §2.3(d); `addenda/gap_02.md` §1.3) [I-calc].
  - It lies beyond P99.99 in M1–M5 and at P99.87 in M6 (gap_02 §1.2) [I-calc].
- **T4′.**
  - θ\* = 0.76 and G\* = $11.1bn (M6, P99.6).
  - Facility need: $13.9bn; $6.1bn with the pacing rule; $0 with the band (gap_02 §1.2–1.3) [I-calc].
  - Ten replications give θ\* of 0.76–0.81; the pooled estimate is 0.79, needing $14.6bn. The $15bn cap binds at θ = 0.82 (`groups/addenda/gap_01.md` §0, §3) [I-calc].
- **Milder calibrations.** The mixture's P99.6 gives G\* = $4.1bn (θ = 0.42); the worst of M1–M5 gives $2.6bn (θ = 0.35) (gap_02 §1.2) [I-calc].
- **IG floor.**
  - 8% elastic and 4% hard. Usable IG + cash is $13.6bn against $14.2bn: 7.7%, or $0.56bn short.
  - An 8% hard floor lifts literal T4 to $41.5bn (gap_02 §1.1, §1.3) [I-calc].
- **HF queue.**
  - The whole book is noticed at t0, with crisis pass-through of 0.83.
  - A 0.5 pass-through moves literal T4 to $32.7bn; a fully gated book moves it to $64.9bn (`gap02_results.json`, named stresses; gap_02 §1.3) [I-calc].
  - The state machine adds 3–5 months of survival but cuts the 24-month need by only ≈$1.4bn (`addenda/gap_01.md` §5) [I-calc].
  - T4′ sensitivities to HF terms were not reported.
- **Owner band.** It activates in 12–22% of paths within a year and withholds $3–7bn over five years. Mix B (band) costs 21bp of premium against 62bp for Mix A (no band); 23–29bp against 66–76bp after PACE repricing (gap_02 §2.3; groups gap_04 §0) [I-calc].
- **T6.** Mix A certifies at 0.98% (M5 bound), Mix B at 0.79%. The M6 floor is 2.4% with the band and 5.2–5.8% without; in M6, large revolvers without the band fail covenant gate T9 at 1.6–2.4% (gap_02 §2.3) [I-calc].
- **Headroom price.** A dollar of month-24 headroom costs 24% PV before a revolver is signed and 1.1% after (groups gap_01 §0) [I-calc].
- **Auditor arithmetic, not a research result.**
  - The ladder sets facility need = gap ÷ credit (`gap_02_calcs/t1_engine.py` l.969).
  - At 50% credit, the do-nothing book needs ≈$22.2bn ($11.1bn ÷ 0.5), above PIF's $15bn and the $17.7bn target. With the pacing rule it needs ≈$9.8bn.
  - Mixes A and B keep positive T4′ headroom (≈+$7.5bn and ≥+$8.6bn; from the groups gap_01 §1.2 headroom rows).

## 2. Evidence

**Strongest support.**
- **Reproducibility.** Fixed seeds; groups gap_01's replica reproduces gap_02's ladder exactly (maximum difference 0.0); tests pass 8/8 and 18/18; groups gap_04 reproduces `t1_engine` path for path. The arithmetic is strong; realism is medium, because the models are stylised proxies and the calibration rule is [I] (00_SYNTHESIS L15).
- **External anchors** [S]: Basel LCR40.82 and Reg YY (0% facility credit in 30-day rows); LCR20.5 (usable buffers); the 2023 interagency liquidity Addendum (lines "may become unavailable"); Ivashina–Scharfstein (new loans to large borrowers −47% in Q4-2008); Chodorow-Reich–Falato (about a third of loans breached covenants); AltamarCAM (GFC calls −50%, distributions −60–82%).
- **Verification.** The G7 log confirmed 28 of 34 claims and corrected 6. **No adversarial verification log covers gap_02 or T4′.**

**Contradictions.**
1. **Facility credit.** gap_02 §1.1, 00_SYNTHESIS §2.3(d) and the groups synthesis §2.3 credit the revolver at 80%; `t1_engine` l.594 also uses 80% in demand-bust and Gulf-war crises. The literature synthesis (§4.3) and the brief (§7.2) set ≤50% in the joint oil–crisis state, zero for new facilities and a ≈1.1pp tightening premium. `design/ARCHITECTURE.md` §4.9 still specifies 80%.
2. **30-day coverage.** ADIC-LCR(30d) reads 2.10× (Green) in 00_SYNTHESIS §4.9, but 1.91× (Amber) on CF-controlled HQLA in the groups synthesis (C12, §2.4) [C].
3. **Census.** T4′ exists only on census v1.0. Census v1.1 (PE unfunded $16.4bn, not $27.4bn) cuts literal-T4 needs from $40–41bn to $19.5–21bn (fixed-USD draws) and from $23–24bn to $2–4bn (current-NAV draws), but T4′ on v1.1 is "not yet computed" (groups synthesis C21; groups gap_02 §2).
4. **θ\*.** 0.76 ($13.9bn) in the main synthesis; 0.79 pooled ($14.6bn) in the groups layer.
5. **Overlay line.** T4′ assumes a $4.05bn ladder payoff and a 1.5%-of-NAV opportunistic loss, which groups gap_03 refutes (V5); reconciled use is ≈$0.9bn larger (C18) [I; not an engine run].
6. **M6 floor.** 2.4% on gap_02's playbook-free engine; 0.09% on groups gap_04's integrated engine, assuming no playbook slippage.
7. **Band price.** 00_SYNTHESIS §4.7 prices the band as a 2% fiscal-stress premium [I]. The literature (§4.2) calls this contested: the owner's cost peaks in demand busts, and governments withdrew more than $211bn from sovereign funds in 2020–21 [lit, abstract-level].
8. **Recourse order.** P's fixed waterfall (00_SYNTHESIS §4.8) is contradicted by the literature (§4.4).

**Citation-audit items** (literature synthesis §2.4 #14; G7 literature file and verification log): Li–Strahan–Zhang tie 2020 line performance to Fed support and deposit inflows, a condition the facility assumptions drop and an oil–fiscal stress may lack; Gorton–Metrick's haircut spike was bilateral repo only; Lazard's 27% is a GP-led survey figure, not an LP-sale failure rate. No not-found or mismatched citation underpins a T4′ number.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | Conventions as hashed contract fields, the s\*(θ) family and calibration rule, ladder rows LR1–LR8, contingency-funding (CFP) stages, Phase I/II recovery, the HF state machine and the mandate switch are all specified; the literature endorses the architecture. |
| BUILD | Yes | Core code and tests exist, and facility credit is already a parameter (`Stress.fac_credit`). The literature's refinements are specified only as formulas, with no values or tests: state-dependent availability, the owner's acceptance probability, owner-directed obligations, a state-dependent waterfall and VM receipt lags. |
| IC ANSWER | No | The direction is defensible: literal T4 cannot be bought, T4′ can be met, and T6 binds. But the facility size and Mix A's T6 certification rest on an 80% credit the brief has superseded, and no engine has been run at ≤50%. |
| NEEDS ADIC DATA | Yes | HF terms τ per lot; PE commitments by vintage; existing lines and covenants; appetite for a syndicated revolver; the draw convention and a written band agreement; CSA terms. |

## 4. Gaps

| Gap | Impact | Close by | Detail |
|---|---|---|---|
| Revolver at ≤50% availability in the joint oil–crisis state | high | build_experiment | Re-run the T4′ ladder (`fac_credit=0.5`) and the T6 Monte Carlo (parameterize l.594); add GCC-lender wrong-way risk; re-certify Mixes A and B |
| Band priced at ADIC's cost; P(owner accepts) in demand busts; owner-directed investments unmodelled | high | build_experiment | Mix A is the default without written agreement |
| Written band agreement; draw convention | high | user_decision | The convention alone moves literal T4 between $25bn and $43bn |
| PE vintages; T4′ on census v1.1 | high | adic_data | Recalibrate θ\* and the need on the confirmed census |
| HF terms τ | high (stage); medium (facility) | adic_data | A fully gated book doubles literal T4 |
| Existing facilities, covenants, syndicate | high | adic_data | $10–15bn is unconfirmed; precedents support the low end |
| Calibration quantile; M6 weight | medium | user_decision | G\* spans $2.6–11.1bn |
| Overlay convention (C18); LCR basis (C12) | medium | build_experiment | Reconcile, then re-run |
| Waterfall ablation; two-quarter pacing lag; VM receipt delays; pre-funded term cash | medium | build_experiment | Brief §7 items 1, 9, 14 |
| Proxy models; gap_02 never independently validated | medium | build_experiment | Re-run on engine E under model-risk management |

**Verdict: mostly_sufficient.**
- Design and build are covered.
- One high-impact gap needs no ADIC data: facility reliability at ≤50% availability. Closing it is a parameter re-run on existing code.
- No facility figure should reach the IC until that re-run is done.
