"""Registry artifacts (BUILD_SPEC v1.1 §4.6, §1.12): round trips with checksums for models, array containers,
Arrow tables and bytes; JSON-pointer references; SYNTHETIC labels; tamper detection; write-once names and
provenance parents. Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pyarrow as pa
import pytest
from pydantic import BaseModel, ConfigDict

from adic_tpa import SYNTHETIC_FOOTER
from adic_tpa.contracts.arrays import ArrayContainer
from adic_tpa.contracts.claims import ProvenanceNode
from adic_tpa.contracts.enums import DataClass
from adic_tpa.contracts.errors import DataClassMixError, EvidenceMissing, HashMismatch, SchemaError
from adic_tpa.contracts.evidence import MetricDef, RunManifest
from adic_tpa.contracts.hashing import canonical_artifact_hash, content_hash
from adic_tpa.contracts.optimizer import DualQuality, DualSet
from adic_tpa.registry import Registry
from adic_tpa.registry.artifacts import LABEL_PREFIX, table_checksum


class LocalCard(BaseModel):
    """A result model defined outside contracts (like core.sim's Tier1Board)."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)
    rows: dict[str, dict[str, float]]
    label: str


@dataclass(frozen=True, slots=True)
class LocalBox(ArrayContainer):
    """An array container defined outside contracts (no ARRAY_SPECS entry)."""

    values: np.ndarray


def _duals() -> DualSet:
    quality = DualQuality(one_sided=(0.0, 1.0), at_kink=False, ranging=(0.0, 2.0), band=(0.4, 0.5, 0.6),
                          sign_flip=False, pinned=False, method="ranging")
    return DualSet(pi_row=np.array([0.5, 0.0]), mu_cash=np.array([1.25]), M_cash=np.zeros(1), ell=np.array([0.01]),
                   quality={"T4P:h=07": quality})


def _no_temp_files(root: Path) -> bool:
    return not [p for p in root.rglob(".tmp-*")]


def test_contracts_model_round_trips_with_checksum(run_reg: Registry, factory) -> None:
    d = factory.metric_def()
    ref = run_reg.put_artifact(factory.RUN_A, "metric_card", d)
    assert ref == f"{factory.RUN_A}:metric_card:"
    back = run_reg.get_artifact(ref)
    assert isinstance(back, MetricDef) and back == d
    assert run_reg.get_artifact(f"{ref}/unit") == "prob"
    info = run_reg.artifact_info(ref)
    assert info.format == "json" and info.class_path == "adic_tpa.contracts.evidence:MetricDef"
    assert info.kind == "MetricDef" and info.data_class == DataClass.SYNTHETIC
    assert info.checksum == content_hash(d) and info.canonical_hash == canonical_artifact_hash(d)
    assert run_reg.artifact_path(ref).name == "metric_card.json"


def test_models_outside_contracts_come_back_as_json_unless_named(run_reg: Registry, factory) -> None:
    card = LocalCard(rows={"T6": {"M6": 0.0058}}, label="SYNTHETIC")
    ref = run_reg.put_artifact(factory.RUN_A, "tier1_board", card, kind="tier1_board")
    assert run_reg.get_artifact(ref) == {"rows": {"T6": {"M6": 0.0058}}, "label": "SYNTHETIC"}
    assert run_reg.get_artifact(ref, model=LocalCard) == card
    assert run_reg.get_artifact(f"{factory.RUN_A}:tier1_board:/rows/T6/M6") == 0.0058
    with pytest.raises(EvidenceMissing, match="does not resolve"):
        run_reg.get_artifact(f"{factory.RUN_A}:tier1_board:/rows/T7")


def test_array_container_round_trips_with_checksum(run_reg: Registry, factory) -> None:
    duals = _duals()
    ref = run_reg.put_artifact(factory.RUN_A, "duals", duals)
    back = run_reg.get_artifact(ref)
    assert isinstance(back, DualSet) and back.checksum() == duals.checksum()
    np.testing.assert_array_equal(back.pi_row, duals.pi_row)
    assert run_reg.get_artifact(f"{ref}/mu_cash/0") == 1.25
    assert run_reg.get_artifact(f"{ref}/quality/T4P:h=07/method") == "ranging"
    assert run_reg.get_artifact(f"{ref}/quality/T4P:h=07")["band"] == [0.4, 0.5, 0.6]
    np.testing.assert_array_equal(run_reg.get_artifact(f"{ref}/pi_row"), duals.pi_row)
    with pytest.raises(EvidenceMissing, match="out of range"):
        run_reg.get_artifact(f"{ref}/mu_cash/3")
    assert run_reg.artifact_info(ref).checksum == duals.checksum()


def test_containers_outside_contracts_need_the_class(run_reg: Registry, factory) -> None:
    box = LocalBox(values=np.arange(3.0))
    ref = run_reg.put_artifact(factory.RUN_A, "box", box)
    with pytest.raises(SchemaError, match="pass model="):
        run_reg.get_artifact(ref)
    assert run_reg.get_artifact(ref, model=LocalBox).checksum() == box.checksum()
    assert run_reg.get_artifact(f"{ref}/values/2", model=LocalBox) == 2.0


def test_invalid_containers_are_refused(run_reg: Registry, factory) -> None:
    bad = DualSet(pi_row=np.array([np.nan]), mu_cash=np.ones(1), M_cash=np.zeros(1), ell=np.zeros(1), quality={})
    with pytest.raises(SchemaError, match="non-finite"):
        run_reg.put_artifact(factory.RUN_A, "bad", bad)
    assert _no_temp_files(run_reg.artifact_root) and run_reg.list_artifacts(factory.RUN_A) == []


def test_tables_round_trip_with_checksum_and_labels(run_reg: Registry, factory) -> None:
    table = pa.table({"metric": ["a", "b", "c"], "value": [0.1, 0.2, 0.3]}).replace_schema_metadata({"unit": "prob"})
    ref = run_reg.put_artifact(factory.RUN_A, "path_metrics", table)
    back = run_reg.get_artifact(ref)
    assert back.equals(table) and back.schema.metadata == {b"unit": b"prob"}
    assert table_checksum(back) == run_reg.artifact_info(ref).checksum
    assert run_reg.get_artifact(f"{ref}/value/1") == 0.2
    assert run_reg.get_artifact(f"{ref}/metric") == ["a", "b", "c"]
    with pytest.raises(EvidenceMissing):
        run_reg.get_artifact(f"{ref}/missing")
    raw = pa.ipc.open_file(pa.py_buffer(run_reg.artifact_path(ref).read_bytes())).read_all()
    labels = {k[len(LABEL_PREFIX):].decode(): json.loads(v) for k, v in raw.schema.metadata.items()
              if k.startswith(LABEL_PREFIX)}
    assert labels == {"artifact": "path_metrics", "data_class": "SYNTHETIC", "is_synthetic": True,
                      "footer": SYNTHETIC_FOOTER}


def test_table_checksum_ignores_chunking() -> None:
    one = pa.table({"x": [1, 2, 3, 4]})
    two = pa.concat_tables([pa.table({"x": [1, 2]}), pa.table({"x": [3, 4]})])
    assert two.column("x").num_chunks == 2
    assert table_checksum(one) == table_checksum(two)
    assert table_checksum(one) != table_checksum(pa.table({"x": [1, 2, 3, 5]}))


def test_bytes_round_trip(run_reg: Registry, factory) -> None:
    ref = run_reg.put_artifact(factory.RUN_A, "figure.svg", b"<svg>SYNTHETIC</svg>")
    assert run_reg.get_artifact(ref) == b"<svg>SYNTHETIC</svg>"
    with pytest.raises(EvidenceMissing):
        run_reg.get_artifact(f"{ref}/0")


def test_json_artifacts_carry_the_synthetic_footer(reg: Registry, factory) -> None:
    reg.begin_run(factory.manifest())
    reg.begin_run(factory.manifest(factory.RUN_B, data_class=DataClass.REAL))
    synthetic = json.loads(reg.artifact_path(reg.put_artifact(factory.RUN_A, "card", factory.metric_def())).read_text(
        encoding="utf-8"))
    assert synthetic["footer"] == SYNTHETIC_FOOTER and synthetic["is_synthetic"] is True
    assert synthetic["data_class"] == "SYNTHETIC" and synthetic["artifact"] == "card"
    real = json.loads(reg.artifact_path(reg.put_artifact(factory.RUN_B, "card", factory.metric_def())).read_text(
        encoding="utf-8"))
    assert real["footer"] is None and real["data_class"] == "REAL"


def test_tampered_or_missing_files_raise(run_reg: Registry, factory) -> None:
    ref = run_reg.put_artifact(factory.RUN_A, "card", factory.metric_def())
    path = run_reg.artifact_path(ref)
    path.write_bytes(path.read_bytes().replace(b'"prob"', b'"bp"'))
    with pytest.raises(HashMismatch, match="modified"):
        run_reg.get_artifact(ref)
    path.unlink()
    with pytest.raises(HashMismatch, match="missing"):
        run_reg.get_artifact(ref)


@pytest.mark.parametrize("name", ["", ".hidden", "..", "a/b", "a\\b", "x" * 129, "name with space", "NUL",
                                  "con.txt", "com1", "Manifest"])
def test_artifact_names_are_validated(run_reg: Registry, factory, name: str) -> None:
    with pytest.raises(SchemaError, match="artifact name"):
        run_reg.put_artifact(factory.RUN_A, name, b"x")


def test_artifact_names_are_unique_case_blind(run_reg: Registry, factory) -> None:
    ref = run_reg.put_artifact(factory.RUN_A, "Card", b"first")
    with pytest.raises(SchemaError, match="case-blind"):
        run_reg.put_artifact(factory.RUN_A, "card", b"second")       # one file on NTFS
    assert run_reg.get_artifact(ref) == b"first"


def test_artifacts_are_written_once(run_reg: Registry, factory) -> None:
    with pytest.raises(SchemaError, match="reserved"):
        run_reg.put_artifact(factory.RUN_A, "manifest", b"x")
    ref = run_reg.put_artifact(factory.RUN_A, "note", b"first")
    with pytest.raises(SchemaError, match="written once"):
        run_reg.put_artifact(factory.RUN_A, "note", b"second")
    with pytest.raises(SchemaError, match="unsupported artifact type"):
        run_reg.put_artifact(factory.RUN_A, "dict", {"a": 1})
    assert run_reg.get_artifact(ref) == b"first"
    assert _no_temp_files(run_reg.artifact_root)
    assert [i.name for i in run_reg.list_artifacts(factory.RUN_A)] == ["note"]


def test_lookups_that_do_not_resolve(run_reg: Registry, factory) -> None:
    with pytest.raises(EvidenceMissing):
        run_reg.get_artifact(f"{factory.RUN_A}:nothing:")
    with pytest.raises(SchemaError):
        run_reg.get_artifact("not-a-ref")
    with pytest.raises(EvidenceMissing):
        run_reg.artifact_info(f"{factory.RUN_A}:nothing:")


def test_manifest_reference(run_reg: Registry, factory) -> None:
    manifest = run_reg.get_artifact(f"{factory.RUN_A}:manifest:")
    assert isinstance(manifest, RunManifest) and manifest.run_id == factory.RUN_A
    assert run_reg.get_artifact(f"{factory.RUN_A}:manifest:/kind") == "quarter"
    assert run_reg.get_artifact(f"{factory.RUN_A}:manifest:/scenario_hashes/SEARCH:M1") == factory.H


def test_parents_must_exist_and_share_the_data_class(reg: Registry, factory) -> None:
    reg.begin_run(factory.manifest())
    reg.begin_run(factory.manifest(factory.RUN_B, data_class=DataClass.REAL))
    real = reg.put_artifact(factory.RUN_B, "real_input", b"x")
    with pytest.raises(EvidenceMissing, match="not registered"):
        reg.put_artifact(factory.RUN_A, "child", b"y", parents=[f"{factory.RUN_A}:ghost:"])
    with pytest.raises(DataClassMixError):
        reg.put_artifact(factory.RUN_A, "child", b"y", parents=[real])
    ref = reg.put_artifact(factory.RUN_A, "child", b"y", parents=[f"{factory.RUN_A}:manifest:"])
    assert reg.artifact_info(ref).parents == (f"{factory.RUN_A}:manifest:",)


def test_canonical_hash_ignores_run_ids_but_checksum_does_not(reg: Registry, factory) -> None:
    hashes = {}
    for run in (factory.RUN_A, factory.RUN_B):
        reg.begin_run(factory.manifest(run))
        node = ProvenanceNode(ref=f"{run}:cards:/0", kind="card", parents=(f"{run}:manifest:",), hash=factory.H)
        info = reg.artifact_info(reg.put_artifact(run, "node", node))
        reg.end_run(run, "OK")
        hashes[run] = (info.checksum, info.canonical_hash, reg.get_manifest(run).canonical_artifact_hashes["node"])
    (ca, na, ma), (cb, nb, mb) = hashes[factory.RUN_A], hashes[factory.RUN_B]
    assert ca != cb and na == nb and ma == mb == na


def test_artifact_paths_are_relative_and_under_the_run(run_reg: Registry, factory, paths: SimpleNamespace) -> None:
    info = run_reg.artifact_info(run_reg.put_artifact(factory.RUN_A, "duals", _duals()))
    assert info.rel_path == f"{factory.RUN_A}/artifacts/duals.npz"
    assert (paths.root / info.rel_path).is_file() and not Path(info.rel_path).is_absolute()
