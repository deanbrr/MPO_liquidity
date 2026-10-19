"""Ed25519 sign-offs (BUILD_SPEC v1.1 §4.1; S-ADR-40, S-ADR-37).

A ``SignOff`` signs ``canonical_json({object_hash, role, signer_hash, signed_at})``. Private keys are per person,
stored as DPAPI-protected blobs (``win32crypt``) and referenced by ``key_ref = "dpapi:<path>"``; public keys live
in ``config/room/signers_roster.yaml`` (WP-27) keyed by ``signer_hash``. DEV/SYNTHETIC mode signs with a fixed
test key (``key_ref = "dev_test_key"``) that is labelled SYNTHETIC and refused in REAL mode (``RunModeRefused``).
Signatures are lower-case hex.

``verify`` recognizes a DEV test-signer sign-off by identity, not by its ``method`` label (which the signature
does not cover): its ``signer_hash`` is ``DEV_TEST_SIGNER_HASH``, its roster key is the DEV public key, or its
method says ``dev_test_key``. Such a sign-off verifies only under an explicit ``run_mode=RunMode.DEV_SYNTHETIC``;
``run_mode=RunMode.REAL`` and an omitted run mode both raise ``RunModeRefused`` (fail closed). Real sign-offs verify
in any mode.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Final

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from adic_tpa.contracts.contract import DEV_TEST_SIGNER_HASH, SignOff
from adic_tpa.contracts.enums import RunMode
from adic_tpa.contracts.errors import RunModeRefused, SchemaError
from adic_tpa.contracts.hashing import canonical_json

__all__ = [
    "sign", "verify", "verify_payload", "signoff_payload", "DEV_TEST_KEY_REF", "DEV_TEST_SIGNER_HASH",
    "DEV_TEST_LABEL", "dev_test_public_key", "public_key_bytes", "protect_private_key", "generate_dpapi_key",
    "signer_hash",
]

DEV_TEST_KEY_REF: Final = "dev_test_key"
DEV_TEST_LABEL: Final = "SYNTHETIC – DEV TEST SIGNER – NOT A REAL SIGNATURE"
# Deterministic seed so Replay cassettes and golden manifests reproduce DEV signatures bit for bit.
_DEV_SEED: Final = hashlib.sha256(b"adic-tpa dev test key | SYNTHETIC - NOT ADIC DATA | refused in REAL mode").digest()
_DPAPI_PREFIX: Final = "dpapi:"
_DPAPI_DESCRIPTION: Final = "adic-tpa Ed25519 signing key"


def signer_hash(identity: str) -> str:
    """``sha256:<hex>`` of a signer identity (e.g. a Windows SID); rosters key public keys by it."""
    return "sha256:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _dev_private_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(_DEV_SEED)


def public_key_bytes(key: Ed25519PrivateKey | Ed25519PublicKey) -> bytes:
    """Raw 32-byte public key."""
    pub = key.public_key() if isinstance(key, Ed25519PrivateKey) else key
    return pub.public_bytes(Encoding.Raw, PublicFormat.Raw)


def dev_test_public_key() -> bytes:
    """Raw public key of the DEV test signer (enter it in DEV rosters under ``DEV_TEST_SIGNER_HASH``)."""
    return public_key_bytes(_dev_private_key())


def signoff_payload(object_hash: str, role: str, signer_hash: str, signed_at: datetime) -> bytes:
    """The signed bytes: ``canonical_json({object_hash, role, signer_hash, signed_at})``."""
    return canonical_json({"object_hash": object_hash, "role": role, "signer_hash": signer_hash,
                           "signed_at": signed_at})


def _refuse_dev_in_real(run_mode: RunMode | None, what: str) -> None:
    if run_mode is RunMode.REAL:
        raise RunModeRefused(f"{what}: the DEV test signer is refused in REAL mode (S-ADR-37)",
                             {"facility": "dev_test_key"})


def _load_private_key(key_ref: str) -> Ed25519PrivateKey:
    if key_ref == DEV_TEST_KEY_REF:
        return _dev_private_key()
    if key_ref.startswith(_DPAPI_PREFIX):
        import win32crypt  # pywin32; Windows only (S-ADR-40)

        blob = Path(key_ref[len(_DPAPI_PREFIX):]).read_bytes()
        _, raw = win32crypt.CryptUnprotectData(blob, None, None, None, 0)
        return Ed25519PrivateKey.from_private_bytes(bytes(raw))
    raise SchemaError(f"unknown key_ref {key_ref!r}: expected {DEV_TEST_KEY_REF!r} or 'dpapi:<path>'")


def sign(payload: bytes, key_ref: str, *, run_mode: RunMode | None = None) -> str:
    """Ed25519 signature of ``payload`` (hex) with the key behind ``key_ref``.

    ``run_mode=RunMode.REAL`` refuses the DEV test key (``RunModeRefused``).
    """
    if key_ref == DEV_TEST_KEY_REF:
        _refuse_dev_in_real(run_mode, "sign")
    return _load_private_key(key_ref).sign(bytes(payload)).hex()


def verify_payload(payload: bytes, signature_hex: str, public_key: bytes) -> bool:
    """True iff ``signature_hex`` is a valid Ed25519 signature of ``payload`` under the raw ``public_key``."""
    try:
        Ed25519PublicKey.from_public_bytes(bytes(public_key)).verify(bytes.fromhex(signature_hex), bytes(payload))
    except (InvalidSignature, ValueError):
        return False
    return True


def verify(signoff: SignOff, roster: Mapping[str, bytes], *, run_mode: RunMode | None = None) -> bool:
    """Verify a ``SignOff`` against a roster ``{signer_hash: raw public key}``.

    Returns False for an unknown signer or a bad signature. A DEV test-signer sign-off (by signer hash, roster key
    or method label) raises ``RunModeRefused`` unless ``run_mode`` is ``RunMode.DEV_SYNTHETIC``.
    """
    public_key = roster.get(signoff.signer_hash)
    dev = signoff.is_dev_test or (public_key is not None and bytes(public_key) == dev_test_public_key())
    if dev and run_mode is not RunMode.DEV_SYNTHETIC:
        if run_mode is RunMode.REAL:
            _refuse_dev_in_real(run_mode, "verify")
        raise RunModeRefused("verify: a DEV test-signer sign-off verifies only with run_mode=DEV_SYNTHETIC "
                             "(S-ADR-37; fail closed when the run mode is not given)", {"facility": "dev_test_key"})
    if public_key is None:
        return False
    payload = signoff_payload(signoff.object_hash, signoff.role, signoff.signer_hash, signoff.signed_at)
    return verify_payload(payload, signoff.signature, public_key)


def protect_private_key(raw: bytes, path: Path) -> None:
    """Store a raw 32-byte Ed25519 private key at ``path`` as a DPAPI blob (current Windows user)."""
    import win32crypt  # pywin32; Windows only (S-ADR-40)

    if len(raw) != 32:
        raise SchemaError("an Ed25519 private key has 32 bytes")
    blob = win32crypt.CryptProtectData(bytes(raw), _DPAPI_DESCRIPTION, None, None, None, 0)
    Path(path).write_bytes(blob)


def generate_dpapi_key(path: Path) -> bytes:
    """Create a new Ed25519 key protected by DPAPI at ``path``; return its raw public key for the roster."""
    from cryptography.hazmat.primitives.serialization import NoEncryption, PrivateFormat

    key = Ed25519PrivateKey.generate()
    raw = key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    protect_private_key(raw, path)
    return public_key_bytes(key)
