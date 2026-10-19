# G4 barrier-correction re-run: results

*Research addendum for the ADIC multi-period robust TPA framework, 2026-10-18.*

**All model figures here are SYNTHETIC.** They come from the illustrative G4 co-investment engine and are not ADIC data.

**What this note does:**
- It fixes the Broadie–Glasserman–Kou (BGK) usage error flagged in `research/literature/00_LITERATURE_SYNTHESIS.md` §2.4 item 1 and `research/literature/G4_coinvest.lit.md`.
- It re-runs every statistic that depends on a monitored barrier.
- It lists old and new values and every file that quotes them, so that editors can apply the changes.

**No report was edited, and the original scripts were not changed.**

---

## 0. Bottom line

1. **The audit is right about the sign.** To make a quarterly check reproduce a *continuously* monitored down barrier, the barrier must move **toward** the current value: κD·e^{+0.5826σ√Δ}. The dossier's e^{−0.5826σ√Δ} moves it the wrong way, so survival is overstated further (§1).
2. **Only one quoted statistic is a quarterly-checked continuous barrier.** It is the book-simulation write-off rate (dossier E3, V ≤ 0.75D), and it changes:

   | Start regime | Old (SYNTHETIC) | New, BGK-corrected (SYNTHETIC) |
   |---|---|---|
   | Drought | 2.5% a year per position | **3.3%** |
   | Normal | 2.1% | **2.8%** |

   - An independent fine-grid simulation puts the continuous-monitoring value at 3.1% and 2.7%. The corrected quarterly rule is therefore accurate to about 0.1pp (§3–§4).
   - Three-year write-offs rise by about 31%, from 6.7 to 8.8 positions (drought start).
   - Distributions, net cash flow and year-1 yields are unchanged at the precision quoted in GC1, the groups report and the main report.
   - Apart from the write-off rate, two rows of the dossier's §6.3 table change in the last digit: the normal-start net cash flow P90 and the NAV-gap row (§3).
3. **The wipe-out and LTV-breach rates in groups finding 8 are *not* changed by the fix.**
   - **Wipe-out** (7.0% → 22.8% in a drought; 2.1% → 11.8% normal). These are *at-exit* probabilities from calc section 6, with no barrier monitoring at all, so BGK does not apply.
     - Adding the dossier's own E3 barrier as a definitional sensitivity gives 7.6% → 22.9% in a drought and 2.2% → 11.8% normal. The conclusion holds (§5.2).
   - **LTV breach** ("50–63% of quarterly-tested paths": 49.6% / 62.5%; default level 32.7% / 47.9%). These are correct as labelled, because the covenant itself is tested at quarterly NAV dates. Simulating a quarterly test quarterly needs no shift.
     - If the LTV were monitored continuously, the trigger rates would be 62.2% / 73.4% and the default-level rates 42.5% / 57.4%. With monthly tests they would be 54.6% / 67.0% (§5.1).
4. **"Simulate monthly" is not a fix on its own.** Monthly checks without the shift still miss about 13–14% of continuous write-offs and 6–8pp of the trigger probability.

---

## 1. Direction of the correction: first principles and the paper

**The paper.** Broadie, M., Glasserman, P. & Kou, S. (1997), "A Continuity Correction for Discrete Barrier Options", *Mathematical Finance* 7(4):325–349, DOI 10.1111/1467-9965.00035.
- Metadata re-checked on Crossref (`api.crossref.org/works/10.1111/1467-9965.00035`) on 2026-10-18: print October 1997, online 5 January 2002.
- The deposited abstract says "discrete barrier options can be priced with remarkable accuracy using continuous barrier formulas". It continues: "The correction shifts the barrier away from the underlying by a factor of exp(βσ√Δt), where β ≈ 0.5826, σ is the underlying volatility".
- The closed form β = −ζ(1/2)/√(2π) is not in the deposited abstract. It evaluates to 0.5825972 (checked with `scipy.special.zeta`) and is used here only as the numerical value of 0.5826.

