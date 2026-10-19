# Verification log: Stream 11, objective design (`dossiers/11_objectives.md`)

**Verifier:** adversarial fact-check agent. **Date:** 2026-10-18. **Dossier version checked:** 627 lines, "As of 2026-10-18".

**Method:**
- All 20 claims the author flagged were checked, plus 10 further load-bearing claims (30 in total), against the primary page or document wherever one was reachable.
- PDFs were downloaded, their text extracted locally with `pypdf`, then searched. They were:
  - Nielsen (2013);
  - Busseti, Ryu & Boyd (2016);
  - the Rockafellar & Uryasev (2000) draft;
  - the Long, Sim & Zhou preprint;
  - the Dybvig (1998) draft;
  - Föllmer & Leukert (2000);
  - the J.P. Morgan 2026 LTCMA USD assumption matrix.
- Bibliographic metadata for 40+ references (title, authors, venue, volume/issue/pages, year) came from the Crossref API, arXiv and RePEc.
- I recomputed every [I] quantitative claim in §1, §2.3, §2.5, §3.2(a), (b), (d) and §6.5 in closed form (scipy).
- I stress-tested the C3 drawdown constraint in closed form and with a 200,000-path Monte Carlo.
- Scripts are in the session scratchpad:
  - `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\v11\scripts\check_numbers.py`
  - `...\scratchpad\v11\scripts\scen_n.py`

**Process caveats:**
- **Browne (1999).** Cambridge Core returned 403. I checked the abstract through search-indexed copies (Cambridge, Columbia, RePEc), Crossref metadata and Nielsen's restatement.
- **Solvency II.** I did not fetch EUR-Lex directly. Art. 101(3) was checked against EIOPA's Solvency II rulebook text and the PRA's restatement.
- **CPP 55/45 and the triennial review.** These were confirmed from search-index excerpts of CPP Investments' own documents (Investment Statement, annual report), not from a full page fetch.
- **Toy scripts.** I did not re-run `s11_*.py`. Toy outputs in §3.2(c) and (e) were checked only for internal consistency.

---

## 1. Summary

- **Facts: strong.** Of 30 load-bearing claims: **28 confirmed, 2 corrected, 0 refuted, 0 unverifiable.**
  - Every market, peer and regulatory figure flagged high-confidence matches its primary source, mostly to the decimal. Sources: MSCI (both charts), NACUBO-Commonfund (via ai-CIO and NACUBO), TIFF, J.P. Morgan, the Harvard Crimson, APFC, Yale, BIS, EIOPA, DNB, IPE and CPP.
  - Every attribution to a paper matches the paper's own text, including the verbatim quotes:
    - Basak & Shapiro;
    - Busseti et al., eq. (6);
    - Nielsen, eqs. (36)–(37) and the "finitely capped leverage" sentence;
    - Dybvig's riskless-rate proposition and his 10%/30%/3%/4.5% example;
    - Long, Sim & Zhou, eq. (6);
    - Rockafellar & Uryasev;
    - Föllmer & Leukert's "dynamic version of the static Value at Risk concept".
  - **Correction 1, return convention.** The J.P. Morgan 2026 LTCMA headline numbers are **compound (geometric)** returns, per the USD matrix. The derived claim that a 60% private / 40% liquid mix "lands near 8.5–9% arithmetic" is therefore mislabeled. It is ≈8.9% compound, or ≈10.5% arithmetic.
  - **Correction 2, Yale rule.** The dossier's version of Yale's spending rule is the simplified web-page version. Yale's formal policy adds a lagged market value, an inflation adjustment and a 4.0–6.5% collar.
- **Arithmetic: reproducible.** Every recomputed [I] number matches:
  - floor table (d), to within 0.05pp;
  - the 31–49% range;
  - the payout identity;
  - Browne P* of 90.4 / 94.2 / 96.9%;
  - table (a);
  - Kelly leverage of 3.1×;
  - the C4 binding σ of ≈14.35%;
  - the scenario-approach sample sizes N. These correspond to β = 10⁻⁶, which the dossier does not state.
- **Citations: clean.** All 12 core references, plus about 30 more, exist with correct authors, year, title and venue. I found no hallucinated or garbled citations.
  - Föllmer & Leukert (2000) is used in the text but missing from §10.
  - Several incomplete entries can now be completed (Section 3).
- **Reasoning: this is where the risk is.**
  - **R1 (high). The recommended C3 real-drawdown constraint is infeasible.** It gives an empty feasible set at every payout in the 5–10% band under the dossier's own return assumptions. Two reasons:
    - The risk-constrained Kelly (RCK) bound needs E ln G > 0 (in fact E ln G ≥ λs²/2 ≈ 5.1%/yr). G here is real growth net of distributions, which has roughly zero or negative drift.
    - The underlying target itself is out of reach. The probability of real NAV ever falling below 70% of start within 10 years is ≈24% at d=5% and ≈50% at d=7.5%, against the 5% default.
  - **R2 (medium). "Drawdown" is mislabeled.** RCK bounds an infinite-horizon fall below *initial* wealth, not peak-to-trough drawdown.
  - **R3 (medium).** The calibration confuses compound and arithmetic returns and understates risk relative to its stated anchor, J.P. Morgan.
  - **R4 (medium).** The "~7% sustainable payout" assumes the 10% geometric target is actually achieved. Under the dossier's own CMAs the figure is ≈5–6%.
  - **R5 (medium).** The claim that the program is conic fails for the time-weighted-return (TWR) based shortfall term.
  - **R6 (low–medium).** Euler additivity does not hold for the C1 path-maximum deficit.
  - **R7–R15.** Smaller issues.
