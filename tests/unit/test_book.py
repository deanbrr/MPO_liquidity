"""Book and marks contracts (BUILD_SPEC v1.1 §3.3, §3.5, §1.12). Owner WP-01. SYNTHETIC values only."""

from __future__ import annotations

import copy
import json
from typing import Any

import numpy as np
import pytest
from pydantic import ValidationError

from adic_tpa.contracts.book import UNIT_KIND_ENGINE, UNIT_KIND_TERMS, BookSnapshot, Holding
from adic_tpa.contracts.errors import DataClassMixError
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.marks import ForecastRecord, Mark, Quote

H64 = "sha256:" + "0" * 64

FUND_TERMS = {"kind": "fund", "strategy_class": "buyout_mid", "age_years": 6.0, "effective_age_years": 6.5,
              "fee_rate_a": 0.015, "carry": 0.2, "hurdle_a": 0.08, "lpa_term_years": 10.0, "extensions_used": 0,
              "subscription_line_bn": 0.0, "gp_navloan_bn": 0.0, "recallable_bn": 0.0}
YOUNG = dict(FUND_TERMS, age_years=2.0, effective_age_years=2.0)
TREASURY_TERMS = {"kind": "treasury", "sleeve": "CASH", "haircut": 0.0, "hqla_level": "L1", "cf_controlled": True,
                  "duration_years": 0.0}


def holding(hid: str, group: str, unit_kind: str, nav: float, terms: dict | None, **kw: Any) -> dict[str, Any]:
    base = {"holding_id": hid, "group": group, "strategy": "x", "unit_kind": unit_kind, "region": "US",
            "nav_reported_bn": nav, "nav_reference_date": "2026-09-30", "terms": terms, "is_synthetic": True,
            "data_class": "SYNTHETIC", "source": "synth/R0"}
    base.update(kw)
    return base


HOLDINGS = [
    holding("SYN-PE-0002", "PE", "fund", 2.0, FUND_TERMS, commitment_bn=3.0, unfunded_bn=0.5, gp_id="SYN-GP-0001"),
    holding("SYN-PE-0001", "PE", "fund", 1.0, YOUNG, commitment_bn=2.0, unfunded_bn=1.0, gp_id="SYN-GP-0001"),
    holding("SYN-CF-0001", "CF", "treasury", 5.0, TREASURY_TERMS),
    holding("SYN-CO-0001", "COINVEST", "company", 1.5, None, vintage=2020, gp_id="SYN-GP-0002"),
    holding("SYN-OVL-0001", "OVERLAY", "overlay_bucket", 0.5, None),
]


def book(**changes: Any) -> BookSnapshot:
    data = {
        "snapshot_id": "R0", "asof": "2026-09-30", "known_at": "2026-10-18T00:00:00Z", "taxonomy_version": "v2",
        "allocation": "v2", "census_id": "v1.1", "holdings": copy.deepcopy(HOLDINGS),
        "overlap": {"sponsors": [{"sponsor_id": "SYN-GP-0001", "tier": "core"},
                                 {"sponsor_id": "SYN-GP-0002", "tier": "elite"}], "companies": [], "edges": []},
        "facilities": [{"facility_id": "SYN-FAC-01", "kind": "revolver", "status": "requested", "committed": True,
                        "size_bn": 15.0, "spread_drawn_a": 0.0085, "fee_undrawn_a": 0.0015, "fee_upfront": 0.001,
                        "maturity": "2031-09-30", "credit_stress": 0.5, "consent_scenario": "R1"}],
        "overlay": {"trades": [], "csas": [], "services": [], "policy": {}},
        "owner": {"convention": "opening_fy_reported_nav", "history": [[2025, 0.06], [2026, 0.058]], "d_prev": 0.058},
        "nav_total_reported_bn": 10.0, "data_class": "SYNTHETIC", "content_hash": H64,
    }
    data.update(changes)
    return BookSnapshot.model_validate_json(json.dumps(data))


def test_snapshot_and_unit_index() -> None:
    b = book()
    idx = b.unit_index()
    idx.validate()
    assert idx.unit_ids == ("SYN-PE-0001", "SYN-PE-0002", "SYN-CO-0001", "SYN-OVL-0001", "SYN-CF-0001")  # taxonomy order
    assert idx.group_of.tolist() == [0, 0, 3, 6, 8]
    assert idx.engine_of == ("priv.fund", "priv.fund", "priv.company", "overlay", "treasury")
    assert idx.age_bucket.tolist() == [0, 1, 1, -1, -1]          # young fund, mature fund, vintage 2020, non-private
    assert idx.red_tier.tolist() == [True, True, True, False, False]
    groups = b.by_group()
    assert list(groups)[0] == "PE" and len(groups["PE"]) == 2 and groups["REALASSETS"] == ()
    conc = b.overlap.gp_concentration(b)
    assert conc["SYN-GP-0001"] == pytest.approx(4.5 / 6.0) and conc["SYN-GP-0002"] == pytest.approx(1.5 / 6.0)
    assert b.hash_payload().keys() == set(BookSnapshot.model_fields) - {"content_hash"}
    assert content_hash(b.hash_payload()).startswith("sha256:")


