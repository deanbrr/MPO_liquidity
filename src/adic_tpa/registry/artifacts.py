"""Artifact files of the registry (BUILD_SPEC v1.1 §4.6, §1.12, §2; owner WP-04).

An artifact lives at ``<artifact_root>/<run_id>/artifacts/<name><ext>`` (``runs/`` is git-ignored, §2) and is
indexed by one hash-chained registry row holding its ``ArtifactInfo``. Formats:

- ``json``: a Pydantic model, written as the canonical-JSON envelope ``{"artifact", "body", "class", "data_class",
  "footer", "is_synthetic"}`` so every JSON artifact of a SYNTHETIC run carries the SYNTHETIC footer (§1.12 rule 3);
- ``npz``: an ``ArrayContainer`` through ``ArrayContainer.to_npz`` (validated first when ``ARRAY_SPECS`` has the
  class);
- ``arrow``: a ``pyarrow.Table`` as an Arrow IPC file whose schema metadata carries the labels. §4.6 names
  Parquet, but this machine's application-control policy blocks pyarrow's Parquet DLL, so the store uses Arrow
  IPC (Feather v2), which pyarrow, pandas and R read alike (recorded deviation; the format is per-row, so a later
  switch is local);
- ``bytes``: raw bytes.

Three hashes per artifact: ``checksum`` (content identity: ``content_hash`` of a model, the container checksum,
the table checksum, or sha256 of bytes), ``canonical_hash`` (``canonical_artifact_hash`` of a model, volatile
fields normalized; the raw checksum otherwise, BUILD-27) and ``file_sha256`` (the file bytes, tamper evidence).
Reads verify ``file_sha256`` and then the content checksum, and raise ``HashMismatch`` on any difference.

Classes are restored only from ``adic_tpa.contracts`` (always importable here, §4.0): a model defined elsewhere
comes back as its JSON body unless the caller passes ``model=``, so the registry never loads engine code into
the lab, room or analyst processes.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Final, Literal

from pydantic import BaseModel

from adic_tpa import SYNTHETIC_FOOTER
from adic_tpa.contracts.arrays import ARRAY_SPECS, ArrayContainer
from adic_tpa.contracts.config import load_json_payload
from adic_tpa.contracts.enums import DataClass
from adic_tpa.contracts.errors import EvidenceMissing, HashMismatch, SchemaError
from adic_tpa.contracts.hashing import canonical_json, content_hash, normalize_volatile, sha256_hex, to_jsonable
from adic_tpa.contracts.ids import ArtifactRef, RunId
from adic_tpa.registry.chain import RegistryModel
from adic_tpa.registry.provenance import resolve_pointer, split_pointer

if TYPE_CHECKING:
    import pyarrow as pa

__all__ = [
    "ArtifactFormat", "ArtifactInfo", "Encoded", "ARTIFACT_NAME_RE", "RESERVED_NAMES", "EXTENSIONS", "LABEL_PREFIX",
    "check_name", "class_path", "resolve_class", "write_artifact", "read_artifact", "file_sha256", "table_checksum",
    "verify_file",
]

ArtifactFormat = Literal["json", "npz", "arrow", "bytes"]
EXTENSIONS: Final[Mapping[ArtifactFormat, str]] = MappingProxyType(
    {"json": ".json", "npz": ".npz", "arrow": ".arrow", "bytes": ".bin"})
# The §1.8 artifact component ([A-Za-z0-9_.-]+) without a leading dot, so no name is "." or ".." or hidden.
ARTIFACT_NAME_RE: Final = re.compile(r"^[A-Za-z0-9_-][A-Za-z0-9_.-]{0,127}$")
RESERVED_NAMES: Final = frozenset({"manifest"})   # "<run_id>:manifest:" is the run's manifest (provenance root)
# Windows device names cannot be file names, whatever the extension (NTFS); names are also unique case-blind.
_DEVICE_NAMES: Final = frozenset({"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
                                  *(f"lpt{i}" for i in range(1, 10))})
LABEL_PREFIX: Final = b"adic_tpa."                 # Arrow schema-metadata keys the store adds (stripped on read)
_CHUNK: Final = 1 << 20
_CONTRACTS: Final = "adic_tpa.contracts"


class ArtifactInfo(RegistryModel):
    """The hash-chained registry row of one artifact (the body of a chain row of kind ``artifact``)."""

    run_id: RunId
    name: str
    format: ArtifactFormat
    class_path: str | None          # "<module>:<qualname>" of the stored model or container
    kind: str                       # provenance kind (producer-supplied, else the class name, "table" or "bytes")
    rel_path: str                   # POSIX path under the artifact root (never absolute)
    checksum: str
    canonical_hash: str
    file_sha256: str
    nbytes: int
    parents: tuple[ArtifactRef, ...]
    data_class: DataClass

    @property
    def ref(self) -> ArtifactRef:
        return ArtifactRef.make(self.run_id, self.name)


@dataclass(frozen=True, slots=True)
class Encoded:
    """What ``write_artifact`` learned while writing."""

    format: ArtifactFormat
    class_path: str | None
    default_kind: str
    checksum: str
    canonical_hash: str


def check_name(name: str) -> str:
    """Validate an artifact name (§1.8 artifact component, no leading dot, not reserved)."""
    if not isinstance(name, str) or not ARTIFACT_NAME_RE.fullmatch(name):
        raise SchemaError(f"invalid artifact name {name!r}: expected [A-Za-z0-9_.-]{{1,128}} without a leading dot")
    if name.lower() in RESERVED_NAMES:
        raise SchemaError(f"artifact name {name!r} is reserved (the run manifest)")
    if name.split(".", 1)[0].lower() in _DEVICE_NAMES:
        raise SchemaError(f"invalid artifact name {name!r}: a Windows device name")
    return name


def class_path(cls: type) -> str:
    return f"{cls.__module__}:{cls.__qualname__}"


def resolve_class(path: str | None, base: type) -> type | None:
    """The class named by ``path`` if it lives in ``adic_tpa.contracts`` and subclasses ``base``, else None."""
    if not path:
        return None
    module, _, qualname = path.partition(":")
    if module != _CONTRACTS and not module.startswith(_CONTRACTS + "."):
        return None
    try:
        obj: Any = importlib.import_module(module)
    except ImportError:
        return None
    for part in qualname.split("."):
        obj = getattr(obj, part, None)
        if obj is None:
            return None
    return obj if isinstance(obj, type) and issubclass(obj, base) else None


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(_CHUNK), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def _normalized_table(t: pa.Table) -> pa.Table:
    t = t.combine_chunks()
    return t.replace_schema_metadata(t.schema.metadata or None)


def table_checksum(t: pa.Table) -> str:
    """sha256 of the Arrow IPC stream of the table with chunks combined (schema metadata included)."""
    import pyarrow as pa

    t = _normalized_table(t)
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, t.schema) as writer:
        writer.write_table(t)
    return sha256_hex(sink.getvalue().to_pybytes())


def _is_table(obj: object) -> bool:
    if not type(obj).__module__.startswith("pyarrow"):
        return False
    import pyarrow as pa

    return isinstance(obj, pa.Table)


def _labels(name: str, data_class: DataClass) -> dict[str, Any]:
    synthetic = data_class == DataClass.SYNTHETIC
    return {"artifact": name, "data_class": data_class.value, "is_synthetic": synthetic,
            "footer": SYNTHETIC_FOOTER if synthetic else None}


def write_artifact(obj: object, path: Path, *, name: str, data_class: DataClass) -> Encoded:
    """Serialize ``obj`` to ``path`` (BaseModel | ArrayContainer | pyarrow.Table | bytes); see the module doc."""
    if isinstance(obj, BaseModel):
        body = to_jsonable(obj)
        path.write_bytes(canonical_json({**_labels(name, data_class), "body": body, "class": class_path(type(obj))}))
        # == content_hash(obj) and canonical_artifact_hash(obj), without serializing the model twice more
        return Encoded("json", class_path(type(obj)), type(obj).__name__, sha256_hex(canonical_json(body)),
                       sha256_hex(canonical_json(normalize_volatile(body))))
    if isinstance(obj, ArrayContainer):
        if type(obj).__name__ in ARRAY_SPECS:
            obj.validate()
        checksum = obj.to_npz(path)
        return Encoded("npz", class_path(type(obj)), type(obj).__name__, checksum, checksum)
    if isinstance(obj, (bytes, bytearray, memoryview)):
        data = bytes(obj)
        path.write_bytes(data)
        return Encoded("bytes", None, "bytes", sha256_hex(data), sha256_hex(data))
    if _is_table(obj):
        import pyarrow as pa

        table: pa.Table = obj  # type: ignore[assignment]
        meta = dict(table.schema.metadata or {})
        meta.update({LABEL_PREFIX + k.encode("ascii"): json.dumps(v).encode("utf-8")
                     for k, v in _labels(name, data_class).items()})
        labelled = table.replace_schema_metadata(meta)
        with pa.OSFile(str(path), "wb") as sink, pa.ipc.new_file(sink, labelled.schema) as writer:
            writer.write_table(labelled)
        checksum = table_checksum(table)
        return Encoded("arrow", None, "table", checksum, checksum)
    raise SchemaError(f"unsupported artifact type {type(obj).__name__}: expected a Pydantic model, an "
                      "ArrayContainer, a pyarrow.Table or bytes")


def verify_file(path: Path, info: ArtifactInfo) -> None:
    """Raise ``HashMismatch`` if the artifact file is missing or its bytes differ from the registered hash."""
    if not path.is_file():
        raise HashMismatch(f"{info.ref}: artifact file is missing", {"ref": str(info.ref), "path": info.rel_path})
    actual = file_sha256(path)
    if actual != info.file_sha256:
        raise HashMismatch(f"{info.ref}: artifact file was modified (sha256 {actual} != {info.file_sha256})",
                           {"ref": str(info.ref), "path": info.rel_path})


def _mismatch(info: ArtifactInfo, actual: str) -> HashMismatch:
    return HashMismatch(f"{info.ref}: decoded content checksum {actual} != registered {info.checksum}",
                        {"ref": str(info.ref)})


def _read_json(path: Path, info: ArtifactInfo, pointer: str, model: type | None) -> Any:
    env = json.loads(path.read_bytes())
    body = env["body"]
    if pointer:
        return resolve_pointer(body, pointer, where=str(info.ref))
    cls = model if model is not None else resolve_class(info.class_path, BaseModel)
    if cls is None:
        actual = sha256_hex(canonical_json(body))
        if actual != info.checksum:
            raise _mismatch(info, actual)
        return body
    if not (isinstance(cls, type) and issubclass(cls, BaseModel)):
        raise SchemaError(f"{info.ref}: model= must be a Pydantic model class for a json artifact")
    obj = load_json_payload(json.dumps(body, ensure_ascii=False), cls)
    actual = content_hash(obj)
    if actual != info.checksum:
        raise _mismatch(info, actual)
    return obj


def _read_npz(path: Path, info: ArtifactInfo, pointer: str, model: type | None) -> Any:
    cls = model if model is not None else resolve_class(info.class_path, ArrayContainer)
    if cls is None:
        raise SchemaError(f"{info.ref}: container class {info.class_path} is not in adic_tpa.contracts; "
                          "pass model=<the ArrayContainer class>", {"ref": str(info.ref)})
    if not (isinstance(cls, type) and issubclass(cls, ArrayContainer)):
        raise SchemaError(f"{info.ref}: model= must be an ArrayContainer class for an npz artifact")
    obj = cls.from_npz(path, expected_checksum=info.checksum)
    return resolve_pointer(obj, pointer, where=str(info.ref)) if pointer else obj


def _read_arrow(path: Path, info: ArtifactInfo, pointer: str) -> Any:
    import pyarrow as pa

    table = pa.ipc.open_file(pa.py_buffer(path.read_bytes())).read_all()
    meta = {k: v for k, v in (table.schema.metadata or {}).items() if not k.startswith(LABEL_PREFIX)}
    table = table.replace_schema_metadata(meta or None)
    actual = table_checksum(table)
    if actual != info.checksum:
        raise _mismatch(info, actual)
    if not pointer:
        return table
    # Tables resolve column-wise: /<column> is the column's values, /<column>/<row> one value.
    column = split_pointer(pointer)[0]
    if column not in table.column_names:
        raise EvidenceMissing(f"{info.ref}: pointer {pointer!r} names no column", {"ref": str(info.ref)})
    return resolve_pointer({column: table.column(column).to_pylist()}, pointer, where=str(info.ref))


def read_artifact(path: Path, info: ArtifactInfo, *, pointer: str = "", model: type | None = None) -> Any:
    """Decode an artifact file (already ``verify_file``-checked) and resolve ``pointer`` inside it (RFC 6901)."""
    if info.format == "json":
        return _read_json(path, info, pointer, model)
    if info.format == "npz":
        return _read_npz(path, info, pointer, model)
    if info.format == "arrow":
        return _read_arrow(path, info, pointer)
    data = path.read_bytes()
    if sha256_hex(data) != info.checksum:
        raise _mismatch(info, sha256_hex(data))
    if pointer:
        raise EvidenceMissing(f"{info.ref}: a bytes artifact has no JSON pointer targets", {"ref": str(info.ref)})
    return data
