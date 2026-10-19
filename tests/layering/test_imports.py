"""Import table (BUILD_SPEC v1.1 §4.0; owner WP-01).

Every ``adic_tpa`` import must be listed for the importing layer (all imports count, function-level and
``TYPE_CHECKING`` ones included); engine modules never import the agent layer or networking modules; the asset
engines never import ``beliefs``. Modules of later WPs are checked automatically as they land.
"""

from __future__ import annotations

from types import SimpleNamespace


def test_every_package_has_a_layer(layer_rules: SimpleNamespace) -> None:
    unknown = sorted({layer_rules.layer_of(layer_rules.module_name(p)) for p in layer_rules.package_files()}
                     - set(layer_rules.IMPORT_TABLE) - {"__root__"})
    assert not unknown, f"modules outside the §4.0 import table: {unknown}"


def test_internal_imports_follow_the_table(import_records: list, layer_rules: SimpleNamespace) -> None:
    violations = [f"{r.where()}: {r.module} imports {r.target}" for r in import_records
                  if r.top == "adic_tpa" and not layer_rules.is_allowed(r.module, r.target)]
    assert not violations, "layering violations (§4.0):\n" + "\n".join(violations)


def test_engine_modules_never_import_networking(import_records: list, layer_rules: SimpleNamespace) -> None:
    violations = [f"{r.where()}: {r.module} imports {r.target}" for r in import_records
                  if layer_rules.layer_of(r.module) in layer_rules.ENGINE_LAYERS and r.top in layer_rules.NETWORK_MODULES]
    assert not violations, "engine modules import networking modules:\n" + "\n".join(violations)


def test_engine_modules_never_import_the_agent_layer(import_records: list, layer_rules: SimpleNamespace) -> None:
    violations = [f"{r.where()}: {r.module} imports {r.target}" for r in import_records
                  if r.top == "adic_tpa" and layer_rules.layer_of(r.module) in layer_rules.ENGINE_LAYERS
                  and layer_rules.layer_of(r.target) in layer_rules.FORBIDDEN_FOR_ENGINES]
    assert not violations, "engine modules import the agent layer:\n" + "\n".join(violations)


def test_asset_engines_never_import_beliefs(import_records: list, layer_rules: SimpleNamespace) -> None:
    violations = [f"{r.where()}: {r.module} imports {r.target}" for r in import_records
                  if layer_rules.layer_of(r.module) in {"priv", "pub", "overlay"} and r.top == "adic_tpa"
                  and layer_rules.layer_of(r.target) == "beliefs"]
    assert not violations, "belief draws arrive through AssetEngine.init (S-ADR-28):\n" + "\n".join(violations)


def test_harness_flags_a_planted_violation(tmp_path, layer_rules: SimpleNamespace) -> None:
    """The checker itself works: a planted contracts module importing ledger and socket is caught."""
    planted = tmp_path / "zz_planted.py"
    planted.write_text("from __future__ import annotations\nimport socket\n"
                       "def f():\n    from adic_tpa.ledger import kernel\n    from . import ids\n", encoding="utf-8")
    records = layer_rules.parse_imports(planted, module="adic_tpa.contracts.zz_planted")
    targets = {r.target for r in records}
    assert targets == {"socket", "adic_tpa.ledger", "adic_tpa.contracts.ids"}
    bad = [r for r in records if r.top == "adic_tpa" and not layer_rules.is_allowed(r.module, r.target)]
    assert [r.target for r in bad] == ["adic_tpa.ledger"]
    assert any(r.top in layer_rules.NETWORK_MODULES for r in records)
    assert not layer_rules.is_allowed("adic_tpa.contracts.book", "adic_tpa.ledger.kernel")
    assert layer_rules.is_allowed("adic_tpa.contracts.book", "adic_tpa.contracts.taxonomy")
    assert layer_rules.is_allowed("adic_tpa.core.h", "adic_tpa.core.observables")          # core.h -> core.sim
    assert not layer_rules.is_allowed("adic_tpa.core.sim", "adic_tpa.core.h")
    assert layer_rules.is_allowed("adic_tpa.evaluator.service", "adic_tpa.core.mpc")       # core.*
    assert layer_rules.is_allowed("adic_tpa.lab.fsm", "adic_tpa.evaluator.client")
    assert not layer_rules.is_allowed("adic_tpa.lab.fsm", "adic_tpa.evaluator.service")
    assert layer_rules.is_allowed("adic_tpa.seal.runner", "adic_tpa.evaluator.service")    # runner override
    assert not layer_rules.is_allowed("adic_tpa.seal.commit", "adic_tpa.evaluator.service")
    assert layer_rules.is_allowed("adic_tpa.attrib.prices", "adic_tpa.core.irb")           # attrib (+ core.irb)
    assert layer_rules.is_allowed("adic_tpa.cli", "adic_tpa.pipeline.quarter")
    assert layer_rules.is_allowed("adic_tpa.rng.keys", "adic_tpa")                          # package root
