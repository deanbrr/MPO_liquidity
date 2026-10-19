# Verification log: Stream 10, scenario generation, regime models, robustness and probabilistic stress testing

**Dossier checked:** `research/dossiers/10_scenarios_robustness.md` (not edited).
**Verified:** 2026-10-18.
**Role:** adversarial fact-check before Investment Committee (IC) use.

---

## 1. Summary

**The sourced facts are accurate and no citation is hallucinated.**
- Every provider number I checked matches its primary source: J.P. Morgan 2026 and 2027, BlackRock (workbook cells), AQR (PDF exhibits), Vanguard and Bain 2026.
- So does every regulatory fact: SR 26-2 (including its footnote excluding generative and agentic AI), PRA SS1/23 and NIST AI 600-1.
- So does every attribution of a finding to a paper.
- The JPM 2026 correlation matrix is genuinely not PSD (minimum eigenvalue −0.0161; a Higham repair changes no entry by more than 0.0066).
- **Result: 26 claims checked. 22 confirmed, 4 corrected, 0 refuted, 0 unverifiable.**

**The derived analytics carry the real risk.** Four problems would change what the IC sees:

1. **The CMA ensemble mixes gross-of-fee and net-of-fee returns (§1 #2, #5; §4.2; §6.8 defaults; §8).**
   - BlackRock states: "The published returns are gross of fees and we net out representative client fees, accounting for management fees, carried interest, and hurdle rates, when creating and optimizing portfolios."
   - JPM's alternatives are "leveraged, net of fees" (2026 LTCMA, Exhibit 5). AQR's buyout figure is net of a 3.5% all-in fee.
   - The "11.4% (BlackRock)" upper end therefore overstates the BlackRock view. Illustrative haircuts give **≈9.2-10.2%** (centre 9.7%).
   - The headline ranges become:

     | Metric | Dossier | Fee-consistent |
     |---|---|---|
     | P(5y ≥ 10%) | 27-59% | **≈27-51%** |
     | P(5y < 7%) | 24-55% | **≈31-55%** |
     | Cross-provider KL vs JPM | 0.04-0.15 nats | **≈0.02-0.06 nats** |
     | Detection-error range | 18-38% | **≈25-38%** |
     | Mean dispersion across providers | "≈5pp" | **≈3-4pp** |

   - The η = 0.10 calibration argument and the "model dispersion is about 5pp" warning must be restated.
2. **The proposed replacement gate T1-L is itself a knife-edge (§6.9).**
   - It applies a KL-robust "≤1%" limit to rare liquidity breaches.
   - At η = 0.10, **a single failing path out of 50,000 gives a worst-case breach probability of 1.73%**, so the gate fails.
   - **Zero failing paths always pass**, because KL cannot put mass on outcomes that were never simulated.
   - Passing at η = 0.10 needs a nominal probability below 1.7×10⁻⁷.
   - This repeats the "infeasible / quietly relaxed gate" problem the dossier criticises in the prior deck. η_L must be set explicitly and small (about 0.01-0.02), with importance sampling.
3. **Wasserstein-1 worst-case threshold probabilities are mis-calibrated (§3, §6.8).**
   - ε is justified as "fee, smoothing and measurement bias", i.e. a roughly uniform shift.
   - The W1 worst case instead piles the transport budget onto atoms just above the threshold:

     | ε | W1 worst-case P(5y<7%) | P(5y<7%) after a uniform shift of ε |
     |---|---|---|
     | 0.25pp | 57.5% | ≈42.3% |
     | 0.5pp | 64.5% | ≈43.7% |
     | 1pp | 74.2% | ≈46.5% |

   - The IC reading "average return shift we cannot rule out" is misleading. Use W∞, which is exactly the uniform shift, for probabilities, and keep W1 for Lipschitz metrics (mean, CVaR).
4. **The effective-number-of-scenarios (ENS) diagnostics are redundant with KL (§6.8, §6.10, §7).**
   - With uniform nominal weights, ENS = N·exp(−KL) exactly.
   - So "ENS/N = 0.905 for the η = 0.10 tilt" is just e^{−0.10}. The ENS warn/block gates (0.10N, 0.02N) correspond to KL of 2.30 and 3.91 nats, so they can never fire before the 0.25-nat KL warning.
   - Detecting "domination by a few scenarios" needs Kish ESS (1/Σq²) or a maximum weight-ratio check.

**Smaller issues:**
- The §2.2 multiplier-robustness formula has the wrong sign.
- Leverage "through the overlay" scales the entire 60%-private book, so the leverage benefit is overstated.
- The SDDP / scenario-approach recommendations ignore the latent regime and the discrete SELL/HOLD/REFINANCE/LEVER actions.
- The return conventions inside §4.2 are inconsistent: the CMA table overstates P(5y<7%) by about 3pp against a consistent lognormal.
- The Campi-Garatti N values are 1-6 above the exact minima (sufficient, not minimal).

**Overall reliability: MEDIUM.**
- **High** for sourced facts and citations.
- **Medium-to-low** for the derived ensemble ranges (§1 #2, #5; §4.2), the T1-L gate design (§6.9) and the W1/ENS diagnostics (§6.8, §6.10).

Fix those before any IC pack.

---

## 2. Method

- **Search budget.** The session's shared web-search budget ran out mid-run (one search returned "budget used up"). The remaining checks used direct fetches of primary URLs: regulator pages, provider pages and files, RePEc, arXiv and the Crossref API.
- **PDFs and workbooks.**
  - Downloaded and text-extracted locally (pypdf; a standard-library xlsx reader): SR 26-2 attachment, AQR 2026 PDF, Bain GPER 2026 PDF, Long-Sim-Zhou SSRN preprint and the BlackRock CMA workbook.
  - Each file was copied into its own scratch folder.
- **JPM 2026 matrix.**
  - The JPM download links are JavaScript-gated. The USD matrix was therefore checked against the text of the JPM 2026 LTCMA full report (30th edition) already extracted in this session's shared scratchpad (`docs_jpm/ltcma_full.txt`).
  - Its headline numbers match the official JPM press release exactly.
  - I re-parsed the matrix with my own header-driven parser rather than reusing the author's. It found 59 assets and matched the author's arrays exactly.
- **Recomputations.** I re-ran independently:
  - Campi-Garatti N (binary search, cross-checked by log-space summation);
  - Monte Carlo SEs (400 replications, plus asymptotic VaR/ES formulas);
  - KL inversions, detection error and the Tier-1 gate;
  - the ensemble (author's convention, a consistent lognormal, and fee-adjusted BlackRock);
  - Higham nearest-correlation repair to convergence;
  - leverage via an ACWI-futures overlay.
- **Prototype code.** I also read the author's `proto_robust.py` and `cma_ensemble.py` to see exactly how each number was produced.

Script paths are listed in §6.

---

## 3. Claims table

| # | Claim (dossier §) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | JPM 2026 LTCMA (as of 30 Sep 2025, published 20 Oct 2025, compound, 10-15y): US LC 6.7% (σ16.47); ACWI 7.0% (σ16.78); EM 7.8%; US Agg 4.8%; cash 3.1%; US HY 6.1%; PE cap-weighted composite 10.2% (arith. 11.91, σ19.78); DL 7.7%; US core RE 8.2%; global core infra 6.5%; diversified HF 5.3%; US inflation 2.5%; 60/40 6.4% (6.9% with 30% alts); PE-ACWI 0.81; ACWI-US Agg +0.33 (§4.1) | **Confirmed** | Headline figures appear in the press release. Matrix values all match the 30th-edition USD matrix (59 assets): Agg, cash, DL, HF, inflation, vols, arithmetic returns and the correlations PE-ACWI 0.81, PE-US LC 0.75, ACWI-Agg 0.33. **Context the dossier omits:** JPM Exhibit 5 labels alternatives returns "leveraged, net of fees". | https://am.jpmorgan.com/us/en/asset-management/institutional/about-us/media/press-releases/jp-morgan-releases-2026-long-term-capital-market-assumptions/ |
| 2 | JPM 2027 LTCMA (31st ed., as of 30 Sep 2026): 60/40 7.0% (+60bp); 7.5% with alts; US LC 7.5% (+80bp); global agg 5.3%; large-cap PE median manager 9.6% (−60bp); diversified HF 6.7% (+140bp); global core RE 7.9%; global infra 7.1%; global inflation 2.6% (§4.1) | **Confirmed** | The 60/40-with-alts figure is +50bp. The −60bp comparator is 2026 large/mega-cap PE (10.2), not the composite. The ensemble substitutes global proxies (global agg for US Agg, global core RE for US core RE). | https://am.jpmorgan.com/us/en/asset-management/institutional/insights/portfolio-insights/ltcma/ |
| 3 | BlackRock CMAs (Aug 2026, data 30 Jun 2026, USD, 10y): US LC 8.97% (σ19.35, IQR 4.1-14.0); ACWI 9.02%; US buyout 15.89% (σ26.06, IQR 9.0-23.2); global 60/40 7.60%; US Agg 4.88%; cash 3.66%. Scenarios (US LC / PE): AI productivity boom 15.94% / 27.61%; global risk premia rise 2.02% / 9.36% (§4.1) | **Confirmed** (numbers) | All cells match the workbook: Starting point, AI productivity boom and Global risk premia rise sheets. 60/40 scenario values 8.06% / 6.37% also match. **Omitted caveat:** BlackRock says "published returns are gross of fees" (see #6). | https://www.blackrock.com/institutions/en-us/insights/charts/capital-market-assumptions |
| 4 | AQR 2026 CMAs (as of 31 Dec 2025, 5-10y local real): global 60/40 3.4%; US LC 3.9%; US buyouts 4.2%; US private credit 2.6%; US Agg 2.5%; 50% chance that realised 10-year equity returns miss by more than 3% p.a. (§4.1) | **Confirmed** | Exact text: "a 50% chance that realized equity market returns over the next 10 years will under- or overshoot our estimate by more than 3% per annum". The buyout figure is "net-of-fee" with a 3.5% all-in fee. Also checked: US 10y real 2.4%, US 10y inflation forecast 2.4% (the dossier's real-to-nominal add-on), US HY 2.7%. | https://www.aqr.com/Insights/Research/Alternative-Thinking/2026-Capital-Market-Assumptions-for-Major-Asset-Classes |
| 5 | Vanguard VCMM (as of 30 Jun 2026): 10y US equity 4.2-6.2%; developed ex-US 4.5-6.5% (§4.1) | **Confirmed** | The page is dated 22 Jul 2026. | https://corporate.vanguard.com/content/corporatesite/us/en/corp/vemo/vemo-return-forecasts.html |
| 6 | Own calculation: stylised 60%-private book returns 6.2% (AQR), 8.0% (JPM 2026/27), 11.4% (BlackRock); P(5y ≥ 10%) 27-59%; P(5y < 7%) 24-55%; 5y KL vs JPM 0.04-0.15 nats; AQR-BlackRock 0.35 (§1 #2, #5; §4.2) | **Corrected** | The arithmetic reproduces exactly under the author's conventions. However, the BlackRock member uses gross-of-fee private and HF returns plus gross levered DL (11.79%), against net-of-fee JPM and AQR. With illustrative haircuts (PE 2.5-4.5pp, centre = AQR's 3.5% all-in fee; DL 1.5-2.5; infra 1.5-2.5; HF 2-3; core RE 0.75-1.25), the BlackRock-based book is **9.19-10.15% (centre 9.67%)**. That gives **P(5y≥10%) ≈ 27-51%**, **P(5y<7%) ≈ 31-55%**, **KL vs JPM ≈ 0.02-0.06**, and **AQR-BlackRock ≈ 0.12-0.20**. Separately, the convention (weighted compound mean; σ_log = √ln(1+σ²)) overstates P(5y<7%). On a consistent lognormal, JPM 2026 gives **40.4% (not 43.8%)** and P(5y≥10%) **39.1% (not 37.5%)**. | https://www.blackrock.com/institutions/en-us/insights/charts/capital-market-assumptions |
| 7 | Own calculation: the deck's Tier-1 gate P(5y<7%) ≤ 5% needs an expected return of ≈16.6% given 5y σ ≈ 5.9%, so it is infeasible (§1 #3) | **Confirmed** (in substance) | The required centre is **15.8-17.9%** depending on convention. The 5y σ is 5.3% on a consistent lognormal (5.8% under the author's log-vol), not 5.9%; 16.6% corresponds to σ5 = 5.83%. The conclusion holds under the realised-return reading of the gate (see R6). | Own recomputation (§6) |
| 8 | Bain GPER 2026: buyout distributions/NAV ≈14% (12m to Q3 2025); below 15% for four years running (record); level last seen 2008-09; ~32,000 unsold companies worth $3.8tn; hold ≈7y at exit; CVs < 10% of PE exit value (§4.3) | **Confirmed** | Figure 19 note: buyout category, "2025 represents the 12-month period from Q4 2024 to Q3 2025", source MSCI. Also confirmed: secondaries +41% YoY; CVs +62% YoY; ~40% held >5y (29% in 2019); net cash flow "modestly above the breakeven line". | https://www.bain.com/insights/topics/global-private-equity-report/ |
| 9 | SR 26-2 (Fed/FDIC/OCC, 17 Apr 2026) supersedes SR 11-7 and SR 21-8; keeps effective challenge and validation (conceptual soundness, outcomes analysis, ongoing monitoring); excludes generative and agentic AI (§5) | **Confirmed** | Footnote 3: "Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance." Also confirmed: "most relevant" above $30bn; the model definition excludes simple arithmetic and deterministic rule-based processes. | https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm (attachment SR2602a1.pdf) |
| 10 | PRA SS1/23 (effective 17 May 2024) re-issued effective 23 Apr 2026 after low-impact amendments; five principles incl. independent validation (§5) | **Confirmed** | "Published 23 April 2026. Effective from 23 April 2026", following LIAF01/26 (Low Impact Amendments Finalisation). Five principles confirmed. | https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss |
| 11 | Long, Sim & Zhou (2023): κ_τ = min k s.t. E_P[f] − τ ≤ kΔ(P, P̂) ∀P; fragility ρ(v) = inf{k>0: kμ(v/k) ≤ 0}; under KL it relates to Aumann-Serrano riskiness (§2.4) | **Confirmed** | Eq. (6) with τ ≥ Z₀. Proposition 6 ("Risk-based Representation") uses SSRN-preprint numbering. The preprint states "Under the KL-divergence, the fragility measure relates to the riskiness index (Aumann and Serrano 2008)". Published OR 71(1):61-82 confirmed; published proposition numbering not checked. | https://ideas.repec.org/a/inm/oropre/v71y2023i1p61-82.html |
| 12 | Aumann-Serrano riskiness of a normal gamble = variance/(2·mean); prototype k* = 0.153 matched it (0.152) (§2.4, §6.8) | **Confirmed** | The abstract says that for normally distributed gambles the index "equals half of variance divided by mean". Recomputed s²/(2m) = 0.0049/0.0322 = 0.1522. | https://ideas.repec.org/a/ucp/jpolec/v116y2008i5p810-836.html |
| 13 | Guidolin & Timmermann (2007): four regimes (crash, slow growth, bull, recovery); ignoring regimes has substantial welfare costs (§2.3) | **Confirmed** | "Welfare costs from ignoring regime switching can be substantial even after accounting for parameter uncertainty." | https://ideas.repec.org/a/eee/dyncon/v31y2007i11p3503-3544.html |
| 14 | Ang & Bekaert (2002): bear regimes have higher vol and higher cross-market correlation (§2.3) | **Confirmed** | Correlations "tend to increase in highly volatile bear markets". The cost of ignoring regimes is small for all-equity portfolios and larger when a conditionally risk-free asset exists. | https://ideas.repec.org/a/oup/rfinst/v15y2002i4p1137-1187.html |
| 15 | Pástor & Stambaugh (2012): with parameter uncertainty and imperfect predictors, stocks are more volatile per year over long horizons, which offsets mean reversion (§2.3) | **Confirmed** | | https://ideas.repec.org/a/bla/jfinan/v67y2012i2p431-478.html |
| 16 | Breuer & Csiszár (2013): maximum-loss theorem gives the worst-case distribution in a relative-entropy ball. Glasserman & Xu (2014): worst-case model error computable from baseline MC "with little effort" (§2.4, §2.5) | **Confirmed** | GX's actual wording is "very little computational effort beyond that required to evaluate performance under the baseline nominal model"; the dossier's quotation is a slight misquote. | https://ideas.repec.org/a/eee/jbfina/v37y2013i5p1552-1559.html ; https://ideas.repec.org/a/taf/quantf/v14y2014i1p29-58.html |
| 17 | Own simulation (1y loss, t₅, 13% vol, 50k paths): SE(VaR99) ≈ 0.40pp; SE(ES99) ≈ 0.82pp; SE of a 5% probability ≈ 0.10pp; asymptotic quantile SE confirmed (§4.4) | **Confirmed** | Independent run: true VaR99 25.9%. SE(VaR99) 0.41pp (asymptotic) / 0.42pp (simulated); SE(ES99) 0.77pp / 0.82pp; binomial 0.097pp; path counts 7,300 / 12,048 / 38,032 exact. Minor: the 10k-row VaR SE of 1.05pp is high against 0.92pp (asymptotic) / 0.94pp (simulated). | Own recomputation (§6) |
| 18 | Campi-Garatti exact bound: N ≥ 989 for d=30, ε=5%, β=10⁻³; N ≥ 2,662 for d=100; also 448 (d=10) and 4,976 (ε=1%) (§1 #8, §4.4, §6.7) | **Corrected** (minor) | Exact minimal N: **986** (d=30), **2,658** (d=100), **447** (d=10), **4,970** (d=30, ε=1%). The dossier's values are sufficient but not minimal; the prototype's search step was Nn//200. The guarantee also requires a **convex** scenario program (see R9). | https://doi.org/10.1137/07069821X |
| 19 | The JPM 2026 USD correlation matrix is not PSD (min eigenvalue −0.016); Higham repair changes no entry by more than 0.007 (§4.1) | **Confirmed** | Independent parse: 59×59, minimum eigenvalue −0.0161, 5 negative eigenvalues. Higham alternating projections run to convergence: maximum entry change 0.0066 (Frobenius 0.022). | https://doi.org/10.1093/imanum/22.3.329 |
| 20 | JPM 2026: ≈1,960bp top-vs-bottom-decile PE manager dispersion vs ≈200bp in public equity (§4.1, §6.3) | **Confirmed** | "public equity has approximately 200bps ... private equity has exhibited 1,960bps of dispersion." | JPM 2026 LTCMA full report (see #1) |
| 21 | JPM 2026: "place more weight on scenarios of inflation and rate volatility to complement growth shock scenarios"; relationships "changing – and unstable" (§4.1) | **Confirmed** | Verbatim. | JPM 2026 LTCMA full report (see #1) |
| 22 | Campbell, Chan & Viceira (2003): predictability "greatly increases" optimal stock demand (§2.3) | **Confirmed** | Verbatim in the abstract. | https://ideas.repec.org/a/eee/jfinec/v67y2003i1p41-80.html |
| 23 | Shu, Yu & Mulvey (2024): jump models more persistent and practical than HMMs out of sample, 1990-2023 (§2.3) | **Confirmed** | US, German and Japanese indices, with costs and delays. Published in J. Asset Management (DOI 10.1057/s41260-024-00376-x). | https://arxiv.org/abs/2402.05272 |
| 24 | Pesenti, Millossovich & Tsanakas (2019): minimum-KL measure producing a stressed VaR/ES; one baseline simulation suffices (§2.5) | **Confirmed** | "Can be performed on a single set of input/output scenarios, simulated under the baseline model." | https://ideas.repec.org/a/eee/ejores/v274y2019i2p654-670.html |
| 25 | Lange et al. (arXiv:2610.18933): meta-controller with rubric verification at each stage; "its ablations attribute reliable autonomy to the cross-agent orchestration layer" (§5) | **Corrected** (wording) | The abstract says reliable autonomy depends "not only on base model capabilities" but also on the orchestration layer. The two act jointly; orchestration is not credited alone. | https://arxiv.org/abs/2610.18933 |
| 26 | With 20 years of returns, the chance of picking the wrong provider is about 18-38% (§1 #5, §4.2) | **Corrected** | The arithmetic is right (37.8% and 18.3%). But the 18% uses the gross-of-fee BlackRock mean. With a fee-consistent BlackRock (9.2-10.2%), the BlackRock-AQR error is **≈25-30%**, so the range is **≈25-38%**. "Undetectable for decades" overstates it: 62-82% of samples are classified correctly at 20 years. | Own recomputation (§6) |

---

## 4. Citation check

The 10 most load-bearing references, plus others checked opportunistically:

| Reference | Exists? | Authors/year/title/venue correct? | Note |
|---|---|---|---|
| Long, Sim & Zhou (2023), *Robust satisficing*, OR 71(1):61-82 | Yes | Yes | DOI 10.1287/opre.2021.2238 |
| Aumann & Serrano (2008), *An economic index of riskiness*, JPE 116(5):810-836 | Yes | Yes | DOI 10.1086/591947 |
| Hansen & Sargent (2022), *Structured ambiguity and model misspecification*, JET 199 | Yes | Yes | DOI 10.1016/j.jet.2020.105165 |
| Breuer & Csiszár (2013), JBF 37(5):1552-1559 | Yes | Yes | |
| Glasserman & Xu (2014), *Robust risk measurement and model risk*, QF 14(1):29-58 | Yes | Yes | Quoted phrase slightly altered (see #16) |
| Guidolin & Timmermann (2007), JEDC 31(11):3503-3544 | Yes | Yes | |
| Ang & Bekaert (2002), RFS 15(4):1137-1187 | Yes | Yes | |
| Pástor & Stambaugh (2012), JF 67(2):431-478 | Yes | Yes | |
| Campi & Garatti (2008), *The exact feasibility of randomized solutions of uncertain convex programs*, SIAM J. Optim. 19(3):1211-1230 | Yes | Yes | Crossref |
| Higham (2002), *Computing the nearest correlation matrix*, IMA J. Numer. Anal. 22(3):329-343 | Yes | Yes | Crossref |
| Pesenti, Millossovich & Tsanakas (2019), EJOR 274(2):654-670 | Yes | Yes | |
| Glasserman, Kang & Kang (2015), QF 15(1):25-41 | Yes | Yes | |
| Campbell, Chan & Viceira (2003), JFE 67(1):41-80 | Yes | Yes | |
| Kuhn, Shafiee & Wiesemann (2025), *Distributionally robust optimization*, Acta Numerica 34 | Yes | Yes | Pages 579-804 omitted |
| Lange, Grillotti, Yamada, Charakorn, Ha (2026), arXiv:2610.18933 | Yes | Yes | Submitted 13 Oct 2026 |
| Shu, Yu & Mulvey (2024), arXiv:2402.05272 | Yes | Yes | Cited as arXiv only; published version exists |
| Mohajerin Esfahani & Kuhn (2018), arXiv:1505.05116 | Yes | Title truncated | Full title adds ": Performance guarantees and tractable reformulations". Journal details not verified (the dossier flags this). |
| Gao & Kleywegt, arXiv:1604.02199 | Yes | Yes | arXiv comment "Accepted by Mathematics of Operations Research"; final citation not given |
| NIST AI 600-1 (26 Jul 2024) | Yes | Yes | |
| fortitudo.tech v1.2.5 (20 Aug 2026), GPL-3.0-or-later, SeqEP | Yes | Yes | PyPI author "Fortitudo Technologies" (maintainer antonvorobets) |
| Meucci (2008), *Fully flexible views*, Risk 21(10) | Not verifiable in session | n/a | SSRN returned 403 again. A well-known reference, low risk. |
| Rebonato & Denev (2014, CUP); Pflug (2001, Math. Prog. 89) | Not re-checked | n/a | Already marked unverified in the dossier |

**No hallucinated or garbled citations were found.** The issues are minor: one truncated title, missing page or venue details, one altered quotation, and one paraphrase that overstates (Lange et al.).

**Erratum (2026-10-18).** The later literature audit (`research/literature/10_scenarios_robustness.lit.md` §1–2; `research/literature/recheck/10_scenarios_robustness.recheck.md`) shows that this log accepted two items it should have flagged: Gao & Kleywegt's metadata, although the paper was published as *Math. of OR* 48(2):603–655 (2023), DOI 10.1287/moor.2022.1275; and claim #16, whose Glasserman–Xu quotation is not verbatim, so #16 should read "Corrected (wording)" (tally: 21 confirmed, 5 corrected). The §1 statement that every attribution checks out covers only the claims tested here: the audit found Heitsch & Römisch (2003) applied to multistage trees, the ENS source Meucci (2012) uncited, and Buehler et al., Carr & Wu and Broadie, Du & Moallemi misdescribed; all are corrected in the dossier.

---

## 5. Reasoning issues and overclaims (most severe first)

**R1 (High). The ensemble is not like-for-like on fees (§1 #2, #5; §4.2; §6.6; §6.8 defaults; §8).**
- The fee bases differ:
  - BlackRock: "The published returns are gross of fees …" (CMA page).
  - JPM: "LTCMA expected returns (leveraged, net of fees, %)" (2026 Exhibit 5).
  - AQR: "an expected net-of-fee return for U.S. buyout funds" with "all-in fee estimate … 3.5%".
- The BlackRock member also uses the gross levered DL (11.79%) rather than the 9.31% unlevered figure.
- The workbook's SAA notes add: "For assets without indices (private markets), we have assumed top-quartile performance." This applies at least to its SAA illustrations.
- Effects:
  - the upper end of the "model uncertainty" range is overstated by about 1.3-2.2pp;
  - the cross-provider KL used to justify η = 0.10 shrinks to about 0.02-0.06 nats;
  - the "≈5pp dispersion" becomes about 3-4pp.
- Fix:
  - put every provider on the same net-of-fee, same-leverage basis before ensembling (BlackRock publishes fee assumptions on its methodology tab);
  - document the haircut;
  - re-derive the η defaults.

**R2 (High). The T1-L KL-robust rare-event chance constraints are knife-edge and cannot be checked by simulation (§6.9).**
- The table gives the largest nominal breach probability that keeps the KL worst case ≤ 1%:

  | η_L | Max nominal p | Paths of 50k |
  |---|---|---|
  | 0.10 | 1.7×10⁻⁷ | ≈0 |
  | 0.05 | 2.5×10⁻⁵ | ≈1 |
  | 0.02 | 5.3×10⁻⁴ | ≈26 |
  | 0.01 | 1.6×10⁻³ | ≈80 |

- At η = 0.10, one failing path out of 50k gives a worst case of 1.73% (gate fails). Zero failing paths give 0 (gate passes), because KL is support-blind.
- The gate outcome is therefore driven by Monte Carlo noise. That is the same "infeasible or quietly relaxed gate" failure the dossier attributes to the deck.
- Fix:
  - specify η_L explicitly and small (about 0.01-0.02);
  - use importance sampling toward crisis and illiquidity regimes;
  - gate on an upper confidence bound of the nominal probability plus named structural stresses;
  - or use a likelihood-ratio cap or a Wasserstein ball on the buffer level, which can create new failures.

**R3 (Medium-High). W1 worst-case threshold probabilities do not match their stated calibration (§3 table, §6.8 defaults, §6.9 IC card).**
- An indicator is not Lipschitz. The W1 worst case concentrates transport on atoms just above τ, giving 57.5 / 64.5 / 74.2% at ε = 0.25 / 0.5 / 1pp.
- A uniform bias of the same size gives about 42.3 / 43.7 / 46.5% (normal approximation to the prototype outcome: mean 8.61%, sd 7%).
- Labelling ε as "fee, smoothing and measurement bias" and calling it "average return shift we cannot rule out" will mislead the IC by about 15-28pp.
- Fix: for probabilities use W∞ (worst case = P(y < τ + ε)) or a smoothed indicator. Keep W1 only for Lipschitz functionals, where R5's closed forms (mean − ε, CVaR + ε/α) are correct.

**R4 (Medium). ENS adds nothing when nominal weights are uniform (§6.8 prototype, §6.10 gates, §7 pitfalls).**
- With ENS = exp(−Σq ln q) and uniform weights, ENS/N = exp(−KL(q‖p)) exactly.
- So 0.905 = e^{−0.10}, and the EP prototype's 0.91 = e^{−0.091}.
- The warn/block thresholds (0.10N / 0.02N) correspond to KL of 2.30 / 3.91 nats, so they can never bind under the KL budgets used (≤ 0.25).
- The stated aim ("KL tilts on heavy-tailed losses are dominated by a few scenarios") needs Kish ESS = 1/Σq², max q_i/p_i, or tail-ESS.

**R5 (Medium). Leverage "through the overlay" is modelled as pro-rata scaling of the whole 60%-private book at cash+50bp (§4.2).**
- That implicitly earns the PE and VC premia through derivatives, which an OTC overlay cannot do.
- Adding ACWI futures instead (JPM 2026 risk):

  | Leverage | Geometric return | Vol | P(5y≥10%) | P(5y<7%) |
  |---|---|---|---|---|
  | 1.15x, dossier | 8.99% | 15.0% | 44.0% | 38.1% |
  | 1.15x, ACWI futures | 8.80% | 15.4% | 43.0% | 39.4% |
  | 1.30x, dossier | 9.55% | 17.0% | 47.6% | 36.5% |
  | 1.30x, ACWI futures | 9.17% | 17.8% | 45.8% | 39.0% |

- With ACWI futures, leverage barely moves P(5y<7%) (unlevered: 40.4%). It mainly widens the distribution, which is the more useful message for the IC.

**R6 (Medium). Tier-1 infeasibility depends on an unstated reading (§1 #3, §6.9).**
- The deck's gate ("plausible model misspecification … at most 5% breach probability under misspecification") can be read two ways:
  - (a) P(realised R5 < 7%) ≤ 5% under the worst-case model, which needs a centre of about 16-18% and is infeasible;
  - (b) a model-uncertainty probability that E[R5] < 7%, which is feasible.
- The dossier assumes (a), while its own replacement T1-F effectively adopts (b).
- Fix: state the interpretation. Use σ5 ≈ 5.3% (consistent lognormal), not 5.9%.

**R7 (Medium). The return conventions inside §4.2 are inconsistent.**
- The CMA table uses the weighted compound mean (7.98%). That ignores about 0.41pp of diversification return, and σ_log = √ln(1+σ²) omits the (1+m)² term (0.130 vs 0.119).
- The leverage table uses the consistent lognormal (8.39%).
- Result: the CMA table overstates P(5y<7%) by about 3pp (JPM: 43.8% vs 40.4%) and understates P(5y≥10%) (37.5% vs 39.1%).

**R8 (Medium). The structured ambiguity set understates provider disagreement on risk and mixes definitions (§4.2, §6.6).**
- JPM risk is used for every provider. BlackRock's own vols are higher: US buyout 26.06% vs JPM PE 19.78%; US LC 19.35% vs 16.47%.
- Members mix definitions:
  - JPM 2027 uses global agg for US Agg, global core RE for US core RE, and large-cap median-manager PE for the composite;
  - AQR uses developed-market local-real equity as ACWI USD nominal;
  - BlackRock uses levered gross DL.
- Mean-only KL therefore understates structured ambiguity in tail metrics.

**R9 (Medium). The SDDP "maps one-to-one" claim and scenario-approach certificates assume conditions ADIC lacks (§3, §6.7).**
- Campi-Garatti requires a convex scenario program.
- SDDP on a Markovian policy graph requires convex cost-to-go and an observed Markov state.
- The ESG regime is latent (filtered probabilities), and SELL/HOLD/REFINANCE/LEVER are discrete.
- This needs either integer-capable cuts (SDDiP / Lagrangian cuts) or partially observable SDDP over the belief state, or the regime must be treated as observed (look-ahead).
- So "best fit for ADIC" is an overclaim until these are addressed. (Literature pointers are not fetched in this session: Zou, Ahmed & Sun 2019, Math. Prog.; Dowson, Morton & Pagnoncelli 2020, ORL.)

**R10 (Low-Medium). Sign error in the §2.2 multiplier-robustness formula.**
- The dossier writes "min_q E_q[ℓ] + θ KL(q‖p)" with ℓ a loss. That is the optimistic tilt q ∝ p e^{−ℓ/θ}.
- The robust version is max_q E_q[ℓ] − θ KL(q‖p) = θ ln E_p[e^{ℓ/θ}], with q ∝ p e^{ℓ/θ}. Equivalently, min_q E_q[u] + θ KL for a utility u.
- Fix before it reaches code.

**R11 (Low). The breakdown-divergence translation is tautological (§6.8).**
- For a Gaussian, σ_y √(2η*) equals E[y] − τ by construction. So "η* = 0.027 nats, i.e. a 1.6pp mean shift" just restates 8.61% − 7%.
- The comparison with the "1.8pp JPM-AQR gap" also mixes statistics: the mean of the 5-year annualised return against a difference of weighted compound means.

**R12 (Low). Further minor points.**
- "Statistically undetectable for decades" overstates (see #26).
- The η = 0.10 value is the author's, not Hansen & Sargent's; the citation supports the structure only.
- A full covariance per regime with K = 4 and about 20 factors is 840 parameters, not "about 600".
- R4's greedy W1 formula assumes equal weights. After view tilts, q must enter.
- The prototype "regime mixture" draws regimes i.i.d. across years (no persistence), so it understates 5-year dispersion relative to the recommended semi-Markov ESG. The §6.8 robust numbers are therefore illustrative only.
- The log-linear confidence blend p^{1−c} q^c departs from Meucci's linear blend. It does not hit a view at fraction c.

**What checked out (no change needed):**
- R1: exact via the data-processing inequality.
- R2: Donsker-Varadhan dual.
- R3: CVaR-KL with Sion's minimax and joint convexity.
- R4 greedy formula (equal weights).
- R5 closed forms (W1 on the scalar outcome).
- R6 and R7 forms; the R7 normal approximation k* = σ²/(2(τ − μ)).
- The EP dual in §6.10.
- Ergodic mean matching in §6.6 (the new mean equals m^CMA exactly).
- Memory estimate (50k × 120 × 25 float32 ≈ 0.6 GB).

---

## 6. Recomputation record

Scripts are in this session's scratchpad (`C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\scripts\`):
- `jpm_parse_check.py`: header-driven parse of the JPM 2026 USD matrix. 59 assets, minimum eigenvalue −0.0161; identical to the author's arrays.
- `verify10.py`:
  - Higham repair (max change 0.0066);
  - portfolio: arithmetic 9.17%, vol 13.08%, geometric 8.39%; P(10y ≥ 10%) 34.8%;
  - ensemble in three conventions;
  - Tier-1 gate;
  - detection error (37.8% / 18.3%);
  - KL inversions (47.6 / 56.3 / 62.8 / 71.9%);
  - ENS identity;
  - normal-model consistency: worst mean 5.48%, η* 0.0264, k* 0.1522;
  - uniform shift vs W1;
  - exact Campi-Garatti N;
  - MC standard errors.
- `blk_rows.py`, `xlsx_dump.py`: BlackRock workbook extraction (Starting point and scenario sheets).
- `pdf_grep.py`: text extraction for SR 26-2, AQR, Bain and LSZ.

**Fee-adjusted BlackRock (author's convention, JPM 2026 risk):**

| Haircut set | Book mean | P(5y≥10%) | P(5y<7%) | KL vs JPM | KL vs AQR |
|---|---|---|---|---|---|
| As published (gross) | 11.43% | 58.8% | 24.3% | 0.145 | 0.345 |
| Low (PE 2.5pp) | 10.15% | 50.9% | 30.9% | 0.058 | 0.200 |
| Mid (PE 3.5pp) | 9.67% | 47.9% | 33.6% | 0.035 | 0.155 |
| High (PE 4.5pp) | 9.19% | 44.9% | 36.4% | 0.018 | 0.116 |

---

## 7. Overall reliability rating and edits required before IC use

**MEDIUM.** The empirical base is strong: all provider, regulatory, Bain and paper-attribution claims verify, and no citations are fabricated. Several derived headline numbers and two design gates need correction.

**Required edits:**
1. Put the CMA ensemble on a common net-of-fee, same-leverage basis, then restate §1 #2, #3 and #5, the §4.2 table, the §6.8 η justification and §8 (R1, #6, #26).
2. Specify η_L for T1-L. Show it is checkable at the planned path count with importance sampling, or replace it with UCB-plus-stress gating (R2).
3. Replace W1 threshold probabilities with W∞ (uniform-shift) probabilities, or relabel them as concentrated-transport worst cases (R3).
4. Replace exp-entropy ENS gates with Kish ESS or maximum-weight diagnostics (R4).
5. Fix the multiplier sign (R10), the overlay-leverage specification (R5), the Tier-1 interpretation statement (R6) and the convention consistency (R7).
6. Qualify the SDDP and scenario-approach claims for latent regimes and discrete actions (R9). Update Campi-Garatti N to the exact minima (#18).

## Citation corrections (2026-10-18)
- §4: added one erratum line after the citation-check conclusion (Gao & Kleywegt metadata and claim #16 wrongly accepted; the §1 attribution statement limited to the claims tested). No verdict, table or number elsewhere in this log was changed.
- Cross-reference (no change here): the dossier now applies this log's #16 (verbatim Glasserman–Xu quote), #18 and R9 (exact Campi–Garatti minima, convexity requirement) and #25 (Lange wording), and resolves the §4 items left open here (Meucci 2008, Pflug 2001, Rebonato & Denev 2014, Mohajerin Esfahani & Kuhn, Gao & Kleywegt, Shu, Yu & Mulvey, Kuhn et al. pages); see the dossier's own "Citation corrections (2026-10-18)" section. The scenario-approach convexity caveat is stated there, but the SDDP latent-regime part of R9 and the other required edits in §7 are not citation corrections and remain open.
