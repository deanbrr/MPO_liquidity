# Stream 05 literature check: secondaries, NAV financing, continuation vehicles, preferred equity and CFOs

**Dossier checked:** `research/dossiers/05_secondaries_navfin.md` (as of 2026-10-18, 36 references).
**Date:** 2026-10-18.
**Search engine:** Consensus. I ran 19 searches, one at a time and without filters: 5 citation look-ups and 14 topical backfill searches. I also ran 4 WebSearches: one to resolve a citation that Consensus does not index, and three to confirm the published versions of SSRN records.
**Companion:** `research/verification/05_secondaries_navfin.verify.md`.

**Reading conventions**
- Findings come only from the titles and abstracts that Consensus returned. I did not read full texts.
- **[Inference]** marks design reasoning that goes beyond what an abstract states.
- Author lists appear as Consensus displays them, with "et al." where Consensus truncates.
- Years are Consensus record years. Published versions confirmed by WebSearch or by a verification log are noted separately.
- "In dossier" refers to stream 05 only. Where another stream already cites a paper I say so, so the streams can cross-reference instead of duplicating work.
- Codes: **B1–B25** are the annotated papers (Section 3), **F1–F35** the further missed papers (Section 4.7), and **U1–U8** the records Consensus holds without abstracts (Section 4.8).
- **Organizational mapping.** This follows the user's confirmations of 2026-10-18:
  - The **Secondaries group** is a hybrid book of fund commitments and direct deals.
  - **Capital Solutions** prices NAV and preferred-equity deals.
  - **Corporate Finance owns Treasury**: the liquidity gate, portfolio-level facilities, collateral and owner distributions.

---

## 1. Summary

### Citation integrity
- **Scope.** The reference list is almost entirely practitioner material: advisor reports, law-firm notes, ILPA guidance and press. I checked all eight items that could count as academic or quasi-academic:
  - **Four academic works** in the reference list (refs 14–17).
  - **Three methods** the text names by author but never lists: Dixit–Pindyck (§2.3), Longstaff–Schwartz (§7) and Heckman (§7).
  - **Ref 19**, a practitioner article in an ABA periodical.
- **Result.** 7 found, 1 mismatched, 0 not found. No hallucinated references.
- **Fixes needed:**
  1. **Bollen & Sensoy (ref 15): wrong source for a number.** The metadata are correct, but the claim is not from the published paper.
     - The dossier says illiquidity raises the required return by "up to 5–10 pp".
     - The published abstract that Consensus indexes says something else: breakeven returns are close to observed fund returns for moderately risk-tolerant LPs with up to 40% in PE.
     - The 5–10 pp figure comes from the 2015 working paper and should be cited to it. This agrees with verification item F10.
  2. **Maurin, Robinson & Strömberg (ref 17).** The dossier wrote the authors "from memory". Consensus confirms them. Add 2023, 69(10):5740–5771 (Crossref, via the verification log).
  3. **Albuquerque et al. (ref 16).** Add the SSRN DOI 10.2139/ssrn.3182481. Its abstract is now available, so "findings not retrieved" can be replaced (see B3).
  4. **Dixit–Pindyck, Longstaff–Schwartz and Heckman.** All three exist and are invoked correctly, but none is in §10. Add full references.
  5. **WilmerHale (ref 19): wrong title.** The article is "Trends in the Private Equity Secondary Market", *Business Law Today* 18(4), March/April 2009. One WebSearch confirmed this; Consensus does not index the article.
  6. **Nadauld et al. (ref 14).** Add 132(3):158–181 (from the verification log).
  7. **"Evercore/HEC" (§3.2(3)).** There is no reference entry, and I could not identify an HEC academic source.
     - [Inference] One candidate is Gottschalg (2024, SSRN; U4), a continuation-vehicle (CV) performance paper by an HEC Paris author (affiliation from general knowledge, not from Consensus).
     - Consensus holds no abstract for it, so the claim remains unconfirmed.

### Backfill (14 topical searches)
- I ran the five seed queries plus nine refinements. 68 relevant records are listed:
  - 25 annotated in Section 3;
  - 35 tabulated in Section 4.7;
  - 8 without abstracts in Section 4.8.
- **The dossier misses eight clusters of work:**
  1. **Market-based PE discount rates and secondary price indices.** Boyer et al. (*JF* 2023), plus listed-PE evidence from Jegadeesh et al., Lahr & Herschke and Ennis et al.
  2. **How the market for LP interests works.**
     - What drives bidder counts and buyer mix: Kleymenova et al.
     - Tax and fund-structure discounts: Mason & Utke.
     - The 2009 "valuation gap": Hege & Nuti.
     - Transfer restrictions as a way for GPs to screen LPs: Lerner & Schoar.
  3. **Commitment risk and the price of unfunded commitments.** Gourier et al. (*JF* 2024), Giommetti et al. and Meyer.
  4. **How NAVs are measured and biased.** Brown, Ghysels & Gredil; Jenkinson et al.; Brown, Gredil & Kaplan; Barber & Yasuda.
  5. **Fund-level debt.** Albertus & Denes; Schillinger et al.; Brown et al. (2024).
  6. **CFO cash-flow modelling and structured-finance model risk.** de Malherbe; Billias et al.; the *JEP* (2009) structured-finance paper; the correlated-collateral paper.
  7. **Fire sales, adverse selection and funding liquidity.** Shleifer & Vishny; Brunnermeier & Pedersen; Gârleanu & Pedersen; Diamond & Rajan; Huang et al.; Chaderina et al.; Guerrieri & Shimer; Dow & Han.
  8. **Fragility of evergreen buyers.** Li et al. (*RFS* 2021) on redemption gates and Couts (2025) on queues and buffers.
- **The academic literature on the instruments themselves is thin.**
  - For NAV loans, preferred equity and continuation vehicles, Consensus returns only 2024–2026 SSRN papers and one journal article, all without abstracts (U1–U5), plus one CFA Institute report on CVs (F25).
  - The dossier therefore has no alternative to practitioner data for these instruments.
  - Keep their parameters tagged [C] or [I], with wide robustness ranges.
- **Overlap with other streams.**
  - These papers are already cited in streams 04, 06, 07 or 08:
    - Brown–Ghysels–Gredil;
    - Gupta–Van Nieuwerburgh;
    - Gourier et al.;
    - Giommetti & Sørensen;
    - Jegadeesh et al.;
    - Franzoni et al.;
    - Jenkinson et al.;
    - Shleifer–Vishny;
    - Brunnermeier–Pedersen.

    Stream 05 should cross-reference them.
  - Streams 07 and G2 cite the authors' 2018 NBER index paper (w25207), not the 2023 *JF* discount-rate paper (B2).

### Challenges
- **Discount-rate risk explains more than illiquidity does.**
  - Five papers imply that most of the "alpha" in NAV-based and cash-flow-based measures disappears under market-consistent discount rates: Boyer et al., Jegadeesh et al., Gupta & Van Nieuwerburgh, Sørensen, Wang & Yang, and Ennis et al.
  - [Inference] The hold value implied by strategy-group forecasts is therefore probably overstated.
  - Two dossier figures need re-basing on a common market kernel: the implied cost of selling quality buyout (8–15%) and the reading of the belief gap.
- **CFO senior notes are not a cheap rung free of model risk.** Tranche safety depends on correlation assumptions, and tranching amplifies estimation error.
- **The first rung of a crisis pecking order can be crowded.** Selling the most liquid, widely held assets first can backfire.
- **Commitment sizing matters more than tradability.** Investors would pay more to adjust the amount committed than to remove limited tradability.
- **Selection corrections are fragile.** Heckman-type corrections need credible exclusion restrictions.

None of these overturns the dossier's architecture (action library → marginal-cost-of-liquidity (MCL) curve → λ). They do change the price equation, the pricing kernel, the CFO and crisis calibrations, and the action set. Sections 4 and 5 give the details.

---

## 2. Citation-integrity table

