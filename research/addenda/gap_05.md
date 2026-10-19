# Gap 05 addendum: what you need to believe to earn 10%

## An expected-return bridge for each CMA model, and v8's attribution re-run in the new engine

**Date:** 2026-10-18. **Closes:** critic gap 05, "no positive account of how the 10% target could be reached" (R5 target, R13 attribution).

**Inputs.** `00_SYNTHESIS.md` §1–§4 and §7; C1 §5.10; C3 DQ18 and DQ22; verification logs 10, G1, G4 and G5; dossiers G1–G6 and G8; GC2. Re-read in this session: EFW, HJK 2016, Gupta–Van Nieuwerburgh, Boyer et al., Berg–Saunders–Steffen, AQR 2026, the BlackRock workbook and the JPM 2027 LTCMA page.

**New computations [I-calc]** in `research/addenda/gap_05_calcs/`: `bridge.py` (bridge, break-evens, probabilities; regression-tested against verifier 10) and `v8_rerun.py` (50,000 paths, exact Shapley over 64 coalitions on common random numbers, CRN), with helpers `calib_v8.py`, `comonotone.py`, `lev_vol.py` and results in `*_results.json`. Tags follow the synthesis.

> **SYNTHETIC – NOT ADIC DATA.** All weights are the context §1A working allocation. Lever priors are syntheses of published evidence, not estimates from ADIC records.

