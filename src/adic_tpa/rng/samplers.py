"""Vectorized inverse-CDF samplers, one uniform per variate (BUILD_SPEC v1.1 §1.7, §4.2; S-ADR-38).

Every sampler maps uniforms u ∈ [0, 1) (the output of ``rng.uniforms``) through an inverse CDF, so slot accounting
is exact: a variate consumes its pre-indexed slot whether or not it is used. Inputs outside [0, 1), or NaN, raise
``SchemaError``. ``u`` below ``U_MIN = 2^-54`` (half the generator's 2^-53 grid step; in practice only u = 0) is read
as ``U_MIN``, so no inverse CDF returns an infinity.

Tabulated inverse CDFs (S-ADR-38: ``stdtrit``/``gammaincinv`` cost ≈ 180–200 ns per variate, so they serve only to
build tables and in tests). A table is built once per parameter value (memoized) from scipy's quantiles and exact
densities, as cubic Hermite interpolation on a uniform grid in a log coordinate; the grid is doubled until the
error at every cell mid-point is ≤ ``TABLE_TOL`` = 1e-9, 100 times inside the §4.2 contract (abs error < 1e-7).

- Student t (``df`` = ν): by symmetry only the lower half is tabulated, Q(e^v) for v = log u ∈ [log u_split,
  log ½]; u > ½ uses Q(u) = −Q(1 − u) with 1 − u exact. Below u_split = F(−√(ν/0.2)) the tail is the convergent
  asymptotic expansion F(−t) = c ν^{(ν+1)/2} t^{−ν} Σ_k binom(−(ν+1)/2, k) (ν/t²)^k/(ν + 2k), inverted by Newton in
  log t from the leading term (relative error ≈ 5e-15, so the absolute bound also holds where |t| reaches the
  thousands). The absolute bound is met for ν ≥ 2.5; for smaller ν the extreme quantiles pass 10^7 and only the
  ≈ 5e-15 relative accuracy (float64 resolution) holds there.
  ``standardize`` multiplies by √((ν − 2)/ν) (unit variance; S-ADR-35).
- Gamma (``shape`` = a): two tables of L = log Q, over v = log u for u ≤ ½ and w = log(1 − u) for u > ½, so the
  power-law lower tail (log Q ≈ (log u + log Γ(a+1))/a) and the logarithmic upper tail are both nearly linear in the
  table coordinate. Where scipy's quantile underflows, log Q comes from that lower-tail limit. The 1e-7 bound
  applies to the unit-scale quantile; ``scale`` multiplies it.

The other samplers are closed forms: ``normal`` = ``scipy.special.ndtri``; ``exponential`` = −log(1 − u)/rate;
``bernoulli`` = u < p; ``categorical`` = #{k: cum_k ≤ u}; ``kou_jump`` = one double-exponential jump per period with
probability 1 − e^{−λ} (three uniforms: occurrence, size, sign; WP-02 reading of §4.2).
"""

from __future__ import annotations

import functools
import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

import numpy as np
from scipy import special

from adic_tpa.contracts.arrays import B, F64, I8
from adic_tpa.contracts.errors import SchemaError, SolverError
from adic_tpa.numerics.numba_utils import inline_helper, kernel

__all__ = ["U_MIN", "TABLE_TOL", "normal", "student_t", "truncated_t", "gamma", "exponential", "bernoulli",
           "categorical", "kou_jump", "warm_samplers"]

U_MIN: Final = 2.0 ** -54
TABLE_TOL: Final = 1e-9
_HALF_LOG: Final = math.log(0.5)
_T_TAIL_X_MAX: Final = 0.2          # the t tail expansion is used where ν/t² ≤ 0.2
_T_TAIL_TERM_TOL: Final = 1e-18
_T_TAIL_MAX_TERMS: Final = 4000
_T_NEWTON_MAX: Final = 30
_T_NEWTON_TOL: Final = 1e-12        # checked after the step is applied, so the result is at rounding level
_TABLE_N0: Final = 257
_TABLE_N_MAX: Final = 2 ** 18 + 1
_TABLE_CACHE: Final = 64
_GAMMA_TINY: Final = 1e-280         # below this, log Q comes from the lower-tail limit
_UP_X_LO: Final = math.log(2.0 ** -53)   # smallest 1 − u for u < 1 in float64


