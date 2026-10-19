"""Merge extract_X1/X2/X3.json into architecture_model.json.

Run:  .venv\\Scripts\\python.exe design\\schematic\\merge_model.py
Every correction made while merging is logged in meta.corrections with the
ARCHITECTURE.md (or brief section 8) reference that settled it.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BADGE = "added 18 Oct; research in progress; interim rules (brief §8)"
VIEW_ORDER = ["overview", "engines", "capital_market", "lab", "room", "cycle"]
NODE_KINDS = ["deterministic", "agentic", "human", "store", "external", "boundary_note"]
EDGE_KINDS = ["data", "control", "price", "evidence", "decision", "feedback", "guard"]

corrections: list[dict] = []


def log(view: str, item: str, change: str, reason: str) -> None:
    corrections.append({"view": view, "item": item, "change": change, "reason": reason})


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def node(v: dict, nid: str) -> dict:
    for n in v["nodes"]:
        if n["id"] == nid:
            return n
    raise KeyError(f"{v['id']}: node {nid}")


def edge(v: dict, a: str, b: str, label_start: str | None = None) -> dict:
    hits = [e for e in v["edges"] if e["from"] == a and e["to"] == b
            and (label_start is None or e.get("label", "").startswith(label_start))]
    if len(hits) != 1:
        raise KeyError(f"{v['id']}: edge {a}->{b} ({len(hits)} matches)")
    return hits[0]


def setf(v: dict, obj: dict, field: str, value, reason: str, what: str) -> None:
    old = obj.get(field)
    if old == value:
        return
    obj[field] = value
    log(v["id"], what, f"{field}: {old!r} -> {value!r}", reason)


# --------------------------------------------------------------- brief refs
BRIEF_PATTERNS = [
    (re.compile(r"\(brief §8\.(\d), §8\.(\d)\)"), r"(brief §8 rules \1, \2)"),
    (re.compile(r"brief §8\.(\d)–8\.(\d)"), r"brief §8 rules \1–\2"),
    (re.compile(r"brief §8, §8\.(\d)"), r"brief §8 rule \1"),
    (re.compile(r"brief §8\.(\d)"), r"brief §8 rule \1"),
]


def norm_brief(s: str) -> str:
    for pat, rep in BRIEF_PATTERNS:
        s = pat.sub(rep, s)
    return s


def normalize_brief_refs(v: dict) -> None:
    """X1 wrote 'brief §8.1' etc., which reads like ARCHITECTURE §8.1 (decision rights)."""
    count = 0
    for coll in ("nodes", "edges"):
        for o in v[coll]:
            for f in ("section", "sublabel", "label", "detail"):
                if isinstance(o.get(f), str):
                    new = norm_brief(o[f])
                    if new != o[f]:
                        o[f] = new
                        count += 1
    new_notes = [norm_brief(t) for t in v.get("notes", [])]
    count += sum(1 for a, b in zip(v.get("notes", []), new_notes) if a != b)
    v["notes"] = new_notes
    if count:
        log(v["id"], "all section strings", f"{count} 'brief §8.n' refs -> 'brief §8 rule n'",
            "'§8.n' collides with ARCHITECTURE §8.n; brief §8 numbers interim rules 1-7")


# ------------------------------------------------------------ owner filling
HUMAN_SELF_OWNER = {
    "sovereign_owner": "Sovereign owner", "treasurer_cf": "Corporate Finance (Treasurer)",
    "board": "Board", "ic": "Investment Committee", "cio": "CIO", "cro": "CRO and CRO office",
    "group_heads": "Group heads", "ra_head": "Real Assets head", "ic_secretariat": "IC secretariat",
    "mrm": "MRM", "ai_governance": "AI governance function",
    "operators": "TPA desk quant developers; data/platform engineer",
    "raci_owners": "RACI owners named in the contract", "h1": "IC voting members",
    "h2": "IC voting members", "h3": "IC voting members (rotating devil's advocate)",
    "member_confirm": "IC member", "c_event": "Stage authority or decider per §8.1-8.2",
    "c_annual": "Proposers and deciders per Register A1-A9", "c_ra": "Real Assets head",
}


def fill_owners(v: dict) -> None:
    for n in v["nodes"]:
        if n.get("owner"):
            continue
        k = n["kind"]
        if n.get("badge"):
            n["owner"] = "Real Assets head" if k == "human" else "not yet assigned (brief §8 interim)"
        elif k == "human":
            n["owner"] = HUMAN_SELF_OWNER.get(n["id"], n["label"])
        elif k == "external":
            n["owner"] = "external (outside ADIC)"
        elif k == "boundary_note":
            n["owner"] = "design rule (no module owner)"
        else:
            n["owner"] = ""  # rendered as 'not stated in ARCHITECTURE.md'


def badge_ra(v: dict) -> set[str]:
    """Badge every Real Assets node, and every edge that touches one or rests on brief §8."""
    ra_nodes: set[str] = set()
    for n in v["nodes"]:
        if n.get("badge") or n.get("real_assets") or n.get("sublabel") == BADGE \
                or n.get("section", "").startswith("brief §8"):
            n["badge"] = BADGE
            ra_nodes.add(n["id"])
        n.pop("real_assets", None)
    for e in v["edges"]:
        if e.get("badge") or e["from"] in ra_nodes or e["to"] in ra_nodes \
                or e.get("section", "").startswith("brief §8"):
            e["badge"] = BADGE
    for n in v["nodes"]:
        if n.get("badge") and n.get("sublabel") == BADGE:
            raise ValueError(f"{v['id']}:{n['id']} still uses the badge text as its sublabel")
    return ra_nodes


# -------------------------------------------------------- per-view fixes
def fix_overview(v: dict) -> None:
    setf(v, node(v, "llm_gateway"), "owner", "CIO office under AI governance",
         "§3.4 lab/agents owner; §7.2 puts the gateway inside 'tpa lab run' (matches X3)",
         "node llm_gateway")
    e = edge(v, "ra_engine", "priv")
    setf(v, e, "label", "closed-end funds reuse PE-fund engine",
         "brief §8 rule 2 wording (reuse of the PE-fund commitment engine)", "edge ra_engine->priv")
    setf(v, node(v, "group_taxonomy"), "section", "brief §8 rule 1; §3.4 (GroupId); §9.1",
         "§9.1 is where ARCHITECTURE fixes the seven-group hierarchy", "node group_taxonomy")
    setf(v, edge(v, "ic", "board"), "section", "§2.1; §2.4; §8.1",
         "§8.1 Board/owner row: 'IC recommendation plus minority report'", "edge ic->board")
    v["groups"] = [
        {"id": "tb1_machine", "label": "ADIC machine: TB1 data perimeter", "rows_of_lanes": ["L10", "L0"],
         "section": "§2.4 (TB1); §7.2", "kind": "perimeter"},
        {"id": "tb3_lab", "label": "tpa lab run: TB3 sole egress", "nodes": ["lab", "agents", "llm_gateway"],
         "section": "§2.4 (TB3); §7.2"},
        {"id": "tb2_eval", "label": "TB2 evaluator", "nodes": ["evaluator_search"],
         "section": "§2.4 (TB2); §7.2"},
        {"id": "tb4_seal", "label": "TB4 seal (CRO account)", "nodes": ["evaluator_final", "seal", "final_store"],
         "section": "§2.4 (TB4); §7.2; §7.5"},
        {"id": "tb8_truth", "label": "TB8 truth seal", "nodes": ["truth_store"], "section": "§2.4 (TB8); §9.4"},
    ]
    log("overview", "groups", "added 5 trust-boundary enclosures (TB1, TB2, TB3, TB4, TB8)",
        "task asks for the evaluator/seal boundary and trust boundaries; members per §2.4 and §7.2")


def fix_engines(v: dict) -> None:
    n = node(v, "real_assets_engine")
    setf(v, n, "sublabel", "closed-end funds on PE-fund engine; Geltner NAV; NR debt; redemption queue",
         "X2 used the badge text as sublabel; content from brief §8 rule 2", "node real_assets_engine")
    setf(v, n, "section", "brief §8 rule 2", "specific interim rule", "node real_assets_engine")
    for (a, b, sec) in [("scen", "real_assets_engine", "§4.1; brief §8 rule 5"),
                        ("beliefs", "real_assets_engine", "§4.7; brief §8 rule 4"),
                        ("real_assets_engine", "ledger", "brief §8 rules 2–3"),
                        ("real_assets_engine", "actions", "brief §8 rule 3")]:
        setf(v, edge(v, a, b), "section", sec, "specific interim rule of brief §8", f"edge {a}->{b}")
    setf(v, edge(v, "icm", "pack"), "kind", "price",
         "λ, FTP and envelopes are prices (§6.1); X1 draws the same edge as 'price'", "edge icm->pack")
    for b in ("core_sim", "seal"):
        setf(v, edge(v, "c_h", b), "kind", "data",
             "C_H is a candidate fed to P and to the sealed run (§5.9, §7.4), not evidence for the IC",
             f"edge c_h->{b}")
    setf(v, node(v, "cards"), "sublabel", "actions scores on H duals: priced_on, intervals, flips",
         "§3.4 puts cards in `actions` (L3); drawn here downstream of the duals as in the §3.2 diagram",
         "node cards")


def fix_capital_market(v: dict) -> None:
    setf(v, node(v, "sovereign_owner"), "kind", "human",
         "§2.1 lists the owner as an actor who decides the draw; §3.3 human column; X1 uses 'human'",
         "node sovereign_owner")
    n = node(v, "g_real_assets")
    setf(v, n, "sublabel", "RE, infra, energy & NR; funds, co-invest, direct/JV; NR asset debt",
         "X2 used the badge text as sublabel; content from brief §8 background and rule 3",
         "node g_real_assets")
    setf(v, n, "section", "brief §8 rules 1, 3, 6", "specific interim rules", "node g_real_assets")
    setf(v, node(v, "group_heads"), "section", "§2.1; §6; brief §8 rule 1 (generic over groups)",
         "generic node, not a Real Assets addition, so it stays unbadged", "node group_heads")
    for b in ("g_privcredit", "g_capsol", "g_overlay", "g_secondaries"):
        setf(v, edge(v, "g_real_assets", b), "section", "brief §8 rule 7", "interaction list", f"edge ->{b}")
    e = edge(v, "g_real_assets", "treasurer_cf")
    setf(v, e, "label", "look-through leverage, collateral", "brief §8 rule 7 (CF line)", "edge ->treasurer_cf")
    setf(v, e, "section", "brief §8 rules 3, 7", "brief §8 rule 3: NR debt counts in look-through leverage",
         "edge ->treasurer_cf")
    setf(v, edge(v, "treasurer_cf", "liquidity_buffer"), "label", "buffer (Q3), top-up (Q2)",
         "§8.2: Q2 holds the reserve top-up, Q3 the buffer", "edge treasurer_cf->liquidity_buffer")
    # lane rows: groups row keeps Real Assets next to its brief §8 rule 7 partners
    order = ["group_heads", "g_pe", "g_coinvest", "g_public", "g_overlay",
             "g_secondaries", "g_capsol", "g_real_assets", "g_privcredit"]
    for i, nid in enumerate(order):
        node(v, nid)["order"] = i
    log("capital_market", "lane groups", "re-ordered group nodes (layout only)",
        "keeps Real Assets beside Private Credit, Capital Solutions, Secondaries (brief §8 rule 7)")


def fix_lab(v: dict) -> None:
    setf(v, node(v, "backend_live"), "kind", "deterministic",
         "§7.13/§3.2: AnthropicBackend is one of three LLMBackend classes inside `agents`; "
         "only the provider (llm_providers) is external", "node backend_live")
    n = node(v, "ra_engine")
    setf(v, n, "sublabel", "closed-end funds reuse PE-fund engine; Geltner NAV; NR debt; queue",
         "X3 used the badge text as sublabel; content from brief §8 rule 2", "node ra_engine")
    existing = {(e["from"], e["to"]) for e in v["edges"]}
    added = 0
    for n in v["nodes"]:
        tgt = n.get("attached_to")
        if n["kind"] == "boundary_note" and tgt and (n["id"], tgt) not in existing:
            v["edges"].append({"from": n["id"], "to": tgt, "label": "", "kind": "guard",
                               "section": n["section"]})
            added += 1
    log("lab", "guard edges", f"added {added} guard edges from 'attached_to' fields",
        "X3 attached TB notes to nodes without drawing an edge; §2.4 enforcement points")


def fix_room(v: dict) -> None:
    subs = {
        "ra_head": ("RE, infra, energy & NR; funds, co-invest, direct; files forecasts",
                    "brief §8 background and rules 1, 4"),
        "seat_ra": ("q: Real Assets filed forecasts; θ and loss term not yet set",
                    "brief §8 rule 1 gives the seat; §8.5 group-seat belief channel"),
        "ra_block": ("group block B; interim SELL/HOLD/REFI/LEVER cards",
                     "brief §8 rules 1 and 3; §8.6 agenda block B"),
    }
    for nid, (sub, why) in subs.items():
        setf(v, node(v, nid), "sublabel", sub, f"X3 used the badge text as sublabel; {why}", f"node {nid}")


def fix_cycle(v: dict) -> None:
    setf(v, node(v, "c_ra"), "sublabel", "files at T−25; cards at T−20; seat at T−7",
         "X3 used the badge text as sublabel; content from its own detail (brief §8 rules 1, 3, 4)",
         "node c_ra")


def guards(v: dict) -> None:
    kinds = {n["id"]: n["kind"] for n in v["nodes"]}
    count = 0
    for e in v["edges"]:
        if kinds.get(e["from"]) == "boundary_note" and e["kind"] != "guard":
            e["kind"] = "guard"
            count += 1
    if count:
        log(v["id"], "edges from rule notes", f"{count} edges re-kinded to 'guard'",
            "they state a rule that constrains the target (§2.4, §6, §8.1), not a data or control flow")


# ------------------------------------------------------------------ layout
def lr(*rows):
    return [list(r) for r in rows]


LAYOUTS = {
    "overview": {"mode": "grid", "columns": 8, "rows": lr(
        ["human"], ["oversight", "ext_ai"], ["L10", "interfaces"], ["L9"], ["L8"], ["L7"], ["L6"],
        ["L5"], ["L4"], ["L3"], ["L2"], ["L1"], ["L0"], ["ext_data"], ["boundaries"])},
    "engines": {"mode": "grid", "columns": 7, "rows": lr(
        ["human_plane", "l10_room"], ["l9_lab", "l8_evidence"], ["l7_explain"], ["l6_decide"],
        ["l5_ledger"], ["l4_beliefs"], ["l3_assets"], ["l2_world"], ["l0_l1_inputs", "annotations"]),
        "lane_rows": {"l6_decide": lr(
            ["core_tree", "phase1", "recovery_mode", "phase2", "duals_kernel", "colgen_levelb", "cards"],
            ["core_policy", "core_sim", "certify", "c_h", "module_f", "icm"])}},
    "capital_market": {"mode": "grid", "columns": 7, "rows": lr(
        ["owner_board", "governance"], ["internal_bank"], ["engines"], ["intake", "external"],
        ["groups"], ["controls"]),
        "lane_rows": {"groups": lr(
            ["group_heads", "g_pe", "g_coinvest", "g_public", "g_overlay"],
            ["g_secondaries", "g_capsol", "g_real_assets", "g_privcredit"])}},
    "lab": {"mode": "grid", "columns": 7, "rows": lr(
        ["l_human"], ["l_stores"], ["l_fsm"], ["l_lab"], ["l_agents_a"],
        ["l_agents_b", "l_agents_mix", "l_room"], ["l_llm", "l_external"], ["l_eval"],
        ["l_seal", "l_ci"], ["l_planes"]),
        "lane_rows": {
            "l_fsm": lr(["st_draft", "st_frozen", "st_signed", "st_signed_rec", "st_design_reviewed",
                         "st_baseline_priced", "st_ideation"],
                        ["st_screening", "st_selection", "st_sealed", "st_retrospective", "st_memo",
                         "st_review", "st_shadow_ic"],
                        ["st_prevote_lock", "st_ic", "st_closed", "st_escalate", "st_aborted"]),
            "l_lab": lr(["meta_controller", "tool_firewall", "llm_gateway", "tb1", "budgets"],
                        ["campaign_memory", "escalation", "claims_validator", "claims_renderer",
                         "design_linter"])},
        "serpentine": ["l_fsm"], "pack": ["l_fsm"]},
    "room": {"mode": "grid", "columns": 7, "rows": lr(
        ["r_actors"], ["r_register"], ["r_pack"], ["r_shadow"], ["r_meeting"], ["r_whatif"],
        ["r_log", "r_rules"]),
        "lane_rows": {"r_meeting": lr(["h0", "h1", "h2", "h3", "h4", "h5", "h6"],
                                      ["agenda", "consent_agenda", "ra_block", "decision_rules",
                                       "minutes_drafter"])},
        "pack": ["r_meeting"]},
    "cycle": {"mode": "timeline"},
}

KIND_TEXT = {
    "node": {
        "deterministic": "Deterministic: engines and code own every number (§3.3)",
        "agentic": "Agentic: LLM roles propose, extract, argue, narrate (§3.3)",
        "human": "Human: decides, signs, votes (§2.1, §3.3)",
        "store": "Store: data store, registry or balance held",
        "external": "External system or party (§2.2, §2.3)",
        "boundary_note": "Rule or trust-boundary note (§2.4)",
    },
    "edge": {
        "data": "Data or flow, producer to consumer",
        "control": "Control: request, spawn, configure",
        "price": "Price: λ, FTP, duals, quotes",
        "evidence": "Evidence to the pack, claims or IC",
        "decision": "Decision: sign-off, vote, approval",
        "feedback": "Feedback: scores, previous-quarter outputs",
        "guard": "Rule or guard applies to",
    },
}


# -------------------------------------------------------------- validation
def validate(v: dict) -> list[str]:
    errs = []
    ids = [n["id"] for n in v["nodes"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate node ids")
    lanes = {l["id"] for l in v["lanes"]}
    for n in v["nodes"]:
        if n["lane"] not in lanes:
            errs.append(f"node {n['id']} lane {n['lane']} missing")
        if n["kind"] not in NODE_KINDS:
            errs.append(f"node {n['id']} kind {n['kind']}")
        if not n.get("section"):
            errs.append(f"node {n['id']} has no section")
    for e in v["edges"]:
        for end in ("from", "to"):
            if e[end] not in ids:
                errs.append(f"edge {e['from']}->{e['to']} missing {end}")
        if e["kind"] not in EDGE_KINDS:
            errs.append(f"edge {e['from']}->{e['to']} kind {e['kind']}")
        if not e.get("section"):
            errs.append(f"edge {e['from']}->{e['to']} has no section")
    lay = v["layout"]
    if lay["mode"] == "grid":
        placed = [l for row in lay["rows"] for l in row]
        if sorted(placed) != sorted(lanes):
            errs.append(f"layout rows {sorted(placed)} != lanes {sorted(lanes)}")
        for lane, rows in lay.get("lane_rows", {}).items():
            members = sorted(n["id"] for n in v["nodes"] if n["lane"] == lane)
            if sorted(x for r in rows for x in r) != members:
                errs.append(f"lane_rows {lane} does not match lane members")
    return errs


def main() -> int:
    x = [load(f"extract_X{i}.json") for i in (1, 2, 3)]
    views = {v["id"]: copy.deepcopy(v) for xi in x for v in xi["views"]}
    fixes = {"overview": fix_overview, "engines": fix_engines, "capital_market": fix_capital_market,
             "lab": fix_lab, "room": fix_room, "cycle": fix_cycle}
    out_views, problems = [], []
    for vid in VIEW_ORDER:
        v = views[vid]
        normalize_brief_refs(v)
        fixes[vid](v)
        guards(v)
        badge_ra(v)
        fill_owners(v)
        v.setdefault("groups", [])
        v["layout"] = LAYOUTS[vid]
        problems += [f"{vid}: {p}" for p in validate(v)]
        out_views.append(v)
    meta = {
        "title": "TPA Lab Architecture",
        "project": "ADIC Agentic Total-Portfolio Laboratory",
        "source": "design/ARCHITECTURE.md, pre-critique version, 18 Oct 2026",
        "ra_notice": ("Real Assets, the eighth investment group, is being integrated. Items badged '"
                      + BADGE + "' come from design/00_DESIGN_BRIEF.md §8 and are not yet in ARCHITECTURE.md."),
        "badge_text": BADGE,
        "synthetic_label": "SYNTHETIC – NOT ADIC DATA",
        "section_convention": ("§x.y = ARCHITECTURE.md; 'brief §8 rule n' = 00_DESIGN_BRIEF.md §8 interim "
                               "rule n; ADR-nn = ARCHITECTURE.md §12"),
        "merged_from": ["extract_X1.json (overview)", "extract_X2.json (engines, capital_market)",
                        "extract_X3.json (lab, room, cycle)"],
        "kinds": KIND_TEXT,
        "corrections": corrections,
    }
    model = {"meta": meta, "views": out_views}
    (HERE / "architecture_model.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=1), encoding="utf-8")
    for v in out_views:
        nb = sum(1 for n in v["nodes"] if n.get("badge")) + sum(1 for e in v["edges"] if e.get("badge"))
        print(f"{v['id']:15s} lanes={len(v['lanes']):2d} nodes={len(v['nodes']):3d} "
              f"edges={len(v['edges']):3d} badged={nb:2d} notes={len(v.get('notes', [])):2d}")
    print(f"corrections logged: {len(corrections)}")
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

