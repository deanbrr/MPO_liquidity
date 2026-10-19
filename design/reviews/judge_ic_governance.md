# Judge report: IC usability and governance

**Panel role:** IC usability and governance judge. **Date:** 2026-10-18.
**Proposals judged:** PA (quant rigor first), PB (agentic laboratory first), PC (IC decision room first), PD (pragmatic production path), PE (the user's blueprint, judged on its ideas, not its format).

**Read for this review.**
- All five proposals, in full.
- `design/00_DESIGN_BRIEF.md`; `inputs/00_CONTEXT_AND_PRIOR_WORK.md`.
- `research/00_SYNTHESIS.md` v1.1: §0–1 in full, plus §2, §3 (L1–L16), §4.3–4.5, §4.7–4.12, §5, §6, §9 and §10.
- `research/groups/01_GROUPS_SYNTHESIS.md` §0–2.1, §4, §5 and §7; groups addenda gap_01 (all), gap_02 (§0, §3, §5) and gap_03 (§1–4).
- `research/addenda/gap_01.md` §6–7.
- `research/verification/13_paper_deepread.localcheck.md` (all).
- `research/literature/14_ic_deliberation.lit.md` §1 and §4–5.

**Citation keys.** SYN = 00_SYNTHESIS; GROUPS = 01_GROUPS_SYNTHESIS; "groups gap_0k" = `research/groups/addenda/gap_0k.md`; "gap_0k" = `research/addenda/gap_0k.md`; LC = the local paper check; LIT14 = the stream-14 literature check; BP = the user blueprint (PE). "PC §6.5" means section 6.5 of proposal PC.

> **SYNTHETIC.** Every ADIC balance, probability, price, survival horizon or cost quoted below comes from the synthetic working book (context §1A, census v1.0) or research prototypes. None of it is ADIC data.

---

## 0. Verdict in brief

| Rank | Proposal | Overall (1–10) | One-line verdict |
|---|---|---|---|
| 1 | **PC** IC decision room | **8.5** | The only proposal that designs the committee as an institution: who decides what and when, what each person sees, how dissent and credibility are handled, and how Corporate Finance and the owner plug in. Its evidence-plane integrity is thinner than PB's. |
| 2 | **PB** Agentic laboratory | 6.6 | Best integrity engineering and the best claim-rendering discipline. But it is lab-centric: no path for event decisions or group-head proposals, LLM seat views are pooled, and an agent-searchable `payout_topup` slot contradicts the owner-set distribution. |
| 3 | **PD** Pragmatic production | 6.5 | The most research-faithful group economics: RECOVERY delivery shares, ex-ante tail credit, the spare-lever KKT cap. Clean P1 hygiene. The IC layer is a competent restatement with no decision rights, no Board path and thin deliberation design. |
| 4 | **PA** Quant rigor | 6.3 | Best explainability: dual quality, certificates, "what moved". The IC layer is thin and quant-facing; it defaults to three workers against brief P9. |
| 5 | **PE** User blueprint | 2.7 | Several valuable ideas, already grafted by PB/PC/PD. As written it fails governance: the distribution is a decision variable, P(CAGR ≥ 10%) sits in the objective, the action definitions are swapped, and a surrogate supplies live numbers. |

**Recommended base: a composite with PC as the base.**
- PC's decision room and governance layer (Register, pack, computed shadow IC, decision log, politics rules).
- PB's evaluator and seal-service integrity, plus its rendered-claims layer.
- PD's ledger-kernel engine path and its group-economics fixes from the groups addenda.
- PA's dual-quality and certificate explainability on every card.

Section 5 gives the composite. Sections 6 and 7 give the prioritised grafts and the must-fix list.

**Five must-fix items that every proposal misses or gets wrong** (§7 has all 15).
1. No payout lever may exist under Mode B (owner call). Today PB has a `payout_topup` DSL slot; PA and PC keep a top-up and a "payout to minimum" rung in the standing policy.
2. Phase I must never presume owner or bank consent. All four put "a band request" among the reversible levers without reporting u\* with and without it (groups gap_01 §2.1 does).
3. Readiness-Red must be split from event-Red (groups gap_01 §1.3). Otherwise a forward-looking stress indicator fires the irreversible Red playbook.
4. The gate comparator must change in RECOVERY. "Non-inferior to HOLD" is ill-posed when HOLD itself fails Tier 1.
5. Credibility must model strategic bias. The research requires the robust estimator FBE-R plus the pay remedy as a deployment precondition (groups gap_02 §3); no proposal has either.

---

## 1. Method

**Criteria and weights.** The overall score is a weighted judgement. The weights reflect this judge's remit: decision rights, pack clarity and deliberation are the committee's core; governance underwrites everything; the organisational criteria decide whether the system survives contact with seven group heads and a Treasurer.

| Criterion | Weight |
|---|---|
| G1 Decision rights: humans own decisions and contracts; agents propose only | 15% |
| G2 IC pack clarity: what the IC sees; how probabilities and uncertainty are communicated | 15% |
| G3 Usability of SELL/HOLD/REFINANCE/LEVER by group; fairness of the internal capital market | 12.5% |
| G4 Shadow IC and deliberation design | 15% |
| G5 Explainability | 10% |
| G6 Governance: MRM, AI governance, audit trail, claim-to-source | 12.5% |
| G7 Forecast credibility handled constructively | 10% |
| G8 Corporate Finance / Treasurer integration and the owner relationship | 10% |

**Scale.**
- 9–10: best-in-panel and research-complete.
- 7–8: strong, with named gaps.
- 5–6: adequate restatement of the synthesis, with little added.
- 3–4: partial or partly wrong.
- 1–2: contradicts the brief or the user's confirmed definitions.

**What every proposal was checked against.**
- The user-confirmed definitions: REFINANCE = cash-out, LEVER = exposure-up, and the owner sets the distribution as an exogenous liability (brief §1 R8, §6 user answers).
- Principles P1–P15.
- The research findings in the task brief.
- The governance-relevant addenda: groups gap_01 (RECOVERY envelopes, readiness- vs event-Red, priced_on), groups gap_02 (strategic bias, pay as precondition), groups gap_03 (ex-ante tail credit, services ledger).
- LIT14's corrections to the deliberation protocol.

---

## 2. Score summary

| | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted | **Overall** |
|---|---|---|---|---|---|---|---|---|---|---|
| **PA** | 7 | 5 | 6 | 5 | 9 | 8 | 5 | 6 | 6.30 | **6.3** |
| **PB** | 9 | 7 | 5 | 6 | 7 | 9 | 5 | 5 | 6.75 | **6.6** |
| **PC** | 9 | 9 | 8 | 9 | 8 | 8 | 8 | 9 | 8.55 | **8.5** |
| **PD** | 7 | 6 | 7 | 5 | 8 | 7 | 5 | 7 | 6.45 | **6.5** |
| **PE** | 2 | 3 | 3 | 3 | 3 | 2 | 4 | 2 | 2.73 | **2.7** |

PB's overall sits 0.15 below its weighted score. It contains the panel's only explicit contradiction of the owner-set distribution, in its agent action space, and it has no route for time-critical decisions.

---

## 3. Per-proposal assessments

### 3.1 PA: Quant rigor first

| | Score | Justification |
|---|---|---|
| G1 | 7 | Agents may emit only typed, priceable objects: columns, ScenarioSpecs, ViewSpecs, amendment drafts and claims bound to registry IDs (PA §5). The IC/CIO sign the AnalysisContract, AI seats flag but never vote, and "nothing executes" (PA §2 P8, §6, §10). Three things are left implicit: decision tiers; Board/owner sign-off for a RECOVERY contract (only the T_rec extension names the Board, §4.8.4); and who authorises "the standing policy acts" between quarters (§4.8.8). |
| G2 | 5 | Every probability carries value, world range and MC error (§2 R3), and the pack lists the SYN §6.7 contents (§6). But there is no ICD-203 lexicon and no plane label on claims, no pack structure or attention budget. The whole IC is shown solver certificates (Γ, the MMW gap) instead of an IC-readable layer (§6). |
| G3 | 6 | The group action table respects REFINANCE = cash-out and LEVER = exposure-up (§4.6). A request above an envelope is priced at λ only inside the RHS-ranging interval; beyond it the TPC re-solves (§4.8.6). That is a rigorous fairness rule, and "at a kink" labels plus an FTP-as-a-band fallback protect groups from unstable prices (§4.8.6, §10 risk 1). Missing: a dispute route, transparency rules, RECOVERY delivery shares and ex-ante tail credit. The Overlay row leaves HOLD and REFINANCE blank, although groups gap_03 §2.3 defines them for all three books. |
| G4 | 5 | Twelve mandate seats, blind pre-vote, minority reports and signposts are restated from SYN §6.3 in eight bullets (§6). The blueprint personas become the Treasurer's and CIO's mandates. Nothing on influence caps, authentic versus assigned dissent, seat diversity, sycophancy testing, or where seat numbers come from (P1). |
| G5 | 9 | The panel's best explainability. Reduced costs carry one-sided dual intervals, "at a kink" labels, RHS-ranging validity, bootstrap bands and an H–P agreement check (§4.8.6). Forced re-solves flag "second-order effects material" (§4.8.7). The Farley certificate Γ backs "selection not certified" labels (§4.8.5). An Aumann–Shapley path integral explains "what moved H" since last quarter (§4.11 item 4). Exact Shapley is paired with a switch-off null. |
| G6 | 8 | The error ledger A1–A16, with acceptance tests, plus the consistency contract (§4.12) is a ready MRM artefact. Also: an out-of-process evaluator, guarded files, a stale-cache stop, a layering test, and a family-B audit that flags same-family review (§2, §5). It defaults to three workers (2 shared + 1 isolated; §2 P9, §5), against brief P9's default of 2 and LC M5's warning that three is untested and that violations appeared without shared memory. Integrity infrastructure is less hardened than PB's. |
| G7 | 5 | The mechanics are right: a forecast enters once at precision 1/(κ_g²σ̂²) with κ median 1.75, information value is shown against the group's own reference class at n_eff ≥ 20, and pay is decoupled from budget (§4.5, §6, §11 item 19). The presentation politics are not designed: no privacy, no league-table ban, no contest route, no sandbagging symmetry, no strategic-bias model (groups gap_02 §3). |
| G8 | 6 | CF owns the cash rows, λ and FTP publication (§3, §4.8.6), the Treasurer view is complete (§6), and Mode B is the default (§4.7). But the band request sits in Phase I's reversible lever set with no owner-consent guard (§4.8.4). The standing policy keeps "a de Finetti top-up" (§4.8.1), which is a payout decision under Mode B. There is no owner-draw or CFP decision protocol. |

**Fatal flaws.** None from the governance lens.

**Serious gaps.**
- The IC layer is too thin to run a committee.
- Decision rights and event decisions are left to SYN by implication.
- The owner band is presumed available in Phase I.
- A payout top-up stays in a policy that "acts" between quarters.
- Three workers, against brief P9.

**Best ideas to graft.**
- §4.8.6 dual quality on every card.
- §4.8.5 the Γ certificate and its card label.
- §4.8.7 forced re-solves.
- §4.11 item 4 "what moved H".
- §4.12 the error ledger and consistency contract.
- §4.9 item 1 the tolerance cascade: Tier-2 gains may not come from statistically invisible Tier-1 erosion.

### 3.2 PB: Agentic laboratory first

| | Score | Justification |
|---|---|---|
| G1 | 9 | Decision rights are enforced in code. No agent has a `sign` tool. Adopting an amendment needs SignOff objects that no agent tool can create, and a RECOVERY contract needs Board/owner sign-off (PB §5.3, §5.6). No agent holds a trade tool (§2 P1). H's own output is only a candidate that must pass the gates (§5.6), and "a QUALIFIED label never substitutes for the ballot" (§6). Decision tiers are inherited by reference to SYN §6.1 and GRP §7.3. |
| G2 | 7 | Claims are rendered, never written. Each placeholder is filled with value, unit, plane label (SEALED / SEARCH / EXPLORATORY), CI, model range and ICD-203 word. The validator rejects improvement verbs on NOT_QUALIFIED results and probabilities without a range (§5.10). But block D, shown to the whole IC (N_eval, N_eff, deflation, optimism gap, PBO, provenance DAG; §5.8, §6), is lab-facing. There is no attention budget, no usability test and no event path. |
| G3 | 5 | The group lens table is faithful (§4.6). Group blocks show envelope use, cards, Zombie-NAV flags and the marginal-asset agenda (§6). But only agents emit IdeaBundles (§5.4–5.5). Only IC-sponsored hypotheses get extra α-wealth weight (§5.8), so a group head has no defined route to put a proposal into the lab. The quarterly campaign runs from T−25 to T+2 (§5.14), so it cannot serve GP elections or expiring bids. FTP fairness is restated without a dispute or transparency process. |
| G4 | 6 | Twelve mandate seats with no personas, a family-B AI validator, archetypes A–C beside every recommendation, and the SYN protocol with blind pre-vote and hashed minority reports (§6). Seat views are "linearly pooled, not settled by debate" because one persuasive agent can swing a group. But the pooled views are LLM outputs, which is a P1 tension. There is no influence cap and no authentic/assigned dissent ordering. Phase-0 "family B" is a same-provider model, `claude-sonnet-5-5` (§5.11); PB discloses this. |
| G5 | 7 | Cards carry binding rows, shadow prices, marginal value, attribution and flip points by construction (§2 P14, §4.6). The anchored-residual DSL with identity at zero makes the switch-off null control exact, so the IC sees how much of a gain is scaffolding and how much is search (§5.9, TR5). Dual quality is limited to bands over SAA replications (§4.10). |
| G6 | 9 | The panel's best integrity engineering (§5.2): four OS processes with a tool firewall; read-only ACLs; per-request hash checks that move the campaign to ABORTED on mismatch; a CRO-owned seal service with commit-reveal final seeds; and a hash-chained ledger that the gates read. CI drills target each failure the paper observed (§5.16). Claims are rendered and digits outside them rejected (§5.10). MRM inventories the lab as an AI system (§3). Planted-effect campaigns calibrate the lab's false-qualification rate (§7). |
| G7 | 5 | The core is right: precision 1/(κ_g²σ̂²), a forecast enters once, own reference class at n_eff ≥ 20, never a league table (§4.5); pay is decoupled (§11 item 19). But Zombie-NAV flags and "half precision without registered catalysts" go into the group blocks with no privacy, contest or symmetric-scoring safeguards, and there is no strategic-bias model. |
| G8 | 5 | CF owns the ledger, facilities, collateral, payout and λ (§2 R14, §3). "Payout is not a decision variable" (§4.8). The Treasurer block covers LR1–LR8, facility and covenant paths, VM/IM by CSA, owner-draw paths, band activation, and published versus decision FTP (§6). But the agent DSL exposes a `payout_topup` slot (§5.4), contradicting §4.8 and the owner-set liability. The first campaign "starts in CFP stage Red" (§5.14) with no readiness/event split. Owner overrides and stage changes have no route between campaigns. |

**Fatal flaw (wrong as written; a one-line fix).** PB §5.4's PolicySpec grammar lists `payout_topup` as a slot that agents may search. That makes the payout partly an agent-searchable variable. It contradicts PB's own §4.8 and the user-confirmed exogenous, owner-set distribution (brief §6 item 6; user answers of 2026-10-18).

**Serious gaps.**
- No path for event-driven decisions (CFP stage changes, owner overrides, GP-triggered events, expiring windows).
- No path for group heads' own proposals.
- LLM seat views are pooled (P1).
- The CFP stage is Red with no readiness/event distinction.
- The IC pack is weighted toward lab evidence.

**Best ideas to graft.**
- §5.2 the seal service, commit-reveal, tool firewall and hash-chained ledger.
- §5.10 rendered placeholders and the validator rules.
- §5.3 SignOff objects no agent can create.
- §5.4 + §5.9 anchored residuals, which make the null control exact.
- §5.16 integrity drills.
- §7 planted-effect lab calibration.
- §6 "QUALIFIED never substitutes for the ballot".

### 3.3 PC: IC decision room first

| | Score | Justification |
|---|---|---|
| G1 | 9 | The Decision Register gives 23 decision types each a human proposer and decider, a tier, a cadence and a deadline (PC §6.1). The Register and AnalysisContract are written and signed by humans, and agents only draft amendments (§2.2 P8). Seats take numbers only from `implied_actions`, and AI seats never vote (§2.2 P1). Recusal is enforced in software: the vote is recorded but not tallied (§6.6). The band, the mandate and CFP Black go to the Board and owner (§6.1 Q2, A6, E3). A consent agenda keeps every member's right to pull an item. |
| G2 | 9 | Three levels: L0 is a fund-on-a-page readable in ≤ 5 minutes; L1 briefs follow a fixed seven-part anatomy (question, deadline, decider and recusals; options including status quo and DEFER; consequences; economics; beliefs; disagreement; what would change it); L2 reaches every number in two clicks (§6.3). Visual grammar: "central [model range] ± MC error" with scenario hash, ICD-203 words, grey when \|Δ\| < 2 paired SE, P(10%) always beside P(red), and a linter against league tables. A brief with an unmet evidence contract shows "EVIDENCE MISSING", never a silent fill (§6.1). Usability acceptance tests sit in `tests/room` (§6.3, §8). |
| G3 | 8 | Each head gets a first screen and a standing question (§6.4), and a T−18 slot for forecasts, proposals and quotes (§6.2). Decision types with deciders by tier cover GP-triggered events and expiring windows (§6.1 Q5, Q6, Q9, E1, E2). Heads see their budget elasticity ("+100bp of credible α\* buys $X bn"). Transfer-pricing disputes go to a CRO-office committee with a 10-business-day SLA, and each head sees their own itemised charges and peers' only in aggregate (§6.8). Missing: RECOVERY delivery shares φ_g, the spare-lever KKT cap and ex-ante tail credit (groups gap_01 §2.2–2.3; groups gap_03 §4). |
| G4 | 9 | A computed shadow IC (§6.5). Each seat is a declared (beliefs q_k, values θ_k), with θ_k in an admissible set Θ: no indicator terms, and a T6 limit no looser than the IC's tolerance. The engine computes implied actions and regret. A belief/value Shapley split routes belief splits to diligence and value splits upward. Recused positions leave the pool, and a diversity alarm fires on seat rank correlation > 0.9. LIT14 §4–5 corrections are adopted: one debate round by default, an influence cap, a second source for conflicted quotes, authentic dissent shown first, and the Red Team labelled "assigned dissent", aimed at the recommendation and then the human majority. The meeting adds an integration step, a rotating human devil's advocate, and a simultaneous ballot with a second-chance check (§6.6). The record carries a commitment plan (§6.7). The room is evaluated for sycophancy, reliance and legitimacy (§6.9). |
| G5 | 8 | Briefs are rejected unless they carry binding constraints, shadow prices, marginal value per action, attribution and flip thresholds (§2.2 P14). The λ-priced waterfall, envelope use, `priced_on`, signposts and cross-fitted EVSI are fixed parts of the brief (§6.3). Attribution runs prices → counterfactuals → Shapley with an anticipation audit (§4.14), and signpost flip values come from root-finding (§6.7). There is less dual-quality machinery than PA. |
| G6 | 8 | Gates G0–G9 include a brief gate (coverage, plane labels, ICD-203, P14 fields) and a family-B audit with both verdicts printed (§5.4). DecisionRecords are append-only, bitemporal and hashed (§6.7). The room is itself an inventoried model, revalidated annually (A9). It is evaluated by shadow mode, seeded errors that include senior members, sycophancy tests and reliance KPIs (§6.9). Evaluator integrity is stated (§2.2 P2) but not engineered to PB's level: no seal service, no commit-reveal, no hash-chained ledger. |
| G7 | 8 | §6.8 is the only design that treats credibility as an organisational mechanism. It shows information value in dollars; uses the group's own reference class at n_eff ≥ 20; blocks league tables by linter; keeps individual scores private; uses symmetric WIS; holds that "a forecast cannot buy budget" while showing the elasticity; decouples pay (≤ 10 WIS points); and gives groups a contest route decided outside the IC. A8 releases credibility annually. Gaps: no strategic-bias estimator or pay precondition (groups gap_02 §3). The computed group seats hold forecasts "at face value" and make "the politics measurable" (§6.5). That risks showing, item by item, the cost of a named head's bias, which GROUPS §7.4 warns against. |
| G8 | 9 | Corporate Finance is wired into the decision process, not only the data. The Register gives it: Q2, the quarterly owner-draw response 10 days before an instalment (band trigger → Board + owner); Q3, buffer, funding and leverage (the Treasurer decides funding); A5, the facility programme → Board; A6, the mandate proposal → Board + owner; E3, CFP stage playbooks by stage authority; E4, owner overrides (§6.1). The Treasurer's standing question is "Can we pay the next four instalments in the binding state without a red sale?" (§6.4). Decision versus published FTP and the mismatch P&L are on screen. Gaps: the band request is in Phase I's reversible set and a top-up rule remains in the standing policy (§4.11); there is no readiness/event-Red split. |

**Fatal flaws.** None.

**Serious risks.**
- Process burden and legitimacy, which PC itself names as its biggest risk (§10). The mitigations are credible: attention caps, the consent agenda, a Tier-B pilot and shadow mode.
- Computed group-head seats read as caricatures of named people.
- The blueprint's LM row enters Tier 1A as a new hard row (§4.11–4.12). That changes the contract without A1 ratification.
- Band request in Phase I; top-up rule; no FBE-R; no readiness/event-Red split.

**Best ideas to graft.** All of PC §6.1–6.9 (detailed in §6 below).

### 3.4 PD: Pragmatic production path

| | Score | Justification |
|---|---|---|
| G1 | 7 | Agents hold no file, shell, code or network tool, and the evaluator is a separate process (PD §5). No execution adapter exists (§2 P1), and the AnalysisContract takes a CIO/CRO signature (§2 P8). Any what-if number that enters the decision log is recomputed by the Python engine (§6), the cleanest P1 rule in the panel for W1. But PD never mentions the Board: no Board/owner sign-off for SIGNED_IN_RECOVERY (§5), and no decision tiers. |
| G2 | 6 | Block A shows the whole IC the Tier-1 board (nominal, range, CP bound, KL worst case, band), WYNTB, P(10y ≥ 10%) beside worst-model P(red), archetypes A/B/C and gambling flags (§6). Every probability carries model range, MC error and scenario hash (§2 R3). No ICD-203 lexicon, plane labels, pack structure or usability tests. |
| G3 | 7 | The most research-faithful group economics. Each head sees hurdle, FTP and its RECOVERY delivery share φ_g (§6; groups gap_01 §2.2). Decision prices use the spare-lever KKT cap (§4.10; groups gap_01 §2.3). The Overlay gets ex-ante tail credit with the policy residual on the IC line, plus a services ledger and fatigue tracker (§4.8, §6; groups gap_03 §3–4). Its overlay S/H/R/L row is the panel's only complete one (§4.6). There is no dispute or transparency process for FTP. |
| G4 | 5 | Restates the twelve seats and the SYN protocol (§6), with correlated-seat disclosure (§5). Its v1 exit criterion is "hidden-profile ≥ 80%" (§8). That is SYN §6.6's surfacing target, which LIT14 §4.3 and §5 item 4 say to replace with decision accuracy. No new safeguards. |
| G5 | 8 | Prices first with the KKT interlock, capability values from forced warm re-solves, and exact Shapley (§4.14). Dual bands from 10 SAA replications carry sign-flip flags and hysteresis (§4.11). An H–P ranking test (Kendall τ ≥ 0.8, else select on P) and a replay test back the cards (§4.11). "Unstable cards flagged, not hidden" (§10). |
| G6 | 7 | A separate evaluator checks the sha256 of source, config, seeds, cubes and snapshot on every request and refuses on mismatch (§2 P2). MRM owns the append-only, hash-chained registry and the sealed truth (§3). Agentic tests cover replay determinism, seeded-error drills and prompt-injection documents (§8), and "every failure stops loudly" (§4.15). No Board path in recovery and no evaluation of the room. |
| G7 | 5 | Precision κ_g, information value against the group's own class at n_eff ≥ 20, pay decoupled (§4.5, §6, §11 item 19), and Zombie-NAV plus a catalyst rule that halves precision (§4.5). No privacy, league-table, symmetric-scoring or contest rules, and no strategic-bias model. |
| G8 | 7 | CF owns the ledger, the owner-draw engine, FTP publication and collateral (§3, §4.10). The Treasurer sees Phase-I infeasibility prices (never on cards), owner-draw paths, band activation and J\*_A − J\*_B (§6). §4.9 draws the panel's cleanest boundary: "The payout-rule library is used only for proposals to the owner." Missing: an owner-draw decision cadence, CFP stage authorities, Board/owner sign-off in recovery, and the readiness/event-Red rule. |

**Fatal flaws.** None.

**Serious gaps.**
- No decision rights and no Board path.
- T3 is hardened to CVaR₉₉ of stressed VM as a design default (§4.12). That is a Tier-1 contract change the IC/Board must ratify.
- Thin deliberation design, with a surfacing KPI that LIT14 rejects.

**Best ideas to graft.**
- §6 the RECOVERY delivery share φ_g.
- §4.8 + §6 ex-ante tail credit, the services ledger and the fatigue tracker.
- §4.10 the spare-lever KKT cap.
- §4.9 the payout-library boundary.
- §6 W1 numbers recomputed before logging.
- §4.11 the H–P ranking test.
- §4.6 the complete overlay lens.

### 3.5 PE: User blueprint (judged on its ideas)

| | Score | Justification |
|---|---|---|
| G1 | 2 | The policy vector includes the distribution D_t, and the objective rewards a distribution utility U(D_t) (BP §2.5). That takes a decision from the owner. The agora has a "CIO Chair Agent", and an orchestrator "projects... recommended asset-level shifts directly onto the IC screen" (BP §3, §3.2). There is no statement that AI does not vote, no contract ownership and no decision tiers. |
| G2 | 3 | It asks for probability fans and a "P(target) vs distribution rate" surface (BP §4 Phase 4). But the surface treats the payout as a choice. Live numbers come from an unvalidated neural surrogate (BP §3.2 step 4; brief §6 caution). There are no model ranges, MC errors or lexicon, and illustrative figures ("+14.2%", "64% → 41%") are written as agent outputs (BP §3.1, §3.2). |
| G3 | 3 | The four-action matrix and the λ^liq hurdle (BP §2.3) are the right instinct. But LEVER is defined as NAV lending, preferred equity and sub-line extension with a cash inflow (+λN): that is REFINANCE under the user's definition. REFINANCE rests on recaps the GP controls (brief §6 caution). There are no groups, no Corporate Finance, no FTP and no envelopes. |
| G4 | 3 | Opposing institutional utilities, a devil's advocate and a dry-run debate (BP §3.2) are good seeds. But the "Total Return Architect" maximises P(CAGR ≥ 10%) (SYN L9). The personas lack mandate grounding (GROUPS §7.1 caricature risk). There is no blind pre-vote, minority report, dissent record or decision log. |
| G5 | 3 | It has a liquidity shadow price as the hurdle and a live counterfactual interface (BP §2.3, §3.2). But there are no binding constraints, reduced costs, attribution or flip thresholds. Its "implied cost of selling", d/Duration + E[r̃], differs from the research's reservation-price and ρ > s rules (SYN §4.4). |
| G6 | 2 | The only control is "zero hallucinated numbers" (BP §4 Phase 4). There is no evaluator integrity, plane separation, counting, deflation, claim-to-source, audit or MRM. Agent_Discovery "logs proven structural insights for the IC" straight from search (BP §3.1 item 5), the failure P3–P5 exist to stop. LangGraph/AutoGen orchestration conflicts with P9. |
| G7 | 4 | Its most valuable ideas: hierarchical-Bayes de-biasing with group bias, a market-implied anchor, catalyst milestones, Zombie NAV, and P(forecast achieved within k quarters) (BP §2.2, §3.1). But the framing is adversarial ("deal teams... defend the initial r^UW"; a devil's advocate that challenges the groups' forecasts), with no presentation or incentive design (contrast GROUPS §7.4 and L8). |
| G8 | 2 | Distribution as a decision variable is rejected by the user (brief §6 item 6). There is no Treasury or Corporate Finance, no CFP and no FTP. Three ideas are useful to a Treasurer: the Liquidity Guardian persona, the liquidity-margin constraint, and the tail hedge as liquidity that pays when λ peaks (BP §2.4, §3.2). |

**Fatal flaws (as written).**
1. The distribution D_t is a decision variable with a utility term (BP §2.5). The user rejected this (brief §6 item 6; user answers of 2026-10-18).
2. Three places reward hitting 10%: a P(CAGR ≥ 10%) indicator in the objective, a persona that maximises it, and a discovery agent that maximises P(Return ≥ 10% \| Distribution ∈ [5%, 10%]) (BP §2.5, §3.2, §4 Phase 3). That is the digital-option pathology (SYN L9: in a toy model, P(target) rises from ≈34% to ≈68% at the cost of a ≈4.6% chance of a > 40% loss [I]).
3. The action definitions contradict the user-confirmed split: the LEVER row raises cash, and REFINANCE relies on recaps the GP controls (BP §2.3; brief §6).
4. Live IC numbers come from a neural-operator surrogate (BP §3.2 step 4, §4 Phase 3). That violates P1 unless the surrogate is validated, labelled and confirmed by the engine.
5. Search results are reported as "proven" insights with no sealed plane, counting or deflation (BP §3.1 item 5). That is ungovernable under P3–P5.
6. An AI "CIO Chair Agent", with no human decision rights, contract ownership or decision log (BP §3).
7. The tooling is unavailable here: Gurobi/MOSEK, PyMC/Stan and LangGraph/AutoGen (BP §3.1, §4; brief §3, §6). It is unbuildable as written.

**Best ideas to graft.** PB, PC and PD have already adopted them; the brief §6 list stands.
- §2.2 a market-implied return as a fourth fusion signal.
- §3.1 Zombie NAV, P(forecast within k quarters) and catalyst milestones.
- §2.4 the liquidity-margin constraint, and the stress-coverage test (§3.1 item 4).
- §3.2 opposing institutional utilities, kept inside an admissible set.
- §3.2 archetypes A/B/C.
- §3.2 natural-language what-ifs turned into typed overrides.
- §4 the phased roadmap.

---

## 4. Cross-cutting checks against the research and the brief

"Partial" means the mechanism is present but incomplete or ambiguous. Section references are to the proposal.

| # | Check (source) | PA | PB | PC | PD | PE |
|---|---|---|---|---|---|---|
| 1 | No payout lever under Mode B; distribution exogenous (brief §6 item 6; SYN §4.9) | Partial: top-up in standing policy, §4.8.1 | **No**: `payout_topup` DSL slot, §5.4 | Partial: top-up rule, §4.11; A6 correct | Yes, §4.9 | **No**, §2.5 |
| 2 | REFINANCE = cash-out, LEVER = exposure-up (brief R8) | Yes, §4.6 | Yes, §4.6 | Yes, §4.6 | Yes, §4.6 | **No**, §2.3 |
| 3 | P(10%) reported, never maximised (SYN L9, §4.9) | Yes, §4.9 | Yes, §4.11 | Yes, §4.12; seats in Θ | Yes, §4.1 | **No**, §2.5 |
| 4 | λ only from a feasible problem; `priced_on` on cards (L15; gap_02 §4) | Yes, §4.8.4 | Yes, §4.10, §5.7 | Yes, §4.10 | Yes, §4.10–4.11 | No |
| 5 | Owner/bank consent never presumed in Phase I: u\* reported with and without band and revolver (groups gap_01 §2.1) | No | No | No | No | No |
| 6 | Board/owner sign-off for a RECOVERY contract (SYN §5.3 G0) | Partial: T_rec extension only | Yes, §5.3 | Yes, §5.4 G0 | No | No |
| 7 | Readiness-Red vs event-Red (groups gap_01 §1.3) | No | No: "starts in CFP stage Red", §5.14 | No | No | No |
| 8 | Event decisions: CFP stage change, owner override, GP events, expiring windows (SYN §6.1, §6.5) | No | No | Yes, E1–E4 | No | No |
| 9 | Shadow-IC numbers from the engine, not LLMs (P1) | Partial: unspecified | No: LLM seat views pooled, §6 | Yes, §6.5 | Partial: unspecified | No |
| 10 | ICD-203 lexicon and plane labels on probabilities (SYN §5.5) | No | Yes, §5.10 | Yes, §6.3, G7 | No | No |
| 11 | Credibility presentation safeguards: own class, n_eff ≥ 20, private, no league tables, contest (GROUPS §7.4) | Partial | Partial | Yes, §6.8 | Partial | No |
| 12 | Strategic-bias FBE-R and pay as a deployment precondition (groups gap_02 §3) | No | No | No | No | No |
| 13 | RECOVERY envelopes Λ_g + φ_g·g_t with delivery tracking (groups gap_01 §2.2) | No | No | No | Yes, §6 | No |
| 14 | Ex-ante tail credit, policy residual on the IC line, services ledger (groups gap_03 §3–4) | No | No | Partial: credits crisis payoffs, §4.8 | Yes, §4.8, §6 | No |
| 15 | FTP dispute and transparency process (L14; GROUPS §4.3) | Partial: ranging rule | No | Yes, §6.8 | No | No |
| 16 | LIT14 deliberation corrections (§4–5) | No | Partial: pooling over debate | Yes, §6.5–6.6, §6.9 | No: surfacing KPI | No |
| 17 | Gate comparator valid in RECOVERY (brief P5 Gate 1 when HOLD fails Tier 1) | No | No | No | No | No |
| 18 | Default 2 workers, configurable to 4 (brief P9; LC M5) | **No**: 3 workers | Yes | Yes | Yes | n/a |
| 19 | No surrogate numbers in front of the IC (brief §6) | Yes | Yes | Yes | Yes | **No** |

**Reading.**
- Rows 5, 7, 12 and 17 are missed by every proposal. They become must-fix items 2, 3, 7 and 4.
- Rows 1 and 9 separate the proposals. PD draws the cleanest payout boundary; PC is the only P1-compliant shadow IC.

---

## 5. Recommended base: a composite on PC

From this judge's remit, PC is the base. It is the only design whose organising object, the Decision Register, matches how a sovereign fund's committee actually works: recurring and event-driven decisions, each with an owner, a decider, a deadline and an evidence contract. The other proposals add what PC lacks.

| Layer | Base | Grafted from | Why |
|---|---|---|---|
| Decision layer: Register, briefs, pack, deliberation, ballot, decision log, signposts | **PC §6.1–6.9** | PA §4.8.6 dual-quality labels on cards; PB §6 block D cut to one page ("what we tried, what qualified, what did not") | G1, G2, G4 and G8 leader; LIT14-sourced protocol |
| Claims and evidence rendering | **PB §5.10** | PC G7 brief gate (P14 fields mandatory) | Numbers can only be rendered, never written |
| Evaluator, planes, seal, ledger | **PB §5.2, §5.16** | PD separate final-plane evaluator instance (§5); PC gates G0–G9 | G6 leader; infrastructure, not prompts (paper l.7489-7490) |
| Contract | **PB §5.3** SignOff objects | PC Register as a signed catalogue; A1/A2 annual ratification of bands and model weights | Agents can never adopt; Board/owner in RECOVERY |
| Group economics and fairness | **PD §4.8, §4.10, §6** | PC §6.8 dispute SLA and transparency; PA §4.8.6 ranging rule for requests above an envelope | Research-faithful prices plus a fair process |
| Treasury and owner | **PC §6.1** Q2, Q3, A5, A6, E3, E4 | PD §4.9 payout-library boundary; must-fix 1–3 | CF runs the liability side inside the process |
| Explainability | **PA §4.8.5–4.8.7, §4.11 item 4** | PD §4.11 H–P ranking test; PB §5.9 exact null control | Every price shows how far it can be trusted |
| Engines and production path | PD's ledger kernel and measured budgets (PD §1, §4.15) | PA §4.12 error ledger and consistency contract | Left to the quant and production judges; noted for coherence |

PC's own MVP keeps the burden manageable: Q1 with Phase I, Q2, Q4, Q5 and Q6 only, on `StubBackend`, with pre-vote, log and signposts (PC §8). That MVP should come first. The full 23-entry Register should follow after a Tier-B pilot and shadow mode (PC §10).

---

## 6. Prioritised graft list

1. **PB §5.2 + §5.16: integrity infrastructure.**
   - A process-separated evaluator with a tool firewall, read-only ACLs and per-request hash checks (ABORTED on mismatch).
   - A CRO-owned seal service with commit-reveal final seeds: HMAC(salt, world), committed at SIGNED and revealed after the run.
   - A hash-chained ledger that the gates read.
   - CI integrity drills mapped to the failures the paper observed (paper l.1224-1234, l.1320-1322).
2. **PB §5.10: claims rendered from typed placeholders.**
   - `{{m:metric_id|format}}` is filled with value, unit, plane label, CI, model range and ICD-203 word.
   - The validator rejects literal digits, improvement verbs on NOT_QUALIFIED results, probabilities without ranges, citations to memory, and synthetic numbers attributed to ADIC.
3. **PB §5.3: human-owned contract.**
   - SignOff objects that no agent tool can create.
   - Board/owner sign-off when mode = RECOVERY.
   - The miss-to-false-discovery cost ratio and the sealed test's MDE fixed in the contract.
4. **PC §6.1: the Decision Register.**
   - Each entry carries proposer → decider, tier, cadence and deadline.
   - Options always shown: status quo, DEFER, the recommendation and archetypes A/B/C.
   - Evidence contracts compile into a content-hashed evidence DAG; "EVIDENCE MISSING" is never silently filled.
   - It includes event decisions E1–E4, the quarterly owner-draw response Q2 and the owner mandate proposal A6.
5. **PC §6.3: the three-level pack.**
   - L0 in ≤ 5 minutes; L1 seven-part briefs; L2 two-click drill-down.
   - Visual grammar: "central [model range] ± MC error" with scenario hash; ICD-203 words; grey when \|Δ\| < 2 paired SE; P(10%) always beside P(red); a league-table linter.
   - Usability acceptance tests in `tests/room`.
6. **PC §6.5: the computed shadow IC.**
   - Each seat is (q_k, θ_k ∈ Θ): no indicator terms, and a T6 limit no looser than the IC's tolerance.
   - Implied actions and regret come from `implied_actions`.
   - A belief/value Shapley split; recused positions leave the pool; a diversity alarm.
7. **PC §6.5–6.6: deliberation hygiene, sourced from LIT14 §4–5.**
   - One debate round by default, and an influence cap.
   - A second source for conflicted Secondaries and Capital Solutions quotes.
   - Authentic minority reports first; the Red Team labelled "assigned dissent", aimed at the model recommendation and, after H1, the human majority.
   - An H2 integration step, a rotating human devil's advocate, and a simultaneous ballot (approve / resize / defer / reject) with a second-chance check.
8. **PC §6.6–6.7: committee mechanics.**
   - Consent-agenda rules: P(best) ≥ 0.8 in every model class, no minority trigger, minimax regret ≤ materiality, no Board trigger, and every member may pull an item with a logged reason.
   - A 180-minute attention budget with ≤ 4 Tier-A items.
   - Recusal enforced in software.
   - DecisionRecord with override reason codes (belief, value, information outside the model, implementation, legal consent, relationship), a commitment plan, and signposts found by root-finding.
9. **PC §6.8: the politics table.**
   - Credibility shown as information value in dollars, against the group's own reference class at n_eff ≥ 20, with private individual scores, no league tables and symmetric WIS.
   - "A forecast cannot buy budget", with the elasticity displayed; pay decoupled; a contest route outside the IC.
   - FTP disputes go to a CRO-office committee with a 10-business-day SLA; heads see their own itemised charges and peers' only in aggregate.
10. **PD §6, §4.8, §4.10: group-economics fixes from the groups addenda.**
    - The RECOVERY delivery share φ_g in every group block (groups gap_01 §2.2).
    - The spare-lever KKT cap on decision prices (groups gap_01 §2.3).
    - Ex-ante kernel crediting of the tail hedge, with the policy residual on the IC line, a services ledger and a fatigue tracker (groups gap_03 §3–4).
    - The complete overlay S/H/R/L row (PD §4.6).
11. **PD §6: P1 rule for what-ifs.** Any W1 (entropy-pooling) number that enters the decision log is recomputed by the Python engine. The in-browser golden self-test shows a red banner on any mismatch (also PC §6.6).
12. **PD §4.9: the payout boundary.** The payout-rule library and Modes A/H serve only owner proposals (Register A6), never ADIC decisions.
13. **PA §4.8.6–4.8.7: dual quality on every card.**
    - One-sided derivatives with "at a kink" labels, RHS-ranging validity, bootstrap bands and an H–P agreement check.
    - Envelope requests priced at λ only inside the ranging interval; beyond it, a TPC re-solve.
    - Forced re-solves flagged "second-order effects material".
14. **PA §4.8.5 + §4.11 item 4.** The Farley certificate Γ, with "selection not certified" on the card. An Aumann–Shapley "what moved H since last quarter" attribution for the IC.
15. **PA §4.12.** The error ledger A1–A16 and the consistency contract, as the MRM validation artefact.
16. **PC §6.9 + LIT14 §4.5: evaluating the room in shadow mode.**
    - Hidden-profile *decision accuracy*.
    - Seeded errors that include senior members.
    - Sycophancy tests.
    - Reliance split by whether the model was right or wrong, and override accuracy.
    - DEFER frequency and anti-portfolio returns.
    - An annual legitimacy survey.
    - Annual MRM revalidation of the room (PC A9).
17. **PB §5.9.** An exact switch-off null control via anchored residuals (identity at zero), reported as "scaffolding share versus searched share" in a one-page lab block.
18. **BP §2.2, §2.4, §3.1, §3.2, as adopted by PB/PC/PD.**
    - The market-implied anchor, entered through the pricing committee with a second source (PC §4.5).
    - Zombie NAV and P(forecast within k quarters).
    - Catalyst milestones.
    - The stress-coverage ratio on the offset card (PC §4.8; PD §4.12 item 2).
    - Archetypes A/B/C beside every recommendation.
    - Natural-language what-ifs turned into member-confirmed typed overrides.

---

## 7. Must-fix list (regardless of base)

1. **No payout lever under Mode B (owner call).**
   - Delete PB's `payout_topup` DSL slot (PB §5.4).
   - In the standing policy, disable the de Finetti top-up and the waterfall's "payout to minimum" rung (PA §4.8.1, PC §4.11; SYN §4.8) unless the contract mode is H or A with owner sign-off.
   - Modes A/H and J\*_A − J\*_B appear only in owner-proposal packs, labelled counterfactual (brief §6 item 6; user answers of 2026-10-18).
2. **Never presume owner or bank consent.**
   - Phase I reports u\* and the IIS separately for four lever sets: group levers only; + Treasury; + the revolver; + the owner band (groups gap_01 §2.1, readings R0x / R0 / R1 / R2).
   - λ, FTP, envelopes and cards are priced only on levers already signed.
   - A RECOVERY contract needs Board/owner sign-off (SYN §5.3 G0). It is missing in PD and partial in PA.
3. **Split readiness-Red from event-Red.**
   - A forward-looking SH_TP signal under T4′ triggers the Phase-II plan: pacing rule, revolver request, band request.
   - It never triggers the Red playbook's irreversible actions: line draws, P2S, amber sales, hedge monetisation (groups gap_01 §1.3).
   - Event-Red comes only from 30-day coverage, Treasury ÷ NAV, liquid share and LaR. On the synthetic book, SH_TP is 17 months against the 18-month Amber line, and the pacing rule lifts it to 20 months (Amber) [I-calc; SYNTHETIC].
4. **Fix the gate comparator in RECOVERY.**
   - When HOLD fails Tier 1, "non-inferior to HOLD" (brief P5 Gate 1; all four proposals) penalises the premium that survival costs.
   - Use the Phase-II restored minimum-cost plan as the comparator, and report HOLD as a control marked "Tier-1 infeasible".
   - Otherwise the IC sees survival actions labelled NOT_QUALIFIED.
5. **P1 for the shadow IC.**
   - Seat numbers come only from engine computation under declared (q_k, θ_k) (PC §6.5).
   - LLM seats argue, select evidence and write minority reports. Any probability they state is labelled "agent judgment" and is never pooled with model outputs.
   - This fixes PB §6's "linearly pooled" views and the unspecified seat outputs in PA §6 and PD §6.
6. **AI seats are mandate analyses, not people.**
   - Name them by mandate ("PE mandate, AI seat").
   - Never show "regret of the PE head".
   - Present forecast disagreement as information value, not as the cost of a named head's bias (GROUPS §7.4; the risk sits in PC §6.5).
7. **Credibility must model strategic bias.**
   - In production, use FBE-R: a Huber bias regression with regime, anchoring-gap, SELL-flag and envelope-status covariates, pooled across groups.
   - Add gate G-E: a group that fails under strategic bias gets non-trivial forecast precision only after the pay remedy (b ≤ 0.005, s ≥ 50, nothing scaling with budget). Pay design is a deployment precondition (groups gap_02 §3).
   - In the prototype, status-quo pay leaves even the robust FBE failing its CRPS gate [I-calc; SYNTHETIC]. No proposal includes this.
8. **Make the politics rules executable tests:** n_eff ≥ 20; own reference class; private scores; no league tables; symmetric WIS; the contest route; the FTP dispute SLA; own-versus-peer charge visibility (PC §6.8).
9. **Explicit, machine-enforced decision rights.**
   - The SYN §6.1 tiers, GROUPS §7.3 group rights and CFP stage authorities.
   - The symmetric irreversibility protocol: letting a bid or financing window lapse is a decision.
   - Event decisions: CFP stage changes, owner overrides, GP-triggered events, expiring bids. These are missing in PA, PB and PD; PC's Register (§6.1) is the template.
10. **Human authority over the standing policy and module F.**
    - Between meetings, the standing policy is an IC-approved delegated rule executed by named humans under CFP and tier authorities. It never self-executes (PA §4.8.8, PC §4.11).
    - When module F projects an IC amendment, the pack shows "what changed", and a Board exception path exists for any Tier-1 override (SYN §6.1 Board triggers).
11. **Group fairness in RECOVERY and for the Overlay.**
    - RECOVERY envelopes are Λ_g + φ_g·g_t, with delivery tracking; a group behind schedule loses envelope or buys it back at the dual (groups gap_01 §2.2).
    - Reverse stresses never price.
    - `priced_on` and the recovery hash appear on every card, enforced by the AI Validator (groups gap_01 §5).
    - The tail hedge is credited ex ante, with an IC-owned policy residual. Services are booked to client groups at FTP, and V2 runs on DVA ledgers (groups gap_03 §3–4).
12. **Probability communication.**
    - ICD-203 words and plane labels (SEALED / SEARCH / EXPLORATORY) on every probability, with the model range first. PA and PD lack the lexicon.
    - P(10%) always beside P(red), and never optimised.
    - No illustrative blueprint figure in any pack.
13. **Tier-1 contract changes need A1 ratification.**
    - PD's hardening of T3 to CVaR₉₉ VM (PD §4.12) and PC's new LM row (PC §4.11–4.12) change the Tier-1 contract.
    - The IC/Board must ratify them with the priced ε_R–cost impact.
    - They must sit inside Phase I's tiers so they cannot pin duals (gap_02 §4).
14. **Honest cross-family review.**
    - Phase 0 has one provider. Label same-family review "correlated" and never extremise.
    - Apply the ≤ 40%-per-family seat rule only across approved families (SYN §5.7, §6.2; PB §5.11 discloses this correctly).
15. **Protocol and parameter defaults.**
    - Use brief P9's default of 2 workers (configurable to 4), not PA's 3 (LC M5).
    - Replace PD's "hidden-profile surfacing ≥ 80%" exit criterion with hidden-profile decision accuracy plus the surfacing-to-use conversion rate (LIT14 §4.3; §5 item 4).

---

## 8. Interfaces that implement the must-fix items

Pydantic v2 sketches for the chief architect. Names are indicative.

```python
class MandateMode(str, Enum):
    B_OWNER_CALL = "B"      # default: the draw is exogenous (user, 2026-10-18)
    H_HYBRID = "H"          # owner band pre-agreed in CFP Red / crisis
    A_ADIC_RULE = "A"       # counterfactual only, for owner proposals (A6)

class AnalysisContract(BaseModel, frozen=True, extra="forbid"):
    mandate_mode: MandateMode = MandateMode.B_OWNER_CALL
    owner_signoff: SignOff | None = None      # required iff mandate_mode != B
    purpose: Literal["DECISION", "OWNER_PROPOSAL"] = "DECISION"
    # Type rule TR8 (DSL compiler): slots {payout_topup, payout_to_minimum} compile
    # only if mandate_mode in {A, H} AND owner_signoff is set; OWNER_PROPOSAL outputs
    # never reach group cards, envelopes or FTP.                     -> must-fix 1

class ConsentScenario(str, Enum):              # groups gap_01 §2.1
    R0X_GROUP_LEVERS = "R0x"; R0_TREASURY = "R0"; R1_REVOLVER = "R1"; R2_BAND = "R2"

class Phase1Result(BaseModel):
    u_star: dict[ConsentScenario, dict[RowId, float]]
    iis: dict[ConsentScenario, list[str]]       # levers named by owning group
    pricing_scenario: ConsentScenario           # highest scenario whose levers are SIGNED
    recovery_hash: str | None                   # -> must-fix 2

class CFPReading(BaseModel):                    # groups gap_01 §1.3
    readiness_stage: Stage   # from forward-looking SH_TP under T4'
    event_stage: Stage       # from LCR(30d), Treasury/NAV, liquid share, LaR99/CBC
    playbook: Literal["PHASE2_PLAN", "AMBER", "RED", "BLACK"]
    # invariant: playbook in {RED, BLACK} only if event_stage >= Red    -> must-fix 3

class GateSpec(BaseModel):
    ni_comparator: Literal["HOLD", "RESTORED_BASELINE"]   # RESTORED_BASELINE when contract is in RECOVERY
    hold_label: Literal["control", "control_tier1_infeasible"]  # -> must-fix 4

class SeatSpec(BaseModel, frozen=True):
    seat_id: str
    display_name: str                 # e.g. "PE mandate (AI seat)"   -> must-fix 6
    beliefs: BeliefChannel            # q_k
    values: Theta                     # theta_k, validated against the admissible set
    numeric_source: Literal["implied_actions"] = "implied_actions"
    judgmental_probability_label: Literal["agent judgment"] = "agent judgment"  # never pooled -> must-fix 5

class CredibilityRelease(BaseModel):          # groups gap_02 §3; GROUPS §5, §7.4
    group: GroupId
    n_eff: float
    shown: bool                               # True iff n_eff >= 20
    reference_class: str
    information_value_usd: float
    estimator: Literal["FBE-R"]
    strategic_terms: tuple[str, ...] = ("regime", "anchoring_gap", "sell_flag", "envelope_status")
    pay_remedy_ok: bool                       # gate G-E; False caps forecast precision
    contest_ticket: str | None = None         # -> must-fix 7, 8

class GroupEnvelope(BaseModel):               # groups gap_01 §2.2
    group: GroupId
    phase2_envelope: float
    glide_share: float                        # phi_g
    scheduled_delivery: float
    delivered: float
    priced_on: Literal["feasible", "restored_problem"]
    recovery_hash: str | None                 # -> must-fix 11
```

**CI tests to add.** Each pins one must-fix item.

| Test | Must-fix |
|---|---|
| `test_no_payout_lever_in_mode_B` | 1 |
| `test_phase1_reports_all_consent_scenarios` | 2 |
| `test_readiness_red_never_fires_red_playbook` | 3 |
| `test_ni_comparator_restored_in_recovery` | 4 |
| `test_seat_numbers_only_from_implied_actions` | 5 |
| `test_no_named_person_regret_in_pack` | 6 |
| `test_credibility_hidden_below_neff_20` and `test_no_league_table` | 8 |
| `test_recovery_envelopes_sum_and_glide_shares` (already in groups gap_01 §2.4) | 11 |

*SYNTHETIC – NOT ADIC DATA (every figure quoted from the research).*