# ---------------------------------------------------------------------------------------------- validation
def _uniform_array(u: F64, name: str) -> F64:
    arr = np.asarray(u, dtype=np.float64)
    if arr.size:
        lo, hi = arr.min(), arr.max()
        if not (lo >= 0.0 and hi < 1.0):     # NaN fails both comparisons
            raise SchemaError(f"{name}: uniforms must lie in [0, 1) (min {lo}, max {hi})")
    return arr


def _positive(x: float, name: str) -> float:
    v = float(x)
    if not (math.isfinite(v) and v > 0):
        raise SchemaError(f"{name} must be positive and finite, got {x!r}")
    return v


def _flat(arr: F64) -> F64:
    return np.ascontiguousarray(arr.reshape(-1))


# ---------------------------------------------------------------------------------------------- tables
@dataclass(frozen=True)
class _Hermite:
    """Cubic Hermite interpolation of a function on a uniform grid x0 + i·h (read-only arrays)."""

    x0: float
    inv_h: float
    h: float
    values: F64
    derivs: F64


def _freeze(a: F64) -> F64:
    out = np.ascontiguousarray(a, dtype=np.float64)
    out.flags.writeable = False
    return out


def _hermite_mid(values: F64, derivs: F64, h: float) -> F64:
    return 0.5 * (values[:-1] + values[1:]) + 0.125 * h * (derivs[:-1] - derivs[1:])


def _build_table(x_lo: float, x_hi: float, nodes: Callable[[F64], tuple[F64, F64]],
                 error_at: Callable[[F64, F64], float], what: str) -> _Hermite:
    """Double the grid until the Hermite value at every cell mid-point is within TABLE_TOL of the exact one."""
    n = _TABLE_N0
    while True:
        x = np.linspace(x_lo, x_hi, n)
        values, derivs = nodes(x)
        h = (x_hi - x_lo) / (n - 1)
        err = error_at(0.5 * (x[:-1] + x[1:]), _hermite_mid(values, derivs, h))
        if err <= TABLE_TOL:
            return _Hermite(float(x_lo), 1.0 / h, float(h), _freeze(values), _freeze(derivs))
        if n >= _TABLE_N_MAX:
            raise SolverError(f"{what}: inverse-CDF table did not reach {TABLE_TOL} with {n} nodes (error {err})",
                              {"nodes": n, "error": err})
        n = 2 * n - 1


@dataclass(frozen=True)
class _TTable:
    nu: float
    lower: _Hermite
    tail: bool
    log_u_split: float
    log_c: float          # log of the density constant Γ((ν+1)/2)/(√(νπ) Γ(ν/2))
    log_a: float          # log c + (ν+1)/2·log ν: prefactor of the tail expansion
    log_t0: float         # log c + (ν−1)/2·log ν: leading-order start of the tail Newton iteration
    betas: F64            # binom(−(ν+1)/2, k)/(ν + 2k)


def _t_log_c(nu: float) -> float:
    return math.lgamma(0.5 * (nu + 1.0)) - math.lgamma(0.5 * nu) - 0.5 * math.log(nu * math.pi)


def _t_tail_betas(nu: float) -> F64:
    a = 0.5 * (nu + 1.0)
    betas: list[float] = []
    b = 1.0
    for k in range(_T_TAIL_MAX_TERMS):
        beta = b / (nu + 2.0 * k)
        betas.append(beta)
        if k > 4 and abs(beta) * _T_TAIL_X_MAX ** k < _T_TAIL_TERM_TOL / nu:
            return np.asarray(betas)
        b *= -(a + k) / (k + 1.0)
    raise SolverError(f"student_t: tail expansion for df={nu} did not converge", {"df": nu})


@functools.lru_cache(maxsize=_TABLE_CACHE)
def _t_table(nu: float) -> _TTable:
    log_c = _t_log_c(nu)
    u_split = float(special.stdtr(nu, -math.sqrt(nu / _T_TAIL_X_MAX)))
    tail = u_split > U_MIN
    x_lo = math.log(u_split) if tail else math.log(U_MIN)

    def pdf(q: F64) -> F64:
        return np.exp(log_c - 0.5 * (nu + 1.0) * np.log1p(q * q / nu))

    def nodes(x: F64) -> tuple[F64, F64]:
        u = np.exp(x)
        u[-1] = 0.5
        q = special.stdtrit(nu, u)
        q[-1] = 0.0
        return q, u / pdf(q)

    def error_at(xm: F64, approx: F64) -> float:
        return float(np.max(np.abs(approx - special.stdtrit(nu, np.exp(xm)))))

    lower = _build_table(x_lo, _HALF_LOG, nodes, error_at, f"student_t(df={nu})")
    betas = _t_tail_betas(nu) if tail else np.zeros(1)      # large ν: the table reaches U_MIN, no tail needed
    return _TTable(nu=nu, lower=lower, tail=tail, log_u_split=x_lo, log_c=log_c,
                   log_a=log_c + 0.5 * (nu + 1.0) * math.log(nu), log_t0=log_c + 0.5 * (nu - 1.0) * math.log(nu),
                   betas=_freeze(betas))


