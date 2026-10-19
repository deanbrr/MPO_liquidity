# G8 literature review: internal capital markets, transfer pricing and forecast incentives

*Literature check of `research/groups/dossiers/G8_org_tpa_economics.md` for the ADIC multi-period robust TPA framework. Prepared 2026-10-18. The dossier was not edited. This review complements the adversarial fact-check in `research/groups/verification/G8_org_tpa_economics.verify.md`. That log checked claims against primary text; this review checks reference metadata and looks for missing literature. Two of its entries are superseded here (see §1).*

> **Method note: read this first.**
> - **Consensus could not be used.** My first query (the Stein 1997 title) was rejected three times, 30 seconds apart, with the monthly-quota message reproduced verbatim in §6. The quota resets on 1 November. The quota covers the whole account, so I sent no further Consensus calls. **No Consensus search completed in this session.**
> - **OpenAlex** (a Consensus index): HTTP 429, `Retry-After: 46587` seconds (about 12.9 hours). Not used.
> - **Semantic Scholar** (a Consensus index): relevance search returned HTTP 429 on two attempts. One batch of three DOI look-ups went through. I used one abstract from it (Bauer & Zanjani 2021), tagged [S2].
> - **Crossref carried the work.** I ran 14 topical searches (plain query, no filters), about 110 title or DOI look-ups, and one arXiv API call for the four arXiv-cited works. Crossref's recall on topical queries is weaker than Consensus. Several seminal or recent papers below were therefore found by **title look-up of candidates I proposed from background knowledge or took from sibling reviews**. Each one was confirmed in Crossref before it was used, and the search log in §7 marks them.
> - **WebSearch and WebFetch were not used.**
> - **No Consensus URL was generated in this session.** 17 Consensus URLs appear below. Each is copied verbatim from a sibling review or the G8 verification log, and its source file is named. Every other link is the DOI or arXiv URL exactly as Crossref or arXiv returned it.
> - **Citation counts** are Crossref `is-referenced-by-count` (CR), read 2026-10-18. They usually run below Consensus or Google Scholar counts. Counts from saved Consensus records are labelled "CS-saved".
> - **"Finding" restates the retrieved abstract.** Quoted phrases are the authors' words. Where Crossref holds no abstract (common for Elsevier, Taylor & Francis and JSTOR back issues), no finding is reported. Anything beyond an abstract is tagged **[inference]**.
> - **User context relayed for this run.** The Secondaries group is "a hybrid of direct and fund investments", and "corporate finance own[s] the treasury function". Both bear on G8 (internal transfers; who owns FTP). See §4.7.

---

## 1. Summary

### Citation integrity
- **All 50 academic works in the dossier were checked.** That is the 45 academic entries in §10 (including Nadauld et al. inside entry 50) plus the 5 listed as "not verified in-session (background only)". The 25 most load-bearing came first; the other 25 were cheap to add once Consensus was out.
  - **48 found, 2 mismatched, 0 not found.** No hallucinated reference was found, which agrees with the verification log.
- **The two mismatches:**
  1. **Lamont (1997) has the wrong pages.** It is *JF* 52(1):**83–109**, DOI 10.1111/j.1540-6261.1997.tb03809.x. Pages 57–82 of that issue belong to Carhart, "On Persistence in Mutual Fund Performance" (DOI …tb03808.x). The verification log marked "JF 52(1):57–82" as correct; it is not.
  2. **Shin & Stulz (1998): the working-paper pointer is wrong.** NBER w5639 is *An Analysis of Divisional Investment Policies* (1996). This confirms the verification log. The *QJE* citation itself is correct.
- **Upgrades and minor fixes:**
  - **Chen, Kash, Ruberry & Shnayder (2014)** can lose its [M] tag. It is *ACM TEAC* 2(2):1–27. The abstract confirms the dossier's claim: strictly proper decision making "requires the decision maker use a completely mixed strategy".
  - **Gneiting (2011)** journal details are correct: *JASA* 106(494):746–762.
  - **Boutilier "(2011/2012)".** Crossref lists a 2012 proceedings version, pp. 737–744, DOI 10.65109/jsvv3990. Its container label is garbled. This supersedes the verification log's note that no 2012 venue version exists.
  - **The five background works all exist:** Denault (2001); Holmström & Milgrom (1991); Matvos & Seru (2014); Tetlock (Crossref holds the 2009 digital edition); Jenkinson, Jones & Martinez (2016). Jenkinson et al.'s abstract, which the dossier could not get, is now available (see table).
  - **Crawford & Sobel (1982)** is in §10 (entry 24) but never cited in the text. It is an orphan reference.
  - **Kuppuswamy & Villalonga:** the title drops the subtitle "Evidence from the 2007–2009 Financial Crisis".
  - **Alonso, Dessein & Matouschek (2008)** has a corrigendum, *AER* 98(3):1195–1196, which restores the equations on p. 153.
  - **Glaser et al. (2013):** the quoted "all unit managers systematically over-budget" and "about 40% more" are not in the abstract Crossref holds for either the *JF* or the 2008 SSRN version. The verification log sources them to RePEc. Cite that page explicitly.

### Backfill: what the dossier misses
I ran 14 topical searches (§7). §3 annotates 25 papers: 23 the dossier does not cite (§3.1–3.8) and 2 it does (§3.9). §3.10 lists 27 more in one line each. The main gaps:

1. **The asset-owner version of the internal capital market.** The dossier's ICM theory is about corporations (its own §4 says so). The literature on a CIO delegating to several asset-class managers is missing:
   - van Binsbergen, Brandt & Koijen (2008): the costs of decentralization and optimal benchmarks;
   - Blake et al. (2013): pension sponsors cut each manager's risk budget to offset coordination problems;
   - Sharpe (1981), the seminal paper (metadata only).
2. **Newer ICM evidence, including the "bright side":**
   - Matvos & Seru (2014): structural socialism wedges, and external capital costs four times higher in dislocations;
   - Hoang, Gatzer & Ruckes (2025, *MS*): a CFO survey on approval layers, delegation and "even" allocations;
   - Dai, Giroud, Jiang & Wang (2024): a q theory of ICMs;
   - Duchin & Sosyura (2013): connections to the CEO;
   - Krüger, Landier & Thesmar (2015): the cost of a single hurdle rate.
3. **Challenges to the "dark side" reading:** Whited (2001), Maksimovic & Phillips (2002), Hoang & Ruckes (2015), Gautier & Heider (2009).
4. **The economics of risk-capital allocation:**
   - Bauer & Zanjani (2016): Euler on ES can be economically inefficient;
   - Bauer & Zanjani (2021): dynamic RAROC;
   - Loebnitz & Roorda (2011): a liquidity-adjusted Euler principle, which answers the dossier's non-homogeneity problem.
5. **Capital charges under private information:** Baldenius, Dutta & Reichelstein (2007), with the sequential extension by Pfeiffer & Schneider.
6. **Academic FTP:** Dermine on FTP components, and on picking maturity by purpose (pricing, performance or hedging).
7. **Forecast incentives and budgeting behaviour:**
   - Witkowski et al. (2023) and Lichtendahl & Winkler (2007): competition breaks properness;
   - Fissler & Ziegel (2016): (VaR, ES) are jointly elicitable;
   - Evans et al. (2001): partial honesty;
   - Daumoser et al. (2018): a review of the budgetary-slack literature;
   - Graham (2022): internal forecasts are trusted only about two years ahead.
8. **Internal transfers inside fund families:** Gaspar, Massa & Matos (2006) on performance shifting through opposite trades, and Bhattacharya, Lee & Pool (2013) on internal liquidity insurance paid for by one pool.

### Challenges (detail in §5)
The literature most directly challenges eight dossier positions:
1. that ICM misallocation is established fact;
2. that even or pro-rata allocations are simply "socialism";
3. that winner-picking is costless;
4. that Euler-CVaR risk charges are economically right;
5. that ES should never be scored;
6. that hurdles should always equal the true shadow price;
7. that forecast inflation grows linearly with budget stakes;
8. that long-horizon group forecasts are credible fusion inputs.

### Evidence gaps
My searches found nothing on:
- internal capital markets *inside asset owners*, meaning allocation across a sovereign or pension fund's investment groups;
- liquidity transfer pricing at an asset owner, as opposed to a bank;
- forecast-scoring systems with pay consequences for institutional investment teams.

The dossier's transplant caveat (§8.8) stands.

---

## 2. Citation-integrity table (50 checked)

Status key:
- **found:** the metadata matches the version cited.
- **mismatched:** the work exists but some cited metadata is wrong; the corrected value is given.
- **Core 25:** marked ★ (the most load-bearing).

