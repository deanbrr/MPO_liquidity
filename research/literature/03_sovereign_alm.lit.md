# Topic 03 literature review: sovereign ALM, the oil-fiscal linkage and owner distribution demand

**Dossier reviewed:** `research/dossiers/03_sovereign_alm.md` (as of 18 Oct 2026)
**Prepared:** 18 Oct 2026
**Companion:** `research/verification/03_sovereign_alm.verify.md` (fact-check of the same dossier)
**Tools:** Consensus academic search, 33 searches run one at a time with no filters. For metadata Consensus could not resolve, we also ran one WebSearch and one WebFetch of ijcb.org. Two further WebSearch calls were refused because the session's search budget was exhausted.

**Conventions**
- Every paper link is the Consensus URL exactly as returned.
- Authors are listed as Consensus shows them, usually first author plus "et al.".
- Citation counts are Consensus counts on 18 Oct 2026.
- "[inference]" marks our reasoning. Everything else restates a search result or abstract.
- **User context (18 Oct 2026).**
  - Treasury belongs to Corporate Finance, a non-investment function.
  - The Secondaries group is a hybrid of direct and fund investments.
  - The design notes below therefore route liquidity and liability outputs to the Corporate Finance / Treasury seat.

---

## 1. Summary

### Citation integrity
We checked the 25 most load-bearing academic works. The dossier cites 32 academic works (34 if two official/expert reports are counted), plus non-academic sources.

| Outcome | Count | Detail |
|---|---|---|
| Found, metadata matches | 23 | |
| Mismatched | 1 | Moutanabbir & Noureldin is cited as ERF WP 1172 (2018). It was later published in *International Review of Economics & Finance* (2020), DOI 10.1016/j.iref.2020.06.014. Cite the journal version, and re-check the 0.01–0.07pp hedging-demand figure against it, because that figure was verified against the WP. |
| Not found in Consensus | 1 | Merton (1993), the endowment chapter. A web search confirms it exists with the dossier's metadata: NBER chapter c6102, chapter 7 of Clotfelter & Rothschild (eds), U. Chicago Press, 1993. |

**Minor issues**
- Some works are indexed only as working papers: Bodie & Brière (SSRN), Balding & Yao (SSRN) and Meucci (arXiv).
- Two titles omit their subtitles: Baumeister & Hamilton 2019 and Känzig 2021.
- Consensus shows the SSRN DOI for Ready (2018).
- Consensus dates Breuer et al. to 2012. ijcb.org confirms IJCB Vol 5 No 3, Sept 2009, so the dossier is right.
- The Consensus record for Rockafellar & Uryasev carries the abstract of a different paper. This is a database artefact; the metadata match.

**Bonus finding:** Dybvig (1999, *FAJ*), tagged [U] in the dossier, is indexed and can be upgraded. No hallucinated citation was found, which is consistent with the verification log.

### Backfill
We ran 14 topical searches. The dossier's theoretical core, hedging demand with non-tradable oil wealth (Gintschel–Scherer, Scherer, van den Bremer et al., Bodie–Brière), is well chosen. It misses four bodies of work that bear directly on its design:

1. **How owners actually draw, and how stabilization-fund rules perform.**
   - Draws depend on the owner's fiscal space and fund size (AlKathiri et al. 2020; Shah et al. 2026).
   - Fiscal reaction functions switch between pro- and countercyclical regimes and have an upward spending bias (Bjørnland et al. 2026).
   - A fixed withdrawal rate out of assets is the robust rule design (Landon & Smith 2015).
   - The IMF already has a SALM template for an SWF drawn to cover a commodity-price financing gap (Al-Hassan et al. 2018).
2. **Spending sustainability.**
   - Spending a fund's expected return depletes it eventually (Mork et al. 2022; Aase 2024).
   - ADIC's 5–10% band against a 10% nominal target therefore needs a long-horizon depletion test, not just a liquidity test.
3. **Portfolio choice with illiquid assets, and liquidity stress testing.** These are the right models for a fund that is about 60% private and faces stochastic draws:
   - Dimmock, Wang & Yang (endowment model with lockups);
   - Ang, Papanikolaou & Westerfield 2014 (illiquidity crises);
   - Cont et al. 2020 (scenario-consistent "Liquidity at Risk").
4. **Real-time shock identification and identification risk.**
   - A peer-reviewed daily, real-time SVAR is available for the shock-type nowcaster (Gazzani et al. 2024, *JME*).
   - The supply-vs-demand attribution the dossier relies on depends on the identification scheme (Braun 2023, *QE*; Kilian 2024, *JEDC*).
   - Highly cited DCC evidence supports the dossier's sign pattern for state-conditional oil–equity correlation (Filis et al. 2011).

### Challenges to the dossier (detail in §5)
- **Endowment hoarding.** Rosen et al. (2019) contradict the "hoarding" result behind the dossier's "anti-endowment" contrast.
- **Shock identification.** Braun (2023), Kilian (2024) and Degasperi (2026) weaken the evidence (BH 2019, Känzig 2021) used to label shock types.
- **Geopolitical risk.** Cuñado et al. (2020) warn against equating geopolitical risk with "oil up".
- **Draw rules.** Normative spending-rule work (Landon & Smith 2015; Mendes & Pennings 2017; Wills 2018; Mork et al. 2023) questions treating countercyclical owner draws as a fixed given rather than a negotiable rule.
- **Hybrids.** We found no paper that supports or refutes "buy joint-state hybrids now".

**Usage message:** none appeared in any Consensus result.

---

## 2. Citation-integrity table (25 checked)

