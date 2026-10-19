# Chat with the model (R16): inventory of the current design and its gaps

**Date:** 2026-10-18 · **Author:** design workflow (chat inventory step) · **Status:** input to `design/addenda/CHAT_ANALYST.md`; not binding.

**Sources**
- Brief §1 (R16), §2 and §9.
- `design/ARCHITECTURE.md` v1.0. Bare § numbers refer to it.
- `design/BUILD_SPEC.md` ("BS"), as on disk at 18:33. It covers only §0–§2 and predates R16, which was added to the brief at 18:35.
- The SDK `README.md` and `tool-use.md`.

§4 was checked against the installed `anthropic` 1.15.0 and `mcp` 2.3.0 source. Code-font names exist in ARCH or BS; **(new)** marks a proposal.

## 1. Bottom line

The design already has the parts of a grounded analyst (§2):
- the Ask, W1, W2 and W3 modes;
- a Translator and a Q&A Answerer;
- claims rendered from placeholders, checked by a validator that rejects stray digits;
- run links;
- a read-only analyst MCP server;
- Stub and Replay backends.

It has no conversation:
1. **No chat surface.** There is no `tpa chat`, and the pack is static with no Ask backend. The analyst server serves "an operator's MCP client" (§11.3), and operators decide nothing about the portfolio (§2.1).
2. **Thin tools.** Explanation and drill-down tools sit in lab allowlists or nowhere. The Q&A Answerer has only `get_metric`, `get_provenance` and `answer_grounded`.
3. **No principal model.** Visibility and politics rules live in the pack linter and tests (§8.4, §8.10), not at a tool layer.
4. **No chat infrastructure.** There is no session, transcript record, budget, clarification policy or evaluation set.
5. **Claude Code and Desktop bypass the guardrails.** A client-side model writes the answer, outside the gateway (TB3), redaction (§9.7) and the validator (§10.6).

## 2. What the design already provides

### 2.1 Modes (§8.7; ADR-23)

| Mode | Engine path | Latency | Label |
|---|---|---|---|
| Ask | Registry reads citing `run_id:artifact:path`; "not in the artifacts" is valid | Seconds | Per statement: model output / agent judgment / assumption |
| W1 | Entropy pooling in the pack (`pack/static/ep.js`, disabled if its golden self-test is off by > 10⁻⁶); Python twin behind `ep_condition` (§4.12) | < 1 s (B4) | EXPLORATORY |
| W2 | Re-fusion and H at what-if size on cached CRN paths (`optimize_h`, `price_actions`) | ≤ 60 s (B6) | EXPLORATORY |
| W3 | Re-simulation with a tilted sampler; handle polled by `get_run_status` (§11.3) | Minutes to overnight | Confirmatory only on the sealed plane |

**Inherited rules**
- The Translator maps asset-return and lever views to FBE ViewSpecs, and scenario, cash-flow and regime views to entropy-pooling ViewSpecs.
- The member confirms the *effective* view after shrinkage. Gates: KL flags at 0.05 / 0.25 / 1.20 / 2.30 nats (red forces W3); Kish ESS ≥ 5,000; weight ratio ≤ 50.
- Logged W1 numbers are recomputed in Python.
- An irreversible Tier-A action on exploratory evidence needs a sealed confirmatory run.
- No surrogate numbers.
- What-ifs run on the exploration plane (fresh keys, ≤ 10k paths; §7.5).

### 2.2 Roles (§7.3)

| Role | Family, effort | Tools | Gate |
|---|---|---|---|
| Q&A Answerer | A, medium | `get_metric`, `get_provenance`, `answer_grounded` | Claim validator |
| Translator | A, medium | `draft_viewspec`, `draft_scenariospec`, `ep_condition` | Human confirms the effective view |
| Memo / Brief Writer | A, high | `list_metrics`, `get_metric`, `get_provenance`, `draft_memo`, `validate_claims` | G7 |
| Auditor | B, high | `read_ledger`, `read_run_logs`, `read_engine_diff`, `read_rendered_memo`, `read_bundles` | G8 ("supports") |
| AI Validator | B, medium | `read_pack`, `read_registry` | Pack gate |
| Facilitator | A, medium | Protocol state only; introduces no claims | — |

