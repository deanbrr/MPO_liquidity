"""Integrity drill ``test_chain_verification`` (BUILD_SPEC v1.1 §7.13, §4.6): edit a registry row with sqlite3 and
``verify_chain`` names the first bad row. Every variant first drops the append-only trigger it needs, as a tamperer
must; the report flags the missing trigger too, and a writable registry refuses to open the tampered file. A
tamperer who re-hashes the whole chain after an edit is still caught by the record-level chains (decisions, mFDR
wealth) and by the externally anchored head. Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from adic_tpa.contracts.enums import ConsentScenario, DataClass, EvidencePlane, KeyValue, Plane, PricedOn, RunMode
from adic_tpa.contracts.errors import HashMismatch
from adic_tpa.contracts.evidence import MetricDef, MetricInstance, RunManifest
from adic_tpa.contracts.room import DecisionRecord
from adic_tpa.registry import Registry
from adic_tpa.registry.chain import GENESIS_HASH, chain_record, row_hash

RUN = "run-20261018T091500Z-3f2a9c1d"
H = "sha256:" + "5" * 64


def _decision(prev_hash: str) -> DecisionRecord:
    return chain_record(DecisionRecord(
        decision_id="dec-Q1-2026Q4-1", register_id="Q1", as_of=date(2026, 10, 18), tier="A", options=(),
        engine_recommendation="HOLD", evidence_plane="search", run_manifests=(RUN,), priced_on=PricedOn.FEASIBLE,
        consent_scenario=ConsentScenario.R0, recovery_hash=None, prevote_hashes=(), ballots=(), decision="approve",
        override=None, rationale="SYNTHETIC drill decision", minority_reports=(), signposts=(), commitment_plan=(),
        review_date=date(2027, 1, 15), data_class=DataClass.SYNTHETIC, prev_hash=GENESIS_HASH,
        record_hash=GENESIS_HASH), prev_hash)


def _populate(tmp_path: Path) -> SimpleNamespace:
    db, root = tmp_path / "registry.sqlite", tmp_path / "runs"
    manifest = RunManifest(
        run_id=RUN, kind="quarter", created_at=datetime(2026, 10, 18, 9, 15, tzinfo=timezone.utc),
        engine_git_sha="abc123", engine_tree_hash=H, config_hash=H, contract_hash=None, snapshot_hash=H,
        census_hash=None, belief_hash=None, scenario_hashes={}, seed_spawn={}, plane=Plane.SEARCH, cache_keys=(),
        solver_records=(), versions={}, env={}, llm_calls=(), data_class=DataClass.SYNTHETIC,
        run_mode=RunMode.DEV_SYNTHETIC, status="STARTED")
    with Registry(db, root) as reg:
        reg.begin_run(manifest)                                                      # seq 1
        reg.define_metric(MetricDef(metric_id="tier1.t6.cp_upper@v1", description="SYNTHETIC", unit="prob",
                                    aggregation="mean", ci_method="clopper_pearson", range_method="model_min_max",
                                    icd203=True, owner_role="CRO", code_ref="core.certify", code_hash=H))   # seq 2
        reg.put_metrics([MetricInstance(metric_id="tier1.t6.cp_upper@v1", run_id=RUN, value=value, unit="prob",
                                        plane=EvidencePlane.SEARCH, scenario_hash=H, by={"class": f"M{i}"},
                                        data_class=DataClass.SYNTHETIC)
                         for i, value in enumerate((0.0051, 0.0062, 0.0073), start=1)])   # seq 3..5
        for i in range(3):
            reg.append_ledger("budget", KeyValue(key="core_s", value=36.0 + i))      # seq 6..8
        artifact = reg.put_artifact(RUN, "note", b"SYNTHETIC note")                  # seq 9
        reg.append_decision(_decision(reg.decision_head()))                          # seq 10
        reg.mfdr().configure(w0=0.05, payout=0.05, decay=0.9)                        # seq 11
        reg.mfdr().record(contract_id="ctr-2026Q4-v1", hypothesis_id="h1", p_value=0.3, alpha_level=0.01,
                          rejected=False, wealth_after=0.0425)                       # seq 12
        report = reg.verify_chain()
        assert report.ok
    return SimpleNamespace(db=db, root=root, artifact=artifact, head=report.head)


def _tamper(db: Path, *statements: str) -> None:
    con = sqlite3.connect(db)
    try:
        for sql in statements:
            con.execute(sql)
        con.commit()
    finally:
        con.close()


def _rewrite_and_rechain(db: Path, seq: int, old: str, new: str) -> None:
    """Edit one payload, then recompute every row hash from there on (a tamperer who re-hashes the chain)."""
    con = sqlite3.connect(db)
    try:
        con.execute("DROP TRIGGER chain_no_update")
        rows = con.execute("SELECT seq, payload, prev_hash FROM chain WHERE seq >= ? ORDER BY seq", (seq,)).fetchall()
        prev = rows[0][2]
        for s, payload, _ in rows:
            if s == seq:
                assert old in payload
                payload = payload.replace(old, new)
            digest = row_hash(prev, payload)
            con.execute("UPDATE chain SET payload = ?, prev_hash = ?, row_hash = ? WHERE seq = ?",
                        (payload, prev, digest, s))
            prev = digest
        con.commit()
    finally:
        con.close()


def _verify(reg_paths: SimpleNamespace):
    with Registry(reg_paths.db, reg_paths.root, readonly=True) as reg:
        return reg.verify_chain()


def test_an_edited_ledger_row_is_named(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    _tamper(p.db, "DROP TRIGGER chain_no_update",
            "UPDATE chain SET payload = replace(payload, '37.0', '3700.0') WHERE seq = 7")
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 7
    assert report.first_bad.table == "chain" and "edited" in report.first_bad.reason
    assert any(i.table == "schema" and "chain_no_update" in i.reason for i in report.issues)
    with pytest.raises(HashMismatch, match="triggers are missing"):
        Registry(p.db, p.root)


def test_a_rewritten_row_with_a_recomputed_hash_is_named(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    con = sqlite3.connect(p.db)
    payload, prev = con.execute("SELECT payload, prev_hash FROM chain WHERE seq = 4").fetchone()
    con.close()
    forged = payload.replace("0.0062", "0.0001")
    assert forged != payload
    con = sqlite3.connect(p.db)
    con.execute("DROP TRIGGER chain_no_update")
    con.execute("UPDATE chain SET payload = ?, row_hash = ? WHERE seq = 4", (forged, row_hash(prev, forged)))
    con.commit()
    con.close()
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 4 and "rewritten" in report.first_bad.reason


def test_a_deleted_row_is_named(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    _tamper(p.db, "DROP TRIGGER chain_no_delete", "DELETE FROM chain WHERE seq = 6")
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 6
    reasons = {i.reason for i in report.issues if i.seq == 6}
    assert any("missing" in r for r in reasons) and any("no chain row" in r for r in reasons)


def test_an_edited_index_column_is_named(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    _tamper(p.db, "DROP TRIGGER metrics_no_update",
            "UPDATE metrics SET by_key = '{\"class\":\"M9\"}' WHERE seq = 5")
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 5
    assert report.first_bad.table == "metrics" and "by_key" in report.first_bad.reason


@pytest.mark.parametrize("kind", ["ledger.drill", "bogus"])
def test_an_edited_kind_column_is_named(tmp_path: Path, kind: str) -> None:
    p = _populate(tmp_path)
    _tamper(p.db, "DROP TRIGGER chain_no_update", f"UPDATE chain SET kind = '{kind}' WHERE seq = 8")
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 8


def test_an_edited_artifact_file_is_named(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    (p.root / RUN / "artifacts" / "note.bin").write_bytes(b"SYNTHETIC note, edited")
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 9 and report.first_bad.table == "artifacts"
    assert report.artifacts_checked == 1


def test_a_rechained_decision_edit_is_caught_by_the_decision_chain(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    _rewrite_and_rechain(p.db, 10, '"decision":"approve"', '"decision":"reject"')
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 10
    assert {i.table for i in report.issues if i.seq is not None} == {"decisions"}
    assert report.head != p.head                       # and the externally anchored head no longer matches


def test_a_rechained_wealth_edit_is_caught_by_the_mfdr_sequence(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    _rewrite_and_rechain(p.db, 12, '"wealth_before":0.05', '"wealth_before":0.5')
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 12 and report.first_bad.table == "mfdr_tests"


def test_a_rechained_artifact_path_cannot_point_outside_the_run(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    (tmp_path / "outside.bin").write_bytes(b"SYNTHETIC note")              # same bytes, same sha256
    _rewrite_and_rechain(p.db, 9, f'"rel_path":"{RUN}/artifacts/note.bin"', '"rel_path":"../outside.bin"')
    report = _verify(p)
    assert not report.ok and report.first_bad_seq == 9 and "registered path" in report.first_bad.reason
    with Registry(p.db, p.root, readonly=True) as reg, pytest.raises(HashMismatch, match="registered path"):
        reg.get_artifact(p.artifact)


def test_the_untouched_registry_verifies(tmp_path: Path) -> None:
    p = _populate(tmp_path)
    report = _verify(p)
    assert report.ok and report.rows == 12 and report.head == p.head
    assert report.first_bad_seq is None and report.first_bad is None
