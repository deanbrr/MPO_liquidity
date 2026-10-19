# Q06 challenge: leverage at portfolio and asset level

**Skeptic's verdict: partial** (auditor: mostly sufficient). DESIGN yes; BUILD no, and not "close"; IC ANSWER direction only. The facility-sizing figures are stale under the user's own census choice, and asset-level leverage covers seven of eight groups.

Keys as in the audit, plus CTX = `inputs/00_CONTEXT_AND_PRIOR_WORK.md`, BRIEF = `design/00_DESIGN_BRIEF.md`, ENG = `research/addenda/gap_02_calcs/t1_engine.py`. Every [I-calc] figure is SYNTHETIC.

## 1. Number checks: all 10 found

All ten values sit where the audit says: 2.36×/4.28%/4.52% (SYN §2.3(e); V06 R2); 8.84→9.66%, 14.4→18.2%, 6.06→5.88% (SYN §4.12); 1.42×/1.51× (SYN §4.12); 2.0/5.8 years (SYN L6; C2 §4.4); SOFR+300/+480 (V08 R4); 7.0→22.8% and 49.6/62.5% (G4 verifier R3, R2); $13.9/6.1/0bn (gap_02 §1.3); $25–92bn (SYN §2.3(d)); and the auditor's $22.2bn, which follows from ENG l.969 (`fac_need = gap.max()/s.fac_credit`; credit 0.80 at l.756).

Three of the stated meanings go too far:
- **Literal T4 against the hard limit.** The low end ($24.9bn, current-NAV draws) is *below* the $26.6bn hard limit. It exceeds only the stressed month-24 limit of $17.4bn (SYN §2.3(d)). Both limits are [I] proposals, not "ADIC's own".
- **"Cannot buy the target at current funding costs."** This holds for futures funding at SOFR+75 (D06 §6.9A). It fails at 4.05% repo/CP funding, where 2.36× reaches 10%. V06 R2 corrected exactly this overclaim.
- **"+0.8pp at the cap."** It assumes 30bp futures financing (gap_05 §6). The June-2026 roll cost 81bp, which takes off ≈0.16pp.

## 2. Readiness claims that fail

**Sizing rests on a superseded census.**
- ENG uses PE NAV $52bn and PE unfunded $27.4bn (l.35–36).
- CTX §1A records that the user chose census v1.1: PE unfunded $16.4bn, or ≈$10.9bn at v2's $34bn PE bucket. v2 also carves $18bn of Real Assets out of PE.
- GS calls the census "decisive" for T4′, θ\* and the facility need (§1, decision 4). It says T4′ on v1.1 "is not yet computed" (finding 3).
- On v1.1, literal T4 at G7 conventions needs $19.5–20.9bn with fixed-USD draws and $2.3–3.7bn with current-NAV draws. On v1.0 it needed $23–49bn (GS §2.4).
- So "literal T4 cannot be bought, hence T4′" depends on the census. The census lowers the need and ≤50% credit raises it; neither combination has been run.

**Sizing also depends on the engine and the model class.**
- G\* of $11.1bn is M6's P99.6 quantile. The mixture gives $4.1bn and the worst of M1–M5 gives $2.6bn (SYN §2.3(d); §9.3 #3 is still open). That puts the facility need at $3.3–13.9bn at 80% credit and $5.2–22.2bn at 50% [my arithmetic].
- With group playbooks, GS's integrated engine cuts do-nothing P(red) from 8.2/21.2/37.3% to 1.6/6.3/14.5% (no slippage assumed; GS §2.4), so the playbook-free sizing engine overstates the need.
- "$0 with band" uses the owner band, which LS §4.2 rates *Contested*. BRIEF §7 item 3 makes no-band Mix A the default, and Mix A certifies at 0.98% against a 1% gate (gap_02 §2.3): almost no margin for lower crisis availability.

**"Not a route to 10%" is a choice of cap, not a finding.** M1's 1.42× break-even is peer-level exposure: OTPP ran 1.43× in 2024 and CPP ≈1.36× (V06 R1). M2 needs no leverage at all. The claim holds only at the [I] 1.30× cap, and in M3 and M6.

**The doctrine is inconsistent.**
- Test 3 uses ΔP(10%), which SYN rejects as an objective. At the cap, M6's P(10y ≥ 10%) rises from 19.6% to 23.8% while its E[R] falls (SYN §4.12).
- D06 §6.8(a) defines "breach" as the 7% floor. But 1.3× futures leverage *lowers* P(5y < 7%) from 40.4% to 39.0% (SYN §2.3(e)), so the ratio's denominator is negative.
- Test 2 fails by construction for the aggregate book (SYN §4.5). The only rule given, "[1, 1.3], monotone in the cushion" (GS §3.7), conflicts with ≈0.97× exposure at t0 and with TPA's stage rule ($12.5/10/5/0bn of beta, Green to Black).

**The current-state answer is missing.** The book fails T4′ by $11.3bn and is in execution recovery at readiness-Red (GS finding 6). By the corpus's own cushion rule, economic leverage belongs at or below 1.0× today, so the +0.18pp and +0.8pp bridge rows are unavailable now. The audit never says so.

**The asset-level evidence is thin and presented selectively.**
- V08 R4 rests on one worked example. Even at SOFR+300, LEVER wins only for a flat ℓ of 3.5–4.25%. The LEVER ≡ ADD + REFI identity holds "by construction", and Rede's margins price GP-level loans, not LP-level borrowing.
- The same SYN §4.4 row shows *bank* back-leverage lifting Capital Solutions' RoE to 10.2%, against 9.25% unlevered.
- D06 §6.8(b)'s core-infrastructure example passes the LEVER test.
- The BGK correction's direction is unproven for the 1.5× trigger. The trigger is tested quarterly on lagged reported NAV (SYN §4.5, limit 4), and the G4 verifier says smoothed marks would *lower* the 49.6 / 62.5% figures.

**"Tested engine" overstates.** The 8/8 test checks pinned duals, not sizing; the models are stylised proxies (gap_02 §7); T4′ overlay use is understated by ≈$0.9bn, re-run open (GS C18).

## 3. Missed gaps

1. **Re-run on current inputs** (High; build_experiment): T4′, θ\*, Mixes A/B and covenant risk on census v1.1 and allocation v2, at ≤50% credit, on the integrated engine.
2. **Real Assets asset-level debt** (High; more_research): non-recourse LEVER, cash-out REFI, DSCR and maturity walls are in BRIEF §8; the G10–G15 research is not on disk.
3. **Doctrine** (Medium; user_decision): define "breach", replace ΔP(10%), specify the aggregate risk-budget rule.
4. **Current state** (Medium; user_decision): no added leverage while in recovery.
5. **Sizing model class** (Medium; user_decision) for θ\* and the facility need.
6. **Draw timing** (Medium; build_experiment). The fixed recourse waterfall that times facility draws (ENG l.590–608) is rated Contradicted (LS §4.4).
7. **Covenant definitions** (Low). gap_02's T9 caps revolver covenant risk at ≤1% at 25% debt/NAV, while SYN §4.5 sets a ≤2% trigger. The rating proxy is unpinned (V06 R9).
8. **Other inputs** (Low). The HF-TRS was run only on C3's mild path. NAV-facility cost is SOFR+300 in C2 §4.5 but SOFR+550 in D06 §6.5.
