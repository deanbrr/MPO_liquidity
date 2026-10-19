# G12 Real Assets: energy & natural resources (oil linkage, wrong-way risk): Verification Log

- **Dossier checked:** `research/groups/dossiers/G12_ra_natural_resources_energy.md` (stream G12, as of 18 Oct 2026). The dossier was not edited.
- **Date of check:** 18 Oct 2026. Adversarial fact-check ahead of the IC pack.
- **Background read:** `inputs/00_CONTEXT_AND_PRIOR_WORK.md` §1A; `design/00_DESIGN_BRIEF.md` §8; `research/00_SYNTHESIS.md` (draw kinks, oil put-spread programme).
- **Method:**
  - **Primary PDFs were fetched and text-extracted locally** (pypdf, isolated folders): Meketa (2024), both Norges Bank letters (2017, 2018), IMF WP/10/9, the OCC handbook (v2.2), SEC Release 33-8995, the NGFS Phase V overview, Jefferies H1 2026 and NSHE INV-6.
  - **Web pages were read directly:** CA (2017, 2020), Haynes and Boone (spring and fall 2016) and the ARMB materials index.
  - **Press or secondary sources were used where the primary page was blocked** (403 or login redirect): regjeringen.no, iea.org, nature.com and cnbc.com.
  - **Academic metadata** came from the Crossref and OpenAlex APIs and IDEAS/RePEc.
  - **[I-calc]: recomputed independently** from raw Kenneth French files (49 industries and FF factors, to Aug 2026) and EIA Brent (RBRTE, via FRED DCOILBRENTEU). Covered: the five episode tables, the max drawdowns since 1988 and the full-sample partial oil betas.
  - **[I-MC]: every synthetic number was traced** to the JSON outputs in `research/groups/addenda/G12_calcs/`. The scripts (`g12_wrongway_sim.py`, `g12_hedging_demand.py`, `g12_enr_book.py`) were read for method. A small harness computed put-spread deltas and sleeve-delta variants.
  - **ARMB** figures were checked against a text extract of the 15–16 Sep 2026 (day-2) board packet held in the session scratchpad. The packet is listed on the ARMB materials page.
  - Consensus was not used.

---

## 1. Summary

- **Scope:** 29 claims checked: the 20 author-flagged claims, 3 added in the main table and 6 supplementary spot checks. **26 confirmed, 2 corrected, 0 refuted, 1 unverifiable.**
- **The sourced evidence is strong.** Every external statistic matches its primary source, mostly verbatim:
  - Meketa/CA composite returns, volatility and correlations; CA 2017 and CA 2020;
  - both Norges Bank letters: every beta, the 14.86% → 15.02% volatility and the NOK 4,000bn;
  - the IMF WP/10/9 quotations (pp. 8 and 19), the OCC RBL mechanics and SEC 33-8995;
  - Haynes and Boone, ARMB, Jefferies, NGFS, Welsby et al. and Wheaton–BHP.
- **Reproducibility is strong.**
  - The 2014–16 episode reproduces exactly from raw data: Brent −70.2%, US market −0.6%, oil −38.5%, coal −88.0%, mines −44.6%.
  - The other four episodes and every max drawdown also reproduce exactly. The partial oil betas are within one standard error.
  - Every [I-MC] number matches its JSON.
- **Source-level correction (1).** Norway did **not** exclude "the highest-oil-beta subsector".
  - In Norges Bank's own table, oil equipment & services (0.61) sits above E&P (0.54). Services were retained; Norges Bank called the difference "not significant".
  - Norway excluded by FTSE label. The dossier's "classify by oil beta, not by label" is a sound design principle, but it cannot be drawn from Norway's practice.
- **Analysis-level corrections.** These matter more for the IC:
  1. **R1. The headline HEDGE action is mostly not available to ADIC as LP.** "Hedge 70% of 3-year production at asset level → ≈6m bbl" assumes ADIC controls hedging.
     - In the synthetic split, $0.80bn of the $1.07bn of levered upstream sits in closed-end funds, where the GP decides.
     - Hedging only the $0.27bn direct position leaves ≈10.7m bbl, still above the 10m hard limit.
  2. **R2. "Breaches the hard limit" depends on an unstated price basis.**
     - The 12.2m bbl uses elasticities at the $70 N state. C1 is defined at the generator's *current* state.
     - The same JSON's GW/$95 elasticities give ≈9.2m bbl for the same $2.5bn NAV: inside the hard limit, above the soft limit.
  3. **R3. "Offsets 31–61% of the put-spread programme" divides delta by option notional.**
     - At the overlay's forwards, 20–40m bbl of 1-year 64/31 put spreads carry only ≈2–8m bbl of spot-equivalent delta.
     - In the glut state, the dossier's own losses ($0.68–0.96bn) are 0.9–2.5× the put-spread payoff ($0.38–0.76bn).
  4. **R4. Equity cures are modelled as mandatory cash calls.** Reserve-based lending (RBL) is normally non-recourse, so a cure is the sponsor's option. For fund-held assets the GP decides, within unfunded commitments.
  5. **R5. C3 sizes the cure reserve at the SG-conditional mean (13% of levered equity), not at a tail.** About half of SG outcomes would exceed it.
