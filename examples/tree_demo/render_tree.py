"""Render the worked multi-period tree (results.json) as a terminal outline and an
interactive, self-contained HTML page (design/examples/Tree_Example.html).

All numbers come from results.json, produced by tree_demo.py; nothing is retyped.
SYNTHETIC: illustrative teaching example, not ADIC data.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = HERE / "results.json"
OUT_HTML = ROOT / "design" / "examples" / "Tree_Example.html"

REGIME = {"N": "Normal", "D": "PE drought", "C": "Crisis + oil shock"}
STATE_NAMES = {
    "C": "Cash / Treasury", "L": "Liquid book", "P": "PE book (NAV)", "U": "PE unfunded",
    "Y": "Yield book", "BR": "Revolver drawn", "BN": "NAV loan", "X": "Synthetic exposure",
    "IM": "Initial margin", "NAV": "Total NAV",
}
FLOW_NAMES = {
    "owner_draw": "Owner draw", "pe_distributions": "PE distributions", "pe_calls": "PE capital calls",
    "yield_cash": "Yield-book cash", "cash_interest": "Interest on cash", "margin_returned": "Margin returned",
    "lever_variation_margin": "Variation margin", "revolver_interest_and_fees": "Revolver interest & fees",
    "nav_loan_interest": "NAV-loan interest", "net_cash_flow_ex_returns": "Net cash flow (before decisions)",
}
DECISION_NAMES = {
    "sell_liquid": "Sell liquid assets", "buy_liquid": "Buy liquid assets", "sell_pe_nav": "Sell PE (NAV sold)",
    "pe_sale_cash_proceeds": "PE sale proceeds", "pe_sale_discount_loss": "PE sale discount loss",
    "unfunded_passed_to_buyer": "Unfunded passed to buyer", "nav_loan_change": "NAV loan draw (+) / repay (-)",
    "revolver_change": "Revolver draw (+) / repay (-)", "synthetic_notional": "Synthetic exposure (notional)",
    "synthetic_change": "Synthetic exposure change", "p2s": "Physical-to-synthetic switch",
    "lever_synthetic": "LEVER via synthetic exposure", "synthetic_closed": "Synthetic exposure closed",
    "borrowed_for_purchases": "Borrowed to buy assets", "revolver_lever": "Revolver used to LEVER",
    "nav_loan_lever": "NAV loan used to LEVER", "revolver_refinance": "Revolver used to REFINANCE (cash-out)",
    "nav_loan_refinance": "NAV loan used to REFINANCE (cash-out)", "initial_margin_posted": "Initial margin posted",
    "pace_cut": "PE pacing cut", "new_commitments": "New PE commitments", "cash_target_shortfall": "Below 8% cash target by",
}


def load() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def slim_node(n: dict) -> dict:
    """Keep only what the page shows; drop zero decisions."""
    dec = {k: v for k, v in (n.get("decisions") or {}).items() if isinstance(v, (int, float)) and abs(v) > 5e-4}
    term = n.get("terminal") or {}
    return {
        "id": n["id"], "stage": n["stage"], "regime": n["regime"], "path": n["path"], "parent": n.get("parent"),
        "children": n.get("children") or [], "p": n["probability"], "bp": n.get("branch_probability"),
        "type": n.get("node_type", ""), "labels": n.get("labels") or {}, "cfp": n.get("cfp_stage", ""),
        "red": n.get("red_event_reasons") or [], "open": n.get("opening_state") or {},
        "close": {k: v for k, v in (n.get("closing_state") or {}).items() if k in STATE_NAMES},
        "flows": n.get("exogenous_flows") or {}, "dec": dec,
        "bind": [{"c": b.get("constraint", b.get("row", "")), "v": b.get("shadow_value_node_usd_per_usd")}
                 for b in (n.get("binding_constraints") or [])],
        "lam": (n.get("duals") or {}).get("liquidity_premium_lambda"),
        "pace_be": (n.get("duals") or {}).get("pacing_cut_break_even_cost_per_usd"),
        "term": {k: term.get(k) for k in ("balance_sheet_NAV_reported", "W_tilde", "annualized_return",
                                           "draws_paid_accrued")} if term else {},
    }


def fmt_lab(s: str) -> str:
    return "–" if not s or s == "NONE" else s


def ascii_tree(nodes: list[dict]) -> str:
    by_id = {n["id"]: n for n in nodes}
    lines: list[str] = []

    def dec_line(n: dict) -> str:
        lab = n["labels"]
        lam = n.get("lam")
        lam_s = f"λ {lam * 100:.2f}%" if isinstance(lam, (int, float)) else ""
        return (f"{n['path']:<8} p={n['p']:.3f}  Liquid {fmt_lab(lab.get('liquid_book'))} | PE {fmt_lab(lab.get('pe_book'))}"
                f" | Yield {fmt_lab(lab.get('yield_book'))} | CF {fmt_lab(lab.get('corporate_finance'))} | {lam_s} | {n['cfp']}")

    root = by_id[0]
    lines.append("t0  " + dec_line(root))
    s1 = root["children"]
    for i, c1 in enumerate(s1):
        n1 = by_id[c1]
        last1 = i == len(s1) - 1
        lines.append(("└─ " if last1 else "├─ ") + "t1  " + dec_line(n1))
        for j, c2 in enumerate(n1["children"]):
            n2 = by_id[c2]
            last2 = j == len(n1["children"]) - 1
            pre = "   " if last1 else "│  "
            lines.append(pre + ("└─ " if last2 else "├─ ") + "t2  " + dec_line(n2))
            leaves = []
            for c3 in n2["children"]:
                lf = by_id[c3]
                ar = (lf.get("term") or {}).get("annualized_return")
                red = " RED" if lf["red"] else ""
                leaves.append(f"{lf['regime']} {ar * 100:+.1f}%/yr{red}" if isinstance(ar, (int, float)) else lf["regime"])
            pre2 = pre + ("   " if last2 else "│  ")
            lines.append(pre2 + "   t3 outcomes: " + " · ".join(leaves))
    return "\n".join(lines)


# ----------------------------------------------------------------------------- layout

ROW_H = 32.0          # leaf row height
TOP = 70.0            # space for column headers
COLS = {0: (16, 228), 1: (286, 250), 2: (580, 305), 3: (935, 300)}  # x, width
H_DEC = {0: 104, 1: 104, 2: 90}


def layout(nodes: list[dict]) -> dict[int, tuple[float, float, float, float]]:
    """Leaves stacked; each parent centred on its children. Returns id -> (x, y, w, h)."""
    by_id = {n["id"]: n for n in nodes}
    pos: dict[int, tuple[float, float, float, float]] = {}
    leaves = [n for n in nodes if n["stage"] == 3]
    # order leaves by tree traversal so siblings are adjacent
    order: list[int] = []

    def walk(i: int) -> None:
        n = by_id[i]
        if n["stage"] == 3:
            order.append(i)
        for c in n["children"]:
            walk(c)

    walk(0)
    assert len(order) == len(leaves)
    for k, i in enumerate(order):
        x, w = COLS[3]
        pos[i] = (x, TOP + k * ROW_H + 3, w, ROW_H - 6)
    for stage in (2, 1, 0):
        for n in nodes:
            if n["stage"] != stage:
                continue
            ys = [pos[c][1] + pos[c][3] / 2 for c in n["children"]]
            cy = sum(ys) / len(ys)
            x, w = COLS[stage]
            h = H_DEC[stage]
            pos[n["id"]] = (x, cy - h / 2, w, h)
    return pos


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def svg_for_case(nodes: list[dict], case: str, other: dict[int, dict] | None) -> str:
    pos = layout(nodes)
    by_id = {n["id"]: n for n in nodes}
    parts: list[str] = [f'<g class="case" data-case="{case}">']
    # edges first
    for n in nodes:
        if n["parent"] is None:
            continue
        px, py, pw, ph = pos[n["parent"]]
        x, y, w, h = pos[n["id"]]
        x1, y1 = px + pw, py + ph / 2
        x2, y2 = x, y + h / 2
        mx = (x1 + x2) / 2
        parts.append(f'<path class="edge" d="M{x1:.1f},{y1:.1f} C{mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}"/>')
        bp = n.get("bp")
        if isinstance(bp, (int, float)):
            parts.append(f'<text class="eprob" x="{x2 - 6:.1f}" y="{y2 - 4:.1f}" text-anchor="end">{bp:.2f}</text>')
    for n in nodes:
        x, y, w, h = pos[n["id"]]
        reg = n["regime"]
        changed = False
        if other is not None and n["id"] in other:
            changed = n["labels"] != other[n["id"]]["labels"]
        cls = f"node r{reg}" + (" changed" if changed else "") + (" leaf" if n["stage"] == 3 else "")
        tip = f"{n['path']} · {REGIME.get(reg, reg)} · p={n['p']:.3f}"
        parts.append(f'<g class="{cls}" data-id="{n["id"]}" tabindex="0" role="button" aria-label="{esc(tip)}">')
        parts.append(f'<title>{esc(tip)}</title>')
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="7"/>')
        parts.append(f'<rect class="stripe" x="{x:.1f}" y="{y:.1f}" width="6" height="{h:.1f}" rx="3"/>')
        tx = x + 14
        if n["stage"] == 3:
            ar = n["term"].get("annualized_return") if n["term"] else None
            ar_s = f"{ar * 100:+.1f}% a yr" if isinstance(ar, (int, float)) else ""
            red = "  ⚠ red event" if n["red"] else ""
            parts.append(f'<text class="t1" x="{tx:.1f}" y="{y + h / 2 + 4.5:.1f}">{esc(n["path"])}'
                         f'<tspan class="muted"> p={n["p"]:.3f}</tspan>'
                         f'<tspan class="ret" x="{x + w - 10:.1f}" text-anchor="end">{esc(ar_s)}{esc(red)}</tspan></text>')
        else:
            lab = n["labels"]
            lam = n.get("lam")
            lam_s = f"λ {lam * 100:.2f}%" if isinstance(lam, (int, float)) else "λ n/a"
            title = "TODAY · decide now" if n["stage"] == 0 else n["path"].replace(">", " › ")
            lines = [
                (f'<tspan class="b">{esc(title)}</tspan><tspan class="muted"> p={n["p"]:.3f}</tspan>', "t1"),
                (f'Liquid: <tspan class="act">{esc(fmt_lab(lab.get("liquid_book")))}</tspan>', "t2"),
                (f'PE: <tspan class="act">{esc(fmt_lab(lab.get("pe_book")))}</tspan> · Yield: '
                 f'<tspan class="act">{esc(fmt_lab(lab.get("yield_book")))}</tspan>', "t2"),
                (f'Corp. Finance: <tspan class="act">{esc(fmt_lab(lab.get("corporate_finance")))}</tspan>', "t2"),
                (f'<tspan class="lam">{esc(lam_s)}</tspan> · CFP {esc(n["cfp"])}', "t2"),
            ]
            step = (h - 10) / len(lines)
            for k, (txt, c) in enumerate(lines):
                parts.append(f'<text class="{c}" x="{tx:.1f}" y="{y + 14 + k * step:.1f}">{txt}</text>')
        parts.append("</g>")
    parts.append("</g>")
    return "".join(parts)


def column_headers() -> str:
    heads = {0: "Today (t0)", 1: "Year 1 (t1)", 2: "Year 2 (t2)", 3: "Year 3 (t3): outcomes"}
    subs = {0: "the decision executed now", 1: "contingent plan", 2: "contingent plan", 3: "3-year return a year, incl. draws paid"}
    out = []
    for s, (x, w) in COLS.items():
        out.append(f'<text class="colh" x="{x:.1f}" y="26">{esc(heads[s])}</text>')
        out.append(f'<text class="cols" x="{x:.1f}" y="44">{esc(subs[s])}</text>')
    return "".join(out)


def build_html(d: dict) -> str:
    main_nodes = [slim_node(n) for n in d["nodes"]]
    nr_nodes = [slim_node(n) for n in d["cases"]["no_revolver"]["nodes"]]
    # leaves in the no-revolver case may lack terminal blocks; fall back to compact summaries
    by_main = {n["id"]: n for n in main_nodes}
    by_nr = {n["id"]: n for n in nr_nodes}
    n_leaves = sum(1 for n in main_nodes if n["stage"] == 3)
    height = TOP + n_leaves * ROW_H + 20
    width = COLS[3][0] + COLS[3][1] + 16
    svg = (f'<svg id="tree" viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="Scenario tree">'
           + column_headers() + svg_for_case(main_nodes, "with", by_nr) + svg_for_case(nr_nodes, "without", by_main) + "</svg>")
    s_main = d["summary"]
    s_nr = d["cases"]["no_revolver"].get("summary", {})
    payload = {"with": main_nodes, "without": nr_nodes, "summary": {"with": s_main, "without": s_nr},
               "names": {"state": STATE_NAMES, "flow": FLOW_NAMES, "dec": DECISION_NAMES, "regime": REGIME},
               "meta": {"label": d["meta"].get("label"), "solver": d["meta"].get("solver"),
                        "lp": d["meta"].get("lp_size_main_case")}}
    data_js = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    lp = d["meta"].get("lp_size_main_case") or {}
    return TEMPLATE.replace("{{SVG}}", svg).replace("{{DATA}}", data_js).replace(
        "{{LP}}", esc(f"{lp.get('columns', '?')} variables × {lp.get('rows', '?')} constraints")).replace(
        "{{SOLVER}}", esc(d["meta"].get("solver", "")))


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Multi-Period Tree Example</title>
<style>
:root{--bg:#f7f8fa;--panel:#ffffff;--text:#1d2330;--muted:#5d6676;--line:#c9cfd8;--edge:#9aa3b2;
--n-fill:#e4f0fa;--n:#0072b2;--d-fill:#fdf0d5;--d:#b77900;--c-fill:#fbe2d6;--c:#c4510b;--act:#13306b;--lam:#6a1b9a;--chg:#7b2cbf;--warn:#b00020}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#11151c;--panel:#1a202b;--text:#e7ebf2;--muted:#9aa4b5;--line:#343c4a;--edge:#5d6779;
--n-fill:#10283b;--n:#56b4e9;--d-fill:#33280f;--d:#f0c25a;--c-fill:#3a1e12;--c:#ff9a5c;--act:#cfe0ff;--lam:#d7a7ff;--chg:#c99bff;--warn:#ff8a95}}
:root[data-theme="dark"]{--bg:#11151c;--panel:#1a202b;--text:#e7ebf2;--muted:#9aa4b5;--line:#343c4a;--edge:#5d6779;
--n-fill:#10283b;--n:#56b4e9;--d-fill:#33280f;--d:#f0c25a;--c-fill:#3a1e12;--c:#ff9a5c;--act:#cfe0ff;--lam:#d7a7ff;--chg:#c99bff;--warn:#ff8a95}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 "Segoe UI",system-ui,-apple-system,Arial,sans-serif}
header,main,footer{max-width:1480px;margin:0 auto;padding:0 16px}
h1{font-size:24px;margin:18px 0 4px}.sub{color:var(--muted);margin:0 0 10px}
.badge{display:inline-block;border:1px dashed var(--muted);border-radius:4px;padding:1px 8px;font-size:12px;font-weight:600;letter-spacing:.04em}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:10px 0}
button{font:inherit;border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:6px;padding:5px 12px;cursor:pointer}
button[aria-pressed="true"]{border-color:var(--act);box-shadow:inset 0 0 0 1px var(--act);font-weight:600}
.legend{display:flex;flex-wrap:wrap;gap:14px;color:var(--muted);font-size:13px}
.sw{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-1px;margin-right:5px;border:2px solid}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:14px;align-items:start}
@media (max-width:1100px){.grid{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.treewrap{overflow-x:auto}
svg#tree{width:100%;min-width:900px;height:auto;display:block}
.edge{fill:none;stroke:var(--edge);stroke-width:1.4}.eprob{font-size:11px;fill:var(--muted)}
.colh{font-size:15px;font-weight:700;fill:var(--text)}.cols{font-size:12px;fill:var(--muted)}
.node rect{stroke-width:1.5;cursor:pointer}.node:focus{outline:none}.node:focus rect:first-of-type,.node.sel rect:first-of-type{stroke-width:3}
.rN rect{fill:var(--n-fill);stroke:var(--n)}.rN .stripe{fill:var(--n);stroke:none}
.rD rect{fill:var(--d-fill);stroke:var(--d)}.rD .stripe{fill:var(--d);stroke:none}
.rC rect{fill:var(--c-fill);stroke:var(--c)}.rC .stripe{fill:var(--c);stroke:none}
.node text{fill:var(--text);font-size:12px;pointer-events:none}.node .t1{font-size:12.5px}.b{font-weight:700}
.muted{fill:var(--muted)}.act{font-weight:600;fill:var(--act)}.lam{fill:var(--lam);font-weight:600}.ret{font-weight:600}
.case[data-case="without"]{display:none}
body.nr .case[data-case="with"]{display:none}body.nr .case[data-case="without"]{display:inline}
body.nr .node.changed rect:first-of-type{stroke:var(--chg);stroke-width:3;stroke-dasharray:6 3}
table{border-collapse:collapse;width:100%;font-size:13px}td{padding:2px 4px;border-bottom:1px solid var(--line)}td.v{text-align:right;font-variant-numeric:tabular-nums}
h2{font-size:16px;margin:4px 0 8px}h3{font-size:13px;margin:12px 0 4px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.why{background:var(--bg);border-left:4px solid var(--lam);padding:6px 10px;margin:8px 0;border-radius:4px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px}
.kpi{background:var(--bg);border-radius:8px;padding:8px 10px}.kpi b{display:block;font-size:20px}.kpi span{color:var(--muted);font-size:12px}
ol li,ul li{margin:3px 0}footer{color:var(--muted);font-size:12px;margin:18px auto 30px}
</style></head><body>
<header>
<div class="bar" style="justify-content:space-between"><h1>Multi-Period Tree Example</h1>
<div><span class="badge">SYNTHETIC – NOT ADIC DATA</span> <button id="theme" type="button">Dark theme</button></div></div>
<p class="sub">A small, fully solved version of the optimizer: 3 years × 3 regimes = 40 nodes. One linear program ({{LP}}) decides every node at once.
Solver: {{SOLVER}}. Independently re-solved with a second solver (CLARABEL) with matching results.</p>
<div class="bar">
<span>Case:</span>
<button type="button" id="cWith" aria-pressed="true">Revolver signed</button>
<button type="button" id="cWithout" aria-pressed="false">No revolver</button>
<span class="legend">
<span><i class="sw" style="background:var(--n-fill);border-color:var(--n)"></i>Normal</span>
<span><i class="sw" style="background:var(--d-fill);border-color:var(--d)"></i>PE drought</span>
<span><i class="sw" style="background:var(--c-fill);border-color:var(--c)"></i>Crisis + oil shock</span>
<span>Edge labels = probability of that branch · <b style="color:var(--lam)">λ</b> = liquidity premium (value of $1 of extra cash at that node) · dashed purple outline = decision differs between the two cases</span>
</span></div>
</header>
<main>
<div class="grid">
<div class="card treewrap">{{SVG}}</div>
<aside class="card" id="panel" aria-live="polite"><h2>Click any box</h2>
<p>Each box is a point in the future. The left-most box is the only decision executed today; every other box is the plan if that branch happens. Click a box to see its balance sheet, cash flows, the decisions in $bn, the binding limits and their prices.</p></aside>
</div>
<div class="card" style="margin-top:14px"><h2>Outcomes across the tree (<span id="caseName">revolver signed</span>)</h2><div class="kpis" id="kpis"></div></div>
<div class="card" style="margin-top:14px"><h2>How this works</h2>
<ol>
<li><b>The tree.</b> Start today in a PE drought. Each year the economy moves to Normal, Drought or Crisis with the probabilities on the edges (a crisis comes with an oil shock: the owner draws 10% of NAV, the credit line is only 50% available, and PE sells at a 35% discount).</li>
<li><b>Cash must balance at every box.</b> In: PE distributions, yield-book cash, interest. Out: the owner's draw (always paid in full), PE capital calls, interest on borrowing.</li>
<li><b>At every box the optimizer chooses</b> SELL / HOLD / REFINANCE / LEVER for each book, credit-line use and PE pacing, knowing only the path so far (it never sees which branch comes next).</li>
<li><b>All boxes are decided together</b> by one optimization: maximize the expected risk-averse value of the 3-year outcome, subject to the cash floor, borrowing limits and leverage cap. Same inputs, same answer.</li>
<li><b>Only today's decision is executed.</b> Next quarter the tree is rebuilt from where ADIC actually is and solved again (rolling re-optimization).</li>
<li><b>λ, the liquidity price,</b> is the value of one more dollar of cash at that box. It is what Corporate Finance would charge as its transfer price, and what decides SELL vs HOLD for a fund: sell only if the bid beats the value of holding.</li>
</ol>
<p style="color:var(--muted)">The production design is the same mechanism at larger scale: quarterly steps, about 576 end-states over 8 periods, six model worlds and all eight groups, re-solved every quarter. Probabilities for the IC are then certified on 10,000–50,000 simulated paths. Humans set the limits and approve; no AI produces any number here.</p>
</div>
</main>
<footer>Source: examples/tree_demo/results.json (generated by tree_demo.py; verification in examples/tree_demo/RESULTS.md). SYNTHETIC illustrative example, not ADIC data and not a forecast.</footer>
<script id="data" type="application/json">{{DATA}}</script>
<script>
(function(){
const D=JSON.parse(document.getElementById('data').textContent);
let cur='with';
const byId=c=>Object.fromEntries(D[c].map(n=>[n.id,n]));
let idx={with:byId('with'),without:byId('without')};
const pct=v=>(v==null||isNaN(v))?'n/a':(v*100).toFixed(1)+'%';
const bn=v=>(v==null||isNaN(v))?'':(Math.abs(v)<0.0005?'0.00':v.toFixed(2));
const lab=s=>(!s||s==='NONE')?'–':s;
function rows(obj,names){return Object.entries(obj||{}).filter(([k,v])=>typeof v==='number').map(([k,v])=>`<tr><td>${names[k]||k}</td><td class="v">${bn(v)}</td></tr>`).join('')}
function why(n){
 const L=n.labels||{},p=[];
 const reg=D.names.regime[n.regime]||n.regime;
 const f=n.flows||{};
 if(n.stage===3){const t=n.term||{};return `Outcome after 3 years on the path ${n.path}: ${pct(t.annualized_return)} a year (counting the owner draws paid). No decisions here: debts are settled and limits restored.`}
 if(f.owner_draw!=null)p.push(`${reg}: the owner draws $${bn(-f.owner_draw)}bn; PE pays out $${bn(f.pe_distributions||0)}bn and calls $${bn(-(f.pe_calls||0))}bn.`);
 else p.push(`${reg} today.`);
 const acts=[];
 if(lab(L.liquid_book)!=='–')acts.push(`liquid book ${L.liquid_book}`);
 if(lab(L.pe_book)!=='–')acts.push(`PE ${L.pe_book}`);
 if(lab(L.corporate_finance)!=='–')acts.push(`Corporate Finance ${L.corporate_finance}`);
 p.push('The optimizer chooses: '+acts.join('; ')+'.');
 if(n.bind&&n.bind.length)p.push(`Binding: ${n.bind.map(b=>b.c).join('; ')}.`);
 if(n.lam!=null)p.push(`λ = ${pct(n.lam)}${n.lam>0.01?' (cash is scarce here)':(n.lam>0.002?' (cash carries a modest premium here)':' (cash is plentiful here)')}.`);
 return p.join(' ');
}
function show(id){
 const n=idx[cur][id]; if(!n)return;
 document.querySelectorAll('.node.sel').forEach(e=>e.classList.remove('sel'));
 document.querySelectorAll(`.case[data-case="${cur}"] .node[data-id="${id}"]`).forEach(e=>e.classList.add('sel'));
 const other=idx[cur==='with'?'without':'with'][id];
 const L=n.labels||{};
 let h=`<h2>${n.stage===0?'Today':n.path.replaceAll('>',' › ')}</h2>`;
 h+=`<p><b>${D.names.regime[n.regime]}</b> · probability ${n.p.toFixed(3)} · CFP stage ${n.cfp||'n/a'}${n.red&&n.red.length?' · <b style="color:var(--warn)">red event: '+n.red.join(', ')+'</b>':''}</p>`;
 h+=`<div class="why">${why(n)}</div>`;
 h+=`<h3>Actions</h3><table><tr><td>Liquid book</td><td class="v">${lab(L.liquid_book)}</td></tr><tr><td>PE book</td><td class="v">${lab(L.pe_book)}</td></tr><tr><td>Yield book</td><td class="v">${lab(L.yield_book)}</td></tr><tr><td>Corporate Finance</td><td class="v">${lab(L.corporate_finance)}</td></tr></table>`;
 if(other&&JSON.stringify(other.labels)!==JSON.stringify(n.labels))h+=`<p style="color:var(--chg)"><b>In the ${cur==='with'?'no-revolver':'revolver-signed'} case this box decides differently:</b> liquid ${lab(other.labels.liquid_book)}; PE ${lab(other.labels.pe_book)}; CF ${lab(other.labels.corporate_finance)}.</p>`;
 if(Object.keys(n.dec||{}).length)h+=`<h3>Decisions ($bn)</h3><table>${rows(n.dec,D.names.dec)}</table>`;
 if(n.flows&&Object.keys(n.flows).length)h+=`<h3>Cash flows this year ($bn)</h3><table>${rows(n.flows,D.names.flow)}</table>`;
 h+=`<h3>Balance sheet ($bn): opening</h3><table>${rows(n.open,D.names.state)}</table>`;
 if(n.bind&&n.bind.length)h+=`<h3>Binding limits and their prices</h3><table>${n.bind.map(b=>`<tr><td>${b.c}</td><td class="v">${b.v==null?'':b.v.toFixed(4)+' $/$'}</td></tr>`).join('')}</table>`;
 if(n.lam!=null)h+=`<h3>Liquidity price</h3><p>λ = <b style="color:var(--lam)">${pct(n.lam)}</b>${n.pace_be!=null?` · a PE pacing cut pays only if it costs less than ${(n.pace_be*100).toFixed(1)}¢ per $`:''}</p>`;
 if(n.stage===3&&n.term)h+=`<h3>Outcome</h3><table><tr><td>NAV at year 3</td><td class="v">${bn(n.term.balance_sheet_NAV_reported)}</td></tr><tr><td>Draws paid, accrued</td><td class="v">${bn(n.term.draws_paid_accrued)}</td></tr><tr><td>Return a year</td><td class="v">${pct(n.term.annualized_return)}</td></tr></table>`;
 document.getElementById('panel').innerHTML=h;
}
function kpis(){
 const s=D.summary[cur]||{};
 const k=[['Expected return a year',pct(s.expected_annualized_return)],['Median return a year',pct(s.median_annualized_return)],['P(return ≥ 10% a year)',pct(s.P_annualized_return_ge_10pct)],['P(return < 0)',pct(s.P_annualized_return_lt_0)],['Worst 10% average (CVaR10) a year',pct(s.cvar10_annualized_return)],['P(any PE sale)',pct(s.P_any_pe_sale)],['P(red event)',pct(s.P_red_event)],['P(revolver drawn somewhere)',pct(s.P_revolver_drawn_somewhere)]];
 document.getElementById('kpis').innerHTML=k.map(([a,b])=>`<div class="kpi"><b>${b}</b><span>${a}</span></div>`).join('');
 document.getElementById('caseName').textContent=cur==='with'?'revolver signed':'no revolver';
}
function setCase(c){cur=c;document.body.classList.toggle('nr',c==='without');document.getElementById('cWith').setAttribute('aria-pressed',c==='with');document.getElementById('cWithout').setAttribute('aria-pressed',c==='without');kpis();show(0)}
document.getElementById('cWith').onclick=()=>setCase('with');
document.getElementById('cWithout').onclick=()=>setCase('without');
document.querySelectorAll('.node').forEach(g=>{g.addEventListener('click',()=>show(+g.dataset.id));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show(+g.dataset.id)}})});
const tb=document.getElementById('theme');
function setTheme(t){document.documentElement.setAttribute('data-theme',t);tb.textContent=t==='dark'?'Light theme':'Dark theme';try{localStorage.setItem('treeTheme',t)}catch(e){}}
let saved=null;try{saved=localStorage.getItem('treeTheme')}catch(e){}
if(saved)setTheme(saved);
tb.onclick=()=>setTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':(document.documentElement.getAttribute('data-theme')==='light'?'dark':(matchMedia('(prefers-color-scheme: dark)').matches?'light':'dark')));
kpis();show(0);
})();
</script></body></html>"""


def main() -> None:
    d = load()
    main_nodes = [slim_node(n) for n in d["nodes"]]
    print(ascii_tree(main_nodes))
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(build_html(d), encoding="utf-8")
    print(f"\nwrote {OUT_HTML}", file=sys.stderr)


if __name__ == "__main__":
    main()
