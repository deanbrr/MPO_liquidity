"""Never collect anything under ``tests/regression/fixtures`` (BUILD_SPEC v1.1 §10.4; owner WP-03).

The directory holds read-only copies of research files ported by ``tools/port_research.py``, including the
research's own pytest suites (``test_no_pinned_duals.py``, ``test_no_pinned_duals_groups.py``) that import research
modules. They are fixtures, not tests: the ports that run production code on them live in ``tests/regression/``.
"""

collect_ignore_glob = ["*"]
