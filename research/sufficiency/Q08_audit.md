# Q08 audit: is the SELL / HOLD / REFINANCE / LEVER lens fully specified? (R8)

Research-sufficiency audit, 2026-10-18. Read-only review of the corpus. Every ADIC figure below is **SYNTHETIC**: it comes from the working allocation, census v1.0 and proxy models, never from ADIC data. Tags follow main §0: [S] sourced, [C] corrected by a verifier, [I] inference or default, [I-calc] synthetic arithmetic.

**Verdict: mostly sufficient.** The lens is ready to design and nearly ready to build. The IC can get a qualified answer today. Calibration needs ADIC's data.

## 1. Answer today

Yes, at design grade. The research defines the lens for every group and for Corporate Finance (CF), and values every action with one rule.

- **By group.** Two documents state, for each group × action, the instrument, pricing rule and defaults, time to cash, regime availability, consents and encumbrance:
  - a 17-row instrument library (`00_SYNTHESIS.md` §4.4, taken from gap_01 §3);
  - seven group specifications (`groups/01_GROUPS_SYNTHESIS.md` §3.1–3.7). The Overlay gets a full matrix of 3 books × 4 actions (§3.7).

  Control rights decide which actions exist. Continuation-vehicle elections are GP-triggered events, single-asset co-investment REFINANCE is inadmissible, and transfers between ADIC groups raise no liquidity.
- **By asset.** Positions carry consent, ROFR and pledge flags, a lead time and a feasibility flag (groups §1 finding 2, §3.0). The first stage of H, the here-and-now optimizer, is asset-level (main §4.8). Each holding gets a generated card showing its reservation price, break-even ℓ, P(best), regret and a `priced_on` flag (main §4.4).
- **One valuation rule.**
  - Every action combines an exposure decision and a financing decision, so LEVER ≡ ADD + REFINANCE, which is used as a test.
  - All actions are priced on one kernel, π = p·m·∏(1+ℓ)⁻¹. The liquidity premium ℓ comes from the duals of every constraint row that contains cash; m is a market-risk deflator.
  - Each action is scored by its full reduced cost (main §4.4; C2 §3.2–3.3), which fixes dossier 08's errors R2 and R3 [C].
  - Duals are read only from the restored problem (Phase II). Phase I first finds the minimum violation using reversible levers only, with no PE fire sales.
  - Group envelopes and decision prices come from the same solve (main §4.8, L15; groups §4.3–4.8).

| Result (SYNTHETIC) | Value | Source · tag |
|---|---|---|
| Why Phase I matters | A penalty-pinned dual makes every fund a SELL at a 0.9% reservation price. After restoration the price is 76.8% | gap_02 §4 · [I-calc] |
| Liquidity price at t0 | μ = 0.243 per $ of month-24 headroom with group levers only (R0); 0.0113 with the revolver signed (R1) | groups §4.8 · [I-calc] |
| Cards flip on the revolver | PE card at an 88% bid: reservation price 70.6% → SELL (R0), 90.7% → HOLD (R1). Secondaries: 75.2% → 90.9%. Hurdles fall from 3.0–5.0% to 0.13–0.97% a year | groups §4.8 · [I-calc] |
| Lever cost, PV per $ of T4′ headroom (T4′ = the canonical 24-month stress) | Revolver 1.1%; SMA run-off 4.8%; SMA sale 5.4%; NAV facility 7.0%, capped by pledges at ≈$2.1bn; pacing cut 21.9% | groups §2.3 · [I] |
| REFINANCE vs SELL | A NAV loan beats a sale only if repaid within ≈2 years | main L6, §4.4 · [C] |
| LEVER | Needs financing at ≲ SOFR + 300bp; never optimal at SOFR + 480bp | 08 verification log R4 · [C] |
| Physical-to-synthetic (P2S), cost per $ freed a year | 0.40–0.70% normal, 2.2–3.3% in stress. A $5bn conversion carries $1.65bn of VM in a −33% month | main §4.4 · [I-calc] |
| Co-investment LEVER | A 12% holdco PIK raises drought wipe-out from 7.0% to 22.8% | groups §3.4 · [C], provisional (§2) |
| Worked SELL example | SELL advantage $3.3m, not $10.75m; reservation price 87.3% | main §4.4 · [C] (toy) |

The research *proposes* this lens and runs its parts on proxy models. It does not yet *show* that the lens works on a book of individual holdings.

## 2. Evidence

**Strongest support**
- **Dossier 08's verification log.** Of 33 claims, 29 were confirmed, 3 corrected and none refuted. The script reproduces its results byte for byte. Main §4.4 and C2 apply the log's fixes R1–R4.
- **Group dossiers G1–G9.** Of 289 claims, 245 were confirmed, 32 corrected and none refuted (groups §0).
- **Prototypes.**
  - `test_no_pinned_duals.py` passes 8/8 and the group version 18/18. They test penalty invariance, catch pinned cards and check the KKT spare-lever cap.
  - Envelopes and FTP charges were computed on a reduced H over 10 replications (groups gap_04 §5).
- **Literature.** It supports one state-contingent λ plus envelopes (lit §1, §4.6), and found no hallucinated citations in stream 08 (34 of 35 found).

