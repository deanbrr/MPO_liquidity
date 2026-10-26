/* ADIC Total Portfolio Platform - stakeholder demo (self-contained: no network, no libraries).
   Every number comes from the embedded engine run (build_demo.py). The scenario controls re-weight the certified
   out-of-sample paths live (world probabilities, hurdle) and switch between precomputed stresses; plans themselves
   were optimized by the engine at each group's own view. */
(() => {
  "use strict";
  const D = JSON.parse(document.getElementById("tpp-data").textContent);
  const ROLES = ["strategy", "balance_sheet", "liquidity", "asset_allocation"];
  const TABS = ROLES.concat(["ic", "yale", "data"]);
  const TITLE = { strategy: "Strategy", balance_sheet: "Balance Sheet", liquidity: "Liquidity",
    asset_allocation: "Asset Allocation", ic: "Investment Committee", yale: "Yale model", data: "Data & method" };
  const WORLDS = ["Downside", "Base", "Upside"];
  const YEARS = ["Today", "Y1", "Y2", "Y3", "Y4", "Y5"];
  const FLOWYEARS = ["Y1", "Y2", "Y3", "Y4", "Y5"];
  const MINUS = "−";

  // ------------------------------------------------------------------ formatting
  const ok = (x) => x !== null && x !== undefined && isFinite(x);
  const sgn = (x) => (x < 0 ? MINUS : "+");
  const F = {
    pct: (x, d = 1) => (ok(x) ? (x < 0 ? MINUS : "") + Math.abs(x * 100).toFixed(d) + "%" : "–"),
    spct: (x, d = 1) => (ok(x) ? sgn(x) + Math.abs(x * 100).toFixed(d) + "%" : "–"),
    pp: (x, d = 1) => (ok(x) ? (+(x * 100).toFixed(d) === 0 ? (0).toFixed(d) + "pp" : sgn(x) + Math.abs(x * 100).toFixed(d) + "pp") : "–"),
    bn: (x, d = 1) => (ok(x) ? (x < 0 ? MINUS : "") + "$" + Math.abs(x).toFixed(d) + "bn" : "–"),
    sbn: (x, d = 1) => (ok(x) ? sgn(x) + "$" + Math.abs(x).toFixed(d) + "bn" : "–"),
    x: (x, d = 2) => (ok(x) ? x.toFixed(d) + "×" : "–"),
    n: (x, d = 2) => (ok(x) ? (x < 0 ? MINUS : "") + Math.abs(x).toFixed(d) : "–"),
    int: (x) => (ok(x) ? Math.round(x).toLocaleString("en-US") : "–"),
  };

  // ------------------------------------------------------------------ DOM helpers
  function el(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    if (attrs) for (const [k, v] of Object.entries(attrs)) {
      if (v === undefined || v === null || v === false) continue;
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k === "html") e.innerHTML = v;            // static markup authored here only, never data
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : v);
    }
    for (const k of kids.flat()) if (k !== null && k !== undefined && k !== false) e.append(k instanceof Node ? k : document.createTextNode(String(k)));
    return e;
  }
  const NS = "http://www.w3.org/2000/svg";
  function s(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    if (attrs) for (const [k, v] of Object.entries(attrs)) if (v !== undefined && v !== null) e.setAttribute(k, v);
    if (parent) parent.appendChild(e);
    return e;
  }
  function stext(parent, x, y, str, attrs) {
    const t = s("text", Object.assign({ x, y }, attrs || {}), parent);
    t.textContent = str;
    return t;
  }
  const cssv = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const tip = document.getElementById("tip");
  function showTip(evt, title, rows) {
    tip.replaceChildren();
    if (title) tip.append(el("div", { class: "t", text: title }));
    for (const r of rows) {
      const row = el("div", { class: "r" });
      if (r.color) row.append(el("span", { class: "key", style: `background:${r.color}` }));
      row.append(el("span", { class: "v", text: r.value }), el("span", { class: "n", text: r.name }));
      tip.append(row);
    }
    tip.style.display = "block";
    const pad = 14, w = tip.offsetWidth, h = tip.offsetHeight;
    let x = evt.clientX + pad, y = evt.clientY + pad;
    if (x + w > window.innerWidth - 8) x = evt.clientX - w - pad;
    if (y + h > window.innerHeight - 8) y = evt.clientY - h - pad;
    tip.style.left = x + "px";
    tip.style.top = y + "px";
  }
  const hideTip = () => { tip.style.display = "none"; };

  // ------------------------------------------------------------------ per-path results (live statistics)
  const TWR = new Map();
  function twr(b64) {
    if (!b64) return null;
    if (TWR.has(b64)) return TWR.get(b64);
    const bin = atob(b64);
    const n = bin.length / 2;
    const a = new Float32Array(n);
    for (let i = 0; i < n; i++) {
      let v = bin.charCodeAt(2 * i) | (bin.charCodeAt(2 * i + 1) << 8);
      if (v >= 32768) v -= 65536;
      a[i] = v / 1e4;
    }
    const order = Array.from(a.keys()).sort((i, j) => a[i] - a[j]);
    const rec = { a, order, n: n / 3 };
    TWR.set(b64, rec);
    return rec;
  }
  function stats(rec, pi, h) {
    const { a, order, n } = rec;
    const bw = [0, 0, 0], mw = [0, 0, 0];
    for (let w = 0; w < 3; w++) {
      let c = 0, sum = 0;
      for (let j = 0; j < n; j++) { const v = a[w * n + j]; if (v >= h - 1e-9) c++; sum += v; }
      bw[w] = c / n; mw[w] = sum / n;
    }
    const pg = pi[0] * bw[0] + pi[1] * bw[1] + pi[2] * bw[2];
    const mean = pi[0] * mw[0] + pi[1] * mw[1] + pi[2] * mw[2];
    const wt = (i) => pi[Math.floor(i / n)] / n;
    const q = (p) => { let acc = 0; for (const i of order) { acc += wt(i); if (acc >= p) return a[i]; } return a[order[order.length - 1]]; };
    const cvar = (lvl) => { let acc = 0, s2 = 0; for (const i of order) { const w = Math.min(wt(i), lvl - acc); if (w <= 0) break; s2 += w * a[i]; acc += w; } return s2 / lvl; };
    const neff = n / (pi[0] ** 2 + pi[1] ** 2 + pi[2] ** 2);
    return { pg, bw, mean, mw, cvar10: cvar(0.10), cvar1: cvar(0.01), p5: q(0.05), p50: q(0.5), p95: q(0.95), neff, ci: wilson(pg, neff) };
  }
  // per-path objective bits (tpp.metrics.OBJ_*): 1 Balance Sheet, 2 Liquidity, 4 Asset Allocation; the Strategy
  // group's objective, the hurdle, is tested from the TWR so the hurdle control moves it
  const FLAGS = new Map();
  function flags(b64) {
    if (!b64) return null;
    if (FLAGS.has(b64)) return FLAGS.get(b64);
    const bin = atob(b64), a = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i);
    FLAGS.set(b64, a);
    return a;
  }
  const OBJ_KEYS = ["goal", "bs", "liq", "aa", "all", "goal_bs", "goal_liq", "goal_aa"];
  // ref: the status quo's paths for the same case (null for the status quo itself), for the Asset Allocation test
  function objStats(rec, fl, pi, h, ref) {
    const n = rec.n, a = rec.a, out = Object.fromEntries(OBJ_KEYS.map((k) => [k, 0]));
    for (let w = 0; w < 3; w++) {
      const c = Object.fromEntries(OBJ_KEYS.map((k) => [k, 0]));
      for (let j = 0; j < n; j++) {
        const i = w * n + j, g = a[i] >= h - 1e-9, f = fl ? fl[i] : 7;
        const bs = (f & 1) > 0, lq = (f & 2) > 0, aa = ref ? g || ref.a[i] < h - 1e-9 : true;
        c.goal += g; c.bs += bs; c.liq += lq; c.aa += aa;
        c.all += g && bs && lq && aa; c.goal_bs += g && bs; c.goal_liq += g && lq; c.goal_aa += g && aa;
      }
      for (const k of OBJ_KEYS) out[k] += (pi[w] * c[k]) / n;
    }
    return out;
  }
  function wilson(p, n, z = 1.959964) {
    const den = 1 + (z * z) / n;
    const c = (p + (z * z) / (2 * n)) / den;
    const hw = (z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n))) / den;
    return [c - hw, c + hw];
  }
  function paired(recA, recB, pi, h) {
    const n = recA.n;
    let m = 0, v = 0;
    for (let w = 0; w < 3; w++) {
      let s1 = 0, s2 = 0;
      for (let j = 0; j < n; j++) {
        const d = (recA.a[w * n + j] >= h - 1e-9 ? 1 : 0) - (recB.a[w * n + j] >= h - 1e-9 ? 1 : 0);
        s1 += d; s2 += d * d;
      }
      const mu = s1 / n;
      m += pi[w] * mu;
      v += (pi[w] ** 2) * Math.max(s2 / n - mu * mu, 0) / n;
    }
    const se = Math.sqrt(v);
    return { d: m, ci: [m - 1.96 * se, m + 1.96 * se] };
  }
  function histo(rec, pi) {
    const edges = D.meta.hist_edges;
    const nb = edges.length - 1, out = new Array(nb).fill(0);
    const { a, n } = rec;
    for (let i = 0; i < a.length; i++) {
      const v = Math.min(Math.max(a[i], edges[0]), edges[nb] - 1e-9);
      let b = Math.floor(((v - edges[0]) / (edges[nb] - edges[0])) * nb);
      b = Math.min(Math.max(b, 0), nb - 1);
      out[b] += pi[Math.floor(i / n)] / n;
    }
    return out;
  }

  // ------------------------------------------------------------------ state
  const viewPi = (tab) => {
    const p = tab === "ic" ? D.ic.view.prefs.scenario_probs : (D.roles[tab] ? D.roles[tab].prefs.scenario_probs : D.ic.view.prefs.scenario_probs);
    return WORLDS.map((w) => p[w]);
  };
  const viewStress = (tab) => (D.roles[tab] ? D.roles[tab].stress : "base");
  const st = {
    tab: document.documentElement.getAttribute("data-default-role") || "strategy",
    pi: {}, stress: {}, hurdle: D.meta.goal_rate, theme: null, aa: null,
  };
  for (const t of TABS) { st.pi[t] = viewPi(t); st.stress[t] = viewStress(t); }
  const hashTab = (location.hash || "").replace("#", "");
  if (TABS.includes(hashTab)) st.tab = hashTab;
  if (!TABS.includes(st.tab)) st.tab = "strategy";
  // deep links: ?pi=40,45,15&hurdle=9&stress=oil_crash set the opening controls of the opening view
  const qs = new URLSearchParams(location.search);
  if (qs.get("pi")) {
    const v = qs.get("pi").split(",").map(Number);
    if (v.length === 3 && v.every((x) => x >= 0) && v.some((x) => x > 0)) { const sum = v[0] + v[1] + v[2]; st.pi[st.tab] = v.map((x) => x / sum); }
  }
  if (qs.get("hurdle")) { const hv = Number(qs.get("hurdle")); if (hv > 0 && hv < 30) st.hurdle = hv / 100; }
  if (qs.get("stress") && D.stresses[qs.get("stress")] && st.tab !== "ic" && st.tab !== "data") st.stress[st.tab] = qs.get("stress");
  if (["light", "dark"].includes(qs.get("theme"))) document.documentElement.setAttribute("data-theme", qs.get("theme"));
  const piNow = () => st.pi[st.tab];
  const hurdle = () => st.hurdle;

  // ------------------------------------------------------------------ chart kit (SVG, viewBox-scaled)
  const C = { w: 640, padL: 52, padR: 72, padT: 14, padB: 30 };
  function frame(host, h, opts = {}) {
    const svg = s("svg", { viewBox: `0 0 ${C.w} ${h}`, role: "img", "aria-label": opts.label || "chart" });
    host.append(svg);
    return svg;
  }
  function niceTicks(lo, hi, n = 5) {
    if (!(hi > lo)) { hi = lo + 1; }
    const span = hi - lo, raw = span / n, mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((x) => span / x <= n) || 10 * mag;
    const t0 = Math.ceil(lo / step - 1e-9) * step, out = [];
    for (let v = t0; v <= hi + step * 1e-9; v += step) out.push(+v.toFixed(10));
    return out;
  }
  // A scale domain that always covers the data (ticks extended outward to whole steps), with optional headroom
  function domain(lo, hi, n = 5, padLo = 0, padHi = 0) {
    if (!(hi > lo)) { const e = Math.abs(lo) * 0.05 || 0.01; lo -= e; hi += e; }
    const span = hi - lo, nonneg = lo >= 0, nonpos = hi <= 0;
    lo -= span * padLo; hi += span * padHi;
    if (nonneg) lo = Math.max(lo, 0);            // padding never invents a negative (or positive) region
    if (nonpos) hi = Math.min(hi, 0);
    const ticks = niceTicks(lo, hi, n);
    const step = ticks.length > 1 ? ticks[1] - ticks[0] : span;
    while (ticks[0] > lo + step * 1e-9) ticks.unshift(+(ticks[0] - step).toFixed(10));
    while (ticks[ticks.length - 1] < hi - step * 1e-9) ticks.push(+(ticks[ticks.length - 1] + step).toFixed(10));
    return { lo: ticks[0], hi: ticks[ticks.length - 1], ticks };
  }
  // Greedy label placement: right of the point, then left, above, below; never off the viewBox
  function placeLabel(boxes, px, py, label, w) {
    const tw = label.length * 6.1 + 4, th = 12;
    const cands = [[px + 10, py + 4, "start"], [px - 10, py + 4, "end"], [px - tw / 2, py - 10, "start"], [px - tw / 2, py + 18, "start"],
      [px + 8, py - 8, "start"], [px + 8, py + 16, "start"], [px - 8, py - 8, "end"], [px - 8, py + 16, "end"],
      [px + 10, py - 20, "start"], [px - 10, py - 20, "end"], [px + 10, py + 28, "start"], [px - 10, py + 28, "end"]];
    for (const [x, y, anchor] of cands) {
      const left = anchor === "end" ? x - tw : x, right = left + tw;
      if (left < 2 || right > w - 2) continue;
      const box = [left, y - th + 2, right, y + 2];
      if (!boxes.some((b) => !(box[2] < b[0] || box[0] > b[2] || box[3] < b[1] || box[1] > b[3]))) { boxes.push(box); return { x, y, anchor }; }
    }
    return null;
  }
  function yAxis(svg, y, ticks, fmt, x0, x1) {
    for (const t of ticks) {
      s("line", { x1: x0, x2: x1, y1: y(t), y2: y(t), stroke: cssv("--grid"), "stroke-width": 1 }, svg);
      stext(svg, x0 - 8, y(t) + 4, fmt(t), { "text-anchor": "end", "font-size": 11, fill: cssv("--text-muted") });
    }
  }
  function xLabels(svg, xs, labels, yPos) {
    labels.forEach((lb, i) => stext(svg, xs(i), yPos, lb, { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-muted") }));
  }
  function legend(items) {
    const lg = el("div", { class: "legend" });
    for (const it of items) {
      const k = el("span", { class: "k" });
      const cls = it.kind === "line" ? "ln" : it.kind === "band" ? "band" : "sw";
      k.append(el("span", { class: cls, style: `background:${it.color}` }), el("span", { text: it.name }));
      lg.append(k);
    }
    return lg;
  }
  function tableView(cols, rows) {
    const t = el("table", { class: "t" });
    const tr = el("tr");
    cols.forEach((c, i) => tr.append(el("th", { class: i ? "num" : "", text: c })));
    t.append(el("thead", null, tr));
    const tb = el("tbody");
    for (const r of rows) {
      const row = el("tr");
      r.forEach((v, i) => row.append(el("td", { class: i ? "num" : "", text: v })));
      tb.append(row);
    }
    t.append(tb);
    return el("div", { class: "tablewrap short" }, t);
  }
  // A card that holds a chart and its table-view twin
  function chartCard(title, sub, build, table, cls) {
    const host = el("div", { class: "chart" });
    const tv = el("div", { class: "hidden" });
    const btn = el("button", { class: "btn", text: "Table", "aria-pressed": "false",
      onclick: () => { const on = tv.classList.toggle("hidden"); host.classList.toggle("hidden", !on); btn.classList.toggle("on", !on); btn.setAttribute("aria-pressed", String(!on)); } });
    const card = el("div", { class: "card" + (cls ? " " + cls : "") },
      el("div", { class: "head" }, el("div", null, el("h3", { text: title }), sub ? el("p", { class: "sub", text: sub }) : null), table ? el("div", { class: "tools" }, btn) : null),
      host, tv);
    requestAnimationFrame(() => { build(host); if (table) { const t = table(); tv.append(t.cols ? tableView(t.cols, t.rows) : t); } });
    return card;
  }

  // Fan chart: bands (P5-95, P25-75) and median for each fan series; plain lines; reference lines
  function fanChart(host, o) {
    const h = o.h || 250;
    const xsN = o.labels.length;
    const vals = [];
    for (const sr of o.fans || []) for (const k of ["p5", "p95", "p50"]) vals.push(...sr.fan[k]);
    for (const ln of o.lines || []) vals.push(...ln.values);
    for (const r of o.refs || []) vals.push(...(Array.isArray(r.values) ? r.values : [r.y]));
    let lo = Math.min(...vals.filter(ok)), hi = Math.max(...vals.filter(ok));
    if (o.zero) lo = Math.min(lo, 0);
    const dm = domain(lo, hi, 5, 0.04, 0.06), ticks = dm.ticks;
    lo = dm.lo; hi = dm.hi;
    const svg = frame(host, h, { label: o.title });
    const x0 = C.padL, x1 = C.w - C.padR, y0 = h - C.padB, y1 = C.padT;
    const x = (i) => x0 + (i * (x1 - x0)) / (xsN - 1);
    const y = (v) => y0 - ((v - lo) / (hi - lo)) * (y0 - y1);
    yAxis(svg, y, ticks, o.yfmt, x0, x1);
    xLabels(svg, x, o.labels, h - 10);
    const path = (arr) => arr.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join("");
    const area = (a, b) => path(a) + b.slice().reverse().map((v, i) => `L${x(b.length - 1 - i).toFixed(1)},${y(v).toFixed(1)}`).join("") + "Z";
    for (const r of o.refs || []) {
      const arr = Array.isArray(r.values) ? r.values : new Array(xsN).fill(r.y);
      const ra = { d: path(arr), fill: "none", stroke: r.color || cssv("--axis"), "stroke-width": 1.5 };
      if (r.dash) ra["stroke-dasharray"] = "5 4";
      s("path", ra, svg);
    }
    const ends = (o.refs || []).map((r) => ({ v: Array.isArray(r.values) ? r.values[xsN - 1] : r.y, name: r.label, ref: true }));
    for (const sr of o.fans || []) {
      const c = sr.color;
      s("path", { d: area(sr.fan.p5, sr.fan.p95), fill: sr.wash || "var(--wash-1)", stroke: "none" }, svg);
      s("path", { d: area(sr.fan.p25, sr.fan.p75), fill: sr.wash2 || "var(--wash-1b)", stroke: "none" }, svg);
      s("path", { d: path(sr.fan.p50), fill: "none", stroke: c, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }, svg);
      ends.push({ v: sr.fan.p50[xsN - 1], name: sr.name });
    }
    for (const ln of o.lines || []) {
      s("path", { d: path(ln.values), fill: "none", stroke: ln.color, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }, svg);
      ends.push({ v: ln.values[xsN - 1], name: ln.name });
    }
    // end labels, stacked 13px apart when they would collide (the legend carries identity)
    ends.sort((a, b) => y(a.v) - y(b.v));
    let last = -1e9;
    for (const e of ends) {
      const yy = Math.max(y(e.v), last + 13);
      stext(svg, x1 + 6, yy + 4, e.ref ? e.name : `${e.name.length <= 10 ? e.name : e.name.split(" ")[0]} ${o.yfmt(e.v)}`, { "font-size": 11, fill: e.ref ? cssv("--text-muted") : cssv("--text-secondary") });
      last = yy;
    }
    // crosshair
    const cross = s("line", { y1: y1, y2: y0, stroke: cssv("--axis"), "stroke-width": 1, visibility: "hidden" }, svg);
    const hit = s("rect", { x: x0, y: y1, width: x1 - x0, height: y0 - y1, fill: "transparent" }, svg);
    hit.addEventListener("pointermove", (ev) => {
      const r = svg.getBoundingClientRect(), px = ((ev.clientX - r.left) / r.width) * C.w;
      const i = Math.max(0, Math.min(xsN - 1, Math.round(((px - x0) / (x1 - x0)) * (xsN - 1))));
      cross.setAttribute("x1", x(i)); cross.setAttribute("x2", x(i)); cross.setAttribute("visibility", "visible");
      const rows = [];
      for (const sr of o.fans || []) rows.push({ color: sr.color, value: `${o.yfmt(sr.fan.p50[i])}  (${o.yfmt(sr.fan.p5[i])} to ${o.yfmt(sr.fan.p95[i])})`, name: sr.name + ", median (P5 to P95)" });
      for (const ln of o.lines || []) rows.push({ color: ln.color, value: o.yfmt(ln.values[i]), name: ln.name });
      for (const r2 of o.refs || []) rows.push({ color: cssv("--axis"), value: o.yfmt(Array.isArray(r2.values) ? r2.values[i] : r2.y), name: r2.label });
      showTip(ev, o.labels[i], rows);
    });
    hit.addEventListener("pointerleave", () => { cross.setAttribute("visibility", "hidden"); hideTip(); });
  }

  // Histogram: first series as thin columns, the others as step lines; optional marker
  function histChart(host, o) {
    const h = o.h || 230, edges = o.edges, nb = edges.length - 1;
    const dm = domain(0, Math.max(...o.series.flatMap((sr) => sr.p)) || 0.01, 4, 0, 0.12);
    const maxv = dm.hi, ticks = dm.ticks;
    const svg = frame(host, h, { label: o.title });
    const x0 = C.padL, x1 = C.w - 24, y0 = h - C.padB, y1 = C.padT;
    const x = (v) => x0 + ((v - edges[0]) / (edges[nb] - edges[0])) * (x1 - x0);
    const y = (v) => y0 - (v / maxv) * (y0 - y1);
    yAxis(svg, y, ticks, (t) => F.pct(t, 0), x0, x1);
    for (const t of niceTicks(edges[0], edges[nb], 7)) stext(svg, x(t), h - 10, F.pct(t, 0), { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-muted") });
    const bw = (x1 - x0) / nb;
    const main = o.series[0];
    main.p.forEach((v, i) => {
      if (v <= 0) return;
      const bx = x(edges[i]) + 1, ww = Math.max(bw - 2, 1), top = y(v), r = Math.min(4, ww / 2);
      s("path", { d: `M${bx},${y0}L${bx},${top + r}Q${bx},${top} ${bx + r},${top}L${bx + ww - r},${top}Q${bx + ww},${top} ${bx + ww},${top + r}L${bx + ww},${y0}Z`, fill: main.color }, svg);
    });
    for (const sr of o.series.slice(1)) {
      let d = "";
      sr.p.forEach((v, i) => { d += `${i ? "L" : "M"}${x(edges[i]).toFixed(1)},${y(v).toFixed(1)}L${x(edges[i + 1]).toFixed(1)},${y(v).toFixed(1)}`; });
      s("path", { d, fill: "none", stroke: sr.color, "stroke-width": 2, "stroke-linejoin": "round" }, svg);
    }
    s("line", { x1: x0, x2: x1, y1: y0, y2: y0, stroke: cssv("--axis"), "stroke-width": 1 }, svg);
    // the end bins hold the tails: everything below the second edge, everything above the second-to-last
    const tailLab = (i, txt, anchor) => {
      const v = Math.max(...o.series.map((sr) => sr.p[i] || 0));
      if (v > 0) stext(svg, x(edges[i]) + bw / 2, y(v) - 6, txt, { "text-anchor": anchor, "font-size": 10, fill: cssv("--text-muted") });
    };
    tailLab(0, "≤" + F.pct(edges[1], 0), "start");
    tailLab(nb - 1, "≥" + F.pct(edges[nb - 1], 0), "end");
    if (o.marker) {
      const mx = x(o.marker.x);
      s("line", { x1: mx, x2: mx, y1: y1 - 4, y2: y0, stroke: cssv("--text-secondary"), "stroke-width": 1.5 }, svg);
      stext(svg, mx + 5, y1 + 8, o.marker.label, { "font-size": 11, fill: cssv("--text-secondary") });
    }
    const hit = s("rect", { x: x0, y: y1, width: x1 - x0, height: y0 - y1, fill: "transparent" }, svg);
    hit.addEventListener("pointermove", (ev) => {
      const r = svg.getBoundingClientRect(), px = ((ev.clientX - r.left) / r.width) * C.w;
      const i = Math.max(0, Math.min(nb - 1, Math.floor(((px - x0) / (x1 - x0)) * nb)));
      const lbl = i === 0 ? `5-year return below ${F.pct(edges[1], 0)}` : i === nb - 1 ? `5-year return ${F.pct(edges[i], 0)} or more` : `5-year return ${F.pct(edges[i], 0)} to ${F.pct(edges[i + 1], 0)}`;
      showTip(ev, lbl, o.series.map((sr) => ({ color: sr.color, value: F.pct(sr.p[i], 1), name: sr.name + " (probability)" })));
    });
    hit.addEventListener("pointerleave", hideTip);
  }

  // Horizontal bars: rows x series (<= 3); values may be negative (bars grow from zero)
  function barsH(host, o) {
    const rows = o.rows, ns = o.series.length;
    const band = ns > 1 ? 14 * ns + 12 : 26, h = C.padT + rows.length * band + 26;
    const vals = rows.flatMap((r) => r.values.filter(ok));
    let lo = Math.min(0, ...vals), hi = Math.max(0, ...vals);
    const dm = domain(lo, hi, 4, lo < 0 ? 0.22 : 0, hi > 0 ? 0.10 : 0);   // headroom so value labels clear the bars
    lo = dm.lo; hi = dm.hi;
    const labW = o.labelW || 210;
    const svg = frame(host, h, { label: o.title });
    const x0 = labW, x1 = C.w - 64, y0 = h - 22;
    const x = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0);
    const ticks = dm.ticks;
    for (const t of ticks) {
      s("line", { x1: x(t), x2: x(t), y1: C.padT - 4, y2: y0, stroke: t === 0 ? cssv("--axis") : cssv("--grid"), "stroke-width": 1 }, svg);
      stext(svg, x(t), h - 6, o.fmt(t), { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-muted") });
    }
    rows.forEach((r, ri) => {
      const top = C.padT + ri * band;
      const lab = r.short || r.label, maxc = Math.floor((labW - 16) / 6.4);
      stext(svg, labW - 10, top + band / 2 + 4, lab.length > maxc ? lab.slice(0, maxc - 1) + "…" : lab, { "text-anchor": "end", "font-size": 11.5, fill: cssv("--text-secondary") });
      r.values.forEach((v, si) => {
        if (!ok(v)) return;
        const th = ns > 1 ? 12 : 16, by = top + (ns > 1 ? 6 + si * 14 : (band - th) / 2);
        const a = x(Math.min(0, v)), b = x(Math.max(0, v)), wpx = Math.max(b - a, 1), rr = Math.min(4, wpx / 2);
        const pos = v >= 0;
        const d = pos
          ? `M${a},${by}L${b - rr},${by}Q${b},${by} ${b},${by + rr}L${b},${by + th - rr}Q${b},${by + th} ${b - rr},${by + th}L${a},${by + th}Z`
          : `M${b},${by}L${a + rr},${by}Q${a},${by} ${a},${by + rr}L${a},${by + th - rr}Q${a},${by + th} ${a + rr},${by + th}L${b},${by + th}Z`;
        const color = (o.colorFn ? o.colorFn(v, si, r) : o.series[si].color);
        const bar = s("path", { d, fill: color }, svg);
        const lx = pos ? b + 5 : a - 5;
        if (o.labelSeries === undefined || o.labelSeries === si) stext(svg, lx, by + th - 3, o.fmt(v) + (r.note && si === 0 ? " · " + r.note : ""), { "text-anchor": pos ? "start" : "end", "font-size": 11, fill: cssv("--text-secondary") });
        const hit = s("rect", { x: x0 - 4, y: top, width: x1 - x0 + 8, height: band, fill: "transparent" }, svg);
        hit.addEventListener("pointermove", (ev) => showTip(ev, r.label, o.series.map((sr, k) => ({ color: o.colorFn ? o.colorFn(r.values[k], k, r) : sr.color, value: o.fmt(r.values[k]), name: sr.name }))));
        hit.addEventListener("pointerleave", hideTip);
      });
    });
  }

  // Vertical columns by category: grouped (<= 3 series) or stacked (signed: positive above, negative below zero)
  function colsChart(host, o) {
    const h = o.h || 240, cats = o.cats, ns = o.series.length;
    const svg = frame(host, h, { label: o.title });
    const x0 = C.padL, x1 = C.w - 18, y0 = h - C.padB, y1 = C.padT;
    let lo = 0, hi = 0;
    if (o.stacked) {
      cats.forEach((_, ci) => { let p = 0, n2 = 0; o.series.forEach((sr) => { const v = sr.values[ci] || 0; if (v >= 0) p += v; else n2 += v; }); hi = Math.max(hi, p); lo = Math.min(lo, n2); });
    } else {
      for (const sr of o.series) for (const v of sr.values) if (ok(v)) { hi = Math.max(hi, v); lo = Math.min(lo, v); }
    }
    for (const ln of o.lines || []) for (const v of ln.values) if (ok(v)) { hi = Math.max(hi, v); lo = Math.min(lo, v); }
    for (const r of o.refs || []) { hi = Math.max(hi, r.y); lo = Math.min(lo, r.y); }
    const dm = domain(lo, hi || 1, 5, 0, 0.05), ticks = dm.ticks;
    lo = dm.lo; hi = dm.hi;
    const y = (v) => y0 - ((v - lo) / (hi - lo)) * (y0 - y1);
    yAxis(svg, y, ticks, o.fmt, x0, x1);
    const bandW = (x1 - x0) / cats.length;
    const cx = (i) => x0 + bandW * (i + 0.5);
    cats.forEach((c, i) => { if (cats.length <= 16 || i % 2 === 0) stext(svg, cx(i), h - 10, c, { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-muted") }); });
    const colPath = (bx, ww, ya, yb, roundTop) => {
      const top = Math.min(ya, yb), bot = Math.max(ya, yb), r = Math.min(4, ww / 2, (bot - top) / 2);
      if (roundTop) return `M${bx},${bot}L${bx},${top + r}Q${bx},${top} ${bx + r},${top}L${bx + ww - r},${top}Q${bx + ww},${top} ${bx + ww},${top + r}L${bx + ww},${bot}Z`;
      return `M${bx},${top}L${bx + ww},${top}L${bx + ww},${bot - r}Q${bx + ww},${bot} ${bx + ww - r},${bot}L${bx + r},${bot}Q${bx},${bot} ${bx},${bot - r}Z`;
    };
    cats.forEach((cat, ci) => {
      if (o.stacked) {
        const ww = Math.min(24, bandW * 0.6), bx = cx(ci) - ww / 2;
        let p = 0, n2 = 0;
        const posIdx = o.series.map((sr, k) => k).filter((k) => (o.series[k].values[ci] || 0) > 0);
        const negIdx = o.series.map((sr, k) => k).filter((k) => (o.series[k].values[ci] || 0) < 0);
        posIdx.forEach((k, j) => { const v = o.series[k].values[ci]; const ya = y(p), yb = y(p + v) + (j < posIdx.length - 1 ? 0 : 0); s("path", { d: colPath(bx, ww, ya - (j ? 1 : 0), yb + 1, j === posIdx.length - 1), fill: o.series[k].color }, svg); p += v; });
        negIdx.forEach((k, j) => { const v = o.series[k].values[ci]; const ya = y(n2), yb = y(n2 + v); s("path", { d: colPath(bx, ww, ya + (j ? 1 : 0), yb - 1, false), fill: o.series[k].color }, svg); n2 += v; });
      } else {
        const ww = Math.min(24, (bandW * 0.8) / ns - 2);
        o.series.forEach((sr, k) => {
          const v = sr.values[ci]; if (!ok(v) || v === 0) return;
          const bx = cx(ci) - (ns * (ww + 2)) / 2 + k * (ww + 2);
          s("path", { d: colPath(bx, ww, y(0), y(v), v > 0), fill: sr.color }, svg);
        });
      }
      const hit = s("rect", { x: cx(ci) - bandW / 2, y: y1, width: bandW, height: y0 - y1, fill: "transparent" }, svg);
      hit.addEventListener("pointermove", (ev) => showTip(ev, (o.catTitle || "") + cat, o.series.map((sr) => ({ color: sr.color, value: o.fmt(sr.values[ci]), name: sr.name })).concat((o.lines || []).map((ln) => ({ color: ln.color, value: o.fmt(ln.values[ci]), name: ln.name })))));
      hit.addEventListener("pointerleave", hideTip);
    });
    s("line", { x1: x0, x2: x1, y1: y(0), y2: y(0), stroke: cssv("--axis"), "stroke-width": 1 }, svg);
    for (const ln of o.lines || []) {
      const d = ln.values.map((v, i) => `${i ? "L" : "M"}${cx(i).toFixed(1)},${y(v).toFixed(1)}`).join("");
      s("path", { d, fill: "none", stroke: ln.color, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }, svg);
      ln.values.forEach((v, i) => { if (ok(v)) s("circle", { cx: cx(i), cy: y(v), r: 4, fill: ln.color, stroke: cssv("--surface-1"), "stroke-width": 2 }, svg); });
    }
    for (const r of o.refs || []) {
      s("line", { x1: x0, x2: x1, y1: y(r.y), y2: y(r.y), stroke: cssv("--text-secondary"), "stroke-width": 1.5, "stroke-dasharray": "5 4" }, svg);
      stext(svg, x1 - 4, y(r.y) - 5, r.label, { "text-anchor": "end", "font-size": 11, fill: cssv("--text-secondary") });
    }
  }

  // Lines over a numeric x axis (borrowing in $bn), with horizontal and vertical reference lines
  function lineXY(host, o) {
    const h = o.h || 260, svg = frame(host, h, { label: o.title });
    const x0 = C.padL, x1 = C.w - 24, y0 = h - C.padB - 8, y1 = C.padT + 4;
    const xs = o.series.flatMap((sr) => sr.pts.map((q) => q.x)), ys = o.series.flatMap((sr) => sr.pts.map((q) => q.y)).concat((o.refs || []).map((r) => r.y));
    const dx = domain(Math.min(...xs), Math.max(...xs), 6), dy = domain(Math.min(...ys), Math.max(...ys), 5, 0.05, 0.08);
    const x = (v) => x0 + ((v - dx.lo) / (dx.hi - dx.lo)) * (x1 - x0), y = (v) => y0 - ((v - dy.lo) / (dy.hi - dy.lo)) * (y0 - y1);
    yAxis(svg, y, dy.ticks, o.yfmt, x0, x1);
    for (const t of dx.ticks) stext(svg, x(t), y0 + 16, o.xfmt(t), { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-muted") });
    if (o.xlabel) stext(svg, (x0 + x1) / 2, h - 2, o.xlabel, { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-secondary") });
    for (const r of o.refs || []) {
      s("line", { x1: x0, x2: x1, y1: y(r.y), y2: y(r.y), stroke: cssv("--text-secondary"), "stroke-width": 1.5, "stroke-dasharray": "5 4" }, svg);
      stext(svg, x1 - 4, y(r.y) - 5, r.label, { "text-anchor": "end", "font-size": 11, fill: cssv("--text-secondary") });
    }
    for (const r of o.vrefs || []) {
      if (r.x == null || r.x < dx.lo || r.x > dx.hi) continue;
      s("line", { x1: x(r.x), x2: x(r.x), y1: y1, y2: y0, stroke: r.color || cssv("--text-secondary"), "stroke-width": 1, "stroke-dasharray": "3 3" }, svg);
      stext(svg, x(r.x) + 4, y1 + 10 + (r.row || 0) * 13, r.label, { "font-size": 10.5, fill: cssv("--text-secondary") });
    }
    for (const sr of o.series) {
      const d = sr.pts.map((q, i) => `${i ? "L" : "M"}${x(q.x).toFixed(1)},${y(q.y).toFixed(1)}`).join("");
      const a = { d, fill: "none", stroke: sr.color, "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" };
      if (sr.dash) a["stroke-dasharray"] = "6 4";
      s("path", a, svg);
      if (!sr.dash) sr.pts.forEach((q) => s("circle", { cx: x(q.x), cy: y(q.y), r: 3.5, fill: sr.color, stroke: cssv("--surface-1"), "stroke-width": 1.5 }, svg));
    }
    const hit = s("rect", { x: x0, y: y1, width: x1 - x0, height: y0 - y1, fill: "transparent" }, svg);
    hit.addEventListener("pointermove", (ev) => {
      const r = svg.getBoundingClientRect(), px = ((ev.clientX - r.left) / r.width) * C.w;
      const xv = o.series[0].pts.reduce((b, q) => (Math.abs(x(q.x) - px) < Math.abs(x(b.x) - px) ? q : b)).x;
      showTip(ev, o.xfmt(xv), o.series.map((sr) => { const q = sr.pts.find((z) => z.x === xv); return { color: sr.color, value: q ? o.yfmt(q.y) : "\u2013", name: sr.name }; }));
    });
    hit.addEventListener("pointerleave", hideTip);
  }

  // Dumbbell: per row, status quo (gray) -> plan (accent)
  function dumbbell(host, o) {
    const rows = o.rows, band = 28, h = C.padT + rows.length * band + 26, labW = o.labelW || 230;
    const vals = rows.flatMap((r) => [r.a, r.b]).filter(ok).concat(o.ref !== undefined ? [o.ref] : []);
    const dm = domain(Math.min(...vals), Math.max(...vals), 5, 0.04, 0.12), ticks = dm.ticks;
    const lo = dm.lo, hi = dm.hi;
    const svg = frame(host, h, { label: o.title });
    const x0 = labW, x1 = C.w - 60, y0 = h - 22;
    const x = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0);
    for (const t of ticks) {
      s("line", { x1: x(t), x2: x(t), y1: C.padT - 4, y2: y0, stroke: cssv("--grid"), "stroke-width": 1 }, svg);
      stext(svg, x(t), h - 6, o.fmt(t), { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-muted") });
    }
    if (o.ref !== undefined) { s("line", { x1: x(o.ref), x2: x(o.ref), y1: C.padT - 6, y2: y0, stroke: cssv("--text-secondary"), "stroke-width": 1.5 }, svg); }
    rows.forEach((r, i) => {
      const yy = C.padT + i * band + band / 2;
      const lab = r.short || r.label;
      stext(svg, labW - 10, yy + 4, lab.length > 36 ? lab.slice(0, 35) + "…" : lab, { "text-anchor": "end", "font-size": 11.5, fill: cssv("--text-secondary") });
      if (ok(r.a) && ok(r.b)) s("line", { x1: x(r.a), x2: x(r.b), y1: yy, y2: yy, stroke: cssv("--axis"), "stroke-width": 2 }, svg);
      if (ok(r.a)) s("circle", { cx: x(r.a), cy: yy, r: 5, fill: o.colorA, stroke: cssv("--surface-1"), "stroke-width": 2 }, svg);
      if (ok(r.b)) s("circle", { cx: x(r.b), cy: yy, r: 5, fill: o.colorB, stroke: cssv("--surface-1"), "stroke-width": 2 }, svg);
      if (ok(r.b)) stext(svg, Math.max(x(r.a), x(r.b)) + 9, yy + 4, o.fmt(r.b), { "font-size": 11, fill: cssv("--text-secondary") });
      const hit = s("rect", { x: 0, y: yy - band / 2, width: C.w, height: band, fill: "transparent" }, svg);
      hit.addEventListener("pointermove", (ev) => showTip(ev, r.label, [{ color: o.colorA, value: o.fmt(r.a), name: o.nameA }, { color: o.colorB, value: o.fmt(r.b), name: o.nameB }].concat(r.extra || [])));
      hit.addEventListener("pointerleave", hideTip);
    });
  }

  // Scatter with direct labels (<= 8 points); emphasized points in the accent, the rest de-emphasized
  function scatter(host, o) {
    const h = o.h || 280, pts = o.points;
    const svg = frame(host, h, { label: o.title });
    const x0 = C.padL + 6, x1 = C.w - 24, y0 = h - C.padB - 6, y1 = C.padT + 6;
    const xs = pts.map((p) => p.x), ys = pts.map((p) => p.y);
    const dx = domain(Math.min(...xs), Math.max(...xs), 5, 0.10, 0.30), dy = domain(Math.min(...ys), Math.max(...ys), 5, 0.10, 0.12);
    const xt = dx.ticks, yt = dy.ticks, xlo = dx.lo, xhi = dx.hi, ylo = dy.lo, yhi = dy.hi;
    const x = (v) => x0 + ((v - xlo) / (xhi - xlo)) * (x1 - x0), y = (v) => y0 - ((v - ylo) / (yhi - ylo)) * (y0 - y1);
    yAxis(svg, y, yt, o.yfmt, x0, x1);
    for (const t of xt) stext(svg, x(t), h - 14, o.xfmt(t), { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-muted") });
    stext(svg, (x0 + x1) / 2, h - 1, o.xlabel, { "text-anchor": "middle", "font-size": 11, fill: cssv("--text-secondary") });
    const boxes = pts.map((p) => [x(p.x) - 7, y(p.y) - 7, x(p.x) + 7, y(p.y) + 7]);
    // emphasized points get their labels first; coincident points share one label
    const order = pts.map((p, i) => i).sort((a, b) => (pts[b].emph ? 1 : 0) - (pts[a].emph ? 1 : 0));
    const seen = new Map();
    order.forEach((i) => {
      const p = pts[i], key = `${p.x.toFixed(4)}|${p.y.toFixed(4)}`;
      if (seen.has(key)) { seen.get(key).push(p.label); return; }
      seen.set(key, [p.label]);
    });
    pts.forEach((p) => {
      const c = p.emph ? cssv("--series-1") : cssv("--deemph");
      s("circle", { cx: x(p.x), cy: y(p.y), r: p.emph ? 6 : 5, fill: c, stroke: cssv("--surface-1"), "stroke-width": 2 }, svg);
    });
    for (const i of order) {
      const p = pts[i], key = `${p.x.toFixed(4)}|${p.y.toFixed(4)}`, labs = seen.get(key);
      if (!labs || labs[0] !== p.label) continue;
      const txt = labs.join(" = ");
      const pos = placeLabel(boxes, x(p.x), y(p.y), txt, C.w);
      // never leave a point unnamed: fall back to the side with room, even if it overlaps
      const at = pos || (x(p.x) > C.w * 0.7 ? { x: x(p.x) - 10, y: y(p.y) + 4, anchor: "end" } : { x: x(p.x) + 10, y: y(p.y) + 4, anchor: "start" });
      stext(svg, at.x, at.y, txt, { "text-anchor": at.anchor, "font-size": 11, fill: p.emph ? cssv("--text-primary") : cssv("--text-secondary"), "font-weight": p.emph ? 600 : 400 });
    }
    pts.forEach((p) => {
      const c = p.emph ? cssv("--series-1") : cssv("--deemph");
      const hit = s("circle", { cx: x(p.x), cy: y(p.y), r: 14, fill: "transparent" }, svg);
      hit.addEventListener("pointermove", (ev) => showTip(ev, p.label, [{ color: c, value: o.yfmt(p.y), name: o.ylabel }, { color: c, value: o.xfmt(p.x), name: o.xlabel }].concat(p.extra || [])));
      hit.addEventListener("pointerleave", hideTip);
    });
  }

  // ------------------------------------------------------------------ common blocks
  const kpi = (label, value, delta, hero) => el("div", { class: "tile" + (hero ? " hero" : "") },
    el("div", { class: "label", text: label }), el("div", { class: "value", text: value }), delta ? el("div", { class: "delta" }, delta) : null);
  const deltaSpan = (d, fmt, goodUp = true, suffix = "") => {
    if (!ok(d)) return el("span", { text: "–" });
    const good = goodUp ? d > 0 : d < 0;
    return el("span", null, el("span", { class: Math.abs(d) < 1e-9 ? "" : good ? "up" : "down", text: fmt(d) }), suffix);
  };
  const tag = (kind) => el("span", { class: "tag " + kind, text: kind === "data" ? "DATA" : kind === "assume" ? "ASSUMPTION" : "DERIVED" });
  const stressLabel = (k) => (D.stresses[k] || { label: k }).label;
  const R = (role) => D.roles[role];
  const entry = (role, stress) => R(role).stresses[stress || st.stress[role]];
  const full = (role, stress, which) => { const e = entry(role, stress); return e && e.full ? e.full[which] : null; };
  const fullOrBase = (role, which) => full(role, st.stress[role], which) || full(role, R(role).stress, which);

  const LEAD = { strategy: "Strategy group: reaching 10% a year", balance_sheet: "Balance Sheet group: assets and liabilities",
    liquidity: "Liquidity group: capital calls and the owner's annual distribution",
    asset_allocation: "Asset Allocation group: sell, hold, refinance or lever, and what replaces it" };
  const BLABEL = Object.fromEntries(D.overview.buckets.map((b) => [b.bucket, b.label]));
  function lead(role) {
    const lens = R(role).lens;
    const objText = R(role).objective_text;
    const p = R(role).prefs;
    const basis = { strategy: "ER strategy returns", blend: "blend of ER, debiased underwriting and actual performance", underwritten: "debiased underwritten IRRs", actual: "actual performance (full persistence)" }[p.basis];
    return el("div", { class: "lead" },
      el("h2", { text: LEAD[role] }),
      el("p", { text: `${lens.subtitle}. Objective: ${objText}, under every group's house limits. Return view: ${basis}; world weights ${WORLDS.map((w) => `${w} ${F.pct(p.scenario_probs[w], 0)}`).join(" / ")}; risk aversion ${p.risk_aversion}.` }));
  }

  // Live headline tiles for a role: status quo vs the role's plan at the current controls
  function liveHead(role) {
    const e = entry(role);
    const pi = piNow(), h = hurdle();
    const sq = stats(twr(e.twr.sq), pi, h), pl = stats(twr(e.twr.plan), pi, h), np = stats(twr(e.twr.np), pi, h);
    const d = paired(twr(e.twr.plan), twr(e.twr.sq), pi, h);
    const b = e.brief.plan, bs = e.brief.sq;
    return { sq, pl, np, d, b, bs };
  }
  function headTiles(role, extra) {
    const { sq, pl, np, d, b, bs } = liveHead(role);
    const h = hurdle();
    const tiles = [
      kpi(`P(${F.pct(h, 0)} a year over 5 years), ${R(role).lens.title} plan`, F.pct(pl.pg, 1), el("span", { text: `95% CI ${F.pct(pl.ci[0], 1)} to ${F.pct(pl.ci[1], 1)}` }), true),
      kpi("Status quo (with the PE program)", F.pct(sq.pg, 1), deltaSpan(d.d, (x) => F.pp(x), true, ` plan vs status quo (CI ${F.pp(d.ci[0])} to ${F.pp(d.ci[1])})`)),
      kpi("Mean 5-year return", F.pct(pl.mean, 2), deltaSpan(pl.mean - sq.mean, (x) => F.pp(x, 2), true, " vs status quo")),
      kpi("Worst 10% average (CVaR10)", F.pct(pl.cvar10, 1), deltaSpan(pl.cvar10 - sq.cvar10, (x) => F.pp(x, 1), true, " vs status quo")),
      kpi("Forced private sale (red event)", F.pct(b.p_red, 2), el("span", { text: `status quo ${F.pct(bs.p_red, 2)}` })),
      kpi("PE program effect on the status quo", F.pp(sq.pg - np.pg), el("span", { text: `without the program ${F.pct(np.pg, 1)}` })),
    ];
    if (extra) tiles.splice(4, 2, ...extra);
    return el("div", null, northStarCard(role), el("div", { class: "kpis", style: "margin-top:14px" }, ...tiles), objectivesCard(role), fiveYearsCard(role));
  }

  // The Strategy group's north star (10% a year) as the owner sees the fund: its size after the owner's
  // distributions, against doing nothing, the status quo and this group's plan
  // the north star path: today's size earning h a year (quarterly) while paying the owner's expected distribution
  // (the rule's mean rate by year, a quarter of it each quarter on the year's opening size)
  function starPath(h) {
    const d = (D.meta.owner || {}).draw_mean || [0, 0, 0, 0, 0];
    const nav = [D.meta.W0], paid = [0];
    for (let t = 0; t < 5; t++) {
      let x = nav[t], out = 0;
      for (let q = 0; q < 4; q++) { x *= Math.pow(1 + h, 0.25); x -= (d[t] / 4) * nav[t]; out += (d[t] / 4) * nav[t]; }
      nav.push(x); paid.push(paid[t] + out);
    }
    return { nav, paid };
  }
  function northStarCard(role) {
    const e = entry(role), pi = piNow(), h = hurdle(), W0 = D.meta.W0, own = D.meta.owner || {};
    const fP = fullOrBase(role, "plan"), fS = fullOrBase(role, "sq"), fD = (e.full || {}).dn;
    if (!fD || !fP || !fP.fans || !e.twr.dn) return el("div");
    const sp = starPath(h), star = sp.nav, d1 = (own.draw_mean || [0])[0], cap = own.cap || 0.1;
    const ob = (k) => objStats(twr(e.twr[k]), flags((e.flags || {})[k]), pi, h, k === "sq" ? null : twr(e.twr.sq));
    const rD = ob("dn"), rS = ob("sq"), rP = ob("plan");
    const med5 = (f) => f.fans.nav.p50[5];
    const title = R(role).lens.title;
    const grow = Math.pow(star[5] / W0, 0.2) - 1;
    const tiles = el("div", { class: "kpis" },
      kpi("North star (Strategy group), a year", F.pct(h, 0), el("span", { text: `pays the owner ${F.bn(sp.paid[5], 0)} over five years and ends at ${F.bn(star[5], 0)}` }), true),
      kpi("Owner's distribution", F.pct(d1, 1), el("span", { text: `of opening NAV a year (about ${F.bn(d1 * W0, 0)}); more when oil is weak, up to ${F.pct(cap, 0)}` })),
      kpi("Do nothing: chance of the north star", F.pct(rD.goal, 1), el("span", { text: `median fund ${F.bn(med5(fD), 0)} in year 5` })),
      kpi("Status quo (PE program as decided)", F.pct(rS.goal, 1), deltaSpan(rS.goal - rD.goal, (x) => F.pp(x), true, " vs doing nothing")),
      kpi(`${title} plan`, F.pct(rP.goal, 1), deltaSpan(rP.goal - rD.goal, (x) => F.pp(x), true, " vs doing nothing")),
      kpi("Fund keeps its size", F.pct(fP.p_preserve, 1), el("span", { text: `plan: year 5 at least today's ${F.bn(W0, 0)}; status quo ${F.pct(fS.p_preserve, 1)}` })));
    const chart = chartCard("The fund over five years, after paying the owner", `The fund's size at each year end after the owner's distributions: the plan's P5-P95 and P25-P75 bands and median, the status quo's and doing nothing's medians, the north star (${F.pct(h, 0)} a year while paying the owner's expected distribution, dashed) and today's size (dotted line at ${F.bn(W0, 0)}).`,
      (host) => { host.append(legend([{ name: "Plan P5-P95", color: "var(--wash-1b)", kind: "band" }, { name: `${title} plan, median`, color: cssv("--series-1"), kind: "line" }, { name: "Status quo, median", color: cssv("--deemph"), kind: "line" }, { name: "Do nothing, median", color: cssv("--series-3"), kind: "line" }, { name: `North star, ${F.pct(h, 0)} a year`, color: cssv("--text-secondary"), kind: "line" }, { name: "Today's size", color: cssv("--text-muted"), kind: "line" }])); fanChart(host, { labels: YEARS, fans: [{ name: "Plan", fan: fP.fans.nav, color: cssv("--series-1") }], lines: [{ name: "Status quo", values: fS.fans.nav.p50, color: cssv("--deemph") }, { name: "Do nothing", values: fD.fans.nav.p50, color: cssv("--series-3") }], refs: [{ values: star, label: "North star", color: cssv("--text-secondary"), dash: true }, { y: W0, label: "Today", color: cssv("--text-muted"), dash: true }], yfmt: (t) => F.bn(t, 0), h: 270 }); },
      () => ({ cols: ["Year", "North star", "Paid to the owner on the north star", "Plan P5", "Plan median", "Plan P95", "Status quo median", "Do nothing median"], rows: YEARS.map((y2, i) => [y2, F.bn(star[i], 0), F.bn(sp.paid[i], 0), F.bn(fP.fans.nav.p5[i], 0), F.bn(fP.fans.nav.p50[i], 0), F.bn(fP.fans.nav.p95[i], 0), F.bn(fS.fans.nav.p50[i], 0), F.bn(fD.fans.nav.p50[i], 0)]) }));
    const yr5 = [["North star", star[5], sp.paid[5], null, null, null], ["Do nothing", med5(fD), fD.owner5_p50_bn, fD.p_preserve, rD.goal, rD.all], ["Status quo", med5(fS), fS.owner5_p50_bn, fS.p_preserve, rS.goal, rS.all], [`${title} plan`, med5(fP), fP.owner5_p50_bn, fP.p_preserve, rP.goal, rP.all]];
    const t5 = el("table", { class: "t" });
    t5.append(el("thead", null, el("tr", null, ...["", "Fund, year 5", "Paid to owner", "Keeps its size", `P(${F.pct(h, 0)})`, "Every objective"].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb5 = el("tbody");
    const pc = (x) => (x == null ? "\u2013" : F.pct(x, 1));
    for (const [nm, v5, paid, keep, pg, pa] of yr5) tb5.append(el("tr", null, el("td", { class: "nm", text: nm }), el("td", { class: "num", text: F.bn(v5, 0) }), el("td", { class: "num", text: F.bn(paid, 0) }), el("td", { class: "num", text: pc(keep) }), el("td", { class: "num", text: pc(pg) }), el("td", { class: "num", text: pc(pa) })));
    t5.append(tb5);
    const side = el("div", { class: "card" }, el("h3", { text: "Where each lands in year 5" }),
      el("p", { class: "sub", text: "The median fund after the owner's distributions against the north star, what the owner received over the five years (median), the chance the fund is at least today's size in year 5, and the chance of the target (alone, and with every group's objective met). Fund sizes and the owner's take are at the default world weights; the chances of the target follow the controls." }),
      el("div", { class: "tablewrap full" }, t5),
      el("p", { class: "note", style: "margin-top:10px", text: `Doing nothing ${rD.goal >= rS.goal ? "beats" : "trails"} the status quo by ${(Math.abs(rD.goal - rS.goal) * 100).toFixed(1)}pp${rD.goal >= rS.goal ? ": the status quo sells PE at drought bids" : ""}; the ${title} plan ${rP.goal >= rD.goal ? "adds" : "gives up"} ${(Math.abs(rP.goal - rD.goal) * 100).toFixed(1)}pp against doing nothing.` }));
    const grid = el("div", { class: "grid g2", style: "margin-top:12px" }, chart, side);
    return el("div", { class: "card northstar" }, el("h3", { text: `The north star: ${F.pct(h, 0)} a year while paying the owner, and what doing nothing would do` }),
      el("p", { class: "sub", text: `The owner takes a distribution every year, about what the fund earns (${F.pct(d1, 1)} of opening NAV now; more when oil is weak, up to ${F.pct(cap, 0)}), so the fund's size stays roughly constant. ${F.pct(h, 0)} a year pays the owner and still grows the fund about ${F.pct(grow, 1)} a year. Returns are time-weighted, so the owner's distributions do not count against them. Doing nothing means no decisions at all: no sales (the PE program is not executed), no new commitments, no rebalancing and no new debt; distributions pile up as cash while the owner's distribution and existing calls are paid. The status quo executes the PE program and keeps today's pacing and rebalancing. Probabilities follow the controls above.` }),
      tiles, grid);
  }

  // The five years, year by year: growth against the target path, annualized return to date, and one path at a time
  const MACRO = ["expansion", "late cycle", "crisis", "recovery"], EXITW = ["exits open", "normal exits", "exit drought", "exits frozen"];
  // the decisions a plan takes on one path: today's as planned; the adaptive plan's later ones by that path's
  // market classes (commitments by the class when made; year-2 sales and debt by year 1's; year 3's by both)
  const STN = ["Benign", "Exit drought", "Stress"];
  const unitNav = (cl) => { const nav0 = {}; for (const r of cl.sells) if (r.fraction > 1e-9) nav0[r.unit] = r.nav_bn / r.fraction; return nav0; };
  const saleCtx = (arr, tau, cls) => (tau === 2 && arr.length === 9 ? cls[1] * 3 + cls[2] : cls[tau]);
  function planActions(role, t, pth) {
    const p = R(role).plan, c = p.contingent, cl = R(role).change_list, out = [];
    const cls = pth && pth.cls, live = !!(c && cls && t > 0);
    const nav0 = unitNav(cl), pe = new Set(cl.sells.filter((r) => r.pe_program).map((r) => r.unit));
    let sold = 0, prog = false;
    if (!live) { for (const r of cl.sells.filter((r) => r.tranche === t + 1)) { sold += r.nav_bn; prog = prog || r.pe_program; } }
    else if (t <= 2) for (const [u, v] of Object.entries(c.sell)) { const f = v[t - 1][saleCtx(v[t - 1], t, cls)]; if (f > 1e-6 && nav0[u]) { sold += f * nav0[u]; prog = prog || pe.has(u); } }
    if (sold > 0.05) out.push(`sell ${F.bn(sold)} of private NAV${prog ? " (PE program)" : ""}`);
    const cm = (ok) => (live ? Object.entries(c.commit).filter(([k]) => ok(k)).reduce((a, [, x]) => a + x[t - 1][cls[t]], 0) : Object.entries(p.commit).filter(([k]) => ok(k)).reduce((a, [, x]) => a + (x[t] || 0), 0));
    const all = cm(() => true), sec = cm((k) => k.startsWith("SEC_"));
    out.push(`commit ${F.bn(all)}${sec > 0.05 ? ` (secondaries ${F.bn(sec)})` : ""}`);
    if (t <= 2) { const td = live ? c.term[t - 1][saleCtx(c.term[t - 1], t, cls)] : (p.term_sched || [])[t] || 0; if (td > 0.05) out.push(`draw ${F.bn(td)} of term debt`); }
    const bt = live && c.beta ? c.beta[t - 1][cls[t]] : p.beta_bn;
    if (bt > 0.05) out.push(`hold ${F.bn(bt)} of synthetic beta`);
    if (t === 0) out.push("move the liquid sleeves to the plan");
    return out.join("; ");
  }
  function fiveYearsCard(role) {
    const fP = fullOrBase(role, "plan"), fS = fullOrBase(role, "sq"), h = hurdle();
    if (!fP || !fP.cum_fan) return el("div");
    const tgt = YEARS.map((_, t) => Math.pow(1 + h, t));
    const card = el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "The five years, year by year" }),
      el("p", { class: "sub", text: `How the plan travels toward the target over the five years, on this group's view and the current stress: the growth of $1 at the plan's time-weighted return (as if the owner's distributions stayed invested), the annualized return to date, and any single path in detail. The plan's decisions are dated: sales in three tranches, commitments every year, term debt drawn at the start of years 1-3; an adaptive plan sets the later ones from the market class it has seen by then (its rules are under the change list); each year the reserve, liquid sales and the revolver meet what that path brings.` }));
    const g = el("div", { class: "grid g2" });
    g.append(chartCard("Growth of $1 against the target path", `Plan P5-P95 and P25-P75 bands and median; the status quo's median; ${F.pct(h, 0)} a year compounded (dashed).`,
      (host) => { const fD = (entry(role).full || {}).dn; host.append(legend([{ name: "Plan P5-P95", color: "var(--wash-1b)", kind: "band" }, { name: "Plan median", color: cssv("--series-1"), kind: "line" }, { name: "Status quo median", color: cssv("--deemph"), kind: "line" }].concat(fD ? [{ name: "Do nothing median", color: cssv("--series-3"), kind: "line" }] : [], [{ name: `North star, ${F.pct(h, 0)} a year`, color: cssv("--text-secondary"), kind: "line" }]))); fanChart(host, { labels: YEARS, fans: [{ name: "Plan", fan: fP.cum_fan, color: cssv("--series-1") }], lines: [{ name: "Status quo", values: fS.cum_fan.p50, color: cssv("--deemph") }].concat(fD ? [{ name: "Do nothing", values: fD.cum_fan.p50, color: cssv("--series-3") }] : []), refs: [{ values: tgt, label: "North star", color: cssv("--text-secondary"), dash: true }], yfmt: (t) => "$" + t.toFixed(2), h: 260 }); },
      () => ({ cols: ["Year", "Plan P5", "Plan P25", "Plan median", "Plan P75", "Plan P95", "Status quo median", `${F.pct(h, 0)} a year`], rows: YEARS.map((y2, i) => [y2, ...["p5", "p25", "p50", "p75", "p95"].map((k) => "$" + fP.cum_fan[k][i].toFixed(2)), "$" + fS.cum_fan.p50[i].toFixed(2), "$" + tgt[i].toFixed(2)]) })));
    g.append(chartCard("Annualized return to date", `Each year's annualized return since today: the plan's bands and median, the status quo's median, and the ${F.pct(h, 0)} target.`,
      (host) => { host.append(legend([{ name: "Plan P5-P95", color: "var(--wash-1b)", kind: "band" }, { name: "Plan median", color: cssv("--series-1"), kind: "line" }, { name: "Status quo median", color: cssv("--deemph"), kind: "line" }])); fanChart(host, { labels: FLOWYEARS, fans: [{ name: "Plan", fan: fP.ann_fan, color: cssv("--series-1") }], lines: [{ name: "Status quo", values: fS.ann_fan.p50, color: cssv("--deemph") }], refs: [{ y: h, label: F.pct(h, 0), color: cssv("--text-secondary"), dash: true }], yfmt: (t) => F.pct(t, 0), h: 260 }); },
      () => ({ cols: ["Year", "Plan P5", "Plan median", "Plan P95", "Status quo median"], rows: FLOWYEARS.map((y2, i) => [y2, F.pct(fP.ann_fan.p5[i]), F.pct(fP.ann_fan.p50[i]), F.pct(fP.ann_fan.p95[i]), F.pct(fS.ann_fan.p50[i])]) })));
    card.append(g);
    // one path at a time
    const pe = st.pathPick || (st.pathPick = { which: "plan", world: 1, q: "median" });
    const fDn = (entry(role).full || {}).dn;
    const src = pe.which === "plan" ? fP : pe.which === "dn" && fDn ? fDn : fS, reps = src.rep_paths || [];
    const pth = reps.find((r) => r.world === pe.world && r.q === pe.q) || reps[0];
    if (!pth) return card;
    const mk = (opts, cur, set, lab) => { const s2 = el("select", { "aria-label": lab, onchange: (e) => { set(e.target.value); render(); } }); for (const [v2, t] of opts) s2.append(el("option", { value: v2, text: t, selected: String(v2) === String(cur) ? "selected" : null })); return s2; };
    const sels = el("div", { class: "searchrow" },
      mk([["plan", `${R(role).lens.title} plan`], ["sq", "Status quo"]].concat(fDn ? [["dn", "Do nothing"]] : []), pe.which, (x) => { st.pathPick.which = x; }, "Plan"),
      mk(WORLDS.map((w, i) => [i, `${w} world`]), pe.world, (x) => { st.pathPick.world = +x; }, "ER world"),
      mk([["worst 10%", "Worst 10% path"], ["median", "Median path"], ["best 10%", "Best 10% path"]], pe.q, (x) => { st.pathPick.q = x; }, "Outcome"));
    const g2 = el("div", { class: "grid g2", style: "margin-top:14px" });
    g2.append(chartCard(`One path: the ${pe.q} outcome in the ${WORLDS[pe.world]} world`, `Its five-year return is ${F.pct(pth.twr, 1)} a year, so it ${pth.twr >= h - 1e-9 ? "reaches" : "misses"} the ${F.pct(h, 0)} target. Bars: the return in each year; line: annualized to date.`,
      (host) => { host.append(legend([{ name: "Return in the year", color: cssv("--series-1") }, { name: "Annualized to date", color: cssv("--series-2"), kind: "line" }])); colsChart(host, { cats: FLOWYEARS, series: [{ name: "Return in the year", color: cssv("--series-1"), values: pth.ret }], lines: [{ name: "Annualized to date", color: cssv("--series-2"), values: pth.ann }], refs: [{ y: h, label: `${F.pct(h, 0)} target` }], fmt: (t) => F.pct(t, 0), h: 240 }); }));
    const rowsT = [
      ["Markets at year end", (t) => (pth.macro ? `${MACRO[pth.macro[t]]}, ${EXITW[pth.exit[t]]}` : "\u2013")],
      ["Return in the year", (t) => F.pct(pth.ret[t], 1)],
      ["Annualized to date", (t) => F.pct(pth.ann[t], 1)],
      ["Fund at year end, after the owner", (t) => F.bn(pth.nav[t + 1])],
      ["Owner distribution", (t) => F.bn(pth.draw[t])],
      ["Capital calls", (t) => F.bn(pth.calls[t])],
      ["Distributions received", (t) => F.bn(pth.dist[t])],
      ["Secondary sales", (t) => F.bn(pth.sales[t])],
      ["Liquid sales", (t) => F.bn(pth.lr_sold[t])],
      ["Revolver drawn", (t) => F.bn(pth.rev_draw[t])],
      ["Forced private sales", (t) => F.bn(pth.forced[t])],
      ["Reserve at year end", (t) => F.bn(pth.reserve[t + 1])],
      ["Leverage at year end", (t) => F.x(pth.lev[t + 1], 2)],
      ["Overcommitment at year end", (t) => F.x(pth.ovc[t + 1], 2)],
      ["Coverage at the start of the year", (t) => F.x(pth.lcr[t], 1)],
    ];
    if (pth.cls) rowsT.splice(1, 0, ["Market class at year end", (t) => STN[pth.cls[t + 1]]]);
    if (pe.which === "plan") rowsT.unshift([R(role).plan.contingent ? "The plan's decisions on this path" : "The plan's dated decisions", (t) => planActions(role, t, pth)]);
    const tt = el("table", { class: "t path" });
    tt.append(el("thead", null, el("tr", null, el("th", { text: "" }), ...FLOWYEARS.map((yy) => el("th", { class: "num", text: yy })))));
    const tb = el("tbody");
    for (const [lab, fn] of rowsT) tb.append(el("tr", null, el("th", { text: lab }), ...FLOWYEARS.map((_, t) => el("td", { class: lab.startsWith("The plan") || lab.startsWith("Market") ? "txt" : "num", text: fn(t) }))));
    tt.append(tb);
    const sum = (k) => pth[k].reduce((a, b) => a + b, 0);
    const kv = [["Five-year return", `${F.pct(pth.twr, 1)} a year (${pth.twr >= h - 1e-9 ? "reaches" : "misses"} ${F.pct(h, 0)})`],
      ["Fund after the owner", `${F.bn(pth.nav[0])} today to ${F.bn(pth.nav[5])} in year 5`],
      ["Owner distributions", `${F.bn(sum("draw"))} over five years`],
      ["Private calls / distributions", `${F.bn(sum("calls"))} / ${F.bn(sum("dist"))}`],
      ["Secondary and liquid sales", `${F.bn(sum("sales"))} / ${F.bn(sum("lr_sold"))}`],
      ["Revolver / forced sales", `${F.bn(sum("rev_draw"))} / ${F.bn(sum("forced"))}`],
      ["Lowest coverage", F.x(Math.min(...pth.lcr), 1)],
      ["Highest leverage / overcommitment", `${F.x(Math.max(...pth.lev), 2)} / ${F.x(Math.max(...pth.ovc), 2)}`]];
    g2.append(el("div", { class: "card" }, el("h3", { text: "This path in brief" }), el("p", { class: "sub", text: "Totals over the five years and the extremes the balance sheet and the waterfall saw." }),
      el("div", { class: "kv" }, ...kv.flatMap(([k, x]) => [el("span", { class: "k", text: k }), el("span", { class: "v", text: x })]))));
    card.append(el("h4", { text: "Follow one path" }), sels, g2,
      el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "What happened, year by year" }), el("p", { class: "sub", text: "The same path: the plan's dated decisions, markets, flows, the waterfall and the balance sheet at each year end." }), el("div", { class: "tablewrap full" }, tt)));
    return card;
  }

  // Each group's objective as a test on every path (judged against the house limits, whatever plan is tested)
  const OBJ = {
    strategy: { key: "goal", both: "all", label: "Return target", short: "target" },
    balance_sheet: { key: "bs", both: "goal_bs", label: "Balance sheet within limits", short: "balance sheet" },
    liquidity: { key: "liq", both: "goal_liq", label: "Calls and distributions met", short: "calls and distributions" },
    asset_allocation: { key: "aa", both: null, label: "Never costs the target", short: "never costs the target" },
  };
  const objTest = (role, h) => ({
    strategy: `the five-year return reaches ${F.pct(h, 1)} a year (annualized)`,
    balance_sheet: `gross leverage stays at or below ${F.x(D.house.lev_cap, 2)} and overcommitment (private NAV plus unfunded, over NAV) at or below ${F.x(D.house.overcommit, 2)} at every year-end`,
    liquidity: "every capital call and owner distribution is paid without a forced private sale",
    asset_allocation: "wherever the status quo reaches the target, the plan does too: the substitutions never cost the goal on a path (a path the status quo misses can only be gained)",
  }[role]);
  function objectivesCard(role) {
    const pi = piNow(), h = hurdle(), o = OBJ[role], e = entry(role), own = (k) => k === o.key || k === o.both;
    const rec = (k, ent) => objStats(twr(ent.twr[k]), flags((ent.flags || {})[k]), pi, h, k === "sq" ? null : twr(ent.twr.sq));
    const plans = (e.twr.dn ? [["Do nothing", "dn"]] : []).concat([["Status quo (PE program as decided)", "sq"], [`${R(role).lens.title} plan`, "plan"], ["Status quo without the PE program", "np"]]);
    const S = Object.fromEntries(plans.map(([, k]) => [k, rec(k, e)]));
    const cols = [["goal", `Return of ${F.pct(h, 0)} a year`], ["bs", "Balance sheet within limits"], ["liq", "Calls and distributions met"], ["aa", "Never costs the target"]];
    if (o.both && o.both !== "all") cols.push([o.both, `${F.pct(h, 0)} a year and ${o.short}`]);
    cols.push(["all", "Every objective together"]);
    const t = el("table", { class: "t" });
    t.append(el("thead", null, el("tr", null, el("th", { text: "Probability over the paths" }), ...cols.map(([k, c]) => el("th", { class: "num" + (own(k) ? " own" : ""), text: c })))));
    const tb = el("tbody");
    for (const [name, k] of plans) tb.append(el("tr", null, el("td", { text: name }), ...cols.map(([key]) => el("td", { class: "num" + (own(key) ? " own" : ""), text: key === "aa" && k === "sq" ? "\u2013" : F.pct(S[k][key], 1) }))));
    t.append(tb);
    // every stress: the target and this group's objective, status quo and plan
    const sub = role === "strategy" ? [["goal", `${F.pct(h, 0)} a year`], ["all", "Every objective"]]
      : o.both ? [["goal", `${F.pct(h, 0)} a year`], [o.key, o.label], [o.both, "Both"]]
        : [["goal", `${F.pct(h, 0)} a year`], [o.key, o.label], ["all", "Every objective"]];
    const t2 = el("table", { class: "t" });
    t2.append(el("thead", null,
      el("tr", null, el("th", { text: "" }), el("th", { class: "num grp", colspan: sub.length, text: "Status quo" }), el("th", { class: "num grp", colspan: sub.length, text: `${R(role).lens.title} plan` })),
      el("tr", null, el("th", { text: "Stress" }), ...[0, 1].flatMap(() => sub.map(([k, c]) => el("th", { class: "num" + (k !== "goal" ? " own" : ""), text: c }))))));
    const tb2 = el("tbody");
    for (const k of Object.keys(D.stresses)) {
      const ent = R(role).stresses[k];
      if (!ent || !ent.flags) continue;
      const a = rec("sq", ent), b = rec("plan", ent);
      tb2.append(el("tr", { class: k === st.stress[role] ? "cur" : "" }, el("td", { text: stressLabel(k) }),
        ...[a, b].flatMap((x) => sub.map(([key]) => el("td", { class: "num" + (key !== "goal" ? " own" : ""), text: F.pct(x[key], 1) })))));
    }
    t2.append(tb2);
    return el("div", { class: "card objcard", style: "margin-top:14px" },
      el("h3", { text: `Is the objective met? ${OBJ[role].label === "Return target" ? `The ${F.pct(h, 0)} target and every group's objective` : `The ${F.pct(h, 0)} target and this group's objective`}` }),
      el("p", { class: "sub", text: `Each group's objective is a pass/fail test on every simulated path, judged against the house limits. This group's test: ${objTest(role, h)}. Shaded columns are this group's. Probabilities follow the controls above (world weights, hurdle, stress).` }),
      el("div", { class: "tablewrap" }, t),
      el("h4", { text: "Every stress" }),
      el("div", { class: "tablewrap" }, t2));
  }

  // ------------------------------------------------------------------ filters
  function renderFilters() {
    const box = document.getElementById("filters");
    box.replaceChildren();
    if (st.tab === "data" || st.tab === "yale") { document.getElementById("filternote").textContent = ""; return; }
    const pi = piNow();
    const vals = pi.map((v) => Math.round(v * 100));
    const setPi = (i, v) => {
      const arr = st.pi[st.tab].slice();
      arr[i] = Math.max(0, v / 100);
      const sum = arr.reduce((a, b) => a + b, 0) || 1;
      st.pi[st.tab] = arr.map((x) => x / sum);
      render();
    };
    const worlds = el("div", { class: "f" }, el("label", { text: "ER world probabilities" }),
      el("div", { class: "row" }, ...WORLDS.map((w, i) => el("span", { class: "row" },
        el("span", { class: "small", text: w }),
        el("input", { type: "range", min: 0, max: 100, step: 5, value: vals[i], "aria-label": `${w} probability`, onchange: (ev) => setPi(i, +ev.target.value) }),
        el("span", { class: "val", text: F.pct(pi[i], 0) })))));
    const presets = el("div", { class: "f" }, el("label", { text: "Presets" }), el("div", { class: "row" },
      el("button", { class: "btn", text: "This group's view", onclick: () => { st.pi[st.tab] = viewPi(st.tab); render(); } }),
      el("button", { class: "btn", text: "Pessimistic 40/45/15", onclick: () => { st.pi[st.tab] = [0.40, 0.45, 0.15]; render(); } }),
      el("button", { class: "btn", text: "Central 25/50/25", onclick: () => { st.pi[st.tab] = [0.25, 0.50, 0.25]; render(); } }),
      el("button", { class: "btn", text: "Optimistic 15/50/35", onclick: () => { st.pi[st.tab] = [0.15, 0.50, 0.35]; render(); } })));
    const hur = el("div", { class: "f" }, el("label", { text: "Hurdle" }), el("div", { class: "row" },
      el("input", { type: "range", min: 6, max: 12, step: 0.5, value: st.hurdle * 100, "aria-label": "Hurdle rate", onchange: (ev) => { st.hurdle = +ev.target.value / 100; render(); } }),
      el("span", { class: "val", text: F.pct(st.hurdle, 1) })));
    box.append(worlds, presets, hur);
    if (st.tab !== "ic") {
      const sel = el("select", { "aria-label": "Stress scenario", onchange: (ev) => { st.stress[st.tab] = ev.target.value; render(); } });
      for (const [k, v] of Object.entries(D.stresses)) sel.append(el("option", { value: k, text: v.label, selected: k === st.stress[st.tab] ? "selected" : null }));
      box.append(el("div", { class: "f" }, el("label", { text: "Stress (whole view)" }), sel));
    }
    const note = document.getElementById("filternote");
    const sd = st.tab !== "ic" ? D.stresses[st.stress[st.tab]] : null;
    note.textContent = (sd ? `${sd.label}: ${sd.desc} ` : "") + "World weights and the hurdle re-weight the certified out-of-sample paths live; the plans themselves were optimized by the engine at each group's own view.";
  }

  // ------------------------------------------------------------------ STRATEGY
  function viewStrategy() {
    const role = "strategy", v = document.getElementById("v-strategy");
    v.replaceChildren(lead(role), headTiles(role));
    const e = entry(role), pi = piNow(), h = hurdle();
    const rS = twr(e.twr.sq), rP = twr(e.twr.plan), rN = twr(e.twr.np);
    const sP = stats(rP, pi, h), sS = stats(rS, pi, h), sN = stats(rN, pi, h);
    const g1 = el("div", { class: "grid g2" });
    const hp = histo(rP, pi), hs = histo(rS, pi);
    g1.append(chartCard("Distribution of the 5-year annualized return", `Plan vs status quo; the line marks the ${F.pct(h, 0)} hurdle. Probability per 1pp bin.`,
      (host) => { host.append(legend([{ name: "Strategy plan", color: cssv("--series-1") }, { name: "Status quo", color: cssv("--deemph"), kind: "line" }])); histChart(host, { edges: D.meta.hist_edges, series: [{ name: "Strategy plan", p: hp, color: cssv("--series-1") }, { name: "Status quo", p: hs, color: cssv("--deemph") }], marker: { x: h, label: `${F.pct(h, 0)} hurdle` } }); },
      () => ({ cols: ["Bin", "Plan", "Status quo"], rows: hp.map((p, i) => [`${F.pct(D.meta.hist_edges[i], 0)} to ${F.pct(D.meta.hist_edges[i + 1], 0)}`, F.pct(p, 2), F.pct(hs[i], 2)]) })));
    g1.append(chartCard("Probability of the hurdle by ER world", "Each world is one column of the ER file (Downside / Base / Upside); the controls set their weights.",
      (host) => { host.append(legend([{ name: "Status quo", color: cssv("--deemph") }, { name: "Strategy plan", color: cssv("--series-1") }, { name: "Without the PE program", color: cssv("--series-2") }])); colsChart(host, { cats: WORLDS.concat(["Weighted"]), series: [{ name: "Status quo", color: cssv("--deemph"), values: sS.bw.concat([sS.pg]) }, { name: "Strategy plan", color: cssv("--series-1"), values: sP.bw.concat([sP.pg]) }, { name: "Without the PE program", color: cssv("--series-2"), values: sN.bw.concat([sN.pg]) }], fmt: (t) => F.pct(t, 0), h: 230 }); },
      () => ({ cols: ["World", "Status quo", "Plan", "No program"], rows: WORLDS.concat(["Weighted"]).map((w, i) => [w, F.pct(sS.bw.concat([sS.pg])[i]), F.pct(sP.bw.concat([sP.pg])[i]), F.pct(sN.bw.concat([sN.pg])[i])]) })));
    v.append(g1);
    // levers and frontier
    const ex = R(role).extras;
    const g2 = el("div", { class: "grid g2", style: "margin-top:14px" });
    const fullRow = ex.levers[0];
    const lev = ex.levers.slice(1).map((r) => ({ label: r.name, values: [fullRow.p_goal - r.p_goal], r }));
    g2.append(chartCard("What each lever buys", "Re-optimized with one lever switched off: the loss in P(hurdle) against the full plan (out of sample, the group's view).",
      (host) => barsH(host, { rows: lev, series: [{ name: "P(hurdle) the lever adds", color: cssv("--series-1") }], fmt: (t) => F.pp(t, 1), colorFn: (val) => (val >= 0 ? cssv("--series-1") : cssv("--div-neg")), labelW: 250 }),
      () => ({ cols: ["Lever switched off", "P(hurdle)", "Lever adds", "CVaR10", "Max leverage P95"], rows: ex.levers.map((r) => [r.name, F.pct(r.p_goal), F.pp(fullRow.p_goal - r.p_goal), F.pct(r.cvar10), F.x(r.lev_max_p95)]) })));
    const pts = ex.frontier.map((r) => ({ label: r.name.replace("Tail allowance", "Tail +").replace(" of NAV", ""), x: r.cvar10, y: r.p_goal, emph: r.key === "delta0", extra: [{ value: F.pct(r.p_red, 2), name: "P(red event)" }, { value: F.x(r.lev_max_p95), name: "max leverage P95" }] }));
    const sqb = entry(role, "base").brief.sq;
    pts.push({ label: "Status quo", x: sqb.cvar10, y: sqb.p_goal, emph: false });
    g2.append(chartCard("Risk frontier: what each extra unit of tail risk buys", "P(hurdle) against the average of the worst 10% of outcomes. 'Tail +x%' lets the plan's tail be up to x% of NAV worse than the status quo's (the depth guard); the house setting is 0%.",
      (host) => scatter(host, { points: pts, xfmt: (t) => F.pct(t, 1), yfmt: (t) => F.pct(t, 0), xlabel: "CVaR10 of the 5-year return (right is safer)", ylabel: "P(hurdle)", h: 290 }),
      () => ({ cols: ["Variant", "P(hurdle)", "CVaR10", "P(red)", "Max lev P95", "Term debt", "Beta"], rows: ex.frontier.map((r) => [r.name, F.pct(r.p_goal), F.pct(r.cvar10), F.pct(r.p_red, 2), F.x(r.lev_max_p95), F.bn(r.financing.term_total_bn), F.bn(r.financing.beta_bn)]) })));
    v.append(g2, el("p", { class: "note", style: "margin-top:8px", text: "Sweeps re-optimize with one schedule for every path on 360 in-sample scenarios, for speed; the groups' plans and the adaptivity comparison use the adaptive optimizer on 900." }));
    if ((ex.target_only || []).length) v.append(targetOnlyCard());
    if (ex.adaptivity) v.append(adaptivityCard());
    // fans and on-track
    const fP = fullOrBase(role, "plan"), fS = fullOrBase(role, "sq");
    const g3 = el("div", { class: "grid g2", style: "margin-top:14px" });
    g3.append(chartCard("NAV after owner distributions", "Median and P5-P95 / P25-P75 bands for the plan; the status quo's median for reference ($bn).",
      (host) => { host.append(legend([{ name: "Plan P5-P95", color: "var(--wash-1b)", kind: "band" }, { name: "Plan median", color: cssv("--series-1"), kind: "line" }, { name: "Status quo median", color: cssv("--deemph"), kind: "line" }])); fanChart(host, { labels: YEARS, fans: [{ name: "Plan", fan: fP.fans.nav, color: cssv("--series-1") }], lines: [{ name: "Status quo", values: fS.fans.nav.p50, color: cssv("--deemph") }], yfmt: (t) => F.bn(t, 0) }); },
      () => ({ cols: ["Year", "Plan P5", "Plan median", "Plan P95", "SQ median"], rows: YEARS.map((y2, i) => [y2, F.bn(fP.fans.nav.p5[i], 0), F.bn(fP.fans.nav.p50[i], 0), F.bn(fP.fans.nav.p95[i], 0), F.bn(fS.fans.nav.p50[i], 0)]) })));
    g3.append(chartCard("On track: annualized return to date at or above the hurdle", "Share of paths on track at each year end (group's view, 10% hurdle).",
      (host) => { host.append(legend([{ name: "Plan", color: cssv("--series-1"), kind: "line" }, { name: "Status quo", color: cssv("--deemph"), kind: "line" }])); fanChart(host, { labels: FLOWYEARS, fans: [], lines: [{ name: "Plan", values: fP.on_track, color: cssv("--series-1") }, { name: "Status quo", values: fS.on_track, color: cssv("--deemph") }], yfmt: (t) => F.pct(t, 0), h: 220 }); },
      () => ({ cols: ["Year", "Plan", "Status quo"], rows: FLOWYEARS.map((y2, i) => [y2, F.pct(fP.on_track[i]), F.pct(fS.on_track[i])]) })));
    v.append(g3);
    v.append(changeListCard(role));
    v.append(solveCard(role));
  }

  // The 10% target alone: every group's limit removed (static: this group's default view, base case)
  function targetOnlyCard() {
    const role = "strategy", to = R(role).extras.target_only, e = entry(role, "base"), sp = R(role).plan;
    const hf = D.overview.buckets.find((b) => b.bucket === "HF"), eq = D.overview.buckets.find((b) => b.bucket === "GE_DM");
    const ref = [
      { name: "Status quo (PE program as decided)", p: e.brief.sq.p_goal, cvar10: e.brief.sq.cvar10, cvar1: e.brief.sq.cvar1, red: e.brief.sq.p_red, ob: e.objectives.sq, hf: to[0].liquid_sq.HF, res: to[0].reserve_sq_bn, debt: 0, prog: true },
      { name: "Strategy plan (every group's limits)", p: e.brief.plan.p_goal, cvar10: e.brief.plan.cvar10, cvar1: e.brief.plan.cvar1, red: e.brief.plan.p_red, ob: e.objectives.plan, hf: sp.liquid.HF, res: sp.cash + sp.treasury, debt: sp.term_sched.reduce((a, b) => a + b, 0) + sp.navf_bn, prog: true, emph: true },
    ];
    const rows = ref.concat(to.map((r) => ({ name: r.name, p: r.p_goal, cvar10: r.cvar10, cvar1: r.cvar1, red: r.p_red, ob: r.objectives, hf: r.liquid.HF, res: r.reserve_bn, debt: r.borrowing_bn, prog: r.pe_program_sold, r })));
    const t = el("table", { class: "t" });
    const cols = ["Portfolio", "P(10% a year)", "CVaR10", "Worst 1%", "Forced private sale", "Balance sheet within limits", "Calls and distributions met", "Hedge funds", "Reserve", "Borrowing", "Sells the PE program"];
    t.append(el("thead", null, el("tr", null, ...cols.map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb = el("tbody");
    for (const r of rows) tb.append(el("tr", null, el("td", null, r.emph ? el("strong", { text: r.name }) : document.createTextNode(r.name)), el("td", { class: "num", text: F.pct(r.p, 1) }), el("td", { class: "num", text: F.pct(r.cvar10, 1) }), el("td", { class: "num", text: F.pct(r.cvar1, 1) }), el("td", { class: "num", text: F.pct(r.red, 1) }), el("td", { class: "num", text: F.pct(r.ob.p_bs, 1) }), el("td", { class: "num", text: F.pct(r.ob.p_liq, 1) }), el("td", { class: "num", text: F.bn(r.hf) }), el("td", { class: "num", text: F.bn(r.res) }), el("td", { class: "num", text: F.bn(r.debt) }), el("td", { class: "num", text: r.prog ? "yes" : "no" })));
    t.append(tb);
    const none = to.find((r) => r.key === "to_none"), lev = to.filter((r) => r.lev_cap > 1).sort((a, b) => a.lev_cap - b.lev_cap);
    const er = (b) => `${b.er.map((x) => F.pct(x, 1)).join(" / ")}`;
    const msg = [
      `With nothing but the target, the optimizer sells the equity, Global Agg and MAO sleeves, puts ${F.bn(none.liquid.HF)} in hedge funds (today ${F.bn(none.liquid_sq.HF)}), runs the reserve down and commits up to ${F.x(Math.max(...none.commit_by_year) / none.commit_sq_bn, 1)} today's pace, much of it called after year 5.`,
      `Why hedge funds: the ER file gives them ${er(hf)} in the Downside / Base / Upside worlds against ${er(eq)} for developed-market equities, at less than half the volatility in this model. Capped at twice today's program, the optimizer moves to the next such sleeve.`,
      `There is no interior optimum: P(10%) rises with every turn of leverage (${lev.map((r) => `${F.x(r.lev_cap, 2)}: ${F.pct(r.p_goal, 1)}`).join(", ")}) while the worst 1% of outcomes deepens to ${F.pct(lev[lev.length - 1].cvar1, 0)} a year.`,
      `Without borrowing, the four groups' limits cost ${F.pp(none.p_goal - ref[1].p)} of P(10%). What they buy: the balance sheet stays within limits (${F.pct(ref[1].ob.p_bs, 0)} of paths vs ${F.pct(none.objectives.p_bs, 0)}) and calls and distributions are met without forced sales (${F.pct(ref[1].ob.p_liq, 0)} vs ${F.pct(none.objectives.p_liq, 0)}).`,
    ];
    return el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "The 10% target alone: every group's limit removed" }),
      el("p", { class: "sub", text: "The Strategy objective re-optimized with no leverage, debt, LTV or overcommitment caps, no reserve floor, forced-sale appetite or depth guard, no IC ranges or pacing bands, and the PE program optional. What stays is fact: the owner's distribution and capital calls must be paid, the secondary market's depth, co-invest deal flow, and fund commitments up to 5x today's pace. This group's default view, base case; objectives judged against the house limits." }),
      el("div", { class: "tablewrap" }, t), el("ul", { class: "tight", style: "margin-top:10px" }, ...msg.map((x) => el("li", { text: x }))));
  }

  // The adaptive plan's rules for years 2-5: each later decision follows the market class observed by then
  function rulesCard(role) {
    const p = R(role).plan, c = p.contingent, cl = R(role).change_list;
    if (!c) return el("div");
    const nav0 = unitNav(cl), sh = (x) => ` (${F.pct(x, 0)} of paths)`;
    const tbl = (head, rows) => { const t = el("table", { class: "t" }); t.append(el("thead", null, el("tr", null, ...head.map((x, i) => el("th", { class: i ? "num" : "", text: x }))))); const tb = el("tbody"); for (const r of rows) tb.append(el("tr", null, ...r.map((x, i) => el("td", { class: i ? "num" : "", style: i ? null : "white-space:nowrap", text: x })))); t.append(tb); return el("div", { class: "tablewrap full" }, t); };
    const com = (k, s2, ok) => Object.entries(c.commit).filter(([b]) => ok(b)).reduce((a, [, x]) => a + x[k][s2], 0);
    const comRows = [0, 1, 2, 3].map((k) => [`Year ${k + 2}`, ...[0, 1, 2].map((s2) => { const sec = com(k, s2, (b) => b.startsWith("SEC_")); return `${F.bn(com(k, s2, () => true))}${sec > 0.05 ? `, of which secondaries ${F.bn(sec)}` : ""}${sh(c.freq_commit[k][s2])}`; })]);
    const saleY2 = [0, 1, 2].map((s1) => Object.entries(c.sell).reduce((a, [u, v]) => a + v[0][s1] * (nav0[u] || 0), 0));
    const saleY3 = [0, 1, 2].map((s1) => [0, 1, 2].map((s2) => Object.entries(c.sell).reduce((a, [u, v]) => a + v[1][v[1].length === 9 ? s1 * 3 + s2 : s2] * (nav0[u] || 0), 0)));
    const termY3 = [0, 1, 2].map((s1) => [0, 1, 2].map((s2) => c.term[1][c.term[1].length === 9 ? s1 * 3 + s2 : s2]));
    const hist = (x) => `Year 3 if year 2 ${x.toLowerCase()}`;
    const g1 = el("div", { class: "grid g2" },
      el("div", null, el("h4", { text: "Commitments, by the market class when they are made" }), tbl(["", ...STN], comRows)),
      el("div", null, el("h4", { text: "Secondary sales (private NAV): year 2 by the year-1 class; year 3 by both" }),
        tbl(["Year-1 class", "Year 2", ...STN.map(hist)], [0, 1, 2].map((s1) => [STN[s1], F.bn(saleY2[s1]), ...saleY3[s1].map((x) => F.bn(x))]))));
    const beta = c.beta ? el("div", null, el("h4", { text: "Synthetic beta for the year, by the class at its start" }), tbl(["", ...STN], [0, 1, 2, 3].map((k) => [`Year ${k + 2}`, ...[0, 1, 2].map((s2) => F.bn(c.beta[k][s2]))])))
      : el("div", null, el("h4", { text: "Synthetic beta" }), el("p", { class: "note", text: `One size for all five years (${F.bn(p.beta_bn)}): the market class says little about the overlay's next return, and a rule by class fitted noise when tested.` }));
    const g2 = el("div", { class: "grid g2", style: "margin-top:10px" },
      el("div", null, el("h4", { text: "Term debt drawn: year 2 by the year-1 class; year 3 by both" }),
        tbl(["Year-1 class", "Year 2", ...STN.map(hist)], [0, 1, 2].map((s1) => [STN[s1], F.bn(c.term[0][s1]), ...termY3[s1].map((x) => F.bn(x))]))), beta);
    return el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: `${R(role).lens.title} plan: the rules for years 2 to 5` }),
      el("p", { class: "sub", text: "Today's decisions are fixed; each later one is taken when its year starts, from the market class observed at that year end (benign, exit drought, or stress: a macro crisis, frozen exits, or an oil shock that pushes the owner's draw well up). The plan never sees the future: every path in the same situation gets the same decision. A class seen on too few of the optimizer's scenarios shares the most common related class's decision. Year-3 sales and debt follow the year-1 and year-2 classes together, so the PE program's total and the debt cap hold on every path. In a stress year the plan may buy secondaries up to the market's capacity (the countercyclical mandate); otherwise the program's pacing limits apply." }),
      g1, g2);
  }

  // What adaptivity adds: the adaptive Strategy plan against one fixed schedule (same objective, same limits)
  function adaptivityCard() {
    const A = R("strategy").extras.adaptivity, base = A.stresses.find((r) => r.stress === R("strategy").stress) || A.stresses[0];
    const ci = (r) => `${F.pp(r.d_p_goal)} (${F.pp(r.d_p_goal_ci[0])} to ${F.pp(r.d_p_goal_ci[1])})`;
    const sig = (r) => (r.d_p_goal_ci[0] > 0 ? "ahead of" : r.d_p_goal_ci[1] < 0 ? "behind" : "level with");
    const t = el("table", { class: "t" });
    t.append(el("thead", null, el("tr", null, ...["Stress", "Fixed: P(target)", "Adaptive: P(target)", "Adaptive minus fixed (95% CI)", "Fund keeps its size: fixed / adaptive", "Forced sale: fixed / adaptive"].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb = el("tbody");
    for (const r of A.stresses) tb.append(el("tr", null, el("td", { text: stressLabel(r.stress) }), el("td", { class: "num", text: F.pct(r.fixed.p_goal, 1) }), el("td", { class: "num", text: F.pct(r.adaptive.p_goal, 1) }), el("td", { class: "num", text: ci(r) }), el("td", { class: "num", text: `${F.pct(r.fixed.p_preserve, 1)} / ${F.pct(r.adaptive.p_preserve, 1)}` }), el("td", { class: "num", text: `${F.pct(r.fixed.p_red, 1)} / ${F.pct(r.adaptive.p_red, 1)}` })));
    t.append(tb);
    const up = A.stresses.filter((r) => r.d_p_goal_ci[0] > 0).length, down = A.stresses.filter((r) => r.d_p_goal_ci[1] < 0).length;
    const nm = A.no_mandate, lc = (r) => { const t = stressLabel(r.stress); return t.charAt(0).toLowerCase() + t.slice(1); };
    const msg = [
      `In the ${lc(base)}, the adaptive plan is ${sig(base)} the fixed schedule: ${ci(base)} of P(target) on the same ${F.int(D.meta.n_oos * 3)} paths. Across the ${A.stresses.length} stresses it is significantly ahead in ${up}${down ? ` and significantly behind in ${down}` : " and never significantly behind"}.`,
      nm ? `Where the gain comes from: without the countercyclical secondaries mandate, the market-class rules alone add ${ci(nm)}. The mandate lets the plan buy secondaries when sellers need liquidity and prices are low, which a fixed schedule cannot time.` : null,
      (() => {
        const app = (D.house && D.house.forced_eps) || 0.01, lbl = lc;
        const over = A.stresses.filter((r) => r.adaptive.p_red > app + 1e-9 && r.adaptive.p_red > r.fixed.p_red + 0.002);
        const head = `Forced private sales: ${F.pct(base.adaptive.p_red, 1)} of paths in the ${lbl(base)} (fixed: ${F.pct(base.fixed.p_red, 1)}), within the ${F.pct(app, 0)} appetite the plan was validated against.`;
        return over.length ? `${head} The cost shows in harsher stresses: buying in a stress year leaves less cash for what follows, and forced sales exceed the appetite in ${over.map((r) => `${lbl(r)} (${F.pct(r.adaptive.p_red, 1)} against ${F.pct(r.fixed.p_red, 1)} fixed)`).join(", ")}. Requiring the guard to hold in those stresses too would give back part of the gain.` : head;
      })(),
      "Why the gain is not larger: returns are not predictable in this model (regimes move risk, not expected returns), realistic timing gains in private equity are small (Brown, Harris, Hu, Jenkinson, Kaplan and Robinson, JFE 2021), and most decisions sit at their limits whatever happens. The owner's distribution, about what the fund earns, is what makes timing worth something: cash is scarce exactly when prices are low.",
    ].filter(Boolean);
    return el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "What adaptivity adds: the adaptive plan against one fixed schedule" }),
      el("p", { class: "sub", text: "The same objective and house limits, optimized twice: later decisions by the market class observed by then, or one schedule for every path. Both plans' tail and forced-sale guards are re-checked on validation paths the optimizer never saw; the comparison is paired on the certification paths. This group's default weights." }),
      el("div", { class: "tablewrap full" }, t), el("ul", { class: "tight", style: "margin-top:10px" }, ...msg.map((x) => el("li", { text: x }))));
  }

  // ------------------------------------------------------------------ change list (shared)
  function changeListCard(role) {
    const cl = R(role).change_list;
    const card = el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: `${R(role).lens.title} plan: the change list` }),
      el("p", { class: "sub", text: "Every difference from the status quo without the program, dated. Secondary sales show the expected proceeds at the realized bid of each tranche. Commitment rows show five-year totals, with year 1's commitment (plan vs status quo) in the label." }));
    const g = el("div", { class: "grid g2" });
    const t1 = el("table", { class: "t" });
    t1.append(el("thead", null, el("tr", null, ...["Sale (unit, tranche)", "NAV", "Unfunded", "Proceeds", "Discount"].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb1 = el("tbody");
    for (const r of cl.sells) tb1.append(el("tr", null, el("td", { text: `${r.label} ${r.part === "tail" ? "(underperformers)" : r.part === "core" ? "(core)" : ""} · year ${r.tranche}${r.pe_program ? " · PE program" : ""}` }), el("td", { class: "num", text: F.bn(r.nav_bn, 2) }), el("td", { class: "num", text: F.bn(r.unfunded_bn, 2) }), el("td", { class: "num", text: F.bn(r.expected_proceeds_bn, 2) }), el("td", { class: "num", text: F.bn(r.discount_bn, 2) })));
    t1.append(tb1);
    const t2 = el("table", { class: "t" });
    t2.append(el("thead", null, el("tr", null, ...["Allocation change", "From", "To", "Change"].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb2 = el("tbody");
    for (const r of cl.liquid) tb2.append(el("tr", null, el("td", { text: `${r.label} (${r.lens})` }), el("td", { class: "num", text: F.bn(r.from_bn) }), el("td", { class: "num", text: F.bn(r.to_bn) }), el("td", { class: "num", text: F.sbn(r.change_bn) })));
    tb2.append(el("tr", null, el("td", { text: "Reserve (cash + Treasury)" }), el("td", { class: "num", text: F.bn(cl.reserve.from_bn) }), el("td", { class: "num", text: F.bn(cl.reserve.to_bn) }), el("td", { class: "num", text: F.sbn(cl.reserve.to_bn - cl.reserve.from_bn) })));
    for (const r of cl.commits.slice().sort((a, b) => Math.abs(b.change_5y_bn) - Math.abs(a.change_5y_bn)).slice(0, 12)) tb2.append(el("tr", null, el("td", { text: `${r.label} (${r.change_5y_bn >= 0 ? (r.fund ? "PACE UP" : "ADD") : (r.fund ? "PACE DOWN" : "CUT")}: year 1 ${F.bn(r.plan_by_year[0], 2)} vs ${F.bn(r.sq_by_year[0], 2)})` }), el("td", { class: "num", text: F.bn(r.sq_by_year.reduce((a, b) => a + b, 0)) }), el("td", { class: "num", text: F.bn(r.plan_by_year.reduce((a, b) => a + b, 0)) }), el("td", { class: "num", text: F.sbn(r.change_5y_bn) })));
    t2.append(tb2);
    g.append(el("div", { class: "tablewrap short" }, t1), el("div", { class: "tablewrap short" }, t2));
    const fin = cl.financing, r1 = cl.r1, pe = cl.pe_program;
    card.append(g, el("div", { class: "callout" }, el("strong", { text: "Financing and R1 labels. " }),
      `New term debt ${F.bn(fin.term_total_bn)} (drawn ${fin.term_sched_bn.map((x, i) => `y${i + 1} ${F.bn(x)}`).join(", ")}), NAV facility ${F.bn(fin.navf_bn)}, synthetic beta ${F.bn(fin.beta_bn)}. Of ${F.bn(r1.dB_bn)} new financing, ${F.bn(r1.LEVER_bn)} is LEVER (funds added exposure) and ${F.bn(r1.REFINANCE_bn)} is REFINANCE (cash raised without adding exposure). PE program in this plan: ${F.bn(pe.exposure_bn)} exposure (${F.bn(pe.nav_bn)} NAV, ${F.bn(pe.unfunded_bn)} unfunded), expected proceeds ${F.bn(pe.proceeds_bn)}; by tranche ${pe.by_tranche_bn.map((x) => F.bn(x)).join(" / ")}.`));
    return el("div", null, card, rulesCard(role));
  }
  function solveCard(role) {
    const r = R(role), ins = r.in_sample, b = entry(role, r.stress).brief.plan;
    const logs = r.solve_log.map((l) => `${l.name}: ${l.status} (${l.time_s.toFixed(1)}s)`).join(" · ");
    return el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "How the engine chose this plan" }),
      el("div", { class: "kv" },
        el("span", { class: "k", text: "Objective" }), el("span", { class: "v", text: `${r.objective_text} [${r.label}]` }),
        el("span", { class: "k", text: "LP" }), el("span", { class: "v", text: `${F.int(r.lp_size.cols)} columns, ${F.int(r.lp_size.rows)} rows, ${F.int(r.lp_size.nnz)} nonzeros on ${F.int(D.meta.n_lp * 3)} in-sample scenarios` }),
        el("span", { class: "k", text: "Solves" }), el("span", { class: "v", text: logs }),
        el("span", { class: "k", text: "House limits applied" }), el("span", { class: "v", text: Object.keys(r.eps || {}).map((k) => ({ depth_guard: "depth guard (tail no worse than the status quo)", forced_eps: `forced-sale appetite ${F.pct(r.eps.forced_eps, 1)}`, ret_min: `return floor ${F.pct(r.eps.ret_min, 1)}`, p_goal_min: `P(hurdle) floor ${F.pct(r.eps.p_goal_min, 0)}`, bs_guard: `balance sheet within its leverage and overcommitment limits at every year end on ${F.pct(r.eps.bs_guard.prob, 0)} of paths` }[k] || k)).join("; ") + "; leverage, debt, LTV, overcommitment, IC ranges, pacing and market-depth caps" }),
        el("span", { class: "k", text: "Validation" }), el("span", { class: "v", text: (() => { const cb = r.calibration || []; if (!cb.length) return "\u2013"; const last = cb[cb.length - 1]; return cb.length === 1 ? `the house guards held on ${F.int(D.meta.n_val * 3)} validation paths the optimizer never saw` : `the guards were breached on ${F.int(D.meta.n_val * 3)} validation paths and tightened ${cb.length - 1} time${cb.length > 2 ? "s" : ""} (tail guard by ${F.pp(last.tighten)}, forced-sale appetite to ${F.pct(last.forced_eps, 2)}) before the plan was accepted; forced sales on ${F.pct(last.p_red, 1)} of validation paths`; })() + (() => { const cb = r.calibration || []; const last = cb[cb.length - 1]; return last && last.bs_within != null ? `; balance sheet within its limits at every year end on ${F.pct(last.bs_within, 1)} of them` : ""; })() }),
        el("span", { class: "k", text: "In-sample vs certified" }), el("span", { class: "v", text: `P(hurdle) ${F.pct(ins.p_goal)} on the LP's own scenarios vs ${F.pct(b.p_goal)} on ${F.int(D.meta.n_oos * 3)} fresh paths (the optimism gap is ${F.pp(ins.p_goal - b.p_goal)})` })));
  }

  // ------------------------------------------------------------------ BALANCE SHEET
  function viewBS() {
    const role = "balance_sheet", v = document.getElementById("v-balance_sheet");
    const b = entry(role).brief.plan, bs = entry(role).brief.sq;
    v.replaceChildren(lead(role), headTiles(role, [
      kpi("Max leverage (P95, plan)", F.x(b.lev_max_p95), el("span", { text: `status quo ${F.x(bs.lev_max_p95)}` })),
      kpi("Debt P95 (plan)", F.bn(b.debt_p95_bn), el("span", { text: `overcommitment median peak ${F.x(b.ovc_max_p50)}` })),
    ]));
    const fP = fullOrBase(role, "plan"), fS = fullOrBase(role, "sq");
    const ov = D.overview.book;
    const g1 = el("div", { class: "grid g2" });
    const comp = ["priv", "lr", "reserve"];
    const names = { priv: "Private holdings", lr: "Liquid risk (equities, HF, Agg, MAO)", reserve: "Reserve (cash + Treasury)" };
    const colors = [cssv("--series-1"), cssv("--series-2"), cssv("--series-3")];
    g1.append(chartCard("Projected balance sheet (plan, mean path)", "Assets above zero; debt (term, NAV facility, revolver) below. $bn.",
      (host) => { host.append(legend(comp.map((k, i) => ({ name: names[k], color: colors[i] })).concat([{ name: "Debt", color: cssv("--series-4") }]))); colsChart(host, { cats: YEARS, stacked: true, series: comp.map((k, i) => ({ name: names[k], color: colors[i], values: fP.fans[k].mean })).concat([{ name: "Debt", color: cssv("--series-4"), values: fP.fans.debt.mean.map((x) => -x) }]), fmt: (t) => F.bn(t, 0), h: 260 }); },
      () => ({ cols: ["Year", "Private", "Liquid risk", "Reserve", "Debt", "NAV"], rows: YEARS.map((y2, i) => [y2, F.bn(fP.fans.priv.mean[i]), F.bn(fP.fans.lr.mean[i]), F.bn(fP.fans.reserve.mean[i]), F.bn(fP.fans.debt.mean[i]), F.bn(fP.fans.nav.mean[i])]) })));
    g1.append(chartCard("Leverage: gross exposure / NAV", "Plan P5-P95 band and median; the status quo's median; the house cap.",
      (host) => { host.append(legend([{ name: "Plan P5-P95", color: "var(--wash-1b)", kind: "band" }, { name: "Plan median", color: cssv("--series-1"), kind: "line" }, { name: "Status quo median", color: cssv("--deemph"), kind: "line" }])); fanChart(host, { labels: YEARS, fans: [{ name: "Plan", fan: fP.fans.lev, color: cssv("--series-1") }], lines: [{ name: "Status quo", values: fS.fans.lev.p50, color: cssv("--deemph") }], refs: [{ y: D.house.lev_cap, label: `cap ${F.x(D.house.lev_cap)}` }], yfmt: (t) => F.x(t, 2), h: 240 }); },
      () => ({ cols: ["Year", "Plan median", "Plan P95", "SQ median"], rows: YEARS.map((y2, i) => [y2, F.x(fP.fans.lev.p50[i]), F.x(fP.fans.lev.p95[i]), F.x(fS.fans.lev.p50[i])]) })));
    v.append(g1);
    const ex = R(role).extras;
    const g2 = el("div", { class: "grid g2", style: "margin-top:14px" });
    g2.append(chartCard("Debt capacity: what borrowing buys toward the hurdle", "The hurdle objective (GBO) re-optimized under this group's view at each debt allowance, every other house limit unchanged (out of sample). Hover for the balance-sheet cost.",
      (host) => dumbbell(host, { rows: ex.debt_frontier.map((r) => ({ label: r.name, short: r.name.replace("New term debt up to", "Debt up to").replace(", synthetic beta allowed", " + synthetic beta"), a:entry(role, R(role).stress).brief.sq.p_goal, b: r.p_goal, extra: [{ value: F.bn(r.debt_p95_bn), name: "debt P95" }, { value: F.x(r.lev_max_p95), name: "max leverage P95" }, { value: F.pct(r.cvar10), name: "CVaR10" }] })), colorA: cssv("--deemph"), colorB: cssv("--series-1"), nameA: "Status quo", nameB: "Re-optimized", fmt: (t) => F.pct(t, 1), labelW: 260 }),
      () => ({ cols: ["Allowance", "P(hurdle)", "Mean TWR", "CVaR10", "Debt P95", "Max lev P95", "LEVER", "REFINANCE"], rows: ex.debt_frontier.map((r) => [r.name, F.pct(r.p_goal), F.pct(r.twr_mean, 2), F.pct(r.cvar10), F.bn(r.debt_p95_bn), F.x(r.lev_max_p95), F.bn(r.r1.LEVER_bn), F.bn(r.r1.REFINANCE_bn)]) })));
    const sl = D.overview.buckets.filter((r) => r.sleeve_bn > 0.001 || r.tier === "reserve");
    const t = el("table", { class: "t" });
    t.append(el("thead", null, el("tr", null, ...["Sleeve", "In the fund file", "Internal sleeve", "Source"].map((c, i) => el("th", { class: i && i < 3 ? "num" : "", text: c })))));
    const tb = el("tbody");
    for (const r of sl) tb.append(el("tr", null, el("td", { text: r.label }), el("td", { class: "num", text: F.bn(r.file_nav_bn) }), el("td", { class: "num", text: F.bn(r.sleeve_bn) }), el("td", null, r.sleeve_bn > 0 ? tag("assume") : tag("data"))));
    t.append(tb);
    const ns = ex.nav_sensitivity;
    g2.append(el("div", { class: "card" }, el("h3", { text: "The whole fund: what the fund file does not hold" }),
      el("p", { class: "sub", text: `The fund file holds ${F.bn(ov.file_nav_bn)} marked at ${D.meta.files.as_of}; the whole fund is set to ${F.bn(ov.total_nav_bn)}. The gap is the internally managed sleeves, sized by assumption until actual balances are entered.` }),
      el("div", { class: "tablewrap short" }, t),
      el("div", { class: "callout" }, el("strong", { text: "Sensitivity to the whole-fund NAV. " }), ns.map((r) => `${F.bn(r.total_nav_bn, 0)}: P(hurdle) ${F.pct(r.sq.p_goal)} status quo`).join(" · ") + ". Liabilities today: revolver drawn " + F.bn(ov.revolver_drawn0_bn) + ", term debt " + F.bn(ov.term0_bn) + " (assumptions: enter actual balances).")));
    v.append(g2, el("p", { class: "note", style: "margin-top:8px", text: "Sweeps re-optimize with one schedule for every path on 360 in-sample scenarios, for speed; the groups' plans and the adaptivity comparison use the adaptive optimizer on 900." }));
    v.append(changeListCard(role), solveCard(role));
  }

  // ------------------------------------------------------------------ LIQUIDITY
  function viewLiquidity() {
    const role = "liquidity", v = document.getElementById("v-liquidity");
    const b = entry(role).brief.plan, bs = entry(role).brief.sq;
    v.replaceChildren(lead(role), headTiles(role, [
      kpi("Revolver used (probability)", F.pct(b.p_revolver, 1), el("span", { text: `status quo ${F.pct(bs.p_revolver, 1)}` })),
      kpi("Worst-year coverage, P5 (plan)", F.x(b.lcr_min_p5, 2), el("span", { text: `status quo ${F.x(bs.lcr_min_p5, 2)}` })),
    ]));
    const fP = fullOrBase(role, "plan"), fS = fullOrBase(role, "sq");
    const g0 = el("div", { class: "grid g2" });
    const dpi = D.overview.dpi.filter((r) => r.vintage >= 2008 && r.commit_bn > 0.2);
    g0.append(chartCard("DPI has been falling: distributions to paid-in by vintage", "Commitment-weighted DPI and TVPI of the live book (DATA). Young vintages have returned little cash; the base case starts in an exit drought.",
      (host) => { host.append(legend([{ name: "DPI", color: cssv("--series-1") }, { name: "TVPI", color: cssv("--series-2"), kind: "line" }])); colsChart(host, { cats: dpi.map((r) => String(r.vintage).slice(2)), series: [{ name: "DPI", color: cssv("--series-1"), values: dpi.map((r) => r.dpi) }], lines: [{ name: "TVPI", color: cssv("--series-2"), values: dpi.map((r) => r.tvpi) }], fmt: (t) => t.toFixed(1) + "×", h: 240, catTitle: "Vintage 20" }); },
      () => ({ cols: ["Vintage", "DPI", "TVPI", "Commitments", "NAV", "Holdings"], rows: dpi.map((r) => [String(r.vintage), F.x(r.dpi), F.x(r.tvpi), F.bn(r.commit_bn), F.bn(r.nav_bn), String(r.n)]) })));
    const fl = fP.flows, fls = fS.flows;
    g0.append(chartCard("Annual cash needs and private distributions (plan, mean path)", "Owner distribution and capital calls against private distributions, $bn a year.",
      (host) => { host.append(legend([{ name: "Owner distribution", color: cssv("--series-1") }, { name: "Capital calls", color: cssv("--series-2") }, { name: "Private distributions", color: cssv("--series-3") }])); colsChart(host, { cats: FLOWYEARS, series: [{ name: "Owner distribution", color: cssv("--series-1"), values: fl.draw.mean }, { name: "Capital calls", color: cssv("--series-2"), values: fl.calls.mean }, { name: "Private distributions", color: cssv("--series-3"), values: fl.dist.mean }], fmt: (t) => F.bn(t, 0), h: 240 }); },
      () => ({ cols: ["Year", "Owner draw", "Calls", "Distributions", "Draw P95", "Calls P95", "Dist P5"], rows: FLOWYEARS.map((y2, i) => [y2, F.bn(fl.draw.mean[i]), F.bn(fl.calls.mean[i]), F.bn(fl.dist.mean[i]), F.bn(fl.draw.p95[i]), F.bn(fl.calls.p95[i]), F.bn(fl.dist.p5[i])]) })));
    v.append(g0);
    const g1 = el("div", { class: "grid g2", style: "margin-top:14px" });
    g1.append(chartCard("How the gap is funded (plan, mean path)", "Secondary-sale proceeds, liquid sales, revolver draws and forced sales, $bn a year.",
      (host) => { host.append(legend([{ name: "Secondary sales", color: cssv("--series-1") }, { name: "Liquid sales", color: cssv("--series-2") }, { name: "Revolver draws", color: cssv("--series-3") }, { name: "Forced sales", color: cssv("--series-4") }])); colsChart(host, { cats: FLOWYEARS, stacked: true, series: [{ name: "Secondary sales", color: cssv("--series-1"), values: fl.sales.mean }, { name: "Liquid sales", color: cssv("--series-2"), values: fl.lr_sold.mean }, { name: "Revolver draws", color: cssv("--series-3"), values: fl.rev_draw.mean }, { name: "Forced sales", color: cssv("--series-4"), values: fl.forced.mean }], fmt: (t) => F.bn(t, 0), h: 240 }); },
      () => ({ cols: ["Year", "Secondary sales", "Liquid sales", "Revolver", "Forced", "SQ liquid sales"], rows: FLOWYEARS.map((y2, i) => [y2, F.bn(fl.sales.mean[i]), F.bn(fl.lr_sold.mean[i]), F.bn(fl.rev_draw.mean[i]), F.bn(fl.forced.mean[i]), F.bn(fls.lr_sold.mean[i])]) })));
    g1.append(chartCard("Liquidity coverage: sources at the start of each year / that year's uses", "Plan band and median; status quo median; 1.0× means the year's draw, calls and interest are just covered.",
      (host) => { host.append(legend([{ name: "Plan P5-P95", color: "var(--wash-1b)", kind: "band" }, { name: "Plan median", color: cssv("--series-1"), kind: "line" }, { name: "Status quo median", color: cssv("--deemph"), kind: "line" }])); fanChart(host, { labels: FLOWYEARS, fans: [{ name: "Plan", fan: fP.lcr_fan, color: cssv("--series-1") }], lines: [{ name: "Status quo", values: fS.lcr_fan.p50, color: cssv("--deemph") }], refs: [{ y: 1.0, label: "1.0×" }], yfmt: (t) => F.x(t, 1), zero: true }); },
      () => ({ cols: ["Year", "Plan P5", "Plan median", "SQ P5", "SQ median"], rows: FLOWYEARS.map((y2, i) => [y2, F.x(fP.lcr_fan.p5[i]), F.x(fP.lcr_fan.p50[i]), F.x(fS.lcr_fan.p5[i]), F.x(fS.lcr_fan.p50[i])]) })));
    v.append(g1);
    // stress table and draw policies
    const g2 = el("div", { class: "grid g2", style: "margin-top:14px" });
    const rows = Object.keys(D.stresses).map((k) => ({ k, e: entry(role, k) }));
    g2.append(chartCard("Every stress: worst-year coverage (P5)", "Status quo vs the Liquidity plan; below 1.0× a year's needs exceed what is available at its start.",
      (host) => dumbbell(host, { rows: rows.map(({ k, e }) => ({ label: stressLabel(k), short: stressLabel(k).split(" (")[0], a: e.brief.sq.lcr_min_p5, b: e.brief.plan.lcr_min_p5, extra: [{ value: F.pct(e.brief.plan.p_revolver, 1), name: "revolver used (plan)" }, { value: F.pct(e.brief.plan.p_red, 2), name: "red event (plan)" }] })), colorA: cssv("--deemph"), colorB: cssv("--series-1"), nameA: "Status quo", nameB: "Liquidity plan", fmt: (t) => F.x(t, 1), ref: 1.0, labelW: 240 }),
      () => ({ cols: ["Stress", "SQ coverage P5", "Plan coverage P5", "SQ revolver", "Plan revolver", "SQ red", "Plan red", "SQ reserve min P5", "Plan reserve min P5"], rows: rows.map(({ k, e }) => [stressLabel(k), F.x(e.brief.sq.lcr_min_p5), F.x(e.brief.plan.lcr_min_p5), F.pct(e.brief.sq.p_revolver, 1), F.pct(e.brief.plan.p_revolver, 1), F.pct(e.brief.sq.p_red, 2), F.pct(e.brief.plan.p_red, 2), F.bn(e.brief.sq.reserve_min_p5_bn), F.bn(e.brief.plan.reserve_min_p5_bn)]) })));
    const dp = R(role).extras.draw_policies;
    const t = el("table", { class: "t" });
    t.append(el("thead", null, el("tr", null, ...["Owner distribution", "Y1 draw", "Revolver used: SQ / plan", "Coverage P5: SQ / plan", "Red event: SQ / plan"].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb = el("tbody");
    for (const r of dp) tb.append(el("tr", null, el("td", { text: r.name }), el("td", { class: "num", text: F.bn(r.draws_sq.p50[0]) }), el("td", { class: "num", text: `${F.pct(r.sq.p_revolver, 1)} / ${r.plan ? F.pct(r.plan.p_revolver, 1) : "–"}` }), el("td", { class: "num", text: `${F.x(r.sq.lcr_min_p5, 1)} / ${r.plan ? F.x(r.plan.lcr_min_p5, 1) : "–"}` }), el("td", { class: "num", text: `${F.pct(r.sq.p_red, 1)} / ${r.plan ? F.pct(r.plan.p_red, 1) : "–"}` })));
    t.append(tb);
    const pe = R(role).change_list.pe_program;
    g2.append(el("div", { class: "card" }, el("h3", { text: "Owner distributions and the PE program" }),
      el("p", { class: "sub", text: `Under the '${stressLabel(R(role).stress)}' view. The owner's draw is set each year from Brent (${F.pct((D.meta.owner || {}).floor || 0.09, 0)}-${F.pct((D.meta.owner || {}).cap || 0.1, 0)} of opening NAV: about what the fund earns, more when oil is weak; smoothed) unless a fixed policy is chosen.` }),
      el("div", { class: "tablewrap short" }, t),
      el("div", { class: "callout" }, el("strong", { text: "The PE program as a liquidity source. " }), `In the Liquidity plan it sells ${F.bn(pe.exposure_bn)} of PE exposure: ${F.bn(pe.nav_bn)} of NAV for expected proceeds of ${F.bn(pe.proceeds_bn)}, and the buyers take ${F.bn(pe.unfunded_bn)} of unfunded commitments (future capital calls ADIC no longer pays).`)));
    v.append(g2);
    v.append(changeListCard(role), solveCard(role));
  }

  // ------------------------------------------------------------------ ASSET ALLOCATION
  const CARD_COLORS = () => ({ SELL: cssv("--series-2"), "SELL?": cssv("--series-4"), HOLD: cssv("--deemph"), REFINANCE: cssv("--series-3"), LEVER: cssv("--series-1"), LIQUID: cssv("--axis") });
  function hcol(name) { return D.holdings.columns.indexOf(name); }
  function liveReturns(row, p) {
    // tpp.returns.holding_returns, per holding (the same formulas and caps)
    const g = (c) => row[hcol(c)];
    const cap = 0.08, lo = -0.20, hi = 0.35;
    const clip = (x, a, b) => Math.min(Math.max(x, a), b);
    const Sd = g("S_down"), Sb = g("S_base"), Su = g("S_up");
    const uw = g("uw_irr"), beta = p.debias ? (g("uw_beta") || 0) : 0, youth = g("uw_youth") || 0;
    const U = ok(uw) ? uw - beta : null;
    const tiltU = U !== null ? youth * clip(U - Sb, -cap, cap) : 0;
    const phi = p.basis === "actual" ? 1 : p.phi;
    const ex = g("act_excess") || 0, cred = g("act_cred") || 0;
    const tiltA = clip(phi * cred * clip(ex, -2 * cap, 2 * cap), -cap, cap);
    let level;
    if (p.basis === "underwritten") level = U !== null ? clip(U, lo, hi) : Sb;
    else if (p.basis === "actual") level = Sb + tiltA;
    else if (p.basis === "blend") level = Sb + p.wU * tiltU + p.wA * tiltA;
    else level = Sb;
    const r = [Sd, Sb, Su].map((x) => clip(level + (x - Sb), lo, hi));
    const pi = p.pi;
    const E = r[0] * pi[0] + r[1] * pi[1] + r[2] * pi[2];
    const H = 5, gam = p.gamma;
    let ce;
    if (Math.abs(gam - 1) < 1e-9) ce = Math.exp(r.reduce((a2, x, i) => a2 + pi[i] * Math.log(1 + x), 0)) - 1;
    else { const e2 = H * (1 - gam); ce = Math.pow(r.reduce((a2, x, i) => a2 + pi[i] * Math.pow(1 + x, e2), 0), 1 / e2) - 1; }
    return { r, E, ce };
  }
  function viewAA() {
    const role = "asset_allocation", v = document.getElementById("v-asset_allocation");
    const r0 = R(role), cl = r0.change_list;
    const counts = r0.card_counts || {};
    v.replaceChildren(lead(role), headTiles(role, [
      kpi("Sold by the plan (NAV)", F.bn(cl.sells.reduce((a, b) => a + b.nav_bn, 0)), el("span", { text: `proceeds ${F.bn(cl.sells.reduce((a, b) => a + b.expected_proceeds_bn, 0))}, discount ${F.bn(cl.sells.reduce((a, b) => a + b.discount_bn, 0))}` })),
      kpi("Holding cards", `${(counts.SELL || { size: 0 }).size} sell`, el("span", { text: `${(counts["SELL?"] || { size: 0 }).size} sell if limits allow · ${(counts.REFINANCE || { size: 0 }).size} refinance · ${(counts.LEVER || { size: 0 }).size} lever` })),
    ]));
    const ex = r0.extras;
    const g1 = el("div", { class: "grid g2" });
    const bas = ex.basis;
    g1.append(chartCard("The return basis decides what the PE program is worth", `Effect of the ${F.bn(D.house.pe_program_total_bn, 0)} program on the status quo's P(hurdle), and the book's forward return, under each return basis (out of sample).`,
      (host) => barsH(host, { rows: bas.map((r) => ({ label: { strategy: "ER strategy returns", blend: "Blend (ER + evidence)", underwritten: "Debiased underwriting", actual: "Actual performance persists" }[r.basis], values: [r.program_effect.d_p_goal] })), series: [{ name: "Program effect on P(hurdle)", color: cssv("--series-1") }], fmt: (t) => F.pp(t, 1), colorFn: (val) => (val >= 0 ? cssv("--series-1") : cssv("--div-neg")), labelW: 200 }),
      () => ({ cols: ["Return basis", "Book forward return", "SQ P(hurdle)", "Program effect", "Plan P(hurdle)", "Plan vs SQ"], rows: bas.map((r) => [r.basis, F.pct(r.book_return_exp, 2), F.pct(r.sq.p_goal), F.pp(r.program_effect.d_p_goal), F.pct(r.plan.p_goal), F.pp(r.delta.d_p_goal)]) })));
    const pv = ex.program_variants;
    g1.append(chartCard("PE program variants (status quo plus each variant)", "P(hurdle) against no program; NAV sold and proceeds in the table.",
      (host) => barsH(host, { rows: pv.map((r) => ({ label: r.name, short: r.name.length > 38 ? r.name.split(",")[0] : r.name, values: [r.vs_no_program.d_p_goal] })), series: [{ name: "vs no program", color: cssv("--series-1") }], fmt: (t) => F.pp(t, 1), colorFn: (val) => (val >= 0 ? cssv("--series-1") : cssv("--div-neg")), labelW: 260 }),
      () => ({ cols: ["Variant", "P(hurdle)", "vs no program", "Exposure sold", "NAV sold", "Proceeds", "Unfunded transferred"], rows: pv.map((r) => [r.name, F.pct(r.metrics.p_goal), F.pp(r.vs_no_program.d_p_goal), F.bn(r.exposure_bn), F.bn(r.nav_bn), F.bn(r.proceeds_bn), F.bn(r.unfunded_bn)]) })));
    v.append(g1, el("p", { class: "note", style: "margin-top:8px", text: "Sweeps re-optimize with one schedule for every path on 360 in-sample scenarios, for speed; the groups' plans and the adaptivity comparison use the adaptive optimizer on 900." }));
    v.append(holdingsCard());
    const g2 = el("div", { class: "grid g2", style: "margin-top:14px" });
    const bk = D.overview.buckets.filter((r) => r.uw_n >= 10);
    g2.append(chartCard("Underwriting optimism measured in this book", "Median of underwritten minus actual IRR over mature holdings (age ≥ 6 or DPI ≥ 0.75), strategies with at least 10; the engine debiases underwritten returns by it, credibility-weighted toward the department's median.",
      (host) => barsH(host, { rows: bk.map((r) => ({ label: r.label, note: `n=${r.uw_n}`, values: [r.uw_gap] })), series: [{ name: "Underwritten minus actual IRR", color: cssv("--series-1") }], fmt: (t) => F.pp(t, 1), labelW: 260 }),
      () => ({ cols: ["Strategy", "Mature holdings", "Median gap", "Debias applied"], rows: bk.map((r) => [r.label, String(r.uw_n), F.pp(r.uw_gap), F.pp(r.uw_bias)]) })));
    const sw = ex.swaps;
    const t = el("table", { class: "t" });
    t.append(el("thead", null, el("tr", null, ...["Substitution test", "NAV sold", "Proceeds", "Δ P(hurdle)", "Δ mean return"].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb = el("tbody");
    for (const r of sw) tb.append(el("tr", null, el("td", { text: r.name }), el("td", { class: "num", text: F.bn(r.sold_nav_bn, 2) }), el("td", { class: "num", text: F.bn(r.proceeds_bn, 2) }), el("td", { class: "num", text: `${F.pp(r.delta.d_p_goal, 2)} (${F.pp(r.delta.d_p_goal_ci[0], 2)} to ${F.pp(r.delta.d_p_goal_ci[1], 2)})` }), el("td", { class: "num", text: F.pp(r.delta.d_twr, 2) })));
    t.append(tb);
    const alts = (D.holdings.alternatives || []).slice(0, 10);
    const ta = el("table", { class: "t" });
    ta.append(el("thead", null, el("tr", null, ...["New money: strategy", "Downside", "Base", "Upside", "Expected", "Certainty equiv."].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tba = el("tbody");
    for (const r of alts) tba.append(el("tr", null, el("td", { text: r.label }), ...r.er.map((x) => el("td", { class: "num", text: F.pct(x) })), el("td", { class: "num", text: F.pct(r.exp) }), el("td", { class: "num", text: F.pct(r.ce) })));
    ta.append(tba);
    g2.append(el("div", { class: "card" }, el("h3", { text: "Substitution: sell, and buy what instead?" }),
      el("p", { class: "sub", text: "Each test sells named holdings today at their modeled bid and redeploys the proceeds; the change is paired on the same paths (95% interval)." }),
      el("div", { class: "tablewrap short" }, t), el("h4", { text: "Alternatives for new money (ER strategy returns under this group's world weights and risk aversion)" }), el("div", { class: "tablewrap short" }, ta)));
    v.append(g2);
    v.append(changeListCard(role), solveCard(role));
  }
  function holdingsCard() {
    if (!st.aa) st.aa = { basis: R("asset_allocation").prefs.basis, wU: R("asset_allocation").prefs.weights.underwritten, wA: R("asset_allocation").prefs.weights.actual, phi: R("asset_allocation").prefs.persistence, gamma: R("asset_allocation").prefs.risk_aversion, debias: true, q: "", dept: "", card: "PRIVATE", sort: "nav_bn", dir: -1, page: 1, cardsRole: "asset_allocation" };
    const a = st.aa;
    const card = el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "Holdings: forward returns, bids, hold thresholds and cards" }),
      el("p", { class: "sub", text: "Forward returns recompute live from your return preferences (the same formulas as the engine). Cards and hold thresholds come from the chosen group's optimized plan (the LP's shadow prices): SELL = in the plan's sales; SELL? = the bid beats the hold threshold but sale limits bind; REFINANCE = worth more held than its NAV-facility cost; LEVER = clears the hurdle and asset-level financing. The hold threshold is the price per $1 of NAV below which the plan would rather keep the holding; it counts the liquidity and tail-risk relief a sale brings (calls avoided in a drought), so a strong performer can still show SELL? when buyers pay near or above NAV." }));
    const prefs = el("div", { class: "prefs" });
    const rerender = () => { const host = document.getElementById("hold-table"); host.replaceChildren(holdingsTable()); };
    const mk = (label, input) => el("div", { class: "f" }, el("span", { class: "lab", text: label }), input);
    const basisSel = el("select", { onchange: (e) => { a.basis = e.target.value; a.page = 1; rerender(); } });
    for (const [k, t] of [["strategy", "ER strategy returns"], ["blend", "Blend"], ["underwritten", "Debiased underwriting"], ["actual", "Actual performance persists"]]) basisSel.append(el("option", { value: k, text: t, selected: k === a.basis ? "selected" : null }));
    const rng = (min, max, step, val, fn) => el("input", { type: "range", min, max, step, value: val, oninput: (e) => { fn(+e.target.value); rerender(); } });
    const cardsSel = el("select", { onchange: (e) => { a.cardsRole = e.target.value; rerender(); } });
    for (const rl of ROLES) cardsSel.append(el("option", { value: rl, text: TITLE[rl] + " plan", selected: rl === a.cardsRole ? "selected" : null }));
    prefs.append(mk("Return basis", basisSel), mk("Weight on underwriting (blend)", rng(0, 1, 0.05, a.wU, (x) => { a.wU = x; })), mk("Weight on actual (blend)", rng(0, 1, 0.05, a.wA, (x) => { a.wA = x; })),
      mk("Persistence of relative performance", rng(0, 1, 0.05, a.phi, (x) => { a.phi = x; })), mk("Risk aversion (CRRA)", rng(1, 8, 0.5, a.gamma, (x) => { a.gamma = x; })),
      mk("Debias underwriting", el("input", { type: "checkbox", checked: a.debias ? "checked" : null, onchange: (e) => { a.debias = e.target.checked; rerender(); } })), mk("Cards from", cardsSel));
    const search = el("div", { class: "searchrow" },
      el("input", { type: "search", placeholder: "Search holdings", value: a.q, oninput: (e) => { a.q = e.target.value; a.page = 1; rerender(); } }),
      (() => { const s2 = el("select", { onchange: (e) => { a.dept = e.target.value; a.page = 1; rerender(); } }); s2.append(el("option", { value: "", text: "All departments" })); for (const d of [...new Set(D.holdings.rows.map((r) => r[hcol("department")]))].sort()) s2.append(el("option", { value: d, text: d, selected: d === a.dept ? "selected" : null })); return s2; })(),
      (() => { const s2 = el("select", { onchange: (e) => { a.card = e.target.value; a.page = 1; rerender(); } }); s2.append(el("option", { value: "", text: "All holdings", selected: a.card === "" ? "selected" : null }), el("option", { value: "PRIVATE", text: "Private holdings (all cards)", selected: a.card === "PRIVATE" ? "selected" : null })); for (const c of ["SELL", "SELL?", "HOLD", "REFINANCE", "LEVER", "LIQUID"]) s2.append(el("option", { value: c, text: c, selected: c === a.card ? "selected" : null })); return s2; })());
    card.append(prefs, search, el("div", { id: "hold-table" }, holdingsTable()));
    return card;
  }
  function holdingsTable() {
    const a = st.aa;
    const p = { basis: a.basis, wU: a.wU, wA: a.wA, phi: a.phi, gamma: a.gamma, debias: a.debias, pi: piNow() };
    const cards = D.holdings.cards[a.cardsRole] || {};
    const q = a.q.trim().toLowerCase();
    let rows = D.holdings.rows.map((row) => {
      const lr = liveReturns(row, p);
      const c = cards[row[hcol("FUND_CODE")]] || [row[hcol("card")], row[hcol("p_star")], row[hcol("why")]];
      return { row, lr, card: c[0], pstar: c[1], why: c[2] };
    }).filter((x) => (!q || String(x.row[hcol("FUND_NAME")]).toLowerCase().includes(q)) && (!a.dept || x.row[hcol("department")] === a.dept)
      && (!a.card || (a.card === "PRIVATE" ? x.card !== "LIQUID" : x.card === a.card)));
    const keyf = { nav_bn: (x) => x.row[hcol("nav_bn")], E: (x) => x.lr.E, ce: (x) => x.lr.ce, bid: (x) => x.row[hcol("bid0")] || 0, uw: (x) => x.row[hcol("uw_irr")] || -9, act: (x) => x.row[hcol("act_irr")] || -9, name: (x) => String(x.row[hcol("FUND_NAME")]) };
    const kf = keyf[a.sort] || keyf.nav_bn;
    rows.sort((x, y) => (kf(x) > kf(y) ? 1 : kf(x) < kf(y) ? -1 : 0) * a.dir);
    const total = rows.length, nav = rows.reduce((s2, x) => s2 + (x.row[hcol("nav_bn")] || 0), 0);
    const per = 40, shown = rows.slice(0, a.page * per);
    const t = el("table", { class: "t" });
    const th = (label, key, num) => el("th", { class: (num ? "num " : "") + (key ? "sortable" : ""), text: label + (a.sort === key ? (a.dir > 0 ? " ▲" : " ▼") : ""), onclick: key ? () => { a.dir = a.sort === key ? -a.dir : -1; a.sort = key; document.getElementById("hold-table").replaceChildren(holdingsTable()); } : null });
    t.append(el("thead", null, el("tr", null, th("Holding", "name"), th("Strategy bucket"), th("Vintage", null, true), th("NAV", "nav_bn", true), th("Unfunded", null, true), th("UW IRR", "uw", true), th("Actual IRR", "act", true), th("Forward E", "E", true), th("Certainty eq.", "ce", true), th("Bid", "bid", true), th("Hold thr.", null, true), th("Card"))));
    const tb = el("tbody");
    const cc = CARD_COLORS();
    for (const x of shown) {
      const r = x.row, g = (c) => r[hcol(c)];
      const badge = el("span", { class: "badge", title: x.why || "" }, el("span", { class: "dot", style: `background:${cc[x.card] || cc.HOLD}` }), x.card || "–");
      tb.append(el("tr", null, el("td", { text: g("FUND_NAME") }), el("td", { text: `${g("department")} · ${g("vehicle")}` }), el("td", { class: "num", text: g("vintage") ? String(g("vintage")).slice(0, 4) : "–" }),
        el("td", { class: "num", text: F.bn(g("nav_bn"), 3) }), el("td", { class: "num", text: F.bn(g("unfunded_bn"), 3) }), el("td", { class: "num", text: F.pct(g("uw_irr")) }), el("td", { class: "num", text: F.pct(g("act_irr")) }),
        el("td", { class: "num", text: F.pct(x.lr.E) }), el("td", { class: "num", text: F.pct(x.lr.ce) }), el("td", { class: "num", text: ok(g("bid0")) && g("department") !== "Public Markets" && g("department") !== "Global Equities Division" ? F.n(g("bid0")) : "–" }), el("td", { class: "num", text: ok(x.pstar) ? F.n(x.pstar) : "–" }), el("td", null, badge)));
    }
    t.append(tb);
    const wrap = el("div", null, el("p", { class: "note", text: `${F.int(total)} holdings, ${F.bn(nav)} NAV match the filters; showing ${Math.min(shown.length, total)}. Hover a card for its reason.` }), el("div", { class: "tablewrap" }, t));
    if (shown.length < total) wrap.append(el("button", { class: "btn", style: "margin-top:8px", text: "Show more", onclick: () => { a.page++; document.getElementById("hold-table").replaceChildren(holdingsTable()); } }));
    return wrap;
  }

  // ------------------------------------------------------------------ IC
  function viewIC() {
    const v = document.getElementById("v-ic");
    const ic = D.ic, pi = piNow(), h = hurdle();
    const sqRec = twr(ic.twr.status_quo);
    const NAME = { do_nothing: "Do nothing", status_quo: "Status quo (PE program as decided)", no_program: "Status quo without the PE program" };
    const cs = (key, stress) => (ic.cases && ic.cases[key] ? ic.cases[key][stress] : null);
    const refOf = (key, stress) => (key === "status_quo" || !cs("status_quo", stress) ? null : twr(cs("status_quo", stress).twr));
    const rows = ic.rows.slice().sort((a, b) => (b.key === "do_nothing") - (a.key === "do_nothing")).map((r0) => { const r = Object.assign({}, r0, { name: NAME[r0.key] || r0.name }); const rec = twr(ic.twr[r.key]); const c = cs(r.key, ic.view.stress); return { r, s: stats(rec, pi, h), d: paired(rec, sqRec, pi, h), o: c ? objStats(twr(c.twr), flags(c.flags), pi, h, refOf(r.key, ic.view.stress)) : null }; });
    // the best of the plans on the table (the status quo rows are references, not choices)
    const best = rows.filter((x) => !(x.r.key in NAME) && !x.r.key.startsWith("to_")).sort((a, b) => b.s.pg - a.s.pg)[0];
    v.replaceChildren(el("div", { class: "lead" }, el("h2", { text: "Investment Committee: every group's plan on one view" }),
      el("p", { text: `Each group optimized its own objective under every group's limits; here all plans run on the same ${F.int(D.meta.n_oos * 3)} fresh paths under the IC view (${ic.view.prefs.basis} returns, ${stressLabel(ic.view.stress)}). The consensus plan maximizes the buffered probability of the hurdle under every limit at once.` })));
    const t = el("table", { class: "t" });
    const star5 = starPath(h).nav[5];
    const cols = ["Plan", `P(${F.pct(h, 0)})`, "vs status quo", "Balance sheet within limits", "Calls and distributions met", "Never costs the target", "Every objective together", `Fund in year 5, median (north star ${F.bn(star5, 0)})`, "CVaR10", "Debt P95", "PE exposure sold"];
    t.append(el("thead", null, el("tr", null, ...cols.map((c, i) => el("th", { class: (i ? "num" : "") + (i >= 3 && i <= 6 ? " own" : ""), text: c })))));
    const tb = el("tbody");
    const op = (x) => (x == null ? "\u2013" : F.pct(x, 1));
    for (const { r, s: s2, d, o } of rows) {
      const m = r.metrics;
      tb.append(el("tr", null, el("td", null, el("strong", { text: r.name })), el("td", { class: "num", text: `${F.pct(s2.pg)}` }), el("td", { class: "num", text: r.key === "status_quo" ? "\u2013" : `${F.pp(d.d)}` }), el("td", { class: "num own", text: op(o && o.bs) }), el("td", { class: "num own", text: op(o && o.liq) }), el("td", { class: "num own", text: r.key === "status_quo" ? "\u2013" : op(o && o.aa) }), el("td", { class: "num own", text: op(o && o.all) }), el("td", { class: "num", text: F.bn(m.nav5_p50_bn, 0) }), el("td", { class: "num", text: F.pct(s2.cvar10) }), el("td", { class: "num", text: F.bn(m.debt_p95_bn) }), el("td", { class: "num", text: F.bn(r.pe_program.exposure_bn) })));
    }
    t.append(tb);
    v.append(el("div", { class: "card" }, el("h3", { text: "The comparison matrix" }), el("p", { class: "sub", text: `Every plan on the same paths. The shaded columns test each group's objective on every path against the house limits: the balance sheet within its leverage and overcommitment limits at every year-end; every call and owner distribution paid without a forced private sale; never costing the target where the status quo reaches it; and all of them with the ${F.pct(h, 0)} target. Do nothing takes no decisions: no sales, no new commitments, no rebalancing, no new debt. The probability columns, the year-5 median and CVaR10 follow the controls; the others are at the IC view's default weights.` }), el("div", { class: "tablewrap full" }, t)));
    // every plan under every stress
    if (ic.cases) {
      const metric = st.icMetric || "goal";
      const MET = [["goal", `${F.pct(h, 0)} a year`], ["bs", "Balance sheet within limits"], ["liq", "Calls and distributions met"], ["aa", "Never costs the target"], ["all", "Every objective together"]];
      const SHORTP = { do_nothing: "Do nothing", status_quo: "Status quo", no_program: "No PE program", strategy: "Strategy", balance_sheet: "Balance Sheet", liquidity: "Liquidity", asset_allocation: "Asset Allocation", consensus: "Consensus", to_none: "Target only", to_150: "Target only, 1.5x" };
      const SHORTS = { base: "Base", prolonged_drought: "DPI decline", crisis_y1: "Crisis Y1", oil_crash: "Oil crash", exit_window_opens: "Exits reopen", rate_shock: "Rates +200bp", stagflation: "Stagflation", hf_gates: "HF gates", private_markdown: "Markdown", calls_spike: "Call spike", draw_10: "Draw 10%" };
      const sel2 = el("select", { "aria-label": "Objective", onchange: (ev) => { st.icMetric = ev.target.value; render(); } });
      for (const [k, c] of MET) sel2.append(el("option", { value: k, text: c, selected: k === metric ? "selected" : null }));
      const SK = Object.keys(D.stresses);
      const cells = rows.map(({ r }) => SK.map((k) => { const c = cs(r.key, k); return c ? objStats(twr(c.twr), flags(c.flags), pi, h, refOf(r.key, k))[metric] : null; }));
      const flat = cells.flat().filter((x) => x != null), lo = Math.min(...flat), hi = Math.max(...flat);
      const th = el("table", { class: "t heat" });
      th.append(el("thead", null, el("tr", null, el("th", { text: "Plan" }), ...SK.map((k) => el("th", { class: "num", title: stressLabel(k), text: SHORTS[k] || stressLabel(k).split(" (")[0] })))));
      const tbh = el("tbody");
      rows.forEach(({ r }, i) => tbh.append(el("tr", null, el("td", { class: "nm", title: r.name, text: SHORTP[r.key] || r.name }), ...cells[i].map((x) => {
        const na = x == null || (metric === "aa" && r.key === "status_quo");
        const a = na || hi <= lo ? 0 : 6 + (54 * (x - lo)) / (hi - lo);
        return el("td", { class: "num", style: na ? "" : `background: color-mix(in srgb, var(--series-1) ${a.toFixed(0)}%, transparent)`, text: na ? "\u2013" : F.pct(x, 0) });
      }))));
      th.append(tbh);
      v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "Every plan under every stress" }),
        el("p", { class: "sub", text: "Choose the objective; each cell is the probability it is met on that stress's paths (IC view, live weights and hurdle). Darker is higher within the table." }),
        el("div", { class: "searchrow" }, sel2), el("div", { class: "tablewrap full" }, th)));
    }
    const g = el("div", { class: "grid g2", style: "margin-top:14px" });
    g.append(chartCard("Return against tail risk, every plan", "P(hurdle) against the average of the worst 10% of 5-year returns (right is safer). The consensus plan is highlighted.",
      (host) => scatter(host, { points: rows.map(({ r, s: s2 }) => ({ label: { do_nothing: "Do nothing", status_quo: "Status quo", no_program: "No PE program", to_none: "Target only", to_150: "Target only, 1.5x" }[r.key] || r.name.replace(" plan", ""), x: s2.cvar10, y: s2.pg, emph: r.key === "consensus", extra: [{ value: F.pct(r.metrics.p_red, 2), name: "P(red event)" }] })), xfmt: (t2) => F.pct(t2, 1), yfmt: (t2) => F.pct(t2, 0), xlabel: "CVaR10 of the 5-year return (right is safer)", ylabel: "P(hurdle)", h: 300 }),
      () => ({ cols: ["Plan", "P(hurdle)", "CVaR10"], rows: rows.map(({ r, s: s2 }) => [r.name, F.pct(s2.pg), F.pct(s2.cvar10)]) })));
    const sel = st.icPick || (st.icPick = { a: "status_quo", b: "consensus" });
    const pa = rows.find((x) => x.r.key === sel.a) || rows[0], pb = rows.find((x) => x.r.key === sel.b) || rows[rows.length - 1];
    const ha = histo(twr(ic.twr[pa.r.key]), pi), hb = histo(twr(ic.twr[pb.r.key]), pi);
    const pick = (key, which) => { const s2 = el("select", { onchange: (e) => { st.icPick[which] = e.target.value; render(); } }); for (const { r } of rows) s2.append(el("option", { value: r.key, text: r.name, selected: r.key === key ? "selected" : null })); return s2; };
    const c2 = chartCard("Compare two plans' distributions", "Choose the plans; the line marks the hurdle.",
      (host) => { host.append(el("div", { class: "searchrow" }, pick(pb.r.key, "b"), el("span", { class: "note", text: "against" }), pick(pa.r.key, "a")), legend([{ name: pb.r.name, color: cssv("--series-1") }, { name: pa.r.name, color: cssv("--deemph"), kind: "line" }])); histChart(host, { edges: D.meta.hist_edges, series: [{ name: pb.r.name, p: hb, color: cssv("--series-1") }, { name: pa.r.name, p: ha, color: cssv("--deemph") }], marker: { x: h, label: `${F.pct(h, 0)} hurdle` } }); },
      () => ({ cols: ["Bin", pb.r.name, pa.r.name], rows: hb.map((p2, i) => [`${F.pct(D.meta.hist_edges[i], 0)} to ${F.pct(D.meta.hist_edges[i + 1], 0)}`, F.pct(p2, 2), F.pct(ha[i], 2)]) }));
    g.append(c2);
    v.append(g);
    if (ic.hf_leverage) v.append(leverageCard());
    // where the groups disagree
    const by = Object.fromEntries(rows.map((x) => [x.r.key, x]));
    const lines = [];
    const has = (k) => by[k] !== undefined;
    const ppAbs = (x) => Math.abs(x * 100).toFixed(1) + "pp";
    const more = (x) => (x >= 0 ? "more" : "less");
    const better = (x) => (x >= 0 ? "better" : "worse");
    if (has("strategy") && has("liquidity")) {
      const dg = by.strategy.s.pg - by.liquidity.s.pg, dt = by.liquidity.s.cvar10 - by.strategy.s.cvar10;
      const lp = R("liquidity").plan, sp = R("strategy").plan;
      lines.push(`Strategy vs Liquidity: the Strategy plan reaches the hurdle ${ppAbs(dg)} ${more(dg)} often. The Liquidity plan holds ${F.bn(lp.cash + lp.treasury)} of reserve (Strategy ${F.bn(sp.cash + sp.treasury)}) and ${F.bn(lp.beta_bn)} of synthetic beta (Strategy ${F.bn(sp.beta_bn)}); its worst 10% is ${ppAbs(dt)} ${better(dt)}, and it draws the revolver in ${F.pct(by.liquidity.r.metrics.p_revolver, 1)} of paths on this view.`);
    }
    if (has("balance_sheet")) {
      const dg = best.s.pg - by.balance_sheet.s.pg;
      const bestTail = rows.every((x) => x.s.cvar10 <= by.balance_sheet.s.cvar10 + 1e-9);
      lines.push(`Balance Sheet: its risk-averse, pessimistic plan ${dg > 0 ? `gives up ${ppAbs(dg)} of P(hurdle) against the best plan (${best.r.name})` : "is the best plan for P(hurdle) on this view"} for a CVaR10 of ${F.pct(by.balance_sheet.s.cvar10)}${bestTail ? ", the best tail on the page" : ""}.`);
    }
    if (has("no_program")) {
      const dg = by.status_quo.s.pg - by.no_program.s.pg;
      lines.push(`The PE program as decided ${dg < 0 ? "lowers" : "raises"} the status quo's P(hurdle) by ${ppAbs(dg)} on this view: drought-level bids for underperformers sit below the value of holding them, and the buyers take future commitments with them.`);
    }
    if (has("do_nothing")) {
      const dn = by.do_nothing, dsq = by.status_quo.s.pg - dn.s.pg, dbest = best.s.pg - dn.s.pg;
      lines.push(`Doing nothing reaches the ${F.pct(h, 0)} north star in ${F.pct(dn.s.pg)} of paths: ${dsq < 0 ? `better than the status quo by ${F.pp(-dsq)}, because the status quo sells PE at drought bids` : `${F.pp(dsq)} behind the status quo`}. The best plan (${best.r.name}) adds ${F.pp(dbest)} to doing nothing.`);
    }
    if (has("to_none")) {
      const tn = by.to_none, tr = (R("strategy").extras.target_only || []).find((x) => x.key === "to_none");
      lines.push(`The ${F.pct(h, 0)} target alone (every group's limit removed, no borrowing) reaches ${F.pct(tn.s.pg)}, but keeps the balance sheet within limits in ${F.pct(tn.o.bs, 0)} of paths and pays every call and distribution without a forced sale in ${F.pct(tn.o.liq, 0)}${tr ? `: it holds ${F.bn(tr.liquid.HF)} in hedge funds and runs the reserve down` : ""}.`);
    }
    if (has("consensus")) lines.push(`Consensus (every group's limits at once): ${F.pct(by.consensus.s.pg)} P(hurdle), ${F.pp(by.consensus.d.d)} vs the status quo, CVaR10 ${F.pct(by.consensus.s.cvar10)}, red-event probability ${F.pct(by.consensus.r.metrics.p_red, 2)}.`);
    v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "Where the groups disagree" }), el("ul", { class: "tight" }, ...lines.map((x) => el("li", { text: x })))));
    if (ic.consensus_plan) {
      const cp = ic.consensus_plan;
      v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "The consensus plan, in one paragraph" }),
        el("p", { class: "note", text: `Sell ${Object.keys(cp.sell).length} private holding groups in the program's tranches (${Object.entries(cp.sell).map(([k, fr]) => `${BLABEL[k.split(":")[0]] || k} ${{ tail: "underperformers", core: "core", swap: "substitution test" }[k.split(":")[1]] || ""}: ${fr.map((f2, i) => (f2 > 0.001 ? `${Math.round(f2 * 100)}% in year ${i + 1}` : null)).filter(Boolean).join(", ")}`).join("; ")}). Hold ${F.bn(cp.cash + cp.treasury)} of reserve. Liquid allocation: ${Object.entries(cp.liquid).filter(([, x]) => x > 0.05).map(([k, x]) => `${BLABEL[k] || k} ${F.bn(x)}`).join(", ")}. Term debt ${F.bn(cp.term_bn)} (${cp.term_sched.map((x, i) => `year ${i + 1} ${F.bn(x)}`).join(", ")}); NAV facility ${F.bn(cp.navf_bn)}; synthetic beta ${F.bn(cp.beta_bn)}.` })));
    }
  }

  // Leverage on the hedge-fund allocation: how much borrowing reaches 10% (static: the IC view's default weights)
  function leverageCard() {
    const L = D.ic.hf_leverage, g = D.meta.goal_rate, S = L.bases.status_quo, Cn = L.bases.consensus;
    const pts = (rows, key) => rows.map((r) => ({ x: r.borrow_bn, y: r[key] }));
    const cr = L.cross.status_quo || {}, cc = (L.cross.consensus || {});
    const lev = (b) => F.x(1 + b / L.W0_bn, 2);
    const bn0 = (b) => (b == null ? "beyond $100bn" : `$${b.toFixed(0)}bn`);
    const card = el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: `Leverage on the hedge-fund allocation: how much borrowing reaches ${F.pct(g, 0)}?` }),
      el("p", { class: "sub", text: `ADIC borrows at the fund level (term debt at ${F.pct(L.rate, 2)}, SOFR plus the term spread), draws it today and invests it in hedge funds (today ${F.bn(L.hf_today_bn)}), rebalanced like every sleeve. Out of sample on the IC view; the balance-sheet test uses the house cap of ${F.x(L.lev_cap, 2)}.` }));
    const g2 = el("div", { class: "grid g2" });
    const ser = [{ name: "Status quo + leverage", color: cssv("--series-1"), pts: pts(S.base, "p_goal") }];
    if (Cn) ser.push({ name: "Consensus plan + leverage", color: cssv("--series-2"), pts: pts(Cn.base, "p_goal") });
    ser.push({ name: "Status quo + leverage, crisis in year 1", color: cssv("--series-1"), dash: true, pts: pts(S.crisis_y1, "p_goal") });
    g2.append(chartCard(`Chance of ${F.pct(g, 0)} a year`, "Against new borrowing; dashed verticals mark where each reaches an even chance (median at the target).",
      (host) => { host.append(legend(ser.map((x) => ({ name: x.name, color: x.color, kind: "line" })))); lineXY(host, { series: ser, refs: [{ y: 0.5, label: "even chance" }], vrefs: [{ x: cr.median_10, label: `status quo ${bn0(cr.median_10)}` }, { x: cc.median_10, label: `consensus ${bn0(cc.median_10)}`, row: 1 }], xfmt: (t) => `$${t}bn`, yfmt: (t) => F.pct(t, 0), xlabel: "New borrowing invested in hedge funds ($bn)", h: 280 }); },
      () => ({ cols: ["Borrowing", "Leverage today", "Status quo + leverage", "Consensus + leverage", "Status quo, crisis Y1"], rows: S.base.map((r, i) => [`$${r.borrow_bn}bn`, lev(r.borrow_bn), F.pct(r.p_goal), Cn ? F.pct(Cn.base[i].p_goal) : "\u2013", F.pct(S.crisis_y1[i].p_goal)]) })));
    const ser2 = [{ name: "Median, status quo + leverage", color: cssv("--series-1"), pts: pts(S.base, "twr_p50") }, { name: "Mean, status quo + leverage", color: cssv("--series-1"), dash: true, pts: pts(S.base, "twr_mean") }];
    if (Cn) ser2.push({ name: "Median, consensus + leverage", color: cssv("--series-2"), pts: pts(Cn.base, "twr_p50") });
    g2.append(chartCard("Five-year return", `Median and mean annualized return against new borrowing; the dashed line is ${F.pct(g, 0)}.`,
      (host) => { host.append(legend(ser2.map((x) => ({ name: x.name, color: x.color, kind: "line" })))); lineXY(host, { series: ser2, refs: [{ y: g, label: `${F.pct(g, 0)} a year` }], vrefs: [{ x: cr.mean_10, label: `mean ${bn0(cr.mean_10)}` }, { x: cr.median_10, label: `median ${bn0(cr.median_10)}`, row: 1 }], xfmt: (t) => `$${t}bn`, yfmt: (t) => F.pct(t, 1), xlabel: "New borrowing invested in hedge funds ($bn)", h: 280 }); },
      () => ({ cols: ["Borrowing", "Median", "Mean", "Consensus median"], rows: S.base.map((r, i) => [`$${r.borrow_bn}bn`, F.pct(r.twr_p50, 2), F.pct(r.twr_mean, 2), Cn ? F.pct(Cn.base[i].twr_p50, 2) : "\u2013"]) })));
    card.append(g2);
    const t = el("table", { class: "t" });
    const cols = ["Borrowing", "Leverage today", "Leverage, worst 5%", `P(${F.pct(g, 0)})`, "Median", "Mean", "CVaR10", "Worst 1%", "Balance sheet within limits", "Calls and distributions met", `P(${F.pct(g, 0)}), crisis Y1`, "Forced sale if hedge funds gate"];
    t.append(el("thead", null, el("tr", null, ...cols.map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tb = el("tbody");
    S.base.forEach((r, i) => tb.append(el("tr", null, el("td", { text: `$${r.borrow_bn}bn` }), el("td", { class: "num", text: lev(r.borrow_bn) }), el("td", { class: "num", text: F.x(r.lev_p95, 2) }), el("td", { class: "num", text: F.pct(r.p_goal, 1) }), el("td", { class: "num", text: F.pct(r.twr_p50, 2) }), el("td", { class: "num", text: F.pct(r.twr_mean, 2) }), el("td", { class: "num", text: F.pct(r.cvar10, 1) }), el("td", { class: "num", text: F.pct(r.cvar1, 1) }), el("td", { class: "num own", text: F.pct(r.p_bs, 0) }), el("td", { class: "num own", text: F.pct(r.p_liq, 0) }), el("td", { class: "num", text: F.pct(S.crisis_y1[i].p_goal, 1) }), el("td", { class: "num", text: F.pct(S.hf_gates[i].p_red, 1) }))));
    t.append(tb);
    const per10 = (S.base[S.base.length - 1].p_goal - S.base[0].p_goal) / (S.base[S.base.length - 1].borrow_bn / 10);
    const msg = [
      `On the status quo, the mean five-year return reaches ${F.pct(g, 0)} with about ${bn0(cr.mean_10)} of borrowing (${cr.mean_10 != null ? lev(cr.mean_10) : "\u2013"}); an even chance of ${F.pct(g, 0)} a year (the median path at the target) takes about ${bn0(cr.median_10)} (${cr.median_10 != null ? lev(cr.median_10) : "\u2013"}), taking hedge funds to about ${cr.median_10 != null ? F.bn(L.hf_today_bn + cr.median_10) : "\u2013"}.`,
      `It is a weak lever: each $10bn adds about ${F.pp(per10)} of P(${F.pct(g, 0)}), because hedge funds earn only a few points over the borrowing cost and less in the Downside world; P(${F.pct(g, 0)}) reaches ${F.pct(S.base[S.base.length - 1].p_goal, 0)} at $${S.base[S.base.length - 1].borrow_bn}bn.`,
      `Above the house cap the balance-sheet objective fails on every path, and markdowns push the worst 5% of paths well past the starting leverage.`,
      Cn ? `From the consensus plan, about ${bn0(cc.median_10)} is enough for an even chance: it already earns more per unit of risk.` : "",
    ].filter(Boolean);
    card.append(el("div", { class: "tablewrap full", style: "margin-top:12px" }, t), el("ul", { class: "tight", style: "margin-top:10px" }, ...msg.map((x) => el("li", { text: x }))));
    return card;
  }

  // ------------------------------------------------------------------ YALE MODEL
  function viewYale() {
    const v = document.getElementById("v-yale"), Y = D.yale;
    if (!Y) { v.replaceChildren(el("p", { text: "Rebuild the page to include the Yale-model benchmark." })); return; }
    const fit = Y.fit;
    v.replaceChildren(el("div", { class: "lead" }, el("h2", { text: "Against the Yale model (Takahashi-Alexander)" }),
      el("p", { text: `The Yale model projects each private fund's calls, distributions and NAV from its age: calls a fixed share of the remaining commitment (25%, 33%, then 50% a year), distributions a share of NAV that rises with age along a bow, NAV growing at a fixed rate. It is multi-year but deterministic: one path, no markets, no exit cycle, no liabilities, no decisions. Here it runs on ADIC's own book with the same expected returns as the engine, as given and fitted to ADIC's vintages, against what the engine sees.` })));
    const dp = Y.dpi.filter((r) => r.vintage >= 2010 && r.vintage <= 2025 && r.dpi_actual != null);
    const fitLab = `Yale model fitted (life x${fit.life_mult.toFixed(1)}, bow x${fit.bow_mult.toFixed(1)})`;
    const g1 = el("div", { class: "grid g2" });
    g1.append(chartCard("DPI by vintage: ADIC's actual against the Yale model", `Commitment-weighted, live book. The textbook settings overstate recent vintages; fitting needs a fund life ${fit.life_mult >= 2.95 ? "at least " : ""}${fit.life_mult.toFixed(1)}x the textbook to come close (error ${F.pct(1 - fit.sse / fit.sse_textbook, 0)} lower), because today's shortfall is an exit drought, not an age effect.`,
      (host) => { host.append(legend([{ name: "ADIC actual", color: cssv("--series-1") }, { name: "Yale model, textbook", color: cssv("--series-2"), kind: "line" }, { name: fitLab, color: cssv("--series-3"), kind: "line" }])); colsChart(host, { cats: dp.map((r) => String(r.vintage)), series: [{ name: "ADIC actual", color: cssv("--series-1"), values: dp.map((r) => r.dpi_actual) }], lines: [{ name: "Yale model, textbook", color: cssv("--series-2"), values: dp.map((r) => r.dpi_yale) }, { name: fitLab, color: cssv("--series-3"), values: dp.map((r) => r.dpi_fit) }], fmt: (t) => F.x(t, 2), h: 260, catTitle: "Vintage " }); },
      () => ({ cols: ["Vintage", "Age", "ADIC actual", "Yale textbook", "Yale fitted"], rows: dp.map((r) => [r.vintage, r.age.toFixed(1), F.x(r.dpi_actual, 2), F.x(r.dpi_yale, 2), F.x(r.dpi_fit, 2)]) })));
    const pi = (Y.paid_in || []).filter((r) => r.vintage >= 2010 && r.vintage <= 2025);
    g1.append(chartCard("Paid-in by vintage: ADIC's actual against the Yale model", "Share of commitments called. The Yale model calls nearly everything; ADIC's mature vintages leave part of each commitment uncalled.",
      (host) => { host.append(legend([{ name: "ADIC actual", color: cssv("--series-1") }, { name: "Yale model", color: cssv("--series-2"), kind: "line" }])); colsChart(host, { cats: pi.map((r) => String(r.vintage)), series: [{ name: "ADIC actual", color: cssv("--series-1"), values: pi.map((r) => r.paid_in_actual) }], lines: [{ name: "Yale model", color: cssv("--series-2"), values: pi.map((r) => r.paid_in_yale) }], fmt: (t) => F.pct(t, 0), h: 260, catTitle: "Vintage " }); },
      () => ({ cols: ["Vintage", "ADIC actual", "Yale model"], rows: pi.map((r) => [r.vintage, F.pct(r.paid_in_actual), F.pct(r.paid_in_yale)]) })));
    v.append(g1);
    const E = Y.engine.base, E2 = Y.engine.exit_window_opens;
    const proj = (key, title, sub) => chartCard(title, sub,
      (host) => { host.append(legend([{ name: "Engine P5-P95", color: "var(--wash-1b)", kind: "band" }, { name: "Engine median (exit drought today)", color: cssv("--series-1"), kind: "line" }, { name: "Engine mean, exits reopen", color: cssv("--series-3"), kind: "line" }, { name: "Yale textbook", color: cssv("--series-2"), kind: "line" }, { name: "Yale fitted", color: cssv("--series-4"), kind: "line" }])); fanChart(host, { labels: FLOWYEARS, fans: [{ name: "Engine", fan: E[key], color: cssv("--series-1") }], lines: [{ name: "Exits reopen", values: E2[key].mean, color: cssv("--series-3") }, { name: "Yale", values: Y.ta[key], color: cssv("--series-2") }, { name: "Yale fit", values: Y.ta_fit[key], color: cssv("--series-4") }], yfmt: (t) => F.bn(t, 0), zero: key !== "net", h: 250 }); },
      () => ({ cols: ["Year", "Engine P5", "Engine median", "Engine P95", "Exits reopen (mean)", "Yale textbook", "Yale fitted"], rows: FLOWYEARS.map((y2, i) => [y2, F.bn(E[key].p5[i]), F.bn(E[key].p50[i]), F.bn(E[key].p95[i]), F.bn(E2[key].mean[i]), F.bn(Y.ta[key][i]), F.bn(Y.ta_fit[key][i])]) }));
    const g2 = el("div", { class: "grid g2", style: "margin-top:14px" });
    g2.append(proj("dist", "Private distributions over the next five years", "Status quo without the PE program, $bn a year. The engine starts in today's exit drought and lets it end at its own pace; the Yale model has no exit cycle."));
    g2.append(proj("calls", "Capital calls over the next five years", "The Yale model calls half of each mature fund's remaining commitment every year (the fit changes distributions, not calls, so its two lines coincide); the engine's calls follow fund age and the exit window."));
    v.append(g2);
    const cap = [
      ["Periods", "Yearly, from each fund's age", "Five annual decision stages, 20 quarters simulated; decisions dated by year (sales in three tranches, commitments each year, term debt drawn in years 1-3) with recourse every year"],
      ["Uncertainty", "None: one deterministic path", `Regime-switching markets (macro, exit window, oil), fat-tailed factors, the oil-linked owner draw, three ER worlds, ${Object.keys(D.stresses).length} stresses; ${F.int(D.meta.n_oos * 3)} fresh paths per plan`],
      ["Private cash flows", "Fixed call and distribution schedules, fixed growth", "The same age-based structure, moved by the exit window (distributions about half of normal in a drought), markets and the ER world"],
      ["Rest of the fund", "Not modeled", "Every sleeve: hedge funds with gates, equities, Agg, MAO, reserve, debt, synthetic beta"],
      ["Liabilities and liquidity", "Not modeled", "Owner distribution, calls, interest; the waterfall of reserve, liquid sales, revolver, forced sales; coverage each year"],
      ["Decisions", "Pacing set by hand against the projection", "One multi-period optimization of sales, allocation, commitments, debt and beta under every group's limits"],
      ["Objective", "None (a projection tool)", "Probability of 10% a year (GBO), utility, liquidity cost or mean-CVaR; every group's objective tested on every path"],
      ["Validation", "None", "Out-of-sample certification on fresh paths with confidence intervals; the Yale model's own DPI and paid-in checked against ADIC's vintages above"],
    ];
    const tc = el("table", { class: "t" });
    tc.append(el("thead", null, el("tr", null, ...["", "Yale model (Takahashi-Alexander)", "This framework"].map((c) => el("th", { text: c })))));
    const tbc = el("tbody");
    for (const r of cap) tbc.append(el("tr", null, el("th", { text: r[0] }), el("td", { text: r[1] }), el("td", { text: r[2] })));
    tc.append(tbc);
    const d1 = E.dist.mean[0], dY = Y.ta.dist[0], dF = Y.ta_fit.dist[0];
    const msg = [
      `Next year's private distributions: the engine expects ${F.bn(d1)} on average from today's drought (${F.bn(E2.dist.mean[0])} if exits reopen); the Yale model projects ${F.bn(dY)} as given and ${F.bn(dF)} fitted. Planning liquidity on the Yale model would count on cash that the current market is not paying.`,
      `Calls: the Yale model calls ${F.bn(Y.ta.calls[0])} next year against the engine's ${F.bn(E.calls.mean[0])} on average; ADIC's mature vintages show that part of every commitment is never called.`,
      "The Yale model cannot give a probability of reaching 10%, a tail, a forced-sale risk or a best decision: it has one path and no objective. Every number on the other tabs needs the distribution.",
      "What carries over: the engine keeps the Yale model's insight that cash flows are driven by fund age, and adds what moves them.",
    ];
    v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "What the comparison shows" }), el("ul", { class: "tight" }, ...msg.map((x) => el("li", { text: x })))));
    v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "Side by side" }), el("div", { class: "tablewrap full" }, tc)));
    const fam = Y.families;
    const tf = el("table", { class: "t" });
    tf.append(el("thead", null, el("tr", null, ...["Strategy family", "Rate of contribution by year", "Life (years)", "Bow", "Yield"].map((c, i) => el("th", { class: i ? "num" : "", text: c })))));
    const tbf = el("tbody");
    for (const [k, f] of Object.entries(fam)) tbf.append(el("tr", null, el("td", { text: k.replace("_", " ") }), el("td", { class: "num", text: f.rc.map((x) => F.pct(x, 0)).join(" / ") }), el("td", { class: "num", text: f.life.toFixed(0) }), el("td", { class: "num", text: f.bow.toFixed(1) }), el("td", { class: "num", text: F.pct(f.yield, 0) })));
    tf.append(tbf);
    v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "The Yale model's settings (textbook)" }), el("p", { class: "sub", text: "Growth G is each strategy's ER base return. These are assumptions in config/assumptions.json (yale.families); the fit scales every life and bow together to ADIC's DPI by vintage." }), el("div", { class: "tablewrap full" }, tf)));
  }

  // ------------------------------------------------------------------ DATA & METHOD
  function viewData() {
    const v = document.getElementById("v-data");
    const ov = D.overview, q = ov.quality, cov = ov.coverage;
    v.replaceChildren(el("div", { class: "lead" }, el("h2", { text: "Data, classification and assumptions" }),
      el("p", { text: `Fund file: ${D.meta.files.fund_file}; strategy returns: ${D.meta.files.er_file}. Book as of ${q.as_of}. Built ${D.meta.built}.` + (D.meta.files.sensitivity_label ? " Both workbooks carry a sensitivity label: this page holds holding-level data; keep it inside ADIC." : "") })));
    const g = el("div", { class: "grid g2" });
    const t1 = el("table", { class: "t" });
    t1.append(el("thead", null, el("tr", null, ...["Rows", "Count", "NAV +", "NAV −", "Note"].map((c, i) => el("th", { class: i && i < 4 ? "num" : "", text: c })))));
    const tb1 = el("tbody");
    tb1.append(el("tr", null, el("td", null, el("strong", { text: "Live book (marked within 12 months)" })), el("td", { class: "num", text: F.int(q.live_rows) }), el("td", { class: "num", text: F.bn(q.live_nav_bn) }), el("td", { class: "num", text: "–" }), el("td", { text: `unfunded ${F.bn(q.live_unfunded_bn)}` })));
    for (const r of q.excluded) tb1.append(el("tr", null, el("td", { text: r.reason }), el("td", { class: "num", text: F.int(r.rows) }), el("td", { class: "num", text: F.bn(r.nav_pos_bn) }), el("td", { class: "num", text: F.bn(r.nav_neg_bn) }), el("td", { text: r.note })));
    t1.append(tb1);
    const t2 = el("table", { class: "t" });
    t2.append(el("thead", null, el("tr", null, ...["Largest legacy rows (excluded)", "NAV", "Last valued"].map((c, i) => el("th", { class: i === 1 ? "num" : "", text: c })))));
    const tb2 = el("tbody");
    for (const r of q.top_legacy_rows.slice(0, 12)) tb2.append(el("tr", null, el("td", { text: r.name }), el("td", { class: "num", text: F.bn(r.nav_bn, 2) }), el("td", { text: r.last_valued })));
    t2.append(tb2);
    g.append(el("div", { class: "card" }, el("h3", { text: "What the fund file contains" }), el("p", { class: "sub", text: `${F.int(q.file_rows)} rows, gross NAV ${F.bn(q.file_nav_gross_bn)}. Only rows marked at or near ${q.as_of} are live holdings; the rest are legacy or pipeline rows, listed, never dropped silently.` }), el("div", { class: "tablewrap short" }, t1), el("h4", { text: "Legacy rows" }), el("div", { class: "tablewrap short" }, t2)));
    const t3 = el("table", { class: "t" });
    t3.append(el("thead", null, el("tr", null, ...["Low-confidence mapping (largest)", "Class / style", "Mapped to", "NAV"].map((c, i) => el("th", { class: i === 3 ? "num" : "", text: c })))));
    const tb3 = el("tbody");
    for (const r of cov.low_confidence_top.slice(0, 25)) tb3.append(el("tr", null, el("td", { text: r.name }), el("td", { text: `${r.class || "–"} / ${r.style || "–"}` }), el("td", { text: r.bucket }), el("td", { class: "num", text: F.bn(r.nav_bn, 3) })));
    t3.append(tb3);
    g.append(el("div", { class: "card" }, el("h3", { text: "Mapping holdings to the ER strategies" }), el("p", { class: "sub", text: `The fund file has no strategy column, so ordered rules map each holding (config/classifier_rules.json; overrides in config/mapping_overrides.csv). ${F.pct(cov.share_high_or_medium, 0)} of NAV maps with high or medium confidence; ${F.bn(cov.proxied_bn)} of Asia / RoW buyout is proxied by the Buyout - US row (the ER file has no Asia row).` }),
      el("div", { class: "kv" }, ...Object.entries(cov.nav_by_confidence_bn).sort((a, b) => ["high", "medium", "low"].indexOf(a[0]) - ["high", "medium", "low"].indexOf(b[0])).flatMap(([k, x]) => [el("span", { class: "k", text: k }), el("span", { class: "v", text: F.bn(x) })])), el("h4", { text: "Review list" }), el("div", { class: "tablewrap short" }, t3)));
    v.append(g);
    // ER and buckets
    const tb = el("table", { class: "t" });
    tb.append(el("thead", null, el("tr", null, ...["ER strategy", "NAV", "Unfunded", "Pacing (SQ)", "ER Down", "ER Base", "ER Up", "Existing E", "Existing CE", "UW optimism", "Source"].map((c, i) => el("th", { class: i && i < 10 ? "num" : "", text: c })))));
    const tbb = el("tbody");
    for (const r of ov.buckets) tbb.append(el("tr", null, el("td", { text: r.label }), el("td", { class: "num", text: F.bn(r.nav_bn) }), el("td", { class: "num", text: F.bn(r.unfunded_bn) }), el("td", { class: "num", text: F.bn(r.pace_sq_bn, 2) }), ...r.er.map((x) => el("td", { class: "num", text: F.pct(x) })), el("td", { class: "num", text: F.pct(r.exist_exp) }), el("td", { class: "num", text: F.pct(r.exist_ce) }), el("td", { class: "num", text: r.uw_n ? F.pp(r.uw_bias) : "–" }), el("td", null, r.sleeve_bn > 0.001 ? tag("assume") : tag("data"), r.er_flags ? el("span", { class: "note", text: " " + r.er_flags }) : null)));
    tb.append(tbb);
    v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "The book by ER strategy" }), el("p", { class: "sub", text: "NAV and unfunded from the fund file (internal sleeves from the whole-fund NAV); ER returns as given; existing-holding returns under the Strategy view; pacing = average commitment of the 2023-25 vintages." }), el("div", { class: "tablewrap" }, tb)));
    // assumptions
    const ta = el("table", { class: "t fixed" });
    ta.append(el("colgroup", null, ...["20%", "17%", "7%", "38%", "18%"].map((w) => el("col", { style: `width:${w}` }))));
    ta.append(el("thead", null, el("tr", null, ...["Assumption", "Value", "Unit", "Rationale", "Source"].map((c) => el("th", { text: c })))));
    const tba = el("tbody");
    const showVal = (val) => (Array.isArray(val) ? val.map((x) => (typeof x === "object" ? JSON.stringify(x) : String(x))).join(", ")
      : val && typeof val === "object" ? Object.entries(val).map(([k, x]) => `${k}: ${typeof x === "object" ? JSON.stringify(x) : x}`).join(", ") : String(val));
    for (const r of D.assumptions) tba.append(el("tr", null, el("td", { text: r.key }), el("td", { text: showVal(r.value) }), el("td", { text: r.unit || "" }), el("td", { text: r.rationale || "" }), el("td", { text: r.source || "" })));
    ta.append(tba);
    v.append(el("div", { class: "card", style: "margin-top:14px" }, el("h3", { text: "Every assumption (config/assumptions.json)" }), el("p", { class: "sub", text: "Each non-data number with its unit, rationale and source. The regime, factor and owner-draw model is the MPO v2 prototype's (examples/mpo_v2/params.json)." }), el("div", { class: "tablewrap" }, ta)));
    v.append(methodCard());
  }
  function methodCard() {
    const cb = D.overview.coverage.nav_by_confidence_bn, cbt = Object.values(cb).reduce((a, b) => a + b, 0) || 1;
    const mapShare = F.pct(((cb.high || 0) + (cb.medium || 0)) / cbt, 0);
    const m = el("div", { class: "card method", style: "margin-top:14px" }, el("h3", { text: "Method in brief" }));
    const p = (t) => el("p", { text: t });
    const fm = (t) => el("span", { class: "formula", text: t });
    m.append(
      el("h4", { text: "1. Returns: preference and utility, not a fixed fusion" }),
      p("Three return sources per holding: the ER strategy forward return (Downside / Base / Upside), the underwritten base IRR (debiased by the underwriting optimism measured in this book), and the since-inception actual IRR (relative to same-strategy, same-vintage peers). Each group chooses the basis and weights, the ER world probabilities, and its risk aversion:"),
      fm("level_i = ER_base + w_U x youth_i x clip(UW_i - beta_b - ER_base) + w_A x clip(phi x cred_i x (actual_i - peer_i))\nr_i,s = clip(level_i + (ER_s - ER_base))     E_i = sum_s pi_s r_i,s     CE_i = [sum_s pi_s (1 + r_i,s)^(5(1 - gamma))]^(1/(5(1 - gamma))) - 1"),
      el("h4", { text: "2. Scenarios" }),
      p("The MPO v2 prototype's quarterly regime generator (macro, exit window, oil; six factors with fat tails) and private-market engine (calls and distributions by age and exit window) run every holding group at full size; each ER column is a world, and each bucket's alpha is set so its mean return in each world equals the ER (or preference) return. Stresses shock the factor paths (crisis, oil, rates) or the regimes (prolonged drought)."),
      el("h4", { text: "3. Optimization" }),
      p("One linear program over five annual stages on in-sample scenarios: secondary sales in three dated tranches, today's liquid allocation and reserve, five years of commitments, dated term debt, the NAV facility and synthetic beta, all non-anticipative. Recourse is need-based only (reserve, liquid sales at their expected return, the revolver, forced sales as a last resort), so no path's future can be traded on. Every group's limits are rows: leverage, debt, LTV, overcommitment, the reserve floor, the forced-sale appetite, the depth guard (tail no worse than the status quo), IC ranges, market depth and the " + F.bn(D.house.pe_program_total_bn, 0) + " PE program. Objectives: GBO (maximum buffered probability of the hurdle, as the prototype), CRRA utility, liquidity risk at a return floor."),
      el("h4", { text: "4. Certification" }),
      p("Every plan is re-run on fresh paths the LP never saw by an exact quarterly simulator with the Liquidity group's waterfall (liquid sales, hedge funds behind gates, the revolver, then forced sales). The probabilities on this page are those out-of-sample results; the in-sample figure is shown beside them as the optimism gap."),
      el("h4", { text: "North star and doing nothing" }),
      p("The Strategy group's north star is 10% a year for five years (the hurdle control moves it). Doing nothing is the baseline of no decisions: no sales (the PE program is not executed), no new commitments, no rebalancing or reserve top-ups and no new debt; distributions accumulate as cash and the owner's distribution and existing calls are paid through the waterfall. The status quo is different: it executes the PE program as decided and keeps today's pacing and annual rebalancing."),
      el("h4", { text: "5. Objectives as tests" }),
      p(`Every case reports the probability that each group's objective is met, alone and with the return target, from the same paths. Strategy: the five-year return reaches the hurdle. Balance Sheet: gross leverage at or below ${F.x(D.house.lev_cap, 2)} and overcommitment at or below ${F.x(D.house.overcommit, 2)} of NAV at every year-end. Liquidity: every capital call and owner distribution paid without a forced private sale. Asset Allocation: the substitutions never cost the target (wherever the status quo reaches it on a path, the plan does too). Each test uses the house limits whatever plan is judged, so a plan built without them (the target alone) is held to them.`),
      el("h4", { text: "Limitations" }),
      el("ul", { class: "tight" }, ...["The fund file has no strategy column: mappings are rule-based (" + mapShare + " of NAV high or medium confidence) and editable.", "Internal sleeves (Global Equities Division, Treasury, Cash, Global Agg, MAO capital) and today's drawn debt are assumptions until actual balances are entered.", "ER returns are read as compound (geometric) annual returns; if they are arithmetic, every P(hurdle) here is optimistic.", "Secondary bids are modeled (strategy, age, market state, relative performance), not quotes.", "Liquid sleeves are held at their plan weights (annual rebalancing); there is no rate-level path beyond the stresses, and SOFR is flat."].map((x) => el("li", { text: x }))));
    return m;
  }

  // ------------------------------------------------------------------ shell
  function renderStamp() {
    const b = D.overview.book, box = document.getElementById("stamp");
    box.replaceChildren(el("span", { class: "chip", text: `Book ${D.meta.files.as_of}` }), el("span", { class: "chip", text: `Whole fund ${F.bn(b.total_nav_bn, 0)} · fund file ${F.bn(b.file_nav_bn)}` }),
      el("span", { class: "chip", text: `${F.int(D.meta.n_oos * 3)} certification paths` }), D.meta.files.sensitivity_label ? el("span", { class: "chip conf", text: "Confidential: holding-level data" }) : null,
      el("button", { class: "btn", text: "Light / dark", onclick: () => { const cur = document.documentElement.getAttribute("data-theme"); const dark = cur ? cur === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; document.documentElement.setAttribute("data-theme", dark ? "light" : "dark"); render(); } }));
    document.getElementById("foot").textContent = "Numbers are engine outputs on the user's fund file and ER strategy returns plus documented assumptions; none is a forecast or a recommendation to trade. Plans are inputs to IC discussion: the IC approves, amends or rejects each change. Built " + D.meta.built + ".";
  }
  function renderTabs() {
    const box = document.getElementById("tabs");
    box.replaceChildren(...TABS.map((t) => el("button", { role: "tab", "aria-selected": String(t === st.tab), class: t === st.tab ? "active" : "", text: TITLE[t], onclick: () => { st.tab = t; history.replaceState(null, "", "#" + t); render(); window.scrollTo({ top: 0 }); } })));
  }
  const VIEWS = { strategy: viewStrategy, balance_sheet: viewBS, liquidity: viewLiquidity, asset_allocation: viewAA, ic: viewIC, yale: viewYale, data: viewData };
  function render() {
    hideTip();
    renderTabs();
    renderFilters();
    for (const t of TABS) document.getElementById("v-" + t).classList.toggle("active", t === st.tab);
    try { VIEWS[st.tab](); } catch (err) { console.error(err); document.getElementById("v-" + st.tab).append(el("div", { class: "callout warn", text: "This view could not render: " + err.message })); }
  }
  renderStamp();
  render();
})();
