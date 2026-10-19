# GC2 · Public Markets, cross-group liquidity, organizational economics and synthetic data

*ADIC multi-period robust TPA framework · group-cluster synthesis GC2 (streams G5, G7, G8, G9) · as of 2026-10-18*

> **SYNTHETIC-DATA NOTICE.** Every ADIC balance, holding count, survival horizon, facility need and [I-calc] figure below is computed on the working allocation of context §1A or on design defaults. None of it is ADIC data, and none of it may be presented as ADIC data.

**Inputs read in full:** context §1–§1A, and the G5, G7, G8 and G9 dossiers with their verification logs.

**Checked for consistency:**
- `00_SYNTHESIS.md` (§2.3, L1–L6, §4.3, §4.9);
- C1 §5.4 (the Tier-1 rows);
- C2 (LP-level instruments; sale-success priors);
- C3 (the convex floor);
- the G1–G4 and G6 spec cards (census).

**Evidence tags:** [S] sourced and verifier-confirmed; [C] verifier-corrected (only the corrected statement appears); [I] inference or design default; [I-calc] synthetic arithmetic; [A] client statement or working assumption; [U] unverifiable, never load-bearing; [nrv] from memory, not re-verified.

**New computation.** The scripts are in `research/groups/addenda/GC2_calcs/` (all outputs SYNTHETIC).
- `gc2_reconcile.py` loads the unmodified stream-G7 ladder module.
  - It reproduces G7 and its verifier exactly: S1 needs of $36.7bn / $54.1bn; survival of 28 months at a 0% floor and 17 months at a 4% floor.
  - It adds a stress aligned with C1's T1.4, run under both owner-draw conventions.
  - It also computes Basel-capped coverage, Form PF cash timing, credibility weights and a private-credit PD calibration.
- `gc2_hf_split_variant.py` re-splits hedge-fund liquidity beyond 90 days to the SEC curve.
- `gc2_extra_checks.py` holds the small checks.

**Naming.** "Group 7 (Overlay)" is the investment group; "stream G7" is the liquidity research stream. **Corporate Finance (CF)** owns Treasury, the liquidity pool, the contingency funding plan (CFP), facilities, collateral (VM/IM), owner distributions and the FTP curve (context §1A). Where G7 or G8 say "central Treasury", read CF.

---

## 1. Executive summary

1. **Public Markets holds two reservoirs that fail differently.**
   - **Long-only ($36bn [A]) is market liquidity**, settling at T+1/T+2.
     - Impact on a $1–5bn basket is about 4–13bp for US large cap, 9–23bp for developed ex-US and 23–40bp for EM including taxes [I-calc].
     - These figures hold only up to a few % of ADV and need constituent-level volatility [C].
   - **Hedge funds ($20bn [A]) are contractual liquidity.**
     - Form PF's investor buckets (8.4% of NAV within 7 days, 27.3% at 8–90 days, 64.4% beyond; 30 Jun 2026 [S]) are *notice-based* and already assume gates [C].
     - With a 30-day payment lag and a 5% holdback, the synthetic book receives about **$4.9bn of cash within 90 days, not $7.1bn** [I-calc].
     - SEC's cumulative curve (58.2% of NAV redeemable within a year, Q3 2025 [S]) leaves about 42% beyond a year. Stream G7 had assumed about 21%.
   - **The reservoir fails where liquidity is dearest.** In 2008, net redemptions were $399bn (20%), gates were "liberally exercised" and secondary discounts reached 50% [S]. Model it as a state machine with a queue, not a bucket.

2. **Physical-to-synthetic (P2S) replacement is the cheapest non-cash liquidity in normal regimes, and a contingent liability in crises.**
   - Cost per $ of cash freed per year [I-calc]:
     - 0.40–0.70% in a normal regime;
     - 0.80–1.11% at June-2026 financing;
     - 2.24–2.69% at the documented quarterly-tenor peak;
     - 2.87–3.33% at an assumed 175bp.
   - A −33% month on a $5bn conversion is a $1.65bn VM call.
   - P2S is a cross-group action (Public Markets → Overlay → CF collateral), approved at Tier B.

3. **On the synthetic book, 30-day coverage is adequate but not ample, and the 24-month test fails.**
   - **30 days.** ADIC-LCR(30d) is **2.10×** with Basel composition caps (1.91× on Treasury-controlled assets), not 4.5× [C].
   - **S1 demand bust.** SH_TP is survival on Treasury + Public Markets with the buffer usable down to 4%. It is **17 months (Red), not 28** [C].
   - **C1's T1.4 vertex.** The vertex is: equity ≈−40%; PE, Secondaries and Co-investment distributions at zero and calls ×1.5 for 24 months; draws at the cap; facilities 50% available. Under it [I-calc]:
     - **SH_TP is 12 months on a fixed-USD draw and 15 months on a current-NAV draw.**
     - Clearing T1.4's hard row, which counts facilities, needs **$42–49bn** of committed facilities on a fixed-USD draw and **$25–31bn** on current NAV. The range spans G7's and SEC's hedge-fund splits; with the CFP pacing cut it is $14–38bn.
     - T1.4's elastic slack is positive at t0, which H reports as breach evidence. SH_TP puts the CFP stage at Red.
   - **The mandate dominates.** An owner-agreed 5% draw lifts SH_TP to 18–24 months. The facility need falls to $0.5–15bn, or $0–4bn with the CFP [I-calc]. This is consistent with main-synthesis L4.

4. **Policy beats assets, but G7's policy ladder is optimistic.**
   - P(red within 5 years) from a drought start [I-calc; C]: 18.1% with no facilities; 11.5% with facilities; 4.4% adding stage-based pacing cuts and early HF notices; 1.5% adding owner-agreed band use; 1.2% adding a 12% Treasury target.
   - These runs omit standby fees, forced paydowns, the owner's deferral cost and the P2S futures leg [C].
   - None meets the ≤ 1% gate.

5. **Organizational rule: groups are price-takers inside quantity envelopes.** Budgets aggregate H's solution. Decision prices are H's robust duals, with HQLA and borrowing as decisions, so buffer carry is a ceiling, never a floor [C]. Performance charges are vintage-locked full-cost allocations. Contingent liquidity is charged once per price set [C]. Bands are free only for releases [C]. Attribution is in dollars and credits every charge to a centre line [C].

6. **Interested forecasters need a mechanism, not just a score:**
   - a bitemporal P10/P50/P90 registry scored with the weighted interval score (WIS);
   - a hierarchical bias model using shadow-tracked declined deals;
   - one precision weight in the Forward Belief Engine (FBE), with no double shrinkage [C];
   - pay linear in realized DVA plus a skill KPI, with nothing scaling with budget or AUM.

   The inflation incentive is δ\* = bZB′/(2s).

7. **Synthetic data: a structural generator with sealed truth and labels enforced in code.** Six G9 fixes are required before release [C]:
   - PE unfunded sits *above* the Takahashi–Alexander steady state;
   - the normal-regime private-credit PD is 1.8%, not 2.5%;
   - the vintage-alpha coefficient is −0.05 a year, not −0.5;
   - BGK's 2.6pp is a symmetric peer-reversion scale;
   - smoothing is fund-level, not index-level;
   - SELL and REFINANCE use only LP-accessible instruments.

8. **One census and one bias prior serve every engine (§4.6).** The census has about 395 positions, with unfunded commitments ($bn) of PE 27.4, Secondaries 3.9, Co-investment 1.5, Capital Solutions 1.2 and Private Credit 4.0. The same priors drive the generator and the estimator, as simulation-based calibration (SBC) requires.

---

## 2. Verification ledger

| Stream | C / Corr / R / U | Corrections carried here | Unverifiable (not used) |
|---|---|---|---|
| G5 | 35 / 2 / 0 / 3 | **ADIC item.** Bloomberg via Hedgeweek (12 Jun 2026): plans *under consideration* for up to $15bn via leveraged structures, reportedly bank TRS on mainly large multi-strategy funds; the structure *was* reported. No inference about internal matters. **Fed FSR (May 2026):** requests "much larger than 5 percent of NAV"; most capped at 5%; accepted requests "somewhat exceeded new inflows" in Q1 2026. **Upgraded to [S]:** Aragon's 4–7%; Jenkinson–Jones–Martinez; HFRI Macro 2025 +7.2% | CME "+38bp Q2 2025"; Fung–Hsieh (2000) bias sizes; 10y UST on 16 Oct (5.10% on 15 Oct is confirmed) |
| G7 | 28 / 6 / 0 / 0 | Post-Lehman loans rose ≈6% over **five weeks**. Lazard's ≈27% is a **GP-led buyer survey**, not an LP-sale failure rate. WilmerHale's "given away" ("Trends in the Private Equity Secondary Market", ABA *Business Law Today* 18(4), 2009) was a **forecast**. The 2023 Addendum is **guidance** and asks for collateral *planning*. Harvard's figures come from the Jul 2009 article. Policy C is 4.4% | — |
| G8 | 30 / 2 / 0 / 0 | Pairing prices with envelopes is **our inference**, not Baumol–Fabian's (who are disputed by Maiti et al. 1973). FSI 2011: missing attribution is "**probably** the most striking example of poor practice". Shin–Stulz WP pointer mislabelled (NBER w5639 is a different 1996 paper; the *QJE* 113(2):531–552 citation stands) | — |
| G9 | 24 / 2 / 0 / 1 | BGK's sample is **USD-denominated**. Its 2.6pp is a **symmetric one-SD peer reversion**. CDLI is "averaging 9.5%". Campbell–Sharpe is contested (Hess & Orbe 2013). MOVE peak 264.6 confirmed. CA vintage component 0.10–0.13 after effective-n correction | Partners Capital "40–50% maximum illiquid" |

