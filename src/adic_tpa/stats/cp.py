"""Clopper–Pearson bounds for event probabilities (BUILD_SPEC v1.1 §4.4; ARCH §5.10).

Certification passes a Tier-1 gate iff the one-sided 95% Clopper–Pearson upper bound on P(event) is within the
class band; at 50,000 paths p̂ = 0.90% passes a 1% gate and p̂ = 1.00% fails. The exact bounds are beta quantiles:
upper = B⁻¹(1 − α; k + 1, n − k) (1 when k = n); two-sided (B⁻¹(α/2; k, n − k + 1), B⁻¹(1 − α/2; k + 1, n − k)).

``is_cp_upper`` serves importance-sampled certification (rare events below 0.5%; ARCH §5.10): with likelihood-ratio
weights w the event rate is the self-normalized p̂ = Σ w·1{event}/Σ w, and the bound is the Clopper–Pearson upper
bound at the Kish effective sample size n_eff = (Σw)²/Σw² with k_eff = p̂·n_eff (non-integer beta parameters). With
equal weights it equals ``clopper_pearson(k, n)`` exactly. (WP-02 reading of "importance-sampled; Kish-effective n".)
"""

from __future__ import annotations

import math
from typing import Literal

import numpy as np
from scipy import special

from adic_tpa.contracts.arrays import B, F64
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.numerics.lse import kish_ess

__all__ = ["clopper_pearson", "is_cp_upper"]


def _check_alpha(alpha: float) -> float:
    a = float(alpha)
    if not 0.0 < a < 1.0:
        raise SchemaError(f"alpha must lie in (0, 1), got {alpha}")
    return a


def _upper(k: float, n: float, alpha: float) -> float:
    return 1.0 if k >= n else float(special.betaincinv(k + 1.0, n - k, 1.0 - alpha))


def clopper_pearson(k: int, n: int, alpha: float = 0.05,
                    side: Literal["upper", "two"] = "upper") -> float | tuple[float, float]:
    """Exact binomial bound(s) for k events in n trials: the one-sided (1 − α) upper bound, or the two-sided
    (1 − α) interval ``(lower, upper)`` with ``side="two"``."""
    a = _check_alpha(alpha)
    if isinstance(k, bool) or isinstance(n, bool) or int(k) != k or int(n) != n or not 0 <= k <= n or n < 1:
        raise SchemaError(f"clopper_pearson: need integers 0 <= k <= n, n >= 1; got k={k}, n={n}")
    k, n = int(k), int(n)
    if side == "upper":
        return _upper(k, n, a)
    if side == "two":
        lower = 0.0 if k == 0 else float(special.betaincinv(k, n - k + 1.0, a / 2.0))
        return lower, _upper(k, n, a / 2.0)
    raise SchemaError(f"clopper_pearson: side must be 'upper' or 'two', got {side!r}")


def is_cp_upper(weights: F64, events: B, alpha: float = 0.05) -> float:
    """One-sided (1 − α) Clopper–Pearson upper bound of an importance-sampled event rate (module docstring)."""
    a = _check_alpha(alpha)
    w = np.asarray(weights, dtype=np.float64)
    e = np.asarray(events)
    if e.dtype != np.bool_:
        raise SchemaError(f"is_cp_upper: events must be a boolean array, got dtype {e.dtype}")
    if w.shape != e.shape or w.ndim != 1:
        raise SchemaError(f"is_cp_upper: weights {w.shape} and events {e.shape} must be equal-length 1-d arrays")
    n_eff = kish_ess(w)
    p_hat = float(w[e].sum() / w.sum())
    k_eff = p_hat * n_eff
    if math.isclose(k_eff, n_eff, rel_tol=1e-15, abs_tol=0.0) or k_eff >= n_eff:
        return 1.0
    return _upper(k_eff, n_eff, a)