**Fold-in map.** §1 → synthesis §1 findings 1 and 8. §2–§7 → new §4.12 (engine `bridge/`), §6.7 (a "What you need to believe", WYNTB, card) and §7.1 (lever priors, drag parameters). §8 → §4.11 (retire v8's +3.5pp), §5.4 gates and §8 (`test_v8_replica`).

## 1. Answer for the IC

1. **Beta.** On fee-consistent CMAs the working book's beta is **5.8–10.0%** geometric (equal-weight mixture 7.85%). That is wider than the stylized book's 6.2–9.7%, because ADIC is 50% PE-family and so inherits the providers' disagreement on the private premium.
2. **Evidence-central bridge.** Selection and implementation α\* add **+0.37pp**, the opportunistic overlay **+0.37pp** and leverage at the expected 1.05× **−0.02 to +0.23pp**; explicit drags subtract **0.31–0.64pp**. Expected return comes out at **6.1–10.5%** (mixture 8.3%), and P(10-year TWR ≥ 10%) at **20–54%** (mixture 36%).
3. **Verdict by model.**
   - **Plan** only under BlackRock fee-adjusted CMAs (M2: 10.5%). BlackRock's workbook assumes top-quartile performance for private markets in its SAA illustrations (verifier 10), so its PE line may already embed selection.
   - **Stretch** under the JPM-anchored models (M1, M4, M5). The gap is 1.1–1.4pp. The probability that the *true* expected return reaches 10% is 0–16% at 1.05×, and 12–38% only at the 1.30× cap.
   - **Aspiration** under AQR and BlackRock "risk premia rise" (M3, M6). The gap is 3.2–3.9pp, and no amount of leverage closes it.
4. **No single lever closes a JPM-anchored gap within the evidence.** M1 break-evens: +4.7pp a year on all PE primaries, +12pp on co-investment, +15pp on secondaries, +10pp on hedge funds, a Sharpe ratio (SR) of 1.0 on the overlay at 1.5% volatility, or 1.42× leverage (above the cap). Each has a prior probability of 0.2% or less.
5. **Where risk budget buys P(10%).**
   - Leverage buys the most: +7.6pp at the cap in M1. But it is beta, it lifts volatility from 14.4% to 18.2%, and it destroys value in M6.
   - Next come the overlay (+3.4pp at its 90th percentile, P90, subject to the deflated-Sharpe gate) and PE manager selection plus fee terms (+3.3pp).
   - Hedge funds, co-investment and secondaries add about 1pp each.
   - Private Credit, Capital Solutions, long-only and physical-to-synthetic (P2S) add ≈0. Budget them for liquidity, carry or diversification.
6. **Drags are first-order.** They cost 0.31–0.64pp centrally and 0.14–1.23pp across cases, comparable to all evidence-based α\* combined.
7. **v8's +3.5pp does not survive.** In the new engine it falls to **+0.61pp** on the v8 book, **+0.35pp** on ADIC's book on the named path and **+0.47pp** ex ante. Overlay execution survives (+0.37–0.38pp), provided the deflated-Sharpe gate is passed. State protection survives as a small, mainly risk-reducing effect. Mean-reversion timing, α\* reallocation and the QDD filter do not survive as return sources.
8. **Payout.** At the mixture's 8.3%, real NAV is preserved only at a payout of ≈5.3%. P(10-year return ≥ 10.8%), the hurdle for a 7.5% payout, is 15–47%.

## 2. Formulation

**Mapping.** The allocation maps onto six CMA classes:
- PE-family 49.7% (PE funds, Secondaries, Co-investment, ½ Capital Solutions);
- direct lending (DL) 10.2% (Private Credit, ½ Capital Solutions);
- hedge funds 11.3%;
- ACWI 15.8% (long-only equity);
- Aggregate bonds 4.5%;
- cash 8.5% (Treasury).

**Bridge.** For model m, in arithmetic space:

$$m_m=w^\top a_m+\sum_j\omega_j\alpha^*_j+SR\,\sigma_O+(L-1)(a_{m,EQ}-r_{f,m}-s)-\sum_kD_{k,m}$$

$$\sigma_m^2=w^\top\Sigma w+2(L-1)(\Sigma w)_{EQ}+(L-1)^2\Sigma_{EQ,EQ}+\sigma_O^2,\qquad g_m=e^{\ln(1+m_m)-\frac12\ln(1+\sigma_m^2/(1+m_m)^2)}-1$$

**Terms.**
- $a_m$ is each provider's compound return plus JPM-2026's arithmetic-to-compound spread for that class.
- Σ uses JPM-2026 volatilities and correlations, Higham-repaired, for every model; this understates disagreement on risk (verifier 10-R8). For M5, Σ is stressed: volatilities ×1.15, correlations between risky assets moved halfway to 0.9, and stock–bond correlation set to +0.4.

**α\* is defined against the CMA's own benchmark.** Each α\* is per $ of sleeve ω_j and net of fees, measured against how that CMA line is built:
- JPM's PE and hedge-fund lines are median-manager returns, net of fees;
- BlackRock's lines are gross, haircut as in C1;
- AQR's buyout line is net of a 3.5% all-in fee.

This is the double-counting guard.

**Probabilities and break-evens.**
- The probability of an H-year return of at least x is $1-\Phi\big((\ln(1+x)-\ln(1+g))/\sqrt{\sigma_{\log}^2/H+\tau^2}\big)$.
- $\tau^2=\sum_j(\omega_j sd_j)^2+(sd_{SR}\sigma_O)^2$ is the uncertainty in the lever parameters, with sd = (P90 − P10)/2.563. It does not diversify over time. τ is 0.49pp if the levers are independent and 1.17pp if they are comonotone.
- **P(μ ≥ 10%)** uses τ alone, so it asks whether the *true* expected return is at least 10%.
- A lever's **break-even α\*** solves g_m = 10% with every other lever at its central value.

**Regression test.** On stream 10's stylized book the code reproduces verifier 10 exactly: 9.17% arithmetic, 13.08% volatility, 8.39% geometric, P(5y ≥ 10%) 39.1%, P(5y < 7%) 40.4%.

## 3. Beta: fee-consistent CMAs on the working book

| Model (as of) | PE | DL | HF | ACWI | Agg | Cash | Book beta (geo) | P(10y ≥ 10%) |
|---|---|---|---|---|---|---|---|---|
| M1 JPM 2027 (30 Sep 2026; 2026 values where silent) | 9.6 (median manager) | 7.7 | 6.7 (median manager) | 7.5 | 5.3 (global agg) | 3.1 | **8.33** | 34.8% |
| M2 BlackRock (30 Jun 2026), fee-adjusted | 15.89 − 3.5 | 9.31 − 2.0 (unlevered) | 9.29 − 2.5 | 9.02 | 4.88 | 3.67 | **9.97** | 49.7% |
| M3 AQR (31 Dec 2025), real + 2.4 | 6.6 (net of 3.5% fee) | 5.0 | 5.3 (JPM fill) | 6.6 | 4.9 | 3.7 | **6.28** | 19.5% |
| M4 JPM drought | = M1 | | | | | | **8.33** | 34.8% |
| M5 JPM stagflation | = M1, stressed Σ | | | | | | **8.38** | 37.4% |
| M6 BlackRock "global risk premia rise", fee-adjusted | 9.36 − 3.5 | 8.96 − 2.0 | 7.66 − 2.5 | 4.57 | 5.11 | 4.05 | **5.81** | 16.7% |

**Reading.** Beta alone gives P(5y ≥ 10%) of 24.7–49.8%. M4 and M5 share M1's means by construction (C1 anchors each model's compound returns to its CMA), so their structure enters through drags and dispersion. M5's higher P(10%) at the same median is the digital-option effect (L9) in miniature, which is why P(10%) is reported, never optimized.

**The contested beta is the PE premium.** Harris, Jenkinson and Kaplan (JOIM 14(3), 2016; Burgiss data to June 2014) find buyout beat public markets by ≈3–4% a year for pre-2006 vintages but roughly matched them for the (still maturing) post-2005 vintages. Gupta and Van Nieuwerburgh (NBER w26514) put average buyout risk-adjusted profit at ≈−18 to −21 cents per $1, with about a quarter of funds above +10 cents. The premium over ACWI runs from ≈0 (AQR) through +2.1pp (JPM) to +3.4pp (BlackRock, fee-adjusted). That disagreement belongs in model weights, not in α\*.

## 4. Lever priors (per $ of sleeve, net, pp a year)

