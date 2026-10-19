# Verification log: Stream 01, multi-period portfolio optimization and sequential decision methods

**Dossier checked:** `research/dossiers/01_mpo.md` v1.0 (not edited).
**Verified:** 2026-10-18.
**Role:** adversarial fact-check before Investment Committee (IC) use.

---

## 1. Summary

**Sourced facts are accurate. No citation is hallucinated.**
- Every Bain GPER 2026 statistic the dossier quotes matches the Bain pages.
- The SOFR print (3.89% on 2026-10-15, FRED updated 2026-10-16) matches FRED.
- Every attribution of a finding to a paper that I could check is correct.
- Result: 34 claims checked; 27 confirmed, 5 corrected, 0 refuted, 2 unverifiable.

**The design mathematics carries the real risk.** Five problems would change what the IC sees:

1. **The REFINANCE break-even double-counts the risk-free rate (§1.3a, §6.7).** The dossier defines the implied liquidity rate $\rho$ net of $r^f$. It then says REFINANCE wins when $\rho > r^f + s$. The correct test is $\rho > s$. At today's SOFR, the rule as written sets the hurdle about 389 bp too high, so it would systematically under-recommend facility draws.
2. **The Tier-1 floor cannot be computed in the tree it is meant for (C7 vs §6.9).** C7 needs 20 quarters of distributions and $NAV_{20}$ in every scenario. The L1 tree is only 12 quarters long. L2 cuts supply an expected value, not a NAV distribution by scenario at year 5.
3. **The scenario approach is misapplied as L3's certifier (§1.3d, §2.5).**
   - The Campi-Garatti guarantee requires a convex scenario program in which the constraint is enforced on all $N$ scenarios. A policy tuned by CMA-ES through a non-convex simulator meets neither condition.
   - A fixed policy can be certified on fresh draws with about 93 zero-violation samples, whatever its dimension.
   - The dossier's ~1,000 and ~60,000 come from a loose sufficient condition. The exact bound it cites gives 631 and 31,785.
4. **The Luxenberg calibration is used inconsistently (§1.5, §3.4, §6.9).**
   - The paper's own stated mean intensities (λ1 0.26, λ0 0.128, δ 0.33) do not reproduce its steady-state gains. The gains (α_K 2.491, α_I 3.685, α_D 1.804) come from its eq. (8) distribution. Monte Carlo puts that distribution's means at E[λ1] ≈ 0.33, E[λ0] ≈ 0.17, E[δ] ≈ 0.40 and E[R] ≈ 1.22.
   - The dossier compares δ, a fraction of post-return NAV, directly with Bain's distributions-to-NAV yield. Like for like, the overstatement is about 2.7-3.5x, not 2-2.5x.
   - The intensities come from eFront buyout data. Only the 15.8% return comes from BlackRock's 2021 assumptions.
5. **Constraint set C1-C8 is internally inconsistent and may be infeasible.**
   - C3 is enforced hard in every scenario, while C8 allows a 1% breach.
   - C8 applies CVaR ≤ 0 to a "shortfall". If the shortfall is non-negative, that forces zero breach.
   - C1-C6 are hard in every scenario with no guarantee of relatively complete recourse.

**Overall reliability: MEDIUM.** It is high for sourced facts and citations, and medium-to-low for the design formulas in §1.3, §2.5, §6.5 and §6.7. Fix those formulas before any of them reaches an IC pack.

---

## 2. Method

- **Bain GPER 2026 and FRED.** Fetched directly. The 14% period definition comes from the Figure 19 note, and the 53% reason from the full sentence.
- **Full-text extraction.** I downloaded the PDFs and extracted the text with pypdf (each file isolated in its own scratch folder). Papers covered:
  - Luxenberg et al. (arXiv:2207.07767): §3.1-3.5, §4.1-4.2, §7.3;
  - Boyd et al. (2017, arXiv:1705.00109): the computation, MPO and examples sections;
  - Powell (arXiv:1912.03513): §6.1-6.4;
  - Dulac-Arnold et al. (arXiv:1904.12901);
  - the SDDP.jl IJOC preprint and Dowson's policy-graph preprint, both linked from sddp.dev;
  - Campi's ECC'13 scenario-approach slides.
- **Recomputation by script.**
  - Luxenberg's eq. (8) means and steady-state gains, by Monte Carlo with 2M draws.
  - Exact Campi-Garatti binomial sample sizes.
  - $5^{20}$ and the dossier's liquidity arithmetic.