- **Overall reliability: MEDIUM.**
  - It is high for sourced facts and for reproducibility.
  - Recommendation 6(c)/(e), the HEDGE action definition, C2 and C3 must be restated with R1–R5 before they reach the IC. The direction of the advice survives: run ENR on an oil-delta budget, add no new unhedged upstream, and sell into the Gulf-war bid.

---

## 2. Claims table

| # | Claim (as in dossier) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| 1 | CA Global Natural Resources composite: 11.2% a year since 1990 (US equity 10.1%, PE 15.0%); 3.2% from Q3-2013 to Q2-2023 (PE 15.2%, US equity 12.3%); smoothed vol 11.4% (PE 10.3%, US equity 16.7%); ρ 0.34 with US equity, 0.48 with PE, 0.0 with bonds. Also: 27 of 35 years; IQR 12.9%; fund terms | Confirmed | All verbatim (Meketa pp. 7–8 and 10–12). Footnotes give the periods (Q1-1990 to Q2-2023; Q3-2013 to Q2-2023), the basis (linked quarterly pooled IRRs) and US equity = Russell 3000. Also confirmed: "27 of the 35 analyzed years"; IQR 12.9% for 2010–19 vintages; average 23 funds per vintage; fees 1.5–2.0%, 6–8% hurdle, 15–20% carry, 10–15-year terms; "store on the stump". *Omission:* Meketa also says private energy–oil correlations "have been positive but low over the long term", even when lagged. That is relevant to the dossier's "high-oil-beta" reading and the smoothing argument. | https://meketa.com/wp-content/uploads/2024/03/MEKETA_Private-Natural-Resources.pdf |
| 2 | 184 energy funds of 2004–14 vintages trailed PE by 0.56× net MOIC; 2013–14 vintages by 0.40×; correlations > 0.7 since 2013; record $55.2bn raised in 2014 | Confirmed | "184 mature and maturing funds with vintage years between 2004 and 2014"; "lagged broader PE returns by 0.56x"; "19 2013 and 2014 vintage year ELOC funds lagging broader PE by an average 0.40x", so the 0.40× rests on only 19 funds; correlations "both above 0.7 since 2013"; "$55.2 billion". Published 21 May 2020. | https://www.cambridgeassociates.com/insight/real-asset-dynamics-pe-energy/ |
| 3 | 1986–2010 vintages: mean net IRR 12.7%, TVPI 1.8×, ≈500bp over PME; a 1pp three-year oil move ≈ 0.65pp of private energy return; private energy 2.8% of the average US endowment and foundation portfolio, >25% of real assets | Confirmed | "average net IRR of 12.7% and a net TVPI of 1.8"; "nearly 500 basis points"; 0.65pp over a three-year window; 2.8% of E&F portfolios; real assets 9.9%, of which ">25%" is private energy. Published 20 Sep 2017. | https://www.cambridgeassociates.com/insight/private-energy-deserving-a-place/ |
| 4 | NB (2018): relative oil betas to 12-month WTI futures, Jan 2006–Aug 2017: E&P 0.54, integrated 0.36, OES 0.61, pipelines 0.27, renewable equipment 0.06 (insignificant). Excluding oil and gas: equity vol 14.86% → 15.02%; 70/30 10.86% → 10.99% (1973–2017) | Confirmed | Enclosure Table 2 (Newey–West, 3 lags) and Table 7 (MSCI World, Jan 1973–Dec 2017), verbatim. Nuance: the renewable-equipment sample is Dec 2009–Aug 2017 (N = 93); alternative fuels is 0.12 (insignificant). Table 8 confirms the fiscal cash-flow β of 1.24 (1973–2016) and 1.92 (ρ = 79%, 1996–2016). | https://www.nbim.no/contentassets/5beb197aa8c544b39fe547e2d6eb3b13/2018-04-26-nb-to-mof-energy-stocks-in-the-gpfg.pdf |
| 5 | NB (2017): PV of government oil and gas revenue ≈NOK 4,000bn, fund ≈2×; a permanent NOK 100/bbl drop "would more than halve" it; oil and gas ≈4% of the fund; with Statoil ≈2× index weight; β_oil 0.41, β_eq 0.71; relative β 0.40 (R² 0.45); energy bonds 0.04 (0.08 since 2008); basic materials 0.14 | Confirmed | All verbatim: letter pp. 2–3 and enclosure Tables 2–4. The 0.41/0.71 are excess-return betas over the entire sample. The 0.40 with R² 0.45 is Model 4 (Jan 1994–Jul 2017). The bond β of 0.08 is from July 2008. | https://www.norges-bank.no/contentassets/5f4d6b9f67534cdebbd09a29215748bf/20171114_letter.pdf |
| 6 | Norway excluded FTSE "0533 Exploration and Production" to reduce vulnerability to a permanent oil-price decline: proposal 8 Mar 2019; Storting 12 Jun 2019; ≈134 companies, ≈NOK 70bn (≈US$7.9bn, ≈1.2% of equities); later ≈95 companies | Confirmed (press) | 134 companies, NOK 70bn ($7.9bn) and 1.2% of equity holdings are confirmed by press. Reuters gives ≈$7.6bn (NOK 66bn, YE-2018 holdings). The Storting endorsement is Innst. 339 S (2018–2019), 12 Jun 2019. ≈95 companies, ≈NOK 54bn (mid-Sep 2019) per Al Jazeera/Reuters; NBIM's 11 Sep 2019 letter gives "just over 50 billion kroner", 0.8% of the benchmark. The regjeringen.no primary returned 403. | https://oilnow.gy/featured/worlds-largest-sovereign-wealth-fund-to-scrap-oil-and-gas-stocks/ ; https://www.aljazeera.com/ajimpact/norway-sovereign-wealth-fund-divest-oil-explorers-191002094236458.html ; https://www.nbim.no/en/news-and-insights/submissions-to-ministry/2019/energy-stocks-in-the-government-pension-fund-global/ |
| 7 | "A peer with the same economics excluded the **highest-oil-beta** subsector, kept integrated and pipeline exposure" (§4.3 Lesson); "shed the highest-oil-beta subsector (E&P)" (§5.1) | **Corrected** | **In NB Table 2, oil equipment & services has the highest relative oil β (0.61), above E&P (0.54).** Norway excluded E&P only. It kept OES, integrateds (0.36) and pipelines (0.27). NB: services' sensitivity is "slightly greater ... but the difference is not significant". Norway selected by FTSE label, not by measured beta. See R7. | https://www.nbim.no/contentassets/5beb197aa8c544b39fe547e2d6eb3b13/2018-04-26-nb-to-mof-energy-stocks-in-the-gpfg.pdf |
| 8 | IMF WP/10/9: a stabilisation fund's SAA should hold assets negatively correlated with the commodity; reserves in the optimiser force a short oil position; pre-select assets "uncorrelated with or countercyclical to" oil | Confirmed | Verbatim, p. 8: "The SAA of the SWF will, therefore, contain assets that have negative correlation with the respective commodity price." Verbatim, p. 19: "will either force the financial assets into a short oil position or render the analysis meaningless all together", and "select asset classes or currencies which are uncorrelated with or countercyclical to the price of oil", citing Sharpe and Tint (1990). The first author is **Aaron** Brown; January 2010. | https://ideas.repec.org/p/imf/imfwpa/2010-009.html ; https://ifswf.org/media-download/15229 |
| 9 | Jun 2014–Jan 2016: Brent −70%, US market −0.6%, US oil and gas −38.5%, coal −88%, mining −45% [I-calc] | Confirmed (recomputed) | Independent rerun on raw data. Brent month-end $111.03 (Jun-14) → $33.14 (Jan-16) = −70.2%. Over the 19 months Jul-14 to Jan-16: market −0.6%, Oil −38.5%, Coal −88.0%, Mines −44.6%. The window matters: starting one month earlier gives market +2.0% and oil −35.9%. | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html ; https://fred.stlouisfed.org/series/DCOILBRENTEU |
| 10 | OCC: semiannual redeterminations; decks at a discount to the NYMEX strip; advance rates 50–65% of risk-adjusted NPV; over-advances cured in 30 days or repaid over six months; hedges ≤3 years; RBL hedges secured pari passu, margin may be prohibited | Confirmed | Handbook v2.2 (15 Oct 2018). Redeterminations "typically occur semiannually", with 1–2 extra (p. 11). Decks "at a discount to the current NYMEX futures curve" (p. 22). Risk factors 100 / 90–95 / 65–75 / 25–50%; advance 50–65%; non-producing reserves ≤25–35% (p. 24). Cure "within 30 days", else "repay the over-advance evenly over six months" (p. 25). Hedges "tend to be short term with three-year maturities or less" (p. 14). Counterparties "often are secured pari passu"; a "prohibition ... for hedging subject to margin" is listed as an examiner consideration (p. 21). Covenants: debt/EBITDAX 3.5× (≤ 4.0×); interest cover 2.5–3.0×. | https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/files/oil-gas-exploration-prod-lending/pub-ch-oil-and-gas.pdf |
| 11 | Haynes and Boone: spring-2016 borrowing bases expected to fall 38% on average, 79% expecting decreases; fall 2016 a further −20% | Confirmed (qualified) | Spring (25 Jan 2016): anticipated decrease "38 percent" (39% in fall 2015); "an average of 79 percent of the respondents expect borrowers to see their bases decline". Fall (29 Sep 2016): "an average 20 percent decrease from the spring 2016 borrowing bases" (lenders 16%, borrowers 29%), **but respondents "expect 41 percent of borrowers will see a decrease"**. Both releases report survey expectations, not realised cuts. See R6. | https://www.haynesboone.com/press-releases/spring-2016-borrowing-base-redeterminations ; https://www.haynesboone.com/news/press-releases/fall-2016-borrowing-survey |
| 12 | SEC reserves use a 12-month unweighted average of first-day-of-the-month prices (33-8995, effective 1 Jan 2010) | Confirmed | Verbatim: "12-month average price, calculated as the unweighted arithmetic average of the first-day-of-the-month price for each month within the 12-month period". Release Nos. 33-8995; 34-59192; FR-78 (31 Dec 2008); "Effective Date: January 1, 2010". | https://www.sec.gov/rules/final/2008/33-8995.pdf |
| 13 | ARMB legacy energy 0.7% (10y), −1.9% (15y) net at 30 Jun 2026, being wound down; NCREIF Timberland 10y 5.5%; Farmland (80/20) 10y 6.3%; ARMB cut timber 10 → 7% and farmland 25 → 18% of real assets | Confirmed | Packet p. 383, "Sub-Sector Net Performance": Energy 1y 1.6%, 3y −5.2%, 5y −1.4%, 10y 0.7%, 15y −1.9%; relative to CPI+4%, −6.0 to −12.3pp; NCREIF Timberland 10y 5.5%; Farmland 10y 6.3%. Callan's p. 439 table gives 0.73% / −1.88% / 5.54% / 6.27%. "ARMB's Energy exposure (+0.6%) is a legacy position and continues to be wound down." Timber 10 → 7% in FY2026 (p. 462). **Farmland was cut in two steps: 25 → 20% in FY2024, then 20 → 18% in FY2026** (p. 458), "due to lower expected returns and a desire to increase liquidity". | https://treasury.dor.alaska.gov/armb (packet: 2026-09-15-16_armb_bot_packet_v-f-2-day2_only.pdf) |
| 14 | Jefferies H1 2026: commodity volatility raised upstream/NR fund pricing and demand; all-strategy LP average ≈87% of NAV; RE 68%; infrastructure 91% | Confirmed | Verbatim: "Commodity price volatility in the energy markets significantly increased the pricing and demand of upstream and natural resources funds during the period". "Approximately 87% of NAV"; RE 68%; infrastructure 91% (buyout 91%, credit 89%, venture 79%). **No upstream or NR price level is given** (see the spec-card citation note in §4). | https://www.jefferies.com/wp-content/uploads/sites/4/2026/07/Jefferies-Global-Secondary-Market-Review-July-2026.pdf |
| 15 | IEA WEO 2025: STEPS oil peak ≈102 mb/d around 2030; CPS ≈113 mb/d in 2050 (+13% vs 2024) | Confirmed (secondary) | DieselNet (12 Nov 2025): CPS "113 million barrels per day (mb/d) by 2050", ≈13% above 2024. Fortune: STEPS peak "around 102 million barrels per day by 2030". Carbon Brief instead gives CPS "11% above current levels by 2050". iea.org returned 403. | https://dieselnet.com/news/2025/11iea.php ; https://fortune.com/2025/11/12/gas-oil-fossil-fuel-coal-peak-2030-iea-age-of-electricity ; https://www.carbonbrief.org/iea-fossil-fuel-use-will-peak-before-2030-unless-stated-policies-are-abandoned |
| 16 | NGFS Phase V: ≈$300/tCO2 needed by 2035 for net zero by 2050 (≈$50 more than Phase IV); GDP losses 7–15% by 2050 | Confirmed | Verbatim, p. 2: "A carbon price of around $300/tCO2 would be needed by 2035 to incentivize a transition towards net zero by 2050, which is around $50/tCO2 more than in Phase IV." GDP losses "in between 7% and 15% in 2050 in Phase V", measured against a baseline with no climate change. | https://www.ngfs.net/system/files/import/ngfs/media/2024/11/05/ngfs_scenarios_high-level_overview.pdf |
| 17 | Welsby et al. (2021): for a 50% chance of 1.5 °C, 58% of oil, 59% of gas and 89% of coal reserves are unextractable by 2050 | Confirmed | 58% oil, 59% fossil methane gas and 89% coal, on a 2018 reserve base (Nature 597:230–234). The Nature page is paywalled; figures confirmed via the UKERC and ChemistryViews summaries. | https://doi.org/10.1038/s41586-021-03821-8 ; https://ukerc.ac.uk/news/unextractable-fossil-fuels-in-a-1-5c-world/ |
| 18 | Wheaton–BHP (Feb 2026, silver): $4.3bn upfront plus 20% of spot | Confirmed | Announced 17 Feb 2026, completed 2 Apr 2026. US$4.3bn upfront; "20 per cent of the spot silver price" per ounce; 33.75% of Antamina silver (90% payable) until 100 Moz, then 22.5%. | https://www.bhp.com/news/media-centre/releases/2026/02/bhp-enters-into-a-silver-streaming-agreement |
| 19 | The owner draw is a NAV-scaled short oil put spread: ≈$200m per $1/bbl in band; kinks ≈$67/$23 (linear) and ≈$64/$31 (log) at P^BE $44.8; overlay put spreads ≈20–40m bbl [C] | Confirmed (internal) | Matches `research/00_SYNTHESIS.md` (lines 405, 992, 1067). In `g12_wrongway_sim.py` the linear map gives 0.00625 × 11.3 / 62.2 × $177bn = $0.201bn per $1/bbl. That is the 8pp fiscal-balance band, ≈$44 wide, worth $8.85bn. The 201m bbl is the *static* d* map; with smoothing the first-year delta is ≈100m bbl (synthesis §4.7). | research/00_SYNTHESIS.md |
| 20 | L_eff: 7.5–9.9% of NAV (P^BE $45–65); 7.1–9.3% (h 6–15%); 9.3 → 10.0% (b doubled); 4.8% (P^BE $35) [I-MC] | Confirmed (reproduced) | JSON: 7.47 / 9.25 / 9.90; 7.11–9.33; 9.30 → 9.97; 4.80. The arithmetic b·h·P(in band)·2.304 checks. The formula omits the ρ = 0.5 draw smoothing (×0.946, so ≈5% lower). Conclusions are unchanged (R9). | research/groups/addenda/G12_calcs/g12_hedging_demand_results.json ; g12_low_breakeven_check_results.json ; g12_slope_check_results.json |
| 21 | Unlevered upstream distributions 0.43× / 0.49× in SG/DB; 40%-LTV cure calls in 73% / 69% of SG/DB years, mean 18–20% of equity; owner hurdles at γ 2–4: 1.2–2.4% / 2.4–4.8% / 0.5–0.9% / 0.3–0.6% [I-MC] | Confirmed (reproduced) | JSON (P^BE $55, log): cash_vs_N 0.43 / 0.488. Cure probability 0.733 / 0.692; mean when called 0.180 / 0.198. Hurdles 1.20–2.39%, 2.38–4.76%, 0.46–0.93%, 0.31–0.62%. Method caveats: R4, R5. | research/groups/addenda/G12_calcs/g12_wrongway_sim_results.json ; g12_hedging_demand_results.json |
| 22 | Synthetic $2.5bn sleeve: ≈12.2m bbl (31–61% of a 20–40m bbl programme); ≈6.1m after a 70% 3-year asset-level hedge; SG one-year loss ≈$0.68bn (≈$0.96bn on the 2014–16 analogue) [I-calc] | **Corrected (basis and method)** | The numbers reproduce from the JSONs, but four qualifications apply. **(a)** 12.2m uses N-state elasticities at $70; at the same JSON's GW/$95 elasticities the sleeve is ≈9.2m bbl (R2). **(b)** "≈6.1m after hedge" assumes the fund-held $0.80bn is hedged at asset level; hedging only the direct $0.27bn gives ≈10.7m bbl (R1). **(c)** The "$0.96bn analogue" is $2.5bn × −38.5%: the listed oil industry's *19-month* return applied to the *whole* sleeve, including $0.85bn of fee midstream. It is not a one-year, segment-consistent loss (R10). **(d)** "31–61%" compares delta with notional (R3). | research/groups/addenda/G12_calcs/g12_enr_book.py ; g12_enr_book_results.json ; g12_check_hedged_sleeve_results.json ; g12_wrongway_sim_results.json ("GW_at_95") |
| 23 | Energy fund LP interests at ≈41% of NAV in a March 2020 buyer survey (Setter Capital); bids 40–70% of NAV in busts | Unverifiable | Already tagged [U] by the dossier. Search found only the paywalled Secondaries Investor survey article, which gives buyout, VC and fund-of-funds pricing, not energy. Keep [U]. It feeds the SELL economics and the OC row ("40–60%"). | https://www.secondariesinvestor.com/market-will-take-nine-months-to-return-to-normal-survey/ |

