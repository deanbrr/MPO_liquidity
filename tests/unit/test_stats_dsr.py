"""Expected maximum, its quantile, DSR, the deflated improvement and MDE (BUILD_SPEC v1.1 §4.4, §7.7; BUILD-20).
Owner WP-02.

``expected_max_z(200)`` within 0.02 of 2.746 and ``max_z_quantile(200)`` within 0.02 of 3.474 (the spec's
acceptance), plus closed forms. SYNTHETIC values only.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy import special

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.stats import deflated_improvement, deflated_sharpe, expected_max_z, max_z_quantile, mde


def test_expected_max_at_200() -> None:
    assert abs(expected_max_z(200) - 2.746) < 0.02
    assert expected_max_z(200) == pytest.approx(2.7460, abs=1e-3)
    # Bailey–López de Prado's approximation is 2.766: the exact value is not that
    bldp = (1 - np.euler_gamma) * special.ndtri(1 - 1 / 200) + np.euler_gamma * special.ndtri(1 - 1 / (200 * math.e))
    assert bldp == pytest.approx(2.766, abs=1e-3) and abs(expected_max_z(200) - bldp) > 0.015


def test_expected_max_closed_forms() -> None:
    assert expected_max_z(1) == 0.0
    assert expected_max_z(2) == pytest.approx(1.0 / math.sqrt(math.pi), abs=1e-10)
    assert expected_max_z(3) == pytest.approx(1.5 / math.sqrt(math.pi), abs=1e-10)
    vals = [expected_max_z(n) for n in (1, 2, 5, 10, 50, 200, 1000, 10 ** 5)]
    assert (np.diff(vals) > 0).all()


def test_max_quantile_at_200() -> None:
    assert abs(max_z_quantile(200) - 3.474) < 0.02
    assert max_z_quantile(200) == pytest.approx(special.ndtri(0.95 ** (1 / 200)), abs=1e-9)
    assert max_z_quantile(1) == pytest.approx(special.ndtri(0.95), abs=1e-12)
    assert max_z_quantile(200, q=0.99) > max_z_quantile(200)
    assert np.isfinite(max_z_quantile(10 ** 9))


def test_deflated_improvement_uses_the_quantile() -> None:
    assert deflated_improvement(10.0, 2.0, 200) == pytest.approx(10.0 - 2.0 * 3.4739, abs=1e-3)
    assert deflated_improvement(10.0, 0.0, 200) == 10.0


def test_deflated_sharpe_formula() -> None:
    sr, n, t, skew, kurt = 0.12, 200, 1000, -0.5, 6.0
    sr0 = expected_max_z(n) / math.sqrt(t - 1)
    z = (sr - sr0) * math.sqrt(t - 1) / math.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr * sr)
    assert deflated_sharpe(sr, n, t, skew, kurt) == pytest.approx(float(special.ndtr(z)), abs=1e-14)
    # one trial: DSR is the PSR against zero
    psr = special.ndtr(sr * math.sqrt(t - 1) / math.sqrt(1 + 0.5 * sr * sr))
    assert deflated_sharpe(sr, 1, t, 0.0, 3.0) == pytest.approx(float(psr), abs=1e-14)
    # an explicit cross-trial variance replaces the null default
    assert deflated_sharpe(sr, n, t, 0.0, 3.0, sr_trials_var=0.0) == pytest.approx(
        deflated_sharpe(sr, 1, t, 0.0, 3.0), abs=1e-14)
    assert deflated_sharpe(0.2, n, t, 0, 3) > deflated_sharpe(0.1, n, t, 0, 3)
    assert deflated_sharpe(0.1, 1000, t, 0, 3) < deflated_sharpe(0.1, 10, t, 0, 3)


def test_deflated_sharpe_validation() -> None:
    with pytest.raises(SchemaError):
        deflated_sharpe(0.1, 0, 100, 0.0, 3.0)
    with pytest.raises(SchemaError):
        deflated_sharpe(0.1, 10, 1, 0.0, 3.0)
    with pytest.raises(SchemaError):
        deflated_sharpe(2.0, 10, 100, 5.0, 1.0)                 # 1 − 10 + 0 < 0
    with pytest.raises(SchemaError):
        expected_max_z(2.5)  # type: ignore[arg-type]
    with pytest.raises(SchemaError):
        max_z_quantile(10, q=1.0)
    with pytest.raises(SchemaError):
        deflated_sharpe(math.nan, 10, 100, 0.0, 3.0)
    with pytest.raises(SchemaError):
        deflated_sharpe(0.1, 10, 100, 0.0, 3.0, sr_trials_var=-1.0)
    with pytest.raises(SchemaError):
        deflated_improvement(1.0, -0.1, 10)


def test_mde_one_sided() -> None:
    assert mde(1.0) == pytest.approx(2.4865, abs=1e-4)
    assert mde(3.0, alpha=0.05, power=0.8) == pytest.approx(3.0 * (special.ndtri(0.95) + special.ndtri(0.8)))
    assert mde(0.0) == 0.0
    with pytest.raises(SchemaError):
        mde(-1.0)
    with pytest.raises(SchemaError):
        mde(1.0, power=1.0)