**Erratum (2026-10-18).** The G8 verification log accepted Lamont (1997) as *JF* 52(1):57–82; the pages are 83–109, and 57–82 is Carhart (1997) (`research/literature/00_LITERATURE_SYNTHESIS.md` §2.3). GC2 does not cite Lamont.

All four streams rate HIGH on evidence and MEDIUM on design. Every verifier design issue is resolved in §3–§4: G5 R1–R11, G7 R1–R11, G8 R1–R20 and G9 R1–R14.

---

## 3. Design questions and recommendations

| # | Question | Dossiers | **Recommendation** |
|---|---|---|---|
| D1 | What Form PF measures | G5: cash. G7: lagged time to cash. G9: SEC curve | Notice-based redeemability, with gates assumed, no suspensions and no fees [S]. Calibrate the synthetic book to it on that definition only. Cash timing comes from each lot's terms τ. The ladder consumes only φ_i(h,S), the P5 share of NAV delivered within h |
| D2 | Hedge-fund NAV beyond 90 days | G7: two-thirds within a year | **Follow SEC's curve**: ≈36% of the >90-day share within a year, giving 8.4 / 27.3 / 23.0 / 41.4% at ≤7d / 8–90d / 91–365d / >365d. G7's split is the optimistic sensitivity. The change costs $3.4bn of 24-month T + P capacity and adds ≈$7bn to the T1.4 facility need [I-calc]. OFR (35.7%) and SEC (35.0%) agree at 90 days |
| D3 | Leverage statistic | G5: GAV-weighted 12.3×. G9: SEC 3.3× | **NAV-weighted** for LP look-through (OFR Jun 2026): multi-strategy 4.5×, macro 6.8×, RV 8.1×, equity 1.8×, credit 1.7× [S]. GAV-weighted only for systemic narratives. The SEC–OFR gap stays open |
| D4 | Crisis gating in the ladder | G7: 50% on top of Form PF | Use the state machine's φ. Report three brackets: P5 (≈14% of the reconciled book gated in a two-quarter crisis; 17% on G5's split) [I-calc]; 50% gated; 100% gated |
| D5 | Hedge-fund return engine | G5: regime betas, put factor, skew-t, CRIS jumps. G9: t₄, C3 jumps | **G5's engine is the generator of record.** CRIS jumps at 0.3 per quarter, size 2σ (1.5–3), for multi-strategy, RV, credit and event [I], anchored on the GS VIP index's −19.07% in Q3 2008 [S]. Truncate shocks wherever exponentiated |
| D6 | Smoothing | G5: designed θ. G9: GLM index θ₀ | Fund-level θ priors from GLM's TASS fund tables, to be extracted [C]. Index ρ₁ only for aggregates. Constraints: θ ≥ 0, Σθ = 1, K ≤ 2, θ₀ ≥ 0.5 |
| D7 | Long-only alpha | G5: IR 0 to 0.10. G9: N(−0.05, 0.15²) | **Net IR mean −0.05 for all sleeves** (sd 0.15 DM, 0.20 EM/small cap); 0 as the upper sensitivity. G5's positive priors lacked support (Gerakos–Linnainmaa–Morse) [C] |
| D8 | Credibility | G5: Bühlmann Z (long-only 0.36). G8: Z × 1/κ² | **One hierarchical FBE model.** Forecast precision is 1/(κ_g²σ̂²); β_g uncertainty is propagated; no extra Z [C]. Bühlmann Z is display-only (hedge-fund residuals de-smoothed first): long-only 0.10 (DM) and 0.17 (EM) at 5 years [C] |
| D9 | Bias priors | G8: PE 2.0pp, Co-investment 3.0pp optimism. G9: 3.0, 3.5 | **One shared prior** for generator and estimator. Centre it on G9 = FBE defaults: +3%/yr, +4% late life, +5% underwriting [S: main §4.3]. G8's values are the low case |
| D10 | Overconfidence | G8: κ median 1.75. G9: κ_conf 0.45–0.7 | κ is lognormal, median 1.75 (1.2–2.7); κ_conf = 1/κ. At the median, a stated 80% range covers 54% of outcomes if unbiased and 48% with a half-SD bias; κ = 2.74 gives BGH's 36% [I-calc]. Calibrate κ jointly with b^f; 2.74 is an upper illustration [C] |
| D11 | Can the 8% IG + cash floor be used? | Main T2 hard. C1 elastic. G7: 4% hard | **8% elastic (M^IG) plus a hard 4% row at the top tier**, restored within 4 quarters. Basel LCR20.5: buffers are for use [S] |
| D12 | Named stress s\* | G7: S1. C1/main: T1.4. Main §2.3(d): C3's path | **T1.4 is s\***; S1 and C3's path stay in the CFP library. Year-1 net private flow is −$19.1bn under T1.4, against −$12.8bn in S1 and −$4.5bn on C3's path [I-calc]. **The IC must ratify the vertex**: it moves the facility need from ≈$4–7bn to ≈$42–49bn |
| D13 | How survival metrics nest | G7: SH_TP bands; SH_TPF ≥ 36m. C1: 24-month hard row. Main T4: target 36m | **Hard:** SH_TPF(T1.4) ≥ 24 months. **Appetite:** SH_TPF ≥ 36 months. **Stage indicator:** SH_TP on G7's bands. On the synthetic book, SH_TPF is 15–18 months (16–22 with CFP actions) [I-calc] |
| D14 | Owner-draw convention | G7: opening NAV (stresses), current NAV (Monte Carlo) | Show both, labelled; default to the mandate text. S1 needs: $36.7bn / $54.1bn on fixed USD, against $33.3bn / $45.3bn on current NAV [C] |
| D15 | 30-day coverage | G7: 4.5× uncapped | **T3 is the hard row.** ADIC-LCR(30d) uses its numerator: L2 ≤ 40% and L2B ≤ 15% caps, CF control, facilities 0%, 75% inflow cap. The ≈3.8%/month call rate rejects Basel's 40% prior, which would give 0.72× [I-calc] |
| D16 | Liquid share; stage thresholds | G7: 40.1% vs 32.8%; Monte Carlo vs CFP bands | Liquid share = (Treasury + long-only + HF cash ≤ 90 days at P5) ÷ NAV ≈ 31.6% [I-calc]. Use the CFP thresholds everywhere |
| D17 | Merit order | C1 six steps; G7 eleven; G5 within-group | **One recourse LP**, priced on state-dependent cost and reach (§4.4). Repo is a route, not a source. Pacing cuts and band use are stage-triggered, in parallel |
| D18 | Encumbrance basis | Main: total assets. G7: liquid assets | Total assets for the T5 limit; liquid assets as a stage indicator |
| D19 | Transfer prices | G8: duals floored at 3% plus a CLC. G7: Σℓ_h·LC | **Decision prices:** current robust duals from H, with HQLA and borrowing endogenous and no floor [C]. **Performance charges:** vintage-locked full cost, including the CLC at c_buf = 1.5% (1–3%) [C]. Stressed unfunded draws appear **once** per price set [C] |
| D20 | Envelope bands | G8: unilateral δ_g = √(2ε/H_g) | Free for releases only. Increases on binding rows pay the dual. Slack is shared so that Σ_g a^k_g δ_g⁺ ≤ slack_k. No free band above the Tier-A threshold (0.25% of NAV ≈ $0.44bn) [C] |
| D21 | P2S approval and model | G8: Tier C. G7 Monte Carlo drops the exposure | **Tier B or above**, drawing on leverage and collateral budgets [C]. Public Markets proposes, Overlay executes, CF funds collateral. Simulated P2S keeps the exposure: futures are added and VM becomes contingent [C] |
| D22 | Who holds the reserve | G5: a group share. G7: central | One CF pool (LCR30.18 analogue) [S]. Public Markets gets a ladder-contribution target and a consumption budget B_g |
| D23 | Census | G9: 495; group dossiers differ | Census v1.0 (§4.6) |
| D24 | Unfunded split | G7, G9 and the group dossiers differ | Group-dossier values. Co-investment 1.5 (midpoint; G4 gives none). PE is the residual of $38bn [A] = 27.4. Sensitivities: G1's $25bn and $12bn |
| D25 | Overlay at t0 | G7: beta $15bn, premium 0.4%. G9: beta $0–10bn, tail $25bn, opportunistic $45bn | **Synthetic beta $10bn** ($15bn in every stress run here), inside the 0.30W cap. Tail budget on the IC's 0.15%-of-NAV convex floor (0.15–0.5%). Opportunistic IM ≈ $1bn. Compare peers on stressed VM/IM, not gross notional [C] |
| D26 | Stressed 12-month calls | G8: 30% (Basel analogy). G7: ×1.25. T1.4: ×1.5 | **Stress:** 1.25–1.5 × the 28–31% base (≈35–45%/yr), per Cambridge Associates' "at or above their long-term average" [S]. **Central paths:** C2's m^C. Basel's 40% is a 30-day bank rate, so use it only as a cross-check [C] |
| D27 | LP-sale failure | G7: Lazard 27% | C2's success priors: 0.75–0.85 benign, 0.6 stress, 0.4–0.5 crisis [I], until ADIC data exist [C] |
| D28 | Financing spreads | G5 mixed tenors | **Separate series.** Quarterly roll: 30–50bp normal, 80–140bp tight [S], 175bp stress [I]. Short tenor (≈200bp, 26 Jun 2026 [S]) for TRS resets [C] |
| D29 | Dry-powder triggers | G7: Green/Amber. G8: discount > 20% and gate green | Require **both**. Value comes from contingent columns in H, with no separate liquidity-value term |
| D30 | Plan bonus; ES forecasts | G8: Weitzman kink; "never score ES" | **Linear DVA pay** plus a WIS-skill KPI; Weitzman only as a quantile score [C]. Score (VaR, ES) jointly where needed, never ES alone [C] |