def test_snapshot_validators() -> None:
    with pytest.raises(ValidationError, match="nav_total_reported_bn"):
        book(nav_total_reported_bn=11.0)
    with pytest.raises(ValidationError, match="nav_total_reported_bn"):
        book(nav_total_reported_bn=10.0 + 1e-6)                            # 1e-9 relative tolerance, not 1e-3
    assert book(nav_total_reported_bn=10.0 + 5e-9).nav_total_reported_bn > 10.0
    with pytest.raises(ValidationError, match="not in taxonomy v1"):
        book(taxonomy_version="v1", holdings=[holding("SYN-RA-0001", "REALASSETS", "ra_asset", 10.0, None)])
    with pytest.raises(ValidationError, match="duplicate holding ids"):
        book(holdings=[HOLDINGS[0], HOLDINGS[0]], nav_total_reported_bn=4.0)


def test_mixed_data_classes_raise_data_class_mix_error() -> None:
    """§1.12 rule 2 / §1.10: SYNTHETIC and REAL together raise DataClassMixError (code DATA_CLASS_MIX)."""
    with pytest.raises(DataClassMixError) as exc:
        book(data_class="REAL")                                             # synthetic rows in a REAL snapshot
    assert exc.value.code == "DATA_CLASS_MIX" and exc.value.context["data_classes"] == ["REAL", "SYNTHETIC"]
    real_row = dict(HOLDINGS[2], holding_id="ADIC-TRS-1", is_synthetic=False, data_class="REAL")
    with pytest.raises(DataClassMixError):
        book(holdings=[*copy.deepcopy(HOLDINGS[:2]), real_row], nav_total_reported_bn=8.0)
    trade = {"trade_id": "ADIC-TR-1", "book": "TAIL", "template": "put", "underlying": "SPX", "notional_bn": 1.0,
             "premium_bn": 0.01, "venue": "listed", "is_synthetic": False, "data_class": "REAL"}
    with pytest.raises(DataClassMixError):
        book(overlay={"trades": [trade], "csas": [], "services": [], "policy": {}})


def test_synthetic_holding_ids_carry_their_group_code() -> None:
    """§1.8 SYN-<GROUPCODE>-<4 digits>: review R14."""
    wrong_group = holding("SYN-RA-0009", "CF", "treasury", 1.0, TREASURY_TERMS)
    with pytest.raises(ValidationError, match="group's code"):
        book(holdings=[*copy.deepcopy(HOLDINGS), wrong_group], nav_total_reported_bn=11.0)
    unknown_code = holding("SYN-XYZ-0001", "CF", "treasury", 1.0, TREASURY_TERMS)
    with pytest.raises(ValidationError, match="group's code"):
        book(holdings=[*copy.deepcopy(HOLDINGS), unknown_code], nav_total_reported_bn=11.0)
    assert len(book().holdings) == 5                                         # SYN-CO-0001 sits in COINVEST (CO)


def test_age_bucket_boundary_is_young_max_age() -> None:
    """A unit exactly at young_max_age_years (4.0) is mature; just below it is young."""
    at_edge = dict(FUND_TERMS, age_years=4.0, effective_age_years=4.0)
    below = dict(FUND_TERMS, age_years=3.99, effective_age_years=3.99)
    holdings = [holding("SYN-PE-0001", "PE", "fund", 1.0, below, commitment_bn=1.0),
                holding("SYN-PE-0002", "PE", "fund", 1.0, at_edge, commitment_bn=1.0)]
    idx = book(holdings=holdings, nav_total_reported_bn=2.0).unit_index()
    assert idx.age_bucket.tolist() == [0, 1]


def test_unit_kind_tables() -> None:
    assert dict(UNIT_KIND_ENGINE) == {
        "fund": "priv.fund", "company": "priv.company", "claim": "priv.claims", "loan_cohort": "priv.credit",
        "hf_lot": "pub.hf", "longonly": "pub.longonly", "treasury": "treasury", "ra_asset": "priv.realassets",
        "ra_open_end": "priv.realassets", "overlay_bucket": "overlay"}
    assert set(UNIT_KIND_TERMS) == set(UNIT_KIND_ENGINE) and UNIT_KIND_TERMS["ra_open_end"] == "realasset"
    assert UNIT_KIND_TERMS["overlay_bucket"] is None


