# G4 literature review: direct minority co-investments alongside GPs

*Literature check of `research/groups/dossiers/G4_coinvest.md` for the ADIC multi-period robust TPA framework. Prepared 2026-10-18. The dossier was not edited. This review complements the adversarial fact-check in `research/groups/verification/G4_coinvest.verify.md`, which checked the dossier's numbers against the primary PDFs. It does not repeat that work.*

> **Method note: read this first.**
> - **Consensus could not be used.** All three attempts at the first query returned the monthly-quota message reproduced verbatim in §6. The quota resets on 1 November.
> - **OpenAlex** is one of the indexes Consensus searches. I used it as the G1 review did: plain relevance search with no year, type or citation filters. After 8 successful queries it returned HTTP 429. The response headers showed this IP's daily credit allowance was used up (Retry-After about 13.5 hours).
> - **Semantic Scholar**, another Consensus index, throttled most calls (HTTP 429). Four of seven calls returned data, one of them only after retries.
> - **Crossref therefore carried most searches.** I used plain bibliographic or general queries with no filters, and DOI lookups for metadata and deposited abstracts. Crossref recall on topical queries is weaker than Consensus, so this backfill may miss papers a Consensus run would find.
> - **WebSearch** was used three times, only for metadata and abstracts the APIs could not supply: Axelson–Sorensen–Strömberg, L'Her et al., and Ayash & Rastad.
> - **No Consensus URL was generated in this session.** Ten Consensus URLs appear in this file. Each is copied verbatim from a sibling review or the G4 verification log, and its source file is named. Every other link is the DOI, OpenAlex or web URL exactly as the API or search returned it.
> - **Citation counts** are labelled by source: OA = OpenAlex `cited_by_count`, CR = Crossref `is-referenced-by-count`, S2 = Semantic Scholar. All were read on 2026-10-18.
> - "Finding" restates the retrieved abstract, and quoted phrases are the authors' words. Anything beyond an abstract is tagged **[inference]**.

---

## 1. Summary

### Citation integrity
- **13 academic works checked.** These are the 8 academic references in dossier §10 plus 5 cited only in the text: Axelson et al. 2013, Axelson–Sorensen–Strömberg, Broadie–Glasserman–Kou, Kou and Rockafellar–Uryasev.
  - **13 found, 0 metadata mismatches, 0 not found.** No hallucinated or garbled academic citation was found, which agrees with the verification log.
- **Four problems in how citations are used:**
  1. **The Broadie–Glasserman–Kou (BGK) correction has the wrong sign (§7).** BGK shift the barrier "away from the underlying" to price a *discretely* monitored barrier with continuous formulas. To make a quarterly simulation mimic continuous default monitoring of a down barrier, the barrier must move *toward* the underlying: $\kappa D\,e^{+0.5826\sigma\sqrt\Delta}$. The dossier writes $e^{-0.5826\sigma\sqrt\Delta}$. That lowers the barrier, which *raises* simulated survival, the opposite of the stated intent. The verification log does not raise this. The calculation script applies no correction at all.
  2. **Lopez-de-Silanes, Phalippou & Gottschalg is misread as deal-size evidence (§4.2 "Size").** Their "diseconomies of scale" refer to a PE firm's number of *simultaneous investments*, not to deal size. The §10 title is also truncated.
  3. **Bhardwaj, Gupta & Howell is applied at the wrong scale (E5).** The abstract's "2.4 times the targeted firm mean" goes with an **84% average increase in total debt**. The dossier applies ×2.4 to recaps that add 25% debt (φ = 0.25). This complements verification issue R4, which shows ×2.4 is an IV increment, not a multiplier.
  4. **Gaps in the reference list.** Axelson et al. (2013) and Axelson–Sorensen–Strömberg (the source of β = 2.3) are cited in the text but missing from §10. The latter is an unpublished 2014 working paper. The *JEP* pages for Kaplan & Strömberg (121–146) are missing.

### Backfill: what the dossier misses
I ran 14 topical searches and 13 title lookups (log in §7). Section 3 annotates 25 papers: 7 the dossier cites and 18 it does not. Section 4.7 lists 15 more in one line each. The main gaps:

1. **Selection runs through offer *timing* and asset *retention*, not through the average deal.**
   - Hüther (2023, *JFQA*): late investments "made under pressure before fundraising" earn lower returns.
   - Braun & Schmidt (2014): deal returns drop once a GP establishes a new partnership.
   - Abuzov et al. (2025, NBER): assets moved into continuation funds are "better performing and larger".
   - BJS's own probit, cited in the dossier, shows offers are likelier before the follow-on fund closes.
2. **Benchmarking and risk.**
   - L'Her et al. (2016, *FAJ*): buyout outperformance disappears against a levered, size- and sector-adjusted benchmark.
   - The deal-level jump CAPM of Axelson–Sorensen–Strömberg: β of 2.2–2.4 per the draft.
   - Ewens, Jones & Rhodes-Kropf (2013, *RFS*): agency makes diversifiable risk priced.
3. **Leverage and price are endogenous to the regime.**
   - Axelson et al. (2013, *JF*): higher deal leverage goes with higher prices and lower returns.
   - Haddad, Loualiche & Plosser (2017, *JF*): the equity risk premium drives buyout activity, leverage and performance.
4. **Distress is resolved with sponsor capital.** Hotchkiss, Smith & Strömberg (2021, *RCFS*): PE-backed firms default more often but restructure faster and liquidate less, often after sponsor equity infusions.
5. **Deal-level information signals.**
   - Ercan, Kaplan & Strebulaev (2025): mark history predicts outcomes.
   - Biesinger, Bircan & Ljungqvist (2020): execution of value-creation plans raises returns, while financial engineering does not create value.
   - Puche & Braun (2018): multiple expansion relative to the market.
6. **Size, costs and organization.**
   - Bhardwaj et al. (2025): larger funds do larger, worse-performing deals.
   - Phalippou, Rauch & Umber (2018): portfolio-company fees.
   - Hüther et al. (2020): deal-by-deal carry.
   - Andonov, Eichholtz & Kok (2015): in-house management at scale.
7. **LP bargaining, liquidity timing and sovereign peers.**
   - Tuft (2023): co-investment shares surplus with high-bargaining-power LPs and gives LP-discretion investors a timing option.
   - McCahery & de Roode (2017): sovereign wealth funds shift toward co-investing.
   - Gredil, Liu & Sensoy (2020): the certainty-equivalent cost of under-diversification.

### Challenges (detail in §5)
The literature most directly challenges six dossier positions:
1. "Selection is not the main problem".
2. Re-basing expected multiples by lowering leverage with the EV process held fixed.
3. PME-based calibration read as absolute value.
4. "0/20 co-investments are about as expensive as a fund".
5. A constant follow-on rate with near-zero equity recovery.
6. SACV pricing used for ordinary assets.

### Evidence gaps
None of my searches found:
- an academic co-investment performance study covering vintages after about 2010;
- an academic study of LP-led single-asset (strip) sale pricing;
- an LP-level estimate of the co-investment offer rate θ.

---

## 2. Citation-integrity table (13 checked)

