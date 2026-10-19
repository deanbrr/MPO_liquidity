"""numba conventions shared by the WP-02 kernels (BUILD_SPEC v1.1 §1.13, S-ADR-42).

Every kernel is compiled with ``cache=True`` (the evaluator points ``NUMBA_CACHE_DIR`` at a per-plane directory
and warms the kernels at start-up, outside the hash checks), ``fastmath=False`` (no reassociation, so results are
bit-reproducible), ``error_model="numpy"`` (no Python zero-division checks inside hot loops) and ``nogil=True``.
``parallel=True`` is used only for loops over paths in kernels that hold no RNG state (§1.13), so results never
depend on the thread count.

numba caches a kernel against its own source file only. Jitted helpers that a cached kernel inlines therefore live
in the kernel's own module (``rng.philox``, ``rng.samplers``), never here, so editing a helper always invalidates
the cache of the kernels that use it.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator, Mapping
from types import MappingProxyType
from typing import Any, Final, TypeVar

import numba
from numba.core import config as _numba_config

__all__ = ["KERNEL_OPTIONS", "kernel", "inline_helper", "numba_threads", "max_threads", "current_threads"]

_Fn = TypeVar("_Fn", bound=Callable[..., Any])

# The options of every cached WP-02 kernel (§1.13). Recorded here so manifests can cite one place.
KERNEL_OPTIONS: Final[Mapping[str, Any]] = MappingProxyType(
    {"cache": True, "fastmath": False, "error_model": "numpy", "nogil": True})


def kernel(*, parallel: bool = False) -> Callable[[_Fn], _Fn]:
    """Decorator: ``numba.njit`` with :data:`KERNEL_OPTIONS`; ``parallel=True`` only for loops over paths."""
    return numba.njit(parallel=parallel, **KERNEL_OPTIONS)  # type: ignore[no-any-return]


def inline_helper(fn: _Fn) -> _Fn:
    """Decorator for small jitted helpers that kernels inline at the numba IR level (not cached on their own)."""
    return numba.njit(inline="always", fastmath=False, error_model="numpy")(fn)  # type: ignore[no-any-return]


def max_threads() -> int:
    """``NUMBA_NUM_THREADS``: the size of numba's thread pool (recorded in manifests, §1.13)."""
    return int(_numba_config.NUMBA_NUM_THREADS)


def current_threads() -> int:
    """The number of threads numba currently uses for ``prange`` loops."""
    return int(numba.get_num_threads())


@contextlib.contextmanager
def numba_threads(n: int) -> Iterator[int]:
    """Run a block with numba using ``min(n, NUMBA_NUM_THREADS)`` threads; restore the previous count after.

    Used by the determinism suite (1, 4 and 8 threads, §10.6). Yields the thread count actually set.
    """
    if n < 1:
        raise ValueError(f"thread count must be >= 1, got {n}")
    previous = current_threads()
    numba.set_num_threads(min(n, max_threads()))
    try:
        yield current_threads()
    finally:
        numba.set_num_threads(previous)
