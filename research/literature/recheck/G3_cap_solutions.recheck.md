# Topic G3 (Capital Solutions): re-check of the 12 citations left unchecked (quota)

**Date:** 2026-10-18.

**Scope:** the 12 rows marked "unchecked (quota)" in the citation-integrity table (§2) of `research/literature/G3_cap_solutions.lit.md`. These are refs 41–47, 51 and 53–55 of the dossier's §10, plus "Mack", which appears only in the body (§3.8). The works are cited in `research/groups/dossiers/G3_cap_solutions.md`. The dossier was not edited.

**Method**
- **Metadata** came from Crossref (`api.crossref.org/works/<DOI>` and `query.bibliographic`), plus the Fed and NBER pages.
- **Usage.** Each number or finding the dossier attributes to one of these works was checked against the source.
  - **Full text**, with text extracted locally using pypdf:
    - NBER w32278 (March 2024), and an April 2026 revision of it;
    - the published *FAJ* PDF of Böni & Manigart (open access, with the Taylor & Francis cover page);
    - the Ayache–Forsyth–Vetzal working paper of 22 Apr 2003 (Forsyth's Waterloo page);
    - Duffie (1998), *Defaultable Term Structure Models with Fractional Recovery of Par* (Stanford page). It was used for the reduced-form recovery conventions.
  - **Abstracts:** NBER (Erel et al.; Kaplan & Strömberg, w7660) and the FEDS Note page.
- **Sources that were not available:**
  - OpenAlex returned HTTP 429 (Retry-After about 34,800 s).
  - The Springer, PM Research and Cambridge pages required a sign-in or returned 403.
  - Semantic Scholar holds no abstract for Lando.
  - The CAS archive copy of Mack (1993) is a scan with no text layer.
  - Crossref returned 429 on parallel calls; serial calls succeeded.
  - Consensus was not used (quota exhausted).

**Verdict convention.** As in the other re-check files, "ok", "mismatched" and "not found" describe metadata. Usage verdicts are given separately in the same cell.

## Summary

- **12 checked: 10 ok, 2 mismatched, 0 not found.** No reference is fabricated.
  - **Kaplan & Strömberg:** the title drops its subtitle.
  - **Mack:** there is no reference entry, year or title. The probable work, Mack (1993), exists in Crossref.
  - **The three [K] entries (Black–Cox, Tsiveriotis–Fernandes, Lando) are correct but incomplete.** Add pages and DOIs, and drop [K].
  - DOIs can also be added for Erel et al. and Cai & Haque.
- **Usage problems (5). One confirms the companion verification log (VL); four contain new findings.**
  1. **Cai & Haque (confirms VL F11).** The recovery figures are KBRA DLD data, not S&P data.
  2. **Böni & Manigart (§3.6; new).** In their regressions, the coefficient on ex-ante credit spreads is positive but not significant for IRR. The significant effects are on net multiples and on PME against IG and HY bonds. The omitted TED-spread effect (VL R4) still stands.
  3. **Erel, Flanagan & Weisbach (new).**
     - The "+$0.041" is a GPME with a stock factor only, not an estimate "with equity and bond factors".
     - An April 2026 revision changes most of the numbers, but not the conclusion.
     - The §6.8 "underwritten" label (VL R5) still stands.
  4. **Jarrow & Turnbull (§2.4, minor; new).** "Recovery proportional to market value" is Duffie & Singleton's convention. Jarrow & Turnbull recover a fraction of an equivalent default-free bond, and the Cox-process intensity is Lando's.
  5. **Tsiveriotis & Fernandes (§3.3, minor; new).** The dossier offers TF as an equal alternative to AFV. But AFV, cited in the same sentence, argue that the TF model is internally inconsistent.
- **Every other attributed number matches its source:**
  - all Böni & Manigart values in §1.4, §4.4 and §6.6;
  - all Erel et al. values in §1.4 and §4.4, against the cited March 2024 version;
  - the Fed's recoveries (33%, 52%, 39%) and market sizes (US$1.7tn, US$1.4tn, US$1.3tn; June 2023 data).
- **Against the VL and the lit file.**
  - VL F6, F7, F11 and the VL's bibliography rows are reproduced.
  - **One clarification:** the FEDS Note's 26-Feb-2024 correction concerns the data source of Figure 13 (Pitchbook changed to KBRA DLD). It does not concern the recovery figure (Figure 15).

## Citation table

| Citation (dossier §10 ref; where used) | Verdict | Correction / notes | Source URL |
|---|---|---|---|
| Ref 41. Cai, F., & Haque, S. (23-Feb-2024). *Private Credit: Characteristics and Risks.* FEDS Notes (§1.5 l. 32; §4.2 l. 243; §4.5 l. 287) | ok; **usage problem (attribution)** | **Confirmed:** Fang Cai and Sharjil Haque, *FEDS Notes*, Board of Governors of the Federal Reserve System, 23 Feb 2024. Add DOI 10.17016/2380-7172.3462. **The numbers match.** The post-default value of a direct loan is "around 33 percent", against "52 and 39 percent" for syndicated loans and HY bonds. Private credit is "nearly $1.7 trillion", against "roughly $1.4 trillion" for leveraged loans and "about $1.3 trillion" for HY bonds. Figure 1 says "Data as of June 2023" (source: Preqin). **The attribution is wrong.** Figure 15 ("Recovery Rate") gives "Source: KBRA DLD". The note cites S&P Global only for repeat defaults. In §1.5, replace "(Fed, citing S&P)", and in §4.5 replace "Fed FEDS Note citing S&P", with "Fed FEDS Note, KBRA DLD data". The 26-Feb-2024 correction fixed the source of Figure 13 (Pitchbook changed to KBRA DLD), not these figures. | https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-characteristics-and-risks-20240223.html · https://api.crossref.org/works/10.17016/2380-7172.3462 |
| Ref 42. Erel, I., Flanagan, T., & Weisbach, M. S. (2024). *Risk-Adjusting the Returns to Private Debt Funds.* NBER WP 32278 (§1.4 l. 30; §1.6 l. 36; §4.4 ll. 268, 272; §6.6 #8; §6.8 l. 530; §6.13) | ok (as cited); **usage problem (minor label)**; **version note** | **Confirmed:** NBER WP 32278, March 2024; add DOI 10.3386/w32278. Crossref still has no journal version, only SSRN copies (10.2139/ssrn.4779852 and 10.2139/ssrn.4771873), and a web search found none. **Numbers:** every §4.4 number matches the March 2024 text (note 1). **Fix the label:** "risk-adjusted profit ≈ 0 with equity and bond factors" is the RAP estimate: −$0.001 per $1, t = −0.01 (Table 4B). The +$0.041 GPME (t = 1.48) uses a stock factor only, because the authors say GPME cannot use both factors (fn 7). **Version:** an April 2026 draft, with the same title and authors, revises the numbers: 545 funds; net IRR 8.5%; gross alpha 6.1% (4.0% with elastic net) on 55 funds; imputed fees of 3.2% or 4.2% (note 1). Its conclusion is unchanged. **Still wrong (VL R5):** the §6.8 label "underwritten gross − 4 to 6pp [S-anchored: EFW …]". Erel et al. compare realised gross returns with net returns; they do not measure underwritten returns. | https://www.nber.org/papers/w32278 · https://www.nber.org/system/files/working_papers/w32278/w32278.pdf (Tables 2–7; printed pp. 3–4, 13–20) · https://api.crossref.org/works?query.bibliographic=Risk-Adjusting+the+Returns+to+Private+Debt+Funds+Erel+Flanagan+Weisbach&rows=6 · https://bpb-us-w2.wpmucdn.com/u.osu.edu/dist/8/7843/files/2026/04/Alpha_for_Private_Debt_Funds-April-2026.pdf |
| Ref 43. Böni, P., & Manigart, S. (2022). Private debt fund returns, persistence, and market conditions. *FAJ* 78(4), 121–144. DOI 10.1080/0015198X.2022.2092384 (§1.4 l. 30; §1.6 l. 37; §3.6 l. 182; §4.4 l. 267; §6.6 #8–9; §6.8; §6.13) | ok; **usage problem (§3.6 overstated; §1.6 incomplete)** | **Confirmed against Crossref:** *FAJ* 78(4):121–144; online 18 Aug 2022, print 2 Oct 2022; licence CC BY-NC-ND 4.0. Every number in §1.4, §4.4 and §6.6 matches the published text (note 2). **§3.6, "expected vintage IRR rises with ex-ante spreads":** in Table 5 the ex-ante credit-spread coefficient on IRR is positive but **not significant** (1.363). It is significant for the net multiple (5%) and for PME against IG and HY bonds (1%), and not for PME against the S&P 500. **§1.6, "funds raised when spreads are wide earn more":** this holds for multiples and for PME against bond benchmarks. It omits two points. BM's spread is the BB OAS over the 360 days before the first capital call. And a higher ex-ante TED spread significantly *lowers* PME outperformance (VL R4). BM's own summary is "performance is highest when credit spreads expand ex ante and ex post, whilst TED spreads contract". | https://api.crossref.org/works/10.1080/0015198X.2022.2092384 · https://doi.org/10.1080/0015198X.2022.2092384 (published PDF: article pp. 2–4; Tables 1, 2, 3, 4C, 5) |
| Ref 44. Merton, R. C. (1974). *JF* 29(2), 449–470 (§2.4 l. 81) | ok; usage accurate | **Confirmed against Crossref:** Robert C. Merton, "On the Pricing of Corporate Debt: The Risk Structure of Interest Rates", *JF* 29(2):449–470, May 1974, DOI 10.1111/j.1540-6261.1974.tb03058.x. **Usage:** AFV (fn 2) describe Merton as considering zero-coupon debt that defaults if firm value is below its face value "at its maturity". **Optional precision for §2.4:** add "at the debt's maturity". That sharpens the contrast with Black–Cox. | https://api.crossref.org/works/10.1111/j.1540-6261.1974.tb03058.x · https://cs.uwaterloo.ca/~paforsyt/convert.pdf (fn 2) |
| Ref 45. Jarrow, R. A., & Turnbull, S. M. (1995). *JF* 50(1), 53–85 (§2.4 l. 82) | ok; **usage imprecise (minor)** | **Confirmed against Crossref:** "Pricing Derivatives on Financial Securities Subject to Credit Risk", *JF* 50(1):53–85, March 1995, DOI 10.1111/j.1540-6261.1995.tb05167.x. **Usage:** §2.4 attributes "a Cox-process intensity, with recovery proportional to market value" to Jarrow–Turnbull, Duffie–Singleton and Lando together. Duffie (1998) separates the conventions. Jarrow and Turnbull "stipulated that, at default, a bond would have a market value equal to an exogenously specified fraction of an otherwise equivalent default-free bond". Recovery of market value is Duffie and Singleton's convention. Reword (note 3). | https://api.crossref.org/works/10.1111/j.1540-6261.1995.tb05167.x · https://web.stanford.edu/~duffie/par.pdf (p. 3) |
| Ref 46. Duffie, D., & Singleton, K. J. (1999). *RFS* 12(4), 687–720 (§2.4 l. 82) | ok; usage accurate | **Confirmed against Crossref:** "Modeling Term Structures of Defaultable Bonds", *RFS* 12(4):687–720, July 1999, DOI 10.1093/rfs/12.4.687. **Usage:** Duffie (1998) cites the 1997 working paper of the same title. He describes it as "exogenous fractional recovery of market value at default", which is the convention §2.4 names. | https://api.crossref.org/works/10.1093/rfs/12.4.687 · https://web.stanford.edu/~duffie/par.pdf (p. 3) |
| Ref 47. Ayache, E., Forsyth, P. A., & Vetzal, K. R. (2003). *Journal of Derivatives* 11(1), 9–29 (§3.3 l. 154) | ok; usage accurate (but see ref 54) | **Confirmed against Crossref:** "Valuation of Convertible Bonds With Credit Risk", *Journal of Derivatives* 11(1):9–29, 2003, DOI 10.3905/jod.2003.319208. The working paper is titled "The Valuation of …"; cite the journal title, as the dossier does. **Usage:** the abstract confirms an approach based on "the numerical solution of linear complementarity problems", which is a PDE formulation with early-exercise constraints, and "a Poisson default process". The paper's central claim is that the TF model is internally inconsistent (ref 54 row). | https://api.crossref.org/works/10.3905/jod.2003.319208 · https://cs.uwaterloo.ca/~paforsyt/convert.pdf (abstract; §1; §5) |
| Ref 51. Kaplan, S. N., & Strömberg, P. (2003). *Financial contracting theory meets the real world.* *RES* 70(2), 281–315 (§2.3 l. 76) | **mismatched (minor: title truncated)**; usage accurate | **Title:** the full title is "Financial Contracting Theory Meets the Real World: **An Empirical Analysis of Venture Capital Contracts**" (Crossref; NBER w7660). Add the subtitle. **The rest is confirmed:** *RES* 70(2):281–315, April 2003, DOI 10.1111/1467-937X.00245. **Usage:** the NBER abstract says investors gain full control when the company performs poorly, and the entrepreneur gains control as performance improves. The authors find the contracts most consistent with Aghion & Bolton (1992) and Dewatripont & Tirole (1994), which are both incomplete-contracts theories. This matches "state-contingent control transfers, the incomplete-contracts logic". | https://api.crossref.org/works/10.1111/1467-937X.00245 · https://www.nber.org/papers/w7660 |
| Ref 53. [K] Black, F., & Cox, J. C. (1976). *Journal of Finance* 31(2) (§2.4 l. 81) | ok (incomplete); usage plausible [unverified] | **Complete the entry and drop [K]:** Fischer Black and John C. Cox, *JF* 31(2):**351–367**, May 1976, DOI 10.1111/j.1540-6261.1976.tb01891.x. The title matches. **Usage:** AFV list the paper among structural models in which "default occurs when the firm's value becomes sufficiently low that it is unable to meet its financial obligations". "A first-passage barrier represents covenants" also fits the title ("Some Effects of Bond Indenture Provisions"). [unverified: neither the paper's text nor an abstract was accessible, so the barrier feature was not read in the source.] | https://api.crossref.org/works/10.1111/j.1540-6261.1976.tb01891.x · https://cs.uwaterloo.ca/~paforsyt/convert.pdf (§1) |
| Ref 54. [K] Tsiveriotis, K., & Fernandes, C. (1998). *Journal of Fixed Income* 8(2) (§3.3 l. 154) | ok (incomplete); **usage: caveat missing (minor)** | **Complete the entry, and drop [K] and the failed-DOI note:** Kostas Tsiveriotis and Chris Fernandes, "Valuing Convertible Bonds with Credit Risk", *Journal of Fixed Income* 8(2):**95–102**, Sept 1998, DOI **10.3905/jfi.1998.408243**. **Usage:** AFV confirm the dossier's description of the TF split. It has a "cash-only" part, which is subject to credit risk, and an equity part, which is not; this gives a pair of coupled PDEs. However, AFV conclude that "the widely used convertible bond model of Tsiveriotis and Fernandes (1998) is internally inconsistent", because it never specifies what happens at default. AFV is cited in the same §3.3 sentence. Present TF as a simple benchmark, not as an equal alternative (note 4). | https://api.crossref.org/works/10.3905/jfi.1998.408243 · https://cs.uwaterloo.ca/~paforsyt/convert.pdf (pp. 2–3; §5.1) |
| Ref 55. [K] Lando, D. (1998). *On Cox processes and credit risky securities.* *Review of Derivatives Research* 2 (§2.4 l. 82) | ok (incomplete); usage accurate | **Complete the entry and drop [K]:** David Lando, *Review of Derivatives Research* 2(**2–3**):**99–120**, December 1998, DOI 10.1007/BF01531332. The title matches. **Usage:** the Cox-process framing in §2.4 is the paper's own, as its title shows. No abstract was accessible: Springer requires a sign-in, and Semantic Scholar omits it. | https://api.crossref.org/works/10.1007/BF01531332 · https://web.stanford.edu/~duffie/par.pdf (ref. 25) |
| §3.8 "Mack" (workout-recovery development triangles); no reference entry (l. 195) | **mismatched (no reference entry, year or title)**; usage plausible | **Probable work** [Inference]: Thomas Mack (1993), "Distribution-free Calculation of the Standard Error of Chain Ladder Reserve Estimates", *ASTIN Bulletin* 23(2):213–225, November 1993, DOI 10.2143/AST.23.2.2005092. Crossref confirms it exists. If it is the intended work, add it to §10. **Usage:** applying the chain-ladder standard error to workout-recovery triangles is the dossier's own analogy; §3.8 is tagged [I]. [unverified: the abstract was not read. The Cambridge page returned 403, and the CAS archive copy is a scan with no text layer.] "Bootstrap" is a method name and needs no citation. | https://api.crossref.org/works?query.bibliographic=Mack+Distribution-free+calculation+of+the+standard+error+of+chain+ladder+reserve+estimates&rows=5 |

## Notes

**1. Erel, Flanagan & Weisbach: numbers by version**

| Dossier value (§4.4; also §1.4, §1.6) | NBER w32278, March 2024 (the cited version) | April 2026 draft |
|---|---|---|
| 532 USD funds, Burgiss-MSCI, 1992–2015 vintages | Confirmed (printed pp. 13–14) | 545 funds; same filters |
| Average net IRR 8.6% | Confirmed (Table 3) | 8.5% |
| Mezzanine 8.4%, distressed 8.3% | Confirmed: 8.4% (193 funds) and 8.3% (163 funds) (Table 6) | 8.3% (191 funds) and 8.3% (164 funds) |
| Risk-adjusted profit ≈ 0 with equity and bond factors | Confirmed: RAP −$0.001 per $1, t = −0.01; alpha ≈ 0 (Table 4B) | RAP +$0.035 per $1; alpha 0.6% (SE 1.0%); insignificant |
| "GPME +$0.041 per $1, insignificant" | +$0.041 is the **stock-factor** GPME: t = 1.48 in Table 4C, 1.46 in Table 6. The bond-factor GPME is +$0.120 and significant. GPME with both factors is not estimated (fn 7). | Stock factor +$0.080 (insignificant); bond factor +$0.096 (significant); HY bond plus stock factor about −$0.001 (insignificant) |
| 15% of holdings (20% value-weighted) carry equity features | Confirmed. The source is Pitchbook holdings data, not the Burgiss sample (Table 2). | Unchanged |
| Gross IRR 13.9% and gross alpha ~4.1%, on a 65-fund subsample | Confirmed (Table 7B: 65 observations) | Gross IRR 14.2%; alpha 6.1% (baseline) or 4.0% (elastic net); 55 funds |
| Fees ≈ 3.1–3.9% a year | Confirmed, but **imputed** from assumed contracts: 1.5/15 with a 6% hurdle, and 2/20 with an 8% hurdle (Table 7A) | 3.2% and 4.2%. The gross–net IRR wedge is 5.2%, which the authors treat as an upper bound. |
| Gross alpha ≈ fees; net alpha ≈ 0 | Confirmed (printed p. 20) | Unchanged |
| Cash flows load on equity factors (§1.6) | Confirmed: significant stock loadings at horizons 1–4 and 10–11 (Table 5) | Unchanged in substance: stock beta 0.6 early in a fund's life |

- **Recommendation.** Keep citing NBER w32278 and fix the GPME label.
  - If the dossier owner wants the latest figures, cite the April 2026 draft explicitly. Then update §1.4 and §4.4, and change the "3–4pp of fees" inference in §4.4 to 3.2–4.2pp.
  - The draft is not peer-reviewed, and the NBER page still lists only the March 2024 version.

**2. Böni & Manigart: what the paper reports**
- **Numbers.** All are confirmed in the published PDF (Tables 2–3; article pp. 2–3):
  - 448 funds; vintages 1986–2018; Preqin data with a cut-off of 31 Dec 2020;
  - mean (median) net IRR 9.19% (8.46%);
  - direct lending 8.78% (7.9%);
  - distressed 8.37% (8.3%), net multiple 1.37x;
  - mezzanine 9.04% (9.4%), net multiple 1.34x;
  - special situations 12.62% (8.0%), SD 23.1%;
  - PME against HY bonds 1.06;
  - top quartile 23.3%, bottom quartile −3.6%.
- **How market conditions are measured.** Ex-ante conditions cover the 360 days before the first LP cash contribution. The credit spread is the ICE BofA US Corporate BB OAS (Table 1 notes).
- **Regressions (Table 5; standard errors clustered by GP).**
  - Ex-ante credit spread: positive and significant for the net multiple (0.0401, at 5%), PME against IG (0.0594, at 1%) and PME against HY (0.0442, at 1%). It is insignificant for IRR (1.363), and negative and insignificant for PME against the S&P 500 (−0.0209).
  - Ex-ante TED spread: negative and significant for PME against IG (−0.177) and against HY (−0.195), and insignificant for IRR.
- **Portfolio sort on PME against IG (Table 4C).** Outperforming funds were launched at credit spreads 70–75bp higher and TED spreads 1–2bp lower.
- **Implication for §3.6.** Calibrate the spread effect on multiples or on PME against bond benchmarks, not on IRR. Add the TED (funding-liquidity) term, as the lit file's challenge 2 and VL R4 already ask.

**3. The reduced-form sentence in §2.4**
- **Duffie (1998, Stanford working paper, p. 3)** separates the two recovery conventions:
  - Jarrow and Turnbull "stipulated that, at default, a bond would have a market value equal to an exogenously specified fraction of an otherwise equivalent default-free bond".
  - Duffie and Singleton "followed with a model that, when specialized to exogenous fractional recovery of market value at default, allows for closed-form solutions in a wider range of cases".
  - Duffie's draft writes "Jarrow and Turnbull (1996)" in the text, but its only Jarrow–Turnbull reference is the *JF* 50 article.
- **Lando's** title supplies the Cox-process framing.
- [Inference] The dossier's own engine uses a third convention. In §3.1 the claim converts at default to the recovery rate times the accreted claim, which is recovery of face (par). That is the convention Duffie (1998) models.
- **Suggested wording:** "Reduced-form view. Default arrives at an intensity (Jarrow–Turnbull 1995), which is stochastic in Lando's (1998) Cox-process framework. Recovery is a fixed fraction of an equivalent default-free bond in Jarrow–Turnbull, and a fraction of pre-default market value in Duffie–Singleton (1999). §3.1 uses recovery of the accreted claim."

**4. Convertibles (§3.3)**
- **AFV's abstract** says that TF-type models "are unsatisfactory in that they do not explicitly specify what happens in the event of a default by the issuing firm". This "can lead to internal inconsistencies, such as cases where a call by the issuer just before expiry renders the convertible value independent of the credit risk of the issuer, or situations where the implied hedging strategy may not be self-financing".
- **AFV §5.1:** in the TF model, the equity component is discounted at the risk-free rate and the bond component at a risky rate.
- **Suggested wording:** "For convertibles with credit risk, use the Ayache–Forsyth–Vetzal (2003) PDE (linear-complementarity) formulation with an explicit default and recovery model. Use the Tsiveriotis–Fernandes (1998) split only as a benchmark: a cash-only part discounted at a risky rate, and an equity part discounted at the risk-free rate. AFV show that it can be internally inconsistent."

## Suggested changes for the dossier owner (not applied)

1. **Ref 41.** Add DOI 10.17016/2380-7172.3462. Change "citing S&P" to "KBRA DLD data" in §1.5 (l. 32) and §4.5 (l. 287).
2. **Ref 42.**
   - In the §4.4 row, change the parenthesis to "(RAP −$0.001 per $1, t = −0.01; GPME with a stock factor +$0.041, t = 1.48; both insignificant)".
   - Optionally add DOI 10.3386/w32278 and a note on the April 2026 revision.
3. **Ref 43, §3.6 (l. 182).** "Funds launched when ex-ante BB credit spreads are higher earn higher net multiples and outperform IG and HY bond benchmarks (the IRR coefficient is positive but insignificant). A higher ex-ante TED spread lowers outperformance (Böni & Manigart 2022, Table 5)."
4. **§2.4 (l. 82).** Use the wording in note 3.
5. **§3.3 (l. 154).** Use the wording in note 4.
6. **Ref 51.** Add the subtitle ": An Empirical Analysis of Venture Capital Contracts".
7. **Refs 53–55.** Replace them with:
   - Black, F., & Cox, J. C. (1976). Valuing corporate securities: some effects of bond indenture provisions. *Journal of Finance* 31(2), 351–367. https://doi.org/10.1111/j.1540-6261.1976.tb01891.x
   - Tsiveriotis, K., & Fernandes, C. (1998). Valuing convertible bonds with credit risk. *Journal of Fixed Income* 8(2), 95–102. https://doi.org/10.3905/jfi.1998.408243
   - Lando, D. (1998). On Cox processes and credit risky securities. *Review of Derivatives Research* 2(2–3), 99–120. https://doi.org/10.1007/BF01531332
8. **New entry, if Mack (1993) is the intended work:** Mack, T. (1993). Distribution-free calculation of the standard error of chain ladder reserve estimates. *ASTIN Bulletin* 23(2), 213–225. https://doi.org/10.2143/AST.23.2.2005092
