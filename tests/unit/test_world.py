"""World, cube and tree contracts (BUILD_SPEC v1.1 §3.6, §3.7, §3.17). Owner WP-01. SYNTHETIC values only."""

from __future__ import annotations

import json

import numpy as np
import pytest
from pydantic import ValidationError

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.optimizer import NodeCoefficients
from adic_tpa.contracts.policy import PolicyRef
from adic_tpa.contracts.world import (
    SCENARIO_ARRAYS, CubeMeta, GroupRates, GroupRatesMeta, ScenarioCube, StatePanel, Tree, TreeSpec, WorldSpec,
    scenario_identity, validate_world_id,
)

P, M, K, A = 3, 6, 2, 2


def cube_arrays(seed: int = 0) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    post = rng.random((P, M, 3)).astype(np.float32)
    post /= post.sum(axis=2, keepdims=True)
    regimes = np.zeros((P, M, 3), dtype=np.int8)
    regimes[..., 2] = 5                                                      # ShockType.GW
    return {"factors": rng.normal(size=(P, M, K)).astype(np.float32), "regimes": regimes, "stress_post": post,
            "vol": np.zeros((P, M, 3), dtype=np.float32), "fin_window": np.ones((P, M), dtype=np.int8),
            "crowding_index": np.zeros((P, M), dtype=np.float32),
            "asset_returns": rng.normal(0, 0.01, (P, M, A)).astype(np.float32),
            "brent": np.full((P, M), 70.0, dtype=np.float32)}


META = {"world_id": "M1", "plane": "SEARCH", "base_entropy_hex": "00ff", "generator_hash": "g", "asof": "2026-09-30",
        "n_paths": P, "path_offset": 0, "months": M, "factor_names": ["us_eq", "short_rate"],
        "factor_kinds": ["logret", "level"], "asset_names": ["us_eq", "pe_buyout"], "is_synthetic": True,
        "data_class": "SYNTHETIC", "checksum": ""}


def cube_meta(**changes) -> CubeMeta:
    return CubeMeta.model_validate_json(json.dumps({**META, **changes}))


def cube(**overrides) -> ScenarioCube:
    """A cube whose meta.checksum is the identity of the unmodified arrays; ``overrides`` replace arrays after."""
    arrays = cube_arrays()
    identity = scenario_identity(cube_meta(), arrays)
    return ScenarioCube(meta=cube_meta(checksum=identity), **{**arrays, **overrides})


def test_cube_validates_and_checksums_exclude_meta() -> None:
    c = cube()
    c.validate()
    assert c.scenario_checksum() == c.meta.checksum and c.meta.checksum.startswith("sha256:")
    with_draws = cube(draw_rate=np.full((P, 11), 0.058, dtype=np.float32), draw_override=np.zeros((P, 11), bool))
    with_draws.validate()                                                    # attaching draws keeps the identity
    assert with_draws.scenario_checksum() == c.scenario_checksum() and with_draws.checksum() != c.checksum()
    built = ScenarioCube.build(cube_meta(checksum="stale"), **cube_arrays())  # build() sets the identity
    built.validate()
    assert built.meta.checksum == c.meta.checksum and built.checksum() == c.checksum()


@pytest.mark.parametrize(("field", "value"), [("world_id", "M6"), ("plane", "FINAL"), ("path_offset", 2000),
                                              ("factor_kinds", ["logret", "change"]), ("asof", "2026-12-31"),
                                              ("generator_hash", "g2"), ("asset_names", ["us_eq", "pe_growth"])])
def test_relabelling_a_cube_changes_both_checksums(field: str, value: object) -> None:
    """Review R08: the identity binds the generating meta, so a relabelled cube no longer validates."""
    c = cube()
    relabelled = ScenarioCube(meta=cube_meta(**{field: value, "checksum": c.meta.checksum}),
                              **{name: getattr(c, name) for name in SCENARIO_ARRAYS})
    assert relabelled.checksum() != c.checksum()
    with pytest.raises(SchemaError, match="meta.checksum"):
        relabelled.validate()
    rebuilt = ScenarioCube.build(relabelled.meta, **{name: getattr(c, name) for name in SCENARIO_ARRAYS})
    rebuilt.validate()
    assert rebuilt.meta.checksum != c.meta.checksum


