# Q04 challenge: the owner's 5–10% draw as an oil-linked liability

**Verdict: partial (the audit said mostly sufficient).**
- **Design:** ready.
- **Build:** ready for the Phase-1 reduced form only, once six specification choices are fixed (§2).
- **IC:** a directional answer only.
- **ADIC data:** needed.

The audit itself rates three of the question's four elements as open: calibration "not yet credible", the Abu Dhabi basis "unresolved", and crisis behaviour "peer evidence only". Sustainability is solid only at first order. SYNTHETIC = working book or proxy models.

## 1. Number checks (10)

All ten values are where the audit cites them. Four of them mean less than the audit implies.

| Value | Found | Location; caveat |
|---|---|---|
| $44.8/bbl | Yes | Dossier 03 §4.5; verify F1 [S] |
| 6.0 / 6.6–6.7 / 7.2–7.3% | Yes | Synthesis §4.7; C3 §5.2; draw_model_demo.json. **These are fixed breakevens from the superseded log script** (h 11.0, GW −6pp, no override or volume; draw_model_demo.py l.35–37), not values "under the priors" [I-MC] |
| 0.8–1.4% → 10.2–15.3% | Yes | C3 §5.2; dossier §6.6; same script [I-MC] |
| ≈$67/$23, ≈$64/$31; ≈$200m per $1/bbl | Yes | Synthesis L3; C3 §5.1(c). **Computed at the lower anchor (P^BE 44.8, q = 1).** At the $55 median the linear kinks are ≈$77/$33 [my arithmetic]. The $200m is the target slope; same-year exposure is about half (C3 §1 item 7) [I-calc] |
| $9.9–10.8bn; P90 $10.0–12.7bn | Yes | gap_04 §6.2; initial_state_results.json, Gulf-war-posterior runs only [I-calc] SYNTHETIC |
| ≈1.2% = P(override) | Yes | initial_state_results.json, every run [I-calc] |
| ≈5.3% (6.8% / 4.6%) | Yes | Synthesis §2.3(a); exactly 5.36% [I-calc]/[C] |
| 21 vs 62bp; 23–29 vs 66–76bp | Yes | gap_02 §2.3; groups gap_04 §7, which reprices pacing only [I-calc] SYNTHETIC |
| $13.9bn → $0 | Yes | Synthesis §2.3(d); gap_02 §1.3 [I-calc] SYNTHETIC |
| DB 10%, SG 8.75% | Yes | t1_engine.py l.87; GW is 8.0% [I] |

## 2. Where the audit overstates

1. **The near-term tail is an artifact of smoothing.**
   - With ρ_d = 0.5 and d_2026 = 5.8%, the draw cannot exceed 7.9% in 2027 or 8.95% in 2028, and cannot reach 9.5% before 2030, unless the owner overrides (C3 §5.2; g4_initial_state.py l.230–234) [my arithmetic].
   - So "P(2027 ≥ 9.5%) ≈ 1.2%" and the panel's year-1 Green (gap_04 §8) just restate the assumed override probability p_ov.
   - ρ_d (0.3–0.7, C3 §5.8) is itself the crisis-behaviour parameter the question asks about.
   - No stored run of the adopted specification covers the cited 2028–29 glut; the log demo's mean draw is flat at ≈5.9–6.2%.
2. **The band's $13.9bn headline is mechanical.**
   - T4′ fixes draws at 10%, 10% and 7.5%, and the band pays 5% in crisis months (t1_engine.py l.753, 879–880). The adopted draw model cannot reach the cap in FY2027–28.
   - θ\* calibrates only the total gap, so the stress leans on the draw. Removing ≈$8.85bn a year of assumed cap draw (groups synthesis §2.3) explains most of the move from $13.9bn to $0 [I-calc] SYNTHETIC.
3. **The engines disagree on year 1.**
   - gap_02 starts at d_prev = 7.5% with GW and SG targets of 8.0% and 8.75%. That gives ≈7.7% of NAV (≈$13.6bn) in year 1 [my arithmetic, t1_engine.py l.86–87, 279, 477–478]. gap_04 gives 5.6–6.1%.
   - The October state, including its 5.7% year-1 draw, moves do-nothing P(red) by 2–6pp (groups gap_04 §2, S1).
   - "One draw engine" is therefore high impact, not medium.
4. **The sustainability answer ignores the model range.**
   - Real-preserving payouts across M1–M6 are ≈3.4–7.2% (synthesis §4.12, E[R] 6.06–10.47%). Mean draws therefore exceed them by −1.2 to +3.9pp, not by 0.7–2.0pp [my arithmetic].
   - At September CPI of 3.74% (gap_04 §6.2), the mixture's real-preserving rate is ≈4.2%.
   - Only one statement holds in all six models: the upper half of the band is real decumulation.
5. **"The breakeven matters ten times more than the slope" holds for means only.** At $65, moving b from 0.625 to 1.0 lifts P(≥3 years ≥ 9.5%) from 10.2% to 15.3% (dossier §6.6). That is about half the breakeven effect.
6. **The glut state is mis-set.** C3 §5.1(b) uses ρ_SG = 0.1. The dossier's own Jul 2014–Feb 2016 window shows +0.40 (US) and +0.50 (developed) (§4.1) [I-calc]. How shocks are identified is contested (lit 03 §5 item 2).
7. **The circular fiscal basis comes back.** gap_04 builds d_2026 and its IMF fusion from headline net lending (g4_initial_state.py l.227–229, 268). That is the basis D9 rejected (C3 §2.2; verify issue 4).
8. **The case for the band changes from file to file.**
   - Main synthesis: the cheapest route to the gate.
   - Groups synthesis §1: needed for M6 capacity, not for T4′.
   - Groups gap_04 §2: with playbooks, Mix B's M6 rate falls to 0.09%; re-certification is pending (§8 item 8).
   - gap_02 §2.3: in M6, Mix B (6.5%) does worse than Mix A (5.8%).
   - Literature: contested (§4.2).

**Six choices to fix before the build:**
1. FN^bud is not operational; gap_04 uses realised 2027 prices.
2. The mid-year reset (C3 §4.2) is unimplemented.
3. ω must be reported but is absent from the Phase-1 equation.
4. Oil: spot-started one-factor (C3) vs futures-started two-factor (gap_04).
5. Gulf-war dwell: memoryless or duration-conditioned.
6. The override breaches the client's 5–10% clip (design brief §6).

## 3. Missed gaps

- **Owner-correlated assets.** Real Assets' energy holdings and Gulf real estate (design brief §8; no Real Assets synthesis is on disk), plus legacy domestic bank stakes (dossier 03 §5).
- **Abu Dhabi's own crisis financing** in 2015–16 and 2020 (borrowing vs fund draws), the empirical prior for ω and DebtCap.
- **Denominator.** FB uses UAE GDP and UAE h, but the owner is Abu Dhabi, so b×h, the draw's actual oil sensitivity, is unidentified.
- **Deflator.** Whether "real" means US CPI or AED prices is unstated.

## 4. Revised readiness

| Level | Ready | Basis |
|---|---|---|
| Design | Yes | The architecture survives |
| Build | Yes (Phase 1) | After the six fixes above |
| IC answer | Directional | The structure is credible; the calibration is not. The upper half of the band is real decumulation, and liquidity binds first. Oil-linked magnitudes and the band ranking are "not established" |
| ADIC data | Yes | Draw history and rule text (ρ_d, p_ov, d_2026), the pre-transfer Abu Dhabi breakeven, ω, energy holdings |
