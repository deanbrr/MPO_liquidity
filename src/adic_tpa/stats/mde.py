"""Minimum detectable effect (BUILD_SPEC v1.1 §4.4; ARCH §7.6 Gate 3: NOT_ASSESSED when MDE > ε_mat).

The qualification test is one-sided (LCB > ε_mat), so MDE = SE·(z_{1−α} + z_power): the smallest true effect the
test detects with probability ``power`` at level ``alpha`` (2.486·SE at the defaults). Units: those of ``se``
(CE bp a year in Gate 3).
"""

from __future__ import annotations

import math

from scipy import special

from adic_tpa.contracts.errors import SchemaError

__all__ = ["mde"]


def mde(se: float, alpha: float = 0.05, power: float = 0.8) -> float:
    """One-sided minimum detectable effect SE·(Φ⁻¹(1 − α) + Φ⁻¹(power))."""
    if not (math.isfinite(se) and se >= 0):
        raise SchemaError(f"mde: se must be finite and >= 0, got {se}")
    if not 0.0 < alpha < 1.0 or not 0.0 < power < 1.0:
        raise SchemaError(f"mde: alpha and power must lie in (0, 1), got {alpha}, {power}")
    return float(se * (special.ndtri(1.0 - alpha) + special.ndtri(power)))
