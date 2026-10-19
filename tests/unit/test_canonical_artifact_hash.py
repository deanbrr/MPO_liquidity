"""canonical_artifact_hash (BUILD_SPEC v1.1 §4.1, §9.4 #9; BUILD-27): two runs that differ only in run ids,
timestamps, chain hashes, signatures over timestamps and absolute paths hash equal; content changes do not.
Owner WP-01."""

from __future__ import annotations

from datetime import datetime, timezone

from adic_tpa.contracts.enums import DataClass, Plane, RunMode
from adic_tpa.contracts.evidence import RunManifest
from adic_tpa.contracts.hashing import VOLATILE_FIELDS, canonical_artifact_hash, content_hash, normalize_volatile


def _manifest(run_id: str, created: datetime, parent: str) -> RunManifest:
    return RunManifest.model_validate_json(RunManifest(
        run_id=run_id, kind="quarter", created_at=created, engine_git_sha="abc123", engine_tree_hash="sha256:" + "1" * 64,
        config_hash="sha256:" + "2" * 64, contract_hash=None, snapshot_hash="sha256:" + "3" * 64, census_hash=None,
        belief_hash=None, scenario_hashes={"search:M1": "sha256:" + "4" * 64}, seed_spawn={"search:M1": "00ff"},
        plane=Plane.SEARCH, cache_keys=("k1",), solver_records=(), versions={"numpy": "2.5.4"}, env={},
        llm_calls=(), data_class=DataClass.SYNTHETIC, run_mode=RunMode.DEV_SYNTHETIC, parent_runs=(parent,),
        status="OK").model_dump_json())


def _artifact(run_id: str, ts: str, prev: str, path: str) -> dict:
    return {
        "run_id": run_id, "created_at": ts, "prev_hash": prev, "record_hash": "sha256:" + prev[-64:],
        "ref": f"{run_id}:tier1_board:/rows/T6/M6/cp_upper", "value": 0.0123,
        "ballots": [{"member_hash": "m1", "cast_at": ts, "choice": "approve"}],
        "signoff": {"role": "CIO", "signed_at": ts, "signature": prev[-16:], "object_hash": "sha256:" + "9" * 64},
        "pack_path": path, "out": {"timing": {"time_s": float(len(path))}},
    }


def test_runs_differing_only_in_volatile_fields_hash_equal() -> None:
    a = _artifact("run-20261018T091500Z-3f2a9c1d", "2026-10-18T09:15:00Z", "sha256:" + "a" * 64,
                  r"C:\users\dean\runs\run-20261018T091500Z-3f2a9c1d\pack")
    b = _artifact("run-20261019T101010Z-0badcafe", "2026-10-19T10:10:10Z", "sha256:" + "b" * 64,
                  r"D:\other\machine\pack")
    assert content_hash(a) != content_hash(b)
    assert canonical_artifact_hash(a) == canonical_artifact_hash(b)


def test_manifests_differing_only_in_run_ids_and_times_hash_equal() -> None:
    m1 = _manifest("run-20261018T091500Z-3f2a9c1d", datetime(2026, 10, 18, 9, 15, tzinfo=timezone.utc),
                   "run-20261017T000000Z-11111111")
    m2 = _manifest("run-20261020T120000Z-22222222", datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc),
                   "run-20261019T000000Z-33333333")
    assert content_hash(m1) != content_hash(m2)
    assert canonical_artifact_hash(m1) == canonical_artifact_hash(m2)


def test_content_changes_still_change_the_hash() -> None:
    a = _artifact("run-20261018T091500Z-3f2a9c1d", "t", "sha256:" + "a" * 64, "/x")
    b = dict(a, value=0.0124)
    assert canonical_artifact_hash(a) != canonical_artifact_hash(b)


def test_declared_volatile_fields() -> None:
    assert {"run_id", "created_at", "recorded_at", "cast_at", "locked_at", "prev_hash", "record_hash"} <= VOLATILE_FIELDS
    norm = normalize_volatile({"ref": "run-20261018T091500Z-3f2a9c1d:pack:/l0", "json_pointer": "/rows/T6",
                               "artifact_root": "/home/x", "note": "C:\\temp\\x"})
    assert norm == {"ref": "<run>:pack:/l0", "json_pointer": "/rows/T6", "artifact_root": "<path>", "note": "<path>"}