@dataclass(frozen=True)
class _GammaTable:
    shape: float
    lower: _Hermite       # log Q over log u, u ≤ ½
    upper: _Hermite       # log Q over log(1 − u), u > ½


@functools.lru_cache(maxsize=_TABLE_CACHE)
def _gamma_table(a: float) -> _GammaTable:
    lg_a = math.lgamma(a)
    lg_a1 = math.lgamma(a + 1.0)

    def log_q_lower(x: F64) -> F64:
        q = special.gammaincinv(a, np.exp(x))
        out = (x + lg_a1) / a                       # lower-tail limit, exact to double precision where Q is tiny
        ok = q > _GAMMA_TINY
        out[ok] = np.log(q[ok])
        return out

    def lower_nodes(x: F64) -> tuple[F64, F64]:
        lq = log_q_lower(x)
        return lq, np.exp(x + lg_a - a * lq + np.exp(lq))

    def lower_error(xm: F64, approx: F64) -> float:
        return float(np.max(np.abs(np.exp(approx) - np.exp(log_q_lower(xm)))))

    def upper_nodes(x: F64) -> tuple[F64, F64]:
        lq = np.log(special.gammainccinv(a, np.exp(x)))
        return lq, -np.exp(x + lg_a - a * lq + np.exp(lq))

    def upper_error(xm: F64, approx: F64) -> float:
        return float(np.max(np.abs(np.exp(approx) - special.gammainccinv(a, np.exp(xm)))))

    what = f"gamma(shape={a})"
    return _GammaTable(shape=a, lower=_build_table(math.log(U_MIN), _HALF_LOG, lower_nodes, lower_error, what),
                       upper=_build_table(_UP_X_LO, _HALF_LOG, upper_nodes, upper_error, what))


# ---------------------------------------------------------------------------------------------- kernels
@inline_helper
def _hermite(x0, inv_h, h, values, derivs, x):  # type: ignore[no-untyped-def]
    s = (x - x0) * inv_h
    n = values.shape[0]
    i = int(s)
    if i < 0:
        i = 0
    elif i > n - 2:
        i = n - 2
    tau = s - i
    t2 = tau * tau
    t3 = t2 * tau
    return ((2.0 * t3 - 3.0 * t2 + 1.0) * values[i] + (t3 - 2.0 * t2 + tau) * h * derivs[i]
            + (3.0 * t2 - 2.0 * t3) * values[i + 1] + (t3 - t2) * h * derivs[i + 1])


@inline_helper
def _t_tail(log_p, nu, log_a, log_c, log_t0, betas):  # type: ignore[no-untyped-def]
    """t > 0 with F(−t) = p, by Newton in log t on the tail expansion of log F (relative accuracy ≈ 5e-15)."""
    t = math.exp((log_t0 - log_p) / nu)
    t_floor = math.sqrt(nu / 0.9)          # keeps ν/t² inside the expansion's convergence disc during Newton
    for _ in range(_T_NEWTON_MAX):
        if t < t_floor:
            t = t_floor
        x = nu / (t * t)
        s = 0.0
        for k in range(betas.shape[0] - 1, -1, -1):
            s = s * x + betas[k]
        log_g = log_a - nu * math.log(t) + math.log(s)
        log_f = log_c - 0.5 * (nu + 1.0) * math.log1p(t * t / nu)
        step = (log_g - log_p) / (t * math.exp(log_f - log_g))
        t = t * math.exp(step)
        if abs(step) < _T_NEWTON_TOL:
            break
    return t


@kernel()
def _t_kernel(u, out, x0, inv_h, h, values, derivs, tail, log_u_split, nu, log_a, log_c, log_t0, betas,
              scale):  # type: ignore[no-untyped-def]
    for i in range(u.shape[0]):
        ui = u[i]
        upper = ui > 0.5
        p = 1.0 - ui if upper else ui
        if p < U_MIN:
            p = U_MIN
        lp = math.log(p)
        if tail and lp < log_u_split:
            q = -_t_tail(lp, nu, log_a, log_c, log_t0, betas)
        else:
            q = _hermite(x0, inv_h, h, values, derivs, lp)
        out[i] = (-q if upper else q) * scale


