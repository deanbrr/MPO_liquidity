# Gap 02 (groups): a sealed PE ground truth and a misspecification-robust validation layer for SYN-ADIC-177

**Date:** 2026-10-18 · **Companion to:** `research/groups/01_GROUPS_SYNTHESIS.md` (findings 3 and 9; §2.2–2.4, §3.1, §4.7, §5, §6) · **Status:** design-grade addendum. It proposes census v1.1, which replaces census v1.0's PE unfunded once the user accepts it. · **Computation:** `research/groups/addenda/gap_02_calcs/` (nine scripts with `*_results.json`; project venv, `python -I -B`).

> **SYNTHETIC-DATA NOTICE.** Every balance, commitment, cash flow, survival horizon, facility need and score below is synthetic or [I-calc]. None of it is ADIC data, and none of it may be presented as ADIC data. *SYNTHETIC – NOT ADIC DATA.*

**Research note.** The requested Consensus searches could not be run: the account returned "You've used all 500 included searches this month; resets on November 1st." Overlap anchors use KBRA DLD and other fetched sources (§8); re-run after 1 Nov 2026.

---

## 0. What changes

1. **Census v1.0's $27.4bn of PE unfunded is reproducible only by implausible histories.**
   - Under RFT-TA v2, smooth histories reach $27.4bn at a 7–11% H1-2026 distribution rate only with +17% to +29% a year of commitment growth into the 2022–26 drought, and all of them fail the contribution half of V6.
   - The only V6-compliant routes are two-spike histories, or V-shaped ones at the 7% edge of a looser contribution band (§1.2).
   - **Census v1.1 seals PE unfunded of $16.4bn** (U/NAV 0.32): H1-2026 distribution rate 9.0%, contribution rate 29.0%, 2026 pace $5.3bn. Total unfunded becomes $27.0bn.
2. **Finding 3's sign holds, but only for histories that pass V6.**
   - The sealed book's drought private book nets **+$3.7bn** (PE −$0.9bn).
   - The history that reproduces v1.0 nets −$0.1bn; 20%-a-year growth nets −$3.0bn.
3. **The stress results move a long way.**
   - T4 (s\*) year-1 PE drain: $14.0bn → $7.7bn.
   - Committed facility to clear 24 months: $40–41bn → $19.5–21bn at the fixed-USD draw, and $23–24bn → $2–4bn at the current-NAV draw.
   - L8: 0.81 (breach) → 0.75 (pass).
4. **PACE and co-investment.**
   - A 2027 pause returns $0.7bn in year 1 and $3.5bn by 2030, then costs $4.4bn by 2040; the implied cost is 9.8%.
   - Accepted co-investment flow is $0.6–1.2bn a year.
5. **Pre-registered misspecification gates now sit alongside SBC.**
   - The production-style FBE fails four gates.
   - A robust FBE fails only under status-quo pay, which makes pay design a precondition for deployment.
6. **O3, κ and overlap.**
   - O3 becomes a deterministic module (17/17 golden tests).
   - κ_conf is retired.
   - Overlap gets parameters and gate V24. On the overlap graph, the GP ≤ 5% limit binds in about a third of sampled censuses.

---

## 1. The census PE book (task 1)

### 1.1 Engine, targets, method

The engine is RFT-TA v2 (C2 §4.1) at its mean path, on a quarterly grid. The census date is 2026-09-30.

$$C=(1-e^{-\lambda\Delta})U,\ \lambda=-\ln\big(1-RC_s(\lfloor a\rfloor)\big)m^C(e);\quad D=(1-e^{-\delta\Delta})V(1+g)^{\Delta},\ \delta=-\ln\big[1-\min(0.95,(a^e/L_s)^{B_s})\big]m^D(e);\quad a^e\mathrel{+}=\kappa(e)\Delta$$

**Parameters.**
- **Liquidation:** a hazard of 35% a year applies once a^e ≥ L.
- **Expiry:** unfunded expires after age-year 8.
- **Strategies** (stream 04 §6.4):

  | Strategy | Calls (% of remaining unfunded) | L | B |
  |---|---|---|---|
  | Buyout and sector | 20/25/30/35/40% | 16 | 2.0 |
  | Growth | as buyout | 15 | 2.0 |
  | VC | 15/20/25/30/35% | 18 | 2.5 |
  | Special situations | — | 12 [I] | — |

- **Regime multipliers m^D / m^C / κ** (mid-points of the published ranges):

  | O | N | D | F |
  |---|---|---|---|
  | 1.25 / 1.3 / 1.2 | 1 / 1 / 1 | 0.475 / 0.975 / 0.6 | 0.325 / 0.8 / 0.5 |

