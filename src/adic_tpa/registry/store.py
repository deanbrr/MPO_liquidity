"""The registry (BUILD_SPEC v1.1 §4.6; owner WP-04): an append-only, hash-chained run / artifact / metric / claim /
decision / ledger store in one SQLite database (WAL mode) plus artifact files under the run directories (§2:
``runs/<run_id>/manifest.json`` and ``runs/<run_id>/artifacts/``; ``runs/`` is git-ignored).

Design (schema in ``schema.sql``; chain rules in ``chain.py``):

- **One chain.** Every write appends rows to ``chain``: the record's canonical-JSON envelope with ``prev_hash`` and
  ``row_hash = sha256(prev_hash ‖ envelope)``. Typed tables (``runs``, ``artifacts``, ``metrics``, ...) only index
  chain rows; reads return records decoded from the chain envelope (``model_validate_json``, S-ADR-39), and
  ``verify_chain`` re-derives every index column, so editing any table, file or row is detected.
- **Append-only.** Triggers raise on UPDATE and DELETE of every table. A writable registry refuses to open a
  database whose triggers were removed (tamper evidence is kept for a read-only ``verify_chain``).
- **One writer at a time.** Writes run in ``BEGIN IMMEDIATE`` transactions under a per-instance lock and a
  cross-process file lock (``<db>.lock``), so concurrent processes (evaluator, lab, analyst) never fork the
  chain; readers are unlimited.
- **Immutability rules.** A run begins once and ends once, and takes artifacts and metrics only while open; an
  artifact name, a metric definition and a metric instance (metric, run, plane, ``by``) are written once; claims
  and decisions are versioned (the latest version wins) and only their audit and outcome fields may change.
- **Read-only handles** (``readonly=True``) refuse every write with ``EntitlementDenied`` except the analyst's
  own ledger kinds (CHAT_ANALYST §9.6, §11).
- **Labels.** Data classes must agree along every edge (parent runs, artifact parents, metrics, decisions):
  SYNTHETIC and REAL never meet (``DataClassMixError``, §1.12); JSON and table artifacts of SYNTHETIC runs carry
  the SYNTHETIC footer.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import sys
import threading
import time
import uuid
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Literal, TypeVar, get_args

from pydantic import BaseModel

from adic_tpa.contracts.analyst import ANALYST_LEDGER_KINDS
from adic_tpa.contracts.arrays import ArrayContainer
from adic_tpa.contracts.claims import ClaimRecord, ProvenanceNode
from adic_tpa.contracts.config import load_json_payload, validate_model
from adic_tpa.contracts.enums import DataClass, EvidencePlane, Plane
from adic_tpa.contracts.errors import (
    DataClassMixError, EntitlementDenied, EvidenceMissing, ExecutionFailed, HashMismatch, SchemaError, UnitError,
)
from adic_tpa.contracts.evidence import MetricDef, MetricInstance, RunManifest
from adic_tpa.contracts.hashing import canonical_json, content_hash
from adic_tpa.contracts.ids import ArtifactRef, MetricId, RunId
from adic_tpa.contracts.room import DecisionRecord
from adic_tpa.registry import artifacts as art
from adic_tpa.registry.artifacts import ArtifactInfo
from adic_tpa.registry.chain import (
    GENESIS_HASH, MAX_ISSUES, ChainIssue, ChainReport, RegistryModel, envelope, record_hash, row_hash,
    split_envelope, verify_links,
)
from adic_tpa.registry.metrics import by_key, core_definition, definition_hash, next_version
from adic_tpa.registry.mfdr import CONFIG_KIND, TEST_KIND, MFDRConfig, MFDRLedger, MFDRTest
from adic_tpa.registry.provenance import MANIFEST_ARTIFACT, artifact_node, parse_ref, resolve_pointer, run_node

if TYPE_CHECKING:
    import pyarrow as pa

if sys.platform == "win32":
    import msvcrt
else:  # pragma: no cover - the reference machine is Windows
    import fcntl

__all__ = [
    "Registry", "RunEnd", "RunRecord", "MetricApproval", "LedgerEntry", "LedgerKind", "LabLedgerKind",
    "AnalystLedgerKind", "LAB_LEDGER_KINDS", "LEDGER_KINDS", "TABLES", "EXPECTED_TRIGGERS", "SCHEMA_VERSION",
    "DEFAULT_DB_PATH", "DEFAULT_ARTIFACT_ROOT",
]

logger = logging.getLogger(__name__)

SCHEMA_VERSION: Final = "1"
# §2 locations, relative to the repository root: the database in stores/, the run directories in runs/.
DEFAULT_DB_PATH: Final = Path("stores") / "registry.sqlite"
DEFAULT_ARTIFACT_ROOT: Final = Path("runs")
LabLedgerKind = Literal["eval_request", "eval_record", "llm_call", "budget", "escalation", "assumption", "seal",
                        "drill"]
AnalystLedgerKind = Literal["chat_session", "chat_turn", "override_draft", "whatif_bundle", "override_confirmation",
                            "whatif_run", "chat_spend", "access_denial", "turn_validation", "decision_link"]
LedgerKind = LabLedgerKind | AnalystLedgerKind
LAB_LEDGER_KINDS: Final[tuple[str, ...]] = get_args(LabLedgerKind)
LEDGER_KINDS: Final[tuple[str, ...]] = LAB_LEDGER_KINDS + tuple(ANALYST_LEDGER_KINDS)
TABLES: Final[tuple[str, ...]] = ("meta", "chain", "runs", "run_ends", "artifacts", "metric_defs", "metric_approvals",
                                  "metrics", "claims", "decisions", "ledger", "mfdr_config", "mfdr_tests")
EXPECTED_TRIGGERS: Final[tuple[str, ...]] = tuple(f"{t}_no_{op}" for t in TABLES for op in ("update", "delete"))
_SCHEMA_SQL: Final = Path(__file__).with_name("schema.sql")
_LEDGER_PREFIX: Final = "ledger."
_LOCK_TIMEOUT_S: Final = 60.0       # operational: how long a writer waits for another process's transaction
_BUSY_TIMEOUT_MS: Final = 60_000
_LOCK_POLL_S: Final = 0.002
# DecisionRecord fields a later version may change (Brier outcomes, signpost states); ClaimRecord audit fields.
_DECISION_MUTABLE: Final = frozenset({"outcomes", "signposts", "prev_hash", "record_hash"})
_CLAIM_MUTABLE: Final = frozenset({"supports_verdict", "auditor_family", "human_countersign"})
_RUN_MANIFEST_CLASS: Final = art.class_path(RunManifest)

M = TypeVar("M", bound=BaseModel)


class RunEnd(RegistryModel):
    """Body of a ``run_end`` chain row."""

    run_id: RunId
    status: Literal["OK", "FAILED", "ABORTED"]
    error: str | None
    canonical_artifact_hashes: dict[str, str]


class RunRecord(RegistryModel):
    """A run as the registry knows it: the manifest (final once ended) and its status."""

    manifest: RunManifest
    status: Literal["STARTED", "OK", "FAILED", "ABORTED"]
    error: str | None


class MetricApproval(RegistryModel):
    """MRM approval of one metric definition (bound to its definition hash)."""

    metric_id: MetricId
    approver: str
    def_hash: str


class LedgerEntry(RegistryModel):
    """One ``append_ledger`` row as read back; ``parse`` validates the payload into its model."""

    seq: int
    kind: str
    payload_class: str | None
    recorded_at: datetime
    row_hash: str
    payload_json: str

    def parse(self, model: type[M]) -> M:
        return load_json_payload(self.payload_json, model)

    @property
    def payload(self) -> Any:
        return json.loads(self.payload_json)


# ------------------------------------------------------------------------------------------------ internals
def _now_iso() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond:06d}Z"


def _connect(path: Path, *, readonly: bool) -> sqlite3.Connection:
    if readonly:
        conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, isolation_level=None,
                               check_same_thread=False)
    else:
        conn = sqlite3.connect(str(path), isolation_level=None, check_same_thread=False)
    conn.execute(f"PRAGMA busy_timeout = {_BUSY_TIMEOUT_MS}")
    conn.execute("PRAGMA foreign_keys = ON")
    if not readonly:
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = FULL")      # an audit store: every commit is durable
    return conn


class _WriterLock:
    """Cross-process exclusive lock on ``<db>.lock``, held only for the length of one write transaction.

    Byte 0 is the lock; byte 1 is a turnstile a waiter holds while it polls byte 0, so a writer that has just
    released cannot take the lock straight back and starve the other processes (handoff, not barging).
    """

    _MAIN: Final = 0
    _TURNSTILE: Final = 1

    def __init__(self, path: Path) -> None:
        self._path = path
        self._fd: int | None = None

    def __enter__(self) -> _WriterLock:
        if self._fd is None:
            self._fd = os.open(self._path, os.O_RDWR | os.O_CREAT, 0o644)
        deadline = time.monotonic() + _LOCK_TIMEOUT_S
        self._poll(self._fd, self._TURNSTILE, deadline)
        try:
            self._poll(self._fd, self._MAIN, deadline)
        finally:
            self._release(self._fd, self._TURNSTILE)
        return self

    def __exit__(self, *exc: object) -> None:
        assert self._fd is not None
        self._release(self._fd, self._MAIN)

    def _poll(self, fd: int, offset: int, deadline: float) -> None:
        while True:
            try:
                self._acquire(fd, offset)
                return
            except OSError:
                if time.monotonic() >= deadline:
                    raise ExecutionFailed("registry writer lock is busy", {"lock": str(self._path)}) from None
                time.sleep(_LOCK_POLL_S)

    @staticmethod
    def _acquire(fd: int, offset: int) -> None:
        if sys.platform == "win32":
            os.lseek(fd, offset, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        else:  # pragma: no cover
            fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 1, offset)

    @staticmethod
    def _release(fd: int, offset: int) -> None:
        if sys.platform == "win32":
            os.lseek(fd, offset, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        else:  # pragma: no cover
            fcntl.lockf(fd, fcntl.LOCK_UN, 1, offset)

    def close(self) -> None:
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None


class _Writer:
    """Appends chain rows (and their index rows) inside one write transaction."""

    __slots__ = ("conn", "recorded_at", "seq", "head")

    def __init__(self, conn: sqlite3.Connection, recorded_at: str, seq: int, head: str) -> None:
        self.conn, self.recorded_at, self.seq, self.head = conn, recorded_at, seq, head

    def append(self, kind: str, body_text: str, *, cls: str | None, table: str, columns: Mapping[str, object]) -> str:
        payload = envelope(kind, body_text, cls=cls, recorded_at=self.recorded_at)
        seq, digest = self.seq + 1, row_hash(self.head, payload)
        self.conn.execute("INSERT INTO chain (seq, kind, payload, prev_hash, row_hash) VALUES (?, ?, ?, ?, ?)",
                          (seq, kind, payload, self.head, digest))
        names = ", ".join(("seq", *columns))
        marks = ", ".join("?" * (len(columns) + 1))
        self.conn.execute(f"INSERT INTO {table} ({names}) VALUES ({marks})", (seq, *columns.values()))
        self.seq, self.head = seq, digest
        return digest


@dataclass(frozen=True, slots=True)
class _IndexSpec:
    """How a typed table's columns derive from its chain rows (for verify_chain)."""

    table: str
    kinds: tuple[str, ...]          # exact chain kinds; empty with prefix set for the ledger
    columns: tuple[str, ...]
    derive: Callable[[str, dict[str, Any]], tuple[object, ...]]
    prefix: str | None = None


