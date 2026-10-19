# Q02 challenge: robust scenario-analysis design (R2)

- **Date:** 2026-10-18. **Role:** adversarial skeptic of `Q02_audit.md`.
- **Tags:** as in 00_SYNTHESIS §0. Scenario figures are SYNTHETIC (stylised proxies on the working book) unless they are marked as public data.
- **Revised verdict: PARTIAL** (the audit said mostly sufficient).
  - DESIGN: upheld.
  - BUILD: still no, and not close.
  - IC ANSWER: downgraded. The corpus itself contradicts the audit's proxy numbers.

## 1. Number checks

All ten values are where the audit cites them. Three need caveats.

| Value | Found at | Caveat |
|---|---|---|
| 3–4pp vs ≈0.2pp | 00_SYNTHESIS §1, finding 2 [C] | — |
| Book 6.2–9.7%; P(5y≥10%) 27–51%; P(5y<7%) 31–55%; KL 0.02–0.06 | §7.1; verify-10 claim 6, §6 [C] | Only the fee basis was corrected. The convention still overstates P(5y<7%) by ≈3pp (verify-10 R7), and the 51% belongs to the 10.15% book, not the 9.7% one. |
| η 0.05, η_L 0.01, radius 0.5pp; 1.73% | §4.10; C1 §5.11, D11–D12 | — |
| 50k paths; SE ≈0.10pp | §4.1; C1 §7; verify-10 claim 17 | — |
| θ\* 0.76, G\* $11.1bn; pooled 0.79 | gap_02 §1.2; groups synthesis §2.4 [I-calc] | $14.6bn is the pooled *facility need*, not G\* |
| $13.9bn / $6.1bn / $0 | gap_02 §1.3 [I-calc] | See §2b |
| M6 floor 2.4% (CP 2.5%) | gap_02 §0, §2.3 [I-calc] | Superseded (§2a) |
| Calm ≥0.99; F 0.10; D 0.87; GW ≈0.85; $9.9–10.8bn | gap_04 §1, §4.2, §6.2 | Public data; GW elicited [I] |
| $111 vs $84; 49% vs ≈17% | gap_04 §6.2 | — |
| −0.14 / +0.43 / +0.32 | C3 §6; dossier 03 §4.1 [I-calc] | See §2f |

## 2. Where the audit overstates

**a. The M6 "floor" and the model-class T6 bands are engine artefacts.**
- Groups gap_04 §2 reruns the same M1–M6 proxies with group playbooks switched on:
  - do-nothing P(red) falls from 8.2 / 21.2 / 37.3% to 1.6 / 6.3 / 14.5% (M1 / M4 / M6);
  - Mix B in M6 falls from 6.4% to 0.09%. That run assumes no slippage, so 0.09% is optimistic.
- Its conclusion: the 2.4% floor is "a property of its playbook-free engine". Groups synthesis §2.4 says to re-certify before relying on it.
- 00_SYNTHESIS was saved at 15:08, before groups gap_04 (16:53). It still carries finding 6, the §4.9 bands and §9.2 item 13 ("enters recovery today").
- The audit repeats these figures with no caveat, although §9.2 item 10 bars results from IC use until a single engine replicates them.

**b. The stress conventions conflict with the literature.**
- *Facility credit.* s\* credits revolvers at 80% (gap_02 §1.1; the engine uses 0.80–0.90). Literature §4.3 and brief §7 item 2 allow at most 50% in the joint oil–crisis state, which is where s\* starts.
  - Facility need = G\*/credit (11.1/0.8 = 13.9).
  - At 50%, that gives ≈$22bn [my arithmetic; SYNTHETIC], above the "realistic" $10–15bn (§9.2 item 12).
- *Owner band.* `t1_engine.py` grants the band whenever it is triggered. Literature §4.2 rates the band contested, so the "$0" figure needs advance written agreement (brief §7 item 3).
- *Recourse order.* The engine's waterfall is fixed. Literature §4.4 rates a fixed order contradicted.

**c. θ\* rests on a superseded state.**
- The engine uses C3's *prior* P^Z, whose stationary shares miss C3's own targets (N 49%, DB 7%; C3 §5.1a).
- Its first-year draw is ≈7.75% (a 7.5% start, targeting 8% in GW). gap_04 §6.2 puts it at 5.6–6.1%.
- It starts from Z₀ = GW at 0.7, not from the G2-frozen state. That state alone moves P(red) by 2–6pp (groups gap_04 §2, step S1).

**d. The build is not close.**
- *Brent.* The two-factor model appears only as an initialization rule (§4.1). The only dynamic equation is C3 §5.1(b)'s one-factor form, and no Schwartz–Smith parameters exist.
- *Exit window.* Its transitions are given in form only (C2 §4.1). The drought-exit hazard is an open question (C2 §9.1 item 4).
- *Rare-event bound.* C1 D12 pairs Clopper–Pearson with importance sampling, but CP assumes unweighted draws. No weighted bound is given.
- *Red team.* It has no defined `plausibility_class` (dossier 12, ScenarioSpec). Its GW→SG→DB benchmark has never been computed.
- *C1 is stale.* C1 §6 still uses literal T4 and never mentions T4′.

**e. The "strongest" evidence is weak.**
- F_t's Brier skill is 2.4–8.1%, and its middle bins under-forecast (0.17 forecast vs 0.24 observed; gap_04 §4.1–4.2).
- The 4-state proxy of the master chain failed the same harness (gap_04 §4.3).
- P(stress within 12 months) ranges from 13% to 35% across filters (gap_04 §6.2).

**f. The era-correlation target is weakly posed.**
- The +0.32 averages Covid (+0.81) with the war months (−0.58) (dossier 03 §4.1).
- verify-03 issue 6 requires era states or structural breaks. Neither was adopted.

## 3. Where the audit is too harsh

ARCHITECTURE.md §4.1 and §7.5 (not audited) already cover two of the audit's gaps:
- They assign B1 to the search plane, and B2 plus a misspecification ensemble to the sealed plane.
- They widen the ensemble: K = 3/5 and jump models, drought persistence 0.95, adverse HF terms, playbook slippage.

One weakness remains. B2 (FHS, 2017–2026) overlaps E's 1990–2026 calibration window, so the sealed plane is disjoint in model family but not in data.

## 4. Gaps the audit missed

1. Reconcile the gap_02 and groups gap_04 engines.
2. Adopt stress conventions consistent with the literature.
3. Recalibrate the Z chain and draws on the frozen state.
4. Specify the two-factor oil model.
5. Estimate the exit hazards.
6. Derive an importance-sampling-weighted bound.
7. Define a red-team plausibility metric.
8. Validate a master chain out of sample.
9. Add Real Assets oil factors. Brief §8 confirms energy holdings; E has no cap-rate or energy series, and 02_REAL_ASSETS_SYNTHESIS.md is missing.
10. Add López (2023)'s withdrawals to the demand-bust draw pool (literature §3.4).

## 5. Revised readiness

| Level | Revised | Why |
|---|---|---|
| DESIGN | Yes | Every element has a method and targets; what is missing is depth |
| BUILD | No | §2c–2d |
| IC ANSWER | No for numbers | Outputs vary 2.6–70× by engine and rest on contested conventions |
| ADIC DATA | Yes | The audit's list, plus revolver availability in stress and the owner's band agreement |