- **Regime history:** N for 2010–20, O for 2021, D from 2022.
- **NAV growth:** 11% a year in N and O (12% for VC); 7% in D.
- **Strategy shares** are solved so the census NAV mix equals §3.1: 40/25/12/8/10/5.

**MSCI definitions, verified [S: MSCI Q2-2026, p.16].**
- "Distribution rate is calculated as period distributions / previous valuation, and is annualized."
- "Contribution rate is calculated as period contributions / (starting dry powder + capitalization of newly raised funds), and is annualized."
- H1-2026 PE values: **9% and 31%** (p.13). V6 checks both at ±2pp.

**Method.** Census quantities are linear in the vintage commitments c_v, so feasibility is an LP: maximise Σu_v c_v subject to Σn_v c_v = 52, both rates in band, and c_{v+1}/c_v ∈ [1/k, k].

### 1.2 What fits

*Table 1. Named histories on RFT-TA v2 (NAV $52bn).*

| History | 2026 pace | Unfunded | U/NAV | H1-26 distribution rate | H1-26 contribution rate | V6 distribution / contribution |
|---|---|---|---|---|---|---|
| Mature (flat) | 4.95 | 13.9 | 0.27 | 10.4% | 28.7% | pass / fail by 0.3pp |
| 10%/yr to 2022, then flat | 6.60 | 18.4 | 0.35 | 7.9% | 28.3% | pass / fail |
| 20%/yr growth | 15.3 | 31.9 | 0.61 | 5.8% | 26.0% | fail / fail |
| v1.0 reproduction (smoothest history at 27.4 and 9.0%) | 13.9 | 27.4 | 0.53 | 9.0% | 25.8% | pass / fail |
| **Sealed v1.1** | **5.34** | **16.4** | **0.32** | **9.0%** | **29.0%** | **pass / pass** |

*$bn. SYNTHETIC – NOT ADIC DATA.*

**Findings.**
- **The distribution half alone never binds.** With k = 1.25, unfunded can reach $35.5bn.
- **The contribution half at the H1-2026 points caps it below $27.4bn.**
  - At a 7.0% distribution rate: $21.6bn (k = 1.25) or $26.4bn (k = 1.5).
  - At 9.0%: $20.0bn or $24.7bn.
  - Only corridor-free histories with spikes exceed $27.4bn, for example $68bn committed in 2010, nothing until $20bn in 2023, then $70bn in 2024.
- **Against the averaged contribution band** (2022–H1-26 mean 29.2% ± 2pp), V-shaped histories reach $28.3bn, but only at a 7.0% distribution rate (commitments of $5.6bn in 2010, $1.8bn in 2015 and $11.9bn in 2024–25). At 9.0% the maximum is $26.2bn.
- **Plan-consistent histories top out lower.** The family is steady growth to 2020, a 2021–22 boom of at most 1.5×, a step in 2023, then −10% to +10% a year. It reaches **$19.3bn** on the H1 bands and $24.9bn on the averaged band, the latter only with +10% a year into the drought.
- **Smooth fits need a steep acceleration.** Minimum-curvature fits at $27.4bn grow commitments +17% to +29% a year over 2022–26, reaching 2.9–4.1× the 2019 pace.
- **Industry cross-check.** MSCI's H1-2026 figures imply (dry powder + newly raised) ÷ prior valuation ≈ **0.31**: (2×228/0.31)/(2×211/0.09) [derived]. The sealed book is at 0.40; the v1.0 reproduction at 0.64.

**Decision.** No history that is both plausible and V6-compliant reproduces $27.4bn, so census unfunded is revised. For 20% growth, v2 gives U/NAV 0.61 against G1's 0.52, because of quarterly timing, the hazard-form drought multiplier, m^C = 0.975 and the strategy mix.

### 1.3 Sealed census v1.1 and truth variants

**Rule, stated in `seal_history.py`:** within the plan-consistent family, require a distribution rate of exactly 9.0% and a contribution rate of at least 29.0%, and take the member with the largest unfunded (the liquidity-conservative choice).

**The sealed history.**

| Period | Rule | Commitments ($bn) |
|---|---|---|
| 2010–20 | +1.44% a year | $3.80bn → $4.39bn |
| 2021–22 | 1.5× boom | $6.67bn, $6.77bn |
| 2023–26 | −5.75% a year | $6.38bn → $5.34bn (¾ committed by the census date) |