**Admission tests (§7.10):** translator pass³ ≥ 0.9; sycophancy < 10% unjustified flips; auditor ≥ 90% recall on seeded errors.

**Validation and prompts:** each role ends with a `submit_<artifact>` tool. The meta-controller re-validates it, with ≤ 3 retries. Prompts are hashed in `llm_policy` (§7.3).

**Gap:** §11.7 gives the Q&A Answerer no materiality tier.

### 2.3 Tools

**Evaluator catalogue (§7.3).** Strict schemas with `additionalProperties: false`:
`state_snapshot`, `phase1_restore`, `optimize_h`, `price_actions`, `evaluate_policy`, `evaluate_scenario`, `implied_actions`, `ep_condition`, `evsi_crossfit`, `flip_thresholds`, `robustness_card`, `bridge_card`, `group_envelopes`, `overlay_offset_card`, `attribute`, `price_trade`, `crif_sensitivities`, `simm_like`, `greek_offsets`, `hybrid_quote_check`, `get_metric`, `list_metrics`, `get_provenance`, `validate_claims`, `register_forecast`, `log_assumption`, `escalate`.
- Writes: `register_forecast`, `log_assumption`, `escalate`.
- `evaluate_policy` is counted.

**Lab-only reads a chat needs:** `get_state_card`, `read_state_card`, `get_price_table`, `get_cards`, `get_evidence_slice`, `get_exploration_result`, `read_pack`, `read_registry`, `read_ledger`, `read_run_logs`.

**Analyst server (§11.3):** `get_metric`, `list_metrics`, `get_provenance`, "pack queries", "W2 what-ifs" (EXPLORATORY), `get_run_status`.
- It has no final plane, no sealed truth, and no write path to engines, beliefs or scenarios.
- The two quoted families are unnamed and unspecified.
- `mcp_server.py` (WP-29, BS §2) has no contract yet, because BS §3–§4 are unwritten.

### 2.4 Grounding: renderer, validator, registry, run links

**Renderer.** `{{m:<metric_id>|<format>}}` is filled with value, unit, plane label, CI, model range and ICD-203 word (§10.6; ADR-20; BS `claims/`).

**The validator rejects:**
- literal digits outside a whitelist (dates, section numbers);
- unknown or wrong-plane metrics;
- improvement verbs on NOT_QUALIFIED or NOT_ASSESSED results, or within MC error;
- probabilities without a range;
- citations to memory;
- synthetic numbers attributed to ADIC;
- coverage below 1.

**Registry**
- Metric instances: `(metric_id, run_id, value, unit, plane, CI, model range, MC error, scenario hash)` (§10.3).
- IDs: `tier1.t6.cp_upper@v1`, `run-<UTC>-<hash8>`, `<run_id>:<artifact>:<json-pointer>` (BS §1.8).
- `RunManifest` holds every hash. For each LLM call it records the model, prompt and response hashes, tokens, cost and any fallback (§10.2).
- The registry is append-only and hash-chained.

**Pack**
- Every number is ≤ 2 clicks from its manifest (§8.4).
- "EVIDENCE MISSING: ⟨metric⟩" is never filled silently (§8.2).

### 2.5 Labels

- **Plane:** SEALED / SEARCH / EXPLORATORY (§8.4).
- **Gate 3:** QUALIFIED / NOT_QUALIFIED / NOT_CORRECT / NOT_ASSESSED (§7.6).
- **Statement labels** (§8.7).
- **Probabilities:** central [model range] ± MC error, with scenario hash and ICD-203 word. They are greyed when |Δ| < 2 paired SE. P(10%) and bPOE sit beside P(red) (§8.4; S-ADR-07).
- **Synthetic data:** "SYNTHETIC – NOT ADIC DATA" on every output derived from it, CLI summaries included (§9.5; BS §1.12).
- **Other labels:** "agent judgment" (§3.3); "correlated" (§7.10); "at a kink", "selection not certified" and `priced_on` (§4.8).

### 2.6 Decision rights and boundaries

