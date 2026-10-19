# Visual QA: TPA Lab Architecture schematic

Reviewed 18 Oct 2026. Subject: `design/schematic/TPA_Lab_Architecture.html` (built 18 Oct 19:58 by `build_schematic.py` from `architecture_model.json`). Checker: `design/schematic/qa_check.py`. No project file other than these two was changed.

## Verdict

**Mechanically clean; hard to read.** The page passes every required check in all six views and in both themes:

- No boxes, labels or captions overlap, and nothing is clipped.
- All 2,206 texts drawn inside boxes fit. Three methods agree: the 0.6 x font-size estimate, the installed Segoe UI metrics, and widths measured in headless Edge.
- The smallest text is 11.32px in a 1400px container.
- 1,019 of 1,022 edge endpoints touch their node, or the node's axis tick in the timeline.
- All 325 nodes, 511 edges and 484 edge labels have a `<title>` tooltip that names a section.
- All 10 Real Assets nodes show the full badge.
- All text contrast is at least 5.81:1 in the light theme and 7.65:1 in the dark theme.
- The page scaffolding is complete: tokens, the dark media query, the data-theme overrides, an explicit body background, and no remote URLs.

The problems are legibility and layout, not defects:

- The four detail views are dense webs, with 540 to 913 edge crossings each (5 to 10 per edge).
- Every view except the cycle is 3 to 4 screens tall.
- Lines pass under 484 opaque label tags, and lane captions cut 181 gaps into lines.
- Half of the overview's width sits mostly empty.

The Quarterly cycle is the only view that reads at a glance. Ten issues follow below: one high, five medium and four low.

## How it was checked

- **Checker.** `qa_check.py` uses the standard library only (`re`, `html.parser`, `xml.etree`, `struct`; `subprocess` only for the optional browser run). Run it with `.venv\Scripts\python.exe design\schematic\qa_check.py --browser auto`; exit 0 means no errors.
  - It parses each inline SVG and resolves the CSS cascade with both token sets.
  - It runs the required checks: overlaps, text fit, effective size, endpoints, tooltips, WCAG contrast in light and dark, remote references, and theme scaffolding.
  - It also measures layout: crossings, bends, lines hidden under labels or captions, port crowding, lane order and flow direction.
- **Width calibration.** Over all 2,214 texts, the Segoe UI font-file widths and Edge's `getComputedTextLength()` agree to a median of 0.008px (95th percentile 0.45px). Edge renders weights 650 and 750 as Segoe UI Bold, so the checker's use of Black for 750 is conservative.
- **Mutation test.** Ten defects were planted in a scratch copy:
  - an overlapping box;
  - an overflowing sublabel;
  - a 9.5px font;
  - an edge start moved 12px off its box;
  - a missing tooltip;
  - low dark-theme contrast;
  - a remote stylesheet;
  - no body background;
  - a trust-boundary box cutting a node;
  - wrong badge text.

  The checker caught all ten, with exit 1 each time.
- **Visual review.** Full-page headless Edge screenshots of all six tabs at 1440px, read tile by tile in light, plus dark for Overview and Cycle.

## Checker results (summary)

| View | viewBox | Nodes / edges / labels | Required checks | Smallest text | Crossings (per edge) | Warnings |
|---|---|---|---|---|---|---|
| Overview | 1360 x 3545 | 66 / 89 / 84 | all pass | 11.32px | 304 (3.4) | 21 lines cut by captions |
| Engines | 1360 x 2544.5 | 45 / 104 / 99 | all pass | 11.32px | 565 (5.4) | 13 lines cut by captions |
| Capital market | 1360 x 2497 | 45 / 94 / 91 | all pass | 11.32px | 913 (9.7) | 35 lines cut by captions |
| Laboratory | 1360 x 2932.5 | 84 / 105 / 97 | all pass | 11.32px | 540 (5.1) | 82 lines cut by captions |
| Decision room | 1360 x 2610 | 65 / 93 / 88 | all pass | 11.32px | 603 (6.5) | 30 lines cut by captions |
| Quarterly cycle | 1360 x 673 | 20 / 26 / 25 | all pass | 11.32px | 17 (0.7) | 3 arcs stop 5.5px short of an axis dot |

Lowest contrast across all views:

| Element | Light | Dark | What sets the minimum |
|---|---|---|---|
| Node text | 6.97:1 | 8.05:1 | sublabel (`sv-ns`) |
| Edge labels | 5.85:1 | 7.78:1 | guard label |
| Captions | 5.81:1 | 7.65:1 | trust-boundary caption |
| Edge strokes vs the page (graphics need 3:1) | 3.07:1 | 4.60:1 | guard stroke |

Real Assets: 10 badged nodes appear wherever groups or group machinery appear:
- Overview: head, engine, group taxonomy.
- Engines: engine.
- Capital market: the group.
- Laboratory: engine.
- Decision room: head, mandate seat, agenda block.
- Cycle: filings.

All 26 Real Assets edges carry the halo, and their tooltips carry the badge text.

## Judgement

### Overall legibility, view by view

- **Overview.** Reads top-down as a layer cake, and the boxes and labels are crisp. The centre is a lattice, though.
  - The channel between L10 and L9 is about 200px of stacked labelled tracks crossed by dashed verticals.
  - Bundles of four to six similar dashed lines run 6px apart through the centre gutters.
  - The view is 4.1 screens tall (a 4,786px page).
- **Engines.** The densest view. The channel between the two L6 sub-rows holds about 12 labelled tracks with dozens of verticals crossing them. With five dash patterns layered this densely, edge kinds stop being distinguishable, and the grey dotted guard lines nearly vanish.
- **Capital market.** The most crossings (913). Ten arrowheads land on the top of "All group heads (generic)" about 12px apart, and long orange price lines snake across lanes. The Real Assets group and its five haloed links are clear.
- **Laboratory.** The meta-controller FSM is laid out as a sensible serpentine, but every transition is a U-turn (see V8), and long unrelated lines cross the FSM lane in three gutters. Long lane captions span several columns, so this view has the most lines cut by captions (82).
- **Decision room.** Follows the IC process from top to bottom. The meeting steps H0 to H6 are drawn as U-turns. The Real Assets head → forecast registry halo forms a yellow spine down the middle.
- **Quarterly cycle.** Good: a clean timeline with gate chips on the axis, phase brackets, short labels and off-cycle arcs below. The only mechanical flaw in the whole page is here: three arcs stop 5.5px short of the dot they point at.

