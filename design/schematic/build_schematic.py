"""Render architecture_model.json into one self-contained, offline HTML file.

Run:  .venv\\Scripts\\python.exe design\\schematic\\build_schematic.py
Reads  design/schematic/architecture_model.json
Writes design/schematic/TPA_Lab_Architecture.html  (six inline SVG views, no external resources)

Layout is deterministic: lanes are rows on a shared column grid; within a lane row, nodes are
ordered by the barycentre of their neighbours (sequences and trust-boundary groups keep their
order and contiguity); columns are chosen by a small dynamic programme that balances the
neighbours' pull against an even spread; edges are routed orthogonally through horizontal
channels (between rows) and vertical gutters (between columns), with every segment on its own
track, so no two edges overlap and edge labels never overlap each other or a box.  Boxes take
their natural height with tops aligned.  Captions sit only in zones no line enters: over
columns with no line entering from above, or beside a box whose top line ends are squeezed
aside; a second routing pass can steer long lines away from those zones.  Each grid view is laid
out under a fixed set of settings (SEARCH) and the one with the least height + crossings wins.
Neighbours in a row joined by an unlabelled edge get a short side arrow.  The page adds line-type
toggles to every legend and a details panel that keyboard and touch users reach by focusing a box.
The cycle view uses a timeline layout.
"""
from __future__ import annotations

import bisect
import html
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL_PATH = HERE / "architecture_model.json"
OUT_PATH = HERE / "TPA_Lab_Architecture.html"

# ------------------------------------------------------------------ config
TARGET_W = 1360          # viewBox width aimed at a 1440px laptop at 100% zoom
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 18, 18, 6, 14
F_LABEL, F_SUB, F_EDGE, F_LANE, F_BADGE, F_GROUP = 12.5, 11.0, 11.0, 11.5, 11.0, 11.0
LH_LABEL, LH_SUB, LH_BADGE, LH_CAPTION = 15.0, 13.5, 13.0, 14.0
NODE_PAD_X, NODE_PAD_T, NODE_PAD_B = 8, 7, 8
TRACK_H, CH_PAD_T, CH_PAD_B, CH_EMPTY = 16, 17, 11, 14
GUT_TRACK, GUT_PAD, GUT_MIN = 6, 9, 20
ROW_PAD_T_NOCAP, ROW_PAD_B = 8, 8
MIN_CW, MAX_CW = 120, 215
CORNER_R = 5
# layout tuning (visual review V1, V2, V5, V8)
EVEN_W = 0.6             # weight of the even-spread slot against the neighbours' barycentre (V5)
GUT_LOAD_W = 0.9         # congestion cost per gutter track already used over the same rows (V5)
BARY_SWEEPS, FIX_SWEEPS = 14, 6   # sweeps that may reorder a lane by barycentre, then column-only sweeps (V1)
PORT_MIN_GAP = 8.5       # minimum spacing of line ends on a box side squeezed by a caption (V2)
CAP_MIN_W = 66           # narrowest caption block placed beside a box's line ends (V2)
CAP_GAP = 6              # clearance between a caption block and the nearest line end (V2)
AVOID_W = 1.2            # gutter cost per row whose caption would wrap less without that gutter (V2)
CROSS_W = 1.3            # layout search objective: px of height worth one crossing (V1)
# even-spread weight stays >= 0.35 so boxes keep filling the width (V5)
SEARCH = [dict(even_w=e, gut_load_w=g, bary=b, avoid=a)
          for e in (0.35, 0.5, 0.6, 0.75) for g in (0.3, 0.45, 0.9, 1.4, 2.0) for b in (6, BARY_SWEEPS, 24)
          for a in (False, True)]

# ------------------------------------------------------------ text metrics
_NARROW = set("iljI.,;:'!|`′")
_MID = set("()[]{}/\\-·*\"ftr ")
_WIDE = set("MWmw@%—∞⇄")


def char_w(c: str) -> float:
    """Approximate advance width as a fraction of font size (deliberately generous)."""
    if c in "  ":
        return 0.32
    if c in _NARROW:
        return 0.34
    if c in _MID:
        return 0.44
    if c in _WIDE:
        return 0.92
    if c in "→←⇒≤≥≈±×∑ΣΠΛΓΘΨΔ":
        return 0.78
    if c.isupper() or c.isdigit():
        return 0.70
    return 0.58


def text_w(s: str, fs: float, bold: bool = False) -> float:
    """Never below the 0.6 x font-size per character rule; wider for capitals."""
    w = sum(char_w(c) for c in s) * fs
    w = max(w, 0.6 * len(s) * fs)
    return w * (1.03 if bold else 1.0)


_BREAK_AFTER = "_/-·.,;@|"


def _split_long(word: str, fs: float, max_w: float, bold: bool) -> list[str]:
    if " " in word:                       # undo symbol glue before cutting inside a word
        pieces = word.split(" ")
        out, cur = [], ""
        for p in pieces:
            trial = f"{cur} {p}" if cur else p
            if text_w(trial, fs, bold) <= max_w:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = p
        if cur:
            out.append(cur)
        if all(text_w(p, fs, bold) <= max_w for p in out):
            return out
        word = " ".join(out)
    parts, cur = [], ""
    for ch in word:
        if cur and text_w(cur + ch, fs, bold) > max_w:
            cut = max((cur.rfind(b) for b in _BREAK_AFTER), default=-1)
            if cut >= 1:
                parts.append(cur[:cut + 1])
                cur = cur[cut + 1:]
            else:
                parts.append(cur)
                cur = ""
        cur += ch
    if cur:
        parts.append(cur)
    return parts


_GLUE_PREV = {"·", "|", "/", "–", "—", "→", "⇄", "+", "=", "&"}
_GLUE_NEXT = {"≤", "≥", "≈", "×", "±", "<", ">", "~", "−"}


def _tokens(text: str) -> list[str]:
    """Split on plain spaces only (NBSP keeps pairs together); glue lone symbols to a neighbour."""
    raw = [w for w in text.split(" ") if w]
    out: list[str] = []
    carry = ""
    for w in raw:
        if w in _GLUE_NEXT:
            carry = (carry + " " if carry else "") + w
            continue
        if carry:
            w = carry + " " + w
            carry = ""
        if w in _GLUE_PREV and out:
            out[-1] = out[-1] + " " + w
        else:
            out.append(w)
    if carry:
        if out:
            out[-1] = out[-1] + " " + carry
        else:
            out.append(carry)
    return out


def wrap(text: str, fs: float, max_w: float, bold: bool = False) -> list[str]:
    if not text:
        return []
    lines, cur = [], ""
    for word in _tokens(text):
        trial = f"{cur} {word}" if cur else word
        if text_w(trial, fs, bold) <= max_w:
            cur = trial
            continue
        if cur:
            lines.append(cur)
            cur = ""
        if text_w(word, fs, bold) <= max_w:
            cur = word
        else:
            pieces = _split_long(word, fs, max_w, bold)
            lines.extend(pieces[:-1])
            cur = pieces[-1]
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- helpers
def esc(s) -> str:
    return html.escape(str(s), quote=True)


def f1(x: float) -> str:
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def rounded_path(pts: list[tuple[float, float]], r: float = CORNER_R) -> str:
    """Orthogonal polyline with small rounded corners; drops zero-length legs."""
    clean = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - clean[-1][0]) > 0.01 or abs(p[1] - clean[-1][1]) > 0.01:
            clean.append(p)
    pts = clean
    if len(pts) == 1:
        return f"M{f1(pts[0][0])},{f1(pts[0][1])}"
    d = [f"M{f1(pts[0][0])},{f1(pts[0][1])}"]
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        l1 = math.hypot(x1 - x0, y1 - y0)
        l2 = math.hypot(x2 - x1, y2 - y1)
        rr = min(r, l1 / 2, l2 / 2)
        if rr < 0.5:
            d.append(f"L{f1(x1)},{f1(y1)}")
            continue
        ax = x1 - (x1 - x0) / l1 * rr
        ay = y1 - (y1 - y0) / l1 * rr
        bx = x1 + (x2 - x1) / l2 * rr
        by = y1 + (y2 - y1) / l2 * rr
        d.append(f"L{f1(ax)},{f1(ay)}Q{f1(x1)},{f1(y1)} {f1(bx)},{f1(by)}")
    d.append(f"L{f1(pts[-1][0])},{f1(pts[-1][1])}")
    return "".join(d)


def node_tooltip(n: dict, meta: dict) -> str:
    owner = n.get("owner") or "not stated in ARCHITECTURE.md"
    parts = [n["label"]]
    if n.get("sublabel"):
        parts.append(n["sublabel"])
    parts.append(f"Owner: {owner}")
    parts.append(f"Section: {n.get('section', '')}")
    if n.get("badge"):
        parts.append(f"Real Assets: {n['badge']}")
    if n.get("detail"):
        parts.append(n["detail"])
    for key in ("tools", "labels", "drills", "tests"):
        if n.get(key):
            parts.append(f"{key.capitalize()}: " + ", ".join(n[key]))
    for key in ("family", "effort", "output", "gate", "produces", "fsm_state"):
        if n.get(key):
            parts.append(f"{key.replace('_', ' ').capitalize()}: {n[key]}")
    if n.get("actors"):
        parts.append("Actors: " + ", ".join(n["actors"]))
    return "\n".join(parts)


def edge_tooltip(e: dict, nodes: dict) -> str:
    a, b = nodes[e["from"]]["label"], nodes[e["to"]]["label"]
    parts = [f"{a} → {b}"]
    if e.get("label"):
        parts.append(e["label"])
    parts.append(f"Kind: {e['kind']}")
    parts.append(f"Section: {e.get('section', '')}")
    if e.get("badge"):
        parts.append(f"Real Assets: {e['badge']}")
    if e.get("detail"):
        parts.append(e["detail"])
    return "\n".join(parts)


def group_tooltip(g: dict) -> str:
    parts = [g["label"], f"Section: {g.get('section', '')}"]
    if g.get("detail"):
        parts.append(g["detail"])
    return "\n".join(parts)


# ------------------------------------------------------------ grid layout
ARRIVE_GAP_W = 1.8       # relative spacing between two arrowheads that land on the same box side


def spread(items: list[dict], lo: float, hi: float) -> None:
    """Spread line ends over [lo, hi] in far-end order; neighbouring arrowheads on one box side get more room."""
    items.sort(key=lambda it: (it["key"], it["tie"]))
    if not items:
        return
    gaps = [1.0]
    for a, b in zip(items, items[1:]):
        both = a.get("arrive") and b.get("arrive") and a.get("node") == b.get("node") and a.get("side") == b.get("side")
        gaps.append(ARRIVE_GAP_W if both else 1.0)
    gaps.append(1.0)
    tot, acc = sum(gaps), 0.0
    for k, it in enumerate(items):
        acc += gaps[k]
        it["x"] = lo + (hi - lo) * acc / tot


def split_spans(counts: list[int], cols: int) -> list[int]:
    spans, extra = list(counts), cols - sum(counts)
    if extra < 0:
        raise ValueError(f"shared row needs {sum(counts)} columns, grid has {cols}")
    order = sorted(range(len(counts)), key=lambda k: (-counts[k], k))
    i = 0
    while extra > 0:
        spans[order[i % len(order)]] += 1
        extra -= 1
        i += 1
    return spans


def dp_assign(desired: list[float], c0: int, c1: int, pack: bool = False) -> list[int]:
    """Strictly increasing columns in [c0, c1) minimising squared distance to desired."""
    k, m = len(desired), c1 - c0
    if k == 0:
        return []
    if pack:
        best = min(range(m - k + 1),
                   key=lambda s: (sum((c0 + s + i - desired[i]) ** 2 for i in range(k)), s))
        return [c0 + best + i for i in range(k)]
    inf = float("inf")
    cost = [[inf] * m for _ in range(k)]
    back = [[-1] * m for _ in range(k)]
    for c in range(m):
        cost[0][c] = (c0 + c - desired[0]) ** 2
    for i in range(1, k):
        best, bi = inf, -1
        for c in range(m):
            if c >= 1 and cost[i - 1][c - 1] < best:
                best, bi = cost[i - 1][c - 1], c - 1
            if best < inf:
                cost[i][c] = best + (c0 + c - desired[i]) ** 2
                back[i][c] = bi
    c = min(range(m), key=lambda cc: (cost[k - 1][cc], cc))
    out = [0] * k
    for i in range(k - 1, -1, -1):
        out[i] = c0 + c
        c = back[i][c]
    return out


