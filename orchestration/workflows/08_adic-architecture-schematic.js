export const meta = {
  name: 'adic-architecture-schematic',
  description: 'Build a verified, offline HTML architectural schematic of the ADIC TPA lab from ARCHITECTURE.md: extract model, generate SVG views, fidelity + visual QA, fix',
  phases: [
    { title: 'Extract', detail: 'three readers turn ARCHITECTURE.md into a structured node/edge model per view' },
    { title: 'Build', detail: 'merge the model and generate the HTML/SVG schematic with a Python generator' },
    { title: 'Verify', detail: 'fidelity check against ARCHITECTURE.md and programmatic visual QA' },
    { title: 'Fix', detail: 'apply findings, regenerate, re-run checks' },
  ],
}

const ROOT = 'C:\\users\\dean\\ai_envs\\adic_tpa_lab'
const PY = ROOT + '\\.venv\\Scripts\\python.exe'
const ARCH = ROOT + '\\design\\ARCHITECTURE.md'
const BRIEF = ROOT + '\\design\\00_DESIGN_BRIEF.md'
const CONTEXT = ROOT + '\\inputs\\00_CONTEXT_AND_PRIOR_WORK.md'
const OUT = ROOT + '\\design\\schematic'
const MODEL = OUT + '\\architecture_model.json'
const GEN = OUT + '\\build_schematic.py'
const HTML = OUT + '\\TPA_Lab_Architecture.html'
const QA = OUT + '\\qa_check.py'

const COMMON = `PROJECT: the ADIC Agentic Total-Portfolio Laboratory. The authoritative design is ${ARCH} (about 245 KB; use Grep to locate sections, then Read the ranges you need). Windows PowerShell 5.1: the cwd resets every call, so use absolute paths; Python is ${PY}.
IMPORTANT CONTEXT: ARCHITECTURE.md was written for SEVEN investment groups. The user has since added an EIGHTH group, Real Assets (real estate, infrastructure, energy and natural resources; funds plus co-investments and direct assets; inside the ~60% private allocation). Its research is in progress; ${BRIEF} section 8 gives the interim design rules (data-driven taxonomy, an interim Real Assets engine, action set, open-end redemption queue, asset-level non-recourse debt, oil wrong-way risk). Show Real Assets wherever groups appear, visibly badged "added 18 Oct; research in progress; interim rules (brief §8)". Do not invent anything else that is not in ARCHITECTURE.md or brief section 8. Every node and edge must carry the ARCHITECTURE.md section it comes from.`

const MODEL_FORMAT = `Write JSON with this shape:
{"views":[{"id":"...","title":"...","subtitle":"...","nodes":[{"id":"snake_id","label":"short label (<= 28 chars)","sublabel":"optional detail (<= 60 chars)","kind":"deterministic|agentic|human|store|external|boundary_note","lane":"the column/row/layer/plane it belongs to","order":0,"owner":"accountable ADIC function if stated","section":"§x.y"}],
 "edges":[{"from":"id","to":"id","label":"short label (<= 30 chars) or empty","kind":"data|control|price|evidence|decision|feedback","section":"§x.y"}],
 "lanes":[{"id":"...","label":"...","kind":"layer|plane|actor_group|phase|boundary","order":0}],
 "notes":["one-line notes shown under the view, each with a section reference"]}]}
Keep labels short and exact; prefer the document's own module names (e.g. core.h, ledger, icm, evaluator, seal).`

const EXTRACTS = [
  { id: 'X1', file: 'extract_X1.json', scope: `View "overview": the layered system (ARCHITECTURE §0.3, §2.1-2.4, §3.1-3.4, §11.1-11.4): layers L0 Contracts to L10 Room with their modules; the human plane; the deterministic / agentic / human boundary (§3.3); trust boundaries and external systems (§2.2-2.4: data sources, LLM providers, MCP server, CLI); downward-only dependencies; the seal service and evaluator processes; owners of modules (§3.4).` },
  { id: 'X2', file: 'extract_X2.json', scope: `Two views. (a) "engines": the deterministic engine data flow (§3.2 mermaid, §4.1-4.13, §5.1-5.10): scen/state/owner -> priv/pub/overlay/actions with beliefs -> the ONE ledger kernel used three ways (P simulator on 10k-50k paths; H here-and-now program with Phase I/II and duals; T4-prime stress replica) -> icm (lambda, FTP, envelopes), actions (cards, Gamma, Level-B selection), certify (CP bounds), module F, robust, attrib, bridge -> evidence for the pack. Include the Phase I / recovery logic and the pinned-dual CI test as annotations. (b) "capital_market": the organization and internal capital market (§2.1 actors, §4.3 owner, §4.9-4.10 ledger and Corporate Finance funding, §6.1-6.9, §8.1 decision rights): the sovereign owner (draw demand, mandate modes), Corporate Finance as internal bank (liquidity buffer, facilities, collateral VM/IM, distributions, FTP curve publication), the eight investment groups (PE funds, Secondaries, Capital Solutions, Co-investment, Public Markets, Private Credit, Overlay, Real Assets - badged as above) with their flows: proposals and forecasts up, envelopes and FTP charges down, in-house pricing desks (Secondaries for SELL, Capital Solutions for REFINANCE) with conflict controls, netting of internal transfers, services transfer pricing (Overlay); the IC, CIO, CRO, MRM and their decision rights.` },
  { id: 'X3', file: 'extract_X3.json', scope: `Three views. (a) "lab": the agentic laboratory and trust boundaries (§7.1-7.13, §10.1-10.6): meta-controller FSM states and transitions (§7.4), LLM roles and their tools (§7.3), evaluator search/final instances, seal service with commit-reveal seeds, registry, planes (§7.5), gates G0-G9 and failure taxonomy (§7.6), budgets, memory as search heuristic, escalation and assumption log, cross-family review, claims renderer and validator, integrity drills, Stub/Replay LLM backends. (b) "room": the decision room and IC flow (§8.1-8.11): Decision Register, evidence compiler, briefs rendered from placeholders, pack L0/L1/L2 and console, computed shadow-IC seats (implied_actions; opposing utilities inside the admissible set Theta), human blind pre-vote, meeting, ballots, DecisionRecords, decision log, signposts and commitment plans, Q&A / what-ifs / view conditioning, archetypes A/B/C, politics rules. (c) "cycle": the quarterly cycle timeline (§3.6 table: T-28 ... T+5 and monthly), each step with what it produces and its gate.` },
]

