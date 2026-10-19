"""Evidence contracts (BUILD_SPEC v1.1 §3.15, §3.17; S-ADR-36): tuning boxes, path-metric series. Owner WP-01.
SYNTHETIC values only."""

from __future__ import annotations

import json

import numpy as np
import pytest
from pydantic import ValidationError

from adic_tpa.contracts.evidence import REQUIRED_TERMINAL_SERIES, PathMetrics, PathMetricsMeta, TuningJob

H64 = "sha256:" + "0" * 64


def test_tuning_job_dict_view() -> None:
    job = TuningJob.model_validate_json(json.dumps(
        {"box": [{"name": "rho", "lo": -0.5, "hi": 0.5}, {"name": "on", "lo": 0.1, "hi": 0.9}], "max_evals": 12}))
    assert job.as_dict() == {"rho": (-0.5, 0.5), "on": (0.1, 0.9)}
    assert job.method == "cmaes"
    for bad in ({"box": [{"name": "rho", "lo": 0.0, "hi": 1.0}] * 2},                 # one box per parameter
                {"box": [{"name": "rho", "lo": 1.0, "hi": 0.0}]},                     # lo <= hi
                {"box": [], "max_evals": 0}):
        with pytest.raises(ValidationError):
            TuningJob.model_validate_json(json.dumps(bad))


def _meta(**changes: object) -> PathMetricsMeta:
    return PathMetricsMeta.model_validate_json(json.dumps({
        "world_id": "M6", "plane": "FINAL", "policy_ref": {"kind": "native", "name": "P0", "params_hash": H64},
        "cube_checksum": H64, "quarterly_names": ["w_tilde"], "terminal_names": list(REQUIRED_TERMINAL_SERIES),
        "data_class": "SYNTHETIC", **changes}))


def test_terminal_series_reads_the_named_column() -> None:
    terminal = np.tile(np.arange(len(REQUIRED_TERMINAL_SERIES), dtype=np.float64), (4, 1))
    terminal[:, REQUIRED_TERMINAL_SERIES.index("red_event")] = [0.0, 1.0, 0.0, 1.0]
    terminal[:, REQUIRED_TERMINAL_SERIES.index("payout_short")] = 0.0
    terminal[:, REQUIRED_TERMINAL_SERIES.index("failed")] = 1.0
    pm = PathMetrics(meta=_meta(), quarterly=np.zeros((4, 41, 1), dtype=np.float32), terminal=terminal)
    pm.validate()
    assert pm.terminal_series("red_event").tolist() == [0.0, 1.0, 0.0, 1.0]
    assert pm.terminal_series("twr_10y").tolist() == [float(REQUIRED_TERMINAL_SERIES.index("twr_10y"))] * 4
    with pytest.raises(ValueError):
        pm.terminal_series("not_a_series")


def test_path_metrics_meta_rules() -> None:
    with pytest.raises(ValidationError, match="missing"):
        _meta(terminal_names=["w_tilde_40"])
    with pytest.raises(ValidationError, match="48"):
        _meta(quarterly_names=[f"q{i}" for i in range(49)])
    with pytest.raises(ValidationError, match="unique"):
        _meta(quarterly_names=["a", "a"])
