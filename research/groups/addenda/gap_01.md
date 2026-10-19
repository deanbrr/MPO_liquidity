# Groups gap 01 addendum: re-basing the group layer on T4′ and adding a group RECOVERY mode

- **Date:** 2026-10-18. **Closes:** groups critic gap 01. **Amends:** `01_GROUPS_SYNTHESIS.md` §1 (findings 3 and 6, decisions), §2.2, §2.4, §4.3, §4.4, §7.2, §9 (Q7, Q8); `research/00_SYNTHESIS.md` finding 5, §2.3(d), §4.9, §6.2 (replacement text in §5). Neither report is edited in place; this addendum governs where they differ.
- **SYNTHETIC – NOT ADIC DATA.** Every balance, flow, price and probability below comes from the context §1A working allocation, gap_02's stylised engine and design defaults.
- **Reproducibility.** `research/groups/addenda/gap_01_calcs/`: `g01_core.py` is a group-resolved replica of gap_02's `t1_engine.ladder` (`g01_verify_replica.py` asserts exact reproduction on six readings × eight policies, maximum difference 0.0). `g01_run.py` writes `g01_results.json`. `test_no_pinned_duals_groups.py` passes 18/18; gap_02's own test still passes 8/8.
- **Tags** as in the synthesis. All numbers here are [I-calc] unless tagged. Lever costs are [I]. Consensus returned no results this session because the account's monthly quota was exhausted.

---

## 0. Answer in brief

1. **One facility number.** Under T4′ = s\*(0.76) with gap_02's conventions, the do-nothing book needs **$13.9bn** of committed facilities, **$6.1bn** with the stage-triggered pacing rule, and **$0** with the owner band. The other two figures are retired:
   - $3–19bn came from C3's mild path, which is θ = 0 in the s\* family;
   - $23–49bn came from readings of literal T4, which is now a reverse stress only ($32.2bn at canonical conventions).
2. **θ\* is slightly understated.** Ten 50k-path replications of the M6 calibration give θ\* of 0.76–0.81. The pooled estimate on 500k paths is **0.79**, with a facility need of **$14.6bn**. gap_02's single seed was the lowest of the ten.
3. **The CFP stage still starts in Red, now on one indicator only.** SH_TP is 17 months, just under the 18-month Amber line, and 18 on the census v1.0 split. Adopting the stage-triggered pacing rule lifts it to 20 months (Amber); the band lifts it to 29 (Green). The other indicators are Green or Amber.
4. **No structural recovery on T4′.** Phase I over the group-tagged levers alone returns **u\* = 0**, without the revolver, the band or any fire sale. The current book still fails the hard row by **d₀ = $11.3bn**, so it is in *execution* recovery: its cards are priced on the plan, with `priced_on: restored_problem`.
5. **Prices depend on whether the revolver exists.**

   | | Value of $1 of month-24 headroom (5-year PV) | Group hurdles | 2018 buyout fund at 88% |
   |---|---|---|---|
   | Before the revolver (group levers only) | 24% | 3.0–5.0% a year | SELL |
   | Revolver signed | 1.1% | 0.13–0.97% a year | HOLD (reservation 90.7%) |

   The price stays at revolver carry across the whole SAA range. It jumps four- to five-fold (to 4.8–5.5%) only if θ\* ≥ 0.82, where the $15bn market capacity binds.
6. **Where penalty-pinned duals still appear.** The critic reading (a reverse stress) pins μ at the penalty tier: μ = 100, or 1,000 at ten times the tier. Every group's SELL card then fires, and the PE card's reservation price is *negative*. The extended test catches this, and it also refuses envelopes from a pinned solve or from any reverse stress.
7. **Drop the NAV facility.** A 20% pledge cap on $106bn of private NAV supports **$2.1bn at 10% LTV and $1.1bn at 5% stressed LTV**. That is 8–15% of the T4′ need, at **≈6×** the revolver's cost per credited dollar (7.0% vs 1.1% PV).

---

## 1. Group numbers under T4′ (item 1)

