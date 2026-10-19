"""Philox4x64-10 in numba (BUILD_SPEC v1.1 §1.7, §4.2; Salmon, Moraes, Dror & Shaw 2011).

Ten rounds with multipliers ``0xD2E7470EE14C6C93``, ``0xCA5A826395121157`` and Weyl key increments
``0x9E3779B97F4A7C15``, ``0xBB67AE8584CAA73B``. The 64×64→128-bit products come from a numba intrinsic that emits an
LLVM ``i128`` multiply (one hardware multiply on x86-64, ≈ 2.3× faster than forming the product from 32-bit halves);
everything else is wrapping ``uint64`` arithmetic. Uniform = ``(x >> 11) · 2^-53`` ∈ [0, 1): an exact multiple of
2^-53, so the lower and upper tails have the same granularity.

``philox4x64_10(counters, key)`` is the raw bijection. numpy's ``Philox`` bit generator increments its counter
before each block, so ``numpy.random.Philox(counter=c, key=k).random_raw(4)`` equals
``philox4x64_10([c + 1], k)[0]`` (counter words little-endian, carry included); the Random123 known-answer vectors
hold as well. Both are pinned by ``tests/unit/test_philox_numpy_equivalence.py``.

Stream layout (S-ADR-38): the uniform of slot s for (path, month) under a stream key is lane ``s mod 4`` of the
block at counter ``(path, month, ⌊s/4⌋, 0)``, so all four Philox outputs are used. ``fill_uniforms`` writes
[path, month, entity, slot] arrays directly; it loops over paths with ``prange`` and holds no state, so the result
does not depend on the thread count, the block size or the entity order. Outputs below ``PARALLEL_MIN`` values run
the same inlined body on one thread: a parallel launch costs ≈ 30 µs on an idle 24-core machine and milliseconds
when the machine is oversubscribed, more than the work itself. Measured on the build machine (24
cores), 4-slot requests: ≈ 420M uniforms/s on one thread and ≈ 4.7G/s on 24 for the kernel, ≈ 310M/s and ≈ 1.6G/s
including the output allocation; a 1-slot request uses one lane per counter (the §1.7 layout), ≈ 120M/s and
≈ 1.4G/s for the kernel (§4.2 asks ≥ 100M/s single-threaded with all four lanes; WP-02 DoD ≥ 50M/s).
"""

from __future__ import annotations

from typing import Any, Final

import numba
import numpy as np
from numba import types as nb_types
from numba.extending import intrinsic, overload

from adic_tpa.contracts.arrays import F64, U64
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.numerics.numba_utils import inline_helper, kernel

__all__ = ["PHILOX_M0", "PHILOX_M1", "PHILOX_W0", "PHILOX_W1", "PHILOX_ROUNDS", "UNIFORM_SCALE", "LANES",
           "PARALLEL_MIN", "philox4x64_10", "fill_uniforms"]

PHILOX_M0: Final = np.uint64(0xD2E7470EE14C6C93)
PHILOX_M1: Final = np.uint64(0xCA5A826395121157)
PHILOX_W0: Final = np.uint64(0x9E3779B97F4A7C15)
PHILOX_W1: Final = np.uint64(0xBB67AE8584CAA73B)
PHILOX_ROUNDS: Final = 10
LANES: Final = 4
UNIFORM_SCALE: Final = 2.0 ** -53
PARALLEL_MIN: Final = 1 << 16                  # output values below which the serial twin kernel runs

_SHIFT11 = np.uint64(11)
_ZERO = np.uint64(0)


_MASK64 = (1 << 64) - 1


@intrinsic
def _umul128(typingctx: Any, a: Any, b: Any) -> Any:
    """(low, high) 64-bit words of the 128-bit product a·b of two uint64 (LLVM ``i128`` multiply; jitted code only)."""
    if a != nb_types.uint64 or b != nb_types.uint64:
        return None
    sig = nb_types.UniTuple(nb_types.uint64, 2)(nb_types.uint64, nb_types.uint64)

    def codegen(context: Any, builder: Any, signature: Any, args: Any) -> Any:
        x, y = args
        i64 = x.type
        i128 = type(i64)(128)                          # the IR integer type, without importing llvmlite
        prod = builder.mul(builder.zext(x, i128), builder.zext(y, i128))
        lo = builder.trunc(prod, i64)
        hi = builder.trunc(builder.lshr(prod, i128(64)), i64)
        return context.make_tuple(builder, signature.return_type, (lo, hi))

    return sig, codegen


def _mulhilo(a: np.uint64, b: np.uint64) -> tuple[np.uint64, np.uint64]:
    """(low, high) words of a·b. Python reference, used when a kernel body runs uncompiled (``.py_func``,
    ``NUMBA_DISABLE_JIT``); jitted code resolves the call to ``_umul128`` through the overload below."""
    prod = int(a) * int(b)
    return np.uint64(prod & _MASK64), np.uint64(prod >> 64)


@overload(_mulhilo, inline="always")
def _mulhilo_jit(a, b):  # type: ignore[no-untyped-def]  # numba requires the implementation's exact signature
    if a == nb_types.uint64 and b == nb_types.uint64:
        return lambda a, b: _umul128(a, b)
    return None


