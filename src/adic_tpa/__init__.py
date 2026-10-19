"""ADIC Agentic Total-Portfolio Laboratory (BUILD_SPEC v1.1 §1.1, §2; owner WP-01).

SYNTHETIC – NOT ADIC DATA. The package root holds only constants and imports nothing, so importing any
subpackage stays cheap and every layer may read these names (tests/layering treats ``adic_tpa`` itself as
importable from everywhere).
"""

from __future__ import annotations

from typing import Final

__all__ = ["SYNTHETIC_FOOTER", "__version__"]

__version__: Final = "0.1.0"

# §1.12 rule 3: every chart, table, page, JSON artifact and CLI summary built from a SYNTHETIC run carries it.
SYNTHETIC_FOOTER: Final = "SYNTHETIC – NOT ADIC DATA"
