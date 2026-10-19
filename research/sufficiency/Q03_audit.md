# Q03 audit: probabilities of outcomes (R3)

**Question.** Can the framework produce credible probabilities of outcomes (P(10%), red events, drawdowns, liquidity breaches) with honest uncertainty across model classes? What are those probabilities today on the synthetic book?

**Verdict: mostly_sufficient.** The research is ready for design and build. The IC answer is indicative only.

Audit date 2026-10-18. Every number is SYNTHETIC (working allocation, SYN-ADIC-177 census v1.0, stylised proxy models M1–M6) unless marked as public data. "Checked" means the auditor matched the figure to its results JSON.

## 1. Answer today

**Can it?** The research *proposes* a complete machinery. It does not yet *show* that the probabilities are credible.
- **Reporting.** Each probability appears as a central value, its range across six fee-consistent CMA models plus a held-out bootstrap generator, and its MC error, with a scenario hash (synthesis §6.7).
- **Certification.** Tier-1 rows use a one-sided 95% Clopper–Pearson bound on 50k fresh paths per model, importance sampling below 0.5%, a reported KL(η = 0.01) worst case, and T6 bands by model class (§4.8–4.9).
- **Discipline.** P(10%) is reported, never optimized (§4.9). The claim validator rejects any probability that lacks its lexicon term, CI and world range (§5.5).
- **Outcome scoring.** Only the market-fragility signal F_t has been scored against outcomes (gap_04 §4.2).

**Today's numbers.**

| Outcome | Reading | Source, tag |
|---|---|---|
| P(10-year TWR ≥ 10%), evidence-central | 20–54% across models, equal-weight mean 36% (M1 40.0, M2 54.1, M3 24.4, M4 38.0, M5 41.5, M6 19.6) | gap_05 §6; synthesis §4.12; [I-calc], checked |
| P(true E[R] ≥ 10%) at 1.05× leverage | M1 1–16%, M2 66–83%, M3 and M6 0% | gap_05 §6 [I-calc] |
| P(red event within 5 years), do nothing | M1 7.8, M2 6.1, M3 10.1, M4 20.8, M5 18.6, M6 37.2% | gap_02 §2.1 [I-calc], checked |
| Same, certified mixes | Mix A ≤ 0.98% and Mix B ≤ 0.79% (CP bounds) in M1–M5; M6 5.8% and 6.5%; best M6 floor 2.4% (CP 2.5%) | gap_02 §2.3 [I-calc], checked |
| Same, integrated group engine with playbooks | Do nothing 1.6 / 6.3 / 14.5% (M1 / M4 / M6); Mix B 0.00 / 0.00 / 0.09%, assuming no slippage | groups gap_04 §2 [I-calc], checked |
| Liquidity | Survival under T4′ 17 months (readiness-Red); ADIC-LCR(30d) 1.91× on CF's basis; 12-month LaR99 $28.4–38.3bn across models | gap_02 §1.3; groups synthesis §2.4 [I-calc; C] |
| Drawdown | Appetite rule P(10-year max DD > 40%) ≤ 10% is **not computed on the book**. i.i.d. lower bounds are 0.5–7.6%. A 3-year re-run of v8 gives P(DD > 15%) falling from 26.4% to 18.1% ex ante | C1 §13 [I-new]; gap_05 §8 [I-calc] |
| Market layer (public data) | F_t 0.10 against a 0.17 base rate; P(stress regime within 12 months) 13–35% | gap_04 §4.2, §6.2 [I-calc] |

**In plain language:**
- 10% is a minority outcome in five of the six models.
- Doing nothing breaches the 1% red-event tolerance in every model.
- A certified 1% mix exists in M1–M5. Whether M6 can meet the gate depends on whether the group playbooks are credited.
- Model choice dominates sampling error. Mean returns disperse 3–4pp across providers against ≈0.2pp of MC error. Even with 20 years of data, a test confuses the providers' models 25–38% of the time (C1 §1; verifier 10 [C]).

## 2. Evidence

**Strong.**
- **Verified machinery.** Verifier 10 recomputed the statistics (C1 §2, §5.7, §5.11 [C]):
  - Clopper–Pearson sizing: at 50k paths, p̂ = 0.90% passes a 1% gate and 1.00% fails;
  - KL worst cases: a nominal 1% becomes 2.70% at η = 0.01;
  - W∞ replaces W1 for probabilities, Kish ESS replaces ENS, and a sign error was fixed.
- **F_t reliability out of sample.** Forecasts of 0.08 / 0.12 / 0.17 verified at 0.10 / 0.14 / 0.24. The top bin is overconfident, 0.60 against 0.46 (gap_04 §4.2).
- **Literature and paper.** The literature supports never maximizing P(10%) and treating drawdown as an appetite metric (literature synthesis §4.7). The paper asks for paired, pre-declared uncertainty on final claims (l.6826–6829).
- **Reproducibility.** The headline figures match `gap02_results.json`, `gap02_certify_extra.json`, `bridge_results.json` and `g04_bridge_results.json`.

**Weak or illustrative.**
- **No figure comes from engine E.**
  - The P(red) runs use six stylised proxies (gap_02 §7).
  - P(10%) comes from a closed-form lognormal that uses JPM-2026 risk for every model, which understates how much the providers disagree on risk (gap_05 §2; verifier 10 R8).
- **The model classes are not independent.**
  - All six share one factor architecture (synthesis §9.2 item 3).
  - Crises fill 13–19% of quarters (gap_02 §2.1).
- **Not yet IC-grade, by the research's own rule.** Every [I-calc] figure must be replicated in one engine before IC use (gap_05 §10; synthesis §9.2 item 10).
- **Rare-event probabilities cannot be validated on outcomes.** Detecting a 0.01 Brier improvement needs ≈6,300 forecasts per arm (synthesis §6.6 [C]).