@kernel()
def _gamma_kernel(u, out, lx0, linv_h, lh, lvalues, lderivs, ux0, uinv_h, uh, uvalues, uderivs,
                  scale):  # type: ignore[no-untyped-def]
    for i in range(u.shape[0]):
        ui = u[i]
        if ui <= 0.5:
            p = ui if ui > U_MIN else U_MIN
            lq = _hermite(lx0, linv_h, lh, lvalues, lderivs, math.log(p))
        else:
            lq = _hermite(ux0, uinv_h, uh, uvalues, uderivs, math.log(1.0 - ui))
        out[i] = math.exp(lq) * scale


def _run_t(arr: F64, nu: float, scale: float) -> F64:
    tab = _t_table(nu)
    lo = tab.lower
    flat = _flat(arr)
    out = np.empty(flat.shape[0], dtype=np.float64)
    _t_kernel(flat, out, lo.x0, lo.inv_h, lo.h, lo.values, lo.derivs, tab.tail, tab.log_u_split, tab.nu, tab.log_a,
              tab.log_c, tab.log_t0, tab.betas, float(scale))
    return out.reshape(arr.shape)


# ---------------------------------------------------------------------------------------------- samplers
def normal(u: F64) -> F64:
    """Standard normal variates Φ⁻¹(u) (``scipy.special.ndtri``)."""
    arr = _uniform_array(u, "normal")
    return special.ndtri(np.maximum(arr, U_MIN))


def _check_df(df: float, standardize: bool) -> float:
    nu = _positive(df, "df")
    if standardize and not nu > 2.0:
        raise SchemaError(f"standardize needs df > 2 (finite variance), got df={nu}")
    return nu


def student_t(u: F64, df: float, *, standardize: bool = True) -> F64:
    """Student t variates with ``df`` degrees of freedom from a tabulated inverse CDF (abs error < 1e-7).

    ``standardize=True`` (default) returns √((ν − 2)/ν)·t, unit variance (engine E's ε, §4.10; S-ADR-35).
    """
    arr = _uniform_array(u, "student_t")
    nu = _check_df(df, standardize)
    return _run_t(arr, nu, math.sqrt((nu - 2.0) / nu) if standardize else 1.0)


def truncated_t(u: F64, df: float, lo: float, hi: float, *, standardize: bool = False) -> F64:
    """Student t variates conditioned on [lo, hi]: Q(F(lo) + u·(F(hi) − F(lo))), clipped to the bounds.

    ``lo``/``hi`` may be infinite. With ``standardize=True`` the bounds and the result are on the unit-variance
    scale √((ν − 2)/ν)·t. Bounds in the upper half are handled by symmetry, so tail intervals keep full precision.
    """
    arr = _uniform_array(u, "truncated_t")
    nu = _check_df(df, standardize)
    s = math.sqrt((nu - 2.0) / nu) if standardize else 1.0
    a, b = float(lo) / s, float(hi) / s
    if math.isnan(a) or math.isnan(b) or not a < b:
        raise SchemaError(f"truncated_t: need lo < hi, got lo={lo}, hi={hi}")
    flip = a >= 0.0
    if flip:                                  # X on [a, b] is −Y with Y on [−b, −a]; Q_X(u) = −Q_Y(1 − u)
        f_lo, f_hi = float(special.stdtr(nu, -b)), float(special.stdtr(nu, -a))
        mapped = f_hi - arr * (f_hi - f_lo)
    else:
        f_lo, f_hi = float(special.stdtr(nu, a)), float(special.stdtr(nu, b))
        mapped = f_lo + arr * (f_hi - f_lo)
    if not f_hi > f_lo:
        raise SchemaError(f"truncated_t: no probability mass in [{lo}, {hi}] at df={nu}")
    q = _run_t(np.clip(mapped, 0.0, 1.0), nu, s)
    return np.clip(-q if flip else q, float(lo), float(hi))