def _ledger_cols(kind: str, body: dict[str, Any]) -> tuple[object, ...]:
    sub = kind[len(_LEDGER_PREFIX):]
    if sub not in LEDGER_KINDS:
        raise ValueError(f"unknown ledger kind {sub!r}")
    return (sub,)


_INDEX: Final[tuple[_IndexSpec, ...]] = (
    _IndexSpec("runs", ("run",), ("run_id", "kind"), lambda k, b: (b["run_id"], b["kind"])),
    _IndexSpec("run_ends", ("run_end",), ("run_id", "status"), lambda k, b: (b["run_id"], b["status"])),
    _IndexSpec("artifacts", ("artifact",), ("run_id", "name"), lambda k, b: (b["run_id"], b["name"])),
    _IndexSpec("metric_defs", ("metric_def",), ("metric_id", "def_hash"), lambda k, b: (b["metric_id"], content_hash(b))),
    _IndexSpec("metric_approvals", ("metric_approval",), ("metric_id",), lambda k, b: (b["metric_id"],)),
    _IndexSpec("metrics", ("metric",), ("metric_id", "run_id", "plane", "by_key"),
               lambda k, b: (b["metric_id"], b["run_id"], b["plane"], by_key(b["by"]))),
    _IndexSpec("claims", ("claim",), ("claim_id", "doc_id"), lambda k, b: (b["claim_id"], b["doc_id"])),
    _IndexSpec("decisions", ("decision",), ("decision_id", "record_hash"),
               lambda k, b: (b["decision_id"], b["record_hash"])),
    _IndexSpec("ledger", (), ("kind",), _ledger_cols, prefix=_LEDGER_PREFIX),
    _IndexSpec("mfdr_config", (CONFIG_KIND,), ("one",), lambda k, b: (1,)),
    _IndexSpec("mfdr_tests", (TEST_KIND,), ("contract_id",), lambda k, b: (b["contract_id"],)),
)
_KNOWN_KINDS: Final = frozenset(k for spec in _INDEX for k in spec.kinds)


def _body(payload: str, model: type[M]) -> M:
    return load_json_payload(split_envelope(payload)[0], model)


def _strip(record: BaseModel, mutable: frozenset[str]) -> dict[str, Any]:
    return record.model_dump(mode="json", exclude=set(mutable))


