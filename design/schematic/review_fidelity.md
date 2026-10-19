# Fidelity review: TPA Lab architecture schematic

**Reviewed:** `design/schematic/architecture_model.json` (6 views, 325 nodes, 510 edges, 100 notes) and its rendering `design/schematic/TPA_Lab_Architecture.html`.
**Against:** `design/ARCHITECTURE.md` v1.0 (read in full, §0–§15), plus `design/00_DESIGN_BRIEF.md` §8 for Real Assets only.
**Date:** 2026-10-18. **Scope:** whether the content is faithful to the document. Layout and visual design are out of scope.

## Verdict

The schematic is largely faithful and can be fixed in place. The following match the document closely and need no change:

- all 31 modules of the §3.2 layer list, with §3.4 owners where they are given;
- every flow in the §3.2 and §2.4 mermaid diagrams;
- every step of the §3.6 cycle;
- every state and transition of the §7.4 state machine;
- the §7.3 role table and the full 27-tool evaluator catalogue;
- the §8.5 seat table (q_k, γ, λ_T, T6);
- the §6 capital-market mechanics (decision prices versus published FTP, envelopes, recovery envelopes, pacing, contingent budgets, desk conflicts, netting, services ledger).

All section references resolve to real headings: 118 sections and 36 ADRs. No edge points to a missing node.

There is **one high-severity gap**. §0.3 rule 4, the lexicographic Tier-1/Tier-2 program with T6 banded by model class (§5.2), does not appear as a component anywhere. There are also **five medium issues**:

1. the consequences of readiness-Red ≠ event-Red are missing;
2. agent packages and IC amendments are not routed through module F;
3. the evaluator's MCP server sits outside the TB2 enclosure in the overview;
4. 52 tooltips say "Owner: not stated in ARCHITECTURE.md" where §3.4 does name an owner;
5. the human G8 countersignature is attributed to the AI Auditor.

Real Assets is visibly badged on all 10 Real Assets nodes and drawn with the Real Assets halo on all 26 Real Assets edges. Its content matches brief §8, with four small labelling problems (F-16 to F-19).

**Recommendation:** fix F-01 to F-06 before the schematic is shared. The low items can follow.

## Issues

Severity: **high** means a design rule from §0.3, or a central component, is missing or misdrawn. **Medium** means a relationship, boundary or owner is wrong, or an important flow is missing. **Low** means a precision, labelling or consistency problem.

