# RA gap 02: Real Assets engine reference spec, a sealed debt tape and a structural run on the census of record

**Date:** 2026-10-19 · **Companion to:** `research/groups/02_REAL_ASSETS_SYNTHESIS.md` v1.1 (§4.2, §4.5–4.7, §7.5, §9.1, §11) · **Status:** design-grade addendum; prototype on the ten-sleeve census (RA §11), with nothing fitted to ADIC data · **Computation:** `research/groups/addenda/ra_gap_02_calcs/` (`ra_common.py`, `ra_tape.py`, `ra_engine.py`, `ra_gates.py`, `ra_summarize.py`, results JSON, sealed tape; project venv, `python -B`).

> **SYNTHETIC-DATA NOTICE.** Every balance, tranche, path, cure, cash flow and LTV below is synthetic or [I-calc]. None of it is ADIC data, and none may be presented as such. Gate *targets* are public data. *SYNTHETIC – NOT ADIC DATA.*

Tags follow the RA report. Consensus was not used. The papers and series in §7 were fetched and read; FRED data were downloaded on 19 Oct 2026.

---

## 0. What changes

1. **Regime map.** Every RA parameter set now keys to the canonical (S, e, Z), plus an explicit financing window f ∈ {N, T, C} fitted on the Fed's Senior Loan Officer Opinion Survey (SLOOS), 1991–2026.
   - Retired: G11's private transition matrix, G14's regime base yields and GW/OD term sets, G10's private S chain, and RA12's undefined "N or T".
   - Today f₀ = N, but the RE transaction window starts in drought: the 10-year is 5.10%.
2. **Sealed tape.** 198 tranches on 188 assets carry the census's $17.43bn of debt.
   - 12.1% matures within 12 months and 28.0% within 24.
   - G15's uniform 17% a year is too high for ADIC-controlled debt (6.4% / 17.5%) and too low for closed-end value-add (VA) RE (34.5% / 53.8%).
   - V^mat is defined on each tranche's own collateral.
3. **Cash row.** Under the canonical generator, RA nets **−$0.15bn over 12 months (P5 −0.43) and −$0.28bn over 24 (P5 −0.91)**.
   - The steady-state rows nearly match G15: normal +0.30 against +0.40; drought −0.14 against −0.16.
   - **Structural T4′ nets −0.99 / −1.64** against G15's −1.32 / −2.46. With empirical calls instead of ×1.38 it nets **−0.28 / −0.55**, so the T4′ drain is mostly the call convention.
4. **Cures.** Under T4′, ADIC's own 24-month cure cash averages **$0.28bn (CVaR95 $0.54bn)**. That covers controlled assets, shortfalls and co-investment participation.
   - Including protective calls, CVaR95 is $0.70bn. The fund-level need averages $0.37bn (CVaR95 $0.71bn). G15 had $0.36bn direct plus up to $0.54bn at fund level.
   - The tail sits in GP-controlled closed-end VA RE, which needs about $0.23bn of protective calls over 24 months even in steady state. **GP behaviour drives it more than ϖ**: ϖ = 0 cuts T4′ CVaR95 to $0.35bn.
