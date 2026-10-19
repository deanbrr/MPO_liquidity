# Q14 audit: the seven groups and Corporate Finance as one internal capital market (R14)

*Audit, 2026-10-18. Every figure is SYNTHETIC unless stated. Tags: [S] sourced, [C] corrected or checked, [I] inference, [I-calc] computed.*

**Verdict: mostly sufficient.** Ready to design and nearly ready to build. The IC can get a synthetic answer today. Price levels and credibility need ADIC data.

## 1. Answer today

**Yes, by design and in synthetic prototypes. Not yet shown to work in practice.** The research models ADIC as an internal capital market in which the groups compete for unencumbered liquidity. Corporate Finance (CF) owns and prices that liquidity (groups synthesis §1, §2.1; main §2.2).

- **Taxonomy and actions.**
  - Each group is a module with schema, state, engine, SELL / HOLD / REFINANCE / LEVER rules (plus PACE and ADD), constraints and sourced parameters (groups §3.1–3.7).
  - One kernel prices everything; group P&L is attribution only.
  - Control rights decide which actions exist (consents, GP-triggered events, gate V23).
  - CF owns portfolio LEVER, collateral and payouts; groups propose asset-level actions.
- **Internal capital market.**
  - Groups are price-takers inside quantity envelopes, Λ_g = Σ a_i(x\*), from the same optimizer that produces λ. Releasing capacity is free; increases pay the dual.
  - Decision charges come from undamped robust duals, with no floor. The published FTP curve is an EWMA with a ±50% collar.
  - Performance charges are vintage-locked, and CF holds the mismatch.
  - Prices come only from a feasible problem (the Phase-II restored one), and each carries a `priced_on` flag (groups §4.3–4.4, §4.8).
- **Netting.** Liquidity raised means external cash only. Both legs are booked at fair value, and any wedge goes to a centre line. Gate V2 checks netting on both cash and DVA ledgers (groups §4.1).
- **Credibility.**
  - One bitemporal registry, WIS scoring, one bias model and one overconfidence parameter, κ_g.
  - A group's score is shown only against its own reference class, and only once n_eff ≥ 20. No league tables.
  - Pay does not depend on budget size (groups §5, §7.4).
- **Decision rights** (groups §7.3; main §6.1):
  - deals inside the envelope: the group;
  - up to +20% above the envelope: CIO + CRO (Tier B);
  - actions ≥ 0.25% of NAV: full IC (Tier A);
  - envelopes and FTP: TPC/IC each quarter, with the method approved by the Board;
  - contingency-funding (CFP) actions: by stage.

**Caveat for the IC.** Following the prices reproduces the optimum only by construction (G8 verifier R14). In a synthetic 40-asset test, a price-only rule did $24.7m worse than the exact MILP, so the marginal assets go to the IC (main §4.4; dossier 08, Example 3).

| Value (SYNTHETIC) | Meaning | Source | Tag |
|---|---|---|---|
| 24% vs 1.1% PV per $ of month-24 headroom (μ 0.243 vs 0.0113) | t0 liquidity price before vs after a signed revolver | groups §4.8; groups gap_01 §3 | [I-calc] |
| PE hurdle 299bp → 14bp; PE card SELL (70.6%) → HOLD (90.7%) | The same price change flips group cards | groups §4.8 | [I-calc] |
| FTP 71–306bp per NAV-year at tolerance (risk only); 135–201bp at appetite | Reduced-H charges, Mix B, M1–M5, census v1.0 | groups gap_04 §5 | [I-calc] |
| 0 vs −$7.05bn | The services ledger nets to zero on 2,000 paths; the naive booking double counts in S1 | groups gap_03 §3 | [I-calc] |
| $50m | Fake alpha from a $1bn internal transfer at 85% vs a 90% fair value | groups §4.1 | [I-calc] |
| CF −7.1 / −14.3 / −18.5pp | Nine-player Shapley ΔP(red) in M1 / M4 / M6; census v1.0, re-run pending (C19) | groups gap_04 §6 | [I-calc] |
| κ_g median 1.75 | A stated 80% interval covers ≈54% of outcomes | groups §5 | [I-calc] |
| δ\* 320bp vs 80bp | Forecast inflation under status-quo vs designed pay. Conservative: ≈3.5× high per G8 verifier R13 | groups §5–6 | [I-calc] |
| 18/18 | Group pinned-dual test; this audit re-ran it and it passes | groups `gap_01_calcs` | [C] |

## 2. Evidence

**Strongest sources.**
1. **Groups synthesis v1.1.** A complete specification. Of 289 group claims checked, 245 were confirmed, 32 corrected and none refuted; high on facts, medium on design (groups §0).
2. **G8 dossier and verification log.** The theory (Baumol–Fabian, Scharfstein–Stein, CEBS/FSI FTP) is confirmed on 30 of 32 claims. Rated MEDIUM for specification errors R1–R5, all fixed in the groups synthesis.
3. **Prototypes.** Groups gap_01 (Phase I/II envelopes, FTP, hurdles, tests); gap_03 (services ledger, self-verified); gap_04 (a joint engine for the groups and CF, exact Shapley over 512 coalitions). All use stylised proxies, and a one-year LP or a linearised block stands in for the 12-quarter H.
4. **Literature** §4.6 and §4.16: "supported, refined". No study covers internal capital markets or FTP inside asset owners (§4.17), so the mechanism is a transplant from corporations and banks.

