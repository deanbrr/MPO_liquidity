# Q05 challenge (R5): can ADIC reach the 10% target?

*Skeptic review of `Q05_audit.md`, 2026-10-18. Read-only on the corpus. Every ADIC figure is SYNTHETIC (context §1A v1 unless stated). [Chal] marks this reviewer's own rough checks, not research results. They come from two scripts in the session scratchpad folder `q05_challenge\`: `bridge_copy.py`, a scratchpad copy of gap_05's `bridge.py` re-run, and `chal_sens.py`, which first reproduces gap_05's v1 central row exactly (8.84 / 10.47 / 6.82 / 8.61 / 8.86 / 6.06).*

**Verdict: mostly sufficient. Upheld, with corrections.**
- The bridge exists, runs and reproduces.
- Its direction (≈8–8.3% central; 10% is a stretch) survived every perturbation I tried.
- Its only "Plan" verdict is weaker than the audit says.

## 1. Number checks

| Claim | Found | Location |
|---|---|---|
| Beta 5.8–10.0% (mean 7.85%) | Yes | gap_05 §1.1, §3; JSON `mixture.beta_geo` |
| Levers +0.37 / +0.37 / −0.02 to +0.23pp; drags 0.31–0.64pp (0.14–1.23pp) | Yes | gap_05 §1.2, §5, §6; synthesis §4.12 |
| E[R] 6.1–10.5% (mean 8.28%) | Yes | gap_05 §6; synthesis §1 finding 1 |
| P(10y ≥ 10%) 20–54% (mean 36.3%) | Yes | gap_05 §6; JSON |
| P(μ ≥ 10%): M1 1–16% (1.05×) / 24–38% (1.30×); M2 66–83% / 91–100% | Yes | gap_05 §6; JSON + `comonotone.py` |
| Break-evens: PE +4.7pp, co-investment +12.3pp, secondaries +15.5pp; overlay SR 1.02; leverage 1.42× | Yes | gap_05 §7; my re-run gives 4.651 / 12.268 / 15.488 |
| +7.6pp P(10%) at the 1.30× cap; volatility 14.4% → 18.2% | Yes | gap_05 §1.5, §7 |
| v8's +3.5pp → +0.61 / +0.35 / +0.47pp; 30% path knowledge, 54% unevidenced | Yes | gap_05 §8 (1.03 / 3.5; 1.88 / 3.5) |
| Payout hurdles 7.9 / 10.8 / 13.9%; ≈5.3% payout at 8.3% | Yes | synthesis §2.3(a) |
| [Aud] M2 at 8.84 / 9.97 / 10.69%; P(μ ≥ 10%) 1–92% | Yes | auditor's `r8_sensitivity.py`, re-run |

Also confirmed:
- Ennis's −1.87pp is still unverified [U] (verifier 02, lines 28 and 133; lit §2.3).
- NZ Super's 9.68% vs 8.19% is confirmed.
- Verifier 06's L≈2.36 is the case with 4.05% funding. The ≈4.3% figure is the separate infeasibility threshold (≈4.28%). The audit runs the two together.

## 2. Readiness

- **DESIGN: survives.**
- **BUILD: survives for the standalone module only.** `bridge.py` re-runs to the published JSON (maximum difference 0). The production `bridge/` is less specified than the audit implies:
  - no Real Assets class and no per-provider Σ;
  - the double-count test ("unless evidence supports more") cannot be coded;
  - the FBE credibility update of lever priors is described in prose only;
  - drags are constants, not outputs of the ledger or gap_02;
  - leverage is never checked against Tier 1;
  - the verdict rule does not say which end of the τ range decides.
- **IC ANSWER: the direction survives; the per-model labels do not** (§3, item 3).
- **NEEDS ADIC DATA: survives.**

## 3. Claims refuted or overstated

1. **"Most [open issues] push lower."** The literature's revisions to the priors point both ways.
   - *Up:* Private Credit's fund-age prior (Böni–de Roon, alphas above 6%; lit §3.9 #23) and long-only's +31bp (lit §4.11).
   - *Down:* the PE fund-size penalty, secondaries' discount-rate exposure, and co-investment's matched benchmarks.
   - A generous upward reading adds ≈0.4–0.6pp to M1 [Chal arithmetic], short of its 1.16pp gap. The direction holds, but not for the audit's reason.
2. **"The main and groups syntheses do not conflict here."** They do on priors:
   - Groups §3.5's hedge-fund net α defaults are 0.5–2.0% (≈1.2% weighted).
   - Groups §4.3's G8 illustration, since superseded, gives Private Credit −41bp.
   - The bridge uses 0 for both.
3. **M2's "Plan" fails for more than conventions.**
   - *The v2 allocation.* With JPM-2026 core real estate and infrastructure as a Real Assets proxy, M2 falls from 10.47% to 9.93%. P(μ ≥ 10%) becomes 43–47%, so M2 becomes a **Stretch**. The mixture falls from 8.28% to 8.09% [Chal].
   - *BlackRock's PE line.* M2 also falls below 10% if that line overstates the median manager by more than **0.93pp** [Chal]. The corpus itself says BlackRock assumes top-quartile private-markets performance (verifier 10 R1; synthesis §4.12 reading 4, §9.3 Q14). Korteweg–Sorensen's interquartile spread is 8.03pp.
   - *The double-count guard.* It caps PE selection α\*, but removing that α\* moves M2 by only 0.08pp (to 10.39%). The guard tests the wrong term.
   - So no model makes 10% a robust Plan.
4. **Leverage peers.** The audit cites CPP (≈1.36×) and OTPP 2024 (1.43×) but leaves out two points from verifier 06:
   - 1.30× matches OTPP 2025 (1.32×);
   - the peer anchors are not like-for-like (R1).

   Synthesis §4.5 puts the limits below peers on purpose.

## 4. Gaps the audit missed

| Gap | Impact | Close by |
|---|---|---|
| M2 runs BlackRock's PE line with no median-manager adjustment (break-even −0.93pp), and the guard tests the wrong term | High | more_research, then build_experiment |
| No BlackRock or AQR Real Assets CMA is on disk, so v2 cannot be re-run consistently. On a JPM proxy, v2 already removes M2's Plan | High | more_research |
| "Stretch" assumes 1.30× is reachable, but the Tier-1 gate blocked amplification in 55% (named path) and 34% (ex ante) of signal months (gap_05 §8). At 1.20×, P(μ ≥ 10%) is 4–22% for M4 and 9–29% for M1 [Chal] | Medium | build_experiment |
| P(μ ≥ 10%) is model-conditional: τ leaves out within-model CMA error and drag uncertainty. Drag uncertainty alone moves M1 from 1–16% to 3–17% [Chal] | Medium | build_experiment |
| The α priors conflict across layers (groups on hedge funds and Private Credit; the literature on Private Credit), and the benchmarks must be reconciled before the priors enter the registry | Medium | more_research |
| M1's "ACWI 7.5%" is verified only as JPM 2027 *US large cap* (verifier 10, claim 2). Each 0.3pp of error moves the book ≈0.06pp | Low | more_research |

## 5. Revised verdict

**Mostly sufficient (upheld).**
- DESIGN, BUILD (standalone module), IC ANSWER (direction only) and NEEDS ADIC DATA all stay "yes".
- **Line for the IC:** "Expect ≈8.1–8.3% centrally. 10% is a stretch in the J.P. Morgan models, needing leverage at the cap plus above-median levers, and it is not a robust Plan in any model."
