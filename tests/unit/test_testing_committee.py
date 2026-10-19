"""Synthetic committee and the RoomPort fake (BUILD_SPEC v1.1 §4.5, §4.31, S-ADR-37; owner WP-03).

SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

import pytest

from adic_tpa import SYNTHETIC_FOOTER
from adic_tpa.contracts import ports
from adic_tpa.contracts.enums import DataClass, RunMode
from adic_tpa.contracts.errors import RunModeRefused, SchemaError
from adic_tpa.contracts.hashing import content_hash
from adic_tpa.testing import FakeEvaluator, FakeRoom, SyntheticCommittee, mini_register, synthetic_committee
from adic_tpa.testing.committee import CHOICES, GENESIS_HASH


def test_committee_is_seeded_and_labelled() -> None:
    reg = mini_register()
    c = synthetic_committee(reg, 1)
    assert c.items == ("Q1", "Q2") and len(c.members) == 7 and len(set(c.members)) == 7
    pv = c.prevotes("Q1")
    assert pv == synthetic_committee(reg, 1).prevotes("Q1")
    assert all(v.rationale.startswith(SYNTHETIC_FOOTER) and v.choice in CHOICES for v in pv)
    for v in pv:
        assert v.hash == content_hash(v.model_dump(exclude={"hash"}))
    other = synthetic_committee(reg, 2).prevotes("Q1")
    assert [v.probabilities for v in other] != [v.probabilities for v in pv]


def test_ballots_record_recusals() -> None:
    c = synthetic_committee(mini_register(), 3)
    ballots = c.ballots("Q2", recused={c.members[0]})
    assert ballots[0].recused and not any(b.recused for b in ballots[1:])
    assert all(b.rationale.startswith(SYNTHETIC_FOOTER) and b.second_chance_ack for b in ballots)
    with pytest.raises(SchemaError):
        c.ballots("Q9")


def test_real_mode_refuses_the_synthetic_committee() -> None:
    reg = mini_register()
    with pytest.raises(RunModeRefused):
        synthetic_committee(reg, 1, run_mode=RunMode.REAL)
    c = synthetic_committee(reg, 1)
    with pytest.raises(RunModeRefused):
        SyntheticCommittee(register_hash=c.register_hash, items=c.items, seed=1, members=c.members,
                           run_mode=RunMode.REAL)


def test_fake_room_flow_and_decision_chain() -> None:
    reg = mini_register()
    ev = FakeEvaluator()
    room = FakeRoom(reg, synthetic_committee(reg, 5), ev)
    assert isinstance(room, ports.RoomPort)
    plan = room.compile_agenda("2026Q4", "sha256:" + "1" * 64)
    assert set(plan.by_decision) == {"Q1", "Q2"} and plan.hash == content_hash(plan.model_dump(exclude={"hash"}))
    briefs = room.build_briefs(plan)
    assert len(briefs) == 2 and all(b.data_class is DataClass.SYNTHETIC and SYNTHETIC_FOOTER in b.template_text
                                    for b in briefs)
    seats = room.run_shadow_ic(["Q1"])
    assert ev.calls == ["implied_actions"] and seats[0].item_id == "Q1"
    assert seats[0].hash == content_hash(seats[0].model_dump(exclude={"hash"}))
    locked = room.lock_prevotes("2026Q4")
    assert len(locked) == 14
    records = room.record_decisions("2026Q4")
    assert records[0].prev_hash == GENESIS_HASH and records[1].prev_hash == records[0].record_hash
    for r in records:
        assert r.record_hash == content_hash(r.model_dump(exclude={"record_hash"}))
        assert r.prevote_hashes == room.prevote_hashes[r.register_id] and r.data_class is DataClass.SYNTHETIC
        tally = {ch: sum(b.choice == ch for b in r.ballots if not b.recused) for ch in CHOICES}
        assert tally[r.decision] == max(tally.values())