def gamma(u: F64, shape: float, scale: float = 1.0) -> F64:
    """Gamma(shape, scale) variates from tabulated inverse CDFs (abs error < 1e-7 on the unit-scale quantile)."""
    arr = _uniform_array(u, "gamma")
    a = _positive(shape, "shape")
    sc = _positive(scale, "scale")
    tab = _gamma_table(a)
    lo, up = tab.lower, tab.upper
    flat = _flat(arr)
    out = np.empty(flat.shape[0], dtype=np.float64)
    _gamma_kernel(flat, out, lo.x0, lo.inv_h, lo.h, lo.values, lo.derivs, up.x0, up.inv_h, up.h, up.values,
                  up.derivs, sc)
    return out.reshape(arr.shape)


def exponential(u: F64, rate: F64) -> F64:
    """Exponential variates −log(1 − u)/rate. Units: ``rate`` per period of the producing clock."""
    arr = _uniform_array(u, "exponential")
    r = np.asarray(rate, dtype=np.float64)
    if not np.isfinite(r).all() or (r <= 0).any():
        raise SchemaError("exponential: rate must be positive and finite")
    return -np.log1p(-arr) / r


def bernoulli(u: F64, p: F64) -> B:
    """Bernoulli variates u < p (``p`` broadcasts against ``u``)."""
    arr = _uniform_array(u, "bernoulli")
    pr = np.asarray(p, dtype=np.float64)
    if not np.isfinite(pr).all() or (pr < 0).any() or (pr > 1).any():
        raise SchemaError("bernoulli: p must lie in [0, 1]")
    return np.asarray(arr < pr)


def categorical(u: F64, cum_probs: F64) -> I8:
    """Category index #{k: cum_probs[..., k] ≤ u}; ``cum_probs`` [..., K] non-decreasing with last entry 1, K ≤ 127.

    A 1-d ``cum_probs`` is shared by every variate; otherwise its leading axes broadcast against ``u``.
    """
    arr = _uniform_array(u, "categorical")
    c = np.asarray(cum_probs, dtype=np.float64)
    if c.ndim < 1 or not 1 <= c.shape[-1] <= np.iinfo(np.int8).max:
        raise SchemaError(f"categorical: cum_probs must have 1..127 categories on its last axis, got {c.shape}")
    if not np.isfinite(c).all() or (c < 0).any() or (np.diff(c, axis=-1) < 0).any():
        raise SchemaError("categorical: cum_probs must be finite, non-negative and non-decreasing")
    if (np.abs(c[..., -1] - 1.0) > 1e-9).any():
        raise SchemaError("categorical: the last cumulative probability must be 1")
    k = c.shape[-1]
    idx = np.searchsorted(c, arr, side="right") if c.ndim == 1 else (arr[..., None] >= c).sum(axis=-1)
    return np.minimum(idx, k - 1).astype(np.int8)


def kou_jump(u_occ: F64, u_size: F64, u_sign: F64, lam: float, eta_up: float, eta_dn: float, p_up: float) -> F64:
    """Kou double-exponential log jump for one period (0 when no jump): three uniforms per variate.

    A jump occurs with probability 1 − e^{−λ} (``u_occ``); it is up with probability ``p_up`` (``u_sign``), of size
    Exp(η_up) if up and −Exp(η_dn) if down (``u_size``), so up and down jumps have means 1/η_up and −1/η_dn. At most
    one jump per period (monthly steps keep λ small). Units: ``lam`` jumps per period; η per unit log return.
    """
    occ = _uniform_array(u_occ, "kou_jump u_occ")
    size = _uniform_array(u_size, "kou_jump u_size")
    sign = _uniform_array(u_sign, "kou_jump u_sign")
    lam_ = float(lam)
    if not (math.isfinite(lam_) and lam_ >= 0):
        raise SchemaError(f"kou_jump: lam must be >= 0, got {lam}")
    up, dn = _positive(eta_up, "eta_up"), _positive(eta_dn, "eta_dn")
    pu = float(p_up)
    if not 0.0 <= pu <= 1.0:
        raise SchemaError(f"kou_jump: p_up must lie in [0, 1], got {p_up}")
    occ, size, sign = np.broadcast_arrays(occ, size, sign)
    e = -np.log1p(-size)
    jump = np.where(sign < pu, e / up, -e / dn)
    return np.where(occ < -math.expm1(-lam_), jump, 0.0)


def warm_samplers() -> None:
    """Compile (or load from the numba cache) the sampler kernels for writable and read-only inputs (§1.13)."""
    u = np.array([0.0, 0.25, 0.5, 0.75], dtype=np.float64)
    ro = u.copy()
    ro.flags.writeable = False
    for arr in (u, ro):
        student_t(arr, 5.0)
        gamma(arr, 2.0)
