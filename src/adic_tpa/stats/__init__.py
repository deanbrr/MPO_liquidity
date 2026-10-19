"""Statistics for certification, gates and deflation (BUILD_SPEC v1.1 §4.4; owner WP-02, wave 0).

Clopper–Pearson bounds (``cp``), the paired bootstrap (``bootstrap``), Holm and α-investing (``multiple``), the
maximum of null statistics, DSR and the deflated improvement (``dsr``), PBO by CSCV (``pbo``), the minimum detectable
effect (``mde``), CVaR and bPOE (``bpoe``) and the certainty-equivalent conversions (``ce``). ``stats`` imports only
``contracts`` and ``numerics`` (§4.0).

SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

from adic_tpa.stats.bootstrap import BootstrapResult, paired_bootstrap
from adic_tpa.stats.bpoe import bpoe, cvar
from adic_tpa.stats.ce import delta_ce_bp, h_delta_ce_bp, j_to_ce_wealth, sure_objective, usd_m_per_bp_year
from adic_tpa.stats.cp import clopper_pearson, is_cp_upper
from adic_tpa.stats.dsr import deflated_improvement, deflated_sharpe, expected_max_z, max_z_quantile
from adic_tpa.stats.mde import mde
from adic_tpa.stats.multiple import AlphaInvesting, holm
from adic_tpa.stats.pbo import pbo_cscv

__all__ = [
    "clopper_pearson", "is_cp_upper", "BootstrapResult", "paired_bootstrap", "holm", "AlphaInvesting",
    "expected_max_z", "max_z_quantile", "deflated_sharpe", "deflated_improvement", "pbo_cscv", "mde",
    "cvar", "bpoe", "j_to_ce_wealth", "sure_objective", "delta_ce_bp", "h_delta_ce_bp", "usd_m_per_bp_year",
]
