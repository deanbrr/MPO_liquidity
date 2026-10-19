"""Strictness of every contracts model (BUILD_SPEC v1.1 §3, §4.1): frozen, extra fields rejected, strict; array
containers are slotted dataclasses with an ARRAY_SPECS entry. Owner WP-01."""

from __future__ import annotations

import dataclasses
import importlib
import pkgutil
import sys

import pytest
from pydantic import ValidationError

import adic_tpa.contracts as contracts_pkg
from adic_tpa.contracts.arrays import ARRAY_SPECS, ArrayContainer
from adic_tpa.contracts.enums import ContractModel, Interval, ReturnBasis
from adic_tpa.contracts.optimizer import RowKey
from adic_tpa.contracts.enums import RowFamily

MUTABLE_CONTAINERS = {"ActionSlice", "UnitFinancing", "LedgerState"}


def _load_all() -> None:
    for info in pkgutil.iter_modules(contracts_pkg.__path__):
        importlib.import_module(f"adic_tpa.contracts.{info.name}")


def _subclasses(cls: type) -> list[type]:
    out, todo = [], list(cls.__subclasses__())
    while todo:
        c = todo.pop()
        out.append(c)
        todo.extend(c.__subclasses__())
    return out


def _exported(c: type) -> bool:
    """The class its module exports (``@dataclass(slots=True)`` leaves the pre-slots class among subclasses)."""
    return c.__module__.startswith("adic_tpa.") and getattr(sys.modules[c.__module__], c.__name__, None) is c


_load_all()
MODELS = sorted({c for c in _subclasses(ContractModel) if "[" not in c.__name__ and _exported(c)},
                key=lambda c: (c.__module__, c.__name__))
CONTAINERS = sorted({c for c in _subclasses(ArrayContainer) if _exported(c)}, key=lambda c: c.__name__)


def test_inventory_is_complete() -> None:
    assert len(MODELS) > 250
    names = {c.__name__ for c in MODELS}
    for required in ("BookSnapshot", "AnalysisContract", "SignOff", "LensAction", "WorldSpec", "CFPReading",
                     "Fact", "ToolResult", "OverrideConfirmation", "AnswerDraft", "BridgeCard", "TaxonomyConfig"):
        assert required in names


@pytest.mark.parametrize("model", MODELS, ids=lambda c: f"{c.__module__.rsplit('.', 1)[1]}.{c.__name__}")
def test_config_and_extra_field_rejected(model: type[ContractModel]) -> None:
    cfg = model.model_config
    assert cfg.get("frozen") is True and cfg.get("extra") == "forbid" and cfg.get("strict") is True
    with pytest.raises(ValidationError) as exc:
        model.model_validate({"__unexpected_field__": 1})
    assert any(e["type"] == "extra_forbidden" for e in exc.value.errors())


def test_instances_are_frozen() -> None:
    for obj, field in ((ReturnBasis(kind="log", fees="net"), "kind"), (Interval(lo=0.0, hi=1.0), "lo"),
                       (RowKey(family=RowFamily.T4P, idx=(("h", 7),)), "family")):
        with pytest.raises(ValidationError):
            setattr(obj, field, getattr(obj, field))


def test_strict_python_mode_rejects_coercion() -> None:
    with pytest.raises(ValidationError):
        ReturnBasis.model_validate({"kind": "log", "fees": 1})
    with pytest.raises(ValidationError):
        Interval.model_validate({"lo": "0.0", "hi": 1.0})          # no str -> float coercion
    assert Interval.model_validate_json('{"lo": 0, "hi": 1}').lo == 0.0   # JSON ints are floats


def test_row_key_is_hashable_and_round_trips() -> None:
    key = RowKey(family=RowFamily.LR4, idx=(("g", "PE"), ("h", 24)))
    assert str(key) == "LR4:g=PE:h=24"
    assert RowKey.parse("T4P:h=07") == RowKey(family=RowFamily.T4P, idx=(("h", 7),))
    assert str(RowKey.parse("TRANSITION:s=C:n=113")) == "TRANSITION:s=C:n=113"
    assert {key: 1}[RowKey.parse(str(key))] == 1


@pytest.mark.parametrize("cls", CONTAINERS, ids=lambda c: c.__name__)
def test_array_containers_are_slotted_dataclasses_with_specs(cls: type) -> None:
    assert dataclasses.is_dataclass(cls)
    # slots on every class of the MRO, so instances carry no __dict__
    assert all("__slots__" in k.__dict__ for k in cls.__mro__ if k is not object)
    params = cls.__dataclass_params__  # type: ignore[attr-defined]
    assert params.frozen is (cls.__name__ not in MUTABLE_CONTAINERS)
    assert cls.__name__ in ARRAY_SPECS, f"{cls.__name__} has no ARRAY_SPECS entry"
    fields = {f.name for f in dataclasses.fields(cls)}
    assert set(ARRAY_SPECS[cls.__name__]) <= fields


def test_every_spec_names_an_existing_container() -> None:
    assert set(ARRAY_SPECS) == {c.__name__ for c in CONTAINERS}


def test_frozen_container_rejects_mutation() -> None:
    import numpy as np

    from adic_tpa.contracts.optimizer import DualSet

    ds = DualSet(pi_row=np.zeros(2), mu_cash=np.ones(1), M_cash=np.zeros(1), ell=np.zeros(1), quality={})
    with pytest.raises(dataclasses.FrozenInstanceError):
        ds.ell = np.ones(1)  # type: ignore[misc]
    with pytest.raises((AttributeError, TypeError)):
        ds.extra = 1  # type: ignore[attr-defined]
