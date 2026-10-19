"""The fixture scenario tree (BUILD_SPEC v1.1 §4.5, §3.7, §5.13; owner WP-03). SYNTHETIC – NOT ADIC DATA."""

from __future__ import annotations

import numpy as np
import pytest

from adic_tpa.contracts.enums import StressState
from adic_tpa.contracts.errors import SchemaError
from adic_tpa.testing import fixture_tree
from adic_tpa.testing.trees import FIXTURE_TREE_WORLDS, N_FACILITIES


def _members(tree, node: int) -> list[int]:
    return tree.member_idx[tree.member_ptr[node]:tree.member_ptr[node + 1]].tolist()


def test_default_tree_shape_and_probabilities() -> None:
    tree = fixture_tree()
    tree.validate()
    assert tree.p.size == 15 and int(tree.is_leaf.sum()) == 8
    assert tree.pooled_worlds == FIXTURE_TREE_WORLDS == tree.spec.worlds
    assert tree.p[0] == pytest.approx(1.0, abs=1e-15)
    assert tree.p[tree.is_leaf].sum() == pytest.approx(1.0, abs=1e-15)
    for k in range(len(tree.pooled_worlds)):                       # each world's leaves carry its whole mass
        assert tree.p_world[tree.is_leaf, k].sum() == pytest.approx(1.0, abs=1e-15)
        assert int((tree.leaf_world == k).sum()) == 4
    child_mass = np.bincount(tree.parent[1:], weights=tree.p[1:], minlength=tree.p.size)
    interior = ~tree.is_leaf
    assert np.array_equal(child_mass[interior], tree.p[interior])  # parents are exact sums of their children


def test_breadth_first_order_and_periods() -> None:
    tree = fixture_tree()
    assert tree.parent.tolist() == [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
    assert tree.stage.tolist() == [0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]
    assert tree.t_end.tolist() == tree.stage.tolist() and tree.period_q[0] == 0 and (tree.period_q[1:] == 1).all()
    semi = fixture_tree(period_q=2)
    assert (semi.t_end == 2 * tree.t_end).all() and semi.spec.fan_ends_q == (6,)
    assert not np.array_equal(semi.coef.ret_simple, tree.coef.ret_simple)


def test_unreduced_tree_has_one_path_per_leaf_and_exact_coefficients() -> None:
    tree = fixture_tree()
    leaves = np.flatnonzero(tree.is_leaf)
    assert [_members(tree, int(n)) for n in leaves] == [[i] for i in range(8)]
    assert _members(tree, 0) == list(range(8))
    for node in range(1, tree.p.size):                             # a node holds the paths of its subtree
        assert set(_members(tree, node)) <= set(_members(tree, int(tree.parent[node])))
    reduced = fixture_tree(unreduced=False)
    reduced.validate()
    assert [len(_members(reduced, int(n))) for n in leaves] == [3] * 8
    assert reduced.spec.paths_per_world == 12 and tree.spec.paths_per_world == 4
    assert not np.array_equal(reduced.coef.delta, tree.coef.delta), "reduced nodes average differing paths"


def test_regimes_follow_branch_parity() -> None:
    tree = fixture_tree()
    crisis = tree.regime_class == StressState.CRISIS
    assert not crisis[0] and crisis.tolist()[1:3] == [False, True]
    assert (tree.coef.ret_simple[crisis].mean() < tree.coef.ret_simple[~crisis].mean())
    assert (tree.coef.fac_avail.shape == (15, N_FACILITIES)) and (tree.coef.fac_avail[crisis] == 0.5).all()


def test_tree_is_deterministic_and_hash_sensitive() -> None:
    a, b = fixture_tree(), fixture_tree()
    assert a.tree_hash == b.tree_hash and a.checksum() == b.checksum()
    assert fixture_tree((3, 2)).tree_hash != a.tree_hash
    assert fixture_tree(worlds=("M1", "M2")).tree_hash != a.tree_hash
    single = fixture_tree((2, 2), worlds=("M1",))
    single.validate()
    assert single.p_world.shape == (7, 1)


@pytest.mark.parametrize("kwargs", [dict(branching=()), dict(branching=(2, 0)), dict(period_q=3),
                                    dict(branching=(1,), worlds=("M1", "M6"))])
def test_invalid_trees_are_refused(kwargs: dict) -> None:
    with pytest.raises(SchemaError):
        fixture_tree(**kwargs)
