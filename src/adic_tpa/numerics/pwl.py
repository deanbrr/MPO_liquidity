"""Piecewise-linear proxies of the Tier-2 objective and its exact value (BUILD_SPEC v1.1 §4.3, §5.3, §5.11; A8).

H maximizes Σ_ℓ p_ℓ [u_ℓ − λ^H_T ψ_ℓ] with u_ℓ under the tangents of U_γ(x) = x^{1−γ}/(1−γ) (log x at γ = 1)
evaluated at real terminal wealth x = W̃^real_ℓ/W₀, and ψ_ℓ over the secants of ((1 − W̃_ℓ/W̃*_ℓ)⁺)^p (§5.3 UTILITY
and SHORTFALL rows). Wealth arguments are in W₀ units (multiples of opening NAV), so utilities are dimensionless.

- ``crra_tangents``: slopes a_k = U′(x_k) = x_k^{−γ} and intercepts b_k = U(x_k) − a_k x_k, one cut u ≤ a_k x + b_k
  per point. Tangents of a concave function lie above it and touch it at the points.
- ``adaptive_tangent_points``: n weighted quantiles of the previous solve's leaf wealth at levels evenly spaced on
  [lo_q, hi_q] (P1–P99 by default); with the defaults 38 of 48 points fall inside the weighted P10–P90.
- ``pwl_power``: the convex PWL of (x⁺)^p in secant form on ``breaks`` (which start at 0): piece 0 is the flat piece
  ψ ≥ 0 left of the kink, piece j ≥ 1 the secant through breaks j−1 and j. So there are ``len(breaks)`` pieces, the
  per-leaf SHORTFALL row count of §5.3 (6 for the default breaks); beyond the last break the last secant extends.
- ``tangent_error_bound``: max over consecutive points of h_k² max|U″|/8 on [x_k, x_{k+1}], where |U″| = γx^{−γ−1}
  peaks at x_k; it bounds the tangent proxy's overestimate of U between the outermost points (reported beside Γ,
  never a gate; A8). On the critique's eight points (0.60 … 2.00) at γ = 3 it is 0.065 utility units.
- ``exact_objective``: Σ_ℓ p_ℓ [U_γ(W̃^real_ℓ) − λ ((1 − W̃_ℓ/W̃*_ℓ)⁺)^p], the H objective with exact U and ψ, at the
  solution's leaf wealth (``HSolution.exact_objective``; A8).
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.numerics.lse import weighted_quantile

__all__ = ["crra_utility", "crra_tangents", "adaptive_tangent_points", "pwl_power", "tangent_error_bound",
           "exact_objective"]


def _check_gamma(gamma: float) -> float:
    g = float(gamma)
    if not (np.isfinite(g) and g > 0):
        raise SchemaError(f"CRRA gamma must be positive and finite, got {gamma}")
    return g


def _positive_points(points: Sequence[float] | F64, name: str) -> F64:
    x = np.asarray(points, dtype=np.float64)
    if x.ndim != 1 or x.size == 0:
        raise SchemaError(f"{name}: expected a non-empty 1-d sequence of points")
    if not np.isfinite(x).all() or (x <= 0).any():
        raise SchemaError(f"{name}: CRRA points must be finite and positive (wealth in W0 units)")
    return x


def crra_utility(x: F64 | float, gamma: float) -> F64:
    """U_γ(x) = x^{1−γ}/(1−γ), or log x at γ = 1; x is wealth in W₀ units (x > 0)."""
    g = _check_gamma(gamma)
    xs = np.asarray(x, dtype=np.float64)
    if (xs <= 0).any():
        raise SchemaError("crra_utility: wealth must be positive")
    return np.log(xs) if g == 1.0 else np.power(xs, 1.0 - g) / (1.0 - g)


def crra_tangents(points: Sequence[float], gamma: float) -> tuple[F64, F64]:
    """``(slopes, intercepts)`` of the tangent cuts u ≤ a_k x + b_k of U_γ at ``points`` (W₀ units, in input order)."""
    g = _check_gamma(gamma)
    x = _positive_points(points, "crra_tangents")
    slopes = np.power(x, -g)
    intercepts = crra_utility(x, g) - slopes * x
    return slopes, intercepts


def adaptive_tangent_points(leaf_wealth: F64, weights: F64, n: int = 48, lo_q: float = 0.01,
                            hi_q: float = 0.99) -> F64:
    """``n`` tangent points at the weighted quantiles of leaf wealth (W₀ units) at levels linspace(lo_q, hi_q, n).

    The points are non-decreasing; atoms in the leaf distribution can repeat a point (a repeated tangent is a
    redundant row). Raises ``SchemaError`` if a point is not positive (CRRA needs positive wealth).
    """
    if n < 1:
        raise SchemaError(f"adaptive_tangent_points: n must be >= 1, got {n}")
    if not 0.0 <= lo_q <= hi_q <= 1.0:
        raise SchemaError(f"adaptive_tangent_points: need 0 <= lo_q <= hi_q <= 1, got {lo_q}, {hi_q}")
    levels = np.linspace(lo_q, hi_q, n)
    pts = np.asarray(weighted_quantile(leaf_wealth, weights, levels), dtype=np.float64)
    if (pts <= 0).any():
        raise SchemaError("adaptive_tangent_points: a tangent point is not positive; CRRA needs positive leaf wealth")
    return pts


def pwl_power(breaks: Sequence[float], p: float) -> tuple[F64, F64]:
    """``(slopes, intercepts)`` of the convex PWL of (x⁺)^p in secant form: ψ ≥ s_j x + t_j for every piece j.

    ``breaks`` must be strictly increasing and start at 0; ``p >= 1``. Returns ``len(breaks)`` pieces: the flat
    piece (0, 0) and one secant per consecutive pair of breaks (module docstring).
    """
    b = np.asarray(breaks, dtype=np.float64)
    if b.ndim != 1 or b.size < 2:
        raise SchemaError("pwl_power: need at least two breaks")
    if not np.isfinite(b).all() or b[0] != 0.0 or (np.diff(b) <= 0).any():
        raise SchemaError(f"pwl_power: breaks must be finite, strictly increasing and start at 0, got {b.tolist()}")
    pp = float(p)
    if not (np.isfinite(pp) and pp >= 1.0):
        raise SchemaError(f"pwl_power: exponent must be >= 1 (convexity), got {p}")
    fb = np.power(b, pp)
    sec_slopes = np.diff(fb) / np.diff(b)
    sec_intercepts = fb[:-1] - sec_slopes * b[:-1]
    return np.concatenate(([0.0], sec_slopes)), np.concatenate(([0.0], sec_intercepts))


def tangent_error_bound(points: Sequence[float], gamma: float) -> float:
    """Bound on the tangent proxy's error between the outermost points: max_k h_k² γ x_k^{−γ−1}/8 (utility units)."""
    g = _check_gamma(gamma)
    x = np.unique(_positive_points(points, "tangent_error_bound"))
    if x.size < 2:
        raise SchemaError("tangent_error_bound: need at least two distinct points")
    h = np.diff(x)
    return float(np.max(h * h * g * np.power(x[:-1], -g - 1.0) / 8.0))


