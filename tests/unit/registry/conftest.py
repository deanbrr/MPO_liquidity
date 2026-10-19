"""Fixtures of the registry unit tests (BUILD_SPEC v1.1 §4.6; owner WP-04). SYNTHETIC values only.

``factory`` exposes small builders (manifest, metric definition and instance, claim, decision) as one namespace,
because test modules cannot import this conftest under ``--import-mode=importlib``.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date, datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from adic_tpa.contracts.claims import ClaimRecord
from adic_tpa.contracts.enums import ConsentScenario, DataClass, EvidencePlane, Plane, PricedOn, RunMode
from adic_tpa.contracts.evidence import MetricDef, MetricInstance, RunManifest
from adic_tpa.contracts.room import DecisionRecord
from adic_tpa.registry import Registry
from adic_tpa.registry.chain import GENESIS_HASH, chain_record

RUN_A = "run-20261018T091500Z-3f2a9c1d"
RUN_B = "run-20261018T101500Z-0badcafe"
RUN_C = "run-20261018T111500Z-12345678"
H = "sha256:" + "5" * 64


def make_manifest(run_id: str = RUN_A, *, plane: Plane = Plane.SEARCH, data_class: DataClass = DataClass.SYNTHETIC,
                  parents: tuple[str, ...] = (), kind: str = "quarter", status: str = "STARTED") -> RunManifest:
    return RunManifest(
        run_id=run_id, kind=kind, created_at=datetime(2026, 10, 18, 9, 15, tzinfo=timezone.utc),
        engine_git_sha="abc123", engine_tree_hash="sha256:" + "1" * 64, config_hash="sha256:" + "2" * 64,
        contract_hash=None, snapshot_hash="sha256:" + "3" * 64, census_hash=None, belief_hash=None,
        scenario_hashes={"SEARCH:M1": H}, seed_spawn={"SEARCH:M1": "00ff"}, plane=plane, cache_keys=(),
        solver_records=(), versions={"numpy": "2.5.4"}, env={}, llm_calls=(), data_class=data_class,
        run_mode=RunMode.DEV_SYNTHETIC if data_class == DataClass.SYNTHETIC else RunMode.REAL,
        parent_runs=parents, status=status)


def make_def(metric_id: str = "tier1.t6.cp_upper@v1", *, unit: str = "prob", **over: Any) -> MetricDef:
    fields: dict[str, Any] = dict(metric_id=metric_id, description="SYNTHETIC test metric", unit=unit,
                                  aggregation="mean", ci_method="clopper_pearson", range_method="model_min_max",
                                  icd203=True, owner_role="CRO", code_ref="core.certify", code_hash=H)
    fields.update(over)
    return MetricDef(**fields)


def make_metric(metric_id: str = "tier1.t6.cp_upper@v1", *, run_id: str = RUN_A, value: float = 0.0042,
                unit: str = "prob", plane: EvidencePlane = EvidencePlane.SEARCH, by: dict[str, str] | None = None,
                data_class: DataClass = DataClass.SYNTHETIC) -> MetricInstance:
    return MetricInstance(metric_id=metric_id, run_id=run_id, value=value, unit=unit, plane=plane,
                          ci=(0.001, 0.009), scenario_hash=H, by=by or {}, data_class=data_class)


def make_claim(claim_id: str = "c-1", **over: Any) -> ClaimRecord:
    fields: dict[str, Any] = dict(claim_id=claim_id, doc_id="memo-2026Q4", sentence_index=0,
                                  placeholders=("tier1.t6.cp_upper@v1",), verbs=("shows",))
    fields.update(over)
    return ClaimRecord(**fields)


def make_decision(prev_hash: str = GENESIS_HASH, *, decision_id: str = "dec-Q1-2026Q4-1",
                  runs: tuple[str, ...] = (RUN_A,), data_class: DataClass = DataClass.SYNTHETIC,
                  **over: Any) -> DecisionRecord:
    fields: dict[str, Any] = dict(
        decision_id=decision_id, register_id="Q1", as_of=date(2026, 10, 18), tier="A", options=(),
        engine_recommendation="HOLD", evidence_plane="search", run_manifests=runs, priced_on=PricedOn.FEASIBLE,
        consent_scenario=ConsentScenario.R0, recovery_hash=None, prevote_hashes=(), ballots=(), decision="approve",
        override=None, rationale="SYNTHETIC test decision", minority_reports=(), signposts=(), commitment_plan=(),
        review_date=date(2027, 1, 15), data_class=data_class, prev_hash=GENESIS_HASH, record_hash=GENESIS_HASH)
    fields.update(over)
    return chain_record(DecisionRecord(**fields), prev_hash)


@pytest.fixture
def factory() -> SimpleNamespace:
    return SimpleNamespace(manifest=make_manifest, metric_def=make_def, metric=make_metric, claim=make_claim,
                           decision=make_decision, RUN_A=RUN_A, RUN_B=RUN_B, RUN_C=RUN_C, H=H)


@pytest.fixture
def paths(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(db=tmp_path / "stores" / "registry.sqlite", root=tmp_path / "runs")


@pytest.fixture
def reg(paths: SimpleNamespace) -> Iterator[Registry]:
    registry = Registry(paths.db, paths.root)
    yield registry
    registry.close()


@pytest.fixture
def run_reg(reg: Registry) -> Registry:
    """A registry with RUN_A begun and the CP-upper metric defined."""
    reg.begin_run(make_manifest())
    reg.define_metric(make_def())
    return reg