**Conventions (gap_02 §1.1).**
- Equity −37.6% at the vertex.
- PE, Secondaries and Co-investment distributions at 10.8% of drought rates.
- Calls at 1.38 × 28% of unfunded.
- 23 crisis months.
- Draws at 10% of opening fiscal-year NAV ($17.7bn in year 1).
- Private Credit cash at 10% and Capital Solutions at 7% of NAV a year.
- IG + cash: 8% elastic, 4% hard.
- The whole hedge-fund book noticed at t0, with 0.83 crisis pass-through.
- Revolver credited at 80% from month 2; NAV facility credited at 5% LTV on the pledge pool.
- $10bn of synthetic beta; new commitments $12bn a year split 60/10/10/10/10.

The engine uses gap_02's unfunded split. Census v1.0 moves G\* from $11.12bn to $10.85bn and SH_TP from 17 to 18 months.

### 1.1 §2.2: replace the "T4 named stress (s\*)" column

**12 months, $bn, do-nothing book** [I-calc; SYNTHETIC].

| Group | Distributions | Calls | **Net** | Net, 24 months |
|---|---|---|---|---|
| PE funds | 0.56 | 11.97 | **−11.42** | −20.91 |
| Secondaries | 0.18 | 2.66 | **−2.48** | −3.48 |
| Co-investment | 0.16 | 1.78 | **−1.62** | −3.03 |
| Capital Solutions | 0.52 | 0.69 | **−0.17** | −0.53 |
| Private Credit | 1.31 | 2.03 | **−0.73** | −0.76 |
| **Private book** | 2.72 | 19.14 | **−16.42** | −28.71 |
| Overlay, net | | | **−2.94** | −1.32 |
| CF opex | | | −0.18 | −0.35 |
| **Before payout** | | | **−19.54** | |
| Liquid-book funding, canonical draw | | | **37.2 (52% of $71bn)** | |
| Liquid-book funding at a 5 / 7.5 / 10% payout | | | 28.4 / 32.8 / 37.2 (40 / 46 / 52%) | |

*SYNTHETIC – NOT ADIC DATA.*

Overlay detail: VM −3.76, ΔIM −0.22, tail monetization +4.05, premium −0.35, opportunistic −2.66.

**Reading.**
- PE is 70% of the 12-month private drain and 73% of the 24-month drain.
- No private group is a net source.
- The overlay's net use falls from G7's ≈$6.0bn to $2.9bn, because canonical synthetic beta is $10bn, not $15bn.
- The retired column (private book −18.4, before payout −24.6) moves to the reverse-stress library.

### 1.2 §2.4: replace the T4 rows of the ladder table

| s\*(0.76), canonical conventions | SH_TP (months) | SH_TPF (months) | Minimum 24-month headroom ($bn) | Facility for 24 months ($bn) |
|---|---|---|---|---|
| Do nothing | 17 | 17 | −11.1 | **13.9** (SAA 13.9–15.1; pooled 14.6) |
| Stage-triggered pacing rule | 20 | 20 | −4.9 | 6.1 |
| Owner band | 29 | 29 | +2.3 | 0 |
| Rule + band | > 36 | > 36 | +8.6 | 0 |
| Revolver $13.9bn | 17 | 24 | 0.0 | — |
| Mix A: revolver $15bn, $6bn pacing + rule, reserve 14% | 24 | > 36 | +12.0 (+0.0 without the revolver) | — |
| Mix B: revolver $10bn, rule, band | > 36 | > 36 | +10.8 | — |
| NAV facility $2.1bn | 17 | 18 | −10.1 | 12.6 |
| *Reverse stress:* literal T4 / T4 as written / critic reading | 15 / 12 / 8 | — | −16.1 / −20.7 / −45.8 | 32.2 / 41.5 / 91.7 |

- **Red-event gate.** "No policy meets the ≤ 1% red-event gate" becomes: Mixes A and B certify ≤ 1% in M1–M5 (Clopper–Pearson bounds 0.98% and 0.79%; gap_02 §2.3). In the M6 class the floor is 2.4% with the band and 5.2–5.8% without it, against a 5% capacity level.
- **Liquidity at risk.** 12-month LaR99 is $28.4–38.3bn across M1–M6 (mean $31.2bn) on gap_02's engine at 50k paths. It replaces G7's $33.9bn.

### 1.3 CFP stage indicators at t0 (replaces "SH_TP under T4")

