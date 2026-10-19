"""Canonical JSON, content hashes, array checksums and tree hashes (BUILD_SPEC v1.1 §4.1, §1.8, S-ADR-42).

``canonical_json`` is the single serialization behind every content hash, signature payload and registry row
hash: sorted keys, separators ``(",", ":")``, UTF-8, floats by ``repr`` (−0.0 normalized to 0.0), NaN and ±inf
rejected, datetimes as ISO-8601 UTC with ``Z`` (naive datetimes are read as UTC), dates as ISO-8601, enums by
value, numpy arrays and array containers by checksum, Pydantic models through ``model_dump(mode="python")`` and
the same conversions (so datetimes are normalized, which ``mode="json"`` would not do). Hashes are therefore
stable across processes, machines and ``PYTHONHASHSEED`` values.

Text files are hashed with CRLF→LF normalization so checkouts with different ``core.autocrlf`` agree.
``canonical_artifact_hash`` additionally normalizes the declared ``VOLATILE_FIELDS`` (§9.4 #9; BUILD-27).
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import fields, is_dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal
from enum import Enum
from pathlib import Path, PurePath
from typing import Any, Final

import numpy as np
from pydantic import BaseModel

from adic_tpa.contracts.errors import SchemaError

__all__ = [
    "canonical_json", "to_jsonable", "content_hash", "array_checksum", "file_hash", "file_tree_hash",
    "engine_tree_hash", "config_hash", "package_root", "VOLATILE_FIELDS", "canonical_artifact_hash",
    "normalize_volatile", "DEFAULT_TREE_PATTERNS", "TEXT_SUFFIXES", "VOLATILE_PLACEHOLDER", "RUN_PLACEHOLDER",
    "PATH_PLACEHOLDER", "sha256_hex",
]

DEFAULT_TREE_PATTERNS: Final[tuple[str, ...]] = ("**/*.py", "**/*.yaml", "**/*.csv", "**/*.md", "**/*.j2", "**/*.js")
TEXT_SUFFIXES: Final = frozenset({
    ".py", ".pyi", ".yaml", ".yml", ".csv", ".md", ".j2", ".js", ".json", ".jsonl", ".txt", ".html", ".css",
    ".sql", ".toml", ".sha256", ".cfg", ".ini"})

# Field names whose values differ between two runs of the same manifest (run ids, wall-clock stamps, chain
# hashes, signatures over wall-clock stamps, measured durations). Absolute paths and run-id prefixes inside any
# string (ArtifactRefs included) are normalized by value.
VOLATILE_FIELDS: Final[frozenset[str]] = frozenset({
    "run_id", "created_at", "recorded_at", "cast_at", "locked_at", "raised_at", "signed_at", "confirmed_at",
    "expires_at", "started_at", "finished_at", "ts", "prev_hash", "record_hash", "row_hash", "chain_hash",
    "chain_head", "signature", "time_s", "latency_s", "cpu_s",
})
VOLATILE_PLACEHOLDER: Final = "<volatile>"
RUN_PLACEHOLDER: Final = "<run>"
PATH_PLACEHOLDER: Final = "<path>"

_RUN_ID_RE: Final = re.compile(r"run-\d{8}T\d{6}Z-[0-9a-f]{8}")
_WIN_ABS_PATH_RE: Final = re.compile(r"^(?:[A-Za-z]:[\\/]|\\\\)")
_PATH_KEY_RE: Final = re.compile(r"(?:^|_)(?:path|paths|dir|root)$")


def sha256_hex(data: bytes) -> str:
    """``sha256:<hex>`` of ``data``."""
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _canonical_float(x: float) -> float:
    if not math.isfinite(x):
        raise SchemaError(f"canonical_json: non-finite float {x!r} is forbidden")
    return 0.0 if x == 0.0 else float(x)


def _iso_utc(dt: datetime) -> str:
    utc = dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    text = utc.strftime("%Y-%m-%dT%H:%M:%S")
    if utc.microsecond:
        text += f".{utc.microsecond:06d}"
    return text + "Z"


def _key(k: Any) -> str:
    if isinstance(k, Enum):
        k = k.value
    if isinstance(k, bool):
        return "true" if k else "false"
    if isinstance(k, (int, np.integer)):
        return str(int(k))
    if isinstance(k, str):
        return str(k)
    if isinstance(k, datetime):
        return _iso_utc(k)
    if isinstance(k, date):
        return k.isoformat()
    raise SchemaError(f"canonical_json: unsupported mapping key type {type(k).__name__}")


def _dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def to_jsonable(obj: Any) -> Any:
    """Convert ``obj`` to plain JSON types under the canonical rules (see module docstring)."""
    if obj is None or isinstance(obj, bool):
        return obj
    if isinstance(obj, Enum):
        return to_jsonable(obj.value)
    if isinstance(obj, int):
        return int(obj)
    if isinstance(obj, float):
        return _canonical_float(obj)
    if isinstance(obj, str):
        return str(obj)
    if isinstance(obj, BaseModel):
        return to_jsonable(obj.model_dump(mode="python"))
    if getattr(type(obj), "__tpa_array_container__", False):
        return obj.checksum()
    if isinstance(obj, np.ndarray):
        return array_checksum(obj)
    if isinstance(obj, np.generic):
        return to_jsonable(obj.item())
    if isinstance(obj, datetime):
        return _iso_utc(obj)
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, time):
        return obj.isoformat()
    if isinstance(obj, Mapping):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            key = _key(k)
            if key in out:
                raise SchemaError(f"canonical_json: mapping keys collide after conversion ({key!r})")
            out[key] = to_jsonable(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, (set, frozenset)):
        return sorted((to_jsonable(v) for v in obj), key=_dumps)
    if isinstance(obj, (bytes, bytearray, memoryview)):
        return bytes(obj).hex()
    if isinstance(obj, PurePath):
        return obj.as_posix()
    if isinstance(obj, Decimal):
        if not obj.is_finite():
            raise SchemaError(f"canonical_json: non-finite Decimal {obj!r} is forbidden")
        return str(obj)
    if is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: to_jsonable(getattr(obj, f.name)) for f in fields(obj)}
    raise SchemaError(f"canonical_json: unsupported type {type(obj).__name__}")


def canonical_json(obj: Any) -> bytes:
    """Canonical UTF-8 JSON bytes of ``obj`` (§4.1)."""
    return _dumps(to_jsonable(obj)).encode("utf-8")


def content_hash(obj: Any) -> str:
    """``sha256:<hex>`` of ``canonical_json(obj)``."""
    return sha256_hex(canonical_json(obj))


def array_checksum(*arrays: np.ndarray) -> str:
    """``sha256:<hex>`` over (dtype.str, shape, C-order bytes) of each array, in order."""
    h = hashlib.sha256()
    for a in arrays:
        arr = np.asarray(a)
        if arr.dtype.hasobject:
            raise SchemaError("array_checksum: object arrays are not hashable")
        c = np.ascontiguousarray(arr)
        h.update(f"{c.dtype.str}|{','.join(str(n) for n in c.shape)}|{c.nbytes};".encode("ascii"))
        h.update(c.reshape(-1).view(np.uint8))
    return "sha256:" + h.hexdigest()


def _file_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return data


def file_hash(path: Path) -> str:
    """``sha256:<hex>`` of one file, text files LF-normalized."""
    return sha256_hex(_file_bytes(Path(path)))


def file_tree_hash(root: Path, patterns: Sequence[str] = DEFAULT_TREE_PATTERNS) -> str:
    """Hash of sorted relative POSIX paths and file bytes under ``root`` (text CRLF→LF; S-ADR-42).

    ``__pycache__`` and dot-directories are skipped. Each entry contributes ``path NUL length NUL bytes``.
    """
    base = Path(root)
    if not base.is_dir():
        raise SchemaError(f"file_tree_hash: {base} is not a directory")
    files: set[Path] = set()
    for pattern in patterns:
        for p in base.glob(pattern):
            rel_parts = p.relative_to(base).parts
            if p.is_file() and "__pycache__" not in rel_parts and not any(s.startswith(".") for s in rel_parts[:-1]):
                files.add(p)
    h = hashlib.sha256()
    for rel, p in sorted((p.relative_to(base).as_posix(), p) for p in files):
        data = _file_bytes(p)
        h.update(rel.encode("utf-8") + b"\0" + str(len(data)).encode("ascii") + b"\0")
        h.update(data)
    return "sha256:" + h.hexdigest()


def package_root() -> Path:
    """``src/adic_tpa`` of the running checkout."""
    return Path(__file__).resolve().parents[1]


def engine_tree_hash() -> str:
    """``file_tree_hash(src/adic_tpa)``."""
    return file_tree_hash(package_root())


def config_hash() -> str:
    """``file_tree_hash(src/adic_tpa/config)`` (§1.11)."""
    return file_tree_hash(package_root() / "config")


def normalize_volatile(node: Any, key: str | None = None) -> Any:
    """Replace volatile values in a ``to_jsonable`` tree (field names in ``VOLATILE_FIELDS``, run ids inside
    strings, absolute paths)."""
    if key is not None and key in VOLATILE_FIELDS:
        return VOLATILE_PLACEHOLDER
    if isinstance(node, dict):
        return {k: normalize_volatile(v, k) for k, v in node.items()}
    if isinstance(node, list):
        return [normalize_volatile(v, key) for v in node]
    if isinstance(node, str):
        if _WIN_ABS_PATH_RE.match(node) or (key is not None and _PATH_KEY_RE.search(key) and node.startswith("/")):
            return PATH_PLACEHOLDER
        return _RUN_ID_RE.sub(RUN_PLACEHOLDER, node)
    return node


def canonical_artifact_hash(obj: Any) -> str:
    """``content_hash`` after normalizing ``VOLATILE_FIELDS`` (two runs differing only in run ids and
    timestamps hash equal; e2e #9, BUILD-27)."""
    return sha256_hex(_dumps(normalize_volatile(to_jsonable(obj))).encode("utf-8"))
