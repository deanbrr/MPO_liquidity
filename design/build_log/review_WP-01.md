# Review of WP-01: contracts, pyproject, taxonomy config and analyst contracts

**Reviewer:** adversarial spec-conformance review (build wave 0) · **Date:** 2026-10-19 · **Authority:** BUILD_SPEC v1.1 (§0–§3, §4.0–§4.1, §9.2, §10); CHAT_ANALYST v1.1 §5.1, §5.3, §5.5, §6.3, §11, §14.1 (binding for `contracts/analyst.py`) · **Code reviewed:** `src/adic_tpa/__init__.py`, `py.typed`, `src/adic_tpa/contracts/*` (31 modules), `src/adic_tpa/config/taxonomy/groups_v{1,2}.yaml`, `pyproject.toml`, `.gitattributes`, `tools/dev_install.py`, and every WP-01 test under `tests/{unit,property,layering,determinism,perf}`.

> SYNTHETIC – NOT ADIC DATA. Every number below comes from synthetic fixtures or from reviewer probes on synthetic objects.

## Verdict

**CHANGES REQUIRED before `contracts-v1.0` is tagged: 1 critical and 2 high findings.** The work package is broadly complete and faithful to the specification:

- **Inventory:** all 346 class names in §3 and CHAT_ANALYST §5.1/§5.3/§6.3 exist.
- **Fields:** field names match the spec. Every difference traces to a documented CHAT_ANALYST §5.5 reconciliation or a WP-01 addition.
- **Tests and coverage:** all eleven §4.1 test files exist and pass. Line coverage of `contracts` is 95.2% (target ≥ 90%).
- **Taxonomy:** v1 and v2 match the normative §3.2 table.

Three defects must still be fixed:

- **WP01-R01 (critical):** `PolicySpec` and every model that carries one cannot round-trip through its own JSON. This violates S-ADR-39, and a test pins the broken behaviour.
- **WP01-R02 (high):** enum values contradict the spec's explicit spellings: `FactorKind` against S-ADR-35 (`logret`/`level`/`change`) and `TargetMode` against S-ADR-06 (`"precommitted"`).
- **WP01-R03 (high):** the `FlowSlice.intra` netting check rejects legitimate float32 data.

The test suite is also weaker than its size suggests. 31 of 39 targeted mutants survive, including every §1.12 labelling validator outside `Holding`.

## How the review was done

1. Read BUILD_SPEC §0–§3 in full, plus §4.0, §4.1, §4.8 (OwnerConfig), §4.10 (factor kinds), §4.29, §7.1–§7.5, §9.2, §10 and CHAT_ANALYST §4.2–§6.6, §11 and §14.
2. Read every WP-01 source file and test line by line.
3. Ran the WP-01 tests and the whole suite.
4. Ran four reviewer probe scripts on scratch copies (never on the repo) to confirm each suspected defect.
5. Mechanical inventory check of class names, plus a heuristic field-level diff of spec class blocks against `model_fields` and dataclass fields.
6. Mutation testing: 40 single-bug mutants of a scratch copy of `src/`, each run against `tests/unit` and `tests/property`. The harness was validated by mutant M00 (`sort_keys=False`), which was killed.
7. Line coverage of `contracts` via `sys.monitoring` during `tests/unit`, `property`, `layering` and `perf`. This stands in for §10.3, because `tools/coverage_lite.py` belongs to WP-03 and does not exist yet.
8. Read-only git checks: no tags exist.

## Test results