@inline_helper
def _round(c0, c1, c2, c3, k0, k1):  # type: ignore[no-untyped-def]
    lo0, hi0 = _mulhilo(PHILOX_M0, c0)
    lo1, hi1 = _mulhilo(PHILOX_M1, c2)
    return hi1 ^ c1 ^ k0, lo1, hi0 ^ c3 ^ k1, lo0


@inline_helper
def _philox(c0, c1, c2, c3, k0, k1):  # type: ignore[no-untyped-def]
    """Philox4x64-10 of one counter: round 1 with the key, then nine (bump key, round) steps."""
    c0, c1, c2, c3 = _round(c0, c1, c2, c3, k0, k1)
    for _ in range(PHILOX_ROUNDS - 1):
        k0 = k0 + PHILOX_W0
        k1 = k1 + PHILOX_W1
        c0, c1, c2, c3 = _round(c0, c1, c2, c3, k0, k1)
    return c0, c1, c2, c3


@inline_helper
def _unit(x):  # type: ignore[no-untyped-def]
    return np.float64(x >> _SHIFT11) * UNIFORM_SCALE


@inline_helper
def _philox_row(i, counters, key, out):  # type: ignore[no-untyped-def]
    x0, x1, x2, x3 = _philox(counters[i, 0], counters[i, 1], counters[i, 2], counters[i, 3], key[0], key[1])
    out[i, 0] = x0
    out[i, 1] = x1
    out[i, 2] = x2
    out[i, 3] = x3


@kernel(parallel=True)
def _philox_kernel(counters, key, out):  # type: ignore[no-untyped-def]
    for i in numba.prange(counters.shape[0]):
        _philox_row(i, counters, key, out)


@kernel()
def _philox_kernel_serial(counters, key, out):  # type: ignore[no-untyped-def]
    for i in range(counters.shape[0]):
        _philox_row(i, counters, key, out)


@inline_helper
def _uniform_path(ip, keys, paths, months, slots, out):  # type: ignore[no-untyped-def]
    """Every uniform of path index ``ip``: months × entities × slots, lane s mod 4 of counter (path, m, ⌊s/4⌋, 0)."""
    c0 = paths[ip]
    for im in range(months.shape[0]):
        c1 = months[im]
        for ie in range(keys.shape[0]):
            k0 = keys[ie, 0]
            k1 = keys[ie, 1]
            for g in range((slots + 3) // 4):
                x0, x1, x2, x3 = _philox(c0, c1, np.uint64(g), _ZERO, k0, k1)
                s = 4 * g
                out[ip, im, ie, s] = _unit(x0)
                if s + 1 < slots:
                    out[ip, im, ie, s + 1] = _unit(x1)
                if s + 2 < slots:
                    out[ip, im, ie, s + 2] = _unit(x2)
                if s + 3 < slots:
                    out[ip, im, ie, s + 3] = _unit(x3)


@kernel(parallel=True)
def _uniform_kernel(keys, paths, months, slots, out):  # type: ignore[no-untyped-def]
    for ip in numba.prange(paths.shape[0]):
        _uniform_path(ip, keys, paths, months, slots, out)


@kernel()
def _uniform_kernel_serial(keys, paths, months, slots, out):  # type: ignore[no-untyped-def]
    for ip in range(paths.shape[0]):
        _uniform_path(ip, keys, paths, months, slots, out)


def _as_u64_matrix(a: np.ndarray, cols: int, name: str) -> U64:
    arr = np.asarray(a)
    if arr.ndim != 2 or arr.shape[1] != cols:
        raise SchemaError(f"{name}: expected shape [N, {cols}], got {arr.shape}")
    if arr.dtype != np.uint64:
        if arr.dtype.kind not in "iu" or (arr.size and arr.min() < 0):
            raise SchemaError(f"{name}: expected unsigned 64-bit words, got dtype {arr.dtype}")
        arr = arr.astype(np.uint64)
    return np.ascontiguousarray(arr)


def philox4x64_10(counters: np.ndarray, key: np.ndarray) -> U64:
    """Philox4x64-10 bijection: counters U64[N, 4] (word 0 first) under key U64[2] -> U64[N, 4].

    Parallel numba kernel (pure; any thread count gives the same output).
    """
    ctr = _as_u64_matrix(counters, 4, "philox4x64_10 counters")
    k = _as_u64_matrix(np.asarray(key).reshape(1, -1), 2, "philox4x64_10 key")[0]
    out = np.empty((ctr.shape[0], 4), dtype=np.uint64)
    (_philox_kernel if out.size >= PARALLEL_MIN else _philox_kernel_serial)(ctr, k, out)
    return out


def fill_uniforms(keys: U64, paths: U64, months: U64, slots: int) -> F64:
    """Uniforms [len(paths), len(months), len(keys), slots] for stream keys U64[E, 2] (validated by the caller)."""
    out = np.empty((paths.shape[0], months.shape[0], keys.shape[0], slots), dtype=np.float64)
    (_uniform_kernel if out.size >= PARALLEL_MIN else _uniform_kernel_serial)(keys, paths, months, slots, out)
    return out