def test_holding_rules() -> None:
    ok = Holding.model_validate_json(json.dumps(HOLDINGS[0]))
    assert ok.terms is not None and ok.terms.kind == "fund" and ok.age_years(__import__("datetime").date(2026, 9, 30)) == 6.0
    bad_cases = [
        (dict(HOLDINGS[0], unfunded_bn=4.0), "must not exceed"),
        (dict(HOLDINGS[0], data_class="REAL"), "disagrees"),
        (dict(HOLDINGS[0], holding_id="ADIC-1"), "lacks the SYN- prefix"),
        (dict(HOLDINGS[0], terms=TREASURY_TERMS), "does not match unit_kind"),
        (dict(HOLDINGS[4], terms=FUND_TERMS), "carries no terms"),
        (dict(HOLDINGS[3], unfunded_bn=0.1), "needs a commitment"),
        (dict(HOLDINGS[0], nav_reported_bn=-1.0), ">= 0"),
    ]
    for data, msg in bad_cases:
        with pytest.raises(ValidationError, match=msg):
            Holding.model_validate_json(json.dumps(data))
    real = dict(HOLDINGS[2], holding_id="ADIC-TRS-1", is_synthetic=False, data_class="REAL")
    assert Holding.model_validate_json(json.dumps(real)).data_class.value == "REAL"


def test_real_asset_terms_use_coinvestment_access() -> None:
    ra = {"kind": "realasset", "sector": "INFRASTRUCTURE", "access": "COINVESTMENT", "noi_bn": 0.1, "cap_rate": 0.06,
          "inflation_passthrough": 0.5, "oil_beta": 0.0, "capex_reserve_rate_a": 0.01, "development": None,
          "debt": {"balance_bn": 0.4, "rate_type": "FLOATING", "spread_a": 0.02, "hedge_ratio": 0.5,
                   "maturity": "2029-06-30", "ltv_max": 0.65, "dscr_covenant": 1.2, "amort_q": 0.0},
          "open_end": None, "appraisal_lambda": 0.7, "report_lag_q": 1}
    h = Holding.model_validate_json(json.dumps(holding("SYN-RA-0001", "REALASSETS", "ra_asset", 1.0, ra)))
    assert h.terms.debt.recourse is False  # type: ignore[union-attr]
    with pytest.raises(ValidationError):
        Holding.model_validate_json(json.dumps(holding("SYN-RA-0001", "REALASSETS", "ra_asset", 1.0,
                                                       dict(ra, access="COINVEST"))))


MARK = {"holding_id": "SYN-PE-0042", "mark_type": "FORECAST", "as_of": "2026-09-30",
        "recorded_at": "2026-10-05T00:00:00Z", "basis": "IRR", "gross_net": "net", "value": 0.16, "author": "pe-desk",
        "revision_id": 3, "case_down": 0.08, "case_base": 0.16, "case_up": 0.22, "is_synthetic": True,
        "data_class": "SYNTHETIC"}


def test_marks_and_cases() -> None:
    m = Mark.model_validate_json(json.dumps(MARK))
    assert m.case_map.down == "p10" and m.since_inception
    with pytest.raises(ValidationError, match="ordered"):
        Mark.model_validate_json(json.dumps(dict(MARK, case_down=0.3)))
    cap = dict(MARK, basis="EXIT_CAP_RATE", value=0.06, case_down=0.07, case_base=0.06, case_up=0.05)
    assert Mark.model_validate_json(json.dumps(cap)).case_up == 0.05      # cap rates run the other way


def test_forecast_quantiles_and_quotes() -> None:
    rec = {"record_id": "f1", "group": "PE", "holding_id": "SYN-PE-0042", "author": "pe-desk", "as_of": "2026-09-30",
           "recorded_at": "2026-10-05T00:00:00Z", "horizon_q": 8, "target": "irr_si",
           "quantiles": {"p90": 0.22, "p10": 0.08, "p50": 0.16},
           "snapshot": {"u": 0.18, "a": 0.12, "nav_bn": 0.5, "regime": 0, "exit": 1},
           "is_synthetic": True, "data_class": "SYNTHETIC"}
    assert ForecastRecord.model_validate_json(json.dumps(rec)).quantiles["p50"] == 0.16
    with pytest.raises(ValidationError, match="increase strictly"):
        ForecastRecord.model_validate_json(json.dumps(dict(rec, quantiles={"p10": 0.2, "p50": 0.16})))
    quote = {"quote_id": "q1", "holding_id": "SYN-PE-0042", "as_of": "2026-09-30", "kind": "secondary_bid",
             "bid_pct_ref_nav": 0.88, "ref_nav_date": "2026-06-30", "source": "in_house", "desk": "SECONDARIES",
             "counterparty_class": "internal", "conflict_flag": True, "is_synthetic": True, "data_class": "SYNTHETIC"}
    assert Quote.model_validate_json(json.dumps(quote)).conflict_flag
    with pytest.raises(ValidationError, match="conflict_flag"):
        Quote.model_validate_json(json.dumps(dict(quote, conflict_flag=False)))


def test_unit_index_arrays_are_typed() -> None:
    idx = book().unit_index()
    assert idx.group_of.dtype == np.int32 and idx.age_bucket.dtype == np.int8 and idx.red_tier.dtype == np.bool_
