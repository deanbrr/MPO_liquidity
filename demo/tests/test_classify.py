"""The classifier: rule file integrity, the ER catalog, overrides, and known mappings.

The rule file and the known-mapping cases name managers and holdings from the fund file, so both stay out of git
(config/classifier_rules.json, data/classifier_cases.json); the tests that need them skip where they are absent."""
import json
import re
from pathlib import Path

import pytest

from tpp.buckets import BY_KEY, CATALOG
from tpp.classify import CONFIG, Classifier

RULES = CONFIG / "classifier_rules.json"
CASES = Path(__file__).resolve().parents[1] / "data" / "classifier_cases.json"
needs_rules = pytest.mark.skipif(not RULES.exists(), reason="config/classifier_rules.json is local (git-ignored)")
_cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"] if CASES.exists() else []


def test_every_bucket_is_an_er_row():
    assert len(CATALOG) == 29
    for b in CATALOG:
        assert BY_KEY[b.er_key] is b


@needs_rules
def test_rule_patterns_compile_and_carry_no_control_characters():
    spec = json.loads(RULES.read_text(encoding="utf-8"))
    for r in spec["rules"]:
        pat = r.get("pattern")
        if pat:
            assert not any(ord(ch) < 32 for ch in pat), r["id"]          # a JSON "\b" would be a backspace
            re.compile(pat, re.I)
    assert "pattern" not in spec["rules"][-1] and "classes" not in spec["rules"][-1], "the list must end with a catch-all"


@needs_rules
def test_override_file_wins(tmp_path):
    ov = tmp_path / "ov.csv"
    ov.write_text("FUND_CODE,department,vertical,vehicle,comment\nAA1,Real Estate,Global RE,Fund,test\n", encoding="utf-8")
    out = Classifier(overrides_path=ov).classify_row("AA1", "Example Buyout Fund VIII", "Closed ended Fund", "Primary")
    assert out["bucket"] == "RE_F" and out["rule"] == "OVERRIDE"


@needs_rules
@pytest.mark.skipif(not _cases, reason="data/classifier_cases.json is local (git-ignored)")
@pytest.mark.parametrize("case", _cases, ids=lambda c: c["bucket"])
def test_known_mappings(case):
    out = Classifier().classify_row("X", case["name"], case["class"], case["style"])
    assert out["bucket"] == case["bucket"], (case, out)
    if case.get("proxy"):
        assert out["proxy"] and out["confidence"] == "low"
