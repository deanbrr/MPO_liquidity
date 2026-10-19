"""Rate and unit conversions (BUILD_SPEC v1.1 §1.2, §4.1).

Money is USD bn at every interface (S-ADR-04); rates are decimal per period of the producing clock; annual values
appear only in config and display (suffix ``_a``). Every function accepts a float or a float64 array and returns
the same kind. Rates must exceed −1 and intensities must lie in [0, 1]; violations raise ``UnitError``.
"""

from __future__ import annotations

from typing import Final, overload

import numpy as np

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.errors import UnitError

__all__ = ["BP", "q_rate", "m_rate", "a_from_q", "a_from_m", "q_intensity", "m_intensity", "to_bp", "from_bp"]

BP: Final = 1e-4


def _as_array(x: float | F64, name: str) -> F64:
    arr = np.asarray(x, dtype=np.float64)
    if not np.isfinite(arr).all():
        raise UnitError(f"{name}: non-finite input")
    return arr


def _out(arr: F64, like: float | F64) -> float | F64:
    return float(arr) if np.ndim(like) == 0 and not isinstance(like, np.ndarray) else arr


def _check_rate(arr: F64, name: str) -> None:
    if (arr <= -1.0).any():
        raise UnitError(f"{name}: a rate must exceed -1 (got min {arr.min()})")


def _check_intensity(arr: F64, name: str) -> None:
    if ((arr < 0.0) | (arr > 1.0)).any():
        raise UnitError(f"{name}: an intensity must lie in [0, 1] (got {arr.min()}..{arr.max()})")


@overload
def q_rate(r_a: float) -> float: ...
@overload
def q_rate(r_a: F64) -> F64: ...
def q_rate(r_a: float | F64) -> float | F64:
    """Quarterly rate from an annual rate: ``(1 + r_a)**0.25 - 1``. Units: decimal a year → per quarter."""
    arr = _as_array(r_a, "q_rate")
    _check_rate(arr, "q_rate")
    return _out(np.power(1.0 + arr, 0.25) - 1.0, r_a)


@overload
def m_rate(r_a: float) -> float: ...
@overload
def m_rate(r_a: F64) -> F64: ...
def m_rate(r_a: float | F64) -> float | F64:
    """Monthly rate from an annual rate: ``(1 + r_a)**(1/12) - 1``. Units: decimal a year → per month."""
    arr = _as_array(r_a, "m_rate")
    _check_rate(arr, "m_rate")
    return _out(np.power(1.0 + arr, 1.0 / 12.0) - 1.0, r_a)


@overload
def a_from_q(r_q: float) -> float: ...
@overload
def a_from_q(r_q: F64) -> F64: ...
def a_from_q(r_q: float | F64) -> float | F64:
    """Annual rate from a quarterly rate: ``(1 + r_q)**4 - 1``. Units: per quarter → decimal a year."""
    arr = _as_array(r_q, "a_from_q")
    _check_rate(arr, "a_from_q")
    return _out(np.power(1.0 + arr, 4.0) - 1.0, r_q)


@overload
def a_from_m(r_m: float) -> float: ...
@overload
def a_from_m(r_m: F64) -> F64: ...
def a_from_m(r_m: float | F64) -> float | F64:
    """Annual rate from a monthly rate: ``(1 + r_m)**12 - 1``. Units: per month → decimal a year."""
    arr = _as_array(r_m, "a_from_m")
    _check_rate(arr, "a_from_m")
    return _out(np.power(1.0 + arr, 12.0) - 1.0, r_m)


@overload
def q_intensity(x_a: float) -> float: ...
@overload
def q_intensity(x_a: F64) -> F64: ...
def q_intensity(x_a: float | F64) -> float | F64:
    """Quarterly event probability from an annual one: ``1 - (1 - x_a)**0.25`` (SYN §0). Units: probability."""
    arr = _as_array(x_a, "q_intensity")
    _check_intensity(arr, "q_intensity")
    return _out(1.0 - np.power(1.0 - arr, 0.25), x_a)


@overload
def m_intensity(x_a: float) -> float: ...
@overload
def m_intensity(x_a: F64) -> F64: ...
def m_intensity(x_a: float | F64) -> float | F64:
    """Monthly event probability from an annual one: ``1 - (1 - x_a)**(1/12)``. Units: probability."""
    arr = _as_array(x_a, "m_intensity")
    _check_intensity(arr, "m_intensity")
    return _out(1.0 - np.power(1.0 - arr, 1.0 / 12.0), x_a)


def to_bp(x: float) -> float:
    """Decimal to basis points (0.0085 → 85.0). Units: decimal → bp."""
    return float(x) / BP


def from_bp(bp: float) -> float:
    """Basis points to decimal (85 → 0.0085). Units: bp → decimal."""
    return float(bp) * BP