"n/a" in the Consensus column means no Consensus record exists in this session or in the sibling files. Corrected or confirmed metadata comes from Crossref unless marked [arXiv].

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| ★ Stein (1997), *JF* 52(1):111–133 | found | DOI 10.1111/j.1540-6261.1997.tb03810.x (CR 1,432). The abstract says ICMs "may sometimes function more efficiently" with "a small and focused set of projects". The dossier drops the hedge (as the verification log notes). | https://consensus.app/papers/details/6a07d86c178059559396b6c5f188a331/?utm_source=claude_desktop (from `08_action_valuation.lit.md`) |
| ★ Scharfstein & Stein (2000), *JF* 55(6):2537–2564 | found | DOI 10.1111/0022-1082.00299 (CR 1,218). "Preferential capital budgeting allocations" and "a kind of 'socialism'" are verbatim. | https://consensus.app/papers/details/75689033f1ce55ef910f66907b8387a8/?utm_source=claude_desktop (from `08_action_valuation.lit.md`) |
| ★ Rajan, Servaes & Zingales (2000), *JF* 55(1):35–80 | found | DOI 10.1111/0022-1082.00200 (CR 1,367). The SSRN abstract confirms the claims: funds go to "the most inefficient divisions"; 1979–1993. | n/a |
| ★ Shin & Stulz (1998), *QJE* 113(2):531–552 (WP: NBER 5639) | **mismatched (WP pointer only)** | The *QJE* metadata is correct: DOI 10.1162/003355398555676 (CR 810). **NBER w5639 is "An Analysis of Divisional Investment Policies" (1996)**, DOI 10.3386/w5639. Drop the WP pointer. | https://consensus.app/papers/details/c7c5bc16465b5f2b943974f4ed01132e/ (from the G8 verification log) |
| ★ Lamont (1997), *JF* 52(1):57–82 | **mismatched (pages)** | **Pages are 83–109**, DOI 10.1111/j.1540-6261.1997.tb03809.x (CR 836). Pages 57–82 are Carhart (1997). The abstract confirms the oil-shock finding verbatim. | n/a |
| ★ Glaser, Lopez-de-Silanes & Sautner (2013), *JF* 68(4):1577–1631 | found | DOI 10.1111/jofi.12046 (CR 127). The JF abstract in Crossref confirms that powerful managers get larger windfall allocations and overinvest. It lacks the "all unit managers systematically over-budget" and "about 40%" phrases; per the verification log those come from RePEc. | https://consensus.app/papers/details/848f600b945b589a8924c56d7af118ab/?utm_source=claude_desktop (from `08_action_valuation.lit.md`) |
| ★ Kuppuswamy & Villalonga (2016), *MS* 62(4):905–923 | found (subtitle omitted) | Full title adds "Evidence from the 2007–2009 Financial Crisis". DOI 10.1287/mnsc.2015.2165 (CR 281). The abstract confirms ICMs became "more valuable". | n/a |
| ★ Milgrom (1988), *JPE* 96(1):42–60 | found | DOI 10.1086/261523 (CR 428). Crossref holds no abstract, so the quoted "discretion of decision makers" remains unchecked. | n/a |
| ★ Harris & Raviv (1996), *JF* 51(4):1139–1174 | found | DOI 10.1111/j.1540-6261.1996.tb04065.x (CR 280). The abstract confirms under-investment when productivity is high and over-investment when it is low. The mechanism details stay [M]. | n/a |
| ★ Antle & Eppen (1985), *MS* 31(2):163–174 | found | DOI 10.1287/mnsc.31.2.163 (CR 391). The abstract confirms slack, rationing, and a cut-off rate above the market rate. | n/a |
| ★ Stoughton & Zechner (2007), *JFI* 16(3):312–342 | found | Title "Optimal capital allocation using RAROC™ and EVA®", DOI 10.1016/j.jfi.2006.12.004 (CR 71). | n/a |
| ★ Weitzman (1976), *Bell J. Econ.* 7(1):251–257 | found | DOI 10.2307/3003200 (CR 172). Crossref gives the start page only. Note: a published comment exists (Ekern 1979, *Bell J.* 10(2):720, DOI 10.2307/3003363). | n/a |
| ★ Weitzman (1980), *Bell J. Econ.* 11(1):302–308 | found | DOI 10.2307/3003414 (CR 306). | n/a |
| ★ Jensen (2003), *EFM* 9(3):379–406 | found | DOI 10.1111/1468-036x.00226 (CR 273). The abstract confirms both gaming channels: lying in budget formulation and gaming realization. | n/a |
| ★ Baumol & Fabian (1964), *MS* 11(1):1–32 | found | DOI 10.1287/mnsc.11.1.1 (CR 116). The "no prices" sentence is verbatim. The verification log's F5 notes the rebuttal by Maiti et al. (1973). | n/a. The rebuttal's record is https://consensus.app/papers/details/9af6dae07ffa5846b3f543e032a0a4da/ (from the G8 verification log). |
| ★ Hirshleifer (1956), *J. Business* 29(3):172–184 | found | DOI 10.1086/294110 (CR 340). No abstract in Crossref, so the content stays [M]. | n/a |
| ★ Stein (2002), *JF* 57(5):1891–1921 | found | DOI 10.1111/0022-1082.00483 (CR 1,931). The soft/hard information abstract is confirmed. | n/a |
| ★ Alonso, Dessein & Matouschek (2008), *AER* 98(1):145–179 | found | DOI 10.1257/aer.98.1.145 (CR 441). "Decentralization can dominate centralization even when coordination is extremely important" is verbatim. Add the corrigendum, *AER* 98(3):1195–1196 (DOI 10.1257/aer.98.3.1195). | n/a |
| ★ Tasche (2008), arXiv:0708.2542 | found [arXiv] | Single author. arXiv v1 is dated 19 Aug 2007, so "2008" refers to a later version (v3). The abstract confirms "adopted by many financial institutions". Crossref does not index it. | n/a |
| ★ Gneiting (2011), *JASA* 106(494):746–762 [M] | found; **remove [M]** | DOI 10.1198/jasa.2011.r10138 (CR 1,009); arXiv 0912.0902. | n/a |
| ★ Bracher, Ray, Gneiting & Reich (2021), *PLoS Comput Biol* 17(2):e1008618 | found | DOI 10.1371/journal.pcbi.1008618 (CR 325). | n/a |
| ★ Boutilier (2011/2012), arXiv:1106.2489 | found; venue note | arXiv v1 dated 13 Jun 2011. Crossref also lists a **2012 proceedings version, pp. 737–744, DOI 10.65109/jsvv3990** (CR 2). Its container label ("…Third International Joint Conference on Autonomous Agents and Multiagent Systems") is garbled. [Inference] It is probably the AAMAS 2012 paper; confirm before citing. | n/a |
| ★ Ben-David, Graham & Harvey (2013), *QJE* 128(4):1547–1584 | found | DOI 10.1093/qje/qjt023 (CR 737). The abstract confirms "more than 13,300" distributions and 36%. | https://consensus.app/papers/details/c521fdc6c47d5eb9bae7b451ebce14fc/?utm_source=claude_desktop (SSRN record; from `07_return_fusion.lit.md`) |
| ★ Smith & Winkler (2006), *MS* 52(3):311–322 | found | DOI 10.1287/mnsc.1050.0451 (CR 264). | https://consensus.app/papers/details/bfffdcbd36c45ee1b9b2dbf025b8cafc/?utm_source=claude_desktop (from `12_agentic_ai.lit.md` and `13_paper_deepread.lit.md`) |
| ★ Froot & Stein (1998), *JFE* 47(1):55–82 | found | DOI 10.1016/s0304-405x(97)00037-8 (CR 667). | n/a |
| Ozbas & Scharfstein (2010), *RFS* 23(2):581–599 | found | DOI 10.1093/rfs/hhp071 (CR 260; Crossref year 2009, online first). | https://consensus.app/papers/details/6cc2e034f8c95dc6b1bb978d3eb90e05/ (from the G8 verification log) |
| Graham, Harvey & Puri (2015), *JFE* 115(3):449–470 | found | DOI 10.1016/j.jfineco.2014.10.011 (CR 363). | n/a |
| Meyer, Milgrom & Roberts (1992), *JEMS* 1(1):9–35 | found | DOI 10.1111/j.1430-9134.1992.00009.x (CR 318). The abstract confirms "the prospect of organizational decline and layoffs creates additional influence costs in multiunit organizations". | n/a |
| Jagannathan, Matsa, Meier & Tarhan (2016), *JFE* 120(3):445–463 | found | DOI 10.1016/j.jfineco.2016.01.012 (CR 139). | n/a |
| Groves & Loeb (1979), *MS* 25(3):221–230 | found | DOI 10.1287/mnsc.25.3.221 (CR 139). The abstract confirms the dossier's description of the Groves-type evaluation measure. | n/a |
| Groves (1973), *Econometrica* 41(4):617–631 | found | DOI 10.2307/1914085 (CR 2,293). | n/a |
| Osband (1989), *JPE* 97(5):1091–1112 | found | DOI 10.1086/261644 (CR 47). | n/a |
| Crawford & Sobel (1982), *Econometrica* 50(6):1431–1451 | found; **orphan** | DOI 10.2307/1913390 (CR 3,216). Listed in §10 but never cited in the text. | n/a |
| Erel, Myers & Read (2015), *JFE* 118(3):620–635 | found | DOI 10.1016/j.jfineco.2014.10.006 (CR 35). | n/a |
| Brier (1950), *MWR* 78(1):1–3 | found | DOI as cited (CR 1,992). | n/a |
| Savage (1971), *JASA* 66(336):783–801 | found | DOI as cited (CR 799). | n/a |
| Gneiting & Raftery (2007), *JASA* 102(477):359–378 | found | DOI 10.1198/016214506000001437 (CR 4,715). | https://consensus.app/papers/details/cb608bdcfc4b52baa11789d9cfee6d2c/?utm_source=claude_desktop (from `07_return_fusion.lit.md`) |
| Chen, Kash, Ruberry & Shnayder (2014), *ACM TEAC* 2(2) [M] | found; **remove [M]** | Pages 1–27, DOI 10.1145/2556271 (CR 9). The abstract confirms the "completely mixed strategy" requirement. | n/a |
| Mellers et al. (2014), *Psych. Sci.* 25(5):1106–1115 | found | DOI as cited (CR 248); 13 authors, ending with Tetlock. | n/a |
| Goyal & Wahal (2008), *JF* 63(4):1805–1847 | found | DOI 10.1111/j.1540-6261.2008.01375.x (CR 172). | n/a |
| Fang, Ivashina & Lerner (2015), *JFE* 116(1):160–178 | found | DOI 10.1016/j.jfineco.2014.12.002 (CR 124). | https://consensus.app/papers/details/4e0c268caabc5b468d053656985a3deb/?utm_source=claude_desktop (from `02_endowment_swf.lit.md` and `G4_coinvest.lit.md`) |
| Braun, Jenkinson & Schemmerl (2020), *JFE* 136(1):44–62 | found | DOI 10.1016/j.jfineco.2019.01.009 (CR 63). | https://consensus.app/papers/details/74305f05d7e758dfbc4c1b624c2fa5db/?utm_source=claude_desktop (from `G4_coinvest.lit.md`) |
| Erel, Flanagan & Weisbach (2024), NBER WP 32278 | found | DOI 10.3386/w32278 (CR 27). Crossref shows no journal version. | n/a |
| Gompers, Kaplan & Mukharlyamov (2016), *JFE* 121(3):449–476 | found | DOI 10.1016/j.jfineco.2016.06.003 (CR 385). | n/a |
| Nadauld et al. (2019), NBER w22404 (in §10 entry 50) | found | Journal version: *JFE* 132(3):158–181, DOI 10.1016/j.jfineco.2018.11.007 (CR 90). Authors Nadauld, Sensoy, Vorkink, Weisbach. | n/a |
| Background: Denault (2001), Aumann–Shapley allocation | found; **upgrade** | "Coherent allocation of risk capital", *Journal of Risk* 4(1):1–34, DOI 10.21314/jor.2001.053 (CR 301). No abstract in Crossref. | n/a |
| Background: Holmström & Milgrom (1991), multitask incentives | found; **upgrade** | *JLEO* 7 (special issue):24–52, DOI 10.1093/jleo/7.special_issue.24 (CR 4,105). | n/a |
| Background: Matvos & Seru (2014) | found; **upgrade** | "Resource Allocation within Firms and Financial Market Dislocation: Evidence from Diversified Conglomerates", *RFS* 27(4):1143–1189, DOI 10.1093/rfs/hhu005 (CR 204). Annotated in §3. | n/a |
| Background: Jenkinson, Jones & Martinez (2016), *JF* 71(5), "abstract not available" | found; **abstract now retrieved** | "Picking Winners? Investment Consultants' Recommendations of Fund Managers", *JF* 71(5):2333–2370, DOI 10.1111/jofi.12289 (CR 101). Recommendations are "driven largely by soft factors", move flows, and show "no evidence that these recommendations add value". | n/a |
| Background: Tetlock (2005), *Expert Political Judgment* | found (edition note) | Princeton book; the Crossref record is the 2009 digital edition, DOI 10.1515/9781400830312. | n/a |