### Supplementary spot checks

| # | Claim | Verdict | Note | Source URL |
|---|---|---|---|---|
| S1 | Harvard marked natural resources down ≈$1.1bn to ≈$2.9bn in FY2017 (§5.3) | Confirmed | Bloomberg (26 Oct 2017): revalued to "$2.9 billion from $4 billion". The Crimson says ≈$1bn; Harvard Magazine gives FY2016 NR at $3.6bn. | https://www.bloomberg.com/news/articles/2017-10-26/harvard-endowment-hit-by-1-billion-natural-resources-writedown |
| S2 | CA median TVPI ≈1.09× for 2012-vintage NR funds vs ≈1.40× for 2015; NSHE legacy NR funds at 1.48–1.50× ("our reading of the table columns") | Confirmed | INV-6 legacy NR table. Commonfund Capital NR IX (2012): TVPI 1.50 vs CA median 1.09. NR X (2015): 1.48 vs 1.40. Both second quartile; both are fund-of-funds vehicles. The column reading is consistent with the DPI pairs (0.66/0.68; 0.64/0.76). | https://nshe.nevada.edu/html/wp-content/uploads/file/BoardOfRegents/Agendas/2025/03-mar-mtgs/refs/inv/INV-6.pdf |
| S3 | The UAE left OPEC on 1 May 2026 (§4.6, [C]) | Confirmed | Announced 28 Apr 2026; exit from OPEC and OPEC+ effective 1 May 2026. | https://www.enerdata.net/publications/daily-energy-news/uae-announces-exit-opec-effective-1-may-2026-after-59-years.html |
| S4 | Brent $126.55 on 14 Oct 2026 (§4.2) | Confirmed | EIA RBRTE via FRED: 14 Oct 2026 = 126.55. | https://fred.stlouisfed.org/series/DCOILBRENTEU |
| S5 | Episode table (Jun08–Feb09, Dec19–Mar20, 2022, Feb–Aug 2026) and max drawdowns since 1988 [I-calc] | Confirmed (recomputed) | Every cell reproduces. Examples: 2022 oil +65.2%, coal +100.1%, market −19.9%; Feb–Aug 2026 Brent +25.8%, oil +17.8%, market +12.3%. Max drawdowns: oil −64.8%, coal −98.7% (Mar 2020), mines −66.4%, gold −77.7%, utilities −37.9%, Brent −89.3%. | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html |
| S6 | Full-sample partial oil betas (§4.2 table) [I-calc] | Confirmed (≈) | Rerun with Newey–West (3), Jan 1988–Aug 2026. Oil 0.223 (0.026) vs 0.23 (0.025); coal 0.244 (0.049) vs 0.27 (0.046); mines 0.091 vs 0.10; gold 0.089 vs 0.09; utilities 0.014 vs 0.02; paper −0.028 vs −0.03; agriculture 0.032 vs 0.03. All are within one s.e.; the small gaps are likely month-end or sample conventions. | (as S5) |

