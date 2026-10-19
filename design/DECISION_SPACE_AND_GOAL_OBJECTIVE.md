# Decision Space and Goal-Seeking Objective

*Specification for the slimmed five-component prototype (data and fusion · scenario tree · multi-period optimizer · simulator · reports and chat). 19 October 2026, v1.1: v1.0 revised after the adversarial quant review in `examples/mpo_v2/spec_review.md`; the changes are listed in "Review changes" at the end and tagged [RV-nn] where they occur. **SYNTHETIC – NOT ADIC DATA.** Every number below is a research default, a computation on synthetic inputs, or a working assumption, and is tagged.*

**Tags.**
- [R: file §] research or design source: SYN = `research/00_SYNTHESIS.md`; GRP = `research/groups/01_GROUPS_SYNTHESIS.md`; RA = `research/groups/02_REAL_ASSETS_SYNTHESIS.md`; LIT = `research/literature/00_LITERATURE_SYNTHESIS.md`; ARCH = `design/ARCHITECTURE.md`; TD = `examples/tree_demo/` (RESULTS.md, verify_finance.md).
- [S: author year] published source, as recorded in the research.
- [A] working assumption for the prototype, owned and swept.
- [I] derivation made in this spec, with a proof or a reproducible check.
- [RV-nn] a change made by the v1.1 review; nn is the issue number in `examples/mpo_v2/spec_review.md`.

---

## 0. Summary

**What changes from the tree demo.** The demo had 40 nodes, three aggregate books and a CRRA objective. It mostly sold liquid assets, drew the revolver and beat a simple rule by about $0.04bn [R: TD RESULTS §3]. Its 27 leaves made P(≥ 10%) identical across policies [R: TD verify_finance L5]. This spec replaces it on five fronts:
1. **Decisions** per holding across the eight groups and Corporate Finance: about 250 units and 60 instruments in one action ledger (§1–§2).
2. **Beliefs**: three marks fused per holding, then read against its bid and the liquidity price (§3).
3. **Objective**: the greatest probability of 10% a year without rewarding mean-preserving gambles, with the guards that stop cheaper gambles made load-bearing (§4) [RV-03].
4. **Tree and simulator**: 640 leaves (10 × 8 × 8), with at least one more branch than matched drivers at every branching, and probabilities certified on ≥ 10,000 fresh paths per world across K ≥ 8 independently generated synthetic books whose truth model differs from the belief model (§5) [RV-02, RV-06].
5. **Value-add**: nine baselines (B0–B4, P0 and archetypes A–C) including a risk-matched leverage control, value measured at equal tail risk, switch-off attribution by action family, and an explicit t0 change list (§6) [RV-04].

This document details `design/SLIM_ARCHITECTURE.md` §3, and §4.3 reconciles the two.

**Five findings that shape the design.**
1. **bPOE is degenerate for a stretch goal.** Under research-central assumptions the expected 5-year outcome is below the goal: the mixture's 8.3% geometric return is ≈9.4% arithmetic at 14.4% log volatility [R: SYN §4.12]. The buffered probability of missing then equals 1 for every policy, and by Jensen no concave lower bound on P(goal) can be positive (§4.2) [I].
2. **The main objective repairs this, but the guards carry the safety.** The Goal-Buffered Objective (GBO) is bPOE with a capped buffer.
   - When the goal is reachable on average, it is exactly bPOE.
   - When the goal is a stretch, it maximizes expected wealth inside the IC's tail limits, which is P(goal)-optimal at those limits for location–scale outcomes.
   - It never rewards a mean-preserving spread. In a synthetic check a pure gamble raised P(goal) from 52.6% to 54.3% while bPOE worsened [I].
   - It is still a linear hinge, the shortfall class that can reproduce probability maximization [R: LIT §4.7]. In a complete synthetic market its optimum is all-or-nothing, with wealth at zero in 13–26% of states (§4.2) [I-calc]. So the multi-level depth guard, the red-event row and the cushion caps (§4.6–§4.7) are load-bearing, not optional [RV-03].
3. **In the stretch case the tail limit is the decision.** Above the mean, P(goal) is bought with tail risk or with drift, so the IC picks a point on a frontier of P(goal) against tail and red-event risk (§4.8).
4. **Value must come from drift that adds no tail risk**: belief-versus-bid selection, avoided liquidity costs, counter-cyclical ADDs, cushion-gated leverage. Research priors suggest +0.3 to +1.0pp a year, ≈+2 to +6pp of 5-year P(goal): hypotheses, not promises (§6.5) [I, from R: SYN §4.12]. Value is therefore measured *at equal tail risk*, against a risk-matched leverage control. Beta bought with the tail budget is reported as risk taken, not as optimizer value: in the bridge model, 1.15× beta alone adds ≈+3.2pp of P(goal) for 0.05·W₀ of worst-decile wealth [I-calc] [RV-04].
5. **Probabilities come only from out-of-sample runs on a truth the beliefs did not generate.** The tree decides; the simulator certifies the root decision plus a recourse rule on fresh paths. The sealed truth comes from a different model than the fusion assumes, is replicated over K ≥ 8 synthetic books, and is checked against a null-information placebo (§5.5) [RV-02].

---

## 1. Conventions and lens algebra

### 1.1 Units and symbols

- **Units and clock.** Solvers use W₀ = $177bn; reports use $bn. Decisions are annual at t = 0, 1, 2; fans run t = 3–5 (3–10 in the 10-year sensitivity); the simulator steps quarterly. **Fan years t = 3, 4, 5 are constraint nodes**: every hard row that holds "at every node" holds there too [RV-07].
- **Indices.** Unit i (a holding, or a cohort of small ones) in group g(i); cohort k(i) (group × belief tercile × liquidity class, ≈40); nodes n, children c ≻ n, leaves ℓ with probability p_ℓ.
- **Stocks.** V economic NAV; N reported NAV (it sets draws, bids and LTV); θ = V/N, path-dependent (§5.1); U unfunded; C unencumbered Treasury cash and IG; E economic exposure (delta-adjusted, including synthetic and TRS exposure); W NAV; W̃ distribution-inclusive wealth (§4.1).
- **Debt and financing claims [RV-12].** B = B^rec + B^sec + B^sf + B^syn: recourse debt (revolver, term, repo); secured and asset-level debt (NAV facility, back-leverage, CFO notes, holdco PIK, RA asset debt, unit loans); seller financing (deferred payables, preferred equity's claim); and the financing embedded in derivatives (notional minus posted margin, for futures, TRS and P2S). Limits use the measure each names (H5's recourse cap uses B^rec only); the lens test R1 uses total B.
- **Prices.** μ̂ fused forward return; h hurdle; ℓ per-year liquidity premium from the cash rows' duals [R: ARCH §5.6]; π^G goal kernel (§4.3); κ^G the goal-tail risk charge read from the LP's duals (§3.4); κ a charge.
- **Node classes [A].** BEN: expansion or recovery with exits open or normal. DRT: exit drought without a macro crisis. STR: macro crisis, frozen exits, or a demand-bust or glut shock with the draw ≥ 8%. Availability, bids, red status and caps are keyed to these classes. Each node also carries two exogenous readings computed on the status quo's (B0's) path: its event stage (Green, Amber, Red or Black by the CFP indicators) and its goal-path gap ln(W̃^{B0}_n / (W₀·1.10^{t(n)})), which defines "behind" in G4 [RV-09, RV-11].

### 1.2 Lenses and portfolio levers

The user confirmed two definitions: **REFINANCE** raises cash against a holding without selling it, and **LEVER** borrows to add exposure [R: ARCH §4.8].

| Code | Definition | ΔE now | ΔB | Cash now |
|---|---|---|---|---|
| SELL | Dispose wholly or partly (sale, strip, tertiary, syndication, elected CV exit) | − | 0 | + |
| HOLD | Keep; fund calls, capex and cures | 0 | 0 | − calls |
| ADD | New exposure paid with cash or sales (re-up, purchase, new money) | + | 0 | − |
| REFINANCE | Borrow against a holding; exposure unchanged | 0 | + | + |
| LEVER | Borrow to add exposure; ≡ ADD + REFINANCE | + | + | ≈ 0 |
| PACE | Commitment budget; exposure arrives through calls | + later | 0 | 0 |
| REBALANCE | Net SELL in one group, ADD in another (two scored actions) | ± | 0 | ± |
| HEDGE | Size, roll, monetize or restrike convex protection | risk only | 0 | − premium / + monetization |
| FUND | Arrange or size Corporate Finance capacity (revolver, term-debt programme, repo lines) and set the buffer target. Drawing is not a lens of its own: a draw is REFINANCE or LEVER by R1 | 0 | 0 (capacity +) | − fees |
| REDEEM | Queued SELL of hedge-fund or open-end units on notice dates | − later | 0 | + later |

**Classification rules.**
- **R1, exposure-delta test (closed form) [RV-12].** Labels come from (ΔE, ΔB) at the node against the parent's position, not from the instrument. With ΔB_n the node's net new financing (total B, §1.1) and ΔE^disc_n the node's net discretionary exposure change (purchases, re-ups, synthetic and TRS adds, and calls on commitments made inside the tree, minus sales):
  $$\mathrm{LEVER}_n=\min\big(\Delta B_n^+,\ (\Delta E^{disc}_n)^+\big),\qquad \mathrm{REFINANCE}_n=\Delta B_n^+-\mathrm{LEVER}_n$$
  Borrowing therefore first funds the draw, calls on commitments that existed at t0, debt service and the floor (REFINANCE); only the remainder funds new exposure (LEVER). The split is unique and fixes the demo's mislabelled draws [R: TD verify_finance H5]. A FUND draw that meets needs is a portfolio-level REFINANCE (cash raised against the unencumbered balance sheet), and its card says so.
