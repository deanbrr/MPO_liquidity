"""Hash stability across processes and PYTHONHASHSEED values (BUILD_SPEC v1.1 §4.1 invariant, §10.5). Owner WP-01.

The golden hashes of tests/unit/test_hashing.py pin the values; this test shows a child interpreter with another
hash seed reproduces them, set ordering included.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from adic_tpa.contracts.hashing import content_hash

UNIT_DIR = Path(__file__).resolve().parents[1] / "unit"
CODE = ("import sys; sys.path.insert(0, sys.argv[1]); from adic_tpa.contracts.hashing import content_hash; "
        "from test_hashing import golden_objects; "
        "print([content_hash(o) for _, o in golden_objects()] + [content_hash({'x', 'y', 'z', 'w'})])")


def _golden_objects() -> list[tuple[str, object]]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("_golden_hashing", UNIT_DIR / "test_hashing.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.golden_objects()


def test_hash_stable_across_processes_and_hash_seeds() -> None:
    seed = "12345" if os.environ.get("PYTHONHASHSEED") != "12345" else "54321"
    out = subprocess.run([sys.executable, "-c", CODE, str(UNIT_DIR)], capture_output=True, text=True,
                         env={**os.environ, "PYTHONHASHSEED": seed}, timeout=60, check=True)
    here = [content_hash(o) for _, o in _golden_objects()] + [content_hash({"x", "y", "z", "w"})]
    assert out.stdout.strip() == str(here)
