"""Seed keys of the counter-based generator (BUILD_SPEC v1.1 §1.7, §4.2; S-ADR-25 as amended by S-ADR-38).

::

    base(plane, world)  = SeedSequence(entropy=root_seed, spawn_key=(PLANE_CODE[plane], world_code))
                              .generate_state(4, uint32)                 # 16 bytes
    base(FINAL, world)  = HMAC-SHA256(salt, world_id.encode())[:16]      # salt held by the seal service
    stream key          = SHA-256(base ‖ source ‖ u64 entity_key)[:16]  -> Philox key (2 × u64)
    entity_key(id)      = first 8 bytes of SHA-256(id) as u64; 0 when there is no entity

The slot is not in the key (S-ADR-38): it selects the counter word ⌊slot/4⌋ and the output lane slot mod 4
(``rng.philox``). World codes: M1–M6 → 1–6, B1 → 11, B2 → 12, misspecification world i of the contract's list →
100 + i.

Byte order (WP-02 decision; §1.7 leaves it open): every integer ↔ bytes conversion is little-endian — the four
``uint32`` words of the SeedSequence state, the u64 entity key inside the stream-key preimage, the two u64 key words
taken from the digest, and the u64 read from the first 8 digest bytes. Strings are UTF-8. ``base`` and the entity
key have fixed lengths, so the preimage ``base ‖ source ‖ entity`` determines the source uniquely.

Stream keys are cached per block (S-ADR-38) by ``stream_keys``: a bounded memo of a pure function keyed on
``(base, source, entity_ids)``, so the 40 quarterly ``draw_block`` calls of a block hash each entity once. The memo
never changes a result.
"""

from __future__ import annotations

import functools
import hashlib
import hmac
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Final

import numpy as np

from adic_tpa.contracts.arrays import U64
from adic_tpa.contracts.enums import Plane, WorldId, check_world_id
from adic_tpa.contracts.errors import SchemaError, SealBreach

__all__ = [
    "PLANE_CODE", "WORLD_CODE", "MISSPEC_WORLD_BASE", "BASE_BYTES", "ROOT_SEED_BITS", "world_code", "base_entropy",
    "entity_key", "stream_key", "stream_keys", "check_base",
]

PLANE_CODE: Final[Mapping[Plane, int]] = MappingProxyType({
    Plane.CALIBRATION: 0, Plane.SEARCH: 1, Plane.FINAL: 2, Plane.HISTORICAL: 3, Plane.EXPLORATION: 4})