| Indicator | t0 value under T4′ | Stage |
|---|---|---|
| SH_TP under T4′ | 17 months (18 on census v1.0); 20 with the stage rule; 29 with the band | **Red** → Amber → Green |
| ADIC-LCR(30d), Basel-capped | 2.10× [C, GC2] | Green |
| Treasury ÷ NAV, unencumbered | 7.7%; 8.0% after a $0.56bn top-up | Amber → Green |
| Liquid share | 30.8% | Green |
| LaR99 ÷ CBC_TP(12m) | 0.65 (mean of M1–M6); 0.80 (M6) | Amber |

**Rule.** When the only Red indicator is a forward-looking one (SH_TP under a hypothetical stress), the stage triggers the Phase-II plan, not the Red event playbook (line draws, P2S and amber sales). That plan is: adopt the pacing rule, request the revolver, request the band. Event-Red comes only from the 30-day coverage, Treasury ÷ NAV, liquid-share and LaR indicators. Under this rule the book moves to Amber once the pacing rule is adopted and the 8% target is restored.

### 1.4 L4 group budgets on the binding horizon

$$\textstyle\sum_g B_{g,h}+B_{\mathrm{OVL},h}\le \mathrm{Pool}_h=\mathrm{CBC}_{TP}(h)+F(h)-D(h)-\mathrm{opex}(h)-\mathrm{fees}(h)-0.04\,W(h),\qquad h\in\{12,24\}$$

The 24-month row is hard. The 12-month row is reported but slack in every configuration.

**B_g (24 months / 12 months), $bn** [I-calc; SYNTHETIC].

| | Do nothing | Minimum T4′ plan: revolver $13.6bn + SMA sale $0.58bn | Mix A | Mix B |
|---|---|---|---|---|
| PE | 20.9 / 11.4 | 20.9 / 11.4 | 16.8 / 10.4 | 17.7 / 10.7 |
| Secondaries | 3.5 / 2.5 | 3.5 / 2.5 | 2.8 / 2.3 | 3.0 / 2.4 |
| Co-investment | 3.0 / 1.6 | 3.0 / 1.6 | 1.0 / 0.7 | 1.5 / 0.9 |
| Capital Solutions | 0.5 / 0.2 | 0.5 / 0.2 | −0.1 / 0.0 | 0.0 / 0.1 |
| Private Credit | 0.8 / 0.7 | 0.9 / 0.8 | 0.1 / 0.6 | 0.3 / 0.6 |
| Overlay | 1.3 / 2.9 | 1.3 / 2.9 | 1.3 / 2.9 | 1.3 / 2.9 |
| Pool | 18.9 / 25.4 | 30.1 / 36.7 | 33.9 / 40.9 | 40.2 / 41.9 |
| **Slack** | **−11.1** / +6.1 | 0.0 / +17.2 | +12.0 / +24.1 | +16.5 / +24.4 |

*SYNTHETIC – NOT ADIC DATA.*

---

## 2. Group envelopes in RECOVERY (item 2)

### 2.1 Phase I over group-tagged reversible levers

**Linearised H block.** The model has monthly T+P+F rows (h = 1…24) under s\*(θ\*) and the t0 T2 row:

$$\mathrm{hd}_h(x,q)=\mathrm{hd}^0_h+\textstyle\sum_\ell s_{\ell h}x_\ell+\sum_c s_{ch}q_c\ \ge -r_S,\qquad \sum_\ell \iota_\ell x_\ell+\sum_c b_cq_c\ \ge\ 0.08W_0-U_0\ (=\$0.56\text{bn})-r_{IG}$$

- Slopes s come from finite differences on the replica.
- q are SELL cards for PE, Secondaries, Co-investment and hedge-fund lots, at bid b and hold value 0.95.
- A shared-sleeve row requires $x_{sell}+x_{ro}\le\$5.6$bn, so run-off and SMA sales cannot use the same loans. EBA/GL/2023/06 ¶30 makes the same demand for mutually exclusive recovery options.

**Phase I** is gap_02's lexicographic minimum violation:
- $u^\*=\min u$ s.t. $\mathrm{hd}_h+u\ge0\ \forall h$, with x restricted to the levers available in the state and **q = 0**;
- then the same for IG.

**Lever catalogue (s\*(0.76)).** Cost is a 5-year PV per unit [I].