| Lever (NAV share) | P10 / central / P90 | Evidence (dated) |
|---|---|---|
| PE primaries: selection + fee terms (29.4%) | −0.55 / **+0.75** / +2.05 (selection +0.25, terms +0.5) | Korteweg–Sorensen (JFE 2017): buyout interquartile spread 8.03pp, but per-fund signal-to-noise ≈0.15 (five top-quartile funds give 47% odds of top-quartile expected returns). Harris–Jenkinson–Kaplan–Stucke (NBER w28109, 2020; JCF 2023): post-2000 buyout has no persistence at fundraising beyond bottom-quartile avoidance; perfect foresight is worth +2–2.5% a year. Cavagnaro et al. (JF 2019): 1 s.d. of LP skill ≈1–2pp a year. Sensoy–Wang–Weisbach (JFE 2014): the endowment edge vanished after 1999. Begenau–Siriwardane (JF 2024): fee tiers within one fund differ by ≈91bp of management fee and ≈5.8pp of carry |
| Co-investment (10.2%) | −1.0 / **+1.0** / +2.5 | Braun–Jenkinson–Schemmerl (JFE 2020): no adverse selection (gross PME 1.76 vs 1.70, t = −0.55); at 0/20, portfolios beat funds only from ≈30 deals. Fang–Ivashina–Lerner (JFE 2015): capital-weighted IRR of −0.09% vs 16.8% on solo deals, concentrated in 2006–08 and in large deals. Lerner–Mao–Schoar–Zhang (JFE 2022): alternative vehicles trail the main funds |
| Secondaries (7.9%) | −0.5 / **+1.0** / +2.5 | Nadauld et al. (JFE 2019; 2006–14): buyers' PME 1.023 vs sellers' 0.976, ≈5pp a year; ≈3pp for funds aged 4–9; ≈0 for tail-ends [unverified: the G2 review traces these age splits to the 2016 WP, NBER w22404; not re-checked against the JFE tables]. Boyer et al. (JF 2023; figures from its 2021 version, NBER w28691): the all-ages transaction-priced buyout index averaged ≈14% a year over 2006–18 (22% for funds aged 4–9), with an insignificant CAPM alpha of about −2% a year, while cash-flow GPMEs are large and positive; the JF abstract attributes the gap to a discount-rate risk premium [corrected 2026-10-18: "≈20% a year over 2006–17" was the superseded 2018 WP (w25207) figure; JF full text not accessed]. H1-2026 pricing: LP portfolios at 87%, buyout at 91% of NAV (Jefferies). Day-one "discount capture" is an ASC 820 artifact (G2) |
| Capital Solutions (4.5%; beta ½ PE + ½ DL) | −1.5 / **0** / +1.5 | Erel–Flanagan–Weisbach (NBER w32278, Mar 2024): gross alpha ≈4.0–4.1%, roughly equal to fees; net ≈0. Böni–Manigart (FAJ 2022, Table 5): funds launched when ex-ante BB credit spreads are wider earn higher net multiples and beat IG and HY bond benchmarks (the IRR coefficient is positive but insignificant); a higher ex-ante TED spread (funding illiquidity) lowers that outperformance [corrected 2026-10-18] |
| Private Credit (7.9%) | −1.5 / **0** / +0.75 | Erel–Flanagan–Weisbach: net alpha −0.001% (SE 0.9%) with stock and bond factors, and +1.8% only against bond factors; net IRR 8.6% vs 13.9% gross. Credit stress is RED (Fitch default rate 6.3%, trailing twelve months to Aug 2026), so the skew is downward |
| Hedge-fund selection vs median (11.3%) | −1.5 / **0** / +1.5 | Ben-David–Birru–Rossi (RCFS 2026): investors kept ≈36¢ per $ of gross excess return. Dichev–Yu (JFE 2011): dollar-weighted returns trail by 3–7% a year. Aggarwal–Jorion (FAJ 2010): hidden survivorship bias above 5% a year. Upside: consultant-recommended funds earn +0.70% a year (Joenväärä et al. 2026, SSRN) |
| Long-only active (15.8%) | −0.6 / **−0.15** / +0.3 | Busse–Goyal–Wahal (JF 2010): 4,617 products, alpha ≈0. Barras–Scaillet–Wermers (JF 2010): ≈75% of funds have zero alpha. Goyal–Wahal (JF 2008). GC2: net IR −0.05 at ≈3% tracking error. AQR 2026's +0.5–1% for factor tilts comes from an interested party |
| P2S ($10bn, per $ converted) | −0.5 / **−0.1** / +0.2 | Fee and α saving of ≈0.15–0.4 against financing of 30bp (2021–23), 81bp (June-2026 roll) and 175bp (stress) (G5; GC2 D25). This is a liquidity lever |
| Opportunistic overlay (1.0–1.5% NAV vol) | SR −0.02 / **0.30** / 0.62 (+0.375pp at 1.25% vol) | Prior N(0.3, 0.25²) (C3 DQ18): a backtested SR of 1.0 over 8 years has posterior 0.50 and deflated Sharpe ratio (DSR) 0.86, failing the 0.95 gate. Harvey–Liu (JPM 2015): haircuts exceed 50% when SR < 0.4. AQR 2026: a single long/short theme earns SR 0.2–0.3 |
| Economic leverage (ACWI futures) | 1.00 / **1.05** / 1.30× | Cushion-monotone rule; the 1.30× cap (§4.5); financing at 30 / 81 / 175bp over cash |

