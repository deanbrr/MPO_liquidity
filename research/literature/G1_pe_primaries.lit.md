# G1 literature review: the PE fund-commitment program, LP skill, pacing and fees

*Literature check of `research/groups/dossiers/G1_pe_primaries.md` for the ADIC multi-period robust TPA framework. Prepared 2026-10-18. The dossier was not edited.*

> **Method note: read this first.** Consensus could not be used. All three attempts at the first query returned the monthly-quota message reproduced verbatim in §6 (it resets on 1 November). Retrying before then would fail, so I stopped calling Consensus.
>
> As a substitute I queried **OpenAlex** directly. It is one of the three indexes Consensus searches over. I used plain relevance search with no year, type or citation filters, the same rule as for Consensus.
>
> Some records had no abstract in OpenAlex. For those I took the abstract from **Crossref** (SSRN deposits) or **Semantic Scholar**, and I say so in each entry. I used one WebSearch, to look for a journal version of Albertus & Denes.
>
> **There are no Consensus URLs in this file.** Every link is the DOI or OpenAlex URL exactly as the API returned it. Citation counts are OpenAlex `cited_by_count` as of 2026-10-18. If the program needs Consensus links specifically, re-run the citation table after 1 November.
>
> Findings below restate retrieved abstracts only. Anything beyond an abstract is tagged **[inference]**.

---

## 1. Summary

### Citation integrity
- **22 academic works checked.** This is every academic reference in the dossier: 16 cited directly and 6 cited "via Stream 04/05".
  - **22 found, 0 mismatched, 0 not found.**
- **Six carry version notes. None is an error.**
  - Albertus & Denes. The SSRN record (3410076) carries the 2019 title "Distorting Private Equity Performance: The Rise of Fund Debt". OpenAlex and one web search found no journal version.
  - Lerner, Schoar, Mao & Zhang (NBER w24941). Published in *JFE* 2022 as Lerner, **Mao, Schoar**, Zhang, "…in Private **Equity**".
  - Brown et al. (w26755). Published in *JFE* 139(2).
  - Cavagnaro et al. The NBER WP the dossier links (w22547) has a different title.
  - Begenau & Siriwardane. Volume and issue are 79(2). The WP (NBER w29887) is titled "How do Private Equity Fees vary across Public Pensions?".
  - Luxenberg et al. (arXiv 2207.07767). Also published in the ICAIF '22 proceedings.
- **Abstracts back the dossier's characterizations.** I checked the abstracts of Hochberg, Ljungqvist & Vissing-Jørgensen (informational holdup), Lerner & Schoar (screening for deep-pocket LPs), Sensoy, Wang & Weisbach (access drove the endowment edge) and Schillinger, Braun & Cornel (standard lines are mainly cash-flow management; extended use alters rankings).
  - The dossier flagged two of these as unverified: Hochberg et al. "not fetched" and Schillinger et al. "summary only". Both caveats are now resolved.
  - This independent check agrees with the verification log (`research/groups/verification/G1_pe_primaries.verify.md` §3).

### Backfill: what the dossier misses
I ran 14 topical searches and 14 title lookups (log in §7). Section 3 annotates 25 papers, all missing from the G1 dossier. The main gaps:

1. **Seminal and current persistence evidence.**
   - The dossier cites neither the founding paper, Kaplan & Schoar (2005, *JF*, 1,949 cites), nor the deal-level paper showing buyout persistence "has substantially declined", Braun, Jenkinson & Stoff (2017, *JFE*).
2. **Non-performance signals for choosing GPs.** Two papers do better than track records:
   - Fernández Tamayo et al. (2023): machine learning on fund prospectuses predicts performance, while prior performance does not.
   - Ercan, Kaplan & Strebulaev (2025): the history of interim marks (staleness, markdown frequency) predicts outcomes.
3. **Diseconomies of fund size.** Bhardwaj et al. (2025) estimate causally that a 1% increase in fund size cuts net IRR by 0.1pp. The dossier relies on "no significant buyout size–performance relation".
4. **Fee-contract economics.**
   - Metrick & Yasuda (2010): about two-thirds of GP revenue is fixed.
   - Robinson & Sensoy (2013): pay is unrelated to net performance.
   - Hüther et al. (2020): deal-by-deal carry is associated with *higher* net returns.
   - Phalippou, Rauch & Umber (2018): portfolio-company fees exceed 6% of equity invested.
5. **LP scale, access and sovereign governance.**
   - Scale: Dyck & Pomorski (2016); Da Rin & Phalippou (2017).
   - Investor-specific SDFs: Korteweg, Panageas & Systla (2026, *JFE*) find access, not selection skill.
   - Non-US LPs: Brav et al. (2023).
   - Home bias: Hochberg & Rauh (2013).
   - Political involvement in SWFs: Bernstein, Lerner & Schoar (2013).
6. **Liquidity theory and learned pacing.**
   - Dimmock, Wang & Yang (2024): staggered lockups as "liquidity diversification", with endogenous rebalancing bands.
   - Kieffer et al. (2023): explainable evolutionary search for recommitment rules.
7. **The co-investment link, central to ADIC's hybrid direct/fund model.** Fang, Ivashina & Lerner (2015) and Braun, Jenkinson & Schemmerl (2020) disagree on whether co-investments suffer adverse selection. Tuft (2023) models co-investment as surplus-sharing and a liquidity-timing option.
8. **Risk adjustment.** Franzoni, Nowak & Phalippou (2012): a liquidity-risk premium of about 3% a year takes PE alpha to zero.
9. **Survey.** Ljungqvist (2024), CFA Institute Research Foundation.

### Challenges (detail in §5)
The literature most directly challenges five dossier positions:
1. The track-record learning rule, and the claim that the remaining edge is "disciplined, graded re-up decisions".
2. Up-sizing re-ups without any fund-size penalty.
3. An implicit preference for LP-friendly (whole-of-fund) waterfalls.
4. Treating fees as a pure drag term in the objective.
5. A positive default value for co-investment flow, and a hurdle of 0 to +1% that ignores the liquidity-risk premium.

No academic paper I found measures how much access an LP loses after skipping a re-up or selling an interest. The dossier's Δp(access) parameters therefore remain judgment, consistent with verification issue R8.

---

## 2. Citation-integrity table (22 checked)

