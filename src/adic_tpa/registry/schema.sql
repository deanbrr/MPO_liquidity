-- Registry schema (BUILD_SPEC v1.1 §4.6; owner WP-04). SYNTHETIC - NOT ADIC DATA in every synthetic build.
--
-- `chain` holds every registry record as a canonical-JSON envelope, hash-chained row to row
-- (row_hash = sha256(prev_hash || payload); adic_tpa.registry.chain). The other tables only index `chain` for
-- lookups: each row points at its chain row by `seq` and holds nothing that cannot be derived from that row's
-- envelope, and verify_chain re-derives every index column. Every table is append-only: the triggers at the
-- end raise on UPDATE and DELETE. Applied once, when the database is created (WAL mode is set by the store).

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS chain (
    seq       INTEGER PRIMARY KEY,           -- 1, 2, 3, ... without gaps
    kind      TEXT NOT NULL,                 -- the envelope's kind
    payload   TEXT NOT NULL,                 -- {"body","class","kind","recorded_at"} canonical JSON
    prev_hash TEXT NOT NULL,
    row_hash  TEXT NOT NULL UNIQUE
) STRICT;
CREATE INDEX IF NOT EXISTS chain_by_kind ON chain (kind, seq);

CREATE TABLE IF NOT EXISTS runs (                          -- kind 'run': the RunManifest at begin_run
    seq    INTEGER PRIMARY KEY REFERENCES chain (seq),
    run_id TEXT NOT NULL UNIQUE,
    kind   TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS run_ends (                      -- kind 'run_end': status, error, artifact hashes
    seq    INTEGER PRIMARY KEY REFERENCES chain (seq),
    run_id TEXT NOT NULL UNIQUE REFERENCES runs (run_id),
    status TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS artifacts (                     -- kind 'artifact': ArtifactInfo
    seq    INTEGER PRIMARY KEY REFERENCES chain (seq),
    run_id TEXT NOT NULL REFERENCES runs (run_id),
    name   TEXT NOT NULL,
    UNIQUE (run_id, name)
) STRICT;
-- NTFS file names are case-blind, so artifact names are unique case-blind within a run
CREATE UNIQUE INDEX IF NOT EXISTS artifacts_casefold ON artifacts (run_id, lower(name));

CREATE TABLE IF NOT EXISTS metric_defs (                   -- kind 'metric_def': MetricDef (immutable per id)
    seq       INTEGER PRIMARY KEY REFERENCES chain (seq),
    metric_id TEXT NOT NULL UNIQUE,
    def_hash  TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS metric_approvals (              -- kind 'metric_approval': MRM approval of a definition
    seq       INTEGER PRIMARY KEY REFERENCES chain (seq),
    metric_id TEXT NOT NULL REFERENCES metric_defs (metric_id)
) STRICT;

CREATE TABLE IF NOT EXISTS metrics (                       -- kind 'metric': MetricInstance
    seq       INTEGER PRIMARY KEY REFERENCES chain (seq),
    metric_id TEXT NOT NULL REFERENCES metric_defs (metric_id),
    run_id    TEXT NOT NULL REFERENCES runs (run_id),
    plane     TEXT NOT NULL,
    by_key    TEXT NOT NULL,                 -- canonical JSON of MetricInstance.by
    UNIQUE (metric_id, by_key, run_id, plane)
) STRICT;
CREATE INDEX IF NOT EXISTS metrics_by_run ON metrics (run_id, metric_id);

CREATE TABLE IF NOT EXISTS claims (                        -- kind 'claim': ClaimRecord versions (latest wins)
    seq      INTEGER PRIMARY KEY REFERENCES chain (seq),
    claim_id TEXT NOT NULL,
    doc_id   TEXT NOT NULL
) STRICT;
CREATE INDEX IF NOT EXISTS claims_by_id ON claims (claim_id, seq);
CREATE INDEX IF NOT EXISTS claims_by_doc ON claims (doc_id, seq);

CREATE TABLE IF NOT EXISTS decisions (                     -- kind 'decision': DecisionRecord versions, own chain
    seq         INTEGER PRIMARY KEY REFERENCES chain (seq),
    decision_id TEXT NOT NULL,
    record_hash TEXT NOT NULL UNIQUE
) STRICT;
CREATE INDEX IF NOT EXISTS decisions_by_id ON decisions (decision_id, seq);

CREATE TABLE IF NOT EXISTS ledger (                        -- kind 'ledger.<kind>': append_ledger payloads
    seq  INTEGER PRIMARY KEY REFERENCES chain (seq),
    kind TEXT NOT NULL
) STRICT;
CREATE INDEX IF NOT EXISTS ledger_by_kind ON ledger (kind, seq);

CREATE TABLE IF NOT EXISTS mfdr_config (                   -- kind 'mfdr_config': at most one row
    seq INTEGER PRIMARY KEY REFERENCES chain (seq),
    one INTEGER NOT NULL UNIQUE CHECK (one = 1)
) STRICT;

CREATE TABLE IF NOT EXISTS mfdr_tests (                    -- kind 'mfdr_test': the online test sequence
    seq         INTEGER PRIMARY KEY REFERENCES chain (seq),
    contract_id TEXT NOT NULL
) STRICT;
CREATE INDEX IF NOT EXISTS mfdr_by_contract ON mfdr_tests (contract_id, seq);

-- Append-only: UPDATE and DELETE raise on every table (§4.6).
CREATE TRIGGER IF NOT EXISTS meta_no_update BEFORE UPDATE ON meta BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on meta'); END;
CREATE TRIGGER IF NOT EXISTS meta_no_delete BEFORE DELETE ON meta BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on meta'); END;
CREATE TRIGGER IF NOT EXISTS chain_no_update BEFORE UPDATE ON chain BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on chain'); END;
CREATE TRIGGER IF NOT EXISTS chain_no_delete BEFORE DELETE ON chain BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on chain'); END;
CREATE TRIGGER IF NOT EXISTS runs_no_update BEFORE UPDATE ON runs BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on runs'); END;
CREATE TRIGGER IF NOT EXISTS runs_no_delete BEFORE DELETE ON runs BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on runs'); END;
CREATE TRIGGER IF NOT EXISTS run_ends_no_update BEFORE UPDATE ON run_ends BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on run_ends'); END;
CREATE TRIGGER IF NOT EXISTS run_ends_no_delete BEFORE DELETE ON run_ends BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on run_ends'); END;
CREATE TRIGGER IF NOT EXISTS artifacts_no_update BEFORE UPDATE ON artifacts BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on artifacts'); END;
CREATE TRIGGER IF NOT EXISTS artifacts_no_delete BEFORE DELETE ON artifacts BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on artifacts'); END;
CREATE TRIGGER IF NOT EXISTS metric_defs_no_update BEFORE UPDATE ON metric_defs BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on metric_defs'); END;
CREATE TRIGGER IF NOT EXISTS metric_defs_no_delete BEFORE DELETE ON metric_defs BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on metric_defs'); END;
CREATE TRIGGER IF NOT EXISTS metric_approvals_no_update BEFORE UPDATE ON metric_approvals BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on metric_approvals'); END;
CREATE TRIGGER IF NOT EXISTS metric_approvals_no_delete BEFORE DELETE ON metric_approvals BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on metric_approvals'); END;
CREATE TRIGGER IF NOT EXISTS metrics_no_update BEFORE UPDATE ON metrics BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on metrics'); END;
CREATE TRIGGER IF NOT EXISTS metrics_no_delete BEFORE DELETE ON metrics BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on metrics'); END;
CREATE TRIGGER IF NOT EXISTS claims_no_update BEFORE UPDATE ON claims BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on claims'); END;
CREATE TRIGGER IF NOT EXISTS claims_no_delete BEFORE DELETE ON claims BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on claims'); END;
CREATE TRIGGER IF NOT EXISTS decisions_no_update BEFORE UPDATE ON decisions BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on decisions'); END;
CREATE TRIGGER IF NOT EXISTS decisions_no_delete BEFORE DELETE ON decisions BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on decisions'); END;
CREATE TRIGGER IF NOT EXISTS ledger_no_update BEFORE UPDATE ON ledger BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on ledger'); END;
CREATE TRIGGER IF NOT EXISTS ledger_no_delete BEFORE DELETE ON ledger BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on ledger'); END;
CREATE TRIGGER IF NOT EXISTS mfdr_config_no_update BEFORE UPDATE ON mfdr_config BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on mfdr_config'); END;
CREATE TRIGGER IF NOT EXISTS mfdr_config_no_delete BEFORE DELETE ON mfdr_config BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on mfdr_config'); END;
CREATE TRIGGER IF NOT EXISTS mfdr_tests_no_update BEFORE UPDATE ON mfdr_tests BEGIN SELECT RAISE(ABORT, 'registry is append-only: UPDATE on mfdr_tests'); END;
CREATE TRIGGER IF NOT EXISTS mfdr_tests_no_delete BEFORE DELETE ON mfdr_tests BEGIN SELECT RAISE(ABORT, 'registry is append-only: DELETE on mfdr_tests'); END;
