# G6 literature check: Private Credit (returns, defaults, leverage)

**Dossier checked:** `research/groups/dossiers/G6_private_credit.md` (as of 2026-10-18; 20 academic works). The dossier was not edited.
**Date:** 2026-10-18.
**Companion:** `research/groups/verification/G6_private_credit.verify.md` (the "verification log", VL).

> **Blocker: Consensus, OpenAlex and Semantic Scholar were all unavailable for this run.**
> - **Consensus.** My first query (the Erel–Flanagan–Weisbach title) was rejected three times, 30 seconds apart, with the monthly-quota message in Section 6. The quota resets on 1 November 2026. Because the quota covers the whole account, I sent no further Consensus calls. **No Consensus search completed.**
> - **OpenAlex** (the substitute the G1 run used): HTTP 429. The daily free credit is exhausted (`X-RateLimit-Remaining: 0`, `Retry-After: 48357` seconds, about 13.4 hours).
> - **Semantic Scholar** public API: HTTP 429 on all four attempts.
> - **Consequence.** The only Consensus URLs in this file are records that sibling streams saved earlier today. Section 7 gives a rerun plan for after the reset.

**Fallbacks (disclosed)**
1. **Crossref REST API [CR].** This was the only bibliographic index I could reach. I used it for:
   - **14 topical searches**, standing in for the Consensus backfill. They were plain queries with no filters, run one after another.
   - 10 title searches and 44 DOI look-ups (some DOIs repeated), for metadata and abstracts.

   Links are the DOI URLs exactly as Crossref returned them. Citation counts are Crossref `is-referenced-by` counts, which usually run below Consensus or Google Scholar counts. Crossref holds abstracts only where publishers deposit them: usually SSRN, Oxford University Press and Wiley, but not Elsevier or NBER.
2. **Saved Consensus records [CS-saved: source]** from sibling literature and verification files. I copied the URLs exactly as those files recorded them and did not re-run those searches.
3. **WebSearch ×3 [WS] and WebFetch ×3 [WF].** I used them only where Crossref could not resolve something:
   - two *Risk* magazine articles that have no DOI (Vasicek; Frye);
   - one abstract hunt (Chernenko & Scharfstein, unsuccessful);
   - the arXiv abstract page of a 2026 survey;
   - one 2026 FEDS Note (a DOI redirect, then the page itself).
4. **The VL [VL]**, which fetched the NBER and Federal Reserve pages for several references.

**Reading conventions**
- **[Inference]** marks reasoning that goes beyond what a record or abstract states.
- Findings restate abstracts, or for B18 the Federal Reserve page. I read no full texts.
- "In dossier" means the G6 dossier.
- Codes: **B1–B24** are annotated papers (Section 3); **F1–F14** are further records (Section 4.7).

**Organizational mapping (user-confirmed, 2026-10-18)**
- **Secondaries** is a hybrid of direct and fund investments. **Capital Solutions** is the structured and hybrid capital group.
- **Corporate Finance owns Treasury:** the liquidity gate, portfolio-level borrowing and facilities, overlay collateral and owner distributions.
- What this means for G6:
  - The optimizer's liquidity shadow price λ and any portfolio-level facility belong to Corporate Finance. SMA back-leverage on the Private Credit (PC) book is a group REFINANCE or LEVER proposal, and it must clear Corporate Finance's liquidity gate.
  - Evergreen exits, DDTL and revolver draws, and borrowing-base cures all draw on Corporate Finance's liquidity pool.
  - The dossier's "dry-powder reserve for opportunistic secondaries" (§6.3) overlaps the Secondaries group's direct-deal mandate. [Inference] Name one owner, and apply the intra-ADIC zero-liquidity rule (context §1A).

---

## 1. Summary

### Citation integrity
- **Scope: 20 academic works.**
  - **16** in the dossier's "Academic" list. Two bullets each hold two papers: Vasicek + Gordy, and Geltner + Getmansky–Lo–Makarov (GLM).
  - **2** FEDS Notes in the "Regulators" list: Cai & Haque (2024) and Berrospide et al. (2025).
  - **2** named in the body with no reference entry: Bühlmann (§2.7) and Takahashi–Alexander (§3).
  - **Not counted:**
    - the Fine–Gray estimator named in §7 (checked anyway; see the table);
    - official, practitioner and press sources, which the VL covers.
- **Result: 20 found, 0 mismatched, 0 not found.**
  - 18 confirmed in Crossref. The other 2 are *Risk* magazine articles with no DOIs (Vasicek, Frye), confirmed by WebSearch.
  - 4 also have saved Consensus records: Altman et al.; Bühlmann; Takahashi–Alexander; and GLM, for which only a thesis record exists.
  - 4 carry title variants, none of them errors:
    - Vasicek: *Risk* prints the title differently;
    - Altman et al., Frye and Rintamäki & Steffen: the subtitle is omitted.
  - This agrees with the VL: there are no hallucinated or garbled references.
- **Fixes:**
  1. **Upgrade the ten [K] entries to full metadata** (details in Section 2):
     - Altman et al., *J. Business* 78(6):2203–2228;
     - Duffie & Singleton, *RFS* 12(4):687–720;
     - Duffie et al., *JF* 64(5):2089–2123;
     - Lando, *RDR* 2(2–3):99–120;
     - Vasicek, *Risk* 15(12):160–162;
     - Gordy, *JFI* 12(3):199–232;
     - Frye, *Risk*, April 2000;
     - Geltner, *JRER* 8(3):325–345;
     - GLM, *JFE* 74(3):529–609;
     - Stanton, *RFS* 8(3):677–708.

     Add DOIs where they exist.
  2. **Add §10 entries for the two body-only works:** Bühlmann (1967) and Takahashi & Alexander (2002). Optionally add Fine & Gray (1999) for the estimator named in §7.
  3. **Rintamäki & Steffen.**
     - Full title: "PIK Now and Pay Later - How Deferred Interest Reshapes Private Credit", SSRN 2025, DOI 10.2139/ssrn.5341145.
     - Crossref holds no abstract, so the "+1–2pp" finding is still second-hand via the FSB. Keep it tagged [E]. VL C15 adds that it is an association with BDC-loan delinquency, not with default.
  4. **Add the missing DOIs:**
     - Erel–Flanagan–Weisbach (EFW) SSRN versions: 10.2139/ssrn.4771873 and 10.2139/ssrn.4779852;
     - FEDS Notes: 10.17016/2380-7172.3462 (Cai & Haque) and 10.17016/2380-7172.3802 (Berrospide et al.).
  5. **Geltner.** Sibling streams hold a different paper (Geltner 1991, *JREFE*). [Inference] The dossier's 1993 *JRER* paper fits its partial-adjustment marks model. Keep 1993 here and make the sibling dossiers consistent.

### Backfill
- **Method.** I ran 14 Crossref topical searches (4 seeds and 10 refinements; log in Section 7) and added saved records.
  - Three refinements returned only noise: BDC-specific, PIK, and open-end fragility. Saved records partly cover the last of these.
- **Result.** Section 3 annotates 24 papers:
  - 6 already in the dossier, re-read at abstract level;
  - **18 missing from it**.

  Section 4.7 lists 14 further records, for 38 in all.
- **The dossier misses six clusters of work:**
  1. **Return evidence that disagrees with "alpha ≈ 0".**
     - **Böni & de Roon (B2):** annual alphas above 6%. Alpha falls from 8.2% early in fund life to 3.9% late. Returns are left-skewed, with higher downside than upside betas.
     - **Böni & Manigart (B3):** funds outperform bond and equity benchmarks, with performance persistence.
     - **On the other side:** a 2026 survey (Zou, B4) agrees with EFW that fees consume most of the risk-adjusted return.
  2. **Equity risk inside private credit.**
     - EFW's own abstract (B1) says a typical fund carries equity risk as well as credit risk, and that ignoring equity risk produces positive alpha.
     - The dossier cites EFW for "alpha ≈ 0" but does not carry this equity loading into its risk model.
  3. **How direct lenders lend, and what that means for recoveries.**
     - **Jang, Kim & Sufi (B6):** direct lenders make enterprise-value loans to PE-backed, intangible-capital firms, with collateral claims on continuation value.
     - **Acharya, Bharath & Srinivasan (B11):** recoveries fall when the defaulter's industry is in distress.
  4. **Credit-supply cyclicality and bank funding.**
     - **Fleckenstein et al. (B16):** nonbank loan supply is about three times as cyclical as banks'.
     - **Haque & Wang (B18):**
       - banks charged BDCs about 1.1pp more during the 2022 tightening than they charged comparable borrowers;
       - credit risk does not explain the premium;
       - the lender base is concentrated.
  5. **Fund balance sheets.**
     - **Matvos, Piskorski & Seru (B19):** funds are 65–80% equity, with little maturity mismatch.
     - Losses fall largely on equity investors, that is, on LPs such as ADIC.
  6. **Wrapper-dependent marks and redemption fragility.**
     - **Andrade & Lie (B21):** the same loan is marked higher by sponsors whose investors exit at market prices than by sponsors that pay out at NAV. The gap widens with PIK income.
     - **Couts (B22):** queues protect open-end funds, but buffers do not, and buffers amplify fragility when added to queues.
     - **Li et al. (B23):** gates worsened the 2020 money-market fund run.
