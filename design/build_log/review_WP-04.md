# Review of WP-04: registry

**Reviewer:** adversarial spec-conformance review (build wave 0) · **Date:** 2026-10-19 · **Authority:** BUILD_SPEC v1.1 (§0–§3, §4.0, §4.6, §7.8, §7.13, §8.7, §9.2, §10); ARCH §9.3, §10.2–§10.3, §10.6; CHAT_ANALYST v1.1 §3.6, §9.3, §9.6–§9.7, §11 (context) · **Code reviewed:** `src/adic_tpa/registry/{__init__,store,chain,artifacts,metrics,provenance,mfdr}.py`, `schema.sql`, and every WP-04 test: `tests/unit/registry/*` (6 files + conftest), `tests/drills/test_chain_verification.py`, `tests/property/test_registry_properties.py`, `tests/perf/test_registry_perf.py`. No registry or WP-04 test file changed during the review (last write 03:46).

> SYNTHETIC – NOT ADIC DATA. Every number below comes from synthetic fixtures or from reviewer probes on synthetic objects in scratch databases.

## Verdict

**CHANGES REQUIRED: 1 critical, 2 high, 6 medium and 12 low findings.** The registry is well built and largely faithful to §4.6:

- **Signatures:** all 15 methods of the §4.6 `Registry` exist with the specified names, parameters, types and return types. Every extra parameter is keyword-only with a default. The extra public methods (`get_run`, `read_ledger`, `decision_head`, `chain_head`, ...) are permitted refinements.
- **Storage:** WAL mode, `synchronous=FULL`, triggers on all 13 tables, and a cross-process writer lock with `BEGIN IMMEDIATE`. Two handles and four threads, and a second process, never fork the chain.
- **Tests:** all five §4.6 tests exist and pass, as does the §7.13 drill `test_chain_verification`.
- **Performance:** `verify_chain` on 1M rows takes **7.7 s** (budget 60 s). `put_metrics` runs at **25–40k rows/s** on an empty store and **≥ 11.9k rows/s at 1M rows** (budget 10k).
- **Coverage:** 95.8% of lines; every `__all__` function is called by a test.

These defects must be fixed before WP-25/27/29/39 build on the registry:

- **WP04-R01 (critical):** the record-level hash chain (`chain.record_hash`, enforced by `append_decision`) leaves `prev_hash` out of the hashed JSON. §8.7 puts it in: `record_hash = sha256(prev_hash ‖ canonical_json(record without record_hash))`. A §8.7-conformant `DecisionRecord` is therefore **refused** with `HASH_MISMATCH`, and registry-hashed records fail a §8.7 verifier (`tpa audit chain`).
- **WP04-R02 (high):** decision outcomes and signpost changes are stored as re-appended versions of the whole `DecisionRecord`. §8.7 instead appends outcomes as separate `outcome` records referencing `decision_id` ("nothing is edited"), and says "the registry mirrors the chain". `append_decision` cannot mirror such a log.
- **WP04-R03 (high):** `get_metric` (and `list_metrics`) serve instances from **ABORTED, FAILED and still-STARTED runs** as the "latest" evidence. Probe: after an ABORTED run (SEAL_BREACH) wrote 0.09, `get_metric` returned 0.09.

The tests are weaker than their number suggests. Of 48 single-bug mutants, 12 survive and 8 of those matter. One is the drill's own property: reporting the *last* bad row instead of the first goes unnoticed (M01). Another is evidence hiding: deleting a metric's index row (M03).

## How the review was done

1. **Reading.**
   - Read BUILD_SPEC §0–§2 in full, §3.15–§3.18, §4.0, §4.6, §4.27–§4.31 (consumers), §7.6–§7.13, §8.1, §8.7, §9.2 and §10.
   - Read ARCH §9.3 and §10.2–§10.6, and CHAT_ANALYST §3.6, §9 and §11.
   - Read every WP-04 source and test file line by line.
2. **Test runs.** Ran the WP-04 tests, the WP-04 perf tests and the whole suite.
3. **Coverage.** Measured with `tools/coverage_lite.py` (WP-03) and `--require-public`.
4. **Probes.** Ran four reviewer probe scripts (22 probes) against the real `src`. All databases lived in scratch directories; nothing was written to the repo.
5. **Mutation testing.** Applied 48 single-bug mutants plus a sanity mutant M00 to a scratch copy of `src/`. Each ran against the WP-04 unit, drill and property tests with `-m "not slow"`. M00 was killed, which validates the harness.
6. **Cross-checks against other WPs.** Compared:
   - the mFDR ledger with `stats.AlphaInvesting` (WP-02);
   - the record chain with §8.7 (consumed by WP-27, WP-29 and WP-39);
   - the read-only handle with CHAT_ANALYST §9.6.

## Test results

