# Q07 (R7) sufficiency audit: the private book with declining PE DPI

*Read-only audit, 2026-10-18. ADIC figures are SYNTHETIC unless marked as market data. **Verdict: mostly_sufficient.***

## 1. Answer today

**The engine is designed well enough. It is not yet built or validated.**

**What the design covers.** The research specifies three engines for the five private groups (00_SYNTHESIS §4.2; groups synthesis §3):
- *Fund interests* (PE funds, secondary funds, closed-end credit funds) run on RFT-TA v2: a regime-switching, factor-driven Takahashi–Alexander model with an effective-age clock.
- *Single companies* (co-investments, continuation-vehicle (CV) stakes, Capital Solutions kickers) run on one enterprise-value (EV) engine.
- *Contractual claims* (Capital Solutions claims, private-credit loans) run on one competing-risks credit engine.

The DPI drought is an exit-window state (open, normal, drought, frozen). In drought, distributions fall and the distribution clock slows; the model starts today in drought, and a scalar Φ covers a permanent decline. Unfunded commitments are a per-position state, with stressed-call rules and an over-commitment limit. Pacing is a corridor-bounded lever priced on the common valuation kernel.

**What it shows on synthetic data.** The direction holds:
- distributions run at about half their normal rate while calls stay sticky;
- the four non-PE groups keep the drought private book cash-positive for every plausible PE vintage history;
- the liquid book still funds the payout;
- PE causes 70–82% of the private book's stressed cash drain;
- pacing is the slow, first-order lever;
- no private group hedges the drought's cash channel.

**What is not settled.** Over-commitment, drought net cash and facility needs move with the PE vintage structure, and the two syntheses currently disagree on that structure. Every number comes from simplified prototypes, not from the engine as specified.

| Value | Meaning | Source | Tag |
|---|---|---|---|
| 9% (H1-26) and 9–11% (2022–25), vs 17–24% (2017–20); calls 27–31% | PE distribution rate vs contribution rate (market data) | 00_SYNTHESIS §7.1; C2 §6 | [S] |
| ≈2.7–3.5× | How far normal-era intensities overstate today's cash (rejected) | 00_SYNTHESIS §4.2 | [C] |
| Distribution multiplier 1.25 / 1.0 / 0.45–0.50 / 0.30–0.35; clock speed 1.2 / 1.0 / 0.6 / 0.5 | By exit window (open, normal, drought, frozen) | 00_SYNTHESIS §4.2 | [I] |
| Drought 0.87; $11.8bn vs $20.7bn | Drought probability today; expected 12-month private distributions vs a normal start (SYNTHETIC) | gap_04 §6.2 | [I-calc] |
| +$2.2bn (census v1.0) / +$3.7bn (v1.1); +$2.6bn to +$5.3bn | 12-month drought net cash of the private book; range over histories passing gate V6 (SYNTHETIC) | 00_SYNTHESIS §2.3(b); groups synthesis §2.2 | [I-calc] |
| −$16.4bn, 70% PE | Private-book cash use in year 1 under the canonical 24-month stress T4′, census v1.0 (SYNTHETIC) | groups synthesis §2.2 | [I-calc] |
| 0.81 → 0.97 (v1.0); 0.75 (v1.1) | (Private NAV + unfunded) / NAV today and after three drought years (SYNTHETIC) | 00_SYNTHESIS §2.3(c); groups gap_02 §0 | [I-calc] |
| $0.67bn / $3.51bn / −$4.38bn | One-year pause in 2027: cash back in year 1, cash back by 2030, net cost to 2040 (SYNTHETIC, v1.1) | groups synthesis §3.1 | [I-calc] |
| 8.6¢ (5.6–12.3¢) | Cost per PE dollar of commitments forgone, model M1 (range across models) (SYNTHETIC) | groups synthesis §3.1 | [I-calc] |
| $13.9bn → $6.1bn | Facility needed under T4′, without and with the stage-triggered pacing cut (SYNTHETIC) | 00_SYNTHESIS §2.3(d) | [I-calc] |
| ≈$0.8–0.9bn | Year-1 run-off of private-credit separately managed accounts (SMAs): the only switchable "natural DPI" | 00_SYNTHESIS §4.2 | [C] |

