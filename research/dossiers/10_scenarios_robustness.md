# Stream 10: Scenario generation, regime models, robustness and probabilistic stress testing

*Dossier for the ADIC multi-period robust TPA framework. Prepared 2026-10-18.*
*Evidence tags: **[S]** = sourced fact (URL in §10); **[P]** = practitioner consensus; **[I]** = my own inference or calculation. The **prototype** numbers come from scratch scripts that use the J.P. Morgan 2026 LTCMA risk matrix and **assumed** stylised weights. They are illustrative only and are not ADIC data.*
*Research constraint: this session's shared web-search budget ran out early. Sources were then read by fetching known primary URLs directly (arXiv, RePEc, Crossref, regulator and provider pages and files). Anything I could not verify is marked "unverified".*

---

## 1. Executive summary

1. **One scenario engine, many probability vectors.** Build a large, versioned **scenario matrix** Ξ: 50,000 joint paths, monthly steps, a 10-year horizon, with assets, private cash flows, liquidity, overlay drivers and the owner's distribution demand. It comes from a **regime-switching, fat-tailed factor ESG anchored to a capital-market-assumption (CMA) ensemble**. All robustness, stress-testing and IC-view work is then a *reweighting* (exponential tilt, entropy pooling) or a *transport* of that fixed matrix. This is cheap (O(N), milliseconds), auditable and internally consistent. It is Meucci's "fully flexible probabilities" idea extended to robustness [I].
2. **Model uncertainty swamps Monte Carlo error.** Take one stylised 60%-private book. Its expected compound return is **6.2% on AQR-based CMAs, 8.0% on J.P. Morgan 2026/2027 and 11.4% on BlackRock**. So P(5-yr annualised ≥10%) ranges from **27% to 59%**, while the MC standard error at 50k paths is about 0.2pp [I; inputs §4.1]. Extra paths buy almost nothing. The effort should go into model ensembles and robustness metrics.
3. **The prior deck's Tier-1 gate cannot be met as specified.** The gate is "≤5% probability that the 5-yr annualised return is below 7%". The 5-yr annualised σ is ≈5.9% (13% annual vol), so passing needs an expected return of ≈16.6%. Under 2026 CMAs the stylised book has **P(5y<7%) ≈ 24–55%** depending on provider [I]. Re-specify Tier 1 as **hard robust liquidity-survival constraints** plus a **robust-satisficing (fragility) floor** (§6.9).
4. **A cheap robustness layer.** It has exact or 1-D formulas on simulated scenarios:
   - KL worst-case event probability (Bernoulli-KL inversion);
   - KL worst-case expectation (Donsker–Varadhan dual);
   - KL worst-case CVaR (2-D convex);
   - Wasserstein-1 worst-case probability (greedy transport) and worst-case CVaR (= CVaR + ε/α);
   - the **breakdown divergence η\*** (reverse stress test);
   - the **robust-satisficing fragility k\***, which under KL equals the **Aumann–Serrano riskiness** of the surplus over target [I; theory S].
5. **Size the ambiguity radius by what experts disagree on and data cannot detect.** Cross-provider CMA dispersion gives 5-yr KL distances of 0.04–0.15 nats versus JPM, and 0.35 between AQR and BlackRock. With 20 years of returns, the chance of picking the wrong provider is still about 18–38% [I]. Recommended set-up:
   - treat the providers as a **structured** ambiguity set;
   - add an **unstructured** KL ball, η = 0.10, around each (Hansen & Sargent 2022 [S]).
6. **ESG specification.**
   - **Regimes:** K = 4 (expansion, inflationary late-cycle, crisis, recovery), with semi-Markov or jump-penalised persistence.
   - **Factors:** about 20 monthly factors, including oil, USD, VIX/skew, credit spreads, an exit-activity factor and a secondary-discount factor.
   - **Private returns:** a desmoothed factor model plus Getmansky–Lo–Makarov smoothing.
   - **Private cash flows:** Takahashi–Alexander with regime-dependent distribution rates, calibrated to the **≈14% distributions/NAV trough (Bain 2026 [S])**.
   - **Owner demand:** a stochastic 5–10% distribution demand linked to oil.
   - **Overlay:** implied-vol-surface factors with a variance risk premium.
7. **View conditioning by entropy pooling.**
   - IC views on factor means, event and regime probabilities, and distribution yields become linear constraints on q.
   - Each member's posterior is pooled log-linearly.
   - Diagnostics: effective number of scenarios (ENS) and KL(q‖p).
   - **LLMs draft constraints; humans supply the numbers.**
