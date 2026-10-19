"""Artifact references and provenance nodes (BUILD_SPEC v1.1 §1.8, §3.16, §4.6; ARCH §10.6; owner WP-04).

A reference is ``<run_id>:<artifact>:<json-pointer>`` (§1.8), e.g. ``run-…:tier1_board:/rows/T6/M6/cp_upper``.
The pointer is RFC 6901 and resolves inside the artifact's JSON form: a model's JSON body, a container's fields
(then array axes, then JSON), or a table's columns. ``<run_id>:manifest:`` names the run itself.

Provenance is a DAG of ``ProvenanceNode``: an artifact's parents are the references its producer declared
(``put_artifact(..., parents=...)``) plus the manifest of the run that produced it; a run's parents are the
manifests of its ``parent_runs``. ``claims.provenance_dag`` walks it through ``Registry.get_provenance``.
"""

from __future__ import annotations

import dataclasses
import re
from collections.abc import Iterable, Mapping, Sequence
from enum import Enum
from typing import Any, Final

import numpy as np
from pydantic import BaseModel

from adic_tpa.contracts.claims import ProvenanceNode
from adic_tpa.contracts.errors import EvidenceMissing, SchemaError
from adic_tpa.contracts.ids import ArtifactRef, RunId

__all__ = [
    "MANIFEST_ARTIFACT", "parse_ref", "manifest_ref", "artifact_ref", "split_pointer", "join_pointer",
    "escape_token", "resolve_pointer", "run_node", "artifact_node",
]

MANIFEST_ARTIFACT: Final = "manifest"
_INDEX_RE: Final = re.compile(r"^(?:0|[1-9][0-9]*)$")


def parse_ref(ref: ArtifactRef | str) -> ArtifactRef:
    """Validate a reference (``SchemaError`` on a malformed one)."""
    return ref if isinstance(ref, ArtifactRef) else ArtifactRef(str(ref))


def manifest_ref(run_id: RunId | str) -> ArtifactRef:
    return ArtifactRef.make(str(run_id), MANIFEST_ARTIFACT)


def artifact_ref(run_id: RunId | str, name: str, *tokens: str | int) -> ArtifactRef:
    """``<run_id>:<name>:<pointer>`` with the pointer built from unescaped tokens."""
    return ArtifactRef.make(str(run_id), name, join_pointer(tokens))


def escape_token(token: str | int) -> str:
    return str(token).replace("~", "~0").replace("/", "~1")


def join_pointer(tokens: Iterable[str | int]) -> str:
    return "".join("/" + escape_token(t) for t in tokens)


def split_pointer(pointer: str) -> tuple[str, ...]:
    """RFC 6901 reference tokens of ``pointer`` ("" is the whole document)."""
    if pointer == "":
        return ()
    if not pointer.startswith("/"):
        raise SchemaError(f"JSON pointer {pointer!r} must be empty or start with '/'")
    return tuple(t.replace("~1", "/").replace("~0", "~") for t in pointer[1:].split("/"))


def _key_text(key: object) -> str:
    return str(key.value) if isinstance(key, Enum) else str(key)


def _missing(where: str, pointer: str, token: str, what: str) -> EvidenceMissing:
    return EvidenceMissing(f"{where}: pointer {pointer!r} does not resolve at {token!r} ({what})",
                           {"ref": where, "pointer": pointer, "token": token})


def _step(node: Any, token: str, where: str, pointer: str) -> Any:
    if isinstance(node, BaseModel):
        node = node.model_dump(mode="json")
    if isinstance(node, Mapping):
        if token in node:
            return node[token]
        for key, value in node.items():
            if _key_text(key) == token:
                return value
        raise _missing(where, pointer, token, "no such key")
    if isinstance(node, (list, tuple)) or (isinstance(node, np.ndarray) and node.ndim > 0):
        if not _INDEX_RE.fullmatch(token):
            raise _missing(where, pointer, token, "not an array index")
        length = len(node)
        if int(token) >= length:
            raise _missing(where, pointer, token, f"index out of range (length {length})")
        return node[int(token)]
    if dataclasses.is_dataclass(node) and not isinstance(node, type):
        if token in {f.name for f in dataclasses.fields(node)}:
            return getattr(node, token)
        raise _missing(where, pointer, token, "no such field")
    raise _missing(where, pointer, token, f"cannot descend into {type(node).__name__}")


def resolve_pointer(doc: Any, pointer: str, *, where: str = "artifact") -> Any:
    """Resolve an RFC 6901 pointer in ``doc``; raise ``EvidenceMissing`` when it does not resolve.

    Models are read in their JSON form; containers by field; arrays by leading axis. A numpy scalar comes back
    as a Python number, a model as its JSON form.
    """
    node = doc
    for token in split_pointer(pointer):
        node = _step(node, token, where, pointer)
    if isinstance(node, np.generic):
        return node.item()
    if isinstance(node, BaseModel):
        return node.model_dump(mode="json")
    return node


def run_node(run_id: RunId | str, manifest_hash: str, parent_runs: Sequence[RunId | str]) -> ProvenanceNode:
    """Node of a run: its manifest, with the parent runs' manifests as parents."""
    return ProvenanceNode(ref=manifest_ref(run_id), kind="run",
                          parents=tuple(manifest_ref(p) for p in parent_runs), hash=manifest_hash)


def artifact_node(ref: ArtifactRef, kind: str, parents: Sequence[ArtifactRef], checksum: str) -> ProvenanceNode:
    """Node of an artifact reference: declared parents, then the producing run's manifest (deduplicated)."""
    ordered = tuple(dict.fromkeys((*parents, manifest_ref(ref.run_id))))
    return ProvenanceNode(ref=ref, kind=kind, parents=ordered, hash=checksum)