5. **LTV.** On the actual debt path, look-through LTV stays at 45–51% (peak P95 52–54%), because debt amortises, is swept and is cured down.
   - With debt fixed (G15's convention) it is **55% at q4 and q8 (P95 58% / 59.5%)**, and 57% / 58% if rates do not fall (P95 60% / 63%).
   - G15's 62% sits in that tail. Infrastructure barely falls when the 10-year rallies, and hedged ENR falls 8–9%, not 30%.
6. **Gates replace V-RA-CF.** None passes cleanly as specified.
   - **G-ODCE:** drawdowns pass; the trough lag fails at G13's λ = 0.75 (λ 0.55–0.70 pass).
   - **G-Jiang:** fails. Office negative equity is 34% against 44.6%, all CRE 8.6% against 14.3%; office still fails after a three-parameter recalibration.
   - **G-Chen:** the §4.5 capacity channel gives at most −0.019 per pp against −0.111. Rollover sales are behavioural, so a calibrated sponsor hazard is added.

---

## 1. Regime map (task 1)

### 1.1 Canonical states

The generator uses the gap_02 `t1_engine` rules, imported unmodified by groups gap_04, with Z₀ from gap_04 (GW 0.85).
- **Crisis:** entry probability min(0.95, 0.02·κ_Z). A DB entry starts a crisis with probability 0.85, which persists with probability 0.90 (0.75 outside DB).
- **RECV** is the four quarters after a crisis. **e_t** follows t1's M1 rows.
- **EXP vs LATE** is a two-state sub-chain [I] until the HSMM lands. The start is LATE.

**Finding: C3's P^Z_a cannot be embedded quarterly (or monthly).**
- Its principal fourth root has entries as low as −0.16.
- Clipping misses P^Z_a by 0.16, the linearisation by 0.28, and the best stochastic root (used here) by 0.09.
- So ARCHITECTURE §4.1's test "P_m^12 reproduces P^Z_a" will fail until P^Z_a is re-estimated monthly.
- The stationary crisis share is 16.9%, against t1's 14.3%.

### 1.2 Financing window

$$L_{t+1}=c+\phi L_t+b_{rec}\mathbb 1\{S_{t+1}=\text{CRIS}\}+b_y(y_{t+1}-y_{t-3})^++b_s(s_{t+1}-s_{t-3})+a_{Z}+\sigma\varepsilon,\qquad f=N\ (L<20),\ T\ (20\le L<50),\ C\ (L\ge50)$$

- **Data.** L is the net percentage of banks tightening CRE standards: FRED DRTSCREL to 2013Q3, spliced to SUBLPDRCSN [S].
- **OLS fit,** 1991Q1–2026Q3 (n = 143), with NBER recessions as the crisis proxy (SE in brackets):

  | c | φ | b_rec | b_y | b_s | σ |
  |---|---|---|---|---|---|
  | −0.04 (1.11) | 0.791 (0.039) | 7.8 (3.8) | 6.4 (1.8) | 6.6 (1.5) | 10.1 |

  The shock-type add-ons a_Z are [I].
- **History.** The thresholds give N 69% / T 19% / C 12% of quarters over 1990–2026. C covers 1990, 2007Q4–2009Q2, 2020Q2–Q4 and **2022Q4–2023Q4**. That last episode had no recession, which is why f must be a state of its own.
- **Today.** L₀ = −11.3 (2026Q3), so f₀ = N. Four quarters ahead, f is N/T/C in 66.5% / 28.6% / 4.9% of base paths, against a 14.8% crisis share.
- **Start-state correction.** Baa minus the 10-year is **1.44% (FRED, 15 Oct 2026), not RA §11's ≈2.0%**.

### 1.3 Mapping table

| RA parameter set | Keyed to | Values | Retired |
|---|---|---|---|
| G14 standards: LTV^max / DSCR^min / DY^min / availability / spread add-on | f = N / T / C | 62.5/57.5/52.5%; 1.25/1.35/1.40; 8.5/9.5/10.5%; 0.97/0.85/0.60; +0/75/175bp. Infrastructure: +10pp LTV, −0.05 DSCR, no DY test, +0.05 availability, −25bp. ENR: −5pp LTV (−10pp more if Z ∈ {SG, DB}), −0.10 DSCR | G14 base yields (rate level now y_t / SOFR_t); GW and OD term sets |
| GCC lending | max(f, floor(Z)); floor N/N/T/C/T/T for N/B/SG/DB/SS/GW | — | G14 "GW like C" vs G15 "normal": now T, with C as an axis |
| G11 state N/I/C/G | C if S = CRIS; else G if Z ∈ {GW, SS}; else I if LATE; else N | Risk-premium mean 0/0.20/1.00/0.40pp; power price 0/+0.15/−0.30/+0.35 (SG −0.15); jumps on crisis onset and GW entry | G11's 4×4 matrix; its rate, inflation, GDP and spread means; p^fail 0/1/15/3% (now emergent) |
| e^RE | F if f = C; D if f = T, or LATE with 10y > 4.75%; O if f = N, EXP and Baa < 1.6%; else N | Today D | G10's S chain; GW → D outside the GCC |
| Credit-availability premium on cap rates | f | 0/10/75bp | Keyed to S |
| P(extension given a gap): axis | f | 0, or G10's 0.35/0.50/0.50; −5pp if non-recourse, −7pp if DY < 8% (Glancy) | G14 0.55–0.70 |
| ADIC ℓ̄; sale discount d | f | 1/3/10%; 3/8/15% | Five G14 regime labels |
| Sponsor ℓ̄; rollover hazard | f | 5/10/20%; 0.111 per pp of positive rate gap × 1/0.6/0.2 | — |
| RA12 sales tier | Amber iff f ∈ {N, T} and S ≠ CRIS; red under T4′ | — | Undefined "N or T" |
| Asset dispersion σ_id | f | 8/15/28% a year; office ×1.5 (§5) | Flat 8% |

**What emerges.** The share of maturing infrastructure debt left unrefinanced (base, 5 years) is 2.3 / 1.2 / 8.8 / 2.9% in states N/I/C/G, against the retired p^fail of 0/1/15/3%. State C reaches 10.9% under T4′.

---

## 2. Sealed debt tape and V^mat (task 2)

### 2.1 Construction

Debt and GAV are held at ADIC share and rescaled exactly to the census.
- **RE maturities** are drawn as U{1…4/h} quarters, with h MBA's 2026 maturing share by holder: banks 21%, life companies 10%, CMBS/CLO 25%, credit companies 29%; all CRE 17% of $5.0tn [S].
- **VA bridge loans:** 30/25/45% of initial maturities in quarters 1–4 / 5–8 / 9–16. They carry one or two one-year extensions conditional on DSCR 1.10–1.25 at the cap strike, DY 7.0–8.5%, LTV ≤ 70%, a 2.5% paydown and a new cap.
- **Caps and fixed share.** 40% of capped VA loans have caps expiring before maturity, the CRED iQ share across 682 CRE-CLO loans [S]. Open-end debt is 79% fixed (Accordant: ">75% fixed", ≈4.5% cost [S]).
- **Infrastructure** follows G11's archetype gearings, scaled to the sleeve LTV. Project-finance debt is sculpted to the archetype DSCR, with lock-up at 1.15–1.20 and default at 1.05 (Arthur Cox: ≈1.10 / 1.05 [P]). Holdco debt is hedged 60–90%.
- **ENR reserve-based lending (RBL):** an advance of 0.55–0.65 on PV at 0.85 × strip, with semiannual and interim redeterminations [S: OCC, advance rates of 50–65% of risk-adjusted PV, deck "at a discount to the current NYMEX futures curve"].
- **GCC:** amortising bank loans on 18–25-year profiles, half swapped, with a 65% appraisal-LTV covenant. Two of the four carry corporate guarantees [I].
- **Development:** the data-centre JV has a construction facility at LTC 55% with a completion guarantee.
- **Seed rule,** fixed before any engine run: among 64 seeds, choose the one whose sleeve-level 12- and 24-month maturity shares deviate least from the generator's expectation. The result is seed 20261059, with a maximum deviation of 10.8pp.

| Sleeve | Tranches | Debt $bn | Maturing 12m / 24m | Floating / unhedged | Caps expiring early |
|---|---|---|---|---|---|
| RE open-end | 30 | 1.00 | 16% / 34% | 21% / 13% | All capped loans |
| **RE closed-end VA/opportunistic** | 42 | 3.90 | **35% / 54%** | 68% / 0% | 45% |
| RE JV/direct, global / GCC | 6 / 4 | 1.39 / 0.98 | 7/24%; 19/43% | 38/0%; 50/50% | 100%; — |
| RE co-investment | 4 | 1.20 | 0% / 35% | 58% / 0% | 50% |
| Infrastructure open-end / closed-end / direct | 42 / 40 / 15 | 2.00 / 3.06 / 2.44 | 11/21%; 4/19%; 0/6% | 13–20% / 10–13% | 78–82% |
| ENR closed-end / direct | 10 / 5 | 0.86 / 0.60 | 0/0%; 0/17% (RBL redetermined semiannually) | 75 / 38% unhedged | — |
| **Total** | **198** | **17.43** | **12.1% / 28.0%** (RE 21% / 43%) | | |

*SYNTHETIC – NOT ADIC DATA.*

### 2.2 §7.5 checks on controllable debt ($4.34bn on $9.08bn GAV, 22 tranches)

| Test | Result |
|---|---|
| Portfolio LTV | **47.8%: fails** the 45% target; passes the 55% hard limit |
| Maturing within 12 / 24 months | 6.4% / 17.5%: passes |
| Unhedged floating | 17.3%: passes |
| Hedged to maturity | **Fails:** 29.6% unhedged including caps that expire early |
| Single-asset LTV; development LTC | No breach on 21 assets; 55%: passes |
| P(covenant trigger within 12 months) ≤ 2% per loan | **Fails for 4 of 22 loans** (maximum 10.8%: three GCC bank loans and an airport holdco lock-up); 10 under T4′ (maximum 56%), adding global JV loans and a fixed-PPA project loan (`ra_cov_kpi_results.json`) |

T5 limit-1 recourse inputs: completion guarantees $0.51bn at maximum exposure, GCC corporate guarantees $0.53bn, carve-outs $0.02bn.

### 2.3 V^mat

$$V^{mat}_{i,T}=\omega_iV^*_{i,T},\qquad S_{i,T}=\begin{cases}\Big(D_{i,T}+D^{sib}_i-\min\big\{LTV^{max}_fV^{mat}_{i,T},\ \tfrac{NOI_{i,T}}{DSCR^{min}_f(r^{new}_T+0.01)},\ \tfrac{NOI_{i,T}}{DY^{min}_f}\big\}\Big)^+ & \text{lender available }(a=1)\\ D_{i,T} & a=0\end{cases}$$

- **V\*\_{i,T}** is the economic value of tranche i's own collateral at its (possibly extended) maturity, taken from that collateral's path: NOI(1+ĝ)/c for RE, structural V^A for infrastructure, PV at the strip for ENR (0.85 × strip for the RBL base).
- **D^sib** is debt on the same collateral. Pool lines use the pool. Maintenance covenants test appraisal V^A; refinancing tests V^mat.
- **G15's implicit V^mat** = (D^mat/LTV₀)(1 + ΔV^sleeve) is the special case where every loan sits at the sleeve LTV. Because E[(D − L^max)^+] ≥ (E[D] − E[L^max])^+, it understates gaps whenever the mean loan is inside capacity, which is the census case.
- **Seal.** SHA-256 is assets `79e9c5a0…` and tranches `6637ce25…`, with the full hashes in `ra_tape_manifest.json`. `load_tape()` refuses a broken seal.

---

## 3. Engine on the census (task 3)

The engine runs quarterly for 20 quarters from 2026Q4, on 5,000 canonical (M1) paths with common random numbers.
- **RE property layer (G10).**
  - Lease roll, sticky opex, and partial adjustment toward c\* = c₀ + 0.45Δy + 0.50Δs + Δliq(f) + Gulf(Z), with the Gulf term differenced from the initial state.
  - Each asset has its own cap rate and idiosyncratic path. Appraisals use the λ recalibrated in §5, with a one-quarter lag.
- **Infrastructure (G11).**
  - Revenue: Δln R = θ_kπ_{t−L_k}/4 + (1−θ_k)ē_k/4 + g_k/4 + β^g_k g_t/400 + ΔJ + m_kΔx^p.
  - Regulated assets: CF = ω·RAB, with the RAB CPI-indexed and ω reset every 20 quarters to r^real + ERP + ½β^q q + δ_op. Value is V^A = RAB[ωA(x,τ) + (x+δ_op)/x·(1+x)^−τ].
  - Other archetypes: V^A = CF^perm(1+g)A(r−g, n), excluding transitory jumps and 65% of power moves.
  - Debt service is sculpted, with DSCR lock-ups.
- **ENR (G12).** The curve follows C3 dynamics with Z-dependent expected paths.
  - Reserves are valued on a 12%-decline PDP profile, with a 3% net decline after maintenance drilling.
  - RBL base = advance × PV(0.85 × strip), cut 10pp in SG/DB, redetermined semiannually and on |Δln P| ≥ 0.20. Deficiencies are paid over two quarters.
- **§4.5 module at maturity.** Lender availability comes from a one-factor copula with ρ = 0.5. The resolution order:
  1. refinance if S = 0;
  2. contractual extension, if its tests pass;
  3. discretionary extension, with probability p_ext(f);
  4. forbearance, for up to two no-lender quarters at +200bp;
  5. cure: always for controlled assets under ϖ = 1; otherwise iff V − D − ℓ̄S > max(0, V(1−d) − D);
  6. sale;
  7. hand-back.

  Sponsor-owned RE instead sells with probability 0.111·(r^new − r^cur)⁺_pp, damped by f.
- **Fund-level module.** The distribution stop is stop = min(need, income), and the protective call is prot = min(need − stop, U). Any remainder is a NAV loss. Open-end funds sell assets at d(f), and the G10 queue machine runs on them.
- **Calls.** The groups CALL table keyed to e (0.39/0.29/0.28/0.30), or 0.28 × 1.38 under T4′. The structural m^C(e) is an axis.

---

## 4. Outputs and reconciliation (task 4)

| Run ($bn) | 12m: distributions / calls + dev / ADIC cures + protective calls | 12m net (P5, P95) | 24m net (P5, P95) | 24m cure CVaR95: ADIC; + protective | 24m fund need (CVaR95) | q8 LTV, economic (P95) | q8 LTV, debt fixed (P95) |
|---|---|---|---|---|---|---|---|
| Normal | 1.70 / 1.24 / 0.16 | +0.30 (0.21, 0.39) | +0.61 (0.41, 0.82) | 0.24; 0.48 | 0.31 (0.39) | 43.0 (44.0) | 48.4 (49.7) |
| Drought | 1.22 / 1.20 / 0.16 | −0.14 (−0.22, −0.05) | −0.25 (−0.43, −0.07) | 0.25; 0.50 | 0.32 (0.41) | 43.6 (44.7) | 48.4 (49.7) |
| **Base (canonical)** | 1.27 / 1.23 / 0.20 | **−0.15 (−0.43, +0.15)** | **−0.28 (−0.91, +0.35)** | **0.33; 0.62** | 0.37 (0.53) | 43.0 (46.0) | 48.4 (53.1) |
| Rate shock (2022-type) | 1.21 / 1.22 / 0.22 | −0.23 (−0.46, +0.01) | −0.51 (−0.94, −0.08) | 0.34; 0.71 | 0.45 (0.60) | 44.8 (47.1) | 50.9 (54.5) |
| Gulf war persists | 1.30 / 1.23 / 0.19 | −0.12 (−0.35, +0.16) | −0.27 (−0.78, +0.31) | 0.30; 0.62 | 0.38 (0.54) | 43.5 (45.9) | — |
| Supply glut | 1.20 / 1.23 / 0.22 | −0.26 (−0.47, +0.01) | −0.40 (−0.90, +0.15) | 0.30; 0.61 | 0.38 (0.52) | 43.1 (45.7) | — |
| **T4′ structural** | 0.81 / 1.61 / 0.19 | **−0.99 (−1.18, −0.82)** | **−1.64 (−1.97, −1.32)** | **0.54; 0.70** | 0.37 (0.71) | 44.7 (47.2) | **54.7 (59.5)** |
| T4′, rates flat | 0.79 / 1.61 / 0.20 | −1.02 | −1.72 (−2.05, −1.39) | 0.56; 0.73 | 0.42 (0.78) | 46.9 (49.4) | 58.3 (63.2) |
| T4′, structural calls | — | −0.28 | −0.55 (−0.89, −0.22) | 0.54; 0.71 | 0.37 | 46.4 | — |

*SYNTHETIC – NOT ADIC DATA.* "Debt fixed" means t0 debt over the market-value index.

**Ladder and outcomes.**
- Contractual maturities: $2.12bn within 12 months and $4.89bn within 24 (RE $1.79bn / $3.62bn; controllable $0.28bn / $0.76bn). G15 implied $2.96bn / $5.93bn.
- Re-maturities after extensions raise 24-month maturity events to $5.17bn (base) and $5.58bn (T4′).
- 5-year outcomes, base / T4′: refinance 51 / 49%, contractual extension 8 / 8%, discretionary extension 13 / 15%, cure 20 / 15%, sale 4 / 2.5%, hand-back 0.4 / 2.0%, forbearance 4 / 8%.

**Values under T4′ (q4 / q8).**
- RE funds: −18 to −20% / −27 to −29%.
- Global JV/direct: −10% / −13%.
- GCC: −30% / −5% (the scenario forces Z to DB, then N).
- Infrastructure: −2% to +2% (−6% to −9% with rates flat).
- ENR closed-end: −9% / −8%.

**Where T4′ cures sit (24 months).**
- ADIC-funded: GCC direct $0.15bn (mostly LTV-covenant paydowns), global JV/direct $0.07bn, ENR RBL $0.03bn, co-investment $0.06bn.
- Fund level: closed-end VA RE $0.20bn (protective calls 0.11, distribution stops 0.09); open-end RE $0.12bn.
- In the base run, closed-end VA RE carries ≈85% of the fund need. KBRA found ≈73% of 2021–22 CRE-CLO loans failing 2023 debt-yield standards [S-sec].
- Extensions defer cures: over 60 months ADIC cures reach $0.36bn in base and $0.45bn under T4′.

**Open-end queue.** On a full t0 redemption, the share paid by q4 / q8 (P50) is:
- RE: 31% / 59% in base (P5 26% at q4), and 18% / 29% under T4′;
- infrastructure: 54% / 100% in base, and 36% / 74% under T4′.

**Axes, 24 months** (base: ADIC CVaR95; + protective calls. T4′: net; ADIC CVaR95; + protective calls):

| Axis | Base | T4′ |
|---|---|---|
| Default | 0.33; 0.62 | −1.64; 0.54; 0.70 |
| No discretionary extension | 0.38; 0.72 | −1.73; 0.61; 0.85 |
| ϖ = 0 | 0.27; 0.58 | −1.58; 0.35; 0.53 |
| Fund module off | — | −1.40; 0.54; 0.54 |
| Co-investment not cured | — | −1.58; 0.46; 0.63 |
| As specified (λ 0.75, flat σ_id) | 0.25; 0.55 | −1.75; 0.42; 0.68 |
| GCC Gulf-war floor C | 0.35; 0.64 | — |

**Reconciliation with G15.**

| Item | G15 | Engine | Explained by |
|---|---|---|---|
| Normal / drought, 12m net | +0.40 / −0.16 | +0.30 / −0.14 | +$0.15bn of protective calls for cash-in refinancing of VA bridge loans at today's rates; calls plus development 0.08–0.09 lower; distributions −0.03 / +0.09 |
| T4′ net, 24m (12m) | −2.46 (−1.32) | −1.64 (−0.99) | Distributions +0.65 (+0.23): income 1.38 vs 1.10, and window-based exits and sales 0.50 vs 0.13. Calls −0.22 (−0.17): G15 also called direct unfunded at ×1.38. Cures +0.04 (+0.06) |
| T4′ cures, 24m | 0.36 direct (0.13 co-investment), plus ≤ 0.54 fund | ADIC 0.28 (CVaR95 0.54); fund 0.37 (CVaR95 0.71) | Controllable maturities 6% / 18%, not 17% a year; GP cures capped by unfunded and ruthless; extensions defer |
| Stressed LTV | 62% (GAV −20.7%) | 55% at q4 and q8 (P95 58% / 59.5%); 57% / 58% with rates flat (P95 60% / 63%) | GAV −9.6% (P5 −14.4%): RE agrees, but infrastructure ≈0 vs −12% and ENR −8% vs −30% |

---

## 5. Gates that replace V-RA-CF (task 4)

| Gate | Target and source | As specified | After stated recalibration |
|---|---|---|---|
| **G-ODCE.** 2021Q4–2026Q2 replay of the unchanged RE layer on FRED factors; ODCE mix, 25% leverage | Appraisal levered drawdown −18.8% ± 3pp (ODCE 2022Q3–2024Q2); true levered −25.7% ± 5pp (relevered REITs); trough lag 3 ± 1 quarters. Office shock fitted to Green Street −35% (one parameter) | −16.6% ✓; −22.4% ✓; lag 5 ✗. Green Street all-property −19.6% against −22% ✓ | λ_agg 0.60: −19.4% ✓, lag 3 ✓ (0.55–0.70 all pass) |
| **G-Jiang.** CMBS replica at 2023Q4: 39% of vintages 2013–15; initial LTV 61.0% / 54.4% | Current LTV 66.2 / 86.0%; > 80%: 29.0 / 56.0%; > 100%: **14.3 / 44.6%** (all / office; ± 4pp) | 67.2 ✓ / 92.8 ✗; 24.1 ✗ / 65.4 ✗; **8.6 ✗ / 34.3 ✗** | Fitted to 3 moments: pre-2022 drift +3.0% / +4.5% a year (non-office / office) and repricing dispersion σ 0.40. Held out: all > 80% 27.0% ✓; office > 80% 47.5% ✗; office > 100% 28.6% ✗ |
| **G-Chen.** `decide_maturity` on a seasoned CMBS-type population; LPM with quarter fixed effects | Slope −0.111 (SE 0.019), CI [−0.148, −0.074] | +0.002; **at most −0.019** (no equity injections, no planned sales) ✗ | Sponsor hazard 0.111 per pp: −0.110 ✓, by construction (calibration, not validation) |

- **G-ODCE.** The loadings reproduce 2022–24 levels without refitting. G13's core-RE smoothing is too sticky, as G10's α ≈ 0.5–0.6 implied. **Set λ_agg to 0.60 for core RE** (0.55 VA, 0.65 GCC).
- **G-Jiang.** The replay gives residential −25% and office −50% over 2013–23: the sector drifts, set to 2026 NOI, are too negative for 2013–21. A unimodal dispersion also cannot produce the office cross-section, where 44% of loans are below 80% LTV and 45% are above 100%. **The engine understates office negative-equity tails.**
  - The forward engine adopts regime dispersion: σ_id 8/15/28% (×1.5 for office), giving ≈0.40 over eight closed quarters. This raises T4′ CVaR95 from 0.42 to 0.54.
  - It still needs a sector trend factor and bimodal office dispersion.
- **G-Chen.** Seasoned loans rarely fail capacity, so the observed −11.1pp is behavioural. Rollover sales clear 12–13% below refinance appraisals [S].
  - The hazard applies only to sponsor-controlled RE, damped in T and C because the sample is 2003–19.
  - The only hold-out is the same paper's matched −0.128. An independent one is needed; Glancy's ≈20% stress-period office payoff is the candidate.

---

## 6. Design implications

1. **f_t joins the canonical state and the frozen initial state.** It is readable each quarter from the SLOOS. Ship the §1.3 table as configuration, and re-estimate P^Z_a monthly.
2. **The tape becomes a sealed first-class input.** Its schema is in `ra_tape_tranches_v1.csv`. It retires G15's MATURITY_PA and the implicit V^mat. The KPIs (12- and 24-month maturities, unhedged floating share, cure CVaR95) come from it.
3. **Calibrate GP behaviour before ϖ.** ϖ moves T4′ CVaR95 by $0.19bn, and extension policy moves it by $0.15bn (with protective calls). Request GP extend, cure and sale history for 2023–25 alongside the RA §14 tapes.
4. **Report T4′ under both call conventions:** −$1.64bn at ×1.38 against −$0.55bn structural. Keep the fund module on (it adds −$0.24bn), rather than assuming ×1.38 covers it.
5. **Report LTV on the actual debt path and with debt fixed.** Neither reaches 62% at P50 under the canonical crisis.
6. **Infrastructure stress is rate-path dependent:** about 0% when the 10-year rallies, −6 to −9% when it does not. Pair T4′ with a rates-flat variant.
7. **ENR stress is driven by the C3 curve's mean reversion.** Spot falls 42%, but the model strip falls only 23% in year 1 and 4% in year 3. Unhedged upstream falls 16% and the sleeve 8–9%. State this in the RA §9 loadings, or move to the ICE strip as planned.
8. **§7.5 on the tape.** The portfolio-LTV target, hedged-to-maturity and 2% covenant-trigger tests fail. Keep them as origination and monitoring tests under RA4's no-forced-sale protocol.
9. **BUILD_SPEC gates.** Keep G-ODCE, the measurement-matched G-Jiang and G-Chen (mechanism plus hazard). Add a Glancy payoff hold-out and RA's queue gate V-RE2. Every fitted parameter needs a named target and at least one held-out moment.
10. **Open items:** the sector trend factor and office bimodality; an independent hold-out for the rollover hazard; ADIC tapes, control rights and ϖ (RA §14, questions 3–5); a 10,000-path certification run.

---

## 7. Sources

- Jiang, Matvos, Piskorski & Seru, NBER w31970 (Dec 2023, rev. Dec 2024), Table 2 and Appendix A5. Sample: 35,253 CMBS loans ($825bn), indexed by Green Street MSA × type [S, read]. https://www.nber.org/papers/w31970
- Chen & Chen (9 Jun 2025), Tables 9–10: −0.111 (0.019), n = 12,990; matched −0.128 (0.024); sale discount −0.115 / −0.127 [S, read]. https://haas.berkeley.edu/wp-content/uploads/archive/The-Writing-on-the-MAturity-Wall.pdf
- Glancy, FEDS 2026-025 (May 2026) [S, read]:
  - about half of maturing loans were extended in 2023–25;
  - low-debt-yield loans were 7pp and non-recourse loans 5pp less likely to be extended;
  - office payoff was ≈20% in stress against > 40% pre-pandemic.

  https://www.federalreserve.gov/econres/feds/pretend-or-amend-on-evergreening-in-cre.htm
- OCC, *Comptroller's Handbook: Oil and Gas E&P Lending*, v2.2 (2018), pp. 11 and 24 [S, read]. https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/files/oil-gas-exploration-prod-lending/pub-ch-oil-and-gas.pdf
- Moody's, *Infrastructure & Project Finance: Defaults & Recoveries* (10 Jun 2020): workout recovery 77.9%, distressed-sale exits 49.5% [S, read]. https://ma.moodys.com/rs/961-KCJ-308/images/Default%20Reports%20-%20Infrastructure-Project-Finance-Global%20-%2010Jun20.pdf
- FRED, downloaded 19 Oct 2026: DRTSCREL, SUBLPDRCSN, DGS10, BAA10Y, CPIAUCSL, GDPC1 [S]. https://fred.stlouisfed.org/
- Green Street CPPI:
  - via Bisnow (8 Dec 2023, November data): −22% from the March-2022 peak, office −35% [S-sec]. https://www.bisnow.com/national/news/capital-markets/green-street-cre-prices-fell-another-3-but-may-well-have-hit-bottom-121991
  - Green Street (6 Feb 2024): −21% [S]. https://ca.greenstreet.com/commercial-property-price-index-january-2024/
- MBA (9 Feb 2026), CBRE Q2-2026 (3 Aug 2026), CRED iQ via Commercial Observer (27 Mar 2023), Accordant Q1-2026 (25 Jun 2026), and the NCREIF ODCE and Nareit series as computed in `G10_calcs` [S; verified in the G10, G14 and G15 logs].
- KBRA (20 Oct 2023), CRE CLO refinance research [S-sec]. https://www.businesswire.com/news/home/20231020398101/en/KBRA-Releases-Research-CRE-CLO-Refinance-Challenges-Ahead-for-2021-22-Vintage-Loans
- Arthur Cox (2021), project-finance covenants [P]. https://www.arthurcox.com/wp-content/uploads/2021/05/Article-11-Buckley.1.pdf