- LLMs draft view translations and Q&A text; humans confirm, vote and sign (§3.3).
- Only authenticated humans create `SignOff` objects, and AI seats never vote (TB5, §8.5).
- Decision tiers are A/B/C/Board, with symmetric irreversibility and software recusal (§8.1).
- Only MRM validation jobs can read the sealed truth (TB8).
- Nothing self-executes (ADR-32).

### 2.7 Politics and room rules that bind chat

- **§8.10:** `test_information_value_not_bias_label`, `test_credibility_hidden_below_neff_20` and `test_no_league_table`. WIS scoring is symmetric, envelopes are invariant to forecasts, and groups have a contest route. Each head sees its own itemized charges and peers' charges only in aggregate (§6.9).
- **§8.5:** seats are named by mandate (`test_no_named_person_regret_in_pack`). Seat numbers come only from `implied_actions`.
- **§6.6, §4.8:** desks sit behind information barriers, conflicted quotes need a second source, and no MNPI moves between groups.
- **§8.6:** H0 is a blind pre-vote on the fact pack, with no AI narrative, seat map or minority reports. The pack is published at T−7; the pre-vote locks at T−1.
- **§8.9:** verbatim transcripts are "a separate, restricted choice".
- **§8.11:** no persuasion optimization or personalization.

### 2.8 Offline backends and LLM configuration

**Backends (§7.13; BS `agents/backends/`).** `LLMBackend` has three implementations, chosen by `TPA_LLM_MODE ∈ {offline, replay, live}` (§11.1):
- `AnthropicBackend`;
- `ReplayBackend`, keyed by the SHA-256 of the canonical request; it fails closed with `REPLAY_MISS` (BS §1.10);
- `StubBackend`, which is seeded, schema-valid and rule-based.

**Calls (§11.2; S-ADR-23).** Calls use `client.beta.messages.parse(..., output_format=Model, betas=["server-side-fallback-2026-07-01"], fallbacks="default")`, with:
- explicit effort;
- strict tools, with `tool_choice` on auto;
- no sampling parameters or prefill;
- append-only transcripts that preserve thinking blocks;
- refusal checks;
- prefix caching.

### 2.9 CLI (§11.4)

`tpa data freeze` · `tpa synth build` · `tpa scen build` · `tpa state snapshot` · `tpa run quarter` · `tpa phase1` · `tpa h solve --preset {whatif,...}` · `tpa p certify` · `tpa evaluator serve --plane {search,final}` · `tpa seal {commit,run,reveal}` · `tpa lab start|status|escalations` · `tpa room compile|pack|prevote|record` · `tpa mcp serve` · `tpa bench` · `tpa audit labels`.

None of these is conversational. `tpa mcp serve` does not say which of the two servers it starts, and there is no `--plane exploration`.

## 3. Gaps for R16

### 3.1 Explanation and drill-down tools

