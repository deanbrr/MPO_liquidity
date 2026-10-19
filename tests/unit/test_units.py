"""contracts.units (BUILD_SPEC v1.1 §1.2, §4.1). Owner WP-01."""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.errors import UnitError
from adic_tpa.contracts.units import (
    BP, a_from_m, a_from_q, from_bp, m_intensity, m_rate, q_intensity, q_rate, to_bp,
)


def test_rate_conversions() -> None:
    assert q_rate(0.10) == pytest.approx(1.10 ** 0.25 - 1, abs=1e-15)
    assert m_rate(0.0389) == pytest.approx(1.0389 ** (1 / 12) - 1, abs=1e-15)
    assert a_from_q(q_rate(0.10)) == pytest.approx(0.10, abs=1e-15)
    assert a_from_m(m_rate(0.07)) == pytest.approx(0.07, abs=1e-15)
    assert q_rate(0.0) == 0.0 and isinstance(q_rate(0.05), float)


def test_intensities() -> None:
    assert q_intensity(0.2) == pytest.approx(1 - 0.8 ** 0.25, abs=1e-15)
    assert m_intensity(0.12) == pytest.approx(1 - 0.88 ** (1 / 12), abs=1e-15)
    p = q_intensity(0.3)
    assert 1 - (1 - p) ** 4 == pytest.approx(0.3, abs=1e-15)          # four quarters compound back to a year


def test_vectorized() -> None:
    r = np.array([0.0, 0.05, 0.10])
    out = q_rate(r)
    assert isinstance(out, np.ndarray) and out.dtype == np.float64 and out.shape == (3,)
    assert np.allclose(a_from_q(out), r, atol=1e-15)


def test_basis_points() -> None:
    assert to_bp(0.0085) == pytest.approx(85.0) and from_bp(85.0) == pytest.approx(0.0085) and BP == 1e-4


@pytest.mark.parametrize("bad", [-1.0, -1.5, np.array([0.1, -1.2])])
def test_rates_must_exceed_minus_one(bad: object) -> None:
    with pytest.raises(UnitError):
        q_rate(bad)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [-0.1, 1.1, float("nan")])
def test_intensity_domain(bad: float) -> None:
    with pytest.raises(UnitError):
        q_intensity(bad)
