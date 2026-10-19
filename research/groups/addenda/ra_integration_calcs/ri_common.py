"""
ri_common: shared definitions for the Real Assets integration re-run (ra_integration_calcs).

SYNTHETIC - NOT ADIC DATA. Every balance, rate and outcome produced by the ri_* scripts comes from the working
allocation (context s1A, v1 and v2), the census of record and design defaults [I]. Nothing is ADIC data.

Books compared (all SYNTHETIC; private NAV stays $106bn in every book):
  v1pub   seven groups AS PUBLISHED: PE 52 / unfunded 27.4 (gap_02 split for T4', census v1.0 split for the cash
          map) - reproduction anchor only
  v1      seven groups on the census the user chose (context s1A, 2026-10-18): PE 52 / 16.4 (census v1.1, sealed
          vintage profile); non-PE unfunded census v1.0 split (unchanged in v1.1): total unfunded 27.0
          (ra_book book key 'v1s')
  v2u16   eight groups, allocation v2: PE 34 / 16.4 (the user's figure kept on the smaller bucket) + Real Assets
          18 / 4.0 (ten census sleeves); total unfunded 31.0
  v2u11   eight groups: PE 34 / 10.9 (census v1.1 U/NAV 0.32 rescaled to the v2 bucket) + Real Assets 18 / 4.0;
          total unfunded 25.5
"""
from __future__ import annotations

import hashlib
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "SYNTHETIC - NOT ADIC DATA"
SEED = 20261018

BOOKS = {
    "v1pub": dict(rb_book="v1", census="gap02", label="v1 as published (7 groups; PE 52/27.4; gap_02 split)"),
    "v1": dict(rb_book="v1s", census="v1", label="v1 on census v1.1 (7 groups; PE 52/16.4)"),
    "v2u16": dict(rb_book="v2u16", census="v1", label="v2 U16 (8 groups; PE 34/16.4 + RA 18/4.0)"),
    "v2u11": dict(rb_book="v2u11", census="v1", label="v2 U11 (8 groups; PE 34/10.9 + RA 18/4.0)"),
}
MAIN_BOOKS = ("v1", "v2u16", "v2u11")

# published theta* anchors (gap_02 / groups gap_01 for v1pub; ra_gap_01 for v2); the ri_calib stage recomputes
# all four with the same rule and engine, and downstream stages read ri_calib_results.json when present
THETA_PUBLISHED = {"v1pub": 0.76, "v2u16": 0.835, "v2u11": 0.877}

POLICY_KW = {
    "dn": dict(),
    "rule": dict(pace_cut=True),
    "band": dict(band=True),
    "rule_band": dict(pace_cut=True, band=True),
    "mixA": dict(rcf=15.0, pace=6.0, pace_cut=True, reserve=0.14),
    "mixB": dict(rcf=10.0, pace=12.0, pace_cut=True, band=True, reserve=0.08, hf_t0=5.0),
}
MODELS = ("M1", "M2", "M3", "M4", "M5", "M6")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _default(o):
    if hasattr(o, "tolist"):
        return o.tolist()
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    return str(o)


def save(name: str, obj: dict) -> str:
    path = os.path.join(HERE, name)
    obj = dict(obj)
    obj.setdefault("label", LABEL)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, default=_default)
    return path


def load(name: str):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def theta_star(book: str) -> float:
    """theta* for a book: ri_calib_results.json if present, else the published anchor."""
    cal = load("ri_calib_results.json")
    if cal is not None and book in cal.get("theta_star", {}):
        return float(cal["theta_star"][book]["theta"])
    if book in THETA_PUBLISHED:
        return THETA_PUBLISHED[book]
    raise KeyError(f"theta* for {book} needs ri_calib.py first")


def r2(x, nd=2):
    return None if x is None else round(float(x), nd)
