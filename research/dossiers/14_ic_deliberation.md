# Stream 14: Investment-Committee Deliberation, Decision Science and Human–AI Co-Deliberation

**Project:** ADIC multi-period robust Total Portfolio Approach (TPA) framework
**Dossier date:** 2026-10-18
**Scope:** How the Investment Committee (IC) should discuss and decide using the framework's probabilistic outputs, and how AI agents can improve that deliberation rather than degrade it.

**Evidence tags**

| Tag | Meaning |
|---|---|
| **[S]** | Sourced fact (citation in §10) |
| **[P]** | Practitioner consensus or documented institutional practice |
| **[I]** | This team's inference or design choice |
| *(nr)* | Standard reference cited from the literature but **not re-verified** in this session |

Parameter values tagged [I] are defaults to be calibrated. They are not findings.

**Method note.** The session's shared web-search budget ran out after a few queries, so most evidence was gathered by fetching primary sources directly (arXiv, journals, regulators, fund websites). Full texts were extracted and read where reachable: Tessler et al. 2024, Du et al. 2023, ChatEval, ICD 203, SR 11-7, the Santiago Principles and the Sakana "Agentic Scientist" paper. Items marked *(nr)* could not be re-fetched (paywalls, timeouts); check them before external use.

---

## 1. Executive summary

**1. The IC is where model value is realized or lost.**

- The framework will produce joint distributions over 5-year paths. From these come P(10%), P(7% floor breach), liquidity survival, shadow prices, and asset-level SELL / HOLD / REFINANCE / LEVER recommendations.
- These outputs only improve decisions if the committee can absorb them without the well-documented group failure modes:
  - groupthink;
  - under-sampling of uniquely held information ("hidden profiles");
  - anchoring and cascades;
  - noise between members;
  - conformity under transparency.
- These failure modes are systematic, not random. Committees still outperform individuals on average: in Blinder & Morgan's experiments, groups decided better and no more slowly [S].
- The goal is therefore to engineer the committee's information flow, not to replace the committee.

**2. Evidence on AI in deliberation is real but conditional (numbers in §4).**

- *Where AI helped.* AI mediation found common ground: Habermas Machine statements were preferred to human mediators' 56% vs 44% (one experiment: 75 six-person groups, n = 439; N = 5,734 is the whole programme) [corrected 2026-10-18: the preference was not measured on N = 5,734] and within-group agreement rose ≈ 8 pp, but views drifted toward the majority and the system lacks fact-checking [S]. Debate improved some reasoning tasks (arithmetic 67.0→81.8%) [S] and, crucially, helps a judge who cannot see the evidence: 84% vs 74% judge accuracy for debate vs consultancy, in which a single expert argues for one answer that is correct half of the time [S].
- *Where AI disappointed or harmed.* Majority voting explains most of debate's gains, and debate alone is a martingale in expected correctness [S]. Debate can lower accuracy as agents flip to agree [S]; challenged LLMs flip ≈ 46% of the time [S]; sycophancy is pervasive [S]. Human–AI teams underperform the better of the two on decision tasks (g = −0.27) [S]; explanations raise acceptance "regardless of its correctness" [S]; persuasion-boosting methods "systematically decreased factual accuracy" (N = 76,977) [S].

**3. Design consequence [I].**

The AI layer should be an *information-surfacing and challenge machine* that sits on top of deterministic tools. It should not act as an oracle, a voter or a persuader. We propose an **IC Deliberation Module (IDM)** with four parts.

- **(i) An AI shadow-IC.** Seats defined by mandate, evidence slice and loss function, on ≥ 3 model families. Protocol: independent assessment → simultaneous reveal → evidence-gated debate on ≤ 3 cruxes → pre-mortem → immutable minority reports → questions for the human IC ranked by value of information.
- **(ii) A human-IC console.** Blind pre-votes are recorded before any AI conclusion is shown (human-first ordering reduces anchoring on AI output [S], with no accuracy gain shown) [corrected 2026-10-18: was "reduces uncritical agreement with AI"]; Q&A is grounded in run artifacts; members condition the 50k-path scenario set live on their own views via entropy pooling; a disagreement map shows each member's views → implied action; ballots capture rationale and preserve dissent.
- **(iii) Safeguards.** No number without a tool citation (run_id + artifact hash); append-only dissent; agents never tuned or selected on whether humans adopted their advice; agents blind to authority signals; seeded-error drills to monitor automation bias, which training does not prevent. Aligned with SR 11-7 "effective challenge", ICD 203, EU AI Act Art. 14(4)(b) and Santiago GAPP 6/9.
- **(iv) Evaluation.** Ablations (single agent vs voting ensemble vs debate); hidden-profile and seeded-error suites; a forecast registry scoring humans and agents against the model baseline; noise audits; an "anti-portfolio" of rejected deals; item-level randomization of when the AI memo is shown.

**4. The conceptual core: aggregate beliefs, not verdicts [I].**

- Every member's (and agent's) views become a re-weighting $q_k$ of the *same* scenario set. The *same* deterministic optimizer maps each $q_k$ to an implied decision $a^*_k$.
- The committee sees three things:
  - (a) belief disagreement;
  - (b) *decision-relevant* disagreement, i.e. each member's regret, under their own beliefs, from the committee choice;
  - (c) the cruxes that drive it, ranked by expected value of information.
- Disagreement splits into two parts:
  - a **belief** part, which is empirical, can be resolved by diligence, and justifies DEFER when EVSI exceeds the cost of delay;
  - a **value** part (shadow prices, risk appetite), which the Board or owner owns.
- The robust committee choice is max-min, or minimax-regret, over the members' credal set within Tier-1 feasibility. This is the committee analogue of the prior deck's misspecification-robust 7% floor.
- Aggregating premises (views fed through the optimizer) and aggregating conclusions (votes) can disagree; this is the discursive dilemma. The IDM shows both and flags any divergence.

---

## 2. Core concepts and theory

### 2.1 The IC as the last link in a delegation chain

**Santiago Principles [S].** The governance frame for sovereign funds is the Santiago Principles: 24 Generally Accepted Principles and Practices (GAPP), endorsed by IFSWF members. The relevant principles are:

- **GAPP 6:** the governance framework "should be sound and establish a clear and effective division of roles and responsibilities".
- **GAPP 7:** the owner sets objectives, appoints the governing bodies and exercises oversight.
- **GAPP 8:** governing bodies need "a clear mandate and adequate authority and competency".
- **GAPP 9:** operational management should "implement the SWF's strategies in an independent manner".
- **GAPP 19:** investment decisions should aim to maximize risk-adjusted financial returns on economic and financial grounds.
- **GAPP 22:** the fund needs a framework that identifies, assesses and manages risk.

**Clark & Urwin (2008) [S].** Good governance "makes a significant incremental difference to value creation". Best practice is organized into **coherence** (mission, capacities), **people** (competence, roles) and **process** (decision making and implementation). Their twelve findings include mission clarity, deliberate use of the governance time budget, strong investment beliefs, risk budgeting, real-time decision capacity and a learning organization *(list paraphrased; nr)*.

**Ambachtsheer.** His "governance deficit" work links governance quality to fund performance *(nr)*.

**Drew & Walk (2019) [S].** Writing for the CFA Institute Research Foundation, they frame governance as "people, policies, processes, and systems". They ask for a process that is "defensible, repeatable, and documented", which also serves as evidence of diligence.

**Peer chains [S] (details in §5):**

- **NBIM:** Storting → Ministry of Finance (management mandate) → Norges Bank Executive Board → CEO → leader group.
- **NZ Super:** the Board retains investment policy, total-fund risk and strategy approval. A management Investment Committee handles the liquidity profile, new investments and opportunity-level risk budgets.

**Implication [I].** The IC decides within delegated authority, escalates what lies beyond it, and leaves an auditable record for the owner. AI is staff work: no AI agent holds a seat with decision rights.

### 2.2 Why committees fail predictably

**Groupthink** (Janis 1972/1982) *(nr)*. Symptoms include illusions of invulnerability and unanimity, self-censorship, pressure on dissenters and self-appointed "mindguards". Remedies: an impartial leader, an assigned critical evaluator, outside experts, parallel subgroups, and a **second-chance meeting** to air residual doubts before final commitment.

**Hidden profiles** (Stasser & Titus 1985) *(verified 2026-10-18, literature check)*.