**Reasoning for a down barrier B below the current value V₀ (default when V ≤ κD):**
1. **Continuous monitoring** defaults a path when its running minimum over [0, T] reaches B. Dossier E3 defines exactly this: τ_D = inf{t : V_t ≤ κD_t}.
2. **A quarterly check sees V only at quarter ends.** The minimum over quarter ends is never below the true minimum. So every path the quarterly check defaults is also defaulted continuously, but not the reverse: a path that dips below B mid-quarter and recovers is missed. Hence P_quarterly(B) ≤ P_continuous(B), and **quarterly checks overstate survival**. The dossier's sentence is correct.
3. **The fix must make the quarterly test fire more often.** P_quarterly(B′) rises with B′, so the test barrier must be **raised, toward V₀**.
4. **Size of the shift.** BGK show that a discretely monitored barrier B behaves like a continuously monitored barrier at B·e^{−βσ√Δ}, further from the underlying. The reason is that a discrete walk first crosses the barrier with an average log overshoot of about βσ√Δ. Inverting this:

   continuous(B) ≈ discrete(B·e^{+βσ√Δ}),

   so the quarterly simulation should use **κD·e^{+0.5826σ√Δ}**. Here σ is the diffusive volatility of ln V per year and Δ the time between checks in years.
5. **The dossier's e^{−0.5826σ√Δ}** lowers the barrier. The quarterly test then fires even less often, which adds to the bias it was meant to remove.

**Which shift applies when:**

