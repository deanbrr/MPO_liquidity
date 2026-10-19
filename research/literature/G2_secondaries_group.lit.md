# G2 literature check: Secondaries group (secondary-fund commitments and direct secondary deals)

**Dossier checked:** `research/groups/dossiers/G2_secondaries_group.md` (as of 2026-10-18; 38 references, 16 of them academic).
**Companion:** `research/groups/verification/G2_secondaries_group.verify.md`.
**Date:** 2026-10-18.

**Organizational mapping (user-confirmed, 2026-10-18).**
- The Secondaries group is a **hybrid book**: LP commitments to third-party secondary funds, plus direct secondary deals (LP-portfolio purchases and GP-led continuation-vehicle stakes).
- **Corporate Finance owns Treasury**: the liquidity buffer, the contingency funding plan, internal transfer pricing (FTP), portfolio-level facilities, overlay collateral and owner distributions. Any reserve the Secondaries group holds for stress buying is a claim on Corporate Finance's liquidity.

**IMPORTANT: Consensus was unavailable in this session.**
- My first Consensus call returned a monthly-quota error. I waited 30 seconds and retried, twice, as the protocol requires. Both retries failed with the same message, which is reproduced verbatim in Section 6.
- I made no further Consensus calls. The error is account-level, and the quota resets on 1 November 2026.
- **What replaced it:**
  1. **Consensus records retrieved earlier today by other agents in this project.** I copied their URLs character for character from those agents' files. No URL was modified or regenerated.
  2. **13 WebSearches and 3 WebFetches in this session.** I used them only where no Consensus record existed or a record lacked an abstract.
- Every row and entry below carries a provenance tag:

| Tag | Source |
|---|---|
| **[P05]** | Consensus record in `research/literature/05_secondaries_navfin.lit.md` |
| **[P04]** | Consensus record in `research/literature/04_pe_cashflows.lit.md` |
| **[P06]** | Consensus record in `research/literature/06_leverage.lit.md` |
| **[P01]** | Consensus record in `research/literature/01_mpo.lit.md` |
| **[P08]** / **[P09]** | Consensus record in `08_action_valuation.lit.md` / `09_overlay.lit.md` |
| **[P11]** | Consensus record in `11_objectives.lit.md` |
| **[VL]** | Consensus URL recorded in the G2 verification log (§7) |
| **[WS]** | WebSearch run in this session. The URL is the web result, **not** a Consensus URL |
| **[CR]** | Crossref API, fetched in this session |

**Reading conventions**
- Findings are abstract-level only. They come from the Consensus abstracts summarised in the source files, or from abstracts shown in WebSearch results. I read no full texts.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Author lists are shown as Consensus displays them, with "et al." where it truncates.
- Citation counts are those shown on the Consensus records when they were retrieved earlier today. "n/a" means there is no Consensus record.

---

## 1. Summary

### Citation integrity
- **Scope.** I checked 17 academic citations: the 16 academic references in dossier §10 (refs 11–26), plus one academic citation that appears only in the text ("Rode et al.", §2.6). Two practitioner references are shown for context and are not counted.
- **Result:** **16 found, 0 mismatched on metadata, 1 not found.** No hallucinated references.
  - 13 are backed by a Consensus record of the cited work itself.
  - 1 (ref 12, Boyer et al. 2018) is confirmed by WebSearch, plus a Consensus record of its published successor.
  - 2 are confirmed by WebSearch only: Allen & Gale 1994, and Gottschalg 2025 (HEC RP 1584).
  - The one not found is Rode et al.
- **Fixes needed (none changes a headline number):**
  1. **Boyer et al. (ref 12) is superseded.** The 2018 NBER WP 25207 was published as "Discount-Rate Risk in Private Equity: Evidence from Secondary Market Transactions", *Journal of Finance* 78(2):835–885 (2023); an intermediate version is NBER WP 28691 (2021).
     - The dossier's β > 2 versus < 0.5 contrast comes from the 2018 WP.
     - The published paper reframes the result as **time-varying discount rates**. Re-check the numbers before they reach the IC. This agrees with the verification log (ref 12 note and R5).
  2. **Albuquerque et al. (ref 13).**
     - Replace the dead Tuck-forum link with SSRN DOI 10.2139/ssrn.3182481. It is still a working paper: one WebSearch found no journal version.
     - What a source supports: a seminar listing found by WebSearch supports the "2009–2016" bid data.
     - What no source supports: the young-fund, VIX, funding-cost and non-specialist-buyer specifics are not in the abstract. Keep them tagged [C] or drop them. This agrees with verification item A7.
  3. **Bollen & Sensoy (ref 15).**
     - It is an **orphan**: listed but never cited in the G2 text.
     - The full title is "How much for a haircut? Illiquidity, secondary markets, and the value of private equity".
     - Its published abstract matters for G2's liquidity-premium logic (Section 5, row 7).
  4. **Gourier, Phalippou & Westerfield (ref 25)** is also an orphan in the G2 text. Its result bears directly on the secondary-fund commitments and on unfunded-heavy purchases (A13).
  5. **Luxenberg et al. (ref 26).** Cite the peer-reviewed ICAIF '22 proceedings version (DOI 10.1145/3533271.3561769), not only the arXiv preprint.
  6. **Nadauld et al. (ref 11).** The quoted figures are from the 2016 working paper (seller PME 0.974). The JFE abstract reports 0.976.
  7. **Gottschalg (refs 21–22).**
     - Add SSRN DOI 10.2139/ssrn.4752652 to ref 21.
     - RP 1584 is confirmed: 386 CVs, 297 with performance data.
     - Both are non-peer-reviewed research papers based on interim, mostly unrealised marks.
  8. **"Rode et al." (§2.6)** has no reference entry, and one WebSearch did not identify it. Take the full citation from the CFA Institute report, or drop the 60bp / 75bp figure.
  9. **Maurin, Robinson & Strömberg (ref 14)** is a theory paper. Tag its claims as model predictions.

### Backfill
- **Where the dossier stands.** Its practitioner sourcing is excellent. It cites few academic papers on the *buyer's* problem.
- **Missed academic work falls into eight clusters:**
  1. **Discount-rate risk in secondary prices.** Boyer et al. (*JF* 2023); market-price evidence from Jegadeesh et al. and Ennis et al.
  2. **How LP-interest auctions work.** Bidder counts and buyer mix (Kleymenova et al.); tax class (Mason & Utke); the 2009 volume collapse and quick recovery (Hege & Nuti).
  3. **What a purchased NAV is worth.** NAV bias by strategy (Jenkinson et al., *TAR*); NAV inflation while the GP is fundraising (Brown et al. 2019; Barber & Yasuda); falling returns and rising dispersion after year 7–8 (Brown et al. 2020).
  4. **Commitment risk and the price of unfunded commitments.** Gourier et al. (cited but orphaned); Giommetti et al.; Meyer.
  5. **Deployment pressure.** Secondary buyouts made under pressure to spend underperform (Degeorge et al.).
  6. **Dry powder and fire sales.** Natural buyers constrained together (Shleifer & Vishny 1992); returns on cash when fire sales are expected (Diamond & Rajan); countercyclical liquidity holdings (Acharya, Shin & Yorulmazer); slow-moving capital (Duffie 2010); adverse selection (Guerrieri & Shimer).
  7. **Fragility of evergreen vehicles.** This matters both for ADIC's optional evergreen units and for buyer depth (Couts; Li et al.).
  8. **Deal-level exit models** for the CV template (Tausch et al.).
- **Gaps that remain open.**
  - Neither Consensus (stream 05, earlier today) nor WebSearch (this session) found a peer-reviewed study of **secondary-fund net performance**.
  - **Continuation-vehicle** evidence is limited to the HEC working-paper series and one 2026 journal article (Jo & Ryu). Crossref confirms its metadata, but no abstract was accessible.
  - Keep the secondary-fund and CV parameters tagged [C] / [I], with wide ranges.

### Challenges (detail in Section 5)
1. **Part of "discount capture", and of the W-flag α, is compensation for discount-rate risk, not alpha** (Boyer et al.; Jegadeesh et al.; Ennis et al.).
2. **Tail-end θ is set too high.** Brown et al. 2020 find returns fall off after year 7–8 and dispersion rises. This supports verification issue R2.
3. **Reserves.**
   - Privately chosen liquidity holdings are "inefficiently low during economic booms but excessively high during crises" (Acharya et al.). Build reserve capacity ex ante.
   - How long discounts take to recover depends on how fast capital arrives (Duffie; Hege & Nuti). Do not use a fixed window.
