"""Numerical helpers (BUILD_SPEC v1.1 §4.3; owner WP-02, wave 0).

PWL proxies of the Tier-2 objective and its exact value (``pwl``), bracketed root finding (``roots``), the nearest
correlation matrix (``linalg``), weight utilities (``lse``) and the numba kernel conventions (``numba_utils``).
``numerics`` imports only ``contracts`` (§4.0).

SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

from adic_tpa.numerics.linalg import nearest_correlation
from adic_tpa.numerics.lse import kish_ess, logsumexp_weights, weighted_quantile
from adic_tpa.numerics.pwl import (
    adaptive_tangent_points, crra_tangents, crra_utility, exact_objective, pwl_power, tangent_error_bound,
)
from adic_tpa.numerics.roots import brentq

__all__ = [
    "crra_utility", "crra_tangents", "adaptive_tangent_points", "pwl_power", "tangent_error_bound", "exact_objective",
    "brentq", "nearest_correlation", "logsumexp_weights", "weighted_quantile", "kish_ess",
]
