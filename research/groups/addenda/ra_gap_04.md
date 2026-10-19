# RA gap 04: Real Assets estimators brought to the R15 standard

**Date:** 2026-10-19 · **Companion to:** `research/groups/02_REAL_ASSETS_SYNTHESIS.md` v1.1 (§4.2, §4.6, §8, §11, §14 Q7, spec card). Canonical standard: groups gap_02 §1, §3, §5 and `01_GROUPS_SYNTHESIS.md` §6. · **Status:** design-grade addendum. Every model number is [I-calc] on SYN-ADIC-177. · **Computation:** `research/groups/addenda/ra_gap_04_calcs/` (`ra04_*.py` with `*_results.json`; project venv, `python -I -B`; the G13 engine is imported read-only).

> **SYNTHETIC-DATA NOTICE.** All positions, vintages, cash flows, marks, forecasts and scores are synthetic or [I-calc]. External targets are public, dated statistics and are labelled as such. Nothing here is ADIC data. *SYNTHETIC – NOT ADIC DATA.*

---

## 0. Verdicts

1. **RAME under the canonical ensemble** (five segments).
   - **Passes:** the G-A metrics in all segments. SBC passes in four; CORE_RE's plug-in bands cover 0.725. G-B passes for M1, M3, M5 and M6.
   - **Fails:** M4 (transaction index contaminated by appraisals, 0/5), M2 (valuers resist markdowns, 2/5), M5s (2/5) and G-C (MALL 0/5). Every pre-registered τ axis fails G-B except the drought-only level bias (3/5).
2. **R2 holds only for a contemporaneous τ.** It passes for contemporaneous, mildly smoothed or level-biased indices (0.27–0.49). It fails with a one- or two-quarter lag (0.53–0.74), where adding τ is worse than ignoring it.
3. **G-D for RAME.** Lags are detected (power 0.99–1.00, no false positives); AR smoothing and drought-only bias are not (power ≤ 0.49).
4. **Bids.** Leave-one-out bids are harmless and add almost no information. Circular bids bias θ̂ by −2.3 to −5.3pp in droughts.
5. **RA forecast engine.**
   - **Production style:** FBE-B-RA fails M5, M5s and G-C.
   - **Robust:** FBE-R-RA with pooled terms and §8.5 fusion passes G-A, G-B for every variant except M5s, and G-C. So **G-E binds**: the pay remedy is a precondition for RA forecast precision.
   - **Components absent:** costs about 2pp of CRPS (brief §9).
6. **κ.** One κ_g per group, with segment effects as empirical-Bayes random effects. Scoring a segment κ needs 8–40+ annual resolutions.
7. **V-RA1 and V-RE2.** V-RA1 passes on Cannon & Cole's adjusted basis once smoothing depends on the downturn; VA_RE's failure was a basis artefact. V-RE2 fails out of sample: the GFC queue peaks at 40% of NAV, against 15–21% published.
8. **Seal and R15.** The census is reproducible and sealed. Pace and callable unfunded are recovered within 1–3%, but the intervals are 5–10pp too narrow. Lapse and recycling must be modelled: only about 70% of the unfunded is ever called.
9. **External gates.** These pass: OIL-X1, OIL-X3, CF-X1. These fail: OIL-X2 (the ENR deck lag), CF-X3 (RE drought appreciation), CF-X2 (infrastructure call rates).

---

## 1. The canonical ensemble on RAME

