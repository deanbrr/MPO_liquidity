"""The mFDR table (BUILD_SPEC v1.1 S-ADR-18, §7.7, §4.6; owner WP-04; wired into the lab by WP-38).

Error control across contracts runs as one online sequence of hypothesis tests that spans campaigns, quarters
and processes (Holm within a contract, mFDR across; decaying-memory generalized alpha-investing with W0 = 0.05,
payout 0.05). The registry cannot import ``stats`` (§4.0), so this ledger does not run the investing rule: the
lab applies ``stats.AlphaInvesting`` (Holm within the contract first) and records each online test here. The
ledger keeps the sequence durable and hash-chained and enforces what any alpha-investing record must satisfy:

- the parameters (``w0``, ``payout``, ``decay``) are fixed once for the whole ledger;
- tests form one sequence: each test's ``wealth_before`` is the previous ``wealth_after`` (``w0`` at the start);
- a test rejects exactly when ``p_value <= alpha_level``; p-values and levels are probabilities; wealth is never
  negative.

``p_values()`` returns the sequence in order, so a restarted lab rebuilds the investing state exactly by replay.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import model_validator

from adic_tpa.contracts.config import load_json_payload
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import canonical_json
from adic_tpa.registry.chain import RegistryModel, split_envelope

if TYPE_CHECKING:
    from adic_tpa.registry.store import Registry

__all__ = ["MFDRConfig", "MFDRTest", "MFDRRow", "MFDRState", "MFDRLedger", "CONFIG_KIND", "TEST_KIND"]

CONFIG_KIND = "mfdr_config"
TEST_KIND = "mfdr_test"


def _finite(*values: float) -> bool:
    return all(math.isfinite(v) for v in values)


class MFDRConfig(RegistryModel):
    """Parameters of the across-contract alpha-investing sequence (fixed for the ledger's life)."""

    w0: float
    payout: float
    decay: float

    @model_validator(mode="after")
    def _ranges(self) -> MFDRConfig:
        if not _finite(self.w0, self.payout, self.decay):
            raise ValueError("mFDR parameters must be finite")
        if not 0.0 < self.w0 < 1.0 or not 0.0 <= self.payout <= 1.0 or not 0.0 < self.decay <= 1.0:
            raise ValueError("mFDR parameters need 0 < w0 < 1, 0 <= payout <= 1 and 0 < decay <= 1")
        return self


class MFDRTest(RegistryModel):
    """One online test of the sequence (the body of a chain row of kind ``mfdr_test``)."""

    contract_id: str
    campaign_id: str | None
    hypothesis_id: str
    family_size: int                # hypotheses in the contract's Holm family behind this online test
    p_value: float                  # as tested online (e.g. the family's Holm-adjusted p-value)
    alpha_level: float
    rejected: bool
    wealth_before: float
    wealth_after: float

    @model_validator(mode="after")
    def _consistent(self) -> MFDRTest:
        if not _finite(self.p_value, self.alpha_level, self.wealth_before, self.wealth_after):
            raise ValueError("mFDR test values must be finite")
        if not 0.0 <= self.p_value <= 1.0 or not 0.0 <= self.alpha_level <= 1.0:
            raise ValueError("p_value and alpha_level are probabilities")
        if self.rejected != (self.p_value <= self.alpha_level):
            raise ValueError("a test rejects exactly when p_value <= alpha_level")
        if self.wealth_before < 0.0 or self.wealth_after < 0.0:
            raise ValueError("alpha-wealth is never negative")
        if self.family_size < 1:
            raise ValueError("family_size >= 1")
        return self


class MFDRRow(MFDRTest):
    """A recorded test with its position in the registry chain."""

    seq: int
    recorded_at: datetime


class MFDRState(RegistryModel):
    config: MFDRConfig | None
    n_tests: int
    n_rejections: int
    wealth: float | None            # None until configured
    contracts: tuple[str, ...]      # in order of first test


class MFDRLedger:
    """Registry-backed mFDR table; obtain it with ``Registry.mfdr()``."""

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    # -- reads ----------------------------------------------------------------------------------------------
    def config(self) -> MFDRConfig | None:
        rows = self._registry._query(
            "SELECT c.payload FROM mfdr_config m JOIN chain c ON c.seq = m.seq ORDER BY m.seq LIMIT 1")
        return load_json_payload(split_envelope(rows[0][0])[0], MFDRConfig) if rows else None

    def rows(self, *, contract_id: str | None = None) -> list[MFDRRow]:
        sql = "SELECT c.seq, c.payload FROM mfdr_tests m JOIN chain c ON c.seq = m.seq"
        params: tuple[object, ...] = ()
        if contract_id is not None:
            sql, params = sql + " WHERE m.contract_id = ?", (contract_id,)
        out = []
        for seq, payload in self._registry._query(sql + " ORDER BY m.seq", params):
            body, header = split_envelope(payload)
            test = load_json_payload(body, MFDRTest)
            out.append(MFDRRow(**dict(test), seq=seq, recorded_at=datetime.fromisoformat(header["recorded_at"])))
        return out

    def wealth(self) -> float:
        """Current alpha-wealth: the last test's ``wealth_after``, ``w0`` before any test."""
        cfg = self.config()
        if cfg is None:
            raise SchemaError("the mFDR ledger is not configured (MFDRLedger.configure)")
        last = self._registry._query(
            "SELECT c.payload FROM mfdr_tests m JOIN chain c ON c.seq = m.seq ORDER BY m.seq DESC LIMIT 1")
        return load_json_payload(split_envelope(last[0][0])[0], MFDRTest).wealth_after if last else cfg.w0

    def p_values(self) -> tuple[float, ...]:
        """The online p-values in test order (replay them through ``stats.AlphaInvesting``)."""
        return tuple(r.p_value for r in self.rows())

    def state(self) -> MFDRState:
        cfg = self.config()
        rows = self.rows()
        wealth = (rows[-1].wealth_after if rows else cfg.w0) if cfg is not None else None
        return MFDRState(config=cfg, n_tests=len(rows), n_rejections=sum(r.rejected for r in rows), wealth=wealth,
                         contracts=tuple(dict.fromkeys(r.contract_id for r in rows)))

    # -- writes ---------------------------------------------------------------------------------------------
    def configure(self, *, w0: float, payout: float, decay: float) -> MFDRConfig:
        """Fix the parameters once; a repeat call with the same values is a no-op, different values raise."""
        self._registry._check_write_allowed()
        try:
            cfg = MFDRConfig(w0=float(w0), payout=float(payout), decay=float(decay))
        except ValueError as exc:
            raise SchemaError(f"invalid mFDR parameters: {exc}") from exc
        with self._registry._transaction() as w:
            rows = w.conn.execute(
                "SELECT c.payload FROM mfdr_config m JOIN chain c ON c.seq = m.seq LIMIT 1").fetchall()
            if rows:
                existing = load_json_payload(split_envelope(rows[0][0])[0], MFDRConfig)
                if existing != cfg:
                    raise SchemaError(f"the mFDR ledger is configured with {existing.model_dump()}; parameters are "
                                      "fixed across contracts", {"existing": existing.model_dump()})
                return existing
            w.append(CONFIG_KIND, canonical_json(cfg).decode("utf-8"), cls=None, table="mfdr_config",
                     columns={"one": 1})
        return cfg

    def record(self, *, contract_id: str, hypothesis_id: str, p_value: float, alpha_level: float, rejected: bool,
               wealth_after: float, campaign_id: str | None = None, family_size: int = 1) -> str:
        """Append one online test; ``wealth_before`` is the ledger's current wealth. Returns the row hash."""
        self._registry._check_write_allowed()
        with self._registry._transaction() as w:
            cfg_rows = w.conn.execute(
                "SELECT c.payload FROM mfdr_config m JOIN chain c ON c.seq = m.seq LIMIT 1").fetchall()
            if not cfg_rows:
                raise SchemaError("configure the mFDR ledger before recording tests (MFDRLedger.configure)")
            last = w.conn.execute(
                "SELECT c.payload FROM mfdr_tests m JOIN chain c ON c.seq = m.seq ORDER BY m.seq DESC LIMIT 1").fetchall()
            before = (load_json_payload(split_envelope(last[0][0])[0], MFDRTest).wealth_after if last
                      else load_json_payload(split_envelope(cfg_rows[0][0])[0], MFDRConfig).w0)
            try:
                test = MFDRTest(contract_id=str(contract_id), campaign_id=None if campaign_id is None else str(campaign_id),
                                hypothesis_id=str(hypothesis_id), family_size=int(family_size),
                                p_value=float(p_value), alpha_level=float(alpha_level), rejected=bool(rejected),
                                wealth_before=before, wealth_after=float(wealth_after))
            except ValueError as exc:
                raise SchemaError(f"invalid mFDR test: {exc}", {"contract_id": contract_id}) from exc
            return w.append(TEST_KIND, canonical_json(test).decode("utf-8"), cls=None, table="mfdr_tests",
                            columns={"contract_id": contract_id})