| R16 question | Engine source | Exposed today | Proposed tool **(new)** |
|---|---|---|---|
| "Why is this fund a SELL?" | Decision card (§4.8): reduced cost, dual interval, P(best), regret, LAPV waterfall, flip thresholds, belief card, `priced_on`, Γ | `get_cards` (ideators), `flip_thresholds` (lab) | `explain_card(holding_id, run_id)`, carrying every P14 field or rejected (§1.2) |
| Binding constraints, shadow prices | `HSolution` duals with one-sided intervals; RHS ranging (§5.6); λ by binding row (S-ADR-16); KKT interlock (§4.13) | `get_price_table` (ideators) | `binding_constraints(scope, run_id)`, `lambda_curve(run_id)` |
| Three marks, forecast credibility | `mark`, `forecast`, `milestone`; belief card (raw vs fused, market anchor, F1–F10, Zombie-NAV, catalyst, P(achieved ≤ k)); κ_g, WIS, coverage (§4.7, §9.2–9.3) | None | `holding_marks(holding_id, as_of)`; `forecast_history(holding_id)`, bitemporal (brief §9); `group_credibility(group_id)`, n_eff ≥ 20 |
| Group roll-ups | Views only (§9.1): envelopes, FTP charges, φ_g, DVA_g | `group_envelopes` (lab) | `group_rollup(group_id, metrics, as_of)` |
| Controls, archetypes | Frozen controls at 3/5/10 years (§5.10, §10.5); S-ADR-13 ablations | `evaluate_policy` (counted) | `compare_policies(refs, horizons)` on stored results, with paired SE |
| Probabilities, under views | Clopper–Pearson bounds; `ep_condition`; bridge P(μ ≥ 10%) (§4.11) | `ep_condition` (Translator) | `probability(event_id, threshold, view_id)`, registered events only |
| What changed | Aumann–Shapley path of duals (§4.13) | None | `explain_change(metric_id, run_a, run_b)` |
| Attribution, robustness, bridge, overlay | `attribute`, `robustness_card`, `bridge_card`, `overlay_offset_card` | Evaluator only | Read-only queries on stored results |
| Fund state, Treasury | Tier-1 board, CFP readings, LR1–LR8, draw fan, T4′ survival (§4.9, §8.4) | None | `state_panel()`, `treasury_panel()` |
| Shadow IC, decisions | Seat map, minority reports, `DecisionRecord`, signposts | Seats; `read_registry` | `seat_map()`, `decision_log()`, gated by the pre-vote rule (§3.5) |
| Names to ids | None | None | `find_entities(text)`; asks when the name is ambiguous |
| Differences, sums, ranks | None (a difference an LLM computes has no run link) | None | `compute_delta(refs)` with paired SE; cross-group ranks refused |

"Pack queries" need a typed contract over `pack/payload.py` (L0/L1/L2).

### 3.2 The what-if path outside the pack

The Translator's tools are lab-side only, so the analyst server cannot draft, confirm or run a what-if. Proposed flow:
1. `draft_whatif` **(new)** returns the typed ViewSpec or ScenarioSpec, the effective view, KL, ESS and a draft hash.
2. A human confirms.
3. `run_whatif(draft_hash)` **(new)** runs W1 (`ep_condition`) or W2 (`optimize_h` + `price_actions`) on the exploration plane. It creates a new run carrying `parent_run` and `override_hash`.

The frozen snapshot, `BeliefSet@hash` and scenario sets never change.

**Confirmation must be a human act the model cannot perform.**
- **`tpa chat` and the Ask panel:** confirmation is a UI step outside the model loop. With the SDK, the application either gates inside the tool, or inspects pending `tool_use` blocks and calls `runner.set_messages_params()`.
- **Claude Code and Desktop:** mcp 2.3's `Context.elicit` counts only where the client shows it to the human. Its docstring says an agent client may answer automatically.

**Missing**
- An `Override` record **(new)**: principal, time, effective view, KL, ESS.
- Engine-side counting of exploratory runs, separate from lab budgets (P4).
- An exploration-plane evaluator instance and cache that never shares search caches or counters (§7.2).
- Isolation from lab agents and memory.

### 3.3 Surfaces

**`tpa chat` (absent from §11.4)**
- A typer + rich REPL with `--offline|--replay|--live`. Sessions are pinned to a run set.
- Offline mode needs a chat stub: a deterministic intent grammar that calls the same tools and renderer. `StubBackend` only samples schema-valid output.
- Live mode adds network egress, which §7.2 grants only to `tpa lab run`. Chat should route through `agents/gateway.py`, and §7.2 needs a new row.

**Pack Ask panel backend (missing).** The pack is static (`console.html.j2`), and no web framework is installed. It needs:
- a stdlib `http.server` service on 127.0.0.1 with a session token;
- the pack and the chat API served from one origin, since a `file://` pack would need a null-origin CORS exception;
- the panel disabled with a notice when the service is down, as W1 is on a failed self-test.

In the laptop phase, only users of the serving machine can reach it.

**Analyst MCP server in Claude Code and Desktop.** The client's model writes the answer. That bypasses the gateway, redaction, `llm_policy`, cost caps, LLM-call manifests and the validator. Mitigations:
- pre-rendered results with labels and run links;
- `MCPServer(instructions=...)`;
- `ToolAnnotations(read_only_hint=True)`;
- SYNTHETIC data only until open question Q6 (LLM deployment) is answered;
- narrative from this surface declared unvalidated.