8. **Path counts.**
   - **Policy evaluation:** 50k paths. VaR99 SE ≈0.40pp, ES99 SE ≈0.82pp, SE of a 5% probability ≈0.10pp.
   - **Policy comparisons:** common random numbers.
   - **Optimisation:** 2–10k training scenarios, or SDDP on a Markov-regime policy graph.
   - **Testing:** an independent 50k test set.
   - **Scenario approach:** about 1,000 scenarios (exact minimum 986) for d = 30, ε = 5%, β = 10⁻³ (Campi–Garatti exact bound) [I; S]. The guarantee holds only for a convex scenario program, which the discrete SELL/HOLD/REFINANCE/LEVER actions break [corrected 2026-10-18: exact minimum and convexity requirement, per verification #18 and R9].
9. **Model risk management.** U.S. **SR 26-2 (17 Apr 2026) supersedes SR 11-7 and explicitly excludes generative and agentic AI from scope** [S].
   - The ESG, robustness and EP engines are "models" and need validation.
   - The LLM agents need a separate governance track (e.g., NIST AI 600-1).
   - They must not own numbers.

## 2. Core concepts and theory

### 2.1 Three layers of uncertainty
- **Risk:** randomness inside a model, handled by simulation.
- **Structured ambiguity:** a finite set of credible models M₁…M_K. Examples: CMA providers, regime specifications, private-asset smoothing and cash-flow parameters.
- **Unstructured misspecification:** nearby models that statistics cannot rule out, expressed as divergence balls around each M_k. Hansen & Sargent (2022) combine a structured family with relative-entropy misspecification [S].

ADIC's "robust floor under misspecification" should be computed over both layers, not over one Monte Carlo set [I].

### 2.2 The scenario-matrix paradigm and its exponential-family core
Let Ξ ∈ ℝ^{N×M} hold path features: 5-yr return, minimum liquidity headroom, drawdown, distribution shortfall, overlay P&L, factor summaries and regime occupancy. Let p ∈ Δ_N be the nominal scenario probabilities. Four distinct operations all have solutions of the same form, $q_i \propto p_i \exp(\lambda^\top g(\xi_i))$:
- **View conditioning (entropy pooling):** $\min_q \mathrm{KL}(q\|p)$ s.t. $E_q[g]=b$.
- **Worst case:** $\sup_{q:\mathrm{KL}(q\|p)\le\eta} E_q[\ell]$.
- **Reverse stress:** $\min_q \mathrm{KL}(q\|p)$ s.t. $E_q[\text{failure}]\ge\tau$.
- **Multiplier robustness:** $\min_q E_q[\ell]+\theta\,\mathrm{KL}(q\|p)$.

This unifies Meucci's entropy pooling, Breuer & Csiszár's maximum-loss theorem [S], Glasserman & Xu's worst-case model error [S], Pesenti et al.'s reverse sensitivity testing [S] and Hansen–Sargent multiplier preferences. One solver and one diagnostic set (KL, ENS) serve all four [I].

### 2.3 ESG model classes
- **VAR with predictors.** Campbell, Chan & Viceira (2003) model returns and state variables as a VAR, $z_{t+1}=\Phi_0+\Phi_1 z_t+v_{t+1}$. Predictability "greatly increases" optimal stock demand for long-horizon investors [S].
  - **Caveat:** Pástor & Stambaugh (2012) show that once parameter uncertainty and imperfect predictors are included, stocks are *more* volatile per year over long horizons [S].
  - Do not let mean reversion shrink 10-yr equity risk without parameter-uncertainty overlays [I].
- **Markov switching.** Hamilton (1989) introduced latent discrete regimes [S].
  - Ang & Bekaert (2002): bear regimes have higher volatility *and* higher cross-market correlation. Ignoring regimes is cheap for all-equity portfolios but costly when a conditionally risk-free asset exists [S].
  - Guidolin & Timmermann (2007): **four regimes ("crash, slow growth, bull and recovery")** are needed for joint stock–bond returns, and ignoring them has substantial welfare costs even after parameter uncertainty [S].
- **HMM, HSMM and jump models.**
  - Nystrup, Madsen & Lindström (2018) feed time-varying-HMM forecasts into model-predictive control. This beats static rules and buy-and-hold after costs and delays [S].
  - Nystrup, Lindström & Madsen (2020) penalise jumps to obtain persistent states [S].
  - Shu, Yu & Mulvey (2024) find statistical jump models more persistent and practical than HMMs out of sample over 1990–2023 [S].
- **Conditional heteroskedasticity, fat tails and dependence.**
  - GARCH or regime volatility with Student-t or skew-t innovations.
  - Pair-copula (vine) constructions for asymmetric tail dependence (Aas et al. 2009) [S].
  - The stationary bootstrap (Politis & Romano 1994), with data-driven block lengths (Politis & White 2004, as corrected by Patton, Politis & White 2009) [S].
  - Filtered historical simulation (Barone-Adesi, Giannopoulos & Vosper 1999) [S].
- **Generative market simulators.** Examples are Quant GANs (Wiese et al. 2020) and signature/VAE simulators built to work when training data are scarce (Bühler et al. 2026; preprint 2020) [S]. They reproduce stylised facts but are opaque, and GAN-type simulators are also data-hungry. Use them as validation challengers, not as the primary ESG [I].

### 2.4 Distributionally robust optimisation and robustness preferences
- **φ-divergence sets.** Ben-Tal, den Hertog, De Waegenaere, Melenberg & Rennen (2013) show φ-divergence balls are natural confidence sets for probability vectors and have tractable robust counterparts [S].
  - For KL, the Donsker–Varadhan dual gives
  $$\sup_{\mathrm{KL}(Q\|P)\le\eta}E_Q[\ell]=\inf_{\theta>0}\ \theta\eta+\theta\ln E_P\!\left[e^{\ell/\theta}\right],\qquad Q^\*\propto P\,e^{\ell/\theta^\*}.$$
  - **Limitation:** Q must be absolutely continuous with respect to P. **KL can only reweight simulated scenarios and cannot create worse ones** [I; LSZ note this, S].
- **Wasserstein balls.**
  - Mohajerin Esfahani & Kuhn (2018) give finite convex (often linear) reformulations with finite-sample guarantees [S].
  - Gao & Kleywegt (2023) prove strong duality and give an interpretable structure for worst-case distributions [S].
  - The Kuhn, Shafiee & Wiesemann survey (Acta Numerica 2025) is the current reference [S].
  - Wasserstein lets mass move to *new* outcomes, so it is the right complement to KL.
  - Wasserstein chance constraints reduce to CVaR-type constraints (Xie 2021) [S].
  - Under high ambiguity, risk-minimising portfolios converge to 1/N (Pflug, Pichler & Wozabal 2012) [S].
- **Moment-based sets.** Delage & Ye (2010) handle uncertainty in the mean and covariance [S]. This is useful for private assets, where only rough moments are credible [I].
- **Multiplier versus constraint robustness.** Hansen & Sargent (2001) compare the two robust-control formulations [S]. In portfolio settings, Maenhout (2004) finds robustness greatly reduces equity demand [S]. Separately, smooth ambiguity (Klibanoff, Marinacci & Mukerji 2005) separates ambiguity from attitude towards it [S].
  - **Calibrating θ.** Detection-error probabilities measure how hard it is to tell the approximating model from the worst-case model given historical data (Anderson, Hansen & Sargent 2003; Barillas, Hansen & Sargent 2009) [S].
- **Robust satisficing.** Long, Sim & Zhou (2023) solve
  $$\kappa_\tau=\min\ k\ \ \text{s.t.}\ \ E_P[f(x,\tilde z)]-\tau\le k\,\Delta(P,\hat P)\ \ \forall P,\qquad \tau\ge Z_0 .$$
  - The decision maker sets a **target τ** instead of a radius. κ_τ is the system's **fragility**, which is monotone, positively homogeneous and subadditive [S].
  - **Proposition 6** represents it as $\rho(v)=\inf\{k>0: k\,\mu(v/k)\le 0\}$ for a normalised convex risk measure μ [S].
  - With entropic μ (KL), this becomes $E_{\hat P}[e^{(f-\tau)/k}]\le 1$, i.e. **the Aumann–Serrano (2008) riskiness index** of the surplus τ−f [I; LSZ state the link, S]. For a normal surplus with mean m and variance s², **k\* = s²/(2m)** [S: Aumann–Serrano].
  - Related criteria: Brown & Sim (2009) satisficing measures and Chen & Sim (2009) goal-driven optimisation [S].
- **Model-risk measurement.** Glasserman & Xu (2014) bound worst-case risk-measurement error under a relative-entropy budget. Computing the bound takes "very little computational effort beyond that required to evaluate performance under the baseline nominal model" [S].

### 2.5 Probabilistic stress testing and views
- **Breuer & Csiszár (2013).** Search systematically for the worst case "within a relative entropy ball of sufficiently plausible scenarios". A maximum-loss theorem gives the worst-case distribution explicitly [S].
- **Glasserman, Kang & Kang (2015).** Reverse stress testing via an empirical-likelihood estimate of the conditional mean of factors given large losses, with confidence regions scaled by tail heaviness [S].
- **Pesenti, Millossovich & Tsanakas (2019).** Find the minimum-KL measure that produces a stressed VaR or ES, and rank inputs by how much their distributions move. One baseline simulation suffices [S].
- **Bayesian nets.** Rebonato & Denev (*Portfolio Management under Stress*, CUP 2014) elicit causal conditional probabilities to build coherent joint stress scenarios [S].
- **Entropy pooling.** Meucci ("Fully Flexible Views", *Risk* 2008; verified via arXiv:1012.2848) gives the KL projection above [S].
- **Elicitation and aggregation.** See O'Hagan et al. (2006) on eliciting expert probabilities [S] and Genest & Zidek (1986) on opinion pools [S].

## 3. Methods, models and trade-offs

**ESG engines (scored for ADIC's needs) [I]:**

| Engine | Tails/crisis dependence | Narrative/IC legibility | CMA anchoring | Parameters | Verdict |
|---|---|---|---|---|---|
| Gaussian VAR (CCV) | weak | medium | easy | low–med | baseline only |
| **Regime-switching factor VAR, t-innovations, regime-scaled covariance** | good | **high (named regimes)** | easy (ergodic matching) | medium | **primary** |
| Stationary bootstrap / FHS | empirical | low | hard | low | challenger, short horizon |
| Vine copula + GARCH | very good | low | medium | high | tail-dependence module |
| GAN/VAE simulators | good (stylised facts) | very low | hard | very high | validation challenger |

**Scenario reduction and trees for multi-stage optimisation:**
- forward selection or backward reduction of scenario *sets* under probability metrics (Heitsch & Römisch 2003) [S]. This suits two-stage problems and evaluation sets. Multistage decision trees must also control the filtration distance, so reduce them with the multistage method of Heitsch & Römisch (2009) [S] [corrected 2026-10-18: the 2003 algorithms do not preserve a multistage tree's information structure];
- moment matching by nonlinear programming (Høyland & Wallace 2001) [S];
- optimal discretisation and quantisation (Pflug 2001) [S]; k-means is a practical proxy;
- **SDDP on a Markovian policy graph**. Regimes become the nodes of a Markov chain and innovations are stagewise independent given the regime (Dowson 2020; SDDP.jl, Dowson & Kapelevich 2021) [S]. Risk-averse SDDP is in Philpott & de Matos (2012) [S]. This maps one-to-one onto a regime ESG and is the best fit for ADIC's annual decision stages [I].

**Statistical discipline for optimisation:**
- **Sample-average approximation** (Kleywegt, Shapiro & Homem-de-Mello 2002) with **optimality-gap bounds** (Mak, Morton & Wood 1999) [S].
- **The optimizer's curse.** Selected alternatives disappoint even under unbiased estimates (Smith & Winkler 2006) [S]. Data-snooping corrections are needed when many policies are tried (White 2000) [S]. This matters doubly when **agents** generate many candidate policies [I].
- **Scenario approach** (Campi & Garatti 2008): exact feasibility guarantees for convex programs with sampled constraints [S].
- **Nested simulation.** Future-node risk metrics (e.g., P99 margin at year 2) need inner simulations. Split the budget optimally (Gordy & Juneja 2010) or use regression proxies (Broadie, Du & Moallemi 2015) [S].

**Robustness instruments compared [I]:**

| Instrument | Captures | Misses | Cost on N scenarios | IC reading |
|---|---|---|---|---|
| Structured ensemble (CMA providers, regime specs) | disagreement among credible models | nearby unmodelled shapes | K× simulation (CRN) | "range across houses" |
| KL ball | reweighting toward bad regions | outcomes outside the simulated support | O(N) per 1-D dual | "probability shift we cannot rule out" |
| Wasserstein-1 | outcome shifts (bias, fees, mismeasurement) | regime-probability shifts | O(N log N) | "average return shift we cannot rule out" |
| Moment set | unknown shape with known moments | — | SDP/SOCP | private-asset parameters |
| Robust satisficing | fragility at a stated target | — | 1-D root per policy | "how much misspecification before the target fails" |

**View machinery:**
- **Black–Litterman** is the normal, linear special case.
- **Entropy pooling** handles any distribution, probability, quantile and ranking views, and non-linear views sequentially.
- **Bayesian nets** give causal coherence.
- **Re-simulation** is needed when a view changes *structure* (e.g., a new regime, or permanently lower PE distribution rates) [I].

## 4. Empirical evidence and current market data

### 4.1 Capital-market assumptions (USD nominal unless noted)

| Provider (as-of; published) | Horizon | US large cap | Global eq. | EM eq. | US Agg/bonds | Cash | US HY | PE | Private credit | Core RE | Infra | HF | 60/40 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **JPM LTCMA 2026** (30 Sep 2025; 20 Oct 2025), compound | 10–15y | 6.7 (σ16.5) | 7.0 ACWI (σ16.8) | 7.8 (σ20.9) | 4.8 (σ4.8) | 3.1 | 6.1 | 10.2 cap-wtd composite (σ19.8) | 7.7 DL (σ14.0) | 8.2 US | 6.5 | 5.3 div. | 6.4; 6.9 with 30% alts |
| **JPM LTCMA 2027** (30 Sep 2026; Oct 2026) | 10–15y | 7.5 (+80bp) | 7.5 (+50bp) | n/a | 5.3 global agg | n/a | n/a | 9.6 large-cap median mgr (−60bp) | n/a | 7.9 global core | 7.1 | 6.7 (+140bp) | 7.0; 7.5 with alts |
| **BlackRock** (30 Jun 2026; Aug 2026), 10y | 10y | 8.97 (σ19.4; IQR 4.1–14.0) | 9.02 ACWI | 8.80 | 4.88 | 3.66 | 6.43 | 15.89 US buyout (σ26.1; IQR 9.0–23.2) | 11.79 DL levered / 9.31 unlevered | 6.33 | 13.59 infra equity | 9.29 | 7.60 |
| **AQR** (31 Dec 2025; 14 Jan 2026), **local real** | 5–10y | 3.9 | 4.2 global | 5.1 | 2.5 (10y UST 2.4) | — | 2.7 | 4.2 US buyout (+0.9) | 2.6 | 3.1 | — | — | 3.4 global |
| **Vanguard VCMM** (30 Jun 2026) | 10y | 4.2–6.2 (US eq.) | 4.5–6.5 dev ex-US | — | — | — | — | — | — | — | — | — | — |

Sources [S]: JPM 2026 full report, assumption matrix (59 assets); JPM 2027 LTCMA page; BlackRock CMA workbook; AQR *Alternative Thinking 2026 Issue 1*; Vanguard return-forecast page.

**Not verified in session:** GMO's 7-year forecasts and Research Affiliates' AAI. The web-search budget was exhausted; they should be added to the ensemble.

**Additional facts [S]:**
- **JPM 2026 correlations:** PE–ACWI 0.81, PE–US large cap 0.75, ACWI–US Agg **+0.33**.
- **JPM 2026 inflation:** US inflation 2.5% (σ1.77).
- **Manager dispersion (JPM 2026):** about **1,960bp between top- and bottom-decile PE managers versus ≈200bp in public equity** over 10 years. This is a calibration target for asset-level idiosyncratic spread.
- **JPM 2026 on regimes:** investors should "place more weight on scenarios of inflation and rate volatility to complement growth shock scenarios". Stock–bond and stock–USD relationships are "changing – and unstable".
- **BlackRock scenario CMAs** (10y):

  | Scenario | US large cap | PE buyout | Global 60/40 |
  |---|---|---|---|
  | Base | 8.97% | 15.89% | 7.60% |
  | "AI productivity boom" | 15.94% | 27.61% | 8.06% |
  | "Global risk premia rise" | 2.02% | 9.36% | 6.37% |

- **AQR error bands:** a 50% chance that realised 10-yr equity returns miss its estimate by more than 3% p.a. Treating the band as normal implies σ ≈ 4.4% p.a. of *expected-return* uncertainty [I].

**Numerical pitfall [I]:** the published JPM 2026 correlation matrix is **not positive semi-definite** (min eigenvalue −0.016, from rounding). A Higham (2002) nearest-correlation repair changes no entry by more than 0.007.

### 4.2 What the CMA dispersion means for ADIC (prototype)
**Set-up [I]:**
- Stylised book with 60% private: PE 38, VC 4, direct lending 7, core RE 4, value-add RE 2, infrastructure 5; ACWI 22, Agg 6, IG 2, HF 6, cash 4.
- JPM 2026 vols and correlations are used throughout; only the means vary by provider.
- Where a provider gives no figure, the JPM 2026 value fills in. AQR real returns are converted to nominal by adding 2.4%.

| CMA set | Weighted geometric mean | P(5y ann. ≥10%) | P(5y ann. <7%) | 5-yr KL vs JPM-2026 |
|---|---|---|---|---|
| JPM 2026 | 7.98% | 37.5% | 43.8% | 0 |
| JPM 2027* | 7.98% | 37.5% | 43.8% | ≈0 |
| BlackRock* | 11.43% | 58.7% | 24.3% | 0.145 nats |
| AQR*-based | 6.17% | 27.1% | 55.3% | 0.043 nats |

(*mixed with JPM-2026 values where a provider is silent.)

**Further prototype results under JPM 2026 [I]:**
- **Full lognormal portfolio:** arithmetic 9.17%, vol 13.08%, geometric 8.39%; P(10y ≥10%) = 34.8%.
- **Leverage through the overlay at cash+50bp:**

  | Leverage | Geometric return | Vol | P(5y ≥10%) | P(5y <7%) |
  |---|---|---|---|---|
  | 1.15× | 8.99% | 15.0% | 44.0% | 38.1% |
  | 1.30× | 9.55% | 17.0% | 47.6% | 36.5% |

- **Detection:** for a 1.8pp mean gap (JPM vs AQR) with σ = 13%, the Bayes detection-error probability after 20 years of annual data is $\Phi(-\sqrt{20}\,\Delta/2\sigma)\approx 38\%$. For BlackRock vs AQR it is ≈18%.

The provider disagreement is therefore **statistically undetectable for decades**, which is exactly the Hansen–Sargent criterion for treating it as ambiguity rather than risk.

### 4.3 Private-markets liquidity regime (calibration targets) [S: Bain GPE Report 2026]
- **Buyout distributions/NAV ≈14%** (12 months to Q3 2025), **below 15% for four years running**, an industry record and a level last seen in 2008–09.
- **Unsold portfolio:** about **32,000 unsold companies worth $3.8tn**.
- **Holding periods:** ≈7 years at exit (vs 5–6 in 2010–2021). About 40% of companies have been held more than 5 years (29% in 2019).
- **Secondaries:** GP- and LP-led transaction value rose **41% YoY in 2025**. Continuation vehicles rose 62% YoY but are still **<10% of PE exit value**.
- **LP cash flow:** net cash flow was only modestly above breakeven in 2025.

**Implication [I]:** the low-distribution state is persistent, so it should be a *regime* in the cash-flow model, not a shock.

### 4.4 Monte Carlo precision (prototype, one-year loss ~ scaled Student-t with ν=5, vol 13%, true VaR99 = 25.9%) [I]

| N paths | Tail obs. | SE(VaR99) | SE(ES99) | SE of P = 5% | SE of P = 40% |
|---|---|---|---|---|---|
| 10,000 | 100 | 1.05pp | 1.81pp | 0.22pp | 0.49pp |
| 50,000 | 500 | 0.40pp | 0.82pp | 0.10pp | 0.22pp |
| 100,000 | 1,000 | 0.30pp | 0.54pp | 0.07pp | 0.15pp |
| 250,000 | 2,500 | 0.18pp | 0.36pp | 0.04pp | 0.10pp |
| 1,000,000 | 10,000 | ≈0.08pp | 0.18pp | 0.02pp | 0.05pp |

- **Formula check:** the asymptotic $\mathrm{SE}(\hat q_p)=\sqrt{p(1-p)/N}/f(q_p)$ matched the replications.
- **Paths for a 95% CI:** ±0.5pp on a 5% probability needs 7,300 paths; ±0.25pp on 2% needs 12,048; ±0.1pp on 1% needs 38,032.
- **Rare events:** for the deck's 0.6% 12-month breach risk, 50k paths give a relative SE of ≈5.8%.
- **Campi–Garatti exact bound (ε = 5%, β = 10⁻³):** N ≥ 447 for d = 10, 986 for d = 30 and 2,658 for d = 100. With ε = 1% and d = 30, N ≥ 4,970 [corrected 2026-10-18: exact minima per verification #18; the earlier 448 / 989 / 2,662 / 4,976 were sufficient but not minimal]. The guarantee requires a convex scenario program; ADIC's discrete SELL/HOLD/REFINANCE/LEVER actions break convexity (verification R9).

## 5. Practitioner and peer practice, case studies

- **CMA providers.**
  - JPM publishes full annual return, volatility and correlation matrices (2026: 59 USD assets). These are the cheapest anchor for ESG calibration, but need PSD repair.
  - **BlackRock** publishes quarterly CMAs with interquartile uncertainty bands and **scenario-conditional CMA sheets**. This is a practitioner precedent for exactly the "structured ambiguity set" recommended here.
  - AQR publishes 50% error bars; Vanguard publishes ranges from its VCMM distribution [S].
  - **[P]:** large allocators blend several providers' CMAs with a house view, rather than trusting one.
- **2022 as a case study [P/I].** Constant-correlation ESGs calibrated to 2000–2020 assumed negative stock–bond correlation. In 2022 both fell together. JPM's 2026 matrix now carries ACWI–Agg +0.33 [S].
  - Lesson: make the stock–bond correlation **regime-dependent**, negative in disinflationary crises and positive in inflation shocks. Include an inflationary regime.
- **Endowment cash-flow modelling.** Yale's Takahashi–Alexander (2002) model of calls, distributions and NAV is the industry template [S].
  - Its deterministic rates must become stochastic and regime-dependent to reproduce the 2022–25 distribution drought [I].
  - Appraisal smoothing should be modelled explicitly, as Getmansky, Lo & Makarov (2004) do for illiquid hedge-fund returns [S].
- **Model risk management.**
  - **SR 26-2** (Fed, FDIC, OCC; 17 Apr 2026) replaces SR 11-7 and SR 21-8 [S]. Key points:
    - It defines a model as a complex quantitative method, system or approach that "applies statistical, economic, or financial theories to process input data into quantitative estimates". Simple arithmetic and deterministic rule-based processes are excluded.
    - It keeps **effective challenge** and **validation = conceptual soundness + outcomes analysis + ongoing monitoring**, plus inventory, documentation and vendor-model rules.
    - It is risk-based and tailored, and is "most relevant" above $30bn of assets.
    - It states that "Generative AI and agentic AI models… are not within the scope of this guidance".
  - **PRA SS1/23** (principles for banks; effective 17 May 2024) was updated with low-impact amendments on **23 Apr 2026**. Its five principles are identification and tiering, governance, development/implementation/use, independent validation, and risk mitigants. Firms should manage risks from AI "in modelling techniques" [S].
  - **NIST AI 600-1** (26 Jul 2024) is the U.S. generative-AI risk profile complementing AI RMF 1.0 [S].
  - ADIC is not a bank, so these are best-practice references. The governance gap for agentic systems is now explicit in regulation [I].
- **Agentic orchestration.** *The Agentic Scientist* (Lange et al., arXiv:2610.18933, 13 Oct 2026) uses a meta-controller with **rubric verification at each stage**. Its ablations indicate that reliable autonomy depends on the cross-agent orchestration layer as well as on base-model capability [S]. Here, that means rubric gates on scenario quality, ENS, MC error and out-of-sample checks (§6.13).
- **Unverified in session (no URL):** insurers' prescribed real-world ESGs (e.g., US statutory reserving) and regulator-prescribed uniform scenario sets for Dutch pension funds. They are worth checking as precedents for *fixed, governed scenario sets with fixed path counts*.

## 6. Design implications for the ADIC framework

### 6.1 State vector (simulation grid: monthly; private cash flows quarterly; decisions annual)
| Block | Variables | Role |
|---|---|---|
| Regime | S_t ∈ {1..4}, regime duration d_t | drives all conditional moments |
| Macro | global growth (IP/PMI proxy), US CPI, policy rate, 10y UST, 2s10s, Brent (log), USD index (log) | fiscal link, inflation regimes, discounting |
| Credit | IG OAS, HY OAS, private-credit default/loss rate | private credit, NAV-loan pricing |
| Equity and vol | ACWI and EM excess returns, log VIX, 25Δ skew, term slope | overlay pricing, PE betas, margin |
| Private markets | desmoothed PE/VC/RE/infra returns; exit-activity index X^{exit}; secondary discount δ; NAV-loan spread and max LTV | SELL / HOLD / REFINANCE / LEVER payoffs |
| Liability | owner distribution demand d_t ∈ [5%, 10%] | stochastic outflow |
| Overlay | futures/swap returns, implied surface, VM/IM | tail hedge and opportunistic book |

### 6.2 Regime and factor dynamics
**Regime chain.** $S_t$ follows a hidden semi-Markov chain with negative-binomial dwell times, or a Markov chain fitted with a jump penalty. The transition matrix Π has stationary distribution π.

**Factor dynamics.**
$$x_t=c_{S_t}+A\,x_{t-1}+D_{S_t}L_{S_t}\varepsilon_t,\quad \varepsilon_t\sim t_\nu(0,I)\ \text{scaled to unit variance},$$
with $R_s=(1-\omega_s)R_0+\omega_s R_{\text{crisis}}$ and $D_s=\mathrm{diag}(\sigma_s)$.

**Parsimony.** Regimes move means, a volatility multiplier per block and the blend weight ω_s. A full covariance per regime would need about 600 parameters on about 430 monthly observations [I].

**Asset returns.**
$$r_{i,t}=a_{i,S_t}+b_i^\top x_t+\sigma_{i,S_t}u_{i,t}.$$

**Starting point.** Simulation starts from the current filtered regime probabilities (from the deck's State/Fragility engine, which combines an HMM/HSMM with turbulence and absorption-ratio fragility indicators; their standard sources are Kritzman & Li 2010 and Kritzman, Li, Page & Rigobon 2011 [S]) and current yields, spreads, VIX and oil. Near-term paths then reflect today's state, while long-run moments converge to the CMA anchors.

**Defaults [I]:**
- K = 4, chosen from K ∈ {3, 4, 5} by out-of-sample log score;
- ν = 5;
- crisis dwell 6–18 months and expansion 36–60 months, both to be estimated.

### 6.3 Private markets and SELL / HOLD / REFINANCE / LEVER drivers
- **True return:** $r^\*_{j,t}=\alpha_j+\beta_j^\top f_t+e_{j,t}$.
- **Reported return:** $r^{rep}_{j,t}=\sum_{k=0}^{K}\theta_{jk}r^\*_{j,t-k}$, with $\sum_k\theta_{jk}=1$ [GLM 2004].
- **Calls:** $C_{j,t}=\gamma_c(S_t,\text{age})\,U_{j,t}$.
- **Distributions:** $D_{j,t}=\gamma_d(S_t,\text{age},X^{exit}_t)\,NAV_{j,t}$.
- **NAV roll-forward:** $NAV_{j,t+1}=NAV_{j,t}(1+r^\*_{j,t})+C_{j,t}-D_{j,t}$.

**Calibration targets for γ_d.** Use regime means that reproduce **≈14% p.a. distributions/NAV in the drought regime** [S: Bain]. Higher normal-regime rates should be estimated from ADIC's own cash flows and MSCI/Burgiss data.

**Pathwise action values:**
- **SELL:** secondary price $P^{sec}_{j,t}=NAV_{j,t}(1-\delta_{j,t})$, with $\delta_{j,t}=\delta_0+\delta_1\mathbb 1\{S_t=\text{crisis}\}+\delta_2(-r^{eq}_{t-3:t})^+ +\text{quality/age}+\text{noise}$.
- **REFINANCE:** NAV-loan rate = SOFR + s₀ + s₁·HY OAS, with LTV_max(S_t).
- **LEVER:** fund- or asset-level leverage cost as a function of the same rate.
- **HOLD:** the baseline cash-flow path.

All δ, s and LTV values are to be calibrated. No defaults are asserted here.

**Idiosyncratic spread.** Asset-level e_{j,t} should reproduce the large PE manager dispersion (≈1,960bp top-vs-bottom decile [S: JPM]).

### 6.4 Owner distribution demand (stochastic liability)
$$d_t=\mathrm{clip}\!\big(\bar d+\kappa_{oil}(\ln\bar O-\ln O_t)+\kappa_{f}\,\xi_t,\ 5\%,\ 10\%\big)\times NAV_t .$$
When oil (and usually risk assets) fall, the demand rises. This is **wrong-way risk** for the liquidity gate. The oil link is a design hypothesis to confirm with ADIC's owner-policy data [I].

### 6.5 Overlay drivers and pricing consistency
- **ATM vol:** $\ln\sigma^{ATM}_{t+1}=\mu_\sigma(S)+\phi(\ln\sigma^{ATM}_t-\mu_\sigma(S))+\rho\,\eta^{eq}_{t+1}+J_{t+1}$, with a strongly negative equity link. Model skew and term slope as correlated AR factors.
- **Surface shape:**
  - surface factors follow Cont & da Fonseca (2002) [S];
  - each expiry slice is an arbitrage-free SVI (Gatheral & Jacquier 2014) [S];
  - the sticky-moneyness rule is refined by the factor link.
- **Variance risk premium:** on average the premium, measured as realised variance minus the variance-swap rate, is negative, so implied variance exceeds realised variance (Carr & Wu 2009) [S] [unverified: the sign of the average premium is confirmed only by secondary literature; full text not accessed]. That this holds in calm regimes is [I]. Tail hedges therefore bleed carry in calm regimes and pay convexly in crisis paths.
- **Valuation:** at every node, value options with Black–Scholes on the simulated surface (Q-measure). Paths evolve under P.
- **Margin:** VM is the negative change in MTM. IM is sensitivities times regime-scaled risk weights.
- **Validation:** replay the hedge P&L through 2008, 2020, 2022 and the 2025 tariff shock [I].

### 6.6 Calibration procedure
1. **Fit** the regime and factor model on monthly data from 1990–2026, extending to the 1970s for the inflation block.
2. **Ergodic mean matching.** With regime-invariant A, the long-run mean is $\bar m=(I-A)^{-1}\sum_s\pi_s c_s$. Set $c_s\leftarrow c_s+(I-A)(m^{CMA}-\bar m)$. This hits CMA targets exactly while preserving regime spreads.
3. **Asset intercepts.** Shift $a_{i,s}$ by a constant Δ_i, solved by 1-D root-finding, so that the 10-yr expected *compound* return equals each CMA. Mind the arithmetic vs compound convention; JPM publishes both.
4. **Volatilities and correlations.** Scale the volatility multipliers to the CMA vols, then apply a Higham repair.
5. **Private assets.** Fit desmoothing on ADIC NAV series, then cash-flow rates by strategy, vintage and regime.
6. **Ensemble.** M_k ∈ {JPM-2027, JPM-2026, BlackRock base, BlackRock "risk premia rise", AQR-nominal, house view, GMO/RA when verified}. Simulate all models with **common random numbers** (same ε, different intercepts), so model differences are pure. Default prior weights are equal, then IC-set.

### 6.7 Path counts and compute budget
| Use | Paths × steps | Notes |
|---|---|---|
| Policy evaluation and IC metrics | 50,000 × 120 months, per ensemble model | float32; SE table §4.4 |
| Policy comparison | same draws (CRN) | paired differences |
| Final tail sign-off (P99.5 margin, breach <1%) | 250k or importance sampling toward the crisis regime | — |
| Optimisation training | 2,000–10,000 reduced scenarios, or SDDP policy graph | Heitsch–Römisch (2009) multistage tree reduction / k-means + moment match [corrected 2026-10-18] |
| Out-of-sample test | independent 50,000 | Mak–Morton–Wood gap, 10–20 replications |
| Scenario-approach chance constraints | ≥986, i.e. about 1,000 (d ≤ 30, ε = 5%, β = 10⁻³) | Campi–Garatti; convex scenario programs only [corrected 2026-10-18] |
| Future-node risk metrics | regression-based nested simulation (few inner draws per outer scenario) | Broadie–Du–Moallemi [corrected 2026-10-18] |

### 6.8 Robustness layer (operates on any scenario matrix; per policy; all O(N))
Let y be a scenario outcome (e.g., 5-yr annualised return), ℓ a loss, A a failure event, p nominal weights, and p_A = p(A).

- **R1. KL worst-case probability.**
  $$\bar P_\eta(A)=\max\{q\ge p_A:\ q\ln\tfrac{q}{p_A}+(1-q)\ln\tfrac{1-q}{1-p_A}\le\eta\}.$$
  Solve by bisection. This is exact by the data-processing inequality [I].
- **R2. KL worst-case expectation.**
  $$\bar E_\eta[\ell]=\inf_{\theta>0}\ \theta\eta+\theta\ln\sum_i p_i e^{\ell_i/\theta}.$$
  This is a 1-D convex problem; use log-sum-exp.
- **R3. KL worst-case CVaR_α.**
  $$\min_t\ \big\{t+\alpha^{-1}\bar E_\eta[(\ell-t)^+]\big\}.$$
  This is jointly convex in (t, θ). Sion's minimax theorem justifies swapping the sup over Q and the min over t [I].
- **R4. W1 worst-case P(y < τ).** Use |·| cost on y.
  1. Sort $d_{(1)}\le d_{(2)}\le\dots$, the distances of the non-failing atoms to τ.
  2. Set $k=\max\{k:\sum_{j\le k}d_{(j)}\le N\varepsilon\}$.
  3. Then $\bar P_\varepsilon=p_A+\frac1N\big[k+(N\varepsilon-\sum_{j\le k}d_{(j)})/d_{(k+1)}\big]$ [I].
- **R5. W1 closed forms.** Worst-case CVaR_α(ℓ) = CVaR_α + ε/α, because $(\ell-t)^+$ is 1-Lipschitz and the bound is attained by shifting the α-tail. Worst-case mean return = E[y] − ε [I].
- **R6. Breakdown divergence (reverse stress).**
  $$\eta^\*=\min_q \mathrm{KL}(q\|p)\ \text{s.t.}\ E_q[y]\le\tau,\qquad q^\*\propto p\,e^{-\theta y}.$$
  Report the tilted factor means, $E_{q^\*}[x]-E_p[x]$, and the regime occupancy. Translate η\* into (a) a Gaussian mean shift $\sigma_y\sqrt{2\eta^\*}$ and (b) a detection-error probability.
- **R7. Fragility (robust satisficing, KL).**
  $$k^\*=\inf\{k>0:\ \textstyle\sum_i p_i e^{(f_i-\tau)/k}\le1\},$$
  which requires $E_p[f]<\tau$. Normal approximation: $k^\*\approx\sigma^2/(2(\tau-\mu))$.
- **R8. Structured layer.** Compute every metric for each M_k and report the min, max and mixture.

**Defaults [I]:**
- η ∈ {0.02, 0.05, **0.10**, 0.20} nats on the 5-yr path law. Justification: cross-provider KL is 0.04–0.15 and the detection-error probability at 20 years is ≥18%.
- ε ∈ {0.25, **0.5**, 1.0}pp of annualised return (fee, smoothing and measurement bias).

**Prototype on 50k simulated 5-yr outcomes** (regime-mixture, nominal P(5y<7%) = 40.6%) [I]:

| Metric | Nominal | Robust value |
|---|---|---|
| KL worst-case P(5y<7%) | 40.6% | 47.6% (η=0.01) · 56.3% (η=0.05) · 62.8% (η=0.10) · 71.9% (η=0.20) |
| W1 worst-case P(5y<7%) | 40.6% | 57.5% (ε=0.25pp) · 64.5% (ε=0.5pp) · 74.2% (ε=1pp) |
| KL worst-case mean (η=0.10) | 8.61% | 5.48% |
| ENS/N of the η=0.10 tilt | — | 0.905 |

- **Breakdown divergence for E[R5] ≤ 7%:** η\* = 0.027 nats, i.e. a 1.6pp Gaussian mean shift. That is *smaller* than the 1.8pp JPM–AQR gap, so the 7% expected-return floor is fragile to the choice of CMA provider.
- **Fragility:** k\* = 0.153, which matches the Aumann–Serrano normal formula s²/(2m) = 0.07²/(2·0.0161) = 0.152.

### 6.9 Re-specified Tier 1 and objective terms
**T1-L, hard liquidity survival.** For every M_k and every Q with KL(Q‖P_k) ≤ η_L:
- P_Q(liquid buffer < 0 within 24m) ≤ 1%;
- P_Q(forced secondary sale at δ > δ_max) ≤ 2%;
- the haircut 30-day liquidity covers P99 margin plus stressed 12-month net calls plus the distribution demand d_t.

Checks are monthly, using R1 and R3.

**T1-F, robust floor.** Require nominal mixture E[R5] ≥ 7% (or a real/distribution-adjusted floor to be decided), then **minimise k\*** or **maximise η\***. Report P(5y<7%) with its ensemble range instead of gating it at 5%. The 5% gate rejects every realistic book (§4.2).

**Tier 2.** Maximise the ensemble-robust P(5y ≥ 10%), or KL-robust expected utility, net of shadow costs. This cross-links to the optimiser stream.

**IC card per policy:**
- nominal value ± MC SE;
- ensemble min/max;
- KL(0.10) and W1(0.5pp) worst cases;
- η\* and k\*;
- the tilted-world narrative;
- metrics under each IC member's view posterior and under the pooled posterior;
- a decision-stability flag.

### 6.10 View conditioning (entropy pooling)
**Problem.**
$$\min_q\sum_i q_i\ln\frac{q_i}{p_i}\ \text{s.t.}\ Gq=b,\ Hq\le c,\ \mathbf 1^\top q=1 .$$

**Dual.**
$$\min_{\lambda,\ \nu\ge0}\ \ln\sum_ip_i e^{\lambda^\top g_i-\nu^\top h_i}-\lambda^\top b+\nu^\top c,\qquad q_i\propto p_ie^{\lambda^\top g_i-\nu^\top h_i}.$$

Solve with BFGS or Newton. The dimension equals the number of views, typically 2–20.

**View taxonomy:**
- factor means (oil average over 2y);
- event probabilities, e.g. P(recession by 2028) = 35%;
- **regime-path probabilities**, e.g. P(crisis regime in Y1) = 25%;
- quantiles, e.g. P(10y UST > 5.5%) = 10%;
- rankings, e.g. E[PE − ACWI] ≥ 1%;
- **cash-flow views**, e.g. P(PE distributions/NAV < 12% for 2 years) = 60%;
- volatility and correlation views, handled by sequential EP (fortitudo.tech implements SeqEP [S]).

**Confidence and pooling.**
- Confidence blend: $q_c\propto p^{1-c}q^c$ (log-linear).
- IC pooling: $q^{pool}\propto\prod_m (q^{(m)})^{w_m}$. Logarithmic pools are externally Bayesian; linear pools preserve marginals. These properties are reviewed in Genest & Zidek (1986) [P].
- Disagreement is the Jensen–Shannon divergence among the $q^{(m)}$.
- **Decision relevance:** does the ranking of policies change under any member's posterior?

**Diagnostics and gates [I]:**
- ENS = exp(−Σq ln q), the effective number of scenarios of Meucci (2012) [S]: warn below 0.10N and block below 0.02N. Below the block level, regenerate with importance sampling toward the view region.
- Report KL(q‖p) as "distance the IC moved the base case" and warn above 0.25 nats.
- Check LP feasibility of the views before solving.

**Prototype [I]:** two views (E[oil] = −15%; P(stress-heavy path) from 6.1% to 15%) were met exactly, with KL = 0.091, ENS/N = 0.91 and P(5y<7%) moving from 40.6% to 45.0%.

**Narrative-to-numbers workflow.**
1. An LLM agent turns IC narrative ("prolonged exit drought, $55 oil, sticky inflation") into a *table* of candidate constraints with sources and analogues.
2. Members supply the probabilities, individually first and then after discussion (O'Hagan et al. 2006 protocol style).
3. The deterministic engine solves.
4. The IC signs off the view table, which is versioned.

For causal coherence across multiple shocks, elicit a small Bayesian net (Rebonato–Denev) and pass its joint event probabilities to EP as views.

### 6.11 Reverse stress outputs (per recommended policy)
- the most plausible failure world: q\* from R6, with η\*;
- factor shifts under q\*, e.g. oil, distribution rate, secondary discount, VIX;
- the regime-occupancy shift;
- GKK's conditional factor mean given loss > threshold, with confidence region [S];
- Pesenti-style sensitivity ranking: which inputs' distributions move most [S].

### 6.12 Data needs
- monthly macro-financial history (yields, spreads, oil, USD, VIX, implied surfaces);
- ADIC fund-level cash flows and NAVs by strategy and vintage;
- secondary-pricing history;
- NAV-loan term sheets;
- OTC positions and CSA/IM terms;
- owner distribution history and fiscal/oil linkage;
- provider CMA files (JPM matrix, BlackRock xlsx, AQR tables), versioned by as-of date.

### 6.13 Agent roles and rubric gates (cross-link: architecture stream)
| Agent | Role | Gate |
|---|---|---|
| Scenario Architect | drafts ESG configs and runs calibration in a sandbox | stylised-fact rubric: fat tails, volatility clustering, leverage effect, crisis correlation |
| Calibration Validator | checks CMA match, PSD, MC SE | |
| Robustness Auditor | runs R1–R8 | no recommendation if η\* < η_min without an IC flag |
| Stress Narrator | turns q\* into prose | numbers pulled only from the engine |
| View Elicitor | builds the constraint table | never invents probabilities |
| MRM Validator | out-of-sample, benchmarking, sensitivity | counts the policies tried (data-snooping log) |

## 7. Implementation notes
- **Core:** numpy/scipy (`special.logsumexp`, `optimize.brentq`, `minimize`), with numba or JAX for path loops. `scipy.stats.qmc.Sobol` with a Brownian-bridge ordering for factor shocks.
- **Regimes:**
  - statsmodels `MarkovRegression`/`MarkovAutoregression` (univariate);
  - hmmlearn `GaussianHMM` (multivariate);
  - jump models (Shu et al.; package name unverified);
  - HSMM via custom EM or pomegranate (not checked).
- **Volatility and bootstrap:** `arch` (GARCH family, `StationaryBootstrap`, optimal block length; block-length code should follow the Patton, Politis & White 2009 correction).
- **Copulas:** pyvinecopulib (not installed in the lab venv).
- **Optimisation and transport:** cvxpy (CVaR LPs à la Rockafellar–Uryasev 2000 [S]; Wasserstein DRO); POT for optimal transport.
- **Entropy pooling:** fortitudo.tech v1.2.5 (20 Aug 2026) [S], licensed **GPL-3.0-or-later**. Prefer an in-house ~50-line dual solver to avoid copyleft [I].
- **SDDP:** SDDP.jl (Julia) [S].
- **Complexity:** EP dual O(N·V) per iteration; KL duals O(N) per θ; W1 greedy O(N log N).
  - Memory for 50k×120×25 float32 is ≈0.6GB, so store path *features* and only selected full paths.
- **Numerical pitfalls:**
  - always use log-sum-exp;
  - KL tilts on heavy-tailed losses are dominated by a few scenarios, so monitor the ENS of every tilt;
  - non-PSD vendor matrices need a Higham repair;
  - label switching across re-estimations: anchor regimes by ordering crisis volatility;
  - keep the arithmetic vs geometric convention consistent;
  - seed management: CRN across policies and models, an independent seed stream for testing, and a scenario-set hash in every IC output.
- **Prototype provenance:** the scratch scripts (`proto_robust.py`, `cma_ensemble.py`, `jpm_matrix.py`) can be ported into `src/`.

## 8. Risks, pitfalls and limitations
- **False precision.** Model dispersion is about 5pp of mean return against an MC SE of 0.2pp. IC outputs must lead with ensemble ranges.
- **Infeasible gates.** The 5% Tier-1 gate either rejects everything or gets quietly relaxed. Re-specify it explicitly (§6.9).
- **KL support blindness.** KL cannot create worse-than-simulated outcomes. Pair it with Wasserstein and deliberate crisis-regime oversampling.
- **Wasserstein metric choice.** Results depend on the outcome space and cost units. Define ε on interpretable outcomes, not raw factor space.
- **Regime models:** look-ahead bias in labels, instability of K, over-reaction to filtered probabilities. Mitigate with jump penalties, out-of-sample log-score selection and posterior smoothing.
- **CMA herding.** Providers share methods, so the ensemble may understate true ambiguity. Keep a house "stagnation" model and BlackRock's downside scenario.
- **Private data.** Smoothing, survivorship and stale NAVs. The DPI drought may be structural; a permanent shift needs re-simulation, not just a view.
- **Optimizer's curse and agent p-hacking.** Many agent-generated policies tested on the same scenarios inflate apparent edge. Use a locked test set and shrink selected advantages (Smith–Winkler; White).
- **View manipulation.** Entropy pooling can encode any belief. Discipline it with elicitation protocols, a KL budget and an audit trail.
- **Governance gap.** SR 26-2 excludes generative and agentic AI. Without a separate AI-governance track, LLM-translated views or extracted assumptions could enter validated models unchecked.

## 9. Open questions
1. **Owner policy.** How is the 5–10% distribution actually set (rule, discretion, oil linkage)? Can a smoothing rule be negotiated?
2. **Floor definition.** Should the floor be nominal or real, 5 or 10 years, before or after distributions? What breach tolerance will the IC accept under honest CMAs?
3. **Provider weights.** IC-set, equal, or performance-scored? Should the BlackRock downside sheet enter as a separate model?
4. **Missing providers.** GMO and Research Affiliates 2026 numbers need verifying when search capacity returns.
5. **Data.** Are fund-level cash flows by strategy and vintage, secondary-bid history and NAV-loan terms available, and back to which year?
6. **Tooling.** Is a Julia dependency acceptable for SDDP, or should the project stay in Python with reduced trees and decision rules?
7. **Currency.** Is the base currency USD-pegged? Confirm, and decide whether a non-USD liability view is needed.
8. **Elicitation appetite.** How formal should elicitation be (SHELF/IDEA-style rounds), and should members' calibration be scored over time?

## 10. References
(Verified in session unless marked; "via" = the page used to verify.)
- Aas, K., Czado, C., Frigessi, A., Bakken, H. (2009). Pair-copula constructions of multiple dependence. *Insurance: Math. & Econ.* 44(2):182–198. DOI 10.1016/j.insmatheco.2007.02.001. https://ideas.repec.org/a/eee/insuma/v44y2009i2p182-198.html
- Anderson, E., Hansen, L.P., Sargent, T.J. (2003). A quartet of semigroups for model specification, robustness, prices of risk, and model detection. *JEEA* 1(1):68–123. https://ideas.repec.org/a/tpr/jeurec/v1y2003i1p68-123.html
- Ang, A., Bekaert, G. (2002). International asset allocation with regime shifts. *RFS* 15(4):1137–1187. DOI 10.1093/rfs/15.4.1137. https://ideas.repec.org/a/oup/rfinst/v15y2002i4p1137-1187.html
- AQR Portfolio Solutions Group (2026). *Capital Market Assumptions for Major Asset Classes*, Alternative Thinking 2026 Issue 1 (as of 31 Dec 2025). https://www.aqr.com/Insights/Research/Alternative-Thinking/2026-Capital-Market-Assumptions-for-Major-Asset-Classes
- Aumann, R.J., Serrano, R. (2008). An economic index of riskiness. *JPE* 116(5):810–836. https://ideas.repec.org/a/ucp/jpolec/v116y2008i5p810-836.html
- Bain & Company (2026). *Global Private Equity Report 2026*. https://www.bain.com/insights/topics/global-private-equity-report/
- Barillas, F., Hansen, L.P., Sargent, T.J. (2009). Doubts or variability? *JET* 144(6):2388–2418. DOI 10.1016/j.jet.2008.11.014. https://ideas.repec.org/a/eee/jetheo/v144y2009i6p2388-2418.html
- Barone-Adesi, G., Giannopoulos, K., Vosper, L. (1999). VaR without correlations for portfolios of derivative securities. *J. Futures Markets* 19(5):583–602. DOI `10.1002/(SICI)1096-9934(199908)19:5<583::AID-FUT5>3.0.CO;2-S`. https://ideas.repec.org/a/wly/jfutmk/v19y1999i5p583-602.html
- Ben-Tal, A., den Hertog, D., De Waegenaere, A., Melenberg, B., Rennen, G. (2013). Robust solutions of optimization problems affected by uncertain probabilities. *Management Science* 59(2):341–357. DOI 10.1287/mnsc.1120.1641. https://ideas.repec.org/a/inm/ormnsc/v59y2013i2p341-357.html
- BlackRock Investment Institute (Aug 2026; data 30 Jun 2026). Capital market assumptions (workbook incl. scenario sheets). https://www.blackrock.com/institutions/en-us/insights/charts/capital-market-assumptions
- Board of Governors of the Federal Reserve System, FDIC, OCC (17 Apr 2026). SR 26-2: Revised Guidance on Model Risk Management (supersedes SR 11-7, SR 21-8). https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm ; attachment https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf
- Breuer, T., Csiszár, I. (2013). Systematic stress tests with entropic plausibility constraints. *JBF* 37(5):1552–1559. https://ideas.repec.org/a/eee/jbfina/v37y2013i5p1552-1559.html
- Broadie, M., Du, Y., Moallemi, C.C. (2015). Risk estimation via regression. *OR* 63(5):1077–1097. DOI 10.1287/opre.2015.1419. https://ideas.repec.org/a/inm/oropre/v63y2015i5p1077-1097.html
- Brown, D.B., Sim, M. (2009). Satisficing measures for analysis of risky positions. *Management Science* 55(1):71–84. https://ideas.repec.org/a/inm/ormnsc/v55y2009i1p71-84.html
- Bühler, H., Horvath, B., Lyons, T., Perez Arribas, I., Wood, B. (2026). A data-driven market simulator for small data environments. In *Stochastic Analysis and Applications 2025*, Springer Nature Switzerland, pp. 273–310 (online 1 Apr 2026). https://doi.org/10.1007/978-3-032-03914-9_10 (preprint: Buehler et al. 2020, arXiv:2006.14498, https://arxiv.org/abs/2006.14498)
- Campbell, J.Y., Chan, Y.L., Viceira, L.M. (2003). A multivariate model of strategic asset allocation. *JFE* 67(1):41–80. DOI 10.1016/S0304-405X(02)00231-3. https://ideas.repec.org/a/eee/jfinec/v67y2003i1p41-80.html
- Campi, M.C., Garatti, S. (2008). The exact feasibility of randomized solutions of uncertain convex programs. *SIAM J. Optim.* 19(3):1211–1230. https://doi.org/10.1137/07069821X
- Carr, P., Wu, L. (2009). Variance risk premiums. *RFS* 22(3):1311–1341. DOI 10.1093/rfs/hhn038. https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1311-1341.html
- Chen, W., Sim, M. (2009). Goal-driven optimization. *OR* 57(2):342–357. DOI 10.1287/opre.1080.0570. https://ideas.repec.org/a/inm/oropre/v57y2009i2p342-357.html
- Cont, R., da Fonseca, J. (2002). Dynamics of implied volatility surfaces. *Quant. Finance* 2(1):45–60. DOI 10.1088/1469-7688/2/1/304. https://ideas.repec.org/a/taf/quantf/v2y2002i1p45-60.html
- Delage, E., Ye, Y. (2010). Distributionally robust optimization under moment uncertainty with application to data-driven problems. *OR* 58(3):595–612. DOI 10.1287/opre.1090.0741. https://ideas.repec.org/a/inm/oropre/v58y2010i3p595-612.html
- Dowson, O. (2020). The policy graph decomposition of multistage stochastic programming problems. *Networks* 76(1):3–23. https://doi.org/10.1002/net.21932
- Dowson, O., Kapelevich, L. (2021). SDDP.jl: a Julia package for stochastic dual dynamic programming. *INFORMS J. Computing* 33(1):27–33. https://ideas.repec.org/a/inm/orijoc/v33y2021i1p27-33.html
- Gao, R., Kleywegt, A.J. (2023). Distributionally robust stochastic optimization with Wasserstein distance. *Math. of OR* 48(2):603–655. https://doi.org/10.1287/moor.2022.1275 (preprint arXiv:1604.02199, https://arxiv.org/abs/1604.02199)
- Gatheral, J., Jacquier, A. (2014). Arbitrage-free SVI volatility surfaces. *Quant. Finance* 14(1):59–71. DOI 10.1080/14697688.2013.819986. https://ideas.repec.org/a/taf/quantf/v14y2014i1p59-71.html
- Genest, C., Zidek, J.V. (1986). Combining probability distributions: a critique and an annotated bibliography. *Statistical Science* 1(1):114–135. https://doi.org/10.1214/ss/1177013825
- Getmansky, M., Lo, A.W., Makarov, I. (2004). An econometric model of serial correlation and illiquidity in hedge fund returns. *JFE* 74(3):529–609. DOI 10.1016/j.jfineco.2004.04.001. https://ideas.repec.org/a/eee/jfinec/v74y2004i3p529-609.html
- Glasserman, P., Kang, C., Kang, W. (2015). Stress scenario selection by empirical likelihood. *Quant. Finance* 15(1):25–41. https://ideas.repec.org/a/taf/quantf/v15y2015i1p25-41.html
- Glasserman, P., Xu, X. (2014). Robust risk measurement and model risk. *Quant. Finance* 14(1):29–58. https://ideas.repec.org/a/taf/quantf/v14y2014i1p29-58.html
- Gordy, M.B., Juneja, S. (2010). Nested simulation in portfolio risk measurement. *Management Science* 56(10):1833–1848. DOI 10.1287/mnsc.1100.1213. https://ideas.repec.org/a/inm/ormnsc/v56y2010i10p1833-1848.html
- Guidolin, M., Timmermann, A. (2007). Asset allocation under multivariate regime switching. *JEDC* 31(11):3503–3544. https://ideas.repec.org/a/eee/dyncon/v31y2007i11p3503-3544.html
- Hamilton, J.D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica* 57(2):357–384. DOI 10.2307/1912559. https://ideas.repec.org/a/ecm/emetrp/v57y1989i2p357-84.html
- Hansen, L.P., Sargent, T.J. (2001). Robust control and model uncertainty. *AER* 91(2):60–66. https://ideas.repec.org/a/aea/aecrev/v91y2001i2p60-66.html
- Hansen, L.P., Sargent, T.J. (2022). Structured ambiguity and model misspecification. *JET* 199:105165. https://doi.org/10.1016/j.jet.2020.105165
- Heitsch, H., Römisch, W. (2003). Scenario reduction algorithms in stochastic programming. *Comput. Optim. Appl.* 24(2–3):187–206. https://doi.org/10.1023/A:1021805924152
- Heitsch, H., Römisch, W. (2009). Scenario tree reduction for multistage stochastic programs. *Comput. Manag. Sci.* 6(2):117–133. https://doi.org/10.1007/s10287-008-0087-y
- Higham, N.J. (2002). Computing the nearest correlation matrix—a problem from finance. *IMA J. Numer. Anal.* 22(3):329–343. https://doi.org/10.1093/imanum/22.3.329
- Høyland, K., Wallace, S.W. (2001). Generating scenario trees for multistage decision problems. *Management Science* 47(2):295–307. https://ideas.repec.org/a/inm/ormnsc/v47y2001i2p295-307.html
- J.P. Morgan Asset Management (2025). *2026 Long-Term Capital Market Assumptions*, 30th ed. (estimates as of 30 Sep 2025), incl. USD assumption matrix; press release 20 Oct 2025. https://am.jpmorgan.com/us/en/asset-management/institutional/about-us/media/press-releases/jp-morgan-releases-2026-long-term-capital-market-assumptions/
- J.P. Morgan Asset Management (Oct 2026). *2027 Long-Term Capital Market Assumptions*, 31st ed. (estimates as of 30 Sep 2026). https://am.jpmorgan.com/us/en/asset-management/institutional/insights/portfolio-insights/ltcma/
- Klibanoff, P., Marinacci, M., Mukerji, S. (2005). A smooth model of decision making under ambiguity. *Econometrica* 73(6):1849–1892. https://ideas.repec.org/a/ecm/emetrp/v73y2005i6p1849-1892.html
- Kleywegt, A.J., Shapiro, A., Homem-de-Mello, T. (2002). The sample average approximation method for stochastic discrete optimization. *SIAM J. Optim.* 12(2):479–502. https://doi.org/10.1137/S1052623499363220
- Kritzman, M., Li, Y. (2010). Skulls, financial turbulence, and risk management. *FAJ* 66(5):30–41. https://doi.org/10.2469/faj.v66.n5.3
- Kritzman, M., Li, Y., Page, S., Rigobon, R. (2011). Principal components as a measure of systemic risk. *JPM* 37(4):112–126. https://doi.org/10.3905/jpm.2011.37.4.112
- Kuhn, D., Shafiee, S., Wiesemann, W. (2025). Distributionally robust optimization. *Acta Numerica* 34:579–804. https://doi.org/10.1017/S0962492924000084 ; arXiv:2411.02549. https://arxiv.org/abs/2411.02549
- Lange, R.T., Grillotti, L., Yamada, Y., Charakorn, R., Ha, D. (2026). The Agentic Scientist: Orchestrating coding agents for automated scientific (co-)discovery. arXiv:2610.18933. https://arxiv.org/abs/2610.18933
- Long, D.Z., Sim, M., Zhou, M. (2023). Robust satisficing. *OR* 71(1):61–82. https://ideas.repec.org/a/inm/oropre/v71y2023i1p61-82.html (preprint read: https://iora.nus.edu.sg/wp-content/uploads/2022/02/SSRN-id3478930.pdf)
- Maenhout, P.J. (2004). Robust portfolio rules and asset pricing. *RFS* 17(4):951–983. DOI 10.1093/rfs/hhh003. https://ideas.repec.org/a/oup/rfinst/v17y2004i4p951-983.html
- Mak, W.-K., Morton, D.P., Wood, R.K. (1999). Monte Carlo bounding techniques for determining solution quality in stochastic programs. *Oper. Res. Letters* 24(1–2):47–56. https://doi.org/10.1016/S0167-6377(98)00054-6
- Meucci, A. (2008). Fully flexible views: theory and practice. *Risk* 21(10):97–102. arXiv:1012.2848, via https://arxiv.org/abs/1012.2848 (pages from the arXiv journal reference; replaces the SSRN 1213325 link, which returned 403)
- Meucci, A. (2012). Effective number of scenarios in fully flexible probabilities. Record: https://consensus.app/papers/details/9602d72f6f065f43974fbfbb196c33bc/?utm_source=claude_desktop [unverified: venue, pages and DOI not confirmed; Crossref returns no record and OpenAlex search was rate-limited (HTTP 429)]
- Mohajerin Esfahani, P., Kuhn, D. (2018). Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. *Math. Programming* 171(1–2):115–166. https://doi.org/10.1007/s10107-017-1172-1 (preprint arXiv:1505.05116, https://arxiv.org/abs/1505.05116)
- NIST (2024). AI RMF: Generative AI Profile (NIST AI 600-1), 26 Jul 2024. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- Nystrup, P., Lindström, E., Madsen, H. (2020). Learning hidden Markov models with persistent states by penalizing jumps. *Expert Syst. Appl.* 150:113307. https://doi.org/10.1016/j.eswa.2020.113307
- Nystrup, P., Madsen, H., Lindström, E. (2018). Dynamic portfolio optimization across hidden market regimes. *Quant. Finance* 18(1):83–95. DOI 10.1080/14697688.2017.1342857. https://ideas.repec.org/a/taf/quantf/v18y2018i1p83-95.html
- O'Hagan, A., et al. (2006). *Uncertain Judgements: Eliciting Experts' Probabilities*. Wiley. https://doi.org/10.1002/0470033312
- Pástor, Ľ., Stambaugh, R.F. (2012). Are stocks really less volatile in the long run? *JF* 67(2):431–478. DOI 10.1111/j.1540-6261.2012.01722.x. https://ideas.repec.org/a/bla/jfinan/v67y2012i2p431-478.html
- Patton, A., Politis, D.N., White, H. (2009). Correction to "Automatic block-length selection for the dependent bootstrap" by D. Politis and H. White. *Econometric Reviews* 28(4):372–375. https://doi.org/10.1080/07474930802459016
- Pesenti, S.M., Millossovich, P., Tsanakas, A. (2019). Reverse sensitivity testing: what does it take to break the model? *EJOR* 274(2):654–670. https://ideas.repec.org/a/eee/ejores/v274y2019i2p654-670.html
- Pflug, G.Ch. (2001). Scenario tree generation for multiperiod financial optimization by optimal discretization. *Math. Programming* 89(2):251–271. https://doi.org/10.1007/pl00011398
- Pflug, G.Ch., Pichler, A., Wozabal, D. (2012). The 1/N investment strategy is optimal under high model ambiguity. *JBF* 36(2):410–417. DOI 10.1016/j.jbankfin.2011.07.018. https://ideas.repec.org/a/eee/jbfina/v36y2012i2p410-417.html
- Philpott, A.B., de Matos, V.L. (2012). Dynamic sampling algorithms for multi-stage stochastic programs with risk aversion. *EJOR* 218(2):470–483. https://ideas.repec.org/a/eee/ejores/v218y2012i2p470-483.html
- Politis, D.N., Romano, J.P. (1994). The stationary bootstrap. *JASA* 89(428):1303–1313. https://doi.org/10.1080/01621459.1994.10476870
- Politis, D.N., White, H. (2004). Automatic block-length selection for the dependent bootstrap. *Econometric Reviews* 23(1):53–70. DOI 10.1081/ETC-120028836. https://ideas.repec.org/a/taf/emetrv/v23y2004i1p53-70.html (see the Patton, Politis & White 2009 correction)
- Prudential Regulation Authority (2023; updated 23 Apr 2026). SS1/23 Model risk management principles for banks. https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss
- Rebonato, R., Denev, A. (2014). *Portfolio Management under Stress: A Bayesian-Net Approach to Coherent Asset Allocation*. Cambridge UP. https://doi.org/10.1017/CBO9781107256736
- Rockafellar, R.T., Uryasev, S. (2000). Optimization of conditional value-at-risk. *J. Risk* 2(3):21–41. https://doi.org/10.21314/JOR.2000.038
- Shu, Y., Yu, C., Mulvey, J.M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. *J. Asset Management* 25(5):493–507. https://doi.org/10.1057/s41260-024-00376-x (preprint arXiv:2402.05272, https://arxiv.org/abs/2402.05272)
- Smith, J.E., Winkler, R.L. (2006). The optimizer's curse: skepticism and postdecision surprise in decision analysis. *Management Science* 52(3):311–322. DOI 10.1287/mnsc.1050.0451. https://ideas.repec.org/a/inm/ormnsc/v52y2006i3p311-322.html
- Takahashi, D., Alexander, S. (2002). Illiquid alternative asset fund modeling. *JPM* 28(2):90–100. https://doi.org/10.3905/jpm.2002.319836
- Vanguard (22 Jul 2026; VCMM as of 30 Jun 2026). Vanguard economic and market outlook: return forecasts. https://corporate.vanguard.com/content/corporatesite/us/en/corp/vemo/vemo-return-forecasts.html
- Vorobets, A. fortitudo.tech (Entropy Pooling, CVaR), v1.2.5, GPL-3.0-or-later. https://pypi.org/project/fortitudo.tech/
- White, H. (2000). A reality check for data snooping. *Econometrica* 68(5):1097–1126. DOI 10.1111/1468-0262.00152. https://ideas.repec.org/a/ecm/emetrp/v68y2000i5p1097-1126.html
- Wiese, M., Knobloch, R., Korn, R., Kretschmer, P. (2020). Quant GANs: deep generation of financial time series. *Quant. Finance* 20(9):1419–1440. DOI 10.1080/14697688.2020.1730426. https://ideas.repec.org/a/taf/quantf/v20y2020i9p1419-1440.html
- Xie, W. (2021). On distributionally robust chance constrained programs with Wasserstein distance. *Math. Programming* 186(1–2):115–155. https://doi.org/10.1007/s10107-019-01445-5 (preprint arXiv:1806.07418, https://arxiv.org/abs/1806.07418)

## Citation corrections (2026-10-18)
Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.3–2.4; `research/literature/10_scenarios_robustness.lit.md` §1–2; `research/literature/recheck/10_scenarios_robustness.recheck.md`. New volume, issue and page details were re-confirmed on Crossref DOI records, and Meucci (2008) on arXiv.
- §1 #8: the Campi–Garatti count now gives the exact minimum (986) and states the convex-program requirement (verification #18, R9).
- §2.3: the Politis & White (2004) block-length citation now adds the Patton, Politis & White (2009) correction.
- §2.3: Buehler et al. (2020) is now Bühler et al. (2026; preprint 2020), and "data-hungry" now applies to GAN-type simulators only, because the paper is built for scarce data.
- §2.4: the Gao & Kleywegt and Xie in-text citations now carry their publication years (2023, 2021).
- §2.4: the Glasserman & Xu quotation is now verbatim ("very little computational effort beyond that required to evaluate performance under the baseline nominal model"; was "with little effort").
- §2.5: the Rebonato & Denev "unverified in session" flag is removed (book confirmed on Crossref), and the claim is tagged [S].
- §2.5: Meucci (2008) is verified via arXiv:1012.2848 (was "SSRN 1213325 returned 403, so unverified"), and the claim is tagged [S].
- §3: Heitsch & Römisch (2003) is limited to scenario sets (two-stage problems, evaluation sets); multistage decision trees now use Heitsch & Römisch (2009), which controls the filtration distance.
- §3: the Pflug (2001) "unverified in session" flag is removed (Crossref-confirmed), and the claim is tagged [S].
- §4.4: Campi–Garatti N is corrected to the exact minima 447 / 986 / 2,658 / 4,970 (was 448 / 989 / 2,662 / 4,976), and the convexity requirement is stated.
- §5: Lange et al. (2026) is reworded: reliable autonomy depends on the orchestration layer as well as on base-model capability (was "attribute reliable autonomy to the cross-agent orchestration layer"; verification #25).
- §6.2: the orphan references Kritzman & Li (2010) and Kritzman, Li, Page & Rigobon (2011) are now cited for the turbulence and absorption-ratio indicators of the deck's State/Fragility engine (engine composition per `inputs/00_CONTEXT_AND_PRIOR_WORK.md`, slide 4).
- §6.5: Carr & Wu (2009) is now cited only for the negative average variance risk premium [unverified: sign confirmed only by secondary literature], and "in calm regimes" is tagged [I].
- §6.7 table, optimisation-training row: now Heitsch–Römisch (2009) multistage tree reduction (was undated Heitsch–Römisch, i.e. the 2003 set method).
- §6.7 table, scenario-approach row: now ≥986 (about 1,000), convex scenario programs only (was ≥1,000).
- §6.7 table, future-node row: now "regression-based nested simulation (few inner draws per outer scenario)" (was "regression proxy, not nested"), matching Broadie, Du & Moallemi (2015).
- §6.10: the ENS diagnostic now cites its source, Meucci (2012).
- §7: block-length code should follow the Patton, Politis & White (2009) correction.
- §10, Bühler et al.: now the 2026 Springer chapter (*Stochastic Analysis and Applications 2025*, pp. 273–310, DOI 10.1007/978-3-032-03914-9_10), keeping arXiv:2006.14498 as the preprint.
- §10, Gao & Kleywegt: now *Math. of OR* 48(2):603–655 (2023), DOI 10.1287/moor.2022.1275 (was arXiv, "accepted").
- §10, Heitsch & Römisch (2009): added, *Comput. Manag. Sci.* 6(2):117–133, DOI 10.1007/s10287-008-0087-y.
- §10, Kuhn, Shafiee & Wiesemann: pages 579–804 and DOI 10.1017/S0962492924000084 added.
- §10, Meucci (2008): now *Risk* 21(10):97–102 via arXiv:1012.2848; the SSRN link and the "unverified" flag are removed.
- §10, Meucci (2012): added [unverified: venue, pages and DOI].
- §10, Mohajerin Esfahani & Kuhn: subtitle ": performance guarantees and tractable reformulations" restored; *Math. Programming* 171(1–2):115–166, DOI 10.1007/s10107-017-1172-1 (was "journal details not re-verified").
- §10, Patton, Politis & White (2009): added, *Econometric Reviews* 28(4):372–375, DOI 10.1080/07474930802459016.
- §10, Pflug (2001): issue and pages 89(2):251–271 and DOI 10.1007/pl00011398 added; the "unverified" flag is removed.
- §10, Rebonato & Denev: DOI 10.1017/CBO9781107256736 added; the "unverified" flag is removed.
- §10, Shu, Yu & Mulvey: now *J. Asset Management* 25(5):493–507, DOI 10.1057/s41260-024-00376-x, keeping the arXiv preprint.
- §10, Smith & Winkler: subtitle restored ("The optimizer's curse: skepticism and postdecision surprise in decision analysis"); DOI 10.1287/mnsc.1050.0451 added.
- §10, Xie: now *Math. Programming* 186(1–2):115–155 (2021), DOI 10.1007/s10107-019-01445-5, keeping the arXiv preprint.
- §10: Crossref-confirmed DOIs added to the 22 other entries that had only a RePEc link: Aas et al., Ang & Bekaert, Barillas et al., Barone-Adesi et al., Ben-Tal et al., Broadie et al., Campbell et al., Carr & Wu, Chen & Sim, Cont & da Fonseca, Delage & Ye, Gatheral & Jacquier, Getmansky et al., Gordy & Juneja, Hamilton, Maenhout, Nystrup et al. (2018), Pástor & Stambaugh, Pflug et al. (2012), Politis & White, White, Wiese et al.
