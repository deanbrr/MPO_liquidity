"""Keyed uniform streams and per-block draws (BUILD_SPEC v1.1 §1.7, §4.2).

``uniforms(base, source, entity_ids, paths, months, slots)`` returns float64 uniforms in [0, 1) shaped
[len(paths), len(months), len(entity_ids), slots]: entry (p, m, e, s) is lane s mod 4 of Philox4x64-10 at counter
(paths[p], months[m], ⌊s/4⌋, 0) under ``stream_key(base, source, entity_key(entity_ids[e]))``. Paths and months are
absolute indices (a block passes its path offset + 0…1,999), so every uniform is a pure function of (base, source,
entity, path, month, slot): common random numbers hold across policies by construction, and results cannot depend
on the block size, the thread count or the entity order (§1.7). Two entities with the same id read the same stream,
which is how every claim on one company reads one EV draw per path (gate V24a).

``draw_block(base, requests, paths)`` generates every ``NoiseRequest`` of a step before the engine kernels run and
returns the ``NoiseSlice`` the engines read (§1.3 step order; no kernel holds RNG state). A request with
``entity_ids=None`` is one stream with entity key 0. Sources must be unique within a block, and a block holds at most
``MAX_BLOCK_PATHS`` paths (§1.5). Stream keys are memoized across the block's quarterly calls (``rng.keys``).
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from adic_tpa.contracts.arrays import F64, MAX_BLOCK_PATHS, U64
from adic_tpa.contracts.engine_io import NoiseRequest, NoiseSlice
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.rng.keys import check_base, stream_keys
from adic_tpa.rng.philox import fill_uniforms

__all__ = ["uniforms", "draw_block"]


def _index_array(a: np.ndarray | Sequence[int], name: str) -> U64:
    arr = np.asarray(a)
    if arr.ndim != 1:
        raise SchemaError(f"{name}: expected a 1-d array of indices, got shape {arr.shape}")
    if arr.size == 0:
        return np.zeros(0, dtype=np.uint64)
    if arr.dtype.kind not in "iu":
        raise SchemaError(f"{name}: indices must be integers, got dtype {arr.dtype}")
    if arr.dtype.kind == "i" and arr.min() < 0:
        raise SchemaError(f"{name}: indices must be non-negative (absolute path and month indices)")
    return np.ascontiguousarray(arr, dtype=np.uint64)


def uniforms(base: bytes, source: str, entity_ids: Sequence[str | None], paths: np.ndarray, months: np.ndarray,
             slots: int) -> F64:
    """Keyed uniforms [len(paths), len(months), len(entity_ids), slots] in [0, 1) (module docstring).

    Raises ``SchemaError`` on a malformed base, source, entity id, index array or slot count.
    """
    b = check_base(base)
    if isinstance(slots, bool) or not isinstance(slots, int | np.integer) or slots < 1:
        raise SchemaError(f"slots must be an integer >= 1, got {slots!r}")
    if isinstance(entity_ids, str):
        raise SchemaError("entity_ids must be a sequence of ids, not a single string")
    keys = stream_keys(b, source, entity_ids)
    return fill_uniforms(keys, _index_array(paths, "paths"), _index_array(months, "months"), int(slots))


def draw_block(base: bytes, requests: Sequence[NoiseRequest], paths: np.ndarray) -> NoiseSlice:
    """Every request's uniforms for one block of paths, as a ``NoiseSlice`` (u[source]: [P, n_months, n_ent, slots]).

    The slice is valid by construction and is not re-validated here (a full pass over the arrays would cost more
    than drawing them); tests and callers that need the check call ``NoiseSlice.validate()``.
    """
    b = check_base(base)
    p = _index_array(paths, "paths")
    if p.shape[0] > MAX_BLOCK_PATHS:
        raise SchemaError(f"draw_block: a block holds at most {MAX_BLOCK_PATHS} paths (§1.5), got {p.shape[0]}")
    u: dict[str, F64] = {}
    for req in requests:
        if not isinstance(req, NoiseRequest):
            raise SchemaError(f"draw_block: expected NoiseRequest, got {type(req).__name__}")
        if req.source in u:
            raise SchemaError(f"draw_block: duplicate source {req.source!r} in one block (it would reuse a stream)")
        ents: Sequence[str | None] = (None,) if req.entity_ids is None else req.entity_ids
        keys = stream_keys(b, req.source, ents)
        u[req.source] = fill_uniforms(keys, p, _index_array(np.asarray(req.months, dtype=np.int64), "months"),
                                      req.slots)
    return NoiseSlice(requests=tuple(requests), u=u)