class Grid:
    """Rows of lanes on a shared column grid, routed through channels and gutters."""

    def __init__(self, view: dict, meta: dict, params: dict | None = None):
        self.v, self.meta = view, meta
        self.p = {"even_w": EVEN_W, "gut_load_w": GUT_LOAD_W, "bary": BARY_SWEEPS, "avoid": False,
                  **(params or {})}
        self.avoid: set[tuple[int, int]] = set()
        self.lay = view["layout"]
        self.C = int(self.lay["columns"])
        self.nodes = {n["id"]: n for n in view["nodes"]}
        self.lanes = {l["id"]: l for l in view["lanes"]}
        self.edges = [dict(e, idx=i) for i, e in enumerate(view["edges"])]
        self.badge = meta["badge_text"]
        self.warnings: list[str] = []
        self.serp = set(self.lay.get("serpentine", []))
        self.fixed = set(self.lay.get("pack", [])) | self.serp      # sequences keep their model order
        self.group_of = {nid: g["id"] for g in view.get("groups", []) if g.get("kind") != "perimeter"
                         for nid in g["nodes"]}
        self._build_rows()
        self._assign_columns()

    # -------------------------------------------------------------- rows
    def _lane_node_rows(self, lane: str, span: int) -> list[list[str]]:
        override = self.lay.get("lane_rows", {}).get(lane)
        if override:
            rows = [list(r) for r in override]
        else:
            ids = [n["id"] for n in sorted((n for n in self.v["nodes"] if n["lane"] == lane),
                                           key=lambda n: (n.get("order", 0), n["id"]))]
            k = max(1, math.ceil(len(ids) / span))
            sizes = [len(ids) // k + (1 if i < len(ids) % k else 0) for i in range(k)]
            rows, p = [], 0
            for s in sizes:
                rows.append(ids[p:p + s])
                p += s
        for r in rows:
            if len(r) > span:
                raise ValueError(f"lane {lane}: row of {len(r)} nodes exceeds {span} columns")
        return rows

    def _build_rows(self) -> None:
        self.rows: list[list[dict]] = []
        for spec in self.lay["rows"]:
            if len(spec) == 1:
                lane = spec[0]
                lrows = self._lane_node_rows(lane, self.C)
                for j, ids in enumerate(lrows):
                    self.rows.append([{"lane": lane, "c0": 0, "c1": self.C, "ids": ids,
                                       "first": j == 0, "last": j == len(lrows) - 1, "lrow": j}])
            else:
                members = []
                for lane in spec:
                    lr = self._lane_node_rows(lane, self.C)
                    if len(lr) != 1:
                        raise ValueError(f"lane {lane} spans rows; it cannot share a row")
                    members.append(lr[0])
                spans = split_spans([len(m) for m in members], self.C)
                c, segs = 0, []
                for lane, ids, sp in zip(spec, members, spans):
                    segs.append({"lane": lane, "c0": c, "c1": c + sp, "ids": ids,
                                 "first": True, "last": True, "lrow": 0})
                    c += sp
                self.rows.append(segs)
        self.R = len(self.rows)
        self.seg_of: dict[str, dict] = {}
        self.row_of: dict[str, int] = {}
        for r, segs in enumerate(self.rows):
            for seg in segs:
                for nid in seg["ids"]:
                    self.seg_of[nid] = seg
                    self.row_of[nid] = r
        missing = set(self.nodes) - set(self.row_of)
        if missing:
            raise ValueError(f"{self.v['id']}: nodes not placed: {sorted(missing)}")

    def _seg_order(self, seg: dict) -> list[str]:
        ids = list(seg["ids"])
        if seg["lane"] in self.lay.get("serpentine", []) and seg["lrow"] % 2 == 1:
            ids.reverse()
        return ids

    # ----------------------------------------------------------- columns
    def _reorder(self, seg: dict, bary: dict[str, float | None], rank: dict[str, int]) -> None:
        """Order a lane row by its neighbours' barycentre (V1), keeping trust-boundary groups contiguous."""
        def key(nid: str) -> float:
            b = bary[nid]
            return b if b is not None else self.col[nid] + 0.5
        units, seen = [], set()
        for nid in seg["ids"]:
            g = self.group_of.get(nid)
            if g is None:
                units.append((key(nid), rank[nid], [nid]))
            elif g not in seen:
                seen.add(g)
                mem = sorted((x for x in seg["ids"] if self.group_of.get(x) == g), key=lambda x: (key(x), rank[x]))
                units.append((sum(key(x) for x in mem) / len(mem), rank[mem[0]], mem))
        units.sort(key=lambda u: (u[0], u[1]))
        seg["ids"][:] = [x for u in units for x in u[2]]

    def _assign_columns(self) -> None:
        packed = set(self.lay.get("pack", []))
        self.col: dict[str, int] = {}
        rank: dict[str, int] = {}
        for r, segs in enumerate(self.rows):
            for seg in segs:
                ids, m = self._seg_order(seg), seg["c1"] - seg["c0"]
                for i, nid in enumerate(ids):
                    self.col[nid] = seg["c0"] + int((i + 0.5) * m / len(ids))
                    rank[nid] = i
        nbrs: dict[str, list[tuple[str, float]]] = {nid: [] for nid in self.nodes}
        for e in self.edges:
            if e["from"] == e["to"]:
                continue
            w = 0.35 if e["kind"] == "guard" else 1.0
            nbrs[e["from"]].append((e["to"], w))
            nbrs[e["to"]].append((e["from"], w))
        sweeps, even_w = self.p["bary"], self.p["even_w"]
        for it in range(sweeps + FIX_SWEEPS):
            seq = range(self.R) if it % 2 == 0 else range(self.R - 1, -1, -1)
            for r in seq:
                for seg in self.rows[r]:
                    m = seg["c1"] - seg["c0"]
                    if not any(nbrs[nid] for nid in seg["ids"]):      # unlinked lane: pack to the left
                        for i, nid in enumerate(self._seg_order(seg)):
                            self.col[nid] = seg["c0"] + i
                        continue
                    bary: dict[str, float | None] = {}
                    for nid in seg["ids"]:
                        tot = wsum = 0.0
                        for other, w in nbrs[nid]:
                            dw = w / (1.0 + 0.15 * abs(self.row_of[other] - r))
                            tot += self.col[other] * dw
                            wsum += dw
                        bary[nid] = tot / wsum if wsum else None
                    if it < sweeps and seg["lane"] not in self.fixed:
                        self._reorder(seg, bary, rank)
                    ids = self._seg_order(seg)
                    desired = []
                    for i, nid in enumerate(ids):
                        even = seg["c0"] + (i + 0.5) * m / len(ids) - 0.5
                        b = bary[nid]
                        desired.append((1 - even_w) * b + even_w * even if b is not None else even)
                    for nid, c in zip(ids, dp_assign(desired, seg["c0"], seg["c1"],
                                                     pack=seg["lane"] in packed)):
                        self.col[nid] = c

    # ----------------------------------------------------------- routing
    def route(self) -> None:
        """Discrete routing: case per edge, gutter choice, port slots, gutter tracks."""
        self.routes: list[dict] = []
        for e in self.edges:
            a, b = e["from"], e["to"]
            r = {"e": e, "rs": self.row_of[a], "cs": self.col[a], "rt": self.row_of[b], "ct": self.col[b]}
            rs, rt = r["rs"], r["rt"]
            if rs == rt and not e.get("label") and abs(r["cs"] - r["ct"]) == 1:
                # neighbours in one row (a sequence step): a short arrow between side ports (V8)
                right = r["ct"] > r["cs"]
                r.update(case="side", s_side="right" if right else "left", t_side="left" if right else "right")
            elif rs == rt:
                r.update(case="same", ch1=rs + 1, s_side="bottom", t_side="bottom")
            elif rt == rs + 1:
                r.update(case="down1", ch1=rs + 1, s_side="bottom", t_side="top")
            elif rt == rs - 1:
                r.update(case="up1", ch1=rs, s_side="top", t_side="bottom")
            elif rt > rs:
                r.update(case="down", ch1=rs + 1, ch2=rt, s_side="bottom", t_side="top")
            else:
                r.update(case="up", ch1=rs, ch2=rt + 1, s_side="top", t_side="bottom")
            if r["case"] in ("down", "up"):
                r["va"], r["vb"] = min(r["ch1"], r["ch2"]), max(r["ch1"], r["ch2"])
            self.routes.append(r)
        # same-row U-turns use the less loaded side, so arrowheads do not pile up on one box edge
        load: dict[tuple[str, str], int] = {}
        for r in self.routes:
            if r["case"] not in ("same", "side"):
                for nid, side in ((r["e"]["from"], r["s_side"]), (r["e"]["to"], r["t_side"])):
                    load[(nid, side)] = load.get((nid, side), 0) + 1
        for r in sorted((r for r in self.routes if r["case"] == "same"), key=lambda r: r["e"]["idx"]):
            a, b = r["e"]["from"], r["e"]["to"]
            lb = load.get((a, "bottom"), 0) + load.get((b, "bottom"), 0)
            lt = load.get((a, "top"), 0) + load.get((b, "top"), 0)
            side = "top" if lt + 2 <= lb else "bottom"
            r.update(ch1=r["rs"] if side == "top" else r["rs"] + 1, s_side=side, t_side=side)
            for nid in (a, b):
                load[(nid, side)] = load.get((nid, side), 0) + 1
        # gutters: longest spans first, cost = horizontal detour + congestion
        occ: dict[int, list[tuple[int, int]]] = {g: [] for g in range(self.C + 1)}
        need = sorted((r for r in self.routes if r["case"] in ("down", "up")),
                      key=lambda r: (-(r["vb"] - r["va"]), r["e"]["idx"]))
        for r in need:
            cs, ct = r["cs"] + 0.5, r["ct"] + 0.5
            mid = (cs + ct) / 2

            def cost(g: int) -> tuple:
                load = sum(1 for (a, b) in occ[g] if not (r["vb"] < a or r["va"] > b))
                pen = sum(1 for rr in range(r["va"], r["vb"]) if (rr, g) in self.avoid)   # keep caption zones open
                return (abs(g - cs) + abs(g - ct) + self.p["gut_load_w"] * load + AVOID_W * pen, abs(g - mid), g)
            g = min(range(self.C + 1), key=cost)
            r["g"] = g
            occ[g].append((r["va"], r["vb"]))
        # port slot items, grouped by (channel, column)
        self.port_groups: dict[tuple[int, int], list[dict]] = {}

        def add(key: tuple[int, int], item: dict) -> None:
            self.port_groups.setdefault(key, []).append(item)
        for r in self.routes:
            i = r["e"]["idx"]
            if r["case"] == "side":
                continue
            if r["case"] in ("down1", "up1") and r["cs"] == r["ct"]:
                # one straight vertical: it enters the top of the lower box
                lower = r["rt"] if r["case"] == "down1" else r["rs"]
                item = {"key": r["cs"] + 0.5, "tie": 2 * i, "x": None, "node": r["e"]["to"],
                        "side": r["t_side"], "arrive": True, "top_row": lower}
                r["sp"] = r["tp"] = item
                add((r["ch1"], r["cs"]), item)
                continue
            for end in ("s", "t"):
                row = r["rs"] if end == "s" else r["rt"]
                col = r["cs"] if end == "s" else r["ct"]
                side = r["s_side"] if end == "s" else r["t_side"]
                if r["case"] in ("down", "up"):
                    far = float(r["g"])
                else:
                    far = (r["ct"] if end == "s" else r["cs"]) + 0.5
                item = {"key": far, "tie": 2 * i + (0 if end == "s" else 1), "x": None,
                        "node": r["e"]["from" if end == "s" else "to"], "side": side, "arrive": end == "t",
                        "top_row": row if side == "top" else None}
                r["sp" if end == "s" else "tp"] = item
                add((row + 1 if side == "bottom" else row, col), item)
        # gutter tracks (interval colouring over channel spans, inclusive)
        self.gutter_n = [0] * (self.C + 1)
        for g in range(self.C + 1):
            segs = sorted((r for r in self.routes if r.get("g") == g),
                          key=lambda r: (r["va"], r["vb"], r["e"]["idx"]))
            tracks: list[list[tuple[int, int]]] = []
            for r in segs:
                for ti, used in enumerate(tracks):
                    if all(r["vb"] < a or r["va"] > b for (a, b) in used):
                        used.append((r["va"], r["vb"]))
                        r["gt"] = ti
                        break
                else:
                    tracks.append([(r["va"], r["vb"])])
                    r["gt"] = len(tracks) - 1
            self.gutter_n[g] = len(tracks)

    # ------------------------------------------------------ x geometry
    def geometry_x(self) -> None:
        gw = []
        for g, n in enumerate(self.gutter_n):
            outer = g in (0, self.C)
            base = 6 if outer else GUT_MIN
            gw.append(max(base, 2 * GUT_PAD + (n - 1) * GUT_TRACK) if n else base)
        cw = (TARGET_W - MARGIN_L - MARGIN_R - sum(gw)) / self.C
        if cw < MIN_CW:
            self.warnings.append(f"column width {cw:.0f} < {MIN_CW}; diagram wider than target")
        self.cw = max(MIN_CW, min(MAX_CW, cw))
        self.gw = gw
        x = MARGIN_L
        self.gut_x, self.col_x = [], []
        for g in range(self.C + 1):
            self.gut_x.append(x)
            x += gw[g]
            if g < self.C:
                self.col_x.append(x)
                x += self.cw
        self.W = x + MARGIN_R
        for (ch, col), items in self.port_groups.items():
            spread(items, self.col_x[col], self.col_x[col] + self.cw)
        for r in self.routes:
            if "g" in r:
                n = self.gutter_n[r["g"]]
                center = self.gut_x[r["g"]] + self.gw[r["g"]] / 2
                r["gx"] = center + (r["gt"] - (n - 1) / 2) * GUT_TRACK

    # ------------------------------------------------- nodes and captions
    def measure_nodes(self) -> None:
        inner = self.cw - 2 * NODE_PAD_X
        self.nl: dict[str, dict] = {}
        for nid, n in self.nodes.items():
            L = wrap(n["label"], F_LABEL, inner, bold=True)
            S = wrap(n.get("sublabel", ""), F_SUB, inner)
            B = wrap(self.badge, F_BADGE, inner - 8) if n.get("badge") else []
            hc = NODE_PAD_T + len(L) * LH_LABEL + ((2 + len(S) * LH_SUB) if S else 0)
            h = hc + ((4 + len(B) * LH_BADGE + 6 + 3) if B else NODE_PAD_B)
            self.nl[nid] = {"L": L, "S": S, "B": B, "hc": hc, "h": h}
        self.row_node_h = [max(self.nl[nid]["h"] for seg in segs for nid in seg["ids"])
                           for segs in self.rows]

    def _group_boxes(self) -> None:
        """Resolve trust-boundary groups to rows; perimeter groups span whole rows."""
        self.boxes, self.perimeters = [], []
        for g in self.v.get("groups", []):
            if g.get("kind") == "perimeter":
                first, last = g["rows_of_lanes"]
                rows_first = [r for r, segs in enumerate(self.rows) if any(s["lane"] == first for s in segs)]
                rows_last = [r for r, segs in enumerate(self.rows) if any(s["lane"] == last for s in segs)]
                self.perimeters.append({"g": g, "r0": min(rows_first), "r1": max(rows_last)})
                continue
            rows = {self.row_of[n] for n in g["nodes"]}
            if len(rows) != 1:
                self.warnings.append(f"group {g['id']} spans rows; skipped")
                continue
            r = rows.pop()
            cols = [self.col[n] for n in g["nodes"]]
            inside = [nid for nid in self.nodes if self.row_of[nid] == r
                      and min(cols) <= self.col[nid] <= max(cols) and nid not in g["nodes"]]
            if inside:
                self.warnings.append(f"group {g['id']} would enclose {inside}; skipped")
                continue
            self.boxes.append({"g": g, "r": r, "c0": min(cols), "c1": max(cols)})

    def _lane_caption(self, lane: dict) -> str:
        t = lane["label"]
        if lane["id"] in self.serp:
            t += " · rows alternate →, ←"      # marks the serpentine wrap (V8)
        return t

    def captions(self) -> None:
        """Place captions only where no line runs (V2).

        In a row's caption band the only lines are (i) line ends entering the top of that row's boxes and
        (ii) vertical gutter tracks passing through the row.  A caption therefore goes either over an empty
        column (spanning further empty columns where no gutter track crosses the row), or over the left part
        of an occupied column whose top line ends are then spread over the rest of the box's width."""
        self._group_boxes()
        occ = [set() for _ in range(self.R)]
        for nid, r in self.row_of.items():
            occ[r].add(self.col[nid])
        gcross: list[set[int]] = [set() for _ in range(self.R)]
        for rt in self.routes:
            if "g" in rt:
                for rr in range(rt["va"], rt["vb"]):
                    gcross[rr].add(rt["g"])
        self.cap_items: list[list[dict]] = [[] for _ in range(self.R)]
        self.port_limits: dict[tuple[int, int], tuple[float, float]] = {}
        self.cap_h = []
        self.wanted: set[tuple[int, int]] = set()
        for r in range(self.R):
            wants = self._wants(r)
            if self.p["avoid"] and not self.avoid and gcross[r]:
                # which crossed gutters, if routed elsewhere, would let this row's captions wrap less?
                base = self._row_lines(r, wants, gcross[r])
                if base > 1:
                    self.wanted |= {(r, g) for g in gcross[r]
                                    if self._row_lines(r, wants, gcross[r] - {g}) < base}
            zones: dict[int, dict] = {}
            for w in wants:
                self._place_caption(r, w, gcross[r], zones)
            n_lines = max((z["lines"] for z in zones.values()), default=0)
            self.cap_h.append((4 + n_lines * LH_CAPTION + 6) if n_lines else ROW_PAD_T_NOCAP)
        self.row_h = [self.cap_h[r] + self.row_node_h[r] + ROW_PAD_B for r in range(self.R)]
        for (r, c), (lo, hi) in self.port_limits.items():
            # only line ends entering the box from above cross the caption band; squeeze those, keep the
            # ends of the box above spread over the whole column, and keep every x distinct
            items = self.port_groups.get((r, c), [])
            top = [it for it in items if it.get("top_row") == r]
            rest = [it for it in items if it.get("top_row") != r]
            spread(top, lo, hi)
            spread(rest, self.col_x[c], self.col_x[c] + self.cw)
            taken = sorted(it["x"] for it in top)
            for it in rest:
                for _ in range(4):
                    clash = [x for x in taken if abs(it["x"] - x) < 1.6]
                    if not clash:
                        break
                    it["x"] = clash[0] + (2.0 if it["x"] >= clash[0] else -2.0)
                taken.append(it["x"])

    def _wants(self, r: int) -> list[dict]:
        """Captions requested in row r: trust-boundary groups first, then lanes, then the perimeter."""
        wants = [{"kind": "group", "text": b["g"]["label"], "fs": F_GROUP, "lo": b["c0"], "hi": b["c1"],
                  "side": "left", "g": b["g"]} for b in self.boxes if b["r"] == r]
        for seg in self.rows[r]:
            if seg["first"]:
                lane = self.lanes[seg["lane"]]
                wants.append({"kind": "lane", "text": self._lane_caption(lane), "fs": F_LANE,
                              "lo": seg["c0"], "hi": seg["c1"] - 1, "side": "left", "lane": lane})
        wants += [{"kind": "perimeter", "text": p["g"]["label"], "fs": F_GROUP, "lo": 0, "hi": self.C - 1,
                   "side": "right", "g": p["g"]} for p in self.perimeters if p["r0"] == r]
        return wants

    def _row_lines(self, r: int, wants: list[dict], gcross: set[int]) -> int:
        zones: dict[int, dict] = {}
        return max((self._place_caption(r, w, gcross, zones, dry=True) for w in wants), default=0)

    def _place_caption(self, r: int, w: dict, gcross: set[int], zones: dict[int, dict], dry: bool = False) -> int:
        """Choose a caption zone in row r: a run of columns that no line enters from above (free), optionally
        ending in the near part of a column whose top line ends are then squeezed to its far part (busy).
        With dry=True only the zones are marked and the line count returned."""
        cw, fs, text = self.cw, w["fs"], w["text"]
        full = text_w(text, fs, True)
        lo_c, hi_c = w["lo"], w["hi"]

        def n_top(c: int) -> int:
            return sum(1 for it in self.port_groups.get((r, c), []) if it.get("top_row") == r)

        def usable(c: int) -> float:          # caption width a busy column can give up
            return cw - 2 - CAP_GAP - (n_top(c) + 1) * PORT_MIN_GAP

        def grow(x0: float, width: float, cur: int, members: list[int]):
            """Extend a zone rightwards over free columns, ending in at most one busy column."""
            busy_end = None
            while full > width:
                nxt = cur + 1
                if nxt > hi_c or nxt in zones or nxt in gcross:          # gutter nxt lies between cur and nxt
                    break
                if n_top(nxt):
                    u = usable(nxt)
                    if u >= 24:
                        width = self.col_x[nxt] + u - x0
                        members.append(nxt)
                        busy_end = nxt
                    break
                width = self.col_x[nxt] + cw - 2 - x0
                members.append(nxt)
                cur = nxt
            return width, members, busy_end
        cands = []
        for s in range(lo_c, hi_c + 1):
            if s in zones:
                continue
            if not n_top(s):
                x0 = self.col_x[s]
                cands.append((x0, *grow(x0, cw - 2, s, [s]), None))
                continue
            u = usable(s)
            x0 = self.col_x[s] - 2                       # left part of a busy box; its line ends move right
            cands.append((x0, max(CAP_MIN_W, min(cw - 4, u)), [s], s, None))
            if u >= 24 and s + 1 <= hi_c and s + 1 not in zones and s + 1 not in gcross and not n_top(s + 1):
                x0 = self.col_x[s] + cw - u              # right part of a busy box; its line ends move left
                cands.append((x0, *grow(x0, u - 2, s, [s]), s))
        best = None
        for x0, width, members, busy_end, busy_start in cands:
            lines = wrap(text, fs, width, bold=True)
            pos = (members[0] - lo_c) if w["side"] == "left" else (hi_c - members[-1])
            score = 2.0 * len(lines) + 0.45 * pos + 0.5 * ((busy_end is not None) + (busy_start is not None))
            if best is None or score < best[0]:
                best = (score, x0, members, busy_end, busy_start, lines)
        if best is None:                                   # no free column left: stack in the first column
            z = zones[lo_c]
            lines = wrap(text, fs, cw - 4, bold=True)
            z["lines"] += len(lines)
            if dry:
                return z["lines"]
            self.warnings.append(f"caption '{text[:30]}' found no free zone in row {r}")
            item = {"kind": w["kind"], "x": z["x"], "line": z["lines"] - len(lines), "lines": lines,
                    "anchor": "start"}
        else:
            _, x0, members, busy_end, busy_start, lines = best
            z = {"lines": len(lines), "x": x0}
            for c in members:
                zones[c] = z
            if dry:
                return len(lines)
            tw = max(text_w(t, fs, True) for t in lines)
            if busy_start is not None:
                self.port_limits[(r, busy_start)] = (self.col_x[busy_start] + 3, x0 - CAP_GAP)
            if busy_end is not None and x0 + tw > self.col_x[busy_end]:
                self.port_limits[(r, busy_end)] = (x0 + tw + CAP_GAP, self.col_x[busy_end] + cw - 3)
            item = {"kind": w["kind"], "x": x0, "line": 0, "lines": lines, "anchor": "start"}
        item["lane" if w["kind"] == "lane" else "g"] = w.get("lane") or w.get("g")
        self.cap_items[r].append(item)
        return len(lines)

    # ------------------------------------------------- channel tracks
    def channel_tracks(self) -> None:
        self.hsegs: dict[int, list[dict]] = {}
        for r in self.routes:
            if r["case"] == "side":
                r["hs"] = []
                continue
            lab = r["e"].get("label") or ""
            xs, xt = r["sp"]["x"], r["tp"]["x"]
            if r["case"] in ("same", "down1", "up1"):
                u = ("below" if r["s_side"] == "bottom" else "above") if r["case"] == "same" else None
                parts = [(r["ch1"], xs, xt, True, u)]
            else:
                parts = [(r["ch1"], xs, r["gx"], True, None), (r["ch2"], r["gx"], xt, False, None)]
            r["hs"] = []
            for ch, x0, x1, labelled, uturn in parts:
                lo, hi = min(x0, x1), max(x0, x1)
                s = {"route": r, "ch": ch, "x0": x0, "x1": x1, "lo": lo, "hi": hi,
                     "label": lab if labelled else "", "uturn": uturn}
                if s["label"]:
                    lw = text_w(lab, F_EDGE) + 8
                    cx = (x0 + x1) / 2
                    cx = min(max(cx, MARGIN_L + lw / 2), self.W - MARGIN_R - lw / 2)
                    s.update(lcx=cx, lw=lw)
                    s["occ"] = (min(lo, cx - lw / 2) - 3, max(hi, cx + lw / 2) + 3)
                else:
                    s["occ"] = (lo - 3, hi + 3)
                self.hsegs.setdefault(ch, []).append(s)
                r["hs"].append(s)
        self.ch_n = [0] * (self.R + 1)

        def fits(s: dict, used: list[tuple[float, float]]) -> bool:
            return all(s["occ"][1] <= a or s["occ"][0] >= b for (a, b) in used)
        for ch in range(self.R + 1):
            # U-turns under a row take the top tracks, U-turns over a row the bottom tracks: short stubs
            segs = sorted(self.hsegs.get(ch, []), key=lambda s: ({"below": 0, None: 1, "above": 2}[s["uturn"]],
                                                                 s["occ"][0], s["route"]["e"]["idx"]))
            tracks: list[list[tuple[float, float]]] = []
            for s in segs:
                order = range(len(tracks) - 1, -1, -1) if s["uturn"] == "above" else range(len(tracks))
                for ti in order:
                    if fits(s, tracks[ti]):
                        tracks[ti].append(s["occ"])
                        s["t"] = ti
                        break
                else:
                    tracks.append([s["occ"]])
                    s["t"] = len(tracks) - 1
            self.ch_n[ch] = len(tracks)
        self.ch_h = []
        for ch, n in enumerate(self.ch_n):
            if n:
                self.ch_h.append(CH_PAD_T + (n - 1) * TRACK_H + CH_PAD_B)
            else:
                self.ch_h.append(4 if ch == 0 else (8 if ch == self.R else CH_EMPTY))

    def geometry_y(self) -> None:
        y = MARGIN_T
        self.ch_y, self.row_y = [], []
        for i in range(self.R + 1):
            self.ch_y.append(y)
            y += self.ch_h[i]
            if i < self.R:
                self.row_y.append(y)
                y += self.row_h[i]
        self.H = y + MARGIN_B
        self.node_box: dict[str, tuple[float, float, float, float]] = {}
        for nid in self.nodes:
            r = self.row_of[nid]
            x = self.col_x[self.col[nid]]
            yy = self.row_y[r] + self.cap_h[r]
            self.node_box[nid] = (x, yy, self.cw, self.nl[nid]["h"])       # natural height, tops aligned (V4)
        for r in self.routes:
            for s in r["hs"]:
                s["y"] = self.ch_y[s["ch"]] + CH_PAD_T + s["t"] * TRACK_H
            sx, sy, sw, sh = self.node_box[r["e"]["from"]]
            tx, ty, tw, th = self.node_box[r["e"]["to"]]
            if r["case"] == "side":
                y = sy + min(sh, th) / 2
                r["pts"] = [(sx + sw if r["s_side"] == "right" else sx, y),
                            (tx if r["t_side"] == "left" else tx + tw, y)]
                continue
            ys = sy + sh if r["s_side"] == "bottom" else sy
            yt = ty + th if r["t_side"] == "bottom" else ty
            xs, xt = r["sp"]["x"], r["tp"]["x"]
            if r["case"] in ("same", "down1", "up1"):
                h0 = r["hs"][0]["y"]
                r["pts"] = [(xs, ys), (xs, h0), (xt, h0), (xt, yt)]
            else:
                h1, h2 = r["hs"][0]["y"], r["hs"][1]["y"]
                r["pts"] = [(xs, ys), (xs, h1), (r["gx"], h1), (r["gx"], h2), (xt, h2), (xt, yt)]

    def _pass(self) -> None:
        self.warnings = []
        self.route()
        self.geometry_x()
        self.measure_nodes()
        self.captions()

    def layout(self) -> "Grid":
        self._pass()
        if self.p["avoid"] and self.wanted:      # second pass: route long lines around caption zones
            self.avoid = set(self.wanted)
            self._pass()
        self.channel_tracks()
        self.geometry_y()
        return self

    # ------------------------------------------------------------ render
    def svg(self) -> str:
        vid, W, H = self.v["id"], self.W, self.H
        o = [svg_open(vid, W, H, self.v["title"]), markers(vid)]
        o.append('<g class="sv-lanes">')
        lane_rows: dict[str, list[tuple[int, dict]]] = {}
        for r, segs in enumerate(self.rows):
            for seg in segs:
                lane_rows.setdefault(seg["lane"], []).append((r, seg))
        for lid, items in lane_rows.items():
            lane = self.lanes[lid]
            kind = lane.get("kind", "layer")
            xs0 = [self.col_x[s["c0"]] - 7 for _, s in items]
            xs1 = [self.col_x[s["c1"] - 1] + self.cw + 7 for _, s in items]
            r0, r1 = items[0][0], items[-1][0]
            y0, y1 = self.row_y[r0], self.row_y[r1] + self.row_h[r1]
            more = f"\n{lane['detail']}" if lane.get("detail") else ""
            tip = f"<title>{esc(lane['label'])}{esc(more)}\nLane kind: {esc(kind)}</title>"
            if kind == "boundary":
                o.append(f'<rect class="sv-bound" x="{f1(min(xs0))}" y="{f1(y0)}" width="{f1(max(xs1) - min(xs0))}" '
                         f'height="{f1(y1 - y0)}" rx="7">{tip}</rect>')
            else:
                for (r, s), a, b in zip(items, xs0, xs1):
                    o.append(f'<rect class="sv-band sv-b-{esc(kind)}" x="{f1(a)}" y="{f1(self.row_y[r])}" '
                             f'width="{f1(b - a)}" height="{f1(self.row_h[r])}" rx="6">{tip}</rect>')
            o.append(f'<rect class="sv-acc sv-a-{esc(kind)}" x="{f1(min(xs0))}" y="{f1(y0 + 2)}" width="3" '
                     f'height="{f1(y1 - y0 - 4)}" rx="1.5"/>')
        o.append('</g><g class="sv-groups">')
        for p in self.perimeters:
            y0 = self.row_y[p["r0"]] - 5
            y1 = self.row_y[p["r1"]] + self.row_h[p["r1"]] + 5
            o.append(f'<rect class="sv-perim" x="7" y="{f1(y0)}" width="{f1(W - 14)}" height="{f1(y1 - y0)}" rx="10">'
                     f'<title>{esc(group_tooltip(p["g"]))}</title></rect>')
        for b in self.boxes:
            bx = [self.node_box[n] for n in b["g"]["nodes"]]
            x0 = min(q[0] for q in bx) - 5
            x1 = max(q[0] + q[2] for q in bx) + 5
            y0 = min(q[1] for q in bx) - 5
            y1 = max(q[1] + q[3] for q in bx) + 5
            b["rect"] = (x0, y0, x1 - x0, y1 - y0)
            o.append(f'<rect class="sv-tb" x="{f1(x0)}" y="{f1(y0)}" width="{f1(x1 - x0)}" height="{f1(y1 - y0)}" rx="8">'
                     f'<title>{esc(group_tooltip(b["g"]))}</title></rect>')
        o.append('</g><g class="sv-edges">')
        for r in self.routes:
            o.append(edge_svg(vid, r["e"], rounded_path(r["pts"]), self.nodes))
        o.append('</g><g class="sv-nodes">')
        for nid, n in self.nodes.items():
            o.append(node_svg(vid, n, self.node_box[nid], self.nl[nid], self.meta))
        o.append('</g><g class="sv-elabels">')
        for r in self.routes:
            if r["hs"] and r["hs"][0]["label"]:
                s = r["hs"][0]
                o.append(edge_label_svg(vid, r["e"], s["lcx"], s["y"] - 4, self.nodes))
        o.append('</g><g class="sv-captions">')
        for r in range(self.R):
            halo = self.lanes[self.rows[r][0]["lane"]].get("kind", "layer")
            for it in self.cap_items[r]:
                for j, t in enumerate(it["lines"]):
                    yb = self.row_y[r] + 4 + (it["line"] + j + 1) * LH_CAPTION - 3.5
                    k = it["lane"].get("kind", "layer") if it["kind"] == "lane" else halo
                    w = text_w(t, F_LANE if it["kind"] == "lane" else F_GROUP, True)
                    x0 = it["x"] - (w if it["anchor"] == "end" else 0)
                    o.append(f'<rect class="sv-capbg sv-cb-{esc(k)}" x="{f1(x0 - 3)}" y="{f1(yb - 10.5)}" '
                             f'width="{f1(w + 6)}" height="14" rx="3"/>')
                    if it["kind"] == "lane":
                        o.append(f'<text class="sv-cap sv-h-{esc(k)}" x="{f1(it["x"])}" y="{f1(yb)}">{esc(t)}</text>')
                    else:
                        o.append(f'<text class="sv-gl sv-h-{esc(halo)}" x="{f1(it["x"])}" y="{f1(yb)}" '
                                 f'text-anchor="{it["anchor"]}"><title>{esc(group_tooltip(it["g"]))}</title>'
                                 f'{esc(t)}</text>')
        o.append('</g></svg>')
        return "".join(o)

    # -------------------------------------------------------- self-check
    def check(self) -> list[str]:
        issues = list(self.warnings)
        nb = list(self.node_box.items())
        rects = [("node " + k, b) for k, b in nb]
        for r in self.routes:
            s = r["hs"][0] if r["hs"] else None
            if s and s["label"]:
                rects.append((f"label {r['e']['from']}->{r['e']['to']}",
                              (s["lcx"] - s["lw"] / 2 + 3, s["y"] - 4 - 9.5, s["lw"] - 6, 12.5)))
        for r in range(self.R):
            for it in self.cap_items[r]:
                for j, t in enumerate(it["lines"]):
                    yb = self.row_y[r] + 4 + (it["line"] + j + 1) * LH_CAPTION - 3.5
                    bold = True
                    w = text_w(t, F_LANE if it["kind"] == "lane" else F_GROUP, bold)
                    x0 = it["x"] - (w if it["anchor"] == "end" else 0)
                    rects.append((f"caption {t[:24]}", (x0, yb - 10, w, 13)))
        issues += overlap_issues(rects)
        issues += segment_issues(self.routes, self.node_box)
        if self.W > TARGET_W + 0.5:
            issues.append(f"width {self.W:.0f} exceeds target {TARGET_W}")
        return issues


# ------------------------------------------------------- shared SVG pieces
EDGE_KINDS = ["data", "control", "price", "evidence", "decision", "feedback", "guard"]
NODE_RX = {"deterministic": 3, "agentic": 13, "human": 7, "store": 3, "external": 3, "boundary_note": 2}


def svg_open(vid: str, W: float, H: float, title: str) -> str:
    return (f'<svg class="sv" id="svg-{esc(vid)}" viewBox="0 0 {f1(W)} {f1(H)}" width="100%" '
            f'style="min-width:{math.ceil(W)}px" role="group" aria-label="{esc(title)}">')


def markers(vid: str) -> str:
    m = ["<defs>"]
    for k in EDGE_KINDS:
        size = 7 if k == "guard" else 8.5
        m.append(f'<marker id="{esc(vid)}-ah-{k}" viewBox="0 0 10 10" refX="9.6" refY="5" '
                 f'markerWidth="{size}" markerHeight="{size}" markerUnits="userSpaceOnUse" orient="auto">'
                 f'<path d="M0,0.6 L10,5 L0,9.4 z" class="sv-ah sv-f-{k}"/></marker>')
    m.append("</defs>")
    return "".join(m)


def edge_svg(vid: str, e: dict, d: str, nodes: dict) -> str:
    k = e["kind"]
    ra = " sv-ra" if e.get("badge") else ""
    s = [f'<g class="sv-edge sv-e-{k}{ra}" data-edge="{esc(vid)}-e{e["idx"]}" data-from="{esc(e["from"])}" '
         f'data-to="{esc(e["to"])}"><title>{esc(edge_tooltip(e, nodes))}</title>',
         f'<path class="sv-hit" d="{d}"/>']
    if ra:
        s.append(f'<path class="sv-rahalo" d="{d}"/>')
    s.append(f'<path class="sv-line" d="{d}" marker-end="url(#{esc(vid)}-ah-{k})"/></g>')
    return "".join(s)


def edge_label_svg(vid: str, e: dict, x: float, y: float, nodes: dict,
                   lines: list[str] | None = None, ys: list[float] | None = None) -> str:
    """Edge label as a small opaque tag (rect + text) so crossing lines pass underneath it."""
    lines = lines if lines is not None else [e["label"]]
    ys = ys if ys is not None else [y]
    s = [f'<g class="sv-elg sv-lk-{e["kind"]}" data-edge="{esc(vid)}-e{e["idx"]}">'
         f'<title>{esc(edge_tooltip(e, nodes))}</title>']
    for t, yb in zip(lines, ys):
        w = text_w(t, F_EDGE) + 4
        s.append(f'<rect class="sv-elbg" x="{f1(x - w / 2)}" y="{f1(yb - 10)}" width="{f1(w)}" height="13.5" rx="3"/>')
    for t, yb in zip(lines, ys):
        s.append(f'<text class="sv-el sv-t-{e["kind"]}" x="{f1(x)}" y="{f1(yb)}" text-anchor="middle">{esc(t)}</text>')
    s.append("</g>")
    return "".join(s)


def badge_strip(x: float, y: float, w: float, h: float, lines: list[str]) -> tuple[str, float]:
    """Returns svg for a badge strip placed at the bottom of a box, and its height."""
    sh = len(lines) * LH_BADGE + 6
    sy = y + h - 3 - sh
    s = [f'<rect class="sv-badge" x="{f1(x + 3)}" y="{f1(sy)}" width="{f1(w - 6)}" height="{f1(sh)}" rx="3"/>']
    for i, line in enumerate(lines):
        s.append(f'<text class="sv-bt" x="{f1(x + 7)}" y="{f1(sy + 3 + (i + 1) * LH_BADGE - 3.2)}">{esc(line)}</text>')
    return "".join(s), sh


def box_shape(k: str, x: float, y: float, w: float, h: float) -> str:
    s = [f'<rect class="sv-box" x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{NODE_RX[k]}"/>']
    if k == "store":
        s.append(f'<path class="sv-lid" d="M{f1(x + 3)},{f1(y + 5.5)}H{f1(x + w - 3)}"/>')
    if k == "external":
        s.append(f'<rect class="sv-inner" x="{f1(x + 3)}" y="{f1(y + 3)}" width="{f1(w - 6)}" '
                 f'height="{f1(h - 6)}" rx="1.5"/>')
    return "".join(s)


def node_attrs(vid: str, n: dict) -> str:
    """Keyboard and touch access (V10): every box is focusable and describes itself in the details panel."""
    name = n["label"] + (f" (Real Assets: {n['badge']})" if n.get("badge") else "")
    return (f'data-node="{esc(n["id"])}" tabindex="0" role="button" aria-label="{esc(name)}" '
            f'aria-describedby="det-{esc(vid)}"')


def node_svg(vid: str, n: dict, box: tuple, nl: dict, meta: dict) -> str:
    x, y, w, h = box
    k = n["kind"]
    ra = " sv-ra" if n.get("badge") else ""
    s = [f'<g class="sv-node sv-n-{k}{ra}" {node_attrs(vid, n)}><title>{esc(node_tooltip(n, meta))}</title>',
         box_shape(k, x, y, w, h)]
    tx = x + NODE_PAD_X
    for i, line in enumerate(nl["L"]):
        s.append(f'<text class="sv-nl" x="{f1(tx)}" y="{f1(y + NODE_PAD_T + (i + 1) * LH_LABEL - 3.6)}">{esc(line)}</text>')
    y0 = y + NODE_PAD_T + len(nl["L"]) * LH_LABEL + 2
    for j, line in enumerate(nl["S"]):
        s.append(f'<text class="sv-ns" x="{f1(tx)}" y="{f1(y0 + (j + 1) * LH_SUB - 3.4)}">{esc(line)}</text>')
    if nl["B"]:
        s.append(badge_strip(x, y, w, h, nl["B"])[0])
    s.append("</g>")
    return "".join(s)


def count_crossings(routes: list[dict]) -> int:
    """Crossings between orthogonal segments of different edges (the QA checker's definition)."""
    hs, vs = [], []
    for i, r in enumerate(routes):
        for (x0, y0), (x1, y1) in zip(r["pts"], r["pts"][1:]):
            if abs(y0 - y1) < 0.05 and abs(x0 - x1) > 0.05:
                hs.append((y0, min(x0, x1), max(x0, x1), i))
            elif abs(x0 - x1) < 0.05 and abs(y0 - y1) > 0.05:
                vs.append((x0, min(y0, y1), max(y0, y1), i))
    vs.sort()
    xs = [v[0] for v in vs]
    n = 0
    for y, a, b, i in hs:
        for k in range(bisect.bisect_right(xs, a + 0.5), bisect.bisect_left(xs, b - 0.5)):
            x, y0, y1, j = vs[k]
            if j != i and y0 + 0.5 < y < y1 - 0.5:
                n += 1
    return n


def overlap_issues(rects: list[tuple[str, tuple]]) -> list[str]:
    out = []
    for i in range(len(rects)):
        ni, (ax, ay, aw, ah) = rects[i]
        for j in range(i + 1, len(rects)):
            nj, (bx, by, bw, bh) = rects[j]
            ox = min(ax + aw, bx + bw) - max(ax, bx)
            oy = min(ay + ah, by + bh) - max(ay, by)
            if ox > 1.0 and oy > 1.0:
                out.append(f"overlap: {ni} / {nj} ({ox:.0f}x{oy:.0f}px)")
    return out


def segment_issues(routes: list[dict], boxes: dict) -> list[str]:
    V, Hz = [], []
    for r in routes:
        pts, i = r["pts"], r["e"]["idx"]
        for a, b in zip(pts, pts[1:]):
            if abs(a[0] - b[0]) < 0.01 and abs(a[1] - b[1]) > 0.01:
                V.append((a[0], min(a[1], b[1]), max(a[1], b[1]), i))
            elif abs(a[1] - b[1]) < 0.01 and abs(a[0] - b[0]) > 0.01:
                Hz.append((a[1], min(a[0], b[0]), max(a[0], b[0]), i))
    out = []
    for segs, name in ((V, "vertical"), (Hz, "horizontal")):
        segs.sort()
        for p in range(len(segs)):
            for q in range(p + 1, len(segs)):
                if segs[q][0] - segs[p][0] > 0.75:
                    break
                if segs[p][3] != segs[q][3] and min(segs[p][2], segs[q][2]) - max(segs[p][1], segs[q][1]) > 1:
                    out.append(f"collinear {name} overlap: edges {segs[p][3]} and {segs[q][3]}")
    for x, y0, y1, i in V:
        for nid, (bx, by, bw, bh) in boxes.items():
            if bx + 0.5 < x < bx + bw - 0.5 and min(y1, by + bh) - max(y0, by) > 1.5:
                out.append(f"edge {i} crosses box {nid}")
    for y, x0, x1, i in Hz:
        for nid, (bx, by, bw, bh) in boxes.items():
            if by + 0.5 < y < by + bh - 0.5 and min(x1, bx + bw) - max(x0, bx) > 1.5:
                out.append(f"edge {i} crosses box {nid}")
    return out


# ------------------------------------------------------------ timeline view
GATE_RE = re.compile(r"^G\d")


class Timeline:
    """Quarterly cycle: steps alternate above/below a time axis; other links run as arcs below."""

    LOOP_W = 66      # space kept right of the last step for the monthly loop
    SEQ_GAP = 44     # axis to box distance (room for two lines of sequence labels)

    def __init__(self, view: dict, meta: dict):
        self.v, self.meta = view, meta
        self.nodes = {n["id"]: n for n in view["nodes"]}
        self.lanes = {l["id"]: l for l in view["lanes"]}
        self.edges = [dict(e, idx=i) for i, e in enumerate(view["edges"])]
        self.steps = sorted((n for n in view["nodes"] if "seq" in n), key=lambda n: n["seq"])
        self.off = sorted((n for n in view["nodes"] if "seq" not in n), key=lambda n: n.get("order", 0))
        self.idx = {n["id"]: i for i, n in enumerate(self.steps)}
        self.warnings: list[str] = []
        self.badge = meta["badge_text"]

    # --------------------------------------------------------- content
    @staticmethod
    def title_of(n: dict) -> str:
        t = n["label"]
        day = n.get("day", "")
        for prefix in (day, day.replace(" to ", "…")):
            if prefix and t.startswith(prefix):
                t = t[len(prefix):].strip()
        t = re.sub(r"\s*·\s*G\d.*$", "", t)
        return t

    def box_lines(self, n: dict, w: float) -> dict:
        inner = w - 2 * NODE_PAD_X
        day = n.get("day", "")
        D = wrap(day.replace(" to ", " – "), 12.5, inner, bold=True) if day else []
        T = wrap(self.title_of(n) if day else n["label"], 12.0, inner, bold=True)
        prod = n.get("produces") or n.get("sublabel", "")
        P = wrap(("→ " + prod) if n.get("produces") else prod, F_SUB, inner)
        gate = n.get("gate", "")
        G = wrap(f"check: {gate}", F_SUB, inner) if gate and gate != "—" and not GATE_RE.match(gate) else []
        B = wrap(self.badge, F_BADGE, inner - 8) if n.get("badge") else []
        h = NODE_PAD_T + len(D) * 15 + len(T) * 14.5 + 2 + len(P) * LH_SUB + len(G) * LH_SUB + 14 + NODE_PAD_B - 2
        if B:
            h += 4 + len(B) * LH_BADGE + 6
        return {"D": D, "T": T, "P": P, "G": G, "B": B, "h": h}

    # ---------------------------------------------------------- layout
    def layout(self) -> "Timeline":
        N = len(self.steps)
        W = TARGET_W
        # x0 - (dx - 8) >= MARGIN_L ; x_{N-1} + (dx - 8) + LOOP_W <= W - MARGIN_R
        dx = (W - MARGIN_L - MARGIN_R - self.LOOP_W + 12) / (N + 1)
        self.dx, self.bw = dx, 2 * dx - 12
        x0 = MARGIN_L + dx - 6
        self.x = [x0 + i * dx for i in range(N)]
        self.W = W
        for i, n in enumerate(self.steps):
            n["_side"] = "top" if i % 2 == 0 else "bottom"
        self.lines = {n["id"]: self.box_lines(n, self.bw) for n in self.steps}
        self.off_w = min(2 * self.bw, 230)
        for n in self.off:
            self.lines[n["id"]] = self.box_lines(n, self.off_w)
        top_h = max(self.lines[n["id"]]["h"] for n in self.steps if n["_side"] == "top")
        bot_h = max(self.lines[n["id"]]["h"] for n in self.steps if n["_side"] == "bottom")
        # phases
        self.phases = []
        for lid, lane in self.lanes.items():
            mem = [self.idx[n["id"]] for n in self.steps if n["lane"] == lid]
            if not mem:
                continue
            i0, i1 = min(mem), max(mem)
            left = (self.x[i0 - 1] + self.x[i0]) / 2 + 4 if i0 > 0 else self.x[0] - dx + 6
            right = (self.x[i1] + self.x[i1 + 1]) / 2 - 4 if i1 < N - 1 else self.x[-1] + dx - 6
            lines = wrap(lane["label"], F_GROUP, right - left + 12, bold=True)
            self.phases.append({"lane": lane, "l": left, "r": right, "lines": lines})
        ph_lines = max(len(p["lines"]) for p in self.phases)
        y = MARGIN_T + 6
        self.ph_text_y = y
        self.ph_y = y + ph_lines * LH_CAPTION + 6
        self.top_y = self.ph_y + 12
        self.top_h = top_h
        self.axis_y = self.top_y + top_h + self.SEQ_GAP
        self.bot_y = self.axis_y + self.SEQ_GAP + 2
        self.bot_h = bot_h
        self.box: dict[str, tuple] = {}
        for i, n in enumerate(self.steps):
            bx = self.x[i] - self.bw / 2
            self.box[n["id"]] = (bx, self.top_y if n["_side"] == "top" else self.bot_y, self.bw,
                                 top_h if n["_side"] == "top" else bot_h)
        self._route_arcs()
        return self

    def _anchor(self, nid: str, end: str) -> dict:
        """Where an arc attaches: bottom of a lower box, the axis under an upper box, or an off-cycle box top."""
        if nid in self.idx:
            i = self.idx[nid]
            n = self.steps[i]
            if n["_side"] == "bottom":
                bx, by, bw, bh = self.box[nid]
                return {"x": self.x[i], "y": by + bh, "dir": "down", "key": (nid, "b")}
            kind, _, _ = self._chip(n)                     # meet the tick itself (V9): chip 18px, IC dot r 6, else 4.5
            half = 9.0 if kind == "chip" else (6.0 if n.get("day") == "T" else 4.5)
            return {"x": self.x[i], "y": self.axis_y + half + 1, "dir": "down", "key": (nid, "a")}
        return {"x": None, "y": None, "dir": "up", "key": (nid, "o")}

    def _route_arcs(self) -> None:
        self.seq, self.arcs = [], []
        for e in self.edges:
            a, b = e["from"], e["to"]
            if a in self.idx and b in self.idx and self.idx[b] == self.idx[a] + 1:
                self.seq.append(e)
            else:
                self.arcs.append({"e": e})
        # off-cycle boxes: centre near the median x of their partners, then pack left to right
        want = []
        for n in self.off:
            xs = []
            for r in self.arcs:
                e = r["e"]
                other = e["to"] if e["from"] == n["id"] else (e["from"] if e["to"] == n["id"] else None)
                if other in self.idx:
                    xs.append(self.x[self.idx[other]])
            xs.sort()
            want.append(xs[len(xs) // 2] if xs else self.W / 2)
        order = sorted(range(len(self.off)), key=lambda k: want[k])
        placed, last_r = {}, MARGIN_L - 12
        for k in order:
            cx = max(want[k], last_r + 12 + self.off_w / 2)
            cx = min(cx, self.W - MARGIN_R - self.off_w / 2)
            placed[k] = cx
            last_r = cx + self.off_w / 2
        self.off_cx = {self.off[k]["id"]: placed[k] for k in placed}
        # ports: spread several arcs at one anchor
        anchors: dict[tuple, list] = {}
        for r in self.arcs:
            for end in ("s", "t"):
                nid = r["e"]["from" if end == "s" else "to"]
                an = self._anchor(nid, end)
                if an["x"] is None:
                    an["x"] = self.off_cx[nid]
                r[end] = an
                anchors.setdefault(an["key"], []).append((r, end))
        for key, items in anchors.items():
            def other_x(it):
                r, end = it
                return r["t" if end == "s" else "s"]["x"]
            items.sort(key=lambda it: (other_x(it), it[0]["e"]["idx"]))
            m = len(items)
            spread = 4.0 if key[1] == "a" else (min(14.0, self.bw / (m + 1)) if key[1] == "b" else 30.0)
            for k, (r, end) in enumerate(items):
                r[end]["x"] += (k - (m - 1) / 2) * spread
        # tracks in the arc band
        segs = []
        for r in self.arcs:
            lo, hi = sorted((r["s"]["x"], r["t"]["x"]))
            lab = r["e"].get("label", "")
            lw = text_w(lab, F_EDGE) + 8 if lab else 0
            cx = min(max((lo + hi) / 2, MARGIN_L + lw / 2), self.W - MARGIN_R - lw / 2)
            r.update(lo=lo, hi=hi, lw=lw, lcx=cx, occ=(min(lo, cx - lw / 2) - 3, max(hi, cx + lw / 2) + 3))
            segs.append(r)
        segs.sort(key=lambda r: (r["occ"][0], r["e"]["idx"]))
        tracks: list[list[tuple]] = []
        for r in segs:
            for ti, used in enumerate(tracks):
                if all(r["occ"][1] <= a or r["occ"][0] >= b for (a, b) in used):
                    used.append(r["occ"])
                    r["trk"] = ti
                    break
            else:
                tracks.append([r["occ"]])
                r["trk"] = len(tracks) - 1
        self.band_y = self.bot_y + self.bot_h + 4
        self.n_tracks = len(tracks)
        band_h = CH_PAD_T + max(0, self.n_tracks - 1) * TRACK_H + CH_PAD_B
        self.off_cap_y = self.band_y + band_h + 4
        self.off_y = self.off_cap_y + LH_CAPTION + 6
        off_h = max((self.lines[n["id"]]["h"] for n in self.off), default=0)
        self.off_h = off_h
        for n in self.off:
            cx = self.off_cx[n["id"]]
            self.box[n["id"]] = (cx - self.off_w / 2, self.off_y, self.off_w, off_h)
        for r in self.arcs:
            ty = self.band_y + CH_PAD_T + r["trk"] * TRACK_H
            r["y"] = ty
            pts = []
            for end in ("s", "t"):
                an = r[end]
                nid = r["e"]["from" if end == "s" else "to"]
                ay = an["y"] if an["y"] is not None else self.off_y
                if an["key"][1] == "o":
                    ay = self.box[nid][1]
                if end == "s":
                    pts += [(an["x"], ay), (an["x"], ty)]
                else:
                    pts += [(an["x"], ty), (an["x"], ay)]
            r["pts"] = pts
        self.H = self.off_y + off_h + MARGIN_B + 4

    # ---------------------------------------------------------- render
    def _chip(self, n: dict) -> tuple[str, float, str]:
        gate = n.get("gate", "")
        if gate and GATE_RE.match(gate):
            return "chip", text_w(gate, F_EDGE, True) + 12, gate
        if gate and gate != "—":
            return "check", 9.0, gate
        return "dot", 9.0, ""

    def _seq_labels(self) -> list[dict]:
        out = []
        for e in self.seq:
            i = self.idx[e["from"]]
            if not e.get("label"):
                continue
            lines = wrap(e["label"], F_EDGE, 2 * self.dx - 14)
            mid = (self.x[i] + self.x[i + 1]) / 2
            above = i % 2 == 0
            ys = ([self.axis_y - 14 - (len(lines) - 1 - j) * LH_SUB for j in range(len(lines))] if above
                  else [self.axis_y + 23 + j * LH_SUB for j in range(len(lines))])
            out.append({"e": e, "x": mid, "lines": lines, "ys": ys})
        return out

    def svg(self) -> str:
        vid, W, H = self.v["id"], self.W, self.H
        o = [svg_open(vid, W, H, self.v["title"]), markers(vid), '<g class="sv-phases">']
        for p in self.phases:
            l, r, y = p["l"], p["r"], self.ph_y
            tip = f"<title>{esc(p['lane']['label'])}\nSection: §3.6</title>"
            o.append(f'<path class="sv-phase" d="M{f1(l)},{f1(y + 6)}V{f1(y)}H{f1(r)}V{f1(y + 6)}">{tip}</path>')
            n = len(p["lines"])
            for j, t in enumerate(p["lines"]):
                yb = y - 5 - (n - 1 - j) * LH_CAPTION
                o.append(f'<text class="sv-cap sv-ph sv-h-none" x="{f1((l + r) / 2)}" y="{f1(yb)}" '
                         f'text-anchor="middle">{tip}{esc(t)}</text>')
        o.append('</g><g class="sv-conns">')
        for i, n in enumerate(self.steps):
            x = self.x[i]
            if n["_side"] == "top":
                o.append(f'<path class="sv-conn" d="M{f1(x)},{f1(self.top_y + self.top_h)}V{f1(self.axis_y - 9)}"/>')
            else:
                o.append(f'<path class="sv-conn" d="M{f1(x)},{f1(self.axis_y + 9)}V{f1(self.bot_y)}"/>')
        o.append('</g><g class="sv-edges">')
        half = {}
        for i, n in enumerate(self.steps):
            kind, w, _ = self._chip(n)
            half[i] = w / 2 if kind == "chip" else 6
        for e in self.seq:
            i = self.idx[e["from"]]
            x0, x1 = self.x[i] + half[i] + 2, self.x[i + 1] - half[i + 1] - 2
            o.append(edge_svg(vid, e, f"M{f1(x0)},{f1(self.axis_y)}H{f1(x1)}", self.nodes))
        for r in self.arcs:
            o.append(edge_svg(vid, r["e"], rounded_path(r["pts"]), self.nodes))
        last = self.steps[-1]
        bx, by, bw, bh = self.box[last["id"]]
        x1, y1, y2 = bx + bw, by + bh * 0.30, by + bh * 0.70
        o.append(f'<g class="sv-edge sv-e-feedback"><title>Monthly loop\nSignpost monitor, CFP readings and event '
                 f'decisions repeat every month\nKind: feedback\nSection: §3.6; §8.9</title>'
                 f'<path class="sv-line" d="M{f1(x1)},{f1(y1)}'
                 f'C{f1(x1 + 52)},{f1(y1 - 8)} {f1(x1 + 52)},{f1(y2 + 8)} {f1(x1 + 1)},{f1(y2)}" '
                 f'marker-end="url(#{esc(vid)}-ah-feedback)"/></g>')
        o.append(f'<text class="sv-el sv-loop-l sv-t-feedback sv-lk-feedback" x="{f1(x1 + 6)}" y="{f1(y1 - 10)}">'
                 f'monthly</text>')
        o.append('</g><g class="sv-ticks">')
        for i, n in enumerate(self.steps):
            kind, w, gate = self._chip(n)
            x, y = self.x[i], self.axis_y
            tip = f"<title>{esc(n.get('day', ''))}: gate {esc(n.get('gate', '—'))} (§7.6; §3.6)</title>"
            if kind == "chip":
                o.append(f'<g class="sv-chip">{tip}<rect x="{f1(x - w / 2)}" y="{f1(y - 9)}" width="{f1(w)}" '
                         f'height="18" rx="9"/><text x="{f1(x)}" y="{f1(y + 4)}" text-anchor="middle">{esc(gate)}</text></g>')
            elif kind == "check":
                o.append(f'<rect class="sv-check" x="{f1(x - 4.5)}" y="{f1(y - 4.5)}" width="9" height="9">{tip}</rect>')
            else:
                cls = "sv-dot sv-dot-ic" if n.get("day") == "T" else "sv-dot"
                rr = 6 if n.get("day") == "T" else 4.5
                o.append(f'<circle class="{cls}" cx="{f1(x)}" cy="{f1(y)}" r="{rr}">{tip}</circle>')
        o.append('</g><g class="sv-nodes">')
        for n in self.steps + self.off:
            o.append(self._box_svg(n))
        o.append('</g><g class="sv-elabels">')
        for sl in self._seq_labels():
            o.append(edge_label_svg(vid, sl["e"], sl["x"], 0, self.nodes, sl["lines"], sl["ys"]))
        for r in self.arcs:
            if r["e"].get("label"):
                o.append(edge_label_svg(vid, r["e"], r["lcx"], r["y"] - 4, self.nodes))
        off_lane = next((self.lanes[n["lane"]] for n in self.off), None)
        if off_lane:
            o.append(f'<text class="sv-cap sv-h-none" x="{MARGIN_L + 2}" y="{f1(self.off_cap_y + 11)}">'
                     f'{esc(off_lane["label"])}</text>')
        o.append("</g></svg>")
        return "".join(o)

    def _box_svg(self, n: dict) -> str:
        x, y, w, h = self.box[n["id"]]
        L = self.lines[n["id"]]
        k = n["kind"]
        ra = " sv-ra" if n.get("badge") else ""
        s = [f'<g class="sv-node sv-n-{k}{ra}" {node_attrs(self.v["id"], n)}>'
             f'<title>{esc(node_tooltip(n, self.meta))}</title>', box_shape(k, x, y, w, h)]
        tx, cy = x + NODE_PAD_X, y + NODE_PAD_T
        for t in L["D"]:
            s.append(f'<text class="sv-nd" x="{f1(tx)}" y="{f1(cy + 15 - 3.6)}">{esc(t)}</text>')
            cy += 15
        for t in L["T"]:
            s.append(f'<text class="sv-nl" x="{f1(tx)}" y="{f1(cy + 14.5 - 3.6)}">{esc(t)}</text>')
            cy += 14.5
        cy += 2
        for t in L["P"] + L["G"]:
            cls = "sv-ns sv-it" if t in L["G"] else "sv-ns"
            s.append(f'<text class="{cls}" x="{f1(tx)}" y="{f1(cy + LH_SUB - 3.4)}">{esc(t)}</text>')
            cy += LH_SUB
        mx = tx + 4
        my = cy + 7
        for a in n.get("actors", []):
            if a == "human":
                s.append(f'<path class="sv-mk sv-mk-human" d="M{f1(mx)},{f1(my - 5)}L{f1(mx + 5)},{f1(my)}'
                         f'L{f1(mx)},{f1(my + 5)}L{f1(mx - 5)},{f1(my)}Z"/>')
            elif a == "agentic":
                s.append(f'<circle class="sv-mk sv-mk-agentic" cx="{f1(mx)}" cy="{f1(my)}" r="4.5"/>')
            else:
                s.append(f'<rect class="sv-mk sv-mk-deterministic" x="{f1(mx - 4.2)}" y="{f1(my - 4.2)}" '
                         f'width="8.4" height="8.4" rx="1"/>')
            mx += 15
        if L["B"]:
            s.append(badge_strip(x, y, w, h, L["B"])[0])
        s.append("</g>")
        return "".join(s)

    def check(self) -> list[str]:
        issues = list(self.warnings)
        rects = [("box " + k, b) for k, b in self.box.items()]
        for sl in self._seq_labels():
            for t, yb in zip(sl["lines"], sl["ys"]):
                w = text_w(t, F_EDGE)
                rects.append((f"seq label {t}", (sl["x"] - w / 2, yb - 9.5, w, 12.5)))
        for r in self.arcs:
            if r["e"].get("label"):
                rects.append((f"arc label {r['e']['label']}", (r["lcx"] - r["lw"] / 2 + 3, r["y"] - 13.5, r["lw"] - 6, 12.5)))
        for i, n in enumerate(self.steps):
            kind, w, _ = self._chip(n)
            rects.append((f"tick {n['id']}", (self.x[i] - w / 2, self.axis_y - 9, w, 18)))
        for p in self.phases:
            n = len(p["lines"])
            for j, t in enumerate(p["lines"]):
                w = text_w(t, F_GROUP, True)
                yb = self.ph_y - 5 - (n - 1 - j) * LH_CAPTION
                rects.append((f"phase {t}", ((p["l"] + p["r"]) / 2 - w / 2, yb - 10, w, 13)))
        issues += overlap_issues(rects)
        issues += segment_issues([{"pts": r["pts"], "e": r["e"]} for r in self.arcs], self.box)
        for i, n in enumerate(self.steps):
            L = self.lines[n["id"]]
            if L["h"] > self.box[n["id"]][3] + 0.5:
                issues.append(f"box {n['id']} content taller than box")
        return issues


# ------------------------------------------------------------------- page
LIGHT = """
  --bg:#ffffff; --panel:#f6f7f9; --ink:#1b2129; --ink-2:#465160; --ink-3:#6b7480; --rule:#d8dde4;
  --accent:#0b5cad; --tab:#eef1f5; --tab-on:#ffffff;
  --n-det:#0072b2; --n-det-f:#e8f2fa; --n-agt:#b36800; --n-agt-f:#fdf1df;
  --n-hum:#a0457c; --n-hum-f:#f8ebf3; --n-sto:#00785a; --n-sto-f:#e4f4ee;
  --n-ext:#5d6875; --n-ext-f:#eef1f4; --n-note:#7d6f00; --n-note-f:#fbf8dc;
  --ra:#b8a600; --ra-f:#fbf2a4; --ra-ink:#433c00; --ra-halo:rgba(240,228,66,.38);
  --e-data:#4b5563; --e-control:#0072b2; --e-price:#d55e00; --e-evidence:#009e73;
  --e-decision:#a0457c; --e-feedback:#b07a00; --e-guard:#6b7480;
  --t-data:#374151; --t-control:#005a8c; --t-price:#a84300; --t-evidence:#00664d;
  --t-decision:#8e3a6c; --t-feedback:#7a5400; --t-guard:#5c6670;
  --band-plane:#f6eff7; --band-layer:#f3f5f8; --band-actor_group:#f4f5f2; --band-phase:#f3f5f8;
  --acc-plane:#a0457c; --acc-layer:#98a3b0; --acc-actor_group:#a3a797; --acc-phase:#98a3b0; --acc-boundary:#7d8794;
  --bound:#7d8794; --tb:#b03030; --conn:#a9b1bc; --chip:#1b2129; --chip-ink:#ffffff;"""

DARK = """
  --bg:#0f141a; --panel:#151b23; --ink:#e7eaef; --ink-2:#b7c0cb; --ink-3:#8e98a5; --rule:#2b333e;
  --accent:#6cb6ff; --tab:#18202a; --tab-on:#0f141a;
  --n-det:#56b4e9; --n-det-f:#10283b; --n-agt:#e69f00; --n-agt-f:#33240a;
  --n-hum:#dc8fbd; --n-hum-f:#331d2b; --n-sto:#2bbf94; --n-sto-f:#0c2d25;
  --n-ext:#9aa5b4; --n-ext-f:#1c222a; --n-note:#e2d14a; --n-note-f:#29270f;
  --ra:#e2d14a; --ra-f:#39340d; --ra-ink:#f6ee9e; --ra-halo:rgba(240,228,66,.28);
  --e-data:#a3adba; --e-control:#56b4e9; --e-price:#f07c3a; --e-evidence:#34c79a;
  --e-decision:#dc8fbd; --e-feedback:#e3a830; --e-guard:#738090;
  --t-data:#c6ccd5; --t-control:#86c8f0; --t-price:#f9a066; --t-evidence:#63d6b0;
  --t-decision:#e8a9cf; --t-feedback:#efc265; --t-guard:#a0a9b4;
  --band-plane:#1d1722; --band-layer:#151b22; --band-actor_group:#171b1f; --band-phase:#151b22;
  --acc-plane:#dc8fbd; --acc-layer:#5d6876; --acc-actor_group:#646a5c; --acc-phase:#5d6876; --acc-boundary:#6b7583;
  --bound:#5f6977; --tb:#f19292; --conn:#4f5966; --chip:#e7eaef; --chip-ink:#0f141a;"""

CSS = """
:root{--font:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif;
  color-scheme:light;%LIGHT%}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;%DARK%}}
:root[data-theme="dark"]{color-scheme:dark;%DARK%}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--font);font-size:15px;line-height:1.5}
.wrap{max-width:1440px;margin:0 auto;padding:0 16px 40px}
.top{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:flex-start;justify-content:space-between;
  padding:18px 0 12px;border-bottom:1px solid var(--rule)}
.top h1{margin:0;font-size:26px;line-height:1.2;letter-spacing:-.01em}
.top p{margin:4px 0 0;color:var(--ink-2);font-size:14px;max-width:980px}
.top .src code{font-size:13px}
.ra-line{display:flex;gap:8px;align-items:baseline}
.ra-chip{display:inline-block;background:var(--ra-f);color:var(--ra-ink);border:1px solid var(--ra);
  border-radius:4px;padding:0 6px;font-size:12px;font-weight:700;white-space:nowrap}
.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.syn{font-size:12px;font-weight:700;letter-spacing:.04em;color:var(--ink-2);border:1px dashed var(--ink-3);
  border-radius:4px;padding:2px 8px;white-space:nowrap}
button{font:inherit}
#theme{font-size:13px;padding:6px 12px;border-radius:6px;border:1px solid var(--rule);background:var(--panel);
  color:var(--ink);cursor:pointer}
#theme:hover{border-color:var(--ink-3)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.tabs{display:flex;flex-wrap:wrap;gap:4px;margin:14px 0 0;border-bottom:1px solid var(--rule)}
.tabs [role=tab]{border:1px solid var(--rule);border-bottom:none;background:var(--tab);color:var(--ink-2);
  padding:8px 14px;border-radius:7px 7px 0 0;cursor:pointer;font-size:14px;margin-bottom:-1px}
.tabs [role=tab][aria-selected=true]{background:var(--tab-on);color:var(--ink);font-weight:650;
  border-color:var(--rule);box-shadow:inset 0 3px 0 var(--accent)}
.panel{padding:14px 0 0}
.panel[hidden]{display:none}
.vhead h2{margin:0;font-size:21px;line-height:1.25}
.vhead .sub{margin:4px 0 0;color:var(--ink-2);font-size:14px}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;margin:12px 0 10px;padding:9px 12px;background:var(--panel);
  border:1px solid var(--rule);border-radius:8px;font-size:13px;color:var(--ink-2)}
.legend h3{flex-basis:100%;margin:0;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.lg{display:inline-flex;align-items:center;gap:7px;max-width:100%}
.lg-group{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center}
.sw{display:inline-block;width:28px;height:16px;border:1.3px solid;border-radius:3px;flex:none}
.sw-deterministic{background:var(--n-det-f);border-color:var(--n-det)}
.sw-agentic{background:var(--n-agt-f);border-color:var(--n-agt);border-radius:8px}
.sw-human{background:var(--n-hum-f);border-color:var(--n-hum);border-width:2.4px;border-radius:5px}
.sw-store{border-color:var(--n-sto);background:linear-gradient(var(--n-sto),var(--n-sto)) 0 3px/100% 1.2px no-repeat,var(--n-sto-f)}
.sw-external{background:var(--n-ext-f);border-color:var(--n-ext);outline:1px solid var(--n-ext);outline-offset:-4px}
.sw-boundary_note{background:var(--n-note-f);border-color:var(--n-note);border-style:dashed}
.sw-ra{background:var(--ra-f);border-color:var(--ra);border-radius:3px}
.sw-tb{background:transparent;border:1.6px dashed var(--tb);border-radius:6px}
.sw-bound{background:transparent;border:1.3px dashed var(--bound);border-radius:6px}
.ew{display:inline-block;position:relative;width:38px;height:2px;flex:none;margin-right:6px}
.ew::after{content:"";position:absolute;right:-6px;top:50%;transform:translateY(-50%);border-left:7px solid var(--c);
  border-top:4px solid transparent;border-bottom:4px solid transparent}
.ew-data{--c:var(--e-data);background:var(--c)}
.ew-control{--c:var(--e-control);background:repeating-linear-gradient(90deg,var(--c) 0 6px,transparent 6px 10px)}
.ew-price{--c:var(--e-price);background:var(--c);height:3px}
.ew-evidence{--c:var(--e-evidence);height:2.5px;background:repeating-linear-gradient(90deg,var(--c) 0 2px,transparent 2px 5px)}
.ew-decision{--c:var(--e-decision);height:2.5px;background:repeating-linear-gradient(90deg,var(--c) 0 12px,transparent 12px 16px)}
.ew-feedback{--c:var(--e-feedback);background:repeating-linear-gradient(90deg,var(--c) 0 8px,transparent 8px 11px,var(--c) 11px 13px,transparent 13px 16px)}
.ew-guard{--c:var(--e-guard);height:1.5px;background:repeating-linear-gradient(90deg,var(--c) 0 1.5px,transparent 1.5px 4.5px)}
.ew-ra{--c:var(--e-data);background:var(--c);box-shadow:0 0 0 2px var(--ra-halo)}
.mk{display:inline-block;width:10px;height:10px;flex:none}
.mk-human{background:var(--n-hum);transform:rotate(45deg) scale(.85)}
.mk-agentic{background:var(--n-agt);border-radius:50%}
.mk-deterministic{background:var(--n-det);border-radius:1px}
.chip-sw{display:inline-block;background:var(--chip);color:var(--chip-ink);border-radius:9px;font-size:11px;
  font-weight:700;padding:0 7px;line-height:17px}
.chk-sw{display:inline-block;width:10px;height:10px;border:1.4px solid var(--ink-2);background:var(--bg)}
.scroller{overflow-x:auto;overflow-y:hidden;border:1px solid var(--rule);border-radius:8px;background:var(--bg);
  -webkit-overflow-scrolling:touch}
.hint{margin:6px 0 0;font-size:13px;color:var(--ink-3)}
.notes{margin:16px 0 0}
.notes h3{margin:0 0 6px;font-size:15px}
.notes ol{margin:0;padding-left:22px;columns:2 520px;column-gap:36px;font-size:13.5px;color:var(--ink-2)}
.notes li{break-inside:avoid;margin:0 0 6px}
footer{margin:28px 0 0;padding:12px 0 0;border-top:1px solid var(--rule);font-size:12.5px;color:var(--ink-3)}
/* ---------- diagram ---------- */
.sv{display:block;height:auto;font-family:var(--font)}
.sv text{font-family:var(--font)}
.sv-band{stroke:none}
.sv-b-plane{fill:var(--band-plane)}.sv-b-layer{fill:var(--band-layer)}.sv-b-actor_group{fill:var(--band-actor_group)}
.sv-b-phase{fill:var(--band-phase)}
.sv-bound{fill:none;stroke:var(--bound);stroke-width:1.2;stroke-dasharray:6 4}
.sv-acc{stroke:none}
.sv-a-plane{fill:var(--acc-plane)}.sv-a-layer{fill:var(--acc-layer)}.sv-a-actor_group{fill:var(--acc-actor_group)}
.sv-a-phase{fill:var(--acc-phase)}.sv-a-boundary{fill:var(--acc-boundary)}
.sv-perim{fill:none;stroke:var(--tb);stroke-width:1.6;stroke-dasharray:10 5}
.sv-tb{fill:none;stroke:var(--tb);stroke-width:1.5;stroke-dasharray:7 4}
.sv-box{stroke-width:1.3}
.sv-n-deterministic .sv-box{fill:var(--n-det-f);stroke:var(--n-det)}
.sv-n-agentic .sv-box{fill:var(--n-agt-f);stroke:var(--n-agt)}
.sv-n-human .sv-box{fill:var(--n-hum-f);stroke:var(--n-hum);stroke-width:2.4}
.sv-n-store .sv-box{fill:var(--n-sto-f);stroke:var(--n-sto)}
.sv-lid{fill:none;stroke:var(--n-sto);stroke-width:1.2}
.sv-n-external .sv-box{fill:var(--n-ext-f);stroke:var(--n-ext)}
.sv-inner{fill:none;stroke:var(--n-ext);stroke-width:.9}
.sv-n-boundary_note .sv-box{fill:var(--n-note-f);stroke:var(--n-note);stroke-dasharray:5 3}
.sv-badge{fill:var(--ra-f);stroke:var(--ra);stroke-width:1}
.sv-bt{font-size:11px;font-style:italic;fill:var(--ra-ink)}
.sv-nl{font-size:12.5px;font-weight:650;fill:var(--ink)}
.sv-nd{font-size:12.5px;font-weight:750;fill:var(--ink)}
.sv-ns{font-size:11px;fill:var(--ink-2)}
.sv-it{font-style:italic}
.sv-line{fill:none;stroke-width:1.4;stroke-linejoin:round}
.sv-e-data .sv-line{stroke:var(--e-data)}
.sv-e-control .sv-line{stroke:var(--e-control);stroke-dasharray:6 4}
.sv-e-price .sv-line{stroke:var(--e-price);stroke-width:2.2}
.sv-e-evidence .sv-line{stroke:var(--e-evidence);stroke-width:1.9;stroke-dasharray:1.6 3.4;stroke-linecap:round}
.sv-e-decision .sv-line{stroke:var(--e-decision);stroke-width:1.9;stroke-dasharray:12 4}
.sv-e-feedback .sv-line{stroke:var(--e-feedback);stroke-width:1.6;stroke-dasharray:8 3 2 3}
.sv-e-guard .sv-line{stroke:var(--e-guard);stroke-width:1.4;stroke-dasharray:1.4 3;stroke-linecap:round}
.sv-f-data{fill:var(--e-data)}.sv-f-control{fill:var(--e-control)}.sv-f-price{fill:var(--e-price)}
.sv-f-evidence{fill:var(--e-evidence)}.sv-f-decision{fill:var(--e-decision)}.sv-f-feedback{fill:var(--e-feedback)}
.sv-f-guard{fill:var(--e-guard)}
.sv-hit{fill:none;stroke:transparent;stroke-width:9;pointer-events:stroke}
.sv-rahalo{fill:none;stroke:var(--ra-halo);stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round}
.sv-el{font-size:11px;paint-order:stroke;stroke:var(--bg);stroke-width:3px;stroke-linejoin:round}
.sv-elbg{fill:var(--bg);fill-opacity:0;stroke:none}
.sv-loop-l{font-size:11px;paint-order:stroke;stroke:var(--bg);stroke-width:3.5px;stroke-linejoin:round}
.sv-t-data{fill:var(--t-data)}.sv-t-control{fill:var(--t-control)}.sv-t-price{fill:var(--t-price)}
.sv-t-evidence{fill:var(--t-evidence)}.sv-t-decision{fill:var(--t-decision)}.sv-t-feedback{fill:var(--t-feedback)}
.sv-t-guard{fill:var(--t-guard)}
.sv-cap{font-size:11.5px;font-weight:700;fill:var(--ink-2);paint-order:stroke;stroke-width:3.5px;stroke-linejoin:round}
.sv-gl{font-size:11px;font-weight:700;fill:var(--tb);paint-order:stroke;stroke-width:3.5px;stroke-linejoin:round}
.sv-ph{font-size:11px}
.sv-h-plane{stroke:var(--band-plane)}.sv-h-layer{stroke:var(--band-layer)}.sv-h-actor_group{stroke:var(--band-actor_group)}
.sv-h-phase{stroke:var(--band-phase)}.sv-h-boundary,.sv-h-none{stroke:var(--bg)}
.sv-capbg{stroke:none}.sv-cb-plane{fill:var(--band-plane)}.sv-cb-layer{fill:var(--band-layer)}
.sv-cb-actor_group{fill:var(--band-actor_group)}.sv-cb-phase{fill:var(--band-phase)}
.sv-cb-boundary,.sv-cb-none{fill:var(--bg)}
.sv-phase{fill:none;stroke:var(--ink-3);stroke-width:1.2}
.sv-conn{fill:none;stroke:var(--conn);stroke-width:1}
.sv-chip rect{fill:var(--chip)}.sv-chip text{fill:var(--chip-ink);font-size:11px;font-weight:700}
.sv-check{fill:var(--bg);stroke:var(--ink-2);stroke-width:1.4}
.sv-dot{fill:var(--ink-3)}.sv-dot-ic{fill:var(--n-hum)}
.sv-mk-human{fill:var(--n-hum)}.sv-mk-agentic{fill:var(--n-agt)}.sv-mk-deterministic{fill:var(--n-det)}
.sv-node,.sv-edge,.sv-elg{transition:opacity .12s}
.sv-node:hover .sv-box,.sv-node.hl .sv-box{stroke-width:2.8}
.sv-edge.hl .sv-line,.sv-edge:hover .sv-line{stroke-width:3}
.sv-elg.hl text{font-weight:700}
.sv.focus .sv-edge:not(.hl){opacity:.14}
.sv.focus .sv-elg:not(.hl){opacity:.2}
.sv.focus .sv-node:not(.hl){opacity:.5}
.sv-node{cursor:pointer;outline:none}
.sv-node:focus-visible .sv-box,.sv-node.sel .sv-box{stroke:var(--accent);stroke-width:3.2}
%HIDE%
/* ---------- legend toggles, details panel, notes ---------- */
.lg-k{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:13px;color:var(--ink-2);
  background:var(--bg);border:1px solid var(--rule);border-radius:6px;padding:2px 9px 2px 7px;cursor:pointer}
.lg-k:hover{border-color:var(--ink-3)}
.lg-k[aria-pressed=false]{opacity:.5;text-decoration:line-through}
.lg-act{font:inherit;font-size:13px;color:var(--accent);background:none;border:0;padding:2px 4px;cursor:pointer;
  text-decoration:underline}
.lg-note{flex-basis:100%;font-size:12.5px;color:var(--ink-3)}
.det{margin:8px 0 0;padding:9px 12px;border:1px solid var(--rule);border-radius:8px;background:var(--panel);
  font-size:13.5px;color:var(--ink-2);min-height:42px}
.det h4{margin:0 0 3px;font-size:14.5px;color:var(--ink)}
.det p{margin:2px 0}
.det ul{margin:4px 0 0;padding-left:20px}
.det .det-k{color:var(--ink-3)}
.notes li.ra-note .ra-chip{margin-right:6px}
@media (max-width:700px){.top h1{font-size:22px}.tabs [role=tab]{padding:7px 10px;font-size:13px}}
"""

EARLY_JS = ("(function(){try{var t=localStorage.getItem('tpa-theme');"
            "if(t==='light'||t==='dark'){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();")

JS = r"""
(function(){
  var root=document.documentElement, btn=document.getElementById('theme');
  var mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: dark)'):null;
  function eff(){var t=root.getAttribute('data-theme');return t?t:(mq&&mq.matches?'dark':'light');}
  function label(){var e=eff();btn.textContent=(e==='dark'?'Light theme':'Dark theme');
    btn.setAttribute('aria-label','Switch to '+(e==='dark'?'light':'dark')+' theme');}
  btn.addEventListener('click',function(){var next=eff()==='dark'?'light':'dark';
    root.setAttribute('data-theme',next);try{localStorage.setItem('tpa-theme',next);}catch(e){}label();});
  if(mq&&mq.addEventListener){mq.addEventListener('change',label);}
  label();
  var tabs=Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function select(tab,focus){
    tabs.forEach(function(t){var on=(t===tab);t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;
      document.getElementById(t.getAttribute('aria-controls')).hidden=!on;});
    if(focus){tab.focus();}
    try{localStorage.setItem('tpa-tab',tab.id);}catch(e){}
    try{if(history.replaceState){history.replaceState(null,'','#'+tab.id.slice(4));}}catch(e){}
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){select(t,false);});
    t.addEventListener('keydown',function(ev){var j=null;
      if(ev.key==='ArrowRight'){j=(i+1)%tabs.length;}else if(ev.key==='ArrowLeft'){j=(i-1+tabs.length)%tabs.length;}
      else if(ev.key==='Home'){j=0;}else if(ev.key==='End'){j=tabs.length-1;}
      if(j!==null){ev.preventDefault();select(tabs[j],true);}});
  });
  var start=null, h=(location.hash||'').replace('#','');
  if(h){start=document.getElementById('tab-'+h);}
  if(!start){try{var s=localStorage.getItem('tpa-tab');if(s){start=document.getElementById(s);}}catch(e){}}
  select(start||tabs[0],false);
  function each(list,fn){Array.prototype.forEach.call(list,fn);}
  each(document.querySelectorAll('.legend[data-view]'),function(lg){
    var svg=document.getElementById('svg-'+lg.getAttribute('data-view'));
    if(!svg){return;}
    var btns=Array.prototype.slice.call(lg.querySelectorAll('.lg-k'));
    function setKind(b,on){b.setAttribute('aria-pressed',on?'true':'false');
      svg.classList.toggle('hk-'+b.getAttribute('data-kind'),!on);}
    btns.forEach(function(b){b.addEventListener('click',function(){setKind(b,b.getAttribute('aria-pressed')!=='true');});});
    each(lg.querySelectorAll('.lg-act'),function(a){a.addEventListener('click',function(){
      var on=a.getAttribute('data-act')==='all';btns.forEach(function(b){setKind(b,on);});});});
  });
  each(document.querySelectorAll('svg.sv'),function(svg){
    var det=document.getElementById('det-'+svg.id.slice(4)), pinned=null;
    function clear(){svg.classList.remove('focus');
      each(svg.querySelectorAll('.hl,.sel'),function(el){el.classList.remove('hl');el.classList.remove('sel');});}
    function mark(sel){each(svg.querySelectorAll(sel),function(el){el.classList.add('hl');});}
    function titleOf(el){for(var c=el.firstChild;c;c=c.nextSibling){
      if(c.nodeName&&c.nodeName.toLowerCase()==='title'){return c.textContent;}}return '';}
    function lightNode(t){var id=t.getAttribute('data-node');svg.classList.add('focus');t.classList.add('hl');
      each(svg.querySelectorAll('.sv-edge'),function(e){
        var f=e.getAttribute('data-from'),to=e.getAttribute('data-to');
        if(f===id||to===id){e.classList.add('hl');mark('.sv-elg[data-edge="'+e.getAttribute('data-edge')+'"]');
          mark('[data-node="'+(f===id?to:f)+'"]');}});}
    function lightEdge(eid){svg.classList.add('focus');mark('[data-edge="'+eid+'"]');
      var g=svg.querySelector('.sv-edge[data-edge="'+eid+'"]');
      if(g){mark('[data-node="'+g.getAttribute('data-from')+'"]');mark('[data-node="'+g.getAttribute('data-to')+'"]');}}
    function restore(){clear();if(pinned){lightNode(pinned);pinned.classList.add('sel');}}
    function show(t){if(!det){return;}
      var id=t.getAttribute('data-node'),lines=titleOf(t).split('\n'),items=[];
      det.textContent='';
      var h=document.createElement('h4');h.textContent=lines[0];det.appendChild(h);
      lines.slice(1).forEach(function(l){var p=document.createElement('p');p.textContent=l;det.appendChild(p);});
      each(svg.querySelectorAll('.sv-edge'),function(e){
        if(e.getAttribute('data-from')===id||e.getAttribute('data-to')===id){items.push(titleOf(e).split('\n').join(' · '));}});
      if(items.length){var p=document.createElement('p');p.className='det-k';p.textContent='Links ('+items.length+'):';
        det.appendChild(p);var ul=document.createElement('ul');
        items.forEach(function(s){var li=document.createElement('li');li.textContent=s;ul.appendChild(li);});
        det.appendChild(ul);}}
    function pick(t){pinned=t;restore();show(t);}
    function nodeOf(ev){return ev.target.closest?ev.target.closest('[data-node]'):null;}
    svg.addEventListener('mouseover',function(ev){
      var t=ev.target.closest?ev.target.closest('[data-node],[data-edge]'):null;
      if(!t){restore();return;} clear();
      if(t.hasAttribute('data-node')){lightNode(t);}else{lightEdge(t.getAttribute('data-edge'));}
    });
    svg.addEventListener('mouseleave',restore);
    svg.addEventListener('focusin',function(ev){var t=nodeOf(ev);if(t){pick(t);}});
    svg.addEventListener('click',function(ev){var t=nodeOf(ev);if(t){pick(t);}});
    svg.addEventListener('keydown',function(ev){var t=nodeOf(ev);
      if(ev.key==='Escape'){pinned=null;clear();if(t&&t.blur){t.blur();}}
      else if(t&&(ev.key==='Enter'||ev.key===' ')){ev.preventDefault();pick(t);}});
  });
})();
"""

TAB_NAMES = {"overview": "Overview", "engines": "Engines", "capital_market": "Capital market",
             "lab": "Laboratory", "room": "Decision room", "cycle": "Quarterly cycle"}


def legend_html(v: dict, meta: dict, L) -> str:
    kinds = meta["kinds"]
    node_used = [k for k in kinds["node"] if any(n["kind"] == k for n in v["nodes"])]
    edge_used = [k for k in kinds["edge"] if any(e["kind"] == k for e in v["edges"])]
    o = [f'<div class="legend" role="group" aria-label="Legend and line filters" data-view="{esc(v["id"])}">'
         '<h3>Legend</h3><div class="lg-group">']
    for k in node_used:
        o.append(f'<span class="lg"><span class="sw sw-{k}"></span>{esc(kinds["node"][k])}</span>')
    o.append('</div><div class="lg-group" role="group" aria-label="Line types: press to show or hide">')
    for k in edge_used:
        o.append(f'<button type="button" class="lg-k" data-kind="{k}" aria-pressed="true">'
                 f'<span class="ew ew-{k}"></span>{esc(kinds["edge"][k])}</button>')
    o.append('<button type="button" class="lg-act" data-act="all">Show all lines</button>'
             '<button type="button" class="lg-act" data-act="none">Hide all</button>'
             '<span class="lg-note">Press a line type to hide or show it. Hide all, then show one type, to read one '
             'kind of flow at a time.</span>')
    o.append('</div><div class="lg-group">')
    if any(n.get("badge") for n in v["nodes"]) or any(e.get("badge") for e in v["edges"]):
        o.append(f'<span class="lg"><span class="sw sw-ra"></span>Real Assets badge: {esc(meta["badge_text"])}</span>')
        o.append('<span class="lg"><span class="ew ew-ra"></span>Real Assets link (yellow halo)</span>')
    if v.get("groups"):
        o.append('<span class="lg"><span class="sw sw-tb"></span>Trust boundary or process enclosure (§2.4, §7.2)</span>')
    if any(l.get("kind") == "boundary" for l in v["lanes"]) and v["layout"]["mode"] == "grid":
        o.append('<span class="lg"><span class="sw sw-bound"></span>Boundary lane: process, perimeter or rule set</span>')
    if v["layout"]["mode"] == "timeline":
        o.append('<span class="lg"><span class="chip-sw">G2</span>Meta-controller gate on the axis (§7.6)</span>')
        o.append('<span class="lg"><span class="chk-sw"></span>Other check (schema, pinned-dual CI test)</span>')
        o.append('<span class="lg"><span class="mk mk-human"></span><span class="mk mk-agentic"></span>'
                 '<span class="mk mk-deterministic"></span>Actors in the step: human, agentic, deterministic</span>')
    o.append("</div></div>")
    return "".join(o)


def build_html(model: dict, rendered: list[tuple[dict, str, object]]) -> str:
    meta = model["meta"]
    hide = "".join(f".sv.hk-{k} .sv-e-{k},.sv.hk-{k} .sv-lk-{k}{{display:none}}\n" for k in EDGE_KINDS)
    css = CSS.replace("%LIGHT%", LIGHT).replace("%DARK%", DARK).replace("%HIDE%", hide.rstrip("\n"))
    o = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         f'<title>{esc(meta["title"])}</title>',
         '<meta name="description" content="Six-view architectural schematic of the ADIC Agentic '
         'Total-Portfolio Laboratory, generated from design/ARCHITECTURE.md.">',
         f'<style>{css}</style><script>{EARLY_JS}</script></head><body><div class="wrap">',
         '<header class="top"><div class="titles">',
         f'<h1>{esc(meta["title"])}</h1>',
         f'<p class="src">Source: {esc(meta["source"])} · {esc(meta["project"])}</p>',
         f'<p class="ra-line"><span class="ra-chip">Real Assets</span><span>{esc(meta["ra_notice"])}</span></p>',
         '</div><div class="tools">',
         f'<span class="syn">{esc(meta["synthetic_label"])}</span>',
         '<button id="theme" type="button">Dark theme</button></div></header>',
         '<div class="tabs" role="tablist" aria-label="Schematic views">']
    for i, (v, _, _) in enumerate(rendered):
        vid = v["id"]
        o.append(f'<button type="button" role="tab" id="tab-{vid}" aria-controls="panel-{vid}" '
                 f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
                 f'{i + 1}. {esc(TAB_NAMES.get(vid, v["title"]))}</button>')
    o.append("</div>")
    for i, (v, svg, L) in enumerate(rendered):
        vid = v["id"]
        hidden = "" if i == 0 else " hidden"
        o.append(f'<section class="panel" role="tabpanel" id="panel-{vid}" aria-labelledby="tab-{vid}"{hidden}>')
        o.append(f'<div class="vhead"><h2>{esc(v["title"])}</h2><p class="sub">{esc(v["subtitle"])}</p></div>')
        o.append(legend_html(v, meta, L))
        o.append(f'<div class="scroller" tabindex="0" role="region" aria-label="{esc(v["title"])} diagram">{svg}</div>')
        o.append(f'<div class="det" id="det-{esc(vid)}" role="status" aria-live="polite"><p class="det-k">Select a box '
                 '(click, tap, or Tab then Enter) to see its owner, ARCHITECTURE.md section and links here. Esc '
                 'clears the selection.</p></div>')
        o.append('<p class="hint">Hover a box to light up its links; hover a line or label for its kind and '
                 'section. Every tooltip gives the sublabel, owner and ARCHITECTURE.md section.</p>')
        notes = v.get("notes", [])
        if notes:
            o.append('<div class="notes"><h3>Notes</h3><ol>')
            for t in notes:
                if meta["badge_text"] in t:
                    o.append(f'<li class="ra-note"><span class="ra-chip">Real Assets</span>{esc(t)}</li>')
                else:
                    o.append(f"<li>{esc(t)}</li>")
            o.append("</ol></div>")
        o.append("</section>")
    n_corr = len(meta.get("corrections", []))
    n_fix = len(meta.get("review_fixes", []))
    o.append(f'<footer>Generated by design/schematic/build_schematic.py from design/schematic/architecture_model.json '
             f'(merged from {esc(", ".join(meta["merged_from"]))}; {n_corr} merge corrections are logged in '
             f'meta.corrections and {n_fix} review fixes in meta.review_fixes). Section references: '
             f'{esc(meta["section_convention"])}. {esc(meta["synthetic_label"])}.</footer>')
    o.append(f"</div><script>{JS}</script></body></html>")
    return "".join(o)


def main() -> int:
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    meta = model["meta"]
    rendered, total_issues = [], 0
    for v in model["views"]:
        note = ""
        if v["layout"]["mode"] == "grid":
            # deterministic search over a fixed set of layout settings: least height + crossings, no issues
            best = None
            for params in SEARCH:
                cand = Grid(v, meta, params).layout()
                cand_issues = cand.check()
                cross = count_crossings(cand.routes)
                score = cand.H + CROSS_W * cross + (1e6 if cand_issues else 0.0)
                if best is None or score < best[0]:
                    best = (score, cand, params, cross)
            _, L, params, cross = best
            note = (f"  crossings {cross:4d}  [even {params['even_w']}, load {params['gut_load_w']}, "
                    f"bary {'on' if params['bary'] else 'off'}, avoid {'on' if params['avoid'] else 'off'}]")
        else:
            L = Timeline(v, meta).layout()
        svg = L.svg()
        issues = L.check()
        total_issues += len(issues)
        rendered.append((v, svg, L))
        print(f"{v['id']:15s} {v['layout']['mode']:8s} viewBox {L.W:.0f} x {L.H:.0f}  nodes {len(v['nodes']):3d}  "
              f"edges {len(v['edges']):3d}  issues {len(issues)}{note}")
        for msg in issues[:40]:
            print("    -", msg)
    page = build_html(model, rendered)
    OUT_PATH.write_text(page, encoding="utf-8")
    # ------------------------------------------------------- self-check
    text = OUT_PATH.read_text(encoding="utf-8")
    n_svg = len(re.findall(r"<svg\b", text))
    external = re.findall(r"https?://|<link\b|<img\b|<iframe\b|\bsrc\s*=|@import|url\((?!#)", text)
    small = sorted({float(m) for m in re.findall(r"font-size:\s*([\d.]+)px", text) if float(m) < 11})
    print(f"wrote {OUT_PATH} ({len(text) / 1024:.0f} KB)")
    print(f"self-check: svg elements = {n_svg} (expect 6); external references = {len(external)}; "
          f"font sizes below 11px = {small or 'none'}; layout issues = {total_issues}")
    ok = n_svg == 6 and not external and not small
    print("SELF-CHECK", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