Status values are found, mismatched or not found. A gap between online-first and print years, or a working-paper year shown on a Consensus record, does not count as a mismatch.

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| Ref 14. Nadauld, Sensoy, Vorkink & Weisbach (2019), *JFE*, DOI 10.1016/j.jfineco.2018.11.007; NBER WP 22404 | found | Taylor D. Nadauld et al., 2019, *Journal of Financial Economics*, 66 citations, same DOI. The abstract matches the dossier: buyer PME 1.023 vs seller PME 0.976, about 5 pp a year. Add 132(3):158–181 (from the verification log; Consensus does not show it). | [link](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop) |
| Ref 15. Bollen & Sensoy (2022), *Financial Management* 51(2):501–538, DOI 10.1111/fima.12375; WP 2015 | found (content attributed to the wrong version) | Consensus record: Nicolas P. B. Bollen et al., "2016", *Financial Management*, with the SSRN DOI 10.2139/ssrn.2608549, 14 citations. The dossier's metadata are correct; Consensus attaches the SSRN year and DOI. The abstract (published version) reports breakeven returns close to observed returns for moderately risk-tolerant LPs with up to 40% in PE and makes no "5–10 pp" statement. Cite that number to the 2015 WP. | [link](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop) |
| Ref 16. Albuquerque, Cassel, Phalippou & Schroth (2018), working paper; "findings not retrieved" | found | R. Albuquerque et al., 2018, SSRN, DOI 10.2139/ssrn.3182481, 11 citations. Add the DOI. The abstract is available; see B3. | [link](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop) |
| Ref 17. *A Theory of Liquidity in Private Equity*, *Management Science*, DOI 10.1287/mnsc.2022.4612; authors "from memory, not re-verified" | found | Vincent Maurin et al., 2022 (online), *Manag. Sci.*, same DOI, 8 citations. The funding note names Maurin, Strömberg and Robinson, which confirms the dossier's authors. Print: 69(10):5740–5771 (2023), per the verification log. An earlier SSRN version exists ([link](https://consensus.app/papers/details/f14343ef7ec55d55a7434fec5d6f5713/?utm_source=claude_desktop), 2020, DOI 10.2139/ssrn.3527298). | [link](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop) |
| §2.3 "Dixit-Pindyck" (in text; no reference entry) | found | Dixit, A. & Pindyck, R. (1994), *Investment under Uncertainty*, Princeton University Press. Consensus indexes the book through a 1994 *Journal of Finance* record whose abstract is the book's description (author shown as "E. Schwartz", DOI 10.2307/2329279, 7,403 citations); [Inference] most likely a JF book review. The Princeton 1994 details appear in an indexed citing abstract ([Dikos et al. 2012](https://consensus.app/papers/details/5f8ebc4bd9175b8dbed181d9118a9256/?utm_source=claude_desktop)). Add to §10. | [link](https://consensus.app/papers/details/cd37622c7e6b520eb023e1fc950ea746/?utm_source=claude_desktop) |
| §7 "Longstaff-Schwartz least-squares Monte Carlo" (no reference entry) | found | Longstaff, F. & Schwartz, E. (2001), "Valuing American Options by Simulation: A Simple Least-Squares Approach", *RFS* 14(1):113–147, DOI 10.1093/rfs/14.1.113, 3,480 citations. Consensus truncates the venue to "The Finance"; volume and pages are quoted in an indexed citing abstract ([Wu et al. 2014](https://consensus.app/papers/details/a05d494aa4b85679be6ae43d410751c6/?utm_source=claude_desktop)). Add to §10. | [link](https://consensus.app/papers/details/80f7e4358bab534185c423e61ad9ce8e/?utm_source=claude_desktop) |
| §7 "Heckman-style" selection equation (no reference entry) | found | Heckman, J. (1979), "Sample selection bias as a specification error", DOI 10.2307/1912352, 30,146 citations. The DOI is *Econometrica*'s JSTOR DOI, though Consensus labels the venue "Applied Econometrics". Add to §10. | [link](https://consensus.app/papers/details/a410156e488f5b9b94d6aa91e56aa360/?utm_source=claude_desktop) |
| Ref 19. WilmerHale / ABA *Business Law Today* 18(4), Mar/Apr-2009, "Secondary market for private equity interests" | mismatched (title) | Consensus does not index it. One WebSearch confirms the title as **"Trends in the Private Equity Secondary Market"**, *Business Law Today* 18(4), March/April 2009 ([WilmerHale page](https://www.wilmerhale.com/en/insights/publications/trends-in-the-private-equity-secondary-market-march-april-2009)). The verification log names the authors as Beaudoin, Berrent, Evans and Rothermel; the search did not confirm them. It is a practitioner article, not peer-reviewed. | none (not in Consensus) |

**Not tabulated.**
- **§3.2(3) "Evercore/HEC".** It has no reference entry and no identifiable academic work, so I could not check it. See the fixes list, item 7.
- **Practitioner references (refs 1–13, 18, 20–36).** These are advisor reports, ILPA documents, law-firm notes and press. They are outside an academic citation check. The verification log covers most of them.

---

## 3. Annotated bibliography (25 papers)

### 3.1 How LP interests are priced, and what liquidity costs (B1–B11)

**B1. [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)**
- **Record:** Taylor D. Nadauld et al. · 2019 · *Journal of Financial Economics* · 66 citations · DOI 10.1016/j.jfineco.2018.11.007. In dossier: yes (ref 14).
- **Finding:** Using proprietary intermediary data, the paper finds that most transactions occur at a discount to NAV. Buyers earn an annualized PME of 1.023 against 0.976 for sellers, about 5 pp a year market-adjusted. Flexible buyers earn returns by supplying liquidity to investors who want to exit.
- **Relevance to ADIC:** This is the empirical anchor for the liquidity-transfer part of $y_{mkt}-y_{hold}$ and for the hedonic features.
  - [Inference] The 5 pp gap is an average across sellers. A deep-pocket seller selling from strength should pay less, which is the reasoning behind the dossier's "sell from strength" policy.

**B2. [Discount Rate Risk in Private Equity: Evidence from Secondary Market Transactions](https://consensus.app/papers/details/d9f67be2c83856ea8703fcd0bfeb3f57/?utm_source=claude_desktop)**
- **Record:** Brian H. Boyer et al. · 2021 (SSRN record) · 4 citations · DOI 10.2139/ssrn.3823332.
  - **Published version:** *Journal of Finance* 78(2):835–885 (2023), confirmed by WebSearch through the [IDEAS/RePEc record](https://ideas.repec.org/a/bla/jfinan/v78y2023i2p835-885.html).
  - In dossier: no. Streams 07 and G2 cite the authors' 2018 NBER WP 25207 instead.
- **Finding:**
  - An index built from secondary transaction prices shows that PE discount rates vary considerably.
  - The index's standard alpha is zero, yet cash-flow-based performance measures for the same funds are large and positive.
  - Ignoring this variation can misallocate capital.
- **Relevance to ADIC:** This bears directly on two dossier components: the consensus secondary-price index (§3.3) and the staleness decomposition (§2.2).
  - [Inference] Part of the observed discount, and part of its movement across regimes, is a time-varying discount rate rather than a liquidity cost.
  - The decomposition therefore needs a discount-rate term, and the belief gap Δy should be measured against a market-consistent discount rate, not against cash-flow IRRs.

**B3. [Liquidity Provision in the Secondary Market for Private Equity Fund Stakes](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop)**
- **Record:** R. Albuquerque et al. · 2018 · SSRN · 11 citations · DOI 10.2139/ssrn.3182481. In dossier: yes (ref 16, "findings not retrieved").
- **Finding:** Using a broker's bid data, the authors show three things:
  - The demand response to aggregate liquidity shocks is negatively related to contemporaneous bids.
  - The effect is stronger for funds likely to be offered in low-liquidity periods.
  - It is unrelated to future NAV-to-NAV returns and to future bidding.

  Discount variation therefore tracks variation in liquidity provision.
- **Relevance to ADIC:** This fills the gap the dossier acknowledges.
  - [Inference] The regime term of the price equation should be modelled as a buyer-liquidity factor, separate from fundamentals.
  - Because these discounts do not predict NAV returns, crisis discounts behave like a pure transfer to buyers. That strengthens the "never be a forced seller" constraint and the option value of waiting.

**B4. [Liquidity in the Secondaries Private Equity Market](https://consensus.app/papers/details/9bc5ce1dd6415d858fb1193b5b1b3466/?utm_source=claude_desktop)**
- **Record:** Anya Kleymenova et al. · 2012 · working paper (venue unknown) · 10 citations · no DOI. In dossier: no.
- **Finding:** The paper measures liquidity from auction data supplied by a large advisory firm (the acknowledgments thank Cogent Partners), using the number of bids, the variation in bids and excess demand.
  - **A fund interest is more liquid when:**
    - the fund is larger;
    - it is buyout-focused;
    - it has less undrawn capital;
    - it has made fewer distributions;
    - the manager's funds have traded before.
  - Liquidity also improves when more non-traditional buyers bid and market conditions are good.
  - Liquidity proxies are positively associated with final bids.
- **Relevance to ADIC:** This supplies features and an execution model for §3.3 and §3.4.
  - [Inference] Make expected bidder count and buyer mix state variables.
  - Make $p_j$ and price impact functions of fund size, strategy, undrawn share and the GP's secondary-trading history.

**B5. [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop)**
- **Record:** Vincent Maurin et al. · 2022 (online; print 2023) · *Management Science* · 8 citations · DOI 10.1287/mnsc.2022.4612. In dossier: yes (ref 17).
- **Finding:**
  - Sequential capital calls are the optimal answer to GP moral hazard, but they expose LPs to illiquidity risk.
  - LPs that tolerate more illiquidity earn higher returns.
  - GPs may inefficiently accelerate drawdowns to avoid LP default.
  - A secondary market narrows differences in fund returns but not differences in LP returns.
- **Relevance to ADIC:** This is the theoretical basis for a deep-pocket LP to harvest an illiquidity premium and to keep the buffer that prevents forced sales.
  - [Inference] The stressed cash-flow scenarios should include drawdowns accelerated under stress (call bunching), not only subscription-line catch-up.

**B6. [How much for a haircut? Illiquidity, secondary markets, and the value of private equity](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop)**
- **Record:** Nicolas P. B. Bollen et al. · 2016 (Consensus record; SSRN DOI) · *Financial Management* · 14 citations · DOI shown 10.2139/ssrn.2608549. In dossier: yes (ref 15).
- **Finding:** The paper builds a subjective valuation model of LP commitments that includes secondary-market exits.
  - Model breakeven returns are close to observed average fund returns for moderately risk-tolerant LPs with PE allocations up to 40%.
  - More risk-averse LPs put little, but not zero, weight on PE.
- **Relevance to ADIC:** The lattice is a template for the sell-or-hold valuation (§2.3).
  - [Inference] The published headline suggests that, for a risk-tolerant LP near ADIC's PE weight, illiquidity is already priced into observed returns. The dossier's "5–10 pp" figure belongs to the 2015 WP.

**B7. [The Illiquidity Puzzle: Theory and Evidence from Private Equity](https://consensus.app/papers/details/490b5722c3535ebe9382df360741067d/?utm_source=claude_desktop)**
- **Record:** Josh Lerner et al. · 2004 · *Journal of Financial Economics* · 257 citations · DOI 10.1016/s0304-405x(03)00203-4. In dossier: no (cited in group dossiers G1 and G2).
- **Finding:** GPs set transfer restrictions to screen for "deep pocket" LPs that rarely face liquidity shocks.
  - Restrictions are less common in a firm's later funds.
  - They are less prevalent where the LPs are known for few liquidity shocks, such as endowments and foundations.
- **Relevance to ADIC:** This grounds the transferability state $g_i$ and the signalling cost.
  - [Inference] A sovereign that becomes a visible repeat seller may lose its deep-pocket standing with GPs, raising future access costs.
  - Signal_k should therefore rise with the frequency and visibility of ADIC's sales.

**B8. [Capital Commitment](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop)**
- **Record:** Elise Gourier et al. · 2024 (SSRN record) · 8 citations · DOI 10.2139/ssrn.2490430.
  - **Published version:** *Journal of Finance* 79(5):3407–3457 (2024), confirmed by WebSearch and by the stream-04 verification log.
  - In dossier: no; stream 04 cites it.
- **Finding:** In a dynamic portfolio model with ex-ante commitment, investors are under-allocated to private funds.
  - They would pay more to adjust the amount committed than to remove timing uncertainty or limited tradability.
  - Commitment risk premiums *rise* with secondary-market liquidity, and diversifying across funds does not remove them.
- **Relevance to ADIC:**
  - [Inference] Resizing or shedding unfunded commitments is the most valuable liquidity lever. This supports the dossier's correction (b) on unfunded transfer.
  - Commitment sizing deserves first-class action status next to SELL and REFINANCE.
  - Secondary-market depth does not remove commitment risk.

**B9. [Optimal Allocation to Private Equity](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop)**
- **Record:** Nicola Giommetti et al. · 2021 · SSRN · 5 citations · DOI 10.2139/ssrn.3761243. In dossier: no (cited in stream 04 and in literature files 01 and 02).
- **Finding:** An LP repeatedly commits to PE funds, and these investments substantially change its optimal allocations.
  - The PE allocation is not monotone in risk aversion.
  - An extension adds a secondary market to price NAV and unfunded liabilities.
- **Relevance to ADIC:** This is a structural basis for pricing NAV and unfunded commitments separately.
  - [Inference] Give the hedonic model separate NAV and unfunded terms, which allows negative prices for unfunded-heavy interests (dossier §7, pitfall 5).

**B10. [Private Equity Fund Pricing in Secondary Markets: Effects of Taxes and Fund Structure](https://consensus.app/papers/details/480f7ceb6b345835a7453cf1ee01ca84/?utm_source=claude_desktop)**
- **Record:** Paul Mason et al. · 2023 · Consensus venue unknown; the DOI indicates *J. Alternative Investments* · 2 citations · DOI 10.3905/jai.2023.1.182. In dossier: no.
- **Finding:** Fund legal structure can impose a tax discount on top of the illiquidity discount.
  - The companion summary ([Practical Applications](https://consensus.app/papers/details/c2b14c396c9b52f1b590899447e8b962/?utm_source=claude_desktop)) adds that classes designed for tax-exempt investors are worth less to taxable buyers.
  - It also says most sellers are tax-exempt and most buyers taxable.
- **Relevance to ADIC:**
  - [Inference] A sovereign may hold share classes or feeders built for tax-exempt holders.
  - Add a tax and structure term $d^{tax}$ to the §2.2 decomposition, and a class-mismatch feature to the hedonic model.
  - The same term matters for the Secondaries group's own bids.

**B11. [The Private Equity Secondaries Market During the Financial Crisis and the "Valuation Gap"](https://consensus.app/papers/details/e2a6180114bb5e16be2ab5d849fa5cbf/?utm_source=claude_desktop)**
- **Record:** U. Hege et al. · 2011 · *The Journal of Private Equity* · 5 citations · DOI 10.3905/jpe.2011.14.3.042. In dossier: no.
- **Finding:**
  - Effective secondary liquidity collapsed in early 2009 to a fraction of earlier volume.
  - Framing, loss aversion and accounting effects explain the gap between seller and buyer valuations.
  - The market recovered quickly, with no more protracted turbulence than the stock market.
- **Relevance to ADIC:**
  - [Inference] Use a crisis regime in which volume collapses and execution probability falls close to zero.
  - The state should be short-lived, which raises the value of waiting.
  - The IC should see crisis prices as both low and transient.

### 3.2 NAV measurement and market-implied valuation (B12–B15)

**B12. [Nowcasting Net Asset Values: The Case of Private Equity](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop)**
- **Record:** Gregory W. Brown et al. · 2020 (SSRN record) · 20 citations · DOI 10.2139/ssrn.3507873.
  - **Published version:** *RFS* 36(3):945–986 (2023), DOI 10.1093/rfs/hhac045 (WebSearch; also cited in streams 04 and 07).
  - In dossier: no.
- **Finding:** The method estimates weekly unsmoothed NAVs for individual funds and outperforms simple extrapolation.
  - The average buyout fund has a market beta of about 1.0 and the average venture fund about 1.4.
  - Total risk is 33% a year for buyout and 40% for venture.
  - Risk-taking and reporting quality persist by manager.
- **Relevance to ADIC:**
  - It supplies the de-smoothed value $\hat V_{i,t}$ that the staleness adjustment and discount calculation need.
  - It also supplies the volatilities for the NAV-covenant chance constraint and for CFO LTV tests.
  - Caveat: the stream-07 verifier notes that the RFS numbers can differ from the WP numbers.

**B13. [Private Equity Net Asset Values and Future Cash Flows](https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop)**
- **Record:** Tim Jenkinson et al. · 2019 (print 2020) · *The Accounting Review* · 31 citations · DOI 10.2308/accr-52486. In dossier: no (stream 07 cites it).
- **Finding:** The sample is 384 VC and 195 buyout funds from 1988 to 2016.
  - Buyout NAVs show little systematic bias against discounted realized cash flows.
  - VC NAVs are relatively aggressively biased, especially since 2000.
- **Relevance to ADIC:**
  - [Inference] Part of the larger VC secondary discount may be NAV overstatement rather than illiquidity.
  - NAV-based advance rates for VC-heavy collateral pools need an extra haircut.

**B14. [Valuing Private Equity Investments Strip by Strip](https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop)**
- **Record:** Arpit Gupta et al. · 2021 · *The Journal of Finance* · 24 citations · DOI 10.1111/jofi.13073. In dossier: no (cited in streams 04 and 08).
- **Finding:** The method replicates PE cash flows with listed equity and fixed-income strips and values them with a flexible asset-pricing model.
  - It produces a risk-adjusted profit for each investment and a time series of expected returns.
  - The average fund's risk-adjusted profit is negative in most PE categories.
  - Performance varies widely across funds and persists.
- **Relevance to ADIC:** This makes the dossier's "common pricing kernel" for value cost per dollar $c_k$ (§2.1) operational and fixes verifier issue R13.
  - [Inference] Value the give-up streams $G^k$ of sales, NAV loans, preferred equity and CFOs under the same strip kernel so the MCL rungs are comparable.

**B15. [Risk and Expected Returns of Private Equity Investments: Evidence Based on Market Prices](https://consensus.app/papers/details/0e0c66f44a5d50b99383e02fcaf6e5a0/?utm_source=claude_desktop)**
- **Record:** Narasimhan Jegadeesh et al. · 2015 · *Review of Financial Studies* · 88 citations · DOI 10.1093/rfs/hhv046. In dossier: no (stream 04 cites it).
- **Finding:** Prices of listed funds of funds and listed PE vehicles imply three things:
  - Expected abnormal returns for unlisted funds of −0.5% to 2% a year.
  - A market beta close to 1, with a positive SMB loading.
  - More systematic risk than NAV-based indices show.
- **Relevance to ADIC:**
  - It gives the MKT member of the belief set $\mathcal B_i$ an anchor.
  - It also gives the price index a high-frequency observable.
  - [Inference] When strategy-group forecasts imply alphas far above this anchor, the belief-gap flag should fire.

### 3.3 Fund finance and securitization (B16–B19)

**B16. [Distorting Private Equity Performance: The Rise of Fund Debt](https://consensus.app/papers/details/84b7e9e9b66151e78637a4ebfac077ae/?utm_source=claude_desktop)**
- **Record:** James F. Albertus et al. · 2020 · SSRN · 4 citations · DOI 10.2139/ssrn.3410076. In dossier: no.
  - Consensus also lists [Private Equity Fund Debt: Agency Costs and Cash Flow Management](https://consensus.app/papers/details/d658bfc490c45ecf9e5985e72653204e/?utm_source=claude_desktop) (Albertus et al., 2026, *JFQA*, DOI 10.1017/s0022109026102890), with no abstract.
  - [Inference] The JFQA paper is likely the published successor.
- **Finding:** Funds that use subscription lines:
  - call less capital;
  - show large distortions in measures sensitive to cash-flow timing;
  - are disproportionately poor performers;
  - earn more carried interest, both because more funds earn carry and because each earns more.
- **Relevance to ADIC:** This gives academic backing to the dossier's ILPA-based §3.2(8) and to judging funds on unlevered IRR or PME.
  - [Inference] Make subscription-line use a per-fund state.
  - It should shift the call-timing model and lower the credibility of IRR-based GP forecasts ($y^{SG}$).

**B17. [MODELING PRIVATE EQUITY FUNDS AND PRIVATE EQUITY COLLATERALISED FUND OBLIGATIONS](https://consensus.app/papers/details/d37c8dac4aa651048a5f3a5f42bec38a/?utm_source=claude_desktop)**
- **Record:** Etienne de Malherbe · 2004 · *International Journal of Theoretical and Applied Finance* · 24 citations · DOI 10.1142/s0219024904002359. In dossier: no (stream 04 mentions it via a secondary description).
- **Finding:** For securitizations of PE funds of funds, the paper models funds in three stages:
  - drawdowns;
  - investment value, as a lognormal process;
  - repayments.

  Drawdown and repayment rates follow squared Bessel processes.
- **Relevance to ADIC:** This is a stochastic cash-flow model suited to CFO tranche analysis (§3.2(7)): cash-trap tests, LTV triggers and PIK.
  - [Inference] Use it, or the stream-04 regime-switching Takahashi–Alexander (RFT-TA) engine, to simulate note coverage on an Astrea-style structure by regime.

**B18. [Beyond the Blind Pool: How Private Asset-backed Structured Products Reshape Risk and Return](https://consensus.app/papers/details/a0b201dfd115568d865c33cce497d4f1/?utm_source=claude_desktop)**
- **Record:** Alex Billias et al. · 2026 · SSRN · 0 citations · DOI 10.2139/ssrn.6433038. In dossier: no.
- **Finding:** The paper treats CFOs as a way to turn private-asset portfolios into securities with distinct risk-return profiles. It analyzes diversification, tranching, cash-flow timing and regulatory capital, and sets out the products' limitations.
- **Relevance to ADIC:**
  - [Inference] This recent framework is a checklist for the Capital Solutions group's CFO work.
  - It also helps with the dossier's open question 4: whether ADIC should sponsor an Astrea-like vehicle.

**B19. [The Economics of Structured Finance (*Journal of Economic Perspectives* 23(1):3–25)](https://consensus.app/papers/details/89f1ef7a5962598bb7ec8c607c0eee2a/?utm_source=claude_desktop)**
- **Record:** Consensus shows no authors ("N/A") and a title string that begins "Journal of Economic Perspectives—Volume 23, Number 1—Winter 2009". 472 citations; no DOI shown.
  - The JEP article is by Coval, Jurek and Stafford. That attribution is general knowledge; the Consensus record does not confirm it.
  - In dossier: no.
- **Finding:**
  - Senior tranches are much safer than the average collateral only if rating agencies estimate default risk and correlation precisely.
  - Issuing a capital structure amplifies errors in evaluating the underlying risk.
- **Relevance to ADIC:** This challenges the dossier's treatment of CFO senior notes as a cheap, stable rung.
  - [Inference] Ratings on PE-equity collateral are sensitive to the correlation of fund NAVs, which rises in crises.
  - Add rating-migration and model-risk haircuts to CFO capacity and pricing by regime.

### 3.4 Fire sales, adverse selection and funding liquidity (B20–B25)

**B20. [Fire Sales in Finance and Macroeconomics](https://consensus.app/papers/details/38094184238d5f8f9fe8944a05e37411/?utm_source=claude_desktop)**
- **Record:** A. Shleifer et al. · 2011 · *Journal of Economic Perspectives* · 700 citations · DOI 10.1257/jep.25.1.29. In dossier: no (stream 08 cites it).
- **Finding:** Fire sales are forced sales in which high-valuation bidders are sidelined, usually because debt overhang hits many specialist bidders at once. They cause undervaluation, downward spirals and failed arbitrage.
- **Relevance to ADIC:** This is the theory behind the dossier's "cash-in-the-market" crisis anchor.
  - [Inference] Model secondary-market depth from specialist buyers' balance sheets: leverage, dry powder and evergreen redemptions.
  - Do not use the overhang ratio, which the verifier showed is inverted (R1).

**B21. [Market liquidity and funding liquidity](https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop)**
- **Record:** M. Brunnermeier et al. · 2009 · *Review of Financial Studies* · 5,153 citations · DOI 10.1093/rfs/hhn098. In dossier: no (cited in streams 06 and 08).
- **Finding:** Traders' funding (capital and margins) depends on market liquidity, and market liquidity depends on their funding. Margins can destabilize and create liquidity spirals. Liquidity dries up suddenly, moves together across securities and with volatility, and flees to quality.
- **Relevance to ADIC:** This formalizes the dossier's view of a NAV facility as a private margin call (§2.4).
  - [Inference] Simulate NAV-loan advance rates, CFO LTV tests and secondary prices jointly, as functions of volatility and market illiquidity.
  - Covenant-breach probabilities computed with fixed haircuts are biased low.

**B22. [Margin-Based Asset Pricing and Deviations from the Law of One Price](https://consensus.app/papers/details/c5d81d132abf5d118a3a62c20200c195/?utm_source=claude_desktop)**
- **Record:** Nicolae Gârleanu et al. · 2011 · Consensus venue "NBER", but the DOI is an RFS DOI · 663 citations · DOI 10.1093/rfs/hhr027. In dossier: no (backfilled in literature file 01).
- **Finding:**
  - When agents face margin constraints, required returns depend on both beta and margin.
  - In funding crises a basis opens between securities with identical cash flows but different margins.
  - The spread between collateralized and uncollateralized loans captures the shadow cost of capital.
- **Relevance to ADIC:**
  - [Inference] This gives Corporate Finance an observable check on the optimizer's λ, which is its transfer-pricing curve: compare λ with the spread between ADIC's secured funding (NAV facility, CFO) and its unsecured funding.
  - It also explains why assets with high advance rates should be pledged first.

**B23. [Fear of Fire Sales, Illiquidity Seeking, and Credit Freezes](https://consensus.app/papers/details/a6c668ff8cfe5396bed107c465c18632/?utm_source=claude_desktop)**
- **Record:** Douglas W. Diamond et al. · 2011 · *Quarterly Journal of Economics* · 571 citations · DOI 10.1093/qje/qjr012. In dossier: no.
- **Finding:** An overhang of institutions that may be forced to sell later raises the private return to holding illiquid assets. Cash-rich buyers who expect fire sales earn high expected returns on cash, so they lock up less in term loans.
- **Relevance to ADIC:**
  - [Inference] This formally backs context implication 5, that dry powder has option value. Value the Secondaries and Capital Solutions groups' crisis buying capacity as an option, and size Corporate Finance's buffer with that in mind.
  - The same mechanism lowers other buyers' bids for ADIC's assets in a crisis.

**B24. [The Information in Asset Fire Sales](https://consensus.app/papers/details/26c33fcf27c25a34a7c10c36644285a0/?utm_source=claude_desktop)**
- **Record:** Sheng Huang et al. · 2022 · *Management Science* · 19 citations · DOI 10.1287/mnsc.2022.4585. In dossier: no.
- **Finding:** In mutual-fund fire sales:
  - Discretionary trades carry fundamental information and expected (pro-rata) trades do not.
  - Other traders cannot tell the two apart.

  This explains why fire-sale discounts are large and persistent.
- **Relevance to ADIC:**
  - [Inference] This is evidence for the dossier's strip and pro-rata sale formats. Cherry-picked portfolios invite a lemons discount.
  - In the MCL, apply an adverse-selection markup to discretionary tranches and a smaller one to strips.

**B25. [The Dark Side of Liquid Bonds in Fire Sales](https://consensus.app/papers/details/52bf617f88795c2cba5f577f1bb26cb2/?utm_source=claude_desktop)**
- **Record:** Maria Chaderina et al. · 2026 · *Management Science* · 11 citations · DOI 10.1287/mnsc.2023.03670. In dossier: no.
- **Finding:** Selling the most liquid bonds first can backfire. When many investors sell the same liquid, widely held bonds while buying capital is scarce, those bonds fall the most. The evidence comes from P&C insurers after natural catastrophes.
- **Relevance to ADIC:** This challenges a fixed pecking order that sells quality-buyout LP interests first in a crisis.
  - [Inference] If peer sovereign funds and pensions sell the same widely held funds, that rung becomes crowded.
  - Add a crowding term to the price-impact function.

---

## 4. Missed-but-important papers: design implications

All items are **[Inference]** unless a sentence is a direct paraphrase of a cited abstract. Owners follow the organization confirmed by the user:
- groups own asset-level SELL / HOLD / REFINANCE / LEVER proposals;
- Corporate Finance owns Treasury, portfolio-level facilities and λ.

### 4.1 State variables

| State (new or changed) | Description | Literature basis | Owner |
|---|---|---|---|
| $\mu^{dr}_t$, $\mu^{liq}_{s_t}$ | Split the regime term of the price equation into a discount-rate component and a buyer-liquidity component. | B2, B3 | Secondaries group (market intelligence) |
| $y^{LPE}_t$ | Weekly listed-PE NAV discount, an extra observation equation for the Kalman price index (§3.3). | F12, B15, F13 | Secondaries group |
| $\hat V_{i,t}$, $\hat\beta_i$, $\hat\sigma_i$ | Weekly nowcast value, beta and total volatility for each interest. Replaces the simple beta-and-lag de-smoothing. | B12 | PE group / risk (stream-04 engine) |
| $q^{NAV}_i$ | NAV-quality score built from three inputs: strategy (VC bias); a fundraising-window flag for low performers; and the manager's persistent reporting quality. It feeds the hedonic price, NAV advance rates and belief credibility. | B13, F10, F11, B12 | PE group; NAV-quality agent |
| $\pi^U_{s}$ | A separate, possibly negative, price for unfunded commitments: $P_i=\pi^{NAV}_i\hat V_i-\pi^U_s U_i$. | B9, F9, B8 | Secondaries group |
| $n^{bid}_{i,t}$, buyer mix | Expected bidder count and share of non-traditional buyers per interest. | B4, B3 | Secondaries group |
| $\tau_i$ | Tax and structure class of the interest, and how well it matches taxable buyers. | B10 | Secondaries group / legal |
| $sl_i$ | Whether the fund uses a subscription line, and its size. | B16, F15, F16 | PE group |
| $K^{spec}_t$, $K^{ever}_t$, $gate_t$ | Specialist buyer capital, and evergreen capacity with a gate and redemption state. Replaces the overhang classifier flagged by the verifier (R1). | B20, F6, F26, F27 | Secondaries group → Corporate Finance |
| $\chi_i$ | Crowding score: overlap of interest $i$ with likely peer sellers' holdings. | B25 | Secondaries group |

### 4.2 Models

1. **Extended price equation.** This replaces dossier §6.5 [Inference]:
   $$\pi_{i,t}=\frac{\hat V_{i,t}}{NAV^{ref}_i}\exp\!\big(\mu^{liq}_{s_t}+\mu^{dr}_t+\beta^\top f_i-\kappa_s\,q_t/\text{Depth}_t-\psi\,AS_i-\phi\,\chi_i+\varepsilon_i\big)$$
   - $f_i$ adds three features: tax class (B10), NAV quality (B13, F10) and bidder-count drivers (B4).
   - $AS_i$ marks discretionary versus pro-rata selection (B24).
   - $\chi_i$ is crowding (B25).
   - Unfunded commitments are priced separately, as in 4.1.
   - Use a single functional form; the verifier found the dossier switches between two (R14).
2. **Joint price and execution model.** Better assets trade at higher prices but in less liquid markets: their sellers accept a lower chance of trading (F5).
   - Model $p_i(r)=\Pr(\text{sale}\mid \text{reserve }r, s_t, n^{bid}_i)$ jointly with $\mathbb E[\pi\mid\text{sale}]$, instead of using fixed $p_j$ values.
   - This also responds to verifier R2.
   - Estimate it from bid data with a selection correction (Heckman 1979). It needs an explicit exclusion restriction and sensitivity bounds, because selection models are fragile (F23). Candidate instruments are process-level variables such as advisor-run versus bilateral sales and the GP-consent regime [Inference].
3. **Common pricing kernel.** Compute $PV_m(G^k)$ for every instrument with strip replication (B14).
   - Report $c_k$ under at least two kernels as a robustness check. A survey of the risk-adjustment literature finds that estimates vary substantially with method, period and data (F14).
4. **Coupled liquidity spiral for NAV facilities.** Make the advance rate depend on the state: $\ell^{max}_t=\ell_0\,h(\hat\sigma_t,\text{ILLIQ}_t)$.
   - $\hat\sigma$ comes from B12 and ILLIQ from the price index.
   - Simulate it jointly with secondary prices (B21), and evaluate the covenant chance constraint on these paths.
   - This also fixes the fixed-haircut weakness in dossier §3.2(4).
5. **CFO tranche simulator.** Drive pool cash flows with B17 or the stream-04 RFT-TA engine and stress correlation explicitly.
   - Senior safety depends on correlation (B19).
   - Concentrated collateral produced more defaults and downgrades, and the concentration was not priced (F18).
   - Confidence intervals on CFO default probabilities are wide (F19).
   - Track rating migrations and cash-trap triggers. Analogy: CLO equity proved resilient because of its long-term funding (F17). That supports long-dated CFO funding over LTV-triggered NAV facilities [Inference].
6. **Sell-or-wait.** Keep the dossier's least-squares Monte Carlo design (Longstaff & Schwartz 2001; convergence results in F22).
   - Add the duality upper bound (F21) as a rubric check on policy quality.
   - Real-options theory shows the hurdle can be large; F20 reports waiting until benefits reach twice the cost for reasonable parameters. This replaces the "Irrev" proxy, as the verifier recommends (R8).
7. **Forced-sale hazard.** F8 models surprise liquidity shocks that force sales at a stochastic discount, which matches the dossier's lattice assumption.
   - [Inference] For ADIC the hazard should be endogenous to its own liquidity state: payout, calls and margin. Do not use an exogenous Poisson rate.

### 4.3 Parameters and calibration priors (literature values, not ADIC data)

| Parameter | Literature value | Source | Use in framework | Caveat |
|---|---|---|---|---|
| Buyer–seller return gap | about 5 pp a year (PME) | B1 | Prior for the liquidity-transfer component | Sample average, not seller-specific |
| Fund beta and total volatility | buyout β≈1.0, σ≈33%; VC β≈1.4, σ≈40% | B12 (SSRN abstract) | NAV paths for covenants and CFO tests | RFS numbers may differ (stream-07 verifier) |
| Market-implied PE abnormal return | −0.5% to +2% a year | B15 | MKT anchor in the belief set | Listed-vehicle sample |
| Listed-PE beta and alpha | β≈1.5, no significant alpha | F13 | Cross-check on de-smoothed risk | New, uncited work (2026) |
| Listed-PE NAV discount | starts at −2.5%, settles at about −21% after two years | F12 | Offset in the price-index observation equation | Listed funds, not LP interests |
| Liquidity risk premium | about 3% a year | F7 | Illiquidity premium in the hold value | Factor-model dependent |
| Distressed block-sale discount | about 8%; 13–14% for stakes above 5% or sold as a block; prices recover | F2 | Cross-asset prior for κ and for recovery half-life | Listed minority stakes |
| Unlisted-asset sale discount | 15–30%; larger when the seller is constrained and debt is expensive | F1 | Supports co-moving SELL and REFINANCE costs by regime | M&A setting |
| Real-option waiting hurdle | up to about 2x benefits/cost in simulations | F20 | Illustrates irreversibility; sanity check on the sell-or-wait policy | Not directly transferable |
| Legacy-LP cash-out in CVs | about 80–90% sell | F25 | Default election prior (consistent with dossier's 14–17% rollover) | Practitioner-sourced report |
| Subscription-line effects | intermediate IRRs strongly affected; MOICs weakly | F16 | Judge belief gaps on MOIC or PME, not interim IRR | Simulation study |

### 4.4 Constraints

1. **Covenant chance constraint with endogenous haircuts** (B21, B22). Evaluate $\Pr(\ell_{k,t}\ge\ell^{trig})\le\alpha_{cov}$ on paths where both advance rates and prices tighten in stress.
   - [Inference] This also supports giving committed facilities a 100% haircut in the 30-day bucket, which resolves the inconsistency flagged by the verifier (R10).
2. **Visibility and predictability limit on sale programmes** (F3, F4).
   - Predictable forced trades get front-run, and a known distressed seller gets less.
   - Cap the volume that is pre-announced or visible per semester.
   - Wall off ADIC's sale calendar from counterparties.
3. **Adverse-selection cap on cherry-picking** (B24, F5). Limit the share of discretionary (non-pro-rata) selections, or charge a lemons markup for them, when adverse selection is high.
4. **Crowding cap** (B25): $\sum_i x_i\hat V_i\chi_i\le C^{crowd}_{s}$, tightened in stress regimes.
5. **Depth haircut tied to evergreen buyers** (F26, F27, B20).
   - Redemption gates exacerbated runs in money-market funds (F26).
   - In open-end private real-estate funds, queues limit fragility, but liquidity buffers amplify it when added to queues (F27).
   - [Inference] Cut $K^{ever}$ when evergreen gates bind; this addresses verifier R9.
6. **Commitment resizing as a first-class lever** (B8, F29, F35).
   - Timing commitments yields modest gains at best, because investors cannot time calls or exits (F29).
   - Suspending new commitments can rebalance without forced sales (F35).
   - Count pacing cuts toward the 6–24-month buckets only. Price "unfunded shed" explicitly, using B8 and B9.

### 4.5 Objectives and shadow prices

- **One kernel, one place.** Liquidity costs should enter only through simulated cash flows valued under the strip kernel (B14). This fixes the double counting the verifier found (R3).
  - Keep separate penalties only for what cash flows miss: the signalling and access cost, which B7 grounds in theory.
- **An external check on λ.**
  - Corporate Finance's transfer-pricing curve should stay within a band of observed secured-minus-unsecured spreads (B22).
  - If the optimizer's dual drifts outside that band, refer it to the Treasurer seat.
- **Value of dry powder.**
  - Expected returns to holding cash rise when fire sales are anticipated (B23).
  - Discounts widen when sellers are constrained and debt is expensive (F1).
  - So capacity earmarked for crisis buying by the Secondaries and Capital Solutions groups has a positive, state-dependent shadow value, and Corporate Finance should not release it for free.
  - Counterweight: buyers under pressure to spend underperform (F33), so deployment discipline is part of the option.
- **Relationship cost.**
  - Theory supports a signalling cost (B7).
  - The evidence on persistence suggests access value is smaller and noisier than often assumed (F30, F31, F32). Use these as priors when eliciting the PE team's access-loss probabilities (dossier open question 5).

### 4.6 Agent and IC design

- **Secondary Price Index agent** (extends the dossier's Librarian).
  - Ingests listed-PE discounts weekly, advisor reports semi-annually and any transaction-based index.
  - Each month, decomposes index moves into $\mu^{dr}$ (B2) and $\mu^{liq}$ (B3), and shows which drove the change.
- **NAV-quality agent.**
  - Flags interests by strategy bias (B13).
  - Flags fundraising-window marks from low performers (F10, F11).
  - Tracks each manager's persistent reporting quality (B12).
  - Its flags gate both hedonic pricing and NAV-facility advance rates.
- **Conflict-of-interest guard.**
  - Applies when the Secondaries group (a hybrid buyer) or Capital Solutions quotes on ADIC's own SELL or REFINANCE.
  - The CV literature describes the GP's conflict from sitting on both sides, and a competitive bidding process as the remedy (F25).
  - Require external price discovery for any intra-ADIC transfer, and count such transfers as zero liquidity raised (context implication 1).
- **Red-team scenario set.**
  1. A liquidity spiral, impaired specialist buyers and binding evergreen gates (B21, B20, F26).
  2. Crowded selling by peer sovereign funds of the same fund names (B25).
  3. A CFO correlation shock with rating migration (B19, F18).
  4. A short crisis with fast recovery, as in 2009 (B11), to test the value of waiting.
- **IC Action Economics Card: new fields.**
  - Value of the commitment liability shed (B8, B9).
  - Kernel-based $c_k$ under two kernels (B14, F14).
  - The discount split into discount-rate and liquidity parts (B2, B3).
  - Lemons markup (B24).
  - Crowding score (B25).
  - NAV-quality flag (B13).
  - Market-implied return anchor (B15).
  - Tax-class discount (B10).

### 4.7 Further missed papers (compact)

| # | Paper | Record (Consensus) | Finding (abstract) | Use in framework |
|---|---|---|---|---|
| F1 | [The price of corporate liquidity: Acquisition discounts for unlisted targets](https://consensus.app/papers/details/6f3ed8f7e26c50d29022453169f85362/?utm_source=claude_desktop) | Micah S. Officer · 2007 · *JFE* · 457 cit. · DOI 10.1016/j.jfineco.2006.01.004 | Unlisted targets sell at 15–30% acquisition discounts; discounts are larger when parents are liquidity-constrained and debt is expensive | SELL and REFINANCE costs move together by regime; don't treat rungs as diversifying |
| F2 | [Fire sale discount: Evidence from the sale of minority equity stakes](https://consensus.app/papers/details/ee77045e07675a659c38a6f8264d43a1/?utm_source=claude_desktop) | Serdar Dinç et al. · 2017 · *JFE* · 17 cit. · DOI 10.2139/ssrn.2627404 | Distressed-sale discount about 8%; 13–14% for stakes above 5% or sold as a block; prices recover | Block-size price impact; recovery half-life |
| F3 | [Asset Fire Sales (and Purchases) in Equity Markets](https://consensus.app/papers/details/188208bed13350bfaf3135a3e7d0ecff/?utm_source=claude_desktop) | Joshua D. Coval et al. · 2007 · *JFE* · 1,514 cit. · DOI 10.2139/ssrn.718201 | Forced sales are costly; liquidity providers earn significant returns; predictable flow-driven trades invite front-running | Confidentiality of sale programmes |
| F4 | [Predatory Trading](https://consensus.app/papers/details/aad99f81cafa5c229eb30095c0affe39/?utm_source=claude_desktop) | M. Brunnermeier et al. · 2005 · *JF* DOI 10.1111/j.1540-6261.2005.00781.x · 27 cit. (a 2003 WP record shows 603) | When one trader must sell, others sell and buy back, so prices overshoot and the distressed seller gets less; markets are illiquid when liquidity is most needed | Hide covenant stress; avoid visible distress |
| F5 | [Dynamic Adverse Selection: A Theory of Illiquidity, Fire Sales, and Flight to Quality](https://consensus.app/papers/details/1b0262aa82f6534fb36a9d203ff9ac70/?utm_source=claude_desktop) | Veronica Guerrieri et al. · 2014 · *AER* · 237 cit. · DOI 10.1257/aer.104.7.1875 | Better assets trade at higher prices in less liquid markets; high-quality sellers accept lower trading probability | Joint reserve-price and execution-probability frontier |
| F6 | [The Paradox of Financial Fire Sales: The Role of Arbitrage Capital in Determining Liquidity](https://consensus.app/papers/details/3609684b074f5b77b3cdb79a7a904d82/?utm_source=claude_desktop) | James Dow et al. · 2018 · *JF* · 36 cit. · DOI 10.1111/jofi.12584 | When specialists are liquidity-constrained, prices lose information, adverse selection rises and non-specialist capital withdraws | Depth multiplier beyond dedicated capital |
| F7 | [Private Equity Performance and Liquidity Risk](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop) | Francesco Franzoni et al. · 2012 · *JF* · 251 cit. · DOI 10.1111/j.1540-6261.2012.01788.x | PE loads on the liquidity risk factor; premium about 3% a year; works through a funding-liquidity channel (cited in stream 04) | Hold value and the correlation of secondary prices with funding stress |
| F8 | [Equilibrium Liquidity Premia of Private Equity Funds](https://consensus.app/papers/details/b0e4b7258dc2593ca346fa7fab2cc1c1/?utm_source=claude_desktop) | A. Buchner · 2016 · *J. Risk Finance* · 1 cit. · DOI 10.2139/ssrn.2549694 | Surprise liquidity shocks force secondary sales at a stochastic discount; derives equilibrium liquidity premia | Forced-sale hazard structure (make it endogenous for ADIC) |
| F9 | [Hidden in Plain Sight—The Impact of Undrawn Commitments](https://consensus.app/papers/details/d99e5eff8f48558898b24269df59ba18/?utm_source=claude_desktop) | T. Meyer · 2020 · DOI 10.3905/jai.2020.1.101 · 2 cit. | Uncalled capital carries risk and opportunity cost and is priced through larger secondary discounts and subscription lines; model it as a loan against the fund | Unfunded price $\pi^U$ |
| F10 | [Do private equity funds manipulate reported returns?](https://consensus.app/papers/details/3331159853ab59dea783df670c91ee0a/?utm_source=claude_desktop) | Gregory W. Brown et al. · 2019 · *JFE* · 90 cit. · DOI 10.3386/w22493 | Some under-performers boost reported returns during fundraising; top performers likely understate | NAV-quality flag; reference-NAV reliability |
| F11 | [Interim Fund Performance and Fundraising in Private Equity](https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop) | Brad M. Barber et al. · 2017 · *JFE* · 113 cit. · DOI 10.1016/j.jfineco.2017.01.001 | GPs time fundraising to performance peaks; low-reputation GPs show NAV management | NAV-quality flag |
| F12 | [Net asset value discounts in listed private equity funds](https://consensus.app/papers/details/efbe3a9efab257cdb2bd314bdf29d186/?utm_source=claude_desktop) | Henry Lahr et al. · 2010 · DOI 10.2139/ssrn.1494246 · 8 cit. | Discounts settle at about −21% after two years; premia predict returns and depend on liquidity, sentiment, credit markets and systematic risk | Observation equation for the price index |
| F13 | [Buyout Performance with Assets Valued at Market](https://consensus.app/papers/details/3acac11a0e225ab8b04a38002b7e440d/?utm_source=claude_desktop) | Richard M. Ennis et al. · 2026 · DOI 10.3905/jpmi.2026.011 · 0 cit. | Market-priced listed-PE risk exceeds NAV-based risk; β≈1.5, no significant alpha; consistent with secondary-transaction studies | Belief-gap anchor; de-smoothing check |
| F14 | [Risk Adjustment in Private Equity Returns](https://consensus.app/papers/details/996d0a57b17957dd81fec3ac0698ec30/?utm_source=claude_desktop) | Arthur Korteweg · 2019 · *Annual Review of Financial Economics* · 37 cit. · DOI 10.2139/ssrn.3293984 | Survey: risk-adjusted estimates vary substantially by method, period and data; VC net returns zero or negative since 2000 | Kernel-robustness requirement |
| F15 | [Distortion or Cash Flow Management? Understanding Credit Facilities in Private Equity Funds](https://consensus.app/papers/details/607b6f3085c653fca914c18d18b14c3e/?utm_source=claude_desktop) | Pierre Schillinger et al. · 2019 · SSRN · 1 cit. · DOI 10.2139/ssrn.3434112 | Standard subscription lines have moderate effects; extensive use can substantially raise time-sensitive returns and alter rankings | Subscription-line state $sl_i$ |
| F16 | [Unpacking Private Equity Performance](https://consensus.app/papers/details/911bba796e2a56e5924f1563664ff4b4/?utm_source=claude_desktop) | Gregory W. Brown et al. · 2024 · DOI 10.2139/ssrn.4656457 · 0 cit. | Interim IRRs strongly affected by subscription lines and pacing; MOICs weakly by lines; recycling accounting matters | Use MOIC or PME for belief comparisons |
| F17 | [CLO Performance](https://consensus.app/papers/details/c712f36af0415b9488a4a6e63c8facb8/?utm_source=claude_desktop) | Larry Cordell et al. · 2020 · Philadelphia Fed WP · 17 cit. · DOI 10.2139/ssrn.3652124 | CLOs add value by easing regulatory constraints; equity resilient to volatility because of long-term funding | Analogy supporting long-dated CFO funding |
| F18 | [Correlated Collateral](https://consensus.app/papers/details/b9e7fb5f00b15112a3d6e2d05b5bda77/?utm_source=claude_desktop) | Taylor D. Nadauld et al. · 2010 · DOI 10.2139/ssrn.1573042 · 3 cit. | Concentrated (correlated) collateral produced more defaults and downgrades; concentration not priced | CFO correlation stress |
| F19 | [Correlation Breakdown in the Valuation of Collateralized Fund Obligation](https://consensus.app/papers/details/0388804773bd5109a600293f90766779/?utm_source=claude_desktop) | Unai Ansejo et al. · 2006 · DOI 10.3905/jai.2006.670101 · 3 cit. | Low transparency makes confidence intervals on CFO default probabilities and spreads wide | CFO model-risk haircut |
| F20 | [The Value of Waiting to Invest](https://consensus.app/papers/details/b10fe378894f50539e6bbe12f00fbade/?utm_source=claude_desktop) | Robert Mcdonald et al. · 1986 · *QJE* · 3,935 cit. · DOI 10.2307/1884175 | Option value of waiting can be large; may wait until benefits reach twice the cost | Sell-or-wait hurdle sanity check |
| F21 | [Pricing American Options: A Duality Approach](https://consensus.app/papers/details/2f8e256edd7050af8d5956da33471254/?utm_source=claude_desktop) | Martin B. Haugh et al. · record year 2018 · *Oper. Res.* · 482 cit. · DOI 10.1287/opre.1030.0070 | Upper and lower price bounds from any approximation; tight when the approximation is good | Rubric bound on the least-squares Monte Carlo sell-or-wait policy |
| F22 | [Convergence of the Least Squares Monte Carlo Approach to American Option Valuation](https://consensus.app/papers/details/9c2adc2799ed525dac7a05cdcd54bceb/?utm_source=claude_desktop) | L. Stentoft · 2004 · *Manag. Sci.* · 205 cit. · DOI 10.1287/mnsc.1030.0155 | Least-squares Monte Carlo approximations converge in multi-period, multi-dimensional settings | Justifies least-squares Monte Carlo on regime paths |
| F23 | [Selection models in accounting research](https://consensus.app/papers/details/3ccacfe25c36504484eacfd6aa6e6ac9/?utm_source=claude_desktop) | C. Lennox et al. · 2012 · *Accounting Review* · 1,312 cit. · DOI 10.2308/accr-10195 | Selection models are fragile and can give almost any result after minor specification changes | Exclusion restriction plus sensitivity analysis for failed-process correction |
| F24 | [The Secondary Market](https://consensus.app/papers/details/cdb9a9ebe1a25ea0bfddb958fb777405/?utm_source=claude_desktop) | P. Cornelius et al. · 2012 · book chapter · 4 cit. · DOI 10.1002/9781119208143.ch6 | The secondary market "should not be perceived as a game changer" in risk management; distressed sellers accept substantial discounts | Crisis MCL should rely little on sales |
| F25 | [Continuation Funds: Ethics in Private Markets, Part I](https://consensus.app/papers/details/23aed12e6aa650ac9d160c9cf1c5ed5a/?utm_source=claude_desktop) | Stephen Deane et al. · 2025 · CFA Institute (DOI 10.56227/25.1.29) · 0 cit. | GP sits on both sides; about 80–90% of legacy investors cash out; a fair competitive bidding process addresses conflicts; evergreen funds affect CVs and secondaries | CV election defaults; conflict guard |
| F26 | [Liquidity Restrictions, Runs, and Central Bank Interventions: Evidence from Money Market Funds](https://consensus.app/papers/details/389740373ccf5208b969643b471e31ae/?utm_source=claude_desktop) | Lei Li et al. · 2021 · *RFS* · 79 cit. · DOI 10.1093/rfs/hhab065 | Gates and fees exacerbated the 2020 money-market fund run through strategic complementarities | Analogy: evergreen gates shrink buyer capacity in stress |
| F27 | [Liquidity transformation risks and stabilization tools: Evidence from open-end private equity real estate funds](https://consensus.app/papers/details/abc2df60ee515faa8f6cf53c880555a8/?utm_source=claude_desktop) | Spencer J. Couts · 2025 · *Real Estate Economics* · 2 cit. · DOI 10.1111/1540-6229.12532 | Stale NAVs invite NAV-timing; queues protect; buffers amplify fragility when added to queues | Evergreen-buyer fragility state |
| F28 | [Valuing Private Equity](https://consensus.app/papers/details/15cb135a45b35616b82e97bf090f24ae/?utm_source=claude_desktop) | M. Sørensen et al. · 2013 record · *RFS* · 110 cit. · DOI 10.1093/rfs/hhu013 | Fees, carry and illiquidity are costly; LPs may only break even net of all of them | Lower the hold value used in sale-cost IRRs |
| F29 | [Can investors time their exposure to private equity?](https://consensus.app/papers/details/b5880343ab7b57ebaf68b353dfff48da/?utm_source=claude_desktop) | Gregory W. Brown et al. · 2020 · *JFE* · 30 cit. · DOI 10.1016/j.jfineco.2020.08.014 | Modest gains at best from timing commitments; calls and exits cannot be timed | Pacing cuts have slow, limited cash effects |
| F30 | [Skill and Luck in Private Equity Performance](https://consensus.app/papers/details/a0bf5a58fd485ea895fabd5c39cb76ce/?utm_source=claude_desktop) | Arthur Korteweg et al. · 2017 · *JFE* · 150 cit. · DOI 10.1016/j.jfineco.2017.03.006 | High long-term persistence (7–8 pp quartile spread) but little investable persistence | Prior for GP-access value |
| F31 | [How Persistent is Private Equity Performance? Evidence from Deal-Level Data](https://consensus.app/papers/details/00af5930c4c75ef99ef2ac1654c52789/?utm_source=claude_desktop) | Reiner Braun et al. · 2017 · *JFE* · 127 cit. · DOI 10.2139/ssrn.2314400 | Buyout manager persistence has substantially declined as the industry matured | Prior for GP-access value |
| F32 | [Limited Partner Performance and the Maturing of the Private Equity Industry](https://consensus.app/papers/details/f4aeacf09dae5b4c9e87522d93f16191/?utm_source=claude_desktop) | Berk A. Sensoy et al. · 2014 · *JFE* · 134 cit. · DOI 10.2139/ssrn.2212190 | Endowments' 1991–98 edge came from access to top VC; after 1999 no access or selection edge | Prior for GP-access value |
| F33 | [On Secondary Buyouts](https://consensus.app/papers/details/7bf7597e234759c785c4d2057d100202/?utm_source=claude_desktop) | François Degeorge et al. · 2016 · *JFE* · 91 cit. · DOI 10.2139/ssrn.2329202 | Secondary buyouts made by buyers under pressure to spend underperform; without pressure they perform like other buyouts | Deployment discipline for the Secondaries group's CV and direct deals |
| F34 | [A Latent Factor Cash Flow Model for Alternative Investment Funds](https://consensus.app/papers/details/bb74f63a8fc15983a1e7753d4057d4f0/?utm_source=claude_desktop) | Wenbo Cao et al. · 2025 · *FAJ* · 1 cit. · DOI 10.1080/0015198x.2025.2489923 | Takahashi–Alexander extended with systematic factors for stress testing and commitment design (cited in stream 01) | Stressed calls and distributions in liquidity released by horizon $H$ |
| F35 | [Managing Illiquidity in Open-Ended Funds with Private Asset Allocations: Challenges and Solutions](https://consensus.app/papers/details/12cd077c32a755c9bbab6ea80a91706c/?utm_source=claude_desktop) | Raul Leote de Carvalho et al. · 2026 · DOI 10.3905/jpmi.2026.002 · 0 cit. | Suspending future commitments can rebalance a portfolio without forced secondary sales | Pacing suspension as a pre-sale lever |

### 4.8 Identified but not assessable (no abstract in Consensus)

These records bear directly on the instruments, but Consensus returned no abstract, so I report no findings. Read them in full before relying on them.

| # | Record | Why it matters |
|---|---|---|
| U1 | [Net Asset Value Financing and Private Equity](https://consensus.app/papers/details/f457b903aae95a57844b6cd41904b1d7/?utm_source=claude_desktop) · Colleen M. Baker · 2024 · SSRN · DOI 10.2139/ssrn.4851709 · 1 cit. | One of very few academic treatments of NAV financing |
| U2 | [Private Equity and Net Asset Value Debt - Ticking Time Bomb or Ticking All the Right Boxes](https://consensus.app/papers/details/dfec35a563a150b0ac00b68fa35ab87d/?utm_source=claude_desktop) · B. Reddy · 2024 · SSRN · DOI 10.2139/ssrn.4838394 · 0 cit. | NAV debt risk assessment |
| U3 | [Do GPs truly present fair value? The case of continuation funds](https://consensus.app/papers/details/db39905dbfb5585d842909b4318279bc/?utm_source=claude_desktop) · Jinhyeong Jo et al. · 2026 · *J. Int. Financial Markets, Institutions and Money* · DOI 10.1016/j.intfin.2025.102265 · 1 cit. | Peer-reviewed test of CV pricing fairness; directly relevant to CV sell-or-roll decisions |
| U4 | [Continuation Funds: Performance and Determinants, 2018-2022 Vintages](https://consensus.app/papers/details/7fed9c1e30af54af9c085178ada5a481/?utm_source=claude_desktop) · Oliver Gottschalg · 2024 · SSRN · DOI 10.2139/ssrn.4752652 · 0 cit. | CV performance; possible source of the dossier's "HEC" attribution [Inference] |
| U5 | [Collateralized Fund Obligations: A Liquidity Solution for Private Equity](https://consensus.app/papers/details/b729a0a107fc586b91a375dcb370076f/?utm_source=claude_desktop) · Hoku Eggertsen · 2025 · SSRN · DOI 10.2139/ssrn.5229406 · 0 cit. | CFO as a liquidity tool |
| U6 | [Subscription Lines of Credit and Fund Performance in Private Equity](https://consensus.app/papers/details/4a63123b02f7535dab66f36b205d2f18/?utm_source=claude_desktop) · Karan Bhanot et al. · 2025 · SSRN · DOI 10.2139/ssrn.5896663 · 0 cit. | Recent evidence on subscription-line performance distortion |
| U7 | [Private Equity Secondary Markets](https://consensus.app/papers/details/ade4a116261a53ada3ee2f9eaa6b5dea/?utm_source=claude_desktop) · Paul Mason et al. · 2023 · SSRN · DOI 10.2139/ssrn.4422541 · 3 cit. | Possibly a survey of secondary-market research |
| U8 | [To Roll or not to Roll (Forward): LP NAV Estimation for Private Equity and Real Estate](https://consensus.app/papers/details/dddd55127f665e2ba3a43181f3085db1/?utm_source=claude_desktop) · Aili Chen · 2023 · SSRN · DOI 10.2139/ssrn.4648564 · 1 cit. | Roll-forward of stale NAVs (dossier §2.2 staleness) |

---

## 5. Papers that challenge the dossier's recommendations

| # | Paper(s) | What it challenges in the dossier | Recommended change |
|---|---|---|---|
| 1 | B2 Boyer et al.; B15 Jegadeesh et al.; B14 Gupta & Van Nieuwerburgh; F28 Sørensen, Wang & Yang; F13 Ennis et al. | **§1.2, §3.2(1) and §2.2.** The dossier treats strategy-group IRR forecasts as the hold value and the residual discount as illiquidity. The market-based evidence shows that discount rates vary and that cash-flow alpha largely disappears under market-consistent risk adjustment. [Inference] The implied cost of selling quality buyout (8–15%) is therefore probably overstated, and the belief gap Δy partly reflects discount-rate risk rather than "SG optimism or private information". This is consistent with verifier R16. | Add $\mu^{dr}$ to the price equation. Compute $y_{sell}$ and $c_k$ against a kernel-based hold value. Show the market-implied return anchor on every IC card. |
| 2 | B6 Bollen & Sensoy (published abstract) | **§2.2, "required return up to 5–10 pp higher".** The published headline is that breakeven returns match observed returns for moderately risk-tolerant LPs with up to 40% in PE. | Cite 5–10 pp to the 2015 WP. Recompute the illiquidity cost at ADIC's own risk tolerance. |
| 3 | B19 *JEP* 2009; F18 Correlated Collateral; F19 Ansejo et al. | **§1.2 ladder, §4.7 "template lessons" and the §6.6 CFO row.** The dossier ranks CFO senior notes as a cheap rung and expects ratings to improve as LTV falls. Tranche ratings are highly sensitive to correlation and default-probability errors, and estimates are imprecise for opaque fund collateral. | Add correlation-stressed rating migration and a model-risk spread to CFO cost by regime. Treat Astrea-style capacity as falling or closed when correlations rise, not only in "crisis". |
| 4 | B25 Chaderina et al. | **§3.4 pecking order.** In a crisis the dossier would sell quality buyout (the most liquid rung) first. Selling liquid, widely held assets can backfire when many sellers converge and buying capital is scarce. | Add crowding $\chi_i$ to price impact and a crowding cap. Diversify crisis sales across less widely held names, or rely on financing instead. |
| 5 | B8 Gourier et al. | **§1.4–5 and §6.2 action emphasis.** The dossier includes pacing cuts (§3.1, decision variable $n_t$ in §6.2) but centres on SELL and REFINANCE, and puts no value on commitment risk itself. Investors value adjusting committed quantity more than removing tradability frictions, and commitment risk premia *rise* with secondary liquidity. | Make commitment resizing (pacing, partial unfunded sales, fund-size elections) a first-class action with its own value. Do not assume secondary depth neutralizes commitment risk. |
| 6 | F24 Cornelius et al.; B11 Hege & Nuti | **§3.4 and §6.6 crisis MCL.** The dossier still lists LP sales as a crisis rung, with execution probability 0.4–0.5. In 2009, volume collapsed to a fraction of prior levels, and the secondary market "should not be perceived as a game changer" for risk management. Hege & Nuti also report a quick recovery. | Lower crisis execution probability further, but make the crisis state short-lived. Value waiting explicitly through the least-squares Monte Carlo continuation value. |
| 7 | F23 Lennox et al. | **§7, pitfall 3 (Heckman-style correction for failed processes).** Selection models are fragile without justified exclusion restrictions. | Name the exclusion restriction (for example, process type or the GP-consent regime) and report bounds and sensitivity, not a single corrected estimate. |
| 8 | F30 Korteweg & Sørensen; F31 Braun et al.; F32 Sensoy et al. (versus B7 Lerner & Schoar) | **§6.3(6), the relationship constraint (at most two exits per GP per three years).** [Inference] Investable persistence and endowments' access edge have declined, so a hard cap may over-value access. B7 still supports a non-zero signalling cost. | Replace the hard cap with a priced access cost, elicited from the PE team using these papers as priors. |
| 9 | F26 Li et al.; F27 Couts | **§4.5, evergreen capital counted as buyer depth.** Gates and queues create run dynamics that shrink capacity in stress. Consistent with verifier R9. | Haircut $K^{ever}$ when gates or queues bind; include this in the red-team scenario. |
| 10 | F1 Officer | **§3.4, implicit independence of rung costs.** Sale discounts widen when debt is expensive and the seller is constrained. | Model SELL and REFINANCE costs as positively correlated across regimes in the MCL. |

---

## 6. Verbatim usage message

None. No Consensus result in this run contained a sign-up, upgrade or usage message.

---

## 7. Scope notes

- **Searches.**
  - **Consensus (19, one at a time, no filters):**
    - 5 citation look-ups;
    - 14 backfill searches: the five seeds, plus refinements on discount-rate risk, subscription lines, fire sales, funding liquidity, listed-PE prices, LP liquidity shocks and commitments, a second CV query, secondary-fund performance, and evergreen funds.
  - **WebSearch (4):**
    - 1 to resolve the WilmerHale title;
    - 3 to confirm published versions of Boyer et al., Gourier et al. and Brown–Ghysels–Gredil.
  - No rate-limit errors occurred.
- **What I did not do.**
  - I did not read full texts. Findings are abstract-level.
  - I did not check practitioner references against academic indexes.
  - The secondary-fund performance query (buy-side returns for the Secondaries group's fund book) did not surface secondary-fund-specific studies. That gap remains open.
- **Agreement with the verification log.** Consensus corroborates the log's F10 (Bollen–Sensoy attribution), A7 (Maurin authors) and A8 (Albuquerque existence). It adds the Albuquerque et al. abstract, which the dossier and the log lacked.
- **Record-year caveats.** Several Consensus records carry the working-paper or online year: Bollen–Sensoy 2016, Haugh–Kogan 2018, Sørensen–Wang–Yang 2013, Maurin et al. 2022. I did not treat these as mismatches.
- **Overlap with other streams.** Streams 04, 06, 07 and 08 already cite B8, B9, B12, B13, B14, B15, B20, B21 and F7. Streams 07 and G2 cite Boyer et al.'s 2018 index paper rather than B2. The orchestrator may want one canonical reference set across streams.
