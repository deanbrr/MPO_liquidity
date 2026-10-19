"""contracts.hashing (BUILD_SPEC v1.1 §4.1): golden hashes for 10 objects, float repr round trip, NaN/inf
rejected, canonical rules. Owner WP-01. (Cross-process and PYTHONHASHSEED stability:
tests/determinism/test_hash_seed_stability.py.)"""

from __future__ import annotations

import json
import math
from datetime import date, datetime, timedelta, timezone
from enum import IntEnum
from pathlib import Path

import numpy as np
import pytest

from adic_tpa.contracts.enums import CFPStage, ConsentScenario, Lens, ReturnBasis, RowFamily
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import array_checksum, canonical_json, content_hash, to_jsonable
from adic_tpa.contracts.ids import HoldingId
from adic_tpa.contracts.optimizer import RowKey


def golden_objects() -> list[tuple[str, object]]:
    """Ten fixed objects whose hashes are frozen below (any change here is a contract change)."""
    return [
        ("empty_dict", {}),
        ("scalars", {"b": True, "n": None, "i": -7, "f": 0.1, "s": "SYNTHETIC – NOT ADIC DATA"}),
        ("nested_unsorted", {"z": [3, 2, 1], "a": {"y": 1.5, "x": [True, False]}}),
        ("floats", [1.0, 1e-17, 1e300, -2.5, 177.0, 0.0085, 1 / 3]),
        ("datetimes", {"aware": datetime(2026, 10, 18, 13, 15, tzinfo=timezone(timedelta(hours=4))),
                       "naive": datetime(2026, 10, 18, 9, 15, 0, 250000), "date": date(2026, 9, 30)}),
        ("enums", [Lens.REFINANCE, ConsentScenario.R0X, CFPStage.AMBER]),
        ("model", ReturnBasis(kind="log", fees="net")),
        ("row_key", RowKey(family=RowFamily.LR4, idx=(("g", "PE"), ("h", 24)))),
        ("array", np.arange(6, dtype=np.float32).reshape(2, 3)),
        ("mixed", {"holding": HoldingId("SYN-PE-0042"), "tuple": (1, "a"), "bytes": b"\x00\xff",
                   "enum_keys": {CFPStage.RED: 1, CFPStage.GREEN: 0}}),
    ]


GOLDEN = {
    "empty_dict": "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    "scalars": "sha256:db67b8744841aa35100ba5b1a522b9dfedad01dcbce2ac469612379373d118a1",
    "nested_unsorted": "sha256:783f31c2ceafd2b259f92a8d1b80d978434a21754f058af7adf8236babb44003",
    "floats": "sha256:191ec6cca2dda6ec8db4fe6733a124255feb11e49d8d381d13cf5f74024c36a1",
    "datetimes": "sha256:b48481b746ccfa55fded98c9d255296de2cf186cf84739c45264bd02988c90c6",
    "enums": "sha256:83a9f97f1ae64b249f7970c81acc0ae162cb540f5e1e71e516223c8eb7e872cd",
    "model": "sha256:a5c304bcfcd6d826c72c236f7646a4f0a2b0756d58d7bb96d44f5946c9938c95",
    "row_key": "sha256:4c059347d149f80cd3f15e93470231ee157662abe1734ce1ff2354861fab5a95",
    "array": "sha256:00e5d5f14df2320689622693d6cdb46f38584c48a0dad453bd3d5283d4755a7a",
    "mixed": "sha256:db86d6b8f9d7a43b55b95b44fdf87f2560bc39aae4206a1d20464e97c3da99b4",
}


@pytest.mark.parametrize(("name", "obj"), golden_objects(), ids=[n for n, _ in golden_objects()])
def test_golden_hashes(name: str, obj: object) -> None:
    assert content_hash(obj) == GOLDEN[name]


def test_canonical_form() -> None:
    assert canonical_json({"b": 1, "a": [1.0, None, True]}) == b'{"a":[1.0,null,true],"b":1}'
    assert canonical_json(datetime(2026, 10, 18, 13, 15, tzinfo=timezone(timedelta(hours=4)))) == \
        b'"2026-10-18T09:15:00Z"'
    assert canonical_json(datetime(2026, 10, 18, 9, 15)) == b'"2026-10-18T09:15:00Z"'   # naive read as UTC
    assert canonical_json(Lens.SELL) == b'"SELL"' and canonical_json(CFPStage.RED) == b"2"
    assert canonical_json(-0.0) == b"0.0"
    assert canonical_json("–") == "\"–\"".encode("utf-8")                              # UTF-8, not \u escapes


@pytest.mark.parametrize("x", [0.1, 1 / 3, 1e-310, 2.0**-1074, 1.7976931348623157e308, 123456.789e-12, -5e-324])
def test_float_repr_round_trip(x: float) -> None:
    text = canonical_json(x).decode()
    assert text == repr(x)
    assert float(json.loads(text)) == x


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf, {"x": [1.0, math.nan]}, np.float64(np.inf)])
def test_non_finite_rejected(bad: object) -> None:
    with pytest.raises(SchemaError):
        canonical_json(bad)


def test_key_collision_and_unsupported_types_rejected() -> None:
    with pytest.raises(SchemaError):
        canonical_json({1: "a", "1": "b"})
    with pytest.raises(SchemaError):
        canonical_json(object())
    with pytest.raises(SchemaError):
        canonical_json({(1, 2): "tuple key"})


def test_insertion_order_and_sets_do_not_matter() -> None:
    assert content_hash({"a": 1, "b": 2}) == content_hash({"b": 2, "a": 1})
    assert content_hash({3, 1, 2}) == content_hash({2, 3, 1}) == content_hash(frozenset({1, 2, 3}))


def test_numpy_scalars_and_int_enums_hash_like_python_values() -> None:
    class Code(IntEnum):
        X = 3

    assert content_hash(np.int64(3)) == content_hash(3) == content_hash(Code.X)
    assert content_hash(np.float32(0.5)) == content_hash(0.5)
    assert to_jsonable(Path("a") / "b") == "a/b"


def test_array_checksum_sensitivity() -> None:
    a = np.arange(6, dtype=np.float64)
    assert array_checksum(a) == array_checksum(a.copy())
    assert array_checksum(a) != array_checksum(a.astype(np.float32))           # dtype
    assert array_checksum(a) != array_checksum(a.reshape(2, 3))                 # shape
    assert array_checksum(a[::2]) == array_checksum(np.ascontiguousarray(a[::2]))   # C-order bytes
    assert array_checksum(a, a) != array_checksum(a)                             # sequence
    with pytest.raises(SchemaError):
        array_checksum(np.array([object()]))


def test_pydantic_models_hash_by_content() -> None:
    assert content_hash(ReturnBasis(kind="log", fees="net")) == content_hash({"kind": "log", "fees": "net"})
