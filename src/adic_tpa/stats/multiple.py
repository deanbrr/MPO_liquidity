"""Multiple-testing control: Holm within a cycle, α-investing across cycles (BUILD_SPEC v1.1 §4.4, §7.7; ARCH §7.7;
S-ADR-18).

``holm(pvalues, alpha)`` is Holm's step-down procedure: sort the p-values, reject p_(i) while p_(i) ≤ α/(m − i + 1),
stop at the first acceptance; it controls the family-wise error rate at α under any dependence.

``AlphaInvesting`` is decaying-memory generalized α-investing (Foster & Stine 2008; Aharoni & Rosset 2014; Ramdas
et al. 2017) with wealth W₀ = ``w0``, payout ω = ``payout`` and memory factor δ = ``decay``. Test j spends the
fraction (1 − δ) of the current wealth, φ_j = (1 − δ)·W_{j−1}, at level α_j = φ_j/(1 + φ_j), i.e. at the
Foster–Stine price φ_j = α_j/(1 − α_j). A rejection returns the stake plus the payout (W_j = W_{j−1} + ω); an
acceptance loses it (W_j = δ·W_{j−1}). So the wealth decays geometrically while nothing is found, and a reward earned
k tests ago contributes (1 − δ)δ^k of itself to the current level: the memory of past discoveries decays (the
geometric spending sequence of LORD-type rules; Ramdas et al.'s remedy for piggybacking). ``decay = 0`` is the
research's all-in rule α_j = W/(1 + W), 0.0476 at the start (C4 §5.7(h)). The rule meets the generalized α-investing
conditions with α = ω (φ_j ≤ W_{j−1}; reward ψ_j = φ_j + ω ≤ min(φ_j/α_j + α − 1, φ_j + α)), so it controls
mFDR_η = E[V]/(E[R] + η) ≤ ω with η = W₀/ω (1 at the defaults) for independent tests. Alpha-death is not repaired
automatically: the lab escalates when the wealth falls below 0.005 (§7.7), about 22 consecutive unrewarded tests at
the defaults, and any reset is decided by MRM and the IC. (WP-02 reading of the §4.4 signature, which fixes only
``w0``, ``payout``, ``decay``, ``test`` and ``wealth``.)
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np

from adic_tpa.contracts.errors import SchemaError

__all__ = ["holm", "AlphaInvesting"]


def _check_p(p: float, where: str) -> float:
    v = float(p)
    if not 0.0 <= v <= 1.0:          # NaN fails too
        raise SchemaError(f"{where}: p-values must lie in [0, 1], got {p!r}")
    return v


def holm(pvalues: Sequence[float], alpha: float) -> tuple[bool, ...]:
    """Holm step-down rejections at FWER level ``alpha``, in the order of ``pvalues``."""
    if not 0.0 < float(alpha) < 1.0:
        raise SchemaError(f"holm: alpha must lie in (0, 1), got {alpha}")
    p = np.asarray([_check_p(x, "holm") for x in pvalues], dtype=np.float64)
    m = p.size
    reject = np.zeros(m, dtype=bool)
    for rank, idx in enumerate(np.argsort(p, kind="stable")):
        if p[idx] <= alpha / (m - rank):
            reject[idx] = True
        else:
            break
    return tuple(bool(r) for r in reject)


class AlphaInvesting:
    """Decaying-memory generalized α-investing ledger (module docstring). Mutable: ``test`` updates the wealth."""

    def __init__(self, w0: float = 0.05, payout: float = 0.05, decay: float = 0.9) -> None:
        if not (math.isfinite(w0) and w0 > 0):
            raise SchemaError(f"AlphaInvesting: w0 must be positive, got {w0}")
        if not (math.isfinite(payout) and 0 < payout < 1):
            raise SchemaError(f"AlphaInvesting: payout must lie in (0, 1), got {payout}")
        if not 0.0 <= decay < 1.0:
            raise SchemaError(f"AlphaInvesting: decay must lie in [0, 1), got {decay}")
        self._w0 = float(w0)
        self._payout = float(payout)
        self._decay = float(decay)
        self._wealth = float(w0)
        self._n_tests = 0
        self._n_rejections = 0

    @property
    def wealth(self) -> float:
        """Current α-wealth W_j (the lab escalates below 0.005)."""
        return self._wealth

    @property
    def level(self) -> float:
        """The level α_j the next ``test`` will use, φ/(1 + φ) with φ = (1 − decay)·wealth (e.g. for Holm within a
        cycle at the α-investing allocation)."""
        stake = (1.0 - self._decay) * self._wealth
        return stake / (1.0 + stake)

    @property
    def alpha(self) -> float:
        """The controlled mFDR level (= payout)."""
        return self._payout

    @property
    def eta(self) -> float:
        """η of the controlled mFDR_η = E[V]/(E[R] + η), W₀/payout."""
        return self._w0 / self._payout

    @property
    def n_tests(self) -> int:
        return self._n_tests

    @property
    def n_rejections(self) -> int:
        return self._n_rejections

    def test(self, p: float) -> bool:
        """Test one hypothesis (or one cycle's family p-value) at the current level; update the wealth."""
        pv = _check_p(p, "AlphaInvesting.test")
        stake = (1.0 - self._decay) * self._wealth
        rejected = stake > 0.0 and pv <= stake / (1.0 + stake)    # no wealth, no test (alpha-death)
        self._wealth = self._wealth + self._payout if rejected else self._wealth - stake
        self._n_tests += 1
        self._n_rejections += int(rejected)
        return rejected
