"""JSON-lines logging (BUILD_SPEC v1.1 §1.9). Owner WP-01."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from adic_tpa.contracts.enums import Plane
from adic_tpa.contracts.errors import HashMismatch
from adic_tpa.contracts.logjson import CONTEXT_KEYS, JsonFormatter, jsonl_handler


def _record(msg: str, **extra: object) -> logging.LogRecord:
    logger = logging.getLogger("adic_tpa.test")
    return logger.makeRecord("adic_tpa.test", logging.INFO, __file__, 1, msg, (), None, extra=extra)


def test_one_json_object_per_line_with_context_keys() -> None:
    line = JsonFormatter().format(_record("solver_done", run_id="run-1", plane=Plane.SEARCH, status="optimal"))
    obj = json.loads(line)
    assert "\n" not in line
    assert obj["event"] == "solver_done" and obj["level"] == "INFO" and obj["module"] == "adic_tpa.test"
    assert obj["ts"].endswith("Z") and obj["run_id"] == "run-1" and obj["plane"] == "SEARCH"
    assert obj["status"] == "optimal" and obj["campaign_id"] is None and obj["world"] is None
    assert set(CONTEXT_KEYS) <= set(obj)


def test_exception_records_carry_the_error_code() -> None:
    try:
        raise HashMismatch("cube changed")
    except HashMismatch:
        import sys

        rec = logging.getLogger("x").makeRecord("x", logging.ERROR, __file__, 1, "abort", (), sys.exc_info())
    obj = json.loads(JsonFormatter().format(rec))
    assert obj["error_code"] == "HASH_MISMATCH" and obj["exc_type"] == "HashMismatch"


def test_file_handler_writes_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    handler = jsonl_handler(str(path))
    logger = logging.getLogger("adic_tpa.test.file")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    try:
        logger.info("cube_built", extra={"world": "M1", "n_paths": 2000})
    finally:
        logger.removeHandler(handler)
        handler.close()
    (line,) = path.read_text(encoding="utf-8").splitlines()
    assert json.loads(line)["n_paths"] == 2000