---

## 4. Component specifications

### 4.1 Public Markets: hedge funds

**Data fields (per lot).**

| Field group | Fields |
|---|---|
| Identity | `holding_id`; group; strategy; manager; vehicle (commingled, SMA, managed account, UCITS, HF-TRS basket); share class |
| Size | NAV (reported and de-smoothed); ADIC share ω; fund AUM; investor-base mix |
| Terms τ | Frequency; notice; lock-up and type; soft-lock fee; fund gate and mandatory flag; investor gate; K^max; holdback; payment lag; side-pocket maximum; suspension; PIK/SPV; **`notice_revocable` (default false), `transfer_consent`, `pledge_consent`** [C] |
| Fees | Management; incentive; hurdle; high-water mark; pass-through cap |
| Risk and returns | NAV-weighted look-through leverage; monthly net and gross returns; u/a/f series with author and timestamps |
| HF-TRS terms | Counterparty; independent amount; margin frequency; termination triggers |

**Returns (monthly).**

$$r_{i,t}=r_{f,t}+\boldsymbol\beta_{i,S_t}^{\top}\mathbf F_t+\gamma_iP_t+\alpha_{i,t}+\sigma_{i,S_t}\epsilon_{i,t}+J_{i,t},\qquad \alpha_{i,t}=\alpha_{i,0}e^{-\delta\,age}(A_{ref}/A_{i,t})^{\eta}$$

| Term | Meaning |
|---|---|
| $\mathbf F$ | Fung–Hsieh factors plus liquidity. Seven factors explain "up to 80 percent" of the variation of diversified portfolios [S] |
| $P$ | OTM put return; γ < 0 for short-put strategies [S] |
| $\epsilon$ | Truncated skew-t |
| $J$ | Jumps per D5 |

- **Reported returns:** $r^o_t=\sum_{k\le2}\theta_kr_{t-k}$ (Getmansky–Lo–Makarov). θ = (0.55, 0.30, 0.15) understates volatility by 36% and inflates Sharpe 1.55× [I-calc].
- **Net returns:** $r^{net}=r^{gross}-m-e^{PT}-\kappa[V_t-\max(HWM_{t-1},H_t)]^+/V_{t-1}$. The effective incentive fee is ≈50%, 2.5× contractual [S].

**State and decisions.**
- **State per lot:** true and reported NAV, smoothing buffer, HWM, posterior α, fund AUM and ω; liquidity state X ∈ {LOCK, SOFT, OPEN, NOTICE, QUEUE, SUSP, PAY, SP, LIQ, DONE, TRS_TERM}; request q, times gated k, receivables, holdback and side-pocket units. Others' backlog is held per fund.
- **Quarterly decisions:** redemption notices; secondary sales; unit borrowing; portable-alpha notional; hires and terminations.

**Liquidity-term state machine** (at each dealing date d).
1. **Others' requests.** $R^{oth}_d=NAV_d\,\mathrm{clip}(\rho^{(d)}_S+\rho_1[-r^{rel}]^++\rho_2\mathbb 1\{\hat p^{gate}>p^*\},0,1)$, carried forward if unpaid.
   - ρ is converted from quarterly to the dealing frequency.
   - The preemption term is a model prediction (Cipriani et al.) [C].
2. **Gate.** If $q^{ADIC}+R^{oth}>gNAV_d$, a gate is imposed: always if mandatory, otherwise with probability $p^{gate}$, where $\mathrm{logit}\,p^{gate}=a_{c,S}+b_1DD^{3m}+b_2R^{oth}/NAV+b_3M_i+b_4(Lev_i-1)$.
   - The mismatch $M_i$ is on a net-asset basis, net of financing to be repaid [C].
3. **Payout.** $\pi_d=\min(1,gNAV_d/R_d)$ only when a gate is imposed [C]. $Pay=\min(q\pi_d,\gamma^{inv}B^0)$. Payment is in full at K^max.
4. **Suspension** lasts a geometric time with mean 3 quarters. A share ς of suspended funds liquidates.
5. **Side pocket:** up to $sp^{max}$ of NAV, cashed at hazard ψ_S with recovery μ^SP.
6. **Cash:** $(1-h)Pay$ arrives at $d+p$. The holdback follows the audit. A soft-lock exit pays $(1-\phi^{soft})$.
7. **Liquidation:** 50% within 3 months, 30% within 12 and 20% within 36, at 0.85–1.0 of NAV [I].
8. **Notices are irrevocable** unless flagged revocable. Pre-emptive notices signal [C].
9. **HF-TRS:** margin on reference-NAV moves; independent amount; bank termination on triggers or a gated hedge [C].

φ_i(h,S) is the **only** interface to the ladder.

**Strategy defaults** (SYNTHETIC [I]; fees per CA 2024 [S]; θ placeholders per D6).

| Strategy (weight) | β_eq normal / CRIS | Resid. σ | θ | Net α: mean (sd) | Fees: mgmt / PT or exp. / incentive (%) | Terms | CRIS gate hazard / quarter |
|---|---|---|---|---|---|---|---|
| Multi-strategy (30%) | 0.10 / 0.30 | 4% | (0.9, 0.1) | 2.0% (2.5%) | 0–1.5 / 4.5 / 20 | Quarterly; 60–90d notice; investor gate 1/16–1/20 per quarter | 3% |
| Equity L/S (15%) | 0.45 / 0.65 | 7% | (0.85, 0.15) | 0.5% (2.5%) | 1.5 / 0.15 / 20 | Monthly–quarterly; 45d; 1y soft lock | 4% |
| Event (10%) | 0.35 / 0.75 | 6% | (0.75, 0.2, 0.05) | 0.5% (2.5%) | 1.5 / 0.2 / 20 | Quarterly; gate 20–25% | 10% |
| Credit (15%) | 0.25 / 0.55 | 6% | (0.7, 0.2, 0.1) | 1.0% (2.5%) | 1.5 / 0.27 / 20 | Quarterly or semi-annual; side pocket ≤ 20% | 20% |
| RV / FI arbitrage (10%) | 0.10 / 0.30 | 4% | (0.75, 0.2, 0.05) | 1.0% (2.0%) | 1.5–2 / 0.2 / 20 | Quarterly; gate 25% | 20% |
| Macro (10%) | 0.05 / 0.00 | 7% | (1.0) | 1.0% (2.5%) | 2.0 / 0.18 / 20 | Monthly; 30d | 1% |
| Trend (10%) | 0.00 / −0.20 | 11% | (1.0) | 1.0% (2.0%); Sharpe ≈ 0.3 | 1–2 / 0.1 / 20 | Monthly or daily (managed account) | 1% |

**Other regime parameters.** Gate hazards outside CRIS are 0.1–2% per quarter. Others' requests run 3 / 4 / 15 / 6% of NAV per quarter in EXP / LATE / CRIS / RECV. CRIS side pockets: 10% per quarter, taking 10–30% of NAV. Report results across $p^{gate}_{CRIS}\in[5\%,40\%]$. Platform terms are contingent, not fixed [C]: Citadel's 6.25% quarterly limit applies "under certain circumstances", and Point72 allowed 25% [S].

**Actions** (scored with the C2 kernel).
- **SELL (redeem).** This is a queued SELL.
  - Redeem if $\hat\alpha^{net}_i+\kappa^{reentry}_i<\bar\ell(T^{cash}_i)$, using the term premium at the horizon when cash arrives.
  - Keep ADIC's share of any fund ≤ 10–20%.
  - Never break up capacity-constrained top managers.
  - Penalize redeeming the best liquid funds, the 2008 pattern [S].
- **SELL (secondary).** Sell at $(1-d^{HF}_S)$ if that beats the kernel value of the redemption schedule. Needs manager consent.
  - Discounts [I] are anchored on Hedgebay: 79.8% of NAV on average in Dec 2009, with extremes near 50% [S].
  - Defaults: 0–5% for liquid funds in normal markets (redeem instead); 15–25% for quarterly funds in CRIS; 30–50% for gated interests.
- **HOLD.** Value = NAV + PV(α^net) − the value of the terms to the investor. Ang–Bollen put that at ≈1% for a 2-year lock-up, and above 10% if the manager can suspend at will [S].
- **REFINANCE.**
  - (a) Borrow against units at 20–50% LTV, halved in CRIS, at SOFR + 150–300bp [nrv]. Needs pledge consent.
  - (b) Redeem and replicate the betas with futures, i.e. $y^{add}$ in §4.3.
- **LEVER.**
  - **Portable alpha** if $E[\hat\alpha^{net}]-\bar f>\lambda_R\Delta CVaR+\lambda_{Lev}\Delta Lev+\kappa^{VM}+\kappa^{mis}$, where $\kappa^{mis}$ = P(gate | CRIS) × (VM need − HF cash).
    - Collateral must be HQLA, never hedge-fund NAV.
    - In a −33% month, $2bn of beta needs $0.70–0.78bn within days, against $0.32–0.65bn returnable within 90 days [I-calc].
  - **HF-TRS sleeve** (the reported structure [C]). Extend HQLA backing to its independent amount and VM, and run a double-leverage stress that includes the termination branch.

