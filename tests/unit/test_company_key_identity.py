"""Company key identity (BUILD_SPEC v1.1 §4.2 tests; §1.7; gate V24a). Owner WP-02.

Company draws use ``entity_key(company_id)``, so every ADIC claim on one company — a co-investment, a Capital
Solutions instrument, a fund's look-through position — reads the same EV draw per path, whichever engine, block
or entity list asks for it. SYNTHETIC ids only.
"""

from __future__ import annotations

import numpy as np

from adic_tpa.contracts.engine_io import NoiseRequest
from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import base_entropy, draw_block, entity_key, stream_key, uniforms

BASE = base_entropy(20261019, Plane.SEARCH, "M1")
SOURCE = "priv.company.ev"
COMPANY = "SYN-CMP-000417"
PATHS = np.arange(2000)
MONTHS = np.array([0, 1, 2])


def test_two_claims_on_one_company_read_identical_ev_draws() -> None:
    # entity list built from claims: (co-investment claim -> company), (capsol claim -> same company), other company
    claim_companies = [COMPANY, COMPANY, "SYN-CMP-000999"]
    u = uniforms(BASE, SOURCE, claim_companies, PATHS, MONTHS, 1)
    assert np.array_equal(u[:, :, 0], u[:, :, 1])
    assert not np.array_equal(u[:, :, 0], u[:, :, 2])


def test_identity_holds_across_engines_blocks_and_lists() -> None:
    a = draw_block(BASE, [NoiseRequest(source=SOURCE, slots=1, entity_ids=(COMPANY, "SYN-CMP-000001"),
                                       months=(0, 1, 2))], PATHS[:1000])
    b = draw_block(BASE, [NoiseRequest(source=SOURCE, slots=1, entity_ids=("SYN-CMP-000002", COMPANY),
                                       months=(0, 1, 2))], PATHS)
    assert np.array_equal(a.u[SOURCE][:, :, 0], b.u[SOURCE][:1000, :, 1])


def test_the_key_depends_on_the_company_id_only() -> None:
    k = stream_key(BASE, SOURCE, entity_key(COMPANY))
    assert k.tolist() == stream_key(BASE, SOURCE, entity_key(str(COMPANY))).tolist()
    assert k.tolist() != stream_key(BASE, SOURCE, entity_key("SYN-CMP-000418")).tolist()
