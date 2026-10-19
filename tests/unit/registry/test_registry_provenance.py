"""Provenance and references (BUILD_SPEC v1.1 §1.8, §4.6; ARCH §10.6): RFC 6901 pointers and the
run → artifact provenance DAG. Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.claims import ProvenanceNode
from adic_tpa.contracts.errors import EvidenceMissing, SchemaError
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.registry import Registry
from adic_tpa.registry.provenance import (
    artifact_ref, escape_token, join_pointer, manifest_ref, parse_ref, resolve_pointer, split_pointer,
)


def test_pointer_tokens_round_trip() -> None:
    tokens = ("rows", "T6/M6", "a~b", "", "0")
    pointer = join_pointer(tokens)
    assert pointer == "/rows/T6~1M6/a~0b//0"
    assert split_pointer(pointer) == tokens
    assert split_pointer("") == ()
    assert escape_token("~/") == "~0~1"
    with pytest.raises(SchemaError):
        split_pointer("rows")


def test_resolve_pointer_on_json_arrays_and_models(factory) -> None:
    doc = {"rows": {"T6": {"M6": 0.0058}}, "list": [10, 20], "": "empty-key", "a/b": 1}
    assert resolve_pointer(doc, "") is doc
    assert resolve_pointer(doc, "/rows/T6/M6") == 0.0058
    assert resolve_pointer(doc, "/list/1") == 20
    assert resolve_pointer(doc, "/") == "empty-key"
    assert resolve_pointer(doc, "/a~1b") == 1
    arr = np.arange(6.0).reshape(2, 3)
    assert resolve_pointer({"x": arr}, "/x/1/2") == 5.0 and isinstance(resolve_pointer({"x": arr}, "/x/1/2"), float)
    np.testing.assert_array_equal(resolve_pointer({"x": arr}, "/x/0"), arr[0])
    assert resolve_pointer(factory.metric_def(), "/unit") == "prob"
    assert resolve_pointer({"m": factory.metric_def()}, "/m")["unit"] == "prob"   # models come back as JSON
    for bad in ("/missing", "/list/2", "/list/01", "/list/x", "/rows/T6/M6/deeper"):
        with pytest.raises(EvidenceMissing):
            resolve_pointer(doc, bad, where="test")
    with pytest.raises(EvidenceMissing):
        resolve_pointer({"x": np.float64(1.0)}, "/x/0")


def test_reference_builders(factory) -> None:
    assert manifest_ref(factory.RUN_A) == f"{factory.RUN_A}:manifest:"
    assert artifact_ref(factory.RUN_A, "tier1_board", "rows", "T6", "M6", "cp_upper") == \
        f"{factory.RUN_A}:tier1_board:/rows/T6/M6/cp_upper"
    ref = parse_ref(f"{factory.RUN_A}:tier1_board:/rows/T6")
    assert (ref.run_id, ref.artifact, ref.pointer) == (factory.RUN_A, "tier1_board", "/rows/T6")
    with pytest.raises(SchemaError):
        parse_ref("run-x:tier1_board:")


def _walk(reg: Registry, ref: str) -> dict[str, ProvenanceNode]:
    nodes: dict[str, ProvenanceNode] = {}
    todo = [ref]
    while todo:
        node = reg.get_provenance(todo.pop())
        nodes[node.ref] = node
        todo += [p for p in node.parents if p not in nodes]
    return nodes


def test_provenance_dag_from_artifact_to_parent_runs(reg: Registry, factory) -> None:
    reg.begin_run(factory.manifest())
    cube = reg.put_artifact(factory.RUN_A, "cube_meta", factory.metric_def(), kind="scenario_cube")
    reg.end_run(factory.RUN_A, "OK")
    reg.begin_run(factory.manifest(factory.RUN_B, parents=(factory.RUN_A,)))
    card = reg.put_artifact(factory.RUN_B, "decision_card", b"SYNTHETIC card", kind="decision_card", parents=[cube])
    node = reg.get_provenance(f"{card}/0/legs")
    assert node.ref == f"{card}/0/legs" and node.kind == "decision_card"
    assert node.parents == (cube, manifest_ref(factory.RUN_B))
    assert node.hash == reg.artifact_info(card).checksum
    run_b = reg.get_provenance(manifest_ref(factory.RUN_B))
    assert run_b.kind == "run" and run_b.parents == (manifest_ref(factory.RUN_A),)
    assert run_b.hash == content_hash(reg.get_manifest(factory.RUN_B))          # the manifest as begun
    dag = _walk(reg, card)
    assert set(dag) == {card, cube, manifest_ref(factory.RUN_A), manifest_ref(factory.RUN_B)}
    assert dag[manifest_ref(factory.RUN_A)].parents == ()
    with pytest.raises(EvidenceMissing):
        reg.get_provenance(f"{factory.RUN_B}:ghost:")
    with pytest.raises(EvidenceMissing):
        reg.get_provenance(manifest_ref(factory.RUN_C))
