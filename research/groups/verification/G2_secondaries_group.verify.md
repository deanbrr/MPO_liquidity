# G2 Secondaries group: verification log

*Adversarial fact-check of `research/groups/dossiers/G2_secondaries_group.md`. Prepared 2026-10-18. The dossier was not edited.*

## 1. Summary

**What was checked.**
- 25 empirical claims: the author's 18 flagged claims plus 7 others I judged load-bearing or suspicious.
- 30 references, 10 of them in detail (§3).
- The design implications and the specification card (§2.7, §3, §6, §7), for reasoning and formula errors. I re-ran the arithmetic of Examples A, B, E, F and G, the winner's-curse haircut and the excess-return approximation.

**Method.**
- I downloaded every primary PDF myself and extracted the text layers with pypdf: Jefferies Jul-2026 and Jan-2025, Evercore H1-2026 and FY-2025, Lazard Interim-2026, Campbell Lutyens FY-2025, the CFA Institute CV report, IPEV Dec-2025, ILPA 2023 (CVs) and 2017 (subscription lines), NBER w22404 and w25207, and Proskauer FY-2025.
- I then grepped for each number and read the surrounding text.
- Web pages were read with WebFetch: Callan, ILPA's CV page, Unquote, PEI, Fortune, Cornell LII (17a-7), BIS, IDEAS/RePEc and HEC working-paper pages.
- Bibliographic metadata came from Crossref and IDEAS.
- **Consensus search worked in this session.** I used it to check Maurin-Robinson-Strömberg, Albuquerque et al., Brown-Ghysels-Gredil and Harris et al. The dossier's research note 2, which says these tools were authentication stubs, is now out of date.
- A small arithmetic script lives at `scratchpad/scripts/g2v_checks.py` (session scratchpad).

**Bottom line.** The factual layer is very strong:
- All 18 flagged claims are confirmed against primary documents, essentially to the digit.
- Of the 7 additional claims, 3 are confirmed, 3 are corrected and 1 is unverifiable (§2).
- The 3 corrections are all minor:
  - "GP-led was the majority in H1-2026" holds for Jefferies and Evercore but not for Lazard (~49%).
  - The ILPA carry-roll sentence is a recommendation, not observed practice.
  - Buyer IRR was "≥20% in every age group" except 4-9-year funds (19.8%).
- Every reference checked exists, with correct authors, year, title and venue. There are a few version and labelling problems (§3).

**The design and specification layer has five must-fix problems (§4):**
1. **ℓ has two different units.** It is used as an annual liquidity spread (Example G, the REFINANCE test) and as a one-off premium compared directly with deal NPV (§2.7, G2-E12, the PACE rule, Example F). Under stream 08's curve the one-off equivalent is ≈17-24%, not 9%.
2. **The tail-end θ is mis-anchored and internally inconsistent.**
   - θ_tail = 0.88-0.92 is said to be "anchored on Nadauld et al.". Nadauld's own data (buyout tail-end mean price 82.2%; buyer PME ≈1.00) imply θ_tail ≈ 0.80-0.83.
   - With p_tail = 0.70-0.80, the regime table implies 4-10%/yr excess returns on tail-end deals in every regime. That contradicts the dossier's own α column and §2.3 ("tail-end is mostly lemons, not alpha").
3. **The PACE zero-reserve rule ignores the probability of stress.** "Zero when ℓ_S ≥ NPV_S − carry" contradicts the dossier's own Example F in 7 of 12 cells (2 more are borderline).
4. **G2-E6 accretion is on an inconsistent basis.** A₀ = N^ref − P^ce counts post-reference-date cash flows on one side only. Net distributions of 10% of N^ref before closing overstate accretion by 10pp (23% instead of 13%). G2-E2 also drops the (1 − f) factor from §2.2.
5. **The SACV risk parameters are inconsistent.** The drift μ ≈ 14% uses transaction β ≈ 2, but σ_SA = 35% is barely above BGG's diversified-fund 33%, which comes with β ≈ 1.0. With β ≈ 2, σ_SA should be ≈45-50%, and P(net < 1x) rises from 19-42% to ≈49%.

**Overall reliability:** sourcing and citations **HIGH**; design and specification layer **MEDIUM**; **overall MEDIUM** until R1-R5 are fixed (§6).

## 2. Claims table

S = author-flagged claim; A = additional claim I selected.