| Lever (owner) | Capacity | Month-24 relief per unit | Cost per $ of headroom |
|---|---|---|---|
| PE pacing, stage cut with protected 25% core (PE) | 75% of $7.2bn a year | 4.31 per full cut | 0.219 |
| Co-investment pause (Co-investment) | 100% of $1.2bn a year | 1.92 | 0.123 |
| Contingent budgets off (Secondaries / PC / CS) | 100% of $1.2bn a year each | 0.72 / 0.68 / 0.69 | 0.299 / 0.093 / 0.426 |
| SMA loan sales at 0.96 (PC; G6 T-regime 0.95–0.97) | $5.6bn sleeve | 0.74 per $ | 0.054 |
| SMA run-off at 6.5% a year (PC; G6 crisis rate 5–8%) | Same sleeve | 0.10 per $ | 0.048 |
| Syndication or sell-down at 0.90 (CS) | $2.0bn | 0.82 per $ | 0.243 |
| Hedge-fund notices (Public Markets) | Already in CBC_TP by convention | 0 | — |
| P2S (Public Markets proposes, Overlay executes) | $11bn | ≤ 0 (VM; no credit for the s\* rebound) | — (cheapest T2 source, 3.4% PV per $) |
| Opportunistic IM release (Overlay); tail monetization is already in the convention ($4.05bn by month 6) | $1.0bn | 0.96 per $ | 0.690 |
| Treasury top-up from DM equities (CF) | $10.6bn | 0.30 per $ | 0.249 |
| Committed revolver (CF) | $15bn (PIF precedent) | 0.80 per $ | **0.011** |
| Owner band (Board / owner) | Binary | 13.4 | 0.072 |

Lever cost bases [I]:
- **Pacing:** α\*·D per $ forgone (G8 E1 α\*).
- **Sales:** discount, plus 2% a year of carry where α\* > 0.
- **P2S:** 0.40–0.70% a year per $ freed (GC2).
- **Revolver and band:** gap_02.

**u\* by state** ($bn):

| Reading | R0x: group levers only | R0: + Treasury top-up | R1: + revolver (Mode B) | R2: + band (Mode H) |
|---|---|---|---|---|
| **T4′ = s\*(0.76)** | **0** | **0** | **0** | **0** |
| Literal T4 (reverse) | 1.65 | 0 | 0 | 0 |
| Critic reading (reverse) | 30.1 | 26.4 | 19.0 | 2.65 |

**IIS.** For the critic reading in R1 the irreducible infeasible subsystem is {T4′ row at month 24; every PE, Co-investment, Secondaries, PC and CS pacing lever at capacity; the SMA sleeve; CS syndication; Overlay IM; the Treasury top-up; the revolver at $15bn; band unavailable}. On T4′ the IIS is empty, so T4′ needs **no structural recovery**.

### 2.2 Execution deficit, glide path and allocation to groups

The current book fails the hard row by $d_0=\max(0,-\min_h\mathrm{hd}_h(x_0))=\$11.3$bn: nothing is signed, and the 8% top-up is not done. Recovery therefore has two parts:
- the structural part u\*, owned by CF/Board through the band request and Board sign-off (zero on T4′);
- the execution part, $d_0-u^\*$, delivered on a glide path.

gap_02's T_rec of 4 quarters (8 with Board approval) is longer than the 6 months over which EBA/GL/2023/06 accumulates liquidity recovery capacity. That is why the quarterly progress test matters.

$$g_t=d_0\,(1-t/T_{rec})^+,\quad T_{rec}=4\text{ quarters};\qquad e_t=d_0-g_t-R^{CF}_t;\qquad \varphi_{g,t}=\frac{\sum_{\ell\in\mathcal L_g}s_{\ell,24}\,x^{(t)}_\ell}{\sum_{\ell}s_{\ell,24}\,x^{(t)}_\ell}$$

- $R^{CF}_t$ is the relief from CF levers signed by t.
- $x^{(t)}$ is the least-cost solution at t over the *reversible* group levers, with no sales.
- $\varphi_{g,t}$ is group g's share of the interim deficit $e_t$.

**Group envelopes in RECOVERY.**
- The envelope is $B^{rec}_{g,t}=\Lambda_g(x^\*)+\varphi_{g,t}\,g_t$: the Phase-II envelope plus the group's share of the tolerated deficit.
- The tolerance covers the legacy book only. New deployment pays the terminal Phase-II price (§2.3).
- A group behind its delivery schedule loses envelope one for one, or buys it back at the dual.
- The quarterly progress test withdraws the glide path (gap_02 §4).

