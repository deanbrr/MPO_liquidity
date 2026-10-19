"""JSON-lines logging (BUILD_SPEC v1.1 §1.9).

``JsonFormatter`` renders one JSON object per line with ``ts`` (UTC ISO-8601), ``level``, ``module``, ``event``
(the log message, a stable event name), the context keys ``run_id``, ``campaign_id``, ``plane``, ``world``
(null when absent) and every event-specific key passed through ``extra``. Log messages carry event names, not
free-text numbers that claims could cite. Logs go to ``runs/<run_id>/logs/*.jsonl``.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any, Final

__all__ = ["JsonFormatter", "CONTEXT_KEYS", "jsonl_handler"]

CONTEXT_KEYS: Final[tuple[str, ...]] = ("run_id", "campaign_id", "plane", "world")
_STANDARD_ATTRS: Final = frozenset(vars(logging.LogRecord("", 0, "", 0, "", (), None)).keys()) | {"message", "asctime", "taskName"}


def _default(obj: Any) -> Any:
    if hasattr(obj, "value") and not isinstance(obj, (str, int, float)):
        return obj.value
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


class JsonFormatter(logging.Formatter):
    """One JSON object per line (keys sorted for stable diffs)."""

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, tz=timezone.utc)
        out: dict[str, Any] = {
            "ts": ts.strftime("%Y-%m-%dT%H:%M:%S.") + f"{ts.microsecond // 1000:03d}Z",
            "level": record.levelname,
            "module": record.name,
            "event": record.getMessage(),
        }
        for key in CONTEXT_KEYS:
            out[key] = getattr(record, key, None)
        for key, value in vars(record).items():
            if key not in _STANDARD_ATTRS and key not in out:
                out[key] = value
        if record.exc_info:
            out["exc_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
            out["exc"] = self.formatException(record.exc_info)
            code = getattr(record.exc_info[1], "code", None)
            if isinstance(code, str):
                out["error_code"] = code
        return json.dumps(out, sort_keys=True, default=_default, ensure_ascii=False)


def jsonl_handler(path: str) -> logging.FileHandler:
    """A UTF-8 file handler writing JSON lines to ``path``."""
    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setFormatter(JsonFormatter())
    return handler
