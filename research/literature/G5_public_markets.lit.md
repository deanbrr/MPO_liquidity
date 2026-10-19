# G5 literature check: Public Markets (hedge funds and long-only managers)

**Dossier checked:** `research/groups/dossiers/G5_public_markets.md` (prepared 2026-10-18). The dossier was not edited.
**Companion:** `research/groups/verification/G5_public_markets.verify.md` (verification log, "VL" below).
**Date:** 2026-10-18.

**Organizational mapping (user-confirmed, 2026-10-18).**
- The Public Markets group invests through external managers: hedge funds and long-only managers, via funds, SMAs or managed accounts. When long-only beta is replaced synthetically, the Overlay (group 7) executes the trade.
- **Corporate Finance owns Treasury.** That covers the liquidity buffer, the contingency funding plan, internal transfer pricing (FTP), portfolio-level facilities, overlay collateral and owner distributions. Papers below on futures financing, prime-broker and TRS counterparty risk, and HQLA backing therefore bear on Corporate Finance's constraints, not only on the group's.
- The Secondaries group is a hybrid of direct and fund investments. Its overlap with G5 is limited. The dossier's hedge-fund secondary-sale option (SELL) prices hedge-fund interests, a different market from the PE secondaries that group trades (studied by Ramadorai 2012).

