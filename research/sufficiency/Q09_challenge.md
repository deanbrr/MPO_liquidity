# Q09 challenge: skeptic review of the R9 fusion audit

Read-only review of `Q09_audit.md`, 2026-10-18. Tags: [S] sourced, [C] checked, [I] judgment, [I-calc] computed; results are SYNTHETIC unless tagged [S].

**Revised verdict: partial (the audit said mostly sufficient).**
- The audit's numbers are right.
- Its interpretation is not. It treats the gap_02 prototype as strong support and the ×1.81–2.74 widening as sourced.
- It misses the eighth group.
- It misses that the design has already adopted the market anchor and FBE-R.

## 1. Number checks: 10 of 10 found

| Claim | Location |
|---|---|
| 36% coverage | 07 §1, §4.5; 07 verify row 9 [S] |
| κ prior LN(ln 1.75, 0.25²); 1.16–2.64; 54% | groups §5; groups gap_02 §5. The prior is shared, but recovery mode pins per-group κ at 1.43–2.22 [I] |
| b^u/b^f table | groups §5; G9 §6.4 [I] |
| χ²₁₉ 207 vs 30.1; 0.727 vs 11.9 and 0.797 | G9 §3.7 E4 |
| 0.757 vs 0.898 | G9 §3.7 E3 (analytic 0.767, per G9 verify) |
| MALL +46.9%/0.545/3.00 vs +9.1%/0.746/1.47; M5s +15.8%; ≈7pp cost | groups gap_02 Table 5, which matches the JSON |
| 13.6% (7.8–19.7%); P_opt 96.3%; ≈94% at α_f = 0 | 07 §6.8 Ex. 1; 07 verify §4 and R8 |
| SELL flips at an 86.9% bid | 07 verify R1; C2 §5.3 |
| δ* 320bp / 80bp; overstated ≈3.5× | groups §5; gap_02 §3; G8 verify R13 |
| Nadauld +3.0 / −0.8 / −2.2pp; data 2006–2014 | 07 verify rows 17–18 |

## 2. Where the audit overstates

1. **"Widen ×1.81–2.74 [S]."**
   - Only the 36% is sourced (CFOs forecasting the S&P 500).
   - ×1.81 rests on a hypothetical 52% coverage in 07 Example 5.
   - G8 verify R9: inverting 36% into κ = 2.74 conflates bias with dispersion; the effective n is roughly the number of quarters. Show 2.74 only as an upper-end illustration.
   - G9 verify R9: the per-group κ values are not reconciled with that evidence.
   - Resolution C14 (κ vs κ_conf) fixed notation, not evidence.
2. **The prototype is weaker support than the audit says.** In `misspec_ensemble_proto.py`:
   - both estimators are given the true error SDs, and KAPPA is defined but never used, so κ_g is never estimated;
   - the outside-view prior equals the generator;
   - actuals are unbiased;
   - the eight pooled groups are identical;
   - SELL flags are exogenous;
   - forecast and underwriting error SDs are 3%, against the documented 6% (main §4.3; 07 §6.4; C2 §4.2);
   - the b^f prior SD is 0.01, against 0.02 in the documents.

   Table 5 also leaves two results out:
   - Under M4, where there is no anchoring, the regression detects the "gap" term in 61% of worlds (0.613 in the JSON, shown as "—").
   - Under MALL, flag power is 0.69, below G-D's 0.70.

   The M0 flag false-positive check is vacuous (flags are zero in M0).
3. **My in-memory rerun** ([I-calc] SYNTHETIC). It uses the corpus functions and seeds and writes no files, and it reproduces Table 5 exactly.
   - **Documented noise** (forecast and underwriting error SDs 0.06, b^f prior SD 0.02):
     - In M4, M6 and MALL even the variant-aware oracle has SELL bias of 1.76–2.34pp, above the absolute gates of 1.5 and 2.0pp. FBE-R has 1.98–2.18pp.
     - The post-hoc gates cannot be met at the corpus's own defaults, so "fails only M5s" is parameter-dependent.
     - False gap detection under M4 rises to 1.00.
   - **δ\* corrected to ≈91bp** (G8 R13): FBE-R passes every M5s gate: excess CRPS +12.1%, coverage 0.802, SELL bias 1.09pp, regret +27.1%.
     - The finding "pay design is a precondition for deployment" (groups §1 and recommendation 7; ARCHITECTURE §4.7 and ADR-24) does not survive this correction.
   - **Outside-view prior 2pp too high:** FBE-R degrades but passes (MALL +14.4%, coverage 0.722).
4. **"The market anchor is a user decision" is out of date.**
   - ARCHITECTURE §4.7 and ADR-24 already fuse a fourth mark, with a bias prior taken from Nadauld's gaps (+24.5 / +3.0 / −0.8pp).
   - The same ADR adopts FBE-R on synthetic evidence, against brief §7.13.
   - What is open is the evidence, not the decision.

## 3. Gaps the audit missed

- **Real Assets** (context §1A, brief §8; confirmed by the user, $18bn working figure) has no translation, b^u/b^f or κ, and no streams on disk; brief §8 even lists its market-implied mark.
- **The anchor is not identified.**
  - ρ_π = ln(R̂/πV)/H uses ADIC's own R̂ (07 §6.2; Example 3). If R̂ = E[R], then ρ_π − μ̂ = ln(V*/πV)/H, so F10 is just a discount flag.
  - ADR-24 uses realized, crisis-dominated PME gaps (07 verify R14) as an ex-ante bias.
  - Discounts also embed hurdles, deferral, fees and adverse selection (05 verify R16; G9 verify R11).
- **BUILD blockers:**
  - Three FBE-R specifications disagree: gap_02; groups §5 (with β_s, β_a and a t_ν(κ_g) likelihood); and ARCHITECTURE (adds an envelope covariate). Only the gap_02 version was tested.
  - There is no production estimator for fund interests: FBE-R needs u, and C2 §4.2 drops u for them.
  - Per-group prior SDs are missing, so Tier 1's "+2 sd" stress is undefined.
  - The Kalman step μ_{t+1} = m + φ(μ_t − m) + η_t has no φ, no Var(η) and no observation equation. It also contradicts "draw μ_i once per path" (main §4.3).
  - The shrinkage intensity is unspecified; 07 lit §4.3 suggests the Roccazzella closed form.
- **Literature conflicts the audit does not list:**
  - Boutros 2020: widen ranges per person and permanently, not per group "until scored".
  - Bordalo and Yee 2026: estimate β_f where each forecast is produced.
  - van Binsbergen 2023 and Prater 2017: the prior's weight must be earned.
  - Dahlquist 2026: the prior mean carries cross-CMA uncertainty.
  - IC views enter at face value (main §6.4, κ = 1) while group ranges are widened, which breaks principle L8.
- **Minor:**
  - Under allocation v2, PE is $34bn, not $52bn.
  - Lazard's 27% failure rate covers GP-led processes (05 verify A21).

## 4. Revised readiness

| Level | Verdict |
|---|---|
| DESIGN | Yes for seven groups. Real Assets and the anchor's bias model are missing |
| BUILD | No |
| IC ANSWER | Yes, but at method level and narrower. The architecture is standard and the magnitudes are judgment. The synthetic tests show computational correctness (SBC) and robustness only under favourable assumptions. Do not present the pay precondition, "FBE-R fails one gate" or the [S] widening as findings |
| NEEDS ADIC DATA | Yes: a bitemporal forecast archive, development triangles, bids with fund age, and per-person forecasts |
