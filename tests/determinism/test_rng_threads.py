"""RNG determinism across thread counts and block sizes (BUILD_SPEC v1.1 §4.2 tests, §1.7, §1.13, §10.6). Owner
WP-02.

Uniforms are pure functions of (base, source, entity, path, month, slot), so the parallel kernels give identical
bits at 1, 4 and 8 numba threads, and splitting the paths into blocks of any size changes nothing (small blocks run
the serial twin kernel, so these tests also pin serial == parallel). SYNTHETIC seeds.
"""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.engine_io import NoiseRequest
from adic_tpa.contracts.enums import Plane
from adic_tpa.numerics.numba_utils import max_threads, numba_threads
from adic_tpa.rng import base_entropy, draw_block, philox4x64_10, student_t, uniforms

BASE = base_entropy(99, Plane.SEARCH, "B1")
IDS = [f"SYN-PC-{i:04d}" for i in range(30)]
PATHS = np.arange(4000, 6000)
MONTHS = np.arange(24, 27)


@pytest.fixture(scope="module")
def reference() -> np.ndarray:
    with numba_threads(1):
        return uniforms(BASE, "priv.credit.default", IDS, PATHS, MONTHS, 5)


@pytest.mark.parametrize("n_threads", [1, 4, 8])
def test_uniforms_are_identical_at_any_thread_count(n_threads: int, reference: np.ndarray) -> None:
    if n_threads > max_threads():
        pytest.skip(f"numba pool has {max_threads()} threads")
    with numba_threads(n_threads) as used:
        assert used == n_threads
        got = uniforms(BASE, "priv.credit.default", IDS, PATHS, MONTHS, 5)
    assert np.array_equal(got, reference)


@pytest.mark.parametrize("n_threads", [1, 4, 8])
def test_philox_batch_and_draw_block_are_thread_invariant(n_threads: int) -> None:
    if n_threads > max_threads():
        pytest.skip(f"numba pool has {max_threads()} threads")
    ctrs = np.arange(32_768 * 4, dtype=np.uint64).reshape(32_768, 4)          # above PARALLEL_MIN: parallel kernels
    key = np.array([11, 13], dtype=np.uint64)
    req = [NoiseRequest(source="sale.success", slots=12, entity_ids=None, months=(30, 31, 32))]
    with numba_threads(1):
        ref_p, ref_d = philox4x64_10(ctrs, key), draw_block(BASE, req, PATHS).u["sale.success"]
    with numba_threads(n_threads):
        assert np.array_equal(philox4x64_10(ctrs, key), ref_p)
        assert np.array_equal(draw_block(BASE, req, PATHS).u["sale.success"], ref_d)
        assert np.array_equal(student_t(ref_d, 5.0), student_t(ref_d.copy(), 5.0))


@pytest.mark.parametrize("block", [1, 7, 500, 1999])
def test_block_size_does_not_change_draws(block: int, reference: np.ndarray) -> None:
    parts = [uniforms(BASE, "priv.credit.default", IDS, PATHS[i:i + block], MONTHS, 5)
             for i in range(0, PATHS.size, block)]
    assert np.array_equal(np.concatenate(parts, axis=0), reference)


def test_any_path_subset_reads_its_own_rows(reference: np.ndarray) -> None:
    pick = np.array([1999, 0, 1000, 17, 17])
    got = uniforms(BASE, "priv.credit.default", IDS, PATHS[pick], MONTHS, 5)
    assert np.array_equal(got, reference[pick])
