# G4 — Co-investment group: direct minority co-investments alongside GPs

*ADIC multi-period robust TPA framework. Group research dossier, as of 2026-10-18.*

- **Scope:** ADIC's Co-investment group (working NAV ≈ US$18bn, synthetic allocation in context §1A). It makes deal-by-deal minority equity co-investments alongside lead GPs.
- **Evidence tags:** **[S]** sourced fact (citation in §10). **[P]** practitioner consensus. **[I]** my inference, model output or design choice. **‡** marks figures seen only in a search-engine summary because the primary page was paywalled or blocked. Treat them as unverified.
- **Reproducibility:** every model number tagged [I] comes from `research/groups/verification/G4_coinvest_calcs.py`. The script is seeded and writes `G4_coinvest_calcs_results.json`. The exception is the §6.3 book-simulation cells marked †: they were re-run on 2026-10-18 with the corrected write-off barrier by `research/groups/addenda/G4_barrier_rerun/G4_coinvest_calcs_bgk.py` (see `RESULTS.md` in that folder). **All model outputs are synthetic** and are not ADIC data.
- **Limitations of this pass:**
  - The shared WebSearch budget ran out twice. I worked from primary PDFs (text-extracted locally) and from sibling-dossier URLs that I re-fetched myself.
  - The Consensus connector exposed only authentication tools, so it was not used.
- **Sibling dossiers used, not duplicated:**
  - 04: PE cash flows, regimes, exits, IPO window
  - 05: secondaries and NAV finance
  - 06: leverage
  - 07: return fusion
  - 08: action valuation

---

## 1. Executive summary

**What the group is.** ADIC writes minority equity tickets into companies that GPs control. The co-investment is usually funded about 100% at close and sits beside the GP's fund. It exits when the GP exits ("in together, out together"). Fees are low or zero. The three things that matter for ADIC are selection, diversification and control. Each is mostly settled by evidence, and each drives a specific design choice.

**1. Selection is not the main problem; timing and size are.**
- Braun, Jenkinson & Schemmerl (BJS 2020) study 1,016 co-investments in 464 funds (13,430 deals) [S]:
  - They find no adverse selection on gross returns. Buyout co-investments have a mean gross PME of 1.76, against 1.70 for the funds' other deals.
  - The main driver of whether a deal is offered for co-investment is its size relative to the fund.
- Fang, Ivashina & Lerner (FIL 2015) report the opposite in data from seven large LPs [S]:
  - Capital-weighted co-investment IRR was **−0.09%** (TVPI 1.20), against 16.8% for the same LPs' solo deals.
  - The underperformance was concentrated in 2006–08 deals, when co-investment volume peaked; co-investment TVPI was 1.18, 1.10 and 0.78 for those years. TVPI has a correlation of −0.59 with industry fund commitments.
  - Co-invested deals averaged an enterprise value of $2.7bn, nearly 3× the same GP's median deal.
- Lerner, Mao, Schoar & Zhang (2022) add a third finding [S]:
  - Alternative vehicles match the PE market on average but trail the sponsor's main fund.
  - Top LPs get preferential access to the best vehicles.
- **Reading for ADIC [I]:** the failure mode is buying large deals in hot vintages, not being sold lemons. Pacing and size discipline are the controls.

**2. Deal outcomes are extremely skewed** [S: BJS Table 4]. For buyout co-investments:
- gross PME at the 25th percentile is 0.26, the median 1.16, the 75th percentile 2.45 and the 99th 8.43;
- the standard deviation is 2.10 and the skewness 2.50;
- only 35% of buyout deals beat their own fund's return.
- Separately, about 1 in 10 PE investments returns no money [S: Lopez-de-Silanes et al.].

**3. A levered-equity structural model reproduces this distribution [I].**
- Equity is modelled as a call on enterprise value: $M=\max(G-L,0)/(1-L)$, with lognormal EV growth $G$.
- The fit uses historical debt/EV $L=0.60$, σ≈0.60 over the hold (≈0.28 a year), rare upside jumps and a distress-recovery floor. It matches the BJS quartiles, the mean (1.73 against 1.76) and the ~10% zero-return share.
- In this model, $P(M<1)\approx46\%$ does not depend on leverage. Leverage sets only the depth of losses and the size of the upside.

**4. Re-base the reference class to today's capital structures [I].**
- Today's buyouts carry about 36% debt/EV, enter at about 14× and pay 8–9% for debt [S: Bain 2026].
- Running the historical EV process at $L=0.40$:
  - the expected PME multiple falls from 1.73 to **1.45**, or 1.30 if multiples compress from 14× to 13×;
  - the probability of near-total loss falls from 10% to 4–5%.
- Underwriting must be judged against this re-based class, not against historical co-investment averages.

**5. Diversify across vintages more than across deals [I].**
- With independent deals:
  - P(portfolio multiple <1) is 46% for one deal, 9.8% for 10 and 2.7% for 20.
  - This matches the BJS bootstrap: the median rises from 1.16 for one deal to 1.48 for five and 1.63 for ten.
- Add a modest common factor (ρ = 0.1–0.2 in log-EV space) and P(<1) stalls at **8–18% even with 100 deals**.
- Spreading 60 deals over eight vintages instead of one cuts P(<1) from 22% to 6%.
- Practitioner evidence agrees: in HarbourVest's simulation, P(<1.5×) is 24% with six companies and 3% with fifty‡.

**6. Fees.**
- "No fee, no carry" is still the norm [S: Sidley 2025]:
  - about two-thirds of managers charge no management fee;
  - more than half charge no carry;
  - fewer than 7% of deals propose economics (Investment Officer 2026).
- Hidden costs are material: monitoring fees of 1–2% of commitment a year, transaction fees of 0.5–3% of EV, broken-deal costs in about 20% of deals, and no fee offsets [S: Torys 2026].
- Deal-by-deal carry acts like a strip of call options with no netting [I]:
  - 0/20 deal-by-deal costs about 18% more expected carry than the same terms pooled.
  - Its "IRR of the mean" is 16.4%, against 16.1% for a pooled 2/20 fund and 19.9% for 0/0.
  - On these assumptions, **0/20 co-investments are about as expensive as a fund**.

**7. Cash flows: funded at close, exits on the GP's clock.**
- A Weibull exit hazard fitted to Kaplan & Strömberg gives k = 1.45 and η = 7.7 years, a median of about 6 years [I]. A drought (hazard × 0.5) halves the book's annual exit fraction, from 13.5% to 7.0%.
- Dividend recaps are the main interim cash channel: about $74bn of sponsored recap loans in 2025, adding about one turn of leverage [S]. Recaps that raise total debt by 84% on average increase the chance of financial distress by 2.4 times the target-firm mean [S: Bhardwaj, Gupta & Howell; IV estimate, an increment; OLS ≈0.4 times]. For E5's smaller recaps (φ = 0.25), linear scaling gives a hazard multiplier of about ×1.1 (OLS) to ×1.7 (IV) [I] [corrected 2026-10-18: was "raise distress probability 2.4× its mean"; the 2.4 belongs to the +84% debt increase].
- The synthetic $18bn book simulation [I] shows a year-1 distribution yield of 12.4% of NAV from a drought start and 19.3% from a normal start. 3-year net cash flow averages +$3.4bn, with a 10th percentile of −$1.3bn.

**8. SELL / HOLD / REFINANCE / LEVER.**
- **SELL.** Demand for single assets is deep at the top: about 87% of single-asset CV volume priced above 90% of NAV in H1-2026 [S: Lazard], and buyers underwrite to about 2.3× gross over four years [S: Evercore]. LPs strip-sold large co-investments, including one sale above $1bn [S: Jefferies].
- **Worked example [I].** At a 95% bid, selling a good asset needs a 5.8% liquidity premium in normal conditions. In a drought it wins outright, because the PV of holding falls to 91.5% of NAV.
- **REFINANCE.** Company recaps are the GP's decision. ADIC's own lever is a pool facility at about 15% LTV and about 11% all-in [I]. On a single asset it carries a 29–37% chance of breaching the covenant trigger.
- **LEVER.** A 12% holdco PIK on an asset expected to return about 9% adds no expected return. It doubles wipe-out risk in a drought, from 12% to 23%.

**9. Cross-group links [S/I].**
- Co-investment deal flow depends on PE primary commitments. GPs offered a median of 33¢ of co-investment per $1 of fee-bearing capital, with a range of 0–110¢ [S: Bain 2026]. Cutting primary commitments therefore cuts co-investment flow 1–5 years later.
- Dividend recaps financed by private credit move value from ADIC's credit exposure to its equity exposure. ADIC must net these on a look-through basis.

**Build:**
- a deal-level jump-diffusion engine with competing-risk exits, recaps and smoothed GP marks (Specification Card, §6.10);
- deal-level belief fusion against the re-based reference class, with "what you need to believe" diagnostics;
- vintage, GP and size budgets;
- SELL, REFI and LEVER operators priced with the dual-price score from dossier 08.

