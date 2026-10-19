"""Philox4x64-10 equals numpy's Philox (BUILD_SPEC v1.1 §4.2 tests; §1.7). Owner WP-02.

numpy's ``Philox`` bit generator increments its 256-bit counter (word 0 first, with carry) *before* it generates a
block of four words, so a state counter c yields ``philox4x64_10(c + 1)``. This file pins that convention on 20
(counter, key) pairs — zero and all-ones words, every carry position, the wrap-around of the full counter, random
words — and pins the Random123 known-answer vectors, so the kernel is checked against numpy and an independent
reference. It also checks the uniform pipeline (§1.7: counter (path, month, ⌊slot/4⌋, 0), lane slot mod 4,
u = (x >> 11)·2^-53) against numpy end to end. SYNTHETIC seeds only.
"""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.enums import Plane
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.rng import base_entropy, entity_key, philox4x64_10, stream_key, uniforms
from adic_tpa.rng.philox import PARALLEL_MIN

M = 2 ** 64 - 1

# (counter words c0..c3, key words k0, k1): numpy state counter c, compared with philox4x64_10(c + 1)
PINNED: list[tuple[tuple[int, int, int, int], tuple[int, int]]] = [
    ((0, 0, 0, 0), (0, 0)),
    ((M, 0, 0, 0), (1, 2)),                       # carry into word 1
    ((M, M, 0, 0), (3, 4)),                       # carry into word 2
    ((M, M, M, 0), (5, 6)),                       # carry into word 3
    ((M, M, M, M), (7, 8)),                       # the full counter wraps to zero
    ((0, 0, 0, 0), (M, M)),
    ((1, 2, 3, 4), (5, 6)),
    ((M - 1, 0, 0, 0), (0, M)),
    ((0x243F6A8885A308D3, 0x13198A2E03707344, 0xA4093822299F31D0, 0x082EFA98EC4E6C89),
     (0x452821E638D01377, 0xBE5466CF34E90C6C)),
    ((0x0123456789ABCDEF, 0xFEDCBA9876543210, 0x0F1E2D3C4B5A6978, 0x8796A5B4C3D2E1F0),
     (0xDEADBEEFCAFEBABE, 0x0BADF00D0DDBA11)),
    ((1999, 119, 3, 0), (0x9E3779B97F4A7C15, 0xBB67AE8584CAA73B)),     # a (path, month, slot-group, 0) counter
    ((0, 7, 0, 0), (0xD2E7470EE14C6C93, 0xCA5A826395121157)),
    ((0xFFFFFFFF, 0xFFFFFFFF00000000, 0x00000000FFFFFFFF, 0x8000000000000000), (0x8000000000000000, 1)),
    ((0x5851F42D4C957F2D, 0x14057B7EF767814F, 0x2545F4914F6CDD1D, 0x9E3779B97F4A7C15),
     (0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9)),
    ((0xA0761D6478BD642F, 0xE7037ED1A0B428DB, 0x8EBC6AF09C88C6E3, 0x589965CC75374CC3),
     (0x1D8E4E27C47D124F, 0xBF58476D1CE4E5B9)),
    ((0x94D049BB133111EB, 0x2545F4914F6CDD1D, 0x9FB21C651E98DF25, 0xD6E8FEB86659FD93),
     (0xFF51AFD7ED558CCD, 0xC4CEB9FE1A85EC53)),
    ((0x6A09E667F3BCC908, 0xBB67AE8584CAA73B, 0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1),
     (0x510E527FADE682D1, 0x9B05688C2B3E6C1F)),
    ((0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179, 0xCBBB9D5DC1059ED8, 0x629A292A367CD507),
     (0x9159015A3070DD17, 0x152FECD8F70E5939)),
    ((0x67332667FFC00B31, 0x8EB44A8768581511, 0xDB0C2E0D64F98FA7, 0x47B5481DBEFA4FA4),
     (0x428A2F98D728AE22, 0x7137449123EF65CD)),
    ((12345, 0, 0, 0), (0x747270A2A073A510, 0x5318AC7705CB63A0)),
]

# Random123 kat_vectors for philox4x64-10: counter, key -> output (the bijection itself, no increment)
KAT: list[tuple[tuple[int, int, int, int], tuple[int, int], tuple[int, int, int, int]]] = [
    ((0, 0, 0, 0), (0, 0),
     (0x16554D9ECA36314C, 0xDB20FE9D672D0FDC, 0xD7E772CEE186176B, 0x7E68B68AEC7BA23B)),
    ((M, M, M, M), (M, M),
     (0x87B092C3013FE90B, 0x438C3C67BE8D0224, 0x9CC7D7C69CD777B6, 0xA09CAEBF594F0BA0)),
    ((0x243F6A8885A308D3, 0x13198A2E03707344, 0xA4093822299F31D0, 0x082EFA98EC4E6C89),
     (0x452821E638D01377, 0xBE5466CF34E90C6C),
     (0xA528F45403E61D95, 0x38C72DBD566E9788, 0xA5A1610E72FD18B5, 0x57BD43B5E52B7FE6)),
]


