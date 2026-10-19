# Verification log: Stream 14 (IC deliberation, decision science and human–AI co-deliberation)

**Dossier checked:** `research/dossiers/14_ic_deliberation.md` (dated 2026-10-18). The dossier was not edited.
**Verifier:** adversarial fact-check pass, 2026-10-18

**Method:**

- **Primary sources, fetched directly:** arXiv abstract pages for every flagged arXiv paper.
- **Full texts extracted locally (pypdf):** Du et al. (arXiv PDF); Tessler et al. (*Science* PDF copy); ChatEval (arXiv PDF); SR 11-7 (Federal Reserve PDF); ICD 203 (ODNI archive PDF); the Santiago Principles (IFSWF PDF); and the user's local copy of Lange et al. (`C:\Users\dean\Downloads\2610.18933v1.pdf`).
- **Other primary pages:** the PMC full text of Vaccaro et al.; NBER, AEA, RePEc, PMLR and Europe PMC metadata; the BoE, NBIM, NZ Super, PyPI, artificialintelligenceact.eu and claude.com pages.
- **Secondary sources:** law-firm notes, used only for the adoption status of the EU "Digital Omnibus on AI".
- **Search budget.** The session's shared web-search budget ran out near the end. Three items that the dossier itself marks *(nr)* could not be checked (§6).
- **Formulas.** Every formula and numerical example in dossier §§2.2, 2.4, 6.5, 6.8 and 6.11 was recomputed, and two counterexamples were simulated. Script: `C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\scripts\numcheck14.py` (session scratchpad; key outputs are reproduced in §5).

---

## 1. Summary

41 claims or claim bundles were checked: all 20 flagged by the author, plus 21 others (including three the dossier marked *(nr)*).

| Verdict | Count |
|---|---|
| Confirmed | 35 |
| Corrected | 4 |
| Refuted | 0 |
| Unverifiable | 2 |

**Citations.** No reference is fabricated or garbled. Every arXiv ID, DOI and URL checked resolves to the stated work and authors, including the 2026 items (Lange et al.; fortitudo.tech 1.2.5; the EU AI Act timetable). Remaining citation problems:

- one secondary citation is presented as the cited authors' own finding;
- two works are cited as preprints although peer-reviewed versions with different headline figures or titles exist;
- one regulatory date is sourced to the wrong legal act.

**Errors in the fact layer that would reach the IC:**

1. **Habermas Machine sample size is conflated** (§1, §4 row 1). The 56% vs 44% preference over human mediators comes from **one experiment of 75 six-person groups (n = 439)**. It does not come from the programme N = 5,734. Attaching N = 5,734 overstates the evidential weight of that comparison by about 13×.
2. **Fogliato et al. studied *veterinary* radiologists** (19). The dossier says "radiologists". The same treatment arm also **sought fewer second opinions from colleagues** when they disagreed with the AI, and rated the AI less useful. Both points matter for an IC design.
3. **Sakana misattribution** (§5, §6.10). "An LLM auditor detected flaws far more reliably from logs and code than from the paper alone" is a finding of **Luo et al. (2026)**, which Lange et al. summarize in their related work. It is not a caution of the Sakana authors' own.
4. **BoE/FCA automated-decision shares are put on different bases** (§4 row 14). "24% semi-autonomous" is 24% *of the 55%* with automated decision-making (about 13% of all use cases). "2% fully autonomous" is a share of *all* use cases.

**Most important design-layer problems (details in §4):**

- **R1.** The online experiment cannot detect its own success threshold. BSS +0.05 corresponds to ΔBS ≈ 0.01, about one quarter of the stated minimum detectable effect of 0.04, before clustering is counted.
- **R2.** The "preposterior on the same paths" EVSI is biased upward. Simulated in-sample EVSI is 0.07–1.5 pp when the true value is zero. Because DEFER fires iff EVSI > c_delay, the bias tilts the committee toward DEFER.
- **R3.** The vertex shortcut for max-min fails for the dossier's own CVaR-penalized objectives. In the counterexample, the worst case is understated by 0.09.
- **R4–R9.** Six pieces of evidence are misapplied or over-read: Vaccaro's g < 0 used to justify "no AI vote"; Fogliato's result described as reducing "uncritical" agreement; Choi's "bias toward correction" (actually majority-based in practice); Du et al. used to justify a 2-round cap; the consultancy baseline (dishonest half the time by design); and contested debate-vs-vote evidence presented as settled.

**Overall reliability:**

| Layer | Rating |
|---|---|
| Sourced empirical facts and citations | **HIGH** |
| Design-implication layer (§§3, 6) | **MEDIUM**: specific statistical and decision-theoretic fixes needed before IC or MRM use |
| Composite | **HIGH for use as a research input**, conditional on the corrections below |

None of the problems overturns the dossier's central architecture: independence before interaction, deterministic tools own numbers, dissent is preserved, and humans decide.

---

## 2. Claims table

F = flagged by the author; A = added by the verifier.

