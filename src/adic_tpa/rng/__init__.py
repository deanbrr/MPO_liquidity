"""Counter-based keyed random numbers (BUILD_SPEC v1.1 §1.7, §4.2; owner WP-02, wave 0).

Common random numbers by construction, independent of thread count, block size and entity order: every uniform is
a pure function of (base, source, entity, path, month, slot) through SHA-256-keyed Philox4x64-10 streams
(S-ADR-25, S-ADR-38). ``keys`` derives the bases and stream keys, ``philox`` holds the generator, ``streams`` the
uniform arrays and per-block ``NoiseSlice`` draws, ``samplers`` the inverse-CDF transforms. ``rng`` imports only
``contracts`` and ``numerics`` (§4.0).

SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

import numpy as np

from adic_tpa.rng.keys import (
    BASE_BYTES, MISSPEC_WORLD_BASE, PLANE_CODE, WORLD_CODE, base_entropy, check_base, entity_key, stream_key,
    stream_keys, world_code,
)
from adic_tpa.rng.philox import PARALLEL_MIN, UNIFORM_SCALE, philox4x64_10
from adic_tpa.rng.samplers import (
    U_MIN, bernoulli, categorical, exponential, gamma, kou_jump, normal, student_t, truncated_t, warm_samplers,
)
from adic_tpa.rng.streams import draw_block, uniforms

__all__ = [
    "PLANE_CODE", "WORLD_CODE", "MISSPEC_WORLD_BASE", "BASE_BYTES", "UNIFORM_SCALE", "U_MIN", "world_code",
    "base_entropy", "entity_key", "stream_key", "stream_keys", "check_base", "philox4x64_10", "uniforms",
    "draw_block", "normal", "student_t", "truncated_t", "gamma", "exponential", "bernoulli", "categorical",
    "kou_jump", "warm_up",
]


def warm_up() -> None:
    """Compile or load every WP-02 kernel from the numba cache (evaluator start, outside the hash checks; §1.13).

    Both the serial and the parallel Philox kernels are touched (outputs below and above ``PARALLEL_MIN``).
    """
    big = PARALLEL_MIN // 4
    for n in (1, big):
        philox4x64_10(np.zeros((n, 4), dtype=np.uint64), np.zeros(2, dtype=np.uint64))
        uniforms(bytes(BASE_BYTES), "warm_up", [None], np.arange(n), np.zeros(1, dtype=np.int64), 4)
    warm_samplers()
