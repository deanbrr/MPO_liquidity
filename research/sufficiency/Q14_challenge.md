# Q14 challenge: groups and Corporate Finance as one internal capital market

*Skeptic review of `Q14_audit.md`, 2026-10-18. Every figure is SYNTHETIC (ADIC-like book, not ADIC data). Tags: [S] sourced, [C] checked, [I] assumption, [I-calc] computed.*

*Files:*
- *groups* = `research/groups/01_GROUPS_SYNTHESIS.md`
- *G-gap_0x* = `research/groups/addenda/gap_0x.md`
- *main* = `research/00_SYNTHESIS.md`
- *lit* = `research/literature/00_LITERATURE_SYNTHESIS.md`
- *brief* = `design/00_DESIGN_BRIEF.md`
- *context* = `inputs/00_CONTEXT_AND_PRIOR_WORK.md`

**Revised verdict: partial** (the audit says mostly sufficient).
- The seven-group mechanism is designed.
- The IC can be told how it works, not what it charges.
- Build is further off than "nearly".
- The client's new eighth group is missing.

## 1. Number checks: all ten found, with the stated meaning

| Value | Source | Tag |
|---|---|---|
| μ 0.243 vs 0.0113; 24% vs 1.1% | groups §4.8 t0 table; G-gap_01 §0 item 5 and §3 | [I-calc] |
| PE hurdle 299 → 14bp; card SELL 70.6% → HOLD 90.7% (percentages are reservation prices) | groups §4.8; G-gap_01 §3 | [I-calc] |
| FTP 71–306bp and 135–201bp; liquidity component ≈100–185bp; PE net α\* +20bp | G-gap_04 §5 | [I-calc] |
| Services ledger 0 vs −$7.05bn | G-gap_03 §1 and §3 | [I-calc] |
| $24.7m; 36 of 40 decisions | main §4.4 tags it [S], but dossier 08 Ex. 3 says "synthetic" | [I-calc] |
| Shapley CF and Public Markets values; error index 0.7–1.5 on P(red) and 1.0–2.6 on CE | Reproduced from `g04_shapley_summary.json`; the 69% end of "69–89%" is M2 (G-gap_04 §6) | [I-calc] |
| κ median 1.75 → 54% coverage; n_eff ≥ 20 → ±8.9pp | groups §5 | [I-calc] |
| δ\* 320 vs 80bp | groups §5; G-gap_02 M5 row | [I-calc] |
| 18/18 tests | Re-run here with `pytest -B -p no:cacheprovider`: 18 passed, no files changed | [C] |
| $0.44bn; +20% | groups §4.4 and §7.3; main §6.1 | [I] |

The values hold; several framings do not.

## 2. Claims that do not survive

1. **"Conservative" δ\*.**
   - G-gap_02 computes 320 / 80bp with B′ = $400bn per unit, the uncorrected 1/q_PE that G8 verifier R13 calls ≈3.5× too high; its own formula sets B′ = 1/H_g.
   - With B′ ≈ 113, status-quo pay gives ≈90bp [I-calc]. That is close to the 80bp at which FBE-R passed.
   - So the overstatement is not conservative for the pay-precondition conclusion (gate G-E; IC decision 7), which is untested at the corrected value.
2. **"Consistent with the literature verdicts."** The audit cites none of the following.
   - lit §4.2 rates the owner band *Contested* and keeps Mix A as the default without written agreement. Yet G-gap_04 computes FTP and envelopes only under Mix B. Mix A is infeasible at appetite (headroom −$0.05bn, G-gap_04 §5).
   - lit §4.4 rates the fixed recourse waterfall *Contradicted*, and G-gap_04's engine imports it.
   - lit §4.3 says the revolver is ≤ 50% available in the joint oil–crisis state. lit §4.5 gives pacing cuts no liquidity credit for two quarters. The R1 prices and the Q1 glide path (co-investment pause supplies 56%, G-gap_01 §2.2) ignore both.
