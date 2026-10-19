"""CVaR and the buffered probability of exceedance (BUILD_SPEC v1.1 §4.4; S-ADR-07; Rockafellar & Uryasev 2002;
Mafusalov & Uryasev 2018).

Convention: ``x`` is a loss (larger is worse) with optional probability weights ``w`` (normalized internally) and
``alpha`` is the confidence level, so ``cvar(x, 0.95)`` is the mean of the worst 5% of outcomes. For a lower-tail
measure of a return (e.g. the CVaR₁₀% of a 10-year TWR) pass −return and α = 0.90 and negate the result.

- ``cvar(x, α)`` = VaR_α + E[(x − VaR_α)⁺]/(1 − α), VaR_α the lower α-quantile; exact for discrete distributions
  (an atom at VaR is split), and E[x] at α = 0.
- ``bpoe(x, z)`` = min_{a ≥ 0} E[(a(x − z) + 1)⁺] = min(1, min_{c < z} E[(x − c)⁺]/(z − c)): 1 for z ≤ E[x], P(x = max)
  at z = max x, 0 above it, and 1 − α where CVaR_α = z in between, so bPOE(CVaR_α) = 1 − α and bPOE ≥ P(x > z).
  The minimum over c is attained at a sample point (the ratio is monotone between them), found in O(n log n).
"""

from __future__ import annotations

import math

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.errors import SchemaError

__all__ = ["cvar", "bpoe"]


def _sorted_sample(x: F64, w: F64 | None, name: str) -> tuple[F64, F64]:
    xs = np.asarray(x, dtype=np.float64)
    if xs.ndim != 1 or xs.size == 0 or not np.isfinite(xs).all():
        raise SchemaError(f"{name}: x must be a non-empty finite 1-d array")
    if w is None:
        ps = np.full(xs.size, 1.0 / xs.size)
    else:
        ps = np.asarray(w, dtype=np.float64)
        if ps.shape != xs.shape or not np.isfinite(ps).all() or (ps < 0).any() or not ps.sum() > 0:
            raise SchemaError(f"{name}: w must be finite, non-negative, with a positive sum and the shape of x")
        ps = ps / ps.sum()
    order = np.argsort(xs, kind="stable")
    return xs[order], ps[order]


def cvar(x: F64, alpha: float, w: F64 | None = None) -> float:
    """Conditional value at risk of the loss ``x`` at confidence ``alpha`` ∈ [0, 1) (mean of the worst 1 − α)."""
    if not 0.0 <= alpha < 1.0:
        raise SchemaError(f"cvar: alpha must lie in [0, 1), got {alpha}")
    xs, ps = _sorted_sample(x, w, "cvar")
    i = min(int(np.searchsorted(np.cumsum(ps), alpha, side="left")), xs.size - 1)
    var = xs[i]
    return float(var + np.dot(ps, np.maximum(xs - var, 0.0)) / (1.0 - alpha))


def bpoe(x: F64, threshold: float, w: F64 | None = None) -> float:
    """Buffered probability that the loss ``x`` exceeds ``threshold`` (module docstring)."""
    z = float(threshold)
    if not math.isfinite(z):
        raise SchemaError(f"bpoe: threshold must be finite, got {threshold}")
    xs, ps = _sorted_sample(x, w, "bpoe")
    if z <= float(np.dot(ps, xs)):
        return 1.0
    # suffix sums over the sorted sample: S_p[k] = Σ_{j≥k} p_j, S_px[k] = Σ_{j≥k} p_j (x_j − x_ref)
    ref = xs[-1]
    s_p = np.concatenate((np.cumsum(ps[::-1])[::-1], [0.0]))
    s_px = np.concatenate((np.cumsum((ps * (xs - ref))[::-1])[::-1], [0.0]))
    cand = np.flatnonzero(xs < z)            # non-empty: z > E[x] ≥ min x
    # E[(x − c)⁺] at c = x_i: Σ_{j>i} p_j (x_j − x_i) = S_px[i+1] + S_p[i+1]·(ref − x_i); ties at x_i add zero
    c = xs[cand]
    excess = s_px[cand + 1] + s_p[cand + 1] * (ref - c)
    return float(min(1.0, np.min(np.maximum(excess, 0.0) / (z - c))))