**Commitment shares by strategy:** large buyout 39.9%, mid buyout 25.0%, growth 12.7%, VC 6.5%, sector 10.0%, special situations 5.9%.

**The book at the census date** [I-calc]:
- **NAV $52.0bn by vintage:** 2010–15 $7.3bn; 2016–20 $22.5bn; 2021–22 $12.8bn; 2023–26 $9.5bn.
- **Unfunded $16.4bn by vintage:** pre-2021 $0.6bn; 2021–22 $2.5bn; 2023–24 $5.6bn; 2025–26 $7.7bn.
- **Largest vintage:** 2021 at 13.1% of NAV, inside the 15% limit.

**Distribution-rate history against MSCI.**

| Period | Book | MSCI |
|---|---|---|
| 2011–20 | ≈22% | 24% → 17% (2017–20) |
| 2021 | 27% | 27% |
| 2022–25 | 10.7 / 10.4 / 10.0 / 9.5% | 11 / 9 / 11 / 11% |

The book is within ±2pp except in 2019–20, where it runs 4–5pp high. That gap belongs to the engine's normal-regime calibration, not to the census.

**The seal.**
- **File:** `sealed_pe_history_v1_1.csv`, giving commitments by vintage and strategy plus census NAV and unfunded by vintage.
- **SHA-256:** `4346dc249e83bff8d952588715a69ec038b9725ab436e0b24b8bb4227f2f54a9`.
- **In production** it moves to the sealed truth store (L6); estimators see only observation-layer data.

**Truth variants** use the same engine and NAV:

| Variant | Unfunded | Note |
|---|---|---|
| Mature | $13.9bn | — |
| 10%-then-flat | $18.4bn | — |
| 20% growth | $31.9bn | Fails V6 by construction; kept as the stress truth |
| v1.0 reproduction | $27.4bn | Kept for continuity |

**R15 recovery test:** estimators must recover the pace and the unfunded by vintage within V17's ±5pp coverage tolerance under every variant.

---

## 2. Re-runs on the vintage-resolved book (task 2)

**Only the PE leg changes.** Everything else is exactly as in the GS and GC2 scripts on the census split, imported read-only.

**Reproduction checks are exact.** The cash map reproduces with a difference of $0.00bn; GC2's T4 ladder (12 months, $41.97bn) and gap_01's state-machine result (15 months, $40.6bn) are both reproduced.

**The forward PE pace is each history's own 2026 pace.**

*Table 2. Group cash map, first 12 months ($bn).*

| | v1.0 (rate leg) | Sealed v1.1 | Mature | 10% → flat | 20% growth | v1.0 reproduction |
|---|---|---|---|---|---|---|
| Drought PE: distributions / calls / net | 6.34 / 8.65 / −2.32 | 4.63 / 5.48 / **−0.85** | 5.37 / 4.64 / +0.73 | 4.15 / 6.10 / −1.95 | 3.02 / 10.53 / −7.52 | 4.40 / 9.09 / −4.68 |
| Drought private book, net | +2.23 | **+3.69** | +5.28 | +2.60 | −2.97 | −0.14 |
| Liquid funding at a 7.5% payout (share of $71bn) | 11.1 (16%) | 9.6 (14%) | 8.0 (11%) | 10.7 (15%) | 16.3 (23%) | 13.4 (19%) |
| S1: PE net / private net | −9.81 / −11.98 | −3.89 / −6.07 | −2.41 / −4.58 | −4.96 / −7.14 | −11.14 / −13.31 | −8.50 / −10.67 |
| T4: PE net / private net | −13.97 / −18.40 | −7.72 / −12.15 | −6.55 / −10.97 | −8.62 / −13.04 | −14.98 / −19.40 | −12.93 / −17.36 |
| T4 liquid funding at a 10% payout | 42.3 (60%) | 36.0 (51%) | 34.9 (49%) | 36.9 (52%) | 43.3 (61%) | 41.3 (58%) |

*SYNTHETIC – NOT ADIC DATA.*

**Notes to Table 2.**
- **At GS's $7.2bn pace:** the sealed book's drought PE net is −$1.06bn (private book +$3.49bn); the v1.0 reproduction's is −$3.95bn (+$0.59bn).
- **Crisis-distribution convention:** S1 PE distributions use v2's F multiplier (5.4% of NAV). At G7's 3.5% convention, the sealed book's S1 PE net is −$4.89bn.

*Table 3. S1 and s\* (T4) ladders on the census split. Each cell shows static buckets / hedge-fund state machine (P5).*

