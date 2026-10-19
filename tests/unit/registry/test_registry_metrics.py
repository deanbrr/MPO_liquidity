"""Metric registry (BUILD_SPEC v1.1 §4.6, S-ADR-42; ARCH §10.3): a definition change creates a new id; MRM
approval rows; the config/metrics/wp-NN.yaml catalog merges with a duplicate-id check. Owner WP-04. SYNTHETIC
values only."""

from __future__ import annotations

from pathlib import Path

import pytest

from adic_tpa.contracts.config import config_root, declared_model_path
from adic_tpa.contracts.errors import EvidenceMissing, SchemaError
from adic_tpa.contracts.evidence import MetricDef
from adic_tpa.registry import Registry
from adic_tpa.registry.metrics import (
    MetricCatalogEntry, by_key, catalog_definitions, core_definition, definition_hash, load_metric_catalog,
    metrics_config_root, next_version, split_version,
)


def test_definition_change_creates_a_new_id(reg: Registry, factory) -> None:
    v1 = factory.metric_def()
    reg.define_metric(v1)
    reg.define_metric(v1)                                                 # identical repeat: no-op
    changed = factory.metric_def(description="SYNTHETIC test metric, re-binned")
    with pytest.raises(SchemaError, match="new metric id") as exc:
        reg.define_metric(changed)
    assert exc.value.context["suggested"] == "tier1.t6.cp_upper@v2"
    v2 = factory.metric_def("tier1.t6.cp_upper@v2", description="SYNTHETIC test metric, re-binned")
    reg.define_metric(v2)
    assert reg.get_metric_def("tier1.t6.cp_upper@v1") == v1               # the old id keeps the old definition
    assert reg.get_metric_def("tier1.t6.cp_upper@v2") == v2
    assert [d.metric_id for d in reg.list_metric_defs(prefix="tier1.t6")] == ["tier1.t6.cp_upper@v1",
                                                                              "tier1.t6.cp_upper@v2"]
    assert reg.list_metric_defs(prefix="tier9") == []
    with pytest.raises(EvidenceMissing):
        reg.get_metric_def("tier1.t6.cp_upper@v3")
    assert reg.verify_chain().rows == 2


def test_mrm_approval_flag(reg: Registry, factory) -> None:
    reg.define_metric(factory.metric_def())
    assert not reg.is_metric_approved("tier1.t6.cp_upper@v1")
    reg.approve_metric("tier1.t6.cp_upper@v1", approver="MRM:sha256:" + "7" * 64)
    assert reg.is_metric_approved("tier1.t6.cp_upper@v1")
    with pytest.raises(SchemaError, match="undefined"):
        reg.approve_metric("tier1.t7.cp_upper@v1", approver="MRM")
    assert reg.verify_chain().ok


def test_catalog_entries_enter_the_registry_as_core_definitions(reg: Registry, factory) -> None:
    core = factory.metric_def()
    entry = MetricCatalogEntry(**core.model_dump(), short_label="P(red) CP upper", scope="portfolio",
                               aliases=("p_red_cp",), entity_keys=("class",))
    assert type(core_definition(entry)) is MetricDef and core_definition(entry) == core
    assert definition_hash(entry) == definition_hash(core)
    reg.define_metric(entry)
    reg.define_metric(core)                                               # same definition: no-op
    assert type(reg.get_metric_def(core.metric_id)) is MetricDef
    with pytest.raises(SchemaError):
        core_definition({"metric_id": "x"})  # type: ignore[arg-type]


def test_by_key_and_versions() -> None:
    from adic_tpa.contracts.hashing import canonical_json
    from adic_tpa.contracts.ids import GroupId

    assert by_key(None) == by_key({}) == "{}"
    assert by_key({"world": "M6", "class": "M1-M5"}) == '{"class":"M1-M5","world":"M6"}'
    for by in ({"b": "é – x", "a": "1"}, {GroupId("REALASSETS"): "SYN-RA-0007"}, {"q": "\"quoted\""}):
        assert by_key(by) == canonical_json(dict(by)).decode("utf-8")
    assert split_version("tier1.t6.cp_upper@v12") == ("tier1.t6.cp_upper", 12)
    assert next_version("tier1.t6.cp_upper@v1", ["tier1.t6.cp_upper@v1", "tier1.t6.cp_upper@v4", "x.y@v9"]) == \
        "tier1.t6.cp_upper@v5"
    with pytest.raises(SchemaError):
        split_version("no_version")


def _write(path: Path, owner: str, ids: list[str]) -> None:
    lines = ["# model: adic_tpa.registry.metrics:MetricCatalogFile", f"owner_wp: {owner}", "metrics:"]
    for mid in ids:
        lines += [f"  - metric_id: {mid}", "    description: SYNTHETIC test metric", "    unit: prob",
                  "    aggregation: mean", "    ci_method: clopper_pearson", "    range_method: model_min_max",
                  "    icd203: true", "    owner_role: CRO", "    code_ref: core.certify",
                  "    code_hash: sha256:" + "4" * 64, "    short_label: P(red)", "    scope: portfolio",
                  "    entity_keys: [class]"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_catalog_merges_wp_files(tmp_path: Path, reg: Registry) -> None:
    _write(tmp_path / "wp-17.yaml", "WP-17", ["tier1.t6.cp_upper@v1", "tier1.t7.share@v1"])
    _write(tmp_path / "wp-13.yaml", "WP-13", ["ledger.t4p.survival_months@v1"])
    catalog = load_metric_catalog(tmp_path)
    assert sorted(catalog) == ["ledger.t4p.survival_months@v1", "tier1.t6.cp_upper@v1", "tier1.t7.share@v1"]
    assert catalog["tier1.t6.cp_upper@v1"].entity_keys == ("class",)
    assert declared_model_path(tmp_path / "wp-17.yaml") == "adic_tpa.registry.metrics:MetricCatalogFile"
    for d in catalog_definitions(catalog):
        reg.define_metric(d)
    assert len(reg.list_metric_defs()) == 3


def test_catalog_rejects_duplicates_and_misnamed_files(tmp_path: Path) -> None:
    _write(tmp_path / "wp-17.yaml", "WP-17", ["tier1.t6.cp_upper@v1"])
    _write(tmp_path / "wp-18.yaml", "WP-18", ["tier1.t6.cp_upper@v1"])
    with pytest.raises(SchemaError, match="duplicate metric id") as exc:
        load_metric_catalog(tmp_path)
    assert exc.value.context["files"] == ["wp-17.yaml", "wp-18.yaml"]
    (tmp_path / "wp-18.yaml").unlink()
    _write(tmp_path / "wp-19.yaml", "WP-20", ["x.y@v1"])
    with pytest.raises(SchemaError, match="does not match"):
        load_metric_catalog(tmp_path)
    (tmp_path / "wp-19.yaml").unlink()
    _write(tmp_path / "metrics.yaml", "WP-21", ["x.z@v1"])
    with pytest.raises(SchemaError, match="wp-NN.yaml"):
        load_metric_catalog(tmp_path)
    (tmp_path / "metrics.yaml").unlink()
    _write(tmp_path / "wp-21.yaml", "21", ["x.z@v1"])
    with pytest.raises(SchemaError, match="owner_wp"):
        load_metric_catalog(tmp_path)


def test_packaged_catalog_loads() -> None:
    assert metrics_config_root() == config_root() / "metrics"
    catalog = load_metric_catalog()                                       # every WP's file merges cleanly
    assert all(isinstance(e, MetricCatalogEntry) for e in catalog.values())
    assert load_metric_catalog(config_root() / "no_such_dir") == {}
