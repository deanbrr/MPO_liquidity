"""Every WP-02 numba kernel equals its own Python body (BUILD_SPEC v1.1 §1.13, §10.3). Owner WP-02.

Each kernel and inlined helper is run uncompiled through ``.py_func`` on small inputs and compared with the compiled
result: integers bit for bit, floats to rounding. During the Python runs the modules' helper names point at their
``.py_func`` too (compiled helpers return uint64 as Python ints, which cannot be passed back in), so the whole chain
executes as Python. This pins the jitted code to readable Python, keeps the kernels working under
``NUMBA_DISABLE_JIT=1``, and lets the ``sys.monitoring`` line-coverage tool (§10.3) see kernel lines, which compiled
code never executes as Python. SYNTHETIC seeds only.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from adic_tpa.contracts.enums import Plane
from adic_tpa.rng import base_entropy, stream_keys
from adic_tpa.rng import philox as px
from adic_tpa.rng import samplers as sm

KEYS = stream_keys(base_entropy(3, Plane.SEARCH, "M1"), "parity", ["SYN-PE-0001", None])
PATHS = np.array([0, 5, 1999], dtype=np.uint64)
MONTHS = np.array([0, 119], dtype=np.uint64)
U = np.array([0.0, 1e-12, 0.0123, 0.25, 0.5, 0.75, 0.99, 1.0 - 2.0 ** -53])


def _python_bodies(monkeypatch: pytest.MonkeyPatch, module: object, names: tuple[str, ...]) -> None:
    for name in names:
        monkeypatch.setattr(module, name, getattr(module, name).py_func)


def test_mulhilo_reference_is_the_exact_128_bit_product() -> None:
    for a, b in ((0, 0), (2 ** 64 - 1, 2 ** 64 - 1), (0xD2E7470EE14C6C93, 12345), (2 ** 63, 2)):
        lo, hi = px._mulhilo(np.uint64(a), np.uint64(b))
        assert (int(hi) << 64) | int(lo) == a * b


def test_philox_kernels_match_their_python_bodies(monkeypatch: pytest.MonkeyPatch) -> None:
    ctr = np.array([[1, 2, 3, 4], [2 ** 64 - 1, 0, 7, 0]], dtype=np.uint64)
    key = KEYS[0]
    compiled = px.philox4x64_10(ctr, key)
    unit_top = px._unit(np.uint64(2 ** 64 - 1))
    _python_bodies(monkeypatch, px, ("_round", "_philox", "_philox_row", "_unit"))
    with np.errstate(over="ignore"):                         # uint64 scalar arithmetic wraps, as in the kernel
        for i in range(2):
            assert tuple(int(x) for x in px._philox(*ctr[i], key[0], key[1])) == tuple(int(x) for x in compiled[i])
        for kern in (px._philox_kernel, px._philox_kernel_serial):
            out = np.empty_like(compiled)
            kern.py_func(ctr, key, out)
            assert np.array_equal(out, compiled)
        assert px._unit(np.uint64(2 ** 64 - 1)) == unit_top


def test_uniform_kernels_match_their_python_bodies(monkeypatch: pytest.MonkeyPatch) -> None:
    slots = 6
    compiled = px.fill_uniforms(KEYS, PATHS, MONTHS, slots)
    _python_bodies(monkeypatch, px, ("_round", "_philox", "_unit", "_uniform_path"))
    with np.errstate(over="ignore"):
        for kern in (px._uniform_kernel, px._uniform_kernel_serial):
            out = np.empty_like(compiled)
            kern.py_func(KEYS, PATHS, MONTHS, slots, out)
            assert np.array_equal(out, compiled)


@pytest.mark.parametrize("df", [5.0, 3.0])
def test_student_t_kernel_matches_its_python_body(df: float, monkeypatch: pytest.MonkeyPatch) -> None:
    tab = sm._t_table(df)
    lo = tab.lower
    args = (lo.x0, lo.inv_h, lo.h, lo.values, lo.derivs, tab.tail, tab.log_u_split, tab.nu, tab.log_a, tab.log_c,
            tab.log_t0, tab.betas, 1.0)
    fast = np.empty_like(U)
    sm._t_kernel(U, fast, *args)
    _python_bodies(monkeypatch, sm, ("_hermite", "_t_tail"))
    slow = np.empty_like(U)
    sm._t_kernel.py_func(U, slow, *args)
    assert np.allclose(slow, fast, rtol=1e-13, atol=1e-15)
    assert math.isfinite(sm._t_tail(math.log(1e-9), tab.nu, tab.log_a, tab.log_c, tab.log_t0, tab.betas))


def test_gamma_kernel_matches_its_python_body(monkeypatch: pytest.MonkeyPatch) -> None:
    g = sm._gamma_table(2.5)
    args = (g.lower.x0, g.lower.inv_h, g.lower.h, g.lower.values, g.lower.derivs, g.upper.x0, g.upper.inv_h,
            g.upper.h, g.upper.values, g.upper.derivs, 2.0)
    fast = np.empty_like(U)
    sm._gamma_kernel(U, fast, *args)
    _python_bodies(monkeypatch, sm, ("_hermite",))
    slow = np.empty_like(U)
    sm._gamma_kernel.py_func(U, slow, *args)
    assert np.allclose(slow, fast, rtol=1e-13, atol=1e-300)
