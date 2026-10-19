import sys, json
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
r = json.load(open(r"C:\users\dean\ai_envs\adic_tpa_lab\examples\mpo_v2\results.json", encoding="utf-8"))
for c in r["contingent_year1"]:
    print(c["node"], c["class"], c["stratum"], "p=%.4f" % c["prob"], "eq=%.3f brent=%.1f draw=%.4f" % (c["eq_year_log_excess"], c["brent"], c["draw_rate_next"]),
          "W=%.1f E/W=%.3f LQ=%.3f beta=%.2f tail=%.2f opp=%.2f M=%.2f ell=%.4f" % (c["W_bn"], c["E_over_W"], c["IGcash_over_W"], c["synthetic_beta_bn"], c["tail_notional_bn"], c["opp_im_bn"], c["red_margin_bn"], c["ell"]))
    print("    sales", {k: round(v, 4) for k, v in c["sales_bn_by_group"].items()}, "debt", {k: round(v, 3) for k, v in c["debt_bn"].items()}, "tpl", {k: round(v, 3) for k, v in c["templates_bn"].items()})
print("== cards HF/PC/RA/LO")
for c in r["cards"]:
    if c["group"] in ("HF", "LO", "PC", "RA") or c["action"] != "HOLD":
        print(c["unit_id"], c["action"], "sell %.3f red %.3f add %.3f size %.3f pce %.4f p* %.4f theta %.3f mu %.4f h %.4f hu %.4f D %.2f goal_driven %s" % (c["sell_frac"], c["redeem_frac"], c["add_frac"], c["size_bn"], c["p_ce"], c["p_star"], c["theta"], c["mu_hat"], c["hurdle_goal"], c["hurdle_utility"], c["duration_y"], c["goal_driven"]))
print("== change list flags")
for c in r["change_list"]:
    print(c["unit_id"], c["action"], c.get("lens"), round(c["size_bn"], 3), "dp_forced", c.get("dp_goal_forced"), "eqtail", c.get("dp_goal_forced_equal_tail"), "risk_budget", c.get("risk_budget"), "limit_driven", c.get("limit_driven"), "goal_driven", c.get("goal_driven"))
print("== in_tree_simulator", json.dumps(r["in_tree_simulator"]))
print("== selection", json.dumps(r["selection"]["summary"]))
print("== beliefs PC-05/SEC-06/CO-08 signals")
for b in r["beliefs"]:
    if b["unit_id"] in ("PC-05", "PC-02", "SEC-06", "CO-08", "CO-02", "HF-03", "RA-02"):
        print(b["unit_id"], json.dumps(b["signals_forward_basis"])[:600], "w", json.dumps(b["weights"]), "mu", b["mu_hat"], "own bid", b["mu_hat_with_own_bid"])