WORLD_CODE: Final[Mapping[str, int]] = MappingProxyType({
    "M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5, "M6": 6, "B1": 11, "B2": 12})
MISSPEC_WORLD_BASE: Final = 100            # misspecification world i of the contract's list -> 100 + i
BASE_BYTES: Final = 16
ROOT_SEED_BITS: Final = 128
_MISSPEC_PREFIX: Final = "MS:"
_KEY_CACHE_SIZE: Final = 256           # ≈ 20 sources × 7 worlds per process, ≤ ~12 MB at 2,000 entities


def world_code(world: WorldId, misspec_index: int | None = None) -> int:
    """The §1.7 world code; a misspecification world (``MS:<name>``) needs its index in the contract's list."""
    try:
        wid = check_world_id(world)
    except ValueError as exc:
        raise SchemaError(str(exc), {"world": world}) from exc
    if wid.startswith(_MISSPEC_PREFIX):
        if misspec_index is None or isinstance(misspec_index, bool) or not isinstance(misspec_index, int) \
                or misspec_index < 0:
            raise SchemaError(f"world {wid!r} needs a non-negative misspec_index (its position in the contract's list)",
                              {"world": wid})
        return MISSPEC_WORLD_BASE + misspec_index
    if misspec_index is not None:
        raise SchemaError(f"misspec_index applies only to MS: worlds, not {wid!r}", {"world": wid})
    return WORLD_CODE[wid]


def base_entropy(root_seed: int, plane: Plane, world: WorldId, *, salt: bytes | None = None,
                 misspec_index: int | None = None) -> bytes:
    """The 16-byte base of a (plane, world) pair (§1.7).

    Non-final planes: SeedSequence(entropy=root_seed, spawn_key=(PLANE_CODE[plane], world code)), 4 uint32 words.
    FINAL: HMAC-SHA256(salt, world_id)[:16]; without a salt it raises ``SealBreach`` (only the seal service holds
    it). A salt on any other plane raises ``SchemaError``. ``root_seed`` is the contract's 128-bit seed.
    """
    try:
        pl = Plane(plane)
    except ValueError as exc:
        raise SchemaError(f"unknown plane {plane!r}") from exc
    code = world_code(world, misspec_index)
    if isinstance(root_seed, bool) or not isinstance(root_seed, int) or not 0 <= root_seed < 2 ** ROOT_SEED_BITS:
        raise SchemaError(f"root_seed must be an int in [0, 2**{ROOT_SEED_BITS}), got {root_seed!r}")
    if pl is Plane.FINAL:
        if not salt:
            raise SealBreach("FINAL-plane seeds need the seal salt; final-plane access outside the seal runner",
                             {"plane": pl.value, "world": world})
        if not isinstance(salt, bytes | bytearray):
            raise SchemaError("salt must be bytes")
        return hmac.new(bytes(salt), world.encode("utf-8"), hashlib.sha256).digest()[:BASE_BYTES]
    if salt is not None:
        raise SchemaError(f"a salt applies only to the FINAL plane, not {pl.value}", {"plane": pl.value})
    seq = np.random.SeedSequence(entropy=root_seed, spawn_key=(PLANE_CODE[pl], code))
    return seq.generate_state(4, np.uint32).astype("<u4").tobytes()


def entity_key(entity_id: str | None) -> np.uint64:
    """First 8 bytes of SHA-256(entity_id) as a little-endian u64; 0 when there is no entity (``None``)."""
    if entity_id is None:
        return np.uint64(0)
    if not isinstance(entity_id, str) or not entity_id:
        raise SchemaError(f"entity ids are non-empty strings (None means no entity), got {entity_id!r}")
    return np.uint64(int.from_bytes(hashlib.sha256(entity_id.encode("utf-8")).digest()[:8], "little"))


def check_base(base: bytes) -> bytes:
    if not isinstance(base, bytes | bytearray) or len(base) != BASE_BYTES:
        raise SchemaError(f"base must be {BASE_BYTES} bytes (rng.base_entropy), got {base!r:.40}")
    return bytes(base)


def _check_source(source: str) -> bytes:
    if not isinstance(source, str) or not source:
        raise SchemaError(f"source must be a non-empty string, got {source!r}")
    return source.encode("utf-8")


def _key_digest(base: bytes, src: bytes, entity: int) -> bytes:
    return hashlib.sha256(base + src + entity.to_bytes(8, "little")).digest()[:BASE_BYTES]


def stream_key(base: bytes, source: str, entity: np.uint64) -> U64:
    """Philox key (uint64[2]) of one (source, entity) stream: SHA-256(base ‖ source ‖ u64 entity)[:16]."""
    ent = int(entity)
    if not 0 <= ent < 2 ** 64:
        raise SchemaError(f"entity key must be a u64, got {entity!r}")
    digest = _key_digest(check_base(base), _check_source(source), ent)
    return np.frombuffer(digest, dtype="<u8").astype(np.uint64)


@functools.lru_cache(maxsize=_KEY_CACHE_SIZE)
def _stream_keys_bytes(base: bytes, source: str, entity_ids: tuple[str | None, ...]) -> bytes:
    src = _check_source(source)
    return b"".join(_key_digest(base, src, int(entity_key(e))) for e in entity_ids)


def stream_keys(base: bytes, source: str, entity_ids: Sequence[str | None]) -> U64:
    """Philox keys of ``source`` for each entity, uint64[E, 2] (a fresh array); memoized per block (module doc)."""
    ids = tuple(entity_ids)
    raw = _stream_keys_bytes(check_base(base), source, ids)
    return np.frombuffer(raw, dtype="<u8").astype(np.uint64).reshape(len(ids), 2)
