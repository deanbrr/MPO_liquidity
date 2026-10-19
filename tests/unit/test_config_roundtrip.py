"""Config round trip (BUILD_SPEC v1.1 §1.11, §4.1; S-ADR-39). Owner WP-01; every WP's config files are covered.

Every YAML file under ``src/adic_tpa/config`` declares its model in a ``# model: <module>:<Class>`` header and
loads through it in Pydantic JSON mode. JSON mode is what makes strict models accept enum strings and YAML lists
for tuple fields.
"""

from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path

import pytest
from pydantic import BaseModel

from adic_tpa.contracts.config import (
    ConfigLoad, clear_config_audit, config_root, declared_model_path, load_json_payload, load_yaml,
    loaded_config_files, note_config_load, validate_model,
)
from adic_tpa.contracts.enums import ContractModel, Lens
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import file_hash

CONFIG_FILES = sorted(p for p in config_root().rglob("*") if p.suffix in (".yaml", ".yml"))


def _resolve(dotted: str) -> type[BaseModel]:
    module, _, name = dotted.partition(":")
    model = getattr(importlib.import_module(module), name)
    assert isinstance(model, type) and issubclass(model, BaseModel), f"{dotted} is not a Pydantic model"
    return model


def test_config_tree_holds_the_taxonomies() -> None:
    names = {p.relative_to(config_root()).as_posix() for p in CONFIG_FILES}
    assert {"taxonomy/groups_v1.yaml", "taxonomy/groups_v2.yaml"} <= names


@pytest.mark.parametrize("path", CONFIG_FILES, ids=lambda p: p.relative_to(config_root()).as_posix())
def test_every_config_file_loads_through_its_model(path: Path) -> None:
    dotted = declared_model_path(path)
    assert dotted is not None, f"{path.name}: add a '# model: <module>:<Class>' header comment"
    obj = load_yaml(path, _resolve(dotted))
    again = type(obj).model_validate_json(obj.model_dump_json())   # JSON round trip is lossless
    assert again == obj


class _Kind(StrEnum):
    A = "A"
    B = "B"


class _Probe(ContractModel):
    lens: Lens
    kind: _Kind
    pair: tuple[float, float]
    lenses: tuple[Lens, ...]


def test_enum_strings_and_yaml_lists_validate_in_json_mode(tmp_path: Path) -> None:
    path = tmp_path / "probe.yaml"
    path.write_text("# model: test:Probe\nlens: REFINANCE\nkind: B\npair: [0.25, 0.75]\nlenses:\n  - SELL\n  - HOLD\n",
                    encoding="utf-8")
    obj = load_yaml(path, _Probe)
    assert obj.lens is Lens.REFINANCE and obj.kind is _Kind.B and obj.pair == (0.25, 0.75)
    assert obj.lenses == (Lens.SELL, Lens.HOLD)
    with pytest.raises(Exception):   # strict Python mode would reject the same data
        _Probe.model_validate({"lens": "REFINANCE", "kind": "B", "pair": [0.25, 0.75], "lenses": ["SELL"]})


def test_yaml_dates_validate(tmp_path: Path) -> None:
    from datetime import date

    class Dated(ContractModel):
        asof: date

    path = tmp_path / "d.yaml"
    path.write_text("asof: 2026-09-30\n", encoding="utf-8")
    assert load_yaml(path, Dated).asof == date(2026, 9, 30)