## 2. Evidence

**Strongest support.**
- **Market calibration (strong).** Stream 04's verifier traced ≈150 numbers to primary PDFs (22 confirmed, 3 corrected, 0 refuted; 04 verify §1). The group streams checked 156 claims (128 / 20 / 0) and rate HIGH on evidence (GC1 §2).
- **Design (medium, repaired).** Stream 04's four must-fixes are applied (C2 §1 V1–V4; main §9.1):
  - fees were counted twice;
  - the alpha runway ran on the drought-slowed clock;
  - the shadow price had the wrong units;
  - an exit-only statistic was applied to unsold inventory.

  R5 (the intensity break at fund end) is fixed by a cap plus a liquidation hazard.
- **Literature (supportive, with refinements).**
  - Factor and stochastic extensions of Takahashi–Alexander have published precedent (Cao et al. 2025; Beutler et al. 2023).
  - Pacing as the slow lever is "supported, refined" (literature synthesis §4.5).
  - No peer-reviewed study of the 2022–26 drought exists (04 lit §1).
- **Prototypes (partial).** None implements the full specification:
  - `rfta_v2_book.py` is a deterministic mean-path RFT-TA v2. It tracks MSCI within ±2pp except in 2019–20, where it runs 4–5pp high.
  - `t1_engine.py` is rate-based.
  - `g04_engine.py` runs simplified stochastic cohorts and reproduces t1 path for path.

**Contradictions.**
1. **Census.** Main v1.1 still uses census v1.0 and headlines "ADIC is already over-committed" (finding 4: ≈81%; PE unfunded/NAV 0.53). Groups gap_02 §1.2 shows that $27.4bn of PE unfunded arises only from vintage histories that fail gate V6, and proposes census v1.1 ($16.4bn). On v1.1 the over-commitment row passes at 0.75 and drought net cash is +$3.7bn. v1.1 is unconfirmed.
2. **Cash released by a pause.** The engines release 66% (RFT-TA v2) or 69% (G1) of forgone commitments within four years, against ≈40% in the Cliffwater/ERSRI check. The groups synthesis calls this gap "open" (groups §8; G1 verify R6). Main still quotes "≈$3.6bn by year 4".
3. **Near-term pacing relief.**
   - Stream 04's literature review infers that pacing gives little near-term relief (Brown et al. 2020).
   - Main §2.4 calls pacing "the most effective single lever" on the red event.
   - The literature's rule of no liquidity credit for a cut for two quarters is not coded: in `t1_engine` a cut lowers unfunded at once, and calls fall from the next quarter.
4. **Crisis calls.** The engine's frozen state uses a call multiplier of 0.8 plus stress calls. The stresses use ×1.25 (S1), ×1.38 (T4′) and ×1.5 (literal T4). The literature suggests 0.8–1.1, and in the GFC buyout calls fell ≈50% from peak to trough.
5. **Prototypes vs specification.**
   - `g04` PE cohorts run on calendar age, not the effective-age clock, and their history fails V6 (groups C19).
   - `t1` and `g04` smooth reported NAV with a 0.5/0.5 two-quarter average, below the specified first-order autocorrelation target of 0.66–0.71.
6. **Evidence tag.** The unfunded half-life of 2.1–2.5 years is tagged [I] in main finding 4 and [C] in groups §3.1.