**Base-rate check.** Central α\* plus the overlay is **+0.75pp a year**, between Ennis's −1.87pp a year for large endowments versus passive (12 years to June 2020) and NZ Super's +1.5pp a year over its Reference Portfolio (9.68% vs 8.19% over 20 years); CPP's five-year value-added was −C$63.7bn at FY2024. Evidence-central private α\* is ≈0.7pp per $ of private NAV, whereas Dimmock–Wang–Yang's calibration supports ~60% alternatives only at about 3% net alpha. ADIC's endowment model therefore rests on beta and liquidity management, not on demonstrated alpha.

## 5. Drags (pp of NAV a year)

| Drag | Parameterization | Central (M1) | Range | Basis |
|---|---|---|---|---|
| Convex sleeve | Premium of 0.15–0.50% of NAV × (1 − expected payoff / premium), with that ratio 0.70–0.40 | 0.09 | 0.05–0.30 | IC floor 0.15% (DQ22); Cboe PPUT ran −2.8% a year vs S&P 500 total return; G8 E1 carry is −45% of premium |
| Reserve top-up (DCR above the 8.5% Treasury) | 3–7% of NAV (+1pp in M4–M6) × (½ equity risk premium + ½ × 125bp) | 0.14 | 0.04–0.23 | §4.7; GC2 |
| Committed facilities | 5–20% of NAV (+5pp in drought) × 15–40bp standby | 0.03 | 0.01–0.10 | Berg–Saunders–Steffen (JF 2016; US credit lines, 1986–2011): undrawn all-in spread mean 31bp, median 25bp; investment-grade borrowers mostly pay facility fees (median 12.5bp); upfront fee median 27.5bp |
| Forgone vintages | Private share 0–6pp lower (+3pp in drought) × (PE − ACWI + 0.75 α\*) | 0.09 | 0–0.26 | §2.3(c); G1-R1 (cost a pacing cut as forgone net alpha once beta is replaced) |
| Forced-sale losses | 0.03–0.25pp (+0.10 in drought) | 0.06 | 0.03–0.35 | Stream 02: ≈0.64% of starting NAV over ten years [C] |
| **Total** | | **0.41** | Central 0.31–0.64 across models; 0.14–1.23 across cases | |

## 6. The bridge, by model (geometric, 10-year, pp)

| | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|
| CMA beta | 8.33 | 9.97 | 6.28 | 8.33 | 8.38 | 5.81 |
| + α\* (8 sleeves) | +0.37 | +0.37 | +0.37 | +0.37 | +0.37 | +0.37 |
| + Opportunistic overlay | +0.37 | +0.37 | +0.37 | +0.37 | +0.37 | +0.37 |
| + Leverage at 1.05× | +0.18 | +0.23 | +0.10 | +0.18 | +0.16 | −0.02 |
| − Drags | −0.41 | −0.47 | −0.31 | −0.64 | −0.43 | −0.47 |
| **= Evidence-central E[R]** | **8.84** | **10.47** | **6.82** | **8.61** | **8.86** | **6.06** |
| Gap to 10% | 1.16 | −0.47 | 3.18 | 1.39 | 1.14 | 3.94 |
| At the 1.30× cap | 9.66 | 11.53 | 7.24 | 9.42 | 9.58 | 5.88 |
| All levers at P90, 1.30×, low drags | 11.35 | 13.27 | 8.86 | 11.13 | 11.28 | 7.52 |
| All levers at P10, 1.00×, high drags | 6.50 | 8.03 | 4.63 | 6.27 | 6.52 | 3.97 |
| P(10y ≥ 10%), central (at 1.30×), % | 40.0 (47.6) | 54.1 (60.7) | 24.4 (31.5) | 38.0 (46.0) | 41.5 (47.5) | 19.6 (23.8) |
| P(μ ≥ 10%), %, at 1.05× / 1.30× (independent–comonotone levers) | 1–16 / 24–38 | 66–83 / 91–100 | 0 / 0–1 | 0–12 / 12–31 | 1–16 / 19–36 | 0 / 0 |
| **Verdict** | Stretch | Plan | Aspiration | Stretch | Stretch | Aspiration |

**Notes.**
- Rows may not sum exactly, because of rounding and the lognormal conversion.
- **Verdict rule [I]:**
  - Plan: P(μ ≥ 10%) ≥ 50% at central leverage.
  - Stretch: below that, but ≥ 10% at the cap.
  - Aspiration: below 10% even at the cap.
- The all-P90 row is a joint tail outcome, not a plan.
- Leverage uses 30bp futures financing. At the June-2026 roll (81bp) the 1.30× row falls by ≈0.16pp; at stress financing (175bp), by ≈0.44pp.
- Real-preserving payout hurdles over 10 years: P(≥ 7.9%, the 5% payout) is 34–72%; P(≥ 10.8%, 7.5%) is 15–47%; P(≥ 13.9%, 10%) is 5–23%.

## 7. IC table: break-even α\* and P(10%) by lever