def _as_int(words: tuple[int, ...]) -> int:
    return sum(w << (64 * i) for i, w in enumerate(words))


def _plus_one(words: tuple[int, int, int, int]) -> tuple[int, ...]:
    v = (_as_int(words) + 1) % 2 ** 256
    return tuple((v >> (64 * i)) & M for i in range(4))


def _numpy_block(counter: tuple[int, int, int, int], key: tuple[int, int]) -> np.ndarray:
    return np.random.Philox(counter=_as_int(counter), key=_as_int(key)).random_raw(4)


def test_twenty_pinned_pairs_are_distinct() -> None:
    assert len(PINNED) == 20
    assert len({(c, k) for c, k in PINNED}) == 20


@pytest.mark.parametrize(("counter", "key"), PINNED)
def test_matches_numpy_philox_with_counter_advanced_first(counter: tuple[int, int, int, int],
                                                           key: tuple[int, int]) -> None:
    got = philox4x64_10(np.array([_plus_one(counter)], dtype=np.uint64), np.array(key, dtype=np.uint64))[0]
    assert got.tolist() == _numpy_block(counter, key).tolist()


@pytest.mark.parametrize(("counter", "key", "expected"), KAT)
def test_random123_known_answer_vectors(counter: tuple[int, int, int, int], key: tuple[int, int],
                                        expected: tuple[int, int, int, int]) -> None:
    got = philox4x64_10(np.array([counter], dtype=np.uint64), np.array(key, dtype=np.uint64))[0]
    assert tuple(int(x) for x in got) == expected


def test_numpy_stream_continues_with_successive_counters() -> None:
    counter, key = PINNED[9]
    expected = np.random.Philox(counter=_as_int(counter), key=_as_int(key)).random_raw(12)
    ctrs = [_plus_one(counter)]
    for _ in range(2):
        ctrs.append(_plus_one(ctrs[-1]))  # type: ignore[arg-type]
    got = philox4x64_10(np.array(ctrs, dtype=np.uint64), np.array(key, dtype=np.uint64))
    assert got.reshape(-1).tolist() == expected.tolist()


def test_parallel_batch_equals_serial_chunks_and_rows() -> None:
    gen = np.random.Generator(np.random.Philox(7))
    ctrs = gen.integers(0, 2 ** 63, size=(20_000, 4), dtype=np.int64).astype(np.uint64)
    key = np.array([0x0123456789ABCDEF, 0xFEDCBA9876543210], dtype=np.uint64)
    assert ctrs.size >= PARALLEL_MIN                     # the parallel kernel; the chunks below run serially
    batch = philox4x64_10(ctrs, key)
    chunks = np.vstack([philox4x64_10(ctrs[i:i + 1000], key) for i in range(0, ctrs.shape[0], 1000)])
    assert np.array_equal(batch, chunks)
    rows = np.vstack([philox4x64_10(ctrs[i:i + 1], key) for i in range(0, 200)])
    assert np.array_equal(batch[:200], rows)
    assert batch.dtype == np.uint64 and batch.shape == (20_000, 4)


def test_uniform_pipeline_matches_numpy_end_to_end() -> None:
    base = base_entropy(20261019, Plane.SEARCH, "M6")
    source, ent = "priv.company.ev", "SYN-CMP-000417"
    paths, months, slots = np.array([0, 1, 1999]), np.array([0, 3, 119]), 7
    u = uniforms(base, source, [ent], paths, months, slots)
    key = stream_key(base, source, entity_key(ent))
    k = int(key[0]) | (int(key[1]) << 64)
    for ip, p in enumerate(paths):
        for im, m in enumerate(months):
            for s in range(slots):
                state = (int(p) + (int(m) << 64) + ((s // 4) << 128) - 1) % 2 ** 256   # numpy advances first
                raw = int(np.random.Philox(counter=state, key=k).random_raw(4)[s % 4])
                assert u[ip, im, 0, s] == (raw >> 11) * 2.0 ** -53


def test_rejects_malformed_inputs() -> None:
    key = np.zeros(2, dtype=np.uint64)
    with pytest.raises(SchemaError):
        philox4x64_10(np.zeros((3, 3), dtype=np.uint64), key)
    with pytest.raises(SchemaError):
        philox4x64_10(np.zeros((3, 4), dtype=np.uint64), np.zeros(3, dtype=np.uint64))
    with pytest.raises(SchemaError):
        philox4x64_10(-np.ones((1, 4), dtype=np.int64), key)
    with pytest.raises(SchemaError):
        philox4x64_10(np.zeros((1, 4), dtype=np.float64), key)
    assert philox4x64_10(np.ones((2, 4), dtype=np.int64), key).dtype == np.uint64   # non-negative ints are cast
