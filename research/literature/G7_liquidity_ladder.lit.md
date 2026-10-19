# G7 literature check: cross-group liquidity management and stress (liquidity ladder)

**Dossier checked:** `research/groups/dossiers/G7_liquidity_ladder.md` (as of 2026-10-18). Its §10 "Academic" list has 10 works. The body names 4 more methods without reference entries, and the "Market data" list holds one BIS research bulletin. The dossier was not edited.
**Date:** 2026-10-18.
**Companion:** `research/groups/verification/G7_liquidity_ladder.verify.md` (the "verification log", VL).

> **Blocker: Consensus could not be used in this run (monthly quota).**
> - **Consensus.** My first query (Robinson & Sensoy) was rejected three times, 30 seconds apart, with the monthly-quota message in §6. After moving on, one call on the next query (the Li–Strahan–Zhang title) was rejected the same way. The quota resets on 1 November 2026. **No Consensus search completed.** Sibling streams G3, G4 and G6 hit the same limit earlier today.
> - **OpenAlex:** HTTP 429. The daily credit is exhausted (`Retry-After: 46608` seconds, about 13 hours).
> - **Semantic Scholar** (one of Consensus's source indexes) was throttled but usable. 7 of 12 topical searches attempted there completed after back-off, and both batch abstract look-ups completed.
> - **Crossref** worked throughout.
> - **Consequence.** The only Consensus URLs in this file are records that sibling streams saved earlier today. I copied them exactly as those files recorded them, tagged **[CS-saved: stream]**. All other links are DOI or Semantic Scholar URLs exactly as Crossref or Semantic Scholar returned them.

**Fallbacks (disclosed)**
1. **Semantic Scholar [S2]:** 7 topical searches (plain query, no filters, one at a time) and 2 batch look-ups covering 27 identifiers, for abstracts.
2. **Crossref [CR]:** 7 topical searches (5 of them as fallbacks when S2 returned HTTP 429), 16 title searches and 42 DOI look-ups. Crossref holds abstracts only where publishers deposit them: usually OUP, Wiley, INFORMS, CUP and SSRN, but not Elsevier.
3. **Saved Consensus records [CS-saved]:** I indexed the 1,166 unique Consensus URLs saved in sibling literature and verification files and reused 34 of them here. Findings attributed to these records restate the abstract summaries the sibling streams wrote down; I did not re-read those abstracts.
4. **WebSearch ×1 and WebFetch ×1 [WS/WF]:** used only for the Duffie & Ziegler (2003) abstract, which neither Crossref nor S2 holds. I fetched it from the IDEAS/RePEc record.
5. **The VL**, which fetched primary PDFs. Its extraction of the IMF WP/12/3 title page settled that paper's author list.

**Reading conventions**
- **[Inference]** marks reasoning that goes beyond what a record or abstract states.
- I read abstracts only, no full texts.
- Citation counts carry their source: **CS** = the Consensus count recorded by the sibling stream; **CR** = Crossref `is-referenced-by`; **S2** = Semantic Scholar. All were read on 2026-10-18.
- Codes: **B1–B25** are the annotated papers (§3), **F1–F24** further records (§4.7) and **C1–C8** challenges (§5).

**Organizational mapping (user-confirmed, 2026-10-18; context §1A)**
- Secondaries is a hybrid of direct and fund investments. Capital Solutions is the structured and hybrid capital group.
- **Corporate Finance owns Treasury.** That covers the liquidity gate, the contingency funding plan (CFP), internal transfer pricing, portfolio-level borrowing and facilities, overlay collateral (VM/IM) and distributions to the owner. The seven groups run the asset side.
- What this means for G7:
  - §6.11 of the dossier says a "central Treasury … reports to the CIO and IC". It should name **Corporate Finance**, with the Treasurer's seat on the shadow IC.
  - Every funding-side lever in the dossier's policy ladder is a Corporate Finance action: facilities, the Treasury band, the collateral pool, and draw timing agreed with the owner. Pacing cuts and hedge-fund redemptions are group actions that must clear Corporate Finance's gate.
  - The literature below on facilities (B14–B18), collateral (B10–B13), the owner (B24–B25) and CFP governance (F15) therefore lands on Corporate Finance.

---

## 1. Summary

### Citation integrity
- **Scope: 15 academic works.**
  - The 10 works in the dossier's "Academic" list.
  - 4 methods named in the body without a reference entry: Glasserman–Kang–Kang, Gerber–Shiu, Little's law and Clopper–Pearson.
  - The Schrimpf, Shin & Sushko *BIS Bulletin*. The dossier lists it under "Market data", but SSRN indexes it like a working paper.
  - **Not counted:**
    - Fleming & Ruela, a *Liberty Street Economics* blog post. Crossref does not index it; the VL confirmed its content.
    - Official and practitioner sources, which the VL covers (28 claims confirmed, 6 corrected).
- **Result: 15 found, 0 mismatched, 0 not found.** There are no hallucinated references, which agrees with the VL.
- **But the reference metadata is thin:**
  - **8 entries omit or truncate titles.**
    - Titles omitted: Robinson–Sensoy, Brunnermeier–Pedersen, Bolton–Chen–Wang, Ang–Papanikolaou–Westerfield, Nadauld et al. and Schrimpf–Shin–Sushko.
    - Titles truncated: Li–Strahan–Zhang and Acharya–Steffen.
  - **4 body-named methods have no §10 entry.**
  - **Miller–Orr is tagged [nrv].** It is now verified: *QJE* 80(3):413–435, DOI 10.2307/1880728.
  - **Nadauld et al. lacks volume and pages:** *JFE* 132(3):158–181.
- **Content checks against abstracts.** Six dossier claims were checked against the papers' abstracts, and all hold:
  - Ang et al.: investors would "forgo 2% of their wealth";
  - Bolton–Chen–Wang: the double barrier;
  - Acharya–Steffen: the two phases of the dash for cash;
  - Li–Strahan–Zhang: record line draws in March 2020;
  - Schrimpf–Shin–Sushko: "points to forced selling";
  - Brunnermeier–Pedersen: "mutually reinforcing" (confirmed by stream 08).
- **Two claims need qualifying:**
  - **Gorton–Metrick.** The haircut spike they document was in *bilateral* repo. In tri-party repo, margins were "surprisingly stable" (B16).
  - **Li–Strahan–Zhang.** Their own abstract says banks could meet the 2020 line draws because of Fed liquidity programs, deposit inflows and strong capital. The dossier does not carry that condition into its facility assumptions (C2).

### Backfill
- **Method.** 14 topical searches: 5 seeds and 9 refinements (log in §7).
- **Result.** §3 annotates **25 papers, none cited in the dossier**. §4.7 lists **24 further records**.
- **The dossier's academic base is 10 papers. Seven clusters are missing:**
  1. **Which assets to sell first (B1–B4).** This is the most important gap. Classic theory (Duffie & Ziegler 2003; Brown, Carlin & Lobo 2010) and new evidence (Chaderina et al. 2026; IMF 2020) find a liquid-first sale order to be myopic, and costly in the tail.
  2. **Measurement:** liquidity-at-risk on the same scenarios as solvency, liquidity-adjusted value, and the frequency and severity of liquidity events (B5–B9).
  3. **Collateral liquidity of derivative overlays (B10–B13).** Calls can exceed 6% of total assets (Jansen et al., *RFS* 2026). 13–33% of derivative-using funds lack buffers (Jukonis et al.).
  4. **How reliable contingent funding is in a crisis (B14–B18).** Credit lines get costlier and scarcer in aggregate stress. Stressed lenders reprice lines. Repo runs are quantity runs, not haircut runs.
  5. **Hedge-fund redemption rights valued as options, and gates as run triggers (B19–B20).**
  6. **What liquidity is worth to an investor with payouts and commitments, and how fast pacing works as a lever (B21–B23).**
  7. **How sponsors behave in stress (B24–B25).** Governments withdrew more than US$211bn from SWFs in 2020–21. Endowments cut payouts after losses.
- **Academic work on CFP design is thin.** The searches returned practitioner book chapters and one 2026 SSRN paper on board governance of the CFP (F15). The dossier's regulatory backbone (SR 10-6, Reg YY, FSB) remains the right source.

### Challenges (detail in §5)
1. **Liquid-first pecking order (§2.4, §6.9):** B1–B4.
2. **Facilities as a dependable recourse tier in the joint stress** (TPF; policy B): B14, B15, B18, and the Li–Strahan–Zhang abstract.
3. **Pacing cuts as a fast lever** (policy C): B23.
4. **Owner-agreed draw flexibility** (policy D): B24, B25.
5. **Repo haircut stress** taken from the 2007–08 run: B16.
6. **"The price of safety is low"**, measured by mean wealth: B21.
7. Tail-hedge monetization as step 2 (weak): F11, B12.
8. Liquidity budgets may be too conservative (weak, and pointing the other way): F23.

**Synthesis [Inference].** The dossier's headline, "policy levers dominate asset levers", rests on three levers: facilities, pacing and owner flexibility. The literature finds each of them weakest in the joint stress state that the dossier itself identifies as the dangerous one. The architecture survives: the ladder, the nested recourse tiers, the stage machine and the CFP testing regime. What should change is the waterfall logic and the parameters of those three levers.

---

## 2. Citation-integrity table

**Status key**
- **found:** the work exists, and every stated element (authors, year, venue, volume) matches.
- **incomplete:** found, but the title, pages or a reference entry is missing or truncated. This is not a mismatch.

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| Ref 21. Robinson, D. T., & Sensoy, B. A. (2016). *JFE* 122(3), 521–543; NBER WP 17428 | found [CS-saved: 03, 04][CR]; incomplete (no title) | "Cyclicality, performance measurement, and cash flow liquidity in private equity", *JFE* 122(3):521–543, DOI 10.1016/j.jfineco.2016.09.008 (CS 203; CR 182). WP: NBER 2011, DOI 10.3386/w17428. Consensus, CR and S2 hold no abstract. The VL confirmed the "liquidity providers (sinks)" quote from the NBER abstract. | https://consensus.app/papers/details/86bf821b6ba65861a9da20fed7862965/?utm_source=claude_desktop |
| Ref 22. Li, L., Strahan, P. E., & Zhang, S. (2020). "Banks as Lenders of First Resort." *RCFS* 9(3); NBER WP 27256 | found [CR]; incomplete (title truncated) | "Banks as Lenders of First Resort: Evidence from the COVID-19 Crisis", *RCFS* 9(3):472–500, DOI 10.1093/rcfs/cfaa009 (CR 290). The abstract confirms record line draws in March 2020. It adds that Fed liquidity programs, deposit inflows and strong pre-shock capital "explain why banks were able to accommodate these liquidity demands" (see C2). | none |
| Ref 23. Acharya, V. V., & Steffen, S. (2020). "The Risk of Being a Fallen Angel and the Corporate Dash for Cash." *RCFS* 9(3); NBER WP 27601 | found [CR]; incomplete (title truncated) | The full title adds "in the Midst of COVID". *RCFS* 9(3):430–471, DOI 10.1093/rcfs/cfaa013 (CR 440). The abstract confirms the two phases quoted in §4.2(3). | none |
| Ref 24. Gorton, G., & Metrick, A. (2012). "Securitized banking and the run on repo." *JFE* 104(3); NBER WP 15223 | found [CS-saved: 06][CR] | *JFE* 104(3):425–451, DOI 10.1016/j.jfineco.2011.03.016 (CS 1,687; CR 1,468). No abstract in CR or S2. **Scope note for §2.5:** the haircut spike was in bilateral repo; tri-party margins stayed "surprisingly stable" for most borrowers (B16). | https://consensus.app/papers/details/1731101d29a15c0da2c78761804fb43d/?utm_source=claude_desktop |
| Ref 25. Schmieder, Hesse, Neudorfer, Puhr & Schmitz (2012). *Next Generation System-Wide Liquidity Stress Testing*. IMF WP/12/3 | found [CR][VL] | IMF Working Paper 2012/003, DOI 10.5089/9781475502466.001 (CR 8). The PDF title page lists the five authors as the dossier cites them. Crossref adds two names (Andre Santos, Salih Neftci); treat that as a Crossref metadata error, not a dossier error. Add the DOI. | none |
| Ref 26. Brunnermeier, M., & Pedersen, L. H. (2009). *RFS* 22(6) | found [CS-saved: 06, 08][CR]; incomplete (no title) | "Market Liquidity and Funding Liquidity", *RFS* 22(6):2201–2238, DOI 10.1093/rfs/hhn098 (CS 5,153; CR 4,060). Stream 08 confirmed that "mutually reinforcing" appears in the abstract. | https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop |
| Ref 27. Bolton, P., Chen, H., & Wang, N. (2011). *JF* 66(5); linked to NBER w14845 | found [CS-saved: 08, 09][CR]; incomplete (no title) | "A Unified Theory of Tobin's q, Corporate Investment, Financing, and Risk Management", *JF* 66(5):1545–1578, DOI 10.1111/j.1540-6261.2011.01681.x (CR 671; CS 716 on the WP record). The abstract confirms an "endogenous double-barrier policy" and the "marginal value of liquidity (cash and credit line)". | https://consensus.app/papers/details/e303976b52515556ab7c0f0476889f19/?utm_source=claude_desktop |
| Ref 28. Ang, A., Papanikolaou, D., & Westerfield, M. (2014). *Management Science* 60(11) | found [CS-saved: VL, 02, 09][CR]; incomplete (no title) | "Portfolio Choice with Illiquid Assets", *MS* 60(11):2737–2761, DOI 10.1287/mnsc.2014.1986 (CS 171; CR 135). The abstract confirms investors would "forgo 2% of their wealth to hedge against illiquidity crises occurring once every 10 years". | https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop |
| Ref 29. Nadauld, T., Sensoy, B., Vorkink, K., & Weisbach, M. (2019). *JFE*; linked to NBER w22404 | found [CS-saved: VL, 05][CR][S2]; incomplete (no title, volume or pages) | "The liquidity cost of private equity investments: Evidence from secondary market transactions", *JFE* 132(3):158–181, DOI 10.1016/j.jfineco.2018.11.007 (CS 66; CR 90). | https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop |
| Ref 30. Miller, M. H., & Orr, D. (1966). "A model of the demand for money by firms." *QJE* 80(3) [nrv] | found [CR][S2]; **upgrade from [nrv]** | *QJE* 80(3):413–435, DOI 10.2307/1880728 (CR 846; S2 1,425). No abstract is available, so the "band with replenishment" reading in §2.4 was not checked against the text. | none |
| §7 "Glasserman–Kang–Kang conditional means [S→10]" (no §10 entry) | found [CS-saved: 10][CR]; incomplete (no entry) | Glasserman, P., Kang, C., & Kang, W., "Stress scenario selection by empirical likelihood", *Quantitative Finance* 15(1):25–41 (online 2014), DOI 10.1080/14697688.2014.926019 (CR 56; S2 71). Add a §10 entry. | https://consensus.app/papers/details/dfb066c744f9534f9354125656683f26/?utm_source=claude_desktop |
| §2.6 "Gerber–Shiu severity budgets [S→C1]" (no §10 entry) | found [CR]; incomplete (no entry) | Gerber, H. U., & Shiu, E. S. W. (1998), "On the Time Value of Ruin", *NAAJ* 2(1):48–72, DOI 10.1080/10920277.1998.10595671 (CR 679). The program synthesis lists the same paper. No sibling stream checked it in Consensus. Add a §10 entry. | none |
| §2.6 "Little's law" [I] (no §10 entry) | found [CR]; incomplete (no entry) | Little, J. D. C. (1961), "A Proof for the Queuing Formula: L = λW", *Operations Research* 9(3):383–387, DOI 10.1287/opre.9.3.383 (CR 2,435). The abstract proves L = λW only if the three means are finite and the processes "strictly stationary". [Inference] A crisis breaks stationarity, so use the law for normal-state throughput only. | none |
| §6.4 "Clopper–Pearson bounds (C1 D12)" (no §10 entry) | found [CR]; incomplete (no entry) | Clopper, C. J., & Pearson, E. S. (1934), "The use of confidence or fiducial limits illustrated in the case of the binomial", *Biometrika* 26(4):404–413, DOI 10.1093/biomet/26.4.404 (CR 4,267). | none |
| Ref 20. Schrimpf, A., Shin, H. S., & Sushko, V. (2 Apr 2020). *BIS Bulletin* 2 (no title) | found [CR]; incomplete (no title) | "Leverage and margin spirals in fixed income markets during the Covid-19 crisis". SSRN record, DOI 10.2139/ssrn.3761873 (CR 70). Its abstract contains the dossier's quote: evidence "points to forced selling of treasury securities by investors who had attempted to exploit small yield differences through the use of leverage". | none |

*Noted, not counted:* Ref 19, Fleming & Ruela (2020), *Liberty Street Economics*. It is a blog post and Crossref does not index it. The VL fetched the page and confirmed all three statistics.

**Fixes for §10**
1. Complete the 8 incomplete titles and the Nadauld et al. volume and pages, using the table above. Add DOIs throughout.
2. Add entries for the 4 body-named methods: Glasserman–Kang–Kang, Gerber–Shiu, Little and Clopper–Pearson.
3. Upgrade Miller–Orr from [nrv].
4. **§2.5:** qualify "Repo haircuts rose in the 2007–08 run" as bilateral repo, and cite Copeland, Martin & Walker (B16) alongside it.
5. **§4.2(3):** carry over Li–Strahan–Zhang's own condition, that 2020 line performance depended on Fed support and deposit inflows. [Inference] That condition may not hold in an oil- or fiscal-specific ADIC stress.

---

## 3. Annotated bibliography (25 papers, none cited in the dossier)

### 3.1 Which assets to sell first (B1–B4)

**B1. [Liquidation Risk](https://doi.org/10.2469/faj.v59.n3.2530)** [S2][CR][WS/WF]
- **Record:** Darrell Duffie & Alexandre Ziegler · 2003 · *Financial Analysts Journal* 59(3):42–51 · CR 42; S2 30 · DOI 10.2469/faj.v59.n3.2530. The abstract excerpts come from the IDEAS/RePEc record via WebFetch; neither Crossref nor S2 holds the abstract.
- **Finding:** Having to liquidate while bid–ask spreads widen "causes significant increases in risk measures": insolvency likelihood, VaR and expected tail loss, especially with fat-tailed returns. The alternative is to "sell illiquid assets first while keeping a 'cushion' of cash and liquid assets for a 'rainy day'". That raises expected transaction costs but can cut tail losses and the probability of insolvency.
- **Relevance to ADIC:** This directly tests the dossier's step order (§6.9: Treasury, then overlay, P2S, long-only … and PE and co-investment last).
  - [Inference] Evaluate the cash-last alternative in the policy simulator (P). The dossier's own reverse stress finds slow-burn failures, which is exactly when a cushion matters.

**B2. [Optimal Portfolio Liquidation with Distress Risk](https://doi.org/10.1287/mnsc.1100.1235)** [CR]
- **Record:** David B. Brown, Bruce Ian Carlin & Miguel Sousa Lobo · 2010 · *Management Science* 56(11):1997–2014 · CR 73 · DOI 10.1287/mnsc.1100.1235 (SSRN 10.2139/ssrn.1570223).
- **Finding:** A myopic investor with an immediate cash need "always prefers to sell more liquid assets". If a large downstream shock is possible, the non-myopic investor "unwinds positions more than immediately necessary". That investor keeps more of the low-temporary-impact (liquid) assets to hedge future distress, and sells strictly more of assets with a low ratio of permanent to temporary impact, "even if these assets are relatively illiquid".
- **Relevance to ADIC:** This is the formal version of the dossier's own finding that "the drought loads the gun; the crisis pulls the trigger" (86–99% of first red events fall in crisis quarters).
  - [Inference] In a drought, raise liquidity early through planned tail-end and LP-interest sales and term funding. Do not drain Treasury and Public Markets toward the 4% floor first.
  - [Inference] It also suggests a parameterization: split each tier's cost into temporary impact (η) and permanent impact (signalling, and mark-downs on the rest of the book).

**B3. [The Dark Side of Liquid Bonds in Fire Sales](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop)** [CS-saved: 05][CR]
- **Record:** Maria Chaderina, Alexander Muermann & Christoph Scheuch · 2026 · *Management Science* (online; no volume yet) · CS 11; CR 1 · DOI 10.1287/mnsc.2023.03670.
- **Finding:** Selling the most liquid bonds "can backfire". When many investors sell the same widely held liquid bonds while buying capital is scarce, those bonds fall the most, and no seller internalizes the effect. Property and casualty (P&C) insurers sell liquid bonds first after catastrophes, and those bonds show the largest price declines.
- **Relevance to ADIC:** [Inference] ADIC's B0–B2 rungs (Treasuries, IG, DM equities, commingled long-only funds) are what other SWFs, pensions and funds also sell first in a demand bust.
  - The stress haircuts in §6.3 (2%, 10%, 1.5%) need a crowding term that rises with aggregate forced selling.
  - Stream 05 applies the same logic to quality-buyout LP interests.

**B4. [The Behavior of Fixed-income Funds during COVID-19 Market Turmoil](https://doi.org/10.5089/9781513563695.064)** [S2][CR]
- **Record:** Frank Hespeler & Felix Suntheim · 2020 · IMF *Analytical Notes* 20(02) · CR 0; S2 7 · DOI 10.5089/9781513563695.064.
- **Finding:** In March 2020, funds facing redemptions "predominantly shed liquid assets first — for example, cash, cash equivalents, and US Treasury securities". Those forced sales amplified price pressure and drained liquidity across fixed-income markets until central banks intervened.
- **Relevance to ADIC:** It supplies the mechanism behind the Treasury-depth collapse the dossier cites (Fleming–Ruela; Schrimpf–Shin–Sushko).
  - [Inference] Make B0–B1 depth depend on aggregate fund redemptions.
  - [Inference] ADIC's commingled long-only funds will be doing the same selling at the same time.

### 3.2 Measuring liquidity under stress (B5–B9)

**B5. [Liquidity at risk: Joint stress testing of solvency and liquidity](https://consensus.app/papers/details/73c5a80bdb8c5f408aabc6305a0cdf9d/?utm_source=claude_desktop)** [CS-saved: 03][CR][S2]
- **Record:** Rama Cont, Artur Kotlicki & Laura Valderrama · 2020 · *Journal of Banking & Finance* 118:105871 · CS 48; CR 45 · DOI 10.1016/j.jbankfin.2020.105871.
- **Finding (S2 abstract):** The paper derives liquidity shocks endogenously from solvency shocks, so both are stressed on one consistent scenario. It defines "Liquidity at Risk" as "the liquidity resources required for a financial institution facing a stress scenario". Funding costs arising from liquidity needs can amplify equity losses.
- **Relevance to ADIC:** It supports the dossier's LaR (§2.2, §6.5) and adds the missing feedback loop.
  - [Inference] For ADIC the solvency-to-liquidity links are NAV-linked owner draws, facility LTV cures and VM on synthetic beta.
  - [Inference] The liquidity-to-solvency link is the cost of recourse: secondary discounts and facility spreads reduce NAV.
  - [Inference] Compute LaR and NAV on the same paths and feed recourse costs back into NAV.

**B6. [Liquidity risk theory and coherent measures of risk](https://doi.org/10.1080/14697680802373975)** [CR]
- **Record:** Carlo Acerbi & Giacomo Scandolo · 2008 · *Quantitative Finance* 8(7):681–692 · CR 67; S2 119 · DOI 10.1080/14697680802373975. The abstract is from the SSRN version (DOI 10.2139/ssrn.1048322).
- **Finding:** With liquidity risk, portfolio value is no longer linear in holdings. The authors define a non-linear "Value" function that depends on a "liquidity policy" and on market microstructure. Risk measures built on it are convex, and the framework is model-free.
- **Relevance to ADIC:** [Inference] This is the formal object behind ADIC's counterbalancing capacity (CBC).
  - Liquidity-adjusted value = mark-to-market minus the cost of meeting the liquidity policy, i.e. the ladder rows under s* within h.
  - It justifies showing the IC a liquidity-adjusted NAV, and modelling large sales with concave proceeds.

**B7. [Systemwide Stress Test at the IMF](https://doi.org/10.5089/9798229054980.001)** [S2][CR]
- **Record:** Hiroko Oura, Guillaume Arnould, Xiaodan Ding, Pierpaolo Grippa, Marco Gross, Dimitrios Laliotis, Mindaugas Leika, Caterina Lepore, Elisa Letizia, Laura Valderrama & Yuchen Zhang · 2026 · IMF Working Paper 2026/170 · CR 0; S2 1 · DOI 10.5089/9798229054980.001.
- **Finding:** The paper reviews "classic and modern theories and operational methods" for systemic liquidity risk across banks, nonbanks and markets. The channels covered are "runs, redemptions, margin and collateral calls, fire sales, price dynamics, and disruptions in core markets". It details two tools: a flow-of-funds framework and an investment-fund liquidity analysis with fire-sale dynamics.
- **Relevance to ADIC:** It is the most recent survey found.
  - [Inference] Use its fund tool as the template for the Public Markets sleeve.
  - [Inference] Use its list of channels as a checklist for the named-regime generator (§2.5).

**B8. [The Liquidity Coverage Ratio a Decade on: A Stocktake of the Literature](https://doi.org/10.2139/ssrn.5758225)** [S2][CR]
- **Record:** Sebastian Doerr & Mathias Drehmann · 2025 (S2 lists 2026) · SSRN working paper · CR 0; S2 2 · DOI 10.2139/ssrn.5758225.
- **Finding:** The LCR "strongly raises banks' high-quality liquid assets and somewhat reduces their reliance on short-term funding". But "it can crowd out lending and induce greater risk-taking". Its calibration, consequences and interaction with central-bank policy remain open questions.
- **Relevance to ADIC:** This is the survey to cite behind the ADIC-LCR.
  - [Inference] A binding static ratio crowds out return-seeking, which supports the dossier's elastic floors.
  - [Inference] A large buffer may invite risk-taking elsewhere in the book, so judge buffer size by total-portfolio risk.

**B9. [Asset Allocation and Private Market Investing](https://consensus.app/papers/details/61e21abbf1425eac88e593ae69993030/?utm_source=claude_desktop)** [CS-saved: 02][S2][CR]
- **Record:** Junying Shen, Ding Li, Grace (Tiantian) Qiu, Vishv Jeet, Michelle (Yu) Teng & Ki Cheong Wong · 2021 · *Journal of Portfolio Management* 47(4):71–82 · CS 7; CR 8 · DOI 10.3905/jpm.2021.1.211.
- **Finding (S2 abstract):** The framework links bottom-up private cash flows with top-down allocation. It measures the trade-off between allocation, total-portfolio performance and "the frequency of certain liquidity events with different severities". "Commitment pacing … plays a crucial role" in that trade-off.
- **Relevance to ADIC:** It supports the dossier's Monte Carlo design.
  - [Inference] Report P(red) as a frequency × severity table (events per decade by tier).
  - It is an independent prior for pacing as the main *structural* lever; B23 qualifies how fast that lever works.

### 3.3 Collateral and margin liquidity (B10–B13)

**B10. [Pension Liquidity Risk](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop)** [CS-saved: 03, 06][S2]
- **Record:** Kristy A. E. Jansen, Sven Klingler, Angelo Ranaldo & Patty Duijm · 2026 · *Review of Financial Studies* · CS 0; S2 0 · DOI 10.1093/rfs/hhag068.
- **Finding (S2 abstract):** Dutch pension funds with worse funding ratios use swaps more aggressively, and margin calls when rates rise "can exceed 6% of their total assets". Funds meet the calls by selling medium-term government bonds. That procyclical selling depresses those bonds' prices.
- **Relevance to ADIC:** [Inference] Overlay collateral calls can be a material share of total assets, not a P99 footnote. They are met by selling the very HQLA that make up the Treasury band. So stress the ADIC-LCR(30d) numerator for the price impact of ADIC's own sales.

**B11. [The Impact of Derivatives Collateralisation on Liquidity Risk: Evidence from the Investment Fund Sector](https://consensus.app/papers/details/8235e347f86b5b799f4cd8e4e7e31838/?utm_source=claude_desktop)** [CS-saved: 09][S2][CR]
- **Record:** Audrius Jukonis, Elisa Letizia & Linda Rousová · 2022 · SSRN; also IMF WP 2024/026 (DOI 10.5089/9798400267239.001) · CS 2; CR 1 · DOI 10.2139/ssrn.4305519.
- **Finding:** On transaction-level derivatives data, "between 13% and 33% of euro area funds with sizeable derivatives exposures may not have sufficient liquidity buffers" for stressed VM calls. Those funds would redeem MMF shares, "procyclically sell assets and draw on credit lines".
- **Relevance to ADIC:** [Inference] A method template for (L1): revalue every overlay trade under each scenario and compare with unencumbered HQLA by currency and legal entity, instead of using a P99 scalar. It also shows the second-round channel: other funds redeem MMFs and draw lines in the same state.

**B12. [Simulating liquidity stress in the derivatives market](https://consensus.app/papers/details/2ed33ac2bdc9586d98e71535615286bf/?utm_source=claude_desktop)** [CS-saved: 06, 09][S2][CR]
- **Record:** Marco Bardoscia, Gerardo Ferrara, Nicholas Vause & Michael Yoganayagam · 2021 · *Journal of Economic Dynamics and Control* 133:104215 · CS 48; CR 11 · DOI 10.1016/j.jedc.2021.104215.
- **Finding (S2 abstract):** Institutions short of cash wait "as long as possible to receive payments before making their own", so VM shortfalls grow as they spread through the network. The aggregate shortfall was a modest fraction of daily repo borrowing, and coordinating payments centrally would avoid little of it.
- **Relevance to ADIC:** [Inference] The daily overlay sub-steps should book tail-hedge receipts from stressed dealers with a delay and a partial-payment haircut, while ADIC's own VM goes out the same day. This matters because tail-hedge monetization is step 2 of the pecking order.

**B13. [An anatomy of the 2022 gilt market crisis](https://doi.org/10.2139/ssrn.4488189)** [CR]
- **Record:** Gabor Pinter · 2023 · SSRN (Bank of England staff paper; a second SSRN record exists, DOI 10.2139/ssrn.4407740) · CR 7 · DOI 10.2139/ssrn.4488189.
- **Finding:** In the LDI–pension–insurance sector, firms with larger pre-crisis repo and swap exposure sold more gilts, while hedge funds were paid for providing liquidity. Transaction costs soared even for non-LDI investors and small trades, and price dispersion more than doubled in days: "consistent with the contagious nature of illiquidity".
- **Relevance to ADIC:** It is the microstructure evidence behind the TPR buffer rules the dossier cites.
  - [Inference] In S3, raise government-bond execution haircuts for every seller, not only leveraged ones.
  - [Inference] Use the overlay's own repo and swap exposure to predict ADIC's forced sales.

### 3.4 Contingent funding: credit lines, repo and pre-arranged borrowing (B14–B18)

**B14. [Aggregate Risk and the Choice between Cash and Lines of Credit](https://doi.org/10.1111/jofi.12056)** [CR]
- **Record:** Viral V. Acharya, Heitor Almeida & Murillo Campello · 2013 · *Journal of Finance* 68(5):2059–2116 · CR 307 · DOI 10.1111/jofi.12056 (NBER w16122, 2010).
- **Finding:** Banks provide liquidity by pooling idiosyncratic risk, so lines to firms with high aggregate risk are costlier, and those firms hold cash instead. "In times of heightened aggregate volatility … bank credit lines feature fewer initiations, higher spreads, and shorter maturity".
- **Relevance to ADIC:** [Inference] ADIC's needs peak in systematic stress, which makes it a high-aggregate-risk borrower.
  - Expect committed capacity to cost more, and to be hard to add or roll, in exactly the regimes where the TPF tier and policy B count on it.
  - Give new facilities zero credit in Crisis.

**B15. [Bank lines of credit as contingent liquidity: Covenant violations and their implications](https://doi.org/10.1016/j.jfi.2019.03.004)** [S2][CR]
- **Record:** Viral Acharya, Heitor Almeida, Filippo Ippolito & Ander Perez Orive · 2020 · *Journal of Financial Intermediation* 44:100817 · CR 54; S2 47 · DOI 10.1016/j.jfi.2019.03.004.
- **Finding (S2 abstract):** In the 2007–08 collapse of the asset-backed commercial paper (ABCP) market, banks more exposed to ABCP conduits "renegotiated significantly tougher conditions" on lines to borrowers in covenant violation: higher spreads and higher commitment fees. Lender liquidity risk passes through to firms that rely on lines.
- **Relevance to ADIC:** [Inference] Facility terms (§6.2 `Facility`: LTV/MAC, availability by regime) should depend on the lender's stress as well as ADIC's. Falling NAVs erode LTV headroom (§4.2(5)), and a stressed lender will use any breach to reprice. This supports VL R5(c), which notes that forced paydowns are not modelled.

**B16. [Repo Runs: Evidence from the Tri-Party Repo Market](https://consensus.app/papers/details/b4498a6023e95908834404ffd98876ab/?utm_source=claude_desktop)** [CS-saved: 06][CR]
- **Record:** Adam Copeland, Antoine Martin & Michael Walker · 2014 · *Journal of Finance* 69(6):2343–2380 · CS 273 (record year 2012, the WP); CR 245 · DOI 10.1111/jofi.12205.
- **Finding:** There was "no system-wide run on repo". In tri-party repo, "the level of margins and the amount of funding were surprisingly stable for most borrowers", with a sharp funding drop only for Lehman. The WP abstract contrasts this with bilateral repo, where haircuts rose sharply (Gorton–Metrick).
- **Relevance to ADIC:** It qualifies §2.5.
  - [Inference] For B0 overnight Treasury repo, the stress risk is a quantity run on a weak dealer, not a haircut spiral.
  - [Inference] Use dealer-concentration limits and dealer-specific availability, and keep haircut stress for non-Treasury collateral.

**B17. [Integrating Illiquid Assets into the Portfolio Decision Process](https://consensus.app/papers/details/29f5d1f3ce855a36b86e0c22a1ef2f0c/?utm_source=claude_desktop)** [CS-saved: 02, 06][CR]
- **Record:** Paul M. Anglin & Yanmin Gao · 2011 · *Real Estate Economics* 39(2):277–311 · CR 23 · DOI 10.1111/j.1540-6229.2010.00291.x.
- **Finding (CR abstract):** The cost of illiquidity depends on the investor's uncertain need to liquidate and on its other assets. "Borrowing to pay for a liquidity shock cannot overcome all of the costs of owning an illiquid asset. In contrast, borrowing at t = 0 benefits from the complementarity in the assets."
- **Relevance to ADIC:** It supports pre-arranged facilities (policy B) over NAV loans taken after the shock.
  - [Inference] Corporate Finance should also test pre-funded term debt held as cash, counted in tier T, against undrawn lines.

**B18. [What drives corporate liquidity? An international survey of cash holdings and lines of credit](https://doi.org/10.1016/j.jfineco.2010.04.006)** [CR]
- **Record:** Karl V. Lins, Henri Servaes & Peter Tufano · 2010 · *Journal of Financial Economics* 98(1):160–176 · CR 496 · DOI 10.1016/j.jfineco.2010.04.006. The abstract is from the SSRN version (DOI 10.2139/ssrn.971178).
- **Finding:** In a survey of CFOs in 29 countries, lines of credit ("options on liquidity") are tied to funding future investment opportunities. Non-operational cash ("realized liquidity") "is primarily held as a general buffer against future cash shortfalls".
- **Relevance to ADIC:** [Inference] This revealed preference matches B14.
  - Hold cash and Treasuries against obligations: the owner draw, VM and calls.
  - Use committed lines mainly for opportunity capital, such as Secondaries and Capital Solutions dry powder in Green or Amber.
  - It supports keeping TP, not TPF, as the hard survival test, as the dossier does.

### 3.5 Hedge-fund redemption rights (B19–B20)

**B19. [Locked Up by a Lockup: Valuing Liquidity as a Real Option](https://doi.org/10.1111/j.1755-053x.2010.01104.x)** [CR]
- **Record:** Andrew Ang & Nicolas P. B. Bollen · 2010 · *Financial Management* 39(3):1069–1096 · CR 47 · DOI 10.1111/j.1755-053x.2010.01104.x (NBER w15937).
- **Finding:** Withdrawing from a hedge fund is a real option; lockups and notice periods are exercise restrictions, and fund failure probabilities vary over time. A two-year lockup with three months' notice costs about 1% of the initial investment (constant relative risk aversion of 3). But "the cost of illiquidity can easily exceed 10% if the hedge fund manager can arbitrarily suspend withdrawals".
- **Relevance to ADIC:** [Inference] This values the queue model (L7).
  - Early redemption (policy C) is early exercise, worth it when the risk of failure or suspension rises.
  - Gate and suspension risk, not notice lags, should drive the hedge-fund tier haircut. Parameterize it by regime and by fund.

**B20. [Liquidity Restrictions, Runs, and Central Bank Interventions: Evidence from Money Market Funds](https://consensus.app/papers/details/389740373ccf5208b969643b471e31ae/?utm_source=claude_desktop)** [CS-saved: 05, G6][CR]
- **Record:** Lei Li, Yi Li, Marco Macchiavelli & Xing (Alex) Zhou · 2021 · *Review of Financial Studies* 34(11):5402–5437 · CS 79; CR 108 · DOI 10.1093/rfs/hhab065.
- **Finding (CR abstract):** The redemption gates and fees introduced in the 2016 reform "exacerbated the run on prime MMFs" in COVID. They "could generate strategic complementarities among investors in crisis times".
- **Relevance to ADIC:** [Inference] Gate risk is endogenous.
  - As a fund nears its gate, other LPs redeem early and ADIC's pro-rata share shrinks. Make other investors' requests rise with perceived gate risk.
  - Holding only government MMFs in B0 sidesteps the gated prime-fund channel. This is an inference: the abstract covers prime funds.

### 3.6 What liquidity is worth to an investor with payouts and commitments (B21–B23)

**B21. [The Shadow Costs of Illiquidity](https://consensus.app/papers/details/97a784fb4e9e50e19a68e7bd6ce46251/?utm_source=claude_desktop)** [CS-saved: 01][CR]
- **Record:** Kristy A. E. Jansen & Bas J. M. Werker · 2022 · *JFQA* 57(7):2693–2723 · CS 3; CR 5 · DOI 10.1017/s0022109022000473.
- **Finding (CR abstract):** Illiquidity that only distorts asset allocation is cheap. Costs are high "when illiquidity restricts consumption": for short-term investors, for investors facing substantial liquidity shocks, and for those wanting a large illiquid share.
- **Relevance to ADIC:** ADIC has all three features: a mandated 5–10% draw and roughly 60% in private markets.
  - [Inference] Measure the value of safety as a shadow cost on the draw channel. Mean distribution-inclusive wealth, the measure behind §6.6's "price of safety is low", is the wrong yardstick.
  - [Inference] Drive the optimizer's ℓ_h from the draw rows.

**B22. [Alternatives and Liquidity: Will Spending and Capital Calls Eat Your "Modern" Portfolio?](https://consensus.app/papers/details/8935f6aa693b5a87ac77f10001be06a2/?utm_source=claude_desktop)** [CS-saved: 03][CR]
- **Record:** Laurence B. Siegel · 2008 · *Journal of Portfolio Management* 35(1):103–114 · CS 34; CR 24 · DOI 10.3905/jpm.2008.35.1.103. There is no abstract in CR or S2; the finding is as stream 03 recorded it from the Consensus abstract.
- **Finding:** Spending, capital calls and margin can exhaust the liquid sleeve in bear markets. Stream 03 drew the implication to ladder commitments gradually and hold a considerable liquid sleeve.
- **Relevance to ADIC:** This is a seminal endowment-model statement of G7's thesis (§1.1–1.2), written in 2008.
  - [Inference] Use it as the IC's narrative anchor and as a historical analogue for S1.

**B23. [Can investors time their exposure to private equity?](https://consensus.app/papers/details/b5880343ab7b57ebaf68b353dfff48da/?utm_source=claude_desktop)** [CS-saved: 04, 05, 08, G2][S2][CR]
- **Record:** Gregory W. Brown, Robert S. Harris, Wendy Hu, Tim Jenkinson, Steven N. Kaplan & David T. Robinson · 2021 (online 2020) · *JFE* 139(2):561–577 · CS 30; CR 42 · DOI 10.1016/j.jfineco.2020.08.014.
- **Finding (S2 abstract):** Timing commitments yields "modest gains, at best", because investors "cannot time when commitments are called or when investments are exited". Net cash flows are highly correlated over time "even across commitment strategies that allocate capital in a very different manner over time".
- **Relevance to ADIC:** It challenges how fast the pacing lever works (policy C's ×0.25 cut).
  - [Inference] Calls over the next 4–8 quarters come mostly from existing unfunded commitments.
  - Decompose policy C's P(red) gain (11.5% to 4.5%) into its pacing and hedge-fund-redemption parts, and credit pacing only through the age curve.

### 3.7 The owner in stress (B24–B25)

**B24. [SWF 3.0: How sovereign wealth funds navigated COVID-19 and changed forever](https://consensus.app/papers/details/554f5e983997579aa32a8313d73304b8/?utm_source=claude_desktop)** [CS-saved: 03][S2][CR]
- **Record:** Diego López · 2023 · *Journal of International Business Policy* 6(3):372–387 · CS 13; CR 12 · DOI 10.1057/s42214-023-00147-2.
- **Finding:** From March 2020 to December 2021, governments withdrew more than US$211bn from SWFs and "invited" them to rescue sectors and firms, especially state-owned airlines. S2 returned the abstract in German and Spanish (paraphrased here); stream 03's English record confirms the US$211bn figure.
- **Relevance to ADIC:** [Inference]
  - It adds 2020–21 to stream 03's pool of demand-bust episodes.
  - It reveals a new contingent outflow: **owner-directed domestic investments**. These consume liquidity even when the cash draw stays within the band. Add them as an `Obligation` type.

**B25. [How University Endowments Respond to Financial Market Shocks: Evidence and Implications](https://doi.org/10.1257/aer.104.3.931)** [CR]
- **Record:** Jeffrey R. Brown, Stephen G. Dimmock, Jun-Koo Kang & Scott J. Weisbenner · 2014 · *American Economic Review* 104(3):931–962 · CR 108 · DOI 10.1257/aer.104.3.931.
- **Finding:** Endowments "actively reduce payouts relative to their stated payout policies following negative, but not positive, shocks" ("endowment hoarding"). Negative shocks also cut university operations, including personnel.
- **Relevance to ADIC:** This is the closest evidence on a fund cutting its payout in stress, which is what policy D asks of ADIC's owner.
  - [Inference] The cost of the cut lands on the sponsor when it is weakest. A sovereign in a fiscal shock is the owner least likely to accept a lower draw.
  - [Inference] Price policy D's cost to the owner (VL R5(b)) and agree it in advance, or remove it from the base policy set.

---

## 4. Missed-but-important papers: design implications

Every item is **[Inference]** unless it restates a cited finding. Owners follow the user-confirmed organization:
- **Corporate Finance:** the liquidation policy, facilities, collateral, the owner protocol and the CFP.
- **Groups:** asset-level proposals, pacing and hedge-fund redemption requests.

### 4.1 State variables (new or refined)

| State | Definition | Feeds | Source |
|---|---|---|---|
| Forward-shock pressure π_t | P(crisis within 4–8 quarters given the filtered regime posterior); high in drought | Liquidation mix (cushion versus liquid-first); buffer-use rule | B1, B2 |
| Crowding index Crowd_t | Aggregate forced selling of liquid rungs: fund outflows, SWF and pension selling, dealer balance-sheet strain | Execution haircut η and depth for UST, IG, DM equities and commingled funds | B3, B4, B13 |
| Lender stress L_{f,t} per facility | The lender's own funding stress, aggregate volatility, ADIC's covenant headroom | Facility availability, roll probability, spread, repricing after a breach | B14, B15 |
| Dealer state D_{j,t} per repo counterparty | Dealer-specific funding capacity (quantity), not haircut | B0 repo capacity; concentration | B16 |
| Trade-level collateral state | Scenario VM per trade and CSA/CCP; IM; payment-receipt delay | (L1); encumbrance ledger | B10–B12 |
| Gate hazard g_{j,t} per hedge fund | Probability of a gate or suspension, and other investors' redemption pressure | Queue fulfilment; early-filing trigger | B19, B20 |
| Owner-directed investment requests | Contingent rescue or domestic-support outflow in DB and GW states | `Obligation`; the 12- and 24-month ladder rows | B24 |
| Payout-flexibility status | Whether band use is agreed in advance, and its fiscal cost to the owner | Whether policy D is admissible in DB states | B25 |
| Liquidity-event counter | Events per decade by severity tier | IC frequency × severity table | B9 |

### 4.2 Models
1. **A non-myopic liquidation policy in P,** replacing the fixed waterfall in §6.9.
   - Each quarter, choose how much to take from each tier to minimize recourse cost plus the continuation value of the remaining cushion, given π_t.
   - Structure from B2: separate temporary impact (η) from permanent impact (signalling, mark-downs). Sell more of assets with a low permanent-to-temporary ratio, and when π_t is high, unwind more than the immediate need.
   - Benchmarks: liquid-first (the dossier), cash-last (B1) and pro-rata. Run all three as a standing ablation.
   - This keeps the dossier's rule of adding no separate "liquidity value" term (§6.8). The cushion's value emerges from the multi-period recourse problem instead of a per-path static LP (§6.4).
2. **Crowding-dependent price impact on liquid rungs:** η_{k,t} = η_k(S_t)·(1 + c_k·Crowd_t), plus a depth cap (B3, B4, B13).
   - For red-tier LP interests, set depth from specialist buyers' dry powder (F9). The Secondaries group's market intelligence supplies the inputs, under the conflict controls of context §1A.
3. **Scenario-consistent LaR (B5).**
   - NAV and outflows run on the same paths, and recourse costs feed back into NAV, NAV-linked draws and LTV cures.
   - Report both LaR definitions: the dossier's net need before management actions, and B5's resources required under s*.
4. **Liquidity-adjusted NAV (B6):** V^L = MTM − min cost{meet NCO_{s*}(h) within h | φ, depth}.
   - Report it per group (an attribution of LC_g) and in total.
   - Use V^L, not NAV, wherever the optimizer values terminal wealth for liquidity-constrained policies.
5. **A trade-level VM engine (B11, B12, B10).**
   - VM out the same day.
   - VM in from stressed dealers at T+1 to T+k, with a partial-payment haircut.
   - Price impact on ADIC's own HQLA sales when meeting calls.
6. **Hedge-fund redemption as an option (B19)** inside the queue model.
   - Failure and suspension hazards are regime-dependent, and competing redemptions are endogenous (B20).
7. **A facility model (B14, B15, B17).**
   - Availability A_{f,t} = A_f(S_t)·a(L_{f,t}, headroom).
   - Spread s_{f,t} = s_f^0 + β_f·σ_t.
   - New facilities only in Green; repricing on a covenant breach.
   - Pre-funded term debt modelled as cash in tier T.
8. **An extended owner module (B24, B25):** the cash draw, plus directed-investment requests, plus a low probability that the owner accepts a payout cut in DB states.

### 4.3 Parameter priors (literature values, not ADIC data)

| Parameter | Prior | Source | Caveat |
|---|---|---|---|
| Swap margin calls, rate-hedged pension funds | Can exceed 6% of total assets when rates rise | B10 | Dutch pensions; interest-rate swaps |
| Share of derivative-using funds with insufficient VM buffers | 13–33% | B11 | Euro-area funds; scenario-dependent |
| Peak VM multiple, COVID | About 5× | Rousová et al. 2020 (F24) | Title not recorded by stream 09; use as a cross-check only |
| Aggregate network VM shortfall | A modest fraction of daily repo borrowing; little gain from coordination | B12 | UK trade-repository data |
| Cost of a 2-year lockup with 3-month notice | About 1% of initial investment; can exceed 10% if the manager can suspend | B19 | Constant relative risk aversion of 3; model-based |
| Commitment-risk premium | About 1.63% a year with many funds (2014 version); larger value from adjusting the *quantity* committed | F1 | Model-based; revised paper |
| PE liquidity-risk premium | About 3% a year, through a funding-liquidity channel | F2 | Fund-level data |
| Credit lines in aggregate volatility | Fewer initiations, higher spreads, shorter maturity | B14 | Qualitative direction only |
| Line terms when the lender is stressed | Higher spreads and commitment fees for covenant violators | B15 | 2007–08 ABCP episode |
| SWF withdrawals in a global demand bust | More than US$211bn (Mar 2020 – Dec 2021), plus directed rescues | B24 | Global aggregate |
| Pacing effect on net cash flow | Highly correlated across very different commitment strategies | B23 | Qualitative direction only |
| Recommitment baseline | Commitments = distributions + uncalled, scaled by target/actual. Reached 86% of target with an 8% chance of overinvestment; ~30% overcommitment in build-up; ~10% never called | F7 (as recorded by stream 01) | 1980–2005 data |

### 4.4 Constraints
1. **A state-dependent liquid cushion (B1, B2).** Liquid share ≥ L_min(π_t), with L_min rising in drought. Add it as a soft row at 12 months and a hard row at 24 months, alongside or replacing the static stage thresholds of 20/24/28%.
2. **A buffer-use rule (B1, B2, with Basel LCR20.5).**
   - Keep the usable 8% → 4% band.
   - In an acute shock expected to be short, use the buffer.
   - In a slow-burn drought, require pre-emptive actions (planned secondary tranches, term funding) before Treasury ÷ NAV falls below 6%.
3. **Facility credit (B14–B16).**
   - Draws ≤ A_f(S_t)·a(L_{f,t}).
   - Zero credit for facilities not arranged before the stress.
   - Repo counterparty concentration limits, with dealer-specific availability.
4. **(L1) at trade level (B10, B11, B12).** Compute it by currency and legal entity. Book incoming VM from stressed dealers with a lag, and outgoing VM the same day.
5. **A hedge-fund early-filing trigger (B19, B20).** File when g_{j,t} exceeds a threshold, and size queue fulfilment net of competing redemptions.
6. **Pacing credit (B23).** Pacing cuts reduce calls only through the age curve (stream 04), with no credit in the first two quarters.
7. **Policy D admissibility (B24, B25).** Use owner band-use only where the owner has agreed in advance. Otherwise model the draw at the fiscal-state level.

### 4.5 Objectives and shadow prices
1. **The value of safety (B21):** measure it as the shadow cost on the draw rows (ℓ_h from the draw constraints), not as mean wealth. ℓ_h should spike in DB states, and Corporate Finance's transfer-pricing curve inherits that spike.
2. **The liquidation trade-off (B1):** for each liquidation policy, show expected recourse cost *and* P(red) and expected severity. B1 says the two move in opposite directions.
3. **Two-sided transfer pricing (F5):** charge liquidity users and credit liquidity providers, including the option value of dry powder. The dossier already credits liquidity provided (§6.8); F5 gives the formal basis.
4. **An owner-cost term for policy D (B25),** so the optimizer cannot buy P(red) improvements for free with the owner's budget.

### 4.6 Agent and IC design
1. **The Corporate Finance (Treasurer) seat** owns:
   - the liquidation-policy choice (B1–B4);
   - the facility reliability panel: lender stress and covenant headroom (B14–B17);
   - the trade-level collateral engine (B10–B12);
   - the owner protocol (B24–B25).
2. **A liquidation-order challenger agent.** For every Amber or Red playbook it runs the cash-last and pro-rata alternatives and reports the tail trade-off (B1, B2).
3. **CFP governance (F15, a 2026 single-author preprint; use as a checklist, not as evidence).** Five elements:
   - pre-delegated authority with quantitative thresholds per stage;
   - a standing crisis subcommittee with delegated board authority;
   - real-time management information for non-executives;
   - a documented emergency-session protocol;
   - an annual CFP simulation with board participation.

   Map them to Corporate Finance (Green and operational Amber), the CIO (strategic Amber), the IC (Red) and the Board and owner (Black), as in dossier §6.10.
4. **IC pack additions:**
   - a frequency × severity table of liquidity events (B9);
   - liquidity-adjusted NAV (B6);
   - the facility reliability panel (B14, B15);
   - a crowding indicator for liquid rungs (B3, B4);
   - owner-protocol status, including directed-investment requests (B24, B25).
5. **LLM role.** Agents parse CSAs, LPAs and facility agreements for covenant, MAC and gate clauses (B15, B19, B20). Deterministic code owns every number.

### 4.7 Further records (compact)

| # | Record | Metadata | What it adds |
|---|---|---|---|
| F1 | [Capital Commitment](https://doi.org/10.2139/ssrn.2490430) [CR]; earlier version [Capital Commitment and Illiquidity Risks in Private Equity](https://consensus.app/papers/details/9b5881d8cef05dffa4a40423d6b15bc8/?utm_source=claude_desktop) [CS-saved: 01, 06]; 2024 record [link](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) [CS-saved: 06] | Elise Gourier, Ludovic Phalippou & Mark M. Westerfield · SSRN 2014 (revised 2024) · CR 3 | Investors would pay more to adjust the quantity committed than to remove timing uncertainty or limited tradability. Commitment-risk premia rise with secondary-market liquidity and persist across many funds. The 2014 version's figure is 1.63% a year. |
| F2 | [Private Equity Performance and Liquidity Risk](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop) [CS-saved: 02][CR] | Francesco Franzoni, Eric Nowak & Ludovic Phalippou · 2012 · *JF* 67(6):2341–2373 · CR 225 · DOI 10.1111/j.1540-6261.2012.01788.x | PE loads on the same liquidity risk factor as public equity (premium about 3% a year), through a funding-liquidity channel. PE marks and funding stress co-move: wrong-way risk for SELL and REFINANCE. |
| F3 | [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop) [CS-saved: 02, 05, G2][S2] | Vincent Maurin, D. Robinson & Per Strömberg · 2023 (online 2022) · *Management Science* 69:5740–5771 · DOI 10.1287/mnsc.2022.4612 | GPs "may inefficiently accelerate drawdowns to avoid default by LPs". This supports the dossier's stress add-on to calls (×1.25). |
| F4 | [Pension fund's illiquid assets allocation under liquidity and capital requirements](https://doi.org/10.1017/s1474747219000398) [S2][CR] | Dirk W. G. A. Broeders, Kristy A. E. Jansen & Bas J. M. Werker · 2020 · *JPEF* 20(1):102–124 · CR 20 | Short-term payments and derivative margining create liquidity requirements that shape the illiquid allocation. Supports optimizing the overlay size and the illiquid share jointly. |
| F5 | [Liquidity and Portfolio Choice: A Unified Approach](https://consensus.app/papers/details/87606279740d57b4b0350e859446911b/?utm_source=claude_desktop) [CS-saved: 02, 08][CR] | Will Kinlaw, Mark Kritzman & David Turkington · 2013 · *JPM* 39(2):19–27 · CS 29 · DOI 10.3905/jpm.2013.39.2.019 | Liquidity as a "shadow asset" (opportunity) and a "shadow liability" (defence). The basis for two-sided transfer pricing. |
| F6 | [A Note on Liquidity Risk Management](https://consensus.app/papers/details/e5d07eaeb7cb57e9977a1900ca0d5a7a/?utm_source=claude_desktop) [CS-saved: 06][CR] | Markus K. Brunnermeier & Motohiro Yogo · 2009 · *AER* 99(2):578–583 · CS 89 · DOI 10.1257/aer.99.2.578 | Minimizing rollover risk means maximizing the *effective* maturity of liabilities. Corporate Finance should term out facilities while healthy. |
| F7 | [Private Equity Recommitment Strategies for Institutional Investors](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop) [CS-saved: 01][CR] | Gerben de Zwart, Brian Frieser & Dick van Dijk · 2012 · *FAJ* 68(3):81–99 · CS 13 · DOI 10.2469/faj.v68.n3.1 | An explainable recommitment rule to use as the baseline pacing policy in P (priors in §4.3). |
| F8 | [Managing Illiquidity in Open-Ended Funds with Private Asset Allocations](https://consensus.app/papers/details/12cd077c32a755c9bbab6ea80a91706c/?utm_source=claude_desktop) [CS-saved: 02][S2] | Raul Leote de Carvalho, Xiao Lu, Thomas Heckel & Gilles David · 2026 · *J. Private Markets Investing* 24(4):57–86 · DOI 10.3905/jpmi.2026.002 | Stress tests show "suspending future commitments can rebalance the portfolio without forced secondary sales". It supports pacing as a structural lever, over a longer horizon than B23 implies for the short run. |
| F9 | [Fire Sales in Finance and Macroeconomics](https://consensus.app/papers/details/38094184238d5f8f9fe8944a05e37411/?utm_source=claude_desktop) [CS-saved: 05][CR] | Andrei Shleifer & Robert Vishny · 2011 · *JEP* 25(1):29–48 · CS 700; CR 666 · DOI 10.1257/jep.25.1.29 | Fire sales happen when the highest-valuation bidders are themselves constrained. Model red-tier depth from specialist buyers' capital. |
| F10 | [The Bright Side of Fire Sales](https://doi.org/10.2139/ssrn.2473123) [CR] | Jean-Marie Meier & Henri Servaes · 2014 · SSRN · CR 7 | Buyers in fire sales earn excess returns about 2pp higher, through reduced seller bargaining power. Supports counter-cyclical dry powder for Secondaries and Capital Solutions. |
| F11 | [Corporate Risk Management: Integrating Liquidity, Hedging, and Operating Policies](https://consensus.app/papers/details/c6027dda48605911a46b3578a9a0a3ea/?utm_source=claude_desktop) [CS-saved: 01, 09][CR] | Andrea Gamba & Alexander J. Triantis · 2014 · *MS* 60(1):246–264 · CR 84 · DOI 10.1287/mnsc.2013.1752 | Liquidity plays "a critical and distinct role … justifying high levels of cash"; the marginal value of derivatives hedging "is likely to be low" (C7). |
| F12 | [Hedge-Fund Performance and Liquidity Risk](https://doi.org/10.2139/ssrn.1917118) [CR] | Ronnie Sadka · 2011 · SSRN · CR 8. A related paper is *JFE* 98(1):54–71 (2010), DOI 10.1016/J.JFINECO.2010.05.001, whose abstract I did not retrieve | Funds loading on liquidity risk outperform by about 6.5% a year but perform negatively in liquidity crises, independent of share restrictions. Hedge-fund value falls just when ADIC would redeem. |
| F13 | [Liquidity Stress Tests for Investment Funds: A Practical Guide](https://doi.org/10.5089/9781484324783.001) [CR] | Antoine Bouveret · 2017 · IMF WP 17/226 · CR 6 | Calibrating redemption shocks, measuring buffers and assessing fund resilience. A template for stress-testing ADIC's commingled managers. |
| F14 | [Too Many Cooks, Not Enough Risk Management: Gilt Market Dysfunction and Liability-Driven Investment (LDI)](https://doi.org/10.2139/ssrn.4445632) [CR] | Laura Kodres · 2023 · SSRN · CR 1 | Nonbank institutions "took on leverage without properly assessing and preparing for its liquidity implications". A review of remedies and misdiagnoses. |
| F15 | [Board Governance and the Contingency Funding Plan](https://doi.org/10.2139/ssrn.6494519) [CR] | Sunando Roy · 2026 · SSRN · CR 0 | Three recurring CFP governance failures: sanitized board briefings, undefined authority thresholds and untested convening mechanisms. Five fixes (§4.6 #3). A single-author preprint. |
| F16 | [When Margin Call Burns Out Liquidity Buffer: Hedge Fund Ratings and Securities Financing Haircuts](https://doi.org/10.2139/ssrn.4825764) [CR][S2] | Wujiang Lou · 2024 · SSRN · CR 0 | Treats a fund's liquidity buffer as a margin account that defaults when calls deplete it. An analogue of the survival horizon. |
| F17 | [Hedging as a Liquidity Risk Management Strategy for Optimal Liquidation](https://doi.org/10.2139/ssrn.6377318) [CR] | Taher Khan · 2026 · SSRN · CR 0 | A proportional unwind is bottlenecked by the least liquid asset. Hedging while selling slowly ("hedged hibernation") cut risk by 80% in a hypothetical fund. Supports physical-to-synthetic and overlay hedging before illiquid sales. Low weight. |
| F18 | [Do Institutional Investors Stabilize Equity Markets in Crisis Periods? Evidence from COVID-19](https://www.semanticscholar.org/paper/b0856793bd4a7aeea58e2ff81d02380b229f821f) [S2] | Simon Glossner, Pedro Matos, Stefano Ramelli & A. Wagner · 2025 · *MS* 71:8623–8641 · S2 38 · DOI 10.1287/mnsc.2022.03411 | Institutions downscaled equity in the 2020 crash, and those price effects reversed in the recovery. A crowding analogue for B1-rung DM equities. |
| F19 | [Liquidity Requirements, Liquidity Choice, and Financial Stability](https://doi.org/10.1016/bs.hesmac.2016.03.011) [CR][S2] | Douglas W. Diamond & Anil K. Kashyap · 2016 · *Handbook of Macroeconomics* 2:2263–2303 · CR 74 | Abstract not retrieved, so the finding is not reported. The core theory reference for liquidity requirements; re-check in Consensus. |
| F20 | [Redemption risk and cash hoarding by asset managers](https://doi.org/10.1016/j.jmoneco.2017.03.008) [CR][S2] | Stephen Morris, Ilhyock Shim & Hyun Song Shin · 2017 · *JME* 89:71–87 · CR 118 | Abstract not retrieved, so the finding is not reported. Relevant to how ADIC's external managers behave in stress; re-check. |
| F21 | [Share Restrictions and Investor Flows in the Hedge Fund Industry](https://www.semanticscholar.org/paper/cf92372e9d4e07c3d5f6f3ed4add42240f3f38fc) [S2] | Mila Getmansky, Bing Liang, Christopher Schwarz & R. Wermers · 2015 · SSRN · S2 15 · DOI 10.2139/SSRN.2692598 | Abstract not retrieved, so the finding is not reported. A candidate calibration source for the hedge-fund queue. |
| F22 | [Central Clearing and Collateral Demand](https://consensus.app/papers/details/c3c3447985445b129533b8517cc5f424/?utm_source=claude_desktop) [CS-saved: 09] | J. D. Duffie et al. (co-authors not recorded by stream 09) · 2015 · SSRN · CS 229 · DOI 10.2139/ssrn.2388894 | IM requirements significantly raise collateral demand, and VM movement causes a "velocity drag". Venue choice changes the overlay's collateral need. |
| F23 | [Integrating private assets in a total portfolio approach](https://consensus.app/papers/details/129e1fa8557c5944852b405eac05dc19/?utm_source=claude_desktop) [CS-saved: 02] | Thomas Meyer · 2025 · *J. Securities Operations & Custody* · DOI 10.69554/tfxb7809 | Owners "may be overestimating their liquidity needs" (C8, weak). |
| F24 | [Rousová et al. 2020](https://consensus.app/papers/details/1568e37e2c845eef816b5c7ccc9f8648/?utm_source=claude_desktop) [CS-saved: 01, 09] | Title, venue and DOI were not recorded by the sibling streams | Euro-area funds met "the fivefold increase in variation margin" in COVID, some only through repo, asset sales and line draws. Resolve the metadata before citing. |

**Practitioner books on CFPs (no abstracts; for the CFP drafters):**
- Lai & Tuosto (2016), "Contingency Funding Planning", in *Liquidity Risk Management* (Wiley), DOI 10.1002/9781118898130.ch7.
- "Step V: Stress Testing and the Contingency Funding Plan", in *The Liquidity Risk Management Guide* (Wiley, 2014), DOI 10.1002/9781118858035.ch10.
- Papaioannou et al. (2018), a chapter on SWF funding-withdrawal rules ([CS-saved: 02](https://consensus.app/papers/details/2b4c462b545a58e3ae8f9d60e1196d5c/?utm_source=claude_desktop)). It argues for operating frameworks that "avoid a fiscal gap-filling function".

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier position (§) | Challenging evidence | Strength | Suggested change |
|---|---|---|---|---|
| C1 | **A liquid-first two-dimensional pecking order** (§2.4, §6.9 steps 1–11). Deviations are allowed only for a Green-market tail-end sale or a Gulf-war reordering. | B1: a cash-last cushion lowers tail losses and insolvency risk at higher expected cost. B2: non-myopic liquidation sells more than needed and preserves liquid assets when future shocks loom. B3: liquid assets fall most when crowded. B4: funds shed liquid assets first and amplify stress. | **Strong in direction.** Two classic theory papers, a 2026 *MS* paper and IMF evidence. B1 is a stylized model, and B3's evidence comes from insurers' bonds. | Make the waterfall state-dependent (§4.2 #1, §4.4 #1–2). In drought or Amber, raise liquidity early through planned illiquid tranches and term funding while Treasury is still above 6%. Add crowding to liquid-rung haircuts. Run liquid-first, cash-last and pro-rata as a standing ablation in the IC pack. |
| C2 | **Facilities as a dependable recourse tier** (TPF; policy B cuts P(red) from 18.1% to 11.5%; revolver 75% available in stress; NAV-facility LTV 10% → 5%) | B14: lines are costlier and scarcer for high-aggregate-risk borrowers and in high volatility. B15: stressed lenders reprice lines when covenants break. B18: firms rely on cash, not lines, for shortfalls. Li–Strahan–Zhang's own abstract ties 2020 line performance to Fed programs, deposit inflows and strong bank capital. | **Moderate to strong.** The evidence is on corporate borrowers; ADIC is a sovereign-owned borrower with different standing [Inference]. | Make availability depend on lender stress and covenant headroom (§4.2 #7). Re-run policy B with availability ≤ 50% in the joint state. Count pre-funded term cash in T (B17). Keep TP as the hard test, as the dossier does. |
| C3 | **Stage-based pacing cuts as a fast lever** (policy C: a ×0.25 cut, plus early hedge-fund redemptions, takes P(red) to 4.5%) | B23: net cash flows stay highly correlated across very different commitment strategies, because calls and exits cannot be timed. F1: what is valuable is flexibility in the *quantity* committed, ex ante. Supportive over longer horizons: B9 and F8. | **Moderate.** B23 studies return timing, but its cash-flow correlation finding bears directly on liquidity. | Decompose policy C into its two parts. Credit pacing only through the age curve, with none in the first two quarters. Show the IC the quarter-by-quarter cash effect. |
| C4 | **Owner-agreed draw flexibility** (policy D: draw at 5% in crisis or Red; P(red) from 4.5% to 1.5%) | B25: payout cuts move the stress onto the sponsor's operations. B24: governments raised withdrawals and directed rescue investments in 2020–21. | **Moderate.** The evidence is from endowments and SWFs; ADIC's owner may differ [Inference]. | Treat it as an owner decision with an explicit fiscal cost (§4.5 #4). Make policy C the base case and D conditional on advance agreement. Add directed-investment outflows to DB states. |
| C5 | **Repo haircut stress based on the 2007–08 "run on repo"** (§2.5) | B16: tri-party margins stayed stable for most borrowers, and the run was a quantity run on Lehman. | **Moderate** (evidence from one market segment). | Keep Treasury repo in B0, with dealer-quantity risk and concentration limits. Confine haircut stress to bilateral and non-Treasury collateral. |
| C6 | **"The price of safety is low"** (§6.6: mean distribution-inclusive wealth differs by less than 0.2%) | B21: the shadow costs of illiquidity are high when illiquidity restricts consumption, here the draw. F1: a commitment-risk premium of about 1.63% a year. | **Moderate** (theory). | Measure the value of safety as a shadow cost on the draw channel. Mean wealth is the wrong metric in both directions; VL R5 already shows the omitted costs. |
| C7 | **Tail-hedge monetization as step 2** (§6.9) | F11: cash has a critical role, and the marginal value of derivatives hedging is likely low. B12: receipts from stressed dealers may be delayed. | **Weak to moderate** (a corporate model and a network simulation). | Book tail-hedge inflows with receipt delays and partial-payment haircuts. Require the hedge to beat an equal-cost cash buffer; stream 09 already plans that ablation. |
| C8 | **Conservative liquidity budgets in general** (the opposite direction) | F23: owners "may be overestimating their liquidity needs". | **Weak** (a practitioner journal). | No change. Note it as a counterpoint when the IC compares ADIC with Partners Capital's 7-year rule. |

**What the literature supports.** Several dossier positions find support:
- **Usable buffers:** the Basel text quoted in the dossier; B8 lists calibration as an open question.
- **Reporting distributions, not a P99 scalar:** B5, B9.
- **Hedge funds being less liquid than their labels:** B19, B20, F12.
- **The joint dangerous state:** B10–B13, B24, F2.
- **Pre-arranged rather than ad hoc borrowing:** B17.
- **Counter-cyclical dry powder released only in Green or Amber:** F9, F10, and Nadauld et al., which the dossier cites.
- **Testing contingent sources:** B15, B16.

---

## 6. Verbatim usage message

Consensus returned this message on all four attempts. It is a monthly-quota rejection, not a rate limit:

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Search log, sources and rerun plan

**Consensus.**
- 4 attempts: 3 on query 1 ("Robinson Sensoy cyclicality performance measurement cash flow liquidity private equity"), 30 seconds apart, then 1 on query 2 ("Banks as Lenders of First Resort: Evidence from the COVID-19 Crisis").
- All were rejected by the monthly quota, so **0 searches completed**.
- No filters were used and no thread tools were called.

**OpenAlex.** One probe returned HTTP 429 (`Retry-After: 46608`, `X-RateLimit-Remaining: 0`).

**Topical searches (14).** All used a plain query with no filters, run one at a time. S2 = Semantic Scholar relevance search with up to 6 back-off attempts; CR = Crossref bibliographic search.

| # | Query | Engine | Outcome |
|---|---|---|---|
| 1 | "liquidity risk management institutional investors" (seed) | S2 (3 attempts) | Mostly noise. Glossner et al. (F18). |
| 2 | "pension fund liquidity stress margin calls" (seed) | S2 (3) | B10, B11, B12, F4, B7 |
| 3 | "liquidity coverage ratio" (seed) | S2 (4) | B8. The rest are country bank-ratio studies. |
| 4 | "contingency funding plan liquidity" (seed) | S2 failed (429 ×6), then CR | F15; practitioner book chapters |
| 5 | "liquidity at risk measurement" (seed) | S2 (1) | Noise. B5 came from a saved record instead. |
| 6 | "portfolio liquidation strategy sell liquid assets first or keep liquid cushion distress" | S2 (4) | B1 |
| 7 | "optimal portfolio liquidation distress risk uncertain liquidity needs price impact" | S2 failed, then CR | B2; F17 |
| 8 | "lines of credit liquidity insurance aggregate risk covenant violations cash holdings" | S2 failed, then CR | B18, B15, B14 (NBER version; *JF* version via a title check) |
| 9 | "hedge fund lockup notice period redemption gates investor liquidity" | S2 (6) | F21; Sadka; Ang–Bollen (garbled NBER record, resolved via a CR title check: B19) |
| 10 | "liability driven investment gilt market crisis 2022 pension funds collateral calls" | S2 failed, then CR | F14. Pinter (B13) via a title check. |
| 11 | "usability of bank liquidity buffers stress reluctance to fall below regulatory minimum" | CR | Noise |
| 12 | S2: "university endowments financial crisis payout cuts liquidity private equity capital calls" | S2 failed, then CR, rephrased as "university endowments respond to financial market shocks payout liquidity" | B25 |
| 13 | "liquidity risk theory coherent measures of risk liquidation value portfolio liquidity policy" | CR | B6 |
| 14 | "asset managers cash hoarding liquidity management redemptions liquid assets sold first stress" | S2 (1) | B4 |

**Crossref title searches (16).**
- *Citations (5):* Bolton–Chen–Wang; Schmieder et al.; Schrimpf–Shin–Sushko; Fleming–Ruela (not found); FSI 2011 (not found).
- *Supplementary (11):* hedge-fund liquidity and Form PF; Ang–Bollen; Pinter; Acharya–Almeida–Campello (*JF*); Rousová (resolved only to Jukonis et al.); Copeland–Martin–Walker; Chaderina et al.; Bouveret; Diamond–Kashyap; Morris–Shim–Shin; Bardoscia et al. (*JEDC*).

**Look-ups.**
- **Crossref DOI look-ups:** 42, for metadata and abstracts.
- **Semantic Scholar batch look-ups:** 2, covering 27 identifiers, for abstracts.

**WebSearch (1) and WebFetch (1).** Used for the Duffie & Ziegler (2003) abstract. Sources:
- [IDEAS/RePEc record](https://ideas.repec.org/a/taf/ufajxx/v59y2003i3p42-51.html), fetched;
- [CFA Institute RPC page](https://rpc.cfainstitute.org/research/financial-analysts-journal/2003/liquidation-risk), listed in the search results.

**Saved Consensus records reused (34).** I built an index of the 1,166 unique Consensus URLs in sibling files and reused these:
- *Citation table (7):* Robinson–Sensoy, Gorton–Metrick, Brunnermeier–Pedersen, Bolton–Chen–Wang, Ang–Papanikolaou–Westerfield, Nadauld et al., Glasserman–Kang–Kang.
- *Bibliography (13):* B3, B5, B9, B10, B11, B12, B16, B17, B20, B21, B22, B23, B24.
- *Further records (14):* F1 (two records), F2, F3, F5, F6, F7, F8, F9, F11, F22, F23, F24, plus Papaioannou et al.

The URLs are copied exactly as the sibling files recorded them.

**Raw logs** (session scratchpad):
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g7lit_log_citations.txt`
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g7lit_log_backfill.txt`
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g7lit_cs_index.txt` (the saved-record index)
- Scripts are in `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g7lit_scripts\`.

**Rerun plan after 1 November 2026 (Consensus, no filters)**
1. **Re-run the citation table** so that the 8 rows without a Consensus URL get one: Li–Strahan–Zhang, Acharya–Steffen, Schmieder et al., Miller–Orr, Gerber–Shiu, Little, Clopper–Pearson and Schrimpf–Shin–Sushko.
2. **Re-run the five seeds.** S2's ranking returned noise for seeds 1, 3 and 5.
3. **Targeted gaps:**
   - "liquidity buffer usability banks COVID stigma";
   - "contingency funding plan effectiveness";
   - "LP capital call default financial crisis";
   - "sovereign wealth fund withdrawals oil price decline";
   - "hedge fund gates 2008 redemptions";
   - "private equity secondary market depth crisis";
   - "liquidity transfer pricing asset managers".
4. **Missing abstracts:** Diamond–Kashyap (F19), Morris–Shim–Shin (F20), Getmansky et al. (F21), Sadka *JFE* 2010, Robinson–Sensoy, Gorton–Metrick, Glasserman–Kang–Kang, Siegel (B22) and Kinlaw et al. (F5).
5. **Resolve the metadata for Rousová et al. 2020 (F24).**
