"""Registry (BUILD_SPEC v1.1 §4.6; owner WP-04): the append-only, hash-chained run / artifact / metric / claim /
decision / ledger store (SQLite in WAL mode plus artifact files under ``runs/``), with the metric registry,
provenance references and the across-contract mFDR table (S-ADR-18).

``registry`` imports only ``contracts`` (§4.0). Modules: ``store`` (``Registry``), ``chain`` (hash rules,
``ChainReport``), ``artifacts`` (artifact files), ``metrics`` (definitions and the ``config/metrics`` catalog),
``provenance`` (``<run_id>:<artifact>:<json-pointer>`` references), ``mfdr`` (``MFDRLedger``) and ``schema.sql``.
"""

from __future__ import annotations

from adic_tpa.registry.artifacts import ArtifactInfo
from adic_tpa.registry.chain import (
    GENESIS_HASH, ChainIssue, ChainReport, chain_record, record_hash, verify_record_chain,
)
from adic_tpa.registry.metrics import MetricCatalogEntry, MetricCatalogFile, load_metric_catalog
from adic_tpa.registry.mfdr import MFDRConfig, MFDRLedger, MFDRRow, MFDRState
from adic_tpa.registry.provenance import artifact_ref, manifest_ref, resolve_pointer
from adic_tpa.registry.store import LEDGER_KINDS, LedgerEntry, LedgerKind, Registry, RunRecord

__all__ = [
    "Registry", "RunRecord", "LedgerEntry", "LedgerKind", "LEDGER_KINDS", "ArtifactInfo", "ChainIssue",
    "ChainReport", "GENESIS_HASH", "chain_record", "record_hash", "verify_record_chain", "MetricCatalogEntry",
    "MetricCatalogFile", "load_metric_catalog", "MFDRLedger", "MFDRConfig", "MFDRRow", "MFDRState", "artifact_ref",
    "manifest_ref", "resolve_pointer",
]
