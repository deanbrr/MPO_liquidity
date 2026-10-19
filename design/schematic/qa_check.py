#!/usr/bin/env python3
"""Visual QA checker for design/schematic/TPA_Lab_Architecture.html.

Run:  .venv\\Scripts\\python.exe design\\schematic\\qa_check.py [HTML] [--browser auto] [--json OUT]

Standard library only (re, html.parser, xml.etree, struct; subprocess is used only for the
optional headless-browser measurement).  For every inline SVG view the checker

  1. finds the node rectangles (g.sv-node > rect.sv-box) and the text drawn in them;
  2. flags overlapping rectangles: node/node, edge-label tag vs node or tag, lane caption vs node
     or tag, timeline ticks; lane bands and trust-boundary boxes whose outline cuts a node; and
     anything clipped by the viewBox;
  3. flags text whose estimated width (0.6 x font-size per character, 0.55 for narrow families)
     exceeds its box minus padding (padding = the text's own left inset, 1px inside a label tag),
     and text that spills out of the bottom of its box or into the Real Assets badge strip;
  4. flags text below 11px effective size when the viewBox is drawn in a 1400px-wide container;
  5. flags edges whose endpoints do not touch their from/to node (timeline: the node's axis tick),
     edges that start or end inside a box, and edges that pass through a box;
  6. checks every node, edge and edge label has a <title> tooltip, that node and edge tooltips
     carry a Section, and that Real Assets items show the full badge text;
  7. computes WCAG contrast of node text vs node fill for the light and the dark token sets
     (extras: edge labels, captions, chips, and edge strokes vs the page);
  8. confirms there are no external URLs and that the :root tokens, the dark-mode media query,
     the data-theme overrides and an explicit body background are present.

It also prints layout metrics for the human reviewer: edge crossings, bends, lines hidden under
labels, port crowding, lane order and flow direction.  Optional, more realistic text checks use
the installed Segoe UI font files (--fonts auto, the default) and true rendered widths from a
headless Edge or Chrome (--browser auto).

Exit status: 1 if any ERROR was found, else 0.
"""
from __future__ import annotations

import argparse
import html as htmlmod
import json
import math
import re
import statistics
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_HTML = HERE / "TPA_Lab_Architecture.html"
DEFAULT_BADGE = "added 18 Oct; research in progress; interim rules (brief §8)"

CHAR_FACTOR, NARROW_FACTOR = 0.60, 0.55     # estimated advance per character, x font-size
NARROW_HINTS = ("condensed", "narrow", "compressed")
MIN_PX = 11.0                                # minimum effective text size
CONTRAST_TEXT, CONTRAST_GRAPHIC = 4.5, 3.0   # WCAG 1.4.3 text, 1.4.11 graphics
TOUCH_TOL = 1.5        # an endpoint this close to the box outline touches it
TICK_TOL = 4.0         # timeline arrows stop short of an axis tick by design
OVERLAP_TOL = 0.5
ASCENT, DESCENT = 0.75, 0.22                 # glyph extent above / below the baseline, x font-size
ARROW_W = 7.5          # arrowhead base width in user units (markerHeight 8.5, base 0.6..9.4 of 10)
VIEWPORT_H = 900.0     # for the "screens of scrolling" metric

SEV_RANK = {"ERROR": 0, "WARN": 1, "INFO": 2}


# ====================================================================== findings
class Findings:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, view: str, check: str, sev: str, msg: str) -> None:
        self.items.append({"view": view, "check": check, "sev": sev, "msg": msg})

    def n(self, sev: str, view: str | None = None, check: str | None = None) -> int:
        return sum(1 for f in self.items if f["sev"] == sev and (view is None or f["view"] == view)
                   and (check is None or f["check"] == check))


# ====================================================================== parsing
SVG_RE = re.compile(r"<svg\b[^>]*>.*?</svg>", re.S)


