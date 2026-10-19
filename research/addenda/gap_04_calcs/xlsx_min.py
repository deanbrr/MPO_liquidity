"""Minimal, dependency-free reader for simple .xlsx sheets (values only).

read_xlsx(path, sheet_index=1) -> list of rows (list of str|float|None), dense by column letter.
"""
from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _col_idx(ref: str) -> int:
    letters = re.match(r"([A-Z]+)", ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx(path: str, sheet_index: int = 1) -> list[list]:
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        root = ET.fromstring(zf.read(f"xl/worksheets/sheet{sheet_index}.xml"))
    rows_out: list[list] = []
    for row in root.iter("{%s}row" % NS["m"]):
        vals: dict[int, object] = {}
        for c in row.findall("m:c", NS):
            ref = c.get("r")
            t = c.get("t")
            v = c.find("m:v", NS)
            if v is None:
                isel = c.find("m:is", NS)
                if isel is not None:
                    vals[_col_idx(ref)] = "".join(x.text or "" for x in isel.iter("{%s}t" % NS["m"]))
                continue
            txt = v.text
            if t == "s":
                vals[_col_idx(ref)] = shared[int(txt)]
            elif t in ("str", "inlineStr"):
                vals[_col_idx(ref)] = txt
            else:
                try:
                    vals[_col_idx(ref)] = float(txt)
                except (TypeError, ValueError):
                    vals[_col_idx(ref)] = txt
        if vals:
            width = max(vals) + 1
            rows_out.append([vals.get(i) for i in range(width)])
    return rows_out


if __name__ == "__main__":
    import sys
    rows = read_xlsx(sys.argv[1])
    for r in rows[:25]:
        print(r)
    print("...")
    for r in rows[-12:]:
        print(r)
    print("n rows", len(rows))