**Contradictions.** The main synthesis was last written at 15:08 and groups v1.1 at 17:22, so main is stale in places.
- **Price-following.** Main L14 says a group that follows its prices "cannot hurt the total portfolio". Groups C10 and G8 R14 say that holds only by construction.
- **Overlay row.** Main §2.2 has "$15bn in stress" and "−6.0 in a crash year". Groups C8 has $10bn and −$4.0bn.
- **Contingent-budget gate.** Main §4.4 requires CFP Green or Amber. Groups C7 allows any stage but Black.
- **30-day coverage and stage.** Main §4.9, §6.7 and §9.1 show ADIC-LCR(30d) at 2.10× and "stage Red". Groups C12 and C16 give 1.91× on CF-controlled HQLA (Amber), and the book is Red on the forward-looking indicator only.
- **Census.** Main findings 3–4 use census v1.0: PE drought net −$2.0 to −$2.3bn, unfunded/NAV 0.53. The groups headline uses the proposed v1.1: −$0.9bn and 0.32. T4′ on v1.1 and the gap_04 re-runs are still open (C18, C19).
- **Decision rights.**
  - Groups §7.3 gives portfolio LEVER to CF. Main §6.1 makes a leverage increase above 1pp a Tier-A item, and leverage outside its band a Board item.
  - Tail budget: main makes changes above 10bp Tier A; groups makes any move within the band Tier A.
- **Literature vs both syntheses**, not yet folded in (brief §7 item 10 requires ADRs): an Euler-CVaR risk row vs Bauer & Zanjani's owner-loss row; "no idle reserve pays" vs Diamond & Rajan; misallocation as established vs Whited; a single hurdle and uncollared envelopes vs Krüger et al. and Hoang & Ruckes; δ\* linear in the stake vs Evans et al.
- **Tagging.** Main tags the 40-asset test [S]; it is a synthetic computation.

**Citation-audit errors that touch Q14** (literature §2). All are still unfixed in groups v1.1:
- **G4, barrier correction.** The sign is wrong, and the script applies no correction at all. Co-investment LTV breaches (50–63%) and holdco wipe-out (7.0% → 22.8%) are therefore understated. The conclusion against asset-level LEVER gets stronger, but the numbers are provisional.
- **G4, Bhardwaj–Gupta–Howell.** Misused: the post-recap distress multiplier of 1.4–3.4 should be ≈1.1–1.7.
- **G8 and G2, Glaser et al.** The quotes are not in the abstracts. They are part of the forecast-inflation evidence.
- **Hygiene only:** Lamont's pages and the Shin & Stulz working-paper pointer (G8); Boyer et al. superseded by the 2023 version (G2); "Central Treasury" should read Corporate Finance (G7).

## 3. Readiness

| Level | Ready | Reason |
|---|---|---|
| DESIGN | Yes | Every R14 element and brief decisions 16–20 has a mechanism, owner and rule, consistent across the groups synthesis, main gap_01 and the literature verdicts |
| BUILD | Nearly, so no | Formulas, schemas, gates and tests exist, but no single H computes the full charge. Open: risk row, pricing level, contingent-liquidity channel, T6 dual, decision-rights matrix; the schema lacks sub-strategy and transfer-ledger fields |
| IC ANSWER | Yes | Defensible if labelled synthetic: integrated by design, prices state-dependent, decentralization unproven. Use groups v1.1 figures, not main's stale ones |
| NEEDS ADIC DATA | Yes | Envelope and FTP levels; credibility (years of archive to reach n_eff ≥ 20); transfer history; real authorities and pay. No asset-owner evidence exists |

## 4. Gaps

| Gap | Impact | Close | Detail |
|---|---|---|---|
| Charges and envelopes on the full H | High | build_experiment | Compute charge_i and Λ_g on the 12-quarter H with Phase II and the CVaR, leverage and T6 rows; reconcile gap_01's liquidity-only FTP with gap_04's risk-plus-liquidity FTP |
| PE census and vintage data | High | adic_data | Confirm census v1.1 or supply vintages (groups §9 Q4); re-run T4′, envelopes and gap_04 |
| Calibrating credibility | High | adic_data | Point-in-time forecast archive incl. declined deals; estimate δ from the registry; freeze gates G-A–G-E |
| Which Tier-1 level is priced | Medium | user_decision | The IC states whether FTP is priced at tolerance or at appetite (groups §4.3) |
| Literature refinements | Medium | user_decision | ADRs on: the owner-loss risk row, envelope collars, a haircut on summed risk budgets, no single hurdle, a financing-window state, Lagrangian bounds |
| Decision-rights matrix and pay | Medium | user_decision | Reconcile CF with Tier A and the Board on leverage, and the tail-budget threshold. ADIC's authorities, recusal practice and pay parameters b and s (groups §9 Q10) |
| Stale main synthesis | Medium | more_research | Carry C7, C8, C10, C12 and the census choice into main |
| Decentralization in practice | Medium | build_experiment | Test price-following with private α, non-linear CVaR and playbook slippage on SYN-ADIC-177; shadow-run on ADIC later |
| Group boundaries and schema | Medium | user_decision | Confirm the boundaries between Capital Solutions, Private Credit and Secondaries (§9 Q1–Q2). Add sub_strategy, internal/external counterparty and transfer-ledger fields |
| Gate V2 beyond services | Low | build_experiment | Test netting on PE → Secondaries sales, Capital Solutions lending and recap netting (V24a) |
| Literature usage errors | Low | more_research | Re-run the barrier statistics; fix the recap multiplier and the citations |