class _Tree(HTMLParser):
    """Fallback tree builder for SVG markup that is not well-formed XML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root: ET.Element | None = None
        self.stack: list[ET.Element] = []

    def handle_starttag(self, tag, attrs):
        el = ET.Element(tag, {k: (v or "") for k, v in attrs})
        if self.stack:
            self.stack[-1].append(el)
        elif self.root is None:
            self.root = el
        self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self.stack:
            return
        cur = self.stack[-1]
        if len(cur):
            cur[-1].tail = (cur[-1].tail or "") + data
        else:
            cur.text = (cur.text or "") + data


def parse_svg(markup: str) -> tuple[ET.Element, str]:
    try:
        root, how = ET.fromstring(markup), "xml.etree"
    except ET.ParseError:
        tb = _Tree()
        tb.feed(markup)
        tb.close()
        root, how = tb.root, "html.parser fallback"
    for el in root.iter():
        if isinstance(el.tag, str) and el.tag.startswith("{"):
            el.tag = el.tag.split("}", 1)[1]
        if any(k != k.lower() for k in el.attrib):
            el.attrib = {k.lower(): v for k, v in el.attrib.items()}
    return root, how


def rendered_text(el: ET.Element) -> str:
    """Text a <text> element draws: its own text and tspans, never a <title> child."""
    parts = [el.text or ""]
    for c in el:
        if c.tag != "title":
            parts.append(rendered_text(c))
        parts.append(c.tail or "")
    return "".join(parts)


def norm_text(s: str) -> str:
    return re.sub(r"[ \t\r\n]+", " ", s).strip(" \t\r\n")     # keeps NBSP, like SVG


def title_of(el: ET.Element) -> str | None:
    t = next((c for c in el if c.tag == "title"), None)
    return None if t is None else (t.text or "").strip()


def fa(el: ET.Element | None, name: str, default: float = 0.0) -> float:
    if el is None:
        return default
    try:
        return float(el.get(name))
    except (TypeError, ValueError):
        return default


def rect_of(el: ET.Element) -> tuple[float, float, float, float]:
    return (fa(el, "x"), fa(el, "y"), fa(el, "width"), fa(el, "height"))


def circle_box(el: ET.Element) -> tuple[float, float, float, float]:
    cx, cy, r = fa(el, "cx"), fa(el, "cy"), fa(el, "r")
    return (cx - r, cy - r, 2 * r, 2 * r)


def classes(el: ET.Element) -> list[str]:
    return el.get("class", "").split()


# ====================================================================== CSS
def css_blocks(css: str) -> list[tuple[str, str]]:
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        out.append((css[i:j].strip(), css[j + 1:k - 1]))
        i = k
    return out


def css_decls(body: str) -> list[tuple[str, str]]:
    out = []
    for part in body.split(";"):
        if ":" not in part:
            continue
        k, v = part.split(":", 1)
        k, v = k.strip(), v.strip()
        if k:
            out.append((k if k.startswith("--") else k.lower(), v))
    return out


_COMPOUND = re.compile(r"^([a-zA-Z][\w-]*)?((?:\.[\w-]+)*)$")


def parse_selector(sel: str):
    """Tag/class compounds joined by descendant combinators; anything else is unsupported (None)."""
    comps = []
    for part in sel.split():
        m = _COMPOUND.match(part)
        if not m:
            return None
        tag = m.group(1).lower() if m.group(1) else None
        cls = frozenset(c for c in m.group(2).split(".") if c)
        if tag is None and not cls:
            return None
        comps.append((tag, cls))
    return comps or None


class CSS:
    def __init__(self, text: str):
        self.text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        self.rules: list[tuple] = []           # (comps, specificity, order, decls), outside @media
        self.raw: list[tuple[str, list, str | None]] = []
        self.light: dict[str, str] = {}
        self.light_attr: dict[str, str] = {}
        self.dark_media: dict[str, str] = {}
        self.dark_attr: dict[str, str] = {}
        self.dark_media_guarded = False
        self.local_props: set[str] = set()     # custom properties declared outside :root rules
        order = 0
        for prelude, body in css_blocks(self.text):
            if prelude.startswith("@"):
                if prelude.lower().startswith("@media"):
                    dark_q = re.search(r"prefers-color-scheme\s*:\s*dark", prelude) is not None
                    for p2, b2 in css_blocks(body):
                        d2 = css_decls(b2)
                        for sel in p2.split(","):
                            sel = sel.strip()
                            self.raw.append((sel, d2, prelude))
                            norm = sel.replace("'", '"').replace(" ", "")
                            if dark_q and norm.startswith(":root"):
                                if ':not([data-theme="light"])' in norm:
                                    self.dark_media_guarded = True
                                self.dark_media.update({k: v for k, v in d2 if k.startswith("--")})
                continue
            decls = css_decls(body)
            for sel in prelude.split(","):
                sel = sel.strip()
                self.raw.append((sel, decls, None))
                norm = sel.replace("'", '"').replace(" ", "")
                cprops = {k: v for k, v in decls if k.startswith("--")}
                if norm == ":root":
                    self.light.update(cprops)
                elif norm == ':root[data-theme="dark"]':
                    self.dark_attr.update(cprops)
                elif norm == ':root[data-theme="light"]':
                    self.light_attr.update(cprops)
                else:
                    self.local_props.update(cprops)
                comps = parse_selector(sel)
                if comps:
                    spec = (sum(len(c[1]) for c in comps), sum(1 for c in comps if c[0]))
                    self.rules.append((comps, spec, order, decls))
                    order += 1

    def themes(self) -> dict[str, dict[str, str]]:
        light = dict(self.light)
        light.update(self.light_attr)
        dark = dict(self.light)
        dark.update(self.dark_attr or self.dark_media)
        return {"light": light, "dark": dark}

    def decl(self, selector: str, prop: str) -> str | None:
        val = None
        for sel, decls, media in self.raw:
            if media is None and sel.strip().lower() == selector:
                for k, v in decls:
                    if k == prop:
                        val = v
        return val


_VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)")


def resolve(value: str | None, tokens: dict[str, str], depth: int = 0) -> str | None:
    if value is None or depth > 10:
        return value

    def rep(m):
        v = tokens.get(m.group(1))
        if v is None:
            v = m.group(2) if m.group(2) is not None else f"<undefined {m.group(1)}>"
        return resolve(v, tokens, depth + 1)
    return _VAR.sub(rep, value).strip()


INHERITED = ("font-size", "font-weight", "font-style", "font-family", "fill", "fill-opacity",
             "text-anchor", "stroke", "stroke-width")


class Styler:
    """Minimal cascade: simple class/tag selectors with descendant combinators, specificity,
    source order, presentation attributes, inline style and SVG inheritance."""

    def __init__(self, css: CSS, root: ET.Element, base: dict[str, str]):
        self.parent = {c: p for p in root.iter() for c in p}
        self.cache: dict[int, dict[str, str]] = {}
        self.base = base
        self.by_class: dict[str, list] = defaultdict(list)
        self.by_tag: dict[str, list] = defaultdict(list)
        for r in css.rules:
            tag, cls = r[0][-1]
            if cls:
                self.by_class[min(cls)].append(r)
            else:
                self.by_tag[tag].append(r)

    def _ok(self, comp, el) -> bool:
        tag, cls = comp
        return (tag is None or el.tag == tag) and cls <= set(classes(el))

    def _match(self, comps, el) -> bool:
        if not self._ok(comps[-1], el):
            return False
        k, e = len(comps) - 2, self.parent.get(el)
        while k >= 0 and e is not None:
            if self._ok(comps[k], e):
                k -= 1
            e = self.parent.get(e)
        return k < 0

    def style(self, el: ET.Element) -> dict[str, str]:
        key = id(el)
        if key in self.cache:
            return self.cache[key]
        p = self.parent.get(el)
        st = dict(self.style(p)) if p is not None else dict(self.base)
        for a in INHERITED:
            if el.get(a) is not None:
                st[a] = el.get(a)
        cands = {id(r): r for r in self.by_tag.get(el.tag, [])}
        for c in classes(el):
            for r in self.by_class.get(c, []):
                cands[id(r)] = r
        for comps, spec, order, decls in sorted(cands.values(), key=lambda r: (r[1], r[2])):
            if self._match(comps, el):
                for k, v in decls:
                    if k in INHERITED:
                        st[k] = v
        for k, v in css_decls(el.get("style", "")):
            if k in INHERITED:
                st[k] = v
        self.cache[key] = st
        return st


def px(v: str | None, parent: float = 15.0) -> float | None:
    if v is None:
        return None
    v = v.strip()
    m = re.fullmatch(r"(-?[\d.]+)(px)?", v)
    if m:
        return float(m.group(1))
    m = re.fullmatch(r"(-?[\d.]+)(em|rem)", v)
    if m:
        return float(m.group(1)) * parent
    m = re.fullmatch(r"(-?[\d.]+)%", v)
    if m:
        return float(m.group(1)) / 100 * parent
    return None


def parse_weight(v: str | None) -> int:
    v = (v or "400").strip().lower()
    if v.isdigit():
        return int(v)
    return {"normal": 400, "bold": 700, "bolder": 700, "lighter": 300}.get(v, 400)


# ====================================================================== colour
NAMED = {"black": (0, 0, 0), "white": (255, 255, 255)}


def parse_color(s: str | None):
    if not s:
        return None
    s = s.strip().lower()
    if s in ("none", "transparent") or s.startswith("<undefined"):
        return None
    if s in NAMED:
        return (*NAMED[s], 1.0)
    m = re.fullmatch(r"#([0-9a-f]{3,8})", s)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
    m = re.fullmatch(r"rgba?\(([^)]*)\)", s)
    if m:
        parts = [p for p in re.split(r"[,\s/]+", m.group(1)) if p]
        rgb = [float(p[:-1]) * 2.55 if p.endswith("%") else float(p) for p in parts[:3]]
        a = 1.0
        if len(parts) > 3:
            a = float(parts[3][:-1]) / 100 if parts[3].endswith("%") else float(parts[3])
        return (*rgb, a)
    return None


def over(fg, bg):
    a = fg[3]
    return (fg[0] * a + bg[0] * (1 - a), fg[1] * a + bg[1] * (1 - a), fg[2] * a + bg[2] * (1 - a), 1.0)


def rel_lum(c) -> float:
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def contrast(a, b) -> float:
    la, lb = rel_lum(a), rel_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def hexc(c) -> str:
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c[:3])


# ====================================================================== real font metrics (optional)
SEGOE = {(300, "normal"): "segoeuil.ttf", (350, "normal"): "segoeuisl.ttf", (400, "normal"): "segoeui.ttf",
         (600, "normal"): "seguisb.ttf", (700, "normal"): "segoeuib.ttf", (900, "normal"): "seguibl.ttf",
         (300, "italic"): "seguili.ttf", (350, "italic"): "seguisli.ttf", (400, "italic"): "segoeuii.ttf",
         (600, "italic"): "seguisbi.ttf", (700, "italic"): "segoeuiz.ttf", (900, "italic"): "seguibli.ttf"}


def css_match_weight(w: int, avail: list[int]) -> int:
    """CSS Fonts 4 weight matching over the available faces."""
    avail = sorted(avail)
    if w in avail:
        return w
    if 400 <= w <= 500:
        order = [a for a in avail if w <= a <= 500] + sorted((a for a in avail if a < w), reverse=True) + \
                [a for a in avail if a > 500]
    elif w < 400:
        order = sorted((a for a in avail if a <= w), reverse=True) + [a for a in avail if a > w]
    else:
        order = [a for a in avail if a >= w] + sorted((a for a in avail if a < w), reverse=True)
    return order[0]


class TTF:
    """Advance widths from a TrueType file (hmtx + cmap format 4 / 12); kerning ignored."""

    def __init__(self, path: Path):
        d = path.read_bytes()
        base = struct.unpack(">I", d[12:16])[0] if d[:4] == b"ttcf" else 0
        num = struct.unpack(">H", d[base + 4:base + 6])[0]
        t = {}
        for i in range(num):
            rec = base + 12 + 16 * i
            tag, _, off, _ = struct.unpack(">4sIII", d[rec:rec + 16])
            t[tag] = off
        self.upem = struct.unpack(">H", d[t[b"head"] + 18:t[b"head"] + 20])[0]
        nhm = struct.unpack(">H", d[t[b"hhea"] + 34:t[b"hhea"] + 36])[0]
        hm = t[b"hmtx"]
        self.adv = struct.unpack(f">{2 * nhm}H", d[hm:hm + 4 * nhm])[0::2]
        self.cmap = self._cmap(d, t[b"cmap"])

    @staticmethod
    def _cmap(d: bytes, co: int) -> dict[int, int]:
        n = struct.unpack(">H", d[co + 2:co + 4])[0]
        best = None
        for i in range(n):
            pid, eid, off = struct.unpack(">HHI", d[co + 4 + 8 * i:co + 12 + 8 * i])
            fmt = struct.unpack(">H", d[co + off:co + off + 2])[0]
            if fmt == 12 and (pid, eid) in ((3, 10), (0, 4), (0, 6)):
                best = (co + off, 12)
                break
            if fmt == 4 and (pid, eid) in ((3, 1), (0, 3)) and best is None:
                best = (co + off, 4)
        m: dict[int, int] = {}
        if best is None:
            return m
        s, fmt = best
        if fmt == 4:
            seg2 = struct.unpack(">H", d[s + 6:s + 8])[0]
            seg = seg2 // 2
            ends = struct.unpack(f">{seg}H", d[s + 14:s + 14 + seg2])
            starts = struct.unpack(f">{seg}H", d[s + 16 + seg2:s + 16 + 2 * seg2])
            deltas = struct.unpack(f">{seg}h", d[s + 16 + 2 * seg2:s + 16 + 3 * seg2])
            ro = s + 16 + 3 * seg2
            ros = struct.unpack(f">{seg}H", d[ro:ro + seg2])
            for k in range(seg):
                for c in range(starts[k], ends[k] + 1):
                    if c == 0xFFFF:
                        continue
                    if ros[k] == 0:
                        g = (c + deltas[k]) & 0xFFFF
                    else:
                        addr = ro + 2 * k + ros[k] + 2 * (c - starts[k])
                        g = struct.unpack(">H", d[addr:addr + 2])[0]
                        if g:
                            g = (g + deltas[k]) & 0xFFFF
                    if g:
                        m[c] = g
        else:
            ng = struct.unpack(">I", d[s + 12:s + 16])[0]
            for k in range(ng):
                a, b, g0 = struct.unpack(">III", d[s + 16 + 12 * k:s + 28 + 12 * k])
                for c in range(a, min(b, 0x2FFFF) + 1):
                    m[c] = g0 + (c - a)
        return m

    def width(self, s: str, fs: float) -> tuple[float, int]:
        tot, miss = 0.0, 0
        for ch in s:
            g = self.cmap.get(ord(ch))
            if g is None:
                miss += 1
                tot += 0.6 * self.upem
            else:
                tot += self.adv[min(g, len(self.adv) - 1)]
        return tot / self.upem * fs, miss


class FontBook:
    """Segoe UI faces chosen by CSS Fonts 4 weight matching (650 -> Bold, 750 -> Black).
    Calibrated against headless Edge on this machine: 650 renders Bold (matches), 750 renders Bold
    via DirectWrite, so for 750 the Black face used here is the wider, conservative choice."""

    def __init__(self, font_dir: Path | None):
        self.faces = {}
        if font_dir is not None and font_dir.is_dir():
            self.faces = {k: font_dir / f for k, f in SEGOE.items() if (font_dir / f).exists()}
        self.loaded: dict[tuple, TTF] = {}

    def ok(self) -> bool:
        return (400, "normal") in self.faces

    def width(self, s: str, fs: float, weight: int, style: str) -> tuple[float, int, tuple]:
        sty = "italic" if style in ("italic", "oblique") else "normal"
        avail = sorted({w for (w, st) in self.faces if st == sty}) or sorted({w for (w, _) in self.faces})
        w = css_match_weight(weight, avail)
        key = (w, sty) if (w, sty) in self.faces else (w, "normal")
        if key not in self.loaded:
            self.loaded[key] = TTF(self.faces[key])
        wd, miss = self.loaded[key].width(s, fs)
        return wd, miss, key


# ====================================================================== headless browser (optional)
MEASURE_JS = r"""
(function(){var out={};var svgs=document.querySelectorAll('svg.sv');
for(var s=0;s<svgs.length;s++){var svg=svgs[s];var vid=svg.id.replace(/^svg-/,'');var rows=[];
var ts=svg.getElementsByTagName('text');
for(var i=0;i<ts.length;i++){var t=ts[i];var b=t.getBBox();
rows.push([Math.round(t.getComputedTextLength()*100)/100,Math.round(b.x*100)/100,Math.round(b.y*100)/100,
Math.round(b.width*100)/100,Math.round(b.height*100)/100]);}
out[vid]=rows;}
var pre=document.createElement('pre');pre.id='qa-out';pre.textContent=JSON.stringify(out);
document.body.appendChild(pre);})();
"""

BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]


def browser_measure(spec: str, page: str) -> tuple[dict | None, str]:
    if spec in ("off", "none", ""):
        return None, "browser measurement off"
    exe = spec if spec != "auto" else next((b for b in BROWSERS if Path(b).exists()), None)
    if not exe or not Path(exe).exists():
        return None, "no Edge/Chrome found"
    page = page.replace("</head>", "<style>.panel[hidden]{display:block!important}</style></head>", 1)
    k = page.rfind("</body>")
    page = page[:k] + f"<script>{MEASURE_JS}</script>" + page[k:]
    with tempfile.TemporaryDirectory(prefix="tpa_qa_", ignore_cleanup_errors=True) as tmp:
        p = Path(tmp) / "qa_measure.html"
        p.write_text(page, encoding="utf-8")
        cmd = [exe, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               "--disable-extensions", f"--user-data-dir={Path(tmp) / 'profile'}",
               "--virtual-time-budget=10000", "--window-size=1440,1000", "--dump-dom", p.as_uri()]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=180)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return None, f"browser failed: {exc}"
        out = r.stdout.decode("utf-8", errors="replace")
        m = re.search(r'<pre id="qa-out">(.*?)</pre>', out, re.S)
        if not m:
            return None, "browser produced no measurement (" + r.stderr.decode("utf-8", "replace")[-200:] + ")"
        return json.loads(htmlmod.unescape(m.group(1))), f"measured in {Path(exe).name} (headless)"


# ====================================================================== geometry
def overlap(a, b) -> tuple[float, float]:
    return (min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]),
            min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))


def inside(inner, outer, tol: float = 0.5) -> bool:
    return (inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol and
            inner[0] + inner[2] <= outer[0] + outer[2] + tol and inner[1] + inner[3] <= outer[1] + outer[3] + tol)


def point_rect_dist(p, r) -> float:
    """> 0: gap outside the rectangle; <= 0: minus the depth inside it."""
    x0, y0, x1, y1 = r[0], r[1], r[0] + r[2], r[1] + r[3]
    dx, dy = max(x0 - p[0], 0.0, p[0] - x1), max(y0 - p[1], 0.0, p[1] - y1)
    if dx > 0 or dy > 0:
        return math.hypot(dx, dy)
    return -min(p[0] - x0, x1 - p[0], p[1] - y0, y1 - p[1])


def side_of(p, r) -> tuple[str, float]:
    d = {"top": abs(p[1] - r[1]), "bottom": abs(p[1] - (r[1] + r[3])),
         "left": abs(p[0] - r[0]), "right": abs(p[0] - (r[0] + r[2]))}
    s = min(d, key=d.get)
    return s, (p[0] if s in ("top", "bottom") else p[1])


def path_points(d: str) -> list[tuple[float, float, str]]:
    """Absolute points along a path: M/L/H/V targets, Q corner (control) and end, C end."""
    toks = re.findall(r"[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", d)
    pts: list[tuple[float, float, str]] = []
    i, n, cmd = 0, len(toks), ""
    cx = cy = sx = sy = 0.0

    def take(k):
        nonlocal i
        vals = [float(t) for t in toks[i:i + k]]
        i += k
        return vals
    while i < n:
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                pts.append((sx, sy, "L"))
                cx, cy = sx, sy
            continue
        rel, c = cmd.islower(), cmd.upper()
        if c == "M":
            x, y = take(2)
            if rel:
                x, y = x + cx, y + cy
            cx, cy, sx, sy = x, y, x, y
            pts.append((x, y, "M"))
            cmd = "l" if rel else "L"
        elif c == "L":
            x, y = take(2)
            if rel:
                x, y = x + cx, y + cy
            cx, cy = x, y
            pts.append((x, y, "L"))
        elif c == "H":
            (x,) = take(1)
            cx = x + cx if rel else x
            pts.append((cx, cy, "L"))
        elif c == "V":
            (y,) = take(1)
            cy = y + cy if rel else y
            pts.append((cx, cy, "L"))
        elif c == "Q":
            x1, y1, x, y = take(4)
            if rel:
                x1, y1, x, y = x1 + cx, y1 + cy, x + cx, y + cy
            pts.append((x1, y1, "Qc"))
            pts.append((x, y, "Q"))
            cx, cy = x, y
        elif c == "C":
            x1, y1, x2, y2, x, y = take(6)
            if rel:
                x, y = x + cx, y + cy
            pts.append((x, y, "C"))
            cx, cy = x, y
        else:
            break
    return pts


def segments(pts) -> list[tuple]:
    out = []
    for (x0, y0, _), (x1, y1, k) in zip(pts, pts[1:]):
        if k == "M" or (abs(x0 - x1) < 0.05 and abs(y0 - y1) < 0.05):
            continue
        if k == "C":
            out.append(("D", x0, y0, x1, y1))
        elif abs(y0 - y1) < 0.05:
            out.append(("H", y0, min(x0, x1), max(x0, x1)))
        elif abs(x0 - x1) < 0.05:
            out.append(("V", x0, min(y0, y1), max(y0, y1)))
        else:
            out.append(("D", x0, y0, x1, y1))
    merged: list[tuple] = []
    for s in out:
        m = merged[-1] if merged else None
        if (m and s[0] in "HV" and m[0] == s[0] and abs(m[1] - s[1]) < 0.05
                and min(m[3], s[3]) >= max(m[2], s[2]) - 0.05):
            merged[-1] = (s[0], m[1], min(m[2], s[2]), max(m[3], s[3]))
        else:
            merged.append(s)
    return merged


def seg_rect_len(s, r, shrink: float = 0.0) -> float:
    """Length of an orthogonal segment inside rectangle r (shrunk by `shrink` on every side)."""
    x0, y0, x1, y1 = r[0] + shrink, r[1] + shrink, r[0] + r[2] - shrink, r[1] + r[3] - shrink
    if s[0] == "H":
        return max(0.0, min(s[3], x1) - max(s[2], x0)) if y0 < s[1] < y1 else 0.0
    if s[0] == "V":
        return max(0.0, min(s[3], y1) - max(s[2], y0)) if x0 < s[1] < x1 else 0.0
    return 0.0


def seg_rect_gap(s, r) -> float:
    """Euclidean distance between an orthogonal segment and a rectangle (0 if they touch)."""
    if s[0] == "H":
        dx = max(r[0] - s[3], 0.0, s[2] - (r[0] + r[2]))
        dy = max(r[1] - s[1], 0.0, s[1] - (r[1] + r[3]))
    elif s[0] == "V":
        dx = max(r[0] - s[1], 0.0, s[1] - (r[0] + r[2]))
        dy = max(r[1] - s[3], 0.0, s[2] - (r[1] + r[3]))
    else:
        return float("inf")
    return math.hypot(dx, dy)


# ====================================================================== per-view analysis
class View:
    def __init__(self, vid, heading, root, how, css, themes, opts, F, fonts, measured):
        self.vid, self.heading, self.root, self.how = vid, heading, root, how
        self.css, self.themes, self.opts, self.F = css, themes, opts, F
        self.fonts, self.measured = fonts, measured
        vb = [float(x) for x in root.get("viewbox", "0 0 0 0").replace(",", " ").split()]
        self.W, self.H = vb[2], vb[3]
        m = re.search(r"min-width\s*:\s*([\d.]+)px", root.get("style", ""))
        self.min_w = float(m.group(1)) if m else 0.0
        self.render_w = max(opts.container, self.min_w)
        self.scale = self.render_w / self.W if self.W else 1.0
        body_fs = px(css.decl("body", "font-size")) or 16.0
        self.styler = Styler(css, root, {"font-size": f"{body_fs}px", "font-weight": "400",
                                         "font-style": "normal",
                                         "font-family": css.decl("body", "font-family") or "sans-serif",
                                         "fill": "#000000", "fill-opacity": "1", "text-anchor": "start",
                                         "stroke": "none", "stroke-width": "1"})
        self.text_index = {id(t): i for i, t in enumerate(root.iter("text"))}
        self.metrics: dict = {}
        self.contrast_rows: list[tuple] = []
        self.collect()

    # ------------------------------------------------------------ collection
    def collect(self) -> None:
        R = self.root
        self.nodes: dict[str, dict] = {}
        self.dupes: list[str] = []
        self.edges: list[dict] = []
        self.labels: list[dict] = []
        self.captions: list[dict] = []
        self.ticks: list[dict] = []
        self.containers: list[dict] = []
        for g in R.iter("g"):
            cl = classes(g)
            if "sv-node" in cl:
                nid = g.get("data-node") or f"(unnamed node {len(self.nodes)})"
                box = next((c for c in g if c.tag == "rect" and "sv-box" in classes(c)), None)
                badge = next((c for c in g if c.tag == "rect" and "sv-badge" in classes(c)), None)
                if nid in self.nodes:
                    self.dupes.append(nid)
                self.nodes[nid] = {"id": nid, "kind": next((c[5:] for c in cl if c.startswith("sv-n-")), "?"),
                                   "ra": "sv-ra" in cl, "title": title_of(g), "box_el": box,
                                   "box": rect_of(box) if box is not None else None,
                                   "badge_el": badge, "badge": rect_of(badge) if badge is not None else None,
                                   "texts": list(g.iter("text")), "g": g}
            elif "sv-edge" in cl:
                line = next((c for c in g if c.tag == "path" and "sv-line" in classes(c)), None)
                pts = path_points(line.get("d", "")) if line is not None else []
                self.edges.append({"id": g.get("data-edge") or f"(unnamed edge {len(self.edges)})",
                                   "frm": g.get("data-from"), "to": g.get("data-to"),
                                   "kind": next((c[5:] for c in cl if c.startswith("sv-e-")), "?"),
                                   "ra": "sv-ra" in cl, "title": title_of(g), "line": line, "pts": pts,
                                   "segs": segments(pts), "g": g,
                                   "marker": line is not None and bool(line.get("marker-end"))})
            elif "sv-elg" in cl:
                self.labels.append({"edge": g.get("data-edge"), "title": title_of(g),
                                    "rects": [rect_of(c) for c in g if c.tag == "rect"],
                                    "rect_els": [c for c in g if c.tag == "rect"],
                                    "texts": [c for c in g if c.tag == "text"], "g": g})
            elif "sv-captions" in cl:
                last = None
                for c in g:
                    if c.tag == "rect":
                        last = c
                    elif c.tag == "text":
                        self.captions.append({"text": c, "bg_el": last, "bg": rect_of(last) if last is not None else None})
                        last = None
            elif "sv-chip" in cl:
                r = next((c for c in g if c.tag == "rect"), None)
                t = next((c for c in g if c.tag == "text"), None)
                self.ticks.append({"kind": "chip", "box": rect_of(r), "text": t, "el": r,
                                   "title": title_of(g) or ""})
        for el in R.iter():
            cl = classes(el)
            if el.tag == "rect" and "sv-check" in cl:
                self.ticks.append({"kind": "check", "box": rect_of(el), "text": None, "el": el,
                                   "title": title_of(el) or ""})
            elif el.tag == "circle" and "sv-dot" in cl:
                self.ticks.append({"kind": "dot", "box": circle_box(el), "text": None, "el": el,
                                   "title": title_of(el) or ""})
            elif el.tag == "rect":
                for k in ("sv-band", "sv-bound", "sv-perim", "sv-tb"):
                    if k in cl:
                        self.containers.append({"kind": k[3:], "box": rect_of(el),
                                                "title": (title_of(el) or "").split("\n")[0]})
        claimed = set()
        for n in self.nodes.values():
            claimed.update(id(t) for t in n["texts"])
        for lab in self.labels:
            claimed.update(id(t) for t in lab["texts"])
        for c in self.captions:
            claimed.add(id(c["text"]))
        for tk in self.ticks:
            if tk["text"] is not None:
                claimed.add(id(tk["text"]))
        self.free_texts = [t for t in R.iter("text") if id(t) not in claimed]
        self.node_rows = sorted({round(n["box"][1], 1) for n in self.nodes.values() if n["box"]})
        self.is_timeline = bool(self.ticks)

    # ------------------------------------------------------------ text helpers
    def tinfo(self, el: ET.Element) -> dict:
        st = self.styler.style(el)
        light = self.themes["light"]
        fs = px(resolve(st.get("font-size"), light)) or 16.0
        fam = resolve(st.get("font-family"), light) or ""
        first = fam.split(",")[0].strip().strip("\"'").lower()
        factor = NARROW_FACTOR if any(h in first for h in NARROW_HINTS) else CHAR_FACTOR
        s = norm_text(rendered_text(el))
        return {"s": s, "fs": fs, "w": len(s) * fs * factor, "x": fa(el, "x"), "y": fa(el, "y"),
                "anchor": (st.get("text-anchor") or "start").strip(), "weight": parse_weight(st.get("font-weight")),
                "style": (st.get("font-style") or "normal").strip(), "el": el}

    @staticmethod
    def tbox(ti: dict, w: float) -> tuple[float, float, float, float]:
        x0 = ti["x"] if ti["anchor"] == "start" else (ti["x"] - w / 2 if ti["anchor"] == "middle" else ti["x"] - w)
        return (x0, ti["y"] - ASCENT * ti["fs"], w, (ASCENT + DESCENT) * ti["fs"])

    def widths(self, ti: dict) -> list[tuple[str, float]]:
        out = [("text-fit", ti["w"])]
        if self.fonts is not None and self.fonts.ok():
            w, _, _ = self.fonts.width(ti["s"], ti["fs"], ti["weight"], ti["style"])
            out.append(("text-fit/segoe-ui", w))
        if self.measured is not None:
            i = self.text_index.get(id(ti["el"]))
            if i is not None and i < len(self.measured):
                out.append(("text-fit/browser", self.measured[i][0]))
        return out

    def paint(self, el, prop: str, theme: str, backdrop):
        st = self.styler.style(el)
        tok = self.themes[theme]
        c = parse_color(resolve(st.get(prop), tok))
        if c is None:
            return None
        op = 1.0
        if prop == "fill":
            try:
                op = float(resolve(st.get("fill-opacity") or "1", tok))
            except ValueError:
                op = 1.0
        return over((c[0], c[1], c[2], c[3] * op), backdrop)

    def page_bg(self, theme: str):
        c = parse_color(resolve("var(--bg)", self.themes[theme]))
        return c if c else (255, 255, 255, 1.0)

    # ------------------------------------------------------------ checks
    def check_titles(self, badge_text: str) -> None:
        V, F = self.vid, self.F
        for nid in self.dupes:
            F.add(V, "tooltips", "ERROR", f"duplicate data-node id '{nid}'")
        for n in self.nodes.values():
            t = n["title"]
            if not t:
                F.add(V, "tooltips", "ERROR", f"node {n['id']}: no <title> tooltip")
                continue
            m = re.search(r"^Section:\s*(.*)$", t, re.M)
            if not m or not m.group(1).strip():
                F.add(V, "tooltips", "ERROR", f"node {n['id']}: tooltip has no 'Section:' value")
            if n["ra"]:
                shown = " ".join(norm_text(rendered_text(x)) for x in n["texts"] if "sv-bt" in classes(x))
                if n["badge"] is None or norm_text(shown) != badge_text:
                    F.add(V, "ra-badge", "ERROR", f"node {n['id']}: Real Assets badge strip missing or text "
                                                  f"differs ('{shown}')")
                if badge_text not in t:
                    F.add(V, "ra-badge", "ERROR", f"node {n['id']}: tooltip lacks the Real Assets badge text")
        for e in self.edges:
            t = e["title"]
            if not t:
                F.add(V, "tooltips", "ERROR", f"edge {e['id']}: no <title> tooltip")
                continue
            m = re.search(r"^Section:\s*(.*)$", t, re.M)
            if not m or not m.group(1).strip():
                F.add(V, "tooltips", "ERROR", f"edge {e['id']}: tooltip has no 'Section:' value")
            if e["ra"] and badge_text not in t:
                F.add(V, "ra-badge", "ERROR", f"edge {e['id']}: Real Assets edge tooltip lacks the badge text")
        for lab in self.labels:
            if not lab["title"]:
                F.add(V, "tooltips", "ERROR", f"edge label {lab['edge']}: no <title> tooltip")

    def solids(self) -> list[tuple[str, str, tuple]]:
        out = []
        for n in self.nodes.values():
            if n["box"]:
                out.append(("node", n["id"], n["box"]))
        for lab in self.labels:
            for r in lab["rects"]:
                out.append(("label", lab["edge"], r))
        for c in self.captions:
            if c["bg"]:
                out.append(("caption", norm_text(rendered_text(c["text"]))[:48], c["bg"]))
        for tk in self.ticks:
            out.append(("tick", (tk["title"].split(":")[0] or tk["kind"]), tk["box"]))
        for t in self.free_texts:
            ti = self.tinfo(t)
            out.append(("text", ti["s"][:48], self.tbox(ti, ti["w"])))
        return out

    def check_overlaps(self) -> None:
        V, F = self.vid, self.F
        S = self.solids()
        for i in range(len(S)):
            ci, ni, ri = S[i]
            for j in range(i + 1, len(S)):
                cj, nj, rj = S[j]
                if ci == cj == "label" and ni == nj:
                    continue
                ox, oy = overlap(ri, rj)
                if ox > OVERLAP_TOL and oy > OVERLAP_TOL:
                    sev = "ERROR" if ("node" in (ci, cj) or (ox > 2 and oy > 2)) else "WARN"
                    F.add(V, "overlap", sev, f"{ci} '{ni}' overlaps {cj} '{nj}' by {ox:.1f} x {oy:.1f}px")
        # containers whose outline cuts through a node; nodes outside every lane
        for c in self.containers:
            for n in self.nodes.values():
                if not n["box"]:
                    continue
                ox, oy = overlap(c["box"], n["box"])
                if ox > OVERLAP_TOL and oy > OVERLAP_TOL and not inside(n["box"], c["box"]):
                    sev = "ERROR" if c["kind"] in ("tb", "perim") else "WARN"
                    F.add(V, "container-cut", sev, f"{c['kind']} '{c['title'][:50]}' outline cuts node {n['id']}")
        lanes = [c for c in self.containers if c["kind"] in ("band", "bound")]
        if lanes:
            for n in self.nodes.values():
                if n["box"] and not any(inside(n["box"], c["box"]) for c in lanes):
                    F.add(V, "container-cut", "WARN", f"node {n['id']} is not inside any lane band")
        # clipping by the viewBox
        vb = (0.0, 0.0, self.W, self.H)
        boxes = list(S)
        for n in self.nodes.values():
            for t in n["texts"]:
                ti = self.tinfo(t)
                boxes.append(("node text", f"{n['id']}: {ti['s'][:30]}", self.tbox(ti, ti["w"])))
        for e in self.edges:
            for p in e["pts"]:
                if not (-0.5 <= p[0] <= self.W + 0.5 and -0.5 <= p[1] <= self.H + 0.5):
                    F.add(V, "clipping", "ERROR", f"edge {e['id']} has a point outside the viewBox ({p[0]:.1f},{p[1]:.1f})")
                    break
        for c, name, r in boxes:
            if not inside(r, vb):
                F.add(V, "clipping", "ERROR", f"{c} '{name}' extends outside the viewBox {self.W:g}x{self.H:g}")

    def fit_targets(self):
        for n in self.nodes.values():
            if not n["box"]:
                continue
            for t in n["texts"]:
                if "sv-bt" in classes(t) and n["badge"] is not None:
                    yield t, n["badge"], f"node {n['id']} badge", "inset", None
                else:
                    yield t, n["box"], f"node {n['id']}", "inset", n["badge"]
        for lab in self.labels:
            for k, t in enumerate(lab["texts"]):
                if k < len(lab["rects"]):
                    yield t, lab["rects"][k], f"edge label {lab['edge']}", "tag", None
        for c in self.captions:
            if c["bg"] is not None:
                yield c["text"], c["bg"], "caption", "tag", None
        for tk in self.ticks:
            if tk["text"] is not None:
                yield tk["text"], tk["box"], "gate chip", "tag", None

    def check_text(self) -> None:
        V, F = self.vid, self.F
        worst: dict[str, float] = defaultdict(lambda: -1e9)
        n_checked = 0
        for el, box, where, mode, badge in self.fit_targets():
            ti = self.tinfo(el)
            n_checked += 1
            bx0, bx1 = box[0], box[0] + box[2]
            pad = max(1.0, ti["x"] - bx0) if (mode == "inset" and ti["anchor"] == "start") else 1.0
            for method, w in self.widths(ti):
                x0, _, ww, _ = self.tbox(ti, w)
                x1 = x0 + ww
                past_box = max(x1 - bx1, bx0 - x0)
                into_pad = max(x1 - (bx1 - pad), (bx0 + pad) - x0) if ti["anchor"] != "start" else x1 - (bx1 - pad)
                worst[method] = max(worst[method], into_pad)
                if past_box > 0.5:
                    F.add(V, method, "ERROR", f"{where}: '{ti['s']}' ({ti['fs']:g}px) runs {past_box:.1f}px past "
                                              f"the box outline (text {ww:.0f}px, box {box[2]:.0f}px)")
                elif into_pad > 0.5:
                    F.add(V, method, "WARN", f"{where}: '{ti['s']}' ({ti['fs']:g}px) runs {into_pad:.1f}px into the "
                                             f"{pad:.0f}px padding (text {ww:.0f}px, box {box[2]:.0f}px)")
            top, bot = ti["y"] - ASCENT * ti["fs"], ti["y"] + DESCENT * ti["fs"]
            limit = badge[1] if badge is not None else box[1] + box[3]
            if bot > limit + 0.5:
                what = "into the Real Assets badge strip" if badge is not None else "below the bottom of its box"
                F.add(V, "text-fit", "ERROR", f"{where}: '{ti['s']}' extends {bot - limit:.1f}px {what}")
            if top < box[1] - 0.5:
                F.add(V, "text-fit", "ERROR", f"{where}: '{ti['s']}' starts {box[1] - top:.1f}px above its box")
        self.metrics["texts_in_boxes"] = n_checked
        self.metrics["worst_into_padding"] = dict(worst)
        # effective font size at the intended width
        sizes = []
        for t in self.root.iter("text"):
            ti = self.tinfo(t)
            eff = ti["fs"] * self.scale
            sizes.append(eff)
            if eff < MIN_PX - 1e-6:
                F.add(V, "font-size", "ERROR", f"'{ti['s'][:40]}' is {ti['fs']:g}px, {eff:.2f}px effective "
                                               f"at {self.render_w:.0f}px (minimum {MIN_PX:g})")
        self.metrics["min_effective_px"] = min(sizes) if sizes else None
        self.metrics["n_text"] = len(sizes)

    def check_edges(self) -> None:
        V, F = self.vid, self.F
        tick_of = {}
        if self.ticks:
            for n in self.nodes.values():
                if not n["box"]:
                    continue
                cx = n["box"][0] + n["box"][2] / 2
                best = min(self.ticks, key=lambda t: abs(t["box"][0] + t["box"][2] / 2 - cx))
                if abs(best["box"][0] + best["box"][2] / 2 - cx) <= 1.0:
                    tick_of[n["id"]] = best["box"]
        self.ports: dict[str, list] = defaultdict(list)
        stats = Counter()
        for e in self.edges:
            pts = [(p[0], p[1]) for p in e["pts"]]
            if len(pts) < 2:
                F.add(V, "edge-endpoints", "ERROR", f"edge {e['id']}: no drawable path")
                continue
            if not e["marker"]:
                F.add(V, "edge-endpoints", "WARN", f"edge {e['id']}: no arrowhead (marker-end)")
            line_d = e["line"].get("d", "") if e["line"] is not None else ""
            for p in e["g"].iter("path"):
                if p is not e["line"] and p.get("d", "") != line_d:
                    F.add(V, "edge-endpoints", "WARN", f"edge {e['id']}: {p.get('class', 'path')} does not follow the "
                                                       f"drawn line (hover or halo is misplaced)")
            for which, p, q, nid in (("start", pts[0], pts[1], e["frm"]), ("end", pts[-1], pts[-2], e["to"])):
                implicit = nid is None
                if implicit:
                    cands = [n for n in self.nodes.values() if n["box"]]
                    nid = min(cands, key=lambda n: abs(point_rect_dist(p, n["box"])))["id"]
                node = self.nodes.get(nid)
                if node is None or node["box"] is None:
                    F.add(V, "edge-endpoints", "ERROR", f"edge {e['id']}: {which} names unknown node '{nid}'")
                    continue
                d = point_rect_dist(p, node["box"])
                label = f"edge {e['id']} ({e['frm'] or '?'} -> {e['to'] or '?'}, {e['kind']})"
                if abs(d) <= TOUCH_TOL:
                    stats["box"] += 1
                    side, pos = side_of(p, node["box"])
                    self.ports[nid].append((side, pos, which == "end", e["id"]))
                    if point_rect_dist(q, node["box"]) < -0.5:
                        F.add(V, "edge-endpoints", "ERROR", f"{label}: {which} segment runs inside node {nid}")
                elif d < -TOUCH_TOL:
                    stats["inside"] += 1
                    sev = "ERROR" if d < -3 else "WARN"
                    F.add(V, "edge-endpoints", sev, f"{label}: {which} point lies {-d:.1f}px inside node {nid}"
                                                    f"{' (arrowhead hidden under the box)' if which == 'end' else ''}")
                elif nid in tick_of:
                    dt = point_rect_dist(p, tick_of[nid])
                    if dt <= TICK_TOL:
                        stats["tick"] += 1
                    else:
                        stats["tick_gap"] += 1
                        F.add(V, "edge-endpoints", "WARN", f"{label}: {which} stops {dt:.1f}px short of the axis "
                                                           f"tick of {nid} (and {d:.0f}px from its box)")
                else:
                    stats["gap"] += 1
                    sev = "ERROR" if d > 3 else "WARN"
                    F.add(V, "edge-endpoints", sev, f"{label}: {which} is {d:.1f}px from node {nid}"
                                                    f"{' (no data-from/data-to; nearest node)' if implicit else ''}")
        self.metrics["endpoint_stats"] = dict(stats)
        # port crowding: arrowheads arriving closer than their own width
        crowd = 0
        for nid, items in self.ports.items():
            by_side = defaultdict(list)
            for side, pos, arrive, eid in items:
                by_side[side].append((pos, arrive, eid))
            for side, lst in by_side.items():
                lst.sort()
                for (p1, a1, e1), (p2, a2, e2) in zip(lst, lst[1:]):
                    gap = p2 - p1
                    if (a1 and a2 and gap < ARROW_W) or gap < 3.0:
                        crowd += 1
                        F.add(V, "port-crowding", "WARN", f"node {nid} {side}: ends of {e1} and {e2} are "
                                                          f"{gap:.1f}px apart{' (arrowheads overlap)' if a1 and a2 else ''}")
        self.metrics["port_crowding"] = crowd

    def check_routes(self) -> None:
        """Edges through boxes, grazing, shared tracks, crossings, lines hidden under labels/captions."""
        V, F = self.vid, self.F
        boxes = [(n["id"], n["box"]) for n in self.nodes.values() if n["box"]]
        through, graze = 0, 0
        for e in self.edges:
            for s in e["segs"]:
                if s[0] not in "HV":
                    continue
                for nid, b in boxes:
                    L = seg_rect_len(s, b, shrink=1.0)
                    if L > 0.5:
                        through += 1
                        F.add(V, "edge-through-node", "ERROR", f"edge {e['id']} ({e['frm']} -> {e['to']}) runs "
                                                               f"{L:.0f}px through node {nid}")
                        continue
                    if s[0] == "V":
                        near = min(abs(s[1] - b[0]), abs(s[1] - (b[0] + b[2])))
                        ov = min(s[3], b[1] + b[3]) - max(s[2], b[1])
                        if near < 2.0 and ov > 2.0 and not (b[0] + 1 < s[1] < b[0] + b[2] - 1):
                            graze += 1
                            F.add(V, "edge-grazes-node", "WARN", f"edge {e['id']} runs {ov:.0f}px along the side of "
                                                                 f"node {nid}, {near:.1f}px away")
                    else:
                        near = min(abs(s[1] - b[1]), abs(s[1] - (b[1] + b[3])))
                        ov = min(s[3], b[0] + b[2]) - max(s[2], b[0])
                        if near < 2.0 and ov > 2.0 and not (b[1] + 1 < s[1] < b[1] + b[3] - 1):
                            graze += 1
                            F.add(V, "edge-grazes-node", "WARN", f"edge {e['id']} runs {ov:.0f}px along the top/bottom "
                                                                 f"of node {nid}, {near:.1f}px away")
        # shared tracks (collinear overlap between different edges)
        flat = [(e["id"], s) for e in self.edges for s in e["segs"] if s[0] in "HV"]
        shared = 0
        for i in range(len(flat)):
            ei, si = flat[i]
            for j in range(i + 1, len(flat)):
                ej, sj = flat[j]
                if ei == ej or si[0] != sj[0] or abs(si[1] - sj[1]) >= 1.0:
                    continue
                ov = min(si[3], sj[3]) - max(si[2], sj[2])
                if ov > 1.0:
                    shared += 1
                    F.add(V, "shared-track", "WARN", f"edges {ei} and {ej} share a {si[0]} track for {ov:.0f}px")
        # crossings
        cross, per = 0, Counter()
        for i in range(len(self.edges)):
            for j in range(i + 1, len(self.edges)):
                a, b = self.edges[i], self.edges[j]
                for s in a["segs"]:
                    for t in b["segs"]:
                        if s[0] == "H" and t[0] == "V":
                            h, v = s, t
                        elif s[0] == "V" and t[0] == "H":
                            h, v = t, s
                        else:
                            continue
                        if h[2] + 0.5 < v[1] < h[3] - 0.5 and v[2] + 0.5 < h[1] < v[3] - 0.5:
                            cross += 1
                            per[a["id"]] += 1
                            per[b["id"]] += 1
        # occlusion by other edges' label tags and by captions
        hidden_len, hidden_pairs, corner_hidden = 0.0, 0, 0
        cap_rects = [(norm_text(rendered_text(c["text"]))[:40], c["bg"]) for c in self.captions if c["bg"]]
        for e in self.edges:
            corners = [(p[0], p[1]) for p in e["pts"] if p[2] == "Qc"]
            for lab in self.labels:
                if lab["edge"] == e["id"]:
                    continue
                for r in lab["rects"]:
                    L = sum(seg_rect_len(s, r) for s in e["segs"])
                    if L > 0.5:
                        hidden_len += L
                        hidden_pairs += 1
                    for c in corners:
                        if point_rect_dist(c, r) < -0.5:
                            corner_hidden += 1
                            F.add(V, "edge-under-label", "WARN", f"a bend of edge {e['id']} is hidden under the label "
                                                                 f"of edge {lab['edge']}")
            for name, r in cap_rects:
                L = sum(seg_rect_len(s, r) for s in e["segs"])
                if L > 0.5:
                    F.add(V, "edge-under-caption", "WARN", f"edge {e['id']}: {L:.0f}px of line hidden under caption '{name}'")
        # label placement: each label tag should sit on (or right beside) its own line
        own = {e["id"]: e for e in self.edges}
        tol = 30.0 if self.is_timeline else 6.0
        detached = 0
        for lab in self.labels:
            e = own.get(lab["edge"])
            if e is None:
                F.add(V, "label-placement", "WARN", f"label for {lab['edge']} has no matching edge")
                continue
            gap = min((seg_rect_gap(s, r) for s in e["segs"] for r in lab["rects"]), default=float("inf"))
            if gap > tol:
                detached += 1
                F.add(V, "label-placement", "WARN", f"label of edge {lab['edge']} sits {gap:.0f}px from its own line")
        bends = [sum(1 for p in e["pts"] if p[2] == "Qc") for e in self.edges]
        lengths = [sum((s[3] - s[2]) if s[0] in "HV" else math.hypot(s[3] - s[1], s[4] - s[2]) for s in e["segs"])
                   for e in self.edges]
        self.metrics.update({
            "edge_through_node": through, "edge_grazes_node": graze, "shared_tracks": shared,
            "crossings": cross, "crossings_per_edge": round(cross / max(1, len(self.edges)), 2),
            "most_crossed": per.most_common(5), "label_hides_line_pairs": hidden_pairs,
            "line_px_hidden_under_labels": round(hidden_len), "bends_hidden_under_labels": corner_hidden,
            "labels_detached": detached,
            "bends_mean": round(statistics.mean(bends), 2) if bends else 0, "bends_max": max(bends, default=0),
            "edge_len_mean": round(statistics.mean(lengths)) if lengths else 0,
            "edge_len_max": round(max(lengths, default=0)),
            "edges_over_1000px": sum(1 for x in lengths if x > 1000),
        })

    def check_contrast(self) -> None:
        V, F = self.vid, self.F
        rows: dict[tuple, list] = {}

        def put(group, theme, what, fg, bg, need):
            if fg is None or bg is None:
                return
            r = contrast(fg, bg)
            key = (group, theme, what)
            if key not in rows or r < rows[key][0]:
                rows[key] = [r, hexc(fg), hexc(bg), need]
        for theme in ("light", "dark"):
            page = self.page_bg(theme)
            for n in self.nodes.values():
                if n["box_el"] is None:
                    continue
                fill = self.paint(n["box_el"], "fill", theme, page)
                badge = self.paint(n["badge_el"], "fill", theme, fill) if n["badge_el"] is not None else None
                for t in n["texts"]:
                    cl = classes(t)
                    bg = badge if ("sv-bt" in cl and badge is not None) else fill
                    fg = self.paint(t, "fill", theme, bg)
                    tc = next((c for c in cl if c in ("sv-nl", "sv-ns", "sv-nd", "sv-bt")), cl[0] if cl else "text")
                    put("node text", theme, f"{tc} on {n['kind']}{' badge' if tc == 'sv-bt' else ''}", fg, bg,
                        CONTRAST_TEXT)
            for lab in self.labels:
                for k, t in enumerate(lab["texts"]):
                    if k < len(lab["rect_els"]):
                        bg = self.paint(lab["rect_els"][k], "fill", theme, page)
                        fg = self.paint(t, "fill", theme, bg)
                        tc = next((c for c in classes(t) if c.startswith("sv-t-")), "sv-el")
                        put("edge label", theme, tc, fg, bg, CONTRAST_TEXT)
            for c in self.captions:
                if c["bg_el"] is None:
                    continue
                bg = self.paint(c["bg_el"], "fill", theme, page)
                fg = self.paint(c["text"], "fill", theme, bg)
                cb = next((x for x in classes(c["bg_el"]) if x.startswith("sv-cb-")), "bg")
                tc = "sv-gl" if "sv-gl" in classes(c["text"]) else "sv-cap"
                put("caption", theme, f"{tc} on {cb}", fg, bg, CONTRAST_TEXT)
            for tk in self.ticks:
                if tk["text"] is not None:
                    bg = self.paint(tk["el"], "fill", theme, page)
                    put("chip", theme, "gate chip", self.paint(tk["text"], "fill", theme, bg), bg, CONTRAST_TEXT)
            for t in self.free_texts:
                cl = classes(t)
                put("free text", theme, " ".join(cl), self.paint(t, "fill", theme, page), page, CONTRAST_TEXT)
            seen = set()
            for e in self.edges:
                if e["line"] is None or e["kind"] in seen:
                    continue
                seen.add(e["kind"])
                put("edge stroke vs page", theme, e["kind"], self.paint(e["line"], "stroke", theme, page), page,
                    CONTRAST_GRAPHIC)
            bands = {}
            for el in self.root.iter("rect"):
                if "sv-band" in classes(el):
                    k = next((x for x in classes(el) if x.startswith("sv-b-")), "band")
                    bands.setdefault(k, el)
            for k, el in bands.items():
                band = self.paint(el, "fill", theme, page)
                kinds_done = set()
                for n in self.nodes.values():
                    if n["box_el"] is None or n["kind"] in kinds_done:
                        continue
                    kinds_done.add(n["kind"])
                    put("node outline vs band", theme, f"{n['kind']} on {k}",
                        self.paint(n["box_el"], "stroke", theme, band), band, CONTRAST_GRAPHIC)
        for (group, theme, what), (r, fg, bg, need) in sorted(rows.items()):
            self.contrast_rows.append((group, theme, what, round(r, 2), fg, bg, need))
            if r < need:
                if group == "node text":
                    sev = "ERROR"
                elif need == CONTRAST_TEXT:
                    sev = "ERROR"
                else:
                    sev = "WARN"
                F.add(V, "contrast", sev, f"{theme}: {group} {what}: {r:.2f}:1 ({fg} on {bg}), needs {need:g}:1")

    def layout_metrics(self) -> None:
        m = self.metrics
        m["viewBox"] = f"{self.W:g} x {self.H:g}"
        m["render_width"] = self.render_w
        m["scale"] = round(self.scale, 4)
        m["screens_tall"] = round(self.H * self.scale / VIEWPORT_H, 1)
        m["nodes"], m["edges"], m["labels"] = len(self.nodes), len(self.edges), len(self.labels)
        m["node_rows"] = len(self.node_rows)
        bx = [n["box"] for n in self.nodes.values() if n["box"]]
        if bx:
            m["node_w"] = (round(min(b[2] for b in bx)), round(max(b[2] for b in bx)))
            m["node_h"] = (round(min(b[3] for b in bx)), round(max(b[3] for b in bx)))
        fills, lines = [], []
        for n in self.nodes.values():
            if not n["box"]:
                continue
            body = [t for t in n["texts"] if "sv-bt" not in classes(t)]
            lines.append(len(body))
            if body:
                last = max(fa(t, "y") for t in body) + 4
                content = (last - n["box"][1]) + (n["badge"][3] + 3 if n["badge"] else 0)
                fills.append(min(1.0, content / n["box"][3]))
        if fills:
            m["node_fill_median"] = round(statistics.median(fills), 2)
            m["nodes_under_half_full"] = sum(1 for f in fills if f < 0.5)
        if lines:
            m["text_lines_per_node_mean"] = round(statistics.mean(lines), 1)
            m["text_lines_per_node_max"] = max(lines)
        # lane order (captions top to bottom) and flow direction between node rows
        if self.is_timeline:
            ph: dict[float, list] = defaultdict(list)      # a wrapped phase caption shares one x
            for t in self.free_texts:
                if "sv-ph" in classes(t):
                    ph[round(fa(t, "x"), 1)].append((fa(t, "y"), norm_text(rendered_text(t))))
            m["lane_order"] = [" ".join(s for _, s in sorted(lines)) for _, lines in sorted(ph.items())]
        else:
            caps = sorted((fa(c["text"], "y"), fa(c["text"], "x"), norm_text(rendered_text(c["text"])))
                          for c in self.captions if "sv-cap" in classes(c["text"]))
            merged: list[list] = []
            for y, x, s in caps:
                if merged and abs(merged[-1][0] - y) < 0.5 and abs(merged[-1][1] - x) < 0.5:
                    merged[-1][2] += " " + s
                elif merged and abs(merged[-1][1] - x) < 0.5 and 0 < y - merged[-1][3] <= 14.5:
                    merged[-1][2] += " " + s
                    merged[-1][3] = y
                else:
                    merged.append([y, x, s, y])
            m["lane_order"] = [s for _, _, s, _ in merged]
            row_of = {n["id"]: self.node_rows.index(round(n["box"][1], 1)) for n in self.nodes.values() if n["box"]}
            flow = Counter()
            spans = []
            for e in self.edges:
                if e["frm"] in row_of and e["to"] in row_of:
                    d = row_of[e["to"]] - row_of[e["frm"]]
                    flow["up" if d < 0 else ("down" if d > 0 else "same row")] += 1
                    spans.append(abs(d))
            m["flow"] = dict(flow)
            m["row_span_mean"] = round(statistics.mean(spans), 2) if spans else 0
            m["edges_spanning_4plus_rows"] = sum(1 for s in spans if s >= 4)
        m["ra_nodes"] = sorted(n["id"] for n in self.nodes.values() if n["ra"])
        m["ra_edges"] = sum(1 for e in self.edges if e["ra"])


# ====================================================================== page-level checks
EXTERNAL = [("http(s) URL", r"https?://"),
            ("protocol-relative URL", r"""["'(=]\s*//[a-z0-9.-]+\.[a-z]{2,}"""),
            ("src= attribute", r"\bsrc\s*="),
            ("href= to a non-fragment", r"""\bhref\s*=\s*["']?(?!#)"""),
            ("@import", r"@import"),
            ("url() to a non-fragment", r"""url\(\s*["']?(?!#)"""),
            ("<link>", r"<link\b"), ("<img>", r"<img\b"), ("<iframe>", r"<iframe\b"),
            ("<object>/<embed>", r"<(?:object|embed)\b"), ("<base>", r"<base\b")]