**Synthetic result** [I-calc]. Assume the revolver signs at t = 2 quarters [I].
- In Q1, groups must deliver $e_1$ = **$2.8bn**: a Co-investment pause of 82% of flow (**56%**) and PC run-off plus contingent budget off (**44%**). The interim price is 12.3% PV.
- From Q2 the revolver carries the deficit (φ_CF = 96%), and PC's $0.58bn SMA sale restores the 8% T2 target (φ_PC = 4%). The interim levers are then released.
- If the revolver never signed, reversible group levers alone would still close T4′ by T_rec. That takes every pacing lever and the Treasury top-up at capacity plus a partial opportunistic de-risk, at a marginal price of 69% PV. With SMA and CS sales admitted (R0), the price is 24%.

### 2.3 Duals, FTP and hurdles only from the Phase-II restored problem

**Phase II.** Maximize $\sum_c(b_c-h_c)q_c-\sum_\ell c_\ell x_\ell$ subject to hard rows relaxed by u\* only, with sales re-admitted. The duals are μ_h ≥ 0 and y_IG ≥ 0.

$$y_{cash}=\textstyle\sum_h\mu_h\kappa_h+y_{IG},\qquad p^\*_c=\dfrac{h_c-\sum_h\mu_h\rho_{ch}}{1+y_{cash}}\ \ (\text{SELL iff }b_c\ge p^\*_c)$$

$$\phi^{new}_g=\textstyle\sum_h\mu_h a_{gh}+y_{IG}\mathbb 1_{g=\text{Co}},\qquad \text{hurdle}_g=\phi^{new}_g/D_g,\qquad \text{FTP}^{hold}_g=\sum_h\mu_h\,\mathrm{NCO}_g(h)/(5\,\mathrm{NAV}_g)$$

- κ₂₄ = 0.825: a dollar of t0 cash buys only $0.83 of month-24 headroom, because the year-2 draw and the 4% floor are NAV-linked.
- ρ is group-specific relief beyond the proceeds. For PE, the buyer assumes 0.53 of unfunded per $ of NAV.
- a_g is the headroom consumed by $1 of new commitment.
- **Correction to §4.3.** "KKT caps μ at buffer carry" holds only once the row is restorable. The cap is then the cheapest *spare* lever per unit of headroom: $\sum_h\mu_hs_{\ell h}+y_{IG}\iota_\ell\le c_\ell$ for every lever below its cap. A Treasury top-up therefore caps μ at 25% PV per $ of headroom, not at 1.5% a year, because it relieves only 0.30 per $ (`test_kkt_cap_cheapest_spare_lever`).

### 2.4 Test extension

`test_no_pinned_duals_groups.py` checks seven things (18 tests in all):
1. Pinned group cards are caught. In the critic elastic solve, μ = M and scales with M; every group card says SELL with a reservation price below 2%; envelopes are refused.
2. In the restored problem, group duals, cards, envelopes, FTP, hurdles and glide shares are invariant to ten times the penalty tiers, with reservation prices above 60%.
3. Reverse stresses never price.
4. The KKT cap holds.
5. The Phase-I closed form holds, and the IIS names levers by owning group.
6. Envelopes add up to NCO(24), and glide shares sum to 1.
7. The interim path is feasible without sales.

---

## 3. t0 table: envelopes, charges and hurdles by group (item 3)

**Pricing states.**
- `priced_on: restored_problem` for both, because the current book fails T4′ by $11.3bn.
- Recovery-target hashes: R1 `684473e1b79d4f75`, R0 `95b61fae526726ba`.
- Brackets give the range across 10 SAA replications of θ\* (M6, 50k paths each; θ\* 0.76–0.81).

