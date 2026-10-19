"""Suite-wide pytest hooks (owner WP-03): the golden-update path of BUILD_SPEC v1.1 §10.4.

``pytest --update-golden`` rewrites the WP-03 golden files instead of comparing against them. Updating a golden
needs a contract-change note naming the reason and review by the module owner and MRM (§10.4).
"""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--update-golden", action="store_true", default=False,
                     help="rewrite golden files (BUILD_SPEC §10.4: needs a contract-change note)")


@pytest.fixture(scope="session")
def update_golden(request: pytest.FixtureRequest) -> bool:
    """True when the run was started with ``--update-golden``."""
    return bool(request.config.getoption("--update-golden"))
