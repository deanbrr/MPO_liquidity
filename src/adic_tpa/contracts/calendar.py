"""Time index and calendar (BUILD_SPEC v1.1 §1.3, §4.1; S-ADR-26).

Instant ``i`` is the end of period ``i − 1`` and the start of period ``i``; instant 0 is the as-of
(2026-09-30, the census date). Quarter period 0 is Q4-2026, month period 0 is October 2026; month period ``m``
lies in quarter period ``m // 3``. Fiscal year = calendar year; the owner instalment of quarter period ``t`` falls
at the end of month period ``3t + 2``.
"""

from __future__ import annotations

import calendar as _cal
from datetime import date

from pydantic import model_validator

from adic_tpa.contracts.enums import ContractModel
from adic_tpa.contracts.errors import SchemaError

__all__ = ["Calendar"]


def _add_months_month_end(start: date, months: int) -> date:
    idx = start.year * 12 + (start.month - 1) + months
    year, month0 = divmod(idx, 12)
    return date(year, month0 + 1, _cal.monthrange(year, month0 + 1)[1])


class Calendar(ContractModel):
    """The simulation calendar: 40 quarters (120 months) from the as-of instant."""

    asof_instant: date = date(2026, 9, 30)
    n_quarters: int = 40

    @model_validator(mode="after")
    def _month_end_asof(self) -> Calendar:
        if self.asof_instant.day != _cal.monthrange(self.asof_instant.year, self.asof_instant.month)[1]:
            raise ValueError(f"asof_instant must be a month end, got {self.asof_instant}")
        if self.asof_instant.month % 3 != 0:
            raise ValueError(f"asof_instant must be a calendar quarter end, got {self.asof_instant}")
        if self.n_quarters < 1:
            raise ValueError("n_quarters must be >= 1")
        return self

    @property
    def n_months(self) -> int:
        return 3 * self.n_quarters

    def quarter_end(self, t: int) -> date:
        """Date of quarter instant ``t`` (t = 0 is the as-of; t = 1 is the end of quarter period 0)."""
        if t < 0:
            raise SchemaError(f"quarter instant must be >= 0, got {t}")
        return _add_months_month_end(self.asof_instant, 3 * t)

    def month_end(self, m: int) -> date:
        """Date of month instant ``m`` (m = 0 is the as-of; m = 1 is the end of October 2026)."""
        if m < 0:
            raise SchemaError(f"month instant must be >= 0, got {m}")
        return _add_months_month_end(self.asof_instant, m)

    def fiscal_year(self, t: int) -> int:
        """Fiscal (= calendar) year of quarter period ``t``: 2026 for t = 0, 2027 for t = 1..4, ..."""
        if t < 0:
            raise SchemaError(f"quarter period must be >= 0, got {t}")
        return self.quarter_end(t + 1).year

    def quarter_of_month(self, m: int) -> int:
        """Quarter period containing month period ``m``."""
        if m < 0:
            raise SchemaError(f"month period must be >= 0, got {m}")
        return m // 3

    def instalment_month(self, t: int) -> int:
        """Month period of quarter period ``t``'s owner instalment: ``3t + 2``."""
        if t < 0:
            raise SchemaError(f"quarter period must be >= 0, got {t}")
        return 3 * t + 2

    def fy_open_quarter(self, fy: int) -> int:
        """Quarter instant at which FY ``fy`` opens (0 for the as-of fiscal year's in-horizon remainder)."""
        first = self.fiscal_year(0)
        if fy < first:
            raise SchemaError(f"FY{fy} precedes the as-of fiscal year FY{first}")
        if fy == first:
            return 0
        t = 0
        while self.fiscal_year(t) < fy:
            t += 1
        return t

    def fiscal_years(self) -> tuple[int, ...]:
        """Fiscal years touched by the horizon (FY2026–FY2036 at the defaults, Y = 11 draw-rate columns)."""
        return tuple(range(self.fiscal_year(0), self.fiscal_year(self.n_quarters - 1) + 1))

    def fy_index(self, fy: int) -> int:
        """Column of FY ``fy`` in [P, Y] draw-rate arrays."""
        years = self.fiscal_years()
        if fy not in years:
            raise SchemaError(f"FY{fy} outside the horizon {years[0]}..{years[-1]}")
        return fy - years[0]

    def instalments_left(self, t: int) -> int:
        """Instalments left in quarter period ``t``'s fiscal year, counting ``t`` itself (4 in Q1, 1 in Q4)."""
        fy = self.fiscal_year(t)
        n = 0
        while self.fiscal_year(t + n) == fy:
            n += 1
        return n
