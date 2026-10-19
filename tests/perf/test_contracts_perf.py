"""contracts performance (BUILD_SPEC v1.1 §4.1): content_hash(BookSnapshot) for 500 holdings + 1,500 loan cohorts
< 0.5 s on the reference laptop. Nightly (perf). Owner WP-01. SYNTHETIC values only."""

from __future__ import annotations

import json
import time

import pytest

from adic_tpa.contracts.book import BookSnapshot
from adic_tpa.contracts.hashing import content_hash

pytestmark = pytest.mark.perf

FUND = {"kind": "fund", "strategy_class": "buyout_mid", "age_years": 6.0, "effective_age_years": 6.5,
        "fee_rate_a": 0.015, "carry": 0.2, "hurdle_a": 0.08, "lpa_term_years": 10.0, "extensions_used": 0,
        "subscription_line_bn": 0.0, "gp_navloan_bn": 0.0, "recallable_bn": 0.0}
LOAN = {"kind": "loan_cohort", "segment": "DL", "vehicle_id": "v1", "wrapper": "SMA", "n_loans": 40, "par_bn": 0.01,
        "spread_a": 0.055, "floor_a": 0.01, "oid": 0.02, "wam_years": 4.0, "undrawn_bn": 0.0, "sponsored_share": 0.9,
        "software_share": 0.2, "state_shares": {"0": 0.9, "1": 0.1}, "collateral_type": "first_lien"}


def _holding(i: int, group: str, kind: str, terms: dict) -> dict:
    code = {"PE": "PE", "PRIVCREDIT": "PC"}[group]
    return {"holding_id": f"SYN-{code}-{i:04d}", "group": group, "strategy": "x", "unit_kind": kind, "region": "US",
            "nav_reported_bn": 0.01, "nav_reference_date": "2026-09-30", "terms": terms, "commitment_bn": 0.02,
            "unfunded_bn": 0.005, "is_synthetic": True, "data_class": "SYNTHETIC", "source": "synth/R0"}


def test_content_hash_of_a_large_book_is_fast() -> None:
    holdings = [_holding(i, "PE", "fund", FUND) for i in range(500)]
    holdings += [_holding(i, "PRIVCREDIT", "loan_cohort", LOAN) for i in range(1500)]
    book = BookSnapshot.model_validate_json(json.dumps({
        "snapshot_id": "R0", "asof": "2026-09-30", "known_at": "2026-10-18T00:00:00Z", "taxonomy_version": "v2",
        "allocation": "v2", "census_id": "v1.1", "holdings": holdings,
        "overlap": {"sponsors": [], "companies": [], "edges": []}, "facilities": [],
        "overlay": {"trades": [], "csas": [], "services": [], "policy": {}},
        "owner": {"convention": "opening_fy_reported_nav", "history": [], "d_prev": 0.058},
        "nav_total_reported_bn": 20.0, "data_class": "SYNTHETIC", "content_hash": "sha256:" + "0" * 64}))
    start = time.perf_counter()
    h = content_hash(book.hash_payload())
    elapsed = time.perf_counter() - start
    assert h.startswith("sha256:")
    assert elapsed < 0.5, f"content_hash took {elapsed:.3f} s"
