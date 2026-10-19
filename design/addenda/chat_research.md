# Conversational analyst (R16): research addendum

**Author:** research subagent (design workflow, R16). **Date:** 2026-10-18. **Status:** research input to `design/addenda/CHAT_ANALYST.md`; not binding.

**Tags:** [S] sourced (§9); [V] verified locally (bundled SDK docs v2.1.302; installed `anthropic` 1.15.0, `mcp` 2.3.0); [I] design inference. **Method:** web search ran out partway; later sources were fetched directly from primary pages; Consensus was not used; arXiv 2605.05409 is excluded (withdrawn by its author). Figures such as "37% [26–38%]" are ARCH format illustrations, not results.

## 0. Ten rules

1. The LLM picks tools and words; it never computes. Every number, difference and probability in an answer is a tool output rendered from a placeholder (P1, P7).
2. One deterministic analyst service owns every tool; MCP, `tpa chat` and the Ask panel are thin surfaces over it. Entitlements, walls and politics rules run in the service, never in prompts.
3. Answers are typed cards: statements with placeholders, a status equal to the weakest label of any number used, SYNTHETIC taint, and run links.
4. "Not in the artifacts" and "Ambiguous: which of these?" are valid answers. A new quantity triggers a run, never an estimate.
5. A what-if is drafted by the model, validated and back-translated by code, confirmed by a human in ADIC-controlled UI, and run on the exploration plane under its own run id.
6. Latency follows human limits: seconds for cached answers, under 1 s for W1, progress and cancel for W2, a run handle for W3.
7. A server-minted context handle pins as-of, contract, census, plane and data class.
8. Answers are short: number, range, labels and ICD-203 word first; uncertainty numeric; verification one click away.
9. The analyst holds private data and reads untrusted text, so it gets no exfiltration channel.
10. Every turn is logged, append-only and hash-chained.

## 1. How tool-using LLMs fail on analytics questions

### 1.1 Evidence [S]

| Finding | Value | Source |
|---|---|---|
| Consistency | GPT-4o-class agents solved under 50% of τ-bench tasks; pass^8 was under 25% in retail. pass^k (all k trials succeed) fits a system that users re-ask | [1] Jun 2024 |
| Function calling | Single-turn calls are largely solved; memory, dynamic decisions and long horizons remain open | [2] ICML 2025 |
| Benchmark quality | 24 of 50 sampled BFCL v4 tasks (48%) had defects that could affect accuracy | [3] Sep 2026 |
| Conversation | Insufficient information, state dependency and canonicalization are hardest. Models are weak at deciding *not* to call a tool, or to ask a follow-up instead | [4] Aug 2024; [5] NAACL 2025 |
| Multi-turn | Performance drops 39% on average in underspecified multi-turn chat. Models assume early, then over-rely on the assumption | [6] May 2025 |
| Text-to-SQL | Spider 2.0 21.3%, against Spider 1.0 91.2% and BIRD 73.0%. The valid readings of ambiguous questions go unsurfaced | [7] ICLR 2025; [8] EMNLP 2023 |
| Semantic layer | GPT-4 scored 16% over raw SQL, against 54% over a knowledge-graph layer | [9] Nov 2023 |
| Finance QA | FinQA: 61.24% vs experts' 91.16%. TAT-QA: 58.0 vs 90.8 F1. GPT-4-Turbo with retrieval was wrong or refused on 81% of FinanceBench | [10][11] 2021; [12] Nov 2023 |
| Offloading arithmetic | Program-of-Thoughts beat chain-of-thought by about 12%, including on FinQA, ConvFinQA and TAT-QA. A library of 3,133 Python functions lifted GPT-4o from 83.2% to 91.6%. Numerical precision remains weak; the best model scored 53.0% on FinMMR-hard | [13] TMLR 2023; [14] ACL 2025; [15] ICCV 2025 |
| Tool bypass | Models simulate a tool's output instead of calling the tool, escaping audit controls | [16] Jan 2026 |