**Forecasts and bias.**
- **Underwritten (u):** target net α, tracking error, crisis beta and terms.
- **Actual (a):** de-smoothed, factor-adjusted TWR and DWR, plus realized liquidity.
- **Forecast (f):** net-alpha P10/P50/P90 and a liquidity outlook.
- **Biases [S]:** selection on past returns (Goyal–Wahal); optimistic ratings, though the hedge-fund evidence is mixed (consultant picks earned an FH7 alpha of 0.70% [C]); survivorship above 5%/yr; smoothing; short-put tails; gross versus net; capacity; assumed contractual liquidity.
- **Bias prior:** b^f = +2.0pp.
- **Display Z at 3 / 5 / 10 years** [I-calc, C]: event/credit 0.34 / 0.47 / 0.63 (0.22 / 0.32 / 0.48 de-smoothed); multi-strategy 0.54 / 0.66 / 0.80; trend 0.09 / 0.14 / 0.25.
- **Grading:** rank IC; top-quartile hit rate; Brier score; crisis-beta error; time-to-cash and gate errors; regret against the "keep the fired manager" baseline; false-discovery control.

**Synthetic defaults.** 40 lots on the mix above, with lognormal sizes (σ = 0.6). Terms are drawn to the Form PF curve (D1–D2). Optional HF-TRS scenario.

**IC artifacts:** the ladder (contractual vs CRIS-P5); a manager evidence card (u/a/f, de-smoothed Sharpe, fee waterfall, time to cash, action scores); a portable-alpha stress card; forecaster scorecards.

### 4.2 Public Markets: long-only and physical-to-synthetic

**Data fields.**
- `mandate_id`, benchmark, tracking-error target, fee, holdings, ADV coverage, currency.
- Vehicle type: **SMA or commingled**. This decides T+1 sale, P2S feasibility and LCR control [C].
- Tax treatment of synthetic exposure (§892, §871(m) [nrv]).

**Returns and costs.**
- **Returns:** $r=r_b+(\beta-1)(r_b-r_f)+\alpha+TE\,\epsilon$. Fixed income adds $\beta^{cr}r^{cr}$, because its "alpha" is mostly credit beta [S: Brooks et al.].
- **Impact:** $c_j=Y\sigma_S\sqrt{Q/V_S}+\tfrac12spread_S+tax_j$, with Y = 0.5–1.0 [S: Tóth et al.].
  - Cap the formula at a few % of ADV; above that, use multi-day schedules or risk-transfer quotes [C].
  - σ and spreads run 2–3× in CRIS [I].

**Priors.**
- Tracking error: DM 3%, EM / small cap 5%, core FI 1%, HY/EMD 3%.
- Net IR −0.05 (D7).
- Display Z at 3 / 5 / 10 years: DM 0.06 / 0.10 / 0.18; EM 0.11 / 0.17 / 0.29 [C].

**Evidence [S].** 4,617 institutional products show alphas indistinguishable from zero (gross or net is still open). About 75% of mutual funds have zero net alpha. Fired managers match their replacements.

**Actions.**
- **SELL:** liquidate at $c_j$, or move in kind to passive.
- **HOLD:** the default.
- **LEVER:** add synthetic beta if $ERP_S-f_S$ exceeds the charges.
- **REFINANCE = P2S.** Exposure is unchanged; only the financing changes. Use it when, per $ freed per year [C: G5 R7]:

  $$\bar\ell_\tau\ \ge\ \frac{\bar f+\hat\alpha^{net}+(c^{sell}+c^{rebuy})/\tau}{1-m-b}+\frac{\lambda_{Lev}\,\Delta Lev}{C}+\kappa^{VM}_{>b}$$

  - C = (1 − m − b)N is the cash freed, with m = IM and b = the pre-funded VM buffer.
  - Leverage is charged on the actual Δ(economic leverage).
  - VM is priced only beyond the buffer.

**Worked example** ($5bn US large cap; fee 25bp; 16bp round trip over 2 years) [I-calc]:

| Regime | Spread | IM / VM buffer | Cash freed | Cost per $ freed per year |
|---|---|---|---|---|
| Normal | 50bp | 6% / 11.7% | $4.1bn | 0.40–0.70% |
| June-2026-like | 81bp [S, excerpt] | 8% / 11.7% | $4.0bn | 0.80–1.11% |
| Documented quarterly peak | 140bp | 12% / 33% | $2.75bn | 2.24–2.69% |
| Assumed stress | 175bp [I] | 12% / 33% | $2.75bn | 2.87–3.33% |

**Comparators.**
- An **LP-portfolio** NAV facility at SOFR + 300bp (250–400) [I, C2], plus fees and encumbrance. G5's 5.8% applied GP-level margins [C].
- A 12%-discount secondary at ≈4.6%/yr over an arbitrary 3 years.

### 4.3 Group waterfall and rebalancing

**Corrected program per scenario node** [C: G5 R3]. It separates exposure-neutral P2S ($y^{p2s}$) from beta adds ($y^{add}$):

$$\min\ \sum_i\big[\hat\alpha^{net}_i\tau_ix_iV_i+TC_i(x_iV_i)+\kappa^{reentry}_iz_i\big]+\sum_m(\bar f_m+\kappa^{VM}_m)(y^{p2s}_m+y^{add}_m)$$

Subject to:
- **Cash by bucket.** For b ∈ {7d, 30d, 90d, 1y}: $\sum_i\varphi_i(h_b)x_iV_i+\sum_m(1-m_m-b_m-c_m)y^{p2s}_m-\sum_m(m_m+b_m)y^{add}_m\ge Need_b$.
- **Beta drift.** $|\sum_i\beta_ix_iV_i-\sum_my^{add}_m|\le\delta^\beta$, with $y^{p2s}_m\le V_m$.
- **Concentration.** ADIC's post-trade share ≤ ω̄; otherwise cash is piecewise in ADIC's own request.
- **Economic exposure** ≤ 1.30× (C1 T1.5).

The bucket duals feed stream 08's MCL curve. The resulting priority:
1. Treasury above its floor.
2. P2S on long-only beta.
3. Passive sleeves.
4. Lowest-α long-only mandates.
5. Short-notice, low-α hedge funds.
6. Hedge-fund secondaries, only for gated interests at high λ.

**Rebalancing.**
- Test monthly on **economic** weights, with a 2pp band. GPFG's trigger is 2pp around 70% [S].
- Re-centre with futures, then trade physical over 1–3 months.
- Risk-adding rebalances proceed only if $\ell_t<\ell^*$, or synthetically with VM covered.
- Test a trend delay: monthly 60/40's maximum drawdown in 2007–09 was 1.2× buy-and-hold's [S].
- Public Markets proposes, Overlay executes, CF funds VM.

### 4.4 Total-portfolio liquidity engine

**Ownership.**
- CF owns the pool, the CFP, facilities, collateral and payouts, and publishes ℓ_h as the FTP curve.
- HQLA must sit under the liquidity function's control [S: LCR30.18].
- Group budgets B_g are the liquidity rows of the envelopes (§4.5).

**Data model** (stream G7): `Position` (with **counterparty type external/intra-ADIC**); `LiquidityProfile` per regime (time to cash, haircut, capacity, gate or φ, depth); `Encumbrance`; `Obligation` (draws, calls, DDTL, deferred payments, VM/IM, debt service, cures); `Facility` (availability by regime, lead time, LTV, cost, last test); `CollateralEligibility`; `StageState`.

**Buckets.**
- B0 T+0 · B1 1–7d · B2 8–30d · B3 1–3m · B4 3–6m · B5 6–12m · B6 12–24m · B7 > 24m.
- Committed lines count from B3 and never in 30-day ratios [S: Reg YY].
- **Intra-ADIC transfers count as zero.**

**Core equations.**

$$\mathrm{NCO}_s(h)=\sum_{t\le h}(O_{s,t}-I_{s,t}),\quad \mathrm{CBC}^R_s(h)=\sum_{k\in R}\sum_{t\le h}q_{k,s,t}P_{k,s,t}(1-\eta_{k,s,t})+F^R_s(h),\quad \mathrm{SH}^R_s=\min\{h:\mathrm{NCO}_s(h)>\mathrm{CBC}^R_s(h)\}$$

- **Recourse tiers nest:** T (Treasury) ⊂ TP (+ Public Markets) ⊂ TPF (+ facilities) ⊂ TPFA (+ amber sales: Private Credit, Capital Solutions) ⊂ ALL (+ red sales: PE, Secondaries, Co-investment).
- **LaR** = $q_\alpha(\mathrm{NCO}(h))$. For policy A, 12-month LaR95 = $24.0bn and LaR99 = $33.9bn, before management actions [I-calc].

**Flows by group.**

| Group | Flow model |
|---|---|
| PE | Calls $\kappa_g(S)U$; distributions $\delta_g(S,x^{exit})$NAV (G7 defaults: 11% drought, 3.5% crisis; GC1 supplies production values) |
| Secondaries | Faster distributions; deferred payables are liabilities |
| Co-investment | Exit hazard and follow-ons |
| Capital Solutions | PIK-toggle coupons |
| Private Credit | Interest plus DDTL/revolver spikes. US C&I loans rose $482bn in three weeks of March 2020, apparently all from existing commitments [S]. Banks could meet those draws because of Fed liquidity programs, deposit inflows and strong pre-shock capital [S: Li–Strahan–Zhang]; an oil- or fiscal-specific ADIC stress may lack that support [I] |
| Public Markets | φ-scheduled proceeds |
| Overlay | VM, IM, premia, monetization |
| CF | Draws, debt service |

**Corrected and reconciled synthetic results** [I-calc; SYNTHETIC; ranges are G7's vs SEC's hedge-fund split].