### Crowding and crossings

Crossings come mostly from mixing edge kinds on one canvas. Counted on the current geometry with only one kind shown:

| View | Crossings, all kinds | One kind at a time |
|---|---|---|
| Overview | 304 | data 108, control 24, every other kind 4 or fewer |
| Engines | 565 | data 186, evidence 25, control 14 |
| Capital market | 913 | decision 107, control 44, data 33, price 25 |
| Laboratory | 540 | data 136, control 82 |
| Decision room | 603 | data 205, control 53 |

Per-kind toggles in the legend are therefore the cheapest large improvement.

The builder keeps each lane's model order. Reordering nodes within each lane by the barycentre of their neighbours was tried in memory with `Grid`; no file was written:

| View | Crossings now | After reordering |
|---|---|---|
| Overview | 304 | 250 (18% fewer) |
| Engines | 565 | 545 (4% fewer) |
| Capital market | 913 | 724 (21% fewer; 240px shorter) |
| Laboratory | 540 | 482 (11% fewer) |
| Decision room | 603 | 603 (no change) |

Useful, but not sufficient on its own: 89 to 105 labelled edges per view is intrinsically dense.

Other measures:
- 25 to 37 edges per detail view are longer than 1,000px.
- 14 to 33 edges per view span four or more rows.
- Opaque label tags hide 2,500 to 5,000px of other lines per view, in 185 to 372 places. A line that disappears under a tag reads as ending at that label.

### Lines cut by captions

Lane and trust-boundary captions are drawn after the edges, on an opaque background. Where a port stub or gutter line passes through a caption, the line shows a 14px gap. A zoom on the Engines "L0–L1 Contracts & data" caption confirms it: seven lines leaving "data: bitemporal store" break at the caption and reappear above it. Totals: Overview 21, Engines 13, Capital market 35, Laboratory 82, Decision room 30.

### Lane order

Sensible in every view:
- **Overview:** the canonical stack, from humans through L10 to L0, then external data, with the rule cards last.
- **Engines:** mirrors the overview stack.
- **Capital market:** governance → internal bank → TPA desk → intake and counterparties → groups → rules.
- **Laboratory:** governance → stores → FSM → lab process → agents → backends → evaluator → seal → planes.
- **Decision room:** the IC process in order.
- **Cycle:** time order.

Flow direction fits the stated convention. In Engines, data flows mostly upward (54 up, 20 down). In Decision room, flow is mostly downward (40 down, 20 up), following the meeting. The other views are mixed.

Two placements cost long, faint lines:
- **Engines.** "Guards & annotations" sits in the bottom row, but its guard links target L6 and L8. Edges e98, e99 and e100 are three of the five most-crossed edges, with 31 to 34 crossings each.
- **Capital market.** "Rules & controls" sits at the bottom, so e92 (rule → Treasurer) and e91 (rule → IC/TPC) cross 59 and 46 lines.

Both use the faintest stroke on the page: 1.1px dotted, at 3.07:1 in light.

### Space

- **Uniform row heights.** Every box takes the height of the tallest box in its row. Overview boxes are 136px wide and 86 to 186px tall, with 5.1 text lines on average. 10 of the 66 overview nodes are less than half full.
- **The badge sets row heights.** The five-line Real Assets badge sets the height of its whole row: 171px in the human plane, and likewise in L3 Assets and L0 Contracts. The other boxes in those rows are 40 to 60% empty.
- **Unused columns.** In the overview's 8-column grid, columns 2 to 4 carry nodes in 13 to 16 of the 16 rows. Columns 0, 1, 6 and 7 carry nodes in only 3, 5, 4 and 1 rows.
- **Horizontal scrolling.** The 1360px `min-width` keeps every text at 11px or larger. The cost is horizontal scrolling below about 1394px of CSS width, which is common on Windows laptops at 125 to 150% scaling. This trade-off is deliberate and acceptable.

### Real Assets presentation

The badge requirement is met everywhere, and the header banner and legend explain it. The yellow halo on Real Assets links has two costs in the light theme:
- At 7px wide and 0.55 opacity, it is wider than the 6px gutter-track pitch, so a haloed line visually swallows the lines next to it.
- Long Real Assets links become the boldest marks on the page, for content that is explicitly interim.

In the dark theme the halo (0.28 opacity) is appropriately quiet.

### Themes and page

All scaffolding is present, and the dark theme renders correctly: node text is crisp and the badge is legible as an olive strip with light text. Lane bands are subtle in both themes (about 1.07 to 1.09:1 against the page), so lanes are told apart by their captions and 3px accent bars. That is fine for background grouping. Tooltips are the only place owners and sections appear, and they work with a mouse only (V10).

### Limits

- Crossing counts are intersections of orthogonal segments. They measure clutter, not correctness.
- Node-outline contrast is computed for every node kind against every band kind in a view, as a worst case.
- The font-file method ignores kerning; it is calibrated against the browser above.
- Content correctness (which section an element cites, and whether it exists in ARCHITECTURE.md) is outside this visual review. One spot check: the hard-coded monthly loop in the cycle view cites §3.6 and §8.9, and ARCHITECTURE.md §3.6 has the matching "Monthly" row.

## Issues

