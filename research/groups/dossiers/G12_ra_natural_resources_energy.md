# Stream G12: Real Assets: energy and natural resources (with agriculture and timber as excluded comparators). Oil linkage and wrong-way risk with the owner's draw

**Project:** ADIC multi-period robust TPA framework (agentic) · **Group:** 8, Real Assets · **Stream:** G12 · **As of:** 18 Oct 2026 · **Audience:** design/architecture, quant team, Real Assets head, Treasurer/Corporate Finance, IC secretariat

**Scope after the user's confirmation (design brief §8; context §1A, re-read 18 Oct 2026).** ADIC's Real Assets group holds real estate, infrastructure, and **energy and natural resources (ENR)**. **Agriculture and timber are excluded.** This dossier therefore treats ENR as a *held* book: how much oil exposure to keep, how to manage the existing positions, and how they enter the engine. Timberland and farmland appear only in §4.7, as zero-oil-beta comparators and as configuration placeholders. Power generation and energy-transition infrastructure belong mainly to G11. Here they appear only where oil or gas prices drive them.

**Evidence tags.** [S] sourced fact (§10); [P] practitioner consensus; [I] our inference or design proposal; [I-calc] our computation on public data; [I-MC] our stylised simulation (assumption-driven, not a forecast); [C] carried from a verified project document; [U] could not be verified in-session. Every book-level number is **SYNTHETIC – NOT ADIC DATA**.

**Reproducibility.** Scripts and JSON outputs are in `research/groups/addenda/G12_calcs/`:
- `g12_oil_betas.py`: listed-proxy oil loadings by era and by shock type (EIA Brent, Ken French 49 industries);
- `g12_episode_stats.py`: episode returns;
- `g12_wrongway_sim.py`: stream-03 oil/shock-type/draw model plus segment cash-flow models;
- `g12_hedging_demand.py`: liability oil exposure, hurdles and oil-delta budget;
- `g12_enr_book.py` and `g12_check_hedged_sleeve.py`: the synthetic ENR sleeve against the overlay's oil put spreads, before and after hedging;
- `g12_low_breakeven_check.py` and `g12_slope_check.py`: L_eff sensitivity to P^BE and b.

Raw downloads stay outside the project, in an isolated scratch folder.

**Session caveat.** A web-search budget shared by every agent ran out mid-stream. Some facts therefore rest on primary documents fetched directly, or on search summaries; those are flagged.

---

## 1. Executive summary

1. **For an oil sovereign's fund, oil-linked assets are a short hedge sold twice.** [I]
   - ADIC is already short a NAV-scaled put spread on oil through the owner's draw [C: main L3; 03 §2.3]. Inside the band, each $1/bbl moves the draw by ≈$200m on the linear map. That is ≈201m bbl of in-band delta [I-calc].
   - Upstream, royalty and oil-linked midstream assets add *long* oil delta. They lose value and cut distributions exactly when the draw rises.
   - **Evidence, 2014–16 supply glut** [I-calc, Ken French industries vs EIA Brent]: Brent −70%; the US equity market flat (−0.6%); listed oil and gas −38.5%, mining −45%, coal −88%; the UAE fiscal balance swung −8.1pp of GDP [C: 03]. Markets gave no cushion.

2. **The wrong-way loss is mostly cash and refinancing capacity, not volatility.** On stream 03's oil and shock-type model, with stylised segment models [I-MC, SYNTHETIC]:
   - **Distributions** relative to the normal state:

     | Segment | Supply glut (SG) | Demand bust (DB) |
     |---|---|---|
     | Unlevered proved-producing (PDP) upstream | 0.43× | 0.49× |
     | Oil royalties | 0.63× | 0.69× |
     | Fee-based midstream | 0.95× | 0.98× |

   - **Levered upstream.** With the borrowing base redetermined on a bank price deck at 40% loan-to-value (LTV), equity cures hit in 73% of SG and 69% of DB years, averaging 18–20% of equity. Net cash to ADIC turns *negative* (−0.29× normal). In spring 2016, borrowing bases were expected to fall 38% [S: Haynes Boone].

3. **The owner hurdle.** [I-MC]
   - In a surplus mean–variance frame, an oil-linked asset must earn a premium Δμ = γ·L_eff·Cov(r_j, Δln P).
   - L_eff is ADIC's effective liability oil exposure: the PV of extra draws per unit log-oil shock. It is **7.5–9.9% of NAV** for breakevens of $45–65.
   - The required premium at γ = 2–4, as an annual excess return on the asset:

     | Asset | Premium (p.a.) |
     |---|---|
     | Unlevered PDP | 1.2–2.4% |
     | Levered upstream equity | 2.4–4.8% |
     | Oil royalties | 0.9–1.9% |
     | Upstream with 70% of 3-year output hedged | 0.5–0.9% |
     | Midstream | 0.3–0.6% |
     | Timber, farmland | ≈0 |

   - A draw-utilisation weight gives the same order of magnitude. Stream 03's owner-state weight (κ_own = 1) gives 3–5× more and should be recalibrated (§6.4).

4. **Private energy has not earned that hurdle recently.** [S]
   - Cambridge Associates' (CA) natural resources composite: 11.2% a year from 1990, but only **3.2% from Q3-2013 to Q2-2023** (PE 15.2%).
   - Energy funds of 2004–14 vintages trailed PE by **0.56× net MOIC**, with correlation above 0.7 to markets and commodities since 2013.
   - A US pension's legacy energy book returned 0.7% a year over 10 years and −1.9% over 15 (Jun 2026), and is being wound down.
   - The 1986–2010 record (12.7% IRR) is a commodity-boom record.

5. **The 5–10% band saturates the owner's oil dependence.** [I-MC] L_eff stays within 7–10% of NAV across most plausible owner parameters:

   | Parameter varied | Range | L_eff (% of NAV) |
   |---|---|---|
   | Hydrocarbon share h | 6% → 15% of GDP | 7.1 → 9.3 |
   | Draw slope b | doubled | 9.3 → 10.0 |
   | Effective breakeven P^BE | $45 → $65 | 7.5 → 9.9 |

   - A steeper or more oil-dependent owner spends more time at the floor or cap, so the band absorbs the change.
   - L_eff falls materially only if the effective breakeven is low (≈$35: 4.8% of NAV) or ADIC controls the band (mandate Mode A). Either would roughly double the oil budget or more.
   - **Conditional rule:** ADIC's oil-linked holdings should be sized off L_eff, which the owner module publishes, rather than off the oil share of the owner's GDP.

6. **Recommendation: run ENR on an oil-delta budget netted against the owner.** [I]
   - **(a) No new unhedged oil-price-linked commitments** (upstream, oil-weighted royalties, oilfield services) while the draw sits in its active band.
   - **(b) Real Assets oil-delta budget** of **5m bbl-equivalent (soft) and 10m (hard)**, measured at the generator's current state. That is 2.5–5% of the in-band draw delta. It means ≈$0.5–1.1bn of 40%-LTV upstream equity, ≈$0.9–1.8bn unlevered, or ≈$2.4–4.8bn of 70%-hedged PDP.
   - **(c) The synthetic ENR sleeve breaches the hard limit.** G15's synthetic sleeve ($2.5bn: $1.6bn of funds, $0.9bn direct) carries **≈12m bbl**. That offsets **31–61% of the overlay's 20–40m bbl oil put-spread programme**. A glut year would cost it ≈$0.7bn (simulation) to ≈$1.0bn (2014–16 analogue), against a put-spread payoff of $0.38–0.76bn at $45 Brent. Either hedge 70% of its upstream output for three years (→ ≈6m bbl) or sell $0.6–0.8bn of its $1.07bn levered upstream (→ 4.9–6.7m bbl).
   - **(d) Use the Gulf-war window to SELL or hedge.** Upstream fund secondary pricing and demand rose in H1 2026 [S: Jefferies].
   - **(e) Prefer asset-level, unmargined hedges** secured pari passu under the reserve-based lending (RBL) facility [S: OCC] over overlay swaps. Overlay swaps return collateral in SG/DB but drain it in Gulf-war tails (P05 −15% of hedged value a year).

7. **REFINANCE and LEVER are oil-procyclical in ENR.** RBL borrowing bases and stream, royalty and VPP prices are all set off a strip or deck that falls in SG/DB [S: OCC; P]. REFINANCE is an option to exercise in normal or boom states, not a stress lever. Streams are the cleanest cash-out without selling control (Wheaton–BHP, Feb 2026: $4.3bn upfront plus 20% of spot) [S].

8. **The energy transition drifts the same factor.** Scenario ranges are wide [S]: IEA STEPS has an oil peak of ≈102 mb/d around 2030 against ≈113 mb/d in 2050 under CPS; NGFS needs ≈$300/tCO2 by 2035; 58% of oil reserves are unextractable by 2050 at 1.5°C. Transition risk lowers the long-run oil level, the *same* direction as the owner's structural risk. It enters as a drift on the oil factor, plus a reserve-life charge [I].

---

## 2. Core concepts and theory

### 2.1 The asset in the ground and the asset in the fund

**The owner's balance sheet** [C: 03 §2.1]. The owner's comprehensive wealth is $W^{own}=\sum_kF_k+V^{oil}+V^{tax}-V^G-B$. ADIC is one pocket $F_k$, and its outflow is the policy draw $D_t=d_tB_t$.

**Hedging demand with non-tradable resource wealth** [S: Gintschel & Scherer 2008; Scherer 2009, 2011; van den Bremer, van der Ploeg & Wills 2016]. The static mean–variance form is
$$w^*=\tfrac1\gamma\Sigma^{-1}(\mu-r\mathbf 1)-\tfrac{V^{oil}}{F}\Sigma^{-1}\sigma_{r,o}.$$
- Assets that co-move with oil carry *negative* hedging demand.
- Van den Bremer et al. integrate extraction and fund management:
  - subsoil oil should change the fund's portfolio through extra leverage and hedging;
  - spending is a share of total wealth;
  - unhedgeable volatility calls for precautionary saving.