| Group | 24-month envelope B_g, $bn: R1 [SAA] / R0 | Pacing in stress, $bn a year: R1 / R0 | FTP on holdings, bp a year: R1 / R0 | Hurdle on new deployment, bp a year of α\*: R1 [SAA] / R0 [SAA] | Card or lever at t0: R1 / R0 |
|---|---|---|---|---|---|
| PE | 20.9 [20.9–21.4] / 17.6 | 7.2 / 1.8 | 9 / 164 | 14 [14–14] / 299 [299–303] | HOLD 90.7% / SELL 70.6% |
| Secondaries | 3.5 [3.5–3.6] / 3.4 | 1.2 / 1.2 | 6 / 119 | 20 [20–21] / 439 [439–445] | HOLD 90.9% / SELL 75.2% |
| Co-investment | 3.0 [3.0–3.1] / 0.9 | 1.2 / 0 | 4 / 25 | 96\* [96–97] / 498 [498–499] | HOLD 91.0% / HOLD 76.1% (bid 75%) |
| Capital Solutions | 0.53 [0.53–0.55] / 0.54 | 1.2 / 1.2 | 1.5 / 33 | 16 [16–16] / 349 [349–353] | — / syndicate $0.34bn |
| Private Credit | 0.85 [0.85–0.88] / 1.03 | 1.2 / 0 | 1.4 / 36 | 21 [21–21] / 450 [450–455] | SMA sale $0.58bn / $5.6bn |
| Public Markets | CBC_TP(24m) contribution 40.6 | — | — | — | HF secondary HOLD 91.9% / 93.6% |
| Overlay | 1.3 (net use) | — | — | — | IM release unused |
| CF | Revolver $13.6bn [13.6–14.8] | — | — | — | Glide share 96% / 0% |
| **Duals** | μ: R1 0.0113 [flat]; R0 0.243 [0.242–0.243]. y_IG: R1 0.033; R0 0 | | | | |

*SYNTHETIC – NOT ADIC DATA.*

\* Co-investment deploys cash at t0, so it also pays the T2 dual. In H's multi-period form, every group's calls pay the T2 dual of the quarter in which they land.

**What the table says.**
- **R1 prices are flat at revolver carry** (≈23bp a year per $ of month-24 headroom) while the revolver has spare capacity, which is true in all ten SAA replications (revolver $13.6–14.8bn).
- **θ = 0.82 is a signpost.** At that value the $15bn cap binds, and μ moves to SMA run-off and sales at 4.8–5.5% PV.
- **Under the certified mixes T4′ goes slack.** Mix B's headroom is +$8.6bn without its revolver; Mix A's is +$0.0bn without its revolver and +$12.0bn with it. The T4′ dual then falls to ≈0.
- **The binding price becomes T6's.** H must carry that price through its 12-quarter CVaR surrogate, under the same guard.
- **Until then, envelopes lead with quantities.** The pacing corridor comes from P: Mix A's base pacing gives PE $3.6bn a year, Mix B's $7.2bn. T4′ prices act as a floor (Baumol–Fabian).

---

## 4. IC decisions this quarter (item 4, replaces §1 decisions)

1. **Ratify T4′ = s\*(θ\*).**
   - Ratify the calibration rule (worst-model P99.6 on pooled replications: θ\* 0.76, pooled 0.79), with the canonical conventions as hashed fields.
   - Literal T4 becomes a reverse stress: a Board item only if SH_TPF < 24 months.
   - Settle the opening-reset draw convention.
   - Open the band conversation. The band is needed for the M6-class T6 capacity row, not for T4′.
2. **Request revolver indications; drop the NAV facility.**
   - Request indications for **$10–15bn of committed unsecured revolving capacity**: 3 + 2 years; at least 10 banks, none above 12.5%; covenants tested under s\*; a yearly test draw. At least $6.1bn should be firm.
   - **Precedent supports the floor more than the top.** PIF's $15bn facility (August 2024, 23 banks) is the largest precedent found. Mubadala's 2019 revolver was $2bn over five years with 28 arrangers [S: AidData]. Danantara's 2025 approach for up to $10bn reportedly closed at $1bn (three years, SOFR + 95bp) [S: press, snippet-level].
   - **The NAV facility fails the test.** It cannot be justified against a 20% pledge cap of private NAV:
     - the cap allows a $2.1bn facility at 10% LTV, of which only $1.1bn counts at the 5% stressed LTV, against a $13.9bn need;
     - it relieves T4′ by only $1.0bn;
     - it costs 7.0% vs 1.1% PV per credited dollar;
     - it forces paydowns in exactly the stress.
3. **Adopt the stage-triggered pacing rule now.** It moves SH_TP from 17 to 20 months and the facility need from $13.9bn to $6.1bn.
   - Set the PE corridor with its protected core.
   - Publish group envelopes, FTP and hurdles from Phase II with `priced_on` flags.
   - Until the revolver signs, run the Q1 glide path: Co-investment pause and PC run-off.