- **R2.** Internal transfers raise no liquidity and are priced at fair value on both legs [R: GRP §2.1].
- **R3.** P2S is REFINANCE (ΔE = 0; the futures' embedded financing enters B^syn), kept separate from beta additions [R: SYN §2.1].
- **R4.** At most one lens action per unit per node. It is exact only in the Level-B integer restoration of the root (SLIM §1.6 step 3). The LP and the comparison MILP use net-trade variables; at cohort level the rule has no meaning [RV-13].
- **R5.** Only LP-accessible instruments, in the cell the control rights allow [R: SYN §4.2 V23; RA §7.2].
- **R6.** An instrument's lens is fixed by R1 at the node where it is used, not by its name. The §2 tables name the usual lens, and "by R1" where use decides.

### 1.3 The action ledger

Each action a on unit i at node n, of size q ≥ 0, is one LP column. Its coefficients are recorded once:

$$\mathcal L(a,i,n)=\big(\Delta C_n,\ \{\Delta C_c\}_{c\succ n},\ \Delta V,\ \Delta N,\ \Delta U,\ \Delta B,\ \Delta\mathrm{Enc},\ \Delta E,\ \Delta m^{red},\ \{\Delta\widetilde W_\ell\},\ \kappa\big)$$

- **Linearity.** Engines are positively homogeneous in the fraction held, so entries are linear in q [R: ARCH §5.1].
- **Costs.** Size discounts and impact are convex piecewise-linear; every cost is charged once, as cash flowing into W̃ [R: ARCH ADR-42].
- **Fills.** Sold quantity ≤ success probability × attempted quantity [A].

---

## 2. Decision space by group

"Cash, exposure, CF" is the immediate cash effect, the exposure change and the change in future flows. Risk enters through factor loadings (§3.3) and the red margin (§4.6). Regime-keyed values read benign / drought / stress, mapped to node classes.

### 2.1 PE funds (allocation v2: NAV $34bn; unfunded $10.9–16.4bn)

Unfunded is $16.4bn on census v1.1, or $10.9bn at the v2 bucket's U/NAV [R: inputs §1A].

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| LP secondary sale or strip (SELL) | Cash +φ·p^ce·q now, (1 − φ)·p·q at t_d; V −q·θ; U −(U/N)q, because the buyer assumes the unfunded; later flows fall pro rata | Hedonic price p = Π_regime·g(age)·h(q̄)·exp(−κ_z(q/Depth)^γ). Buyout 0.91–0.94 of lagged NAV (benign); age multipliers 0.99 / 0.96 / 0.88 / 0.79 / 0.70; tail-end discount ≥ 25%; LP portfolios 0.87 (drought); crisis residual 0.80–0.84 of economic NAV. Deferral: p^ce = φp + (1 − φ)p(1 + r_v)^{−t_d} | 1–2 quarters. Success 0.75–0.85 / 0.6 / 0.4–0.5. ≤ 5% of segment depth per half-year. GP consent, ROFR. Red tier: red status by H9 | SYN §4.4; GRP §3.1; ARCH §5.2 (ADR-39) |
| CV election (SELL or HOLD; event) | As SELL at the CV price if elected | Sell iff p^ce ≥ roll value; SACVs 52% at par, 14% above, 34% below; LP rollover 14% | GP-triggered, ≥ 30 days; offers 0.05 a year per fund (benign), 0.08 (drought) [A] | GRP §3.1; LIT §4.11 |
| Re-up or up-size (ADD) | U +k; calls by age (20 / 25 / 30 / 35 / 40% of remaining) from the next year | Add iff posterior option value E[(μ_g − h)⁺] beats charges; fund-size penalty | GP allocation cap; 1–4 quarters | GRP §3.1; LIT §4.11 |
| Commitment budget (PACE) | A cut returns 12.5% of itself in year 1 and 66% by year 4; no liquidity credit for 2 quarters | c^PACE = 8.6¢ per PE $ forgone (5.6–12.3¢) | Green 0.75–1.25× plan; Amber 0.25–0.5× with a protected 25% core. Plan $3.5bn a year [A; v1.1's $5.34bn × 34/52] | GRP §3.1, §2.3 |
| LP-portfolio NAV facility (REFINANCE; Corporate Finance) | Cash +b(1 − OID); B +b; PIK, with a sweep at 1.5× starting LTV and default at 2×; pledged NAV encumbered | SOFR + 300bp (250–400); OID 1–2%; +140bp in stress. LTV 10% (5% stressed) on a pledge pool ≤ 20% of private NAV: ≈$2.1bn, $1.1bn credited | 6–12 weeks (0 if pre-arranged); availability 100 / 100 / 50%; pledge consent | SYN §4.4; GRP §2.3 |
| LP-portfolio preferred (REFINANCE) | Cash +20–35% of pool NAV; preferred return paid from distributions | 12% (14% in stress); MOIC floor 1.3× | 2–4 months [A] | GRP §3.1 |
| Collateralized fund obligation, CFO (REFINANCE) | Senior notes against a seasoned pool | Senior SOFR + 295bp (single-A) | 6–12-month lead; pool ≥ $1bn | SYN §4.4 |

### 2.2 Secondaries (NAV $14bn; unfunded $3.5bn plus $0.4bn deferred)

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| Discount purchase of LP interests (contingent ADD) | Cash −p^ce·N^ref; V +θ_n·N^ref; U +U^ref. Accretion (1 + y_P) ≈ (1 + y_V)(θ_n/p)^{1/D} is reported separately | **One price primitive [RV-10]:** price per $ of reported NAV p^ce_n = ρ_n·θ_n, with ρ_n the buyer residual on *economic* NAV; the reported-NAV discount 1 − ρ_nθ_n is derived, not set. ρ ≈ 0.98–1.02 at BEN (the 0.91–0.94 bid ÷ θ ≈ 0.92), 0.96–1.00 at DRT (the 0.87 LP-portfolio bid ÷ θ ≈ 0.88), and 0.80–0.84 at STR (the crisis residual on economic NAV) [R: SYN §4.4; GRP §3.1]. So a real edge exists mainly at STR nodes, and "discounts are not value" elsewhere [R: GRP finding 7]. θ_n is path-dependent (§5.1); tail-end θ is 0.78–0.83 / 0.75–0.80 / 0.65–0.70 [R: GRP §3.2]. Buy iff b\* ≥ p^ce after a 4.2–5.1% winner's-curse haircut. Sensitivities: θ = 0.75, and a zero-edge placebo with ρ = 1 in every class | Gate: discount > 20%, Tier 1 green, stage not Black. ≤ 3–5% of segment volume ($226–240bn in 2025) [S]; group NAV ≤ 10% of the fund. Research value 15–22¢ per $ at θ = 0.92 but 0.5–9¢ at θ = 0.75 [R: GRP §1] | GRP §3.2 |
| Deferred-payment purchase (LEVER = ADD + seller-financed REFINANCE, by R1) [RV-12] | Deferred payables are seller financing in B^sf (≤ 10% of group NAV) and hard outflows; at leaves they are deducted at face | At 91% with half deferred 12 months: IRR 14.3 → 15.3%, MOIC 1.47 → 1.41× | — | GRP §3.2 |
| Tertiary sale, strip or CV-stake sale (SELL) | As PE SELL; liquidity only with an external buyer | LP pricing by age; GP-led SACV and MACV pricing | Consent, ROFR; 3–6+ months; red tier | GRP §3.2 |
| LP-level facility; CFO (REFINANCE) | As the PE NAV facility | SOFR + 300bp; LTV 10–20% | Pledge consent | GRP §3.2 |
| Secondary-fund commitments (PACE) | Calls 45% a year of the remainder for 4 years | Countercyclical pacing (η < 0) | Contingent budget | GRP §3.2; SYN L14 |

### 2.3 Co-investment (NAV $18bn; 45 positions [A])

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| Single-asset sale or strip (SELL) | Cash +p·q; exposure −q | Bid = E_b[X]/(1 + y_b)^τ − tc, y_b 20–25%: 0.71–0.79 of NAV (BEN), 0.56–0.65 (DRT); CV-grade assets at SACV prices | 3–9 months; GP consent; red tier | GRP §3.4 |
| Pool facility (REFINANCE) | Cash +b; B +b; quarterly covenants | SOFR + 450–750bp; LTV ≤ 10 / 15 / 20% for effective N < 10 / 10–25 / > 25. **Single-asset REFINANCE is inadmissible** (trigger breached on 49.6% / 62.5% of paths) | GP consent; BEN only | GRP §3.4 |
| Holdco PIK (REFINANCE or LEVER by R1) [RV-12] | SPV debt at 12% PIK, 25% LTV, in B^sec with the PIK accrual deducted at leaves; equity wiped out if V ≤ κD. Cash-out against an existing co-investment is REFINANCE; only proceeds that buy exposure are LEVER | IRR 9.2 vs 9.2% (benign), 6.0 vs 6.3% (drought); wipe-out at exit 2.1 → 11.8% (benign), 7.0 → 22.8% (drought). It does not pay as LEVER in either class; as REFINANCE it needs ℓ̄ above ≈8% | BEN only; LTV ≤ 25% | GRP §3.4; SYN finding 8 |
| New co-investments (ADD, PACE) | Cash −q at close | ≤ accepted offered flow (θ = 0.33 per fee-bearing PE $) | $0.6–1.2bn a year; paused in Amber; effective N ≥ 40; position ≤ 4%; company ≤ 1% of NAV | GRP §3.4, §3.0; taxonomy v2 |

### 2.4 Capital Solutions (NAV $8bn)

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| Syndication; secondary sell-down (SELL) | Cash +p·q | Sell-down at 0.90 relieves $0.82 per $; secondaries at the yield mark −8–12% (BEN), −20–30% (STR) | ≤ 6 months; thin in STR; amber tier | GRP §3.3, §2.3 |
| Back-leverage (REFINANCE) | Cash +b at D/E ≤ 0.5, plus a cash-carry row (stressed cash income ≥ interest + fees) | Bank ≈ SOFR + 300bp. RoE 10.2% (bank), 8.9% (alternative lender), 9.25% unlevered; −2.3% cash carry per $ at a 30% PIK share | Arrange in BEN; P(LTV breach) ≤ 5%; ≤ 40% of the book encumbered | GRP §3.3 |
| Book CFO (REFINANCE) | Senior notes at LTV 35–45% | SOFR + 250–300bp | 6–12-month lead | GRP §3.3 |
| New money (contingent ADD) | Cash −q. E[r] = y^cash + y^PIK(1 − p^L_PIK) + OID/WAL + ρE[kicker]/WAL − PD·LGD − δ^ext/WAL, ρ ≈ 0.5 | Break-even IRR ≈ (1 + r_h)(1 + ℓ̄) − 1: 13.3% at the 9/9/4 fallback, 8.3% at ℓ = 1.83%; rescue deals 15–20% gross | ≤ $1.2bn a year; cash-pay families only | GRP §3.3, §2.3 |
| Amendment response (HOLD) | Grant, enforce or sell, by least-squares Monte Carlo | — | Event-driven | GRP §3.3 |

### 2.5 Private Credit (NAV $14bn: SMA 40%, closed-end 45%, evergreen 10%, BDC 5%)

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| SMA loan sales (SELL) | Cash +p·q | 1.00 / 0.99 / 0.95–0.97 / 0.80–0.88 of par (boom / normal / tight / crisis); beats run-off once ℓ̄ > 0.8–1.0% at 0.99 | Weeks; one $5.6bn sleeve shared with run-off | GRP §3.6 |
| LP sale; evergreen tender; BDC sale (SELL) | Cash +p·q | LP interests 0.92–0.95 / 0.85–0.89 / 0.70–0.78; tenders ≈38% filled; BDC at q·NAV | Days to 4 months; STR queues | GRP §3.6 |
| SMA run-off ρ ∈ [0, 1] (SELL at par by R1: ΔE < 0, cash +) [RV-12] | +$0.8–0.9bn in year 1 | Forgone reinvestment value net of losses | Quarterly | GRP §3.6 |
| SMA back-leverage (REFINANCE) | LTV ≤ 40–45% at a 65% advance | SOFR + 200–275bp; P(deficiency in 3 years) 1.0 / 3.0 / 12.8% | BEN; lender lead time | GRP §3.6 |
| SMA leverage (LEVER) | D/E ≤ 1.0× | Senior, non-software; expected loss < y_A − c_B ≈ 4.0% at P95 | BEN | GRP §3.6 |
| New loans (ADD, PACE) | LAY = r^fwd + s + o/T − PD·LGD − fees | Unitranche SOFR + 525bp (normal), +525–600 (tight), +700–900 (crisis); LGD 0.67; PD_N 1.1% | Contingent budget | GRP §3.6; SYN §4.3 |

### 2.6 Public Markets (hedge funds $20bn in 20 lots; long-only $36bn: DM equity 22, EM 6, fixed income 8)

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| Hedge-fund redemption (REDEEM) | No cash now; later cash at φ(h, S), P5 shares 19 / 55 / 66% by months 3 / 6 / 12 | Redeem iff α̂^net + κ^reentry < ℓ̄(T^cash) | Notice dates only; irrevocable; crisis gate hazard 1–20% a quarter | GRP §3.5; SYN §4.6 |
| Hedge-fund secondary sale (SELL) | Cash +(1 − d)·q now | d 15–25% (quarterly funds in a crisis) to 30–50% (gated) | — | GRP §3.5 |
| Unit loan (REFINANCE) | LTV 20–50% | SOFR + 250bp [A] | Pledge consent | ARCH §4.8 |
| Portable alpha; hedge-fund TRS (LEVER) | Exposure up; 10% independent amount; margin on reference NAV; HQLA collateral; costs ≈2 survival months | Net α must beat financing plus CVaR, leverage, VM and mismatch charges. α prior ≈ 0 [S: Jurek & Stafford 2015]; α = 0 is a mandatory sensitivity | Inside the 1.30× cap | GRP §3.5; LIT §3.9 |
| Long-only sale or purchase (SELL, ADD) | ±cash, ±exposure | Impact Yσ√(Q/V) + half-spread + tax: 4–13bp (US large cap) to 23–40bp (EM) per $1–5bn | T+1/T+2 | GRP §2.3, §3.5 |
| Physical-to-synthetic (REFINANCE) | Cash +(1 − m − b)·q; exposure unchanged; contingent VM ($1.65bn per $5bn in a −33% month) | Cost per $ freed per year 0.40–0.70% (normal), 0.80–1.11% (June 2026), 2.2–3.3% (stress) | 1–7 days; ≤ $10bn [A] | SYN §4.4 |
| Synthetic beta or completion (LEVER; embedded financing in B^syn) | Exposure +x; cash −IM (4% → 10%); financing SOFR + f | f 30bp average, 81bp (June-2026 roll), 175bp stress; CLC 27bp. Add iff ERP − f − κ^G − leverage and CLC charges > 0. Beta has α\* = 0 against its own benchmark, so it is never optimizer value: it is reported as risk budget spent (family F4a, §6.3) [RV-04, RV-08] | E within the cushion cap (§4.7 G5); gross overlay ≤ 0.30W; $10bn at t0 | GRP §3.7; SYN §4.5 |

### 2.7 Real Assets (NAV $18bn: real estate 9.0, infrastructure 6.5, ENR 2.5)

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| Asset or stake sale; JV sell-down (SELL) | Cash +p·q | Core direct discount 2 / 8 / 15–20%; value cost per $ raised (κ) 3.3% (US) to 14–18% in STR; infrastructure LP κ 5% / 15%; real-estate LP κ 31% / 45%; JV sell-down (controlled only) 0.95 / 0.92 / 0.80 | 4.5 / 7 / 10+ months; availability 0.85 / 0.70 / 0.50; ≤ 20% of annual segment volume; red tier | RA §6.2, §7.3 |
| Open-end redemption (REDEEM) | Queue at NAV: real estate 34% paid by month 12 (P5), infrastructure 67% (14% and 31% under T4′); zero credit in T3 and T4′ | Queue value cost at ℓ = 10%: 3.6 / 10.3 / 16.2% | Notices at Amber | RA §4.6, §7.4 |
| Cash-out at maturity (REFINANCE; controlled only) | Cash +b; B +b | ŝ 3.2 / 4.4 / 7.2% over SOFR; capacity $0.53–0.90bn; no early cash-out while the lock-in Λ > 0.5% of GAV | At maturity; availability 0.97 / 0.85 / 0.60 | RA §7.3 |
| Junior capital; sale-leaseback; ground lease (REFINANCE) | Junior 13–16%; leaseback ŝ ≈ 3.5–4.7% in perpetuity, near-irreversible | Headroom cost ≥ 0.34 per $ (leaseback) | 6–12 weeks; 3–6 months | RA §7.3 |
| Acquisition debt (LEVER; controlled only) | Exposure up through asset debt | Core real estate fails (cap 5.6–6.4% vs debt 6.8–7.1%); contracted infrastructure passes at SOFR + 200bp (α\* ≈ +0.4% after charges); ENR only ≥ 70% hedged with RBL ≤ 40% of deck PV, never in a glut or bust | Single asset ≤ 65% LTV (70% infrastructure); portfolio ≤ 55%; P(trigger in 12 months) ≤ 2% | RA §7.4–7.5 |
| Asset hedge (HEDGE; controlled only) | Swaps on ENR output or floating debt | Margin in boom tails | — | RA §9.3 |
| Commitments (PACE, ADD) | ≈$1.2bn a year inside an infrastructure-led envelope of $1.8bn ($1.5–2.1bn) | Hold oil-linked j only if α̂_j ≥ H_j + FTP_j + τ_j (H_j: levered upstream funds 2.4–2.9% of NAV a year; royalties 0.8–1.2%; fee midstream 0.3–0.4%) | ENR ≤ 1.5% of NAV; GCC real estate ≤ 1.0%; the 11.2m bbl RA delta may not rise while Tier 1 is violated | RA §2.3, §9.3 |

### 2.8 Overlay

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| Tail-ladder size (HEDGE) | Premium 3.74% a year of notional; crash payoff 0.166 per $ (4.4× the annual premium); $7.1bn of notional at the floor | 90/72 put spreads on 3 / 6 / 12-month rungs (25 / 50 / 25%); listed first. Must beat an equal-cost cash buffer [S: Gamba & Triantis 2014] | Budget 0.15–0.50% of NAV a year | GRP §3.7; LIT §3.10 |
| Monetize or restrike (HEDGE, SELL) | Cash +V(1 − ba) | Δ ≤ −0.5, value ≥ 3× premium or VIX ≥ 35 → sell 50%, reinvest 40%; refined by least-squares Monte Carlo (monetize iff V(1 − ba) + λ^wΔL ≥ continuation) | T+0 (listed) | SYN §4.6 |
| Opportunistic scale (LEVER, SELL) | Vol 1.0–1.5% of NAV; IM $1.0bn | Sharpe prior N(0.3, 0.25²); deflated Sharpe ≥ 0.95; cut at the drawdown stop, an OV breach or event-Red | IM ≤ $1.5bn; OV1–OV3 | GRP §3.7 |
| Oil put spreads (HEDGE, if mandated) | ≈0.078 bbl delta per bbl of notional | Crash protection (enabling value) | — | RA §9.3 |

### 2.9 Corporate Finance

| Action (lens) | Cash, exposure, CF | Pricing and cost | Availability, lag, capacity | Source |
|---|---|---|---|---|
| Arrange a committed revolver (FUND) | Capacity L ≤ $15bn; 15bp undrawn, 15bp upfront per 3 years | Needs banks (consent scenario R1) | From stage 1 after a 2-quarter lead; ≥ 10 banks, none > 12.5%; yearly test draw | SYN §4.5; ARCH §4.10 |
| Draw or repay (FUND; REFINANCE or LEVER by use, R1) | ±cash, ±B | SOFR + 85bp drawn; 0% in 30-day rows; ≤ 50% available in STR; facilities signed in stress count zero | — | LIT §4.3; ARCH ADR-38 |
| Term debt (FUND to arrange; the issue is REFINANCE or LEVER by R1) | 5-year bullet in B^rec | SOFR + 70–100bp [A]; beats selling if repaid within ≈5.8 years | Recourse debt ≤ 10% / 15%; ≤ 20% maturing in 12 months | SYN L6, §4.5 |
| Repo (FUND; a route, not a source) | Overnight to 3 months | Haircuts widen; quantity-run risk | No source credit in STR | LIT §4.3 |
| Liquidity buffer (FUND) | Treasury: 8% target, 4% hard | Carry c_buf 1.5% (1–3%), a ceiling | — | SYN §4.4, §4.9 |

### 2.10 Cross-group REBALANCE and admissibility

- **REBALANCE** is the net of SELL and ADD columns across groups; only external cash counts as liquidity. IC group ranges are **elastic and priced**, as SLIM §5.4 requires [RV-19]. Inside 0.5–1.5× the SAA weight there is no charge [A]. Beyond that, a breach costs 50bp a year per $ [A], waived at STR nodes (the CFP playbook breaches ranges before it sells red), and its dual is reported. Tight hard ranges drove every result in the demo [R: TD verify_finance H3]. Proximity to the edges is reported, and A20 re-solves with the ranges removed.
- **Inadmissible:** call default; non-consented transfers or pledges; REFINANCE or LEVER on LP or minority holdings; single-asset co-investment REFINANCE; refusing contractual delayed draws; counting internal transfers as liquidity [R: GRP §3.0].

---

## 3. Holding-level beliefs (component 1)

### 3.1 Translating the three marks onto one forward basis

**The basis.** Every signal is restated as the annualized forward log return on nowcast economic NAV, net of fees and carry, over the unit's remaining life H_i [R: SYN §4.3]. The nowcast is V\*_i = N_i·exp(β̃_kΔm − ψ_k). Since-inception IRR is sunk and is shown greyed out.

| Signal | Translation onto the forward basis | Error scale |
|---|---|---|
| Forecast f (base case, with P10/P90) | ρ_f = H_f^{-1}·ln(R_f e^{β̃Δm}/V\*), with R_f the remaining value implied by the stated MOIC or IRR on the engine's distribution profile | σ_f = κ_g(q₉₀ − q₁₀)/2.563 |
| Underwritten u | ρ_u = (ln M_u − ln M_t)/(T_u − a_i), with M_t current economic TVPI [I]; expires after T_u + 1 | κ_g × case spread |
| Actual a | ã = μ_k + φ_a(r^a − r^bench), r^a de-smoothed over ≤ 3 years; φ_a = 0.5 (buyout), 0 before year 3 | Outcome noise |
| Market anchor m (external bid p_i) | ρ_m = (y_b − π_b(age)) + ln(p_i/θ̂_i)/D_i. y_b: LP buyout 14%, tail-end 18%, single-asset co-investment 22% [A; co-investment from GRP §3.4's 20–25%]. π_b, the buyer–seller PME gap: ≈3pp a year at ages 4–9, −0.8pp tail-end; the anchor is unused below age 4, where the gap is +24.5pp | σ_m = bid dispersion ÷ D [A] |
| Prior | μ_k = r_f + β_k·ERP + α\*_k, from the CMA mixture and α\* priors (PE +0.75, co-investment +1.0, secondaries +1.0, Capital Solutions 0, Private Credit 0, hedge funds 0, long-only −0.15pp) | Prior sd from the α\* P10–P90 |

Sources: R: SYN §4.3, §4.12; ARCH §4.7; GRP §3.2.

Bids enter leave-one-out, and in-house desk quotes are never prices [R: SYN §2.2 rule 4; RA §7.4]. Real Assets translate through cap rate, NOI growth and exit cap on the RAME nowcast [R: RA §8.2–8.3].

### 3.2 Correcting group bias from the quarterly archive

Each debiased signal is s̃_j = s_j − b̂_{g,j}, with a Bühlmann-type credibility estimate of the bias:

$$\hat b_{g,j}=Z_{g,j}\,\bar e_{g,j}+(1-Z_{g,j})\,b^{prior}_{g,j},\qquad Z=\frac{n_{eff}}{n_{eff}+20}$$

- **Errors.** Archived forecasts are scored against the realized forward return over the next 4–8 quarters, clustered by vintage, with declined deals included at inverse-propensity weights.
- **Bias priors, b^u / b^f in pp a year:** PE +5.0 / +3.0 (+4.0 after age 8); Secondaries +2.0 / +1.5; co-investment +6.0 / +3.5 after structural corrections (hold +1.5–2 years, exit multiple shrunk 50% toward entry); Capital Solutions +2.0 / +1.5; Private Credit +0.75 / +0.75; hedge funds +3.0 / +2.0; long-only +1.0 / +0.75; Real Assets by segment (core RE +1.5 / +1.0; value-add RE +4.0 / +2.5; core infrastructure +1.0 / +0.75; ENR +3.0 / +2.0, rising to +2 to +4 when oil falls).
- **Credibility.** κ_g, the ratio of true to stated 80% widths, has prior LN(ln 1.75, 0.25²); stated ranges widen ×1.81–2.74. Precision is 1/(κ_g²σ²)·min(1, 8/h) at a horizon of h quarters, with no second credibility multiplier.

Sources: R: SYN §4.3; GRP §3.1–3.6; RA §8.4; ARCH §4.7.

### 3.3 Fusion and the forward distribution

$$\hat\mu_i=\frac{w_0\mu_k+\sum_jw_j\tilde s_j}{w_0+\sum_jw_j},\qquad w_j=\tfrac12\,\frac{\text{prec}_j}{\sum\text{prec}}+\tfrac12\,\frac1{J+1}\ \ (\text{until } n_{eff}\ge20)$$

- **Weights.** They are shrunk halfway toward equal weights until the group's archive reaches n_eff ≥ 20. Constrained GLS is rejected, because it lost to simple averages out of sample. Correlated errors enter only the predictive variance [R: RA §8.5; LIT §4.10].
- **Fund interests.** Benktander credibility combines the forecast's chain-ladder estimate with the Bornhuetter–Ferguson prior frozen at inception: c\* = p/(p + t), t = 0.3–0.5 [R: SYN §4.3].
- **Predictive distribution.** σ̂_i² is the posterior variance plus outcome noise (15% a year for funds, 30% for single deals). Tails are Student-t with ν = 5 [R: SYN §4.1, §4.3].
- **Factor loadings b_i** (equity, credit, rates, oil, exit), de-smoothed: buyout β 1.0 and VC 1.4; co-investment β ≈ β_A·V/E with β_A 0.9; CV stakes 1.5–1.6; core RE 0.57 true against 0.22 observed; oil elasticities 0.84 (levered upstream), 0.41 (royalties), 0.13 (fee midstream); GCC real estate 0 today and 0.18 in SG or DB states [R: GRP §3.1–3.4; RA §8.5, §9.3].
- **Output per unit:** (μ̂, σ̂, ν, b, θ̂, P10/P50/P90, weights, flags, P(forecast optimistic) = Φ((ρ_f − μ̂)/σ̂)).
- **In the tree [RV-01],** R_{i,c} = μ̂_i − ½σ²_{sys,i} + b_i'(f_c − E f) + σ_{post,i}(ρ_g e_{g,c} + √(1 − ρ_g²) e_c).
  - The last term is **belief risk**: e_c is one standardized belief-error driver drawn at the stage-1 branching and held to the leaves, and e_{g,c} is its group-bias component. ρ_g comes from the archive's bias credibility (§3.2) [A]. Without it, two units with the same loadings but different μ̂ form a riskless spread in the tree, and the LP would push belief-versus-bid swaps to their caps with no perceived risk.
  - Idiosyncratic outcome noise stays in the simulator. In the tree it enters as concentration caps (H12) and a per-unit trade cap, |Δv_i| ≤ k_sel·W₀·σ_ref/σ_{post,i} [A: k_sel = 0.5%, σ_ref = the median σ_post], so units with weaker evidence trade in smaller size.
  - Out of sample the truth is sealed and comes from a different model than the fusion assumes; a second mode draws α ~ N(μ̂, σ²_post) (§5.5).

### 3.4 From belief to action: hurdle, reservation price and break-even return

Reading rules for the decision card: the LP decides jointly, and these explain its choices. **Every card quantity is read from the solved LP, so a card can never contradict the decision it explains [RV-08].** Test A23 checks this on every root column.

**Hurdle (goal basis).** $h_i=r_f+\bar\ell_i(D_i)+\kappa^G_i$: the term-average liquidity premium from the duals [R: ARCH §5.6], and the goal-tail risk charge κ^G_i. κ^G_i is the unit's risk adjustment under the LP's own goal kernel: the duals of the goal rows, the depth-guard rows (H10), the red-event row (H9) and the cushion caps, times the unit's marginal contribution to each. Equivalently, h_i is the forward return at which the unit's HOLD column has zero reduced cost.
- **What changed from v1.0.** v1.0 also added the CMA risk premium RP_i. The goal objective already prices risk through κ^G, so adding RP_i counted risk twice. That version would have read FAIL on synthetic beta (μ̂ − r_f − RP = 0) while the LP, which earns ERP − f against κ^G, takes it.
- **Utility view.** The research hurdle r_f + RP_i + ℓ̄_i + κ^R_i [R: SYN §4.4] is shown on the card as a second line, labelled "utility view". The IC can see when a choice is goal-driven, that is, it passes on the goal basis but fails on the utility view.

**Reservation price,** per $ of reported NAV:

$$p^*_i=\hat\theta_i\,e^{(\hat\mu_i-h_i)D_i}+u_i\,\psi_i+\frac{\kappa^{GP}_i+\kappa^{irr}_i}{N_i},\qquad \psi_i=\mathrm{PV}_h(\text{calls})\big(e^{(\hat\mu_i-h_i)D_U}-1\big)$$

- u_i = U_i/N_i, and ψ_i is the value of each $ of unfunded commitment. It is negative when μ̂ < h, in which case a buyer taking the unfunded is relief [I, from R: GRP §3.0].

**Break-even forward return.** μ^BE_i solves p\*_i(μ^BE) = p^ce_i. Ignoring the unfunded and the charges, μ^BE_i = h_i + ln(p^ce_i/θ̂_i)/D_i.

| Decision | Rule (card) | Source |
|---|---|---|
| SELL | μ̂_i < μ^BE_i (equivalently p^ce > p\*), and the sale is admissible. A sale that is a red event by ADR-39 (H9) is shown only through a forced re-solve; at the root, every red-tier sale is (today's stage is Amber) | R: GRP §3.0; ARCH §5.2 |
| HOLD | μ̂_i ≥ μ^BE_i, and no financing action pays | — |
| REFINANCE | HOLD wins and liquidity is scarce over a bridge of length T: s_B + f/T + λ_Lev + covenant charge + tightening premium (≈1.1pp) < ℓ̄_{[0,T]}. Display aid only: the sell-versus-borrow horizon T\*_i = (ln(θ̂_i/p^ce_i) − f)/s_B. It reproduces L6's "≈2 years" but ignores the asset's carry μ̂ − h, so the decision itself comes from the LP | R: ARCH §4.8; LIT §4.3; [I] for T\* |
| ADD | μ̂^new + ln(θ̂/p^buy)/D − h^new > 0, within capacity and gates | R: GRP §3.0, §3.2 |
| LEVER | Read additively (ADR-49): μ̂ − (r_f + s_B + f/T) − λ_Lev − covenant charge − tightening premium − κ^G > 0, and the guards of §4.7 allow it. For beta, μ̂ − r_f = ERP, so the card shows "risk budget" rather than "alpha" [RV-08] | R: ARCH ADR-49 |

**Goal reading.** Each card also shows the goal value per $, $G_a=\sum_\ell\pi^G_\ell\,\Delta\widetilde W_\ell(a)$ (§4.3), and its forced-re-solve ΔP(goal) out of sample. Flip thresholds (μ^BE, p\*, break-even ℓ) come from parametric re-solves of the LP, not from the closed forms above. The closed forms are first-order readings and must agree with the LP's choice in sign (A23).

**Worked anchor.** A 2018 buyout fund bid at 88% has p\* = 87.3–87.7%, a marginal SELL; on a pinned dual p\* collapses to 0.9%, hence feasible-only prices [R: SYN §4.4; L15].

---

## 4. The goal-seeking objective (component 3)

### 4.1 The goal

**Definition.** Ten percent a year nominal, as a time-weighted return gross of distributions, over a 5-year decision horizon; the 10-year horizon is a sensitivity [A, user working assumption]. **The TWR is measured on economic NAV** (de-smoothed, §3.1), in the tree and in the simulator alike. P(goal) on reported NAV is shown beside it. A gap above 2pp in favour of reported NAV is flagged as reliance on appraisal smoothing, because stale marks after a crisis would otherwise let an illiquid-heavy plan look closer to the goal [RV-18]. With draws D_t paid at the end of period t, time-weighted wealth satisfies

$$W_0\prod_{t\le T}(1+r_t)=W_T+\sum_{t\le T}D_t\,G_{t\to T},\qquad G_{t\to T}=\prod_{k=t+1}^{T}(1+r_k)$$

- **In the tree,** G_{t→T} is the scenario's realized static-SAA return, exogenous per scenario, so W̃_ℓ is affine in the decisions [R: SYN §4.9; ARCH §5.4].
- **In the simulator** the exact TWR is computed; the difference is error-ledger row E1 (§7.2).
- **Goal and miss.** W* = W₀·1.10⁵ ≈ $285.1bn (10-year sensitivity: W₀·1.10¹⁰ ≈ $459.1bn). The normalized miss is X = (W* − W̃)/W₀, and the goal is met iff X ≤ 0.

**Terminal value at the leaves [RV-07, RV-18].** The tree and the simulator use the same valuation.
- **Private NAV** counts at economic value with ω_g = 1. Economic NAV already carries the crisis, so v1.0's ω = 0.90 after a crisis year counted the crisis twice. A liquidation basis (ω_g = 0.90 after a crisis for red-tier groups, floored at 1 − the crisis discount [R: TD params]) is a sensitivity, applied in both engines.
- **Unfunded commitments** carry ψ_g = $0.02–0.05 per $ [A] (sensitivity 0–0.10).
- **Every financing claim is deducted at fair value:**
  - debt at face plus accrued PIK;
  - CFO notes;
  - deferred payables;
  - preferred equity at the greater of its accrued 12% preferred return and its 1.3× MOIC floor, less what it has received;
  - sale-leaseback and ground-lease obligations at the PV of their rents;
  - TRS, futures and overlay positions at mark-to-market.

  Otherwise a REFINANCE through any non-debt claim would look free at the horizon.
- **Pacing charge counted once.** New commitments made in the tree earn their modelled returns inside the horizon. So c^PACE applies only to the post-horizon part of the forgone alpha, as a terminal charge per $ of cut, not as an upfront cash charge.
- **Horizon rows.** Every horizon row of §4.6 holds at the leaves and at every fan year, which stops end-of-horizon artefacts [R: TD verify_finance H1].

### 4.2 Why bPOE, and where it fails

**bPOE.** For the miss X, the buffered probability of exceedance at threshold 0 is

$$\mathrm{bPOE}_0(X)=\min_{a\ge0}\mathbb E\big[(aX+1)^+\big]=1-\alpha\ \text{ such that }\ \mathrm{CVaR}_\alpha(X)=0$$

[S: Rockafellar & Royset 2010; Mafusalov & Uryasev 2018], as implemented in `stats.bpoe`.
It is the share of worst outcomes whose average just reaches the goal.
- **Properties.** bPOE ≥ P(X > 0); it is quasi-convex; {bPOE ≤ p} = {CVaR_{1−p}(X) ≤ 0}; for affine losses it is an LP [S: Rockafellar & Uryasev 2000, 2002].
- **Precedents.** Cash-flow matching [S: Shang, Kuzmenko & Uryasev 2018]; mean–bPOE pre-commitment behaves well when re-solved [R: LIT §4.7, Dang et al. 2025].

**Proposition 1 (bPOE cannot be gamed) [I].** If X ≤_icx X′, then bPOE₀(X) ≤ bPOE₀(X′).
- *Proof.* Each x ↦ (ax + 1)⁺ is convex and non-decreasing, so each expectation is icx-monotone, and so is their minimum.
- *Consequence.* A pure gamble (a mean-preserving spread of the miss) can never lower bPOE, though it can lower P(miss): the digital-option pathology [S: Browne 1999; Föllmer & Leukert 1999; R: SYN L9].

**Remark 1 (what Proposition 1 does not exclude) [I] [RV-03].** Icx-monotonicity rules out mean-*preserving* spreads only. For a fixed a, E[(aX + 1)⁺] = (a/W₀)·E[(W^b − W̃)⁺] with W^b = W* + W₀/a. That is a *linear* shortfall below a buffered target, the exponent-1 class that LIT §4.7 [S: Krabichler et al.] shows can reproduce probability maximization.
- **Pointwise argument.** With a pricing kernel ξ, minimizing E[(W^b − W̃)⁺] subject to E[ξW̃] = W₀ sets W̃ = W^b in states where ξ is cheap relative to probability, and W̃ = 0 elsewhere. So bPOE can reward *mean-increasing* spreads that load wealth into cheap good states.
- **Check** [I-calc, SYNTHETIC; `examples/mpo_v2/review_checks/check_objective.py`, reproduced by test A6b]. Complete lognormal market, 5 years, 400 states, 14.4% volatility. The bPOE-optimal payoff is two-valued: {0, 2.77·W₀} with 26% of states at zero (8.3% mixture), and {0, 2.40·W₀} with 13% at zero (10.47%, M2). The squared-shortfall optimum is smooth, with 400 distinct values.
- **Implication.** ADIC's market is far from complete, but leverage, short-volatility carry, levered credit and option overlays move the book toward that shape. In STRETCH, GBO is risk-neutral inside the guards. The protection against digital payoffs therefore comes from H9, the multi-level H10, G4–G5 and the CRRA tie-break, not from the objective alone. This is the reason SLIM §2.4 makes its downside floor hard.

**Proposition 2 (a stretch goal makes it degenerate) [I].**
1. If E[X] ≥ 0, that is E[W̃] ≤ W*, then bPOE₀(X) = 1, because E[(aX + 1)⁺] ≥ aE[X] + 1 ≥ 1 for every a ≥ 0.
2. If E[W̃] < W*, any concave ψ ≤ 𝟙{w ≥ W*} has E[ψ(W̃)] ≤ ψ(E W̃) ≤ 0, by Jensen.

So above the expected outcome no convex program can certify a positive goal probability. A probability objective has gradient there only through risk.

**Proposition 3 (what the probability objective asks for) [I].** Let W̃(x) = m(x) + s(x)Z for a fixed standardized Z, on a concave increasing (m, s) frontier.
- *Stretch (m < W\*).* P(goal) = 1 − F_Z((W* − m)/s) rises with s at fixed m. Under a binding limit ρ(W̃) ≤ c, with ρ translation-equivariant and positively homogeneous (CVaR, for example), the P(goal)-optimal point is the mean-maximizing point at that limit.
- *Plan (m > W\*).* bPOE and P(goal) both depend only on (m − W*)/s, so minimizing bPOE maximizes P(goal). This is Roy's safety-first criterion [S: Roy 1952].

**Numbers.** I.i.d. lognormal check, 300,000 paths, σ = 14.4%, futures financing 30bp, SOFR 3.89% [I-calc, SYNTHETIC; reproduced by acceptance test A6]:

| Geometric return a year (bridge model) | Leverage | E[W̃]/W* | P(goal, 5y) | bPOE₀ | Optimal buffer c\* (W₀) |
|---|---|---|---|---|---|
| 8.30% (mixture) | 1.00× | 0.974 | 40.4% | **1.000** | — |
| 8.30% | 1.30× | 1.047 | 46.0% | 0.969 | 1.76 |
| 8.84% (M1) | 1.00× | 0.999 | 43.5% | **1.000** | — |
| 8.84% | 1.30× | 1.080 | 49.0% | 0.938 | 1.43 |
| 10.47% (M2) | 1.00× | 1.075 | 52.6% | 0.910 | 0.92 |
| 10.47% | 1.30× | 1.188 | 57.9% | 0.820 | 0.96 |

**A pure gamble, on the M2 row.** Add a 5% chance of losing a further 1.0·W₀, offset by a small gain otherwise, so the mean is unchanged. P(goal) rises from 52.6% to 54.3%; bPOE worsens from 0.910 to 0.913. Research-central models sit on the degenerate rows unless levered [R: SYN §4.12].

1 − bPOE is Brown and Sim's CVaR satisficing measure [R: SYN L9; SLIM §3.3]: an aspiration above the mean cannot be satisficed without taking risk.

### 4.3 The main objective: the Goal-Buffered Objective (GBO)

$$\Phi(x)=\min_{a\ge a_{\min}}\mathbb E\big[(aX(x)+1)^+\big],\qquad a_{\min}=1/c_{\max},\quad c_{\max}=2W^*/W_0\ (\approx3.2\text{ at }5\text{ years},\ 5.2\text{ at }10)\ [A]$$

c_max sits above the largest optimal buffer in the check (1.8·W₀ at 5 years). On a finite tree the optimal buffer is attained at a leaf, c\* = (W̃_ℓ\* − W\*)/W₀ ≤ (max_ℓ W̃_ℓ − W\*)/W₀. So one condition, **max_ℓ W̃_ℓ ≤ W\* + c_max·W₀ (= 3W\* at 5 years)**, guarantees both GBO = bPOE in PLAN and the exact STRETCH form P3 [I] [RV-17]. Test A7 checks the condition and flags a binding a_min.

| Property | Statement | Status |
|---|---|---|
| P1 Bound | Φ ≥ bPOE₀ ≥ P(miss); Φ = bPOE₀ when c\* ≤ c_max | [I] |
| P2 No mean-preserving gamble | Monotone in the increasing convex order, so a mean-preserving spread is never rewarded. Mean-increasing skewed payoffs can be rewarded (Remark 1), so the guards of §4.6–§4.7 carry that protection | [I] (Prop. 1, Remark 1) |
| P3 Stretch limit | If E[X] ≥ 0 for every feasible x, the minimum is at a = a_min and Φ = a_min·E[(X + c_max)⁺]. That equals 1 + E[X]/c_max when the leaf condition above holds; otherwise it is a capped mean, which is still concave in W̃. GBO then maximizes E[W̃] inside the rows and guards, which is P(goal)-optimal at the binding tail limit under location–scale | [I] (Props 2–3) |
| P4 Continuity | Φ crosses 1 continuously at E[W̃] = W\*. Below 1 it is a buffered miss probability; at 1 or above the goal is STRETCH, with (Φ − 1)·c_max = E[X] | [I] |
| P5 Linear | Write the miss as X_ℓ(x) = c_ℓ − g_ℓ'x, where c_ℓ = (W\* − W̃_ℓ(0))/W₀ is the decision-free part and g_ℓ the leaf's decision coefficients (SLIM §3.2 writes the same affine map as L_ℓ = c_ℓ'x + e_ℓ). Then y = a·x, τ = a ≥ a_min; minimize Σ_ℓ p_ℓ z_ℓ s.t. z_ℓ ≥ τc_ℓ − g_ℓ'y + 1, z ≥ 0, A_ub·y ≤ b_ub·τ, A_eq·y = b_eq·τ. Auxiliary variables of the CVaR rows (H9, H10) are scaled by τ as well | [S: Mafusalov & Uryasev 2018]; [I] |
| P6 Prices | Duals give the goal kernel π^G and the hurdles | [I] |

**Algorithm.**
1. **Phase I.** Minimize the hard-row violation over reversible levers. If u\* > 0, report STRUCTURAL_RECOVERY; prices come only from the restored problem [R: SYN L15; ARCH §5.5].
2. **Mean LP.** Maximize E[W̃] under every row of §4.6 and guard of §4.7. If E\*[W̃] ≤ W\*, the label is **STRETCH** and this is GBO's solution.
3. **bPOE bisection.** Otherwise the label is **PLAN**. Find the smallest p with min_x CVaR_{1−p}(X(x)) ≤ 0; this is monotone in p, so bisection is valid. About 10 LPs reach a precision of 10⁻³ and about 20 reach 10⁻⁶. The minimizer at p\* is the policy, and p\* = Φ\*.
4. **Cross-check.** Steps 2–3 must match the perspective LP in Φ to within the bisection tolerance plus 10⁻⁶. The LP's value must match `stats.bpoe` on its own leaf values to within 10⁻⁶; this replaces SLIM's 10⁻⁹, which is below HiGHS's default feasibility tolerance of 10⁻⁷ [RV-17].

**Selection, reconciled with SLIM §3.3.** SLIM's candidates are the plans ĝ\*(p), p = 5–95%, each maximizing the mean of the worst 1 − p outcomes of W̃.
- **The family contains both GBO solutions:** p → 0 is the mean LP (STRETCH), and in PLAN the bPOE solution is ĝ\*(1 − Φ\*).
- **Selection.** Candidates are scored on a selection set of 10,000 paths, and the guarded one with the highest exact P(goal) is adopted; GBO's solution wins ties within 2 paired SE. Reported probabilities come from a separate certification set (§5.5), so the choice does not bias them. In STRETCH, P(goal) rises with risk (Prop. 3), so this rule picks the most aggressive guarded candidate. The report therefore shows every candidate against the risk-matched control's line (§4.8) [RV-04].
- **Tie-break (mandatory).** Hold the goal value within a tolerance, then maximize the CRRA(3) certainty equivalent. This removes unpaid risk, damps the all-or-nothing tendency of Remark 1, and gives λ in ordinary units [R: SLIM §3.3; ARCH §5.4]. The tolerance is defined per case [RV-16]:
  - PLAN: CVaR_{1−(Φ\*+0.005)}(X) ≤ 0, i.e. bPOE ≤ Φ\* + 0.5pp;
  - STRETCH: E[W̃] ≥ E\*[W̃] − 0.005·c_max·W₀ (≈ 0.016·W₀ ≈ $2.9bn of 5-year mean wealth, ≈ 0.25pp a year);
  - ĝ\*(p) candidates: the mean of the worst 1 − p of W̃ stays within 0.5pp a year (annualized) of its optimum.
- **Pre-commitment.** The tree's contingent plan is pre-committed and re-solved quarterly against the original goal path W₀·1.10^t, not a reset goal (Forsyth 2020); horizon test A10 polices drift [R: LIT §3.2]. Certification reports both the pre-committed playbook and rolling MPC (§5.5) [RV-15].

**The goal kernel.**
- In PLAN, π^G_ℓ ∝ p_ℓ on the buffer tail {ℓ : a\*X_ℓ + 1 > 0} and 0 elsewhere. A dollar is worth the same in every near-miss and miss leaf, and nothing in comfortable leaves.
- In STRETCH, π^G_ℓ = p_ℓ(1 + Σ_α η_α·𝟙{ℓ ∈ worst 1 − α}/(1 − α)) over the depth-guard levels α ∈ {0.90, 0.95, 0.99}, plus the red-margin and limit duals, with η_α the dual of each H10(a) row. This is a mean–CVaR kernel.
- The liquidity premium is read from the cash rows as ℓ_n = M_n/(π^H_n − M_n), always on a feasible problem [R: SYN §4.4; ARCH §5.6]. v1.0 wrote μ_n, which collides with the return symbol [RV-17].

### 4.4 Exact comparison: maximize P(goal) as a MILP

$$\max\sum_\ell p_\ell g_\ell\quad\text{s.t.}\quad \widetilde W_\ell-W^*\ge\varepsilon_gW_0-M_\ell(1-g_\ell),\quad g_\ell\in\{0,1\},\ \text{plus every row of §4.6–§4.7}$$

- **Big-M [RV-13].** M_ℓ = W* + ε_gW₀ − L_ℓ, for any valid lower bound L_ℓ ≤ min W̃_ℓ over the feasible set: with g_ℓ = 0 the row reads W̃_ℓ ≥ L_ℓ. ε_g = 0.001 [A] stops knife-edge successes [I].
  - **Default: L_ℓ = 0.** This is valid because H5 holds at every constraint node, so wealth stays non-negative while no one-year exposure-weighted loss in the tree exceeds 1/1.30 ≈ 77% (checked when the tree is built), and accrued draws are non-negative.
  - **Optional: LP-tightened L_ℓ and U_ℓ**, two cost-only re-solves per leaf. With them, fix g_ℓ = 1 where L_ℓ ≥ W* + ε_gW₀ and g_ℓ = 0 where U_ℓ < W* + ε_gW₀. Use them only if the gap stalls. In the pilot, 400 bound LPs took 514 s and fixed 54 of 200 binaries, and the MILP then took 95 s against 65 s without fixing. At full scale they would cost hours.
- **Integers.** Only the goal indicators. R4's one-action rule is not imposed here (§1.2), because ≈40 cohorts × 91 decision nodes × 5 lenses would add ≈18,000 binaries (≈12,000 on v1.0's 61-node tree) for a rule that has no meaning at cohort level.
- **Solver.** HiGHS MIP: gap 0.005, a 1,800-second limit, and a MIP start from GBO with g_ℓ = 𝟙{W̃_ℓ ≥ W* + ε_gW₀}.
- **Sizing evidence** [I-calc, SYNTHETIC; `examples/mpo_v2/review_checks/milp_pilot.py` and `optimism_check.py`, with their outputs]. A 10 × 5 × 4 tree with 40 cohort assets, 9.6k columns, 8.3k rows and 200 goal binaries closed to optimality (gap < 0.5%) in 65 s and 441 branch-and-bound nodes, single-threaded, and also closed with the loose M = W* + ε_gW₀ + W₀. The full tree (640 binaries, ≈80k columns) is expected to need 30–90 minutes. If the gap exceeds 2pp at 1,800 s, the MILP runs on a stratified subtree (10 × 8 × 2: two fan paths per stage-2 node, drawn from the lower and upper halves of the fan, each with mass p_n/2), with GBO re-solved there.
- **Model size.** The MILP runs on the same cohort-recourse model as GBO (§5.3), so the comparison is like-for-like with no separate reduction. The recommendation comes from GBO.
- **Diagnostics.** Reported: pile-up mass P(W* ≤ W̃ < W* + 0.01·W₀), deep-miss mass P(X > 0.2), the in-tree minus out-of-sample gap, and the free-binary count. A8's "in-tree P(goal) ≥ GBO's" holds by construction through the MIP start, so it checks the start only. The informative MILP test is H5 (§6.5).
- **Variant B (Tier 1 only, SLIM §3.4) and variant A (every guard).** Variant B exposes the pathology §4.7 blocks. In the pilot, the guarded MILP lifted in-tree P(goal) from 39.5% to 67.0%, yet its root decision was 1.3pp *worse* out of sample than a risk-matched leverage control (§6.1).

### 4.5 Third comparison: CRRA plus quadratic shortfall (the current design)

$$\max\sum_\ell p_\ell\Big[\hat U_3(\widetilde W^{real}_\ell/W_0)-\lambda_T\,\hat\psi\big((1-\widetilde W_\ell/W^*)^+\big)\Big]$$

γ = 3; λ_T = 1 (0–2); 48 adaptive tangents, and a piecewise-linear square; the target restated at 5 years [R: SYN §4.9; ARCH §5.4]. The exponent is 2 > 1 [R: LIT §4.7].

### 4.6 Hard constraints (identical under all three objectives)

"At every node" includes the fan years t = 3, 4, 5 of every leaf path [RV-07]. Each row's dual is reported. Each IC-set limit (as opposed to a contractual or survival row) is also re-solved relaxed, one at a time, so a limit that does the work is visible (A20) [RV-19].

| # | Constraint | Form in the tree | Source |
|---|---|---|---|
| H1 | Owner draw paid at every node | D_n = d_n·B_{y(n)}: opening-year reported NAV times an exogenous oil-linked rate (§5.1), in every cash row with no slack | SYN §4.7; TD §9 |
| H2 | Cash floors | C_n ≥ 0.04·W_n at every node and leaf. C_n ≥ 0.08·W_n at BEN and DRT nodes, except the first node after a STR node; posted IM excluded. SLIM prices the 8%, but a notional price would distort W̃, so here it is hard and its dual is the price. In the demo any price ≥ 1% gave the same plan [R: TD RESULTS §7] | SYN §4.9 (T2) |
| H3 | Short-horizon coverage | At the root and stage-1 nodes: unencumbered haircut HQLA ≥ the 30-day need, with facilities at 0%. At every decision node, non-red capacity within 6 months (Treasury above 4%, long-only after a stress haircut, hedge-fund φ(6m), facility headroom from month 2) ≥ the next six months' draw + stressed net calls − P10 distributions [A] | SYN §4.9 (T3) |
| H4 | 24-month named stress at the root (T4′) | Σ_k h_kR_k(x₀) + F²⁴(x₀) ≥ NCO²⁴_{s\*}(x₀), linear by positive homogeneity. s\*(θ\* = 0.58; 0.76 as a sensitivity): equity −35.8%; distributions at 0.189 × drought rates; calls ×1.29; draws at 10% of opening NAV for 2 years; revolver credited ≤ 50% from month 2 if signed; NAV facility at 5% LTV; hedge funds fully noticed at 0.83 pass-through. If the book fails with Phase I u\* = 0, an EXECUTION_RECOVERY allowance applies at the root, and the row must hold at stage-1 non-STR nodes | ARCH §4.9, §5.5 |
| H5 | Leverage and debt | E_n ≤ 1.30W_n. Recourse debt ≤ 0.15W (hard; 0.10 reported as target). Encumbrance ≤ 20% of total assets; private pledges ≤ 20% of private NAV; ≤ 20% of debt maturing within 12 months | SYN §4.5 |
| H6 | LTV caps | As in §2 (NAV facility 10%, 5% at STR; co-investment pool 10–20%; Capital Solutions D/E 0.5; SMA 45%; RA 65% / 70%, portfolio 55%; holdco PIK 25%, BEN only), with forced paydowns when a cap tightens | §2 tables |
| H7 | Sale-depth caps | PE and Secondaries LP sales ≤ 5% of segment depth per half-year × success probability; RA ≤ 20% of segment volume; co-investment ≤ 10% of group NAV a year [A]; shared SMA sleeve; long-only impact above 5% of ADV. In liquidity rows (H2–H4, H9) planned sales count at the *stress-class* success probability of the node's worst child, because failures cluster in stress | §2 tables |
| H8 | Oil exposure | ENR ≤ 1.5% of NAV; GCC real estate ≤ 1.0%; total delta ≤ the Tier-1 backstop (≈170m bbl under Mix B); RA delta frozen while any Tier-1 row is violated; new oil-linked ADDs clear H_j | RA §9.3 |
| H9 | Red-event limit (CVaR surrogate) | Signed red margin per node: m^red_n = next-12-month required outflows − non-red capacity (cash above the floor, liquid book after haircut, hedge-fund φ, facility headroom, amber sales), linear in the state. With R_ℓ the maximum over the path's decision nodes **and fan years**: η + (1/ε_R)Σ_ℓ p_ℓ z_ℓ ≤ 0, z_ℓ ≥ m^red_n − η for every n on ℓ's path, z ≥ 0. **ε_R in the tree is a tuned buffer**, default 0.60% (SYN §4.9's surrogate), tightened by bisection on the selection set until the certification Clopper–Pearson bound on P(red, 5y) is ≤ 1% [RV-22]. **Red event by ADR-39 [RV-09]:** a sale of a red-tier unit (PE, Secondaries, Co-investment, Real Assets assets or LP interests) is a red event if (i) it is forced recourse, (ii) the node's status-quo event stage is Amber or worse, or the node is the first after a STR node (the only BEN or DRT node where H2 lets IG + cash fall below 8%; this keeps ADR-39's cash test exogenous and the row linear), or (iii) its bid is below 0.9 × the unit's normal-class bid. Planned (non-red) red-tier sales are therefore possible only at Green BEN nodes. Today's stage is Amber, so at the root every red-tier SELL column is held at zero and priced by forced re-solve | SYN §4.9 (T6); ARCH §5.2 (ADR-39), §5.4 (H3–H4) |
| H10 | Depth guard | (a) **Relative, multi-level [RV-03]:** CVaR_α(X) ≤ CVaR_α(X^{B0}) + δ_α for α ∈ {0.90, 0.95, 0.99}, where X^{B0} is the status quo's leaf distribution on the same tree. Default δ_α = δ = 0 for the recommendation, which approximates second-order dominance of B0 at three tail levels; δ = 0.01·W₀ (≈0.23pp a year in the worst decile) and above are frontier points (§4.8) [A]. One level alone (v1.0) lets loss migrate into the 1% tail while CVaR₉₀ stays fixed. (b) Absolute, per world: the class-banded CVaR₁₀ floor of SLIM G3 / ARCH §5.2, restated for 5 years, with buffers tuned so it holds out of sample (SLIM G3) [A] | [I]; LIT §3.2; SLIM §3.5 |
| H11 | Overcommitment | Private NAV + unfunded ≤ 0.80W. If violated at t0, it follows a glide path: non-increasing along every path, and met by year 2 at BEN and DRT nodes. STR nodes are exempt for one year, so the row cannot force red sales in a crisis [RV-19] | SYN §4.9 (LR8); L15 glide path |
| H12 | Concentration | Company ≤ 1% of NAV; GP ≤ 5% of private NAV + unfunded; co-investment position ≤ 4% | GRP §3.0, §3.4 |
| H13 | Overlay | Tail budget 0.15–0.50% of NAV a year; OV1 (economic vega ≥ 0.75 × the tail sleeve's) and OV2 (offset ratio ≤ 25%) on precomputed revaluations; opportunistic IM ≤ $1.5bn; gross overlay ≤ 0.30W | SYN §4.6; GRP §3.7 |
| H14 | Admissibility | R1–R5; consents; lead times (facility from stage 1, calls from the next year); notice dates; contingent gates | §1.2; GRP §3.0 |
| H15 | Horizon rows | At leaves: H2, H5, H6; no new borrowing; non-red liquidity ≥ next year's draw + stressed net calls; every financing claim deducted at fair value (§4.1) | TD verify_finance H1 |
| H16 | Fan discipline [RV-07] | In fan years only need-based funding moves are allowed. Gross sales of any sleeve are ≤ that year's required outflows plus floor restoration; there are no purchases beyond contractual calls; and forced deleveraging (cutting synthetic beta) is allowed to meet H5 and G5. Fans are buy-and-hold in dollars (a constant mix would be bilinear). This bounds the clairvoyance of path-specific funding (error ledger E2) | [I] |

### 4.7 Anti-gambling guards

- **G1, objective.** GBO is icx-monotone (P2): no mean-preserving gamble is rewarded. It is still a linear hinge (Remark 1), so G2, G4 and G5 are load-bearing. No indicator term appears in GBO or in the CRRA comparison, and the MILP is labelled a comparison, never the recommendation [R: ARCH §5.2] [RV-03].
- **G2, depth guard (H10, multi-level).** Improvements must come from the body of the distribution, not from a deeper tail at the 10%, 5% or 1% level. δ is the IC's lever on the frontier; the recommendation uses δ = 0.
- **G3, exponent.** Every shortfall *penalty* added to an objective (the CRRA comparison's L2 term, any tie-break) has exponent > 1, since linear shortfall reproduces probability maximization [R: LIT §4.7, Krabichler et al.]. GBO's own hinge is linear. This override of ARCH §5.2's rule (S-ADR-06) is disclosed, as SLIM §2.4 does, and is compensated by G2 and the mandatory CRRA tie-break [RV-03].
- **G4, no doubling down [RV-11].** Node n is *behind* if the status quo's cumulative TWR to n trails the goal path by more than 2pp. It is *thin* if its class is DRT or STR, or the status quo's Treasury/NAV there is below 6% [A]. A *loss year* means the status quo's return on the branch into n is negative. All three tests are exogenous, so the rule stays linear.
  - After a loss year, or when behind (thin or not), exposure may not rise as a share of wealth: E_n ≤ E_{parent}·(W^{B0}_n/W^{B0}_{parent}). In dollar terms, v1.0's "not above the parent's" let leverage rise after a loss, which is the G6 signature itself.
  - LEVER balances and illiquid ADDs may not exceed the parent's in dollars [R: SLIM G5].
- **G5, cushion-monotone caps [RV-11].** Three linear rows, all of which must hold:
  - **Class caps.** E_n ≤ L^class_n·W_n, with L^class 1.30 at BEN, 1.15 at DRT and 1.10 at STR [A].
  - **Behind.** At behind nodes (G4) the cap is 1 + ½(L^class_n − 1): 1.15 at BEN, 1.075 at DRT, 1.05 at STR. A book that falls behind therefore de-levers toward 1.0× through forced deleveraging of synthetic beta, which is not a red sale. That makes ARCH's hard signature "leverage at the cap while behind" impossible by construction. With class caps alone, GBO in STRETCH would sit at 1.30× at behind BEN nodes, and A14 would block its own change list.
  - **Liquidity cushion.** Borrowed exposure L^bor_n (with L^bor_n ≥ E_n − W_n and L^bor_n ≥ 0) satisfies L^bor_n ≤ κ_c·max(0, −m^{red,B0}_n) [A: κ_c = 1]. Here −m^{red,B0}_n is the status quo's non-red liquidity cushion net of the next 12 months' required outflows, i.e. the H9 margin evaluated on B0's path. The right side is therefore exogenous and never negative.
    - This is the research's cushion-monotone rule, with the cushion read as liquidity slack as in SYN §4.8, so leverage goes to zero as stress consumes capacity [R: SYN §4.8; ARCH §5.2, §5.10].
    - Reading the policy's own margin instead would make the row force sales exactly where H9 binds.

  At STR nodes the class cap is met within four quarters, not instantly, so it does not force deleveraging at the bottom.
- **G6, signatures, out of sample:** Sarle's bimodality coefficient on terminal TWR (flag > 0.555) [S: Pfister et al. 2013] with Hartigan's dip test [S: Hartigan & Hartigan 1985]; pile-up mass at the goal; P(goal) rising with a flat median; leverage rising after losses; leverage at the cap while behind; reaching for yield [R: ARCH §5.2]. Any flag on the GBO policy, for the playbook or the rolling-MPC policy, blocks the change list (test A14).
- **G7, dominance certificate.** Does the policy's out-of-sample terminal wealth second-order dominate the status quo's, by LPM₁ at every threshold? "Yes" means every risk-averse investor prefers it [S: Dentcheva & Ruszczyński 2003]. The strict frontier point imposes dominance in the LP, one row per benchmark leaf value [S: Dentcheva & Ruszczyński 2006]. A δ > 0 point cannot pass when its H10(a) row binds: the policy's worst-decile mean wealth is then below B0's, which fails the dominance condition at the 10% level [I] [RV-05].

**Guard numbering against SLIM §3.5 [RV-23].** The reports use SLIM's numbers and show this document's in brackets.

| SLIM | Here |
|---|---|
| G1 Tier 1 | H1–H8, H11–H16 |
| G2 Red events | H9 |
| G3 Downside floor | H10(b), and H10(a) multi-level |
| G4 Depth-aware objective | G1 (GBO) |
| G5 No doubling down | G4, G5 |
| G6 Gambling detector | G6 |
| G7 Leverage doctrine | §3.4 LEVER card, G5 |
| G8 Out of sample | §5.5 |
| G9 Feasibility first | Phase I (§4.3) |
| — | G3 exponent, G7 dominance |

### 4.8 The frontier

- **Grid.** ε_R ∈ {0.5%, 1%, 2%} (certified levels; the tree buffer is tuned to each) × δ ∈ {SSD, 0, 0.01, 0.02, 0.04·W₀, unbounded}, i.e. ≈{—, 0, 0.23, 0.45, 0.9pp a year, ∞}. GBO runs at every point, the MILP at ε_R = 1%.
- **Further sensitivities** [RV-09, RV-19]: the class leverage caps scaled to {1.00, 1.10, 1.20, 1.30} at BEN; ADR-39 relaxed to allow planned red-tier sales in Amber at bids ≥ 0.9 × normal, which is likely the largest single driver of t0 SELL value and an IC governance choice, not a model choice; IC ranges hard against elastic.
- **Plot (out of sample).** P(goal) against CVaR₁₀ of 5-year TWR, coloured by P(red), labelled PLAN or STRETCH, with the baselines marked. The plot also draws **the risk-matched line** [RV-04]: B0 plus a synthetic-beta overlay at scales 1.00–1.60×, a measurement device that may exceed H5. A policy's *value at equal tail* is its vertical distance above this line at its own CVaR₁₀. Points below the line are risk taken less efficiently than plain beta.
- **What the line shows** [I-calc, SYNTHETIC bridge model, §0 finding 4]. Beta alone buys ≈+0.7pp of P(goal) per 0.01·W₀ of worst-decile wealth, so the δ = 0.04·W₀ point can show ≈+2.6pp, and the 1.15× DRT cap ≈+3.2pp, with no optimization at all. In the pilot, the mean-LP root decision's +6.9pp out-of-sample uplift over the status quo was +0.8pp at equal tail.
- **Decision.** The IC chooses (ε_R, δ), seeing the marginal ΔP(goal) per 0.1pp of tail on both the policy frontier and the risk-matched line.

---

## 5. Tree and simulation (components 2 and 4)

### 5.1 Generator (SYNTHETIC)

- **Regimes.** Three coupled chains: macro S ∈ {expansion, late-cycle, crisis, recovery} (semi-Markov; crisis dwell 6–18 months); exit window e ∈ {open, normal, drought, frozen}; oil-shock type Z ∈ {normal, boom, glut, demand bust, supply shock, Gulf war}. P(crisis | demand bust) ≥ 0.8 and P(crisis | glut) ≈ 0.15 [R: SYN §4.1].
- **Start (October 2026).** Drought 0.87, Gulf war ≈0.85, market calm; Brent starts from the futures strip, and the Gulf-war dwell is conditioned on time elapsed [R: SYN §4.1; RA §9.3].
- **Factors and tails.** Equity excess return, credit spread, rates, log Brent, the exit factor and **equity implied volatility** (a VIX-equivalent level, so the overlay and the opportunistic book see their tails) follow f_t = c_S + Af_{t−1} + D_SL_Sε_t, with ε ~ t₅ and R_s = (1 − ω_s)R₀ + ω_sR_crisis [RV-20].
  - Regimes move volatility, tails, cash flows, bids and availability, but not next year's mean, so there is nothing to time [R: TD verify_finance M2; SYN §4.8].
- **Worlds [RV-14].** Means are anchored to the CMAs of the worlds the prototype implements: M1, M2 and M6, pooled with IC weights (default equal, so the mixture is ≈8.5% geometric against the six-world 8.3% of §0 and §4.2). The tree samples worlds inside its stage-1 branching and clusters on pooled observables, so recourse cannot learn which world is true (SLIM §1.5). PLAN or STRETCH is labelled per world and pooled. Production pools all six worlds (SLIM). The misspecification worlds of §5.5 are separate, used out of sample only.
- **Economic and reported NAV.** Economic NAV follows the factor path through de-smoothed loadings. Reported NAV lags it through the smoothing engine, so θ_n = V/N is path-dependent: it falls in DRT and STR states, where tail-end θ is 0.75–0.80 and 0.65–0.70 [R: GRP §3.2]. Bids are set on economic NAV (§2.2), so crisis discounts partly pay for stale marks, as in the research [RV-10].
- **Synthetic truth ≠ belief model [RV-02].** The certification truth is generated by a model the fusion does not assume:
  - true α dispersion at 0.5× and 1.5× the FBE prior's (two variants);
  - group bias drawn around the bias prior shifted by +1 sd, with a regime-dependent component (forecasts more optimistic in drought);
  - stated 80% ranges covering 36–52% of outcomes [R: SYN L7];
  - secondary bids informative about true α only through the market anchor's own noise model, with a 50% informativeness variant.

  Each synthetic book (holdings, archive, marks, bids, true α) is regenerated from a fresh seed. Results are reported across K ≥ 8 books, and a **null-information placebo book** has true α independent of all three marks and of the bids.
- **Owner draw.** $d^{tgt}_y=\Pi_{[5\%,10\%]}(0.075+0.625\,FN_y)$, $d_y=\Pi(0.5d_{y-1}+0.5d^{tgt}_y)$.
  - Fiscal need is linear in Brent (kinks ≈$67 and ≈$23); the basis is opening-year NAV, paid quarterly; overrides 0.25–2% by shock type.
  - The 12-month draw from today is $9.9–10.8bn [R: SYN §4.7].
- **Private flows.** $D=(1-e^{-\delta\Delta})V$ on an effective-age clock (κ(e) = 1.2 / 1.0 / 0.6 / 0.5); $C=(1-e^{-\lambda\Delta})U$.
  - Exit multipliers m^D 1.25 / 1.0 / 0.45–0.50 / 0.30–0.35 and m^C 1.3 / 1.0 / 0.95–1.0 / 0.8, plus stress calls.
  - Credit cash: Private Credit 10% and Capital Solutions 7% of NAV a year; RA from its debt module [R: SYN §4.2; RA §4.5].
- **Market data per node.** Bids, spreads and availability by node class (§2), with bids keyed to θ_n.
- **Start-state stratification.** The stage-1 branching is stratified by shock type as well as class. Its ≥ 2 STR branches include at least one demand bust (triple wrong-way: draws up, equities down, exits shut) and one glut or high-draw state with calm markets, plus a Gulf-war continuation branch, because the three call on liquidity differently [R: SYN L3] [RV-06].

### 5.2 The tree: 10 × 8 × 8 fans = 640 leaves [RV-06]

| Stage | Construction | Probabilities |
|---|---|---|
| t = 0 → 1 | Simulate 20,000 one-year paths from the start state. Stratified k-means on observable features (regime posteriors, equity and portfolio returns, credit spread, Brent, implied volatility, PE distribution rate, draw rate) gives 10 branches, stratified by shock type (§5.1), at least 2 of them in STR. The belief-error driver (§3.3) is drawn here and held to the leaves | Cluster mass; tail strata oversampled with likelihood-ratio weights |
| t = 1 → 2 | From each stage-1 node, 2,000 continuations clustered into 8 children | As above |
| t = 2 → 5 (fan) | From each stage-2 node, 8 three-year paths, one drawn from each octile of the conditional 3-year return of the status-quo portfolio | p_n/8 each, before moment matching |

- **Rank rule.** A branching with K children can match a covariance of rank at most K − 1. So every branching needs K ≥ d + 1 children, where d is the number of drivers matched there: d = 8 at stage 1 (seven factors plus the belief error) and d = 7 at stage 2 and in the fans.
  - v1.0's 5 children and 4 fan paths could not meet its own ±2% and ±0.05 tolerances for six drivers. On a synthetic driver correlation (eigenvalues 2.56, 1.45, 0.99, 0.46, 0.36, 0.19), the best rank-4 match misses vols by up to 12.5% and correlations by up to 0.25; rank 3 misses by 15.5% and 0.41 [I-calc, SYNTHETIC].
  - The unmatched directions were riskless in the tree, so stage-1 and stage-2 decisions could hedge the specific children (in-sample optimism).
- **Moment matching.** At every branching, least squares adjusts branch values so the conditional means, covariances and equity skew of the d drivers (equity, credit, rates, Brent, exit factor, implied volatility, draw rate; plus the belief error at stage 1) match the generator: means ±1bp, vols ±2%, correlations ±0.05 [S: Høyland & Wallace 2001]. Residuals are reported per branching (A22).
- **No arbitrage.** The positive state-price test applies to the benchmark and factor assets (CMA lines, futures, the overlay templates) at each branching [S: Klaassen 2002; R: LIT §4.9]. It does not apply to alpha-bearing units: by construction their returns are not priced by the factors, which is what the belief-error driver and the trade caps (§3.3) control. v1.0's version would have failed whenever two units with the same loadings had different μ̂ [RV-01].
- **Fan recourse rule (buy-and-hold).** Each leaf path inherits its stage-2 node's holdings, pacing, overlay and beta in dollars. Only need-based funding moves are path-specific, under H16: Treasury use, pro-rata long-only sales, hedge-fund notices, the revolver within availability, amber sales and forced deleveraging. Discretionary actions therefore cannot exploit foresight, and the clairvoyance left in funding moves is bounded by H16 and measured out of sample (E2).
- **Resolution.** Average leaf mass is 0.16%; the pack reports the effective number of leaves, 1/Σp_ℓ², and the leaf mass inside each CVaR level of H10 (the 1% level must contain at least 6 leaves).
- **Stability.** Five tree seeds are run. Besides in-sample stability (A11), the five root decisions are evaluated on the *same* fresh paths: their out-of-sample P(goal) must agree within 1pp (Kaut–Wallace out-of-sample stability). The Mak–Morton–Wood optimality-gap estimate is reported, as ARCH A4 requires.

### 5.3 Size and solve budget

- **Scale.** ≈250 units (PE 60, Secondaries 25, co-investment 45, Capital Solutions 20, Private Credit 15, RA 30, hedge funds 20, long-only 8, ≈27 opportunity units), about 450 positions with the small ones cohorted (SLIM §0); 91 decision nodes; 640 fan paths.
- **Columns [RV-06, RV-23].** Per unit at the root and the 10 stage-1 nodes. At the 80 stage-2 nodes, per cohort basket: ≈40 cohorts, each trading a fixed basket at its t0 weights, so positions stay linear, with a non-negativity row per unit. This is SLIM §1.6's group-level recourse in linear form. Fan paths carry only funding moves (≈8 per fan year), with group values a linear map of the stage-2 positions.
- **LP.** ≈70–90k variables, ≈80k rows, ≈1.2M nonzeros, assembled in `scipy.sparse` and passed to `highspy` [R: ARCH §5.4].
- **Budgets [A].** 10–90 s per LP; 10–20 warm-started LPs for the bisection; the MILP ≤ 1,800 s on the same model or the stratified subtree (§4.4), with LP-tightened leaf bounds only if its gap stalls; about 50 GBO solves for switch-offs and the frontier, plus 128 for the Shapley table (§6.3); the whole pipeline × K synthetic books for the headline comparisons (§5.5).

### 5.4 Ten-year sensitivity

Fans run t = 3–10 under the same rule, with goal W₀·1.10¹⁰. A root decision that differs from the 5-year run is labelled "horizon-sensitive" (test A10).

### 5.5 Out-of-sample certification (component 4)

**Paths [RV-23].** A certification set of at least 10,000 fresh quarterly paths *per world* on its own seed, separate from the tree and from the §4.3 selection set, with common random numbers across policies. That is 30,000 pooled for M1, M2 and M6 (SLIM's 50,000 per world is the production setting).

**Truth [RV-02].** Truth is **sealed** and comes from the synthetic truth model of §5.1, which differs from the belief model.
- The headline comparisons (O1 against the baselines, H1–H4 and H6) repeat over K ≥ 8 independently generated synthetic books. Each book is regenerated, re-fused, re-solved and re-certified, and intervals are clustered by book, so one lucky draw of true α cannot carry the result.
- A posterior-draw mode (α ~ N(μ̂, σ²_post)) is reported beside it. Posterior mode confirms the beliefs by construction, so it is never the headline.
- The **null-information placebo book** is run through the same pipeline (A19).

**Policy executed.** The root decision is applied exactly. Then:
- **Years 1–2: RR1, nearest-node playbook.**
  - Each path maps to the nearest stage-1 node, then to its nearest child, by Mahalanobis distance on observable features within the regime stratum.
  - Decisions are applied in relative form: sell fraction, ADD and commitments as % of NAV, REFINANCE as % of capacity.
  - A projection restores the hard rows through the fixed waterfall, and every repair is logged.
- **Years 3–5:** the fan rule (H16).
- **Rolling MPC [RV-15].** Small trees are re-solved at years 1–2 against the original goal path, on ≥ 2,000 paths with common random numbers. This is enough to bound the playbook-versus-MPC difference in P(goal) to about ±1–2pp as a paired estimate; v1.0's 500 paths gave ±4.4pp unpaired. Both policies are reported. The headline names the policy it describes: the pre-committed playbook, which the IC adopts. A difference above 2pp, or a gambling signature in the re-solves (a time-inconsistent re-solve at a behind node is STRETCH, so it levers unless G5 binds), is flagged.

**Statistics.**
- P(goal) on exact TWR on economic NAV, with a Wilson 95% interval, and P(goal) on reported NAV beside it (§4.1).
- bPOE at the goal (10%), the floor (7%) and capital (0%).
- Mean and median TWR, and CVaR at 10%, 5% and 1%.
- P(red), with a one-sided Clopper–Pearson bound.
- Leverage paths, the gambling signatures and the dominance certificate.
- Paired differences against each baseline: McNemar test [S: McNemar 1947] and a bootstrap interval, clustered by synthetic book.
- **Value at equal tail**: P(goal) minus the risk-matched line's P(goal) at the same CVaR₁₀ (§4.8) [RV-04].
- The optimism gap, tree minus out-of-sample, with the number of candidate policies tried and Smith–Winkler shrinkage (ARCH §5.10).
- **Multiplicity [RV-24].** H1 (pooled, R1) is the primary test, and H1–H7 are Holm-adjusted as one family. Per-world and per-consent results are descriptive.

**Misspecification worlds.**
- M2-like and M6-like worlds;
- group bias +1 sd;
- hedge-fund α = 0;
- playbook slippage: a one-quarter delay and 50% fills [R: ARCH §5.10].

---

## 6. Value-add demonstration (component 5)

### 6.1 Baselines

| Id | Policy | Rule |
|---|---|---|
| B0 | Status quo HOLD | Hold everything; plan pacing; draws from Treasury, then pro-rata long-only, then hedge-fund notices; red sales only when forced |
| B1 | Sell liquid first | Treasury → long-only → hedge funds → revolver (if signed) → amber → red; restore 8% |
| B2 | Pro-rata | Raise needs pro rata across liquid and amber sleeves; rebalance yearly to SAA |
| B3 | v8-style rule | Gate on IG + cash ≥ 8% and P99 margin + 12-month calls; hedge or amplify on F_t: exposure up to 1.30× when F_t < 0.17, down to 1.0× when F_t ≥ 0.34 [A; R: ARCH §5.10 controls; inputs §2] |
| B4 | Risk-matched leverage control [RV-04] | B0 plus a synthetic-beta overlay financed at SOFR + f, traced at scales 1.00–1.60× to give the risk-matched line (§4.8). The point matched to O1's CVaR₁₀ on the *selection* set is the control. It is a measurement device and may exceed H5 |
| P0 | Tuned standing policy | ARCH §5.10's cushion-monotone rule (about 20 parameters) tuned on the selection set: the research's "simple heuristic close to MPC" benchmark [R: SYN L10] |
| A, B, C | Archetypes | A: de-risking by secondary sales; B: synthetic DPI through REFINANCE (cash-out) plus tail monetization; C: opportunistic alpha expansion, with leverage along the cushion rule to its permitted maximum (ARCH §5.10; SLIM §1.7). Each is passed through the safety filter |

Baselines share the flows, limits, charges, tree and paths, with soft range edges [R: TD verify_finance H4]. **Facility parity [RV-21]:** under R1 and R2 every baseline has the same signed facilities, uses them before any red sale and pays the same fees. In the toy, about half the headline uplift was revolver access that the naive rule could not use [R: TD verify_finance H4].

### 6.2 Optimized policies

- **O1 is GBO, the recommendation, at (ε_R = 1%, δ = 0)** with the multi-level H10(a) rows. It improves P(goal) without a deeper tail than the status quo at the 10%, 5% and 1% levels [RV-05].
- O1 is also run at every frontier point (§4.8). Points with δ > 0 are shown as risk-for-probability trades for the IC to choose, each with its value at equal tail.
- O2 is the exact MILP; O3 is CRRA + L2, the current design.
- Each runs under three consent scenarios: R0, no revolver signed; R1, a revolver signed; R2, a revolver plus the owner band, i.e. pre-agreed 5% draws in CFP Red [R: SYN L4]. A card that flips between them is labelled consent-sensitive [R: ARCH §5.5].

### 6.3 Switch-off attribution by action family

O1 is re-solved with each family's columns fixed at zero or the status quo, and evaluated out of sample on the same paths.

| Family | Columns removed |
|---|---|
| F1 SELL | Planned secondary, asset and loan sales |
| F2 ADD | Re-ups, discount purchases, new money, co-investments |
| F3 REFINANCE | NAV facility, preferred, back-leverage, cash-out, P2S, unit loans, leaseback |
| F4a BETA [RV-04] | Synthetic beta and completion adds: risk budget, reported as risk taken, never as optimizer value |
| F4b LEVER (alpha-funded) | Portable alpha, hedge-fund TRS, acquisition debt, holdco PIK used as LEVER, SMA leverage |
| F5 PACE | Commitment budgets held at plan |
| F6 REDEEM | Hedge-fund and open-end notices |
| F7 HEDGE | Tail size and monetization at the status quo; opportunistic book fixed |
| F8 FUND | Revolver arrangement, draws, term debt |
| F9 REBALANCE | Cross-group moves (groups held at SAA weights) |
| F10 Beliefs | Fused μ̂ replaced by the group prior μ_k: the value of the three-mark fusion |

**Report per family:** ΔP(goal) with a 95% interval, ΔE[TWR], ΔCVaR₁₀, ΔP(red), Δ(value at equal tail), and the binding rows that change. Switch-offs do not sum when families substitute, so an exact Shapley value is also computed on CRN over seven grouped players (SELL + REDEEM, ADD + PACE, REFINANCE + FUND, BETA, LEVER, HEDGE, Beliefs; 128 coalitions, on the cohort model if the budget requires). Stand-alone attribution is never shown alone [R: ARCH §4.13].
- **Freed tail respent on beta [RV-04].** Families that free tail budget (FUND avoiding forced sales, HEDGE) can look valuable only because the freed budget buys beta. The table therefore shows each family's ΔP(goal) both raw and at equal tail.
- **Placebo [RV-02].** F10 is also run on the null-information placebo book, where its value must be indistinguishable from zero (A19).

### 6.4 The t0 change list

One row per root action with a nonzero size, sorted by |goal value|.

**Fields** (schema in §7.1):
- unit, group and segment; action and lens (R1);
- size in $bn and as % of the unit;
- p^ce, μ̂ (P10/P50/P90), h on the goal basis with the utility-view line, μ^BE and p\*, all read from the LP (§3.4);
- G_a per $;
- ΔP(goal) and ΔE[TWR] out of sample from a forced re-solve without the action, raw and at equal tail;
- binding rows with duals and the root ℓ;
- consent, lag, red status (ADR-39), the consent-sensitive flag, and tree-seed agreement (k/5).

**New flags [RV-04, RV-09, RV-19]:**
- `risk_budget` when the action's value disappears at equal tail;
- `limit_driven` when relaxing one IC limit (A20) changes the action's sign or its size by more than 20%;
- `goal_driven` when it passes on the goal basis but fails on the utility view.

**Red-tier sales at the root** are red events by ADR-39 in today's Amber stage. They appear only as forced-re-solve cards, with the ΔP(goal) and ΔP(red) of forcing them, never as planned rows.

**Format examples.** Values come from research worked cases (rows 1 and 3: SYN §4.4; row 2: GRP §3.6; row 4: RA §9.3); they are not prototype results.

| Unit | Action (lens) | Size | Price | μ̂ / μ^BE | p\* | Note |
|---|---|---|---|---|---|---|
| PE 2018 buyout fund | SELL | 100% | 0.88 | μ̂ ≈ μ^BE − 0.2pp [I] | 0.873–0.877 | Marginal; planned only at a Green BEN node with Treasury ≥ 8%; at the root it is a forced-re-solve card (ADR-39) |
| Private Credit SMA loans | SELL | $0.58bn | 0.99 | ℓ̄ > 0.8–1.0% | — | Restores the 8% target |
| Long-only DM equity | REFINANCE (P2S) | $5bn | 0.40–0.70% a year per $ freed | — | — | VM liability $1.65bn in a −33% month |
| ENR levered upstream fund | HOLD at a 0.80 bid | — | 0.80 | — | 0.87 with Mix B | NOT ESTABLISHED; sell only at ≥ the confirmed p\* |

### 6.5 Pre-registered hypotheses (sealed before the first out-of-sample run)

- **H1 (primary).** O1 beats B0 by ≥ +2pp of out-of-sample P(goal), paired p < 0.05 clustered by synthetic book, at δ = 0 with the multi-level depth guard, with P(red) ≤ 1% (Clopper–Pearson bound) [RV-05].
- **H2.** O1 beats the best of B1–B3, P0 and archetypes A–C by ≥ +1pp, paired p < 0.05.
- **H3.** H1 holds in sealed-truth mode across K ≥ 8 books whose truth model differs from the belief model, not only in posterior mode: the gain is real, not belief-confirming [RV-02].
- **H4.** No gambling signature on O1, for the playbook or rolling MPC, and the dominance certificate holds against B0 at O1's point (it can hold only at δ = 0 or at the SSD point; §4.7 G7).
- **H5.** O2's optimism gap exceeds O1's. The exact maximizer overfits the tree.
- **H6 (value at equal tail) [RV-04].** O1's P(goal) exceeds the risk-matched line's at O1's CVaR₁₀ by ≥ +1pp, paired p < 0.05. This is the test that beta cannot pass.
- **H7 (placebo) [RV-02].** On the null-information book, F10's value is within one paired SE of zero, and O1's value at equal tail is ≤ +0.5pp.
- **Multiplicity.** H1–H7 are Holm-adjusted as one family; per-world results are descriptive.

**Basis for the thresholds.** Evidence-central α\* plus the overlay is +0.75pp a year, against drags of 0.31–0.64pp [R: SYN §4.12]. In the §4.2 check, +0.1pp a year of drift is worth ≈+0.57pp of 5-year P(goal) [I-calc], so +0.3 to +1.0pp of captured drift maps to +2 to +6pp. The upper end is optimistic: B0 already earns the evidence-central α\* of what it holds, and today's Amber stage keeps root red-tier sales out of the plan, so a NOT ESTABLISHED outcome is plausible. A failed hypothesis is reported as NOT ESTABLISHED, with the attribution showing why [R: SYN L12].

**Why this design should show more than the toy.** The toy had no cross-section, no yield-book levers, no contingent ADDs, cheap liquidity and a CRRA objective [R: TD RESULTS §3, §10]. Here value can come from four places, each measured by its switch-off:
- belief-versus-bid selection across ≈250 units;
- pre-arranged REFINANCE and FUND that turn forced red sales into planned ones [S: Duffie & Ziegler 2003];
- counter-cyclical purchases at discounts above 20% [R: GRP §3.2], valued against economic NAV with path-dependent θ, and shown at θ = 0.75 and at zero edge [RV-10];
- cushion-gated beta at ≈30bp financing. This adds P(goal), but it is risk budget, not optimizer value, so it is reported separately and judged at equal tail [RV-04].

---

## 7. Output schema and acceptance checks

### 7.1 JSON (one file per run, `runs/<run_id>/decision_run.json`)

```json
{
  "meta": {"label": "SYNTHETIC - NOT ADIC DATA", "spec": "DSGO-1.1", "run_id": "str", "created": "ISO-8601",
           "seed_tree": 0, "seed_select": 0, "seed_cert": 0, "seed_books": [0], "code_sha": "str", "config_hash": "str",
           "solver": {"name": "HiGHS", "version": "str", "lp_method": "dual_simplex|ipm", "mip_gap": 0.005}},
  "config": {"goal": {"rate": 0.10, "years": 5, "basis": "TWR_gross_of_distributions_on_economic_NAV",
                      "W0_bn": 177.0, "Wstar_bn": 285.06},
             "objective": "GBO|MILP_PGOAL|CRRA_L2", "c_max_W0": 3.22,
             "eps_red_certified": 0.01, "eps_red_tree": 0.006,
             "depth_guard": {"levels": [0.90, 0.95, 0.99], "delta_W0": 0.0},
             "cushion": {"class_caps": [1.30, 1.15, 1.10], "behind_cap_rule": "1+0.5*(L_class-1)", "kappa_c": 1.0},
             "consent_scenario": "R0|R1|R2", "consent_defs": {"R0": "no revolver", "R1": "revolver signed",
                                                              "R2": "revolver + owner band (5% draws in CFP Red)"},
             "theta_star": 0.58, "worlds": {"M1": 0.3333, "M2": 0.3333, "M6": 0.3333},
             "truth_model": {"alpha_dispersion_x": [0.5, 1.5], "bias_shift_sd": 1.0, "bid_informativeness": [1.0, 0.5],
                             "books_K": 8, "placebo_book": true},
             "tree": {"branches": [10, 8], "fan_paths": 8, "fan_years": 3, "matched_drivers": [8, 7, 7]}},
  "book": {"as_of": "2026-09-30", "units": [{"unit_id": "PE-017", "group": "PE", "segment": "buyout_mid",
           "vehicle": "LP", "control": "LP", "nav_rep_bn": 0.0, "nav_econ_bn": 0.0, "unfunded_bn": 0.0, "age_y": 0.0,
           "bid": {"p_ce": 0.0, "source": "external|segment", "node_class": "DRT"},
           "marks": {"underwritten": {"moic": 0.0, "irr": 0.0}, "actual": {"tvpi": 0.0, "irr": 0.0},
                     "forecast": {"p10": 0.0, "p50": 0.0, "p90": 0.0, "as_of": "date"}},
           "belief": {"mu_hat": 0.0, "sigma_hat": 0.0, "nu": 5, "p10": 0.0, "p90": 0.0,
                      "loadings": {"equity": 0.0, "credit": 0.0, "rates": 0.0, "oil": 0.0, "exit": 0.0},
                      "weights": {"prior": 0.0, "f": 0.0, "u": 0.0, "a": 0.0, "m": 0.0}, "bias_applied": 0.0, "flags": []},
           "admissible": ["SELL", "HOLD", "ADD", "REFINANCE", "PACE"], "consents": {"transfer": true, "pledge": false}}]},
  "tree": {"nodes": [{"id": "0", "parent": null, "stage": 0, "prob": 1.0, "class": "DRT", "draw_rate": 0.058,
            "features": {}}], "leaves": [{"id": "0.3.2.f1", "node": "0.3.2", "prob": 0.0}],
           "checks": {"moments": {}, "rank_rule": true, "arbitrage_free_factor_assets": true, "effective_leaves": 0.0,
                      "leaves_in_cvar99": 0, "oos_stability_pp": 0.0, "mmw_gap": 0.0}},
  "solutions": {"GBO": {"label": "PLAN|STRETCH", "phi": 0.0, "bpoe_tree": 0.0, "p_goal_tree": 0.0, "E_Wtilde_W0": 0.0,
                        "root_actions": [], "node_actions": [], "leaf_Wtilde_W0": [],
                        "binding_rows": [{"row": "H5.leverage@0", "dual": 0.0, "slack": 0.0, "range": [0.0, 0.0]}],
                        "ell_by_node": [{"node": "0", "ell": 0.0}], "goal_kernel": []},
                "MILP": {"p_goal_tree": 0.0, "mip_gap": 0.0, "time_s": 0.0, "pileup_mass": 0.0, "deep_miss_mass": 0.0},
                "CRRA": {"ce_bn": 0.0}},
  "oos": {"paths_per_world": 10000, "truth": "sealed|posterior", "books": 8,
          "policies": [{"id": "O1", "policy_kind": "playbook|rolling_mpc", "world": "pooled|M1|M2|M6",
          "p_goal": 0.0, "p_goal_ci95": [0.0, 0.0], "p_goal_reported_nav": 0.0,
          "bpoe": {"goal": 0.0, "floor7": 0.0, "zero": 0.0}, "twr_mean": 0.0, "twr_median": 0.0,
          "cvar_twr": {"10": 0.0, "5": 0.0, "1": 0.0},
          "p_red": 0.0, "p_red_cp95": 0.0, "lev_max": 0.0, "bimodality": 0.0, "dip_p": 0.0, "ssd_vs_B0": true,
          "value_at_equal_tail": {"dp_goal": 0.0, "ci95": [0.0, 0.0]},
          "paired": {"B0": {"dp_goal": 0.0, "ci95": [0.0, 0.0], "mcnemar_p": 0.0, "holm_p": 0.0}}, "optimism_gap": 0.0,
          "recourse_repairs": 0.0}],
          "risk_matched_line": [{"beta_scale": 1.0, "p_goal": 0.0, "cvar10_twr": 0.0}],
          "placebo": {"F10_dp_goal": 0.0, "O1_value_at_equal_tail": 0.0}},
  "attribution": {"switch_off": [{"family": "F1_SELL", "dp_goal": 0.0, "dp_goal_equal_tail": 0.0, "ci95": [0.0, 0.0],
                  "dtwr_mean": 0.0, "dcvar10": 0.0, "dp_red": 0.0}],
                  "shapley": [{"player": "SELL+REDEEM", "phi_p_goal": 0.0, "se": 0.0}]},
  "change_list": [{"unit_id": "str", "group": "str", "action": "str", "lens": "SELL", "size_bn": 0.0, "size_pct": 0.0,
                   "p_ce": 0.0, "mu_hat": [0.0, 0.0, 0.0], "hurdle_goal": 0.0, "hurdle_utility": 0.0,
                   "mu_be": 0.0, "p_star": 0.0,
                   "goal_value_per_usd": 0.0, "dp_goal_forced": 0.0, "dp_goal_forced_equal_tail": 0.0,
                   "dtwr_forced": 0.0, "binding_rows": [],
                   "consent": "str", "lag_q": 0, "red_event": false, "consent_sensitive": false,
                   "risk_budget": false, "limit_driven": false, "goal_driven": false,
                   "tree_seed_agreement": "5/5"}],
  "frontier": [{"eps_red": 0.01, "delta_W0": 0.0, "objective": "GBO", "label": "STRETCH", "p_goal_oos": 0.0,
                "cvar10_twr": 0.0, "p_red": 0.0, "twr_mean": 0.0, "value_at_equal_tail": 0.0}],
  "checks": [{"id": "A1", "value": 0.0, "threshold": 0.0, "pass": true}]
}
```

### 7.2 Acceptance checks

| Id | Check | Pass criterion |
|---|---|---|
| A1 | Identities: cash, NAV, unfunded and debt at every node and leaf, recomputed from published values | Residual ≤ 10⁻⁸·W₀ |
| A2 | Owner draw paid at every node, every fan year and every out-of-sample quarter | Zero shortfall |
| A3 | Every hard row H1–H16 at every node, fan year and leaf | Slack ≥ −10⁻⁷ (HiGHS feasibility tolerance) |
| A4 | Lens labels reproduce R1's closed form on every node (total B including B^syn and B^sf; calls on t0 commitments excluded from ΔE^disc), and the §2 relabels hold (deferred purchase = LEVER, run-off = SELL, holdco PIK by use) | 100% |
| A5 | GBO value against `stats.bpoe` on the leaf distribution, read-only | Equal to within 10⁻⁶ when Φ < 1 |
| A6 | The degeneracy unit test reproduces the §4.2 table. The STRETCH solution attains the mean LP's optimal value, and the leaf condition max W̃_ℓ ≤ W\* + c_max·W₀ is reported. Solutions are compared by objective, not by ‖x − x_mean‖, because LP optima are not unique | Table within MC error; \|E[W̃] − E\*[W̃]\| ≤ 10⁻⁶·W₀ |
| A6b | The complete-market check of Remark 1 reproduces the two-valued bPOE optimum and the smooth squared-shortfall optimum | Two levels; ≥ 100 levels |
| A7 | The bisection agrees with the perspective LP; a_min does not bind in PLAN | Φ within the bisection tolerance + 10⁻⁶; flag otherwise |
| A8 | MILP: big-M valid (the 77% one-year-loss check for L_ℓ = 0), gap and free binaries reported, MIP start accepted | All hold; a gap above 2pp triggers the subtree |
| A9 | Duals: finite-difference re-solves on ≤ 10 pricing rows; ℓ only from a feasible problem (Phase I u\* = 0) | Relative error ≤ 10⁻⁴ |
| A10 | Horizon: root actions stable from 5 to 7 years, at 10 years, and under ±50% changes in ω and ψ | Same sign; size within 20%, else labelled |
| A11 | Tree stability across 5 seeds (in sample) and on common fresh paths (out of sample); moment matching and no-arbitrage on factor assets at every branching | ≥ 4 of 5 agree, else "tree-sensitive"; out-of-sample P(goal) within 1pp; §5.2 tolerances; MMW gap reported |
| A12 | Out-of-sample precision | P(goal) 95% half-width ≤ 1pp per world |
| A13 | Switch-off and Shapley tables complete, raw and at equal tail, with the interaction residual | All families |
| A14 | No gambling signature on O1, for the playbook or rolling MPC (§4.7 G4–G6) | Otherwise the change list is blocked |
| A15 | H1–H7 reported with raw and Holm-adjusted p-values, failures included | Present |
| A16 | SYNTHETIC labels; determinism (same seeds, same hash) | 100%; identical |
| A17 | Budgets: LP ≤ 120 s; MILP ≤ 1,800 s, with its gap | Logged |
| A18 | Every root action carries every §6.4 field | 100% |
| A19 | Placebo [RV-02]: the null-information book runs the full pipeline | F10 within 1 paired SE of zero; O1's value at equal tail ≤ +0.5pp |
| A20 | Limit sensitivity [RV-19]: each IC-set limit (group ranges, the 8% target, H11, the class caps, ε_R, δ) relaxed one at a time and re-solved; out-of-sample ΔP(goal) reported | Any limit moving P(goal) by > 1pp is named in the report, and its actions are flagged `limit_driven` |
| A21 | Truth replication [RV-02]: headline comparisons over K ≥ 8 books, truth model ≠ belief model | Intervals clustered by book; the per-book spread is reported |
| A22 | Rank and moments [RV-06]: K ≥ d + 1 children at every branching; matching residuals; ≥ 6 leaves inside the 1% CVaR level | All hold |
| A23 | Card–LP consistency [RV-08]: every root column's card (h, μ^BE, p\*, LEVER test) agrees in sign with the LP's choice | 100% |
| A24 | Valuation basis [RV-18]: P(goal) on economic and on reported NAV; tree and simulator use the same leaf valuation and deduct every financing claim | Gap reported; > 2pp in favour of reported NAV is flagged |

**Error ledger:** E1, affine W̃ against exact TWR; E2, the fans' funding clairvoyance under H16; E3, playbook against rolling MPC (≥ 2,000 paired paths); E4, the MILP's subtree, when used (GBO on the full tree against the subtree); E5, belief risk in the tree (one driver) against the simulator's full idiosyncratic and belief noise.

---

## 8. Assumptions register

| [A] item | Default | Sweep | Owner |
|---|---|---|---|
| Goal and horizon | 10% TWR, 5 years | 10 years | Board / IC |
| c_max; depth guard δ and levels; red-event ε_R (certified / tree buffer) | 2W\*/W₀; δ = 0 at CVaR₉₀/₉₅/₉₉; 1% / 0.60% tuned | 1.0–5.0; frontier 0–0.04·W₀; 0.5–2% | TPA; IC; CRO |
| Guard thresholds (behind, thin, class caps, behind cap, cushion slope κ_c) | 2pp; 6%; 1.30 / 1.15 / 1.10; 1 + ½(L^class − 1); 1.0 | 1–4pp; caps 1.00–1.30; κ_c 0.5–2 | CRO / IC |
| Unfunded burden ψ; liquidation-basis ω | $0.02–0.05 per $; ω = 1 on economic NAV | 0, 0.10; ω = 0.90 after a crisis | TPA |
| Secondary inputs (y_b; buyer residual ρ on economic NAV by BEN / DRT / STR; θ_n) | 14 / 18 / 22%; 0.98–1.02 / 0.96–1.00 / 0.80–0.84; from the smoothing engine | ±3pp; θ = 0.75; zero-edge placebo ρ = 1 | Secondaries (external prices only) |
| Belief risk in the tree (ρ_g; per-unit trade cap k_sel) | from archive credibility; 0.5% of W₀ at median σ_post | ρ_g 0–1; k_sel 0.25–1% | CRO office |
| World weights; synthetic books K; truth-model variants | M1 / M2 / M6 equal; K = 8; α dispersion ×0.5 and ×1.5, bias +1 sd, bid informativeness 1.0 and 0.5 | IC weights; K = 16 | IC; CRO office |
| Tree shape | 10 × 8 × 8 (rank rule) | 10 × 9 × 8; MILP subtree 10 × 8 × 2 | CRO office |
| IC range breach charge | 50bp a year per $ outside 0.5–1.5× SAA; waived at STR | 0–200bp; hard | IC |
| PE pace at v2; term-debt spread | $3.5bn a year; SOFR + 70–100bp | $5.34bn; +150bp | CIO; Corporate Finance |
| Node classes; co-investment sale cap; 6-month coverage | §1.1; 10% of group NAV a year; §4.6 H3 | Cut-offs; 5–20%; 3–9 months | CRO; Co-investment; Treasurer |

Every [A] item lives in the run's parameter file with its value, source, rationale and owner, as in the demo's `params.json`. The pack's "what moves the answer" table re-solves each sweep [R: TD RESULTS §7].

**References not yet in the research corpus,** for the citation pass: Dentcheva & Ruszczyński 2003 (*SIAM J. Optim.* 14(2)) and 2006 (*J. Banking & Finance* 30(2)); Rockafellar & Royset 2010 (*Reliab. Eng. Syst. Saf.* 95(5)); Shang, Kuzmenko & Uryasev 2018 (*Ann. Oper. Res.* 260); Hartigan & Hartigan 1985 (*Ann. Stat.* 13(1)); Pfister et al. 2013 (*Front. Psychol.* 4); McNemar 1947 (*Psychometrika* 12); Kaut & Wallace 2007 (*Pacific J. Optim.* 3(2), scenario-tree stability); Mak, Morton & Wood 1999 (*Oper. Res. Lett.* 24, optimality-gap estimator); Smith & Winkler 2006 (*Management Sci.* 52(3), optimizer's curse). Browne, Föllmer–Leukert, Roy, Høyland–Wallace, Klaassen and Krabichler et al. are already cited in the research clusters and dossiers.

---

## Review changes (v1.0 → v1.1)

The adversarial quant review in `examples/mpo_v2/spec_review.md` found 24 issues: 3 critical, 7 high, 12 medium and 2 low. Each change is tagged [RV-nn] where it occurs. *SYNTHETIC – NOT ADIC DATA:* every number quoted below comes from synthetic checks in `examples/mpo_v2/review_checks/`.

| RV | Change | Where |
|---|---|---|
| 01 | A belief-error driver and per-unit trade caps put belief risk in the tree; no-arbitrage is tested on factor assets only. Without them, equal-loading units with different μ̂ formed riskless spreads, and the v1.0 check could not pass | §3.3, §5.2 |
| 02 | The certification truth comes from a model different from the fusion's. Headline comparisons run over K ≥ 8 regenerated books with intervals clustered by book. A null-information placebo book is added (H7, A19, A21). Posterior mode is never the headline | §0, §5.1, §5.5, §6.3, §6.5, §7.2 |
| 03 | GBO's "cannot gamble" claim is narrowed to mean-preserving spreads. Remark 1 shows a two-valued, all-or-nothing bPOE optimum in a complete market. H10(a) is now multi-level (CVaR₉₀/₉₅/₉₉); G1 and G3 are restated and the override of ARCH's exponent rule is disclosed; the CRRA tie-break is mandatory | §0, §4.2, §4.3, §4.6, §4.7 |
| 04 | New risk-matched control B4 (B0 + synthetic beta) and the risk-matched line; value is measured at equal tail. F4 is split into BETA and alpha-funded LEVER; new hypothesis H6. In the pilot, a +6.9pp uplift was +0.8pp at equal tail | §0, §2.6, §4.3, §4.8, §5.5, §6.1, §6.3, §6.5 |
| 05 | The recommendation O1 moves to δ = 0, multi-level. A δ > 0 point cannot pass SSD (G7) once its depth row binds, so H1 and H4 now sit at the same point | §4.6, §4.7, §6.2, §6.5 |
| 06 | The tree becomes 10 × 8 × 8 = 640 leaves under a rank rule (children ≥ matched drivers + 1). v1.0's 5 and 4 could not match its own tolerances: on a synthetic correlation the vol errors were 12.5% and 15.5%. Stage 1 is stratified by shock type; out-of-sample stability and the MMW gap are added | §0, §5.1–§5.3, §7.2 |
| 07 | Fan years are constraint nodes for every row, including H9's red margin. Leaves deduct every financing claim at fair value. New H16 limits fan funding to need-based moves and makes fans buy-and-hold | §1.1, §4.1, §4.6, §5.2 |
| 08 | Card hurdles come from the LP's goal kernel (h = r_f + ℓ̄ + κ^G), with the CMA-premium version kept as a "utility view". The LEVER card is read additively per ADR-49 against κ^G. Flip thresholds come from parametric re-solves; new test A23 | §3.4, §6.4 |
| 09 | The red event follows ADR-39 in full, including the stage test. Root red-tier SELL columns are held at zero and shown by forced re-solve. "ADR-39 relaxed in Amber" is an IC sensitivity | §1.1, §3.4, §4.6, §4.8, §6.4 |
| 10 | Secondary purchases are priced from one primitive (a buyer residual on economic NAV) with path-dependent θ, plus a zero-edge placebo and a θ = 0.75 sensitivity | §2.2, §5.1, §6.5 |
| 11 | G5 becomes cushion-monotone: class caps, a behind cap of 1 + ½(L^class − 1), and borrowed exposure ≤ the liquidity cushion. G4 binds in ratio terms and on "behind" alone | §1.1, §4.7 |
| 12 | R1 has a closed form, LEVER = min(ΔB⁺, ΔE^disc⁺), and B includes seller and derivative financing. Relabelled: deferred-payment purchase → LEVER, SMA run-off → SELL, holdco PIK and term debt by use; FUND = capacity only | §1.1, §1.2, §2 |
| 13 | The comparison MILP has only goal binaries (R4 is exact only in Level-B restoration). The big-M default is L_ℓ = 0 with a validity check. Pilot: 200 binaries closed in 65 s; subtree fallback | §1.2, §4.4, §5.3 |
| 14 | One world set: M1, M2 and M6 pooled in the tree with IC weights, labels per world; misspecification worlds are separate | §5.1 |
| 15 | Playbook and rolling MPC are both certified, MPC on ≥ 2,000 paired paths; re-solves keep the original goal path | §4.3, §5.5 |
| 16 | The tie-break tolerance is defined per case (PLAN, STRETCH, ĝ\*(p)) | §4.3 |
| 17 | GBO's exactness condition (max W̃ ≤ W\* + c_max·W₀); c_ℓ and g_ℓ defined; tolerances made consistent with HiGHS and the bisection; A6 compares objective values | §4.3, §7.2 |
| 18 | The goal is measured on economic NAV, with reported-NAV P(goal) shown beside it. The leaf ω no longer counts the crisis twice; the pacing charge is counted once; tree and simulator value leaves identically (A24) | §4.1, §5.5, §7.2 |
| 19 | IC ranges are elastic and priced (SLIM §5.4); H11 becomes a glide path; A20 relaxes each IC limit one at a time and flags `limit_driven` actions; the frontier adds the cap scale | §2.10, §4.6, §4.8, §6.4, §7.2 |
| 20 | Implied volatility is added as a driver, so short-volatility and overlay tails are in the tree | §5.1, §5.2 |
| 21 | Facility parity: every baseline uses the same signed facilities before red sales | §6.1 |
| 22 | ε_R in the tree is a tuned buffer (default 0.60%) certified to 1% out of sample | §4.6 |
| 23 | Aligned with SLIM: guard-numbering map, paths per world, unit and leaf counts, group-level recourse in linear form, consent scenario R2 defined | §4.7, §5.3, §5.5, §6.2, §7.1 |
| 24 | H1 is primary; H1–H7 are Holm-adjusted | §5.5, §6.5 |

**Unchanged and confirmed.** The bPOE identity and its LP form (Rockafellar–Royset; Mafusalov–Uryasev); Propositions 1–3; the §4.2 lognormal table (re-derived analytically: 40.4%, 46.0%, 52.6%; bPOE 0.969 and 0.910; c\* 1.76 and 0.92); the big-M construction; the selection/certification split; and the action economics against SYN §4.4, GROUPS §3 and RA §7, apart from the relabels in RV-12.