M1 is the base, with [M4; M3] in brackets. M2 needs no lever.

| Lever | Central contribution (pp of NAV) | Break-even alone (per $ of sleeve) | P(prior ≥ break-even) | P(10y ≥ 10%) in M1, lever at 0 / central / P90 |
|---|---|---|---|---|
| PE primaries | +0.22 | +4.7 [5.4; 11.5] | <0.1% | 38.1 / 40.0 / 43.3 |
| Co-investment | +0.10 | +12.3 [14.5; 32.0] | <0.1% | 39.1 / 40.0 / 41.3 |
| Secondaries | +0.08 | +15.5 [18.4; 40.9] | <0.1% | 39.3 / 40.0 / 41.0 |
| Hedge-fund selection | 0.00 | +10.1 [12.2; 27.9] | <0.1% | 40.0 / 40.0 / 41.4 |
| Private Credit | 0.00 | +14.5 [17.4; 39.9] | <0.1% | 40.0 / 40.0 / 40.5 |
| Capital Solutions | 0.00 | +25.4 [30.4; 69.8] | <0.1% | 40.0 / 40.0 / 40.5 |
| Long-only active | −0.02 | +7.1 [8.5; 19.8] | <0.1% | 40.2 / 40.0 / 40.6 |
| P2S ($10bn) | −0.01 | +20.2 [24.2; 55.7] | <0.1% | 40.0 / 40.0 / 40.1 |
| Opportunistic overlay | +0.37 | SR 1.02 at 1.5% vol [1.17; 2.35] | 0.2% | 36.8 / 40.0 / 43.4 |
| Economic leverage | +0.18 | 1.42× [1.51×; unreachable] | beyond the 1.30× cap | 37.9 / 40.0 / 47.6 at 1.30× |

