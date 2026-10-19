"""Keyed uniform streams and per-block draws (BUILD_SPEC v1.1 §1.7, §4.2). Owner WP-02.

``uniforms`` is a pure function of (base, source, entity, path, month, slot); ``draw_block`` returns a valid
``NoiseSlice`` for a step's requests. SYNTHETIC seeds only.
"""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.arrays import MAX_BLOCK_PATHS
from adic_tpa.contracts.engine_io import NoiseRequest, NoiseSlice
from adic_tpa.contracts.enums import Plane
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.numerics.numba_utils import KERNEL_OPTIONS, current_threads, numba_threads
from adic_tpa.rng import UNIFORM_SCALE, base_entropy, draw_block, uniforms, warm_up

BASE = base_entropy(7, Plane.SEARCH, "M1")
P = np.arange(64)


def test_warm_up_compiles_every_kernel_and_kernels_are_cached() -> None:
    warm_up()                                   # evaluator start (§1.13); a second call only hits the caches
    warm_up()
    assert KERNEL_OPTIONS["cache"] is True and KERNEL_OPTIONS["fastmath"] is False
    before = current_threads()
    with pytest.raises(ValueError):
        with numba_threads(0):
            pass
    assert current_threads() == before


def test_shape_dtype_layout_and_range() -> None:
    u = uniforms(BASE, "priv.fund.idio", ["SYN-PE-0001", "SYN-PE-0002", None], P, np.array([0, 1, 2]), 5)
    assert u.shape == (64, 3, 3, 5) and u.dtype == np.float64 and u.flags.c_contiguous
    assert u.min() >= 0.0 and u.max() < 1.0


def test_values_are_exact_multiples_of_two_to_minus_53() -> None:
    u = uniforms(BASE, "s", [None], P, np.arange(4), 4)
    k = u / UNIFORM_SCALE
    assert np.array_equal(k, np.floor(k))


def test_adding_slots_keeps_earlier_slots() -> None:
    m = np.array([5, 6])
    u4, u6, u9 = (uniforms(BASE, "s", ["e1", "e2"], P, m, s) for s in (4, 6, 9))
    assert np.array_equal(u6[..., :4], u4)
    assert np.array_equal(u9[..., :6], u6)
    assert not np.array_equal(u9[..., 4], u9[..., 0])        # slot 4 opens a new counter block, not a repeat


def test_month_and_path_subsets_are_consistent() -> None:
    full = uniforms(BASE, "s", ["e"], P, np.array([3, 4, 5]), 2)
    assert np.array_equal(uniforms(BASE, "s", ["e"], P, np.array([4]), 2)[:, 0], full[:, 1])
    assert np.array_equal(uniforms(BASE, "s", ["e"], P[[10, 3]], np.array([3, 4, 5]), 2), full[[10, 3]])


def test_sources_bases_and_entities_give_different_streams() -> None:
    m = np.array([0])
    ref = uniforms(BASE, "a", ["e"], P, m, 4)
    assert not np.array_equal(ref, uniforms(BASE, "b", ["e"], P, m, 4))
    assert not np.array_equal(ref, uniforms(base_entropy(8, Plane.SEARCH, "M1"), "a", ["e"], P, m, 4))
    assert not np.array_equal(ref, uniforms(BASE, "a", ["f"], P, m, 4))
    assert not np.array_equal(ref, uniforms(BASE, "a", [None], P, m, 4))


def test_empty_axes_are_allowed() -> None:
    assert uniforms(BASE, "s", [], P, np.array([0]), 1).shape == (64, 1, 0, 1)
    assert uniforms(BASE, "s", ["e"], np.array([], dtype=np.int64), np.array([0]), 1).shape == (0, 1, 1, 1)


@pytest.mark.parametrize("kwargs", [
    {"base": b"x" * 15}, {"source": ""}, {"entity_ids": "SYN-PE-0001"}, {"entity_ids": [""]},
    {"paths": np.array([-1, 0])}, {"paths": np.array([0.5])}, {"paths": np.zeros((2, 2), dtype=np.int64)},
    {"months": np.array([-3])}, {"slots": 0}, {"slots": 2.0}, {"slots": True},
])
def test_rejects_malformed_arguments(kwargs: dict) -> None:
    args = {"base": BASE, "source": "s", "entity_ids": ["e"], "paths": P, "months": np.array([0]), "slots": 2}
    args.update(kwargs)
    with pytest.raises(SchemaError):
        uniforms(**args)


def _requests() -> list[NoiseRequest]:
    return [
        NoiseRequest(source="priv.fund.idio", slots=3, entity_ids=("SYN-PE-0001", "SYN-PE-0002"), months=(9, 10, 11)),
        NoiseRequest(source="sale.success", slots=1, entity_ids=None, months=(9,)),
        NoiseRequest(source="priv.company.ev", slots=4, entity_ids=("SYN-CMP-000417",), months=(9, 10, 11)),
    ]


def test_draw_block_returns_a_valid_noise_slice_equal_to_uniforms() -> None:
    paths = np.arange(2000, 2000 + 300)
    ns = draw_block(BASE, _requests(), paths)
    assert isinstance(ns, NoiseSlice)
    ns.validate()                                            # shapes, dtype, finiteness and [0, 1) per ARRAY_SPECS
    for req in _requests():
        ents = (None,) if req.entity_ids is None else req.entity_ids
        expected = uniforms(BASE, req.source, ents, paths, np.array(req.months), req.slots)
        assert np.array_equal(ns.u[req.source], expected)
        assert not ns.u[req.source].flags.writeable          # the frozen slice owns read-only views
    assert ns.u["sale.success"].shape == (300, 1, 1, 1)


def test_draw_block_rules() -> None:
    reqs = _requests()
    with pytest.raises(SchemaError):
        draw_block(BASE, [reqs[0], reqs[0]], P)                # a duplicate source would reuse a stream
    with pytest.raises(SchemaError):
        draw_block(BASE, reqs, np.arange(MAX_BLOCK_PATHS + 1))  # one block at most (§1.5)
    with pytest.raises(SchemaError):
        draw_block(BASE, [{"source": "x"}], P)  # type: ignore[list-item]
    assert draw_block(BASE, reqs, np.arange(MAX_BLOCK_PATHS)).u["priv.fund.idio"].shape == (2000, 3, 2, 3)
    empty = NoiseRequest(source="none", slots=2, entity_ids=None, months=())
    assert draw_block(BASE, [empty], P).u["none"].shape == (64, 0, 1, 2)