### 3.4 Conversation memory

ARCH has append-only transcripts and preserved thinking (§11.2), but no session model. Needed:
- A `ChatSession` **(new)** pinned to a contract, snapshot and run set, so numbers never shift mid-conversation. Newer runs are announced.
- Structured context (referenced ids, confirmed overrides) for follow-ups like "that fund", with a defined override scope and reset.
- Compaction summaries never treated as evidence; numbers are re-fetched.
- No cross-session memory. §8.11 forbids personalization, and the validator rejects memory citations.

### 3.5 Access control by role

Today identity exists only for `SignOff` (TB5), the CRO seal account (TB4) and NTFS ACLs (§7.2).

Needed: a `Principal(user, roles, groups, recusals, barriers)` **(new)**, taken from the Windows account (stdio servers run as the user) or a session token. An entitlement filter applies it at the tool layer, never in prompts:
- **Group heads:** own group in detail, peers in aggregate (§6.9).
- **Credibility:** own reference class only, n_eff ≥ 20; no cross-group rankings.
- **Desk barriers (§6.6):** no drill-down into holdings a desk may bid for or quote.
- **Restricted data:** infeasibility prices only in the Treasurer context (§6.1); never the sealed truth or the final store.
- **Voting members:** facts only (no AI narrative, seat map or minority reports) until their pre-vote locks (§8.6).

Refusals name the rule that applied and are logged.

### 3.6 Transcript logging

**What exists**
- LLM-call hashes in manifests (§10.2).
- JSON logs without citable free-text numbers (BS §1.9).
- The `assumption` table.

**What is missing**
- `chat_session` and `chat_turn` registry records **(new)**. Each holds the principal, surface and question; tool calls with arguments and run ids; the rendered answer, validator verdict and labels; and `_request_id`, served model, tokens and cost.
- Retention and access: the CRO office and MRM (§8.9), plus the user.
- Redaction (§9.7).
- Links to the DecisionRecords a chat informed.

The MCP surface logs tool calls only.

### 3.7 Clarifying questions

Lab roles have `escalate` and "data insufficient" (§7.9), and Ask allows "not in the artifacts". Chat has no policy.

Proposed rule: ask only when the ambiguity changes the number. Such ambiguities include:
- the holding and the as-of date;
- the plane;
- census v1.1/v1.1r/v1.0 and allocation v1/v2 (S-ADR-03);
- the world and the horizon;
- whether 10% is gross or net of distributions;
- group or total portfolio;
- tolerance or appetite pricing (ADR-29).

Otherwise, state the default used. Ask at most one question per turn, and never guess an entity.

### 3.8 Answer contract and labels

R16's "EXPLORATORY vs QUALIFIED" mixes plane labels with Gate-3 labels. Baseline cards (BASELINE_PRICED) are neither.

**`ChatAnswer` (new)** needs:
- placeholder statements, each with a statement label and citations;
- an evidence status equal to the weakest status cited: SEALED-QUALIFIED, SEALED-NOT_QUALIFIED/NOT_ASSESSED, BASELINE or EXPLORATORY;
- SYNTHETIC and INTERIM flags (INTERIM covers Real Assets; S-ADR-02).

**Validation.** No meta-controller state hosts Q&A (§7.4). The chat loop itself must therefore re-validate (≤ 3 retries) and fall back to a templated table of the cited metrics.

**Validator whitelist.** It must admit identifiers that contain digits (holding, run and metric ids; quarters). User parameters enter only through override placeholders.

**Scope.** The analyst explains recommendations and flip thresholds. It never recommends a vote.

### 3.9 Evaluation

- Golden conversations per role, with expected tool calls and cited metric ids.
- Refusal cases: league tables, peers' charges, sealed truth, narrative before the pre-vote.
- Clarification cases.
- What-if translation at pass³ ≥ 0.9 (§7.10).
- The fabricated-number drill (§7.11), run against chat.
- Sycophancy and flip tests.
- Injection via holding names and notes (TB6).
- Replay cassettes in CI.
- Re-qualification after model upgrades (S-ADR-18).
- A materiality tier (§11.7).

### 3.10 Cost and compute limits