**Practical rule from the IMF** [S: Brown, Papaioannou & Petrova 2010, WP/10/9].
- A stabilisation fund's strategic allocation "will, therefore, contain assets that have negative correlation with the respective commodity price" (p. 8).
- Putting oil reserves in the optimiser "will either force the financial assets into a short oil position or render the analysis meaningless". The remedy is to **pre-select** asset classes "uncorrelated with or countercyclical to the price of oil" (p. 19, citing Sharpe & Tint 1990).
- The IMF's 2014 SALM guidance and WP/18/26 put this on the integrated sovereign balance sheet [S].

**For ADIC the relevant liability is the draw, not the reserves** [I]. Stream 03 writes the target draw as a clipped linear function of the fiscal balance $FB_t=100h_t\ln(P_t/P^{BE})+w_{Z_t}+\epsilon_t$:
$$d^*_t=\Pi_{[5\%,10\%]}(c-b\,FB_t),\qquad d_t=\Pi(\rho d_{t-1}+(1-\rho)d^*_t).$$
ADIC is therefore short a NAV-scaled log-put spread. The kinks are ≈$64/$31 on the log form and ≈$67/$23 on the linear form at P^BE = $44.8 [C].

**Effective liability oil exposure** (this stream) [I]. A unit log-oil shock decays at φ = 1 − κ = 0.6 a year in the generator. It moves the draw only while $d^*$ is inside the band. The PV of extra draws per unit log-oil shock, as a fraction of NAV, is therefore
$$L_{eff}=b\,h\,\Pr(d^*\in\text{band})\sum_{k\ge0}\Big(\frac{\phi}{1+r}\Big)^k .$$
With b = 0.625, h ≈ 0.10 and r = 6%, it is 7.5% (P^BE $44.8), 9.3% ($55) and 9.9% ($65) of NAV [I-MC].

**Hurdle for an oil-linked asset** [I]. Treat the draw as a liability return $-L_{eff}\Delta\ln P$ and maximise $\mathbb E[r_p]-\tfrac\gamma2\mathrm{Var}(r_p+L_{eff}\Delta\ln P)$. The first-order condition gives each asset the extra required return
$$\Delta\mu_j=\gamma\,L_{eff}\,\mathrm{Cov}(r_j,\Delta\ln P).$$
Its minimum-variance hedge weight is $-L_{eff}\mathrm{Cov}(r_j,\Delta\ln P)/\mathrm{Var}(r_j)$. For unlevered PDP that is −12% of NAV: ADIC's hedging demand is negative, so a long-only book holds zero unless alpha clears $\Delta\mu_j$.

### 2.2 Wrong-way risk depends on the shock type

The six oil/fiscal states $Z\in\{N,B,SG,DB,SS,GW\}$ [C: 03 §2.4] map onto ENR assets as follows [I]:

| State | Oil | Owner draw | ENR value | ENR cash | Verdict for oil-linked ENR |
|---|---|---|---|---|---|
| SG (glut or price war; 1986, 1998, 2014–16) | ↓↓ | ↑ toward the cap | ↓↓ | ↓↓; RBL cures | **Wrong-way. Markets give no cushion** |
| DB (demand bust; 2008, 2020) | ↓↓ | cap | ↓↓ | ↓↓ | Wrong-way; the triple state (exits shut too) |
| GW (Gulf war or export-volume shock; 2026) | ↑↑ | ↑ (volume wedge) | ↑ for assets outside the Gulf | ↑ | **Right-way for upstream outside the Gulf**; Gulf-located assets suffer the volume risk |
| SS (stagflation spike; 1990, 2022) | ↑↑ | floor | ↑↑ | ↑↑ | Pays when the owner does not need it |
| B, N | ↑ / ~ | floor / low | + | + | Neutral |

- **Probability weights.** Under stream 03's prior, the wrong-way states (SG + DB) hold ≈22% of the stationary distribution and the right-way GW state ≈4% [I-MC].
- **The GW→SG transition** is 35% a year, encoding the post-war glut thesis.
- **Today** (Z0 ≈ GW at 0.85 [C]), out-of-Gulf upstream is temporarily right-way. The expected path runs into the state where it is most wrong-way.

### 2.3 The inflation hedge is right-way-redundant

Natural resources are sold as inflation hedges [S: Meketa 2024]. For ADIC the inflation they hedge best is *oil-driven*.
- In 2022 (SS), listed oil and gas rose 65% and coal 100% while the US market fell 20% [I-calc].
- In SS the owner is flush and the draw sits at the floor. The hedge pays where ADIC's marginal value of cash is lowest [I].
- Non-oil inflation hedges (real estate, infrastructure with CPI pass-through: G10, G11) carry no such redundancy.

### 2.4 Valuation building blocks

**Reserve-based NPV under the forward curve** [S: SEC 2008; OCC 2018; P].
$$V_t=\sum_{k\ge1}q_{t,k}\Big[F_t(k)\,\nu(1-\tau)-c^{LOE}-c^{G\&A}-c^{T}\Big]^+(1+\varrho)^{-(k-\frac12)}+\mathcal O_t$$
- ν is the net revenue interest (after royalty) and τ the severance and ad valorem taxes.
- $\mathcal O_t$ holds the shut-in, development and abandonment options [S: Brennan & Schwartz 1985].
- SEC reserves use "a 12-month average price, calculated as the unweighted arithmetic average of the first-day-of-the-month price" [S]. Booked reserves and PV-10 therefore lag the strip by about six months.
- **Production decline** follows Arps: $q(t)=q_i(1+bD_it)^{-1/b}$, with b ∈ [0, 1] conventional and b > 1 early shale.
- **Operating leverage** (cash elasticity to price) is $\nu(1-\tau)F/[\nu(1-\tau)F-c]$. That is ≈1.6 at $70 and ≈2.2 at $50 on our defaults.

**The forward curve the generator must supply** [I].
- The two-factor Schwartz–Smith model separates short-term from long-run shocks [S].
- The project's generator uses log-OU Brent with state drifts μ_Z [C]. The model-consistent median curve conditional on $(x_t,z_t)$ is
$$\ln F_t(k)=\bar x+\phi^k(x_t-\bar x)+\sum_{i=1}^{k}\phi^{k-i}\,(P_Z^{\,i}\mu)_{z_t}.$$
- This is what makes ENR values Z-dependent. In SG the curve drops by more than the spot move, because μ_SG persists.
- **Define the 3-year strip average** $F^{(3)}_t=\tfrac13\sum_{k=1}^{3}F_t(k)$, the factor used below and the natural hedge tenor. In the generator a 1% spot shock moves it by ≈0.39%.
- **Elasticities of value to a spot shock** under this curve [I-MC, at $70]:

  | Segment | Elasticity |
  |---|---|
  | Unlevered PDP | 0.39 |
  | 40%-LTV equity | 0.64 |
  | Royalties | 0.31 |
  | Fee-based midstream | 0.10 |

  These are the same order as Norges Bank's relative betas of global E&P (0.54) and pipelines (0.27) to 12-month WTI futures [S], and CA's 0.65 three-year oil sensitivity of private energy [S]. The bases differ: spot here, futures or three-year windows there.

**Other structures** [S/P].
- **Royalties and minerals:** no operating costs. Value ≈ volume × curve × (1 − tax), with volumes responding to operators' drilling.
- **Streams:** an upfront deposit buys a share of future metal at a fixed price or fixed share of spot (§4.5).
- **Volumetric production payments and ORRI carve-outs** are the oil-and-gas analogues [P].

**Timber and farmland (excluded).** Timber's ≈4–5% a year of biological growth makes harvest a real option: owners defer harvests at low prices ("store on the stump") [S: Meketa], and a reservation-price rule weakly dominates a fixed Faustmann rotation [S: Insley & Rollins 2005 and related work]. Farmland is capitalised rent plus land value.

---

## 3. Methods, models and trade-offs

| Need | Options | Trade-off | Recommendation [I] |
|---|---|---|---|
| Oil price and curve | GBM; log-OU; Schwartz–Smith two-factor; regime log-OU with μ_Z and GW jumps [C] | Two-factor fits the term structure; regimes carry shock type | Keep the project's regime model. Derive curves with the formula in §2.4. In production, anchor to ICE futures and add a P-measure risk-premium map |
| Direct upstream assets | Reserve-based DCF by category (PDP, PDNP, PUD); real options for development and shut-in (Brennan–Schwartz; Paddock et al. [U]) | DCF is transparent and matches the RBL engineering; options matter for PUD and shut-ins | DCF with a floor at zero netback (shut-in), plus a PUD development option by least-squares Monte Carlo (LSMC) |
| Closed-end ENR funds | RFT-TA cohort engine [C] with oil-elastic distributions; or factor model on NAV | Cohorts keep calls and distributions; factors keep risk | RFT-TA with $\delta=\bar\delta(a^e)\exp(\kappa_DX_t+\eta_{oil}\ln(F^{(3)}_t/\bar F))$ and NAV loading on $\Delta\ln F^{(3)}$ |
| Royalties, streams, midstream | Volume × price × contract; minimum volume commitments (MVCs) and take-or-pay floors | Contract detail drives oil beta (0.1–0.3) | Contract-level cash engine; midstream volume response to drilling |
| Owner linkage | Covariance hedging demand (GS); surplus optimisation; owner-state weights; λ-weights | Covariance demand is unstable by era [C: 03]; weights need calibration | Report all three in §6.4. **Decide on λ-weighted cash** once the optimiser publishes duals |
| Hedging | Asset-level swaps and collars inside the RBL; overlay swaps or options; put spreads at the draw kinks [C] | Asset-level hedges carry no VM but tenor ≤ 3 years [S: OCC]; overlay hedges are flexible but need collateral | Asset-level for production; overlay only for the residual oil-delta budget |
| Transition risk | Scenario overlays (IEA, NGFS); reserve-life (stranding) haircuts; carbon-cost pass-through | Scenario dispersion is the risk | Drift on the long-run oil factor, plus a carbon-cost term by asset, plus a reserve-life charge |

