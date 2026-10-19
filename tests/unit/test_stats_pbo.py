"""PBO by CSCV (BUILD_SPEC v1.1 §4.4; ARCH §7.6 Gate 3: PBO ≤ 0.20 on the search ledger). Owner WP-02.

Genuine skill gives PBO 0, a perfectly overfit ledger gives 1, and pure noise averages ½. SYNTHETIC ledgers only.
"""

from __future__ import annotations

import itertools

import numpy as np
import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.stats import pbo_cscv


def test_genuine_skill_gives_zero() -> None:
    gen = np.random.Generator(np.random.Philox(1))
    perf = gen.normal(size=(30, 800)) * 0.1 + np.linspace(0.0, 1.0, 30)[:, None]
    assert pbo_cscv(perf) == 0.0
    assert pbo_cscv(perf, metric="sharpe") == 0.0


def test_a_perfectly_overfit_ledger_gives_one() -> None:
    # one trial per in-sample half: positive on its 4 blocks, negative elsewhere -> the IS winner is worst OOS
    combos = list(itertools.combinations(range(8), 4))
    perf = np.full((len(combos), 8 * 10), -1.0)
    for i, c in enumerate(combos):
        for b in c:
            perf[i, b * 10:(b + 1) * 10] = 1.0
    assert pbo_cscv(perf, n_blocks=8) == 1.0


def test_noise_averages_one_half() -> None:
    gen = np.random.Generator(np.random.Philox(2))
    vals = [pbo_cscv(gen.normal(size=(20, 160))) for _ in range(120)]
    assert np.mean(vals) == pytest.approx(0.5, abs=0.08)        # SE of the mean ≈ 0.19/√120 ≈ 0.017


def test_uneven_blocks_and_block_counts() -> None:
    gen = np.random.Generator(np.random.Philox(3))
    perf = gen.normal(size=(10, 103)) + np.arange(10)[:, None]
    assert pbo_cscv(perf, n_blocks=4) == 0.0
    assert pbo_cscv(perf, n_blocks=10) == 0.0


@pytest.mark.parametrize(("perf", "kw"), [
    (np.zeros((1, 16)), {}), (np.zeros((3, 16)), {"n_blocks": 7}), (np.zeros((3, 4)), {"n_blocks": 8}),
    (np.full((3, 16), np.nan), {}), (np.zeros(16), {}), (np.zeros((3, 16)), {"metric": "median"}),
])
def test_validation(perf: np.ndarray, kw: dict) -> None:
    with pytest.raises(SchemaError):
        pbo_cscv(perf, **kw)


def test_sharpe_metric_needs_variation() -> None:
    with pytest.raises(SchemaError):
        pbo_cscv(np.ones((3, 16)), metric="sharpe")
