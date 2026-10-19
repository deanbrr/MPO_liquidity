# Q15 challenge: the synthetic data generator (R15)

*Adversarial review of `Q15_audit.md`, 2026-10-18.*

**Revised verdict: partial (the audit said mostly sufficient). Audit not upheld.**
- Design-ready: yes.
- Build-ready: no.
- IC answer: yes, but only on the generator's role and its limits.
- Needs ADIC data: yes.

> **SYNTHETIC – NOT ADIC DATA.** Every [I-SIM] or [I-calc] figure here comes from SYN-ADIC-177 or from toy prototypes.

## 1. Number checks

I checked 10 of the most load-bearing numbers.

| Value | Found | Location and note |
|---|---|---|
| SHA-256 `4346dc24…f54a9` | Yes | groups gap_02 §1.3; groups §6. I recomputed it with Get-FileHash and it matches [C, challenger] |
| PE unfunded $16.4bn; total $27.0bn | Yes | gap_02 §0 and §1.2 Table 1 [I-calc], SYNTHETIC. The audit gives the wrong status: brief §8 says the user chose v1.1 |
| V16 rank χ² p > 0.01; V17 ±5pp; V18 CRPS skill > 0; V20 100% | Yes | G9 §6.6 [I] |
| χ²₁₉ = 207 against 30.1; 80% coverage 0.727 against 0.797 | Yes | G9 §3.7 E4; verify log §4 [I-SIM], SYNTHETIC |
| Coverage 0.757 against 0.898; analytic value 0.767 | Yes | G9 §3.7 E3; verify log §4 [I-SIM], SYNTHETIC. I re-derived the analytic value: 2Φ(1.645/√1.9) − 1 = 0.767 |
| FBE-B under MALL +46.9% and 0.545; FBE-R under M5s +15.8%; ≈7pp cost | Yes | gap_02 §3 Table 5; the results JSON gives 0.4687, 0.5452, 0.1579 and 0.0685 [I-calc], SYNTHETIC. The JSON reports no Monte Carlo standard errors |
| PE b^u +5.0 and b^f +3.0; κ prior median 1.75, giving 54% coverage | Yes | groups §5; gap_02 §5 [I]. In recovery mode PE's κ is pinned at 2.00 (48%), not 1.75 |
| V3 margins: 0.189 at p5, 0.0945 at p50 | Yes | Recomputed from G9 §3.7 E1e and §6.6 V3 [I-calc, challenger], SYNTHETIC |
| Gap-term power 0.613 under M4; flag-term power 0.692 under MALL | Yes | results JSON `M4.detection.power_gap` and `MALL.detection.power_flag` [I-calc], SYNTHETIC |
| "Worse than random" | Yes, but narrower than claimed | lit §3.13; G9 lit B1. The finding is for minimum *absolute bias*; the same paper is "better for mean squared error" [S, abstract-level] |

**Also confirmed:** the verify log's 24/2/1/0 of 27 claims (verify §1, §5); G9's 25/0/1 citations (lit §2.1); census v1.0 (main §10).

## 2. Where the audit overstates

1. **The audit's census status is out of date.**
   - Brief §8 records that "the user chose census v1.1 ($16.4bn)".
   - That makes three parts of the audit wrong: the "needs confirmation" row, contradiction 3 and gap 6.
   - The files that are actually stale are groups §6, gap_02 §7, and ARCHITECTURE §9.4 and Q2. ARCHITECTURE still says both censuses are shown "until the user confirms one".
2. **The FBE-R evidence tests an estimator that cannot run on real data.** In `misspec_ensemble_proto.py`:
   - Both estimators are handed the generator's true noise SDs: σ_u 0.03, σ_a 0.05, σ_f 0.03 (lines 125, 178).
   - FBE-R's u–f covariance estimate subtracts the true σ_a² (line 175) and is clipped using the true σ_u·σ_f (line 176).
   - `KAPPA` is defined but never used, so no stated ranges are generated and κ is never estimated.
   - "Robust" means robust given the true noise scales, on a static one-group toy.
3. **The build gaps are not minor.**
   - **No equation for O1 manipulation.** The verify log (R4) withdrew the original equation. The replacement exists only in words, and groups §6 drops GC2 §4.6's "+1pp at 2 SD above peers".
   - **No estimand mapping.** Under O4, PE's net forecast bias against truth is about w_u·b^u + b^f = 0.35 × 5 + 3 ≈ 4.75pp [I-calc, challenger].
     - The "shared prior" table labels +3.0pp as bias "vs truth", which does not match.
     - So M0 on the structural generator is not the well-specified case that SBC needs.
     - G-A and V16 are defined only on the toy.
4. **The role contradiction is real, but its evidence is thinner than the audit says.** Advani et al.'s failure is for absolute-bias selection, while FBE-R was chosen on CRPS. The rule rests more on G9 lit B2–B4. ADR-24 cites only gap_02.

## 3. Gaps the audit missed

| # | Gap | Impact | Close by |
|---|---|---|---|
| 1 | Real Assets, the eighth group (brief §8), has no engine, bias priors, census rows or gates, and G10–G15 are not on disk. The working v2 allocation (pending the user) cuts PE from $52bn to $34bn, so the v1.1 seal describes a bucket that v2 replaces; it is only rescaled (≈$10.9bn) | High | more_research |
| 2 | Re-run the ensemble on the O1–O4 generator, not the toy: estimate the noise scales, generate stated ranges and test κ recovery | High | build_experiment |
| 3 | Define the estimands: the map from structural θ to the FBE's β_g, γ and κ_g, and σ_true for the stated intervals. Add a reduced-form M0 mode for SBC | High | build_experiment |
| 4 | The sealed truth is public. The v1.1 vintage values and the regime history used to seal them (gap_02 §1.1) are printed in groups §6, gap_02 and ARCHITECTURE, and the CSV sits in `research/`. Any agent task graded against them is contaminated; brief §7.12 asks for leakage locks and canaries | Medium | build_experiment |
| 5 | The ensemble has no simple or screened-average arm, so brief §7.7's GLS test has not been run, even on synthetic data | Medium | build_experiment |
| 6 | FBE-R passes M2 by only 0.7pp of CRPS (14.3% against 15%) and 1.7pp of regret (33.3% against 35%). There are no Monte Carlo standard errors, and the gates were set after this run | Medium | build_experiment |
| 7 | The SELL-bias gate is absolute, not oracle-relative. Under MALL the oracle scores 1.58pp and FBE-R beats it (1.47pp), so the metric partly measures shrinkage | Low | build_experiment |
| 8 | ADR-24's fourth mark has a bias prior (+24.5 / +3.0 / −0.8pp) but only a one-line generator in ARCHITECTURE §9.4, with no truth behind it | Low | more_research |

## 4. Revised readiness

- **DESIGN: yes.** The layers, T1–T9, O2–O4 and L1–L8 are specified and fact-checked.
- **BUILD: no, for the full R15 component.**
  - Can be coded now: the truth engines and labelling.
  - Cannot be coded yet: the O1 manipulation term, the stylized-fact gates, the recovery estimands, the SBC mode and Real Assets.
- **IC ANSWER: yes, narrowly.** The IC can be told what synthetic results can and cannot prove. It must not be told that FBE-R is robust, even provisionally.
- **NEEDS ADIC DATA: yes.** As the audit lists, plus Real Assets data.
