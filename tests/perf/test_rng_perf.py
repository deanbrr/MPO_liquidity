"""RNG and sampler performance (BUILD_SPEC v1.1 §4.2 performance, §9.2 WP-02 DoD, §10.1 B1 RNG line and B9).
Nightly (perf). Owner WP-02.

- DoD: ≥ 50M uniforms/s on one thread with all four Philox lanes (§4.2 states 100M/s as the design figure;
  measured on the build machine: ≈ 180M/s single-threaded, ≈ 2G/s on 24 threads).
- B1 RNG line: one quarter of draws for a 2,000-path block of the v2 book ≤ 0.02 s (+10% nightly slack, §10.1),
  on a representative request set [I]: 600 holdings × 3 months × 2 slots, 200 companies × 1 slot, 1,500 loan
  cohorts × 3 months × 1 slot and 20 scalar streams, ≈ 8,300 uniforms per path-quarter (16.6M per block-quarter).
  The engines' real request sets are fixed by WP-09–WP-12; WP-17's ``test_b1_profile`` asserts the line on them.
- B9 support: the standardized t₅ innovations of one 10,000-path × 120-month cube with 20 factors (24M variates)
  take ≤ 40% of B9's 2.5 s.

Loaded machines run 3–4.5× slower (§10.1), so failures here are judged on the reference laptop. SYNTHETIC seeds.
"""

from __future__ import annotations

import time

import numpy as np
import pytest

from adic_tpa.contracts.engine_io import NoiseRequest
from adic_tpa.contracts.enums import Plane
from adic_tpa.numerics.numba_utils import max_threads, numba_threads
from adic_tpa.rng import base_entropy, draw_block, student_t, uniforms

pytestmark = pytest.mark.perf

BASE = base_entropy(1, Plane.SEARCH, "M1")
DOD_UNIFORMS_PER_S = 50e6
B1_BLOCK_QUARTER_S = 0.02 * 1.10


def _best_of(fn, repeats: int = 5) -> float:  # type: ignore[no-untyped-def]
    fn()
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


def test_single_thread_throughput_meets_the_dod() -> None:
    ids = [f"SYN-PE-{i:04d}" for i in range(500)]
    paths, months = np.arange(2000), np.arange(3)
    n = paths.size * months.size * len(ids) * 4
    with numba_threads(1):
        t1 = _best_of(lambda: uniforms(BASE, "perf.uniforms", ids, paths, months, 4))
    with numba_threads(max_threads()):
        tn = _best_of(lambda: uniforms(BASE, "perf.uniforms", ids, paths, months, 4))
    rate1, rate_n = n / t1, n / tn
    print(f"\nPhilox uniforms: {rate1 / 1e6:.0f}M/s on 1 thread, {rate_n / 1e6:.0f}M/s on {max_threads()} threads")
    assert rate1 >= DOD_UNIFORMS_PER_S, f"{rate1 / 1e6:.1f}M uniforms/s single-threaded < 50M/s (WP-02 DoD)"


def _v2_block_quarter_requests(t: int) -> list[NoiseRequest]:
    months = (3 * t, 3 * t + 1, 3 * t + 2)
    reqs = [
        NoiseRequest(source="priv.fund.idio", slots=2, entity_ids=tuple(f"SYN-PE-{i:04d}" for i in range(600)),
                     months=months),
        NoiseRequest(source="priv.company.ev", slots=1, entity_ids=tuple(f"SYN-CMP-{i:06d}" for i in range(200)),
                     months=(3 * t,)),
        NoiseRequest(source="priv.credit.default", slots=1,
                     entity_ids=tuple(f"SYN-PC-{i:04d}" for i in range(1500)), months=months),
    ]
    reqs += [NoiseRequest(source=f"misc.scalar.{k}", slots=1, entity_ids=None, months=(3 * t,)) for k in range(20)]
    return reqs


def test_one_block_quarter_of_v2_draws_fits_the_b1_line() -> None:
    reqs = _v2_block_quarter_requests(7)
    paths = np.arange(4000, 6000)
    elapsed = _best_of(lambda: draw_block(BASE, reqs, paths), repeats=9)
    n = sum(a.size for a in draw_block(BASE, reqs, paths).u.values())
    print(f"\nblock-quarter draws: {n / 1e6:.1f}M uniforms in {elapsed * 1e3:.1f} ms on {max_threads()} threads")
    assert elapsed <= B1_BLOCK_QUARTER_S, f"{elapsed:.4f} s > 0.02 s per 2,000-path block-quarter (B1 RNG line)"


def test_t5_innovations_of_a_cube_fit_inside_b9() -> None:
    u = uniforms(BASE, "perf.scen.eps", [None], np.arange(10_000), np.arange(120), 20).reshape(-1)
    elapsed = _best_of(lambda: student_t(u, 5.0), repeats=3)
    print(f"\nstandardized t5: {elapsed / u.size * 1e9:.1f} ns per variate ({u.size / 1e6:.0f}M in {elapsed:.2f} s)")
    assert elapsed <= 0.4 * 2.5