4. **Data requests.** Hedge-fund terms (τ) per lot, PC wrapper rights, and **SMA sale and run-off rights**: SMA run-off and sales are the cheapest group levers, at 4.8–5.4% PV per $ of headroom.
5. **Unchanged:** the point-in-time forecast archive.
6. **Unchanged:** the boundaries between Capital Solutions, Private Credit and Secondaries.

**Questions for the user (§9).**
- Q7 becomes "Will the IC ratify the T4′ calibration rule and the pooled θ\*?"
- Q8 becomes "Existing lines, covenant terms and appetite for a $10–15bn syndicated revolver?" The NAV-facility question is dropped.

---

## 5. Replacement text for `00_SYNTHESIS.md` (item 5)

**Finding 5 (replace).** *Survival in the joint stress binds; committed liquidity and the mandate clear it.*
- T4 as written is infeasible on the working book ($25–92bn across readings) and lies outside the six-model ensemble.
- Its replacement, T4′ = s\*(θ\*), equates the 24-month gap to the worst model's P99.6 (θ\* = 0.76; 0.79 on pooled replications). It needs $13.9bn of committed facilities ($14.6bn pooled), $6.1bn with the stage-triggered pacing rule, and none with an owner-agreed band [I-calc].
- The do-nothing book survives 17 months on Treasury and Public Markets (CFP Red); the pacing rule lifts this to 20 (Amber).
- Group levers alone can restore T4′ (Phase I u\* = 0), but price liquidity at 24% PV per $ of headroom. A signed revolver cuts the price to 1.1% [I-calc].
- The binding gate is T6: Mixes A and B certify ≤ 1% in M1–M5, and the stressed M6 class needs the band. A tail-option sleeve adds ≈1–3 months [I].

**§2.3(d) (replace the table and its lead-in).** "Survival on the canonical stress T4′ (gap_02 §1.1 conventions; groups gap_01 §1.2)." Then insert the §1.2 table above, then this note:

> The earlier $3–19bn came from C3's mild DB → SG → SG path. That path is θ = 0 in the s\* family (G\* = −$4.7bn at canonical conventions) and is kept only as the mild end of the family.

**§4.9 Tier 1A (replace three rows; add one line).**
- **T2.** IG + cash: 8% target (elastic, M^IG) and 4% hard, excluding encumbered IM, restored within 4 quarters of stress exit. P2S cash counts only net of stressed IM and P99 30-day VM.
- **T4′.** A 24-month canonical stress s\*(θ\*): equity −37.6%; PE-type distributions at 10.8% of drought rates; calls ×1.38; 23 crisis months; draws at 10% of opening fiscal-year NAV; vertex timing.
  - Facility credit by instrument and horizon: revolver 80% from month 2 with covenant headroom; NAV facility 5% LTV on a 20% pledge pool; uncommitted lines 0%.
  - Hedge funds: the whole book noticed at t0, 0.83 pass-through.
  - θ\* is set by the worst-model P99.6 on pooled SAA replications and recalibrated annually.
  - Hard row SH_TPF ≥ 24 months (H, F); appetite 36 months.
  - Literal T4 is a reverse stress.
- **T6.** Bands of 0.5 / 1 / 2% (appetite / tolerance / capacity) for the M1–M5 class and the mixture; 2.5 / 5% (tolerance / capacity) for M6-class structures. A capacity breach triggers RECOVERY.
- **Add line: recovery mode.**
  - Phase I over group-tagged reversible levers, with no sales of PE, Secondaries or Co-investment interests, returns u\* and the IIS.
  - λ, FTP, hurdles and envelopes come only from Phase II.
  - Every card and envelope carries `priced_on` and the recovery-target hash.
  - CI runs `test_no_pinned_duals` and its group extension.

**§6.2 Shadow IC (replace).**

Twelve seats are defined by mandate (main gap_01 §7). AI seats flag but never vote. With ≤ 40% of seats per model family, at least three families are needed (four is the target).

