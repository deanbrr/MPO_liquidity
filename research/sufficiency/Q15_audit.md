# Q15 audit: is the synthetic data generator (R15) specified, and is its role clear?

*Research-sufficiency audit, 2026-10-18. Read-only review of the corpus.*

**Verdict: mostly sufficient.** The generator is ready to design and build, but two of the five requested elements are incomplete. The stylized-fact checks have no pass criteria. The "correctness, not estimator selection" role is stated in the brief and the literature sweep, but the group layer contradicts it by choosing the production FBE on synthetic evidence alone.

> **SYNTHETIC – NOT ADIC DATA.** Every [I-SIM] or [I-calc] figure below comes from SYN-ADIC-177 or from toy prototypes.

## 1. Answer today

**Yes on specification; partly on role.** The research specifies SYN-ADIC-177, a structural generator with three layers (G9 §2.2, §6.3–6.4; groups synthesis §6):
- **World:** regimes, factors, the exit factor and the valuation gap.
- **Sealed truth:** skill, economic NAV, true μ, bias draws and outcomes. No estimator or agent can see it.
- **Observation:** the three marks, generated from the truth through named mechanisms. These are NAV smoothing and fundraising-window marking, underwriting optimism, sticky and overconfident forecasts, timing optimism and strategic bias.

Labels (L1–L8) are enforced in code. SBC and parameter recovery are release gates. The literature limits what the book can prove to correctness and robustness, not which estimator is best (brief §7.13; literature §3.13, Advani et al. 2019 [S, abstract-level]). The group layer has not applied that limit consistently (§2).

| Number | Meaning | Source | Tag |
|---|---|---|---|
| ≈395 positions + ≈1,500 loans + ≈250 trades; $177bn NAV; $38bn unfunded | Census v1.0 | main §10; gap_01 §8 | [A], SYNTHETIC |
| PE unfunded $16.4bn; total unfunded $27.0bn | Proposed census v1.1, which needs the user's confirmation | groups gap_02 §1.3 | [I-calc], SYNTHETIC |
| SHA-256 `4346dc24…` | Seal on the PE history; the auditor recomputed it and it matches | groups gap_02 §1.3 | [C, auditor] |
| R1: 1,000 worlds × 40 quarters; R2: 200 history worlds | Data releases | G9 §6.1 | [I] |
| V16 rank χ² p > 0.01; V17 coverage of 50/80/95% intervals within ±5pp; V18 CRPS skill > 0; V20 labels 100% | Recovery and labelling gates | G9 §6.6; groups §6 | [I] |
| χ²₁₉ = 207 against a critical 30.1; 80% coverage 0.727 | SBC catches a fusion posterior that ignores the correlation between forecast and underwriting errors | G9 §3.7 E4 | [I-SIM], SYNTHETIC |
| Coverage 0.757 vs 0.898 of a nominal 90% | Bias intervals that ignore vintage clustering vs intervals that model it | G9 §3.7 E3; verify log | [I-SIM], SYNTHETIC |
| FBE-B under MALL: +46.9% excess CRPS, coverage 0.545. FBE-R fails only M5s (+15.8%) | Misspecification ensemble, 2,000 worlds; the results JSON matches | groups gap_02 §3 | [I-calc], SYNTHETIC |
| PE b^u +5.0 and b^f +3.0 (+4.0 late in fund life), in pp a year. κ_g median 1.75, so a stated 80% interval covers 54% | Planted bias defaults | groups §5; gap_02 §5 | [I], direction anchored on [S] |

**In plain language.** The generator is specified well enough to build. Synthetic results can show that the engines compute correctly, that planted biases are recovered, and how estimators degrade under misspecification. They cannot show that the planted biases are ADIC's, or which estimator will do best on ADIC data.

## 2. Evidence

**Strongest sources.**
- **The G9 dossier and its verification log.** The log checked 27 claims: 24 confirmed, 2 corrected, 1 unverifiable and none refuted. It rates the facts HIGH and the design MEDIUM (G9 verify §1, §5).
- **The log's six material design errors are fixed** (GC2 §4.6; gap_01 §8; groups §6):
  - unfunded commitments sit *above* the steady state, rather than matching it;
  - the private-credit loss was ≈1.4%/yr, which failed the dossier's own V12 gate;
  - the vintage-alpha coefficient goes from −0.5z to −0.05z;
  - BGK's 2.6pp is treated as a symmetric peer reversion;
  - smoothing is set at fund level, not index level;
  - only LP-accessible actions are modelled (V23).
- **Groups gap_02 adds** a sealed PE truth with truth variants, the misspecification ensemble M0–M6 and MALL with gates G-A–G-E, a deterministic O3 module that passes 17/17 golden tests, a single κ_g, and gate V24.
- **The G9 literature check** found 25 citations, 0 not found and 1 mismatched.