---

## 2. Core concepts and theory

### 2.1 The instrument and its rights [P/S]
A co-investment is a minority stake taken next to a GP's fund, usually through a GP-managed co-investment vehicle or a direct holding. Its defining features:
- **Alignment terms.** Co-investors buy and sell the same securities, in the same proportions and on the same terms as the main fund ("in together, out together"). They negotiate pre-emptive rights on follow-ons by any vehicle the sponsor manages [S: Sidley 2025].
- **Exit by the GP.** ADIC's exit rights are tag-along. Its exit obligations are drag-along [P].
- **Transfers and pledges** usually need GP consent and may face a right of first refusal [P]. This sets how fast and whether a SELL or a pledge-based REFI can happen.
- **Size.** On average the co-investment vehicle's equity is 32% of the GP fund's own investment in the deal [S: BJS, 72 matched deals].

### 2.2 Why GPs offer co-investments, and what that implies [S]
BJS give three motives:
- **Single-deal limits.** Relative deal size is the main determinant: buyout probit coefficients 0.09–0.12***.
- **Price discrimination toward sophisticated LPs.** Most-favoured-nation clauses make it hard to discriminate through fund terms.
- **Courting LPs during fundraising.** A deal done before the follow-on fund closes is more likely to be offered, in buyouts: coefficient 0.20–0.22**.

LMSZ model the outcome as GP–LP bargaining: better LPs reach better vehicles.

Implications [I]:
- ADIC's co-investment flow, and its *quality*, is endogenous to its standing as a primary LP.
- Offers bunch around GP fundraising.
- The reputational discipline that kept adverse selection out of the BJS data needs repeated play. One-off GP relationships deserve wider priors.

### 2.3 Equity as a levered call: the shape of outcomes [I]
Let $V$ be enterprise value, $D$ net debt and $L_0=D_0/V_0$ entry leverage. Then:
$$M=\frac{\max(V_T-D_T,0)}{V_0-D_0}\approx\frac{\max(G-L_0,0)}{1-L_0},\qquad G=V_T/V_0 .$$
Three properties follow, and each matters for ADIC:
1. **The probability of loss does not depend on leverage.** $M<1 \iff G<1$ when $D_T\approx D_0$. Leverage sets the *depth* of losses ($P(G<L_0)$) and the size of the upside.
2. **Fees and leverage sit in the same equation.** For entry multiple $m_0$, debt multiple $\ell_0$ (debt/EBITDA), exit multiple $m_T$ and target MOIC $M^\*$, the required EBITDA growth is:
$$g^\*=\Big[\frac{M^\*(m_0-\ell_0)+\ell_T}{m_T}\Big]^{1/T}-1 .$$
   This reproduces Bain's "12 is the new 5":
   - **2015:** $m_0=10$, $m_T=12.5$, 50% debt/EV with modest paydown gives about 5–6%.
   - **2025:** $m_0=14$, $m_T=15$, about 36% debt/EV gives about 12–13% [S inputs: Bain 2026].
3. **Leverage above about 6× EBITDA fails through cash flow, not only through value.** At 8–9% debt costs, 6× of debt consumes about 50% of EBITDA in interest. Default is therefore better modelled as a coverage-driven hazard than as $V<D$ alone. This is the mechanism behind ADIC's own memo-corpus lesson (context §2, slide 8).

### 2.4 Fee economics: the netting problem [S/I]
- **Fund costs.** FIL estimate that 2-and-20 costs investors 5–7 percentage points a year [S].
- **Co-investment terms.** Co-investments are typically 0/0, 1/10 or 0/20, with an 8% hurdle on deal-by-deal carry [S: BJS].
- **No netting.** Deal-by-deal carry is $\sum_i \min\{(P_i-H)^+, cP_i^+\}$, with no offset for losers. Its value rises with dispersion, just as a basket of calls is worth more than a call on the basket [I].
- **Hidden costs.** Portfolio-company monitoring and transaction fees are usually *not* offset for co-investment vehicles [S: Torys 2026].
- **Expense allocation precedent.** The SEC's 2015 KKR case covered $338m of broken-deal expenses over six years. Co-investors bore none of them, and KKR paid nearly $30m [S].

### 2.5 Control, liquidity and marks [S/P]
- **Exits:** controlled by the GP.
- **Marks:** the GP's valuation × ownership share. They are smoothed and lagged by about one quarter, with λ≈0.5 per quarter (dossier 04).
- **Exit uplift:** about 75% of buyout assets exit above their next-to-last quarterly mark [S: Bain midyear 2026]. Most LPs lose confidence in a GP when an exit comes in more than 5% below the last mark [S: ILPA poll via Bain].
- **Liquidity routes for a co-investor:**
  1. tag-along at the GP's exit;
  2. an LP-led single-asset sale or strip sale, subject to consent and right of first refusal;
  3. an election in a GP-led continuation vehicle (CV).

  ILPA asks for at least 30 calendar days to elect, a status-quo roll option, and that non-response default to *sell*. Whether co-investment vehicles receive the same rights is contractual and must be confirmed (§9).

---

## 3. Methods and models: trade-offs

| Approach | What it captures | Data | Strengths | Weaknesses | Role at ADIC |
|---|---|---|---|---|---|
| Empirical bootstrap of deal multiples (BJS-style) | Skew and dispersion; no dynamics | Deal-level PMEs | Model-free | Historical capital structures; no timing or regimes; PME ≠ cash | Validation benchmark |
| **Static structural (Merton equity), §6.3** | Loss depth vs leverage; upside convexity | Quartiles, leverage | Few parameters; re-bases to today's leverage | No timing | Reference-class prior and re-basing |
| **Dynamic deal engine (recommended)** | EV jump-diffusion, debt, default, competing-risk exits, recaps, marks, follow-ons, regimes | Deal cash flows and marks; regime model | Produces timed cash flows, NAV and marks per scenario; hosts the SELL/REFI/LEVER operators | ~20 parameters; needs pooling | Core engine |
| Fund-style Takahashi–Alexander | Smooth call/distribution curves | Fund cash flows | Simple | Wrong for single assets (no lumpiness or default) | Not for co-investments |
| Survival models (Weibull, Cox, Fine–Gray, random survival forests) | Exit and default hazards, competing routes | Deal histories | Censoring handled; covariates | Data hungry | Calibrate hazard multipliers |
| State-space mark filter (Kalman) | Nowcast of economic equity from lagged marks and comparables | Marks, comparables, debt | Removes smoothing; feeds SELL | Assumes linearity | Nowcast input to dossier 07's fusion |
| Hierarchical Bayes (GP × sector × vintage) | Partial pooling of drift, bias and hazard | ADIC history and licensed deal data | Credibility for thin cells | Prior-sensitive | Bias and credibility estimation |

Trade-off [I]:
- The dynamic engine is required, because ADIC's questions are timing questions: distributions under drought, covenant paths, recap cash.
- The static model is the cheapest way to impose today's leverage on historical outcome data.

---

## 4. Empirical evidence and current market data

### 4.1 Performance studies [S]

| Study | Sample | Key result |
|---|---|---|
| FIL (JFE 2015; NBER w19299) | 392 direct deals by 7 large LPs, 1991–2011; $22.6bn, of which 288 co-investments ($13.9bn) | Capital-weighted TVPI/IRR: co-investments **1.20 / −0.09%**; solo **3.08 / 16.8%**. On 73 matched co-investments, IRR is >8 pp below the sponsor fund, with no TVPI difference, because exits come later. Co-investment EV is ~3× the same GP's median deal. |
| BJS (JFE 2020) | 1,016 co-investments by 458 investors; 464 funds; 13,430 deals | No adverse selection on gross PME. Net buyout PME is 1.76 (0/0), 1.59 (1/10) and 1.56 (0/20), against 1.36 for funds. Portfolios of about **10 buyout deals** beat funds net of fees; VC needs **20+**. |
| LMSZ (JFE 2022) | Custodial data, 112 LPs | By 2017, alternative vehicles were 40% of commitments. They match the market but trail sponsor main funds; top LPs get the best vehicles. In the WP (2018), the discretionary-vehicle PME gap is −0.016 (not significant). |
| BJSt (JFE 2017) | 13,523 deals in 865 buyout funds | Realised deals: median PME 1.4, MOIC 1.9, hold 4.3 years. GP persistence has declined. |
| Lopez-de-Silanes, Phalippou & Gottschalg (JFQA 2015; WP 2010) | ~7,500 investments | ~1 in 10 returns no money; ~1 in 4 has an IRR above 50%. Median IRR (WP) falls from 36% in the smallest-scale decile to 16% in the largest. Scale here is the PE firm's number of simultaneous investments, not deal size [corrected 2026-10-18]. |
| Kaplan & Strömberg (NBER w14207 / JEP 2009) | 17,171 LBOs, 1970–2007 | Exit routes: strategic 38%, financial buyer 24%, IPO 14%, bankruptcy 6%, unknown 11%. Exited by 2 / 5 / 7 / 10 years: 12 / 42 / 58 / 76%. Default ≈1.2% a year. |
| Gompers, Kaplan & Mukharlyamov (JFE 2016) | Survey of 79 PE firms | Firms rely on gross IRR and MOIC; <20% use DCF. Median targets: 25% IRR, 2.5× MOIC. Five-year forecast horizon. 16% set the exit multiple equal to the entry multiple. Target leverage 4.0× (2012). Deal-level equity beta of 2.3 (citing Axelson, Sorensen & Strömberg). |
| Bhardwaj, Gupta & Howell (NBER w33435, 2025) | PE dividend recaps | Total debt +84% on average. That raises the chance of financial distress by 2.4 times the target-firm mean (10-year IV estimate, an increment; OLS ≈0.4 times) [corrected 2026-10-18: was "Distress probability ×2.4 the target-firm mean"]. Deal returns rise while fund returns fall. |