| # | Dossier citation | Status | Corrected metadata / note | Consensus URL |
|---|---|---|---|---|
| 1 | Gintschel & Scherer (2008), *J. Asset Management* 9, 215–238 | found | 2008, *Journal of Asset Management*, 40 cit., DOI 10.1057/jam.2008.19. The SSRN version, "Total Wealth Management for Oil Revenue Funds" (DOI 10.2139/ssrn.493345), is also indexed. | https://consensus.app/papers/details/0644f03ab6be5e608a59b751de988332/?utm_source=claude_desktop |
| 2 | Scherer (2009), *Fin. Markets & Portfolio Mgmt* 23, 315–327 | found | 2009, *FMPM*, 31 cit., DOI 10.1007/s11408-009-0105-2 | https://consensus.app/papers/details/5c3da8c349df5a82b6b777011c9a5e90/?utm_source=claude_desktop |
| 3 | Scherer (2011), *J. Alternative Investments* 13, 24–34 | found | Consensus lists the year as 2010. The DOI 10.3905/jai.2011.13.3.024 encodes 2011, vol 13 no 3, p.24. Add issue no. 3. 25 cit. | https://consensus.app/papers/details/7468f90568ef5c9e8e356a66a4d12455/?utm_source=claude_desktop |
| 4 | van den Bremer, van der Ploeg & Wills (2016), *EER* 82, 113–131 | found | 2016, *European Economic Review*, 42 cit., DOI 10.1016/j.euroecorev.2015.10.005 | https://consensus.app/papers/details/46e0449b577f53ae921bf6ba17efb732/?utm_source=claude_desktop |
| 5 | Bodie & Brière (2014), *JOIM* 12(1) | found (WP record) | Consensus indexes only the SSRN version: same title, 2013, 21 cit., DOI 10.2139/ssrn.1460692. The JOIM record is not in Consensus; the verification log confirmed the JOIM listing. | https://consensus.app/papers/details/848357ab551a580793407efeed637bbb/?utm_source=claude_desktop |
| 6 | Moutanabbir & Noureldin (2018), ERF WP 1172 | **mismatched (superseded)** | Published as Moutanabbir, K. et al. (2020), "Optimal asset allocation and consumption rules for commodity-based sovereign wealth funds", *International Review of Economics & Finance*, DOI 10.1016/j.iref.2020.06.014 (0 cit.). Cite the journal version. | https://consensus.app/papers/details/5182918fd69a5116b305d7f557bb70c3/?utm_source=claude_desktop |
| 7 | Balding & Yao (2011), *International Finance Review* 12, 293–312 | found (WP record) | SSRN 2011, "Portfolio Allocation for Sovereign Wealth Funds in the Shadow of Commodity Based National Wealth", 17 cit., DOI 10.2139/ssrn.1805297. The IFR volume is not shown. | https://consensus.app/papers/details/d49cd186f5e55cb8a4d5f80a79806df8/?utm_source=claude_desktop |
| 8 | Lessmann, Tahri & Yanovski (2024), *Strategic Behavior and the Environment* 10(1–2) | found | 2024, *SBE*, 1 cit., DOI 10.1561/102.00000109. Shown as "Kai Lessmann et al." | https://consensus.app/papers/details/dcfc9f665e2554238467cd232b3ac8ca/?utm_source=claude_desktop |
| 9 | Das, Lu, Mulder & Sy (2009), IMF WP/09/179 | found | SSRN record, 2009, 76 cit., DOI 10.2139/ssrn.1489652. Shown as "U. Das et al." | https://consensus.app/papers/details/d3120c2951e1506994afaa449d289074/?utm_source=claude_desktop |
| 10 | Merton (1993), "Optimal investment strategies for university endowment funds", in Clotfelter & Rothschild (eds) | **not found in Consensus; exists (web-verified)** | WebSearch confirms NBER chapter c6102: chapter 7 of *Studies of Supply and Demand in Higher Education*, U. Chicago Press, 1993. The NBER PDF lists pp. 211–242; another listing gives 211–236. It is preceded by NBER WP 3820 (Aug 1991). The dossier's metadata are consistent. | none (web: https://www.nber.org/chapters/c6102) |
| 11 | Brown, Dimmock, Kang & Weisbenner (2014), *AER* 104(3), 931–62 | found | 2014, *AER*, 119 cit., DOI 10.1257/aer.104.3.931 | https://consensus.app/papers/details/7831f601f303581cb3e87906847e0fab/?utm_source=claude_desktop |
| 12 | Kilian (2009), *AER* 99(3), 1053–69 | found | 4,453 cit., DOI 10.1257/aer.99.3.1053 | https://consensus.app/papers/details/fa321872270c5dbdbba0af7f1726d8f7/?utm_source=claude_desktop |
| 13 | Baumeister & Hamilton (2019), *AER* 109(5), 1873–1910 | found | 839 cit., DOI 10.1257/aer.20151569. The full title adds the subtitle "…: Revisiting the Role of Oil Supply and Demand Shocks". | https://consensus.app/papers/details/0d4e6d0d27bb5443b208a085a542bb4c/?utm_source=claude_desktop |
| 14 | Känzig (2021), *AER* 111(4), 1092–1125 | found | 365 cit., DOI 10.1257/aer.20190964. The full title adds "…: Evidence from OPEC Announcements". | https://consensus.app/papers/details/ce581674164250868313bd57db561d99/?utm_source=claude_desktop |
| 15 | Ready (2018), *Review of Finance* 22(1), 155– | found | 396 cit. Consensus shows the SSRN DOI 10.2139/ssrn.2140034. The dossier's RoF DOI is not shown but is not contradicted; pages are 155–176 per the verification log. | https://consensus.app/papers/details/106a12e9d4db5748b7dd05cdd01bea8d/?utm_source=claude_desktop |
| 16 | Robinson & Sensoy (2016), *JFE* 122(3) | found | 203 cit., DOI 10.1016/j.jfineco.2016.09.008 | https://consensus.app/papers/details/86bf821b6ba65861a9da20fed7862965/?utm_source=claude_desktop |
| 17 | Borensztein, Jeanne & Sandri (2009), IMF WP/09/229 | found | 77 cit., DOI 10.5089/9781451873764.001. The *J. Development Economics* 2013 version, tagged [U] in the dossier, was not returned by Consensus. A web check was refused (budget exhausted), so keep it [U]. | https://consensus.app/papers/details/af6552e41d9255a98dd96d7056cbc0a4/?utm_source=claude_desktop |
| 18 | Erbil (2011), IMF WP/11/171 | found | 72 cit., DOI 10.5089/9781462314324.001.a001 | https://consensus.app/papers/details/2c4db88c53155ad78b31c684319b0168/?utm_source=claude_desktop |
| 19 | Kilian & Park (2009), *IER* 50(4) | found | 1,686 cit., DOI 10.1111/j.1468-2354.2009.00568.x | https://consensus.app/papers/details/9cdcaa9198f651f7a8c49b4aa106fa7c/?utm_source=claude_desktop |
| 20 | Schwartz & Smith (2000), *Mgmt Sci* 46(7) | found | 1,188 cit., DOI 10.1287/mnsc.46.7.893.12034 | https://consensus.app/papers/details/bb40f38ca8a45003bd2f2583eb95cb71/?utm_source=claude_desktop |
| 21 | Hamilton (1989), *Econometrica* 57(2) | found | 10,153 cit., DOI 10.2307/1912559 | https://consensus.app/papers/details/0ee00e5cdc5455caa6923a5ff7a6d577/?utm_source=claude_desktop |
| 22 | Rockafellar & Uryasev (2000), *J. Risk* 2(3) | found | 7,235 cit., DOI 10.21314/jor.2000.038. The abstract shown on the Consensus record describes a different paper, a bank risk-return management application; this is a database artefact. Title, year, venue and DOI match. | https://consensus.app/papers/details/a500ccf654ae5205a70fe138eb0d82d7/?utm_source=claude_desktop |
| 23 | Meucci (2008), *Risk* 21(10) | found (preprint record) | Indexed as the arXiv version, DOI 10.48550/arxiv.1012.2848, 92 cit. The *Risk* venue is not shown. | https://consensus.app/papers/details/9ed7d3116f4656ada56ea14eb7491b12/?utm_source=claude_desktop |
| 24 | Breuer, Jandačka, Rheinberger & Summer (2009), *IJCB* 5(3) | found | The Consensus record is dated 2012, has no venue and 130 cit. The ijcb.org issue page lists the article in Vol 5 No 3, Sept 2009, so the dossier is correct. | https://consensus.app/papers/details/ac197fd82c6b5c1cad30bc15cac96241/?utm_source=claude_desktop |
| 25 | Stulz (1982), *JFE* 10(2) | found | 572 cit., DOI 10.1016/0304-405x(82)90011-3. The full title adds "…: Analysis and applications". | https://consensus.app/papers/details/b842156844715df58bf91c0043c7deb3/?utm_source=claude_desktop |

### Additional checks beyond the 25 (surfaced by other searches)

