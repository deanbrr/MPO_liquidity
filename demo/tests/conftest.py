"""Test setup for the stakeholder demo. Tests that need the user's (MSIP-labelled, git-ignored) workbooks skip
when demo/data does not hold them, so the suite runs anywhere; the engine tests run on the real book locally."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

DEMO = Path(__file__).resolve().parents[1]
if str(DEMO) not in sys.path:
    sys.path.insert(0, str(DEMO))

DATA = DEMO / "data"
FUND = DATA / "fund_returns.xlsx"
ER = DATA / "er_strategy_returns.xlsx"
HAVE_DATA = FUND.exists() and ER.exists()
needs_data = pytest.mark.skipif(not HAVE_DATA, reason="the user's workbooks are not in demo/data")


@pytest.fixture(scope="session")
def P():
    from tpp.legacy import demo_params
    return demo_params()


@pytest.fixture(scope="session")
def er():
    from tpp import ingest
    return ingest.load_er(ER)


@pytest.fixture(scope="session")
def platform(tmp_path_factory):
    from tpp import service
    return service.Platform(state_dir=tmp_path_factory.mktemp("state"), quick=True)
