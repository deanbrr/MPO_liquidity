# Q09 audit (R9): fusing underwritten, actual, forecast and market-implied returns

Read-only sufficiency audit, 2026-10-18. Corpus tags: [S] sourced, [C] corrected, [I] default, [I-calc] SYNTHETIC computation (never ADIC data).

**Verdict: mostly sufficient.** The fusion can be designed now. The core that fuses underwritten (u), actual (a) and forecast (f) returns is close to buildable. The market-implied anchor is not specified as a fused input. Per-group bias and credibility values are judgment priors until ADIC's own forecast history is scored.

## 1. Answer today

The research specifies a deterministic Forward Belief Engine (FBE) (07 §1, §6; C2 §4.2 "FBE v2"; main §4.3). It translates u, a and f onto one basis (forward log return on nowcast NAV, net of fees, with as-of timestamps), anchors on an outside-view prior, debiases against ADIC's own forecast–outcome history, fuses by precision weighting, and scores continuously.

How each piece works:
- **Two paths.** Fund interests use Bornhuetter–Ferguson/Benktander credibility, with a prior frozen at inception, fused only with the forecast. Single deals use a Gaussian posterior with correlated errors.
- **Since-inception IRR is sunk.** It is shown greyed out.
- **Per group** (groups synthesis §5; main §4.3 table): a group-specific translation rule; one shared bias model with group, strategy and age terms; one overconfidence parameter κ_g; one forecast precision 1/(κ_g²σ̂²), with no second credibility multiplier (G8 verify R11).
- **IC presentation** (groups §7.4): information value, not "bias", against the group's own reference class, only when n_eff ≥ 20, never as a league table.
- **Tiers.** Tier 2 uses posterior means; Tier 1 the posterior 10th percentile, with group bias stressed by +2 sd.
- **The market-implied return is a diagnostic only.** It is ρ_π, and flag F10 fires at |ρ_π − μ̂| > 400bp (07 §6.2; C2 §4.2). Whether it becomes a fourth fused input is undecided.

| Number | Meaning | Source | Tag |
|---|---|---|---|
| 36% | Share of outcomes inside executives' 80% intervals; the anchor for widening stated ranges ×1.81–2.74 | 07 §4.5; 07 verify row 9 | [S] |
| κ_g prior median 1.75 (90% range 1.16–2.64) | Overconfidence prior; a stated 80% range then covers 54% of outcomes | groups synthesis §5 | [I-calc] |
| b^u / b^f in pp a year: PE +5.0/+3.0 (+4.0 late); Co-investment +6.0/+3.5; Secondaries and Capital Solutions +2.0/+1.5; hedge funds +3.0/+2.0; long-only +1.0/+0.75; Private Credit +0.75/+0.75 | Per-group optimism priors for underwriting (b^u) and forecasts (b^f) | groups synthesis §5 table | [I] defaults, not estimates |
| χ²₁₉ = 207 (critical value 30.1); 80% coverage 0.727 | SBC flags a fusion that ignores the correlation between u and f errors | G9 §3, E4 | [I-calc] SYNTHETIC |
| 0.757 vs 0.898 | Coverage of nominal 90% group-bias intervals: cluster-blind vs cluster-aware (ICC 0.3) | G9 §3, E3 | [I-calc] SYNTHETIC |
| FBE-B under all misspecifications combined (MALL): excess CRPS +46.9%, coverage 0.545, SELL bias 3.00pp. FBE-R: +9.1%, 0.746, 1.47pp | The production-style estimator (FBE-B) fails four gates; the robust one (FBE-R) fails only M5s (+15.8% against a 15% gate). Robustness costs ≈7pp of CRPS when the model is right | groups gap_02 §3 Table 5; values reproduced from `misspec_ensemble_proto_results.json` | [I-calc] SYNTHETIC |
| 13.6% fused (80% band 7.8–19.7%) vs a 22.2% forecast; P_opt 96.3% | Worked example. P_opt is ≈94% even with zero assumed optimism, from shrinkage alone | 07 §6.8 Ex. 1; 07 verify R8 | [I] hypothetical |
| SELL flips at a bid of 86.9% of NAV | Example 3 assumes an 88% bid; tail-end interests trade near 70% (Evercore) or at 25%+ discounts (Jefferies) | 07 verify R1 | [C] |

**In plain terms:** the u/a/f fusion is specified at equation level and its method is evidence-based; the per-group magnitudes are directional priors; the market anchor is a diagnostic only.

## 2. Evidence