**Reading [I].** Error falls when the model selects among governed, typed operations and code does the arithmetic, but entity resolution, ambiguity, missing inputs and drift remain. Public leaderboards are not acceptance evidence.

### 1.2 Error modes and controls [I]

| Error mode | ADIC example | Control |
|---|---|---|
| Entity mis-resolution | "Fund VII" exists under three GPs; "PE" may mean the group or the asset class | `resolve` returns ranked canonical ids; ambiguity gets a choice, never a guess |
| Invented arguments | Horizon, plane or census filled in silently | No silent defaults for semantic choices; any default is echoed in the card |
| Arithmetic or tool bypass | "Forecast minus actual"; IRR converted to MOIC | `compare`/`diff` tools. The validator rejects literal digits and references not fetched in this turn |
| Misread output | Since-inception IRR read as a forward belief; planes mixed | Outputs carry unit, basis and plane; the renderer formats them |
| Multi-turn drift | A run cited from an earlier as-of | References must belong to the context handle |
| Overconfident "why" | A speculative story for a SELL card | Every statement is typed as model output, agent judgment or assumption (ICD 203 Std 3) |
| Capitulation | "That can't be right" | Numbers never change under pushback; the reply is provenance or a what-if |

### 1.3 Evaluation [I]

**Golden set.** At least 300 items on SYN-ADIC-177, spanning every role and group, the five R16 question types (explanation, drill-down, probability, comparison, what-if), and ambiguous, unanswerable, out-of-entitlement, injection-bearing and pushback items.

**Metrics:** 100% numeric exactness; citation resolution; label and taint correctness; correct denials; override-translation pass^3 ≥ 0.9 (ARCH §7.10); answer invariance across paraphrases and roles; unjustified flip rate below 10% (D14 §6.8); latency per tier.

**Regression.** Replay cassettes run in CI. Re-qualify on any model, prompt or tool change (P10; S-ADR-18).

## 2. Grounding: numbers are rendered, never written

### Evidence [S]

- **Citation gaps.** In ALCE, even the best models lacked complete citation support 50% of the time on ELI5 [17].
- **Vendor guidance.** Anthropic advises permitting "I don't know", citing sources, and retracting unsupported claims [18].
- **Verified queries.** Snowflake grounds answers in verified question–SQL pairs carrying `verified_by`/`verified_at`, and reports when one was used [20].
- **Native citations.** Claude's search-result blocks return citations with `cited_text`. They cannot be combined with structured outputs, and a tool result that uses them must contain only search results [19][31].
- **Resolves vs supports.** Resolution can be checked deterministically; support needs an audit (P7).

### Design [I]

- **AnswerCard** (`contracts.claims`) fields: `context_id`; `statements[]` as `{text, kind ∈ {model_output, agent_judgment, assumption}, refs[]}`; `status`; `data_class`; run links; `not_answered[]`.
- **Placeholders:**
  - `{{m:<metric_id>@<run_id>|fmt}}` for metric values;
  - `{{a:<run_id>:<artifact>:<json-pointer>|fmt}}` for artifact values;
  - `{{q:<artifact_ref>}}` for verbatim quotes (minority reports, assumption log).

  The renderer adds unit, CI, model range, ICD-203 word, plane and footer.
- **Validator** (extends ARCH §10.6). It rejects literal digits; references not fetched in this turn under this `context_id` (which defeats tool bypass [16]); improvement verbs on non-QUALIFIED results or within 2 paired SE; probabilities without ranges; and synthetic numbers attributed to ADIC. The model gets one retry. If that fails, the user sees a deterministic fact card without prose.
- **Status lattice:** QUALIFIED > SEALED NOT_QUALIFIED/NOT_ASSESSED > SEARCH > EXPLORATORY. An answer takes the lowest label it uses, the way SYNTHETIC taint propagates (ARCH §9.5).
- **Submission.** The answer is a strict `submit_answer` call validated by Pydantic (ARCH §7.3). Quotes go through `{{q:}}`, so the Ask path needs no API citations.
- **Data semantics (brief §9).** Marks are since-inception IRR or MOIC, net, with cases read as nominal P10/P50/P90. They are shown as history, with IRR labelled sunk, beside the FBE forward belief. Point-in-time questions pass `as_of` and `recorded_at`. Credibility appears as information value in $ and is hidden below n_eff = 20 (ARCH §8.10).

