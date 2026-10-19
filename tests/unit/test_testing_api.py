"""The ``adic_tpa.testing`` API keeps the §4.5 signatures (BUILD_SPEC v1.1 §4.5, §0.2; owner WP-03).

Each public function must take §4.5's parameters first, unchanged (name, kind, default, annotation), may add only
parameters with defaults (§0.2), and must return the annotated type.
"""

from __future__ import annotations

import inspect
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

import adic_tpa.testing as testing
from adic_tpa.contracts import ports


class SPEC:
    """§4.5 verbatim (annotations as strings; bodies elided)."""

    def mini_book(allocation: AllocationId = "v2", *, seed: int = 7) -> BookSnapshot: ...  # noqa: F821
    def mini_cube(n_paths: int = 200, world: WorldId = "M1", *, seed: int = 7) -> ScenarioCube: ...  # noqa: F821
    def mini_flowcube(book: BookSnapshot, cube: ScenarioCube) -> FlowCube: ...  # noqa: F821
    def fixture_tree(branching: tuple[int, ...] = (2, 2, 2), *, unreduced: bool = True) -> Tree: ...  # noqa: F821
    def fake_engines(book: BookSnapshot) -> list[AssetEngine]: ...  # noqa: F821
    def fake_beliefs(book: BookSnapshot) -> BeliefSet: ...  # noqa: F821
    def golden(name: str) -> Any: ...
    def assert_manifest_reproduces(manifest_path: Path) -> None: ...
    def fixture_h() -> tuple[LPModel, HSolution, DualSet, Tree]: ...  # noqa: F821
    def fake_filter(params: StressFilterParams | None = None) -> Callable[..., F32]: ...  # noqa: F821
    def fake_owner_draws(cube: ScenarioCube, rate: float = 0.075) -> ScenarioCube: ...  # noqa: F821
    def fake_belief_draws(bs: BeliefSet, world: WorldSpec, n_paths: int) -> BeliefDraws: ...  # noqa: F821
    def synthetic_committee(register: Register, seed: int) -> SyntheticCommittee: ...  # noqa: F821


NAMES = [n for n in vars(SPEC) if not n.startswith("_")]


def _norm(annotation: Any) -> str:
    text = annotation if isinstance(annotation, str) else getattr(annotation, "__name__", repr(annotation))
    return re.sub(r"\s+", "", text.strip("'\""))


def _params(fn: Callable[..., Any]) -> list[tuple[str, str, str, str]]:
    return [(p.name, p.kind.name, "<none>" if p.default is inspect.Parameter.empty else repr(p.default),
             _norm(p.annotation)) for p in inspect.signature(fn).parameters.values()]


@pytest.mark.parametrize("name", NAMES)
def test_testing_api_refines_section_4_5(name: str) -> None:
    impl, spec = getattr(testing, name), getattr(SPEC, name)
    got, want = _params(impl), _params(spec)
    assert got[:len(want)] == want, f"{name}: {got} vs §4.5 {want}"
    assert all(p[2] != "<none>" for p in got[len(want):]), f"{name}: added parameters need defaults (§0.2)"
    assert _norm(inspect.signature(impl).return_annotation) == _norm(inspect.signature(spec).return_annotation)
    assert name in testing.__all__


def test_fake_ledger_subclasses_the_protocol() -> None:
    assert issubclass(testing.FakeLedger, ports.Ledger)              # §4.5: class FakeLedger(Ledger)
