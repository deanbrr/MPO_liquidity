"""SYNTHETIC - NOT ADIC DATA. Verification step 4: the out-of-sample simulator.
- reproduce the certified P(goal) of B0 / B3 / O1 (rule, playbook) from O1's solution on the certification seed;
- fresh draws: certification vs selection vs tree paths vs replication-book paths (and seed collisions);
- same recourse rule: what the rule variant actually does (instrumented SCRATCH COPY of sim.py, never the original);
- exact bPOE vs the 400-candidate approximation used in the report."""
import json
import os
import pickle
import sys
import time

import numpy as np

SRC = r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2"
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
sys.path.insert(1, OUT)
sys.dont_write_bytecode = True
logf = open(os.path.join(OUT, "oos_check.log"), "w", encoding="utf-8", buffering=1)
T0 = time.time()


def L(msg=""):
    logf.write(f"[{time.time() - T0:7.1f}s] {msg}\n")
    logf.flush()


res = {}
try:
    from common import Params
    import world
    import sim as simmod
    from policy import extract_policy
    import vlib

    P = Params(os.path.join(SRC, "params.json"))
    w = world.build(P, log=None, phase1=False)
    D, m = w["D"], w["m"]
    dm = pickle.load(open(os.path.join(OUT, "full_dump.pkl"), "rb"))
    x1 = dm["caps"][3]["x"]
    pol = extract_policy(m, x1)
    truth = w["book"]["truth"]
    R = json.load(open(os.path.join(SRC, "results.json"), encoding="utf-8"))
    rep = R["oos"]["policies"]
    pols = {"B0": {"kind": "B0", "restore8": False}, "B3": {"kind": "B3", "restore8": True},
            "O1_rule": dict(pol, playbook=False), "O1_playbook": pol}
    s = simmod.Sim(D, w["gen"], 10000, P.get("seeds.cert"), truth, P.get("simulation.chunk"), idio=True, tpl_truth_seed=502)
    t0 = time.time()
    out = s.evaluate(pols)
    L(f"certification rerun (10,000 paths, seed 31, chunk 1250, tpl seed 502) in {time.time() - t0:.1f}s")
    for k in pols:
        pg = float(np.mean(out[k]["twr"] >= 0.10))
        L(f"  {k:12s} P(goal) rerun {pg:.6f}  results.json {rep[k]['p_goal']:.6f}  mean TWR {out[k]['twr'].mean():.6f} vs {rep[k]['twr_mean']:.6f}")
        res[f"repro_{k}"] = {"rerun": pg, "reported": rep[k]["p_goal"]}
    # rule vs playbook: node mapping only in the playbook variant
    res["rule_node1_unique"] = np.unique(out["O1_rule"]["node1"]).tolist()
    res["playbook_node1_unique"] = np.unique(out["O1_playbook"]["node1"]).tolist()[:12]
    L(f"  node1 used by O1_rule: {res['rule_node1_unique']}; by O1_playbook: {res['playbook_node1_unique']}")
    # exact bPOE vs the 400-candidate approximation of mpo_v2.bpoe_fast
    import importlib.util
    spec = importlib.util.spec_from_file_location("mpo_main_copy", os.path.join(SRC, "mpo_v2.py"))
    W = (1 + out["O1_rule"]["twr"]) ** 5
    Xg = 1.1 ** 5 - W
    pe = np.full(len(Xg), 1.0 / len(Xg))
    ex, _ = vlib.bpoe0(Xg, pe)
    srt = np.sort(Xg)
    neg = srt[srt < 0]
    cand = np.unique(-1.0 / neg)
    if len(cand) > 400:
        cand = np.quantile(cand, np.linspace(0, 1, 400))
    approx = min([1.0] + [float(np.mean(np.maximum(a * Xg + 1.0, 0.0))) for a in cand])
    res["bpoe_goal_O1_rule"] = {"exact": ex, "approx400": approx, "reported": rep["O1_rule"]["bpoe"]["goal"]}
    L(f"  bPOE at the goal, O1_rule: exact {ex:.6f}, 400-candidate approximation {approx:.6f}, reported {rep['O1_rule']['bpoe']['goal']}")
    # ---------------------------------------------------------------- fresh draws
    gen = w["gen"]

    def chunk_f(seed, ci, n):
        rng = np.random.default_rng([seed, ci])
        st0 = gen.start_state(n, rng)
        sm = gen.simulate(st0, 4, rng)
        return np.round(sm["f"][:, 0, :], 12)

    cert = np.vstack([chunk_f(31, ci, 1250) for ci in range(8)])
    sel = np.vstack([chunk_f(21, ci, 1000) for ci in range(4)])
    book = np.vstack([chunk_f(1031, ci, 2000) for ci in range(2)])
    # the tree's raw stage-1 paths (same RNG sequence as tree.build_tree with tree.seed)
    rng = np.random.default_rng(P.get("tree.seed"))
    gen.start_state(1, rng)
    st = gen.start_state(P.get("tree.n_stage1_paths"), rng)
    sm = gen.simulate(st, 4, rng)
    treef = np.round(sm["f"][:, 0, :], 12)
    hs = lambda A: set(map(bytes, np.ascontiguousarray(A).view(np.uint8).reshape(len(A), -1)))
    Hc, Hs, Hb, Ht = hs(cert), hs(sel), hs(book), hs(treef)
    res["fresh"] = {"cert_unique": len(Hc), "cert_n": len(cert), "cert_x_select": len(Hc & Hs), "cert_x_tree": len(Hc & Ht),
                    "cert_x_books": len(Hc & Hb), "select_x_tree": len(Hs & Ht)}
    L("  fresh-draw check (first-quarter factor vectors): " + json.dumps(res["fresh"]))
    # template-truth seed collisions (replication books: book seed sd, template-truth seed sd + 1)
    seeds_rep = P.get("seeds.replication_books")
    coll = [(sd, sd + 1) for sd in seeds_rep if sd + 1 in seeds_rep]
    res["seed_collisions_book_vs_tpl_truth"] = coll
    z_tpl = np.random.default_rng(7102).standard_normal(len(D["tpl"]))
    z_book = np.random.default_rng(7102).standard_normal(len(D["units"]))
    res["tpl_truth_7101_equals_book_7102_alpha_z"] = bool(np.allclose(z_tpl, z_book[:len(z_tpl)]))
    L(f"  template-truth seed of book k = book seed of book k+1: {coll}; identical normals: {res['tpl_truth_7101_equals_book_7102_alpha_z']}")
    # ---------------------------------------------------------------- same recourse rule: instrumented scratch copy
    src = open(os.path.join(SRC, "sim.py"), encoding="utf-8").read()
    patches = [("    lev_path = np.zeros((n, 6))\n", "    lev_path = np.zeros((n, 6))\n    revbal_path = np.zeros((n, 6))\n    hed_path = np.zeros((n, 6))\n    mult_path = np.zeros((n, 6))\n"),
               ("        lev_path[:, t] = E / W\n", "        lev_path[:, t] = E / W\n        revbal_path[:, t] = B[:, 0]\n        hed_path[:, t] = hed\n        mult_path[:, t] = (mult_now * is_commit[None, :]).sum(1)\n"),
               ('"capcls_path": capcls_path,', '"capcls_path": capcls_path, "revbal_path": revbal_path, "hed_path": hed_path, "mult_path": mult_path,')]
    src2 = src
    for a, b in patches:
        assert src2.count(a) == 1, a
        src2 = src2.replace(a, b)
    rp_line = "        if kind == \"plan\" and t <= 2:\n            rp = rp * 0.0"
    assert src2.count(rp_line) == 1
    src3 = src2.replace(rp_line, "        if kind == \"plan\" and t <= 2 and pol.get(\"playbook\", True):\n            rp = rp * 0.0")
    ns2, ns3 = {"__name__": "sim_instr"}, {"__name__": "sim_instr_rp"}
    exec(compile(src2, "sim_instr.py", "exec"), ns2)
    exec(compile(src3, "sim_instr_rp.py", "exec"), ns3)
    pols2 = {"B0": pols["B0"], "B1": {"kind": "B1", "restore8": True}, "O1_rule": pols["O1_rule"], "O1_playbook": pols["O1_playbook"]}
    s2 = ns2["Sim"](D, w["gen"], 10000, 31, truth, 1250, idio=True, tpl_truth_seed=502)
    o2 = s2.evaluate(pols2)
    s3 = ns3["Sim"](D, w["gen"], 10000, 31, truth, 1250, idio=True, tpl_truth_seed=502)
    o3 = s3.evaluate({"O1_rule": pols["O1_rule"]})
    pg2 = float(np.mean(o2["O1_rule"]["twr"] >= 0.10))
    pg3 = float(np.mean(o3["O1_rule"]["twr"] >= 0.10))
    rb = o2["O1_rule"]["revbal_path"]
    res["rule_recourse"] = {
        "O1_rule_P_goal_instrumented": pg2,
        "O1_rule_P_goal_with_revolver_repaid_like_baselines": pg3,
        "share_paths_revolver_drawn_t1": float(np.mean(rb[:, 1] > 1e-9)), "share_paths_revolver_drawn_t2": float(np.mean(rb[:, 2] > 1e-9)),
        "mean_revolver_t1_t2_bn": [float(rb[:, 1].mean()), float(rb[:, 2].mean())],
        "B1_share_revolver_drawn_t1": float(np.mean(o2["B1"]["revbal_path"][:, 1] > 1e-9)),
        "O1_rule_hed_path_mean": o2["O1_rule"]["hed_path"].mean(0).tolist(),
        "O1_rule_hed_path_sd": o2["O1_rule"]["hed_path"].std(0).tolist(),
        "B0_hed_path_mean": o2["B0"]["hed_path"].mean(0).tolist(),
        "O1_rule_commit_mult_sum_path": o2["O1_rule"]["mult_path"].mean(0).tolist(),
        "O1_rule_commit_mult_sd": o2["O1_rule"]["mult_path"].std(0).tolist(),
        "O1_playbook_commit_mult_sd": o2["O1_playbook"]["mult_path"].std(0).tolist(),
        "O1_rule_cap_path_t1_unique": np.unique(np.round(o2["O1_rule"]["cap_path"][:, 1], 4)).tolist(),
        "B0_cap_path_t1_unique": np.unique(np.round(o2["B0"]["cap_path"][:, 1], 4)).tolist(),
        "B1_cap_path_t1_unique": np.unique(np.round(o2["B1"]["cap_path"][:, 1], 4)).tolist(),
    }
    L("  rule recourse: " + json.dumps(res["rule_recourse"], default=float))
    # ---------------------------------------------------------------- in-tree simulator (E1) for B0 and O1 rule
    tw = simmod.tree_world(D, w["gen"])
    pw = tw["prob"]
    g_ext = simmod.run_policy(D, tw, {"kind": "B0", "restore8": False})["green_path"].astype(bool)
    e1 = {}
    for k in ("B0", "O1_rule", "O1_playbook"):
        pk = dict(pols[k], green_ext=g_ext) if pols[k]["kind"] == "plan" else pols[k]
        rr = simmod.run_policy(D, tw, pk)
        e1[k] = float(np.dot(pw, rr["twr"] >= 0.10))
    res["E1_intree_sim"] = e1
    res["E1_reported"] = {k: R["in_tree_simulator"][k]["p_goal"] for k in ("B0", "O1_rule", "O1_playbook")}
    L(f"  in-tree simulator P(goal): {e1}  reported {res['E1_reported']}")
    json.dump(res, open(os.path.join(OUT, "oos_check.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
except Exception:
    import traceback
    L(traceback.format_exc())
L("done")
