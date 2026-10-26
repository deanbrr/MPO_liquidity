"""ADIC Total Portfolio Platform (TPP): the multi-stakeholder demo engine.

One book, one scenario engine and one optimizer serve four stakeholder lenses (Strategy, Balance Sheet, Liquidity,
Asset Allocation) and the IC comparison. Built on the MPO v2 prototype in examples/mpo_v2 (regime generator,
private-market cash-flow engine, bPOE / GBO objective, CVaR rows, statistics), with the prototype's synthetic
three-mark fusion replaced by the Return Preference Engine (tpp.returns) fed by the user's ER strategy returns and
fund-level underwritten / actual returns.

Labels used throughout: DATA (read from the user's files), ASSUMPTION (a configurable default in
config/assumptions.json, with unit, rationale and source), DERIVED (computed from the two).
"""

__version__ = "0.1.0"
