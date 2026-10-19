"""Paired bootstrap of a mean difference on common random numbers (BUILD_SPEC v1.1 §4.4; ARCH §7.6 Gates 2–3).

``paired_bootstrap(diff)`` resamples the per-path paired differences (candidate − comparator on CRN paths):
i.i.d. when ``block`` is None, otherwise the circular block bootstrap of Politis & Romano (1992) with blocks of
``block`` consecutive observations (every observation is equally likely to be drawn). It returns the sample mean,
the bootstrap standard error (standard deviation of the replicate means, ddof = 1) and percentile bounds.

``lcb``/``ucb`` are one-sided bounds, each at confidence ``level``: the (1 − level) and ``level`` quantiles of the
replicate means (WP-02 reading: GateSpec.lcb_level = 0.95 asks for a one-sided LCB95, e.g. Gate 3's Holm-adjusted
LCB95(ΔΨ) > ε_mat; [lcb, ucb] is then a two-sided (2·level − 1) interval).

Replicates are drawn by numpy's ``Generator(Philox(seed))`` (stats may not import ``rng``, §4.0), in chunks of at
most ~2M resampled values so memory stays bounded at 10,000 paths × 2,000 replicates.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.errors import SchemaError

__all__ = ["BootstrapResult", "paired_bootstrap"]

_CHUNK_VALUES: Final = 2_000_000


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    """Mean, bootstrap SE and one-sided percentile bounds (each at the requested level), in the units of ``diff``."""

    mean: float
    se: float
    lcb: float
    ucb: float


def paired_bootstrap(diff: F64, *, n_boot: int = 2000, block: int | None = None, level: float = 0.95,
                     seed: int = 0) -> BootstrapResult:
    """Bootstrap the mean of paired differences (module docstring). Same seed, same result."""
    d = np.asarray(diff, dtype=np.float64)
    if d.ndim != 1 or d.size < 2:
        raise SchemaError(f"paired_bootstrap: need a 1-d array of at least 2 differences, got shape {d.shape}")
    if not np.isfinite(d).all():
        raise SchemaError("paired_bootstrap: differences must be finite (failed paths are scored, never dropped)")
    if n_boot < 2:
        raise SchemaError(f"paired_bootstrap: n_boot must be >= 2, got {n_boot}")
    if not 0.5 < level < 1.0:
        raise SchemaError(f"paired_bootstrap: level must lie in (0.5, 1), got {level}")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise SchemaError(f"paired_bootstrap: seed must be a non-negative int, got {seed!r}")
    n = d.size
    if block is not None and not 1 <= block <= n:
        raise SchemaError(f"paired_bootstrap: block must lie in [1, {n}], got {block}")
    gen = np.random.Generator(np.random.Philox(seed))
    chunk = max(1, _CHUNK_VALUES // n)
    means = np.empty(n_boot, dtype=np.float64)
    if block is None or block == 1:
        for start in range(0, n_boot, chunk):
            m = min(chunk, n_boot - start)
            means[start:start + m] = d[gen.integers(0, n, size=(m, n))].mean(axis=1)
    else:
        n_blocks = math.ceil(n / block)
        offsets = np.arange(block)
        for start in range(0, n_boot, chunk):
            m = min(chunk, n_boot - start)
            starts = gen.integers(0, n, size=(m, n_blocks))
            idx = ((starts[:, :, None] + offsets) % n).reshape(m, n_blocks * block)[:, :n]
            means[start:start + m] = d[idx].mean(axis=1)
    lcb, ucb = np.quantile(means, [1.0 - level, level])
    return BootstrapResult(mean=float(d.mean()), se=float(means.std(ddof=1)), lcb=float(lcb), ucb=float(ucb))