**Table A. BJS Table 4: gross PME distributions [S]**

| Group | N | Mean | P25 | Median | P75 | P99 | SD | Skew | Capital-weighted mean |
|---|---|---|---|---|---|---|---|---|---|
| Buyout co-investments | 365 | 1.76 | 0.26 | 1.16 | 2.45 | 8.43 | 2.10 | 2.50 | 1.76 |
| Buyout other deals | 5,399 | 1.70 | 0.41 | 1.13 | 2.15 | 11.35 | 2.15 | 3.50 | 1.59 |
| Buyout funds | 246 | 1.86 | 1.39 | 1.70 | 2.11 | 5.37 | 0.75 | 2.04 | 1.59 |
| VC co-investments | 651 | 1.25 | 0.15 | 0.77 | 1.24 | 13.84 | 2.13 | 4.39 | 1.55 |

### 4.2 Size, timing and sector effects [S]
- **Size.**
  - FIL: co-investment deals are ~3× larger.
  - BJS: the *largest deals not offered* for co-investment perform worst (capital-weighted 1.59 against 1.76).
  - Not deal-size evidence: Lopez-de-Silanes et al.'s diseconomies of scale concern the number of investments a PE firm holds simultaneously, not deal size [corrected 2026-10-18].
  - Hamilton Lane (2024): middle-market deals show more outperformance with "only slightly higher loss ratios", but warns that DIY co-investing risks "doubling down" on a few sponsors.
- **Timing.**
  - FIL: co-investment volume crested in 2006–07, and TVPI was 1.10–1.18 for 2006–07 deals and 0.78 for 2008.
  - Recent cohorts: only 17% of 2021-vintage deals had exited four years after investment, against 32% of the 2017 cohort [S: Bain via ABF Journal].
- **Sector (2026).**
  - Software PE marks fell about 8% in Q1-2026 [S: Bain midyear].
  - Software CVs fell to 10% of GP-led volume, from 18% in 2025 [S: Evercore].
  - Buyers place "less reliance on sponsor-marked NAV" for software [S: Lazard].
  - Treat software co-investments as a distinct high-uncertainty cohort [I].

### 4.3 Terms and costs, 2025–2026 [S]

| Item | Value | Source (date) |
|---|---|---|
| No management fee | ~2/3 of managers; ~1 in 10 charge the full fund rate | Sidley (Oct 2025) |
| No carry | >1/2 of managers | Sidley (Oct 2025) |
| Deals proposing economics | <7%; ~62% of co-investment occurs pre-signing (co-underwriting) | Investment Officer roundtable (Feb 2026; teaser) |
| Hidden costs | Admin $50–150k or 2–10 bp; monitoring 1–2% of commitment a year; transaction 0.5–3% of EV; broken-deal sharing in ~20% of deals; no offsets | Torys (Jul 2026) |
| Average buyout management fee | 1.6% (2025), against a traditional 2% | Bain (Feb 2026, citing Preqin) |
| Co-investment offered per $ of fee-bearing capital | median 33¢ (range 0–110¢), equal to a 25% revenue reduction | Bain (Feb 2026) |
| Program cost assumption | Co-investment 0.91% of committed a year for 5 years; funds 0.11% | FIL, as used by BJS |

### 4.4 Diversification evidence

| Source | Finding |
|---|---|
| BJS (2020) [S] | Median net-net PME at 0/0 by portfolio size: 1 deal 1.16, 5 deals 1.48, 10 deals 1.63, 50 deals 1.65. Mean 1.71. Fund portfolios ≈1.44. |
| HarbourVest‡ | US buyout co-investments, 2004–18 vintages, 1%/12.5% fees: P(<1.5×) is 24% with 6 companies and 3% with 50. |
| Altius (2014) [S headline] | "Adverse selection and portfolio concentration are the main risks". 20-company portfolios can still lose significant capital‡. |
| Capital Dynamics‡ | 435 realised buyout co-investments (1988–2017). Archetypes: >50 holdings (large-cap global), 20–30 (mid-market), <20 (concentrated regional). |

### 4.5 Exits, holding periods and recaps [S]
- **Exits and holds.**
  - 2025 buyout exits: $717bn on 1,570 deals.
  - Average holding period about 7 years, against 5–6 years in 2010–21.
  - About 32,000 unsold companies worth $3.8tn (Bain 2026), and about 33,000 by June 2026.
  - PitchBook's US median hold at exit is 5.5 years (via dossier 04).
- **Recap volumes** (PitchBook LCD, second-hand via Capstone and ABF):
  - Sponsored recap loans: $74.3bn in 2025 (+11%), after +326% in 2024.
  - Broadly syndicated loan dividends: $43.6bn by 8 Dec 2025, the highest since the GFC.
  - Q1 2026: $11bn, down 54.5% year on year (Capstone; the source does not attribute this figure).
- **Recap leverage:** average leverage rose from 4.2× before the dividend to 5.2× pro forma. 22% of 2025 recaps were at ≥6×, against 46% in 2021. The lag from LBO to recap is 4.5 years, against 3.6.
- **Exit quality vs marks:** 75% of buyout exits come in above the next-to-last mark.

### 4.6 Secondary markets for co-investment and single-asset exposure (H1-2026) [S]

| Metric | Jefferies (Jul 2026) | Evercore (Jul 2026) | Lazard (interim 2026) |
|---|---|---|---|
| Total / GP-led volume | $118bn / $62bn (53%) | $121bn / $65bn | $124bn / ~49% |
| Single-asset share | SACVs 68% of CVs | SACVs 53% of GP-led ($34bn, +88% YoY) | SACVs 54% of GP-led |
| Single-asset pricing | n/a | 52% at par, 14% above, 34% below | ~87% of SACV volume >90% of NAV; 23% above par (8% in 2025) |
| Buyer target (gross, 4 years) | n/a | SACV ~2.3×; MACV ~1.9×; single LP interest ~1.8×; diversified ~1.7× | n/a |
| Co-investment specifics | Co-investment fundraising +17% to ~$27bn. LP sales of co-investment exposure "gained momentum". Partial sales of large co-investments, including one >$1bn. | "Directs" 5% of GP-led | Existing LPs still prefer selling to rolling |
| LP portfolio pricing | 87% (buyout 91%; tail-end ≥25% discount) | high-quality buyout ~90% | n/a |

Other secondary-market data:
- **Mid-size CV syndication:** syndicate capital for CVs under $750m "has significantly decreased" [S: Jefferies]. This is a liquidity constraint for mid-size co-investment assets moving into CVs [I].
- **Buyer capacity:** ~15% of secondary buyers can write SACV checks above $250m [S: Jefferies].

### 4.7 Financing: NAV facilities and holdco PIK [S]
- **Proskauer FY-2025, primary NAV facilities:**
  - closing LTV: <5% (23%), 5–10% (32%), 10–25% (36%), ≥25% (9%);
  - spreads: concentrated at 4–5%, with a 7–8%+ tail of 21%;
  - OID mostly 1–1.5%; 5-year maturities (45%); LTV-based sweeps (63%);
  - no minimum MOIC in 49% of facilities;
  - uses: 45% follow-ons, 7% dividends to investors.
- **Rede (Jun 2026):** margins have converged to 4–7%.
- **No co-investment data.** Neither survey separates co-investment or single-asset collateral. The concentrated-pool terms in §6 are [I].
- **Holdco PIK benchmarks:**
  - Verisure Holdco (H&F, 2025): €1bn PIK-toggle notes at 5.625% cash or 6.375% PIK, six years, secured on a 43.7% *listed* stake at low LTV. It was the "largest and tightest" holdco PIK since 2019, and private credit "typically lend[s] at a higher price" [S: IFR].
  - Freshfields (GRR, Nov 2025): holdco debt is structurally junior. Enforcing the share pledge triggers an opco change of control [S].

---