**Design.** Only the generator changes; the production filter stays fixed (G13's seven-state appraisal Kalman model, fitted by MLE on appraisals, listed proxy and transaction index τ). There are two layers:
- **Canonical layer** (`ra04_rame_ensemble.py ss`):
  - M0 is the SBC case: data are drawn from RAME's own model, with index-level parameters implied by G13.
  - M1–M6 are mapped onto the observation layer.
  - The oracle is a Kalman filter that knows the generator.
- **G13 layer:** G13's world, used for R2, G0 and bids.

Each layer covers five segments, with 100 worlds of 80 quarters on common seeds.

| Id | RAME mapping of the canonical mechanism |
|---|---|
| M1 | λ + 0.10 in the down regime |
| M2 | λ + 0.15 whenever true value is below the prior mark |
| M3 | t3 shocks and noises, rescaled to the Gaussian 80% width |
| M4 | τ = 0.7v + 0.3a (appraisal-anchored comparables) |
| M5 / M5s | Appraisal level +0.8 / +3.2pp, plus 2pp on the 30% of holdings flagged SELL (defend-the-holding) |
| M6 | Index noise AR 0.90 against the filter's fixed 0.75 (external appraisals rarer than assumed); noise ×1.5 |
| τ axes (§11) | TL1 / TL2: lag 1 or 2 quarters. TA3 / TA5: AR 0.3 or 0.5. TB: +3% level. TBC: +4% in the down regime only. TW = TL1 + TA5 + TBC |

**Metrics.** The SELL rule is: sell if the bid ≥ 0.861 θ̂, with θ = e^(v − a). The SELL bias is the mean θ̂ − θ on true-SELL quarters, in pp of NAV. Thresholds are canonical.

| Variant | Segments passing | Excess CRPS | 80% coverage | SELL bias (pp) | Excess regret |
|---|---|---|---|---|---|
| M0 (G-A metrics) | 5/5 | −0.8% to +0.1% | 0.78–0.79 | −0.09 to +0.02 | −4% to +4% |
| M1, M3, M5, M6 | 5/5 each | −3.7% to +11.2% | 0.78–0.83 | −0.26 to +0.46 | −9% to +18% |
| M2 | 2/5 | +1.8% to +94% | 0.63–0.81 | +0.5 to +3.1 | +1% to +103% |
| M4 | 0/5 | +26% to +45% | 0.51–0.59 | −1.4 to −0.3 | +27% to +78% |
| M5s | 2/5 | +3.7% to +31% | 0.73–0.80 | +0.8 to +1.4 | +3% to +50% |
| TL1 / TL2 | 0/5 / 0/5 | +19% to +72% | 0.37–0.57 | −2.1 to −0.4 | +21% to +97% |
| TA3 / TA5 | 0/5 / 0/5 | +6% to +55% | 0.46–0.67 | −1.1 to −0.2 | +7% to +92% |
| TB / TBC | 0/5 / 3/5 | +3% to +58% | 0.63–0.78 | +1.9 to +2.4 / ≈ 0 | −5% to +95% |
| MALL (G-C) / MALL + TW | 0/5 / 0/5 | +40% to +133% | 0.30–0.60 | −0.8 to +2.9 | +30% to +134% |

*SYNTHETIC; canonical layer, production fit with τ.*

**SBC (G-A).** In 300 replications per segment with parameters drawn from a prior, KS p is 0.12–0.34 and 80% coverage is 0.76–0.81 in four segments. CORE_RE under-covers: coverage 0.725, χ² p = 0.001. Plug-in MLE ignores parameter uncertainty, so a parametric bootstrap (already G13's advice for λ) is needed.

**G-D.** The lagged-τ likelihood test has power 0.99–1.00 on TL1, TL2 and TW, and false positives 0.00. The τ-innovation AR test reaches only 0.01–0.29 on TA3 and TA5. The regime test reaches 0.25–0.49 on TBC, with false positives of 0.04–0.10.

**G-E analogue.** Status-quo-pay strategic marks fail in three segments. The RAME counterpart of the pay remedy is valuation governance for flagged holdings (§8).

---

## 2. R2, starting gaps and the bid channel (G13 layer)

**R2: nowcast RMSE ≤ 50% of the appraisal RMSE.** Ranges are over five segments:

| τ in the generator | ALT (with τ) | ALT4 (τ yearly) | AL (no τ) | ALT band coverage | Pass |
|---|---|---|---|---|---|
| Contemporaneous, unbiased | 0.27–0.45 | 0.49–0.60 | 0.59–0.69 | 0.66–0.77 | 5/5 |
| Lag 1 / lag 2 quarters | 0.53–0.63 / 0.62–0.74 | 0.56–0.68 | 0.59–0.69 | 0.33–0.52 | 0/5 |
| AR 0.3 / AR 0.5 | 0.34–0.49 / 0.45–0.55 | 0.51–0.64 | 0.59–0.69 | 0.43–0.65 | 5/5 / 4/5 |
| Level +3% / +4% in drought | 0.31–0.46 / 0.28–0.47 | 0.50–0.61 | 0.59–0.69 | 0.57–0.75 | 5/5 |
| Worst case (TW) | 0.64–0.74 | 0.59–0.68 | 0.59–0.69 | 0.33–0.43 | 0/5 |

*SYNTHETIC.*

**What R2 shows.**
- **Lag is what matters.** The headline gains (28–33% in G13) need a contemporaneous τ. One quarter of closing lag removes them and makes the τ-augmented filter worse than the listed-only one.
- **Interim IC figures.** Until production RAME models τ's lag, IC figures use the listed-only grade: index RMSE about 5.3–6.3%, which is where ra_gap_01's 5.5% sits.
- **Annual-return error.** The nowcast's annual-return error (slope 0.92, sd 4.5pp with an ideal τ; 0.53 and 6.3pp under TW) parameterises the forecast engine's common-shock control in §3.

**G0.**
- **Gap left in the estimate.** Of an imposed 2%, 5% or 8% starting gap, 7–23% remains in Ĝ with τ (mean 16%) and 17–40% without it (mean 30%). The share does not depend on the gap's size.
- **Band coverage at the census date:** 0.57–0.81. Ĝ replaces an assumed G₀ (RA8), with bands about 1.25× wider at t0.

**Bids** (seen in half of all quarters).
- **Circular use.** If the bid being priced enters θ̂, θ̂ error falls by 0.3–5pp but θ̂ is biased by −2.3 to −5.3pp in drought, because the wider buyer premium is read as value. In ENR, drought SELL decisions rise from 0.7% to 5.6%.
- **Leave-one-out.** It removes the bias, but bids then add almost nothing: θ̂ RMSE 3.15–5.86 against 3.17–6.04, and regret within ±3%.
- **Bad τ.** Under TW, drought SELL decisions run at 4–14× the true rate. Fire sales come from a bad τ, not from bids.
- **The fourth mark.** It is the listed proxy plus τ. Bids serve as a leave-one-out diagnostic and premium-regime signal.

---

## 3. The canonical ensemble on the RA forecast engine

**World** (`ra04_fbe_ensemble.py`, 2,000 worlds). It extends the canonical prototype:
- the 115-position census is mapped to the eight §8.4 segments, with four annual resolutions;
- outcomes carry a common segment-date shock, observed through RAME's control (§2 linkage);
- forecasts anchor on the appraisal lag (w_a = 0.30);
- stated cases imply segment κ_s ~ LN(ln 1.75, 0.25²), unknown to the estimators;
- NOI and exit-cap components resolve fast; capex, schedule and strategic terms resolve only through total return.

The test date is late-cycle and in drought.

**Estimators.**
- **FBE-B-RA** (§8.4–8.5 as written): segment biases, fixed control and w_a, the segment κ table, independent errors, 50%-shrunk precision weights.
- **FBE-R-RA:**
  - regime, gap and flag terms pooled across the other seven groups (the regime term relative);
  - RA Huber regression, with segment random effects around the §8.4 priors and a pooled group shift;
  - one κ_g, the u–f covariance only in the variance, and §8.5 fusion.
- **R-GLS:** the same with canonical GLS. A pre-freeze ablation (`ra04_fbe_ablation.py`) shows GLS with an estimated covariance amplifies the κ error.
- **R-cap:** zero forecast precision.

| Variant | FBE-B-RA: excess CRPS / coverage / SELL bias (pp) / excess regret | FBE-R-RA | Gate (B / R) |
|---|---|---|---|
| M0 | 9.3% / 0.79 / 0.99 / 18% | 9.2% / 0.80 / 1.04 / 19% | G-A metrics: pass / pass |
| M1 | 13.0% / 0.78 / 1.47 / 26% | 10.5% / 0.80 / 1.05 / 23% | pass / pass |
| M2, M3, M4, M6 | 4.6–12.0% / 0.74–0.79 / ≤ 1.27 / ≤ 25% | 5.1–11.9% / 0.77–0.81 / ≤ 1.21 / ≤ 26% | pass / pass |
| M5 | 17.5% / 0.76 / 1.60 / 44% | 10.6% / 0.79 / 1.26 / 23% | **fail** / pass |
| M5s | 31.5% / 0.70 / 2.22 / 72% | 19.8% / 0.76 / 1.84 / 42% | **fail / fail → G-E** |
| MALL (G-C) | 29.0% / 0.63 / 2.52 / 35% | 5.7% / 0.76 / 1.55 / 9% | **fail** / pass |
| Components absent: M0 / M5s / MALL | 10.3% / 29.6% / 29.4% | 11.2% / 15.9% / 7.2% | R: pass / fail / pass |
| RAME quality: listed-only / worst τ (M0); worst τ (MALL) | 16.7% / 15.4%; 33.2% | 11.7% / 12.8%; 7.9% | B fails; R passes |
| G0 2% / 5% / 8% (ideal τ); 8% listed-only | 9.5–11.0%; 21.8% | 9.3–10.3%; 16.1% | R fails only the last (CRPS) |
| Archive 8 years (M0 / MALL); κ truth = §8.4 table (M0 / MALL) | 9.1 / 28.4%; 8.6 / 34.1% | 7.9 / 4.0%; 9.3 / 6.1% | R passes all |

*SYNTHETIC. R-GLS fails every variant on CRPS (+16.7% to +57%). R-cap passes only M4 and the MALL family.*

**Reading.**
- **Coverage under one κ_g is honest in every segment:** 0.790–0.806 under M0.
- **G-D.** Pooled detection reaches 0.94 for the regime term and 0.71 for the gap term. It reaches 0.68 for the SELL-flag term, just below 0.70; false positives are ≤ 0.04. Within RA alone the powers are 0.27 / 0.42 / 0.53, and the anchoring term reaches only 0.15–0.24, so w_a keeps its prior.
- **G-E.** M5s fails even the robust estimator, and status-quo pay costs about 9pp of CRPS (19.8% against 10.6% under designed pay). Under the canonical rule, RA forecasts get non-trivial precision only after the pay remedy (b ≤ 0.005, s ≥ 50).

---

## 4. κ settled: one κ_g per group, segment effects as shrunk random effects

κ := w₈₀(true)/w₈₀(stated), scored on realized outcomes with σ̂ = (P90 − P10)/2.563. Errors share a segment-date component: standardized errors have intra-cluster correlation ρ, and squared errors ρ². The test is a date-clustered log-ratio t test (5%, two-sided) on the census, with 4,000 replications per cell (`ra04_kappa_power.py`).

| Annual resolutions for 80% power | ρ = 0.1 | ρ = 0.3 | ρ = 0.5 |
|---|---|---|---|
| κ ratio 1.33 (the table's 1.67 vs 2.22) | 8 for large segments; 20–40 for GCC_RE, RE_DEV | 8 (VA_INF); 12 (large); 20–40 (small) | 20 (large); 40 (small) |
| κ ratio 1.20 (1.67 vs 2.00) | 8–20; > 40 (RE_DEV, GCC_RE) | 20–40; > 40 (RE_DEV, GCC_RE) | > 40 (VA_INF: 40) |

*SYNTHETIC. Test size is 5.0–7.7%.*

**n_eff.** At ρ = 0.3, bias n_eff accrues at 20.5 a year for the group but at 1.5–3.1 a year per segment, so a segment reaches n_eff 20 only after 6.4–13 years. The per-segment n_eff ≥ 20 rule cannot be met.

**Estimators** (RMSE of ln κ_s at 8 years, ρ = 0.3):

| Truth heterogeneity τ | Raw segment κ | One κ_g | Random effects (DL τ̂) |
|---|---|---|---|
| 0 | 0.123 | **0.040** | 0.064 |
| 0.10 | 0.123 | 0.106 | **0.093** |
| 0.25 | 0.124 | 0.253 | **0.116** |

*SYNTHETIC.*

**Decision.**
- **Parameterisation.** ln κ_g ~ N(ln 1.75, 0.25²), with segment deviations as empirical-Bayes random effects. The eight §8.4 values become prior means, not parameters to score.
- **Reporting a segment κ.** Only once it clears the power line above (about 8–12 years for segments with ≥ 16 positions). GCC_RE, RE_DEV and GF_INF stay pooled.
- **Fusion switch.** The n_eff switch for the 50% shrink-to-equal fusion applies at group level.

---

## 5. V-RA1 and V-RE2

**V-RA1** (`ra04_vra1.py`, 5 seeds × 100 worlds).
- **Basis.** Cannon & Cole roll the sale price back by the *appraisal-based* NPI appreciation (eq. 1–3). G13 compared unadjusted statistics against mixed-basis targets.
- **Published adjusted values (equal-weighted).** Mean absolute error 12.5%; 2006 boom +11.6% (s.e. 0.8%); 2008 crash −11.0% (s.e. 1.1%) (Tables 2A, 4A). Property-level increments: levered +1.0pp, office +1.5pp, closed-end fund 0.0pp, no recent appraisal +2.2pp (Table 8).

| Adjusted basis | Mean absolute error | Crash | Boom | Verdict (2 s.e.) |
|---|---|---|---|---|
| CORE_RE, G13 defaults | 10.6% | −8.4% (z +2.4) | +11.8% (z +0.3) | Crash too shallow |
| CORE_RE, λ + 0.10 in downturns | 10.9% | −9.1% (z +1.7) | +12.1% (z +0.6) | **Pass** |
| VA_RE, defaults / λ + 0.10 | 14.8% / 15.1% | −7.7% / −8.3% | +14.0% / +14.5% | Mean absolute error inside the VA band |

*SYNTHETIC. G13's unadjusted figures are reproduced exactly (CORE_RE 12.5% / +16.3%; VA_RE 17.1%).*

**VA_RE** gets a 12.5–16.5% band: the NPI mean, plus 4.7pp of property increments, capped at the worst NPI year. σ_e is not identified: 13.7–15.0% across σ_e 0.03–0.07, so it stays at 0.07. **CORE_RE** adopts G13's downturn-dependent smoothing, to which RAME is robust (M1, §1).

**V-RE2** (`ra04_vre2_queue.py`).
- **Inputs.** G10's machine (b 0.12, w 0.08), driven by the GFC stale-NAV gap: NPI quarterly returns (Cannon & Cole Appendix Table 1) relevered to 25% leverage, against FTSE Nareit REITs unlevered at 35% [I].
- **GFC.** The queue peaks at **40% of NAV in 2010Q1**, with a range of 23–45% across sensitivities. The published figures are ≈15% (Callan, 20 Feb 2025) and ≈21% of core NAV (Townsend via PREA, Winter 2024). **Fail**, in the conservative direction.
- **Fixes tried.** Each was refitted to 2022–26.
  - Capping the stale premium leaves the peak at 28%.
  - Markdown cancellations give 28–32%; they improve the 2022–26 fit (RMSE 0.94 → 0.61pp) and match 2023 payout speed (5.4% against ≈5%).
- **2023 payout speed** (not a fit target): 7.6% a quarter. **Pass** in 2.5–10%.
- **Fund dispersion.** A redemption-sensitivity spread s ≈ 0.3–0.5 reproduces Callan's 4Q24 spread (P5–P95 4–39%, maximum 35–52%). This is a calibration.
- **Likely cause.** Raw REIT gaps of 60–80% overstate the premium investors perceived. Requests should read RAME's filtered Ĝ.

---

## 6. Sealed RA closed-end vintage history and the R15 recovery test

**Method** (`ra04_seal_ra_ce.py`, the census v1.1 method).
- **Engine.** RFT-TA v2 mean path with §4.2 parameters. Unfunded lapses after age-year 6 (RE, ENR) or 7 (infrastructure). ENR is scaled by (Brent/75)^1.2.
- **Returns and regimes.** Returns follow MSCI's 2023 to Q2-2026 closed-end indices. Regimes: N 2012–19, D 2020, O 2021, D 2022–26.
- **Linearity.** Census quantities are linear in commitments, so feasibility is an LP.
- **Targets.** NAV $6.7bn and unfunded $3.1bn (§11).
- **External band.** Real estate funds distributed 7% of NAV in the year to Q3-2025, "about a third of the 10-year average" (Ares, 11 Feb 2026); used as 7% ± 2pp.
- **Rule.** Seal the plan-consistent member that reproduces the census unfunded inside the bands; otherwise the largest-unfunded admissible member.

| Sector | Commitments | NAV / unfunded ($bn) | U/NAV | Distribution rate to Q3-25 | Contribution rate, H1-26 | LP unfunded range (corridor 1.5) |
|---|---|---|---|---|---|---|
| RE | Flat: $0.33bn, then $0.43bn from 2021 | 2.60 / 1.20 | 0.46 | 6.8% | 26.0% | 0.18–3.61 |
| Infrastructure | +6.2% a year ($0.15 → $0.45bn) | 2.50 / 1.30 | 0.52 | 6.8% | 21.7% | 0.04–4.14 |
| ENR | −3.2% a year ($0.25 → $0.20bn) | 1.60 / 0.60 | 0.38 | 9.6% | 26.3% | 0.05–2.31 |

*SYNTHETIC. Unfunded by bucket (2012–19 / 2020–22 / 2023–24 / 2025–26): RE 0 / 0.19 / 0.41 / 0.61; infrastructure 0 / 0.23 / 0.42 / 0.64; ENR 0 / 0.10 / 0.21 / 0.29. Truth variants (unfunded RE / infrastructure / ENR): mature 1.03 / 0.80 / 0.60; +10% 1.58 / 1.33 / 0.91; +20% 2.18 / 1.98 / 1.25.*

**The seal.**
- **File and hash.** `sealed_ra_ce_history_v1.csv`, SHA-256 `5ed8acfd735f0d6b0425f0762ee61805f5b4d0654e44c59f72f0b51a897171a3`.
- **Census result.** The census is reproducible, so there is no revision, unlike PE v1.1.
- **Drought multiplier.** G10's 0.45 cannot meet the Ares point without +29% to +56% a year of commitment growth in 2023–26. The seal uses the synthesis' canonical 6% / 18% = 0.33.
- **External check.** A mature population on the same path gives 7.8% at Q3-25 (Ares: 7%), and a 10-year time average of 17.4% (implied: ≈21%) (CF-X1).

**R15 recovery test** (`ra04_r15_recovery.py`; 200 replications; bootstrap of 40 fund clusters × 10 draws).
- **Truth.** 15 / 24 / 15 funds; σ_ζ 0.30; lumpy Gamma(4) calls.
- **Observed.** Calls and contractual unfunded.
- **Estimands.** Next-4 and next-8-quarter calls (pace), and all future calls (callable unfunded), by vintage bucket.
- **Estimator.** Age × regime call rates, shrunken fund effects, and a lapse age learned from observed releases.
- **Gate.** V17: coverage 0.85–0.95 and |bias| ≤ 5%.

| Truth variant | Pace (8 quarters): coverage / bias | Callable unfunded: coverage / bias | V17 |
|---|---|---|---|
| Naive estimator (no lapse model) | 0.86–0.88 / small | **0.00 / +30% to +39%** | Fail |
| Sealed; mature, +10%, +20% histories | 0.82–0.90 / −1% to −3% | 0.76–0.82 / −2% to −3% | Fail (width) |
| Lapse two years later (learned) | 0.83–0.87 / −2% to −3% | 0.75–0.79 / −2% to −3% | Fail (width) |
| T4′ calls ×1.38, scenario-conditional | 0.82–0.86 / −1% to −2% | 0.77–0.84 / −2% | Fail (width) |
| Recallable distributions (10%) | 0.77–0.85 / −4% to −5% | 0.35–0.50 / −7% to −8% | Fail (structural) |
| T4′ ×1.38, unannounced | 0.00–0.15 / −21% to −22% | 0.18–0.35 / −9% to −10% | Fail (structural) |

*SYNTHETIC. Another seed (80 replications) gives callable-unfunded coverage of 0.84–0.89.*

**Reading.**
- **Recovery.** The bias is fine; the intervals are 5–10pp too narrow.
- **Callable share.** Only **69–71%** of census unfunded is ever called in drought (74–76% under T4′, 80–82% with a later lapse).
- **Model requirements.** Without a lapse model, callable unfunded is overstated by about a third. The engine must also model recycling and condition on the scenario's multiplier.

---

## 7. External-data gates replacing V-RA-CF and V-RA-OIL

The old gates checked the prototype against itself, so they could not fail: V-RA-CF required that the cash row "reproduces G15", and V-RA-OIL required "12.2m bbl ± 5%". Their ingredients are now tested against public data (`ra04_external_gates.py`). The barrel delta is derived from validated elasticities (12.2m bbl at $70, 9.0m at $95). Reproduction mode stays only as a software regression test, as ra_gap_01 uses it. Engine invariants are kept: cures ≤ maturing debt, intra-ADIC flows net to zero, and V-RA-CTRL.

| Gate | External target (source, date) | Model [I-calc] | Verdict |
|---|---|---|---|
| OIL-X1: ENR fund marks, 2014–16 (Brent path; ENR λ 0.50; 2-quarter deck lag) | Cambridge Associates private energy, 2015: −20.5% (Jun 2016; via G15) | −14.7% (−16.9% without the lag) | Pass (±7pp) |
| OIL-X2: mark timing, 2026 spike | MSCI natural resources, closed-end: Q1 +6.9%, Q2 +3.6% (Q2-2026, p. 7) | H1 +0.1% with the lag; +12.6% without | **Fail**: deck lag rejected |
| OIL-X3: sleeve elasticity | Listed oil equities against Brent: 0.33 (2020), 0.40 (2014–16), 0.71 (2026) (G12) | 0.34 | Pass (low end) |
| CF-X1: RE distributions | Ares: 7% at Q3-25; ≈21% 10-year average | Mature population: 7.8% / 17.4% | Pass |
| CF-X2: contribution rate, H1-26 | MSCI all private capital: 29% ± 5pp (p. 12) | RE 26.0%, ENR 26.3%, infrastructure 21.7% | Infrastructure fails |
| CF-X3: drought NAV growth | MSCI closed-end 2024–25 average: RE −0.15%, infrastructure +9.5%, natural resources +4.3% | G15: 3.0% / 8.0% / 7.0% | **RE fails** (+3.2pp) |
| CF-X4 / X5: open-end income | ODCE 4.08% gross (NCREIF); bfinance ≥ 6% | 3.25%; 5.5% | Identities, not counted |
| CF-X6: queue | V-RE2 | — | GFC fail; 2023 pass |

*SYNTHETIC model outputs against public targets. Episode elasticity = ln(1 + r_equity)/ln(1 + r_Brent).*

---

## 8. Design implications and patch list

1. **τ becomes a state in RAME.** Model τ\*_t = ρτ\*_{t−1} + (1 − ρ)v_{t−ℓ}, with an optional appraisal-contamination loading, estimated with the rest. Gate ALT figures on the lag test; use listed-only figures until it passes.
2. **Choose and test the index.** Prefer transaction-based indices, and test them for appraisal contamination (M4). Model direction-dependent smoothing (M2), which V-RA1's crash shortfall supports.
3. **Valuation governance is RAME's G-E.** For holdings under a SELL flag or card: external valuation, no carry-forward or internal marks, and a capped appraisal weight.
4. **Bids enter only leave-one-out**, with a regime-dependent premium. This settles §7.4's θ̂ rule.
5. **Production RA forecast engine = FBE-R-RA with §8.5 fusion**; GLS is rejected. The pay remedy is a precondition for its precision (G-E).
6. **κ** is one κ_g with empirical-Bayes segment effects (§4).
7. **Engine fixes.**
   - Drop the ENR deck lag for fund NAVs.
   - Set RE closed-end drought appreciation to about 0%.
   - Use the 0.33 drought exit multiplier in the vintage engine.
   - Model lapse and recycling, and report callable unfunded beside contractual.
   - Review infrastructure call rates.
8. **Queue machine.** Add markdown cancellations, drive requests with Ĝ, and label outputs as upper bounds. Zero Tier-1 credit stands.
9. **Gate harmonisation.**
   - R4 (≥ 0.75) gives way to G-A/G-B's two-sided bands.
   - R5 becomes the random-effects coverage error.
   - R2 keeps its τ condition.
   - V-RA1 moves to the adjusted basis with |z| ≤ 2.
   - V-RA-CF and V-RA-OIL become CF-X1–X6 and OIL-X1–X3.
   - RA-R15 (with the seal hash) is added.
   - Freeze and hash everything with G-A–G-E before the first scored release.

**Patches to `02_REAL_ASSETS_SYNTHESIS.md`.**

| Section | Change |
|---|---|
| §4.2 | Drought exit 0.33, lapse and recycling, seal reference |
| §4.6 | V-RE2 result and the queue changes |
| §4.7 | RE drought appreciation; callable share |
| §5 | λ_down; ENR deck lag |
| §8.2 | R2 statement, τ state, bids |
| §8.4 | κ column; components-absent result |
| §8.5 | Fusion confirmed |
| §11 | Gates table and the pre-registered axes with results |
| §14 | Data requests |
| Spec card | Updated accordingly |

**Data requests:**
1. RA closed-end commitments by fund and vintage, with commitment periods and recycling terms.
2. Fund-level open-end queue statements.
3. Whether archived plans store components (§14 Q7).
4. Valuation policy for flagged holdings.
5. ADIC's RA sales against the last appraisal.
6. The transaction index licensed, and its lag.
7. ENR GP price decks.

---

## Sources (accessed 2026-10-18/19)

- Ares (11 Feb 2026). Real estate secondary market volume hits record $20 billion in 2025. https://www.ares.com/us/news-and-insights/real-estate-secondary-market-volume-hits-record-20-billion-2025
- Cannon & Cole (2011). How accurate are commercial real estate appraisals? *JPM* 35(5), 68–88. https://doi.org/10.3905/jpm.2011.35.5.068; MPRA 32589, https://mpra.ub.uni-muenchen.de/32589/1/MPRA_paper_32589.pdf (eq. 1–4; Tables 2A, 4A, 4B and 8; Appendix Table 1).
- MSCI (Sep 2026). *Private Capital Benchmarks Summary Q2 2026*, pp. 7, 12, 13 and 16. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
- Callan (20 Feb 2025), ODCE queues (verified in the G10 log). Townsend/PREA queue figures (Kochis & Moné, *PREA Quarterly*, Winter 2024), via G14. Cambridge Associates, Real Asset Dynamics (Jun 2016), via G15.
- Public series in sibling folders: FRED DCOILBRENTEU; FTSE Nareit All Equity REITs; NCREIF ODCE 2022–26; Ken French industries and EIA Brent.
- Internal: groups gap_02 (`seal_history.py`, `rfta_v2_book.py`, `misspec_ensemble_proto.py`); the G10, G12, G13 and G15 calculation folders; ra_gap_01 and the integration memo (no conflicts).

*SYNTHETIC – NOT ADIC DATA (all [I-calc] figures).*