## 3. What-ifs: words → typed override → effective change → confirmation

**Evidence [S].**
- An interface that lets users fix a generated query by editing its step-by-step explanation outperformed state-of-the-art baselines; it was also evaluated in a 24-participant user study [21].
- Ambiguous requests have several valid formalizations that models miss [8]. Models also guess instead of asking [4][5].
- Human–AI guidelines call for efficient correction and for conveying the consequences of user actions (G9, G16) [22].
- Confirmation fatigue weakens security [23].

**Pipeline [I]** (ARCH §8.7 made concrete):
1. **Propose.** The model calls one strict proposal tool per override kind: `propose_belief_view`, `propose_scenario_view` or `propose_lever_change`. Proposals have no side effects. There is no polymorphic root schema, because Claude Code flattens a root-level `anyOf` [28].
2. **Validate.** The service checks bounds in Pydantic, because strict schemas do not enforce `minimum`/`maximum` server-side [31]. It returns `override_id` and `spec_hash`; a plain-language back-translation; the effective view after shrinkage (at c = 0.6, "30% below base" becomes 18%); KL and ESS flags; what will be recomputed; and the latency tier.
3. **Confirm.** The user accepts, edits or declines, mirroring MCP elicitation's accept/decline/cancel [25].
4. **Run.** `run_whatif(override_id, spec_hash)` runs on the exploration plane under its own run id, labelled EXPLORATORY. It appends the view to the view ledger under the member's name. Tokens are single-use and expire.
5. **Promote.** A W1 number that enters the decision log is recomputed in Python. An irreversible Tier-A action needs a sealed confirmatory run.

**Where confirmation lives.**
- **`tpa chat` and Ask:** inside the tool function, which returns a "user declined" result as the SDK documents [31].
- **Claude Code:** `_meta["anthropic/requiresUserInteraction"]: true` prompts on every call, even in bypass modes [28].
- **Attested vs confirmed.** An Agent-SDK callback can still approve that prompt, and an Elicitation hook can answer elicitations without showing a dialog [28]. MCP confirmations are therefore logged as *client-attested*; only ADIC-surface confirmations count as human-confirmed.

**Latency [S][I].** At 0.1 s a response feels instantaneous; at 1 s the user's flow holds. Beyond 10 s users need percent-done progress and a way to interrupt [24].

| Mode | Target | Chat behaviour |
|---|---|---|
| Ask on cached artifacts | Seconds | Stream the card |
| W1 entropy pooling | < 1 s | Inline |
| W2 re-fusion and H | ≤ 60 s | Progress and cancel; the user can keep chatting |
| W3 re-simulation | Minutes to overnight | Return a run handle; notify on completion |

**Long runs.** MCP 2026-07-28 moved tasks into an extension; servers that need cross-call state now keep it in server-minted handles passed as ordinary tool arguments [27]. The installed `mcp` 2.3.0 has task types but no implementation [V]. So `run_whatif` returns a handle, polled with `get_run(handle)`, which closes ARCH §11.3's open item.

## 4. Surfaces, MCP and SDK

### 4.1 One service, three surfaces

- **`tpa chat` and Ask** run ADIC's own loop. Final text passes the renderer, validator and linters, so these surfaces are **decision-grade**.
- **Claude Code or Desktop via MCP.** The client's model writes the prose and ADIC cannot validate it [I]. Tool results are therefore self-contained rendered cards (text + `structuredContent` + `outputSchema`), the tool-call log is the record, and the surface is labelled "analyst exploration, not for the decision record".
- **Parity.** `tpa chat` can consume the same server through `anthropic.lib.tools.mcp.async_mcp_tool`, which imports in the venv [V].
- **Offline (P12).** Stub mode is a deterministic slash grammar (`/metric`, `/holding`, `/compare`, `/whatif`) over the same tools and cards; only narrative is lost. Replay drives CI.

