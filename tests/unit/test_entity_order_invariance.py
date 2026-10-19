"""Entity-order invariance (BUILD_SPEC v1.1 §4.2 tests; §1.7: results cannot depend on entity order). Owner WP-02.

Each entity reads its own keyed stream, so permuting, subsetting or splitting the entity list permutes the entity
axis bit for bit, and the order of a step's requests does not matter. SYNTHETIC ids only.
"""

from __future__ import annotations

import numpy as np

from adic_tpa.contracts.engine_io import NoiseRequest
from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import base_entropy, draw_block, uniforms

BASE = base_entropy(42, Plane.SEARCH, "M6")
IDS = [f"SYN-PE-{i:04d}" for i in range(1, 41)] + [None]
PATHS = np.arange(500, 700)
MONTHS = np.array([12, 13, 14])


def test_permuting_entities_permutes_the_entity_axis() -> None:
    ref = uniforms(BASE, "priv.fund.idio", IDS, PATHS, MONTHS, 6)
    gen = np.random.Generator(np.random.Philox(3))
    for _ in range(5):
        perm = gen.permutation(len(IDS))
        got = uniforms(BASE, "priv.fund.idio", [IDS[i] for i in perm], PATHS, MONTHS, 6)
        assert np.array_equal(got, ref[:, :, perm, :])


def test_subsets_and_splits_read_the_same_columns() -> None:
    ref = uniforms(BASE, "priv.fund.idio", IDS, PATHS, MONTHS, 2)
    picks = [5, 0, 40, 17]
    assert np.array_equal(uniforms(BASE, "priv.fund.idio", [IDS[i] for i in picks], PATHS, MONTHS, 2),
                          ref[:, :, picks, :])
    halves = [uniforms(BASE, "priv.fund.idio", part, PATHS, MONTHS, 2) for part in (IDS[:13], IDS[13:])]
    assert np.array_equal(np.concatenate(halves, axis=2), ref)


def test_request_order_does_not_matter() -> None:
    reqs = [NoiseRequest(source="a", slots=2, entity_ids=tuple(IDS[:10]), months=(12,)),   # type: ignore[arg-type]
            NoiseRequest(source="b", slots=1, entity_ids=None, months=(12, 13)),
            NoiseRequest(source="c", slots=5, entity_ids=tuple(IDS[10:20]), months=(14,))]  # type: ignore[arg-type]
    fwd = draw_block(BASE, reqs, PATHS)
    rev = draw_block(BASE, reqs[::-1], PATHS)
    for src in ("a", "b", "c"):
        assert np.array_equal(fwd.u[src], rev.u[src])