- **Overall reliability:**
  - **HIGH** for sourced facts, citations and arithmetic.
  - **MEDIUM** for the design implications.
  - **Overall: MEDIUM.**
  - Fix R1–R5 before IC use. R1 sits in the recommended default parameter table.

---

## 2. Claims table

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | Browne (1999, AAP 31(2):551–577): maximizing P(reach goal by deadline) is equivalent to buying a European digital option. In the multi-asset case the log-optimal portfolio replaces the stock. | **Confirmed** | Abstract: "equivalent to simply buying a European digital option". The general case replaces the stock with the log-optimal (growth-optimal) portfolio. Crossref metadata matches. | https://doi.org/10.1239/aap/1029955147 ; https://ideas.repec.org/p/fth/colubu/96-16.html |
| 2 | Nielsen restates Browne: J=Φ(Φ⁻¹(π/b)+((μ−r)/σ)√(T−t)); the risky fraction diverges as t→T; "A strategy with finitely capped leverage would have J(π,T) = 0 for π < b." | **Confirmed** (clarify) | §V.C, eqs. (36)–(37) and the quote are verbatim. Nielsen's π is the **discounted** relative portfolio value π_t = P_t e^{−rt}/P_0, and b is a "real return target" in those units. J→π/b as t→T. | https://arxiv.org/abs/1311.2550 |
| 3 | Basak & Shapiro (2001): VaR managers often choose a larger risky exposure and incur larger losses when losses occur. They propose an expected-loss alternative. | **Confirmed** | Abstract verbatim. The alternative is "based on the expectation of a loss". *RFS* 14(2):371–405. | https://ideas.repec.org/a/oup/rfinst/v14y2001i2p371-405.html |
| 4 | Busseti, Ryu & Boyd (2016): E[(rᵀb)^−λ] ≤ 1 with λ = log β / log α implies Prob(W_min < α) < β, giving a convex risk-constrained Kelly problem. | **Confirmed** (scope) | Eq. (6) and the §5 convexity proof are verbatim. Scope: IID returns. W_min = inf over t=1,2,… (infinite horizon), measured against **initial** wealth, not a running peak. The paper assumes E log(rᵀb) > 0. λ = ln 0.05 / ln 0.7 = 8.399 ✓. See R1–R2. | https://arxiv.org/abs/1603.06183 |
| 5 | Rockafellar & Uryasev (2000): CVaR can be optimized by LP on scenarios; β-VaR never exceeds β-CVaR, so low-CVaR portfolios have low VaR. | **Confirmed** | Verbatim: "the β-VaR is never more than the β-CVaR, so portfolios with low CVaR must have low VaR as well"; the scenario problem "can even reduce to linear programming". *J. Risk* 2(3):21–41 (Crossref). | https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf |
| 6 | Long, Sim & Zhou (2023, OR 71(1)): robust satisficing, min k s.t. E_P[f]−τ ≤ k·Δ(P,P̂) ∀P, with τ ≥ Z₀. It minimizes fragility and improves out-of-sample performance (optimizer's curse). | **Confirmed** | Preprint eq. (6), with "τ≥Z0" and "minimizes the fragility of the system" verbatim. The abstract covers out-of-sample gains and alleviating the Optimizer's Curse. *OR* 71(1):61–82 (Crossref). | https://iora.nus.edu.sg/wp-content/uploads/2022/02/SSRN-id3478930.pdf |
| 7 | Dybvig (1998 draft / FAJ 1999): spending above endowment × riskless rate cannot be guaranteed in perpetuity; risky holding = K(w−s/r); with a 10% mean, 30% sd, 3% inflation and 4.5% spending, real value → 0 a.s. | **Confirmed** | Draft dated 30 Oct 1998. The proposition, Table 1 (α_t = K(w_t − s_t/r), s_t ≥ r*w_t) and the footnote example are all verbatim. Note that r is the riskless rate, "presumably the excess over inflation". *FAJ* 55(1):49–62 (Crossref). | https://phildybvig.com/research/papers/ratchet2p.pdf |
| 8 | Browne (1997, Math OR 22(2)): with fixed withdrawals the state space splits into a "danger zone" and a "safe region". | **Confirmed** | Abstract: ruin is possible in the "danger-zone" and avoidable with certainty in the "safe-region". *MOR* 22(2):468–493 (Crossref). | https://doi.org/10.1287/moor.22.2.468 |
| 9 | MSCI (2026-06-11): closed-end PE returned 12% of asset value in 2025, just over half the ~20% 20-year average. Distributions near decade lows for four straight years. | **Confirmed** | Dated June 11, 2026. Data through Q4 2025 (May 2026 update). Quote: "The 20-year average is roughly 20%". | https://www.msci.com/data-and-analytics/private-asset-solutions/visualizations/the-distribution-drought-in-private-equity-persists |
| 10 | MSCI (2026-10-13): buyout distribution rate 12% in H1-2026 (15% in 2025) vs ~27% historical. Top-quartile exit multiple 18.2× EBITDA, a series high. Net cash flow +USD 21bn. | **Confirmed** | All figures verbatim. The series high is "back to 2016". Median multiple 12.5×. | https://www.msci.com/data-and-analytics/private-asset-solutions/visualizations/the-best-exit-pricing-in-a-decade-and-lps-are-still-waiting-for-cash |
| 11 | NACUBO-Commonfund FY2025 (published 2026-02-12): average 10.9%; 10-yr 7.7% (6.8% the prior year); 20-yr 7.3%; 25-yr 6.6%. | **Confirmed** | ai-CIO also gives 3y 10.0%, 5y 10.2%, 15y 8.5%, 657 institutions, $944.3bn and 15.2% of operating budgets. The FY2024 figure of 6.8% is not in the ai-CIO piece. It is confirmed by NACUBO's Feb-2025 release (658 institutions, $873.7bn). | https://www.ai-cio.com/news/turbulent-year-university-endowments-report-average-return/ ; https://www.nacubo.org/Press-Releases/2025/US-Higher-Education-Endowments-Report-10-Year-Average-Annual-Return |
| 12 | J.P. Morgan 2026 LTCMA (released 2025-10-20): USD 60/40 6.4%; with 30% alternatives 6.9%; global equities 7.0%; US large cap 6.7%; PE 10.2%; IG credit 5.2%. | **Confirmed** (convention note) | The press release states these verbatim, plus US core RE 8.2%, intermediate Treasuries 4.0% and HY 6.1%. **The USD matrix shows these are compound returns**, with arithmetic return and volatility as follows: PE 11.91% / 19.78%; ACWI 8.28% / 16.78%; US large cap 7.94% / 16.47%; IG 5.46% / 7.39%. US inflation 2.50%, cash 3.10%. | https://am.jpmorgan.com/us/en/asset-management/adv/about-us/media/press-releases/jp-morgan-releases-2026-long-term-capital-market-assumptions/ ; https://am.jpmorgan.com/content/dam/jpm-am-aem/global/en/insights/ltcma-2026-us-matrix_usd.pdf |
| 13 | April 2025: Harvard in talks to sell ~$1bn of PE stakes (~5% of the PE book; PE ~40% of a $53bn endowment). It borrowed $1.2bn via two bond sales as contingency planning. Yale was considering a sale. | **Confirmed** | Crimson: "nearly $1 billion" to Lexington Partners; "nearly 5 percent"; "nearly 40 percent of its $53 billion endowment"; bond sales in March and April; "part of ongoing contingency planning"; Yale's announcement; Longo's discount quote. | https://www.thecrimson.com/article/2025/4/25/private-equity-stake-sales/ |
| 14 | Solvency II Art. 101(3): SCR = VaR of basic own funds at 99.5% over one year. | **Confirmed** | EIOPA rulebook Art. 101: "99,5 % over a one-year period". The PRA restates the same rule. | https://www.eiopa.europa.eu/rulebook/solvency-ii/article-2188_en |
| 15 | Basel III LCR: HQLA for a 30-calendar-day stress; 100% minimum from 1 Jan 2019. | **Confirmed** | BIS page, published 7 Jan 2013. Phased in since 2015. | https://www.bis.org/publ/bcbs238.htm |
| 16 | Alaska POMV: draw capped at 5.0% of average market value over the first five of the preceding six fiscal years. FY28 draw $4.1bn; more than 66% of general fund revenue. | **Confirmed** | APFC: FY28 draw $4.1bn on a 5-year average of $81.9bn (FY27: $3.997bn). Quote: "more than 66% of the state's general fund revenue". | https://apfc.org/the-fund/ |
| 17 | Yale rule: spending = 0.80 × last year's spending + 0.20 × (5.25% × endowment value); "creates a cushion…". | **Corrected** (incomplete) | The cited overview page says exactly this, including the quote. Yale's **formal policy** (§2202.1, revised 2026-07-01) is fuller: payout = [0.80 × prior-year spending + 0.20 × (5.25% × previous year's *beginning* endowment market value)], **adjusted for inflation**, and **constrained to 4.0%–6.5%** of fair value at the start of the prior year. Use the formal rule if Yale serves as a C6 template. | https://www.yale.edu/funding-yale-home/overview-yales-endowment ; https://your.yale.edu/policies-procedures/2202-endowment-spending-and-distributions |
| 18 | Ang, Papanikolaou & Westerfield: illiquidity brings increased, state-dependent risk aversion; investors would give up ~2% of wealth to hedge once-a-decade illiquidity crises. | **Confirmed** | NBER abstract verbatim: "forego 2% of their wealth to hedge against illiquidity crises occurring once every ten years". *Management Science* 60(11):2737–2761 (2014). | https://www.nber.org/papers/w19436 |
| 19 | Brown, Dimmock, Kang & Weisbenner (2014): payouts are cut below policy after negative shocks but not raised after positive shocks ("endowment hoarding"). | **Confirmed** | AER abstract verbatim. *AER* 104(3):931–962. | https://www.aeaweb.org/articles?id=10.1257/aer.104.3.931 |
| 20 | Own computation: the 7%/5y/95% floor needs log-vol ≤3.8% at a 10% median (≤5.7% at 11.6%). P(5y annualized < 7%) ≈31–49% for 8.5–10% expected return at 11–17% vol. | **Confirmed** | Recomputed: 3.76% and 5.72%. The range runs from 30.6% (10%, 11% vol) to 49.0% (8.5%, 17% vol). All of table (d) is reproduced exactly. | own computation (check_numbers.py) |
| 21 | §1: "A 60% private / 40% liquid mix therefore lands near 8.5–9% *arithmetic*." §3.2(a): μ₀=8.5% arithmetic, σ₀=12% "consistent with JPM-style CMAs for a 60% PE mix". | **Corrected** | J.P. Morgan's figures are compound, so 0.6×10.2 + 0.4×(6.4–7.0) = 8.7–8.9% is a **compound** blend. Using J.P. Morgan's arithmetic returns, vols and ρ(PE, ACWI)=0.81, a 60% PE / 40% ACWI mix has ≈10.5% arithmetic return, ≈17.7% vol and a ≈9.1% median (geometric). That gives P(10y ≥ 10%) ≈43%, against the dossier's 30–40% (its base gives 28.5%), and P(5y < 7%) ≈39.5%. The Sharpe ratio is similar (≈0.41 vs 0.42), but the level and the volatility are not. | https://am.jpmorgan.com/content/dam/jpm-am-aem/global/en/insights/ltcma-2026-us-matrix_usd.pdf |
| 22 | CPP: 85/15 global equity / Canadian bond Reference Portfolio; 55/45 for the additional CPP; triennial review. | **Confirmed** | CRR (2024-09-25) confirms 85/15. CPP Investments documents confirm 55/45 for the additional CPP ("greater sensitivity to shortfalls") and a review every three years, after the Chief Actuary's triennial report. The dossier's "not retrievable" caveat can be removed. | https://crr.bc.edu/canada-pension-plan-fall-short-of-indexed-benchmark/ ; https://www.cppinvestments.com/wp-content/uploads/2025/04/InvestmentStatement-InvestmentPortfolio-EN-Apr022025.pdf |
| 23 | Dutch FTK: 97.5%, "once-in-40-year" (IPE 2004). FTK funds averaged 131.4% in Q2-2026, with transition due by 2028-01-01 (DNB). | **Confirmed** | IPE (2004-10-25) does **not** state a horizon, so the dossier's "secondary sources describe as one-year" hedge is appropriate. DNB (2026-07-28): 131.4%, up 6.6pp. | https://ipe.com/dutch-regulator-unveils-supervisory-framework/9992.article ; https://www.dnb.nl/en/general-news/news-2026/pension-transition-and-pension-fund-funding-ratios-2026q2/ |
| 24 | TIFF: the $5bn+ cohort averaged 11.8% in FY2025; top concerns are "federal funding cuts and liquidity"; endowments funded 15.2% of operating budgets. | **Confirmed** | TIFF, 2026-02-17. All three items verbatim. | https://www.tiff.org/fy2025-nacubo-results-show-strong-returns-but-rising-pressures-on-institutions-budgets/ |
| 25 | Yale FY2025: 11.1% return; 10-year 9.4% p.a.; $15.3bn spent over 10 years (60% of starting value). | **Confirmed** | Yale News, 2025-10-24. Endowment $44.1bn. | https://news.yale.edu/2025/10/24/yale-reports-investment-return-fiscal-2025 |
| 26 | Föllmer & Leukert's follow-up calls quantile hedging a dynamic VaR that ignores shortfall size, and replaces it with loss-weighted expected shortfall. | **Confirmed** (citation gap) | Föllmer & Leukert (2000), "Efficient hedging: cost versus shortfall risk", *F&S* 4(2):117–146, introduction verbatim. **Not listed in §10.** | https://www2.mathematik.hu-berlin.de/~foellmer/papers/hedges_57.pdf |
| 27 | Chen & Sim (2009): the model "maximizes the shortfall-aware aspiration-level criterion" and reduces to CVaR LPs, or SOCP under robust decision rules. | **Confirmed** | Abstract excerpts. *OR* 57(2):342–357. | https://ideas.repec.org/a/inm/oropre/v57y2009i2p342-357.html |
| 28 | Boyd et al. (2017): a trade sequence is planned and "only the first one executed". | **Confirmed** | arXiv abstract verbatim. | https://arxiv.org/abs/1705.00109 |
| 29 | Das et al. GBWM (MathWorks): at low wealth the higher-return portfolio is chosen "even at the cost of increasing the volatility"; near the horizon choices polarize. | **Confirmed** | MathWorks page verbatim. Journal version: *Computational Management Science* 17(4):613–640 (2020), which resolves the dossier's ⚠. | https://www.mathworks.com/help/finance/dynamic-portfolio-allocation-in-gbwm-for-multiple-periods.html ; https://doi.org/10.1007/s10287-019-00351-7 |
| 30 | Other [I] numbers, all reproduced (details below the table). | **Confirmed** | Browne P* uses r = ln 1.035. The N values correspond to β = 10⁻⁶, which the dossier does not state (R8). | own computation |

Row 30 covers:
- Browne P* of 90.4 / 94.2 / 96.9%;
- table (a);
- Kelly leverage of 3.1×;
- C4 binding at σ≈14.3% (CVaR₁₀ of +1.5% / −1.7%);
- scenario-approach N of 3,260 / 9,086 / 27,418 / 1,801;
- the per-year translations ε/H and 1−(1−ε)^{1/H};
- the relative standard error of 4.5%;
- the payout identity (6.8 / 7.9 / 10.8 / 13.9%).

---

## 3. Citation check

### 3.1 The 12 most important references

| # | Reference as cited | Verified metadata (source) | Status |
|---|---|---|---|
| 1 | Browne (1999), *Adv. Appl. Probab.* 31(2):551–577 | Sid Browne, "Reaching goals by a deadline: digital options and continuous-time active portfolio management", AAP 31(2):551–577, 1999 (Crossref) | ✓ Correct |
| 2 | Browne (1997), *Math. OR* 22(2):468–493 | "Survival and Growth with a Liability: Optimal Portfolio Strategies in Continuous Time", MOR 22(2):468–493, 1997 (Crossref) | ✓ Correct |
| 3 | Nielsen (2013), arXiv:1311.2550 | Mads Nielsen (sole author), "The Kelly growth optimal strategy with a stop-loss rule", v1 11 Nov 2013 (arXiv) | ✓ Correct. It is a secondary restatement of Browne in §V.C, so cite Browne as the primary source. |
| 4 | Basak & Shapiro (2001), *RFS* 14(2):371–405 | "Value-at-Risk-Based Risk Management: Optimal Policies and Asset Prices", RFS 14(2):371–405, 2001 (Crossref) | ✓ Correct |
| 5 | Busseti, Ryu & Boyd (2016), arXiv:1603.06183 | "Risk-Constrained Kelly Gambling", submitted 20 Mar 2016 (arXiv) | ✓ Correct |
| 6 | Rockafellar & Uryasev (2000), *J. Risk* 2(3), "details from memory" | "Optimization of conditional value-at-risk", J. Risk 2(3):**21–41**, 2000 (Crossref) | ✓ Correct. Add the pages. |
| 7 | Long, Sim & Zhou (2023), *OR* 71(1):61–82 | "Robust Satisficing", OR 71(1):61–82, 2023 (Crossref) | ✓ Correct |
| 8 | Dybvig (1999), *FAJ* 55(1):49–62 | "Using Asset Allocation to Protect Spending", FAJ 55(1):49–62, 1999 (Crossref) | ✓ Correct |
| 9 | Chen & Sim (2009), *OR* 57(2):342–357 | "Goal-Driven Optimization", OR 57(2):342–357, 2009 (Crossref) | ✓ Correct |
| 10 | Fishburn (1977), *AER* 67(2):116–126 | "Mean-Risk Analysis with Risk Associated with Below-Target Returns", AER 67(2):116–126, Mar 1977 (RePEc) | ✓ Correct. No abstract is online. The α<1 risk-seeking reading is confirmed via secondary literature. |
| 11 | Ang, Papanikolaou & Westerfield (2014), *Management Science* (no vol./pp.) | "Portfolio Choice with Illiquid Assets", MS **60(11):2737–2761**, 2014 (Crossref) | ✓ Correct. Add vol./pp. |
| 12 | Brown, Dimmock, Kang & Weisbenner (2014), *AER* 104(3):931–962 | "How University Endowments Respond to Financial Market Shocks: Evidence and Implications", AER 104(3):931–962 (Crossref) | ✓ Correct. Short title acceptable. |

### 3.2 Further references, all correct

All of these match Crossref, arXiv or RePEc on authors, title, venue, volume/issue/pages and year.

**Risk measures, chance constraints and scenario methods**
- Shapiro (2009), *ORL* 37(3):143–147
- Nemirovski & Shapiro, *SIAM J. Optim.* 17(4):969–996 (Crossref year 2007)
- Campi & Garatti (2008), *SIAM J. Optim.* 19(3):1211–1230
- Calafiore & Campi (2006), *IEEE TAC* 51(5):742–753
- Rockafellar & Uryasev (2002), *JBF* 26(7):1443–1471
- Artzner, Delbaen, Eber & Heath (1999), *Math. Finance* 9(3):203–228
- Chekhlov, Uryasev & Zabarankin (2005), *IJTAF* 8(1):13–58
- Charnes & Cooper (1959), *MS* 6(1):73–79
- Roy (1952), *Econometrica* 20(3):431–449
- Leibowitz & Henriksson (1989), *FAJ* 45(2):34–41

**Robustness and model uncertainty**
- Mohajerin Esfahani & Kuhn (2018), *Math. Prog.* 171(1–2):115–166
- Brown & Sim (2009), *MS* 55(1):71–84. The abstract confirms "dual to classes of risk measures" and the ambiguity interpretation.
- Hansen & Sargent (2001), *AER* 91(2):60–66
- Glasserman & Xu (2014), *QF* 14(1):29–58

**Multistage and dynamic programming**
- Ruszczyński & Shapiro (2006), *MOR* 31(3):544–561
- Ruszczyński (2010), *Math. Prog.* 125(2):235–261
- Pereira & Pinto (1991), *Math. Prog.* 52:359–375
- Philpott & de Matos (2012), *EJOR* 218(2):470–483

**Portfolio choice, hedging and goals**
- Grossman & Zhou (1993), *Math. Finance* 3(3):241–276
- Föllmer & Leukert (1999), *F&S* 3(3):251–273
- Browne (1999), *F&S* 3(3):275–294
- Das, Markowitz, Scheid & Statman (2010), *JFQA* 45(2):311–334
- Dybvig (1995), *RES* 62(2):287–313
- Kelly (1956), *BSTJ* 35(4):917–926
- Kahneman & Tversky (1979), *Econometrica* 47(2):263–291

**Actuarial, endowment and illiquidity**
- Gerber & Shiu (1998), *NAAJ* 2(1):48–72
- Avanzi (2009), *NAAJ* 13(2):217–251
- Gourier, Phalippou & Westerfield (2024), *JF* 79(5):3407–3457
- Tobin (1974), *AER* 64(2):427–432

**Control**
- Abate, Prandini, Lygeros & Sastry (2008), *Automatica* 44(11):2724–2734
- Wabersich & Zeilinger, arXiv:1812.05506
- Ames, Coogan, Egerstedt, Notomista, Sreenath & Tabuada, arXiv:1903.11199
- Boyd et al. (2017), arXiv:1705.00109

**Not independently checked** (none is load-bearing):
- Constantinides (1990);
- Merton (1993);
- Tasche (2007), arXiv:0708.2542;
- the items the dossier itself marks ⚠ (Cvitanić & Karatzas; Brunel).

### 3.3 Citation hygiene items

1. **Missing reference.** Föllmer & Leukert (2000), *F&S* 4(2):117–146, is quoted in §2.1 as "their follow-up" but is absent from §10.
2. **Surname.** "Esfahani, P.M." should read **Mohajerin Esfahani, P.** Long, Sim & Zhou themselves cite "Mohajerin Esfahani and Kuhn 2018".
3. **Incomplete entries to fill:**
   - Rockafellar & Uryasev (2000), pp. 21–41;
   - Ang, Papanikolaou & Westerfield (2014), 60(11):2737–2761;
   - Das et al. (2020), *CMS* 17(4):613–640, replacing the ⚠;
   - the CPP 55/45 and triennial-review facts are now sourced (row 22).

---

## 4. Reasoning issues and overclaims

### R1 (HIGH): The C3 real-drawdown constraint is infeasible as specified

**Where:** §1 parameter table ("Real drawdown ≤ 30% with ≥ 95% probability over 10y (λ=8.4)"), §1 (C3), §2.3, §6.4 (C3) and §6.5.

**What the dossier does.** It imposes E[G_t^{−λ}] ≤ 1 with λ = 8.40, where G_t = (1+R_t)(1−d_t)/(1+π_t) is **real growth net of distributions**.

**Why that cannot work.**
- Busseti et al. derive the bound for IID returns over an **infinite** horizon and assume E log G > 0 (their §3).
- Jensen's inequality gives E[G^{−λ}] ≥ exp(−λ E ln G). So E[G^{−λ}] ≤ 1 *requires* E ln G ≥ 0.
- Under lognormality it requires E ln G ≥ λs²/2.

**Numbers under the dossier's own base calibration** (8.5% arithmetic, 12% vol, 2.5% inflation):
- The constraint needs **E ln G ≥ 5.11%/yr** of real growth net of payout.
- Actual E ln G is −0.05%/yr at d=5%, −2.72%/yr at d=7.5% and −5.46%/yr at d=10%.
- So E[G^{−8.4}] = **1.54 / 1.93 / 2.43**, all above 1.
- No mix of the risky portfolio with 3.5% cash is feasible even at d=5%. The minimum is 1.31, at 40% risky.
- Under a J.P. Morgan-consistent calibration (≈10.5% arithmetic, 17.7% vol) the values are 2.23 / 2.79 / 3.52.
- **The feasible set is empty for every payout in the 5–10% band.**

**The underlying target is also out of reach, not just the surrogate.**
- In a Monte Carlo with 200k paths, annual steps, 1.0× leverage and the base calibration, P(real NAV < 0.7 W₀ at some point within 10y) is:
  - **23.6% at d=5%**;
  - **49.7% at d=7.5%**;
  - against the 5% default.
- This agrees with the toy ALM's own median real NAV₁₀ of 0.79 at d=7.5%.
- §8's "surrogate conservatism" caveat does not cover this case. The target itself conflicts with the payout band under the dossier's CMAs.

**Fix:**
- (a) Apply the drawdown constraint to NAV **gross of distributions** (investment drawdown), or to real NAV relative to a declining glide path implied by the payout rule.
- (b) When E ln G ≤ 0, use a finite-horizon simulated chance constraint or CDaR instead of the infinite-horizon RCK bound.
- (c) Show the IC the jointly feasible (d, α_DD, β_DD) region explicitly. It is a first-order trade-off and should not be a fixed default.

### R2 (MEDIUM): "Drawdown" is mislabeled

- RCK bounds the probability that wealth **ever falls below α × initial wealth**, measured from the start.
- An IC will read "real drawdown ≤ 30% with ≥ 95% probability over 10y" as **peak-to-trough** drawdown within 10 years. That is a strictly harder event.
- Base-calibration Monte Carlo at d=5%:
  - P(peak-to-trough real drawdown > 30%) = **35.3%**;
  - P(below 70% of start) = 23.6%.
- **Fix:** label C3 as a "real NAV floor at 70% of start" and use the already-listed CDaR for peak-to-trough drawdown.

### R3 (MEDIUM): Return convention and calibration anchor

- J.P. Morgan's 2026 numbers are **compound** (row 12). "≈8.5–9% arithmetic" should read **≈8.9% compound, or ≈10.5% arithmetic**.
- The illustrative base (μ₀ = 8.5% arithmetic, σ₀ = 12%) has J.P. Morgan's Sharpe ratio (≈0.42 vs ≈0.41). It understates **both** the return level and the risk relative to J.P. Morgan:
  - J.P. Morgan's PE volatility is 19.8%;
  - 60% PE / 40% ACWI gives ≈17.7%;
  - it would be lower, in the mid-teens, if the liquid sleeve holds bonds.
- The lower end of the dossier's "11–17% de-smoothed vol" range therefore looks low for ~60% PE.
- **Consequence:** P(10y ≥ 10%) ≈43% under J.P. Morgan-consistent inputs, versus 28.5% under the base. Payout sustainability and floor-breach probabilities shift with it.
- **Fix:**
  - calibrate to J.P. Morgan's arithmetic returns and vols, or label the base explicitly as a haircut;
  - tag every return as arithmetic or geometric.

### R4 (MEDIUM): The sustainable payout is overstated

- Two statements are affected:
  - "Payouts above ~7% of NAV are, in expectation, transfers from future to current owners";
  - the §6.10 calibration target "d* ≈ 6.8%".
- Both assume a **realized 10% geometric return**. The dossier itself puts that at only 30–40% probability.
- Real-NAV-preserving payout under other assumptions:

  | Calibration | Median-preserving payout | Mean-preserving payout |
  |---|---|---|
  | Dossier's own base | ≈4.95% | ≈5.5% |
  | J.P. Morgan-consistent | ≈6.0% | ≈7.2% (arithmetic 10.46%) |

- "In expectation" mixes mean and median preservation.
- **Fix:**
  - present the sustainable payout as a function of the CMA;
  - distinguish mean from median preservation;
  - lead with ≈5–6% under current CMAs.
- This matters directly for the IC's 5–10% payout discussion.

### R5 (MEDIUM): The conic-program claim for (P) does not hold for the TWR shortfall term

- §6.4 says: "Both terms are concave in θ when wealth is affine in θ, so (P) is a power-cone/SOC program." That holds for the CRRA term. It does **not** hold for the target term built on **TWR_H**.
- TWR is a chain-linked product of period returns (W_{t+1}+D_t+flows)/W_t, which are ratios of affine functions. That product is neither affine nor log-concave in θ in general, even when each W_t is affine (for example, dollar holdings in a scenario tree).
- With fraction-based decision rules (L1), wealth itself is multiplicative in θ. The dossier does acknowledge derivative-free search for L1.
- **Fix:** for L2, state the target term on an affine "gross wealth" proxy, for example terminal NAV plus distributions accumulated at fixed rates. Keep the 10-year TWR as a reported KPI.

### R6 (LOW–MEDIUM): Euler additivity is claimed for the C1 deficit

- §6.6 says: "CVaR is positively homogeneous, so Euler allocation gives additive contributions E[L_i | L ≥ VaR] … an asset's contribution to the deficit CVaR in C1 is its liquidity-tail cost."
- The C1 loss is max_t Δ_t, and Δ_t contains **fixed** liabilities: minimum payout, IM floor, debt service and the operating minimum.
- So the loss is neither linear nor degree-1 homogeneous in asset positions. Euler contributions will not sum to the total.
- Marginal contributions and duals are still valid, and they are what §6.6's reduced-cost logic actually uses.
- **Fix:** report marginal contributions and the liability block separately. Do not present them as a full additive decomposition.

### R7 (LOW): The Yale rule is simplified (row 17)

- This matters if Yale serves as the C6 template.
- The 4.0–6.5% collar and the inflation indexation change payout dynamics after drawdowns.
- The 6.5% cap limits the dossier's point that smoothing "can raise the payout rate after declines".

### R8 (LOW): The scenario-approach certificate is mis-sized for L2

- The table omits β. Its N values correspond exactly to β = 10⁻⁶.
- More importantly, §7 L2 uses "5–10k paths" or S = 10⁴ scenarios with affine rules where θ ~ 10²–10³.
- At ε = 1% and β = 10⁻⁶, the scenario approach needs:
  - N ≈ **15,464** for d = 100;
  - N ≈ **115,679** for d = 1,000.
- So L2 frontiers at that size cannot carry a scenario-approach guarantee. They need out-of-sample validation, which the dossier does recommend elsewhere.
- **Fix:** state β, and drop the implied certification for L2.

### R9 (LOW): Notation

- The J(π,t) formula needs the caveat that π is **discounted** wealth (Nielsen's π_t = P_t e^{−rt}/P_0). With r ≠ 0 and nominal wealth it would read Φ(Φ⁻¹(x e^{r(T−t)}/b) + θ√(T−t)). The dossier's later P* formula does this correctly.
- π is also reused for inflation in §2.6.

### R10 (LOW): Internal inconsistencies in reported toy numbers

- §1 gives "34.5% to 67.5%", while table (c) gives 34.1% and 67.6%, and table (a) gives 34%.
- §1 gives "28% (1.0×)", while table (a) gives 29%. The closed form is 28.5%.
- The scripts were not re-run to adjudicate these.

### R11 (LOW): C4 may bind

- C4 binds at σ ≈ 14.3% (i.i.d. lognormal, μ = 8.5%). That is inside the dossier's own 11–17% volatility range.
- Every toy-ALM policy has a 10y q05 ≤ −2.0%, so C4 would likely be violated there too.
- Present C4 to the IC as potentially binding, not as a loose backstop.

### R12 (LOW): Overclaims

- **"P(10%) is the most risk-seeking criterion possible below target."** P(target) is the α = 0 boundary of Fishburn's family. It is not the most risk-seeking criterion conceivable.
- **"Real NAV is preserved iff (1+g)(1−d) = 1+π."** This is a deterministic identity. Under uncertainty the statement needs to say whether it means mean or median preservation.
- **Under rolling MPC "Browne-type explosion cannot occur".** Leverage still pins at the cap when behind if an indicator objective is kept. The actual fix is §6.9 rule 1: no indicator terms.

### R13 (LOW): Inert parameter in C2

C2 lists "secondary discount ∈ [25%, 40%]" while forbidding PE secondaries in that test. The parameter does nothing and may confuse readers.

### R14 (LOW): Toy ALM base case is optimistic against its own guidance

- The toy's base PE distribution rate is 17% in normal regimes and 6% in stress. Its stationary average is ≈15.2%.
- That is the top of the dossier's own recommended 10–15% centre (§4, §6.10). Base breach probabilities are therefore optimistic.
- The "drought" variant (12% / 5%) is the better base case.

### R15 (LOW): Citation hygiene

See Section 3.3.

---

## 5. Overall reliability rating

| Layer | Rating | Basis |
|---|---|---|
| Sourced empirical facts (market, peer, regulatory) | **HIGH** | 30 checked: 28 confirmed, 2 corrected (convention and completeness), none refuted. |
| Attributions and citations | **HIGH** | All quotes match the source texts. No hallucinated references. Minor hygiene gaps. |
| Arithmetic of [I] computations | **HIGH** | Fully reproduced. Two small rounding inconsistencies. |
| Design implications | **MEDIUM** | R1: a default constraint is infeasible across the payout band. R3–R4: calibration convention and sustainable-payout statements are biased. R5–R6: tractability and decomposition claims are overstated. |
| **Overall** | **MEDIUM** | Fix R1–R5 before the framework or its defaults reach the IC. |

---

## Citation corrections (2026-10-18)

- **Erratum** (§1 "Every attribution to a paper matches the paper's own text"; claims-table row 8): row 8 confirmed Browne (1997) only for the dossier's §2.2 claim. The topic-11 recheck (`research/literature/recheck/11_objectives.recheck.md`, note 1) found that the dossier's §6.5 "Real drawdown" row put Browne's danger-zone boundary at the ~6.8% payout sustainable at a 10% return. Browne's boundary is the safe level c/r, set by the riskless rate, so a fixed 5% payout is already inside the zone at the dossier's 3.5% cash rate [unverified in Browne's own text: the MOR full text is paywalled; c/r comes from Bayraktar & Young, arXiv:math/0703824]. The dossier row has been corrected.
- **Status:** the open citation items in this log were applied to the dossier on 2026-10-18: Föllmer & Leukert (2000) is added to §10 (§1; row 26; §3.3 item 1); "Mohajerin Esfahani" is corrected (§3.3 item 2); the incomplete entries are filled (§3.3 item 3); β = 10⁻⁶ is stated in the N table (R8). See `dossiers/11_objectives.md`, "Citation corrections (2026-10-18)". No other verdict in this log changes.
