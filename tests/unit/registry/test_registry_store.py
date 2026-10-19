"""Registry store (BUILD_SPEC v1.1 §4.6): runs, metrics, ledger, claims, decisions, read-only handles, append-only
triggers, WAL mode and concurrent writers. Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import json
import sqlite3
import threading
from types import SimpleNamespace
from typing import get_args

import pytest

from adic_tpa.contracts.analyst import ANALYST_LEDGER_KINDS
from adic_tpa.contracts.enums import DataClass, EvidencePlane, KeyValue, Plane
from adic_tpa.contracts.errors import (
    DataClassMixError, EntitlementDenied, EvidenceMissing, ExecutionFailed, HashMismatch, SchemaError, UnitError,
)
from adic_tpa.contracts.evidence import EvalRequest, RunManifest
from adic_tpa.contracts.hashing import canonical_json
from adic_tpa.registry import Registry
from adic_tpa.registry.chain import GENESIS_HASH, chain_record
from adic_tpa.registry.store import (
    DEFAULT_ARTIFACT_ROOT, DEFAULT_DB_PATH, EXPECTED_TRIGGERS, LAB_LEDGER_KINDS, LEDGER_KINDS, TABLES, AnalystLedgerKind,
)


def _eval_request(n: int = 1) -> EvalRequest:
    return EvalRequest(request_id=f"r{n}", campaign_id="cmp-2026Q4-1", attempt_id=f"a{n}", spec_hash="sha256:" + "a" * 64,
                       kind="evaluate")


# ------------------------------------------------------------------------------------------------ database
def test_database_is_wal_mode_with_append_only_triggers(reg: Registry, paths: SimpleNamespace) -> None:
    assert reg.db_path == paths.db and reg.artifact_root == paths.root and not reg.readonly
    assert reg.run_dir("run-20261018T091500Z-3f2a9c1d") == paths.root / "run-20261018T091500Z-3f2a9c1d"
    with pytest.raises(SchemaError):
        reg.run_dir("../escape")
    log = reg.log_path("run-20261018T091500Z-3f2a9c1d", "evaluator")
    assert log == paths.root / "run-20261018T091500Z-3f2a9c1d" / "logs" / "evaluator.jsonl" and log.parent.is_dir()
    assert DEFAULT_DB_PATH.as_posix() == "stores/registry.sqlite" and DEFAULT_ARTIFACT_ROOT.as_posix() == "runs"
    con = sqlite3.connect(paths.db)
    try:
        assert con.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        triggers = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'")}
        tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    finally:
        con.close()
    assert set(EXPECTED_TRIGGERS) <= triggers
    assert set(TABLES) <= tables


@pytest.mark.parametrize("table", TABLES)
def test_update_and_delete_are_rejected_on_every_table(run_reg: Registry, paths: SimpleNamespace, factory, table: str) -> None:
    run_reg.put_metrics([factory.metric()])
    run_reg.put_claim(factory.claim())
    run_reg.append_ledger("eval_request", _eval_request())
    run_reg.append_decision(factory.decision())
    run_reg.approve_metric("tier1.t6.cp_upper@v1", approver="MRM")
    run_reg.mfdr().configure(w0=0.05, payout=0.05, decay=0.9)
    run_reg.mfdr().record(contract_id="ctr-2026Q4-v1", hypothesis_id="h1", p_value=0.5, alpha_level=0.01,
                          rejected=False, wealth_after=0.04)
    run_reg.put_artifact(factory.RUN_A, "note", b"SYNTHETIC")
    run_reg.end_run(factory.RUN_A, "OK")
    con = sqlite3.connect(paths.db)
    try:
        assert con.execute(f"SELECT count(*) FROM {table}").fetchone()[0] >= 1
        column = con.execute(f"PRAGMA table_info({table})").fetchall()[-1][1]
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            con.execute(f"UPDATE {table} SET {column} = {column}")
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            con.execute(f"DELETE FROM {table}")
    finally:
        con.close()
    assert run_reg.verify_chain().ok


def test_reopening_keeps_the_chain(paths: SimpleNamespace, factory) -> None:
    with Registry(paths.db, paths.root) as reg:
        assert reg.chain_head() == (0, GENESIS_HASH)
        reg.begin_run(factory.manifest())
        head = reg.append_ledger("drill", _eval_request())
        assert reg.chain_head() == (2, head)
    with Registry(paths.db, paths.root) as reg:
        report = reg.verify_chain()
        assert report.ok and report.rows == 2 and report.head == head == reg.chain_head()[1]


def test_a_foreign_sqlite_file_is_refused(tmp_path) -> None:
    db = tmp_path / "other.sqlite"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE x (a)")
    con.commit()
    con.close()
    with pytest.raises(SchemaError, match="not a registry"):
        Registry(db, tmp_path / "runs")


# ------------------------------------------------------------------------------------------------ runs
def test_run_lifecycle_and_manifest_file(reg: Registry, paths: SimpleNamespace, factory) -> None:
    rid = reg.begin_run(factory.manifest())
    assert rid == factory.RUN_A
    on_disk = RunManifest.model_validate_json((paths.root / rid / "manifest.json").read_text(encoding="utf-8"))
    assert on_disk.status == "STARTED"
    assert reg.get_run(rid).status == "STARTED"
    reg.put_artifact(rid, "note", b"SYNTHETIC")
    reg.end_run(rid, "FAILED", error="engine fault")
    record = reg.get_run(rid)
    assert record.status == "FAILED" and record.error == "engine fault"
    final = RunManifest.model_validate_json((paths.root / rid / "manifest.json").read_text(encoding="utf-8"))
    assert final == record.manifest == reg.get_manifest(rid)
    assert final.status == "FAILED" and set(final.canonical_artifact_hashes) == {"note"}
    assert [r.manifest.run_id for r in reg.list_runs(kind="quarter")] == [rid]
    assert reg.list_runs(kind="other") == []


def test_run_rules(reg: Registry, factory) -> None:
    with pytest.raises(SchemaError, match="STARTED"):
        reg.begin_run(factory.manifest(status="OK"))
    reg.begin_run(factory.manifest())
    with pytest.raises(SchemaError, match="already registered"):
        reg.begin_run(factory.manifest())
    with pytest.raises(SchemaError, match="unknown parent"):
        reg.begin_run(factory.manifest(factory.RUN_B, parents=(factory.RUN_C,)))
    with pytest.raises(SchemaError, match="unknown run"):
        reg.end_run(factory.RUN_B, "OK")
    with pytest.raises(SchemaError, match="status"):
        reg.end_run(factory.RUN_A, "DONE")  # type: ignore[arg-type]
    reg.end_run(factory.RUN_A, "OK")
    with pytest.raises(SchemaError, match="has ended"):
        reg.end_run(factory.RUN_A, "OK")
    with pytest.raises(SchemaError, match="has ended"):
        reg.put_artifact(factory.RUN_A, "late", b"x")
    with pytest.raises(EvidenceMissing):
        reg.get_run(factory.RUN_B)


def test_parent_runs_must_share_the_data_class(reg: Registry, factory) -> None:
    reg.begin_run(factory.manifest())
    reg.begin_run(factory.manifest(factory.RUN_B, parents=(factory.RUN_A,)))
    with pytest.raises(DataClassMixError):
        reg.begin_run(factory.manifest(factory.RUN_C, parents=(factory.RUN_A,), data_class=DataClass.REAL))


# ------------------------------------------------------------------------------------------------ metrics
def test_metric_round_trip_and_lookup_rules(run_reg: Registry, factory) -> None:
    run_reg.begin_run(factory.manifest(factory.RUN_B))
    m6 = factory.metric(by={"class": "M6"}, value=0.0058)
    run_reg.put_metrics([factory.metric(value=0.004), m6, factory.metric(run_id=factory.RUN_B, value=0.003)])
    mid = "tier1.t6.cp_upper@v1"
    assert run_reg.get_metric(mid, by={"class": "M6"}) == m6
    assert run_reg.get_metric(mid).value == 0.003                       # latest undimensioned instance
    assert run_reg.get_metric(mid, run_id=factory.RUN_A).value == 0.004
    assert run_reg.get_metric(mid, plane=EvidencePlane.SEARCH).value == 0.003
    with pytest.raises(EvidenceMissing, match="EVIDENCE MISSING: tier1.t6.cp_upper@v1"):
        run_reg.get_metric(mid, plane=EvidencePlane.SEALED)
    with pytest.raises(EvidenceMissing):
        run_reg.get_metric(mid, by={"class": "M1"})
    assert len(run_reg.list_metrics()) == 3
    assert len(run_reg.list_metrics(run_id=factory.RUN_A)) == 2
    assert len(run_reg.list_metrics(prefix="tier1.t6")) == 3
    assert run_reg.list_metrics(prefix="tier1.t7") == []


def test_metric_write_rules(run_reg: Registry, factory) -> None:
    with pytest.raises(SchemaError, match="not defined"):
        run_reg.put_metrics([factory.metric("tier1.t7.cp_upper@v1")])
    with pytest.raises(UnitError):
        run_reg.put_metrics([factory.metric(unit="bp")])
    with pytest.raises(DataClassMixError):
        run_reg.put_metrics([factory.metric(data_class=DataClass.REAL)])
    with pytest.raises(SchemaError, match="FINAL-plane"):
        run_reg.put_metrics([factory.metric(plane=EvidencePlane.SEALED)])
    with pytest.raises(SchemaError, match="unknown run"):
        run_reg.put_metrics([factory.metric(run_id=factory.RUN_B)])
    with pytest.raises(SchemaError, match="twice in the batch"):
        run_reg.put_metrics([factory.metric(), factory.metric(value=0.1)])
    run_reg.put_metrics([factory.metric()])
    with pytest.raises(SchemaError, match="written once"):
        run_reg.put_metrics([factory.metric(by={"class": "M1"}), factory.metric(value=0.2)])
    assert len(run_reg.list_metrics()) == 1                             # the failed batch left nothing behind
    run_reg.put_metrics([])
    assert run_reg.verify_chain().ok


def test_sealed_metrics_come_from_final_runs(reg: Registry, factory) -> None:
    reg.begin_run(factory.manifest(plane=Plane.FINAL))
    reg.define_metric(factory.metric_def())
    reg.put_metrics([factory.metric(plane=EvidencePlane.SEALED)])
    assert reg.get_metric("tier1.t6.cp_upper@v1", plane=EvidencePlane.SEALED).plane == EvidencePlane.SEALED


# ------------------------------------------------------------------------------------------------ ledger
def test_ledger_kinds_cover_the_spec_and_the_analyst() -> None:
    assert LAB_LEDGER_KINDS == ("eval_request", "eval_record", "llm_call", "budget", "escalation", "assumption",
                                "seal", "drill")
    assert get_args(AnalystLedgerKind) == tuple(ANALYST_LEDGER_KINDS)
    assert set(LEDGER_KINDS) == set(LAB_LEDGER_KINDS) | set(ANALYST_LEDGER_KINDS)


def test_append_and_read_ledger(reg: Registry) -> None:
    h1 = reg.append_ledger("eval_request", _eval_request(1))
    h2 = reg.append_ledger("budget", KeyValue(key="core_s", value=36.0))
    h3 = reg.append_ledger("eval_request", _eval_request(2))
    assert len({h1, h2, h3}) == 3 and all(h.startswith("sha256:") for h in (h1, h2, h3))
    rows = reg.read_ledger("eval_request")
    assert [r.parse(EvalRequest).request_id for r in rows] == ["r1", "r2"]
    assert rows[0].payload_class == "adic_tpa.contracts.evidence:EvalRequest" and rows[1].row_hash == h3
    assert rows[0].payload["campaign_id"] == "cmp-2026Q4-1"
    assert [r.kind for r in reg.read_ledger()] == ["eval_request", "budget", "eval_request"]
    assert [r.kind for r in reg.read_ledger(after_seq=rows[0].seq, limit=1)] == ["budget"]
    with pytest.raises(SchemaError, match="unknown ledger kind"):
        reg.append_ledger("gossip", _eval_request())  # type: ignore[arg-type]
    with pytest.raises(SchemaError, match="Pydantic"):
        reg.append_ledger("drill", {"a": 1})  # type: ignore[arg-type]


# ------------------------------------------------------------------------------------------------ claims
def test_claims_are_versioned_on_audit_fields_only(reg: Registry, factory) -> None:
    reg.put_claim(factory.claim())
    reg.put_claim(factory.claim())                                       # identical repeat: no new version
    audited = factory.claim(supports_verdict="supports")
    reg.put_claim(audited)
    reg.put_claim(factory.claim("c-2", sentence_index=1))
    assert reg.get_claim("c-1") == audited
    assert [c.claim_id for c in reg.list_claims()] == ["c-1", "c-2"]
    assert [c.supports_verdict for c in reg.list_claims(doc_id="memo-2026Q4")] == ["supports", "unaudited"]
    with pytest.raises(SchemaError, match="audit fields"):
        reg.put_claim(factory.claim(verbs=("improves",)))
    with pytest.raises(EvidenceMissing):
        reg.get_claim("c-9")
    assert reg.verify_chain().rows == 3


# ------------------------------------------------------------------------------------------------ decisions
def test_decision_chain(run_reg: Registry, factory) -> None:
    assert run_reg.decision_head() == GENESIS_HASH
    d1 = factory.decision()
    run_reg.append_decision(d1)
    assert run_reg.decision_head() == d1.record_hash
    d2 = factory.decision(d1.record_hash, decision_id="dec-Q2-2026Q4-1")
    run_reg.append_decision(d2)
    assert [d.decision_id for d in run_reg.list_decisions()] == ["dec-Q1-2026Q4-1", "dec-Q2-2026Q4-1"]
    assert run_reg.get_decision("dec-Q2-2026Q4-1") == d2


def test_broken_decision_chain_raises(run_reg: Registry, factory) -> None:
    d1 = factory.decision()
    run_reg.append_decision(d1)
    stale = factory.decision(GENESIS_HASH, decision_id="dec-Q2-2026Q4-1")        # links to the old head
    with pytest.raises(HashMismatch, match="decision chain broken"):
        run_reg.append_decision(stale)
    forged = factory.decision(d1.record_hash, decision_id="dec-Q2-2026Q4-1").model_copy(update={"decision": "reject"})
    with pytest.raises(HashMismatch, match="record_hash"):
        run_reg.append_decision(forged)
    assert len(run_reg.list_decisions()) == 1


def test_decision_versions_change_only_outcomes_and_signposts(run_reg: Registry, factory) -> None:
    from datetime import date

    from adic_tpa.contracts.room import OutcomeScore

    d1 = factory.decision()
    run_reg.append_decision(d1)
    scored = factory.decision(d1.record_hash, outcomes={"q1": OutcomeScore(horizon="q1", brier=0.12,
                                                                            resolved_at=date(2027, 1, 15), detail={})})
    run_reg.append_decision(scored)
    assert run_reg.get_decision("dec-Q1-2026Q4-1").outcomes["q1"].brier == 0.12
    assert len(run_reg.list_decisions()) == 2 and len(run_reg.list_decisions(latest_only=True)) == 1
    changed = factory.decision(scored.record_hash, decision="reject")
    with pytest.raises(SchemaError, match="outcomes and signposts"):
        run_reg.append_decision(changed)


def test_decision_runs_must_exist_and_share_the_data_class(run_reg: Registry, factory) -> None:
    with pytest.raises(SchemaError, match="unknown run"):
        run_reg.append_decision(factory.decision(runs=(factory.RUN_B,)))
    with pytest.raises(DataClassMixError):
        run_reg.append_decision(factory.decision(data_class=DataClass.REAL))
    with pytest.raises(HashMismatch):
        run_reg.append_decision(chain_record(factory.decision(), "sha256:" + "f" * 64))
    assert run_reg.list_decisions() == []


# ------------------------------------------------------------------------------------------------ read-only
def test_readonly_handle_refuses_writes_but_appends_analyst_kinds(run_reg: Registry, paths: SimpleNamespace,
                                                                   factory) -> None:
    run_reg.put_metrics([factory.metric()])
    with Registry(paths.db, paths.root, readonly=True) as ro:
        assert ro.readonly
        assert ro.get_metric("tier1.t6.cp_upper@v1").value == 0.0042
        refusals = [
            lambda: ro.begin_run(factory.manifest(factory.RUN_B)),
            lambda: ro.end_run(factory.RUN_A, "OK"),
            lambda: ro.put_artifact(factory.RUN_A, "x", b"x"),
            lambda: ro.define_metric(factory.metric_def("tier1.t7.cp_upper@v1")),
            lambda: ro.approve_metric("tier1.t6.cp_upper@v1", approver="MRM"),
            lambda: ro.put_metrics([factory.metric(by={"class": "M1"})]),
            lambda: ro.append_ledger("eval_record", _eval_request()),
            lambda: ro.put_claim(factory.claim()),
            lambda: ro.append_decision(factory.decision()),
            lambda: ro.mfdr().configure(w0=0.05, payout=0.05, decay=0.9),
        ]
        for attempt in refusals:
            with pytest.raises(EntitlementDenied) as exc:
                attempt()
            assert exc.value.context["rule"] == "REGISTRY_READONLY"
        digest = ro.append_ledger("chat_turn", KeyValue(key="turn", value=1.0))
        assert ro.verify_chain().head == digest
    assert run_reg.read_ledger("chat_turn")[0].row_hash == digest
    assert run_reg.verify_chain().ok


def test_readonly_needs_an_existing_database(tmp_path) -> None:
    with pytest.raises(EvidenceMissing):
        Registry(tmp_path / "missing.sqlite", tmp_path / "runs", readonly=True)


def test_a_closed_handle_refuses_use(paths: SimpleNamespace) -> None:
    reg = Registry(paths.db, paths.root)
    reg.close()
    reg.close()                                                           # idempotent
    for attempt in (lambda: reg.append_ledger("drill", _eval_request()), reg.verify_chain, reg.read_ledger,
                    lambda: reg.get_claim("c-1")):
        with pytest.raises(ExecutionFailed, match="closed"):
            attempt()
    ro = Registry(paths.db, paths.root, readonly=True)
    ro.close()
    with pytest.raises(ExecutionFailed, match="closed"):
        ro.append_ledger("chat_turn", KeyValue(key="turn", value=1.0))


# ------------------------------------------------------------------------------------------------ concurrency
def test_threads_and_two_handles_never_fork_the_chain(paths: SimpleNamespace) -> None:
    with Registry(paths.db, paths.root) as a, Registry(paths.db, paths.root) as b:
        def work(reg: Registry, tag: str) -> None:
            for i in range(25):
                reg.append_ledger("drill", KeyValue(key=f"{tag}{i}", value=float(i)))

        threads = [threading.Thread(target=work, args=(r, t)) for r, t in ((a, "a"), (a, "b"), (b, "c"), (b, "d"))]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        report = a.verify_chain()
        assert report.ok and report.rows == 100
        assert len({e.row_hash for e in b.read_ledger()}) == 100


@pytest.mark.slow
def test_a_second_process_writes_the_same_chain(paths: SimpleNamespace) -> None:
    import os
    import subprocess
    import sys
    from pathlib import Path

    src = Path(__file__).resolve().parents[3] / "src"
    with Registry(paths.db, paths.root) as reg:
        reg.append_ledger("drill", KeyValue(key="parent", value=0.0))
        script = ("import sys\nfrom pathlib import Path\nfrom adic_tpa.contracts.enums import KeyValue\n"
                  "from adic_tpa.registry import Registry\n"
                  "with Registry(Path(sys.argv[1]), Path(sys.argv[2])) as r:\n"
                  "    for i in range(40): r.append_ledger('drill', KeyValue(key='child', value=float(i)))\n")
        env = {**os.environ, "PYTHONPATH": str(src)}
        child = subprocess.Popen([sys.executable, "-c", script, str(paths.db), str(paths.root)], env=env)
        appended = 0
        while child.poll() is None and appended < 5000:      # keep writing for as long as the child writes
            reg.append_ledger("drill", KeyValue(key="parent", value=float(appended)))
            appended += 1
        assert child.wait(timeout=120) == 0
        report = reg.verify_chain()
        assert report.ok and report.rows == 1 + appended + 40
        keys = [e.parse(KeyValue).key for e in reg.read_ledger()]
        first_child, last_child = keys.index("child"), len(keys) - 1 - keys[::-1].index("child")
        assert "parent" in keys[first_child:last_child]             # the two writers interleaved


def test_chain_payload_is_the_canonical_envelope(run_reg: Registry, paths: SimpleNamespace, factory) -> None:
    run_reg.put_metrics([factory.metric()])
    con = sqlite3.connect(paths.db)
    try:
        payloads = [r[0] for r in con.execute("SELECT payload FROM chain ORDER BY seq")]
    finally:
        con.close()
    for payload in payloads:
        assert canonical_json(json.loads(payload)).decode("utf-8") == payload
    assert json.loads(payloads[-1])["body"] == json.loads(canonical_json(factory.metric()))
