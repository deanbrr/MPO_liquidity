# Group gap 03 addendum: the Overlay (Group 7) at parity with the other groups

**Action sets, schema, service transfer pricing, ex-ante DVA and one reconciled sizing**

- **Date:** 2026-10-18. **Closes:** group gap 03. Group 7 had no S/H/R/L action set, attribution convention or verification stream.
- **Amends** `01_GROUPS_SYNTHESIS.md` §2.2, §3.7 (replaced by §2), §3.8, §4.3, §6 and §7.1, and main §4.6 governance.
- **Status.** This file is the G-stream-equivalent dossier ("G10, Overlay organization"). §7 is its adversarial verification log.
- **Computation.** `gap_03_calcs/gap03g_overlay_calcs.py` → `gap03g_overlay_results.json`, run in the project venv with `python -I`. It loads the unmodified stream-G7 module and the GS cash-map results. Public inputs: Cboe SPX, VIX, VIX3M, VIX6M, VIX1Y and SKEW to 16 Oct 2026; the Fama–French T-bill series (CRSP 202608).
- **Tags** as in groups synthesis §0.

> **SYNTHETIC-DATA NOTICE.** Every ADIC notional, payoff, charge and cash flow below is synthetic or [I-calc], never ADIC data. *SYNTHETIC – NOT ADIC DATA* applies to every table with [I-calc] figures.

---

## 1. Findings

1. **S/H/R/L is well defined for all three books, once REFINANCE is read as "raise cash, keep the exposure".**
   - *Tail:* monetize or restrike; roll; restructure or transform collateral; add layers.
   - *Opportunistic:* cut; hold; optimize IM; scale.
   - *Synthetic beta:* cut; roll; switch instrument; add beta.

   Each action is scored with main §4.4. It is admissible only if gap_03's L1–L3 still hold after the trade.
2. **The §2.2 overlay row has four inconsistencies. Reconciled, its stress use falls from −$6.0bn to −$4.0bn** [I-calc]:
   1. It runs $15bn of synthetic beta in every column, although the text sets $10bn at t0.
   2. If the extra $5bn is Red-stage P2S, the $5bn of sale proceeds are missing; the tranche nets **+$2.7bn** over the S1 year.
   3. Its −1.5%-of-NAV opportunistic loss breaches L2 even against its own ladder, where the cap is $0.88bn.
   4. Its $20bn ladder at 0.4% of NAV is 2.7× the IC floor.
3. **One price settles the sizing.** On 16 Oct 2026 prices, a 90/72 put-spread ladder costs **3.74%** of outstanding notional a year: 3.47–3.96% across skew assumptions, against G7's implied 3.54%.
   - The 0.15% floor ($0.27bn) buys **$7.1bn** of notional, which pays ≈$1.2bn in S1.
   - The 0.5% cap buys $23.6bn.
   - G9's ≈$25bn stack would cost ≈0.53% of NAV, above the cap. It stays a test fixture only.
4. **For services, the client bears exposure and liquidity; the Overlay bears execution and basis; Corporate Finance (CF) bears funding.**
   - This booking nets to zero at machine precision on 2,000 paths (gate V2).
   - The naive booking double counts **−$7.05bn** over the S1 year.