| Measure | Stream G7 | Corrected / reconciled |
|---|---|---|
| ADIC-LCR(30d) | 4.5× | **2.10×** capped; **1.91×** Treasury-controlled only; 3.67× if all long-only FI were Level 1; 0.72× under Basel's 40% unfunded prior |
| S1 survival, T + P | 28m | **17m** at the 4% floor (Red), either split; 24m (G7) or 18m (SEC) with the CFP pacing cut; 14m if 8% is unusable |
| S1 needs, 12m / 24m | $36.7bn / $54.1bn | $33.3bn / $45.3bn on current NAV; 24m cover 1.21, not 1.01 |
| T1.4, fixed-USD draw | — | Needs $43.0bn / $71.3bn; cover 0.72–0.77; **SH_TP 12m**; SH_TPF 15m; facility need **$42–49bn** ($31–38bn with the CFP) |
| T1.4, current-NAV draw | — | Needs $39.3bn / $62.3bn; cover 0.83–0.88; **SH_TP 15m**; SH_TPF 17–18m; facility need **$25–31bn** ($14–20bn with the CFP) |
| T1.4 + owner 5% draw | — | SH_TP 18–19m (fixed) or 20–24m (current); facility need $8–15bn or $0.5–7bn; $0–4bn with the CFP |
| T1.4, calls ×1.25 | — | SH_TP 14m or 16–17m; facility need $33–40bn or $16–22bn |
| Liquid share, t0 | 40.1% | 32.8% (HF ≤ 90 days by notice); 31.6% (HF cash ≤ 90 days) |
| Policy ladder, P(red) | 18.1 / 11.5 / 4.5 / 1.5 / 1.2% | **4.4%** for C. B–E are optimistic [C] and were not re-run on the SEC split, which would raise them |

- **Facility need** is committed capacity, counted from month 2 at 50% availability, that lifts SH_TP at the 4% floor to 24 months.
- **SH_TPF** adds the assumed $5bn revolver and a 5%-LTV NAV facility from month 3.
- **T1.4 runs** use G7's $15bn synthetic beta and S1 path: equity −39%, 18 crisis months.

**Reverse stress** (96 cells; T + P).
- 12-month breaches occur in only 3 cells. Each needs equity −50%, distributions ≤ 30% of drought rates, a 10% draw and calls ≥ 1.25×. These are necessary conditions, not sufficient ones.
- 24-month breaches occur in 58 cells.
- The most plausible failure is a deepening drought plus a moderate bear market. Rank failure worlds by KL-minimal tilting (C1).

**Constraints** (extending C1 T1.3–T1.5).
- **(L1) 30-day coverage** (= T3/T1.3).
  - It is elastic at the top tier, so any positive $u^M$ is a breach that escalates the stage [C].
  - Numerator: unencumbered, CF-controlled, capped HQLA. Facilities count 0%.
- **(L2) Ladder rows** at 3, 12 and 24 months under T1.4: $\sum_k\phi_{k,s}(h)A_k+F_s(h)-\mathrm{NCO}_s(h)\ge-u^L_h$, with $\phi=(1-\eta)\min\{1,\mathrm{cap}(h-\mathrm{ttc})^+\}\gamma$.
  - The 24-month row on T + P + F is hard. The 3- and 12-month rows are soft.
  - The duals μ_h give ℓ_h for stream 08's LAPV.
- **(L3)** Treasury band: 8% elastic, 4% hard.
- **(L4)** $LC_g=\sum_{i\in g}(\kappa^{s^*}_gU_i+c^{s^*}_i-\delta^{s^*}_gV_i)\le B_g+u_g$, with $\sum_gB_g\le\mathrm{CBC}_{TP}(12)-\text{draw}_{12}-\mathrm{VM}^{99}_{12}-\text{buffer}$. The dual is the group's hurdle.
- **(L5)** Encumbrance per D18. Pledged assets never count in L1–L3.
- **(L6)** Facility draws ≤ availability_S. P(LTV breach within 12 months) ≤ 2%. Simulate forced paydowns [C].
- **(L7)** Hedge-fund requests only on notice dates, with proceeds via φ.
- **(L8)** Private NAV + unfunded ≤ 0.80W. The synthetic book, at 0.81, breaches it.
- **Certified in P:** P(red within 5 years) ≤ 1%; payout met with ≥ 97.5% probability; P(SH_TP < 12 months | posterior) ≤ 5%.

**Action lens.** Every group's actions enter the ladder the same way:
- **SELL** adds (1 − η)Pq to CBC at the bucket's time to cash. It removes future inflows and transfers unfunded (relief ≈ $\kappa^{s^*}U$). It is worth doing when the bid ≥ LAPV(hold) at ℓ_h.
- **HOLD** keeps δ inflows and κ outflows in NCO.
- **REFINANCE** adds F(h) once the lead time has passed. It adds debt service and cure contingencies, and encumbers the pledged NAV. Choose it when the spread is below ℓ over its effective life.
- **LEVER** raises NCO and lowers CBC. It is allowed only if L1–L4 still hold.

**Pecking order** (priced per state by the recourse LP).

| Step | Source | Reach | Cost | Stress caveat |
|---|---|---|---|---|
| 1 | Treasury above 4% (cash; UST by sale or repo; IG) | B0–B1 | ≈ 0 | Treasury depth fell to ≈10% in Mar 2020 [S] |
| 2 | Tail-hedge monetization; IM released by opportunistic de-risking | B1 | Negative | Stream 09 rules |
| 3 | P2S on DM equities | B1 | Spread + IM | Contingent VM |
| 4 | Other long-only sales | B1–B2 | Impact | Commingled funds can suspend |
| 5 | Committed revolver | Month 2+ | Spread + fees | "May become unavailable" [S] |
| 6 | Hedge-fund redemptions, lodged at Amber | B3–B7 | Forgone α | Gates; queue |
| 7 | Pre-arranged LP-portfolio NAV facility | B3 | SOFR + 250–400bp | LTV cuts |
| 8 | Private Credit / Capital Solutions sales (amber) | B3–B4 | 11–30% | Buyers retreat |
| 9 | PE / Secondaries LP sales (red) | B4 | 9–35% | Success 0.4–0.5 in crisis [I] |
| 10 | Co-investment sales (red) | B5 | 15–45% | GP consent |

Pacing cuts and owner band use run in parallel from Amber.

**CFP stages** (per SR 10-6, Reg YY and FSB 2024 [S]).
- **Library:** B0, S1, S2 owner cap, S3 rates/collateral, S4 credit defaults, S5 Gulf-war shock, and an annual reverse stress.

| Indicator | Green | Amber | Red | Black |
|---|---|---|---|---|
| SH_TP(s\*) | ≥ 24m | 18–24m | 12–18m | < 12m |
| ADIC-LCR(30d) | ≥ 2.0 | 1.5–2.0 | 1.0–1.5 | < 1.0 |
| Treasury ÷ NAV | ≥ 8% | 6–8% | 4–6% | < 4% |
| Liquid share | ≥ 28% | 24–28% | 20–24% | < 20% |
| LaR99(12m) ÷ CBC_TP(12m) | ≤ 0.6 | 0.6–0.8 | 0.8–1.0 | > 1.0 |

- **Transitions.** Any hard trigger escalates. De-escalation needs two consecutive better readings. **The synthetic book starts in Red under T1.4.**
- **Soft EWIs:** P(crisis) > 0.5; VIX > 30; LP pricing < 85%; **ADIC's own** sale-failure rate (replacing Lazard's figure [C]); NAV-loan spread > SOFR + 700bp; PE distribution rate < 6%; calls ÷ distributions > 1.5; hedge-fund gate notices; dealer IM hikes; Brent below the owner's breakeven; DDTL utilization spikes; forecast accuracy < 80%.
- **Pre-approved actions:**
  - **Green (CF Treasurer):** normal pacing; dry powder within budget.
  - **Amber (CIO):** commitments cut to 25–50%; co-investment paused; hedge-fund notices per the queue plan; secondary tranche pre-positioned; NAV-facility documents activated; owner dialogue opened.
  - **Red (IC, weekly):** draw lines; P2S and long-only sales; monetize hedges; cut the opportunistic book; amber sales; formal band request.
  - **Black (Board and owner):** red sales; non-contractual outflows suspended.
  - Any distribution change needs the Board and owner.
- **Testing:** an annual fire drill; quarterly test draws on every line (the Addendum says "should regularly test" [C]); slice monetizations; collateral-mobility planning; a hedge-fund notice-calendar audit; an annual secondary indication; an owner-protocol test.

### 4.5 Organizational economics layer

**Roles.**
- **Board:** reference portfolio; appetites; distribution policy; annual FTP methodology; pay.
- **Total Portfolio Committee / IC:** CIO (chair), CRO, **Treasurer (CF)** and head of TPA. Group heads attend but recuse on their own budgets. Approves quarterly envelopes, prices and contingent budgets.
- **TPA desk:** runs H and P and computes duals.
- **CF:** publishes FTP and books the vintage mismatch. It is a cost centre with no profit target [S: CEBS ¶10].
- **Groups:** sourcing, selection, execution and forecasts inside their envelopes.
- **Validator / CRO office:** registry, scoring, model validation and the transfer-pricing committee.

**State per group and quarter:** reported and economic NAV; unfunded by vintage; stressed outflows and inflows by horizon and scenario; Euler CVaR contribution; leverage used and envelope use; the vintage-FTP ledger; registry state ($\hat\beta_g$, $\hat\kappa_g$, $n_{eff}$); the transfer ledger.

**Group decisions:** pacing, NAV band, liquidity and risk budgets, leverage, and contingent budgets.

**Action routing:**
- **SELL** is proposed by the owning group and priced through the firewall. An internal buyer makes it a transfer that raises no liquidity.
- **REFINANCE** raises liquidity only with an external lender. When Capital Solutions is the lender, it is internal leverage.
- **LEVER** draws on the leverage budget at λ_Lev.

