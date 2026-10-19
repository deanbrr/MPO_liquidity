"""Ed25519 sign-offs (BUILD_SPEC v1.1 §4.1, S-ADR-40, S-ADR-37): round trip; tampered payload fails; the DEV
test key is refused in REAL mode; DPAPI-protected keys round trip on Windows. Owner WP-01."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from adic_tpa.contracts.contract import SignOff
from adic_tpa.contracts.enums import RunMode
from adic_tpa.contracts.errors import RunModeRefused, SchemaError
from adic_tpa.contracts.signing import (
    DEV_TEST_KEY_REF, DEV_TEST_SIGNER_HASH, dev_test_public_key, generate_dpapi_key, public_key_bytes, sign,
    signer_hash, signoff_payload, verify, verify_payload,
)

OBJ = "sha256:" + "ab" * 32
WHEN = datetime(2026, 10, 18, 9, 0, tzinfo=timezone.utc)
ROSTER = {DEV_TEST_SIGNER_HASH: dev_test_public_key()}
DEV = RunMode.DEV_SYNTHETIC


def dev_signoff(role: str = "CIO", obj: str = OBJ) -> SignOff:
    sig = sign(signoff_payload(obj, role, DEV_TEST_SIGNER_HASH, WHEN), DEV_TEST_KEY_REF)
    return SignOff(role=role, signer_hash=DEV_TEST_SIGNER_HASH, signed_at=WHEN, object_hash=obj,
                   method="dev_test_key", signature=sig)


def real_signoff(key: Ed25519PrivateKey, who: str = "S-1-5-21-synthetic-signer") -> tuple[SignOff, dict[str, bytes]]:
    """A non-DEV sign-off with an in-memory key (SYNTHETIC identity) and its roster."""
    sh = signer_hash(who)
    sig = key.sign(signoff_payload(OBJ, "CRO", sh, WHEN)).hex()
    return (SignOff(role="CRO", signer_hash=sh, signed_at=WHEN, object_hash=OBJ, method="ed25519_dpapi",
                    signature=sig), {sh: public_key_bytes(key)})


def test_round_trip() -> None:
    assert verify(dev_signoff(), ROSTER, run_mode=DEV)
    assert dev_signoff().is_dev_test and signer_hash("SYNTHETIC dev test signer") == DEV_TEST_SIGNER_HASH


def test_real_signoffs_verify_in_every_mode() -> None:
    signoff, roster = real_signoff(Ed25519PrivateKey.from_private_bytes(bytes(range(32))))
    assert not signoff.is_dev_test
    for mode in (None, RunMode.REAL, DEV):
        assert verify(signoff, roster, run_mode=mode)
    assert not verify(signoff.model_copy(update={"role": "CIO"}), roster, run_mode=RunMode.REAL)


def test_dev_signatures_are_deterministic() -> None:
    assert dev_signoff().signature == dev_signoff().signature   # Ed25519 is deterministic; Replay depends on it


def test_tampered_payload_fails() -> None:
    good = dev_signoff()
    assert not verify(good.model_copy(update={"object_hash": "sha256:" + "cd" * 32}), ROSTER, run_mode=DEV)
    assert not verify(good.model_copy(update={"role": "CRO"}), ROSTER, run_mode=DEV)
    assert not verify(good.model_copy(update={"signed_at": WHEN.replace(minute=1)}), ROSTER, run_mode=DEV)
    flipped = good.signature[:-1] + ("0" if good.signature[-1] != "0" else "1")
    assert not verify(good.model_copy(update={"signature": flipped}), ROSTER, run_mode=DEV)
    assert not verify(good.model_copy(update={"signature": "not-hex"}), ROSTER, run_mode=DEV)


def test_unknown_signer_fails() -> None:
    signoff, _ = real_signoff(Ed25519PrivateKey.from_private_bytes(bytes(range(32))))
    assert not verify(signoff, {signer_hash("someone else"): dev_test_public_key()}, run_mode=RunMode.REAL)
    assert not verify(dev_signoff(), {}, run_mode=DEV)


def test_dev_key_refused_in_real_mode() -> None:
    with pytest.raises(RunModeRefused) as exc:
        verify(dev_signoff(), ROSTER, run_mode=RunMode.REAL)
    assert exc.value.code == "RUN_MODE"
    with pytest.raises(RunModeRefused):
        sign(b"payload", DEV_TEST_KEY_REF, run_mode=RunMode.REAL)


def test_dev_signoff_needs_an_explicit_dev_mode() -> None:
    """Fail closed: without a run mode a DEV sign-off is refused, never silently accepted."""
    with pytest.raises(RunModeRefused, match="DEV_SYNTHETIC"):
        verify(dev_signoff(), ROSTER)


def test_relabelled_dev_signoff_is_refused_by_identity() -> None:
    """Review R07: ``method`` is not signed; relabelling a DEV signature must not get it past REAL mode."""
    relabelled = dev_signoff().model_copy(update={"method": "ed25519_dpapi"})
    assert relabelled.is_dev_test                                       # by signer hash
    with pytest.raises(RunModeRefused):
        verify(relabelled, ROSTER, run_mode=RunMode.REAL)
    assert verify(relabelled, ROSTER, run_mode=DEV)                     # the bytes still verify in DEV mode
    # a roster that files the DEV public key under another signer hash is caught by key identity
    alias = signer_hash("mislabelled roster entry")
    sig = sign(signoff_payload(OBJ, "CIO", alias, WHEN), DEV_TEST_KEY_REF)
    disguised = SignOff(role="CIO", signer_hash=alias, signed_at=WHEN, object_hash=OBJ, method="ed25519_dpapi",
                        signature=sig)
    assert not disguised.is_dev_test
    with pytest.raises(RunModeRefused):
        verify(disguised, {alias: dev_test_public_key()}, run_mode=RunMode.REAL)


def test_payload_is_canonical_json() -> None:
    payload = signoff_payload(OBJ, "CIO", DEV_TEST_SIGNER_HASH, WHEN)
    assert payload.startswith(b'{"object_hash":') and b'"signed_at":"2026-10-18T09:00:00Z"' in payload
    aware = WHEN.astimezone()                                  # same instant, local offset
    assert signoff_payload(OBJ, "CIO", DEV_TEST_SIGNER_HASH, aware) == payload


def test_unknown_key_ref() -> None:
    with pytest.raises(SchemaError):
        sign(b"x", "file:C:/keys/k.bin")


@pytest.mark.skipif(sys.platform != "win32", reason="DPAPI is Windows-only")
def test_dpapi_key_round_trip(tmp_path: Path) -> None:
    key_file = tmp_path / "signer.dpapi"
    public = generate_dpapi_key(key_file)
    assert len(public) == 32 and key_file.read_bytes()[:4] != b"\x00\x00\x00\x00"
    sig = sign(b"payload", f"dpapi:{key_file}", run_mode=RunMode.REAL)
    assert verify_payload(b"payload", sig, public)
    assert not verify_payload(b"payload2", sig, public)