- Group discussion over-samples information that members already share. In the collective information-sampling model [unverified: this formula's attribution to Stasser & Titus 1985 is unconfirmed; it is usually credited to later model papers], a fact held by $h$ of $n$ members surfaces with probability

$$p_{\text{mention}}(h)=1-(1-p)^{h}.$$

- With $p = 0.3$, a fact held by one member surfaces 30% of the time. A fact held by six members surfaces 88% of the time (illustrative numbers).
- The 25-year meta-analysis by Lu, Yuan & McLeod (2012) finds that groups mention common information far more than unique information, and rarely solve hidden-profile tasks *(magnitudes nr)*.
- *ADIC translation [I]:* the financing specialist's knowledge of NAV-loan covenants, or the overlay desk's knowledge of collateral terms, is precisely the uniquely held fact that tends to get lost.

**Social influence and anchoring.**

- Exposure to others' estimates reduces their diversity without improving accuracy (Lorenz et al. 2011) *(nr)*.
- First numbers and first speakers anchor the discussion (Tversky & Kahneman 1974).

**Transparency effects.**

- After FOMC members learned in 1993 that transcripts would be published, voiced dissent fell (Meade & Stasavage 2008) *(nr)*.
- Hansen, McMahon & Prat (2018) find both a positive *discipline* effect and a negative *conformity* effect after transparency, with discipline dominating on their influence measure [S].
- *Implication [I]:* record positions and rationales in a structured form. Treat verbatim transcripts as a separate policy choice.

**Noise.**

- Unwanted variability between professionals judging identical cases is large, and is invisible without a *noise audit* (Kahneman, Sibony & Sunstein 2021).
- The **Mediating Assessments Protocol (MAP)** of Kahneman, Lovallo & Sibony (2019) breaks a decision into pre-defined assessments. These are scored independently and factually, ideally as percentiles against a reference class, before any holistic judgment *(core steps confirmed 2026-10-18 via a readable summary that cites the article, Sydney Business Insights, May 2019: criteria defined in advance, fact-based independent assessments, holistic judgment delayed to the final evaluation. Percentile scoring against a reference class is unverified; the MIT SMR full text is paywalled)*.

**Do policymakers add value over staff?**

- Romer & Romer (2008) ask whether FOMC members' own forecasts add value over the staff's forecasts *(citation verified; finding recalled as little-or-no value added, nr)*.
- This is the direct analogue of an IC overriding model probabilities. The IDM therefore *measures* override value (§6.11).

### 2.3 The decision-hygiene toolkit

| Technique | Mechanism | Evidence | IDM use |
|---|---|---|---|
| Independent estimates before discussion | Preserves diversity; prevents anchoring and cascades | Wisdom-of-crowds theory; Lorenz et al. *(nr)*; human-first ordering reduces anchoring on AI output, with no accuracy gain shown (Fogliato et al.) [S] | S1, H0 |
| MAP | Structures holistic judgment; reduces noise | Kahneman et al. 2019 (core steps confirmed via a secondary summary, §2.2), 2021 *(nr)* | Asset-level SELL/HOLD/REFI/LEVER scorecards |
| Delphi / Nominal Group Technique | Anonymous iterated estimates; silent idea generation | Dalkey & Helmer 1963; Delbecq & Van de Ven 1971; Rowe & Wright 1999; Diehl & Stroebe 1987 (nominal > interacting brainstorming) *(nr)* | Reveal and re-estimate rounds |
| Pre-mortem | Prospective hindsight surfaces failure paths | Klein 2007 [S]; Mitchell, Russo & Pennington 1989 *(nr)* | S4, H3 |
| Devil's advocacy (DA) vs dialectical inquiry (DI) | Structured conflict | Schwenk 1990 meta-analysis [S]: DA beat an expert-recommendation baseline. DI's advantage over the expert approach was not demonstrated on relatively ill-structured tasks, and neither DA nor DI beat the other [corrected 2026-10-18: was "both beat an expert-recommendation baseline"] | Standing red-team seat (DA); DI only on cruxes with explicit rival assumption sets [I] [corrected 2026-10-18: was "DI on cruxes"] |
| ACH; key-assumptions check; indicators and signposts | Hypothesis × evidence matrix; linchpin assumptions; tripwires | Heuer 1999; Heuer & Pherson; ICD 203 Standards 2–4 [S] | S0, S4 |
| Reference-class forecasting | Outside view corrects optimism | Lovallo & Kahneman 2003; Flyvbjerg 2006 *(nr)* | Outside-View seat; underwritten-vs-actual drift |
| Calibrated probabilities and proper scoring | Accountability for accuracy | Brier 1950; Murphy 1973; Mellers et al. 2014; Tetlock & Gardner 2015 *(nr)* | Forecast registry |
| Decision journals; Decision Quality (DQ) chain | Separates decision quality from outcome luck | Spetzler, Winter & Meyer 2016 *(nr)* | Decision ledger; review rubric |

**Mapping words to numbers [S].** ICD 203 (signed January 2015, amended January 2022) requires fixed likelihood bands:

| Term | Probability |
|---|---|
| almost no chance | 1–5% |
| very unlikely | 5–20% |
| unlikely | 20–45% |
| roughly even chance | 45–55% |
| likely | 55–80% |
| very likely | 80–95% |
| almost certain | 95–99% |

ICD 203 also requires that:

- confidence levels and likelihood terms are never combined in the same sentence;
- assumptions are kept distinct from underlying information;
- alternatives are analyzed;
- indicators are named;
- changes in judgment are explained.

The IDM adopts these rules as its house style [I].

### 2.4 Formal aggregation and robust committee choice

**Opinion pools** *(textbook results; nr)*.

- The linear pool is $p_c=\sum_k w_kp_k$. It preserves marginal distributions.
- The logarithmic pool is $p_c\propto\prod_k p_k^{w_k}$. It is "externally Bayesian".
- Sources: Genest & Zidek 1986; Clemen & Winkler 1999.

**Extremizing** *(Baron et al. verified 2026-10-18, literature check; Satopää et al. nr)*.

- The aggregate is pushed away from 0.5:

$$p_c=\operatorname{logit}^{-1}\Big(\alpha\sum_k w_k\operatorname{logit}p_k\Big),\qquad \alpha>1.$$

- This is justified when forecasters hold partly independent information, or when individual forecasts are regressed toward 0.5 (Baron et al. 2014; Satopää et al. 2014).
- *Inference [I]:* LLM agents share pre-training data, so their errors are correlated. Their ensembles should **not** be extremized ($\alpha\le1$). Humans should be extremized only once they have a track record.

**Performance weighting** *(nr)*.

- Cooke's classical model weights each expert by calibration × informativeness on seed questions.
- The IDEA protocol (Hemming et al. 2018) runs Investigate → Discuss → Estimate → Aggregate, with anonymous estimate, discuss, re-estimate rounds.

**Actuarial credibility (cross-discipline transfer) [I].**

- Bühlmann (1967) credibility gives a shrinkage weight for each member's estimated skill:

$$\hat s_k=Z_k\bar s_k+(1-Z_k)\bar s,\qquad Z_k=\frac{n_k}{n_k+K},\qquad K=\frac{\mathbb E[\sigma^2_{\text{within}}]}{\operatorname{Var}(\text{true skill})}.$$

**Judgment aggregation: the discursive dilemma** *(List & Pettit verified 2026-10-18, literature check)*.

- Majority voting on premises and majority voting on conclusions can give different answers (List & Pettit 2002).
- *ADIC example [I].* Decision rule: SELL iff ¬P1 ∧ P2, where:
  - P1 = "PE distributions recover within 24 months";
  - P2 = "the secondary-market discount is ≤ 12%".

| Member | P1 | P2 | Implied action |
|---|---|---|---|
| A | ¬P1 | P2 | SELL |
| B | P1 | P2 | HOLD |
| C | ¬P1 | ¬P2 | HOLD |

- The conclusion vote is HOLD, 2–1.
- The premise majorities are ¬P1 (A, C) and P2 (A, B), which imply **SELL**.
- The scenario engine aggregates premises natively. The IDM computes both answers and flags the divergence.

**Robust choice over a credal set** *(textbook decision theory; nr)*.

- Treat the members' posteriors $\{q_k\}$, plus the model baseline $p$, as a credal set $\mathcal Q$.
- Maxmin expected utility (Gilboa & Schmeidler 1989):

$$a^{\text{MM}}=\arg\max_a\min_{q\in\mathcal Q}J(a;q).$$

  - When $J$ is linear in $q$ (e.g. $J=\sum_s q_s u(a,x_s)$), the inner minimum lies at a vertex. Evaluating it costs $K+1$ evaluations.
- Minimax regret (Savage):

$$a^{\text{MR}}=\arg\min_a\max_k R_k(a),\qquad R_k(a)=J(a^*_k;q_k)-J(a;q_k).$$

**Value of information and deferral** *(theory nr; application [I])*.

- Let $\pi$ be the committee's mixture belief about a contested quantity $\theta$. Then:

$$\text{EVPI}=\mathbb E_\pi\big[\max_aJ(a;\theta)\big]-\max_a\mathbb E_\pi J(a;\theta),$$

$$\text{EVSI}=\mathbb E_y\big[\max_a\mathbb E_{\pi\mid y}J\big]-\max_a\mathbb E_\pi J.$$

- DEFER is optimal iff the EVSI of information obtainable by the next decision date exceeds $c_{\text{delay}}$. The cost of delay covers carry, expiry of secondary bids and decay of the opportunity.
- This is the decision-analytic and real-options reading of "defer" (Howard 1966; Dixit & Pindyck 1994).

### 2.5 Machine deliberation: what the evidence supports

**Theory [S].**

- Irving, Christiano & Amodei (2018) show that, with optimal play, "debate … can answer any question in PSPACE given polynomial time judges".
- In their sparse-MNIST experiment, a judge's accuracy rose from 59.4% to 88.9% with 6 pixels revealed through debate.
- The mechanism is *adversarial revelation of evidence to a judge who lacks it*.

**Positive empirics [S].**

- **Du et al. (ICML 2024),** 3 agents × 2 rounds: gains on arithmetic, GSM8K, MMLU and biographies (66.0→73.8%; others in §4). However, "while debates typically converged into single final answers, these answers were not necessarily correct", and models "confidently affirm" wrong consensus answers.
- **Liang et al. (EMNLP 2024).** Debate counters "degeneration-of-thought", but needs:
  - an adaptive break;
  - only a "modest level" of tit-for-tat;
  - care with judges, since LLM judges can be unfair when the debaters are different LLMs.
- **Khan et al. (2024) and Michael et al. (2023).** Debate beats consultancy for judges who cannot see the source evidence. Notably, as debaters become more skilled, consultancy accuracy *falls* while debate accuracy rises.
- **Role and model diversity.**
  - ChatEval found that "utilizing the same role description … can lead to a degradation in performance".
  - ReConcile beat prior single- and multi-agent baselines by up to 11.4%; its component analysis found that "the diversity originating from different models is critical to its superior performance" [corrected 2026-10-18: the 11.4% is not a diversity effect].

**Sceptical empirics [S].**

- **Smit et al.** Multi-agent debate methods "do not reliably outperform" self-consistency or ensembling, and are sensitive to hyperparameters. The abstract adds that adjusting agent agreement levels "can significantly enhance performance and even surpass all other non-debate protocols we evaluated" [added 2026-10-18].
- **Choi, Zhu & Li (NeurIPS 2025),** across 7 benchmarks:
  - Majority voting delivers most of the gain. For Qwen2.5-7B, average accuracy was 0.769 with voting vs 0.738 with the best debate configuration.
  - Debate induces a martingale over beliefs: "debate alone does not improve expected correctness".
  - Biasing belief updates toward correction helps.
- **Wynn, Satija & Hadfield (2025).**
  - Accuracy can *fall* over rounds, as agents end up "favoring agreement over challenging flawed reasoning".
  - Weaker agents can drag down stronger ones, even when the strong agents are in the majority. The effect is not uniform: some groups with a stronger majority improve (e.g. on GSM8K).

**Failure modes [S].** Sycophancy, partly induced by human preference data (Sharma et al.); answer flipping under challenge, 46% average flip rate and 17% accuracy drop (Laban et al.); overconfidence when confidence is verbalized (Xiong et al.); personas do not improve accuracy, with effects "largely random" across 162 roles and 2,410 questions (Zheng et al. 2024); caricature in persona simulations (Cheng et al.) and flattening of identity groups (Wang et al.); acquiescence bias in LLM forecasts, i.e. mean predictions above 50% despite balanced outcomes (Schoenegger et al.); LLM-judge position, verbosity and self-enhancement biases (Zheng et al. 2023).

**Persuasion [S].**

- Personalized GPT-4 produced an 81.2% relative increase in the odds of higher post-debate agreement compared with human opponents (95% CI +26.0% to +160.7%; N = 900). In pairs where the two sides were not equally persuasive, it was more persuasive 64.4% of the time (Salvi et al., *Nat. Hum. Behav.* 2025) [corrected 2026-10-18: was the arXiv v1 figure, +81.7%].
- Post-training raised persuasiveness by up to 51% and prompting by up to 27%, but both reduced factual accuracy (Hackenburg et al. 2025).

**AI-mediated deliberation [S].**

- The Habermas Machine generated many candidate statements and ranked them with a personalized reward model, aggregating predicted rankings in a simulated election. It was trained to maximize endorsement.
- Its benefits came with a measurable drift toward majority positions. In the authors' words, it "does not have the mediation-relevant capacities of fact-checking, staying on topic, or moderating".
- An LLM-augmented Polis pilot found summarization promising, but its quality was limited by context length (Small et al. 2023).

**Synthesis [I].** Debate earns its keep through two mechanisms: (1) *revealing evidence to a judge*, and (2) *ensembling*. Conformity dynamics that bring no new evidence are neutral or harmful. Two rules follow:

- **Estimates come from independent ensembles.**
- **Debate exists only to surface evidence to the human IC.** An agent may update only when it cites a newly surfaced, validator-checked artifact (an "evidence-gated update"). This puts Choi et al.'s "bias toward correction" into practice without needing an oracle.

### 2.6 Human–AI teaming and automation bias

**Vaccaro, Almaatouq & Malone (2024): meta-analysis of 106 experiments and 370 effect sizes [S].**

| Comparison | Hedges' g |
|---|---|
| Human–AI combinations vs the better of human or AI alone | −0.23 |
| Human–AI combinations vs humans alone | +0.64 |
| Decision tasks only (vs better of the two) | −0.27 |
| When humans outperform the AI alone (vs better of the two) | +0.46 |
| When the AI alone outperforms humans (vs better of the two) [added 2026-10-18] | −0.54 (95% CI −0.71 to −0.37) |

- Losses are concentrated in decision tasks. Gains appear when the humans are better than the AI.
- In their words, "neither of these factors [explanations, confidence displays] significantly affected the performance of human–AI systems".

**Other findings [S].** Explanations increase "the chance that humans will accept the AI's recommendation, regardless of its correctness" (Bansal et al. 2021). Cognitive forcing, e.g. deciding before seeing the AI, reduces overreliance but is liked least (Buçinca et al. 2021). Veterinary radiologists (n = 19) who recorded a provisional decision first were "less likely to agree with the AI regardless of whether the advice is accurate", at no time cost and with no accuracy gain; they also sought a colleague's second opinion less often when they disagreed with the AI (Fogliato et al. 2022) [corrected 2026-10-18: was "Radiologists", with no accuracy result]. LLM assistants improved human forecasting accuracy by 24–28%, and a 12-LLM crowd was statistically indistinguishable from 925 human forecasters (Schoenegger et al. 2024).

**Automation bias.**

- Parasuraman & Manzey (2010) model it as complacency and bias in the use of automation *(verified 2026-10-18, literature check)*. Automation bias affects naive and expert users alike and is not prevented by training or instructions (per a summary of the paper) [added 2026-10-18].
- It is now a regulatory concept [S]. Under EU AI Act Art. 14(4)(b), overseers must remain aware of "the possible tendency of automatically relying or over-relying on the output".
- Art. 14(4)(d–e) requires that overseers can disregard, override or reverse outputs, or stop the system.

### 2.7 Cross-disciplinary transfers used in the design

| Field | Idea transferred | IDM element |
|---|---|---|
| Operations research / decision analysis | Decision conferencing (Phillips 2007, nr); value of information; break-even analysis | Live what-if console; VOI-ranked cruxes; decision-flip thresholds |
| Control theory | Event-triggered control; state observers | Signposts re-open decisions when indicators cross flip thresholds |
| Actuarial science | Bühlmann credibility | Track-record shrinkage weights |
| Bank model risk (SR 11-7) | Effective challenge = incentives + competence + influence | Validator seat with publication veto; IDM treated as a model |
| Intelligence analysis (ICD 203) | Probability bands, alternatives, indicators, explaining changes | House analytic standard; minority reports |
| Central banking | Recorded votes, dissents, projection distributions; transparency trade-offs | IC "dot plot" after blind submission; structured records |
| Public finance [P] | Independent fiscal institutions separate forecasts from decisions | "Tools own numbers; IC owns decisions" |
| Machine learning | Ensembles, debate, calibration, online learning (Hedge) | Shadow-IC; scoring; display weights |
| Real options | Value of waiting under irreversibility | DEFER rule (EVSI > $c_{\text{delay}}$) |

---

## 3. Methods and models, and their trade-offs

| Design choice | Option A | Option B | Evidence-based default [I] |
|---|---|---|---|
| Agent aggregation | Debate to consensus | Independent ensemble + vote/pool | Ensemble for *estimates* (Choi; Smit). Debate only to surface evidence on cruxes, at most 2 rounds (Du; Liang's adaptive break; Wynn's degradation finding) |
| Role of AI | Participant / voter | Facilitator and evidence-surfacer | Facilitator + challenger. No AI vote counts in the IC ballot (decision tasks show g < 0) |
| Agent diversity | Demographic or personality personas | Mandate + evidence slice + loss function + model family | Mandates and evidence partitions; ≥ 3 model families; ≤ 40% of seats on any one family (ReConcile; ChatEval; persona null results; caricature risk) |
| Ordering | AI memo first | Human pre-vote first | Human pre-vote before AI *conclusions*. The neutral fact pack and model outputs may come first (Fogliato, for reduced anchoring on AI output, not better decisions; Buçinca) |
| Structured conflict | Devil's advocate | Dialectical inquiry | A standing red-team seat (DA), which Schwenk supports. DI only on cruxes with explicit rival assumption sets [I]: Schwenk did not show DI beating the expert approach on relatively ill-structured tasks [corrected 2026-10-18: was "Both: a standing red-team seat (DA) and DI on the top cruxes (Schwenk)"] |
| Record | Verbatim transcript | Structured positions + rationale + dissent | Structured record by default; transcripts restricted [I] (Meade & Stasavage). Hansen et al. show a discipline-vs-conformity trade-off, with discipline dominating on their influence measure, so they do not by themselves support restriction [corrected 2026-10-18: Hansen et al. were cited in support of restriction] |
| Aggregation target | Conclusions (votes) | Premises (views → optimizer) | Both, with a discursive-dilemma flag (List & Pettit) |
| Weighting | Equal | Track-record weights | Equal until $n_k\ge30$ resolved forecasts, then credibility/Hedge weights for *display only*. Votes stay one member, one vote |
| Mediation objective | Maximize endorsement | Accuracy + coverage of dissent | Accuracy and coverage. Never endorsement or persuasion (Habermas majority drift; Hackenburg accuracy loss) |
| What-if engine | Full re-simulation per question | Entropy-pooling re-weighting | Entropy pooling (EP) for live use; re-simulate when the effective number of scenarios collapses (§6.5) |
| Robust rule | Pooled-belief optimum | Max-min / minimax-regret over member beliefs | Show all three. Recommend the robust rule for irreversible actions |

**Key trade-offs [I].** *Diversity vs coherence:* heterogeneous seats surface more information but add noise, which pooling and evidence gating absorb. *Anonymity vs accountability:* anonymous reveal fights anchoring; named ballots keep accountability. *Speed vs depth:* debate is capped at 3 cruxes; the rest is pooled or deferred with diligence. *Consensus vs dissent:* the IDM seeks a well-understood decision with explicit dissent, not consensus.

---

## 4. Empirical evidence and current data (dated, sourced)

| # | Finding | Value | Source (as of) |
|---|---|---|---|
| 1 | AI-mediated group statements vs trained human mediators | Preferred 56% vs 44% (one experiment: 75 six-person groups, n = 439; N = 5,734 is the whole programme) [corrected 2026-10-18]. Group agreement rose ≈ 8 pp. Unanimous groups rose from 22.8% to 38.6% (cohort 1). Initial majority grew in 29–32% of rounds vs minority in 20–26%. No fact-checking capacity | Tessler et al., *Science* 386, 18 Oct 2024 |
| 2 | Multi-agent debate (3 agents, 2 rounds) | Arithmetic 67.0→81.8%; GSM8K 77.0→85.0%; MMLU 63.9→71.1% | Du et al., ICML 2024 |
| 3 | Majority vote vs debate | Qwen2.5-7B average: single 0.721, vote 0.769, best debate 0.738. Llama-3.1-8B: 0.620 / 0.724 / 0.699 | Choi et al., NeurIPS 2025 |
| 4 | LLM answer flipping when challenged | 46% average flip rate; −17% accuracy; fine-tuning reduced the deterioration by 60% | Laban et al., arXiv (v2 Feb 2024) |
| 5 | Debate vs consultancy, human judges | 84% vs 74%; debates were 68% of the length of consultancies | Michael et al., Nov 2023 |
| 6 | Debate with non-expert judges | Model judges 76% vs 48%; human judges 88% vs 60%, each against naive (no-debate) baselines. Consultancy gave 54% (model judges) and 78% (human judges) | Khan et al., ICML 2024 |
| 7 | Human–AI vs best single agent | g = −0.23 overall; −0.27 on decision tasks; +0.64 vs humans alone | Vaccaro et al., *Nat. Hum. Behav.*, 28 Oct 2024 |
| 8 | Persuasion vs accuracy | N = 76,977; 19 LLMs; 466,769 claims fact-checked. Post-training up to +51% persuasion, prompting up to +27%, with accuracy falling where persuasion rose | Hackenburg et al., *Science* 390(6777):eaea3884, 4 Dec 2025 (preprint Jul 2025) |
| 9 | Personalized LLM persuasion | +81.2% relative odds of higher post-debate agreement vs human opponents (95% CI +26.0% to +160.7%; N = 900); more persuasive 64.4% of the time in pairs that were not equally persuasive [corrected 2026-10-18: was the arXiv v1 figure, +81.7%, N = 820] | Salvi et al., *Nat. Hum. Behav.* 9(8), online 19 May 2025 (preprint arXiv v1, Mar 2024) |
| 10 | LLM help for human forecasters | +24–28% accuracy (N = 991). A 12-LLM crowd was not statistically different from 925 human forecasters | Schoenegger et al., 2024 |
| 11 | Persona prompting | No improvement across 162 roles and 2,410 questions | Zheng et al., Findings of EMNLP 2024 |
| 12 | Transparency and FOMC deliberation | Discipline effect dominates conformity effect (on the authors' influence measure) | Hansen, McMahon & Prat, *QJE* 133(2), 2018 |
| 13 | Committees vs individuals | Groups make better decisions with no significant extra delay; majority rule and unanimity equally fast | Blinder & Morgan, NBER WP 7909 (2000); peer-reviewed version *JMCB* 37(5), 2005 |
| 14 | AI adoption in UK finance | 75% of firms use AI and a further 10% plan to. Foundation models are 17% of use cases. 55% of use cases involve some automated decision-making (24% semi-autonomous, 2% fully autonomous). 118 respondents | Bank of England / FCA, 21 Nov 2024 |
| 15 | AI adoption at a sovereign fund (vendor-reported) | NBIM: >20% of weekly time saved on AI-assisted tasks; 600+ Claude users within two months | claude.com/customers/nbim (accessed 2026-10-18) |
| 16 | Agentic-research orchestration | AI-reviewer vs performance correlation r = 0.44. Rubric gates failed to flag runs that altered their own evaluation; a manual audit caught them. Verification is "only as complete as its task-specific evaluators and rubrics" | Lange et al., arXiv:2610.18933, 13 Oct 2026 |
| 17 | EU AI Act high-risk timetable (a benchmark for ADIC, not binding) | Annex III obligations from 2 Dec 2027; Annex I from 2 Aug 2028 | artificialintelligenceact.eu (accessed 2026-10-18) |
| 18 | Open-source entropy-pooling tooling | fortitudo.tech 1.2.5 (20 Aug 2026), GPL-3.0-or-later | PyPI (accessed 2026-10-18) |

**Reading the evidence [I].**

- Nearly all of this evidence comes from tasks with ground truth and fast feedback. IC decisions are high-stakes, few in number, long-horizon and partly value-laden.
- What transfers is mechanisms, not effect sizes:
  - independence preserves information;
  - adversarial structure helps judges who lack the evidence;
  - consensus pressure without evidence destroys information;
  - fluency and explanation inflate trust;
  - the order in which people see information matters.

---

## 5. Practitioner and peer practice; case studies

### Norway: owner–manager split [S]

- The Storting sets the legal frame.
- The Ministry of Finance issues the management mandate and appointed the independent Council on Ethics.
- Norges Bank's Executive Board delegates operational management to NBIM.
- The CEO "has the overall responsibility for implementing requirements defined by the Excecutive Board" [sic] and delegates investment mandates to the leader group.

*Lesson [I].* Strategy-level choices sit with the owner. ADIC's distribution policy (5–10%) and leverage ceiling are the analogues of those strategy-level choices. They should be *escalation* items with an IC recommendation, not IC decisions.

### NZ Super: Board vs management IC [S]

- The Board retains investment policy, total-fund risk, strategy approval and certain manager approvals.
- The management Investment Committee consists of:
  - the co-CIOs, as co-chairs;
  - the CRO;
  - the Head of Asset Allocation;
  - the CEO, ex officio;
  - **two invited members co-opted for expertise relevant to each meeting's proposals**.
- The IC considers the liquidity profile, new investments and manager appointments, exclusions, and new opportunities, including opportunity-level risk budgets.
- Strategic tilting is contrarian and is sized by deviation from fair value, risk and *confidence*. The IC oversees it within ranges and maximum positions that the Board reviews.

*Lessons [I].*

- Per-meeting expert seats map naturally onto AI seats whose evidence slices change with the agenda.
- Confidence-scaled sizing is a precedent for feeding elicited confidence into decisions.

### CPP Investments and Future Fund

Both are TPA practitioners. Their Boards set risk appetite and reference or strategic portfolios, and delegate implementation to management committees *(nr this session; the websites did not render or blocked fetching)*.

### Central banks [P]

- Monetary-policy committees publish votes and minutes that record dissent.
- They also publish projection distributions: Bank of England fan charts, and FOMC "dot plots".
- *Template for ADIC [I]:* an IC "dot plot" of members' P(10%), P(floor breach) and preferred action, shown only *after* blind submission.

### Intelligence analysis [S]

- ICD 203 requires that analysts:
  - explain uncertainty;
  - name indicators;
  - analyze alternatives, "particularly important … when low probability events could produce high-impact results";
  - fully consider significant differences in judgment and bring them "to the attention of customers".
- This is the closest institutional template for a minority report.

### Bank model risk: SR 11-7 (4 Apr 2011) [S]

- "Effective challenge" is "critical analysis by objective, informed parties who can identify model limitations". It "depends on a combination of incentives, competence, and influence".
- The guidance warns that "simply picking an extreme point on a given modeled distribution may not be conservative" if the model is misspecified.
- The Validator seat is built to meet all three conditions: separation from development (incentives), technical skill (competence), and a publication veto (influence).
- The IDM itself should be inventoried and validated as a model [I].

### Other precedents

- **Decision conferencing** (Phillips 2007) *(nr)*: facilitated workshops with on-the-spot modelling, the ancestor of the live what-if console [I].
- **Practitioner anecdotes [P]:** Bridgewater's believability weighting (Dalio 2017) and narrative pre-read memos show the promise of track-record weighting and also its risk of hardening into status hierarchy; IDM weights inform the display only.
- **LLM "investment committees" [S]:** TradingAgents simulates analysts, bull/bear researchers, traders and a risk team; its claims rest on backtests, with no evidence yet on real IC decision quality.

### Agentic science: Sakana [S]

- Lessons for the IDM:
  - stage-wise rubric gates enforced by a meta-controller;
  - a claim-to-source map;
  - an audit agent that checks reported numbers against canonical data;
  - reviewers drawn from several model families.
- The authors stress two cautions:
  - an LLM auditor detected flaws far more reliably "from logs and code than from the paper alone";
  - verified results "should therefore still be inspected and validated by human researchers".
- The human role shifts toward "specifying the research contract".
- *IC analogue [I]:* the IC specifies the **decision contract** (objective, constraints, questions) and audits the result.

---

## 6. Design implications for ADIC: the IC Deliberation Module (IDM)

### 6.1 Principles [I]

1. Deterministic tools own numbers. Agents own evidence surfacing and challenge. Humans own decisions. Values are owned at the correct governance level.
2. Aggregate beliefs, not verdicts, and show the verdicts too.
3. Independence comes before interaction, and interaction is evidence-gated.
4. Dissent is a first-class, immutable artifact.
5. Everything forecastable is registered and scored.

This extends the deck v8 motto ("LLMs accelerate evidence; deterministic models own numbers; humans own decisions") with *process hygiene*.

### 6.2 Decision-rights matrix and escalation (defaults [I], NAV ≈ $177bn)

**Tier A: full IC plus shadow-IC.**

- *Triggers (any one):*
  - a single action ≥ 0.25% of NAV (≈ $0.44bn);
  - any secondary SELL at a discount > 10% to NAV;
  - a REFINANCE or LEVER that raises a sleeve's look-through LTV by > 5 pp, or portfolio leverage by > 1 pp;
  - a change to the tail-hedge budget > 10 bp of NAV p.a.;
  - any change to the opportunistic overlay's risk limit.
- *Process:* S0–S7 and H0–H6.
- *Approval:* simple majority, but a ⅔ supermajority for irreversible actions (reversibility > 3 years, or exit cost > 3%).

**Tier B: two-key.**

- *Triggers:* below Tier A but above desk mandates; intra-period re-strikes of the overlay.
- *Process:* a light shadow-IC (S1 + S5 only).
- *Approval:* CIO + CRO ("four-eyes").

**Tier C: within mandate.**

- *Triggers:* actions within approved mandates.
- *Process:* ledger entry only.
- *Approval:* the desk.

**Escalation to the Board or owner.**

- *Triggers (any one):*
  - the Tier-1 gate is amber or red;
  - P50 liquidity survival falls below 24 months;
  - a recommendation on the distribution rate;
  - leverage outside the policy band;
  - the belief/value decomposition (§6.5c) shows a *value* (risk-appetite) split.
- *Process:* IC recommendation plus minority report.
- *Approval:* the Board.

### 6.3 Shadow-IC seats

Each seat is defined by its mandate, evidence scope, loss function, tools and model family. There are **no** demographic or personality personas.

| Seat | Mandate / loss emphasis | Evidence slice | Notes |
|---|---|---|---|
| Facilitator (non-substantive) | Runs the protocol, timeboxes, ensures coverage, drafts the neutral synthesis | All artifacts, read-only | May not introduce claims or numbers |
| Fiduciary & Distribution Steward | Owner's 5–10% distribution; heavy penalties on floor breach and liquidity shortfall | Liquidity engine; distribution policy | Speaks for Tier 1 |
| Private-Markets Underwriter | Drift between underwritten, actual and forecast returns; exit paths; GP quality | Asset table; memo corpus; GP reports | Reference class required |
| Capital-Structure & Financing | REFINANCE / LEVER: NAV loans, subscription lines, continuation vehicles, preferred equity; covenant and margin-spiral risk | Facility terms; LTV paths | Typical holder of unique information |
| Tail-Hedge Strategist | Convexity per unit of carry; monetization rules; basis risk; collateral | Overlay engine; option surfaces | |
| Opportunistic-Trading PM | Evidence of alpha vs beta; capacity; correlation in stress | Strategy P&L; risk reports | Must show skill evidence |
| Outside-View Forecaster | Base rates and calibration; owns the probability table | Reference-class database | Superforecasting-style procedure |
| Risk & Model Validator | SR 11-7 effective challenge; provenance; misspecification | Run logs, code, data lineage | **Can block publication**; runs on a different model family from the proposing seats |
| Red Team | Strongest case against; ACH; failure analogues | Post-mortems; failure corpus | Assigned dissent |

Seats run on ≥ 3 model families. Each family may hold at most 40% of the substantive seats.

### 6.4 Protocol and meeting flow

**Shadow-IC stages (T = meeting day).**

**S0 – Frame (T−10).** The decision contract contains:

- the question and the alternatives, always including the status quo and DEFER;
- the Tier-1 constraints;
- the run_id(s);
- a key-assumptions register;
- 8–15 resolvable elicitation questions $\mathcal Q$, binary or quantile, with at least half resolving within 12 months;
- 6–8 MAP dimensions, for example:
  - underwriting drift (actual vs underwritten);
  - credibility of the strategy group's forecast vs the reference class;
  - liquidity impact;
  - financing risk;
  - reversibility;
  - Tier-1 impact;
  - governance and reputation.

**S1 – Independent assessment (T−7).** There is no cross-visibility between seats. Each seat produces:

- MAP percentiles;
- probabilities for $\mathcal Q$;
- a preferred action for each asset in scope;
- its top-3 evidence artifacts;
- "what would change my mind".

*Rubric gate:* every number must be either a tool output or a labelled judgment anchored to a base rate.

**S2 – Reveal and map (T−5).**

- pooled estimates and their dispersion;
- the member-to-decision map (§6.5);
- cruxes ranked by EVPI;
- the discursive-dilemma check.

**S3 – Evidence-gated debate (T−4).**

- Dialectical inquiry on at most 3 cruxes, each limited to 2 rounds. Per §3, use DI only where a crux has explicit rival assumption sets, and DA otherwise [corrected 2026-10-18: Schwenk 1990 does not show DI beating the expert approach on ill-structured questions].
- A seat may move a probability by more than 5 pp only by citing a newly surfaced, validator-checked artifact. Otherwise the change is reverted and logged.
- Both the pre-debate and post-debate pools are reported, and divergence between them is flagged.

**S4 – Pre-mortem and ACH (T−3).**

- The prompt is: "It is October 2029 and this decision failed."
- Seats write failure narratives independently.
- The narratives are clustered into failure modes. Each failure mode becomes 3–6 signposts, each with an indicator, threshold, owner and review date.
- An ACH matrix tests the key structural hypothesis, e.g. *the DPI decline is cyclical vs structural*.

**S5 – Minority reports (T−2).**

- Triggered when $|p_k-\bar p|\ge\delta_p$ on any key question, or when $a^*_k\neq a_c$ with $R_k(a_c)\ge\delta_U$.
- Reports are append-only and hashed.

**S6 – Questions for the human IC (T−2).** Ranked by EVPI and by the distance to each decision-flip threshold.

**S7 – Package (T−2).** A memo of at most 6 pages containing:

- a claims table with provenance;
- the probability table;
- the options and their Tier-1 status;
- the dissents;
- the signposts;
- an AI track-record panel.

**Human-IC flow.**

**H0 – Blind pre-vote.**

- Members submit their $\mathcal Q$ probabilities, MAP scores and a provisional action.
- They have the neutral fact pack and the model outputs, but not the shadow-IC conclusions.
- Submissions lock on submit.

**H1 – Reveal.** Material is shown in this order:

1. the anonymized dispersion of human views;
2. the model baseline;
3. the shadow-IC map;
4. the minority reports.

**H2 – Discussion of cruxes,** using the live console (§6.6).

**H3 – Human pre-mortem,** led by a rotating human devil's advocate.

**H4 – Simultaneous ballot.**

- Options: approve / resize / defer / reject.
- Each ballot also carries probabilities, a one-line rationale and "what would change my mind".
- A Janis-style second-chance check is held before the decision becomes final.

**H5 – Minutes.**

- The AI drafts the minutes, with every number linked to its source.
- The secretary approves them.
- Dissent is recorded verbatim, with attribution at the member's option.

**H6 – Close the loop.**

- Signposts go to monitoring.
- Questions go to the forecast registry.
- Decisions are re-opened when signposts are triggered.

### 6.5 Formal core

**(a) View conditioning by entropy pooling (Meucci 2008).**

The 50k-path engine supplies prior path weights $p\in\Delta^N$, with $p_s=1/N$. A member's views are linear in $q$: expectations, probabilities, rankings or regime probabilities, written $Aq\le b,\;Cq=d$. The posterior is

$$q^*=\arg\min_{q\in\Delta^N}\sum_sq_s\ln\frac{q_s}{p_s}\quad\text{s.t.}\quad Aq\le b,\;Cq=d\;\;\Longrightarrow\;\;q^*_s\propto p_s\,e^{-\lambda^\top g(x_s)},$$

where $\lambda$ solves the $m$-dimensional concave dual

$$\max_{\lambda_A\ge0,\lambda_C}\;-\ln\sum_sp_se^{-\lambda^\top g_s}-\lambda^\top h .$$

Confidence pooling blends the posterior with the prior: $q_k=(1-c_k)p+c_kq^*_k$.

*Example.* "PE distributions over Y1–Y2 will be 30% below base, confidence 0.6" becomes

$$\mathbb E_q[D^{PE}_{1:2}]=0.7\,\mathbb E_p[D^{PE}_{1:2}],\qquad c=0.6 .$$

The LLM proposes this translation. The member confirms a plain-language back-translation and the formula. The engine then solves.

**How extreme is a view?**

- Effective number of scenarios: $\text{ENS}=\exp(-\sum_sq_s\ln q_s)$.
- Under a uniform prior, $\text{ENS}/N=e^{-\mathrm{KL}(q\Vert p)}$.
- **Amber flag:** ENS/N < 0.30, i.e. KL > 1.20 nats.
- **Red flag:** ENS/N < 0.10, i.e. KL > 2.30 nats, equivalent to conditioning on a 10% tail. A red flag forces re-simulation with a tilted sampler.

**How precise is the estimate?**

- Monte Carlo error uses the Kish effective sample size, $n_{\text{eff}}=1/\sum_sq_s^2$, so that

$$\text{SE}(\hat P)\approx\sqrt{\hat P(1-\hat P)/n_{\text{eff}}}.$$

- For P(10%) ≈ 0.5, the SE is about 0.22 pp at $n_{\text{eff}}$ = 50,000, but 0.71 pp at 5,000.
- The console greys out differences smaller than 2 SE.

**(b) Implied decisions.**

$$a^*_k=\arg\max_{a\in\mathcal A_{T1}}J(a;q_k)$$

- $J$ is the Tier-2 objective, e.g. $P_q(\bar R_5\ge10\%)$ net of shadow costs, or a certainty-equivalent (CE) return.
- $\mathcal A_{T1}$ is the set of actions that are Tier-1 feasible under the framework's ambiguity set.
- A member's beliefs join that ambiguity set only if $\mathrm{KL}(q_k\Vert p)\le\eta_{\max}$. More extreme views must bring evidence.

**(c) Disagreement metrics.**

- **Belief dispersion:** $\sigma_j=\operatorname{sd}_k(p_{k,j})$.
- **Decision-relevant disagreement:** $\text{DRD}=\sum_kw_kR_k(a_c)$, in bp of CE return or pp of P(10%). If dispersion is high but DRD is low, the disagreement does not matter for the decision and the committee can move on.
- **Belief vs value decomposition.** For member $k$ against the committee median $(q_m,\theta_m)$, where $\theta$ denotes shadow prices and penalty weights:
  - compute the 2×2 counterfactuals $a^*(q,\theta)$ for $q\in\{q_k,q_m\}$ and $\theta\in\{\theta_k,\theta_m\}$;
  - attribute the regret gap between beliefs and values with a two-factor Shapley split.
  - A belief split leads to diligence and VOI analysis. A value split leads to escalation.
- **Crux sensitivity.**
  - Exact Shapley over $m\le10$ view components (requiring $2^m$ EP + optimizer runs); or
  - the one-at-a-time flip value $v_j^{\dagger}$ at which $a^*$ changes.

**(d) SELL / HOLD / REFINANCE / LEVER break-evens shown in the console.**

Let

$$V_i^H(q)=\mathbb E_q\Big[\sum_t(D_{i,t}-C_{i,t})(1+r^*)^{-t}\Big],$$

and let $\mu_L$ be the Tier-1 liquidity dual, i.e. the value of $1 of cash today.

- **SELL vs HOLD.** SELL beats HOLD iff $(1-d)(1+\mu_L)\mathrm{NAV}_i>V_i^H(q)+\kappa_i$. The break-even discount is

$$d^{\dagger}_i=1-\frac{V^H_i(q)+\kappa_i}{(1+\mu_L)\,\mathrm{NAV}_i}.$$

  Scarce liquidity (high $\mu_L$) *raises* the discount the fund can rationally accept.
- **REFINANCE.** For a NAV facility of size $B$ at spread $s$:

$$\text{value}\approx\mu_LB-\mathrm{PV}_q(\text{interest}+\text{fees})-P_q(\mathrm{LTV}_t>\bar\ell)\,L_{\text{breach}},$$

  which yields a break-even spread $s^{\dagger}$.
- **LEVER.** Adding exposure $\beta$ at cost $c$:

$$\Delta J\approx\beta\,\mathbb E_q[r-c]-\lambda_{DD}\,\Delta\mathrm{CVaR}_q-\mu_M\,\mathbb E_q[\text{margin}].$$

The IC debates $q$ (empirical) separately from $\mu_L$ and $\lambda_{DD}$ (policy).

**(e) Committee recommendation and DEFER.**

- Report $a^{\text{MM}}$, $a^{\text{MR}}$, the pooled-belief optimum $a^{\text{pool}}$ and the ballot outcome. Flag any disagreement between them.
- DEFER is recommended iff $\text{EVSI}>c_{\text{delay}}$.
- EVSI is computed *preposteriorly on the same paths*:
  1. bin the paths by the signal that will be observable at the next meeting (e.g. next-quarter distributions, secondary bids);
  2. re-optimize within each bin;
  3. average across bins.

**(f) Signposts as event-triggered control.**

- Each signpost's threshold sits at the indicator value where $a^*$ flips, minus a margin (default: 0.5 sd of indicator noise).
- Crossing the threshold re-opens the decision. This replaces calendar-only reviews, with the signpost acting as an observer of the decision's state.

**(g) Learning loop.**

- **Brier score** $\text{BS}=\tfrac1N\sum(f_i-o_i)^2$, with the Murphy decomposition $\text{BS}=\text{REL}-\text{RES}+\text{UNC}$.
- **Log score.**
- **Skill against the model baseline:** $\text{BSS}=1-\text{BS}/\text{BS}_{\text{model}}$. This is the judgmental value-add, i.e. the value of overriding the model.
- **Display weights** follow the Hedge update $w_{k,t+1}\propto w_{k,t}e^{-\eta\ell_{k,t}}$, shrunk by $Z_k$, with a floor of 0.05.
- **Minority-report hit rate:** the share of dissents later vindicated. It measures whether dissent carries information.

### 6.6 Console: Q&A, what-if and uncertainty communication

**Artifact-grounded Q&A.**

- Answers draw only on run artifacts and tool calls. New quantities, such as "P(floor breach) without the overlay", trigger an engine run.
- Every answer cites run_id:artifact:path.
- Each statement is labelled as *model output*, *agent judgment* or *assumption*, following ICD 203 Standard 3.
- If the answer is not in the artifacts, the agent says so.

**What-if.**

- Members type a view in natural language.
- The system shows the formal constraint, a back-translation, KL/ENS flags, and the updated P(10%), P(floor breach), liquidity survival and implied asset actions, with ±2 SE bands.
- Every view is written to the view ledger under the member's name.

**Uncertainty displays** *(design guidance; sources partly nr)*:

- Frequency framing, e.g. "in 546 of 1,000 simulated futures…" (Gigerenzer & Hoffrage 1995).
- Fan charts with 50/80/95% bands (Bank of England practice).
- Quantile dotplots for 5-year return distributions (Kay et al. 2016).
- Overlays showing the model's state-confidence.
- Explanations draw on:
  - Shapley attribution (as in deck v8);
  - binding constraints and their shadow prices;
  - counterfactual flip thresholds.

**Disagreement map.** A matrix of members by key questions (shown after the lock), plus each member's implied action, DRD, the belief/value split and the cruxes ranked by VOI.

### 6.7 State variables, decision variables, constraints and objective terms

**State $S_t$:**

- member and agent view vectors and confidences;
- track records ($n_k$, BS, REL, RES);
- the open-decision ledger (actions, signposts, thresholds, owners);
- the dissent ledger;
- the override log (model recommendation vs IC decision, with reason codes);
- the agent registry (model versions, prompt hashes, regression results).

**Decision variables:**

- the IC action on each agenda item: approve, resize to $x$, defer, or reject;
- the asset action: SELL, HOLD, REFI$(B,s)$ or LEVER$(\beta)$;
- diligence assignments that accompany a DEFER;
- signpost thresholds;
- escalation flags.

**Constraints:**

- the decision-rights matrix;
- a quorum of at least ⅔ of voting members;
- recusal for conflicts of interest;
- Tier-1 feasibility;
- a supermajority for irreversible actions;
- provenance coverage of 100% of numeric tokens in AI output;
- a minority report wherever the trigger fires.

**Objective terms that the IDM *exposes* but does not optimize:**

- $J$ and its decomposition;
- DRD;
- EVSI − $c_{\text{delay}}$;
- irreversibility shadow cost;
- the process KPIs (§6.11).

### 6.8 Parameters

All values are defaults [I] unless a source is given.

| Parameter | Default | Rationale / source |
|---|---|---|
| Shadow-IC seats | 9 (7 substantive + facilitator + validator) | Mandate coverage; ChatEval role diversity |
| Model families | ≥ 3; ≤ 40% of seats each | ReConcile model diversity; correlated errors |
| Debate rounds per crux; number of cruxes | 2; ≤ 3 | Du et al. (2 rounds); Liang adaptive break; Wynn degradation |
| Evidence-gated update threshold | 5 pp | Choi's "bias toward correction" |
| Dissent triggers | $\delta_p$ = 15 pp; $\delta_U$ = 10 bp CE, or 3 pp ΔP(10%) | Balances noise against record bloat |
| ENS/KL flags | Amber 0.30 / 1.20 nats; red 0.10 / 2.30 nats | Identity ENS/N = $e^{-\mathrm{KL}}$ |
| Monte Carlo display rule | Show differences > 2 SE (Kish $n_{\text{eff}}$) | Sampling error |
| Credibility constant $K$ | 30 resolved forecasts | Bühlmann; small-sample prudence |
| Hedge η; weight floor | 0.3 per resolution batch; 0.05 | Online-learning practice; preserves diversity |
| Extremizing α | 1.0 (agents ≤ 1.0; humans fitted after ≥ 100 resolutions, capped at 1.5) | Baron et al.; correlated LLM information |
| Probability language | ICD 203 bands | ICD 203 |
| Pre-mortem horizon; signposts | 3 years; 3–6 per decision | Matches the 3-year simulation and 5-year floor |
| Short-fuse questions per meeting | 10–20, ≥ 50% resolving within 12 months | Fast learning signal |
| Seeded-error drills | 1 per Tier-A meeting (programme disclosed, items not) | Automation-bias monitoring |
| Supermajority for irreversible actions | ⅔ | Reversibility asymmetry |
| Calibration targets: unjustified flip rate | < 10% (vs a 46% literature baseline) | Laban et al. |
| Calibration targets: validator seeded-error detection | ≥ 90% | Design target |
| Calibration targets: hidden-profile surfacing | ≥ 80% | Design target |

### 6.9 Data needs

- An immutable **run artifact store**: run_id, scenario-set hash, parameter set, code commit and timestamps, held in Parquet/DuckDB.
- An **asset table** holding underwritten, actual and forecast returns, cash flows and facility terms.
- The 18-year **memo corpus**, including post-mortems.
- **Reference-class datasets**: fund outcomes by strategy and vintage, secondary pricing, NAV-loan terms.
- A **forecast registry**: question, resolution rule and date, forecaster, probability, timestamp, outcome and score.
- **Decision, dissent and override ledgers.**
- A **signpost monitor** with indicator feeds.
- A **member registry**: role, conflicts, track record.
- An **agent registry**: model, version, prompt hash, evaluation results.
- Restricted, optional transcripts.

### 6.10 Safeguards

1. **Numeric provenance.**
   - A validator parses every numeric token in agent output.
   - Each must resolve to a tool output (artifact_id + JSON path) or be a labelled elicited judgment. Otherwise publication is blocked.
   - This follows Sakana's claim-to-source map and audit agent. The validator audits logs and code, not just the memos [S].
2. **Write barriers.** Agents cannot alter model inputs. Views reach the engine only as view objects that a human has confirmed.
3. **Dissent preservation.**
   - Minority reports are append-only, hashed and displayed next to the recommendation.
   - The synthesizer may not paraphrase them.
   - The minutes must reference every dissent.
4. **No persuasion optimization.**
   - Agents are never fine-tuned, selected or rewarded on whether their advice is adopted.
   - Output is never personalized to individual members' profiles.
   - Agents use a plain register, must include the strongest counter-argument, and avoid rhetorical devices.
   - A periodic A/B audit presents the same content in plain vs fluent style (cf. Hackenburg; Salvi).
5. **Anti-sycophancy and anti-conformity.**
   - Agents are blind to the identities and preferences of the chair and CIO.
   - Human views reach agents anonymized, and only after S1.
   - Belief updates are evidence-gated.
   - Regression suites cover "are you sure?" challenges and weak-agent drag.
6. **Automation-bias countermeasures.**
   - Human-first pre-votes, with AI conclusions hidden until the vote locks.
   - Cognitive forcing: a member accepting an AI recommendation must write down one way it could be wrong.
   - The AI track record and calibration are displayed with confidence intervals.
   - Seeded-error drills, which monitor and measure automation bias rather than prevent it: training and instructions do not prevent it (Parasuraman & Manzey 2010) [corrected 2026-10-18: drills were listed as a countermeasure].
   - A per-item kill switch, analogous to EU AI Act Art. 14(4)(e).
7. **Untrusted inputs.**
   - GP and manager documents are treated as data, never as instructions, to defend against prompt injection.
   - Tools are scoped read-only.
   - Confidential deliberation runs on sovereign or on-premises hosting.
8. **Model risk management.**
   - The IDM is inventoried under SR 11-7-style validation, monitoring and change control.
   - Model versions are pinned.
   - A canned-case regression suite runs before every upgrade.
   - Reviewers are drawn from several model families [S: Sakana suggestion].

### 6.11 Evaluating whether it improves decision quality

**Offline.**

- **Historical replay** on the memo corpus:
  - Use strict time-slicing, and anonymize names and dates to limit leakage from pre-training. Add leakage probes.
  - Score shadow-IC probabilities on resolved outcomes, e.g. DPI ≥ 1.0× by year 6, TVPI quartile, distribution timing.
  - Compare against base rates, the original underwriting, a single agent, a voting ensemble and debate. These are Sakana-style baselines and ablations.
- **Hidden-profile suites,** with critical facts partitioned across seats. Target surfacing rate: ≥ 80%.
- **Seeded-error suites.** Target validator detection: ≥ 90%.
- **Sycophancy, flip and diversity checks.** Alert if the pairwise rank correlation of seat outputs exceeds 0.9.

**Shadow mode (6–12 months).** The IDM runs without being shown to the IC, to establish baselines.

**Online experiment.**

- Randomize, at the agenda-item level, whether the shadow-IC memo arrives before or after the human pre-vote.
- Fit a hierarchical Bayesian model (PyMC) and report $P(\beta<0)$:

$$\text{BS}_{iqk}=\alpha+\beta T_i+u_k+v_q+\varepsilon .$$

- *Rough power [I]:* with a per-forecast Brier sd of about 0.2 and 400 independent forecasts per arm, SE(Δ) ≈ 0.014 and the minimum detectable effect is ≈ 0.04. Clustering by question inflates this, so plan for 2 years.

**KPIs.**

- BSS against the model baseline, i.e. the value of overrides.
- Noise index: the mean standard deviation of members' estimates before discussion.
- Surfacing rate.
- Weight-of-advice toward the AI, split by whether the AI was right or wrong (appropriate reliance, cf. Schemmer et al.).
- Dissent rate and minority-report hit rate.
- A six-element Decision Quality rubric, scored blind to outcomes.
- Performance of the anti-portfolio of rejected and deferred items.
- Minutes per decision.

**Success thresholds [I].**

- BSS gain ≥ 0.05.
- Noise reduced by 20% with no loss of resolution.
- No increase in weight-of-advice toward the AI when the AI is wrong.
- Dissent rate not below baseline.

---

## 7. Implementation notes

**Stack.** Entropy pooling: numpy/scipy for the dual (L-BFGS-B on $m\le20$ multipliers, log-sum-exp stabilized) and cvxpy (`rel_entr`, exponential cone) for feasibility and cross-checks. **fortitudo.tech** implements sequential entropy pooling and CVaR optimization but is **GPL-3.0**; review the licence before embedding it in proprietary code. Schemas: pydantic / JSON Schema for view objects, ballots and memos. Storage and provenance: DuckDB/Parquet with sha256 hashes. Scoring: scikit-learn `brier_score_loss`, `calibration_curve`. Evaluation: PyMC or Bambi. Interface: Streamlit, Panel or Dash with plotly fan charts and quantile dotplots. Orchestration: a meta-controller with stage rubrics; any framework works if it supports parallel seats, structured outputs, tool-call logging and per-seat model routing.

**Complexity.**

- The EP dual costs $O(Nm)$ per gradient, i.e. milliseconds at N = 50k and m ≤ 20.
- Re-optimizing decisions for each view set dominates the cost. Mitigations:
  - warm starts;
  - weighted scenario subsampling;
  - precomputed response surfaces to keep interaction latency low.
- Exact Shapley over m = 10 view components needs 1,024 (EP + optimizer) runs. Beyond that, use permutation sampling.
- EVSI with B signal bins needs B re-optimizations.

**Numerical pitfalls.**

- **Inconsistent views** make the dual diverge. Run a Phase-I LP feasibility test first and report the minimal relaxation.
- **Tail views** on 50k paths leave few scenarios, so the effective sample size collapses. Re-simulate with importance tilting.
- **Two different quantities.** Do not confuse ENS (a measure of how extreme a view is) with the Kish ESS (which governs sampling error).
- **Path-dependent quantities** such as drawdown and liquidity survival must be computed per path and then re-weighted. Never re-weight summary statistics.
- **LLM nondeterminism.**
  - Fix temperatures.
  - Log prompts and model versions.
  - Re-run S1 with different seeds to measure noise within each seat.

---

## 8. Risks, pitfalls and limitations

- **External validity.** The evidence comes from laboratory, benchmark and political-deliberation settings. Its effect sizes will not transfer directly to a sovereign IC of 6–12 people.
- **Both automation bias and algorithm aversion.** Human-first ordering reduces *uncritical* agreement with AI, but may also reduce *correct* agreement (Fogliato). Monitor appropriate reliance, not raw agreement.
- **Homogenization.** LLM seats may share blind spots. Diversity across model families helps but does not guarantee independent errors.
- **Consensus drift.** AI mediation can move groups toward majority positions (Habermas). The IDM never optimizes endorsement.
- **Goodhart effects.**
  - Members may game scoring through question selection. Question sets are frozen at S0.
  - Rubric gates check only the criteria they enumerate (Sakana). Mandatory human audit samples cover what the gates miss.
- **Transparency trade-offs.** Verbatim records may chill dissent, while thin records weaken accountability.
- **Responsibility diffusion.** "The model said so" is a risk. Ballots must carry personal rationales.
- **Values disguised as beliefs.** Risk appetite must not be smuggled in through probability debates. The belief/value decomposition (§6.5c) is the guard.
- **Legal and operational exposure.** Confidentiality, discoverability of records, data residency, cost and latency all need attention. Live re-optimization may be too slow for some decisions.

---

## 9. Open questions

1. Who elicits and owns the utility trade-offs (floor-breach aversion, certainty of distributions, leverage tolerance): the IC, the Board or the owner?
2. Can agents be calibrated on private-markets questions that resolve rarely and slowly? Which short-fuse proxy questions are valid?
3. Is anonymous reveal culturally feasible at ADIC, and how does it interact with seniority?
4. Should member beliefs enter the Tier-1 ambiguity set, and if so, with what plausibility bound $\eta_{\max}$? (Cross-link to the robust-optimization stream.)
5. What interaction latency is acceptable, and which decisions require full re-simulation rather than re-weighting?
6. What is the legal status of AI-drafted minority reports and minutes in the sovereign record?
7. How should owner-level preferences be represented without politicizing the shadow-IC?
8. How can outcome leakage from pre-training be prevented when back-testing on historical deals?

---

## 10. References

URLs were accessed 2026-10-18 unless stated otherwise. *(nr)* = not re-verified in this session.

- Bank of England & FCA (2024, 21 Nov). *Artificial intelligence in UK financial services – 2024*. https://www.bankofengland.co.uk/report/2024/artificial-intelligence-in-uk-financial-services-2024
- Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E., Ribeiro, M.T., Weld, D.S. (2021). Does the whole exceed its parts? The effect of AI explanations on complementary team performance. CHI '21. https://arxiv.org/abs/2006.14779
- Baron, J., Mellers, B.A., Tetlock, P.E., Stone, E., Ungar, L.H. (2014). Two reasons to make aggregated probability forecasts more extreme. *Decision Analysis* 11(2):133–145. https://doi.org/10.1287/deca.2014.0293
- Blinder, A.S., Morgan, J. (2000). Are two heads better than one? An experimental analysis of group vs. individual decisionmaking. NBER WP 7909. https://www.nber.org/papers/w7909 . Peer-reviewed version: Blinder, A.S., Morgan, J. (2005). Are two heads better than one? Monetary policy by committee. *Journal of Money, Credit and Banking* 37(5):789–811.
- Brier, G.W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review* 78(1):1–3.
- Britton, E., Fisher, P., Whitley, J. (1998). The Inflation Report projections: understanding the fan chart. *Bank of England Quarterly Bulletin* (Feb). *(nr)*
- Buçinca, Z., Malaya, M.B., Gajos, K.Z. (2021). To trust or to think: cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making. *PACM HCI* (CSCW). https://arxiv.org/abs/2102.09692
- Bühlmann, H. (1967). Experience rating and credibility. *ASTIN Bulletin* 4(3):199–207. https://doi.org/10.1017/S0515036100008989
- Chan, C.-M., Chen, W., Su, Y., Yu, J., Xue, W., Zhang, S., Fu, J., Liu, Z. (2023). ChatEval: Towards better LLM-based evaluators through multi-agent debate. https://arxiv.org/abs/2308.07201
- Chen, J.C.-Y., Saha, S., Bansal, M. (2024). ReConcile: Round-table conference improves reasoning via consensus among diverse LLMs. *Proc. 62nd Annual Meeting of the ACL (Vol. 1: Long Papers)*, pp. 7066–7085. https://doi.org/10.18653/v1/2024.acl-long.381 ; https://arxiv.org/abs/2309.13007
- Cheng, M., Piccardi, T., Yang, D. (2023). CoMPosT: Characterizing and evaluating caricature in LLM simulations. EMNLP 2023. https://arxiv.org/abs/2310.11501
- Choi, H.K., Zhu, X., Li, S. (2025). Debate or vote: Which yields better decisions in multi-agent large language models? NeurIPS 2025. https://arxiv.org/abs/2508.17536
- Clark, G.L., Urwin, R. (2008). Best-practice pension fund governance. *Journal of Asset Management* 9(1):2–21. https://doi.org/10.1057/jam.2008.1 (abstract: https://ideas.repec.org/a/pal/assmgt/v9y2008i1d10.1057_jam.2008.1.html)
- Clemen, R.T., Winkler, R.L. (1999). Combining probability distributions from experts in risk analysis. *Risk Analysis* 19(2):187–203.
- Cooke, R.M. (1991). *Experts in Uncertainty*. Oxford University Press.
- Dalio, R. (2017). *Principles*. Simon & Schuster. (practitioner source)
- Dalkey, N., Helmer, O. (1963). An experimental application of the Delphi method to the use of experts. *Management Science* 9(3):458–467.
- Delbecq, A.L., Van de Ven, A.H. (1971). A group process model for problem identification and program planning. *Journal of Applied Behavioral Science* 7(4):466–492. *(nr)*
- Diehl, M., Stroebe, W. (1987). Productivity loss in brainstorming groups: toward the solution of a riddle. *JPSP* 53(3):497–509.
- Dixit, A.K., Pindyck, R.S. (1994). *Investment under Uncertainty*. Princeton University Press.
- Drew, M.E., Walk, A.N. (2019). *Investment Governance for Fiduciaries*. CFA Institute Research Foundation. https://rpc.cfainstitute.org/research/foundation/2019/investment-governance-for-fiduciaries
- Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., Mordatch, I. (2024). Improving factuality and reasoning in language models through multiagent debate. ICML 2024 (PMLR 235). https://arxiv.org/abs/2305.14325
- European Union (2024). Artificial Intelligence Act, Article 14: Human oversight (and Art. 113 timetable as presented). https://artificialintelligenceact.eu/article/14/
- Federal Reserve Board & OCC (2011, 4 Apr). SR 11-7 Attachment: *Supervisory Guidance on Model Risk Management*. https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107a1.pdf
- Flyvbjerg, B. (2006). From Nobel Prize to project management: getting risks right. *Project Management Journal* 37(3):5–15. *(nr)*
- Fogliato, R., Chappidi, S., Lungren, M., Fisher, P., Wilson, D., Fitzke, M., Parkinson, M., Horvitz, E., Inkpen, K., Nushi, B. (2022). Who goes first? Influences of human-AI workflow on decision making in clinical imaging. *FAccT '22*, pp. 1362–1374. https://doi.org/10.1145/3531146.3533193 ; preprint https://arxiv.org/abs/2205.09696
- Freund, Y., Schapire, R.E. (1997). A decision-theoretic generalization of on-line learning and an application to boosting. *JCSS* 55(1):119–139.
- Genest, C., Zidek, J.V. (1986). Combining probability distributions: a critique and an annotated bibliography. *Statistical Science* 1(1):114–135.
- Gigerenzer, G., Hoffrage, U. (1995). How to improve Bayesian reasoning without instruction: frequency formats. *Psychological Review* 102(4):684–704.
- Gilboa, I., Schmeidler, D. (1989). Maxmin expected utility with non-unique prior. *Journal of Mathematical Economics* 18(2):141–153.
- Hackenburg, K., Tappin, B.M., Hewitt, L., Saunders, E., Black, S., Lin, H., Fist, C., Margetts, H., Rand, D.G., Summerfield, C. (2025). The levers of political persuasion with conversational artificial intelligence. *Science* 390(6777):eaea3884 (4 Dec 2025). https://doi.org/10.1126/science.aea3884 ; preprint, titled "...with conversational AI": https://arxiv.org/abs/2507.13919
- Hansen, S., McMahon, M., Prat, A. (2018). Transparency and deliberation within the FOMC: a computational linguistics approach. *QJE* 133(2):801–870. https://doi.org/10.1093/qje/qjx045
- Hemming, V., Burgman, M.A., Hanea, A.M., McBride, M.F., Wintle, B.C. (2018). A practical guide to structured expert elicitation using the IDEA protocol. *Methods in Ecology and Evolution* 9(1):169–180.
- Heuer, R.J. Jr. (1999). *Psychology of Intelligence Analysis*. CIA Center for the Study of Intelligence.
- Heuer, R.J. Jr., Pherson, R.H. (2010; 3rd ed. 2020). *Structured Analytic Techniques for Intelligence Analysis*. CQ Press. *(nr)*
- Howard, R.A. (1966). Information value theory. *IEEE Transactions on Systems Science and Cybernetics* 2(1):22–26.
- IFSWF / International Working Group of SWFs (2008). *Generally Accepted Principles and Practices ("Santiago Principles")*. https://www.ifswf.org/santiago-principles-landing/santiago-principles ; PDF: https://www.ifswf.org/sites/default/files/santiagoprinciples_0_0.pdf
- Irving, G., Christiano, P., Amodei, D. (2018). AI safety via debate. https://arxiv.org/abs/1805.00899
- Janis, I.L. (1982). *Groupthink: Psychological Studies of Policy Decisions and Fiascoes* (2nd ed.). Houghton Mifflin.
- Kahneman, D., Lovallo, D., Sibony, O. (2019, 4 Mar). A structured approach to strategic decisions. *MIT Sloan Management Review* (Spring 2019 issue; Reprint 60314). https://sloanreview.mit.edu/article/a-structured-approach-to-strategic-decisions/
- Kahneman, D., Rosenfield, A.M., Gandhi, L., Blaser, T. (2016). Noise: How to overcome the high, hidden cost of inconsistent decision making. *Harvard Business Review* (Oct). https://hbr.org/2016/10/noise
- Kahneman, D., Sibony, O., Sunstein, C.R. (2021). *Noise: A Flaw in Human Judgment*. Little, Brown Spark.
- Kay, M., Kola, T., Hullman, J., Munson, S. (2016). When (ish) is my bus? User-centered visualizations of uncertainty in everyday, mobile predictive systems. CHI 2016. *(nr)*
- Khan, A., Hughes, J., Valentine, D., Ruis, L., Sachan, K., Radhakrishnan, A., Grefenstette, E., Bowman, S.R., Rocktäschel, T., Perez, E. (2024). Debating with more persuasive LLMs leads to more truthful answers. ICML 2024. https://arxiv.org/abs/2402.06782 ; https://proceedings.mlr.press/v235/khan24a.html
- Klein, G. (2007). Performing a project premortem. *Harvard Business Review* 85(9). https://hbr.org/2007/09/performing-a-project-premortem
- Laban, P., Murakhovs'ka, L., Xiong, C., Wu, C.-S. (2023). Are you sure? Challenging LLMs leads to performance drops in the FlipFlop experiment. https://arxiv.org/abs/2311.08596
- Lange, R.T., Grillotti, L., Yamada, Y., Charakorn, R., Ha, D. (Sakana AI) (2026, 13 Oct). The Agentic Scientist: Orchestrating coding agents for automated scientific (co-)discovery. arXiv:2610.18933v1. https://arxiv.org/html/2610.18933v1
- Liang, T., He, Z., Jiao, W., Wang, X., Wang, Y., Wang, R., Yang, Y., Shi, S., Tu, Z. (2024). Encouraging divergent thinking in large language models through multi-agent debate. EMNLP 2024. https://arxiv.org/abs/2305.19118
- List, C., Pettit, P. (2002). Aggregating sets of judgments: an impossibility result. *Economics and Philosophy* 18(1):89–110.
- Lorenz, J., Rauhut, H., Schweitzer, F., Helbing, D. (2011). How social influence can undermine the wisdom of crowd effect. *PNAS* 108(22):9020–9025. https://www.pnas.org/doi/10.1073/pnas.1008636108 *(nr)*
- Lovallo, D., Kahneman, D. (2003). Delusions of success: how optimism undermines executives' decisions. *Harvard Business Review* 81(7). *(nr)*
- Lu, L., Yuan, Y.C., McLeod, P.L. (2012). Twenty-five years of hidden profiles in group decision making: a meta-analysis. *Personality and Social Psychology Review* 16(1):54–75. https://doi.org/10.1177/1088868311417243 *(metadata verified 2026-10-18; magnitudes nr)*
- Meade, E.E., Stasavage, D. (2008). Publicity of debate and the incentive to dissent: evidence from the US Federal Reserve. *Economic Journal* 118(528):695–717. *(nr)*
- Mellers, B., Ungar, L., Baron, J., et al. (2014). Psychological strategies for winning a geopolitical forecasting tournament. *Psychological Science* 25(5):1106–1115. *(nr)*
- Meucci, A. (2008). Fully flexible views: theory and practice. *Risk* 21(10):97–102. SSRN 1213325. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1213325 ; arXiv copy: https://arxiv.org/abs/1012.2848
- Michael, J., Mahdi, S., Rein, D., Petty, J., Dirani, J., Padmakumar, V., Bowman, S.R. (2023). Debate helps supervise unreliable experts. https://arxiv.org/abs/2311.08702
- Mitchell, D.J., Russo, J.E., Pennington, N. (1989). Back to the future: temporal perspective in the explanation of events. *Journal of Behavioral Decision Making* 2(1):25–38. *(nr)*
- Murphy, A.H. (1973). A new vector partition of the probability score. *Journal of Applied Meteorology* 12(4):595–600.
- NBIM. Governance structure. https://www.nbim.no/en/organisation/governance-model/
- NBIM customer story (vendor-reported). https://claude.com/customers/nbim
- NZ Super Fund (Guardians of New Zealand Superannuation). How we invest: https://www.nzsuperfund.nz/how-we-invest/ ; Investment Committee: https://www.nzsuperfund.nz/about-the-guardians/management/investment-committee/ ; Delegations: https://www.nzsuperfund.nz/about-the-guardians/governance/delegations/ ; Strategic tilting: https://www.nzsuperfund.nz/how-we-invest/actual-portfolio/how-we-add-value/strategic-tilting/
- ODNI (2015; technical amendment 21 Jan 2022). *Intelligence Community Directive 203: Analytic Standards*. https://archive.dni.gov/files/documents/ICD/ICD-203.pdf
- Parasuraman, R., Manzey, D.H. (2010). Complacency and bias in human use of automation: an attentional integration. *Human Factors* 52(3):381–410. https://doi.org/10.1177/0018720810376055
- Phillips, L.D. (2007). Decision conferencing. In W. Edwards, R.F. Miles, D. von Winterfeldt (eds.), *Advances in Decision Analysis*. Cambridge University Press. *(nr)*
- PyPI (2026). fortitudo.tech 1.2.5. https://pypi.org/project/fortitudo.tech/
- Romer, C.D., Romer, D.H. (2008). The FOMC versus the staff: where can monetary policymakers add value? *American Economic Review* 98(2):230–235. https://www.aeaweb.org/articles?id=10.1257/aer.98.2.230
- Rowe, G., Wright, G. (1999). The Delphi technique as a forecasting tool: issues and analysis. *International Journal of Forecasting* 15(4):353–375. *(nr)*
- Salvi, F., Horta Ribeiro, M., Gallotti, R., West, R. (2025). On the conversational persuasiveness of GPT-4. *Nature Human Behaviour* 9(8):1645–1653 (online 19 May 2025). https://doi.org/10.1038/s41562-025-02194-6 ; preprint "On the conversational persuasiveness of large language models: a randomized controlled trial", arXiv 2403.14380 v1 (21 Mar 2024): https://arxiv.org/abs/2403.14380
- Satopää, V.A., Baron, J., Foster, D.P., Mellers, B.A., Tetlock, P.E., Ungar, L.H. (2014). Combining multiple probability predictions using a simple logit model. *International Journal of Forecasting* 30(2):344–356. *(nr)*
- Schemmer, M., Kühl, N., Benz, C., Bartos, A., Satzger, G. (2023). Appropriate reliance on AI advice: conceptualization and the effect of explanations. *IUI '23*, pp. 410–422. https://doi.org/10.1145/3581641.3584066 ; https://arxiv.org/abs/2302.02187
- Schoenegger, P., Park, P.S., Karger, E., Trott, S., Tetlock, P.E. (2024). AI-augmented predictions: LLM assistants improve human forecasting accuracy. https://arxiv.org/abs/2402.07862
- Schoenegger, P., Tuminauskaite, I., Park, P.S., Tetlock, P.E. (2024). Wisdom of the silicon crowd: LLM ensemble prediction capabilities rival human crowd accuracy. https://arxiv.org/abs/2402.19379
- Schwenk, C.R. (1990). Effects of devil's advocacy and dialectical inquiry on decision making: a meta-analysis. *OBHDP* 47(1):161–176. https://doi.org/10.1016/0749-5978(90)90051-a
- Sharma, M., Tong, M., Korbak, T., et al. (2023). Towards understanding sycophancy in language models. https://arxiv.org/abs/2310.13548
- Small, C.T., Vendrov, I., Durmus, E., Homaei, H., Barry, E., Cornebise, J., Suzman, T., Ganguli, D., Megill, C. (2023). Opportunities and risks of LLMs for scalable deliberation with Polis. https://arxiv.org/abs/2306.11932
- Smit, A., Grinsztajn, N., Duckworth, P., Barrett, T.D., Pretorius, A. (2024). Should we be going MAD? A look at multi-agent debate strategies for LLMs. ICML 2024, PMLR 235:45883–45905. Preprint (2023; author order Smit, Duckworth, Grinsztajn, Barrett, Pretorius): https://arxiv.org/abs/2311.17371
- Spetzler, C., Winter, H., Meyer, J. (2016). *Decision Quality: Value Creation from Better Business Decisions*. Wiley.
- Stasser, G., Titus, W. (1985). Pooling of unshared information in group decision making: biased information sampling during discussion. *JPSP* 48(6):1467–1478. https://doi.org/10.1037/0022-3514.48.6.1467
- Tessler, M.H., Bakker, M.A., Jarrett, D., et al. (2024). AI can help humans find common ground in democratic deliberation. *Science* 386(6719):eadq2852. https://www.science.org/doi/10.1126/science.adq2852
- Tetlock, P.E., Gardner, D. (2015). *Superforecasting: The Art and Science of Prediction*. Crown.
- Tversky, A., Kahneman, D. (1974). Judgment under uncertainty: heuristics and biases. *Science* 185(4157):1124–1131.
- Vaccaro, M., Almaatouq, A., Malone, T. (2024). When combinations of humans and AI are useful: a systematic review and meta-analysis. *Nature Human Behaviour* 8(12):2293–2303. https://doi.org/10.1038/s41562-024-02024-1
- Wang, A., Morgenstern, J., Dickerson, J.P. (2025). Large language models that replace human participants can harmfully misportray and flatten identity groups. *Nature Machine Intelligence* 7(3):400–411 (online 17 Feb 2025). https://doi.org/10.1038/s42256-025-00986-z ; preprint https://arxiv.org/abs/2402.01908
- Wynn, A., Satija, H., Hadfield, G. (2025). Talk isn't always cheap: understanding failure modes in multi-agent debate. ICML 2025 MAS Workshop. https://arxiv.org/abs/2509.05396
- Xiao, Y., Sun, E., Luo, D., Wang, W. (2024). TradingAgents: Multi-agents LLM financial trading framework. https://arxiv.org/abs/2412.20138
- Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., Hooi, B. (2024). Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs. ICLR 2024. https://arxiv.org/abs/2306.13063
- Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. NeurIPS 2023 Datasets & Benchmarks. https://arxiv.org/abs/2306.05685
- Zheng, M., Pei, J., Logeswaran, L., Lee, M., Jurgens, D. (2024). When "A helpful assistant" is not really helpful: personas in system prompts do not improve performances of large language models. Findings of EMNLP 2024. https://arxiv.org/abs/2311.10054

---

## Citation corrections (2026-10-18)

Sources: `research/literature/00_LITERATURE_SYNTHESIS.md` §2 (items 2.4.9, 2.4.10, 2.6.2); `research/literature/14_ic_deliberation.lit.md` §2; `research/literature/recheck/14_ic_deliberation.recheck.md`; `research/literature/recheck/13_paper_deepread.recheck.md` (MAP); `research/literature/recheck/10_scenarios_robustness.recheck.md` (Lange initials); Crossref look-ups of 2026-10-18 (Bühlmann; Wang et al.). The barrier re-run (`research/groups/addenda/G4_barrier_rerun/RESULTS.md`) does not apply: this dossier quotes no barrier statistic.

- §2.3 and §3, Schwenk (1990): "both beat an expert-recommendation baseline" → "DA beat an expert-recommendation baseline. DI's advantage over the expert approach was not demonstrated on relatively ill-structured tasks, and neither DA nor DI beat the other" (synthesis §2.4 item 9). Tag *(nr)* → [S]; DOI added in §10.
- §3 "Structured conflict" default, §2.3 "IDM use" and §6.4 S3: conclusion updated after the Schwenk correction. DI is now used only on cruxes with explicit rival assumption sets, with DA otherwise, tagged [I] (lit file §1 and §5 row 1).
- §1 item 3(iii), §2.6 and §6.10 item 6, Parasuraman & Manzey (2010): seeded-error drills monitor and measure automation bias rather than prevent it, because training and instructions do not prevent it (synthesis §2.4 item 10). Tag *(nr)* → verified; DOI added in §10.
- §1 item 3(ii), Fogliato et al.: "reduces uncritical agreement with AI" → "reduces anchoring on AI output, with no accuracy gain shown".
- §2.6, Fogliato et al.: "Radiologists" → "Veterinary radiologists (n = 19)". Added: no accuracy gain, and fewer second-opinion requests when participants disagreed with the AI.
- §2.3 and §3 "Ordering", Fogliato et al.: now cited for reduced anchoring only, not for better decisions.
- §10, Fogliato et al.: authors reordered to the FAccT '22 proceedings order (Lungren, Fisher, Wilson, Fitzke, Parkinson); pp. 1362–1374 and DOI 10.1145/3531146.3533193 added; arXiv kept as preprint.
- §2.5 and §4 row 9, Salvi et al.: the arXiv v1 figures (+81.7%, N = 820) → the *Nature Human Behaviour* figures: +81.2% relative odds (95% CI +26.0% to +160.7%; N = 900), and more persuasive 64.4% of the time in pairs that were not equally persuasive.
- §10, Salvi et al.: preprint title with a journal attribution → "On the conversational persuasiveness of GPT-4", *Nature Human Behaviour* 9(8):1645–1653, DOI 10.1038/s41562-025-02194-6; arXiv v1 kept as preprint.
- §10 and §4 row 8, Hackenburg et al.: the arXiv preprint → *Science* 390(6777):eaea3884 (4 Dec 2025), retitled "...with conversational artificial intelligence", DOI 10.1126/science.aea3884. Numbers unchanged.
- §2.5, ReConcile: "(gains of up to 11.4%)" next to the diversity quote → the 11.4% is the gain over prior single- and multi-agent baselines, and the diversity quote comes from the component analysis. §10: ACL 2024 Vol. 1, pp. 7066–7085, DOI 10.18653/v1/2024.acl-long.381.
- §1 item 2, Michael et al.: "a single advocate ('consultancy')" → "consultancy, in which a single expert argues for one answer that is correct half of the time".
- §4 row 6, Khan et al.: 48% and 60% labelled as naive (no-debate) baselines; consultancy figures added (54% model judges, 78% human judges).
- §3 "Record", Hansen et al.: no longer cited in support of restricting transcripts; cited for the discipline-vs-conformity trade-off. §2.2 and §4 row 12: noted that "dominates" rests on the authors' influence measure.
- §2.6, Vaccaro et al.: row added for g = −0.54 (95% CI −0.71 to −0.37) when the AI alone outperforms humans. §10: issue 12 and DOI 10.1038/s41562-024-02024-1.
- §2.5, Smit et al.: added the abstract's finding that tuned agreement levels let debate surpass every non-debate protocol tested. §10: ICML 2024, PMLR 235:45883–45905, proceedings author order (Smit, Grinsztajn, Duckworth, Barrett, Pretorius).
- §2.5, Wynn et al.: "Weaker agents drag down stronger ones" → "can drag down", and the effect is noted as not uniform. §10: ICML 2025 MAS Workshop venue added.
- §2.2, Stasser & Titus (1985): tag *(nr)* → verified, and the information-sampling formula's attribution marked [unverified]. §10: DOI 10.1037/0022-3514.48.6.1467.
- §10, Lu, Yuan & McLeod (2012): *(nr)* → metadata verified; magnitudes still *(nr)*.
- §2.4 and §10, Baron et al. (2014): *(nr)* → verified; DOI 10.1287/deca.2014.0293 added. §2.4, List & Pettit (2002): *(nr)* → verified.
- §2.2 and §2.3, Kahneman, Lovallo & Sibony (2019): MAP caveat narrowed. The core steps are confirmed by a secondary summary; percentile scoring is still unverified (paywall). §10: Spring 2019 issue, Reprint 60314.
- §1 item 2 and §4 row 1, Tessler et al.: the 56% vs 44% preference was attached to the programme N = 5,734 → one experiment, 75 six-person groups, n = 439 (companion verification F1, flagged in the lit file §2.1 item 3).
- §10, Wang, Morgenstern & Dickerson: Crossref confirms *Nature Machine Intelligence* 7(3):400–411 (online 17 Feb 2025), DOI 10.1038/s42256-025-00986-z, so the journal version is cited, with arXiv 2402.01908 as preprint (resolves synthesis §2.4 item 10, which lacked this confirmation).
- §10, Bühlmann (1967): DOI 10.1017/S0515036100008989 added. Crossref confirms it is 4(3):199–207; 10.1017/S0515036100008023 is a 1969 paper with the same title, 5(2):157–165 (synthesis §2.6 item 2).
- §10, hygiene: Schemmer et al. IUI '23 pp. 410–422 and DOI 10.1145/3581641.3584066 added; Blinder & Morgan's peer-reviewed version (*JMCB* 37(5):789–811, 2005) added, also in §4 row 13; Meucci (2008) arXiv 1012.2848 added; Lange et al. author initials added.
- Not changed here: companion-verification corrections that the literature audit did not carry (A1 Luo et al. attribution, A5 BoE/FCA bases, A10 EU AI Act dates, R1–R17), and the Tessler majority-drift nuance, which the lit file calls "a nuance, not an error".
