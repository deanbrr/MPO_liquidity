"""Probability of backtest overfitting by combinatorially symmetric cross-validation (BUILD_SPEC v1.1 §4.4; ARCH §7.6
Gate 3; Bailey, Borwein, López de Prado & Zhu 2017).

``pbo_cscv(perf, n_blocks)``: ``perf`` is [n_trials, n_obs], one row per counted evaluation of the search ledger
(Gate 3 computes PBO there, never on the sealed plane) and one column per observation (path or structural block).
The observations are cut into ``n_blocks`` (even, ≥ 2) contiguous blocks (sizes differ by at most one when n_obs is
not a multiple). For each of the C(S, S/2) ways to choose half the blocks as in-sample: the trial with the best
in-sample performance is ranked out of sample (average ranks for ties, 1 = worst), its relative rank is
ω = rank/(N + 1) and its logit λ = ln(ω/(1 − ω)). PBO = the share of splits with λ ≤ 0, i.e. where the in-sample
winner is at or below the out-of-sample median (the closed interval is the conservative choice).

Performance on a set of observations is the mean (default), or the Sharpe ratio mean/sd with ``metric="sharpe"``.
"""

from __future__ import annotations

import itertools
from typing import Literal

import numpy as np
from scipy import stats as sps

from adic_tpa.contracts.arrays import F64
from adic_tpa.contracts.errors import SchemaError

__all__ = ["pbo_cscv"]


def pbo_cscv(perf: F64, n_blocks: int = 8, *, metric: Literal["mean", "sharpe"] = "mean") -> float:
    """PBO of the search ledger ``perf`` [n_trials, n_obs] by CSCV over ``n_blocks`` blocks (module docstring)."""
    m = np.asarray(perf, dtype=np.float64)
    if m.ndim != 2 or m.shape[0] < 2:
        raise SchemaError(f"pbo_cscv: perf must be [n_trials >= 2, n_obs], got shape {m.shape}")
    if not np.isfinite(m).all():
        raise SchemaError("pbo_cscv: perf must be finite")
    if isinstance(n_blocks, bool) or n_blocks < 2 or n_blocks % 2:
        raise SchemaError(f"pbo_cscv: n_blocks must be even and >= 2, got {n_blocks}")
    n_trials, n_obs = m.shape
    if n_obs < n_blocks * (2 if metric == "sharpe" else 1):
        raise SchemaError(f"pbo_cscv: {n_obs} observations cannot fill {n_blocks} blocks")
    if metric not in ("mean", "sharpe"):
        raise SchemaError(f"pbo_cscv: metric must be 'mean' or 'sharpe', got {metric!r}")
    blocks = np.array_split(np.arange(n_obs), n_blocks)
    sums = np.stack([m[:, b].sum(axis=1) for b in blocks], axis=1)              # [N, S]
    sumsq = np.stack([(m[:, b] ** 2).sum(axis=1) for b in blocks], axis=1)
    counts = np.array([b.size for b in blocks], dtype=np.float64)

    def score(mask: np.ndarray) -> F64:
        n = counts[mask].sum()
        mean = sums[:, mask].sum(axis=1) / n
        if metric == "mean":
            return mean
        var = (sumsq[:, mask].sum(axis=1) - n * mean * mean) / (n - 1.0)
        if (var <= 0).any():
            raise SchemaError("pbo_cscv: a trial has zero variance on a split; the Sharpe metric is undefined")
        return mean / np.sqrt(var)

    logits = []
    for chosen in itertools.combinations(range(n_blocks), n_blocks // 2):
        is_mask = np.zeros(n_blocks, dtype=bool)
        is_mask[list(chosen)] = True
        best = int(np.argmax(score(is_mask)))
        omega = sps.rankdata(score(~is_mask))[best] / (n_trials + 1.0)
        logits.append(np.log(omega / (1.0 - omega)))
    return float(np.mean(np.asarray(logits) <= 0.0))