**Reading.**
1. Within the evidence, the M1 gap closes only through a joint outcome: leverage at the cap *and* above-median levers. Even then P(μ ≥ 10%) is only 24–38%.
2. Leverage buys the most P(10%), but it is beta. It lifts volatility from 14.4% to 18.2%, adds variation margin (VM) in exactly the states that bind (§2.3d), and destroys value in M6.
3. Only two alpha-type levers move P(10%) by more than 3pp at their P90: the overlay, and PE manager selection plus fee terms.
4. A group forecast implying break-even-scale α\* (for example v8's +280bp secondaries proposal) is a flag for Forward Belief Engine (FBE) debiasing, not an input to the bridge.

## 8. v8 scenario re-run, Shapley on CRN

**Set-up common to all runs.**
- Slide 6's annual means for Y1–Y3.
- Monthly Student-t(5) shocks with regime-specific volatilities and correlations.
- 50,000 paths.
- Exact Shapley values over 6 players (64 coalitions) on the same draws. Every Shapley standard error is ≤0.4bp.

**A, the v8 replica.**
- Book: equity 33 / fixed income 15 / hedge funds 10 / PE 22 / real assets 10 / private credit 10, with 55% liquid.
- Slide 7's positions are known in advance, and v8's own additive values are used for α\*, QDD, overlay and drag.
- It reproduces v8's static SAA: mean 7.14% (v8: 7.3), P(3y ≥ 10%) 31.1% (31.7), P10 −0.45% (−0.3).
- It reproduces v8's robust policy: 10.64% (10.8), 53.4% (54.6), +2.9% (+2.8). P(drawdown > 15%) on reported (lagged) private marks is 26.5% → 13.3% (v8: 23.9 → 14.3).
- Matching v8's +0.5 and +0.8 required scaling slide 7's hedge and amplification notionals to 62% and 48%.

**B–D, the new engine.**
- *Signals:* a non-anticipative 2-state filter; hedge when p(stress) > 0.6, release below 0.4; amplify after a trailing year ≤ −5% when p < 0.4.
- *Costs:* 3bp trading; 50bp financing on long futures.
- *α\*:* 3% of NAV reallocated a year; posterior α ~ N(0.75%, 1.5%); 1% liquidity charge when the liquid share is below 30%. *QDD:* bottom-quartile avoidance on new vintages. *Overlay:* SR ~ N(0.3, 0.25²) at 1.25% vol.
- *Drags:* a 90/72 put spread at 0.20% of NAV priced at 1.15× realized volatility, a 10%-of-NAV facility (30bp standby, 50% available in stress) and, on ADIC's book, a 5%-of-NAV reserve top-up.
- *Tier-1 filter:* economic exposure ≤ 1.30×; on ADIC's book, amplify only if the liquid share is ≥ 25% and cash ≥ 6%.
- **C** adds ADIC's book: a 7.5% payout, drought distributions (6 / 10 / 15 / 20% by regime), calls at 28% of unfunded, $11bn a year of commitments, and forced LP sales below a 4% cash floor at 25 / 15 / 10 / 8% discounts.
- **D** draws the regime path from a Markov chain, so the recovery is not assumed.

| Player (pp/yr, 3-yr mean) | v8 deck | A replica | B v8 book | C ADIC, named path | D ADIC, ex ante | Verdict |
|---|---|---|---|---|---|---|
| State/fragility protection | +0.5 | +0.50 | +0.12 | +0.11 | +0.16 | Survives, small; a risk tool |
| Mean-reversion timing | +0.8 | +0.80 | +0.14 | −0.04 | +0.02 | **Does not survive** |
| α\* reallocation | +0.8 | +0.80 | +0.04 | −0.01 | 0.00 | Not a 3-year return source |
| QDD filter | +0.5 | +0.50 | +0.02 | +0.02 | +0.02 | Not a return source |
| Overlay execution | +1.0 | +1.00 | +0.38 | +0.38 | +0.37 | Survives if the DSR gate passes |
| Liquidity/carry drag | −0.1 | −0.10 | −0.09 | −0.12 | −0.09 | Real cost; buys forced-sale avoidance |
| **Total uplift** | **+3.5** | **+3.50** | **+0.61** | **+0.35** | **+0.47** | |
| Mean, static → robust | 7.3 → 10.8 | 7.14 → 10.64 | 7.14 → 7.75 | 5.72 → 6.06 | 4.72 → 5.19 | |
| P(3y ≥ 10%), % | 31.7 → 54.6 | 31.1 → 53.4 | 31.1 → 34.6 | 21.1 → 20.9 | 19.8 → 19.9 | |
| P(drawdown > 15%), economic, % | 23.9 → 14.3 (reported basis) | 34.4 → 19.5 | 34.4 → 32.1 | 31.6 → 19.8 | 26.4 → 18.1 | |
| P(forced PE sale), % | — | — | — | 0 → 0 | 4.4 → 0.03 | |

**Single-feature ablations from A** (change in uplift when each new-engine feature is switched on alone): non-anticipative signals −1.03pp (state 0.50 → 0.12; mean reversion 0.80 → 0.16); evidence-based α\* and QDD −1.26; evidence-based overlay −0.62; costs −0.02; new drags +0.01. Their sum, −2.92, is close to the joint −2.89. **About 30% of v8's uplift was knowledge of the path, and ≈54% was unevidenced claims for α\*, QDD and the overlay.**

**On ADIC's book.**
- The Tier-1 gate blocked amplification in 55% of the months the signal wanted it on the named path (34% ex ante).
- Payouts and drought calls drained the liquid share to 17–19%, while the private share rose to 75–76%. This is the §2.3(c) ratchet, inside three years.

**State protection.** Its return is an upper bound, because the generator gives regimes sharply different means; real-time evidence on timing and volatility management is weak (Welch–Goyal, RFS 2008; Campbell–Thompson, RFS 2008, small gains only under restrictions; Asness–Ilmanen–Maloney, JOIM 2017; Cederburg et al., JFE 2020, failure in real time across 103 strategies; Brown et al., JFE 2021, PE commitment timing gives "modest gains, at best"). Its durable value is risk reduction: drawdown probability falls from 31.6% to 19.8% on the named path. Ex ante, together with the drag player, it also cuts forced sales from 4.4% to 0.03%.

**Do not count α\* twice.** The re-run's α\* player is the value of three years of *reallocation decisions*. The bridge's sleeve α\* (+0.37pp) is a standing property of the book.

## 9. Design implications

1. **`bridge/` engine and a WYNTB card.** Each quarter, per model: beta, levers, drags, the gap, P(μ ≥ 10%) as an independent–comonotone range, break-evens and the verdict. The IC votes on model weights, not on a single number.
2. **Lever priors in the forecast registry**, hierarchical, with source and as-of date. The FBE updates them from ADIC's realized net PME, direct alpha and fee terms by credibility weighting; Tier 2 uses posterior means and Tier 1 the posterior P10.
3. **A benchmark-definition field on every CMA line** (median manager or not; gross or net; levered or not). Add a double-count test, for example PE selection α\* ≤ 0.25pp in M2 unless evidence supports more.
4. **Drags as owned line items, in transfer-pricing (FTP) units.** The IC owns the convex budget; Corporate Finance owns reserve carry, standby fees and the forced-sale expectation; the Total Portfolio Committee (TPC) owns pacing. Each action card shows its drag delta next to its α\*.
5. **Attribution protocol (R13).** Retire v8's +3.5pp from IC materials and keep it only as `test_v8_replica` (tolerance ±0.05pp per row). Every attribution must be non-anticipative, ex ante across worlds, run on CRN with standard errors, costed and Tier-1 filtered. An **anticipation audit** reports each attribution's path-knowledge share.
6. **Lab gate (§5.4).** A component claim needs an ex-ante Shapley lower 95% bound of ≥5bp a year in at least two worlds. Under that gate, mean-reversion timing, α\* reallocation and QDD are NOT ESTABLISHED as return sources. QDD continues as a governance tool, scored on forecast skill.
7. **Risk budget.** Allocate active risk by evidence-weighted α\*/σ, net of liquidity charges. Leverage moves only through the cushion-monotone rule and is never sized to the gap; the gambling detector flags leverage at the cap while behind target.
8. **IC Deliberation Module (IDM).** A member's view on a lever (for example "co-investment α\* = 3%") enters as an FBE signal. The console shows the implied P(μ ≥ 10%) and the distance to break-even.
9. **Data to request from ADIC:** net PME and fee terms by fund; co-investment deal cash flows; secondary purchase discounts against realized outcomes; the overlay's full trial list, needed for the DSR.

## 10. Caveats

- These are prototype numbers on the synthetic allocation, and JPM risk is used for every model.
- Lever priors are judgment syntheses of the cited ranges, not meta-analytic estimates.
- The re-run uses a stylized regime generator, fixed commitments and a fixed 7.5% payout.
- Every [I-calc] figure must be replicated in the production engine before IC use.

## Sources (accessed 18 Oct 2026)

**CMAs**
- J.P. Morgan AM, 2027 LTCMA (as of 30 Sep 2026): https://am.jpmorgan.com/us/en/asset-management/institutional/insights/portfolio-insights/ltcma/
- J.P. Morgan AM, 2026 LTCMA matrix (via verifier 10).
- BlackRock CMA workbook (Aug 2026): https://www.blackrock.com/institutions/en-us/insights/charts/capital-market-assumptions
- AQR 2026 CMAs: https://www.aqr.com/Insights/Research/Alternative-Thinking/2026-Capital-Market-Assumptions-for-Major-Asset-Classes

**Private-equity skill, persistence and premium**
- Korteweg & Sorensen (2017): https://research-api.cbs.dk/ws/files/55394727/morten_soerensen_skill_and_luck_in_private_equity_performance_acceptedversion.pdf
- Harris, Jenkinson, Kaplan & Stucke, w28109: https://www.nber.org/system/files/working_papers/w28109/w28109.pdf
- Harris, Jenkinson & Kaplan (2016), JOIM 14(3): https://www.joim.com/how-do-private-equity-investments-perform-compared-to-public-equity/
- Gupta & Van Nieuwerburgh, w26514: https://www.nber.org/papers/w26514
- Cavagnaro et al.: https://www.nber.org/papers/w22547
- Sensoy, Wang & Weisbach: https://www.nber.org/papers/w18793
- Begenau & Siriwardane (2024), *JF* 79(2):1199–1247: https://doi.org/10.1111/jofi.13319 (summary: https://corpgov.law.harvard.edu/2024/05/10/fee-variation-in-private-equity/)

**Co-investment and secondaries**
- Braun, Jenkinson & Schemmerl: https://ora.ox.ac.uk/objects/uuid:f0b81a82-4ec1-44fc-abce-d5a64bfac082
- Fang, Ivashina & Lerner: https://www.nber.org/papers/w19299
- Lerner, Mao, Schoar & Zhang (2022), *JFE* 143(1):359–380: https://doi.org/10.1016/j.jfineco.2021.05.034 (WP: https://www.nber.org/papers/w24941)
- Nadauld, Sensoy, Vorkink & Weisbach (2019), "The liquidity cost of private equity investments: Evidence from secondary market transactions", *JFE* 132(3):158–181: https://doi.org/10.1016/j.jfineco.2018.11.007 (WP: https://www.nber.org/papers/w22404)
- Boyer, Nadauld, Vorkink & Weisbach (2023), "Discount-Rate Risk in Private Equity: Evidence from Secondary Market Transactions", *JF* 78(2):835–885: https://doi.org/10.1111/jofi.13202. Earlier versions: NBER w25207 (2018), https://www.nber.org/papers/w25207, and NBER w28691 (2021), https://www.nber.org/papers/w28691, the source of the §4 figures
- Jefferies (Jul 2026): https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf

**Private debt**
- Erel, Flanagan & Weisbach, w32278 (March 2024): https://www.nber.org/papers/w32278, DOI 10.3386/w32278. The §4 figures come from this version. An April 2026 draft revises most of them but keeps the conclusion.
- Böni & Manigart (2022), *FAJ* 78(4):121–144: https://doi.org/10.1080/0015198X.2022.2092384 (also https://rpc.cfainstitute.org/research/financial-analysts-journal/2022/private-debt-fund-returns-persistence-market-conditions)

**Hedge funds and long-only managers**
- Ben-David, Birru & Rossi (2026), *RCFS* 15(3):704–747: https://doi.org/10.1093/rcfs/cfag015 (WP: https://www.nber.org/papers/w27454)
- Aggarwal & Jorion: https://ideas.repec.org/a/taf/ufajxx/v66y2010i2p69-74.html
- Busse, Goyal & Wahal: https://ideas.repec.org/a/bla/jfinan/v65y2010i2p765-790.html
- Goyal & Wahal: https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1805-1847.html
- Dichev & Yu; Barras, Scaillet & Wermers; Joenväärä et al.: via the G5 verification log.

**Overlay and backtest deflation**
- Harvey & Liu (2015), *JPM* 42(1): https://doi.org/10.3905/jpm.2015.42.1.013 (PDF: https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF)
- Bailey & López de Prado (2014), *JPM* 40(5): https://doi.org/10.3905/jpm.2014.40.5.094 (PDF: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)

**Market timing and volatility management**
- Welch & Goyal (2008): https://academic.oup.com/rfs/article-abstract/21/4/1455/1565737
- Campbell & Thompson: https://nber.org/papers/w11468
- Asness, Ilmanen & Maloney: https://www.aqr.com/-/media/AQR/Documents/Insights/White-Papers/Market-Timing-Sin-a-Little.pdf
- Cederburg et al.: https://www.lehigh.edu/~xuy219/research/COWY.pdf
- Brown, Harris, Hu, Jenkinson, Kaplan & Robinson (2021), *JFE* 139(2):561–577: https://doi.org/10.1016/j.jfineco.2020.08.014 (WP: https://www.nber.org/papers/w26755)

**Facility fees, endowment model and peers**
- Berg, Saunders & Steffen (working-paper version): https://epub.ub.uni-muenchen.de/22795/1/489.pdf
- Dimmock, Wang & Yang: https://www.nber.org/papers/w25559
- Ennis (II, 1 Apr 2021): https://www.institutionalinvestor.com/article/2bswtbayp11p67nyfj3ls/portfolio/its-time-to-replace-the-grossly-inefficient-endowment-model-says-richard-ennis. The article reports "negative excess returns of 1.87 percent" for endowments above $1bn over the 12 years to June 2020 but does not name the paper. Probable primary source: Ennis, R. M. (2021). Failure of the Endowment Model. *JPM* 47(5):128–143. https://doi.org/10.3905/jpm.2021.1.217 [unverified: the −1.87% is not in that paper's abstract, and its full text was not read].
- NZ Super and CPP: via C3 and G8.

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2, the per-topic reviews (02, 09, G1, G2, G5, G7) and `research/literature/recheck/G3_cap_solutions.recheck.md`. No computed result in §1–§9 changes. One quoted source figure does: Boyer et al.'s index return in §4.

- §4, Secondaries row: Nadauld et al.'s age splits (≈3pp for ages 4–9, ≈0 for tail-ends) are tagged unverified. The G2 review traces them to the 2016 WP and they were not re-checked against the JFE tables. The headline 1.023 vs 0.976 (≈5pp) matches the published abstract.
- §4, Secondaries row: Boyer et al. is now cited to *JF* 78(2):835–885 (2023), which supersedes NBER w25207 (synthesis §2.4 item 6). "≈20% a year over 2006–17" was a 2018-WP figure. It now reads ≈14% a year over 2006–18 (22% for funds aged 4–9), with an insignificant CAPM alpha of about −2% a year. Those figures were read in the text of the 2021 version, NBER w28691 (printed pp. 26–27 and 31), and match the G2 dossier's correction. Added the JF abstract's discount-rate-risk framing. The JF full text was not accessed. The lever prior is unchanged.
- §4, Capital Solutions row: Böni–Manigart reworded to match their Table 5. Wider ex-ante BB spreads raise net multiples and PME against IG and HY bonds, but the IRR coefficient is insignificant. A higher ex-ante TED spread lowers outperformance (G3 re-check, ref 43). The lever prior is unchanged.
- §4, Capital Solutions and Private Credit rows: the Erel–Flanagan–Weisbach figures were checked against the March 2024 text of NBER w32278. They match: net alpha −0.001% (SE 0.9%) with both factors, 1.8% with bond factors only, gross IRR 13.9% against 8.6% net, and gross alpha ≈4.0–4.1%. Added DOI 10.3386/w32278 and a note on the April 2026 revision (G3 re-check, ref 42).
- §4 base-rate check: the Ennis −1.87% figure is confirmed in the cited II article (endowments above $1bn, 12 years to June 2020). Added the probable primary source, Ennis (2021), "Failure of the Endowment Model", *JPM* 47(5):128–143, DOI 10.3905/jpm.2021.1.217, marked unverified (synthesis §2.3, stream 02). Metadata from Crossref.
- Sources, Nadauld et al.: NBER w22404 link → *JFE* 132(3):158–181, with title and DOI 10.1016/j.jfineco.2018.11.007 (synthesis §2.3; G7 review). The seller PME was already the published 0.976.
- Sources, Boyer et al.: NBER w25207 link → *JF* 78(2):835–885, DOI 10.1111/jofi.13202 (Crossref), with w25207 and w28691 kept as earlier versions.
- Sources: version updates from the G1 review (synthesis §2.5). Lerner, Mao, Schoar & Zhang → *JFE* 143(1):359–380, DOI 10.1016/j.jfineco.2021.05.034; Brown et al. → *JFE* 139(2):561–577, DOI 10.1016/j.jfineco.2020.08.014; Begenau & Siriwardane → *JF* 79(2):1199–1247, DOI 10.1111/jofi.13319.
- Sources, Böni & Manigart: added *FAJ* 78(4):121–144 and DOI 10.1080/0015198X.2022.2092384 (G3 re-check).
- Sources, Ben-David, Birru & Rossi: added *RCFS* 15(3):704–747 and DOI 10.1093/rcfs/cfag015 (G5 review, A11).
- Sources: added issue numbers and DOIs for Harvey & Liu (2015), *JPM* 42(1), and Bailey & López de Prado (2014), *JPM* 40(5) (09 review).