const EX_SCHEMA = {
  type: 'object',
  properties: { path: { type: 'string' }, views: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, nodes: { type: 'integer' }, edges: { type: 'integer' } }, required: ['id', 'nodes', 'edges'] } }, notes: { type: 'string' } },
  required: ['path', 'views'],
}
const BUILD_SCHEMA = {
  type: 'object',
  properties: { html_path: { type: 'string' }, model_path: { type: 'string' }, generator_path: { type: 'string' }, views: { type: 'array', items: { type: 'string' } }, self_check: { type: 'string' } },
  required: ['html_path', 'model_path', 'generator_path', 'views', 'self_check'],
}
const ISSUE_SCHEMA = {
  type: 'object',
  properties: {
    report_path: { type: 'string' },
    issues: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] }, view: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'view', 'issue', 'fix'] } },
    verdict: { type: 'string' },
  },
  required: ['report_path', 'issues', 'verdict'],
}
const FIX_SCHEMA = {
  type: 'object',
  properties: { html_path: { type: 'string' }, fixed: { type: 'integer' }, not_fixed: { type: 'array', items: { type: 'string' } }, qa_clean: { type: 'boolean' }, summary: { type: 'string' } },
  required: ['html_path', 'fixed', 'not_fixed', 'qa_clean', 'summary'],
}

// ---------------- Extract ----------------
phase('Extract')
const ex = await parallel(EXTRACTS.map(x => () => agent(`${COMMON}

TASK: read the relevant parts of ARCHITECTURE.md and extract a precise structured model for the schematic.
SCOPE: ${x.scope}
${MODEL_FORMAT}
Aim for completeness at the level a CIO, CRO or engineer would expect on an architecture schematic: every module, store, actor and boundary the document names in this scope, but no invented components. 15-45 nodes per view is typical.
OUTPUT: write the JSON to ${OUT}\\${x.file} (create the folder if needed) and validate it parses with ${PY}. Return the structured summary.`, { label: `extract:${x.id}`, phase: 'Extract', schema: EX_SCHEMA })))
const exOk = ex.filter(Boolean)
log(`Extracted ${exOk.length}/3 models: ` + exOk.map(e => e.views.map(v => `${v.id}(${v.nodes}n/${v.edges}e)`).join(' ')).join(' '))