def test_container_checksum_ignores_only_the_derived_meta_checksum() -> None:
    c = cube()
    restamped = ScenarioCube(meta=cube_meta(checksum="sha256:" + "e" * 64),
                             **{name: getattr(c, name) for name in SCENARIO_ARRAYS})
    assert restamped.checksum() == c.checksum()
    with pytest.raises(SchemaError, match="missing scenario arrays"):
        scenario_identity(c.meta, {"factors": c.factors})


def test_cube_invariants() -> None:
    tampered = cube_arrays()["factors"].copy()
    tampered[0, 0, 0] += 1.0
    with pytest.raises(SchemaError, match="meta.checksum"):
        cube(factors=tampered).validate()
    rates = np.full((P, 11), 0.058, dtype=np.float32)
    rates[0, 1] = 0.12
    with pytest.raises(SchemaError, match="override"):
        cube(draw_rate=rates, draw_override=np.zeros((P, 11), bool)).validate()
    flags = np.zeros((P, 11), bool)
    flags[0, 1] = True
    with pytest.raises(SchemaError, match="0.05, 0.10"):
        cube(draw_rate=rates * 0 + 0.04, draw_override=flags).validate()
    rates_ok = rates.copy()
    cube(draw_rate=rates_ok, draw_override=flags).validate()                 # the 12% year is a flagged override
    with pytest.raises(SchemaError, match="attached together"):
        cube(draw_rate=rates_ok).validate()
    bad_regimes = cube_arrays()["regimes"].copy()
    bad_regimes[0, 0, 1] = 4                                                 # ExitWindow has codes 0..3
    with pytest.raises(SchemaError, match="ExitWindow"):
        cube(regimes=bad_regimes).validate()
    with pytest.raises(SchemaError, match="axis"):
        cube(brent=np.full((P, M + 1), 70.0, dtype=np.float32)).validate()   # M is bound by meta.months
    with pytest.raises(SchemaError, match="size 11"):                        # Y = 11 fiscal years (§3.17)
        cube(draw_rate=np.full((P, 5), 0.058, dtype=np.float32), draw_override=np.zeros((P, 5), bool)).validate()


def group_rates(cube_checksum: str) -> GroupRates:
    meta = GroupRatesMeta(groups=("PE", "SECONDARIES"), age_buckets=("young", "mature"),
                          policy_ref=PolicyRef.model_validate_json('{"kind": "native", "name": "HOLD", "params_hash": "h"}'),
                          world_id="M1", cube_checksum=cube_checksum, quarters=2)
    q4 = np.full((P, 2, 2, 2), 0.05, dtype=np.float32)
    q2 = np.zeros((P, 2), dtype=np.float32)
    share = np.full((P, 2, 2, 2), 0.5, dtype=np.float32)
    return GroupRates(meta=meta, delta=q4, qcall=q4, ret_simple=q4, bid=np.full((P, 2, 2, 2), 0.9, np.float32),
                      income=q4, u_per_nav=q4, nav_share=share, call_stress_12m=q4, lo_ret=q2, hf_ret=q2,
                      hf_phi=np.full((P, 2, 4), 0.5, np.float32), vm_per_beta=q2, cash_rate=q2, fac_rate=q2,
                      ra_debt_rate=q2, ra_amort=q2, ra_direct_share=q2, tail_prem_rate=q2, tail_value=q2,
                      opp_pnl_rate=q2, delta_im_rate=q2, draw_rate_q=q2, stress_class=np.zeros((P, 2), np.int8),
                      obs=np.zeros((P, 2, 3), np.float32))


def test_group_rates_attach_to_their_cube() -> None:
    c = cube()
    gr = group_rates(c.meta.checksum)
    gr.validate()
    cube(group_rates=gr).validate()
    with pytest.raises(SchemaError, match="another cube"):
        cube(group_rates=group_rates("sha256:" + "f" * 64)).validate()
    bad_share = gr.nav_share.copy()
    bad_share[..., 0] = 0.7
    with pytest.raises(SchemaError, match="sum to 1"):
        GroupRates(**{**{f: getattr(gr, f) for f in gr.__dataclass_fields__}, "nav_share": bad_share}).validate()