### 4.2 MCP design

| Topic | Practice | Source |
|---|---|---|
| Primitives | **Resources** (application-controlled), `@`-mentionable in Claude Code: `tpa://context/{id}`, `tpa://glossary/{term}`, `tpa://run/{id}/manifest`, `tpa://pack/{quarter}/l0`. **Prompts** (user-controlled): `ask`, `explain_card`, `whatif` | [25][28] |
| Tools | Few, consolidated, semantically named: `resolve`, `list_metrics`, `get_metric`, `get_holding`; `explain_card` (binding constraints, shadow prices, flip thresholds); `compare` (controls, archetypes and DEFER as paired CRN deltas); `get_provenance`, `get_quote`; three `propose_*` tools, `run_whatif`, `get_run`, `validate_answer` | [29][30] |
| Typing | `outputSchema`, which servers MUST conform to, plus the same JSON serialized as text | [25] |
| Annotations | `readOnlyHint` on read tools. Clients MUST treat annotations as untrusted, so enforcement stays server-side | [25] |
| Errors | `isError` results with actionable codes: `AMBIGUOUS_ENTITY` (with candidates), `ENTITLEMENT_DENIED`, `EVIDENCE_MISSING` | [25][29] |
| Duties | Validate inputs, enforce access control, rate-limit, sanitize outputs, log tool use | [25] |
| State | The protocol is stateless: pass `context_id` and handles as arguments, keep `tools/list` order deterministic, and carry trace context in `_meta` | [27] |
| Size | Claude Code warns above 10k tokens, caps at 25k, and moves results over 50k characters to a file. Default to `detail="concise"` and paginate | [28][29] |
| Transport | Local servers SHOULD use stdio; over HTTP, require a token or restricted IPC | [26] |
| Installed SDK | `MCPServer.tool(annotations=…, structured_output=…)`, `ctx.elicit`, protocol versions up to 2026-07-28 | [V] |

### 4.3 SDK pattern for `tpa chat` [V unless marked]

- **Runner.** Call `client.beta.messages.tool_runner(model="claude-opus-5-5", tools=[…], output_config={"effort": …}, max_iterations=…)` with `@beta_tool(strict=True, input_schema=<PydanticModel>)`. Anthropic 1.15.0 has both parameters, plus the hooks `set_messages_params`, `append_messages`, `generate_tool_call_response` and `until_done`.
- **Tool choice.** `tool_choice` stays `auto`, because forcing a tool returns a 400 on Opus 5.5. If a numeric question gets no tool call, re-prompt once [31].
- **Model settings.** Thinking is always on, so set effort explicitly. Send no sampling parameters and no prefill, and pass thinking blocks back unchanged. Before running tools, check `stop_reason` for `refusal`, and for `max_tokens` with a pending `tool_use` [31].
- **Replay.** Either a replay transport behind `DefaultHttpxClient` (unverified; WP-25 spike), or the documented manual loop, which the docs allow for custom transports [31].
- **Compaction** (beta). It summarizes the conversation server-side and can drop labels and run ids. It is never the record: keep sessions short and re-fetch [31][I].
- **Mid-conversation `system` messages** are model-gated; verify them on Opus 5.5 before use [31].

## 5. Human factors: designing against over-reliance