def test_invalid_config_raises_schema_error_with_errors(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("lens: SIDEWAYS\nkind: A\npair: [1, 2]\nlenses: []\nextra: 1\n", encoding="utf-8")
    with pytest.raises(SchemaError) as exc:
        load_yaml(path, _Probe)
    types = {e["type"] for e in exc.value.context["errors"]}
    assert {"enum", "extra_forbidden"} <= types
    broken = tmp_path / "broken.yaml"
    broken.write_text("a: [1, 2\n", encoding="utf-8")
    with pytest.raises(SchemaError, match="cannot read YAML"):
        load_yaml(broken, _Probe)


def test_loads_are_audited_with_lf_normalized_hashes(tmp_path: Path) -> None:
    clear_config_audit()
    path = tmp_path / "probe.yaml"
    path.write_bytes(b"lens: SELL\r\nkind: A\r\npair: [0, 1]\r\nlenses: []\r\n")
    load_yaml(path, _Probe)
    (record,) = loaded_config_files()
    assert record.file_hash == file_hash(path) and record.model.endswith("_Probe")
    path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    assert file_hash(path) == record.file_hash


def test_json_payloads_validate_in_json_mode() -> None:
    raw = json.dumps({"lens": "ADD", "kind": "A", "pair": [1, 2], "lenses": ["PACE"]})
    assert load_json_payload(raw, _Probe).lenses == (Lens.PACE,)
    with pytest.raises(SchemaError):
        load_json_payload(raw.replace("ADD", "add"), _Probe)


def test_validate_model_is_the_python_data_boundary() -> None:
    """Review R18: Python data (enum members or strings, tuples, nested models) validates in JSON mode and
    failures are SchemaError (a TPAError), never a bare pydantic.ValidationError."""
    obj = validate_model(_Probe, {"lens": Lens.SELL, "kind": "B", "pair": (0.25, 0.75), "lenses": [Lens.HOLD, "ADD"]})
    assert obj.lens is Lens.SELL and obj.pair == (0.25, 0.75) and obj.lenses == (Lens.HOLD, Lens.ADD)
    with pytest.raises(SchemaError) as exc:
        validate_model(_Probe, {"lens": "SIDEWAYS", "kind": "A", "pair": [1, 2], "lenses": []})
    assert exc.value.code == "SCHEMA" and exc.value.context["errors"][0]["type"] == "enum"
    with pytest.raises(SchemaError, match="not JSON-serializable"):
        validate_model(_Probe, {"lens": object()})

    class Outer(ContractModel):
        probe: _Probe
        when: datetime

    outer = validate_model(Outer, {"probe": obj, "when": datetime(2026, 10, 18, 9, tzinfo=timezone.utc)})
    assert outer.probe == obj and outer.when.year == 2026


def test_tpa_errors_raised_by_validators_pass_through_the_loaders() -> None:
    from adic_tpa.contracts.errors import RunModeRefused
    from adic_tpa.contracts.evidence import RunManifest

    manifest = {"run_id": "run-20261018T091500Z-3f2a9c1d", "kind": "quarter", "created_at": "2026-10-18T09:15:00Z",
                "engine_git_sha": "abc", "engine_tree_hash": "h", "config_hash": "h", "contract_hash": None,
                "snapshot_hash": "h", "census_hash": None, "belief_hash": None, "scenario_hashes": {},
                "seed_spawn": {}, "plane": "SEARCH", "cache_keys": [], "solver_records": [], "versions": {},
                "env": {}, "llm_calls": [], "data_class": "REAL", "run_mode": "DEV_SYNTHETIC", "status": "OK"}
    with pytest.raises(RunModeRefused):
        load_json_payload(json.dumps(manifest), RunManifest)
    with pytest.raises(RunModeRefused):
        validate_model(RunManifest, manifest)


def test_note_config_load_records_once() -> None:
    clear_config_audit()
    record = ConfigLoad(path="C:/x/cached.yaml", file_hash="sha256:" + "0" * 64, model="m:M")
    note_config_load(record)
    note_config_load(record)
    assert loaded_config_files() == (record,)
    clear_config_audit()


def test_model_header_parsing(tmp_path: Path) -> None:
    path = tmp_path / "h.yaml"
    path.write_text("# comment first\n#  model:  pkg.mod:Model  \n\nkey: 1\n", encoding="utf-8")
    assert declared_model_path(path) == "pkg.mod:Model"
    path.write_text("key: 1\n# model: pkg.mod:Model\n", encoding="utf-8")
    assert declared_model_path(path) is None