| Real-world event | Evaluated by | Shift |
|---|---|---|
| Continuous barrier (E3 default) | Simulation checked every Δ | Barrier × e^{+0.5826σ√Δ} (toward V) |
| Event tested every Δ (e.g. a quarterly LTV covenant) | Simulation checked every Δ | None |
| Event tested every Δ | Continuous closed-form formula | Barrier × e^{−0.5826σ√Δ} (away from V; BGK's own use) |

**Numerical proof** uses the decision example in calc section 6. There EV is a GBM and net debt is constant, so continuous hitting probabilities have exact closed forms. Normal regime (τ = 2.5y, μ = 6%, σ = 28%); event = 1.5× LTV trigger, i.e. EV ≤ D + ⅔·NAV. SYNTHETIC, 400k paths:

| How the trigger is evaluated | P(trigger) |
|---|---|
| At exit only (calc §6, dossier "29%") | 28.7% |
| Quarterly checks (verifier; published 49.6%) | 49.6% |
| BGK prediction of the quarterly value: continuous formula, barrier × e^{−βσ√Δ} | 49.0% |
| Monthly checks | 54.6% |
| Weekly checks | 58.4% |
| 312 checks a year | 60.6% |
| Continuous, extrapolated from monthly / weekly / 312 (√Δ law) | 62.1% |
| **Continuous, exact closed form** | **62.2%** |
| **Quarterly checks, barrier × e^{+βσ√Δ} (the fix)** | **62.3%** |
| Quarterly checks, barrier × e^{−βσ√Δ} (dossier formula) | 38.2% |

The "+" shift on a quarterly check reproduces continuous monitoring. The "−" shift on the continuous formula reproduces the quarterly check. The dossier's version moves away from both. The drought regime gives the same picture: quarterly 62.5% (published), quarterly with "+" 73.3%, exact continuous 73.4%, quarterly with "−" 52.3%.

---

## 2. Inventory of barrier-type statistics

I grepped every `.py` file under `research/groups` for "0.5826", "barrier", "wipe", "LTV", "kappa" and "write-off". I also checked the verifier and GC1 scratchpad scripts that the reports cite.

| # | Statistic (script) | How it is monitored | Real-world event | BGK fix applies? | Outcome |
|---|---|---|---|---|---|
| 1 | Book-simulation write-offs, V ≤ 0.75D: rate per position-year, 3-year count, written-off cost share (`groups/verification/G4_coinvest_calcs.py` §7, step 3) | Quarter ends; **no correction** | Continuous (E3) | **Yes** | **Changed** (§3) |
| 2 | Book-simulation cash flows, NAV and yields (same §7) | Depend on #1 | — | Indirectly | Unchanged at quoted precision, except two dossier rows (§3) |
| 3 | Single-asset facility: P(1.5× LTV trigger) 49.6% / 62.5%; P(2× default level) 32.7% / 47.9% (verifier `scratchpad/g4v_scripts/check_decisions.py`) | Quarter ends | Covenant tested at quarterly NAV dates (GC1 D14: "tested path-wise on lagged reported NAV") [I] | **No** | Unchanged; continuous and monthly bounds added (§5.1) |
| 4 | LEVER wipe-out, unlevered → levered: 2.1% → 11.8% and 7.0% → 22.8% (calc §6 `p_wipeout`, `p_residual_zero`) | At exit only; no barrier | — | **No** (not a barrier statistic) | Unchanged; E3 sensitivity added (§5.2) |
| 5 | REFI "29–37%" (calc §6 `p_nav_down_33pct_at_exit`) | At exit only | — | No | Unchanged by this fix. Already superseded by #3 (verification R2) |
| 6 | gap_04 group engine: co-investment write-off V < 0.85D (`groups/addenda/gap_04_calcs/g04_engine.py`, line 978) | Quarter ends; **no correction** | Continuous (same E3 logic) | Yes, in principle | **Not re-run** (§6.3) |
| 7 | NAV-facility LTV caps of 5% / 10% with forced paydown (G7, GC2, gap_01, gap_04 engines) | Model step | Contractual cap, applied mechanically | No | Not affected |

**Not affected:**
- Calc sections 1–6 contain no monitored barrier. The corrected script's full output equals the published JSON in every section except 7.
- `gc1_reconcile.py` (GC1 §8) computes no barrier statistic.
- The `G10_calcs`, `G11_calcs` and `G13_calcs` folders that appeared during this run were empty.

---

## 3. Book-simulation re-run (calc section 7): old vs new

**Set-up.**
- Same seeds and 2,000 paths as the published run.
- Section 7 draws its random numbers in fixed shapes, so the corrected run uses *exactly* the published random numbers. Every difference comes from the barrier rule alone.
- Fix: write off when V ≤ 0.75·D·e^{+0.5826·σ_V·√0.25}, with σ_V = √((β_A·σ_m,regime)² + σ_id²) the diffusive EV volatility.
- Resulting effective κ by regime: 0.814 (open), 0.816 (normal), 0.818 (drought), 0.835 (crisis).
- The published run is reproduced exactly. The verbatim copy matches every value in the published JSON (0 mismatches), and the corrected copy run with `BARRIER_MODE = "none"` equals the original.

**Table 3. SYNTHETIC $18bn book, 90 positions, 12 quarters.** Rows are the values the reports quote, at the precision they quote them.

| Metric | Drought start, old | Drought start, new | Normal start, old | Normal start, new | Changes as quoted? |
|---|---|---|---|---|---|
| **Write-off rate per position-year** | 2.5% | **3.3%** | 2.1% | **2.8%** | **Yes** |
| Write-offs over 3 years, mean (P10/P50/P90) | 6.74 (1/4/15) | **8.81 (1/6/19)** | 5.66 (1/4/12) | **7.39 (1/5/16)** | Not quoted |
| Written-off cost ÷ (initial NAV + new calls) | 5.8% | **7.5%** | 4.7% | **6.1%** | Not quoted |
| Distributions over 3 years, mean (P10/P50/P90), $bn | 9.2 (3.6/8.4/16.0) | 9.2 (3.6/8.4/16.0) | 11.7 (5.4/11.0/18.6) | 11.7 (5.4/11.0/18.6) | No |
| Calls over 3 years, mean, $bn | 5.8 | 5.8 | 6.7 | 6.7 | No |
| Net cash flow over 3 years, mean (P10/P90), $bn | +3.4 (−1.3/+9.4) | +3.4 (−1.3/+9.4) | +5.0 (−0.4/**+11.4**) | +5.0 (−0.4/**+11.3**) | **Yes (normal P90)** |
| Net cash flow if drought all 12 quarters (21% of paths) | +1.6 (P10 −1.8) | +1.6 (P10 −1.8) | n/a | n/a | No |
| Year-1 distribution yield, mean (P10/P90) | 12.4% (4.3/22.6) | 12.4% (4.3/22.6) | 19.3% (8.7/31.3) | 19.3% (8.7/31.3) | No |
| Recap dividends ÷ exit proceeds | 3.6% | 3.6% | 3.6% | 3.6% | No |
| P(exit > next-to-last mark) | 0.72 | 0.72 | 0.74 | 0.74 | No |
| Reported vs economic NAV gap, P10/P50/P90 | −18.5/−3.5/+21.9% | **−18.5/−3.6/+21.5%** | −18.7/−3.0/+19.2% | **−18.8/−3.1/+19.3%** | **Yes** |

Raw values:
- Write-off rate 0.02504 → 0.03305 (drought) and 0.02122 → 0.02793 (normal).
- Normal-start net cash flow P90 11.356 → 11.302.

**Why cash flows barely move.** The barrier sits below face value: κ·factor ≈ 0.82 < 1. A newly written-off position therefore already has zero equity. Writing it off removes only its option to recover, which is worth little over 3 years.

**Sensitivities** (same seeds; rates for drought / normal start):

| Variant | Write-off rate |
|---|---|
| σ also includes Kou jump variance | 3.4% / 2.9% (over-corrects; see §4) |
| Dossier's printed sign, e^{−…} | 1.9% / 1.6% |

The full corrected output, all sections, is in `G4_coinvest_calcs_bgk_results.json`.

---

## 4. Independent fine-grid check

**Set-up** (`fine_grid_book.py`):
- Same section-7 model and parameters (imported from the verbatim copy).
- EV is stepped 78 times a quarter, with sub-step increments whose quarterly sums have the original distribution. Each Kou jump falls at a uniformly drawn sub-step, and debt amortises per sub-step.
- 8,000 paths per start regime, on seeds independent of the published run.
- All monitoring rules run on the **same** random numbers. Recaps, follow-ons, exits, marks and deployment stay quarterly.

**Table 4. Write-off rate per position-year (SYNTHETIC; level SE ≈ 0.04pp).** The last column is the paired, common-random-number difference from the finest grid; its SE is ≈ 0.005pp.

| Monitoring rule | Drought start | Normal start | Paired difference vs 312/yr (drought; normal) |
|---|---|---|---|
| Quarterly, κD (original rule) | 2.44% | 2.10% | −0.60; −0.52pp |
| **Quarterly, κD·e^{+βσ√¼} (fix)** | **3.22%** | **2.76%** | +0.18; +0.15pp |
| Quarterly, κD·e^{−βσ√¼} (dossier sign) | 1.85% | 1.58% | −1.19; −1.04pp |
| Monthly, κD | 2.70% | 2.31% | −0.35; −0.30pp |
| Monthly, κD·e^{+βσ√(1/12)} | 3.16% | 2.72% | +0.12; +0.10pp |
| Weekly, κD | 2.91% | 2.50% | −0.13; −0.12pp |
| 312 checks a year, κD | 3.04% | 2.62% | 0 |
| **Continuous limit** (least-squares fit in √Δ over monthly, weekly and 312/yr) | **3.12%** | **2.68%** | +0.08; +0.07pp |

**Reading:**
- The uncorrected quarterly rule is about 22% below continuous monitoring, and the dossier's sign about 41% below.
- The corrected quarterly rule is within +0.10pp (drought) and +0.08pp (normal) of the continuous limit, about 3% high. The small overshoot comes from the jumps and the regime-dependent volatility, which BGK's Brownian setting does not cover.
- Rescaled to the published seeds (continuous ≈ 1.28 × the quarterly rule), the continuous-monitoring rates are ≈ 3.2% and 2.7%, against 3.3% and 2.8% from the corrected script.
- Written-off cost share (drought / normal): quarterly 5.6% / 4.6%; fixed 7.3% / 6.0%; continuous limit 7.1% / 5.8%.
- Three-year write-off count: fixed 8.58 / 7.31; continuous 8.33 / 7.11.

---

## 5. Decision example (calc section 6 inputs)

`check_decisions_bgk.py` uses NAV $400m, nowcast 97%, net debt 6.0× at 14× EV, and 400k paths. "Exact" means closed form. The verifier's original `run()` is kept and reproduces the published figures.

### 5.1 Single-asset facility covenant: 15% LTV, trigger at 1.5×, default level at 2×

| SYNTHETIC | Trigger, normal | Trigger, drought | Default level, normal | Default level, drought |
|---|---|---|---|---|
| At exit only, exact (dossier "29–37%") | 28.7% | 37.5% | 19.8% | 29.2% |
| **Quarterly tests (published; unchanged)** | **49.6%** | **62.5%** | **32.7%** | **47.9%** |
| Monthly tests | 54.6% | 67.0% | 36.4% | 51.7% |
| Continuous, exact | 62.2% | 73.4% | 42.5% | 57.4% |
| Quarterly with the "+" shift (≈ continuous) | 62.3% | 73.3% | 43.0% | 57.8% |
| Quarterly with the dossier's "−" shift | 38.2% | 52.3% | 24.2% | 38.9% |

**Recommendation.** Keep "50–63% of quarterly-tested paths" (49.6% / 62.5%; default level 32.7% / 47.9%). The statistic models a quarterly covenant test correctly, and the BGK fix does not apply to it. If a report wants the probability that LTV ever crosses 1.5× during the loan's life, quote 62–73% (continuous) and say so.

The separate caveat from verification R2 still stands and is not changed here: tests on lagged, smoothed reported NAV would give lower rates than tests on economic equity.

### 5.2 LEVER wipe-out (12% holdco PIK, 25% LTV)

| SYNTHETIC | Normal, unlevered | Normal, levered | Drought, unlevered | Drought, levered |
|---|---|---|---|---|
| **At exit (calc §6; published; unchanged)** | **2.1%** | **11.8%** | **7.0%** | **22.8%** |
| Exact at-exit value (closed form) | 2.11% | 11.85% | 6.96% | 22.87% |
| With E3 barrier V ≤ 0.75D at any time, exact | 2.16% | 11.85% | 7.55% | 22.93% |
| With E3, quarterly check, no shift | 2.12% | 11.83% | 7.17% | 22.91% |
| With E3, quarterly check with "+" shift | 2.16% | 11.83% | 7.55% | 22.95% |

**Recommendation.** No change is required by the BGK fix. Label the figures "at exit".
- For E3-consistent figures, use **2.2% → 11.8% (normal)** and **7.6% → 22.9% (drought)**.
- The PIK still about triples drought wipe-out risk (×3.0 rather than ×3.3), so the conclusion against asset-level LEVER is unchanged.
- The published 11.8% and the closed-form 11.85% differ only by Monte Carlo noise.

---

## 6. Where the values are quoted (for editors)

### 6.1 Values that change

| File : line | Current text | Replace with (SYNTHETIC) |
|---|---|---|
| `groups/dossiers/G4_coinvest.md:425` (§6.3 table) | Write-off rate per position-year: 2.5% / 2.1% | **3.3% / 2.8%**. Footnote: quarterly check with the BGK shift; continuous-monitoring check 3.1% / 2.7% |
| `groups/dossiers/G4_coinvest.md:422` (§6.3) | Net cash flow … +$5.0bn (−0.4 / **+11.4**) | +$5.0bn (−0.4 / **+11.3**) |
| `groups/dossiers/G4_coinvest.md:428` (§6.3) | Reported vs economic NAV gap: −18.5 / −3.5 / +21.9% and −18.7 / −3.0 / +19.2% | **−18.5 / −3.6 / +21.5%** and **−18.8 / −3.1 / +19.3%** |
| `groups/dossiers/G4_coinvest.md:555` (§6.8 item 9) | "against the simulated 2–2.5% a year" | "against the simulated ≈2.8–3.3% a year" |
| `groups/dossiers/G4_coinvest.md:595` (§7 pitfall) | "Apply the Broadie–Glasserman–Kou shift (barrier × e^{−0.5826σ√Δ}) or simulate monthly." | See §7 below |
| `groups/verification/G4_coinvest.verify.md:195` (R14) | "simulated write-off rate (2.1–2.5% a year) is about double KS's 1.2% a year" | "simulated write-off rate, after the BGK fix (2.8–3.3% a year), is about 2.3–2.8× KS's 1.2% a year". This strengthens R14 |
| `groups/clusters/GC1_private_groups.md:163` (spec card E3) | "a barrier V ≤ κD, monitored monthly or with a Broadie–Glasserman–Kou shift" | "…checked at step Δ against κD·e^{+0.5826σ√Δ} (shifted toward V), or at weekly or finer steps". Monthly checks alone still understate write-offs by ≈13–14% |

**Optional wording, same logic:**
- `groups/01_GROUPS_SYNTHESIS.md:549` ("plus a barrier at V ≤ κD").
- `00_SYNTHESIS.md:708` ("write-off at V ≤ κD").

Either can append "monitored continuously (quarterly checks use κD·e^{+0.5826σ√Δ})".

### 6.2 Values that stay as they are (the BGK fix does not touch them)

**Section-7 cash flows**: Y1 yields 12.4% / 19.3%; distributions $9.2bn (P10 3.6); net +$3.4bn (P10 −1.3). Quoted in:
- `G4_coinvest.md:77, 420–424, 426–427`
- `GC1_private_groups.md:27, 165`
- `01_GROUPS_SYNTHESIS.md:550`
- `groups/addenda/GS_calcs/gs_group_cashmap.py:49–50`, which uses 0.193 / 0.124; still correct to 3 decimals.

**Quarterly-tested covenant breach** (49.6% / 62.5%, "50–63%"; default level 32.7% / 47.9%). Quoted in:
- `G4_coinvest.verify.md:32, 130–131, 216–218`
- `GC1_private_groups.md:34, 168`
- `01_GROUPS_SYNTHESIS.md:145, 567`
- `00_SYNTHESIS.md:846`
- `research/addenda/gap_01.md:28`
- `sufficiency/Q06_challenge.md:9`

Keep these; optionally add "62–73% if monitored continuously".

**Wipe-out at exit** (2.1% → 11.8%; 7.0% → 22.8%). Quoted in:
- `01_GROUPS_SYNTHESIS.md:144, 568`
- `GC1_private_groups.md:34, 169`
- `00_SYNTHESIS.md:131, 846`
- `G4_coinvest.verify.md:136–139, 223`
- `G4_coinvest.md:497`
- `research/addenda/gap_01.md:28, 71`
- `sufficiency/Q06_challenge.md:9`

Keep these, labelled "at exit". The E3-consistent alternative is 2.2% → 11.8% and 7.6% → 22.9%.

**Terminal REFI "29–37%" and LEVER "12% to 23%"** (`G4_coinvest.md:82–83, 492`). These are not barrier statistics. They are already wrong for other reasons (verification R2 and R3) and are not changed by this fix.

**Text that called these figures provisional** can now say they are re-checked:
- `design/00_DESIGN_BRIEF.md:444` (§7 item 15)
- `sufficiency/Q03_audit.md:76`
- `sufficiency/Q06_audit.md:34–35, 92`
- `sufficiency/Q07_audit.md:74, 102`
- `sufficiency/Q08_audit.md:33, 61`
- `sufficiency/Q14_audit.md:68`
- `literature/00_LITERATURE_SYNTHESIS.md:27, 132–135`

Suggested wording: "the sign error is confirmed. The affected statistic is the book-simulation write-off rate (2.1–2.5% → 2.8–3.3%). The finding-8 wipe-out (at exit) and quarterly-tested LTV-breach rates are unaffected."

Note that Q07's "Apply the BGK shift (+0.5826σ√Δ)" is the correct direction.

### 6.3 Related site not re-run: gap_04

- **The code.** `groups/addenda/gap_04_calcs/g04_engine.py:978` writes off a co-investment when `co_v < 0.85 * co_d`, checked quarterly with no correction.
- **The equivalent barrier.** With σ_V ≈ 0.28 a year in calm quarters (β_A 0.9 × 0.07 quarterly market SD, σ_id 0.25), the BGK-equivalent barrier is ≈ 0.92·D in calm quarters and higher in crisis.
- **What it affects.** gap_04 quotes no write-off statistic. The bias reaches its outputs only through lost recovery options and the linked private-credit overlap defaults (`pc_loss`).
- **Why it was not re-run.** A full re-run of the multi-stage gap_04 pipeline (10,000 paths, several stages) is out of scope for this step.
- **Recommendation.** The gap_04 owner should apply the same one-line shift (κ·e^{+0.5826σ_V/2}) at its next re-run.

---

## 7. Proposed replacement for the dossier's §7 pitfall bullet

> Discrete barrier monitoring overstates survival. A continuously monitored default barrier (E3) simulated at step Δ should be checked against **κD·e^{+0.5826σ√Δ}**: Broadie–Glasserman–Kou (1997), applied in reverse, which moves the barrier toward the current value. Here σ is the diffusive EV volatility. Alternatively, simulate at weekly or finer steps. Monthly checks without the shift still miss ≈13–14% of write-offs. The opposite shift, e^{−0.5826σ√Δ}, is BGK's own use: evaluating a discretely tested event, such as a quarterly covenant test, with a continuous formula. A covenant tested quarterly and simulated quarterly needs no shift.

---

## 8. Caveats

1. **BGK assumes Brownian motion between checks.** Section 7 also has Kou jumps, regime-switching volatility, and quarter-end debt jumps from recaps and follow-ons.
   - Using the diffusive σ is the better choice. Including jump variance moves the result further from the fine-grid limit (3.4% against 3.1%).
   - The residual error of the corrected quarterly rule is ≈ +0.1pp.
2. **The higher write-off rate widens verification issue R14.** The rate is now 2.3–2.8× Kaplan–Strömberg's ≈1.2% a year default rate. The Weibull exit hazard is fitted to all-cause exits, bankruptcies included, so the case for cause-specific hazards and a recalibrated κ or ICR hazard is stronger. That recalibration is a model-owner decision and was not made here.
3. **Monte Carlo error.**
   - Published-seed results have about 0.07pp sampling SE on the write-off rate. Corrected-minus-old differences use common random numbers and are exact for the given draws.
   - Fine-grid levels have ≈0.04pp SE; paired differences ≈0.005pp.
   - Decision-example probabilities have ≈0.08pp SE at 400k paths.
4. **All figures are SYNTHETIC illustrations from stylised parameters.** None are ADIC data.

---

## 9. Files and reproduction

All files are in `research/groups/addenda/G4_barrier_rerun/`. Run each with `C:\users\dean\ai_envs\adic_tpa_lab\.venv\Scripts\python.exe -I <script>` (Python 3.12.15, numpy 2.5.4, scipy 1.18.1).

| File | Content | Run time |
|---|---|---|
| `orig/G4_coinvest_calcs.py`, `orig/check_decisions.py` | Verbatim copies. They reproduce the published JSON (0 mismatches) and 49.6 / 62.5 / 32.7 / 47.9% | 165 s; < 1 s |
| `G4_coinvest_calcs_bgk.py` → `G4_coinvest_calcs_bgk_results.json` | Corrected copy: section 7, step 3 only. `BARRIER_MODE` = `none` / `bgk` / `bgk_wrong_sign`; `BGK_SIGMA` = `diffusive` / `total` | 167 s |
| `run_section7_variants.py` → `section7_variants_results.json` | Section 7 under the original, fixed, total-σ and wrong-sign rules, on the published random numbers, plus reproducibility checks | 19 s |
| `fine_grid_book.py [n_batches]` → `fine_grid_book_results.json` | Independent fine-grid check (§4); run with 4 batches | 248 s |
| `check_decisions_bgk.py` → `check_decisions_bgk_results.json` | Decision example: closed forms, BGK in both directions, fine grid, E3 wipe-out sensitivity (§1, §5) | 11 s |
| `compare_old_new.py` → `old_vs_new.json` | Old vs new at quoted precision (§3, §5) | < 1 s |

The original scripts (`groups/verification/G4_coinvest_calcs.py` and the verifier's scratchpad `check_decisions.py`) were not modified.
