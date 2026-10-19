# Q01 challenge: can the optimizer be built, and solved within target?

*Skeptic review of `Q01_audit.md`, 2026-10-18. Every [I-calc] number is SYNTHETIC. [ch-calc] marks this review's own arithmetic or re-computation.*

**Result.** PARTIAL stands, as do IC ANSWER (No) and NEEDS ADIC DATA (No). BUILD is downgraded: P, module F and Phase I/II can be built now; H as specified cannot. Two audit claims are wrong and one is overstated.

## 1. Number checks

| Claim | Found | Where, and note |
|---|---|---|
| ≈1.8M variables per model; ≈5.4M for three | Yes | C1 §8 (both); synthesis §4.8 (1.8M only). Built as 150 variables/node × 1,000 leaves × 12 quarters (01_mpo §4.2); verifier R7's 8,121 nodes imply ≈1.2M [ch-calc]. |
| 0.8M variables, "tens of minutes with HiGHS" | Yes | C1 §8; synthesis §4.8 (no variable count) |
| 0.4M variables, "seconds to about a minute" | Yes | 01_mpo §4.2: one model, 200 scenarios, solver unstated |
| LP under 2 min; 10k paths × 40 quarters × 300 holdings under 60 s | Yes | Brief §3, "to be confirmed in design" |
| HiGHS MILP: 1.7, 9.3 and 39 s; 4.4 s | Yes | 08 verify R10 |
| Dual of 100 → 0.9%; dual of 0.237 → 76.8% | Yes | gap_02 §4. Re-computed 0.95/101 = 0.94% and 0.95/1.237 = 76.8%. The LP has 10 variables and 2 rows (`phase1_demo.py`). |
| T4′ dual 0.046–0.051 at appetite, 0 at tolerance; ≈3,000 variables | Yes | gap_04 §5; `g04_rh_results.json` (pooled Mix B, appetite: 0.0456–0.0508). `solve_rh` has 3,023 variables, solved by scipy `linprog(method="highs")`. |
| Clopper–Pearson: 0.97% passes, 1.08% fails | Yes | C1 §5.7; re-computed 0.973% and 1.076% |
| 54 min on 22 cores, ≈23 core-seconds per evaluation | Yes, but | gap_04 §6. It is not the only timing (§2, item 1). |
| 631 / 31,785 | Yes | 01 verify claim 18 and R3; re-computed exactly |

## 2. Claims that do not survive

1. **"The only simulator timing."** False. `g04_validate_results.json` records one integrated run of 10k paths × 20 quarters, in a single process, at 6.5 s [I-calc]. The audit's 23 core-seconds comes from 22 concurrent jobs, which slows each run about 3.5× (main runs take 27–31 s).
   - At 40 quarters that is ≈13 s [ch-calc], so the 60 s *evaluation* target is likely met at cohort level.
   - *Tuning* is the problem: 200 CMA-ES iterations × population 12 × 6 models ≈ 52 core-hours at 10k paths [ch-calc], against 01_mpo §4.2's "minutes" at 50k paths.
2. **The reduced H as evidence for H's duals.** It has no recourse variables, only 20 envelope variables plus CVaR auxiliaries over simulator bump sensitivities.
   - Its scenario-CVaR liquidity rows (L12, L24) have **zero** duals in every model, replication and band. The only liquidity price comes from the deterministic T4′ row.
   - The one binding scenario row, the CVaR₉₅ risk row (50-path tail), varies up to ≈2× across replications at appetite: 0.035–0.078 in M4 [I-calc].
3. **"The target LP is the size the research expects to take tens of minutes."** Overstated. Its 0.6M lower end sits next to the 0.4M "seconds to a minute" estimate, and both assume free per-node recourse, not H as specified (§3). The honest answer is "unknown", with [I] estimates on both sides.
4. **Tag.** The 08 verifier reproduced the 40-asset test exactly (08 verify §5), so it is [C] on synthetic data, not [I].

## 3. Why BUILD is downgraded

- **The sizing describes a different program.** C1 §5.6 puts linear decision rules (LDRs) in the fans, with coefficients "shared across each stage-2 node", but never defines ξ_[t] (what the rules respond to) or which nodes share coefficients. No file sizes this form, whose shared columns are dense.
- **H is a fixed point with P.** b^red and b^floor are "tuned in P" (C1 §5.4), λ^H_T is tuned until H and P rank actions alike, and ω and ψ are regressed from P (C1 §5.5). No rule says when this loop has converged.
- **LP or MILP?** 08 §7 solves "the here-and-now LP" for duals; synthesis §4.8 makes H a MILP with ≈900 binaries; the brief targets an LP.
- **The interface is still a proposal.** `DualSet.pi` is shaped [S, T], with no model axis and no rule for mapping tree nodes to scenarios (08 §7).
- **The T6 surrogate rests on a handful of leaves.** CVaR at 1 − ε′ = 99.4% puts 6 leaves per model in the tail at 1,000 leaves, and 1.2–2.4 at the Phase-0 size of 200–400 (synthesis §10) [ch-calc]. Under the certified mixes this is the binding price (groups §4.4, open item). No tail-weighted tree is specified, so C1 §8's replication-stability check would likely fail.

## 4. Gaps the audit missed

1. **Thin CVaR tail** for the T6 and severity rows (see §3). High.
2. **No size or density estimate for H in its LDR form.** The two node counts in the corpus disagree (12,000 vs 8,121 node-periods). High.
3. **No HiGHS estimate for the MILP at H scale.** "Tens of minutes" is for the LP, and "minutes to an hour" for the MILP names no solver. The overnight decomposed run is unestimated and its decomposition unbuilt. High.
4. **The path-based affine LP's density.** 11 §7 calls it "tractable" from a row count (≈2×10⁵). With 10²–10³ rule coefficients in every row, it carries ≈10⁷–10⁸ nonzeros [ch-calc]. Medium.
5. **Phase I multiplies the solves:** up to five tier solves, Phase II and the 10× penalty-invariance check make about seven H solves per pricing run, in no compute estimate. Medium.
6. **LDRs can make H infeasible** (01 lit §4.4). Phase I would read that as a structural deficit (u\* > 0) and trigger RECOVERY; no test tells the two apart. Medium.
7. **HDP-in-the-loop is infeasible, not just unbudgeted.** The benchmark (C1 §5.7) means 20,000–80,000 H solves; at the research's HiGHS estimates it cannot run. Medium.
8. **Two smaller points.** Lit §4.6 cites Lagrangian bounds whose gap does not grow with the number of subproblems, so price decomposition need not stay "only a heuristic". And the engine behind the reduced H and the timings runs on census v1.0, which fails V6 (groups C19, open item). Low.

## 5. Revised readiness

| Level | Audit | Challenge |
|---|---|---|
| DESIGN | Yes | Yes |
| BUILD | Yes (Phase 0) | **No for H; yes for P, F and Phase I/II** |
| IC ANSWER | No | No |
| NEEDS ADIC DATA | No | No |