**Evidence [S].**
- On decision tasks, human–AI teams underperform the better of the two (g = −0.27). Explanations raise acceptance regardless of correctness, and deciding before seeing the AI helps [D14 §2.6].
- In a field experiment with 758 BCG consultants, those using GPT-4 on a task beyond its frontier were right 60–70% of the time, against 84% without AI [32].
- Explanations curb over-reliance when they make verifying the AI cheaper [33].
- Longer explanations raised confidence but not accuracy. Explanations tailored to the model's confidence narrowed the calibration and discrimination gaps [34].
- First-person hedges reduced over-reliance and improved accuracy (N = 404) [35].
- Models rarely hedge, and 47% of their confident answers were wrong. Users relied on answers regardless, and human preference data penalize uncertainty [36].
- Printing numeric ranges inline beside verbal probabilities lifted agreement with the ICD-203 scale to 66%, against 32% in the control group. Tooltips did not help [37].
- NIST names automation bias and over-reliance (under "Human-AI Configuration"), and defines confabulation as "confidently stated but erroneous" content [38].
- Project literature: lead with authentic dissent and aim the AI devil's advocate at the AI's own recommendation [LIT §3.12]; track decision accuracy and under-reliance, show evidence first, audit retrieval, add a conviction band [LIT §4.15]; order humans first, never optimize for persuasion, keep agents blind to authority [D14 §6.10].

**Design [I].**
1. **Answer shape.** Open with the line "P(red) 37% [26–38%] ± 0.2pp (*likely*; EXPLORATORY; SYNTHETIC)". Follow with at most three sentences, under a length cap. Close with "what this does not tell you": model range, NOT_QUALIFIED status, data gaps.
2. **Uncertainty.** Model uncertainty is stated numerically, never in words alone. The analyst states its own uncertainty about the question in the first person ("I am not sure which Fund VII you mean").
3. **Cheap verification.** Each card shows its inputs (as-of, hashes, census, plane), a one-click manifest link, the flip threshold (P14), and the controls and archetypes on CRN (P6). Differences below 2 paired SE render as "not distinguishable".
4. **Pushback.** A challenge gets provenance or a what-if, never a changed number. The LLM sees no identity or seniority, so a CIO and an analyst get the same answer apart from redaction. Flip rates are tested.
5. **Pre-vote integrity.** Between pack publication and the H0 lock, Ask on Tier-A items serves facts only: no agent judgment, seat arguments or minority reports. Members' questions stay private until the lock (ARCH §8.6).
6. **"Why SELL?"** Show binding constraints, shadow prices and the strongest counter-case, with authentic minority reports first. Use a plain register; never tune on adoption.
7. **KPIs.** Track reliance split by whether the model was right, under-reliance, and override accuracy. Run seeded-error drills in training and shadow sessions only.

## 6. Security, entitlements, audit

### 6.1 Prompt injection

- **Untrusted text.** Forecast rationales, memos, GP notices and even minority-report text are untrusted. LLM applications "blur the line between data and instructions" [39].
- **OWASP 2025** says it is unclear whether fool-proof prevention exists. It prescribes least privilege, deterministic output checks, segregation of external content and human approval for high-risk actions [40].
- **The lethal trifecta.** Private data and untrusted text are two of its three legs [41]. Remove the third, external communication: no web, e-mail or file-write tools; a CSP that blocks remote images, closing markdown-image exfiltration; and no external links in Ask.
- **Patterns** [23]: an action-selector over a fixed tool set; plan-then-execute; context minimization, with quotes rendered via `{{q:}}` instead of read by the model; and human confirmation for every run.
- **Cost of provable designs.** On AgentDojo, CaMeL's provably secure design solved 77% of tasks, against 84% undefended [42]. The analyst's tiny action space makes that cost acceptable.
- **MCP attacks.** Tool poisoning, rug pulls and cross-server shadowing let one server exfiltrate data through another [43]. With real data, run the analyst in a dedicated Claude Code profile with a managed MCP allowlist and no other servers [28].

### 6.2 Entitlements and MNPI walls

