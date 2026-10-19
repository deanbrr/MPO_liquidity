"""LensAction schema rules (BUILD_SPEC v1.1 §3.13; ARCH §4.8; JE-MF9): REFINANCE = cash-out with exposure
unchanged; LEVER = exposure-up with new financing (≡ ADD + REFI). Owner WP-01."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from adic_tpa.contracts.actions import LensAction
from adic_tpa.contracts.enums import Lens


def action(lens: Lens, exp: float, fin: float, cash: float, unit: str | None = "SYN-PE-0042") -> LensAction:
    return LensAction(unit_id=unit, group="PE", lens=lens, instrument="x", size_bn=1.0, exposure_delta_bn=exp,
                      financing_delta_bn=fin, cash_out_bn=cash)


VALID = [
    (Lens.SELL, -1.0, 0.0, 0.9),
    (Lens.HOLD, 0.0, 0.0, 0.0),
    (Lens.REFINANCE, 0.0, 0.5, 0.5),
    (Lens.ADD, 0.4, 0.0, -0.4),
    (Lens.LEVER, 0.4, 0.4, 0.0),
]
INVALID = [
    (Lens.SELL, 0.0, 0.0, 0.0, "SELL requires exposure_delta_bn < 0"),
    (Lens.SELL, 0.5, 0.0, 0.0, "SELL requires"),
    (Lens.HOLD, 0.1, 0.0, 0.0, "HOLD requires"),
    (Lens.HOLD, 0.0, 0.1, 0.0, "HOLD requires"),
    (Lens.REFINANCE, 0.2, 0.5, 0.5, "REFINANCE requires"),       # exposure must not move
    (Lens.REFINANCE, 0.0, 0.0, 0.5, "REFINANCE requires"),       # needs new financing
    (Lens.REFINANCE, 0.0, 0.5, 0.0, "REFINANCE requires"),       # needs cash out
    (Lens.ADD, 0.4, 0.4, 0.0, "ADD requires"),                   # funded ADD is a LEVER
    (Lens.ADD, -0.4, 0.0, 0.0, "ADD requires"),
    (Lens.LEVER, 0.4, 0.0, 0.0, "LEVER requires"),               # unfunded LEVER is an ADD
    (Lens.LEVER, 0.0, 0.4, 0.4, "LEVER requires"),               # no exposure change is a REFINANCE
]


@pytest.mark.parametrize(("lens", "exp", "fin", "cash"), VALID)
def test_valid_lens_actions(lens: Lens, exp: float, fin: float, cash: float) -> None:
    assert action(lens, exp, fin, cash).lens is lens


@pytest.mark.parametrize(("lens", "exp", "fin", "cash", "msg"), INVALID)
def test_invalid_lens_actions(lens: Lens, exp: float, fin: float, cash: float, msg: str) -> None:
    with pytest.raises(ValidationError, match=msg):
        action(lens, exp, fin, cash)


def test_pace_is_group_level() -> None:
    assert action(Lens.PACE, 0.0, 0.0, 0.0, unit=None).unit_id is None
    with pytest.raises(ValidationError, match="PACE"):
        action(Lens.PACE, 0.0, 0.0, 0.0)


def test_zero_tolerance_is_1e_12() -> None:
    assert action(Lens.HOLD, 1e-13, -1e-13, 0.0).lens is Lens.HOLD
    with pytest.raises(ValidationError):
        action(Lens.HOLD, 1e-11, 0.0, 0.0)


def test_lever_equals_add_plus_refi_in_deltas() -> None:
    add = action(Lens.ADD, 0.4, 0.0, -0.4)
    refi = action(Lens.REFINANCE, 0.0, 0.4, 0.4)
    lever = action(Lens.LEVER, add.exposure_delta_bn + refi.exposure_delta_bn,
                   add.financing_delta_bn + refi.financing_delta_bn, add.cash_out_bn + refi.cash_out_bn)
    assert lever.cash_out_bn == 0.0     # cash-neutral: ℓ̄ cancels (ARCH §4.8)
