"""Linear-algebra helpers (BUILD_SPEC v1.1 §4.3).

``nearest_correlation`` is Higham's (2002) alternating projections with Dykstra's correction: project onto the
positive semidefinite cone (eigenvalues clipped at 0) and onto the unit-diagonal matrices in turn, until the
iterates move less than ``tol`` (relative Frobenius norm). Engine E repairs its regime-blended correlation
matrices with it (§4.10: "R_s = (1 − ω_s)R₀ + ω_s R_crisis repaired by nearest_correlation").

The returned matrix is symmetric with an exact unit diagonal and no negative eigenvalue beyond rounding: after
convergence the last iterate is projected onto the cone once more and rescaled by its diagonal (a congruence, so
it stays positive semidefinite). A valid correlation matrix is returned unchanged; non-convergence raises
``SolverError`` rather than returning a matrix that is not the nearest one.
"""

from __future__ import annotations

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.errors import SchemaError, SolverError

__all__ = ["nearest_correlation"]


def _sym(a: F64) -> F64:
    return 0.5 * (a + a.T)


def _proj_psd(a: F64) -> F64:
    vals, vecs = np.linalg.eigh(a)
    return _sym((vecs * np.maximum(vals, 0.0)) @ vecs.T)


def _unit_diagonal(a: F64) -> F64:
    out = a.copy()
    np.fill_diagonal(out, 1.0)
    return out


def _rescale(a: F64) -> F64:
    d = np.sqrt(np.diag(a))
    out = _sym(a / np.outer(d, d))
    np.fill_diagonal(out, 1.0)
    return out


def nearest_correlation(C: F64, *, tol: float = 1e-10, maxiter: int = 500) -> F64:
    """Nearest correlation matrix to ``C`` in the Frobenius norm (Higham 2002); see the module docstring.

    ``C`` must be square and finite; it is symmetrized first. Raises ``SolverError`` without convergence.
    """
    a = np.array(C, dtype=np.float64)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape[0] == 0:
        raise SchemaError(f"nearest_correlation: expected a non-empty square matrix, got shape {a.shape}")
    if not np.isfinite(a).all():
        raise SchemaError("nearest_correlation: non-finite entries")
    a = _unit_diagonal(_sym(a))
    if np.linalg.eigvalsh(a)[0] >= 0.0:
        return a
    y = a
    x = a
    ds = np.zeros_like(a)
    for _ in range(maxiter):
        r = y - ds
        x_new = _proj_psd(r)
        ds = x_new - r
        y_new = _unit_diagonal(x_new)
        ny = np.linalg.norm(y_new)
        moved = max(np.linalg.norm(x_new - x) / np.linalg.norm(x_new), np.linalg.norm(y_new - y) / ny,
                    np.linalg.norm(y_new - x_new) / ny)
        x, y = x_new, y_new
        if moved <= tol:
            break
    else:
        raise SolverError(f"nearest_correlation: no convergence to tol={tol} in {maxiter} iterations",
                          {"tol": tol, "maxiter": maxiter, "n": a.shape[0]})
    return _rescale(_proj_psd(y))
