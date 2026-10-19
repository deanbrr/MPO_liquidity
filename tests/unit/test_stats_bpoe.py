"""CVaR and bPOE on closed-form cases (BUILD_SPEC v1.1 §4.4; S-ADR-07). Owner WP-02.

Convention: x is a loss and α the confidence level. The randomized properties (bPOE ≥ POE, bPOE(CVaR_α) = 1 − α)
are in tests/property/test_bpoe_properties.py. SYNTHETIC values only.
"""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.stats import bpoe, cvar

X = np.arange(1.0, 101.0)            # losses 1..100, equal weights


def test_cvar_is_the_mean_of_the_worst_tail() -> None:
    assert cvar(X, 0.95) == pytest.approx(np.mean(X[-5:]))
    assert cvar(X, 0.90) == pytest.approx(np.mean(X[-10:]))
    assert cvar(X, 0.0) == pytest.approx(X.mean())
    assert cvar(np.array([7.0]), 0.99) == 7.0


def test_cvar_splits_an_atom_at_var() -> None:
    x = np.array([0.0, 10.0])
    w = np.array([0.9, 0.1])
    # worst 15%: the 10% atom at 10 plus 5% of the atom at 0 -> (0.1·10 + 0.05·0)/0.15
    assert cvar(x, 0.85, w) == pytest.approx(1.0 / 0.15)
    assert cvar(x, 0.95, w) == pytest.approx(10.0)
    assert cvar(x, 0.85, 3.0 * w) == pytest.approx(cvar(x, 0.85, w))          # weights are normalized


def test_bpoe_regions() -> None:
    assert bpoe(X, X.mean()) == 1.0
    assert bpoe(X, 0.0) == 1.0
    assert bpoe(X, 101.0) == 0.0
    assert bpoe(X, 100.0) == pytest.approx(0.01)                # P(x = max)
    assert bpoe(X, cvar(X, 0.95)) == pytest.approx(0.05, abs=1e-12)
    assert bpoe(X, cvar(X, 0.9)) == pytest.approx(0.10, abs=1e-12)


def test_bpoe_weighted_two_point() -> None:
    x = np.array([0.0, 10.0])
    w = np.array([0.9, 0.1])
    z = cvar(x, 0.85, w)
    assert bpoe(x, z, w) == pytest.approx(0.15, abs=1e-12)
    assert bpoe(x, 10.0, w) == pytest.approx(0.1)
    assert bpoe(x, 5.0, w) >= (x > 5.0) @ w


def test_validation() -> None:
    with pytest.raises(SchemaError):
        cvar(X, 1.0)
    with pytest.raises(SchemaError):
        cvar(np.array([]), 0.5)
    with pytest.raises(SchemaError):
        cvar(X, 0.5, np.ones(3))
    with pytest.raises(SchemaError):
        bpoe(np.array([np.nan, 1.0]), 0.5)
    with pytest.raises(SchemaError):
        bpoe(X, np.inf)
    with pytest.raises(SchemaError):
        bpoe(X, 1.0, -np.ones(100))
