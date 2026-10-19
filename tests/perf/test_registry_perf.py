"""Registry performance (BUILD_SPEC v1.1 §4.6): ``put_metrics`` ≥ 10,000 rows/s; ``verify_chain`` on 1M rows
< 60 s on the reference laptop. Nightly (perf). Owner WP-04. SYNTHETIC values only."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from adic_tpa.contracts.enums import DataClass, EvidencePlane, Plane, RunMode
from adic_tpa.contracts.evidence import MetricDef, MetricInstance, RunManifest
from adic_tpa.registry import Registry

pytestmark = pytest.mark.perf

RUN = "run-20261018T091500Z-3f2a9c1d"
H = "sha256:" + "5" * 64
BATCH = 20_000


def _registry(tmp_path: Path) -> Registry:
    reg = Registry(tmp_path / "registry.sqlite", tmp_path / "runs")
    reg.begin_run(RunManifest(
        run_id=RUN, kind="perf", created_at=datetime(2026, 10, 18, 9, 15, tzinfo=timezone.utc), engine_git_sha="abc",
        engine_tree_hash=H, config_hash=H, contract_hash=None, snapshot_hash=H, census_hash=None, belief_hash=None,
        scenario_hashes={}, seed_spawn={}, plane=Plane.SEARCH, cache_keys=(), solver_records=(), versions={}, env={},
        llm_calls=(), data_class=DataClass.SYNTHETIC, run_mode=RunMode.DEV_SYNTHETIC, status="STARTED"))
    reg.define_metric(MetricDef(metric_id="perf.metric.value@v1", description="SYNTHETIC", unit="bp",
                                aggregation="mean", ci_method="mc_se", range_method="none", icd203=False,
                                owner_role="MRM", code_ref="tests.perf", code_hash=H))
    return reg


def _batch(start: int) -> list[MetricInstance]:
    return [MetricInstance(metric_id="perf.metric.value@v1", run_id=RUN, value=float(i), unit="bp",
                           plane=EvidencePlane.SEARCH, mc_se=0.5, scenario_hash=H, by={"path_block": str(i)},
                           data_class=DataClass.SYNTHETIC) for i in range(start, start + BATCH)]


def test_put_metrics_throughput(tmp_path: Path) -> None:
    with _registry(tmp_path) as reg:
        batch = _batch(0)
        start = time.perf_counter()
        reg.put_metrics(batch)
        rate = BATCH / (time.perf_counter() - start)
        assert rate >= 10_000, f"put_metrics {rate:,.0f} rows/s"


def test_verify_chain_on_a_million_rows(tmp_path: Path) -> None:
    with _registry(tmp_path) as reg:
        for k in range(1_000_000 // BATCH):
            reg.put_metrics(_batch(k * BATCH))
        start = time.perf_counter()
        report = reg.verify_chain()
        elapsed = time.perf_counter() - start
    assert report.ok and report.rows == 1_000_002
    assert elapsed < 60.0, f"verify_chain took {elapsed:.1f} s"