- **Code, not prompts.** Each role (IC member, CIO, CRO, Treasurer, group head, analyst, operator, MRM, compliance) maps to entitlements: groups visible at holding level, aggregation floors, planes, what-if rights and transcript access. Entitlements are checked in code on every call [40].
- **Identity.** On stdio, the Windows account plus a signed role map. Ask binds to 127.0.0.1 and checks a per-launch token and the Host and Origin headers [26].
- **Walls.** A Chinese wall withholds information held in one part of a business from another part (FCA SYSC 10.2) [45].
  - Private Credit, Capital Solutions, Co-investment and the direct books of Secondaries and Real Assets may hold MNPI on issuers that Public Markets and the opportunistic overlay trade [I].
  - Rules: wall tags on rows and fields; restricted-list checks before any issuer-level fact reaches a public-side role; uniform denials that do not reveal whether the data exist; aggregates only above a minimum cell size; separate sessions, caches and transcripts per wall.
  - Walled data never enter a public-side context, because a model cannot be trusted to withhold what it has read.
- **The Copilot lesson.** Permission-inheriting assistants surface whatever entitlements allow. Microsoft's own blueprint starts with "remediate oversharing" [44]. Audit entitlements before launch.
- **Politics rules at chat time** (ARCH §8.10): no league tables; credibility hidden below n_eff = 20; information value, not bias labels; a group's own FTP charges itemized, peers' only in aggregate.
- **Confidentiality (P13).** Claude Code and Desktop send tool results to the model provider, so every MCP client is an egress path. Under REAL data, MCP outputs follow the gateway redaction policy until in-region serving is approved (Q6).

### 6.3 Logging and audit

- **Per turn, log:** user, role, entitlement version, surface, `context_id` and question; tool calls with arguments, result hashes and run ids; model id, `_request_id`, prompt and tool-list hashes, effort and `stop_reason`; the rendered card and its verdicts; confirmations (who, when, `spec_hash`, attested or confirmed); and denials.
- **Storage and tracing.** Logs are append-only and hash-chained in the registry. OpenTelemetry GenAI spans [48] use MCP trace context to link turn → tool → run [27]. Stub and Replay sessions are marked.
- **Benchmarks, not law.** EU AI Act Art. 12 requires lifetime logging (Annex III systems from 2 Dec 2027), and Art. 26(6) requires logs kept for at least 6 months [46]. The SEC's $392.75m in penalties on 26 firms (14 Aug 2024) for unpreserved off-channel messages shows that communications are records [47].
- **Access.** Only the user, compliance and MRM may read transcripts; transparency can chill dissent (ARCH §8.9).

## 7. Implications for CHAT_ANALYST.md and BUILD_SPEC [I]

1. **`contracts.claims`:** `AnswerCard`, `Statement`, the status lattice, the placeholder grammar (`m`, `a`, `q`) and `context_id`.
2. **`claims.validator`:** same-turn reference binding, the min-label rule, 2-SE greying, and the entitlement, wall and politics linters.
3. **Analyst service:** the §4.2 catalogue, with one strict proposal tool per override kind.
4. **Proposal tokens** (`override_id`, `spec_hash`, TTL, single use), `requiresUserInteraction` on `run_whatif`, and the attested-vs-confirmed distinction.
5. **Run handles** for W2 and W3. Adopt the MCP tasks extension only when clients support it.
6. **`tpa chat`** on the tool runner, with a Replay transport spike (manual-loop fallback) and the Stub slash grammar.
7. **Ask panel:** a localhost stdlib server with token, CSP and a facts-only pre-vote mode.
8. **Tests:** the `tests/room/chat` golden suite (§1.3), with re-qualification on every change.
9. **Signed configuration:** wall map, restricted list, aggregation floors and role map.
10. **Audit plumbing:** transcript store, retention policy and OTel spans.

## 8. Open questions for the user

1. Is the MCP surface open to IC members, or only to analysts and operators (ARCH §2.1)?
2. Which groups are private-side, and what is the restricted-list source?
3. How long are transcripts retained, and who may read them?
4. Is Ask allowed during the pre-vote window, and in which mode?
5. May a chat what-if be cited in a brief? Proposed: only after a Python recompute and, for Tier-A items, a sealed confirmatory run.

## 9. References (accessed 2026-10-18)

