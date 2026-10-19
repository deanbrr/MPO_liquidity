"""Mini fixtures (BUILD_SPEC v1.1 §4.5; owner WP-03): book, world, state, register, contract, cube, FlowCube.

SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np
import pytest

from adic_tpa.contracts.enums import (
    DataClass, ExitWindow, FactorKind, FlowType, MacroRegime, RunMode, ShockType, StressState,
)
from adic_tpa.contracts.errors import RunModeRefused, SchemaError
from adic_tpa.contracts.signing import dev_test_public_key, verify
from adic_tpa.contracts.taxonomy import GroupRegistry
from adic_tpa.contracts.world import validate_world_id
from adic_tpa.testing import (
    MINI_ASSET_CLASSES, MINI_FACTORS, book_hold_flows, fake_beliefs, mini_book, mini_contract, mini_cube,
    mini_flowcube, mini_owner_config, mini_register, mini_state0, mini_world,
)
from adic_tpa.testing.fixtures import ALLOCATIONS, MINI_FACTOR_KINDS


@pytest.mark.parametrize("allocation", ["v1", "v2"])
def test_mini_book_structure(allocation: str) -> None:
    book = mini_book(allocation)
    tax = GroupRegistry.for_version(book.taxonomy_version)
    assert book.taxonomy_version == allocation and book.allocation == allocation
    assert book.census_id == {"v1": "v1.0", "v2": "v1.1"}[allocation]
    kinds = Counter(h.unit_kind for h in book.holdings)
    assert kinds["hf_lot"] == 3 and kinds["longonly"] == 2 and kinds["treasury"] == 3 and kinds["overlay_bucket"] == 3
    idx = book.unit_index(tax)
    for g in tax.private():                                   # one unit per private group × age bucket
        buckets = sorted(int(b) for u, b, gi in zip(idx.unit_ids, idx.age_bucket, idx.group_of, strict=True)
                         if gi == tax.index(g))
        assert buckets == [0, 1], g
    assert len(book.overlay.trades) == 5 and len(book.overlay.csas) == 2 and len(book.overlay.services) == 1


@pytest.mark.parametrize("allocation", ["v1", "v2"])
def test_mini_book_follows_the_working_allocation(allocation: str) -> None:
    book = mini_book(allocation)
    by_group: dict[str, float] = {}
    for h in book.holdings:
        by_group[str(h.group)] = by_group.get(str(h.group), 0.0) + h.nav_reported_bn
    for g, nav in ALLOCATIONS[allocation].items():
        assert by_group[g] == pytest.approx(nav, abs=1e-9)
    assert book.nav_total_reported_bn == pytest.approx(177.0, abs=1e-9)        # context §1A: $177bn


@pytest.mark.parametrize("allocation", ["v1", "v2"])
def test_mini_book_is_synthetic_and_hashed(allocation: str) -> None:
    from adic_tpa.contracts.hashing import content_hash

    book = mini_book(allocation)
    assert book.data_class is DataClass.SYNTHETIC
    assert all(h.is_synthetic and str(h.holding_id).startswith("SYN-") for h in book.holdings)
    assert all(t.is_synthetic for t in book.overlay.trades)
    assert book.content_hash == content_hash(book.hash_payload())
    assert mini_book(allocation).content_hash == book.content_hash


def test_mini_book_seed_moves_splits_not_totals() -> None:
    a, b = mini_book("v2", seed=7), mini_book("v2", seed=8)
    assert a.content_hash != b.content_hash
    assert a.nav_total_reported_bn == pytest.approx(b.nav_total_reported_bn)


def test_mini_book_rejects_unknown_allocation() -> None:
    with pytest.raises(SchemaError):
        mini_book("v3")  # type: ignore[arg-type]


def test_mini_cube_shapes_names_and_kinds() -> None:
    cube = mini_cube()
    cube.validate()
    assert cube.factors.shape == (200, 120, len(MINI_FACTORS))
    assert cube.meta.factor_names == MINI_FACTORS and cube.meta.factor_kinds == MINI_FACTOR_KINDS
    assert {MINI_FACTORS[i] for i, k in enumerate(MINI_FACTOR_KINDS) if k is FactorKind.LOGRET} == {"us_eq", "brent_log"}
    assert cube.meta.asset_names == MINI_ASSET_CLASSES and cube.meta.is_synthetic
    assert cube.draw_rate is None and cube.group_rates is None


def test_mini_cube_is_deterministic_and_path_prefix_stable() -> None:
    big, small = mini_cube(200), mini_cube(50)
    assert big.checksum() == mini_cube(200).checksum()
    for name in ("factors", "regimes", "stress_post", "asset_returns", "brent", "fin_window"):
        assert np.array_equal(getattr(small, name), getattr(big, name)[:50]), name


def test_mini_cube_worlds_and_seeds_differ() -> None:
    m1, m6 = mini_cube(200, "M1"), mini_cube(200, "M6")
    assert m1.meta.checksum != m6.meta.checksum
    crisis = lambda c: float((c.regimes[:, :, 0] == MacroRegime.CRIS).mean())  # noqa: E731
    assert crisis(m6) > crisis(m1)
    assert mini_cube(20, seed=1).meta.checksum != mini_cube(20, seed=2).meta.checksum


def test_mini_cube_regimes_drive_the_derived_series() -> None:
    cube = mini_cube()
    crisis = cube.regimes[:, :, 0] == MacroRegime.CRIS
    assert np.array_equal(cube.regimes[:, :, 1] == ExitWindow.D, crisis)
    assert np.array_equal(cube.regimes[:, :, 2] == ShockType.DB, crisis)
    post = cube.stress_post[:, :, StressState.CRISIS]
    assert post[crisis].mean() > post[~crisis].mean() + 0.2      # the filter sees the crisis
    hy = cube.factors[:, :, MINI_FACTORS.index("hy_spread")]
    assert hy.min() >= 0.005 and (cube.brent > 0).all()


@pytest.mark.parametrize("bad", [0, 2001])
def test_mini_cube_is_one_block(bad: int) -> None:
    with pytest.raises(SchemaError):
        mini_cube(bad)


def test_mini_flowcube_is_the_hold_run_of_the_engines() -> None:
    book, cube = mini_book("v2"), mini_cube(40)
    fc = mini_flowcube(book, cube)
    fc.validate()
    units, values = book_hold_flows(book, cube, beliefs=fake_beliefs(book))
    assert fc.meta.unit_ids == tuple(m.unit_id for m in units)
    assert fc.meta.cube_checksum == cube.meta.checksum and fc.meta.action is None
    assert np.array_equal(fc.values, values.astype(np.float32))
    assert "treasury" not in {m.engine_id for m in units}
    assert (fc.values[..., FlowType.CALL] <= 0).all() and (fc.values[..., FlowType.DISTRIBUTION] >= 0).all()
    assert (fc.values[..., FlowType.PIK_ACCRUAL] >= 0).all()


@pytest.mark.parametrize("world", ["M1", "M2", "M5", "M6", "B1", "B2", "MS:fat_tails"])
def test_mini_world_every_id(world: str) -> None:
    w = mini_world(world)
    assert w.world_id == validate_world_id(world) and set(w.cma) == set(MINI_ASSET_CLASSES)
    assert w.t6_class == ("M6" if world == "M6" or world.startswith("MS:") else "M1_M5")
    assert (w.bootstrap is not None) == (world in ("B1", "B2"))


def test_mini_world_stress_lowers_risky_means() -> None:
    m1, m6 = mini_world("M1"), mini_world("M6")
    assert m6.cma["pe_buyout"].arith_mean_a < m1.cma["pe_buyout"].arith_mean_a
    assert m6.cma["cash"].arith_mean_a == m1.cma["cash"].arith_mean_a


def test_mini_state0_and_owner_config() -> None:
    s = mini_state0()
    assert s.e0[ExitWindow.D] == pytest.approx(0.87) and math.isclose(sum(s.z0), 1.0)
    assert set(s.factor_levels0) == {n for n, k in zip(MINI_FACTORS, MINI_FACTOR_KINDS) if k is FactorKind.LEVEL}
    o = mini_owner_config()
    assert o.override_p_a[ShockType.GW] == 0.02 and o.p_accept_band[ShockType.DB] == 0.30


def test_mini_register_is_signed_by_the_dev_signer() -> None:
    reg = mini_register()
    assert [e.id for e in reg.entries] == ["Q1", "Q2"]
    so = reg.signoffs[0]
    roster = {so.signer_hash: dev_test_public_key()}
    assert verify(so, roster, run_mode=RunMode.DEV_SYNTHETIC)
    with pytest.raises(RunModeRefused):
        verify(so, roster, run_mode=RunMode.REAL)


def test_mini_contract_dev_and_real() -> None:
    c = mini_contract()
    assert c.run_mode is RunMode.DEV_SYNTHETIC and c.data_class is DataClass.SYNTHETIC
    assert c.allocation == "v2" and c.tier1.theta_star == pytest.approx(0.58)
    assert sum(c.objective.model_weights.values()) == pytest.approx(1.0)
    with pytest.raises(RunModeRefused):                       # REAL refuses the DEV test signer (S-ADR-37)
        mini_contract(run_mode=RunMode.REAL)