## 5. Practitioner practice and case studies

**How co-investment teams forecast [S/P].**
- Deal teams build 5-year LBO models with base, downside and upside cases. Valuation is by gross IRR and MOIC, with exit values from comparables. 16% set the exit multiple equal to the entry multiple [S: GKM].
- Group re-forecasts update EBITDA, exit year and exit multiple.
- **Documented biases:**
  - **Hold period:** models assume about 5 years, against about 7 years realised today [S: Bain].
  - **Multiple expansion:** before 2021 it drove >50% of buyout returns [S: Bain 2026], and models still lean on it.
  - **Leverage tolerance:** recaps above 6× were common in 2021.
  - **ADIC's own memo lessons** (context §2): leverage above 6× EBITDA, dependence on multiple expansion and weak downside cases failed. Distribution timing was "repeatedly too optimistic" after spread shocks.
- In GKM, more than half of PE investors do not adjust hurdles for deal leverage [S]. An undifferentiated 20–25% target therefore over-rewards levered deals [I].

**Program archetypes [S‡].** Capital Dynamics groups programs into >50, 20–30 and <20 holdings. Hamilton Lane promotes fund-based co-investment at about half the fees of commingled funds, a marketing claim. At $18bn, ADIC is a direct program comparable to the large LPs in FIL and LMSZ; LMSZ cite Harvard, CPPIB and Texas TRS demanding co-investment and special terms [S].

**Case lessons.**
1. **FIL's seven LPs.** Skilled direct investors still lost on co-investments concentrated in 2006–08 megadeals [S]. *Lesson: vintage budget and size caps [I].*
2. **KKR broken-deal expenses (SEC, 2015).** Co-investors escaped $338m of costs for years [S]. *Lesson: ADIC is now the co-investor; model and audit vehicle-level cost allocation.*
3. **2026 strip sales.** LPs sold partial stakes in appreciated co-investments to "crystallize gains and de-risk" [S: Jefferies]. *Lesson: SELL is a sizing tool (fraction x), not binary. The disposition bias in dossier 08 applies.*
4. **Recap-driven DPI.** Recaps became a main return-of-capital route in 2025 [S: ABF], at a cost in distress risk [S: Bhardwaj et al.]. *Lesson: book recap cash as distribution, and raise that deal's default hazard.*

---

## 6. Design implications for the ADIC framework

### 6.1 State variables

**Per deal $i$:**

| Variable | Meaning |
|---|---|
| $V_{i,t}$ | Enterprise value, ADIC share basis |
| $D_{i,t}$ | Net debt (opco) |
| $B^{spv}_{i,t}$ | ADIC-level SPV or holdco debt |
| $K_{i,t}$ | Cost basis, including follow-ons |
| $a_{i,t}$ | Age |
| $M_{i,t}, M^-_{i,t}$ | GP mark and previous mark |
| $\omega_i$ | Ownership share |
| $\mathrm{ICR}_{i,t}$ | Interest coverage |
| Tags | lead GP $g(i)$ and linked PE fund; vintage $v(i)$; sector; region |
| Rights | tag/drag, ROFR/consent, pre-emptive, CV election, pledge permission |
| Status | active, exited or written off |
| Beliefs | fused forward belief $(\hat\mu_i,\hat\sigma_i,\hat\tau_i)$ from dossier 07 |

**Global:** regime $s_t\in\{B,N,D,C\}$ (dossier 04), listed-equity factor $r_{m,t}$, credit window $c_t$, and secondary pricing state $\pi^{SA}_t$.

### 6.2 Deal-level dynamics (quarterly, Δ = ¼) [I]

**(E1) Enterprise value:** Kou jump-diffusion with a regime-dependent factor.
$$\ln\frac{V_{i,t+\Delta}}{V_{i,t}}=(\alpha_i-\tfrac12\sigma_{id}^2)\Delta+\beta_A\,r_{m,t+\Delta}+\sigma_{id}\sqrt\Delta\,\varepsilon_{i,t+\Delta}+\sum_{n=1}^{N_{i,t}}J_{i,n},\quad N\sim\mathrm{Poi}(\lambda_J\Delta),\ J\sim\mathrm{DExp}(p_{up},\eta_{up},\eta_{dn}).$$
Add a sector factor where data permit, for example software/AI.

**(E2) Debt:**
$$D_{t+\Delta}=D_t(1-a\Delta)+\Delta D^{rec}_t+\Delta D^{PIK}_t .$$
Equity is $E=\max(V-D,0)$.

**(E3) Default:** absorbing write-off at $\tau_D=\inf\{t:V_t\le\kappa D_t\}$, with κ≈0.75 to reflect covenant-lite survival.
- A production upgrade is the hazard form $h_D=h_0\exp\{b(\mathrm{ICR}^\*-\mathrm{ICR}_t)^+\}$.
- Equity recovery is $R\sim U(0,R_{max})$.

**(E4) Exit:** competing risks.
$$\lambda^X_{i,t}=m_X(s_t)\,\frac{k}{\eta}\Big(\frac{a_{i,t}}{\eta}\Big)^{k-1}\exp\{\gamma\ln(E_{i,t}/K_{i,t})\}.$$
- Exit routes $r\in$ {strategic, sponsor, IPO (staged over 4–8 quarters), CV} have probabilities $\pi_r(s_t)$.
- Proceeds are $X=E(1+u)$, with $u\sim N(\mu_u,\sigma_u)$.
- On the CV route ADIC chooses between selling at the CV price and rolling.