- **Other primary pages.** Abstracts and metadata from RePEc/IDEAS, NBER, Optimization Online, arXiv, IAOR, BIS, SIAM/Crossref, CFA Institute, and GitHub (mpi-sppy README).
- **Limitation.** The session-wide web-search budget ran out partway through. After that, every check used a direct fetch of a primary page or of Crossref DOI metadata. No search engine, proxy or archive was used. Two claims remain unverifiable (see §3).

---

## 3. Claims table

Verdicts: **C** = confirmed, **X** = corrected, **R** = refuted, **U** = unverifiable. Flagged claims are marked (F).

| # | Claim (dossier §) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | (F) PE distributions about 14% of NAV in the 12 months Q4 2024-Q3 2025, flat and the lowest since 2008-09; below 15% for four straight years (§1.5, §4.3) | C | Bain: "essentially flat at 14%, a level not seen since 2008-09". The Fig. 19 note defines 2025 as Q4 2024-Q3 2025. "Below 15% for four years running", which Bain calls an industry record. | https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ |
| 2 | (F) Holding period about 7 years (vs 5-6 in 2010-21); 32,000 unsold companies worth $3.8tn; secondaries +41%; GP-led CVs +62%; 53% of LPs constrained by undrawn commitments (§4.3) | C | All five match. Bain's 41% is the transaction value of "GP- and LP-led vehicles". The 53% comes from a PEI survey (Aug-Oct 2025), and the stated reason is "past commitments have yet to be drawn down". | same as #1 |
| 3 | (F) LBO cost 8-9% at 30-40% leverage vs 6-7% at about 50% in 2015; 10-12% EBITDA growth needed for 2.5x MOIC over 5 years; "12 is the new 5" (§4.3) | C | Verbatim match. The Fig. 1 note gives about 36% leverage at 8% for 2025, and about 50% at 6% for 2015. "12 is the new 5" is a section heading. | https://www.bain.com/insights/welcome-to-a-new-era-global-private-equity-report-2026/ |
| 4 | Buyout exit value +47% to $717bn in 2025; report published 2026-02-22 (§4.3) | C | Both match. | same as #1 |
| 5 | (F) SOFR 3.89% on 2026-10-15, FRED updated 2026-10-16 (§4.3, §6.9) | C | 3.89 on 2026-10-15; "Updated: Oct 16, 2026". Neighbouring prints: 3.88 (10-14), 3.89 (10-13). | https://fred.stlouisfed.org/series/SOFR |
| 6 | (F) Luxenberg model and calibration: λ0 0.128, λ1 0.26, δ 0.33 per year ("2021 buyout assumptions"); $1/yr sustains $3.685 NAV; CE-MPC with H=10, γ=0.97, P(insolvency) ≤ 2% is close to the liquid benchmark over 20 periods and less so over 10; cuts delayed RMS tracking error by 11% (§3.4) | X | The equations and every number appear in the paper, but four corrections apply. (a) The intensities are "calibrated from private equity data for the eFront Buyout fund". Only the 15.8% return is from BlackRock's CMA (July 2021). (b) The paper is internally inconsistent: its stated means (0.26/0.128/0.33) give α_K = 3.35 and α_I = 4.5-5.4. The reported gains (α_K 2.491, α_I 3.685, α_D 1.804) correspond to the eq. (8) distribution, whose means I compute as E[λ1] 0.334, E[λ0] 0.167, E[δ] 0.402 and E[R] 1.218; the log-mean of 0.158 gives an arithmetic mean of about 21.8%, not 15.8%. (c) The 11% RMS reduction (0.274 → 0.244) is from the §4.2 commitment-tracking example, not the §7 H=10/γ=0.97/ε=2% experiment. (d) Over 20 periods, both MPC and the simple steady-state heuristic are "extremely close" to the liquid ceiling. | https://arxiv.org/abs/2207.07767 (PDF pp. 6-9, 13-14, 22-23) |
| 7 | Calibration warning: a stationary 2021 calibration (δ = 0.33) would overstate private cash generation by about 2-2.5x vs Bain's 14% (§1.5) | X | 0.33/0.14 = 2.36 is the right arithmetic, but it compares unlike quantities. In Luxenberg, $D=\delta R I$, so the distribution yield on NAV is $E[R\delta]$. The paper's steady state gives D/I = 1.804/3.685 ≈ 0.49/yr, which is **about 3.5x** Bain's 14%. Using δ 0.33 with E[R] 1.158 gives about 2.7x. The direction holds; the magnitude is understated. | https://arxiv.org/abs/2207.07767 ; Bain URL as #1 |
| 8 | (F) Russell-Yasuda Kasai: +42 bp extra income, ¥8.7bn (about US$79m), first two years, FY1991-92 (§1.4, §3.1) | C | Abstract: "extra income of 42 basis points (¥8.7 billion or US$79 million)" during fiscal 1991-92. | https://ideas.repec.org/a/inm/orinte/v24y1994i1p29-49.html |
| 9 | (F) Multistage SP dominates fixed-mix in simulation because it adapts to information in the tree (Fleten et al. 2002) (§1.4, §4.1) | C | Abstract: "due to the ability of the stochastic programming model to adapt to the information in the scenario tree, it dominates the fixed mix approach". IDEAS shows no abstract. | https://iaorifors.com/paper/39935 |
| 10 | (F) Kouwenberg (2001): SP performance for a Dutch pension fund "could be improved drastically" with appropriate scenario generation (rolling horizon vs fixed mix) (§3.1, §4.1) | C | Verbatim in the abstract. | https://repub.eur.nl/pub/66451 |
| 11 | (F) Nystrup et al. (2019): MPC with HMM forecasts and drawdown-dependent risk aversion; about two decades out of sample; little or no loss of mean-variance efficiency; leverage raises return without raising max drawdown (§3.4) | C | Verbatim in the abstract. Citation: Ann. OR 282:245-271. | https://stanford.edu/~boyd/papers/multiperiod_portfolio_drawdown.html |
| 12 | (F) Boyd et al. (2017): SPO with 1,500 assets and 50 factors solves in under 0.5 s on one core; about 80,000 problems "ran" in under 10 minutes on 32 cores; MPO cost linear in H; hyperparameters "can greatly affect" performance; S&P 500 example uses H=2 with solves of about 0.15 s per period (§3.4, §4.2) | X | The linear-in-H, "can greatly affect" and H=2 statements are verbatim. Corrections: (a) the <0.5 s and 80,000-problem figures are projections ("can solve", "can carry out", "based conservatively on 1 Gflop/s"), not measured runs; (b) the measured 0.15 s per day is the SPO back-test optimization time (Fig. 7.8), not the H=2 MPO example; (c) the measured run was 410 back-tests, about 0.5M problems, in about 30 minutes on 32 cores. | https://arxiv.org/abs/1705.00109 (arXiv PDF pp. 40-41, 45, 53, 68, 72) |
| 13 | (F) Valladão, Silva and Poggi (2019): Markov-chain SDDP, per-period CVaR, transaction costs, up to 100 assets and 5 factors (§3.2, §4.2) | C | Abstract: one-period CVaR constraints, "Markov chained SDDP", "100 assets and 5 factors following a discrete Markov chain". Pages 379-405. | https://ideas.repec.org/a/spr/annopr/v282y2019i1d10.1007_s10479-018-2991-z.html |
| 14 | (F) Kozmík and Morton (2015): the standard upper-bound estimator performs poorly in risk-averse SDDP; importance-sampling estimators; multistage asset allocation (§3.2) | C | Confirmed from the abstract text (via search summary; the Springer page is paywalled). Volume is now verifiable: Math. Prog. 152(1-2):275-300. | https://api.crossref.org/works/10.1007/s10107-014-0787-8 |
| 15 | (F) Ang, Papanikolaou and Westerfield (2014): about 2% of wealth to hedge once-a-decade illiquidity crises; uncertainty of the interval drives cost; lower allocations to both liquid and illiquid risky assets (§2.2, §4.1) | C | Verbatim in the abstract. | https://ideas.repec.org/a/inm/ormnsc/v60y2014i11p2737-2761.html |
| 16 | (F) Dimmock, Wang and Yang: endogenous, time-varying rebalancing boundaries; staggered lock-ups raise allocations and welfare; large deviations from targets in crises (§2.2) | C | Verbatim. Published in MS 70(3):1554-1579 (2024). | https://www.nber.org/papers/w25559 |
| 17 | (F) Brown, Dimmock, Kang and Weisbenner (2014): payouts cut below stated policy after negative shocks, not raised after positive ones ("hoarding") (§4.1) | C | Abstract: endowments "actively reduce payouts relative to their stated payout policies following negative, but not positive, shocks", which it calls "endowment hoarding". The paraphrase is fair. | https://www.nber.org/papers/w15861 |
| 18 | (F) Scenario approach: exact binomial-tail bound; d=20 needs about 1,000 scenarios and d=1,500 about 60,000 (ε 5%, β 1%) (§1.3d, §2.5) | X | Exactness for fully-supported convex programs is confirmed. The dossier's numbers come from the sufficient condition (2/ε)(d + ln 1/β), giving 984 and 60,184; the arithmetic is right. **The exact bound the dossier cites gives N = 631 and 31,785.** More importantly, this is the wrong tool for L3 (see reasoning issue R3). | https://optimization-online.org/2007/07/1727/ ; my calculation |
| 19 | (F) mpi-sppy: Pyomo-based hub-and-spoke PH with bound and heuristic spokes; largest known stochastic MIP unit-commitment instances solved to provably tight gaps in minutes (§3.3, §4.2) | C | Abstract: "largest known instances of stochastic mixed-integer unit commitment problems ... provably tight optimality gaps in minutes of wall clock time". The README confirms PH and "bounding and heuristic procedures". | https://optimization-online.org/2020/11/8088/ ; https://github.com/Pyomo/mpi-sppy |
| 20 | (F) Dulac-Arnold et al.: nine real-world RL challenges, "every one applies to ADIC" (§3.7) | X | The list of nine is exact. The claim that all nine apply is an overclaim. Challenge 8, "inference that must happen in real-time at the control frequency", is immaterial for quarterly decisions. Eight of nine apply. | https://arxiv.org/abs/1904.12901 |
| 21 | (F) Powell: most real problems are solved with PFA/CFA; deterministic lookahead (MPC) is the most widely used approximation; stochastic lookaheads are hard to tune; "caution" with neural networks (§2.1, §3.4) | C | Verbatim, but the first point is stated as belief: "It is our belief that the vast majority of real-world sequential decision problems are solved with policies from the policy search class". Present it as Powell's view, not as an empirical finding. | https://arxiv.org/abs/1912.03513 (PDF §6.2, §6.4) |
| 22 | (F) Boyd et al. (2014): SDP bound "typically close" to the ADP policy's performance (§2.6, §4.1) | C | "in numerical examples the two values are typically close". The authors note there is no theoretical guarantee. | https://web.stanford.edu/~boyd/papers/port_opt_bound.html |
| 23 | SDDP.jl runs about 30% slower than a C++ implementation on the NZ hydro benchmark (§3.2, §4.2) | U | Not in the cited IJOC (2021) abstract, and not in the IJOC preprint's full text, which I extracted. It may come from an earlier 2017 preprint that I could not retrieve. Drop it or re-source it. | https://ideas.repec.org/a/inm/orijoc/v33y2021i1p27-33.html ; https://github.com/odow/SDDP.jl/blob/master/papers/other/dowson_kapelevich_2021.pdf |
| 24 | Pereira and Pinto (1991) solved a 39-reservoir system (§3.2) | C | "A case study ... for a 39-reservoir system". Math. Prog. 52(2):359-375. | https://www.iaorifors.com/paper/6581 |
| 25 | InnoALM: used since 2000 at Siemens; regulation; variable periods; state-dependent correlations (§1.4, §3.1) | C | "used since 2000 for Siemens Austria, Siemens worldwide". The other features also match. | https://ideas.repec.org/a/inm/oropre/v56y2008i4p797-810.html |
| 26 | Gondzio and Grothey: QP with more than 10^9 variables on 1,280 processors (§3.3) | C | Exact. Full title: "...with 10^9 decision variables on massively parallel architectures". | https://webhomes.maths.ed.ac.uk/~gondzio/reports/compfin06.html |
| 27 | Basel III LCR: 30-day stress, unencumbered HQLA, 100% minimum from 2019 (§5) | C | Fully binding from 1 January 2019. | https://www.bis.org/publ/bcbs238.htm |
| 28 | Frazier (2018): BO is best suited to continuous domains with fewer than 20 dimensions and noisy evaluations (§3.6) | C | Verbatim. | https://arxiv.org/abs/1807.02811 |
| 29 | The SDDP.jl docs warn that the lower bound is invalid with non-expectation risk measures (§3.2) | C | "if we use a different risk measure, the lower bound is no longer valid!" | https://sddp.dev/stable/explanation/risk/ |
| 30 | Dowson: end-of-horizon effects in finite models disappear with an infinite-horizon policy graph (§3.2) | C | The paper shows that the finite-horizon *dairy-farming* model "suffers from end-of-horizon effects, which we are able to overcome with an infinite-horizon model". It is demonstrated on one model, not proven in general. | https://github.com/odow/SDDP.jl/blob/master/papers/policy_graph/preprint.pdf |
| 31 | Kusy and Ziemba (1986): 5-year SLP for a credit union; beats deterministic LP at comparable effort (§3.1) | C | Vancouver City Savings Credit Union; "computational requirements ... comparable". | https://ideas.repec.org/a/inm/oropre/v34y1986i3p356-376.html |
| 32 | A published comment shows that Høyland-Wallace moment matching can create arbitrage (§3.1) | C | Klaassen (2002), MS 48(11):1512-1516. The comment is not in the dossier's reference list; add it. | https://ideas.repec.org/a/inm/ormnsc/v48y2002i11p1512-1516.html |
| 33 | Towers Perrin: CAP:Link generator "projecting 10-40 years", OPT:Link, FIN:Link (§3.1) | U | The three modules are confirmed. The "10-40 years" horizon is not in the 2000 abstract; possibly from the 1996 companion paper, which I did not check. | https://ideas.repec.org/a/inm/orinte/v30y2000i1p96-114.html |
| 34 | Moallemi and Sağlam (2017): linear rebalancing rules are near-optimal in execution (§3.5, §4.1) | C | "achieves near optimal performance" in the execution application. | https://ideas.repec.org/a/cup/jfinqa/v52y2017i03p1247-1278_00.html |