| | v1.0 PE leg | Sealed v1.1 | v1.0 reproduction | 20% growth |
|---|---|---|---|---|
| T4, fixed-USD draw: SH_TP (months) | 13 / 16 | 17 / 19 | 13 / 16 | 12 / 15 |
| T4, fixed-USD draw: committed facility for 24 months | 41.4 / 40.0 | **20.9 / 19.5** | 44.4 / 43.0 | 52.0 / 50.6 |
| T4, current-NAV draw: SH_TP; facility | 15 / 18; 24.1 / 22.7 | 22 / 24; **3.7 / 2.3** | 15 / 18; 27.1 / 25.7 | 14 / 17; 34.7 / 33.3 |
| S1, fixed-USD draw: SH_TP; facility | 17 / 22; 3.4 / 2.7 | 35 / 31; 0 / 0 | 18 / 21; 5.3 / 4.6 | 16 / 19; 10.2 / 9.5 |

*SYNTHETIC – NOT ADIC DATA.*

**The CFP stage depends on convention.** On the sealed book under T4 with the fixed-USD draw, the stage is Red (17 months) with static buckets and Amber (19 months) with the state machine.

**PACE levers** are run on path L (drought to 2029) at the sealed pace of $5.34bn.

| Lever | Year-1 cash | Cash by 2030 | Cumulative 2027–40 | Implied IRR | NAV in 2031 |
|---|---|---|---|---|---|
| Pause 2027 | +0.67 (12.5%) | +3.51 (66%) | −4.38 | 9.8% | −7.5% |
| Pause 2027–28 | +0.67 | +6.22 (58%) | −8.13 | 9.6% | −13.6% |
| Halve 2027–28 | +0.33 | +3.11 (58%) | −4.06 | 9.6% | −6.8% |

*$bn. SYNTHETIC – NOT ADIC DATA.*

The shares are pace-invariant: the mature and 20%-growth books also release 66% within four years. Year-1 release is below G1's 20% because v2 commits quarterly.

**Co-investment flow (§4.7)** follows $O_t=\theta\sum_{k=0}^{4}d_kC_{t-k}$, with θ = 0.33, d = 0.15/0.25/0.25/0.20/0.15, acceptance 0.3–0.6, and C_{t−k} from the sealed history.

| Case | Accepted flow ($bn) |
|---|---|
| 2026 (offered $1.98bn) | 0.60–1.19 |
| 2027, pace held | 0.57–1.13 |
| 2027, after a 2027 pause | 0.49–0.97 |
| 2028, after a 2027 pause | 0.41–0.83 |
| 2026, v1.0 reproduction | 0.93–1.85 |
| 2026, 20% growth | 1.09–2.18 |

Sustaining about $3bn a year would need a PE pace of $15–30bn.

**L8 (private NAV + unfunded ≤ 0.80W).**

| Book | Ratio | Headroom |
|---|---|---|
| v1.0 | 0.814 | −$2.4bn |
| **Sealed v1.1** | **0.752** | **+$8.6bn** |
| 20% growth | 0.839 | — |

### 2.1 Restated findings (replacement text)

> **3. The drought sign depends on PE vintage structure. It is positive for every V6-compliant history.**
> - **Sealed census v1.1** (PE unfunded $16.4bn, pace $5.3bn): the private book nets **+$3.7bn** over 12 months. PE contributes −$0.9bn (distributions $4.6bn, 8.9% of NAV; calls $5.5bn) and the four other groups +$4.5bn.
> - **Across truth variants:** +$5.3bn (mature) to +$2.6bn (10% then flat). The result turns negative only for histories that fail V6: −$0.1bn for the history that reproduces v1.0's $27.4bn, which needs a $13.9bn pace, and −$3.0bn for 20% growth.
> - **v1.0's +$2.2bn** paired U = 27.4 with a $7.2bn pace and a flat 11% rate. No commitment history produces that combination.
> - **Payout:** 7.5% draws $9.6bn, 14% of the liquid book.
> - **T4:** the private book consumes $12.2bn in year 1, 64% of it PE. At cap draws the liquid book funds $36.0bn, 51% of itself [I-calc].
>
> **9. PE pacing is the slowest big lever, and co-investment rides on it.**
> - **On the sealed pace,** a one-year pause in 2027 returns $0.7bn in year 1 and $3.5bn by 2030 (66% of the amount forgone), then costs $4.4bn over 2027–40. The implied financing cost is 9.8%, before access, vintage and co-investment costs [I-calc].
> - **Co-investment flow** from lagged commitments is $0.6–1.2bn a year, and $0.4–1.0bn after a pause, against about $3bn needed to sustain $18bn.
> - **No V6-compliant pace sustains the book.** Sourcing must extend beyond ADIC's fund GPs, which the offer log will show, or the book shrinks.