- **Where evidence is still thin.** Crossref keyword search found:
  - nothing academic on PIK toggles beyond Rintamäki & Steffen, which has no abstract;
  - nothing on recovery rates for direct loans;
  - nothing on BDC leverage after the 2018 change to the leverage cap.

  Keep those parameters tagged [I] or practitioner [S], with wide ranges. Re-run these searches in Consensus after 1 November (Section 7).

### Challenges (detail in Section 5)
1. **"Shrink group alpha toward 0 (Erel et al.)"** (§1.7, §6.11) depends on the method used (B1 against B2 and B3). Use a range, not a point.
2. **The credit-only risk engine** omits the equity and downside-beta exposure documented in B1 and B2. It therefore overstates how well PC diversifies against PE and public equity in down states.
3. **Marks use one κ schedule for every wrapper**, which ignores wrapper effects (B21). [Inference] NAV-redeemable evergreen units may be marked *more* conservatively than the books of listed-heavy sponsors, not less.
4. **Evergreen buffers do not protect holders the way the dossier implies** (B22, B23). This affects the IMF buffer horizon of 9–11 / 5–7 quarters, and the queue cap Liq_t in §6.4(8).
5. **Two recovery assumptions conflict with B6, B11 and B13:** direct-lending recoveries of 60–65% in Benign and Normal, and a software overlay that applies only in Crisis. This adds literature support to VL R3.
6. **The REFINANCE and LEVER cost assumptions** understate the tightening premium and lender concentration (B18).
7. **The system-fragility framing, and the synthetic look-through debt/equity of 0.5–0.75**, sit high against the newest balance-sheet data (B19).

None of these overturns the dossier's architecture: the competing-risks cohort engine, desmoothing, the queue model and the S/H/R/L economics. They change parameters, add state variables and alter two models (fund returns and marks).

---

## 2. Citation-integrity table

**Status key**
- **found:** metadata confirmed in the stated source.
- **title variant:** the published or full title differs slightly from the dossier's wording. This is not an error.