def node_coefficients(n: int) -> NodeCoefficients:
    nc3 = np.zeros((n, 2, 2))
    n1 = np.zeros(n)
    kw = {f: nc3 for f in ("delta", "qcall", "ret_simple", "bid", "income", "u_per_nav", "nav_share",
                           "call_stress_12m")}
    kw.update({f: n1 for f in ("lo_ret", "hf_ret", "vm_per_beta", "cash_rate", "fac_rate", "draw_rate_q", "tau_lo",
                               "h_im", "ra_debt_rate", "ra_amort", "ra_direct_share", "tail_prem_rate", "tail_value",
                               "opp_pnl_rate", "delta_im_rate", "opex_rate")})
    return NodeCoefficients(**kw, hf_phi=np.zeros((n, 4)), fac_avail=np.ones((n, 1)), amber_depth=np.zeros((n, 2)))


def tree(p_children: tuple[float, float] = (0.4, 0.6)) -> Tree:
    spec = TreeSpec(worlds=("M1", "M6"))
    p = np.array([1.0, *p_children])
    return Tree(spec=spec, tree_hash="t", pooled_worlds=("M1", "M6"), parent=np.array([-1, 0, 0], dtype=np.int32),
                t_end=np.array([0, 1, 1], dtype=np.int16), period_q=np.array([0, 1, 1], dtype=np.int8),
                stage=np.array([0, 1, 1], dtype=np.int8), p=p,
                p_world=np.array([[1.0, 1.0], [0.5, 0.3], [0.5, 0.7]]), is_leaf=np.array([False, True, True]),
                leaf_world=np.array([-1, 0, 1], dtype=np.int8), lr_weight=np.ones(3),
                member_ptr=np.array([0, 2, 3, 4], dtype=np.int32), member_idx=np.array([0, 1, 0, 1], dtype=np.int32),
                coef=node_coefficients(3), obs_centroid=np.zeros((3, 2)), regime_class=np.zeros(3, dtype=np.int8))


def test_tree_probability_invariants() -> None:
    tree().validate()
    with pytest.raises(SchemaError, match="children"):
        tree((0.4, 0.5)).validate()
    assert TreeSpec(worlds=("M1", "M6")).k1 == 24


def test_world_spec_classes() -> None:
    def spec(world_id: str, family: str, t6_class: str, bootstrap: dict | None = None) -> WorldSpec:
        return WorldSpec.model_validate_json(json.dumps({
            "world_id": world_id, "family": family, "provider": "jpm", "cma_asof": "2026-06-30", "cma": {},
            "regime": None, "factors": None, "oil": {"kappa": {}, "vol": {}, "rho_eq": {}, "gw_jump": {}},
            "vol": {"move": {}, "ovx": {}}, "bootstrap": bootstrap, "t6_class": t6_class, "content_hash": "h"}))

    assert spec("M6", "E", "M6").t6_class == "M6"
    boot = {"panel_start": "1990-01-01", "panel_end": "2015-12-31", "method": "stationary_block",
            "observed_factors": ["us_eq"]}
    assert spec("B1", "B1", "M1_M5", boot).family == "B1"
    for args, msg in ((("M2", "E", "M6"), "M1_M5"), (("B1", "E", "M1_M5", boot), "family"),
                      (("B2", "B2", "M1_M5"), "BootstrapParams"), (("MS:fat_tails", "E", "M1_M5"), "misspecification")):
        with pytest.raises(ValidationError, match=msg):
            spec(*args)
    assert validate_world_id("MS:fat_tails") == "MS:fat_tails"
    with pytest.raises(SchemaError):
        validate_world_id("M9")


def test_state_panel_has_twelve_rows() -> None:
    row = {"index": 1, "light": "green", "metric_id": "state.f_t@v1", "status": "INFO", "policy_link": "Q8"}
    assert len(StatePanel.model_validate_json(json.dumps({"rows": [row] * 12})).rows) == 12
    with pytest.raises(ValidationError, match="12 rows"):
        StatePanel.model_validate_json(json.dumps({"rows": [row] * 11}))
    staged = StatePanel.model_validate_json(json.dumps({"rows": [dict(row, status=2)] * 12}))
    assert int(staged.rows[0].status) == 2                                   # CFPStage.RED
