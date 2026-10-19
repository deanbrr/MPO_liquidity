"""Golden loader, port-manifest hash check and manifest reproduction (BUILD_SPEC v1.1 §4.5, §10.4; owner WP-03).

SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pytest

from adic_tpa.contracts.enums import DataClass, Plane, RunMode
from adic_tpa.contracts.errors import HashMismatch, SchemaError
from adic_tpa.contracts.evidence import RunManifest
from adic_tpa.contracts.hashing import canonical_artifact_hash, file_hash
from adic_tpa.contracts.ids import RunId
from adic_tpa.testing import fixture_tree, golden, mini_book
from adic_tpa.testing.golden import (
    RERUN_FILE, assert_manifest_reproduces, golden_path, port_manifest, regression_fixtures_root,
    rerun_frozen_fixtures,
)

# ``adic_tpa.testing.golden`` the attribute is the §4.5 loader function; the module is reached through importlib.
golden_module = importlib.import_module("adic_tpa.testing.golden")


def test_golden_loads_each_format() -> None:
    coefs = golden("gap02/coefs")
    assert coefs["nav0_bn"] == 177.0 and set(coefs["readings"]) == {"canonical", "as_written", "critic"}
    rows = golden("sealed_pe_history/sealed_pe_history_v1_1.csv")
    assert rows and isinstance(rows[0], dict) and all(not next(iter(r.values()), "").startswith("#") for r in rows)
    matrix = golden("bridge/jpm2026_matrix.npz")
    assert matrix and all(isinstance(v, np.ndarray) for v in matrix.values())
    script = golden("hf_ladder/hf_ladder.py")
    assert isinstance(script, str) and "def " in script


def test_golden_resolves_only_inside_the_golden_trees() -> None:
    assert golden_path("frozen_fixtures").name == "frozen_fixtures.json"
    with pytest.raises(SchemaError):
        golden("does/not/exist")
    with pytest.raises(SchemaError):
        golden_path("../../pyproject.toml")


def _fake_fixture_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, text: str) -> Path:
    root = tmp_path / "fixtures"
    (root / "demo").mkdir(parents=True)
    target = root / "demo" / "data.json"
    target.write_bytes(text.encode("utf-8"))
    entries = [{"fixture": "demo/data.json", "sha256": file_hash(target), "source": "synthetic"}]
    (root / "port_manifest.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
    monkeypatch.setattr(golden_module, "regression_fixtures_root", lambda: root)
    monkeypatch.setattr(golden_module, "golden_root", lambda: tmp_path / "golden-empty")
    return target


def test_an_edited_port_raises_hash_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = _fake_fixture_tree(tmp_path, monkeypatch, '{"x": 1}\n')
    assert golden("demo/data") == {"x": 1}
    target.write_bytes(b'{"x": 1}\r\n')                        # CRLF checkouts hash the same (S-ADR-42)
    assert golden("demo/data") == {"x": 1}
    target.write_bytes(b'{"x": 2}\n')
    with pytest.raises(HashMismatch) as err:
        golden("demo/data")
    assert err.value.context["fixture"] == "demo/data.json"


def test_write_and_check_frozen_fixtures(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The ``--update-golden`` path writes a file the check then accepts; an edited checksum is named."""
    monkeypatch.setattr(golden_module, "golden_root", lambda: tmp_path)
    assert golden_module.check_frozen_fixtures()[0].endswith("is missing; run pytest --update-golden")
    path = golden_module.write_frozen_fixtures()
    assert path == tmp_path / "frozen_fixtures.json" and golden_module.check_frozen_fixtures() == []
    body = json.loads(path.read_text(encoding="utf-8"))
    body["fixtures"]["mini_cube"]["checksum"] = "sha256:" + "f" * 64
    path.write_text(json.dumps(body), encoding="utf-8")
    problems = golden_module.check_frozen_fixtures()
    assert len(problems) == 1 and problems[0].startswith("mini_cube.checksum")


def test_port_manifest_is_present() -> None:
    manifest = port_manifest()
    assert manifest["entries"] and (regression_fixtures_root() / "port_manifest.json").is_file()


def _manifest(tmp_path: Path, hashes: dict[str, str]) -> Path:
    m = RunManifest(run_id=RunId("run-20261018T000000Z-0000fa4e"), kind="golden_test",
                    created_at=datetime(2026, 10, 18, tzinfo=timezone.utc), engine_git_sha="0" * 40,
                    engine_tree_hash="sha256:" + "0" * 64, config_hash="sha256:" + "0" * 64, contract_hash=None,
                    snapshot_hash="sha256:" + "0" * 64, census_hash=None, belief_hash=None, scenario_hashes={},
                    seed_spawn={}, plane=Plane.SEARCH, cache_keys=(), solver_records=(), versions={}, env={},
                    llm_calls=(), data_class=DataClass.SYNTHETIC, run_mode=RunMode.DEV_SYNTHETIC, status="OK",
                    canonical_artifact_hashes=hashes)
    path = tmp_path / "manifest.json"
    path.write_text(m.model_dump_json(), encoding="utf-8")
    return path


def test_manifest_reproduces_with_a_callable(tmp_path: Path) -> None:
    tree = fixture_tree()
    path = _manifest(tmp_path, {"tree": canonical_artifact_hash(tree)})
    assert_manifest_reproduces(path, rerun=lambda m: {"tree": fixture_tree()})
    with pytest.raises(HashMismatch):
        assert_manifest_reproduces(path, rerun=lambda m: {"tree": fixture_tree((2, 2))})
    with pytest.raises(HashMismatch):
        assert_manifest_reproduces(path, rerun=lambda m: {"tree": tree, "extra": mini_book("v1")})
    with pytest.raises(HashMismatch):
        assert_manifest_reproduces(path, rerun=lambda m: {})


def test_manifest_reproduces_through_rerun_json(tmp_path: Path) -> None:
    artifacts = rerun_frozen_fixtures(None)  # type: ignore[arg-type]
    path = _manifest(tmp_path, {k: canonical_artifact_hash(v) for k, v in artifacts.items()})
    with pytest.raises(SchemaError):
        assert_manifest_reproduces(path)                              # no rerun.json yet
    (tmp_path / RERUN_FILE).write_text(json.dumps({"entry": "adic_tpa.testing.golden:rerun_frozen_fixtures"}),
                                       encoding="utf-8")
    assert_manifest_reproduces(path)
    (tmp_path / RERUN_FILE).write_text(json.dumps({"entry": "os:getcwd"}), encoding="utf-8")
    with pytest.raises(SchemaError):
        assert_manifest_reproduces(path)
