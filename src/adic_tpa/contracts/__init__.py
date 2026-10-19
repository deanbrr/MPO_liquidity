"""The frozen vocabulary of the lab (BUILD_SPEC v1.1 §3, §4.1; owner WP-01).

Models, enums, ids, units, calendar, hashing, signing, the taxonomy registry, errors, config loading, array specs,
shared rules and the Protocols. ``contracts`` imports no other ``adic_tpa`` package (§4.0); import names from the
submodules, e.g. ``from adic_tpa.contracts.book import BookSnapshot``.

Submodules: ``ids enums units calendar hashing errors config logjson signing taxonomy arrays book marks overlay
world engine_io ledger beliefs rules policy optimizer actions contract evidence lab claims room tools ports
analyst``.

SYNTHETIC – NOT ADIC DATA.
"""

from __future__ import annotations

from typing import Final

from adic_tpa import SYNTHETIC_FOOTER

__all__ = ["SYNTHETIC_FOOTER", "CONTRACTS_VERSION"]

# The tag this vocabulary freezes under (contracts-v1.0; tagged only after the WP-03 walking skeleton is green).
CONTRACTS_VERSION: Final = "1.0"