| ID | Severity | View | Issue | Fix |
|---|---|---|---|---|
| V1 | high | engines, capital_market, lab, room (overview less so) | Too dense to read without hovering: 540–913 crossings per view (5–10 per edge), 89–105 labelled edges, and 25–37 edges over 1,000px. The overview has 304 crossings, packed into the centre gutters. | Add show/hide toggles per edge kind to each legend, applied to `.sv-edge.sv-e-<kind>` and to its label group (add the kind class to `.sv-elg`). With one kind shown at a time, the current geometry leaves 0–205 crossings (Capital market: 107/44/33/25 instead of 913). Then order nodes within each lane by the barycentre of their neighbours (measured: overview 304→250, capital market 913→724 and 240px shorter, lab 540→482). Consider splitting Engines and Capital market into two views each. |
| V2 | medium | overview, engines, capital_market, lab, room | Lane and trust-boundary captions are drawn over edges on an opaque background, cutting 181 gaps of 14px into lines (21 / 13 / 35 / 82 / 30). Lines look broken or seem to end at the caption. | Move lane captions out of the line field, into a reserved left margin outside the column grid. Place trust-boundary captions where no port stub or gutter track passes. Fallback: draw `sv-captions` before `sv-edges` and drop the opaque `sv-capbg`, keeping the text halo. |
| V3 | medium | overview, engines, capital_market, lab, room | Opaque label tags (fill-opacity 0.94) hide crossing lines in 185–372 places per view, 2,500–5,000px of line in all. A line vanishing under a tag reads as ending at that label, and with 84–99 labels per view, attributing labels to lines is hard. | Replace the tag box with a roughly 3px `--bg` text halo (`paint-order: stroke`) so crossing lines stay visible around the text. Shorten long labels and move secondary detail into tooltips. V1's toggles also reduce the problem. |
| V4 | medium | overview, engines, capital_market, lab, room | Uniform row heights make each view 3–4 screens tall. Every box takes its row's tallest height: overview boxes are 136px wide and 86–186px tall, and 10 of 66 are under half full. The five-line Real Assets badge sets whole-row heights (human plane 171px, L3, L0), leaving the other boxes 40–60% empty. | Let boxes take their natural height and align their tops (the channel already starts below the tallest box). Widen columns where possible; for the overview, try 6 columns of about 185px so labels wrap less. Keep the full badge text, but let only the badged box grow. |
| V5 | medium | overview | Nodes bunch into the middle columns. Columns 2–4 hold nodes in 13–16 of 16 rows; columns 0, 1, 6 and 7 in only 3, 5, 4 and 1. Half the width is mostly empty while 4–6 parallel dashed lines, 6px apart, crowd the centre gutters. | In `Grid._assign_columns`, raise the even-spread weight from 0.25 to about 0.6, or cap how far a node may move from its even slot. Add a congestion term that spreads gutter tracks across gutters. |
| V6 | medium | engines, capital_market | Guard and rule lanes sit at the bottom, so their links are the longest, faintest and most-crossed lines. Engines: e98, e99, e100 (31–34 crossings each). Capital market: e92 (59) and e91 (46). Guard strokes are 1.1px dotted at 3.07:1 in light. | Place these lanes next to the lanes they govern (Engines: beside L6/L8; Capital market: near the internal bank and governance), or replace each guard link with a numbered marker on the target node. Thicken guard strokes to 1.4px and darken `--e-guard` to about #6b7480 (4.7:1). |
| V7 | low | overview, engines, capital_market, lab, room, cycle | The light-theme Real Assets halo (7px, rgba(240,228,66,0.55)) is wider than the 6px track pitch, so it swallows neighbouring lines. Long Real Assets links become the boldest marks on the page, for content marked interim. | Narrow the halo to 4–5px and about 0.35 opacity (or use a thin yellow casing). Keep the badge strip as the main Real Assets cue. |
| V8 | low | lab, room | Sequences within a lane are drawn as U-turns: each FSM transition, and each H0→H6 step, leaves the bottom of one box and re-enters the next from below. The serpentine wrap from IDEATION to SCREENING is unmarked, and through-lines cross the FSM lane. | Route same-row sequence edges as short horizontal arrows between side ports, mark the serpentine wrap, and route through-traffic around the FSM lane. |
| V9 | low | cycle | Three arcs stop 5.5px short of their axis dot: e20 (start, at c_monthly), e21 (to c_t10) and e24 (to c_t7). Upper-step anchors sit at axis + 10px, which only meets 18px gate chips. | In `Timeline._anchor`, use axis_y + tick half-height + 1: 10 for chips, 5.5 for dots and checks, 7 for the IC dot. |
| V10 | low | overview, engines, capital_market, lab, room, cycle | Owners and ARCHITECTURE.md sections appear only in tooltips, which work with a mouse only. Nodes and edges are not focusable, so keyboard and touch users cannot reach them. | Add `tabindex="0"` and a focus ring to node groups, and show the tooltip text in a details panel on focus or tap (via `aria-describedby`). |

## Appendix: checker output

Command: `.venv\Scripts\python.exe design\schematic\qa_check.py --browser auto`. Exit code 0: no errors, 184 warnings.