**Citation-audit items touching Q07** (literature synthesis §2).
- **Changes numbers: barrier shift.** In the co-investment work the Broadie–Glasserman–Kou barrier shift has the wrong sign, and the script applies none. The quoted wipe-out (7.0% → 22.8%) and LTV-breach (50–63%) rates are therefore likely understated; the brief (§7 item 15) marks them provisional.
- **Changes numbers: recap multiplier.** The ×2.4 recap figure belongs to +84% debt (≈×1.1–1.7 at φ = 0.25). The groups synthesis still carries 1.4–3.4.
- **Metadata only:** Luxenberg (ICAIF '22); Sorensen–Wang–Yang, *RFS* 27(7); Nadauld's seller PME 0.976; DOI for Jeet et al. 2026.
- **Attribution:** "smoothing ≈0.5 (BGG)" is stream 04's own derivation, not a BGG figure.
- **Unchecked:** Metrick–Yasuda; check it before the fee fix is coded.

## 3. Readiness

| Level | Met? | Reason |
|---|---|---|
| DESIGN | Yes | Equations, states, regime tables, sourced defaults, validation gates and interfaces exist for all five groups, with verifier fixes applied |
| BUILD | No (nearly) | The fund-interest core is codable from C2 §4.1, with `rfta_v2_book.py` as a reference. Unspecified: exit-factor and regime-duration parameters, mark-gap and quality-drift calibration, the lumpiness law, the pacing MPC. One known barrier bug; no benchmark harness |
| IC ANSWER | Yes, qualified | The direction is robust across histories and models. Levels must be shown on both censuses, labelled as proxy-engine output and SYNTHETIC |
| NEEDS ADIC DATA | Yes | PE commitments and unfunded by vintage set the levels. Also needed: fund cash flows, SMA and wrapper rights, loan tapes, co-investment offer logs, LPA consent terms |

## 4. Gaps

| # | Gap | Impact | Close via | Detail |
|---|---|---|---|---|
| 1 | PE commitments and unfunded by vintage and strategy | High | adic_data | Decide over-commitment, drought sign and level, the T4′ need and group envelopes |
| 2 | Census v1.0 vs v1.1; main synthesis not updated | High | user_decision | Confirm v1.1 or supply data. Then re-run T4′ (not computed on v1.1) and the g04 fans and Shapley values |
| 3 | The specified stochastic RFT-TA v2 is unbuilt | High | build_experiment | Exit factor, mark gap and selection, lumpiness, quality drift, smoothing fitted to the autocorrelation target |
| 4 | Cyclical vs structural share of the DPI decline (Φ, drought-exit hazard) | High | user_decision | Only one drought spell and no academic study. Elicit the IC's prior and put ambiguity on regime persistence |
| 5 | Refit the distribution curve on age × calendar panels | Medium | more_research | The current fit uses a benign end-2019 Cambridge Associates cross-section; use licensed MSCI/Burgiss or Preqin panels |
| 6 | Pause cash release: 66–69% vs ≈40% | Medium | build_experiment | Make calls respond to regime; reconcile to ERSRI |
| 7 | Pacing policy untested | Medium | build_experiment | MPC with the corridor (G1 R3), a de Zwart baseline, Gourier option value, the two-quarter lag, unfunded counted in leverage |
| 8 | Crisis call multiplier | Medium | user_decision | Ratify the T4′ rule, test 0.8–1.1 in the engine, and obtain ADIC's 2008–09 calls |
| 9 | No out-of-sample backtest or benchmark | Medium | build_experiment | Benchmark against Cao 2025 and Beutler 2023; check 80% and 95% interval coverage |
| 10 | Co-investment barrier and recap errors | Medium | build_experiment | Apply the BGK shift (+0.5826σ√Δ) and a recap multiplier of ×1.1–1.7; re-run the statistics |
| 11 | Private-credit PD/LGD split; PIK multiplier ×1.5 vs ×9; Capital Solutions PIK shares (low confidence) | Medium | adic_data | Loan tapes; wrapper rights size the run-off |
| 12 | Literature refinements not adopted | Low | build_experiment | Mark-gap priors; IPO sell-down over 8–16 quarters; β 1.5 sensitivity; heavy tails; regime-dependent smoothing |