| Run | Result |
|---|---|
| WP-04 tests: `tests/unit/registry`, `tests/drills/test_chain_verification.py`, `tests/property/test_registry_properties.py` | **107 passed, 0 failed** in 8.3 s. Slowest: the property test 2.7 s cold (0.55 s warm); the `slow`-marked second-process test about 1 s; everything else < 0.5 s |
| WP-04 perf: `tests/perf/test_registry_perf.py` | **2 passed**. `put_metrics` 20k rows in 0.81 s; the 1M-row test 134.8 s wall, nearly all of it building the store |
| Whole suite, excluding the walking skeleton | **1,909 passed, 0 failed** in 153.9 s |
| Walking skeleton (`tests/skeleton`, WP-03) | WP-03's fixer edited it during the review (timestamps 03:50 → 03:56). First run: collection error (`TypeError` at line 1028). Re-run: 35 passed, 3 failed (ledger identity, port tuple, `draw_block` signature), 11 skipped. **None involves the registry**; the skeleton calls no `Registry` method at all (R20) |
| Coverage of `registry` (§10.3 ≥ 85%; 100% of `__all__` functions called) | **1,365 / 1,425 lines = 95.8%** ✓. Per module: artifacts 93.4%, store 95.3%, provenance 97.2%, mfdr 97.7%, metrics 98.8%, chain 98.9%. **No `__all__` function uncalled** ✓ |
| Reviewer perf probe (1M metric rows) | `verify_chain` **7.7 s** ✓; `put_metrics` 39.9k rows/s (first batch) → 12.2k rows/s (last batch; min 11.96k) ✓; `get_metric` 0.1 ms; database 1,055 MB |

## Definition of done (§9.2 WP-04; §4.6; §7.13; §10.3)

| DoD item | Status | Evidence |
|---|---|---|
| Deliverable: SQLite + artifacts | ✓ | WAL mode and STRICT tables. Artifacts under `runs/<run_id>/artifacts/` in four formats: JSON, NPZ, Arrow IPC (Parquet is blocked on this machine, R14) and bytes. Three hashes per artifact, verified on read |
| Deliverable: hash chain | ✓ global chain / ✗ record chain | Global chain: one chain over every write; `verify_chain` names the first bad row on single-row edits, insertions and deletions. Record chain: its formula contradicts §8.7 (R01) |
| Deliverable: metric registry | ✓ | Immutable definitions per id, an MRM approval row, and the `config/metrics/wp-NN.yaml` catalogue merged with a duplicate-id check (S-ADR-42) |
| Deliverable: provenance | ✓ | `get_provenance`: declared parents plus the producing run's manifest; runs link to their parent runs. Dangling pointers are accepted (R13) |
| Deliverable: mFDR table | ✓ with gaps | Fixed parameters, one wealth sequence across contracts, and the rejection rule. It misses rule-agnostic invariants and disagrees with `stats.AlphaInvesting` ranges (R08) |
| §4.6 test: tamper drill | ✓ (single bad row) | 10 drill variants. The "first" in "first bad row" is never tested with two or more bad rows: mutant M01 (`max` instead of `min`) survives (R05) |
| §4.6 test: UPDATE/DELETE rejected | ✓ | Parametrized over all 13 tables. `REPLACE INTO` bypasses the triggers (R04) |
| §4.6 test: artifact round trip with checksum | ✓ | Contracts model, model outside contracts, `DualSet`, container outside contracts, Arrow table, bytes |
| §4.6 test: metric definition change creates a new id | ✓ (refusal reading) | The registry refuses the change and suggests `@v2`; the caller defines the new id (R10) |
| §4.6 test: decision chain broken → error | ✓ | Stale `prev_hash` → `HashMismatch`; forged field → `HashMismatch`. Both use the non-§8.7 formula (R01) |
| §4.6 performance | ✓ | `put_metrics` ≥ 10k rows/s (25–40k fresh, ≥ 11.9k at 1M rows); `verify_chain` 1M rows 7.7 s < 60 s |
| §4.6 algorithm: triggers raise on UPDATE/DELETE of any table; one writer (file lock); readers unlimited | ✓ | `schema.sql` lines 97–123; `_WriterLock` with a turnstile; WAL readers |
| §7.13 drill `test_chain_verification` (edit a ledger row → `verify_chain` names the row) | ✓ | `test_an_edited_ledger_row_is_named` (seq 7) |
| §4.0 layering (registry → contracts only) | ✓ | Layering and allowlist tests green; the package-root import of `SYNTHETIC_FOOTER` is allowed |
| §1.12 labels | partial | JSON and Arrow artifacts of SYNTHETIC runs carry the footer; data classes are checked along run, artifact, metric and decision edges. Payload labels are unchecked (R07); `manifest.json` has no footer (R12) |
| §10.3 coverage | ✓ | 95.8%; every public function called |

## Findings (most severe first)

