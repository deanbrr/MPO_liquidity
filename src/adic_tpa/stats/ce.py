"""Certainty-equivalent conversions to bp a year (BUILD_SPEC v1.1 §1.2, §4.4, §5.11; ARCH §5.2).

CE metrics are reported in bp a year of certainty-equivalent return, with "≈ $X m a year" beside them
(1bp a year ≈ $17.7m a year at W₀ = $177bn).

- ``j_to_ce_wealth``: the sure terminal wealth w (multiple of W₀) whose Tier-2 objective equals J. ARCH §5.2's J is
  E[U_γ(W̃^real/W₀)] − λ_T·(E[((1 − W̃/W̃*)⁺)^p])^{1/p}; for a sure outcome the p-norm of the shortfall is the
  shortfall itself, so w solves U_γ(w) − λ_T·(1 − w/target_rel)⁺ = J, which is strictly increasing in w (the
  exponent cancels; it is still validated > 1, S-ADR-06). The CE wealth enters both terms, so ``target_rel`` must be
  stated in the utility's units (WP-02 reading: §4.4 passes a single wealth scale). w is closed-form at or above
  the target and root-found (``numerics.brentq``) below it.
- ``delta_ce_bp(J1, J0, obj, years)`` = 1e4·(w₁^{1/years} − w₀^{1/years}): the difference of the annualized CE
  returns, with target_rel = (1 + target_annual)^horizon_years and λ_T, γ, p from ``obj`` (P-side J).
- ``h_delta_ce_bp(Δobj, ū′, years)`` = 1e4·Δobj/(ū′·years): H's first-order conversion (§5.11), ū′ the marginal
  objective per W₀ unit of terminal wealth from the active PWL pieces, over the tree's 3 years.
- ``usd_m_per_bp_year(W₀)`` = W₀·1e-4·1e3 = $m a year per bp a year (17.7 at W₀ = 177).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.units import BP
from adic_tpa.numerics.roots import brentq

if TYPE_CHECKING:
    from adic_tpa.contracts.contract import ObjectiveSpec

__all__ = ["j_to_ce_wealth", "delta_ce_bp", "h_delta_ce_bp", "usd_m_per_bp_year", "sure_objective"]

_USD_M_PER_BN = 1e3


def _utility(w: float, gamma: float) -> float:
    return math.log(w) if gamma == 1.0 else w ** (1.0 - gamma) / (1.0 - gamma)


def _inverse_utility(j: float, gamma: float) -> float | None:
    """U_γ⁻¹(J), or None when J is outside U_γ's range."""
    if gamma == 1.0:
        return math.exp(j) if j < 709.0 else None
    base = (1.0 - gamma) * j
    if base <= 0.0:
        return None
    return base ** (1.0 / (1.0 - gamma))


def _check(gamma: float, lambda_T: float, shortfall_exponent: float, target_rel: float) -> None:
    if not (math.isfinite(gamma) and gamma > 0):
        raise SchemaError(f"gamma must be positive, got {gamma}")
    if not (math.isfinite(lambda_T) and lambda_T >= 0):
        raise SchemaError(f"lambda_T must be >= 0, got {lambda_T}")
    if not (math.isfinite(shortfall_exponent) and shortfall_exponent > 1.0):
        raise SchemaError(f"shortfall_exponent must be > 1 strictly (S-ADR-06), got {shortfall_exponent}")
    if not (math.isfinite(target_rel) and target_rel > 0):
        raise SchemaError(f"target_rel must be positive, got {target_rel}")


def sure_objective(w: float, gamma: float, lambda_T: float, shortfall_exponent: float, target_rel: float) -> float:
    """J of a sure terminal wealth w (multiple of W₀): U_γ(w) − λ_T·(((1 − w/target)⁺)^p)^{1/p}."""
    _check(gamma, lambda_T, shortfall_exponent, target_rel)
    if not (math.isfinite(w) and w > 0):
        raise SchemaError(f"wealth must be positive, got {w}")
    shortfall = max(0.0, 1.0 - w / target_rel)
    return _utility(w, gamma) - lambda_T * (shortfall ** shortfall_exponent) ** (1.0 / shortfall_exponent)


def j_to_ce_wealth(J: float, gamma: float, lambda_T: float, shortfall_exponent: float, target_rel: float) -> float:
    """Certainty-equivalent terminal wealth (multiple of W₀) of the objective value J (module docstring).

    Raises ``SchemaError`` when no positive sure wealth attains J (e.g. J ≥ 0 at γ > 1).
    """
    _check(gamma, lambda_T, shortfall_exponent, target_rel)
    if not math.isfinite(J):
        raise SchemaError(f"J must be finite, got {J}")
    w_free = _inverse_utility(J, gamma)                 # the answer if there is no shortfall
    if w_free is not None and not w_free > 0.0:
        raise SchemaError(f"the certainty-equivalent wealth of J={J} underflows float64 (gamma={gamma})")
    if w_free is not None and (w_free >= target_rel or lambda_T == 0.0):
        return w_free
    if w_free is None and gamma >= 1.0:
        raise SchemaError(f"no sure wealth attains J={J} at gamma={gamma} (CRRA utility is negative for gamma > 1)")
    if lambda_T > 0 and gamma < 1.0 and J <= -lambda_T:
        raise SchemaError(f"no sure wealth attains J={J}: the objective exceeds -lambda_T={-lambda_T} for w > 0")

    def gap(w: float) -> float:
        return _utility(w, gamma) - lambda_T * (1.0 - w / target_rel) - J

    lo = w_free if w_free is not None else target_rel * 1e-300
    return brentq(gap, lo, target_rel, xtol=1e-15 * target_rel, maxiter=500)


def delta_ce_bp(J1: float, J0: float, obj: ObjectiveSpec, years: int = 10) -> float:
    """CE improvement of J1 over J0 in bp a year: 1e4·(w₁^{1/years} − w₀^{1/years}) (module docstring)."""
    if not years > 0:
        raise SchemaError(f"years must be positive, got {years}")
    target = (1.0 + obj.target_annual) ** obj.horizon_years
    w1 = j_to_ce_wealth(J1, obj.gamma, obj.lambda_T, obj.shortfall_exponent, target)
    w0 = j_to_ce_wealth(J0, obj.gamma, obj.lambda_T, obj.shortfall_exponent, target)
    return 1e4 * (w1 ** (1.0 / years) - w0 ** (1.0 / years))


def h_delta_ce_bp(delta_obj: float, marginal_utility_wealth: float, years: float = 3.0) -> float:
    """H's CE conversion 1e4·Δobj/(ū′·years) in bp a year (§5.11). Units: ū′ per W₀ unit of terminal wealth."""
    if not (math.isfinite(marginal_utility_wealth) and marginal_utility_wealth > 0):
        raise SchemaError(f"marginal utility of wealth must be positive, got {marginal_utility_wealth}")
    if not (math.isfinite(years) and years > 0) or not math.isfinite(delta_obj):
        raise SchemaError(f"need finite delta_obj and years > 0, got {delta_obj}, {years}")
    return 1e4 * delta_obj / (marginal_utility_wealth * years)


def usd_m_per_bp_year(w0_bn: float) -> float:
    """$m a year per bp a year of CE return at opening NAV ``w0_bn`` (17.7 at 177). Units: USD bn → USD m a year."""
    if not (math.isfinite(w0_bn) and w0_bn > 0):
        raise SchemaError(f"w0_bn must be positive, got {w0_bn}")
    return w0_bn * BP * _USD_M_PER_BN