**Limits.** The Phase-I block is a linearised single-scenario LP, and the reduced H is a one-year LP, "not H itself" (groups gap_04 §9). Price decomposition has been tested on only 40 synthetic assets. Most defaults are [I].

**Contradictions between files**
1. **Revolver credit.** The canonical T4′ convention credits the revolver at 80% (main §2.3(d), groups §2.3, the reduced H). The literature and brief §7.2 cut it to ≤ 50% in the joint oil–crisis state and to zero for new facilities (lit §4.3). This is load-bearing: T4′'s $13.9bn facility need, the R1 duals and the HOLD flips all use 80%. Once the $15bn market cap binds, μ jumps 4–5× (groups §4.8).
2. **NAV-facility availability in a crisis.** Main §4.4 gives 50%; C2 §4.3(d) says the market closes.
3. **Secondaries deployment gate.** Main §4.4 still requires CFP stage Green or Amber; groups v1.1 (C7) allows any stage but Black.
4. **Co-investment SELL lag.** Main §4.4 gives 3–9 months; groups §3.4 gives 3–6.
5. **Recourse waterfall.** The literature contradicts P's fixed waterfall, which P's SELL screen inherits (lit §4.4).
6. **Price decomposition.** Main calls it a heuristic only (§4.8). The literature says Lagrangian bounds exist whose gap does not grow, and asks for them to be published (lit §4.6).
7. **Hedge-fund alpha.** Priors of 0.5–2.0% (groups §3.5) against the literature's α ≈ 0 (lit §4.11). The priors drive the redemption rule.
8. **Tagging.** Main tags the 40-asset toy test [S].

**Citation-audit errors touching this question** (lit §2.4)
- **Co-investment barrier (item 1).** The sign of the Broadie–Glasserman–Kou correction is reversed, and the script applies none. Breach rates (49.6% and 62.5%) and wipe-out rates are therefore understated; they are to be re-run (brief §7.15). This only strengthens the inadmissibility conclusion.
- **Bhardwaj–Gupta–Howell (item 2).** The ×2.4 was misapplied; use ×1.1–1.7. This moves the post-recap distress multiplier.
- **Li–Strahan–Zhang (item 14).** The 2020 line draws had Fed support, which an oil–fiscal stress may lack. This bears on revolver reliability.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | **Yes** | Every group × action is specified, and one kernel, score, Phase I and envelope rule ties them together, with the logs' corrections applied |
| BUILD | **Not yet (nearly)** | The formulas, tests T1–T5 and prototypes can be coded now (main §10). Still needed: decisions (ADRs) on the facility convention, the T6 dual and the kernel, plus about seven missing lags or terms |
| IC ANSWER | **Yes, qualified** | The IC can see the lens, the rule and synthetic results with `priced_on` flags and ranges. It cannot get asset-level recommendations, and the card flips are provisional |
| NEEDS ADIC DATA | **Yes** | Bids and ADIC's own sale-failure rate, LPA consents, hedge-fund terms τ, PE unfunded by vintage, Private Credit wrapper rights and loan tapes, offer logs, CSAs, facility indications and term sheets (main §9.2 item 4) |

## 4. Gaps

| # | Gap | Impact | Close by |
|---|---|---|---|
| 1 | Revolver credit (80% vs ≤ 50%) and a ≈1.1pp tightening premium on REFINANCE and LEVER hurdles are undecided. T4′, the duals and the cards must then be re-run | High | user_decision |
| 2 | No end-to-end run asset by asset: the full H (12-quarter MILP, selection loop, dual bands) is not built. The worst-case decomposition gap grows ≈7× at ~20 rows (08 log R10) | High | build_experiment |
| 3 | The census is unconfirmed. T4′ on v1.1 is not computed; envelopes, cards and PE fans need re-running (groups C6, C19, C21) | High | adic_data |
| 4 | [I] pricing defaults need calibration: hedonic model, execution copula, success rates, capacity, preferred equity at 12% (no 2026 benchmark, C2 §4.3(f)), pool spreads | High | adic_data |
| 5 | Pricing once T4′ goes slack under Mix A or B: the T6 CVaR dual in H is still open (groups §4.4) | Medium | build_experiment |
| 6 | Which kernel governs if utility-implied and CMA-implied risk prices diverge (C2 test T3; main §9.3 Q7), and whether the risk row comes from the owner's loss function (lit §3.5) | Medium | user_decision |
| 7 | Literature refinements await decisions: λ split by binding row; regime-conditional prices and a financing-window state; the 9/9/4 fallback only where the payout binds; the LEVER interaction term (the identity held by construction, 08 log R4c); waiting values under incomplete markets | Medium | build_experiment |
| 8 | Cells without numbers: Secondaries REFINANCE lag and regimes; co-investment pool and holdco lags; Capital Solutions back-leverage lag; Private Credit lender lead time; hedge-fund unit-loan pricing; TRS terms; revolver lead time | Medium | more_research |
| 9 | Permitted instruments and group boundaries (main §9.3 Q6; groups §9) | Medium | user_decision |
| 10 | Co-investment barrier statistics are provisional | Low | build_experiment |
| 11 | Re-run with the reconciled overlay convention (groups C18) | Low | build_experiment |