| Run | Result |
|---|---|
| Full suite `tests/` (= WP-01's tests; no other WP has landed) | **728 passed, 0 failed** in 30.6 s |
| Slowest | `layering/test_contracts_import_order.py::test_every_cycle_reaching_module_imports_first` 6.6 s; `determinism/test_hash_seed_stability.py` 3.0 s; `property/...dict_insertion_order` 1.5 s; `unit/test_package.py::test_isolated_mode_imports_this_checkout` 1.03 s (subprocess); everything else < 1 s |
| Perf §4.1: `content_hash(BookSnapshot)`, 500 funds + 1,500 loan cohorts | 0.17–0.22 s measured, budget 0.5 s ✓ |
| Coverage of `contracts` (§10.3 ≥ 90%) | **5,668 / 5,952 lines = 95.2%** ✓. Lowest modules: `logjson` 85.4%, `evidence` 86.2%, `engine_io` 91.0% |

## Definition of done (§9.2 WP-01; §4.1; CHAT_ANALYST §14.1 WP-01 part; §10.3)

| DoD item | Status | Evidence |
|---|---|---|
| Every §3 model and enum: recourse protocol, `BeliefDraws`, contexts, LLM draft models, `contracts/analyst.py` per CHAT_ANALYST §5 | ✓ | 346/346 spec class names present. Field diff clean apart from documented reconciliations (§5.5) and the WP-01 addition `AnalysisContract.lever_signoffs`. All 34 analyst tools are catalogued; 21 are increment-1 tools (rows 1–15, 24, 25, 30–33); MCP stages and tiers match §5.2 |
| units, calendar, hashing incl. `canonical_artifact_hash`, signing, `contracts.rules`, errors, JSON-mode config loader, `ARRAY_SPECS`, Protocols | ✓ | All §4.1 signatures present (extra keyword-only parameters with defaults only). The 22 §1.10 error classes and codes are exact. `EvaluatorPort` has one method for each of the 28 §7.4 evaluator tools |
| Taxonomy v1/v2 | ✓ | Every normative §3.2 column matches: codes, kinds, engines, recourse tiers, red/amber, seat, split (v2 0.50/0.10×5, sum 1; v1 PE 0.60), η sign, contingent, `fund_distribution_stress` = PE/SEC/CO. Couplings as §3.2 (θ 0.33, kernel weights, acceptance, ρ_GP 0.6 pairwise). n_groups 8, seats 13 (v1: 7, 12) |
| §4.1 tests incl. config round trip, LF hashing, signing | ✓ | `test_hashing` (10 goldens, float repr, NaN), `test_models_strict` (>250 models, plus containers), `test_lens_action_rules`, `test_contract_validators` (every ARCH §10.1 rule, both directions), `test_cfp_invariant`, `test_no_hardcoded_group_ids`, `test_config_roundtrip`, `test_text_hash_lf`, `test_canonical_artifact_hash`, `test_signing`, `test_rules`: all present and green |
| Invariant: `content_hash` stable across processes and hash seeds | ✓ | Golden values plus a child interpreter with a different `PYTHONHASHSEED` |
| Invariant: all models frozen; mutation raises | ✓ (models) / partial (arrays) | `model_config` is checked for every model. Frozen containers still hold writable arrays (R15) |
| Contracts tagged only after the WP-03 walking skeleton is green | ✓ (pending, as required) | `git tag --list` is empty |
| `test_no_hardcoded_group_ids` and the allowlist harness in place | ✓ | `tests/layering/*`, each with a planted-violation self-test |
| CHAT_ANALYST §14.1: `check_llm_schema` on every LLM-facing model | ✓ with a gap | `test_llm_facing_schemas` runs `anthropic.transform_schema` on 75 models. `Escalation`, the `escalate` tool input, is missing from the inventory (R12) |
| §10.3: ≥ 90% lines; 100% of `__all__` functions called by a test | lines ✓; functions ✗ (one) | `arrays.validate_container` is never called. Numbers-bearing methods such as `StressSpec.s_star` and `LeverSet.available` are never executed (R05) |

## Findings (most severe first)

### WP01-R01: critical. PolicySpec's computed `spec_hash` breaks the JSON round trip of PolicySpec, IdeaBundle and VariantSet

- **Where:**
  - `contracts/policy.py:143-147`: `@computed_field spec_hash` on a model with `extra="forbid"`.
  - `tests/unit/test_policy_contracts.py:23-25` asserts that `spec_hash` is rejected as input.
- **What happens:** `model_dump_json()` emits `spec_hash`, but `model_validate_json()` rejects it as `extra_forbidden`. Probe results:
  - `PolicySpec.model_validate_json(spec.model_dump_json())` raises `ValidationError: spec_hash Extra inputs are not permitted`.
  - The same failure occurs for `IdeaBundle` (`spec.spec_hash`) and `VariantSet` (`variants.0.spec_hash`).
- **Why critical:**
  - S-ADR-39 requires registry rows and MCP payloads to be validated with `model_validate_json`.
  - PolicySpec is the core agent↔evaluator exchange object: `compile_spec`, the IDEATOR's `IdeaBundle`, the ablation `VariantSet`, plane-store rows keyed by `spec_hash`, and Replay cassettes.
  - WP-21, WP-24, WP-25 and WP-26 would each have to bake ad-hoc `exclude={"spec": {"spec_hash"}}` workarounds into frozen code.
  - There are also two identities for one spec, because `content_hash(spec) != spec.spec_hash`.
- **Fix:**
  - Stop serializing the derived hash. Either make `spec_hash` a plain property or method (not a `computed_field`), or accept an optional `spec_hash` input and verify it equals the recomputed hash.
  - State which identity keys the plane store.
  - Add a generic test that JSON-round-trips one fixture instance of every LLM-facing model and every registry/MCP model. Such a test would have caught this.

### WP01-R02: high. Enum values contradict the spec's explicit lower-case spellings (FactorKind, TargetMode); LLMMode's documented mapping is not implemented

- **Where:**
  - `contracts/enums.py:284-289` (`FactorKind`), `:505-509` (`TargetMode`), `:468-473` (`LLMMode`).
  - `tests/unit/test_enums.py:41-45` pins `value == name` for both enums.
  - `tests/unit/test_world.py:41` uses `"LOGRET"`.
- **What happens:**
  - The module adopts the convention that a shorthand `class X(StrEnum): A, B` has values equal to the member names, which here means upper case.
  - The spec spells some of these values explicitly in lower case:
    - S-ADR-35, §1.2 and §4.10: factor kinds `logret`, `level`, `change`, declared in `scen/factors.yaml`.
    - S-ADR-06: `ObjectiveSpec.target_mode = "precommitted"`.
  - WP-06's `factors.yaml` and WP-24's contract template, written as specified, will fail to validate. Probe: `FactorKind("logret")` raises `ValueError`.
  - `LLMMode`'s docstring says `TPA_LLM_MODE` values offline/replay/live "map case-insensitively", but there is no `_missing_`: `LLMMode("offline")` raises `ValueError`.
  - Python's own `StrEnum` + `auto()` would produce lower-case values. The convention is therefore a spec-level ambiguity that must be recorded.
- **Fix:**
  - Set `FactorKind` values to `"logret"`, `"level"`, `"change"` and `TargetMode` values to `"precommitted"`, `"rolling"`.
  - Update `test_enums` and the world fixtures.
  - Implement a case-insensitive `LLMMode._missing_`, or drop the claim from the docstring.
  - Record the value convention used for the other shorthand StrEnums as a deviation.

### WP01-R03: high. The `FlowSlice.intra` netting check (1e-9 × scale on float32 data) rejects legitimate intra-ADIC flows

- **Where:** `contracts/arrays.py:137-142` (`_inv_sum_axis1_zero`; scale = max(1, Σ_g|x|)), applied by `ARRAY_SPECS["FlowSlice"]["intra"]` (`:532`).
- **What happens:**
  - §3.8 and §3.17 store `intra` as f32 and require Σ_g = 0 within "1e-9 × scale", with scale left undefined.
  - Float32 resolution is about 6e-8 relative, so any cell that nets three or more entries fails.
  - Probe at `FlowSlice.validate()` level: the overlay bills client A $0.1bn and client B $0.2bn, and the OVERLAY row = fee_a + fee_b in float32. The residual is 7.45e-9 against a tolerance of 1.0e-9, so validation raises `SchemaError`.
  - A 2-party exact negation passes, which is why the test (±0.1) does not catch it.
  - WP-11 (P2S), WP-12 (services ledger) and WP-13 cannot produce valid multi-party intra flows.
- **Fix:**
  - Use a float32-aware tolerance, e.g. `tol = max(1e-9·scale_bn, 8·np.finfo(np.float32).eps·Σ_g|x|)` (about 1e-6 relative).
  - Record it as a deviation, raise a contract note to the spec owner (the 1e-9 cannot hold on f32 storage), and add a 3-party float32 test.

### WP01-R04: medium. Weak tests: 31 of 39 targeted single-bug mutants survive the unit + property suites

- **Where:** see the mutation table in the appendix.
- **What survives.** No test fails when any of these validators or functions is broken:
  - **§1.12 labelling validators:**
    - `CubeMeta` is_synthetic ↔ data_class.
    - `Mark`, `Quote` and `OverlayTrade` synthetic consistency.
    - `AnswerCard` SYNTHETIC label.
  - **§3.17 Tree invariants:** leaves sum to 1, `p_world` leaves sum to 1 per world, `leaf_world`.
  - **Flow and recourse rules:**
    - The positive-sign half of the §1.4 flow-sign rule: a negative DISTRIBUTION passes.
    - `LeverSet.available` nesting (consent R0x ⊂ R0 ⊂ R1 ⊂ R2).
    - `RecourseOutcome` red-only-on-sold.
  - **Configuration and contract rules:**
    - `CanonicalConventions` split sum.
    - `RunManifest` REAL ⇒ ¬DEV.
    - The recovery plan's mode equals the contract mode.
    - `ObjectiveSpec` negative weights.
    - `GroupSpec` fund_distribution_stress ⇒ private.
    - Taxonomy coupling references.
  - **Evidence and optimizer checks:**
    - `PathMetrics` 0/1 flags.
    - `FlowCube` column cubes have 1–3 units.
    - `HSolution` RESTORED ⇒ recovery_hash.
    - `DecisionCard` LEVER legs.
    - The `EvalRequest` tune rule.
    - The `NoiseSlice` months axis.
  - **Analyst and room checks:**
    - `Fact` categorical ⇒ fmt `cat`.
    - `ToolResult` OK + error.
    - `ViewSpec` unconfirmed fields.
    - `OverrideConfirmation.signed_payload` dropping `user_hash` and `surface` (security-relevant: the signature would no longer bind who confirmed and where).
  - **Book and rules details:**
    - `UNIT_KIND_ENGINE["ra_open_end"]`.
    - The age-bucket boundary.
    - The SALE_PROCEEDS intra-quarter profile.
    - The 1e-9 tolerance on BookSnapshot NAV totals, which survives loosening to 1e-3.
- **Why it matters:** these invariants exist in code but nothing pins them, so a refactor can silently delete them after the freeze. The labelling validators carry governance weight (§1.12; `tpa audit labels` at 100%).
- **Fix:** add a parametrized "each validator rejects its violation" table, one negative case per validator. Do the labelling validators, the Tree checks, the confirmation signed payload and LeverSet first.

### WP01-R05: medium. Untested numbers-bearing methods; one `__all__` function never called (§10.3 sub-target)

- **Where:**
  - `ledger.StressSpec.s_star`, the canonical s*(θ): equity −(0.30 + 0.10θ), distributions 0.45(1 − θ), calls 1 + 0.5θ, 28% base, 24 months.
  - `optimizer.LeverSet.available`.
  - `optimizer.ColKey.parse`, which also raises a bare `ValueError` instead of `SchemaError` on a malformed string.
  - `evidence.TuningJob.as_dict`, `evidence.PathMetrics.terminal_series`, `ids.HoldingId.is_synthetic`, `taxonomy.GroupRegistry.config`.
  - `arrays.validate_container`, which is in `__all__` and never called.
- **Evidence:** coverage run with `sys.monitoring`. I checked the values by hand: `s_star(0.58)` = (−0.358, 0.189, 1.29, 0.28, 24) is correct today but unprotected.
- **Fix:**
  - Add golden tests for `s_star` at θ ∈ {0, 0.58, 1}, nesting tests for `available`, and a `ColKey` round trip.
  - Call or remove `validate_container`.
  - Make `RowKey.parse` and `ColKey.parse` raise `SchemaError` on malformed input.

### WP01-R06: medium. Mixed SYNTHETIC+REAL raises a code-less pydantic ValidationError instead of `DataClassMixError`; the run-mode clashes do not raise `RunModeRefused`

- **Where:** `book.py:435-437`, `evidence.py:95-99`, `contract.py:339-342`.
- **What happens:**
  - §1.12 rule 2: "SYNTHETIC and REAL together raise `DataClassMixError`" (§1.10 code `DATA_CLASS_MIX`).
  - Probe: a book with one SYN and one REAL holding raises `pydantic.ValidationError`, which is neither a `TPAError` nor a `DataClassMixError`.
  - Gates and the failure taxonomy therefore cannot classify the event.
  - Pydantic propagates non-`ValueError` exceptions unchanged, so the validator can raise `DataClassMixError` directly.
- **Fix:**
  - Raise `DataClassMixError` from `BookSnapshot` when classes mix.
  - Raise `RunModeRefused` for REAL + DEV_SYNTHETIC in `RunManifest` and `AnalysisContract`, or document why a `SchemaError` is preferred.
  - Test `exc.code`.

### WP01-R07: medium. The REAL-mode refusal of the DEV test signer keys on the unsigned `method` label

- **Where:**
  - `signing.py:70-73, 107-119`.
  - `contract.py:339-340`.
- **What happens:**
  - The signed payload is `{object_hash, role, signer_hash, signed_at}` (S-ADR-40). `method` is not covered.
  - Probe: a dev-key signature relabelled `method="ed25519_dpapi"` verifies **True** under `run_mode=RunMode.REAL` when the roster contains the dev key.
  - `verify()` defaults to `run_mode=None` and then accepts dev-key sign-offs.
  - `AnalysisContract`'s REAL rule also checks only `method`.
- **Fix:**
  - In REAL mode, refuse by key identity: `signer_hash == DEV_TEST_SIGNER_HASH` or the roster key equals `dev_test_public_key()`.
  - Consider making `run_mode` a required keyword.
  - Add a relabelled-method test.

### WP01-R08: medium. `ScenarioCube.checksum()` excludes all of `meta`, so relabelling a cube changes neither checksum

- **Where:** `world.py:321` (`_CHECKSUM_EXCLUDE = {"meta"}`), `:323-325`.
- **What happens:**
  - `scenario_checksum()` covers the eight scenario arrays only, and the container checksum skips the whole of `meta`, not just `meta.checksum`.
  - Probe: changing `world_id` M1 → M6 leaves `checksum()` identical. The same holds for `plane`, `data_class`, `factor_names` and `factor_kinds`, `path_offset` and `asof`.
  - Manifests (`scenario_hashes`, `GroupRatesMeta.cube_checksum`, `FlowCubeMeta.cube_checksum`) therefore cannot detect a mislabelled cube.
- **Fix:**
  - Exclude only `meta.checksum`, i.e. hash `meta.model_dump(exclude={"checksum"})` into `checksum()`.
  - Decide and document whether the scenario identity (`meta.checksum`) should bind the generating meta.

### WP01-R09: medium. Intra-quarter profile shapes are unspecified modelling numbers hard-coded in contracts and not recorded

- **Where:** `rules.py:25-36, 64-72`.
- **What happens:**
  - DEBT_DRAW lands in month 1; SALE_PROCEEDS, DEBT_REPAY and OWNER_DRAW in month 3; all other flows are spread evenly.
  - `Clock.MONTHLY` raises.
  - ARCH §4.0 only says the profile "spreads calls and distributions over months". The other choices move the monthly T4′ ledger and the HQLA-floor months.
  - §1.11: "code holds no calibrated numbers".
  - The SALE_PROCEEDS timing is untested (mutant M30 survives).
- **Fix:**
  - Record the choices as a deviation and confirm them with the WP-13 owner.
  - Preferably move the table to config with `# [I]` tags, or document why it belongs in contracts.
  - Test every FlowType's profile.

### WP01-R10: medium. Analyst v1 tool shapes (rows 16–23, 34) are reconstructions about to be frozen, and two class names collide

- **Where:** `analyst.py:478-525`, plus the payloads `GovernanceView`, `BindingView`, `AttributionView`.
- **What happens:**
  - CHAT_ANALYST v1.1 §5.3 says these rows "keep v1.0's shapes". v1.0 is not on disk, so the fields are invented.
  - `analyst.ImpliedIn(item_id)` and `analyst.AttributeIn(kind, run_id?, group?)` share their names with `tools.ImpliedIn(seat_id, item_id)` and `tools.AttributeIn(run_id, kind)`. The field diff surfaced this collision.
- **Fix:**
  - Record the reconstruction as a deviation.
  - Mark the v1 analyst models provisional for WP-40, or keep them out of the v1.0 freeze.
  - Give the analyst models distinct names (e.g. `ImpliedActionsIn`, `AttributionIn`) and keep the addendum names as aliases.

### WP01-R11: medium. `RealAssetTerms.access` value renamed COINVEST → COINVESTMENT

- **Where:** `book.py:225-227`.
- **What happens:**
  - §3.3 lists `COINVEST`, but the §4.1 lint forbids any string literal in `src/` equal to a configured group id.
  - The rename is a sensible resolution of this spec self-conflict, and the code comments on it. It is still a value change in a frozen contract.
- **Fix:**
  - Put the rename in the deviation list and notify WP-09, WP-15 and the spec owner.
  - Alternative: exempt typed `Literal` vocabularies in `contracts/` from the lint.

### WP01-R12: low. The LLM-facing inventory is incomplete (Escalation), and OptimizeHIn/EPIn are excluded without a record

- **Where:** `ports.py:263-268`.
- **What happens:**
  - §7.4 makes `Escalation` the input of the `escalate` tool for all roles, but it is absent from `LLM_TOOL_INPUT_MODELS`, so the schema check never runs on it. It passes when run manually.
  - It also carries system- and human-owned fields (`raised_at`, `resolved_by`, `resolution`), contrary to S-ADR-36.
  - `OptimizeHIn` and `EPIn` list the TRANSLATOR (an LLM role) as a caller, yet they carry `ViewSpec` with the human-owned `confirmed` and `author_hash`. They are excluded silently.
- **Fix:** add `Escalation`, or an `EscalationDraft` without the resolver fields; record the OptimizeHIn/EPIn decision; raise a contract note.

### WP01-R13: low. Some shape symbols are looser than the §3.17 table

- **What happens:**
  - `ScenarioCube.draw_rate`/`draw_override`: Y is unbound (spec [P, 11]); a [P, 5] rate validates (probe).
  - The `GroupRates` age axis is bound to `meta.age_buckets` (spec [.., 2]); 3 buckets validate.
  - `LedgerPaths` M1 is unbound (spec 121).
  - `FlowCube` "one block at most" (P ≤ 2,000) is unchecked.
  - `StressReport.survival_months` has no upper bound of 25.
  - The `DualSet.ell` invariant is unchecked.
- **Fix:** bind or check these, or record the deliberate ones (the age axis) as deviations.

### WP01-R14: low. A SYN holding id's group code is not checked against its group

- **Where:** `book.py:425-443`.
- **What happens:** probe shows `SYN-RA-0001` is accepted in group CF, and the unknown code `SYN-XYZ-0001` is accepted (§1.8 `SYN-<GROUPCODE>-<4 digits>`).
- **Fix:** in `BookSnapshot`, require `holding_id.group_code == tax.spec(group).code` for synthetic rows.

### WP01-R15: low. Frozen array containers hold writable arrays

- **Where:** `arrays.py:287-322`.
- **What happens:** probe: `DualSet.ell[0] = nan` after `validate()` changes `checksum()` silently.
- **Fix:** set `flags.writeable = False` on every array of frozen containers in `__post_init__`, so containers truly own their arrays (§1.5).

### WP01-R16: low. The config audit misses cached taxonomies after `clear_config_audit()`

- **Where:** `taxonomy.py:229-231` (`lru_cache`) and `config.py:91-92`.
- **What happens:** probe shows 0 audit records after clear followed by `for_version("v2")`. Long-lived workers' manifests would omit the taxonomy file.
- **Fix:** re-record the audit entry on cache hits, or clear the cache together with the audit.

### WP01-R17: low. `FlowType.sign` and `is_cash` fail on plain ints

- **Where:** `enums.py:247-251`.
- **What happens:** `FlowType.sign(0)` raises `AttributeError`. §3.1 describes them as table lookups `FlowType.sign(ft)`.
- **Fix:** index with `int(self)`, or make them static methods that accept an int.

### WP01-R18: low. Direct model construction raises `pydantic.ValidationError`, which is not a `TPAError`

- **What happens:** only `load_yaml` and `load_json_payload` convert to `SchemaError` (§1.10 "All exceptions derive from TPAError").
- **Fix:** document the boundary rule for consumers, and offer a helper such as `contracts.config.validate_model(model, data)`.

### WP01-R19: low. Deviations visible in code that must be in the implementer's deviation list (verify)

1. The StrEnum value convention (R02).
2. `canonical_json` goes through `model_dump(mode="python")` with its own conversions instead of `mode="json"`. The aim is UTC "Z" normalization; it also normalizes −0.0 to 0.0.
3. `VOLATILE_FIELDS` is extended beyond the §4.1 list (`signed_at`, `signature`, `expires_at`, `time_s`, …).
4. Real `HoldingId`s must contain "-" so that `HoldingId | GroupId` stays disjoint.
5. `RealAssetTerms.kind = "realasset"`, and the `UNIT_KIND_ENGINE` engine-id strings.
6. `AnalysisContract.lever_signoffs`. R1 accepts any lever id and any role as "a signed revolver".
7. The DECISION ⇒ mandate B rule, derived from S-ADR-14.
8. `PolicyRef` limits native names to the closed §3.11 list.
9. `TuningJob.box` uses named `TuningBox` sub-models (S-ADR-36), and `ResidualSpec.box` uses `Interval` (§3.16 note).
10. `LLMRequest`, `LLMResponse`, `ToolDef` and `ToolExecutor` are defined in `contracts.ports`. §3.18 says they are defined in agents and re-exported, which §4.0 makes impossible. The `ToolExecutor` signature is invented.
11. `ConfirmToken` is omitted, because addendum v1.1 has no tokens.
12. The `# model: module:Class` config header is a convention that binds every config-owning WP.
13. The `seal.runner` import override.
14. The intra-quarter profiles (R09).
15. `DRAW_FLOOR_A`/`DRAW_CAP_A` as code constants.

### WP01-R20: low (contract issue for the spec owner). Spec-level labelling gap

- **What happens:**
  - §1.12 rule 1 says every data row carries `is_synthetic` and `data_class`.
  - The §3 field lists for `Milestone`, `Facility`, `CSA`, `CRIFRow`, `ServiceContract` and the overlap nodes and edges have neither.
  - `BookSnapshot.data_class` covers the nested rows, but `Milestone` and `CRIFRow` travel standalone.
- **Fix:** have the spec owner decide between adding the labels and defining inheritance for `tpa audit labels`.

### WP01-R21: low (integration note). `.gitattributes` `* text eol=lf` will renormalize 212 tracked or addable CRLF text files

- **What happens:**
  - The 212 files are 135 json, 49 txt, 4 md, 3 csv, 16 `.crash1` and a few others.
  - The rule forces text handling on any future binary type not listed, e.g. `.sqlite3`, `.xls`, `.pickle`, `.webp`, `.hdf5` and DPAPI key blobs.
  - A scan found no currently binary file affected.
- **Fix:**
  - The orchestrator should commit `.gitattributes` together with `git add --renormalize .` in a dedicated commit.
  - Widen the binary list, or raise a contract note proposing `* text=auto eol=lf`.

### WP01-R22: low. Test runtime

- **What happens:**
  - `test_contracts_import_order` takes 6.6 s.
  - `test_isolated_mode_imports_this_checkout` takes 1.03 s.
  - The perf test runs in the default selection; only the CI `-m "not slow and not perf"` filter excludes it.
- **Fix:** mark the import-order test `slow`, or narrow it.

## Appendix A: mutation testing (scratch copies only; unit + property suites; `-x`)

| Mutant (one plausible bug) | Result |
|---|---|
| M00 sanity: `sort_keys=False` in canonical JSON | KILLED (harness valid) |
| M29 instalment floor dropped · M31 −0.0 kept · M32 abs paths not normalized · M34 CFP invariant weakened · M36 consent order swapped · M37 B2 allowed on search · M38 bundle hash drops field_tags · M39 q_rate = r/4 | KILLED |
| M01 positive-sign flow check dropped · M02 Tree leaf sum · M03 Tree p_world · M04 Tree leaf_world · M05 GroupSpec FDS⇒private · M06 coupling refs · M07 conventions split sum · M08 LeverSet `<` instead of `<=` · M09 negative model weights · M10 AnswerCard SYNTHETIC label · M11 CubeMeta synthetic consistency · M12 Mark consistency · M13 Quote consistency · M14 OverlayTrade consistency · M15 PathMetrics 0/1 · M16 RunManifest REAL/DEV · M17 FlowCube column units · M18 DecisionCard LEVER legs · M19 HSolution RESTORED hash · M20 Fact cat fmt · M21 ToolResult OK+error · M22 ViewSpec unconfirmed fields · M23 confirmation payload drops user_hash/surface · M24 NoiseSlice months axis · M25 EvalRequest tune rule · M26 recovery plan mode · M27 ra_open_end engine · M28 age boundary · M30 SALE_PROCEEDS profile · M33 red-only-on-sold · M35 NAV tolerance 1e-3 | **SURVIVED (31)** |

## Appendix B: probes (reviewer scratch scripts, not in the repo)

1. `PolicySpec`, `IdeaBundle` and `VariantSet` JSON round trips all fail with `extra_forbidden` on `spec_hash` (R01).
2. `FactorKind("logret")` and `LLMMode("offline")` raise `ValueError` (R02).
3. A float32 three-entry intra cell fails `FlowSlice.validate()`: residual 7.45e-9 > 1e-9 (R03).
4. A relabelled dev-key `SignOff` verifies True in REAL mode (R07).
5. A world relabel leaves `ScenarioCube.checksum()` unchanged (R08).
6. A mixed book raises `ValidationError`, not `DataClassMixError` (R06).
7. `draw_rate` [P, 5] and three age buckets validate (R13).
8. An id/group-code mismatch is accepted (R14).
9. An in-place array edit changes the checksum silently (R15).
10. Audit count is 0 after clear plus a cached load (R16).
11. `FlowType.sign(0)` raises `AttributeError` (R17).
12. `content_hash` of 2,000 holdings takes 0.17–0.22 s (perf ✓).
13. `s_star(0.58)` = (−0.358, 0.189, 1.29, 0.28, 24) ✓.
14. A `ColKey` round trip works.
15. No currently tracked file would be corrupted by `.gitattributes`.

## Contract issues to raise (outside WP-01's files, for the spec owner and consumers)

- **R03:** the "1e-9 × scale" netting tolerance cannot hold on f32 `FlowSlice.intra`. The spec should define scale relative to float32 epsilon.
- **R20:** rows without labels versus §1.12 rule 1.
- **R12:** whether the TRANSLATOR may submit `ViewSpec` with `confirmed=True`, or the firewall resolves view ids.
- **R10:** WP-40 must confirm or replace the reconstructed v1 analyst shapes before they are relied on.
- **R11:** the RealAssetTerms `COINVESTMENT` value, for WP-09 and WP-15.
