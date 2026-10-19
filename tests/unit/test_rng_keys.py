"""Seed keys (BUILD_SPEC v1.1 §1.7, §4.2; S-ADR-25/-38). Owner WP-02.

Bases come from a SeedSequence spawn tree at the (plane, world) level, or from HMAC(salt, world) on the FINAL plane;
stream keys hash (base, source, entity) and never the slot. Byte order is little-endian throughout (WP-02 decision).
Goldens pin the derivation so an accidental change cannot pass silently. SYNTHETIC seeds only.
"""

from __future__ import annotations

import hashlib
import hmac

import numpy as np
import pytest

from adic_tpa.contracts.enums import Plane
from adic_tpa.contracts.errors import SchemaError, SealBreach
from adic_tpa.rng import (
    MISSPEC_WORLD_BASE, PLANE_CODE, WORLD_CODE, base_entropy, entity_key, stream_key, stream_keys, world_code,
)

GOLDEN_BASE_SEARCH_M1 = "747270a2a073a5105318ac7705cb63a0"     # base_entropy(12345, SEARCH, "M1")


def test_plane_and_world_codes_follow_section_1_7() -> None:
    assert dict(PLANE_CODE) == {Plane.CALIBRATION: 0, Plane.SEARCH: 1, Plane.FINAL: 2, Plane.HISTORICAL: 3,
                                Plane.EXPLORATION: 4}
    assert dict(WORLD_CODE) == {"M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5, "M6": 6, "B1": 11, "B2": 12}
    assert world_code("MS:slippage", 0) == MISSPEC_WORLD_BASE == 100
    assert world_code("MS:fat_tails", 3) == 103


def test_base_is_the_seedsequence_state_in_little_endian() -> None:
    base = base_entropy(12345, Plane.SEARCH, "M1")
    expected = np.random.SeedSequence(entropy=12345, spawn_key=(1, 1)).generate_state(4, np.uint32)
    assert base == expected.astype("<u4").tobytes()
    assert base.hex() == GOLDEN_BASE_SEARCH_M1
    assert len(base) == 16


def test_bases_differ_by_seed_plane_world_and_misspec_index() -> None:
    seen = {
        base_entropy(1, Plane.SEARCH, "M1"), base_entropy(2, Plane.SEARCH, "M1"),
        base_entropy(1, Plane.CALIBRATION, "M1"), base_entropy(1, Plane.SEARCH, "M6"),
        base_entropy(1, Plane.SEARCH, "B1"), base_entropy(1, Plane.SEARCH, "MS:a", misspec_index=0),
        base_entropy(1, Plane.SEARCH, "MS:a", misspec_index=1),
    }
    assert len(seen) == 7
    assert base_entropy(1, Plane.SEARCH, "M1") == base_entropy(1, "SEARCH", "M1")       # str plane value accepted


def test_final_plane_needs_the_salt() -> None:
    with pytest.raises(SealBreach) as exc:
        base_entropy(1, Plane.FINAL, "M1")
    assert exc.value.code == "SEAL_BREACH"
    salt = b"SYNTHETIC-seal-salt"
    got = base_entropy(1, Plane.FINAL, "M1", salt=salt)
    assert got == hmac.new(salt, b"M1", hashlib.sha256).digest()[:16]
    assert got == base_entropy(999, Plane.FINAL, "M1", salt=salt)      # the salt replaces the root seed
    assert got != base_entropy(1, Plane.FINAL, "M6", salt=salt)
    with pytest.raises(SchemaError):
        base_entropy(1, Plane.SEARCH, "M1", salt=salt)


def test_plane_salt_and_entity_key_validation() -> None:
    with pytest.raises(SchemaError):
        base_entropy(1, "SEALED", "M1")  # type: ignore[arg-type]
    with pytest.raises(SchemaError):
        base_entropy(1, Plane.FINAL, "M1", salt="not-bytes")  # type: ignore[arg-type]
    with pytest.raises(SchemaError):
        stream_key(bytes(16), "src", np.int64(-1))  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [-1, 2 ** 128, 1.5, True, "7"])
def test_root_seed_must_be_a_128_bit_int(bad: object) -> None:
    with pytest.raises(SchemaError):
        base_entropy(bad, Plane.SEARCH, "M1")  # type: ignore[arg-type]


def test_root_seed_upper_edge_is_accepted() -> None:
    assert len(base_entropy(2 ** 128 - 1, Plane.SEARCH, "M1")) == 16


@pytest.mark.parametrize(("world", "index"), [("MS:x", None), ("MS:x", -1), ("M1", 0), ("M7", None), ("Q1", None)])
def test_world_validation(world: str, index: int | None) -> None:
    with pytest.raises(SchemaError):
        base_entropy(1, Plane.SEARCH, world, misspec_index=index)


def test_entity_key_is_the_first_eight_sha256_bytes_little_endian() -> None:
    cid = "SYN-CMP-000417"
    assert entity_key(cid) == np.uint64(int.from_bytes(hashlib.sha256(cid.encode()).digest()[:8], "little"))
    assert isinstance(entity_key(cid), np.uint64)
    assert entity_key(None) == np.uint64(0)
    assert entity_key("SYN-PE-0001") != entity_key("SYN-PE-0002")
    with pytest.raises(SchemaError):
        entity_key("")
    with pytest.raises(SchemaError):
        entity_key(17)  # type: ignore[arg-type]


def test_stream_key_hashes_base_source_and_entity_only() -> None:
    base = bytes(range(16))
    ent = entity_key("SYN-PE-0042")
    digest = hashlib.sha256(base + b"priv.fund.idio" + int(ent).to_bytes(8, "little")).digest()[:16]
    key = stream_key(base, "priv.fund.idio", ent)
    assert key.dtype == np.uint64 and key.shape == (2,)
    assert key.tolist() == [int.from_bytes(digest[:8], "little"), int.from_bytes(digest[8:], "little")]
    others = {tuple(stream_key(base, "priv.fund.call", ent)), tuple(stream_key(bytes(16), "priv.fund.idio", ent)),
              tuple(stream_key(base, "priv.fund.idio", entity_key("SYN-PE-0043")))}
    assert tuple(key) not in others and len(others) == 3


def test_stream_keys_stack_stream_key_and_return_fresh_arrays() -> None:
    base = bytes(range(16, 32))
    ids = ["SYN-PE-0001", None, "SYN-PE-0001", "SYN-RA-0007"]
    keys = stream_keys(base, "src", ids)
    assert keys.shape == (4, 2) and keys.dtype == np.uint64
    for row, e in zip(keys, ids, strict=True):
        assert row.tolist() == stream_key(base, "src", entity_key(e)).tolist()
    keys[:] = 0                                            # the memo must not hand out shared buffers
    assert stream_keys(base, "src", ids)[0].tolist() == stream_key(base, "src", entity_key(ids[0])).tolist()
    assert stream_keys(base, "src", []).shape == (0, 2)


@pytest.mark.parametrize("base", [b"short", bytes(17), "0" * 16])
def test_malformed_base_or_source(base: object) -> None:
    with pytest.raises(SchemaError):
        stream_key(base, "src", np.uint64(0))  # type: ignore[arg-type]
    with pytest.raises(SchemaError):
        stream_key(bytes(16), "", np.uint64(0))
