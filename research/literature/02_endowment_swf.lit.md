# Literature review 02: Endowment model, spending policy, SWF practice and the Total Portfolio Approach

**Project:** ADIC multi-period robust TPA framework (agentic) · **Stream:** 02 · **Prepared:** 18 Oct 2026

**Inputs read:**
- `research/dossiers/02_endowment_swf.md` (the dossier under review; not edited)
- `research/verification/02_endowment_swf.verify.md` (the adversarial fact-check)
- `inputs/00_CONTEXT_AND_PRIOR_WORK.md` §1 and §1A

**User confirmations used to target the search (2026-10-18):**
- The Secondaries group is a hybrid of direct and fund investments.
- Treasury is owned by Corporate Finance and is not an investment group.

Papers bearing on these two points are flagged in §4.7.

**Evidence conventions:**
- Findings come from Consensus abstracts only. No full texts were read.
- Anything marked *(inference)* is our reading of what a paper implies for ADIC. It is not a claim the paper makes.
- Authors appear as Consensus lists them, with "et al." where Consensus truncates the list.
- Citation counts are Consensus counts as of 18 Oct 2026.
- Years are Consensus years. Where Consensus shows a working-paper year or an indexing artefact, the published year is noted.

**Contents:**
- §1 Summary
- §2 Citation-integrity table (21 dossier works)
- §3 Annotated bibliography (25 papers)
- §4 Design implications, plus 69 supplementary papers (§4.8)
- §5 Papers that challenge the dossier
- §6 Usage message
- §7 Method and limitations

---

## 1. Summary

1. **Citation integrity is high. Three metadata or attribution fixes are needed.**
   - **Scope.** We checked 21 academic works cited in the dossier: everything in §10 "Theory and literature" plus the "not verified in-session" list.
   - **17 exist with matching metadata.**
     - 15 were found in Consensus.
     - Merton (1993) is not indexed in Consensus. It was confirmed at NBER by WebSearch.
     - The CAIA/TAI TPA report is not indexed either. Its existence was confirmed by fetching the TAI page.
   - **3 are mismatched:**
     - **Ennis's 2020 SSRN paper** was published as Ennis (2021) in *The Journal of Investing*.
     - **The 12-year −1.87% figure.** The dossier's single Ennis reference also carries this figure, which belongs to a separate paper. That paper is probably Ennis (2021), "Failure of the Endowment Model", *JPM* *(inference)*.
     - **The CFA Institute TPA guide** is cited without authors. The record is Urwin et al., DOI 10.56227/26.1.20.
   - **1 cannot be verified.** de Finetti (1957) is not indexed. A citing paper corroborates its venue and pages.
   - **8 "unverified" items can be upgraded to verified:**
     - Dybvig (1995)
     - Dufresne (1988)
     - Owadally & Haberman (1999)
     - Owadally & Haberman (2004)
     - Lerner, Schoar & Wang (2008)
     - Powell (2019)
     - Constantinides (1990)
     - Kydland & Prescott (1977)
   - No citation is fabricated.
2. **The largest gap is the expected-return spending anchor.**
   - **What the dossier recommends.** It adopts "spend from expected, not realized, returns" (Norway, Singapore) and tests θ up to 1.0.
   - **What uncited literature says.** A 2016–2024 cluster argues three things:
     - Spending the expected return depletes a fund with probability one [2].
     - Optimal spending is significantly below the expected return [2][4].
     - Smoothing can exhaust wealth in finite time [1].
   - **Consequence.** This changes the dossier's expected-return rule and its θ grid (§5, C1).
3. **The dossier lacks SWF-specific theory.**
   - **Subsoil oil belongs on the balance sheet.** The owner's balance sheet includes oil below ground. Per [6], it "should alter a fund's portfolio through additional leverage and hedging".
   - **The oil–equity correlation drives the answer.** The optimal allocation for a commodity SWF is "particularly sensitive" to it [8].
   - **The state should separate three funds:** an intergenerational fund, a liquidity fund for precautionary buffers, and an investment fund [7]. The liquidity fund maps directly onto ADIC's Corporate Finance/Treasury.
4. **Illiquidity theory and calibration are thin.** Five uncited papers supply state variables, parameters and a solver that yields duals: the shadow prices that verification R4 says are missing.
   - illiquidity crises of uncertain duration [12]
   - model-predictive control (MPC) of commitments under a chance constraint [13]
   - a frequency-and-severity view of liquidity events [14]
   - secondary-market liquidity costs [15]
   - a PE liquidity-risk premium of about 3% a year [16]
5. **Two empirical pillars are contested.**
   - **"Endowment hoarding" is disputed.** Brown et al.'s (2014) finding is contradicted by Rosen & Sappington (2019), who find symmetric payout responses [20].
   - **The performance critique goes beyond Ennis.**
     - Alpha is about zero once alternatives are benchmarked [18].
     - Large endowments' effective US equity exposure is about 97% [19].
6. **Recent TPA work (2025–2026) is operational.**
   - an appraisal ratio measured against the reference portfolio [23]
   - pre-committed governance whose decision rights tighten as uncertainty rises [24]
   - delegated benchmarks [S60]
   - drawdown-first tracking-error budgets [S61]
   - a 44-agent SAA pipeline governed by the IPS [25]
7. **Well-posed replacements exist for the dossier's ill-defined habit objective (verification R1):**
   - affine payout rules that are optimal under a linear-quadratic (LQ) criterion [21]
   - drawdown constraints on payout rates, with ruin possible [22]
   - habit-formation constraints [S46]
   - soft-social-norm preferences [4]

**Run statistics:**
- 29 Consensus searches: 17 citation checks and 12 topical searches.
- 1 WebSearch (Merton) and 1 direct fetch (the TAI hub page).
- A second WebSearch failed because the session's shared web-search budget was exhausted. As a result, SSRN 3614875 and de Finetti's title could not be checked on the web.
- No Consensus sign-up, upgrade or usage message appeared.

---

## 2. Citation-integrity table

**Status key:**
- **Found:** metadata matches.
- **Mismatched:** the work exists but authors, year, title or venue differ.
- **Not found:** no Consensus match and no web confirmation.

