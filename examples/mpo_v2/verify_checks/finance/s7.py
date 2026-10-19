import sys, json, os
sys.stdout = open(sys.argv[1], "w", encoding="utf-8")
d = os.path.dirname(os.path.abspath(sys.argv[1]))
hd = json.load(open(os.path.join(d, "fin_sim_full.json"), encoding="utf-8"))
print("book | SR draw | own: B0 / O1_rule / O1_playbook / veq_rule / veq_playbook / veq_rule_opp1.0 | SR0.30: veq_rule / veq_rule_opp1.0 / veq_playbook | SR0: veq_rule / veq_rule_opp1.0")
for b in ["BOOK_7101","BOOK_7102","BOOK_7103","BOOK_7104","BOOK_PLACEBO"]:
    p = os.path.join(d, f"book_{b}.json")
    if not os.path.exists(p):
        print(b, "missing"); continue
    j = json.load(open(p, encoding="utf-8"))
    o, s3, s0 = j["own"]["all10000"], j["sr030"]["all10000"], j["sr0"]["all10000"]
    print(f"{b} | {j['opp_sharpe_true']:.3f} | {100*o['B0']:.2f} / {100*o['O1_rule']:.2f} / {100*o['O1_playbook']:.2f} / {100*o['veq_O1_rule']:+.2f} / {100*o['veq_O1_playbook']:+.2f} / {100*o['veq_O1_rule_opp1.0']:+.2f} | "
          f"{100*s3['veq_O1_rule']:+.2f} / {100*s3['veq_O1_rule_opp1.0']:+.2f} / {100*s3['veq_O1_playbook']:+.2f} | {100*s0['veq_O1_rule']:+.2f} / {100*s0['veq_O1_rule_opp1.0']:+.2f}  [root opp {j['root_opp']:.2f} beta {j['root_beta']:.2f} E/W {j['root_E_W']:.3f}]")
    o4 = j["own"]["first4000"]
    print(f"     first 4000 (published paths): B0 {100*o4['B0']:.3f} O1_rule {100*o4['O1_rule']:.3f} O1_playbook {100*o4['O1_playbook']:.3f} veq_rule {100*o4['veq_O1_rule']:+.3f} veq_playbook {100*o4['veq_O1_playbook']:+.3f}")
s = hd["sealed"]; s3 = hd["sealed_sr030"]; s0 = hd["sealed_sr0"]
print(f"HEADLINE (cert seed) | 0.672 | {100*s['B0']['p_goal']:.2f} / {100*s['O1_rule']['p_goal']:.2f} / n.a. / {100*s['O1_rule']['veq']:+.2f} / n.a. / {100*s['O1_opp1.0']['veq']:+.2f} | {100*s3['O1_rule']['veq']:+.2f} / {100*s3['O1_opp1.0']['veq']:+.2f} / n.a. | {100*s0['O1_rule']['veq']:+.2f} / {100*s0['O1_opp1.0']['veq']:+.2f}")
