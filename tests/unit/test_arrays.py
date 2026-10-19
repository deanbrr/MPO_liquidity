"""Array contracts (BUILD_SPEC v1.1 §1.5, §3.17, §4.1): ARRAY_SPECS checks, checksums, npz round trips. Owner WP-01."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from scipy import sparse  # imported at collection: the first import costs ~1 s

from adic_tpa.contracts.arrays import ARRAY_SPECS, INVARIANTS, MAX_BLOCK_PATHS, ArraySpec, validate_container
from adic_tpa.contracts.beliefs import BeliefMeta, BeliefSet
from adic_tpa.contracts.engine_io import ActionSlice, FlowCube, FlowCubeMeta, FlowSlice, NoiseRequest, NoiseSlice
from adic_tpa.contracts.enums import Clock, FlowType, RecourseTier
from adic_tpa.contracts.errors import HashMismatch, SchemaError
from adic_tpa.contracts.ledger import RecourseAvailability, RecourseOutcome, StressReport
from adic_tpa.contracts.optimizer import ColKey, LPMeta, LPModel, RowKey
from adic_tpa.contracts.enums import RowFamily
from adic_tpa.contracts.policy import Observables

P = 4


def noise(u_value: float = 0.5) -> NoiseSlice:
    req = NoiseRequest.model_validate_json(json.dumps(
        {"source": "priv.fund.idio", "slots": 2, "entity_ids": ["SYN-PE-0001", "SYN-PE-0002", "SYN-PE-0003"],
         "months": [0, 1, 2]}))
    req2 = NoiseRequest.model_validate_json(json.dumps({"source": "sale.success", "slots": 1, "entity_ids": None,
                                                        "months": [2]}))
    return NoiseSlice(requests=(req, req2), u={"priv.fund.idio": np.full((P, 3, 3, 2), u_value),
                                               "sale.success": np.full((P, 1, 1, 1), 0.25)})


def flows(**overrides: np.ndarray) -> FlowSlice:
    by_group = np.zeros((P, 2, 18), dtype=np.float32)
    by_group[:, 0, FlowType.CALL] = -1.0
    by_group[:, 0, FlowType.DISTRIBUTION] = 2.0
    by_group[:, 1, FlowType.VM] = -0.3                                # VM may take either sign
    intra = np.zeros((P, 2, 18), dtype=np.float32)
    intra[:, 0, FlowType.FEES], intra[:, 1, FlowType.FEES] = -0.1, 0.1
    kw = dict(engine_id="priv.fund", clock=Clock.QUARTERLY, t=0, by_group=by_group, intra=intra, by_unit=None,
              recourse_unit_ids=("SYN-PE-0001",), by_recourse_unit=np.zeros((P, 1, 18), dtype=np.float32),
              nav_econ=np.ones((P, 3), dtype=np.float32), nav_rep=np.ones((P, 3), dtype=np.float32),
              unfunded=np.zeros((P, 3), dtype=np.float32), encumbered=np.zeros((P, 3), dtype=np.float32),
              hqla_contrib_bn=np.zeros(P, dtype=np.float32))
    kw.update(overrides)
    return FlowSlice(**kw)


def quotes() -> RecourseAvailability:
    return RecourseAvailability(
        engine_id="priv.fund", unit_ids=("SYN-PE-0001", "SYN-PC-0001"), group_of=("PE", "PRIVCREDIT"),
        bid_frac=np.full((P, 2), 0.9, dtype=np.float32), normal_bid_frac=np.array([0.93, 0.97], dtype=np.float32),
        depth_frac=np.full((P, 2), 0.25, dtype=np.float32), lag_m=np.ones((P, 2), dtype=np.int8),
        tier=np.array([2, 1], dtype=np.int8))


def outcome(sold: float = 0.1, red_amber: bool = False) -> RecourseOutcome:
    sold_frac = np.zeros((P, 2), dtype=np.float32)
    sold_frac[0] = sold
    red = np.zeros((P, 2), dtype=bool)
    red[0, 0] = sold > 0
    red[0, 1] = red_amber and sold > 0
    month = np.full((P, 2), -1, dtype=np.int16)
    month[0] = 2 if sold > 0 else -1
    return RecourseOutcome(unit_ids=("SYN-PE-0001", "SYN-PC-0001"), sold_frac=sold_frac, month=month,
                           proceeds_bn=np.where(sold_frac > 0, 0.5, 0.0), red=red,
                           reason=np.zeros((P, 2), dtype=np.int8))


def stress_report() -> StressReport:
    headroom = np.tile(np.linspace(1.0, -2.0, 24), (P, 1))
    return StressReport(spec_hash="sha256:" + "1" * 64, headroom_bn=headroom, nco_bn=np.zeros((P, 24)),
                        cbc_bn={RecourseTier.T: np.ones((P, 24)), RecourseTier.TP: np.full((P, 24), 2.0)},
                        survival_months={RecourseTier.TP: np.full(P, 17, dtype=np.int16)}, gap_bn=np.zeros(P),
                        d0_bn=np.full(P, 2.0))


def lp_model() -> LPModel:
    meta = LPMeta.model_validate_json(json.dumps({
        "tree_hash": "t", "contract_hash": "c", "catalogue_hash": "k", "ledger_hash": "l", "builder_version": "1",
        "consent_scenario": "R0", "pricing_level": "tolerance", "replication": 0}))
    A = sparse.csc_array(np.array([[1.0, 2.0], [0.0, -1.0], [3.0, 0.0]]))
    return LPModel(name="H", meta=meta, c=np.array([1.0, -0.5]), A=A, row_lo=np.array([-np.inf, 0.0, 0.0]),
                   row_hi=np.array([1.0, np.inf, 5.0]), col_lo=np.zeros(2), col_hi=np.array([np.inf, 10.0]),
                   integrality=None,
                   row_keys=(RowKey(family=RowFamily.T4P, idx=(("h", 24),)), RowKey(family=RowFamily.LR8),
                             RowKey(family=RowFamily.T1_PAYOUT)),
                   col_keys=(ColKey(family="decision", name="sell", node=0), ColKey(family="state", name="cash")),
                   row_role=np.array([1, 3, 0], dtype=np.int8), row_tier=np.array([2, 0, 1], dtype=np.int8),
                   node_of_row=np.zeros(3, dtype=np.int32), node_of_col=np.zeros(2, dtype=np.int32), scale_bn=177.0)


def test_valid_containers_pass() -> None:
    for obj in (noise(), flows(), quotes(), outcome(), stress_report(), lp_model(),
                ActionSlice.empty(0, P, 3, 2, 1, 2)):
        obj.validate()
    outcome().check_against(quotes())


def test_shape_symbols_bind_across_fields() -> None:
    with pytest.raises(SchemaError, match="axis"):
        flows(nav_rep=np.ones((P, 4), dtype=np.float32)).validate()          # UE disagrees with nav_econ
    with pytest.raises(SchemaError, match="axis"):
        flows(by_recourse_unit=np.zeros((P, 2, 18), dtype=np.float32)).validate()   # UR vs recourse_unit_ids
    with pytest.raises(SchemaError, match="size 18"):
        flows(by_group=np.zeros((P, 2, 17), dtype=np.float32)).validate()


def test_dtype_rank_contiguity_and_nan() -> None:
    with pytest.raises(SchemaError, match="dtype"):
        flows(hqla_contrib_bn=np.zeros(P)).validate()                        # float64 instead of float32
    with pytest.raises(SchemaError, match="rank"):
        flows(hqla_contrib_bn=np.zeros((P, 1), dtype=np.float32)).validate()
    with pytest.raises(SchemaError, match="C-contiguous"):
        flows(nav_econ=np.ones((3, P), dtype=np.float32).T).validate()
    bad = np.ones((P, 3), dtype=np.float32)
    bad[1, 1] = np.nan
    with pytest.raises(SchemaError, match="non-finite"):
        flows(nav_econ=bad).validate()


def test_flow_sign_and_netting_invariants() -> None:
    wrong = flows().by_group.copy()
    wrong[0, 0, FlowType.CALL] = 1.0                                         # a positive call
    with pytest.raises(SchemaError, match="negative-sign FlowType"):
        flows(by_group=wrong).validate()
    negative_dist = flows().by_group.copy()
    negative_dist[0, 0, FlowType.DISTRIBUTION] = -0.5                        # a negative distribution
    with pytest.raises(SchemaError, match="positive-sign FlowType"):
        flows(by_group=negative_dist).validate()
    tiny = flows().by_group.copy()
    tiny[0, 0, FlowType.DISTRIBUTION] = -1e-13                               # within 1e-12
    flows(by_group=tiny).validate()
    unbalanced = flows().intra.copy()
    unbalanced[0, 1, FlowType.FEES] = 0.2
    with pytest.raises(SchemaError, match="sum to 0"):
        flows(intra=unbalanced).validate()


def test_three_party_float32_intra_flows_net_to_zero() -> None:
    """Review R03: the overlay bills client A 0.1 and client B 0.2; its row is fee_a + fee_b in float32, which
    leaves a 7.45e-9 residual: legitimate data the plain 1e-9 rule rejected."""
    fee_a, fee_b = np.float32(0.1), np.float32(0.2)
    intra = np.zeros((P, 3, 18), dtype=np.float32)
    intra[:, 0, FlowType.FEES], intra[:, 1, FlowType.FEES] = -fee_a, -fee_b
    intra[:, 2, FlowType.FEES] = fee_a + fee_b
    residual = abs(float(intra[0, :, FlowType.FEES].astype(np.float64).sum()))
    assert 1e-9 < residual < 1e-7
    three = dict(by_group=np.zeros((P, 3, 18), dtype=np.float32), intra=intra)
    flows(**three).validate()
    off = intra.copy()
    off[0, 2, FlowType.FEES] += np.float32(1e-5)                             # a real imbalance still fails
    with pytest.raises(SchemaError, match="sum to 0"):
        flows(by_group=three["by_group"], intra=off).validate()


def test_float64_netting_keeps_the_1e9_rule() -> None:
    check = INVARIANTS["sum_axis1_zero"]
    x = np.zeros((1, 3, 1))
    x[0, :, 0] = [-0.1, -0.2, 0.3 + 2e-9]                                    # 2e-9 residual on a scale of 1
    with pytest.raises(SchemaError, match="sum to 0"):
        check(x, "f64")
    x[0, 2, 0] = 0.3 + 5e-10
    check(x, "f64")


def test_noise_invariants() -> None:
    with pytest.raises(SchemaError, match=r"\[0.0, 1.0\)"):
        noise(1.0).validate()
    n = noise()
    bad = NoiseSlice(requests=n.requests, u={**n.u, "sale.success": np.full((P, 1, 1, 2), 0.25)})
    with pytest.raises(SchemaError, match="disagrees with its request"):
        bad.validate()


def test_recourse_outcome_checks() -> None:
    with pytest.raises(SchemaError, match="tier = red"):
        outcome(red_amber=True).check_against(quotes())
    with pytest.raises(SchemaError, match="depth"):
        outcome(sold=0.5).check_against(quotes())
    o = outcome()
    with pytest.raises(SchemaError, match="sale month"):
        RecourseOutcome(unit_ids=o.unit_ids, sold_frac=o.sold_frac, month=np.full((P, 2), -1, dtype=np.int16),
                        proceeds_bn=o.proceeds_bn, red=np.zeros((P, 2), dtype=bool), reason=o.reason).validate()


def test_stress_report_d0() -> None:
    s = stress_report()
    with pytest.raises(SchemaError, match="d0_bn"):
        StressReport(spec_hash=s.spec_hash, headroom_bn=s.headroom_bn, nco_bn=s.nco_bn, cbc_bn=s.cbc_bn,
                     survival_months=s.survival_months, gap_bn=s.gap_bn, d0_bn=np.zeros(P)).validate()


def test_lp_model_bounds_and_coefficients() -> None:
    m = lp_model()
    big = LPModel(**{**{f: getattr(m, f) for f in m.__dataclass_fields__}, "A": sparse.csc_array(np.array(
        [[1e5, 0.0], [0.0, 1.0], [1.0, 0.0]]))})
    with pytest.raises(SchemaError, match="1e4"):
        big.validate()
    nan_lo = LPModel(**{**{f: getattr(m, f) for f in m.__dataclass_fields__}, "row_lo": np.array([np.nan, 0, 0.0])})
    with pytest.raises(SchemaError, match="NaN"):
        nan_lo.validate()


def test_checksum_is_stable_and_sensitive() -> None:
    a, b = flows(), flows()
    assert a.checksum() == b.checksum() and a.checksum().startswith("sha256:")
    changed = flows(hqla_contrib_bn=np.ones(P, dtype=np.float32))
    assert changed.checksum() != a.checksum()
    assert stress_report().checksum() == stress_report().checksum()


@pytest.mark.parametrize("make", [noise, flows, quotes, outcome, stress_report, lp_model,
                                  lambda: ActionSlice.empty(3, P, 3, 2, 1, 2)])
def test_npz_round_trip(tmp_path: Path, make) -> None:
    obj = make()
    path = tmp_path / "c.npz"
    checksum = obj.to_npz(path)
    back = type(obj).from_npz(path, expected_checksum=checksum)
    assert back.checksum() == checksum
    back.validate()
    with pytest.raises(HashMismatch):
        type(obj).from_npz(path, expected_checksum="sha256:" + "0" * 64)


def test_npz_round_trip_with_empty_mappings(tmp_path: Path) -> None:
    obs = Observables(t=2, values={"F_t": np.zeros(P, dtype=np.float32)}, unit_values={}, group_values={})
    path = tmp_path / "obs.npz"
    back = Observables.from_npz(path, expected_checksum=obs.to_npz(path))
    assert back.unit_values == {} and back.world_hidden is True and back.t == 2


def test_npz_class_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "q.npz"
    quotes().to_npz(path)
    with pytest.raises(SchemaError, match="holds a RecourseAvailability"):
        RecourseOutcome.from_npz(path)


def test_belief_set_invariants() -> None:
    meta = BeliefMeta.model_validate_json(json.dumps({
        "asof": "2026-09-30", "fbe_version": "fbe-r-1", "prior_hash": "p", "inputs_hash": "i",
        "frozen_optimizer_outputs_hash": "f", "data_class": "SYNTHETIC", "content_hash": "sha256:" + "2" * 64}))
    alpha, bench = np.array([0.01, -0.02]), np.array([0.07, 0.06])
    kw = dict(meta=meta, unit_ids=("SYN-PE-0001", "SYN-PE-0002"), alpha_a=alpha, benchmark_id=("us_eq", "us_eq"),
              beta_hat=np.ones(2), bench_ref_a=bench, mu_total_a=bench + alpha, sigma_hat=np.full(2, 0.2),
              band80=np.stack([bench + alpha - 0.1, bench + alpha + 0.1], axis=1), mu_p10=bench + alpha - 0.1,
              weights=np.full((2, 4), 0.25), market_anchor=np.zeros(2), has_market=np.zeros(2, dtype=bool),
              nowcast_nav_bn=np.ones(2), flags=np.array([0b1, 1 << 10], dtype=np.uint32),
              p_achieved=np.full((2, 2), 0.5), group_bias_mean=np.zeros(3), group_bias_sd=np.ones(3),
              kappa=np.full(3, 1.75))
    bs = BeliefSet(**kw)
    bs.validate()
    assert bs.flag_names(0) == ("F1",) and bs.flag_names(1) == ("ZOMBIE",)
    with pytest.raises(SchemaError, match="bench_ref_a"):
        BeliefSet(**{**kw, "mu_total_a": bench}).validate()
    with pytest.raises(SchemaError, match="band80"):
        BeliefSet(**{**kw, "band80": np.stack([bench + alpha, bench + alpha + 0.1], axis=1)}).validate()


def test_observables_mappings_share_path_and_entity_axes() -> None:
    obs = Observables(t=4, values={"F_t": np.zeros(P, dtype=np.float32)},
                      unit_values={"bid_ce": np.ones((P, 3), dtype=np.float32)},
                      group_values={"envelope_use": np.ones((P, 2), dtype=np.float32)})
    obs.validate()
    bad = Observables(t=4, values={"F_t": np.zeros(P + 1, dtype=np.float32)}, unit_values={}, group_values={})
    with pytest.raises(SchemaError):
        Observables(t=4, values={"F_t": np.zeros(P, dtype=np.float32)},
                    unit_values={"bid_ce": np.ones((P + 1, 3), dtype=np.float32)}, group_values={}).validate()
    bad.validate()                                                            # a lone mapping binds P itself


def test_action_slice_defaults_and_order() -> None:
    a = ActionSlice.empty(0, P, 3, 2, 1, 2, recourse_order=(5, 4, 3, 2, 1, 0))
    a.validate()
    assert a.recourse_order.shape == (P, 6) and a.sma_runoff.min() == 1.0
    a.sell_frac[0, 0] = 1.5                                                    # mutable slice; invariant catches it
    with pytest.raises(SchemaError, match=r"\[0.0, 1.0\]"):
        a.validate()
    with pytest.raises(SchemaError):
        ActionSlice.empty(0, P, 3, 2, 1, 2, recourse_order=(0, 1, 2))


def test_validate_container_is_the_functional_alias() -> None:
    validate_container(flows())
    bad = flows(hqla_contrib_bn=np.zeros(P))
    with pytest.raises(SchemaError, match="dtype"):
        validate_container(bad)


def test_frozen_containers_hold_read_only_views() -> None:
    """Review R15: a frozen container owns its arrays; an in-place edit through it raises, the caller's array is
    untouched and the checksum cannot drift."""
    hqla = np.zeros(P, dtype=np.float32)
    fs = flows(hqla_contrib_bn=hqla)
    before = fs.checksum()
    with pytest.raises(ValueError, match="read-only"):
        fs.hqla_contrib_bn[0] = 1.0
    with pytest.raises(ValueError, match="read-only"):
        fs.intra[0, 0, 0] = 1.0
    assert hqla.flags.writeable and fs.checksum() == before
    n = noise()
    with pytest.raises(ValueError, match="read-only"):
        n.u["priv.fund.idio"][0, 0, 0, 0] = 0.9                               # dict-of-array fields too
    report = stress_report()
    with pytest.raises(ValueError, match="read-only"):
        report.survival_months[RecourseTier.TP][0] = 99


def test_mutable_containers_stay_writable() -> None:
    a = ActionSlice.empty(0, P, 3, 2, 1, 2)
    a.sell_frac[0, 0] = 0.5
    assert a.sell_frac[0, 0] == np.float32(0.5)


def test_pickle_and_copies_rebuild_frozen_containers() -> None:
    import copy
    import pickle

    fs = flows()
    for clone in (pickle.loads(pickle.dumps(fs)), copy.deepcopy(fs), copy.copy(fs)):
        assert type(clone) is FlowSlice and clone.checksum() == fs.checksum()
        assert not clone.by_group.flags.writeable
        clone.validate()
    a = ActionSlice.empty(1, P, 3, 2, 1, 2)
    back = pickle.loads(pickle.dumps(a))
    assert back.t == 1 and back.sell_frac.flags.writeable and back.checksum() == a.checksum()


def test_flow_cube_holds_at_most_one_block() -> None:
    meta = FlowCubeMeta.model_validate_json(json.dumps({"unit_ids": ["SYN-PE-0001"], "group_of": ["PE"],
                                                        "quarters": 2, "cube_checksum": "sha256:" + "0" * 64}))
    FlowCube(meta=meta, values=np.zeros((MAX_BLOCK_PATHS, 2, 1, 18), dtype=np.float32)).validate()
    with pytest.raises(SchemaError, match="one block"):
        FlowCube(meta=meta, values=np.zeros((MAX_BLOCK_PATHS + 1, 2, 1, 18), dtype=np.float32)).validate()


def test_spec_table_is_well_formed() -> None:
    for owner, specs in ARRAY_SPECS.items():
        for name, spec in specs.items():
            assert isinstance(spec, ArraySpec)
            for inv in spec.invariants:
                assert inv == "allow_inf" or inv in INVARIANTS, f"{owner}.{name}: unknown invariant {inv}"
            if spec.kind in ("array", "mapping", "sparse"):
                np.dtype(spec.dtype)
