"""contracts.ids (BUILD_SPEC v1.1 §1.8, §3.1, §1.12): formats validated on construction. Owner WP-01."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from adic_tpa.contracts.enums import ContractModel, DataClass
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.ids import (
    ArtifactRef, CampaignId, CompanyId, ContractId, CsaId, DecisionId, FacilityId, GroupId, HoldingId, MetricId, RunId,
    SponsorId, TradeId, UnitId, check_synthetic_consistency, is_content_hash, make_run_id, synthetic_holding_id,
)

CASES = [
    (GroupId, ["PE", "REALASSETS", "NEW_GROUP_9"], ["pe", "", "9PE", "P-E"]),
    (HoldingId, ["SYN-PE-0042", "SYN-RA-0007", "SYN-OVL-0001", "ADIC-HF-123"],
     ["SYN-PE-42", "SYN-GP-0031", "SYN-CMP-0001", "has space", "PE", "ADIC123"]),   # real ids contain '-'
    (CompanyId, ["SYN-CMP-000417", "LEI529900T8BM49AURSDO55"], ["SYN-CMP-417", "SYN-GP-000417"]),
    (SponsorId, ["SYN-GP-0031"], ["SYN-GP-31", "SYN-CMP-0031"]),
    (TradeId, ["SYN-TR-00001"], ["SYN-TR-1"]),
    (CsaId, ["SYN-CSA-01"], ["SYN-CSA-1"]),
    (FacilityId, ["SYN-FAC-01"], ["SYN-FAC-001"]),
    (RunId, ["run-20261018T091500Z-3f2a9c1d"], ["run-20261018-3f2a9c1d", "run-20261018T091500Z-3F2A9C1D"]),
    (MetricId, ["tier1.t6.cp_upper@v1", "ladder.lr4@v12"], ["tier1@v1", "Tier1.t6@v1", "tier1.t6"]),
    (DecisionId, ["dec-Q1-2026Q4-1"], ["dec-Q1-2026Q5-1"]),
    (ContractId, ["ctr-2026Q4-v1"], ["ctr-2026Q4-1"]),
    (CampaignId, ["cmp-2026Q4-3"], ["cmp-2026-3"]),
    (ArtifactRef, ["run-20261018T091500Z-3f2a9c1d:tier1_board:/rows/T6/M6/cp_upper",
                   "run-20261018T091500Z-3f2a9c1d:pack:"], ["tier1_board:/rows", "run-20261018T091500Z-3f2a9c1d:x:rows"]),
    (UnitId, ["SYN-PC-0012:DL:2024", "SYN-PE-0042"], ["", "a b"]),
]


@pytest.mark.parametrize(("cls", "good", "bad"), CASES, ids=[c[0].__name__ for c in CASES])
def test_formats(cls: type, good: list[str], bad: list[str]) -> None:
    for value in good:
        obj = cls(value)
        assert obj == value and isinstance(obj, str) and isinstance(obj, cls) and cls.is_valid(value)
    for value in bad:
        assert not cls.is_valid(value)
        with pytest.raises(SchemaError):
            cls(value)


def test_ids_validate_inside_models_and_serialize_as_strings() -> None:
    class Row(ContractModel):
        holding_id: HoldingId
        group: GroupId

    row = Row(holding_id="SYN-PE-0042", group="PE")
    assert type(row.holding_id) is HoldingId and row.model_dump() == {"holding_id": "SYN-PE-0042", "group": "PE"}
    assert row.model_dump_json() == '{"holding_id":"SYN-PE-0042","group":"PE"}'
    with pytest.raises(ValidationError):
        Row(holding_id="SYN-PE-42", group="PE")
    assert "pattern" in Row.model_json_schema()["properties"]["holding_id"]


def test_artifact_ref_parts() -> None:
    ref = ArtifactRef.make("run-20261018T091500Z-3f2a9c1d", "tier1_board", "/rows/T6")
    assert ref.run_id == "run-20261018T091500Z-3f2a9c1d" and ref.artifact == "tier1_board" and ref.pointer == "/rows/T6"


def test_holding_and_group_ids_are_disjoint() -> None:
    for value in ("PE", "REALASSETS", "SYN-PE-0042", "ADIC-HF-123"):
        assert HoldingId.is_valid(value) != GroupId.is_valid(value), value


def test_holding_group_code_and_helpers() -> None:
    assert HoldingId("SYN-SEC-0001").group_code == "SEC" and HoldingId("REAL-1").group_code is None
    assert HoldingId("SYN-SEC-0001").is_synthetic and not HoldingId("REAL-1").is_synthetic
    assert synthetic_holding_id("RA", 7) == "SYN-RA-0007"
    rid = make_run_id(datetime(2026, 10, 18, 13, 15, tzinfo=timezone.utc), "sha256:" + "3f2a9c1d" + "0" * 56)
    assert rid == "run-20261018T131500Z-3f2a9c1d"
    assert is_content_hash("sha256:" + "a" * 64) and not is_content_hash("sha256:" + "A" * 64)


def test_synthetic_consistency() -> None:
    check_synthetic_consistency(True, DataClass.SYNTHETIC, "SYN-PE-0001", None)
    check_synthetic_consistency(False, DataClass.REAL, "ADIC-1")
    with pytest.raises(SchemaError):
        check_synthetic_consistency(True, DataClass.REAL)
    with pytest.raises(SchemaError):
        check_synthetic_consistency(True, DataClass.SYNTHETIC, "ADIC-1")
    with pytest.raises(SchemaError):
        check_synthetic_consistency(False, DataClass.REAL, "SYN-PE-0001")