| # | Claim (abridged) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| S1 | H1-2026 volume a record $118bn (GP-led $62bn, 53%; LP-led $56bn); 2025 $240bn; Jefferies 2026 outlook ~$260bn; Evercore H1 $121bn; Lazard H1 $124bn | **Confirmed** | Exact: Jefferies pp. 2-4 ("~$260 Billion" updated outlook); Evercore p. 2 ($121bn = $65bn GP + $56bn LP); Lazard p. 3 ($124bn). See A1 for Lazard's lower GP-led share. | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| S2 | H1-2026 average LP pricing 87% (buyout 91, venture 79, credit 89, infrastructure 91, real estate 68); tail-end 25%+ discounts; Asia/EM 35%+ | **Confirmed** | Exact (pp. 2, 5-6). Geography: North America 88%, Europe 86%, Asia 66%, rest of world 59%. The 2020-25 panel in dossier §4.3 also matches the Fig. 2 text layer. | (Jefferies Jul-2026, above) |
| S3 | Dedicated capital $290bn at H1-2026 ($327bn at YE-2025); overhang 1.2x (LTM) vs 3.1x in 2020; leverage estimated at 15% of equity dry powder plus fundraising ($38bn) | **Confirmed** | Exact (p. 12). $143bn dry powder + $97bn closed-end + $12bn retail + $38bn leverage = $290bn; 15% × $252bn = $37.8bn. The overhang uses $252bn LTM volume (290/252 = 1.15x). Note that the $290bn **includes** the estimated leverage. The adjusted overhang is 1.3x on $328bn. | (Jefferies Jul-2026, above) |
| S4 | Evergreen FMV $120bn, 46% in secondaries; 2026 triggered elevated redemptions; several managers activated 5% NAV gates | **Confirmed** | Exact (p. 11; EvergreenLink data). The 46% share is up from 41% in 2025. Jefferies calls the 5% gates "standard" but does not state a period (a quarter is typical). | (Jefferies Jul-2026, above) |
| S5 | Evercore H1-2026: dry powder $194bn (LP-led $90bn, GP-led $104bn); semi-liquid evergreen AUM ~$500bn, >$130bn at secondary managers, ~45% allocated to secondaries; target gross multiples (4 years) 1.7 / 1.8 / 1.9 / 2.3x | **Confirmed** | Exact (pp. 5, 6, 10). Overhang "close to 1.0x … healthy, but not abundant". H2 fundraising target $154bn. Scope note: Evercore's ~$500bn is *all* semi-liquid evergreen AUM, while Jefferies' $120bn is PE-evergreen FMV, so the two are not comparable. | https://www.evercore.com/wp-content/uploads/2026/07/Evercore-H1-2026-Secondary-Market-Review.pdf |
| S6 | Evercore: 66% of LP-led volume had no deferral, 9% deferred >18 months (GP-led: 84% none); deferral "acts as a form of leverage"; Jefferies: deferrals in 26% of H1-2026 LP sales | **Confirmed** | Exact. Evercore p. 9: LP-led 66/3/20/2/9%, GP-led 84/6/10/1/0%. Deferred amount: 26-50% of price in 16%, 51-75% in 12%, 76-100% in 5%. Jefferies p. 6: 33% of LP sales structured, 26% with deferrals. | (Evercore H1-2026, above) |
| S7 | Lazard 1H-2026: ~87% of buyout SACV volume above 90% of NAV, 23% above par; 40% of buyout MACV volume below 90%; ~27% of transactions failed or paused; 40% of investors run evergreen or '40 Act vehicles with lower return thresholds | **Confirmed** | Exact (pp. 3, 9, 13, 15). SACV 1/12/5/59/23%; MACV 13/26/10/43/8% (39% below 90%, which Lazard rounds to 40%). **Caveat:** the 27% is a respondent-reported figure in a paragraph about technology deals returning in 2H. Lazard does not call it "27% of GP-led processes", as dossier §4.7 and §6.7 restate it (see R6). | https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf |
| S8 | Nadauld et al. (2006-14 broker data): PME 1.023 buyers vs 0.974 sellers (~5pp/yr), ~3pp for funds aged 4-9; buyer IRR mean (median) 22.3% (16.7%); sellers of 10+ year funds out-earn buyers on PME; 2009 mean price 54% of NAV | **Confirmed** | Exact against NBER w22404 (pp. 1-3, 15-19; Tables 1, 5, 6). 4-9 years: 1.013 vs 0.983. 2009: mean 54.4%, median 52.6%, 213 deals. Notes: (i) the published JFE (2019) abstract reports seller PME **0.976**, while 0.974 is the WP figure. (ii) The tail-end PME gap is −0.8pp and **insignificant** in the full sample (t = 1.20). It is significant only in buyout (−2.2pp, t = 4.25). | https://www.nber.org/papers/w22404 |
| S9 | Discounts and buyer-seller gaps larger in weak economies with less capital, for smaller funds and smaller deals; tail-end ~10% discount persists under time fixed effects | **Confirmed** | Exact (pp. 3, 20-21). Return gaps are also smaller for larger transactions (Table 8). The ~10% tail-end coefficient is relative to 4-9-year funds. Unconditional buyout tail-end mean price is 82.2% (Table 3). | (NBER w22404, above) |
| S10 | Transaction-based buyout indices: β > 2, vs < 0.5 for NAV-based (Preqin, Burgiss); insignificant CAPM alpha | **Confirmed** | Exact (w25207 pp. 1, 5-6; the hedonic index averages ~20%/yr, with α not significantly different from 0). Published as JF 78(2) (2023) under a new title; see §3 and R5. [2026-10-18 re-check, literature synthesis §2.4 item 6: the *JF* abstract (DOI 10.1111/jofi.13202) reports no betas but states that the index's CAPM alpha is zero. NBER WP 28691 (2021, same title as the *JF* paper) gives an index β of 1.79 (1.94 with log returns), volatility of about 34% against 14-20% for NAV indices, and "quite low" NAV betas (0.73-0.85 even with seven Dimson lags). The β > 2 / < 0.5 contrast is therefore a 2018-WP figure, and the dossier now cites the 2021 values. The *JF* full text was not accessed.] | https://www.nber.org/papers/w25207 |
| S11 | IPEV 2025: ASC 820-10-35-59 to 62 permits NAV for fund interests; buying at a discount "does not necessarily mean" underlying fair values must be adjusted; exceptions for actively traded interests or a decision to sell at other than NAV | **Confirmed** | Exact (Section I.4, Guideline 4.1 and commentary). The "does not necessarily" sentence concerns the fund's *underlying* investments. The day-one gain inference is US-GAAP-specific (R10). | https://www.privateequityvaluation.com/Portals/0/Documents/Guidelines/2025%20IPEV%20Valuation%20Guidelines.pdf |
| S12 | Callan: primaries' pooled TVPI exceeds secondaries' by ~0.38x; IRRs similar; lower dispersion; secondary NAV peaks ~65% of commitment by year 4 vs ~95% in years 5-6 for primaries | **Confirmed** | Exact (A. Davison, 20-Mar-2025, LSEG/Cambridge). Also confirmed: 20-year simulation 1.65x vs 1.35x; 2024 fundraising ~$100bn. | https://www.callan.com/?p=29041 |
| S13 | HEC/Evercore CV studies: 386-387 CVs (2018-24); TVPI variation limited; simulated SACV portfolios Gini 0.280 vs 0.581 (2021 buyout); MACVs earlier DPI | **Confirmed** | Exact, with nuance. 386 CVs (2018-23 vintages, 297 with performance data) is HEC RP 1584. 387 CVs (2018-24) is the 4th study (Evercore FY-2025 p. 13): N = 112 "Portfolio sampling", 1.48x, Gini 0.280, vs N = 185, 1.26x, 0.581. The "simulated portfolios" reading is an interpretation of "Portfolio sampling". TVPIs are NAV-based and mostly unrealised (R15). | https://www.evercore.com/wp-content/uploads/2026/02/Evercore-PCA-2025-Secondary-Market-Report.pdf |
| S14 | Evercore: 2020 LP-led $28bn vs $53bn in 2019 (−47%); GP-led rose to $32bn; third-party leverage 7% (2024) → 14% (2025) of respondents | **Confirmed** | Exact (FY-2025 p. 4 chart; p. 11 GP-led insights). The whole Evercore column of the dossier's §4.1 table, including start-of-year dry powder 65 → 216, matches. | (Evercore FY-2025, above) |
| S15 | Cogent average high bid 84.7% (H1-2008) → 61% (H2-2008); 83.5% after adjusting for public markets | **Confirmed** | Exact (Unquote, 26-Jan-2009). These are average **high** first-round bids on ~300 partnerships marketed Jul-Nov 2008, an upper bound on clearing prices. PEI describes the 61% as "five months through November 2008". | https://www.unquote.com/uk/news/85756/secondaries-pricing-dips-to-a-five-year-low |
| S16 | LP distribution yield ~10% in H1-2026, below 20% since 2023, vs 25% average since 2001 | **Confirmed** | Exact (Jefferies p. 3). This is a portfolio-level yield, not a mature-interest yield (relevant to §6.7's 0.5 multiplier). | (Jefferies Jul-2026, above) |
| S17 | Maurin-Robinson-Strömberg: funds with more illiquidity-tolerant LPs realise higher returns; a secondary market attenuates differences in fund returns but not in LP returns | **Confirmed** | Exact (abstract, *Management Science* 69(10) 5740-5771). It is a theoretical model prediction, not an empirical finding. | https://doi.org/10.1287/mnsc.2022.4612 |
| S18 | ILPA draft CV guidance 24-Jun-2026 (comments closed 5-Aug-2026; final pending); SEC adviser-led secondaries rule struck down by the Fifth Circuit on 5-Jun-2024; true status-quo option in ~22% of 2024 CVs (William Blair via CFA) | **Confirmed** | ILPA page: final guidance "later this year". CFA fn. 37: struck down 5 June 2024. CFA fn. 34: true status quo 22% (2023: 21%), modified 19%, reinvestment 59%. | https://ilpa.org/industry-guidance/principles-best-practices/continuation-funds/ |
| A1 | "GP-led the majority for the first time since 2021" in H1-2026 (§1 item 2, tagged [S]) | **Corrected** | It depends on the advisor. GP-led was a majority per Jefferies (53%) and Evercore (54% of mix). **Lazard estimates GP-led ≈49% and LP-led ≈51% of 1H-2026 volume.** State the disagreement. | https://lazard.com/media/mbcj4xsi/lazard-interim-2026-secondary-market-report.pdf |
| A2 | "The GP rolls 100% of accrued carry 'in almost all cases' (ILPA 2023)", listed under §2.6 alignment terms [S] | **Corrected** | ILPA's sentence is **normative**: "In almost all cases, the GP **should** roll 100% of the carried interest accrued into the continuation vehicle". The observed figure is from William Blair via CFA: GPs (excluding inactive partners) invested 100% of their proceeds in nearly 90% of 2024 CV transactions. | https://ilpa.org/wp-content/uploads/2023/05/Continuation-Funds-Considerations-for-Limited-Partners-and-General-Partners.pdf |
| A3 | Nadauld table note: buyer IRR "≥20% mean in every age group" (§4.5) | **Corrected** | Mean buyer IRR by age (WP Table 5): 24.8% (0-3 years), **19.8% (4-9 years)**, 27.4% (10+ years). Median deal $4.6m of NAV, ~1% seller-paid fee and 85.7% FoF buyers are all confirmed. | https://www.nber.org/system/files/working_papers/w22404/w22404.pdf |
| A4 | Campbell Lutyens FY-2025: 14 players did 70% of volume; LP-led discount 13.9%; SACV / MACV average discounts 3.1% / 4.2% (MACV 9.0% in 2024) | **Confirmed** | Exact (p. 1). The 13.9% is weighted by transaction value. The CL volume column of the dossier (135/106/111/155/225) also matches. | https://campbell-lutyens.com/media/qwydmsgy/2025-secondary-market-flash-report_campbell-lutyens.pdf |
| A5 | BGG: buyout fund-level total risk ≈33%/yr (used to set σ_SA) | **Confirmed** | Abstract: buyout β ≈ 1.0 and total risk 33%/yr (venture 1.4 and 40%). The β of 1.0 sits in tension with the transaction β ≈ 2 used for μ (R5). | https://doi.org/10.2139/ssrn.3507873 |
| A6 | Proskauer FY-2025: secondaries NAV facilities mostly <3% spread; closing LTV 25-50% in 57%, ≥50% in 43%; LTV-based sweeps in 83% | **Confirmed** | Exact (pp. 9, 11-13: "majority falling below 3%", 57%/43%, 83%). Proskauer adds that secondaries facilities are "predominantly used for portfolio acquisitions" (R7). | https://www.proskauer.com/uploads/insights-on-the-nav-financing-market-full-year-2025 |
| A7 | Albuquerque, Cassel, Phalippou & Schroth: 2009-16 bid data; effect stronger for young funds, high-VIX and high-funding-cost periods, and non-specialised buyers (§2.3, tagged [C]) | **Unverifiable** | The SSRN abstract confirms only the core result. The demand response to aggregate liquidity shocks is negatively related to contemporaneous bids, more so for funds likely sold when liquidity is low, and is unrelated to future NAV returns, so discounts track liquidity provision. The period, VIX, funding-cost and buyer-type specifics were not found. | https://doi.org/10.2139/ssrn.3182481 |

**Also confirmed in passing** (not counted above):
- **Jefferies Jan-2025:**
  - 2017-19 dedicated capital $125/192/155bn, overhang 2.2/2.6/1.8x;
  - evergreen "nearly one-third" of 2024 fundraising;
  - deferral lifted 2024 pricing ~400bp;
  - top 10 hold >50% of dry powder;
  - 2024 buyout pricing by age 99/96/88/79/70%.
- **Jefferies FY-2025 web page:** <5 years 95%, >10 years 73%.
- **Jefferies Jul-2026:**
  - 15 LP deals >$1bn and a record 5 >$2bn; >25 CVs >$1bn;
  - GP commitment ~10% in North America vs ~5% in Europe;
  - SACV company average vintage 2019;
  - FoF/secondaries 27% of LP sell-side.
- **Evercore H1-2026:** SACV/MACV pricing 34/52/14% and 71/22/8%; SWFs 12% → 21%; super-carry 35%; credit GP-leds ~99% of FMV.
- **Evercore FY-2025:**
  - new entrants 16% of volume and 21% of dry powder;
  - available capital $37bn (credit), $20bn (infrastructure) and $10bn (venture);
  - net-IRR targets mostly 13-15% for credit and infrastructure, >20% for venture.
- **Lazard:** 6% of investors hold ~43% of 2H GP-led capital; ~60% say GP marks moved only modestly; 2026E $275bn ($255-295bn), 2027E $305bn.
- **CFA Institute:**
  - Lazard 2024 SACV targets 2.2x and 21.3% net IRR;
  - Morgan Stanley median MOIC 1.4x (CVs) vs 1.3x (buyout);
  - Ardian ASF IX $30bn (Jan-2025);
  - lead 60bp vs syndicate 75bp (Rode et al.) [2026-10-18: the split is the report's own example (p. 21). The citation that follows it is Rode, Poldauf & Fuentes Perez (2025), Schroders Capital, p. 5 (reference list p. 45), now dossier ref 39. Schroders' web summary gives CV management fees as "roughly half" of traditional buyout fees and no bp figures, so the split is unverified at source];
  - "unaware of published rigorous studies".
- **ILPA 2017:** 15-25% of uncalled capital, 180 days, net IRR with and without the line. These are example thresholds.
- **Rule 17a-7:** "independent current market price", cash, no remuneration, board procedures, quarterly review.

## 3. Citation check

| Ref | Citation as given | Exists | Authors / year / title / venue | Note |
|---|---|---|---|---|
| 1 | Jefferies (Jul-2026), *Global Secondary Market Review* | Yes | Correct | 13 pp.; text layer extracts cleanly. |
| 5 | Evercore PCA (Jul-2026), *H1 2026 Secondary Market Review* | Yes | Correct | 25 pp. The HEC 5th study (2018-24) is on p. 11. |
| 6 | Evercore PCA (Feb-2026), *2025 Secondary Market Report* | Yes | Correct | 4th HEC study (387 CVs) on p. 13. |
| 7 | Lazard PCA (Aug-2026), *Interim Secondary Market Report 2026* | Yes | Correct | 22 pp. |
| 11 | Nadauld, Sensoy, Vorkink & Weisbach (2019), JFE 132(3) 158-181, DOI 10.1016/j.jfineco.2018.11.007; NBER w22404 | Yes | Correct (Crossref) | **Version mismatch:** all quoted figures come from the 2016 WP. The JFE abstract has seller PME 0.976, not 0.974. Cite the figures to w22404, or re-check them against the JFE tables. [2026-10-18: applied; the dossier now labels them w22404 figures and shows 0.976.] |
| 12 | Boyer, Nadauld, Vorkink & Weisbach (2018), NBER w25207, *Private Equity Indices Based on Secondary Market Transactions* | Yes | Correct (Nov 2018) | **Published version not cited:** "Discount-Rate Risk in Private Equity: Evidence from Secondary Market Transactions", *Journal of Finance* 78(2), 2023, 835-885. Its emphasis is discount-rate risk. Check whether the β > 2 / < 0.5 figures carry over before citing them to the IC. [2026-10-18: they do not carry over to the 2021 version (see S10). Dossier ref 12 now cites the *JF* version, DOI 10.1111/jofi.13202.] |
| 14 | Maurin, Robinson & Strömberg (2023), *Management Science* 69(10) 5740-5771 | Yes | Correct (Crossref) | Theory paper. |
| 27 | IPEV (11-Dec-2025), *Valuation Guidelines*, §4 | Yes | Correct | Cover reads "December 2025"; the day (11th) was not verified. |
| 10 | Callan, A. Davison (20-Mar-2025), *Secondary Investments: Key Issues for Institutional Investors* | Yes | Correct | Author is Aidan Davison. |
| 30 | Deane & Robinson (Sep-2025), *Continuation Funds: Ethics in Private Markets, Part I*, CFA Institute | Yes | Correct | Stephen Deane and Ken Robinson. |

**Other references checked, all correct:**
- Lerner & Schoar (2004) JFE 72(1) 3-40.
- Harris, Jenkinson, Kaplan & Stucke (2018) JFE 129(2) 287-305.
- Bollen & Sensoy (2022) *Financial Management* 51(2) 501-538 (DOI 10.1111/fima.12375). [2026-10-18: the full title adds "Illiquidity, secondary markets, and the value of private equity" (Crossref). It was an orphan in the dossier and is now cited in §2.3.]
- Allen & Gale (1994) AER 84(4) 933-955.
- Shleifer & Vishny (2011) JEP 25(1) 29-48.
- Bolton, Chen & Wang (2013) JFE 109(1) 40-62.
- Takahashi & Alexander (2002) JPM 28(2) 90-100.
- Brown, Ghysels & Gredil (2023) RFS 36(3) 945-986.
- Gourier, Phalippou & Westerfield (2024) JF 79(5) 3407-3457. [2026-10-18: it was an orphan in the dossier and is now cited in §6.5 item 5.]
- Luxenberg, Boyd et al. (2022) arXiv 2207.07767. [2026-10-18: the peer-reviewed version is ICAIF '22, pp. 249-256, DOI 10.1145/3533271.3561769 (Crossref); dossier ref 26 updated.]
- Gottschalg HEC RP 1515 (2024: 231 CVs, 140 with performance) and RP 1584 (2025: 386 CVs, 297 with performance). [2026-10-18: RP 1515 is SSRN DOI 10.2139/ssrn.4752652; both are non-peer-reviewed.]
- Campbell Lutyens FY-2025; Proskauer FY-2025; ILPA 2023 and 2017.
- 17 CFR 270.17a-7; BCBS (15-Apr-2009).
- Unquote (26-Jan-2009).

**Minor citation problems:**
- **Ref 13 (Albuquerque et al., 2018 WP).** It exists (SSRN 3182481, Cass WP), but the paraphrase adds specifics not in the abstract (A7). Cite SSRN. [2026-10-18: applied. Dossier ref 13 cites DOI 10.2139/ssrn.3182481, and §2.3 tags the specifics [C].]
- **Ref 33 (Fortune).** Author and date are correct (Greg McKenna, 15-Jun-2025, "permissible according to generally accepted accounting principles"). The title given is a paraphrase. The actual headline is "As Harvard's and Yale's private equity holdings go on sale, buyers can use this technique for 1,000% windfalls. 'It makes your brain melt'".
- **Ref 35 (Beaudoin et al. 2009).** It exists (WilmerHale reprint, Mar/Apr 2009); the volume/issue "18(4)" was not verified.
- **Ref 28 (ILPA 2023).** The carry-roll quotation is normative (A2).

## 4. Reasoning issues and overclaims (design implications and specification card)

### Must-fix before the specification card is implemented

**R1. ℓ is used in two incompatible units.**
- **As an annual spread:**
  - Example G and executive summary item 8 ("stream 08's liquidity curve 9% / 9% / 4%");
  - the REFINANCE test ("spread + λ_Lev < life-weighted ℓ̄").
- **As a one-off premium compared with deal NPV:**
  - §2.7 ("roughly NPV_{j,s} ≥ ℓ_s");
  - G2-E12 ("NPV_now − ℓ_now ≥ OV_t");
  - the PACE rule;
  - Example F (ℓ_S = 0 / 10 / 20% against NPV_S = 15 / 25%).
- **Size of the gap.** The one-off equivalent of 9%, 9%, then 4% is a PV haircut of ≈17.5% / 20.3% / 23.7% for durations of 2.5 / 3.4 / 4.5 years. Example G's mature interest gives 82.6, a 17.4% haircut. Comparing NPV with ℓ = 9% is therefore far too lenient.
- **Consequence.** At ADIC's current ℓ, Example F's relevant column is ℓ_S ≈ 20%, where holding a reserve never pays.
- **Fix.** Define ℓ_{s,t} as a per-period rate. Wherever NPV is compared, use L_s = π_{s,0}/π̄ − 1, or the duration-weighted equivalent.

**R2. θ_tail is mis-anchored and inconsistent with the dossier's own α and with §2.3.**
- **What the spec says.** The parameter defaults give θ = 0.88 (10+ years), "[I, anchored on Nadauld et al.]". §6.7 uses θ_tail = 0.92 / 0.90 / 0.88 / 0.70 / 0.82 (B/N/D/C/W) against p_tail = 0.80 / 0.75 / 0.70-0.75 / 0.40-0.50 / 0.60.
- **What Nadauld's numbers imply.** Buyout tail-end mean (median) price was 82.2% (80.3%) of NAV (Table 3). Buyout tail-end buyer PME was 1.001 (Table 6). So tail-end buyers earned about the market at ~82% of NAV, which implies θ_tail ≈ 0.80-0.83. It is if anything lower, because unliquidated funds are valued at last NAV.
- **Implied tail-end excess, (θ/p)^{1/D} − 1 with D = 2.5-3.4:**

  | Regime | θ/p | Implied excess | Dossier's α |
  |---|---|---|---|
  | B | 1.15 | 4.2-5.7% | 0-1% |
  | N | 1.20 | 5.5-7.6% | 1-2% |
  | D | 1.17-1.26 | 4.8-9.6% | 3-5% ("complex") |

  For diversified buyout the same formula agrees with the α column: 1.6-2.9% in D, against 2-3%.
- **Consequence.** As specified, the optimizer will see tail-ends as the best opportunity in every regime. That contradicts §2.3 ("The tail-end segment is mostly the second [information or quality component] … not alpha").
- **Fix.** Set θ_tail ≈ p_tail × (1 + small premium). For example θ_tail ≈ 0.78-0.83 in N, and lower in D, where Jefferies flags "challenged" residual assets.

**R3. The PACE zero-reserve condition is mis-specified.**
- **The rule.** "Zero when ℓ_S ≥ NPV_S − carry" omits the stress probability p_S and the forgone deploy-now value.
- **What Example F actually implies.** Example F is reproduced exactly by gain = p_S·max(NPV_S − ℓ_S, 0) − c(p_S), with c = 2.7% at p_S = 10% and 3.0% at p_S = 20%.
- **The contradiction.** The spec rule says "hold" in 10 cells. Example F's gain is negative in 7 of them and zero in 2 more. For example, at p_S = 10%, NPV_S = 25%, ℓ_S = 0 the rule says hold, but the gain is −0.2%.
- **Fix.** Derive the threshold from OV_t: R = 0 when p_S·E[(NPV_S − L_S)^+] ≤ carry + forgone NPV_now (one-period form). Combine with R1.

**R4. G2-E6 and G2-E2 put price, NAV and value on inconsistent bases.**
- **The accretion error.** P^ce = pN^ref + Σ_{(ref,0]}(C − D), but the spec sets A₀ = N^ref − P^ce = (1 − p)N^ref − Σ(C − D).
  - The book NAV at closing is N^ref + Σ(C − D), plus any GP re-mark, so the correct accretion is A₀ = N^GP₀ − P^ce = (1 − p)N^ref absent re-marks.
  - Example: with net distributions of 10% of N^ref between the reference date and closing (common for mature interests), the spec gives 23% accretion instead of 13%.
- **The same basis problem elsewhere.**
  - G2-E11 compares V₀ = θN^ref with P^ce, which includes Σ(C − D).
  - The excess-return approximation compares θ with p.
  - Roll N^ref forward, or strip the post-reference flows from P^ce.
- **Missing fee factor.** G2-E2 (V = N^ref e^{βr} q) omits the (1 − f) term of §2.2.

**R5. The SACV risk parameters are inconsistent with each other.**
- **The drift.** Example E's μ = 14% equals r_f + β·ERP + α at β ≈ 2, the transaction β of S10.
- **The volatility.** σ_SA = 35% is barely above BGG's *diversified-fund* total risk of 33%, which comes with β ≈ 1.0 (A5).
- **Why they conflict.** With β ≈ 2 and market volatility of ~15-16%, systematic volatility alone is ≈30-32%. Single-company idiosyncratic risk then implies σ_SA ≈ 45-50%. [2026-10-18: the 2021 version of Boyer et al. gives β ≈ 1.8 (1.9 with log returns; see S10), so systematic volatility is ≈27-31%. The implied σ_SA is somewhat lower, but the inconsistency with σ_SA = 35% stands.]
- **Size of the effect.** At μ = 14% and σ = 50%, the 4.5-year median gross MOIC is ≈1.07x and P(net < 1x) ≈ 49%, against 19-42% in Example E. SACV concentration risk and the "≈26% reach 2.3x" bias statistic are therefore understated.
- **Either pair works; mixing them does not.**
  - cash-flow β of 1.05-1.25, which the specification card also cites, with σ_SA ≈ 35-40% and a lower μ; or
  - β ≈ 2 with σ_SA ≈ 45-50%.
- **What Boyer et al.'s β actually measures.** It is estimated on secondary prices of *fund stakes*. Those prices embed time-varying discounts, which is the published JF version's "discount-rate risk". Using it as "β for buyout exit values", and as the overlay's exit-value hedge ratio, conflates liquidity-discount risk with asset risk.

### Should-fix

**R6. The execution probability is mis-anchored.**
- **The problem.** §6.7 sets e = 0.70-0.75 in regime D from Lazard's "27% failed or paused". That figure is a respondent-reported process failure rate in a software-repricing half, not ADIC's probability of winning.
- **Win rates are much lower.** With ~3 bids per transaction (Nadauld) and 88% of LP-led volume in advisor-led multi-bidder processes (Evercore), a symmetric bidder wins about a third of processes or fewer.
- **Fix.** Define e = P(process closes) × P(win | bid), or define Q as expected won volume. Avoid double-counting with ω.

**R7. Several SELL / REFINANCE actions are not under the LP's unilateral control.**
- **CV-to-CV exits** are GP-initiated. ADIC can only elect to sell or roll when one is offered.
- **Consents.** Tertiary sales of S1 interests and transfers of S3 interests need GP consent and ROFR waivers.
- **Pledges.** A "book-level secondaries facility" requires pledging LP interests, which LPAs commonly restrict without GP consent.
- **Deferral timing.** "Renegotiate deferral timing" needs the counterparty's agreement.
- **Pricing anchor.** The Proskauer anchor (<300bp, LTV 25-70%) describes secondary *funds'* acquisition facilities ("predominantly used for portfolio acquisitions"), not an LP refinancing an existing book.
- **Fix.** Add feasibility and consent probabilities and lead times to each action, and use an LP-level NAV-facility quote (for example from Capital Solutions).

**R8. "Agrees with stream 06's estimate of about 20bp a year" (§1 item 7) is an overclaim.** The two figures differ in every dimension:

| | G2 dossier | Stream 06 |
|---|---|---|
| Value | +2.0% | ≈20bp |
| Unit | per dollar of reserve per year | of *total NAV* per year |
| Carry | net of 2% carry | gross of carry |
| Stress frequency | p_S = 20% | one episode per ~8 years |
| Price basis | — | headline 25% discount, "assuming fair marks", which G2 itself rejects |

At a comparable frequency (p_S = 10%), G2's own grid gives −0.2% to −2.7%. That is disagreement, not agreement.

**R9. The excess-return approximation omits a factor, and the fit claim is overstated.**
- The exact relation is (1 + y_P) ≈ (1 + y_V)(θ/p)^{1/D}. The (1 + y_V) factor is missing.
- "Agree to within about 0.7pp" fails at θ = 1. Example A gives 14.3 − 9.0 = 5.3pp, against 4.2pp from the formula (4.6pp with the factor).
- Use the corrected form in the specification card.

**R10. The accounting statement is framework-specific.**
- "Buying at 87% books a +14.9% day-one gain" holds under the US-GAAP practical expedient.
- IFRS has no practical expedient. Under IFRS 9 B5.1.2A, a day-one gain not evidenced by a Level-1 price or observable-input technique is deferred, and NAV is a Level-3 input.
- Confirm ADIC's reporting basis. The recommendation to report accretion separately stands either way.

**R11. The W-flag excess α (4-8%) and "opportunity peaks 2-6 quarters after a shock" lack return evidence.**
- They are anchored on the H2/H1-2020 *volume* ratio (2.3x), which is not a return measure.
- Nadauld's large buyer premia came from 2008-09 acute-phase young-fund sales.
- 2020 pricing recovered quickly: buyout 90% in 2020, 97% in 2021.
- Label the W-flag α as a prior and stress-test it.

**R12. The winner's-curse haircut probably understates the effect.**
- "Wins against n similar bidders" with n = 3 uses E[max of 3] = 0.846 (4.2%). That is right only if n counts ADIC.
- With 3 competitors, E[max of 4] = 1.029 (5.1%).
- Nadauld's ~3 bids come from small deals (median $4.6m NAV). ADIC-scale processes are wider auctions, so the haircut is likely larger.

### Minor

- **R13.** Advisor disagreement on the GP-led share (A1) should be shown wherever "majority" is asserted.
- **R14.** ILPA's normative carry-roll statement (A2) is presented as an observed term.
- **R15. SACV dispersion.**
  - "SACV outcomes are narrower" (§1 item 4) rests on NAV-based, mostly unrealised TVPIs and on the Gini of *sampled portfolios* of SACVs.
  - NAV smoothing understates dispersion (S10).
  - Do not use the 0.28 Gini to calibrate single-asset risk, and reconcile it with σ_SA (R5).
- **R16. Tier-1 survival.** It applies a 0.7x acute-phase multiplier to secondary-fund calls, which *reduces* stressed outflows. For a hard survival gate, also test ≥1.0x, since managers with dry powder may accelerate calls when discounts peak.
- **R17. Default pacing.** The default deployment of US$3-4bn a year (§6.1) conflicts with the dossier's own finding that, at current ℓ, mainstream LP purchases have negative LAPV (82.6 vs 87.9 in Example G). Make the default regime- and ℓ-conditional.
- **R18. Price equation.** The §3.4 equation uses K_t/Vol_t, which is endogenous because volume falls when bids fall. Note the simultaneity bias when estimating γ_K, and consider fundraising or evergreen flows as instruments.
- **R19. Rule 17a-7.** It applies only to securities with readily available market quotations. LP interests do not qualify, so it is an analogue, not a template. The dossier's external-price requirement is consistent with that.
- **R20. Pitfall 1 (§7).** "As Nadauld et al. do" is a loose paraphrase. They drop transactions within 4 quarters of fund liquidation or the last available NAV, which is analogous but not identical to excluding positions held for less than 4 quarters.

### Arithmetic reproduced and found correct

- Day-one gain 1/p − 1: 14.9% / 25% / 42.9%.
- Quarter-one annualised IRR: 90% at 0.87 and 166% at 0.80.
- Excess approximation: 4.2% and 2.6%.
- Implied deferral vendor rate: 9.64%.
- Example E (closed form, T = 4.5): medians 1.63 / 1.42 / 1.19x; P(net < 1) 19.5 / 33.3 / 42.5%; P(≥2.3x) 25.9 / 26.0 / 18.8%. The dossier's 27% for row 1 is close.
- Example G rotation: +20.8 / +8.2 / −1.8.
- Staleness factor: 61/83.5 = 0.73.
- MACV volatility formula and CRPS definition.
- Book shares (40 / 33 / 24 / 3%) and constraint checks (unfunded plus deferred 27.9%, deferred 2.9%, SACVs 14.3%, group 7.9% of total).

## 5. Things the dossier gets right that the IC should hear

- Most headline "discount capture" is accretion. The dossier's insistence on economic-basis UW / ACT / SG series and a separate accretion KPI is correct and well sourced (IPEV; Nadauld's 4-quarter exclusion; Fortune).
- Treating deferred consideration as debt (Evercore: deferral "acts as a form of leverage") and as a hard Tier-1 outflow is correct.
- Treating internal crosses as zero-sum apart from costs, and never as liquidity, is correct.
- The countercyclical opportunity versus procyclical ADIC liquidity, and the evergreen pro-cyclicality (gates), are well evidenced.

## 6. Overall reliability rating

- **Sourced empirical claims and citations: HIGH.**
  - 21 of 25 checked claims are confirmed exactly, 3 have minor corrections, none is refuted, and 1 [C]-tagged paraphrase is unverifiable.
  - All references exist and are correctly cited, apart from minor version and title issues.
- **Design and specification layer: MEDIUM.** R1-R5 would change decisions: buy versus hold, reserve sizing, tail-end allocation, accretion reporting and SACV concentration risk.
- **Overall: MEDIUM** until R1-R5 are fixed. Then HIGH.

## 7. Notes for the orchestrator

- Consensus search (not the authentication tools) was usable in this session. The dossier's open question 11 can be partly closed: a systematic peer-reviewed sweep is feasible.
- Papers checked through Consensus search, with the URLs it returned:
  - [Liquidity Provision in the Secondary Market for Private Equity Fund Stakes](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop) (Albuquerque et al., 2018, SSRN, DOI: 10.2139/ssrn.3182481);
  - [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop) (Maurin et al., Management Science, DOI: 10.1287/mnsc.2022.4612);
  - [Nowcasting Net Asset Values: The Case of Private Equity](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop) (Brown et al., SSRN, DOI: 10.2139/ssrn.3507873);
  - [Financial intermediation in private equity: How well do funds of funds perform?](https://consensus.app/papers/details/ea5db342103e5bb78ebe02c7fca2fa95/?utm_source=claude_desktop) (Harris et al., NBER WP 2017; journal version confirmed via IDEAS);
  - [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop) (Nadauld et al., 2019, JFE, DOI: 10.1016/j.jfineco.2018.11.007).

## Citation corrections (2026-10-18)

These are the citation-audit annotations from `research/literature/00_LITERATURE_SYNTHESIS.md` §2 and `research/literature/G2_secondaries_group.lit.md`. The dossier was corrected in the same pass; see its own "Citation corrections (2026-10-18)" section. The original verdicts above are kept, and each annotation is bracketed and dated.

1. S10 (Boyer et al.): re-checked against the *JF* 2023 abstract (DOI 10.1111/jofi.13202) and NBER WP 28691. The β > 2 / < 0.5 contrast is a 2018-WP figure; the 2021 version gives β 1.79 (1.94 with log returns) and "quite low" NAV betas.
2. §2 "Also confirmed in passing" (CFA Institute, Rode et al.): the full citation is recorded (Rode, Poldauf & Fuentes Perez 2025, Schroders Capital). The 60bp / 75bp split is the CFA report's own example and is unverified at source.
3. §3 ref 11 row (Nadauld et al.): marked as applied in the dossier.
4. §3 ref 12 row (Boyer et al.): re-check outcome and *JF* DOI added.
5. §3 "Other references" (Bollen & Sensoy, Gourier et al., Luxenberg et al., Gottschalg RP 1515): orphan status and the dossier fix recorded; full title, ICAIF '22 version and SSRN DOI added.
6. §3 "Minor citation problems", ref 13 (Albuquerque et al.): marked as applied in the dossier.
7. R5: note added that the 2021 β of about 1.8 lowers systematic volatility to about 27-31%, while the β-σ inconsistency stands.
