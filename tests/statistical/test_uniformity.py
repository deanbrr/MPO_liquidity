"""Uniformity of the keyed Philox streams (BUILD_SPEC v1.1 §4.2 tests; §10.6 statistical suite). Owner WP-02.

KS p > 0.01 on 1e6 draws (and on 1e6 draws of each Philox lane), and |corr| < 0.005 between adjacent slots
(including the lane-3 → slot-4 counter boundary), adjacent entities, adjacent paths, adjacent months and two
sources. Basis: every correlation uses ≥ 1e6 pairs, so the SE of a null correlation is ≤ 0.001 and 0.005 is ≥ 5 SE;
fixed seeds make the outcome deterministic. SYNTHETIC seeds only.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import base_entropy, uniforms

BASE = base_entropy(2026, Plane.EXPLORATION, "M3")
IDS = ["SYN-CO-0001", "SYN-CO-0002", "SYN-CO-0003", None]
MILLION = 1_000_000


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.corrcoef(a.reshape(-1), b.reshape(-1))[0, 1])


@pytest.fixture(scope="module")
def draws() -> np.ndarray:
    # 62,500 paths × 4 months × 4 entities × 8 slots: 1e6 cells per slot, 8e6 uniforms
    return uniforms(BASE, "stat.uniformity", IDS, np.arange(62_500), np.arange(40, 44), 8)


def test_ks_on_a_million_draws(draws: np.ndarray) -> None:
    assert stats.kstest(draws.reshape(-1)[:MILLION], "uniform").pvalue > 0.01


@pytest.mark.parametrize("lane", [0, 1, 2, 3])
def test_ks_per_lane(draws: np.ndarray, lane: int) -> None:
    assert stats.kstest(draws[..., lane].reshape(-1)[:MILLION], "uniform").pvalue > 0.01


def test_moments(draws: np.ndarray) -> None:
    x = draws.reshape(-1)
    assert abs(x.mean() - 0.5) < 5 * np.sqrt(1 / 12 / x.size)
    assert abs(x.var() - 1 / 12) < 5 * np.sqrt(1 / 180 / x.size)       # Var((U − ½)²) = 1/180


def test_adjacent_slot_correlations(draws: np.ndarray) -> None:
    for s in range(7):                                  # s = 3 → 4 crosses into the next counter block
        assert abs(_corr(draws[..., s], draws[..., s + 1])) < 0.005, s


def test_adjacent_entity_path_and_month_correlations(draws: np.ndarray) -> None:
    for e in range(3):
        assert abs(_corr(draws[:, :, e], draws[:, :, e + 1])) < 0.005, e
    assert abs(_corr(draws[:-1], draws[1:])) < 0.005
    assert abs(_corr(draws[:, :-1], draws[:, 1:])) < 0.005


def test_two_sources_are_uncorrelated(draws: np.ndarray) -> None:
    other = uniforms(BASE, "stat.uniformity.b", IDS, np.arange(62_500), np.arange(40, 44), 8)
    assert abs(_corr(draws, other)) < 0.005