5. **Ex-post crediting manufactures hedge fatigue.** A floor ladder replayed over 2010–2025 shows negative annual DVA in **11 of 16 years**, with a four-year run (2021–24) and a peak-to-trough loss of 6.2 years of budget. Held to expiry, it is negative in 16 of 16 years [I-calc].
6. **Ex-ante kernel crediting fixes timing and ownership.**
   - Kernel value plus liquidity and enabling credit is 0.62–0.64 per $ of premium (c_buf parity or G8's E1 duals).
   - That leaves a predictable **IC policy residual of ≈−$96m a year at the floor** (−$319m at the cap).
   - The desk is paid on implementation against a reference ladder.
7. **Peers agree** [S].
   - CalPERS's tail programme "did not have a customized benchmark" before it was cut.
   - NZ Super judges Portfolio Completion against benchmarks.
   - CPP shows no benchmark return for its completion portfolio.
8. **The tail budget and the opportunistic book are one decision.**
   - Through L1 and L2, moving from floor to cap raises the opportunistic book's short VIX-vega allowance from ≈$1.0m to $3.4m per point, and its named-stress loss cap from $0.29bn to $0.98bn.
   - On a book starting in CFP Red, the opportunistic default is SELL, which releases ≈$1bn of IM.

---

## 2. Replacement text for groups synthesis §3.7, Overlay (Group 7)

**Mandate.** Listed and OTC derivatives in three books:
- a tail hedge and an opportunistic book, the two strategies of R10 [A];
- synthetic beta, which provides services to other groups and the total portfolio.

The group sources, prices, executes and monitors. It does not own:
- service exposures, which belong to the clients;
- the tail budget, which belongs to the IC;
- collateral, which belongs to CF.

### 2.1 Specification

| Item | Specification |
|---|---|
| **Holdings and schema** | **`overlay_trade`** (G9, extended). Book {tail, opp, beta}; `service_id`; `client_group` {TPA, PUB, PE, COI, PCR}; gap_03 template; strikes and expiry; premium; venue {listed, cleared, bilateral}; csa_id; rung; `s_lock`; hedged-position ids; trigger state; `is_synthetic`. **`crif_row`** (ISDA Risk Data Standards [S]). Keys: ProductClass, RiskType, Qualifier, Bucket, Label1, Label2. Amounts: Amount, AmountCurrency, AmountUSD. Also TradeID, PortfolioID (netting set), IMModel, EndDate. A blank PostRegulations / CollectRegulations entry exempts the row, which encodes a sovereign-exempt one-way CSA. **`csa`**: threshold, MTA, IA, eligible collateral, reuse right (sets φ), IM regime {two-way SIMM, IA-only}, documents (2016 VM CSA; 2018 IM CSA [S]). **`service`**: client, notional, reference index, s_lock, CLC basis |
| **State** | *Tail:* budget use; rungs; delta; $NV^{eq}(s)$; scenario payoffs; triggers; a fatigue tracker of premium, ex-ante credit and experience. *Opportunistic:* exposures or trades; vol and IM use; posterior Sharpe and DSR with trial count; drawdown; $OR(s)$; curvature-IM share. *Beta:* notional by client; β* against de-smoothed β̂; realized basis against s_lock; IM; economic exposure |
| **Model** | Main §4.6 plus gap_03's position layer: templates → CRIF → VM by CSA, SIMM-like IM, net-Greek limits, ledger. The tail follows C3 §5.3(e). The opportunistic book uses exposure templates plus a DSR-gated residual α |
| **Liquidity and stress** | *Tail:* a stress source, recognized at φ = 1 / 0.7 / 0, with listed value at 0.85 in ratios only. *Opportunistic:* IM ≈ 0.46 × annual P&L vol, ×1.0–1.5 for netting-set fragmentation; cleared IM can double in stress (FSB P95). *Beta:* P99 30-day VM of 11.7% of notional, plus IM rising from 4% to 10%. Cash map: §5 |
| **Synthetic defaults** | The policy book is drawn from the budget: a floor ladder of $7.1bn (3M 1.6, 6M 3.4, 12M 2.1), listed first; $10bn of completion beta; $1.0bn of opportunistic IM. The ≈250-trade blotter on 12 CSAs, with its ≈$25bn tail stack, is the engine-test fixture for gap_03 T1–T6. Its premium is rescaled to the budget in decision runs |

Forecasts and bias: unchanged (synthesis §5).

### 2.2 Parameters

| Parameter | Default | Source, as-of | Conf. |
|---|---|---|---|
| Tail budget | Floor 0.15%, cap 0.5% of NAV a year; t0 at the floor | C3 DQ22; GC2 D25 [I] | IC-set |
| Ladder | 90/72%-of-forward put spreads; 3/6/12M rungs weighted 25/50/25; listed first | C3 §5.3(e) [I] | Low |
| Market state | SPX 7,659.44; VIX 19.99; VIX3M 20.50; VIX6M 21.67; VIX1Y 22.61. SKEW 168.59 (mean 123.26; record 183.12 on 18 Feb 2025) | Cboe, 16 Oct 2026 [S rep.] | High |
| Surface | ATM vol = 0.90 × VIX_τ; skew linear in strike, calibrated to the variance-swap identity. 90%/72% vols: 23.7/33.0% (3M), 23.3/30.2% (6M), 23.2/28.2% (12M) | C3 c_ATM [I]; [I-calc] | Medium |
| Ladder economics | Premium 1.02 / 1.97 / 3.16% of notional (3/6/12M); 3.74% a year on outstanding notional; S1 payoff 0.166 per $ (4.4× annual premium) | [I-calc] | Medium |
| Spot–vol; VIX tenor betas | −1.35 / −0.94. Betas 0.64 / 0.45 / 0.30 for 3M / 6M / 1Y | 09 verifier [S-c]; gap_03 [I-calc] | High / Medium |
| Monetization; recognition | Triggers: Δ ≤ −0.5, value ≥ 3× premium, or V3+ with VIX ≥ 35; sell 50%, reinvest 40%. φ = 1 / 0.7 / 0; listed 0.85 | C3 [I] | Low |
| SIMM | Equity-index delta RW 15; vega margin ≈5.35 × vega per vol point; curvature scaling 23.0 / 3.8 / 1.9% at 1/6/12M | ISDA SIMM v2.8+2512, effective 11 Jul 2026 [S] | High |
| Schedule IM; UMR | Equity 15%; MSE $8bn; IM threshold $50m; the sovereign exclusion covers central governments only | 12 CFR 237 [S] | High |
| Futures financing | ≈30bp (2021–23); >140bp (Dec 2024); +81bp (Jun 2026 roll) | D. E. Shaw; CME [S] | High / Medium |
| Opportunistic | Vol 1.0–1.5% of NAV; drawdown stop at 2×; DSR ≥ 0.95; IM $1.0bn within a $1.5bn budget | C3; 09 [I/S-c]; [I-calc] | Medium |
| L1–L3; dealers | L1: $NV^{eq}_{ovl}\ge0.75\,NV^{eq}_{tail}$. L2: OR ≤ 25%. L3: curvature-IM share set by the IC. Dealers: ≤ 0.5% of NAV each; at least 5 | gap_03; C3 [I] | IC-set |
| Contingent-liquidity charge (CLC) on services | c_buf 1.5% × (P99 VM + ΔIM) = **≈27bp a year** of notional (18–53bp at c_buf of 1–3%) | §4.3 [C]; [I-calc] | Medium |

### 2.3 Actions

**Score.** Main §4.4, with overlay terms:

$$\mathrm{Score}(a)=\textstyle\sum\pi\,\mathbb E[\Delta CF_a]+\sum_{h,s}\tilde\mu_{h,s}(\varphi\,\Delta X^{h,s}_a-\Delta O^{h,s}_a)+\sum_k\rho_k\Delta\mathrm{Floor}_k-\lambda_R\Delta\mathrm{CVaR}-\lambda_{Lev}\Delta Lev-\lambda_{Enc}\Delta IM_a-\kappa^{tc}_a$$

- **Terms.** X is hedge inflows and O is VM/IM outflows.
- **Admissibility.** Score > 0, and after the trade L1–L3 hold and the safety filter F accepts.
- **Robust variant.** The same score evaluated on the worst-model duals.

| Book · action | Instruments | Rule | Lead time; consents | Regime; CFP stage | Encumbrance |
|---|---|---|---|---|---|
| **Tail · SELL** | Monetize; restrike (sell 50%, reinvest 40% lower and longer) | $V(1-ba)+\lambda^w\Delta L^{use}\ge\hat E[\text{cont}]$, with $\Delta L^{use}=V(1-ba)-\varphi R^c$ under a CSA. Restrikes scored as a bundle; L1 must hold | Listed: T+0. OTC: T+0–2 after ≥ 3 RFQs. Novation: consent of all three parties [S] | All; OTC capacity thins in crisis [I]. Pre-approved at Red | Releases IM and collateral |
| **Tail · HOLD** | Monthly roll | Mandatory up to the floor, with no score test. Above the floor, only if the robust score > 0 | Monthly; ISDA + CSA for OTC | All; after spikes, roll longer and lower | Listed: premium only. OTC: SIMM ≈$0.19bn at the floor, unless IA-only |
| **Tail · REFINANCE** | Sell a lower strike against a held put; post UST as IM; repo collateral received under reuse | $\sum\tilde\mu\Delta HQLA-\text{cost}-(\Delta KV+\Delta LV+\Delta EV)_{lost}>0$; coverage targets and L1 kept | Days; CSA amendments need dealer consent | Repo haircuts widen in crisis | Changes which assets are encumbered |
| **Tail · LEVER** | More notional; CDX; VIX calls; Brent spreads (need the mandate and the owner); hybrids (≥ 3 quotes within 0.15 implied correlation; Q-vs-P test, m = 25%) | Robust score > 0, with VRP low, fragility rising and SKEW not extreme; ≤ 0.5% | T+0; hybrids take weeks | Green or Amber | Premium plus IM; hybrids may need an IA |
| **Opp · SELL** | Cut | Mandatory at the drawdown stop, on any L1–L3 breach, at DSR < 0.95, or at Red. Otherwise cut if $\mathbb E[(1+\lambda^w)r^O]/\sigma^O<$ charges | T+0 listed or cleared; days for OTC | Crowding raises exit costs | Releases ≈$1bn of IM |
| **Opp · HOLD** | Keep | Within vol and IM budgets and L1–L3; DSR ≥ 0.95 at entry; trial ledger current | Monthly | Green, Amber | IM |
| **Opp · REFINANCE** | Compression, novation, clearing, CSA reallocation, non-cash collateral | $\tilde\mu\Delta IM-\text{cost}>0$, only if L1–L3 hold before **and** after. Otherwise the saving is hidden short volatility | Weeks. Novation needs three parties; transfers need written consent (ISDA 2002 §7 [S]) | All | Frees IM |
| **Opp · LEVER** | Scale up | DSR ≥ 0.95 and $SR^{post}\sigma>$ financing $+\lambda_R\Delta\mathrm{CVaR}+\tilde\mu\Delta IM$; within budgets and L1–L3 | T+0 | Green, Amber | IM rises |
| **Beta · SELL** | Cut completion beta; reverse a P2S | Cushion-monotone hedge rule. $\tilde\mu$(avoided VM + IM) + CVaR relief − forgone ERP − tc > 0. Reverse a P2S when $\bar\ell$ falls below its break-even | T+0; a TRS ends per its confirmation | All | Releases IM |
| **Beta · HOLD** | Quarterly roll | The client pays s_lock; the Overlay bears realized basis | Quarterly | All | IM 4% → 10% |
| **Beta · REFINANCE** | Futures ↔ TRS ↔ ETF; term TRS; UST posted as IM | Δfinancing $+\tilde\mu\Delta IM-$ switching cost > 0. An index TRS carries ≈15% IM, against 4–10% on exchange | ISDA and FCM agreements | All | Changes the IM |
| **Beta · LEVER** | Completion beta; P2S (exposure-neutral; Public Markets' REFINANCE, Tier B); PE rebuild on the de-smoothed β | ERP − f − $\lambda_R\Delta$CVaR − $\lambda_{Lev}\Delta Lev$ − CLC > 0. Exposure ≤ 1.30× and monotone in the cushion; gross overlay ≤ 0.30W | T+0 | Green or Amber; P2S also at Red | IM plus contingent VM |

### 2.4 Constraints

1. **Tail budget.** 0.15% ≤ B ≤ 0.50% of NAV a year.
   - The floor changes only at the annual Board-approved budget.
   - Moves within the band are Tier-A IC decisions.
   - Terminating a layer needs a disclosed Tier-A record.
2. **L1–L3 always hold.**
   - Named stresses are tested by full revaluation; the red team searches unnamed ones.
   - The overlay stays net long VIX-equivalent vega in stress.
3. **Opportunistic book.** $\mathrm{ES}_{97.5}\le B^{opp}W$; IM ≤ $1.5bn; no additions in Red.
4. **Synthetic beta.** Economic exposure ≤ 1.30×; gross overlay ≤ 0.30W. Whether P2S counts toward 0.30W is for ADIC to confirm.
5. **Execution and collateral.**
   - Listed first for the floor sleeve: no IM, φ = 0.85, no CSA consents.
   - Each dealer ≤ 0.5% of NAV.
   - Overlay IM counts toward the 15% / 20% encumbrance limits.

---

## 3. Transfer pricing and attribution for services

Take a service *j*: notional N, reference total return $r_B$, realized financing basis $b_t$, and $s^{lock}$ locked at each roll from the prevailing implied financing.

| Line | Client group | Overlay | CF |
|---|---|---|---|
| Exposure pass-through | $+Nr_B$ | $-Nr_B$ | |
| Locked financing | $-N(r_f+s^{lock})$ | $+N(r_f+s^{lock})$ | |
| Deposit interest (funded services) | $+Nr_f$ | | $-Nr_f$ |
| Contingent-liquidity charge, $CLC_j=c_{buf}\sum_h\omega_hO^{stress}_{j,h}$ | $-CLC$ | | $+CLC$ |
| Credit on cash released (P2S), at FTP | $+LPC$ | | $-LPC$ |
| External: VM and execution | | $N(r_B-r_f-b_t)-TC$ | |
| External: interest on collateral cash | | | $+r_fC_t$ |
| **Net** | $N(r_B-s^{lock})-CLC+LPC$ | $N(s^{lock}-b_t)-TC$ | $CLC-LPC$ |

**Client groups.**
- **Public Markets:** P2S, and portable-alpha or HF-TRS collateral.
- **TPA:**
  - Completion beta, which equitizes Treasury cash.
  - The beta rebuild after PE pacing cuts. Pacing is a CIO/IC decision and κ^GP already prices the forgone vintage, so charging PE would double count.
- **Co-investment and Private Credit:** their index-futures and CDX hedges.
  - The client keeps the risk-charge relief and the *hedge basis* (instrument against its private exposure).
  - The Overlay keeps the *implementation basis* (roll, financing against the lock, on-the-run against reference).
  - A group hedge proceeds only if its total-portfolio score is positive.

**Gate V2** [I-calc]. Test book: $10bn completion, $5bn P2S, $1bn PE rebuild, a −$1bn co-investment hedge and $1bn of CDX HY protection. On the benign path, the S1 path and 2,000 Student-t paths:
- internal transfers net to **0**;
- entity P&Ls equal external P&L with **zero** error. On S1 both sides are −$7.671bn.

The naive booking (client keeps its "as if physical" benchmark; Overlay keeps the VM) double counts −$7.05bn on S1 and +$0.88bn on the benign path. **V2 must therefore run on DVA ledgers, not only on cash.**

---

## 4. Tail-book DVA and pay: credit value ex ante

**Formulation.** For each live rung *j*, with premium $P_j$, coverage period $\tau_j$ and duals vintage-locked at purchase:

$$DVA^{tail}_t=\sum_{j\ \text{live}}(A_j-P_j)\frac{\Delta t}{\tau_j}+w\,E_t,\qquad A_j=KV_j+LV_j+EV_j$$

- **KV** is the market-kernel value of the payoffs; **LV** is $\sum\tilde\mu\,\varphi\,\Delta X$.
- **EV** is $\sum_k\eta_k\Delta\mathrm{slack}_k$ over T3 (where facilities count 0%), T6, T8 and the Tier-1B worst-model floor.
- **$E_t$** is experience: the realized value change minus the kernel-expected change.

**Booking.**
- **Reference ladder.** For the reference ladder R at the IC budget, the accrual $(A_R-P_R)$ and all experience go to the **TPA policy line**, which the IC owns.
- **Desk.** The desk books $(A_j/P_j-A_R/P_R)P_j$ at purchase, plus monetization proceeds minus what the rule would have realized.
- **Pay weight.** Set w = 0 in pay. Experience is shown in the fatigue tracker, and scenario payoffs are scored jointly on (VaR, ES).
- **Parity.** This matches Private Credit and Capital Solutions, which already earn c_buf on stressed inflows ex ante (§4.3).

**Numbers** [I-calc; floor premium $0.266bn].

| | Old: ex-post crediting | New: ex-ante crediting |
|---|---|---|
| Desk DVA, calm year / S1 year | −$266m / +$912m | ≈0 ± implementation |
| Value credited per $ of premium | Payoff when realized | KV 0.55 (G8 E1 carry convention, −45%) + LV/EV 0.0895 (E1 duals) or 0.0665 (c_buf parity) |
| IC policy line | — | **−$96m a year** (−36% of premium); −$319m at the cap |

- **Holding the floor.** The residual is the unmodelled EV the IC must believe in to hold the floor. Measure it on common random numbers.
- **If EV falls short.** The floor is then an explicit premium against model misspecification, which index options are known to carry (Drechsler 2013, Consensus record verified in stream 09).
- **Cross-check on KV.** The replay's realized payoff-to-premium ratio is 0.65 (0.62–0.69 across c_ATM). That is above KV's 0.55, so the convention is not generous to the hedge.

**Fatigue replay** [I-calc]. Floor ladder, monthly purchases from Oct 2009 to Sep 2025; SPX payoffs exact, premiums model-priced (§2.2).

| Exit rule | Negative years, 2010–25 | Worst run | Payoff / premium |
|---|---|---|---|
| Monetize at 3× premium or VIX ≥ 35 | 11 of 16 | 4 years (2021–24) | 0.65 |
| Monetize at 5× premium or VIX ≥ 45 | 12 of 16 | 6 years (2012–17) | 0.47 |
| Hold to expiry | 16 of 16 | 16 years | 0.11 |

Under the first rule the worst cumulative drawdown is 6.2 years of budget ($1.6bn at the floor). Net per $1 of annual budget:

| 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| −0.30 | +0.50 | −0.94 | −1.00 | −0.93 | +0.12 | −0.87 | −1.00 | +1.25 | −1.00 | +0.31 | −0.85 | −0.15 | −0.94 | −0.18 | +0.59 |

Monetization design matters more than skew. Ex-post DVA is a multi-year losing streak by construction.

**Peer check** (web sweep; Consensus blocked, see Sources).

| Peer | Evidence [S] | Design element |
|---|---|---|
| CalPERS, 2016–20 | Universa and LongTail Alpha were hired by Aug 2017; ≈$5bn protected at ≈5bp (base unstated [U]). "It did not have a customized benchmark", so the cost became "just another cost". Staff planned 3–6-month reassessments. Ended Oct 2019 for "high cost, lack of scalability" and "better alternatives"; missed more than $1bn. A board member said the board was not told (her claim) (II, 14–15 Apr 2020) | Reference-ladder benchmark; ex-ante credit; the floor owned by the IC/Board with an annual review; disclosed Tier-A record for any termination |
| NZ Super | Completion is measured as "value add versus our currency hedging benchmark", plus passive replication. Instruments are chosen on total cost, including "funding costs of a derivative". Liquidity is held for "an adverse two day market move". Reference derivatives are "fully backed by cash collateral". Tilting is an overlay with its own risk budget (2015 and Jun 2020 white papers) | The client keeps the exposure; the desk is judged on implementation; the opportunistic book is the tilting analogue; a 2-day VM warning row |
| CPP | The Balancing Portfolio is "a completion portfolio". "Benchmark returns are not presented for TFM because its primary purpose... is to rebalance the total portfolio". TFM adds value through "leverage and financing" and "trade netting" (F2024 AR pp. 20, 49–50) | Completion P&L goes to TPA; the Overlay is credited for execution |
| Literature | Institutions hit by net-worth shocks "reduce hedging substantially" (Rampini et al.); hedging falls near distress (Rampini–Sufi–Viswanathan 2014) | Pre-commit the floor over several years |

**Pay for the Overlay head** (G8 architecture):
- **40%** total portfolio.
- **35%** five-year group DVA:
  - tail implementation, credited ex ante;
  - opportunistic P&L net of FTP, CLC and risk charges, counting DSR-passing strategies only;
  - services implementation, $\sum N(s^{lock}-b)-TC$.
- **25%** individual: up to 10 points for forecasts, plus L1–L3 and rule compliance.

At least 50% is deferred over three years. Nothing scales with notional, premium or IM.

---

## 5. One reconciled sizing, and the §2.2 overlay row recomputed

| Item | Previously | Reconciled base (t0) | Band or stress |
|---|---|---|---|
| Tail premium | 0.4% (cash map); 0.15% floor (§3.7(c)) | **0.15%, $0.27bn.** SKEW at 168.6 fails the scale-up test, and the E1 score is negative | 0.15–0.50% ($0.27–0.89bn); moves are Tier A |
| Tail notional (90/72) | $20bn; ≈$25bn | **$7.1bn** (6.7–7.6) | $23.6bn at the cap (22.4–25.5) |
| S1 tail payoff; L2 cap on opportunistic loss | $3.5bn; none | $1.18bn; $0.29bn | $3.92bn; $0.98bn |
| Tail IM | — | $0 listed; $0.19bn OTC under UMR | $0.62bn OTC at the cap |
| Synthetic beta | $0–10bn; $10bn t0, $15bn stress | **$10bn of TPA completion**; economic exposure ≈0.97× | $10bn in a do-nothing stress. A +$5bn P2S is a Red lever booked to Public Markets *with* its proceeds |
| Opportunistic | ≈$1bn IM; vol 1.0–1.5% | **IM $1.0bn** (vol ≈1.0–1.2%); budget $1.5bn | +$0.5bn cleared-IM step in stress; +$0.25bn if a SIMM recalibration falls within the year |

**Overlay row, first 12 months, $bn** [I-calc]. Census v1.0 private flows are unchanged.

| | Normal | Drought | S1 | T4 |
|---|---|---|---|---|
| Published §2.2 | +0.16 | +0.16 | −6.03 | −6.03 |
| **Reconciled, floor** | **+0.31** | **+0.31** | **−4.00** | **−4.00** |
| of which services: beta VM − ΔIM (client TPA) | +0.58 | +0.58 | −4.12 | −4.12 |
| of which own books: tail + opportunistic | −0.27 | −0.27 | +0.12 | +0.12 |
| Reconciled at 0.25% / at the 0.50% cap | +0.14 / −0.31 | +0.14 / −0.31 | −3.59 / −2.56 | −3.59 / −2.56 |
| Before payout, floor (published) | +9.75 (+9.60) | +2.37 (+2.21) | −16.16 (−18.19) | −22.58 (−24.60) |
| Liquid-book funding at a 7.5% payout, floor (published) | 3.5 (3.7) | 10.9 (11.1) | 29.4 (31.5) | 35.9 (37.9) |

*SYNTHETIC – NOT ADIC DATA.* Memo: the Red P2S tranche on S1 nets +$2.74bn (sale +5.00; IM −0.20; VM −1.96; IM change −0.10). It belongs on Public Markets' line.

---

## 6. Folding this in

1. **Replace:** §3.7 with §2 above; the §2.2 overlay assumptions and row with §5, showing the services/own-books split.
2. **§3.8:** add "services booked to clients at FTP".
3. **§4.3:**
   - ex-ante tail credit;
   - the pass-through convention;
   - V2 run on DVA ledgers.
4. **§6:** policy book separate from the test fixture.
5. **§7 Group-7 IC block.** It shows:
   - budget use;
   - S/H/R/L cards for each book;
   - the L1–L3 offset card;
   - the services ledger;
   - the fatigue tracker;
   - the coverage matrix.

   New standing question: *"What policy residual is the IC paying, and what robust EV offsets it?"*
6. **Data from ADIC:**
   - CSA terms and sovereign IM status;
   - dealer allocation;
   - futures and TRS financing history;
   - the blotter in CRIF;
   - records of past hedge changes;
   - every opportunistic variant ever tested.

---

## 7. Verification log (adversarial)

| # | Claim checked | Verdict |
|---|---|---|
| V1 | The §2.2 overlay row reproduces | Confirmed: +0.162 / +0.162 / −6.025 / −6.025 |
| V2 | The text's "$10bn at t0" matches the computation | **Corrected:** the code uses $15bn everywhere, and the P2S proceeds are missing |
| V3 | A $20bn ladder at 0.4% of NAV | Consistent: the pricer gives 3.47–3.96% a year, i.e. 0.42% of NAV |
| V4 | The ≈$25bn tail stack is consistent with the floor | **Refuted:** it equals ≈0.53%; keep it as a fixture only |
| V5 | A 1.5%-of-NAV opportunistic loss in S1 is admissible | **Refuted** under L2 at every budget |
| V6 | The services split is zero-sum (V2) | Confirmed exactly; the naive booking errs by −$7.05bn |
| V7 | CalPERS facts | Confirmed (II, 14 and 15 Apr 2020). The LongTail payout is contested; the 5bp base is [U] |
| V8 / V9 | NZ Super and CPP quotes | Confirmed from the white-paper PDFs and the F2024 annual-report text |
| V10 | ISDA 2002 §7 consent; novation; CRIF fields | Confirmed. §7 and novation come from secondary texts; CRIF fields from ISDA RDS v1.36 (2017) |
| V11 | E1 tail credit of 895bp; 10.85% break-even dual | Confirmed (G8 verify) |
| V12 | Literature sweep | **Consensus not run.** Corpus Consensus records and the web were used instead |

---

## Sources

**Peers (accessed 2026-10-18).**
- Segal, J. (14 Apr 2020). The inside story of CalPERS' untimely tail hedge unwind. *Institutional Investor.* https://www.institutionalinvestor.com/article/2bsxabrnayd009kkvsd1c/portfolio/the-inside-story-of-calpers-untimely-tail-hedge-unwind
- McElhaney, A. (15 Apr 2020). Board member says CalPERS kept quiet about cutting tail hedge strategy. *Institutional Investor.* https://www.institutionalinvestor.com/article/b1l6npn5lqyd8g/Board-Member-Says-CalPERS-Kept-Quiet-About-Cutting-Tail-Hedge-Strategy
- Fennell, M. & Dunstan, B. (Jun 2020). *Portfolio Completion.* NZ Super Fund. https://fallback.nzsuperfund.nz/assets/Uploads/How-we-Invest-Portfolio-completion.pdf
- Iverson, D. (31 Aug 2015). *Managing Investment Risk and Liquidity.* NZ Super Fund. https://fallback.nzsuperfund.nz/assets/documents-sys/NZS180-Managing-Investment-Risk-Liquidity-White-Paper.pdf
- CPP Investments (2024). *Annual Report F2024.* https://cppinvestments.com/wp-content/uploads/2024/05/CPP-Investments-F2024-Annual-Report.pdf

**Documentation.**
- ISDA (1 Feb 2017). *Risk Data Standards v1.36.* https://www.isda.org/a/owEDE/risk-data-standards-v1-36-public.pdf
- ISDA 2002 §7, via Jolly Contrarian: https://jollycontrarian.com/index.php/Transfer_-_ISDA_Provision
- AIMA, on novation: https://www.aima.org/journal/aima-journal---edition-125-/article/revisiting-issues-involved-in-transferring-positions.html
- Haynes Boone (2016), 2016 VM CSA: https://www.haynesboone.com/news/alerts/isda-publishes-2016-credit-support-annex-for-variation-margin
- ISDA credit-support documentation page (2018 IM CSA): https://www.isda.org/book-taxonomy/credit-support-books/page/4/

**Data and corpus.**
- Data: Cboe daily index files; Fama–French factors (CRSP 202608).
- Corpus: main §4.4 and §4.6; C3 §5.3–5.6; gap_03 (main); G5; G7; G8 and its verification log; GC2 D21 and D25; the GS cash map.

**Literature** (Consensus records verified in `literature/09_overlay.lit.md`).
- Rampini, A. A., Sufi, A. & Viswanathan, S. (2014). Dynamic risk management. *Journal of Financial Economics* 111(2), 271–296. DOI 10.1016/j.jfineco.2013.10.003. Consensus record: https://consensus.app/papers/details/e86c89b63aeb51dcaea2c9919a32ce73/
- Rampini et al.: https://consensus.app/papers/details/57b5729c2197580ea311659a6e2d3970/
- Drechsler (2013): https://consensus.app/papers/details/71219fa7e399578680a3b58da1c70e3c/

**Consensus sweep.** It was attempted; every search returned the tool's usage message, quoted verbatim: "You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/"

*SYNTHETIC – NOT ADIC DATA (all [I-calc] figures).*

---

## Citation corrections (2026-10-18)

*Sources: the citation-integrity table in `research/literature/09_overlay.lit.md` ("Add title" for Rampini, Sufi & Viswanathan); `research/literature/00_LITERATURE_SYNTHESIS.md` §2. Metadata confirmed on Crossref.*

- Literature, Rampini, Sufi & Viswanathan (2014): title, *JFE* 111(2), 271–296 and DOI 10.1016/j.jfineco.2013.10.003 added to the bare Consensus link. The in-text use (hedging falls near distress) matches the abstract, per stream 09.
- Checked, no change: no other work cited here carries an audit correction. Stream 09's Kaminski & Lo (2014) flag concerns dossier 09's stop-loss claim, which this file does not make; its drawdown stop is a C3/09 design parameter. The co-investment barrier re-run affects no figure here.
