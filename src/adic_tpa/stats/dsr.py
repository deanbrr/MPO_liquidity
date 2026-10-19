"""Deflation for search: the maximum of N null statistics, DSR and the deflated improvement (BUILD_SPEC v1.1 §4.4,
§7.7; ARCH §7.7; BUILD-20).

Two different functionals of M_N = max of N i.i.d. N(0, 1) are needed (BUILD-20):

- ``expected_max_z(N)`` = E[M_N] = ∫ x·N φ(x) Φ(x)^{N−1} dx, by quadrature (2.746 at N = 200; the Bailey–López de
  Prado closed-form approximation gives 2.766). It sets DSR's benchmark Sharpe ratio SR₀.
- ``max_z_quantile(N, q)`` = Φ⁻¹(q^{1/N}), the q-quantile of M_N (3.474 at N = 200, q = 0.95): the hurdle of the
  deflated improvement ΔΨ̂ − SE·q₀.₉₅(M_{N_eff}).

``deflated_sharpe`` is Bailey & López de Prado's (2014) DSR = PSR(SR₀) =
Φ((SR̂ − SR₀)·√(T − 1)/√(1 − γ₃·SR̂ + (γ₄ − 1)/4·SR̂²)), with SR̂ and SR₀ per observation period, γ₃ the skewness and
γ₄ the (non-excess) kurtosis (3 for normal returns). SR₀ = √V·E[M_{N_eff}], where V is the variance of the trials'
Sharpe estimates; the §4.4 signature carries no such input, so by default V = 1/(T − 1), the variance of the
estimator under the null SR = 0 (WP-02 choice); ``sr_trials_var`` overrides it.
"""

from __future__ import annotations

import functools
import math

from scipy import integrate, special

from adic_tpa.contracts.errors import SchemaError, SolverError

__all__ = ["expected_max_z", "max_z_quantile", "deflated_sharpe", "deflated_improvement"]


def _check_n(n_eff: int, name: str) -> int:
    if isinstance(n_eff, bool) or int(n_eff) != n_eff or n_eff < 1:
        raise SchemaError(f"{name}: n_eff must be an integer >= 1, got {n_eff!r}")
    return int(n_eff)


@functools.lru_cache(maxsize=1024)
def _expected_max(n: int) -> float:
    if n == 1:
        return 0.0
    log_n = math.log(n)

    def density_times_x(x: float) -> float:
        return x * math.exp(log_n - 0.5 * x * x - 0.5 * math.log(2.0 * math.pi) + (n - 1) * special.log_ndtr(x))

    mode = float(-special.ndtri(1.0 / n))           # ≈ location of the maximum's density peak
    value, abserr = integrate.quad(density_times_x, -12.0, 40.0, points=[mode], limit=500, epsabs=1e-13,
                                   epsrel=1e-12)
    if not abserr < 1e-9:
        raise SolverError(f"expected_max_z: quadrature error {abserr} at n={n}", {"n": n})
    return float(value)


def expected_max_z(n_eff: int) -> float:
    """E[max of n_eff i.i.d. N(0, 1)] (2.746 at 200); 0 for a single trial."""
    return _expected_max(_check_n(n_eff, "expected_max_z"))


def max_z_quantile(n_eff: int, q: float = 0.95) -> float:
    """q-quantile of the maximum of n_eff i.i.d. N(0, 1): Φ⁻¹(q^{1/n_eff}) (3.474 at 200, q = 0.95)."""
    n = _check_n(n_eff, "max_z_quantile")
    if not 0.0 < q < 1.0:
        raise SchemaError(f"max_z_quantile: q must lie in (0, 1), got {q}")
    tail = -math.expm1(math.log(q) / n)             # 1 − q^{1/n}, without cancellation
    return float(-special.ndtri(tail))


def deflated_sharpe(sr: float, n_eff: int, t_obs: int, skew: float, kurt: float, *,
                    sr_trials_var: float | None = None) -> float:
    """Deflated Sharpe ratio (probability that the true SR exceeds the expected maximum of n_eff null trials).

    ``sr``: Sharpe ratio per observation period (not annualized); ``t_obs``: number of observations; ``skew``,
    ``kurt``: skewness and non-excess kurtosis of the returns; ``sr_trials_var``: variance of the trials' Sharpe
    estimates (default 1/(t_obs − 1), module docstring).
    """
    n = _check_n(n_eff, "deflated_sharpe")
    if isinstance(t_obs, bool) or int(t_obs) != t_obs or t_obs < 2:
        raise SchemaError(f"deflated_sharpe: t_obs must be an integer >= 2, got {t_obs!r}")
    if not all(math.isfinite(v) for v in (sr, skew, kurt)):
        raise SchemaError("deflated_sharpe: sr, skew and kurt must be finite")
    var = 1.0 / (t_obs - 1) if sr_trials_var is None else float(sr_trials_var)
    if not (math.isfinite(var) and var >= 0):
        raise SchemaError(f"deflated_sharpe: sr_trials_var must be >= 0, got {sr_trials_var}")
    denom = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr * sr
    if not denom > 0:
        raise SchemaError(f"deflated_sharpe: non-positive variance term {denom} (check skew and kurtosis)")
    sr0 = math.sqrt(var) * expected_max_z(n)
    return float(special.ndtr((sr - sr0) * math.sqrt(t_obs - 1.0) / math.sqrt(denom)))


def deflated_improvement(delta_psi: float, se: float, n_eff: int, q: float = 0.95) -> float:
    """ΔΨ̂ − SE·max_z_quantile(n_eff, q): the search improvement net of the null maximum's q-quantile (CE bp a year
    when ΔΨ̂ and SE are; §7.7)."""
    if not (math.isfinite(delta_psi) and math.isfinite(se) and se >= 0):
        raise SchemaError(f"deflated_improvement: need finite delta_psi and se >= 0, got {delta_psi}, {se}")
    return float(delta_psi - se * max_z_quantile(n_eff, q))