| Dossier citation | Status | Note | Consensus URL |
|---|---|---|---|
| Dybvig (1999), *FAJ* 55(1) [U] | found | "Using Asset Allocation to Protect Spending", *FAJ*, 1999, 53 cit., DOI 10.2469/faj.v55.n1.2241. The author field is blank in Consensus. Upgrade from [U]. | https://consensus.app/papers/details/ac6b4afe4adf5de68e6dee26fa078f05/?utm_source=claude_desktop |
| Gray, Merton & Bodie (2007), *JOIM* 5(4) [U] | partially verified | Consensus returned the companion NBER WP (2006), "A New Framework for Analyzing and Managing Macrofinancial Risks of an Economy" (listed as Z. Bodie et al.), 91 cit., DOI 10.2139/ssrn.936661. The JOIM 2007 record was not returned. | https://consensus.app/papers/details/a5531165a79b5b55af8326f76e858be7/?utm_source=claude_desktop |
| Pereira & Pinto (1991), *Math. Programming* 52 [U] | not found directly | The original was not returned. Rebennack (2015, *Mathematical Programming*) attributes SDDP to Pereira and Pinto in 1991. | https://consensus.app/papers/details/44ed80de0ea85bf8a87f94c21134b6f8/?utm_source=claude_desktop |

**Not checked:**
- Non-academic sources: the IMF 2014 SALM policy paper, Mirzoev et al. (2020, IMF departmental paper), the Valencia (2018) IMF blog, the Bernanke (2016) Brookings blog, EIA, IMF data and press.
- The remaining [U] items: Tobin (1974), Dybvig (1995), O'Hagan et al. (2006), Cooke (1991), Ang–Goetzmann–Schaefer (2009) and BCBS (2013).
- The Valencia blog has an academic companion paper, listed below (E22). Cite that instead.

---

## 3. Annotated bibliography (24 papers)

Tags: **[cited]** = the dossier cites it; **[missed]** = not in the dossier; **[challenge]** = contradicts or qualifies a dossier claim.

### A. Sovereign ALM and portfolio choice with oil wealth