| ID | Sev. | View | Item | What is wrong | Correct content (source) |
|---|---|---|---|---|---|
| F-01 | high | engines | (missing node) | The lexicographic objective and constraint program is absent. "lexicographic", "Tier 1A" and "Tier 2" occur nowhere in the model. "T6" appears only in notes, in the `gate1` and `theta` details and in `c_t12`. "Banded by model class" appears once, in the room's `pack_l0` tooltip. H (`phase1`, `phase2`) is drawn without its rows or objective, and P without the bands it certifies against. | Add a node "Objective & Tier-1 contract" (§5.2; ADR-10, ADR-11) with: Level 0 feasibility → Tier 1A T1–T9 (T6 red event ≤ 1%, banded by model class: M1–M5 and mixture 0.5/1/2%, M6 —/2.5/5%) → Tier 1B floor → Tier 2 J (CRRA(3) + L2 shortfall; PWL proxy in H). P(10%) is reported beside P(red) and never maximized (§0.3 rule 4). Draw these edges: `contract` → node "tier1: Tier1Spec" (§10.1); node → `phase1` "tiers 𝒯₁–𝒯₄" (§5.5); node → `phase2` "rows H2–H6; H4 T6 surrogate per class c ∈ {M1…M6, MIX}; objective" (§5.4); node → `certify` "T6/T7/T9 vs class bands" (§5.10); node → `module_f` "linearized Tier-1 rows" (§5.8). Add the CFA loop `certify` → `phase2` "tune buffers b^red_c, b^floor_m until P certifies" (§5.3). Add the T5 overlay rows `overlay` → `phase2` "OV1/OV2 rows" and `overlay` → `module_f` "SIMM IM, OV3 re-check" (§4.6; ADR-13). |
| F-02 | medium | engines; overview | `cfp_reading`; overview `t4_replica`, `ledger`, e56 | §0.3 rule 6 is half drawn. The engines view shows the readiness/event split, but its only consumers are pacing and the pack. **Missing:** readiness-Red → PHASE2_PLAN (adopt the pacing rule, request the revolver, request the band). **Missing:** the event stage as the sole driver of irreversible playbooks through the stage authorities. The invariant `playbook ∈ {RED, BLACK}` only if `event_stage ≥ Red` is tested by `test_readiness_red_never_fires_red_playbook`. In the overview, rule 6 is invisible: `t4_replica` → `pack` "T4′ survival, CFP stage" credits the whole stage to the T4′ replica. The event stage comes from the ledger's event indicators. | Add `cfp_reading` → "PHASE2_PLAN (readiness-Red)" and `cfp_reading` → "E3 playbook, event stage only; Green Treasurer, Amber CIO, Red IC weekly, Black Board and owner" (§4.9 CFP table; §8.1; §8.2 E3; ADR-08; §10.7). In the overview, restore "CFP readiness/event" to `ledger` (§3.2 L5). Relabel e56 "T4′ survival → readiness stage". Show the event indicators (ADIC-LCR(30d), Treasury ÷ NAV, liquid share, LaR99 ÷ CBC_TP) feeding the CFPReading (§4.9). |
| F-03 | medium | engines; room | `module_f` inputs | Module F receives only optimizer output (`phase2`, `cards`, `recovery_mode`). §5.8 says every proposal passes through F: optimizer, agent package or IC amendment. When F changes an IC amendment, the pack shows the change, and any Tier-1 override needs the Board exception path (JG-MF10). Archetypes A/B/C also pass F (§5.10), but the room's `controls_arch` says so only in its sublabel. Between-quarter execution (P0 and the CFP playbooks act only as IC-approved delegated rules executed by named humans, each logged as a DecisionRecord) appears in notes only. | Add `lab_agents` (via `evaluator`) → `module_f` "agent package". Add `ic_vote` → `module_f` "IC amendment" → `pack` "what changed". Add `module_f` → Board "Tier-1 override exception" (§5.8; ADR-32). Add `core_policy` → `module_f` "archetypes A/B/C" (§5.10; ADR-26). Add a human node "named human executors (delegated rules)" → decision log "rule-triggered DecisionRecord" (§5.9; §8.1; ADR-32). |
| F-04 | medium | overview | `mcp_server`, group `tb2_eval`, `tb5`–`tb7` | The TB2 enclosure (SVG x 518–664, y 1096–1222) holds only `evaluator_search`. `mcp_server` sits in the "interfaces" lane at y 537, so the chain lab → `mcp_server` → `evaluator_search` (e28, e29) crosses TB2 between the MCP server and the evaluator. §7.2 puts the "MCP 2.3 stdio server for typed tools" inside `tpa evaluator serve --plane search`, and the lab view does the same (`eval_tools` in lane `l_eval`). The overview also draws the engines (L0–L7) outside TB2, although they run read-only inside the evaluator process (§7.2; the §3.2 mermaid "Evaluator processes" subgraph). TB5, TB6 and TB7 are isolated notes with no attachment. | Split `mcp_server` into (a) an evaluator MCP server inside the TB2 enclosure (§7.2; §11.3) and (b) a read-only analyst server for operators (§11.3), keeping e17 and e30 on (b). Annotate TB2 "engines loaded read-only, content-hashed, inside the evaluator process" (§1.2 P2; §7.2). Attach `tb5` to e10 and to the sign-off edges e2, e4, e5. Attach `tb6` to e26 and `tb7` to e80 (§2.4). |
| F-05 | medium | lab; room; capital_market; cycle | 52 nodes with an empty owner | The HTML renders "Owner: not stated in ARCHITECTURE.md" for 52 nodes. For most of them §3.4 does state the module owner, so the tooltip is wrong. | Use §3.4 owners. **`idm`** (IC secretariat; Register owned by the CIO): `seat_cio`, `seat_cro`, `seat_treasurer`, `seat_groups`, `seat_outside`, `seat_red_team`, `regret_split`, `protocol`, `minority_reports`, `agenda`, `consent_agenda`, `decision_rules`, `decision_rights`, `h6`, `signposts`, `commitment_plan`, `reg_event`. **`evaluator`** (MRM; "plane registry, caches, counting, gates"): `caches`, `plane_search`, `plane_final`, `plane_exploration`, `plane_historical`, `plane_calibration` (also readable by MRM only, §7.5), and `implied_actions`, `w2`, `w3`, `sealed_confirm`, which are evaluator tools/runs (§7.3). **`seal`** (MRM; seal custody by CRO office): `sealed_store`. **`agents`** (CIO office under AI governance; MRM inventories the lab): `backend_live`, `backend_replay`, `backend_stub`. **`claims`** (same): `provenance_dag`. **`pack`** (IC secretariat): `w1`. **`data`** (Data office): `quote_table` (§9.2). **`registry`** (MRM): `proposal_intake` (T−25 filings are "Registry records", §3.6). **core** (TPA desk): `controls_arch` (frozen PolicySpecs, §5.10). Lab `engines`: "per module, §3.4". Keep "not stated" only for `design_linter`, `integrity_drills`, `planted_calibration` and the cycle steps. Also, engines `recovery_mode` shows sign-off authority as its owner; the module owner is "TPA desk; CRO signs Phase I" (§3.4), with sign-off by mode in the sublabel (§5.5). |
| F-06 | medium | room | e17 `auditor` → `briefs_l1` | The label "'supports' + countersign (G8)" attributes the human countersignature to the family-B AI Auditor. The countersignature is a human act and is a G8 exit condition. | Relabel e17 "'supports' verdicts, overclaim flags (G8)" (§7.3; §10.6). Add a human countersignature edge into the audited pack, "human countersignature (G8)" (§3.6 T−9…T−8; §7.6 G8; §10.6). ARCHITECTURE.md does not name the signer, so do not invent a role. |
| F-07 | low | overview | `truth_store` → `mrm` (e13), `synth` | §0.3 rule 10 says synthetic data are "validated by parameter recovery". This appears only implicitly, inside "gates V1–V24" on `synth`. "SBC", "parameter recovery" and "G-A" occur nowhere. The rule that gate failures block the pack is not drawn. | Label e13 "SBC, ±5pp parameter recovery (V16–V18), misspecification gates G-A–G-E" (§9.4; §4.7 Validation). Add a guard `synth` → `pack` "V1–V24 failures block the pack" (§9.4). |
| F-08 | low | engines | (missing) | The policy-class structure is not shown. "PFA/CFA/DLA/VFA" and "terminal" occur nowhere. P0 (PFA) and H (DLA) are drawn. VFA terminal values ω_g, ψ_g, regressed from P paths into H's terminal wealth, are missing; CFA is covered by F-01. | Add `core_sim` → `phase2` "terminal values ω_g, ψ_g (regress-later)" (§5.12; §5.4 objective; §5.3 VFA). Optionally tag `core_policy` PFA and `phase2` DLA (§5.3). |
| F-09 | low | lab | `claims_renderer`, `claims_validator` in lane `l_lab` | The lane asserts process membership ("tpa lab run … the only process with egress (TB3)"). §7.2 lists that process's contents as the FSM, budgets, tool firewall, LLM gateway, role prompts and campaign memory. `validate_claims` is an evaluator tool (§7.3 catalogue), and briefs are built by `tpa room` (§7.2). | Move the claims nodes out of the egress-process lane, for example into an "L9 claims (module)" lane, or note that §7.2 does not assign them to a process. |
| F-10 | low | lab | `gate1` | Gate 1 runs on both the search and final planes (§7.6), but `gate1` has input only from `evaluator_search`. Gate 3's "correct on the final plane" has no Gate-1 input from `evaluator_final`. The sublabel "T1–T9 bands" merges two different tests: hard rows T1–T5 and T8 must hold on every path, while only T6, T7 and T9 are tested against class bands. | Add `evaluator_final` → `gate1` → `gate3`. Relabel "TR1–TR8; T1–T5, T8 every path; T6/T7/T9 in class bands; floor; NI ≥ −5bp; OV1–OV3; no pinned dual; no gambling" (§7.6). |
| F-11 | low | engines | e77, e95 | e77 `certify` → `pack` "CP bounds, G6 labels": G6 labels (QUALIFIED, NOT_QUALIFIED, NOT_CORRECT, NOT_ASSESSED) come from Gate 3 in the final-plane evaluator (Holm LCB95, PBO, MDE), not from core.certify. e95 `pack` → `ic_vote` "pack → blind pre-vote": H0 sees only the fact pack, with no AI narrative, seat map or minority reports. | Relabel e77 "CP bounds vs class bands" and add `evaluator` → `pack` "G6 labels" (§7.6). Relabel e95 "fact pack only at H0; full pack at H1" (§8.6). |
| F-12 | low | capital_market | e56, e66, e76, `rule_cfp_authority` | Tier-B items are routed to the CIO alone: e56 "requests ≤ +20% (Tier B)", e66 "Q9 transfers → Tier B", e76 "HF notices, P2S (Q8)". Tier B is CIO + CRO, and Q8's decider is "Public Markets → CIO + CRO". The CFP-authority sublabel ends "Black Board" without the owner. | Route these edges to CIO + CRO, either by adding `cro_office` as co-decider or by labelling "CIO + CRO" (§8.1; §6.3; §8.2 Q8, Q9). Change the sublabel to "Black Board and owner" (§8.1; §4.9). |
| F-13 | low | engines; capital_market; overview | `note_recovery`, capital_market e7, overview sign-off edges | `note_recovery` omits two conditions: a T6 capacity breach of the best reversible mix also triggers STRUCTURAL, and NORMAL also needs T6 screens within tolerance. Capital-market e7 Board → `recovery_envelopes` "STRUCTURAL_RECOVERY sign-off" implies the Board governs recovery envelopes generally. In fact §6.4 envelopes apply in EXECUTION_RECOVERY too, which CIO + CRO sign, tabled as a Board item. The overview has no owner sign-off where the band is involved. | Complete the note (§5.5 recovery table). Point e7 at the recovery plan or contract, "STRUCTURAL_RECOVERY, glide path, extensions" (§5.5; §8.1; §10.1). Add owner → lab "SignOff where the band is involved" (§5.5; §10.1). |
| F-14 | low | room | e71 `decision_rights` → `board_owner` | A rule node is drawn as making a decision. Board and owner items go "IC recommendation plus minority report". | Add `ic_members` → `board_owner` [decision] "recommendation + minority report" and re-kind e71 as a guard (§8.1). |
| F-15 | low | engines | (missing) | The error ledger A1–A18 is absent; "error ledger" and "A17" occur nowhere. Only a note covers the consistency contract. §0.4 directs the CRO and MRM to §5.13, and §0.3 lists the error ledger in PA's base. | Add an MRM guard "error ledger A1–A18 + consistency contract (CI on fixtures, nightly on the book)" attached to `core_sim`, `phase2` and `ledger` (§5.13). |
| F-16 | low | overview (RA) | note 19 | "Real Assets working allocation, pending the user: $18bn … ~$4bn unfunded" lacks the SYNTHETIC label, unlike the capital_market note and the room `ra_head` tooltip. Real Assets notes after the first one in each view carry only a text citation, not the badge. | Prefix "SYNTHETIC working allocation (v2, pending the user)" (brief §8 rule 6; §9.5). Repeat the badge text on every Real Assets note. |
| F-17 | low | lab (RA) | `seat_narrators` | "Seat narrators ×12": the Real Assets narrator from brief §8 rule 1 appears only in the tooltip, with no visible badge. Everywhere else, groups get a badged Real Assets element. | Label "×12 (+1 Real Assets seat)" with the badge, or add a badged Real Assets narrator sub-node (brief §8 rule 1; §7.3; §8.5). |
| F-18 | low | engines; overview (RA) | engines e27, overview e86 | "income, capex calls, debt" (e27) and "flows; NR debt look-through" (e86), both drawn into the CF ledger, read as if non-recourse debt sat in Corporate Finance's ledger and facilities. | Relabel "net income, capex/development calls, NR debt service and refinancing (outside CF facilities)". Draw look-through leverage to the §4.10 leverage metrics (`funding`), not to the ledger (brief §8 rule 3; §4.10). |
| F-19 | low | room (RA) | `ra_block` detail | The detail lists "Q5 pacing by group" as generic over groups for Real Assets. Brief §8 rule 1's generic list is roll-ups, envelopes, FTP charges, attribution, the forecast registry and IC seats. A Real Assets pacing rule (η sign, corridor) is not defined in brief §8 or in §6.5. | Drop Q5, or mark it "pending Real Assets research" (brief §8 rule 1; §6.5). |
| F-20 | low | engines | `cards`, `lab_agents` | `cards` ("actions: cards, Γ") sits in the L6 Decide lane, but `actions` is an L3 module (§3.2; §3.4). `lab_agents` (kind agentic, "LLM roles via lab FSM") merges the deterministic meta-controller into an agentic node. | Label `cards` "cards (actions module, L3)" or move it to the L3 lane. Split `lab_agents` into a deterministic meta-controller and agentic roles (§3.3). |
| F-21 | low | overview | `core_tree` | `core_tree` has no input. Trees are built from ScenarioCubes on 6 × 2,000 pooled search-plane paths. This is the overview's only trace of §0.3 rule 3. | Add `scen` → `core_tree` "6 × 2,000 pooled search paths (M1–M6)" (§3.5 `build_tree`; §5.4; §4.1 Paths). |

