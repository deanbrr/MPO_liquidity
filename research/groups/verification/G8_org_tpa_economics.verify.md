# G8 verification log: organizational economics of ADIC's seven-group TPA

- **Dossier checked:** `research/groups/dossiers/G8_org_tpa_economics.md` (as of 18 Oct 2026). The dossier itself was not edited.
- **Verifier:** adversarial fact-check for the IC research program, 18 Oct 2026.
- **Scope:**
  - all 20 author-flagged claims, plus 12 further load-bearing or suspicious claims (32 in total);
  - 22 references checked for existence, authors, year, title and venue;
  - design implications and the specification card (§6) reviewed;
  - every [I-calc] number re-derived from `G8_org_calcs_results.json`.
- **Method:**
  - **Primary sources fetched directly:** NBER, RePEc/IDEAS, arXiv, BIS, the Basel Framework (LCR40), the EBA-hosted CEBS PDF, the CPP Investments F2024 Annual Report PDF, the CalPERS agenda-item PDF, the CFA Institute and CAIA/TAI PDFs, NBIM, Cornell LII, FRED, GIC, NZ Super and the Harvard Gazette. PDFs were text-extracted locally with pypdf.
  - **Consensus search** (search tool only; authentication tools not called) was used for abstract-level checks of academic citations.
  - **One extra synthetic calculation** reuses the dossier's E1 data: `scratchpad/scripts/g8_checks.py`, outside the project.
- **Verdict rule:** a claim is "confirmed" only when the primary text supports it. Where it could not be found, the default was "unverifiable"; no benefit of the doubt was given.

---

## 1. Summary

1. **Evidence base: strong.**
   - Of 32 claims checked, **30 are confirmed and 2 corrected (both minor). None is refuted or unverifiable.**
   - Every load-bearing number matches its primary document exactly:
     - **CPP:** DVA −C$63,731m against a +C$10,135m target, so 0x; absolute return 7.73% against 6.23%, so 1.24x; total-fund multiplier 0.62; weights 30/30/40, senior management 50/50; 10-day LCR 3.8 against 1.0.
     - **CalPERS:** 75/25 Reference Portfolio; 400 bp limit; about 230 bp current; 250–350 bp operating range; 11 benchmarks reduced to 1; discount rate 6.8%.
     - **NBIM, CFA and BGH:** the NBIM pay rules; CFA's 8/66/26 split and barrier counts 5/4/4/3; BGH's 36% coverage across more than 13,300 distributions.
     - **Rates and regulation:** SOFR 3.89% on 15 Oct 2026; LCR40.64 at 40%.
     - **CEBS:** every paragraph citation (¶6, 8, 9, 10, 13, 17, 20, 25, footnote 2, Annexes 1 and 2) matches the 27 Oct 2010 text.
2. **Citations: no hallucinated or garbled references.**
   - One working-paper pointer is mislabeled (Shin & Stulz, "NBER 5639").
   - One prescriptive gloss is attributed to Baumol & Fabian, when the source abstract doesn't state it.
   - FSI's wording is paraphrased too strongly in two places.
   - Two [M] journal details can be upgraded to verified: Gneiting 2011 (JASA) and Chen et al. 2014 (ACM TEAC).
3. **The material risk is in the specification layer, not the evidence.** Five issues would produce wrong prices or budgets if implemented as written:
   - **R1.** The no-regret bands are not jointly feasible. If every group used its upper band at once, the binding crisis-liquidity row would be exceeded by 76% and the CVaR row by 86%.
   - **R2.** The 3% buffer-carry floor on liquidity prices contradicts the dossier's own rule that decision prices are today's duals. In E1 (binding dual 1.83%) it cuts deployment from $6.67bn to $1.48bn; flooring all three liquidity rows cuts it to $0.
   - **R3.** Contingent liquidity is double-counted: stressed unfunded draws are charged through both the dual-based liquidity term and the CLC.
   - **R4.** The DVA attribution identity mixes return and dollar units, and subtracts a risk amount (RC_g) rather than a risk charge.
   - **R5.** c_buf = E[r_FB] − r_HQLA charges an expected risk premium as if it were a liquidity cost, which departs from the CEBS Annex 2 definition and overlaps with the CVaR charge.
4. **Overall reliability: MEDIUM.**
   - The evidence is high quality and can go to the IC with the two wording fixes.
   - The specification card needs the R1–R5 fixes before it computes live prices or budgets.

---

## 2. Claims verified

Verdicts: **C** = confirmed; **Corr** = corrected.

