# Verification log: Stream 06, portfolio-level leverage (`dossiers/06_leverage.md`)

**Verifier:** adversarial fact-check agent. **Date:** 2026-10-18. **Dossier version checked:** 570 lines, "As of 2026-10-18".
**Method:**
- Each load-bearing claim was checked against the primary page or document where one was reachable.
- The PDFs (Jefferies, DBRS/CPP, Moody's/OTPP, ILPA, the CPP F2025 Annual Report and the Gorton-Metrick WP) were downloaded and their text extracted locally with `pypdf`, then searched.
- All quantitative examples in Sections 1, 2.6 and 6.8–6.9 were recomputed in Python (scipy/numpy), with a Monte Carlo cross-check of the Dufresne ruin formula.

**Process caveats:**
- The session-wide web-search budget ran out partway through. After that I used only direct fetches of known primary URLs.
- Four sources could not be read in full:
  - Temasek: every URL returned 403.
  - CME article: two direct fetches timed out, so it was checked via a search-index excerpt of CME's own page.
  - AllianceBernstein: the fetch failed with a header-overflow error.
  - Enterprise AM (Mubadala T+55): not reachable, as the dossier also notes.
- Claims resting only on those sources are marked *unverifiable* unless the primary text was seen.

---

## 1. Summary

- **Facts: strong.** I checked 34 load-bearing claims: **26 confirmed, 3 corrected, 0 refuted, 5 unverifiable.**
  - Every rate, market and peer figure the author flagged as high-confidence matches its primary source, often to the decimal: NY Fed SOFR, FOMC statement, Treasury curve, Emirates NBD/PIF, Harvard Magazine, D. E. Shaw, Jefferies, DBRS, Moody's, OTPP, NBIM, BoE, ILPA, NBER/APW, the Harvard Crimson and Semafor.
  - The one substantive factual correction is the Reuters/Kitco equity-financing item. The "200bp → 89bp" path mixes two different metrics, and the 200bp is equity-repo financing, not futures-implied financing.
- **Arithmetic: fully reproducible.** All recomputed tables match: the Kelly/log-growth table, the Dufresne ruin table (my Monte Carlo gives 58.6% vs the closed-form 57.9%), the implied cost of selling, the sell break-evens, the HOLD/SELL/LEVER example, the regime shares and the liquidity arithmetic.
- **Citations: clean.** All 18 key references checked exist, with correct authors, year, title and venue. I found no hallucinated or garbled citations, only minor attribution looseness (Section 4).
- **Reasoning: where the risk is.** The main problems are framing and design specification, not facts:
  - **R1. Peer-leverage anchors are not like-for-like.** CPP's own Board-governed "recourse leverage" is **36% of net assets**, with a **45% limit**. The 9.7% figure is DBRS's narrow debt-only ratio.
  - **R2. The executive summary overclaims.** It says levering "cannot" reach 10%, but its own table shows 10% is reachable at 2.36× with 4.05% funding. The infeasibility threshold is ≈4.28%, not 4.65%.
  - **R3. The HOLD/SELL/LEVER formula is mis-normalized.** It implicitly assumes 100% LTV, and λ cancels out of a like-for-like SELL-vs-LEVER comparison.
  - **R4. The drawdown barrier can force a net-short overlay** after a drawdown of about 14% when 60% of the book is illiquid.
  - **R5. The LCR/NSFR analogs depart from Basel** and omit unfunded commitments.
  - **R6. The objective can double count** financing and fire-sale costs.
  - **R7–R14.** Smaller specification issues.
- **Overall reliability: HIGH** for sourced facts, arithmetic and citations, and **MEDIUM** for the design implications. Fix R1–R6 before IC use.

---

## 2. Claims table

| # | Claim (as in dossier) | Verdict | Corrected value / verifier note | Source URL |
|---|---|---|---|---|
| 1 | SOFR 3.89% on 15 Oct 2026, volume ≈US$3.03trn | **Confirmed** | 3.89%; volume US$3,025bn; 1st–99th percentile 3.85–3.97% | https://markets.newyorkfed.org/api/rates/secured/sofr/last/5.json |
| 2 | FOMC raised the target range 25bp to 3.75–4.00% on 16 Sep 2026, 12–0, "Inflation remains elevated"; the first hike since 2023 | **Confirmed** | Statement text matches. The 29 Jul 2026 statement *held* at 3.50–3.75% by a 9–3 vote (Hammack, Kashkari and Logan dissented in favour of a hike), which is consistent with "first hike since 2023" | https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm ; https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm |
| 3 | UST par yields on 16 Oct 2026: 3m 4.26, 2y 4.74, 5y 4.89, 10y 5.09, 30y 5.43; 10y 5.31% on 5 Oct | **Confirmed** | Exact match (20y 5.47%) | https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202610 |
| 4 | "3m bills about 37bp above SOFR" (Section 4.1) | **Corrected** (minor) | The raw difference is 37bp, but CMT yields are bond-equivalent and SOFR is act/360. On a like-for-like basis it is ≈32bp (SOFR 3.944% vs 4.26%). The direction of the inference (hikes priced) is unaffected | (same Treasury and NY Fed URLs) |
| 5 | PIF US$2bn 10y sukuk at T+85 on 21 Jan 2026 (IPT T+120; books ≈US$11bn); Saudi sovereign 10y ≈79bp | **Confirmed** | All four numbers match. Caveat: PIF is rated Aa3/A+, so "AA-area" holds on Moody's scale only | https://www.emiratesnbdresearch.com/en/articles/pif-2036-usd-sukuk |
| 6 | PIF US$7bn 3/7/30y in May 2026, book US$23.8bn, spreads T+95–99 | **Unverifiable** (spreads) | Size, tenors and the US$23.8bn peak book are confirmed. The source gives no spreads, initial guidance (IPT) or date | https://www.zawya.com/en/capital-markets/bonds/saudi-pif-raises-7bln-in-3-tranche-bond-sale-orderbook-tops-238bln-q5qhbejk |
| 7 | Mubadala 10y at ≈T+55, Oct 2025 | **Unverifiable** | Source not reachable. Mubadala's ratings (Aa2/AA/AA, issuer MDGH) are confirmed on Mubadala's investor page | https://www.mubadala.com/en/investors/overview |
| 8 | Harvard, Dec 2008: US$1.5bn taxable 5/10/30y at 5.03/6.06/6.53%, ≈T+335–337.5bp; plus US$1bn tax-exempt; swap notional US$3.52bn, termination value −US$330.4m at 30 Jun 2008; partly to fund swap terminations | **Confirmed** | Notional US$3,524.7m; fair value (US$330.4m); "3.35 to 3.375 percentage points" over Treasuries | https://www.harvardmagazine.com/print/3822?page=all |
| 9 | Harvard 2008: "private-partnership distributions slowed sharply while capital calls continued" | **Corrected** (minor) | The source says distributions "slowed to a trickle" and that partnerships "have contractual rights to call" capital. It does **not** say calls continued | https://www.harvardmagazine.com/print/3822?page=all |
| 10 | D. E. Shaw: S&P 500 futures implied financing averaged ≈30bp over risk-free in 2021–23 and peaked >140bp in Dec 2024 | **Confirmed** | "average of 0.3% seen between 2021 and 2023"; "peaked at over 1.4% in December 2024" (20-day rolling average). The piece is dated about 23 Jan 2025 | https://www.deshaw.com/library/imbalance-sheet |
| 11 | CME: June-2026 ES roll implied financing +81bp over 3m SOFR, the richest June roll since at least 2007 | **Confirmed** (via search-index excerpt of CME's own page; two direct fetches timed out) | Both figures appear in the CME text excerpt | https://www.cmegroup.com/articles/2026/funding-the-us-equity-market-to-new-heights.html |
| 12 | CME: "vs +38bp in Q2 2025" | **Unverifiable** | Not in any retrieved text | (same) |
| 13 | Reuters/Kitco: equity financing cost ≈200bp over fed funds on 26 Jun 2026 (Morgan Stanley data), then fell to 89bp; primary dealers ≈US$211bn | **Corrected** | (a) The 200bp (Morgan Stanley data, "highest since December 2024") is the "cost of financing equity positions", i.e. equity repo. It is **not** futures-implied financing, yet the executive summary lists it under "Equity-index futures". (b) The 89bp is "another metric that has a quarterly maturity", so "fell to 89bp" is not a like-for-like decline. (c) The US$211bn is Fed data on dealers' balance-sheet exposure as of 24 Jun 2026 | https://www.kitco.com/news/off-the-wire/2026-07-09/us-markets-brace-renewed-funding-pressure-leverage-rises |
| 14 | Rede (Jun 2026): NAV margins converging on 4–7%; pricing "may rise from here" | **Confirmed** | "converge around a 4-7% margin range"; "may have reached an inflection point and may rise from here"; the gap between recourse-light and secured deals narrowed (no numbers given). Dated 23 Jun | https://www.rede-partners.com/news-insights-database/publication-rede-nav-2026 |
| 15 | AllianceBernstein: NAV-loan LTV 5–30% at close; OID 1–3% | **Unverifiable** | Page fetch failed. These figures are used as defaults in Sections 6.5 and 6.10 | https://www.alliancebernstein.com/us/en-us/investments/insights/investment-insights/nav-loans-flexibility-for-private-equity-when-holding-periods-extend.html |
| 16 | ILPA (Jul 2024): NAV market ≈US$100bn (FFA estimate), US$600bn by 2030; 80% portfolio support / 20% distributions; distributions often recallable; NAV facilities are fund-level leverage; LP-led options may be cheaper; LTV breach leads to paydown or cash sweep | **Confirmed** | All quoted in the text, e.g. "It is ILPA's position that NAV-based facilities constitute fund-level leverage…" and "there may be more cost-effective LP-led options…" | https://ilpa.org/wp-content/uploads/2024/07/ILPA-Guidance-on-NAV-Facilities-2024.pdf |
| 17 | Jefferies H1 2026: US$118bn volume (LP 56 / GP-led 62); LP pricing 87% (buyout 91, infra 91, credit 89, venture 79, RE 68); tail-end 25%+ and Asia/EM 35%+ discounts; liquidity motive 45%; pensions + SWFs 48% of LP supply; 33% structured, 26% deferred; US$290bn dry powder; 1.2× overhang; 15 deals >US$1bn, 5 >US$2bn | **Confirmed** | Every figure matches the report text | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 18 | Jefferies: LP distribution yield ≈10% in H1 2026, <20% since 2023, vs a 25% average since 2001 | **Confirmed** | Verbatim: "stayed near 10% in H1 2026 and has remained below 20% since the beginning of 2023 (as compared to a historical average of 25% since 2001)" | (same) |
| 19 | CPP/DBRS: recourse debt C$76.6bn = 9.7% of adjusted net assets; repo C$113.3bn (vs C$72.1bn); notional C$724.9bn; stressed 1-month LCR 6.9 vs 1.0 minimum; DBRS excludes repo from financial leverage | **Confirmed** | All match. Note: "adjusted net assets" = net assets **plus** recourse debt, so the ratio is D/(E+D). On plain net assets it is 10.7% | https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-DBRS-Rating-Report-091825.pdf.pdf |
| 20 | CPP base-CPP recourse leverage 36% of net assets (18% in F2021) (via search excerpt) | **Confirmed** (primary) | CPP F2025 AR p.44: 18%→36% over F2021–25, C$88bn→C$238bn. **Board limit 45%** (base CPP) / 30% (additional CPP). The definition *includes repo and the net notional of leverage-generating derivatives*, net of cash and reverse repo. See R1 | https://www.cppinvestments.com/wp-content/uploads/attachments/CPP-Investments-F2025-Annual-Report-English.pdf |
| 21 | CPP F2026: net assets C$793.3bn; 7.8% return; benchmarks 13.2% | **Confirmed** | Press release dated 20 May 2026 | https://ca.finance.yahoo.com/news/cpp-investments-net-assets-total-100000452.html |
| 22 | OTPP/Moody's (20 Jul 2026): adjusted leverage 17% at end-2025 (2021–25: 20/19/18/17/17%); upgrade factor <10% sustained, downgrade factor >25% sustained; notional 3.1× total assets; repo + short sales fund 6.0% of gross assets (11.5% end-2019); liquid assets 32%; Level 3 52%; liquidity score aa1 with "Asset Encumbrance" as driver; nettable repo and derivatives are netted | **Confirmed** | Notional C$1,106.4bn vs total assets C$353.8bn = 3.13× | https://www.otpp.com/content/dam/otpp/documents/1-home/about/investors-relations/Credit_Opinion-Ontario-Teachers-Pension-Plan-20Jul2026-PBC_1490754.pdf |
| 23 | OTPP "Funding and other": −C$87.3bn (−32%) in 2025 vs −C$113.1bn (−43%) in 2024, so ≈1.32× gross | **Confirmed** | Net investments C$272.6bn (2025) and C$260.9bn (2024), giving 1.320× and 1.433× | https://otpp.com/en-ca/about-us/news-and-insights/2026/ontario-teachers-announces-positive-2025-results/ |
| 24 | NBIM: leverage ≤5% of the NAV of the combined equity + FI portfolios; securities borrowing ≤5% of fund NAV; unlisted RE debt ratio ≤25%; amended 9 Dec 2025 | **Confirmed** | §4.1.5, §4.1.7, §4.2.6. The dossier omits §4.3.2(e): unlisted renewable-energy infrastructure debt ratio ≤**60%**, which is relevant to infrastructure leverage analogs | https://www.nbim.no/en/about-us/about-the-fund/governance-structure/executive-board-documents/investment-mandate---government-pension-fund-global/ |
| 25 | BoE LDI: ≈250bp = ≈170bp systemic (1-in-100 five-day 30y index-linked shock) + ≈80bp (99.8th percentile, 10y look-back); five-day collateral delivery; unencumbered assets; >35bp on two days vs a prior record of 29bp; four-day rise >2× any since 2000 | **Confirmed** | All quoted; published 29 Mar 2023 | https://www.bankofengland.co.uk/financial-policy-summary-and-record/2023/bank-staff-paper-ldi-minimum-resilience |
| 26 | FSB (10 Dec 2024): eight recommendations; March 2020, Archegos, 2022 commodities and LDI as motivating episodes | **Confirmed** | Recs 1–8 cover governance/CFP, stress testing ("extreme but plausible") and collateral management | https://www.fsb.org/2024/12/liquidity-preparedness-for-margin-and-collateral-calls-final-report/ |
| 27 | Gorton-Metrick haircut index rose from near zero to ≈45–50% "for structured collateral" [K, verify] | **Confirmed** (level) | WP text: "rises from zero in early 2007 to nearly 50 percent at the peak of the crisis in late 2008". The index is an equal-weighted average over **nine non-Treasury classes, including corporates**, and counts 100% haircuts for classes that stopped trading. It is not structured collateral only | https://www.nber.org/papers/w15223 |
| 28 | Ang-Papanikolaou-Westerfield: illiquidity raises state-dependent risk aversion, cuts liquid and illiquid risky holdings; investors forgo ≈2% of wealth to hedge decennial crises | **Confirmed** | Abstract: "increased and state-dependent risk aversion"; "willing to forego 2% of their wealth to hedge against illiquidity crises occurring once every ten years" | https://www.nber.org/papers/w19436 |
| 29 | Temasek total debt ≈5% of NPV (S$25.5bn / S$518bn) at 31 Mar 2026 | **Unverifiable** | NPV S$518bn (MTM, 31 Mar 2026) is confirmed by Temasek Review 2026 materials in search results. The S$25.5bn debt figure could not be checked (all Temasek URLs return 403). The arithmetic (4.9%) is correct | https://www.temasek.com.sg/content/dam/temasek-corporate/our-financials/investor-library/investor-presentation/Temasek%20Investor%20Presentation%202026_EN.pdf |
| 30 | Harvard: US$450m tax-exempt (Mar 2025) + US$750m taxable (Apr 2025), debt ≥US$8.2bn (+32% in two years); US universities issued US$26bn of munis in H1 2025 | **Confirmed** | Crimson (Rai & Sundar); Semafor (26 Aug 2025, Nuveen data: "nearly equal to their total for all of 2024"; six elite schools >10%) | https://www.thecrimson.com/article/2025/4/8/april-2025-bond-sale ; https://www.semafor.com/article/08/26/2025/universities-are-borrowing-more-to-make-up-for-trumps-funding-cuts |
| 31 | Canadian pensions: repo >C$90bn, +14% y/y, ≈half with maturity >1 month (BoC FSR, May 2024) | **Confirmed** (secondary only) | Finadium (13 May 2024) summarizes an IIAC summary of the BoC FSR, and the currency is not stated. Not checked against the BoC primary source | https://finadium.com/?p=140368 |
| 32 | Section 6.9A Kelly/log-growth table (μ=8%, σ=11%; three funding rates) | **Confirmed** (recomputed) | Every cell reproduces: L=2.358 (0.72 Kelly); max g 9.29% and 7.80%. See R2 for the threshold | own recomputation |
| 33 | Section 6.9B Dufresne eventual-ruin table (12 cells) and the executive-summary "≈58% at 7.5%, 15.5% at 5%" | **Confirmed** (recomputed) | Every cell reproduces. A weekly-step Monte Carlo over 150 years gives 58.6% vs the closed-form 57.9%. See R10 for the horizon | own recomputation |
| 34 | Sections 6.8(c) and 6.9C: sell break-evens (2.1/3.8/7.4%; credit 3.4, venture 0.9, tail-end −0.1, RE −2.1) and implied cost of selling | **Confirmed** (recomputed) | All reproduce, e.g. buyout 5.0/8.0/11.1/14.1%; RE 11.3/14.5/17.7/21.0% | own recomputation |

**Counts:** 34 checked; 26 confirmed; 3 corrected; 0 refuted; 5 unverifiable.

---

## 3. Recomputation of the quantitative examples

| Example | Dossier | Recomputed | Verdict |
|---|---|---|---|
| Executive summary 1 / Section 6.9A: L for 10% log-growth at 4.05% | 2.36 (≈0.72 Kelly) | 2.358; 0.72 | OK |
| Max growth at 4.65% / 5.80% | 9.29% / 7.80% | 9.29% / 7.80% | OK |
| "Infeasible once funding ≥4.65%" | threshold implied at 4.65% | **4.28%** for 10% log growth; **4.52%** for 10% annual compounded (ln 1.10 = 9.53% log) | Not tight (R2) |
| Section 6.9B Dufresne (μ 7–10%, σ 12%, D/W₀ 5/7.5/10%) | 29.7/74.3/94.5 … 2.8/26.0/64.2 | identical | OK |
| Section 6.8(c) V_H, V_S, V_L | 1.010; 0.91; 1.0465; 1.141/1.065; 1.105/0.885; τ*≈2.1y | 1.0101; 0.9100; 1.0465; 1.1411/1.0651; 1.1051/0.8851; τ*=2.06y | OK (but see R3: like-for-like τ* = 2.00y for the NAV loan and 5.79y for AA term debt) |
| Section 6.9C implied cost of selling | e.g. buyout 5.0/8.0/11.1/14.1 | identical | OK |
| Section 6.9D regime share; unconditional means | 12.3%; ≈6.5% / ≈8.5% | 12.3%; 6.53% / 8.47% | OK |
| Section 6.9D readings: bp per 1% of NAV borrowed; P05 per 1% | ~3bp/yr; ~0.4pp | 2.9bp/yr (on **medians**); 0.38pp | OK (wording: "expected" should be "median"; R13) |
| Secondaries dry-powder capture | ≈1.7% of NAV per episode, ≈20bp/yr | 1.67%; 21bp/yr at an 8-year cycle | OK |
| Section 6.9E liquidity arithmetic | 8.9–17.7bn; 12–25%; 10.6 vs 26.6; 6.6; 5–14bn | 8.85–17.70; 12.5–25.0%; 10.62 vs 26.55; 6.64; 4.87–13.72 | OK |
| Executive summary 2: US$16bn swing ≈ 9% payout | ≈16bn | 15.93 vs 15.93 | OK |
| Section 2.6 CPPI example | k=4.8; 0.8× | 4.80; 0.800 | OK (but see R4) |
| Peer ratios | CPP 9.7%; OTPP 1.32× / 1.43×; notional 3.1×; Temasek ≈5% | 9.69% (10.73% on NAV); 1.320 / 1.433; 3.13×; 4.92% | OK |
| Section 6.9D Monte Carlo table | (stylized) | Not re-run. The specification leaves out the payout base, debt investment rules, overlay MTM and tail-hedge payoffs, so it cannot be reproduced exactly. Internal checks pass | Not reproducible as specified |

---

## 4. Citation check (key references)

| Reference as cited | Exists | Authors / year / title / venue | How checked | Note |
|---|---|---|---|---|
| Ang, Papanikolaou & Westerfield (2014), *Portfolio Choice with Illiquid Assets*, Mgmt Sci 60(11): 2737–2761; NBER w19436 | Yes | Correct | NBER page | Abstract quotes confirmed |
| Frazzini & Pedersen (2014), *Betting Against Beta*, JFE 111(1): 1–25; NBER w16601 | Yes | Correct | NBER page (abstract); vol/pages from bibliographic knowledge | "prohibited from using leverage" and "must de-lever when they hit their margin constraints" are both in the NBER abstract |
| Asness, Frazzini & Pedersen (2012), *Leverage Aversion and Risk Parity*, FAJ 68(1): 47–59 | Yes | Correct | AQR page (title/authors/journal/year); vol/pages from knowledge | — |
| Brunnermeier & Pedersen (2009), *Market Liquidity and Funding Liquidity*, RFS 22(6): 2201–2238 | Yes | Correct | Bibliographic knowledge (not fetched) | — |
| Gorton & Metrick (2012), *Securitized Banking and the Run on Repo*, JFE 104(3): 425–451; NBER w15223; *Haircuts*, NBER w15273 | Yes | Correct | NBER pages + WP full text | w15273 was published in FRB St. Louis *Review* (Nov 2010), pp. 507–520 |
| Dimmock, Wang & Yang (2024), *The Endowment Model and Modern Portfolio Theory*, Mgmt Sci 70(3): 1554–1579 | Yes | Correct | NBER page | Abstract matches (lock-up plus proportional cost; endogenous boundaries; staggered lock-ups; crisis deviations) |
| Sorensen, Wang & Yang (2014), *Valuing Private Equity*, RFS 27(7): 1977–2021 | Yes | Correct | NBER page | "LPs may just break even" confirmed |
| Brown, Dimmock, Kang & Weisbenner (2014), AER 104(3): 931–962 | Yes | Correct | NBER page | "reduce payouts relative to their stated payout policies following negative, but not positive, shocks" confirmed |
| Grossman & Zhou (1993), *Optimal Investment Strategies for Controlling Drawdowns*, Math Finance 3(3): 241–276 | Yes | Correct | IDEAS/RePEc | — |
| Agarwal, Driscoll & Laibson (2013), *Optimal Mortgage Refinancing: A Closed-Form Solution*, JMCB 45: 591–622 | Yes | Correct | NBER page | Lambert-W confirmed |
| Dufresne (1990), *The distribution of a perpetuity…*, Scand. Actuarial J.: 39–79 | Yes | Correct | Knowledge; formula verified numerically | — |
| Stafford (2022), RFS 35(1): 299–342 | Yes | Correct | Knowledge (not fetched) | — |
| Kelly (1956), BSTJ 35(4): 917–926 | Yes | Correct | Knowledge | **Attribution loose.** The growth formula r_b + ½SR² is the continuous-time (Merton/Thorp) result, not Kelly (1956). The dossier cites it via Wikipedia |
| BoE (2023) LDI minimum-resilience staff paper | Yes | Correct (29 Mar 2023) | Primary page | — |
| FSB (10 Dec 2024) margin preparedness final report | Yes | Correct | Primary page | — |
| ILPA (2024) NAV-facility guidance | Yes | Correct (Jul 2024) | Primary PDF | — |
| Jefferies (Jul 2026); DBRS (Sep 2025); Moody's OTPP (20 Jul 2026); CPP F2025 AR | Yes | Correct | Primary PDFs | — |
| Basel LCR / NSFR | Yes | — | BIS Basel Framework LCR40.82 and NSF30 | Used to test the dossier's [K] haircut and RSF statements (R5) |

**Citation problems (minor):**
- Kelly (1956) is cited for a continuous-time growth formula.
- The Gorton-Metrick index is described as "for structured collateral"; it covers nine non-Treasury classes.
- Harvard Magazine is cited for "capital calls continued", which is not in the source.
- Reuters/Kitco is cited for a 200→89bp "decline", but these are two different metrics, and the Morgan Stanley figure is equity repo, not futures.
- Four items rest only on search excerpts because the primary documents were unreadable: CME, Temasek, AllianceBernstein and Mubadala/Enterprise AM.
- The Mubadala RCF support is a May-2019 announcement (5y/3y facilities), which may be stale.
- DBRS's "adjusted net assets" denominator (NAV + recourse debt) should be adopted explicitly wherever the dossier writes "adjusted NAV".

---

## 5. Reasoning issues and overclaims (ranked by IC impact)

**R1. The peer-leverage anchors are not like-for-like and understate how much leverage peers use (high impact).**
- **What the dossier does.** Executive summary 7 and peer lesson 2 present "recourse debt ≤10% of adjusted NAV" as a peer-derived norm, citing CPP 9.7%, Temasek ≈5% and the Moody's OTPP triggers.
- **Why the comparison fails.** The three numbers measure different things:
  - CPP 9.7% is DBRS's *debt-only* ratio. It excludes C$113.3bn of repo, and its denominator is NAV + debt.
  - CPP's own Board-governed **recourse leverage** (debt + repo + net notional of leverage-generating derivatives) is **36% of net assets** for base CPP. That figure doubled from 18% in F2021, and the **Board limit is 45%** (CPP F2025 AR p.44).
  - OTPP's 17% is Moody's *adjusted* leverage, which includes repo and term debt with some netting.
  - Temasek's ≈5% is total debt / NPV, and the debt figure is unverified.
  - On a debt-plus-repo basis, CPP is about 21% of (NAV + debt + repo).
- **Knock-on effect on the exposure cap.** The proposed 1.30× gross-exposure cap, described as "from peers", sits **below** CPP (≈1.36× on its own measure) and OTPP 2024 (1.43×). It matches only OTPP 2025 (1.32×).
- **Fix.** Publish one harmonized peer table with three columns: debt-only, debt + repo, and economic exposure. Then present ADIC's 10% and 1.30× limits as *deliberately below peers*, justified by mandated outflows and 60% illiquids. The IC should not be told peers run ≤10%.

**R2. The executive summary overclaims that levering "cannot" reach 10% (high impact).**
- The dossier's own table shows that 10% log growth is reachable at L≈2.36 with 4.05% funding, i.e. 0.72 of full Kelly. The accurate claim is "only at imprudent leverage, and only with sub-≈4.3% funding that cannot finance the illiquid 60%".
- The true infeasibility threshold is **≈4.28%** for 10% log growth, or ≈4.52% if the target is a 10% annual compounded return (9.53% log). It is not "≥4.65%".
- Using 10% *log* growth (10.5% compounded) as the target overstates the hurdle.
- The conclusion is highly sensitive to the illustrative μ=8% / σ=11%. It also assumes the illiquid sleeve can be levered and continuously rebalanced, and that σ is not understated by appraisal smoothing.

**R3. The HOLD/SELL/LEVER valuation (Section 6.8(c), executive summary 4) is not normalized like-for-like (medium).**
- **The normalization gap.** V_L adds λ for $1 raised per $1 of NAV, which implies 100% LTV. V_S raises only (1−d) per $1 of NAV.
- **The correct comparison.** Per dollar of liquidity raised, λ cancels. SELL beats LEVER if and only if e^{α*T}/(1−d) − 1 < (c − r_f)τ + covenant/encumbrance cost.
  - λ governs *whether* to raise liquidity versus HOLD, not *which* source to use. The statement that the choice is "priced with λ" is therefore wrong for SELL vs LEVER.
  - The break-evens barely move: NAV loan 2.06y → 2.00y; AA term debt 5.98y → 5.79y. The numerical conclusions survive.
- **Encumbrance is ignored.** At the cited NAV-loan LTVs of 5–30%, each $1 raised pledges **$3.3–20 of NAV**, against $1.10 of NAV sold.
- **Carry mismatch.** Pairing 10y AA term debt with τ = 1 ignores the negative carry over the remaining life unless the bonds are repurchased, which brings mark-to-market (MTM) risk.

**R4. The drawdown barrier (Section 2.6, constraint 10) becomes infeasible or forces a net-short overlay in moderate drawdowns (medium).**
- With α = 0.75 and k = 4.8, the allowed total exposure equals the illiquid share (0.6×) at a **≈14.3% drawdown**.
- If losses fall on the liquid book, the illiquid share of E rises (the denominator effect). At a 15% drawdown, liquid + overlay must then be **net short (−0.14×)**.
- Smoothed private marks lag, so the barrier will trigger late and then hard. That is the procyclical whipsaw the dossier warns about.
- **Fix.** Add feasibility checks, use a lower α (or a barrier defined on the liquid-sleeve or overlay risk budget), and compute E on desmoothed values.

**R5. The LCR and NSFR analogs (constraints 1 and 3) are inconsistent with Basel and with the dossier's own warnings (medium).**
- **(a) LCR numerator.** It counts "committed undrawn lines surviving stress". Basel LCR40.82 gives facilities held at other institutions a **0% inflow**. Given the dossier's wrong-way-risk point (dealers retrench in stress), the hard constraint should exclude them. They could be credited only in a soft target, with a haircut.
- **(b) NSFR analog.** It omits off-balance-sheet **unfunded commitments**, ADIC's largest contingent outflow (≈US$26.6bn assumed). Basel NSF30.34 charges 5% RSF even on undrawn committed facilities, and LP commitments are drawn with near certainty, so ADIC should use a higher factor. The analog also omits the next-12-month payout as a claim on available stable funding.
- **(c) RSF factors.** "0–5% for HQLA, 50% for listed equities" is wrong. The correct factors are:

  | Asset category | RSF factor | Basel paragraph |
  |---|---|---|
  | Level 1 HQLA | 0–5% | — |
  | Level 2A | 15% | NSF30.28 |
  | Level 2B, including eligible equities | 50% | NSF30.29 |
  | Non-HQLA exchange-traded equities | 85% | NSF30.31 |
  | Non-traded equities and assets encumbered ≥1y | 100% | — |

**R6. The Tier 2 objective may double count costs (Section 6.7) (medium).**
- If the objective is P(10%) or E[log E_H] computed from simulated wealth paths that already deduct financing costs and fire-sale losses, subtracting them again as "net of" terms double counts.
- Only unmodeled items should be added as penalties: rating migration, covenant-cure frictions and shadow liquidity penalties.

**R7. The cost-curve specification is inconsistent (Section 6.5) (low-medium).**
- It is described as "convex piecewise-linear" but written as quadratic in utilization.
- Total cost c_k(B)·B is then **cubic**, so the inner problem is not the "LP/QP" claimed in Section 3. It is still convex: use a power-cone/SOCP formulation, or piecewise-linearize.

**R8. The equity identity is ambiguous (Section 6.4) (low-medium).**
- E_t subtracts only *recourse* asset-level debt.
- If P_i is gross of asset-level debt, non-recourse debt must also be deducted, with a limited-liability floor max(P_i − D_i^{nr}, 0) per ring-fenced asset. If P_i is net, the recourse D_i is double counted.
- **Fix.** Specify which convention applies.

**R9. The "Moody's downgrade analog" is mis-mapped (low-medium).**
- The Monte Carlo tracks P(debt/E > 25%). Moody's adjusted leverage nets repo and derivatives, and the report does not state its denominator. OTPP's figures are consistent with a gross-assets base: liabilities of C$75bn on C$354bn gross assets give 21% before netting.
- If Moody's uses assets, debt/E 25% corresponds to debt/assets 20%, so the analog is about a third more conservative than stated.
- **Fix.** Pin the definition and compute every agency variant, as Section 2.1 already recommends.

**R10. The ≈58% ruin figure needs its horizon stated (executive summary 6, Section 6.9B) (low-medium).**
- 58% is the *infinite-horizon* probability. In the same model, ruin within 5y is ≈0%, within 10y ≈0.2%, within 20y ≈20%, within 30y ≈40% and within 50y ≈54% (40k-path Monte Carlo).
- The qualitative point stands: fixed claims create an absorbing barrier. But an IC working on a 5-year horizon could misread the headline number.

**R11. The BoE 250bp buffer is transplanted without recalibration (constraint 12, Section 6.5) (low-medium).**
- 250bp (170 + 80) is calibrated to five-day moves in **30y UK index-linked gilts** and to LDI-fund collateral timelines.
- Applying it to "any rates overlay" in a USD book needs instrument- and tenor-specific 1-in-100 / 99.8th-percentile five-day shocks, and ADIC's own collateral-mobility timelines.

**R12. The equity-financing metrics are conflated (executive summary 3, Sections 4.2 and 6.5) (low).**
- The ~200bp (equity repo over fed funds) is listed under "equity-index futures".
- The 89bp is a different, quarterly-maturity metric.
- The stress spread for "Equity futures / TRS" (+150–200bp) therefore mixes instruments and benchmarks (fed funds vs SOFR).
- **Fix.** Calibrate futures stress from the CME and D. E. Shaw series, and TRS or equity-repo stress separately.

**R13. Wording and specification nits (low).**
- Executive summary 5 says leverage "adds ~30bp/yr in *expected* terms", but the table shows **medians**.
- Reading 1 says "a reserve *or the payout band* nearly eliminates forced sales". The payout band alone only cuts P(forced sale) from 6.4% to 2.7%, and its cost falls on the owner (cumulative payout −1.2pp of E₀), which a bp/yr figure does not capture.
- Constraint 9's Kelly cap needs max(0, ·).
- Constraint 5's "gross exposure" must be delta-adjusted and net of hedges, or it will penalize the tail hedge.
- "The market can absorb ADIC-sized sales" extrapolates from 15 deals >US$1bn to ADIC tranches of US$5–10bn in stress.
- Treating "lost" distributions as lost cash conflates deferral with loss. Applying the market-wide Jefferies distribution yield to ADIC's book should be replaced with ADIC's own fund-level cash-flow data.

**R14. NAV-loan pricing source mismatch (low).**
- Rede's 4–7% margins come from a survey of GP-side NAV financing, but they are applied to an "LP-level NAV facility" in Section 6.5.
- LP-level portfolio financing for a sovereign LP may price differently. Calibrate it from actual quotes.

---

## 6. Residual unverified items (do not present to the IC as fact until closed)

- Temasek total debt of S$25.5bn (≈5% of NPV).
- PIF May-2026 spreads (T+95–99).
- Mubadala 10y at T+55 (Oct 2025).
- AllianceBernstein NAV-loan LTV of 5–30% and OID of 1–3%.
- CME "+38bp in Q2 2025".
- The Canadian pension repo figures, which have been checked against secondary sources only.
- The stylized Section 6.9D Monte Carlo, which is not reproducible from its stated specification. Publish the code and a parameter table before IC use.

## 7. Overall reliability rating

**HIGH** for empirical content, arithmetic and citations. Every high-confidence [S] claim matched its primary source, all quantitative examples reproduce, and no fabricated references were found.

**MEDIUM** for the design implications. R1 (peer-leverage comparability) and R2 (the "cannot reach 10%" overclaim) would mislead an IC if left as written. R3–R6 are specification errors that would propagate into the optimizer.

**Recommended status:** usable as a research input after the author fixes R1–R6 and relabels the five unverifiable items.