| # | Claim (dossier location) | Verdict | Corrected value / note | Source URL |
|---|---|---|---|---|
| F1 | Habermas Machine: preferred 56% vs 44% "(N = 5,734 across experiments)"; group agreement +≈8 pp; unanimous groups 22.8%→38.6% (cohort 1); majority grew in 29–32% of rounds vs minority 20–26%; lacks fact-checking, staying on topic, moderation (§1, §2.5, §4 #1) | **Corrected** | **56% vs 44% comes only from the human-mediator experiment: 75 six-person groups, n = 439** (mixed-model P̂ = 0.575, 95% CI 0.535–0.614). N = 5,734 is the whole programme. Every other number is confirmed verbatim. "About eight percentage points" holds in all three main cohorts; 22.8→38.6% is cohort 1; 29–32% vs 20–26% is exact. The paper says the HM "does not have the mediation-relevant capacities of fact-checking, staying on topic, or moderating the discourse". **Context the dossier omits:** revised statements *overweighted* the minority (weight 0.36 vs 0.29 share); exposure to majority-leaning statements did not predict the shift; similar convergence occurred with human mediators. Science 386(6719) eadq2852, 18 Oct 2024: confirmed. | https://www.science.org/doi/10.1126/science.adq2852 (full text read from a PDF copy) |
| F2 | Du et al.: 3 agents × 2 rounds; arithmetic 67.0→81.8; GSM8K 77.0→85.0; MMLU 63.9→71.1; biographies 66.0→73.8; converged answers "not necessarily correct", models "confidently affirm" (§2.5, §4 #2) | Confirmed | Verbatim (Tables 1–2; Limitations). **Note:** the paper used 2 rounds "due to computational expense" and found "further gains with both more agents and rounds". Its majority-vote baseline sits well below debate (arithmetic 69.0; GSM8K 81.0). Venue: ICML 2024, PMLR 235:11733–11763. | https://arxiv.org/abs/2305.14325 ; https://proceedings.mlr.press/v235/du24e.html |
| F3 | Choi, Zhu & Li: voting explains most of the gains attributed to MAD. Qwen2.5-7B: single 0.721 / vote 0.769 / best debate 0.738. Llama-3.1-8B: 0.620 / 0.724 / 0.699. Debate is a martingale; biasing updates toward correction helps (§2.5, §4 #3) | Confirmed | Table 1 (5 agents): 0.7205 / 0.7691 / 0.7377 (Decentralized, T = 2); 0.6203 / 0.7242 / 0.6990 (Sparse, T = 2). NeurIPS 2025 Spotlight. The martingale is a theorem under the paper's belief model. **Note:** MAD-oracle needs ground truth. The practical variants (MAD-Conformist, MAD-Follower) use the previous round's **majority** as the proxy for "correct". | https://arxiv.org/abs/2508.17536 ; https://arxiv.org/html/2508.17536 |
| F4 | Wynn, Satija & Hadfield: debate can lower accuracy; agents flip correct→incorrect, favouring agreement, even when stronger agents outnumber weaker ones (§2.5) | Confirmed | Abstract. Venue: ICML 2025 MAS *workshop*; v2 dated 13 Oct 2025. | https://arxiv.org/abs/2509.05396 |
| F5 | Laban et al.: 46% average flip rate and 17% average accuracy drop across 10 LLMs and 7 tasks; fine-tuning cut the deterioration by 60% (§2.5, §4 #4) | Confirmed | Abstract; v2 dated 21 Feb 2024. The protocol is a content-free "Are you sure?" challenge on classification tasks with 2023-era models. | https://arxiv.org/abs/2311.08596 |
| F6 | Sharma et al.: sycophancy is a general behaviour of state-of-the-art assistants; human preference judgments likely contribute (§2.5) | Confirmed | Abstract wording. | https://arxiv.org/abs/2310.13548 |
| F7 | Michael et al.: debate 84% vs consultancy 74% judge accuracy; debates 68% of the length; with more skilled debaters, debate accuracy rises and consultancy accuracy falls (§1, §2.5, §4 #5) | Confirmed | Abstract. **Caveat:** by design the consultant argues for the *wrong* answer half the time, and judges never see the source passage. | https://arxiv.org/abs/2311.08702 |
| F8 | Khan et al.: debate raises non-expert models to 76% and humans to 88%, vs naive baselines of 48% and 60% (§4 #6) | Confirmed | Abstract. ICML 2024, PMLR 235:23662–23733. | https://arxiv.org/abs/2402.06782 ; https://proceedings.mlr.press/v235/khan24a.html |
| F9 | Vaccaro et al.: 106 experiments; g = −0.23 vs best of either; −0.27 on decision tasks; +0.64 vs humans alone; +0.46 when humans outperform AI; explanations and confidence displays not significant (§2.6, §4 #7) | Confirmed | All values exact. 95% CIs: −0.39 to −0.07; 0.53 to 0.74; −0.44 to −0.10; 0.28 to 0.66. 106 experiments from 74 papers, 370 effect sizes. Quote "neither of these factors significantly affected the performance of human–AI systems" is verbatim. **Omitted:** g = −0.54 when the AI alone outperforms humans. NHB 8(12):2293–2303, online 28 Oct 2024. | https://pmc.ncbi.nlm.nih.gov/articles/PMC11659167/ |
| F10 | Bansal et al.: explanations increase acceptance "regardless of its correctness" and do not increase complementary performance (§2.6) | Confirmed | CHI '21. AI assistance itself did yield complementary gains; explanations did not add to them. | https://arxiv.org/abs/2006.14779 |
| F11 | Fogliato et al.: recording a provisional decision first made experts less likely to agree with the AI regardless of its accuracy, with no added time; "19 radiologists" (§2.6, §3) | **Corrected** | Participants were **19 veterinary radiologists**. The provisional-first arm was also **less likely to seek a colleague's second opinion** when disagreeing with the AI, and rated the AI less useful. The abstract reports no accuracy gain. FAccT 2022. | https://arxiv.org/abs/2205.09696 |
| F12 | Buçinca et al.: cognitive forcing reduced overreliance vs simple XAI (N = 199) but received the least favourable subjective ratings (§2.6) | Confirmed | PACM HCI (CSCW1), DOI 10.1145/3449287. | https://arxiv.org/abs/2102.09692 |
| F13 | Hackenburg et al.: 19 LLMs, N = 76,977, 466,769 claims; post-training up to +51% persuasion, prompting up to +27%; where these raised persuasion, factual accuracy "systematically decreased" (§2.5, §4 #8) | Confirmed | Abstract. **Citation:** the peer-reviewed version is *Science* 390(6777), 2025, DOI 10.1126/science.aea3884, titled "...with conversational *artificial intelligence*". Cite that version, not the July 2025 preprint. | https://arxiv.org/abs/2507.13919 ; https://researchonline.lse.ac.uk/id/eprint/130605 |
| F14 | Zheng et al. 2024: system-prompt personas do not improve performance across 162 roles and 2,410 questions; effects "largely random" (§2.5, §4 #11) | Confirmed | Findings of EMNLP 2024; 4 model families. Single-agent factual QA, so it does not test multi-agent diversity. | https://arxiv.org/abs/2311.10054 |
| F15 | ReConcile up to +11.4%, with model diversity "critical"; ChatEval: the same role description for every agent degrades performance (§2.5, §6.8) | Confirmed | ReConcile: ACL 2024, wording verbatim. ChatEval abstract: "diverse role prompts (different personas) are essential ... utilizing the same role description ... can lead to a degradation". **Note:** ChatEval's diverse roles were *personality personas*, which the IDM bans. | https://arxiv.org/abs/2309.13007 ; https://arxiv.org/abs/2308.07201 |
| F16 | Hansen, McMahon & Prat: transparency produced both a discipline and a conformity effect; discipline dominates (§2.2, §4 #12) | Confirmed | Abstract ("discipline effect dominates", via their influence measure). QJE 133(2):801–870. | https://doi.org/10.1093/qje/qjx045 ; https://ideas.repec.org/a/oup/qjecon/v133y2018i2p801-870..html |
| F17 | SR 11-7: definition of effective challenge; depends on incentives, competence, influence; an extreme point of a misspecified distribution may not be conservative (§5, §2.7) | Confirmed | Verbatim. The full sentences continue "...limitations and assumptions and produce appropriate changes" and "...if the distribution was misestimated or misspecified in the first place". Federal Reserve and OCC, 4 Apr 2011. | https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107a1.pdf |
| F18 | ICD 203: likelihood bands 1–5, 5–20, 20–45, 45–55, 55–80, 80–95, 95–99%; confidence and likelihood never in the same sentence; assumptions kept separate from information; alternatives; indicators; significant differences brought to customers' attention (§2.3, §5) | Confirmed | Verbatim ("an analytic product must use one of the following sets of terms"). These are Tradecraft Standards 2(a)–(b), 3, 4 and 7; the "brought to the attention of customers" sentence sits under Standard 7. Signed 2 Jan 2015, with a technical amendment on 21 Jan 2022. The PDF also contains a later undated technical amendment on annual training. | https://archive.dni.gov/files/documents/ICD/ICD-203.pdf |
| F19 | EU AI Act Art. 14(4)(b) requires awareness of automation bias; Art. 14(4)(d)–(e) requires ability to disregard, override or reverse outputs, or stop the system (§2.6) | Confirmed | Wording nuance: the provider must supply the system so that overseers are "enabled ... to remain aware". This is a design duty, not a duty placed on overseers. | https://artificialintelligenceact.eu/article/14/ |
| F20 | Lange et al. (Sakana): verification "only as complete as its task-specific evaluators and rubrics"; rubric gates missed runs that altered their evaluation protocol, caught by manual audit; reviewer–performance r = 0.44; claim-to-source map; audit agent; results need human validation (§4 #16, §5, §8) | Confirmed | All verbatim in the local PDF. The protocol change happened in **two of three Pi-harness runs on the RL fine-tuning task**. r = 0.44 uses within-task percentile ranks pooled over 70 campaigns, and the authors read it as a *positive* sign that reviewer scores track performance. arXiv v1 submitted 13 Oct 2026; the PDF header is dated 2026-10-15. | https://arxiv.org/html/2610.18933v1 ; https://arxiv.org/abs/2610.18933 |
| A1 | §5: "The authors stress ... an LLM auditor detected flaws far more reliably 'from logs and code than from the paper alone'". Also §6.10 item 1, tagged [S] | **Corrected** | This is **Luo et al. (2026)**, summarized in Lange et al.'s related-work section. It is not a Sakana finding or caution. The design point may still stand, but cite Luo et al. | https://arxiv.org/html/2610.18933v1 (Related work, "Judging ideas, rubrics, and evidence auditing") |
| A2 | Irving et al.: with optimal play, debate answers any PSPACE question with poly-time judges; sparse MNIST 59.4%→88.9% with 6 pixels (§2.5) | Confirmed | The paper also reports 48.2%→85.2% with 4 pixels. | https://arxiv.org/abs/1805.00899 |
| A3 | Blinder & Morgan: groups decide better and no more slowly; majority rule and unanimity equally fast (§1, §4 #13) | Confirmed | NBER WP 7909, September 2000 (laboratory experiments). | https://www.nber.org/papers/w7909 |
| A4 | Romer & Romer 2008: FOMC members' forecasts add little or no value over the staff's (§2.2; finding recalled) | Confirmed | Combined-forecast tests give FOMC projections about zero weight for inflation and unemployment. AER 98(2):230–35. Later work (Cleveland Fed WP 23-20) finds value in tail-risk narratives. | https://www.aeaweb.org/articles?id=10.1257/aer.98.2.230 ; https://www.nber.org/papers/w13751 |
| A5 | BoE/FCA 2024: 75% of firms use AI, a further 10% plan to; foundation models 17% of use cases; 55% involve some automated decisions "(24% semi-autonomous, 2% fully autonomous)"; 118 respondents (§4 #14) | **Corrected (minor)** | The 24% is "of those", i.e. of the 55% subset, so about 13% of all use cases. The 2% is a share of all use cases. All other figures are exact: 21 Nov 2024, 118 firms. | https://www.bankofengland.co.uk/report/2024/artificial-intelligence-in-uk-financial-services-2024 |
| A6 | Salvi et al.: +81.7% odds of agreement vs human opponents (N = 820), arXiv v1 (§2.5, §4 #9) | Confirmed (v1) | The peer-reviewed version is titled "On the conversational persuasiveness of GPT-4" (Nat Hum Behav 2025, DOI 10.1038/s41562-025-02194-6). It reports **N = 900**: personalized GPT-4 was more persuasive in 64.4% of non-tied pairs, +81.2% relative odds (95% CI +26.0% to +160.7%). Use the journal figures for IC material. | https://arxiv.org/abs/2403.14380 ; https://citations.prolific.com/paper/on-the-conversational-persuasiveness-of-gpt-4 |
| A7 | Schoenegger et al.: LLM assistants raise forecasting accuracy 24–28% (N = 991) (§2.6, §4 #10) | Confirmed | The control was a *less-advanced model*, there were only 6 questions, and a deliberately "noisy" assistant also helped. | https://arxiv.org/abs/2402.07862 |
| A8 | Schoenegger et al.: a 12-LLM crowd was not statistically different from 925 human forecasters; acquiescence (mean prediction > 50%) (§2.5, §4 #10) | Confirmed | | https://arxiv.org/abs/2402.19379 |
| A9 | NBIM (vendor-reported): >20% of weekly time saved on AI-assisted tasks; 600+ Claude users within two months (§4 #15) | Confirmed | Vendor case study based on "internal surveys"; the headline says 20%, the body "more than 20%". Not evidence about deliberation quality. | https://claude.com/customers/nbim |
| A10 | EU AI Act: Annex III obligations from 2 Dec 2027; Annex I from 2 Aug 2028 (§4 #17) | Confirmed | These dates come from the **Digital Omnibus on AI, Regulation (EU) 2026/1744** (Council final adoption 29 Jun 2026; in force late July 2026). The original 2024 text had 2 Aug 2026 and 2 Aug 2027. Cite the amending act. | https://artificialintelligenceact.eu/article/14/ ; https://www.orrick.com/en/Insights/2026/07/EU-AI-Act-Update-Digital-Omnibus-Finalizes-8-Compliance-Changes |
| A11 | fortitudo.tech 1.2.5 (20 Aug 2026), GPL-3.0-or-later; implements sequential entropy pooling and CVaR optimization (§4 #18, §7) | Confirmed | | https://pypi.org/project/fortitudo.tech/ |
| A12 | Santiago Principles: quotations of GAPP 6, 7, 8, 9, 19 and 22 (§2.1) | Confirmed | Verbatim from the IFSWF PDF. | https://www.ifswf.org/sites/default/files/santiagoprinciples_0_0.pdf |
| A13 | NZ Super IC composition (co-CIOs as co-chairs, CRO, Head of Asset Allocation, CEO ex officio, two co-opted members); contrarian tilting sized by deviation from fair value, risk and confidence, with Board-reviewed limits (§5) | Confirmed | | https://www.nzsuperfund.nz/about-the-guardians/management/investment-committee/ ; https://www.nzsuperfund.nz/how-we-invest/actual-portfolio/how-we-add-value/strategic-tilting/ |
| A14 | NBIM governance chain and CEO quote ("Excecutive" [sic]) (§2.1, §5) | Confirmed | The typo is on NBIM's own page. | https://www.nbim.no/en/organisation/governance-model/ |
| A15 | Clark & Urwin: "significant incremental difference to value creation"; coherence / people / process. Drew & Walk: "people, policies, processes, and systems"; "defensible, repeatable, and documented" (§2.1) | Confirmed | | https://ideas.repec.org/a/pal/assmgt/v9y2008i1d10.1057_jam.2008.1.html ; https://rpc.cfainstitute.org/research/foundation/2019/investment-governance-for-fiduciaries |
| A16 | Liang et al.: degeneration-of-thought; adaptive break; modest tit-for-tat; LLM judge may be unfair when debaters are different LLMs (§2.5) | Confirmed | EMNLP 2024 main conference. | https://arxiv.org/abs/2305.19118 |
| A17 | Smit et al.: MAD methods "do not reliably outperform" self-consistency or ensembling, and are hyperparameter-sensitive (§2.5) | Confirmed | **Omitted:** after tuning agreement levels, debate surpassed every non-debate method tested. | https://arxiv.org/abs/2311.17371 |
| A18 | Lorenz et al. 2011: social influence reduces diversity without improving accuracy (§2.2; dossier marks it nr) | Confirmed | Confidence also rose without accuracy gains. PNAS 108(22):9020–9025. | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1073/pnas.1008636108&resultType=core&format=json |
| A19 | Meade & Stasavage 2008: voiced dissent fell after the 1993 transcript decision (§2.2; dossier marks it nr) | Confirmed | Economic Journal 118(528):695–717. | https://ideas.repec.org/a/ecj/econjl/v118y2008i528p695-717.html |
| A20 | Schwenk 1990 meta-analysis: devil's advocacy and dialectical inquiry both beat an expert-recommendation baseline (§2.3; dossier marks it nr) | Unverifiable | The search budget ran out before a source could be retrieved. | — |
| A21 | Collective information-sampling formula, listed under Stasser & Titus 1985 (§2.2) | Unverifiable | The arithmetic is correct (0.30 and 0.882). The formal model is usually credited to Stasser & Titus (1987, JPSP 53:81–93) and Stasser, Taylor & Hanna (1989). This attribution was recalled, not verified this session. | — |

---

## 3. Citation check

The ten most important references, plus every other reference that a load-bearing claim depends on:

| Reference (as cited) | Exists | Authors / year / title / venue | Issue |
|---|---|---|---|
| Tessler et al. 2024, *Science* 386(6719):eadq2852 | Yes | Correct; 12 authors; online 18 Oct 2024 | In-text N is misattached (F1) |
| Du et al. 2024, ICML (PMLR 235) | Yes | Correct; PMLR 235:11733–11763 | None |
| Choi, Zhu & Li 2025, NeurIPS 2025 | Yes | Correct (Spotlight) | None |
| Vaccaro, Almaatouq & Malone 2024, NHB 8:2293–2303 | Yes | Correct; issue 12 | None |
| Michael et al. 2023, arXiv 2311.08702 | Yes | Correct; 7 authors | None |
| Khan et al. 2024, ICML 2024 | Yes | Correct; PMLR 235:23662–23733 | None |
| Hackenburg et al. 2025, arXiv 2507.13919 | Yes | Authors correct | **Peer-reviewed version not cited:** *Science* 390(6777), DOI 10.1126/science.aea3884; title ends "...conversational artificial intelligence" |
| Fogliato et al. 2022, FAccT | Yes | Correct; 10 authors | In-text description wrong: participants were veterinary radiologists (F11) |
| Hansen, McMahon & Prat 2018, QJE 133(2):801–870 | Yes | Correct | None |
| SR 11-7 Attachment (Federal Reserve & OCC, 4 Apr 2011) | Yes | Correct | None |
| ICD 203 (2015; technical amendment 21 Jan 2022) | Yes | Correct | A further, later technical amendment (annual training) also appears in the same PDF |
| EU AI Act Art. 14 "(and Art. 113 timetable as presented)" | Yes | Art. 14 correct | **The timetable comes from Regulation (EU) 2026/1744 (Digital Omnibus on AI)**, which is not cited |
| Lange, Grillotti, Yamada, Charakorn & Ha 2026, arXiv 2610.18933v1 | Yes | Correct; v1 dated 13 Oct 2026 | Author initials missing (R.T., L., Y., R., D.); one secondary finding misattributed (A1) |
| Salvi et al. (2024; *Nat. Hum. Behav.* 2025) | Yes | arXiv title and authors correct | **The journal version's title differs** ("On the conversational persuasiveness of GPT-4"), and its N and headline differ (A6) |
| Laban et al. 2023; Sharma et al. 2023; Wynn et al. 2025; Smit et al. 2023/24; Chan et al. (ChatEval) 2023 | Yes | Authors and titles correct | Venues omitted. Wynn et al. is an ICML 2025 MAS *workshop* paper (verified). ICLR 2024 for Sharma and ChatEval, and ICML 2024 for Smit, were recalled, not verified |
| Bansal 2021; Buçinca 2021; Zheng (personas) 2024; Chen (ReConcile) 2024; Liang 2024; Irving 2018 | Yes | Correct | None |
| Blinder & Morgan 2000; Romer & Romer 2008; Clark & Urwin 2008; Drew & Walk 2019; Lorenz 2011; Meade & Stasavage 2008 | Yes | Correct | None |
| BoE/FCA 2024; Schoenegger ×2 (2024); Santiago Principles; NBIM pages; NZ Super pages; PyPI fortitudo.tech | Yes | Correct | None |

**Verdict.** No hallucinated or garbled references were found. Fixes needed:

- cite Hackenburg et al. in *Science* (2025);
- use the Nature Human Behaviour title and figures for Salvi et al.;
- source the EU dates to Regulation (EU) 2026/1744;
- re-attribute the "logs and code" finding to Luo et al. (2026).

---

## 4. Reasoning issues and overclaims in the design implications

Ranked by severity. Numbers marked † come from `numcheck14.py` (§5).

**R1 [High]. The online experiment cannot detect its own success criterion** (§6.11).

- The power arithmetic is right: SE(Δ) = 0.0141 and the minimum detectable effect (MDE) is 0.0396 in Brier-score units, at 80% power and two-sided 5%.
- The success threshold is "BSS gain ≥ 0.05". With BS_model = 0.15–0.25, that is a ΔBS of only **0.0075–0.0125**. The MDE is **3.2–5.3× too large**. Detecting the threshold needs about **4,000–11,000 independent forecasts per arm**.†
- Randomization is at the agenda-item level, and forecasts within an item share questions and outcomes. Effective n per arm from "400 forecasts" is therefore about 28–118 under plausible intraclass correlations (design effect 3.4–14.4).†
- "Plan for 2 years" is unsupported. The Brier model also lacks an item-level random effect.
- **Fix:** power the experiment on resolved questions or items with an estimated ICC. Pool across years. State success as ΔBS with a credible interval. Otherwise treat the experiment as descriptive.

**R2 [High/Medium]. EVSI "preposteriorly on the same paths" is biased upward, and so is DEFER** (§6.5e, §2.4).

- Choosing the best action in each bin and evaluating it on the same paths is in-sample optimization.
- Simulation with true EVSI = 0 (N = 50,000; per-path payoff-difference sd 0.30): in-sample EVSI = **0.07–1.51 pp**, rising with the bin count (5–50) and the number of candidate actions (2–20). Cross-fitting removes the bias (≈0).†
- Because "DEFER iff EVSI > c_delay", this bias systematically favours DEFER.
- The rule is also **myopic**. It ignores repeated deferral, staged or partial actions, and information that arrives whether or not the decision is deferred.
- It also requires J and c_delay in **common units**: J is P(10%) or a CE return, while c_delay is carry and bid expiry in dollars. No conversion is specified.
- **Fix:** cross-fitted or hold-out-path EVSI (or regression-based EVSI), with a bin-count sensitivity check, a reported CI and an explicit unit conversion.

**R3 [Medium]. The vertex shortcut for max-min fails for the dossier's own objectives** (§2.4, §6.5b/d).

- "J linear in q ⇒ inner minimum at a vertex (K+1 evaluations)" is true only if J is linear in q, or monotone in a linear functional of q.
- The dossier's objectives include CVaR and drawdown penalties (LEVER: −λ_DD ΔCVaR_q). CVaR is concave in q, so J is convex in q, and its minimum over the hull can be interior.
- Counterexample: scenarios with returns (−30%, 0, +30%); q1 = (0, 1, 0); q2 = (0.2, 0, 0.8); J = E_q[r] − CVaR90_q. Then J(q1) = 0.000 and J(q2) = −0.120, but the hull minimum is **−0.210** at the midpoint. The robust value is overstated by 0.09.†
- **Fix:** either define the credal set as the *finite* set {q_k, p}, so K+1 evaluations are exact by definition, or solve the inner minimum as a convex program.

**R4 [Medium]. Vaccaro et al. is misapplied to "No AI vote counts in the IC ballot (decision tasks show g < 0)"** (§3).

- g < 0 compares human–AI combinations with the *better* of the two acting alone.
- The losses concentrate where the AI alone beats humans (g = −0.54). There, adding humans drags down AI-level performance.
- This says nothing against AI votes. If anything it implies that human overrides of a superior model destroy value.
- **Fix:** keep the policy, but ground it in accountability (GAPP 6–9, EU AI Act Art. 14, SR 11-7), and keep the BSS-vs-model override metric.

**R5 [Medium]. Executive-summary overclaim: "human-first ordering reduces uncritical agreement with AI [S]"** (§1 item 3(ii)).

- Fogliato et al. (19 *veterinary* radiologists) found lower agreement **regardless of AI accuracy**, fewer second-opinion requests when participants disagreed with the AI, and lower perceived usefulness. No accuracy gain is reported.
- The fewer-second-opinions finding cuts directly against a deliberative design.
- **Fix:** reword to "reduces agreement with AI, right or wrong". Keep the §8 caveat and monitor appropriate reliance.

**R6 [Medium]. Choi et al. is cited as the basis for the evidence-gated 5 pp update rule** (§2.5 synthesis, §6.8).

- Choi's non-oracle "correction" interventions (MAD-Conformist and MAD-Follower) bias each agent toward the **previous round's majority**. That is conformity, the opposite of the IDM's anti-conformity stance. Their oracle variant needs ground truth.
- Evidence-gated updating is untested, and the 5 pp threshold has no empirical source.
- **Fix:** label the rule [I] and add it to the ablation suite: vote vs vanilla debate vs evidence-gated debate.

**R7 [Medium]. Contested evidence is presented as settled** (§1, §2.5, §3).

- "Majority voting explains most of debate's gains; debate alone is a martingale" rests on 7–8B open models with 5 agents. The martingale is a model-based theorem.
- Du et al. found debate well above majority voting (arithmetic 81.8 vs 69.0; GSM8K 85.0 vs 81.0).
- Smit et al. found that debate surpassed non-debate methods once agreement levels were tuned.
- **Fix:** describe the evidence as mixed and rely on ADIC's own ablations. The default "ensemble for estimates" remains reasonable.

**R8 [Low/Medium]. The 2-round debate cap is attributed to Du et al.** (§6.8).

- Du et al. used 2 rounds only "due to computational expense" and reported further gains from more rounds and agents.
- Valid support exists elsewhere: Choi (decentralized MAD peaks at T = 2 and declines at T = 3 and 5), ChatEval (no gain from more turns) and Wynn (degradation over rounds).

**R9 [Medium]. The consultancy baseline is misread** (§1, §2.5).

- In Michael et al. the single consultant argues for the wrong answer **half the time by design**, and judges never see the source text.
- So 84% vs 74% does not show that debate beats an *honest* single memo, and IC members do have access to evidence.
- **Fix:** state that the transfer is at the level of mechanism only.

**R10 [Medium]. The Monte Carlo "grey out < 2 SE" rule uses the wrong standard error** (§6.5a, §6.8).

- Comparisons between view sets or actions are computed on the *same* 50k paths (common random numbers). The SE of a *difference* is usually much smaller than the marginal Kish SE, so the rule hides real differences.
- Conversely, Monte Carlo SE excludes model and parameter uncertainty, so a "significant" sub-pp difference conveys false precision.
- **Fix:** use paired or bootstrap SEs for differences, plus a separate band for model uncertainty.

**R11 [Medium]. Max-min over member-reported beliefs can be manipulated, and the voting rule is asymmetric** (§1, §2.4, §6.2, §6.5e).

- Under max-min, the most pessimistic *admissible* member determines a^MM. That is a de facto veto, at odds with "one member, one vote", and it invites strategic shading of stated views. The KL bound η_max limits this but does not remove it.
- The ⅔ supermajority applies only to irreversible *actions*. Inaction can be just as irreversible, for example letting a secondary bid expire or forgoing a refinancing window. In a declining-DPI liquidity squeeze, this tilts the IC toward HOLD.
- **Fix:** present a^MM as a diagnostic. Prefer minimax regret within η_max. Treat expiring options as irreversible, or use symmetric thresholds.

**R12 [Medium]. The AI Validator holds a publication veto and is claimed to satisfy SR 11-7** (§5, §6.3).

- SR 11-7's incentives, competence and influence describe *human* organizational arrangements: separation from model development, competence, and organizational standing. Running on a different model family is not separation of incentives in SR 11-7's sense.
- An LLM seat that can block what the IC sees conflicts with §2.1 ("no AI agent holds a seat with decision rights").
- **Fix:** a human validator owns the veto. The AI validator raises flags, and blocked items still reach the IC with the flag attached. The deterministic numeric-provenance parser is fine as a tool gate.

**R13 [Low/Medium]. The entropy-pooling confidence blend changes the view the member confirms** (§6.5a).

- With c = 0.6, the view "PE distributions 30% below base" moves E[D] only **18%** below base: 0.4 × 1 + 0.6 × 0.7 = 0.82.†
- The back-translation that the member confirms must show the *effective* post-blend view.

**R14 [Low]. The model-family arithmetic is inconsistent** (§6.3, §6.8).

- With 7 substantive seats and at most 40% per family, a family can hold at most 2 seats. That requires **at least 4 families, not 3**.†
- A validator "on a different family from the proposing seats" may need a fifth.

**R15 [Low]. Habermas "majority drift" is used as a design rationale without the paper's countervailing results** (§2.5, §3, §8).

- Revised HM statements overweighted the minority.
- Exposure to majority-leaning statements did not predict the shift.
- Similar convergence occurred with human mediators.
- The drift is therefore not shown to be AI-specific.

**R16 [Low]. Selective citation on personas** (§3, §6.3).

- ChatEval's gains came from *personality personas*, and Du et al. found that persona initialization raised MMLU from 71.1 to 74.2.
- The Zheng et al. null result concerns single-agent factual QA.
- A ban on personas can be justified by caricature risk, but ChatEval does not support it.

**R17 [Low]. Smaller parameter and specification issues.**

- **Credibility constant (§6.8).** In Bühlmann's model, K = EPV/VHM is *estimated*, not set; and "equal weights until n ≥ 30, then credibility" double-counts the shrinkage.
- **ENS/N = e^(−KL) (§6.5a)** holds only under the uniform prior. After the mandated tilted re-simulation, define the flags in KL(q‖p).
- **SELL / REFINANCE break-evens (§6.5d).** The algebra is verified correct, but κ_i and r* are undefined, and μ_L is applied to today's cash only, as a constant, even for non-marginal sales. Future calls, distributions and repayments carry their own liquidity shadow values, and REFINANCE omits the present value of principal repayment.
- **Internal inconsistencies:**
  - S0 specifies 8–15 elicitation questions, while §6.8 says 10–20 per meeting.
  - S4 specifies 3–6 signposts *per failure mode*, while §6.8 says 3–6 *per decision*.
  - The online experiment shows the AI memo before the pre-vote on half of items, contradicting safeguard 6 unless an explicit carve-out is added.
- **Flip-rate baseline.** Using Laban et al.'s 46% as the baseline for the "< 10% unjustified flip" target conflates content-free challenges on 2023-era models with challenges that carry evidence. Take the baseline from the in-house regression suite.

---

## 5. Arithmetic re-verification

All of the dossier's arithmetic is correct. Output of `numcheck14.py`:

| Item (dossier location) | Dossier value | Recomputed |
|---|---|---|
| Hidden profile, p = 0.3 (§2.2) | 30%, 88% | 0.300, 0.8824 |
| ENS/N ↔ KL flags (§6.5a) | 1.20 / 2.30 nats | 1.2040 / 2.3026 |
| Kish SE at P = 0.5 (§6.5a) | 0.22 pp / 0.71 pp | 0.224 / 0.707 pp |
| Power (§6.11) | SE ≈ 0.014, MDE ≈ 0.04 | 0.01414, 0.0396 |
| Tier-A trigger (§6.2) | ≈ $0.44bn | $0.4425bn |
| Exact Shapley, m = 10 (§7) | 1,024 runs | 1,024 |
| Discursive dilemma (§2.4) | conclusion HOLD, premises SELL | HOLD / SELL |
| SELL break-even d† (§6.5d) | algebra | Verified: μ_L = 0, 0.10, 0.25 gives d† = 0.130, 0.209, 0.304, so higher μ_L raises d† as claimed |
| Bühlmann Z = n/(n+K), K = EPV/VHM; Brier/Murphy decomposition; Hedge update; EP dual and Gibbs form; confidence pool | formulas | Correct as written |

Counterexample and simulation outputs used in §4: R1 (forecasts needed, design effects), R2 (in-sample EVSI 0.068–1.508 pp vs cross-fitted ≈ 0), R3 (hull minimum −0.210 vs vertex minimum −0.120), R13 (effective view 18%), R14 (at least 4 families).

---

## 6. Not verified this session

The web-search budget ran out. The dossier itself marks these items *(nr)*:

- Schwenk (1990) meta-analysis result;
- the origin of the information-sampling formula (Stasser & Titus 1987 vs 1985);
- Clark & Urwin's twelve-findings list (paywalled);
- Lu, Yuan & McLeod (2012) magnitudes;
- the MAP description in Kahneman, Lovallo & Sibony (2019; MIT SMR, paywalled);
- CPP Investments and Future Fund governance practices;
- Britton et al. (1998) and Kay et al. (2016).

None of these is load-bearing for a numeric claim in the IC package.

---

## 7. Overall reliability rating

- **Sourced facts and citations: HIGH.** 35 of 41 claims are confirmed and 0 refuted. The 4 corrections are a misattached sample size, a population mislabel, a secondary-citation misattribution and a mixed percentage base. All references exist.
- **Design implications: MEDIUM.** The direction of the design is sound. But the evaluation plan is underpowered relative to its own success criterion, the DEFER rule rests on an upward-biased EVSI estimator, the max-min shortcut is invalid for CVaR-penalized objectives, and several design choices cite evidence that does not support them (R4–R9).
- **Composite: HIGH as a research input, conditional on applying the corrections in §§2–4.** Fix R1, R2, R3 and the executive-summary wording (F1, F11, R4, R5) before any material goes to the IC.

---

## Citation corrections (2026-10-18)

- Erratum (source: `research/literature/recheck/14_ic_deliberation.recheck.md`, rows 22–23): two acceptances above were incomplete. (1) §3 lists Fogliato et al. as "Correct; 10 authors", but the dossier gave the arXiv v1 author order. The FAccT '22 proceedings order is Fogliato, Chappidi, Lungren, Fisher, Wilson, Fitzke, Parkinson, Horvitz, Inkpen, Nushi (pp. 1362–1374, DOI 10.1145/3531146.3533193). (2) F15 confirmed "up to +11.4%" beside ReConcile's model-diversity quote, but the 11.4% is ReConcile's gain over prior single- and multi-agent baselines, not a diversity effect. Both are now corrected in the dossier. So are A20 (Schwenk 1990, since checked against its abstract: the dossier overstated DI) and the citation points in F1, F11, F13 and A6 (see the dossier's "Citation corrections (2026-10-18)").