**Knock-ons.**
- **Finding 6:** the T4 facility becomes $19.5–21bn (fixed-USD draw) or $2–4bn (current-NAV draw). "Starts in Red" holds only with static buckets and the fixed-USD draw.
- **§2.3:** the PACE row changes.
- **§2.4:** L8 now passes.

---

## 3. Misspecification ensemble with pre-registered gates (task 3)

SBC under shared priors (V16) stays as the computational check; robustness needs generators the estimator does not assume. G9's ensemble is restored and extended.

*Table 4. Ensemble variants. Only the generator changes; the estimator stays fixed.*

| Id | Mechanism | Specification [I] |
|---|---|---|
| M0 | Well specified | The SBC case |
| M1 | Regime-dependent optimism | b^f × (1 + 1{D}). Training is 30% D; test is 100% D (today is LATE × D) |
| M2 | Nonlinear anchoring | f = (1−w)f₀ + w·u, with w = 0.15 + 0.45·tanh((u − a − 0.05)⁺/0.04). The forecast clings to the underwriting after bad news [S direction: Easterwood & Nutt 1999, analysts underreact to negative information] |
| M3 | t3 tails | η_u, η_f and outcome noise are t3, rescaled to the Gaussian 80% width |
| M4 | Correlated u–f errors | corr(η_u, η_f) = 0.6 |
| M5 / M5s | Strategic bias | See the formula below. Designed pay (b 0.005, s 50, Z 0.4, B′ $400bn per unit) gives δ* = 80bp; status-quo pay (b 0.02) gives 320bp [G8 E5]. u_def = +2pp a year |
| M6 | Prior shift | True b^f = prior mean + 2 prior SD |
| MALL | All of M1–M6 | — |

**Strategic bias (M5 / M5s).**