## Per-view notes

### 1. Overview (66 nodes, 89 edges)

**Correct:**
- All §3.2 modules from L0 to L10 are present, plus `cli` and `mcp_server`.
- Owners match §3.4. That includes the less obvious ones: `cli` and `mcp_server` are owned by the IC secretariat, and `registry` by "MRM (forecast registry run by CRO office)", which reconciles §3.4 with §2.1.
- Every edge in the §3.2 and §2.4 diagrams is drawn with the right direction. This includes VOTE → Register (DecisionRecord) and VOTE → FBE (Brier).
- The external sources match §2.2.
- The TB1, TB3, TB4 and TB8 enclosures are right.

**Issues:** F-02, F-04, F-07, F-13, F-16, F-18, F-21.

### 2. Engines (45 nodes, 104 edges)

**Correct:**
- The one-kernel structure (`ledger` → P, H, T4′, Phase I).
- The Phase I → recovery mode → restored Phase II → duals → λ/FTP/envelopes chain.
- The pinned-dual guard on duals and cards.
- Column generation, Level B and Γ.
- `cfp_reading`, with readiness from SH_TP and the event stage from ledger indicators.
- The FBE-R t−1 feedbacks (SELL flags, envelope status).
- `c_h` → P certification and the sealed run.

Note on consent: e45 (`contract` → `phase1`) and e49 (`recovery_mode` → `contract`) form a loop. This matches §3.6: Phase I runs at the T−22 contract check, before signing.