3. **"Use groups v1.1 figures."**
   - context §1A and the allocation v2 note were edited at 18:12, after the audit. They now list eight groups and say allocation v2 (PE $52bn → $34bn; Real Assets $18bn) supersedes v1.
   - They record the user's choice of census v1.1 and say "the seven-group research ran on v1, so its numbers will be re-run".
   - Every group figure in the audit table rests on allocation v1 and census v1.0.
4. **"R1–R5 all fixed."** Only partly. R5's rule sets c_buf at the cost of Corporate Finance's cheapest liquidity action, but groups §4.3 keeps 1.5% (1–3%).
   - Once the revolver signs, it costs ≈15bp undrawn, 85bp drawn [S, main §4.4], or ≈23bp a year per $ of headroom (groups §4.8).
   - The CLC performance charge then sits several times above the decision price.
5. **Minor.**
   - `design/ARCHITECTURE.md` already has `strategy`/`sub_strategy` fields and a decision register (Q3, Q4, A3, A5), which narrows the build gap.
   - It still says "seven groups", and it keeps both "portfolio LEVER by CF" and "leverage up > 1pp is Tier A".

## 3. Gaps the audit missed

- **Real Assets (HIGH).**
  - brief §8 says "eight groups now" and makes the taxonomy configuration, not code.
  - There are no Real Assets envelopes, FTP, credibility, netting or decision rights.
  - The prototypes hard-code seven groups (`g01_core` `PRIV`; G-gap_04's nine players).
  - Real Assets' non-recourse asset debt sits outside CF's facilities but counts in look-through leverage. No rule assigns its approval or charge, and it runs against groups finding 8.
- **Re-runs on census v1.1 and allocation v2 (HIGH).** Envelopes, FTP (scaled by NCO/NAV), hurdles, Shapley values and co-investment flow all need re-running, reporting PE unfunded at both $16.4bn and $10.9bn.
- **Steady-state prices exist only under the contested band (HIGH).** CF's Shapley credit (−7.1 / −14.3 / −18.5pp) also bundles the band, a Board and owner lever, not CF's (groups §7.3; G-gap_04 §1.4).
- **Price levels are restated assumptions (MEDIUM–HIGH).**
  - The R0 dual equals the assumed CS-syndication cost (0.243), and the R1 dual equals the assumed revolver cost (0.011) (G-gap_01 §2.1 [I]).
  - PE's charge spans 9–299bp across states and methods (G-gap_01 §3; G-gap_04 §5) against an α of 196bp, so the sign of PE's net α\* is open.
  - G-gap_04's T4′ coefficient is a flat 0.62 per $ for every group except Co-investment (1.0).
  - The risk budget R is set at the plan's CVaR.
  - Co-investment's FTP *falls* at appetite (306 → 157bp), although groups §4.3 says FTP "rises".
- **Experiments still to run (MEDIUM):** a waterfall ablation, the revolver-availability and pacing-credit haircuts, and the δ\* gate re-run.
- **Netting beyond services (MEDIUM, not LOW).** PE stakes sold to Secondaries (lit §4.16; Gaspar–Massa–Matos) and Capital Solutions lending to funds in which PE is an LP are untested.
- **Credibility (LOW–MEDIUM).**
  - lit §4.10 is not folded in: cap credibility beyond ≈8 quarters, and widen ranges per person.
  - κ is inconsistent: a prior median of 1.75, a group table of 1.43–2.22, and a pre-scoring widening of ×1.81–2.74.

## 4. Readiness

| Level | Audit | Revised |
|---|---|---|
| DESIGN | Yes | Yes for the seven-group mechanism; Real Assets and asset-level debt rights open |
| BUILD | Nearly, so no | No, and further off: eight-group configuration, v2 re-runs, δ\*, FTP reconciliation, the T6 dual and the risk row |
| IC ANSWER | Yes | Qualitative only: "integrated by design for seven groups, untested, Real Assets pending". No figure can be quoted to the IC |
| ADIC DATA | Yes | Yes, plus real lever costs (revolver indications, SMA rights), which set every price |