**Project.** [D14] `research/dossiers/14_ic_deliberation.md`; [LIT] `research/literature/00_LITERATURE_SYNTHESIS.md`; ARCH = `design/ARCHITECTURE.md`; brief = `design/00_DESIGN_BRIEF.md`.

1. Yao et al., τ-bench, arXiv 2406.12045, 17 Jun 2024.
2. Patil et al., BFCL, ICML 2025 (PMLR 267).
3. Epoch AI, BFCL benchmark review, 10 Sep 2026.
4. Apple, ToolSandbox, arXiv 2408.04682, Aug 2024.
5. Ross et al., When2Call, NAACL 2025.
6. Laban et al., "LLMs Get Lost in Multi-Turn Conversation," arXiv 2505.06120, May 2025.
7. Spider 2.0, arXiv 2411.07763, ICLR 2025.
8. Bhaskar et al., AmbiQT, EMNLP 2023.
9. Sequeda, Allemang, Jacob, arXiv 2311.07509, Nov 2023.
10. Chen et al., FinQA, EMNLP 2021.
11. Zhu et al., TAT-QA, ACL 2021.
12. Islam et al., FinanceBench, arXiv 2311.11944, Nov 2023.
13. Chen et al., Program of Thoughts, TMLR 2023.
14. FinanceReasoning, ACL 2025 (arXiv 2506.05828).
15. FinMMR, ICCV 2025 (arXiv 2508.04625).
16. Healy et al., hallucinations in agent tool selection, arXiv 2601.05214, Jan 2026.
17. Gao et al., ALCE, EMNLP 2023.
18. Anthropic docs, "Reduce hallucinations."
19. Anthropic docs, "Search results."
20. Snowflake docs, "Cortex Analyst Verified Query Repository."
21. Tian et al., editable step-by-step text-to-SQL explanations, EMNLP 2023.
22. Amershi et al., "Guidelines for Human-AI Interaction," CHI 2019.
23. Beurer-Kellner et al., prompt-injection design patterns, arXiv 2506.08837, Jun 2025.
24. Nielsen, "Response Times: The 3 Important Limits," 1993/2014.
25. MCP specification 2025-06-18: Server overview, Tools, Elicitation.
26. MCP specification 2025-11-25: Tasks; Security Best Practices.
27. MCP specification 2026-07-28: Key changes.
28. Claude Code docs, MCP (code.claude.com/docs/en/mcp).
29. Anthropic Engineering, "Writing effective tools for agents," 11 Sep 2025.
30. Anthropic Engineering, "Building effective agents," 19 Dec 2024.
31. Bundled claude-api skill v2.1.302 (Python README, tool-use; shared concepts, agent design).
32. Dell'Acqua et al., HBS WP 24-013, Sep 2023 (figures via co-author E. Mollick, 16 Sep 2023).
33. Vasconcelos et al., CSCW 2023.
34. Steyvers et al., *Nature Machine Intelligence* 2025 (arXiv 2401.13835).
35. Kim et al., FAccT 2024.
36. Zhou et al., "Relying on the Unreliable," ACL 2024.
37. Wintle et al., *PLOS ONE*, 17 Apr 2019.
38. NIST AI 600-1, 26 Jul 2024.
39. Greshake et al., arXiv 2302.12173, Feb 2023.
40. OWASP, LLM01:2025 Prompt Injection.
41. Willison, "The lethal trifecta," 16 Jun 2025.
42. Debenedetti et al., CaMeL, arXiv 2503.18813, Mar 2025.
43. Invariant Labs, "Tool Poisoning Attacks," 1 Apr 2025.
44. Microsoft Learn, Copilot privacy and security (2026-10-08); oversharing blueprint (2026-05-06).
45. FCA Handbook, SYSC 10.2.
46. EU AI Act, Arts. 12 and 26.
47. SEC Press Release 2024-98, 14 Aug 2024.
48. OpenTelemetry GenAI semantic conventions (github.com/open-telemetry/semantic-conventions-genai).