> **IMPORTANT: Consensus was unavailable in this session.**
> - My first Consensus `search` returned a monthly-quota error. I waited 30 seconds and retried twice, as the protocol requires. Both retries returned the same message, reproduced verbatim in §6.
> - I made no further Consensus calls. The quota is account-level and resets on 1 November 2026.
>
> **What I used instead.** Every search was a plain query with no year, type, venue or citation filters, the same rule as for Consensus.
> 1. **OpenAlex API** (one of Consensus's three source indexes). It answered 7 queries, then returned HTTP 429: the daily free budget was exhausted, with Retry-After 48,667 s.
> 2. **Semantic Scholar API** (another Consensus source index). Its search endpoint was rate-limited (429) throughout. Title matching answered 6 of 7 requests, and one batch lookup succeeded, which supplied abstracts.
> 3. **Crossref REST API** (`query.bibliographic` search and DOI lookup). Every request was answered, so Crossref was the main engine: all 14 topical backfill searches and most metadata checks.
> 4. **Consensus records that other agents retrieved earlier today**, copied character for character from their files. No URL was modified or regenerated.
>
> **No new Consensus URLs exist for this file.** Where no sibling Consensus record exists, the link given is the DOI exactly as Crossref returned it (behind the standard `https://doi.org/` resolver), or the OpenAlex ID as returned.
>
> **Reading conventions.**
> - Findings restate retrieved abstracts only. [WP abstract] means the abstract is from the working-paper version, so its numbers may differ from the published article.
> - **[Inference]** marks anything beyond an abstract.
> - Citation counts: **CR** = Crossref `is-referenced-by-count`, **OA** = OpenAlex, **S2** = Semantic Scholar, all as of 2026-10-18.

**Provenance tags**

| Tag | Source |
|---|---|
| **[VL]** | Consensus URL recorded in the G5 verification log |
| **[P04] / [P05] / [P06] / [P09]** | Consensus record in `research/literature/04_pe_cashflows`, `05_secondaries_navfin`, `06_leverage` or `09_overlay` `.lit.md` |
| **[P01-09]** | The same Consensus record appears in streams 01, 02, 04, 06, 08 and 09 |
| **[CR]** | Crossref API, queried in this session |
| **[OA]** | OpenAlex API, queried in this session |
| **[S2]** | Semantic Scholar API, queried in this session |

---

## 1. Summary

### Citation integrity
- **49 academic works checked.** That is every academic reference in the dossier: the 39 in §10 "Read in this session", the 9 academic items in the [nrv] list, and Dimmock, Wang & Yang (2024), which §2.8 cites "via 06".
  - **Table A** covers the 25 most load-bearing: the works that feed return equations, liquidity terms, parameters or calibration targets.
  - **Table B** covers the other 24.
- **Result: 48 found, 1 mismatched, 0 not found.** No fabricated or garbled references.
  - **The one mismatch is minor.** Almgren & Chriss is cited as 2000 in *J. Risk*. Crossref dates it 2001, *J. Risk* 3(2):5–39.
- **Minor metadata notes (not errors).**
  - Four titles are shortened: Barras et al. 2010, Chen–Goldstein–Jiang 2010, Bollen & Pool 2009 and Jagannathan et al. 2010.
  - Five entries lack volume or pages: Ben-David–Birru–Rossi (RCFS 15(3):704–747), Brooks et al. (JFI 29(4):5–19), Asness et al. (JPM 28(1):6–19), Pástor et al. (JFE 116(1):23–45) and Getmansky–Lee–Lo (ARFE 7(1):483–577).
  - Dao et al. (arXiv 2016) was later published in *J. Investment Strategies* 7(1), 2017.
- **Five [nrv] items now have verified bibliographic records:** Kosowski–Naik–Teo (JFE 84(1):229–264), Jenkinson–Jones–Martinez (JF 71(5):2333–2370), Rattray et al. (JPM 46(6):10–31), Davis & Norman (MOR 15(4):676–713) and Geltner (JRER 8(3):325–345).
  - Granger et al. (2014) is "Rebalancing Risk" (SSRN), by Granger, Greenig, Harvey, Rattray & Zou.
  - Grinold & Kahn is a book. Crossref indexes only a 1996 *JF* record for the first edition, so it is confirmed indirectly.
- **Consensus and the GLM paper.** Consensus does not index the *JFE* record of Getmansky–Lo–Makarov (streams 04 and 09 found only Getmansky's thesis). Crossref and OpenAlex both confirm the dossier's metadata.
- **Agreement with the verification log.** This independent check agrees with the VL's citation section (§3: "no hallucinated or garbled citations").

### Backfill: what the dossier misses
I ran 14 topical searches (Crossref; Semantic Scholar search was blocked) and 44 title lookups for candidates. Section 3 annotates 25 papers, none cited in the dossier. The main gaps:

1. **Fragility evidence beyond contractual terms.**
   - An empirical mismatch measure, the "illiquidity gap" (Agarwal, Aragon & Shi 2019).
   - Funding risk that changes as the investor base's lock-ups expire (Aiken et al. 2021).
   - The cost of permissive liquidity, about 1.7% a year, and the share of smoothing due to managerial reporting, 33% (Cao et al. 2017, managed-account platform).
   - Direct evidence that gates *amplify* runs (Li et al. 2021, money-market funds).
2. **Hedge-fund stress that does not come from redemptions.**
   - In the 2020 Treasury-market shock, hedge funds cut arbitrage and raised cash despite stable credit and low redemptions; internal VaR constraints were binding (Kruttli et al. 2025).
   - Prime-broker failure and credit supply (Aragon & Strahan 2012; Li, Monin & Petrasek 2024).
3. **How hedge-fund alpha is measured, and its decline.**
   - Returns look like put-writing (Jurek & Stafford 2015).
   - Fung–Hsieh-type models are "as misspecified as the CAPM"; momentum, variance and carry factors lower measured performance (Ardia et al. 2024).
   - Hedge funds have not improved portfolio Sharpe ratios since 2008 (Bollen et al. 2021).
   - Persistence has been eroded by decreasing returns to scale and survives only under Bayesian alpha (Bollen et al. 2026, *CFR*).
4. **Capacity theory.** Berk & Green (2004) is the seminal model the dossier's α(AUM) equation rests on, and it is uncited. Also missing: managers' incentive to outgrow optimal size (Yin 2016) and fund-specific scalability (Barras, Gagliardini & Scaillet 2022).
5. **Data-quality methods.**
   - Backfill must be removed by listing date, not by truncation (Jorion & Schwarz 2019).
   - Return histories are revised, and revisers underperform (Patton et al. 2015).
   - Stylized facts depend on which database is used (Joenväärä et al. 2021).
6. **Long-only evidence beyond US mutual funds.**
   - Institutional accounts beat benchmarks by 31bp net, but through factor exposures (Gerakos et al. 2021).
   - Active management paid in emerging markets for pension plans (Dyck, Lins & Pomorski 2013).
   - The false-discovery-rate method is underpowered (Andrikogiannopoulou & Papakonstantinou 2019).
7. **Implementation.**
   - The futures–cash basis prices liquidity demand and is persistent (Hazelkorn et al. 2023).
   - Predictable institutional rebalancing is costly and gets front-run (Harvey, Mazzoleni & Melone 2025).
8. **Surveys:** Agarwal, Mullally & Naik (2015) for hedge funds; Cremers, Fulkerson & Riley (2019) for active management.

**Gaps in the literature itself.** No academic paper surfaced on two topics: multi-manager pass-through fee economics, and physical-to-synthetic replacement policy for asset owners. For both, the dossier's practitioner sources (CA, Barclays, D. E. Shaw, CME) remain the best available.

### Challenges (detail in §5)
The literature most directly challenges nine dossier positions:
1. Positive net-alpha priors for hedge funds (§6.11; multi-strategy +2.0%).
2. The Fung–Hsieh + put + liquidity factor set as the return model (§6.4).
3. The "about 75% zero-alpha / net α ≈ 0" anchor for long-only, and false-discovery-rate (FDR) control as the skill test (§1.6, §6.14).
4. Applying the consultant-bias correction to hedge-fund mandates (§6.14).
5. The GPFG-style month-end 2pp rebalancing trigger (§6.9).
6. A hedge-fund stress model built mainly around redemptions (§6.5).
7. Reliance on persistence among superior hedge funds (§4.6).
8. Fixed "classic" backfill and survivorship haircuts as the bias correction (§4.6, §6.14).
9. Square-root liquidation costs with no crowding term (§4.9, §6.8).

There is also supporting evidence:
- Li et al. (2021) gives empirical backing to the dossier's preemptive-run term.
- Dyck et al. (2013) supports the positive emerging-market long-only prior that the VL questioned (R9).

---

## 2. Citation-integrity tables

Status key:
- **found**: the metadata match the version cited.
- **found (note)**: correct, with a version or completeness note.
- **mismatched**: exists, but the metadata differ; corrected metadata given.

The "Consensus URL" column shows a sibling Consensus record where one exists. "n/a" means no Consensus record was available (quota exhausted). The verifying record (Crossref, OpenAlex) is given in the metadata column.

### Table A: the 25 most load-bearing references

| # | Dossier citation | Status | Corrected / confirmed metadata (verifying record) | Consensus URL |
|---|---|---|---|---|
| A1 | Getmansky, Lo & Makarov (2004), *JFE* 74(3), 529–609; NBER WP 9571 (GLM smoothing, §2.2, §6.4) | found | Confirmed *JFE* 74(3):529–609, DOI https://doi.org/10.1016/j.jfineco.2004.04.001; CR 790 cites; OA [W3124792793](https://openalex.org/W3124792793), 999 cites. NBER: https://doi.org/10.3386/w9571 [CR, OA] | Consensus indexes only Getmansky's 2004 thesis, which carries the same abstract [P04; stream 09 reports the same]: [thesis record](https://consensus.app/papers/details/4e43d079332f5046860f2f39350f56f9/?utm_source=claude_desktop) |
| A2 | Fung & Hsieh (2004), "Hedge fund benchmarks: A risk-based approach", *FAJ* 60(5), 65–80 (factor model) | found | DOI https://doi.org/10.2469/faj.v60.n5.2657; CR 831; OA [W2039352825](https://openalex.org/W2039352825), 1,028 [CR, OA] | n/a |
| A3 | Agarwal & Naik (2004), *RFS* 17(1), 63–98 (option-like payoffs) | found | DOI https://doi.org/10.1093/rfs/hhg044; Crossref issue date 2003 (online); CR 923; S2 1,263 [CR, S2] | [record](https://consensus.app/papers/details/6c11eda0862b5ed6b3244b0e9d97c335/?utm_source=claude_desktop) [P09; labelled "2003/2004"] |
| A4 | Fung & Hsieh (2001), *RFS* 14(2), 313–341 (trend factors) | found | DOI https://doi.org/10.1093/rfs/14.2.313; CR 971 [CR] | n/a |
| A5 | Ang & Bollen (2010), *Financial Management* 39(3), 1069–1096 (redemption real option) | found | DOI https://doi.org/10.1111/j.1755-053x.2010.01104.x; CR 47; OA [W3122111947](https://openalex.org/W3122111947), 62. The Crossref abstract confirms "approximately 1%" (two-year lock-up, three-month notice, CRRA 3) and "can easily exceed 10%" under arbitrary suspension [CR, OA] | n/a. The VL confirmed it in Consensus but did not record the URL |
| A6 | Aragon (2007), *JFE* 83(1), 33–58 (lock-up premium; "4–7%" was [nrv]) | found | DOI https://doi.org/10.1016/j.jfineco.2005.11.001; CR 373; OA [W2118205861](https://openalex.org/W2118205861) (online year 2006), 499 [CR, OA]. The Consensus abstract gives "approximately 4-7% per year" (VL), which resolves the [nrv] flag | [record](https://consensus.app/papers/details/c4b55868f55556a9a6e48db4a364822a/?utm_source=claude_desktop) [VL] |
| A7 | Aiken, Clifford & Ellis (2015), *JFE* 116(1), 197–218 (discretionary liquidity restrictions) | found | DOI https://doi.org/10.1016/j.jfineco.2015.01.002; CR 57. WP title "Discretionary Liquidity: Hedge Funds, Side Pockets, and Gates" (SSRN 2012, https://doi.org/10.2139/ssrn.2185999) [CR] | n/a. VL confirmed in Consensus; URL not recorded |
| A8 | Cipriani, Martin, McCabe & Parigi (2014), "Gates, fees, and preemptive runs", FRBNY SR 670 (preemption term) | found (note) | Also Fed Board FEDS 2014-030, https://doi.org/10.17016/feds.2014.030 (CR 7), and SSRN https://doi.org/10.2139/ssrn.2434524 (CR 23). No journal version found. It is a theoretical model framed around money funds (VL R9); see Li et al. 2021 (§3, #4) for empirical support [CR] | n/a |
| A9 | Chen, Goldstein & Jiang (2010), "Payoff complementarities and financial fragility", *JFE* 97(2), 239–262 | found (title shortened) | Full title adds ": Evidence from mutual fund outflows". DOI https://doi.org/10.1016/j.jfineco.2010.03.016; CR 634 [CR] | n/a |
| A10 | Ben-David, Franzoni & Moussawi (2012), *RFS* 25(1), 1–54 (2008 selling; redemption intensity) | found | DOI https://doi.org/10.1093/rfs/hhr114; Crossref issue date 2011 (online); CR 360 [CR] | n/a |
| A11 | Ben-David, Birru & Rossi (2020/2026), NBER w27454; *RCFS* 15(3) (effective incentive fee ≈ 50%) | found (add pages and DOI) | *Review of Corporate Finance Studies* 15(3):704–747 (2026), DOI https://doi.org/10.1093/rcfs/cfag015; NBER https://doi.org/10.3386/w27454 (CR 18) [CR] | n/a |
| A12 | Dichev & Yu (2011), *JFE* 100(2), 248–263 (dollar-weighted returns) | found | DOI https://doi.org/10.1016/j.jfineco.2011.01.003; CR 123 [CR] | n/a |
| A13 | Aggarwal & Jorion (2010), "Hidden survivorship in hedge fund returns", *FAJ* 66(2), 69–74 | found | DOI https://doi.org/10.2469/faj.v66.n2.1; CR 50 [CR]. Crossref also holds a stray test DOI (…v66.n2.test); do not cite it | n/a. VL confirmed in Consensus; URL not recorded |
| A14 | Fung & Hsieh (2000), *JFQA* 35(3), 291–307 (biases; fund-of-funds benchmark) | found | DOI https://doi.org/10.2307/2676205; CR 606 [CR]. The bias magnitudes (3%, 1.4%) are still not abstract-verified (VL A33) | n/a. VL confirmed in Consensus; URL not recorded |
| A15 | Busse, Goyal & Wahal (2010), *JF* 65(2), 765–790 (long-only α ≈ 0) | found | DOI https://doi.org/10.1111/j.1540-6261.2009.01550.x; CR 263. WP title "Performance Persistence in Institutional Investment Management" (SSRN 2006) [CR] | n/a. VL confirmed in Consensus; URL not recorded |
| A16 | Goyal & Wahal (2008), *JF* 63(4), 1805–1847 (hire/fire baseline) | found | DOI https://doi.org/10.1111/j.1540-6261.2008.01375.x; CR 172 [CR] | n/a |
| A17 | Barras, Scaillet & Wermers (2010), "False discoveries in mutual fund performance", *JF* 65(1), 179–216 | found (title shortened) | Full title "False Discoveries in Mutual Fund Performance: Measuring Luck in Estimated Alphas". DOI https://doi.org/10.1111/j.1540-6261.2009.01527.x; CR 665 [CR]. The method is challenged in §5 C3 | n/a |
| A18 | Brooks, Gould & Richardson (2020), "Active fixed income illusions", *J. Fixed Income* | found (add volume and pages) | *JFI* 29(4):5–19, DOI https://doi.org/10.3905/jfi.2020.1.086; CR 6 [CR] | n/a |
| A19 | Sadka (2010), *JFE* 98(1), 54–71 (liquidity factor) | found | DOI https://doi.org/10.1016/j.jfineco.2010.05.001; CR 296 [CR] | n/a. VL confirmed in Consensus; URL not recorded |
| A20 | Boyson, Stahel & Stulz (2010), *JF* 65(5), 1789–1816 (contagion jump) | found | DOI https://doi.org/10.1111/j.1540-6261.2010.01594.x; CR 360. NBER precursor "Hedge Fund Contagion and Liquidity" (2008) [CR] | [record](https://consensus.app/papers/details/010bdfd384ec50809ef53bffb82b8263/?utm_source=claude_desktop) [P09] |
| A21 | Fung, Hsieh, Naik & Ramadorai (2008), *JF* 63(4), 1777–1803 (flows erode alpha) | found | DOI https://doi.org/10.1111/j.1540-6261.2008.01374.x; CR 490 [CR] | n/a |
| A22 | Pástor, Stambaugh & Taylor (2015), "Scale and skill in active management", *JFE*; NBER w19891 | found (add volume and pages) | *JFE* 116(1):23–45, DOI https://doi.org/10.1016/j.jfineco.2014.11.008; CR 542 [CR] | n/a |
| A23 | Naik, Ramadorai & Stromqvist (2007), *EFM* 13(2), 239–256 (capacity) | found | DOI https://doi.org/10.1111/j.1468-036x.2006.00353.x; CR 98 [CR] | n/a |
| A24 | Tóth et al. (2011), *Physical Review X* 1, 021006 (square-root impact) | found | *PRX* 1(2):021006, DOI https://doi.org/10.1103/physrevx.1.021006; CR 158 [CR] | n/a |
| A25 | Jenkinson, Jones & Martinez (2016), *JF* 71(5), 2333–2370 ([nrv]; consultant ratings) | found (resolves [nrv]) | DOI https://doi.org/10.1111/jofi.12289; CR 101. SSRN 2013 version https://doi.org/10.2139/ssrn.2327042 [CR] | [record](https://consensus.app/papers/details/760c6bf6c8eb5ced8d92754ebb965e73/?utm_source=claude_desktop) [VL; the VL notes it confirmed the claim via the SSRN abstract] |

### Table B: the other 24 academic references

| # | Dossier citation | Status | Corrected / confirmed metadata [source] | Consensus URL |
|---|---|---|---|---|
| B1 | Teo (2011), *JFE* 100(1), 24–44 | found | DOI https://doi.org/10.1016/j.jfineco.2010.11.003; CR 164. WP title "How Liquid are Liquid Hedge Funds?" (SSRN 2010) [CR] | n/a (VL confirmed in Consensus) |
| B2 | Jagannathan, Malakhov & Novikov (2010), *JF* 65(1), 217–255 | found (subtitle omitted) | "Do Hot Hands Exist among Hedge Fund Managers? An Empirical Evaluation"; DOI https://doi.org/10.1111/j.1540-6261.2009.01528.x; CR 226 [CR] | n/a |
| B3 | Kosowski, Naik & Teo (2007), *JFE* 84(1) [nrv] | found (resolves [nrv]; add pages) | *JFE* 84(1):229–264, DOI https://doi.org/10.1016/j.jfineco.2005.12.009; CR 437 [CR] | n/a |
| B4 | Rattray, Granger, Harvey & Van Hemert (2020), "Strategic Rebalancing", *JPM* 46(6) [nrv] | found | *JPM* 46(6):10–31, DOI https://doi.org/10.3905/jpm.2020.1.150; CR 9 [CR] | n/a |
| B5 | Berk & van Binsbergen (2015), *JFE* 118(1), 1–20 | found | DOI https://doi.org/10.1016/j.jfineco.2015.05.002; CR 775 [CR] | n/a |
| B6 | Fama & French (2010), *JF* 65(5), 1915–1947 | found | DOI https://doi.org/10.1111/j.1540-6261.2010.01598.x; CR 1,370 [CR] | n/a |
| B7 | Hombert & Thesmar (2014), *JFE* 111(1), 26–44 | found | DOI https://doi.org/10.1016/j.jfineco.2013.09.003; CR 48 [CR] | n/a |
| B8 | Agarwal, Daniel & Naik (2009), *JF* 64(5), 2221–2256 | found | DOI https://doi.org/10.1111/j.1540-6261.2009.01499.x; CR 478 [CR] | n/a |
| B9 | Asness, Krail & Liew (2001), "Do hedge funds hedge?", *JPM* | found (add volume and pages) | *JPM* 28(1):6–19, DOI https://doi.org/10.3905/jpm.2001.319819; CR 328 [CR] | n/a |
| B10 | Bollen & Pool (2009), "Do hedge fund managers misreport returns?", *JF* 64(5), 2257–2288 | found (subtitle omitted) | Adds "Evidence from the Pooled Distribution"; DOI https://doi.org/10.1111/j.1540-6261.2009.01500.x; CR 253 [CR] | n/a |
| B11 | Ramadorai (2012), *JF* 67(2), 479–512 | found | DOI https://doi.org/10.1111/j.1540-6261.2012.01723.x; CR 49 [CR] | n/a |
| B12 | Ramadorai (2013), *JFE* 107(2), 401–416 | found | DOI https://doi.org/10.1016/j.jfineco.2012.08.020; CR 48 [CR] | n/a |
| B13 | Malkiel & Saha (2005), *FAJ* 61(6), 80–88 | found | DOI https://doi.org/10.2469/faj.v61.n6.2775; CR 276 [CR] | n/a |
| B14 | Mitchell & Pulvino (2001), *JF* 56(6), 2135–2175 | found | DOI https://doi.org/10.1111/0022-1082.00401; CR 567 [CR] | n/a |
| B15 | Dao et al. (2016), arXiv:1607.02410 | found (version note) | Published as *Journal of Investment Strategies* 7(1):61–84 (2017), https://doi.org/10.21314/jois.2017.093 (CR 6); SSRN https://doi.org/10.2139/ssrn.2777657 [CR] | n/a |
| B16 | Frazzini, Israel & Moskowitz (2018), "Trading costs", AQR WP | found (WP) | SSRN https://doi.org/10.2139/ssrn.3229719; CR 91 [CR] | n/a |
| B17 | Getmansky, Lee & Lo (2015), *ARFE* 7; NBER w21449 | found (add pages) | *ARFE* 7(1):483–577, https://doi.org/10.1146/annurev-financial-110311-101741; CR 52 [CR] | n/a |
| B18 | Dimmock, Wang & Yang (2024), *MS* (cited "via 06", §2.8) | found [P01-09] | The Consensus record shows year 2019, NBER DOI 10.3386/w25559, venue *Manag. Sci.*; its abstract cites MS DOI 10.1287/mnsc.2023.4759 (streams 01, 02, 04, 06, 08, 09) | [record](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop) |
| B19 | Granger et al. (2014), "as summarised by Man" [nrv] | found | "Rebalancing Risk", Granger, Greenig, Harvey, Rattray & Zou, SSRN (2014), https://doi.org/10.2139/ssrn.2488552; CR 11 [CR] | n/a |
| B20 | Almgren & Chriss (2000), *J. Risk* [nrv] | **mismatched (year)** | "Optimal execution of portfolio transactions", *The Journal of Risk* 3(2):5–39, Crossref issue date **2001**, https://doi.org/10.21314/jor.2001.041; CR 1,276 [CR] | n/a |
| B21 | Davis & Norman (1990), *Math. Oper. Res.* [nrv] | found (add volume and pages) | "Portfolio Selection with Transaction Costs", *MOR* 15(4):676–713, https://doi.org/10.1287/moor.15.4.676; CR 963 [CR] | n/a |
| B22 | Leland (1999) [nrv] | found (WP) | "Optimal Portfolio Management with Transactions Costs and Capital Gains Taxes"; the SSRN record is dated 2000, https://doi.org/10.2139/ssrn.206871; CR 62 [CR] | n/a |
| B23 | Geltner (1993) [nrv] | found | "Estimating Market Values from Appraised Values without Assuming an Efficient Market", *JRER* 8(3):325–345, https://doi.org/10.1080/10835547.1993.12090713; CR 349 [CR] | n/a |
| B24 | Grinold & Kahn, *Active Portfolio Management* (2000) [nrv; book] | found (indirect) | The only Crossref record is a 1996 *JF* entry for the first edition (*JF* 51(4):1559, https://doi.org/10.2307/2329407; listed with Goetzmann; apparently a book review). The second edition is not indexed [CR] | n/a |

**Tally:** 49 checked: 48 found (17 of them with version, title or completeness notes), 1 mismatched (B20), 0 not found.

---

## 3. Annotated bibliography: 25 relevant papers missing from the dossier

Entry format: title (link), then authors · year · venue · citations · DOI, then the finding (abstract-level) and its relevance to ADIC.

### A. Hedge-fund liquidity, runs and fragility (feeds §6.5 state machine and §6.10 constraints)

**1. [Liquidity Transformation and Financial Fragility: Evidence from Funds of Hedge Funds](https://doi.org/10.1017/s0022109018001369)**
- Vikas Agarwal, George O. Aragon, Zhen Shi · 2019 (Crossref issue date 2018) · *JFQA* 54(6):2355–2381 · CR 28 · DOI 10.1017/s0022109018001369 [CR]
- **Finding:** The paper builds an "illiquidity gap": the mismatch between a fund of funds' portfolio liquidity and the liquidity it offers its own investors.
  - Greater liquidity transformation is driven by incentives to attract capital and earn compensation.
  - It goes with greater exposure to investor runs and worse performance in crises.
  - Funds of funds mitigate the risk with larger cash buffers.
- **Relevance:** This is the empirical counterpart of the mismatch term M_i in the dossier's gate hazard (§6.5) and of the fund-of-funds "double mismatch" (§6.11). It also argues for adding fund cash as a mitigating covariate. **[Inference]**

**2. [Return Smoothing, Liquidity Costs, and Investor Flows: Evidence from a Separate Account Platform](https://consensus.app/papers/details/263bf0e52d355c0baf0c7fef98bc44e5/?utm_source=claude_desktop)** [P06]
- Charles Cao, Grant Farnsworth, Bing Liang, Andrew W. Lo · 2017 · *Management Science* 63(7):2233–2250 · CR 16; S2 14 · DOI 10.1287/mnsc.2015.2401 [CR, S2]
- **Finding:** The data come from managed accounts that trade pari passu with matching hedge funds but have third-party reporting and permissive share restrictions.
  - 33% of reported smoothing is due to managerial reporting methods.
  - Fund-level liquidity on the platform is associated with a 1.7% annual performance reduction.
  - Investor flows chase monthly past performance on the platform, but not in the matching funds.
- **Relevance:** It gives three priors that depend on the vehicle (the spec card already has a "vehicle" field):
  - smoothing θ for managed accounts versus commingled funds;
  - a cost of liquidity of about 1.7% a year;
  - more performance-chasing, and so run-prone, flows in liquid vehicles. **[Inference]**

**3. [Funding Liquidity Risk and the Dynamics of Hedge Fund Lockups](https://doi.org/10.1017/s0022109020000393)**
- Adam L. Aiken, Christopher P. Clifford, Jesse A. Ellis, Qiping Huang · 2021 (Crossref issue date 2020) · *JFQA* 56(4):1321–1349 · CR 9 · DOI 10.1017/s0022109020000393 [CR]
- **Finding:** Expiring lock-ups provide a within-fund measure of funding liquidity risk.
  - Funds with lower funding risk earn higher returns, driven by greater exposure to equity-mispricing anomalies.
  - Placebo and regression-discontinuity tests support a causal link.
- **Relevance:** A manager's alpha depends on the lock-up expiry profile of its whole investor base, not only on ADIC's own terms. That calls for a fund-level funding-risk state, with α and the gate hazard conditional on it. **[Inference]**

**4. [Liquidity Restrictions, Runs, and Central Bank Interventions: Evidence from Money Market Funds](https://consensus.app/papers/details/389740373ccf5208b969643b471e31ae/?utm_source=claude_desktop)** [P05]
- Lei Li, Yi Li, Marco Macchiavelli, Xing (Alex) Zhou · 2021 · *RFS* 34(11):5402–5437 · CR 108 (Consensus 79, per stream 05) · DOI 10.1093/rfs/hhab065 [CR]
- **Finding:** Gates and fees introduced by the 2016 money-market fund reform "exacerbated the run on prime MMFs during the COVID-19 crisis", consistent with strategic complementarities. The Fed's facility stabilized the funds.
- **Relevance:** This is empirical support for the preemption term ρ₂·1{p̂^gate > p*} (§6.5). It answers the VL's concern (R9) that the dossier rests that term only on Cipriani et al.'s model. Carrying the effect over to hedge funds is **[inference]**.

**5. [LTCM Redux? Hedge fund Treasury trading, funding fragility, and risk constraints](https://doi.org/10.1016/j.jfineco.2025.104017)**
- Mathias S. Kruttli, Phillip J. Monin, Lubomir Petrasek, Sumudu W. Watugala · 2025 · *JFE* 169:104017 · CR 9; S2 8 · DOI 10.1016/j.jfineco.2025.104017 [CR, S2]
- **Finding [WP abstract]:** The data are regulatory filings around the 2020 Treasury shock.
  - Hedge funds cut arbitrage and raised cash "despite stable credit and low contemporaneous redemptions".
  - Creditors' constraints did not pass through repo.
  - More-regulated dealers provided more funding, and more important clients received more.
  - Reported VaR suggests internal risk constraints were binding.
- **Relevance:** Hedge-fund losses and deleveraging can occur without redemptions or gates. The state machine therefore needs a manager risk-limit (VaR-headroom) channel in the crisis jump J. This matters especially for the reported TRS-based leveraged multi-strategy programme (VL F20), whose collateral sits with Corporate Finance. **[Inference]**

**6. [Hedge funds as liquidity providers: Evidence from the Lehman bankruptcy](https://doi.org/10.1016/j.jfineco.2011.10.004)**
- George O. Aragon, Philip E. Strahan · 2012 · *JFE* 103(3):570–587 · CR 229 · DOI 10.1016/j.jfineco.2011.10.004 [CR]
- **Finding [WP abstract]:** Funds that used Lehman as prime broker could not trade after the bankruptcy and "failed twice as often as otherwise-similar funds". Stocks they traded lost more market liquidity, especially stocks that were already illiquid.
- **Relevance:** This gives a prime-broker counterparty state and a hazard multiplier for the liquidation branch in §6.5. The dossier's data fields already list prime brokers (§6.16) but no equation uses them. **[Inference]**

### B. Return model, alpha measurement, persistence and capacity (feeds §6.4, §6.11, §6.14)

**7. [The Cost of Capital for Alternative Investments](https://doi.org/10.1111/jofi.12269)**
- Jakub W. Jurek, Erik Stafford · 2015 · *JF* 70(5):2185–2226 · CR 61 · DOI 10.1111/jofi.12269 [CR]
- **Finding:** Traditional factor models give hedge funds pre-fee alphas of 6–10% a year over 1996–2012. Yet the hedge-fund return series "is not reliably distinguishable" from mechanical S&P 500 put-writing. In equilibrium, required returns "can dramatically exceed those suggested by traditional models".
- **Relevance:** This challenges the positive alpha priors (§5 C1). It argues for a downside-risk-based hurdle in the Score function and for a put-writing replication baseline in the Challenge agent. **[Inference]**

**8. [Is it alpha or beta? Decomposing hedge fund returns when models are misspecified](https://doi.org/10.1016/j.jfineco.2024.103805)**
- David Ardia, Laurent Barras, Patrick Gagliardini, Olivier Scaillet · 2024 · *JFE* 154:103805 · CR 8; S2 4 · DOI 10.1016/j.jfineco.2024.103805 [CR, S2]
- **Finding:**
  - "Prominent models are as misspecified as the CAPM".
  - Time-series momentum, variance and carry factors capture hedge-fund strategies and lower measured performance.
  - Alpha and beta components correlate negatively and vary widely across funds.
- **Relevance:** Extend the §6.4 factor vector with carry and variance-risk-premium factors, and choose models with misspecification-robust tests. Expect lower alpha priors (§5 C2). **[Inference]**

**9. [Hedge Fund Performance: End of an Era?](https://doi.org/10.1080/0015198x.2021.1921564)**
- Nicolas P.B. Bollen, Juha Joenväärä, Mikko Kauppila · 2021 · *FAJ* 77(3):109–132 · CR 41; S2 21 · DOI 10.1080/0015198x.2021.1921564 [CR, S2]
- **Finding:** Aggregate hedge-fund performance declined over the past decade.
  - Two prediction models picked funds that lowered volatility and raised the Sharpe ratio of a multi-asset portfolio over the full 1997–2016 sample.
  - Hedge-fund allocations "failed to improve the Sharpe ratio from 2008 onward".
- **Relevance:** This sets the default role of hedge funds in the total portfolio as volatility reduction, not Sharpe enhancement. It supports aggregate net-α priors near zero (§5 C1).

**10. [Decreasing returns to scale has eroded hedge fund performance persistence](https://doi.org/10.1108/cfr-06-2023-2497)**
- Nicolas P.B. Bollen, Juha Joenväärä, Mikko Kauppila · 2026 · *Critical Finance Review* 15(1):1–36 · CR 0 · DOI 10.1108/cfr-06-2023-2497 [CR, S2]
- **Finding:** The paper replicates Kosowski–Naik–Teo (2007) and Jagannathan–Malakhov–Novikov (2010). Top funds still persist, even in real-time data. But the persistence available to investors "has substantially weakened", and it appears only under Kosowski et al.'s Bayesian alpha. The decline is linked to decreasing returns to scale among superior funds.
- **Relevance:** This is strong, current evidence:
  - Use Bayesian alpha as the hire and re-up signal.
  - Make α(AUM) bite hardest for the best managers.
  - Temper §4.6's "persistence among superior funds" (§5 C7).

**11. [Do the Best Hedge Funds Hedge?](https://doi.org/10.1093/rfs/hhq105)**
- Sheridan Titman, Cristian Tiu · 2011 (Crossref issue date 2010) · *RFS* 24(1):123–168 · CR 243 · DOI 10.1093/rfs/hhq105 [CR]
- **Finding [WP abstract]:** Funds with lower R² against systematic factors have higher Sharpe and information ratios, charge higher fees and attract more inflows.
- **Relevance:** Factor R² is a cheap manager-evidence-card feature. A caveat for the §6.4 model: the factor model will explain the best funds least. **[Inference]**

**12. [The Optimal Size of Hedge Funds: Conflict between Investors and Fund Managers](https://doi.org/10.1111/jofi.12413)**
- Chengdong Yin · 2016 · *JF* 71(4):1857–1894 · CR 71 · DOI 10.1111/jofi.12413 [CR]
- **Finding:** Manager pay rises with assets even when scale hurts performance, so pay is maximized "at a much larger fund size than is optimal for fund performance". Management firms gather capital even at the expense of flagship performance.
- **Relevance:** Capacity monitoring belongs in the Challenge agent. ADIC's own large tickets push funds past their optimal size, which interacts with the C-PM2 concentration cap. **[Inference]**

**13. [Mutual Fund Flows and Performance in Rational Markets](https://doi.org/10.1086/424739)** (seminal)
- Jonathan B. Berk, Richard C. Green · 2004 · *JPE* 112(6):1269–1295 · CR 1,993 · DOI 10.1086/424739 [CR]
- **Finding [WP abstract]:** With competitive capital provision and decreasing returns to scale, active funds do not outperform passive benchmarks. Past performance cannot predict future returns or reveal average skill. Lack of persistence does not mean managers have no differential ability.
- **Relevance:** This is the theory behind the dossier's α(AUM) decay equation and its warning against performance chasing (§6.4, §6.14). It should be cited as the foundation.

### C. Database biases and data quality (feeds §4.6, §6.12 calibration targets, §6.14)

**14. [The Fix Is In: Properly Backing out Backfill Bias](https://doi.org/10.1093/rfs/hhz024)**
- Philippe Jorion, Christopher Schwarz · 2019 · *RFS* 32(12):5048–5099 · CR 50 · DOI 10.1093/rfs/hhz024 [CR]
- **Finding:** Truncating a fixed number of months "largely preserves backfilled returns". Both common treatments can bias results, including cross-sectional ones. Best practice is to remove returns before the listing date; the authors infer listing dates where databases lack them.
- **Relevance:** Peer benchmarks and the §6.12 calibration targets should use listing-date removal. The dossier's "classic" 1.4% backfill haircut (Fung & Hsieh 2000, [nrv]) is not a sound correction (§5 C8). **[Inference]**

**15. [Change You Can Believe In? Hedge Fund Data Revisions](https://doi.org/10.1111/jofi.12240)**
- Andrew J. Patton, Tarun Ramadorai, Michael Streatfield · 2015 · *JF* 70(3):963–999 · CR 73 · DOI 10.1111/jofi.12240 [CR]
- **Finding:** Historical hedge-fund returns are "routinely revised", partly predictably, and funds that revise "significantly and predictably underperform" funds that never revise.
- **Relevance:** Store dated snapshots of every manager track record and flag revisions as a negative signal on the manager evidence card. A data-quality agent can do this. **[Inference]**

**16. [Hedge Fund Performance: Are Stylized Facts Sensitive to Which Database One Uses?](https://doi.org/10.1561/104.00000104)**
- Juha Joenväärä, Mikko Kauppila, Robert Kosowski, Pekka Tolonen · 2021 · *Critical Finance Review* 10(2):271–327 · CR 47; S2 52 · DOI 10.1561/104.00000104 [CR, S2]
- **Finding:** Several stylized facts depend on database choice, through coverage of dead funds and completeness of AUM data. There is "no performance persistence for certain rebalancing frequencies and databases".
- **Relevance:** Calibration targets and α priors should be robust to database choice; prefer aggregated multi-database panels. **[Inference]**

### D. Long-only and manager evaluation (feeds §2.6, §6.11 long-only priors, §6.14 grading)

**17. [Asset Managers: Institutional Performance and Factor Exposures](https://consensus.app/papers/details/0212f272b5cf5989a5a878405e42c2d3/?utm_source=claude_desktop)** [VL]
- Joseph Gerakos, Juhani T. Linnainmaa, Adair Morse · 2021 · *JF* 76(4):2035–2075 · CR 49 · DOI 10.1111/jofi.13026 [CR]
- **Finding:** The sample is $18trn of institutional accounts. Active accounts beat strategy benchmarks by 75bp gross and 31bp net (2000–2012). The outperformance "came from factor exposures": mean-variance-efficient portfolios of index and institutional funds would not have earned higher Sharpe ratios.
- **Relevance:** For REFINANCE (§6.7), the forgone return when a mandate is replaced by index futures is about the benchmark-relative net α (here +31bp, mostly factor tilts), not zero. That holds unless the overlay also replicates the tilts. **[Inference]**

**18. [Does Active Management Pay? New International Evidence](https://doi.org/10.1093/rapstu/rat005)**
- Alexander Dyck, Karl V. Lins, Lukasz Pomorski · 2013 · *Review of Asset Pricing Studies* 3(2):200–228 · CR 67 · DOI 10.1093/rapstu/rat005 [CR]
- **Finding [WP abstract]:** Defined-benefit pension plans, 1993–2008:
  - emerging-market active positions outperformed by 250bp a year;
  - EAFE by about 50bp (not always significant);
  - US active positions underperformed by the active-minus-passive cost difference.
- **Relevance:** This supports sleeve-specific long-only priors. It backs the dossier's positive EM prior (§6.11), which the VL (R9) said lacked support. The data end in 2008, so shrink them. **[Inference]**

**19. [Reassessing False Discoveries in Mutual Fund Performance: Skill, Luck, or Lack of Power?](https://doi.org/10.1111/jofi.12784)**
- Angie Andrikogiannopoulou, Filippos Papakonstantinou · 2019 · *JF* 74(5):2667–2688 · CR 56 · DOI 10.1111/jofi.12784 [CR]
- **Finding:** The Barras–Scaillet–Wermers FDR method is conservative and underestimates the share of funds with non-zero alpha. In simulations, "65% of funds with economically large alphas … are misclassified as zero alpha" (the alpha threshold is missing from the indexed abstract). Low power "can materially change the conclusion that most funds have zero alpha".
- **Relevance:** This directly challenges §6.14(vii) and the 75% zero-alpha anchor (§5 C3).

**20. [Skill, Scale, and Value Creation in the Mutual Fund Industry](https://doi.org/10.1111/jofi.13096)**
- Laurent Barras, Patrick Gagliardini, Olivier Scaillet · 2022 (Crossref issue date 2021) · *JF* 77(1):601–638 · CR 80 · DOI 10.1111/jofi.13096 [CR]
- **Finding:** Skill and scalability vary widely across funds and are strongly related, because "great investment ideas are difficult to scale up". Value added is positive for most funds and converges towards its optimum after an adjustment period.
- **Relevance:** Make the capacity exponent η in α(AUM) fund-specific rather than one constant. Grade managers on dollar value added as well as alpha. **[Inference]**

**21. [When Do Consultants Add Value? Evidence from Hedge Fund Recommendations](https://consensus.app/papers/details/b7f56cc827ff57d29b6c417e2bfe65b1/?utm_source=claude_desktop)** [VL]
- Juha Joenväärä, Mikko Kauppila, Christian T. Lundblad, Juuso Nissinen · 2026 · SSRN working paper · CR 0 · DOI 10.2139/ssrn.6794318 [CR]
- **Finding:** The data are institutional hedge-fund mandates, 2000–2022. Recommended funds beat feasible alternatives:
  - FH7 alpha of 0.70% a year overall, up to 1.81% for alternatives-specialist consultants;
  - lower downside risk, lower "liquidity fragility" and lower failure rates.
  - Consultants favour restrictive share terms and lower operational risk.
- **Relevance:** Rater credibility should be estimated separately by asset class. The Jenkinson et al. long-only result should not be carried over to hedge-fund raters (§5 C4). It is not yet peer-reviewed.

### E. Synthetic exposure and rebalancing (feeds §2.7, §6.7, §6.9; Corporate Finance FTP)

**22. [Beyond Basis Basics: Liquidity Demand and Deviations from the Law of One Price](https://doi.org/10.1111/jofi.13198)**
- Todd M. Hazelkorn, Tobias J. Moskowitz, Kaushik Vasudevan · 2023 (Crossref issue date 2022) · *JF* 78(1):301–345 · CR 25 · DOI 10.1111/jofi.13198 [CR]
- **Finding [WP abstract]:** Futures–cash bases capture liquidity demand for equity exposure.
  - They co-move with dealer and investor futures positions.
  - They negatively predict futures and spot returns.
  - The imbalances persist, and the compensation for meeting the demand is large ("5-6% annual premium").
- **Relevance:** The financing spread f_{b,t} (§6.2) should be a persistent, demand-driven state variable, not i.i.d. regime noise. It is a direct input to physical-to-synthetic costs and to Corporate Finance's FTP curve. When demand is high, the Overlay could be paid to *supply* synthetic exposure. **[Inference]**

**23. [The Unintended Consequences of Rebalancing](https://doi.org/10.3386/w33554)**
- Campbell Harvey, Michele Mazzoleni, Alessandro Melone · 2025 · NBER WP 33554 · CR 29 · DOI 10.3386/w33554 [CR]
- **Finding [WP abstract, SSRN 5172097]:** Calendar- and threshold-based institutional rebalancing moves markets predictably. When stocks are overweight, the selling lowers next-day equity returns by 17bp. The practice costs about $16bn a year and invites front-running.
- **Relevance:** This challenges the GPFG-style month-end 2pp trigger (§6.9) at ADIC's scale (§5 C5).

### F. Surveys

**24. [The Economics and Finance of Hedge Funds: A Review of the Academic Literature](https://doi.org/10.1561/0500000047)**
- Vikas Agarwal, Kevin A. Mullally, Narayan Y. Naik · 2015 · *Foundations and Trends in Finance* 10(1):1–111 · CR 50 · DOI 10.1561/0500000047 [CR]
- **Finding:** It updates the 2005 survey. The top four finance journals published 16 hedge-fund papers before 2005 and 105 after.
- **Relevance:** A reference base for the agents' knowledge store, and a checklist of the topics the dossier covers.

**25. [Challenging the Conventional Wisdom on Active Management: A Review of the Past 20 Years of Academic Literature on Actively Managed Mutual Funds](https://doi.org/10.1080/0015198x.2019.1628555)**
- K.J. Martijn Cremers, Jon A. Fulkerson, Timothy B. Riley · 2019 · *FAJ* 75(4):8–35 · CR 78 · DOI 10.1080/0015198x.2019.1628555 [CR]
- **Finding [WP abstract]:** Reviewing the literature since Carhart (1997), the authors conclude that "the conventional wisdom is too negative on the value of active management".
- **Relevance:** A counterweight to the dossier's near-zero long-only stance (§5 C3), and a source of skill signals to test.

---

## 4. Missed-but-important papers: design implications

Every row is **[inference]** from the cited abstracts. Equation names follow the dossier.

| Design element | Change suggested by the literature | Evidence (§3 #) |
|---|---|---|
| **State variable: fund liquidity mismatch** | Replace the ad hoc M_i with an illiquidity-gap measure. Add fund cash or unencumbered cash as a mitigating covariate: logit p^gate = … + b₃·IG_i − b₅·cash_i | #1; Liu & Mello (2011, below) |
| **State variable: investor-base lock-up profile** | Track the share of each fund's capital whose lock-ups expire within 1–4 quarters. Use it as a funding-risk index FR_{i,t} that lowers α (e.g., α_{i,t}·(1 − κ_FR·FR_{i,t})) and raises the gate hazard. Request it in due-diligence questionnaires | #3 |
| **State variable: manager risk-limit headroom** | Add VaR utilization or risk-limit headroom as a driver of the crisis jump J, independent of others' redemption requests R^oth | #5 |
| **State variable: prime-broker and TRS counterparty** | Add prime-broker identity and health per fund, and bank-counterparty state for the leveraged-HF TRS. If a prime broker fails, raise the liquidation hazard (twice the failure rate in Lehman's case). Credit supply affects fund leverage and alpha | #6; Li, Monin & Petrasek (2024, below) |
| **State variable: futures–cash basis** | Model f_{b,t} as a persistent AR process linked to dealer and investor positioning. It feeds REFINANCE and LEVER costs and Corporate Finance's FTP curve | #22 |
| **State variable: data vintage** | Keep listing date, reporting status (start and stop) and revision count per manager history | #14, #15; Agarwal–Fos–Jiang, Aiken et al. (below) |
| **Model: hedge-fund factors** | Add carry and variance-risk-premium factors to F_t. Pick factor sets per fund with misspecification-robust comparison. Report alpha against a put-writing replication | #7, #8 |
| **Model: alpha and selection** | Use Bayesian (Kosowski-style) alpha as the hire and re-up signal. Make the capacity exponent fund-specific, and steepest for top funds. Shrink with a prior learned across funds (hierarchical) | #10, #12, #13, #20; Jones & Shanken, Chen–Cliff–Zhao (below) |
| **Model: smoothing by vehicle** | Lower the smoothing θ for managed accounts and third-party-administered vehicles. About one-third of reported smoothing is managerial reporting. Flag conditional smoothing as a fraud indicator | #2; Bollen & Pool (2008, below) |
| **Parameters: hedge-fund α priors** | Set the aggregate post-2008 hedge-fund net α prior near 0. Allow uplift only for funds that pass a credible screen; recommended funds earned +0.70% a year FH7 alpha, so use that as an upper anchor | #9, #21 |
| **Parameters: liquidity premium** | About 1.7% a year is the cost of permissive liquidity on a managed-account platform. It sits alongside Aragon's 4–7% gross lock-up premium in the HOLD and vehicle-choice economics | #2; A6 |
| **Parameters: long-only priors** | US large cap: net α ≈ −(active minus passive cost). EM: positive but shrunk (+250bp in 1993–2008 plan data). Institutional accounts generally: +31bp net, mostly from factors | #17, #18 |
| **Constraint: C-PM2 concentration** | Add the fund's illiquidity gap and investor-base mix (fund-of-funds and short-lock share) to the reflexive-gate test, not just ADIC's ownership share | #1, #3 |
| **Constraint: C-PM4 HQLA** | Extend it to the HF-basket TRS. Stress manager deleveraging and bank margin calls together. Collateral is a Corporate Finance resource | #5, #6 |
| **Constraint: rebalancing (C-PM7)** | Avoid a predictable calendar or threshold schedule. Randomize execution windows. Count predictable-flow costs when scoring rebalancing policies | #23 |
| **Objective: Score risk charge** | For hedge-fund sleeves, price downside risk (put-like exposure) explicitly rather than with mean–variance or factor alpha. Credit hedge funds' volatility reduction separately from their Sharpe contribution | #7, #9 |
| **Objective: REFINANCE forgone return** | Use benchmark-relative net α, including factor tilts, as the cost of moving to index futures, unless the Overlay replicates the tilts with factor futures or swaps | #17 |
| **Agent: Data-quality agent (new)** | Infer listing dates; remove pre-listing returns; aggregate several databases; store dated snapshots; flag revisions | #14, #15, #16 |
| **Agent: Challenge agent additions** | Checks: "replicable by put-writing?", conditional smoothing, revision history, AUM beyond capacity, prime-broker concentration, VaR-driven deleveraging exposure | #5, #6, #7, #12, #15 |
| **Agent: forecast grading (§6.14)** | Treat FDR as a conservative screen only. Add power-aware mixture or Bayesian skill estimates. Never conclude "no skill" from FDR alone | #19, #20; Chen–Cliff–Zhao (below) |
| **IC: rater credibility** | Estimate consultant and analyst credibility separately for hedge-fund and long-only mandates | #21; A25 |
| **IC: artifacts** | A hedge-fund role card (volatility reduction vs Sharpe contribution, put-writing similarity). A rebalancing-predictability panel in the rebalancing monitor. A basis state on the REFINANCE monitor | #7, #9, #22, #23 |
| **IC roster: Corporate Finance seat** | It owns the financing-basis state, HQLA backing and TRS or prime-broker counterparty limits for the leveraged-HF sleeve | #5, #6, #22 |

**Also relevant (verified; brief):**
- [The fragile capital structure of hedge funds and the limits to arbitrage](https://doi.org/10.1016/j.jfineco.2011.06.005)
  - Liu & Mello · 2011 · *JFE* 102(3):491–506 · CR 82.
  - Coordination risk among investors makes managers conservative in crises [WP abstract]. Theory for cash buffers.
- [Out of the Dark: Hedge Fund Reporting Biases and Commercial Databases](https://doi.org/10.1093/rfs/hhs100)
  - Aiken, Clifford & Ellis · 2013 (Crossref issue date 2012) · *RFS* 26(1):208–243 · CR 120.
  - Self-reported data overstate skill; funds that stop reporting have "dramatically lower" returns [WP abstract].
- [Inferring Reporting-Related Biases in Hedge Fund Databases from Hedge Fund Equity Holdings](https://doi.org/10.1287/mnsc.1120.1647)
  - Agarwal, Fos & Jiang · 2013 · *MS* 59(6):1271–1289 · CR 144.
  - Funds start self-reporting after positive abnormal returns that do not persist [WP abstract].
- [Hedge Funds: The Good, the Bad, and the Lucky](https://doi.org/10.1017/s0022109017000217)
  - Chen, Cliff & Zhao · 2017 · *JFQA* 52(3):1081–1109 · CR 69.
  - A mixture-of-skill-groups measure beats alpha and t-statistics out of sample.
- [Mutual fund performance with learning across funds](https://doi.org/10.1016/j.jfineco.2004.08.009)
  - Jones & Shanken · 2005 · *JFE* 78(3):507–552 · CR 116.
  - Under independent priors the maximum posterior alpha grows without bound as the number of funds rises, even with no skill. Prior dependence lets investors aggregate information across funds [WP abstract].
- [Hedge funds, managerial skill, and macroeconomic variables](https://doi.org/10.1016/j.jfineco.2010.10.003)
  - Avramov, Kosowski, Naik & Teo · 2011 · *JFE* 99(3):672–692 · CR 120.
  - Manager skill is predictable from macro variables [WP abstract]. Supports regime-conditional α.
- [High-Water Marks and Hedge Fund Management Contracts](https://doi.org/10.1111/1540-6261.00581)
  - Goetzmann, Ingersoll & Ross · 2003 · *JF* 58(4):1685–1718 · CR 402.
  - A closed-form cost of the high-water-mark contract. Fees are "a claim on a significant proportion of investor wealth". Use it for PV-of-fees in HOLD.
- [Conditional Return Smoothing in the Hedge Fund Industry](https://consensus.app/papers/details/91dda5ed60b15d64a9ed06cae10e125d/?utm_source=claude_desktop) [P04]
  - Bollen & Pool · 2008 · *JFQA* 43(2):267–298 · CR 142.
  - Conditional serial correlation is linked to flow risk and is "a leading indicator of fraud".
- [Asset fire sales (and purchases) in equity markets](https://doi.org/10.1016/j.jfineco.2006.09.007)
  - Coval & Stafford · 2007 · *JFE* 86(2):479–512 · CR 1,459.
  - Forced sales pressure the prices of commonly held stocks, and flow-driven trades are predictable [WP abstract].
- [The Dark Side of Liquid Bonds in Fire Sales](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop) [P05, P09]
  - Chaderina et al. · 2026 · *MS* (stream 05 record).
  - Widely held liquid bonds fall the most when buying capital is scarce.
- [Credit Supply and Hedge Fund Performance: Evidence from Prime Broker Surveys](https://consensus.app/papers/details/98d0571e779f5dd5809059c7f37fea58/?utm_source=claude_desktop) [P06]
  - Li, Monin & Petrasek · 2024 · FEDS 2024-089 · CR 1 · DOI 10.17016/feds.2024.089.
  - More prime-broker credit supply leads to more borrowing and higher returns and alphas, more so for funds with few prime brokers.
- [The Statistics of Sharpe Ratios](https://consensus.app/papers/details/ae10105da6315c3da6ea60251ec0b456/?utm_source=claude_desktop) [P09]
  - Lo · 2002 · *FAJ* 58(4):36–52 · CR 636.
  - Serial correlation can overstate annual Sharpe ratios "by as much as 65 percent" (stream 09 abstract check). Complements the GLM table in §2.2.
- [Share Restrictions and Investor Flows in the Hedge Fund Industry](https://doi.org/10.2139/ssrn.2692598)
  - Getmansky, Liang, Schwarz & Wermers · SSRN 2015.
  - Restrictions turn a convex flow–performance relation into an "inverted S". Use it to specify the others' requests ρ(·) in §6.5.

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier position | Challenge | Evidence and strength | Suggested response **[inference]** |
|---|---|---|---|---|
| C1 | Hedge-fund net α priors are positive: multi-strategy 2.0% (sd 2.5%), others 0.5–1.0% (§6.11); "small positive for hedge funds" (§1 item 10) | Measured hedge-fund alpha may be compensation for downside risk, and aggregate performance has declined | Jurek & Stafford 2015 (*JF*): returns are indistinguishable from put-writing and required returns are high. Bollen et al. 2021 (*FAJ*): no Sharpe improvement from 2008 onward. Ardia et al. 2024 (*JFE*): richer factors lower performance. **Strong** (three peer-reviewed papers). Partial counterweight: Joenväärä et al. 2026 (WP), Bollen et al. 2026 (*CFR*) | Aggregate prior ≈ 0. Uplift only with Bayesian-alpha evidence. Rerun IC conclusions with α = 0 as a mandatory sensitivity |
| C2 | Return model: Fung–Hsieh 8 factors + liquidity + OTM put (§6.4) | Prominent models are "as misspecified as the CAPM". Momentum, variance and carry capture strategies | Ardia et al. 2024. **Moderate–strong.** The dossier already has trend (lookback straddles) and put exposure, so the gap is mainly carry and variance-premium factors and model selection | Add carry and variance-risk-premium factors. Choose per fund with misspecification-robust tests |
| C3 | Long-only "close to zero average net alpha" and "about 75% zero-alpha" (§1 item 6, §4.7). FDR control as the skill test (§6.14 vii) | FDR has low power and misclassifies many skilled funds. Value added is positive for most funds. Institutional accounts beat benchmarks net | Andrikogiannopoulou & Papakonstantinou 2019 (*JF*); Barras, Gagliardini & Scaillet 2022 (*JF*); Gerakos et al. 2021 (*JF*: +31bp net, factor-driven); Cremers et al. 2019 (*FAJ* review); Dyck et al. 2013 (EM +250bp). **Moderate.** Most papers agree net alpha is small after costs; they disagree with "zero" and with the FDR inference | Treat FDR as a screen, not a verdict. Use sleeve-specific priors. Make REFINANCE's forgone return benchmark-relative, including factor tilts |
| C4 | "Optimistic analyst or consultant ratings" are corrected by scoring raters, citing Jenkinson et al. (§6.14) | For hedge-fund mandates, consultant recommendations add value | Joenväärä et al. 2026 (SSRN): FH7 +0.70% a year, lower liquidity fragility. **Moderate** (working paper; also noted in VL R9) | Estimate rater credibility per asset class; do not apply a uniform penalty |
| C5 | GPFG-style rebalancing: monthly test, 2pp band, futures first (§6.9) | Predictable institutional rebalancing has market impact and is front-run | Harvey, Mazzoleni & Melone 2025 (NBER): −17bp next-day equity return; about $16bn a year. **Moderate** (working paper; strong design relevance at ADIC's size). Hazelkorn et al. 2023 implies **[inference]** that futures-first execution pays a demand-driven basis | Randomize timing within windows. Include predictable-flow and basis costs in policy scoring. Keep the trend-delay option the dossier proposes |
| C6 | The hedge-fund liquidity and stress model centres on redemptions, gates and queues (§6.5) | Hedge funds deleverage and lose under internal risk constraints even when redemptions and credit are stable. Prime-broker failure is a separate channel | Kruttli et al. 2025 (*JFE*); Aragon & Strahan 2012 (*JFE*). **Strong** for adding channels. They do not refute the queue model | Add VaR-headroom and prime-broker states. Stress the TRS-based leveraged sleeve on both |
| C7 | "Persistence among superior funds; little among inferior ones" (§4.6, Jagannathan et al. 2010) | Persistence available to investors has "substantially weakened" and shows up only with Bayesian alpha. It depends on the database | Bollen, Joenväärä & Kauppila 2026 (*CFR*, a replication); Joenväärä et al. 2021 (*CFR*). **Strong** | Base hire and re-up decisions on Bayesian alpha with a capacity adjustment. Lower the credibility weights on raw track records |
| C8 | Bias handling: "classic" backfill ≈ 1.4% and survivorship ≈ 3% a year haircuts; "FoF-based or bias-adjusted benchmarks" (§4.6, §6.14) | Fixed truncation leaves most backfill in place. Database revisions and selective reporting create further biases | Jorion & Schwarz 2019 (*RFS*); Patton et al. 2015 (*JF*); Aiken et al. 2013 (*RFS*); Agarwal–Fos–Jiang 2013 (*MS*). **Strong** | Remove pre-listing returns; aggregate databases; keep dated snapshots; treat revisions as a signal |
| C9 | Liquidation costs: square-root impact with regime σ and V (§4.9, §6.6). Waterfall sells the most liquid sleeves first (§6.8) | Forced sales of commonly held assets carry extra price pressure. Widely held liquid assets can fall most in fire sales | Coval & Stafford 2007 (*JFE*); Chaderina et al. 2026 (*MS*). **Moderate** (equity mutual funds and insurers' bonds, not sovereign long-only books) | Add a crowding term (peer common ownership) to c_j(Q,S) in CRIS. Keep Treasury cash first |

**Supporting rather than challenging:**
- Li et al. 2021 supports the preemptive-run term empirically.
- Agarwal, Aragon & Shi 2019 supports the mismatch term.
- Cao et al. 2017 supports the priced liquidity premium (it is smaller than Aragon's figure, but measured more cleanly).
- Dyck et al. 2013 supports the positive EM long-only prior that VL R9 questioned.
- Bollen et al. 2026 and Barras et al. 2022 support α(AUM) decay.

---

## 6. Usage message (verbatim, last Consensus tool result)

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Search log

**Consensus `search`.** Three attempts on the GLM title, at 0, about 30 and about 60 seconds. All three returned the quota message in §6. No filters were used.

**OpenAlex.** 13 requests, 7 answered:
- the GLM title;
- Fung & Hsieh 2004 (with and without author names);
- Agarwal & Naik;
- Ang & Bollen;
- Aragon;
- Aiken et al.

After that, every request returned HTTP 429 (daily budget exhausted; Retry-After 48,667 s).

**Semantic Scholar.** 11 requests, 7 answered:
- title match: 7 requests, 6 answered;
- one batch lookup of 14 DOIs, which supplied the abstracts for #2, #8, #9, #10 and #16;
- the search endpoint: 3 topical attempts, all 429 after retries.

**Crossref.** All requests answered: 106 bibliographic searches and 16 DOI lookups.

**Topical backfill searches (14, Crossref).** Notable hits are named after each query.
1. "hedge fund share restrictions lockups gates": Getmansky, Liang, Schwarz & Wermers (2015 WP); Hong (2014, *JBF*); Aiken et al. (2016 WP, later *JFQA*); Derman (2006); Park & Whitt (2012).
2. "hedge fund performance persistence": Bollen, Joenväärä & Kauppila (2023 WP, later *CFR* 2026).
3. "hedge fund database biases backfill survivorship": Agarwal, Fos & Jiang (*MS* 2013); Jagannathan et al. backfill appendix.
4. "hedge funds during financial crisis": book chapters and minor working papers; nothing new of academic weight.
5. "active management fees performance mutual funds": low-relevance results; nothing new of academic weight.
6. "hedge fund liquidity mismatch fragility funds of hedge funds outflows": book chapters only.
7. "hedge fund return smoothing separate account platform liquidity costs": Cao, Farnsworth, Liang & Lo (*MS* 2017).
8. "multi-manager hedge fund platform pass-through fees": no academic paper on pass-through economics surfaced.
9. "hedge fund alpha decline decreasing returns to scale": Bollen, Joenväärä & Kauppila (*CFR* 2026); Harvey & Liu (2017 WP).
10. "plan sponsors hiring and firing investment managers performance chasing": only minor items.
11. "equity index futures basis implied financing liquidity demand law of one price": Hazelkorn, Moskowitz & Vasudevan (*JF*); Roll, Schwartz & Subrahmanyam (*JF* 2007).
12. "rebalancing flows front-running pension funds unintended consequences": Harvey, Mazzoleni & Melone (2025).
13. "hedge fund redemptions gates suspensions 2008 investor runs": Klaus & Rzepkowski (2009 WP); nothing of academic weight.
14. "hedge fund treasury trading funding fragility COVID-19 leverage redemptions": Kruttli et al. (*JFE* 2025; FEDS 2021-038).

**Title lookups.** 44 Crossref lookups for candidate papers, mostly with author names, plus the 48 citation checks behind §2.

**Limits.**
- Crossref ranks topical queries by keyword, not meaning, so topical recall is weaker than Consensus would give.
- Many of the candidates checked in §3 were identified from domain knowledge and then confirmed by Crossref lookup. Each finding still comes only from a retrieved abstract.
- Re-running the topical searches in Consensus after 1 November is recommended.
