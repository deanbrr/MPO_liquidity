"""The synthetic committee and a ``RoomPort`` fake (BUILD_SPEC v1.1 §4.5, §4.31, S-ADR-37; owner WP-03).

SYNTHETIC – NOT ADIC DATA. ``synthetic_committee(register, seed)`` is the DEV_SYNTHETIC ballot source of the room:
seeded pre-votes and ballots from synthetic members (``member_hash`` = SHA-256 of "SYNTHETIC committee member k"),
every rationale prefixed with the SYNTHETIC footer. REAL mode refuses it (``RunModeRefused``): the caller passes the
contract's run mode (a keyword with the DEV default, a WP-03 refinement of the §4.5 signature).

``FakeRoom`` implements ``contracts.ports.RoomPort`` on a register, a committee and an ``EvaluatorPort`` (seat
numbers only from ``implied_actions``), with a hash-chained decision log (``prev_hash`` / ``record_hash``).
"""

from __future__ import annotations

import hashlib
from collections.abc import Collection, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any, Final, Literal, TypeVar

import numpy as np
from pydantic import BaseModel

from adic_tpa import SYNTHETIC_FOOTER
from adic_tpa.contracts.claims import RenderedDocument, ValidationReport
from adic_tpa.contracts.enums import ConsentScenario, DataClass, OptionKind, Plane, PricedOn, RunMode
from adic_tpa.contracts.errors import RunModeRefused, SchemaError
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.contracts.ids import ArtifactRef, DecisionId, MetricId
from adic_tpa.contracts.ports import EvaluatorPort
from adic_tpa.contracts.room import (
    Ballot, DecisionRecord, EvidencePlan, OptionSummary, PreVote, Register, RunSpec, SeatAssessment,
)
from adic_tpa.contracts.tools import ImpliedIn

__all__ = ["SyntheticCommittee", "synthetic_committee", "FakeRoom", "GENESIS_HASH", "CHOICES"]

Choice = Literal["approve", "resize", "defer", "reject"]
CHOICES: Final[tuple[Choice, ...]] = ("approve", "resize", "defer", "reject")
_CHOICE_P: Final = np.array([0.55, 0.20, 0.15, 0.10])          # seeded choice probabilities [I]
GENESIS_HASH: Final = "sha256:" + "0" * 64
_STAMP: Final = datetime(2026, 10, 18, 9, 0, tzinfo=timezone.utc)
_N_MEMBERS: Final = 7
M = TypeVar("M", bound=BaseModel)


def _rng(*parts: object) -> np.random.Generator:
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).digest()
    return np.random.Generator(np.random.Philox(key=np.frombuffer(digest[:16], dtype=np.uint64).copy()))


def _member_hash(k: int) -> str:
    return "sha256:" + hashlib.sha256(f"SYNTHETIC committee member {k}".encode("utf-8")).hexdigest()


def _sealed(model: type[M], field: str, **body: Any) -> M:
    """``model(**body)`` with ``field`` = content hash of every other field, defaults included (§4.1)."""
    draft = model(**body, **{field: GENESIS_HASH})
    return model(**body, **{field: content_hash(draft.model_dump(exclude={field}))})