**(E5) Recap:** with probability $\rho_R(s_t,c_t)\Delta\cdot\mathbb 1\{a\ge2,\ D/V<L^{elig}\}$:
- debt rises by $\Delta D=\phi D$;
- the distribution is $0.98\,\Delta D$;
- the default hazard is scaled up afterwards by a multiplier of about ×1.1 (OLS) to ×1.7 (IV) at φ = 0.25 [I: Bhardwaj, Gupta & Howell's 10-year distress estimates, which go with an 84% average debt increase, scaled linearly to φ] [corrected 2026-10-18: was "target ×2.4 on the distress mean [S]"].

**(E6) Follow-on:** with probability $q_F\Delta$, a call of $fE$. If ADIC declines, $\omega$ is diluted.

**(E7) Marks:**
$$M_{t+\Delta}=\lambda M_t+(1-\lambda)E_{t-\Delta}+b_{g}+e_t .$$
Here $b_g$ is the GP-specific mark bias and $e_t$ noise. The economic NAV for decisions comes from a Kalman nowcast that uses comparables.

**(E8) Fees and carry** (per vehicle terms):
$$\mathrm{carry}_i=\min\{(P_i-H_i)^+,\ c\,P_i^+\},\qquad H_i=(1+h)^{T_i}-1 .$$
Add vehicle and company-level costs (§4.3).

**(E9) Book aggregation:**
- $\mathrm{NAV}^{econ}=\sum\omega_iE_i$ and $\mathrm{NAV}^{rep}=\sum\omega_iM_i$;
- net cash flow = distributions (exits + recaps) − calls (new tickets + follow-ons + fees);
- risk via the look-through equity beta $\beta_E\approx\beta_A V/E$.

### 6.3 Calibration results [I, targets S]

**Static house fit.** The extended structural model, at $L=0.60$, against the BJS buyout co-investment distribution:

| Statistic | Target | Model | | Derived quantity | Model |
|---|---|---|---|---|---|
| P25 / median / P75 | 0.26 / 1.16 / 2.45 | 0.261 / 1.141 / 2.484 | | P(M<1) | 46.4% |
| P99 | 8.43 | 9.38 | | P(M<0.5) | 32.2% |
| Mean / SD (winsorised) | 1.76 / 2.10 | 1.73 / 1.91 | | P(M>3) / P(M>5) | 19.1% / 7.0% |
| Skew | 2.50 | 1.72 | | Parameters | μ=0.036; σ=0.60 per hold (≈0.28 a year); jump probability 0.148, mean log-jump 0.166; $R_{max}$=0.10 |
| P(M<0.05) | ≈0.10 [Lopez-de-Silanes et al.] | 0.100 | | | |

The model understates the upper tail (SD and skew). It is therefore conservative on upside, and it slightly understates how many deals are needed to diversify. Replace it with ADIC or licensed deal-level data when available.

The best-fitting $L$ is 0.60–0.65. GKM report historical debt-to-capital targets of 60%, and cite Axelson et al. (2013) for 70% [S].

**Re-basing to current capital structures (same EV process):**

| Structure | L | Mean | Median | P(M<0.05) | P(M<0.5) | P(M>3) |
|---|---|---|---|---|---|---|
| Historical fit | 0.60 | 1.73 | 1.14 | 10.0% | 32.2% | 19.1% |
| 6.0× debt at 12× EV | 0.50 | 1.56 | 1.11 | 6.9% | 28.5% | 14.8% |
| Today, ~40% debt/EV | 0.40 | 1.45 | 1.09 | 4.1% | 24.7% | 11.5% |
| Today, plus 14×→13× compression | 0.40 | 1.30 | 0.97 | 5.1% | 28.7% | 9.3% |

**Diversification.** P(portfolio multiple <1) by number of deals and pairwise factor loading ρ:

| N | ρ=0 (median; 5th pct) | ρ=0 | ρ=0.1 | ρ=0.2 | ρ=0.3 |
|---|---|---|---|---|---|
| 1 | 1.14; 0.03 | 46% | 46% | 46% | 46% |
| 5 | 1.63; 0.57 | 19.6% | 25.4% | 29.1% | 32.1% |
| 10 | 1.68; 0.85 | 9.8% | 17.6% | 23.3% | 28.8% |
| 20 | 1.73; 1.09 | 2.7% | 12.5% | 20.4% | 26.7% |
| 50 | 1.75; 1.31 | 0.1% | 9.1% | 17.7% | 25.1% |
| 100 | 1.76; 1.45 | 0.0% | 8.0% | 17.5% | 24.3% |

**Vintage diversification** for 60 deals, with global factor 0.05 and vintage factor 0.20:
- spread over 1, 2, 4 and 8 vintages, P(<1) is 21.8%, 14.1%, 8.5% and 5.9%;
- the 5th percentile is 0.55, 0.74, 0.89 and 0.97.

**Fee drag.** Absolute multiples over a 5-year hold, with mean gross 2.48× and median 1.61×:

| Terms | E[net] | Median net | E[carry] | IRR of the mean |
|---|---|---|---|---|
| 0/0 | 2.48 | 1.61 | 0 | 19.9% |
| 1/10 (8% hurdle, catch-up) | 2.26 | 1.50 | 0.17 | 17.7% |
| 0/20 (8% hurdle) | 2.13 | 1.49 | 0.34 | 16.4% |
| Fund 2/20, pooled over 20 deals | 2.11 | 2.06 | 0.27 | 16.1% |

For a 7-year hold the IRRs of the mean are 16.1%, 14.4%, 13.5% and 13.2%.

**Exit hazard.**
- The Weibull fit (k = 1.447, η = 7.70 years) reproduces Kaplan & Strömberg: model 13 / 41 / 50 / 58 / 77% against 12 / 42 / 51 / 58 / 76% exited by 2 / 5 / 6 / 7 / 10 years.
- One-year exit probability at ages 3 / 5 / 7:
  - normal: 12.4 / 14.9 / 16.9%;
  - drought: 6.4 / 7.8 / 8.9%;
  - open window: 15.8 / 18.9 / 21.4%;
  - crisis: 3.9 / 4.7 / 5.4%.

**Synthetic book simulation** ($18bn, 90 positions, 2,000 paths, 12 quarters):

| Metric | Start in drought | Start normal |
|---|---|---|
| Distributions over 3 years: mean (P10 / P50 / P90) | $9.2bn (3.6 / 8.4 / 16.0) | $11.7bn (5.4 / 11.0 / 18.6) |
| Calls over 3 years (mean) | $5.8bn | $6.7bn |
| Net cash flow over 3 years: mean (P10 / P90) | +$3.4bn (−1.3 / +9.4) | +$5.0bn (−0.4 / +11.3)† |
| Net cash flow if the drought lasts all 12 quarters (21% of paths) | +$1.6bn (P10 −1.8) | n/a |
| Year-1 distribution yield: mean (P10 / P90) | 12.4% (4.3 / 22.6) | 19.3% (8.7 / 31.3) |
| Write-off rate per position-year | 3.3%† (was 2.5%) | 2.8%† (was 2.1%) |
| Recap dividends / exit proceeds | 3.6% | 3.6% |
| P(exit > next-to-last mark), target 0.75 | 0.72 | 0.74 |
| Reported vs economic NAV gap (P10 / P50 / P90) | −18.5 / −3.6 / +21.5%† | −18.8 / −3.1 / +19.3%† |

† [corrected 2026-10-18] Re-run with the E3 write-off barrier checked quarterly against $0.75D\,e^{+0.5826\sigma_V\sqrt{0.25}}$ ($\sigma_V$ = diffusive EV volatility; effective κ 0.81–0.84 by regime), on the published random numbers. The original run checked $V\le 0.75D$ at quarter ends with no correction, which overstates survival (§7). The write-off rate rises from 2.5% to 3.3% (drought start) and from 2.1% to 2.8% (normal start); an independent fine-grid continuous-monitoring check gives 3.1% / 2.7%. Old values in the other marked cells: normal-start net cash flow P90 +11.4; NAV gap −18.5 / −3.5 / +21.9% and −18.7 / −3.0 / +19.2%. All other rows are unchanged at the precision shown. Source: `research/groups/addenda/G4_barrier_rerun/RESULTS.md` §3–§4. SYNTHETIC.

**Concentration** ($18bn; 90 positions; lognormal sizes, σ=0.8):
- effective N = 45; top-10 share 35%; largest position $1.2bn;
- idiosyncratic volatility 6.0% a year (1σ ≈ $1.1bn), against 22.4% systematic, with β_E = 1.4 and market volatility 16%;
- with 150 positions, effective N = 74 and idiosyncratic volatility 4.7%.

### 6.4 Forecast fusion and bias controls for co-investments

**Three series per deal:**
- **u (underwritten):** the investment-committee base case, with downside and upside.
- **a (current actual):** since-inception IRR and TVPI on GP marks, plus the nowcast.
- **f (forecast):** the latest group re-forecast.

Each is mapped into $(\mu,\sigma,\tau)$ of (E1)–(E4) and fused as in dossier 07. Two changes are specific to co-investments [I]:
1. **The prior is the re-based reference class.** Condition on entry debt/EV, entry multiple, sector, size and regime, not on historical co-investment averages. The historical class overstates the mean by about 0.3×.
2. **"What you need to believe" checks.** Each check is a flag, scored with dossier 07's bias model:
   - required growth $g^\*$ (§2.3) above the reference-class 75th percentile;
   - $m_T>m_0$, i.e. reliance on multiple expansion;
   - $\ell_0>6\times$ or ICR < 2.0× at forward SOFR + spread;
   - a forecast exit within 4 quarters while the regime-implied probability is below 15% (distribution timing).

**Initial bias corrections until ADIC's archive supports estimation [I]:**
- hold period +1.5 to 2.0 years (5 years modelled against about 7 realised);
- exit multiple shrunk 50% toward the entry multiple;
- EBITDA CAGR shrunk 30% toward the reference median.

**Correlated errors.** Co-investment and fund positions with the same GP share mark bias $b_g$ and forecast error. Model a GP random effect in both (dossier 07, open question 7).

### 6.5 Decision variables and operators
Decisions per deal and quarter:
- **SELL** $x_{i,t}\in[0,1]$, with strips allowed;
- **channel** $\in$ {LP-led single-asset sale, CV election, portfolio strip};
- **REFI**: ADIC-level pool draw $b_t$;
- **LEVER**: $\ell_{i,t}$ = ADD (new ticket or upsize) plus optional SPV debt;
- **pacing** $n_t$: new co-investment deployment.

Scoring uses dossier 08: $\mathrm{Score}=\sum\pi_{s,t}\Delta CF-\lambda_R\Delta\mathrm{CVaR}-\lambda_{Lev}\Delta Lev-\kappa^{GP}-\kappa^{tc}-\kappa^{irr}$, with LEVER ≡ ADD + REFI.

**SELL**
- Execution lag:
  - LP-led sale: 3–6 months, including consent and ROFR;
  - CV election: the GP's timetable, at least 30 days.
- The bid comes from a buyer-return model:
$$p=\frac{\mathbb E_b[X]}{(1+y_b)^{\tau_b}}-\text{tc},\qquad y_b\approx 0.20\text{–}0.25 \text{ (single asset, gross)} .$$
  Clip to the observed state: in normal conditions about 87% of SACV volume trades above 90% of NAV. Use deep discounts for unfamiliar, software or tail assets. Add stress [I].
- Selling at bid $p$ beats holding when $p(1+\bar\ell)\ge \mathrm{PV}_{hold}$.
- **Worked example [I].** A $400m position: net debt 6.0×, EV 14×, hurdle 9%.

  | | Normal (τ = 2.5y) | Drought (τ = 3.5y) |
  |---|---|---|
  | PV of holding | $402m (100.5% of NAV) | $366m (91.5% of NAV) |
  | Bid 88%: buyer IRR under our beliefs / break-even ℓ | 14.9% / 14.2% | 10.2% / 3.9% |
  | Bid 95%: buyer IRR / break-even ℓ | 11.5% / 5.8% | 7.8% / −3.7% (SELL) |

**HOLD.** This is the baseline. It still carries charges for concentration CVaR and the GP-relationship term $\kappa^{GP}$.

**REFINANCE**
- *Company recaps* are exogenous, GP-controlled events: model them under E5, never as ADIC decisions.
- *ADIC pool facility* [I]:
  - LTV cap set by concentration: ≤10% if effective N < 10, 15% for 10–25, 20% above 25;
  - spread 450–750 bp, OID 1–2%;
  - LTV-based sweep, with a trigger at 1.5× the opening LTV and default at 2×;
  - requires pledge consent from each GP.
- Example: 15% LTV at SOFR + 650 bp costs about 11.0% all-in. The single-asset breach probability is 29% (normal) or 37% (drought). Use pools, not single assets.

**LEVER**
- An SPV holdco PIK at 12% and 25% LTV:
  - expected IRR 9.2% levered against 9.2% unlevered in normal conditions, and 6.0% against 6.3% in a drought;
  - P(residual = 0) at exit is 11.8% in normal conditions and 22.8% in a drought. These at-exit figures involve no barrier monitoring, so the 2026-10-18 barrier fix leaves them unchanged. With the E3 barrier (V ≤ 0.75D at any time) they are 11.8% and 22.9% [I; `research/groups/addenda/G4_barrier_rerun/RESULTS.md` §5.2].
- Rule [I]: lever only if fused $\hat\mu$ minus the PIK rate exceeds $\bar\ell$ plus the risk charge, under robust (worst-case) duals.

**Minority constraints (hard):**
- no discretionary exit timing;
- no recap control;
- dilution if follow-ons are declined;
- transfer and pledge consent required;
- information on the GP's reporting cycle.

### 6.6 Cross-group links [I unless S]
1. **PE → co-investment flow.** Offered flow is $O_t=\theta\sum_{k=0}^{4}d_kC_{t-k}$:
   - $C$ = PE primary commitments; $d$ = deployment profile (0.15/0.25/0.25/0.20/0.15);
   - θ = 0.33 (Bain median [S]); 0.5 or more for top-tier relationships;
   - acceptance rate $a$ = 0.3–0.6.

   At $C$ = $10bn a year, θ = 0.33 and $a$ = 0.5, accepted flow is about $1.65bn a year. Sustaining an $18bn book with roughly 6-year lives needs about $3bn a year. Cutting $C$ by 30% therefore shrinks the book, or forces lower selectivity, with a 1–5 year lag.
2. **Double exposure.** Look-through exposure per company = fund share + co-investment. Apply a per-GP cap over fund plus co-investment exposure.
3. **Secondaries group.** It is a price source and a potential buyer of co-investment strips. An internal transfer is zero-sum and never counts as liquidity (context §1A).
4. **Capital Solutions.** It is a source of holdco PIK and preferred-equity pricing, under conflict controls.
5. **Private Credit.** A recap financed by ADIC-held credit funds moves value between ADIC's own claims (Bhardwaj et al. show losses to pre-existing creditors). Net these at company level.
6. **Overlay.** It can hedge the co-investment book's β_E (about 1.4–2.0 at deal level) with index futures when the liquidity shadow price is high. Basis risk is large.
7. **Treasury.** Calls are 100% at close at short notice. About 62% of co-investments happen pre-signing [S], which adds warehousing and syndication risk. Hold committed liquidity against the pipeline.
8. **Consistency with sibling group streams** [I; checked 2026-10-18; their files are not edited here]:
   - **G1.** G1's realised co-investment ratio ρ≈0.2 per committed dollar equals θ·a (0.33 × 0.3–0.6 ≈ 0.10–0.20). Use θ and a when modelling offers and selectivity separately.
   - **G3.** G3 requires one set of EV paths for PE, Co-investment and Capital Solutions claims. E1 should be that shared engine.
   - **G7.** G7's single-asset SELL discount schedule (15%→45%) is a conservative stress overlay. Here the normal-state bid is quality-dependent: about 87% of SACV volume trades above 90% of NAV.
   - **G9 (recalibration needed).** G9 derives deal P(MOIC<1) ≈ 0.22 from fund dispersion. The BJS-calibrated model implies P(MOIC<1) ≈ 0.38–0.39 at historical leverage and 0.35 at L=0.40, with median MOIC ≈1.5 (converting PME to MOIC at 1.36×, from BJSt's 1.9/1.4). Recalibrate G9's co-investment generator to BJS Table 4. G9's ρ_GP = 0.6 for same-GP fund and co-investment errors is a reasonable default for §6.4.

### 6.7 Objective terms and constraints (book level) [I]
**Objective:** add to the TPA objective:
- co-investment net cash flows priced by $\pi_{s,t}$;
- terminal economic NAV;
- penalties on concentration CVaR, vintage deviation and fee leakage.

**Default constraints** (for IC confirmation):

| Constraint | Default |
|---|---|
| Co-investment NAV | 8–12% of the fund |
| Effective N | ≥ 40 |
| Single position | ≤ 4% of co-investment NAV (≈ $0.7bn) |
| Per GP, look-through | ≤ 15% of PE + co-investment NAV |
| Annual deployment | within ±30% of NAV target / average life |
| Software / AI-exposed | ≤ 25% |
| Entry leverage | debt/EBITDA ≤ 6.0×, debt/EV ≤ 55%, ICR ≥ 2.0× |
| SPV leverage | LTV ≤ 20% |
| Encumbrance | cap shared with dossier 06 |

### 6.8 Calibration targets
1. The BJS quartiles, mean and SD.
2. Lopez-de-Silanes et al.: ~10% zero-return share.
3. Kaplan & Strömberg exit timing and route mix.
4. Bain: ~7-year holds; 75% of exits above the next-to-last mark.
5. MSCI distribution rates by regime (dossier 04): drought 9–11%, normal 17–24%.
6. LCD recap volumes and +1 turn of leverage.
7. The Lazard and Evercore single-asset pricing distributions.
8. The BJS and HarbourVest diversification curves.
9. ADIC's own co-investment write-off rate, against the simulated ≈2.8–3.3% a year [corrected 2026-10-18: was 2–2.5%, from a quarterly barrier check with no correction; see the † note in §6.3].

### 6.9 Data needs (ADIC)
- **Deal ledger:** GP, linked fund, vintage, sector, ownership, cost, follow-ons, dated cash flows, quarterly marks, entry EV/EBITDA, net debt/EBITDA, debt terms, recaps and exit route.
- **Rights:** tag/drag, ROFR, pledge consent, CV elections and pre-emptive rights.
- **Fees:** vehicle and company-level.
- **Bitemporal history** of every deal model (u, f).
- **Deal flow:** offers received, accepted and declined by GP.
- **Cross-holdings** with Private Credit.
- **Reference class:** a licensed deal-level dataset.

### 6.10 SPECIFICATION CARD — Co-investment group

| Item | Specification |
|---|---|
| **Data fields** | `deal_id, gp_id, linked_fund_id, vintage, sector, region, ownership, cost, followons[], cf[date,amt,type], marks[q], ev_ebitda_entry, nd_ebitda_entry, debt_terms, icr, recaps[], exit_route, fees{vehicle,company}, rights{tag,drag,rofr,pledge,cv,preemptive}, deal_model[u_t,f_t] (bitemporal), status`; `synthetic` flag on every generated record |
| **Value equation** | E1–E3: $\ln V$ jump-diffusion with $\beta_A r_m$; $E=\max(V-D,0)$; write-off at $V\le\kappa D$ (or the ICR hazard) |
| **Cash-flow equations** | Calls: ticket at close + follow-ons ($q_F$, $f$) + fees. Distributions: $E(1+u)$ at exit (E4) + recap dividends $0.98\phi D$ (E5) − deal-by-deal carry (E8) |
| **Default parameters [I]** | $\beta_A$=0.9; $\alpha$=1% a year; $\sigma_{id}$=0.25; $\lambda_J$=0.15 a year, $p_{up}$=0.4, $\eta_{up}$=0.20, $\eta_{dn}$=0.30; $L_0$=0.45 (today) and 0.60 (historical calibration); amortisation 1% a year; κ=0.75; Weibull k=1.447, η=7.70 y [fit to S]; γ=0.5; $\mu_u$=0.15, $\sigma_u$=0.10; λ=0.5 per quarter with a 1-quarter lag (dossier 04); recap probability (B/N/D/C) 15/10/5/0% a year when $a\ge2$ and $D/V<0.5$, φ=0.25; $q_F$=5% a year, $f$=10%; exit multipliers 1.3/1.0/0.5/0.3 |
| **Static reference class** | Historical: μ=0.036, σ=0.60 per hold, jumps 0.148 × 0.166, $R_{max}$=0.10, L=0.60 (fit to BJS). Re-base with today's L (≈0.40) and multiple path |
| **Liquidity terms** | No redemption. Exits on the GP's clock. SELL lag 3–6 months (LP-led) or the CV timetable (≥30 days). Pledges need GP consent |
| **Stress behaviour** | Drought: exit hazard ×0.5, recap probability falls to 5%, SACV syndication thins for deals <$750m. Crisis: hazard ×0.3, no recaps, bids fall to 70–80% (assumption), and EV beta plus jumps produce write-offs |
| **SELL** | Fraction $x$ by channel; bid = buyer-return model clipped to the SACV pricing state; accept if $p(1+\bar\ell)\ge \mathrm{PV}_{hold}$ plus κ terms |
| **HOLD** | Baseline LAPV under fused beliefs, minus concentration CVaR |
| **REFINANCE** | Recaps are exogenous (E5). ADIC pool facility: LTV 10–20% by effective N, SOFR + 450–750 bp, 1–2% OID, LTV sweep, trigger at 1.5× and default at 2× opening LTV |
| **LEVER** | ADD plus optional SPV PIK (≈10–13% [I]; listed collateral cheaper, cf. Verisure) or NAV draw; look-through debt/EV ≤ 65% |
| **Forecasts and biases** | Deal models (5-year horizon, IRR/MOIC, comparables exit). Biases: hold optimism (+1.5–2 years), multiple expansion, leverage >6×, distribution timing after spread shocks, no leverage-adjusted hurdles |
| **Synthetic defaults** | 90 positions × $0.2bn, ages U(0,7), lognormal sizes σ=0.8, start regime D, deployment $0.75/0.75/0.50/0.25bn a quarter by regime; label everything SYNTHETIC |
| **Links** | PE (deal flow θ, double exposure, κ^GP); Secondaries (bids, zero-sum transfers); Capital Solutions (holdco and preferred-equity pricing); Private Credit (recap netting); Overlay (β hedge); Treasury (calls at close, warehousing) |

---

## 7. Implementation notes
- **Engine.** Vectorise across paths × position slots in numpy, as in the reference script. Use numba for per-deal event logic at production scale (10⁵ paths × 200 positions × 40 quarters).
- **Common random numbers** across SELL/HOLD/REFI comparisons give low-variance decision deltas. Use Sobol QMC (`scipy.stats.qmc`) for the market and regime drivers.
- **Hazards.** `lifelines` (Weibull or Cox AFT) and `scikit-survival` (random survival forests). Use Aalen–Johansen or Fine–Gray for competing exit routes. Treat unexited deals as censored, never drop them.
- **Hierarchical estimation.** PyMC or NumPyro for GP × sector × vintage effects on drift, mark bias $b_g$ and forecaster bias. Pool toward the re-based reference class.
- **Nowcast.** A Kalman filter on the mark equation (E7), with comparable indices as observed signals. Check against the reported-vs-economic gap distribution in §6.3.
- **Optimisation.** cvxpy for pacing, caps and CVaR (Rockafellar–Uryasev). Use a MILP only for binary SELL bundles (column generation, dossier 08).
- **Numerical pitfalls:**
  - Discrete barrier monitoring overstates survival. A continuously monitored default barrier (E3) simulated at step Δ should be checked against $\kappa D\,e^{+0.5826\sigma\sqrt\Delta}$, which moves the barrier toward the current value; σ is the diffusive EV volatility. This is the Broadie–Glasserman–Kou (1997) continuity correction applied in reverse. Alternatively, simulate at weekly or finer steps: monthly checks without the shift still miss about 13–14% of write-offs. The opposite shift, $e^{-0.5826\sigma\sqrt\Delta}$, is BGK's own use: evaluating a discretely tested event, such as a quarterly covenant test, with a continuous formula. A covenant tested quarterly and simulated quarterly needs no shift. [corrected 2026-10-18: the earlier text read "barrier × $e^{-0.5826\sigma\sqrt\Delta}$ or simulate monthly"; that shift lowers the barrier and adds to the bias. See `research/groups/addenda/G4_barrier_rerun/RESULTS.md` §1 and §7.]
  - **PME ≠ cash multiple.** Convert before any fee or liquidity calculation.
  - BJS statistics are winsorised at the 99th percentile. Match like with like.
  - CVaR at 5% from 2,000 paths has wide standard errors. Report confidence intervals.
  - Avoid IRR averaging: compute portfolio IRRs from pooled cash flows.
  - Keep a bitemporal store to avoid look-ahead in bias estimation.

---

## 8. Risks, pitfalls and limitations
1. **Selection may return.**
   - BJS cover deals through about 2010.
   - In the CV era GPs can keep trophy assets in SACVs and offer co-investment on large or complex deals.
   - Monitor offered-versus-retained performance by GP; use LMSZ-style LP-quality effects as priors.
2. **The structural model is stylised.**
   - It understates the upper tail.
   - The cash-flow default channel (ICR) is simplified.
   - The jump and uplift parameters are tuned to targets, not estimated from ADIC data.
3. **Regime dependence.** Exit multipliers and recap probabilities are assumptions anchored to aggregate data (dossier 04). Co-investments may be more cyclical (FIL correlation −0.59).
4. **Liquidity illusions.** Strip-sale and SACV depth is concentrated in high-quality assets. Mid-size syndication is thin, and stress bids are unobserved.
5. **Recaps** raise DPI but also default risk. They may move value from ADIC's credit sleeve to its equity sleeve.
6. **Fee opacity.** Company-level fees and broken-deal costs erode "no fee" economics. Audit the vehicles.
7. **Source quality.** HarbourVest and Capital Dynamics figures are ‡ and the Investment Officer data come from a teaser. LCD data are second-hand. FIL numbers are from the NBER working paper (the JFE abstract confirms the direction). ASS β = 2.3 is cited through GKM.

---

## 9. Open questions (ADIC to supply or confirm)
1. **Book census:** positions, sizes, GPs, vintages, sectors, entry leverage, marks and fee terms. Which of the working assumptions (90 × $0.2bn) are wrong?
2. **Rights.** Do ADIC's co-investment agreements allow pledges (REFI), transfers without ROFR (SELL), CV status-quo elections and pre-emptive follow-ons?
3. **History:** dated cash flows and the full memo history (u and f) for bias and hazard estimation, plus ADIC's realised write-off rate.
4. **Deal flow:** offers received, accepted and declined by GP. Is allocation tied to commitment size, and how did flow change when commitments slowed (estimate θ)?
5. **Program cost:** internal cost per $ deployed, against FIL's 0.91% a year.
6. **Policy limits** on single-asset size, per-GP look-through, SPV leverage and co-underwriting or warehousing.
7. **Cross-holdings:** with Private Credit (recap netting) and with the PE group (same company).
8. **Internal transfers:** may the Secondaries group bid for co-investment strips (zero-sum; conflicts)?
9. **Legal:** domicile, tax or Shariah constraints on SPV financing and pledges.
10. **Reference class:** which deal-level dataset to license (Burgiss/MSCI, CEPRES, StepStone SPI, Preqin)?

---

## 10. References
1. Fang, L., Ivashina, V. & Lerner, J. (2015). The disintermediation of financial markets: Direct investing in private equity. *JFE* 116(1):160–178. https://ideas.repec.org/a/eee/jfinec/v116y2015i1p160-178.html ; WP: https://www.nber.org/papers/w19299.pdf
2. Braun, R., Jenkinson, T. & Schemmerl, C. (2020). Adverse selection and the performance of private equity co-investments. *JFE* 136(1):44–62. https://ideas.repec.org/a/eee/jfinec/v136y2020i1p44-62.html ; manuscript: https://ora.ox.ac.uk/objects/uuid:f0b81a82-4ec1-44fc-abce-d5a64bfac082
3. Lerner, J., Mao, J., Schoar, A. & Zhang, N. R. (2022). Investing outside the box: Evidence from alternative vehicles in private equity. *JFE* 143(1):359–380. https://dash.harvard.edu/entities/publication/e3f6e98d-7bcd-45a7-a12f-968964c16f5d ; WP: https://www.nber.org/papers/w24941.pdf
4. Braun, R., Jenkinson, T. & Stoff, I. (2017). How persistent is private equity performance? Evidence from deal-level data. *JFE* 123(2):273–291. https://ideas.repec.org/a/eee/jfinec/v123y2017i2p273-291.html ; https://ora.ox.ac.uk/objects/uuid:2f7bd53d-265e-4c0b-94c2-3f4f540cb694
5. Lopez-de-Silanes, F., Phalippou, L. & Gottschalg, O. (2015). Giants at the Gate: Investment Returns and Diseconomies of Scale in Private Equity. *JFQA* 50(3):377–411. DOI 10.1017/S0022109015000113. https://ideas.repec.org/a/cup/jfinqa/v50y2015i03p377-411_00.html ; WP: https://mpra.ub.uni-muenchen.de/28487
6. Kaplan, S. N. & Strömberg, P. (2008). Leveraged Buyouts and Private Equity. NBER WP 14207 (*JEP* 23(1):121–146, 2009, DOI 10.1257/jep.23.1.121). https://www.nber.org/papers/w14207
7. Gompers, P., Kaplan, S. N. & Mukharlyamov, V. (2016). What do private equity firms say they do? *JFE* 121(3):449–476. https://www.nber.org/papers/w21133 ; draft: https://www2.nber.org/conferences/2015/PRs15/Gompers_Kaplan_Mukharlyamov.pdf
8. Bhardwaj, A., Gupta, A. & Howell, S. T. (2025). Capital Structure & Firm Outcomes: Evidence from Dividend Recapitalizations in Private Equity. NBER WP 33435. https://www.nber.org/papers/w33435
9. Bain & Company (Feb 2026). Global Private Equity Report 2026: "Welcome to a new era" and "Outlook: gaining traction". https://www.bain.com/insights/welcome-to-a-new-era-global-private-equity-report-2026/ ; https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/
10. Bain & Company (8 Jun 2026). Midyear PE report press release. https://www.prnewswire.com/news-releases/winning-firms-will-focus-on-what-they-can-control-weather-the-rest-as-triple-shock-brakes-private-equitys-latest-revival-bain--company-2026-midyear-pe-report-302793107.html
11. Jefferies (Jul 2026). Global Secondary Market Review. https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf
12. Evercore (Jul 2026). H1 2026 Secondary Market Review. https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf
13. Lazard (2026). Interim Secondary Market Report 2026. https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf
14. Proskauer (2026). Insights on the NAV Financing Market, Full Year 2025. https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025
15. Rede Partners (Jun 2026). Rede NAV 2026. https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026
16. ILPA (May 2023). Continuation Funds: Considerations for LPs and GPs. https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf
17. SEC (29 Jun 2015). KKR charged with misallocating broken deal expenses (2015-131). https://www.sec.gov/news/pressrelease/2015-131.html
18. Lowe, J. & Gertner, O. (Sidley Austin) (3 Oct 2025). Compelling case for co-investment. *Law Gazette*. https://www.lawgazette.co.uk/practice-points/compelling-case-for-co-investment/5124667.article
19. Appotive, B., Clarkin, M. & Stauder, S. (Torys) (23 Jul 2026). When "No Fee" Means "Yes Fee". https://www.mondaq.com/unitedstates/fund-management-reits/1821370/when-no-fee-means-yes-fee-the-hidden-costs-of-co-investing
20. Investment Officer (27 Feb 2026). Co-Investment Evolves From Fee Break to Strategic Capital Solution (teaser). https://www.investmentofficer.lu/en/analyse/document/22508
21. Capstone Partners (26 Jun 2026). Dividend recapitalizations and solvency opinions (PitchBook LCD data). https://www.capstonepartners.com/?p=25403
22. ABF Journal (Dec 2025). The Dividend Recap Surge (PitchBook LCD data). https://www.abfjournal.com/the-dividend-recap-surge-what-record-sponsor-payouts-reveal-about-the-exit-impasse/
23. IFR (2025). Europe High-Yield Bond: Verisure Holdco's €1bn PIK notes. https://www.ifre.com/ifr-awards/2332504/europe-high-yield-bond-verisure-holdcos-1bn-pik-notes
24. Knapp, M. et al. (Freshfields) (14 Nov 2025). Holding the line: holdco capital solutions. *GRR*. https://globalrestructuringreview.com/review/restructuring-review-of-the-americas/2026/article/holding-the-line-how-documentary-protections-are-shaping-investor-risk-in-the-era-of-holdco-capital-solutions
25. Hamilton Lane (23 Jul 2024). Why Middle-Market Co-Investment Opportunities Make Sense Now. https://hamiltonlane.com/en-us/insight/middle-market-co-investments
26. PEI Secondaries Investor (1 Apr 2014). Altius: co-investments can influence GPs' risk. https://www.pei-secondariesinvestor.com/altius-co-investments-can-influence-gps-risk/
27. ‡ HarbourVest co-investment Monte Carlo (search summary; page not retrievable): https://www.harbourvest.com/?p=11461 . ‡ Capital Dynamics, Co-investments: intelligent portfolio construction over market cycles (403): https://www.capdyn.com/Customer-Content/www/news/PDFs/Capital_Dynamics_Co-investments_intelligent_portfolio_construction_over_market_cycles_.pdf
28. Sibling dossiers (ADIC lab, 2026-10-18): 04 PE cash flows (MSCI, PitchBook and regime table); 05 secondaries and NAV finance; 07 return fusion; 08 action valuation; 01 MPO (SOFR 3.89%, FRED 2026-10-15). Path: `research/dossiers/`.
29. ADIC prior deck v8, slide 8: memo-corpus lessons (context file §2).
30. Axelson, U., Jenkinson, T., Strömberg, P. & Weisbach, M. S. (2013). Borrow Cheap, Buy High? The Determinants of Leverage and Pricing in Buyouts. *JF* 68(6):2223–2267. DOI 10.1111/jofi.12082. Cited in §6.3 via GKM (added 2026-10-18).
31. Axelson, U., Sorensen, M. & Strömberg, P. (2014). Alpha and Beta of Buyout Deals: A Jump CAPM for Long-Term Illiquid Investments. Preliminary draft, November 2014; unpublished working paper, no DOI. https://personal.lse.ac.uk/axelson/ulf_files/alpha%20and%20beta%201.pdf . The draft reports a gross deal-level beta of 2.2–2.4; it is the source of the β = 2.3 that GKM cite (§4.1, §8; added 2026-10-18).
32. Broadie, M., Glasserman, P. & Kou, S. (1997). A Continuity Correction for Discrete Barrier Options. *Mathematical Finance* 7(4):325–349. DOI 10.1111/1467-9965.00035. Cited in the §7 barrier pitfall (added 2026-10-18).

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.4 items 1–3; `research/literature/G4_coinvest.lit.md` §2; `research/groups/addenda/G4_barrier_rerun/RESULTS.md`. New metadata was confirmed on Crossref or OpenAlex, and ref 31 against the draft PDF.

- §7 pitfall: the Broadie–Glasserman–Kou shift changed from barrier × $e^{-0.5826\sigma\sqrt\Delta}$ ("or simulate monthly") to $\kappa D\,e^{+0.5826\sigma\sqrt\Delta}$ toward the current value (σ = diffusive EV volatility), or weekly or finer steps; BGK's own minus-shift use explained.
- §6.3 book simulation: write-off rate per position-year 2.5% / 2.1% → 3.3% / 2.8% (BGK-corrected quarterly check; continuous check 3.1% / 2.7%), with a † note.
- §6.3 book simulation: normal-start 3-year net cash flow P90 +$11.4bn → +$11.3bn.
- §6.3 book simulation: NAV gap −18.5 / −3.5 / +21.9% and −18.7 / −3.0 / +19.2% → −18.5 / −3.6 / +21.5% and −18.8 / −3.1 / +19.3%.
- §6.8 item 9: simulated write-off rate "2–2.5% a year" → "≈2.8–3.3% a year".
- Header, Reproducibility bullet: the † cells are now attributed to the BGK re-run script.
- §6.5 LEVER: P(residual = 0) of 11.8% / 22.8% labelled "at exit" and unchanged by the barrier fix; E3-barrier sensitivity (11.8% / 22.9%) added.
- §1 item 7: Bhardwaj–Gupta–Howell "raise distress probability 2.4× its mean" → an increment of 2.4 times the mean for +84% debt (IV; OLS ≈0.4 times), about ×1.1–×1.7 at φ = 0.25.
- §4.1 table, Bhardwaj–Gupta–Howell row: "Distress probability ×2.4 the target-firm mean" reworded as an increment tied to the +84% debt increase, with the OLS estimate.
- §6.2 E5: "target ×2.4 on the distress mean [S]" → multiplier ×1.1 (OLS) to ×1.7 (IV) at φ = 0.25 [I].
- §4.2 Size: Lopez-de-Silanes et al. marked as not deal-size evidence (their scale is the number of simultaneous investments).
- §4.1 table, Lopez-de-Silanes et al. row: "scale" defined as the PE firm's number of simultaneous investments.
- §10 ref 5: full title "Giants at the Gate: Investment Returns and Diseconomies of Scale in Private Equity" and DOI 10.1017/S0022109015000113 added.
- §10 ref 6: *JEP* pages 121–146 and DOI 10.1257/jep.23.1.121 added.
- §10 ref 30 added: Axelson, Jenkinson, Strömberg & Weisbach (2013), *JF* 68(6):2223–2267, DOI 10.1111/jofi.12082.
- §10 ref 31 added: Axelson, Sorensen & Strömberg (2014), preliminary draft, the source of β = 2.3.
- §10 ref 32 added: Broadie, Glasserman & Kou (1997), *Mathematical Finance* 7(4):325–349, DOI 10.1111/1467-9965.00035.
- Not changed: the "29–37%" REFI breach and "12% to 23%" LEVER figures (§1 item 8, §6.5) are not barrier statistics. They remain open under verification R2 and R3.