Only lab cycles are budgeted ($50 soft / $200 hard; §7.7). Needed:
- a per-turn `max_iterations` cap;
- per-session and per-user daily USD caps;
- `count_tokens` pre-checks;
- caching of a frozen system prompt and tool list, verified via `usage.cache_read_input_tokens`;
- explicit effort per mode;
- W2 quotas and concurrency limits;
- W3 behind approval or a queue;
- a typed budget refusal.

### 3.11 Inconsistencies to resolve first

- **Groups:** §9.1 lists seven groups; S-ADR-01 has eight plus CF and TPA. Chat tools must take `GroupId` strings.
- **Seats:** §8.5 has twelve seats; S-ADR-22 has thirteen.
- **Forecast archive:** §4.7 and §9.3 assume there is no point-in-time archive; brief §9 says it exists.
- **Lab command:** §7.2 uses `tpa lab run`; §11.4 uses `tpa lab start`.
- **Final plane:** §11.3 should allow reading revealed SEALED metric instances, while still forbidding final-plane runs and final-store reads.
- **Transcripts:** §8.9 restricts them; R16 requires logging them.

## 4. SDK facts verified for CHAT_ANALYST.md

**anthropic 1.15.0**
- **Tool runner:** `client.beta.messages.tool_runner(...)` accepts `system`, `thinking`, `output_config`, `output_format`, `max_iterations`, `fallbacks`, `betas`, `cache_control`, `context_management` and `stream`. Its methods are `set_messages_params`, `append_messages`, `until_done`, `generate_tool_call_response`, `compact_before_next_turn`, `add_tools`, `remove_tools` and `close`. It rejects a `compaction` parameter.
- **Tool definitions:** `@beta_tool(strict=True, input_schema=Model)` is exported from `anthropic`. `anthropic.lib.tools.mcp.mcp_tool(tool, client, strict=True)` (`client` = an MCP `ClientSession`) converts MCP tools for the runner, so `tpa chat` can reuse the analyst server's tools and entitlements.
- **Tool choice:** forced `tool_choice` returns 400 on Opus 5.5. `auto` does not guarantee a call, so check for `tool_use` and re-prompt.
- **Conversation state:** the API is stateless. Compaction is the beta `compact-2026-01-12`; pass `response.content` back. A mid-conversation `role: "system"` message is model-gated; verify it on `claude-opus-5-5`.
- **Thinking and refusals:** on Opus 5.5 thinking is always on, the default effort is `medium`, and `display: "summarized"` is opt-in. Thinking is never evidence. Check `stop_reason == "refusal"` and `stop_details`, and log `_request_id`.
- **Replay:** the runner calls the client internally, so Replay needs an injected transport (unverified) or the manual loop in BS `agents/loop.py`.

**mcp 2.3.0**
- **Server class:** `FastMCP` is now `mcp.server.mcpserver.MCPServer`; importing `mcp.server.fastmcp` raises `ModuleNotFoundError`. The constructor takes `name`, `instructions`, `token_verifier`, `auth` and `middleware`.
- **Tool annotations:** `@server.tool(annotations=ToolAnnotations(read_only_hint=True), structured_output=...)`.
- **Context:** `Context.elicit(message, schema)` returns accept, decline or cancel. `Context.report_progress` also exists.
- **Tasks:** task types are in `mcp_types`; the server API is unverified.

## 5. Decisions for CHAT_ANALYST.md

- **D1 Tool catalogue:** names, schemas and engine sources (§3.1–3.2).
- **D2 One tool layer:** the analyst MCP server as the single tool and entitlement layer for all surfaces.
- **D3 Confirmation:** how a human confirms on each surface.
- **D4 Entitlements:** `Principal` and its rules, including desk barriers and the pre-vote window.
- **D5 Answer status:** the status taxonomy and the validator whitelist.
- **D6 Process topology:** chat via the gateway, an exploration-plane evaluator and the Ask service.
- **D7 Runner or manual loop:** decided by what Replay needs.
- **D8 Budgets and quotas.**
- **D9 Transcript retention and access.**
- **D10 Claude Code / Desktop scope:** data class and roles.
