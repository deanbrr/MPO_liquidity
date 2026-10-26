"""Dependency-free .xlsx reader (values only), for the two input workbooks.

The venv has no openpyxl, and the workbooks are plain value grids (no formulas), so the sheet XML is read directly:
shared strings, inline strings, numbers and booleans. Cells keep their stored type: numbers stored as text (the fund
file stores most amounts as long decimal strings) come back as str and are converted by the caller.
"""
from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"


def _col(ref: str) -> int:
    n = 0
    for ch in re.match(r"([A-Z]+)", ref).group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def sheet_names(path: str | Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
    return [s.get("name") for s in wb.iter("{%s}sheet" % _NS["m"])]


def read_sheet(path: str | Path, sheet: int | str = 0) -> list[list]:
    """Rows of one sheet as dense lists (None for empty cells), in sheet order."""
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", _NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % _NS["m"])))
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rmap = {r.get("Id"): r.get("Target") for r in rels.iter(_REL)}
        sheets = [(s.get("name"), rmap[s.get("{%s}id" % _NS["r"])]) for s in wb.iter("{%s}sheet" % _NS["m"])]
        name, target = sheets[sheet] if isinstance(sheet, int) else next(s for s in sheets if s[0] == sheet)
        target = target.lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        root = ET.fromstring(zf.read(target))
    out: list[list] = []
    for row in root.iter("{%s}row" % _NS["m"]):
        vals: dict[int, object] = {}
        for c in row.findall("m:c", _NS):
            t, v = c.get("t"), c.find("m:v", _NS)
            if v is None:
                inl = c.find("m:is", _NS)
                if inl is not None:
                    vals[_col(c.get("r"))] = "".join(x.text or "" for x in inl.iter("{%s}t" % _NS["m"]))
                continue
            txt = v.text
            if t == "s":
                val: object = shared[int(txt)]
            elif t in ("str", "inlineStr", "e"):
                val = txt
            elif t == "b":
                val = bool(int(txt))
            else:
                try:
                    val = float(txt)
                except (TypeError, ValueError):
                    val = txt
            vals[_col(c.get("r"))] = val
        if vals:
            out.append([vals.get(i) for i in range(max(vals) + 1)])
    return out


def doc_properties(path: str | Path) -> dict:
    """Custom document properties (e.g. Microsoft Information Protection labels), for the data-handling notice."""
    props = {}
    with zipfile.ZipFile(path) as zf:
        if "docProps/custom.xml" not in zf.namelist():
            return props
        root = ET.fromstring(zf.read("docProps/custom.xml"))
    for p in root:
        name = p.get("name")
        val = "".join(x.text or "" for x in p)
        props[name] = val
    return props