| # | Claim (abridged) | Verdict | Corrected value / verifier note | Source URL |
|---|---|---|---|---|
| F1 | Winner-picking (actively shifting funds between projects) is a source of ICM value; ICMs work better in focused firms (Stein 1997, JF 52(1):111–133) | C | The abstract defines HQ "winner-picking" and says internal capital markets "may function more efficiently when companies choose relatively focused strategies". The hedge "may" is lost in the dossier, a minor point. JF 52(1):111–133 confirmed | https://www.nber.org/papers/w5101 |
| F2 | Rent-seeking leads HQ to "preferential capital budgeting allocations", producing "a kind of socialism" (Scharfstein & Stein 2000, JF 55(6)) | C | Both quotes are verbatim. JF 55(6):2537–2564 | https://www.nber.org/papers/w5969 |
| F3 | Funds flow to the least efficient divisions; the distortion grows with diversity; 1979–1993 panel (RSZ 2000, JF 55(1)) | C | Abstract: "funds are allocated towards the most inefficient divisions"; "The distortion is greater the more diverse..."; "1979-1993". JF 55(1):35–80 | https://www.nber.org/papers/w6368 |
| F4 | After the 1986 oil collapse, oil firms cut non-oil investment relative to industry medians, mostly in units subsidized in 1985 (Lamont 1997) | C | Verbatim: "significantly reduced their non-oil investment compared to the median industry investment"; "concentrated in non-oil units that were subsidized by the rest of the company in 1985". JF 52(1):57–82 | https://www.nber.org/papers/w5499 |
| F5 | In many cases no prices lead divisions to independently optimal decisions, **so prices must be paired with quantity guidance** (Baumol & Fabian 1964) | Corr (minor) | The first half is in the abstract verbatim: "in many cases there exist no prices which will lead divisions to make independent decisions that are optimal from the point of view of the company or the economy as a whole". The "pair prices with quantity guidance" remedy is **not** in the source abstract and should be tagged [I]; it is consistent with the Dantzig–Wolfe and Kornai–Lipták literature. A 1973 *Management Science* note (Maiti et al., 19(12):1459–1462) disputes B&F's contention, and the dossier does not mention it | https://ideas.repec.org/a/inm/ormnsc/v11y1964i1p1-32.html ; https://consensus.app/papers/details/9af6dae07ffa5846b3f543e032a0a4da/ |
| F6 | BCBS Principle 4 (25 Sep 2008): incorporate liquidity costs, benefits and risks in internal pricing, performance measurement and new-product approval for all significant on- and off-balance-sheet activities | C | The date is per the BIS page. The Principle 4 text ("internal pricing, performance measurement and new product approval process for all significant business activities (both on- and off-balance sheet), thereby aligning ...") is confirmed via the RBI's reproduction of it. The BIS PDF blocked automated download | https://www.bis.org/publ/bcbs144.htm |
| F7 | CEBS (27 Oct 2010): compensate providers, charge users (¶13); committed lines (¶17); contingent costs to generating units (¶20); marginal cost (¶25); no profit target (¶10); buffer cost = funding plus opportunity cost (Annex 2) | C | Every paragraph number and wording matches. Also confirmed: ¶6 (board approves the methodology; ALCO "at least annually"), ¶8, ¶9, footnote 2, and the Annex 1 counts (cost centre 4/5; incentive amendments yes 3, no 2; updates daily 1, weekly 3, monthly 1; one bank's divisional stress tests included undrawn commitments). Note that Annex 2 sizes the buffer for "a short time horizon (for example, up to one month)" (see R5 and R6) | https://www.eba.europa.eu/sites/default/files/documents/10180/16094/da61d4c3-3937-4612-9584-e6136cb98191/cebs18_Guidelines.pdf |
| F8 | FSI (30 Dec 2011), 38 banks in 9 countries: non-attribution was the most striking poor practice; **single average rates were common**; recommends maturity-matched marginal cost and charges for expected contingent usage | Corr (minor) | Confirmed: 38 large banks, nine countries, 30 Dec 2011, and both recommendations. The text reads: "**Probably** the most striking example of poor practice was that some banks failed to attribute liquidity costs"; "Others did attribute ... albeit at one average rate". How often single rates occurred is **not quantified**, so "common" is unsupported. §6.4's "FSI 2011 called missing attribution the worst practice" overstates the source | https://www.bis.org/fsi/fsipapers10.htm |
| F9 | With a decision stake, standard scoring rules stop being proper; compensation rules must offset the stake; with unknown stakes the misreport can only be bounded (Boutilier) | C | Single author; arXiv v1 only (13 Jun 2011). Introduces compensation rules, characterizes proper ones under known utility, and bounds the incentive, degree and loss of misreporting under uncertainty | https://arxiv.org/abs/1106.2489 |
| F10 | Executives' 80% intervals contained realized returns 36% of the time (13,300+ forecasts), implying intervals about 2.7× too narrow (BGH 2013, QJE 128(4)) | C | "more than 13,300" distributions in a 10-year panel; 36% (the final version; the 2010 working paper reported 33%). QJE 128(4):1547–1584. The 2.7× figure is a correct inversion (1.2816/0.4677 = 2.74), but only under normality, zero bias and independent errors (see R9) | https://www.nber.org/papers/w16215 |
| F11 | Quantiles are elicitable via generalized piecewise-linear scores; CVaR is not (Gneiting) | C | "consistent for a quantile if and only if it is generalized piecewise linear"; "Not all functionals are elicitable; for instance, conditional value-at-risk is not". JASA DOI 10.1198/jasa.2011.r10138. The design implication goes further than the source (see R8) | https://arxiv.org/abs/0912.0902 |
| F12 | WIS = 1/(K+1/2)·(w0·AE + Σ w_k·IS_αk), w_k = α_k/2, w0 = 1/2; proper; approximates the CRPS; IS formula as stated (Bracher et al. 2021) | C | Eq. (1)–(2) and the IS definition match exactly, and the score is proper for any non-negative weights. The CRPS approximation is stated "for large K and equally spaced values" of α, so it is weak at the dossier's K = 1 (see R12). PLoS Comput Biol DOI 10.1371/journal.pcbi.1008618 | https://arxiv.org/abs/2005.12881 |
| F13 | Budget-linked pay induces lying and gaming; remove budgets and targets from pay; use purely linear pay (Jensen 2003, EFM 9(3)) | C | "we must stop using budgets or targets in the compensation formulas"; "taking all kinks, discontinuities and non-linearities out"; "purely linear compensation formulas provide no incentives to lie". EFM 9(3):379–406 | https://ideas.repec.org/a/bla/eufman/v9y2003i3p379-406.html |
| F14 | CPP FY2024: TFM designs allocations with the CIO; delegated approval authorities, mandates and risk limits; weights 30/30/40 (senior management 50/50); five-year DVA −C$63.7bn against +C$10.1bn, so 0x and a 0.62 total multiplier; 10-day LCR 3.8 against 1.0 | C | TFM is responsible for "designing and recommending ... capital allocations to investment strategies in conjunction with the CIO" (PDF p.51). "within their delegated approval authorities, mandates and risk limits" (p.22). Weights 30/30/40, senior management 50/50, 0–2× per factor (p.31). Target $10,135m against actual −$63,731m, 0x; 6.23% against 7.73%, 1.24x; 0.62 (pp.74–76). LCR 3.8 against 1.0 at 31 Mar 2024 (p.44). **Omission:** the HRCC applied an *upward adjustment* to the total-fund multiplier for non-senior employees (p.74), relevant to R18 | https://cppinvestments.com/wp-content/uploads/2024/05/CPP-Investments-F2024-Annual-Report.pdf |
| F15 | CalPERS item 5a (17 Nov 2025): TPA; 75/25; 400 bp limit; about 230 bp current; 250–350 bp range; 11 benchmarks reduced to one; discount rate 6.8% | C | All figures verbatim. Also: consolidated SAA ranges came to about 450 bp, and the Board's oversight role is unchanged. The item is a first reading of recommendations; UAO reports a board vote the same day | https://www.calpers.ca.gov/documents/202511-invest-agenda-item05a-00-a/download |
| F16 | NBIM principles (amended 21 May 2026): relative-return pay over ≥2 years; ≥50% deferred ≥3 years and adjusted with absolute return; cap 100%; Leader Group gets no variable pay | C | "last amended 21 May 2026". Further detail: ≥60% is deferred when variable pay is particularly high; exceptions allow up to 200%; pay is "contracted or terminated if the relative return ... is severely negative" | https://www.nbim.no/en/organisation/governance-model/executive-board-documents/compensation-principles-for-norges-bank-investment-management-employees |
| F17 | Top-100 asset owners: 8 TPA, 66 SAA, 26 hybrid. Main barriers: culture, coordination, governance. +1.3% (TAI) and about 150 bp (Garmash) are confounded (Urwin & Hayman, CFA Institute, Jul 2026) | C | The 8/66/26 split is labeled a "preliminary assessment" citing TAI 2025a. Barriers (N=10): culture 5, coordination 4, governance 4, market factors 3. Garmash 150 bp; TAI 1.3% a year (10-year, 26-fund). Confounders named: size, mandates, benchmarks, short history, alternatives exposure | https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/fti_tpa-report_online.pdf |
| F18 | All unit managers over-budget capex; powerful managers capture windfalls and invest about 40% more (Glaser et al. 2013, JF 68(4)) | C | Verbatim: "all unit managers systematically over-budget capital expenditures"; "more powerful and better connected managers obtain larger shares of cash windfalls"; "about 40% more". JF 68(4):1577–1631 | https://ideas.repec.org/a/bla/jfinan/v68y2013i4p1577-1631.html |
| F19 | Rule 17a-7: cash at "independent current market price", no commissions, board procedures with quarterly review, six-year records | C | All four elements confirmed; records are in para. (g), kept ≥6 years. **Scope limit:** the rule covers only securities "for which market quotations are readily available", which fund stakes lack (the dossier acknowledges this) | https://www.law.cornell.edu/cfr/text/17/270.17a-7 |
| F20 | SOFR 3.89% on 15 Oct 2026; Basel LCR40.64 40% drawdown for committed facilities to banks and other FIs, used as a conservative prior for stressed unfunded draws | C (facts) | FRED shows 2026-10-15 = 3.89 (updated 16 Oct 2026). LCR40.64(4) and (5) give 40% (banks; other FIs, credit); (6) gives 100% (other FIs, liquidity facilities); (7) gives 100% (SPEs and conduits). **The LCR horizon is 30 calendar days**, so using it for 12-month LP calls is an analogy, not evidence (R6) | https://fred.stlouisfed.org/series/SOFR ; https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30 |
| A1 | A segment invests out of other segments' cash flow, less than out of its own, regardless of relative opportunities (Shin & Stulz 1998) | C (claim); citation note | The QJE abstract matches exactly. **But** "WP: NBER 5639" is titled *An Analysis of Divisional Investment Policies* (Jun 1996), has a different abstract, and lists no published version | https://consensus.app/papers/details/c7c5bc16465b5f2b943974f4ed01132e/ (DOI 10.1162/003355398555676) |
| A2 | Conglomerates' ICMs became more valuable in 2007–09 (Kuppuswamy & Villalonga 2016) | C | "conglomerates' access to internal capital markets became more valuable". MS 62(4):905–923 | https://ideas.repec.org/a/inm/ormnsc/v62y2016i4p905-923.html |
| A3 | More than 1,000 CEOs and CFOs: gut feel and division-manager reputation; politics and socialism in European and Asian firms (Graham, Harvey & Puri 2015) | C | Verbatim. JFE 115(3):449–470 | https://ideas.repec.org/a/eee/jfinec/v115y2015i3p449-470.html |
| A4 | Hurdle rates are about 2× the cost of capital, partly to ration managerial capacity (Jagannathan et al. 2016) | C | "average twice the firms' cost of financial capital"; "limited qualified management or manpower". JFE 120(3):445–463 | https://ideas.repec.org/a/eee/jfinec/v120y2016i3p445-463.html |
| A5 | 3,400 plan sponsors (1994–2003): hires follow large excess returns; no positive post-hire excess returns; post-firing returns about zero (Goyal & Wahal 2008) | C (nuance) | Post-firing excess returns are "typically indistinguishable from zero but in some cases positive". JF 63(4):1805–1847 | https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1805-1847.html |
| A6 | Unrelated segments are less Q-sensitive, under-investing in high-Q industries; worse with low management ownership (Ozbas & Scharfstein 2010) | C | The abstract matches. RFS DOI 10.1093/rfs/hhp071 | https://consensus.app/papers/details/6cc2e034f8c95dc6b1bb978d3eb90e05/ |
| A7 | 26-fund peer study: 35% (9) adopted TPA; 54% anticipating; SAA users halved since 2017; TPA adopters +1.3% a year (Filbeck & Bok, Oct 2025) | C | Verbatim (Stage 3 section; 10-year data, 1.3% per annum) | https://www.thinkingaheadinstitute.org/content/uploads/2025/10/2025-TPA-Report-from-Vision-to-Execution.pdf |
| A8 | "Hurdle rates reflect capital allocation through a division-specific capital structure" (Stoughton & Zechner 2007) | C | The JFI abstract contains the sentence (the SSRN version instead says hurdle rates "have a common component"). JFI 16(3):312–342 | https://ideas.repec.org/a/eee/jfinin/v16y2007i3p312-342.html |
| A9 | GIC: three-group Strategic Portfolio from 2026; 20-year real return 3.4%, USD nominal 5.6% to 31 Mar 2026 | C | 24 Jul 2026 release: "represents the Client's risk appetite"; "within approved risk parameters"; equities, fixed income, real assets | https://www.gic.com.sg/newsroom/all/gic-delivers-steady-long-term-returns-within-its-mandate-and-stays-focused-on-portfolio-resilience-in-a-structurally-changed-world/ |
| A10 | NZ Super Reference Portfolio since 2010: 75% global equity, 5% NZ equity, 20% fixed income, 100% NZD-hedged; hurdles; value-add net of all costs | C | All elements confirmed (page updated Sep 2023) | https://nzsuperfund.nz/how-we-invest/reference-portfolio/ |
| A11 | CalPERS TPA effective 1 Jul 2026 with a 50–60 bp CIO aim; HMC tied pay to the whole endowment (Jan 2017) | C | UAO (secondary, 1 Jul 2026): "begins operating under a Total Portfolio Approach". The CFA report quotes Gilmore: "perhaps 50–60 basis points". Harvard Gazette 25 Jan 2017: "based on the endowment's overall performance" | https://www.universalassetowners.com/intelligence/uao-daily-brief-2026-07-01/ ; https://news.harvard.edu/gazette/story/2017/01/course-change-for-harvard-management-company |
| A12 | ERISA §408(b)(19) conditions; FRA §23B market terms; Solvency II cost-of-capital rate 4.75% from 30 Jan 2027 (λ_R anchor) | C | ERISA: authorization by a fiduciary other than the manager, ≥$100m in plan assets, quarterly report, written policies, annual signed report; it also requires readily quoted securities. §23B: "substantially the same, or at least as favorable". The 4.75% rate is confirmed only via secondary sources (Deloitte, BNY), not the Official Journal text | https://www.law.cornell.edu/uscode/text/29/1108 ; https://www.law.cornell.edu/uscode/text/12/371c-1 ; https://www.deloitte.com/lu/en/our-thinking/future-of-advice/solvency-ii-review-2025.html |

**Not checked in this pass:**
- market data inherited from other streams [S\*]: Jefferies H1 2026, Bain 2026, Rede 2026, ILPA 2023;
- the CPP Apr 2026 TPA paper, which reaches the dossier only through a blog;
- the wording attributed to Milgrom 1988, Meyer–Milgrom–Roberts 1992, Weitzman 1976, Mellers et al. 2014 and Hirshleifer 1956 ([M]).

None of these is load-bearing for §6.

---

## 3. Citation check (existence, authors, year, title, venue)

| Reference (dossier §10 #) | Exists | Authors / year / title / venue | Issue |
|---|---|---|---|
| Stein 1997 (#1) | Yes | Correct; JF 52(1):111–133; NBER w5101 (May 1995) | None |
| Scharfstein & Stein 2000 (#2) | Yes | Correct; JF 55(6):2537–2564 | None |
| Rajan, Servaes & Zingales 2000 (#3) | Yes | Correct; JF 55(1):35–80 | None |
| Shin & Stulz 1998 (#4) | Yes | Correct; QJE 113(2):531–552 | **The WP pointer "NBER 5639" is mislabeled.** That paper is *An Analysis of Divisional Investment Policies* (1996), with a different abstract and no published-version link. Cite the QJE DOI only, or describe 5639 as an earlier related WP |
| Lamont 1997 (#5) | Yes | Correct; JF 52(1):57–82 | None |
| Glaser, Lopez-de-Silanes & Sautner 2013 (#9) | Yes | Correct; JF 68(4):1577–1631 | None |
| Baumol & Fabian 1964 (#26) | Yes | Correct; MS 11(1):1–32; DOI 10.1287/mnsc.11.1.1 | The prescriptive gloss is attributed to B&F although the source abstract doesn't state it (F5). The Maiti et al. (1973) rebuttal is not mentioned |
| Jensen 2003 (#25) | Yes | Correct; EFM 9(3):379–406 | None |
| BCBS 2008 (#30) | Yes | *Principles for Sound Liquidity Risk Management and Supervision*, 25 Sep 2008 | None |
| CEBS 2010 (#31) | Yes | 27 Oct 2010; "CEBS 2010 198" (reference from the file metadata) | None |
| FSI Occasional Paper 10 (#32) | Yes | 30 Dec 2011; *Liquidity transfer pricing: a guide to better practice* | Paraphrased too strongly (F8) |
| Boutilier (#40) | Yes | Single author; arXiv v1 13 Jun 2011; no journal reference on arXiv | "(2011/2012)" implies a 2012 venue version without citing it. Minor |
| Ben-David, Graham & Harvey 2013 (#42) | Yes | Correct; QJE 128(4):1547–1584 | None (uses the final 36% figure) |
| Gneiting 2011 (#38) | Yes | JASA, DOI 10.1198/jasa.2011.r10138 | The journal details tagged [M] are correct; the tag can be upgraded |
| Bracher, Ray, Gneiting & Reich 2021 (#39) | Yes | PLoS Comput Biol 17(2):e1008618 (DOI matches arXiv) | None |
| Stoughton & Zechner 2007 (#17) | Yes | JFI 16(3):312–342; title "Optimal capital allocation using RAROC(TM) and EVA(R)" | None |
| Chen, Kash, Ruberry & Shnayder 2014 (#41) | Yes | ACM TEAC; DOI 10.1145/2556271 | [M] tag can be upgraded |
| Urwin & Hayman (CFA Institute, Jul 2026) (#52) | Yes | Authors and date confirmed | The title is truncated. Full title: *The Total Portfolio Approach (TPA): A Practical Guide for Navigating the Transition to TPA* |
| Filbeck & Bok (CAIA, Oct 2025) (#51) | Yes | *From Vision to Execution: How Investors Are Operationalizing the Total Portfolio Approach* | None |
| CPP Investments AR F2024 (#53) | Yes | Confirmed | None |
| CalPERS IC item 5a, 17 Nov 2025 (#55) | Yes | Confirmed; authors CFO Nix, Chief Actuary Terando, CIO Gilmore | None |
| NBIM compensation principles (#59) | Yes | Confirmed; laid down 2 Mar 2011, last amended 21 May 2026 | None |

**Erratum (2026-10-18):** the Lamont 1997 (#5) row above and F4 wrongly accepted *JF* 52(1):57–82, which are the pages of Carhart (1997); Lamont is *JF* 52(1):83–109, DOI 10.1111/j.1540-6261.1997.tb03809.x (Crossref; `research/literature/00_LITERATURE_SYNTHESIS.md` §2.3). Separately, Boutilier (#40) does have a 2012 venue version (AAMAS 2012, pp. 737–744, DOI 10.65109/jsvv3990), which the dossier now cites.

**Further references spot-checked (abstracts match the dossier's use):**
- Harris & Raviv 1996 (JF 51(4)): the abstract confirms under-investment when productivity is high and over-investment when it is low. The "initial limit plus audited requests" mechanism, tagged [M] in the dossier, is attributed to this paper by Grinstein et al. (2004).
- Antle & Eppen 1985: "strictly in excess of the cost of capital".
- Osband 1989: "Self-screening tends to be much less valuable than competition".
- Alonso, Dessein & Matouschek 2008: "decentralization can dominate centralization even when coordination is extremely important".
- Tasche 2008: Euler allocation "has been adopted by many financial institutions".
- Erel, Myers & Read 2015: "full and unique allocation".
- Fang, Ivashina & Lerner 2015: seven institutions; solo deals beat co-investments.
- Braun, Jenkinson & Schemmerl 2020: no adverse selection.
- Erel, Flanagan & Weisbach 2024: insignificant net abnormal return; positive against debt-only benchmarks because the funds carry equity risk.
- Gompers, Kaplan & Mukharlyamov 2016: 79 investors, more than $750bn, IRR and multiples.

**No hallucinated references found.**

---

## 4. Reasoning issues and overclaims in the design implications and specification card

Severity: **H** = would produce wrong prices or budgets as written; **M** = material modelling inconsistency; **L** = presentation or robustness.

**R1 (H). The no-regret bands are not jointly feasible.**
- **Where:** §6.3 step 2; §3.1 "Hybrid"; spec card band $\delta_g=\sqrt{2\varepsilon/H_g}$.
- **Problem:** E10 derives each band by moving one group while all the *others re-optimize*. That defines a unilateral band, not a joint envelope. In practice the groups use their bands simultaneously and do not re-optimize for one another.
- **Verifier calculation** (dossier's own E1 data, all upper bands used at once):
  - binding crisis-12m liquidity row: $5.0bn rises to $8.79bn, **+76% of cap**;
  - binding CVaR row: $1.6bn rises to $2.97bn, **+86% of cap**;
  - the drought and 24-month rows also breach, by +24% and +14%.
- **Consequences:**
  - Within-band moves consume binding capacity at a zero price, which contradicts the price logic.
  - The bands (±$0.8–1.3bn, often as large as x\* itself) also exceed the Tier-A proposal threshold of $0.44bn without IC review.
- **Fix:**
  - Draw band headroom from the coupling rows' slack: $\sum_g a^k_g\,\delta_g \le \text{slack}_k$.
  - Or price any within-band increase on a binding row at the dual, keeping the band free only for releases.
  - Or compute a joint ε-optimal region instead of per-group bands.

**R2 (H). The buffer-carry floor contradicts "decision prices are today's duals".**
- **Where:** §6.4 price governance ("Floor the liquidity price at the buffer carry"); §3.2; spec card.
- **Conflict with E1:** E1's binding crisis dual is 1.83%, below the 3.0% default c_buf. The verifier recomputed the groups' decentralized choices at floored prices:
  - floor on the crisis row only: deployment falls from $6.67bn to $1.48bn, PE and Co-investment exit, and crisis-row usage is 1.10 against a 5.0 cap, leaving 78% of the binding capacity idle;
  - floor on all three liquidity rows: deployment falls to $0.
- **Per-row flooring** also charges the same consumption several times, once per horizon or scenario row.
- **Internal contradiction:** the dossier itself says that zero duals everywhere "signal an oversized buffer". That is the marginal-cost reading, and the floor contradicts it.
- **Fix:** make the buffer, and borrowing, endogenous in H, with HQLA holdings carrying cost c_buf. KKT then gives Σ_r μ_r·(relief per $ of HQLA in row r) ≤ c_buf, with equality whenever the buffer is being expanded. So c_buf becomes a *ceiling* on marginal liquidity cost, not a floor. That reproduces the CEBS ¶25 "recalculate the contingent element as the buffer changes" logic without an ad hoc floor. Keep full-cost buffer allocation for *performance* charges only.

**R3 (M–H). Contingent liquidity is double-counted.**
- **Where:** the §6.4 charge formula, CLC and IC pack; the §6.8 DVA identity; the §6.9 calibration target "charges reconcile to dual-valued constraint totals **plus** buffer carry".
- **Problem:**
  - Stressed unfunded draws are part of $a^{h,s}_i$ and so priced at μ in the decision charge. They are charged again in $CLC_g=c_{buf}\sum_h\omega_hO^{stress}_{g,h}$.
  - The IC pack itemizes "liquidity" and "contingent" separately.
  - The DVA identity subtracts both $FTP^{vint}_g$ and $CLC_g$.
- **Fix:** state explicitly that unfunded stressed draws enter *either* the dual-based term *or* the CLC, never both. Change the reconciliation target to "dual-valued totals", or "full-cost buffer allocation" for performance, but not their sum.
- **Note:** §7's double-counting note covers only LAPV against FTP.

**R4 (M). The DVA identity has formula errors.**
- **Where:** §6.8; spec card "Return / cash-flow equations".
- **Units:** the left side, $R_P-R_{RP}$, is a return. The right side, $\sum NAV_i(r_i-r^{FB}_i)-\dots$, is in dollars.
- **Wrong term:** $RC_g$ is defined in §6.2 as the Euler CVaR *contribution*, a risk amount, yet it is subtracted as if it were a charge. It should be $\lambda_R\,RC_g$.
- **Missing offsets:** for the identity to add up, every charge must reappear as income in the TPA and Treasury lines.
- **Fix:** normalize by NAV, or state the identity in dollars on both sides. Replace $RC_g$ with $\lambda_R RC_g$. Add explicit offsetting entries.

**R5 (M). c_buf = E[r_FB] − r_HQLA treats a risk premium as a liquidity cost.**
- **Where:** §1.3; §6.4; §6.9 (default 3.0%).
- **Departure from CEBS:** CEBS Annex 2 defines buffer cost as the *funding cost of the buffer* plus the yield given up on HQLA. Both are near-riskless spreads, and the buffer is sized for about one month.
- **Overlap with the CVaR charge:** the funding basket's expected excess return over HQLA is mainly compensation for risk, which the dossier already charges separately through $\lambda_R\,\partial\mathrm{CVaR}/\partial x_i$.
- **Horizon:** applying c_buf to 12-month stressed draws stretches the CEBS one-month frame.
- **Fix:** set c_buf to the marginal cost of the cheapest liquidity-creating action available to Corporate Finance (facility spread, repo, or the endogenous buffer dual of R2). Show 3% as an upper sensitivity and give the IC a range, for example 1–3%.
- **Effect on the headline:** the $0.34bn a year (38 × 0.30 × 0.03, arithmetic confirmed) scales one-for-one with c_buf.

**R6 (L–M). The Basel 40% "conservative prior" is an analogy, not evidence.**
- **Mismatch:** LCR40.64 sets 30-day run-off rates for credit lines *banks extend* to financial institutions. ADIC's unfunded commitments are LP obligations to funds, drawn at GP discretion, often more slowly in crises, and the stressed horizon here is 12 months.
- **Fix:** take the 12-month stressed draw prior from LP cash-flow data by vintage age (stream 04). Cite Basel only as a cross-check.

**R7 (M). E4 overstates the benefit of a low credibility weight.**
- **Assumption:** the code adds $Z\delta$ to the true α, which assumes the centre's prior $m$ equals the true α. In general $\mu_{post}-\alpha = Z\delta + (1-Z)(m-\alpha)$.
- **Consequence:** with an imperfect prior, a low Z trades inflation damage for prior error and suppresses honest information.
- **Claim affected:** "deadweight loss from $21m to $3.7m at Z = 0.4" holds only with a perfect prior.
- **Fix:** show E4 both with a biased prior and with an honest high-α group, so the IC sees the trade-off.

**R8 (L–M). The elicitability implication goes further than the source.**
- **Claim:** §2.7 says "never for an expected shortfall to be scored".
- **Counter-evidence:** ES is *jointly* elicitable with VaR (Fissler & Ziegel, Annals of Statistics, DOI 10.1214/16-aos1439), so (VaR, ES) pairs can be scored with consistent joint scoring functions. That could matter for overlay tail-hedge P&L forecasts.
- **Fix:** restate it as "do not score ES on its own; score it jointly with the matching quantile if needed".

**R9 (L). The κ = 2.74 calibration conflates bias with dispersion.**
- **Assumptions:** the inversion of BGH's 36% coverage assumes normality, zero bias and independent errors.
- **Why they fail:** BGH's forecasts all target the same market return each quarter, so the effective sample is about the number of quarters, not 13,300. Mis-centering also lowers coverage. The dossier's own error model separates β from κ.
- **Fix:** present 2.74 as an upper-end illustration. The prior median of 1.75 is already more moderate.

**R10 (L–M). The Weitzman plan bonus conflicts with the Jensen citation.**
- **Conflict:** the recommended plan bonus is kinked at the plan (α<β<γ). Jensen (2003) prescribes removing "all kinks" and targets from pay, because kinks invite gaming of *realization* as well as of reporting. Exit timing and NAV marks around the plan are both manageable in PE.
- **Wrong bias targeted:** Weitzman's scheme counters *sandbagging*, whereas ADIC's documented bias is optimism driven by budget stakes. With b > 0 the median is no longer the optimal report (Boutilier).
- **Loose attribution:** "No pay scales with AUM (Jensen 2003)" stretches the source. Jensen's argument concerns budget targets in pay, not AUM scaling.
- **Fix:** present the Weitzman form as a proper quantile score (it adds strength s). Acknowledge the tension with Jensen, and prefer linear pay on realized DVA plus a separate WIS-skill KPI.

**R11 (L). The fusion step shrinks group forecasts twice.**
- **Problem:** "precision scaled by $Z_g/\kappa_g^2$" applies a Bühlmann weight on top of a dispersion-inflated precision. Z is already a precision-based weight, so group information is discounted twice.
- **Fix:** use one coherent hierarchical model in which the forecast enters with precision $1/(\kappa_g^2\hat\sigma^2)$ and the uncertainty in $\beta_g$ is propagated. Drop the extra Z multiplier.

**R12 (L). WIS at K = 1 approximates the CRPS only coarsely.**
- **Problem:** with P10/P50/P90 only, WIS is proper but a crude CRPS proxy. Bracher et al. state the approximation for large K.
- **Fix:** drop the CRPS-equivalence language, or add more quantiles (P5/P25/P75/P95) for groups whose forecasts matter most.

**R13 (L). E5 is inconsistent with E10.**
- **Problem:** E5 sets $B' = 1/q_{PE}$ = 400 $bn per unit of α, the group's own curvature. E10 shows PE's effective curvature is 3.5× higher, so B' is about 113.
- **Effect:** only ratios are quoted in the dossier, so the headline claims survive. Any absolute δ\* (800 bp in the results JSON) is overstated by about 3.5×.
- **Fix:** use $1/H_g$.

**R14 (L). E2 holds by construction.**
- **Problem:** a separable, strictly concave QP plus KKT guarantees that groups facing the duals reproduce x\*. E2 therefore validates the code, not decentralization in practice. In reality α and q are private, and CVaR contributions are not linear in x.
- **Fix:** present E2 as a consistency check, not a "decentralization test".

**R15 (L). λ_R is inconsistent across examples.**
- **Problem:** E1's CVaR dual is 0.81%, while E9 and §6.9 use an external λ_R of 4.75%: the Solvency II risk-margin rate, an insurance transfer-value parameter. The same hedge's risk reduction is valued about 6× higher in E9 than in E1.
- **Fix:** state that decisions use the optimizer dual, and treat 4.75% only as a sanity bound.

**R16 (L). The physical-to-synthetic approval tier is inconsistent.**
- **Problem:** §6.7 approves physical-to-synthetic replacement of long-only holdings at "Tier C within overlay mandate". The move redeems Public Markets' managers (a cross-group action) and consumes margin, which is implicit leverage.
- **Fix:** route it as an internal transfer (Tier B or above) and draw on the leverage or collateral budget.

**R17 (L). The cross-trade analogues are weakest where they are needed.**
- **Problem:** Rule 17a-7 and ERISA §408(b)(19) apply only to securities with readily available quotations. They therefore say least about fund stakes.
- **Fix:** keep the strip-sale, external-bid and fairness-opinion tests as primary. The dossier already notes the gap.

**R18 (L). A peer-practice omission matters for pay design.**
- **Omission:** CPP's HRCC adjusted the total-fund multiplier upward for non-senior employees in FY2024, and CPP announced FY2025 plan changes.
- **Why it matters:** it is direct evidence that the peer most often cited uses discretion to blunt a 0× relative outcome, which is relevant to risk §8.5 and to the pay table.

**R19 (L). Two issues with SAA replications.**
- **Averaging:** the mean of the 10 replication optima need not satisfy each replication's scenario constraints. Use a pooled re-solve, or report envelope ranges.
- **Acronym:** "SAA" is used for both strategic asset allocation and sample-average approximation, which will confuse IC readers.

**R20 (L). The FSI paraphrase in §6.4 is too strong.**
- "Called missing attribution the worst practice" should read "probably the most striking example of poor practice" (F8).

---

## 5. Re-derivation of [I-calc] numbers

Every [I-calc] number quoted in the dossier reproduces from `G8_org_calcs_results.json`:

| Example | Values |
|---|---|
| E1 | Duals 1.834% and 0.807%; charges 125/176/212/171/141/58/−895 bp; net α\* +25/+124/+38/+180/−41/+42/−3,605 bp; budgets and row shares as tabled |
| E2 | Maximum gap 9.8e-6 $bn |
| E3 | Both reduced costs 0 |
| E4 | Z=1: +2.104 / −2.280 / $21.07m. Z=0.4: +0.911 / −0.701 / $3.65m |
| E5 | Ratios 2.5× and 4× |
| E6 | Quantile level 0.5 |
| E7 | WIS 0.086 and 0.0233; skill −2.69; κ 2.74; standard errors 8.9 / 5.7 / 4.0 pp |
| E8 | $50m |
| E9 | 32.8%; 110.9%; crisis dual 10.85% |
| E10 | Curvatures 0.00883 / 0.00808 / 0.00677 / 0.01462 / 0.00563; bands 1.06 / 1.11 / 1.22 / 0.83 / 1.33 |

**Hand checks, all correct:**
- WIS for E7 by hand: (0.5·0.13 + 0.1·0.64)/1.5 = 0.086;
- the Weitzman first-order condition gives (β−α)/(γ−α) = 0.5;
- σ̂ divisor 2×1.2816 = 2.563;
- CLC 38×0.30×0.03 = $0.342bn;
- Tier-A 0.25%×177 = $0.4425bn;
- coverage standard errors √(0.16/n).

The arithmetic is sound. The issues in §4 concern specification and interpretation, not computation.

---

## 6. Overall reliability rating

| Layer | Rating | Basis |
|---|---|---|
| Sourced empirical facts and regulatory text | **High** | 30 of 32 confirmed against primary text, 2 minor wording corrections, no refutations |
| Reference list | **High** | All checked references exist with correct venues; 1 mislabeled WP pointer |
| Design implications and specification card | **Medium** | Five material issues (R1–R5) would distort prices, budgets or attribution if implemented as written |
| **Overall** | **MEDIUM** | Cite the evidence sections to the IC as they stand, with the F5/F8 wording fixes. Revise §6.3, §6.4, §6.8 and the spec card for R1–R5 before computing live prices or envelopes |

---

## Citation corrections (2026-10-18)

- §3: added one erratum line after the citation table. Lamont 1997 is *JF* 52(1):83–109, not 57–82 as accepted in F4 and the §3 row; Boutilier has a 2012 AAMAS version (pp. 737–744). Source: `research/literature/00_LITERATURE_SYNTHESIS.md` §2.3 and `research/literature/G8_org_tpa_economics.lit.md` §2.
- No other entry in this log was changed. F18's RePEc source for the Glaser et al. wording was re-checked and holds. The dossier fixes that close this log's citation notes (Shin & Stulz WP pointer, Gneiting and Chen et al. [M] tags, Urwin & Hayman title, Stein hedge in F1) are listed in the dossier's own "Citation corrections (2026-10-18)" section.