**Rejected** [I].
- Treating ENR as a generic "real assets inflation hedge" with a single beta: it hides SG/DB cash wrong-way.
- Putting the owner's reserves into the optimiser (the IMF warning).
- Spot-started oil states (main §4.1 already rejects them).
- Using SEC PV-10 or 12-month-average marks as current value without a lag correction.

## 4. Empirical evidence and current market data

### 4.1 Private natural resources and energy funds [S]

| Fact | Value | Source, as of |
|---|---|---|
| CA Global Natural Resources composite, annualised (linked quarterly pooled IRR) | 11.2% since 1990 (US equity 10.1%, PE 15.0%); **3.2% Q3-2013 to Q2-2023** (PE 15.2%, US equity 12.3%) | Meketa (Mar 2024), CA data to Jun 2023 |
| Volatility (smoothed); correlations | 11.4% (PE 10.3%, US equity 16.7%); ρ with US equity 0.34, with PE 0.48, with bonds 0.0 | Same |
| Oil co-movement | Private energy returns moved with oil in 27 of 35 calendar years (CA Upstream Energy & Royalties vs WTI) | Same |
| Manager dispersion | Interquartile spread 12.9% (2010–19 vintages) | Same |
| Long-run private energy | 1986–2010 vintages: mean net IRR 12.7%, TVPI 1.8×, ≈500bp over PME. A 1pp three-year oil move ↔ ≈0.65pp private energy return | CA (Sep 2017) |
| Post-2004 energy funds | 184 funds of 2004–14 vintages trailed broader PE by **0.56× net MOIC**; 2013–14 vintages by 0.40×. Correlations with public markets and commodities **> 0.7 since 2013**. Record $55.2bn raised in 2014 | CA (May 2020) |
| Vintage medians | CA median TVPI ≈1.09× for 2012-vintage NR funds vs ≈1.40× for 2015 (bought near the trough) | NSHE board book, CA benchmarks at 30 Sep 2024 (our reading of the table columns) |
| Legacy energy at a US public pension (ARMB) | 1y 1.6%, 3y −5.2%, 5y −1.4%, 10y 0.7%, 15y −1.9% net; −6 to −12pp a year vs CPI + 4%; being wound down | ARMB Board packet, 30 Jun 2026 |
| 2015 drawdown | CA private energy benchmark −20.5% in 2015 | Cited by sibling stream G15; **not re-verified by G12** [U] |
| Terms | Management fee 1.5–2.0%; hurdle 6–8%; carry 15–20%; 10–15-year life; 3–5-year investment period; 5–15 assets | Meketa (Mar 2024) |
| Secondary pricing | H1 2026: "commodity price volatility in the energy markets significantly increased the pricing and demand of upstream and natural resources funds". All-strategy LP average ≈87% of NAV; real estate 68%; infrastructure 91% | Jefferies (Jul 2026) |
| Stress secondary pricing | Energy fund LP interests reported at ≈41% of NAV in a March 2020 buyer survey (Setter Capital), and below 70% of NAV in an earlier Greenhill quarter | Search summaries [U] |

**Reading** [I].
- Private energy is a high-oil-beta, high-dispersion asset class.
- Its realised edge over public energy depended on vintage timing, and the post-2013 decade was poor.
- Because ADIC's own data are net IRR/MOIC by holding with cases (design brief §9), the fusion engine can test whether ADIC's ENR managers beat these benchmarks once the oil factor is removed (§6.8).

### 4.2 Listed proxies: oil loadings by era and by shock type [I-calc]

**Data and method.**
- Monthly value-weighted Ken French 49-industry returns (to Aug 2026) and EIA Brent month-end log returns (to 14 Oct 2026, $126.55).
- The table reports the partial oil beta from $r_i-r_f=a+\beta_m(r_m-r_f)+\beta_o\Delta\ln P+e$, with Newey–West (3) standard errors. Correlations are univariate.

| Industry (proxy) | ρ(oil) 1988–2007 / 2008–19 / 2020–26 | Partial oil β 1988–2007 / 2008–19 / 2020–26 (full sample, s.e.) | Annual vol 2020–26 |
|---|---|---|---|
| Oil (petroleum and gas) | 0.29 / 0.59 / 0.69 | 0.16 / 0.20 / 0.30 (0.23, 0.025) | 35% |
| Coal | 0.10 / 0.52 / 0.48 | 0.15 / 0.52 / 0.28 (0.27, 0.046) | 49% |
| Mines (industrial metals) | 0.06 / 0.50 / 0.23 | 0.08 / 0.23 / 0.00 (0.10, 0.029) | 31% |
| Gold | 0.19 / 0.23 / −0.03 | 0.20 / 0.23 / −0.07 (0.09, 0.047) | 38% |
| Utilities | −0.07 / 0.27 / 0.26 | −0.01 / 0.01 / 0.02 (0.02, 0.016) | 17% |
| Paper (forest products) | −0.20 / 0.32 / 0.15 | −0.05 / −0.04 / −0.02 (−0.03, 0.013) | 20% |
| Agriculture | −0.11 / 0.36 / 0.28 | −0.02 / 0.09 / 0.04 (0.03, 0.023) | 23% |

- **Betas to spot understate betas to the valuation-relevant curve.** Spot is more volatile than 12-month futures. Norges Bank's equivalent regressions on 12-month WTI futures give 0.40 for the global oil and gas sector [S].
- **The oil–equity correlation regime matters here too.** Energy equities' correlation with oil roughly doubled after 2008, matching the oil–equity correlation shift in main L3 [C].

**Episodes** (cumulative total returns) [I-calc]:

| Episode (state) | Brent | US market | Oil | Coal | Mines | Paper | Utilities |
|---|---|---|---|---|---|---|---|
| Jun 2014 → Jan 2016 (SG) | −70% | −0.6% | **−38.5%** | −88% | −45% | −0.2% | −6.5% |
| Jun 2008 → Feb 2009 (DB) | −68% | −41% | −47.5% | −79% | −65% | −43% | −38% |
| Dec 2019 → Mar 2020 (DB) | −78% | −20% | −51% | −59% | −35% | −22% | −18% |
| 2022 (SS) | +7% (Dec–Dec) | −20% | +65% | +100% | −10% | −21% | +3% |
| Feb → Aug 2026 (GW) | +26% | +12% | +18% | +18% | −2.5% | −5% | −7% |

**Shock-type windows.** On overlapping 12-month windows since 1988, using stream 03's sign rules, the oil industry's mean return *relative to the market* is:

| State (number of windows) | Relative return | Absolute return |
|---|---|---|
| SG (62) | **−19.5%** | −6.4% |
| DB (19) | +6.7% | −21.8% |
| SS (23) | +36.7% | |
| B (82) | +8.6% | |

Coal returns −37% relative in SG, and mining −12.6% [I-calc].

**Maximum drawdowns since 1988:** Oil −65% (Mar 2020), Coal **−98.7%** (Mar 2020), Mines −66%, Gold −78%, Utilities −38%, Brent −89% [I-calc]. The coal path is a realised stranded-asset history, with sector bankruptcies in 2015–16 [P].

### 4.3 Primary sovereign evidence on sector oil betas (Norges Bank) [S]

**Letter of 14 Nov 2017.**
- The present value of future Norwegian government oil and gas revenue is ≈NOK 4,000bn, and the fund is about twice that.
- A permanent fall of NOK 100/bbl "would more than halve" that PV.
- Oil and gas stocks were ≈4% of the fund. With the Statoil stake, the state's equity oil exposure was ≈2× an index weight.

**Regressions (relative returns on 12-month WTI futures).**
- 1994–2017: the global oil and gas sector's relative oil beta was 0.40 (R² 0.45 with style factors); in total returns, β_oil 0.41 and β_eq 0.71.
- 2006–17, by FTSE subsector:

  | Subsector | Relative oil β |
  |---|---|
  | Oil equipment and services | 0.61 |
  | E&P | 0.54 |
  | Integrated | 0.36 |
  | Pipelines | 0.27 |
  | Renewable equipment | 0.06 (insignificant) |

- **Other sectors** were near zero (basic materials 0.14). **Energy corporate bonds** had excess-return β_oil 0.04 (0.08 since 2008).

**Cost of exclusion.** Over 1973–2017, excluding oil and gas raised equity index volatility only from 14.86% to 15.02%, and a 70/30 portfolio's from 10.86% to 10.99%.

**Fiscal link.** The government's net petroleum cash flow had β = 1.24 to oil over 1973–2016, and 1.92 (ρ = 0.79) over 1996–2016.

**Decision path.** The 2017 advice was to remove the whole sector. On 8 Mar 2019 the government narrowed it to E&P (FTSE "0533 Exploration and Production") to reduce the vulnerability of common wealth to a permanent oil price decline, stressing that it took no view on prices. The Storting endorsed it on 12 June 2019. The proposal was reported at 134 companies, ≈NOK 70bn (≈US$7.9bn, ≈1.2% of equities), and later ≈95 companies. Unlisted renewables were allowed within environment-related mandates [S, press summaries].

**Lesson** [I]. A peer with the same economics excluded the **highest-oil-beta** subsector, kept integrated and pipeline exposure, and accepted a negligible diversification cost. ADIC's ENR book is smaller but private, and its oil betas are *higher* (levered, unhedged).

### 4.4 Reserve-based lending and borrowing-base procyclicality [S]

**OCC Comptroller's Handbook, Oil and Gas E&P Lending (Oct 2018).**
- **Mechanics.** Redeterminations "typically occur semiannually" (plus 1–2 extra). Price decks are set "at a discount to the current NYMEX futures curve".
- **Sizing.** Risk factors are 100% / 90–95% / 65–75% / 25–50% for seasoned PDP / unseasoned PDP / PDNP / PUD. Advance rates are **50–65%** of risk-adjusted NPV. Non-producing reserves are capped at 25–35% of the base.
- **Over-advances** are cured within 30 days in cash or collateral, else repaid over six months.
- **Covenants:** debt/EBITDAX ≈3.5× (≤4.0×); interest cover 2.5–3.0×.
- **Hedging:** hedges "tend to be short term with three-year maturities or less". RBL hedge counterparties are often secured pari passu, and margined hedging may be prohibited.

