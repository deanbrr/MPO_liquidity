"""Taxonomy as configuration (BUILD_SPEC v1.1 §3.2; S-ADR-01, -05, -22, -32). Owner WP-01."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from adic_tpa.contracts.config import clear_config_audit, loaded_config_files
from adic_tpa.contracts.enums import Lens, RecourseTier
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import content_hash, file_hash
from adic_tpa.contracts.taxonomy import GroupRegistry, TaxonomyConfig, taxonomy_path

V2 = GroupRegistry.for_version("v2")
V1 = GroupRegistry.for_version("v1")


def test_v2_is_the_default_with_eight_investment_groups() -> None:
    assert GroupRegistry.load().ids() == V2.ids()
    assert V2.version == "v2" and V2.n_groups == 8 and V2.n_seats == 13        # seats = n_groups + 5
    assert V2.ids() == ("PE", "SECONDARIES", "CAPSOL", "COINVEST", "PUBLIC", "PRIVCREDIT", "OVERLAY", "REALASSETS",
                        "CF", "TPA")
    assert V2.codes() == ("PE", "SEC", "CS", "CO", "PM", "PC", "OVL", "RA", "CF", "TPA")


def test_normative_v2_columns() -> None:
    assert V2.private() == ("PE", "SECONDARIES", "CAPSOL", "COINVEST", "PRIVCREDIT", "REALASSETS")
    assert V2.red_tier() == ("PE", "SECONDARIES", "COINVEST", "REALASSETS")
    assert V2.amber_tier() == ("CAPSOL", "PRIVCREDIT", "REALASSETS")
    tiers = {g: V2.spec(g).recourse_tier for g in V2.ids()}
    assert tiers["PUBLIC"] is RecourseTier.TP and tiers["CAPSOL"] is RecourseTier.TPFA and tiers["CF"] is RecourseTier.T
    assert tiers["OVERLAY"] is None and tiers["TPA"] is None and tiers["REALASSETS"] is RecourseTier.ALL
    splits = {g: V2.spec(g).commitment_split for g in V2.ids()}
    assert splits["PE"] == 0.50 and splits["REALASSETS"] == 0.10 and abs(sum(splits.values()) - 1) < 1e-12
    eta = {g: V2.spec(g).pacing_eta_sign for g in V2.ids()}
    assert (eta["PE"], eta["SECONDARIES"], eta["CAPSOL"], eta["COINVEST"], eta["REALASSETS"]) == (1, -1, -1, 1, 1)
    assert {g for g in V2.ids() if V2.spec(g).contingent_budget} == {"SECONDARIES", "CAPSOL", "PRIVCREDIT"}
    assert {g for g in V2.ids() if V2.spec(g).fund_distribution_stress} == {"PE", "SECONDARIES", "COINVEST"}
    assert V2.seat_groups() == V2.investment()
    assert V2.spec("REALASSETS").engines == ("realassets", "fund") and V2.spec("PUBLIC").engines == ("hf", "longonly")
    assert Lens.PACE in V2.spec("PE").lenses and Lens.PACE not in V2.spec("PUBLIC").lenses


def test_v1_reproduces_the_research_taxonomy() -> None:
    assert "REALASSETS" not in V1 and V1.n_groups == 7 and V1.n_seats == 12
    assert V1.spec("PE").commitment_split == 0.60
    assert {g: V1.spec(g) for g in V1.ids() if g != "PE"} == {g: V2.spec(g) for g in V1.ids() if g != "PE"}


def test_couplings() -> None:
    kinds = [(c.kind, c.source, c.target) for c in V2.couplings]
    assert ("offered_flow", "PE", "COINVEST") in kinds and ("recap_netting", "COINVEST", "PRIVCREDIT") in kinds
    offered = next(c for c in V2.couplings if c.kind == "offered_flow")
    assert offered.params["theta"] == 0.33 and offered.params["time_unit"] == "quarter"
    assert len(offered.params["d_per_year"]) == 5 and abs(sum(offered.params["d_per_year"]) - 1.0) < 1e-12
    assert V1.couplings == V2.couplings


def test_registry_lookups() -> None:
    assert V2.index("PE") == 0 and V2.index("TPA") == 9 and V2.by_code("RA").group_id == "REALASSETS"
    assert "PE" in V2 and "XX" not in V2 and list(V2) == list(V2.ids()) and len(V2) == 10
    assert V2.ids("public") == ("PUBLIC",) and V2.strategies("REALASSETS")[0] == "real_estate"
    for bad in (lambda: V2.spec("XX"), lambda: V2.index("XX"), lambda: V2.by_code("ZZ")):
        with pytest.raises(SchemaError):
            bad()
    with pytest.raises(AttributeError):
        V2.foo = 1  # type: ignore[attr-defined]


def test_hash_is_stable_and_version_specific() -> None:
    assert V2.hash == GroupRegistry.load(taxonomy_path("v2")).hash != V1.hash
    assert V2.hash.startswith("sha256:")


def test_config_view() -> None:
    cfg = V2.config
    assert isinstance(cfg, TaxonomyConfig) and cfg.version == "v2"
    assert tuple(g.group_id for g in cfg.groups) == V2.ids() and V2.hash == content_hash(cfg)


def test_cached_taxonomies_stay_in_the_config_audit() -> None:
    """Review R16: a long-lived worker that clears the audit and then reads a cached taxonomy still lists it."""
    expected = str(taxonomy_path("v2").resolve())
    clear_config_audit()
    assert GroupRegistry.for_version("v2") is V2                               # served from the cache
    paths = [rec.path for rec in loaded_config_files()]
    assert paths == [expected]
    GroupRegistry.for_version("v2")
    assert [rec.path for rec in loaded_config_files()] == [expected]           # recorded once, not per call
    assert loaded_config_files()[0].file_hash == file_hash(taxonomy_path("v2"))


def _raw(version: str) -> dict:
    import yaml

    return yaml.safe_load(taxonomy_path(version).read_text(encoding="utf-8"))  # type: ignore[arg-type]


def test_config_validators(tmp_path: Path) -> None:
    raw = _raw("v2")
    raw["groups"][0]["commitment_split"] = 0.6                       # splits no longer sum to 1
    with pytest.raises(ValidationError, match="sum to 1"):
        TaxonomyConfig.model_validate_json(json.dumps(raw))
    raw = _raw("v2")
    raw["groups"][1]["code"] = "PE"
    with pytest.raises(ValidationError, match="duplicate group codes"):
        TaxonomyConfig.model_validate_json(json.dumps(raw))
    raw = _raw("v2")
    raw["groups"][0]["recourse_tier"] = "TP"                          # red-tier sales enter at ALL
    with pytest.raises(ValidationError, match="ALL"):
        TaxonomyConfig.model_validate_json(json.dumps(raw))
    raw = _raw("v2")
    raw["groups"][0]["code"] = "GP"                                   # reserved for sponsor ids
    with pytest.raises(ValidationError, match="reserved"):
        TaxonomyConfig.model_validate_json(json.dumps(raw))


def test_a_new_group_is_pure_configuration(tmp_path: Path) -> None:
    """Adding a ninth group needs no code change (S-ADR-01)."""
    import yaml

    raw = _raw("v2")
    new = dict(raw["groups"][1], group_id="INFRADEBT", code="ID", display_name="Infrastructure debt",
               commitment_split=0.05)
    raw["groups"][0]["commitment_split"] = 0.45
    raw["groups"].insert(8, new)
    path = tmp_path / "groups_v2.yaml"
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    reg = GroupRegistry.load(path)
    assert reg.n_groups == 9 and reg.n_seats == 14 and "INFRADEBT" in reg.red_tier()