**Issues:** F-01 (high), F-02, F-03, F-08, F-11, F-15, F-18, F-20.

### 3. Capital market (45 nodes, 94 edges)

**Correct and complete for §6:**
- decision prices versus published FTP (EWMA, ±50% collar) at tolerance and appetite;
- infeasibility prices on the Treasurer panel only;
- envelopes Λ_g per coupling row, and recovery envelopes B_rec = Λ_g + φ_g,t·g_t;
- pacing η signs (PE and Co-investment > 0; Secondaries and Capital Solutions < 0);
- the contingent-budget gate;
- the desk conflict controls, quote table and pricing committee;
- netting, with intra-ADIC flows counting zero;
- the services-ledger split;
- the transfer-pricing committee's 10-day SLA;
- consent scenarios R0x to R2, including owner band → R2 and signed revolver → R1.

**Issues:** F-05 (`proposal_intake`, `quote_table` owners), F-12, F-13.

### 4. Laboratory (84 nodes, 105 edges)

**Correct:**
- The §7.4 state machine is complete: all 19 states including ESCALATE and ABORTED, and every transition with its gate.
- The ABORTED causes: hash mismatch, seal breach and hard cap. The fourth cause, a human stop, has no edge (trivial).
- The §7.3 roles, with family, effort, tools, output and gate.
- The tool catalogue matches all 27 tools.
- The planes, Gate 2 and Gate 3 thresholds, budgets, memory rules, the 15 integrity drills, planted-effect calibration and the three LLMBackends.
- The seal commit-reveal.