@dataclass(frozen=True, slots=True)
class SyntheticCommittee:
    """Seeded synthetic IC members (DEV_SYNTHETIC only; S-ADR-37). Deterministic per (register, seed, item)."""

    register_hash: str
    items: tuple[str, ...]
    seed: int
    members: tuple[str, ...]
    run_mode: RunMode = RunMode.DEV_SYNTHETIC
    label: str = SYNTHETIC_FOOTER

    def __post_init__(self) -> None:
        if self.run_mode is not RunMode.DEV_SYNTHETIC:
            raise RunModeRefused("the synthetic committee is a DEV_SYNTHETIC facility, refused in REAL mode "
                                 "(S-ADR-37)", {"facility": "synthetic_committee"})

    def _check(self, item_id: str) -> None:
        if item_id not in self.items:
            raise SchemaError(f"synthetic committee: {item_id!r} is not a register entry {self.items}")

    def _draw(self, item_id: str, member: str, purpose: str) -> tuple[Choice, dict[str, float]]:
        rng = _rng("synthetic_committee", self.register_hash, self.seed, item_id, member, purpose)
        choice = CHOICES[int(np.searchsorted(np.cumsum(_CHOICE_P), rng.random(), side="right").clip(0, 3))]
        return choice, {"p_recommended_meets_target": round(float(rng.random()), 4)}

    def prevotes(self, item_id: str, *, locked_at: datetime = _STAMP) -> tuple[PreVote, ...]:
        """One locked pre-vote per member for ``item_id`` (SYNTHETIC)."""
        self._check(item_id)
        out = []
        for member in self.members:
            choice, probs = self._draw(item_id, member, "prevote")
            out.append(_sealed(PreVote, "hash", member_hash=member, item_id=item_id, choice=choice,
                               probabilities=probs, rationale=f"{SYNTHETIC_FOOTER}: seeded synthetic pre-vote",
                               locked_at=locked_at))
        return tuple(out)

    def ballots(self, item_id: str, *, cast_at: datetime = _STAMP + timedelta(days=7),
                recused: Collection[str] = ()) -> tuple[Ballot, ...]:
        """One ballot per member for ``item_id``; members in ``recused`` cast recorded, recused ballots."""
        self._check(item_id)
        out = []
        for member in self.members:
            choice, probs = self._draw(item_id, member, "ballot")
            out.append(_sealed(Ballot, "hash", member_hash=member, item_id=item_id, choice=choice,
                               probabilities=probs, rationale=f"{SYNTHETIC_FOOTER}: seeded synthetic ballot",
                               what_would_change="SYNTHETIC: a T4' survival reading below 18 months",
                               recused=member in recused, second_chance_ack=True,
                               how_could_be_wrong="SYNTHETIC: the drought persists beyond the tree's horizon",
                               cast_at=cast_at))
        return tuple(out)


def synthetic_committee(register: Register, seed: int, *,
                        run_mode: RunMode = RunMode.DEV_SYNTHETIC) -> SyntheticCommittee:
    """The seeded SYNTHETIC committee of ``register`` (§4.5); ``RunModeRefused`` when ``run_mode`` is REAL."""
    if run_mode is not RunMode.DEV_SYNTHETIC:
        raise RunModeRefused("synthetic_committee is refused in REAL mode (S-ADR-37)",
                             {"facility": "synthetic_committee", "run_mode": run_mode.value})
    return SyntheticCommittee(register_hash=register.hash, items=tuple(e.id for e in register.entries), seed=seed,
                              members=tuple(_member_hash(k) for k in range(_N_MEMBERS)), run_mode=run_mode)