**2016 stress (Haynes Boone survey, Jan 2016).** Respondents expected spring-2016 borrowing bases to fall **38%** on average, with 79% expecting a decrease. The fall-2016 survey expected a further −20%.

### 4.5 Royalty, stream and cash-out structures [S]

**Streams** monetise a by-product stream without selling the asset.
- Wheaton–BHP (Feb 2026, silver): $4.3bn upfront plus 20% of spot.
- Wheaton–Sibanye (2018): $500m plus 18% of spot, then 22%.
- Triple Flag–CMOC (2020): $550m plus 10% of spot.
- Franco-Nevada (Antapaccay): 20%, then 30%.

**Accounting.** The upfront deposit is deferred revenue with accretion, so the time value of the deposit is "a significant component" (Royal Gold disclosure) [S, summary].

**For ADIC as owner** [I]. The cash-out price embeds the buyer's cost of capital and the curve at signing, so it is procyclical. The structure is a REFINANCE lever to pull in normal or boom states.

### 4.6 Energy transition, carbon and stranding [S]

- **IEA WEO 2025 (12 Nov 2025).**
  - Stated Policies: oil demand peaks at ≈102 mb/d around 2030, then declines gently.
  - Current Policies (revived in 2025): ≈113 mb/d in 2050 (+13% on 2024).
  - The gap between the two is the policy risk the long-run factor must carry.
- **NGFS Phase V (Nov 2024).** "A carbon price of around $300/tCO2 would be needed by 2035" for net zero by 2050, ≈$50 more than Phase IV. Global GDP losses by 2050 are 7–15% across scenarios.
- **EU ETS.** ≈€85/t on 15 Oct 2026, after a high of €88 on 12 Oct [S, IndexBox summary].
- **Stranding estimates.**
  - McGlade & Ekins (2015): for 2°C, about a third of oil reserves, half of gas and over 80% of coal stay unburnt.
  - Welsby et al. (2021): for a 50% chance of 1.5°C, 58% of oil, 59% of gas and 89% of coal reserves (2018 basis) are unextractable by 2050.
  - Semieniuk et al. (2022): stranded upstream losses fall mainly on investors in advanced economies (magnitude not re-read in-session [U]).
- **Owner context** [C: 03]. The UAE's hydrocarbon revenue share falls from 11.3% of GDP (2026) to 9.1% (2030). It left OPEC on 1 May 2026, plausibly to monetise volume before demand declines. This is the same ET drift, from the owner's side.

### 4.7 Agriculture and timber: excluded by the user, kept as comparators [S]

| Index (NCREIF, gross property level unless noted) | 1y | 3y | 5y | 10y | 15y | 20y | As of |
|---|---|---|---|---|---|---|---|
| Timberland | 4.4% | 6.5% | 8.5% | 5.5% | 5.9% | — | 30 Jun 2026 (ARMB packet) |
| Farmland (80/20 row/permanent) | 3.2% | 4.0% | 7.1% | 6.3% | 8.1% | 9.1% | 30 Jun 2026 (ARMB packet) |

- **Farmland 2025:** total 0.20% (income 3.05%, capital −2.80%); permanent cropland −5.43% [S: AgIS, NCREIF]. **Timberland 1995–2025:** EBITDDA 3.4% plus appreciation 3.4% a year [S: Forisk].
- **Inflation and oil.** Private timberland hedged actual, expected and unexpected inflation over 1987–2009 [S: Wan et al. 2013; Washburn & Binkley 1993]. Oil betas are ≈0: paper and forest products −0.03, agriculture 0.03 [I-calc].
- **Peer practice.** ARMB cut timber from 10% to 7% and farmland from 25% to 18% of real assets, citing liquidity and lower expected returns. Its timber manager monetises land through solar leases and data-centre sites [S].
- **Status:** not modelled for ADIC; taxonomy entries only, re-enabled by configuration.

### 4.8 ADIC-specific simulation results [I-MC, SYNTHETIC]

**Setup.**
- Stream 03's annual model: the Z chain, log-OU Brent with κ = 0.40 and P_LR = $70, and the clipped, smoothed draw with c 7.5%, b 0.625, ρ 0.5.
- The hydrocarbon share falls from 11.3% to 9.1%.
- 40,000 paths × 12 years, from the stationary Z distribution, with the first two years dropped.
- Segment cash-flow models (`g12_wrongway_sim.py`) are stylised: PDP with 12% decline, ν 0.80, τ 7%, $20/bbl cash costs and 10% discount.

| Segment | Return vol | ρ(r, Δln P) | Owner β (Δr per +1pp draw) | Cash vs N: SG / DB / GW | Hurdle Δμ, γ = 2–4, P^BE $55 | Draw-weight haircut, κ_d 0.25–1.0 |
|---|---|---|---|---|---|---|
| Upstream PDP, unlevered | 22.5% | 0.88 | −6.8 | 0.43 / 0.49 / 1.26 | 1.2–2.4% | 0.6–1.8% |
| Upstream, 40% LTV RBL | 44.9% | 0.87 | −13.6 | −0.29 / −0.28 / 1.27 | 2.4–4.8% | 1.1–3.6% |
| Upstream, 70% 3-year swap ladder | 8.9% | 0.86 | −2.7 | 0.81 / 0.84 / 1.08 | 0.5–0.9% | 0.2–0.7% |
| Oil mineral and royalty | 17.7% | 0.87 | −5.4 | 0.63 / 0.69 / 1.17 | 0.9–1.9% | 0.5–1.5% |
| Fee-based midstream (MVC 60%) | 5.8% | 0.87 | −1.9 | 0.95 / 0.98 / 1.01 | 0.3–0.6% | 0.2–0.5% |
| Timberland (reference) | 3.2% | 0.00 | 0.0 | 1.00 / 1.00 / 0.99 | 0 | 0 |
| Farmland (reference) | 8.0% | 0.09 | −0.3 | 1.00 / 1.00 / 1.00 | ≈0.05% | ≈0.05% |
| Global equity (reference) | 19.2% | 0.21 | −1.9 | — | 0.24–0.48% | 0.2–0.5% |

- **Draws.** The mean draw is 6.2% / 6.9% / 7.5% of NAV at P^BE $44.8 / $55 / $65, consistent with stream 03's 6.0% / 6.7% / 7.3%. By state: SG 8.1%, DB 7.8%, GW 7.9%, N 6.7% (P^BE $55).
- **Cure calls** on 40%-LTV upstream (advance 60% of a deck at 85% of the curve): probability 73% / 69% / 19% / 9% in SG / DB / GW / N. The mean size when called is 18% / 20% / 16% / 8% of equity; N reflects depletion drift.
- **Collateral, if the 70% hedge sits in the overlay** (% of hedged value a year): mean inflows of +4.5% (SG) and +7.5% (DB); mean outflow of −6.1% in B; GW averages +0.3% but has a P05 of −14.7%; SS P05 −14.6%.

- **Hedging.** The 3-year 70% ladder removes 62% of the PDP's spot elasticity (0.39 → 0.15). The rest sits in years 4+, beyond typical hedge tenors.
- **Oil dependence.** L_eff (% of NAV) across owner parameters:

  | Parameter | Values | L_eff |
  |---|---|---|
  | h (P^BE $55) | 6 / 9.1 / 11.3 / 15% | 7.1 / 8.5 / 8.9 / 9.3 |
  | P^BE | $35 / $40 / $44.8 / $55 / $65 | 4.8 / 6.2 / 7.5 / 9.3 / 9.9 |
  | b | 0.625 → 1.25 | 9.3 → 10.0 |

  When b doubles, P(d* in band) falls from 0.65 to 0.35, which offsets the steeper slope (`g12_low_breakeven_check.py`, `g12_slope_check.py`).