**Issues:** F-05 (15 nodes), F-09, F-10, F-17.

### 5. Decision room (65 nodes, 93 edges)

**Correct:**
- Register Q1–Q10, A1–A9 and E1–E4, with increment-1 entries.
- `compile_agenda` → EvidencePlan → evaluator, and EVIDENCE MISSING.
- L0, L1 and L2 anatomy.
- The Θ bounds and seat parameters.
- The S0–S7 protocol and minority-report triggers.
- The H0–H6 order: the fact pack goes to H0, and H1 reveals in the right order.
- The agenda's 180 minutes and the consent agenda.
- W1–W3 latencies and KL flags.
- The DecisionRecord fields, signposts, politics tests and room evaluation.

Real Assets head, seat and block are badged.

**Issues:** F-03 (IC amendment → F), F-05 (24 nodes), F-06, F-14, F-19.

### 6. Quarterly cycle (20 nodes, 25 edges)

Every §3.6 row from T−28 to Monthly is present, with the right product, gate and state-machine state. Also present:

- the optional-campaign branch;
- salt commit at T−22 → seeds at T−12;
- the t−1 feedbacks into the T−23 freeze;
- A1–A9 in the Q4 cycle;
- the compressed event protocol.

No issues beyond the owner gaps in F-05, which are acceptable for cycle steps.

