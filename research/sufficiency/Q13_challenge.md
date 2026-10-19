# Q13 challenge: skeptic review of the Q13 audit

2026-10-18. Every quantity here is SYNTHETIC unless marked *public data*. [I-ch] marks this reviewer's own calculation. It was run read-only on `gap_05_calcs/*_results.json`, using a lognormal 10-year TWR and the bridge's τ.

**Verdict: upheld with amendments. The research is mostly sufficient.**

| Level | Ready? |
|---|---|
| DESIGN | Yes |
| BUILD | No |
| IC answer | Yes, but only in a caveated, directional form |
| ADIC data | Needed |

The audit's arithmetic holds. It understates the replacement-floor problem and repeats several overstatements from the research.

## 1. Number checks

| # | Claim | Found? | Where |
|---|---|---|---|
| 1 | Uplift +3.5 → +0.61 / +0.35 / +0.47pp | Yes | gap_05 l.194; JSON; synthesis l.1318 |
| 2 | ≈30% / ≈54% (audit: 29.4 / 53.7) | Yes, with a nit | gap_05 l.200. Exact: 29.34% and 53.75%; the singles sum to −2.919 against a joint −2.895 [I-ch] |
| 3 | Overlay +0.37–0.38pp = SR 0.30 × 1.25% vol | Yes | gap_05 l.95, l.192 |
| 4 | Drawdown 31.6 → 19.8%; forced sale 4.4 → 0.03% | Yes | gap_05 l.197–198. Computed for coalitions 0 and 63 only (`v8_rerun.py` l.157–158, 424) |
| 5 | 15.8–17.9%; P(5y < 7%) 31–55% | Yes | Verifier 10 l.105, l.29; C1 l.49–50 [C] |
| 6 | Tier 1B binds near 14.3% vol for an 8.5% book | Yes | Synthesis l.1223; dossier 11 l.417, where μ = 8.5% is *arithmetic* and tagged [I] |
| 7 | Worst-model CVaR10: −0.8% (M3), −1.5% (M6) | Reproduced | −0.78% and −1.54% from `bridge_results.json` [I-ch] |
| 8 | Holm p = 1.0 for all 12 additions | Yes | gap_04 l.13, l.87 (*public data*) |
| 9 | Contrarian −48bp (−121, +21); de-risking +46bp; drawdown 50 → 40% | Yes | gap_04 l.240, 243, 144. Six rules are tabulated, but the text says "seven variants" |
| 10 | Replica 7.14% vs 7.3% and 10.64% vs 10.8%; notionals 62% / 48% | Yes | gap_05 l.173–175; JSON kS 0.625, kM 0.476 |

Also confirmed:
- $0.56bn (synthesis l.325);
- F_t, drought 0.87 and Gulf war 0.85 (gap_04 l.127, 201, 203);
- Shapley standard error ≤ 0.4bp;
- 55.8% (paper l.2660).

## 2. Where the audit is wrong or too soft

1. **Tier 1B is worse than "likely fails".**
   - M5 (σ 17.0%, E[R] 8.86%) sits at −0.03%, or as low as −0.28% with τ. Three of six models therefore fail at t0 [I-ch].
   - Blending the book with each model's cash (indicative only, since private assets cannot be sold) passes the CVaR leg only at ≈16–17% cash excluding M6, or ≈26–27% including it. At those blends the mixture median falls to ≈7.6% and ≈7.2%. The two legs are therefore near jointly infeasible.
   - Because "8.5%" is an arithmetic mean, readers will wrongly think the 8.3% geometric mixture passes.
   - Severity: high, not medium. Verifier 11 R11 had already warned that the floor may bind.
2. **"Reading (b)" is mislabelled, and its feasibility is contradicted.**
   - Verifier 10 R6 (l.225) asserts that it is feasible, but the log contains no calculation.
   - Dossier 10 l.386 shows the E[R5] ≥ 7% floor breaking at 1.6pp, less than the 1.8pp gap between JPM and AQR.
   - On the working book, P(E[R] < 7%) is ≈26–27% across the six models [I-ch].
   - Tier 1B is really dossier 10's T1-F mixture test (l.397), which drops the 5% tolerance. Neither reading of v8's floor survives. Synthesis l.504 overstates the continuity, and the audit marks the issue "resolved".
3. **"α\*/QDD do not survive" is a design artefact.**
   - The run lasts 36 months.
   - Exposures ramp to only 9% and 6% of NAV.
   - An unsourced 1% liquidity charge flips α\* negative on ADIC's book (gap_05 l.180).
   - The 10-year bridge credits sleeve α\* with +0.37pp, equal to the overlay (gap_05 §6). The defensible wording is "untested at the right horizon".
4. **State's +0.11–0.16pp is an upper bound** (gap_05 l.206). The audit drops that caveat.
5. **"Add nothing" should read "not shown to add".** The test has ≈30 episodes and no power analysis, and turbulence's point estimates improve DD3 and CRED6 (gap_04 §4.1).
6. **IG + cash: the audit gives the wrong cause.** The $0.56bn is curable by a top-up (groups synthesis l.70). The research's rationale is Basel LCR20.5, and the 4% level is an [I] default (G7 dossier l.862).
7. **The bridge does not "replace" v8's 10.8% / 54.6%.** Those are 3-year means on a scripted path. The like-for-like figure is gap_05 §8: 4.72% → 5.19% ex ante.

## 3. Gaps the audit missed

- **The "≥ 2 worlds" gate is never instantiated** (synthesis l.1539, l.144). The run has one generator and no M1–M6 dimension, so its survives / NOT ESTABLISHED labels are not gate outputs.
- **`test_v8_replica` either fails or is vacuous.** Its tolerance is ±0.05pp per row (ARCHITECTURE l.1388). The level rows miss by 0.16pp, and the attribution rows were calibrated to match.
- **The forced-sale results rest on a fixed waterfall** (`v8_rerun.py` l.312–331), which literature §4.4 rates contradicted.
- **The run's filter is not the specified one.** It is a hard-coded 2-state Gaussian filter, not the F_t that ARCHITECTURE l.796 specifies.
- **No mapping rows exist for v8 slides 8–10.** The impact is low, because R13 requires only the motto.
- **J's γ = 3 and λ_T = 1 are unelicited.** Literature 11 §5 also rejects deriving γ from Ang et al. alone.

## 4. Revised readiness

- **DESIGN:** yes.
- **BUILD:** no. The audit's three items stand, plus the replica spec, the waterfall and the worlds.
- **IC ANSWER:** yes, but only in this form: "The skeleton survives. The floor, the objective, the lights and the +3.5pp do not. The replacement floor binds today. The re-estimates are single-generator prototypes, not for quotation (gap_05 §10)."
- **ADIC DATA:** yes.