Not in scope: regulatory and practitioner documents (BCBS 2008, CEBS 2010, FSI 2011, Basel LCR40, Directive (EU) 2025/2, CPP, CalPERS, NZ Super, GIC, NBIM, Harvard Gazette, ILPA, CFR/USC, the Filbeck & Bok and Urwin & Hayman reports). The verification log checked them against primary text.

---

## 3. Annotated bibliography (25 papers)

Ordered by theme. "In dossier" marks whether the G8 dossier cites the paper. Links are exactly as returned. Counts are CR unless stated.

### 3.1 Decentralized investment management: the asset-owner ICM

**1. [Optimal Decentralized Investment Management](https://doi.org/10.1111/j.1540-6261.2008.01376.x)** [missed]
- **Record:** Jules H. van Binsbergen, Michael W. Brandt & Ralph S. J. Koijen · 2008 · *Journal of Finance* 63(4):1849–1895 · 130 cites · DOI 10.1111/j.1540-6261.2008.01376.x. In dossier: no.
- **Finding.** A CIO allocates capital to several asset-class managers, and the two-step process "can lead to large utility costs" through:
  - "loss of diversification";
  - "unobservable managerial appetite for risk";
  - "different investment horizons".

  The authors derive "an optimal unconditional linear performance benchmark". The CIO's uncertainty about managers' risk appetites "increases both the costs of decentralized investment management and the value of an optimally designed benchmark".
- **Relevance to ADIC.** This is the closest model to a CIO and TPA team allocating to seven groups. Each named misalignment is present at ADIC: PE's 10-year horizon against the overlay's monthly one, and opaque risk appetites in Capital Solutions and the overlay. [Inference] Derive group benchmarks from the total-portfolio program rather than hand-picking funding baskets, and report each group's cost of decentralization.

**2. [Decentralized Investment Management: Evidence from the Pension Fund Industry](https://doi.org/10.1111/jofi.12024)** [missed]
- **Record:** David Blake, Alberto G. Rossi, Allan Timmermann, Ian Tonks & Russ Wermers · 2013 · *Journal of Finance* 68(3):1133–1178 · 106 cites · DOI 10.1111/jofi.12024. In dossier: no.
- **Finding.**
  - Sponsors replaced generalist balanced managers with better-performing specialists.
  - They replaced single managers with multiple competing managers "to reduce scale diseconomies".
  - "Sponsors implement risk controls that trade off higher anticipated alphas of multiple specialists against the increased difficulty in coordinating their risk-taking and the greater uncertainty concerning their true skills."
  - The 2020 SSRN version (DOI 10.2139/ssrn.3612342) adds that sponsors allocate "reduced risk budgets to each manager", and that competition between specialists improves performance.
- **Relevance to ADIC.** Evidence from real asset owners for the dossier's core choice: quantity envelopes on risk, set centrally. [Inference] Per-group risk budgets should carry a coordination haircut, and a group whose skill is uncertain (low credibility Z) should get a smaller risk envelope as well as a lower fusion weight.

### 3.2 Newer internal-capital-market evidence

**3. [Resource Allocation within Firms and Financial Market Dislocation: Evidence from Diversified Conglomerates](https://doi.org/10.1093/rfs/hhu005)** [missed; dossier lists it as unverified background]
- **Record:** Gregor Matvos & Amit Seru · 2014 · *Review of Financial Studies* 27(4):1143–1189 · 204 cites · DOI 10.1093/rfs/hhu005. Abstract from the 2013 SSRN version, DOI 10.2139/ssrn.2209214. In dossier: background only.
- **Finding.**
  - Internal reallocation "provides an important force countervailing financial market dislocation".
  - In a structural model, "the weaker (stronger) division obtains too much (little) capital, as though it is 12 (9) percent more (less) productive than it really is".
  - "The cost of accessing external capital funds quadruples during extreme financial market dislocations."
- **Relevance to ADIC.** This puts magnitudes on two of the dossier's qualitative claims: socialism, and the value of the ICM in a crisis. [Inference]
  - Use 12% and 9% as outside priors for a socialism diagnostic on ADIC's allocation history.
  - Use "×4 external cost" as a stress prior for Corporate Finance's external-cost state variable (§4.1).
  - These are estimates for US conglomerates, not asset-owner parameters. Label them as such.

**4. [The Economics of Capital Allocation in Firms: Evidence from Internal Capital Markets](https://doi.org/10.1287/mnsc.2021.02755)** [missed; recent]
- **Record:** Daniel Hoang, Sebastian Gatzer & Martin Ruckes · 2025 · *Management Science* 71(8):6392–6425 · 16 cites · DOI 10.1287/mnsc.2021.02755. In dossier: no.
- **Finding** (CFO survey).
  - Top management counters divisional opportunism with "interconnected measures, including layers of approval, divisional budgets, reporting requirements, and compensation schemes".
  - Funding decisions rely heavily on nonfinancial information such as "the assessment of divisional managers' abilities".
  - "Substantial parts of the capital budget do not require top management approval."
  - "Even firms with active internal capital markets tilt capital allocation toward relatively even distributions, reflecting the use of capital allocation as a credible communication device."
  - Agency problems can cause capital rationing. CFOs report lower costs of capital and higher debt capacity from pooling.
- **Relevance to ADIC.** The most recent large-sample evidence on how headquarters actually allocates.
  - It supports the dossier's delegated envelopes and layered tiers.
  - It qualifies the dossier's reading of even allocations as "socialism" (§5).
  - It supports Corporate Finance's pooled borrowing capacity: the coinsurance channel.

**5. [A q Theory of Internal Capital Markets](https://consensus.app/papers/details/2311defdb8b152ab80b1442580fa023f/?utm_source=claude_desktop)** [missed] (Consensus URL from `08_action_valuation.lit.md`)
- **Record:** Min Dai, Xavier Giroud, Wei Jiang & Neng Wang · 2024 · *Journal of Finance* 79(2):1147–1197 · 21 cites (CS-saved: 9) · DOI 10.1111/jofi.13318. In dossier: no.
- **Finding.** In a dynamic model of a multi-division firm with costly external finance:
  - (i) within-firm allocation depends on divisions' risk as well as their productivity;
  - (ii) firms "may voluntarily spin off productive divisions to increase liquidity";
  - (iii) diversification can reduce value in low-liquidity states;
  - (iv) "corporate socialism makes liquidity less valuable";
  - (v) division investment is set by the ratio of marginal q to the marginal value of cash.
- **Relevance to ADIC.** [Inference] This is a formal basis for the dossier's pricing. A group invests while its marginal value exceeds Corporate Finance's marginal value of cash, which is the liquidity dual. Selling *good* assets to raise liquidity can be optimal, so SELL scoring should not penalize it. Socialism also lowers the value of the liquidity buffer.

**6. [Divisional Managers and Internal Capital Markets](https://doi.org/10.1111/jofi.12003)** [missed]
- **Record:** Ran Duchin & Denis Sosyura · 2013 · *Journal of Finance* 68(2):387–429 · 238 cites · DOI 10.1111/jofi.12003. In dossier: no.
- **Finding** (S&P 500 divisional managers).
  - Managers socially connected to the CEO "receive more capital". Connections "outweigh measures of managers' formal influence".
  - Under weak governance, connections reduce investment efficiency and firm value "via favoritism".
  - Under high information asymmetry, connections raise efficiency and value "via information transfer".
- **Relevance to ADIC.** This supports the dossier's recusal and override logs. [Inference] Firewalls can cost information in ADIC's most opaque books (overlay, Capital Solutions). Log influence channels rather than cutting them.

**7. [The WACC Fallacy: The Real Effects of Using a Unique Discount Rate](https://doi.org/10.1111/jofi.12250)** [missed]
- **Record:** Philipp Krüger, Augustin Landier & David Thesmar · 2015 · *Journal of Finance* 70(3):1253–1285 · 138 cites · DOI 10.1111/jofi.12250. In dossier: no.
- **Finding.** With a single discount rate, conglomerates "underinvest (overinvest) in relatively safe (risky) divisions". Division investment rises with division relative risk. When the bidder's beta is lower than the target's, announcement returns are significantly lower.
- **Relevance to ADIC.** Evidence for the dossier's holding-specific funding baskets and risk-specific charges. [Inference] Using ADIC's 10% return target as a common hurdle for all groups would tilt capital toward the riskiest groups (co-investment, venture-heavy PE).

### 3.3 Challenges to the "dark side" reading

**8. [Is It Inefficient Investment that Causes the Diversification Discount?](https://doi.org/10.1111/0022-1082.00385)** [missed; challenge]
- **Record:** Toni M. Whited · 2001 · *Journal of Finance* 56(5):1667–1691 · 340 cites · DOI 10.1111/0022-1082.00385. In dossier: no.
- **Finding.** After correcting for measurement error in Tobin's q, "I find no evidence of inefficient allocation of investment". Earlier results "appear to be artifacts of measurement error and of the correlation between investment opportunities and liquidity".
- **Relevance to ADIC.** The dossier's misallocation evidence (Rajan–Servaes–Zingales, Shin & Stulz, Ozbas & Scharfstein) leans on q-type proxies. Present it as contested, and test for socialism on ADIC's own data.

**9. [Do Conglomerate Firms Allocate Resources Inefficiently Across Industries? Theory and Evidence](https://doi.org/10.1111/1540-6261.00440)** [missed; challenge]
- **Record:** Vojislav Maksimovic & Gordon Phillips · 2002 · *Journal of Finance* 57(2):721–767 · 610 cites · DOI 10.1111/1540-6261.00440. In dossier: no.
- **Finding.** In a profit-maximizing model, "a conglomerate discount is consistent with profit maximization". On plant-level data, "the majority of conglomerate firms exhibit growth across industry segments that is consistent with optimal behavior".
- **Relevance to ADIC.** The neoclassical counterweight to Scharfstein & Stein. [Inference] Uneven or sticky group budgets are not proof of agency problems. Diagnose them against the optimizer's own allocation before treating them as rent-seeking.

**10. [Informed Headquarters and Socialistic Internal Capital Markets](https://doi.org/10.1093/rof/rfu018)** [missed; challenge]
- **Record:** Daniel Hoang & Martin Ruckes · 2015 (Crossref online year 2014) · *Review of Finance* 19(3):1105–1141 · 16 cites · DOI 10.1093/rof/rfu018. In dossier: no.
- **Finding.** Headquarters has private information about divisions' productivities, so today's allocation signals future allocations. "To facilitate effort provision", headquarters biases allocation so as not to reveal productivity differences, which produces socialism as an optimal choice. The bias varies over time.
- **Relevance to ADIC.** [Inference] Some smoothing of group budgets can be rational: it keeps weaker groups exerting effort. The dossier's ±50% price collar has no counterpart for *envelopes*; add one, and separate bounded smoothing from entitlement.

**11. [The Benefit and Cost of Winner-Picking: Redistribution versus Incentives](https://doi.org/10.1628/093245609789919603)** [missed; challenge]
- **Record:** Axel Gautier & Florian Heider · 2009 · *Journal of Institutional and Theoretical Economics* 165(4):622–649 · 6 cites · DOI 10.1628/093245609789919603. In dossier: no.
- **Finding.** Winner-picking "adds an extra layer of noise to the moral-hazard problem". Managers with strong future opportunities "anticipate that headquarters will bail them out should they fail to produce enough resources themselves", which "reduces incentives to create the resources in the first place".
- **Relevance to ADIC.** [Inference] Redeploying dry powder toward Secondaries and Capital Solutions in a drought (dossier §2.1, §6.3) weakens the incentive of cash-generating groups to generate cash.
  - The dossier's provider credits (§6.4) are the right counter. Make them explicit and pre-committed.
  - Charge groups for internal bail-out liquidity at Corporate Finance's price.

### 3.4 Risk-capital allocation

**12. [The Marginal Cost of Risk, Risk Measures, and Capital Allocation](https://doi.org/10.1287/mnsc.2015.2190)** [missed; challenge]
- **Record:** Daniel Bauer & George H. Zanjani · 2016 · *Management Science* 62(5):1431–1457 · 45 cites · DOI 10.1287/mnsc.2015.2190. In dossier: no.
- **Finding.**
  - The authors derive the marginal cost of risk from economic fundamentals, then identify the risk measure that delivers it. "The resulting measure depends on context," and claimants' risk preferences "determine how the correct risk measure must weight various default states".
  - Risk measures for pricing and performance measurement "should be chosen based on economic fundamentals and may not necessarily adhere to the mathematical properties typically imposed".
  - The 2011 SSRN version (DOI 10.2139/ssrn.1787145) states that Euler on Expected Shortfall "generally yields economically inefficient allocations".
- **Relevance to ADIC.** This directly challenges the dossier's default risk charge, $\lambda_R\,\partial\mathrm{CVaR}/\partial x_i$ (§6.4). [Inference] Derive the risk row from the owner's preferences, such as failing to meet distribution demand $D_t$ or breaching the 7% floor, and test whether Euler-CVaR prices agree.

**13. [Economic capital and RAROC in a dynamic model](https://doi.org/10.1016/j.jbankfin.2021.106071)** [missed]
- **Record:** Daniel Bauer & George Zanjani · 2021 · *Journal of Banking & Finance* 125:106071 · 12 cites · DOI 10.1016/j.jbankfin.2021.106071. Abstract from Semantic Scholar [S2]. In dossier: no.
- **Finding.** Moving from a static to a dynamic model changes two things. "Capital" should be defined broadly "to include the continuation value of the firm", and cash-flow valuations must reflect "company effective risk aversion". The dynamic changes are "practically significant", though "static approximations with a properly calibrated company risk aversion are quite accurate".
- **Relevance to ADIC.** A multi-period basis for the risk charge in ADIC's multi-period optimizer. [Inference] Calibrate $\lambda_R$ as ADIC's state-dependent effective risk aversion from the optimizer's duals, not from the Solvency II 4.75% rate. This is also what verification-log R15 asks. Include the value of the continuing commitment program in "capital".

**14. [Liquidity Risk Meets Economic Capital and RAROC](https://doi.org/10.2139/ssrn.1853233)** [missed]
- **Record:** Kolja Loebnitz & Berend Roorda · 2011 · SSRN working paper · 1 cite · DOI 10.2139/ssrn.1853233. In dossier: no.
- **Finding.**
  - A "liquidity cost profile" measures illiquidity at balance-sheet level and gives liquidity-adjusted risk measures.
  - "Convexity and positive super-homogeneity of risk measures is preserved under the liquidity adjustment, while coherence is not, reflecting the common idea that size does matter."
  - The paper addresses "the liquidity-adjustment of the well known Euler allocation principle".
- **Relevance to ADIC.** The dossier leaves an "unallocated residual" because liquidity metrics are not homogeneous (§1.4, §6.4; verifier 11-R6). [Inference] This offers a principled alternative. Build ADIC's liquidity cost profile from secondary-sale and NAV-loan cost curves (streams 05 and 08), then allocate with the liquidity-adjusted Euler rule.

### 3.5 Capital charges under private information

**15. [Cost Allocation for Capital Budgeting Decisions](https://doi.org/10.2308/accr.2007.82.4.837)** [missed; challenge]
- **Record:** Tim Baldenius, Sunil Dutta & Stefan Reichelstein · 2007 · *The Accounting Review* 82(4):837–867 · 50 cites · DOI 10.2308/accr.2007.82.4.837. Abstract from the 2006 SSRN version. In dossier: no.
- **Finding.**
  - Divisions report project profitability, and project acceptance is tied to depreciation plus capital charges.
  - For a common asset, the paper derives a sharing rule among users.
  - The hurdle rate "deviates from the firm's cost of capital in a manner that depends crucially on whether the coordination problem is one of implementing a common asset or choosing among multiple competing projects".
  - "More severe divisional agency problems will increase the hurdle rate for common assets, yet this is generally not true for competing projects."
- **Relevance to ADIC.** [Inference] ADIC has both cases. Groups compete for envelope capacity, which is competing projects. They also share the liquidity buffer and Corporate Finance's facilities, which are common assets. The dossier's rule that "hurdles should be the true shadow prices" (§2.3) fits the first case. For the shared buffer, theory allows an agency-adjusted charge; run it as a sensitivity on the CLC.

### 3.6 Funds transfer pricing

**16. [Fund Transfer Pricing for Deposits and Loans, Foundation and Advanced](https://consensus.app/papers/details/59596c9dbc355d4a93f649ba14e8e1fc/?utm_source=claude_desktop)** [missed] (Consensus URL from `06_leverage.lit.md`)
- **Record:** Jean Dermine · 2012 SSRN (DOI 10.2139/ssrn.2069917; CR 4) and 2011 SSRN (DOI 10.2139/ssrn.1944129). CS-saved record: 2011, *The Journal of Financial Perspectives*, 18 cites. In dossier: no.
- **Finding.** After the crisis, FTP must handle five previously ignored issues:
  - interbank rationing;
  - the cost of "a Basel III contingency liquidity buffer";
  - credit-risk-specific transfer prices;
  - "a liquidity premium in the case of long-term funding";
  - consistent treatment of the bank's own credit spread.
- **Relevance to ADIC.** The academic counterpart to the dossier's CEBS and FSI template, and a component checklist for **Corporate Finance's** curve (§4.7). A companion paper, Dermine (2016, DOI 10.2139/ssrn.2722392), says the right maturity depends on whether the price is used for "pricing, evaluation of performance, and hedging". That supports the dossier's split between decision prices and vintage-locked performance charges.

### 3.7 Forecast incentives, elicitation and budgeting behaviour

**17. [Incentive-Compatible Forecasting Competitions](https://consensus.app/papers/details/4e78c77d15a55452942b3ca0721c296a/?utm_source=claude_desktop)** [missed; challenge] (Consensus URL from `07_return_fusion.lit.md`)
- **Record:** Jens Witkowski, Rupert Freeman, Jennifer Wortman Vaughan, David M. Pennock & Andreas Krause · 2023 · *Management Science* 69(3):1354–1374 · 12 cites · DOI 10.1287/mnsc.2022.4410. AAAI 2018 version: DOI 10.1609/aaai.v32i1.11471. In dossier: no.
- **Finding.** Proper scoring rules elicit truth "if all forecasters are paid according to their scores". Incentives become distorted "if only the best-scoring forecaster wins a prize", because extreme reports raise the chance of the top score. The paper introduces competition mechanisms that are incentive compatible and select the most accurate forecaster with higher probability than any other.
- **Relevance to ADIC.** The dossier cites Osband (1989) for the value of competition and bans league tables. Witkowski et al. show *how* competition must be designed. With Lichtendahl & Winkler (2007; §3.9), this means:
  - any recognition, bonus pool or budget tied to "best forecaster" status breaks properness;
  - if ADIC wants competition, use an incentive-compatible mechanism. [Inference]

**18. [Higher order elicitability and Osband's principle](https://doi.org/10.1214/16-aos1439)** [missed; challenge]
- **Record:** Tobias Fissler & Johanna F. Ziegel · 2016 · *Annals of Statistics* 44(4):1680–1707 · 409 cites · DOI 10.1214/16-aos1439. In dossier: no (the verification log mentions it).
- **Finding.** Functionals that are not elicitable on their own can be components of a higher-order elicitable functional. "The pair (Value at Risk, Expected Shortfall) is jointly elicitable under mild conditions that are usually fulfilled in risk management applications."
- **Relevance to ADIC.** This overturns the dossier's "never for an expected shortfall to be scored" (§2.7). [Inference] For the overlay's tail-hedge payoffs and the opportunistic book's P&L, elicit and score (VaR, ES) jointly with a consistent joint scoring function.

**19. [Honesty in Managerial Reporting](https://doi.org/10.2308/accr.2001.76.4.537)** [missed; challenge]
- **Record:** John H. Evans, R. Lynn Hannan, Ranjani Krishnan & Donald V. Moser · 2001 · *The Accounting Review* 76(4):537–559 · 363 cites · DOI 10.2308/accr.2001.76.4.537. In dossier: no.
- **Finding** (three experiments). "Subjects often sacrifice wealth to make honest or partially honest reports, and they generally do not lie more as the payoff to lying increases." There is less honesty when the contract gives the manager a smaller share of the surplus.
- **Relevance to ADIC.** The dossier's incentive layer predicts inflation $\delta^*=bZB'/(2s)$, rising linearly in the stake $b$ (§6.5). The experiments contradict the linearity. [Inference] Estimate $\delta$ from the registry rather than assuming it from $b$. Perceived fairness of how surplus is split, including group pay against total-fund pay, affects honesty.

**20. [Honesty in budgeting: a review of morality and control aspects in the budgetary slack literature](https://doi.org/10.1007/s00187-018-0267-z)** [missed; review]
- **Record:** Christian Daumoser, Bernhard Hirsch & Matthias Sohn · 2018 · *Journal of Management Control* 29(2):115–159 · 23 cites · DOI 10.1007/s00187-018-0267-z. Abstract from the 2015 SSRN version (DOI 10.2139/ssrn.2670165). In dossier: no.
- **Finding.** In a structured review of top-tier accounting and business-ethics journals:
  - "less slack is created under truth-inducing pay schemes compared to slack-inducing schemes";
  - information asymmetry increases slack, moderated by participation and information systems;
  - "fairness and reputation concerns decrease budgetary slack, but ethics concerns do not";
  - social norms decrease slack, and peer influence moderates the effect.
- **Relevance to ADIC.** A survey-level evidence base for the dossier's incentive and IC norms (§6.5–6.6), which so far rest on theory. [Inference] Reputation (an information-value display) and fairness levers work; appeals to ethics do not.

**21. [Presidential Address: Corporate Finance and Reality](https://doi.org/10.1111/jofi.13161)** [missed; challenge]
- **Record:** John R. Graham · 2022 · *Journal of Finance* 77(4):1975–2049 · 209 cites · DOI 10.1111/jofi.13161. In dossier: no.
- **Finding** (CFO surveys, compared with 20 years earlier). Companies use decision rules that are "conservative, sticky, and geared to time the market". They "rely on internal forecasts that are miscalibrated and considered reliable only two years ahead".
- **Relevance to ADIC.** The dossier fuses 5–10-year group IRR forecasts with a credibility weight (§6.5). [Inference] Make credibility horizon-dependent, with Z capped beyond about 8 quarters. Weight the fast-resolving companion forecasts the dossier already specifies more heavily than long-horizon IRRs.

### 3.8 Internal transfers within fund families

**22. [Favoritism in Mutual Fund Families? Evidence on Strategic Cross-Fund Subsidization](https://doi.org/10.1111/j.1540-6261.2006.00830.x)** [missed]
- **Record:** José-Miguel Gaspar, Massimo Massa & Pedro Matos · 2006 · *Journal of Finance* 61(1):73–104 · 466 cites · DOI 10.1111/j.1540-6261.2006.00830.x. In dossier: no.
- **Finding.** Fund families "strategically transfer performance across member funds". "High family value" funds outperform at the expense of "low value" funds. Preferential IPO allocations and "opposite trades across member funds" partly explain the gap.
- **Relevance to ADIC.** Large-sample evidence for the risk the dossier's §6.7 guards against. Internal trades at off-market prices move measured performance between units; E8 shows "$50m of fake alpha". [Inference] Monitor opposite-direction internal trades and their timing, beyond pricing each transfer at fair value.

**23. [Conflicting Family Values in Mutual Fund Families](https://doi.org/10.1111/j.1540-6261.2012.01797.x)** [missed]
- **Record:** Utpal Bhattacharya, Jung H. Lee & Veronika K. Pool · 2013 · *Journal of Finance* 68(1):173–200 · 157 cites · DOI 10.1111/j.1540-6261.2012.01797.x. In dossier: no.
- **Finding.** Affiliated funds of mutual funds "provide an insurance pool against temporary liquidity shocks to other funds in the family". The family benefits because funds avoid fire sales, but "the cost of this insurance is borne by the investors" in the providing funds.
- **Relevance to ADIC.** [Inference] ADIC's equivalent is one group supplying liquidity to another, for example Public Markets redemptions funding PE calls, or Secondaries absorbing PE-group stakes. It is valuable to the total portfolio and costly to the provider. This is the empirical case for CEBS's "compensate the providers of liquidity" (dossier §2.5) and for logging internal liquidity provision as a priced flow.

### 3.9 Cited papers whose abstracts matter for the design

**24. [Eliciting Predictions and Recommendations for Decision Making](https://doi.org/10.1145/2556271)** [cited; [M] can be removed]
- **Record:** Yiling Chen, Ian A. Kash, Michael Ruberry & Victor Shnayder · 2014 · *ACM Transactions on Economics and Computation* 2(2):1–27 · 9 cites · DOI 10.1145/2556271. In dossier: yes.
- **Finding.** "Strictly proper decision making requires the decision maker use a completely mixed strategy to choose an action." Instead, asking a single expert to *recommend* an action can elicit the decision maker's most preferred action "for a broad class of preferences", including expected-value maximization.
- **Relevance to ADIC.** [Inference] The IC will not randomize approvals, so group forecasts that drive budgets cannot be strictly proper. This strengthens the dossier's shadow-tracking of declined deals. It also suggests registering a recommendation (SELL, HOLD, REFINANCE or LEVER) alongside each P10/P50/P90, and scoring it.

**25. [Incentives in a Divisionalized Firm](https://doi.org/10.1287/mnsc.25.3.221)** [cited]
- **Record:** Theodore Groves & Martin Loeb · 1979 · *Management Science* 25(3):221–230 · 139 cites · DOI 10.1287/mnsc.25.3.221. In dossier: yes.
- **Finding.** The centre acts as if reports are truthful. Each manager is evaluated on own realized profit "less the reported impact of the change in coordinating decisions (resulting from his message) on the profits of the other divisions". Truthful communication is then best "regardless of the messages of all others". The setting assumes perfect information and no risk-sharing problems.
- **Relevance to ADIC.** [Inference] The dossier's net α* after dual-priced charges is a Groves-type measure only if charges are computed from the group's own report, using with-and-without re-solves for lumpy items. The abstract's assumptions (perfect knowledge, no risk aversion) are exactly what ADIC lacks, so treat it as a benchmark, not a guarantee.

### 3.10 Also noted (one line each)

| # | Paper (link as returned) | Record | Finding (from abstract) or status | Use for ADIC [inference] |
|---|---|---|---|---|
| A1 | [Decentralized Investment Management](https://doi.org/10.1111/j.1540-6261.1981.tb00436.x) | W. F. Sharpe · 1981 · *JF* 36(2):217–234 · CR 129 | No abstract retrieved. The seminal paper on multi-manager delegation. | Background for §3.1 |
| A2 | [Probability Elicitation, Scoring Rules, and Competition Among Forecasters](https://consensus.app/papers/details/fe4cb9e41fbf5cd596aa6cfd0ce34799/?utm_source=claude_desktop) (CS-saved, `07_return_fusion.lit.md`) | K. C. Lichtendahl & R. L. Winkler · 2007 · *MS* · DOI 10.1287/mnsc.1070.0729 · CS-saved 64; SSRN DOI 10.2139/ssrn.961001 | Per the saved record: relative-performance concerns lead to more extreme reports; joint scoring rules based on business sharing are strictly proper | No rank-based rewards; consider shared scores |
| A3 | [The Wisdom of Competitive Crowds](https://doi.org/10.2139/ssrn.1926330) | K. C. Lichtendahl, Y. Grushka-Cockayne & P. E. Pfeifer · 2011 SSRN · CR 1. CS-saved record: https://consensus.app/papers/details/d3dea0152fe4520392dce33f9b9d0a8c/?utm_source=claude_desktop. Journal version not confirmed here | Competing forecasters "exaggerate their private information", which makes the competitive crowd's average more accurate than the truthful crowd's | Debias individual group forecasts before fusing; averages may still be informative |
| A4 | [The Effects of Trust and Budget-Based Controls on Budget Gaming and Budget Value](https://doi.org/10.2139/ssrn.2201249) | T. Libby & M. Lindsay · 2013 SSRN · CR 7 | High budget emphasis goes with more gaming; trust between levels goes with less; good prior performance goes with less gaming | Keep budget emphasis out of pay; trust matters as much as mechanism |
| A5 | [Empirical tests of budget ratcheting and its effect on managers' discretionary accrual choices](https://doi.org/10.1016/s0165-4101(01)00044-1) | A. J. Leone & S. Rock · 2002 · *JAE* 33(1):43–67 · CR 157 | SSRN abstract (DOI 10.2139/ssrn.173228): asymmetric ratcheting in business-unit data | Supports the dossier's no-ratchet rule (§6.3 step 5) |
| A6 | [Target Ratcheting and Achievability of Earnings Targets](https://doi.org/10.2139/ssrn.2654475) | M. D. Mahlendorf, M. Matějka & U. Schäffer · 2015 SSRN · CR 7 | Good performance raises next targets but also raises the chance of meeting them; consistent with "commitment" overcoming the ratchet effect | Publish how outcomes feed envelopes; commitment, not abolition, may suffice |
| A7 | [Target ratcheting and effort reduction](https://doi.org/10.1016/j.jacceco.2010.07.002) | J. Bouwens & P. Kroos · 2011 · *JAE* 51(1–2):171–185 · CR 141 | No abstract retrieved | Re-check in Consensus |
| A8 | [The Hidden Effect of Historical Information on Managerial Honesty in Participative Budgeting](https://doi.org/10.2139/ssrn.4506830) | M. Altenburger · 2023 SSRN · CR 0 | Managers report more honestly when past cost budgets were low than when high; "motivated reasoning" rather than anchoring | Show the re-solved envelope, not last year's, as the reference point |
| A9 | [Picking Winners: Managerial Ability and Capital Allocation](https://doi.org/10.2139/ssrn.4601628) | A. Benz, P. R. Demerjian, D. Hoang & M. E. Ruckes · 2023 SSRN · CR 0 | More able division managers get "substantially larger capital allocations", more so under better governance, and it "creates firm value" | Evidence-based credibility (Z) can legitimately steer budgets |
| A10 | [An Economic Approach to Capital Allocation](https://doi.org/10.1111/j.1539-6975.2010.01354.x) | G. Zanjani · 2010 · *JRI* 77(3):523–549 · CR 31 | SSRN abstract (DOI 10.2139/ssrn.1151455): the allocation "adds up"; marginal rules fix capital for marginal units, but "inframarginal units of coverage may in general receive different assignments" | Theory for keeping marginal decision prices separate from legacy (vintage) charges |
| A11 | [To split or not to split: Capital allocation with convex risk measures](https://doi.org/10.1016/j.insmatheco.2008.03.007) | A. Tsanakas · 2009 · *IME* 44(2):268–277 · CR 82 | No abstract retrieved | Candidate method for non-homogeneous (convex) measures; re-check |
| A12 | [Static and dynamic risk capital allocations with the Euler rule](https://doi.org/10.21314/jor.2019.420) | T. J. Boonen · 2019 · *Journal of Risk* · CR 4 | No abstract retrieved | Candidate for multi-period Euler; re-check |
| A13 | [Intertemporal Cost Allocation and Managerial Investment Incentives: A Theory Explaining the Use of Economic Value Added as a Performance Measure](https://doi.org/10.1086/262093) | W. P. Rogerson · 1997 · *JPE* 105(4):770–795 · CR 256 | No abstract retrieved | Background for the vintage-FTP performance charge |
| A14 | [Cost Allocation for Capital Budgeting Decisions Under Sequential Private Information](https://doi.org/10.2139/ssrn.1308846) | T. Pfeiffer & G. T. Schneider · 2008 SSRN · CR 0 | Extends #15 to multi-round funding with abandonment options. The charge rate on the initial joint investment is below (above) the cost of capital if divisions later compete (cooperate). Implemented with linear residual-income contracts | Capital calls are multi-round funding; charge design depends on whether groups later compete |
| A15 | [Fund Transfer Pricing for Bank Deposits. The Case of Products with Undefined Maturity](https://doi.org/10.2139/ssrn.2722392) | J. Dermine · 2016 SSRN · CR 1 | Maturity choice depends on the context: "pricing, evaluation of performance, and hedging" | Supports two price sets (decision against performance) |
| A16 | [Cost of Liquidity and Fund Transfer Pricing](https://doi.org/10.1002/9781118818466.ch11), ch. 11 of *Measuring and Managing Liquidity Risk* | A. Castagna & F. Fede (book authors; chapter authors not in Crossref) · 2013 · Wiley · pp. 425–471 · book CR 30 | No abstract retrieved | Practitioner reference for Corporate Finance's FTP build |
| A17 | [Cross Trading by Investment Advisers: Implications for Mutual Fund Performance](https://doi.org/10.2139/ssrn.2022808) | L. Casavecchia & A. Tiwari · 2013 SSRN · CR 0 | Funds of top-quintile cross-trading advisers underperform the bottom quintile "by 1% per year"; higher commissions are a major source | Cap and disclose internal-transfer volume |
| A18 | [Trading out of sight: An analysis of cross-trading in mutual fund families](https://doi.org/10.1016/j.jfineco.2018.12.005) | A. Eisele, T. Nefedova, G. Parise & K. Peijnenburg · 2020 · *JFE* 135(2):359–378 · CR 45 | No abstract retrieved | Re-check in Consensus |
| A19 | [Predation versus Cooperation in Mutual Fund Families](https://doi.org/10.2139/ssrn.2082369) | A. Eisele, T. Nefedova & G. Parise · 2012 SSRN · CR 0 | Sibling funds "front-run their distressed siblings", which is "the outcome of a coordinated strategy" | Internal "help" can be predation; the firewall (§6.7 rule 4) is warranted |
| A20 | [Fund Management Company Governance and Strategic Cross-Fund Subsidization](https://doi.org/10.2139/ssrn.4741861) | J. Xu & Y. Zhu · 2024 SSRN · CR 0 | Subsidization "continues even after it was forbidden by the regulator in 2011"; better governance reduces it | Rules alone are insufficient; the transfer pricing committee's independence matters |
| A21 | [Ambiguity and the Corporation: Group Disagreement and Underinvestment](https://consensus.app/papers/details/349a3e540a9f507c999fa811de9d8775/?utm_source=claude_desktop) (CS-saved, `14_ic_deliberation.lit.md`) | L. Garlappi et al. · 2017 · *JFE* · DOI 10.1016/j.jfineco.2017.06.005 · CS-saved 64 | Per the saved record: group decisions with heterogeneous beliefs are dynamically inconsistent and underinvest | Pre-committed contingent budgets (dossier §6.3) are the right response |
| A22 | [Incentive contrats [sic] and strictly proper scoring rules](https://doi.org/10.1007/bf02595735) | R. T. Clemen · 2002 · *Test* 11(1):167–189 · CR 14 | No abstract retrieved | Directly on topic; re-check |
| A23 | [Influence and inefficiency in the internal capital market](https://doi.org/10.1016/j.jebo.2009.07.001) | J. Wulf · 2009 · *JEBO* 72(1):305–321 · CR 99 | No abstract retrieved | Influence costs in ICMs; re-check |
| A24 | [Integration, organizational processes, and allocation of resources](https://doi.org/10.1016/j.jfineco.2004.01.003) | O. Ozbas · 2005 · *JFE* 75(1):201–242 · CR 90 | No abstract retrieved | Re-check |
| A25 | [Capital budgeting and compensation with asymmetric information and moral hazard](https://doi.org/10.1016/s0304-405x(01)00065-4) | A. E. Bernardo, H. Cai & J. Luo · 2001 · *JFE* 61(3):311–344 · CR 175 | No abstract retrieved | Joint design of budgets and pay; re-check |
| A26 | [Underestimating Costs in Public Works Projects: Error or Lie?](https://doi.org/10.1080/01944360208976273) | B. Flyvbjerg, M. S. Holm & S. Buhl · 2002 · *JAPA* 68(3):279–295 · CR 1,110 | No abstract retrieved | Strategic misrepresentation in forecasts; re-check |
| A27 | [Do Financial Constraints Affect Internal Capital Markets?](https://doi.org/10.2139/ssrn.968305) | G. Hovakimian · 2007 SSRN · CR 0 | Facing higher external capital costs, "firms tend to increase the efficiency of their internal capital markets" | Same direction as Kuppuswamy & Villalonga, and Matvos & Seru |

---

## 4. Missed-but-important papers: design implications

All rows are **[inference]** unless a source result is quoted. Numbers from corporate studies are outside priors, to be labelled as such and never presented as ADIC data.

### 4.1 State variables to add (dossier §6.2)

| Variable | Definition | Basis | Owner | Use |
|---|---|---|---|---|
| **External-capital cost multiplier** $\xi_t$ | Cost of outside liquidity (secondary discount, NAV-loan spread, facility availability) relative to normal | "External capital … quadruples during extreme financial market dislocations" (#3); ICMs gain value and efficiency when outside capital is costly (Kuppuswamy & Villalonga, cited; A27) | Corporate Finance | Scales the value of internal redeployment and triggers contingent budgets. Enters Corporate Finance's FTP curve. |
| **Horizon-dependent credibility** $Z_{g,h}$ | Credibility per group and forecast horizon, capped beyond about 8 quarters | Internal forecasts "considered reliable only two years ahead" (#21) | Validator | Replaces the single $Z_g$ in the fusion |
| **Risk-appetite uncertainty** $\sigma^{RA}_g$ | Dispersion of a group's realized risk against its mandate | CIO uncertainty about risk appetite raises the cost of decentralization (#1); skill uncertainty drives sponsors' risk controls (#2) | TPA / CRO | Shrinks the group's risk envelope; weights its benchmark design |
| **Influence log** | Who advocated for each envelope change; connections; recusals | Connections increase capital, harmful under weak governance (#6) | IC secretariat | Audit of envelope changes and overrides |
| **Internal liquidity-provision ledger** $L^{prov}_{g\to g',t}$ | Liquidity one group supplies another, with its opportunity cost | Internal insurance pools carry a cost borne by the provider (#23) | Corporate Finance | Credits providers at the FTP price |
| **Transfer-direction monitor** | Opposite-direction internal trades and their timing around measurement dates | Performance shifting via "opposite trades across member funds" (#22); cross-trading costs (A17) | Validator / pricing committee | Flags patterns beyond single-transfer fair-value tests |
| **Continuation value** $CV_t$ | Value of the continuing commitment program, counted in "capital" | Capital should "include the continuation value of the firm" (#13) | TPA | Risk-capital denominator; $\lambda_R$ calibration |

### 4.2 Models

1. **Optimal group benchmarks** (#1).
   - Solve for each group's linear benchmark that minimizes the CIO's (TPA's) utility loss from delegation. Inputs: loss of diversification, risk-appetite uncertainty $\sigma^{RA}_g$ and horizon mismatch.
   - Output: benchmark = funding basket + correction.
   - Report the "cost of decentralization" per group alongside the envelope.
2. **Socialism diagnostic** (#3, with challenges from #8 and #9).
   - Regress changes in group allocations on fused α*, risk and *other groups'* cash flows.
   - Express the residual tilt as productivity-equivalent wedges and compare them with the 12%/9% outside prior.
   - Because q-based evidence is contested (#8), use the optimizer's own allocation as the benchmark, not market proxies.
3. **Liquidity-ratio allocation rule** (#5).
   - The group invests while its marginal value exceeds Corporate Finance's marginal value of cash. This is the dossier's "net α* > charge", now with a theoretical basis.
   - Add the "sell a productive asset for liquidity" branch explicitly to SELL scoring.
4. **Risk row derived from the owner** (#12).
   - Build the risk constraint's state weights from the owner's loss function: failing to meet $D_t$, breaching the floor, forced sales. Do not default to generic CVaR.
   - Compare Euler-CVaR charges with marginal costs from the derived measure, and report the gap to the IC.
5. **Liquidity-adjusted Euler allocation** (#14).
   - Build a liquidity cost profile from secondary-sale and NAV-loan cost curves (streams 05 and 08).
   - Allocate liquidity-adjusted risk with the adjusted Euler rule. This replaces the dossier's "unallocated residual" with an allocation that has a principled basis.
6. **Dynamic RAROC** (#13).
   - Set $\lambda_R$ to the optimizer's state-dependent effective risk aversion, from the dual of the risk row.
   - Use Solvency II's 4.75% only as a sanity bound. This resolves verification-log R15.
7. **Charges for shared capacity** (#15, A14).
   - Model the liquidity buffer and portfolio facilities as common assets. Test an agency-adjusted charge against the pure dual as a sensitivity.
   - For multi-round commitments (capital calls), the charge on the initial commitment depends on whether groups later compete for or share capacity.

### 4.3 Parameters and priors (outside priors; label them as such)

| Parameter | Prior | Source | Note |
|---|---|---|---|
| Socialism wedge | Weaker group as if +12% productive; stronger group as if −9% | #3 (US conglomerates) | Diagnostic prior only |
| External-cost stress multiplier $\xi$ | ×4 in extreme dislocation | #3 | Calibrate to ADIC's secondary and NAV-loan data (streams 05 and 08) |
| Credibility horizon cap | Z declines beyond about 8 quarters | #21 | The dossier already scores 4- and 8-quarter companions |
| Inflation response to stakes | Not linear in $b$; estimate from the registry | #19, #20, A4 | Replaces the analytical $\delta^*$ as a calibration target |
| Coordination haircut on summed risk budgets | Positive; size to be calibrated | #2, #1 | Interacts with verifier R1 (joint feasibility of bands) |

### 4.4 Constraints

- **Joint risk budgets:** $\sum_g R_g \le R^{tot} - \text{coordination buffer}$ (#2, #1). This also addresses verification-log R1, where per-group bands are not jointly feasible.
- **Envelope-change collars:** a limit on quarter-on-quarter envelope changes, matching the dossier's ±50% price collar (#10, #4).
- **Internal transfers:**
  - fair-value pricing (already in the dossier);
  - a volume cap and disclosure (A17);
  - blackout windows (already in the dossier);
  - a ban on opposite-direction trade pairs within a window (#22).
  - Governance strength matters as much as the rule (A20).

### 4.5 Objectives and charges

- **Risk-specific hurdles everywhere** (#7). The dossier's holding-level funding baskets are right. No single "10% hurdle" should be used to compare groups.
- **Corporate Finance's FTP components** (#16):
  - a contingency-buffer cost;
  - a term liquidity premium by liquidity tenor;
  - credit-specific adjustments, for example for Capital Solutions' and Private Credit's inflows;
  - ADIC's own borrowing spread on facility-funded positions.
  - Choose maturity by purpose (A15): decision prices use the liquidity tenor; performance charges use the vintage lock.
- **Provider credits and no free bail-outs** (#11, #23). Credit cash-generating and liquidity-supplying groups at the FTP price. Charge recipients of internal liquidity. This restores the incentive that winner-picking erodes.

### 4.6 Agent and IC design

- **Forecast registry agent:**
  - register a recommendation (SELL, HOLD, REFINANCE or LEVER) with each P10/P50/P90 (#24);
  - elicit (VaR, ES) jointly for overlay books (#18);
  - apply horizon-dependent credibility (#21).
- **No winner-take-all forecasting recognition** (#17, A2). If ADIC wants competition, use an incentive-compatible mechanism. The fusion agent should debias each group's report before averaging (A3).
- **IC norms:**
  - keep budget emphasis low in pay and build trust (A4, #20);
  - use reputation and fairness levers, not ethics appeals (#20);
  - show re-solved envelopes, not last year's, as the anchor (A8).
- **Influence controls:** keep recusal and override logs (#6). Do not cut information channels for the most opaque groups; log them instead.
- **Delegation:** a substantial share of capital decided below the top is normal practice (#4), consistent with the dossier's Tier C.

### 4.7 Organization: Corporate Finance owns FTP (user-confirmed)

- **What the user confirmed.** Corporate Finance owns Treasury. Per context §1A it also owns:
  - the liquidity buffer;
  - the contingency funding plan;
  - internal transfer pricing;
  - portfolio facilities;
  - overlay collateral;
  - owner distributions.
- **What this answers.** Dossier open question 3 (§9), and it means the dossier's role table (§6.1) should split its "TPA and Treasury desk":
  - **Corporate Finance (Treasury):** publishes the FTP curve; holds the mismatch and buffer P&L; runs the contingency funding plan; credits liquidity providers (#23). FSI 2011 (cited) recommends a central, treasury-run FTP.
  - **TPA team:** computes duals, envelopes and benchmarks (#1), and runs the socialism diagnostic.
  - **Validator / CRO office:** owns the registry and the transfer pricing committee.
- **The curve's components.** Corporate Finance's curve should rise with the external-cost state $\xi_t$ (#3). Its components follow Dermine (#16).
- **Secondaries as a hybrid book (user-confirmed).** Its direct secondary deals can buy stakes in PE-group funds, which makes it the main internal-transfer channel. The fund-family evidence (#22, A17, A19, A20) supports the dossier's §6.7 rules and adds two more: volume monitoring and checks for opposite-direction trades.

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier recommendation (§) | Challenging paper(s) | What the evidence says | Suggested response [inference] |
|---|---|---|---|---|
| 1 | ICM misallocation evidence presented as established; magnitudes "do not transfer", but the mechanisms do (§1.1, §2.1, §4) | Whited 2001 (#8); Maksimovic & Phillips 2002 (#9) | Inefficiency results "appear to be artifacts of measurement error"; most conglomerates grow in ways "consistent with optimal behavior" | Present the misallocation evidence as contested. Diagnose ADIC against its own optimizer before invoking socialism. |
| 2 | Pro-rata pacing cuts and entitlement-like budgets read as "socialism" to be removed; groups as price-takers (§2.1, §3.1) | Hoang & Ruckes 2015 (#10); Hoang, Gatzer & Ruckes 2025 (#4) | Biased, even allocation can be optimal to sustain effort; firms with active ICMs tilt toward even distributions as "a credible communication device" | Allow bounded smoothing with envelope collars. Separate smoothing (allowed) from entitlement (not). |
| 3 | Winner-picking as a value source; redeploy dry powder to Secondaries and Capital Solutions in a drought (§1.1, §2.1, §6.3) | Gautier & Heider 2009 (#11) | Anticipated bail-outs reduce incentives to "create the resources in the first place" | Make provider credits explicit and pre-committed. Charge groups for internal bail-out liquidity. |
| 4 | Euler allocation of CVaR for risk budgets and charges (§1.4, §2.6, §6.4) | Bauer & Zanjani 2016 (#12) | Euler on ES "generally yields economically inefficient allocations" (SSRN); the risk measure should follow claimants' preferences | Derive the risk row from the owner's loss function. Report the gap between Euler-CVaR and marginal-cost charges. |
| 5 | "Never for an expected shortfall to be scored" (§2.7) | Fissler & Ziegel 2016 (#18) | (VaR, ES) is "jointly elicitable under mild conditions" | Score (VaR, ES) jointly for overlay forecasts. |
| 6 | "Hurdles should be the true shadow prices … do not also inflate the hurdle" (§2.3) | Baldenius, Dutta & Reichelstein 2007 (#15); Pfeiffer & Schneider 2008 (A14) | Under private information, optimal hurdles deviate from the cost of capital; agency raises the hurdle for *common* assets but not generally for competing projects | Keep duals for competing proposals. For the shared buffer and facilities, run an agency-adjusted charge as a sensitivity. |
| 7 | Inflation $\delta^*=bZB'/(2s)$, linear in stake $b$ (§6.5) | Evans et al. 2001 (#19); Daumoser et al. 2018 (#20); Libby & Lindsay 2013 (A4) | People often report honestly or partially honestly, and do not lie more as payoffs rise; fairness, reputation and trust cut slack; budget emphasis raises gaming | Estimate $\delta$ from the registry. Use the formula only for direction. Keep the trust-building norms. |
| 8 | P10/P50/P90 forecasts of multi-year IRRs as fusion inputs with a single credibility $Z_g$ (§6.5) | Graham 2022 (#21) | Internal forecasts are "miscalibrated and considered reliable only two years ahead" | Horizon-dependent credibility; cap Z beyond about 8 quarters. |
| 9 | Osband (1989): "competition between agents is worth much more than self-screening" (§2.3) | Witkowski et al. 2023 (#17); Lichtendahl & Winkler 2007 (A2) | Winner-take-all competition distorts reports toward extremes unless the mechanism is designed to be incentive compatible | Competition only through incentive-compatible mechanisms. The ban on league tables already points this way. |
| 10 | Firewall on conflicted inputs; group heads present but recused (§6.6, §6.7) | Duchin & Sosyura 2013 (#6) (nuance, not contradiction) | Connections hurt under weak governance but *help* under high information asymmetry | Keep recusal. Log influence channels for opaque groups rather than cutting them. |

Papers that **support** the dossier: Matvos & Seru (#3), Kuppuswamy & Villalonga (cited), Krüger–Landier–Thesmar (#7), Blake et al. (#2), Gaspar et al. (#22), Bhattacharya et al. (#23), Leone & Rock (A5) and Dermine (#16, A15).

---

## 6. Verbatim usage message

Consensus returned this message on all three attempts. It is a monthly-quota rejection, not a rate limit:

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Search log

**Consensus**
- 3 attempts on one query ("Stein Internal capital markets and the competition for corporate resources"), 30 seconds apart, no filters. All three were quota-rejected, so **0 searches completed**.

**OpenAlex**
- 1 attempt: HTTP 429, `Retry-After: 46587`.

**Semantic Scholar**
- 1 relevance search and later a batch of 2 searches: all HTTP 429.
- 1 batch of 3 DOI look-ups. Bauer & Zanjani 2021 returned an abstract, which was used. Tsanakas 2009 returned 404. Bouwens & Kroos returned an empty abstract.

**arXiv API**
- 1 call for 4 IDs: 0708.2542, 0912.0902, 2005.12881 and 1106.2489.

**Crossref: 14 topical searches** (plain `query`, no filters, 6–12 rows each)

| # | Query | Seed or refinement | Useful hits |
|---|---|---|---|
| 1 | internal capital markets | Seed | Hovakimian (A27); Yan WP; mostly low-cited SSRN items |
| 2 | winner picking conglomerates capital allocation | Seed | Gautier & Heider (#11); Benz et al. (A9) |
| 3 | liquidity transfer pricing banks | Seed | Castagna & Fede ch. 11 (A16); Lindblom & Elliot WP (no abstract) |
| 4 | funds transfer pricing FTP liquidity premium contingent liquidity buffer cost allocation business lines | Refinement of 3 | Same as 3; recall weak |
| 5 | Euler risk capital allocation | Seed | Boonen 2019 (A12); Saita book chapters (no abstracts) |
| 6 | proper scoring rules incentive compatible forecasting | Seed | Clemen 2002 (A22) |
| 7 | scoring rules decision making experts predictions decision markets incentive to misreport | Refinement of 6 | Weak; Carvalho 2015 and Karimi & Dimitrov 2018 (not used) |
| 8 | budget gaming forecasts managers | Seed | Libby & Lindsay (A4) |
| 9 | honesty in managerial reporting participative budgeting slack experiment | Refinement of 8 | Evans et al. (#19); Daumoser et al. (#20); Altenburger (A8) |
| 10 | target ratcheting effort reduction performance targets managers empirical | Refinement of 8 | Bouwens & Kroos (A7); Leone & Rock (A5); Mahlendorf et al. (A6) |
| 11 | decentralized investment management multiple asset class managers optimal benchmarks pension fund | Refinement (asset-owner ICM) | Blake et al. (#2) |
| 12 | cross-trading mutual fund families strategic cross-fund subsidization internal trades | Refinement (internal transfers) | Gaspar et al. (#22); Xu & Zhu (A20) |
| 13 | resource allocation within firms financial market dislocation diversified conglomerates internal capital markets crisis | Refinement of 1 | Matvos & Seru (#3) |
| 14 | WACC fallacy single firm-wide discount rate divisions investment distortion conglomerates | Refinement (hurdles) | Krüger, Landier & Thesmar (#7) |

**Crossref: title and DOI look-ups (about 110)**
- **Citation checks:** all 50 academic works in §2, using DOI where the dossier gives one and `query.bibliographic` otherwise, plus DOI checks for the page conflict (Carhart, …tb03808.x) and the NBER w5639 title.
- **Candidates proposed from my background knowledge, then confirmed in Crossref:** van Binsbergen–Brandt–Koijen; Sharpe; Maksimovic & Phillips; Whited; Duchin & Sosyura; Hoang & Ruckes; Hoang–Gatzer–Ruckes; Graham 2022; Bauer & Zanjani (2016, 2021); Loebnitz & Roorda (found as a hit in the BZ 2021 look-up); Zanjani 2010; Tsanakas; Denault; Rogerson; Baldenius–Dutta–Reichelstein (Pfeiffer & Schneider found as a hit); Fissler & Ziegel; Holmström & Milgrom; Bhattacharya–Lee–Pool; Eisele et al.; Wulf; Ozbas; Bernardo et al.; Flyvbjerg et al.; Jenkinson et al.; Witkowski et al.
- **Taken from sibling reviews, then confirmed in Crossref:** Dai et al.; Dermine; Lichtendahl & Winkler; Lichtendahl et al.

**WebSearch / WebFetch**
- Not used.
