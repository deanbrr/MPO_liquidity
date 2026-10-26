"""Map every live holding to an ER strategy bucket (DERIVED, reviewable).

The fund file has no department or strategy column, so each row is classified by ordered, editable rules
(config/classifier_rules.json): investment class and style first, then strategy keywords, then GP names, then class
fallbacks. Every row records the rule that fired and a confidence (high / medium / low); config/mapping_overrides.csv
(FUND_CODE, department, vertical, vehicle) overrides any rule. The coverage report gives NAV by confidence and lists
the largest low-confidence rows for review. Both config files name managers and holdings from the fund file, so they
are git-ignored with the data.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pandas as pd

from .buckets import BY_ID, bucket_for

CONFIG = Path(__file__).resolve().parents[1] / "config"
CO_NAME = re.compile(r"co-?\s?invest|\bCIV\b|co - inv", re.I)


class Classifier:
    def __init__(self, rules_path: Path | None = None, overrides_path: Path | None = None):
        rp = Path(rules_path or CONFIG / "classifier_rules.json")
        if not rp.exists():
            raise FileNotFoundError(f"{rp} not found: it is git-ignored because its patterns name managers and holdings "
                                    "from the fund file; copy it from the machine that built the demo")
        spec = json.loads(rp.read_text(encoding="utf-8"))
        self.rules = []
        for r in spec["rules"]:
            rr = dict(r)
            rr["_re"] = re.compile(r["pattern"], re.I) if r.get("pattern") else None
            rr["_vby"] = [(re.compile(v["pattern"], re.I), v["vertical"]) for v in r.get("vertical_by", [])]
            self.rules.append(rr)
        self.overrides = {}
        op = Path(overrides_path or CONFIG / "mapping_overrides.csv")
        if op.exists():
            with op.open(encoding="utf-8-sig") as fh:
                for row in csv.DictReader(fh):
                    code = (row.get("FUND_CODE") or "").strip()
                    if code and not code.startswith("#"):
                        self.overrides[code] = (row["department"].strip(), row["vertical"].strip(),
                                                row["vehicle"].strip())

    @staticmethod
    def _vehicle(rule_vehicle: str, cls, style, name) -> str:
        if rule_vehicle != "auto":
            return rule_vehicle
        if style in ("Co-investment", "Direct investment"):
            return "Co-Invest"
        if cls in ("Company", "JV"):
            return "Co-Invest"
        if (cls is None or cls == "") and CO_NAME.search(name or ""):
            return "Co-Invest"
        return "Fund"

    def classify_row(self, code: str, name: str, cls, style) -> dict:
        name = name or ""
        cls = None if (cls is None or pd.isna(cls)) else str(cls)
        style = None if (style is None or pd.isna(style)) else str(style)
        if code in self.overrides:
            d, v, veh = self.overrides[code]
            b = bucket_for(d, v, veh)
            return {"bucket": b.id, "rule": "OVERRIDE", "confidence": "override", "proxy": False,
                    "rule_note": "mapping_overrides.csv"}
        for r in self.rules:
            if r.get("classes") and cls not in r["classes"]:
                continue
            if r.get("styles") and style not in r["styles"]:
                continue
            if r.get("styles_not") and style in r["styles_not"]:
                continue
            if r["_re"] is not None and not r["_re"].search(name):
                continue
            vert = None
            if r.get("class_vertical") and cls in r["class_vertical"]:
                vert = r["class_vertical"][cls]
            if vert is None:
                for rx, v in r["_vby"]:
                    if rx.search(name):
                        vert = v
                        break
            vert = vert or r["default_vertical"]
            veh = self._vehicle(r["vehicle"], cls, style, name)
            b = bucket_for(r["department"], vert, veh)
            return {"bucket": b.id, "rule": r["id"], "confidence": r["confidence"], "proxy": bool(r.get("proxy")),
                    "rule_note": r.get("note", "")}
        raise RuntimeError("the rule list must end with a catch-all")

    def classify(self, live: pd.DataFrame) -> pd.DataFrame:
        out = [self.classify_row(r.FUND_CODE, r.FUND_NAME, r.INVESTMENT_CLASS, r.INVESTMENT_STYLE)
               for r in live.itertuples()]
        res = live.copy()
        for k in ("bucket", "rule", "confidence", "proxy", "rule_note"):
            res[k] = [o[k] for o in out]
        res["department"] = [BY_ID[b].department for b in res["bucket"]]
        res["vertical"] = [BY_ID[b].vertical for b in res["bucket"]]
        res["vehicle"] = [BY_ID[b].vehicle for b in res["bucket"]]
        return res


def coverage(book: pd.DataFrame) -> dict:
    tot = float(book["nav_bn"].sum())
    by_conf = book.groupby("confidence")["nav_bn"].sum().to_dict()
    low = book[book["confidence"] == "low"].sort_values("nav_bn", ascending=False)
    proxy = book[book["proxy"]]
    return {
        "nav_bn": tot,
        "nav_by_confidence_bn": {k: float(v) for k, v in by_conf.items()},
        "share_high_or_medium": float(book.loc[book["confidence"].isin(["high", "medium", "override"]), "nav_bn"].sum()
                                      / max(tot, 1e-12)),
        "proxied_bn": float(proxy["nav_bn"].sum()),
        "low_confidence_top": [{"code": r.FUND_CODE, "name": r.FUND_NAME, "class": r.INVESTMENT_CLASS,
                                "style": r.INVESTMENT_STYLE, "bucket": r.bucket, "nav_bn": float(r.nav_bn),
                                "rule": r.rule} for r in low.head(40).itertuples()],
        "by_rule": {k: {"rows": int(len(g)), "nav_bn": float(g["nav_bn"].sum())}
                    for k, g in book.groupby("rule")},
    }