def page_checks(text: str, css: CSS, F: Findings) -> list[str]:
    lines = []

    def res(ok: bool, msg: str, sev: str = "ERROR"):
        lines.append(f"[{'PASS' if ok else sev}] {msg}")
        if not ok:
            F.add("page", "page", sev, msg)
    hits = []
    for name, pat in EXTERNAL:
        for m in re.finditer(pat, text, re.I):
            hits.append(f"{name} at char {m.start()}: {text[max(0, m.start() - 30):m.start() + 50]!r}")
    res(not hits, f"no external URLs or remote references ({len(EXTERNAL)} patterns; {len(hits)} hits)")
    for h in hits[:10]:
        lines.append("       " + h)
    res(len(css.light) >= 10, f":root declares light tokens ({len(css.light)} custom properties)")
    res(bool(css.dark_media), f"@media (prefers-color-scheme: dark) redefines tokens ({len(css.dark_media)})")
    res(css.dark_media_guarded, 'dark media query is guarded by :root:not([data-theme="light"])')
    res(bool(css.dark_attr), f':root[data-theme="dark"] override present ({len(css.dark_attr)} tokens)')
    if css.dark_media and css.dark_attr:
        res(css.dark_media == css.dark_attr, "media-query dark tokens equal the data-theme dark tokens", "WARN")
    themed = set(css.dark_attr or css.dark_media)
    light_only = sorted(k for k in css.light if k not in themed and k != "--font")
    res(not light_only, f"every light token has a dark value (light-only: {light_only or 'none'})", "WARN")
    bg = css.decl("body", "background") or css.decl("body", "background-color")
    themes = css.themes()
    bg_ok = bool(bg) and all(parse_color(resolve(bg, themes[t])) is not None for t in themes)
    res(bg_ok, f"explicit body background ({bg!r}; light {resolve(bg, themes['light']) if bg else None}, "
               f"dark {resolve(bg, themes['dark']) if bg else None})")
    refs = set(re.findall(r"var\(\s*(--[\w-]+)", css.text))
    undefined = sorted(r for r in refs if r not in themes["light"] and r not in css.local_props)
    undefined_dark = sorted(r for r in refs if r not in themes["dark"] and r not in css.local_props)
    res(not undefined and not undefined_dark, f"every var() reference is defined in both themes "
                                              f"({len(refs)} names; undefined: {undefined + undefined_dark or 'none'})")
    small = sorted({float(v) for v in re.findall(r"font-size\s*:\s*([\d.]+)px", css.text) if float(v) < MIN_PX})
    res(not small, f"no CSS font-size below {MIN_PX:g}px (found: {small or 'none'})", "WARN")
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    words = len(m.group(1).split()) if m else 0
    res(bool(m) and 2 <= words <= 4, f"page <title> is a 2-4 word name ({m.group(1) if m else None!r})", "WARN")
    res(re.search(r'<meta[^>]+name="viewport"', text) is not None, "viewport meta present", "WARN")
    return lines