```text
TPA Lab schematic - visual QA checker
file      C:\Users\dean\ai_envs\adic_tpa_lab\design\schematic\TPA_Lab_Architecture.html (762,342 chars)
container 1400px; estimate 0.6 x font-size per character (0.55 for narrow families); minimum 11px; contrast 4.5:1 text, 3.0:1 graphics
fonts     Segoe UI files: segoeui.ttf, segoeuib.ttf, segoeuii.ttf, segoeuil.ttf, segoeuisl.ttf, segoeuiz.ttf, seguibl.ttf, seguibli.ttf, seguili.ttf, seguisb.ttf, seguisbi.ttf, seguisli.ttf
browser   measured in msedge.exe (headless)

== Page ==
  [PASS] no external URLs or remote references (11 patterns; 0 hits)
  [PASS] :root declares light tokens (54 custom properties)
  [PASS] @media (prefers-color-scheme: dark) redefines tokens (53)
  [PASS] dark media query is guarded by :root:not([data-theme="light"])
  [PASS] :root[data-theme="dark"] override present (53 tokens)
  [PASS] media-query dark tokens equal the data-theme dark tokens
  [PASS] every light token has a dark value (light-only: none)
  [PASS] explicit body background ('var(--bg)'; light #ffffff, dark #0f141a)
  [PASS] every var() reference is defined in both themes (55 names; undefined: none)
  [PASS] no CSS font-size below 11px (found: none)
  [PASS] page <title> is a 2-4 word name ('TPA Lab Architecture')
  [PASS] viewport meta present

== Views (6 inline SVGs) ==
  view                  viewBox  scale nodes edges labels min px cross ERROR  WARN  parser
  overview          1360 x 3545  1.029    66    89     84  11.32   304     0    21  xml.etree
  engines         1360 x 2544.5  1.029    45   104     99  11.32   565     0    13  xml.etree
  capital_market    1360 x 2497  1.029    45    94     91  11.32   913     0    35  xml.etree
  lab             1360 x 2932.5  1.029    84   105     97  11.32   540     0    82  xml.etree
  room              1360 x 2610  1.029    65    93     88  11.32   603     0    30  xml.etree
  cycle              1360 x 673  1.029    20    26     25  11.32    17     0     3  xml.etree

== View: overview - Layered architecture overview ==
  required checks:
    overlapping rectangles                   PASS
    outlines cutting nodes                   PASS
    clipped by the viewBox                   PASS
    text fit, 0.6 x font-size rule           PASS
    effective size >= 11px                   PASS
    edge endpoints touch nodes               PASS
    edges never cross a box                  PASS
    <title> on nodes/edges/labels            PASS
    Real Assets badge shown                  PASS
    WCAG contrast (light + dark)             PASS
  extra checks:
    text fit, installed Segoe UI metrics     PASS
    text fit, headless browser               PASS
    arrowheads not stacked                   PASS
    no shared line tracks                    PASS
    lines clear of box sides                 PASS
    bends not hidden by labels               PASS
    lines not hidden by captions             0 error(s), 21 warning(s)
    labels sit on their line                 PASS
  findings:
    WARN edge-under-caption (21)
      - edge overview-e2: 14px of line hidden under caption 'tpa lab run: TB3 sole egress'
      - edge overview-e4: 14px of line hidden under caption 'Interfaces: cli · mcp_server (§3.4, §11.'
      - edge overview-e4: 14px of line hidden under caption 'tpa lab run: TB3 sole egress'
      - edge overview-e5: 14px of line hidden under caption 'tpa lab run: TB3 sole egress'
      - edge overview-e6: 14px of line hidden under caption 'Interfaces: cli · mcp_server (§3.4, §11.'
      - edge overview-e7: 14px of line hidden under caption 'tpa lab run: TB3 sole egress'
      - edge overview-e8: 14px of line hidden under caption 'External: LLM providers (§2.3)'
      - edge overview-e8: 14px of line hidden under caption 'ADIC machine: TB1 data perimeter'
      - edge overview-e13: 14px of line hidden under caption 'tpa lab run: TB3 sole egress'
      - edge overview-e13: 14px of line hidden under caption 'TB8 truth seal'
      - edge overview-e14: 14px of line hidden under caption 'Interfaces: cli · mcp_server (§3.4, §11.'
      - edge overview-e16: 14px of line hidden under caption 'Interfaces: cli · mcp_server (§3.4, §11.'
      ... and 9 more
  contrast (lowest ratio per group and theme; --verbose lists every combination):
    dark  caption                sv-gl on sv-cb-layer                 7.65:1  #f19292 on #151b22
    light caption                sv-gl on sv-cb-layer                 5.81:1  #b03030 on #f3f5f8
    dark  edge label             sv-t-price                           9.03:1  #f9a066 on #0f141a
    light edge label             sv-t-price                           6.06:1  #a84300 on #ffffff
    dark  edge stroke vs page    price                                6.74:1  #f07c3a on #0f141a
    light edge stroke vs page    evidence                             3.42:1  #009e73 on #ffffff
    dark  node outline vs band   external on sv-b-actor_group         6.94:1  #9aa5b4 on #171b1f
    light node outline vs band   agentic on sv-b-plane                3.80:1  #b36800 on #f6eff7
    dark  node text              sv-ns on store                       8.05:1  #b7c0cb on #0c2d25
    light node text              sv-ns on human                       6.97:1  #465160 on #f8ebf3
  layout metrics:
    viewBox                      1360 x 3545
    render_width                 1400.0
    scale                        1.03
    screens_tall                 4.1
    nodes                        66
    edges                        89
    labels                       84
    node_rows                    16
    node_w                       (136, 136)
    node_h                       (86, 186)
    node_fill_median             0.76
    nodes_under_half_full        10
    text_lines_per_node_mean     5.1
    text_lines_per_node_max      7
    min_effective_px             11.32
    crossings                    304
    crossings_per_edge           3.42
    most_crossed                 [('overview-e13', 28), ('overview-e53', 28), ('overview-e11', 26), ('overview-e83', 26), ('overview-e55', 25)]
    bends_mean                   2.96
    bends_max                    4
    edge_len_mean                596
    edge_len_max                 2488
    edges_over_1000px            11
    label_hides_line_pairs       185
    line_px_hidden_under_labels  2498
    bends_hidden_under_labels    0
    labels_detached              0
    shared_tracks                0
    edge_through_node            0
    edge_grazes_node             0
    port_crowding                0
    endpoint_stats               {'box': 178}
    flow                         {'same row': 22, 'down': 29, 'up': 38}
    row_span_mean                2
    edges_spanning_4plus_rows    14
    worst_into_padding           {'text-fit': -0.9, 'text-fit/segoe-ui': -2.0, 'text-fit/browser': -2.0}
    ra_nodes                     ['group_taxonomy', 'ra_engine', 'ra_head']
    ra_edges                     8
    lane order (top to bottom / left to right):
       1. Human plane: decision rights (§2.1, §3.2)
       2. Oversight and operations (§2.1)
       3. External: LLM providers (§2.3)
       4. L10 Room
       5. Interfaces: cli · mcp_server (§3.4, §11.3–11.4)
       6. L9 Lab
       7. L8 Evidence
       8. L7 Explain
       9. L6 Decide
      10. L5 Ledger
      11. L4 Beliefs
      12. L3 Assets
      13. L2 World
      14. L1 Data
      15. L0 Contracts
      16. External data sources (§2.2)
      17. Trust boundaries TB1–TB8 and layering rules (§2.4, §3.2, §3.3)

== View: engines - Deterministic engine data flow ==
  required checks:
    overlapping rectangles                   PASS
    outlines cutting nodes                   PASS
    clipped by the viewBox                   PASS
    text fit, 0.6 x font-size rule           PASS
    effective size >= 11px                   PASS
    edge endpoints touch nodes               PASS
    edges never cross a box                  PASS
    <title> on nodes/edges/labels            PASS
    Real Assets badge shown                  PASS
    WCAG contrast (light + dark)             PASS
  extra checks:
    text fit, installed Segoe UI metrics     PASS
    text fit, headless browser               PASS
    arrowheads not stacked                   PASS
    no shared line tracks                    PASS
    lines clear of box sides                 PASS
    bends not hidden by labels               PASS
    lines not hidden by captions             0 error(s), 13 warning(s)
    labels sit on their line                 PASS
  findings:
    WARN edge-under-caption (13)
      - edge engines-e0: 14px of line hidden under caption 'L0–L1 Contracts & data'
      - edge engines-e1: 14px of line hidden under caption 'L0–L1 Contracts & data'
      - edge engines-e2: 14px of line hidden under caption 'L0–L1 Contracts & data'
      - edge engines-e3: 14px of line hidden under caption 'L0–L1 Contracts & data'
      - edge engines-e4: 14px of line hidden under caption 'L0–L1 Contracts & data'
      - edge engines-e5: 14px of line hidden under caption 'L0–L1 Contracts & data'
      - edge engines-e6: 14px of line hidden under caption 'L0–L1 Contracts & data'
      - edge engines-e13: 14px of line hidden under caption 'L2 World'
      - edge engines-e17: 14px of line hidden under caption 'L2 World'
      - edge engines-e24: 14px of line hidden under caption 'L3 Assets'
      - edge engines-e84: 14px of line hidden under caption 'L8 Evidence'
      - edge engines-e89: 14px of line hidden under caption 'L8 Evidence'
      ... and 1 more
  contrast (lowest ratio per group and theme; --verbose lists every combination):
    dark  caption                sv-cap on sv-cb-layer                9.42:1  #b7c0cb on #151b22
    light caption                sv-cap on sv-cb-plane                7.14:1  #465160 on #f6eff7
    dark  edge label             sv-t-guard                           7.78:1  #a0a9b4 on #0f141a
    light edge label             sv-t-guard                           5.85:1  #5c6670 on #ffffff
    dark  edge stroke vs page    guard                                4.60:1  #738090 on #0f141a
    light edge stroke vs page    guard                                3.07:1  #8a94a1 on #ffffff
    dark  node outline vs band   human on sv-b-layer                  7.19:1  #dc8fbd on #151b22
    light node outline vs band   agentic on sv-b-plane                3.80:1  #b36800 on #f6eff7
    dark  node text              sv-ns on store                       8.05:1  #b7c0cb on #0c2d25
    light node text              sv-ns on human                       6.97:1  #465160 on #f8ebf3
  layout metrics:
    viewBox                      1360 x 2544.5
    render_width                 1400.0
    scale                        1.03
    screens_tall                 2.9
    nodes                        45
    edges                        104
    labels                       99
    node_rows                    10
    node_w                       (150, 150)
    node_h                       (86, 172)
    node_fill_median             0.91
    nodes_under_half_full        2
    text_lines_per_node_mean     5.1
    text_lines_per_node_max      7
    min_effective_px             11.32
    crossings                    565
    crossings_per_edge           5.43
    most_crossed                 [('engines-e98', 34), ('engines-e99', 32), ('engines-e61', 31), ('engines-e100', 31), ('engines-e77', 29)]
    bends_mean                   2.94
    bends_max                    4
    edge_len_mean                714
    edge_len_max                 2185
    edges_over_1000px            25
    label_hides_line_pairs       264
    line_px_hidden_under_labels  3578
    bends_hidden_under_labels    0
    labels_detached              0
    shared_tracks                0
    edge_through_node            0
    edge_grazes_node             0
    port_crowding                0
    endpoint_stats               {'box': 208}
    flow                         {'up': 54, 'same row': 30, 'down': 20}
    row_span_mean                1.85
    edges_spanning_4plus_rows    18
    worst_into_padding           {'text-fit': -1.0, 'text-fit/segoe-ui': -4.6, 'text-fit/browser': -4.6}
    ra_nodes                     ['real_assets_engine']
    ra_edges                     4
    lane order (top to bottom / left to right):
       1. Human plane
       2. L10 Room
       3. L9 Lab
       4. L8 Evidence
       5. L7 Explain
       6. L6 Decide
       7. L5 Ledger (one kernel)
       8. L4 Beliefs
       9. L3 Assets
      10. L2 World
      11. L0–L1 Contracts & data
      12. Guards & annotations

== View: capital_market - Organization and internal capital market ==
  required checks:
    overlapping rectangles                   PASS
    outlines cutting nodes                   PASS
    clipped by the viewBox                   PASS
    text fit, 0.6 x font-size rule           PASS
    effective size >= 11px                   PASS
    edge endpoints touch nodes               PASS
    edges never cross a box                  PASS
    <title> on nodes/edges/labels            PASS
    Real Assets badge shown                  PASS
    WCAG contrast (light + dark)             PASS
  extra checks:
    text fit, installed Segoe UI metrics     PASS
    text fit, headless browser               PASS
    arrowheads not stacked                   PASS
    no shared line tracks                    PASS
    lines clear of box sides                 PASS
    bends not hidden by labels               PASS
    lines not hidden by captions             0 error(s), 35 warning(s)
    labels sit on their line                 PASS
  findings:
    WARN edge-under-caption (35)
      - edge capital_market-e0: 14px of line hidden under caption 'Corporate Finance: internal bank'
      - edge capital_market-e1: 14px of line hidden under caption 'Corporate Finance: internal bank'
      - edge capital_market-e3: 14px of line hidden under caption 'TPA desk & engines (one solve)'
      - edge capital_market-e7: 14px of line hidden under caption 'Corporate Finance: internal bank'
      - edge capital_market-e7: 14px of line hidden under caption 'TPA desk & engines (one solve)'
      - edge capital_market-e9: 14px of line hidden under caption 'Investment groups (eight; Real Assets in'
      - edge capital_market-e12: 14px of line hidden under caption 'Investment groups (eight; Real Assets in'
      - edge capital_market-e24: 14px of line hidden under caption 'External counterparties'
      - edge capital_market-e25: 14px of line hidden under caption 'External counterparties'
      - edge capital_market-e38: 14px of line hidden under caption 'Investment groups (eight; Real Assets in'
      - edge capital_market-e40: 14px of line hidden under caption 'Investment groups (eight; Real Assets in'
      - edge capital_market-e42: 14px of line hidden under caption 'Investment groups (eight; Real Assets in'
      ... and 23 more
  contrast (lowest ratio per group and theme; --verbose lists every combination):
    dark  caption                sv-cap on sv-cb-actor_group          9.41:1  #b7c0cb on #171b1f
    light caption                sv-cap on sv-cb-actor_group          7.36:1  #465160 on #f4f5f2
    dark  edge label             sv-t-guard                           7.78:1  #a0a9b4 on #0f141a
    light edge label             sv-t-guard                           5.85:1  #5c6670 on #ffffff
    dark  edge stroke vs page    guard                                4.60:1  #738090 on #0f141a
    light edge stroke vs page    guard                                3.07:1  #8a94a1 on #ffffff
    dark  node outline vs band   external on sv-b-actor_group         6.94:1  #9aa5b4 on #171b1f
    light node outline vs band   boundary_note on sv-b-actor_group    4.63:1  #7d6f00 on #f4f5f2
    dark  node text              sv-ns on store                       8.05:1  #b7c0cb on #0c2d25
    light node text              sv-ns on human                       6.97:1  #465160 on #f8ebf3
  layout metrics:
    viewBox                      1360 x 2497
    render_width                 1400.0
    scale                        1.03
    screens_tall                 2.9
    nodes                        45
    edges                        94
    labels                       91
    node_rows                    9
    node_w                       (140, 140)
    node_h                       (101, 156)
    node_fill_median             0.79
    nodes_under_half_full        0
    text_lines_per_node_mean     5.3
    text_lines_per_node_max      7
    min_effective_px             11.32
    crossings                    913
    crossings_per_edge           9.71
    most_crossed                 [('capital_market-e92', 59), ('capital_market-e86', 57), ('capital_market-e91', 46), ('capital_market-e12', 46), ('capital_market-e14', 46)]
    bends_mean                   3.19
    bends_max                    4
    edge_len_mean                970
    edge_len_max                 2516
    edges_over_1000px            37
    label_hides_line_pairs       372
    line_px_hidden_under_labels  5022
    bends_hidden_under_labels    0
    labels_detached              0
    shared_tracks                0
    edge_through_node            0
    edge_grazes_node             0
    port_crowding                0
    endpoint_stats               {'box': 188}
    flow                         {'down': 38, 'up': 38, 'same row': 18}
    row_span_mean                2.35
    edges_spanning_4plus_rows    21
    worst_into_padding           {'text-fit': -1.0, 'text-fit/segoe-ui': -3.0, 'text-fit/browser': -3.0}
    ra_nodes                     ['g_real_assets']
    ra_edges                     5
    lane order (top to bottom / left to right):
       1. Owner & Board
       2. IC, officers & committees
       3. Corporate Finance: internal bank
       4. TPA desk & engines (one solve)
       5. Registry & intake stores
       6. External counterparties
       7. Investment groups (eight; Real Assets interim)
       8. Rules & controls

== View: lab - Agentic laboratory and trust boundaries ==
  required checks:
    overlapping rectangles                   PASS
    outlines cutting nodes                   PASS
    clipped by the viewBox                   PASS
    text fit, 0.6 x font-size rule           PASS
    effective size >= 11px                   PASS
    edge endpoints touch nodes               PASS
    edges never cross a box                  PASS
    <title> on nodes/edges/labels            PASS
    Real Assets badge shown                  PASS
    WCAG contrast (light + dark)             PASS
  extra checks:
    text fit, installed Segoe UI metrics     PASS
    text fit, headless browser               PASS
    arrowheads not stacked                   PASS
    no shared line tracks                    PASS
    lines clear of box sides                 PASS
    bends not hidden by labels               PASS
    lines not hidden by captions             0 error(s), 82 warning(s)
    labels sit on their line                 PASS
  findings:
    WARN edge-under-caption (82)
      - edge lab-e0: 14px of line hidden under caption 'LLM roles, family A (claude-opus-5-5)'
      - edge lab-e1: 14px of line hidden under caption 'Contract and provenance stores (L1, L8; '
      - edge lab-e2: 14px of line hidden under caption 'tpa lab run: L9 lab, the only process wi'
      - edge lab-e3: 14px of line hidden under caption 'Meta-controller FSM states (§7.4)'
      - edge lab-e3: 14px of line hidden under caption 'tpa lab run: L9 lab, the only process wi'
      - edge lab-e3: 14px of line hidden under caption 'LLM roles, family A (claude-opus-5-5)'
      - edge lab-e3: 14px of line hidden under caption 'LLM roles, family B (Phase 0: claude-son'
      - edge lab-e3: 14px of line hidden under caption 'LLMBackend (TPA_LLM_MODE: offline | repl'
      - edge lab-e3: 14px of line hidden under caption 'tpa evaluator serve --plane search (TB2)'
      - edge lab-e3: 14px of line hidden under caption 'tpa seal + final-plane evaluator (CRO ac'
      - edge lab-e4: 14px of line hidden under caption 'tpa lab run: L9 lab, the only process wi'
      - edge lab-e4: 14px of line hidden under caption 'LLM roles, family B (Phase 0: claude-son'
      ... and 70 more
  contrast (lowest ratio per group and theme; --verbose lists every combination):
    dark  caption                sv-cap on sv-cb-actor_group          9.41:1  #b7c0cb on #171b1f
    light caption                sv-cap on sv-cb-plane                7.14:1  #465160 on #f6eff7
    dark  edge label             sv-t-decision                        9.70:1  #e8a9cf on #0f141a
    light edge label             sv-t-feedback                        6.78:1  #7a5400 on #ffffff
    dark  edge stroke vs page    guard                                4.60:1  #738090 on #0f141a
    light edge stroke vs page    guard                                3.07:1  #8a94a1 on #ffffff
    dark  node outline vs band   external on sv-b-actor_group         6.94:1  #9aa5b4 on #171b1f
    light node outline vs band   agentic on sv-b-plane                3.80:1  #b36800 on #f6eff7
    dark  node text              sv-ns on store                       8.05:1  #b7c0cb on #0c2d25
    light node text              sv-ns on human                       6.97:1  #465160 on #f8ebf3
  layout metrics:
    viewBox                      1360 x 2932.5
    render_width                 1400.0
    scale                        1.03
    screens_tall                 3.4
    nodes                        84
    edges                        105
    labels                       97
    node_rows                    14
    node_w                       (144, 144)
    node_h                       (72, 158)
    node_fill_median             0.78
    nodes_under_half_full        1
    text_lines_per_node_mean     4.7
    text_lines_per_node_max      6
    min_effective_px             11.32
    crossings                    540
    crossings_per_edge           5.14
    most_crossed                 [('lab-e14', 38), ('lab-e65', 35), ('lab-e4', 33), ('lab-e11', 30), ('lab-e6', 29)]
    bends_mean                   2.91
    bends_max                    4
    edge_len_mean                834
    edge_len_max                 3309
    edges_over_1000px            37
    label_hides_line_pairs       237
    line_px_hidden_under_labels  3200
    bends_hidden_under_labels    0
    labels_detached              0
    shared_tracks                0
    edge_through_node            0
    edge_grazes_node             0
    port_crowding                0
    endpoint_stats               {'box': 210}
    flow                         {'up': 33, 'down': 36, 'same row': 36}
    row_span_mean                2.8
    edges_spanning_4plus_rows    33
    worst_into_padding           {'text-fit': -0.9, 'text-fit/segoe-ui': -2.0, 'text-fit/browser': -2.0}
    ra_nodes                     ['ra_engine']
    ra_edges                     1
    lane order (top to bottom / left to right):
       1. Human plane: signers, custodians, owners
       2. Contract and provenance stores (L1, L8; §10)
       3. Meta-controller FSM states (§7.4)
       4. tpa lab run: L9 lab, the only process with egress (TB3)
       5. LLM roles, family A (claude-opus-5-5)
       6. LLM roles, family B (Phase 0: claude-sonnet-5-5, labelled correlated)
       7. LLM roles, mixed
       8. tpa room (no
       9. families (shadow-IC
      10. network; detail in
      11. seat narrators)
      12. the room view)
      13. LLMBackend (TPA_LLM_MODE: offline | replay | live)
      14. Outside the machine (beyond the TB1 perimeter)
      15. tpa evaluator serve --plane search (TB2)
      16. tpa seal + final-plane evaluator (CRO account, TB4)
      17. CI integrity drills and lab calibration
      18. Planes, hashed at contract signing (§7.5)

== View: room - Decision room and IC flow ==
  required checks:
    overlapping rectangles                   PASS
    outlines cutting nodes                   PASS
    clipped by the viewBox                   PASS
    text fit, 0.6 x font-size rule           PASS
    effective size >= 11px                   PASS
    edge endpoints touch nodes               PASS
    edges never cross a box                  PASS
    <title> on nodes/edges/labels            PASS
    Real Assets badge shown                  PASS
    WCAG contrast (light + dark)             PASS
  extra checks:
    text fit, installed Segoe UI metrics     PASS
    text fit, headless browser               PASS
    arrowheads not stacked                   PASS
    no shared line tracks                    PASS
    lines clear of box sides                 PASS
    bends not hidden by labels               PASS
    lines not hidden by captions             0 error(s), 30 warning(s)
    labels sit on their line                 PASS
  findings:
    WARN edge-under-caption (30)
      - edge room-e0: 14px of line hidden under caption 'Decision Register and evidence (idm)'
      - edge room-e1: 14px of line hidden under caption 'Decision Register and evidence (idm)'
      - edge room-e2: 14px of line hidden under caption 'Decision Register and evidence (idm)'
      - edge room-e3: 14px of line hidden under caption 'Decision Register and evidence (idm)'
      - edge room-e44: 14px of line hidden under caption 'Agenda and human meeting H0–H6'
      - edge room-e45: 14px of line hidden under caption 'Decision Register and evidence (idm)'
      - edge room-e45: 14px of line hidden under caption 'IC pack: L0 / L1 / L2 and console (pack)'
      - edge room-e45: 14px of line hidden under caption 'Computed shadow IC: seats (q_k, θ_k ∈ Θ)'
      - edge room-e45: 14px of line hidden under caption 'Agenda and human meeting H0–H6'
      - edge room-e56: 14px of line hidden under caption 'Decision rights and politics rules'
      - edge room-e61: 14px of line hidden under caption 'Decision log, signposts, scoring'
      - edge room-e65: 14px of line hidden under caption 'Decision log, signposts, scoring'
      ... and 18 more
  contrast (lowest ratio per group and theme; --verbose lists every combination):
    dark  caption                sv-cap on sv-cb-actor_group          9.41:1  #b7c0cb on #171b1f
    light caption                sv-cap on sv-cb-actor_group          7.36:1  #465160 on #f4f5f2
    dark  edge label             sv-t-guard                           7.78:1  #a0a9b4 on #0f141a
    light edge label             sv-t-guard                           5.85:1  #5c6670 on #ffffff
    dark  edge stroke vs page    guard                                4.60:1  #738090 on #0f141a
    light edge stroke vs page    guard                                3.07:1  #8a94a1 on #ffffff
    dark  node outline vs band   human on sv-b-actor_group            7.18:1  #dc8fbd on #171b1f
    light node outline vs band   agentic on sv-b-actor_group          3.92:1  #b36800 on #f4f5f2
    dark  node text              sv-ns on store                       8.05:1  #b7c0cb on #0c2d25
    light node text              sv-ns on human                       6.97:1  #465160 on #f8ebf3
  layout metrics:
    viewBox                      1360 x 2610
    render_width                 1400.0
    scale                        1.03
    screens_tall                 3.0
    nodes                        65
    edges                        93
    labels                       88
    node_rows                    11
    node_w                       (147, 147)
    node_h                       (88, 158)
    node_fill_median             0.74
    nodes_under_half_full        7
    text_lines_per_node_mean     4.9
    text_lines_per_node_max      7
    min_effective_px             11.32
    crossings                    603
    crossings_per_edge           6.48
    most_crossed                 [('room-e59', 41), ('room-e4', 38), ('room-e82', 38), ('room-e5', 37), ('room-e40', 36)]
    bends_mean                   2.8
    bends_max                    4
    edge_len_mean                916
    edge_len_max                 3162
    edges_over_1000px            36
    label_hides_line_pairs       214
    line_px_hidden_under_labels  2889
    bends_hidden_under_labels    0
    labels_detached              0
    shared_tracks                0
    edge_through_node            0
    edge_grazes_node             0
    port_crowding                0
    endpoint_stats               {'box': 186}
    flow                         {'down': 40, 'same row': 33, 'up': 20}
    row_span_mean                2.6
    edges_spanning_4plus_rows    28
    worst_into_padding           {'text-fit': -0.9, 'text-fit/segoe-ui': -4.8, 'text-fit/browser': -4.8}
    ra_nodes                     ['ra_block', 'ra_head', 'seat_ra']
    ra_edges                     5
    lane order (top to bottom / left to right):
       1. Humans: proposers, owners, voters
       2. Decision Register and evidence (idm)
       3. IC pack: L0 / L1 / L2 and console (pack)
       4. Computed shadow IC: seats (q_k, θ_k ∈ Θ)
       5. Agenda and human meeting H0–H6
       6. Q&A, what-ifs W1–W3, view conditioning
       7. Decision log, signposts, scoring
       8. Decision rights and politics rules

== View: cycle - Quarterly cycle ==
  required checks:
    overlapping rectangles                   PASS
    outlines cutting nodes                   PASS
    clipped by the viewBox                   PASS
    text fit, 0.6 x font-size rule           PASS
    effective size >= 11px                   PASS
    edge endpoints touch nodes               0 error(s), 3 warning(s)
    edges never cross a box                  PASS
    <title> on nodes/edges/labels            PASS
    Real Assets badge shown                  PASS
    WCAG contrast (light + dark)             PASS
  extra checks:
    text fit, installed Segoe UI metrics     PASS
    text fit, headless browser               PASS
    arrowheads not stacked                   PASS
    no shared line tracks                    PASS
    lines clear of box sides                 PASS
    bends not hidden by labels               PASS
    lines not hidden by captions             PASS
    labels sit on their line                 PASS
  findings:
    WARN edge-endpoints (3)
      - edge cycle-e20 (c_monthly -> c_event, control): start stops 5.5px short of the axis tick of c_monthly (and 54px from its box)
      - edge cycle-e21 (c_annual -> c_t10, control): end stops 5.5px short of the axis tick of c_t10 (and 54px from its box)
      - edge cycle-e24 (c_ra -> c_t7, data): end stops 5.5px short of the axis tick of c_t7 (and 54px from its box)
  contrast (lowest ratio per group and theme; --verbose lists every combination):
    dark  chip                   gate chip                           15.34:1  #0f141a on #e7eaef
    light chip                   gate chip                           16.20:1  #ffffff on #1b2129
    dark  edge label             sv-t-decision                        9.70:1  #e8a9cf on #0f141a
    light edge label             sv-t-feedback                        6.78:1  #7a5400 on #ffffff
    dark  edge stroke vs page    decision                             7.67:1  #dc8fbd on #0f141a
    light edge stroke vs page    evidence                             3.42:1  #009e73 on #ffffff
    dark  free text              sv-cap sv-h-none                    10.06:1  #b7c0cb on #0f141a
    light free text              sv-el sv-loop-l sv-t-feedback        6.78:1  #7a5400 on #ffffff
    dark  node text              sv-ns on agentic                     8.17:1  #b7c0cb on #33240a
    light node text              sv-ns on human                       6.97:1  #465160 on #f8ebf3
  layout metrics:
    viewBox                      1360 x 673
    render_width                 1400.0
    scale                        1.03
    screens_tall                 0.8
    nodes                        20
    edges                        26
    labels                       25
    node_rows                    3
    node_w                       (129, 230)
    node_h                       (114, 154)
    node_fill_median             0.46
    nodes_under_half_full        11
    text_lines_per_node_mean     4.2
    text_lines_per_node_max      9
    min_effective_px             11.32
    crossings                    17
    crossings_per_edge           0.65
    most_crossed                 [('cycle-e17', 8), ('cycle-e19', 8), ('cycle-e22', 6), ('cycle-e18', 4), ('cycle-e24', 4)]
    bends_mean                   0.58
    bends_max                    2
    edge_len_mean                199
    edge_len_max                 1211
    edges_over_1000px            1
    label_hides_line_pairs       22
    line_px_hidden_under_labels  297
    bends_hidden_under_labels    0
    labels_detached              0
    shared_tracks                0
    edge_through_node            0
    edge_grazes_node             0
    port_crowding                0
    endpoint_stats               {'tick': 35, 'box': 14, 'tick_gap': 3}
    worst_into_padding           {'text-fit': -0.9, 'text-fit/segoe-ui': -2.7, 'text-fit/browser': -2.7}
    ra_nodes                     ['c_ra']
    ra_edges                     3
    lane order (top to bottom / left to right):
       1. Contract and data (T−28 to T−21)
       2. Pricing, lab campaign and seal (T−20 to T−11)
       3. Room preparation (T−10 to T−7)
       4. Decide (T−1 and T)
       5. Close and monitor (T+5 and monthly)

== Totals ==
  0 error(s), 184 warning(s) across 6 views
  JSON written to C:\Users\dean\AppData\Local\Temp\claude\C--users-dean-ai-envs\37b0d0cb-bd73-475d-ba00-d5f7286a2929\scratchpad\qa_final.json
```
