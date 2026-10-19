"""Configuration loading in Pydantic JSON mode (BUILD_SPEC v1.1 §1.11, §4.1; S-ADR-39).

Contracts models are strict, so strict Python-mode validation would reject enum strings and YAML lists for tuple
fields. ``load_yaml`` therefore parses YAML with ``yaml.safe_load`` and validates the JSON text
(``model.model_validate_json(json.dumps(raw, default=iso))``); MCP payloads and registry rows go through
``load_json_payload``. Validation and parse failures raise ``SchemaError`` (the Pydantic error list is in
``context["errors"]``).

Each successful ``load_yaml`` appends the file's LF-normalized hash to a process-level audit list
(``loaded_config_files``), the one sanctioned piece of module-level mutable state in ``contracts``. A loader that
caches its result (``GroupRegistry.for_version``) re-records the cached load with ``note_config_load`` on every
hit, so a manifest built after ``clear_config_audit()`` still lists every file the process uses.

Boundary rule (§1.10): constructing a model directly raises ``pydantic.ValidationError``, which is not a
``TPAError``. Code that validates data crossing a WP boundary uses ``load_yaml``, ``load_json_payload`` or
``validate_model``, which raise ``SchemaError``. Validators that detect a run-mode or data-class clash raise
``RunModeRefused`` or ``DataClassMixError`` themselves, and those pass through all three loaders unchanged.

Config files declare their model in a header comment, ``# model: <module>:<Class>`` (comments do not reach the
model), which ``tests/unit/test_config_roundtrip.py`` and ``tpa config show`` read via ``declared_model_path``.
"""

from __future__ import annotations

import json
import re
import threading
from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum
from pathlib import Path
from typing import Any, Final, TypeVar

import yaml
from pydantic import BaseModel, ValidationError

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import file_hash, package_root

__all__ = [
    "load_yaml", "load_yaml_audited", "load_json_payload", "validate_model", "iso", "ConfigLoad",
    "loaded_config_files", "clear_config_audit", "note_config_load", "declared_model_path", "MODEL_HEADER_RE",
    "config_root",
]

T = TypeVar("T", bound=BaseModel)

MODEL_HEADER_RE: Final = re.compile(r"^#\s*model:\s*(?P<path>[A-Za-z_][\w.]*:[A-Za-z_]\w*)\s*$")


@dataclass(frozen=True, slots=True)
class ConfigLoad:
    """One audited config load."""

    path: str
    file_hash: str
    model: str


_AUDIT: list[ConfigLoad] = []
_AUDIT_LOCK = threading.Lock()


def iso(obj: Any) -> Any:
    """``json.dumps`` default: dates and datetimes as ISO-8601 text, enums by value, Pydantic models in JSON mode."""
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")
    raise TypeError(f"object of type {type(obj).__name__} is not JSON serializable")


def config_root() -> Path:
    """``src/adic_tpa/config``."""
    return package_root() / "config"


def _validation_error(where: str, model: type[BaseModel], err: ValidationError) -> SchemaError:
    errors = json.loads(err.json(include_url=False))
    first = errors[0] if errors else {}
    loc = ".".join(str(p) for p in first.get("loc", ()))
    return SchemaError(f"{where}: invalid {model.__name__} ({err.error_count()} errors; first at {loc or '<root>'}: "
                       f"{first.get('msg', '')})", {"where": where, "model": model.__name__, "errors": errors})


def load_yaml(path: Path, model: type[T]) -> T:
    """Load ``path`` with ``yaml.safe_load`` and validate it into ``model`` in JSON mode; audit the file hash."""
    return load_yaml_audited(path, model)[0]


def load_yaml_audited(path: Path, model: type[T]) -> tuple[T, ConfigLoad]:
    """``load_yaml`` that also returns the audit record it appended (for loaders that cache, see module doc)."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
        raw = yaml.safe_load(text)
        payload = json.dumps(raw, default=iso)
    except (OSError, UnicodeDecodeError, yaml.YAMLError, TypeError) as exc:
        raise SchemaError(f"{p}: cannot read YAML ({exc})", {"where": str(p)}) from exc
    try:
        obj = model.model_validate_json(payload)
    except ValidationError as exc:
        raise _validation_error(str(p), model, exc) from exc
    record = ConfigLoad(path=str(p.resolve()), file_hash=file_hash(p), model=f"{model.__module__}:{model.__qualname__}")
    with _AUDIT_LOCK:
        _AUDIT.append(record)
    return obj, record


def load_json_payload(raw: str | bytes, model: type[T]) -> T:
    """Validate a JSON payload (MCP tool I/O, registry rows) into ``model`` with ``model_validate_json``."""
    try:
        return model.model_validate_json(raw)
    except ValidationError as exc:
        raise _validation_error("json payload", model, exc) from exc


def validate_model(model: type[T], data: Any) -> T:
    """Validate Python data (a mapping, possibly holding enums, dates and models) into ``model`` in JSON mode.

    The data is serialized with ``json.dumps(default=iso)`` first, so strict models accept enum members and
    strings, tuples given as lists and nested models alike; failures raise ``SchemaError`` (§1.10 boundary rule).
    """
    try:
        payload = json.dumps(data, default=iso)
    except (TypeError, ValueError) as exc:
        raise SchemaError(f"validate_model: {model.__name__} data is not JSON-serializable ({exc})",
                          {"model": model.__name__}) from exc
    try:
        return model.model_validate_json(payload)
    except ValidationError as exc:
        raise _validation_error("python data", model, exc) from exc


def loaded_config_files() -> tuple[ConfigLoad, ...]:
    """Every config file loaded by this process, in load order (hashed into manifests)."""
    with _AUDIT_LOCK:
        return tuple(_AUDIT)


def clear_config_audit() -> None:
    """Reset the audit list (tests and long-lived worker processes)."""
    with _AUDIT_LOCK:
        _AUDIT.clear()


def note_config_load(record: ConfigLoad) -> None:
    """Re-record a cached load (no file read) unless the audit list already holds that record."""
    with _AUDIT_LOCK:
        if record not in _AUDIT:
            _AUDIT.append(record)


def declared_model_path(path: Path) -> str | None:
    """The ``module:Class`` named by the file's ``# model:`` header comment (leading comment block), or None."""
    with open(Path(path), encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped:
                continue
            if not stripped.startswith("#"):
                return None
            m = MODEL_HEADER_RE.match(stripped)
            if m:
                return m.group("path")
    return None