# ====================================================================== report
def fmt_metrics(m: dict) -> list[str]:
    keys = ["viewBox", "render_width", "scale", "screens_tall", "nodes", "edges", "labels", "node_rows",
            "node_w", "node_h", "node_fill_median", "nodes_under_half_full", "text_lines_per_node_mean",
            "text_lines_per_node_max", "min_effective_px", "crossings", "crossings_per_edge", "most_crossed",
            "bends_mean", "bends_max", "edge_len_mean", "edge_len_max", "edges_over_1000px",
            "label_hides_line_pairs", "line_px_hidden_under_labels", "bends_hidden_under_labels",
            "labels_detached", "shared_tracks", "edge_through_node", "edge_grazes_node", "port_crowding",
            "endpoint_stats", "flow", "row_span_mean", "edges_spanning_4plus_rows", "worst_into_padding",
            "ra_nodes", "ra_edges"]
    out = []
    for k in keys:
        if k in m:
            v = m[k]
            if isinstance(v, float):
                v = round(v, 2)
            if isinstance(v, dict):
                v = {a: (round(b, 1) if isinstance(b, float) else b) for a, b in v.items()}
            out.append(f"    {k:28s} {v}")
    if m.get("lane_order"):
        out.append("    lane order (top to bottom / left to right):")
        out += [f"      {i + 1:2d}. {s}" for i, s in enumerate(m["lane_order"])]
    return out


