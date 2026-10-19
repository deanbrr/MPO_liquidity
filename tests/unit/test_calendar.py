"""contracts.calendar (BUILD_SPEC v1.1 §1.3, §4.1; S-ADR-26). Owner WP-01."""

from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from adic_tpa.contracts.calendar import Calendar
from adic_tpa.contracts.errors import SchemaError

CAL = Calendar()


def test_defaults() -> None:
    assert CAL.asof_instant == date(2026, 9, 30) and CAL.n_quarters == 40 and CAL.n_months == 120


def test_quarter_and_month_instants() -> None:
    assert CAL.quarter_end(0) == date(2026, 9, 30)
    assert CAL.quarter_end(1) == date(2026, 12, 31)          # end of quarter period 0 (Q4-2026)
    assert CAL.quarter_end(2) == date(2027, 3, 31)
    assert CAL.quarter_end(40) == date(2036, 9, 30)
    assert CAL.month_end(0) == date(2026, 9, 30)
    assert CAL.month_end(1) == date(2026, 10, 31)            # month period 0 = October 2026
    assert CAL.month_end(5) == date(2027, 2, 28)
    assert CAL.quarter_of_month(0) == 0 and CAL.quarter_of_month(5) == 1


def test_fiscal_years() -> None:
    assert CAL.fiscal_year(0) == 2026
    assert [CAL.fiscal_year(t) for t in range(1, 5)] == [2027] * 4
    assert CAL.fiscal_year(5) == 2028 and CAL.fiscal_year(39) == 2036
    years = CAL.fiscal_years()
    assert years[0] == 2026 and years[-1] == 2036 and len(years) == 11   # Y = 11 draw-rate columns
    assert CAL.fy_index(2026) == 0 and CAL.fy_index(2036) == 10


def test_instalments_and_fy_open() -> None:
    assert CAL.instalment_month(0) == 2 and CAL.instalment_month(5) == 17
    assert CAL.fy_open_quarter(2026) == 0 and CAL.fy_open_quarter(2027) == 1 and CAL.fy_open_quarter(2028) == 5
    with pytest.raises(SchemaError):
        CAL.fy_open_quarter(2025)
    with pytest.raises(SchemaError):
        CAL.fy_index(2040)


def test_validation() -> None:
    with pytest.raises(SchemaError):
        CAL.quarter_end(-1)
    with pytest.raises(ValidationError):
        Calendar(asof_instant=date(2026, 9, 29))
    with pytest.raises(ValidationError):
        Calendar(asof_instant=date(2026, 8, 31))             # not a quarter end
    other = Calendar(asof_instant=date(2025, 12, 31), n_quarters=8)
    assert other.fiscal_year(0) == 2026 and other.fy_open_quarter(2026) == 0 and other.fy_open_quarter(2027) == 4