### WP04-R01: critical. The record-level hash formula contradicts §8.7, so spec-conformant decision records are refused

- **Where:**
  - `chain.py:44` (`_RECORD_CHAIN_FIELDS = {"prev_hash", "record_hash"}`) and `chain.py:120-145` (`record_hash`, `chain_record`, `verify_record_chain`).
  - Enforced by `store.py:904-907` (`append_decision`) and `store.py:1069` (`_verify_decisions`).
  - The `chain.py` module docstring (lines 19-21) applies the same rule to `ChatTurnRecord`.
- **What happens:**
  - §8.7 defines the decision-log chain as `record_hash = sha256(prev_hash ‖ canonical_json(record without record_hash))`, with the first `prev_hash = "sha256:" + 64 zeros`. So `prev_hash` is inside the hashed JSON.
  - The implementation hashes the record without **both** `prev_hash` and `record_hash`.
  - Probe on one SYNTHETIC `DecisionRecord`:
    - §8.7 gives `sha256:5a5108bd…`; the registry gives `sha256:cdbeaed5…`.
    - `append_decision` of the §8.7-hashed record raises `HashMismatch` (`HASH_MISMATCH`).
    - The registry-hashed record is accepted, and a §8.7 verifier would reject it.
- **Why critical:** these are exported contract helpers that other WPs will build against:
  - WP-27 `idm.append_decision` / `decision_log` writes `decision_log.jsonl` by §8.7.
  - WP-29 `tpa audit chain` "verifies both" the log and the registry (§9.4 #2).
  - WP-39 chains `chat_turn` records.

  Either the log or the registry chain fails verification. The decision log is a governance record (G9).
- **Fix:**
  - Hash `canonical_json(record.model_dump(exclude={"record_hash"}))`, keeping `prev_hash` in the JSON.
  - Make `chain_record`, `verify_record_chain` and `_verify_decisions` follow.
  - Add a golden test that computes §8.7's formula with `hashlib` on a fixed record, and assert `append_decision` accepts it.
  - State in the docstring that the same formula governs `ChatTurnRecord`, and raise it with WP-39.

### WP04-R02: high. Decision outcomes are stored as new versions of the whole record; §8.7 appends separate `outcome` records, and the registry cannot mirror that log

- **Where:**
  - `store.py:103` (`_DECISION_MUTABLE = {"outcomes", "signposts", …}`) and `store.py:888-921`.
  - Test: `test_decision_versions_change_only_outcomes_and_signposts`.
- **What happens:**
  - §8.7: "Outcomes (Brier scores at 1, 4 and 8 quarters) are appended as new `outcome` records referencing the `decision_id`; nothing is edited. The registry mirrors the chain."
  - The registry instead re-appends the full `DecisionRecord` with `outcomes` filled in, and also lets `signposts` change. The latest version wins.
  - `append_decision` accepts only `DecisionRecord`, so the registry cannot hold §8.7's `outcome` records. A log written to §8.7 therefore cannot be mirrored record for record.
  - Second ambiguity: the registry keeps **one global** decision chain (the head is the last decision of any quarter). But `decision_log.jsonl` lives in `runs/<quarter>/pack/` and starts at the genesis hash. If WP-27 writes one log per quarter, the second quarter's first record (prev = genesis) is refused.
- **Fix:**
  - Decide with WP-27 and the WP-01 owner. Either:
    - (a) add an `OutcomeRecord` contract (decision_id, horizon, `OutcomeScore`, `prev_hash`, `record_hash`) and an `append_outcome` method on the same decision chain, keeping `DecisionRecord` immutable; or
    - (b) amend §8.7 to the versioning design.
  - Fix whether the chain is per quarter or cumulative.
  - Record the decision as a deviation until then.

### WP04-R03: high. `get_metric` serves evidence from ABORTED, FAILED and unfinished runs by default

- **Where:** `store.py:771-793` (`ORDER BY m.seq DESC LIMIT 1`, no run-status filter) and `store.py:795-804` (`list_metrics`).
- **What happens:**
  - Probe: run A ends OK with 0.004. Run B writes 0.09 and ends `ABORTED` (error `SEAL_BREACH`). `get_metric("tier1.t6.cp_upper@v1")` returns **0.09 from the ABORTED run**.
  - A third run, still `STARTED`, then writes 0.5, and `get_metric(…, plane=SEARCH)` returns 0.5.
  - Nothing in the returned `MetricInstance` reveals the run status.
- **Why high:**
  - §7.6 freezes an ABORTED campaign as an incident record. §1.10 routes hash mismatches and seal breaches to ABORTED.
  - The obvious consumer path is `idm.resolve_evidence` (EvidenceSpec = metric, by, plane, max_age_days; no run scope). It maps onto `get_metric(metric, plane=…, by=…)` and would print aborted or in-flight numbers in briefs instead of "EVIDENCE MISSING".
  - The claims renderer and the analyst build on the same default.
- **Fix:**
  - By default, consider only instances whose run ended `OK`.
  - Add a keyword-only `status: Collection[str] = ("OK",)` (or `include_open=False`) to `get_metric` and `list_metrics`.
  - Test the default against FAILED, ABORTED and STARTED runs.
  - Document the semantics for WP-25, WP-27 and WP-39.

### WP04-R04: medium. Tamper evidence is weaker than the code and drill claim

- **Where:**
  - `schema.sql:97-123`: BEFORE UPDATE and BEFORE DELETE triggers only.
  - `chain.py:15-17`: "the head … belongs in manifests and audit output".
  - `tests/drills/test_chain_verification.py:2-3`: "drops the append-only trigger it needs, as a tamperer must".
- **What happens:**
  - **REPLACE bypass.** `REPLACE INTO chain …` replaced row 2 with **no trigger firing and triggers intact**. A writable `Registry` then opened the file without complaint. SQLite fires delete triggers for REPLACE only under `recursive_triggers`, which is off by default. The hash check still caught the edit (`first_bad_seq = 2`, "row hash rewritten"), but the "missing trigger" evidence and the writable-open refusal never trigger. REPLACE also deletes index rows without a trigger.
  - **Re-chain with trigger restore.** Drop `chain_no_update`, change a metric value 0.0062 → 0.0001, recompute the hashes of the rows after it, then recreate the trigger. The result: writable open OK, `verify_chain` **ok=True**, `get_metric` returns 0.0001.
  - **No anchor in code.** Nothing records the head outside the database. `RunEnd` has no head, there is no `verify_chain(anchor=…)`, and nothing writes the head into `manifest.json` or the pack. Only decision and mFDR rows have a second, record-level chain.
  - §4.6 only demands detection of a row edit, which works. The documentation implies more.
- **Fix:**
  - Add `BEFORE INSERT` guard triggers that reject an insert whose primary key or unique key already exists. This closes REPLACE.
  - Add a chain-level guard: `NEW.seq = max(seq) + 1` and `NEW.prev_hash = last row_hash`.
  - Add `verify_chain(*, anchors: Sequence[tuple[int, str]] = ())`, and write `(seq, head)` to `runs/<run_id>/chain_head.json` at `end_run` so `tpa audit chain` can check it.
  - Correct the drill docstring.

### WP04-R05: medium. Weak tests: 8 meaningful mutants survive, including the drill's own "first bad row" property and evidence hiding

- **Where:** see Appendix A. 48 mutants: 36 killed, 12 survived. Of the survivors, 2 are behaviour-neutral or masked by the file hash (M26, M36) and 2 are masked by redundant checks (M04, M45).
- **Meaningful survivors:**
  - **M01:** `first_bad_seq = max(seqs)`. No test has two bad rows at different seqs, so "reports the **first** bad row" (§4.6) is unpinned.
  - **M03:** the "chain row has no index row" check removed. Probe E1: drop `metrics_no_delete`, delete one metric's index row, recreate the trigger. The metric vanishes from `get_metric` (`EvidenceMissing`), and **only this check** catches it in `verify_chain`. No drill deletes an index row.
  - **M02:** the decision `prev_hash` link check in `verify_chain` removed. The issue line (`store.py:1068`) and the unreadable-record branch (1064-1066) are never executed.
  - **M08:** `get_metric`'s index-versus-chain cross-check removed.
  - **M50:** a schema-version mismatch accepted.
  - **M39:** `family_size ≥ 1` unchecked.
  - **M09 / M10:** decision and claim immutability are each tested on a single field. Making `rationale` (decision) or `placeholders` (claim) mutable survives.
- **Fix:** add these drills and tests:
  - two independent edits, asserting `first_bad_seq` is the lower one;
  - index-row deletion with the trigger restored;
  - a re-chained deletion of a decision row, which only the decision link check catches;
  - a schema-version mismatch on open;
  - parametrized immutability over every non-mutable `DecisionRecord` and `ClaimRecord` field;
  - `family_size = 0`.

### WP04-R06: medium. Plane labels: only "SEALED ⇒ FINAL run" is enforced; an EXPLORATION run can write SEARCH-grade evidence

- **Where:** `store.py:759-761`.
- **What happens:** probe results:
  - an EXPLORATION-plane run writes a `MetricInstance` with `plane=SEARCH`;
  - a FINAL run writes `EXPLORATORY`;
  - a CALIBRATION run writes `SEARCH`.

  All are accepted. The claims validator's `WRONG_PLANE` rule and the room read `MetricInstance.plane`. Analyst what-ifs are "exploration grade" (S-ADR-34). A producer bug can therefore launder exploratory numbers into search-grade evidence, and the registry, which already checks one direction, does not stop it.
- **Fix:**
  - Enforce the full mapping: SEARCH run ⇒ `search`; EXPLORATION run ⇒ `exploratory`; FINAL run ⇒ `sealed`; CALIBRATION and HISTORICAL ⇒ `exploratory`, unless the spec owner says otherwise.
  - Test every pair.
  - Record the mapping as a deviation and raise it as a contract note.

### WP04-R07: medium. Payload labels are not checked: SYNTHETIC and REAL meet silently inside artifacts and ledger rows

- **Where:** `artifacts.py:176-206` (`write_artifact` labels by the run only) and `store.py:807-817` (`append_ledger`).
- **What happens:**
  - Probe E2: a `MetricInstance` with `data_class=REAL` stored as an artifact of a SYNTHETIC run is accepted. The artifact is labelled SYNTHETIC while `get_artifact` returns a REAL payload.
  - Probe P16: the same object is appended to the ledger next to a SYNTHETIC run without complaint.
  - §1.12 rule 2 says SYNTHETIC and REAL together raise `DataClassMixError`.
- **Fix:**
  - In `put_artifact` and `append_ledger`, read the payload's top-level `data_class` (and `is_synthetic`) when the model has one. Nested models are optional.
  - Raise `DataClassMixError` on disagreement with the run (for ledgers: with the run named in the payload, if any).
  - Test both.

### WP04-R08: medium. The mFDR table misses rule-agnostic invariants, disagrees with `stats.AlphaInvesting` on parameter ranges, and is never replayed against it

- **Where:**
  - `mfdr.py:7-12` (docstring: "enforces what any alpha-investing record must satisfy"), `mfdr.py:50-56` and `mfdr.py:72-84`.
  - Compare `stats/multiple.py:59-65, 103-111`.
- **What happens:**
  - **Missing invariants.** Probe P8 accepts all of these:
    - a test at `alpha_level = 0.5` with wealth 0.05;
    - wealth rising 0.049 → 0.9 **without a rejection**;
    - the same `(contract_id, hypothesis_id)` recorded twice.

    Two invariants follow from the generalized α-investing update W_j = W_{j−1} − φ_j + R_j·ψ_j with φ_j ≤ W_{j−1}, and from WP-02's rule. They need no `stats` import:
    - no rejection ⇒ W_j ≤ W_{j−1};
    - a bounded test level: α_j ≤ W_{j−1} under WP-02's rule (α_j = φ_j/(1 + φ_j), φ_j = (1 − δ)·W_{j−1}), and α_j ≤ W_{j−1}/(1 − payout) for any GAI rule with a non-negative reward.
  - **Range mismatch** (WP-02 `AlphaInvesting` versus `MFDRConfig`):
    - `decay`: [0, 1) versus (0, 1]. The research's all-in rule `decay = 0`, which WP-02 documents, cannot be configured.
    - `payout`: (0, 1) versus [0, 1].
    - `w0`: > 0 versus (0, 1).
  - **Rejection rule at zero stake.** WP-02 never rejects when the stake is 0. The registry demands `rejected == (p ≤ α)`, which would refuse WP-02's own record at p = α = 0.
  - **Test values.** The test's wealth path (0.05 → 0.04 after an acceptance at α = 0.01) is not what `AlphaInvesting(0.05, 0.05, 0.9)` produces: stake 0.005 at level 0.004975 gives 0.045.
- **Fix:**
  - Add the two invariants (the level bound in its rule-agnostic form α ≤ W/(1 − payout)), plus optional uniqueness of `(contract_id, hypothesis_id)`.
  - Align the ranges with WP-02, or document why they differ.
  - Accept `rejected=False` when `alpha_level == 0`.
  - Add a test (tests may import `stats`) that drives `AlphaInvesting` through 50 seeded p-values, records each step with `level`, `test` and `wealth`, and checks that `p_values()` replays to the same wealth and rejections.

### WP04-R09: medium. No public transactional API for CHAT_ANALYST's atomic check-and-reserve (and link-and-append)

- **Where:** `store.py:416-429` (`_transaction` is private); CHAT_ANALYST §3.6 (line 208) and §9.3 (line 694).
- **What happens:**
  - "Quotas, spend and core-hours are registry aggregates; each check-and-reserve runs in one SQLite `BEGIN IMMEDIATE` transaction, so every surface process shares the same limits." This applies in increment 1 (W1 30 an hour, chat spend caps).
  - The registry offers only single appends. WP-39 must therefore either race (read the aggregate, then append) or reach into `Registry._transaction`, as `MFDRLedger` does from inside the package.
  - `append_decision` has the same race: `decision_head()` then append.
- **Fix:**
  - Add a public, documented hook. For example, `append_ledger_if(kind, payload, *, check: Callable[[RegistryView], None])`, which runs `check` and the append in one write transaction, or a narrow `reserve(kind, payload, *, aggregate_sql_key, limit)`.
  - Raise it as a contract item for WP-39 before the freeze.

### WP04-R10: low. `define_metric` refuses a changed definition instead of "creating a new id"; the MRM approval flag is never consulted

- **Where:** `store.py:668-705`.
- **What happens:**
  - The §4.6 comment ("new id on any definition change") and test name ("metric definition change creates a new id") are implemented as **refuse and suggest** `@v<k+1>`. Probe P9: a `code_hash` change raises `SchemaError` with `suggested = tier1.t6.cp_upper@v2`. This is a sensible reading, because `define_metric` returns `None` and could not report an auto-created id. It still needs recording.
  - Approval is a free-text `approver` string. Repeat approvals are accepted, and `put_metrics` and `get_metric` never consult approval (P10).
- **Fix:**
  - Record the reading as a deviation and tell WP-24, which registers the catalogue.
  - Decide whether unapproved metrics may be cited, at least in REAL mode, and whether approval should be a `SignOff` (S-ADR-40).

### WP04-R11: low. The run manifest is frozen at `begin_run`; fields that accumulate during a run cannot be recorded

- **Where:** `store.py:110-116` (`RunEnd`: status, error and artifact hashes only) and `end_run` (signature as §4.6).
- **What happens:** `RunManifest.solver_records`, `llm_calls`, `cache_keys` and `effective_config_hashes` (§3.15; ARCH §10.2) are produced while a run executes. A run registered at its start can never carry them, and golden manifests compare these fields bit for bit.
- **Fix:** confirm the intended flow with WP-17, WP-18 and WP-24 (register only after compute?). Otherwise add a keyword-only `manifest_updates` to `end_run`, restricted to those accumulating fields and hashed into `RunEnd`.

### WP04-R12: low. `runs/<run_id>/manifest.json` is unverified and unlabelled

- **Where:** `store.py:510-515`.
- **What happens:**
  - Probe P7: editing `config_hash` in `manifest.json` leaves `verify_chain` **ok=True**, although `get_manifest` (from the chain) still has the true value.
  - `testing.assert_manifest_reproduces(manifest_path)` (§4.5) reads manifests from disk.
  - The file carries `data_class` but not the SYNTHETIC footer (§1.12 rule 3, "every … JSON artifact").
- **Fix:**
  - Compare `manifest.json` with the chain-derived manifest in `verify_chain` (`check_artifacts=True`).
  - Write it in the labelled envelope, or add the footer as a sibling file, and document it for WP-03.

### WP04-R13: low. `get_provenance` echoes a dangling JSON pointer as a valid node

- **Where:** `store.py:942-957`.
- **What happens:** probe P6: `get_provenance("<run>:card:/no/such/field")` returns a node, while `get_artifact` on the same reference raises `EvidenceMissing`. A consumer that uses provenance as an existence check, such as the claims validator or the analyst, accepts typos.
- **Fix:** resolve the pointer (or check it resolves) before returning a node, or document the behaviour loudly. Add a test.

### WP04-R14: low (deviation, justified). Arrow IPC replaces Parquet for table artifacts

- **Where:** `artifacts.py:10-13`.
- **Evidence:** `import pyarrow.parquet` fails with "DLL load failed while importing _parquet: An Application Control policy has blocked this file". The deviation is necessary on this machine.
- **Wider impact:** WP-05's bitemporal store (§2 "bitemporal Parquet") and §3.17 ("PathMetrics … streamed per block to Parquet") are hit by the same policy.
- **Fix:** record the deviation, and raise a spec-level note for the spec owner and WP-05 (an allow-list exception, or Arrow IPC throughout).

### WP04-R15: low. `canonical_hash` of table, NPZ and bytes artifacts is the raw checksum

- **Where:** `artifacts.py:184-204`.
- **What happens:** only JSON artifacts normalize `VOLATILE_FIELDS`. A table with a `run_id` or timestamp column, or bytes such as HTML or a payload containing run ids, gets a different canonical hash on every rerun. That breaks §9.4 #9 and §10.5 golden-manifest reproduction.
- **Fix:** document that producers must keep volatile values out of non-JSON artifacts, or normalize table columns whose names are in `VOLATILE_FIELDS`.

### WP04-R16: low. `get_metric` details and non-`TPAError` leaks

- **`by` semantics:** `by=None` matches only undimensioned instances (P11). This is reasonable but undocumented in the spec; record it.
- **Incomplete cross-check:** the index-versus-chain check (`store.py:790`) covers metric id, `by` and run but not **plane**. A tampered `plane` index makes a SEARCH instance answer a SEALED query until `verify_chain` runs.
- **Error leaks:**
  - `get_metric(…, plane="SEALED")` raises a bare `ValueError` (P13), because `EvidencePlane` values are lower case.
  - On Windows, `os.replace` in `_write_manifest_file` raises `PermissionError` if a reader holds `manifest.json` open, after the database commit.
- **Fix:** add plane to the cross-check, wrap enum coercion in `SchemaError`, and catch `OSError` around the manifest file write (log it, and let `get_manifest` stay authoritative).

### WP04-R17: low. The perf test measures throughput only on an empty store

- **Where:** `tests/perf/test_registry_perf.py:42-48`.
- **What happens:** throughput falls from 40k to about 12k rows/s at 1M rows, a thin margin over the 10k budget. The 1M-row test spends about 127 of its 135 s building the store.
- **Fix:** also assert the rate of the last batch inside the 1M-row test, and consider building the 1M rows with raw inserts.

### WP04-R18: low. Metric catalogue model placement; one vacuous test

- **Placement:** `MetricCatalogEntry` and `MetricCatalogFile` (`metrics.py:40-63`, marked `TODO(contracts)`) are the input type of every WP's `config/metrics/wp-NN.yaml`. They are read by claims (aliases) and the analyst (scope, label). §3.18 puts cross-WP input types in `contracts`. The workaround is correct, but the type must move before the freeze or be explicitly accepted.
- **Vacuous test:** `test_packaged_catalog_loads` asserts over an empty catalogue, because `config/metrics/` does not exist yet.
- **Fix:** raise a contract note for WP-01. Make the test also require at least one file once WPs land, or mark it as such.

### WP04-R19: low. Miscellaneous

- **Read-only handle writes:** a read-only handle creates directories via `log_path` (probe E3; CHAT_ANALYST §9.6).
- **Unverified record chains:** `verify_chain` checks the decision and mFDR record chains but not `ChatTurnRecord` chains appended as `chat_turn` ledger rows.
- **Issue truncation:** after `MAX_ISSUES`, a lower-seq issue from a later pass can be dropped, misattributing `first_bad_seq` in a mass corruption.
- **Forecast scores:** §4.6's purpose names a "forecast-score" store, but there is no documented representation (metric instances with `by` dimensions? artifacts?). Tell WP-14.

### WP04-R20: low (integration, other owners)

- **Walking skeleton (WP-03):** it calls no `Registry` method, although §4.5 requires every cross-WP function of §4 once. The registry is consumed by WP-24 to WP-29 and WP-39.
- **`.gitignore` (orchestrator / WP-01):** it ignores `runs/*` but not `stores/`. `DEFAULT_DB_PATH = stores/registry.sqlite` and its `-wal`, `-shm` and `.lock` files would be committed.

### WP04-R21: low. Deviations visible in code that must be in the implementer's deviation list (verify)

1. Global row hash over the envelope `{body, class, kind, recorded_at}`, not the payload alone. `‖` is the ASCII `sha256:<hex>` text followed by the UTF-8 JSON; genesis is `sha256:` plus 64 zeros. This is stronger (it binds kind and append time) but differs from §4.6's literal formula.
2. Record chain without `prev_hash` in the JSON (R01).
3. Decision versions instead of outcome records (R02).
4. Ledger kinds extended with the 10 CHAT_ANALYST §11 kinds; read-only handles may append exactly those (CHAT_ANALYST §9.6).
5. Arrow IPC instead of Parquet (R14).
6. `define_metric` refuses and suggests `@v<k+1>`; approval is a separate row with a free-text approver (R10).
7. `get_metric`: `by=None` means undimensioned, and "latest" is chain order across all runs (R03, R16).
8. Claims are versioned on the audit fields only, and the latest version wins.
9. Artifact naming rules:
   - names match `[A-Za-z0-9_-][A-Za-z0-9_.-]{0,127}`;
   - they are unique regardless of case;
   - `manifest` is reserved, and `<run_id>:manifest:` names the run;
   - Windows device names are refused.
10. JSON artifacts are a labelled envelope. Models outside `contracts` come back as JSON unless `model=` is given.
11. Writer lock `<db>.lock` plus `BEGIN IMMEDIATE`; 60 s timeouts raise `ExecutionFailed`.
12. Read-only refusals raise `EntitlementDenied` (rule `REGISTRY_READONLY`). Missing triggers on open raise `HashMismatch`.
13. `MetricCatalogEntry` and `MetricCatalogFile` with an `owner_wp` field; the `wp-NN.yaml` naming is enforced.
14. The mFDR ledger records tests computed by the lab, because the registry cannot import `stats`.
15. SEALED metrics only from FINAL runs.

## Appendix A: mutation testing (scratch copy; WP-04 unit, drill and property tests; `-x -m "not slow"`)

| Mutant (one plausible bug) | Result |
|---|---|
| M00 sanity: the row hash ignores `prev_hash` | KILLED (harness valid) |
| M05 SEALED from any plane · M06 unit check · M07 oldest instance · M11–M14 data-class edges (decision, metric, artifact parent, parent run) · M15 mFDR wealth sequence · M16 artifact files skipped · M17 read-only accepts writes · M18 manifest hashes use the raw checksum · M19 decision `prev_hash` · M20 decision `record_hash` · M21 ended runs stay open · M22 non-STARTED manifest · M23 writable open ignores missing triggers · M24 no WAL · M25 identical claim re-appended · M27 broken links ignored · M28 missing seqs ignored · M29 rewritten row attributed to its successor · M30 record hash ignores a field · M31 footer dropped · M32 canonical hash not normalized · M33 file sha256 unchecked · M34 reserved name accepted · M35 containers not validated · M37 rejection rule · M38 mFDR parameters mutable · M40 negative wealth · M41 `next_version` · M42 `owner_wp` mismatch · M43 provenance omits the run · M44 pointer index off by one · M47 parents dropped · M49 final manifest drops hashes | KILLED (36) |
| **M01 `first_bad_seq = max` · M02 decision link check in `verify_chain` · M03 "chain row has no index row" · M08 `get_metric` cross-check · M09 decision `rationale` mutable · M10 claim `placeholders` mutable · M39 `family_size` · M50 schema-version mismatch** | **SURVIVED (8 meaningful)** |
| M04 unknown kinds; M45 kind column versus envelope (both masked by index derivation); M26 `define_metric` fast path (behaviour-neutral); M36 JSON body checksum outside contracts (masked by the file sha256) | SURVIVED (4, by design) |

## Appendix B: probes (reviewer scratch scripts; not in the repo)

1. `import pyarrow.parquet` is blocked by Application Control (R14).
2. `REPLACE INTO chain` succeeds with triggers intact; a writable open is accepted; `verify_chain` names seq 2 (R04).
3. Drop trigger, edit a metric value, re-chain, restore the trigger: `verify_chain` ok=True and the value reads 0.0001 (R04).
4. `get_metric` returns 0.09 from an ABORTED run, then 0.5 from a STARTED run (R03).
5. An EXPLORATION run writes SEARCH evidence; a FINAL run writes EXPLORATORY; a CALIBRATION run writes SEARCH (R06).
6. `get_provenance` accepts a dangling pointer (R13).
7. An edited `manifest.json` passes `verify_chain`; it has no footer (R12).
8. mFDR accepts α = 0.5 at W = 0.05, a wealth rise without rejection, and a duplicate hypothesis (R08).
9. A `code_hash` change raises `SchemaError` suggesting `@v2` (R10).
10. An unapproved metric serves instances; repeat free-text approvals are accepted (R10).
11. `by=None` raises `EvidenceMissing` when only dimensioned instances exist (R16).
12. `put_metrics` after `end_run` is refused ✓.
13. `get_metric(plane="SEALED")` raises a bare `ValueError` (R16).
14. The §8.7 record hash differs from `chain.record_hash`; `append_decision` refuses the §8.7 record (R01).
15. Deleting an index row with the trigger restored hides the metric; only the M03 check catches it (R05).
16. A REAL payload is accepted in a SYNTHETIC run's artifact and in the ledger (R07).
17. A read-only handle creates `runs/<run>/logs` (R19).
18. 1M rows: `verify_chain` 7.7 s; `put_metrics` ≥ 11.96k rows/s; `get_metric` 0.1 ms (perf ✓).

## Contract issues to raise (outside WP-04's files)

- **R01 (spec owner, WP-27, WP-29, WP-39):** one record-chain formula, §8.7's, for `DecisionRecord` and `ChatTurnRecord`.
- **R02 (WP-01, WP-27, spec owner):**
  - an `OutcomeRecord` contract, or an amendment of §8.7 to versioning;
  - whether `decision_log.jsonl` is per quarter (genesis per quarter) or cumulative.
- **R03 (WP-25, WP-27, WP-39):** the run-status semantics of `get_metric` and `list_metrics`.
- **R06 (spec owner):** the `Plane` → `EvidencePlane` mapping the registry must enforce.
- **R08 (WP-02, WP-38):** align the `AlphaInvesting` and `MFDRConfig` ranges, and the zero-stake rejection rule.
- **R09 (WP-39):** a public transactional check-and-reserve API in the registry.
- **R11 (WP-17, WP-18, WP-24):** the manifest-completion flow (solver records, LLM calls, cache keys).
- **R14 (spec owner, WP-05):** Parquet is blocked on the reference machine.
- **R18 (WP-01):** move `MetricCatalogEntry` and `MetricCatalogFile` into `contracts` before `contracts-v1.0`, or accept their registry home explicitly.
- **R20 (WP-03, orchestrator):**
  - the walking skeleton should exercise the `Registry` (`begin_run` → `put_artifact` → `put_metrics` → `end_run` → `get_metric` → `verify_chain`);
  - add `stores/` to `.gitignore`.