class FakeRoom:
    """Implements ``contracts.ports.RoomPort`` (§3.17) for tests: agenda from the register's evidence specs, briefs
    as validated SYNTHETIC documents, seat assessments from ``EvaluatorPort.implied_actions``, pre-votes and ballots
    from the synthetic committee, and a hash-chained decision log."""

    def __init__(self, register: Register, committee: SyntheticCommittee, evaluator: EvaluatorPort, *,
                 asof: date = date(2026, 10, 18), run_ref: ArtifactRef | None = None) -> None:
        self.register = register
        self.committee = committee
        self.evaluator = evaluator
        self.asof = asof
        self.run_ref = run_ref if run_ref is not None else ArtifactRef("run-20261018T000000Z-0000fa4e:room:")
        self.prevote_hashes: dict[str, tuple[str, ...]] = {}

    def compile_agenda(self, quarter: str, snapshot_hash: str) -> EvidencePlan:
        specs, by_decision = [], {}
        for entry in self.register.entries:
            names = []
            for ev in entry.evidence:
                args = {"metric": str(ev.metric), "quarter": quarter, "snapshot_hash": snapshot_hash}
                spec = RunSpec(tool="get_metric", args=args, plane=Plane.SEARCH, spec_hash=content_hash(args))
                specs.append(spec)
                names.append(spec.spec_hash)
            by_decision[entry.id] = tuple(names)
        return _sealed(EvidencePlan, "hash", specs=tuple(specs), edges=(), by_decision=by_decision)

    def _document(self, doc_id: str, kind: Literal["brief", "seat_argument"], text: str) -> RenderedDocument:
        return RenderedDocument(doc_id=doc_id, kind=kind, template_text=text, rendered_html=f"<p>{text}</p>",
                                claims=(), validation=ValidationReport(passed=True, coverage=1.0, errors=()),
                                provenance_root=self.run_ref, data_class=DataClass.SYNTHETIC)

    def build_briefs(self, plan: EvidencePlan) -> tuple[RenderedDocument, ...]:
        return tuple(self._document(f"brief-{item}", "brief", f"{SYNTHETIC_FOOTER}. Brief for {item}: "
                                    f"{len(specs)} evidence item(s).") for item, specs in plan.by_decision.items())

    def run_shadow_ic(self, items: Sequence[str]) -> tuple[SeatAssessment, ...]:
        out = []
        for item in items:
            card = self.evaluator.implied_actions(ImpliedIn(seat_id="CRO", item_id=item))
            out.append(_sealed(
                SeatAssessment, "hash", seat_id=card.seat_id, item_id=item, implied_action_ref=card.ref,
                regret_bp=dict(card.regret_bp_by_option), belief_value_split=(0.5, 0.5), event_probs_ref=card.ref,
                cruxes=("SYNTHETIC crux",),
                argument=self._document(f"seat-{card.seat_id}-{item}", "seat_argument",
                                        f"{SYNTHETIC_FOOTER}. Seat argument (engine numbers only).")))
        return tuple(out)

    def lock_prevotes(self, quarter: str) -> tuple[str, ...]:
        hashes = []
        for entry in self.register.entries:
            locked = tuple(pv.hash for pv in self.committee.prevotes(entry.id))
            self.prevote_hashes[entry.id] = locked
            hashes.extend(locked)
        return tuple(hashes)

    def record_decisions(self, quarter: str) -> tuple[DecisionRecord, ...]:
        records, prev = [], GENESIS_HASH
        metric = MetricId("tier1.t6.cp_upper@v1")
        for n, entry in enumerate(self.register.entries, start=1):
            ballots = self.committee.ballots(entry.id)
            tally = {c: sum(b.choice == c for b in ballots if not b.recused) for c in CHOICES}
            options = tuple(OptionSummary(kind=k, label=k.value, policy_ref=None, delta_ce_bp=metric,
                                          p_red_by_class={"M1_M5": metric}, p10_target=metric,
                                          delta_survival_months=metric) for k in entry.always_show)
            body = dict(
                decision_id=DecisionId(f"dec-{entry.id}-{quarter}-{n}"), register_id=entry.id, as_of=self.asof,
                tier="A", options=options, engine_recommendation=OptionKind.RECOMMENDED.value,
                evidence_plane="search", run_manifests=(self.run_ref.run_id,), priced_on=PricedOn.FEASIBLE,
                consent_scenario=ConsentScenario.R1, recovery_hash=None,
                prevote_hashes=self.prevote_hashes.get(entry.id, ()), ballots=ballots,
                decision=max(CHOICES, key=lambda c: (tally[c], -CHOICES.index(c))), override=None,
                rationale=f"{SYNTHETIC_FOOTER}: synthetic committee majority", minority_reports=(), signposts=(),
                commitment_plan=(), review_date=date(2027, 1, 15), data_class=DataClass.SYNTHETIC, prev_hash=prev)
            record = _sealed(DecisionRecord, "record_hash", **body)
            records.append(record)
            prev = record.record_hash
        return tuple(records)