// ---------------- Build ----------------
phase('Build')
const build = await agent(`${COMMON}

TASK: build the architectural schematic as ONE self-contained, offline HTML file.
INPUTS: the extracted models ${exOk.map(e => e.path).join(', ')} (merge them into ${MODEL}; resolve conflicts by checking ARCHITECTURE.md).
APPROACH (required, so later fixes are easy): write a Python generator ${GEN} that reads ${MODEL}, computes a deterministic layout (lanes as rows or columns, nodes placed on a grid by lane and order, orthogonal or gently curved edges routed between lanes with arrowheads, labels sized to fit), and writes inline SVG for every view into ${HTML}. Run it with ${PY}. No external scripts, fonts or images: everything inline, viewable offline.
VIEWS (tabs at the top, keyboard-accessible; one SVG per view):
1. Overview - layered system L0-L10 with modules, the human plane on top, evaluator/seal boundary, deterministic / agentic / human colouring, trust boundaries and external systems.
2. Engines - one ledger kernel used three ways (P, H, T4-prime) with the upstream world and asset engines and downstream prices, cards, certification, module F.
3. Capital market - owner, Corporate Finance as internal bank, the eight groups (Real Assets badged), IC/CIO/CRO/MRM, with flows (proposals and forecasts, envelopes and FTP, desks, netting, services).
4. Laboratory - meta-controller states, roles, evaluator instances, seal, registry, planes, gates, claims validator, trust boundaries.
5. Decision room - Register to pack to shadow IC to human vote to decision log and signposts, with Q&A and view conditioning.
6. Quarterly cycle - a timeline from T-28 to T+5 plus the monthly loop, with gates.
Each view: a title, a one-line subtitle, a legend (node kinds and edge kinds), short notes with section references, and hover tooltips (SVG <title>) on every node and edge giving the sublabel, owner and ARCHITECTURE section. Add a header with the document title "TPA Lab Architecture", the source ("design/ARCHITECTURE.md, pre-critique version, 18 Oct 2026") and a line noting Real Assets is being integrated.
DESIGN: define colours as CSS custom properties on :root, redefine them for dark mode under @media (prefers-color-scheme: dark) guarded by :root:not([data-theme="light"]) and again under :root[data-theme="dark"]; give body an explicit background; a theme toggle button; system font stack; 16px side gutters; the SVG scales to the container width (viewBox) and the container scrolls horizontally inside itself on narrow screens rather than the page; readable at 100% zoom on a 1440px laptop screen (text >= 11px rendered). Distinct, colour-blind-safe hues for deterministic (engines own numbers), agentic (LLM roles), human (decides), stores and external systems; edge kinds by colour and dash pattern. Avoid overlapping boxes and text overflow: compute text widths conservatively (about 0.6 x font-size per character) and size boxes or wrap text accordingly.
Self-check before returning: run the generator, confirm the HTML exists, contains six SVGs, and has no external URLs. Return the structured summary.`, { label: 'build', phase: 'Build', schema: BUILD_SCHEMA })
if (!build) { log('Build failed; stopping.'); return { extracts: exOk } }

// ---------------- Verify ----------------
phase('Verify')
const [fid, vis] = await parallel([
  () => agent(`${COMMON}

TASK: FIDELITY review of the schematic against ARCHITECTURE.md. Read ${MODEL} (and skim ${HTML}). For every view: check each node, edge, label, owner and section reference against ARCHITECTURE.md; list wrong or invented components, wrong directions or relationships, important components or flows that are missing (judge importance by how prominently the document treats them, e.g. §0.3's ten rules, §3.2, §3.3, §3.6, §6, §7.4, §8), and Real Assets labelling problems. Be specific (node or edge id, what is wrong, the correct content with section).
Write ${OUT}\\review_fidelity.md and return the structured issues.`, { label: 'verify:fidelity', phase: 'Verify', schema: ISSUE_SCHEMA }),
  () => agent(`${COMMON}

TASK: VISUAL QA of ${HTML} (generated by ${GEN} from ${MODEL}). Write a Python checker ${QA} (stdlib only: xml.etree / html.parser / re) that, for each SVG view: finds node rectangles and their text; flags overlapping rectangles; flags text whose estimated width (0.6 x font-size per character, or 0.55 for narrow fonts) exceeds its box minus padding; flags text below 11px effective size at the viewBox's intended width (assume a 1400px-wide container); flags edges whose endpoints do not touch a node; checks every node and edge has a <title> tooltip; computes WCAG contrast ratios of node text versus node fill for BOTH the light and dark token sets declared in the CSS (flag < 4.5:1); confirms no external URLs (http/https/src/href to remote) and that :root tokens, the dark-mode media query, the data-theme overrides and an explicit body background are present. Run it with ${PY}, then also read the SVG to judge overall legibility and layout (crowding, crossing edges, lanes in a sensible order).
Write ${OUT}\\review_visual.md (checker output plus your judgement) and return the structured issues.`, { label: 'verify:visual', phase: 'Verify', schema: ISSUE_SCHEMA }),
])
const issues = [...((fid && fid.issues) || []), ...((vis && vis.issues) || [])]
log(`Review found ${issues.length} issues: high ${issues.filter(i => i.severity === 'high').length}, medium ${issues.filter(i => i.severity === 'medium').length}, low ${issues.filter(i => i.severity === 'low').length}.`)

// ---------------- Fix ----------------
phase('Fix')
const fix = await agent(`${COMMON}

TASK: fix the schematic. Read ${OUT}\\review_fidelity.md and ${OUT}\\review_visual.md. Apply every high and medium issue and the low ones that are cheap: correct the model ${MODEL} for content issues and the generator ${GEN} for layout, styling and accessibility issues; regenerate ${HTML} with ${PY}; then run the QA checker ${QA} and iterate (at most 4 rounds) until it reports no overlaps, no text overflow, no missing tooltips, no contrast failures and no external URLs. Keep the six views. Return the structured summary (qa_clean = whether the final checker run was clean).`, { label: 'fix', phase: 'Fix', schema: FIX_SCHEMA })

return { extracts: exOk, build, fidelity: fid ? { verdict: fid.verdict, n: fid.issues.length } : null, visual: vis ? { verdict: vis.verdict, n: vis.issues.length } : null, fix }