| Seat | Recovery-mode evidence slice added here |
|---|---|
| CIO | t0 envelope table; glide shares |
| CRO | T4′ headroom with its SAA band; T6 bands; the reverse-stress panel (literal T4, critic reading) |
| Treasurer / CF (owner's advocate) | Phase-I u\* and IIS; infeasibility-price panel (never on cards); revolver indications; recovery hash |
| Five private-group heads | Their catalogue rows and delivery against φ_g. They recuse on their own envelopes and are scored on delivery and total-portfolio regret, not group P&L |
| Public Markets head | Hedge-fund queue; P2S as the T2 source |
| Overlay head | Two briefs: convexity per unit of carry; deflated alpha and margin |
| Outside-View Forecaster | Base rates |
| Red Team | Must run the literal-T4 and critic reverse stresses |

A non-voting AI Validator rejects any pack in which a card or envelope lacks `priced_on` or derives from a reverse stress.

---

## 6. Design implications and limitations

1. **Pricing.** Price only from Phase II. Report the "cap-binding θ" (0.82) and the revolver's spare capacity as signposts.
2. **Group report §4.3–4.4.** Replace "KKT caps μ at buffer carry" with the spare-lever cap (§2.3). Derive envelopes from Phase II, with RECOVERY envelopes $\Lambda_g+\varphi_{g,t}g_t$.
3. **CFP.** Separate readiness-Red from event-Red (§1.3).
4. **Agentic layer.** Add a RECOVERY state that tracks delivery against the glide shares. The evaluator owns both tests.
5. **Open item.** The T6 surrogate dual in H, under the same guard.

**Limitations.**
- The block is a linearised single-scenario LP, and lever costs and caps are [I].
- P2S's T4′ slope is capped at zero.
- The SAA covers only the stress calibration, not tree sampling in H.
- The revolver's lead time (2 quarters) is assumed.
- The two census splits differ by $0.27bn in G\*.

---

## Sources (accessed 2026-10-18)

- EBA (19 Jul 2023). *Guidelines on overall recovery capacity in recovery planning*, EBA/GL/2023/06 (final report). Recovery capacity accumulates over 6 months for liquidity; ¶30 covers mutual exclusivity and interdependencies. https://www.dirittobancario.it/wp-content/uploads/2023/07/Final-Report-on-GLs-on-overall-recovery-capacity-in-recovery-planning.pdf
- AidData. Mubadala $2bn five-year RCF, 28 MLAs, committed 1 May 2019. https://china.aiddata.org/projects/98914
- Bloomberg (19 Nov 2025). *Indonesia's Danantara Taps Banks for $1 Billion Credit Line*. https://www.bloomberg.com/news/articles/2025-11-19/indonesia-s-danantara-taps-banks-for-1-billion-credit-line ; IDN Financials (20 Nov 2025). https://www.idnfinancials.com/news/58899/danantara-partners-with-four-global-banks-for-us1-bn-credit-facility. Read at snippet level; terms unconfirmed.
- Cited via gap_02:
  - Gulf News (28 Aug 2024). PIF $15bn RCF.
  - Nocedal & Wright (2006), Thm 17.3.
  - Boyd & Vandenberghe (2004), §11.4.
  - Chinneck (2008).
  - Solvency II Art. 138.
  - Clopper, C. J. & Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4), 404–413. DOI 10.1093/biomet/26.4.404. The method behind the red-event bounds in §1.2.
- Cited via the groups report: Baumol & Fabian (1964), *Management Science* 11(1).
- Internal: gap_02 and its calcs; `01_GROUPS_SYNTHESIS.md`; main gap_01; G6 dossier and verification log (SMA run-off 22–30 / 12–16 / 5–8%; uplift ≈$0.8–0.9bn); G7; G8 E1; GC2.

*SYNTHETIC – NOT ADIC DATA (all [I-calc] figures).*

---

## Citation corrections (2026-10-18)

*Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.5, which lists Clopper–Pearson among the methods named in the body without a reference entry; full metadata from `research/literature/G7_liquidity_ladder.lit.md`, confirmed on Crossref.*

- Sources: added a full entry for Clopper & Pearson (1934), *Biometrika* 26(4), 404–413, DOI 10.1093/biomet/26.4.404. §1.2 cited its bounds by name only.
- Checked, no change: this file quotes no statistic from the G4 barrier re-run (those quotes are in the main-report addendum `research/addenda/gap_01.md`). Its NAV-facility LTV caps are contractual caps, not monitored barriers (`G4_barrier_rerun/RESULTS.md` §2, row 7). Baumol & Fabian (1964) matches the G8 review's confirmed metadata.