4. **Deployment under pressure destroys returns** (Degeorge et al.). The default of US$3–4bn a year should depend on the regime and on ℓ (verification issue R17).
5. **Evergreen units (S2) carry run and NAV-timing risk** (Couts; Li et al.). Treat them as illiquid in stress.
6. **A deeper secondary market does not remove commitment risk** (Gourier et al.).
7. **A transaction β ≈ 2 for exit values is contested.** Listed buyout shows β ≈ 1.5 (Ennis et al.), and the published Boyer et al. paper is framed around discount rates (verification issue R5).

---

## 2. Citation-integrity table

**Status values:** found, mismatched or not found. A working-paper or online-first year on a Consensus record does not count as a mismatch.

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| Ref 11. Nadauld, Sensoy, Vorkink & Weisbach (2019), *JFE* 132(3):158–181, DOI 10.1016/j.jfineco.2018.11.007; NBER WP 22404 | found [P05][VL] | **Record:** Taylor D. Nadauld et al., 2019, *Journal of Financial Economics*, 66 citations, same DOI. The abstract matches: discount to NAV; buyer PME 1.023 vs seller PME 0.976. **Version note:** the dossier's 0.974 and its age-group tables come from NBER w22404 (2016). Cite them to the WP or re-check against the JFE tables. | [link](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop) |
| Ref 12. Boyer, Nadauld, Vorkink & Weisbach (2018), *Private Equity Indices Based on Secondary Market Transactions*, NBER WP 25207 | found; superseded [WS][P05] | **The WP as cited:** WebSearch confirms the authors, NBER WP 25207 (November 2018), and the content: indices built from secondary prices, 2006–2017, with higher betas and volatilities and lower alphas than NAV-based indices ([NBER](https://www.nber.org/papers/w25207)). **Published successor:** "Discount-Rate Risk in Private Equity: Evidence from Secondary Market Transactions", *JF* 78(2):835–885 (2023), per the verification log and the stream-05 WebSearch; also NBER WP 28691 (2021). Its Consensus record is SSRN 2021, DOI 10.2139/ssrn.3823332, 4 citations. **Action:** cite the JF version and re-check the β figures there. | successor: [link](https://consensus.app/papers/details/d9f67be2c83856ea8703fcd0bfeb3f57/?utm_source=claude_desktop); WP 25207 itself: none |
| Ref 13. Albuquerque, Cassel, Phalippou & Schroth (2018, WP), *Liquidity Provision in the Secondary Market for Private Equity Fund Stakes* (dead Tuck URL) | found [P05][VL][WS] | **Record:** R. Albuquerque et al., 2018, SSRN, DOI 10.2139/ssrn.3182481, 11 citations. One WebSearch found no journal version. **Action:** replace the URL with the DOI. **Content:** the abstract supports "discounts track liquidity provision". A seminar listing found by WebSearch supports the "2009–2016" bid data. The young-fund, VIX, funding-cost and non-specialist details are not in the abstract. | [link](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop) |
| Ref 14. Maurin, Robinson & Strömberg (2023), *A Theory of Liquidity in Private Equity*, *Management Science* 69(10):5740–5771 | found [P05] | **Record:** Vincent Maurin et al., 2022 (online), *Manag. Sci.*, DOI 10.1287/mnsc.2022.4612, 8 citations. An earlier SSRN version exists ([link](https://consensus.app/papers/details/f14343ef7ec55d55a7434fec5d6f5713/?utm_source=claude_desktop), 2020). **Action:** it is a theory paper, so label its claims as model predictions. | [link](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop) |
| Ref 15. Bollen & Sensoy (2022), *How much for a haircut?*, *Financial Management* 51(2):501–538 | found; orphan [P05][VL] | **Record:** Nicolas P. B. Bollen et al., "2016", *Financial Management*, SSRN DOI 10.2139/ssrn.2608549, 14 citations. The full title adds "Illiquidity, secondary markets, and the value of private equity"; the journal DOI is 10.1111/fima.12375 (verification log). **Action:** it is never cited in the G2 text, so cite it (§2.3) or drop it. | [link](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop) |
| Ref 16. Lerner & Schoar (2004), *The illiquidity puzzle*, *JFE* 72(1):3–40 | found [P05] | **Record:** Josh Lerner et al., 2004, *JFE*, 257 citations, DOI 10.1016/s0304-405x(03)00203-4. The abstract supports the screening claim. | [link](https://consensus.app/papers/details/490b5722c3535ebe9382df360741067d/?utm_source=claude_desktop) |
| Ref 17. Allen & Gale (1994), *Limited Market Participation and Volatility of Asset Prices*, *AER* 84(4):933–955 | found (WebSearch) [WS] | **Confirmed:** IDEAS/RePEc lists Franklin Allen & Douglas Gale, *AER* 84(4):933–955, September 1994 ([IDEAS](https://ideas.repec.org/a/aea/aecrev/v84y1994i4p933-55.html)). **Content:** the abstract supports the §2.3 use. Limited participation magnifies liquidity trading; an arbitrarily small aggregate liquidity shock can cause significant volatility; there are multiple equilibria. | none (no Consensus record; Consensus unavailable) |
| Ref 18. Shleifer & Vishny (2011), *Fire Sales in Finance and Macroeconomics*, *JEP* 25(1):29–48 | found [P05][P06] | **Record:** A. Shleifer et al., 2011, *JEP*, 700 citations, DOI 10.1257/jep.25.1.29. | [link](https://consensus.app/papers/details/38094184238d5f8f9fe8944a05e37411/?utm_source=claude_desktop) |
| Ref 19. Bolton, Chen & Wang (2013), *Market Timing, Investment, and Risk Management*, *JFE* 109(1):40–62 | found (WP record) [P08][P09][VL] | **Record:** P. Bolton et al., 2012, venue shown as "Social Science Research Network", 384 citations, DOI 10.2139/ssrn.1571149, same title. **Journal metadata:** confirmed by the verification log. | [link](https://consensus.app/papers/details/e1bcae07d2be506289e7506e93615bb2/?utm_source=claude_desktop) |
| Ref 20. Harris, Jenkinson, Kaplan & Stucke (2018), *Financial intermediation in private equity: How well do funds of funds perform?*, *JFE* 129(2):287–305 | found (WP record) [VL] | **Record:** the NBER WP (2017) record, same title. **Journal version:** confirmed via IDEAS by the verification log. The citation count was not recorded. | [link](https://consensus.app/papers/details/ea5db342103e5bb78ebe02c7fca2fa95/?utm_source=claude_desktop) |
| Ref 21. Gottschalg (2024), *Continuation Funds: Performance and Determinants, 2018-2022 Vintages*, HEC Paris RP 1515 | found [P05][WS] | **Record:** Oliver Gottschalg, 2024, SSRN, DOI 10.2139/ssrn.4752652, 0 citations, no abstract. **WebSearch:** the EBSLG and IDEAS listings give 231 CVs, 140 with performance data, and the same DOI. **Action:** add the DOI. Not peer-reviewed. | [link](https://consensus.app/papers/details/7fed9c1e30af54af9c085178ada5a481/?utm_source=claude_desktop) |
| Ref 22. Gottschalg (2025), *"Continuation Funds" Performance and determinants 2018-2023 vintages*, HEC Paris RP 1584 | found (WebSearch) [WS] | **Confirmed:** the EBSLG listing matches the title and series. It reports 386 CVs, 297 with performance data, and "little return differences across industries, markets, or type of fund" ([EBSLG](https://ebslgwp.hhs.se/heccah/abs/heccah1584.htm)). **Missing:** no Consensus record is known, and only an abstract preview was available. | none (Consensus unavailable) |
| Ref 23. Takahashi & Alexander (2002), *Illiquid Alternative Asset Fund Modeling*, *JPM* 28(2):90–100 | found [P04][P06] | **Record:** 2002, 68 citations, DOI 10.3905/jpm.2002.319836. Consensus labels the venue "Unknown Journal"; the DOI resolves to *JPM*. | [link](https://consensus.app/papers/details/da7ee2d8587e575f99e3a36a590d2be6/?utm_source=claude_desktop) |
| Ref 24. Brown, Ghysels & Gredil (2023), *Nowcasting Net Asset Values: The Case of Private Equity*, *RFS* 36(3):945–986 | found (WP record) [P04][P05] | **Record:** SSRN 2020, DOI 10.2139/ssrn.3507873, 20 citations. The abstract gives buyout β ≈ 1.0 and total risk 33% (venture 1.4 and 40%). **RFS version:** confirmed by the stream-05 WebSearch and the verification log. The RFS numbers may differ from the WP's (stream-07 verifier). | [link](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop) |
| Ref 25. Gourier, Phalippou & Westerfield (2024), *Capital Commitment*, *JF* 79(5):3407–3457 | found (WP record); orphan [P05][P06] | **Record:** SSRN 2024, DOI 10.2139/ssrn.2490430, 8 citations. **JF version:** confirmed by WebSearch in streams 05 and 11. **Action:** not cited anywhere in the G2 text. | [link](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) |
| Ref 26. Luxenberg et al. (2022), *Strategic Asset Allocation with Illiquid Alternatives*, arXiv:2207.07767 | found; add the peer-reviewed version [P01][P04] | **Record:** Proc. 3rd ACM International Conference on AI in Finance (ICAIF '22), DOI 10.1145/3533271.3561769, 4 citations. The abstract matches the dossier's MPC use. | [link](https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop) |
| §2.6 "Rode et al." (cited through the CFA Institute report; no reference entry) | not found [WS] | One WebSearch found no study matching "Rode et al." with lead fees of 60bp against 75bp for the syndicate; only practitioner CV fee surveys came back. **Action:** take the citation from the CFA report's footnote, or drop the figure. | none |
| *Context only, not counted:* Ref 30. Deane & Robinson (Sep-2025), *Continuation Funds: Ethics in Private Markets, Part I*, CFA Institute | indexed in Consensus [P05] | **Record:** Stephen Deane et al., 2025, DOI 10.56227/25.1.29, 0 citations. It is a practitioner research report. **Part II exists:** WebSearch returned `rpc.cfainstitute.org/sites/default/files/docs/research-reports/continuation-funds-ii_online.pdf`, which I did not read. The dossier cites only Part I. | [link](https://consensus.app/papers/details/23aed12e6aa650ac9d160c9cf1c5ed5a/?utm_source=claude_desktop) |
| *Context only, not counted:* Ref 35. Beaudoin et al. (2009), *Trends in the Private Equity Secondary Market*, ABA *Business Law Today* 18(4) | practitioner; not in Consensus | **Confirmed:** title and venue (March/April 2009), by the stream-05 WebSearch. **Not confirmed:** the authors. | none |

---

## 3. Annotated bibliography (25 papers)

**"In dossier"** means in the G2 dossier. Where the URL is not a Consensus URL, the entry says so.

### 3.1 Secondary pricing, liquidity provision and buyer returns (A1–A8)

**A1. [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)** [P05]
- **Record:** Taylor D. Nadauld et al. · 2019 · *Journal of Financial Economics* · 66 citations · DOI 10.1016/j.jfineco.2018.11.007 · In dossier: yes (ref 11).
- **Finding:**
  - Most secondary transactions occur at a discount to NAV.
  - Buyers earn an annualized PME of 1.023 against 0.976 for sellers, about 5pp a year. Flexible buyers earn this by supplying liquidity to investors who want to exit.
- **Relevance:** This is G2's main calibration anchor for the buyer premium (§6.8, target 2).
  - [Inference] The sample is small deals (median US$4.6m of NAV, per the verification log). ADIC's tickets of US$100m to US$1bn trade in wider auctions, so expect a smaller premium.

**A2. [Discount Rate Risk in Private Equity: Evidence from Secondary Market Transactions](https://consensus.app/papers/details/d9f67be2c83856ea8703fcd0bfeb3f57/?utm_source=claude_desktop)** [P05]
- **Record:** Brian H. Boyer et al. · 2021 SSRN record; published *JF* 78(2):835–885 (2023) · 4 citations · DOI 10.2139/ssrn.3823332 · In dossier: no. The dossier cites only the 2018 WP predecessor (ref 12).
- **Finding:**
  - An index built from secondary transaction prices shows that PE discount rates vary considerably.
  - The index's standard alpha is zero, while cash-flow-based measures for the same funds are large and positive.
  - Ignoring this variation misallocates capital.
- **Relevance:**
  - [Inference] Part of each purchase discount, and part of its swings across the regimes in Table 6.7, is a time-varying discount rate. That part is systematic risk.
  - G2 §2.3 splits a discount into a liquidity premium and an information component. It needs a **third, risk-premium component**. That component is beta, not alpha.

**A3. [Liquidity Provision in the Secondary Market for Private Equity Fund Stakes](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop)** [P05]
- **Record:** R. Albuquerque et al. · 2018 · SSRN · 11 citations · DOI 10.2139/ssrn.3182481 · In dossier: yes (ref 13, abstract only).
- **Finding:** The authors use a broker's bid data.
  - The demand response to aggregate liquidity shocks is negatively related to contemporaneous bids.
  - The effect is stronger for funds likely to be offered when liquidity is low.
  - It is unrelated to future NAV returns and to future bidding.

  Discounts therefore track liquidity provision.
- **Relevance:** This supports the liquidity-premium component of young-fund purchases in a crisis.
  - [Inference] Because these discounts do not predict NAV returns, a buyer's crisis gain is a transfer from forced sellers. That transfer is what gives the reserve its value.

**A4. [Liquidity in the Secondaries Private Equity Market](https://consensus.app/papers/details/9bc5ce1dd6415d858fb1193b5b1b3466/?utm_source=claude_desktop)** [P05]
- **Record:** Anya Kleymenova et al. · 2012 · working paper · 10 citations · no DOI · In dossier: no.
- **Finding:** The paper uses auction data from a large advisory firm. Liquidity is measured by the number of bids, the dispersion of bids and excess demand.
  - **An interest is more liquid when:**
    - the fund is larger;
    - it is buyout-focused;
    - it has less undrawn capital;
    - it has made fewer distributions;
    - the manager's funds have traded before.
  - More non-traditional bidders and good market conditions also raise liquidity.
  - The liquidity proxies are positively associated with final bids.
- **Relevance:** This gives G2 a model for expected bidder count $\hat n_j$ and execution probability $e_j$ (verification issues R6 and R12).
  - [Inference] Replace the fixed n = 3 in the winner's-curse haircut, and the fixed e in Table 6.7, with functions fitted to these features from the group's deal-flow log.

**A5. [The Private Equity Secondaries Market During the Financial Crisis and the "Valuation Gap"](https://consensus.app/papers/details/e2a6180114bb5e16be2ab5d849fa5cbf/?utm_source=claude_desktop)** [P05]
- **Record:** U. Hege et al. · 2011 · *The Journal of Private Equity* · 5 citations · DOI 10.3905/jpe.2011.14.3.042 · In dossier: no.
- **Finding:**
  - Effective secondary liquidity collapsed in early 2009 to a fraction of earlier volume.
  - Framing, loss aversion and accounting effects explain the gap between seller and buyer valuations.
  - The market recovered quickly, with no more protracted turbulence than the stock market.
- **Relevance:** This is academic support for regime C: volume collapses and capacity is tiny, but only briefly.
  - [Inference] It supports a post-shock window. It argues against a fixed window of quarters 2–6 and for a state-dependent one.

**A6. [Private Equity Fund Pricing in Secondary Markets: Effects of Taxes and Fund Structure](https://consensus.app/papers/details/480f7ceb6b345835a7453cf1ee01ca84/?utm_source=claude_desktop)** [P05][WS]
- **Record:** Paul Mason et al. · 2023 · *Journal of Alternative Investments* 25:50–59 (volume and pages from a reference list found by WebSearch) · 2 citations · DOI 10.3905/jai.2023.1.182 · In dossier: no.
  - WebSearch names the authors as Paul Mason and Steven Utke.
- **Finding:** Fund legal structure can add a tax discount to the illiquidity discount.
  - The companion summary ([Practical Applications](https://consensus.app/papers/details/c2b14c396c9b52f1b590899447e8b962/?utm_source=claude_desktop)) adds that share classes designed for tax-exempt investors are worth less to taxable buyers.
  - It also says most sellers are tax-exempt and most buyers taxable.
- **Relevance:**
  - [Inference] A tax-exempt sovereign buyer may face less competition for tax-exempt-designed classes, so part of a discount can be a structural edge for ADIC.
  - Add a tax-class term τ to G2-E1 and confirm ADIC's tax status, which the context file does not state.

**A7. [How much for a haircut? Illiquidity, secondary markets, and the value of private equity](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop)** [P05]
- **Record:** Nicolas P. B. Bollen et al. · Consensus record "2016"; *Financial Management* 51(2) (2022) · 14 citations · DOI shown 10.2139/ssrn.2608549 · In dossier: listed (ref 15) but never cited in the text.
- **Finding:** The paper builds a subjective valuation model of LP commitments that includes exits through the secondary market.
  - Breakeven returns are close to observed average fund returns for moderately risk-tolerant LPs with up to 40% in PE.
  - More risk-averse LPs hold little PE, but not none.
- **Relevance:**
  - [Inference] For an LP with ADIC's large private book, illiquidity may already be roughly priced in normal regimes.
  - The liquidity premium available from buying at normal-regime discounts is then small. It concentrates in stress, consistent with A1 and A3.

**A8. [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop)** [P05]
- **Record:** Vincent Maurin et al. · 2022 online (*Management Science* 69(10), 2023) · 8 citations · DOI 10.1287/mnsc.2022.4612 · In dossier: yes (ref 14).
- **Finding:**
  - Sequential capital calls answer GP moral hazard but expose LPs to illiquidity risk.
  - LPs that tolerate illiquidity earn higher returns.
  - GPs may inefficiently accelerate drawdowns to avoid LP default.
  - A secondary market narrows differences in fund returns but not in LP returns.
- **Relevance:** This is the theoretical basis for a deep-pocket buyer's edge.
  - [Inference] For secondary-fund commitments (S1), stress scenarios should include managers *accelerating* calls. This agrees with verification issue R16: test stress call multipliers of at least 1.0x.

### 3.2 What a purchased NAV is worth: staleness, quality and age (A9–A12)

**A9. [Nowcasting Net Asset Values: The Case of Private Equity](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop)** [P04][P05]
- **Record:** Gregory W. Brown et al. · 2020 SSRN record (*RFS* 36(3), 2023) · 20 citations · DOI 10.2139/ssrn.3507873 · In dossier: yes (ref 24, "BGG").
- **Finding:**
  - The method estimates weekly unsmoothed fund NAVs.
  - The average buyout fund has β ≈ 1.0 (venture 1.4) and total risk of 33% a year (venture 40%).
  - Risk-taking and reporting quality persist by manager.
- **Relevance:**
  - It supplies the staleness factor in θ (G2-E2) for each interest.
  - It also supplies a manager-level reporting-quality input to q.
  - Caveat (verification issue R5): the 33% total risk goes with β ≈ 1.0, not with a transaction β ≈ 2.

**A10. [Private Equity Net Asset Values and Future Cash Flows](https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop)** [P05]
- **Record:** Tim Jenkinson et al. · 2019 online (*The Accounting Review*, 2020) · 31 citations · DOI 10.2308/accr-52486 · In dossier: no.
- **Finding:** The sample is 384 VC and 195 buyout funds, 1988–2016.
  - Buyout NAVs show little systematic bias against discounted realized cash flows.
  - VC NAVs are relatively aggressively biased, especially since 2000.
- **Relevance:** [Inference] Mark quality q should be strategy-specific.
  - Set q ≈ 1 for buyout and q < 1 for venture.
  - Part of the venture discount (79% of NAV in H1-2026) is then NAV overstatement, not a buying opportunity.

**A11. [Do private equity funds manipulate reported returns?](https://consensus.app/papers/details/3331159853ab59dea783df670c91ee0a/?utm_source=claude_desktop)** [P05]
- **Record:** Gregory W. Brown et al. · 2019 · *JFE* · 90 citations · DOI on record 10.3386/w22493 · In dossier: no.
- **Finding:**
  - Some under-performing GPs boost reported returns while they are fundraising.
  - Top performers probably understate theirs.
- **Relevance:** [Inference]
  - Reference NAVs struck while the GP is fundraising deserve a lower q in G2-E2.
  - CV reference prices set by a fundraising GP need extra scrutiny under the CV gates (§6.5, item 8).

**A12. [The Evolution of Private Equity Fund Value](https://consensus.app/papers/details/86f58dd5a5655117a6f2b36792e3eabd/?utm_source=claude_desktop)** [P04]
- **Record:** Gregory W. Brown et al. · 2020 · SSRN · 2 citations · DOI 10.2139/ssrn.3621407 · In dossier: no.
- **Finding:** The sample is 1,400 mature buyout and VC funds.
  - Future returns fall off once funds are about 7–8 years old.
  - Dispersion in future IRR and direct alpha *increases* for funds older than five years.
  - Predictors of future returns: distributions to date, dry powder, prior-fund performance, fund size, GP fundraising, prior public-market returns and credit spreads.
- **Relevance:** This bears directly on tail-end purchases.
  - [Inference] Lower expected returns and wider dispersion after year 7–8 support verification issue R2's lower θ_tail (≈0.80–0.83).
  - They also argue for an age-dependent σ in template (a).
  - Its predictors are ready-made features for the hedonic bid model.

### 3.3 Commitments and the fund layer (S1) (A13–A15)

**A13. [Capital Commitment](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop)** [P05]
- **Record:** Elise Gourier et al. · 2024 SSRN record (*JF* 79(5), 2024) · 8 citations · DOI 10.2139/ssrn.2490430 · In dossier: listed (ref 25), not cited in the text.
- **Finding:**
  - Investors are under-allocated to private funds.
  - They would pay more to adjust the amount committed than to remove timing uncertainty or limited tradability.
  - Commitment risk premiums *rise* with secondary-market liquidity and are not diversified away across funds.
- **Relevance:** [Inference]
  - S1 commitments, and purchased interests with large unfunded balances (high U/N), carry a commitment-risk cost. The buy rule G2-E11 should price it.
  - A deeper secondary market does not remove that cost.

**A14. [Optimal Allocation to Private Equity](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop)** [P05]
- **Record:** Nicola Giommetti et al. · 2021 · SSRN · 5 citations · DOI 10.2139/ssrn.3761243 · In dossier: no.
- **Finding:**
  - Repeated commitments substantially change an LP's optimal allocations.
  - The PE allocation is not monotone in risk aversion.
  - An extension adds a secondary market that prices NAV and unfunded liabilities.
- **Relevance:** This is a structural basis for pricing NAV and unfunded commitments separately in G2-E1, as $p\,N-\pi^U U$.
  - [Inference] Young interests heavy in unfunded commitments can then carry very low or negative prices.

**A15. [Financial intermediation in private equity: How well do funds of funds perform?](https://consensus.app/papers/details/ea5db342103e5bb78ebe02c7fca2fa95/?utm_source=claude_desktop)** [VL]
- **Record:** Robert S. Harris et al. · NBER WP 2017 record (*JFE* 129(2), 2018) · citation count not recorded · In dossier: yes (ref 20).
- **Finding (unverified here):** The dossier states that buyout funds of funds beat public markets but trail direct fund investing. The G2 verification log confirmed the reference's metadata, through Consensus and IDEAS, but recorded neither the abstract nor this claim. No project file shows abstract text supporting it.
- **Relevance:** It is the only academic analogue for S1's two layers of fees.
  - [Inference] Use it as a prior that S1 net alpha is lower than that of direct purchases (S3) at the same price.

### 3.4 Continuation vehicles, direct deals and deployment discipline (A16–A19)

**A16. [Continuation Funds: Performance and Determinants, 2018-2022 Vintages](https://consensus.app/papers/details/7fed9c1e30af54af9c085178ada5a481/?utm_source=claude_desktop)** [P05 record; WS abstract]
- **Record:** Oliver Gottschalg · 2024 · SSRN (HEC Paris RP 1515) · 0 citations · DOI 10.2139/ssrn.4752652 · In dossier: yes (refs 21–22).
- **Finding:** Consensus holds no abstract; this comes from the EBSLG and IDEAS abstracts found by WebSearch.
  - The sample is 231 CVs, 140 with performance data.
  - Returns differ little across industries, markets, or single- versus multi-asset vehicles.
  - Returns are comparable, and single-asset CVs show a narrower spread of outcomes.
  - RP 1584 extends the sample to 386 CVs, 297 with performance data.
- **Relevance:** This is the only systematic CV performance source the dossier has.
  - [Inference] The results are interim, mostly unrealised and NAV-based, and the series is not peer-reviewed. They cannot calibrate single-asset SACV risk (verification issues R5 and R15).

**A17. [Continuation Funds: Ethics in Private Markets, Part I](https://consensus.app/papers/details/23aed12e6aa650ac9d160c9cf1c5ed5a/?utm_source=claude_desktop)** [P05]
- **Record:** Stephen Deane et al. · 2025 · CFA Institute · 0 citations · DOI 10.56227/25.1.29 · In dossier: yes (ref 30). It is a practitioner report, not peer-reviewed.
- **Finding:**
  - In a CV the GP sits on both sides.
  - An estimated 80–90% of legacy investors cash out.
  - A fair, competitive bidding process is the main safeguard.
  - Evergreen funds are affecting CVs and secondaries.
- **Relevance:** It supports G2's CV gates.
  - [Inference] The 80–90% cash-out rate sizes the syndicate equity available to ADIC in each CV.

**A18. [On Secondary Buyouts](https://consensus.app/papers/details/7bf7597e234759c785c4d2057d100202/?utm_source=claude_desktop)** [P05]
- **Record:** François Degeorge et al. · 2016 · *JFE* · 91 citations · DOI on record 10.2139/ssrn.2329202 · In dossier: no.
- **Finding:**
  - Secondary buyouts made by buyers under pressure to spend underperform.
  - Without that pressure, they perform like other buyouts.
- **Relevance:**
  - [Inference] A CV is a GP-to-GP asset transfer in which the same GP sits on both sides.
  - Deployment pressure is therefore a measurable risk factor in two places:
    - for the CV leads that ADIC syndicates behind (end of investment period, large dry powder, evergreen inflows);
    - for ADIC's own pacing (verification issue R17).

**A19. [Modeling the exit cashflows of private equity fund investments](https://consensus.app/papers/details/06a53f89abd05350ae89e3e77c5fc5e6/?utm_source=claude_desktop)** [P04]
- **Record:** Christian Tausch et al. · 2022 · *Journal of Risk* · 2 citations · DOI 10.21314/jor.2022.029 · In dossier: no.
- **Finding:** The paper builds a joint deal-level model with two parts:
  - exit timing, designed for interval-censored data;
  - the exit multiple, designed for a high number of defaults.

  It is estimated by maximum likelihood on buyout and VC data and used for Monte Carlo risk management.
- **Relevance:**
  - [Inference] It is a ready replacement for template (c)'s lognormal multiple. Exit time and multiple are drawn jointly, with a point mass at loss, and estimated from data instead of set by hand.
  - This resolves verification issue R5's μ/σ inconsistency.

### 3.5 Dry powder, fire sales and the reserve (A20–A24)

**A20. [Liquidation Values and Debt Capacity: A Market Equilibrium Approach](https://consensus.app/papers/details/fa39990f63685ac6a7cbf5f932b9e7c2/?utm_source=claude_desktop)** [P06]
- **Record:** A. Shleifer et al. · 1992 · *Journal of Finance* · 2,926 citations · DOI 10.1111/j.1540-6261.1992.tb04661.x · In dossier: no. Only the authors' 2011 survey is cited.
- **Finding:**
  - A distressed seller's natural buyers, its industry peers, are usually in trouble at the same time.
  - Assets therefore sell below value in best use, which makes them "cheap in bad times".
- **Relevance:** This is the seminal basis for the countercyclical opportunity in §2.7.
  - [Inference] ADIC's rivals as buyers play the role of "industry peers":
    - secondary funds with fund-level leverage;
    - evergreen vehicles facing redemptions;
    - peer sovereigns caught in the same DPI drought.
  - The opportunity is largest when those buyers are constrained. Their balance sheets, rather than volume, should drive the regime term of the price equation.

**A21. [Fear of Fire Sales, Illiquidity Seeking, and Credit Freezes](https://consensus.app/papers/details/a6c668ff8cfe5396bed107c465c18632/?utm_source=claude_desktop)** [P05]
- **Record:** Douglas W. Diamond et al. · 2011 · *Quarterly Journal of Economics* · 571 citations · DOI 10.1093/qje/qjr012 · In dossier: no.
- **Finding:**
  - An overhang of institutions that may be forced to sell raises the private return to holding illiquid assets.
  - Cash-rich buyers who expect fire sales earn high expected returns on cash, and lock up less in term lending.
- **Relevance:** This is the formal basis for G2's reserve option value $OV_t$.
  - [Inference] It also predicts that ADIC's competitors hold back cash when fire sales are expected. Buying capacity before a crisis is then lower than the headline dedicated capital suggests.

**A22. [Crisis Resolution and Bank Liquidity](https://ideas.repec.org/a/oup/rfinst/v24y2011i6p2166-2205.html)** [WS; IDEAS URL, not Consensus]
- **Record:** Acharya, Shin & Yorulmazer · 2011 · *Review of Financial Studies* 24(6):2166–2205 (page range per RePEc; sources disagree) · citations n/a · DOI 10.1093/rfs/hhq073 · In dossier: no.
- **Finding (abstract):**
  - When banks have expertise in risky assets, those assets clear at fire-sale prices only after many bank failures.
  - Gains from buying at fire-sale prices make holding liquid assets attractive.
  - The resulting liquidity choice is countercyclical: "inefficiently low during economic booms but excessively high during crises".
  - The data are consistent with these predictions.
- **Relevance:** This is the closest academic model of G2's reserve problem.
  - [Inference] Build reserve capacity *ex ante*, in B and N regimes, through committed facilities that Corporate Finance owns.
  - Guard against over-hoarding once a crisis has started.

**A23. [Presidential Address: Asset Price Dynamics with Slow-Moving Capital](https://ideas.repec.org/a/bla/jfinan/v65y2010i4p1237-1267.html)** [WS; IDEAS URL, not Consensus]
- **Record:** Darrell Duffie · 2010 · *Journal of Finance* 65(4):1237–1267 · citations n/a · DOI 10.1111/j.1540-6261.2010.01569.x · In dossier: no.
- **Finding (abstract):**
  - Supply or demand shocks typically produce a sharp price reaction followed by a more extended reversal.
  - The size of the impact and the path of recovery reflect frictions such as search costs and the time intermediaries need to raise capital.
  - Impediments to capital formation in 2007–09 caused price distortions that later subsided.
- **Relevance:** This is the theory behind G2's post-shock window (the W flag).
  - [Inference] Model discount recovery as mean reversion, with a speed set by secondary fundraising and evergreen inflows ($K_t$, $E_t$).
  - Label the W-flag α a prior (verification issue R11).

**A24. [Dynamic Adverse Selection: A Theory of Illiquidity, Fire Sales, and Flight to Quality](https://consensus.app/papers/details/1b0262aa82f6534fb36a9d203ff9ac70/?utm_source=claude_desktop)** [P05]
- **Record:** Veronica Guerrieri et al. · 2014 · *American Economic Review* · 237 citations · DOI 10.1257/aer.104.7.1875 · In dossier: no.
- **Finding:**
  - Better assets trade at higher prices in less liquid markets.
  - High-quality sellers accept a lower probability of trading.
- **Relevance:**
  - [Inference] Deals ADIC can win quickly at deep discounts are adversely selected, especially tail-end and MACV portfolios.
  - Condition θ on how easily a deal clears, and pair this with the winner's-curse haircut.

### 3.6 Evergreen vehicles (A25)

**A25. [Liquidity transformation risks and stabilization tools: Evidence from open-end private equity real estate funds](https://consensus.app/papers/details/abc2df60ee515faa8f6cf53c880555a8/?utm_source=claude_desktop)** [P05]
- **Record:** Spencer J. Couts · 2025 · *Real Estate Economics* · 2 citations · DOI 10.1111/1540-6229.12532 · In dossier: no.
- **Finding:**
  - Stale NAVs invite investors to time their redemptions against the NAV.
  - Redemption queues protect a fund.
  - Liquidity buffers amplify fragility when they are added to queues.
- **Relevance:** This applies both to ADIC's evergreen units (S2) and to evergreen buyers.
  - [Inference] Holding units in an evergreen secondary vehicle with stale NAVs exposes ADIC to dilution by faster redeemers.
  - Treat S2 liquidity as zero in Tier-1 stress.
  - Cut evergreen buyer depth when gates or queues bind.

---

## 4. Missed-but-important papers: design implications for the framework

All items are **[Inference]** unless a sentence restates a cited abstract.

**Ownership** follows the user-confirmed organization:
- The Secondaries group owns asset-level BUY, SELL, HOLD, REFINANCE and LEVER proposals for its hybrid book.
- **Corporate Finance** owns the reserve's funding (committed lines), the FTP curve, deferred payables and facilities.

### 4.1 State variables

| State (new or changed) | Definition | Basis | Owner |
|---|---|---|---|
| $\mu^{dr}_t$, $\mu^{liq}_{s,t}$ | Split $h(s_t)$ in G2-E1 into a market discount-rate factor and a buyer-liquidity factor. | A2, A3, C3 | Secondaries (market intelligence); shared with stream 05 |
| $\hat n_j$, buyer mix | Expected bidder count per opportunity. Fitted on fund size, strategy, U/N, distributions to date, the GP's trading history and the market state. | A4 | Secondaries (deal-flow log) |
| $\tau_j$ | Tax and structure class of the interest, and how well it fits taxable buyers. | A6 | Secondaries with Legal |
| $q_j=q^{strat}q^{fund}q^{mgr}$ | Mark quality from three sources: strategy (VC bias), a GP-fundraising-window flag, and the manager's persistent reporting quality. | A10, A11, C10, A9 | Secondaries and PE (NAV-quality agent) |
| $\mathbf 1\{a_j\ge 7\text{–}8\}$, $\sigma(a_j)$ | Age flag, with lower expected returns and higher dispersion for older funds (tail-end). | A12 | Secondaries |
| $\pi^U_s$ | Price of unfunded commitments, possibly negative. | A13, A14, C9 | Secondaries |
| $DP_j$, $DP^{ADIC}_t$ | Deployment-pressure index for lead GPs and secondary-fund managers (share of investment period elapsed, dry powder against target), and for ADIC's own book. | A18 | Secondaries; IC |
| $K^{spec}_t$, $gate_t$, $queue_t$ | Whether specialist buyer capital is constrained; evergreen gate and redemption-queue state. | A20, C11, A25, C12 | Secondaries → Corporate Finance |
| $\kappa_t$ | Capital-arrival speed (fundraising plus evergreen inflows). It sets how fast discounts recover after a shock. | A23, A5 | Secondaries |

### 4.2 Models

1. **Extended price equation (G2-E1).**
   $$\log p_{j,t}=\log\Pi^k_t+\mu^{dr}_t+\mu^{liq}_{s,t}+g(\text{age},\text{geo},q,\text{size},U/N,\text{software},\tau)-\psi\,AS_j+\varepsilon_{j,t}$$
   - Unfunded commitments are priced separately (A14).
   - $AS_j$ flags discretionary, cherry-picked portfolios (C15).
   - Estimate $\mu^{dr}$ from listed-PE discounts (C3), a high-frequency observable that the semi-annual advisor index lacks, and from the transaction index (A2).
   - Estimate $\mu^{liq}$ from bid depth (A3, A4).
2. **Return decomposition (§3.3, G2-E8).**
   - Split the economic discount into three parts: a liquidity premium, an information or quality part, and a discount-rate risk premium.
   - Only the residual after a market-consistent kernel counts as alpha (A2, C1, C2, C5, C7).
   - Report it under at least two kernels, because estimates vary with method (C5).
3. **Execution and winner's curse.**
   - $e_j=P(\text{close})\cdot P(\text{win}\mid b_j,\hat n_j)$.
   - $\kappa^{wc}_j=\sigma_e\,\mathbb E[\max_{i\le \hat n_j+1}Z_i]$, with $\hat n_j$ from A4 (verification issues R6 and R12; C18).
4. **Recovery dynamics after a shock.**
   - After entering regime C, let $\log p^k_t-\log\bar p^k(s)$ decay at a rate $\kappa_t$ tied to capital arrival (A23).
   - Keep crisis duration short by default (A5).
   - This replaces the fixed W window (quarters 2–6).
5. **Reserve option ($OV_t$, G2-E12).**
   - Use verification issue R3's corrected one-period form: $p_S\,\mathbb E[(NPV_S-L_S)^+]$ against carry plus the forgone NPV of deploying now. Use the duration-consistent $L_s$ from R1.
   - Evaluate it in B and N regimes, *before* stress, following A22 and A21.
   - Drive $NPV_S$ from competitor capital constraints (A20, C11), not from market volume.
6. **CV template (c).**
   - Use a zero-inflated joint model of exit time and multiple, $(T,M)$, estimated from deal data (A19).
   - Simulate MACVs from correlated deal-level draws, not only with $\sigma\sqrt{\rho+(1-\rho)/k}$.
7. **Adverse-selection conditioning.**
   - Lower $\theta_j$ for deals that clear easily at deep discounts.
   - Lower it again for discretionary portfolio cuts (A24, C15).
8. **Evergreen units (S2).** Model redemptions with NAV-staleness timing, queues and gates (A25, C12). Do not credit a fixed 5% of NAV a quarter.

### 4.3 Parameters and calibration priors

These are literature values, not ADIC data.

| Parameter | Literature value | Source | Use | Caveat |
|---|---|---|---|---|
| Buyer–seller return gap | ~5pp a year (PME) overall; ~3pp for funds aged 4–9 | A1 (WP tables, via dossier and verification log) | α prior for direct purchases (S3) | Small-deal sample |
| Discount-rate component | Varies considerably over time; index alpha ≈ 0 | A2 | Split of the regime price term | Magnitude not in the abstract |
| Liquidity risk premium | ~3% a year | C4 | Harvestable premium on diversified purchases | Depends on the factor model |
| Market-implied abnormal return, unlisted PE | −0.5% to +2% a year | C1 | α prior for S1 and S3 | Listed-vehicle sample |
| Buyout β at market prices | ≈1.5 for listed buyout (C2); >2 for the 2018 transaction index (WP 25207) | C2, A2 | Exit-value β range of 1.5–2, each with a *matching* σ (verification issue R5) | Different samples and constructions |
| Fund-level β and total risk | Buyout ≈1.0 and 33%; VC ≈1.4 and 40% | A9 | A consistent β–σ pair at fund level | WP abstract values |
| Tail-end trajectory | Returns fall after year 7–8; dispersion rises after year 5 | A12 | Lower θ_tail; higher σ_tail | Magnitudes not in the abstract |
| CV legacy-LP cash-out | 80–90% | A17 | Syndicate equity supply per CV | Practitioner estimate |
| Listed-PE NAV discount | ≈ −21% after two years | C3 | Level check for the price index | Listed funds, not LP stakes |
| Crisis liquidity | Volume falls to a fraction of earlier levels, then recovers quickly | A5 | Capacity and duration in regime C | 2009 only |
| Discount for an unlisted asset when the seller is constrained | 15–30% | C13 | Cross-asset prior for stress discounts | M&A setting |

### 4.4 Constraints

1. **Deployment-pressure guard (A18; verification issue R17).**
   - Quarterly deployment may not exceed a regime-dependent cap unless the W state holds and LAPV is positive.
   - Screen lead GPs and S1 managers in the last year of their investment period.
2. **Tail-end and MACV caps (A12, A24).** Make them conditional on look-through evidence of NAV quality. The dossier's caps are size-only.
3. **Evergreen units (A25, C12).** Credit zero Tier-1 liquidity in stress, and cap S2 as a share of group NAV.
4. **Commitment risk (A13).** Keep the existing unfunded-plus-deferred cap (§6.5, item 5), but price the commitment-risk premium in G2-E11 as well. Stressed calls alone are not enough.
5. **Tax-structure diligence gate (A6),** for interests in classes designed for other investor types.
6. **Buyer-side leverage (C14).** Deferrals and facility sweeps should enter the facility-covenant chance constraint (§6.5, item 7) on paths where funding and market liquidity tighten *together*.

### 4.5 Objectives and shadow prices

- **Alpha only above a market-consistent kernel.** Group KPIs should show economic IRR alongside NPV under two kernels (A2, C1, C2, C5, C7). Accretion and discount-rate risk premia are not alpha.
- **Reserve through Corporate Finance's FTP.**
  - The Secondaries group pays carry on its earmarked reserve at the FTP rate and is credited with $OV_t$.
  - A22 favours building the reserve in B and N regimes, funded by committed lines, rather than hoarding cash in C.
- **Crisis gains are transfers from forced sellers (A3).**
  - They are worth having only if ADIC is not itself forced (A8, A20).
  - ADIC's own $\ell_s$ in stress therefore decides whether it acts as a buyer or a seller. The total-portfolio objective must arbitrate between the two.
- **S1 hurdle.** Add a commitment-risk premium (A13) and a two-layer-fee prior (A15, C6).

### 4.6 Agent and IC design

- **Secondary-market state agent** (Secondaries group).
  - Decomposes moves in the price index into $\mu^{dr}$ and $\mu^{liq}$ (A2, A3).
  - Tracks competitor capital constraints and evergreen gates and queues (A20, C11, A25).
  - Estimates capital-arrival speed $\kappa_t$ (A23).
  - Feeds Corporate Finance's ℓ curve, under the conflict controls in the context file.
- **Bid-model agent and winner's-curse challenger.**
  - Computes $\hat n_j$ (A4), the haircut $\kappa^{wc}$, and an adverse-selection flag (A24).
  - Rationale: Thaler notes that the winner's curse cannot occur if all bidders are rational, so evidence of it is an anomaly (C18). [Inference] A coded challenger guards against it better than desk judgement does.
- **NAV-quality agent.** Sets q by strategy (A10), fundraising window (A11, C10), manager reporting quality (A9) and age (A12).
- **CV gate checker.**
  - Inputs: CFA Institute Part I (A17); Part II and Jo & Ryu (2026), both still to be read (Section 4.8); Gottschalg's interim evidence (A16); the lead's deployment pressure (A18).
- **IC buy card: new fields.**
  - The discount split into liquidity, discount-rate and quality parts.
  - $\hat n_j$ and $e_j$.
  - The winner's-curse haircut.
  - Tax-class, age and deployment-pressure flags.
  - The reserve's opportunity cost at FTP.
  - The commitment-risk charge.
- **Treasurer / Corporate Finance seat.**
  - Owns reserve funding and its FTP charge, deferred payables and facilities.
  - Signs off the ex-ante reserve policy (A22).

### 4.7 Further relevant papers (compact)

| # | Paper | Record | Finding (abstract) | Use for G2 |
|---|---|---|---|---|
| C1 | [Risk and Expected Returns of Private Equity Investments: Evidence Based on Market Prices](https://consensus.app/papers/details/0e0c66f44a5d50b99383e02fcaf6e5a0/?utm_source=claude_desktop) [P05] | Narasimhan Jegadeesh et al. · 2015 · *RFS* · 88 cit. · DOI 10.1093/rfs/hhv046 | Listed-vehicle prices imply expected abnormal returns of −0.5% to 2% a year for unlisted funds, β near 1, and more systematic risk than NAV indices show | α prior; belief-gap flag for group forecasts |
| C2 | [Buyout Performance with Assets Valued at Market](https://consensus.app/papers/details/3acac11a0e225ab8b04a38002b7e440d/?utm_source=claude_desktop) [P05] | Richard M. Ennis et al. · 2026 · DOI 10.3905/jpmi.2026.011 · 0 cit. | Market-priced listed-PE risk exceeds NAV-based risk; β ≈ 1.5; no significant alpha | Exit-value β range; challenge to β ≈ 2 |
| C3 | [Net asset value discounts in listed private equity funds](https://consensus.app/papers/details/efbe3a9efab257cdb2bd314bdf29d186/?utm_source=claude_desktop) [P05] | Henry Lahr et al. · 2010 · DOI 10.2139/ssrn.1494246 · 8 cit. | Discounts settle at about −21% after two years; premia predict returns and depend on liquidity, sentiment, credit and systematic risk | High-frequency observation equation for the consensus index (§3.2(2)) |
| C4 | [Private Equity Performance and Liquidity Risk](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop) [P05] | Francesco Franzoni et al. · 2012 · *JF* · 251 cit. · DOI 10.1111/j.1540-6261.2012.01788.x | PE loads on a liquidity risk factor; premium about 3% a year, through a funding-liquidity channel | Size of the harvestable premium |
| C5 | [Risk Adjustment in Private Equity Returns](https://consensus.app/papers/details/996d0a57b17957dd81fec3ac0698ec30/?utm_source=claude_desktop) [P05] (**survey**) | Arthur Korteweg · 2019 · *Annual Review of Financial Economics* · 37 cit. · DOI 10.2139/ssrn.3293984 | Risk-adjusted estimates vary substantially with method, period and data | Require two kernels in KPIs |
| C6 | [Valuing Private Equity](https://consensus.app/papers/details/15cb135a45b35616b82e97bf090f24ae/?utm_source=claude_desktop) [P05] | M. Sørensen et al. · 2013 record · *RFS* · 110 cit. · DOI 10.1093/rfs/hhu013 | Fees, carry and illiquidity are costly; LPs may only break even net of them | S1 two-layer-fee hurdle |
| C7 | [Valuing Private Equity Investments Strip by Strip](https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop) [P05] | Arpit Gupta et al. · 2021 · *JF* · 24 cit. · DOI 10.1111/jofi.13073 | Replicating cash flows with listed strips gives negative average risk-adjusted profit in most PE categories | Kernel for economic value V₀ |
| C8 | [Distorting Private Equity Performance: The Rise of Fund Debt](https://consensus.app/papers/details/84b7e9e9b66151e78637a4ebfac077ae/?utm_source=claude_desktop) [P05] | James F. Albertus et al. · 2020 · SSRN · 4 cit. · DOI 10.2139/ssrn.3410076 | Funds with subscription lines show distorted timing-sensitive measures, are disproportionately poor performers and earn more carry | Judge S1 managers on unlevered metrics (the dossier's ILPA point) |
| C9 | [Hidden in Plain Sight—The Impact of Undrawn Commitments](https://consensus.app/papers/details/d99e5eff8f48558898b24269df59ba18/?utm_source=claude_desktop) [P05] | T. Meyer · 2020 · DOI 10.3905/jai.2020.1.101 · 2 cit. | Uncalled capital carries risk and opportunity cost and is priced through larger secondary discounts and subscription lines | $\pi^U$ |
| C10 | [Interim Fund Performance and Fundraising in Private Equity](https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop) [P05] | Brad M. Barber et al. · 2017 · *JFE* · 113 cit. · DOI 10.1016/j.jfineco.2017.01.001 | GPs time fundraising to performance peaks; low-reputation GPs show NAV management | $q^{fund}$ |
| C11 | [The Paradox of Financial Fire Sales: The Role of Arbitrage Capital in Determining Liquidity](https://consensus.app/papers/details/3609684b074f5b77b3cdb79a7a904d82/?utm_source=claude_desktop) [P05] | James Dow et al. · 2018 · *JF* · 36 cit. · DOI 10.1111/jofi.12584 | When specialists are constrained, prices lose information, adverse selection rises and non-specialist capital withdraws | Stress depth below headline dry powder |
| C12 | [Liquidity Restrictions, Runs, and Central Bank Interventions: Evidence from Money Market Funds](https://consensus.app/papers/details/389740373ccf5208b969643b471e31ae/?utm_source=claude_desktop) [P05] | Lei Li et al. · 2021 · *RFS* · 79 cit. · DOI 10.1093/rfs/hhab065 | Gates and fees made the 2020 money-market fund run worse, through strategic complementarities | Analogy for evergreen gates (S2; buyer depth) |
| C13 | [The price of corporate liquidity: Acquisition discounts for unlisted targets](https://consensus.app/papers/details/6f3ed8f7e26c50d29022453169f85362/?utm_source=claude_desktop) [P05] | Micah S. Officer · 2007 · *JFE* · 457 cit. · DOI 10.1016/j.jfineco.2006.01.004 | Unlisted targets sell at 15–30% discounts, larger when the parent is liquidity-constrained and debt is expensive | Stress-discount prior; seller constraint as a driver of opportunity |
| C14 | [Market liquidity and funding liquidity](https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop) [P05] | M. Brunnermeier et al. · 2009 · *RFS* · 5,153 cit. · DOI 10.1093/rfs/hhn098 | Funding and market liquidity reinforce each other; margins can destabilize and cause spirals | Joint stress on deferral, facility sweeps and secondary prices |
| C15 | [The Information in Asset Fire Sales](https://consensus.app/papers/details/26c33fcf27c25a34a7c10c36644285a0/?utm_source=claude_desktop) [P05] | Sheng Huang et al. · 2022 · *Management Science* · 19 cit. · DOI 10.1287/mnsc.2022.4585 | Discretionary sales carry information, expected pro-rata sales do not, and outsiders cannot tell them apart | Lemons markup on cherry-picked LP portfolios |
| C16 | [The Secondary Market](https://consensus.app/papers/details/cdb9a9ebe1a25ea0bfddb958fb777405/?utm_source=claude_desktop) [P05] | P. Cornelius et al. · 2012 · book chapter · 4 cit. · DOI 10.1002/9781119208143.ch6 | The secondary market "should not be perceived as a game changer" for risk management; distressed sellers accept substantial discounts | Context for buyer-side opportunity in stress |
| C17 | [Can investors time their exposure to private equity?](https://consensus.app/papers/details/b5880343ab7b57ebaf68b353dfff48da/?utm_source=claude_desktop) [P05] | Gregory W. Brown et al. · 2020 · *JFE* · 30 cit. · DOI 10.1016/j.jfineco.2020.08.014 | Timing commitments gives modest gains at best, because calls and exits cannot be timed | Test, rather than assume, the value of regime-timed S1 commitments |
| C18 | [Anomalies: The Winner's Curse](https://stafforini.com/pdfs/thaler-1988-anomalies-winner-curse.pdf) [WS; PDF mirror returned by WebSearch, not Consensus] | Thaler · 1988 · *Journal of Economic Perspectives* (volume and pages not confirmed in the results) · cit. n/a | The winner's curse cannot occur if all bidders are rational. More bidders push both toward bidding aggressively and toward a higher chance of having overestimated. The search results trace the concept to Capen, Clapp & Campbell (1971), "Competitive Bidding in High-Risk Situations" | Rationale for the winner's-curse challenger and an n-dependent haircut |
| C19 | [The Art of Commitment Pacing](https://consensus.app/papers/details/662d9b40176f5566bd73002284298286/?utm_source=claude_desktop) [P04][P11] | Meyer · 2024 · book | Book-length treatment of pacing, including how to model co-investments and secondaries | S1 pacing (MPC inputs) |
| C20 | [A Latent Factor Cash Flow Model for Alternative Investment Funds](https://consensus.app/papers/details/bb74f63a8fc15983a1e7753d4057d4f0/?utm_source=claude_desktop) [P05] | Wenbo Cao et al. · 2025 · *FAJ* · 1 cit. · DOI 10.1080/0015198x.2025.2489923 | Extends Takahashi–Alexander with systematic factors, for stress testing and commitment design | Factor version of template (a) |
| C21 | [Equilibrium Liquidity Premia of Private Equity Funds](https://consensus.app/papers/details/b0e4b7258dc2593ca346fa7fab2cc1c1/?utm_source=claude_desktop) [P05] | A. Buchner · 2016 · *J. Risk Finance* · 1 cit. · DOI 10.2139/ssrn.2549694 | Surprise liquidity shocks force secondary sales at a stochastic discount; derives equilibrium liquidity premia | Supply side of the opportunity set |

### 4.8 Identified but not assessable

I report no findings for these. Read them in full before relying on them.

| # | Record | Status | Why it matters |
|---|---|---|---|
| N1 | [Do GPs truly present fair value? The case of continuation funds](https://consensus.app/papers/details/db39905dbfb5585d842909b4318279bc/?utm_source=claude_desktop) [P05] | Crossref [CR] confirms Jinhyeong Jo & Doojin Ryu, *Journal of International Financial Markets, Institutions and Money* 107, article 102265 (March 2026), DOI 10.1016/j.intfin.2025.102265. No abstract is available in Consensus or Crossref, and ScienceDirect returned 403. | The only peer-reviewed test of CV pricing fairness found. Directly relevant to the CV gates and to syndicate pricing. |
| N2 | [Private Equity Secondary Markets](https://consensus.app/papers/details/ade4a116261a53ada3ee2f9eaa6b5dea/?utm_source=claude_desktop) [P05] | Paul Mason et al. · 2023 · SSRN · DOI 10.2139/ssrn.4422541. No abstract; one WebSearch did not find the SSRN page. | Possibly a survey of secondary-market research [Inference]. |
| N3 | CFA Institute, *Continuation Funds II* (practitioner) | WebSearch returned `https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/continuation-funds-ii_online.pdf`; not read. | Sequel to dossier ref 30. |

**Practitioner evidence surfaced by WebSearch [C]; not academic and not checked against primary documents.**
- **Source:** a Capital Dynamics snapshot of Cambridge Associates data, as reported by [Secondaries Investor](https://www.secondariesinvestor.com/capdyn-snapshot/).
- **What it reports:** average net IRR of about 17% for 1993–2009 secondary funds against about 12.3% for primaries. Average net multiple of 1.55x against 1.67x.
- **How it compares:** the direction agrees with Callan (dossier ref 10): similar or higher IRR, lower multiple.

---

## 5. Papers that challenge the dossier's recommendations

| # | Paper(s) | What it challenges (G2 section) | Recommended change |
|---|---|---|---|
| 1 | A2 Boyer et al. (*JF* 2023); C1 Jegadeesh et al.; C2 Ennis et al.; C5 Korteweg; C7 Gupta & Van Nieuwerburgh | **§2.3 implication** (a discount is liquidity premium plus information), **§6.7 "Excess α"** (including the W-flag 4–8%) and **§6.6 KPIs**. Secondary prices embed time-varying discount rates. [Inference] Part of what the dossier calls excess return is compensation for discount-rate risk, which is beta, not alpha. | Add $\mu^{dr}$ to G2-E1. Report α only above a market-consistent kernel, under two kernels. |
| 2 | C2 Ennis et al.; A2 (published framing) | **§6.10 return equations and Overlay link.** Transaction β ≈ 2 is used for buyout exit values and for the overlay hedge ratio. Listed buyout shows β ≈ 1.5. The published Boyer et al. frames the 2018 result as discount-rate risk in *fund-stake* prices (verification issue R5). | Use a β range of 1.5–2, each with a consistent σ. Do not use the β of secondary stake prices as the asset β for hedging. |
| 3 | A12 Brown et al. 2020 | **§6.7 and parameter defaults: θ_tail = 0.88–0.92.** Returns fall off after year 7–8 and dispersion rises after year 5. Together with Nadauld's tail-end data (verification issue R2), θ_tail is too high, and it makes tail-ends look like the best trade in every regime. | Set θ_tail ≈ 0.80–0.83 in N, lower in D, and use an age-dependent σ. |
| 4 | A22 Acharya, Shin & Yorulmazer | **PACE rule and G2-E12 reserve.** Reserves are built or released in response to ℓ_S. Privately chosen liquidity is "inefficiently low during economic booms but excessively high during crises". | Set reserve capacity ex ante, in B and N regimes, through Corporate Finance's committed lines. Use verification issue R3's corrected $OV_t$. Cap hoarding in C. |
| 5 | A23 Duffie; A5 Hege & Nuti | **§3.4 lag structure and the W flag** (fixed quarters 2–6; α 4–8%). The recovery path depends on how fast capital arrives, and 2009 recovered quickly (verification issue R11). | Use state-dependent recovery driven by $\kappa_t$. Tag the W-flag α as a prior and stress-test it. |
| 6 | A18 Degeorge et al. | **§6.1 default deployment of US$3–4bn a year** (verification issue R17), and S1 manager selection. Buyers under pressure to spend underperform. | Make pacing regime- and ℓ-conditional, add the deployment-pressure guard, and screen managers and CV leads for pressure. |
| 7 | A7 Bollen & Sensoy (published abstract) | **§2.3 "a liquidity premium, which a long-horizon sovereign can harvest".** For moderately risk-tolerant LPs with up to 40% in PE, breakeven returns roughly equal observed returns. This is only a mild challenge, because the dossier already sets α to 0–2% in B and N. | Keep the normal-regime premium small. Value liquidity harvesting mainly in stress (A1, A3). |
| 8 | A13 Gourier et al. | **§6.5 items 5–6 (unfunded handled through stressed calls only).** Commitment-risk premiums are not diversified away, and they *rise* with secondary liquidity. | Add a commitment-risk charge to G2-E11 for S1 and for unfunded-heavy purchases. |
| 9 | A25 Couts; C12 Li et al. | **§2.1 S2 evergreen units** ("about 5% of NAV per quarter, gated in stress") and **§4.2 evergreen depth**. Stale NAVs invite redemption timing, and gates and buffers can amplify runs. | Credit S2 with zero Tier-1 liquidity in stress, model dilution risk, and haircut evergreen buyer depth when gates or queues bind. |
| 10 | A10 Jenkinson et al.; A11 Brown et al. 2019 | **Parameter default θ = 0.96 (4–9 years), the same for every strategy.** VC NAVs are aggressively biased, and fundraising-window NAVs are inflated by some GPs. | Make q depend on strategy and GP state. Lower θ for venture and for fundraising-window reference NAVs. |
| 11 | C17 Brown et al. 2020 (timing) | **§3.1(b) "the vintage regime fixes the discount" and regime-timed S1 commitments.** For primary PE, timing commitments yields modest gains at best. [Inference] S1 deploys within about 4 years, so more of the timing effect may survive than in primaries. | Test the value of regime timing by simulation in the MPC (§3.5) rather than assuming it. |

---

## 6. Verbatim usage message

The last usage message returned by Consensus in this session, quoted exactly (it appeared as the error text on all three calls):

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Scope notes and method

- **Consensus (3 calls, all failed).**
  - Query: the Nadauld et al. title, with no filters.
  - All three calls returned the quota error. I waited 30 seconds before each retry, then stopped after three, as the protocol requires.
  - Calls were strictly sequential. No thread tools were used.
- **Reused Consensus records.**
  - All Consensus URLs in this file were copied unchanged from project files written earlier today: [P01], [P04], [P05], [P06], [P08], [P09], [P11] and [VL].
  - Those agents ran unfiltered Consensus searches, according to their own scope notes.
  - Record metadata, including citation counts, are as those files report them.
- **WebSearch (13 calls), used only where Consensus could not supply the information:**
  1. Allen & Gale (1994).
  2. Gottschalg RP 1584.
  3. Boyer et al. WP 25207.
  4. "Rode et al."
  5. Published version of Albuquerque et al.
  6. Jo & Ryu abstract.
  7. Academic CV studies, 2024–2026: none found.
  8. Secondary-fund performance studies: practitioner results only.
  9. 2023–2025 papers on LP-stake pricing: none new.
  10. Mason et al. (SSRN 4422541).
  11. Duffie (2010).
  12. Acharya, Shin & Yorulmazer (2011).
  13. Winner's-curse sources.
- **WebFetch (3 calls):**
  - the DOI redirect for Jo & Ryu;
  - ScienceDirect, which returned 403;
  - Crossref, which returned Jo & Ryu's metadata without an abstract.
- **What I did not do.**
  - I read no full texts.
  - I ran no new Consensus backfill. The four seed queries were not run in Consensus. The backfill relies on records other agents retrieved today with related queries, including the stream-05 queries on secondary-fund performance, continuation funds and evergreen funds, plus WebSearch.
- **Recommendation to the orchestrator.** After the quota resets on 1 November 2026, re-run in Consensus:
  1. the four seed queries;
  2. the citation look-ups for Allen & Gale, Gottschalg RP 1584, Duffie (2010) and Acharya, Shin & Yorulmazer (2011);
  3. a query for 2025–2026 papers on secondary-fund performance and continuation vehicles.

  Then swap in Consensus URLs where only web URLs appear here.
- **Overlap with stream 05.**
  - Stream 05 covers ADIC as a *seller*. This file reuses its records but draws buyer-side implications: the buy rule, the reserve, the winner's curse, θ, the CV template and S2.
  - Shared state variables ($\mu^{dr}$, $\mu^{liq}$, $\pi^U$, evergreen gate state) should be defined once and used by both streams.
