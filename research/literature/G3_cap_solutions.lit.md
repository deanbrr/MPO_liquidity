# G3 literature check: Capital Solutions (structured and hybrid capital)

**Dossier checked:** `research/groups/dossiers/G3_cap_solutions.md` (as of 2026-10-18; 55 references).
**Date:** 2026-10-18.
**Companion:** `research/groups/verification/G3_cap_solutions.verify.md` (the "verification log", VL).

> **Blocker: Consensus was unavailable for this run.**
> - My first query (the Erel–Flanagan–Weisbach title) was rejected three times, 30 seconds apart, with a monthly-quota message (Section 6). The quota resets on 1 November 2026.
> - **No Consensus search completed and I retrieved no new Consensus records.** I sent no further Consensus calls, because the quota covers the whole account.
> - Everything below comes from the three disclosed fallbacks listed next. Section 7 gives a rerun plan for after the reset.

**Fallbacks (disclosed)**
1. **Saved Consensus records.** Earlier today, the sibling literature files (streams 01–14) and the VL stored Consensus results. I reuse them with their URLs copied exactly as those files recorded them. I did not re-run those searches. They are tagged **[CS-saved: stream NN]** or **[CS-saved: VL]**.
2. **WebSearch, 8 queries.** I used these only to confirm the bibliographic metadata of eight well-known papers on the seed topics, because Consensus could not resolve them today. Findings for these papers come only from the abstract text shown in the search results. They are tagged **[WS]**.
3. **The VL's Crossref check** of the dossier's reference list. Tagged **[VL]**.

**Reading conventions**
- **[Inference]** marks design reasoning that goes beyond what a record or abstract states.
- Author lists follow the source record ("et al." where it truncates).
- "In dossier" refers to the G3 dossier only.
- Codes:
  - **B1–B23**: annotated papers (Section 3).
  - **F1–F12**: further saved records (Section 4.7).
  - **U1–U4**: records with no abstract (Section 4.8).

**Organizational mapping (user, 2026-10-18)**
- **Secondaries** is a hybrid of direct and fund investments.
- **Capital Solutions** is the structured and hybrid capital group.
- **Corporate Finance owns Treasury**: the liquidity gate, portfolio-level borrowing, overlay collateral and owner distributions.
- So the liquidity shadow price ℓ and portfolio-level facilities are Corporate Finance's. Asset-level back-leverage on the Capital Solutions book is a group REFINANCE or LEVER proposal.

---

## 1. Summary