Status key: **found** = metadata matches the version cited. "Version note" = another version exists with different metadata. The Consensus column is "n/a" because the quota was exhausted. The OpenAlex record (as returned) is given there instead.

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| Albertus & Denes (2020), "Private Equity Fund Debt: Capital Flows, Performance, and Agency Costs" (NBER conf. PDF, 26 May 2020) | found (WP; version note) | The SSRN record for the same paper is "Distorting Private Equity Performance: The Rise of Fund Debt", Albertus & Denes, *SSRN Electronic Journal* (2019), DOI https://doi.org/10.2139/ssrn.3410076 (11 cites). No journal version found (OpenAlex; one WebSearch). Cite both titles as versions of SSRN 3410076. | n/a · OpenAlex [W2955225230](https://openalex.org/W2955225230) |
| Begenau & Siriwardane (2024), "Fee Variation in Private Equity", *JF* pp. 1199–1247 | found (version note) | *The Journal of Finance* **79(2)** 1199–1247, DOI https://doi.org/10.1111/jofi.13319 (32 cites). WP: "How do Private Equity Fees vary across Public Pensions?", NBER (2022), https://doi.org/10.3386/w29887 | n/a · OpenAlex [W4392132144](https://openalex.org/W4392132144) |
| Brown, Gredil & Kaplan (2019), *JFE* 132(2); NBER w22493 | found | *JFE* 132(2) **267–297**, DOI https://doi.org/10.1016/j.jfineco.2018.10.011 (online 2018; 203 cites) | n/a · OpenAlex [W3121213291](https://openalex.org/W3121213291) |
| Brown, Harris, Hu, Jenkinson, Kaplan & Robinson (2020), NBER w26755 | found (WP; published version exists) | *JFE* 139(2) 561–577, DOI https://doi.org/10.1016/j.jfineco.2020.08.014 (48 cites). NBER: https://doi.org/10.3386/w26755 | n/a · OpenAlex [W2896332257](https://openalex.org/W2896332257) |
| Barber & Yasuda (2017), *JFE* 124(1) | found | *JFE* 124(1) **172–194**, DOI https://doi.org/10.1016/j.jfineco.2017.01.001 (200 cites) | n/a · OpenAlex [W3124335714](https://openalex.org/W3124335714) |
| Cavagnaro, Sensoy, Wang & Weisbach (2019), *JF* 74(6) 3089–3134; NBER w22547 | found (version note) | DOI https://doi.org/10.1111/jofi.12783 (65 cites). The linked WP is titled "Measuring Institutional Investors' Skill from Their Investments in Private Equity" (NBER 2016, https://doi.org/10.3386/w22547). The published abstract adds that results "are stronger in the earlier part of the sample period and for venture funds". | n/a · OpenAlex [W2950720792](https://openalex.org/W2950720792) |
| Harris, Jenkinson & Kaplan (2014), "Private Equity Performance: What Do We Know?", *JF*; NBER w17874 | found | *JF* **69(5) 1851–1882**, DOI https://doi.org/10.1111/jofi.12154 (594 cites) | n/a · OpenAlex [W3121165378](https://openalex.org/W3121165378) |
| Harris, Jenkinson, Kaplan & Stucke (2020/2023), NBER w28109; *JCF* 81, 102361 | found | *Journal of Corporate Finance* 81, 102361 (2023), DOI https://doi.org/10.1016/j.jcorpfin.2023.102361 (75 cites); NBER https://doi.org/10.3386/w28109 (87 cites) | n/a · OpenAlex [W4320913257](https://openalex.org/W4320913257) |
| Korteweg & Sorensen (2017), *JFE* 124(3) 535–562 | found | DOI https://doi.org/10.1016/j.jfineco.2017.03.006 (167 cites) | n/a · OpenAlex [W3124196106](https://openalex.org/W3124196106) |
| Lerner & Schoar (2002/2004), "The Illiquidity Puzzle", NBER w9146; *JFE* 72(1) | found | *JFE* 72(1) **3–40**, DOI https://doi.org/10.1016/s0304-405x(03)00203-4 (OpenAlex year 2003 = online; 259 cites). The NBER abstract confirms the screening mechanism: liquid ("deep pocket") investors lower the *manager's* future cost of capital. | n/a · OpenAlex [W3125046747](https://openalex.org/W3125046747) |
| Lerner, Schoar & Wongsunwai (2007), *JF* 62(2) 731–764; NBER w11136 | found | DOI https://doi.org/10.1111/j.1540-6261.2007.01222.x (427 cites). The NBER WP (2005) lists the third author as "Wan Wong" and its title ends "Choices?" | n/a · OpenAlex [W3123389049](https://openalex.org/W3123389049) |
| Lerner, Schoar, Mao & Zhang (2018), "Investing Outside the Box: … Private Capital", NBER w24941 | found (WP; published version differs) | Published: Lerner, **Mao, Schoar**, Zhang, "Investing outside the box: Evidence from alternative vehicles in **private equity**", *JFE* 143(1) 359–380 (2022; online 2021), DOI https://doi.org/10.1016/j.jfineco.2021.05.034 (70 cites) | n/a · OpenAlex [W2889193665](https://openalex.org/W2889193665) |
| Phalippou (2009), *JEP* 23(1) 147–166 | found | DOI https://doi.org/10.1257/jep.23.1.147 (140 cites) | n/a · OpenAlex [W2171311254](https://openalex.org/W2171311254) |
| Schillinger, Braun & Cornel (2019), SSRN 3434112 ("summary only") | found | *SSRN Electronic Journal*, DOI https://doi.org/10.2139/ssrn.3434112 (10 cites). This confirms the SSRN ID the verification left open. The Crossref abstract matches the dossier's summary (moderate effects from standard lines; extended lines can raise time-sensitive measures and alter rankings). | n/a · OpenAlex [W2969446750](https://openalex.org/W2969446750) |
| Sensoy, Wang & Weisbach (2014), *JFE* 112(3) 320–343 | found | DOI https://doi.org/10.1016/j.jfineco.2014.02.006 (165 cites) | n/a · OpenAlex [W3124207489](https://openalex.org/W3124207489) |
| Hochberg, Ljungqvist & Vissing-Jørgensen (2014), "Informational Hold-Up…", *RFS* 27(1) ("not fetched") | found | *RFS* 27(1) **102–152**, DOI https://doi.org/10.1093/rfs/hht046 (online 2013; 201 cites). The published spelling is "Holdup". The abstract confirms the mechanism and adds that "up to two-thirds of VC firms lack skill". | n/a · OpenAlex [W3122047865](https://openalex.org/W3122047865) |
| Takahashi & Alexander (2002) (via Stream 04) | found | "Illiquid Alternative Asset Fund Modeling", *JPM* 28(2) 90–100, DOI https://doi.org/10.3905/jpm.2002.319836 (81 cites) | n/a · OpenAlex [W2178410718](https://openalex.org/W2178410718) |
| Luxenberg et al. (2022), arXiv 2207.07767 (via Stream 04) | found (version note) | "Strategic Asset Allocation with Illiquid Alternatives", https://doi.org/10.48550/arxiv.2207.07767. Also published in the ICAIF '22 proceedings, pp. 249–256 (Luxenberg, Boyd, van Beek, Cao, Kochenderfer), https://doi.org/10.1145/3533271.3561769 | n/a · OpenAlex [W4286235989](https://openalex.org/W4286235989) |
| Sorensen, Wang & Yang (2014), NBER w19612 (via Stream 04) | found | "Valuing Private Equity", *RFS* 27(7) 1977–2021, DOI https://doi.org/10.1093/rfs/hhu013 | n/a · OpenAlex [W2891860082](https://openalex.org/W2891860082) |
| Robinson & Sensoy (2016), NBER w17428 (via Stream 04) | found | "Cyclicality, performance measurement, and cash flow liquidity in private equity", *JFE* 122(3) 521–543, DOI https://doi.org/10.1016/j.jfineco.2016.09.008 (208 cites) | n/a · OpenAlex [W78518972](https://openalex.org/W78518972) |
| Nadauld et al. (2019), NBER w22404 (via Stream 05) | found | Nadauld, Sensoy, Vorkink & Weisbach, "The liquidity cost of private equity investments…", *JFE* 132(3) 158–181, DOI https://doi.org/10.1016/j.jfineco.2018.11.007 (105 cites) | n/a · OpenAlex [W3125297906](https://openalex.org/W3125297906) |
| Gourier, Phalippou & Westerfield (2024), DOI 10.1111/jofi.13382 (via Stream 04) | found | "Capital Commitment", *JF* 79(5) 3407–3457 (16 cites) | n/a · OpenAlex [W4401970143](https://openalex.org/W4401970143) |

**Not counted as citations:**
- Method names: Mincer–Zarnowitz, Bühlmann–Straub. Stream 04's review checked Bühlmann.
- Industry sources: ILPA, Bain, MSCI, Evercore, Cliffwater, Hamilton Lane, Cherry Bekaert, CEM, Cobalt. The verification log checked these.

---

## 3. Annotated bibliography (25 papers)

Tags:
- **[missed]**: not cited in the G1 dossier.
- **[challenge]**: contradicts or qualifies a dossier recommendation (§5).
- "abstract via …": the abstract came from a source other than OpenAlex.

"Finding" restates the abstract; quoted phrases are the authors' words. **"Relevance" paragraphs are my inferences for ADIC** unless they quote the paper.

### A. GP selection: persistence, learning and signals

**1. [Private Equity Performance: Returns, Persistence, and Capital Flows](https://doi.org/10.1111/j.1540-6261.2005.00780.x)** [missed]
- Kaplan, S. N., & Schoar, A. · 2005 · *The Journal of Finance* 60(4) 1791–1823 · 1,949 cites · DOI 10.1111/j.1540-6261.2005.00780.x
- **Finding.**
  - Average net-of-fee returns "approximately equal the S&P 500", with substantial heterogeneity.
  - Returns "persist strongly across subsequent funds of a partnership". Better performers raise larger follow-on funds, but the relation is concave.
  - Market entry and fund performance are procyclical, and "established funds are less sensitive to cycles than new entrants".
- **Relevance.**
  - This is the founding result behind the dossier's §2.3 skill section, yet the dossier does not cite it.
  - Procyclical entry supports keying vintage tilts to the fundraising-cycle state $F_t$ and treating new entrants as more cyclical [inference].
  - Treat it as the historical prior only. Later work (items 2 and 3, HJKS) shows buyout persistence weakened after 2000.

**2. [How persistent is private equity performance? Evidence from deal-level data](https://doi.org/10.1016/j.jfineco.2016.01.033)** [missed]
- Braun, R., Jenkinson, T., & Stoff, I. · 2017 (online 2016) · *Journal of Financial Economics* 123(2) 273–291 · 174 cites · DOI 10.1016/j.jfineco.2016.01.033 · abstract via Crossref (SSRN version https://doi.org/10.2139/ssrn.2314400)
- **Finding.**
  - The data cover 13,523 portfolio-company investments by 865 buyout funds.
  - "Persistence of fund managers has substantially declined as the private equity sector has matured and become more competitive." Past performance is now "a poor predictor of the future".
- **Relevance.**
  - This is independent, deal-level support for the dossier's caution on post-2000 buyout persistence.
  - It argues for low learning gains on buyout track records, and against access penalties for non-elite buyout GPs [inference].

**3. [Limited Partners versus Unlimited Machines; Artificial Intelligence and the Performance of Private Equity Funds](https://doi.org/10.2139/ssrn.4490991)** [missed; challenge]
- Fernández Tamayo, B., Braun, R., Lopez-de-Silanes, F., Phalippou, L., & Sigrist, N. · 2023 · *SSRN* working paper · 2 cites · DOI 10.2139/ssrn.4490991 · abstract via Crossref
- **Finding.**
  - The sample is 395 PE fund prospectuses.
  - Performance "is unrelated to quantitative information, such as prior performance, and measures of document readability". Fundraising success correlates with fund characteristics but not with future performance.
  - Machine learning on *qualitative* information predicts performance: the spread between the top and bottom terciles of predicted success is "about 25%".
- **Relevance.**
  - It undercuts a GP-belief update driven mainly by track records (§2.3, §6.5 R1).
  - It suggests a graded document-reading agent as an additional signal [inference]. It is a working paper; replicate it on ADIC's own PPM archive before relying on it.

**4. [Interim Valuations, Predictability, and Outcomes in Private Equity](https://doi.org/10.3386/w33637)** [missed; challenge]
- Ercan, E. Y., Kaplan, S. N., & Strebulaev, I. A. · 2025 · NBER Working Paper w33637 · 4 cites · DOI 10.3386/w33637 · abstracts via Crossref (SSRN versions https://doi.org/10.2139/ssrn.5215933, 2025, and https://doi.org/10.2139/ssrn.4833819, 2024)
- **Finding.**
  - The data are US buyout and VC portfolio-company investments.
  - The history of reported valuations is informative beyond the latest mark. Investments with "greater past staleness or more frequent markdowns tend to perform more poorly", and exit timing is predictable.
  - Interim returns, staleness and markdown frequency together help predict left- and right-tail outcomes, "as early as the first year".
  - The 2024 version states the staleness and markdown effect holds "particularly for buyout funds". It adds that "investments with larger reported interim marks tend to have lower future returns", that is, "past reported returns negatively predict future realized returns".
- **Relevance.**
  - This gives concrete look-through features for forecast fusion and grading (§6.9) and for SELL screening.
  - It also implies that interim marks can carry *negative* information, which the dossier's Kalman rule cannot represent [inference].

**5. [Pay for Performance from Future Fund Flows: The Case of Private Equity](https://doi.org/10.1093/rfs/hhr141)** [missed]
- Chung, J.-W., Sensoy, B. A., Stern, L., & Weisbach, M. S. · 2012 · *The Review of Financial Studies* 25(11) 3259–3304 · 202 cites · DOI 10.1093/rfs/hhr141
- **Finding.**
  - Indirect pay for performance from future fundraising "is of the same order of magnitude as direct pay for performance from carried interest".
  - It is stronger for buyout than for VC, and it "declines in the sequence of a partnership's funds".
- **Relevance.**
  - LP re-up decisions are part of GP compensation. ADIC's re-up, skip and up-size choices are therefore an incentive lever, strongest with early-sequence buyout GPs.
  - The GP side of the access sub-model (§6.5 R3) should depend on fund sequence [inference].

**6. [Does Fund Size Affect Private Equity Performance? Evidence from Donation Inflows to Private Universities](https://doi.org/10.3386/w33596)** [missed; challenge]
- Bhardwaj, A., Gupta, A., Howell, S. T., & Zimmerschied, K. · 2025 · NBER Working Paper w33596 · 4 cites · DOI 10.3386/w33596
- **Finding.**
  - Gifts to universities supply capital to managers with existing relationships, and serve as an instrument for fund size.
  - Returns decrease with scale: "a 1% size increase reduces net IRR by 0.1 percentage points".
  - Larger funds do larger deals, which perform worse. Risk does not change, partly because the additional deals are more levered.
- **Relevance.**
  - It contradicts the dossier's reliance on "no significant buyout size–performance relation" (§2.3).
  - A LEVER via up-sized re-ups into fast-growing funds needs a size penalty on the alpha prior.
  - ADIC's own large tickets contribute to fund growth [inference]. Do not extrapolate the elasticity linearly to large size steps.

**7. [Private Equity Fund Returns and Performance Persistence](https://doi.org/10.1093/rof/rfu045)** [missed]
- Marquez, R., Nanda, V., & Yavuz, M. D. · 2015 (online 2014) · *Review of Finance* 19(5) 1783–1823 · 35 cites · DOI 10.1093/rof/rfu045 · abstract via Crossref
- **Finding.**
  - This is a theory paper. Successful managers keep funds oversubscribed and do not raise size or fees, because they want to attract high-quality entrepreneurs.
  - A manager may "keep fund size small to limit the cost of effort, hoping to manipulate entrepreneurs' beliefs about his ability".
- **Relevance.**
  - It gives a theoretical basis for allocation cutbacks ($\tilde K=\min(K,A_{g,f})$, §6.3): access, not price, rations demand for top GPs [inference].
  - Read with item 6: GPs that do scale up give up part of this edge [inference].

### B. LP scale, access and governance

**8. [Investor Scale and Performance in Private Equity Investments](https://doi.org/10.1093/rof/rfv030)** [missed]
- Dyck, A., & Pomorski, Ł. · 2016 (online 2015) · *Review of Finance* 20(3) 1081–1106 · 42 cites · DOI 10.1093/rof/rfv030
- **Finding.**
  - DB plans with large PE holdings earn substantially greater returns. A one-s.d. increase in PE holdings is associated with "4% greater returns per year".
  - Up to one-third comes from lower costs: avoiding funds of funds and investing directly.
  - The bulk comes from superior gross returns, only partly explained by access and experience.
- **Relevance.**
  - It supports the dossier's view that scale is valuable, but locates most of the benefit in *gross* returns (due diligence), not only fees.
  - It supports ADIC's hybrid direct/fund model as a cost lever [inference]. The result is a cross-sectional association, not a causal estimate.

**9. [The importance of size in private equity: Evidence from a survey of limited partners](https://doi.org/10.1016/j.jfi.2016.07.001)** [missed]
- Da Rin, M., & Phalippou, L. · 2017 (online 2016) · *Journal of Financial Intermediation* 31, 64–76 · 80 cites · DOI 10.1016/j.jfi.2016.07.001
- **Finding.**
  - LPs with larger PE allocations are more specialized and have a wider scope of due diligence and investment activity.
  - Experience, type, location, compensation structure and number of funds "play no role". "Endowments are not special."
- **Relevance.**
  - The LP edge comes from scale-driven specialization, not from being an endowment.
  - This supports resourcing the PE group's diligence in proportion to its $52bn book, and qualifies the dossier's endowment-model framing in §5 item 3 [inference].

**10. [Private equity for pension plans? Evaluating private equity performance from an investor's perspective](https://doi.org/10.1016/j.jfineco.2026.104336)** [missed; challenge]
- Korteweg, A., Panageas, S., & Systla, A. · 2026 · *Journal of Financial Economics* 184, 104336 · 2 cites · DOI 10.1016/j.jfineco.2026.104336 · abstract via Crossref (SSRN https://doi.org/10.2139/ssrn.5032558; NBER w33194)
- **Finding.**
  - PE performance is evaluated with investor-specific stochastic discount factors.
  - "Plans invest in PE funds with higher average risk-adjusted performance. This is mainly due to access to successful PE managers, not superior selection skill."
  - Some plans get higher PE returns by taking more risk without earning higher, and sometimes lower, risk-adjusted returns. The authors read this as "consistent with agency problems within plans".
- **Relevance.**
  1. Value commitments with ADIC's own SDF, which is oil- and fiscal-linked (Streams 03 and 11), rather than a generic PME.
  2. The edge is access more than selection, which cuts against the dossier's "graded re-up decisions" as the remaining edge.
  3. Add an IC check that higher-return proposals are not simply higher-risk ones [inference].

**11. [Private Equity and Venture Capital Fund Performance: Evidence from a Large Sample of Israeli Limited Partners](https://doi.org/10.2139/ssrn.4541887)** [missed]
- Brav, A., Lakan, G., & Yafeh, Y. · 2023 · *SSRN* working paper · 7 cites · DOI 10.2139/ssrn.4541887
- **Finding.**
  - Israeli LPs' realized performance was "slightly below" US-literature estimates. The shortfall is driven by limited access to top seasoned US funds and limited skill in picking first-time US funds.
  - Investments in local funds outperformed foreign ones.
  - Preqin "tends to omit small funds as well as funds with poor performance".
- **Relevance.**
  - It is the closest available evidence for a non-US sovereign LP.
  - Set ADIC's achievable alpha prior below US-LP benchmarks unless access is demonstrated, and treat commercial-database benchmarks as possibly biased upward [inference].

**12. [Local Overweighting and Underperformance: Evidence from Limited Partner Private Equity Investments](https://doi.org/10.1093/rfs/hhs128)** [missed]
- Hochberg, Y. V., & Rauh, J. · 2013 (online 2012) · *The Review of Financial Studies* 26(2) 403–451 · 184 cites · DOI 10.1093/rfs/hhs128
- **Finding.**
  - Public pension funds overweight home-state PE: 9.8% of aggregate PE investments and 16.5% for the average LP.
  - Their in-state investments underperform "by two to four percentage points".
  - States with more self-dealing political climates invest more locally. The total cost is "$1.2 billion per year".
- **Relevance.**
  - For a sovereign fund with possible domestic or regional mandates: tag home-region commitments, benchmark them separately, and disclose them to the IC [inference].
  - Brav et al. (item 11) find the opposite sign for Israeli LPs, so do not impose a default penalty.

**13. [The Investment Strategies of Sovereign Wealth Funds](https://doi.org/10.1257/jep.27.2.219)** [missed]
- Bernstein, S., Lerner, J., & Schoar, A. · 2013 · *Journal of Economic Perspectives* 27(2) 219–238 · 236 cites · DOI 10.1257/jep.27.2.219
- **Finding.**
  - SWFs with greater involvement of political leaders in fund management "favor short-term economic policy goals in their respective countries at the expense of longer-term maximization of returns".
  - SWFs also face transparency and scaling problems.
- **Relevance.**
  - This is a governance prior for ADIC's shadow IC.
  - Record policy-motivated commitments and pacing overrides separately from investment-motivated ones, and attribute their cost [inference].

### C. Fees and contract design

**14. [The Economics of Private Equity Funds](https://doi.org/10.1093/rfs/hhq020)** [missed]
- Metrick, A., & Yasuda, A. · 2010 · *The Review of Financial Studies* 23(6) 2303–2341 · 670 cites · DOI 10.1093/rfs/hhq020
- **Finding.**
  - The data are contracts for 238 funds held by one large LP.
  - "About two-thirds of expected revenue comes from fixed-revenue components that are not sensitive to performance."
  - Buyout is more scalable than VC: BO managers grow fund size faster, with higher revenue per partner in later funds.
- **Relevance.**
  - In negotiation and in the fee state $\mathcal F_i$, weight the management-fee basis and step-downs above headline carry.
  - BO scalability links to the size penalty in item 6 [inference].

**15. [Do Private Equity Fund Managers Earn Their Fees? Compensation, Ownership, and Cash Flow Performance](https://doi.org/10.1093/rfs/hht055)** [missed; challenge]
- Robinson, D. T., & Sensoy, B. A. · 2013 (online 2012) · *The Review of Financial Studies* 26(11) 2760–2797 · 256 cites · DOI 10.1093/rfs/hht055 · abstract from the NBER version (https://doi.org/10.3386/w17942)
- **Finding.**
  - There is no evidence that higher compensation or lower GP ownership goes with worse net-of-fee performance. Compensation is "largely unrelated to net-of-fee cash flow performance".
  - Pay rises and shifts to fixed components during fundraising booms.
  - Distributions around fee and carry triggers suggest an agency conflict. Managers with higher pay "earn back their pay by delivering higher gross performance".
- **Relevance.**
  - A fee-minimizing objective term (§6.7 "− fees") can mis-rank GPs.
  - Useful fee signals are boom-vintage fee drift and behaviour around carry triggers, not fee level as such [inference].

**16. [Paying for Performance in Private Equity: Evidence from Venture Capital Partnerships](https://doi.org/10.1287/mnsc.2018.3274)** [missed; challenge]
- Hüther, N., Robinson, D. T., Sievers, S., & Hartmann-Wendels, T. · 2020 (online 2019) · *Management Science* 66(4) 1756–1782 · 46 cites · DOI 10.1287/mnsc.2018.3274
- **Finding.**
  - "GP-friendly" contracts, which pay carry deal by deal instead of after a benchmark return, "are associated with higher returns, both gross and net of fees".
  - The result is robust to persistence, period effects and other terms, and is related to exit-timing incentives.
- **Relevance.**
  - It qualifies the dossier's ILPA-anchored side-letter stance (§2.5, §5 item 4).
  - Price the waterfall type, with clawback and escrow, rather than treating whole-of-fund as a screen, which may select against stronger VC managers [inference].
  - The evidence is from VC partnerships.

**17. [Private equity portfolio company fees](https://doi.org/10.1016/j.jfineco.2018.05.010)** [missed]
- Phalippou, L., Rauch, C., & Umber, M. P. · 2018 · *Journal of Financial Economics* 129(3) 559–585 · 84 cites · DOI 10.1016/j.jfineco.2018.05.010 · abstract via Semantic Scholar
- **Finding.**
  - GP fees charged to portfolio companies total "$20 billion" over twenty years, "over 6% of the equity invested".
  - They do not vary with business cycles, company characteristics or GP performance. They vary across GPs and persist within them.
  - GPs charging the least raised more capital after the financial crisis.
- **Relevance.**
  - The fee model (T8, $\mathcal F_i$) should carry a GP-level portfolio-company-fee intensity and an offset rate, not assume a full ILPA 100% offset.
  - Because these fees persist within GPs, they are a due-diligence feature [inference].

### D. Fund-level mechanics: subscription lines, pacing and recycling

**18. [Unpacking Private Equity Performance](https://doi.org/10.3905/jpm.2024.1.604)** [missed]
- Brown, G. W., & Volckmann, W. M. · 2024 · *The Journal of Portfolio Management* 50(7) 100–115 · 6 cites · DOI 10.3905/jpm.2024.1.604
- **Finding.** The paper simulates funds:
  - Intermediate IRRs, "likely observed during fundraising periods", are "strongly affected by subscription lines and deployment pacing".
  - Intermediate MOICs are only weakly affected by lines but strongly by pacing.
  - Both IRR and MOIC are "strongly affected by recycle deal accounting methodology".
- **Relevance.** Before the "actual" series enters fusion and grading (§6.9), adjust it for lines, deployment pacing and recycling, not only lines. This supports the dossier's preference for PME or direct alpha [inference].

### E. Pacing, commitment and liquidity

**19. [The Endowment Model and Modern Portfolio Theory](https://doi.org/10.1287/mnsc.2023.4759)** [missed]
- Dimmock, S. G., Wang, N., & Yang, J. · 2024 (online 2023) · *Management Science* 70(3) 1554–1579 · 32 cites · DOI 10.1287/mnsc.2023.4759
- **Finding.** The model has illiquid alternatives with lockups and proportional liquidation costs:
  - Staggered lockups give "liquidity diversification", raising alternatives allocations and welfare.
  - Lockups combined with secondary-market costs create "endogenous and time-varying rebalancing boundaries".
  - In crisis states, holdings "deviate significantly from target allocations".
- **Relevance.** This is formal support for:
  - vintage diversification as a liquidity tool;
  - no-trade bands and pacing corridors instead of point targets;
  - the dossier's lesson that the denominator spike should be tolerated, since deviation in a crisis is optimal [inference].

**20. [Learning private equity recommitment strategies for institutional investors](https://doi.org/10.3389/frai.2023.1014317)** [missed]
- Kieffer, E., Meyer, T., Gloukoviezoff, G., Lucius, H., & Bouvry, P. · 2023 · *Frontiers in Artificial Intelligence* 6, 1014317 · 4 cites · DOI 10.3389/frai.2023.1014317
- **Finding.**
  - The authors propose "a trustworthy and explainable A.I. approach" to recommitment strategies.
  - Using intensive portfolio simulation and evolutionary computing, they show that "efficient and dynamic recommitment strategies can be brought forth automatically". The strategies balance target exposure against the risk of default.
- **Relevance.**
  - This is a published template for the dossier's "parametric policy search" (CMA-ES), and for a pacing agent that proposes explainable rules to the IC.
  - The authors also have an evolutionary version (IEEE SSCI 2021) and a PPO reinforcement-learning version (CCIS 2022); see §4.7 [inference].

### F. The co-investment link (ADIC's hybrid direct/fund model)

**21. [The disintermediation of financial markets: Direct investing in private equity](https://doi.org/10.1016/j.jfineco.2014.12.002)** [missed; challenge]
- Fang, L. H., Ivashina, V., & Lerner, J. · 2015 (online 2014) · *Journal of Financial Economics* 116(1) 160–178 · 150 cites · DOI 10.1016/j.jfineco.2014.12.002 · abstract via Semantic Scholar
- **Finding.**
  - The data are direct investments by seven large institutions.
  - Solo investments outperform co-investments and PE fund benchmarks, especially where information problems are mild (proximate, later-stage deals) and by avoiding inflow booms.
  - Co-investments' "poor performance … appears to result from fund managers' selective offering of large deals".
- **Relevance.** Do not assume a positive value for the co-investment flow attached to G1 commitments (§6.5 R6, ρ ≈ 0.2). GP selection of what to offer is a real risk [inference].

**22. [Adverse selection and the performance of private equity co-investments](https://doi.org/10.1016/j.jfineco.2019.01.009)** [missed; challenge]
- Braun, R., Jenkinson, T., & Schemmerl, C. · 2020 · *Journal of Financial Economics* 136(1) 44–62 · 73 cites · DOI 10.1016/j.jfineco.2019.01.009 · abstract via Semantic Scholar
- **Finding.**
  - "In contrast to Fang et al. (2015) we find no evidence of adverse selection." Gross returns of co-investments and other deals are similar, and co-investments cost less.
  - "Reasonably sized portfolios of co-investments have significantly out-performed fund returns" net of fees.
- **Relevance.** Read together with item 21: the sign of co-investment value is uncertain and depends on portfolio size and selection. Make ρ and value per dollar scenario parameters with both signs [inference].

**23. [Beyond Fees: Co-Investment and the Design of Private Equity Relationships](https://doi.org/10.2139/ssrn.4559453)** [missed]
- Tuft, A. · 2023 · *SSRN* working paper · 3 cites · DOI 10.2139/ssrn.4559453 · abstract via Crossref
- **Finding.**
  - Co-investment is a channel through which "GPs share surplus with those holding greater bargaining power". It complements, rather than substitutes for, main-fund fee discounts.
  - Volcker-rule shock: "a one standard deviation increase in a fund's exposure to the loss of bank LPs raises co-investment by 11.7%".
  - LPs more exposed to liquidity risk co-invest more, which is consistent with co-investment giving "control over the timing of their capital outlays". This holds for LP-discretion deals, not GP-directed ones.
- **Relevance.**
  - Co-investment rights belong in the value of a commitment, both as surplus and as a discretionary liquidity-timing option.
  - This links G1 commitments, G4 co-investment and Corporate Finance's liquidity gate [inference].

### G. Risk adjustment and survey

**24. [Private Equity Performance and Liquidity Risk](https://doi.org/10.1111/j.1540-6261.2012.01788.x)** [missed; challenge]
- Franzoni, F., Nowak, E., & Phalippou, L. · 2012 · *The Journal of Finance* 67(6) 2341–2373 · 260 cites · DOI 10.1111/j.1540-6261.2012.01788.x
- **Finding.**
  - PE is significantly exposed to the same liquidity risk factor as public equity.
  - The "unconditional liquidity risk premium is about 3% annually", and including it in a four-factor model "reduces alpha to zero".
  - The link runs through a funding-liquidity channel.
- **Relevance.**
  - GP alpha used in beliefs, access values and the LEVER test ($\mu_g-h_s$) should be measured net of a liquidity factor. A hurdle of 0 to +1% over the strategy benchmark omits it.
  - PE drawdowns also co-move with ADIC's own funding stress [inference].

**25. [The Economics of Private Equity: A Critical Review](https://doi.org/10.56227/24.1.10)** [missed]
- Ljungqvist, A. P. · 2024 · CFA Institute Research Foundation report (publisher per Crossref) · 8 cites · DOI 10.56227/24.1.10
- **Finding.** A critical synthesis of the academic literature, focused on PE performance as an asset class and on value creation. It also reviews "key aspects of investing in private equity … when forming and managing a portfolio of private equity funds".
- **Relevance.** A single up-to-date survey to anchor the PE group's evidence base and IC briefings. Only the abstract was read; anything beyond it is [inference].

---

## 4. Missed-but-important papers and their design implications

Symbols follow the dossier's §6. Every item is **[inference]** built on the cited abstracts unless it is a direct quote.

### 4.1 State variables (additions to §6.2)
| Symbol | Meaning | Level | Source |
|---|---|---|---|
| $\Delta S_g$ | Fund-size step-up: target size ÷ previous fund size, plus average deal size | GP | Bhardwaj et al. (#6); Metrick & Yasuda (#14); Kaplan & Schoar (#1) |
| $NS_g$ | New-style flag: a buyout GP launching a new fund style | GP | HJKS 2023 abstract (cited): new styles perform "noticeably lower for buyouts (but not VC)" |
| $\tau^{delay}_g$ | Fundraising delay against the GP's normal cycle | GP | HJKS 2023 abstract: GPs avoid "fundraising when interim performance is poor" |
| $(st_i, md_i, IM_i)$ | Interim-mark history per holding: staleness count, markdown frequency, interim multiple | Fund interest (look-through) | Ercan et al. (#4) |
| $q_g$ | Qualitative diligence score from PPM and LPA text | GP / fund | Fernández Tamayo et al. (#3) |
| $PCF_g$, $o_i$ | Portfolio-company fee intensity; fee-offset rate | GP / fund | Phalippou, Rauch & Umber (#17) |
| $wf_i$ | Waterfall type (deal-by-deal or whole-of-fund) and clawback security | Fund | Hüther et al. (#16) |
| $seq_g$ | Fund sequence number (implicit-incentive strength) | GP | Chung et al. (#5) |
| $CI^{type}_i$ | Co-investment right type: LP-discretion or GP-directed | Fund | Tuft (#23); Fang et al. (#21); Braun et al. (#22) |
| $home_i$ | Home-region or policy-mandate tag | Fund | Hochberg & Rauh (#12); Brav et al. (#11); Bernstein et al. (#13) |

### 4.2 Models
1. **Multi-signal GP belief model, replacing the single-signal Kalman rule (§2.3, §6.5 R1).**
   - The prior is $\mu_g = \beta_{TR,s}\cdot TR_g + \beta_q q_g + \beta_S \Delta S_g + \beta_{NS} NS_g + \beta_{IM}\cdot f(st,md,IM) + \dots$, fitted hierarchically by strategy and graded out of sample (Stream 07).
   - $\beta_{TR}$ should be near zero for post-2000 buyout, apart from a bottom-quartile screen (#2; HJKS), and larger for VC (Kaplan & Schoar; HJKS).
   - Pair it with the verification's R2 fix: value re-up decisions on the posterior mean $\mu_g$, not on the unobserved true $\gamma_g$.
2. **A learned recommitment policy as a challenger to MPC.** Evolutionary or RL search over explainable rule families (#20). Benchmark it against the de Zwart et al. rule from Stream 04's review (§4.7) and the dossier's exposure rule.
3. **Pacing corridors as optimal no-trade bands.** Use Dimmock et al. (#19) as the template: bands widen with secondary-market cost and in crisis states, and staggered vintages count as liquidity diversification.
4. **One valuation kernel per investor.**
   - Value commitments with ADIC's SDF (#10), linked to Streams 03 and 11.
   - Measure alpha net of a liquidity-risk factor (#24) before it enters $v_g$, $O_g$ or the LEVER test.
5. **Co-investment option value per dollar committed:** $V^{CI}=\rho\,[\text{selection term}\pm] + \text{fee saving} + \text{timing-option value}$.
   - The sign of the selection term is a scenario variable (#21 against #22).
   - The timing option exists only for LP-discretion rights (#23).

### 4.3 Parameters
| Parameter | Literature value | Use at ADIC |
|---|---|---|
| Buyout track-record loading, post-2000 | Persistence "substantially declined" (#2); prior performance unrelated to future performance (#3) | Near 0, plus a bottom-quartile penalty. K&S's S/N of 0.15 is an upper bound [inference] |
| Fund-size elasticity of net IRR | −0.1pp per +1% fund size (#6) | Local prior on up-size decisions; cap at plausible size steps |
| Liquidity-risk premium | ≈3% a year (#24) | Deduct from measured alpha, or raise the hurdle $h_s$ |
| Portfolio-company fees | ≈6% of equity invested, persistent within GP (#17) | Add to cash-flow fees where the offset is below 100% |
| Fixed share of GP revenue | ≈2/3 (#14) | Weight management-fee terms in negotiation |
| Scale effect | +4% a year per s.d. of PE holdings; ≤1/3 from costs (#8) | Supports ADIC's tier; cross-sectional, not causal |
| Co-investment selection effect | Negative (#21) or none (#22) | Scenario ±; ρ stays 0.2 pending ADIC data |
| Local-investment differential | −2 to −4pp for US public pensions (#12); positive for Israeli LPs (#11) | No default sign; monitor by tag |
| Implicit-incentive weight | Same order as carry; higher for buyout, falls with fund sequence (#5) | Scales the GP's response to ADIC's skip or up-size in R3 |

### 4.4 Constraints
1. **Up-size gate.** An up-sized re-up is admissible only if the fused alpha, after the size penalty and liquidity premium, still clears the hurdle.
   - Optionally cap ADIC's share of a fund's size step-up (#6, #14).
2. **Home-region and policy mandates.** Separate cap, benchmark and IC disclosure. Commitments made for policy reasons are logged as such (#12, #13).
3. **Waterfall type is priced, not a hard rule.** Deal-by-deal carry is allowed when clawback is secured (#16).
4. **Corridors are bands that may widen in crisis** (#19). Re-run the dossier's control experiment with the corridor applied (verification issue R3).
5. **Call default stays inadmissible.** Litvak (2013, §4.7) finds that better VC organisations "lock up investors' capital more tightly", so default costs are highest with the best GPs.
   - Contractual early-termination or no-fault provisions are collective LP-governance tools, not unilateral liquidity levers. Banal-Estañol & Ippolito (§4.7) report they are "common" [inference].

### 4.5 Objective terms (§6.7)
- **Replace "− fees" with net alpha.** Value net-of-fee alpha under ADIC's SDF. Fee level by itself is not a selection signal (#15, #16).
  - This also removes the fee double count the verification flagged in R10.
- **Add a risk-substitution penalty.** Penalise proposals whose expected return rises without a rise in SDF-adjusted value (#10).
- **Add co-investment option value** with selection risk (#21–#23).

### 4.6 Agent and IC design
1. **Document-diligence agent.**
   - It scores PPMs, LPAs and side letters (#3) and feeds $q_g$.
   - It is graded out of sample by an independent grader, not the PE deal team (dossier §8 conflict note).
2. **Mark-forensics agent.**
   - It computes staleness, markdown frequency and interim-multiple features (#4). It extends the BGK and Barber & Yasuda fundraising-period tests the dossier already cites.
   - It flags line-, pacing- and recycling-inflated interim IRRs (#18).
3. **Fee-forensics agent.** It checks management-fee basis and step-downs (#14), portfolio-company fees and offsets (#17), boom-vintage fee drift and behaviour around carry triggers (#15), and the waterfall type (#16).
4. **Pacing-policy agent.** It searches explainable recommitment rules (#20) inside the corridor bands (#19), and proposes them to the IC as a "pacing playbook" alongside MPC.
5. **IC checklists.**
   - Access versus selection: show which GPs are access-constrained (#10, #7).
   - Policy and political rationale (#13).
   - Home-region tags (#12).
   - Risk substitution (#10).
   - Size step-up (#6).
6. **Organization.**
   - Scale diligence resources to the size of the book (#8, #9).
   - Co-investment discretion is a liquidity-timing tool (#23). It should be visible to Corporate Finance, which owns the liquidity gate, portfolio-level borrowing and distributions (context §1A). G1 proposes, and Corporate Finance decides funding-side actions.

### 4.7 Further relevant papers (one line each)
**Retrieved this session (OpenAlex; links as returned).**
- [The Art of Commitment Pacing](https://doi.org/10.1002/9781394159635) (Meyer, 2024, Wiley book). Covers exposure measurement, cash-flow forecasting, investor skill, diversification, co-investments and secondaries, and stress scenarios. A chapter treats direct investments within pacing. Also listed in Stream 04's review.
- [Long-Run Management of Private Equity Investment](https://doi.org/10.3905/jpe.2019.1.083) (Wang & Peterson, 2019, *J. Private Equity* 22(3)). Stochastic simulation of calls, distributions and unfunded commitments under alternative commitment paces.
- [Evolutionary Learning of Private Equity Recommitment Strategies](https://doi.org/10.1109/ssci50451.2021.9660088) (Kieffer et al., 2021, IEEE SSCI) and [Proximal Policy Optimisation for a Private Equity Recommitment System](https://doi.org/10.1007/978-3-030-93842-0_12) (Kieffer et al., 2022, CCIS). Earlier versions of #20.
- Monte Carlo simulation of contractual provisions: an application to default provisions in VC limited partnership agreements (Litvak, 2013, vol. 98(6) 1495–1532; OpenAlex venue "Scholarship @ Cornell Law"; OpenAlex [W73839467](https://openalex.org/W73839467), no DOI returned). Capital lock-in is "inversely related to several measures of expected agency costs".
- Contractual Terms and Conditions in Private Equity Partnership Agreements (Banal-Estañol & Ippolito; SSRN version https://doi.org/10.2139/ssrn.1022023). Commitment may be weaker than perceived "as explicit early termination provisions are also common". It is modelled as a screen for GP ability.
- [Co-Investments of Sovereign Wealth Funds in Private Equity](https://doi.org/10.67929/ecgi-law-334-2016) (McCahery & de Roode, 2016, ECGI WP). SWFs "shift from investing in private equity funds to originating and co-investing".
- [Private Equity Fund Size, Investment Size, and Value Creation](https://doi.org/10.1093/rof/rfr011) (Humphery-Jenner, 2012, *Review of Finance*). Large funds earn lower returns, partly through suboptimal investment in small companies.
- [Estimating Private Equity Returns from Limited Partner Cash Flows](https://doi.org/10.1111/jofi.12688) (Ang, Chen, Goetzmann & Phalippou, 2018, *JF*). A PE return series from LP cash flows, with a time-varying PE premium; relevant to vintage-cycle state.
- Abstract not retrieved; title and venue only:
  - [Does Risk Explain Persistence in Private Equity Performance?](https://doi.org/10.1016/j.jcorpfin.2016.05.003) (Buchner, Mohamed & Schwienbacher, 2016, *JCF* 39);
  - [What Drives Private-Equity Performance Persistence? New Deal-Level Evidence](https://doi.org/10.2139/ssrn.4904483) (Buchner, Espenlaub & Mohamed, 2024, SSRN);
  - [Sovereign wealth fund investment in venture capital, private equity, and real asset funds](https://doi.org/10.1057/s42214-023-00162-3) (Cumming & Monteiro, 2023, *J. Int. Business Policy* 6(3)).

**Already verified in Stream 04's review (`04_pe_cashflows.lit.md`), missing from G1. Consensus URLs are copied from that file.**
- [Private Equity Recommitment Strategies for Institutional Investors](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop) (de Zwart et al., 2012, *FAJ*). The transparent baseline rule any pacing policy should beat.
- [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop) (Maurin et al., 2022, *Management Science*). LPs that tolerate illiquidity earn more, and GPs may accelerate drawdowns.
- [Risk-Adjusted Returns of Private Equity Funds: A New Approach](https://consensus.app/papers/details/d7fa0f4765285b498d96677eb55bdff5/?utm_source=claude_desktop) (Korteweg et al., 2024, *RFS*). A lower-noise fund α that improves prediction of future funds; a better signal $y$ for the belief update.
- [Reus et al. 2015, *J. Asset Mgmt*](https://consensus.app/papers/details/a41e24edf0b25f32b3f29cf414b80885/?utm_source=claude_desktop). A multistage stochastic program for PE commitments.

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation (section) | Challenging evidence | What it implies [inference] |
|---|---|---|---|
| 1 | GP learning from track records (§2.3 Kalman rule, §6.5 R1). "The edge that remains is disciplined, graded re-up decisions" (§5 item 3) | Braun, Jenkinson & Stoff (#2): buyout persistence "substantially declined". Fernández Tamayo et al. (#3): prior performance is unrelated to future performance; qualitative information predicts it. Korteweg, Panageas & Systla (#10): plans' edge comes from access, "not superior selection skill". Cavagnaro et al. (cited): skill effects are stronger early and for VC. | Track-record grading adds little for buyout. The remaining edges are access, qualitative diligence and terms. Re-weight the belief model (§4.2 item 1), and present re-up "skill" to the IC as unproven until ADIC's own graded history shows it. |
| 2 | "No significant buyout size–performance relation" (§2.3, from HJKS). LEVER through "over-commit or up-size re-ups where fused alpha > hurdle" (§6.8) | Bhardwaj et al. (#6): causal decreasing returns, −0.1pp net IRR per +1% size; larger deals perform worse. Metrick & Yasuda (#14): BO revenue scales with size. Kaplan & Schoar (#1): growth is concave in performance. | Add a size-step-up penalty to the alpha prior and an up-size gate (§4.4 item 1). GPs' revenue incentive to grow conflicts with LP returns. |
| 3 | Side letters anchored on ILPA terms. The dossier's [I] that deal-by-deal carry raises the PV of carry (§2.5, §5 item 4) | Hüther et al. (#16): deal-by-deal ("GP-friendly") contracts are associated with *higher* gross and net returns in VC. | Price the waterfall type and secure clawback rather than screening on it. Insisting on LP-friendly waterfalls may select against stronger managers. |
| 4 | Scale worth about 1pp through fees (§1 item 6). A "− fees" objective term (§6.7) | Robinson & Sensoy (#15): pay is unrelated to net performance, and high-pay managers earn it back gross. Dyck & Pomorski (#8): most of the scale benefit is in gross returns, with at most a third from costs. | Use net alpha under ADIC's SDF in the objective. Fees matter as cash flows, not as a selection score. Scale may be worth more than fee savings, through diligence. |
| 5 | Co-investment flow ρ ≈ 0.2, with G4 valuing each dollar (§6.5 R6) | Fang, Ivashina & Lerner (#21): co-investments underperform through GP selection. Braun, Jenkinson & Schemmerl (#22): no adverse selection, and net outperformance. Tuft (#23): co-investment goes to high-bargaining-power LPs and gives a timing option. | Scenario ± for co-investment selection. Prefer LP-discretion rights. Count the timing option in the liquidity plan, owned by Corporate Finance. |
| 6 | Hurdle $h_s$ of 0 to +1% over the strategy benchmark; alpha from PME or direct alpha (§6.10, §6.5) | Franzoni, Nowak & Phalippou (#24): a ≈3%/yr liquidity-risk premium takes alpha to zero. Korteweg, Panageas & Systla (#10): evaluate with an investor-specific SDF. | Add the liquidity-risk premium to the hurdle or the factor model. Access values, already flagged as overstated in verification R2, shrink further. |
| 7 | Interim performance signals with noise that falls with age (§2.3, §6.9) | Ercan, Kaplan & Strebulaev (#4): staleness and markdown frequency predict outcomes. The 2024 version says "past reported returns negatively predict future realized returns". | Interim marks can carry negative information. Use mark-history features, not only the level, in fusion and SELL screening. |
| 8 | Access model: a skip lowers ADIC's access probability Δp (§3.4, §6.5 R3) | Hochberg, Ljungqvist & Vissing-Jørgensen (cited; abstract): outsiders read incumbents' lack of backing "as a sign of low skill", which gives incumbents holdup power. Chung et al. (#5): re-ups are a large part of GP pay, especially for early-sequence buyout GPs. | A skip by a large incumbent costs the GP too. Model access as two-sided bargaining that depends on fund sequence and demand, not a one-way probability drop. No study found measures LP access after a skip, so Δp remains judgment. |

**Missed papers that support the dossier.**
- Dimmock, Wang & Yang (#19): bands rather than point targets, and tolerating crisis deviation (§3.2 lessons).
- Marquez et al. (#7): capacity rationing behind allocation cutbacks.
- Brown & Volckmann (#18): ranking on PME or direct alpha rather than interim IRR (§1 item 7).
- Kieffer et al. (#20): parametric policy search.
- Da Rin & Phalippou (#9): large LPs differ in diligence, consistent with the scale argument.

---

## 6. Usage message

The last (and only) usage message returned by Consensus, verbatim:

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Search log

**Consensus.** Three attempts, all with the query "Korteweg Sorensen Skill and luck in private equity performance", 30 seconds apart. All three failed with the message in §6, and no further Consensus calls were made.

**OpenAlex: citation checks (25 queries; plain search, no filters).**
1. skill and luck in private equity performance (connectivity test)
2. Skill and luck in private equity performance
3. Has persistence persisted in private equity? Evidence from buyout and venture capital funds
4. Smart institutions, foolish choices: the limited partner performance puzzle
5. Limited partner performance and the maturing of the private equity industry
6. Measuring institutional investors' skill at making private equity investments
7. Private equity performance: what do we know?
8. The illiquidity puzzle: theory and evidence from private equity
9. Investing outside the box: evidence from alternative vehicles in private equity
10. Do private equity funds manipulate reported returns?
11. Interim fund performance and fundraising in private equity
12. Can investors time their exposure to private equity?
13. Begenau Siriwardane private equity fees vary across public pensions
14. Beware of venturing into private equity
15. Informational holdup and performance persistence in venture capital
16. Private equity fund debt: capital flows, performance, and agency costs
17. Distortion or cash flow management? Understanding credit facilities in private equity funds
18. Illiquid alternative asset fund modeling Takahashi Alexander
19. Strategic asset allocation with illiquid alternatives
20. Valuing private equity Sorensen Wang Yang
21. Illiquid alternative asset fund modeling
22. Valuing private equity
23. Cyclicality, performance measurement, and cash flow liquidity in private equity
24. The liquidity cost of private equity investments: evidence from secondary market transactions
25. Capital commitment Gourier Phalippou Westerfield (no hit; resolved by DOI lookup doi:10.1111/jofi.13382), plus "Albertus Denes fund debt subscription lines private equity performance" (no journal version)

**OpenAlex: topical backfill (14 queries).** The five seeds were run as given; the rest are refinements.
1. limited partner skill private equity returns
2. private equity performance persistence
3. commitment pacing private equity portfolio
4. private equity commitment strategy overcommitment liquidity institutional investors
5. private equity fees carried interest
6. subscription lines of credit private equity IRR
7. subscription credit facilities private equity funds capital calls
8. sovereign wealth funds private equity investment strategies performance
9. direct investing private equity co-investment limited partners performance
10. private equity fund size performance decreasing returns to scale
11. machine learning predicting private equity fund performance manager selection
12. limited partner relationships general partners fundraising reinvestment decisions private equity
13. private equity performance survey review of the literature
14. default penalties private equity partnerships limited partners capital calls

**OpenAlex: title lookups to confirm metadata (14).**
- The economics of private equity funds
- Paying for performance in private equity: evidence from VC partnerships
- Private equity portfolio company fees
- Investor scale and performance in private equity investments
- Pay for performance from future fund flows: the case of private equity
- The endowment model and modern portfolio theory
- Private equity for pension plans? …
- How persistent is private equity performance? Evidence from deal-level data
- Do private equity fund managers earn their fees? …
- Local overweighting and underperformance …
- The importance of size in private equity …
- Adverse selection and the performance of private equity co-investments
- Private equity performance: a survey Kaplan Sensoy (not found)
- Interim valuations, predictability, and outcomes in private equity

**Abstract retrieval (not searches).**
- OpenAlex work-ID lookups.
- Crossref `/works/{doi}` for the SSRN and NBER DOIs listed in the entries.
- Semantic Scholar batch and title-match calls. Several returned HTTP 429 or had no abstract.

**WebSearch (1).** `Albertus Denes "Private Equity Fund Debt" subscription lines journal published`. No academic result, so no journal version was confirmed.

**Helper scripts** (session scratchpad; not ADIC data; may not persist):
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g1lit_scripts\oa.ps1`
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g1lit_scripts\cr.ps1`
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g1lit_scripts\s2.ps1`
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g1lit_scripts\s2t.ps1`