def exact_objective(w_tilde: F64, w_tilde_real: F64, p: F64, gamma: float, lam_T: float, w_star: F64,
                    p_exp: float) -> float:
    """Exact H objective Σ_ℓ p_ℓ [U_γ(w̃^real_ℓ) − λ_T ((1 − w̃_ℓ/w̃*_ℓ)⁺)^p_exp] at the leaves (dimensionless).

    Units: ``w_tilde``, ``w_tilde_real`` and ``w_star`` are terminal and target wealth in W₀ units (``w_star`` may be
    a scalar or one target per leaf); ``p`` are leaf probabilities; ``lam_T`` is λ^H_T.
    """
    g = _check_gamma(gamma)
    w = np.asarray(w_tilde, dtype=np.float64)
    wr = np.asarray(w_tilde_real, dtype=np.float64)
    pr = np.asarray(p, dtype=np.float64)
    ws = np.broadcast_to(np.asarray(w_star, dtype=np.float64), w.shape)
    if w.ndim != 1 or wr.shape != w.shape or pr.shape != w.shape:
        raise SchemaError(f"exact_objective: shapes differ (w {w.shape}, real {wr.shape}, p {pr.shape})")
    if not (np.isfinite(w).all() and np.isfinite(wr).all() and np.isfinite(pr).all() and np.isfinite(ws).all()):
        raise SchemaError("exact_objective: non-finite input")
    if (pr < 0).any() or (ws <= 0).any():
        raise SchemaError("exact_objective: probabilities must be non-negative and targets positive")
    if not (np.isfinite(lam_T) and lam_T >= 0) or not (np.isfinite(p_exp) and p_exp > 0):
        raise SchemaError(f"exact_objective: need lam_T >= 0 and p_exp > 0, got {lam_T}, {p_exp}")
    shortfall = np.power(np.maximum(1.0 - w / ws, 0.0), float(p_exp))
    return float(np.dot(pr, crra_utility(wr, g) - float(lam_T) * shortfall))