**Strongest support:**
- **Stream 07 and its verification.** Of 30 claims, 24 confirmed, 2 corrected, 0 refuted, 4 unverifiable; every worked example reproduces; reliability MEDIUM (high for facts, medium for design). Its design defects R2 (BF double counting), R3 (outcome noise in Ω), R4 (Mack's t) and R6 (timestamps) are fixed in C2's FBE v2 and main §4.3.
- **Stream 07 literature review.** 42 citations checked, none fabricated, 3 mismatched; Jenkinson–Sousa–Stucke and Barber–Yasuda are now confirmed.
- **Groups §5–6 and the groups gap_02 prototype.** This is the only test of the fusion against generators it does not assume.

**Weakest link: per-group magnitudes.**
- No study tests PE underwriting projections against outcomes (lit synthesis §4.17).
- No behavioural evidence exists for private-credit or structured-capital forecasts (07 lit §4.6), so the Private Credit and Capital Solutions priors must be wide.

**Contradictions:**
1. **Weighting rule.**
   - Main §4.3 fuses by constrained GLS with correlated errors, and the FBE-R prototype estimates weights from the full covariance matrix.
   - The literature verdict (lit synthesis §4.10, Smith & Wallis 2009) and design brief §7.7 say otherwise: shrink weights toward equal, keep covariances only in the predictive variance, and adopt GLS only if it beats simple and screened averages out of sample.
   - G9 E4 supports keeping the correlation in the variance. The main text has not been reconciled.
2. **Market anchor.** Stream 07 §6.2 and C2 §4.2 treat it as a diagnostic only. G2's spec card ("shrinking toward y^MKT"), G6 §1 item 7 ("fuse with market-implied loss-adjusted yields"), the main §4.3 Secondaries row and design brief §6 graft 1 treat it as a signal. Stream 05 verification R16: buyer targets are gross hurdles boosted by deferral and leverage, not clearing returns.
3. **Estimator selection on synthetic data.**
   - Groups gap_02 picks FBE-R for production from the prototype, and its gate values were set after one run (groups §6, "Freezing").
   - Lit synthesis §3.13 (Advani et al.) and design brief §7.13 say SYN-ADIC-177 tests correctness and robustness; it must not choose between estimator variants.
4. **Credibility cap.** Design brief §7.7 and the G8 literature review (Graham 2022) cap credibility beyond about 8 quarters. That clashes with "no extra credibility multiplier" (G8 verify R11).
5. **Outside-view priors.**
   - Main §4.3's hedge-fund α priors of 0.5–2.0% conflict with lit synthesis §4.11, which recommends α ≈ 0 against a put-writing baseline.
   - The long-only and Private Credit priors are contested in the same section.
   - Main §4.3 still applies a GP-fundraising covariate to single deals, though there is no deal-level inflation (07 lit §5, row 10).
6. **Pay finding.** "Pay design is a precondition" rests on variant M5s, with δ\* = 320bp. G8 verify R13 finds absolute δ\* overstated by about 3.5×.

**Already resolved:** κ vs κ_conf (groups C14); double shrinkage (G8 R11); σ_k cut from 6% to 5.5% (07 verify R9); BF double counting (R2); outcome noise in Ω (R3).

**Citation-audit errors that touch Q09** (lit synthesis §2.3–2.4):
- **Cooke's "26 of 33 in-sample"** is an out-of-sample index; in sample it is 32 of 33 (Colson & Cooke 2017). This affects any performance weighting of forecasters.
- **Brown–Ghysels–Gredil betas.** 1.05/1.20 are working-paper figures; the published ones are 1.0/1.4. This affects the VC nowcast β̃.
- **Nadauld et al.** The seller PME is 0.976, and the data cover 2006–2014.
- **Campbell–Sharpe anchoring** calibrates w_a or ρ_f, not w_u (G9).
- **Mack's t = 0.5** is a switching rule, not a credibility parameter.
- **PitchBook's interim-vs-final R²** is still unverified.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | The pipeline, both paths, group translations, bias model, κ_g, registry, scoring, display rules, simulation coupling and flags are all specified. |
| BUILD | No (nearly) | The u/a/f core is at equation level and prototyped. Still open: the weighting rule, the market anchor and its bias model, t vs parameter-free Benktander, and the credibility cap. The fund-interest path (PE, $52bn of working NAV, a SYNTHETIC assumption) is untested beyond arithmetic. |
| IC ANSWER | Yes, at method level | The IC can be told defensibly how beliefs are fused and what the synthetic tests show, with their uncertainty. It cannot be given per-group credibility verdicts. |
| NEEDS ADIC DATA | Yes | b^u, b^f, κ_g, slopes, Ω and ρ by group; development triangles; the NAV-bias term ψ_k; bids; and the out-of-sample weighting test. |

## 4. Gaps

| Gap | Impact | Close by | Detail |
|---|---|---|---|
| Per-group bias and credibility are priors | high | adic_data | Needs a bitemporal forecast archive that includes declined deals. Whether ADIC has one is open (07 §9 Q1). |
| Role of the market anchor | high | user_decision | Diagnostic (F10) or fused signal? Secondaries desk quotes need conflict controls. |
| Bid-to-expected-return model | medium | more_research | If the anchor is fused: bias and precision of ρ_π by fund age, deferral, leverage and adverse selection. Nadauld buyer–seller gaps are +3.0pp at 4–9 years and −0.8pp at 10+ years. About 27% of processes failed. |
| Weighting rule | medium | build_experiment | Default to shrunk or diagonal weights, with constrained GLS as the challenger. The final choice needs ADIC out-of-sample data. |
| Fund-interest path untested | medium | build_experiment | Run SBC and parameter recovery for BF/Benktander, and test whether TVPI or DPI triangles fit Mack's variance model. |
| Prototype scope and post-hoc gates | medium | build_experiment | Freeze the gates. Add NAV-biased actuals and a market signal, and rerun M5s with B′ = 1/H_g. |
| Contested group priors (hedge funds, long-only, Private Credit, PE; the deal covariate) | medium | user_decision | Adopt, or reject in an ADR, per design brief §7.8. |
| Credibility horizon cap | low | user_decision | For example, a horizon-dependent κ_g(h). |
| Calibration tests | low | build_experiment | Recalibrate linear pools; use autocorrelation-robust PIT tests, beta-binomial traffic lights, and SCRPS plus the log score. |
| Citation fixes | low | more_research | Published Brown–Ghysels–Gredil values; the Cooke label; the PitchBook R². |
