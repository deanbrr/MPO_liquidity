"""The research port is complete and unedited (BUILD_SPEC v1.1 §10.4, §9.2 WP-03 DoD, §6.3; owner WP-03).

``tools/port_research.py`` copies research outputs read-only into ``tests/regression/fixtures/<source>/`` and
writes ``port_manifest.json`` with every fixture's SHA-256 and its research source(s). These tests re-hash the
tree: every file is listed, every listed hash matches, copies are byte-identical to their sources, and the sealed
v1.1 PE history carries the §6.3 seal. SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType

import pytest

from adic_tpa.contracts.hashing import file_hash

REPO = Path(__file__).resolve().parents[2]
FIXTURES = REPO / "tests" / "regression" / "fixtures"
SEAL_V1_1 = "sha256:4346dc249e83bff8d952588715a69ec038b9725ab436e0b24b8bb4227f2f54a9"     # BUILD_SPEC §6.3
NOT_PORTED = {"port_manifest.json", "conftest.py"}
# §10.4 "Research ports": one fixture per named source at least.
REQUIRED = (
    "hf_ladder/hf_ladder_results.json", "t1_engine/ladder_readings.json", "gap02/gstar_grid.json",
    "gap02/gap02_results.json", "gap02/coefs.json", "groups_gap01/coefs.json", "perf/golden_cases.json",
    "bridge/bridge_results.json", "v8_rerun/v8_rerun_results.json", "simm/simm_offset_example_results.json",
    "sealed_pe_history/sealed_pe_history_v1_1.csv",
)


@pytest.fixture(scope="module")
def manifest() -> dict:
    with open(FIXTURES / "port_manifest.json", encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def tool() -> Iterator[ModuleType]:
    name = "port_research_under_test"
    spec = importlib.util.spec_from_file_location(name, REPO / "tools" / "port_research.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module                 # dataclasses resolve string annotations through sys.modules
    try:
        spec.loader.exec_module(module)
        yield module
    finally:
        sys.modules.pop(name, None)


def _tree_files() -> set[str]:
    return {p.relative_to(FIXTURES).as_posix() for p in FIXTURES.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.name not in NOT_PORTED}


def test_manifest_lists_every_fixture_file_and_nothing_else(manifest: dict) -> None:
    listed = [e["fixture"] for e in manifest["entries"]]
    assert len(listed) == len(set(listed))
    assert set(listed) == _tree_files()
    assert set(REQUIRED) <= set(listed)


def test_every_hash_matches_and_names_its_sources(manifest: dict) -> None:
    assert manifest["schema"] == "adic_tpa.port_manifest/1" and manifest["data_class"] == "SYNTHETIC"
    for e in manifest["entries"]:
        assert file_hash(FIXTURES / e["fixture"]) == e["sha256"], e["fixture"]
        assert e["sources"] and all(s.startswith("research/") and h.startswith("sha256:")
                                    for s, h in e["sources"].items()), e["fixture"]
        if e["kind"] == "copy":                                     # byte-identical (LF-normalized) copies
            assert list(e["sources"].values()) == [e["sha256"]], e["fixture"]
        else:
            assert e["kind"] == "export" and e["exporter"].startswith("export_"), e["fixture"]


def test_exports_are_labelled_synthetic(manifest: dict) -> None:
    for e in manifest["entries"]:
        if e["kind"] == "export":
            with open(FIXTURES / e["fixture"], encoding="utf-8") as fh:
                body = json.load(fh)
            assert "SYNTHETIC" in body.get("note", ""), e["fixture"]


def test_port_check_is_clean(tool: ModuleType) -> None:
    """Sources and fixtures re-hash to the manifest (``port_research.py --check``)."""
    assert tool.check() == []
    assert tool.SEALED_PE_HISTORY_SHA256 == SEAL_V1_1


def test_sealed_pe_history_carries_the_seal(manifest: dict) -> None:
    path = FIXTURES / "sealed_pe_history" / "sealed_pe_history_v1_1.csv"
    assert file_hash(path) == SEAL_V1_1
    entry = next(e for e in manifest["entries"] if e["fixture"] == "sealed_pe_history/sealed_pe_history_v1_1.csv")
    assert entry["sha256"] == SEAL_V1_1
