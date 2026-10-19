# Gap 03 addendum: a factor and Greek layer for the overlay's OTC books

**Date:** 2026-10-18 · **Closes:** gap 03, "the overlay module cannot represent ADIC's multi-asset OTC books" · **Amends:** synthesis §4.1 (E), §4.6 (overlay), §7.2 item 8 (blotter), §8 (validation) · **Tags:** as synthesis §0 · **Data:** no ADIC data. Worked examples are synthetic or computed on public data. Scripts and JSON outputs are in `research/addenda/gap_03_calcs/` (`gap03_greek_layer_calcs.py`, `simm_offset_example.py`).

---

## 1. What changes, and five findings

The overlay becomes a **position layer**. Every trade (or, until ADIC's blotter arrives, every strategy family) is a template priced on arbitrage-free surfaces driven by the scenario generator's factors. One set of sensitivities then feeds five consumers: P&L, VM by CSA, initial margin (IM), net-Greek limits, and the liquidity ledger behind λ. C3's strategy-family Sharpe process survives only as a shrunk residual-skill term.

**Findings** (public data to 16 Oct 2026; [I-calc] unless tagged):
1. **Vega does not net one-for-one across tenors.** On days VIX rose ≥3 points, 3-, 6- and 12-month VIX moved 0.64, 0.42 and 0.26 points per VIX point. Across six spikes since 2018 the ranges were 0.56–0.76, 0.36–0.56 and 0.23–0.35. SIMM sums equity, FX and commodity vega across expiries [S]. In a worked example (§7.4), a short 1-month book that SIMM sees as exactly offsetting a long 6-month tail sleeve loses $1.77 per $1 the sleeve gains in a 2020-type spike, and putting both books under one CSA cuts posted IM by 31%.
2. **No VIX-level conditioning reproduces the short-vol Sharpe template.** A short-variance proxy has Sharpe 1.4–2.0 *entering* every V-state (V0–V3). Its losses sit in transitions (blocks entering ≤V2 that touch ≥V3: Sharpe −0.57, 17% of blocks) and in V4 (−1.43).
3. **The sign of rates spot–vol depends on the regime.** The daily correlation of Δln MOVE with Δ10y yield was −0.30 in Sep–Dec 2008, −0.40 in Feb–Apr 2020, −0.43 in March 2023 and +0.24 in Jan–Oct 2022.
4. **So does the sign of oil skew dynamics.** OVX rose 1.49 points per 1% Brent *fall* in the 2020 demand bust, but 0.61 per 1% *rise* in the 2022 supply shock. In 2026 it rises and falls with oil.
5. **Contractual IM is sticky; liquidity risk sits in VM and in a deferred IM step.** In March 2020 non-cleared IM "remained relatively stable" while cleared IM rose ≈$300bn [S: BCBS–CPMI–IOSCO 2022]. COVID volatility entered SIMM only in December 2021, with v2.4 [S: Clarus 2021]. Under today's semiannual cycle the lag is ≈6–12 months [I].

---

## 2. Architecture: one position layer, five consumers

```
blotter or family exposures -> instrument templates -> pricers on surfaces(S, Z, V, factors)
  -> MTM, CRIF-style sensitivities, stress P&L -> P&L | VM by CSA | IM | net-Greek limits | ledger and λ
```

- **Two representations, one interface.**
  - *Level 1*, before the blotter: each opportunistic family is a set of factor exposures (§4).
  - *Level 2*: the loaded blotter (§7.2 item 8). Each trade maps to one of ≈15 templates: index futures and TRS; listed and OTC index options; variance swaps; VIX futures and options; cleared IRS; swaptions; FX forwards and options; Brent futures and options; CDX indices and index options; dual digitals; worst-of and conditional puts.
- **P&L.** Outside stress windows:
  $$\Delta V_b\approx\textstyle\sum_k\delta_{b,k}\Delta f_k+\tfrac12\sum_{k,l}\Gamma_{b,kl}\Delta f_k\Delta f_l+\sum_j\nu_{b,j}\Delta\sigma_j+\Theta_b\Delta t$$
  Full revaluation runs monthly, in daily stress sub-steps (C3 §4.2) and at triggers. The explain test (§9, T3) decides where the Taylor form may be used.
- **VM by CSA c.**
  - Required collateral $C^\ast_{c,t}=\mathrm{sgn}(V_{c,t})(|V_{c,t}|-H_c)^+$, with party-specific thresholds $H_c$. A transfer $VM_{c,t}=C^\ast_{c,t}-C_{c,t-1}$ occurs only if it is at least $MTA_c$, settled T+1.
  - Recognition uses C3's φ (1 / 0.7 / 0). Independent amounts and posted IM are encumbered.
  - Daily VM and IM ladders by CSA feed the 30-day coverage row (synthesis T3).
- **One sensitivity definition.** Sensitivities follow SIMM §C (1bp for rates and credit; 1% relative for equity, FX and commodity; one vol point with skew and smile fixed), so one CRIF file serves risk and margin [S: SIMM ¶20–30].

---

## 3. Scenario-generator extensions

E already carries log VIX, skew, the curve, Brent, USD and credit spreads (synthesis §4.1). Add a tenor map for VIX and four implied-vol states, each mean-reverting to a regime level with a regime-signed spot–vol term.

| State | Dynamics (monthly; daily in stress) | Calibration facts [I-calc unless S] |
|---|---|---|
| VIX term structure | $\Delta\sigma_T=\beta(T)\,\Delta VIX$ with $\beta(T)\approx0.94\,(T/30d)^{-0.43}$; feeds SSVI's θ_τ | Daily β (all days): 9D 1.52, 3M 0.64, 6M 0.45, 1Y 0.30. Spike ranges as in finding 1 |
| log MOVE | $\Delta\ln M=\kappa_M(\ln\bar M_S-\ln M)\Delta+b_S\,\Delta y_{10}+\eta_M\sqrt\Delta z$ | $b_S$ per +10bp: −1.5% (2008), −4.3% (2020), −3.2% (Mar 2023), +1.5% (2022). Correlation positive in 16 of 24 years. Peaks: 264.6 (10 Oct 2008), 163.7 (9 Mar 2020), 160.7 (12 Oct 2022), 182.6 (20 Mar 2023); 101 on 16 Oct 2026 (G9). MOVE tracks 1-month OTC options on 2/5/10/30-year Treasuries [S: ICE 2019] |
| Oil vol (OVX-type) | $\Delta O=\kappa_O(\bar O_Z-O)\Delta+s^{up}_Zr^++s^{dn}_Zr^-+\eta_O\sqrt\Delta z$ | $s^{dn}$ / $s^{up}$ per 1% Brent move: 2014–16 glut −0.45 / −0.06; 2020 bust −1.49 / −0.14; 2022 supply shock −0.06 / +0.61; 2026 YTD +0.45 / +0.49. OVX: median 35, p95 61, max 325 (21 Apr 2020), 50.7 on 16 Oct 2026; OVX/VIX median 2.0 (3.3 in 2026). OVX applies the VIX method to USO options [S: Cboe 2008] |
| FX vol and risk reversals | log G10 1-month ATM composite; RR by currency | Carry currencies are negatively skewed [S: Brunnermeier–Nagel–Pedersen 2009]. Pair data not yet obtained |
| CDX spread vol | lognormal spread vol regressed on VIX by regime; spreads from E's credit factor | CDX vol history not obtained (G9 §9) |

---

## 4. Opportunistic book: exposure templates instead of a Sharpe process

Each family *f* is a rule that maps E's observable state to exposures. Its P&L is then generated by the same factor paths that drive the rest of the fund:
$$r^f_t=\underbrace{\textstyle\sum_k\delta^f_{k,t}\Delta f_{k,t}+\tfrac12\Gamma^f_t(\Delta f)^2+\sum_j\nu^f_{j,t}\Delta\sigma_{j,t}+(\Theta^f_t+c^f_t)\Delta}_{\text{factor and premium P\&L from E}}+\alpha^f\Delta+\varepsilon^f_t+J^f_t$$

| Family | Templates | Exposure rule | Premium earned | Crash channel |
|---|---|---|---|---|
| Trend | ≈40 futures across equity, rates, FX and commodities | $\delta_{k,t}=L\,\mathrm{sgn}(\sum_{s\le12}r_{k,t-s})\,\sigma^\ast/\hat\sigma_{k,t}$ | none built in; positive skew from path dependence [S: Sepp–Lucic 2026] | reversal at regime turns (Mar–May 2009), generated endogenously |
| Carry | FX forwards, receivers at steep curve points, backwardated commodities, short CDX protection | rank-weighted carry signal, scaled to target vol [S: Koijen et al. 2018] | carry and roll-down $c_t$ | FX and spread jumps in crisis states; crowding $J$ |
| Relative value | DV01-neutral curve, swap-spread, basis and swaption-vol trades | spread exposures with near-zero net delta | mean reversion of spreads | funding-liquidity jump $J$, since E has no basis factors |
| Short vol | short variance swaps, delta-hedged short strangles, short VIX futures | $\nu<0$, $\Gamma<0$, $\Theta>0$; P&L ≈ $\tfrac12\Gamma S^2(\sigma^2_{real}-\sigma^2_{imp})\Delta+\nu\,\Delta\sigma$ | variance risk premium (mean 4.1 vol pts; synthesis §7.1) | vol transitions, generated endogenously |

**Consistency with the Sharpe templates.** Two rules prevent double counting.
1. **Premia live in E; skill lives in α.**
   - Set $\alpha^f=SR^{post}_f\sigma_f-\mathbb E[\text{factor P\&L}_f]$, then shrink and DSR-gate it as in C3.
   - If α < 0, the family's premia already exceed its posterior, and no skill is credited.
2. **Calibrate to transitions, not levels.** Short-variance proxy: SPX, 1990–2026, 21-day blocks, strike = VIX at entry, gross Sharpe ratios [I-calc]:

| Conditioning | V0 | V1 | V2 | V3 | Tail cases |
|---|---|---|---|---|---|
| C3 template | 0.9 | 0.6 | 0.0 | −2.0 | — |
| V-label at entry | 1.46 | 1.97 | 1.43 | 1.54 | — |
| V-label at exit | 6.56 | 4.25 | 2.86 | 0.35 | — |
| Highest label in block | 11.3 | 6.35 | 4.75 | 1.44 | V4: −1.43 |
| Entered ≤V2, touched ≥V3 | | | | | −0.57 (17% of blocks) |

- **Unconditional:** Sharpe 0.97, skew −9.5. The worst block, starting 14 Feb 2020, lost 252 vol points per unit vega notional.
- **Look-ahead caveat:** exit- and highest-label figures condition on the future, so they are not investable. They show that a template keyed to the VIX level mixes premium harvest with spike losses. The Greek layer separates the two by construction.
- **Calibration targets:**
  - fit each family's simulated moments, by entry state and by transition, to ADIC's own P&L (§7.2 item 10) and to these proxies;
  - keep the trend and carry templates only as priors until that P&L arrives.

---

## 5. Arbitrage-free surfaces

| Asset | Market convention | Model at each node | Anchor in E | No-arbitrage gate |
|---|---|---|---|---|
| Equity index | strike × expiry | SSVI (existing); θ_τ from VIX9D–VIX1Y via β(T) | VIX term structure, SKEW | Gatheral–Jacquier conditions plus numerical butterfly and calendar checks |
| Rates (swaption cube) | normal vol by expiry × tenor × strike | normal SABR per (T, τ), with $\sigma^N_{ATM}(T,\tau)=MOVE_t\,m_S(T,\tau)$ and ρ, ν by regime | log MOVE, regime-signed $b_S$ | density ≥ 0 via arbitrage-free SABR [S: Hagan et al. 2014] or free-boundary SABR [S: Antonov–Konikov–Spector 2015] |
| FX pairs | ATM, 25Δ and 10Δ risk reversals and butterflies; delta and ATM conventions per pair [S: Reiswich–Wystup 2010] | SABR (β = 1), or vanna–volga interpolation [S: Castagna–Mercurio 2007] | FX vol composite; RR state | call prices convex and monotone in strike |
| Brent | Black-76 on ICE futures | SVI per expiry; ATM term structure from the Schwartz–Smith two-factor model [S: 2000]; skew sign keyed to Z (finding 4) | oil vol state, Z | as for equity |
| CDX options | Black on the forward spread | loss-adjusted forward with front-end protection [S: Pedersen 2003], under the no-armageddon measure [S: Morini–Brigo 2011]; SABR smile in spread | credit factor; spread vol | payer–receiver parity including front-end protection |

---

## 6. Hybrids and joint-state options: a regime-mixture factor copula

- **Marginals** come from each asset's own surface (Breeden–Litzenberger), so skew enters directly:
  $$u_i=Q(X_{i,T}\le K_i)=e^{rT}\,\partial P_i/\partial K\big|_{K_i}=N(-d_2)+K_i\,\varphi(d_2)\sqrt T\,\sigma_i'(K_i).$$
- **Dependence** is a mixture, over E's regimes, of Gaussian or t copulas: $C^Q(u)=\sum_sq_s\,C_{R_s}(u)$, with risk-neutral weights $q_s$ fitted to quotes.
  - $R_s$ comes from the regime correlations; oil–equity ρ_Z runs from −0.5 in GW to +0.6 in DB (C3 §5.1).
  - A mixture of copulas is itself a copula, and it produces the correlation skew a single Gaussian cannot.
- **Prices.**
  - A dual digital paying if oil < K₁ and equity < K₂ at T is worth $D_T\,C^Q(u_1,u_2)$.
  - Worst-of and conditional puts are valued by Monte Carlo on the same copula, with common random numbers.
  - Stulz (1982) closed forms serve as a flat-vol check [U].
- **Dealer check.**
  - Every hybrid needs ≥3 dealer quotes, stored in the `quote` table with conflict flags.
  - Invert each quote for an implied correlation. Reject the trade if quotes imply correlations more than 0.15 apart, or if the model price falls outside the bid–offer [I].
  - Then apply the existing Q-vs-P test: buy only if $P^Q(\text{joint down})<(1-m)\,P^{P,adj}$, with m = 25% (C3 §5.3e).
- **Correlation is the first-order risk.**
  - At 2026 vols (oil 70%, equity 20%), a one-year dual digital (oil < 80%, equity < 90%) costs 7.4%, 12.5% and 20.4% of notional at ρ = −0.4, 0 and +0.6 [I-calc, stream 03].
  - SIMM's only correlation risk factor is credit base correlation [S]. Dealers may therefore require an add-on or multiplier (SIMM §L) or an independent amount. Price that IM into the trade.

---

## 7. SIMM-like initial margin from the same sensitivities

### 7.1 Formulas

Source: ISDA SIMM v2.8+2512, effective 11 July 2026, calibrated to data through 31 December 2025 [S: ISDA, 12 Jun 2026]. Computed per CSA, product class (RatesFX, Credit, Equity, Commodity) and risk class.

- **Delta.**
  - Weighted sensitivities: $WS_k=RW_k\,s_k\,CR_k$.
  - Within a bucket: $K_b=\sqrt{\sum_kWS_k^2+\sum_{k\ne l}\rho_{kl}f_{kl}WS_kWS_l}$.
  - Across buckets: $\sqrt{\sum_bK_b^2+\sum_{b\ne c}\gamma_{bc}S_bS_c}$, with $S_b=\max(\min(\sum_kWS_k,K_b),-K_b)$.
- **Vega.**
  - Equity, FX and commodity: $VR_{ik}=HVR\sum_j\sigma_{kj}\,\partial V_i/\partial\sigma$, with $\sigma_{kj}=RW_k\sqrt{365/14}/\Phi^{-1}(0.99)$.
  - Rates and credit: σ is the ATM swaption vol by expiry.
  - Then $VR_k=VRW\cdot\sum_iVR_{ik}\cdot VCR_k$, aggregated in the same two levels.
- **Curvature.**
  - $CVR_{ik}=\sum_jSF(t_{kj})\,\sigma_{kj}\,\partial V_i/\partial\sigma$, with $SF(t)=0.5\min(1,14/t)$: 23.0% at 1 month, 3.8% at 6 months, 1.9% at 12 months.
  - Margin: $\max(\sum CVR+\lambda\sqrt{\cdot},0)$, with $\lambda=(\Phi^{-1}(0.995)^2-1)(1+\theta)-\theta$.
- **Totals.** $SIMM_p=\sqrt{\sum_rIM_r^2+\sum_{r\ne s}\psi_{rs}IM_rIM_s}$ per product class; total SIMM is the sum over the four product classes.

### 7.2 Parameters for ADIC's main risk factors [S: SIMM v2.8+2512]

| Risk class | Delta risk weight | HVR | VRW | Notes |
|---|---|---|---|---|
| Rates, USD | 107 (2w), 61 (5y), 60 (10y), 66 (30y) | 0.74 | 0.20 | cross-currency γ 35% |
| Equity indexes (bucket 11) / volatility indexes (12) | 15 / 15 | 0.56 | 0.29 / 0.72 | vol-index curvature set to zero |
| Crude oil (commodity bucket 2) | 21 | 0.81 | 0.34 | intra-bucket ρ 97% |
| FX, regular currencies | 7.4 | 0.67 | 0.33 | FX ρ 50% |
| Credit qualifying | IG 44–75; HY 136–423 | — | 0.42 | base-correlation risk weight 9.7 |

Store parameters as tables versioned by ISDA release. Calibration is now semiannual: v2.8+2506 used data to 30 June 2025 and took effect on 6 December 2025 [S: ISDA, 31 Oct 2025].

### 7.3 Four properties that change ADIC's numbers

1. **Expiry netting.** For one equity, FX or commodity underlying, vega is summed across expiries: "the USD/JPY FX vega is the sum of all vol-weighted USD/JPY FX vegas" (¶10c). Rates vega is bucketed by expiry. SIMM therefore cannot see the term-structure basis in finding 1.
2. **Short-dated gamma dominates.** Curvature weights fall from 23.0% at 1 month to 1.9% at 12 months, so short-dated opportunistic options drive curvature IM.
3. **Asymmetry.** Curvature is SIMM's only one-sided term. IM to post is computed on sign-flipped sensitivities [S: ActiveViam SIMM documentation], so the party that is net short gamma posts it.
4. **Stickiness.**
   - SIMM is calibrated on three recent years plus one stress year [S: Clarus 2021] and is "weakly affected by sharp market fluctuations" [S: PRA, 28 Jun 2022]. The PRA warned that coverage may fall below 99% for some counterparties.
   - Model a **deferred IM step** at each recalibration date after a stress.
   - Keep VM stress as the binding constraint. SIMM's 10-day delta weight for a volatility index is 15%, while spot VIX rose 115.6% on 5 February 2018 (stream 09).

**Licensing.** The methodology notice permits use "solely for the purpose of a market participant's own commercial transactions"; service providers need a licence [S: SIMM footnote 1]. Reconcile against a licensed calculator.

**Simulation.**
- Propagate node sensitivities by Taylor expansion (Δ′ ≈ Δ + ΓΔf + vanna·Δσ; ν′ ≈ ν + vanna·Δf + volga·Δσ), with full recomputation in stress sub-steps.
- Aggregation is a few quadratic forms per CSA, so compute it directly; regression proxies degrade on diversified portfolios [S: Caspers et al. 2017].
- Schedule IM, cleared IM (EWMA with anti-procyclicality) and independent amounts remain as in C3 §5.4d.

### 7.4 Worked example: what SIMM nets, a stress does not [I-calc; synthetic]

Two delta-hedged books on one index:
- a tail sleeve long 6-month puts, vega +$10m per vol point;
- an opportunistic book short 1-month straddles, vega −$10m.

IM to post, equity risk class, $m:

| | Vega margin | Curvature margin | Total |
|---|---|---|---|
| Separate CSAs (tail / opportunistic) | 53.5 / 53.5 | 0 / 502.7 | 609.7 |
| Same CSA | 0 | 418.9 | 418.9 (−31%) |

- **SIMM reads zero net vega; the stress does not.** VIX-equivalent vega is +$4.2–5.6m for the sleeve (β₆ₘ 0.42–0.56) against −$10m for the short book. The combined book is net short $4.4–5.8m per VIX point.
- **2020 replay (14 Feb–16 Mar; VIX +69.0, VIX6M +38.9):**
  - the sleeve gains ≈$389m on vega alone;
  - the short book loses ≈$690m;
  - the offset ratio is 1.77, before gamma.

---

## 8. Governance rules made computable

- **Economic net vega.** $NV^{eq}(s)=\sum_b\sum_j\nu_{b,j}(s)\,\beta(T_j)$, evaluated after revaluation in stress state *s*, so vanna and volga count. MOVE- and OVX-equivalent vegas use the β maps of §3.
- **L1 vega floor** (makes §4.6 precise): $NV^{eq}_{overlay}(s)\ge0.75\,NV^{eq}_{tail}(s)$ at V3 entry and in the 1987-, 2018- and 2020-type stresses [I]. In §7.4 this caps the short 1-month vega at ≈$1.1–1.4m per vol point, not $10m.
- **L2 offset ratio:** $OR(s)=(-P\&L_{opp}(s))^+/P\&L_{tail}(s)\le25\%$ in every named stress, by full revaluation [I].
- **L3 short-dated gamma budget:** opportunistic curvature IM ≤ an IC-set share of the overlay's IM budget.
- **CSA rule.**
  - Govern offsets on economics (L1–L3), independent of CSA.
  - Then allocate trades to CSAs for margin efficiency, within dealer limits (≤0.5% of NAV per dealer).
  - Once L1–L3 hold, the IM saved by sharing a CSA is legitimate and is credited at λ^w. Before they hold, it is a hidden short-vol position.
- **IC offset card**, per named stress: tail and opportunistic P&L, the offset ratio, economic vs SIMM net vega, IM by CSA, and the λ-priced IM saving.

---

## 9. Validation

### 9.1 Synthetic blotter (G9 SYN-ADIC-177; labelled SYNTHETIC)

| Book | Trades | Templates | Gross notional |
|---|---|---|---|
| Tail stack | ≈70 | SPX/SX5E put spreads on a 3/6/12-month ladder, VIX calls, CDX HY payers, CDX IG protection, Brent put spreads, 3–5 hybrid shells | ≈$25bn |
| Opportunistic | ≈150 | trend futures, FX carry forwards and options, IRS and swaption RV, CDX carry, short strangles and variance swaps | ≈$45bn |
| Synthetic beta | ≈30 | index futures and TRS, Treasury futures, cleared IRS | $0–10bn |

The 12 CSA archetypes cover:
- both IM regimes: two-way SIMM, and independent-amount-only for a sovereign-exempt status;
- zero and non-zero thresholds; MTAs of $0.5–5m;
- cash-only vs UST-eligible collateral; reuse vs pledge; rating triggers;
- two GCC dealers (wrong-way in GW and PS).

At least four dealers face both books.

| Test | Pass criterion [I unless S] |
|---|---|
| T1 Pricing | each template within 0.5% of vega (or 1bp) of QuantLib/ORE references; every simulated surface node passes its §5 gate |
| T2 Sensitivities | analytic vs bump-and-reval on SIMM definitions, within 1% |
| T3 P&L explain | Taylor vs full revaluation on 250 daily scenarios per book. Green: Spearman > 0.80 and KS < 0.09. Red (< 0.70 or > 0.12) forces full revaluation in that state [S: BCBS MAR32 thresholds, as documented by MathWorks] |
| T4 IM | SIMM-like vs a licensed calculator within ±1% per product class and CSA; schedule IM and independent amounts reproduced exactly |
| T5 Seeded offset | the §7.4 position, planted in one CSA, must breach L1 and L2 while SIMM vega margin reads ≈0 |
| T6 Reconciliation | Level-2 sensitivities aggregated by family within 10% of Level-1 exposures (DV01, CS01, equity delta, VIX-equivalent vega) |

### 9.2 Replays (pre-registered; sign and Tier-1 checks only, per synthesis §8)

Daily public factor moves are replayed through the synthetic blotter. The output is VM and IM ladders by CSA, plus the blotter's through-the-cycle look-back floor (synthesis §4.6).

| Window | External evidence | The replay must show |
|---|---|---|
| Sep–Dec 2008 | Collateral against OTC derivatives grew from $2.1trn to ≈$4.0trn during 2008 (+86%) [S: ISDA Margin Survey 2009]; MOVE peak 264.6 (10 Oct); VIX 80.86 (20 Nov) | tail VM inflows recognised at φ = 0.7; negative rates spot–vol; a dealer default handled by the counterparty module |
| 19 Feb–30 Apr 2020 | Peak CCP VM call $140bn (9 Mar); cleared IM up ≈$300bn over March; non-cleared IM "relatively stable" [S: BCBS–CPMI–IOSCO 2022]; some CCPs' IM > +100% q/q [S: FSB 2020] | SIMM-like IM moving only through sensitivities, far less than cleared IM; peak-day VM ≫ daily ΔIM; the SIMM step deferred to the next version |
| Jan–Oct 2022 | Non-cleared IM at phase-one firms +7.4% y/y to $307.2bn, against cleared IRD and CDS IM +18.8% to $384.4bn [S: ISDA Margin Survey YE-2022, 9 May 2023]; 30-year gilts > +270bp (BoE FSR, Dec 2022) | positive rates spot–vol; duration legs failing as hedges; margin calls on short oil calls (call skew); cleared IM growing faster than SIMM-like IM |

---

## 10. Design changes, data and sequencing

1. **§4.1:** add MOVE, oil vol, FX vol and risk reversals, CDX vol and the β(T) map. Key spot–vol signs to S and Z.
2. **§4.6:**
   - Replace the opportunistic Sharpe process with exposure templates plus residual α.
   - L1–L3 replace the verbal vega floor.
   - Adopt the CSA rule and the IC offset card.
3. **Overlay engine:**
   - §5 surfaces;
   - §6 copula pricer with the dealer check;
   - §7 SIMM-like engine with versioned parameters and the deferred IM step.
4. **§7.2 item 8:**
   - blotter fields with CRIF output;
   - daily VM and IM by CSA; SIMM version history;
   - market data: the swaption cube, FX risk reversals and butterflies, ICE Brent options, OVX and CDX option vols;
   - dealer hybrid quotes with correlation marks.
5. **§8 and the lab:**
   - T1–T6 and the three replays.
   - Surface gates and the explain test become rubric checks in gates G3–G6.
   - New typed tools: `price_trade`, `crif_sensitivities`, `simm_like`, `greek_offsets`, `hybrid_quote_check`.
   - The red team searches for opportunistic books that pass L1–L3 but breach L2 in an unnamed stress.
6. **Sequencing:**
   - *Phase 0 (months 0–3):* equity SSVI with β(T), Level-1 templates, the SIMM-like engine, L1–L3, and the 2020 replay on public data.
   - *Phase 1 (months 3–9):* the SABR cube, FX, Brent, CDX and hybrids; the 2008 and 2022 replays; reconciliation to a licensed SIMM and to dealer calls.

**Open questions for ADIC:**
- the IM regime that applies to ADIC;
- whether net short volatility is allowed (C3 Q16);
- CSA terms;
- dealer overlap between the two books.

---

## Sources

**Data, retrieved 2026-10-18:**
- Cboe daily index files (VIX, VIX9D, VIX3M, VIX6M, VIX1Y, SPX, OVX), https://cdn.cboe.com/api/global/us_indices/daily_prices/
- Yahoo Finance ^MOVE
- Federal Reserve GSW yield curve (feds200628)
- EIA Brent daily (RBRTE)

**Margin methodology, regulation and evidence:**
- ISDA (2026). SIMM Methodology v2.8+2512, https://www.isda.org/a/hhkiE/ISDA-SIMM_v2.82512_PUBLIC.pdf; announcement 12 Jun 2026, https://www.isda.org/2026/06/12/isda-publishes-isda-simm-methodology-version-2-8-2512/
- ISDA (31 Oct 2025). SIMM v2.8+2506, https://www.isda.org/2025/10/31/isda-publishes-isda-simm-methodology-version-2-8-2506/
- Clarus (2021). ISDA SIMM v2.4: Covid calibration, https://www.clarusft.com/?p=28856
- PRA (28 Jun 2022). Review of the use of the SIMM model, https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/letter/2022/june/simm-model.pdf
- ActiveViam. SIMM 3.0, post and collect modes, https://docs.activeviam.com/solutions/simm/3.0/calculations/post-and-collect-modes.md
- BCBS–CPMI–IOSCO (29 Sep 2022). Press release on margining in March 2020, https://www.bis.org/press/p220929.htm
- ISDA (2009). Margin Survey 2009, https://www.isda.org/a/eeiDE/isda-margin-survey-2009.pdf
- ISDA (9 May 2023). Margin Survey Year-End 2022 press release, https://www.isda.org/a/cCLgE/ISDA-Margin-Survey-Shows-1.4-Trillion-in-Margin-Collected-at-Year-end-2022.pdf
- MathWorks. Profit and loss attribution workflow (MAR32 thresholds), https://kr.mathworks.com/help/risk/profit-and-loss-attribution-workflow.html
- Caspers, Giltinan, Lichters & Nowaczyk (2017). Forecasting initial margin requirements. *J. Risk Mgmt Fin. Inst.* 10(4), 365–394, https://hstalks.com/article/2900/forecasting-initial-margin-requirements-a-model-ev/

**Volatility indices:**
- ICE (5 Aug 2019). MOVE acquisition release, https://ir.theice.com/press/news-details/2019/Intercontinental-Exchange-Announces-Agreement-to-Acquire-the-Merrill-Lynch-Option-Volatility-Estimate-MOVE-Index-from-Bank-of-America-Merrill-Lynch/default.aspx
- Cboe (2008). OVX launch, via https://mondovisione.com/media-and-resources/news/cboe-introduces-new-crude-oil-volatility-index-ovx-new-benchmark-applies-vix-met-2011124/

**Pricing models:**
- Hagan, Kumar, Lesniewski & Woodward (2014). Arbitrage-free SABR. *Wilmott*, Jan, 60–75.
- Antonov, Konikov & Spector (2015). The free boundary SABR. *Risk*, Sep, https://www.risk.net/2423287
- Reiswich & Wystup (2010). A guide to FX options quoting conventions. *J. Derivatives* 18(2), 58–68.
- Castagna & Mercurio (2007). The vanna–volga method for implied volatilities. *Risk*, Jan, 106–111.
- Pedersen (2003). Valuation of portfolio credit default swaptions. Lehman Brothers QCR.
- Morini & Brigo (2011). No-armageddon pricing of credit index options. *Math. Finance*; arXiv:0812.4156.
- Schwartz & Smith (2000). Short-term variations and long-term dynamics in commodity prices. *Mgmt Sci.* 46(7), 893–911.
- Stulz (1982). Options on the minimum or maximum of two risky assets. *JFE* 10 [U].

**Other references:**
- Gatheral & Jacquier (2014). Arbitrage-free SVI volatility surfaces. *Quant. Finance* 14(1), 59–71. https://doi.org/10.1080/14697688.2013.819986
- Koijen, Moskowitz, Pedersen & Vrugt (2018). Carry. *JFE* 127(2), 197–225. https://doi.org/10.1016/j.jfineco.2017.11.002
- Brunnermeier–Nagel–Pedersen, Sepp–Lucic, FSB 2020 and BoE FSR 2022 are as listed in synthesis §11 and stream 09.

## Citation corrections (2026-10-18)

- §4 Carry row: "[S: Koijen et al.]" now reads "[S: Koijen et al. 2018]".
- Sources: Koijen, Moskowitz, Pedersen & Vrugt (2018), "Carry", *JFE* 127(2):197–225, is now listed in full, with DOI 10.1016/j.jfineco.2017.11.002. It was previously only a pointer to synthesis §11 and stream 09, where the metadata was incomplete. Venue and pages are from `research/literature/00_LITERATURE_SYNTHESIS.md` §2.5 and `09_overlay.lit.md`; the DOI was confirmed on Crossref.
- Sources: Gatheral & Jacquier (2014), "Arbitrage-free SVI volatility surfaces", *Quant. Finance* 14(1):59–71, is now listed in full, with DOI 10.1080/14697688.2013.819986. Stream 09 had left it unchecked. Metadata and usage were confirmed in `research/literature/recheck/10_scenarios_robustness.recheck.md` (row 14).
