"""Bracketed scalar root finding (BUILD_SPEC v1.1 §4.3).

``brentq`` wraps ``scipy.optimize.brentq`` and turns every failure into ``SolverError`` (§1.10): no sign change on
the bracket, a non-finite function value at either end, or no convergence within ``maxiter``. Users include the
IRR/MOIC translation (§4.15: "root-found with numerics.brentq, sign change checked"), the CMA anchoring of engine E
(§4.10) and the certainty-equivalent inversion (``stats.ce``).
"""

from __future__ import annotations

import math
from collections.abc import Callable

from scipy import optimize

from adic_tpa.contracts.errors import SolverError

__all__ = ["brentq"]


def brentq(f: Callable[[float], float], lo: float, hi: float, *, xtol: float = 1e-12, maxiter: int = 200) -> float:
    """Root of ``f`` on ``[lo, hi]`` by Brent's method; ``f(lo)`` and ``f(hi)`` must differ in sign (or be 0).

    Raises ``SolverError`` (code ``SOLVER_NONOPTIMAL``) on a missing sign change, a non-finite end value or
    non-convergence; exceptions raised by ``f`` itself propagate unchanged.
    """
    lo, hi = float(lo), float(hi)
    if not (math.isfinite(lo) and math.isfinite(hi)) or not lo < hi:
        raise SolverError(f"brentq: invalid bracket [{lo}, {hi}]", {"lo": lo, "hi": hi})
    f_lo, f_hi = float(f(lo)), float(f(hi))
    if not (math.isfinite(f_lo) and math.isfinite(f_hi)):
        raise SolverError(f"brentq: non-finite f at the bracket ends (f(lo)={f_lo}, f(hi)={f_hi})",
                          {"lo": lo, "hi": hi, "f_lo": f_lo, "f_hi": f_hi})
    if f_lo == 0.0:
        return lo
    if f_hi == 0.0:
        return hi
    if (f_lo > 0) == (f_hi > 0):
        raise SolverError(f"brentq: no sign change on [{lo}, {hi}] (f(lo)={f_lo}, f(hi)={f_hi})",
                          {"lo": lo, "hi": hi, "f_lo": f_lo, "f_hi": f_hi})
    root, info = optimize.brentq(f, lo, hi, xtol=xtol, maxiter=maxiter, full_output=True, disp=False)
    if not info.converged:
        raise SolverError(f"brentq: no convergence in {maxiter} iterations ({info.flag})",
                          {"lo": lo, "hi": hi, "iterations": int(info.iterations), "flag": str(info.flag)})
    return float(root)
