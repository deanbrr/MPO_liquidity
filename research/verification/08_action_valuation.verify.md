# Verification log: Dossier 08, action valuation (SELL / HOLD / REFINANCE / LEVER)

| Item | Detail |
|---|---|
| Dossier checked | `research/dossiers/08_action_valuation.md` (as of 2026-10-18); not edited |
| Verification date | 2026-10-18 |
| Verifier stance | Adversarial; a claim counts as unverifiable unless a source supports it |

**How it was checked**
- **Primary sources, read directly.**
  - PDFs, with text extracted locally: Jefferies (Jul-2026), Rede NAV Reports 2026 and 2025, Proskauer FY2025.
  - Data and legal text: FRED, BIS (Basel Framework LCR40, FSI OP 10, BCBS 144), EUR-Lex (Directive (EU) 2025/2).
  - Abstracts from NBER, RePEc, AEA and arXiv, plus the case-study articles.
- **Reproducibility.** A copy of `08_action_valuation_examples.py` was re-run and its output compared with the committed results JSON.
- **Sensitivity checks.** Run by importing the author's own functions (scripts kept in the session scratchpad).
- **Search limit.** The shared WebSearch budget ran out mid-session. After that, only direct fetches of known URLs were used, so some secondary references were not re-fetched (see §7).

---

## 1. Summary

**Verdicts:** 33 claims checked; **29 confirmed**, **3 corrected** (all minor), **0 refuted**, **1 unverifiable** (the author had already flagged it).

**Facts and citations are sound.**
- Every [S] market statistic in the author's flagged list traces to the cited source with the stated value. This covers:
  - Jefferies H1-2026 (more than 25 figures);
  - Rede 2026 and 2025, Proskauer FY2025, Bain 2025 and 2026;
  - FRED SOFR, Basel LCR40.64 and LCR40.1, FSI OP 10;
  - Directive (EU) 2025/2 Art. 77(6);
  - the Harvard and Yale case studies.
- Two items looked suspicious and turned out to be correct when the full PDFs were read:
  - the "+140 bp 2022 widening" (Rede 2025, p. 6);
  - the ILPA consent points (Rede 2025, ILPA box).
- **No hallucinated or garbled citations.** All 16 references checked exist, with correct authors, year, title, venue, volume and pages.
- The worked-example script reproduces its results JSON byte for byte. Every number quoted in §§1 and 6.11–6.13 matches it.

**The weaknesses are analytical and touch IC-facing numbers.** Details are in §4.
- **R1 (High).** Example 1's headline is a plug-in value at the mean IRR: "SELL beats HOLD+REFI by $10.75m; cash reservation price 85.9%".
  - Under the dossier's own predictive distribution (same seed), E[HOLD+REFI] is $431.2m, not $423.7m.
  - So the expected SELL advantage is **$3.3m**, not $10.75m, and the reservation price is **87.3%**, not 85.9%.
- **R2 (High).** The production engine's "one currency" claim is not established. The here-and-now LP's objective is never specified.
  - With a linear objective, the cash-balance duals π carry no market-risk premium.
  - Example 1 would then flip to KEEP by about **$72m**.
- **R3 (Medium).** The formula for ℓ and the Score omit constraint rows that contain cash, HQLA (high-quality liquid assets) or unfunded commitments. These include the IG + cash floor and the stressed-call term in the survival row.
- **R4 (Medium).** Example 2's "LEVER is optimal" rests on SOFR+250 financing, below the dossier's own calibration. At Rede's 4.8% secured average, LEVER is never optimal at any flat ℓ. The Rede margins also describe GP fund-level loans, which Rede's scope excludes from "secondary portfolios" lending, not LP-level borrowing.

**Overall reliability:** sourcing **high**; analysis **medium**; **overall medium** until R1–R4 are fixed.

---

## 2. Claims table

Page references are to the cited document's own page numbers.