# --------------------------------------------------------------------------------------------------- registry
class Registry:
    """Append-only, hash-chained registry (§4.6). Use as a context manager or call ``close()``."""

    def __init__(self, db_path: Path, artifact_root: Path, *, readonly: bool = False) -> None:
        self._db_path = Path(db_path)
        self._artifact_root = Path(artifact_root)
        self._readonly = readonly
        self._closed = False
        self._lock = threading.RLock()
        self._writer_lock = _WriterLock(self._db_path.with_name(self._db_path.name + ".lock"))
        self._rw: sqlite3.Connection | None = None
        if readonly and not self._db_path.is_file():
            raise EvidenceMissing(f"registry database {self._db_path} does not exist", {"db": str(self._db_path)})
        if not readonly:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ro = _connect(self._db_path, readonly=readonly)
        try:
            if readonly:
                self._check_schema(self._ro, require_triggers=False)
            else:
                self._rw = self._ro
                self._create_or_check()
        except BaseException:
            self.close()
            raise
        logger.debug("registry.open", extra={"db": self._db_path.name, "readonly": readonly})

    # -- lifecycle ------------------------------------------------------------------------------------------
    def close(self) -> None:
        with self._lock:
            for conn in {id(c): c for c in (self._ro, self._rw) if c is not None}.values():
                conn.close()
            self._rw = None
            self._closed = True
            self._writer_lock.close()

    def __enter__(self) -> Registry:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @property
    def readonly(self) -> bool:
        return self._readonly

    @property
    def db_path(self) -> Path:
        return self._db_path

    @property
    def artifact_root(self) -> Path:
        return self._artifact_root

    def run_dir(self, run_id: RunId | str) -> Path:
        """``<artifact_root>/<run_id>`` (§2: manifest.json, artifacts/, logs/, pack/)."""
        return self._artifact_root / str(RunId(str(run_id)))

    def log_path(self, run_id: RunId | str, stream: str) -> Path:
        """``runs/<run_id>/logs/<stream>.jsonl`` with its directory created (§1.9; for ``contracts.logjson``)."""
        art.check_name(stream)
        directory = self.run_dir(run_id) / "logs"
        directory.mkdir(parents=True, exist_ok=True)
        return directory / f"{stream}.jsonl"

    def _create_or_check(self) -> None:
        conn = self._rw
        assert conn is not None
        with self._lock, self._writer_lock:
            tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            if "meta" not in tables:
                if tables:
                    raise SchemaError(f"{self._db_path} is not a registry database", {"tables": sorted(tables)})
                conn.executescript("BEGIN IMMEDIATE;\n" + _SCHEMA_SQL.read_text(encoding="utf-8") + "\n"
                                   f"INSERT INTO meta (key, value) VALUES ('schema_version', '{SCHEMA_VERSION}');\n"
                                   f"INSERT INTO meta (key, value) VALUES ('created_at', '{_now_iso()}');\n"
                                   "COMMIT;")
        self._check_schema(conn, require_triggers=True)

    def _check_schema(self, conn: sqlite3.Connection, *, require_triggers: bool) -> None:
        with self._lock:
            try:
                row = conn.execute("SELECT value FROM meta WHERE key = 'schema_version'").fetchone()
            except sqlite3.DatabaseError as exc:
                raise SchemaError(f"{self._db_path} is not a registry database ({exc})") from exc
            if row is None or row[0] != SCHEMA_VERSION:
                raise SchemaError(f"registry schema version {row[0] if row else None} != {SCHEMA_VERSION}")
            if require_triggers:
                missing = self._missing_triggers(conn)
                if missing:
                    raise HashMismatch("registry append-only triggers are missing (tampered?); open it with "
                                       "readonly=True and run verify_chain", {"missing": missing})

    @staticmethod
    def _missing_triggers(conn: sqlite3.Connection) -> list[str]:
        present = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'")}
        return [t for t in EXPECTED_TRIGGERS if t not in present]

    # -- write plumbing ---------------------------------------------------------------------------------------
    def _check_write_allowed(self, ledger_kind: str | None = None) -> None:
        if self._readonly and ledger_kind not in ANALYST_LEDGER_KINDS:
            raise EntitlementDenied("this registry handle is read-only: only the analyst's own ledger kinds may be "
                                    "appended (CHAT_ANALYST §9.6)", {"rule": "REGISTRY_READONLY",
                                                                     "ledger_kind": ledger_kind})

    def _write_conn(self, ledger_kind: str | None) -> sqlite3.Connection:
        self._check_write_allowed(ledger_kind)
        if self._closed:
            raise ExecutionFailed("this registry handle is closed", {"db": str(self._db_path)})
        if self._rw is None:   # a read-only handle appending an analyst ledger kind
            conn = _connect(self._db_path, readonly=False)
            if self._missing_triggers(conn):
                conn.close()
                raise HashMismatch("registry append-only triggers are missing (tampered?)")
            self._rw = conn
        return self._rw

    @contextmanager
    def _transaction(self, *, ledger_kind: str | None = None) -> Iterator[_Writer]:
        with self._lock:
            conn = self._write_conn(ledger_kind)
            with self._writer_lock:
                conn.execute("BEGIN IMMEDIATE")
                try:
                    head = conn.execute("SELECT seq, row_hash FROM chain ORDER BY seq DESC LIMIT 1").fetchone()
                    yield _Writer(conn, _now_iso(), *(head or (0, GENESIS_HASH)))
                    conn.execute("COMMIT")
                except BaseException:
                    if conn.in_transaction:
                        conn.execute("ROLLBACK")
                    raise

    def _reader(self) -> sqlite3.Connection:
        if self._closed:
            raise ExecutionFailed("this registry handle is closed", {"db": str(self._db_path)})
        return self._ro

    def _query(self, sql: str, params: Sequence[object] = ()) -> list[tuple[Any, ...]]:
        with self._lock:
            return self._reader().execute(sql, tuple(params)).fetchall()

    # -- runs -----------------------------------------------------------------------------------------------
    def _begin_manifest(self, conn: sqlite3.Connection, run_id: str) -> RunManifest | None:
        row = conn.execute("SELECT c.payload FROM runs r JOIN chain c ON c.seq = r.seq WHERE r.run_id = ?",
                           (str(run_id),)).fetchone()
        return _body(row[0], RunManifest) if row else None

    def _run_end(self, conn: sqlite3.Connection, run_id: str) -> RunEnd | None:
        row = conn.execute("SELECT c.payload FROM run_ends e JOIN chain c ON c.seq = e.seq WHERE e.run_id = ?",
                           (str(run_id),)).fetchone()
        return _body(row[0], RunEnd) if row else None

    def _open_run(self, conn: sqlite3.Connection, run_id: str) -> RunManifest:
        manifest = self._begin_manifest(conn, run_id)
        if manifest is None:
            raise SchemaError(f"unknown run {run_id}: begin_run first", {"run_id": str(run_id)})
        if self._run_end(conn, run_id) is not None:
            raise SchemaError(f"run {run_id} has ended; its artifacts and metrics are closed", {"run_id": str(run_id)})
        return manifest

    def begin_run(self, manifest: RunManifest) -> RunId:
        """Register a run (status STARTED) and write ``runs/<run_id>/manifest.json``.

        Parent runs must be registered and share the run's data class (taint, §1.12).
        """
        self._check_write_allowed()
        if not isinstance(manifest, RunManifest):
            raise SchemaError(f"begin_run expects a RunManifest, got {type(manifest).__name__}")
        if manifest.status != "STARTED":
            raise SchemaError(f"a run begins with status STARTED, got {manifest.status}", {"run_id": str(manifest.run_id)})
        body = canonical_json(manifest).decode("utf-8")
        with self._transaction() as w:
            if self._begin_manifest(w.conn, manifest.run_id) is not None:
                raise SchemaError(f"run {manifest.run_id} is already registered", {"run_id": str(manifest.run_id)})
            for parent in manifest.parent_runs:
                pm = self._begin_manifest(w.conn, parent)
                if pm is None:
                    raise SchemaError(f"unknown parent run {parent}", {"run_id": str(manifest.run_id)})
                if pm.data_class != manifest.data_class:
                    raise DataClassMixError(f"run {manifest.run_id} ({manifest.data_class.value}) derives from "
                                            f"{parent} ({pm.data_class.value})", {"run_id": str(manifest.run_id)})
            w.append("run", body, cls=_RUN_MANIFEST_CLASS, table="runs",
                     columns={"run_id": str(manifest.run_id), "kind": manifest.kind})
        self._write_manifest_file(manifest)
        logger.info("registry.run_begun", extra={"run_id": str(manifest.run_id), "plane": manifest.plane.value})
        return manifest.run_id

    def end_run(self, run_id: RunId, status: Literal["OK", "FAILED", "ABORTED"], error: str | None = None) -> None:
        """Close a run once; fills the manifest's status and ``canonical_artifact_hashes`` (§9.4 #9)."""
        self._check_write_allowed()
        if status not in ("OK", "FAILED", "ABORTED"):
            raise SchemaError(f"end_run status must be OK, FAILED or ABORTED, got {status!r}")
        rid = RunId(str(run_id))
        with self._transaction() as w:
            manifest = self._open_run(w.conn, rid)
            hashes = {i.name: i.canonical_hash for i in self._artifact_infos(w.conn, rid)}
            end = RunEnd(run_id=rid, status=status, error=error, canonical_artifact_hashes=hashes)
            w.append("run_end", canonical_json(end).decode("utf-8"), cls=art.class_path(RunEnd), table="run_ends",
                     columns={"run_id": str(rid), "status": status})
        self._write_manifest_file(self._final_manifest(manifest, end))
        logger.info("registry.run_ended", extra={"run_id": str(rid), "status": status})

    @staticmethod
    def _final_manifest(begin: RunManifest, end: RunEnd | None) -> RunManifest:
        if end is None:
            return begin
        data = begin.model_dump(mode="python")
        data["status"] = end.status
        data["canonical_artifact_hashes"] = {**begin.canonical_artifact_hashes, **end.canonical_artifact_hashes}
        return validate_model(RunManifest, data)

    def _write_manifest_file(self, manifest: RunManifest) -> None:
        run_dir = self.run_dir(manifest.run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        tmp = run_dir / f".manifest-{uuid.uuid4().hex}.tmp"
        tmp.write_bytes(canonical_json(manifest))
        os.replace(tmp, run_dir / "manifest.json")

    def get_run(self, run_id: RunId | str) -> RunRecord:
        with self._lock:
            begin = self._begin_manifest(self._reader(), str(run_id))
            if begin is None:
                raise EvidenceMissing(f"unknown run {run_id}", {"run_id": str(run_id)})
            end = self._run_end(self._reader(), str(run_id))
        return RunRecord(manifest=self._final_manifest(begin, end), status=end.status if end else "STARTED",
                         error=end.error if end else None)

    def get_manifest(self, run_id: RunId | str) -> RunManifest:
        """The run's manifest: as begun, or with the final status and artifact hashes once ended."""
        return self.get_run(run_id).manifest

    def list_runs(self, *, kind: str | None = None) -> list[RunRecord]:
        sql, params = "SELECT run_id FROM runs", ()
        if kind is not None:
            sql, params = sql + " WHERE kind = ?", (kind,)
        return [self.get_run(r[0]) for r in self._query(sql + " ORDER BY seq", params)]

    # -- artifacts ------------------------------------------------------------------------------------------
    def _artifact_info(self, conn: sqlite3.Connection, run_id: str, name: str) -> ArtifactInfo | None:
        row = conn.execute("SELECT c.payload FROM artifacts a JOIN chain c ON c.seq = a.seq "
                           "WHERE a.run_id = ? AND a.name = ?", (str(run_id), name)).fetchone()
        return _body(row[0], ArtifactInfo) if row else None

    @staticmethod
    def _check_name_free(conn: sqlite3.Connection, run_id: str, name: str) -> None:
        row = conn.execute("SELECT name FROM artifacts WHERE run_id = ? AND lower(name) = lower(?)",
                           (str(run_id), name)).fetchone()
        if row is not None:
            raise SchemaError(f"artifact {run_id}:{row[0]} already exists (names are unique case-blind); artifacts "
                              "are written once", {"ref": f"{run_id}:{row[0]}:"})

    def _artifact_infos(self, conn: sqlite3.Connection, run_id: str) -> list[ArtifactInfo]:
        rows = conn.execute("SELECT c.payload FROM artifacts a JOIN chain c ON c.seq = a.seq WHERE a.run_id = ? "
                            "ORDER BY a.seq", (str(run_id),)).fetchall()
        return [_body(r[0], ArtifactInfo) for r in rows]

    def _check_parents(self, conn: sqlite3.Connection, parents: Sequence[ArtifactRef], data_class: DataClass,
                       child: str) -> None:
        for ref in parents:
            if ref.artifact == MANIFEST_ARTIFACT:
                pm = self._begin_manifest(conn, ref.run_id)
                parent_class = pm.data_class if pm is not None else None
            else:
                info = self._artifact_info(conn, ref.run_id, ref.artifact)
                parent_class = info.data_class if info is not None else None
            if parent_class is None:
                raise EvidenceMissing(f"{child}: parent {ref} is not registered", {"parent": str(ref)})
            if parent_class != data_class:
                raise DataClassMixError(f"{child} ({data_class.value}) cannot derive from {ref} "
                                        f"({parent_class.value})", {"parent": str(ref)})

    def put_artifact(self, run_id: RunId, name: str, obj: BaseModel | ArrayContainer | pa.Table | bytes, *,
                     kind: str | None = None, parents: Sequence[ArtifactRef | str] = ()) -> ArtifactRef:
        """Store ``obj`` (Pydantic model, ArrayContainer, pyarrow Table or bytes) once under ``name``.

        ``parents`` are the artifact (or ``<run_id>:manifest:``) references it derives from (provenance);
        ``kind`` labels its provenance node. Returns ``<run_id>:<name>:``.
        """
        self._check_write_allowed()
        rid = RunId(str(run_id))
        art.check_name(name)
        parent_refs = tuple(dict.fromkeys(parse_ref(p) for p in parents))
        with self._lock:                   # fail fast before serializing; re-checked inside the write transaction
            manifest = self._open_run(self._reader(), rid)
            self._check_name_free(self._reader(), rid, name)
        directory = self.run_dir(rid) / "artifacts"
        directory.mkdir(parents=True, exist_ok=True)
        tmp = directory / f".tmp-{uuid.uuid4().hex}"
        moved: Path | None = None
        try:
            enc = art.write_artifact(obj, tmp, name=name, data_class=manifest.data_class)
            final = directory / f"{name}{art.EXTENSIONS[enc.format]}"
            info = ArtifactInfo(run_id=rid, name=name, format=enc.format, class_path=enc.class_path,
                                kind=kind or enc.default_kind,
                                rel_path=final.relative_to(self._artifact_root).as_posix(), checksum=enc.checksum,
                                canonical_hash=enc.canonical_hash, file_sha256=art.file_sha256(tmp),
                                nbytes=tmp.stat().st_size, parents=parent_refs, data_class=manifest.data_class)
            with self._transaction() as w:
                self._open_run(w.conn, rid)
                self._check_name_free(w.conn, rid, name)
                self._check_parents(w.conn, parent_refs, manifest.data_class, f"{rid}:{name}")
                w.append("artifact", canonical_json(info).decode("utf-8"), cls=art.class_path(ArtifactInfo),
                         table="artifacts", columns={"run_id": str(rid), "name": name})
                os.replace(tmp, final)
                moved = final
        except BaseException:
            tmp.unlink(missing_ok=True)
            if moved is not None and self._artifact_row_missing(rid, name):
                moved.unlink(missing_ok=True)      # the commit failed after the file was put in place
            raise
        return info.ref

    def _artifact_row_missing(self, run_id: str, name: str) -> bool:
        with self._lock:
            return self._artifact_info(self._reader(), run_id, name) is None

    def get_artifact(self, ref: ArtifactRef | str, *, model: type | None = None) -> Any:
        """Load an artifact and resolve the reference's JSON pointer inside it.

        A model whose class is outside ``adic_tpa.contracts`` comes back as its JSON body unless ``model`` names
        the class (containers outside contracts need ``model``). ``<run_id>:manifest:<pointer>`` reads the run's
        manifest. Raises ``EvidenceMissing`` when the reference does not resolve and ``HashMismatch`` when the
        file is missing or altered.
        """
        r = parse_ref(ref)
        if r.artifact == MANIFEST_ARTIFACT:
            manifest = self.get_manifest(r.run_id)
            return resolve_pointer(manifest, r.pointer, where=str(r)) if r.pointer else manifest
        with self._lock:
            info = self._artifact_info(self._reader(), r.run_id, r.artifact)
        if info is None:
            raise EvidenceMissing(f"artifact {r.run_id}:{r.artifact} is not registered", {"ref": str(r)})
        path = self._artifact_file(info)
        art.verify_file(path, info)
        return art.read_artifact(path, info, pointer=r.pointer, model=model)

    def _artifact_file(self, info: ArtifactInfo) -> Path:
        """The artifact's file, refusing a registered path other than ``<run_id>/artifacts/<name><ext>``."""
        expected = f"{info.run_id}/artifacts/{info.name}{art.EXTENSIONS[info.format]}"
        if info.rel_path != expected:
            raise HashMismatch(f"{info.ref}: registered path {info.rel_path!r} is not {expected!r}",
                               {"ref": str(info.ref)})
        return self._artifact_root / expected

    def artifact_info(self, ref: ArtifactRef | str) -> ArtifactInfo:
        r = parse_ref(ref)
        with self._lock:
            info = self._artifact_info(self._reader(), r.run_id, r.artifact)
        if info is None:
            raise EvidenceMissing(f"artifact {r.run_id}:{r.artifact} is not registered", {"ref": str(r)})
        return info

    def artifact_path(self, ref: ArtifactRef | str) -> Path:
        """The verified file of an artifact."""
        info = self.artifact_info(ref)
        path = self._artifact_file(info)
        art.verify_file(path, info)
        return path

    def list_artifacts(self, run_id: RunId | str) -> list[ArtifactInfo]:
        with self._lock:
            return self._artifact_infos(self._reader(), str(run_id))

    # -- metrics --------------------------------------------------------------------------------------------
    def _metric_def(self, conn: sqlite3.Connection, metric_id: str) -> tuple[MetricDef, str] | None:
        row = conn.execute("SELECT c.payload, d.def_hash FROM metric_defs d JOIN chain c ON c.seq = d.seq "
                           "WHERE d.metric_id = ?", (str(metric_id),)).fetchone()
        return (_body(row[0], MetricDef), row[1]) if row else None

    def define_metric(self, d: MetricDef) -> None:
        """Register a definition; identical repeats are no-ops, and any change needs a new metric id (ARCH §10.3).

        The MRM approval flag is a separate row (``approve_metric``).
        """
        self._check_write_allowed()
        core = core_definition(d)
        digest = definition_hash(core)
        with self._lock:
            known = self._metric_def(self._reader(), core.metric_id)
        if known is not None and known[1] == digest:
            return
        with self._transaction() as w:
            known = self._metric_def(w.conn, core.metric_id)
            if known is not None:
                if known[1] == digest:
                    return
                taken = [r[0] for r in w.conn.execute("SELECT metric_id FROM metric_defs")]
                suggestion = next_version(core.metric_id, taken)
                raise SchemaError(f"metric {core.metric_id} is already defined differently; a definition change "
                                  f"needs a new metric id, e.g. {suggestion} (ARCH §10.3)",
                                  {"metric_id": str(core.metric_id), "suggested": str(suggestion)})
            w.append("metric_def", canonical_json(core).decode("utf-8"), cls=art.class_path(MetricDef),
                     table="metric_defs", columns={"metric_id": str(core.metric_id), "def_hash": digest})

    def approve_metric(self, metric_id: MetricId | str, *, approver: str) -> None:
        """Record MRM approval of the current definition of ``metric_id``."""
        self._check_write_allowed()
        with self._transaction() as w:
            known = self._metric_def(w.conn, str(metric_id))
            if known is None:
                raise SchemaError(f"cannot approve undefined metric {metric_id}", {"metric_id": str(metric_id)})
            body = MetricApproval(metric_id=known[0].metric_id, approver=approver, def_hash=known[1])
            w.append("metric_approval", canonical_json(body).decode("utf-8"), cls=art.class_path(MetricApproval),
                     table="metric_approvals", columns={"metric_id": str(metric_id)})

    def is_metric_approved(self, metric_id: MetricId | str) -> bool:
        return bool(self._query("SELECT 1 FROM metric_approvals WHERE metric_id = ? LIMIT 1", (str(metric_id),)))

    def get_metric_def(self, metric_id: MetricId | str) -> MetricDef:
        with self._lock:
            known = self._metric_def(self._reader(), str(metric_id))
        if known is None:
            raise EvidenceMissing(f"metric {metric_id} is not defined", {"metric_id": str(metric_id)})
        return known[0]

    def list_metric_defs(self, *, prefix: str | None = None) -> list[MetricDef]:
        sql, params = "SELECT c.payload FROM metric_defs d JOIN chain c ON c.seq = d.seq", ()
        if prefix:
            sql, params = sql + " WHERE d.metric_id >= ? AND d.metric_id < ?", (prefix, prefix + "\U0010ffff")
        return [_body(r[0], MetricDef) for r in self._query(sql + " ORDER BY d.metric_id", params)]

    def put_metrics(self, ms: Sequence[MetricInstance]) -> None:
        """Append metric instances, all or none.

        Each needs a defined metric with the same unit (``UnitError``), an open run with the same data class
        (``DataClassMixError``), and a key (metric, run, plane, ``by``) never written before; SEALED instances
        come only from FINAL-plane runs.
        """
        self._check_write_allowed()
        items = list(ms)
        if not items:
            return
        prepared: list[tuple[MetricInstance, str, str]] = []
        seen: set[tuple[str, str, str, str]] = set()
        for m in items:
            if not isinstance(m, MetricInstance):
                raise SchemaError(f"put_metrics expects MetricInstance objects, got {type(m).__name__}")
            key = by_key(m.by)
            ident = (str(m.metric_id), str(m.run_id), m.plane.value, key)
            if ident in seen:
                raise SchemaError(f"metric instance {ident} appears twice in the batch", {"metric_id": str(m.metric_id)})
            seen.add(ident)
            prepared.append((m, key, canonical_json(m).decode("utf-8")))
        with self._transaction() as w:
            defs: dict[str, MetricDef] = {}
            for mid in {str(m.metric_id) for m, _, _ in prepared}:
                known = self._metric_def(w.conn, mid)
                if known is None:
                    raise SchemaError(f"metric {mid} is not defined (define_metric first)", {"metric_id": mid})
                defs[mid] = known[0]
            runs = {rid: self._open_run(w.conn, rid) for rid in {str(m.run_id) for m, _, _ in prepared}}
            cls = art.class_path(MetricInstance)
            for m, key, body in prepared:
                definition, run = defs[str(m.metric_id)], runs[str(m.run_id)]
                if m.unit != definition.unit:
                    raise UnitError(f"metric {m.metric_id}: unit {m.unit!r} != defined unit {definition.unit!r}",
                                    {"metric_id": str(m.metric_id)})
                if m.data_class != run.data_class:
                    raise DataClassMixError(f"metric {m.metric_id} is {m.data_class.value} but run {m.run_id} is "
                                            f"{run.data_class.value}", {"metric_id": str(m.metric_id)})
                if m.plane == EvidencePlane.SEALED and run.plane != Plane.FINAL:
                    raise SchemaError(f"metric {m.metric_id}: SEALED evidence needs a FINAL-plane run, run "
                                      f"{m.run_id} is {run.plane.value}", {"metric_id": str(m.metric_id)})
                try:
                    w.append("metric", body, cls=cls, table="metrics",
                             columns={"metric_id": str(m.metric_id), "run_id": str(m.run_id),
                                      "plane": m.plane.value, "by_key": key})
                except sqlite3.IntegrityError as exc:
                    raise SchemaError(f"metric instance ({m.metric_id}, {m.run_id}, {m.plane.value}, {key}) is "
                                      "already registered; instances are written once",
                                      {"metric_id": str(m.metric_id)}) from exc

    def get_metric(self, metric_id: MetricId, *, run_id: RunId | None = None, plane: EvidencePlane | None = None,
                   by: Mapping[str, str] | None = None) -> MetricInstance:
        """The latest instance with exactly these ``by`` dimensions (none when ``by`` is None) and the given run
        and plane if set; ``EvidenceMissing`` when there is none (e.g. "EVIDENCE MISSING: <metric>")."""
        key = by_key(by)
        sql = ("SELECT c.payload FROM metrics m JOIN chain c ON c.seq = m.seq WHERE m.metric_id = ? AND m.by_key = ?")
        params: list[object] = [str(metric_id), key]
        if run_id is not None:
            sql += " AND m.run_id = ?"
            params.append(str(run_id))
        if plane is not None:
            sql += " AND m.plane = ?"
            params.append(EvidencePlane(plane).value)
        rows = self._query(sql + " ORDER BY m.seq DESC LIMIT 1", params)
        if not rows:
            raise EvidenceMissing(f"EVIDENCE MISSING: {metric_id}", {
                "metric_id": str(metric_id), "by": dict(by or {}), "run_id": None if run_id is None else str(run_id),
                "plane": None if plane is None else EvidencePlane(plane).value})
        inst = _body(rows[0][0], MetricInstance)
        if inst.metric_id != metric_id or by_key(inst.by) != key or (run_id is not None and inst.run_id != run_id):
            raise HashMismatch(f"metric index disagrees with its chain row for {metric_id} (tampered?)",
                               {"metric_id": str(metric_id)})
        return inst

    def list_metrics(self, *, run_id: RunId | None = None, prefix: str | None = None) -> list[MetricInstance]:
        sql = "SELECT c.payload FROM metrics m JOIN chain c ON c.seq = m.seq WHERE 1 = 1"
        params: list[object] = []
        if run_id is not None:
            sql += " AND m.run_id = ?"
            params.append(str(run_id))
        if prefix:
            sql += " AND m.metric_id >= ? AND m.metric_id < ?"
            params += [prefix, prefix + "\U0010ffff"]
        return [_body(r[0], MetricInstance) for r in self._query(sql + " ORDER BY m.seq", params)]

    # -- ledger ---------------------------------------------------------------------------------------------
    def append_ledger(self, kind: LedgerKind, payload: BaseModel) -> str:
        """Append a ledger row (§7.8 kinds, plus the analyst's kinds of CHAT_ANALYST §11); returns its row hash."""
        if kind not in LEDGER_KINDS:
            raise SchemaError(f"unknown ledger kind {kind!r}", {"kinds": list(LEDGER_KINDS)})
        self._check_write_allowed(kind)
        if not isinstance(payload, BaseModel):
            raise SchemaError(f"ledger payloads are Pydantic models, got {type(payload).__name__}")
        body = canonical_json(payload).decode("utf-8")
        with self._transaction(ledger_kind=kind) as w:
            return w.append(_LEDGER_PREFIX + kind, body, cls=art.class_path(type(payload)), table="ledger",
                            columns={"kind": kind})

    def read_ledger(self, kind: LedgerKind | None = None, *, after_seq: int = 0,
                    limit: int | None = None) -> list[LedgerEntry]:
        """Ledger rows in append order (FSM state, budgets and escalations are rebuilt from them)."""
        sql = ("SELECT c.seq, l.kind, c.payload, c.row_hash FROM ledger l JOIN chain c ON c.seq = l.seq "
               "WHERE l.seq > ?")
        params: list[object] = [after_seq]
        if kind is not None:
            sql += " AND l.kind = ?"
            params.append(kind)
        sql += " ORDER BY l.seq"
        if limit is not None:
            sql += " LIMIT ?"
            params.append(int(limit))
        out = []
        for seq, sub, payload, digest in self._query(sql, params):
            body, header = split_envelope(payload)
            out.append(LedgerEntry(seq=seq, kind=sub, payload_class=header["class"],
                                   recorded_at=datetime.fromisoformat(header["recorded_at"]), row_hash=digest,
                                   payload_json=body))
        return out

    # -- claims ---------------------------------------------------------------------------------------------
    def _latest(self, conn: sqlite3.Connection, table: str, column: str, value: str, model: type[M]) -> M | None:
        row = conn.execute(f"SELECT c.payload FROM {table} t JOIN chain c ON c.seq = t.seq WHERE t.{column} = ? "
                           "ORDER BY t.seq DESC LIMIT 1", (value,)).fetchone()
        return _body(row[0], model) if row else None

    def put_claim(self, c: ClaimRecord) -> None:
        """Append a claim, or a new version of it in which only the audit fields (verdict, auditor family, human
        countersignature) changed; an identical repeat is a no-op."""
        self._check_write_allowed()
        if not isinstance(c, ClaimRecord):
            raise SchemaError(f"put_claim expects a ClaimRecord, got {type(c).__name__}")
        with self._transaction() as w:
            prev = self._latest(w.conn, "claims", "claim_id", c.claim_id, ClaimRecord)
            if prev is not None:
                if prev == c:
                    return
                if _strip(prev, _CLAIM_MUTABLE) != _strip(c, _CLAIM_MUTABLE):
                    raise SchemaError(f"claim {c.claim_id}: only its audit fields may change in a new version",
                                      {"claim_id": c.claim_id})
            w.append("claim", canonical_json(c).decode("utf-8"), cls=art.class_path(ClaimRecord), table="claims",
                     columns={"claim_id": c.claim_id, "doc_id": c.doc_id})

    def get_claim(self, claim_id: str) -> ClaimRecord:
        with self._lock:
            claim = self._latest(self._reader(), "claims", "claim_id", claim_id, ClaimRecord)
        if claim is None:
            raise EvidenceMissing(f"claim {claim_id} is not registered", {"claim_id": claim_id})
        return claim

    def list_claims(self, *, doc_id: str | None = None) -> list[ClaimRecord]:
        """The latest version of each claim (of one document if ``doc_id``), in order of first registration."""
        sql = "SELECT t.claim_id, c.payload FROM claims t JOIN chain c ON c.seq = t.seq"
        params: tuple[object, ...] = ()
        if doc_id is not None:
            sql, params = sql + " WHERE t.doc_id = ?", (doc_id,)
        latest: dict[str, str] = {}
        for claim_id, payload in self._query(sql + " ORDER BY t.seq", params):
            latest[claim_id] = payload        # dict keeps first-insertion order, later versions overwrite
        return [_body(p, ClaimRecord) for p in latest.values()]

    # -- decisions ------------------------------------------------------------------------------------------
    def decision_head(self) -> str:
        """``record_hash`` of the last decision record (``GENESIS_HASH`` before the first); the next record's
        ``prev_hash`` (build it with ``registry.chain.chain_record``)."""
        rows = self._query("SELECT record_hash FROM decisions ORDER BY seq DESC LIMIT 1")
        return rows[0][0] if rows else GENESIS_HASH

    def append_decision(self, d: DecisionRecord) -> None:
        """Append a decision record to the decision chain (§4.6, ARCH §8.9).

        ``prev_hash`` must equal ``decision_head()`` and ``record_hash`` must equal ``chain.record_hash(d)``
        (``HashMismatch`` otherwise). A later version of the same decision may change only ``outcomes`` and
        ``signposts`` (Brier scores, signpost states). Its runs must be registered and share its data class.
        """
        self._check_write_allowed()
        if not isinstance(d, DecisionRecord):
            raise SchemaError(f"append_decision expects a DecisionRecord, got {type(d).__name__}")
        with self._transaction() as w:
            row = w.conn.execute("SELECT record_hash FROM decisions ORDER BY seq DESC LIMIT 1").fetchone()
            head = row[0] if row else GENESIS_HASH
            if d.prev_hash != head:
                raise HashMismatch(f"decision chain broken: {d.decision_id} prev_hash {d.prev_hash} != head {head}",
                                   {"decision_id": str(d.decision_id), "head": head})
            expected = record_hash(d)
            if d.record_hash != expected:
                raise HashMismatch(f"decision {d.decision_id}: record_hash {d.record_hash} != {expected}",
                                   {"decision_id": str(d.decision_id)})
            prev = self._latest(w.conn, "decisions", "decision_id", str(d.decision_id), DecisionRecord)
            if prev is not None and _strip(prev, _DECISION_MUTABLE) != _strip(d, _DECISION_MUTABLE):
                raise SchemaError(f"decision {d.decision_id}: a new version may change only outcomes and signposts",
                                  {"decision_id": str(d.decision_id)})
            for rid in d.run_manifests:
                manifest = self._begin_manifest(w.conn, rid)
                if manifest is None:
                    raise SchemaError(f"decision {d.decision_id} cites unknown run {rid}",
                                      {"decision_id": str(d.decision_id)})
                if manifest.data_class != d.data_class:
                    raise DataClassMixError(f"decision {d.decision_id} ({d.data_class.value}) cites run {rid} "
                                            f"({manifest.data_class.value})", {"decision_id": str(d.decision_id)})
            w.append("decision", canonical_json(d).decode("utf-8"), cls=art.class_path(DecisionRecord),
                     table="decisions", columns={"decision_id": str(d.decision_id), "record_hash": d.record_hash})

    def get_decision(self, decision_id: str) -> DecisionRecord:
        with self._lock:
            rec = self._latest(self._reader(), "decisions", "decision_id", str(decision_id), DecisionRecord)
        if rec is None:
            raise EvidenceMissing(f"decision {decision_id} is not registered", {"decision_id": str(decision_id)})
        return rec

    def list_decisions(self, *, latest_only: bool = False) -> list[DecisionRecord]:
        """Decision records in chain order (every version), or the latest version of each decision."""
        rows = self._query("SELECT t.decision_id, c.payload FROM decisions t JOIN chain c ON c.seq = t.seq "
                           "ORDER BY t.seq")
        if not latest_only:
            return [_body(p, DecisionRecord) for _, p in rows]
        latest: dict[str, str] = {}
        for decision_id, payload in rows:
            latest[decision_id] = payload
        return [_body(p, DecisionRecord) for p in latest.values()]

    # -- provenance and mFDR --------------------------------------------------------------------------------
    def get_provenance(self, ref: ArtifactRef) -> ProvenanceNode:
        """Provenance node of a reference: kind, parents (declared + producing run) and content hash.

        The pointer is echoed, not resolved (``get_artifact`` resolves it).
        """
        r = parse_ref(ref)
        with self._lock:
            if r.artifact == MANIFEST_ARTIFACT:
                manifest = self._begin_manifest(self._reader(), r.run_id)
                if manifest is None:
                    raise EvidenceMissing(f"unknown run {r.run_id}", {"ref": str(r)})
                return run_node(r.run_id, content_hash(manifest), manifest.parent_runs)
            info = self._artifact_info(self._reader(), r.run_id, r.artifact)
        if info is None:
            raise EvidenceMissing(f"artifact {r.run_id}:{r.artifact} is not registered", {"ref": str(r)})
        return artifact_node(r, info.kind, info.parents, info.checksum)

    def mfdr(self) -> MFDRLedger:
        """The across-contract mFDR table (S-ADR-18)."""
        return MFDRLedger(self)

    def chain_head(self) -> tuple[int, str]:
        """(row count, last row hash) without verification: the anchor to record in manifests and packs."""
        rows = self._query("SELECT seq, row_hash FROM chain ORDER BY seq DESC LIMIT 1")
        return (rows[0][0], rows[0][1]) if rows else (0, GENESIS_HASH)

    # -- verification ---------------------------------------------------------------------------------------
    def verify_chain(self, *, check_artifacts: bool = True) -> ChainReport:
        """Verify the whole registry; ``first_bad_seq`` names the first bad row (§4.6 tamper drill).

        Checks: the append-only triggers; contiguous seqs, links and row hashes; that every chain row is indexed
        exactly as its envelope says (kind, every index column); the decision records' own chain; the mFDR wealth
        sequence; and, with ``check_artifacts``, every artifact file's sha256.
        """
        issues: list[ChainIssue] = []
        checked = 0
        with self._lock:
            conn = self._reader()
            conn.execute("BEGIN")       # one read snapshot for every pass, whatever other processes append meanwhile
            try:
                issues += [ChainIssue(seq=None, table="schema", reason=f"append-only trigger {t} is missing")
                           for t in self._missing_triggers(conn)]
                cursor = conn.execute("SELECT seq, payload, prev_hash, row_hash FROM chain ORDER BY seq")
                rows, head, link_issues = verify_links(cursor)
                cursor.close()
                issues += link_issues
                issues += self._verify_indexes(conn)
                issues += self._verify_decisions(conn)
                issues += self._verify_mfdr(conn)
                if check_artifacts:
                    checked, artifact_issues = self._verify_artifact_files(conn)
                    issues += artifact_issues
            finally:
                conn.execute("COMMIT")
        issues = issues[:MAX_ISSUES]
        seqs = [i.seq for i in issues if i.seq is not None]
        report = ChainReport(ok=not issues, rows=rows, head=head, first_bad_seq=min(seqs) if seqs else None,
                             issues=tuple(issues), artifacts_checked=checked, checked_at=datetime.now(timezone.utc))
        log = logger.info if report.ok else logger.error
        log("registry.chain_verified", extra={"ok": report.ok, "first_bad_seq": report.first_bad_seq})
        return report

    def _verify_indexes(self, conn: sqlite3.Connection) -> list[ChainIssue]:
        issues: list[ChainIssue] = []
        unknown = conn.execute(
            "SELECT seq, kind FROM chain WHERE substr(kind, 1, ?) != ? AND kind NOT IN (%s) ORDER BY seq"
            % ", ".join("?" * len(_KNOWN_KINDS)), (len(_LEDGER_PREFIX), _LEDGER_PREFIX, *sorted(_KNOWN_KINDS)))
        issues += [ChainIssue(seq=s, table="chain", reason=f"unknown record kind {k!r}") for s, k in unknown]
        for spec in _INDEX:
            if spec.prefix is not None:
                where, params = "substr(c.kind, 1, ?) = ?", (len(spec.prefix), spec.prefix)
            else:
                where, params = "c.kind IN (%s)" % ", ".join("?" * len(spec.kinds)), spec.kinds
            missing = conn.execute(f"SELECT c.seq FROM chain c WHERE {where} AND NOT EXISTS "
                                   f"(SELECT 1 FROM {spec.table} t WHERE t.seq = c.seq) ORDER BY c.seq", params)
            issues += [ChainIssue(seq=s, table=spec.table, reason="chain row has no index row") for (s,) in missing]
            cols = ", ".join(f"t.{c}" for c in spec.columns)
            cursor = conn.execute(f"SELECT t.seq, {cols}, c.kind, c.payload FROM {spec.table} t "
                                  f"LEFT JOIN chain c ON c.seq = t.seq ORDER BY t.seq")
            try:
                for row in cursor:
                    seq, values, kind, payload = row[0], row[1:-2], row[-2], row[-1]
                    problem = self._index_problem(spec, values, kind, payload)
                    if problem:
                        issues.append(ChainIssue(seq=seq, table=spec.table, reason=problem))
                    if len(issues) >= MAX_ISSUES:
                        return issues
            finally:
                cursor.close()
        return issues

    @staticmethod
    def _index_problem(spec: _IndexSpec, values: tuple[Any, ...], kind: str | None, payload: str | None) -> str | None:
        if payload is None:
            return "index row points at no chain row"
        try:
            env = json.loads(payload)
        except ValueError:
            return "chain payload is not JSON"
        if not isinstance(env, dict) or env.get("kind") != kind:
            return f"chain kind column {kind!r} disagrees with its envelope"
        if spec.prefix is not None:
            if not kind.startswith(spec.prefix):
                return f"indexes a {kind!r} row"
        elif kind not in spec.kinds:
            return f"indexes a {kind!r} row"
        try:
            derived = spec.derive(kind, env["body"])
        except (KeyError, TypeError, ValueError) as exc:
            return f"envelope body cannot be indexed ({exc})"
        if tuple(derived) != tuple(values):
            changed = [c for c, a, b in zip(spec.columns, values, derived, strict=True) if a != b]
            return f"index column(s) {changed} disagree with the chain row"
        return None

    def _verify_decisions(self, conn: sqlite3.Connection) -> list[ChainIssue]:
        issues: list[ChainIssue] = []
        prev = GENESIS_HASH
        for seq, payload in conn.execute("SELECT c.seq, c.payload FROM chain c WHERE c.kind = 'decision' "
                                         "ORDER BY c.seq"):
            try:
                rec = _body(payload, DecisionRecord)
            except SchemaError as exc:
                issues.append(ChainIssue(seq=seq, table="decisions", reason=f"unreadable decision record ({exc.message})"))
                continue
            if rec.prev_hash != prev:
                issues.append(ChainIssue(seq=seq, table="decisions", reason="decision prev_hash breaks the decision chain"))
            if record_hash(rec) != rec.record_hash:
                issues.append(ChainIssue(seq=seq, table="decisions", reason="decision record_hash does not match"))
            prev = rec.record_hash
        return issues

    def _verify_mfdr(self, conn: sqlite3.Connection) -> list[ChainIssue]:
        issues: list[ChainIssue] = []
        wealth: float | None = None
        for seq, kind, payload in conn.execute("SELECT seq, kind, payload FROM chain WHERE kind IN (?, ?) "
                                               "ORDER BY seq", (CONFIG_KIND, TEST_KIND)):
            try:
                if kind == CONFIG_KIND:
                    if wealth is not None:
                        issues.append(ChainIssue(seq=seq, table="mfdr_config", reason="second mFDR configuration"))
                        continue
                    wealth = _body(payload, MFDRConfig).w0
                    continue
                test = _body(payload, MFDRTest)
            except SchemaError as exc:
                issues.append(ChainIssue(seq=seq, table="mfdr_tests", reason=f"unreadable mFDR row ({exc.message})"))
                continue
            if wealth is None:
                issues.append(ChainIssue(seq=seq, table="mfdr_tests", reason="mFDR test before the configuration"))
            elif test.wealth_before != wealth:
                issues.append(ChainIssue(seq=seq, table="mfdr_tests", reason="wealth_before breaks the wealth sequence"))
            wealth = test.wealth_after
        return issues

    def _verify_artifact_files(self, conn: sqlite3.Connection) -> tuple[int, list[ChainIssue]]:
        issues: list[ChainIssue] = []
        count = 0
        for seq, payload in conn.execute("SELECT c.seq, c.payload FROM chain c WHERE c.kind = 'artifact' "
                                         "ORDER BY c.seq"):
            count += 1
            try:
                info = _body(payload, ArtifactInfo)
                art.verify_file(self._artifact_file(info), info)
            except (SchemaError, HashMismatch) as exc:
                issues.append(ChainIssue(seq=seq, table="artifacts", reason=exc.message))
        return count, issues

    def __repr__(self) -> str:
        return f"Registry({self._db_path.name!r}, readonly={self._readonly})"