**Contradictions between files.**
1. **M6 feasibility.**
   - Main synthesis §1 (finding 6) and §4.9, with gap_02 §2.3: no mix reaches 1% in M6. That finding motivates T6 bands by model class and "recovery today".
   - Groups gap_04 §2 and groups synthesis §2.4: Mix B reaches 0.09% in M6 once the playbooks are simulated. They call gap_02's floor "a property of a playbook-free engine".
   - The main synthesis has not been updated.
2. **Census.**
   - Every P(red) figure uses PE unfunded of $27.4bn (census v1.0).
   - Groups gap_02 §0–1 finds v1.0 reproducible only by implausible histories and proposes v1.1 ($16.4bn), under which "stress results move a long way".
   - P(red) has not been re-run on v1.1.
3. **Liquidity readings.**
   - ADIC-LCR(30d): 2.10× in main §4.9 and §6.7, but 1.91× (Amber) in groups synthesis C16.
   - Starting stage: "starts in Red" (main §4.9) against the Red/Amber boundary (groups gap_04 §0).
   - θ\*: 0.76 from one seed (main §2.3(d)) against 0.76–0.81 across ten seeds, pooled 0.79 (groups synthesis §2.4).
4. **Two runs, unlabelled.** Do-nothing P(red) appears as 8.2 / 21.2 / 37.3% (10k paths) and as 7.8 / 20.8 / 37.2% (50k paths). The two agree within MC error.
5. **Gate prices.** Main quotes 8bp for the gate's CE price, 62bp for Mix A's premium and 21bp for Mix B's. Groups gap_04 §7 reprices them to 11–21bp, 66–76bp and 23–29bp.
6. **P(10%) machinery.** gap_05 §6 computes a closed-form 10-year probability (20–54%). gap_05 §8 simulates 3 years on v8's generator and gets ≈20% on ADIC's book. Neither runs in engine E.
7. **Literature against the synthesis.** The structured ambiguity set varies mainly means, yet worst cases load on regime persistence (literature file 10; Hansen et al. 2019; design brief §7 item 5).

**Citation-audit items that touch this question** (literature synthesis §2).
- **§2.4 item 1.** The Broadie–Glasserman–Kou barrier shift has the wrong sign and was never applied, so the co-investment wipe-out (7.0% → 22.8%) and LTV-breach (50–63%) probabilities may be understated. Treat them as provisional (design brief §7 item 15).
- **§2.1.** 37 stream-10 works and 6 stream-11 works went unchecked when the quota ran out.
- **§2.4 items 11 and 13.**
  - Name the error criteria: Holm FWER within a contract, mFDR across contracts.
  - Add the DSR non-normality term.
  - Cite Heitsch–Römisch 2009, not 2003.
  - Meucci (2008) remains [U].
- **Refinements not yet adopted** (§4.7–4.8):
  - report the buffered probability of exceedance (bPoE);
  - test surrogates tighter than T6's 0.60% CVaR;
  - re-impose Tier 1B on a rolling basis.

## 3. Readiness

| Level | Ready? | Reason |
|---|---|---|
| DESIGN | Yes | Event definitions (T6, T7, T9, P(10y ≥ 10%), drawdown appetite), the ensemble, certification, R1–R8, the reporting format and the claim validator are all specified |
| BUILD | Yes, with caveats | Formulas, path counts, bands and acceptance tests are code-ready, and four prototypes reproduce. But engine E is unbuilt, mixture weights are unset, and the bPoE, persistence and slippage tests are unspecified |
| IC ANSWER (synthetic) | No (partial) | Indicative ranges exist for P(10%) and P(red). But M6 red-event levels move about 70× between engines, drawdown is not computed on the book, the census is unsettled, and the research requires one-engine replication first |
| NEEDS ADIC DATA | Yes | Real probabilities need hedge-fund terms τ, PE unfunded by vintage, the draw convention and band, the overlay blotter and CSAs, lever evidence, and ADIC's own VM, bid and draw histories (synthesis §7.2) |

## 4. Gaps

| # | Gap | Impact | Close by |
|---|---|---|---|
| 1 | Red-event levels depend on the engine: M6 Mix B is 6.5% in gap_02 and 0.09% with playbooks. Re-certify at 50k paths with playbook-slippage and delay stresses, then revisit the T6 bands | High | build_experiment |
| 2 | P(red), survival and θ\* all rest on census v1.0. Confirm v1.1 or supply PE commitments by vintage | High | user_decision |
| 3 | The model classes are too alike: one architecture, JPM risk everywhere in the bridge, mostly mean ambiguity, one private cash-flow model. Add provider vols, dwell-time variants and a second private-markets model | High | build_experiment |
| 4 | Real-data calibration (the items in §3) | High | adic_data |
| 5 | No portfolio drawdown probability exists on the book. Compute P(10-year investment max DD > 40%), CDaR, and real NAV against the payout glide path, per model | Medium | build_experiment |
| 6 | MC variability of tail quantiles is unreported (θ\* and P99.6 come from a single seed) | Medium | build_experiment |
| 7 | Mixture weights, M6's weight and the T6 bands are governance choices; the "36%" is an unweighted mean | Medium | user_decision |
| 8 | Literature refinements: bPoE, tighter joint chance-constraint surrogates, rolling Tier 1B, and a dual-bound gap for P | Medium | build_experiment |
| 9 | P(10%) is computed two ways, neither in E. Whether lever uncertainty τ enters the simulated probabilities is unspecified | Medium | build_experiment |
| 10 | Unchecked citations (37 + 6); the barrier-sign error leaves asset-level breach probabilities provisional | Low | more_research |