**Budgets.**
- **Envelopes:** $\Lambda^k_g=\sum_{i\in g}a^k_i(x^*_i)$ for each coupling row (liquidity by horizon and scenario, CVaR, leverage, pacing).
  - Computed from a pooled re-solve across sample-average-approximation replications ("SAA-rep"), with ranges [C].
  - Groups see their budget elasticity $1/H_g$. Coupling makes deviation 1.1–3.5× costlier than own curvature implies [I-calc].
- **Contingent pacing:** $P_{g,t}=P^*_g\,\Pi_{[m^{lo},m^{hi}]}(1-\eta_g(\ell_t-\bar\ell)/\bar\ell)$, with η > 0 for PE and Co-investment and η < 0 for Secondaries and Capital Solutions (D29).
- **Beyond the envelope:** up to +20% at the dual (Tier B); beyond that, Tier A.
- **No ratchet** [S: Weitzman 1980].
- **Why a hybrid:** "in many cases there exist no prices which will lead divisions to make independent decisions that are optimal" [S: Baumol–Fabian]. Pairing prices with envelopes is our inference [C].

**Decision price** per $ of holding or proposal:

$$\text{charge}_i=\sum_{h,s}\mu_{h,s}a^{h,s}_i+\lambda_R\frac{\partial\mathrm{CVaR}}{\partial x_i}+\lambda_{Lev}b_i+\sum_k\rho_k\Delta\mathrm{Floor}^k_i-\sum_{h,s}\mu_{h,s}c^{h,s}_i$$

- **Liquidity duals μ** come from H with endogenous HQLA and borrowing, so KKT caps them at the buffer carry [C].
  - Zero duals across all scenarios signal an oversized buffer, not free liquidity.
  - Use mixture-weighted robust duals and report their dispersion.
- **λ_R** is H's CVaR dual. Solvency II's 4.75% is a sanity bound only [C].
- **Publication.** The published FTP curve is smoothed: EWMA with a 2-quarter half-life and a ±50% collar.
- **Liquidity tenor:** $\ell_{s,t}=\mu_{s,t}/(\pi_{s,t}-\mu_{s,t})$ and $LP(\tau)=\tau^{-1}\sum_{t\le\tau}E[\ell_t]$, charged on each asset's cash-weighted life [S: CEBS].
- **Synthetic illustration** (G8 E1, unfloored) [I-calc].
  - Duals: 1.83% on the crisis-liquidity row; 0.81% on CVaR.
  - Group charges: 58–212bp.
  - Private Credit's net α\* of −41bp earns a zero budget.
  - The tail hedge's credit of 895bp per $ of premium, against −4,500bp of carry, would need a 10.85% dual. Value hedges by liquidity and enabling value instead (main L5).

**Performance charges.**
- Vintage-locked. CF holds the mismatch.
- Full cost includes the CLC [S: CEBS ¶17, ¶20, Annex 2]: $CLC_g=c_{buf}\sum_h\omega_hO^{stress}_{g,h}$.
- **c_buf = 1.5% (1–3%).** This is the marginal cost of the cheapest liquidity-creating action, matching main L5. It is not the funding basket's risk premium, which the CVaR charge already prices [C].
- **Size:** $38bn × 35% × 1.5% ≈ **$0.2bn a year** (range $0.1–0.5bn) [I-calc]. This is the carry of dry powder.
- **Credits:**
  - Private Credit and Capital Solutions earn c_buf on stressed inflows.
  - The Overlay is charged for margin and credited for crisis payoffs.
- **Risk charges:** Euler CVaR contributions. Non-homogeneous liquidity metrics get marginal dual charges plus an unallocated residual [S\*: 11-R6].

**Internal transfers.**