REQUIRED = [("overlap", "overlapping rectangles"), ("container-cut", "outlines cutting nodes"),
            ("clipping", "clipped by the viewBox"), ("text-fit", "text fit, 0.6 x font-size rule"),
            ("font-size", "effective size >= 11px"), ("edge-endpoints", "edge endpoints touch nodes"),
            ("edge-through-node", "edges never cross a box"), ("tooltips", "<title> on nodes/edges/labels"),
            ("ra-badge", "Real Assets badge shown"), ("contrast", "WCAG contrast (light + dark)")]
EXTRA = [("text-fit/segoe-ui", "text fit, installed Segoe UI metrics"), ("text-fit/browser", "text fit, headless browser"),
         ("port-crowding", "arrowheads not stacked"), ("shared-track", "no shared line tracks"),
         ("edge-grazes-node", "lines clear of box sides"), ("edge-under-label", "bends not hidden by labels"),
         ("edge-under-caption", "lines not hidden by captions"), ("label-placement", "labels sit on their line")]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Visual QA checker for the TPA Lab schematic HTML.")
    ap.add_argument("html", nargs="?", default=str(DEFAULT_HTML))
    ap.add_argument("--container", type=float, default=1400.0, help="container width in px (default 1400)")
    ap.add_argument("--fonts", default="auto", help="auto | off | folder holding the Segoe UI .ttf files")
    ap.add_argument("--browser", default="off", help="off | auto | path to msedge/chrome (true rendered widths)")
    ap.add_argument("--badge", default=DEFAULT_BADGE, help="expected Real Assets badge text")
    ap.add_argument("--cap", type=int, default=12, help="max findings printed per view and check")
    ap.add_argument("--verbose", action="store_true", help="print every contrast combination")
    ap.add_argument("--json", default=None, help="write all findings and metrics to this JSON file")
    opts = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    path = Path(opts.html)
    text = path.read_text(encoding="utf-8")
    F = Findings()
    m = re.search(r"<style[^>]*>(.*?)</style>", text, re.S)
    css = CSS(m.group(1) if m else "")
    themes = css.themes()

    fonts = None
    if opts.fonts != "off":
        fdir = Path(r"C:\Windows\Fonts") if opts.fonts == "auto" else Path(opts.fonts)
        fonts = FontBook(fdir)
        if not fonts.ok():
            fonts = None
    measured, bnote = browser_measure(opts.browser, text)

    print("TPA Lab schematic - visual QA checker")
    print(f"file      {path} ({len(text):,} chars)")
    print(f"container {opts.container:g}px; estimate {CHAR_FACTOR} x font-size per character "
          f"({NARROW_FACTOR} for narrow families); minimum {MIN_PX:g}px; contrast {CONTRAST_TEXT}:1 text, "
          f"{CONTRAST_GRAPHIC}:1 graphics")
    print(f"fonts     {'Segoe UI files: ' + ', '.join(sorted({f.name for f in fonts.faces.values()})) if fonts else 'off'}")
    print(f"browser   {bnote}")
    print("\n== Page ==")
    for line in page_checks(text, css, F):
        print("  " + line)

    views: list[View] = []
    headings = re.findall(r'<section class="panel"[^>]*id="panel-([\w-]+)"[^>]*>.*?<h2>(.*?)</h2>', text, re.S)
    head_of = {k: htmlmod.unescape(v) for k, v in headings}
    for mk in SVG_RE.finditer(text):
        markup = mk.group(0)
        root, how = parse_svg(markup)
        vid = (root.get("id") or f"svg{len(views)}").replace("svg-", "", 1)
        meas = measured.get(vid) if measured else None
        v = View(vid, head_of.get(vid, ""), root, how, css, themes, opts, F, fonts, meas)
        if measured is not None and (meas is None or len(meas) != len(v.text_index)):
            F.add(vid, "text-fit/browser", "WARN", "browser measurement does not line up with the parsed text; skipped")
            v.measured = None
        v.check_titles(opts.badge)
        v.check_overlaps()
        v.check_text()
        v.check_edges()
        v.check_routes()
        v.check_contrast()
        v.layout_metrics()
        views.append(v)

    print(f"\n== Views ({len(views)} inline SVGs) ==")
    print(f"  {'view':15s} {'viewBox':>13s} {'scale':>6s} {'nodes':>5s} {'edges':>5s} {'labels':>6s} "
          f"{'min px':>6s} {'cross':>5s} {'ERROR':>5s} {'WARN':>5s}  parser")
    for v in views:
        mm = v.metrics
        print(f"  {v.vid:15s} {mm['viewBox']:>13s} {mm['scale']:6.3f} {mm['nodes']:5d} {mm['edges']:5d} "
              f"{mm['labels']:6d} {mm['min_effective_px'] or 0:6.2f} {mm['crossings']:5d} "
              f"{F.n('ERROR', v.vid):5d} {F.n('WARN', v.vid):5d}  {v.how}")

    for v in views:
        print(f"\n== View: {v.vid} - {v.heading} ==")
        for group, title in (("required", REQUIRED), ("extra", EXTRA)):
            print(f"  {group} checks:")
            for check, desc in title:
                e, w = F.n("ERROR", v.vid, check), F.n("WARN", v.vid, check)
                if check.startswith("text-fit/") and not any(f["check"] == check for f in F.items) and (
                        (check.endswith("segoe-ui") and fonts is None) or (check.endswith("browser") and v.measured is None)):
                    status = "not run"
                else:
                    status = "PASS" if e == w == 0 else f"{e} error(s), {w} warning(s)"
                print(f"    {desc:40s} {status}")
        items = sorted((f for f in F.items if f["view"] == v.vid), key=lambda f: (SEV_RANK[f["sev"]], f["check"]))
        by_check: dict[str, list] = defaultdict(list)
        for f in items:
            by_check[(f["sev"], f["check"])].append(f["msg"])
        if by_check:
            print("  findings:")
        for (sev, check), msgs in by_check.items():
            print(f"    {sev} {check} ({len(msgs)})")
            for msg in msgs[:opts.cap]:
                print(f"      - {msg}")
            if len(msgs) > opts.cap:
                print(f"      ... and {len(msgs) - opts.cap} more")
        if opts.verbose:
            print("  contrast (lowest ratio per combination):")
            rows = v.contrast_rows
        else:
            print("  contrast (lowest ratio per group and theme; --verbose lists every combination):")
            low: dict[tuple, tuple] = {}
            for row in v.contrast_rows:
                k = (row[0], row[1])
                if k not in low or row[3] < low[k][3]:
                    low[k] = row
            rows = sorted(set(low.values()) | {r for r in v.contrast_rows if r[3] < r[6]})
        for group, theme, what, r, fg, bg, need in rows:
            flag = "" if r >= need else "   << below " + f"{need:g}:1"
            print(f"    {theme:5s} {group:22s} {what:34s} {r:6.2f}:1  {fg} on {bg}{flag}")
        print("  layout metrics:")
        for line in fmt_metrics(v.metrics):
            print(line)

    ne, nw = F.n("ERROR"), F.n("WARN")
    print(f"\n== Totals ==\n  {ne} error(s), {nw} warning(s) across {len(views)} views")
    if opts.json:
        Path(opts.json).write_text(json.dumps({
            "file": str(path), "container": opts.container, "browser": bnote,
            "findings": F.items,
            "views": {v.vid: {"metrics": v.metrics, "contrast": v.contrast_rows} for v in views}},
            ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        print(f"  JSON written to {opts.json}")
    return 1 if ne else 0


if __name__ == "__main__":
    sys.exit(main())
