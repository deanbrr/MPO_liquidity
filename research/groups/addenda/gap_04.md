# Gap 04 addendum (groups): the seven groups, Corporate Finance and the overlay simulated jointly

**Date:** 2026-10-18 · **Closes:** groups gap 04 (no joint simulation, self-disabling triggers, inconsistent lever pricing, an undefined 9-player Shapley) · **Amends:** groups synthesis §1 (findings 4, 6, 9), §2.4, §3.2–3.4, §4.3–4.7; gap_02 §2.1, §2.3 · **Status:** SYNTHETIC prototype on SYN-ADIC-177 (census v1.0); no ADIC data · **Code:** `research/groups/addenda/gap_04_calcs/`: `g04_engine.py` (imports gap_02's `t1_engine.py` unmodified), `g04_validate.py`, `g04_run.py` (stages `bridge`, `main`, `rh`, `shapley`, `pace`), `g04_shapley_summary.py`, with JSON outputs alongside. Runs use `python -I` and fixed seeds: 10,000 paths per model and policy, 20 quarters from October 2026, models M1–M6.

> **SYNTHETIC-DATA NOTICE.** Every figure here comes from synthetic data and gap_02's stylised proxy models M1–M6, not from ADIC. Tags follow the groups synthesis; [I-calc] marks figures computed here. Every table is *SYNTHETIC – NOT ADIC DATA*.

---

## 0. Answer in brief

1. **The interactions are simulated jointly on an anchored engine.**
   - With every extension off, the prototype reproduces gap_02's engine path for path: P(red) is 8.2 / 21.2 / 37.3% in M1 / M4 / M6.
   - Its per-path T4′ proxy reproduces gap_02's 17-month ladder exactly.
   - Engine changes move P(red) by a few points; the group playbooks move it most (§2).
2. **(a) PE is the cash sink early and a source late.**
   - Under Mix B, PE's net cash is negative in year 1 in 62–90% of paths, and in 10–21% by year 5, as census v1.0's young 2024–26 vintages season.
   - Capital Solutions and Private Credit are cash-positive in 95–97% of year-1 paths (§3).
3. **(b) On the do-nothing book the counter-cyclical mechanism is off, switched off by Tier 1 rather than by the stage.**
   - P(discount > 20% ∧ stage ≤ Amber ∧ Tier 1 green) is 0.1–1.2% of quarters, or 2–17% of paths over five years.
   - Under Mix A or Mix B the same trigger fires in 71–87% of paths.
4. **The franchise hedge needs committed liquidity, and it is modest.**
   - Current triggers add $0.62–0.81bn of five-year expected wealth under Mix A and $0.17–0.37bn under Mix B: 15–22¢ per dollar deployed, at no measurable P(red) cost. On the do-nothing book they add ≈0.
   - At θ = 0.75 the value falls to 0.5–9¢ per dollar.
5. **Monetization cannot fund the budget, and ring-fencing it backfires.**
   - Tail cash per crisis path is $1.5–1.8bn, under half of one year's $3.9bn budget.
   - Ring-fencing tail cash for deployment in Red raises P(red) by 0.2–0.9pp on the do-nothing book.
   - Gating on Tier 1 alone, in any stage but Black, adds $0.2–0.4bn over the current gate under Mix A (§4).
6. **(c) Liquidity is free at tolerance and priced at appetite.**
   - In a reduced H under Mix B, the liquidity rows are slack at Tier-1 tolerance.
   - At the CFP-Green appetite the T4′ dual is ≈0.05 per $ of headroom, and PE's net α* shrinks to ≈20bp per NAV-year.
   - Mix A is infeasible at that appetite (§5).
7. **(d) Nine-player Shapley values are defined and estimable.** Against the HOLD + plan-pacing baseline:
   - Corporate Finance and Public Markets each carry 26–30% of the red-event reduction;
   - the overlay playbook and TPA's beta rule earn 69–89% of the CE gain;
   - with 32 antithetic permutations, the worst-covered player's exact value is still covered 90–99% of the time (§6).
8. **gap_02's mixes, repriced.** Group PACE economics raise the M1 cost per forgone commitment dollar from 6.4¢ to 8.2¢; a PE dollar costs 8.6¢, of which κ^GP is 5.1¢.
   - The CE price of the 1% gate rises from 8bp to 11–21bp.
   - Mix A's premium rises from 62bp to 66–76bp; Mix B's from 21bp to 23–29bp.
   - The 10.5–11% citation is withdrawn and should be struck from gap_02 §2.1 (§7, §8).
9. **"Starts in Red" holds only under literal T4.**
   - Under T4′ on census v1.0, the do-nothing book is at the Red/Amber boundary (17–18 months), and Amber after one calm quarter.
   - Mix A starts Green. Mix B starts Green, or Amber in 47–66% of paths on the Treasury-share indicator.

## 1. The prototype

### 1.1 Cohort-level group engines [I unless tagged]

| Group | State | Quarterly dynamics; calibration |
|---|---|---|
| PE | 20 vintages: unfunded U_v; economic and reported NAV | **Calls:** $q(c(a)m^C_e)U_v$, with c = 20/25/30/35/40% by age [S: Ljungqvist–Richardson]. **Distributions:** $q(\min(0.95,(a/L)^2)m^D_e\phi)N_v$, with L = 15.05 fitted to a 20% normal rate at t0. **NAV return:** 1.1-beta plus α, GP and vintage effects, plus 3% a year of noise. **History:** commitments growing 12.6% a year to $11.6bn in 2026 reproduce unfunded $27.4bn and NAV $52bn |
| Secondaries | S1 funds, LP interests, CVs, contingent purchases | S1 calls 45% a year and distributes 25%·m^D; LP interests distribute 30%·m^D; CVs exit at 15%·m_X. A purchase at 1 − d acquires θ·(N^econ/N^rep)·N^ref, with θ = 0.92 (0.75 as a sensitivity) |
| Capital Solutions | Cash-pay (A, B, F) and PIK-capable (C–E) claims | PIK 15/30/50/70% (N/D/F/crisis); PD 1/2.5/5/7%; LGD 0.40/0.70, with crisis recovery ×0.7. NAV-loan repayments scale with PE distributions. New money: 13% coupon, 2% OID |
| Co-investment | 90 companies (EV, debt, age, GP, overlap flag) plus yearly cohorts | $\ln v'=\ln v+r_f+0.9(r_m-r_f)+(\alpha_A+\gamma_g+\eta_i)/4-\sigma^2/8+\sigma\varepsilon/2+J$. Write-off below 0.85 × debt, tested on quarter-end values with no discrete-monitoring correction [corrected 2026-10-18: a quarter-end test of a continuously monitored barrier misses mid-quarter breaches and so understates write-offs. The Broadie–Glasserman–Kou-equivalent test barrier is $0.85D\,e^{+0.5826\sigma_V\sqrt{0.25}}$, ≈ 0.92 × debt in calm quarters (σ_V ≈ 0.28 a year) and higher in crisis. Not re-run; see §9]. Weibull exits (k 1.447, η 7.70) × m_X. Recaps add 30% to debt. Effective N 46 |
| Private Credit | SMA, CEF, evergreen, BDC; DDTL | Coupon 9%; PIK 7–18%. PD 1.1% (×1.5 in drought, ×3 in crisis) with LGD 0.67, the FBE pair. CPR 6.5–32%. SMA principal is reinvested or run off. DDTL draws 15–60% a year |
| Overlay | 4 + 4 tranches of 12-month equity (90/70) and Brent (85/65 of the forward) put spreads; trend, carry, RV and short-vol families | Regime volatility with skew; MTM counts in NAV; families are factor exposures (gap_03 Level 1). Premium 0.20% of NAV a year |
| Public Markets, CF | gap_02 long-only, hedge-fund queue, waterfall, facilities, band | P2S keeps the exposure, so VM stays contingent |

### 1.2 Couplings simulated jointly

- **Co-investment flow (§4.7):**

  $$O_t=\theta\sum_{j=0}^{19}\tfrac14 d_{\lfloor j/4\rfloor}C^{PE}_{t-j}$$

  The flow runs on simulated PE commitments, with θ = 0.33 [S: Bain GPER 2026, GP level]. Deployment is $\min(\text{plan},aO_t)$ with a = 0.45.
- **Shared GP draws.** Each path draws γ_g ~ N(0, 3%) once for 70 PE GPs and 30 outside GPs. The PE book and the ≈70% of co-investments with a PE GP both use the draws. Company errors η ~ N(0, 2.4%) set the fund–co-investment correlation at ≈0.6.
- **Company overlap.**
  - 24% of companies also borrow from ADIC's Private Credit, which takes half of ADIC's look-through share of any recap debt.
  - Recap dividends and recap loans net at company level.
  - A write-off defaults the same company's PC loan on the same draw. Because the write-off test omits the discrete-monitoring shift (§1.1), these overlap defaults are understated until the next re-run [corrected 2026-10-18].
- **Desk quotes.** Triggers read the Secondaries desk's forecast $\hat d_t=d_t+0.03\epsilon$; deals execute at $d_t$.
- **P2S VM** lands in the same quarter as tail payoffs and hedge-fund gates.

### 1.3 Discount, stage and Tier 1

- **Discount:**

  $$d_t=\mathrm{clip}(\bar d_{e}+0.25DD_t+0.10\,\mathbb 1_{crisis}+0.03x_t,\ 0.02,\ 0.60)$$

  - $\bar d$ is 5 / 8 / 13 / 20% for O / N / D / F, and DD is the drawdown from the trailing four-quarter high.
  - Anchors: 87% in drought with no drawdown [S: Jefferies, Jul 2026]; 81% in 2022 [S: Jefferies]; 61% in H2-2008 [S: Cogent via Unquote, Jan 2009]; 54% in 2009 [S: Nadauld et al., NBER WP 22404 (2016) broker sample] [corrected 2026-10-18: was cited to the 2019 *JFE* article; the figure comes from the working paper and was not re-checked against the *JFE* tables].
  - d exceeds 20% in 99.7% of crisis quarters and 1.6–3.4% of calm ones.
- **CFP stage (groups §2.4).**
  - The stage is the worst of SH_TP under T4′ (gap_02's ladder evaluated on every path each quarter), ADIC-LCR(30d), Treasury/NAV and liquid share.
  - De-escalation needs two better readings.
  - It is computed gross and net of drawn facilities.
- **Tier 1 green:** usable IG + cash ≥ 8% ∧ LCR30 ≥ 1 ∧ SH_TPF ≥ 24 months, with facilities counted at 80%.

### 1.4 Players and the group-off baseline

There are nine players: PE, SEC, CS, CO, PM, PC, OVL, TPA and CF.

**Group-off baseline (HOLD + plan pacing).**
- $12bn a year committed 60/10/10/10/10, with co-investment at min(plan, accepted flow).
- Treasury is restored to 8% by long-only sales.
- The tail is held to expiry, the opportunistic book is static and synthetic beta stays at $10bn.
- There are no facilities, band, notices, P2S, run-off, contingent budgets or amber sales.
- Forced and emergency sales remain.

**"On" policies.**

| Player | Discretionary policy when on |
|---|---|
| Private groups | The mix's pacing through the stage corridor (1.0 / 0.375 / 0.25×) |
| SEC, CS | Contingent budgets |
| CS, PC | Amber sales; PC sells SMA loans at 0.99 / 0.96 / 0.85 |
| PC | Run-off from Amber |
| CO | Pause from Amber |
| PM | P2S and hedge-fund notices |
| OVL | Market-based monetization; opportunistic book halved in Red; L1 vega floor |
| TPA | Synthetic beta of $12.5 / 10 / 5 / 0bn by stage |
| CF | Facilities, reserve and band |

## 2. Bridge from gap_02's engine

P(red), %, 10k paths.

| Step | Do-nothing levers M1 / M4 / M6 | Mix B M1 / M4 / M6 |
|---|---|---|
| S0 gap_02 engine as published | 8.2 / 21.2 / 37.3 | 0.08 / 0.55 / 6.4 |
| S1 + October-2026 state (gap_04) | 6.1 / 16.2 / 31.7 | 0.07 / 0.51 / 6.0 |
| S2 + cohort engines | 6.6 / 14.4 / 30.9 | 0.04 / 0.39 / 5.5 |
| S3 + flow, shared GP and company draws | 6.4 / 14.2 / 30.7 | 0.04 / 0.36 / 5.4 |
| S4 + Level-1 overlay, static book | 6.5 / 14.8 / 33.0 | 0.04 / 0.25 / 4.8 |
| S5 + group playbooks | 2.0 / 7.0 / 17.3 | 0.00 / 0.00 / 0.12 |
| S6 + CFP stage drives policy | 1.6 / 6.3 / 14.5 | 0.00 / 0.00 / 0.09 |
| S7 + contingent budgets (current) | 1.6 / 6.3 / 14.5 | 0.00 / 0.00 / 0.09 |

- **S1:** the October-2026 state (a 5.7% year-1 draw, the Gulf-war posterior and the drought mix) is worth 2–6pp on the do-nothing book.
- **S5:** the playbooks (PC run-off, co-investment pause, overlay de-risking, TPA beta cut) take Mix B's M6 rate from 4.8% to 0.1%. They are assumed to execute at quarter-end readings without slippage.
- gap_02's 2.4% M6 floor is therefore a property of its playbook-free engine, not of the book.

## 3. (a) Per-group fans

Mix B, current triggers. Fans are P5 / P50 / P95 in $bn; DVA is return less the beta-matched funding basket, before FTP.

| Group | P(net cash < 0), years 1→5, M1 | Same, M6 | 5-year cash, M1 | NAV year 5, M1 | 5-year DVA, M1 |
|---|---|---|---|---|---|
| PE | 63 / 34 / 23 / 18 / 13% | 87 / 74 / 49 / 31 / 21% | −4.5 / 16.1 / 46.0 | 36 / 65 / 110 | −0.9 / 6.2 / 15.3 |
| Secondaries | 44 / 17 / 11 / 10 / 10% | 78 / 31 / 19 / 14 / 12% | 1.1 / 6.5 / 14.3 | 8 / 15 / 28 | 0.2 / 2.6 / 6.5 |
| Capital Solutions | 4 / 13 / 12 / 12 / 14% | 3 / 7 / 6 / 6 / 8% | 2.3 / 4.4 / 6.1 | 5 / 7 / 9 | −1.0 / 1.1 / 3.6 |
| Co-investment | 18 / 22 / 14 / 9 / 7% | 26 / 23 / 13 / 8 / 6% | 2.0 / 7.7 / 18.6 | 8 / 23 / 48 | −0.9 / 4.6 / 12.1 |
| Private Credit | 4 / 4 / 3 / 2 / 2% | 5 / 3 / 1 / 1 / 1% | 4.2 / 5.6 / 7.0 | 12 / 14 / 15 | −0.8 / 1.6 / 4.2 |
| Public Markets (proceeds) | 0 / 0 / 0 / 7 / 13% | 0 / 0 / 0 / 4 / 15% | 18.5 / 26.6 / 36.7 | 15 / 45 / 85 | −1.0 / 0.7 / 2.7 |
| Overlay | 37 / 40 / 41 / 41 / 40% | 43 / 44 / 48 / 48 / 49% | −4.2 / 1.9 / 7.7 | — | −4.3 / 1.8 / 7.6 |
| TPA (beta deviations) | 37 / 39 / 36 / 37 / 36% | 72 / 60 / 46 / 43 / 41% | −6.6 / 2.3 / 9.6 | — | −1.8 / 0.3 / 1.7 |
| CF (draws, fees) | 100% | 100% | −84 / −61 / −40 | — | — |

- **Year 1 is the squeeze.** PE and Secondaries are net users in 78–90% of year-1 paths in M4 and M6.
- **The group-off baseline fails over time.** Hedge funds are never redeemed and long-only runs out, so red events reach 24.8% by year 5 in M1 and 66% in M6.
- **PE cuts starve co-investment, as §4.7 asserts.** Accepted flow falls from $1.3bn a year to $0.4–0.5bn by year 5 under Mix A, and to $0.7–0.9bn under Mix B. Sustaining the book needs ≈$3bn a year [I-calc, G4].
- **Recap netting is small.** Recap dividends total $0.5–0.7bn over five years, 12% of it funded by ADIC's own credit.

## 4. (b) When the contingent-budget triggers fire, and what they are worth

### 4.1 Joint frequencies

Current triggers; ranges over M1–M6.

| Policy | P(trigger) per quarter | P(trigger) ever, 5 years | P(trigger │ crisis) | P(stage ≤ Amber │ d̂ > 20%) | P(Tier 1 │ d̂ > 20%) | Monetizations at stage ≤ Amber |
|---|---|---|---|---|---|---|
| Group-off baseline | 0.07–0.9% | 1–12% | 0.3–5% | 5–21% | 0.3–6% | — (held to expiry) |
| Do-nothing levers, playbooks on | 0.1–1.2% | 2–17% | 0.5–7% | 8–30% | 0.5–8% | 3–16% |
| Mix A | 9.3–11.3% | 73–87% | 29–54% | 42–64% | 86–99% | 27–52% |
| Mix B | 8.3–11.3% | 71–82% | 27–58% | 48–78% | 63–77% | 31–68% |

- **The discount itself is common.** d̂ exceeds 20% in 15–22% of quarters under every policy; 47–68% of paths contain a crisis.
- **Drawn-facility cash does not drive the result.** The net-of-debt stage changes the frequencies by less than 0.1pp.
- **Desk noise creates false triggers.** It adds 2–3pp of quarters with d̂ > 20% while d < 20%.

### 4.2 Realized value

ΔE[W̃] in $bn over five years, paired with "no budget" on common random numbers; ΔP(red) in pp.

| Gate | Do-nothing + playbooks | Mix A | Mix B |
|---|---|---|---|
| Current: d̂ > 20% ∧ Tier 1 ∧ stage ≤ Amber | +0.01–0.07; 0–0.02 | +0.62–0.81; 0 | +0.17–0.37; 0 |
| Tier 1 green, any stage but Black (IG + cash kept ≥ 8%) | identical to current | +0.82–1.16; ≤ 0.01 | +0.20–0.38; ≤ 0.01 |
| Ring-fence all tail cash, deploy in Red | +0.10–0.19; **+0.17–0.92** | +0.16–0.34; ≤ 0.01 | +0.12–0.35; ≤ 0.07 |
| Ring-fence + Tier 1 | −0.05 to +0.02; up to +0.32 | as ring-fence | as ring-fence |
| Ungated (d̂ > 20% only) | +0.86–1.26; **+1.5–6.4** | +0.94–1.69; ≤ 0.55 | +0.79–1.56; ≤ 0.77 |

- **Value per dollar deployed.**
  - At θ = 0.92: 15–24¢ under the current and Tier-1 gates, 12–27¢ across all gates.
  - At θ = 0.75: 0.5–9¢ under the current gate.
- **Deployment discounts** average 23–29% under the current gate and 31–36% under the ring-fence.

### 4.3 Reading and redesign

1. **On the do-nothing book the conjecture holds, but Tier 1 binds, not the stage.** Dropping the stage condition changes nothing. Tier 1 fails in 92–99.5% of hot quarters, mostly because T4′ survival with facilities is below 24 months.
2. **Mix A's facility and Mix B's band hold T4′ above 24 months, so the trigger fires in 27–58% of crisis quarters.**
3. **"Monetization funds contingent budgets" fails on size.**
   - Tail cash of $1.5–1.8bn per crisis path compares with a $1.77bn premium over five years.
   - Early monetization moves cash forward but does not raise it: $1.1–2.0bn against $1.2–2.1bn when held to expiry.
4. **Ring-fencing withdraws exactly the cash the waterfall needs.** ADIC becomes its own sidelined natural buyer, the fire-sale mechanism of Shleifer & Vishny (2011). Liquidity held to buy fire-sold assets pays only for institutions that come through the crisis with spare liquidity (Acharya, Shin & Yorulmazer 2011), and ADIC's spare liquidity is Tier-1 headroom. Cash-in-the-market pricing (Allen & Gale 1994) is why discounts peak when cash is scarcest.
5. **Redesign.**
   - *Gate:* d̂ > 20%, confirmed by a second reading or an external print ∧ Tier 1 green, in any stage but Black.
   - *Size:* min(budget, T4′ headroom less a buffer), re-testing T4′ after deployment.
   - *Funding:* general liquidity. Tail cash is credited to the Overlay, not ring-fenced.
   - *Do-nothing book:* without facilities or the band, the hedge does not exist.

## 5. (c) Envelopes and FTP charges from a reduced H

**Formulation.** A two-stage SAA program over year-1 envelopes, with 10 replications of 1,000 paths. Coefficients come from paired runs that add $1bn to each group's year-1 commitments.

$$\max_x\sum_g\sum_{j=1}^{4}m_j\bar v_gx_{g,j}\ \ \text{s.t.}\ \ \mathrm{CVaR}_{99}\Big(\sum_ga^{h,s}_gx_g-H^{h,s}\Big)\le0\ (h=12,24\text{m}),\ \ \mathrm{CVaR}_{95}\Big(-\sum_g\xi^s_gx_g\Big)\le R,\ \ \sum_gc_gx_g\le HR$$

- **Value** ($\bar v_g$): five-year excess return per $ plus α on the NAV left at T. Tranche weights m = 1 / 0.75 / 0.5 / 0.25 [I].
- **Coefficients:** $a$ is cash use per path per $; $H$ is path slack (usable cash − 4% floor + 95% of long-only + 80% of the undrawn revolver); $\xi$ is demeaned excess return.
- **Risk budget:** R is CVaR at the plan allocation.
- **T4′ row:** $c_g$ = s*(0.76) 24-month calls per $, 0.62 (co-investment 1.0). Headroom HR is $10.75bn (Mix B) at tolerance (TPF) and $8.52bn at the CFP-Green appetite (T+P only).
- **Bounds:** PE ≥ $1.8bn (protected sleeve).
- **FTP:** Σ_k y_k ∂row_k/∂x_g, divided by NAV-years per $.

Results for pooled M1–M5 under Mix B: medians, with min–max over replications.

| Group | Envelope at tolerance ($bn) | Envelope at appetite | FTP at tolerance (bp/NAV-yr) | FTP at appetite | α | Net α* at appetite |
|---|---|---|---|---|---|---|
| PE | 6.75 (6.75–7.06) | 6.75 | 136 (112–154) | 176 (172–188) | 196 | +20 |
| Secondaries | 2.40 (cap) | 1.80 | 71 (49–88) | 135 (130–144) | 300 | +165 |
| Capital Solutions | 1.80 | 1.80 | 138 (119–159) | 201 (195–213) | 270 | +69 |
| Co-investment | 0.99 (0.92–1.01) | 1.12 (1.03–1.13) | 306 (262–322) | 157 (149–162) | 364 | +207 |
| Private Credit | 2.11 (1.80–2.40) | 1.58 (1.56–1.73) | 94 (85–100) | 193 (188–199) | 259 | +65 |

- **At tolerance, liquidity is free.** The liquidity and T4′ duals are zero and FTP is a pure risk charge (λ_R = 0.36–0.42). This is an oversized buffer once the band exists, not free liquidity.
- **At appetite, liquidity binds.** The T4′ dual is 0.046–0.051 per $. The liquidity component of FTP is ≈100–185bp per NAV-year (PE ≈155; co-investment ≈100, because its cash stays invested about 4.7 years), and the risk component falls to ≈5–55bp.
- **PE's net α* is thin, and Mix A cannot meet the appetite.**
  - PE earns ≈20bp; in M3 (AQR) PE sits at the protected minimum.
  - Mix A is infeasible at appetite (headroom −$0.05bn) and goes to recovery mode (gap_02 §4).

## 6. (d) Group Shapley attribution with its Monte Carlo error

- **Value functions.** v(S) is evaluated on 10,000 common-random-number paths, with the players in S running their policy and the rest at the group-off baseline. The functions are P(red), the CE of W̃ (CRRA 3, $bn) and E[W̃].
- **Exact values.** All 2⁹ = 512 coalitions were evaluated per model (Mix B, current triggers). Σφ equals v(N) − v(∅) to 10⁻¹⁴.
- **Monte Carlo error.** Path error is the standard error across 20 blocks of 500 paths. Sampling error comes from antithetic permutations (Castro, Gómez & Tejada 2009; Mitchell et al. 2022).

| Player | ΔP(red), pp: M1 / M4 / M6 | ΔCE, $bn: M1 / M4 / M6 |
|---|---|---|
| CF (facilities, band, reserve) | −7.1 / −14.3 / −18.5 | +0.02 / +0.17 / +0.05 |
| Public Markets (P2S, notices) | −6.7 / −13.6 / −17.5 | −0.85 / −0.82 / −2.23 |
| PE (pacing corridor) | −3.6 / −7.6 / −9.7 | +0.79 / +1.55 / +2.95 |
| Co-investment (pause) | −1.9 / −3.6 / −4.3 | +0.31 / +0.71 / +1.57 |
| Private Credit (run-off, loan sales) | −1.8 / −3.5 / −4.3 | −0.03 / +0.14 / +0.40 |
| Capital Solutions | −1.1 / −2.3 / −2.7 | −0.06 / −0.08 / +0.11 |
| Secondaries | −0.8 / −1.6 / −2.0 | +0.17 / +0.26 / +0.53 |
| Overlay (monetization, de-risking) | −1.2 / −1.3 / −3.9 | +1.68 / +2.45 / +6.66 |
| TPA (beta rule) | −0.6 / −0.6 / −3.3 | +1.17 / +2.49 / +9.36 |
| **Total v(N) − v(∅)** | **−24.8 / −48.3 / −66.2** | **+3.2 / +6.9 / +19.4** |

Path SEs are 0.02–0.19pp on P(red) and $0.01–0.43bn on CE. *SYNTHETIC – NOT ADIC DATA.*

- **Insurance versus return.**
  - CF and Public Markets each remove 26–30% of red-event risk but add little or negative CE, because P2S and redemptions cost return.
  - The overlay playbook and the TPA beta rule earn 69–89% of the CE gain.
- **Stand-alone attribution is wrong by more than the effect.** The index Σ|φ_i − (v({i}) − v(∅))| / Σ|φ_i| is 0.7–1.5 on P(red) and 1.0–2.6 on CE, because liquidity levers substitute for one another.
- **The baseline's own error.** v(∅) carries ±0.40–0.50pp on P(red), ±$0.7–0.9bn on E[W̃] and ±$0.9–1.1bn on CE. Common random numbers shrink the error of the total change in E[W̃] to ±$0.06–0.13bn.
- **Sampling budget.**
  - With P = 32 antithetic permutations (258 coalition evaluations), the maximum RMSE is 0.22–0.51pp on P(red) and $0.08–0.10bn on CE. The band ±1.96 × (path ⊕ permutation SE) covers the exact value 90–99% of the time for the worst-covered player.
  - P = 16 covers 82–95%.
  - P = 64 needs 514 evaluations, more than the exact table.
  - So: compute exactly when evaluations are cheap (here 54 minutes on 22 cores for six models); sample with P ≥ 32 when each coalition needs an H re-solve.

## 7. Repricing gap_02's Mix A and Mix B with the group PACE cost

**Formula.** Cost per $ of plan commitment forgone:

$$c^{PACE}=\sum_gw_g(\alpha^*_g-\mathrm{FTP}_g)^+D^{>T}_g+w_{PE}\big[\kappa^{GP}+\theta a(\alpha^*_{co}-\mathrm{FTP}_{co})^+D_{co}\big]$$

- **Weights** w: plan shares 60/10/10/10/10.
- **NAV-years after 2031** ($D^{>T}$, per $ forgone, timing-weighted from the cohort engines): PE 4.2, Secondaries 2.6, Capital Solutions 3.6, co-investment 4.6, Private Credit 6.0.
- **κ^GP**, upper bound 5.1¢ per PE $ forgone: 92% at 4% (a buyout skip including later funds) plus 8% at 18% (elite VC) [I: G1 §6.5]. The central value of 2.3¢ deflates by ×1.3–2.6 and ×1.8–5.0 [C: G1 verifier R2].
- **Lost co-investment flow:** θa = 0.149 $ of co-investment per PE $ forgone.

**M1 example.** Per PE dollar forgone: net α* 1.35¢ + κ^GP 5.12¢ + lost flow 2.12¢ = 8.6¢. The blended figure is 8.2¢, against gap_02's 2 × (PE − liquid CMA) = 6.4¢. Across models the group cost is 5.6–12.3¢ (gross α*: 6.8–22.1¢), against gap_02's 2.2–9.6¢.

**Repricing.** gap_02's certified mixes were re-run (50k paths, M1–M5, bp of NAV a year); forgone commitments are $40.7bn (A) and $22.4bn (B). The CE price and the CE-best mix come from re-running gap_02's frontier on its 2,880-mix grid.

| | gap_02 | Net α*, κ^GP UB | Net α*, κ^GP central | Gross α* |
|---|---|---|---|---|
| Mix A pacing cost | 27.3 | 38.8 (tolerance FTP: 40.7) | 31.1 | 73.4 |
| Mix B pacing cost | 15.0 | 21.2 (22.5) | 17.0 | 40.8 |
| Mix A premium | 62.5 | 74.1 | 66.4 | 108.7 |
| Mix B premium | 21.3 | 27.5 | 23.2 | 47.0 |
| CE price of the 1% gate, no band / band | 8.0 / 8.0 | 19.1 / 16.1 | 11.4 / 11.4 | 53.7 / 36.6 |
| CE-best mix without gates | revolver $10bn, cut on | revolver $15bn, **no cut** | same | same |

*SYNTHETIC – NOT ADIC DATA.*

- **What does not change.** The ranking stands: Mix B costs about a third of Mix A's premium.
- **What changes.**
  - The gate costs 1.4–2.6× gap_02's price.
  - Mix A's CE gain over do-nothing falls from 32.7 to 21.1bp, and becomes a 13bp loss at gross α*.
  - The best ungated policy drops the stage-triggered pacing cut.
- **The 10.5–11% figure is withdrawn.** The "≈10.5–11% implied financing rate" is the cohort engine's growth G restated [C: G1 verifier R1]. It compares a risky IRR with a debt cost, and none of the repricing above uses it.

## 8. Design implications

1. **groups §2.4.**
   - "Starts in Red" becomes "Red under literal T4; Red/Amber boundary under T4′ (17–18 months); Amber after one calm quarter; Green under Mix A; Green or Amber under Mix B".
   - Compute stage indicators net of drawn facilities as well.
2. **groups §3.2, §4.5.** Adopt §4.3's gate; size budgets to T4′ headroom; state that the franchise hedge requires facilities or the band. Report its value with θ sensitivity: $0.2–1.2bn over five years at θ 0.92, ≈0–0.3bn at θ 0.75.
3. **groups §4.5–4.6.**
   - "Monetization funds contingent budgets" becomes "tail cash ≈$1.5–1.8bn per crisis path; supplementary; never ring-fenced".
   - "Tail hedge vs deployment: Real" becomes "Real only with Tier-1 headroom".
4. **groups §4.3.** Replace "exact Shapley values" with §6's protocol: nine players, the HOLD + plan-pacing baseline, exact when all 512 coalitions are affordable, otherwise antithetic sampling (P ≥ 32) with path and permutation errors reported.
5. **groups §4.4.** Publish FTP at both tolerance and appetite, with envelope ranges across replications. The IC states which Tier-1 level it prices.
6. **groups §4.7.** The flow equation now runs inside the engine. κ^GP includes lost flow, with acceptance a taken from the offer log.
7. **gap_02 §2.1.** Strike "2 × (PE − liquid CMA)… G1's implied financing rate is ≈10.5–11% [I, G1]". Insert $c^{PACE}$ and §7's table: the gate costs 11–21bp, Mix A 66–76bp, Mix B 23–29bp.
8. **gap_02 certification.** Re-certify on the integrated engine with playbook-slippage stresses. The playbooks set M6's floor.
9. **SYN-ADIC-177.** Version the PE vintage census, the co-investment census, GP links and overlap flags. ADIC's unfunded by vintage and its offer log replace them.

## 9. Limitations

- **Stylised dynamics.** All dynamics are [I] on gap_02's proxies.
- **Frequent, severe crises.** Crises occupy 12–18% of quarters and all reach a discount above 20%, which favours deployment.
- **Perfect execution.** Playbooks execute without slippage.
- **Thin calibration.** The discount rests on four prints; θ, κ^GP, acceptance a and overlap shares are assumptions.
- **A reduced H.** The H here is a one-year LP, not H itself.
- **Baseline-dependent Shapley.** Shapley shares depend on the baseline definition.
- **Uncorrected co-investment write-off barrier** [corrected 2026-10-18]. The engine writes off a company when EV < 0.85 × debt on quarter-end values, with no Broadie–Glasserman–Kou shift (`g04_engine.py`, line 978). Write-offs and the linked PC defaults are therefore understated. No figure here quotes a write-off rate: the bias reaches outputs only through lost recovery options and overlap defaults, chiefly in the Co-investment and Private Credit rows of §3. The fix is one line, writing off below $0.85\,e^{+0.5826\sigma_V/2}$ × debt (≈ 0.92 in calm quarters, higher in crisis). Apply it at the next re-run (`G4_barrier_rerun/RESULTS.md` §6.3).

## Sources

Accessed 2026-10-18. The Consensus quota was exhausted, so literature was verified on publisher and repository pages.

**Market data, via the verified corpus**
- Jefferies (Jul 2026), *Global Secondary Market Review*.
- Unquote (26 Jan 2009), Cogent data.
- Nadauld, T. D., Sensoy, B. A., Vorkink, K. & Weisbach, M. S. (2019). The liquidity cost of private equity investments: Evidence from secondary market transactions. *JFE* 132(3), 158–181. DOI 10.1016/j.jfineco.2018.11.007. The 2009 price in §1.3 comes from NBER WP 22404 (2016): https://www.nber.org/papers/w22404
- Bain & Company (2026), *Global Private Equity Report*.
- MSCI (Oct 2026), *Private Capital Benchmarks* Q2-2026.
- Ljungqvist & Richardson (2003), NBER w9454.
- Kaplan, S. N. & Strömberg, P. (2009). Leveraged Buyouts and Private Equity. *Journal of Economic Perspectives* 23(1), 121–146. DOI 10.1257/jep.23.1.121. Via G4.
- G1 dossier and verification log (R1, R2).

**Literature**
- Castro, J., Gómez, D. & Tejada, J. (2009). Polynomial calculation of the Shapley value based on sampling. *Computers & Operations Research* 36(5), 1726–1730. https://doi.org/10.1016/j.cor.2008.04.004
- Mitchell, R., Cooper, J., Frank, E. & Holmes, G. (2022). Sampling permutations for Shapley value estimation. *JMLR* 23(43), 1–46. https://www.jmlr.org/papers/v23/21-0439.html
- Acharya, V., Shin, H. S. & Yorulmazer, T. (2011). Crisis resolution and bank liquidity. *RFS* 24(6), 2166–2205; NBER w15567. https://www.nber.org/papers/w15567
- Shleifer, A. & Vishny, R. (2011). Fire sales in finance and macroeconomics. *JEP* 25(1), 29–48. https://www.nber.org/papers/w16642
- Allen, F. & Gale, D. (1994). Limited market participation and volatility of asset prices. *AER* 84(4), 933–955. https://ideas.repec.org/a/aea/aecrev/v84y1994i4p933-55.html
- Broadie, M., Glasserman, P. & Kou, S. (1997). A Continuity Correction for Discrete Barrier Options. *Mathematical Finance* 7(4), 325–349. DOI 10.1111/1467-9965.00035. Used in reverse (barrier moved toward the current value) so that a quarterly test mimics continuous monitoring (§1.1, §9).

**Internal**
- groups synthesis §2–§4.
- gap_02 (engine, grid, certification).
- gap_03 (Level-1 templates).
- gap_04, main (October-2026 state).
- G1, G2, G4 and G8 dossiers.
- `G4_barrier_rerun/RESULTS.md` §1 and §6.3 (direction of the BGK shift; the gap_04 write-off test).

---

## Citation corrections (2026-10-18)

*Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.2–2.4; the citation-integrity tables in `research/literature/G4_coinvest.lit.md` and `G2_secondaries_group.lit.md`; `research/groups/addenda/G4_barrier_rerun/RESULTS.md` §1 and §6.3. New metadata was confirmed on Crossref (api.crossref.org/works/<DOI>).*

- §1.1, Co-investment row: the write-off test (0.85 × debt on quarter-end values) is now stated as uncorrected for discrete monitoring, with its BGK-equivalent barrier (≈ 0.92 × debt in calm quarters). No figure changes: the engine was not re-run, and this file quotes no write-off statistic.
- §1.2, company overlap: notes that the linked PC defaults are understated until the barrier is corrected.
- §9: new limitation giving the one-line fix for the next re-run.
- §1.3, discount anchors: the 2009 price of 54% is re-attributed to Nadauld et al.'s NBER WP 22404 (2016), as the G2 dossier now does. It was cited to the 2019 *JFE* article.
- Sources, Nadauld et al. (2019): title, pages 158–181 and DOI 10.1016/j.jfineco.2018.11.007 added; WP 22404 named as the source of the 2009 figure.
- Sources, Kaplan & Strömberg (2009): title, *JEP* 23(1), 121–146 and DOI 10.1257/jep.23.1.121 added (the pages flagged as missing in G4).
- Sources: Broadie, Glasserman & Kou (1997) added, since §1.1 and §9 now cite it; `G4_barrier_rerun/RESULTS.md` added under Internal.
- Checked, no change: Ljungqvist & Richardson (2003) exists as NBER w9454, as cited here (§2.2 item 3). None of the re-check results for streams 10, 11, 13, 14 and G3 concerns a work cited in this file.