**Contradictions.**
1. **Role.** Brief §7.13 and literature §3.13 restrict the book to correctness and robustness.
   - Neither research synthesis mentions this.
   - Groups gap_02 §3 concludes "Production uses FBE-R" from the synthetic ensemble alone. Its gates are labelled "pre-registered", but groups §6 says they "were set after one prototype run".
   - ARCHITECTURE ADR-24 adopts FBE-R without citing §7.13.
   - Brief §7.7 ("adopt constrained GLS only if it beats … averages out of sample") does not say where that test runs.
2. **Staleness.** Main §8 and §10 stop at V1–V23 and census v1.0. They lack V24, G-A–G-E, FBE-R and census v1.1.
3. **Superseded parameters.** Private-credit smoothing of 0.3 (G9, GC2) is now 0.5–0.7 (GC1 D17). Co-investment P(MOIC<1) of 0.22 is now 0.35–0.40 (GC1 D19). The private-credit loss pair went from 2.5%/0.40 to 1.8%/0.40 to LGD 0.67 / PD_N 1.1%, with GC1's pair kept as a truth variant (main §4.3). G9's census has ≈495 holdings against ≈395 elsewhere. ARCHITECTURE makes v1.1 the default although groups §6 requires the user's confirmation.
4. **Evidence against defaults.**
   - Reproducing BGH's 36% coverage needs κ = 2.74, above the prior's 90% range of 1.16–2.64 (gap_02 §5).
   - V14 checks bias realism against the generator's own table (±25%). That tests self-consistency, not external realism.

**Citation-audit items** (literature §2.3–2.4; verify log). Modrák et al. is *Bayesian Analysis* 20(2), 2025. Campbell–Sharpe's ≈0.3 calibrates w_a or ρ_f, not w_u (fixed in groups §6 O4 [C]). The BGG and HJK figures come from working papers, and "smoothing ≈0.5 (BGG)" is stream 04's derivation. BGK's sample is USD-denominated, not US. Aas, López de Prado and Borisov are unchecked.

## 3. Readiness

| Level | Ready | Reason |
|---|---|---|
| DESIGN | Yes | Layers, tables, T1–T9, O1–O4 by group, L1–L8 and the gates are specified and verified. ARCHITECTURE §9.4 already builds its design on them |
| BUILD | Yes, with minor gaps | Equations, defaults, schemas, the RNG hierarchy and numeric tolerances are enough to code and test. Still open: stylized-fact thresholds; two either/or choices (truncated vs NIG shocks; metalog vs sinh-arcsinh); fund-level GLM θ, still "to be extracted"; and frozen gates |
| IC ANSWER | Yes, with caveats | The IC can be told what synthetic results do and do not prove. FBE-R's selection must be presented as provisional, resting on synthetic evidence only |
| NEEDS ADIC DATA | Yes | Bias magnitudes, the census, realism (V15 C2ST), the semi-synthetic release and the final choice of estimator |

## 4. Gaps

| # | Gap | Impact | Close by |
|---|---|---|---|
| 1 | No estimator-selection policy has been adopted. Adopt the G9 literature rule (§4.1 item 20) by ADR: synthetic gates are pass/fail only; choose among the passing estimators on held-out ADIC outcomes; report several estimators side by side | Medium | user_decision |
| 2 | The gates were set after one run and are not yet frozen or hashed. G-D does not say which variants it covers: under MALL the flag term's power is 0.69, below the 0.70 bar; under M4 the gap term fires 61% of the time with no gap mechanism planted (results JSON); false positives are tested only under M0 | Medium | build_experiment |
| 3 | The stylized-fact checks have no numeric criteria. V3 passes E1e's mis-skewed fit (auditor's check: \|Δln\| 0.189 at p5 and 0.0945 at p50, against limits of 0.20 and 0.10). So V3 cannot catch the skew error the dossier itself found, and the terminal-first fix has not been demonstrated | Medium | build_experiment |
| 4 | Observation errors are too clean: NAV noise is independent, there is no manager effect and no model-error term, and b^f is regime-dependent only in M1. This is the OSSE failure mode in which the synthetic world is too easy (Privé et al. 2013; Errico et al. 2013) | Medium | build_experiment |
| 5 | The bias magnitudes lack an external anchor at LP level. No study tests PE underwriting against outcomes (literature §4.17), and V14 is circular | Medium | adic_data |
| 6 | Three decisions are open: the census default (v1.0 or v1.1); whether synthetic packs may appear in IC rehearsals; and who signs off the labels (G9 §9 item 9) | Medium | user_decision |
| 7 | Four items need ADIC data: the semi-synthetic release R3, the C2ST realism test (V15), the OSSE innovation match, and the haircut from synthetic to real skill | Medium | adic_data |
| 8 | The main synthesis lags the group layer. Calibration vintages are dated (BGK and HJK cover ≈1984–2008), and some citations are unchecked | Low | more_research |
| 9 | The G9 prototype scripts exist only in the session scratchpad. V16–V18 have no specified Monte Carlo standard errors or ADEMP cards | Low | build_experiment |