---

## 3. Reproducibility of [I-calc] / [I-MC] numbers

- **Recomputed from raw public data:** episode returns (6 windows), max drawdowns, partial oil betas and the Brent level. Every cell matches to rounding (S5, S6, #9).
- **Traced to the JSONs:**
  - L_eff, hurdles, minimum-variance hedge weights and the oil-delta budget conversions ($0.9–1.8bn unlevered, $0.5–1.1bn levered, $2.4–4.8bn hedged, $1.2–2.3bn royalties, $3.6–7.1bn midstream);
  - cash ratios by state, cure statistics, overlay collateral flows, owner-state haircuts (6.1% PDP, 12.2% levered, 2.1% equities at κ = 1) and their invariance to h;
  - stationary Z shares (SG + DB 22.5%, GW 3.8%) and the 35% GW → SG transition;
  - sleeve deltas, the SG loss, put-spread payoffs ($19/bbl × 20–40m) and costs ($3.05–13.05/bbl).
  - All match.
- **Small transcription points:**
  - "3–5× the Gintschel–Scherer hurdle" holds for PDP (2.6–5.1×) but not for equities (≈4–9×).
  - The overlay-collateral tail quoted in the spec card (P05 −15% in GW/SS) omits the worst state: B, P05 −20.3% (R14).

---

## 4. Citation check

| Reference (as listed) | Exists | Authors / year / title / venue check | Verdict |
|---|---|---|---|
| Brown, Papaioannou & Petrova (2010), IMF WP/10/9 | Yes | **Aaron** Brown, Michael Papaioannou, Iva Petrova; January 2010; *Macrofinancial Linkages of the Strategic Asset Allocation of Commodity-Based Sovereign Wealth Funds* | Correct |
| Gintschel & Scherer (2008), *JAM* 9(3) 215–238 | Yes | Andreas Gintschel, Bernd Scherer; "Optimal asset allocation for sovereign wealth funds"; doi 10.1057/jam.2008.19 | Correct |
| van den Bremer, van der Ploeg & Wills (2016), *EER* 82, 113–131 | Yes | Ton van den Bremer, Frederick van der Ploeg, Samuel Wills; "The elephant in the ground" | Correct |
| Norges Bank (14 Nov 2017) letter | Yes | Signed Olsen and Slyngstad; "Investment strategy for the Government Pension Fund Global" | Correct |
| Norges Bank (26 Apr 2018), "Energy stocks in the GPFG" | Yes | Signed Olsen and Slyngstad; replies to the Ministry's 13 Feb 2018 letter | Correct |
| OCC (2018), *Comptroller's Handbook: Oil and Gas E&P Lending* (v2.2) | Yes | Version 2.2, 15 Oct 2018 | Correct |
| SEC (2008), Release 33-8995 | Yes | *Modernization of Oil and Gas Reporting*; 31 Dec 2008; effective 1 Jan 2010 | Correct |
| Meketa (Mar 2024), *Private Natural Resources* | Yes | Contributors Toczylowski, Chew, Giordano, Riela, Benham | Correct |
| Cambridge Associates (20 Sep 2017; 21 May 2020) | Yes | Both titles and dates match; no individual authors credited | Correct |
| Welsby, Price, Pye & Ekins (2021), *Nature* 597, 230–234 | Yes | Issue 7875; doi 10.1038/s41586-021-03821-8 | Correct |
| McGlade & Ekins (2015), *Nature* 517, 187–190 | Yes | Issue 7533; doi 10.1038/nature14016 | Correct |
| Semieniuk et al. (2022), *Nat. Clim. Change* 12, 532–538 | Yes | 10 authors; issue 6. The abstract gives magnitudes the dossier left [U]: lost upstream profits ">US$1 trillion"; a ">15%" net transfer of risk to OECD investors | Correct |
| Jin & Jorion (2006), *JF* 61(2) 893–919 | Yes | Yanbo Jin, Philippe Jorion | Correct |
| Schwartz & Smith (2000), *Mgmt Sci* 46(7) 893–911 | Yes | Eduardo S. Schwartz, James E. Smith | Correct |
| Alhassan, Brake, Papaioannou & Skancke (2018), IMF WP/18/26 | Yes | Abdullah Alhassan, Sue Brake, Michael G. Papaioannou, Martin Skancke | Correct |
| van den Bremer & van der Ploeg (2013), *IMF Econ. Rev.* 61, 130–167 | Yes | Issue 1 | Correct |
| Wan, Mei, Clutter & Siry (2013), *Forest Science* 59(1) 93–104 | Yes | Authors and pages match | Correct |
| Washburn & Binkley (1993), *Land Economics* 69(3) 215– | Yes | Courtland L. Washburn, Clark S. Binkley; "Do forest assets hedge inflation?" | Correct; the page range is incomplete in the dossier and in the registries |
| Insley & Rollins (2005), *AJAE* 87(3) 735–755 | Yes | Full title ends "…: A Linear Complementarity Formulation" | Correct |
| Brennan & Schwartz (1985); Kilian (2009) | Not re-fetched (API rate limit) | Standard citations; details look right | Not re-checked |

**Citation problems:**
1. **Missing or orphan references.**
   - **Scherer (2009, 2011)** is cited in §2.1 but absent from §10.
   - **Kilian (2009)** is listed in §10 but never cited in the text.
   - **Paddock et al.** is cited [U] with no reference entry.
   - Sharpe & Tint (1990) is cited only through the IMF paper.
2. **The spec card over-attributes a secondary price level.** It tags "LP secondary ≈85–95% of NAV in N/GW (H1 2026 strong [S])" to Jefferies. Jefferies gives only a *direction* for upstream/NR funds (the all-strategy average is 87%). Tag the level [I].
3. **Haynes and Boone's "79%" is an averaged expectation.** The spring release's wording is "an average of 79 percent of the respondents expect borrowers to see their bases decline"; the fall release restates the metric as the expected share of borrowers facing a decrease (41%).
4. **Some figures rest on press.**
   - Norway: Reuters gives NOK 66bn / $7.6bn against NOK 70bn / $7.9bn.
   - IEA: STEPS ≈102 mb/d is from Fortune; CPS is +13% vs 2024 (DieselNet) or +11% vs "current" (Carbon Brief).
   - Welsby et al.: the percentages come from summaries; the Nature page is paywalled.
5. **ARMB** was verified against a locally held extract of the day-2 packet. The figures sit on packet pp. 383, 439, 458 and 462, inside the range the dossier cites (pp. 383, 457–462). The farmland cut was two steps (FY2024, FY2026), not one.

---

## 5. Reasoning issues and overclaims in the design implications and specification card

| # | Severity | Where | Problem | Fix |
|---|---|---|---|---|
| R1 | **High** | §1 item 6(c), (e); §6.7 HEDGE and REFINANCE; §6.10; C2; spec card "Action definitions" | **These actions are not available to ADIC as LP.** Asset-level hedges, RBL terms, stream/VPP sales and cure decisions belong to the GP for closed-end fund interests. Those are $1.6bn of the $2.5bn synthetic sleeve, including $0.80bn of the $1.07bn levered upstream (`g12_enr_book.py`). As LP, ADIC can select managers, negotiate side letters, sell the interest or hedge in the overlay (margined). Hedging only the direct levered $0.27bn leaves ≈10.7m bbl, still above the hard limit. JV positions depend on the governance rights in each JV. | Split the action set by vehicle: fund / co-investment / JV / direct operated / direct non-operated. Make C2 a manager-selection and side-letter criterion for funds. Restate 6(c): SELL fund-held upstream into the GW bid, or overlay-hedge the fund-held delta; asset-level hedging applies to direct positions only. Answer §9 Q3 (hedging permissions) before 6(c)/(e) go to the IC. |
| R2 | Medium-high | §1 item 6(b)–(c); §4.8; §6.10; test 7.9(d) | **"Breaches the hard limit" holds only at the $70 N reference.** C1 is measured "at the generator's current state", and E8 divides by P_t, yet the 12.2m bbl uses N-state elasticities at $70. The same JSON's GW/$95 elasticities give ≈9.2m bbl for the same $2.5bn NAV: within the hard limit, above the soft one. The barrel delta is roughly price-invariant only if NAV is re-marked, so the answer hinges on the price at which the synthetic $2.5bn is struck. That price is not stated. | State the price basis of the synthetic NAV. Compute Δ_RA at the current state, as C1 requires, and at a stressed state. Report breach status by state. |
| R3 | Medium | §1 item 6(c); §4.8 table; E8; C1 rationale; §6.6 c^hedge | **Delta is compared with notional.** "Offsets 31–61% of the 20–40m bbl put-spread programme" divides spot-equivalent delta by option notional. At forwards of $70–84 and vol of 35–70%, the 64/31 spread's forward delta is 0.16–0.31 per bbl. The generator moves the 1-year forward by 0.6% per 1% spot, so the programme carries ≈2–8m bbl of spot-equivalent delta and the sleeve holds ≈1.2–6× that. At $45 in SG, the sleeve's loss ($0.68–0.96bn) is 0.9–2.5× the payoff ($0.38–0.76bn). "Neutralising the delta with put spreads" (1.5–6.4% of NAV a year) buys protection between $64 and $31, not delta neutrality. E8's "Σδ − hedges" must convert swap and option notionals to spot-equivalent deltas (φ^k weights), or 2–3-year hedges are over-credited. | Compare like with like: spot-equivalent deltas, or scenario P&L at $45 and $31. Define the hedge credit in E8. Relabel the carry figure as protection cost. |
| R4 | Medium | §1 item 2; §4.8; E3 ("residual is an equity cure call on ADIC"); C3; spec card cash flows | **Cures are modelled as mandatory cash calls.** RBLs are normally non-recourse (§9 Q4 expects none), so curing is an option: inject equity, or accept restructuring or foreclosure. For fund-held assets, any call is a GP decision bounded by unfunded commitments. The −0.29× net cash and the 73% cure frequency assume every over-advance is defended. Two simulation features raise call frequency. Debt is never amortised except through over-advance repayments, so depletion drift alone triggers calls (the 9% N-state rate, conceded in the dossier). Initial borrowing-base utilisation is 78% (D = 0.40V against BB = 0.51V), so any fall of ≈22% in model PV creates an over-advance. Any part that year's cash cannot cover becomes an equity call. | Model the cure as an option: defend if post-cure equity value exceeds the cure, with a strategic-override flag. Cap fund-level cures at unfunded commitments. Show the walk-away loss alongside. Add RBL amortisation. |
| R5 | Medium | §6.5 C3; spec card liquidity row | **The Tier-1 reserve is sized at the mean.** 0.73 × 0.18 = 13% is the SG-conditional *mean* cure: calls occur in 73% of SG paths, averaging 18% when made. Roughly half of SG outcomes exceed it. | Use a tail quantile of the SG/DB cure distribution (e.g. P90), or at least the conditional-on-call mean of 18–20% (≈$0.19–0.21bn on $1.07bn). Publish the distribution from `g12_wrongway_sim.py`. |
| R6 | Low-medium | §4.4; §6.7 REFINANCE ("shrinks ≈38%"); §6.9 OC row ("−38%, then −20%"); calibration target 6 | **Survey expectations are used as realised calibration.** Both numbers are respondents' expectations. The fall-2016 survey expected only 41% of borrowers to see any decrease (lenders −16%, borrowers −29%), so a blanket second round of −20% overstates. | Label them as expectations. Calibrate to realised redeterminations where available. Apply the second round to a fraction of borrowers. |
| R7 | Low-medium | §4.3 Lesson; §5.1 | **Norway lesson misdrawn** (claim #7). Norway excluded E&P by FTSE label and kept the higher-beta services subsector, although the difference was insignificant. | Rephrase. Present "classify by oil beta" as the dossier's own design choice, supported by NB's betas, not as Norway's practice. |
| R8 | Low-medium | §1 item 3; §6.4 ("Gintschel–Scherer hurdle ... IC-readable number"); §6.10 | **Mislabelled hurdle.** The Gintschel–Scherer hedging demand (formula in §2.1) uses the owner's subsoil wealth relative to the fund (V^oil/F). The dossier's hurdle uses L_eff, ADIC's draw liability of ≈0.09 of NAV. Consolidating Abu Dhabi's subsoil wealth would produce the very large short-oil demand the IMF warns about, which is why the dossier sensibly uses the draw. The resulting number is not a Gintschel–Scherer hurdle. | Rename it (e.g. "draw-surplus hurdle"), state the ADIC-standalone perspective explicitly, and keep GS for the owner-level discussion only. |
| R9 | Low | §2.1 L_eff formula; C1 L_eff,t | **L_eff omits draw smoothing (ρ = 0.5).** The PV impulse should be scaled by (1−ρ)/(1−ρ/(1+r)) = 0.946, so L_eff is ≈5% too high. P(in band) is taken from the stationary distribution, not conditional on today's state, although C1 writes L_eff,t. | Include the smoothing factor. Compute a state-conditional L_eff,t. |
| R10 | Low-medium | §1 item 6(c); §4.8 | **The "2014–16 analogue" ($0.96bn) is not a one-year, segment-consistent loss.** It applies a 19-month industry return uniformly to all segments, including midstream. | Use a segment-level analogue (the dossier's own OC marks give ≈$0.9bn) and label it a 19-month episode. |
| R11 | Low | §2.4; §6.8(iii); E6 | **The SEC/PV-10 bias is not only a lag.** SEC prices are held flat over reserve life. In today's steep backwardation (spot $126.55 against the $84 2027 proxy in `g12_enr_book.py`), flat 12-month-average pricing can overstate value against the strip by more than the six-month lag does. | Correct for curve shape as well as lag: re-price on E1 or the ICE strip. |
| R12 | Low-medium | §6.6 objective; C1 | **Oil risk is charged three times.** H_j already prices covariance with the draw; c^hedge·(Δ_RA − B_oil)⁺ charges the same delta again above budget; C1 then caps it. The objective does not say which H enters J (GS, H^d or H^λ) or which B_oil (soft or hard) the penalty uses. | Choose one pricing channel plus the hard cap. Specify H and B. |
| R13 | Low | Spec card, liquidity row | **"≈85–95% of NAV in N/GW [S]"** is an inference from a directional statement (see §4, citation problem 2). | Tag it [I]. |
| R14 | Low | Spec card; §6.7 HEDGE | **The overlay-route collateral tail omits the worst state.** It cites "P05 −15% in GW/SS", but the JSON's worst P05 is the boom state B (−20.3%), with N at −13.4%. | Size the collateral pool on the B-state tail. |
| R15 | Low | §6.10 "Order of magnitude" | **The NBIM comparison is not like for like.** ADIC's retained cap (≈0.3–0.6% of NAV) is compared with NBIM's *excluded* E&P (≈1.2% of equities). Norway kept ≈4.6% of equities in other oil and gas (sector 5.84% at Feb 2018, less E&P). | Compare retained oil exposure with retained oil exposure. |

**What survives.** The core economics hold:
- the draw as a short put spread;
- wrong-way risk concentrated in SG/DB cash and refinancing capacity;
- private energy's weak post-2013 record;
- band saturation of L_eff;
- the procyclicality of REFINANCE and LEVER in ENR;
- the transition drift on the long-run oil factor.

All are well supported by the verified sources and the reproduced calculations.

---

## 6. Overall reliability

**MEDIUM.**
- **Sourced facts: high.** 23 of 25 external claims (main table plus spot checks) are confirmed, mostly verbatim; one narrative claim is corrected (Norway); one figure is already [U] and stays unverifiable.
- **Reproducibility: high.** Every [I-calc] and [I-MC] number reproduces.
- **Before the IC sees the ENR recommendation**, restate:
  - the synthetic-sleeve breach, with its price basis and current-state delta (R2);
  - the HEDGE route, split by vehicle with LP-feasible actions (R1);
  - the put-spread offset ratio (R3);
  - the cure-call treatment and the C3 reserve (R4, R5).
