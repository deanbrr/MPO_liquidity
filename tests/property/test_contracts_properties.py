"""Property tests of contracts invariants (BUILD_SPEC v1.1 §4.1, §10.6). Owner WP-01."""

from __future__ import annotations

import json

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from adic_tpa.contracts.enums import RowFamily
from adic_tpa.contracts.hashing import array_checksum, canonical_artifact_hash, canonical_json, content_hash
from adic_tpa.contracts.optimizer import RowKey

json_leaf = st.one_of(st.none(), st.booleans(), st.integers(-10**12, 10**12),
                      st.floats(allow_nan=False, allow_infinity=False), st.text(max_size=8))
json_tree = st.recursive(json_leaf, lambda children: st.one_of(
    st.lists(children, max_size=3), st.dictionaries(st.text(max_size=4), children, max_size=3)), max_leaves=8)


@settings(max_examples=100, deadline=None)
@given(st.dictionaries(st.text(max_size=4), json_tree, max_size=5), st.permutations(range(5)))
def test_hash_ignores_dict_insertion_order(d: dict, order: list[int]) -> None:
    items = list(d.items())
    shuffled = [items[i] for i in order if i < len(items)]
    assert content_hash(dict(shuffled)) == content_hash(d)


@settings(max_examples=100, deadline=None)
@given(json_tree)
def test_canonical_json_round_trips_through_json(obj: object) -> None:
    text = canonical_json(obj)
    assert canonical_json(json.loads(text)) == text


@settings(max_examples=100, deadline=None)
@given(st.floats(allow_nan=False, allow_infinity=False))
def test_float_repr_round_trip(x: float) -> None:
    assert float(json.loads(canonical_json(x))) == (0.0 if x == 0 else x)


key_names = st.from_regex(r"[a-z][a-z0-9_]{0,5}", fullmatch=True)
key_values = st.one_of(st.integers(0, 10_000), st.from_regex(r"[A-Za-z_][A-Za-z0-9_.]{0,6}", fullmatch=True))


@settings(max_examples=100, deadline=None)
@given(st.sampled_from(list(RowFamily)), st.lists(st.tuples(key_names, key_values), max_size=3))
def test_row_key_string_round_trip(family: RowFamily, idx: list) -> None:
    key = RowKey(family=family, idx=tuple(idx))
    assert RowKey.parse(str(key)) == key


@settings(max_examples=50, deadline=None)
@given(st.integers(1, 6), st.integers(1, 6), st.sampled_from([np.float32, np.float64, np.int8, np.int32, np.bool_]))
def test_array_checksum_depends_on_content_not_layout(r: int, c: int, dtype: type) -> None:
    a = (np.arange(r * c) % 2 == 0).astype(dtype).reshape(r, c)
    assert array_checksum(a) == array_checksum(np.array(a, order="F"))
    assert array_checksum(a) == array_checksum(a.copy())


run_ids = st.from_regex(r"run-20[0-9]{6}T[0-9]{6}Z-[0-9a-f]{8}", fullmatch=True)


@settings(max_examples=100, deadline=None)
@given(run_ids, run_ids, st.floats(allow_nan=False, allow_infinity=False))
def test_artifact_hash_ignores_run_ids(a: str, b: str, value: float) -> None:
    def artifact(run: str) -> dict:
        return {"run_id": run, "ref": f"{run}:cards:/0", "parents": [run], "value": value}
    assert canonical_artifact_hash(artifact(a)) == canonical_artifact_hash(artifact(b))
