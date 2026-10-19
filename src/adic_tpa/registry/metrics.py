"""Metric registry helpers (BUILD_SPEC v1.1 §4.6, §2, S-ADR-42; ARCH §10.3; CHAT_ANALYST §9.7; owner WP-04).

A metric id names one definition forever: any change of definition needs a new id (bump ``@v<k>``, ARCH §10.3),
so ``Registry.define_metric`` refuses an in-place change and names the next free version. MRM approval is a
separate append-only registry row (``Registry.approve_metric``).

Each WP declares its metrics in ``config/metrics/wp-NN.yaml`` (S-ADR-42); ``load_metric_catalog`` merges the
files with a duplicate-id check. The file model adds CHAT_ANALYST §9.7's label and scope fields to ``MetricDef``;
contracts does not define it yet, so it lives here as a local adapter (TODO(contracts)). Only the ``MetricDef``
fields enter the registry and the definition hash; labels and scope stay configuration.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Final

from pydantic import field_validator

from adic_tpa.contracts.config import config_root, load_yaml
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.evidence import MetricDef
from adic_tpa.contracts.hashing import canonical_json, content_hash
from adic_tpa.contracts.ids import MetricId
from adic_tpa.registry.chain import RegistryModel

__all__ = [
    "MetricCatalogEntry", "MetricCatalogFile", "METRIC_FILE_RE", "metrics_config_root", "load_metric_catalog",
    "catalog_definitions", "core_definition", "definition_hash", "by_key", "split_version", "next_version",
]

METRIC_FILE_RE: Final = re.compile(r"^wp-(?P<nn>\d{2})\.yaml$")
_VERSION_RE: Final = re.compile(r"^(?P<base>.+)@v(?P<k>\d+)$")
_OWNER_RE: Final = re.compile(r"^WP-\d{2}$")


class MetricCatalogEntry(MetricDef):
    """TODO(contracts): ``MetricDef`` plus the fields every metric registry entry declares (CHAT_ANALYST §9.7)."""

    short_label: str                 # the label the renderer and the analyst print
    scope: str                       # portfolio, group key, holding key, desk-firewall class or plane
    aliases: tuple[str, ...] = ()    # read by the claim validator's CLAIM_FACT_MISMATCH
    entity_keys: tuple[str, ...] = ()   # the ``by`` dimension keys its instances carry

    def definition(self) -> MetricDef:
        return core_definition(self)


class MetricCatalogFile(RegistryModel):
    """TODO(contracts): one ``config/metrics/wp-NN.yaml`` file (owner = that WP; S-ADR-42)."""

    owner_wp: str
    metrics: tuple[MetricCatalogEntry, ...]

    @field_validator("owner_wp")
    @classmethod
    def _owner(cls, value: str) -> str:
        if not _OWNER_RE.fullmatch(value):
            raise ValueError(f"owner_wp must look like WP-NN, got {value!r}")
        return value


def core_definition(d: MetricDef) -> MetricDef:
    """The ``MetricDef`` fields of ``d`` (drops catalog-only fields of a subclass)."""
    if not isinstance(d, MetricDef):
        raise SchemaError(f"expected a MetricDef, got {type(d).__name__}")
    if type(d) is MetricDef:
        return d
    return MetricDef.model_validate_json(d.model_dump_json(include=set(MetricDef.model_fields)))


def definition_hash(d: MetricDef) -> str:
    """Content hash of the definition's ``MetricDef`` fields (its identity)."""
    return content_hash(core_definition(d))


def by_key(by: Mapping[str, str] | None) -> str:
    """Canonical text of a metric instance's ``by`` dimensions (``{}`` when undimensioned)."""
    items = dict(by or {})
    if all(type(k) is str and type(v) is str for k, v in items.items()):
        # canonical_json of a str -> str mapping, without its generic conversion pass (verify_chain's hot path)
        return json.dumps(items, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return canonical_json(items).decode("utf-8")


def split_version(metric_id: str) -> tuple[str, int]:
    """(``<family>.<name>[.<qualifier>]``, k) of ``...@v<k>``."""
    m = _VERSION_RE.fullmatch(str(metric_id))
    if m is None:
        raise SchemaError(f"metric id {metric_id!r} has no @v<k> version")
    return m.group("base"), int(m.group("k"))


def next_version(metric_id: str, taken: Iterable[str]) -> MetricId:
    """The next free ``@v<k>`` of ``metric_id``'s base name given the ids already ``taken``."""
    base, k = split_version(metric_id)
    versions = [split_version(t)[1] for t in taken if _VERSION_RE.fullmatch(str(t)) and split_version(t)[0] == base]
    return MetricId(f"{base}@v{max([k, *versions]) + 1}")


def metrics_config_root() -> Path:
    """``src/adic_tpa/config/metrics``."""
    return config_root() / "metrics"


def load_metric_catalog(root: Path | None = None) -> dict[MetricId, MetricCatalogEntry]:
    """Merge every ``wp-NN.yaml`` under ``root`` (default ``config/metrics``) with a duplicate-id check.

    Raises ``SchemaError`` for a misnamed file, an ``owner_wp`` that disagrees with the file name, or a metric id
    declared twice (the error names both files). A missing directory is an empty catalog.
    """
    base = Path(root) if root is not None else metrics_config_root()
    if not base.is_dir():
        return {}
    catalog: dict[MetricId, MetricCatalogEntry] = {}
    source: dict[str, str] = {}
    for path in sorted(p for p in base.iterdir() if p.suffix in (".yaml", ".yml")):
        m = METRIC_FILE_RE.fullmatch(path.name)
        if m is None:
            raise SchemaError(f"{path.name}: metric files are named wp-NN.yaml, one per WP (S-ADR-42)",
                              {"path": path.name})
        loaded = load_yaml(path, MetricCatalogFile)
        if loaded.owner_wp != f"WP-{m.group('nn')}":
            raise SchemaError(f"{path.name}: owner_wp {loaded.owner_wp} does not match the file name",
                              {"path": path.name})
        for entry in loaded.metrics:
            if entry.metric_id in catalog:
                raise SchemaError(f"duplicate metric id {entry.metric_id} in {path.name} and {source[entry.metric_id]}",
                                  {"metric_id": str(entry.metric_id), "files": [source[entry.metric_id], path.name]})
            catalog[entry.metric_id] = entry
            source[entry.metric_id] = path.name
    return catalog


def catalog_definitions(catalog: Mapping[MetricId, MetricCatalogEntry]) -> list[MetricDef]:
    """The registry definitions of a catalog, in id order (feed each to ``Registry.define_metric``)."""
    return [catalog[k].definition() for k in sorted(catalog)]