$$b^f_{i,t}=b^f_g+\frac{b_gZ_{g,t-1}B'_{g,t}}{2s_g}+u_{def}\mathbb 1\{\text{SELL}_{i,t-1}\},\qquad B'_{g,t}=\partial\Lambda_g/\partial\hat\mu_g\ (=1/H_g\text{ if the envelope row binds, else }0)$$

- **The bias now responds to three things the generator ignored before:** envelopes, pay and the optimizer's own SELL flags.
- **The "defend-the-holding" uplift** draws on escalation evidence: executive turnover predicted later loan-loss provisions and write-offs across 132 California banks over nine years, and not the reverse [S: Staw, Barsade & Koput 1997].

**Gates (pre-registered; frozen and hashed before the first scored release; no tuning on release data).**

*Metrics:*
- excess CRPS over a **variant-aware oracle**, which knows the generator and so separates estimator failure from a harder world;
- 80% interval coverage;
- mean error on true SELL candidates (μ < 8%);
- excess SELL-decision regret.

*Gates:*
- **G-A (M0):** SBC passes; 80% coverage 0.75–0.85; excess CRPS ≤ 15%.
- **G-B (each of M1–M6):** excess CRPS ≤ 15%; 80% coverage 0.72–0.88 (about ±1 standard error at n = 20); SELL bias ≤ 1.5pp (half the PE b^f prior); excess regret ≤ 35%.
- **G-C (MALL):** ≤ 25%; ≥ 0.70; ≤ 2.0pp; ≤ 50%.
- **G-D (detection):** the pooled bias regression detects the regime, gap and flag terms with power ≥ 0.70; false positives under M0 ≤ 0.05.
- **G-E (pay):** a group that fails G-B under M5s gets non-trivial forecast precision only after the pay remedy: b ≤ 0.005, s ≥ 50, and nothing that scales with budget.

**Prototype.**
- **Set-up:** 2,000 worlds; a PE-like group; n = 40 resolved forecasts (320 pooled across 8 groups); 120 test assets.
- **FBE-B (production baseline):** pooled bias means shrunk to the §5 prior, independent errors.
- **FBE-R (robust):** a Huber bias regression on [1, D, gap, flag] with the slopes pooled across groups; u–f covariance estimated from the test cross-section as cov(u−a, f−a) − σ_a²; bias uncertainty propagated.

*Table 5. Results relative to the variant-aware oracle. Reference: B in M0 has CRPS 1.04pp.*

| Variant | B: excess CRPS / cov80 / SELL bias (pp) / excess regret | R: same | Detection power (regime / flag / gap) |
|---|---|---|---|
| M0 | +4.1% / 0.796 / 0.86 / +8% | +11.3% / 0.804 / 0.94 / +23% | 0.03 / 0.00 / 0.04 |
| M1 | **+16.0%** / 0.745 / **1.74** / +29% | +11.2% / 0.803 / 0.92 / +24% | 0.96 / — / — |
| M2 | +9.9% / 0.772 / 0.99 / +20% | +14.3% / 0.819 / 1.14 / +33% | — / — / 0.73 |
| M3 | +4.9% / 0.767 / 0.84 / +7% | +8.1% / 0.784 / 0.91 / +16% | — |
| M4 | +6.4% / **0.718** / 0.85 / +9% | +7.9% / 0.778 / 1.02 / +17% | — |
| M5 | +11.5% / 0.764 / 1.41 / +33% | +11.0% / 0.807 / 1.07 / +25% | — / 0.76 / — |
| M5s | **+18.4%** / 0.738 / **1.85** / **+50%** | **+15.8%** / 0.787 / 1.46 / +33% | — / 0.74 / — |
| M6 | +6.1% / 0.788 / 1.21 / +11% | +11.9% / 0.802 / 1.22 / +24% | — |
| MALL | **+46.9% / 0.545 / 3.00 / +53%** | +9.1% / 0.746 / 1.47 / +14% | 0.98 / 0.69 / 0.86 |

*SYNTHETIC – NOT ADIC DATA.*

**What it shows.**
- **FBE-B fails four gates:** G-B for M1, M4 and M5s, and G-C.
- **FBE-R fails only the M5s CRPS gate**, which triggers G-E.
- **Robustness costs about 7pp of CRPS** when the model is right.

**Design implications.**
1. Production uses FBE-R.
2. The bias covariates include the optimizer's own outputs: SELL flags and envelope status.
3. Bias coefficients are pooled across groups; one group's n = 40 cannot detect the strategic term.

---

## 4. O3: a deterministic performance module (task 4)

O3 changes from "computed with ADIC's own code" to `perf_module.py` (`perf-0.1.0`).
- **Inputs:** observation-layer data only, so actuals inherit every O1 reporting bias.
- **Conventions:** ACT/365F; Brent root-finding with a sign-change check, returning *None* rather than extrapolating; residual NAV treated as a terminal flow.
- **Benchmark:** a registry field per strategy.
- **Audit:** outputs hashed with the input snapshot.
- **Portability:** the same code will run on ADIC data.

*Table 6. Metric by holding type.*

| Holding type (groups) | Metrics and definition |
|---|---|
| Fund interests: PE funds, Secondaries S1/S3, credit funds. Also deal flows for Co-investment, CV stakes and kickers | **XIRR** solves Σ_k CF_k(1+r)^{−τ_k} = 0. **TVPI** = (ΣD + NAV)/ΣC, with DPI and RVPI alongside. **KS-PME** = [ΣD_t/I_t + NAV_T/I_T] / ΣC_t/I_t [S: Kaplan & Schoar 2005]. **Direct alpha** = ln(1 + IRR({CF_t·I_T/I_t} ∪ {NAV_T})) [S: Gredil, Griffiths & Stucke 2023] |
| Hedge funds, long-only | **TWR** = Π(1 + r_k) − 1. Each r_k is a Modified Dietz return between valuation dates; any flow above 10% of start value must coincide with a valuation [I]. De-smoothing (G5) is a derived series, not O3 |
| Private Credit; Capital Solutions debt and preferred | **Realized cash yield** = (cash interest + fees)/Σ(par·Δt). **PIK share.** **Realized loss rate** = (charge-offs − recoveries)/Σ(par·Δt). **Loss-adjusted cash yield.** XIRR for fund wrappers |
| Overlay | **P&L_book** = ΔMTM + cash (premia, coupons, settlements) − FTP × IM × Δt, for the tail, opportunistic and synthetic-beta books |

The golden tests pass 17/17. They include: XIRR of −100 then +121 over 730 days returns 10%; KS-PME equals TVPI on a flat index; an index tracker has direct alpha 0 and KS-PME 1.

---

## 5. One overconfidence parameter (task 5)

**Definition.** κ_g := w₈₀(true)/w₈₀(stated), where w₈₀ is the width of the 80% central interval. κ_g ≥ 1 means overconfidence; for Gaussian errors, κ = σ_true/σ_stated.

- **Generator:** q₁₀ and q₉₀ = f ∓ 1.2816·σ_true/κ_g. This replaces κ_conf, which equals 1/κ_g.
- **Estimator:** ε_j ~ t_ν(0, κ_g σ̂_j c_ν), with c_ν = 1.2816/t_{ν,0.9} (c₄ = 0.836) and σ̂_j = (q₉₀ − q₁₀)/2.563. This keeps κ's meaning under any tail.
- **Prior:** κ_g ~ LN(ln 1.75, 0.25²), a 90% range of 1.16–2.64.
- **Coverage of a stated 80% interval:** 2Φ(1.2816/κ) − 1, which is 54% at the prior median.

| Group | Old κ_conf | κ | Coverage of a stated 80% interval |
|---|---|---|---|
| PE | 0.5 | 2.00 | 48% |
| Secondaries | 0.6 | 1.67 | 56% |
| Capital Solutions | 0.5 | 2.00 | 48% |
| Co-investment | 0.45 | 2.22 | 44% |
| Private Credit | 0.6 | 1.67 | 56% |
| Hedge funds | 0.6 | 1.67 | 56% |
| Long-only | 0.7 | 1.43 | 63% |

**Modes.** SBC mode draws κ_g from the prior; recovery mode pins it to the table.

---

## 6. Company and sponsor overlap (task 6)

**One graph** links sponsors → funds → companies and every ADIC claim: PE look-through, Co-investment, Capital Solutions (family A fund finance; families C/D/E company exposure) and Private Credit loans.

**Pairwise overlap.** For group g, π_{g,PE} = s_g·c_g·h_g, where:
- s_g is the sponsored share of the group's borrowers or companies;
- c_g is the probability that the sponsor is one of ADIC's GPs;
- h_g is the probability that ADIC holds the fund that owns the company.

**One draw per company per path.** Each company's EV path is keyed by company_id in the SeedSequence hierarchy.

*Table 7. Overlap parameters and their anchors.*

| Parameter | Value | Anchor |
|---|---|---|
| s_PC, sponsored share of PC borrowers | 0.75 | KBRA DLD index: about 1,700 sponsored and 600 non-sponsored borrowers (74%; 22 Mar 2024). US private-debt capital in sponsored deals: mean 78% (n = 38); Europe 42% [Block, Jang, Kaplan & Schulze]. US direct-lending deals: 57.9% sponsored in Q1-2026, above 80% post-pandemic [PitchBook LCD] |
| Sponsor concentration | Top decile backs about 50% of borrowers | S&P (8 Dec 2023): 133 BDC and interval-fund portfolios, about 5,400 borrowers. Seen only in search summaries **[U]**; not load-bearing |
| Lender clubs | 61% of upper-middle-market issuers sit in ≥ 2 portfolios (20% lower middle market). Average BDC overlap 9.2% (portfolios > $5bn) down to 1.4% (< $1bn) | Cliffwater via Future Standard (Q1-2026). LFI/SOLVE (data at 30 Jun 2025). KBRA: 41 AI-exposed loans spread across more than 90 vehicles run by 28 lenders (27 Mar 2026) |
| p_co / h_co | 0.70 / 0.90 | Census v1.0 [A]; co-investment rights attach to fund LPs [I] |
| h | ≈0.6 | 120 funds across 70 GPs, over about 3 active funds per GP [I] |
| p_csA / p_csC | 0.50 / 0.50 | [I] |

**Sampler results** from 20 censuses in `overlap_graph.py` [I-calc]:
- **Co-investment in PE look-through:** 0.67 by count, 0.69 by value.
- **PC loans to look-through companies:** 0.13, about 190 of 1,500 loans.
- **Capital Solutions C/D/E in look-through:** 0.33.
- **Capital Solutions family A lending to ADIC-held funds:** 0.47.
- **Co-investments with an ADIC PC loan:** 0.08, about 7 deals. This is the recap-netting set.
- **GP concentration:** the largest GP averages **4.7%** of private NAV + unfunded (p95 6.6%). **35% of censuses breach the 5% hard limit.**

**Gate V24 (new).**
- **V24a, identity.**
  - Every claim on company k in world w reads one EV draw.
  - Defaults and recaps hit every claim in the same quarter, with waterfall-consistent payoffs.
  - Intra-ADIC recap flows net to zero, which extends V2.
- **V24b, rates.** Each realized overlap share must sit inside the binomial 90% band around its parameter-implied expectation, and each parameter inside its anchor range, until ADIC look-through data replace them. At census sizes the bands are:

  | Pair | Band |
  |---|---|
  | Co-investment ∩ PE | 0.59–0.76 |
  | PC ∩ PE | 0.115–0.143 |
  | Capital Solutions C/D/E ∩ PE | 0.15–0.51 |
  | Capital Solutions A → ADIC funds | 0.26–0.74 |
  | Co-investment with an ADIC PC loan | 0.03–0.13 |

- **V24c, concentration.** GP ≤ 5% is computed on the graph. Census draws that breach it are rejected, unless the run is a labelled concentration stress.
- **V24d, dependence.** The FBE's ρ_GP = 0.6 shock applies only to holdings that share a GP on the graph.

---

## 7. Patch list and data requests

**Edits to the group report.**

| Section | Change |
|---|---|
| §6 census, §1A | PE unfunded 27.4 → 16.4; total 38.0 → 27.0. This revises a working assumption, so **the user must confirm it** |
| §2.2 | Use Table 2's sealed column; rewrite "Reading the map" item 2 |
| §2.3 | Restate the PACE row |
| §2.4 | Restate L8 |
| §3.1 | Update the defaults and truth variants |
| §4.7 | Compute flows from lagged commitments |
| §5 | Replace κ_conf with κ |
| §6 | Add the O3 module, the ensemble and gates, and V24; replace the "shared priors" sentence |
| Findings | Restate 3, 6 and 9 |

**Data requested from ADIC.** The first item is decisive.
1. PE commitments by vintage and strategy since 2010.
2. Look-through company and sponsor IDs.
3. PC loan tapes with sponsor IDs.
4. Co-investment offer logs.
5. The pay parameters b and s.

---

## 8. Sources (accessed 2026-10-18)

- MSCI (Oct 2026). *Private Capital Benchmarks Summary Q2 2026*, pp. 13, 16. https://www.msci.com/downloads/web/msci-com/research-and-insights/paper/msci-private-capital-benchmarks-summary/2026-q2/MSCI-Private-Capital-Benchmarks-Summary-Q2-2026.pdf
- KBRA DLD (22 Mar 2024), via SFNet. https://sfnet.com/home/chapters/canada/news-detail/2024/03/25/kbra-dld-report-direct-lending-defaults-low-sponsored-at-1.5-non-sponsored-at-3.5
- KBRA (22 Jan 2025): an index of about 2,400 borrowers, via ai-CIO. https://www.ai-cio.com/news/direct-lending-default-rate-expected-to-rise-to-3-in-2025/
- KBRA (27 Mar 2026). *Private Credit: Deep Dive on AI and Software*. https://www.kbra.com/publications/KztddwRk/kbra-releases-research-private-credit-deep-dive-on-ai-and-software
- Block, Jang, Kaplan & Schulze (2023/2024). A survey of private debt funds. NBER w30868, Table 3; *RCFS* 13(2). https://www.nber.org/papers/w30868
- PitchBook LCD via Yahoo Finance (29 May 2026). https://finance.yahoo.com/markets/stocks/articles/pe-backed-companies-losing-direct-223251276.html
- Future Standard (7 Aug 2026), Cliffwater data at 31 Mar 2026. https://www.futurestandard.com/insights/chart-of-the-week/private-credit-unique-issuers-market-segment
- LevFin Insights via CreditSights (21 Oct 2025). https://know.creditsights.com/us-insight-lps-look-to-diversify-direct-lending-exposure-as-larger-deals-drive-bdc-portfolio-overlap/
- S&P Global Ratings (8 Dec 2023) **[U: full text returned 403]**. https://www.spglobal.com/ratings/en/research/articles/231208-credit-trends-sponsor-diversity-can-mitigate-private-markets-risk-12940947
- Staw, Barsade & Koput (1997). *J. Applied Psychology* 82(1), 130–142. https://experts.arizona.edu/en/publications/escalation-at-the-credit-window-a-longitudinal-study-of-bank-exec/
- Easterwood & Nutt (1999). *J. Finance* 54(5), 1777–1797. https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1777-1797.html
- Kaplan & Schoar (2005). *J. Finance* 60(4). https://dspace.mit.edu/handle/1721.1/5050
- Gredil, Griffiths & Stucke (2023). *JCF* 81, 102360. Seen via a secondary summary. https://altss.com/glossary/direct-alpha
- Internal sources: C2 §4.1; stream 04 §6.4–6.6; G1 §4.2; G8 E5; the GS, GC2 and gap_01 calculation folders.

*SYNTHETIC – NOT ADIC DATA (all [I-calc] figures).*