## §0.3 ten-rule coverage

| Rule | Shown? | Where | Gap |
|---|---|---|---|
| 1 One ledger kernel (P, H, T4′) | yes | overview e68–e70; engines e33–e36; consistency note | — |
| 2 One price, restored feasible H only | yes | engines `phase1` → `recovery_mode` → `phase2` → `duals_kernel`; `note_pinned_dual` guard | — |
| 3 Every banded world in H and search; pooled-observable tree | partly | `core_tree`, `plane_search` | per-class T6 rows in H (F-01); overview tree input (F-21) |
| 4 Safety first: Tier 1 lexicographic; T6 banded; P(10%) never maximized | **no** | notes only | **F-01** |
| 5 Owner's distribution exogenous (Mode B) | yes | `owner` "Mode B in DECISION runs"; `gate1` TR8; drill `test_no_payout_lever_in_mode_B`; capital-market `distributions` | — |
| 6 Readiness-Red is not event-Red | partly | engines `cfp_reading`, `note_readiness` | PHASE2_PLAN, event-only playbook path, overview (F-02) |
| 7 Integrity by infrastructure | yes | lab view (evaluator, counting, seal, rendered claims) | TB2 placement in overview (F-04) |
| 8 Humans own contract and vote | yes | SignOff, TB5, H0/H4 | countersignature misattributed (F-06) |
| 9 Offline first | yes | lab `backend_*`; overview note | — |
| 10 Synthetic labelled, sealed truth, parameter recovery | partly | TB7, `truth_store`, `synth` "gates V1–V24" | explicit validation flow (F-07) |

## Real Assets labelling audit

**Badged nodes (10), each with a visible badge in the SVG:**
- overview: `ra_head`, `ra_engine`, `group_taxonomy`;
- engines: `real_assets_engine`;
- capital_market: `g_real_assets`;
- lab: `ra_engine`;
- room: `ra_head`, `seat_ra`, `ra_block`;
- cycle: `c_ra`.

**Badged edges (26):** all carry the Real Assets halo and the badge in their tooltip.

**Content checked against brief §8:**
- rule 1: taxonomy as configuration, generic over groups, a shadow-IC seat;
- rule 2: closed-end funds on the PE-fund engine; income plus Geltner-smoothed NAV; capex and development calls; non-recourse debt with LTV, DSCR, maturity wall, refinancing risk and rate hedges; open-end redemption queue;
- rule 3: the action set;
- rule 4: marks;
- rule 5: oil wrong-way risk, the Gulf fiscal cycle, partial inflation pass-through;
- rule 6: the synthetic allocation;
- rule 7: interactions.

All are faithful. The schematic does not place Real Assets in places brief §8 leaves undefined: the §4.9 recourse tiers, Phase I-a reversible levers, the T4′ stress, the 60/10/10/10/10 commitment split, pacing η, c_buf credits or contingent budgets. That restraint is correct.

The Real Assets seat's θ and loss term are honestly marked "not yet set". The owner fields say "not yet assigned (brief §8 interim)", which is also correct.

**Problems:** F-16 (SYNTHETIC label and badge on notes), F-17 (seat narrators), F-18 (non-recourse debt drawn into the CF ledger), F-19 (inferred Q5 pacing).

## Method

1. Read ARCHITECTURE.md §0–§15 and brief §8 in full.
2. Dumped every view's lanes, groups, nodes, edges and notes from the model, and checked each item against the cited and the relevant sections.
3. Ran scripted checks:
   - every `§x.y`, `ADR-nn` and `§0.3 rule n` reference resolves to a heading in ARCHITECTURE.md, and every `brief §8 rule n` has n between 1 and 7 (no failures);
   - no dangling edges or attachments;
   - the only isolated nodes are the overview TB and rule notes;
   - a term-coverage scan, for example "lexicographic", "PHASE2_PLAN", "error ledger" and "parameter recovery", which returned zero hits;
   - SVG geometry of the overview enclosures;
   - a count of rendered "Owner: not stated" tooltips (52) and visible Real Assets badges (10).