**A1. [Optimal asset allocation for sovereign wealth funds](https://consensus.app/papers/details/0644f03ab6be5e608a59b751de988332/?utm_source=claude_desktop)** [cited]
- Andreas Gintschel et al., 2008, *Journal of Asset Management*, 40 cit., DOI 10.1057/jam.2008.19.
- **Finding:** allocating financial assets to hedge oil-reserve risk can cut risk by up to 50%, or 10% without short sales, when reserves and fund are equal in value. That is worth a certainty-equivalent 3.26% a year (48bp long-only). The hedge decision matters more than where the fund sits on the efficient frontier.
- **Relevance:** anchors the owner-correlation tilt. The long-only 48bp is a realistic ceiling. [inference] ADIC is one pocket of several, so its attainable gain is smaller.

**A2. [The Elephant in The Ground: Managing Oil and Sovereign Wealth](https://consensus.app/papers/details/46e0449b577f53ae921bf6ba17efb732/?utm_source=claude_desktop)** [cited]
- T. S. van den Bremer et al., 2016, *European Economic Review*, 42 cit., DOI 10.1016/j.euroecorev.2015.10.005.
- **Finding:** subsoil oil should change the fund's portfolio through extra leverage and hedging. First-best spending is a share of total wealth, and unhedgeable volatility calls for precautionary savings.
- **Relevance:** the basis for linking the owner's draw to total, including below-ground, wealth, and for sizing ADIC's precautionary liquidity by the owner's unhedgeable risk.

**A3. [Sovereign Wealth and Risk Management: A Framework for Optimal Asset Allocation of Sovereign Wealth](https://consensus.app/papers/details/848357ab551a580793407efeed637bbb/?utm_source=claude_desktop)** [cited]
- Z. Bodie et al., 2013 (SSRN record; the dossier cites JOIM 2014), 21 cit., DOI 10.2139/ssrn.1460692.
- **Finding:** contingent-claims sovereign ALM gives optimal sovereign wealth as a performance-seeking portfolio plus three hedging demands: fiscal-surplus variability, external debt and domestic debt. Chile's sovereign investment is under-diversified.
- **Relevance:** the fiscal-surplus hedge term is the formal basis for the dossier's "owner beta" and owner-state weighting.

**A4. [Optimal asset allocation for commodity sovereign wealth funds](https://consensus.app/papers/details/2a0ef305e415569e9411d0fbceaa310d/?utm_source=claude_desktop)** [missed]
- Alfonso A. Irarrazabal et al., *Quantitative Finance*, 4 cit., DOI 10.1080/14697688.2022.2158918. Consensus lists 2020; the DOI suffix suggests a 2022 article [inference].
- **Finding:** in incomplete markets, with a non-tradable commodity revenue stream that ends on a known date, optimal consumption and investment are state- and time-dependent. For Norway, equity should fall from 60% to 40% over 60 years. The solution is "particularly sensitive to the correlation between oil and stock price changes". The paper also estimates welfare losses from suboptimal rules.
- **Relevance:** the owner-hedge term is fragile to ρ(oil, equity), which is exactly the parameter the dossier shows flipping by era and shock type.

**A5. [Portfolio Choice for a Resource-Based Sovereign Wealth Fund: An Analysis of Cash Flows](https://consensus.app/papers/details/696efef8b6b95d62b64a769f38b2f290/?utm_source=claude_desktop)** [missed]
- K. A. Mork et al., 2020, *International Journal of Financial Studies*, 2 cit., DOI 10.3390/ijfs8010014.
- **Finding:** using industry cash flows rather than prices, only oil & gas industry cash flows correlate closely, significantly and persistently with Norway's petroleum cash flow. Other industries' correlations are small and mostly insignificant, which supports underweighting oil & gas shares.
- **Relevance:** a way to estimate owner beta that avoids the discount-rate noise in price correlations. It also confines the natural hedge to energy-linked exposures.

**A6. [Commodity-based Sovereign Wealth Funds; Managing Financial Flows in the Context of the Sovereign Balance Sheet](https://consensus.app/papers/details/c7141a01c2915f2c9d142ef65e3eee81/?utm_source=claude_desktop)** [missed]
- Abdullah Al-Hassan et al., 2018, *IMF Working Papers*, 6 cit., DOI 10.5089/9781484340967.001.
- **Finding:** a management framework for commodity SWFs (stabilization and savings funds) built on macrofiscal linkages and an integrated SALM approach. It is applied to an accumulation scenario and to a scenario in which the SWF is drawn to cover a financing gap after commodity prices fall.
- **Relevance:** the closest official analogue to the dossier's Owner Draw Engine. Use it to structure the financing-gap waterfall in IMF-consistent terms.

### B. Owner draw behaviour, fiscal reaction and spending rules

**B7. [Optimal policies for managing oil revenue stabilization funds: An illustration using Saudi Arabia](https://consensus.app/papers/details/4ab7b0395f8c5e7a97e025705b41a642/?utm_source=claude_desktop)** [missed]
- Nader AlKathiri et al., 2020, *Resources Policy*, 4 cit., DOI 10.1016/j.resourpol.2020.101686.
- **Finding:** the larger the fund, the smaller the additions in high-revenue periods and the bigger the withdrawals in low-revenue periods. The fund can be split into tranches of different asset duration, and the line between a stabilization fund and an SWF "is not a bright line".
- **Relevance:** supports making ADIC's draw share ω state-dependent, with ADIC treated as one duration tranche within the owner's buffer stack.

**B8. [“Institutions and macroeconomic stability under oil price shocks: Evidence from the GCC”](https://consensus.app/papers/details/b100f501a743599d92c00223557b79d8/?utm_source=claude_desktop)** [missed]
- Showkat Ahmad Shah et al., 2026, *North American Journal of Economics and Finance*, 0 cit., DOI 10.1016/j.najef.2026.102702.
- **Finding:** in GCC data for 1980–2023 (PVAR, GMM and regime-dependent local projections), economies with high fiscal space accumulate sovereign buffers countercyclically, while constrained economies draw them down. The asymmetries are most pronounced in oil busts.
- **Relevance:** draw intensity depends on the owner's fiscal space, so the slope b and the share ω should be functions of owner buffers B^own.

**B9. [Fiscal Policy Regimes in Resource‐Rich Economies](https://consensus.app/papers/details/602cd3cbe11d584a8d9f6982d14bae23/?utm_source=claude_desktop)** [missed]
- H. Bjørnland et al., 2026, *Journal of Applied Econometrics*, 1 cit., DOI 10.1002/jae.70074.
- **Finding:** in a Bayesian regime-switching panel of 16 oil producers, fiscal policy alternates repeatedly between procyclical and countercyclical regimes. The procyclical regime is more volatile and more likely for OPEC members. Expenditure growth mostly rises after both increases and decreases in oil revenue, an upward bias.
- **Relevance:** replace the dossier's constant ψ₁≈0.3 with a regime-switching spending reaction plus upward drift. [inference] The UAE's OPEC exit may shift the regime probabilities; elicit them.

**B10. [Capital Preservation and Current Spending with Sovereign Wealth Funds and Endowment Funds: A simulation Study](https://consensus.app/papers/details/c93456144b3e598bbe6aa9eb8ae9d5d8/?utm_source=claude_desktop)** [missed]
- K. A. Mork et al., 2022, *International Journal of Financial Studies*, 4 cit., DOI 10.3390/ijfs10030067.
- **Finding (GPFG simulation):**
  - withdrawals equal to expected returns still deplete the fund eventually;
  - because of PPP mean reversion, value is not preserved even in expectation;
  - using the fund for fiscal policy creates substantial finite-time depletion risk;
  - smoothing raises depletion risk modestly after large losses;
  - only lower withdrawal rates combined with bounds on fiscal use remove depletion risk.
- **Relevance:** test ADIC's 5–10% band and 10% target for long-run real depletion, not only short-run liquidity. Fiscal use is precisely ADIC's channel.

**B11. [Optimal Spending Strategies for Sovereign Wealth Funds Using a Discrete-Time Life Cycle Model](https://consensus.app/papers/details/b92a25866b5350709012a3b8f6d1047b/?utm_source=claude_desktop)** [missed]
- K. Aase, 2024, *Journal of Risk and Financial Management*, 1 cit., DOI 10.3390/jrfm17080327.
- **Finding:** under expected or recursive utility, the optimal spending rate is significantly below the fund's expected real return. Spending the expected return erodes value both in probability and in expectation. The paper gives closed-form sustainability thresholds. A companion SSRN paper (Aase et al. 2021, DOI 10.2139/ssrn.3779850) finds depletion with probability one.
- **Relevance:** an owner-facing sustainable-draw benchmark to set against the 5–10% band.

**B12. [Rule-Based Resource Revenue Stabilization Funds: A Welfare Comparison](https://consensus.app/papers/details/1f9da91d0180515195ee945ad33ee532/?utm_source=claude_desktop)** [missed]
- Stuart Landon et al., 2015, *The Energy Journal*, 17 cit., DOI 10.5547/01956574.36.2.6.
- **Finding:** in Monte Carlo simulations, stabilization funds offer large potential welfare gains. Some designs reduce welfare, especially those that accumulate large asset or debt stocks. A robust performer combines a fixed deposit rate out of resource revenue with a fixed withdrawal rate out of assets.
- **Relevance:** evidence for a fixed-%-of-assets draw rule as an owner-negotiable alternative. [inference] A fiscal-gap-linked draw maximizes liability wrong-way risk.

**B13. [The Impact of Endowment Shocks on Payouts](https://consensus.app/papers/details/30db9b06ea85503da3e4097350b48651/?utm_source=claude_desktop)** [missed] [challenge]
- H. Rosen et al., 2019, *The Journal of Higher Education*, 7 cit., DOI 10.1080/00221546.2019.1621115.
- **Finding:** in panel data on more than 700 universities over 1987–2009, payouts respond symmetrically to positive and negative shocks.
- **Relevance:** contradicts the Brown et al. (2014) "hoarding" result that the dossier's "anti-endowment" contrast relies on.

### C. Oil-shock identification and oil–equity co-movement

**C14. [Oil Prices and the Stock Market](https://consensus.app/papers/details/106a12e9d4db5748b7dd05cdd01bea8d/?utm_source=claude_desktop)** [cited]
- Robert Ready, 2018, *Review of Finance*, 396 cit., DOI shown 10.2139/ssrn.2140034.
- **Finding:** demand shocks are oil-producer returns orthogonal to unexpected VIX changes; supply shocks are the remaining variation in oil prices. Demand shocks correlate strongly positively with market returns and output, supply shocks strongly negatively.
- **Relevance:** the basis of the A2 nowcaster.

**C15. [Dynamic correlation between stock market and oil prices: The case of oil-importing and oil-exporting countries](https://consensus.app/papers/details/b1cab2cbc36c5d1286468283e042e840/?utm_source=claude_desktop)** [missed]
- G. Filis et al., 2011, *International Review of Financial Analysis*, 796 cit., DOI 10.1016/j.irfa.2011.02.014.
- **Finding:** oil–stock correlation rises with aggregate-demand shocks and falls (negative) with precautionary-demand shocks such as wars. Supply-side shocks do not affect it, and oil is not a safe haven in turmoil.
- **Relevance:** highly cited, independent support for the dossier's state-conditional ρ_Z signs: positive in demand bust (DB), negative in Gulf war (GW). Use as priors.

**C16. [Oil price shocks in real-time](https://consensus.app/papers/details/e55f2eaa3fc85060bbb553ab37f251e8/?utm_source=claude_desktop)** [missed]
- A. Gazzani et al., 2024, *Journal of Monetary Economics*, 29 cit., DOI 10.1016/j.jmoneco.2023.12.005.
- **Finding:** a daily SVAR that identifies global oil shocks in real time, avoiding the publication lags of monthly SVARs. It proved valuable during COVID-19 and Russia's invasion of Ukraine.
- **Relevance:** a peer-reviewed real-time structural method for the P(Z_t) nowcast, complementing Ready (2018) and the monthly BH-SVAR.

**C17. [The importance of supply and demand for oil prices: Evidence from non‐Gaussianity](https://consensus.app/papers/details/f89e239dfa155480a6179728c5151ed6/?utm_source=claude_desktop)** [missed] [challenge]
- Robin Braun, 2023, *Quantitative Economics*, 12 cit., DOI 10.3982/qe2091.
- **Finding:** with identification by non-Gaussianity, the short-run supply elasticity shifts toward zero and supply shocks become minor drivers, at a median of about 6% of forecast-error variance at 16 months.
- **Relevance:** contradicts the BH (2019) reading the dossier cites. Historical shock-type labels depend on the identification scheme.

**C18. [Time-Varying Impact of Geopolitical Risks on Oil Prices](https://consensus.app/papers/details/3b90f020bb1954dea3c6f0d71637be1a/?utm_source=claude_desktop)** [missed] [challenge]
- J. Cuñado et al., 2020, *Defence and Peace Economics*, 242 cit., DOI 10.1080/10242694.2018.1563854.
- **Finding:** in a TVP-SVAR over 1974–2017, newspaper-based geopolitical risk generally has a significant negative effect on oil returns, mainly through lower demand. The authors warn against treating all geopolitical risk as Middle East supply shocks.
- **Relevance:** the GW state should not be triggered by geopolitical-risk indices alone. The evidence is mixed: Smales 2019 finds geopolitical risk associated with oil up and stocks down.

### D. Illiquid portfolios and liquidity stress testing

**D19. [The Endowment Model and Modern Portfolio Theory](https://consensus.app/papers/details/20e68a8fe18758fcaf6be78ee7bec8e7/?utm_source=claude_desktop)** [missed]
- Stephen G. Dimmock et al., 2019 (NBER record; venue shown as *Management Science*, and the abstract cites doi.org/10.1287/mnsc.2023.4759), 25 cit., DOI 10.3386/w25559.
- **Finding:** a dynamic model with illiquid alternatives (lockups plus a proportional cost for early liquidation).
  - Staggered lockups ("liquidity diversification") raise both allocations and welfare.
  - Lockups and secondary-market costs create endogenous, time-varying rebalancing boundaries.
  - In crisis states, holdings deviate far from targets.
- **Relevance:** a formal model for ADIC's private book under draws. It supplies state-dependent no-trade bands and a crisis liquidation cost for SELL/HOLD.

**D20. [Portfolio Choice with Illiquid Assets](https://consensus.app/papers/details/c7070e2585ba58468abbef5ce4b0a46c/?utm_source=claude_desktop)** [missed]
- Andrew Ang et al., 2014, *Management Science*, 171 cit., DOI 10.1287/mnsc.2014.1986.
- **Finding:** illiquidity, meaning assets cannot be traded for uncertain intervals, raises effective risk aversion and makes it state-dependent. Uncertain duration is the main cost driver. Investors would forgo about 2% of wealth to hedge illiquidity crises that occur once a decade.
- **Relevance:** an anchor for valuing committed contingent liquidity, and for modelling "exits shut" duration in DB as stochastic.

**D21. [Liquidity at risk: Joint stress testing of solvency and liquidity](https://consensus.app/papers/details/73c5a80bdb8c5f408aabc6305a0cdf9d/?utm_source=claude_desktop)** [missed]
- R. Cont et al., 2020, *Journal of Banking & Finance*, 48 cit., DOI 10.1016/j.jbankfin.2020.105871.
- **Finding:** a structural framework that derives endogenous liquidity shocks from solvency shocks and defines "Liquidity at Risk", the liquidity needed in a stress scenario. Funding costs can amplify losses.
- **Relevance:** a template for a scenario-consistent stressed Distribution Coverage Ratio (DCR), which fixes the mixed-measure DCR the verifier flagged.

### E. Hedging the owner's oil exposure

**E22. [Welfare Gains from Market Insurance: The Case of Mexican Oil Price Risk](https://consensus.app/papers/details/ffcf766db893543ca135d3e4e11f14af/?utm_source=claude_desktop)** [missed]
- Fabián Valencia et al., 2018, IMF Working Paper (SSRN record), 11 cit., DOI 10.5089/9781484344163.001.
- **Finding:** in a sovereign-default model calibrated to Mexico, oil put hedging raises welfare by about 0.44% of permanent consumption. About 90% of the gain comes from lower sovereign spreads.
- **Relevance:** the academic source behind the IMF blog the dossier cites. Most of the value comes through the balance sheet. [inference] For ADIC, the analogue is buffer release, not expected P&L.

### F. Energy transition

**F23. [The economic and fiscal transition costs of global climate mitigation in fossil fuel export dependent economies](https://consensus.app/papers/details/e2a2dffd272759a2b2118eb6cd03a9db/?utm_source=claude_desktop)** [missed]
- Lars Jensen, 2024, *Resources Policy*, 10 cit., DOI 10.1016/j.resourpol.2024.105234.
- **Finding:**
  - 40 fossil-dependent economies lose more than 60% of oil rents (PV US$12–14trn, 2023–40) under net-zero 2050 compared with business as usual.
  - For emerging and developing exporters, a 10pp fall in real oil-price inflation is associated with GDP 1.58% lower after four periods, revenue 0.6–0.8pp of GDP lower, and debt rising about 0.5pp a year.
  - Few, mainly high-income, countries have the savings to cushion this.
- **Relevance:** calibration ranges for the energy-transition (ET) overlay, both the h_t decline and the revenue sensitivity. [inference] The UAE sits in the cushioned group, so energy-transition risk shows up as more persistent draws.

### G. Methods

**G24. [Modeling time-dependent randomness in stochastic dual dynamic programming](https://consensus.app/papers/details/889e982ca4c8514ea4b791ce145b8493/?utm_source=claude_desktop)** [missed]
- N. Löhndorf et al., 2019, *European Journal of Operational Research*, 90 cit., DOI 10.1016/j.ejor.2018.08.001.
- **Finding:** on the Brazilian hydro system, Markov-chain SDDP closes its bounds faster than autoregressive SDDP, and its policy dominates. An AV@R formulation makes policies robust to a misspecified stochastic model.
- **Relevance:** supports the dossier's Markov Z_t × S_t lattice and nested AV@R for robustness and time consistency.

---

## 4. Missed-but-important papers and their design implications

| Paper (see §3 for link) | Framework element | Concrete design implication |
|---|---|---|
| Al-Hassan et al. 2018 (A6) | **Model**: owner fiscal module | Build the Owner Draw Engine as an IMF-style SALM financing-gap waterfall: stabilization balances, then debt, then savings funds. Report ADIC's draw as its tranche of the residual gap, using IMF scenario conventions so the owner's counterparts recognise the numbers. |
| AlKathiri et al. 2020 (B7) | **Parameter** ω_t; **state** B^own | Make ω_t = f(owner buffer level, short-duration tranche depletion). ADIC, as a long-duration tranche, is drawn after short buffers are used. Replaces the constant ω. |
| Shah et al. 2026 (B8) | **Parameters** b, ω; **state** B^own | Use a steeper draw slope when owner fiscal space is low, asymmetric in busts. Piecewise b(B^own). [inference] Add a scenario in which owner buffers are depleted by 2026 war spending. |
| Bjørnland et al. 2026 (B9) | **Model**: spending reaction | Use a two-regime Markov-switching ψ (pro- vs countercyclical) with upward expenditure drift. Elicit regime probabilities, which may shift after the OPEC exit [inference]. |
| Mork et al. 2022 (B10); Aase 2024 (B11) | **Objective / IC metric** | Add P(real NAV depletion over 20–30y) and a sustainable-draw threshold to the IC dashboard. Run the 10% target against a 5–10% draw path. |
| Landon & Smith 2015 (B12) | **Policy lever / IC** | Model alternative draw rules (fixed % of NAV, trailing average, fiscal-gap-linked) as owner-negotiable levers. Compare liability wrong-way risk, liquidity buffer required and expected value across rules. |
| Irarrazabal et al. (A4) | **Robust objective** | Optimize owner-hedge tilts over an ambiguity set for ρ(oil, equity) by shock type Z. Report the wealth-equivalent loss of simple rules relative to the optimum. |
| Mork et al. 2020 (A5) | **Owner-beta estimation** | Estimate β^own from cash-flow (earnings or dividend) covariance with owner hydrocarbon revenue, not price correlation alone. Concentrate natural-hedge underweights in energy-linked exposures. |
| Filis et al. 2011 (C15) | **Priors** for ρ_Z | Priors: aggregate-demand states positive, precautionary or war states negative, supply states about zero. This matches the dossier's §6.4 ρ_Z table; use it as Bayesian priors and calibration evidence. |
| Gazzani et al. 2024 (C16) | **Agent A2** (shock-type nowcaster) | Add a daily real-time SVAR to the nowcast ensemble alongside Ready-type decomposition, HMM and LLM event flags. Raise a disagreement alarm when they diverge. |
| Braun 2023 (C17), with Caldara et al. 2016/19, Kilian 2024 and Degasperi (listed below) | **Model risk / calibration** | Label history under several identification schemes (sign plus elasticity priors, non-Gaussian, proxy). Estimate the Z transition matrix with label uncertainty, for example a Dirichlet posterior over labelled counts, and show the IC the spread. |
| Cuñado et al. 2020 (C18); Smales 2019 | **GW trigger rule** | Require observed export-volume loss or infrastructure damage, not only geopolitical-risk spikes, to enter GW. A1/A2 rubric: "threat vs realised disruption". |
| Dimmock et al. (D19) | **SELL/HOLD model; pacing constraint** | Use state-dependent proportional liquidation costs δ_Z, which create endogenous no-trade bands. Stagger vintages and maturities ("liquidity diversification"). |
| Ang et al. 2014 (D20) | **Liquidity shadow price; hedge budget** | Model exits-shut duration in DB as stochastic. Use willingness-to-pay for liquidity insurance to sanity-check contingent-liquidity spend [inference]. |
| Cont et al. 2020 (D21) | **Tier-1 constraint (DCR)** | Replace the mixed-measure DCR (mean inflows against P99 margin) with a scenario-consistent Liquidity at Risk: one stress path drives NAV, haircuts, draws, calls, distributions and margin. Owner: **Corporate Finance / Treasury** (user-confirmed treasury owner). |
| Valencia et al. 2018 (E22) | **Hedge evaluation** | Score liability hedges by the balance-sheet channel (buffer released, cheaper contingent funding) rather than expected P&L, consistent with the dossier's Borensztein–Jeanne–Sandri yardstick. |
| Jensen 2024 (F23) | **ET overlay parameters** | Calibrate revenue sensitivity (−0.6 to −0.8pp of GDP per −10pp real oil-price inflation) and the rents-loss path for h_t. Treat energy transition as a persistent upward shift in the draw baseline [inference]. |
| Löhndorf & Shapiro 2019 (G24) | **Solver** | Markov-chain SDDP with nested AV@R. Discretize the draw state, or use a smoothed clip, to keep convexity; see Füllner & Rebennack 2025 on SDDP assumptions. |
| Rosen et al. 2019 (B13) | **IC narrative** | Present endowment payout behaviour as contested. Keep the core point, that oil owners draw in busts, on the sovereign evidence. |

### Further relevant candidates (not annotated above; verified Consensus records)
- **[SWF 3.0: How sovereign wealth funds navigated COVID-19 and changed forever](https://consensus.app/papers/details/554f5e983997579aa32a8313d73304b8/?utm_source=claude_desktop)** — D. Lopez, 2023, *J. International Business Policy*, 13 cit., DOI 10.1057/s42214-023-00147-2.
  - Finding: governments withdrew more than US$211bn from SWFs between March 2020 and December 2021.
  - Implication: add 2020 to the demand-bust (DB) draw peer pool.
- **[Investing with Purpose: Evidence from Private Foundations](https://consensus.app/papers/details/18f72439eef650878b6dcf44a2d71cdd/?utm_source=claude_desktop)** — Matteo Binfarè et al., 2026, *Journal of Finance*, 2 cit., DOI 10.1111/jofi.70055.
  - Finding: the 5% minimum spending rule plus accommodative policy led foundations to take more risk and reach for yield; they have underperformed since 2008.
  - Implication: the Devil's-advocate agent should test whether proposals chase the target in order to fund the draw floor.
- **[Pension Liquidity Risk](https://consensus.app/papers/details/65e862e24881598a97200e1611a991ed/?utm_source=claude_desktop)** — Kristy A. E. Jansen et al., 2026, *Review of Financial Studies*, 0 cit., DOI 10.1093/rfs/hhag068.
  - Finding: swap margin calls can exceed 6% of total assets and are met by procyclical sales of safe bonds.
  - Implication: model overlay variation margin consistently with rate moves in the DCR (Treasury seat).
- **[Oil Price Shocks and Stock-Bond Correlation](https://consensus.app/papers/details/93ab74043a255530b3e8db47775de4c2/?utm_source=claude_desktop)** — S. Ziadat et al., 2023, SSRN, 12 cit., DOI 10.2139/ssrn.4360008.
  - Finding: in recessions, oil supply shocks (Ready method) explain the stock–bond correlation; including supply and demand shocks lowers hedging cost.
  - Implication: supports making the duration-hedge rule conditional on Z. See also Pericoli 2020, below.
- **[On risk factors of the stock–bond correlation](https://consensus.app/papers/details/9688e505c393532194785bcdfa3eb4a7/?utm_source=claude_desktop)** — Marcello Pericoli, 2020, *International Finance*, 49 cit., DOI 10.1111/infi.12369.
  - Finding: inflation is procyclical when it is low and demand-driven rather than supply-driven, and that is when the stock–bond correlation turns negative.
- **[Macroeconomic impact of stranded fossil fuel assets](https://consensus.app/papers/details/7a958691d86d50de97f8d6677b6d256e/?utm_source=claude_desktop)** — J. Mercure et al., 2018, *Nature Climate Change*, 364 cit., DOI 10.1038/s41558-018-0182-1.
  - Finding: losses are amplified if low-cost producers "sell out" despite declining demand; US$1–4trn of global wealth is at risk.
  - Implication: raise the supply-glut (SG) / price-war hazard under the energy-transition overlay [inference: consistent with the dossier's OPEC-exit thesis].
- **[How to Construct Monthly VAR Proxies Based on Daily Surprises in Futures Markets](https://consensus.app/papers/details/14a071cec45c5f40954ba1710b8def14/?utm_source=claude_desktop)** — Lutz Kilian, 2024, *JEDC*, 21 cit., DOI 10.1016/j.jedc.2024.104966. Questions whether OPEC-announcement proxies identify oil supply news.
- **[Identification of expectational shocks in the oil market using OPEC announcements](https://consensus.app/papers/details/0ba0415802c954a4903dabb673b55793/?utm_source=claude_desktop)** — Riccardo Degasperi, Consensus year 2026, SSRN, 11 cit., DOI 10.2139/ssrn.6658807.
  - Finding: OPEC surprises mix supply and demand news; restricting the sign of oil–stock co-movement separates them.
  - Implication: a usable identification rule for A2.
- **[Oil price elasticities and oil price fluctuations](https://consensus.app/papers/details/d8743acd2682536c893c63added6179f/?utm_source=claude_desktop)** — Dario Caldara et al., Consensus year 2016 (*JME*), 326 cit., DOI 10.17016/ifdp.2016.1173.
  - Finding: supply shocks explain 50% and global demand 35% of oil price fluctuations; a supply-driven fall in oil prices depresses activity in emerging economies.
- **[The Interaction of Spending Policies, Asset Allocation Strategies, and Investment Performance at University Endowment Funds](https://consensus.app/papers/details/dbb718a2963d55a1b5ae773ef65f8950/?utm_source=claude_desktop)** — K. Brown et al., 2013, NBER, 27 cit., DOI 10.3386/w19517.
  - Finding: about a quarter of endowments change their spending policy each year.
  - Implication: use as a reference class when eliciting the band-override probability p^ov [inference: the dossier's 0.25% a year in normal state N may be low].
- **[Working Paper Series No 5 / 2015 Commodity prices and fiscal policy design: Procyclical despite a rule](https://consensus.app/papers/details/31ff251e7ad35818a0c4fc21b3377e6d/?utm_source=claude_desktop)** — H. Bjørnland et al., 2015, 32 cit. Norway's fiscal policy became more procyclical after its rule was adopted.
- **[The balance between fiscal consolidation and non-oil growth: The case of the UAE](https://consensus.app/papers/details/9f67cdc2ad74511987c86d7af8f169e6/?utm_source=claude_desktop)** — M. Kandil, 2019, *Borsa Istanbul Review*, 17 cit., DOI 10.1016/j.bir.2018.05.002.
  - Finding: UAE oil-price swings significantly affect bank liquidity, domestic credit and FDI.
  - Implication: supports a negative owner beta for domestic bank stakes.
- **[Consumption Smoothing and Shock Persistence: Optimal Simple Fiscal Rules for Commodity Exporters](https://consensus.app/papers/details/c8766d00d6af578d976abab3bed44a0f/?utm_source=claude_desktop)** — A. Mendes et al., 2017, World Bank WP, 5 cit., DOI 10.1596/1813-9450-8035. Because oil shocks are persistent, it is optimal to spend more than two-thirds of windfalls.
- **[Leave the volatility fund alone: Principles for managing oil wealth](https://consensus.app/papers/details/840a55d256775b989a7bbe0e0533adf7/?utm_source=claude_desktop)** — S. Wills, 2018, *J. Macroeconomics*, 4 cit., DOI 10.1016/j.jmacro.2017.12.002. Do not deplete the volatility fund when oil falls; consume only its interest.
- **[Dynamic spending and portfolio decisions with a soft social norm](https://consensus.app/papers/details/62dbecedd3f75999bcf3364f3ba3f122/?utm_source=claude_desktop)** — K. A. Mork et al., Consensus year 2022 (*JEDC*), 0 cit., DOI 10.1016/j.jedc.2023.104667. Spending should be well below the expected return and mostly procyclical; risk-taking modest and procyclical.
- **[Risk Taking and Fiscal Smoothing with Sovereign Wealth Funds in Advanced Economies](https://consensus.app/papers/details/0c6e0c115ef95a64a46a430cf506d3e4/?utm_source=claude_desktop)** — Snorre Lindset et al., 2019, *IJFS*, 6 cit., DOI 10.3390/ijfs7010004. Smoothing draws implies lower risk-taking and possibly procyclical rebalancing.
- **[Alternatives and Liquidity: Will Spending and Capital Calls Eat Your “Modern” Portfolio?](https://consensus.app/papers/details/8935f6aa693b5a87ac77f10001be06a2/?utm_source=claude_desktop)** — Laurence B. Siegel, 2008, *JPM*, 34 cit., DOI 10.3905/jpm.2008.35.1.103.
  - Finding: spending, capital calls and margin can exhaust the liquid sleeve in bear markets.
  - Implication: ladder commitments into illiquids gradually and hold a considerable liquid sleeve.
- **[The liquidity cost of private equity investments: Evidence from secondary market transactions](https://consensus.app/papers/details/cdf4fe53e4cb5afca4f9499a25a85ffb/?utm_source=claude_desktop)** — Taylor D. Nadauld et al., 2019, *JFE*, 66 cit., DOI 10.1016/j.jfineco.2018.11.007.
  - Finding: buyers outperform sellers by a market-adjusted 5pp a year; flexible buyers are paid for supplying liquidity.
  - Implication [inference]: SELL in a demand bust is costly. Purchases by ADIC's hybrid Secondaries group are internal and zero-sum for liquidity.
- **[Background Risk and University Endowment Funds](https://consensus.app/papers/details/bba5c539ac5d59f7bd809353cc8c9dbf/?utm_source=claude_desktop)** — Stephen G. Dimmock, 2012, *REStat*, 73 cit., DOI 10.1162/rest_a_00180. Higher non-financial income volatility goes with lower portfolio risk and more fixed income.
- **[An empirical comparison of stabilization funds and futures hedging for oil exporting developing countries](https://consensus.app/papers/details/6057e76e6aac51ef8b87f85ea5523299/?utm_source=claude_desktop)** — Ricardo Lalloo, 2024, *Rev. Development Econ.*, 3 cit., DOI 10.1111/rode.13126. Futures hedging reduces volatility far more than stabilization funds.
- **[Hedging Government Oil Price Risk](https://consensus.app/papers/details/f607d043586a51e9909677b6023892e9/?utm_source=claude_desktop)** — J. Daniel, 2001, IMF, 70 cit., DOI 10.5089/9781451859416.001.a001. Stabilization funds are inherently flawed; political cost and lack of know-how hold governments back from hedging.
- **Surveys and entry points:**
  - [Rise of the Fiduciary State: A Survey of Sovereign Wealth Fund Research](https://consensus.app/papers/details/f473ce702e4e5dd697b1697359cff9ec/?utm_source=claude_desktop) (W. Megginson et al., 2014, *J. Economic Surveys*, 118 cit.)
  - [Sovereign Wealth Funds in Theory and Practice](https://consensus.app/papers/details/fc9c7a5e88275e07bef6d3893f3fe32c/?utm_source=claude_desktop) (A. James et al., 2022, *Annu. Rev. Resource Econ.*, 11 cit.)
  - [Oil Price Shocks: Causes and Consequences](https://consensus.app/papers/details/96c611980d875df2bb3e65399a6cfbc8/?utm_source=claude_desktop) (Lutz Kilian, 2014, *Annu. Rev. Resource Econ.*, 338 cit.)
  - [Stochastic Dual Dynamic Programming and Its Variants: A Review](https://consensus.app/papers/details/7db5dd5169e35ac19c12c5e823524ce0/?utm_source=claude_desktop) (Christian Füllner et al., 2025, *SIAM Review*, 44 cit.)
  - [Sovereign Risk and Asset and Liability Management-Conceptual Issues](https://consensus.app/papers/details/76de6169b3b35089a58b40cbeb422ec3/?utm_source=claude_desktop) (U. Das et al., 2012, 30 cit.)
  - [How Do Countries Use An Asset And Liability Management Approach? A Survey On Sovereign Balance Sheet Management](https://consensus.app/papers/details/b134aaaaa769504fb4e5c6578adff00b/?utm_source=claude_desktop) (M. C. Cangoz et al., 2018, World Bank WP, 13 cit.; few countries run integrated SALM, and coordination and mandate are the main obstacles).

---

## 5. Papers that challenge the dossier's recommendations

1. **The endowment-"hoarding" contrast (§1.6, §2.6).**
   - *Dossier:* endowments cut payouts after losses (Brown et al. 2014), so ADIC is an "anti-endowment".
   - *Challenge:* Rosen et al. (2019, B13) find symmetric payout responses across more than 700 universities over 1987–2009.
   - *Implication:* call the endowment contrast contested. The core claim, that oil owners draw in busts, still stands on the sovereign evidence the dossier gives, plus Lopez (2023) on more than US$211bn withdrawn in 2020–21 and Shah et al. (2026) on constrained GCC economies drawing buffers in busts.

2. **Shock-type identification evidence (§2.4, §3.1, Table 6.3 priors).**
   - *Dossier:* relies on BH (2019), where supply disruptions explain more of history, and on Känzig (2021) OPEC news shocks.
   - *Challenges:*
     - Braun (2023, C17): supply shocks are minor, about 6% of forecast-error variance;
     - Caldara et al.: supply 50%, global demand 35%;
     - Kilian (2024, *JEDC*): the OPEC-proxy shock may not be supply news;
     - Degasperi: OPEC surprises mix supply and demand news.
   - *Implication:* the SG/DB split of labelled history, and so the transition prior, depends on the identification scheme. Use an ensemble of identifications and carry the label uncertainty through to the IC. Treat Känzig shocks with caution for UAE/OPEC+ event studies.

3. **What triggers the GW state (§1.3, §2.4 table).**
   - *Dossier:* GW means oil up sharply and owner needs rising.
   - *Nuance:* Cuñado et al. (2020, C18) find that geopolitical risk lowers oil returns on average, through demand. Smales (2019) finds higher geopolitical risk associated with higher oil and lower stocks.
   - *Implication:* gate GW on realised export-volume or infrastructure disruption rather than geopolitical-risk indices. The sign of oil in GW is not guaranteed.

4. **Draw smoothing as "valuable warning time" (§6.6).**
   - *Qualification:* Mork et al. (2022, B10) find that smoothing modestly raises depletion risk after large losses. Lindset & Mork (2019) find that smoothed draws imply lower risk-taking and possibly procyclical rebalancing.
   - *Implication:* the smoothing parameter ρ is coupled to investment policy and should be co-optimized with it, not fixed at 0.5 [inference].

5. **Treating countercyclical owner draws as a fixed given (§6.5–6.6, §6.11).**
   - *Normative challenges:*
     - Landon & Smith (2015, B12): fixed withdrawal out of assets is the robust rule;
     - Mendes & Pennings (2017): persistent oil shocks make near-balanced-budget spending close to optimal;
     - Wills (2018): leave the volatility fund alone when oil falls;
     - Mork et al. (2023, *JEDC*): spending should be below expected return and procyclical.
   - *Implication* [inference]: add draw-rule design to the IC and owner dialogue. For example, quantify the hedge-equivalent value of moving from a fiscal-gap-linked draw to a fixed-% rule, alongside the dossier's hedge stack.

6. **DCR construction (§6.8; verifier issue 7).**
   - Cont et al. (2020, D21) support replacing a DCR that mixes conditional-mean inflows with P99 outflows by joint, scenario-consistent solvency–liquidity stress testing (Liquidity at Risk).

7. **"Expect to sit near the cap" in a supply glut (§1.4; verifier issue 1).**
   - The literature implies that draw share and intensity depend on owner buffers and fund size (AlKathiri et al. 2020; Shah et al. 2026).
   - Di Bonaventura-Altuve (2023, *RIPE*) finds that economic crises rarely exhaust SWFs; depletion is mostly driven by political instability ([record](https://consensus.app/papers/details/c0cd86646cfc51a9a9d1692b288e01f3/?utm_source=claude_desktop)).
   - *Implication:* model cap draws as a buffer-conditional stress assumption, not an expectation.

8. **"Buy joint-state hybrids now" (§1.8(v), §6.11.3).**
   - None of the 33 searches found academic evidence on priced oil–equity correlation or correlation skew for such hybrids.
   - The recommendation remains unsupported by the literature, as the verifier noted. This is a gap, not a refutation.

---

## 6. Usage message

No sign-up, upgrade or usage message appeared in any of the 33 Consensus results, so there is nothing to reproduce verbatim.

---

## 7. Method and limitations

### Consensus queries (33, sequential, no filters)

**Citation checks (19 queries covering the 25 works):**
1. Gintschel–Scherer, which also returned Scherer 2009 and 2011
2. *Elephant in the ground*
3. Bodie–Brière, which also returned Moutanabbir–Noureldin and Balding–Yao
4. Lessmann et al.
5. Das et al.
6. Merton endowments
7. Brown et al.
8. Kilian 2009, which also returned BH 2019 and Ready 2018
9. Känzig
10. Robinson–Sensoy
11. Borensztein–Jeanne–Sandri
12. Erbil
13. Kilian–Park
14. Schwartz–Smith
15. Hamilton 1989
16. Rockafellar–Uryasev
17. Meucci
18. Breuer et al.
19. Stulz

**Backfill (14):**
1. SWF withdrawals in oil collapses
2. optimal spending rule for commodity SWFs
3. stabilization-fund rule design
4. time-varying oil–stock correlation regimes
5. sovereign ALM
6. endowment spending with illiquid assets
7. GCC fiscal buffers
8. sovereign oil hedging (Mexico)
9. stock–bond correlation and supply shocks
10. geopolitical risk, oil and stocks
11. energy-transition stranded assets and fiscal risk
12. real-time oil-shock identification
13. institutional liquidity risk and stress testing
14. SDDP with Markov uncertainty

### Web checks
- One WebSearch confirmed Merton (1993).
- Two WebSearch calls (the BJS *JDE* 2013 version, and Breuer et al.) were refused because the session's search budget was exhausted.
- One direct WebFetch of the ijcb.org issue page confirmed Breuer et al. (IJCB 5(3), Sept 2009).

### Limitations
- Consensus truncates author lists and sometimes dates records by their working-paper version. Years and venues are therefore given as shown, with discrepancies noted.
- Several recent (2026) items appear in lower-tier outlets. Examples include Osei-Bonsu et al. on the Feb 2026 Iran shock ([record](https://consensus.app/papers/details/54b56bb12e045b23b93c93e3934fbae3/?utm_source=claude_desktop)) and Temerbulatova et al. on Kazakhstan's National Fund transfers falling with Brent ([record](https://consensus.app/papers/details/f41e7d771b3d57bfa657e9fee42a3952/?utm_source=claude_desktop)). Treat them as leads, not calibration anchors.
- Findings are taken from abstracts only; no full texts were read.