### Citation integrity
- **Scope: 21 academic works.**
  - **15 in the reference list:** refs 41–55, counting the FEDS Note as quasi-academic.
  - **6 named in the body with no reference entry:**
    - Takahashi–Alexander (§3.4, via stream 04's RFT-TA model);
    - Geltner and Getmansky–Lo–Makarov (GLM) (§6.8);
    - Brown–Ghysels–Gredil (BGG) (§4.6);
    - Bühlmann and Mack (§3.8).
  - **Two further items, not counted:** ref 40 (IMF GFSR, an official report) and an unnamed "BIS work" (§4.7).
- **Result against saved Consensus records:**
  - 8 found;
  - 1 not found in Consensus (GLM, which exists: streams 04 and 09 confirmed it by WebSearch);
  - 0 mismatched;
  - 12 could not be checked in Consensus today.
- **Of the 12 unchecked works, 11 were already confirmed by the VL** (against Crossref, or for Cai & Haque against the Fed page).
  - That covers the dossier anchors Erel–Flanagan–Weisbach (EFW) and Böni–Manigart (BM), and all the classic credit and convertible models.
  - Mack is ambiguous: the dossier gives no year or title.
  - Neither the VL nor this check found any hallucinated reference.
- **Fixes needed:**
  1. **Add reference entries for the six body-only works** (metadata in Section 2):
     - Takahashi & Alexander (2002), *JPM* 28(2):90–100;
     - Geltner (1991), *JREFE* 4(3);
     - GLM (2004), *JFE* 74(3):529–609;
     - BGG, *RFS* 36(3):945–986 (2023);
     - Bühlmann (1967), *ASTIN Bulletin* 4(3);
     - Mack: name the paper. [Inference] For development triangles this is usually Mack (1993), but that is not verified.
  2. **Upgrade the three [K] entries using the VL's Crossref metadata:**
     - Black–Cox: *JF* 31(2):351–367.
     - Tsiveriotis–Fernandes: *JFI* 8(2):95–102, DOI 10.3905/jfi.1998.408243. This fixes the failed DOI lookup.
     - Lando: *RDR* 2(2–3):99–120.
  3. **Kaplan & Schoar (ref 52) is an orphan.** Cite it in §4.4 (vintage cyclicality) or drop it (VL).
  4. **Cai & Haque (ref 41): wrong source for the recovery figures.** The 33/52/39% values are KBRA DLD data, not S&P (VL F11).
  5. **The "BIS work" in §4.7 is not identifiable.** The IMF calls the cyclicality evidence "mixed" (VL A3). Name the BIS paper or drop the claim.
  6. **"Smoothing ≈ 0.5 per quarter (BGG-derived)" (§4.6).** The saved BGG abstract reports fund betas and total risk, not a smoothing coefficient. Attribute 0.5 to stream 04's derivation.

### Backfill
- **What I could and could not do.** I could not run the 8–14 Consensus topical searches (seed queries in Section 7).
  - The 23 annotated papers instead come from three sources:
    - 8 papers on the seed topics, confirmed by WebSearch;
    - 13 saved Consensus records;
    - the 2 dossier anchors, EFW and BM.
  - Section 4.7 adds 12 more saved records and Section 4.8 adds 4 without abstracts, for 39 listed in all.
- **The dossier misses seven clusters of work:**
  1. **GP economics, which GP stakes and GP solutions (family B) depend on.**
     - Metrick–Yasuda (B11): about two-thirds of expected GP revenue is fixed.
     - Chung et al. (B12): indirect pay from future fundraising is about as large as carried interest.
     - Barber–Yasuda (B13) and Brown et al. (B14): fundraising-time NAV management.
     - The dossier models GP stakes as "cash yield 6–8% + growth", anchored only on Blackstone's GP Stakes return, with no academic grounding.
  2. **Valuing structured preferred (family C).**
     - Gornall–Strebulaev (B5): headline round valuations of VC unicorns overstate fair value by 48% on average, because they treat all shares like the newest preferred.
     - Sundaresan et al. (B6): priority structures change issuer behaviour.
  3. **Rescue and special-situations capital (family E).**
     - Brophy–Ouimet–Sialm (B7): last-resort PIPE financing goes to weak, opaque issuers. Investors protect themselves with discounts, repricing rights and short positions, and issuers then underperform.
     - Jiang–Li–Wang (B8): hedge funds in Chapter 11, loan-to-own strategies and effects on outcomes.
  4. **Nonbank junior lending (family D) and underwriting targets.**
     - Chernenko–Erel–Prilmeier (B9): nonbank borrowers are unprofitable or highly levered and pay higher rates. Earlier drafts say these loans more often carry warrants.
     - Block et al. (B3): funds target unlevered returns that "appear high relative to their risk".
  5. **Sponsor support in crises.** Bernstein–Lerner–Mezzanotti (B10): PE-backed firms got more equity and debt in 2008, especially where sponsors had more resources.
  6. **Collateral quality for fund finance (family A) and the pricing service.**
     - Albertus et al. (B15): subscription lines distort timing-sensitive performance measures.
     - BGG (B16): fund-level risk of 33–40% a year.
     - Jenkinson et al. (B17): VC NAVs are biased.
  7. **Fire sales, dry powder and funding liquidity (the opportunity set).** Shleifer–Vishny (B18), Diamond–Rajan (B19), Pulvino (B20) and Brunnermeier–Pedersen (B21). Also, for the book's structured exits: the *JEP* structured-finance paper (B22) and Cordell et al. (B23).
- **What remains thin.** The academic evidence on PIK toggles, preferred equity in sponsor-backed companies, NAV loans and GP stakes as instruments is still thin. This check found nothing new on PIK toggles or minimum-MOIC terms, and NAV-financing papers exist only without abstracts (U1–U3).
  - Keep these parameters tagged [C] or [I], with wide robustness ranges.

### Challenges (details in Section 5)
1. **Deploy-versus-wait (§1.6, §5.6 C2).** The dossier concludes that "idle dry powder does not pay", but it fixes crisis IRRs exogenously.
   - Fire-sale theory and evidence (B18–B20) say the return on cash in a fire-sale state is endogenous, and can be high for unconstrained buyers.
   - Together with VL R1, this means C2's conclusion does not yet stand.
2. **Crisis vintage IRRs of 14–18% (§6.7).** These ignore two things:
   - adverse selection among issuers that accept last-resort capital (B7);
   - BM's funding-illiquidity effect, which is negative and more than twice the size of performance persistence (B2, via the VL).
3. **GP stakes (§6.6 #4).** [Inference] GP stakes load on the same performance and fundraising cycle as ADIC's PE book (B11, B12), so they concentrate rather than diversify.
4. **"Current actual" series (§6.8).** The correction list omits valuation error that comes from contract terms (B5).
5. **Uniform crisis hazards (§6.7).** These ignore sponsor resources (B10).

None of these overturns the dossier's architecture: the hybrid structural and reduced-form engine, LAPV-based decisions, and conflict controls on the pricing service. They change the parameters, add state variables and add one model for GP stakes.

---

## 2. Citation-integrity table

**Status values**
- **found** / **not found**: against a saved Consensus record.
- **unchecked (quota)**: Consensus was unavailable. The VL's Crossref result is given where it exists.

A working-paper year or SSRN DOI on a Consensus record does not count as a mismatch.

| Dossier citation | Status | Corrected / confirmed metadata | Consensus URL |
|---|---|---|---|
| Ref 42. Erel, Flanagan & Weisbach (2024), NBER WP 32278 | unchecked (quota; 3 rejected attempts) | [VL] Correct: March 2024, DOI 10.3386/w32278; no journal version in Crossref when the VL checked. | none |
| Ref 43. Böni & Manigart (2022), *FAJ* 78(4):121–144 | unchecked (quota) | [VL] Correct (Crossref; online 18-Aug-2022; open access). | none |
| Ref 41. Cai & Haque (2024), FEDS Notes | unchecked (quota) | [VL] Metadata correct. **Attribution error:** the recovery figures (33/52/39%) are KBRA DLD data, not S&P. Correction posted 26-Feb-2024. | none |
| Ref 44. Merton (1974), *JF* 29(2):449–470 | unchecked (quota) | [VL] Correct (Crossref). | none |
| Ref 45. Jarrow & Turnbull (1995), *JF* 50(1):53–85 | unchecked (quota) | [VL] Correct. | none |
| Ref 46. Duffie & Singleton (1999), *RFS* 12(4):687–720 | unchecked (quota) | [VL] Correct. | none |
| Ref 47. Ayache, Forsyth & Vetzal (2003), *J. Derivatives* 11(1):9–29 | unchecked (quota) | [VL] Correct. | none |
| Ref 48. Longstaff & Schwartz (2001), *RFS* 14(1):113–147 | found [CS-saved: streams 05, 08] | DOI 10.1093/rfs/14.1.113; 3,480 citations; Consensus venue label "The Finance". | [link](https://consensus.app/papers/details/80f7e4358bab534185c423e61ad9ce8e/?utm_source=claude_desktop) |
| Ref 49. Altman, Brady, Resti & Sironi (2005), *J. Business* 78(6) | found [CS-saved: VL] | DOI 10.1086/497044. Consensus lists 2003, the working-paper year; Crossref gives 78(6):2203–2228 (2005). The abstract supports the dossier's use: default rates play "a pivotal role" in recoveries. | [link](https://consensus.app/papers/details/4b638f0501945f7395fa9f005cdcc41f/?utm_source=claude_desktop) |
| Ref 50. Acharya, Bharath & Srinivasan (2007), *JFE* 85(3) | found [CS-saved: VL] | DOI 10.1016/j.jfineco.2006.05.011. The abstract supports the dossier: creditors recover significantly less when the defaulter's industry is in distress. | [link](https://consensus.app/papers/details/6b9770edca525bec9ae7167d872bfcd4/?utm_source=claude_desktop) |
| Ref 51. Kaplan & Strömberg (2003), *RES* 70(2):281–315 | unchecked (quota) | [VL] Correct. | none |
| Ref 52. Kaplan & Schoar (2005), *JF* 60(4):1791–1823 | found [CS-saved: stream 04] | *JF*, 366 citations; Consensus shows the SSRN DOI 10.2139/ssrn.473341. **Orphan:** never cited in the body (VL). | [link](https://consensus.app/papers/details/3eb9b802f17153de8190c3e72ac28aed/?utm_source=claude_desktop) |
| Ref 53. [K] Black & Cox (1976), *JF* 31(2) | unchecked (quota) | [VL] *JF* 31(2):**351–367**, DOI 10.1111/j.1540-6261.1976.tb01891.x. Upgrade from [K]. | none |
| Ref 54. [K] Tsiveriotis & Fernandes (1998), *JFI* 8(2) | unchecked (quota) | [VL] *Journal of Fixed Income* 8(2):**95–102**, DOI **10.3905/jfi.1998.408243**. Upgrade from [K]. | none |
| Ref 55. [K] Lando (1998), *RDR* 2 | unchecked (quota) | [VL] *Review of Derivatives Research* 2(2–3):**99–120**, DOI 10.1007/BF01531332. Upgrade from [K]. | none |
| §3.4 "Takahashi–Alexander" (via stream 04's RFT-TA); no entry | found [CS-saved: streams 04, 06, 08] | Takahashi & Alexander (2002), "Illiquid alternative asset fund modeling", *JPM* 28(2):90–100, DOI 10.3905/jpm.2002.319836; 68 citations; Consensus venue label "Unknown Journal". Add to §10. | [link](https://consensus.app/papers/details/da7ee2d8587e575f99e3a36a590d2be6/?utm_source=claude_desktop) |
| §6.8 "Geltner" de-smoothing; no entry | found [CS-saved: stream 04] | Geltner (1991), *JREFE* 4(3); 391 citations; DOI 10.1007/bf00161933. The dossier does not say which Geltner paper it means. Stream 04 cites 1991 (and 1993, which is unchecked). Add to §10. | [link](https://consensus.app/papers/details/fa03b920e943538884c1f281325a576b/?utm_source=claude_desktop) |
| §6.8 "GLM"; no entry | **not found** in Consensus [streams 04, 09] | Consensus returns only Getmansky's 2004 thesis, which carries the same abstract. WebSearch in streams 04 and 09 confirms *JFE* 74(3):529–609, DOI 10.1016/j.jfineco.2004.04.001 (NBER w9571). Add to §10. | thesis record: [link](https://consensus.app/papers/details/4e43d079332f5046860f2f39350f56f9/?utm_source=claude_desktop) |
| §4.6 "BGG-derived" smoothing ≈ 0.5/quarter; no entry | found [CS-saved: streams 04, 05, 06] | Brown, Ghysels & Gredil, "Nowcasting Net Asset Values: The Case of Private Equity". SSRN record 2020, DOI 10.2139/ssrn.3507873, 20 citations. Published in *RFS* 36(3):945–986 (2023), DOI 10.1093/rfs/hhac045 (stream 05 WebSearch). The abstract gives betas and total risk but no smoothing coefficient; the 0.5 is stream 04's derivation. | [link](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop) |
| §3.8 "Bühlmann credibility"; no entry | found [CS-saved: stream 04] | Bühlmann (1967), "Experience rating and credibility", *ASTIN Bulletin* 4(3); 67 citations; no DOI; the author name is garbled in the record. | [link](https://consensus.app/papers/details/5542fe373291540f857447d36cf464a8/?utm_source=claude_desktop) |
| §3.8 "Mack" development triangles; no entry | unchecked (ambiguous; quota) | No year or title. [Inference] Mack (1993, *ASTIN Bulletin*, chain-ladder standard errors) is the usual reference for development triangles; unverified. Stream 07 holds a different Mack record (2000, Benktander), which does not fit this use. | none |
| §4.7 "BIS work finds PE and private-credit deployment positively correlated with equity returns" | not identifiable | No author or title. VL A3: the IMF calls the evidence "mixed" and says fund lending is less procyclical than BDC lending. | none |
| Ref 40. IMF (Apr-2024), GFSR Ch. 2 | official report; outside the academic check | [VL] Content verified (F10). | none |

**Not tabulated.** Refs 1–39 (platform releases, filings, advisor and law-firm reports, press) are practitioner sources outside an academic check. The VL checked most of them.

---

## 3. Annotated bibliography (23 papers)

### 3.1 Return anchors and risk adjustment (B1–B4)

**B1. [Risk-Adjusting the Returns to Private Debt Funds](https://www.nber.org/papers/w32278)** (URL from the dossier; no Consensus record retrieved)
- **Record:** I. Erel, T. Flanagan & M. S. Weisbach · 2024 · NBER WP 32278 · citations n/a · DOI 10.3386/w32278 [VL]. In dossier: yes (ref 42).
- **Finding** (VL F7, read from the full text):
  - 532 USD funds, 1992–2015 vintages; average IRR 8.6%.
  - Risk-adjusted profit with equity and bond factors is about zero (GPME 0.041, t = 1.46).
  - Gross alpha of about 4.1% on a 65-fund subsample, with imputed fees of 3.1–3.9%.
- **Relevance to ADIC:** This is the anchor for "net alpha ≈ 0".
  - [Inference] The dossier's opportunity condition π_t > ℓ_t should use a factor-adjusted π_t, not a raw IRR. Use EFW's two-factor GPME as the default risk adjustment in the three-series fusion.

**B2. [Private Debt Fund Returns, Persistence, and Market Conditions](https://rpc.cfainstitute.org/research/financial-analysts-journal/2022/private-debt-fund-returns-persistence-market-conditions)** (URL from the dossier; no Consensus record retrieved)
- **Record:** P. Böni & S. Manigart · 2022 · *Financial Analysts Journal* 78(4):121–144 · citations n/a · DOI 10.1080/0015198X.2022.2092384. In dossier: yes (ref 43).
- **Finding** (VL F6, read from the published text):
  - 448 funds; mean net IRR 9.19%.
  - Performance is "highest when credit spreads expand ex ante and ex post, whilst TED spreads contract".
  - The ex-ante funding-illiquidity effect is "more than twice as large as that of performance persistence".
- **Relevance to ADIC:** The opportunity-hedge evidence cuts both ways.
  - [Inference] Condition expected vintage IRR (§3.6, §6.7) on HY OAS *and* a funding-liquidity variable, such as a TED-type spread. In an ADIC liquidity crisis both widen, so the net effect on new deployment is ambiguous.

**B3. [A Survey of Private Debt Funds](https://nber.org/papers/w30868)** [WS]
- **Record:** Block, Jang, Kaplan & Schulze (surnames as the search results give them) · 2024 · *Review of Corporate Finance Studies* 13(2):335–383 · citations n/a · DOI 10.1093/rcfs/cfae001 · NBER WP 30868. In dossier: no.
- **Finding** (abstract text in the search results):
  - Respondents mainly make cash-flow-based loans. They believe they finance companies and leverage levels that banks would not.
  - Direct-lending funds "target unlevered returns that appear high relative to their risk".
  - They use fund leverage, but appreciably less than banks and CLOs.
  - They negotiate both financial and incurrence covenants. A PE sponsor's presence helps them lend more and write more effective covenants.
  - European funds rely less on sponsors and compete more with banks.
  - **Discrepancies between versions:** AuM is over US$390bn in the journal and over US$300bn in the NBER version. One source gives 191 managers.
- **Relevance to ADIC:**
  - [Inference] This is an underwriting-side prior for the "underwritten" series (§6.8). Survey targets set high relative to risk support the dossier's haircut of underwritten returns, but they are targets, not realised returns.
  - Covenant package and sponsor presence belong as covariates in the PIK and default hazards (§3.2).

**B4. [Risk Adjustment in Private Equity Returns](https://consensus.app/papers/details/996d0a57b17957dd81fec3ac0698ec30/?utm_source=claude_desktop)** [CS-saved: stream 05, F14]
- **Record:** Arthur Korteweg · 2019 · *Annual Review of Financial Economics* · 37 citations · DOI 10.2139/ssrn.3293984. In dossier: no.
- **Finding:** This survey finds that risk-adjusted performance estimates vary substantially by method, period and data. VC net returns have been zero or negative since 2000.
- **Relevance to ADIC:**
  - [Inference] EFW's zero alpha comes from one method.
  - Report the Capital Solutions book's risk-adjusted returns under several kernels: EFW factors, plus the strip kernel of F12. Show the spread across kernels on IC cards instead of a single number.

### 3.2 Structured equity: valuation and priority (B5–B6)

**B5. [Squaring venture capital valuations with reality](https://ideas.repec.org/a/eee/jfinec/v135y2020i1p120-143.html)** [WS]
- **Record:** Will Gornall & Ilya Strebulaev · 2020 · *Journal of Financial Economics* 135(1):120–143 · citations n/a · DOI 10.1016/j.jfineco.2018.04.015. In dossier: no.
- **Finding** (abstract in the search results):
  - The authors build a valuation model for VC-backed companies and apply it to 135 US unicorns.
  - Reported post-money valuations average 48% above fair value; 14 are more than 100% above.
  - The main reason is that reported valuations assume all shares are as valuable as the most recently issued preferred.
- **Relevance to ADIC:**
  - [Inference] For family C, terms determine the value of a preferred claim and of the common beneath it: liquidation preference, seniority, ratchets and redemption rights. Marks keyed to the latest round price misstate both.
  - This supports the dossier's structural waterfall (§2.2, §3.3). Apply it to marks (the "current actual" series) as well as to pricing.
  - The 48% figure is specific to VC unicorns and is not a buyout parameter.

**B6. [Dynamic Investment, Capital Structure, and Debt Overhang](https://consensus.app/papers/details/c10673afc91154b6b87c6a1af1c7aa3a/?utm_source=claude_desktop)** [CS-saved: stream 08]
- **Record:** Suresh Sundaresan et al. · 2015 · *Review of Corporate Finance Studies* · 174 citations · DOI 10.2139/ssrn.952540. In dossier: no.
- **Finding:** Firms choose conservative leverage to limit debt overhang on future growth-option exercise. Debt seniority and priority structures have significant effects on exercise and leverage.
- **Relevance to ADIC:**
  - [Inference] Structured capital changes the issuer's incentives. A senior-ranking rescue claim, or a growing PIK accrual, adds overhang that can deter value-creating investment.
  - The anti-priming and priority terms in §4.3 therefore affect value; they are not legal boilerplate.
  - In a sensitivity run of the kicker model (§3.3), let the issuer's investment and exit policy respond to the priority structure.

### 3.3 Rescue, distressed and nonbank junior capital (B7–B10)

**B7. [Hedge Funds as Investors of Last Resort?](https://academicnewsletter.sufe.edu.cn/info/355168)** [WS] (working-paper version: [NBER w11011](https://www.nber.org/papers/w11011.pdf))
- **Record:** Brophy, Ouimet & Sialm · 2009 · *Review of Financial Studies* 22(2):541–574 · citations n/a · DOI 10.1093/rfs/hhl045. In dossier: no.
- **Finding** (search results):
  - Hedge funds fund PIPE issuers with weak fundamentals and high information asymmetry.
  - They protect themselves with steep discounts, repricing rights and short positions in the issuer's stock.
  - Over the next two years, issuers financed by hedge funds underperform issuers financed by other investors.
  - Securities with repricing rights are associated with poor post-issue performance.
- **Relevance to ADIC:** This is the closest academic analogue to rescue or structured equity in listed issuers, the Expedia type of deal.
  - [Inference] When capital is "last resort", the quality of deal flow falls. Rescue returns come from protective terms, not from the regime alone.
  - [Inference] Add an issuer-quality state, make protective terms an eligibility condition, and apply a larger haircut to the warrant kicker in rescue deals.

**B8. [Hedge Funds and Chapter 11](https://econbiz.de/Record/hedge-funds-and-chapter-11-jiang-wei/10010542353)** [WS]
- **Record:** Wei Jiang, Kai Li & Wei Wang · 2012 · *Journal of Finance* 67(2):513–560 · citations n/a · no DOI shown. In dossier: no.
- **Finding** (search results; 474 Chapter 11 cases, 1996–2007):
  - Hedge funds take positions in the capital structure where they can affect value most.
  - Their presence, especially as unsecured creditors, helps balance power between the debtor and secured creditors.
  - With the debtor, this shows up as higher probabilities of losing exclusive rights to file a plan, of CEO turnover and of adopting key-employee retention plans.
  - With secured creditors, it shows up as higher probabilities of emergence and higher payoffs to junior claims.
  - The paper defines loan-to-own: buying a distressed borrower's debt intending to convert it into a controlling equity stake at emergence.
- **Relevance to ADIC:**
  - [Inference] In family E, recovery depends on capital-structure position and on how active the creditor is. The workout branch (§3.1) should let recovery depend on position (secured or unsecured) and on a loan-to-own option.
  - Active-creditor tactics (contesting exclusivity, forcing CEO change) interact with the sovereign reputational limits in §8 and open question 9. The IC must decide whether ADIC will play that role.

**B9. [Why Do Firms Borrow Directly from Nonbanks?](https://nber.org/papers/w26458)** [WS]
- **Record:** Sergey Chernenko, Isil Erel & Robert Prilmeier · 2022 · *Review of Financial Studies* 35(11):4902–4947 · citations n/a · no DOI shown.
  - One index listing appends Gregor Matvos. [Inference] He is probably the handling editor; confirm the author list on the journal page.
  - In dossier: no.
- **Finding** (published abstract per the search results; hand-collected middle-market credit agreements, 2010–2015):
  - About a third of loans come directly from nonbanks.
  - Two-thirds of nonbank lending is attributed to bank regulation that limits lending to unprofitable, highly levered borrowers.
  - Firms with negative EBITDA or debt/EBITDA above 6 are more likely to borrow from nonbanks, and pay higher rates.
  - **Not confirmed in the final version:** earlier drafts and talk slides report that nonbank loans are 37% less likely to carry financial covenants and more likely to carry warrants. The NBER WP gives a 190bp rate premium.
- **Relevance to ADIC:**
  - [Inference] This grounds the dossier's family-D boundary: junior capital with kickers goes to unprofitable or highly levered borrowers.
  - The regulatory driver means bank-regulation regimes, such as the Basel endgame in §8, shift deal flow. A bank-appetite state belongs in Λ_D and in the BankShare pricing term (§3.6).

**B10. [Private Equity and Financial Fragility during the Crisis](https://academicnewsletter.sufe.edu.cn/info/352739)** [WS] (working paper: [NBER w23626](https://www.nber.org/papers/w23626.pdf))
- **Record:** Bernstein, Lerner & Mezzanotti · 2019 · *Review of Financial Studies* · citations n/a · DOI 10.1093/rfs/hhy078.
  - One Kellogg page gives a different title, "Private Equity, Financial Strategy, and the Crisis"; confirm on rerun.
  - The search results describe UK evidence.
  - In dossier: no.
- **Finding** (search results):
  - In 2008, PE-backed companies cut investment less than peers. They had greater equity and debt inflows, higher asset growth and gained market share.
  - The effects were stronger for financially constrained firms and where the PE investors had more resources at the start of the crisis.
  - PE firms reported spending more time with portfolio companies.
- **Relevance to ADIC:**
  - [Inference] For sponsor-backed positions in families C and D (and fund-level family A), sponsor resources belong as a covariate in the PIK, default and recovery models (§3.2). The flat crisis default rate of 6–8% in §6.7 should be conditioned on them.
  - [Inference] In a long DPI drought, sponsors' own resources shrink. The support channel weakens just as the book enters its PIK phase.

### 3.4 GP economics: GP stakes, GP-commitment and management-company loans (B11–B14)

**B11. [The Economics of Private Equity Funds](https://ideas.repec.org/a/oup/rfinst/v23y2010i6p2303-2341.html)** [WS]
- **Record:** Metrick & Yasuda · 2010 · *Review of Financial Studies* 23(6):2303–2341 · citations n/a · DOI 10.1093/rfs/hhq020. In dossier: no.
- **Finding** (published abstract per the search results; 238 funds from one large PE investor):
  - About two-thirds of expected revenue comes from fixed components that are not sensitive to performance.
  - Buyout managers grow their funds faster, which the authors link to a more scalable business.
  - The working paper gave about 60%.
- **Relevance to ADIC:**
  - [Inference] A GP stake (#4) is mostly a claim on fee streams scaled by fundraising, plus a smaller performance option (carry).
  - Decompose the dossier's "cash yield 6–8% + growth" into a fee-related-earnings (FRE) stream (fee rate × fee-paying AUM, with step-downs) and a carry option.

**B12. [Pay for Performance from Future Fund Flows: The Case of Private Equity](https://ideas.repec.org/a/oup/rfinst/v25y2012i11p3259-3304.html)** [WS]
- **Record:** Ji-Woong Chung, Berk A. Sensoy, Léa Stern & Michael S. Weisbach · 2012 · *Review of Financial Studies* 25(11):3259–3304 · citations n/a · DOI 10.1093/rfs/hhr141 · NBER WP 16369. In dossier: no.
- **Finding** (search results):
  - A GP's pay depends on the current fund's results in two ways: directly, through carry; and indirectly, through the ability to raise later funds.
  - A learning model estimates the indirect channel at roughly the size of carry.
  - It is stronger for buyout than VC and weakens across successive funds.
- **Relevance to ADIC:**
  - [Inference] A GP stake's terminal value is the present value of future funds' fees, which depends on current performance and the fundraising market. GP stakes therefore load on the same performance and exit factor as ADIC's PE book.
  - GP-commitment and management-company loans (#3) repay from the same fees and carry.
  - Treat all of these as concentration in the GP, not diversification.

**B13. [Interim Fund Performance and Fundraising in Private Equity](https://consensus.app/papers/details/6ade780e2b3255ce9dd77db1dba5940c/?utm_source=claude_desktop)** [CS-saved: stream 05, F11]
- **Record:** Brad M. Barber et al. · 2017 · *Journal of Financial Economics* · 113 citations · DOI 10.1016/j.jfineco.2017.01.001. In dossier: no.
- **Finding:** GPs time fundraising to performance peaks. Low-reputation GPs show signs of NAV management.
- **Relevance to ADIC:**
  - [Inference] NAV-loan covenants (§3.4) test reported NAV, which may be inflated when the borrower's GP is fundraising. Apply a fundraising-window haircut.
  - GP-stake valuations that rely on current fund marks need the same correction.

**B14. [Do private equity funds manipulate reported returns?](https://consensus.app/papers/details/3331159853ab59dea783df670c91ee0a/?utm_source=claude_desktop)** [CS-saved: stream 05, F10]
- **Record:** Gregory W. Brown et al. · 2019 · *Journal of Financial Economics* · 90 citations · DOI 10.3386/w22493. In dossier: no.
- **Finding:** Some under-performing funds boost reported returns during fundraising; top performers likely understate theirs.
- **Relevance to ADIC:** [Inference] Use it, with B13, to build a NAV-quality flag for NAV-loan collateral and for the pricing service's "GP tier" feature (§6.10).

### 3.5 Fund-finance collateral: fund debt and NAV measurement (B15–B17)

**B15. [Distorting Private Equity Performance: The Rise of Fund Debt](https://consensus.app/papers/details/84b7e9e9b66151e78637a4ebfac077ae/?utm_source=claude_desktop)** [CS-saved: streams 05, 06]
- **Record:** James F. Albertus et al. · 2020 · SSRN · 4 citations · DOI 10.2139/ssrn.3410076. In dossier: no.
  - Probable published successor: [Private Equity Fund Debt: Agency Costs and Cash Flow Management](https://consensus.app/papers/details/d658bfc490c45ecf9e5985e72653204e/?utm_source=claude_desktop) (Albertus et al., 2026, *JFQA*, DOI 10.1017/s0022109026102890). It has no abstract; see U3.
- **Finding:** Funds that use subscription lines call less capital and show large distortions in timing-sensitive performance measures. They are disproportionately poor performers and earn more carried interest.
- **Relevance to ADIC:**
  - [Inference] For family A lending and for the pricing service, subscription-line use is a borrower-quality signal.
  - Sub-line repayments sit ahead of the distributions that sweep a NAV loan. Layered fund leverage (sub line + NAV loan) raises the effective LTV.

**B16. [Nowcasting Net Asset Values: The Case of Private Equity](https://consensus.app/papers/details/0dd5620268c750e8a1db83a9bf0efc44/?utm_source=claude_desktop)** [CS-saved: streams 04, 05, 06]
- **Record:** Gregory W. Brown et al. · 2020 (SSRN record) · 20 citations · DOI 10.2139/ssrn.3507873. Published in *RFS* 36(3):945–986 (2023), DOI 10.1093/rfs/hhac045 (stream 05 WebSearch). In dossier: body mention only (§4.6, "BGG-derived").
- **Finding:**
  - The method gives weekly unsmoothed NAVs for individual funds and beats extrapolation.
  - Average buyout beta about 1.0 and VC 1.4; total risk 33% a year for buyout and 40% for VC.
  - Risk-taking and reporting quality persist by manager.
- **Relevance to ADIC:**
  - [Inference] NAV-loan pools are often a few funds, so collateral volatility is near fund-level, far above portfolio-level marks.
  - Test the LTV chance constraint (#2) and the pool model (§3.4) on nowcast NAV, while covenants still run on reported NAV.
  - Stream 05 notes that the RFS numbers may differ from the working-paper numbers.

**B17. [Private Equity Net Asset Values and Future Cash Flows](https://consensus.app/papers/details/44d91cea6b8b53b481621e6ed4e6ef9e/?utm_source=claude_desktop)** [CS-saved: stream 05, B13]
- **Record:** Tim Jenkinson et al. · 2019 (print 2020) · *The Accounting Review* · 31 citations · DOI 10.2308/accr-52486. In dossier: no.
- **Finding:** The sample is 384 VC and 195 buyout funds, 1988–2016. Buyout NAVs show little systematic bias against discounted realized cash flows. VC NAVs are relatively aggressively biased, especially since 2000.
- **Relevance to ADIC:** [Inference] Give NAV-based advance rates and the REFINANCE quote function a strategy-specific NAV-bias haircut for VC- and growth-heavy pools. This applies to third-party loans and to pricing ADIC's own PE book.

### 3.6 Opportunity set: fire sales, dry powder, funding liquidity (B18–B21)

**B18. [Fire Sales in Finance and Macroeconomics](https://consensus.app/papers/details/38094184238d5f8f9fe8944a05e37411/?utm_source=claude_desktop)** [CS-saved: stream 05, B20]
- **Record:** A. Shleifer et al. · 2011 · *Journal of Economic Perspectives* · 700 citations · DOI 10.1257/jep.25.1.29. In dossier: no.
- **Finding:** Fire sales are forced sales in which high-valuation bidders are sidelined, usually because debt overhang hits many specialist bidders at once. They cause undervaluation, downward spirals and failed arbitrage.
- **Relevance to ADIC:** [Inference] Make the opportunity premium in §3.6 a function of how impaired the specialist capital is, not only a regime dummy. Competitors' leverage (BDCs, levered funds) and redemption pressure become state variables.

**B19. [Fear of Fire Sales, Illiquidity Seeking, and Credit Freezes](https://consensus.app/papers/details/a6c668ff8cfe5396bed107c465c18632/?utm_source=claude_desktop)** [CS-saved: stream 05, B23]
- **Record:** Douglas W. Diamond et al. · 2011 · *Quarterly Journal of Economics* · 571 citations · DOI 10.1093/qje/qjr012. In dossier: no.
- **Finding:** An overhang of institutions that may be forced to sell later raises the private return to holding illiquid assets. Cash-rich buyers who expect fire sales earn high expected returns on cash, so they lock up less in term loans.
- **Relevance to ADIC:**
  - [Inference] This challenges C2 (Section 5, row 1). In the deploy-versus-wait comparison, the return to waiting is endogenous to expected fire sales.
  - It also explains why term lending such as NAV loans freezes in stress: competitors lock up less, so spreads widen.

**B20. [Do Asset Fire Sales Exist? An Empirical Investigation of Commercial Aircraft Transactions](https://consensus.app/papers/details/1f12c0aa9d425ed1b582ce98535bd082/?utm_source=claude_desktop)** [CS-saved: stream 08]
- **Record:** Todd C. Pulvino · 1998 · *Journal of Finance* · 670 citations · DOI 10.1111/0022-1082.00040. In dossier: no.
- **Finding:** Financially constrained airlines get lower prices than unconstrained rivals and sell to industry outsiders more often in downturns. Unconstrained airlines step up buying when prices are depressed.
- **Relevance to ADIC:** [Inference] The opportunity channel is real for unconstrained buyers. Whether ADIC is unconstrained depends on Corporate Finance's buffer, which links the opportunity hedge to the liquidity gate.

**B21. [Market liquidity and funding liquidity](https://consensus.app/papers/details/7c944d8f27a65feea50c7b83eea8e1e3/?utm_source=claude_desktop)** [CS-saved: stream 05, B21]
- **Record:** M. Brunnermeier et al. · 2009 · *Review of Financial Studies* · 5,153 citations · DOI 10.1093/rfs/hhn098. In dossier: no.
- **Finding:** Funding (capital and margins) depends on market liquidity, and market liquidity depends on funding. Margins can destabilize and create liquidity spirals. Liquidity dries up suddenly, moves together across assets and flees to quality.
- **Relevance to ADIC:** [Inference] Back-leverage on the Capital Solutions book (REFINANCE and LEVER, §6.11) faces state-dependent haircuts. Fixed advance rates and fixed LTV triggers (§5.6 D) understate breach risk; this adds to VL R2.

### 3.7 Structured exits of the book (B22–B23)

**B22. [The Economics of Structured Finance](https://consensus.app/papers/details/89f1ef7a5962598bb7ec8c607c0eee2a/?utm_source=claude_desktop)** [CS-saved: stream 05, B19]
- **Record:** No authors shown ("N/A"); *Journal of Economic Perspectives* 23(1):3–25 (Winter 2009) · 472 citations · no DOI shown.
  - Stream 05 attributes it to Coval, Jurek and Stafford from general knowledge; the record does not confirm this.
  - In dossier: no.
- **Finding:** Senior tranches are much safer than the average collateral only if default risk and correlation are estimated precisely. Issuing a capital structure amplifies errors in evaluating the underlying risk.
- **Relevance to ADIC:** [Inference] For rated feeders and CFOs (#12, REFINANCE): add correlation-stressed rating migration and a model-risk spread by regime.

**B23. [CLO Performance](https://consensus.app/papers/details/c712f36af0415b9488a4a6e63c8facb8/?utm_source=claude_desktop)** [CS-saved: stream 05, F17]
- **Record:** Larry Cordell et al. · 2020 · Philadelphia Fed WP · 17 citations · DOI 10.2139/ssrn.3652124. In dossier: no.
- **Finding:** CLOs add value by easing regulatory constraints. CLO equity is resilient to volatility because of long-term funding.
- **Relevance to ADIC:** [Inference] For the book's own leverage, term-matched funding that is not marked to market (a CFO-style structure) is more robust than mark-to-market facilities. Weigh this against B22's model risk.

---

## 4. Missed-but-important papers: design implications

Every item is **[Inference]** unless it paraphrases a cited record. Ownership follows the user-confirmed organization:
- Capital Solutions owns asset-level proposals.
- Corporate Finance owns ℓ, portfolio-level facilities and the liquidity gate.

### 4.1 State variables (new or refined)

| State | Definition | Feeds | Source |
|---|---|---|---|
| GP fundraising state $g^{GP}_{j,t}$ | Months since last close; raised vs target; interim quartile of the current fund | GP-stake FRE and terminal value; GP-commitment and management-company loan PD; NAV-quality flag | B11, B12, B13, B14 |
| Sponsor resources $R^{sp}_{k,t}$ | Sponsor dry powder relative to portfolio size; fund age | PIK, default and recovery hazards for sponsor-backed C, D and A positions | B10, B3 |
| Borrower-fund leverage stack | Subscription-line balance + NAV loan + GP-level leverage | Effective LTV of a NAV loan; timing of sweep cash | B15 |
| NAV-quality vector | Strategy mix (VC share); fundraising window; manager reporting persistence; nowcast vs reported NAV | LTV on adjusted NAV; quote-function features | B13, B14, B16, B17 |
| Issuer quality and information asymmetry $q_i$ | Negative EBITDA; debt/EBITDA > 6; opacity; distress features | Rescue eligibility; kicker haircut; PD prior | B7, B9 |
| Specialist-capital state $K^{spec}_t$ | Leverage, dry powder and redemption pressure of competing hybrid and distressed capital; BDC discounts; bank appetite | Opportunity pricing $s_{f,t}$; deal flow $\Lambda_f$ | B18, B19, B20, B9 |
| Funding-liquidity state $f_t$ | TED-type spread | Vintage-IRR model; back-leverage haircuts | B2, B21 |
| Contract-term vector $\tau_i$ | Liquidation preference, seniority rank, participation, ratchets or repricing, redemption rights, anti-priming | Waterfall marks; issuer-behaviour sensitivity | B5, B6, B7 |
| Workout role $w_i$ | Secured or unsecured; passive or active creditor; loan-to-own option | Position-dependent recovery in the workout branch | B8 |

### 4.2 Models
1. **GP-stake engine (new).**
   - FRE: $FRE_{j,t}=f_j\cdot AUM^{fee}_{j,t}$.
   - AUM grows through a fundraising hazard $h^{raise}_{j,t}=h(\text{interim performance},\ x_t,\ \text{fundraising market})$, linked to the same PE exit factor $x_t$ that drives distributions.
   - Carry is an option on fund performance. Terminal value is the present value of future funds' FRE.
   - Calibrate the fixed:variable revenue split to about 2:1 (B11) and the indirect incentive to about the size of carry (B12).
   - This replaces the dossier's flat "cash yield + growth" row.
2. **Term-aware marking.** Value each structured-equity position jointly with the issuer's other share classes, using the §2.2 waterfall on simulated V paths. Compare with headline or last-round marks; the gap becomes a valuation-risk flag in the "current actual" series (B5).
3. **Adverse-selection layer in the opportunity model.** In crisis, $\Lambda_E$ rises but the issuer-quality distribution shifts down. Deal value is the term-protected payoff under the worse distribution (B7).
4. **Position-dependent workout recovery.** $\text{LGD}\sim\text{Beta}(\mu(\text{seniority},S_t,\text{Cov},w_i),\phi)$, with a loan-to-own branch that converts the claim to equity at emergence (B8). Calibrate when ADIC workout history is available.
5. **Fire-sale pricing process.** Keep entry pricing and realised return separate.
   - **Entry spread:** extend §3.6 to $s_{f,t}=s_{f,0}+s_{f,1}\text{OAS}^{HY}_t+s_{f,2}\mathbb 1\{\text{drought}\}+s_{f,3}\text{BankShare}_t+s_{f,4}\,\text{Impair}(K^{spec}_t)$. The new impairment term means natural buyers are sidelined (B18–B20).
   - **Expected vintage return:** $\mathbb E[r_{f,t}]=g(s_{f,t})-\mathbb E[\text{loss}_{f}\mid S_t]-d\,f_t$, where the last term is the funding-liquidity drag (B2).
6. **Back-leverage haircut function.** Use an advance rate $a_t=a_0-a_1\sigma_t-a_2\,\text{illiq}_t$, and test LTV triggers and cure needs on it rather than on a fixed advance rate (B21).
7. **Multi-kernel risk adjustment.** EFW two-factor GPME as baseline, with the strip kernel (F12) and others as challengers. Report the spread across kernels (B1, B4).
8. **CFO and rated-feeder exit.** Model tranches under correlation stress (B22). Consider term funding as an alternative to mark-to-market back-leverage (B23).

### 4.3 Parameter priors (literature values, not ADIC data)

| Parameter | Prior | Source | Caveat |
|---|---|---|---|
| Fixed share of expected GP revenue | ≈ 2/3 (published; WP ≈ 60%) | B11 | One LP's 238 funds; pre-2010 terms |
| Indirect (future-fund) pay relative to carry | ≈ 1:1; higher for buyout, lower for later funds | B12 | Model-based estimate |
| Headline vs fair value of late-stage VC | +48% on average; 14 of 135 above +100% | B5 | VC unicorns only; not buyout structured equity |
| Nonbank borrower profile and price | Negative EBITDA or debt/EBITDA > 6; premium ≈ 190bp (WP) | B9 | Final RFS figure not confirmed |
| Private-debt fund net IRR; risk-adjusted profit | 9.19% mean (BM); 8.6% (EFW); risk-adjusted profit ≈ 0 (EFW) | B1, B2 | Vintages to 2015–18, before the high-rate regime |
| Funding-illiquidity effect on fund returns | Ex-ante TED effect > 2× persistence | B2 (VL) | Sign: negative |
| Fund-level beta / total risk | Buyout 1.0 / 33%; VC 1.4 / 40% a year | B16 | WP numbers |
| Fire-sale discount, minority stakes | ≈ 8%; 13–14% for blocks or stakes > 5% | F2 | Listed minority stakes |
| Discount for unlisted targets | 15–30%, larger when the parent is constrained | F1 | M&A setting |
| PE liquidity-risk premium | ≈ 3% a year | F3 | Applies by analogy to sponsor-adjacent claims |

### 4.4 Constraints
1. **GP aggregate (upgrade of constraint #4).** Count GP stakes, GP-commitment and management-company loans, and fund finance to a GP's funds alongside ADIC's LP NAV in that GP. Stress them together under a fundraising freeze (B11, B12).
2. **Rescue eligibility.** Require protective terms: minimum return or MOIC, repricing or ratchet, anti-priming, hedgeability. Cap exposure to high-$q_i$ (opaque, weak) issuers (B7).
3. **NAV-loan LTV on adjusted NAV.** Use nowcast NAV with a VC-bias haircut and a fundraising-window haircut (B13, B14, B16, B17).
4. **Layered leverage.** Include the borrower's subscription lines in NAV-loan effective LTV and covenant headroom (B15).
5. **State-dependent back-leverage haircuts.** Run the monthly trigger test on stressed advance rates (B21). Combine with VL R2's cash-carry constraint.
6. **Deployment pace.** Cap the pace when the group's dry powder ages. This is by analogy only: secondary buyouts made under pressure to spend underperform (F9).

### 4.5 Objectives and shadow prices
1. **Risk-adjusted π_t.** The opportunity condition π_t > ℓ_t should use factor-adjusted excess returns, reported across kernels (B1, B4). This is VL R4's fix, now with literature support.
2. **Dry-powder value endogenous to the fire-sale state.** Replace C2's fixed crisis IRR with the §4.2(5) process and a state-dependent ℓ (B18–B20; VL R1).
3. **Cross-check on ℓ for Corporate Finance.** The spread between collateralized and uncollateralized funding is an observable proxy for the shadow cost of capital (F5). Compare it with the optimizer's ℓ, which is Corporate Finance's transfer-pricing curve.
4. **GP-stake objective term.** Score GP stakes by the LAPV of FRE plus carry under the shared kernel, with an explicit correlation to the PE exit factor, so that LAPV captures the concentration (B12).

### 4.6 Agent and IC design
1. **Valuation agent.** Re-mark structured equity with the waterfall, and flag gaps against headline or round-price marks (B5).
2. **Underwriting challenge (red-team) agent.** Applies reference-class priors to group forecasts until ADIC's own data calibrate them:
   - survey targets are high relative to risk (B3);
   - last-resort issuers underperform (B7);
   - private-debt net alpha is about zero (B1).
3. **GP-exposure and conflict agent.**
   - Aggregates exposure per GP across PE, Secondaries, Co-investment and Capital Solutions, including GP stakes and GP loans (B12).
   - Checks GP-consent and transfer limits on LP-portfolio financings (F7; VL R3).
4. **Treasury (Corporate Finance) seat.**
   - Owns ℓ, the funding-liquidity state $f_t$ and back-leverage terms.
   - Dry-powder release rules reference the fire-sale state (B19, B20).
5. **IC cards.**
   - **GP-stake card:** fixed vs variable revenue, fundraising dependence, correlation with ADIC's PE book.
   - **Rescue card:** issuer-quality score, protective terms, adverse-selection prior, and the intended Chapter 11 role (B8), against the reputational limits.

### 4.7 Further relevant saved records (compact)

All are saved Consensus records from sibling streams. The findings are as those files record the abstracts.

| # | Paper | Record (Consensus) | Finding (abstract) | Use in G3 |
|---|---|---|---|---|
| F1 | [The price of corporate liquidity: Acquisition discounts for unlisted targets](https://consensus.app/papers/details/6f3ed8f7e26c50d29022453169f85362/?utm_source=claude_desktop) | Micah S. Officer · 2007 · *JFE* · 457 cit. · DOI 10.1016/j.jfineco.2006.01.004 | Unlisted targets sell at 15–30% discounts, larger when parents are liquidity-constrained and debt is expensive | Constrained-seller discounts feed opportunity pricing; ADIC's own SELL and REFINANCE costs move together |
| F2 | [Fire sale discount: Evidence from the sale of minority equity stakes](https://consensus.app/papers/details/ee77045e07675a659c38a6f8264d43a1/?utm_source=claude_desktop) | Serdar Dinç et al. · 2017 · *JFE* · 17 cit. · DOI 10.2139/ssrn.2627404 | Distressed-sale discount about 8%; 13–14% for blocks or stakes above 5%; prices recover | SELL haircut for minority structured stakes and GP stakes |
| F3 | [Private Equity Performance and Liquidity Risk](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop) | Francesco Franzoni et al. · 2012 · *JF* · 251 cit. · DOI 10.1111/j.1540-6261.2012.01788.x | PE loads on the liquidity risk factor; premium about 3% a year; funding-liquidity channel | Liquidity-factor loading for sponsor-adjacent claims [Inference] |
| F4 | [Valuing Private Equity](https://consensus.app/papers/details/15cb135a45b35616b82e97bf090f24ae/?utm_source=claude_desktop) | M. Sørensen et al. · 2013 record · *RFS* · 110 cit. · DOI 10.1093/rfs/hhu013 | Fees, carry and illiquidity are costly; LPs may only break even net of them | Consistent with EFW; fees absorb gross alpha in third-party hybrid funds |
| F5 | [Margin-Based Asset Pricing and Deviations from the Law of One Price](https://consensus.app/papers/details/c5d81d132abf5d118a3a62c20200c195/?utm_source=claude_desktop) | Nicolae Gârleanu et al. · 2011 · *RFS* DOI 10.1093/rfs/hhr027 · 663 cit. | Required returns depend on beta and margin; collateralized-uncollateralized spread captures the shadow cost of capital | Corporate Finance cross-check on ℓ; pledge high-advance-rate assets first |
| F6 | [Hidden in Plain Sight—The Impact of Undrawn Commitments](https://consensus.app/papers/details/d99e5eff8f48558898b24269df59ba18/?utm_source=claude_desktop) | T. Meyer · 2020 · DOI 10.3905/jai.2020.1.101 · 2 cit. | Uncalled capital carries risk and opportunity cost; treat the LP's uncalled capital as a loan against the fund | Pricing hybrid NAV-plus-uncalled facilities (family A) |
| F7 | [The Illiquidity Puzzle: Theory and Evidence from Private Equity](https://consensus.app/papers/details/490b5722c3535ebe9382df360741067d/?utm_source=claude_desktop) | Josh Lerner et al. · 2004 · *JFE* · 257 cit. · DOI 10.1016/s0304-405x(03)00203-4 | GPs use transfer restrictions to screen for deep-pocket LPs | GP consent for LP-portfolio preferred and NAV loans (family G; VL R3); signalling cost of ADIC's own REFINANCE |
| F8 | [Capital Commitment](https://consensus.app/papers/details/16b6f25d3dc55ab1bc41b977c5deccf8/?utm_source=claude_desktop) | Elise Gourier et al. · 2024 (SSRN record) · 8 cit. · DOI 10.2139/ssrn.2490430; *JF* 79(5):3407–3457 | Investors pay more to adjust committed amounts than to remove tradability frictions; commitment risk premia rise with secondary liquidity | Value of the book's US$1.2bn unfunded and of standby-capacity rights |
| F9 | [On Secondary Buyouts](https://consensus.app/papers/details/7bf7597e234759c785c4d2057d100202/?utm_source=claude_desktop) | François Degeorge et al. · 2016 · *JFE* · 91 cit. · DOI 10.2139/ssrn.2329202 | Buyouts made by buyers under pressure to spend underperform | Deployment-pace constraint in a crowded market (analogy) |
| F10 | [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop) | Taylor D. Nadauld et al. · 2019 · *JFE* · 66 cit. · DOI 10.1016/j.jfineco.2018.11.007 | Buyers' PME 1.023 vs sellers' 0.976, about 5 pp a year | Prior for the cost of credit-secondary SELL (analogy from PE LP interests) |
| F11 | [Liquidity Provision in the Secondary Market for Private Equity Fund Stakes](https://consensus.app/papers/details/b314a37976145a1c8b49352121998821/?utm_source=claude_desktop) | R. Albuquerque et al. · 2018 · SSRN · 11 cit. · DOI 10.2139/ssrn.3182481 | Discount variation tracks liquidity provision, not future NAV returns | Credit-secondary price as a liquidity-supply state |
| F12 | [Valuing Private Equity Investments Strip by Strip](https://consensus.app/papers/details/a07fbcfb0fdd5d5891ce4d67340cbeb8/?utm_source=claude_desktop) | Arpit Gupta et al. · 2021 · *JF* · 24 cit. · DOI 10.1111/jofi.13073 | Strip-replication kernel; negative risk-adjusted profit in most PE categories | Common kernel for the LAPV of Capital Solutions positions; multi-kernel check |

### 4.8 Identified but not assessable (no abstract in Consensus)

These records bear on the instruments, but Consensus held no abstract for them, so I report no findings. They are carried over from stream 05.

| # | Record | Why it matters |
|---|---|---|
| U1 | [Net Asset Value Financing and Private Equity](https://consensus.app/papers/details/f457b903aae95a57844b6cd41904b1d7/?utm_source=claude_desktop) · Colleen M. Baker · 2024 · SSRN · DOI 10.2139/ssrn.4851709 · 1 cit. | One of very few academic treatments of NAV financing (family A) |
| U2 | [Private Equity and Net Asset Value Debt - Ticking Time Bomb or Ticking All the Right Boxes](https://consensus.app/papers/details/dfec35a563a150b0ac00b68fa35ab87d/?utm_source=claude_desktop) · B. Reddy · 2024 · SSRN · DOI 10.2139/ssrn.4838394 · 0 cit. | NAV-debt risk assessment |
| U3 | [Private Equity Fund Debt: Agency Costs and Cash Flow Management](https://consensus.app/papers/details/d658bfc490c45ecf9e5985e72653204e/?utm_source=claude_desktop) · Albertus et al. · 2026 · *JFQA* · DOI 10.1017/s0022109026102890 | Probable published version of B15 |
| U4 | [Collateralized Fund Obligations: A Liquidity Solution for Private Equity](https://consensus.app/papers/details/b729a0a107fc586b91a375dcb370076f/?utm_source=claude_desktop) · Hoku Eggertsen · 2025 · SSRN · DOI 10.2139/ssrn.5229406 · 0 cit. | CFOs as an exit or REFINANCE route for the book (#12) |

---

## 5. Papers that challenge the dossier's recommendations

| # | Paper(s) | What it challenges in the dossier | Why | Recommended change |
|---|---|---|---|---|
| 1 | B19 Diamond–Rajan; B18 Shleifer–Vishny; B20 Pulvino | **§1.6 "The catch" and §5.6 C2:** "Holding idle dry powder for the 'hedge' does not pay." | C2 fixes expected IRRs exogenously at 11/13/16% in the normal, drought and crisis states. In fire-sale states the return to cash is endogenous and can be high for unconstrained buyers (B19); natural buyers are sidelined by overhang (B18); unconstrained buyers step in (B20). Separately, VL R1 shows C2 holds ℓ flat for four years. | Replace fixed crisis IRRs with the §4.2(5) fire-sale process and a state-dependent ℓ, then recompute deploy-versus-wait. Keep the dossier's rule of funding from low-ℓ sources. Present the result to the IC conditionally. |
| 2 | B2 Böni–Manigart (TED result, via VL); B7 Brophy et al. | **§6.7 crisis vintage IRR of 14–18% net; §3.6 pricing driven by HY OAS only.** | Funding illiquidity lowers private-debt fund returns by more than twice the persistence effect (B2). Last-resort capital meets adversely selected issuers and earns its return through protective terms (B7). | Add a funding-liquidity term and an issuer-quality shift. Make crisis IRRs depend on terms. Label 14–18% optimistic [I], as VL R4 also asks. |
| 3 | B11 Metrick–Yasuda; B12 Chung et al. | **§6.6 #4 GP stake:** cash yield 6–8%, growth with AUM, target net 12% (BXGP), with no fundraising risk. | GP value is mostly fees scaled by fundraising, and indirect future-fund pay is about the size of carry. [Inference] GP stakes are therefore levered to the same performance and fundraising cycle as ADIC's DPI drought. | Build the GP-stake engine in §4.2(1). Include GP stakes in the GP aggregate (§4.4(1)). Stress FRE and carry in a drought. |
| 4 | B5 Gornall–Strebulaev | **§6.8 "current actual" corrections** (de-smoothing, PIK haircut, probability-weighted floors). | When preferred terms are strong, headline round prices misvalue share classes. The correction list omits this term-driven error. | Add term-aware re-marking (waterfall) as a fourth correction, with a gap flag in IC materials. |
| 5 | B10 Bernstein et al. | **§6.7 crisis default of 6–8% and recovery multiplier of 0.7, applied uniformly.** | In 2008, sponsor-backed firms received equity and debt inflows, more so where sponsors had resources. | Condition crisis hazards and recoveries on sponsor resources. Also run the adverse case, in which a long DPI drought has already depleted sponsors. |
| 6 | B16 BGG; B17 Jenkinson et al.; B13 Barber–Yasuda; B14 Brown et al. | **§6.6 #1 senior NAV loan** (LTV 10–15%, PD 0.5%, LGD 20%) and §3.4, both on reported NAV. | Fund-level risk is 33–40% a year; VC NAVs are aggressively biased; NAVs may be inflated around fundraising. | Compute LTV on adjusted NAV, with strategy and fundraising-window haircuts. Widen the PD and LGD ranges for VC- or growth-heavy pools. |
| 7 | B21 Brunnermeier–Pedersen | **§5.6 D and §6.11 LEVER:** fixed 50% trigger; D/E 0.5 with a 33% cushion. | Margins and haircuts depend on volatility and liquidity, and spirals form. Fixed-haircut breach probabilities are biased low. | Use state-dependent haircuts (§4.2(6)). Recompute cushions alongside VL R2's loss- and cash-adjusted RoE. |

**Confirmations, not challenges**
- B3 (high return targets) and B1 (zero net alpha) support the dossier's §6.8 view that underwritten returns are optimistic. The dossier's "−4 to 6 pp" prior is still unsourced as an underwriting gap (VL R5).
- B9 supports the family-D boundary rule (junior debt with a kicker goes to Capital Solutions) and the BankShare competition term.

---

## 6. Verbatim usage message

Consensus returned this message on all three attempts. It is a monthly-quota rejection, not a rate limit:

> You've used all 500 included searches this month; resets on November 1st. Enable additional usage in your Consensus account to continue, or contact us if you need more: https://consensus.app/contact/

---

## 7. Scope notes and rerun plan

### Searches made
- **Consensus:** 3 attempts on one query (the EFW title), 30 seconds apart. All were rejected by the monthly quota, so **0 searches completed**. No filters were used and no thread tools were called.
- **WebSearch, 8 queries.** Each confirmed the metadata of one paper Consensus could not resolve today: B3, B5, B7, B8, B9, B10, B11 and B12.
  - The findings for these eight come only from the abstract text in the search results.
  - Inconsistencies between versions are flagged in each entry:
    - B3: AuM and sample size differ between versions.
    - B9: the warrants result is in drafts only, and one listing adds an extra author.
    - B10: an alternative title appears on one Kellogg page.
- **Saved records:** 37 distinct Consensus records from sibling literature files (streams 04, 05, 06 and 08) and the VL. URLs are copied exactly; I re-ran none of them.
  - Stream 09 is cited only for its WebSearch confirmation of GLM.

### What I did not do
- No new Consensus retrieval, so this run produced no new seminal works, 2022–2026 papers, meta-analyses or surveys beyond those listed.
- I did not read full texts. Findings are at abstract level, or VL full-text readings for B1 and B2.
- I did not check practitioner references.

### Rerun plan (after 1 November 2026, one query at a time, no filters)
1. **Citation look-ups (12).** Each of these titles:
   - Erel–Flanagan–Weisbach; Böni–Manigart; Cai–Haque (FEDS Notes may not be indexed);
   - Merton 1974; Jarrow–Turnbull 1995; Duffie–Singleton 1999; Ayache–Forsyth–Vetzal 2003;
   - Kaplan–Strömberg 2003; Black–Cox 1976; Tsiveriotis–Fernandes 1998; Lando 1998;
   - Mack chain-ladder standard error.
   - Also re-search B3, B5 and B7–B12 to obtain Consensus URLs and citation counts.
2. **Backfill (14).**
   - The five seeds:
     - "preferred equity private companies returns";
     - "mezzanine financing returns";
     - "structured equity hybrid securities valuation";
     - "GP stakes private equity firms";
     - "rescue financing distressed firms".
   - Nine refinements:
     - "payment-in-kind toggle debt default risk";
     - "debtor-in-possession financing bankruptcy outcomes";
     - "vulture investors distressed firms control";
     - "convertible security call policy issuer";
     - "venture capital contract terms liquidation preference pricing";
     - "private investment in public equity discounts returns";
     - "private credit fund performance risk-adjusted";
     - "private equity management company valuation fee-related earnings";
     - "government preferred stock warrants recapitalization valuation".
3. **Expected yield.** The rerun should fill the PIK, debtor-in-possession and convertible-call-policy gaps, which I could not cover. It should also add recent 2022–2026 work on private credit and NAV finance.