- **Owner-state weight.** Stream 03's weight $m^{own}=1+\kappa(FB^*-FB)^+/\sigma_{FB}$ gives haircuts of 6.1% for PDP and 12.2% for levered upstream at κ = 1. It is invariant to h because of the $\sigma_{FB}$ normalisation (§6.4).
- **Synthetic ENR sleeve** ($2.5bn, G15's split; our sub-segment mix: $1.07bn levered upstream, $0.18bn royalties, $0.85bn midstream, $0.40bn other):

  | Measure | Value |
  |---|---|
  | Oil delta | **12.2m bbl-equivalent**: 6.1% of the in-band draw delta; 31–61% of the overlay's 20–40m bbl put-spread programme |
  | SG one-year loss vs N | −$0.68bn (−$0.96bn on the 2014–16 listed analogue) |
  | Put-spread payoff at $45 | $0.38bn (20m bbl) to $0.76bn (40m bbl) |
  | Neutralising the delta with 1-year 64/31 put spreads | $3–13/bbl, i.e. 1.5–6.4% a year of sleeve NAV (forward $70–84, vol 35–70%) |

---

## 5. Practitioner and peer practice, case studies

1. **Norway (GPFG; §4.3).** The advice rested "exclusively on financial arguments". The executed version shed the highest-oil-beta subsector (E&P) and kept integrateds and pure renewables. **Lesson** [I]: classify ENR holdings by oil beta, not by label.
2. **IMF guidance (§2.1)** [S]. Hold assets negatively correlated with the commodity, and manage on the integrated sovereign balance sheet, including the drawdown case in which a fund covers a commodity-driven financing gap (WP/18/26).
3. **Endowments and pensions** [S].
   - In 2017 CA put private energy at 2.8% of the average US endowment and foundation portfolio, and over 25% of real assets.
   - Since then:
     - ARMB is winding down legacy energy and cutting timber and farmland;
     - a university system's legacy NR funds of 2012–15 vintages are at 1.48–1.50× TVPI (NSHE);
     - Harvard marked its natural resources down by ≈$1.1bn to ≈$2.9bn in FY2017, including a failed Brazil farm and forest project [S, press].
   - **Lesson** [I]: illiquid, smoothed natural-resource marks hid large economic losses that were revealed late (cf. G13 on de-smoothing).
4. **Producers and lenders** [S].
   - Hedging lowers oil-price sensitivity of US producers' stock prices but shows no firm-value premium (Jin & Jorion 2006). Hedging is risk transfer, not alpha. For ADIC its value is the owner hurdle it removes (§6.4).
   - RBL practice (§4.4) makes borrowing capacity oil-procyclical.
5. **Mexico's sovereign oil hedge** [C: 03 §4.8].
   - Puts on about 29% of production cost ≈0.1% of GDP a year and paid 0.3–0.6% of GDP in 2009, 2015 and 2016.
   - A minority hedge struck near the budget price is politically sustainable. It is the template for the overlay's kink put spreads, which ENR exposure partly offsets (§4.8).
6. **Gulf owners** [C/I].
   - ADIC sits under Mubadala, and Abu Dhabi's wealth is dominated by hydrocarbons in the ground [C: 03 §5].
   - Any ENR asset whose value depends on Gulf export volumes carries GW-state volume risk in addition to price risk. That doubles its owner correlation. Whether ADIC holds such assets is an open question (§9).

## 6. Design implications for the ADIC framework

### 6.1 Placement and taxonomy (configuration, not code)

- **Sector `RA.ENR`**, with sub-sleeves tagged by oil-beta class:
  - high: `UP_OP`, `UP_NONOP`, `MIN_ROY` (oil and gas minerals, ORRI), `OFS`;
  - medium: `MID_COM`;
  - low: `MID_FEE` (MVC or take-or-pay), `MET_BASE` and `MET_PREC` (including streams);
  - gas factor: `PWR_MER`;
  - ≈0: `TRANS`.

  `RA.AG` and `RA.TIM` exist but are **disabled** (user, 18 Oct 2026).
- **Vehicles:** closed-end funds run on the fund-interest engine, with oil-elastic parameters (§6.3 E6). Direct, co-investment and JV assets run on the asset engine (E2–E5).
- **Ownership of decisions.**
  - The Real Assets head owns ENR asset proposals.
  - The **Overlay** executes residual oil hedges.
  - **Corporate Finance** owns the ENR cure reserve and books overlay collateral.
  - The **Sovereign Liability agent** publishes L_eff and the owner hurdles.

### 6.2 State and decision variables

**Global state** (added to the generator): the oil state $(x_t,Z_t)$ with the curve $F_t(k)$ from (E1); an optional gas factor $g_t$ with Z-dependent correlation to oil; a base-metals factor $m_t$; the carbon price $c_t$ (NGFS paths under the ET overlay); the ET drift on the long-run oil level (stream 03: −2% a year real from 2030, high-transition variant); and L_eff from the owner module.

**Per asset:** reserves $(R^{PDP},R^{PDNP},R^{PUD})$ and decline parameters $(q_i,D_i,b)$; ν, τ and cash costs c; contract terms (fee, MVC, escalator); hedge ladder $\{H_{t,k},\bar q_{t,k}\}$; RBL state $(D_t,BB_t,\theta^{deck},a)$; stream or royalty obligations; `oil_delta_bbl`, `owner_beta`, `gulf_volume_flag`.

**Per fund:** commitment K, unfunded U, reported and economic NAV, effective age, sub-sleeve weights, the GP price deck (for re-striking forecasts) and the disclosed hedge ratio.

**Decisions:** SELL fraction; HOLD (fund calls); REFINANCE (RBL draw, stream or royalty sale, volumetric production payment, NAV facility, JV sell-down); LEVER (acquisition or development debt); **HEDGE** (asset-level ladder, or overlay residual); new commitments within the oil-delta budget.

### 6.3 Return, NAV and cash-flow equations

- **(E1) State-conditional curve:** $\ln F_t(k)=\bar x+\phi^k(x_t-\bar x)+\sum_{i\le k}\phi^{k-i}(P_Z^i\mu)_{z_t}$.
  - In production, replace it with the ICE Brent strip on the as-of date, plus a P-measure premium so that simulated P paths and Q curves stay consistent.
- **(E2) Direct upstream.**
  - Value: $V_t=\sum_kq_{t,k}[F_t(k)\nu(1-\tau)-c]^+D_k+\mathcal O^{PUD}_t+\mathrm{MTM}^{hedge}_t$.
  - Cash: $C_t=q_t[P_t\nu(1-\tau)-c]^++\sum h_t(H_t-P_t)\bar q_t-iD_t-\text{capex}_t$.
  - Arps decline for $q$.
- **(E3) RBL.**
  - Borrowing base: $BB_t=a\cdot\mathrm{NPV}(\theta^{deck}F_t;\ \text{risk factors }1/0.9/0.7/0.4)$, with a ≈ 0.60 and θ ≈ 0.85.
  - Over-advance: $O_t=(D_t-BB_t)^+$. It is cured from cash within 30 days or amortised over six months. **The residual is an equity cure call on ADIC.**
  - Redetermine every six months, and on any jump of ≥ 20% in the curve.
- **(E4) Royalties and streams.**
  - A royalty holder receives $s\,q_tP_t(1-\tau)$, where q responds to drilling: $\Delta\ln q=-\delta_r+a_r\ln(F^{(3)}_t/\bar F)$.
  - **Selling a stream (REFINANCE):** upfront $U_0=\mathrm{PV}_{\rho_B}[(1-\kappa_s)q^{bp}P]$. Its cost to ADIC is $\mathrm{PV}_{\rho_{ADIC}}-U_0$, plus lost upside.
- **(E5) Midstream:** $C_t=f_t\max(v_t,\text{MVC}_t)$, with $\Delta\ln v=a_m\ln(F^{(3)}_t/\bar F)$.
- **(E6) Closed-end ENR funds** (RFT-TA v2 [C]).
  - Distribution intensity: $\delta_t=\bar\delta(a^e)\exp(\kappa_DX_t+\eta_{oil}\ln(F^{(3)}_t/\bar F))$, with income yield $y_t=y_0(F^{(3)}_t/\bar F)^{\eta_{oil}}$.
  - Economic NAV return: $r_t=r_f+\beta_{eq}\mathrm{ERP}+\beta_{oil}\Delta\ln F^{(3)}_t+\tilde\alpha+\sigma\varepsilon$.
  - Reported NAV: smoothed with $\lambda_q\approx0.6$, plus a two-quarter price lag for PV-10-anchored marks.
- **(E7) Owner hurdle and haircut.**
  - Hurdle: $\Delta\mu_j=\gamma L_{eff}\mathrm{Cov}(r_j,\Delta\ln P)$.
  - Draw-weighted haircut: $H^d_j=-\mathrm{Cov}(m^d_t,r_j)/\mathbb E\,m^d_t$ (§6.4).
  - Once H's duals exist, the λ-weighted $H^\lambda_j=-\mathrm{Cov}(\lambda_t,r_j)/\mathbb E\lambda_t$ supersedes both.
- **(E8) Oil delta:** $\delta^{bbl}_j=\varepsilon_j\,\mathrm{NAV}_j/P_t$, with $\varepsilon_j$ by bump-and-revalue under (E1). The Real Assets total is $\Delta_{RA}=\sum_j\delta^{bbl}_j-\text{hedges}$.

### 6.4 Which owner weight? (a design correction to stream 03 §6.9)

Stream 03's weight $m^{own}=1+\kappa(FB^*-FB)^+/\sigma_{FB}$ has two problems [I-MC]:
- **(a) It is scale-free in h.** The $\sigma_{FB}$ normalisation makes it invariant to the owner's oil dependence.
- **(b) It is very steep.** At κ = 1 it gives a 6.1% haircut on PDP and 2.1% on global equities, 3–5× the Gintschel–Scherer hurdle at γ = 2–4.

**Recommendation** [I].
- **Interim.** Use the draw-utilisation weight $m^d=1+\kappa_d(d_t-5\%)/5\%$, with $\kappa_d$ set to the marginal cost of funding the last dollar of draw: ≈0.25 from the liquid book (4–40bp), up to ≈1.0 if it forces private sales at 9–45% discounts [C: groups §2.3].
- **Target.** Use λ-weights from H's restored-problem duals, so the hurdle is FTP-consistent (groups §4.3).
- **Reporting.** Show the Gintschel–Scherer hurdle as the IC-readable number.

### 6.5 Constraints

| # | Constraint | Default [I] | Rationale |
|---|---|---|---|
| C1 | Real Assets oil-delta budget $\Delta_{RA}(x_t,Z_t)\le B_{oil}\cdot L^{ref}_{eff}/L_{eff,t}$ | $B_{oil}$ = 5m bbl soft, 10m hard; $L^{ref}_{eff}$ = 9.3% of NAV | Keeps the asset side from offsetting the overlay's 20–40m bbl put spreads. The scaling relaxes the budget if the owner's oil dependence falls (mandate Mode A, lower P^BE) |
| C2 | Levered upstream only if hedged | ≥70% of 3-year production hedged at asset level; RBL LTV ≤ 40% of deck PV; debt/EBITDAX ≤ 3.0× | Cure calls hit in ≈70% of SG/DB years at 40% LTV unhedged |
| C3 | ENR cure reserve in Tier-1 SG and DB rows | $0.73\times0.18\times E^{lev}_{ENR}$ ≈ 13% of levered ENR equity (≈$0.14bn on the synthetic book) | Owned by Corporate Finance; funded like stressed calls |
| C4 | Stressed coverage-ratio rows (stream 03 DCR) | ENR cash at SG/DB multipliers (§6.9); ENR fund calls *not* reduced in SG | GPs buy distressed assets with called capital [I] |
| C5 | Transition exposure | Share of ENR NAV whose value is > 50% beyond 2035 ≤ 30%; carbon cost at NGFS "Delayed Transition" passes through in the ET overlay | Stranding risk is a drift, not a jump |
| C6 | Owner-correlated concentration (stream 03 constraint 6) | Gulf-volume-dependent ENR counts at 2× | GW volume risk adds to price risk |

### 6.6 Objective terms

$$J\;{+}{=}\;-\sum_{j\in ENR}x_j\big(H_j+\tau_j\big)\;-\;c^{hedge}\big(\Delta_{RA}-B_{oil}\big)^+$$

Here $H_j$ is the owner hurdle (§6.4). $\tau_j$ is the transition charge [I]: 0.5% a year for oil reserves with lives above 10 years, 0.25% for gas, 0 for midstream contracted to 2035. $c^{hedge}$ is the overlay's put-spread carry, $3–13/bbl [I-calc]. The terms sit beside the main report's α* and robust floors.

### 6.7 SELL / HOLD / REFINANCE / LEVER (and HEDGE) for ENR

| Action | ENR instrument | Economics and rule [I unless tagged] | State timing |
|---|---|---|---|
| **SELL** | Asset or stake sale off the strip; LP secondary; JV sell-down | Bids fall to ≈40–70% of NAV in busts [U] and rise in GW (H1 2026 [S]). A fair-value sale has ≈0 NPV but **removes $H_j$ and the cure tail**. SELL iff $p^{ceq}>p^*$ (groups §3.0), with HOLD charged $H_j+\tau_j$ | Prefer GW and B (now) |
| **HOLD** | Keep; fund calls | Charged $H_j$, FTP and $\tau_j$; GP forecasts re-struck to the strip (§6.8) | Default in DB (worst bids) |
| **HEDGE** | Asset-level swaps or collars (pari passu, unmargined [S: OCC]); overlay residual | A 70% 3-year ladder removes ≈62% of elasticity and ≈60% of $H_j$. Overlay route: collateral +4.5% / +7.5% in SG / DB, P05 −15% in GW/SS [I-MC] | GW/B, while backwardated strips are high |
| **REFINANCE** (cash-out) | RBL draw; stream, royalty or VPP sale ($4.3bn + 20% of spot [S]); NAV facility (Capital Solutions prices); JV sell-down | Capacity ∝ deck × advance rate, so it shrinks ≈38% in a glut [S]. Pass iff $s_B+f/T+\lambda_{Lev}+\text{covenant charge}<\bar\ell_{[0,T]}$ (groups §3.0). **Arrange in N/B/GW; never count on it in SG/DB** | N/B/GW only |
| **LEVER** (exposure-up) | Acquisition RBL, development capex, drilling JVs | Adds oil delta against C1. Allowed only with C2 hedges and a cleared owner hurdle | Rarely; never in SG/DB |

**Intra-ADIC rule** (groups §4.1). An ENR stake sold to Secondaries, or financed by Capital Solutions, raises zero liquidity.

### 6.8 How forecasts are produced, and their biases

Holdings data are net IRR/MOIC since inception, with downside/base/upside cases (design brief §9). Four biases matter [I]:
- **(i) Price deck.** Business plans run on a deck, so forecasts made at high prices extrapolate. Re-strike each forecast to the curve with $\ln M^{f,adj}=\ln M^f-\varepsilon^{M}_j\ln(F^{deck}/F^{strip})$, where $\varepsilon^M_j$ is the E8 elasticity stored per holding.
- **(ii) Underwriting.** Underwritten IRRs embed the vintage deck (2011–14 vintages were underwritten near $90–110 Brent). Treat them as sunk.
- **(iii) Mark lag.** PV-10 and SEC pricing lag the strip by ≈6 months, and NAVs smooth further (λ ≈ 0.6). De-smooth per G13.
- **(iv) Skill vs beta.** Score skill on $\alpha_j=r_j-\beta_{oil,j}\Delta\ln F^{(3)}-\beta_{eq,j}r_{eq}$, never on raw IRR, which rewards vintage timing.

Bias prior for ENR forecasts: +2 to +4pp a year in falling-price regimes, ≈0 in rising ones. Credibility $\kappa_g$ is estimated from the archive [I].

### 6.9 Scenario generator loadings and the Tier-1 oil-crisis state

**ENR loadings for the generator** (economic NAV; $\Delta\ln F^{(3)}$ is the log change of the 1–3-year strip average; β_oil = spot elasticity ÷ 0.39) [I-calc / I-MC / S as tagged]:

| Sub-sleeve | β_oil (to F(3)) | β_eq | Cash multiplier SG / DB / GW / SS | Notes |
|---|---|---|---|---|
| UP (unlevered) | 0.9–1.1 | 0.4 | 0.45 / 0.5 / 1.25 / 1.7 | ≈0.39 to spot [I-MC]; listed E&P 0.54 relative [S: NB] |
| UP (40% LTV) | 1.5–1.8 | 0.6 | −0.3 (net cures) / −0.3 / 1.25 / 2.2 | Cure P 0.73 / 0.69 / 0.19 |
| MIN_ROY | 0.75–0.9 | 0.3 | 0.63 / 0.69 / 1.17 / 1.5 | No cost leverage; volume response |
| MID_FEE | 0.2–0.3 | 0.5 | 0.95 / 0.98 / 1.0 / 1.04 | Pipelines 0.27 relative [S: NB] |
| OFS | 1.2–1.5 | 0.9 | 0.4 / 0.3 / 1.3 / 1.6 | Services 0.61 relative [S: NB] |
| MET_BASE | 0.1–0.3 | 1.1–1.3 | 0.85 / 0.6 / 1.0 / 1.0 | Mines −45% in 2014–16 [I-calc] |
| MET_PREC and streams | ≈0 | 0.4 | 1.0 / 1.0 / 1.0 / 1.0 | Gold +31% relative in DB windows [I-calc] |
| TRANS | ≈0 | 0.6–0.8 | 1.0 | Renewables 0.06 relative [S: NB] |

**OC: Tier-1 oil-crisis state**, a named row beside T4′ [I]:

| Component | OC specification |
|---|---|
| Brent | −45% from the curve over six months, then $40–50 for 18 more months (2014–16 spent 22 months below 70% of its 36-month mean [C: 03]) |
| Markets and owner | Equities −5% to +5%; exits as today (drought); draw at the 10% cap for two fiscal years, opening-NAV basis [C] |
| ENR marks | Unlevered upstream −35%; levered equity −65%; royalties −30%; midstream −10%; services −50%; base metals −40% (anchors: listed 2014–16 oil −38.5%, mines −45% [I-calc]) |
| ENR cash and financing | Multipliers above; borrowing bases −38%, then −20% [S]; fund calls unchanged; secondary bids 40–60% of NAV [U/I] |
| Overlay | Oil hedges pay; collateral flows in |

**Variants.** *OC×DB* is T4′ plus oil −70% and listed upstream −51% (2020). *GW+* is oil +50% with a −6pp UAE volume wedge: draws rise, overlay oil swaps post P05 VM of ≈15% of hedged value, and out-of-Gulf upstream gains ≈18% (the 2026 war analogue [I-calc]).

### 6.10 Recommendation: how much oil-linked real-asset exposure to hold

**Rule** [I]. Hold oil-linked ENR $j$ only if all three conditions hold:
$$\hat\alpha^{net}_j\ \ge\ H_j(P^{BE},b,h,\kappa)+\mathrm{FTP}_j+\tau_j,\qquad\sum_j\delta^{bbl}_j\le B_{oil}\frac{L^{ref}_{eff}}{L_{eff,t}},\qquad\text{C2 met.}$$

**Defaults today** (Z0 ≈ GW; P^BE prior median $55; mandate Mode B):
- **Budget.** $B_{oil}$ = 5m (soft) / 10m (hard) bbl. That is ≈$0.9–1.8bn of unlevered upstream, $0.5–1.1bn levered, $2.4–4.8bn hedged PDP, $1.2–2.3bn royalties, or $3.6–7.1bn of fee midstream.
- **The synthetic ENR sleeve** ($2.5bn, ≈12m bbl) is **over the hard limit**. Hedge 70% of 3-year production at asset level, which brings it to ≈6m bbl, between the soft and hard limits. Or SELL ≈$0.6–0.8bn of levered upstream into the GW bid, which brings it to ≈5–7m bbl.
- **No new unhedged upstream, OFS or oil-royalty commitments.** New ENR commitments tilt to fee midstream with MVCs, precious-metal streams and royalties, and transition assets. All count against C1 and against G11's limits.
- **Re-size automatically** through C1's $L^{ref}_{eff}/L_{eff,t}$ scaling whenever the owner module re-estimates P^BE, b or the mandate mode.
  - Because the band saturates L_eff (7–10% of NAV across h, b and P^BE of $45–65), the budget is stable in most cases.
  - It roughly doubles only if the effective breakeven is ≈$35 (L_eff 4.8%).
  - It can rise severalfold if the mandate moves to Mode A, where ADIC sets the draw.

**Order of magnitude.** The cap is ≈0.3–0.6% of NAV in unhedged-equivalent oil exposure. That is the same order as NBIM's E&P exclusion (≈1.2% of equities) [S], scaled for ADIC's private, levered holdings.

### 6.11 Calibration targets (the simulator must reproduce)

| # | Target | Value | Source |
|---|---|---|---|
| 1 | Private NR return regimes | 11.2% a year (1990–2023); 3.2% (2013–23); vol 11.4% smoothed; ρ with equity 0.34 | [S] Meketa / CA |
| 2 | Energy funds vs PE | −0.56× net MOIC (2004–14 vintages); ρ with commodities > 0.7 | [S] CA 2020 |
| 3 | Private energy oil sensitivity | ≈0.65 per pp over 3 years | [S] CA 2017 |
| 4 | Sector oil betas (relative, to 12-month futures) | E&P 0.54; integrated 0.36; services 0.61; pipelines 0.27; renewables ≈0 | [S] Norges Bank 2018 |
| 5 | Listed oil industry in SG | −38.5% with the market flat (2014–16); −19.5% relative in SG windows | [I-calc] |
| 6 | Borrowing-base cut in a glut | −38% (spring 2016), then −20% | [S] Haynes Boone |
| 7 | RBL structure | advance 50–65%; deck below strip; semiannual redeterminations; hedges ≤ 3 years | [S] OCC 2018 |
| 8 | Upstream cash vs N | 0.43–0.49× in SG/DB; levered equity net negative | [I-MC] |
| 9 | L_eff | 7.5–9.9% of NAV (P^BE $45–65) | [I-MC] |
| 10 | Transition range | 2050 oil demand ≈113 mb/d (CPS) vs a peak of ≈102 mb/d ≈2030 (STEPS); ≈$300/tCO2 by 2035 (NZ2050) | [S] IEA, NGFS |

### 6.12 Data ADIC must supply

ENR holdings by sub-sleeve, vehicle and geography (flagging Gulf-volume dependence); reserve reports (PV-9/PV-10 by category, decline, costs); the price decks behind every archived forecast; hedge books (volumes, strikes, tenors, margining); RBL documents (borrowing base, advance rates, redetermination dates, covenants, cures); stream, royalty and VPP contracts; ENR fund LPAs; the overlay's permitted oil instruments; and any owner guidance that some oil exposure is held deliberately.

### 6.13 SPECIFICATION CARD: Real Assets, energy and natural resources (`RA.ENR`)

| Field | Specification |
|---|---|
| **Scope** | Upstream (operated and non-operated), minerals and royalties, oilfield services, midstream (fee and commodity), mining and metals (including streams), gas-linked merchant power, transition assets held in ENR. `RA.AG` and `RA.TIM` disabled (user). Vehicles: closed-end funds; co-investments, JVs and direct assets |
| **Data fields** | `group=RA`, `sector=ENR`, `subsleeve`, `vehicle`, `is_synthetic`, `geo`, `gulf_volume_flag`, IRR/MOIC u/a/f with cases (bitemporal), `gp_price_deck`, reserves {PDP, PDNP, PUD}, decline (q_i, D_i, b), ν, τ, costs, contracts {fee, MVC, take-or-pay end}, `hedge_ladder` {tenor, volume, strike, type, margined?}, RBL {D, BB, advance, deck factor, covenants, next redetermination}, stream/royalty terms, `oil_delta_bbl`, `owner_beta`, `H_j`, `tau_j`, encumbrance, consent/ROFR |
| **Return and NAV** | Direct assets: E1 curve → E2/E4/E5 DCF + MTM of hedges; a PUD option by LSMC. Funds: E6 factor NAV with β_oil to F(3) by sub-sleeve (§6.9), reported NAV smoothed (λ ≈ 0.6) plus a two-quarter price lag |
| **Cash flows** | Direct assets: production × netback ± hedge settlement − interest − capex; RBL over-advance → cure from cash, else **equity cure call** (E3). Funds: RFT-TA calls; distributions oil-elastic ($\eta_{oil}$ ≈ 1.2) plus income yield ≈4% normal [C: G15] |
| **Parameter defaults** | PDP decline 12%/yr; ν 0.80; τ 7%; cash cost $20/bbl; discount 10% (PV-10 convention [P]); RBL advance 0.60 on a deck at 0.85 × curve, LTV ≤ 0.40, debt/EBITDAX ≤ 3.0×; risk factors 1/0.9/0.7/0.4 [S: OCC ranges]; royalty decline 8% with activity response 0.10; midstream MVC 60%, volume response 0.15; fees 1.5–2.0% / 15–20% carry / 6–8% hurdle; fund life 10–15 years [S: Meketa]. All [I] unless tagged; replace with ADIC data |
| **Liquidity terms and stress** | LP secondary: ≈85–95% of NAV in N/GW (H1 2026 strong [S]); 40–70% in OC/DB [U/I]. Direct sale 3–9 months. RBL capacity −38% in OC [S]. Cure reserve ≈13% of levered equity in SG/DB rows. Overlay route: collateral in during SG/DB, out in GW/SS tails (P05 −15%/yr of hedged value) |
| **Action definitions** | SELL: asset, stake, LP secondary, JV sell-down. HOLD: fund calls. REFINANCE (cash-out): RBL draw, stream/royalty/VPP sale, NAV facility, JV sell-down. LEVER (exposure-up): acquisition or development debt. HEDGE: asset-level ladder first, overlay residual. Rules in §6.7; owner hurdle in every HOLD/LEVER card |
| **Forecasts and biases** | Group forecasts are GP business plans at a price deck → re-strike to the curve (§6.8); underwritten IRR is sunk; marks lag ≈2 quarters; bias prior +2 to +4pp/yr in falling-price regimes; score skill net of β_oil and β_eq |
| **Constraints and objective** | C1 oil-delta budget 5m/10m bbl (scaled by L_eff); C2 hedged leverage; C3 cure reserve; C4 DCR rows; C5 transition; C6 Gulf-volume ×2. Objective −Σ x(H + τ) − c_hedge·(Δ_RA − B)⁺ |
| **Synthetic defaults** | ENR $2.5bn NAV ($1.6bn closed-end, $0.9bn direct/co-invest; unfunded $0.8bn; LTV 0.35/0.40 [C: G15]). G12 split: levered upstream $1.07bn, royalties $0.18bn, fee midstream $0.85bn, other $0.40bn → Δ ≈ 12.2m bbl. 12–20 funds, vintages 2012–2025; 6–10 direct assets. Generate net IRR/MOIC marks with P10/P50/P90 cases; GP decks drawn from the vintage curve ± 10%; label SYNTHETIC |
| **Links** | Overlay: oil residual hedges, kink put spreads (net the ENR delta), VM via the CF collateral pool. Corporate Finance: cure reserve, look-through leverage, FTP/λ (target owner weight). Capital Solutions: NAV facilities and stream pricing quotes (conflict controls). Secondaries: ENR LP pricing intelligence (firewall). Private Credit: energy credit counts in the oil delta. G11: power and transition assets. G13: de-smoothing. G14: action instruments. G15: cash-map row and OC state |

## 7. Implementation notes (Python, algorithms, numerical pitfalls)

1. **Vectorised curves.** Precompute $A_k(z)=\sum_{i\le k}\phi^{k-i}(P_Z^i\mu)_z$ once per parameter set (a K × 6 table). The curve for N paths is then an (N × K) exponential (`fwd_curve`). Store curves on CRN paths so every action card revalues on the same draws.
2. **Median vs mean forwards.** $\exp(\mathbb E\ln P)$ understates $\mathbb EP$ by $e^{\sigma^2/2}$, and the netback floor adds convexity: our stylised PDP's mean return is ≈1.5pp above its 10% discount rate. In production, value at the Q-curve and simulate P with an explicit premium. Never mix the two.
3. **Depletion artefacts.** PDP "returns" include return of capital, so yields run 15–25%. Compare segments on total return and on cash versus the same-date N state (`cash_vs_N`). Yield on current value spuriously correlates *positively* with the draw for midstream.
4. **RBL engine.** Run a semiannual loop with event redeterminations and the cure waterfall: cash, then six-month amortisation, then equity. Hedges inside the RBL settle at production with no VM. Overlay hedges go through the collateral ledger (main §4.6).
5. **Shut-in and PUD options.** Use LSMC on (x, Z, reserves). Netback floors handle shut-ins to first order. WTI went negative in April 2020, so keep log Brent as the factor but allow negative realised netbacks through differentials.
6. **Betas.** Estimate against $F^{(3)}$, not spot, because spot betas are attenuated (§4.2). Use Newey–West errors and era splits, and pool sub-sleeves hierarchically: CA's 2010–19 private ENR set averages only 23 funds per vintage [S: Meketa].
7. **De-smoothing.** Apply G13's estimator *after* removing the SEC-price lag, or the lag is mistaken for smoothing.
8. **Agentic roles.** The Sovereign Liability agent publishes L_eff, H_j and the budget. An ENR desk agent re-strikes forecasts and runs E2–E5. A red-team agent searches for the most plausible path that breaches C1 or C3. LLMs extract terms from reserve reports and RBL agreements; code owns every number.
9. **Tests.**
   - (a) `cash_vs_N` is monotone in oil for UP and MIN_ROY.
   - (b) An unhedged holding with H > 0 never gets a positive LEVER card while C1 binds.
   - (c) Intra-ADIC ENR transfers raise zero liquidity.
   - (d) The synthetic ENR delta reproduces 12.2m bbl ± 5% at the reference state.

---

## 8. Risks and limitations

- **Stylised models** [I-MC]. Elasticities, cure frequencies and hurdles come from simple cash-flow models on stream 03's *prior* Z chain: design defaults, not estimates. Hurdles scale linearly with γ and L_eff, both elicited.
- **The owner model is the weakest link.** P^BE, b, ω and the mandate mode are unobserved [C: 03]. L_eff could be lower if the owner funds gluts with debt (as Kuwait did in 2025), or higher if ADIC is the marginal pocket.
- **GW is right-way for out-of-Gulf upstream.** Over-hedging in a long war forgoes protective value, which is why the budget is state-dependent.
- **Data gaps** [U]: CA returns after mid-2023 (paywalled); the 2015 −20.5% figure; stress secondary pricing (≈41% of NAV, Mar 2020); Semieniuk et al. magnitudes.
- **Private vs listed.** Private ENR funds hedge early and mark to lagged decks, so measured betas understate economic ones.
- **Transition uncertainty** is two-sided (IEA 102–113 mb/d). A slower transition raises values but does not change the owner correlation.
- **Excluded sleeves.** Timber and farmland would be zero-oil-beta diversifiers. The user excluded them, and this dossier does not argue for re-inclusion.

---

## 9. Open questions (ADIC to supply or confirm)

1. **Holdings.** Actual ENR holdings, by sub-sleeve, vehicle, geography and oil-beta class. Is any of it Gulf-volume-dependent, for example domestic or regional midstream?
2. **Owner intent.** Are any ENR holdings strategic or policy-driven, and so outside the optimiser's SELL set?
3. **Hedging permissions.** May ENR assets hedge at asset level? May the overlay hold oil swaps or options, and how large may the oil hedge book be (main §4.6 item 9)?
4. **Leverage documents.** RBL terms on direct assets: advance rates, deck policy, cure obligations and recourse to ADIC (expected: none, but cures are economic).
5. **Forecast archive.** Do the quarterly forecasts carry the GP or ADIC **price deck**? Without it, the re-strike in §6.8 needs a curve-at-date proxy.
6. **Owner weight.** Which weight does the IC endorse? The λ-weight is the target; the draw-utilisation weight $\kappa_d$ is the interim.
7. **Transition policy.** Any ESG or transition constraints (exclusions, carbon intensity) that would supersede C5?
8. **Exclusion scope.** Do the user's exclusions also bar *agricultural* commodities exposure inside ENR funds (for example fertiliser or ag-tech)? Our default is yes, to config.

---

## 10. References

*Academic and official*
- Brennan, M. J. & Schwartz, E. S. (1985). Evaluating natural resource investments. *Journal of Business* 58(2), 135–157. https://ideas.repec.org/a/ucp/jnlbus/v58y1985i2p135-57.html
- Brown, A., Papaioannou, M. & Petrova, I. (2010). *Macrofinancial Linkages of the Strategic Asset Allocation of Commodity-Based Sovereign Wealth Funds.* IMF WP/10/9. https://ideas.repec.org/p/imf/imfwpa/2010-009.html (full text via https://ifswf.org/media-download/15229)
- Alhassan, A., Brake, S., Papaioannou, M. & Skancke, M. (2018). *Commodity-based Sovereign Wealth Funds: Managing Financial Flows in the Context of the Sovereign Balance Sheet.* IMF WP/18/26. https://ideas.repec.org/p/imf/imfwpa/2018-026.html
- IMF (2014). *Sovereign Asset-Liability Management—Guidance for Resource-Rich Economies.* Policy paper. https://www.imf.org/en/publications/policy-papers/issues/2016/12/31/sovereign-asset-liability-management-guidance-for-resource-rich-economies-pp4876
- Gintschel, A. & Scherer, B. (2008). Optimal asset allocation for sovereign wealth funds. *Journal of Asset Management* 9(3), 215–238. https://doi.org/10.1057/jam.2008.19
- van den Bremer, T., van der Ploeg, F. & Wills, S. (2016). The elephant in the ground: managing oil and sovereign wealth. *European Economic Review* 82, 113–131. https://doi.org/10.1016/j.euroecorev.2015.10.005
- van den Bremer, T. & van der Ploeg, F. (2013). Managing and harnessing volatile oil windfalls. *IMF Economic Review* 61, 130–167. https://doi.org/10.1057/imfer.2013.4
- Kilian, L. (2009). Not all oil price shocks are alike. *American Economic Review* 99(3), 1053–1069. https://doi.org/10.1257/aer.99.3.1053
- Schwartz, E. & Smith, J. E. (2000). Short-term variations and long-term dynamics in commodity prices. *Management Science* 46(7), 893–911. https://doi.org/10.1287/mnsc.46.7.893.12034
- Jin, Y. & Jorion, P. (2006). Firm value and hedging: evidence from U.S. oil and gas producers. *Journal of Finance* 61(2), 893–919. https://doi.org/10.1111/j.1540-6261.2006.00858.x
- Insley, M. & Rollins, K. (2005). On solving the multirotational timber harvesting problem with stochastic prices. *American Journal of Agricultural Economics* 87(3), 735–755. https://ideas.repec.org/a/oup/ajagec/v87y2005i3p735-755.html
- Wan, Y., Mei, B., Clutter, M. L. & Siry, J. P. (2013). Assessing the inflation hedging ability of timberland assets in the United States. *Forest Science* 59(1), 93–104. https://doi.org/10.5849/forsci.11-029
- Washburn, C. L. & Binkley, C. S. (1993). Do forest assets hedge inflation? *Land Economics* 69(3), 215–. https://doi.org/10.2307/3146588
- McGlade, C. & Ekins, P. (2015). The geographical distribution of fossil fuels unused when limiting global warming to 2 °C. *Nature* 517, 187–190. https://doi.org/10.1038/nature14016
- Welsby, D., Price, J., Pye, S. & Ekins, P. (2021). Unextractable fossil fuels in a 1.5 °C world. *Nature* 597, 230–234. https://doi.org/10.1038/s41586-021-03821-8
- Semieniuk, G. et al. (2022). Stranded fossil-fuel assets translate to major losses for investors in advanced economies. *Nature Climate Change* 12, 532–538. https://doi.org/10.1038/s41558-022-01356-y
- SEC (2008). *Modernization of Oil and Gas Reporting*, Release 33-8995 (effective 1 Jan 2010). https://www.sec.gov/rules/final/2008/33-8995.pdf
- OCC (2018). *Comptroller's Handbook: Oil and Gas Exploration and Production Lending* (v2.2). https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/files/oil-gas-exploration-prod-lending/pub-ch-oil-and-gas.pdf
- NGFS (Nov 2024). *NGFS Scenarios: high-level overview (Phase V).* https://www.ngfs.net/system/files/import/ngfs/media/2024/11/05/ngfs_scenarios_high-level_overview.pdf
- IEA (2025). *World Energy Outlook 2025: Stated Policies Scenario.* https://www.iea.org/reports/world-energy-outlook-2025/stated-policies-scenario; CPS figure via DieselNet (12 Nov 2025) https://dieselnet.com/news/2025/11iea.php and Carbon Brief (12 Nov 2025) https://www.carbonbrief.org/iea-fossil-fuel-use-will-peak-before-2030-unless-stated-policies-are-abandoned

*Sovereign and peer documents*
- Norges Bank (14 Nov 2017). Letter to the Ministry of Finance: Investment strategy for the GPFG (oil and gas stocks). https://www.norges-bank.no/contentassets/5f4d6b9f67534cdebbd09a29215748bf/20171114_letter.pdf; press release https://www.norges-bank.no/en/Published/Press-releases/2017/2017-11-16-press-release/
- Norges Bank (26 Apr 2018). Energy stocks in the GPFG. https://www.nbim.no/contentassets/5beb197aa8c544b39fe547e2d6eb3b13/2018-04-26-nb-to-mof-energy-stocks-in-the-gpfg.pdf
- Ministry of Finance, Norway (8 Mar 2019). Excludes exploration and production companies from the GPFG. https://www.regjeringen.no/en/aktuelt/excludes-exploration-and-production-companies-from-the-government-pension-fund-global/id2631707/ (fetch blocked; content via search summary); phase-out letter (28 Jun 2019) https://www.regjeringen.no/en/aktuelt/phaseout-of-exploration-and-production-companies-from-the-gpfg/id2662141; CNBC (8 Mar 2019) https://www.cnbc.com/2019/03/08/norway-worlds-largest-sovereign-wealth-fund-to-scrap-energy-stocks.html
- Alaska Retirement Management Board, Board of Trustees meeting packet, 15–16 Sep 2026 (Day 2), pp. 383, 457–462 (copy downloaded by a sibling stream; materials index https://treasury.dor.alaska.gov/armb; notice https://aws.state.ak.us/OnlinePublicNotices/Notices/View.aspx?id=224974)
- Nevada System of Higher Education (Mar 2025). Endowment OCIO update (INV-6), CA vintage benchmarks at 30 Sep 2024. https://nshe.nevada.edu/html/wp-content/uploads/file/BoardOfRegents/Agendas/2025/03-mar-mtgs/refs/inv/INV-6.pdf

*Practitioner and market data*
- Meketa Investment Group (Mar 2024). *Private Natural Resources* white paper. https://meketa.com/wp-content/uploads/2024/03/MEKETA_Private-Natural-Resources.pdf
- Cambridge Associates (20 Sep 2017). Private Energy: Deserving a Place. https://www.cambridgeassociates.com/insight/private-energy-deserving-a-place/
- Cambridge Associates (21 May 2020). Real Asset Dynamics: PE Energy. https://www.cambridgeassociates.com/insight/real-asset-dynamics-pe-energy/
- Jefferies (Jul 2026). Global Secondary Market Review. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
- Haynes and Boone (25 Jan 2016). Spring 2016 borrowing base redeterminations survey. https://www.haynesboone.com/press-releases/spring-2016-borrowing-base-redeterminations
- NCREIF index returns (2Q2026). https://ncreif.org/indices/index-returns/
- Forisk (5 Jun 2026). Timberland Returns: Comparing the Drivers of Performance (1995–2025). https://forisk.com/timberland-returns-comparing-the-drivers-of-performance-1995-2025/
- AgIS Capital (6 Mar 2026). State of Returns, March 2026 (NCREIF Farmland Q4 2025). https://agiscapital.com/state-of-returns-march-2026/
- BHP (Feb 2026). BHP enters into a silver streaming agreement (Wheaton; $4.3bn upfront; 20% of spot). https://www.bhp.com/es/news/media-centre/releases/2026/02/bhp-enters-into-a-silver-streaming-agreement (fetch blocked; terms via search summary); Glencore, Streaming transaction – Antapaccay https://www.glencore.com/media/news/p/streaming-transaction-antapaccay
- IndexBox (Oct 2026). EU carbon prices reach EUR88 in September–October 2026. https://www.indexbox.io/blog/eu-carbon-prices-hit-eur88-per-tonne-as-october-council-talks-loom/
- Harvard natural resources write-down (2017): press reports, e.g. https://fa-mag.com/news/harvard-was--freaking-out---how-a--270-million-brazil-bet-tanked-51859.html [S, press]
- Setter Capital buyer survey, Mar 2020 (energy ≈41% of NAV): via PEI Secondaries Investor https://www.pei-secondariesinvestor.com/market-will-take-nine-months-to-return-to-normal-survey/ (paywalled) [U]

*Data*
- EIA, Europe Brent spot price FOB (RBRTE), daily. https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=D
- Kenneth R. French Data Library: 49 Industry Portfolios; Fama/French factors. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

*Project documents (carried, [C])*
- `research/00_SYNTHESIS.md` §§2.3, 4.1, 4.6, 4.7 (L3, L4); `research/dossiers/03_sovereign_alm.md` §§2–6; `research/groups/01_GROUPS_SYNTHESIS.md` §§2–4; `design/00_DESIGN_BRIEF.md` §§8–9; G15 synthetic book (`research/groups/addenda/G15_calcs/g15_ra_calcs.py`).