| Transfer | Liquidity raised | Pricing evidence | Approval |
|---|---|---|---|
| PE stake sold to Secondaries | **Zero** (minus fees) | Third-party strip (≥ 20%); ≥ 2 external bids; fairness opinion if ≥ $250m or conflicted | Tier B or A |
| Capital Solutions lends against an ADIC co-investment | Zero unless refinanced externally | External quote or margin band | Tier B; leverage budget |
| Capital Solutions lends to a GP fund where PE is an LP | $-L(1-s)$ (s = ADIC's LP share) | ≥ 50% external syndication or a third-party quote | Tier A |
| P2S of long-only | Real: proceeds minus stressed IM/VM | Market | **Tier B** [C] |

**Transfer rules.**
- Book both legs at fair value; wedges are centre items. A $1bn transfer at 85% against 90% fair value would otherwise create $50m of fake alpha [I-calc].
- **Firewall:** a group that may bid cannot quote.
- **Blackout:** no transfers within 30 days of a measurement date.
- **Benefit test:** a transfer must show net total-portfolio benefit; pure P&L shifting is banned.
- **Market test:** Rule 17a-7, ERISA §408(b)(19) and FRA §23B cover only quoted securities [S], so strips and outside bids are the primary test [C].

**Forecast registry and scoring.**
- **Registry:** bitemporal and append-only. Each record holds author, as-of date, horizon, target, quantiles, a snapshot (u, a, NAV, regime), the decision link, and a declined-deal shadow id.
- **Quantiles:** P10/P50/P90, plus P5/P25/P75/P95 for PE, Co-investment and opportunistic-overlay forecasts [C]. Also 4- and 8-quarter cash flows and exit timing.
- **Score:** $\mathrm{WIS}=\tfrac{1}{1.5}[\tfrac12|y-q_{50}|+0.1\,IS_{0.2}]$, with $IS_\alpha=(u-l)+\tfrac2\alpha(l-y)\mathbb1\{y<l\}+\tfrac2\alpha(y-u)\mathbb1\{y>u\}$.
  - It is proper, but only a coarse CRPS proxy at K = 1 [C].
  - Example: a 12/20/26% co-investment forecast against a realized 7% scores 0.086, against 0.023 for the reference class, a skill of −2.69 [I-calc].
- **Bias model:** $y_j-q_{50,j}=\beta_g+\beta_s+\beta_a+\gamma(u_j-a_j)^++\varepsilon_j$, with $\varepsilon_j\sim t_\nu(0,\kappa_g\hat\sigma_j)$ and $\hat\sigma_j=(q_{90}-q_{10})/2.563$.
  - $n_{eff}=n/(1+(m-1)\rho)$, with ρ = 0.3.
  - Estimate on all forecasts, including shadow-tracked declined deals, with inverse-propensity weights. Approved-only estimates carry the optimizer's curse [S].
- **Display** only when $n_{eff}\ge20$. At n = 20, the standard error on 80% coverage is ±8.9pp.
- **Incentive:** $\delta^*=bZB'/(2s)$, with $B'=1/H_g$ [C].
  - Keep b small and make s real.
  - A low Z helps only if the centre's prior is right [C].

**Attribution** (dollars on both sides) [C]:

$$NAV_0(R_P-R_{RP})=\sum_gDVA_g+DVA_{TPA}+DVA_{CF}+\text{residual},\qquad DVA_g=\sum_{i\in g}NAV_i(r_i-r^{FB}_i)-FTP^{vint}_g-\lambda_RRC_g+CR_g$$

- $DVA_{CF}$ receives $\sum_g(FTP^{vint}_g-CR_g)$.
- $DVA_{TPA}$ receives $\sum_g\lambda_RRC_g$.
- Interactions are attributed by exact Shapley values (256 coalitions) on common random numbers.

**Pay** [I; ADIC's HR and legal constraints are unknown].

| Population | Total portfolio | Group | Individual |
|---|---|---|---|
| Group heads | 40% (5-year absolute return vs 10%, plus DVA) | 35% (vintage-FTP DVA, 5 years) | 25% (≤ 10 points for forecast skill) |
| CIO / senior management | 50% | 50% (department and individual) | — |

- At least 50% is deferred over 3 years, indexed to total-portfolio return. Pay is linear, with no kinks at plan.
- Hedge staff are judged on mandate delivery, not standalone P&L.
- **CPP:** 30/30/40 weights; a −C$63.7bn five-year DVA zeroed its multiplier, leaving a total-fund multiplier of 0.62 [S]. The HRCC then raised the non-senior multiplier [C].
- **NBIM:** variable pay capped at 100% of fixed pay; at least 50% deferred [S].

**IC norms.** Credibility is a weight on information, not a grade on people. Compare each group with its own reference class, and never publish league tables. Show scores selection-adjusted, multi-year and with bands. Penalize sandbagging as much as optimism. Keep individual scores private. Hold blame-free post-mortems. No group vetoes another; prices and envelopes settle conflicts.

### 4.6 Synthetic data: SYN-ADIC-177

**Architecture.**
- **Three layers.** World: regimes, VIX labels, factors, exit factor X_t, valuation gap z_t. Truth (sealed): skill, economic NAV, true μ, outcomes, bias draws. Observation: reported NAV, cash flows, u/a/f, terms, quotes, loan tapes, overlay trades, CSAs.
- **Releases.** R0: the 2026-10-18 snapshot with history from 2008. R1: 1,000 worlds × 40 quarters on common random numbers. R2: 200 history worlds (2000–2040) for time-travel tests.
- **Grid and storage:** US$m; quarterly, monthly for hedge funds, daily overlay sub-steps in V3+. Parquet, with a `SeedSequence` hierarchy.
- **Why structural:** no ADIC data is needed; θ is known; it emits counterfactual action cash flows and truth columns. CTGAN and TabDDPM serve only as realism challengers later [I].

**Census v1.0** (SYNTHETIC).

| Group | Positions | NAV ($bn) | Unfunded ($bn) | Basis |
|---|---|---|---|---|
| PE funds | 120 (~70 GPs) | 52 | 27.4 (residual) | G1: large buyout 40%, mid 25%, growth 12%, VC 8%, sector 10%, special situations 5% |
| Secondaries | 40 | 14 (fund 5.6, LP directs 4.6, SACV 2.0, MACV 1.4, other 0.4) | 3.9 (incl. 0.4 deferred) | G2 |
| Co-investment | 90 | 18 | 1.5 | G4; ~70% share a GP with a PE fund (ρ_GP = 0.6) |
| Capital Solutions | 40 | 8 | 1.2 | G3: fund finance 30%, structured equity 20%, junior 15%, rescue 10%, ABF 15%, GP/LP 10% |
| Private Credit | 35 + ~1,500 loans | 14 | 4.0 (1.0 DDTL/revolver) | G6: direct lending 60%, ABF 15%, mezzanine 10%, opportunistic 15% |
| Hedge funds | 40 | 20 | — | §4.1 mix |
| Long-only | 24 | 36 (DM 22, EM 6, FI 8) | — | G5/G7 |
| Treasury (CF) | 6 sleeves | 15 (cash 6, UST 4, IG 5) | — | G7 |
| Overlay | ~250 trades, 12 CSAs | $50–90bn notional | — | D25 |
| **Total** | **≈ 395** | **177** | **38.0 [A]** | |

**Diagnostics** [I-calc; C].
- PE unfunded ÷ PE NAV = 0.53. That is above the Takahashi–Alexander steady state of 0.37 (normal) and 0.24 (drought). On G9's own census it is 0.46; G9's claim to "match" steady state compared the wrong denominator.
- (Private NAV + unfunded) ÷ NAV = 0.81.

**Truth-process fixes** [C].
- **T2 skill.** $a_v=-0.05z_v+u_v$ per year. The vintage SD becomes ≈1%, not 10%. GP effect 3%, idiosyncratic 2.5%, total σ_α ≈ 4%.
- **T3 PE NAV.**
  - Truncate the t₅ shocks or use NIG, because $E[e^{t_5}]$ is infinite.
  - Jumps cost ≈1%/yr, so α_s = +3% is net of write-downs.
  - PME transfers across market paths only when β ≈ 1.
  - Calibrate *within* each world. Pooling worlds gave a vintage ICC of 0.78, against 0.12 empirically.
- **T6 private credit.** PD 1.8% normal (×1.5 in D, ×3 in C); LGD 0.40 (+15pp in C). On 70/20/10 regime shares this gives a 1.0% long-run loss, matching CDLI [S]. A 2.5% PD gives 1.4% and fails V12.
- **T7 / T8.** The §4.1 engine with NAV-weighted leverage; long-only IR −0.05.
- **Co-investment.** σ_deal(ln MOIC) = 0.77 (P(MOIC < 1) ≈ 22%) is a fragile back-out. Use 0.66–1.00 as a sensitivity, never as a gate [C].

**Observation layer.**
- **O1 NAV manipulation** (BGK model ii) [C]:
  - a symmetric peer reversion of ≈2.6pp of quarterly return per SD;
  - plus ≈+5pp at 2 SD below peers and ≈+1pp at 2 SD above, after five years without a new fund.
- **Other O1 terms:** smoothing λ_q of 0.5 (buyout), 0.6 (VC), 0.3 (private credit), 0.4 (Capital Solutions); a 1-quarter lag; noise N(0, 0.04²); exit uplift ln(P/N_{t−2}) ~ N(0.10, 0.15²), so ≈75% of buyout *assets* exit above their next-to-last mark [S]; tail-end (+12%) and VC (+8%) over-marks [I].
- **O4 forecasts:** $f_t=\rho_ff_{t-1}+(1-\rho_f)[w_uu+w_aa+(1-w_u-w_a)f^*+b^f]+\eta$. Campbell–Sharpe's ≈30% anchoring weight maps to w_a or ρ_f, not w_u [C]. With ρ_f = 0.6, new information gets ≈0.2 weight per quarter. Timing optimism lasts 5 quarters after a high-yield spread shock above +150bp. Overconfidence follows D10.

**Shared bias priors** (pp a year vs truth; + = optimistic; the generator draws them, the estimator uses them as priors).

| Group | b^u | b^f | G8 low case | Specific bias |
|---|---|---|---|---|
| PE funds | +5.0 | +3.0 (+4.0 after age 8) | +2.0 | Fundraising marks; exit timing |
| Secondaries | +2.0 | +1.5 | +1.0 | Discount booked as alpha |
| Co-investment | +6.0 | +3.5 | +3.0 | Leverage > 6×; multiple expansion |
| Capital Solutions | +2.0 | +1.5 | +1.5 | PD understated ×0.7 |
| Private Credit | +0.75 | +0.75 | +1.0 | Expected loss 0.5% vs 1.0% |
| Hedge funds | +3.0 | +2.0 | +2.0 | Extrapolation |
| Long-only | +1.0 | +0.75 | — | — |
| Overlay: tail | Carry understated 30%; payoff overstated 20% | Same | — | Roll cost after spikes |
| Overlay: opportunistic | Sharpe +0.6 | Sharpe +0.4 | Overfitting | Crowding |

**Validation gates.** G9's V1–V20 apply, with these changes [C]:
- **V3:** USD-denominated BGK sample.
- **V4:** vintage component 0.10–0.18.
- **V10:** fund-level θ₀; index ρ₁ on aggregates only.
- **V11:** Form PF curve on its own definition, ±5pp.
- **V12:** regime-weighted loss of 0.8–1.2%.
- **New V21:** census v1.0 and NAV-weighted leverage within ±20% of OFR.
- **New V22:** Basel caps in every coverage ratio.
- **New V23:** no LP-inaccessible SELL or REFINANCE instrument (GP-level NAV loans, secondaries-fund facilities, holdco PIK without consent, CV exits). Actions are re-run on common random numbers. LP-level REFINANCE uses portfolio financing, preferred equity or structured secondaries, and CFOs, each with a GP-consent probability and its own pricing [C].
- **SBC on every Bayesian engine.** In the prototype, SBC flagged a fusion posterior that ignored the correlation between forecast and underwriting errors (χ²₁₉ = 207 against a critical value of 30.1). Separately, cluster-blind intervals for group bias covered 76%, not 90% [I-calc, G9].

**Labelling (L1–L8), enforced in code:** SYN- identifiers and `is_synthetic=true` on every row; Parquet metadata; a "SYNTHETIC – NOT ADIC DATA" footer; taint propagation; sealed truth tables; a claim validator; frozen, separate sets once real data arrive.

### 4.7 Agent roles

LLMs extract, verify, challenge and draft; deterministic code owns every number.

- **Terms Extractor** (quarantined): dual-extracts τ with clause links.
- **Terms Verifier:** applies rubric gates.
- **Waterfall Planner:** calls the §4.3 and recourse LPs.
- **Challenge agent** flags:
  - adverse-selection redemptions and preemptive-run exposure;
  - double leverage and unpriced pass-through fees;
  - VM backed by hedge-fund liquidity;
  - transfers without a market test;
  - forecasts outside the reference class.
- **Calibration agent:** refits quarterly.
- **Playbook drafter:** drafts CFP playbooks; parses CSAs, LPAs and facility terms.
- **Validator:** owns the registry and the scores.

On SYN-ADIC-177, agent tasks are graded against known truth.

---

## 5. Calibration targets

| Parameter | Value | As of | Source | Conf. |
|---|---|---|---|---|
| HF investor liquidity (notice-based, gates assumed) | 8.4% ≤ 7d · 27.3% 8–90d · 64.4% > 90d | 30 Jun 2026 | OFR (Form PF) | High (definition caveat) |
| HF investor liquidity, cumulative | 6.8 / 9.0 / 19.1 / 35.0 / 46.7 / 58.2% at 1 / 7 / 30 / 90 / 180 / 365 days | Q3 2025 | SEC Private Funds Statistics | High |
| HF restrictions | May suspend $3.18tn; may gate $2.05tn; gated $121bn; side-pocketed $103bn (of ≈ $5.2tn) | Q3 2025 | SEC | High |
| HF leverage, NAV-weighted | Multi-strategy 4.5×, macro 6.8×, RV 8.1×, equity 1.8×, credit 1.7× | Jun 2026 | OFR | High |
| Multi-strategy cash | 20.3% of NAV (26.8% in Mar 2020) | Jun 2026 | OFR | High |
| Crisis loss ratios | Composite 0.51 (2008), 0.48 (Q1 2020), 0.23 (2022); Equity Hedge 0.66 and Event 0.78 (2020) | — | HFRI via CA and HFR | High |
| Trend convexity | CTA +14.09% (2008), +7.13% (2022); 1.89%/yr over 2009–25 | Oct 2026 | BarclayHedge | High |
| HF smoothing (index level) | ρ₁ from 56.6% (convertible arbitrage) to 3.2% (managed futures) | 1994–2002 | GLM Table 10 | High (aggregates) |
| HF fees | Management 1.50% median (macro 2.00%); pass-through median 4.53% (0.87–12.99%); effective incentive ≈ 50% | 2024; 2026 | CA; Ben-David, Birru & Rossi | High |
| 2008 redemption stress | $399bn (20%); 20–25% of capital requested; Hedgebay 79.8% of NAV | 2009–10 | Hennessee; CA; WealthBriefing | High |
| Long-only alpha | ≈ 0 across 4,617 products | 1991–2008 | Busse, Goyal & Wahal | High |
| Equity financing | ≈ 30bp (2021–23); > 140bp peak (Dec 2024); +81bp (Jun 2026 roll); ≈ 200bp short tenor | 2025–26 | D. E. Shaw; CME (excerpt); Reuters | High / Medium |
| Base rates | SOFR 3.89%; 10y UST 5.10% | 15 Oct 2026 | NY Fed; FRED | High |
| PE contribution / distribution | 27–31% / 9–11%; 9% in H1 2026 | Oct 2026 | MSCI | High |
| LP secondary pricing | 87% average; buyout 91%; credit 89%; deferrals in 26% | H1 2026 | Jefferies | High |
| Crisis bids | 61% of NAV (83.5% adjusted) | Jan 2009 | Cogent via Unquote | High (upper bound) |
| Revolver dash for cash | C&I loans +$482bn, met with Fed liquidity support and deposit inflows | Mar 2020 | Li, Strahan & Zhang, *RCFS* 9(3):472–500 | High |
| Treasury depth in stress | ≈ 10% of normal; impact 5–6× | Mar 2020 | NY Fed | High |
| Non-cleared VM in cash | 68.3% | End-2024 | ISDA | High |
| Forecaster calibration | 80% intervals cover 36% | 2013 | Ben-David, Graham & Harvey | High |
| Buyout dispersion (p5–p95) | TVPI 0.60 / 1.18 / 1.56 / 2.03 / 3.38; KS-PME 0.48 / 0.89 / 1.22 / 1.53 / 2.16 | Data to Mar 2012 | BGK (USD-denominated) | High |
| Vintage component | ≈ 0.13 (0.10–0.11 after effective-n correction) | 31 Dec 2019 | CA (derived) | Medium |
| VC marketing | Required IRR 31%; marketed net IRR ≈ 24% | 2016–20 | Gompers et al. | High |
| Direct-lending loss | 1.0%/yr long-term; half that now | Aug 2026 | Cliffwater releases | High |
| MOVE | Median 80, p95 141, p99 192; peak 264.6 | 16 Oct 2026 | Yahoo ^MOVE | High |
| VIX | Mean 19.4; p99 46.7 | 16 Oct 2026 | Cboe | High |
| Peer leverage and commitments | CPP recourse leverage 36.3% (limit 45%); unfunded 8.9% of net assets | F2025 | CPP | High |
| **System targets** [I] | P10–P90 coverage 80% (70–90% at n ≥ 50); WIS skill > 0; charges reconcile within 5%; envelope use 70–100% | — | G8 (corrected) | — |

---

## 6. Cross-group interactions and links

| Interaction | Groups | Mechanism | Treatment |
|---|---|---|---|
| Liquidity competition | PE calls, owner draw, overlay VM, dry powder | One ladder in the worst states | Shared L1–L2 rows; FTP; budgets B_g; dry powder gated by stage |
| Crowded waterfall | PE → Public Markets | Calls force redemptions; gates follow; investors then sell their best liquid funds (2008) [S] | State machine; adverse-selection penalty; notices lodged at Amber |
| P2S | Public Markets → Overlay → CF | Exposure kept; VM becomes contingent | Tier B; leverage and collateral budgets |
| Portable alpha / HF-TRS | Public Markets, Overlay, CF | Margin falls due while the alpha sleeve is gated | HQLA-only collateral; κ^mis; TRS termination branch |
| Internal secondary | PE → Secondaries | Relabelling | Zero liquidity; fair value; firewall |
| In-house pricing | Secondaries (SELL bids); Capital Solutions (REFINANCE and unit-financing quotes) | Intelligence with a conflict of interest | Pricing committee; independent quotes; CF decides; logged |
| Internal leverage | Capital Solutions → Co-investment / PE | No outside cash | Zero, or −L(1 − s); leverage budget |
| Natural hedges | Trend/macro vs equity; tail hedge vs deployment | Convex in gap crashes, weak in grinds (0.23 in 2022) | Trend in the defensive stack; monetization funds deployment |
| Counter-cyclical franchises | Secondaries, Capital Solutions | Opportunities widen as liquidity tightens | η_g < 0; contingent budgets (a franchise hedge, not a liquidity hedge) |
| Deal flow | PE → Co-investment; PE ↔ Secondaries; Private Credit ↔ sponsors | Shared GPs | ρ_GP = 0.6; look-through concentration |
| Semi-liquid credit | Private Credit evergreen/BDC wrappers | 5% caps in 2026 [C] | Same state machine |
| Owner channel | Owner ↔ Public Markets | SWFs pulled ≥ $46.5bn from managers in 2015 [S→03] | Owner-draw engine |

**Links to GC1** (`research/groups/clusters/GC1_private_groups.md`: G1, G2, G3, G4, G6).
- **GC1 supplies:** κ_g and δ_g intensities (replacing G7's defaults); consent, ROFR and pledge rights (ladder time to cash; gate V23); LP-level SELL/REFINANCE instrument libraries; group forecast production; census detail; group CFP playbooks.
- **GC2 supplies:** ℓ_h and FTP; envelopes and B_g; the stage machine; the registry and scoring; transfer rules; shared bias priors and SYN-ADIC-177 truth.

**Main program:** C1 (T1.1–T1.8, the H/P/F core, the merit order); C2 (kernel, FBE, instruments, sale priors); C3 (owner draw, overlay ledger, convex floor); C4 (agents, tiers, claim validator).

---

## 7. Open questions and data ADIC must supply

**Most valuable, in order.**
1. **The draw rule.** Fixed USD or % of NAV? Who sets it? Can band use be pre-agreed in stress? On the synthetic book, the draw rule alone moves the T1.4 facility need from ≈$42bn to ≈$0.5bn on G7's hedge-fund split, and from ≈$49bn to ≈$7bn on SEC's.
2. **Ratification of the T1.4 vertex** versus C3's milder path.
3. **Hedge-fund terms:**
   - offering documents and side letters: τ, revocability, transfer and pledge consent, investor gates, ADIC's share of each fund;
   - redemption experience in 2008, 2020, 2022 and 2026;
   - terms beyond 90 days, which decide between G7's and SEC's split.
4. **Facilities:** existing lines and repo, test history, and appetite for a pre-arranged LP-portfolio NAV facility.
5. **Overlay:** CSA/IM terms; whether P2S counts against the 0.30W cap; financing history by index; TRS quotes.
6. **The leveraged hedge-fund programme,** if pursued: counterparty, independent amount, triggers, termination rights.
7. **Long-only:** SMA or commingled vehicles; ADV coverage; transition costs; tax.
8. **Treasury:** composition, and whether the 8% includes encumbered IM.
9. **Unfunded by group,** including DDTL/revolvers and deferred consideration.

**Organization:** mandates, budgets and authorities; funding baskets; IC recusal practice; pay, deferral and clawback constraints; transfer history, with SPV and tax frictions; whether CF can hold the FTP mismatch.

**Forecasts:** a point-in-time archive with authorship, or a registry start date; the declined-deal list; each group's format, horizon and gross/net basis.

**Synthetic data:** holding counts, sizes and vintages; NAV lags; the overlay trade and CSA inventory; whether synthetic packs may appear in IC rehearsal, and who signs off the labels.

**Definitions to settle:** the Form PF portfolio-liquidity basis (gross or net assets; the verifiers differ); the SEC–OFR leverage gap; gross vs net in Busse–Goyal–Wahal; extraction of GLM's fund-level θ tables.

---

## 8. Reproducibility

- **Stream scripts:** `research/groups/verification/G5_public_markets_examples.py`; `research/groups/addenda/G7_calcs/g7_liquidity_ladder_calcs.py`; `research/groups/verification/G8_org_calcs.py`; the G9 prototypes (G9 §7).
- **This synthesis:** `research/groups/addenda/GC2_calcs/`, run with the project venv as `python -I`.
  - `gc2_reconcile.py` writes `gc2_reconcile_results.json`. It loads the G7 module unmodified and reproduces it exactly.
  - `gc2_hf_split_variant.py` writes `gc2_hf_split_variant_results.json`.
  - `gc2_extra_checks.py` writes `gc2_extra_checks_results.json`.
- **Sources:** every primary source, with its URL, is in the dossiers' §10 reference lists and the verification logs.

*SYNTHETIC – NOT ADIC DATA (all [I-calc] figures).*

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2; the G5, G7, G8 and G9 citation tables in `research/literature/`. Metadata was taken from those audited tables.

- §4.4 "Flows by group", Private Credit: added Li–Strahan–Zhang's own condition that banks met the March 2020 line draws thanks to Fed liquidity programs, deposit inflows and strong capital, and that an oil- or fiscal-specific stress may lack that support [I] (audit §2.4 item 14).
- §5 "Revolver dash for cash": the same condition added, with *RCFS* 9(3):472–500 (audit §2.4 item 14; G7 table).
- §2 G8 row: the Shin–Stulz note now says that NBER w5639 is a different 1996 paper and that the *QJE* 113(2):531–552 citation stands (audit §2.3).
- §2 G7 row: the WilmerHale source is identified as "Trends in the Private Equity Secondary Market", ABA *Business Law Today* 18(4), 2009 (audit §2.3, stream 05).
- §2: one erratum line added below the ledger. The G8 verification log accepted Lamont (1997) with the wrong pages (audit §2.3).
- Checked, no change: "central Treasury" is already read as CF (naming note; audit §2.4 item 14); Campbell–Sharpe already calibrates w_a or ρ_f, not w_u (§4.6 O4; audit §2.4 item 8); Getmansky–Lo–Makarov, Ang–Bollen, Aragon, Cipriani et al. and Busse–Goyal–Wahal match the G5 table. GC2 quotes no G4 barrier statistic, and its 5%-LTV NAV facility with forced paydown is a contractual model step that the barrier fix does not touch (`research/groups/addenda/G4_barrier_rerun/RESULTS.md` §2, row 7). It cites none of the works in the stream 10, 11, 13 and 14 re-checks, and gives no Bühlmann DOI, so the cross-file Bühlmann conflict does not reach it.