| # | Dossier citation | Status | Corrected or completed metadata | Consensus URL |
|---|---|---|---|---|
| 1 | Tobin (1974), *AER* 64(2):427–432 | Found | "What Is Permanent Endowment Income", *AER*, 119 citations. Consensus shows the year as 2016, an indexing artefact. | https://consensus.app/papers/details/7f6984422b2a5b739450910c5dc27d01/?utm_source=claude_desktop |
| 2 | Merton (1993), chapter in Clotfelter & Rothschild (eds.); NBER WP 3820 | Found via WebSearch (not indexed in Consensus) | Chapter 7 of *Studies of Supply and Demand in Higher Education*, U. Chicago Press, 1993, pp. 211–242 per the NBER chapter PDF. Working paper: NBER WP 3820, August 1991. Consensus has indirect support: Halem et al. (2022) build on "Merton's (1993) endowment model". | None. Web sources: [NBER chapter c6102](https://www.nber.org/chapters/c6102); [NBER w3820](https://www.nber.org/papers/w3820) |
| 3 | Dybvig (1999), *FAJ* 55(1):49–62 | Found | DOI 10.2469/faj.v55.n1.2241, 53 citations. The *FAJ* record carries no author; the 1998 working-paper record lists Philip H. Dybvig. | https://consensus.app/papers/details/ac6b4afe4adf5de68e6dee26fa078f05/?utm_source=claude_desktop |
| 4 | Dybvig (1995), *RES* 62(2):287–313 (dossier: "unverified") | Found; upgrade to verified | Full title "Dusenberry's Ratcheting of Consumption: Optimal Dynamic Consumption and Investment Given Intolerance for any Decline in Standard of Living". DOI 10.2307/2297806, 188 citations. | https://consensus.app/papers/details/748fe37345405ad99e884e16ca31c814/?utm_source=claude_desktop |
| 5 | Dimmock, Wang & Yang (2024), *Management Science* 70(3):1554–1579; NBER WP 25559 | Found | Consensus shows 2019 and the NBER DOI 10.3386/w25559. The abstract cites the *MS* DOI 10.1287/mnsc.2023.4759. 25 citations. | https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop |
| 6 | Gilbert & Hrdlicka (2015), *RFS*, doi:10.1093/rfs/hhv031 | Found | "Why are University Endowments Large and Risky", 42 citations. | https://consensus.app/papers/details/248d35997763530a9386a6a4059638f2/?utm_source=claude_desktop |
| 7 | Brown, Dimmock, Kang & Weisbenner (2014), *AER* 104(3):931–962 | Found | Full title "How University Endowments Respond to Financial Market Shocks: Evidence and Implications". DOI 10.1257/aer.104.3.931, 119 citations. | https://consensus.app/papers/details/7831f601f303581cb3e87906847e0fab/?utm_source=claude_desktop |
| 8 | Campbell (2012), *Forum Futures 2012* | Found | Consensus: J. Campbell, 2011, no venue, 12 citations. This is consistent with the dossier's note that the slides date from 2011. | https://consensus.app/papers/details/17f62ee307ea509295452c247941d91b/?utm_source=claude_desktop |
| 9 | Cejnek, Franz, Randl & Stoughton (2014), *JOIM* 12(3):90–117 | Found (working-paper version) | Consensus indexes the SSRN version: 2013, DOI 10.2139/ssrn.2205207, 32 citations. The *JOIM* version and its pages are not indexed. | https://consensus.app/papers/details/89bbc59b3d225ff8b53136d5655fbed9/?utm_source=claude_desktop |
| 10 | Ennis (2020), "Endowment performance" (SSRN 3614875) | **Mismatched** (year, venue) | Published as Ennis, R.M. (2021), "Endowment Performance", *The Journal of Investing*, DOI 10.3905/joi.2021.1.166, 10 citations. The abstract says that of the 43 largest endowments over the 11 years to 30 June 2019, "none outperformed with statistical significance, while one in four underperformed with statistical significance", and puts costs at 1–2% of assets. It does not tie the dossier's −1.1% to −1.8% alpha range to those 43 endowments, which is consistent with the verification log's correction to "size cohorts". The SSRN ID was not checked because the web-search budget was exhausted. | https://consensus.app/papers/details/7a715cd5f109565f8ec21d59aba046bc/?utm_source=claude_desktop |
| 11 | Ennis: "−1.87% a year versus passive … 12 years to June 2020" (§2.6), cited to the same reference 10 | **Mismatched** (attribution) | Cite this as a separate paper. Consensus indexes Ennis, R.M. (2021), "Failure of the Endowment Model", *The Journal of Portfolio Management*, DOI 10.3905/jpm.2021.1.217, 12 citations. Its abstract says alternatives were "a consistent drag on performance" over "the past 12 years". The −1.87% figure itself is not in the abstract, so naming this paper as the source is *(inference)*. | https://consensus.app/papers/details/c5b7fa6fe1d857a2a6eaa2a26138ea89/?utm_source=claude_desktop |
| 12 | de Finetti (1957) (dossier: "unverified") | **Not found** (original not indexed) | A citing record in Consensus, Loeffen (2008, *Ann. Appl. Probab.*), gives the source as "de Finetti, Trans. XVth Internat. Congress Actuaries 2 (1957) 433–443". The title could not be web-checked because the budget was exhausted. | Corroborating record: https://consensus.app/papers/details/8e6d66eec4c75444af49fc3bc3155f2b/?utm_source=claude_desktop |
| 13 | Dufresne (1988), *J. Inst. Actuaries* (dossier: "unverified") | Found; upgrade to verified | "Moments of pension contributions and fund levels when rates of return are random", *Journal of the Institute of Actuaries*, DOI 10.1017/s0020268100042815, 81 citations. The Consensus record misspells the first word as "Movements". | https://consensus.app/papers/details/41f77ccdc2e65dd3a6150ce212c3cfdd/?utm_source=claude_desktop |
| 14 | Owadally & Haberman (1999), *NAAJ* (dossier: "unverified") | Found; upgrade to verified | "Pension Fund Dynamics and Gains/Losses Due to Random Rates of Investment Return", *NAAJ*, DOI 10.1080/10920277.1999.10595837, 40 citations. | https://consensus.app/papers/details/878aa164a5645c0d98c365913aab2103/?utm_source=claude_desktop |
| 15 | Owadally & Haberman (2004), *NAAJ* (dossier: "unverified") | Found; upgrade to verified | "Efficient Gain and Loss Amortization and Optimal Funding in Pension Plans", *NAAJ*, DOI 10.1080/10920277.2004.10596126, 23 citations. The abstract supports dossier §2.7: proportional spreading "optimizes mean square deviations in the contributions and fund levels". | https://consensus.app/papers/details/a708f2b9d8f45ad19c68cb048e4661c7/?utm_source=claude_desktop |
| 16 | Lerner, Schoar & Wang (2008), *JEP* (dossier: "unverified") | Found; upgrade to verified | "Secrets of the Academy: The Drivers of University Endowment Success", *JEP* 22(3):207–222, 195 citations. The Consensus record lacks author names. | https://consensus.app/papers/details/ffa91ac141ed50e2a6f0fdcde056c35b/?utm_source=claude_desktop |
| 17 | Powell (2019), *EJOR* (dossier: "unverified") | Found; upgrade to verified | "A unified framework for stochastic optimization", DOI 10.1016/j.ejor.2018.07.014, 331 citations. The abstract confirms "four meta-classes of policies". | https://consensus.app/papers/details/ab76d63d106c536683f1fb197164274c/?utm_source=claude_desktop |
| 18 | Constantinides (1990), *JPE* (dossier: "unverified") | Found; upgrade to verified | "Habit Formation: A Resolution of the Equity Premium Puzzle", DOI 10.1086/261693, 1,037 citations. | https://consensus.app/papers/details/9b1d64a83c5750c2886921a04bbf0dbe/?utm_source=claude_desktop |
| 19 | Kydland & Prescott (1977), *JPE* (dossier: "unverified") | Found; upgrade to verified | "Rules Rather than Discretion: The Inconsistency of Optimal Plans", DOI 10.1086/260580, 8,098 citations. | https://consensus.app/papers/details/0f99ef5696bb58ffa746c2624010abfe/?utm_source=claude_desktop |
| 20 | CFA Institute RPC (Jul 2026), *The Total Portfolio Approach: A Practical Guide for Navigating the Transition to TPA* | **Mismatched** (authors omitted) | Urwin, R. et al. (2026), "The Total Portfolio Approach (TPA): A Practical Guide for Navigating the Transition to TPA", CFA Institute Research and Policy Center, DOI 10.56227/26.1.20. The verification log names the authors as Urwin & Hayman; Consensus shows "Roger Urwin et al." | https://consensus.app/papers/details/5ad8650fbd4a59b1837db3c44daac405/?utm_source=claude_desktop |
| 21 | Filbeck & Bok (CAIA/TAI, Oct 2025), *From Vision to Execution: How Investors Are Operationalizing the TPA* | Found via direct fetch (not indexed in Consensus) | The TAI hub page lists "Vision to Execution: How Investors Are Operationalizing the Total Portfolio Approach", "produced in partnership with CAIA Association". It does not show authors or a date; the PDF path contains /2025/10/. Consensus indexes a peer-reviewed companion: Filbeck, A. (2026), "The Total Portfolio Approach: An Emerging Framework for Institutional Portfolio Construction", DOI 10.3905/jpmi.2026.007. | Companion: https://consensus.app/papers/details/e86826579a4c503eaf62f270b8b88e6e/?utm_source=claude_desktop |

**Totals:** 21 checked · 17 found (2 of them outside Consensus) · 3 mismatched · 1 not found.

**Not checked (non-academic sources):** NACUBO, Bain, peer annual reports, press, statutes and policy pages. The verification log covers these.

---

## 3. Annotated bibliography

The 25 papers below are those most relevant to ADIC's design. None is cited in the dossier. They are grouped by theme.

### A. Spending rules and sustainability

**[1] [How to Squander Your Endowment Pitfalls and Remedies](https://consensus.app/papers/details/55c1f0ca96db59ed9c05f005179e7cac/?utm_source=claude_desktop)**
- **Record.** Philip H. Dybvig et al. · 2016 · venue not given in Consensus (working paper) · 13 citations · no DOI shown.
- **Finding.**
  - The common criterion of "spending less than the expected return on endowment is known not to be sufficient to preserve capital".
  - "Smoothing spending is destabilizing and exhausts wealth in finite time".
  - Compounding "may neutralize the preservation-of-capital constraint in optimization models".
- **Relevance (inference).** This undercuts two dossier pillars: the expected-return anchor and Yale-type smoothing (R5). It also warns that the dossier's intergenerational chance constraint can lose its bite inside an optimizer.

**[2] [The Optimal Spending Rate Versus the Expected Real Return of a Sovereign Wealth Fund](https://consensus.app/papers/details/0afc01aa6dda589abcbe616a0651e145/?utm_source=claude_desktop)**
- **Record.** K. Aase et al. · 2021 · *SSRN Electronic Journal* · 6 citations · DOI 10.2139/ssrn.3779850.
- **Finding.** For an SWF whose inflows have stopped:
  - The optimal spending rate is "significantly less than the fund's expected real rate of return".
  - "Spending the expected return will deplete the fund with probability one".
  - That strategy is "inconsistent with optimal portfolio choice".
- **Relevance (inference).** This is the most direct challenge to the dossier's rule $D=\theta\,\mathbb{E}[r^{real}]W$ with θ = 1. It supplies closed-form thresholds for the "distribution-capacity fan" in §6.7. Aase (2024) extends the result to discrete time [S2].

**[3] [Capital Preservation and Current Spending with Sovereign Wealth Funds and Endowment Funds: A simulation Study](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop)**
- **Record.** K. A. Mork et al. · 2022 · *International Journal of Financial Studies* · 4 citations · DOI 10.3390/ijfs10030067.
- **Finding.** Simulating Norway's GPFG:
  - Withdrawals equal to expected real returns still deplete the fund "eventually".
  - Mean reversion from purchasing-power parity means value is "not even preserved in expectation".
  - Using the fund for fiscal policy brings "a substantial risk of depletion in finite time".
  - Smoothing raises depletion risk "only modestly".
  - Lower withdrawal rates help "more fundamentally" than risk reduction.
- **Relevance (inference).** This is a peer-calibrated replacement for the dossier's stylized Monte Carlo. Its fiscal-policy channel is the closest academic analogue of ADIC's owner-demand shocks $\omega_t$.

**[4] [Dynamic spending and portfolio decisions with a soft social norm](https://consensus.app/papers/details/62dbecedd3f75999bcf3364f3ba3f122/?utm_source=claude_desktop)**
- **Record.** K. A. Mork et al. · 2022 (DOI indicates *JEDC* 2023) · *Journal of Economic Dynamics and Control* · 0 citations · DOI 10.1016/j.jedc.2023.104667.
- **Finding.**
  - The preferences splice two CRRA curvatures around a spending norm: high curvature below the norm, low curvature above it.
  - Under these preferences, optimal spending is "significantly lower than the expected financial return" and "mostly also procyclical".
  - Losses should "as a rule" bring larger-than-proportional cuts.
  - Risk-taking should be "modest and procyclical".
  - Simple rules with a constant or slowly moving equity share and consumption–wealth ratio come close in utility.
- **Relevance (inference).** This is a well-posed owner objective for the dossier's §6.4 that avoids the non-positive additive-habit argument (verification R1). It also challenges the assumption that a smoothed payout is what the owner wants.

**[5] [Portfolio Choice with Sustainable Spending: A Model of Reaching for Yield](https://consensus.app/papers/details/b029ce8a702156d8bc5e5d2fde4d3409/?utm_source=claude_desktop)**
- **Record.** J. Campbell et al. · 2020 · *Journal of Financial Economics* per Consensus · 54 citations · DOI shown: 10.2139/ssrn.3527179.
- **Finding.**
  - Imposing a sustainable-spending constraint on an infinitely lived power-utility investor produces "reaching for yield": more risk when the real rate falls with the risk premium unchanged.
  - The effect intensifies when rates are already low.
- **Relevance (inference).** ADIC's 10% target combined with a real-preservation constraint is the setting this paper describes. The framework should test whether the intergenerational chance constraint and the floor push the optimizer into risk in low-rate states. The deck's anti-target-chasing gate is the matching control.

### B. Sovereign owner and SWF practice

**[6] [The Elephant in The Ground: Managing Oil and Sovereign Wealth](https://consensus.app/papers/details/46e0449b577f53ae921bf6ba17efb732/?utm_source=claude_desktop)**
- **Record.** T. S. van den Bremer et al. · 2016 · *European Economic Review* · 42 citations · DOI 10.1016/j.euroecorev.2015.10.005.
- **Finding.**
  - Oil exporters typically ignore below-ground assets when allocating funds.
  - Subsoil oil "should alter a fund's portfolio through additional leverage and hedging".
  - First-best spending is "a share of total wealth".
  - Unhedgeable volatility calls for precautionary savings.
- **Relevance (inference).** This is the formal SWF version of the dossier's Merton argument in §2.2. It justifies an oil hedge and leverage view at the owner's total-wealth level, and it makes precautionary saving a design target.

**[7] [Guidelines for Exploiting Natural Resource Wealth](https://consensus.app/papers/details/cea94823eb04515ea3d29e1288c2af53/?utm_source=claude_desktop)**
- **Record.** R. van der Ploeg · 2014 · *Oxford Review of Economic Policy* · 22 citations · DOI 10.1093/oxrep/gru008.
- **Finding.** The paper recommends three separate funds:
  - an intergenerational SWF to smooth consumption across generations
  - "a liquidity fund for the precautionary buffers to deal with commodity price volatility"
  - an investment fund to hold windfalls until they can be absorbed
- **Relevance (inference).** This maps directly onto ADIC's structure. Corporate Finance/Treasury plays the liquidity fund, and the investment groups play the intergenerational portfolio. It supports a ring-fenced buffer with its own mandate rather than a liquidity floor inside the investment book.

**[8] [Optimal asset allocation for commodity sovereign wealth funds](https://consensus.app/papers/details/2a0ef305e415569e9411d0fbceaa310d/?utm_source=claude_desktop)**
- **Record.** Alfonso A. Irarrazabal et al. · 2020 · *Quantitative Finance* · 4 citations · DOI 10.1080/14697688.2022.2158918.
- **Finding.**
  - A commodity SWF with a non-tradable revenue stream has state- and time-dependent optimal policies.
  - For Norway, the optimal equity share falls gradually from 60% to 40% over 60 years.
  - The solution is "particularly sensitive to the correlation between oil and stock price changes".
  - The paper estimates welfare losses from suboptimal rules.
- **Relevance (inference).** The oil–equity correlation should be an uncertain, regime-dependent state in ADIC's scenario sets, which also drives the wrong-way owner demand. Its welfare-loss metric gives a template for "value of mandate flexibility" (cf. verification R3).

**[9] [Rethinking Fiscal Policy in Oil-Exporting Countries](https://consensus.app/papers/details/ccaefb167453590699fcd4f088e74b02/?utm_source=claude_desktop)**
- **Record.** Tokhir N Mirzoev et al. · 2019 · *IMF Working Papers* · 6 citations · DOI 10.5089/9781498314749.001.
- **Finding.**
  - The permanent income hypothesis "is not consistent with either intergenerational equity or long-term sustainability in the presence of uncertainty".
  - There is "a volatility tradeoff between government spending and wealth".
  - The paper proposes a "prudent wealth stabilization policy".
- **Relevance (inference).** The volatility trade-off is the owner-side version of the dossier's four-dimension frontier in §3.3, and it supports a funded-ratio-feedback rule (R12) over expected-return spending.

**[10] [The Investment Strategies of Sovereign Wealth Funds](https://consensus.app/papers/details/9f43bdf953095cdda0a0fd73b2492820/?utm_source=claude_desktop)**
- **Record.** Shai Bernstein et al. · 2013 · *Journal of Economic Perspectives* · 259 citations · DOI 10.2139/ssrn.1370112.
- **Finding.**
  - SWF direct private-equity investing shows trend chasing.
  - Funds with politicians involved invest more at home and in higher-P/E industries, which see "a negative valuation change in the year after the investment".
  - Funds with external managers do the opposite.
- **Relevance (inference).** Governance input for ADIC's direct and co-investment books (Secondaries' direct leg, Co-investment, Capital Solutions). It argues for structural independence controls, and for IC and agent checks on home bias and trend chasing.

**[11] [Sovereign wealth funds: Past, present and future](https://consensus.app/papers/details/ec86b0b083d55fe8903fa2180b579d47/?utm_source=claude_desktop)**
- **Record.** Salman Bahoo et al. · 2020 · *International Review of Financial Analysis* · 101 citations · DOI 10.1016/j.irfa.2019.101418.
- **Finding.**
  - A meta-literature review of 184 SWF articles from 2005 to 2019.
  - It identifies three research streams: growth, governance and politics, and investment strategies.
  - It proposes 20 research questions.
- **Relevance (inference).** This is the survey or meta-review entry point the dossier lacks. Use it to seed the Peer Calibration agent's reading list. [S27] is a complementary survey.

### C. Illiquidity, private markets and liquidity management

**[12] [Portfolio Choice with Illiquid Assets](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop)**
- **Record.** Andrew Ang et al. · 2014 · *Management Science* · 171 citations · DOI 10.1287/mnsc.2014.1986.
- **Finding.**
  - Illiquidity, meaning no trading for intervals of uncertain length, raises risk aversion in a state-dependent way and reduces allocations to both liquid and illiquid risky assets.
  - Uncertainty about the length of the illiquid interval is "a primary determinant of the cost of illiquidity".
  - Investors would forgo "2% of their wealth to hedge against illiquidity crises occurring once every 10 years".
- **Relevance (inference).** This is a seminal model the dossier omits. It supplies a normal/illiquidity-crisis regime state and a calibration anchor for the value of Treasury's buffer. It also explains why liquid-book risk should fall as the private share rises.

**[13] [Strategic Asset Allocation with Illiquid Alternatives](https://consensus.app/papers/details/e63add9e25485ea691994d7731b433b1/?utm_source=claude_desktop)**
- **Record.** Eric Luxenberg et al. · 2022 · *Proceedings of the Third ACM International Conference on AI in Finance* · 4 citations · DOI 10.1145/3533271.3561769.
- **Finding.**
  - Illiquid dynamics are modelled as a random linear system.
  - A convex model-predictive control (MPC) policy allocates liquid assets and sets new commitments while meeting capital calls "with very high probability".
  - It performs "surprisingly close" to a fictional fully liquid portfolio.
  - Caveat: the paper treats only a growth problem with no external liabilities.
- **Relevance (inference).** This is a direct template for the dossier's lookahead layer in §7. Its convex chance-constrained problem yields dual variables, which answers verification R4. Adding the owner payout as an external liability is the needed extension.

**[14] [Asset Allocation and Private Market Investing](https://consensus.app/papers/details/61e21abbf1425eac88e593ae69993030/?utm_source=claude_desktop)**
- **Record.** Junying Shen et al. · 2021 · *JPM* per DOI · 7 citations · DOI 10.3905/jpm.2021.1.211.
- **Finding.**
  - The framework links bottom-up private cash flows to top-down allocation.
  - It measures the trade-off between allocation, total-portfolio performance and "the frequency of certain liquidity events with different severities".
  - Commitment pacing "plays a crucial role".
- **Relevance (inference).** This is the fix for verification R2: report frequency and severity of external liquidity events rather than "any forced sale". The verification log cites a CPP TPA paper by Shen, Walker and Rubin second-hand; whether it is related to this paper is unconfirmed.

**[15] [The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)**
- **Record.** Taylor D. Nadauld et al. · 2019 · *Journal of Financial Economics* · 66 citations · DOI 10.1016/j.jfineco.2018.11.007.
- **Finding.**
  - Most secondary transactions occur at a discount to NAV.
  - Buyers earn an annualized PME of 1.023 against 0.976 for sellers, about 5 points a year market-adjusted.
  - The pattern fits "relatively flexible buyers" earning returns "by supplying liquidity".
- **Relevance (inference).** This calibrates the SELL action's cost as a forgone return, not only a point discount. It supports the context note that the Secondaries group's opportunity set is richest when sellers are constrained. Transfers between ADIC groups remain zero-sum.

**[16] [Private Equity Performance and Liquidity Risk](https://consensus.app/papers/details/5ca51c749b2d5020a687871b3f3494f8/?utm_source=claude_desktop)**
- **Record.** Francesco Franzoni et al. · 2012 · *Journal of Finance* · 251 citations · DOI 10.1111/j.1540-6261.2012.01788.x.
- **Finding.**
  - PE is exposed to the same liquidity risk factor as public equity, and the unconditional liquidity risk premium is "about 3% annually".
  - Including it "reduces alpha to zero".
  - The link runs through "a funding liquidity channel".
- **Relevance (inference).** Use this to split the α in Dimmock, Wang & Yang into an illiquidity premium and skill (verification R3). It also models PE drawdowns as co-moving with funding stress, the same state in which owner demand rises.

**[17] [Liquidity and Portfolio Choice: A Unified Approach](https://consensus.app/papers/details/87606279740d57b4b0350e859446911b/?utm_source=claude_desktop)**
- **Record.** W. Kinlaw et al. · 2013 · *The Journal of Portfolio Management* · 29 citations · DOI 10.3905/jpm.2013.39.2.019.
- **Finding.**
  - Liquidity is valued by attaching a "shadow asset" to tradable assets, for using liquidity to raise utility, and a "shadow liability" to non-tradable assets, for using it to stop utility falling.
  - Liquidity serves "to exploit opportunities as well" as to meet demands.
- **Relevance (inference).** This turns the dossier's one-sided internal transfer price into a two-sided one. Illiquid users are charged, and liquid "dry powder" is credited with its option value (context §1A, point 5).

### D. Endowment evidence that bears on the dossier's premises

**[18] [Do (Some) University Endowments Earn Alpha?](https://consensus.app/papers/details/e20b626bfad15b03998153551d51d571/?utm_source=claude_desktop)**
- **Record.** B. Barber et al. · 2013 · *Financial Analysts Journal* · 40 citations · DOI shown: 10.2139/ssrn.1972317.
- **Finding.**
  - The average endowment matches 60/40, with alpha close to zero.
  - Elite endowments earn 2–4% against stock/bond benchmarks, but alpha is "indistinguishable from zero" once hedge-fund and PE indices are added.
  - There is no evidence that manager selection, timing or tactical allocation generate alpha.
- **Relevance (inference).** A prior for "endowment-model premium" should be modelled as compensation for allocation to alternatives, not as manager alpha. This sharpens the dossier's Ennis-based prior.

**[19] [The Modern Endowment Story: A Ubiquitous US Equity Factor](https://consensus.app/papers/details/1f9d4a1f4c655378896d119c4e3e763f/?utm_source=claude_desktop)**
- **Record.** Richard M. Ennis · 2022 · *JPM* per DOI · 1 citation · DOI 10.3905/jpm.2022.1.402.
- **Finding.**
  - Large endowments underperformed by 2.24–2.5% a year over the 13 years to 30 June 2021.
  - Costs are about 2.5% of assets.
  - In the "Modern Era", effective US equity exposure was 97% of asset value.
- **Relevance (inference).** ADIC's private book, about 60% and mostly PE, should be desmoothed and mapped to equity beta before any diversification credit is given. Total-portfolio drawdown risk is probably understated by the appraisal-based ~12% volatility used in the dossier's cases.

**[20] [The Impact of Endowment Shocks on Payouts](https://consensus.app/papers/details/30db9b06ea85503da3e4097350b48651/?utm_source=claude_desktop)**
- **Record.** H. Rosen et al. · 2019 · *The Journal of Higher Education* · 7 citations · DOI 10.1080/00221546.2019.1621115.
- **Finding.** In panel data on over 700 universities from 1987 to 2009, "payouts are affected symmetrically by positive and negative shocks".
- **Relevance (inference).** This contradicts the Brown et al. (2014) "hoarding" asymmetry that the dossier uses in §1.5 and §2.6 to argue that discretion is asymmetric. Pre-commitment can still be defended on time-consistency grounds, but the empirical premise is contested (§5, C3).

### E. Control and actuarial formulations for payout rules

**[21] [Stable dividends under linear-quadratic optimisation](https://consensus.app/papers/details/30129b0d5c79520493164fbe12693874/?utm_source=claude_desktop)**
- **Record.** Benjamin Avanzi et al. · 2022 · *Quantitative Finance* · 4 citations · DOI 10.1080/14697688.2023.2227661.
- **Finding.**
  - De Finetti-type value maximization yields barrier strategies that are "far from stable".
  - Under a linear-quadratic (LQ) criterion that demands stability, the optimal dividend strategies are affine. The value function is characterized by the HJB equation.
- **Relevance (inference).** This gives formal backing to the dossier's claim that R12, a linear state-feedback rule, is the LQ-optimal form (verification R8 asks for this to be labelled "linearized"). It also offers a closed-form seed for R12 gains.

**[22] [Optimal Dividend Distribution Under Drawdown and Ratcheting Constraints on Dividend Rates](https://consensus.app/papers/details/e6348825f6545115aa58b7a157594835/?utm_source=claude_desktop)**
- **Record.** Bahman Angoshtari et al. · 2018 · *SIAM J. Financial Math.* · 30 citations · DOI 10.1137/18m119567x.
- **Finding.**
  - The dividend rate may not fall below a proportion of its historical maximum.
  - This extends Dybvig's (1995) ratchet to the case where ruin can occur.
  - The optimal rate depends on surplus and the running maximum.
- **Relevance (inference).** This is a well-posed, owner-facing stability guarantee (payout drawdown ≤ x%) that can replace the ill-posed additive habit with h = 0.8 (verification R1) and the heuristic ratchet R8 (verification R9). It needs the running-maximum payout as a state variable.

### F. TPA, governance and agentic architecture

**[23] [Applying the Appraisal Ratio and Style Analysis to Total Portfolio Management](https://consensus.app/papers/details/8f465e83b0145ab38206b8fc4524c280/?utm_source=claude_desktop)**
- **Record.** Stefano Cavaglia et al. · 2026 · *JPM* per DOI · 0 citations · DOI 10.3905/jpm.2026.1.824.
- **Finding.**
  - The appraisal ratio measures "the maximum Sharpe ratio improvement from the inclusion of an asset to the reference portfolio".
  - The paper applies it to PE and builds PE style-factor models to project expected returns.
  - The method generalizes to multi-asset, multi-strategy TPA allocations.
- **Relevance (inference).** This is a ready-made, testable form of the deck's α* hurdle and of the SELL/HOLD test for existing holdings against the reference portfolio.

**[24] [Freedom within a Framework: Governing Portfolio Decisions during Regime Shifts](https://consensus.app/papers/details/a7ed0e12f98957ff9d685c676a6dec99/?utm_source=claude_desktop)**
- **Record.** Brian Jacobsen · 2026 · *JPM* per DOI · 0 citations · DOI 10.3905/jpm.2026.005.
- **Finding.**
  - The paper proposes a "pre-committed governance smart contract" embedded in policy documents.
  - It specifies how constraints, oversight, communication cadence and decision rights "adjust automatically as uncertainty increases".
  - It combines robust estimation, regime diagnostics and adaptive decision rights.
- **Relevance (inference).** This is the governance counterpart of the deck's model-confidence threshold and Tier 1 gate. Encode in the IPS which IC decision rights tighten when the state engine's confidence falls, so agent behaviour is rule-based and auditable.

**[25] [The Self Driving Portfolio: Agentic Architecture for Institutional Asset Management](https://consensus.app/papers/details/b737594b0f20537d91819356dfe05f75/?utm_source=claude_desktop)**
- **Record.** Andrew Ang et al. · 2026 · *arXiv* · 0 citations · DOI 10.48550/arxiv.2604.02279.
- **Finding.** The pipeline:
  - 44 specialized agents produce capital market assumptions.
  - Portfolios are built with 21 competing methods; agents critique and vote on each other's outputs.
  - A researcher agent proposes new methods.
  - A meta agent compares past forecasts with realized returns and rewrites agent code and prompts.
  - The whole pipeline is governed by the IPS.
- **Relevance (inference).** This is the closest published analogue of ADIC's planned orchestrator. Adopt its forecast-versus-realized scoring per agent, which mirrors the group-forecast credibility estimation in context §1A, and its IPS-as-constraint pattern. Its self-rewriting loop needs the deck's rule that deterministic models own the numbers.

---

## 4. Missed-but-important papers: design implications

[n] refers to §3; [Sn] refers to the supplementary table in §4.8. All mappings to ADIC are *(inference)*.

### 4.1 State variables to add or change

| State | Specification | Source |
|---|---|---|
| Owner total wealth and fiscal space | Oil price or revenue, the owner's buffer or fiscal-space level, and a regime-dependent oil–equity correlation ρ. Use these to drive the owner shock $\omega_t$ instead of a scalar $O_t$. | [6] spending as "a share of total wealth" including subsoil oil; [8] sensitivity to the oil–stock correlation; [S24] constrained GCC economies draw buffers down in oil busts; [S25] decisions as a function of fund level and oil revenue |
| Liquidity regime with random duration | Normal versus illiquidity crisis, in which some assets "can only be traded infrequently" for intervals of uncertain length. Tie PE returns and secondary discounts to a funding-liquidity factor. This replaces the fixed 25% crisis discount in §3.3. | [12], [16] |
| Commitment pipeline | A random linear system for calls, distributions and NAV per vintage, with unfunded commitments carried as priced liabilities | [13], [S36] |
| Payout memory | The running maximum of real distributions (for a drawdown constraint) or an exponentially weighted habit (for a habit-formation constraint), not only $D_{t-1}$ | [22], [S46] |
| Factor state of the private book | Desmoothed equity beta, with factor exposures measured consistently for liquid and illiquid holdings | [19] (97% effective US equity), [S64] |
| Rule-revision state | Spending rules are revised often in practice, so treat θ as subject to revision risk and political override | [S11] (about a quarter of endowments change policy each year) |

### 4.2 Models and solvers

- **Lookahead layer.** Use MPC with convex chance constraints for commitments plus liquid allocation [13], extended with the owner payout as a liability.
  - It yields dual variables for the liquidity constraint.
  - Those duals are the internal liquidity transfer price that enters α*, answering verification R4.
- **Payout-rule family.**
  - Seed R12 with LQ-affine rules: [21] and the pension spreading literature ([S48]; Owadally & Haberman 2004, already cited).
  - Add a drawdown-constrained variant [22].
  - Add a ruin-probability-constrained barrier variant [S49].
- **Analytic cross-checks on the Monte Carlo.** Use closed-form sustainable-spending thresholds ([2], [S2]) and the stochastic-present-value approximation [S9]. These catch simulator errors cheaply.
- **Owner-demand agent's utility.** Use soft-social-norm preferences, which splice two CRRA curvatures [4].
- **TPA test for every holding.** Measure the appraisal ratio against the reference portfolio and use a PE style-factor model for expected returns [23], with a consistent factor lens across liquid and illiquid assets [S64].
- **Policy-parameter search.**
  - Bayesian optimization of feedback parameters has been used for funding-ratio-adjustment rules [S51]. It is an alternative to CMA-ES or Optuna that is cheaper per evaluation.
  - Report the "economic cost" of each constraint, as done for stochastic-dominance constraints in multistage pension ALM [S57]. This is a defensible estimator for the dossier's floor and cap "shadow prices".
- **Pacing baselines.**
  - Dynamic recommitment rules [S37], and explainable evolutionary recommitment strategies [S42].
  - Pausing commitments as an alternative to forced sales [S38].

### 4.3 Parameters and calibration anchors

| Parameter | Anchor from the literature | Source |
|---|---|---|
| SELL cost of secondary sales | Buyer PME 1.023 vs seller 0.976, about 5 points a year market-adjusted; most trades at a discount to NAV | [15] |
| Illiquidity premium vs skill | PE liquidity-risk premium about 3% a year; alpha falls to zero once it is included | [16] |
| Value of Treasury's buffer | About 2% of wealth to hedge one illiquidity crisis per decade | [12] |
| Private allocation range | Breakeven-consistent "PE allocations up to 40%" for moderately risk-tolerant LPs; about 30% overcommitment needed during build-up | [S35], [S37] |
| Endowment-model premium (prior) | The anchors: alpha about 0 once alternatives are benchmarked [18]; −1.10% a year for non-profit endowments [S17]; −2.15% (range −1.26% to −3.15%) after true-risk adjustment [S16]; −2.24% to −2.5% with about 2.5% costs [19]. The counterpoints are [S18] and [S19]. | as listed |
| LP skill and scale | +1–2 points a year per standard deviation of LP skill; larger PE holdings associated with higher returns; low-cost direct and co-investment beat fund-of-funds | [S33], [S32], [S34] |
| Sovereign-LP effects | SWFs "significantly slower to fully liquidate" and earn lower returns, especially strategic SWFs; use as a prior on DPI timing for sovereign LPs | [S29] |
| Spending sustainability | Optimal spending "significantly lower" than the expected real return; 4–5% spending already demanding against market history | [2], [4], [S8] |
| Band design | Snake-in-the-tunnel bands of 3–7% reduce short-run cuts while preserving real purchasing power | [S5] |

### 4.4 Constraints

- **Liquidity events.**
  - Replace "P(any forced secondary sale) ≤ 5%", which verification R2 shows is set by the floor, with frequency-and-severity limits on external events: a missed owner payment, an unmet call, or unmet margin [14].
  - Optionally add a ruin-probability constraint on distributions [S49].
- **Payout stability.** Impose a drawdown constraint $D_t \ge \alpha \max_{s<t} D_s$, with ruin possible [22], as the owner-facing guarantee. This replaces the additive habit $u(D_t-hD_{t-1})$.
- **Capital-call coverage.** Calls must be met "with very high probability" inside the MPC [13]. This is the same object as the dossier's distribution coverage ratio, made optimizable.
- **Robust floor relative to the reference portfolio.** Consider a stochastic-dominance constraint against the reference portfolio [S57][S58] as a formal alternative to the 7% worst-case floor. Report its economic cost.
- **Leverage.**
  - Add a leverage-tolerance term or limit that captures margin-call and forced-liquidation risk, which variance misses [S44].
  - Stress-test leverage against frictions [S45].
- **Fiscal overrides.** Flag explicitly any withdrawal above the sustainable path. Fiscal gap-filling compromises SWF performance [S26], and fiscal use of a fund creates depletion risk [3].

### 4.5 Objectives

- **The 5–10% band as an EW–ES problem.** Maximize expected cumulative real withdrawals (EW) plus the expected shortfall (ES) of terminal real NAV, subject to a withdrawal cap and floor [S50]. This maps one-to-one onto ADIC's 5–10% band.
- **Two risks, as in pension funding.** The pension literature trades contribution-rate risk against solvency risk [S48]. For ADIC these become distribution-volatility risk and NAV solvency. A quadratic version gives the LQ rule in [21].
- **Owner utility.** Use a soft social norm [4] or a habit-formation constraint [S46] in place of the ill-posed additive habit (verification R1).
- **Drawdown first.** The board sets the tolerable drawdown first; the benchmark and tracking-error budget follow. A dynamic budget adds value at the same drawdown [S61].
- **Goal probability.** Use the probability of meeting both the spending target and real-capital preservation as an SAA criterion [S10]. This is consistent with the deck's target-attainment probability.

### 4.6 Agent and IC design

- **Governance smart contract [24].** Write in the IPS how constraints and decision rights tighten as model confidence falls. Agents read it, and the IC overrides are logged against it.
- **Benchmark architecture [25].** Use competing methods, cross-agent critique and voting, and per-agent forecast-versus-realized scoring, all under the IPS. Keep the deck's rule that deterministic code owns the numbers, and do not allow self-rewriting to touch the numerical models without human sign-off.
- **Delegated benchmarks [S60].** The board anchors the total-fund benchmark; the investment executive designs mandate-level benchmarks. This suits the seven groups and is argued to reduce benchmark gaming.
- **Policy versus strategy [S68], best practice [S66], IC expertise and networks [S67].** The IC or board owns policy, meaning risk and liquidity. Strategy is delegated. Record which IC seats hold which expertise.
- **Political-involvement penalty ([10], [S28]).** Add conflict-of-interest guardrails for owner-directed or home-market deals, alongside the quote controls already planned for Secondaries and Capital Solutions.
- **Generational representation [S56].** Repeated bargaining among the generations represented on a board favours older generations over the social optimum. Add a "future generations" advocate role to the shadow IC to balance the Owner-Demand Scenario agent.
- **Phased TPA transition ([S62], [S63]).** Sequence the change across five areas: people and culture, risk management, asset allocation, delegation of authorities, and measures of success.

### 4.7 Group-specific notes

- **Corporate Finance / Treasury (confirmed owner of Treasury):**
  - [7] is the liquidity-fund mandate.
  - [S25] suggests tranching the buffer by asset duration rather than holding it all short-term.
  - [17] supports a two-sided transfer price that also credits dry powder.
  - [12] gives the buffer's insurance value.
  - [S41]: borrowing "to pay for a liquidity shock cannot overcome all of the costs" of illiquid assets, while borrowing at t = 0 "benefits from the complementarity". This argues for committed facilities arranged in advance.
- **Secondaries (confirmed hybrid of direct and fund investments):**
  - [15]: flexible buyers earn a liquidity-provision return.
  - [S40]: LPs with more tolerance for illiquidity realize higher returns, and a secondary market attenuates fund-level but not LP-level differences.
  - Model the direct leg (LP-portfolio purchases and GP-led continuation vehicles) and the fund leg separately. Their forecasts and the timing of their cash returns differ.
- **Co-investment:**
  - The evidence conflicts. [S30] finds co-investments underperform because GPs selectively offer large deals. [S31] finds no adverse selection and lower costs.
  - So deal-model forecasts need a selection-bias term with a wide prior.
  - [S32] and [S34] document cost advantages of direct programs.
- **PE (fund allocator):** use [S29] for sovereign-LP liquidation timing, [S37] for recommitment, and [S38] for pausing commitments instead of selling.
- **Overlay:**
  - [S65] integrates a factor overlay with the reference portfolio and "levering existing asset class or active management exposures".
  - [S58] uses put options inside a multistage ALM with stress scenarios.
  - Weigh leverage benefits [S43] against frictions [S45].

### 4.8 Supplementary papers (not annotated)

All entries are surfaced in this run's Consensus results and are taken from their abstracts. Format: [Title](exact URL), first author et al., year, venue, then one line of relevance.

**Spending rules and sustainability**
- **S1** [Where's Tobin? Protecting Intergenerational Equity for Endowments: A New Benchmarking Approach](https://consensus.app/papers/details/6f0f965869fc5a6484046604ce849a01/?utm_source=claude_desktop), M. Waring et al., 2022, DOI 10.3905/jpm.2022.1.424. "Smoothing does not make risk go away; it just hides it for a while, deferring it to a later generation."
- **S2** [Optimal Spending Strategies for Sovereign Wealth Funds Using a Discrete-Time Life Cycle Model](https://consensus.app/papers/details/b92a25866b5350709012a3b8f6d1047b/?utm_source=claude_desktop), K. Aase, 2024, *JRFM*, DOI 10.3390/jrfm17080327. Spending the expected real return makes value deteriorate "both in probability and in expectation"; gives closed-form thresholds.
- **S3** [Investing it, spending it: Interactions between Spending and Investment Decisions with a Sovereign Wealth Fund](https://consensus.app/papers/details/4b0cbd1e3f6152dabbfc2426b72b0c14/?utm_source=claude_desktop), Snorre Lindset et al., 2016. Spending and investment cannot be separated; "short-run smoothing raises the long-term variability of spending"; risk-adjust annuity rules.
- **S4** [Institutional spending policies: implications for future asset values and spending](https://consensus.app/papers/details/3593da4a425f559fb5adbd1dffb87af9/?utm_source=claude_desktop), Snorre Lindset et al., 2018, *FMPM*, DOI 10.1007/s11408-018-0304-9. The covariance between returns and the spending rate matters; smoothing policies can deplete funds.
- **S5** [Evaluating Spending Policies in a Low-Return Environment](https://consensus.app/papers/details/c6c980011c485d7b9f5d75004167b9cc/?utm_source=claude_desktop), Peng Wang et al., 2018, *FAJ*, DOI 10.2469/faj.v74.n4.1. Snake-in-the-tunnel bands of 3–7% versus moving averages.
- **S6** [Optimal portfolio and spending rules for endowment funds](https://consensus.app/papers/details/f11a9145a77b5305bdf13f26c640edcb/?utm_source=claude_desktop), Muhammad Kashif et al., 2020, *RQFA*, DOI 10.1007/s11156-019-00856-x. Under a hybrid (smoothed) rule the optimal portfolio is less risky and spending less volatile, but returns lag in strong markets.
- **S7** [Efficiency of institutional spending and investment rules](https://consensus.app/papers/details/a5f4dbe3b5fa53c5ba527f35bdcae893/?utm_source=claude_desktop), J. Schumacher, 2019, *Scand. Actuarial J.*, DOI 10.1080/03461238.2019.1685589. Fixed-mix with inflation-indexed benefits is often inefficient, losing 5–15% of capital. Supports rejecting fixed real amounts.
- **S8** [The Sustainability of Endowment Spending Levels: A Wake-up Call for University Endowments](https://consensus.app/papers/details/061e20dc6acd512b9373622f45a06118/?utm_source=claude_desktop), Gregory Ho et al., 2010, *JPM*, DOI 10.3905/jpm.2010.37.1.133. Gives an upper bound on volatility for a given spending rate; 4–5% spending needs above-market returns.
- **S9** [A Sustainable Spending Rate without Simulation](https://consensus.app/papers/details/8c2a498f58f052c68632ce60ac2b8ba3/?utm_source=claude_desktop), M. Milevsky et al., 2005, *FAJ*, DOI 10.2469/faj.v61.n6.2776. A reciprocal-gamma stochastic-present-value approximation, usable as an analytic check on Monte Carlo.
- **S10** [Strategic Asset Allocation for Endowment Funds](https://consensus.app/papers/details/c03cd55b21a152c59cae91f3817636a8/?utm_source=claude_desktop), K. Jacobs et al., 2021, DOI 10.3905/jpm.2021.1.227. Uses the probability of meeting both the spending target and capital preservation as an SAA criterion; private-asset limits come from liquidity and manager access.

**Endowment behaviour and evidence**
- **S11** [The Interaction of Spending Policies, Asset Allocation Strategies, and Investment Performance at University Endowment Funds](https://consensus.app/papers/details/dbb718a2963d55a1b5ae773ef65f8950/?utm_source=claude_desktop), K. Brown et al., 2013, NBER, DOI 10.3386/w19517. Half of endowments revised their rules at least once, about a quarter each year; rule changes lead allocation changes.
- **S12** [Why I Lost My Secretary: The Effect of Endowment Shocks on University Operations](https://consensus.app/papers/details/d68ad94aa01e5f5a8ab704fb7d1d65e5/?utm_source=claude_desktop), Jeffrey R. Brown et al., 2010, NBER WP 15861. Less liquid endowments (more alternatives) made larger operating cuts after negative shocks.
- **S13** [Seventy-Five Years of Investing for Future Generations](https://consensus.app/papers/details/3cc939a9b2035c5fb75ebc1b198bb14b/?utm_source=claude_desktop), D. Chambers et al., 2020, *FAJ*, DOI 10.1080/0015198x.2020.1802984. Endowments invested countercyclically in crises, raising risky allocations afterwards. Supports valuing dry powder.
- **S14** [Background Risk and University Endowment Funds](https://consensus.app/papers/details/bba5c539ac5d59f7bd809353cc8c9dbf/?utm_source=claude_desktop), Stephen G. Dimmock, 2012, *REStat*, DOI 10.1162/rest_a_00180. Higher background (non-financial income) risk goes with less portfolio risk and fewer alternatives. For ADIC the owner's oil revenue is the background risk *(inference)*.
- **S15** [What Constitutes Prudent Spending from Private College Endowments? Evidence from Underwater Funds](https://consensus.app/papers/details/426ee4ea4c2852a2adfb7de8adce7c9b/?utm_source=claude_desktop), Drew M. Anderson, 2017, *EFP*, DOI 10.1162/edfp_a_00239. Legal flexibility (UPMIFA) raised post-crisis spending by 22%. Mandate text matters.
- **S16** [The Challenge of Endowment Performance Evaluation](https://consensus.app/papers/details/f8ace350da5a5927a035972a2dd057c4/?utm_source=claude_desktop), Mitchell A. Bollinger, 2021, SSRN, DOI 10.2139/ssrn.3725201. Appraisal-based assets understate true risk; alpha for 2009–2019 is −2.15% (range −1.26% to −3.15%).
- **S17** [Investment Returns and Distribution Policies of Non-Profit Endowment Funds](https://consensus.app/papers/details/29f235eb3fde5076bef2c349f8f51aaa/?utm_source=claude_desktop), Sandeep Dahiya et al., 2018, NBER, DOI 10.2139/ssrn.3291117. Covers 29,762 endowments; alpha −1.10% a year; distribution ratios conservative.
- **S18** [Don't Give Up the Ship: The Future of the Endowment Model](https://consensus.app/papers/details/ac7b6c905c475888b1379306cbeb7c70/?utm_source=claude_desktop), Laurence B. Siegel, 2021, DOI 10.3905/jpm.2021.1.221. Counterpoint: structural advantages; recent underperformance partly reflects strong US stocks and bonds.
- **S19** [Surprise, Endowments Have Significantly Outperformed the 60/40 Benchmark](https://consensus.app/papers/details/204d336fbcb05d2c8db715551b09063c/?utm_source=claude_desktop), Hossein Kazemi, 2020. Counterpoint: underperformance results are "not robust and entirely dependent on the assumptions made".
- **S20** [A Better Approach to Systematic Outperformance? 58 Years of Endowment Performance](https://consensus.app/papers/details/30073dfd53795c06b3d5ae7cfae8cc47/?utm_source=claude_desktop), Dennis R. Hammond, 2020, DOI 10.3905/joi.2020.1.138. The average endowment missed its annual return need and long-term goal over 58 years.
- **S21** [COMMENTARY: Problems with the Endowment Model](https://consensus.app/papers/details/b0b4ae46d845589da35f2f7b428a5c68/?utm_source=claude_desktop), Richard M. Ennis, 2021, DOI 10.3905/joi.2021.1.186. Asset classes have become "silos, tantamount to quotas". Consistent with the dossier's advice to avoid quotas.
- **S22** [Pioneering Portfolio Management: An Unconventional Approach to Institutional Investment](https://consensus.app/papers/details/d328cb2d5eb7533fa6422645d19d353f/?utm_source=claude_desktop), David F. Swensen, 2000, 229 citations. The seminal statement of the endowment model; not cited in the dossier.

**Sovereign owner and SWF practice**
- **S23** [The Future of Oil and Fiscal Sustainability in the GCC Region](https://consensus.app/papers/details/0c1a8a274def54a5a22530f8bfd6103b/?utm_source=claude_desktop), Tokhir N Mirzoev et al., 2020, IMF, DOI 10.5089/9781513525907.087. Global oil demand is expected to peak within two decades, so the fiscal imperative may be "larger and more urgent". Use as a structural owner-demand scenario.
- **S24** [Institutions and macroeconomic stability under oil price shocks: Evidence from the GCC](https://consensus.app/papers/details/b100f501a743599d92c00223557b79d8/?utm_source=claude_desktop), Showkat Ahmad Shah et al., 2026, *NAJEF*, DOI 10.1016/j.najef.2026.102702. High-fiscal-space economies build buffers countercyclically while constrained ones draw them down, especially in busts.
- **S25** [Optimal policies for managing oil revenue stabilization funds: An illustration using Saudi Arabia](https://consensus.app/papers/details/4ab7b0395f8c5e7a97e025705b41a642/?utm_source=claude_desktop), Nader AlKathiri et al., 2020, *Resources Policy*, DOI 10.1016/j.resourpol.2020.101686. A stabilization fund can be "partitioned into tranches with different asset durations".
- **S26** [Sovereign Wealth Fund Investment Performance, Strategic Asset Allocation, and Funding Withdrawal Rules](https://consensus.app/papers/details/2b4c462b545a58e3ae8f9d60e1196d5c/?utm_source=claude_desktop), Michael G. Papaioannou et al., 2018, DOI 10.1007/978-3-319-90245-6_4. Strong operating frameworks are needed to "avoid a fiscal gap-filling function" that compromises performance.
- **S27** [Rise of the Fiduciary State: A Survey of Sovereign Wealth Fund Research](https://consensus.app/papers/details/f473ce702e4e5dd697b1697359cff9ec/?utm_source=claude_desktop), W. Megginson et al., 2014, *J. Economic Surveys*, DOI 10.2139/ssrn.2432623. SWF survey covering normative allocation, actual allocation and the "SWF discount".
- **S28** [The Sovereign Wealth Fund Discount: Evidence from Public Equity Investments](https://consensus.app/papers/details/472c2665eed25e73865fa895a9da6f15/?utm_source=claude_desktop), Bernardo Bortolotti et al., 2015, *RFS*, DOI 10.1093/rfs/hhv036. Larger discounts come with board seats and strict government control.
- **S29** [Sovereign wealth fund investment in venture capital, private equity, and real asset funds](https://consensus.app/papers/details/a7ab7e6e279559f89930773cb5d6969c/?utm_source=claude_desktop), Douglas J. Cumming et al., 2023, *JIBP*, DOI 10.1057/s42214-023-00162-3. SWFs are slower to fully liquidate and earn lower returns, especially strategic SWFs.

**Private markets, direct investing and liquidity**
- **S30** [The Disintermediation of Financial Markets: Direct Investing in Private Equity](https://consensus.app/papers/details/4e0c268caabc5b468d053656985a3deb/?utm_source=claude_desktop), Lily H. Fang et al., 2014. Solo direct deals outperform; co-investments underperform because of GPs' selective offering of large deals.
- **S31** [Adverse selection and the performance of private equity co-investments](https://consensus.app/papers/details/74305f05d7e758dfbc4c1b624c2fa5db/?utm_source=claude_desktop), Reiner Braun et al., 2020, *JFE*, DOI 10.2139/ssrn.2871458. No adverse selection; lower costs; co-investment portfolios beat funds.
- **S32** [Investor Scale and Performance in Private Equity Investments](https://consensus.app/papers/details/a99ce133c0c85d79a0503a83dd907c3b/?utm_source=claude_desktop), I. J. Alexander Dyck et al., 2016, *RoF*, DOI 10.2139/ssrn.2192619. One standard deviation more PE holdings goes with 4% a year higher returns; up to a third comes from lower costs and direct investing.
- **S33** [Measuring Institutional Investors' Skill at Making Private Equity Investments](https://consensus.app/papers/details/ce8a4e711b4e52be85a0d0b03ffe44dd/?utm_source=claude_desktop), Daniel R. Cavagnaro et al., 2019, *JF*, DOI 10.1111/jofi.12783. One standard deviation of LP skill adds 1–2 points a year.
- **S34** [Benchmarking the Performance of Private Equity Portfolios of the World's Largest Institutional Investors: A View from CEM Benchmarking](https://consensus.app/papers/details/64a6b1933e72521789155b89b5399519/?utm_source=claude_desktop), A. Beath et al., 2020, DOI 10.3905/joi.2020.1.155. Average net value added −0.67% against lagged small-cap; internal direct and co-investment beats fund-of-funds.
- **S35** [How much for a haircut? Illiquidity, secondary markets, and the value of private equity](https://consensus.app/papers/details/54f4236e9f8c57449fe7b869413531ab/?utm_source=claude_desktop), Nicolas P. B. Bollen et al., 2016, *Financial Management*, DOI 10.2139/ssrn.2608549. Breakeven returns match observed returns for "PE allocations up to 40%".
- **S36** [Optimal Allocation to Private Equity](https://consensus.app/papers/details/c662a34c96985552862c991bf5b1d1a9/?utm_source=claude_desktop), Nicola Giommetti et al., 2021, SSRN, DOI 10.2139/ssrn.3761243. Repeated commitments and a secondary market; prices NAV and unfunded liabilities.
- **S37** [Private Equity Recommitment Strategies for Institutional Investors](https://consensus.app/papers/details/63deabfca2f15e65880fa9a8f5d03a13/?utm_source=claude_desktop), G. D. de Zwart et al., 2012, *FAJ*, DOI 10.2469/faj.v68.n3.1. A dynamic recommitment rule reaches 86% of target with an 8% chance of being overinvested.
- **S38** [Managing Illiquidity in Open-Ended Funds with Private Asset Allocations: Challenges and Solutions](https://consensus.app/papers/details/12cd077c32a755c9bbab6ea80a91706c/?utm_source=claude_desktop), Raul Leote de Carvalho et al., 2026, DOI 10.3905/jpmi.2026.002. "Suspending future commitments can rebalance the portfolio without forced secondary sales."
- **S39** [Integrating private assets in a total portfolio approach](https://consensus.app/papers/details/129e1fa8557c5944852b405eac05dc19/?utm_source=claude_desktop), Thomas Meyer, 2025, *J. Securities Operations & Custody*, DOI 10.69554/tfxb7809. Owners "may be overestimating their liquidity needs"; the cost of illiquidity depends on the portfolio's state.
- **S40** [A Theory of Liquidity in Private Equity](https://consensus.app/papers/details/0b0a7e06da845c6fbcd935f64cb4bb99/?utm_source=claude_desktop), Vincent Maurin et al., 2022, *Management Science*, DOI 10.1287/mnsc.2022.4612. LPs that tolerate illiquidity realize higher returns; GPs may accelerate drawdowns.
- **S41** [Integrating Illiquid Assets into the Portfolio Decision Process](https://consensus.app/papers/details/29f5d1f3ce855a36b86e0c22a1ef2f0c/?utm_source=claude_desktop), P. Anglin et al., 2011, *Real Estate Economics*, DOI 10.1111/j.1540-6229.2010.00291.x. Borrowing at the time of a shock cannot overcome all illiquidity costs; borrowing at t = 0 benefits from complementarity.
- **S42** [Learning private equity recommitment strategies for institutional investors](https://consensus.app/papers/details/1a08544fb5305532bc1270a2b91fa377/?utm_source=claude_desktop), Emmanuel Kieffer et al., 2023, *Frontiers in AI*, DOI 10.3389/frai.2023.1014317. Explainable evolutionary computing designs recommitment strategies.

**Leverage**
- **S43** [Leverage Aversion and Risk Parity](https://consensus.app/papers/details/3544dc48133655e39cf2c08067e8b2da/?utm_source=claude_desktop), Clifford S. Asness et al., 2012, *FAJ*, DOI 10.2469/faj.v68.n1.1. Leverage aversion leaves a premium for investors able to lever.
- **S44** [Leverage Aversion, Efficient Frontiers, and the Efficient Region](https://consensus.app/papers/details/98eedaf2d152557ca41ba243c6fc690b/?utm_source=claude_desktop), B. Jacobs et al., 2013, *JPM*, DOI 10.3905/jpm.2013.39.3.054. Adds leverage aversion to mean–variance, with "a large effect on an investor's portfolio choice".
- **S45** [Will My Risk Parity Strategy Outperform?](https://consensus.app/papers/details/efc234a01031512da8540369cc25e099/?utm_source=claude_desktop), R. M. Anderson et al., 2012, *FAJ*, DOI 10.2469/faj.v68.n6.7. After frictions, levered risk parity underperformed; leverage exacerbates frictions.

**Control, actuarial and intergenerational risk sharing**
- **S46** [Optimal Investment and Consumption under a Habit-Formation Constraint](https://consensus.app/papers/details/761d81de16205348aa54171a5869c7dd/?utm_source=claude_desktop), Bahman Angoshtari et al., 2021, *SIAM J. Financial Math.*, DOI 10.1137/21m1397891. Consumption must stay at least α × habit, with addictive and non-addictive cases. A well-posed alternative to additive habit.
- **S47** [Exponential smoothing methods in pension funding](https://consensus.app/papers/details/6a89d1b78e035e6ea48421e4e11197a6/?utm_source=claude_desktop), M. I. Owadally et al., 2003, *IMA J. Management Mathematics*, DOI 10.1093/imaman/14.2.129. Smoothing helps "up to a point", but "excessive smoothing is inefficient". Relevant to the choice of NAV basis.
- **S48** [Dynamic approaches to pension funding](https://consensus.app/papers/details/5ee699fcb2585e57a1197923d22c5571/?utm_source=claude_desktop), S. Haberman et al., 1994, *IME*, DOI 10.1016/0167-6687(94)90791-9. Minimizes contribution-rate risk and solvency risk together.
- **S49** [Optimal Dividend Payment in De Finetti Models: Survey and New Results and Strategies](https://consensus.app/papers/details/e65363a4d05f591cbec938d66a9ba738/?utm_source=claude_desktop), C. Hipp, 2020, *Risks*, DOI 10.3390/risks8030096. Optimal dividends subject to a cap on ruin probability; two-barrier strategies.
- **S50** [Optimal control of the decumulation of a retirement portfolio with variable spending and dynamic asset allocation](https://consensus.app/papers/details/1e3d85c4dfdf57b99ec6ee3afd9a10cc/?utm_source=claude_desktop), P. Forsyth et al., 2021, *ASTIN Bulletin*, DOI 10.1017/asb.2021.19. The EW–ES objective with a cap and floor on withdrawals.
- **S51** [Intergenerational risk sharing in a defined contribution pension system: analysis with Bayesian optimization](https://consensus.app/papers/details/85e4259f224d57568151dee91714274b/?utm_source=claude_desktop), An Chen et al., 2021, *ASTIN Bulletin*, DOI 10.1017/asb.2023.18. An adjustment rule tied to the funding ratio, with its parameters found by Bayesian optimization.
- **S52** [Structure of intergenerational risk-sharing plans: optimality and fairness](https://consensus.app/papers/details/3aed488b5ea958d9acbe6f1f6289658f/?utm_source=claude_desktop), X. Zhu et al., 2020, *Scand. Actuarial J.*, DOI 10.1080/03461238.2020.1862291. A linear risk-sharing protocol with funding-level constraints is transparent, fair and sustainable.
- **S53** [Intergenerational Risk-Sharing and Risk-Taking of a Pension Fund](https://consensus.app/papers/details/d1baf6a5dedf56dd890a131a35b194b2/?utm_source=claude_desktop), C. Gollier, 2008, *J. Public Economics*, DOI 10.1016/j.jpubeco.2007.07.008. Reserves used efficiently allow intergenerational risk sharing and better use of the equity premium.
- **S54** [Financial fairness and conditional indexation](https://consensus.app/papers/details/5c9f6dd7e5695b9dbfbbef36b7e093e1/?utm_source=claude_desktop), T. Kleinow et al., 2015, *Scand. Actuarial J.*, DOI 10.1080/03461238.2016.1225592. Substantiates the dossier's "Dutch conditional indexation (unverified)" label; fairness holds only for entrants at entry.
- **S55** [Intergenerational risk sharing within funded pension schemes](https://consensus.app/papers/details/894769ccaedd5f2bb33b37406cec8cc2/?utm_source=claude_desktop), Jia-Jia Cui et al., 2010, *JPEF*, DOI 10.1017/s1474747210000065. Benefits and contributions linked to the funding ratio can raise welfare.
- **S56** [Intergenerational risk sharing in closing pension funds](https://consensus.app/papers/details/38e49f602d00568f98d6b9c7bb3f2b7d/?utm_source=claude_desktop), T. Boonen et al., 2017, *IME*, DOI 10.1016/j.insmatheco.2017.02.002. Board bargaining favours older generations.
- **S57** [Multistage stochastic dominance: an application to pension fund management](https://consensus.app/papers/details/f6700f47eec35bcea4e4a910b859f56b/?utm_source=claude_desktop), Miloš Kopa et al., 2023, *Annals of OR*, DOI 10.1007/s10479-023-05658-y. Stochastic dominance against a benchmark portfolio, with an "economic cost" for the constraints.
- **S58** [Pension fund management with hedging derivatives, stochastic dominance and nodal contamination](https://consensus.app/papers/details/fe7dc9c3e32e5f6b801e03656280c570/?utm_source=claude_desktop), Vittorio Moriggia et al., 2019, *Omega*, DOI 10.1016/j.omega.2018.08.011. Multistage ALM with put hedges and scenario-tree stress testing.
- **S59** [Optimal Dividends](https://consensus.app/papers/details/d7300dd9fa6f53be9d9d5652a02a0796/?utm_source=claude_desktop), H. Gerber et al., 2004, *NAAJ*, DOI 10.1080/10920277.2004.10596125. The barrier strategy; explains de Finetti's (1957) original discrete model.

**TPA and governance**
- **S60** [Delegating Benchmarks: Aligning Incentives for Better Total Fund Performance](https://consensus.app/papers/details/3e28f2655ed252599968eb7b0832a67e/?utm_source=claude_desktop), Redouane Elkamhi et al., 2025, DOI 10.3905/jpm.2025.1.803. The board anchors the total-fund benchmark and the executive designs mandate benchmarks; argued to reduce gaming.
- **S61** [Dynamic Tracking Error and the Total Portfolio Approach](https://consensus.app/papers/details/bf62d52861885344a623c3458eff2555/?utm_source=claude_desktop), A. Alankar et al., 2026, *arXiv*, DOI 10.48550/arxiv.2603.03213. The board decides tolerable drawdown first; a dynamic TE budget is worth about 2 points a year at the same drawdown (model claim).
- **S62** [Transitioning from SAA to TPA: Governance and Communication Requirements](https://consensus.app/papers/details/a2f3af9d5fbd532fb33b0401337e5b69/?utm_source=claude_desktop), Stefano Cavaglia et al., 2026, *JPM*, DOI 10.3905/jpm.2026.071. A phased transition across five areas.
- **S63** [The Total Portfolio Approach: An Emerging Framework for Institutional Portfolio Construction](https://consensus.app/papers/details/e86826579a4c503eaf62f270b8b88e6e/?utm_source=claude_desktop), Aaron Filbeck, 2026, DOI 10.3905/jpmi.2026.007. Contrasts TPA with SAA on four dimensions and sets out conditions for adoption (interviews include Future Fund, CPP, NZ Super, GIC and Alaska PF).
- **S64** [Total Portfolio Factor, Not Just Asset, Allocation](https://consensus.app/papers/details/7e69547d780a5f9fbf6c57116944679a/?utm_source=claude_desktop), R. Bass et al., 2017, *JPM*, DOI 10.3905/jpm.2017.43.5.038. Measures factor exposures consistently across liquid and illiquid assets.
- **S65** [Portable Beta and Total Portfolio Management](https://consensus.app/papers/details/80a96c5ab72657579d433eeeeddfac9d/?utm_source=claude_desktop), Stefano Cavaglia et al., 2022, *FAJ*, DOI 10.1080/0015198x.2022.2087448. Integrates a factor overlay with the reference portfolio.
- **S66** [Best-practice pension fund governance](https://consensus.app/papers/details/fa35d5f3b5545c3589f0d8afae94fa8c/?utm_source=claude_desktop), G. Clark et al., 2008, *J. Asset Management*, DOI 10.1057/jam.2008.1. Governance makes "a significant incremental difference" to risk-adjusted returns; draws implications for sovereign funds.
- **S67** [How Important Are Investment Committees? Evidence from University Endowments](https://consensus.app/papers/details/d953a45d9eec5c97a5e5a4c592f53c32/?utm_source=claude_desktop), Matteo Binfarè et al., 2017. IC expertise and networks are linked to allocations, access to funds and active returns.
- **S68** [COMMENTARY: Disentangling Investment Policy and Investment Strategy for Better Governance](https://consensus.app/papers/details/67c0ba40021a5e79823d38e696ca44a0/?utm_source=claude_desktop), Richard M. Ennis, 2023, DOI 10.3905/joi.2023.1.279. Trustees should own policy (controlling risk and ensuring liquidity), not strategy.
- **S69** [Total Portfolio Approach](https://consensus.app/papers/details/43ce94a145365b65a733d3abf4b4c1c0/?utm_source=claude_desktop), Redouane Elkamhi et al., 2025, DOI 10.3905/jpm.2025.1.728. TPA "is not a strategy, but a mindset"; adoption depends on adaptive governance and shared definitions of success.

---

## 5. Papers that challenge the dossier's recommendations

**C1. The expected-return spending anchor**
- **Where the dossier stands.** §1.7 lists it as "peer practice to adopt", it is discussed in §2.7, §5 rates it "Adapt", and §6.5 rule 5 tests θ ∈ {0.5, 0.75, 1.0}.
- **The contrary evidence:**
  - [2]: "Spending the expected return will deplete the fund with probability one", and the strategy is "inconsistent with optimal portfolio choice". The model assumes inflows have stopped.
  - [S2]: deterioration "both in probability and in expectation".
  - [3]: withdrawals equal to expected returns lead to eventual depletion. With mean reversion from purchasing-power parity, value is "not even preserved in expectation".
  - [1]: spending below the expected return "is known not to be sufficient to preserve capital".
  - [S3]: annuity-value rules should risk-adjust the normal return. For GPFG this cuts the draw by up to 3% of mainland GDP.
- **Implication *(inference)*.**
  - Drop θ = 1.0 as a candidate and keep it only as a stress case.
  - Anchor $r^*$ to a risk-adjusted sustainable rate, using the analytic thresholds in [2] and [S2].
  - Report P(depletion) next to each rule.
  - The dossier already argues that Norway's rule does not transfer to an illiquid fund without inflows. This literature says it may be unsustainable even for a liquid one.

**C2. Smoothing rules**
- **Where the dossier stands.** §1.3, §3.3(b) and §5 ("use cautiously").
- **The dossier's direction is supported, and strengthened:**
  - Smoothing "is destabilizing and exhausts wealth in finite time" [1].
  - It "hides" risk and defers it "to a later generation" [S1].
  - Short-run smoothing raises long-run spending variability [S3].
  - Excessive smoothing is inefficient [S47].
- **The magnitude is contested:**
  - Smoothing raises depletion risk "only modestly" [3].
  - Reserves and funding-ratio-linked schemes can raise welfare ([S53], [S55]).
  - Bands of 3–7% preserve purchasing power while cutting short-run reductions [S5].
- **The owner-optimality premise is contradicted.** Under soft-norm preferences, optimal spending is "mostly also procyclical", with larger-than-proportional cuts after losses [4].
- **Implication *(inference)*.** Do not present the 15.6% vs 4.8% forced-sale contrast as a general property of smoothing. The verification log already flags it as driven by the floor (R2) and confounded by payout level (R12).

**C3. "Endowment hoarding" as evidence that discretion is asymmetric**
- **Where the dossier stands.** §1.5 and §2.6.
- **The contrary evidence:**
  - [20] finds payouts respond symmetrically to positive and negative shocks across more than 700 universities, directly contradicting Brown et al. (2014).
  - [S11] shows stated rules are revised often.
- **Implication *(inference)*.**
  - Keep pre-commitment, but justify it on Kydland & Prescott time-consistency grounds.
  - Present asymmetry as contested.
  - Model both rule revision and political override.

**C4. "~60% private is consistent with DWY if α ≥ ~3%"**
- **Where the dossier stands.** §1.6 and §2.4. Verification R3 already objects.
- **The contrary evidence:**
  - A ~3% liquidity-risk premium explains PE alpha, and the channel is funding liquidity [16]. So much of DWY's α may be compensation for crisis-state risk.
  - Illiquidity risk lowers allocations to both liquid and illiquid risky assets [12].
  - The studied, breakeven-consistent range for PE is "up to 40%" [S35].
- **Counter-evidence:**
  - Owners may overestimate their liquidity needs [S39].
  - An MPC commitment policy performs close to a fully liquid portfolio [13].
- **Implication *(inference)*.** Re-solve for ADIC's parameters with α split into an illiquidity premium and skill. Do not cite 3% as a threshold.

**C5. Forced-sale chance constraint and the two-bucket model**
- **Where the dossier stands.** §1.4, §3.3 Table 3 and §6.3.
- **The contrary evidence:**
  - "Suspending future commitments can rebalance the portfolio without forced secondary sales" [S38].
  - Commitments are a control variable [13].
  - The right metric is the frequency and severity of external events [14].
- **Implication *(inference)*.** The dossier's pacing rule (6% / 2%) never suspends commitments. Its forced-sale probabilities probably overstate what an optimized pacing policy would incur, which reinforces verification R2.

**C6. Total-fund leverage as a balance-sheet stabiliser (CPP)**
- **Where the dossier stands.** §1.7, §5 "Adopt" and §6.3.
- **Caution:**
  - Leverage aversion changes optimal portfolios materially [S44].
  - After frictions, levered risk parity underperformed [S45].
  - Borrowing to meet a liquidity shock cannot remove all illiquidity costs [S41].
- **Support:**
  - Leverage-averse markets leave a premium for those who can lever [S43].
  - Subsoil oil calls for "additional leverage and hedging" [6].
- **Implication *(inference)*.** Keep LEVER as a decision variable, but price margin, refinancing and funding-liquidity stress explicitly. CPP practice is not evidence of value.

**C7. A single wide-band prior for the endowment-model premium**
- **Where the dossier stands.** §2.6 and §8.
- **The single wide band is supported** by [18], [19], [S16] and [S17], with counterpoints in [S18] and [S19].
- **The evidence varies with conditions:**
  - Scale and LP skill are associated with outperformance ([S32], [S33]).
  - Sovereign LPs, especially strategic SWFs, earn lower returns and liquidate more slowly [S29].
- **Implication *(inference)*.** Condition the prior on scale, skill and sovereign-LP effects rather than using one band.

**C8. The additive-habit objective (CRRA γ = 2, h = 0.8)**
- **Where the dossier stands.** §6.4. Verification R1 shows it is ill-defined.
- **Well-posed alternatives exist:**
  - soft-social-norm utility [4]
  - drawdown-constrained payouts [22]
  - a habit-formation constraint [S46]
  - EW–ES with a cap and floor [S50]

**Recommendations the literature supports rather than challenges:**
- **Wrong-way owner demand:** [6], [S23], [S24].
- **Treating the TPA "+1.3%" claim as non-causal:** consistent with [S61], [S69].
- **Avoiding asset-class quotas:** [S21].
- **Funded-ratio feedback (R12):** [9], [21], [S52], [S54].

---

## 6. Usage message

None. No sign-up, upgrade or usage message appeared in any of the 29 Consensus results.

---

## 7. Method and limitations

- **Searches.**
  - 29 Consensus searches, run one at a time with no filters: 17 citation checks and 12 topical searches.
  - Topical queries started from the six seeds in the brief and were refined toward:
    - SWF spending
    - commodity-SWF allocation
    - SWF direct investing and governance
    - payout responses to shocks
    - PE illiquidity and secondaries
    - illiquid portfolio choice
    - co-investment
    - GCC oil and fiscal linkages
    - leverage aversion
    - multistage ALM
    - intergenerational risk sharing and conditional indexation
    - investment-committee governance
- **Web checks.**
  - One WebSearch confirmed Merton (1993) at NBER.
  - One direct fetch of the TAI hub page confirmed the CAIA/TAI report.
  - A further WebSearch was refused because the shared session budget was exhausted. As a result, SSRN 3614875 (Ennis 2020) and de Finetti's (1957) title remain unchecked on the web.
- **Limits of Consensus records.**
  - Records are abstract-level. Some carry truncated authors, working-paper years or SSRN DOIs for published papers; these are shown as given.
  - Recent items (2025–2026 JPM papers, arXiv preprints) have 0–1 citations and should be treated as early evidence.
  - No finding here comes from a full text.
- **Overlap with other streams.** Several supplementary entries (PE cash flows, ALM solvers) belong mainly to sister streams. They are listed because they bear on this dossier's distribution and liquidity design.
