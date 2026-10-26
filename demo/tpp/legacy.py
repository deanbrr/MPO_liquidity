"""Bridge to the MPO v2 prototype (examples/mpo_v2): the parts of the code base the demo reuses as they are.

Reused unchanged:
  common.Params                    nested {value, unit, rationale, source} parameter files with usage tracking
  common.cvar_lower, quantile_w, wilson, clopper_pearson_upper   exact weighted statistics
  scenarios.Generator              quarterly regime-switching factor generator (macro, exit window, oil) and the
                                   oil-linked owner draw
  scenarios.UnitEngine             full-position quarterly private-market engine (calls, distributions, NAV)
  scenarios.node_class             BEN / DRT / STR market-state classes
  optim.gbo_value, optim.bpoe      buffered probability of exceedance (the GBO objective's statistic)

The prototype's modules live in a plain folder, so it is appended to sys.path (appended, not prepended, so nothing
in the demo is shadowed). The demo's own modules are all inside the `tpp` package.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MPO = ROOT / "examples" / "mpo_v2"
DEMO = Path(__file__).resolve().parents[1]
if str(MPO) not in sys.path:
    sys.path.append(str(MPO))

from common import Params, clopper_pearson_upper, cvar_lower, quantile_w, wilson  # noqa: E402
from optim import bpoe, gbo_value  # noqa: E402
from scenarios import Generator, UnitEngine, node_class  # noqa: E402

__all__ = ["Params", "clopper_pearson_upper", "cvar_lower", "quantile_w", "wilson", "bpoe", "gbo_value",
           "Generator", "UnitEngine", "node_class", "mpo_params", "demo_params", "segment", "MPO", "DEMO", "ROOT"]

# Prototype finding (README section 2.4, verify_finance): the crisis equity-yield shock correlation of -0.30 makes
# bonds fall with equities in crises, "probably a sign error". The demo restores flight to quality by default; the
# 2022-style stress (stocks and bonds falling together) sets it back.
CRISIS_EQ_YIELD_CORR = 0.30


def mpo_params(overrides: dict | None = None) -> Params:
    """The prototype's params.json (regimes, factors, owner draw, segments) with demo overrides.
    Worlds are neutralized to one: the ER Downside / Base / Upside worlds are applied per bucket by tpp.paths."""
    P = Params(MPO / "params.json")
    w_eq = float(np.mean(P._leaf("worlds.eq_log_excess")["value"]))
    w_tp = float(np.mean(P._leaf("worlds.term_premium")["value"]))
    corr = [list(r) for r in P._leaf("factors.corr_crisis")["value"]]
    corr[0][2] = corr[2][0] = CRISIS_EQ_YIELD_CORR
    base = {
        "worlds.names": ["N"], "worlds.weights": [1.0], "worlds.eq_log_excess": [w_eq],
        "worlds.credit_drift": [0.0], "worlds.term_premium": [w_tp],
        "factors.corr_crisis": corr,
    }
    base.update(overrides or {})
    P.overrides.update(base)
    return P


def demo_params(path: Path | None = None, overrides: dict | None = None) -> Params:
    P = Params(path or DEMO / "config" / "assumptions.json")
    if overrides:
        P.overrides.update(overrides)
    return P


def segment(P: Params, name: str) -> dict:
    """A prototype segment (cash-flow intensities, factor loadings, bid key) as a plain dict."""
    return json.loads(json.dumps(P._leaf(f"book.segments.{name}")["value"]))