Status key: **found** means the metadata matches the version cited. Notes flag version differences or problems in how the paper is used. Where the Consensus column says "n/a", no Consensus URL exists in this session or in the sibling files.

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| 1. Fang, Ivashina & Lerner (2015), *JFE* 116(1):160–178; NBER w19299 | found | *JFE* 116(1) 160–178, DOI 10.1016/j.jfineco.2014.12.002 (online 2014; OA 150). WP: NBER 2013, DOI 10.3386/w19299. The abstract confirms solo deals outperform, and that co-investments underperform through "fund managers' selective offering of large deals". OpenAlex [W3122114492](https://openalex.org/W3122114492) | https://consensus.app/papers/details/4e0c268caabc5b468d053656985a3deb/?utm_source=claude_desktop (from `02_endowment_swf.lit.md`, S30) |
| 2. Braun, Jenkinson & Schemmerl (2020), *JFE* 136(1):44–62 | found | DOI 10.1016/j.jfineco.2019.01.009 (OA 73; CR 63). SSRN 2016: DOI 10.2139/ssrn.2871458. The abstract confirms "no evidence of adverse selection" and that co-investment portfolios out-performed funds. OpenAlex [W3123353822](https://openalex.org/W3123353822) | https://consensus.app/papers/details/74305f05d7e758dfbc4c1b624c2fa5db/?utm_source=claude_desktop (from `02_endowment_swf.lit.md`, S31) |
| 3. Lerner, Mao, Schoar & Zhang (2022), *JFE* 143(1):359–380; NBER w24941 | found (WP version note) | DOI 10.1016/j.jfineco.2021.05.034 (online 2021; OA 71). The WP is "…Alternative Vehicles in Private **Capital**" by Lerner, Schoar, Mao, Zhang (NBER 2018, DOI 10.3386/w24941). The abstract confirms 40% of commitments by 2017, AVs trailing sponsors' main funds, and top LPs' preferential access. OpenAlex [W2889193665](https://openalex.org/W2889193665) | https://consensus.app/papers/details/94e5f805d12f5f58b961fbb751940fc3/?utm_source=claude_desktop (from `G4_coinvest.verify.md`, claim 9) |
| 4. Braun, Jenkinson & Stoff (2017), *JFE* 123(2):273–291 | found | DOI 10.1016/j.jfineco.2016.01.033 (online 2016; OA 174). OpenAlex [W3125376556](https://openalex.org/W3125376556) | https://consensus.app/papers/details/00af5930c4c75ef99ef2ac1654c52789/?utm_source=claude_desktop (from `05_secondaries_navfin.lit.md`, F31) |
| 5. Lopez-de-Silanes, Phalippou & Gottschalg (2015), "Giants at the gate", *JFQA* 50(3):377–411; MPRA 28487 | found (title truncated; use note) | Full title: "Giants at the Gate: Investment Returns and Diseconomies of Scale in Private Equity", DOI 10.1017/s0022109015000113 (OA 163). The WP (2010) is "…On the Cross-Section of Private Equity Investment Returns". **Use note:** in the abstract, "scale" means the PE firm's number of simultaneous investments, not deal size, so §4.2 should not list it as deal-size evidence. OpenAlex [W3123808995](https://openalex.org/W3123808995) | https://consensus.app/papers/details/200e6cc97ac95325b4ef329c9d5a4a85/?utm_source=claude_desktop (from `G4_coinvest.verify.md`, claim 10) |
| 6. Kaplan & Strömberg (2008), NBER WP 14207 (*JEP* 23(1), 2009) | found | *JEP* 23(1) **121–146**, DOI 10.1257/jep.23.1.121 (OA 1,033). NBER (2008), DOI 10.3386/w14207. Add the pages. OpenAlex [W3124463244](https://openalex.org/W3124463244) | n/a |
| 7. Gompers, Kaplan & Mukharlyamov (2016), *JFE* 121(3):449–476; NBER w21133 | found | DOI 10.1016/j.jfineco.2016.06.003 (OA 377). The NBER abstract confirms 79 investors, more than $750bn, and reliance on IRR and multiples. OpenAlex [W3122207317](https://openalex.org/W3122207317) | https://consensus.app/papers/details/9c44ffc9ab6a5bdbaeebc0798a59f4d5/?utm_source=claude_desktop (from `07_return_fusion.lit.md`, #31) |
| 8. Bhardwaj, Gupta & Howell (2025), NBER WP 33435 | found (use problem) | Exact title, "Capital Structure & Firm Outcomes: Evidence from Dividend Recapitalizations in Private Equity"; DOI 10.3386/w33435; SSRN DOI 10.2139/ssrn.5122154. **Use problem:** the abstract ties "2.4 times the targeted firm mean" to "higher total debt (84% on average)", but E5 applies ×2.4 to φ = 0.25 recaps (see also verification R4). OpenAlex [W4407092000](https://openalex.org/W4407092000) | n/a |
| 9. "Axelson et al. (2013)" (text, §6.3: GKM "cite Axelson et al. (2013) for 70%") | found; missing from §10 | Axelson, Jenkinson, Strömberg & Weisbach, "Borrow Cheap, Buy High? The Determinants of Leverage and Pricing in Buyouts", *JF* 68(6) 2223–2267, DOI 10.1111/jofi.12082 (OA 382). Add it to §10. OpenAlex [W3123463192](https://openalex.org/W3123463192) | n/a |
| 10. "ASS β = 2.3", Axelson–Sorensen–Strömberg (cited through GKM, §4.1, §8) | found (unpublished WP; via WebSearch) | "Alpha and Beta of Buyout Deals: A Jump CAPM for Long-Term Illiquid Investments", preliminary draft dated November 2014: https://personal.lse.ac.uk/axelson/ulf_files/alpha%20and%20beta%201.pdf. Listed as a working paper on Axelson's CV and not in Crossref. The search summary of the draft gives a gross β of 2.2–2.4, consistent with 2.3. Add it to §10. | n/a |
| 11. "Broadie–Glasserman–Kou shift" (§7) | found (formula sign problem) | Broadie, Glasserman & Kou, "A Continuity Correction for Discrete Barrier Options", *Mathematical Finance* 7(4) 325–349 (1997), DOI 10.1111/1467-9965.00035 (CR 252). The abstract: the correction shifts the barrier "away from the underlying" by exp(βσ√Δt), β ≈ 0.5826. For a quarterly simulation of a down barrier, use $\kappa D\,e^{+0.5826\sigma\sqrt\Delta}$ (see §1). | n/a |
| 12. "Kou jump-diffusion" (E1) | found | Kou, "A Jump Diffusion Model for Option Pricing", SSRN 2000, DOI 10.2139/ssrn.242367: a double-exponential jump diffusion, as used in E1. The query did not return the journal version, so its metadata is unconfirmed here. | n/a |
| 13. "Rockafellar–Uryasev" CVaR (§7) | found | "Optimization of conditional value-at-risk", *Journal of Risk* 2(3) 21–41 (2000), DOI 10.21314/jor.2000.038 (CR 5,524) | n/a |

**Not counted as citations:**
- Method names: Merton, Weibull, Cox, Fine–Gray, Aalen–Johansen, Kalman, random survival forests. Takahashi–Alexander was verified in the G1 review.
- Industry and legal sources: Bain, Lazard, Evercore, Jefferies, Proskauer, Rede, ILPA, SEC, Sidley, Torys, Investment Officer, Capstone, ABF Journal, IFR, Freshfields, Hamilton Lane, PEI/Altius, HarbourVest‡ and Capital Dynamics‡. The verification log checked these.

---

## 3. Annotated bibliography (25 papers)

Tags:
- **[cited]**: in the G4 dossier.
- **[missed]**: not cited.
- **[challenge]**: contradicts or qualifies a dossier recommendation (§5).

"Relevance" lines are my inferences for ADIC unless they quote the paper.

### A. Co-investment selection, access and terms

**1. [Adverse selection and the performance of private equity co-investments](https://consensus.app/papers/details/74305f05d7e758dfbc4c1b624c2fa5db/?utm_source=claude_desktop)** [cited]
- Braun, R., Jenkinson, T., & Schemmerl, C. · 2020 · *Journal of Financial Economics* 136(1) 44–62 · OA 73 · DOI 10.1016/j.jfineco.2019.01.009 · abstract via Semantic Scholar · Consensus URL copied from `02_endowment_swf.lit.md`
- **Finding.** "In contrast to Fang et al. (2015) we find no evidence of adverse selection. Gross return distributions of co-investments and other deals are similar." Co-investments cost less, and "reasonably sized portfolios of co-investments have significantly out-performed fund returns".
- **Relevance.** This remains the reference class. Read it with the verification log's correction (at 0/20 terms, buyouts need about 30 deals) and with the timing channel in items 6–7. The unconditional result fixes the *mean* selection effect, not its conditional shape [inference].

**2. [The disintermediation of financial markets: Direct investing in private equity](https://consensus.app/papers/details/4e0c268caabc5b468d053656985a3deb/?utm_source=claude_desktop)** [cited; challenge]
- Fang, L. H., Ivashina, V., & Lerner, J. · 2015 (online 2014) · *Journal of Financial Economics* 116(1) 160–178 · OA 150 · DOI 10.1016/j.jfineco.2014.12.002 · abstract via Semantic Scholar · Consensus URL copied from `02_endowment_swf.lit.md`
- **Finding.**
  - Solo investments by seven large institutions outperform co-investments and fund benchmarks, especially where information problems are mild and inflow booms are avoided.
  - "The poor performance of co-investments … appears to result from fund managers' selective offering of large deals to institutions for co-investing."
- **Relevance.** The authors frame the size effect as *GP selection* of what to offer. The dossier's reading, "not being sold lemons", reframes it. A size cap answers both readings. Only the selection reading implies the offer decision itself carries information [inference].

**3. [Investing outside the box: Evidence from alternative vehicles in private equity](https://consensus.app/papers/details/94e5f805d12f5f58b961fbb751940fc3/?utm_source=claude_desktop)** [cited]
- Lerner, J., Mao, J., Schoar, A., & Zhang, N. R. · 2022 (online 2021) · *Journal of Financial Economics* 143(1) 359–380 · OA 71 · DOI 10.1016/j.jfineco.2021.05.034 · abstract via Semantic Scholar · Consensus URL copied from `G4_coinvest.verify.md`
- **Finding.**
  - Alternative vehicles reached 40% of PE commitments by 2017. On average they match the PE market but underperform the sponsors' main funds.
  - Better LPs get better vehicles, "largely driven by preferential access of top LPs to top AVs".
- **Relevance.**
  - ADIC's co-investment quality depends on its standing as an LP.
  - The verification log reports a WP gap of −0.101 (p < 0.01) for GP-directed vehicles against −0.016 (not significant) for discretionary ones. Together with item 4, this supports preferring LP-discretion rights [inference].

**4. [Beyond Fees: Co-Investment and the Design of Private Equity Relationships](https://doi.org/10.2139/ssrn.4559453)** [missed]
- Tuft, A. · 2023 · *SSRN* working paper · CR 2 · DOI 10.2139/ssrn.4559453 · abstract via Crossref
- **Finding.**
  - Co-investment is how GPs "share surplus with those holding greater bargaining power". It complements main-fund fee discounts rather than substituting for them.
  - Under the Volcker shock, a one s.d. increase in exposure to the loss of bank LPs "raises co-investment by 11.7%".
  - LPs more exposed to liquidity risk co-invest more, which is consistent with control over "the timing of their capital outlays". The effect appears only in LP-discretion deals.
- **Relevance.**
  - The offer rate θ is a bargaining outcome, not a constant.
  - Discretionary co-investment is a liquidity-timing option. Corporate Finance, which owns treasury (user-confirmed), should price it [inference].

**5. [Co-Investments of Sovereign Wealth Funds in Private Equity](https://doi.org/10.1093/oxfordhb/9780198754800.013.5)** [missed]
- McCahery, J. A., & de Roode, F. A. · 2017 · Oxford Handbooks Online (handbook chapter; Crossref type "book"; same handbook DOI stem as Wright & Amess 2017 in §4.7) · CR 1 · DOI 10.1093/oxfordhb/9780198754800.013.5 · abstract via Crossref. WP versions: SSRN 2881231 and ECGI law WP 334/2016.
- **Finding.** On Global Corporate Venturing data, SWFs "shift from investing in private equity funds to originating and co-investing together with private equity funds". "The choice for co-investment affects deal size, risk-bearing, fees and returns."
- **Relevance.** This is the closest peer evidence for a sovereign co-investor. The abstract gives no effect sizes, so use it as a peer reference, not a calibration source [inference].

### B. Offer timing, deal size and asset retention: the conditional selection channels

**6. [Do Private Equity Managers Raise Funds on (Sur)real Returns? Evidence from Deal-Level Data](https://consensus.app/papers/details/834e2e8848615de6808f6adbd5bdda10/?utm_source=claude_desktop)** [missed; challenge]
- Hüther, N. · 2023 (online 2022) · *Journal of Financial and Quantitative Analysis* 58(7) 2959–2992 · CR 26 · DOI 10.1017/s0022109022000990 · abstract via Crossref · Consensus URL copied from `07_return_fusion.lit.md`
- **Finding.** There is no evidence of inflated deal-level performance around fundraising. "Fund performance peaks are driven by a cohort effect whereby late investments are made under pressure before fundraising and have lower returns than those made earlier in the fund's life."
- **Relevance.**
  - BJS find offers are more likely for deals done before the follow-on fund closes (probit 0.20–0.22**, verified). Together with Hüther, co-investment offers may cluster in the weaker late cohort [inference]. Condition the prior on the deal's position in the sponsor's fund cycle.
  - The absence of deal-level mark inflation also supports *not* haircutting co-investment marks for fundraising.

**7. [The Limited Partnership Model in Private Equity: Deal Returns over a Fund's Life](https://doi.org/10.2139/ssrn.2411044)** [missed; challenge]
- Braun, R., & Schmidt, M. · 2014 · *SSRN* working paper · CR 3 (S2 9) · DOI 10.2139/ssrn.2411044 · abstract via Crossref
- **Finding.** On 10,566 investments by 702 PE partnerships, "a robust drop in investment returns once a new limited partnership is established". The pattern has strengthened since the late 1990s.
- **Relevance.** This is independent evidence that the sponsor's fund cycle is a deal-return covariate. Add it to the co-investment prior and to monitoring of held deals [inference].

**8. [Does Fund Size Affect Private Equity Performance? Evidence from Donation Inflows to Private Universities](https://doi.org/10.3386/w33596)** [missed]
- Bhardwaj, A., Gupta, A., Howell, S. T., & Zimmerschied, K. · 2025 · NBER Working Paper w33596 · CR 8 · DOI 10.3386/w33596 · abstract via Crossref (SSRN DOI 10.2139/ssrn.5190783)
- **Finding.** With an instrument from university gifts, "a 1% size increase reduces net IRR by 0.1 percentage points. Larger funds do larger deals, which perform worse." Risk does not change, "in part because additional deals are more levered".
- **Relevance.** This is causal support for the dossier's size discipline. Co-investment offers skew to large deals (FIL; BJS's probit), so relative deal size and the sponsor's fund-size step-up belong in the prior [inference].

**9. [Selling to Yourself: Continuation Funds in Private Equity](https://doi.org/10.3386/w34471)** [missed; challenge]
- Abuzov, R., Gornall, W., Shive, S., Strebulaev, I. A., & Weisbach, M. S. · 2025 · NBER Working Paper w34471 · CR 0 · DOI 10.3386/w34471 · abstracts via Crossref (SSRN DOIs 10.2139/ssrn.5771142 and 10.2139/ssrn.5757604)
- **Finding.**
  - Continuation funds grew from 5 in 2018 to 130 in 2024 (a hand-collected sample of 472). They accounted for "9% of PE exits in 2024".
  - They emerge when LPs are heterogeneous and managers have carry to roll.
  - "Assets transferred to CFs are better performing and larger than other assets in legacy funds." LPs overwhelmingly exit, a choice "driven by time-varying LP liquidity demands".
- **Relevance.**
  1. SACV prices are positively selected, which supports verification R1.
  2. A CV is a GP-triggered event on ADIC's *best* holdings, which supports verification R5.
  3. ADIC's sell-or-roll answer should be priced at Corporate Finance's liquidity shadow price [inference].

### C. Deal-level return distribution, risk and benchmarks

**10. [Giants at the Gate: Investment Returns and Diseconomies of Scale in Private Equity](https://consensus.app/papers/details/200e6cc97ac95325b4ef329c9d5a4a85/?utm_source=claude_desktop)** [cited]
- López-de-Silanes, F., Phalippou, L., & Gottschalg, O. · 2015 · *Journal of Financial and Quantitative Analysis* 50(3) 377–411 · OA 163 · DOI 10.1017/s0022109015000113 · abstract via OpenAlex · Consensus URL copied from `G4_coinvest.verify.md`
- **Finding.**
  - In 7,500 investments, "One in 10 investments does not return any money, whereas 1 in 4 has an internal rate of return (IRR) above 50%". "Quick flips are associated with the highest returns."
  - Investments held "in periods with a high number of simultaneous investments underperform substantially".
- **Relevance.**
  - The zero-return calibration target stands.
  - The diseconomy concerns GP bandwidth, so add a sponsor active-deal-count covariate instead of reading the paper as deal-size evidence.
  - The quick-flip result supports E4's performance tilt [inference].

**11. [Alpha and Beta of Buyout Deals: A Jump CAPM for Long-Term Illiquid Investments](https://personal.lse.ac.uk/axelson/ulf_files/alpha%20and%20beta%201.pdf)** [cited second-hand]
- Axelson, U., Sorensen, M., & Strömberg, P. · 2014 (preliminary draft, November) · unpublished working paper (per Axelson's CV) · citations n/a · no DOI · abstract not retrieved; finding from the WebSearch summary of the draft (unverified)
- **Finding.** Per the search summary, the gross-of-fee return on levered buyout-deal equity has an annual alpha of 8.3–8.6% and a beta of 2.2–2.4.
- **Relevance.**
  - This is the academic template for E1, a jump diffusion with market beta.
  - The dossier's β_A·V/E = 0.9/(1−0.60) = 2.25 at historical leverage matches it. At today's L of about 0.36–0.45 it gives about 1.4–1.6 [inference].
  - A 0/0 co-investment earns close to the gross return, so gross estimates are the right comparison. Cite the paper directly, not through GKM.

**12. [A Bottom-Up Approach to the Risk-Adjusted Performance of the Buyout Fund Market](https://doi.org/10.2469/faj.v72.n4.1)** [missed; challenge]
- L'Her, J.-F., Stoyanova, R., Shaw, K., Scott, W., & Lai, C. · 2016 · *Financial Analysts Journal* 72(4) 36–48 · CR 30 (S2 43) · DOI 10.2469/faj.v72.n4.1 · finding from the [CFA Institute abstract page](https://www.cfainstitute.org/research/financial-analysts-journal/2016/a-bottom-up-approach-to-the-risk-adjusted-performance-of-the-buyout-fund-market), via WebSearch; no abstract in Crossref or S2
- **Finding.**
  - On Burgiss data, buyouts look strong before risk adjustment.
  - A bottom-up analysis of portfolio companies' systematic risk yields a levered, size- and sector-adjusted public benchmark. Against it, buyout funds show no significant dollar-weighted outperformance.
  - Secondary coverage reports average net debt/EV of about 65%.
- **Relevance.**
  - PMEs against a broad index, as in BJS and the dossier's calibration, overstate risk-adjusted value. Hurdles and IC scores should use a levered, size- and sector-matched benchmark.
  - The 65% figure, second-hand, supports the dossier's historical L of 0.60–0.65 [inference].

**13. [Borrow Cheap, Buy High? The Determinants of Leverage and Pricing in Buyouts](https://doi.org/10.1111/jofi.12082)** [cited in text only; challenge]
- Axelson, U., Jenkinson, T., Strömberg, P., & Weisbach, M. S. · 2013 · *The Journal of Finance* 68(6) 2223–2267 · OA 382 · DOI 10.1111/jofi.12082 · abstract via OpenAlex
- **Finding.** Economy-wide credit conditions, not the cross-sectional factors behind public-firm leverage, drive buyout leverage. "Higher deal leverage is associated with higher transaction prices and lower buyout fund returns, suggesting that acquirers overpay when access to credit is easier."
- **Relevance.** Leverage is a regime variable tied to entry price and returns. Re-basing by lowering L with the EV process held fixed (§6.3) omits this link [inference; cf. verification R7].

**14. [Buyout Activity: The Impact of Aggregate Discount Rates](https://doi.org/10.1111/jofi.12464)** [missed]
- Haddad, V., Loualiche, E., & Plosser, M. · 2017 · *The Journal of Finance* 72(1) 371–414 · CR 45 · DOI 10.1111/jofi.12464 · abstract via Crossref
- **Finding.** "Buyout booms form in response to declines in the aggregate risk premium." The equity risk premium, not credit-specific conditions, is the primary determinant of activity, and it shapes buyout "riskiness, leverage, and performance" over the cycle.
- **Relevance.** Add an equity-risk-premium or valuation state next to the credit window $c_t$ in vintage pacing and in the regime draw of entry terms [inference].

**15. [Deal Pricing and Returns in Private Equity](https://doi.org/10.3905/jai.2018.1.067)** [missed]
- Puche, B., & Braun, R. · 2018 · *The Journal of Alternative Investments* 21(3) 70–85 · CR 9 (S2 5) · DOI 10.3905/jai.2018.1.067 · abstract via Semantic Scholar
- **Finding.** On 2,174 deals, multiple expansion is important to deal returns. Buying low and selling high against same-segment market prices raises it, and "selling high yields about twice as much as buying low".
- **Relevance.**
  - Run the "what you need to believe" multiple check on multiples *relative to* segment market levels.
  - Most of this value is in exit timing, which the GP controls, while the co-investor only tags along [inference].

**16. [Value Creation in Private Equity](https://doi.org/10.2139/ssrn.3587559)** [missed]
- Biesinger, M., Bircan, Ç., & Ljungqvist, A. · 2020 · *SSRN* working paper · CR 13 · DOI 10.2139/ssrn.3587559 · abstract via Crossref
- **Finding.** The paper uses confidential pre-deal memos and value-creation plans. PE firms create value by "selecting companies that are about to outperform" and through capex and acquisitions, "but not by financial engineering". Successful execution, tracked through monitoring reports, adds to returns.
- **Relevance.** ADIC receives comparable memos (the u series) and monitoring reports. A plan-execution score is a natural state variable for deal-level belief updates [inference].

**17. [The Price of Diversifiable Risk in Venture Capital and Private Equity](https://doi.org/10.1093/rfs/hht035)** [missed]
- Ewens, M., Jones, C. M., & Rhodes-Kropf, M. · 2013 · *The Review of Financial Studies* 26(8) 1854–1889 · CR 123 (S2 325) · DOI 10.1093/rfs/hht035 · abstract via Semantic Scholar
- **Finding.** The GP–LP principal-agent problem "causes limited partner returns to depend on diversifiable risk". This predicts a correlation between total risk and net-of-fee investor returns, which their data support. The evidence is mainly from VC.
- **Relevance.**
  - If deal prices embed a premium for idiosyncratic risk, a diversified co-investor collects it. That is a structural argument for co-investing.
  - It argues for total risk ($\sigma_{id}$), not only beta, in the prior [inference].

### D. Diversification

**18. [Diversifying Private Equity](https://doi.org/10.2139/ssrn.3535677)** [missed]
- Gredil, O., Liu, Y., & Sensoy, B. A. · 2020 · *SSRN* working paper · CR 3 · DOI 10.2139/ssrn.3535677 · abstract via Crossref
- **Finding.**
  - Most LPs invest in fewer than three PE funds a year. In an expected-utility framework, certainty-equivalent returns are "up to 5% lower" than average fund performance implies.
  - Performance chasing adds idiosyncratic risk, and "as few as five funds per year" likely suffices.
- **Relevance.**
  - Use a certainty-equivalent concentration haircut tied to effective N.
  - Deal-level idiosyncratic risk far exceeds fund-level risk, so co-investment books need many more names [inference].
  - Sibling reviews 04 and 08 cite a "Gredil et al. 2020" Consensus record with "2–8%". This version says "up to 5%".

### E. Distress, recaps, exits and marks (the deal engine)

**19. [Private Equity and the Resolution of Financial Distress](https://doi.org/10.1093/rcfs/cfab015)** [missed; challenge]
- Hotchkiss, E. S., Smith, D. C., & Strömberg, P. · 2021 · *The Review of Corporate Finance Studies* 10(4) 694–747 · CR 93 · DOI 10.1093/rcfs/cfab015 · abstract via Crossref. The ECGI 2012 WP covers 2,151 leveraged-loan borrowers, 1997–2010.
- **Finding.**
  - PE-backed firms "have higher leverage and default at higher rates" than other leveraged-loan borrowers. They restructure faster, avoid court more often and liquidate less.
  - PE owners often keep control "by infusing capital as firms approach distress".
- **Relevance.**
  - E3 and E6 should model higher default incidence with lower loss severity, and rescue calls concentrated in distress.
  - A co-investor that declines a rescue call is diluted at the worst time. That is wrong-way liquidity risk for Corporate Finance [inference].

**20. [Capital Structure & Firm Outcomes: Evidence from Dividend Recapitalizations in Private Equity](https://doi.org/10.3386/w33435)** [cited]
- Bhardwaj, A., Gupta, A., & Howell, S. T. · 2025 · NBER Working Paper w33435 · OA 0 · DOI 10.3386/w33435 · abstract via OpenAlex
- **Finding.**
  - "Higher total debt (84% on average) dramatically increases the chance of financial distress (by 2.4 times the targeted firm mean)."
  - Recaps "increase deal returns but reduce fund returns, possibly reflecting moral hazard", and lower pre-existing creditors' loan prices.
- **Relevance.** Scale E5's distress effect to recap size and to the paper's definition (§4.3; verification R4). The pre-existing-creditor loss supports the dossier's look-through netting with Private Credit.

**21. [Interim Valuations, Predictability, and Outcomes in Private Equity](https://doi.org/10.3386/w33637)** [missed]
- Ercan, E. Y., Kaplan, S. N., & Strebulaev, I. A. · 2025 · NBER Working Paper w33637 · CR 4 · DOI 10.3386/w33637 · abstracts via Crossref (SSRN DOIs 10.2139/ssrn.5215933, 2025, and 10.2139/ssrn.4833819, 2024)
- **Finding.**
  - For US buyout and VC portfolio companies, investments with "greater past staleness or more frequent markdowns tend to perform more poorly", and exit timing is predictable.
  - Tail outcomes are predictable "as early as the first year".
  - The 2024 version adds that "past reported returns negatively predict future realized returns".
- **Relevance.** Add staleness and markdown-frequency features to E7's nowcast and to SELL screening. Interim mark-ups should not raise forward-return beliefs one for one [inference].

**22. [IPO Timing, Buyout Sponsors' Exit Strategies, and Firm Performance of RLBOs](https://doi.org/10.1017/s0022109011000160)** [missed]
- Cao, J. X. · 2011 · *Journal of Financial and Quantitative Analysis* 46(4) 1001–1024 · CR 60 · DOI 10.1017/s0022109011000160 · abstract via Crossref
- **Finding.** "LBO duration is negatively related to hot IPO market conditions." Reverse LBOs with shorter holds "experience greater deterioration of performance and higher probability of bankruptcy".
- **Relevance.** This supports regime multipliers on E4's exit hazard. In open windows, a retained or staged IPO stake may carry lower residual quality [inference].

### F. Costs, scale and organization

**23. [Private equity portfolio company fees](https://doi.org/10.1016/j.jfineco.2018.05.010)** [missed]
- Phalippou, L., Rauch, C., & Umber, M. P. · 2018 · *Journal of Financial Economics* 129(3) 559–585 · CR 86 · DOI 10.1016/j.jfineco.2018.05.010 · abstract not retrieved here; finding as recorded in `G1_pe_primaries.lit.md` (via Semantic Scholar)
- **Finding (per the G1 record).** GP fees charged to portfolio companies total about "$20 billion" over twenty years, "over 6% of the equity invested". They vary across GPs and persist within them.
- **Relevance.** Co-investors usually get no offset (dossier §2.4). Give E8 a GP-level portfolio-company-fee intensity, and use it in co-investment due diligence [inference].

**24. [Paying for Performance in Private Equity: Evidence from Venture Capital Partnerships](https://doi.org/10.1287/mnsc.2018.3274)** [missed; challenge]
- Hüther, N., Robinson, D. T., Sievers, S., & Hartmann-Wendels, T. · 2020 · *Management Science* 66(4) 1756–1782 · CR 47 · DOI 10.1287/mnsc.2018.3274 · abstract via Crossref
- **Finding.** "GP-friendly" deal-by-deal carry contracts "are associated with higher returns, both gross and net of fees". The result is robust and tied to exit-timing incentives.
- **Relevance.** The dossier's carry-netting calculation holds gross returns fixed. Report the 0/20 cost as a range. The evidence comes from VC fund contracts, so transferring it to co-investment vehicles is [inference].

**25. [Intermediated investment management in private markets: Evidence from pension fund investments in real estate](https://doi.org/10.1016/j.finmar.2014.11.002)** [missed]
- Andonov, A., Eichholtz, P., & Kok, N. · 2015 · *Journal of Financial Markets* 22, 73–103 · CR 57 (S2 61) · DOI 10.1016/j.finmar.2014.11.002 · abstract via Crossref (SSRN version DOI 10.2139/ssrn.1996819, 2012)
- **Finding.** Larger pension funds invest internally and have "lower costs, and higher net returns". Delegating to intermediaries "increases costs and disproportionally reduces returns".
- **Relevance.** This is real-estate evidence for scale economies in in-house direct programs. With Dyck & Pomorski (§4.7), it supports resourcing the $18bn Co-investment group's own underwriting [inference].

---

## 4. Missed-but-important papers and their design implications

Symbols follow the dossier's §6. Every item is **[inference]** built on the cited abstracts unless it quotes a paper. Item numbers refer to §3.

### 4.1 State variables (additions to dossier §6.1)

| Symbol | Meaning | Level | Evidence |
|---|---|---|---|
| $\tau^{cyc}_i$ | The deal's position in the lead sponsor's fund cycle: months to the end of the investment period; done-before-next-close flag; sponsor in market | Deal | Hüther (#6); Braun & Schmidt (#7); BJS offer probit (cited, verified); Degeorge et al. (§4.7) |
| $s_i$, $\Delta S_g$ | Relative deal size (equity ÷ sponsor fund size) and the sponsor's fund-size step-up | Deal / GP | Bhardwaj et al. (#8); FIL (#2); BJS (#1) |
| $n^{act}_g$ | Sponsor bandwidth: number of simultaneous active investments | GP | Lopez-de-Silanes et al. (#10) |
| $CF_i$ | Continuation-fund event state (none, offered, sold, rolled) and the asset's performance rank in the legacy fund | Deal | Abuzov et al. (#9) |
| $(st_i, md_i, IM_i)$ | Mark history: staleness count, markdown frequency, interim multiple | Deal | Ercan et al. (#21) |
| $VCP_i$ | Value-creation-plan execution score from GP monitoring reports; plan type (operational or financial engineering) | Deal | Biesinger et al. (#16) |
| $\tilde m_{0,i}$, $\tilde m_{T,i}$ | Entry and exit multiples relative to the same-segment market multiple | Deal | Puche & Braun (#15) |
| $ERP_t$ | Equity-risk-premium or valuation state, next to the credit window $c_t$ | Global | Haddad et al. (#14); Axelson et al. (#13) |
| $RT_i$ | Rights type: LP-discretion or GP-directed vehicle | Deal | Tuft (#4); LMSZ (#3, WP gap per the verification log) |
| $\phi^{pc}_g$, $o_i$ | Portfolio-company fee intensity and the offset available to co-investors | GP / deal | Phalippou, Rauch & Umber (#23) |
| $R^{sp}_{i,t}$ | Sponsor rescue capacity: the lead fund's remaining reserves and dry powder | Deal / GP | Hotchkiss et al. (#19) |

### 4.2 Models
1. **A conditional selection prior instead of a flat "no adverse selection" default (§6.4).**
   - The prior is $\mu_i=\mu_{ref}(L_0,m_0,\text{sector},ERP_t,c_t)+\beta_{cyc}\tau^{cyc}_i+\beta_s s_i+\beta_{bw}n^{act}_g+\beta_{RT}\mathbb 1\{\text{GP-directed}\}$.
   - Sign priors: $\beta_{cyc}\le0$ (#6, #7), $\beta_s<0$ (#8, #2), $\beta_{bw}<0$ (#10), $\beta_{RT}<0$ (#3).
   - Constrain the unconditional mean to BJS's "no adverse selection" (#1). Estimate the loadings hierarchically on licensed deal data and on ADIC's offer log (dossier §9, Q4).
2. **Draw the entry terms jointly by regime.**
   - Draw $(L_0, m_0)$ from the credit and risk-premium state, with a negative link to expected EV growth (#13, #14).
   - This replaces the re-basing experiment that varies $L$ with the EV process held fixed, which verification R7 flags as a model artifact.
3. **Benchmark and risk layer.**
   - Score deals against a levered, size- and sector-matched public index (#12), with a jump-CAPM deal beta (#11).
   - E1's $\beta_A V/E$ already gives 2.25 at L = 0.6, consistent with #11.
   - Report PME alongside, never alone.
4. **Distress and rescue module (E3, E6).**
   - Raise default incidence and lower loss severity (#19).
   - Add a rescue call when ICR falls below a trigger. ADIC either participates pro rata, with recovery above the current $U(0,0.10)$, or is diluted.
   - Make $q_F$ depend on state instead of holding it at 5% a year.
5. **Continuation-fund event process (E4, E6).**
   - The GP triggers a CV offer with an intensity that rises with the asset's quality rank and with the GP's carry in the money. See #9; stream 04 adds a carry-in-the-money indicator.
   - ADIC's sell-or-roll choice is valued at Corporate Finance's liquidity shadow price.
   - Apply the SACV price distribution only to CV-eligible assets. This supports verification R1 and R5.
6. **Deal-level nowcast and SELL screen (E7).** Add staleness and markdown-frequency features, and allow interim mark-ups to load negatively on forward returns (#21).
7. **Concentration in certainty-equivalent terms.** Use an expected-utility haircut as a function of effective N (#18), alongside CVaR. Ick & Nowak (§4.7) argue for higher-moment-aware sizing.

### 4.3 Parameters

| Parameter | Literature value | Use at ADIC [inference] |
|---|---|---|
| Deal-level equity β (gross, historical leverage) | 2.2–2.4 (#11; draft, via WebSearch; unverified) | Confirms β_A ≈ 0.9 at L ≈ 0.6. Implies β_E ≈ 1.4–1.6 at today's L of 0.36–0.45 |
| Historical buyout net debt/EV | ≈ 65% (#12; second-hand practitioner summary) | Supports L = 0.60–0.65 in the static fit |
| Fund-size elasticity | −0.1pp net IRR per +1% fund size; larger deals perform worse (#8) | Prior on $\beta_s$; relative deal-size cap |
| Late-cohort effect | Late, pre-fundraising deals earn less (#6); returns drop after a new partnership is set up (#7) | Sign prior $\beta_{cyc}<0$. No magnitude in the abstracts, so estimate it |
| Under-diversification cost | Certainty-equivalent returns up to 5% below the average-fund inference; about 5 funds a year suffice at fund level (#18) | Calibrate a CE haircut against effective N. Deal books need far more names |
| Post-recap distress effect | Distress "2.4 times the targeted firm mean" for +84% debt (#20); the OLS estimate is about 0.42× the mean (verification R4) | At φ = 0.25, linear scaling gives roughly a 1.1× (OLS) to 1.7× (IV) hazard multiplier. Parameterise it; do not fix ×2.4 |
| Portfolio-company fees | About $20bn over 20 years, more than 6% of equity invested; persistent within GPs (#23, per G1) | GP-level intensity in E8; zero offset for co-investors unless negotiated |
| Continuation-fund share of exits | 9% of PE exits in 2024 (#9) | Prior for the CV arrival rate |
| LP response to CVs | LPs "overwhelmingly" exit (#9); 80–90% cash out per Deane et al., 2025 (stream 04) | Base rate for other LPs. ADIC's own choice is priced, not assumed |
| Default and resolution of PE-backed firms | Higher default rates than other leveraged borrowers; faster, less liquidating restructurings (#19) | Higher default incidence and lower LGD than a pure write-off. Reconcile with Kaplan & Strömberg's 1.2% a year (verification R14) |
| Deal-by-deal carry incentive | Associated with higher gross and net returns, in VC (#24) | A sensitivity on gross returns when comparing 0/20 with fund terms |
| Relative pricing | "Selling high yields about twice as much as buying low" (#15) | Weight the relative exit multiple in the "what you need to believe" flags |

### 4.4 Constraints
1. **Late-cohort concentration.** Cap the share of new tickets in deals made late in the sponsor's investment period or within N months of its next close. Above the cap, require explicit IC sign-off (#6, #7).
2. **Relative deal size.** Use a soft cap on $s_i$, and a tighter one for sponsors with large fund-size step-ups (#8, #2).
3. **Rights type.** Prefer LP-discretion rights. GP-directed vehicles get a prior haircut and no liquidity-timing credit (#3, #4).
4. **Rescue reserve.** Corporate Finance holds liquidity for distress follow-ons as well as for calls at close (#19). Policy sets a participation rule in advance.
5. **CV elections are events, not controls.** The optimizer may not count CV proceeds as liquidity before a GP launches a CV (#9; verification R5).
6. **Fee disclosure gate.** Vehicles with high GP-level portfolio-company-fee intensity and no offset need IC disclosure (#23).

### 4.5 Objective terms (dossier §6.7)
- Score co-investments on alpha against a levered, size- and sector-matched benchmark under ADIC's own SDF (#12). Korteweg, Panageas & Systla (2026, verified in the G1 review) argue for investor-specific SDFs. Do not score on PME against a broad index alone.
- Add a certainty-equivalent concentration penalty (#18) next to the concentration-CVaR term.
- Fee leakage should include portfolio-company fees (#23). Show the deal-by-deal carry incentive effect as a sensitivity (#24).
- Credit the timing option of LP-discretion rights in the liquidity objective, at Corporate Finance's transfer price (#4).

### 4.6 Agent and IC design
1. **Offer-screen agent ("why this deal, why now").**
   - Computes $\tau^{cyc}_i$, $s_i$, $n^{act}_g$, $RT_i$ and $\tilde m_{0,i}$.
   - Asks for the GP's retained-versus-offered allocation.
   - Flags late-cohort and pre-fundraising offers (#6, #7, #8, #2, #15).
2. **Benchmark agent.** Reports each deal's levered matched benchmark and jump-CAPM beta next to its PME (#11, #12).
3. **Deal-level mark-forensics agent.** Computes staleness and markdown-frequency features for the nowcast and SELL screen (#21).
4. **Plan-execution tracker.** Ingests value-creation plans and GP monitoring reports, updates beliefs, and flags theses led by financial engineering (#16).
5. **CV-response agent.** When a GP launches a CV on a co-invested asset, it prices sell versus roll under ADIC's beliefs and Corporate Finance's liquidity price. It notes that CV assets are positively selected (#9).
6. **Rescue playbook.** The Co-investment group (asset side) and Corporate Finance (funding side) agree in advance on participation rules and capacity (#19).
7. **Fee-forensics agent.** Checks portfolio-company fees and offsets by GP, and deal-by-deal carry terms (#23, #24).
8. **IC checklist.**
   - Conditional-selection evidence.
   - Entry-regime flags: risk premium and credit (#13, #14).
   - Levered-benchmark alpha.
   - Certainty-equivalent concentration.
   - Rights type.
9. **Organization.**
   - Scale supports in-house underwriting (#25; Dyck & Pomorski). Peer SWFs have moved toward co-investing (#5).
   - Corporate Finance owns treasury (user-confirmed), so it sets the liquidity price used by co-investment pacing, rescue calls and CV responses.
   - The Secondaries group is a hybrid of direct and fund investments (user-confirmed). Its direct deals should share this deal-level engine and the CV evidence (#9).

### 4.7 Further relevant papers (one line each)
**Copied from sibling reviews (Consensus URLs verbatim).**
- [On Secondary Buyouts](https://consensus.app/papers/details/7bf7597e234759c785c4d2057d100202/?utm_source=claude_desktop) (Degeorge et al., 2016, *JFE*; record from `05_secondaries_navfin.lit.md`). Buyers under pressure to spend underperform. This is the deployment-pressure analogue of #6.
- [Benchmarking the Performance of Private Equity Portfolios of the World's Largest Institutional Investors: A View from CEM Benchmarking](https://consensus.app/papers/details/64a6b1933e72521789155b89b5399519/?utm_source=claude_desktop) (Beath & Flynn, 2020, *J. Investing* 30(1) 67–87, per Crossref; URL from `02_endowment_swf.lit.md`). Per that review, internal direct and co-investment programs beat fund-of-funds.
- [Modeling the exit cashflows of private equity fund investments](https://consensus.app/papers/details/06a53f89abd05350ae89e3e77c5fc5e6/?utm_source=claude_desktop) (Tausch, Buchner & Schlüchtermann, 2022, *J. Risk*; URL from `04_pe_cashflows.lit.md`). A joint deal-level model of exit timing and multiple that handles many defaults. It is a template for E4 [inference].

**Retrieved this session (links as returned).**
- [Money Chasing Deals and Deals Chasing Money - The Impact of Supply and Demand on Buyout Performance](https://doi.org/10.2139/ssrn.967527) (Hege, Zipser & Gottschalg, 2007, SSRN). On 684 buyouts, performance falls when large volumes of commitments chase targets. This supports vintage discipline.
- [Omega Based Portfolio Optimization - A Simulation Study on Private Equity Investments](https://doi.org/10.2139/ssrn.1009612) (Ick & Nowak, 2007, SSRN). On 2,380 PE investments, Omega and mean-variance frontiers "deviate substantially", so higher moments matter.
- [Investor Scale and Performance in Private Equity Investments](https://doi.org/10.1093/rof/rfv030) (Dyck & Pomorski, 2016, *RoF* 20(3) 1081–1106). Up to one-third of large holders' outperformance comes from "avoiding fund-of-funds and investing directly".
- [The Rise of Private Equity Continuation Funds](https://doi.org/10.67929/ecgi-law-733-2023) (Kastiel & Nili, 2023, ECGI law WP). A legal analysis; most existing investors decline to roll.
- [Direct Investments in Private Firms by Institutional Investors: Issues And Evidence](https://doi.org/10.1093/oxfordhb/9780195391589.013.0003) (Nielsen, 2012, *Oxford Handbook of Private Equity*) and [Institutional Investors and Private Equity](https://doi.org/10.2139/ssrn.389082) (Nielsen, 2003, SSRN). Institutions invest directly with governance terms that limit minority expropriation, and syndicate to reduce idiosyncratic risk.
- [Sovereign Wealth Funds and Private Equity](https://doi.org/10.1093/oxfordhb/9780198754800.013.12) (Wright & Amess, 2017, Oxford Handbooks Online). About half of SWFs invest in PE; 14% of institutional capital raised by PE funds in 2015 came from sovereign wealth.
- [The Economics of Private Equity Funds](https://doi.org/10.1093/rfs/hhq020) (Metrick & Yasuda, 2010, *RFS* 23(6) 2303–2341). Fee and carry economics; per the G1 review, about two-thirds of GP revenue is fixed.
- Abstract not retrieved; metadata only:
  - [Leveraged buyouts and financial distress](https://doi.org/10.1016/j.frl.2020.101452) (Ayash & Rastad, 2021, *FRL* 38, 101452). A second-hand thesis summary reports 484 LBOs (1980–2006) and higher bankruptcy rates for targets. Unverified.
  - [Who Is the Sovereign among Sovereign Wealth Funds? A Network Analysis of Co-Investments](https://doi.org/10.3905/jpe.2016.19.4.007) (Gianfrate & Merlin, 2016, *J. Private Equity* 19(4) 7–18).
  - [Patient Capital](https://doi.org/10.1515/9780691190037) (Ivashina & Lerner, 2019, Princeton UP), a book on long-term investors.
  - [Private Equity Strategies](https://doi.org/10.1002/9781119094746.ch4) (McCombie, chapter in *The Complete Direct Investing Handbook*, Wiley, 2017), a practitioner text.

### 4.8 Evidence gaps (no academic source found)
1. **Co-investment performance after about 2010.** BJS cover deals through about 2010 and FIL cover 1991–2011. For the continuation-vehicle era, Abuzov et al. (#9) is the closest evidence.
2. **Pricing of LP-led single-asset or strip sales of co-investment stakes.**
3. **An LP-level co-investment offer rate (θ).** Tuft (#4) gives determinants only. Bain's 33¢ is a GP-level ratio (verification R8).
4. **Holdco PIK or SPV leverage on co-investment stakes.**
5. **The size of a vintage common factor in deal-level co-investment returns.** The dossier's vintage-diversification result rests on assumed factor sizes (verification R10).

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation (section) | Challenging evidence | What it implies [inference] |
|---|---|---|---|
| 1 | "Selection is not the main problem; timing and size are." The failure mode is "not being sold lemons" (§1 item 1, §8 item 1) | FIL (#2) attribute the poor performance to GPs' "selective offering of large deals". Hüther (#6): late, pre-fundraising investments earn less. BJS's probit (cited) shows offers are likelier before the follow-on close. Braun & Schmidt (#7). LMSZ (#3): top LPs get top vehicles. Abuzov et al. (#9): GPs move better-performing, larger assets into CFs. | Selection is conditional, not absent. It works through offer timing, deal size, LP standing and asset retention. Use the conditional prior (§4.2 item 1) and the offer-screen agent, and keep BJS as the unconditional mean. |
| 2 | Re-base to today's leverage: at L = 0.40 the expected multiple falls from 1.73 to 1.45 (1.30 with compression) (§1 item 4, §6.3) | Axelson et al. (#13): higher leverage goes with higher prices and *lower* returns. Haddad et al. (#14): the risk premium drives activity, leverage and performance together. | Leverage, entry price and EV growth move together by regime. Re-base them jointly (§4.2 item 2). Present 1.45 and 1.30 as stylised sensitivities, as verification R7 also concludes. |
| 3 | Calibrate and judge on PMEs; BJS portfolios "beat funds" (§1, §4.1, §6.3, §6.8) | L'Her et al. (#12): against a levered, size- and sector-matched benchmark, buyout outperformance disappears. Axelson–Sorensen–Strömberg (#11): deal β is 2.2–2.4. | BJS's result is relative to funds. Absolute value against ADIC's opportunity cost may be near zero before fees. HOLD and LEVER hurdles should use a levered benchmark. |
| 4 | "0/20 co-investments are about as expensive as a fund" (§1 item 6, §2.4, §6.3) | Hüther et al. (#24): deal-by-deal carry is associated with higher gross *and* net returns (VC funds). | The netting calculation holds gross returns fixed. Incentive effects may offset part of the cost, so report a range. Phalippou, Rauch & Umber (#23) *support* the hidden-cost point. |
| 5 | E3/E6: write-off with equity recovery $U(0,0.10)$; constant follow-on rate $q_F$ of 5% a year (§6.2, §6.10) | Hotchkiss et al. (#19): PE-backed firms default more often but restructure faster and liquidate less. Sponsors infuse capital as distress approaches. | Follow-on calls depend on state and cluster in distress, and recovery depends on participation. A constant $q_F$ understates the wrong-way liquidity demand on Corporate Finance. |
| 6 | SELL worked example priced from SACV distributions: "in a drought it wins outright" (§1 item 8, §6.5) | Abuzov et al. (#9): CV assets are "better performing and larger" than other legacy assets. | SACV prices are positively selected (agrees with verification R1). Use quality-conditional bids, and treat the CV route as a GP-triggered event (verification R5). |

**Citation-use problems, which are not challenges from new literature (detail in §1–§2):**
- The BGK sign is reversed (§7).
- Lopez-de-Silanes et al. is read as deal-size evidence (§4.2).
- The Bhardwaj–Gupta–Howell multiplier is applied to a recap about a third the size of the paper's average debt increase (E5).

**Missed papers that support the dossier:**
- Size discipline: Bhardwaj et al. (#8).
- Vintage and flow discipline: Hege et al. (§4.7).
- Hidden fees: Phalippou, Rauch & Umber (#23).
- Concentration penalty: Gredil, Liu & Sensoy (#18).
- The PE-to-co-investment flow link and its liquidity role: Tuft (#4).
- In-house scale: Andonov et al. (#25); Dyck & Pomorski (§4.7).
- E4's performance-tilted, regime-dependent exit hazard: Lopez-de-Silanes et al.'s quick flips (#10); Cao (#22).
- β and L calibration: the deal β of Axelson–Sorensen–Strömberg (#11); the ≈ 65% leverage in L'Her et al. (#12).
- No fundraising haircut on deal marks: Hüther (#6).

---

## 6. Usage message

The last (and only) usage message returned by Consensus, verbatim:

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Search log

**Totals: 54 queries across engines, including failed attempts.**

| Engine | Calls | Outcome |
|---|---|---|
| Consensus | 3 | All failed (quota) |
| OpenAlex | 10 | 8 returned; 2 failed with HTTP 429 |
| Semantic Scholar | 7 | 4 returned |
| Crossref | 31 | 14 topical, 13 title or metadata, 4 DOI-lookup calls |
| WebSearch | 3 | All returned |

No search filters were applied anywhere.

**Consensus (3; all failed).** "Adverse selection and the performance of private equity co-investments", three times, 30 seconds apart. Every attempt returned the message in §6.

**OpenAlex (10; plain relevance search).**
1. Adverse selection and the performance of private equity co-investments
2. Investing outside the box: Evidence from alternative vehicles in private equity
3. How persistent is private equity performance? Evidence from deal-level data
4. Giants at the gate: Investment returns and diseconomies of scale in private equity
5. Kaplan Stromberg Leveraged Buyouts and Private Equity NBER working paper 14207 (no relevant hit; resolved by DOI in Crossref)
6. Capital Structure and Firm Outcomes: Evidence from Dividend Recapitalizations in Private Equity
7. What do private equity firms say they do?
8. Borrow cheap, buy high? The determinants of leverage and pricing in buyouts
9. Alpha and beta of buyout deals: a jump CAPM … (HTTP 429)
10. The same query, retried (HTTP 429). A diagnostic probe then showed the daily credit cap was exhausted (Retry-After 48,694 s).

**Semantic Scholar (7).**
1. Batch by DOI: FIL, BJS, LMSZ. Returned FIL and LMSZ abstracts; BJS was not found by its *JFE* DOI.
2. Title match: BJS. Returned the abstract.
3. Search: Axelson–Sorensen–Strömberg (429).
4. Search: "deal-level private equity returns distribution" (429; rerun on Crossref).
5. Batch: L'Her; Puche & Braun; Braun & Schmidt; Gianfrate & Merlin. Succeeded on the 4th try; returned the Puche & Braun abstract.
6. Batch: Ayash & Rastad (429).
7. Batch: Ayash & Rastad; L'Her; Ewens et al.; Andonov et al. Returned the Ewens et al. abstract only.

**Crossref: topical backfill (14; plain query).** Seeds 1–3 were run as given; seed 3 was refined slightly. The rest are refinements.
1. private equity co-investment performance adverse selection
2. direct investing private equity institutional investors
3. deal-level private equity returns distribution buyout investments
4. co-investment limited partners general partners private equity fees relationships
5. sovereign wealth funds direct investments private equity deals co-investing
6. risk-adjusted performance buyout leverage size bottom-up deal level beta
7. diversifying private equity portfolio skill uncertainty certainty equivalent number of investments
8. leveraged buyouts financial distress bankruptcy private equity backed firms
9. dividend recapitalizations private equity sponsors leveraged loans
10. buyout activity aggregate discount rates credit conditions returns
11. holding period exit timing buyout portfolio companies survival analysis
12. continuation funds GP-led secondary transactions private equity
13. value creation plans private equity execution realized outcomes Biesinger Bircan Ljungqvist (author names included to locate a known study)
14. co-investments private equity returns performance limited partners deal offers

**Crossref: title and metadata lookups (13).**
- Axelson–Sorensen–Strömberg (2 queries; not in Crossref)
- Broadie–Glasserman–Kou continuity correction
- Diversifying private equity (Gredil)
- Private equity and the resolution of financial distress
- Leveraged buyouts and financial distress (Ayash & Rastad)
- The price of diversifiable risk in VC and PE
- Intermediated investment management in private markets
- Patient Capital
- Does fund size affect PE performance?
- Private equity portfolio company fees
- Kou jump-diffusion
- Rockafellar–Uryasev CVaR

**Crossref: DOI lookups (4 calls).**
1. 10.3386/w14207, w33435, w21133.
2. 10.2139/ssrn.2871458 and 10.1016/j.jfineco.2019.01.009.
3. Ten DOIs: Phalippou–Rauch–Umber; Hüther et al.; Metrick–Yasuda; Hüther (*JFQA*); w33637; w33596; Tausch et al.; Dyck–Pomorski; Beath–Flynn; Tuft.
4. 10.2139/ssrn.5215933 and 10.2139/ssrn.4833819 (Ercan et al.).

**WebSearch (3).**
1. Axelson–Sorensen–Strömberg working paper. Found the 2014 draft on Axelson's LSE page and the CV listing.
2. L'Her et al. (*FAJ* 2016) abstract. Found the CFA Institute page.
3. Ayash & Rastad (*FRL* 2021) abstract. Found the IDEAS listing only; findings second-hand.

**Diagnostic calls (not counted).** Two direct HTTP probes, one each to OpenAlex and Semantic Scholar, to read their 429 headers.

**Helper scripts** (session scratchpad; not ADIC data; may not persist):
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g4lit_scripts\oa.ps1` (OpenAlex)
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g4lit_scripts\s2.ps1`, `s2t.ps1` and `s2s.ps1` (Semantic Scholar batch, title match and search)
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g4lit_scripts\cr.ps1` and `crs.ps1` (Crossref DOI lookup and search; no mailto sent)
