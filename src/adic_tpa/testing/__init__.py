"""Testing kit: frozen fixtures and Protocol fakes (BUILD_SPEC v1.1 §4.5; owner WP-03).

SYNTHETIC – NOT ADIC DATA. Every stream builds against these frozen tensors and fakes before the real engines exist
(ARCH §3.4): ``mini_book``, ``mini_cube``, ``mini_flowcube``, ``fixture_tree``, ``fake_engines``, ``FakeLedger``,
``fake_beliefs``, ``golden``, ``assert_manifest_reproduces``, ``fixture_h``, ``fake_filter``, ``fake_owner_draws``,
``fake_belief_draws`` and ``synthetic_committee`` (§4.5), plus the fakes of the remaining §3.17 Protocols
(``FakeEngineFactory``, ``FakePolicy``, ``FakeLLMBackend``, ``FakeEvaluator``, ``FakeRoom``) and the mini world,
state, owner configuration, register and contract the walking skeleton needs.

``testing`` imports ``contracts`` only (§4.0 allows ``rng`` and ``numerics`` too); ``fakes.fake_draw_block`` stands
in for ``rng.draw_block`` until WP-02 lands.
"""

from __future__ import annotations

from adic_tpa.testing.committee import FakeRoom, SyntheticCommittee, synthetic_committee
from adic_tpa.testing.fakes import (
    EVALUATOR_METHODS, MINI_ASSET_CLASSES, FakeEngine, FakeEngineFactory, FakeEngineState, FakeEvaluator,
    FakeLedger, FakeLLMBackend, FakePolicy, book_hold_flows, fake_belief_draws, fake_beliefs, fake_draw_block,
    fake_engines, fake_filter, fake_filter_params, fake_observables, fake_owner_draws, merge_outcomes, merge_quotes,
    simulate_hold, unit_models, world_slice,
)
from adic_tpa.testing.fixture_h import build_fixture_lp, fixture_h, fixture_phase1, solve_fixture_lp
from adic_tpa.testing.fixtures import (
    MINI_FACTORS, mini_book, mini_contract, mini_cube, mini_flowcube, mini_owner_config, mini_register, mini_signoff,
    mini_state0, mini_world,
)
from adic_tpa.testing.golden import (
    assert_manifest_reproduces, check_frozen_fixtures, frozen_fixture_checksums, golden, golden_path, port_manifest,
    write_frozen_fixtures,
)
from adic_tpa.testing.trees import fixture_tree

__all__ = [
    # §4.5 API
    "mini_book", "mini_cube", "mini_flowcube", "fixture_tree", "fake_engines", "FakeLedger", "fake_beliefs", "golden",
    "assert_manifest_reproduces", "fixture_h", "fake_filter", "fake_owner_draws", "fake_belief_draws",
    "synthetic_committee", "SyntheticCommittee",
    # refinements (WP-03)
    "mini_world", "mini_state0", "mini_owner_config", "mini_register", "mini_signoff", "mini_contract", "MINI_FACTORS",
    "MINI_ASSET_CLASSES", "FakeEngine", "FakeEngineState", "FakeEngineFactory", "FakePolicy", "FakeLLMBackend",
    "FakeEvaluator", "EVALUATOR_METHODS", "FakeRoom", "fake_filter_params", "fake_draw_block", "fake_observables",
    "merge_quotes", "merge_outcomes", "simulate_hold", "book_hold_flows", "unit_models", "world_slice",
    "fixture_phase1", "build_fixture_lp", "solve_fixture_lp", "golden_path", "port_manifest",
    "frozen_fixture_checksums", "check_frozen_fixtures", "write_frozen_fixtures",
]