| # | Claim (abridged from dossier) | Verdict | Corrected value / verifier note | Source URL |
|---|---|---|---|---|
| 1 | Average LP portfolio pricing was 87% of NAV in H1-2026. By strategy: buyout 91%, infrastructure 91%, credit 89% (from 91%), venture 79%, real estate 68%. | Confirmed | Exact (pp. 2, 5). Venture rose 100 bp to 79%. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 2 | Tail-end (10+ yr) funds priced at 25%+ discounts and recent vintages at single-digit discounts. Weighted-average vintage sold was 2018; nearly 50% of funds sold were in years 4–8. | Confirmed | Exact (p. 6). "Recent" means less than five years old. The 2018 average was unchanged from 2025. | (Jefferies, as #1) |
| 3 | About 33% of LP sales were structured; deferrals appeared in 26%; pref equity, managed funds and CFOs (collateralised fund obligations) were 7%. | Confirmed | Exact (p. 6). | (Jefferies) |
| 4 | Record $118bn volume: LP-led $56bn (47%), GP-led $62bn (53%). Dedicated capital $290bn (from $327bn). Pensions and SWFs 48% of LP volume. 45% of LP sellers cite liquidity. | Confirmed | Exact (Jefferies pp. 2–4, 12). The author's flagged source, Abbott Capital, corroborates every figure **except** the 45%, which is not on the Abbott page. | (Jefferies); https://www.abbottcapital.com/h1-2026-private-equity-market-overview/ |
| 5 | FY2026E about $260bn vs FY2025 record $240bn. Capital overhang 1.2x. LP supply: FoF/secondaries 27%, E&F 16%. Seller motives: 26% wind-down, 16% rebalancing, 13% non-core. Average LP rollover 14%. CVs about 14% of sponsor-backed exits. NA/Europe priced at 86–88%; Asia/EM at 35%+ discounts. | Confirmed | Exact (pp. 3, 4, 6, 9, 12). | (Jefferies) |
| 6 | LP distribution yield about 10% in H1-2026; below 20% since early 2023; 25% average since 2001. | Confirmed | Exact (p. 3): "since the beginning of 2023". | (Jefferies) |
| 7 | Jefferies statements: disclaimer that aggregate pricing data "is not appropriate for the valuation of individual fund interests"; strip sales "to crystallize gains"; "reducing demand for unfunded capital"; software exposure discounted. | Confirmed | All present (pp. 2, 3, 6, 9, 13). The unfunded-capital quote comes from the **GP-led buyout (CV buy-and-build)** section, not from LP secondaries (see R11). | (Jefferies) |
| 8 | "Buyers ... use recent vintages as 'sweeteners'". "Funds in years 4–8 are the market's 'sweet spot': buyout pricing averaged 91%". | **Corrected** | Recent vintages "were often used as sweeteners in diversified portfolios to increase aggregate pricing". That is a seller or portfolio-construction tactic, not something buyers do. "Sweet spot" refers to activity concentration (nearly 50% of funds sold were in years 4–8). The 91% is the **all-ages buyout average**; Jefferies gives no price for years 4–8. | (Jefferies p. 6) |
| 9 | PE distributions about 14% of NAV in 2025, the fourth straight year below 15%. Bain 2025: 2014–17 average 29% vs 11% annualised through Q3-2024. | Confirmed | Exact. Bain's series is (global) **buyout** distributions as % of NAV; the dossier labels it "PE". | https://www.bain.com/insights/outlook-gaining-traction-global-private-equity-report-2026/ ; https://www.bain.com/insights/outlook-is-a-recovery-starting-to-take-shape-global-private-equity-report-2025/ |
| 10 | Bain 2026: about 32,000 unsold companies worth $3.8tn; about 40% held more than 5 years; average hold about 7 years; 53% of LPs limited by undrawn commitments. | Confirmed | Exact. The 53% comes from a PEI survey cited by Bain, up 15 pp vs YE2024. | (Bain 2026) |
| 11 | Rede 2026: weighted-average target margins 4.8% secured (from 5.2%) and 6.1% recourse-light (from 6.6%). Conventional PE NAV facilities "rarely exceed 20% LTV" and are seldom below 5%. | Confirmed | Exact (pp. 2–3). Rede's wording is "not less than 5% LTV" *unless the capital is needed for a specific use case*. Rede's scope **excludes facilities to FoF or secondary portfolios** (see R4). | https://www.rede-partners.com/s/NAV-Financing-Market-Report-2026_FINAL.pdf |
| 12 | Banks price secured deals at about 3.0% and alternative lenders at about 5.6%. 36% of lenders expect spreads to rise vs 17% to fall. | Confirmed | Exact (pp. 4, 13–14). Bank recourse-light is 4.2%. | (Rede 2026) |
| 13 | Stress add-on: +140 bp, "the 2022 widening" [Rede 2025]. | Confirmed | Rede 2025 PDF p. 6: "lenders reported a 140bps widening of spreads in 2022, that was reversed in 2023". The landing page lacks this, and 140 bp is also, by coincidence, the 2024 gap between secured and recourse-light margins. | https://www.rede-partners.com/s/Rede-NAV-report-2025_FINAL.pdf |
| 14 | ILPA July-2024 guidance, as summarised by Rede 2025: LPAC consent if the LPA is silent; LPAC consent if proceeds fund distributions; standardised disclosure. | Confirmed | All three appear in Rede 2025's ILPA box. | (Rede 2025) |
| 15 | Proskauer FY2025: upfront fees mostly 1–2% (modal 1–1.5%); primary spreads mostly below 5% over 3M Term SOFR; closing LTV mostly below 25%; 5-year maturities common but WAL shorter; 63% use LTV-based sweeps. Secondaries-fund facilities: ≤3% (67%) or 3–4% (33%); closing LTV 25–50% (57%) or 50–75% (43%). | Confirmed | Exact (pp. 8–13). Only 55% of primary spreads are below 5%. **23% of primary facilities close below 5% LTV and 9% at 25% or more**, which conflicts with the dossier's "LTV 5–20%" calibration band (§6.9). | https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025 |
| 16 | SOFR was 3.89% on 15-Oct-2026 (3.88% on 14-Oct). | Confirmed | FRED: 2026-10-15 = 3.89; 2026-10-14 = 3.88. | https://fred.stlouisfed.org/series/SOFR |
| 17 | Average high bid for PE fund interests fell to 61% of NAV in the five months through Nov-2008 (Cogent, via PERE). | Confirmed | Exact. The "first-round bids" qualifier in the author's flag list is **not in the cited article**. The article attributes the fall partly to "stale holding values". | https://www.pei-privaterealestate.com/equity/study-secondaries-pricing-falls-28/ |
| 18 | Nadauld et al.: buyers' PME 1.023 vs sellers' 0.974, about 5 pp a year; about 3 pp for funds aged 4–9; discounts relate to asymmetric information and market depth. | Confirmed | Exact (abstract). | https://www.nber.org/papers/w22404 |
| 19 | Ang, Papanikolaou & Westerfield: investors would forgo 2% of wealth to hedge decennial illiquidity crises; uncertain duration "drives most" of the cost of illiquidity. | **Corrected** | The 2% figure is exact. The abstract says uncertainty about the illiquidity interval "is **a primary determinant** of the cost of illiquidity". It does not say it is "most" of the cost. | https://ideas.repec.org/a/inm/ormnsc/v60y2014i11p2737-2761.html |
| 20 | Sorensen, Wang & Yang: "LPs may just break even, net of management fees, carry, risk, and costs of illiquidity". Costs split about 50% illiquidity, 25% fees, 25% carry. | Confirmed | The quote is verbatim from the NBER/RFS abstract. The split is from the HLS Forum summary, qualified there as "Broadly speaking". | https://www.nber.org/papers/w19612 ; https://corpgov.law.harvard.edu/2014/01/12/valuing-private-equity/ |
| 21 | Robinson & Sensoy: calls and distributions are procyclical; distributions more so, so net flows are procyclical; funds calling capital in bad times perform better; sample 1984–2010. | Confirmed | Exact. 837 buyout and VC funds. | https://ideas.repec.org/a/eee/jfinec/v122y2016i3p521-543.html |
| 22 | Basel LCR40.64 drawdowns on undrawn committed facilities: retail 5%; NFC 10% credit / 30% liquidity; banks 40%; other FIs 40% / 100%; SPVs 100%. Inflow cap of 75% (LCR40.1). | Confirmed | LCR40.64(1)–(7) and LCR40.1 match. The NFC row also covers sovereigns, central banks, PSEs and MDBs. | https://www.bis.org/committees/bcbs/basel-framework/standard/lcr/40/inforce/2019-12-15/published/2023-03-30 |
| 23 | FSI OP 10: survey of 38 banks; marginal funding costs matched to product maturity at origination; charge expected contingent-liquidity usage; avoid "one average rate". | Confirmed | "38 large banks from nine countries"; published 30-Dec-2011. The landing page names no author, as the dossier says. | https://www.bis.org/fsi/fsipapers10.htm |
| 24 | BCBS (2008): "allocating liquidity costs, benefits and risks to all significant business activities". | Confirmed | The phrase appears on the bcbs144 summary page (25-Sep-2008). | https://www.bis.org/publ/bcbs144.htm |
| 25 | Udell & Boyd: suboptimality is "bounded by a term proportional to the maximal number of active constraints" and does not depend on the number of variables. | Confirmed | Exact (arXiv abstract, v2 9-Jan-2016). The bound also scales with each term's non-convexity (see R10). | https://arxiv.org/abs/1410.4158 |
| 26 | Directive (EU) 2025/2 cuts the Solvency II risk-margin cost-of-capital (CoC) rate from 6% to 4.75%, applying from 30-Jan-2027. | Confirmed | Primary text, new Art. 77(6): "The Cost-of-Capital rate ... shall be assumed to be equal to 4,75 % as of 30 January 2027". Directive dated 27-Nov-2024 (OJ 8-Jan-2025). William Fry confirms transposition by 29-Jan-2027. | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025L0002 ; https://www.williamfry.com/knowledge/solvency-ii-reform-key-changes/ |
| 27 | Harvard: about $1bn of PE stakes to Lexington in 2025, about 5% of its PE book, Jefferies advising, PE about 40% of a $53bn endowment. Yale: up to about $2.5bn of PE/VC at a discount under 10% (Evercore advising), later "nearly $3bn". | Confirmed | Crimson (Apr-2025): "planning", nearly 5%, Lexington, Jefferies. Fortune (15-Jun-2025): "recently agreed to sell". PE Wire (5-Jun-2025) covers Yale only and does **not** mention Harvard. The dossier's §5 table says "Sold" for 2025 and 2017, but the cited sources say "planning" or "agreed" (2025) and "nearing the final stage in talks" (2017). | https://www.thecrimson.com/article/2025/4/25/private-equity-stake-sales/ ; https://www.fortune.com/2025/06/15/harvard-yale-private-equity-holdings-sale-net-asset-value-discounts-nav-squeezing ; https://www.privateequitywire.co.uk/yale-nears-2-5bn-secondary-sale-of-pe-and-vc-stakes/ |
| 28 | HMC 2008 "shedded $1 billion in private equity at a loss". Fortune's "NAV squeezing": buyers mark stakes up to the prior NAV. Yale spokesperson: still committed to PE. | Confirmed | All three quotes verified. | https://www.thecrimson.com/article/2017/7/2/HMC-selling-private-equity ; (Fortune) ; https://www.institutionalinvestor.com/article/2eplivly10nvujo3sqzuo/corner-office/yales-potential-pe-sale-wont-solve-liquidity-challenges |
| 29 | Yale's unfunded PE commitments were $6.51bn at FY23, on a $41.4bn endowment. | **Corrected** | $6.51bn is the FY23 figure. $41.4bn is the endowment current when the Apr-2025 article was written, i.e. FY24. Pair like-dated figures; the FY23 endowment was about $40.7bn (verifier's memory, not re-verified). | (Institutional Investor, as #28) |
| 30 | "Press reports describe it as Yale's first secondary sale." | Unverifiable | Not stated in PE Wire, Fortune or Institutional Investor. The author already flags it. | — |
| 31 | Cariño et al. (1994): the Russell–Yasuda Kasai model added 42 bp, ¥8.7bn (US$79m), in its first two years. | Confirmed | Abstract: fiscal 1991 and 1992. | https://ideas.repec.org/a/inm/orinte/v24y1994i1p29-49.html |
| 32 | McDonald & Siegel (1986): it can pay to wait until benefits are about twice the cost. | Confirmed | "may be optimal to wait until benefits are twice the investment cost". | https://www.nber.org/papers/w1019 |
| 33 | Longstaff (2001): bounded-variation trading makes investors act as if they face borrowing and short-sale constraints. Longstaff (2009): "Agents abandon diversification and choose polarized portfolios instead"; liquidity can be a large part of price. | Confirmed | Both abstracts match. | https://ideas.repec.org/a/oup/rfinst/v14y2001i2p407-31.html ; https://www.aeaweb.org/articles?id=10.1257/aer.99.4.1119 |

---

## 3. Citation check (existence and bibliographic accuracy)

All 16 references checked exist and are correctly specified.

| Reference as cited in the dossier | Status | Note |
|---|---|---|
| Nadauld, Sensoy, Vorkink & Weisbach (2019), *JFE*, DOI 10.1016/j.jfineco.2018.11.007 | Correct | The full citation is **132(3): 158–181**, which the dossier omits. |
| Ang, Papanikolaou & Westerfield (2014), *Mgmt Sci* 60(11): 2737–2761 | Correct | DOI 10.1287/mnsc.2014.1986. |
| Sorensen, Wang & Yang (2014), *RFS* 27(7): 1977–2021 | Correct | — |
| Dimmock, Wang & Yang (2024), *Mgmt Sci* 70(3): 1554–1579 | Correct | Summary of findings (staggered lock-ups, endogenous boundaries, crisis deviations) matches. |
| Robinson & Sensoy (2016), *JFE* 122(3): 521–543 | Correct | — |
| Udell & Boyd, arXiv:1410.4158 (v2, Jan-2016) | Correct | The arXiv page lists no journal reference. The verifier believes a journal version exists (*Comput. Optim. Appl.*, 2016) but could not confirm it this session. |
| Everett (1963), *Oper. Res.* 11(3): 399–417 | Correct | The "fail-safe" and "independent activities" wording matches the abstract. |
| Bolton, Chen & Wang (2011), *JF* 66(5): 1545–1578 | Correct | The double-barrier characterisation matches the NBER w14845 abstract. |
| Adelman & Mersereau (2008), *Oper. Res.* 56(3): 712–727 | Correct | Lagrangian vs approximate-LP relaxations, as described. |
| Gupta & Van Nieuwerburgh (2021), *JF* 76(6): 3255–3307 | Correct | — |
| Longstaff (2001), *RFS* 14(2): 407–431; Longstaff (2009), *AER* 99(4): 1119–1144 | Correct | — |
| McDonald & Siegel (1986), *QJE* 101(4): 707–727 | Correct | — |
| Cariño et al. (1994), *Interfaces* 24(1): 29–49 | Correct | Eight authors, including Ziemba. |
| Faulkender & Wang (2006), *JF* 61(4); Brunnermeier & Pedersen (2009), *RFS* 22(6); Lerner, Schoar & Wongsunwai (2007), *JF* 62(2); Shleifer & Vishny (2011), *JEP* 25(1) | Correct | Quoted phrases verified: "declines with larger cash holdings, higher leverage"; "mutually reinforcing"; endowments better at predicting follow-on performance; "forced sale of an asset at a dislocated price". |
| FSI OP 10 (2011); BCBS 144 (2008); Directive (EU) 2025/2 | Correct | — |

**Citation and attribution problems**
1. The Abbott Capital URL (flagged claim #4) does not carry the "45% of LP sellers cite liquidity" figure. That figure is in Jefferies, p. 4; the dossier body attributes it correctly.
2. The PE Wire URL (flagged claim #19) covers Yale only. The Harvard figures come from the Crimson (25-Apr-2025) and Fortune (15-Jun-2025).
3. Cogent via PERE: the author's flag adds "first-round bids", which the article does not say. The article attributes the decline partly to stale NAVs.
4. Bain distribution rates are **buyout** distributions as % of NAV, not "PE".
5. The §5 Harvard table says "Sold" (2017, 2025), where the cited articles say "nearing final stage", "planning" or "agreed".
6. The Rede and Proskauer pair is in tension on LTV. Rede says conventional facilities are at least 5% LTV, while Proskauer reports 23% of primary facilities closing below 5%. The dossier's "5–20%" band (§6.9) should cite both and widen.
7. Not re-fetched this session, because the search budget was exhausted: Whittle (1988), Takahashi & Alexander (2002), Howard (1966) and Korteweg & Nagel (2016), all marked † by the author; and Kahl, Liu & Longstaff (2003), Holmström & Tirole (1998), Acharya & Pedersen (2005), Brennan & Schwartz (1985), Andersen & Broadie (2004), Brown, Smith & Sun (2010), Longstaff & Schwartz (2001), Kouwenberg (2001), Arkes & Blumer (1985), Shefrin & Statman (1985), Tversky & Kahneman (1974). Their metadata matches the verifier's knowledge, and no claim in the dossier depends on numbers taken from them.

---

## 4. Reasoning issues and overclaims

### R1 (High): Example 1's headline uses a plug-in point estimate, not the expected value under the dossier's own beliefs
**The problem**
- The verdict ("SELL beats HOLD+REFI by **$10.75m**, 2.2% of NAV"), the reservation price (85.9%) and the flip thresholds (ℓ\* 7.4%, IRR\* 11.75%) are all computed at the mean forward IRR of 11%.
- LAPV is convex in the growth rate g, because NAV and distributions compound over six years. So E[LAPV] is greater than LAPV(E[g]).

**Evidence**
- The author's own Monte Carlo (seed 20261018, N(11%, 6%)) gives these values:

  | Quantity | Value |
  |---|---|
  | E[HOLD] | $428.9m (point $421.4m; P50 $420.9m) |
  | E[HOLD+REFI] | $431.2m |
  | E[SELL − KEEP] | **$3.3m**, which also equals E-regret(KEEP) 36.16 − E-regret(SELL) 32.88 in the results JSON |
  | Expected-value reservation price | **87.3%** |

- Bids between about 85.9% and 87.3% would be wrongly classed as SELL.
- The IC would see a "2.2% of NAV" margin next to a 45% probability that keeping is better. Those two numbers come from different expectations.

**Fix**
- Compute the Score, p\* and every flip threshold on E[LAPV] under the fused predictive distribution.
- Alternatively, define "fused forward IRR" as the IRR of *expected* cash flows. Centring g at about 10.5% makes E[HOLD] equal the 11% point value.

### R2 (High): "One currency" between the r_h shortcut and the scenario-dual engine is asserted, not established
**The problem**
- The here-and-now LP's **objective is never specified** (§2.3, §6.4).
- With a linear objective, such as expected terminal wealth, the cash-balance duals π are physical probabilities compounded at r_f + ℓ. They contain **no market-risk premium**.
- Risky distributions would then be discounted at r_f + ℓ, not r_h + ℓ. Market risk would enter only through λ_R·ΔCVaR, and only when the CVaR row binds.

**Evidence**
- In Example 1, discounting risky flows at r_f + ℓ raises HOLD from $421.4m to **$506.5m**. The verdict flips to KEEP by **$72m**.

**Consequences**
- Pitfall 5 says "r_h already prices market risk", which holds only in the shortcut.
- In the engine, a slack risk row (λ_R = 0) means **no** market-risk pricing at all.
- In the shortcut, a binding CVaR row prices systematic risk **twice**: once through r_h and once through λ_R.

**Fix**
- Specify the objective. Either use concave utility, so that π is proportional to marginal utility, or multiply π by a calibrated SDF; the dossier's Method 8 (strips / GPME) could supply it.
- Add a reconciliation test: on a degenerate one-scenario case, Method 4 must reproduce Method 3.

### R3 (Medium): ℓ and the Score omit constraint rows that contain cash, HQLA or unfunded commitments
**The ℓ formula**
- Cash enters the IG + cash ≥ 8% NAV row (dual φ) as well as the survival row.
- Stationarity on cash therefore gives π_t = (1+r_f)Σπ_{t+1} + μ_t + 0.92φ_t, plus any other row in which cash or NAV appears. Hence ℓ = (μ + 0.92φ + …)/(π − μ − 0.92φ − …).
- The dossier's ℓ = μ/(π − μ) understates ℓ exactly when the IG + cash floor binds. It reports ℓ = 0 if only that floor binds.

**The Score**
- The Score prices cash at π, and CVaR, leverage and floors at λ and ρ.
- It omits the direct survival-row and IG-row terms for **ΔHQLA** and **ΔU**. ΔU is the change in unfunded commitments, which drives the stressed 12-month calls on the right-hand side of the survival row. The ActionBundle defines both terms.
- So SELL's contingent-call relief beyond expected calls is unpriced, even though §2.3 calls it a key contingent-liquidity charge.

**Fix:** compute the Score as the full LP reduced cost, Σ over rows of dual × column coefficient, rather than a hand-picked subset of terms.

### R4 (Medium): REFI and LEVER financing calibration is inconsistent with the cited market data
**(a) Product mismatch.**
- Rede's 4.8% and 6.1% margins are for **GP fund-level** NAV facilities backed by direct portfolio equity. Rede explicitly excludes "Fund of Funds or secondary portfolios".
- ADIC's REFI is an **LP-level** loan against LP interests. That is a different product, usually needing GP consent to pledge.
- Using these margins for MCL step 6 and Example 1 (SOFR+600 at 15% LTV) is an analogue at best, and the dossier should say so.

**(b) Example 2's LEVER result depends on cheap financing.** The example uses SOFR+250 at 23% LTV (LEVER) and 30% LTV (REFI). That is below the dossier's own defaults: single-fund NAV loan 4.8–6.1%, diversified SPV about SOFR+300–400. The 30% LTV is also above Rede's "rarely exceed 20%". Re-running the author's code:

| Financing spread | Best action at ℓ = 4% | Flat-ℓ range where LEVER is optimal |
|---|---|---|
| SOFR+250 | LEVER | 3.0–4.25% |
| SOFR+300 (bank secured) | LEVER | 3.5–4.25% |
| SOFR+480 (Rede secured average) | ADD | **never** |
| SOFR+560 (alternative lender secured) | ADD | **never** |

The IC message should state that LEVER requires financing at roughly 3% or below.

**(c) The identity holds by construction.** The script charges the same 6.39% rate at 30% LTV (REFI) and 23% LTV (LEVER). LEVER ≡ ADD + REFI therefore holds because the code sets `lever = add + refi`, not because it was demonstrated.

**(d) MCL step 5 overstates the Proskauer data.** The dossier says "SOFR+300–400"; Proskauer reports 67% of secondaries facilities at ≤3% and 33% at 3–4%.

### R5 (Low–Medium): The Nadauld comparison and calibration target 5 use the wrong benchmark
**The problem**
- The "5.7% implied liquidity spread" is measured over r_h. It therefore includes the forgone α\*, about 1.8% (11% vs 8.99%).
- The figure comparable to Nadauld's buyer-minus-seller gap is the sale IRR over the fund's own expected IRR: 15.24% vs 11%, i.e. **3.8%**.
- A 2018 fund is about 8 years old, so it falls in Nadauld's 4–9-year bucket (about 3 pp), not the 5 pp average.
- The conclusion (rough consistency) survives with the right comparison. Calibration target 5 must use the spread over the fund's own IRR, not over r_h.

**Also:** §2.4 says the implied spread is found by "subtracting" the base rate, but the code divides: (1+IRR)/(1+r_h) − 1 gives 5.74%, while subtraction gives 6.25%. State the convention.

### R6 (Low–Medium): The Basel LCR40.64 rates are a 30-day bank metric used as a 12-month PE call prior
- LCR40.64 gives 30-day stress outflow assumptions for facilities that banks extend to counterparties.
- Using them as the prior for ADIC's *12-month* stressed net calls mixes horizons and counterparty economics. PE calls are less cyclical than distributions (Robinson & Sensoy).
- Labelling the 40–100% range "conservative" is fair. Calling it a calibrated prior is not.
- The same caution applies to λ_R (§6.8). The Solvency II CoC is applied to the SCR, a 99.5% one-year VaR, in the risk-margin calculation. Mapping it to "per $ of CVaR95" mixes risk measures and needs a scaling step.

### R7 (Low): The stress bid multiplier mixes statistics
- h ≈ 0.70 = 61/87 divides a Cogent *average high bid* (Jul–Nov 2008, against stale NAVs per the source) by a Jefferies *average executed price* (H1-2026, against current NAV).
- Applied to NAV that the stress paths have already marked down, it risks double counting.
- Fix: calibrate h explicitly against reported-NAV lag.

### R8 (Low): EVPI is misused
- EVPI (about $33m) bounds the value of *information about the forward IRR*.
- Competitive tension (three or more bidders) improves price, not information. A re-underwrite yields EVSI, which is less than EVPI.
- "Spend part of the EVPI on competitive tension" therefore conflates two different things.

### R9 (Low): Internal inconsistencies
- **(a) Reservation price.** §2.4 defines p\* with LAPV(hold) and omits λ_Lev and ρ relief. Example 1's 85.9% uses HOLD + best REFI; on HOLD alone it would be 85.4%.
- **(b) Deferred consideration.** Pitfall 6 prices it at r_f + ℓ + a buyer spread, but Example 1 uses r_f + ℓ. With a 2% or 4% buyer spread, the headline needed to match 88% cash is 94.3% or 95.2%, not 93.5%.
- **(c) Mixed duals.** Open question 5 proposes robust duals for SELL and LEVER but expected duals for REFI. That breaks "one currency" and the LEVER = ADD + REFI identity.

### R10 (Low): Scale claims need caveats
- **Udell–Boyd bound.** It is independent of the number of assets, but it scales with roughly m × (the largest per-asset non-convexity).
  - Moving from m = 3 (Example 3) to m ≈ 20 (§6.4) multiplies the worst-case gap by about 7.
  - The gap is dominated by ADIC's largest positions, so Example 3's 0.02% gap does not transfer automatically.
- **MILP run times.** The claim "~1,500 binaries in seconds" is plausible but optimistic at tight gaps. In the verifier's synthetic weakly coupled tests (1,500 binaries, 30 rows, HiGHS, 1e-6 gap), solve times were 1.7 s, 9.3 s and 39 s; 3,000 binaries took 4.4 s.

### R11 (Low): The unfunded-share penalty is an extrapolation
- Jefferies' "reducing demand for unfunded capital" concerns GP-led CV buy-and-build stories.
- Using it to justify an unfunded-share penalty in LP-interest bid models goes beyond the source. Calibrate the penalty from adviser bid data instead.

---

## 5. Reproducibility check

- `08_action_valuation_examples.py`, re-run from a copy, produced a results JSON **identical** to the committed `08_action_valuation_examples_results.json` (2.3 s).
- These dossier figures all match the JSON: 421.4, 535.3, 434.5, 408.7, 427.6, 93.5%, REFI +1.3/+2.3/+2.0, −7.9, +10.75, 85.9%, 108.2%, 7.4%, 11.75%, 15.2%/5.7%, 11.0%/6.8%, the sensitivity grid, the Monte Carlo statistics, wait-one-year 426.0/416.1/9.9/11%/42%, risk relief 3.8/11.5, κ break-even 12.55, all Example 2 values and probabilities, and all Example 3 values (−104.9/−102.1/2.86, prices, 3 split assets, −$24.7m, 4 disagreements).
- One immaterial rounding point: the dossier's Example 2 boundary "LEVER ≈3.0–4.4%" comes from the script's 0.25% grid, [3.0%, 4.25%]. The interpolated crossover is about 4.3%.
- The dossier says all libraries are present. Verified in the lab venv: cvxpy 1.9.3, clarabel 0.11.1, highspy 1.15.1, numba 0.68.0, pydantic 2.14.1, scipy 1.18.1.

---

## 6. Overall reliability rating

| Layer | Rating | Basis |
|---|---|---|
| Sourced facts ([S]) | **High** | 29 of 33 confirmed exactly; 3 minor corrections; 0 refuted |
| Citations | **High** | 16 of 16 checked are real and correctly specified |
| Worked-example arithmetic | **High** | Reproduces byte for byte |
| Analytical design and IC-facing conclusions | **Medium** | R1 (expected vs plug-in), R2 (unspecified LP objective / SDF), R3 (incomplete ℓ and Score), R4 (financing calibration) |
| **Overall** | **Medium** | Raise to High once R1–R4 are fixed and an engine-vs-shortcut reconciliation test exists |

---

## 7. Limits of this verification

- The shared WebSearch budget ran out partway through. Later checks used direct fetches of known primary URLs only. The references listed in §3, item 7, were not re-fetched.
- The 2009 trough in secondary pricing (relevant to R7) could not be checked for lack of search, so R7 is stated as a methodological concern, not a factual correction.
- The Yale FY23 endowment value (about $40.7bn) in #29 is from the verifier's memory.

---

## Citation corrections (2026-10-18)

- Erratum to claim #18 (Nadauld et al.): it was confirmed against the 2016 NBER WP 22404 abstract, which gives seller PME 0.974, the ~3 pp split for 4–9-year funds and the asymmetric-information and market-depth wording. The dossier cites the 2019 JFE version, 132(3):158–181, whose abstract gives 0.976 and the 5 pp gap only, so #18 should read "Corrected: 0.976 in the cited JFE version" (`research/literature/08_action_valuation.lit.md` fix 2; checked on the IDEAS JFE abstract page and the NBER page, 2026-10-18). The dossier now uses 0.976 and attributes the other points to WP 22404.
