"""Weights: log-sum-exp normalization, Kish effective sample size and weighted quantiles (BUILD_SPEC v1.1 §4.3).

Used wherever paths carry probability or likelihood-ratio weights: tree leaves (``adaptive_tangent_points``),
importance-sampled certification (``stats.is_cp_upper``), entropy pooling and the one ESS rule (ARCH §4.12, §8.4).

``weighted_quantile`` interpolates linearly between the order statistics at plotting positions
``p_k = (M_k − M_1)/(M_n − M_1)``, where ``M_k = C_k − w_k/2`` is the weighted mid-point CDF of the sorted sample.
With equal weights ``p_k = (k − 1)/(n − 1)``, so it reproduces ``numpy.quantile``'s default (linear, type 7)
exactly; positions are symmetric under reversing the sample; zero-weight observations are ignored (WP-02 choice:
§4.3 fixes only the equal-weight case).
"""

from __future__ import annotations

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.errors import SchemaError

__all__ = ["logsumexp_weights", "kish_ess", "weighted_quantile"]


def _weights(w: F64, name: str) -> F64:
    arr = np.asarray(w, dtype=np.float64)
    if arr.ndim != 1:
        raise SchemaError(f"{name}: weights must be 1-d, got shape {arr.shape}")
    if not np.isfinite(arr).all() or (arr < 0).any():
        raise SchemaError(f"{name}: weights must be finite and non-negative")
    if not arr.sum() > 0:
        raise SchemaError(f"{name}: weights must have a positive sum")
    return arr


def logsumexp_weights(logw: F64) -> F64:
    """Normalized weights ``exp(logw) / Σ exp(logw)``, computed stably (shifted by the maximum).

    ``-inf`` entries get weight 0; NaN, ``+inf`` or an all-``-inf`` input raise ``SchemaError``.
    """
    lw = np.asarray(logw, dtype=np.float64)
    if lw.ndim != 1 or lw.size == 0:
        raise SchemaError(f"logsumexp_weights: expected a non-empty 1-d array, got shape {lw.shape}")
    if np.isnan(lw).any() or np.isposinf(lw).any():
        raise SchemaError("logsumexp_weights: NaN or +inf log-weight")
    top = lw.max()
    if not np.isfinite(top):
        raise SchemaError("logsumexp_weights: every log-weight is -inf")
    w = np.exp(lw - top)
    return w / w.sum()


def kish_ess(w: F64) -> float:
    """Kish effective sample size ``(Σw)² / Σw²`` of non-negative weights (unnormalized weights are fine)."""
    arr = _weights(w, "kish_ess")
    return float(arr.sum() ** 2 / np.dot(arr, arr))


def weighted_quantile(x: F64, w: F64, q: float | F64) -> F64:
    """Weighted quantile(s) of ``x`` at probability level(s) ``q`` in [0, 1] (module docstring for the rule).

    Returns a numpy float64 scalar for a scalar ``q`` and an array of ``q``'s shape otherwise, like
    ``numpy.quantile``, which it equals for equal weights.
    """
    xs = np.asarray(x, dtype=np.float64)
    ws = _weights(w, "weighted_quantile")
    if xs.shape != ws.shape:
        raise SchemaError(f"weighted_quantile: x shape {xs.shape} != w shape {ws.shape}")
    if not np.isfinite(xs).all():
        raise SchemaError("weighted_quantile: x must be finite")
    qs = np.asarray(q, dtype=np.float64)
    if not np.isfinite(qs).all() or (qs < 0).any() or (qs > 1).any():
        raise SchemaError("weighted_quantile: q must lie in [0, 1]")
    keep = ws > 0
    xs, ws = xs[keep], ws[keep]
    order = np.argsort(xs, kind="stable")
    xs, ws = xs[order], ws[order]
    if xs.size == 1:
        out = np.full(qs.shape, xs[0])
    else:
        mid = np.cumsum(ws) - 0.5 * ws
        pos = (mid - mid[0]) / (mid[-1] - mid[0])
        pos[-1] = 1.0
        out = np.interp(qs, pos, xs)
    return out[()] if qs.ndim == 0 else out