**Conventions**
- Counts are Crossref `is-referenced-by` unless stated otherwise.
- A working-paper DOI or year on a record does not count as a mismatch.
- The Consensus column shows a URL only where a sibling stream saved one earlier today. No Consensus search completed in this run.

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| Erel, Flanagan & Weisbach (2024), *Risk-Adjusting the Returns to Private Debt Funds*, NBER WP 32278 | found [CR][VL] | NBER WP 2024, DOI 10.3386/w32278 (27 cites). SSRN versions: 10.2139/ssrn.4771873 and 10.2139/ssrn.4779852. Crossref shows no journal version. The abstract supports the dossier (net abnormal return insignificant; gross positive) and adds that funds carry **equity risk** (B1). | none. The VL saw a Consensus record (SSRN 4771873) earlier but logged no URL. |
| Block, Jang, Kaplan & Schulze (2023/2024), *A Survey of Private Debt Funds*, NBER WP 30868; *RCFS* 13(2) | found [CR] | *Review of Corporate Finance Studies* 13(2):335–383 (2024), DOI 10.1093/rcfs/cfae001 (54). Crossref authors (Joern Block; Young Soo Jang; Steven N Kaplan; Anna Schulze) match. The abstract supports the uses in §4.2 and §5. | none |
| Chernenko, Erel & Prilmeier (2022), *Why Do Firms Borrow Directly from Nonbanks?*, *RFS* 35(11):4902–4947 | found [CR] | DOI 10.1093/rfs/hhac016 (148). Earlier versions: NBER WP (2019), DOI 10.3386/w26458; SSRN, DOI 10.2139/ssrn.3488958. | none |
| Acharya & Steffen (2020), *The Risk of Being a Fallen Angel and the Corporate Dash for Cash in the Midst of COVID*, *RCFS* 9(3):430–471 | found [CR] | DOI 10.1093/rcfs/cfaa013 (440). The dossier's quotation ("all firms drew down bank credit lines") appears in the abstract. | none |
| Li, Strahan & Zhang (2020), *Banks as Lenders of First Resort*, *RCFS* 9(3):472–500 | found [CR] | DOI 10.1093/rcfs/cfaa009 (290). | none |
| Rintamäki & Steffen (2025), *PIK Now and Pay Later*, SSRN [E] | found [CR]; title variant | "PIK Now and Pay Later - How Deferred Interest Reshapes Private Credit", Paul Rintamäki & Sascha Steffen, SSRN posted content 2025, DOI 10.2139/ssrn.5341145 (0). Crossref has no abstract, so the finding remains second-hand (FSB; VL C15). | none |
| [K] Altman, Brady, Resti & Sironi (2005), *The Link between Default and Recovery Rates*, *J. Business* 78(6) | found [CR][CS-saved: G3 VL]; title variant | Full title adds "Theory, Empirical Evidence, and Implications". *Journal of Business* 78(6):2203–2228, DOI 10.1086/497044 (516). The Consensus record gives 2003, the working-paper year. | [link](https://consensus.app/papers/details/4b638f0501945f7395fa9f005cdcc41f/?utm_source=claude_desktop) |
| [K] Duffie & Singleton (1999), *Modeling Term Structures of Defaultable Bonds*, *RFS* 12(4) | found [CR] | *RFS* 12(4):687–720, DOI 10.1093/rfs/12.4.687 (1,781). | none |
| [K] Duffie, Eckner, Horel & Saita (2009), *Frailty Correlated Default*, *JF* 64(5) | found [CR][VL] | *JF* 64(5):2089–2123, DOI 10.1111/j.1540-6261.2009.01495.x (420). | none. The VL found it in Consensus earlier but logged no URL. |
| [K] Lando (1998), *On Cox Processes and Credit Risky Securities*, *RDR* 2 | found [CR] | *Review of Derivatives Research* 2(2–3):99–120, DOI 10.1007/BF01531332 (686). | none |
| [K] Vasicek (2002), *The Distribution of Loan Portfolio Value*, *Risk* 15(12) | found [WS]; title variant | *Risk* 15(12):160–162. Risk.net lists the article as "Loan portfolio value". "The distribution of loan portfolio value" is the title on author-hosted copies. No DOI. One bibliography gives a different volume, but most sources give 15(12). | none |
| [K] Gordy (2003), *A Risk-Factor Model Foundation for Ratings-Based Bank Capital Rules*, *JFI* 12(3) | found [CR] | *Journal of Financial Intermediation* 12(3):199–232, DOI 10.1016/S1042-9573(03)00040-8 (609). | none |
| [K] Frye (2000), *Collateral Damage*, *Risk* 13(4) | found [WS]; title variant | *Risk*, April 2000 (volume 13; April is consistent with issue 4). The Federal Reserve Bank of Chicago copy is dated 20 March 2000, labelled as the *Risk* April 2000 version, and titled "Collateral Damage: A Source of Systematic Credit Risk". Page numbers not confirmed. No DOI. | none |
| [K] Geltner (1993), *Estimating Market Values from Appraised Values without Assuming an Efficient Market*, *JRER* 8(3) | found [CR] | *Journal of Real Estate Research* 8(3):325–345, DOI 10.1080/10835547.1993.12090713 (349). Sibling streams' saved Consensus record is a different paper (Geltner 1991, *JREFE* 4(3)). | none |
| [K] Getmansky, Lo & Makarov (2004), *An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns*, *JFE* 74(3) | found [CR] | *JFE* 74(3):529–609, DOI 10.1016/j.jfineco.2004.04.001 (790). In streams 04, 06 and 09, Consensus returned only Getmansky's 2004 thesis, which carries the same abstract. | thesis record: [link](https://consensus.app/papers/details/4e43d079332f5046860f2f39350f56f9/?utm_source=claude_desktop) |
| [K] Stanton (1995), *Rational Prepayment and the Valuation of Mortgage-Backed Securities*, *RFS* 8(3) | found [CR] | *RFS* 8(3):677–708, DOI 10.1093/rfs/8.3.677 (304). | none |
| Cai & Haque (23 Feb 2024), *Private Credit: Characteristics and Risks*, FEDS Notes | found [CR][VL] | DOI 10.17016/2380-7172.3462 (6). Metadata correct. VL C21: the 31% Form PF share belongs to public and private pensions together, not to public pensions alone. | none |
| Berrospide, Cai, Lewis-Hayre & Zikes (23 May 2025), *Bank Lending to Private Credit…*, FEDS Notes | found [CR][VL] | DOI 10.17016/2380-7172.3802 (3). VL C19: the note's table gives 6.4% but its text gives 6.6%. "≈SOFR+200" is the dossier's inference, not the note's. | none |
| §2.7 "Bühlmann" credibility (no year; no §10 entry) | found [CR][CS-saved: stream 04, G3] | Hans Bühlmann (1967), "Experience Rating and Credibility", *ASTIN Bulletin* 4(3):199–207, DOI 10.1017/S0515036100008989 (331). Add a §10 entry. | [link](https://consensus.app/papers/details/5542fe373291540f857447d36cf464a8/?utm_source=claude_desktop) |
| §3 "Takahashi–Alexander (TA) fund model" (no §10 entry) | found [CR][CS-saved: streams 04, 06, 08] | Dean Takahashi & Seth Alexander (2002), "Illiquid Alternative Asset Fund Modeling", *Journal of Portfolio Management* 28(2):90–100, DOI 10.3905/jpm.2002.319836 (56 in Crossref; 68 in the saved Consensus record). Add a §10 entry. | [link](https://consensus.app/papers/details/da7ee2d8587e575f99e3a36a590d2be6/?utm_source=claude_desktop) |
| *Not counted:* §7 "Fine–Gray" estimator (named method, no citation) | found [CR] | Jason P. Fine & Robert J. Gray (1999), "A Proportional Hazards Model for the Subdistribution of a Competing Risk", *JASA* 94(446):496–509, DOI 10.1080/01621459.1999.10474144 (13,536). An optional §10 entry. Aalen–Johansen was not checked. | none |

**Not tabulated.** The practitioner, official and press sources in §10 (Cliffwater, Proskauer, KBRA, Lincoln, IMF, FSB, ECB, BoE and others) are outside an academic check. The VL fetched almost all of them: 29 claims confirmed, 4 corrected, 4 unverifiable.

---

## 3. Annotated bibliography (24 papers)

### 3.1 Returns, risk adjustment and fees (B1–B5)

**B1. [Risk-Adjusting the Returns to Private Debt Funds](https://doi.org/10.3386/w32278)** [CR]
- **Record:** Isil Erel, Thomas Flanagan & Michael Weisbach · 2024 · NBER Working Paper · 27 Crossref cites · DOI 10.3386/w32278; abstract from SSRN version 10.2139/ssrn.4771873. In dossier: yes.
- **Finding:** For funds originated 1992–2015, a typical private credit fund "contains not only credit risk but also equity risk and delivers insignificant abnormal returns to its investors". Gross-of-fee abnormal returns are positive, and so are returns computed while ignoring equity risk.
- **Relevance to ADIC:** This is the anchor for the dossier's net-alpha prior.
  - [Inference] The PC sleeve needs an equity-factor loading in the total-portfolio risk model.
  - [Inference] Judge group forecasts against an equity-plus-debt benchmark, not against loans alone.

**B2. [Risk-Adjusted Private Debt Fund Performance and the Term Structure of Alphas](https://doi.org/10.2139/ssrn.4319347)** [CR]
- **Record:** Pascal Böni & Frans A. de Roon · 2023 · SSRN working paper (previously "Uncovering the Public and Private Components of Private Debt Returns") · 2 cites · DOI 10.2139/ssrn.4319347. In dossier: no.
- **Finding:**
  - Annual alphas are "over six percent".
  - Returns and alpha slope downward over fund life: 8.2% a year early and 3.9% late. Exposure to public factors is lowest early.
  - Returns are left-skewed, because downside betas exceed upside betas. Funds resemble portfolios long high-yield bonds and stocks and short investment-grade bonds.
- **Relevance to ADIC:** It directly contradicts the zero-alpha prior and adds a lifecycle structure.
  - [Inference] Make expected alpha a function of fund age, and use asymmetric (downside) betas.
  - [Inference] Treat the B1–B2 gap as method risk: cash-flow replication versus interim-NAV returns, which may themselves be smoothed.

**B3. [Private Debt Fund Returns, Persistence, and Market Conditions](https://doi.org/10.1080/0015198x.2022.2092384)** [CR]
- **Record:** Pascal Böni & Sophie Manigart · 2022 · *Financial Analysts Journal* 78(4):121–144 · 19 cites · DOI 10.1080/0015198X.2022.2092384; abstract from the 2021 SSRN version, 10.2139/ssrn.3932484. In dossier: no (the G3 dossier cites it).
- **Finding:**
  - Net of fees, private debt funds outperform bond and equity benchmarks in the cross-section, with wide dispersion across strategies and quartiles.
  - Lagged performance significantly affects current performance.
  - Ex-ante and ex-post credit conditions strongly affect performance, and GPs can only partially time them.
- **Relevance to ADIC:**
  - [Inference] Manager selection matters, given the dispersion and persistence. Condition vintage returns on credit conditions at entry.
  - The G3 VL adds, from the published text, that funding illiquidity has a negative effect more than twice the size of persistence.

**B4. [Private Credit Markets Theory, Evidence, and Emerging Frontiers](https://arxiv.org/abs/2603.14491)** [WF]
- **Record:** Jiacheng Zou · 2026 (submitted 15 March) · arXiv preprint, q-fin.GN · citations n/a · no DOI shown. In dossier: no.
- **Finding:** The fetch tool paraphrased the abstract; it would not quote it in full.
  - The survey is organized around four questions: growth, how direct lending differs from bank lending, risk-adjusted returns, and systemic risk.
  - Direct lenders charge a persistent spread premium over broadly syndicated loans, mostly to opaque PE-sponsored borrowers.
  - Fees consume most of the average fund's risk-adjusted return.
- **Relevance to ADIC:** This is the most recent survey found. It supports the dossier's gross-to-net bias (#7).
  - [Inference] Use it as the reading list for the underwriting red-team agent.
  - It is a single-author preprint and has not been peer-reviewed.

**B5. [Private Debt: Volatility, Credit Risk, and Returns](https://doi.org/10.2139/ssrn.2609235)** [CR]
- **Record:** Douglas J. Cumming, Grant Alan Fleming & Zhangxin (Frank) Liu · 2015 · SSRN working paper · 2 cites · DOI 10.2139/ssrn.2609235. In dossier: no.
- **Finding:**
  - The sample is private credit investments in more than 440 companies in 13 Asian countries, 2001–2015. Returns are fairly uniform across size, country and industry.
  - Secondary buying and selling beats buying and holding primary issuance.
  - Excess returns are positive and stationary. They are positively related to ΔVIX and ΔTED, and unrelated to market liquidity.
- **Relevance to ADIC:**
  - [Inference] The dossier treats SELL mainly as a liquidity tool. This paper suggests secondary trading can also be a return source.
  - It is an older, non-US working paper, so give it low weight.

### 3.2 Lending technology, borrower selection and recovery (B6–B11)

**B6. [The Lending Technology of Direct Lenders in Private Credit](https://doi.org/10.2139/ssrn.5744584)** [CR]
- **Record:** Young Soo Jang, Dasol Kim & Amir Sufi · 2025 · SSRN working paper · 0 cites · DOI 10.2139/ssrn.5744584. In dossier: no.
  - Also NBER WP w34500 (2025; 14 cites; DOI 10.3386/w34500).
  - Crossref lists a fourth author, Xiangyu Chen, on the NBER record only.
- **Finding:**
  - The data cover secured borrowing by the universe of US private middle-market firms.
  - Direct lenders rose mainly through their strength in enterprise-value-based loans to PE-backed firms in intangible-capital industries. Post-GFC bank regulation explains part of the rise, but that channel is quantitatively weaker.
  - Direct lenders write collateral claims on continuation value after default, and are more industry-specialized than banks.
- **Relevance to ADIC:** [Inference] Recovery in direct lending is a claim on going-concern value.
  - LGD should therefore depend on sector enterprise-value multiples (software especially) and on workout control (lender takeovers).
  - It will also correlate with ADIC's PE marks, which is wrong-way risk.
  - The paper qualifies B7: regulation is not the main driver of direct lending.

**B7. [Why Do Firms Borrow Directly from Nonbanks?](https://doi.org/10.1093/rfs/hhac016)** [CR]
- **Record:** Sergey Chernenko, Isil Erel & Robert Prilmeier · 2022 · *Review of Financial Studies* 35(11):4902–4947 · 148 cites · DOI 10.1093/rfs/hhac016. In dossier: yes.
- **Finding:**
  - In middle-market credit agreements from 2010–2015, one-third of loans come directly from nonbanks.
  - Two-thirds of that nonbank lending is attributable to bank regulation that limits lending to unprofitable, highly levered borrowers.
  - Firms with negative EBITDA are 32% more likely to borrow from nonbanks; firms with debt/EBITDA above 6 are 15% more likely. These firms pay significantly higher rates, especially after the 2013 leveraged-lending guidance revisions, and receive different non-price terms.
- **Relevance to ADIC:** It gives borrower-quality priors for the hazard covariates x_i.
  - [Inference] Add a negative-EBITDA flag and a debt/EBITDA > 6 flag to the cohort keys.
  - [Inference] A bank-regulation state shifts the opportunity set.

**B8. [A Survey of Private Debt Funds](https://doi.org/10.1093/rcfs/cfae001)** [CR]
- **Record:** Joern Block, Young Soo Jang, Steven N. Kaplan & Anna Schulze · 2024 · *Review of Corporate Finance Studies* 13(2):335–383 · 54 cites · DOI 10.1093/rcfs/cfae001. In dossier: yes.
- **Finding:**
  - Respondents are mainly direct-lending funds, with more than $390bn of AuM. They make mostly cash-flow-based loans, at leverage levels they believe banks would not fund.
  - They "target unlevered returns that appear high relative to their risk" and use less fund leverage than banks or CLOs.
  - PE sponsors help them lend more and write more effective covenants.
- **Relevance to ADIC:** It supports the dossier's haircut on underwritten returns and its sponsor covariate.
  - [Inference] Survey targets are a prior for the "underwritten" series only. They are targets, not realized returns.

**B9. [Direct lenders in the U.S. middle market](https://doi.org/10.1016/j.jfineco.2024.103946)** [CR]
- **Record:** Tetiana Davydiuk, Tatyana Marchuk & Samuel Rosen · 2024 · *Journal of Financial Economics* 162:103946 · 22 cites · DOI 10.1016/j.jfineco.2024.103946. Crossref has no abstract for the journal version; the finding comes from the 2020 SSRN version, DOI 10.2139/ssrn.3568718. In dossier: no.
- **Finding:**
  - The paper uses BDC investment data and three exogenous credit-supply shocks, including new banking regulations and a major finance-company collapse. It finds that BDC capital substitutes for traditional financing.
  - Access to BDC funding raises firms' employment growth and patenting.
- **Relevance to ADIC:**
  - [Inference] Bank-regulation shocks and lender failures raise demand for direct lending. Treat them as drivers of new-issue spreads and deal flow in the regime engine.
  - The published version may differ from the 2020 abstract.

**B10. [Specialization in Nonbank lending](https://doi.org/10.2139/ssrn.5257784)** [CR]
- **Record:** Rajendra Patidar · 2025 · SSRN working paper · 0 cites · DOI 10.2139/ssrn.5257784. In dossier: no.
- **Finding:**
  - BDCs specialize by industry, persistently. Specialization yields better loan performance and more favorable terms in the focus sectors.
  - Using the Senior Loan Officer Opinion Survey (SLOOS) as an instrument, tighter credit increases specialization. Specialized BDCs act as alternative lenders in stress.
- **Relevance to ADIC:** [Inference]
  - Use a manager-specialization score in manager selection and in PD/LGD priors.
  - The paper separates specialist concentration, which goes with better performance, from portfolio correlation (B14), which is a risk. The dossier's caps (§6.6) treat the two alike.

**B11. [Does industry-wide distress affect defaulted firms? Evidence from creditor recoveries](https://consensus.app/papers/details/6b9770edca525bec9ae7167d872bfcd4/?utm_source=claude_desktop)** [CS-saved: G3 VL][CR]
- **Record:** Viral V. Acharya, Sreedhar T. Bharath & Anand Srinivasan · 2007 · *Journal of Financial Economics* 85(3):787–821 · 565 Crossref cites · DOI 10.1016/j.jfineco.2006.05.011. In dossier: no (the G3 dossier cites it).
- **Finding:** This is the saved Consensus abstract, as quoted in the G3 VL. "Creditors of defaulted firms recover significantly lower amounts in present-value terms when the industry of defaulted firms is in distress". The G3 VL also notes a fire-sale effect.
- **Relevance to ADIC:** [Inference] Recoveries should depend on a sector-distress state as well as the macro regime.
  - This matters for software today. The dossier's ECB-based 80% software LGD applies only in Crisis. A sector-distress trigger could switch it on in Tight.

### 3.3 Default dependence, tails and rollover (B12–B15)

**B12. [Frailty Correlated Default](https://doi.org/10.1111/j.1540-6261.2009.01495.x)** [CR]
- **Record:** Darrell Duffie, Andreas Eckner, Guillaume Horel & Leandro Saita · 2009 · *Journal of Finance* 64(5):2089–2123 · 420 cites · DOI 10.1111/j.1540-6261.2009.01495.x. In dossier: yes ([K]).
- **Finding:**
  - Extreme default losses on US corporate debt portfolios are far more likely than observable-factor models imply.
  - At the confidence levels used for economic capital and ratings, conventional loss estimates are "downward biased by a full order of magnitude" on test portfolios. The sample is US public nonfinancial firms, 1979–2004.
- **Relevance to ADIC:** It supports the frailty term ξ_t in §6.4(2).
  - [Inference] Report P99 losses with and without frailty, as a model-risk band.
  - [Inference] σ_ξ = 0.35 is an assumption, and the P99 credit-risk budget in §6.6 is only as reliable as that parameter.

**B13. [The Link between Default and Recovery Rates: Theory, Empirical Evidence and Implications](https://consensus.app/papers/details/4b638f0501945f7395fa9f005cdcc41f/?utm_source=claude_desktop)** [CS-saved: G3 VL][CR]
- **Record:** Edward I. Altman, Brooks Brady, Andrea Resti & Andrea Sironi · 2005 · *Journal of Business* 78(6):2203–2228 · 516 Crossref cites · DOI 10.1086/497044. The Consensus record gives 2003. In dossier: yes ([K]).
- **Finding:** From the saved Consensus abstract: "recovery rates are a function of supply and demand for the securities, with default rates playing a pivotal role".
- **Relevance to ADIC:** It supports the PD–LGD link in §6.4(3).
  - [Inference] Make recoveries depend on the simulated default rate, not only on the regime label, so that bad paths within a regime also recover less.

**B14. [Correlated Collateral](https://consensus.app/papers/details/b9e7fb5f00b15112a3d6e2d05b5bda77/?utm_source=claude_desktop)** [CS-saved: stream 05][CR]
- **Record:** Taylor Nadauld, Shane M. Sherlund & Keith Vorkink · 2010 · SSRN working paper · 4 Crossref cites (3 in the saved record) · DOI 10.2139/ssrn.1573042. In dossier: no.
- **Finding:**
  - In the crisis, subprime MBS deals with geographically concentrated collateral had substantially higher default rates and more downgrades.
  - Concentration varied widely across deals and did not appear to be priced.
- **Relevance to ADIC:** [Inference] Correlation within a pool can go unpriced.
  - This supports the software and sector caps, and a correlation penalty for back-leverage and CFO tranches.
  - The evidence comes from mortgages, so it applies by analogy.

**B15. [Rollover Risk and Credit Risk](https://consensus.app/papers/details/272186b246105b7e98e6c262a594de43/?utm_source=claude_desktop)** [CS-saved: stream 06][CR]
- **Record:** Zhiguo He & Wei Xiong · 2012 · *Journal of Finance* 67(2):391–430 · 561 Crossref cites (630 in the saved record) · DOI 10.1111/j.1540-6261.2012.01721.x. In dossier: no.
- **Finding:**
  - When debt-market liquidity deteriorates, firms lose money rolling over maturing debt.
  - Equity holders bear those losses while maturing debt is repaid in full, so firms default at a higher fundamental threshold.
  - Short-term debt makes rollover risk worse.
- **Relevance to ADIC:** [Inference] This is a microfoundation for the dossier's maturity-extension branch.
  - In stress, borrowers facing maturity walls default earlier unless sponsors absorb the rollover losses.
  - Link the extension probability e_k(s_t) to the nonbank-supply state (B16) and to time to maturity.

### 3.4 Credit-supply cyclicality, monetary policy and bank funding (B16–B20)

**B16. [Nonbank Lending and Credit Cyclicality](https://doi.org/10.1093/rfs/hhaf024)** [CR]
- **Record:** Quirin Fleckenstein, Manasa Gopal, Germán Gutiérrez & Sebastian Hillenbrand · 2025 · *Review of Financial Studies* 39(4):925–966 · 16 cites · DOI 10.1093/rfs/hhaf024. In dossier: no.
- **Finding:**
  - Lower nonbank lending explains most of the contraction in syndicated credit during the GFC, and most of the related job losses. Banks' contribution was small.
  - Across several cycles, nonbank credit supply is about three times as cyclical as banks'.
- **Relevance to ADIC:** [Inference]
  - Refinancing supply for PC borrowers collapses in downturns. That supports lower CPR and more extensions in Tight and Crisis, and a stochastic CPR (VL R8, R9).
  - Competitor capacity also shrinks, which widens the opportunity set.
  - The evidence is on syndicated loans, not direct lending.

**B17. [Weathering Monetary Shocks: Nonbank Lending and Bank Ownership](https://doi.org/10.2139/ssrn.7275422)** [CR]
- **Record:** Jae Hyoung Kim · 2026 · SSRN working paper · 0 cites · DOI 10.2139/ssrn.7275422 (earlier version 2024: 10.2139/ssrn.4951471). In dossier: no.
- **Finding:**
  - In US syndicated loans, nonbank lenders blunt monetary tightening. They expand risky lending relative to banks and amplify banks' risk-shifting.
  - Bank-owned nonbanks increase lending in tightening, more so when the parent bank is highly levered.
- **Relevance to ADIC:** [Inference]
  - Vintages written during tightening, such as after the September 2026 hike, may hold weaker credits. Add a "written in tightening" covariate to the hazards, and net expected losses out of the reinvestment option value (VL R11).
  - Tightening is not the same as a downturn, so this is consistent with B16.
  - It is a single-author working paper on the syndicated market.

**B18. [The Price of Bank Funding Behind Private Credit: Evidence from Business Development Companies](https://doi.org/10.17016/2380-7172.4142)** [CR][WF]
- **Record:** Sharjil M. Haque & Jessie Jiaxu Wang · 7 August 2026 · FEDS Notes, Federal Reserve Board · 0 cites · DOI 10.17016/2380-7172.4142. In dossier: no.
- **Finding** (from the Federal Reserve page via WebFetch):
  - Banks charged BDCs "an additional interest-rate premium of about 0.9 percentage point during tightening". That is about 1.1pp in total over the cycle, compared with borrowers of the same bank, in the same quarter, with the same internal rating.
  - Credit risk and liquidity-risk exposure do not explain the premium. The authors point to bargaining power instead.
  - The top three banks hold about 47% of utilized BDC lending, and BDCs rarely switch lenders.
  - Bank loans are about 40% of BDC debt, against about 50% at the 2022 peak.
- **Relevance to ADIC:** [Inference]
  - Back-leverage and fund-facility spreads need an explicit tightening premium.
  - Facility refinancing risk depends on lender concentration and switching costs.
  - The note reports premiums relative to other bank borrowers, not absolute spreads.

**B19. [Private Credit, Balance Sheets and Financial Stability](https://doi.org/10.3386/w34991)** [CR]
- **Record:** Gregor Matvos, Tomasz Piskorski & Amit Seru · 2026 · NBER Working Paper w34991 · 9 cites · DOI 10.3386/w34991; abstract from SSRN version 10.2139/ssrn.6456977. In dossier: no.
- **Finding:**
  - The data cover most of the industry at fund and asset level. Funds are highly capitalized: equity is typically 65–80% of assets, against about 10% for US banks.
  - Debt use is moderate and is mostly bank credit lines used for liquidity. Fund lives of 10–12 years exceed loan maturities, so maturity mismatch is small.
  - Net returns are positive on average, with limited downside to creditors, because "losses are largely borne by equity investors".
- **Relevance to ADIC:** [Inference]
  - At system level, this moderates the dossier's IMF-based "multiple layers of leverage" framing. But it moves the tail onto LPs like ADIC rather than removing it.
  - Equity of 65–80% implies look-through debt/equity of about 0.25–0.54 (arithmetic). The dossier's synthetic 0.5–0.75 sits at or above the top of that range.

**B20. [The Risk of Being a Fallen Angel and the Corporate Dash for Cash in the Midst of COVID](https://doi.org/10.1093/rcfs/cfaa013)** [CR]
- **Record:** Viral V. Acharya & Sascha Steffen · 2020 · *Review of Corporate Finance Studies* 9(3):430–471 · 440 cites · DOI 10.1093/rcfs/cfaa013. In dossier: yes.
- **Finding:**
  - In the first phase of COVID, all firms drew down bank credit lines and raised cash.
  - After stabilization policies, only the highest-rated firms switched to capital markets. The lowest-quality BBB firms behaved like non-investment-grade firms.
- **Relevance to ADIC:** It confirms the dossier's quotation and its front-loaded crisis draw rate.
  - [Inference] After the first phase, draws concentrate in weaker borrowers. So the DDTL/revolver draw rate d_k(s) should correlate with borrower PD rather than be uniform.

### 3.5 Fund structure, marks and redemption fragility (B21–B24)

**B21. [Valuation, Liquidity, and Fund Structure in Private Credit](https://doi.org/10.2139/ssrn.7533698)** [CR]
- **Record:** Sandro C. Andrade & Erik Lie · 2026 · SSRN working paper · 0 cites · DOI 10.2139/ssrn.7533698. In dossier: no.
- **Finding:**
  - A fund that redeems at stated NAV must pay out what it reports, which restrains valuation optimism.
  - The paper examines 4,655 loans co-owned by BDCs. Sponsors with more assets in listed vehicles, whose investors exit at market prices, mark the same loan on the same date higher.
  - The gap is smaller for quoted loans and widens with the sponsor's PIK-income share. Non-public BDCs hold 4.22pp more of their assets in cash and quoted loans.
- **Relevance to ADIC:** [Inference] Mark bias depends on three things: the wrapper's exit mechanism, whether the loan is quoted, and PIK intensity.
  - Desmoothing in §6.4(6) needs wrapper-specific κ and bias terms.
  - ADIC can run the same test internally, by comparing the marks its managers assign to the same loan.

**B22. [Liquidity transformation risks and stabilization tools: Evidence from open-end private equity real estate funds](https://consensus.app/papers/details/abc2df60ee515faa8f6cf53c880555a8/?utm_source=claude_desktop)** [CS-saved: stream 05][CR]
- **Record:** Spencer J. Couts · 2025 · *Real Estate Economics* 53(5):1009–1044 · 3 Crossref cites (2 in the saved record) · DOI 10.1111/1540-6229.12532. In dossier: no.
- **Finding:**
  - Open-end funds that hold illiquid assets report stale, predictable NAVs. That invites NAV-timing, which transfers wealth from buy-and-hold investors and creates fragility.
  - Queues (discretionary liquidity restrictions) protect against this. Liquidity buffers do not, and buffers "amplify them when added to queues".
- **Relevance to ADIC:** This is the closest academic analogue to evergreen private credit.
  - [Inference] ADIC's redemption requests compete with NAV-timers. Fund cash buffers should not be credited as protecting ADIC's exit.
  - [Inference] Request intensity should rise with expected markdowns.

**B23. [Liquidity Restrictions, Runs, and Central Bank Interventions: Evidence from Money Market Funds](https://consensus.app/papers/details/389740373ccf5208b969643b471e31ae/?utm_source=claude_desktop)** [CS-saved: stream 05, G2][CR]
- **Record:** Lei Li, Yi Li, Marco Macchiavelli & Xing (Alex) Zhou · 2021 · *Review of Financial Studies* 34(11):5402–5437 · 108 Crossref cites (79 in the saved record) · DOI 10.1093/rfs/hhab065. In dossier: no.
- **Finding:**
  - The redemption gates and liquidity fees introduced by the 2016 money-market fund reform worsened the run on prime money-market funds in the COVID crisis.
  - Gates and fees can create strategic complementarities among investors.
- **Relevance to ADIC:** [Inference]
  - Gate risk drives pre-emptive requests. That supports the FSB point the dossier quotes: caps "may also have stimulated further redemption pressures".
  - New requests R^new should therefore depend on the perceived gate probability.
  - It is an analogy from money-market funds.

**B24. [CLO Performance](https://consensus.app/papers/details/c712f36af0415b9488a4a6e63c8facb8/?utm_source=claude_desktop)** [CS-saved: stream 05][CR]
- **Record:** Larry Cordell, Michael R. Roberts & Michael Schwert · 2020 · SSRN / Philadelphia Fed working paper · 17 cites (saved Consensus record) · DOI 10.2139/ssrn.3652124. In dossier: no.
- **Finding:**
  - CLO equity earns positive abnormal returns from the risk-adjusted price gap between leveraged loans and CLO debt.
  - Equity performance holds up through market volatility. The authors credit three features: the closed-end structure, long-term funding, and embedded options to reinvest principal.
- **Relevance to ADIC:** [Inference]
  - It supports the dossier's preference for rated-feeder or CFO funding (§6.8D) over mark-to-market back-leverage.
  - It suggests the reinvestment option is worth most in stress. Weigh that against the dossier's default of run-off.

---

## 4. Missed-but-important papers: design implications

Every item is **[Inference]** unless it restates a cited finding. Ownership follows the user-confirmed organization:
- the PC group owns asset-level proposals;
- Corporate Finance owns λ, portfolio-level facilities, the liquidity gate, and the cash consequences of evergreen exits, draws and cures.

### 4.1 State variables (new or refined)

| State | Definition | Feeds | Source |
|---|---|---|---|
| Fund lifecycle stage $a_j$ | Years since first close; early / mid / late, per fund interest | Expected alpha; ranking of SELL candidates; pricing of credit-secondary purchases | B2 |
| Factor exposures of the PC sleeve | Loadings on equity (separate upside and downside betas), HY and IG | TPA risk aggregation; diversification credit; IC risk card | B1, B2 |
| Nonbank credit-supply state $n_t$ | Nonbank share and volume of new middle-market issuance (for example, KBRA DLD volume); SLOOS standards | CPR; extension probability $e_k$; new-issue spread; opportunity set | B16, B10, B9 |
| Monetary-tightening flag $m_t$ | Policy-rate change over 12 months | Back-leverage spread premium; vintage-quality covariate | B17, B18 |
| Sector-distress state $d_{k,t}$ | Drawdown in sector spreads or EV multiples; sector default rate | Sector LGD; software overlay triggered before Crisis | B11, B6 |
| Collateral type and continuation–liquidation gap | Per loan: EV-based or asset-based; intangible-capital flag | LGD distribution; workout or lender-takeover branch | B6 |
| Wrapper mark-bias vector | Exit mechanism (NAV or market price); sponsor's listed share; quoted-loan flag; sponsor PIK share | κ and bias in the marks equation; economic NAV | B21 |
| Evergreen staleness and gate state | Expected markdown against reported NAV; gate history and probability | Request model $R^{new}$; ADIC fulfilment | B22, B23 |
| Facility lender concentration | Number of lenders; top-lender share; maturity ladder | Facility refinancing risk and cost | B18 |
| Manager specialization score | Industry HHI of the manager's book; persistence | PD and LGD priors; manager selection | B10, B3 |
| Draw–PD linkage | Rating mix of undrawn DDTLs and revolvers | Draw rate $d_k(s)$ | B20 |

### 4.2 Models
1. **A factor model for PC fund-interest returns.** It overlays the cohort engine and links PC to the TPA factors.
   - Specification: $r_{j,t}=\alpha(a_j)+\beta^{+}_{eq}r^{+}_{eq,t}+\beta^{-}_{eq}r^{-}_{eq,t}+\beta_{HY}r_{HY,t}-\beta_{IG}r_{IG,t}+\varepsilon_{j,t}$, with $\beta^{-}_{eq}>\beta^{+}_{eq}$ (B2).
   - Estimation: fit on ADIC's own cash flows by EFW-style replication (B1), with priors from B1 and B2.
2. **A method-mixture prior on alpha.**
   - One component sits near zero net of fees (B1, B4). The other centres on Böni–de Roon's lifecycle alphas (B2).
   - Set the weights by IC judgement and update them by credibility on ADIC's realized cash flows (Bühlmann, already in the dossier). Report both components.
3. **The LGD model.**
   - Specification: $\text{LGD}_i\sim\text{Beta}(\mu(\text{seniority},\ \text{collateral type},\ d_{k,t},\ \widehat{DR}_t),\ \phi)$, where $\widehat{DR}_t$ is the simulated default rate (B11, B13).
   - For EV-based loans in intangible sectors, index recovery to sector EV multiples (B6). This makes LGD co-move with ADIC's PE marks.
4. **Extension and default under rollover stress.**
   - The extension probability becomes $e_k(s_t,n_t,\tau_i)$, where $\tau_i$ is time to maturity.
   - The default threshold rises when $n_t$ falls, unless a sponsor absorbs the rollover loss (B15, B16).
5. **Wrapper-specific marks.**
   - Specification: $p^R_t=p^R_{t-1}+\kappa_w(p^E_t-p^R_{t-1})+b_w$. Here κ_w and b_w vary by wrapper w; b_w rises with the sponsor's PIK share and is smaller for quoted loans (B21).
   - Use cross-holder marks on identical loans as observations in the desmoothing Kalman filter.
6. **An evergreen queue with endogenous requests.**
   - Specification: $R^{new}_t=f(\mathbb E[\text{markdown}_t],\ P(\text{gate}_t),\ \text{others' requests})$.
   - Give no credit for fund buffers (B22, B23). Combine this with VL R7's pro-rata fulfilment formula.
7. **Facility pricing.**
   - Specification: $s^B_t=s^B_0(s_t)+\pi^{tight}m_t+g(\text{lender concentration})$, with $\pi^{tight}$ of about 1pp as a prior (B18).
8. **Term-funding alternative.** Model a CFO or rated feeder as a closed-end vehicle with term funding and a reinvestment option (B24), and compare it with mark-to-market back-leverage on cure tails.

### 4.3 Parameter priors (literature values, not ADIC data)

| Parameter | Prior | Source | Caveat |
|---|---|---|---|
| Net abnormal return, average fund | Insignificant (≈0) against equity and debt benchmarks; positive gross | B1 | Vintages 1992–2015 |
| Alpha from interim returns | Over 6% a year; 8.2% early in fund life, 3.9% late | B2 | Working paper; NAV-based returns |
| Return asymmetry | Downside beta above upside beta; long HY and stocks, short IG | B2 | Working paper |
| Fee drag | Fees consume most of the risk-adjusted return | B4 | Survey; abstract paraphrased |
| Fund capitalization | Equity 65–80% of assets, so look-through debt/equity ≈ 0.25–0.54 (arithmetic) | B19 | The abstract covers "private credit funds". BDC leverage is higher (IMF: debt/equity 0.8–1.2×) |
| Fund life against loan maturity | 10–12 years against shorter loans | B19 | — |
| Nonbank-borrower profile | Negative EBITDA: +32% likelihood of borrowing from nonbanks. Debt/EBITDA > 6: +15%. One-third of middle-market loans | B7 | 2010–2015 |
| Cyclicality of nonbank supply | About 3× that of banks | B16 | Syndicated loans |
| Bank-funding premium for BDCs in tightening | About 0.9pp extra, about 1.1pp in total, relative to comparable borrowers | B18 | Relative, not absolute |
| BDC bank-debt share and concentration | About 40% of BDC debt (about 50% at the 2022 peak); top three banks about 47%; Gini 0.78 | B18 | — |
| Liquidity gap between wrappers | Non-public BDCs hold 4.22pp more in cash and quoted loans | B21 | Same sponsor and quarter |
| Tail bias without frailty | About 10× underestimate at high confidence levels (test portfolios) | B12 | US public firms, 1979–2004 |
| Draw behavior in a crisis | Phase 1: all firms draw. Later, only top-rated firms substitute to capital markets | B20 | COVID episode |

### 4.4 Constraints
1. **Correlation-aware concentration.**
   - Keep the software cap at ≤15% (§6.6) and add a cap linked to sector distress (B14).
   - Do not penalize manager specialization as such (B10). Distinguish manager concentration from portfolio correlation.
2. **Evergreen holdings.**
   - Keep the ≤10% cap.
   - Count expected fulfilment net of competition from NAV-timing redeemers, and never credit fund buffers (B22, B23).
3. **Back-leverage and facilities.**
   - Require at least three lenders and cap the share of any one lender.
   - Term out facilities before tightening, and stress cost by +100bp in tightening (B18).
   - Prefer closed-end or term structures (B24).
4. **The LEVER test.** Apply EL < y_A − c_B with c_B including the tightening premium.
   - Adding 1.1pp to the dossier's base 5.5% gives 9.5% − 6.6% ≈ 2.9% (arithmetic; the premium is a relative measure).
   - The VL gets 3.25–3.75% at the dossier's Tight spreads.
   - Both are below the dossier's 4.0%.
5. **The P99 credit-risk budget.** Evaluate it with frailty, and show a frailty-free band alongside (B12).

### 4.5 Objectives and shadow prices
1. **Charge equity beta.** Price the PC sleeve's equity beta, including downside beta, at the TPA's equity risk price in the Tier-2 objective. Without this, PC is credited with diversification it does not provide in down states (B1, B2).
2. **Fund-age alpha in SELL/HOLD.** Selling a late-life fund interest forgoes less alpha (3.9% against 8.2%), so its λ* threshold should be lower than for an early-life interest (B2).
3. **Reinvestment option value.** Compute it net of expected loss, minus a penalty for vintages written in tightening (B17; VL R11).
4. **Dry-powder value must be state-dependent.**
   - In downturns, nonbank capacity shrinks (B16) and specialists step in (B10). But ADIC's funding cost rises too (B18).
   - So price the reserve off $n_t$ and $m_t$, not as a fixed premium.

### 4.6 Agent and IC design
1. **Return-assumption red-team agent.**
   - Shows the alpha range by method (B1 against B2), the fee drag (B4) and persistence (B3).
   - Requires the group to state the risk-adjustment method behind every forecast.
2. **Valuation agent.**
   - Applies wrapper-aware marks.
   - Compares marks on identical loans held by different managers (B21).
   - Flags PIK-heavy sponsors.
3. **Treasury / Corporate Finance seat.** It owns:
   - the evergreen exit model, including gate complementarities (B23) and no credit for buffers (B22);
   - facility lender concentration and the tightening premium (B18);
   - the link between DDTL draws and borrower PD (B20).
4. **Credit-cycle monitor agent.** Computes $n_t$ and $m_t$ from public series such as issuance volumes and SLOOS (B16, B17).
5. **IC card for Private Credit.** Shows:
   - equity and downside beta;
   - alpha by fund age;
   - mark gap by wrapper;
   - LGD by collateral type and sector distress;
   - lender concentration in facilities.

### 4.7 Further records (compact)

| # | Record | Metadata | What it adds |
|---|---|---|---|
| F1 | [Private Credit and Financial Stability](https://doi.org/10.2139/ssrn.5930356) [CR] | Sergey Chernenko & David S. Scharfstein · 2026 · SSRN · 0 cites | No abstract in Crossref, and one WebSearch found none. Findings not reported. Re-check in Consensus. |
| F2 | [Bank Capital and the Growth of Private Credit](https://doi.org/10.2139/ssrn.5097437) [CR] | Sergey Chernenko, Robert Ialenti & David S. Scharfstein · 2025 · SSRN · 1 cite | No abstract in Crossref. The WebSearch tool's own summary says PC funds are well capitalized and that banks may prefer lending to PC funds over lending to firms directly. That summary is unverified. |
| F3 | [Financial Stability Reports Explore Private Credit](https://doi.org/10.2139/ssrn.4977103) [CR] | W. Scott Frame · 2024 · SSRN · 0 cites | No abstract. Possibly a review of central-bank FSR coverage [Inference from the title]. |
| F4 | [Private Credit: Market Structure, Fund Design, and Retail Access](https://doi.org/10.56227/26.1.15) [CR] | Cheryll-Ann Wilson · 2026 · report (CFA Institute DOI prefix) · 0 cites | No abstract. Relevant to evergreen wrappers [Inference from the title]. |
| F5 | [Optimization of Private Credit Fund Portfolio and its Performance Metrics Selection](https://doi.org/10.2139/ssrn.5320841) [CR] | Dmitry Garmash · 2025 · SSRN · 0 cites | No abstract. |
| F6 | [Monetary tightening and corporate default risk: Evidence from floating-rate debt exposure](https://doi.org/10.1016/j.bir.2026.100837) [CR] | Aykut Şengül & Levent Çinko · 2026 · *Borsa Istanbul Review* 26(4):100837 · 0 cites | No abstract. The title matches the dossier's rate-to-ICR-to-default channel. Check the sample before using it. |
| F7 | [Long-Run Relationship between Default Rates and Macroeconomic Variables in the U.S. Leveraged Loan Market](https://doi.org/10.3905/jfi.2014.24.3.064) [CR] | Daniel Ilg · 2014 · *Journal of Fixed Income* 24(3):64–76 · 2 cites | No abstract. A candidate for linking the macro state to loan defaults. |
| F8 | [Nonbank Market Power in Leveraged Lending](https://doi.org/10.2139/ssrn.6577180) [CR] | Franz J. Hinzen · 2026 · SSRN · 0 cites | CLO managers have market power, rooted in banks' switching costs, and extract lender-friendly terms. Relevant to loan terms in syndicated markets. |
| F9 | [Market liquidity and funding liquidity](https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop) [CS-saved: streams 05, 06, 08, G2] | M. Brunnermeier et al. · 2009 · *RFS* · 5,153 cites · DOI 10.1093/rfs/hhn098 | Funding and market liquidity reinforce each other, and margins can spiral. This supports §6.5's regime-dependent advance rates. |
| F10 | [Hidden in Plain Sight—The Impact of Undrawn Commitments](https://consensus.app/papers/details/d99e5eff8f48558898b24269df59ba18/?utm_source=claude_desktop) [CS-saved: streams 05, 06, G3] | T. Meyer · 2020 · DOI 10.3905/jai.2020.1.101 · 2 cites | Uncalled capital carries risk and opportunity cost. Relevant to PC fund unfunded commitments ($3.0bn, synthetic). |
| F11 | [Frei 2024](https://consensus.app/papers/details/d35d4e1ecf44524eb84639452a64a82c/?utm_source=claude_desktop) [CS-saved: stream 04] | Title and venue not stored in stream 04; Crossref search did not resolve them | Per stream 04: for heavily smoothed series, unsmoothed volatility can overstate true volatility, and cross-asset correlations cannot be fully recovered. Validate desmoothed PC NAVs against loan and BDC prices. |
| F12 | [Anson 2024, *JPM*](https://consensus.app/papers/details/b824603706ab55abbca0473de791c8d8/?utm_source=claude_desktop) [CS-saved: stream 04] | Full metadata not stored; Crossref search did not resolve it | Per stream 04: lagged betas extended to private credit. A cross-check on PC beta. |
| F13 | [Novelli et al. 2026](https://consensus.app/papers/details/fc5b871ff9c953cda7fe259670b078a0/?utm_source=claude_desktop) [CS-saved: stream 07] | *Academy of Management Annals* | Per stream 07: a review of 936 articles on decision-making in PE and private credit. Useful for IC design. |
| F14 | [Risk-adjusting the returns to venture capital](https://consensus.app/papers/details/38b28ae37b555f3087e387f515331a0f/?utm_source=claude_desktop) [CS-saved: streams 04, 08] | Korteweg & Nagel · *JF* 71(3) (2016); record year 2015; DOI 10.2139/ssrn.2309596; 134 cites | The GPME (SDF-based PME) family behind EFW-style risk adjustment. The basis for a multi-kernel alpha report. |

---

## 5. Papers that challenge the dossier's recommendations

| # | Dossier position (§) | Challenging evidence | Strength | Suggested change |
|---|---|---|---|---|
| C1 | "Shrink group alpha toward 0 (Erel et al.)" (§1.7; §5 bias #7; §6.11) | B2: alphas over 6%, falling from 8.2% to 3.9% over fund life. B3: funds outperform benchmarks, with persistence. On the dossier's side: B1 and B4. | Moderate. B2 is a working paper using interim-NAV returns; B3 uses net IRRs. The disagreement may reflect method and smoothing [Inference]. | Replace the point shrinkage with a method-mixture prior (§4.2 #2) and fund-age alpha. Keep "net everything". |
| C2 | A credit-only risk engine (ICR, frailty, EBITDA index); PC framed as the defensive "natural DPI" sleeve (§1.4, §3, §6.4, §6.7) | B1: PC funds carry equity risk. B2: left skew, with downside betas above upside betas. | Strong on direction; two independent sources | Add equity and HY factor loadings with downside asymmetry, charge them in Tier 2, and show them on the IC card. PC's *liquidity* role is unaffected; its *risk-diversification* credit falls [Inference]. |
| C3 | One desmoothing rule, with κ varying only by regime (§2.5, §6.4(6), §6.5). §1.3 uses 15–30% tender discounts on non-traded BDC shares as evidence that reported NAV overstates economic value. | B21: sponsors with a larger share of listed vehicles mark the same loan on the same date *higher*. Paying exiting investors at NAV disciplines marks. The gap widens with PIK share and narrows for quoted loans. F11: desmoothing artefacts. | Moderate: a single 2026 working paper, but a clean identification design | Use wrapper-specific κ_w and b_w, with PIK-share and quoted-loan covariates. The 15–30% tender discounts (aggregator; VL C37) may price illiquidity rather than optimistic marks [Inference]. |
| C4 | Evergreen resilience measured by buffer horizons (IMF 9–11 / 5–7 quarters); queue payouts capped by Liq_t; request rates fixed (§1.2, §4.3, §6.4(8), §6.5) | B22: buffers do not protect, and amplify fragility when added to queues. B23: gates create strategic complementarities. | Moderate: analogues from open-end real estate funds and money-market funds | Make requests endogenous (§4.2 #6) and give no credit for fund buffers. Keep the dossier's rule that "evergreen redemption rights are not liquidity". It is reinforced. |
| C5 | Direct-lending recoveries of 65% / 60% in Benign / Normal; software overlay only in Crisis (§6.5) | B6: lending against continuation value. B11: recoveries fall in industry distress. B13: default rates are "pivotal" for recoveries. | Strong on direction; adds to VL R3 | Make LGD depend on collateral type and sector distress (§4.2 #3). Trigger the software overlay in Tight on sector distress. Tie recoveries to the simulated default rate. |
| C6 | REFINANCE at ≤40–45% LTV is "a cheap bridge" at S+200; the LEVER hurdle is ≈4% (§6.8D–E, §6.11) | B18: about a 1.1pp premium in tightening, with concentrated lenders. B16: nonbank funding is the most cyclical. | Moderate: one Fed note, and the premium is relative | Make facility cost depend on the regime and include a tightening premium. Add a lender-concentration constraint. The LEVER hurdle in Tight becomes about 2.9–3.75% (§4.4 #4). |
| C7 | A system-fragility framing ("multiple layers of leverage", §4.3); synthetic look-through debt/equity of 0.5–0.75 (§6.11) | B19: equity is 65–80% of fund assets, maturity mismatch is small, and losses fall on equity investors. | Moderate: a 2026 working paper with broad data | Recalibrate look-through leverage by wrapper: funds at about 0.25–0.54 (arithmetic), BDCs higher (IMF). The IC message should be the LP tail, not system risk [Inference]. |

**What the literature supports.** Several dossier positions find support:
- the frailty term (B12);
- the PD–LGD link (B13);
- the front-loaded crisis draws (B20);
- the premise that evergreen redemption rights are not liquidity (B22, B23);
- the preference for term or CFO funding over mark-to-market back-leverage (B24);
- the dry-powder option logic for a *future* stress, since nonbank capacity shrinks in downturns (B16) and specialists step in (B10).

As VL R10 notes, today's evidence on credit secondaries (pricing near par) does not show buyer value now.

---

## 6. Verbatim usage message

Consensus returned this message on all three attempts. It is a monthly-quota rejection, not a rate limit:

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Search log, sources and rerun plan

**Consensus**
- 3 attempts on one query ("Risk-Adjusting the Returns to Private Debt Funds"), 30 seconds apart. All three were rejected by the monthly quota, so **0 searches completed**.
- No filters were used and no thread tools were called.

**OpenAlex**
- 5 title queries, run one after another. All returned HTTP 429 (daily credit exhausted; `Retry-After: 48357`). No records were used.

**Semantic Scholar**
- 4 attempts at one relevance search. All returned HTTP 429. No records were used.

**Crossref: 14 topical searches** (plain query, no filters, 8 results each). Outcomes:
1. "private credit direct lending returns": B6.
2. "private debt default recovery rates": noise (sovereign debt).
3. "business development companies leverage performance": noise (corporate leverage).
4. "private credit financial stability risk": B19, F1, F3.
5. "direct lenders middle market private credit": B9, B6.
6. "private credit fund performance": B21, F4, F5.
7. "business development companies BDC": noise.
8. "business development company net asset value discount private credit loans valuation": noise (NAV loans, valuation texts).
9. "payment-in-kind interest private credit loans": noise.
10. "nonbank lending credit cyclicality": B16, B10, B17.
11. "private debt funds returns risk persistence": B1, B3, B2, B5.
12. "leveraged loan recovery rates loss given default": generic; F7.
13. "open-end fund redemptions fragility illiquid assets": noise. Covered by saved records B22 and B23.
14. "floating rate debt interest rate increases corporate default risk": F6.

**Crossref: 10 title searches**
- Chernenko–Erel–Prilmeier; Rintamäki–Steffen; Vasicek; Frye; Cai–Haque; Berrospide et al.; EFW (journal-version check); Anson 2024; Frei 2024; Chernenko–Ialenti–Scharfstein.
- Vasicek, Frye, Anson and Frei were not resolved.

**Crossref: 44 DOI look-ups** (some DOIs repeated), for metadata and abstracts.

**WebSearch (3)**
- Vasicek (2002): sources used were [risk.net, "Loan portfolio value"](https://www.risk.net/risk-management/credit-risk/1530287/loan-portfolio-value), the author-hosted copy at [maths.univ-evry.fr](https://www.maths.univ-evry.fr/pages_perso/crepey/Credit/Vasicek.pdf) and the [vasicekfit reference manual](https://ftp.kaist.ac.kr/CRAN/web/packages/vasicekfit/refman/vasicekfit.html).
- Frye (2000): sources used were the [Chicago Fed copy](https://www.chicagofed.org/~/media/publications/risk-management-papers/sr-2000-15-pdf.pdf) and the [BIS presentation](https://www.bis.org/bcbs/events/oslo/frye.pdf).
- Chernenko & Scharfstein (2026): no abstract found. The results surfaced the arXiv survey (B4) and the related 2025 working paper (F2).

**WebFetch (3)**
- [arXiv abstract page 2603.14491](https://arxiv.org/abs/2603.14491).
- [DOI 10.17016/2380-7172.4142](https://doi.org/10.17016/2380-7172.4142), which redirected; then the [Federal Reserve note page](https://www.federalreserve.gov/econres/notes/feds-notes/the-price-of-bank-funding-behind-private-credit-evidence-from-business-development-companies-20260807.html).

**Raw logs** (session scratchpad):
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g6lit_log_citations.txt`
- `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\g6lit_log_backfill.txt`
- Helper scripts are in `...\scratchpad\g6lit_scripts\`.

**Rerun plan after 1 November 2026, in Consensus with no filters**
1. **Re-run the citation table** so that every row carries a Consensus URL.
2. **Re-run the four seed queries.** Consensus's semantic ranking should surface work that Crossref's keyword ranking missed. This applies especially to queries 2, 3, 7–9 and 13 above, which returned noise.
3. **Targeted gaps:**
   - "PIK toggle default private credit";
   - "direct loan recovery rates lender takeover";
   - "BDC leverage Small Business Credit Availability Act";
   - "non-traded BDC redemptions tender";
   - "private credit monetary policy transmission";
   - "interest coverage floating rate leveraged borrowers default".
4. **Missing abstracts:** fetch them for F1, F2, F6 and F7, and for the journal versions of B9 (*JFE*) and B3 (*FAJ*).