**Arithmetic I re-ran.**
- $5^{20}=9.5\times10^{13}\approx10^{14}$: correct.
- §4.3 liquidity illustration: $14.8bn of distributions, $9.6bn of calls, a gap of $4-13bn (5-18% of $71bn), and $8-17bn at a 10% distribution rate. All correct under the dossier's stated assumptions; see R14 for the assumptions themselves.
- The v8 deck figures used in the dossier (0.6% 12-month breach, static-SAA mean 7.3%, $P(\ge10\%)$ 31.7%, 50k paths, $18bn unfunded on $85bn) match `inputs/00_CONTEXT_AND_PRIOR_WORK.md`.

---

## 4. Citation check

None of the most important references is hallucinated. Authors, years and venues are correct except for the minor issues listed after the table.

| Reference (dossier #) | Status |
|---|---|
| Luxenberg et al. 2022, arXiv:2207.07767 (#49) | OK: nine authors as listed, title correct. The note that the ICAIF '22 version has five authors could not be checked. |
| Boyd et al. 2017, *FnT Optim.* 3(1):1-76 (#8) | OK: seven authors. Volume 3, pp. 1-76 is corroborated by Luxenberg's reference list; the arXiv PDF shows placeholder "pp. 1-74". |
| Nystrup et al. 2019, *Ann. OR* 282:245-271 (#56) | OK |
| Cariño et al. 1994, *Interfaces* 24(1):29-49 (#19) | OK. The full title adds ": An Asset/Liability Model for a Japanese Insurance Company Using Multistage Stochastic Programming". |
| Fleten, Høyland and Wallace 2002, *EJOR* 140(1):37-49 (#28) | OK |
| Kouwenberg 2001, *EJOR* 134(2):279-292 (#44) | OK |
| Valladão, Silva and Poggi 2019, *Ann. OR* 282(1) (#68) | OK; add pp. 379-405. |
| Kozmík and Morton, *Math. Prog.* pp. 275-300 (#45) | OK. The volume is now verified: 152(1-2), online 2014, print 2015. |
| Ang, Papanikolaou and Westerfield 2014, *MS* 60(11):2737-2761 (#1) | OK |
| Dimmock, Wang and Yang 2024, *MS* 70(3):1554-1579 (#23) | OK |
| Brown, Dimmock, Kang and Weisbenner 2014, *AER* 104(3):931-962 (#12) | OK. The title omits the subtitle ": Evidence and Implications". |
| Campi and Garatti 2008, *SIAM J. Optim.* 19(3):1211-1230 (#17) | OK |
| Knueven et al. 2023, *Math. Prog. Comp.* 15(4):591-619 (#43) | OK: author order matches the README. The issue number (4) is not confirmed. |
| Powell, arXiv:1912.03513 (#62); Powell 2019, *EJOR* (#61) | arXiv OK (v2, 18 Dec 2019). The EJOR record was not re-checked. |
| Boyd, Mueller, O'Donoghue and Wang 2014, *FnT Optim.* 1(1):1-69 (#9) | OK |
| Füllner and Rebennack 2025, *SIAM Rev.* 67(3):415-539 (#31) | OK (Crossref) |
| Dowson and Kapelevich 2021, *IJOC* 33(1):27-33 (#26) | OK |
| Dowson, policy graph (#25) | Minor. Published in *Networks* 76(1) (2020) as "...multistage stochastic **optimization** problems". The dossier uses the preprint title ("programming") and says the journal version is unverified. |
| Zou, Ahmed and Sun (#70) | OK. The volume is now verified: *Math. Prog.* 175(1-2):461-502 (print 2019). |
| Pereira and Pinto 1991; Geyer and Ziemba 2008; Mulvey et al. 2000; Kusy and Ziemba 1986; Dantzig and Infanger 1993 (*Ann. OR* 45(1):59-76); Philpott and de Matos 2012; Shapiro (2008 preprint); Hambly et al. 2023; Høyland and Wallace 2001; Cao and van Beek 2025 (*FAJ* 81(3); first author "Wen Cao") | All OK |
| Gondzio and Grothey 2006 (#35) | OK, but the title is truncated (full title in claim 26 of §3). |

**Problems to fix**
- Add Klaassen (2002) to the references; it is cited in the text as "a published comment".
- Fill in the volumes that are now verifiable: Kozmík 152, Zou 175, Valladão pp. 379-405.
- Re-source or drop the SDDP.jl "30% slower" claim.
- Restore the full titles for Brown et al. and Gondzio and Grothey.
- Correct the Dowson title and venue.
- **Erratum (2026-10-18):** the Dowson row above has the two titles the wrong way round. Crossref (DOI 10.1002/net.21932) gives the *Networks* 76(1):3-23 (2020) article the dossier's title, "...multistage stochastic **programming** problems". The 2018 preprint was the one titled "...optimization problems" (`literature/01_mpo.lit.md`, row #25). Keep the dossier's title and add only the venue.

---

## 5. Reasoning errors and overclaims in the design implications

Severity: **H** = would change an IC conclusion or break the model; **M** = would produce wrong diagnostics or unsupported guarantees; **L** = hygiene.

### R1 (H). The REFINANCE break-even double-counts $r^f$ (§1.3a; §2.6; §6.7)

**The definition.** §2.6 defines $\rho_t=\lambda_t/\mathbb{E}[\lambda_{t+1}]-(1+r^f_t)$. This is the liquidity premium *over* the risk-free rate. It is zero when cash is slack, because the reduced cost of carried cash gives $\lambda_t=(1+r^f)\mathbb{E}[\lambda_{t+1}]$.

**The derivation.** Take the §6.7 REFINANCE value for a one-quarter loan, $\mu_0-\mathbb{E}[\mu_1](1+(r^f+s)/4)$. Substituting $\mu_0=\mathbb{E}[\mu_1](1+r^f/4+\rho_q)$ gives $\mathbb{E}[\mu_1](\rho_q-s/4)$.

**The consequence.**
- REFINANCE pays when $\rho>s$, the facility spread. Equivalently, the gross implied rate $r^f+\rho$ must exceed $r^f+s$.
- The dossier's "ρ exceeds SOFR plus spread" sets the hurdle about 389 bp too high at today's SOFR.
- It would systematically understate the value of the NAV facility and distort the liquidity merit order.

**Related unit problem.** The cash equation uses quarterly $r^f$ ("quarterly rates"), while §6.7 uses annual $(r^f+s)/4$. Fix one convention.

### R2 (H). C7's five-year floor cannot be computed inside the 12-quarter L1 tree (§6.5 C7; §6.9)

- $\mathrm{NPV}_{7\%}$ needs $d_1,\dots,d_{20}$ and $NAV_{20}$ in every scenario. The L1 tree ends at quarter 12.
- L2 cuts give a (risk-adjusted) expected value function at $T_1$. They do not give a NAV *distribution* by scenario at quarter 20.
- So C7 cannot be computed scenario-wise as specified. The options are:
  - extend the tree to 20 quarters, with deterministic or fan tails for quarters 13-20;
  - restate the floor over L1's horizon, with a terminal NAV haircut;
  - add a CVaR-type terminal cut family to L2.

  Each choice changes what "P(floor breach)" means, so the IC needs to be told which one is used.

### R3 (H). The scenario approach is misapplied as L3's certifier (§1.3d; §2.5)

- **Wrong setting.** Calafiore-Campi and Campi-Garatti bound the violation probability of the optimizer of a **convex** scenario program in which the constraint is **enforced on all N sampled scenarios**. An L3 PFA/CFA tuned by CMA-ES or BO on *average* simulated performance through a non-convex 40-quarter simulator fails both conditions. Campi's own slides: the theory needs "only convexity"; the "non-convex" case is "still in its infancy".
- **Easier route.** To certify a *fixed, already-tuned* policy, evaluate it on fresh i.i.d. paths. A zero-violation test at ε 5% and β 1% needs only $N\ge\ln(1/\beta)/\varepsilon\approx 93$ paths, whatever the dimension. With violations, use Clopper-Pearson intervals. Reserve the scenario approach for a convex sub-problem, or use the non-convex "wait-and-judge" / compression results.
- **Numbers.** Even on its own terms, the exact binomial bound gives 631 (d = 20) and 31,785 (d = 1,500), not about 1,000 and about 60,000.
- **Consequence.** The design conclusion "L3 uses scenario-approach certification" should be replaced with "L3 uses out-of-sample binomial confidence intervals on held-out seeds and held-out generators".

### R4 (H). The private-cash calibration is mis-mapped (§1.5; §3.4; §6.9)

- **The source's numbers do not agree with each other.** Luxenberg's stated means (λ1 0.26, λ0 0.128, δ 0.33) give α_K = 3.35 and α_I = 4.5-5.4. The paper reports 2.491 and 3.685. Those gains are reproduced only with the eq. (8) means: E[λ1] 0.334, E[λ0] 0.167, E[δ] 0.402 and E[R] 1.218 (product-of-means α_I = 3.689, α_D = 1.805). The dossier pairs "δ̄ = 0.33" with "$1 sustains $3.685", which is inconsistent.
- **Like-for-like comparison.** δ multiplies $R\cdot I$ (§6.4 uses the same $D=\delta R I^+$). Bain's 14% is distributions over NAV. So the low-DPI intensity in §6.9 should be about $0.14/\mathbb{E}[R]\approx0.12$-$0.13$, not 0.14. The Luxenberg steady-state yield is D/I ≈ 0.49, so the overstatement is about 3.5x, not 2-2.5x.
- **Period conversion.** All intensities are annual, but §6.4 is quarterly. Specify the conversion, for example $1-(1-\lambda_{ann})^{1/4}$, and note that λ0 does not scale the same way.

### R5 (M). The C8 chance constraint is mis-specified and conflicts with C3 (§6.5)

- **C8.** If "LCR shortfall" is the positive part, $(\text{outflows}-\text{liquidity})^+\ge0$, then $\mathrm{CVaR}_{0.99}\le0$ forces zero shortfall in every scenario. That is a hard constraint, not a 1% breach budget. Apply CVaR to the *signed* margin $g=\text{outflows}-\text{haircut liquidity}$.
- **C3.** C3 ("Fund LCR, 30-day and 12-month") is enforced "in every scenario s and quarter t". That makes the 12-month breach probability zero in-sample, so C8 is either redundant or contradictory. Choose one: hard 30-day plus probabilistic 12-month, or the reverse.

### R6 (M). Hard constraints without relatively complete recourse (§6.5 C1-C6)

- The distribution floor, the IG + cash floor, the LCR and the covenants are all hard in every scenario. In deep-stress leaves the extensive form will be infeasible, and SAA replications will fail unpredictably.
- Only C7 gets a "recovery mode".
- The dossier's own Russell-Yasuda lesson (§5: "soft constraints with priority-weighted penalties") is not applied. Use elastic variables with lexicographic penalties, and report the penalty usage to the IC as breach evidence.

### R7 (M). The Shapley-Folkman small-gap argument does not apply to L1 (§3.3)

- The Shapley-Folkman/Aubin-Ekeland duality-gap bound scales with the number of coupling constraints, $m$: roughly $(m+1)\times$ the largest individual non-convexity.
- In the stochastic L1, cash balances alone number about 8,100 rows (1,000 leaves × 8 quarters, plus 40 × 3 and the root), before the CVaR, LCR and leverage rows. So $m\gg n\approx300$ assets and the bound is vacuous.
- Price decomposition can still work as a heuristic, but without that guarantee. Validate it against the extensive-form MILP.

### R8 (M). The WS ≥ RP ≥ EEV "machine-checkable invariants" are ill-defined under cross-scenario risk constraints (§2.3; §6.1 step 5; §7 Tests)

- Birge's ordering holds for risk-neutral recourse problems.
- C7 and C8 are CVaR constraints over the *scenario distribution*. Under perfect information they cannot be evaluated scenario by scenario, so WS needs a definition.
- The mean-value first stage can be infeasible in stressed scenarios, which makes EEV = −∞ and VSS infinite.
- Define these diagnostics on a risk-neutral or penalized surrogate, or the rubric check will fire spuriously.
- Likewise, "tightening the floor must never raise expected return" holds for the *optimized objective* (discounted payout + terminal value − penalties), not for reported expected return, and it can fail across SAA replications.

### R9 (M). The information-relaxation "optimality gap" is overclaimed (§1.2 L3; §2.6; §6.8 item 6)

- Brown-Smith-Sun duality bounds expected additive rewards. With chance/CVaR constraints, nested risk and the Tier-1 rules, a valid bound needs a constrained or risk-averse extension, which the dossier does not specify.
- The gap is also only as tight as the chosen penalty.
- It is conditional on the model, so it says nothing about model risk.
- Restate the claim as "gap versus the best policy under model m, risk-neutral surrogate".

### R10 (M). Gaps in action modelling (§6.3-6.4)

- Asset-level REFINANCE proceeds $q_{i,t}$ are declared as a decision but **appear in neither the cash equation nor the NAV transition**. As written, the asset-level recap does nothing.
- The opportunistic-sleeve budget $e_t$ has no P&L mapping except through VM.
- LEVER is modelled as a cash-consuming add-on or co-invest. The user's "lever" may mean borrowing against an asset, which raises cash and risk. Confirm the semantics of all four actions with the user before building.

### R11 (L). Unit and dimension hygiene in §6.7

- The SELL value subtracts the fixed cost $F_i$ unscaled by $\mu_0$; it should be $\mu_0[(1-\delta)I_i-F_i]-CV_i$.
- $CV_i$ multiplies $\mu_{T_1}$ by the cut slope $\theta'_g$. If θ is in objective units, this double-converts; the terminal term should be $(1+r^*)^{-T_1/4}\theta'_g I_{i,T_1}$. State the units explicitly.

### R12 (L). Cash-equation details (§6.4)

- Facility interest is charged on $b_t$ rather than $b_t+\Delta b^+_t-\Delta b^-_t$, although draws happen at the beginning of the quarter.
- $D$ denotes both fund debt and distributions.

### R13 (L). The sizing ignores the model-set multiplier (§4.2)

C7 and C8 must hold "for every model m ∈ M". If each generator supplies its own scenario set inside L1, the extensive form grows by a factor of |M|, about 3x. The 1.8M-variable and minutes-to-an-hour estimates are [I] and do not include this.

### R14 (L). Assumptions in the illustrative liquidity arithmetic (§4.3)

- The arithmetic assumes no new commitments; calls on new commitments ($\lambda^0 n$) are missing.
- It scales unfunded commitments by *total* NAV: 21%, about $37bn.
- Scaling instead by v8's unfunded-to-illiquid ratio ($18bn / $38.2bn ≈ 47%) gives about $50bn unfunded and about $13bn of calls.
- That widens the gap at a 14% distribution rate to about $7-16bn/yr, versus the dossier's $4-13bn. Show both scalings as a range.

### R15 (L). Provenance and emphasis

- §6.9 tags "IRR ≥ 7% over a rolling 5 years ... via CVaR95" as [S deck]. The deck specified a "worst-case 5-year annualised return" with at most a 5% breach. The IRR, rolling-window and CVaR choices are the dossier's inference ([I]).
- The Luxenberg 20-period result (claim #6d) supports simple policy rules as much as MPC; say so.
- The Boyd timings (claim #12) should be labelled projections.

---

## 6. Overall reliability rating

**MEDIUM.**

- **Sourced facts and citations: high.** 27 of 34 claims confirmed; no refutations; no hallucinated references. The only material empirical correction is the Luxenberg calibration (claims #6 and #7).
- **Design implications: medium-to-low until fixed.** R1-R4 are the priority:
  - the REFINANCE hurdle;
  - the C7 horizon;
  - the L3 certification method;
  - the distribution-intensity mapping.

  Each would put a wrong number or a false guarantee in front of the IC. R5-R10 should be fixed before L1 is implemented.

---

## Citation corrections (2026-10-18)

- §4: one erratum line added under "Problems to fix". The *Networks* (2020) version of Dowson's policy-graph paper has the dossier's title ("...programming problems"), so the retitling proposed in the §4 table had the two titles reversed (Crossref 10.1002/net.21932; literature check 01).
