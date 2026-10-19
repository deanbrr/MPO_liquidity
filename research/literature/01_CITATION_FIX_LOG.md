# Citation Fix Log

*18 October 2026. This log verifies the citation-correction pass over the research corpus and records every change it made. Paths are relative to `research/` unless stated. All model figures quoted here are SYNTHETIC, as in the files they come from.*

**What the pass corrected against**
- `literature/00_LITERATURE_SYNTHESIS.md` §2: 574 citations checked; 12 not found (ten exist, none fabricated), 24 mismatched, 16 usage errors (one changes numbers: the co-investment Broadie–Glasserman–Kou barrier correction), reference hygiene (§2.5) and 5 cross-file inconsistencies (§2.6);
- the citation-integrity tables in `literature/NN_*.lit.md` and `literature/GN_*.lit.md`;
- the re-checks of the 69 works the Consensus quota left unchecked (`literature/recheck/`);
- the G4 barrier re-run (`groups/addenda/G4_barrier_rerun/RESULTS.md`).

**Bottom line**
1. **The pass is complete for the files the editors owned.** 29 editor reports made 886 changes in 60 files. Every change sampled for verification is present and matches its source. That covers all 31 barrier re-run changes, all consistency edits, every number-changing fix and a spread of the rest. No table was broken.
2. **The barrier error is fixed wherever it was quoted in an edited file.** The only statistic it changed is the G4 book-simulation write-off rate, now 2.8–3.3% a year instead of 2.1–2.5%. The at-exit wipe-out and quarterly-tested LTV-breach rates stand and are now labelled. The gap_04 engine still carries an uncorrected barrier and has not been re-run; its text now flags the bias.
3. **Two audit items are still open** because they sit only in literature files that no editor was given: the Giommetti co-author (§2.6 #1) and the Gredil–Liu–Sensoy figure (§2.6 #5). Stale "provisional / understated" barrier wording also remains in the design brief, five sufficiency audits and the literature synthesis itself (section 5.1).
4. **About 25 claims cannot be verified from open sources.** Each is marked [unverified] in its file and listed in section 5.3.
5. **The user's request in this run was to add a Real Assets group.** It was not part of this citation pass, and every editor left it out of scope. Real Assets work appears to be under way in other files: the design brief §8 and `groups/dossiers/G10`–`G15_ra_*.md`. Those files were not in the citation audit (section 5.2).

## 1. Summary counts

- **Editor reports:** 29 (fix:01–14, fix:G1–G9, clusters, group clusters, main addenda, group addenda, main synthesis, group synthesis).
- **Files changed:** 60, each with an appended "Citation corrections (2026-10-18)" section. Three files on editors' lists were deliberately left unedited because no correction applied to them: the 05 and 06 verification logs and `groups/addenda/gap_02.md`.
- **Reported changes:** 886.
- **Skipped items recorded by editors:** 386 (section 4).

**Changes by kind**

| Kind | Changes |
|---|---|
| metadata | 378 |
| usage | 130 |
| missing_reference | 82 |
| recheck | 143 |
| inconsistency | 21 |
| consistency_edit | 101 |
| barrier_rerun | 31 |
| **Total** | **886** |

**Changes by editor report**

| Report | Files | metadata | usage | missing_reference | recheck | inconsistency | consistency_edit | barrier_rerun | Total |
|---|---|---|---|---|---|---|---|---|---|
| fix:01 | `dossiers/01_mpo.md`, `verification/01_mpo.verify.md` | 20 | 0 | 2 | 4 | 1 | 2 | 0 | 29 |
| fix:02 | `dossiers/02_endowment_swf.md`, `verification/02_endowment_swf.verify.md` | 22 | 2 | 1 | 0 | 0 | 6 | 0 | 31 |
| fix:03 | `dossiers/03_sovereign_alm.md`, `verification/03_sovereign_alm.verify.md` | 14 | 0 | 2 | 5 | 0 | 1 | 0 | 22 |
| fix:04 | `dossiers/04_pe_cashflows.md`, `verification/04_pe_cashflows.verify.md` | 5 | 4 | 4 | 0 | 2 | 4 | 0 | 19 |
| fix:05 | `dossiers/05_secondaries_navfin.md` | 7 | 2 | 7 | 0 | 0 | 1 | 0 | 17 |
| fix:06 | `dossiers/06_leverage.md` | 8 | 3 | 0 | 0 | 0 | 1 | 0 | 12 |
| fix:07 | `dossiers/07_return_fusion.md`, `verification/07_return_fusion.verify.md` | 16 | 6 | 1 | 1 | 1 | 3 | 0 | 28 |
| fix:08 | `dossiers/08_action_valuation.md`, `verification/08_action_valuation.verify.md` | 8 | 5 | 2 | 0 | 0 | 4 | 0 | 19 |
| fix:09 | `dossiers/09_overlay.md`, `verification/09_overlay.verify.md` | 21 | 5 | 1 | 1 | 0 | 4 | 0 | 32 |
| fix:10 | `dossiers/10_scenarios_robustness.md`, `verification/10_scenarios_robustness.verify.md` | 12 | 4 | 4 | 34 | 0 | 3 | 0 | 57 |
| fix:11 | `dossiers/11_objectives.md`, `verification/11_objectives.verify.md` | 7 | 0 | 2 | 7 | 0 | 2 | 0 | 18 |
| fix:12 | `dossiers/12_agentic_ai.md`, `verification/12_agentic_ai.verify.md` | 12 | 11 | 0 | 5 | 0 | 3 | 0 | 31 |
| fix:13 | `dossiers/13_paper_deepread.md`, `verification/13_paper_deepread.verify.md` | 10 | 5 | 4 | 7 | 0 | 3 | 0 | 29 |
| fix:14 | `dossiers/14_ic_deliberation.md`, `verification/14_ic_deliberation.verify.md` | 14 | 8 | 0 | 25 | 1 | 4 | 0 | 52 |
| fix:G1 | `groups/dossiers/G1_pe_primaries.md`, `groups/verification/G1_pe_primaries.verify.md` | 21 | 0 | 0 | 0 | 3 | 2 | 0 | 26 |
| fix:G2 | `groups/dossiers/G2_secondaries_group.md`, `groups/verification/G2_secondaries_group.verify.md` | 15 | 9 | 6 | 0 | 0 | 4 | 0 | 34 |
| fix:G3 | `groups/dossiers/G3_cap_solutions.md`, `groups/verification/G3_cap_solutions.verify.md` | 3 | 4 | 8 | 10 | 2 | 2 | 0 | 29 |
| fix:G4 | `groups/dossiers/G4_coinvest.md`, `groups/verification/G4_coinvest.verify.md` | 2 | 8 | 3 | 0 | 0 | 3 | 10 | 26 |
| fix:G5 | `groups/dossiers/G5_public_markets.md`, `groups/verification/G5_public_markets.verify.md` | 19 | 3 | 0 | 0 | 2 | 5 | 0 | 29 |
| fix:G6 | `groups/dossiers/G6_private_credit.md`, `groups/verification/G6_private_credit.verify.md` | 10 | 6 | 5 | 3 | 2 | 4 | 0 | 30 |
| fix:G7 | `groups/dossiers/G7_liquidity_ladder.md`, `groups/verification/G7_liquidity_ladder.verify.md` | 13 | 5 | 9 | 0 | 1 | 3 | 0 | 31 |
| fix:G8 | `groups/dossiers/G8_org_tpa_economics.md`, `groups/verification/G8_org_tpa_economics.verify.md` | 14 | 4 | 1 | 2 | 0 | 3 | 0 | 24 |
| fix:G9 | `groups/dossiers/G9_synthetic_data.md`, `groups/verification/G9_synthetic_data.verify.md` | 22 | 5 | 5 | 1 | 2 | 1 | 0 | 36 |
| fix:clusters | `clusters/C1_portfolio_math.md`, `clusters/C2_private_liquidity.md`, `clusters/C3_liabilities_overlay.md`, `clusters/C4_agentic_ic.md` | 13 | 12 | 5 | 8 | 1 | 4 | 0 | 43 |
| fix:group-clusters | `groups/clusters/GC1_private_groups.md`, `groups/clusters/GC2_liquidity_org_data.md` | 6 | 5 | 0 | 3 | 1 | 2 | 5 | 22 |
| fix:main-addenda | `addenda/gap_01.md`, `addenda/gap_02.md`, `addenda/gap_03.md`, `addenda/gap_04.md`, `addenda/gap_05.md` | 11 | 4 | 1 | 7 | 0 | 7 | 2 | 32 |
| fix:group-addenda | `groups/addenda/gap_01.md`, `groups/addenda/gap_03.md`, `groups/addenda/gap_04.md` | 3 | 1 | 2 | 0 | 0 | 3 | 4 | 13 |
| fix:main-synthesis | `00_SYNTHESIS.md` | 35 | 5 | 6 | 15 | 1 | 16 | 3 | 81 |
| fix:group-synthesis | `groups/01_GROUPS_SYNTHESIS.md` | 15 | 4 | 1 | 5 | 1 | 1 | 7 | 34 |

**Coverage of the audit (`00_LITERATURE_SYNTHESIS.md` §2) and the other correction sources**

| Source | Items | Applied | No change needed | Open after this pass |
|---|---|---|---|---|
| §2.2 Not found | 12 | 7: de Finetti, Merton, Gorton–Metrick "Haircuts", Mincer–Zarnowitz, Nordhaus, "Rode et al.", the G3 Getmansky–Lo–Makarov entry | 5: Ljungqvist & Richardson, Getmansky–Lo–Makarov in 04, Lange et al., Song, *The Agentic Scientist* | None. The de Finetti title and the Rode et al. fee split stay [unverified] |
| §2.3 Mismatched | 24 | 24 | 0 | None. The Ennis −1.87% attribution and the Moutanabbir figures stay [unverified] |
| §2.4 Usage errors | 16 | 16 | 0 | The gap_04 engine barrier is not re-run (owner action); stale barrier wording sits outside the edited files |
| §2.5 Reference hygiene | All listed items | All: missing entries (Klaassen; Föllmer & Leukert 2000; seven G3 body-only works; four G7 methods), metadata (09, 11, 06, G1), titles and upgrades (G7, G5, G6, G3), orphans (G2, G8; G3 Kaplan & Schoar withdrawn), unnamed sources (G3 Mack, BIS work), 07 Wikipedia and rdrr.io links | – | None |
| §2.6 Cross-file | 5 | 3: #2 Bühlmann DOI (resolved for G6's DOI; confirmed on Crossref), #3 Albertus & Denes (JFQA 2026 noted as probable successor; content unverified), #4 Geltner (each citation now names its paper) | 0 | 2: #1 Giommetti co-author and #5 Gredil–Liu–Sensoy figure, both only in literature files |
| Barrier re-run (RESULTS §6) | 7 changing values; 2 optional wordings; values that stay; "provisional" text; gap_04 | All 7 changing values and both optional wordings; values that stay are labelled "at exit" or "quarterly-tested", with continuous bounds | – | "Provisional" text in the design brief, sufficiency audits and literature synthesis; gap_04 engine re-run |
| Re-checks (topics 10, G3, 14, 11, 13) | 69 works | Applied wherever a re-checked work is cited (10, 12, 13, 14, 07, 03, 09, 11, G3, G6, G8, clusters, group clusters, addenda, both syntheses) | Works not cited in a file | MAP pre-votes and a few other usage points stay [unverified] |

## 2. Verification results

### 2.1 Method

1. **Targeted presence checks (232).** These cover every `barrier_rerun` change, every `consistency_edit` outside the appended sections, and a spread of the other kinds across all 29 reports. For each, a distinctive phrase from the reported new text was searched for in the target file, after normalizing dashes, emphasis and case. Nine phrases were worded differently from the report; for those, the line was read and confirmed.
2. **Token checks (410 changes).** Every DOI, volume(issue) and page range in a change's new text was searched for in its file.
3. **Audit-prescription checks (132).** The value or wording that §2 prescribes was searched for in the file it concerns. Five of these checks confirm that an old value is gone from the body.
4. **Corrections-section audit (60 files).** Each section was checked for position at the end of its file, entry count against the editor's report, and a sources note.
5. **Table integrity (60 files).** Each markdown table row's cell count was compared with its header, ignoring escaped pipes and pipes inside code or math.
6. **Recomputation.** The 13 Campi–Garatti exact sample sizes that editors changed or relied on were recomputed: the smallest N with binom.cdf(d − 1, N, ε) ≤ β (scipy).
7. **External spot checks.** On Crossref: Wang, Morgenstern & Dickerson (journal venue) and both Bühlmann DOIs. On the risk.net publisher page: the pages of the backtest-overfitting (PBO) paper.
8. **Residual sweep.** 73 regular expressions for old values the audit flagged were run over every `.md` file outside `literature/`. Examples: 0.974, "26 of 33", β > 2, ×2.4, 2.1–2.5%, e^{−0.5826}, "central Treasury", SSRN-only links. The sweep catches values that spread into files no editor reported on.

### 2.2 Results by test

| Test | Scope | Result |
|---|---|---|
| Targeted presence | 232 changes | 232 present (223 by phrase match, 9 after reading the line) |
| Tokens | 410 changes carrying DOIs, volumes or pages | 410 complete; no token missing |
| Audit prescriptions | 132 checks | 132 pass |
| Corrections sections | 60 files | All 60 are the last section of their file; entry counts match the reports, allowing for grouped lines |
| Table integrity | 60 files | No row broken by the edits. 1 pre-existing defect: the G3 §6.8 "Group forecast" row has an unescaped pipe. 2 pre-existing rendering risks: a 12 §7 row with LaTeX pipes, and a G7 l.861 row with a pipe inside code |
| Recomputation | 13 values | 13 exact matches: 631 and 31,785 (01); 447, 986, 2,658 and 4,970 (10); 3,260, 9,086, 27,418 and 1,801 (11); 418, 577 and 935 (06 skip note) |
| External | 4 lookups | All 4 confirm the editors |
| Residual sweep | 73 patterns | No wrong-sign BGK prescription and no stale barrier value in any edited file. Residuals are listed in section 5 |

**Coverage of the change table.** 653 of the 886 changes are covered by at least one row-level check: a check ID, a read, a grep, the section audit, recomputation, an external lookup or a complete token match. The other 233 were not individually sampled. Their presence rests on the file's own corrections-section entry, and on no failure turning up anywhere in the sample.

### 2.3 Findings and discrepancies

1. **Number-changing fixes match their sources.**
   - The barrier re-run values (RESULTS §3, §5) appear in the G4 dossier, the G4 verification log, GC1, the main-report gap_01 and both syntheses.
   - The recap multiplier of about ×1.1–×1.7 checks out: 1 + 0.42 × 25/84 ≈ 1.13 and 1 + 2.4 × 25/84 ≈ 1.71.
   - The write-off rate is 2.3–2.8× Kaplan–Strömberg's ≈1.2% (2.8 ÷ 1.2 and 3.3 ÷ 1.2).
   - All Campi–Garatti minima reproduce exactly.
2. **The wrong-sign formula e^{−0.5826σ√Δ} survives only in two kinds of place:**
   - where the error is described: the literature synthesis, RESULTS.md and the G4 corrections section;
   - as BGK's own use, evaluating a discretely tested event with a continuous formula, which the corrected text now explains.

   Elsewhere outside the edited files, `literature/G4_coinvest.lit.md` and `sufficiency/Q07_audit.md` give the shift with the correct "+" sign.
3. **The main-synthesis consistency edits faithfully port their sources.** These are not citation fixes.
   - The §2.3(d) survival table matches groups gap_01 §1.2 row for row.
   - The T4′ row matches groups gap_01 l.303–306.
   - The 1.91× coverage ratio matches groups synthesis C12.
   - The Shapley wording matches groups synthesis C9: 512 coalitions, 54 minutes on 22 cores.
   - Removing "NAV-facility documents activated" from the Amber row follows groups gap_01's recommendation to drop the NAV facility.
4. **In three places the report's wording differs from the file, with no effect on the outcome.**
   - 08 §2.5 (Whittle): the reported parenthetical with the *J. Appl. Prob.* metadata was not inserted. Instead, "metadata from memory" was removed, and the metadata sits in §10.
   - 10 dossier: its corrections section has 32 entries, against "34 lines" in the report, because some entries group several DOI additions. No change is missing.
   - G4 dossier: the section has 17 change lines plus a "Not changed" line, against "18 changes" in the report, because the † note is folded into the write-off line.
5. **One figure in an editor's skip note does not reproduce. No file is affected.**
   - The 06 editor quotes the Calafiore–Campi (2006) sufficient bound as 1,195 / 1,859 / 3,534 for d = 3 / 5 / 10 at ε = 2% and β = 1%.
   - The standard formula, (2/ε)·ln(1/β) + 2d + (2d/ε)·ln(2/ε), gives 1,848 / 2,773 / 5,086.
   - The exact minima (418 / 577 / 935) are right, and so is the editor's conclusion: 06's "a few thousand scenarios" matches the looser bound.
6. **Two deviations from the audit's instructions are both justified.**
   - Stream 14 cites Wang, Morgenstern & Dickerson as *Nature Machine Intelligence* 7(3):400–411 rather than arXiv v3. Crossref confirms the journal record (title, three authors, 7(3), 400–411, online 17 Feb 2025).
   - Streams 01 and 09 give the PBO paper's pages as 20(4):39–69, first published 19 Sep 2016. Three other editors could not confirm the pages, and Crossref holds none. The risk.net publisher page shows exactly "Volume 20, Number 4 (April 2017)", pages 39–69, first published 19 September 2016.
7. **Bühlmann DOIs re-confirmed on Crossref.** …8989 is the 1967 paper (*ASTIN Bulletin* 4(3):199–207); …8023 is the 1969 paper (*ASTIN Bulletin* 5(2):157–165). The six files now carrying …8989 for the 1967 paper are right: 07, 14, G3, G6, C4 and the main synthesis.
8. **Version choices differ by file, but each is consistent with the audit.**
   - 01 keeps the Luxenberg arXiv preprint (nine authors) as its primary entry, because its figures come from the preprint, and adds the five-author ICAIF version. 04, G2, C1 and the main synthesis make the ICAIF version primary.
   - The Geltner choice is in section 5.1.

### 2.4 Audit-prescription checks

Each row tests whether the value or wording that `00_LITERATURE_SYNTHESIS.md` §2 prescribes is now in the file (normalized text match). Rows marked "absent" test that the old value is gone from the body (outside the corrections section).

| §2 item | What is checked | File | Token | Result |
|---|---|---|---|---|
| 2.2 #1 | de Finetti (1957) venue and pages from the citing record | `dossiers/02_endowment_swf.md` | 2:433–443 | present |
| 2.2 #2 | Merton (1993) ch. 7, pp. 211–242 | `dossiers/03_sovereign_alm.md` | 211–242 | present |
| 2.2 #2 | Merton (1993) ch. 7, pp. 211–242 | `dossiers/02_endowment_swf.md` | 211–242 | present |
| 2.2 #2 | Merton (1993) ch. 7, pp. 211–242 | `dossiers/01_mpo.md` | 211-242 | present |
| 2.2 #5 | Haircuts: FRB St. Louis Review 92(6):507–520 | `dossiers/06_leverage.md` | 92(6): 507–520 | present |
| 2.2 #6 | Mincer & Zarnowitz pp. 3–46 | `dossiers/07_return_fusion.md` | pp. 3–46 | present |
| 2.2 #7 | Nordhaus REStat 69(4):667–674 (dagger removed) | `dossiers/07_return_fusion.md` | 69(4):667–674 | present |
| 2.2 #11 | 'Rode et al.' identified | `groups/dossiers/G2_secondaries_group.md` | Rode, N., Poldauf, P. | present |
| 2.2 #12 | Getmansky, Lo & Makarov entry in G3 | `groups/dossiers/G3_cap_solutions.md` | Getmansky, M., Lo, A. W., & Makarov, I. (2004) | present |
| 2.3 02 | Ennis (2021) J. Investing DOI | `dossiers/02_endowment_swf.md` | 10.3905/joi.2021.1.166 | present |
| 2.3 02 | Ennis (2021) JPM DOI | `dossiers/02_endowment_swf.md` | 10.3905/jpm.2021.1.217 | present |
| 2.3 02 | Size cohorts, not 43 endowments | `dossiers/02_endowment_swf.md` | six fund-size cohorts | present |
| 2.3 02 | TPA guide DOI | `dossiers/02_endowment_swf.md` | 10.56227/26.1.20 | present |
| 2.3 03 | Moutanabbir & Noureldin (2020) IREF | `dossiers/03_sovereign_alm.md` | International Review of Economics & Finance | present |
| 2.3 03 | Moutanabbir & Noureldin DOI given by the audit | `dossiers/03_sovereign_alm.md` | 10.1016/j.iref.2020.06.014 | present |
| 2.3 04 | Luxenberg ICAIF '22 DOI | `dossiers/04_pe_cashflows.md` | 10.1145/3533271.3561769 | present |
| 2.3 04 | SWY RFS 27(7):1977–2021 | `dossiers/04_pe_cashflows.md` | 27(7), 1977–2021 | present |
| 2.3 04 | Nadauld JFE DOI | `dossiers/04_pe_cashflows.md` | 10.1016/j.jfineco.2018.11.007 | present |
| 2.3 04 | Nadauld seller PME 0.976 | `dossiers/04_pe_cashflows.md` | sellers' 0.976 | present |
| 2.3 04 | Jeet et al. DOI | `dossiers/04_pe_cashflows.md` | 10.3905/jpmi.2026.1.010 | present |
| 2.3 05 | WilmerHale title | `dossiers/05_secondaries_navfin.md` | Trends in the Private Equity Secondary Market | present |
| 2.3 05 | WilmerHale BLT 18(4) | `dossiers/05_secondaries_navfin.md` | 18(4) | present |
| 2.3 07 | Colson & Cooke: 32 of 33 in sample | `dossiers/07_return_fusion.md` | 32 of 33 | present |
| 2.3 07 | BGG published β 1.0 / 1.4 | `dossiers/07_return_fusion.md` | about 1.0 (buyout) and 1.4 (venture) | present |
| 2.3 07 | BGG published total risk 40% (VC) | `dossiers/07_return_fusion.md` | 40% | present |
| 2.3 07 | Nadauld seller PME 0.976 | `dossiers/07_return_fusion.md` | sellers' 0.976 | present |
| 2.3 08 | Gribik title | `dossiers/08_action_valuation.md` | Market-clearing electricity prices and energy uplift | present |
| 2.3 10 | Mohajerin Esfahani & Kuhn subtitle | `dossiers/10_scenarios_robustness.md` | performance guarantees and tractable reformulations | present |
| 2.3 10 | Mohajerin Esfahani & Kuhn DOI | `dossiers/10_scenarios_robustness.md` | 10.1007/s10107-017-1172-1 | present |
| 2.3 10 | Gao & Kleywegt DOI | `dossiers/10_scenarios_robustness.md` | 10.1287/moor.2022.1275 | present |
| 2.3 10 | Xie DOI | `dossiers/10_scenarios_robustness.md` | 10.1007/s10107-019-01445-5 | present |
| 2.3 10 | Shu, Yu & Mulvey DOI | `dossiers/10_scenarios_robustness.md` | 10.1057/s41260-024-00376-x | present |
| 2.3 12 | Gao, Jiang & Yan current title | `dossiers/12_agentic_ai.md` | Detecting Lookahead Bias in LLM Forecasts | present |
| 2.3 12 | Nature paper title | `dossiers/12_agentic_ai.md` | Towards end-to-end automation of AI research | present |
| 2.3 12 | Nature paper DOI | `dossiers/12_agentic_ai.md` | 10.1038/s41586-026-10265-5 | present |
| 2.3 13 | Nature paper DOI | `dossiers/13_paper_deepread.md` | 10.1038/s41586-026-10265-5 | present |
| 2.3 13 | Workshop acceptance rate 70% | `dossiers/13_paper_deepread.md` | 70% | present |
| 2.3 G5 | Almgren & Chriss (2001) DOI | `groups/dossiers/G5_public_markets.md` | 10.21314/jor.2001.041 | present |
| 2.3 G8 | Lamont pages 83–109 | `groups/dossiers/G8_org_tpa_economics.md` | 52(1):83–109 | present |
| 2.3 G8 | Shin & Stulz QJE 113(2):531–552 kept | `groups/dossiers/G8_org_tpa_economics.md` | 113(2):531–552 | present |
| 2.3 G9 | Modrák et al. 20(2):461–488 (2025) | `groups/dossiers/G9_synthetic_data.md` | 20(2):461–488 | present |
| 2.4 #1 | BGK shift toward the current value | `groups/dossiers/G4_coinvest.md` | e^{+0.5826 | present |
| 2.4 #1 | BGK paper cited | `groups/dossiers/G4_coinvest.md` | 10.1111/1467-9965.00035 | present |
| 2.4 #2 | Recap multiplier ×1.1 (OLS) | `groups/dossiers/G4_coinvest.md` | ×1.1 (OLS) | present |
| 2.4 #2 | Recap multiplier ×1.7 (IV) | `groups/dossiers/G4_coinvest.md` | ×1.7 (IV) | present |
| 2.4 #3 | LPG full title | `groups/dossiers/G4_coinvest.md` | Giants at the Gate: Investment Returns and Diseconomies of Scale | present |
| 2.4 #3 | Axelson et al. (2013) JF 68(6):2223–2267 | `groups/dossiers/G4_coinvest.md` | 68(6):2223–2267 | present |
| 2.4 #3 | Axelson–Sorensen–Strömberg draft | `groups/dossiers/G4_coinvest.md` | Axelson, U., Sorensen, M. | present |
| 2.4 #3 | Kaplan & Strömberg pages | `groups/dossiers/G4_coinvest.md` | 23(1):121–146 | present |
| 2.4 #4 | Recoveries are KBRA DLD data | `groups/dossiers/G3_cap_solutions.md` | KBRA DLD | present |
| 2.4 #4 | Smoothing 0.5 is stream 04's derivation | `groups/dossiers/G3_cap_solutions.md` | stream 04's derivation | present |
| 2.4 #5 | Bollen & Sensoy published finding (up to 40% in PE) | `dossiers/05_secondaries_navfin.md` | up to 40% | present |
| 2.4 #6 | Boyer et al. JF 78(2):835–885 | `groups/dossiers/G2_secondaries_group.md` | 78(2):835 | present |
| 2.4 #7 | Jeanne & Rancière 9.1% (EJ 2011) | `dossiers/09_overlay.md` | 9.1% of output | present |
| 2.4 #7 | Lo (2002): up to 65% | `dossiers/09_overlay.md` | 65 percent | present |
| 2.4 #7 | Moreira & Muir disputed out of sample | `dossiers/09_overlay.md` | Cederburg | present |
| 2.4 #7 | Kaminski & Lo now checked | `dossiers/09_overlay.md` | When Do Stop-Loss Rules Stop Losses? | present |
| 2.4 #8 | Campbell & Sharpe calibrates w_a or ρ_f | `groups/dossiers/G9_synthetic_data.md` | not the weight on underwriting | present |
| 2.4 #8 | HJK working-paper figures labelled | `groups/dossiers/G9_synthetic_data.md` | NBER WP 17874, Feb 2012 | present |
| 2.4 #8 | BGG λ and noise labelled as WP figures | `groups/dossiers/G9_synthetic_data.md` | 2020 working-paper figures | present |
| 2.4 #9 | Schwenk wording | `dossiers/14_ic_deliberation.md` | neither DA nor DI beat the other | present |
| 2.4 #10 | Drills monitor, not prevent | `dossiers/14_ic_deliberation.md` | rather than prevent it | present |
| 2.4 #10 | Fogliato: 19 veterinary radiologists | `dossiers/14_ic_deliberation.md` | n = 19 | present |
| 2.4 #10 | Hackenburg DOI | `dossiers/14_ic_deliberation.md` | 10.1126/science.aea3884 | present |
| 2.4 #10 | Salvi title | `dossiers/14_ic_deliberation.md` | On the conversational persuasiveness of GPT-4 | present |
| 2.4 #10 | Salvi DOI | `dossiers/14_ic_deliberation.md` | 10.1038/s41562-025-02194-6 | present |
| 2.4 #11 | α-investing controls mFDR | `dossiers/12_agentic_ai.md` | mFDR | present |
| 2.4 #11 | Holm FWER within a contract | `dossiers/12_agentic_ai.md` | FWER | present |
| 2.4 #11 | DSR non-normality term | `dossiers/12_agentic_ai.md` | Non-normality term | present |
| 2.4 #11 | FINSABER abstract wording | `dossiers/12_agentic_ai.md` | deteriorate significantly | present |
| 2.4 #11 | Smith–Winkler shrinkage applied | `dossiers/12_agentic_ai.md` | Shrink reported estimates | present |
| 2.4 #11 | Kosmos despite full citation coverage | `dossiers/12_agentic_ai.md` | cites every statement | present |
| 2.4 #12 | MLReplicate checked against arXiv 2605.16616 | `dossiers/13_paper_deepread.md` | 2605.16616 | present |
| 2.4 #12 | Skalse (2022) added | `dossiers/13_paper_deepread.md` | Skalse | present |
| 2.4 #12 | Pan (2022) added | `dossiers/13_paper_deepread.md` | Pan | present |
| 2.4 #12 | SR 26-2 supersedes SR 11-7 | `dossiers/13_paper_deepread.md` | SR 26-2 | present |
| 2.4 #13 | Glasserman & Xu verbatim | `dossiers/10_scenarios_robustness.md` | very little computational effort beyond that required to evaluate performance under the baseline nominal model | present |
| 2.4 #13 | Heitsch & Römisch (2009) | `dossiers/10_scenarios_robustness.md` | Scenario tree reduction for multistage stochastic programs | present |
| 2.4 #13 | ENS source Meucci (2012) | `dossiers/10_scenarios_robustness.md` | Meucci (2012) | present |
| 2.4 #13 | Meucci (2008) linked to arXiv 1012.2848 | `dossiers/10_scenarios_robustness.md` | 1012.2848 | present |
| 2.4 #14 | Haircut spike in bilateral repo | `groups/dossiers/G7_liquidity_ladder.md` | bilateral | present |
| 2.4 #14 | Draws met with Fed support | `groups/dossiers/G7_liquidity_ladder.md` | Federal Reserve's liquidity programs | present |
| 2.4 #14 | Corporate Finance owns Treasury | `groups/dossiers/G7_liquidity_ladder.md` | Corporate Finance, which owns the Treasury function | present |
| 2.4 #15 | 31% covers public and private pensions | `groups/dossiers/G6_private_credit.md` | public and private pension funds together | present |
| 2.4 #15 | Berrospide table 6.4% vs text 6.6% | `groups/dossiers/G6_private_credit.md` | its text gives 6.6% | present |
| 2.4 #15 | Rintamäki & Steffen second-hand | `groups/dossiers/G6_private_credit.md` | second-hand | present |
| 2.4 #16 | Glaser source page cited | `groups/dossiers/G8_org_tpa_economics.md` | RePEc/IDEAS | present |
| 2.4 #16 | Albuquerque abstract-level only | `groups/dossiers/G2_secondaries_group.md` | SSRN abstract | present |
| 2.5 | Klaassen (2002) in 01 | `dossiers/01_mpo.md` | 10.1287/mnsc.48.11.1512.261 | present |
| 2.5 | Föllmer & Leukert (2000) in 11 | `dossiers/11_objectives.md` | 10.1007/s007800050008 | present |
| 2.5 | G3 body-only works: Takahashi & Alexander | `groups/dossiers/G3_cap_solutions.md` | Takahashi, D., & Alexander, S. (2002) | present |
| 2.5 | G3 body-only works: Geltner | `groups/dossiers/G3_cap_solutions.md` | Geltner, D. M. (1991) | present |
| 2.5 | G3 body-only works: BGG | `groups/dossiers/G3_cap_solutions.md` | Brown, G. W., Ghysels, E., & Gredil, O. R. (2023) | present |
| 2.5 | G3 body-only works: Bühlmann | `groups/dossiers/G3_cap_solutions.md` | Bühlmann, H. (1967) | present |
| 2.5 | G3 body-only works: Mack | `groups/dossiers/G3_cap_solutions.md` | Mack, T. (1993) | present |
| 2.5 | G3 body-only works: BIS work | `groups/dossiers/G3_cap_solutions.md` | Aramonte, S., & Avalos, F. | present |
| 2.5 | G7 method: Glasserman–Kang–Kang | `groups/dossiers/G7_liquidity_ladder.md` | Stress scenario selection by empirical likelihood | present |
| 2.5 | G7 method: Gerber–Shiu | `groups/dossiers/G7_liquidity_ladder.md` | On the Time Value of Ruin | present |
| 2.5 | G7 method: Little | `groups/dossiers/G7_liquidity_ladder.md` | L = λW | present |
| 2.5 | G7 method: Clopper–Pearson | `groups/dossiers/G7_liquidity_ladder.md` | Biometrika 26(4), 404–413 | present |
| 2.5 | 09 PBO venue J. Comput. Finance 20(4) | `dossiers/09_overlay.md` | 20(4), 39–69 | present |
| 2.5 | 01 open PBO venue resolved | `dossiers/01_mpo.md` | 20(4):39-69 | present |
| 2.5 | 09 Koijen et al. JFE 127(2):197–225 | `dossiers/09_overlay.md` | 127(2), 197–225 | present |
| 2.5 | 11 'Mohajerin Esfahani' | `dossiers/11_objectives.md` | Mohajerin Esfahani & Kuhn 2018 | present |
| 2.5 | 06 Brown, Dimmock, Kang & Weisbenner via AER | `dossiers/06_leverage.md` | 10.1257/aer.104.3.931 | present |
| 2.5 | G1 Lerner–Mao–Schoar–Zhang version | `groups/dossiers/G1_pe_primaries.md` | 10.1016/j.jfineco.2021.05.034 | present |
| 2.5 | G1 Brown et al. version | `groups/dossiers/G1_pe_primaries.md` | 10.1016/j.jfineco.2020.08.014 | present |
| 2.5 | G1 Begenau & Siriwardane version | `groups/dossiers/G1_pe_primaries.md` | 10.1111/jofi.13319 | present |
| 2.5 | G5 title: Barras et al. | `groups/dossiers/G5_public_markets.md` | Measuring luck in estimated alphas | present |
| 2.5 | G5 title: Bollen & Pool | `groups/dossiers/G5_public_markets.md` | Evidence from the pooled distribution | present |
| 2.5 | G5 title: Chen, Goldstein & Jiang | `groups/dossiers/G5_public_markets.md` | Evidence from mutual fund outflows | present |
| 2.5 | G5 title: Jagannathan et al. | `groups/dossiers/G5_public_markets.md` | An empirical evaluation | present |
| 2.5 | G6 [K] entries upgraded to [M] | `groups/dossiers/G6_private_credit.md` | [M] = metadata confirmed | present |
| 2.5 | G3 Black & Cox metadata | `groups/dossiers/G3_cap_solutions.md` | 31(2), 351-367 | present |
| 2.5 | G2 Bollen & Sensoy orphan cited | `groups/dossiers/G2_secondaries_group.md` | Bollen & Sensoy's | present |
| 2.5 | G2 Gourier orphan cited | `groups/dossiers/G2_secondaries_group.md` | Gourier, Phalippou & Westerfield's | present |
| 2.5 | G8 Crawford & Sobel orphan cited | `groups/dossiers/G8_org_tpa_economics.md` | Crawford & Sobel (1982) | present |
| 2.5 | 07 rdrr.io link replaced (Bates & Granger DOI) | `dossiers/07_return_fusion.md` | 10.1057/jors.1969.103 | present |
| 2.5 | 07 Wikipedia link replaced (Cooke → Colson & Cooke) | `dossiers/07_return_fusion.md` | 10.1016/j.ress.2017.02.003 | present |
| 2.6 #2 | Bühlmann (1967) DOI …8989 in 07 | `dossiers/07_return_fusion.md` | 10.1017/S0515036100008989 | present |
| 2.6 #2 | Bühlmann (1967) DOI …8989 in G6 | `groups/dossiers/G6_private_credit.md` | 10.1017/S0515036100008989 | present |
| 2.6 #3 | Albertus & Denes JFQA successor noted in G1 | `groups/dossiers/G1_pe_primaries.md` | Agency Costs and Cash Flow Management | present |
| 2.6 #4 | Geltner paper named in 04 | `dossiers/04_pe_cashflows.md` | Geltner (1991) | present |
| 2.6 #4 | Geltner paper named in G3 | `groups/dossiers/G3_cap_solutions.md` | Geltner 1991 | present |
| 2.6 #4 | Geltner paper named in G5 | `groups/dossiers/G5_public_markets.md` | Geltner (1993 | present |
| 2.6 #4 | Geltner paper named in G6 | `groups/dossiers/G6_private_credit.md` | Geltner 1993 | present |
| 2.6 #4 | Geltner paper named in G9 | `groups/dossiers/G9_synthetic_data.md` | Geltner (1993) | present |
| 2.3 G8 | Shin & Stulz NBER 5639 pointer dropped (outside the corrections section) | `groups/dossiers/G8_org_tpa_economics.md` | NBER 5639 | absent (ok) |
| 2.3 G5 | Almgren & Chriss no longer dated 2000 | `groups/dossiers/G5_public_markets.md` | Almgren & Chriss (2000) | absent (ok) |
| 2.3 G8 | Lamont 57–82 removed from the reference | `groups/dossiers/G8_org_tpa_economics.md` | 52(1):57–82 | absent (ok) |
| 2.4 #14 | 'A central Treasury owns' removed from G7 | `groups/dossiers/G7_liquidity_ladder.md` | A central Treasury owns | absent (ok) |
| 2.3 12 | 'Sakana AI (2026' no longer the Nature author in 12 | `dossiers/12_agentic_ai.md` | Sakana AI (2026-03-26). The AI Scientist | absent (ok) |

Result: 132 of 132 prescription checks pass.

### 2.5 Targeted presence checks (232)

All 31 `barrier_rerun` changes, every non-section `consistency_edit` change, and a spread of the other kinds. "present" means the reported new text was found (normalized match); "present (read)" means the reported wording differed slightly and the line was read and confirmed.

| ID | Kind | File | Line(s) | Result |
|---|---|---|---|---|
| B01 | barrier_rerun | `groups/dossiers/G4_coinvest.md` | 425 | present |
| B02 | barrier_rerun | `groups/dossiers/G4_coinvest.md` | 422 | present |
| B03 | barrier_rerun | `groups/dossiers/G4_coinvest.md` | 428 | present |
| B04 | barrier_rerun | `groups/dossiers/G4_coinvest.md` | 430 | present |
| B05 | barrier_rerun | `groups/dossiers/G4_coinvest.md` | 557 | present |
| B06 | barrier_rerun | `groups/dossiers/G4_coinvest.md` | 499 | present |
| B07 | barrier_rerun | `groups/verification/G4_coinvest.verify.md` | 198 | present |
| B08 | barrier_rerun | `groups/verification/G4_coinvest.verify.md` | 135 | present |
| B09 | barrier_rerun | `groups/verification/G4_coinvest.verify.md` | 143 | present |
| B10 | barrier_rerun | `groups/verification/G4_coinvest.verify.md` | 226 | present |
| B11 | barrier_rerun | `groups/clusters/GC1_private_groups.md` | 34 | present |
| B12 | barrier_rerun | `groups/clusters/GC1_private_groups.md` | 85 | present |
| B13 | barrier_rerun | `groups/clusters/GC1_private_groups.md` | 163 | present |
| B14 | barrier_rerun | `groups/clusters/GC1_private_groups.md` | 168 | present |
| B15 | barrier_rerun | `groups/clusters/GC1_private_groups.md` | 169 | present |
| B16 | barrier_rerun | `addenda/gap_01.md` | 28 | present |
| B17 | barrier_rerun | `addenda/gap_01.md` | 71 | present |
| B18 | barrier_rerun | `groups/addenda/gap_04.md` | 53 | present |
| B19 | barrier_rerun | `groups/addenda/gap_04.md` | 69 | present |
| B20 | barrier_rerun | `groups/addenda/gap_04.md` | 319 | present |
| B21 | barrier_rerun | `groups/addenda/gap_04.md` | 349, 355 | present |
| B22 | barrier_rerun | `00_SYNTHESIS.md` | 132 | present |
| B23 | barrier_rerun | `00_SYNTHESIS.md` | 854 | present |
| B24 | barrier_rerun | `00_SYNTHESIS.md` | 716, 2307 | present |
| B25 | barrier_rerun | `groups/01_GROUPS_SYNTHESIS.md` | 144 | present |
| B26 | barrier_rerun | `groups/01_GROUPS_SYNTHESIS.md` | 145 | present |
| B27 | barrier_rerun | `groups/01_GROUPS_SYNTHESIS.md` | 146 | present |
| B28 | barrier_rerun | `groups/01_GROUPS_SYNTHESIS.md` | 550 | present |
| B29 | barrier_rerun | `groups/01_GROUPS_SYNTHESIS.md` | 568 | present |
| B30 | barrier_rerun | `groups/01_GROUPS_SYNTHESIS.md` | 569 | present |
| B31 | barrier_rerun | `groups/01_GROUPS_SYNTHESIS.md` | 1100 | present |
| U-G4 | usage | `groups/dossiers/G4_coinvest.md` | 597 | present |
| C01 | inconsistency | `verification/01_mpo.verify.md` | 139 | present |
| C02a | consistency_edit | `dossiers/02_endowment_swf.md` | 563 | present |
| C02b | consistency_edit | `dossiers/02_endowment_swf.md` | 591 | present |
| C02d | consistency_edit | `verification/02_endowment_swf.verify.md` | 106, 133 | present |
| C02e | consistency_edit | `verification/02_endowment_swf.verify.md` | 127 | present |
| C04a | consistency_edit | `dossiers/04_pe_cashflows.md` | 53 | present |
| C04b | consistency_edit | `dossiers/04_pe_cashflows.md` | 484 | present |
| C07b | consistency_edit | `verification/07_return_fusion.verify.md` | see §2.3 | present (read) |
| C08a | consistency_edit | `dossiers/08_action_valuation.md` | see §2.3 | present (read) |
| C08b | consistency_edit | `dossiers/08_action_valuation.md` | 201 | present |
| C09b | consistency_edit | `verification/09_overlay.verify.md` | 67 | present |
| C09c | consistency_edit | `verification/09_overlay.verify.md` | 157 | present |
| C10b | consistency_edit | `verification/10_scenarios_robustness.verify.md` | see §2.3 | present (read) |
| C11b | consistency_edit | `verification/11_objectives.verify.md` | see §2.3 | present (read) |
| C12a | consistency_edit | `dossiers/12_agentic_ai.md` | 782 | present |
| C13a | consistency_edit | `dossiers/13_paper_deepread.md` | 493 | present |
| C14a | consistency_edit | `dossiers/14_ic_deliberation.md` | see §2.3 | present (read) |
| C14b | consistency_edit | `dossiers/14_ic_deliberation.md` | 326 | present |
| C14c | consistency_edit | `dossiers/14_ic_deliberation.md` | 553 | present |
| CG2a | consistency_edit | `groups/dossiers/G2_secondaries_group.md` | 271 | present |
| CG2b | consistency_edit | `groups/verification/G2_secondaries_group.verify.md` | 188 | present |
| CG4a | consistency_edit | `groups/dossiers/G4_coinvest.md` | 7 | present |
| CG5a | consistency_edit | `groups/dossiers/G5_public_markets.md` | 925 | present |
| CG5b | consistency_edit | `groups/dossiers/G5_public_markets.md` | 856 | present |
| CG5c | consistency_edit | `groups/dossiers/G5_public_markets.md` | 826 | present |
| CG6a | consistency_edit | `groups/dossiers/G6_private_credit.md` | 744 | present |
| CG6b | consistency_edit | `groups/verification/G6_private_credit.verify.md` | 155 | present |
| CG7a | consistency_edit | `groups/dossiers/G7_liquidity_ladder.md` | 826 | present |
| CG7b | consistency_edit | `groups/dossiers/G7_liquidity_ladder.md` | 940 | present |
| CG8a | consistency_edit | `groups/dossiers/G8_org_tpa_economics.md` | 751, 795 | present |
| CMA1 | consistency_edit | `addenda/gap_01.md` | 41 | present |
| CMA2 | consistency_edit | `addenda/gap_02.md` | 101 | present |
| CMS1 | consistency_edit | `00_SYNTHESIS.md` | 114 | present |
| CMS2 | consistency_edit | `00_SYNTHESIS.md` | see §2.3 | present (read) |
| CMS3 | consistency_edit | `00_SYNTHESIS.md` | 1184, 2295 | present |
| CMS4 | consistency_edit | `00_SYNTHESIS.md` | see §2.3 | present (read) |
| CMS5 | consistency_edit | `00_SYNTHESIS.md` | 1188 | present |
| CMS6 | consistency_edit | `00_SYNTHESIS.md` | 1193 | present |
| CMS7 | consistency_edit | `00_SYNTHESIS.md` | 1624 | present |
| CMS8 | consistency_edit | `00_SYNTHESIS.md` | 1649, 1652 | present |
| CMS9 | consistency_edit | `00_SYNTHESIS.md` | 927 | present |
| CMS10 | consistency_edit | `00_SYNTHESIS.md` | 1185 | present |
| CMS11 | consistency_edit | `00_SYNTHESIS.md` | 1218 | present |
| CMS12 | consistency_edit | `00_SYNTHESIS.md` | 1766 | present |
| CMS13 | consistency_edit | `00_SYNTHESIS.md` | 1815 | present |
| CMS14 | consistency_edit | `00_SYNTHESIS.md` | 1892 | present |
| CMS16 | consistency_edit | `00_SYNTHESIS.md` | 1320 | present |
| S01a | recheck | `dossiers/01_mpo.md` | 40 | present |
| S01b | recheck | `dossiers/01_mpo.md` | 40, 799, 800 | present |
| S01c | missing_reference | `dossiers/01_mpo.md` | 791 | present |
| S01d | metadata | `dossiers/01_mpo.md` | 744, 805 | present |
| S01e | metadata | `dossiers/01_mpo.md` | 772 | present |
| S02a | usage | `dossiers/02_endowment_swf.md` | 135 | present |
| S02b | missing_reference | `dossiers/02_endowment_swf.md` | 589 | present |
| S02c | metadata | `dossiers/02_endowment_swf.md` | 627, 658 | present |
| S02d | metadata | `dossiers/02_endowment_swf.md` | 592 | present |
| S03a | metadata | `dossiers/03_sovereign_alm.md` | 151 | present |
| S03b | metadata | `verification/03_sovereign_alm.verify.md` | 290 | present |
| S03c | missing_reference | `dossiers/03_sovereign_alm.md` | 491 | present |
| S04a | metadata | `dossiers/04_pe_cashflows.md` | 508 | present |
| S04b | metadata | `dossiers/04_pe_cashflows.md` | 518 | present |
| S04c | usage | `dossiers/04_pe_cashflows.md` | 104 | present |
| S04d | inconsistency | `dossiers/04_pe_cashflows.md` | 84 | present |
| S04e | missing_reference | `dossiers/04_pe_cashflows.md` | 506 | present |
| S04f | metadata | `dossiers/04_pe_cashflows.md` | 510 | present |
| S04g | usage | `dossiers/04_pe_cashflows.md` | see §2.3 | present (read) |
| S05a | usage | `dossiers/05_secondaries_navfin.md` | 69 | present |
| S05b | metadata | `dossiers/05_secondaries_navfin.md` | 509, 548 | present |
| S05c | missing_reference | `dossiers/05_secondaries_navfin.md` | 529 | present |
| S05d | missing_reference | `dossiers/05_secondaries_navfin.md` | 135 | present |
| S06a | usage | `dossiers/06_leverage.md` | 44 | present |
| S06b | metadata | `dossiers/06_leverage.md` | 512, 577 | present |
| S06c | metadata | `dossiers/06_leverage.md` | 509 | present |
| S07a | usage | `dossiers/07_return_fusion.md` | 160 | present |
| S07b | usage | `dossiers/07_return_fusion.md` | 191 | present |
| S07c | usage | `dossiers/07_return_fusion.md` | 226 | present |
| S07d | metadata | `dossiers/07_return_fusion.md` | 567, 604 | present |
| S07e | inconsistency | `dossiers/07_return_fusion.md` | 534, 599 | present |
| S07f | metadata | `dossiers/07_return_fusion.md` | 525, 597 | present |
| S07g | usage | `dossiers/07_return_fusion.md` | 77 | present |
| S08a | metadata | `dossiers/08_action_valuation.md` | 1039 | present |
| S08b | usage | `dossiers/08_action_valuation.md` | 154, 1048 | present |
| S08c | usage | `dossiers/08_action_valuation.md` | 438, 1050 | present |
| S09a | usage | `dossiers/09_overlay.md` | 147, 994 | present |
| S09b | usage | `dossiers/09_overlay.md` | 228 | present |
| S09c | usage | `dossiers/09_overlay.md` | 245 | present |
| S09d | usage | `dossiers/09_overlay.md` | 247 | present |
| S09e | metadata | `dossiers/09_overlay.md` | 918, 1001 | present |
| S09f | metadata | `dossiers/09_overlay.md` | 922, 1002 | present |
| S09g | missing_reference | `dossiers/09_overlay.md` | 984 | present |
| S10a | recheck | `dossiers/10_scenarios_robustness.md` | 237 | present |
| S10b | recheck | `dossiers/10_scenarios_robustness.md` | 237, 609 | present |
| S10c | usage | `dossiers/10_scenarios_robustness.md` | 104, 604 | present |
| S10d | usage | `dossiers/10_scenarios_robustness.md` | 343, 613 | present |
| S10e | missing_reference | `dossiers/10_scenarios_robustness.md` | 435 | present |
| S10f | metadata | `dossiers/10_scenarios_robustness.md` | 545, 619 | present |
| S10g | metadata | `dossiers/10_scenarios_robustness.md` | 596, 630 | present |
| S10h | metadata | `dossiers/10_scenarios_robustness.md` | 589, 628 | present |
| S10i | metadata | `dossiers/10_scenarios_robustness.md` | 573, 624 | present |
| S10j | recheck | `dossiers/10_scenarios_robustness.md` | 579 | present |
| S10k | metadata | `dossiers/10_scenarios_robustness.md` | 111, 606 | present |
| S11a | missing_reference | `dossiers/11_objectives.md` | 565 | present |
| S11b | recheck | `dossiers/11_objectives.md` | 125, 126, 127, 128 | present |
| S11c | metadata | `dossiers/11_objectives.md` | 422 | present |
| S11d | recheck | `dossiers/11_objectives.md` | 416 | present |
| S12a | metadata | `dossiers/12_agentic_ai.md` | 701, 811 | present |
| S12b | metadata | `dossiers/12_agentic_ai.md` | 730, 812 | present |
| S12c | usage | `dossiers/12_agentic_ai.md` | 37, 813 | present |
| S12d | usage | `dossiers/12_agentic_ai.md` | 165, 442, 444, 475 | present |
| S12e | usage | `dossiers/12_agentic_ai.md` | 470, 817 | present |
| S12f | usage | `dossiers/12_agentic_ai.md` | 473 | present |
| S12g | usage | `dossiers/12_agentic_ai.md` | 21 | present |
| S13a | usage | `dossiers/13_paper_deepread.md` | see §2.3 | present (read) |
| S13b | usage | `dossiers/13_paper_deepread.md` | 192 | present |
| S13c | usage | `dossiers/13_paper_deepread.md` | 544 | present |
| S13d | metadata | `dossiers/13_paper_deepread.md` | 1142, 1189 | present |
| S14a | usage | `dossiers/14_ic_deliberation.md` | 134, 1057 | present |
| S14b | usage | `dossiers/14_ic_deliberation.md` | 847 | present |
| S14c | recheck | `dossiers/14_ic_deliberation.md` | 294, 1061 | present |
| S14d | recheck | `dossiers/14_ic_deliberation.md` | 349, 992, 1066 | present |
| S14e | recheck | `dossiers/14_ic_deliberation.md` | 1029 | present |
| S14f | metadata | `dossiers/14_ic_deliberation.md` | 1044, 1079 | present |
| S14g | usage | `dossiers/14_ic_deliberation.md` | 38, 342 | present |
| SG1a | inconsistency | `groups/dossiers/G1_pe_primaries.md` | 141, 565 | present |
| SG1b | metadata | `groups/dossiers/G1_pe_primaries.md` | 566 | present |
| SG1c | metadata | `groups/dossiers/G1_pe_primaries.md` | 576 | present |
| SG1d | metadata | `groups/dossiers/G1_pe_primaries.md` | 568, 614 | present |
| SG2a | usage | `groups/dossiers/G2_secondaries_group.md` | 75 | present |
| SG2b | missing_reference | `groups/dossiers/G2_secondaries_group.md` | 847 | present |
| SG2c | missing_reference | `groups/dossiers/G2_secondaries_group.md` | 170 | present |
| SG2d | missing_reference | `groups/dossiers/G2_secondaries_group.md` | 649 | present |
| SG2e | usage | `groups/dossiers/G2_secondaries_group.md` | 698 | present |
| SG3a | usage | `groups/dossiers/G3_cap_solutions.md` | 32, 287 | present |
| SG3b | usage | `groups/dossiers/G3_cap_solutions.md` | 298 | present |
| SG3c | missing_reference | `groups/dossiers/G3_cap_solutions.md` | 745 | present |
| SG3d | missing_reference | `groups/dossiers/G3_cap_solutions.md` | 744 | present |
| SG3e | recheck | `groups/dossiers/G3_cap_solutions.md` | 736 | present |
| SG3f | metadata | `groups/dossiers/G3_cap_solutions.md` | 734, 768 | present |
| SG4a | usage | `groups/dossiers/G4_coinvest.md` | 340 | present |
| SG4b | usage | `groups/dossiers/G4_coinvest.md` | 197 | present |
| SG4c | missing_reference | `groups/dossiers/G4_coinvest.md` | 667 | present |
| SG4d | missing_reference | `groups/dossiers/G4_coinvest.md` | 668 | present |
| SG4e | missing_reference | `groups/dossiers/G4_coinvest.md` | 669 | present |
| SG5a | metadata | `groups/dossiers/G5_public_markets.md` | 926 | present |
| SG5b | metadata | `groups/dossiers/G5_public_markets.md` | 858, 945 | present |
| SG5c | inconsistency | `groups/dossiers/G5_public_markets.md` | 207 | present |
| SG6a | usage | `groups/dossiers/G6_private_credit.md` | 128 | present |
| SG6b | usage | `groups/dossiers/G6_private_credit.md` | 374, 816 | present |
| SG6c | usage | `groups/dossiers/G6_private_credit.md` | 291 | present |
| SG6d | inconsistency | `groups/dossiers/G6_private_credit.md` | 802 | present |
| SG7a | usage | `groups/dossiers/G7_liquidity_ladder.md` | 125 | present |
| SG7b | usage | `groups/dossiers/G7_liquidity_ladder.md` | 220 | present |
| SG7c | usage | `groups/dossiers/G7_liquidity_ladder.md` | 341 | present |
| SG7d | missing_reference | `groups/dossiers/G7_liquidity_ladder.md` | 1007 | present |
| SG7e | missing_reference | `groups/dossiers/G7_liquidity_ladder.md` | 1009 | present |
| SG8a | metadata | `groups/dossiers/G8_org_tpa_economics.md` | 689 | present |
| SG8b | metadata | `groups/dossiers/G8_org_tpa_economics.md` | 688 | present |
| SG8c | missing_reference | `groups/dossiers/G8_org_tpa_economics.md` | 215, 785 | present |
| SG8d | usage | `groups/dossiers/G8_org_tpa_economics.md` | 113, 786 | present |
| SG9a | usage | `groups/dossiers/G9_synthetic_data.md` | 48 | present |
| SG9b | usage | `groups/dossiers/G9_synthetic_data.md` | 124 | present |
| SG9c | usage | `groups/dossiers/G9_synthetic_data.md` | 253 | present |
| SG9d | metadata | `groups/dossiers/G9_synthetic_data.md` | 770, 831 | present |
| SG9e | metadata | `groups/verification/G9_synthetic_data.verify.md` | 196 | present |
| SC1a | metadata | `clusters/C1_portfolio_math.md` | 521 | present |
| SC1b | missing_reference | `clusters/C1_portfolio_math.md` | 864, 888 | present |
| SC2a | usage | `clusters/C2_private_liquidity.md` | 153 | present |
| SC2b | metadata | `clusters/C2_private_liquidity.md` | 151 | present |
| SC3a | usage | `clusters/C3_liabilities_overlay.md` | 733, 998, 1027 | present |
| SC4a | usage | `clusters/C4_agentic_ic.md` | 108 | present |
| SC4b | inconsistency | `clusters/C4_agentic_ic.md` | 1084, 1133 | present |
| SC4c | usage | `clusters/C4_agentic_ic.md` | 779 | present |
| SGC1a | usage | `groups/clusters/GC1_private_groups.md` | 70, 303 | present |
| SGC1b | usage | `groups/clusters/GC1_private_groups.md` | 86 | present |
| SGC1c | inconsistency | `groups/clusters/GC1_private_groups.md` | 203 | present |
| SGC2a | usage | `groups/clusters/GC2_liquidity_org_data.md` | 335 | present |
| SGC2b | metadata | `groups/clusters/GC2_liquidity_org_data.md` | 96, 728 | present |
| SMA1 | usage | `addenda/gap_01.md` | 28, 240 | present |
| SMA2 | missing_reference | `addenda/gap_02.md` | 249 | present |
| SMA3 | usage | `addenda/gap_05.md` | 89 | present |
| SMA4 | recheck | `addenda/gap_05.md` | 90 | present |
| SMA5 | recheck | `addenda/gap_04.md` | 317, 346 | present |
| SGA1 | usage | `groups/addenda/gap_04.md` | 80 | present |
| SGA2 | missing_reference | `groups/addenda/gap_01.md` | 363 | present |
| SGA3 | metadata | `groups/addenda/gap_03.md` | 326 | present |
| SMS1 | usage | `00_SYNTHESIS.md` | 1363 | present |
| SMS2 | usage | `00_SYNTHESIS.md` | 1724, 2313 | present |
| SMS3 | usage | `00_SYNTHESIS.md` | 1551 | present |
| SMS4 | usage | `00_SYNTHESIS.md` | 554 | present |
| SMS5 | inconsistency | `00_SYNTHESIS.md` | 2079, 2333 | present |
| SMS6 | metadata | `00_SYNTHESIS.md` | 2142 | present |
| SMS7 | missing_reference | `00_SYNTHESIS.md` | 2277 | present |
| SGS1 | usage | `groups/01_GROUPS_SYNTHESIS.md` | 442 | present |
| SGS2 | metadata | `groups/01_GROUPS_SYNTHESIS.md` | 476 | present |
| SGS3 | usage | `groups/01_GROUPS_SYNTHESIS.md` | 489, 1568 | present |
| SGS4 | usage | `groups/01_GROUPS_SYNTHESIS.md` | 550 | present |
| SGS5 | recheck | `groups/01_GROUPS_SYNTHESIS.md` | 918 | present |
| SGS6 | inconsistency | `groups/01_GROUPS_SYNTHESIS.md` | 1419 | present |
| SGS7 | usage | `groups/01_GROUPS_SYNTHESIS.md` | 1490 | present |
| SGS8 | missing_reference | `groups/01_GROUPS_SYNTHESIS.md` | 1530, 1590 | present |

### 2.6 Corrections-section audit (60 files)

| File | Heading line / file length | Entries | Names its sources | Mentions the barrier re-run |
|---|---|---|---|---|
| `00_SYNTHESIS.md` | 2288 / 2368 | 65 | yes | yes |
| `addenda/gap_01.md` | 235 / 244 | 6 | yes | yes |
| `addenda/gap_02.md` | 260 / 263 | 2 | yes | no |
| `addenda/gap_03.md` | 316 / 320 | 3 | yes | no |
| `addenda/gap_04.md` | 344 / 348 | 3 | yes | no |
| `addenda/gap_05.md` | 282 / 296 | 11 | yes | no |
| `clusters/C1_portfolio_math.md` | 878 / 894 | 10 (+3 sub) | yes | yes |
| `clusters/C2_private_liquidity.md` | 1152 / 1167 | 9 (+3 sub) | yes | yes |
| `clusters/C3_liabilities_overlay.md` | 1016 / 1032 | 7 (+6 sub) | yes | yes |
| `clusters/C4_agentic_ic.md` | 1102 / 1142 | 19 (+13 sub) | yes | yes |
| `dossiers/01_mpo.md` | 795 / 814 | 16 | yes | yes |
| `dossiers/02_endowment_swf.md` | 630 / 662 | 18 (+11 sub) | yes | yes |
| `dossiers/03_sovereign_alm.md` | 1092 / 1113 | 18 | yes | yes |
| `dossiers/04_pe_cashflows.md` | 568 / 581 | 10 | yes | no |
| `dossiers/05_secondaries_navfin.md` | 533 / 549 | 13 | yes | no |
| `dossiers/06_leverage.md` | 571 / 585 | 12 | yes | yes |
| `dossiers/07_return_fusion.md` | 584 / 608 | 21 | yes | no |
| `dossiers/08_action_valuation.md` | 1045 / 1060 | 13 | yes | yes |
| `dossiers/09_overlay.md` | 990 / 1006 | 13 | yes | yes |
| `dossiers/10_scenarios_robustness.md` | 598 / 631 | 32 | yes | yes |
| `dossiers/11_objectives.md` | 631 / 648 | 14 | yes | no |
| `dossiers/12_agentic_ai.md` | 807 / 826 | 16 | yes | yes |
| `dossiers/13_paper_deepread.md` | 1176 / 1202 | 23 | yes | no |
| `dossiers/14_ic_deliberation.md` | 1053 / 1082 | 26 | yes | yes |
| `groups/01_GROUPS_SYNTHESIS.md` | 1561 / 1594 | 30 | yes | yes |
| `groups/addenda/gap_01.md` | 371 / 376 | 2 | yes | yes |
| `groups/addenda/gap_03.md` | 336 / 341 | 2 | yes | yes |
| `groups/addenda/gap_04.md` | 353 / 364 | 8 | yes | yes |
| `groups/clusters/GC1_private_groups.md` | 298 / 317 | 16 | yes | yes |
| `groups/clusters/GC2_liquidity_org_data.md` | 720 / 729 | 6 | yes | yes |
| `groups/dossiers/G1_pe_primaries.md` | 603 / 629 | 21 (+2 sub) | yes | yes |
| `groups/dossiers/G2_secondaries_group.md` | 853 / 868 | 12 | yes | yes |
| `groups/dossiers/G3_cap_solutions.md` | 751 / 770 | 16 | yes | no |
| `groups/dossiers/G4_coinvest.md` | 673 / 694 | 18 | yes | yes |
| `groups/dossiers/G5_public_markets.md` | 940 / 962 | 17 (+2 sub) | in prose or n/a | yes |
| `groups/dossiers/G6_private_credit.md` | 810 / 847 | 32 | yes | yes |
| `groups/dossiers/G7_liquidity_ladder.md` | 1013 / 1031 | 15 | yes | yes |
| `groups/dossiers/G8_org_tpa_economics.md` | 777 / 797 | 17 | yes | yes |
| `groups/dossiers/G9_synthetic_data.md` | 805 / 838 | 30 | yes | yes |
| `groups/verification/G1_pe_primaries.verify.md` | 181 / 186 | 2 | yes | no |
| `groups/verification/G2_secondaries_group.verify.md` | 294 / 304 | 7 | yes | no |
| `groups/verification/G3_cap_solutions.verify.md` | 320 / 322 | 1 | yes | no |
| `groups/verification/G4_coinvest.verify.md` | 246 / 255 | 6 | yes | yes |
| `groups/verification/G5_public_markets.verify.md` | 328 / 347 | 5 (+11 sub) | yes | yes |
| `groups/verification/G6_private_credit.verify.md` | 339 / 346 | 4 | yes | no |
| `groups/verification/G7_liquidity_ladder.verify.md` | 251 / 253 | 1 | in prose or n/a | no |
| `groups/verification/G8_org_tpa_economics.verify.md` | 298 / 301 | 2 | yes | no |
| `groups/verification/G9_synthetic_data.verify.md` | 194 / 196 | 1 | in prose or n/a | no |
| `verification/01_mpo.verify.md` | 266 / 268 | 1 | in prose or n/a | no |
| `verification/02_endowment_swf.verify.md` | 256 / 267 | 6 (+3 sub) | yes | no |
| `verification/03_sovereign_alm.verify.md` | 288 / 290 | 1 | in prose or n/a | no |
| `verification/04_pe_cashflows.verify.md` | 278 / 280 | 1 | in prose or n/a | no |
| `verification/07_return_fusion.verify.md` | 274 / 276 | 1 | in prose or n/a | no |
| `verification/08_action_valuation.verify.md` | 273 / 275 | 1 | in prose or n/a | no |
| `verification/09_overlay.verify.md` | 259 / 263 | 3 | in prose or n/a | no |
| `verification/10_scenarios_robustness.verify.md` | 323 / 325 | 2 | in prose or n/a | no |
| `verification/11_objectives.verify.md` | 365 / 368 | 2 | in prose or n/a | no |
| `verification/12_agentic_ai.verify.md` | 255 / 257 | 1 | in prose or n/a | no |
| `verification/13_paper_deepread.verify.md` | 256 / 262 | 3 | yes | no |
| `verification/14_ic_deliberation.verify.md` | 307 / 309 | 1 | yes | no |

Every section is the last section of its file (no heading follows it).

## 3. Changes by file

Before → after text is abridged from the editors' reports (quotes in the reports were truncated). "Verified" names the check that covers the row: a check ID from §2.5, `section audit` (§2.6), `read`, `grep`, `recomputed` (§2.3), `publisher page` or `Crossref` (§2.3), and `tokens` when every DOI, volume(issue) and page range in the new text was found in the file. A dash means the row was not individually sampled; its presence is attested only by the file's own corrections section.

### `dossiers/01_mpo.md` (27 changes; fix:01)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | recheck | §1 item 3(d), l.40 | "~1,000 scenarios for ~20 parameters; ~60,000 for 1,500 variables" → "exact Campi–Garatti bound needs 631 (d=20) and 31,785 (d=1,500) at ε=5%, β=1%, convex program" | S01a; S01b; recomputed |
| 2 | recheck | §2.5 item 2, heading and first bullet | "(Calafiore and Campi 2006; Campi and Garatti 2008) … exact for fully supported problems" → "scenario approach (Calafiore & Campi 2006) with the exact bound of Campi & Garatti (2008, Thm 2.4)" | – |
| 3 | recheck | §2.5 item 2, new bullet | convexity only implicit → "guarantee requires a convex scenario program with the constraint enforced on all N scenarios; integer actions or non-convex tuning void it" | – |
| 4 | recheck | §2.5 item 2, [I] N bullet | "about 1,000 / about 60,000" → "exact bound N=631 (d=20) and N=31,785 (d=1,500) [corrected 2026-10-18]" | S01b; recomputed; tokens |
| 5 | metadata | §2.5 item 3, in-text | "Mohajerin Esfahani and Kuhn" → "Mohajerin Esfahani and Kuhn (2018)" | – |
| 6 | metadata | §10 ref 53 | arXiv:1505.05116, journal version not given → "(2018) … performance guarantees and tractable reformulations, Math. Programming 171(1–2):115–166" | S01e; tokens |
| 7 | metadata | §2.2, in-text | "(Campbell and Viceira 2002, (unverified))" → "(Campbell and Viceira 2002)" | – |
| 8 | metadata | §10 ref 16 (Campbell & Viceira) | "OUP (unverified in-session)" → "+ DOI 10.1093/0198296940.001.0001 (Crossref-confirmed)" | tokens |
| 9 | missing_reference | §3.1 scenario-generation bullet | "A published comment shows …" → "A published comment (Klaassen 2002) shows …" | – |
| 10 | missing_reference | §10 new ref 72 | (none) → "Klaassen (2002), Comment on 'Generating scenario trees…', Management Science 48(11):1512–1516, DOI 10.1287/mnsc.48.11.1512.261" | S01c; tokens |
| 11 | metadata | §3.1, in-text | "Pflug-Pichler's nested distance (unverified)" → "Pflug and Pichler's (2012) nested distance" | – |
| 12 | metadata | §10 ref 59 (Pflug & Pichler) | "SIAM J. Optim. 22(1) (unverified)" → "22(1):1–23, DOI 10.1137/110825054 (Crossref-confirmed)" | tokens |
| 13 | metadata | §3.2, in-text | "Dowson's policy graph" → "Dowson's (2020) policy graph" | – |
| 14 | metadata | §10 ref 25 (Dowson) | Optimization Online preprint, journal version unverified → "(2020) Networks 76(1):3–23, DOI 10.1002/net.21932; preprint kept" | S01d; tokens |
| 15 | metadata | §3.5, in-text | "(Calafiore 2008, venue details unverified)" → "(Calafiore 2008)" | – |
| 16 | metadata | §10 ref 14 (Calafiore) | "Automatica (volume and pages unverified)" → "Automatica 44(10):2463–2473, DOI 10.1016/j.automatica.2008.02.007; author copy kept" | tokens |
| 17 | metadata | §3.6 overfitting, in-text | "(Bailey et al. 2017, (unverified))" → "(Bailey et al. 2017)" | – |
| 18 | metadata | §10 ref 4 (Bailey et al., PBO) | "J. Computational Finance (unverified; SSRN 403)" → "20(4):39–69 (first published 19 Sep 2016), DOI 10.21314/jcf.2016.322; SSRN preprint" | publisher page; tokens |
| 19 | metadata | §10 ref 63 (Rockafellar & Uryasev) | "J. Risk 2(3) (volume and pages from memory)" → "2(3):21–41, DOI 10.21314/JOR.2000.038; author copy" | tokens |
| 20 | metadata | §2.1, in-text | "[S Powell 2019; arXiv:1912.03513]" → "[S Powell 2019; Powell 2021, preprint arXiv:1912.03513]" | – |
| 21 | metadata | §10 ref 62 (Powell) | arXiv:1912.03513 only → "Powell (2021), chapter in Handbook of Reinforcement Learning and Control; preprint kept" | – |
| 22 | metadata | §10 ref 10 (Brandt et al.) | RFS 18(3):831–873 with NBER link → "+ DOI 10.1093/rfs/hhi019 (Crossref-confirmed); WP link kept" | tokens |
| 23 | metadata | §10 ref 12 (Brown, Dimmock, Kang & Weisbenner) | short title, NBER link → "full title (…: evidence and implications), DOI 10.1257/aer.104.3.931" | tokens |
| 24 | metadata | §10 ref 19 (Cariño et al.) | "The Russell-Yasuda Kasai model" → full subtitle "…: an asset/liability model for a Japanese insurance company using multistage stochastic programming" | – |
| 25 | metadata | §10 ref 49 (Luxenberg et al.) | arXiv entry with note → "arXiv entry kept; proceedings version (five authors) ICAIF '22 pp. 249–256, DOI 10.1145/3533271.3561769 added" | read; tokens |
| 26 | metadata | §10 ref 51 (Merton 1993) | "In Clotfelter and Rothschild (eds.) …" → "ch. 7, pp. 211–242; NBER chapter" | tokens |
| 27 | consistency_edit | end of file | (none) → "Citation corrections (2026-10-18)": sources note (barrier re-run n/a) + 16 entries | section audit; tokens |

### `verification/01_mpo.verify.md` (2 changes; fix:01)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | inconsistency | §4 'Problems to fix' | (no line) → "Erratum: the Dowson row has the two titles the wrong way round; Crossref 10.1002/net.21932 gives Networks 76(1):3–23 the dossier's title" | C01; tokens |
| 2 | consistency_edit | end of file | (none) → corrections section with one line recording the Dowson erratum | section audit |

### `dossiers/02_endowment_swf.md` (25 changes; fix:02)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §2.6 Ennis paragraph (alpha range) | "alphas −1.1% to −1.8% … for 43 large endowments" → "Ennis (2021a): alphas for six fund-size cohorts; of the 43 largest, none outperformed significantly, one in four underperformed" | S02a |
| 2 | usage | §2.6 Ennis paragraph (−1.87%) | "−1.87% a year vs passive … costs 1–2%" → "costs 1–2% [S]; a later Ennis paper reports −1.87% for endowments >$1bn over 12 years to June 2020" | – |
| 3 | metadata | §2.7 insurance dividend theory | "(de Finetti 1957; unverified)" → "(de Finetti 1957; original not indexed, title and venue from a citing reference, see §10)" | – |
| 4 | metadata | §2.7 actuarial funding | "(Dufresne 1988; Owadally & Haberman 1999, 2004; unverified details)" → tag removed | – |
| 5 | metadata | §4 endowment-model performance | "(Lerner, Schoar & Wang 2008; unverified details)" → tag removed | – |
| 6 | metadata | §5 reference-portfolio role | "(CFA Institute guide, July 2026)" → "(Urwin & Hayman, CFA Institute guide, July 2026)" | – |
| 7 | metadata | §7 algorithms | "(Powell 2019, EJOR; unverified details)" → tag removed | – |
| 8 | consistency_edit | §8 data gaps | "… de Finetti, Dufresne and Owadally–Haberman bibliographic details" → "… the original of de Finetti (1957), known only from a citing reference [Dufresne and O–H now verified]" | C02a |
| 9 | metadata | §10 ref 2 (Merton 1993) | no chapter or pages → "ch. 7, pp. 211–242" | tokens |
| 10 | metadata | §10 ref 3 (Dybvig 1999) | FAJ 55(1):49–62 → "+ DOI 10.2469/faj.v55.n1.2241 (OpenAlex-confirmed)" | tokens |
| 11 | metadata | §10 ref 4 (Dybvig 1995) | short title, "details unverified" → full title (…: optimal dynamic consumption and investment given intolerance for any decline in standard of living) | – |
| 12 | metadata | §10 ref 5 (Dimmock, Wang & Yang) | MS 70(3):1554–1579 → "+ DOI 10.1287/mnsc.2023.4759 (OpenAlex-confirmed)" | tokens |
| 13 | metadata | §10 ref 7 (Brown et al. 2014) | short title → "full title (…: evidence and implications), DOI 10.1257/aer.104.3.931" | tokens |
| 14 | metadata | §10 ref 10 → 10(a) (Ennis) | single SSRN 3614875 entry → "two papers; (a) Ennis (2021a) Endowment performance, J. Investing 30(3):6–20, DOI 10.3905/joi.2021.1.166; WP SSRN 3614875" | grep; tokens |
| 15 | missing_reference | §10 ref 10(b) (Ennis) | −1.87% cited to SSRN 3614875 → "(b) Ennis (2021b) Failure of the endowment model, JPM 47(5):128–143, DOI 10.3905/jpm.2021.1.217 [attribution unverified]" | S02b; tokens |
| 16 | consistency_edit | §10 heading of 'not verified' list | "Not verified in-session" → "Further theory references … now verified via Crossref or OpenAlex unless flagged" | C02b |
| 17 | metadata | §10 de Finetti (1957) | "de Finetti (1957);" → "Su un'impostazione alternativa della teoria collettiva del rischio, Trans. XVth Int. Congress of Actuaries 2:433–443 [unverified]" | S02d; tokens |
| 18 | metadata | §10 Dufresne (1988) | short → "Moments of pension contributions and fund levels when rates of return are random, JIA 115(3):535–544 [title unverified: Crossref reads 'Movements']" | tokens |
| 19 | metadata | §10 Owadally & Haberman (1999, 2004) | short → full NAAJ entries | – |
| 20 | metadata | §10 Lerner, Schoar & Wang (2008) | short → "Secrets of the academy…, JEP 22(3):207–222" | tokens |
| 21 | metadata | §10 Powell (2019) | short → "A unified framework for stochastic optimization, EJOR 275(3):795–821, with DOI" | tokens |
| 22 | metadata | §10 Constantinides (1990) | short → "Habit formation…, JPE 98(3):519–543, DOI 10.1086/261693" | tokens |
| 23 | metadata | §10 Kydland & Prescott (1977) | short → "Rules rather than discretion…, JPE 85(3):473–491, with DOI" | tokens |
| 24 | metadata | §10 ref 29 (CFA TPA guide) | "CFA Institute RPC (Jul 2026) …" → "Urwin & Hayman (2026), The Total Portfolio Approach (TPA): A Practical Guide…, DOI 10.56227/26.1.20" | S02c; tokens |
| 25 | consistency_edit | end of file | (none) → corrections section, one line per change; barrier, re-check and §2.6 sets n/a | section audit |

### `verification/02_endowment_swf.verify.md` (6 changes; fix:02)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | consistency_edit | §3 claims table row 17 (Ennis) | "… costs of 1–2% are confirmed" → "+ [later paper probably Ennis (2021), Failure of the Endowment Model, JPM 47(5):128–143]" | C02d; tokens |
| 2 | metadata | §4 Merton (1993) row | "Correct (Chapter 7). WP number not re-checked" → "+ [ch. 7 pp. 211–242 confirmed; NBER WP 3820 (Aug 1991) confirmed]" | tokens |
| 3 | consistency_edit | §4 Dybvig (1995) row | "Can be upgraded to verified" → "+ [upgraded in the dossier, with the full title]" | C02e |
| 4 | metadata | §4 Ennis (2020) row | "Garbled … Split into two references" → "+ [OpenAlex: SSRN 3614875 is the 2020 WP 'Endowment Performance and the Demise of the Multi-Asset-Class Model' …]" | – |
| 5 | metadata | §4 Urwin & Hayman row | "The reference omits the authors" → "+ [OpenAlex: Roger Urwin and Genevieve Hayman, 28 Jul 2026, DOI 10.56227/26.1.20]" | tokens |
| 6 | consistency_edit | end of file | (none) → corrections section (log quotes describe pre-correction text; five row annotations listed) | section audit |

### `dossiers/03_sovereign_alm.md` (21 changes; fix:03)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §2.2 empirical counterpoint, l.151–153 | "Moutanabbir & Noureldin (2018, ERF WP 1172)" → "(2020, IREF 69:708–730) … in their working-paper version (ERF WP 1172, 2018)" | S03a; tokens |
| 2 | metadata | §2.4 shock list, l.198 | "Ready (2018, RoF 22:155)" → "RoF 22:155–176" | tokens |
| 3 | metadata | §3.1 table, Schwartz–Smith row | [U] → [S] | – |
| 4 | recheck | §3.1 table, MS-VAR row | "Hamilton 1989 [U]" → "[S]" | – |
| 5 | metadata | §3.3 item 4 | "Meucci 2008 [U]" → "[S]" | – |
| 6 | metadata | §3.3 item 6 | "Breuer et al. 2009 [U]" → "[S]" | – |
| 7 | recheck | §3.4 table, CVaR hedge row | "Rockafellar–Uryasev 2000 [U]" → "[S]" | – |
| 8 | metadata | §3.4 table, joint-state hybrids | "Stulz 1982 closed forms [U]" → "[S]" | – |
| 9 | missing_reference | §4.8 Mexico header | "(IMF blog, Valencia, March 2018)" → "+ academic companion: Ma & Valencia 2018, IMF WP/18/35" | S03c |
| 10 | metadata | §10 item 3 (Scherer 2011) | "JAI 13, 24–34" → "13(3), 24–34 (Winter 2011; Crossref dates it 31 Dec 2010), DOI 10.3905/jai.2011.13.3.024" | tokens |
| 11 | metadata | §10 item 6 (Moutanabbir & Noureldin) | "(2018) ERF WP 1172" → "(2020) IREF; WP 1172 kept as the source of figures" | – |
| 12 | metadata | §10 item 11 (Merton 1993) | no chapter → "ch. 7, pp. 211–242 (one listing gives 211–236)" | tokens |
| 13 | metadata | §10 item 14 (Baumeister & Hamilton) | short title → "+ ': revisiting the role of oil supply and demand shocks'" | – |
| 14 | metadata | §10 item 15 (Känzig 2021) | short title → "+ ': evidence from OPEC announcements'" | – |
| 15 | metadata | §10 item 16 (Ready 2018) | "22(1), 155–" → "155–176" | tokens |
| 16 | missing_reference | §10 item 20 (Valencia blog) | blog only → "+ academic companion Ma & Valencia (2018), IMF WP/18/35" | – |
| 17 | metadata | §10 item 22 header | "[U] Not verified in-session; standard citations" → "standard citations; (verified) per lit review or topic-10 re-check, [U] otherwise" | – |
| 18 | recheck | §10 item 22, Hamilton (1989) | "Econometrica 57(2);" → "57(2), 357–384, DOI 10.2307/1912559 (verified)" | tokens |
| 19 | recheck | §10 item 22, Rockafellar & Uryasev | "J. Risk 2(3);" → "2(3), 21–41, DOI 10.21314/JOR.2000.038 (verified)" | tokens |
| 20 | recheck | §10 item 22, O'Hagan et al. | short → full author list, subtitle, Wiley, DOI 10.1002/0470033312 | tokens |
| 21 | consistency_edit | end of file | (none) → corrections section (sources note) | section audit |

### `verification/03_sovereign_alm.verify.md` (1 changes; fix:03)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | end of file | (none) → "Erratum to §4 #13 and §2 A3: WP 1172 superseded by IREF 2020; figures stay sourced to the WP [unverified vs 2020 version]" | S03b |

### `dossiers/04_pe_cashflows.md` (17 changes; fix:04)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §10 Luxenberg et al., l.508 | nine-author arXiv entry → "Luxenberg, Boyd, van Beek, Cao & Kochenderfer (2022), ICAIF '22, 249–256, DOI 10.1145/3533271.3561769; preprint noted" | S04a; tokens |
| 2 | consistency_edit | §2.2 Luxenberg example, l.53 | "Their annual example uses …" → "Their annual example (in the arXiv preprint) uses …" | C04a |
| 3 | metadata | §10 Jeet et al. (2026), l.510 | "Jeet, V., et al. … Takahashi and Alexander's …" → "Jeet, Stucke & Partani (2026), A Crucial Enhancement to the Takahashi–Alexander Cash Flow Model, JPMI 24(3), 62–73, DOI 10.3905/jpmi.2026.1.010" | S04f; tokens |
| 4 | metadata | §10 Sorensen, Wang & Yang, l.518 | "RFS 27(2)" → "RFS 27(7), 1977–2021, DOI 10.1093/rfs/hhu013" | S04b; tokens |
| 5 | metadata | §10 Nadauld et al., l.530 | "(2016) NBER WP" → "(2019) JFE 132(3), 158–181" | tokens |
| 6 | usage | §2.6 Nadauld bullet, l.104 | "sellers' 0.974 … 3pp for funds aged 4–9" → "(2019, JFE): sellers' 0.976 (WP 0.974); age split from the WP" | S04c |
| 7 | consistency_edit | §8 working-paper versions bullet, l.484 | "GVN, SWY and Nadauld figures come from NBER WPs" → "GVN and SWY from WPs; Nadauld PMEs are JFE figures, age split from the WP" | C04b |
| 8 | inconsistency | §2.5 Geltner bullet, l.84–85 | "Geltner (1991, 1993): …" → two bullets: Geltner (1991) smoothing model [attribution unverified]; Geltner (1993) unsmoothing without efficient-market assumption | S04d |
| 9 | inconsistency | §3 methods table, unsmoothing row, l.127 | "(Geltner, GLM, CGR)" → "(Geltner 1991 inversion or Geltner 1993 procedure, GLM, CGR)" | grep |
| 10 | usage | §2.5 BGG smoothing sub-bullet, l.91 | "median weekly λ is 0.951" → "+ (working-paper figure)" | grep |
| 11 | usage | §2.5 BGG noise sub-bullet, l.92 | "NAV noise 4.6% mean, 3.1% median" → "+ (working-paper figures)" | – |
| 12 | usage | §6.3 E7 smoothing default, l.321 | "λ_q≈0.5 (from BGG)" → "0.5 is this stream's conversion of BGG's weekly λ (0.951^13≈0.52), not a BGG figure" | S04g |
| 13 | missing_reference | §8 'not verified' bullet, l.480–483 | "MSCI/Jeet model … could not find" → three items identified (Jeet 2020 SSRN 3775008; de Malherbe 2004; Tausch et al. 2022), all in §10 | – |
| 14 | missing_reference | §10 new entry: de Malherbe (2004) | (none) → "IJTAF 7(3), 193–230, DOI 10.1142/S0219024904002359" | S04e; tokens |
| 15 | missing_reference | §10 new entry: Tausch, Buchner & Schlüchtermann (2022) | (none) → "Modeling the Exit Cashflows of PE Fund Investments, J. Risk, with DOI [volume/pages unverified]" | – |
| 16 | missing_reference | §10 new entry: Jeet (2020) | (none) → "Modeling Private Investment Cash Flows With Market Sensitive Periodic Growth, SSRN, DOI 10.2139/ssrn.3775008" | tokens |
| 17 | consistency_edit | end of file | (none) → corrections section, plus 'checked, no change' lines (Giommetti, Mack) | section audit |

### `verification/04_pe_cashflows.verify.md` (2 changes; fix:04)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §4 erratum below table, l.143 | "Luxenberg … preprint only: Correct; Jeet: Correct" → "Erratum: Luxenberg published at ICAIF '22 with five authors; Jeet authors and title corrected" | – |
| 2 | consistency_edit | end of file | (none) → one line recording the §4 erratum | section audit |

### `dossiers/05_secondaries_navfin.md` (17 changes; fix:05)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §2.2 liquidity bullet, l.69 (Bollen–Sensoy) | "required return rises by up to 5–10pp [S]" → "5–10pp is the 2015 WP (p.2); published FM 2022: breakeven ≈ observed returns for moderately risk-tolerant LPs with ≤40% PE" | S05a |
| 2 | metadata | §10 ref 15 (Bollen & Sensoy) | WP link only → "+ note that 5–10pp is from the 2015 WP, not the published paper" | – |
| 3 | usage | §2.2, l.69 (Albuquerque et al.) | "I could not retrieve their estimates" → abstract-level findings (broker bid data) [full text not read] | – |
| 4 | metadata | §10 ref 16 (Albuquerque et al.) | "WP, Cass Business School; findings not retrieved" → "+ SSRN DOI 10.2139/ssrn.3182481 (Crossref)" | tokens |
| 5 | metadata | §2.2, l.69 (Maurin et al.) | "(Management Science); authorship as I recall" → "(Management Science 69(10), 2023); authorship confirmed" | tokens |
| 6 | metadata | §10 ref 17 (Maurin, Robinson & Strömberg) | no authors or year → "(2023) MS 69(10), 5740–5771, DOI 10.1287/mnsc.2022.4612" | tokens |
| 7 | metadata | §10 ref 14 (Nadauld et al.) | "JFE (DOI)" → "JFE 132(3), 158–181" | tokens |
| 8 | metadata | §10 ref 19 (WilmerHale) | "Secondary market for PE interests" → "Beaudoin, Berrent, Evans & Rothermel (2009), Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets, BLT 18(4)" | S05b; tokens |
| 9 | missing_reference | §2.3, l.77 | "(Dixit-Pindyck)" → "(Dixit and Pindyck 1994)" | – |
| 10 | missing_reference | §7 algorithms, l.448 | "Longstaff-Schwartz" → "Longstaff-Schwartz (2001)" | – |
| 11 | missing_reference | §7 pitfall 3, l.453 | "(Heckman-style)" → "(Heckman 1979)" | – |
| 12 | missing_reference | §10 new ref 37 | (none) → "Dixit & Pindyck (1994), Investment under Uncertainty, Princeton UP, DOI 10.1515/9781400830176" | tokens |
| 13 | missing_reference | §10 new ref 38 | (none) → "Longstaff & Schwartz (2001), RFS 14(1):113–147" | tokens |
| 14 | missing_reference | §10 new ref 39 | (none) → "Heckman (1979), Econometrica 47(1), 153–161, DOI 10.2307/1912352" | S05c; tokens |
| 15 | missing_reference | §3.2(3) CV election, l.135 | "[S: Evercore/HEC]" unidentified → "informed counterparties [I]; Evercore FY-2025 p.13 summarizing the fourth HEC Paris CV study (Gottschalg)" | S05d |
| 16 | metadata | §10 ref 6 (Evercore FY-2025) | report entry → "+ note locating the HEC study summary (p.13; methodology p.17)" | – |
| 17 | consistency_edit | end of file | (none) → corrections section (sources line + 13 entries) | section audit |

### `dossiers/06_leverage.md` (12 changes; fix:06)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §2.2 log-growth tag, l.44 | "[K: Merton 1971; Kelly 1956]" → "[K: Merton 1971, continuous time; Kelly 1956 = log-growth criterion for discrete bets]" | S06a |
| 2 | usage | §2.2 Kelly leverage tag, l.48 | "[V: Wikipedia summary of Kelly 1956]" → "[K: continuous-time log-utility result (Merton 1971); not in Kelly 1956]" | – |
| 3 | metadata | §10 Brown, Dimmock, Kang & Weisbenner | NBER w15861 [V] → "full title (…: Evidence and Implications), AER 104(3), DOI 10.1257/aer.104.3.931; WP noted" | S06c; tokens |
| 4 | metadata | §10 Gorton & Metrick, Haircuts | "NBER WP 15273" → "Gorton & Metrick (2010), Haircuts, FRB St. Louis Review 92(6): 507–520, DOI 10.20955/r.92.507-20" | S06b; tokens |
| 5 | usage | §10 Kelly (1956) | Wikipedia summary → "+ cited for the log-growth criterion only" | – |
| 6 | metadata | §10 MacLean, Thorp & Ziemba (2011) | short title → "+ ': Theory and Practice', DOI 10.1142/7598" | tokens |
| 7 | metadata | §10 Merton (1971) | JET 3(4): 373–413 → "+ DOI 10.1016/0022-0531(71)90038-X (Crossref)" | tokens |
| 8 | metadata | §10 Barro (1979) | "JPE 87(5)" → "87(5, Part 1): 940–971, DOI 10.1086/260807" | tokens |
| 9 | metadata | §10 Geanakoplos (2010) | "24: 1–65" → "24(1): 1–66, DOI 10.1086/648285" | tokens |
| 10 | metadata | §10 Stafford (2022) | RFS 35(1): 299–342 → "+ DOI 10.1093/rfs/hhab020 (online 2021)" | tokens |
| 11 | metadata | §10 Getmansky, Lo & Makarov | JFE 74(3): 529–609 → "+ DOI 10.1016/j.jfineco.2004.04.001" | tokens |
| 12 | consistency_edit | end of file | (none) → corrections section (11 entries + 'No change needed') | section audit |

### `dossiers/07_return_fusion.md` (26 changes; fix:07)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §3 methods table, Cooke row, l.160 | "performance weights won in 26 of 33 in-sample" → "beat equal weights in 32 of 33 in-sample and 26 of 33 on an out-of-sample validity index; OOS accuracy below equal weights" | S07a |
| 2 | usage | §4.5 Cooke bullet, l.211 | "33 post-2006 studies (320 experts), best in 26" → "33 professionally contracted studies 2006–2015 (320 experts [unverified]) …" | tokens |
| 3 | missing_reference | §10 ref 21 (Cooke) | Wikipedia link → "Colson & Cooke (2017), RESS 163:109–120, DOI 10.1016/j.ress.2017.02.003" | grep; tokens |
| 4 | usage | §4.2 BGG bullet, l.191 | "β ≈1.05/1.20; risk 33%/38%" → "published RFS: β ≈1.0 (buyout) / 1.4 (venture); total risk ≈33% / 40%" | S07b |
| 5 | metadata | §10 ref 14 (BGG) | UNC link → "+ DOI 10.1093/rfs/hhac045; UNC page carries the 2020 WP abstract" | tokens |
| 6 | usage | §4.6 market-data table, Nadauld row, l.226 | "0.974; 2006–2017 data" → "0.976 (WP 0.974); 2006–2014 transaction data" | S07c; tokens |
| 7 | metadata | §10 ref 50 (Nadauld et al.) | "JFE (DOI)" → "JFE 132(3):158–181; figures follow the published abstract; NBER w22404" | tokens |
| 8 | metadata | §10 ref 49 (Mincer & Zarnowitz) | "NBER.†" → "In J. Mincer (ed.), Economic Forecasts and Expectations, NBER, pp. 3–46" | S07d |
| 9 | metadata | §2.7 M–Z and Nordhaus bullets | "[†]" → "[S: Mincer & Zarnowitz 1969]" and "[S]" | grep |
| 10 | metadata | §10 ref 51 (Nordhaus) | "REStat 69(4):667–674.†" → dagger removed | – |
| 11 | metadata | §10 ref 7 (Bates & Granger) | rdrr.io link → "ORQ (now JORS) 20(4):451–468, DOI 10.1057/jors.1969.103" | S07f; tokens |
| 12 | inconsistency | §10 ref 16 (Bühlmann 1967) | Wikipedia link → "DOI 10.1017/S0515036100008989 (…8023 is the 1969 paper, ASTIN 5(2):157–165)" | S07e; Crossref; tokens |
| 13 | metadata | §10 ref 30 (Glahn & Lowry) | "11(8):1203–1211.†; Wikipedia MOS history" → "+ DOI 10.1175/1520-0450(1972)011<1203:TUOMOS>2.0.CO;2" | tokens |
| 14 | usage | §5 item 4 (MOS) | "conceived 1965, first issued 1968 [S]; EMOS [†]" → "NWS developed MOS [S: Glahn & Lowry 1972]; dates [unverified]; EMOS [S: Gneiting et al. 2005]" | grep |
| 15 | metadata | §3 methods table, EMOS row, l.155 | "[Gneiting et al. 2005†; MOS origin S]" → "[S: Gneiting et al. 2005; MOS origin: Glahn & Lowry 1972]" | – |
| 16 | metadata | §6.4 parameter table, ω_f row | "EMOS form [†]" → "EMOS form [S: Gneiting et al. 2005]" | – |
| 17 | metadata | §2.7 scoring bullets | "Gneiting & Raftery 2007†; Gneiting, Balabdaoui & Raftery 2007†" → daggers removed, [S:] | – |
| 18 | metadata | §1, §2.3, §2.6, §4.5 in-text daggers | daggers on Arkes & Blumer, Diebold & Pauly, Staw, Baron et al. → removed (Tetlock, Mellers keep †) | – |
| 19 | metadata | §10 refs 2, 5, 10, 23, 31, 32, 33, 35 | daggers → removed (audit confirmed works and metadata) | – |
| 20 | metadata | §10 ref 24 (Diebold & Shin) | "IJF 35(4) (journal details†)" → "35(4):1679–1691 (online 2018), DOI 10.1016/j.ijforecast.2018.09.006" | tokens |
| 21 | metadata | §10 ref 56 (Smith & Wallis) | "OBES 71(3) (details†)" → "71(3):331–355, DOI 10.1111/j.1468-0084.2008.00541.x" | tokens |
| 22 | recheck | §10 ref 55 (Smith & Winkler) | short title → full subtitle (…: Skepticism and postdecision surprise in decision analysis), DOI 10.1287/mnsc.1050.0451 | tokens |
| 23 | metadata | §10 ref 28 (Flyvbjerg, Skamris Holm & Buhl) | arXiv link → "+ note: Notice of Redundant Publication (JAPA 78(3):352, 2012)" | tokens |
| 24 | metadata | §10 ref 61 (Staw 1976) | "cited from memory†" → "verified by the 2026-10-18 audit; no dagger" | tokens |
| 25 | usage | §2.3 Bates & Granger sentence | "derive variance-minimizing weights … In matrix form" → "for a pair of forecasts …; later work writes the general case in matrix form" | S07g |
| 26 | consistency_edit | end of file | (none) → corrections section (21 entries) | section audit |

### `verification/07_return_fusion.verify.md` (2 changes; fix:07)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | consistency_edit | §3 after the tally line, l.114 | (none) → "Erratum: row 26 (Cooke 32/33 in-sample; 26/33 OOS) and row 17 (Nadauld 0.976) wrongly accepted; S&W title truncated; corrected tally C24 X4 R0 U2" | C07b |
| 2 | consistency_edit | end of file | (none) → corrections section (one entry) | section audit |

### `dossiers/08_action_valuation.md` (18 changes; fix:08)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §2.1 Ang, Papanikolaou & Westerfield, l.154 | "uncertainty … drives most of its cost" → "'a primary determinant of the cost of illiquidity' (abstract wording)" | S08b |
| 2 | usage | §2.1 Nadauld et al., l.165–167 | "0.974 for sellers … ~3pp ages 4–9" → "0.976 (JFE abstract; WP 0.974); 4–9-year split from the WP" | – |
| 3 | usage | §4 evidence table, buyer vs seller row, l.438 | "PME 1.023 vs 0.974 (~5pp; ~3pp)" → "1.023 vs 0.976 (~5pp); ~3pp for 4–9-year funds per the WP abstract (0.974)" | S08c |
| 4 | usage | §1 main results item 5, l.129 | "[S: Nadauld et al. 2019]" → "+ the 4–9-year figure is from the NBER WP 22404 abstract" | – |
| 5 | usage | §8 adverse selection, l.938 | "[S: Nadauld et al.]" → "[S: Nadauld et al., NBER WP 22404 abstract]" | – |
| 6 | metadata | §10 Nadauld et al., l.991 | "JFE (online 2018), DOI" → "JFE 132(3), 158–181; earlier version NBER WP 22404 (July 2016)" | tokens |
| 7 | metadata | §10 Udell & Boyd (2016), l.1006 | arXiv v2 → "Computational Optimization and Applications 64(2), 355–378 (online 25 Jan 2016), with DOI" | tokens |
| 8 | missing_reference | §6.1 placement, consumes item 1, l.512 | scenario cash flows → "+ Stream 04 builds that engine on Takahashi & Alexander (2002); resolves the orphan" | – |
| 9 | metadata | §10 Takahashi & Alexander (2002), l.995 | "JPM 28(2). DOI.†" → "28(2), 90–100 (Crossref)" | tokens |
| 10 | metadata | §10 header note on † items, l.972 | "details from memory, not re-read" → "first written from memory; confirmed against Crossref on 2026-10-18" | tokens |
| 11 | metadata | §10 Korteweg & Nagel (2016), l.986 | "71(3), 1437–1470.†" → "+ DOI 10.1111/jofi.12390 (Crossref)" | tokens |
| 12 | metadata | §10 Tversky & Kahneman (1974), l.1012 | "185(4157), 1124–1131.†" → "+ DOI 10.1126/science.185.4157.1124 (Crossref)" | tokens |
| 13 | consistency_edit | §2.5 Whittle mention, l.319 | "Whittle (1988; DOI checked, metadata from memory)" → "Whittle (1988)"; metadata in §10 (reported parenthetical not inserted) | read |
| 14 | metadata | §10 Cariño et al. (1994), l.1001 | short title → full subtitle | – |
| 15 | metadata | §10 Gribik, Hogan & Pope, l.1039 | "Not verified … Gribik et al. (2007)" → "Market-clearing electricity prices and energy uplift, HEPG WP Dec 2007; HKS page; index dates it 2008" | S08a |
| 16 | missing_reference | §10 named-only works (Davis & Norman, Hawkins, Myers & Majd) | "Not verified this session" → "named for completeness only (verified 2026-10-18), full entries; Myers & Majd details [unverified]" | tokens |
| 17 | consistency_edit | §2.2 Davis–Norman, l.201 | "Davis–Norman" → "Davis–Norman (1990)" | C08b |
| 18 | consistency_edit | end of file | (none) → corrections section (one line per change + 'no change needed' line) | section audit |

### `verification/08_action_valuation.verify.md` (1 changes; fix:08)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | consistency_edit | end of file (erratum to claim #18) | (no erratum) → "Erratum to claim #18: checked against the 2016 WP abstract (0.974); the cited JFE version gives 0.976" | section audit |

### `dossiers/09_overlay.md` (29 changes; fix:09)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §2.3 'The model', l.133 | "Jeanne & Rancière (IMF WP/06/229)" → "+ published as Jeanne & Rancière 2011, EJ 121(555)" | tokens |
| 2 | usage | §2.3 benchmark sentence, l.147 | "gives 10.1% of GDP" → "WP gives 10.1%; published 2011 version reports 9.1% of output [unverified: via Mihailov & Nasir 2022]" | S09a |
| 3 | usage | §2.6 SE of the Sharpe ratio, l.228 (Lo 2002) | i.i.d. formula only → "+ headline: serial correlation; annual SR can be overstated by as much as 65%" | S09b |
| 4 | usage | §2.6 risk budgeting, l.245 (Moreira & Muir) | "[S: Harvey et al. 2018; Moreira & Muir 2017]" → "M&M report higher Sharpe ratios; gain disputed out of sample (Cederburg et al. 2020; Barroso & Detzel 2021)" | S09c |
| 5 | usage | §2.6 risk budgeting, l.247 (Kaminski & Lo) | "add value only when returns are serially correlated [nrv]" → "under a random walk stop-losses lower expected return; with momentum they can add value [S: 2010 SSRN abstract]" | S09d |
| 6 | usage | §2.6 crowding, l.243 (Daniel & Moskowitz) | "momentum crashes documented [nrv]" → "+ for cross-sectional momentum; bear on trend only by analogy" | – |
| 7 | metadata | §4.7 carry, l.545 | "[S: Koijen et al.]" → "[S: Koijen et al. 2018]" | grep |
| 8 | metadata | §10 ref 3 (Israelov & Nielsen 2015) | "JPM" → "JPM 41(4), 108–120, DOI 10.3905/jpm.2015.41.4.108" | tokens |
| 9 | metadata | §10 ref 5 (Hurst, Ooi & Pedersen 2017) | "JPM, Fall" → "44(1), 15–29 (Fall), DOI 10.3905/jpm.2017.44.1.015" | tokens |
| 10 | metadata | §10 ref 7 (Koijen et al., Carry) | no year or volume → "(2018) JFE 127(2), 197–225, DOI 10.1016/j.jfineco.2017.11.002" | S09e; tokens |
| 11 | metadata | §10 ref 10 (Bailey & López de Prado 2014) | short title → full subtitle; JPM 40(5), 94–107, DOI 10.3905/jpm.2014.40.5.094 | grep; tokens |
| 12 | metadata | §10 ref 11 (Bailey et al., PBO) | "J. Comput. Finance" → "(2017) 20(4), 39–69 (first published 19 Sep 2016), DOI 10.21314/JCF.2016.322" | S09f; publisher page; tokens |
| 13 | metadata | §10 ref 12 (Harvey & Liu 2015) | "JPM, Fall 2015" → "42(1), 13–28, DOI 10.3905/jpm.2015.42.1.013" | tokens |
| 14 | metadata | §10 ref 20 (Jeanne & Rancière) | WP only → "+ published version (2011) EJ 121(555), 905–930" | tokens |
| 15 | metadata | §10 [nrv] list header | no status note → italic note: 11 [nrv] works since confirmed | – |
| 16 | metadata | §10 [nrv] Browne (1999) | "AAP 31(2)" → "31(2), 551–577, DOI 10.1239/aap/1029955147" | tokens |
| 17 | recheck | §10 [nrv] Carr & Wu (2009) | "RFS 22(3)" → "22(3), 1311–1341, DOI 10.1093/rfs/hhn038" | tokens |
| 18 | metadata | §10 [nrv] Coval & Shumway (2001) | "JF 56(3)" → "56(3), 983–1009, DOI 10.1111/0022-1082.00352" | tokens |
| 19 | metadata | §10 [nrv] Daniel & Moskowitz (2016) | "JFE 122(2)" → "122(2), 221–247, DOI 10.1016/j.jfineco.2015.12.002" | tokens |
| 20 | metadata | §10 [nrv] Getmansky, Lo & Makarov (2004) | no title → full title; JFE 74(3), 529–609, DOI | tokens |
| 21 | metadata | §10 [nrv] Grossman & Zhou (1993) | no title → "Optimal Investment Strategies for Controlling Drawdowns, MF 3(3), 241–276, DOI" | tokens |
| 22 | metadata | §10 [nrv] Hardy (2001) | no title → "A Regime-Switching Model of Long-Term Stock Returns, NAAJ 5(2), 41–53, DOI" | tokens |
| 23 | metadata | §10 [nrv] Kaminski & Lo (2014) | no title → "When Do Stop-Loss Rules Stop Losses?, JFM 18, 234–254, DOI 10.1016/j.finmar.2013.07.001" | grep; tokens |
| 24 | metadata | §10 [nrv] Lo (2002) | "FAJ 58(4)" → "58(4), 36–52, DOI 10.2469/faj.v58.n4.2453" | tokens |
| 25 | metadata | §10 [nrv] Mohajerin Esfahani & Kuhn (2018) | "MP 171" → full title with subtitle; MP 171(1–2) | tokens |
| 26 | metadata | §10 [nrv] Rampini & Viswanathan (2010) | no title → "Collateral, Risk Management, and the Distribution of Debt Capacity, JF 65(6), 2293–2322, DOI" | tokens |
| 27 | metadata | §10 [nrv] Rampini, Sufi & Viswanathan (2014) | no title → "Dynamic Risk Management, JFE 111(2), 271–296, DOI 10.1016/j.jfineco.2013.10.003" | tokens |
| 28 | missing_reference | §10 new block (works newly cited in §2.3, §2.6) | (none) → "Barroso & Detzel (2021) JFE 140(3), 744–767; Cederburg, O'Doherty, Wang & Yan (2020) JFE 138(1); others" | S09g; tokens |
| 29 | consistency_edit | end of file | (none) → corrections section (+ 'checked, no change' line) | section audit |

### `verification/09_overlay.verify.md` (3 changes; fix:09)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | consistency_edit | §2 claims table, row F17 note | "… approximate equation 17 gives 9.97%" → "+ [published EJ 121(555), 905–930 (2011) reports 9.1% of output; unverified]" | C09b; tokens |
| 2 | consistency_edit | §4 citation problems, item 4 | "Minor: … lack volume and issue details" → "+ [Resolved 2026-10-18: refs 3 and 7 completed via Crossref]" | C09c; tokens |
| 3 | consistency_edit | end of file | (none) → corrections section (F17 note, item-4 resolution, no-erratum line) | section audit |

### `dossiers/10_scenarios_robustness.md` (55 changes; fix:10)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | recheck | §1 #8 path counts, l.41 | "about 1,000 scenarios for d=30, ε=5%, β=10⁻³" → "about 1,000 (exact minimum 986); holds only for convex scenario programs" | recomputed |
| 2 | recheck | §2.3 stationary bootstrap, l.79 | "(Politis & White 2004)" → "(Politis & White 2004, as corrected by Patton, Politis & White 2009)" | – |
| 3 | usage | §2.3 generative simulators, l.81 | "for small data (Buehler et al. 2020); data-hungry and opaque" → "built for scarce data (Bühler et al. 2026; preprint 2020); opaque …" | – |
| 4 | metadata | §2.4 Gao & Kleywegt in-text, l.90 | "Gao & Kleywegt prove" → "Gao & Kleywegt (2023) prove" | – |
| 5 | metadata | §2.4 Xie in-text, l.93 | "(Xie)" → "(Xie 2021)" | – |
| 6 | usage | §2.4 Glasserman & Xu quote, l.104 | "'with little effort'" → "'very little computational effort beyond that required to evaluate performance under the baseline nominal model'" | S10c |
| 7 | metadata | §2.5 Rebonato & Denev, l.110 | "(CUP 2014; unverified in session)" → "(CUP 2014) [S]" | – |
| 8 | metadata | §2.5 Meucci (2008), l.111 | "SSRN 403, unverified" → "verified via arXiv:1012.2848 [S]" | S10k |
| 9 | usage | §3 scenario reduction, l.127 (Heitsch & Römisch) | "(Heitsch & Römisch 2003)" → "reduction of scenario sets (2003); suits two-stage problems; multistage trees need the 2009 method" | – |
| 10 | metadata | §3 Pflug, l.129 | "(Pflug 2001; unverified in session)" → "(Pflug 2001) [S]" | – |
| 11 | recheck | §4.4 Campi–Garatti exact bound, l.237 | "N ≥ 448 / 989 / 2,662; 4,976" → "N ≥ 447 / 986 / 2,658; 4,970 (exact minima)" | S10a; S10b; recomputed |
| 12 | recheck | §5 agentic orchestration, l.260 (Lange et al.) | "ablations attribute reliable autonomy to the orchestration layer" → "depends on the orchestration layer as well as on base-model capability" | – |
| 13 | recheck | §6.2 starting point, l.288 (Kritzman orphans) | "(from the deck's State/Fragility engine)" → "+ HMM/HSMM with turbulence and absorption-ratio indicators; sources Kritzman & Li (2010), Kritzman et al. (2011)" | – |
| 14 | recheck | §6.5 variance risk premium, l.324 (Carr & Wu) | "implied exceeds expected realised variance in calm regimes" → "on average the premium is negative (realised minus swap rate); calm-regime claim [I]; sign [unverified]" | – |
| 15 | usage | §6.7 table, optimisation row, l.343 | "Heitsch–Römisch" → "Heitsch–Römisch (2009) multistage tree reduction" | S10d |
| 16 | recheck | §6.7 table, scenario-approach row, l.345 | "≥1,000" → "≥986, about 1,000; convex scenario programs only" | – |
| 17 | recheck | §6.7 table, future-node row, l.346 | "regression proxy, not nested" → "regression-based nested simulation (few inner draws per outer scenario)" | – |
| 18 | missing_reference | §6.10 ENS, l.435 | "ENS = exp(−Σq ln q)" → "+ the effective number of scenarios of Meucci (2012) [S]" | S10e |
| 19 | recheck | §7 volatility and bootstrap, l.482 | "arch … optimal block length" → "+ block-length code should follow the Patton, Politis & White 2009 correction" | – |
| 20 | recheck | §10 Buehler/Bühler et al. | "Buehler et al. (2020), arXiv:2006.14498" → "Bühler et al. (2026), chapter in Stochastic Analysis and Applications …; preprint kept" | – |
| 21 | metadata | §10 Gao & Kleywegt | "arXiv:1604.02199 (accepted, MOR)" → "(2023) MOR 48(2):603–655, DOI 10.1287/moor.2022.1275" | S10f; tokens |
| 22 | missing_reference | §10 new Heitsch & Römisch (2009) | (none) → "Scenario tree reduction for multistage stochastic programs, CMS 6(2):117–133, with DOI" | grep; tokens |
| 23 | recheck | §10 Kuhn, Shafiee & Wiesemann | "Acta Numerica 34; arXiv" → "34:579–804, DOI 10.1017/S0962492924000084" | tokens |
| 24 | metadata | §10 Meucci (2008) | "Risk 21(10); SSRN (unverified)" → "21(10):97–102; arXiv:1012.2848" | tokens |
| 25 | missing_reference | §10 new Meucci (2012) | (none) → "Effective number of scenarios in fully flexible probabilities (Consensus record) [venue unverified]" | – |
| 26 | metadata | §10 Mohajerin Esfahani & Kuhn | "MP (journal details not re-verified)" → full subtitle; MP 171(1–2):115–166, DOI 10.1007/s10107-017-1172-1 | S10i; tokens |
| 27 | missing_reference | §10 new Patton, Politis & White (2009) | (none) → "Correction to 'Automatic block-length selection…', ER 28(4):372–375, DOI 10.1080/07474930802459016" | S10j; tokens |
| 28 | metadata | §10 Pflug (2001) | "MP 89 (unverified)" → "89(2):251–271, DOI 10.1007/pl00011398" | tokens |
| 29 | metadata | §10 Rebonato & Denev | "CUP (unverified)" → "+ DOI 10.1017/CBO9781107256736" | tokens |
| 30 | metadata | §10 Shu, Yu & Mulvey | arXiv:2402.05272 → "J. Asset Management 25(5):493–507, DOI 10.1057/s41260-024-00376-x; preprint kept" | S10h; tokens |
| 31 | recheck | §10 Smith & Winkler | short title → full subtitle, DOI 10.1287/mnsc.1050.0451 | tokens |
| 32 | metadata | §10 Xie | arXiv:1806.07418 → "(2021) MP 186(1–2):115–155, DOI 10.1007/s10107-019-01445-5" | S10g; tokens |
| 33 | recheck | §10 Politis & White (2004) | "ER 23(1):53–70" → "+ DOI 10.1081/ETC-120028836; see the 2009 correction" | tokens |
| 34 | recheck | §10 Carr & Wu | "RePEc link only" → "DOI 10.1093/rfs/hhn038" | tokens |
| 35 | recheck | §10 Broadie, Du & Moallemi | "RePEc link only" → "DOI 10.1287/opre.2015.1419" | tokens |
| 36 | recheck | §10 Aas et al. | "RePEc link only" → "DOI 10.1016/j.insmatheco.2007.02.001" | tokens |
| 37 | recheck | §10 Ang & Bekaert | "RePEc link only" → "DOI 10.1093/rfs/15.4.1137" | tokens |
| 38 | recheck | §10 Barillas, Hansen & Sargent | "RePEc link only" → "DOI 10.1016/j.jet.2008.11.014" | tokens |
| 39 | recheck | §10 Barone-Adesi, Giannopoulos & Vosper | "RePEc link only" → "DOI 10.1002/(SICI)1096-9934(199908)19:5<583::AID-FUT5>3.0.CO;2-S" | tokens |
| 40 | recheck | §10 Ben-Tal et al. | "RePEc link only" → "DOI 10.1287/mnsc.1120.1641" | tokens |
| 41 | recheck | §10 Campbell, Chan & Viceira | "RePEc link only" → "DOI 10.1016/S0304-405X(02)00231-3" | tokens |
| 42 | recheck | §10 Chen & Sim | "RePEc link only" → "DOI 10.1287/opre.1080.0570" | tokens |
| 43 | recheck | §10 Cont & da Fonseca | "RePEc link only" → "DOI 10.1088/1469-7688/2/1/304" | tokens |
| 44 | recheck | §10 Delage & Ye | "RePEc link only" → "DOI 10.1287/opre.1090.0741" | tokens |
| 45 | recheck | §10 Gatheral & Jacquier | "RePEc link only" → "DOI 10.1080/14697688.2013.819986" | tokens |
| 46 | recheck | §10 Getmansky, Lo & Makarov | "RePEc link only" → "DOI 10.1016/j.jfineco.2004.04.001" | tokens |
| 47 | recheck | §10 Gordy & Juneja | "RePEc link only" → "DOI 10.1287/mnsc.1100.1213" | tokens |
| 48 | recheck | §10 Hamilton | "RePEc link only" → "DOI 10.2307/1912559" | tokens |
| 49 | recheck | §10 Maenhout | "RePEc link only" → "DOI 10.1093/rfs/hhh003" | tokens |
| 50 | recheck | §10 Nystrup, Madsen & Lindström (2018) | "RePEc link only" → "DOI 10.1080/14697688.2017.1342857" | tokens |
| 51 | recheck | §10 Pástor & Stambaugh | "RePEc link only" → "DOI 10.1111/j.1540-6261.2012.01722.x" | tokens |
| 52 | recheck | §10 Pflug, Pichler & Wozabal (2012) | "RePEc link only" → "DOI 10.1016/j.jbankfin.2011.07.018" | tokens |
| 53 | recheck | §10 White (2000) | "RePEc link only" → "DOI 10.1111/1468-0262.00152" | tokens |
| 54 | recheck | §10 Wiese et al. | "RePEc link only" → "DOI 10.1080/14697688.2020.1730426" | tokens |
| 55 | consistency_edit | end of file | (none) → corrections section (sources line + one line per change) | section audit |

### `verification/10_scenarios_robustness.verify.md` (2 changes; fix:10)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | consistency_edit | §4 after the 'no hallucinated citations' conclusion | (no erratum) → "Erratum: Gao & Kleywegt metadata and claim #16 (G&X quote) wrongly accepted" | C10b |
| 2 | consistency_edit | end of file | (none) → corrections section (erratum + cross-reference line) | section audit |

### `dossiers/11_objectives.md` (16 changes; fix:11)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | missing_reference | §2.1, l.84 (Föllmer & Leukert follow-up) | "Their follow-up calls it …" → "Their follow-up, efficient hedging (Föllmer & Leukert 2000, F&S 4(2)), calls it …" | tokens |
| 2 | recheck | §2.3, l.121 (scenario-approach attribution) | "(Calafiore & Campi 2006; Campi & Garatti 2008)" → "(Calafiore & Campi 2006), with the exact bound of Campi & Garatti (2008, Thm 2.4)" | grep |
| 3 | recheck | §2.3 N table, l.123–128 | no β column → "β = 10⁻⁶ in every row; N unchanged (exact minima)" | S11b; recomputed |
| 4 | recheck | §2.6, l.174 (de Finetti / Avanzi) | "is ADIC's payout problem: pay the owner while controlling ruin" → "maximizes expected discounted dividends until ruin; does not control ruin on its own" | – |
| 5 | recheck | §2.6, l.175 (barrier/band) | "Barrier/band strategies (pay the minimum …) and ratcheting variants" → "barrier and band strategies surveyed by Avanzi (2009); protected-minimum variant [I]" | – |
| 6 | recheck | §6.5 table, 'Real drawdown' row, l.416 | "the fund enters Browne's danger zone [I]" → "payout no longer sustainable in expectation [I]; Browne's (1997) boundary is c/r" | S11d |
| 7 | metadata | §6.5 table, 'Ambiguity set' row, l.422 | "(Esfahani & Kuhn 2018)" → "(Mohajerin Esfahani & Kuhn 2018)" | S11c |
| 8 | metadata | §10 Das et al. | "SSRN 3211951 (2018)" → "(2020) Computational Management Science …" | – |
| 9 | recheck | §10 Föllmer & Leukert (1999) | RePEc link → "+ DOI 10.1007/s007800050062" | tokens |
| 10 | missing_reference | §10 new Föllmer & Leukert (2000) | (none) → "Efficient hedging: cost versus shortfall risk, F&S 4(2):117–146, DOI 10.1007/s007800050008" | S11a; tokens |
| 11 | metadata | §10 Rockafellar & Uryasev (2000) | "J. Risk 2(3) (from memory)" → "2(3):21–41, DOI 10.21314/jor.2000.038" | tokens |
| 12 | metadata | §10 Busseti, Ryu & Boyd (2016) | arXiv → "J. Investing 25(3):118–134, DOI 10.3905/joi.2016.25.3.118" | tokens |
| 13 | metadata | §10 Mohajerin Esfahani & Kuhn (2018) | "Esfahani, P.M., Kuhn, D. … Data-driven DRO" → "Mohajerin Esfahani, P., Kuhn, D., full title" | – |
| 14 | metadata | §10 Boyd et al. (2017) | arXiv → "FnT Optimization 3(1):1–76, DOI 10.1561/2400000023" | tokens |
| 15 | metadata | §10 Ang, Papanikolaou & Westerfield (2014) | "MS; NBER w19436" → "MS 60(11):2737–2761, DOI 10.1287/mnsc.2014.1986" | tokens |
| 16 | consistency_edit | end of file | (none) → corrections section (14 entries) | section audit |

### `verification/11_objectives.verify.md` (2 changes; fix:11)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | recheck | end of file, erratum | (none) → "Erratum: row 8 covered §2.2 only; dossier §6.5 put Browne's danger-zone boundary at the sustainable payout" | read |
| 2 | consistency_edit | end of file, status line | (none) → "Status: open citation items applied to the dossier on 2026-10-18" | C11b; tokens |

### `dossiers/12_agentic_ai.md` (29 changes; fix:12)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §10 ref 4 | "Sakana AI (2026-03-26). The AI Scientist in Nature" → "Lu, Lu, Lange, Yamada, Hu, Foerster, Ha, Clune (2026), Towards end-to-end automation of AI research, Nature 651(8107):914–919" | S12a; tokens |
| 2 | metadata | §10 ref 31 | "Gao, Jiang, Yan (2025). A Test of Lookahead Bias …" → "(2025; v2 2026) Detecting Lookahead Bias in LLM Forecasts (v1 title noted)" | S12b |
| 3 | usage | §1 item 3 (FINSABER) | "'often vanish'" → "'deteriorate significantly' (abstract); introduction says 'often vanish'" | S12c |
| 4 | metadata | §4 table, FINSABER date cell | "2025 (KDD)" → "2025 (arXiv); KDD 2026" | – |
| 5 | metadata | §10 ref 29 (FINSABER) | "Li et al. (2025) … arXiv:2505.07078" → "Li, Kim, Cucuringu, Ma (2025; KDD 2026), Proc. …" | – |
| 6 | usage | §6.3 objective | "s.t. Pr(false promotion) ≤ α" → "s.t. FWER within contract ≤ α (Holm), mFDR across contracts ≤ α (α-investing)" | – |
| 7 | usage | §2.6 table, discovery-across-time row | "α-investing … natural ledger" → "+ controls mFDR, 'a weaker criterion than the FDR'" | S12d |
| 8 | usage | §6.4 item 3 | "Holm-adjusted at α=0.05" → "+ which controls FWER within the contract" | – |
| 9 | usage | §6.4 item 6 | ledger rule → "+ error criterion: mFDR across contracts" | – |
| 10 | usage | §6.4 item 5, new sub-bullet | expected-maximum term only → "Non-normality term: DSR with skewness and kurtosis" | S12e |
| 11 | usage | §2.2 optimizer's-curse bullet | "(Smith and Winkler†)" → "+ their remedy: Bayesian shrinkage toward a prior mean" | – |
| 12 | usage | §6.4 item 5, new sub-bullet | no shrinkage → "Shrink reported estimates: posterior mean F̃ = μ0 + κ(F̂ − μ0)" | S12f |
| 13 | usage | §1 item 1, Kosmos bullet | "79.4% judged accurate" → "+ even though Kosmos cites every statement to code or primary literature" | S12g |
| 14 | usage | §4 table, Kosmos row | "79.4% accurate" → "+ although every statement is cited" | grep |
| 15 | usage | §4 table, AI Scientist v2 / Nature row | "reviewer balanced accuracy 69%" → "+ the workshop 'had an acceptance rate of 70%' (Nature abstract)" | – |
| 16 | recheck | §1 item 1, Agentic Scientist conclusion | "credits orchestration for reliable autonomy" → "ablations indicate reliable autonomy depends on orchestration as well as base-model capability" | – |
| 17 | recheck | §9 open question 9 | "(orchestration matters more than the base model)" → "(depends on the orchestration layer as well as the base model)" | – |
| 18 | recheck | §10 ref 80 (Smith & Winkler) | short title → full subtitle; 52(3):311–322, DOI 10.1287/mnsc.1050.0451 | tokens |
| 19 | recheck | §10 ref 77 (White 2000) | "68(5)" → "68(5):1097–1126, DOI 10.1111/1468-0262.00152" | tokens |
| 20 | metadata | §10 ref 74 (PBO) | "J. Comput. Finance 20(4). SSRN" → "+ DOI 10.21314/jcf.2016.322 (OpenAlex); pages not added" | tokens |
| 21 | metadata | §10 ref 75 (DSR) | short title → full subtitle; JPM 40(5):94–107 | tokens |
| 22 | metadata | §10 ref 79 (Foster & Stine) | short title → full subtitle; JRSS-B 70(2):429–444, DOI 10.1111/j.1467-9868.2007.00643.x | tokens |
| 23 | metadata | §10 ref 5 (Beel et al.) | short title, arXiv → full title; ACM SIGIR Forum 59(1):1–20, DOI 10.1145/3769733.3769747 | tokens |
| 24 | metadata | §10 ref 6 (Co-Scientist) | arXiv → "Nature 655(8122):487–496 (online 19 May 2026), DOI 10.1038/s41586-026-10644-y" | tokens |
| 25 | metadata | §10 ref 16 (Robin) | arXiv → "+ published version noted" | – |
| 26 | metadata | §10 ref 25 (FinMem) | arXiv → "+ published version noted" | – |
| 27 | metadata | §10 ref 30 (Lopez-Lira, Tang, Zhu) | short title → "full title (…: Can We Trust LLMs' Economic Forecasts?); arXiv:2504.14765" | – |
| 28 | consistency_edit | §10 header of classical † list | "(from bibliographic knowledge, not re-fetched)" → "+ metadata and DOIs of 74, 75, 77, 79 and 80 confirmed 2026-10-18" | C12a; tokens |
| 29 | consistency_edit | end of file | (none) → corrections section (16 entries) | section audit |

### `verification/12_agentic_ai.verify.md` (2 changes; fix:12)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | recheck | §3 citation check, after † list | "No hallucinated or garbled citations" → "+ Erratum: Smith & Winkler accepted though ref 80 omitted the subtitle" | – |
| 2 | consistency_edit | end of file | (none) → corrections section (one entry) | section audit |

### `dossiers/13_paper_deepread.md` (26 changes; fix:13)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §2.2 theory (Dwork) | "Dwork et al. (2015) give provable remedies" → "(2015; with the companion Science paper, The reusable holdout)" | – |
| 2 | recheck | §2.2 theory (Smith & Winkler) | "[not re-verified]" → "verified; DOI 10.1287/mnsc.1050.0451" | tokens |
| 3 | usage | §2.8 specification gaming | blog as only source → "blog tagged; 'Academic anchors [S]': Skalse et al. (2022), Pan et al. (2022)" | S13b |
| 4 | metadata | §4.2 Nature publication bullet | "(26 Mar 2026, per Sakana's blog)" → "Lu et al. (2026), Nature 651:914–919; 69% and 6.33 attributed to the blog; 70% acceptance from the abstract" | grep; tokens |
| 5 | usage | §4.2 '59%' bullet | "An unverified figure … 59%" → "MLReplicate (Gaddipati et al. 2026): 10 of 37 accepted; experts flagged fabricated or unsupported claims in 59% of evaluations" | S13a |
| 6 | consistency_edit | §4.3 table, 'Framework generation' row | "v2 workshop acceptance" → "+ (the workshop accepted 70% of submissions, per the Nature abstract)" | C13a |
| 7 | usage | §5.5 Fed/OCC bullet | "Fed SR 11-7 / OCC 2011-12 (2011); URLs 404" → "Fed SR 26-2 / OCC Bulletin 2026-13 (17 Apr 2026) supersede SR 11-7 / OCC 2011-12" | S13c; tokens |
| 8 | recheck | §5.6 MAP bullet | "MAP (2019) [P] … steps not verified" → "MAP (Kahneman, Lovallo & Sibony 2019) [S, via secondary summary]: criteria in advance, independent assessments …" | – |
| 9 | metadata | §5.6 tournament ranking | "(Gottweis et al.)" → "(Gottweis et al., 2026)" | – |
| 10 | recheck | §6.4(2) gates, new paragraph | orphan Alshiekh entry → "gates work like a shield in safe RL (Alshiekh et al., 2018)" | – |
| 11 | missing_reference | §6.5 stage-3 rubric opp_alpha_evidence | "deflated for the number of trials [P]" → "+ with the probability of backtest overfitting estimated for the selection" | – |
| 12 | metadata | §10 Nature article entry | "Sakana AI (26 Mar 2026) blog" → "Lu et al. (2026), Nature 651(8107):914–919, DOI 10.1038/s41586-026-10265-5" | S13d; tokens |
| 13 | metadata | §10 Beel et al. | arXiv → "ACM SIGIR Forum 59(1):1–20 (June 2025), DOI 10.1145/3769733.3769747" | tokens |
| 14 | missing_reference | §10 new MLReplicate entry | (none) → "Gaddipati, Muhammed, Keya, Rabby & Auer (2026), MLReplicate, arXiv:2605.16616" | grep |
| 15 | metadata | §10 Kwa et al. | arXiv → "+ NeurIPS 38 (2025), pp. 102382–102435, DOI 10.52202/085713-3086" | tokens |
| 16 | metadata | §10 Gottweis et al. | arXiv title (v2) → "(2026) Nature 655(8122):487–496, with DOI" | tokens |
| 17 | missing_reference | §10 new Dwork et al. Science entry | (arXiv only) → "The reusable holdout: Preserving validity in adaptive data analysis, Science (2015), DOI 10.1126/science.aaa9375" | tokens |
| 18 | missing_reference | §10 new Skalse et al. and Pan et al. | (none) → "Skalse, Howe, Krasheninnikov & Krueger (2022), NeurIPS 35, pp. 9460–9471; Pan, Bhatia & Steinhardt (2022)" | tokens |
| 19 | metadata | §10 Hyperband | "Hyperband. JMLR 18" → "Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization, JMLR 18:1–52" | – |
| 20 | recheck | §10 Alshiekh et al. | "(2017) arXiv:1708.08611" → "(2018) full authors; Proc. AAAI" | – |
| 21 | recheck | §10 Kahneman, Lovallo & Sibony (2011) | short title → "The Big Idea: Before You Make That Big Decision…, HBR 89(6):50–60, 137 (June 2011)" | tokens |
| 22 | recheck | §10 KLS (2019) + new SBI entry | "MIT SMR" → "MIT SMR Spring 2019 (4 Mar 2019; Reprint 60314); new Sydney Business Insights summary entry" | – |
| 23 | usage | §10 Fed/OCC model-risk guidance | "SR 11-7 / OCC 2011-12 (2011) [not re-verified]" → "three entries: SR 26-2 (17 Apr 2026); OCC Bulletin 2026-13; SR 11-7 noted as superseded" | tokens |
| 24 | recheck | §10 Smith & Winkler | "52(3) [not re-verified]" → "52(3):311–322, DOI 10.1287/mnsc.1050.0451" | tokens |
| 25 | metadata | §10 Bailey et al. (PBO) | "J. Comput. Finance (2017) [not re-verified]" → "(2017) 20(4) (online Sep 2016), DOI 10.21314/JCF.2016.322; pages not added" | tokens |
| 26 | consistency_edit | end of file | (none) → corrections section (23 entries) | section audit |

### `verification/13_paper_deepread.verify.md` (3 changes; fix:13)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §3 citation check, Nature row | "title and authors remain unverified" → "+ [Resolved: Towards end-to-end automation of AI research, Nature 651(8107):914–919]" | tokens |
| 2 | usage | §3 citation check, MLReplicate row | "reports this as unverified" → "+ [Checked against arXiv:2605.16616 v1: 10 of 37; 59% of expert evaluations]" | – |
| 3 | consistency_edit | end of file | (none) → corrections section (two entries; no verdict reversed) | section audit |

### `dossiers/14_ic_deliberation.md` (51 changes; fix:14)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §1 item 2, Tessler et al. | "56% vs 44% (programme N = 5,734)" → "(one experiment: 75 six-person groups, n = 439; N = 5,734 is the whole programme)" | S14g |
| 2 | recheck | §1 item 2, Michael et al. | "debate vs a single advocate ('consultancy')" → "consultancy, in which one expert argues for an answer that is correct half the time" | – |
| 3 | recheck | §1 item 3(ii), Fogliato et al. | "reduces uncritical agreement with AI" → "reduces anchoring on AI output, with no accuracy gain shown" | – |
| 4 | usage | §1 item 3(iii), seeded-error drills | "drills for automation bias" → "drills to monitor automation bias, which training does not prevent" | grep |
| 5 | usage | §2.2 hidden profiles, Stasser & Titus | "(nr) … information-sampling model" → "(verified) … [unverified: attribution of the formula]" | – |
| 6 | recheck | §2.2 transparency, Hansen et al. | "discipline dominating [S]" → "+ on their influence measure" | – |
| 7 | recheck | §2.2 noise, MAP | "(MIT SMR paywalled; nr)" → "core steps confirmed via a summary (Sydney Business Insights, May 2019)" | – |
| 8 | recheck | §2.3 table, independent-estimates row | "human-first ordering, Fogliato et al. [S]" → "+ reduces anchoring on AI output, no accuracy gain shown" | – |
| 9 | recheck | §2.3 table, MAP row | "Kahneman et al. 2019, 2021 (nr)" → "2019 (core steps via secondary summary), 2021 (nr)" | – |
| 10 | usage | §2.3 table, DA vs DI row, evidence | "both beat an expert-recommendation baseline (nr)" → audit wording: DA beat the baseline; DI not shown on ill-structured tasks; neither beat the other [S] | S14a |
| 11 | consistency_edit | §2.3 table, DA vs DI row, IDM use | "DI on cruxes" → "DI only on cruxes with explicit rival assumption sets [I]" | C14a |
| 12 | metadata | §2.4 extremizing tag | "(nr)" → "(Baron et al. verified; Satopää et al. nr)" | – |
| 13 | metadata | §2.4 judgment aggregation tag | "(nr)" → "(List & Pettit verified)" | – |
| 14 | recheck | §2.5 role and model diversity, ReConcile | "diversity … is critical (gains up to 11.4%)" → "beat baselines by up to 11.4%; component analysis found model diversity critical" | – |
| 15 | usage | §2.5 sceptical empirics, Smit et al. | "do not reliably outperform …" → "+ abstract: adjusting agreement levels can surpass the non-debate protocols" | – |
| 16 | recheck | §2.5 sceptical empirics, Wynn, Satija & Hadfield | "Weaker agents drag down stronger ones" → "can drag down …; the effect is not uniform" | – |
| 17 | recheck | §2.5 persuasion, Salvi et al. | "+81.7% odds (arXiv v1)" → "81.2% relative increase in odds (95% CI +26.0% to +160.7%; N = 900)" | – |
| 18 | recheck | §2.6 Vaccaro et al. table | (no row) → "AI alone outperforms humans (vs better of the two): −0.54 (95% CI −0.71 to −0.37)" | – |
| 19 | recheck | §2.6 other findings, Fogliato et al. | "Radiologists … at no time cost" → "Veterinary radiologists (n = 19) … no time cost and no accuracy gain" | S14c |
| 20 | usage | §2.6 automation bias, Parasuraman & Manzey | "model it as complacency … (nr)" → "(verified); affects naive and expert users; training does not prevent it" | – |
| 21 | recheck | §3 table, ordering row | "(Fogliato; Buçinca)" → "(Fogliato, for reduced anchoring, not better decisions; Buçinca)" | – |
| 22 | consistency_edit | §3 table, structured-conflict default | "Both: red-team seat (DA) and DI on the top cruxes (Schwenk)" → "DA seat, which Schwenk supports; DI only on cruxes with rival assumption sets [I]" | C14b |
| 23 | recheck | §3 table, record row | "(Meade & Stasavage; Hansen et al.)" → "[I] (Meade & Stasavage); Hansen et al. show a discipline–conformity trade-off" | – |
| 24 | usage | §4 row 1, Tessler et al. | "(N = 5,734 across experiments)" → "(one experiment: 75 groups, n = 439; N = 5,734 is the programme)" | S14g |
| 25 | recheck | §4 row 6, Khan et al. | "Model 76% vs 48%; human 88% vs 60%" → "+ against naive baselines; consultancy 54% / 78%" | – |
| 26 | recheck | §4 row 8 source, Hackenburg et al. | "Jul 2025" → "Science 390(6777):eaea3884, 4 Dec 2025 (preprint Jul 2025)" | S14d; tokens |
| 27 | recheck | §4 row 9, Salvi et al. | "+81.7% odds (N = 820), arXiv v1" → "+81.2% relative odds (CI …; N = 900); journal version" | – |
| 28 | recheck | §4 row 12, Hansen et al. | "Discipline effect dominates" → "+ (on the authors' influence measure)" | – |
| 29 | metadata | §4 row 13 source, Blinder & Morgan | "NBER WP 7909 (2000)" → "+ peer-reviewed version JMCB 37(5), 2005" | tokens |
| 30 | consistency_edit | §6.4 S3 evidence-gated debate | "DI on at most 3 cruxes" → "+ use DI only where a crux has explicit rival assumption sets, DA otherwise" | C14c |
| 31 | usage | §6.10 item 6, seeded-error drills | "Seeded-error drills." → "which monitor and measure automation bias rather than prevent it (P&M 2010)" | S14b |
| 32 | metadata | §10 Baron et al. (2014) | "(nr)" → "DOI 10.1287/deca.2014.0293" | tokens |
| 33 | metadata | §10 Blinder & Morgan | NBER only → "+ Blinder & Morgan (2005), JMCB 37(5)" | tokens |
| 34 | inconsistency | §10 Bühlmann (1967) | no DOI → "DOI 10.1017/S0515036100008989; …8023 is a 1969 paper" | Crossref; tokens |
| 35 | recheck | §10 Chen, Saha & Bansal (ReConcile) | "ACL 2024" → "Proc. 62nd ACL (Vol. 1), pp. 7066–7085, DOI 10.18653/v1/2024.acl-long.381" | tokens |
| 36 | recheck | §10 Fogliato et al. (2022) | arXiv v1 author order → "FAccT '22 author order; pp. 1362–1374; DOI 10.1145/3531146.3533193" | tokens |
| 37 | recheck | §10 Hackenburg et al. (2025) | arXiv → "The levers of political persuasion with conversational artificial intelligence, Science 390(6777):eaea3884, DOI 10.1126/science.aea3884" | tokens |
| 38 | recheck | §10 Kahneman, Lovallo & Sibony (2019) | "MIT SMR" → "Spring 2019 issue; Reprint 60314; no volume or pages" | – |
| 39 | metadata | §10 Lange et al. (2026) | surnames only → initials added (Lange, R.T., Grillotti, L., Yamada, Y., Charakorn, R., Ha, D.) | – |
| 40 | metadata | §10 Lu, Yuan & McLeod (2012) | "(nr)" → "(metadata verified; magnitudes nr)" | – |
| 41 | metadata | §10 Meucci (2008) | SSRN → "+ arXiv copy 1012.2848" | – |
| 42 | metadata | §10 Parasuraman & Manzey (2010) | "(nr)" → "DOI 10.1177/0018720810376055" | tokens |
| 43 | recheck | §10 Salvi et al. | old preprint title (2024; NHB 2025) → "(2025) On the conversational persuasiveness of GPT-4, NHB 9(8):1645–1653, DOI 10.1038/s41562-025-02194-6" | S14e; tokens |
| 44 | metadata | §10 Schemmer et al. (2023) | "IUI 2023" → "IUI '23, pp. 410–422, DOI 10.1145/3581641.3584066" | tokens |
| 45 | metadata | §10 Schwenk (1990) | "(nr)" → "DOI 10.1016/0749-5978(90)90051-a" | tokens |
| 46 | metadata | §10 Smit et al. | author order, arXiv → "Smit, Grinsztajn, Duckworth, Barrett, Pretorius (2024), ICML 2024, PMLR 235:45883–45905" | tokens |
| 47 | metadata | §10 Stasser & Titus (1985) | no DOI → "DOI 10.1037/0022-3514.48.6.1467" | tokens |
| 48 | recheck | §10 Vaccaro, Almaatouq & Malone (2024) | "8:2293–2303" → "8(12):2293–2303, DOI 10.1038/s41562-024-02024-1" | tokens |
| 49 | metadata | §10 Wang, Morgenstern & Dickerson | "NMI; arXiv" → "NMI 7(3):400–411 (online 17 Feb 2025), DOI 10.1038/s42256-025-00986-z; preprint" | S14f; Crossref; tokens |
| 50 | recheck | §10 Wynn, Satija & Hadfield (2025) | arXiv → "ICML 2025 MAS Workshop" | – |
| 51 | consistency_edit | end of file | (none) → corrections section (25 entries + 1 'not changed' line) | section audit |

### `verification/14_ic_deliberation.verify.md` (1 changes; fix:14)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | recheck | end of file, erratum | (none) → "Erratum (re-check rows 22–23): Fogliato author order and FAccT metadata; ReConcile result wording" | section audit; tokens |

### `groups/dossiers/G1_pe_primaries.md` (23 changes; fix:G1)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §2.2 hold-up, l.93 (Hochberg et al. tag) | "[S, as summarised by K&S; original not fetched]" → "[S: RFS abstract, checked 2026-10-18]" | grep; tokens |
| 2 | metadata | §2.2 side vehicles, l.94 (author order) | "Lerner, Schoar, Mao & Zhang" → "Lerner, Mao, Schoar & Zhang (JFE 2022; WP order noted)" | – |
| 3 | metadata | §2.2, l.97 (source tag) | "[S: NBER w24941]" → "+ figures not re-checked against the JFE 2022 version" | – |
| 4 | metadata | §2.4 subscription lines, l.141 (Schillinger et al. tag) | "[S, summary only]" → "[S: SSRN abstract via Crossref]" | grep |
| 5 | inconsistency | §2.4, l.141 (Albertus & Denes) | "Albertus & Denes dispute …" → "(2020 version) …; the 2026 JFQA version is subtitled 'Agency Costs and Cash Flow Management' [content unverified]" | SG1a |
| 6 | metadata | §8 evidence gaps, l.551 | "verified except Hochberg et al. (via K&S only) and Cavagnaro" → "verified except the Cavagnaro magnitude; Hochberg now abstract-checked" | – |
| 7 | inconsistency | §10 Albertus & Denes entry | 2020 NBER conference version → "+ source of every figure; earlier SSRN version; JFQA 2026 probable successor [unverified]" | grep |
| 8 | metadata | §10 Begenau & Siriwardane | "JF pp. 1199–1247 (volume, issue not re-verified)" → "JF 79(2), 1199–1247, DOI 10.1111/jofi.13319; WP noted" | SG1b; tokens |
| 9 | metadata | §10 Brown, Gredil & Kaplan (2019) | "JFE 132(2)" → "132(2), 267–297, DOI 10.1016/j.jfineco.2018.10.011" | tokens |
| 10 | metadata | §10 Brown, Harris, Hu, Jenkinson, Kaplan & Robinson | "(2020) NBER w26755" → "(2021) JFE 139(2), 561–577 (online 2020), DOI 10.1016/j.jfineco.2020.08.014; WP kept" | SG1d; tokens |
| 11 | metadata | §10 Barber & Yasuda (2017) | "JFE 124(1) (title and venue only)" → "124(1), 172–194, DOI 10.1016/j.jfineco.2017.01.001" | tokens |
| 12 | metadata | §10 Cavagnaro, Sensoy, Wang & Weisbach (2019) | JF 74(6), 3089–3134 → "+ DOI 10.1111/jofi.12783; WP title noted" | tokens |
| 13 | metadata | §10 Harris, Jenkinson & Kaplan (2014) | "JF" → "JF 69(5), 1851–1882, DOI 10.1111/jofi.12154" | tokens |
| 14 | metadata | §10 Harris, Jenkinson, Kaplan & Stucke | "JCF 81, 102361" → "+ (2023), DOI 10.1016/j.jcorpfin.2023.102361" | tokens |
| 15 | metadata | §10 Korteweg & Sorensen (2017) | no DOI → "DOI 10.1016/j.jfineco.2017.03.006" | tokens |
| 16 | metadata | §10 Lerner & Schoar (2002/2004) | "JFE 72(1)" → "72(1), 3–40, DOI 10.1016/s0304-405x(03)00203-4" | tokens |
| 17 | metadata | §10 Lerner, Schoar & Wongsunwai (2007) | no DOI → "DOI 10.1111/j.1540-6261.2007.01222.x; WP notes" | tokens |
| 18 | metadata | §10 Lerner–Mao–Schoar–Zhang | "(2018) NBER w24941" → "(2022) JFE 143(1), 359–380, DOI 10.1016/j.jfineco.2021.05.034; WP is source of figures" | SG1c; tokens |
| 19 | metadata | §10 Schillinger, Braun & Cornel (2019) | "SSRN 3434112 (summary only)" → "SSRN Electronic Journal, DOI 10.2139/ssrn.3434112" | tokens |
| 20 | metadata | §10 Sensoy, Wang & Weisbach (2014) | no DOI → "DOI 10.1016/j.jfineco.2014.02.006" | tokens |
| 21 | metadata | §10 Hochberg, Ljungqvist & Vissing-Jørgensen | "Informational Hold-Up … RFS 27(1) (via K&S)" → "Informational Holdup …, RFS 27(1), 102–152, DOI 10.1093/rfs/hht046" | grep; tokens |
| 22 | metadata | §10 'via Stream 04/05' line | pointers only → full entries (Takahashi & Alexander JPM 28(2) 90–100; Luxenberg ICAIF '22; SWY 27(7); Nadauld JFE 132(3)) | tokens |
| 23 | consistency_edit | end of file | (none) → corrections section, + barrier note ('[S: BGK]' there means Brown–Gredil–Kaplan) | section audit |

### `groups/verification/G1_pe_primaries.verify.md` (3 changes; fix:G1)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | inconsistency | §3 citation check, Albertus & Denes row | "Correct (title page)" → "+ [Update: a JFQA 2026 journal version by the same authors exists]" | – |
| 2 | metadata | §3 citation check, Schillinger row | "SSRN ID not directly confirmed" → "+ [Resolved: confirmed via Crossref]" | – |
| 3 | consistency_edit | end of file | (none) → corrections section (no erratum; one line per annotation) | section audit |

### `groups/dossiers/G2_secondaries_group.md` (23 changes; fix:G2)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §1 item 4, Nadauld bullet, l.71–72 | "(2006–2014 broker data) [S]: … 0.974" → "(figures from NBER WP 22404, 2016) … 0.974 (0.976 in the JFE abstract)" | grep |
| 2 | usage | §1 item 4, Boyer bullet, l.75 | "beta above 2 and insignificant alpha" → "[S: Boyer et al. 2023] beta ≈1.8, CAPM alpha ≈0; GPME large and positive" | SG2a |
| 3 | usage | §2.3 liquidity provision, l.165 (Albuquerque) | specifics stated as sourced → "abstract-level result [S]; 2009–2016, young-fund, VIX and funding-cost details tagged [C]" | grep; tokens |
| 4 | usage | §2.3 equilibrium, l.166 (Maurin et al.) | "Funds with more illiquidity-tolerant LPs earn higher returns …" → "In MRS's theoretical model, …" | – |
| 5 | missing_reference | §2.3 implication, l.170 (Bollen & Sensoy orphan) | "liquidity premium …" → "+ probably small outside stress: Bollen & Sensoy breakeven result" | SG2c |
| 6 | usage | §2.4 risk understated, l.188 (Boyer) | "betas above 2 vs below 0.5" → "beta ≈1.8, vol ≈34% vs 'quite low' betas and 14–20% for NAV indices [WP 28691]" | read |
| 7 | missing_reference | §2.6 fee bullet, l.213 ('Rode et al.') | "60bp vs 75bp (CFA Institute, citing Rode et al.)" → "the CFA report's own example (p.21); Rode, Poldauf & Fuentes Perez (2025) cited [unverified at source]" | – |
| 8 | consistency_edit | §3.1(c) CV fee line, l.271 | "Fees are 0.6–0.75%" → "+ (as in the CFA Institute example, §2.6 [C])" | CG2a |
| 9 | metadata | §4.5 Nadauld table heading, l.429 | "(700 fund-quarter transactions, 2006–2014) [S]" → "+ figures from NBER WP 22404, 2016" | – |
| 10 | metadata | §4.5 Nadauld table, PME row, l.435 | "1.023 / 0.974" → "1.023 / 0.974 (JFE abstract: 0.976)" | grep |
| 11 | usage | §4.5 other evidence, Boyer bullet, l.444 | "beta above 2 vs below 0.5; ~20% a year" → "WP 28691: beta 1.79 (1.94 log), 14% a year (22% ages 4–9), vol ≈34%; NAV betas 0.73–0.85; alpha ≈0" | read |
| 12 | usage | §4.5 CVs, HEC/Gottschalg bullet, l.453 | figures stated as evidence → "marked as non-peer-reviewed evidence based on interim marks" | – |
| 13 | missing_reference | §6.5 item 5, l.649 (Gourier orphan) | "Unfunded plus deferred ≤ 35%" → "+ priced commitment risk (Gourier, Phalippou & Westerfield)" | SG2d |
| 14 | usage | §6.8 calibration target 7, l.698 | "β above 2 [S]" → "β of about 1.8–1.9 [S: Boyer et al., WP 28691]" | SG2e |
| 15 | usage | §6.10 spec card, return equations, l.718 | "≈2 for buyout exit values" → "≈1.8–1.9 [S: Boyer et al.]" | – |
| 16 | metadata | §10 ref 11 (Nadauld et al.) | "JFE 132(3) …; NBER WP 22404" → "+ the WP is the source of all figures quoted" | – |
| 17 | metadata | §10 ref 12 (Boyer et al.) | "(2018) PE Indices Based on Secondary Market Transactions, NBER WP 25207" → "(2023) Discount-Rate Risk in Private Equity…, JF 78(2):835–885, DOI 10.1111/jofi.13202; WPs 28691, 25207" | tokens |
| 18 | metadata | §10 ref 13 (Albuquerque et al.) | dead forum link → "SSRN working paper, DOI 10.2139/ssrn.3182481" | tokens |
| 19 | metadata | §10 ref 15 (Bollen & Sensoy) | short title → full subtitle (Illiquidity, secondary markets, and the value of private equity), DOI 10.1111/fima.12375 | tokens |
| 20 | metadata | §10 refs 21–22 (Gottschalg) | RePEc/handle links → "+ SSRN DOI 10.2139/ssrn.4752652 (RP 1515); marked not peer-reviewed" | tokens |
| 21 | metadata | §10 ref 26 (Luxenberg et al.) | "Luxenberg, E., et al. (2022), arXiv" → "five authors; ICAIF '22 pp. 249–256, DOI 10.1145/3533271.3561769; preprint kept" | tokens |
| 22 | missing_reference | §10 new ref 39 (Rode et al.) | (none) → "Rode, Poldauf & Fuentes Perez (Aug 2025), Redefining Private Equity…, Schroders Capital (via CFA report)" | SG2b |
| 23 | consistency_edit | end of file | (none) → corrections section (12 entries) | section audit |

### `groups/verification/G2_secondaries_group.verify.md` (11 changes; fix:G2)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §2 claims table, row S10 (Boyer) | "… published as JF 78(2) (2023)" → "+ [re-check: WP 28691 gives β ≈1.8; JF abstract: alpha ≈0]" | – |
| 2 | missing_reference | §2 'also confirmed', CFA bullet (Rode) | "lead 60bp vs syndicate 75bp (Rode et al.)" → "+ [split is the report's own example, p.21; citation is Rode, Poldauf & Fuentes Perez]" | – |
| 3 | metadata | §3 citation table, ref 11 row | "Cite the figures to w22404, or re-check …" → "+ [applied]" | – |
| 4 | metadata | §3 citation table, ref 12 row | "Check whether the β > 2 / < 0.5 figures carry over" → "+ [they do not carry over to the 2021 version]" | – |
| 5 | metadata | §3 other references, Bollen & Sensoy | FM 51(2) 501–538 → "+ [full title]" | – |
| 6 | missing_reference | §3 other references, Gourier et al. | JF 79(5) 3407–3457 → "+ [orphan now cited in §6.5 item 5]" | – |
| 7 | metadata | §3 other references, Luxenberg et al. | arXiv 2207.07767 → "+ [ICAIF '22, pp. 249–256, DOI]" | tokens |
| 8 | metadata | §3 other references, Gottschalg | RP 1515 / RP 1584 → "+ [SSRN DOI for RP 1515]" | – |
| 9 | metadata | §3 minor citation problems, ref 13 | "Cite SSRN." → "+ [applied: DOI 10.2139/ssrn.3182481]" | tokens |
| 10 | consistency_edit | §4 R5 'why they conflict' | "β ≈ 2 … σ_SA ≈ 45–50%" → "+ [the 2021 version gives β ≈1.8 (1.9 log); inconsistency stands]" | CG2b |
| 11 | consistency_edit | end of file | (none) → corrections section (7 entries) | section audit |

### `groups/dossiers/G3_cap_solutions.md` (27 changes; fix:G3)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §1 item 5, l.32 | "(Fed, citing S&P)" → "(Fed FEDS Note, KBRA DLD data)" | SG3a |
| 2 | usage | §4.5 table, recovery row source, l.287 | "Fed FEDS Note citing S&P [S]" → "Fed FEDS Note, KBRA DLD data [S]" | SG3a |
| 3 | recheck | §1 item 6, opportunity channel, l.37 (Böni–Manigart) | "funds raised when spreads are wide earn more" → "ex-ante BB spreads: higher net multiples, beat bond benchmarks; IRR effect insignificant; TED effect" | – |
| 4 | recheck | §3.6 calibration, l.182 (Böni–Manigart) | "expected vintage IRR rises with ex-ante spreads" → "higher net multiples and outperformance of IG/HY bonds; IRR coefficient insignificant" | – |
| 5 | recheck | §2.4 structural view, l.81 (Black–Cox) | "(Black-Cox 1976 [K])" → "(Black-Cox 1976 [unverified: paper text not read])" | – |
| 6 | recheck | §2.4 reduced-form view, l.82 | "Cox-process intensity, recovery ∝ market value (Jarrow-Turnbull; Duffie-Singleton; Lando)" → "intensity (Jarrow-Turnbull 1995), stochastic in Lando's (1998) Cox framework; recovery conventions attributed separately" | – |
| 7 | recheck | §3.3 convertibles, l.154 | "AFV (2003) [S] … or Tsiveriotis-Fernandes (1998) [K]" → "AFV linear-complementarity formulation with explicit default and recovery; T–F caveat" | – |
| 8 | missing_reference | §3.4 NAV-loan pool, l.158 | "RFT-TA" → "RFT-TA; Takahashi & Alexander 2002 (new ref 56)" | – |
| 9 | missing_reference | §3.8 actuarial, l.195 | "(Mack or bootstrap); Bühlmann credibility" → "(Mack's 1993 chain-ladder SE, or bootstrap); Bühlmann (1967) (new refs 61, 60)" | – |
| 10 | recheck | §4.4 table, EFW row, l.268 | "GPME +$0.041 per $1, insignificant" → "RAP −$0.001 per $1, t = −0.01; GPME with stock factor +$0.041, t = 1.48" | – |
| 11 | usage | §4.6 table, smoothing row, l.298 | "≈0.5 per quarter (BGG-derived, stream 04)" → "stream 04's derivation, not a figure BGG report" | SG3b |
| 12 | usage | §4.7 competitor-supply bullet, l.305 | "pro-cyclical [S: IMF 2024] … BIS work finds" → "evidence is mixed [S: IMF 2024, pp. 60–61]; BIS (Aramonte & Avalos 2021)" | tokens |
| 13 | recheck | §6.8 table, underwritten row, l.530 | "[S-anchored: EFW, BM, Tac Opps]" → "Prior [I]; those sources report realised, not underwritten, returns" | – |
| 14 | inconsistency | §6.8 table, current-actual row, l.531 | "Geltner or GLM with λ ≈ 0.5" → "Geltner 1991 or Getmansky-Lo-Makarov 2004 (refs 57, 58)" | grep |
| 15 | metadata | §10 ref 41 (Cai & Haque) | Fed URL → "+ DOI 10.17016/2380-7172.3462; recovery figures (Fig. 15) are KBRA DLD" | grep; tokens |
| 16 | recheck | §10 ref 42 (EFW) | "NBER WP 32278" → "(March 2024), DOI 10.3386/w32278; all figures from this version; April 2026 draft noted" | tokens |
| 17 | metadata | §10 ref 51 (Kaplan & Strömberg 2003) | short title → "+ ': an empirical analysis of venture capital contracts'" | SG3f |
| 18 | metadata | §10 ref 52 (Kaplan & Schoar, orphan) | full entry → "withdrawn (number kept): never cited in the body" | – |
| 19 | recheck | §10 refs 53–55 (Black & Cox; Tsiveriotis & Fernandes; Lando) | "[K] … not re-verified" → full metadata: JF 31(2), 351–367; JFI 8(2); RDR 2(2–3), 99–120, with DOIs | SG3e; tokens |
| 20 | missing_reference | §10 new ref 56 | (none) → "Takahashi & Alexander (2002), JPM 28(2), 90–100" | tokens |
| 21 | missing_reference | §10 new ref 57 | (none) → "Geltner (1991), JREFE 4(3), 327–345, DOI 10.1007/BF00161933" | grep; tokens |
| 22 | missing_reference | §10 new ref 58 | (none) → "Getmansky, Lo & Makarov (2004), JFE 74(3), 529–609" | tokens |
| 23 | missing_reference | §10 new ref 59 | (none) → "Brown, Ghysels & Gredil (2023), RFS 36(3), 945–986" | tokens |
| 24 | inconsistency | §10 new ref 60 | (none) → "Bühlmann (1967), ASTIN 4(3), 199–207, DOI …8989 (…8023 is the 1969 sequel)" | grep; Crossref; tokens |
| 25 | missing_reference | §10 new ref 61 | (none) → "Mack (1993), ASTIN 23(2), 213–225, DOI 10.2143/AST.23.2.2005092 [I: probable intended work]" | SG3d; tokens |
| 26 | missing_reference | §10 new ref 62 | (none) → "Aramonte & Avalos (2021), The rise of private markets, BIS Quarterly Review Dec 2021" | SG3c |
| 27 | consistency_edit | end of file, ll.749–770 | (none) → corrections section (16 entries) | section audit |

### `groups/verification/G3_cap_solutions.verify.md` (2 changes; fix:G3)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | recheck | §4 after the citation table, l.152 | (no erratum) → "Erratum: refs 44–51 row wrongly passed Kaplan & Strömberg (2003) title" | tokens |
| 2 | consistency_edit | end of file | (none) → corrections section (one line) | section audit |

### `groups/dossiers/G4_coinvest.md` (19 changes; fix:G4)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §7 numerical pitfalls, barrier bullet, l.597 | "BGK shift (barrier × e^{−0.5826σ√Δ}) or simulate monthly" → "check κD·e^{+0.5826σ√Δ} (toward V) or weekly-or-finer steps; BGK's own minus use explained" | U-G4 |
| 2 | barrier_rerun | §6.3 book simulation, write-off rate row, l.425 | "2.5% / 2.1%" → "3.3%† (was 2.5%) / 2.8%† (was 2.1%)" | B01 |
| 3 | barrier_rerun | §6.3, net cash flow row, normal P90, l.422 | "+11.4" → "+11.3†" | B02 |
| 4 | barrier_rerun | §6.3, NAV gap row, l.428 | "−18.5/−3.5/+21.9%; −18.7/−3.0/+19.2%" → "−18.5/−3.6/+21.5%†; −18.8/−3.1/+19.3%†" | B03 |
| 5 | barrier_rerun | §6.3, new † note, l.430 | (none) → "re-run with 0.75D·e^{+0.5826σ_V√0.25}; continuous check 3.1% / 2.7%" | B04 |
| 6 | barrier_rerun | §6.8 calibration item 9, l.557 | "against the simulated 2–2.5% a year" → "≈2.8–3.3% a year" | B05 |
| 7 | consistency_edit | header, reproducibility bullet, l.7 | script attribution → "+ † cells re-run by the BGK-corrected script" | CG4a |
| 8 | barrier_rerun | §6.5 LEVER wipe-out, l.499 | "P(residual = 0) is 11.8% / 22.8%" → "at exit; unchanged by the fix; E3 sensitivity 11.8% / 22.9%" | B06 |
| 9 | usage | §1 item 7, recap bullet, l.76 | "raise distress probability 2.4× its mean" → "+84% debt → 2.4× target-firm mean (IV increment; OLS ≈0.4); ≈×1.1–1.7 at φ = 0.25" | read |
| 10 | usage | §4.1 table, Bhardwaj–Gupta–Howell row, l.182 | "distress probability ×2.4" → "increment tied to +84% debt (10-year IV; OLS ≈0.4)" | read |
| 11 | usage | §6.2 E5 recap hazard, l.340 | "target ×2.4 on the distress mean [S]" → "×1.1 (OLS) to ×1.7 (IV) at φ = 0.25 [I]" | SG4a |
| 12 | usage | §4.2 size bullet, l.197 | "Lopez-de-Silanes et al.: diseconomies of scale" → "not deal-size evidence: scale = number of simultaneous investments" | SG4b |
| 13 | usage | §4.1 table, Lopez-de-Silanes et al. row, l.179 | "median IRR falls from 36% to 16%" → "+ scale = simultaneous investments, not deal size" | – |
| 14 | metadata | §10 ref 5 (Lopez-de-Silanes, Phalippou & Gottschalg) | "Giants at the gate" → full title; DOI 10.1017/S0022109015000113 | tokens |
| 15 | metadata | §10 ref 6 (Kaplan & Strömberg) | "NBER WP 14207 (JEP 23(1), 2009)" → "JEP 23(1):121–146, DOI 10.1257/jep.23.1.121" | tokens |
| 16 | missing_reference | §10 new ref 30 | (none) → "Axelson, Jenkinson, Strömberg & Weisbach (2013), JF 68(6):2223–2267, DOI 10.1111/jofi.12082" | SG4c; tokens |
| 17 | missing_reference | §10 new ref 31 | (none) → "Axelson, Sorensen & Strömberg (2014), preliminary draft, source of β = 2.3" | SG4d |
| 18 | missing_reference | §10 new ref 32 | (none) → "Broadie, Glasserman & Kou (1997), MF 7(4):325–349, DOI 10.1111/1467-9965.00035" | SG4e; tokens |
| 19 | consistency_edit | end of file | (none) → corrections section (17 change lines + 'Not changed' line) | section audit |

### `groups/verification/G4_coinvest.verify.md` (7 changes; fix:G4)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | barrier_rerun | §4 R14, second bullet, l.198 | "2.1–2.5% a year … about double KS" → "≈2.8–3.3% after the fix, ≈2.3–2.8× KS's 1.2%" | B07 |
| 2 | barrier_rerun | §4 R2, new final bullet, l.135 | (none) → "quarterly-test rates stand; continuous 62.2% / 73.4%" | B08 |
| 3 | barrier_rerun | §4 R3, new final bullet, l.143 | (none) → "at-exit probabilities, unchanged; E3 sensitivity 7.6% → 22.9%" | B09 |
| 4 | barrier_rerun | §5 re-computation, wipe-out line, l.226 | "wipe-out 2.1% → 11.8%; 7.0% → 22.8%" → "wipe-out at exit … [re-checked: unchanged]" | B10 |
| 5 | usage | §4 R4, fix bullet, l.149 | "multiplier over roughly 1.4–3.4" → "+ [1.4–3.4 applies to +84% debt; ≈×1.1–1.7 at φ = 0.25]" | grep |
| 6 | usage | §3 citation problems, new erratum line, l.111 | (none) → "Erratum: log missed the BGK sign error and the LPG 'scale' misreading" | grep |
| 7 | consistency_edit | end of file | (none) → corrections section (6 entries) | section audit |

### `groups/dossiers/G5_public_markets.md` (27 changes; fix:G5)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §3 methods table, transaction costs, l.210 | "Almgren–Chriss schedule [nrv]" → "Almgren–Chriss (2001) schedule [nrv]" | – |
| 2 | metadata | §10 [nrv] list, Almgren & Chriss | "(2000) J. Risk" → "(2001) Optimal execution of portfolio transactions, J. Risk 3(2), 5–39, DOI 10.21314/jor.2001.041" | SG5a; tokens |
| 3 | metadata | §10 ref 8 (Barras, Scaillet & Wermers) | short title → "+ ': Measuring luck in estimated alphas'" | SG5b |
| 4 | metadata | §10 ref 12 (Bollen & Pool) | short title → "+ 'Evidence from the pooled distribution'" | – |
| 5 | metadata | §10 ref 16 (Chen, Goldstein & Jiang) | short title → "+ ': Evidence from mutual fund outflows'" | – |
| 6 | metadata | §10 ref 30 (Jagannathan, Malakhov & Novikov) | short title → "+ 'An empirical evaluation'" | – |
| 7 | metadata | §10 ref 7 (Asness, Krail & Liew) | "JPM" → "JPM 28(1), 6–19, DOI 10.3905/jpm.2001.319819" | tokens |
| 8 | metadata | §10 ref 9 (Ben-David, Birru & Rossi) | "RCFS 15(3)" → "15(3), 704–747, DOI 10.1093/rcfs/cfag015" | tokens |
| 9 | metadata | §10 ref 14 (Brooks, Gould & Richardson) | "JFI" → "29(4), 5–19, DOI 10.3905/jfi.2020.1.086" | tokens |
| 10 | metadata | §10 ref 27 (Getmansky, Lee & Lo) | "ARFE 7" → "7(1), 483–577, DOI 10.1146/annurev-financial-110311-101741" | tokens |
| 11 | metadata | §10 ref 34 (Pástor, Stambaugh & Taylor) | "JFE" → "JFE 116(1), 23–45, DOI 10.1016/j.jfineco.2014.11.008" | tokens |
| 12 | metadata | §10 ref 18 (Dao et al.) | arXiv → "+ published J. Investment Strategies 7(1), 61–84 (2017), DOI 10.21314/jois.2017.093" | tokens |
| 13 | inconsistency | §3 methods table, de-smoothing row, l.207 | "Geltner AR(1) [nrv]" → "Geltner (1993, JRER) AR(1) [nrv]" | SG5c |
| 14 | inconsistency | §10 [nrv] list, Geltner | "Geltner (1993)" → full entry, JRER 8(3), 325–345, DOI 10.1080/10835547.1993.12090713 | grep; tokens |
| 15 | metadata | §10 [nrv] list, Davis & Norman | short → "Portfolio selection with transaction costs, MOR 15(4), 676–713, DOI 10.1287/moor.15.4.676" | tokens |
| 16 | metadata | §10 [nrv] list, Granger et al. | "as summarised by Man" → "Granger, Greenig, Harvey, Rattray & Zou (2014), Rebalancing risk, SSRN, DOI 10.2139/ssrn.2488552" | tokens |
| 17 | metadata | §10 [nrv] list, Jenkinson et al. | "JF 71(5), 2333–2370 findings" → "Picking winners? …, JF 71(5), 2333–2370, with DOI" | tokens |
| 18 | metadata | §10 [nrv] list, Kosowski et al. | "JFE 84(1)" → "Do hedge funds deliver alpha? …, JFE 84(1), 229–264, with DOI" | tokens |
| 19 | metadata | §10 [nrv] list, Leland | "Leland (1999)" → "(1999; SSRN record dated 2000), Optimal portfolio management with transactions costs and capital gains taxes, with DOI" | – |
| 20 | metadata | §10 [nrv] list, Rattray et al. | "JPM 46(6)" → "Strategic rebalancing, JPM 46(6), 10–31, with DOI" | tokens |
| 21 | consistency_edit | §10 [nrv] list structure | single memory list → memory-only paragraph + 'records verified after drafting' sub-list | CG5a |
| 22 | usage | §2.3 Aragon (2007), l.139 | "premium ≈4–7% a year is [nrv]" → "[S: abstract, confirmed in verification log A31]" | – |
| 23 | consistency_edit | §10 ref 6 (Aragon 2007) | "33–58 (bibliographic record only)" → "+ (log A31 later confirmed the 4–7% figure)" | CG5b |
| 24 | usage | §4.7 long-only evidence table, consultant row, l.352 | "no evidence of added value; [nrv]" → "(US active equity) 'no evidence that these recommendations add value'; [S] abstract confirmed" | – |
| 25 | usage | §6.14 bias table, consultant ratings row, l.718 | "Jenkinson et al. [nrv]" → "[S; evidence covers US active equity]" | – |
| 26 | consistency_edit | §8 evidence limits, l.826 | "Aragon; Fung–Hsieh; Jenkinson are [nrv]" → "only Fung–Hsieh (2000) bias sizes remain [nrv]" | CG5c |
| 27 | consistency_edit | end of file | (none) → corrections section (sources, one line per change, closing 'checked' note) | section audit |

### `groups/verification/G5_public_markets.verify.md` (2 changes; fix:G5)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §3 citation check, row 26 (Jenkinson et al.) | "JF volume and pages not independently checked" → "+ Update: Crossref confirms JF 71(5):2333–2370 with DOI" | tokens |
| 2 | consistency_edit | end of file | (none) → corrections section (row-26 update; audit agrees; open items listed) | section audit |

### `groups/dossiers/G6_private_credit.md` (27 changes; fix:G6)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §2.4 PIK bullet, l.128 | "PIK toggles add 1–2pp … (Rintamäki & Steffen, as cited by FSB) [S]" → "association with delinquency in US BDC data; second-hand via the FSB" | SG6a |
| 2 | usage | §6.4(2) PIK-cohort default, l.455 | "calibrated to Rintamäki–Steffen's +1–2pp" → "calibrated to the FSB's second-hand report of Rintamäki–Steffen" | – |
| 3 | usage | §5 peer allocators, l.374 | "U.S. public pensions ≈31% of PC fund investors" → "public and private pension funds together ≈31% ($307bn) of PC fund assets (Form PF, Q4 2021)" | SG6b |
| 4 | usage | §4.3 Berrospide et al., l.291 | "≈6.4% for BDCs" → "+ (the note's Table 1; its text gives 6.6%)" | SG6c |
| 5 | usage | §4.5 bank-line cost, l.343 | "≈6.4% … [S]" → "[S: Berrospide Table 1; text 6.6%]; either gives ≈S+180–230bp" | grep; tokens |
| 6 | usage | §6.5 regime table, back-leverage cost row, l.535 | "Fed 6.4% (2024-Q4)" → "+ (Table 1; the note's text gives 6.6%)" | – |
| 7 | missing_reference | §2.7 actuarial bullet, l.152 | "(Bühlmann)" → "(Bühlmann 1967)" | – |
| 8 | missing_reference | §3 methods table, TA row, l.169 | "Takahashi–Alexander (TA) fund model" → "+ (Takahashi & Alexander 2002; …)" | – |
| 9 | inconsistency | §3 methods table, desmoothing row, l.171 | "Geltner inverse" → "Geltner 1993 inverse" | grep |
| 10 | missing_reference | §7 libraries, l.683 | "Fine–Gray" → "Fine–Gray, i.e. Fine & Gray 1999" | – |
| 11 | consistency_edit | §10 tag legend, l.744 | [V]/[E]/[K] → "+ [M] = metadata confirmed in the 2026-10-18 literature check" | CG6a; tokens |
| 12 | recheck | §10 Cai & Haque (2024) | Fed URL → "+ DOI 10.17016/2380-7172.3462" | tokens |
| 13 | metadata | §10 Berrospide et al. (2025) | URL → "+ DOI 10.17016/2380-7172.3802" | tokens |
| 14 | recheck | §10 Erel, Flanagan & Weisbach (2024) | "NBER WP 32278" → "(March 2024), DOI 10.3386/w32278; SSRN version noted" | tokens |
| 15 | metadata | §10 Rintamäki & Steffen (2025) | "PIK Now and Pay Later … SSRN page not retrieved [E]" → "full title (… - How Deferred Interest Reshapes Private Credit), DOI 10.2139/ssrn.5341145" | tokens |
| 16 | metadata | §10 Altman et al. (2005) | "J. Business 78(6) [K]" → "full subtitle; metadata confirmed [M]" | – |
| 17 | metadata | §10 Duffie & Singleton (1999) | "RFS 12(4) [K]" → "12(4): 687–720, DOI 10.1093/rfs/12.4.687 [M]" | tokens |
| 18 | metadata | §10 Duffie, Eckner, Horel & Saita (2009) | "JF 64(5) [K]" → "64(5): 2089–2123, DOI 10.1111/j.1540-6261.2009.01495.x [M]" | tokens |
| 19 | recheck | §10 Lando (1998) | "RDR 2 [K]" → "2(2–3): 99–120, DOI 10.1007/BF01531332 [M]" | tokens |
| 20 | metadata | §10 Vasicek (2002); Gordy (2003) | "Risk 15(12); Gordy …" → "Risk 15(12): 160–162 (no DOI); Gordy JFI with metadata [M]" | tokens |
| 21 | metadata | §10 Frye (2000) | "Risk 13(4) [K]" → "Risk 13(4), April 2000; FRB Chicago copy title noted [M]" | tokens |
| 22 | metadata | §10 Geltner (1993); Getmansky, Lo & Makarov (2004) | "JRER 8(3); GLM …" → "JRER 8(3): 325–345, DOI; GLM JFE 74(3): 529–609, DOI [M]" | tokens |
| 23 | metadata | §10 Stanton (1995) | "RFS 8(3) [K]" → "8(3): 677–708, DOI 10.1093/rfs/8.3.677 [M]" | tokens |
| 24 | inconsistency | §10 new Bühlmann (1967) | (body-only mention) → "ASTIN 4(3): 199–207, DOI …8989; not the 1969 paper (…8023)" | SG6d; Crossref; tokens |
| 25 | missing_reference | §10 new Takahashi & Alexander (2002) | (none) → "JPM 28(2): 90–100, DOI 10.3905/jpm.2002.319836" | tokens |
| 26 | missing_reference | §10 new Fine & Gray (1999) | (none) → "A Proportional Hazards Model for the Subdistribution of a Competing Risk, JASA" | – |
| 27 | consistency_edit | end of file | (none) → corrections section (28 numbered entries + 'Checked' lines) | section audit |

### `groups/verification/G6_private_credit.verify.md` (3 changes; fix:G6)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §3 citation table, Rintamäki & Steffen row, l.138 | "SSRN page not retrieved … tagged [E]" → "+ [Added: Crossref confirms title and DOI]" | – |
| 2 | consistency_edit | §3 after the [K] list | (none) → "Update: the literature check has since confirmed all nine, plus Duffie et al. (2009)" | CG6b |
| 3 | consistency_edit | end of file | (none) → corrections section (4 entries) | section audit |

### `groups/dossiers/G7_liquidity_ladder.md` (30 changes; fix:G7)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §1 item 9 governance, l.125 | "A central Treasury owns the pool and the CFP" → "Corporate Finance, which owns the Treasury function, owns the pool and the CFP" | SG7a |
| 2 | usage | §6.11 governance heading and reporting line, l.815–817 | "Central Treasury [I] … reports to the CIO and IC" → "Corporate Finance, which owns the Treasury function [I; user-confirmed]; independent of return-seeking groups" | grep |
| 3 | consistency_edit | §6.11 conflict-control bullet, l.826 | "Treasury owns the decision;" → "Corporate Finance owns the decision;" | CG7a |
| 4 | consistency_edit | §9 open question 11, l.940 | "Central-Treasury mandate" → "Corporate Finance's Treasury mandate" | CG7b |
| 5 | usage | §2.5 Gorton–Metrick, l.220 | "repo haircuts rose in the 2007–08 run" → "in bilateral repo; tri-party was stable (Copeland, Martin & Walker 2014)" | SG7b |
| 6 | usage | §4.2(3) Li–Strahan–Zhang, new sub-bullet, l.341 | $482bn only → "+ draws met with Fed liquidity programs and deposit inflows; an oil–fiscal stress may lack that backstop" | SG7c |
| 7 | metadata | §2.4 Miller–Orr tag, l.214 | "[nrv]" → "(1966) [reference verified; reading not re-checked]" | – |
| 8 | missing_reference | §2.6 actuarial ruin, l.254 | "Gerber–Shiu severity budgets" → "Gerber–Shiu (1998) (new ref 48)" | – |
| 9 | missing_reference | §2.6 queueing, l.255 | "Little's law [I]" → "Little's law (Little 1961) [I] (new ref 49)" | – |
| 10 | usage | §2.6 queueing, stationarity caveat | (no condition) → "proved for strictly stationary processes; use for normal-state throughput only" | – |
| 11 | missing_reference | §6.4 rare events, l.563 | "Clopper–Pearson bounds" → "Clopper–Pearson (1934) bounds (new ref 50)" | – |
| 12 | missing_reference | §7 reverse stress, l.886 | "Glasserman–Kang–Kang conditional means" → "Glasserman–Kang–Kang (2015) (new ref 47)" | – |
| 13 | metadata | §10 ref 16 (WilmerHale) | "Secondary market for PE interests" → "Beaudoin, Berrent, Evans & Rothermel (2009), 'Trends in the Private Equity Secondary Market: A Response to Today's Financial Markets'" | – |
| 14 | metadata | §10 ref 20 (Schrimpf, Shin & Sushko) | no title → "'Leverage and margin spirals in fixed income markets during the Covid-19 crisis', BIS Bulletin 2" | – |
| 15 | metadata | §10 ref 21 (Robinson & Sensoy) | no title → "'Cyclicality, performance measurement, and cash flow liquidity in private equity', JFE 122(3), 521–543, with DOI" | tokens |
| 16 | metadata | §10 ref 22 (Li, Strahan & Zhang) | short title → "+ ': Evidence from the COVID-19 Crisis', RCFS 9(3), 472–500, DOI 10.1093/rcfs/cfaa009" | tokens |
| 17 | metadata | §10 ref 23 (Acharya & Steffen) | short title → "+ ' in the Midst of COVID', RCFS 9(3), 430–471, with DOI" | tokens |
| 18 | metadata | §10 ref 24 (Gorton & Metrick) | "JFE 104(3)" → "104(3), 425–451, DOI 10.1016/j.jfineco.2011.03.016" | tokens |
| 19 | metadata | §10 ref 25 (Schmieder et al.) | IMF WP/12/3 → "+ DOI 10.5089/9781475502466.001 (PDF title page lists five authors)" | tokens |
| 20 | metadata | §10 ref 26 (Brunnermeier & Pedersen) | no title → "'Market Liquidity and Funding Liquidity', RFS 22(6), 2201–2238, DOI 10.1093/rfs/hhn098" | tokens |
| 21 | metadata | §10 ref 27 (Bolton, Chen & Wang) | no title → "'A Unified Theory of Tobin's q, Corporate Investment, Financing, and Risk Management', JF 66(5), 1545–1578, with DOI" | tokens |
| 22 | metadata | §10 ref 28 (Ang, Papanikolaou & Westerfield) | no title → "'Portfolio Choice with Illiquid Assets', MS 60(11), 2737–2761, with DOI" | tokens |
| 23 | metadata | §10 ref 29 (Nadauld et al.) | no title → full title; JFE 132(3), with DOI | tokens |
| 24 | metadata | §10 ref 30 (Miller & Orr) | "QJE 80(3) [nrv]" → "80(3), 413–435, DOI 10.2307/1880728; reference verified" | tokens |
| 25 | missing_reference | §10 new ref 47 | (none) → "Glasserman, Kang & Kang (2015), Stress scenario selection by empirical likelihood, QF 15(1), 25–41" | tokens |
| 26 | missing_reference | §10 new ref 48 | (none) → "Gerber & Shiu (1998), On the Time Value of Ruin, NAAJ 2(1), 48–72, with DOI" | tokens |
| 27 | missing_reference | §10 new ref 49 | (none) → "Little (1961), A Proof for the Queuing Formula: L = λW, OR 9(3), 383–387, with DOI" | SG7d; tokens |
| 28 | missing_reference | §10 new ref 50 | (none) → "Clopper & Pearson (1934), Biometrika 26(4), 404–413, with DOI" | tokens |
| 29 | missing_reference | §10 new ref 51 | (none) → "Copeland, Martin & Walker (2014), Repo Runs: Evidence from the Tri-Party Repo Market, JF 69(6), 2343–2380, DOI 10.1111/jofi.12205" | SG7e; tokens |
| 30 | consistency_edit | end of file | (none) → corrections section (sources paragraph + one line per change) | section audit |

### `groups/verification/G7_liquidity_ladder.verify.md` (1 changes; fix:G7)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | inconsistency | end of file, erratum | (none) → "Erratum: §3 flagged three of the eight incomplete titles; Robinson & Sensoy, Ang et al., Nadauld et al. were marked 'None'" | section audit |

### `groups/dossiers/G8_org_tpa_economics.md` (22 changes; fix:G8)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §10 ref #5 (Lamont 1997) | "JF 52(1):57–82" → "52(1):83–109, DOI 10.1111/j.1540-6261.1997.tb03809.x (57–82 is Carhart 1997)" | SG8a; tokens |
| 2 | metadata | §10 ref #4 (Shin & Stulz 1998) | "(WP: NBER 5639)" → pointer dropped (w5639 is a different paper) | SG8b |
| 3 | usage | §1 item 5, evidence bullet (Glaser et al.) | "all unit managers over-budgeted capex (Glaser et al. 2013)" → "+ wording from the abstract on the RePEc/IDEAS page" | grep |
| 4 | usage | §2.2 practice bullet (Glaser et al.) | "about 40% more (Glaser et al. 2013)" → "+ (RePEc/IDEAS abstract page, §10 #9)" | – |
| 5 | usage | §4 evidence table, power and over-budgeting row | "powerful managers invest about 40% more of windfalls" → "obtain larger shares of cash windfalls and raise investment about 40% more" | grep |
| 6 | metadata | §10 ref #9 (Glaser et al.) | RePEc link → "+ DOI 10.1111/jofi.12046; source of quoted wording noted" | grep; tokens |
| 7 | missing_reference | §2.7 decision stakes (Crawford & Sobel orphan) | listed but never cited → "new sentence on strategic communication citing Crawford & Sobel (1982)" | SG8c |
| 8 | metadata | §10 ref #24 (Crawford & Sobel 1982) | RePEc → "+ DOI 10.2307/1913390" | tokens |
| 9 | usage | §2.1 theory, winner-picking (Stein 1997) | "works best in focused firms" → "internal capital markets may work better in relatively focused firms" | SG8d |
| 10 | metadata | §1 item 5, Boutilier in-text | "(Boutilier 2011)" → "(Boutilier 2012)" | – |
| 11 | metadata | §2.7 decision stakes (Boutilier; Chen et al. tag) | "(Boutilier 2011) … [M; DOI resolves]" → "(Boutilier 2012) … [S; abstract confirmed]" | grep |
| 12 | metadata | §10 ref #40 (Boutilier) | "(2011/2012) arXiv:1106.2489" → "(2012) AAMAS 2012 proceedings; arXiv kept" | – |
| 13 | metadata | §10 ref #41 (Chen, Kash, Ruberry & Shnayder 2014) | "ACM TEAC 2(2) [M]" → "2(2):1–27" | tokens |
| 14 | metadata | §10 ref #38 (Gneiting 2011) | "(journal details [M])" → "+ DOI 10.1198/jasa.2011.r10138" | tokens |
| 15 | metadata | §10 ref #11 (Kuppuswamy & Villalonga 2016) | short title → "+ ': Evidence from the 2007–2009 financial crisis', with DOI" | tokens |
| 16 | metadata | §10 ref #13 (Alonso, Dessein & Matouschek 2008) | AER 98(1):145–179 → "+ corrigendum AER 98(3):1195–1196, DOI 10.1257/aer.98.3.1195" | tokens |
| 17 | recheck | §10 ref #44 (Smith & Winkler 2006) | short title → full subtitle, with DOI | – |
| 18 | recheck | §10 ref #48 (Erel, Flanagan & Weisbach 2024) | "NBER WP 32278" → "(March 2024), DOI 10.3386/w32278" | tokens |
| 19 | metadata | §10 ref #50 (Nadauld et al., market-data entry) | NBER link → "JFE 132(3):158–181, with DOI; NBER WP 22404" | tokens |
| 20 | consistency_edit | §10 ref #52 (Urwin & Hayman 2026) | short title → "full title (… for Navigating the Transition to TPA), DOI 10.56227/26.1.20" | CG8a; tokens |
| 21 | metadata | end of §10, background-only list | "Not verified in-session (background only)" → "Background only (existence and metadata confirmed in the G8 literature review): bulleted entries" | – |
| 22 | consistency_edit | end of file | (none) → corrections section (17 lines) | section audit |

### `groups/verification/G8_org_tpa_economics.verify.md` (2 changes; fix:G8)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §3, new line after the citation-check table | (Lamont accepted at 57–82) → "Erratum: the Lamont row and F4 wrongly accepted 52(1):57–82 (Carhart 1997)" | tokens |
| 2 | consistency_edit | end of file | (none) → corrections section (erratum; F18 re-check holds) | section audit |

### `groups/dossiers/G9_synthetic_data.md` (35 changes; fix:G9)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §1 item 4, anchoring bullet, l.48 | "weight about 0.3 on the anchor [S: Campbell & Sharpe]" → "on the previous release, a realized value; calibrates w_a or ρ_f, not w_u" | SG9a |
| 2 | missing_reference | §2.2 OSSE analogy, l.93 | "OSSEs [†]" → "[S: Errico et al. 2013; Privé et al. 2013] (refs 39–40)" | tokens |
| 3 | usage | §2.5 table, appraisal row, evidence, l.124 | "BGG λ 0.951 … noise 4.6% [S, via 04]" → "+ 2020 working-paper figures, not in the RFS abstract" | SG9b |
| 4 | inconsistency | §2.5 table, appraisal row, module, l.124 | "Geltner/BGG filter" → "Geltner (1993)/BGG filter (ref 38)" | SG9b |
| 5 | usage | §2.5 table, anchoring row, module, l.125 | "weight w_u on underwriting" → "w_a on the latest actual, or ρ_f; w_u is an [I] analogy" | – |
| 6 | recheck | §3.3 vine copulas, l.174 | "(Aas et al., via 10) [†]" → "(Aas et al. 2009, via 10) [S]" | – |
| 7 | metadata | §3.4 step 1, l.179 | "[† Keelin 2016]" → "[S: Keelin 2016]" | – |
| 8 | metadata | §3.5 table, stylized-fact row, l.190 | "Cont 2001 †" → "Cont 2001 [S]" | – |
| 9 | metadata | §3.5 table, MMD row, l.193 | "Gretton et al. 2012 †" → "MMD: Gretton et al. 2012 [S]" | – |
| 10 | usage | §4.1 table, PME row source, l.253 | "HJK, Burgiss, 'over 200 investment programs' [S]" → "HJK working paper (NBER WP 17874, Feb 2012) … [S: WP figures; JF abstract covers 'nearly 1,400' funds]" | SG9c |
| 11 | metadata | §5 item 2, l.435 | "López de Prado's case … (†)" → "(2018, ch. 13, 'Backtesting on Synthetic Data') [S]" | – |
| 12 | missing_reference | §5 item 3, reserving bullet, l.437 | "(†)" → "+ e.g. Gabrielli & Wüthrich (2018) calibrated claims simulator" | – |
| 13 | usage | §6.4, sentence after defaults table, l.594 | "anchoring weight 0.2–0.45 around Campbell–Sharpe ≈0.3 [S-anchored]" → "w_u 0.2–0.45 [I]; C–S ≈0.3 anchors w_a or ρ_f" | – |
| 14 | metadata | §10 ref 1 (Brown, Gredil & Kaplan) | "JFE 132(2) (online 2018)" → "+ 267–297, DOI 10.1016/j.jfineco.2018.10.011" | tokens |
| 15 | metadata | §10 ref 2 (Harris, Jenkinson & Kaplan) | JF 69(5):1851–1882; NBER WP 17874 → "+ DOI 10.1111/jofi.12154; WP (Feb 2012) is the source of the §4.1 figures" | tokens |
| 16 | metadata | §10 ref 3 (Gompers, Gornall, Kaplan & Strebulaev) | "JFE (volume and pages not verified)" → "JFE 135(1):169–190 (2020), DOI 10.1016/j.jfineco.2019.06.011" | tokens |
| 17 | metadata | §10 ref 4 (Jenkinson, Landsman, Rountree & Soonawalla) | TAR 95(1):191–210 → "+ (online 2019), DOI 10.2308/accr-52486" | tokens |
| 18 | metadata | §10 ref 8 (Campbell & Sharpe) | "(published JFQA 2009 †)" → "JFQA 44(2):369–390 (2009), DOI 10.1017/S0022109009090127" | tokens |
| 19 | metadata | §10 ref 9 (Coibion & Gorodnichenko) | short title → "+ ': A simple framework and new facts', DOI 10.1257/aer.20110306" | tokens |
| 20 | metadata | §10 ref 10 (Bordalo, Gennaioli, Ma & Shleifer) | AER 110(9):2748–82 → "+ DOI 10.1257/aer.20181219" | tokens |
| 21 | metadata | §10 ref 11 (Getmansky, Lo & Makarov) | JFE 74(3):529–609 → "+ DOI 10.1016/j.jfineco.2004.04.001" | tokens |
| 22 | metadata | §10 ref 12, BGG item | "Brown, Ghysels & Gredil (2023);" → "RFS 36(3):945–986, DOI 10.1093/rfs/hhac045; λ and noise are WP figures" | tokens |
| 23 | metadata | §10 ref 13, from-memory list | † on Keelin, Cont, Gretton … → "† removed for confirmed items; Fang, Braun and Barras keep †" | – |
| 24 | missing_reference | §10 ref 15 (Cook, Gelman & Rubin) | DOI + PDF → "+ correction: Gelman (2017), JCGS 26(4)" | tokens |
| 25 | metadata | §10 ref 16 (Modrák et al.) | "(2023) Bayesian Analysis, doi" → "(2025) 20(2):461–488 (advance publication 2023)" | SG9d; tokens |
| 26 | metadata | §10 ref 18 (TabDDPM) | "ICML 2023 (PMLR 202)" → "PMLR 202:17564–17579" | tokens |
| 27 | metadata | §10 ref 19 (Borisov et al., GReaT) | "Borisov, V. et al. (2023), arXiv" → "Borisov, Seßler, Leemann, Pawelczyk & Kasneci (2023), ICLR 2023 (poster)" | – |
| 28 | metadata | §10 ref 20 (Alaa et al.) | arXiv → "ICML 2022, PMLR 162:290–306" | tokens |
| 29 | metadata | §10 ref 21 (Lopez-Paz & Oquab) | arXiv → "ICLR 2017" | – |
| 30 | metadata | §10 ref 22 (Quant GANs) | "QF" → "QF 20(9):1419–1440, DOI 10.1080/14697688.2020.1730426" | tokens |
| 31 | metadata | §10 ref 24 (Synthcity) | short title → full title; arXiv:2301.07573 | – |
| 32 | inconsistency | §10 new ref 38 (Geltner) | (body-only 'Geltner/BGG filter') → "Geltner (1993), JRER 8(3):325–345, with DOI; choice of 1993 marked [I]" | tokens |
| 33 | missing_reference | §10 new refs 39–40 (OSSE sources) | (none) → "Errico et al. (2013); Privé et al. (2013): OSSE development and validation" | – |
| 34 | missing_reference | §10 new ref 41 (claims simulator) | (none) → "Gabrielli & Wüthrich (2018), An individual claims history simulation machine, Risks 6(2):29, DOI 10.3390/risks6020029" | tokens |
| 35 | consistency_edit | end of file | (none) → sub-heading for refs 38–41 + corrections section | section audit; tokens |

### `groups/verification/G9_synthetic_data.verify.md` (1 changes; fix:G9)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | end of file, erratum | (none) → "Erratum (§3, Modrák et al. row): year 2023 accepted; the article is BA 20(2):461–488 (2025)" | SG9e; tokens |

### `clusters/C1_portfolio_math.md` (9 changes; fix:clusters)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | missing_reference | §2 verification table, row 10-4/10-5 (ENS gates) | "… use Kish ESS and maximum weight" → "+ the ENS diagnostic is Meucci (2012)" | – |
| 2 | recheck | §5.7 policy-rule table, payout top-up row | "(de Finetti barrier)" → "(a de Finetti-style barrier on the top-up only; the classic barrier has no minimum payout)" | – |
| 3 | metadata | §5.10 regimes | "Shu–Yu–Mulvey [S]" → "Shu, Yu & Mulvey (2024), JAM 25(5):493–507, DOI 10.1057/s41260-024-00376-x" | SC1a; tokens |
| 4 | recheck | §5.10 paths (Broadie–Du–Moallemi) | "regression proxies for future-node risk, not nested simulation" → "regression-based nested simulation with few inner draws (BDM 2015, OR 63(5):1077–1097, DOI)" | tokens |
| 5 | metadata | §7 calibration table, Luxenberg row | "arXiv:2207.07767" → "Luxenberg et al., ICAIF '22, DOI 10.1145/3533271.3561769 (preprint arXiv)" | tokens |
| 6 | recheck | §9 insight 4 (actuarial ruin) | "de Finetti barrier gives the payout band; Gerber–Shiu …" → "+ de Finetti's criterion does not bound ruin by itself, so Gerber–Shiu …" | – |
| 7 | missing_reference | §13 key references | "Dowson (2020); Boyd et al. (2017); Luxenberg et al. (2022)" → "+ Klaassen (2002), MS 48(11):1512–1516, DOI; Luxenberg (ICAIF '22)" | SC1b; tokens |
| 8 | metadata | §13 unverified [U] list | long [U] list → "[U] cut to GMO/RA CMAs, SDDP.jl claim, Towers Perrin horizon; new 'verified by the literature audit' block" | – |
| 9 | consistency_edit | end of file | (none) → corrections section (+ checked-unchanged items) | section audit |

### `clusters/C2_private_liquidity.md` (7 changes; fix:clusters)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §1 market-fact corrections, Sorensen–Wang–Yang | "RFS 27(7)" → "27(7):1977–2021, not 27(2)" | SC2b; tokens |
| 2 | metadata | §1 market-fact corrections, WilmerHale | hypothetical note → "+ source: 'Trends in the Private Equity Secondary Market', ABA BLT 18(4), 2009" | tokens |
| 3 | usage | §1 market-fact corrections, Bollen–Sensoy | "5–10pp comes from the 2015 WP" → "+ published FM 51(2):501–538 (2022): breakeven ≈ observed returns for LPs with ≤40% PE" | SC2a; tokens |
| 4 | metadata | §1 '[U] items' list | Jenkinson–Sousa–Stucke and Barber–Yasuda in [U] → "removed from [U]; resolved note" | – |
| 5 | usage | §4.1 E7′ reported NAV | "BGG's weekly 0.951 implies ≈0.66 … [S*]" → "+ both inputs are WP figures the published RFS abstract does not report" | – |
| 6 | usage | §6 calibration table, NAV smoothing row | "2023 / Brown–Ghysels–Gredil, RFS 36(3) / High" → "WP figures / derived by the stream-04 verifier from BGG WP figures" | – |
| 7 | consistency_edit | end of file | (none) → corrections section (+ barrier note on quarterly-tested covenants) | section audit |

### `clusters/C3_liabilities_overlay.md` (5 changes; fix:clusters)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §2.1 corrections table, Ennis row | "… the −1.87% is from the 2021 paper" → "+ (Ennis 2021, J. Investing, DOI 10.3905/joi.2021.1.166); −1.87% probable source JPM 2021 [unverified]" | tokens |
| 2 | metadata | §3 decision register, DQ24 | "(the CFA guide flags confounders)" → "(the CFA Institute guide, Urwin & Hayman 2026, DOI 10.56227/26.1.20, flags confounders)" | tokens |
| 3 | usage | §6 calibration table, J–R benchmark row | "10.1% (exact); 9.97% (approx.) / IMF WP/06/229 / high" → "both WP figures; EJ 121(555):905–930 (2011) gives 9.1% per a citing abstract" | SC3a; tokens |
| 4 | metadata | §12 source pointers | "Jeanne–Rancière IMF WP/06/229" → "+ published as EJ 121(555):905–930 (2011), DOI 10.1111/j.1468-0297.2011.02435.x" | tokens |
| 5 | consistency_edit | end of file | (none) → corrections section (no conclusion changes; §5.7 uses ADIC parameters) | section audit |

### `clusters/C4_agentic_ic.md` (22 changes; fix:clusters)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §2.1 verification ledger, V5 | "69% …; 66% on clean 2025 papers (Nature, 25 Mar 2026)" → "+ neither figure is in the Nature abstract; 69% traced to Sakana's blog" | SC4a |
| 2 | usage | §8 calibration table, AI-reviewer row | "25 Mar 2026 / Nature (Lu et al.) / High" → "26 Mar 2026 / Sakana blog on the Nature paper; abstract reports 70% acceptance" | – |
| 3 | usage | §8 calibration table, Kosmos row | "79.4% / Nov 2025 / Kosmos / High" → "79.4%, although every statement cited code or primary literature" | – |
| 4 | usage | §2.2 [U] list, Schwenk (1990) | "the Schwenk (1990) result" → "removed from [U]; resolved: OBHDP 47(1):161–176, audit wording" | tokens |
| 5 | recheck | §2.2 [U] list, MAP | "steps of MAP (paywalled)" → "finer points of MAP, including whether it prescribes pre-votes [U]" | – |
| 6 | usage | §2.2 [U] list, MLReplicate | "MLReplicate's '59%'" → "removed from [U]; confirmed: 10 of 37 accepted; 59% of expert evaluations" | – |
| 7 | recheck | §3 design question 34 (IC record format) | "transparency adds discipline but can chill dissent (HMP 2018; M&S 2008)" → "trade-off (M&S 2008); HMP find discipline and conformity effects, discipline dominating on their measure" | – |
| 8 | usage | §5.7(e) shrinkage diagnostic | "Alert if s_i<0.5 …" → "+ the ratio shrinks nothing; Smith & Winkler's remedy is Bayesian shrinkage" | – |
| 9 | usage | §5.7(g) deflation of the search maximum | "h_200 ≈ 3.47σ" → "+ assumes a normal null; for Sharpe statistics use the full DSR" | – |
| 10 | usage | §6.9 safeguards, item 6 (automation bias) | "human-first pre-votes; seeded-error drill …" → "training does not prevent it, even in experts (P&M 2010); prevention via workflow; drills measure" | SC4c |
| 11 | metadata | §14 key references, Nature paper | "Lu et al. (2026), Nature 651:914–919" → full author list; title; 651(8107):914–919; DOI | tokens |
| 12 | missing_reference | §14 key references, MLReplicate | (not listed) → "Gaddipati et al. (2026), MLReplicate, arXiv:2605.16616" | – |
| 13 | metadata | §14 key references, deliberation | "Wynn et al. (2025); Smit et al., arXiv" → "Wynn (ICML 2025 MAS workshop); Smit et al., ICML 2024, PMLR 235:45883–45905" | tokens |
| 14 | recheck | §14 key references, Vaccaro; Fogliato | short entries → "Vaccaro, Almaatouq & Malone, NHB 8(12):2293–2303, DOI; Fogliato et al. FAccT '22 author order" | tokens |
| 15 | recheck | §14 key references, Hackenburg; Salvi | short entries → "Hackenburg et al., Science 390(6777):eaea3884, DOI; Salvi et al., NHB 9(8):1645–1653" | tokens |
| 16 | missing_reference | §14 key references, Parasuraman & Manzey | (not listed) → "P&M (2010), Human Factors 52(3):381–410, DOI 10.1177/0018720810376055" | tokens |
| 17 | inconsistency | §14 key references, Bühlmann (1967) | "Bühlmann (1967)" → "+ ASTIN 4(3):199–207, DOI …8989; …8023 is the 1969 sequel" | SC4b; Crossref; tokens |
| 18 | metadata | §14 key references, Bailey et al. (PBO) | "J. Comput. Finance (2017)" → "20(4) (2017), DOI 10.21314/JCF.2016.322" | tokens |
| 19 | recheck | §14 key references, Smith & Winkler | short → full title; MS 52(3):311–322, DOI | tokens |
| 20 | metadata | §14 key references, Dwork et al. | "arXiv:1506.02629" → "+ journal version 'The reusable holdout', Science (2015), DOI 10.1126/science.aaa9375" | tokens |
| 21 | missing_reference | §14 key references, DSR, KLS 2019, Schwenk | (not listed) → "Bailey & López de Prado (2014) DSR; Kahneman, Lovallo & Sibony (2019); Schwenk (1990)" | – |
| 22 | consistency_edit | end of file | (none) → corrections section (sources, changes, checked-unchanged items) | section audit |

### `groups/clusters/GC1_private_groups.md` (16 changes; fix:group-clusters)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | barrier_rerun | §1 executive summary item 6, l.34 | "lifts wipe-out probability from 2.1% to 11.8% …; 1.5× trigger on 50–63%" → "at-exit wipe-out; 50–63% quarterly-tested, 62–73% if continuous; BGK fix changes neither" | B11 |
| 2 | usage | §3 D4 SACV/MACV risk, l.70 | "Boyer et al.'s β>2 is discount-rate risk …" → "+ published as JF 78(2):835–885 (2023), DOI 10.1111/jofi.13202; β>2 is a 2018 WP figure" | SGC1a; tokens |
| 3 | barrier_rerun | §3 D19 co-investment reference class, l.85 | "write-off target 1.2–1.7%/yr" → "+ corrected G4 book simulation writes off 2.8% normal / 3.3% drought, 2.3–2.8× KS; recalibrate κ or ICR hazard" | B12 |
| 4 | usage | §3 D20 recap distress effect, l.86 | "multiplier 1.4 (OLS) to 3.4 (IV), central 2.0 [I]" → "scaled to recap size: ≈1.1–1.7 at φ = 0.25" | SGC1b |
| 5 | recheck | §4.3 natural-hedge test, l.148 (Böni & Manigart) | "spread effect with a TED effect twice persistence; EFW zero alpha" → "ex-ante spread effect in net multiples and PME vs bonds; IRR coefficient insignificant" | – |
| 6 | barrier_rerun | §4.4 spec card, E3, l.163 | "barrier V ≤ κD, monitored monthly or with a BGK shift" → "continuously monitored; quarterly checks test κD·e^{+0.5826σ√Δ} or weekly-or-finer steps" | B13 |
| 7 | barrier_rerun | §4.4 spec card, REFINANCE, l.168 | "49.6% / 62.5%; 32.7% / 47.9% [C]" → "+ continuous 62.2% / 73.4% and 42.5% / 57.4% [I-calc]; quarterly figures stand" | B14 |
| 8 | barrier_rerun | §4.4 spec card, LEVER, l.169 | "wipe-out 2.1% → 11.8% and 7.0% → 22.8%" → "at exit; with the E3 barrier monitored throughout 2.2% → 11.8%, 7.6% → 22.9%" | B15 |
| 9 | inconsistency | §5 calibration, subscription lines source, l.203 | "Albertus & Denes" → "Albertus & Denes (2020 WP); probable successor JFQA (online 7 May 2026) [unverified]" | SGC1c |
| 10 | metadata | §5 calibration, buyer vs seller returns source, l.208 | "Nadauld et al., NBER w22404" → "+ (2016 WP figures); JFE 132(3):158–181, DOI; abstract 1.023 vs 0.976" | tokens |
| 11 | metadata | §5 calibration, tail-end value source, l.209 | "Nadauld et al. Tables 3, 6" → "NBER w22404 Tables 3, 6 (WP tables; not re-checked vs JFE)" | – |
| 12 | recheck | §5 calibration, hybrid-capital row, l.214 | "EFW net risk-adjusted profit ≈0" → "+ (RAP −0.001 per $1, t = −0.01, stock and bond factors)" | – |
| 13 | metadata | §5 calibration, zero-return and exits source, l.219 | "Lopez-de-Silanes et al., JFQA; Kaplan–Strömberg" → "full title, JFQA 50(3):377–411; KS JEP 23(1):121–146 (2009)" | tokens |
| 14 | usage | §5 calibration, recaps row, l.221 | "distress +3.9pp (OLS) to +22.4pp (IV)" → "+ for an 84% average rise in total debt (see D20); BGH cited" | – |
| 15 | recheck | §5 calibration, recoveries source, l.225 | "KBRA DLD via Fed FEDS Note" → "+ (Cai & Haque, 23 Feb 2024, DOI 10.17016/2380-7172.3462)" | tokens |
| 16 | consistency_edit | end of file | (none) → corrections section (15 changes + 'checked, no change' line) | section audit |

### `groups/clusters/GC2_liquidity_org_data.md` (6 changes; fix:group-clusters)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §4.4 flows, Private Credit row, l.335 | "$482bn … from existing commitments [S]" → "+ banks met draws via Fed programs, deposit inflows and capital; an oil–fiscal stress may lack this" | SGC2a |
| 2 | usage | §5 calibration, revolver dash-for-cash row, l.641 | "C&I loans +$482bn / LSZ" → "+ met with Fed support and deposit inflows / LSZ, RCFS 9(3):472–500" | grep; tokens |
| 3 | metadata | §2 verification ledger, G8 row, l.93 | "Shin–Stulz WP pointer mislabelled" → "+ (w5639 is a different 1996 paper; the QJE citation stands)" | – |
| 4 | metadata | §2 verification ledger, G7 row, l.92 | "WilmerHale's 'given away' was a forecast" → "+ ('Trends in the PE Secondary Market', ABA BLT 18(4), 2009)" | tokens |
| 5 | metadata | §2 verification ledger, new line, l.96 | (none) → "Erratum: the G8 log accepted Lamont 52(1):57–82; pages are 83–109 (57–82 is Carhart)" | SGC2b; tokens |
| 6 | consistency_edit | end of file | (none) → corrections section (5 changes + 'checked, no change' line) | section audit |

### `addenda/gap_01.md` (7 changes; fix:main-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §1 must-fix ledger, G2 row (SACV risk) | "SACV σ 45–50% at β ≈ 2" → "+ [β ≈ 2 is the 2018 WP figure; the 2021 version / JF 2023 gives ≈1.8]" | – |
| 2 | usage | §1 must-fix ledger, G4 row (post-recap hazard) | "post-recap hazard ×1.4–3.4" → "≈×1.1 (OLS) to ×1.7 (IV) at φ = 0.25" | SMA1 |
| 3 | barrier_rerun | §1 must-fix ledger, G4 row (REFI breach, LEVER wipe-out) | "≈50% / 63% with quarterly tests; drought wipe-out 7.0% → 22.8%" → "+ (62–73% if continuous); wipe-out at exit" | B16 |
| 4 | consistency_edit | §2 group engines table, co-investment row | "write-off at V ≤ κD" → "monitored continuously (quarterly checks κD·e^{+0.5826σ√Δ}; RESULTS.md §1)" | CMA1 |
| 5 | barrier_rerun | §3 instrument library, Co REFI / LEVER row | "wipe-out 7.0% → 22.8%" → "at exit; with the E3 barrier at any time 7.6% → 22.9%" | B17 |
| 6 | recheck | sources, Cai & Haque (2024) | Fed URL → "+ DOI 10.17016/2380-7172.3462" | tokens |
| 7 | consistency_edit | end of file | (none) → corrections section (sources + 6 entries) | section audit |

### `addenda/gap_02.md` (3 changes; fix:main-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | consistency_edit | §2.1 levers table, pacing row | "G1's implied financing rate is ≈10.5–11% [I, G1]" → "unsupported G1 rate struck 2026-10-18; text recorded in corrections" | CMA2; tokens |
| 2 | missing_reference | sources, academic (Clopper–Pearson) | (no entry) → "Clopper & Pearson (1934), Biometrika 26(4), 404–413, DOI 10.1093/biomet/26.4.404" | SMA2; tokens |
| 3 | consistency_edit | end of file | (none) → corrections section (2 entries) | section audit |

### `addenda/gap_03.md` (4 changes; fix:main-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | §4 opportunistic templates, carry row | "[S: Koijen et al.]" → "[S: Koijen et al. 2018]" | grep |
| 2 | metadata | sources, other references (Koijen et al.) | pointer only → "Koijen, Moskowitz, Pedersen & Vrugt (2018), Carry, JFE 127(2), 197–225, DOI" | grep; tokens |
| 3 | recheck | sources, other references (Gatheral–Jacquier) | pointer only → "Gatheral & Jacquier (2014), Arbitrage-free SVI volatility surfaces, QF 14(1), 59–71, DOI" | tokens |
| 4 | consistency_edit | end of file | (none) → corrections section (3 entries) | section audit |

### `addenda/gap_04.md` (3 changes; fix:main-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | recheck | sources, Kritzman & Li (2010) | FAJ 66(5):30–41 → "+ DOI 10.2469/faj.v66.n5.3" | SMA5; tokens |
| 2 | recheck | sources, Kritzman, Li, Page & Rigobon (2011) | "JPM, Summer 2011" → "JPM 37(4):112–126, DOI 10.3905/jpm.2011.37.4.112" | tokens |
| 3 | consistency_edit | end of file | (none) → corrections section (2 entries + orphan note) | section audit |

### `addenda/gap_05.md` (15 changes; fix:main-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | usage | §4 lever priors, Secondaries row (Nadauld age splits) | "≈3pp for funds aged 4–9; ≈0 for tail-ends" → "+ [unverified: age splits from the 2016 WP; not re-checked vs JFE]" | grep |
| 2 | usage | §4 lever priors, Secondaries row (Boyer et al.) | "(w25207; JF 2023) ≈20% a year 2006–17, insignificant alpha" → "(JF 2023; 2021 w28691): ≈14% a year 2006–18 (22% ages 4–9); alpha ≈0" | SMA3; tokens |
| 3 | recheck | §4 lever priors, Capital Solutions row (Böni–Manigart) | "spreads wide earn more; funding-illiquidity works against" → "Table 5: ex-ante BB spreads → higher net multiples, beat bonds; IRR insignificant" | SMA4 |
| 4 | metadata | sources, Ennis (II, 1 Apr 2021) | II URL → "+ reports −1.87% for >$1bn over 12 years; probable source Ennis (2021) JPM [unverified]" | – |
| 5 | metadata | sources, Nadauld et al. | NBER link → "full entry, JFE 132(3):158–181, DOI; WP kept" | tokens |
| 6 | metadata | sources, Boyer et al. | w25207 link → "Boyer, Nadauld, Vorkink & Weisbach (2023), JF 78(2):835–885, DOI" | tokens |
| 7 | metadata | sources, Lerner, Mao, Schoar & Zhang | NBER link → "(2022) JFE 143(1):359–380, DOI" | tokens |
| 8 | metadata | sources, Brown et al. | NBER link → "(2021) JFE 139(2):561–577, DOI" | tokens |
| 9 | metadata | sources, Begenau & Siriwardane | forum link → "(2024) JF 79(2):1199–1247, DOI" | tokens |
| 10 | recheck | sources, Erel, Flanagan & Weisbach | NBER link → "(March 2024), DOI 10.3386/w32278; April 2026 draft noted" | tokens |
| 11 | recheck | sources, Böni & Manigart | CFA link → "(2022) FAJ 78(4):121–144, DOI 10.1080/0015198X.2022.2092384" | tokens |
| 12 | metadata | sources, Ben-David, Birru & Rossi | NBER link → "(2026) RCFS 15(3):704–747, DOI" | tokens |
| 13 | metadata | sources, Harvey & Liu (2015) | PDF → "JPM 42(1), DOI 10.3905/jpm.2015.42.1.013" | tokens |
| 14 | metadata | sources, Bailey & López de Prado (2014) | PDF → "JPM 40(5), DOI 10.3905/jpm.2014.40.5.094" | tokens |
| 15 | consistency_edit | end of file | (none) → corrections section (11 entries) | section audit |

### `groups/addenda/gap_04.md` (9 changes; fix:group-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | barrier_rerun | §1.1 cohort-engine table, co-investment row, l.53 | "Write-off below 0.85 × debt" → "+ tested on quarter-end values with no discrete-monitoring correction" | B18 |
| 2 | barrier_rerun | §1.2 couplings, company-overlap bullet, l.69 | "A write-off defaults the same company's PC loan" → "+ overlap defaults understated until the next re-run" | B19 |
| 3 | barrier_rerun | §9 limitations, new last bullet, l.319 | (none) → "uncorrected co-investment write-off barrier (g04_engine.py line 978); equivalent ≈0.92D" | B20 |
| 4 | usage | §1.3 discount anchors, l.80 | "54% in 2009 [S: Nadauld et al. 2019]" → "[S: Nadauld et al., NBER WP 22404 (2016) broker sample]" | SGA1 |
| 5 | metadata | sources, market data, Nadauld et al., l.328 | "(2019), JFE 132(3)" → "full entry with title, pages and DOI; WP" | – |
| 6 | metadata | sources, market data, Kaplan & Strömberg, l.332 | "(2009), via G4" → "Leveraged Buyouts and Private Equity, JEP 23(1), 121–146, DOI 10.1257/jep.23.1.121" | tokens |
| 7 | missing_reference | sources, literature, new BGK entry, l.341 | (none) → "Broadie, Glasserman & Kou (1997), MF 7(4), 325–349, DOI 10.1111/1467-9965.00035" | tokens |
| 8 | barrier_rerun | sources, internal, l.349 | (none) → "+ G4_barrier_rerun/RESULTS.md §1 and §6.3" | B21 |
| 9 | consistency_edit | end of file, ll.351–364 | (none) → corrections section (7 lines + 'checked, no change') | section audit |

### `groups/addenda/gap_03.md` (2 changes; fix:group-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | metadata | sources, literature, Rampini, Sufi & Viswanathan, l.326 | Consensus link → "Dynamic risk management, JFE 111(2), 271–296, DOI 10.1016/j.jfineco.2013.10.003" | SGA3; tokens |
| 2 | consistency_edit | end of file | (none) → corrections section (1 change + 'checked, no change') | section audit |

### `groups/addenda/gap_01.md` (2 changes; fix:group-addenda)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | missing_reference | sources, 'cited via gap_02', l.363 | (no Clopper–Pearson entry) → "Clopper & Pearson (1934), Biometrika 26(4), 404–413, DOI 10.1093/biomet/26.4.404" | SGA2; tokens |
| 2 | consistency_edit | end of file | (none) → corrections section (1 change + 'checked, no change') | section audit |

### `00_SYNTHESIS.md` (81 changes; fix:main-synthesis)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | consistency_edit | §1 top-12 finding 5, l.114–119 | "the 24-month named stress cannot be met as written; a calibrated version can" → "Survival in the joint stress binds; committed liquidity and the mandate clear it (groups gap_01 §5)" | CMS1 |
| 2 | consistency_edit | §2.3(d) table and lead-in, l.314–330 | "what each reading needs" table → groups gap_01 §1.2 T4′ survival ladder (SH_TP / SH_TPF) | CMS2; read |
| 3 | consistency_edit | §4.9 Tier 1A row T2, l.1184 | "8% elastic, 4% hard …" → "+ penalty M^IG; P2S cash net of stressed IM and P99 30-day VM; v1.0 fails at t0 by $0.56bn" | CMS3 |
| 4 | consistency_edit | §4.9 Tier 1A row T4′, l.1186 | "s*(θ*) with θ* = 0.76 …" → canonical conventions (equity −37.6%; distributions at 10.8% of drought; calls ×1.38; 23 crisis months …); θ* 0.76 / 0.79 pooled; SH_TPF ≥ 24 months | CMS4; read |
| 5 | consistency_edit | §4.9 Tier 1A row T6, l.1188 | bands by model class → "0.5/1/2% for M1–M5 and the mixture; 2.5/5% for M6-class; capacity breach triggers RECOVERY" | CMS5 |
| 6 | consistency_edit | §4.9, after the Tier 1A table, l.1193 | (none) → "Recovery mode (groups gap_01 §5): group-tagged Phase I; prices only from Phase II" | CMS6 |
| 7 | consistency_edit | §6.2 lead paragraph, l.1624 | "AI Validator … which only flags" → "+ (apart from the mechanical pack check below)" | CMS7 |
| 8 | consistency_edit | §6.2, after the seat bullets, l.1645–1661 | (none) → recovery-mode evidence-slice table (CIO, CRO, Treasurer/CF, group heads; glide share φ_g) | CMS8 |
| 9 | consistency_edit | §4.5 limit 6, l.927 | "ADIC-LCR(30d) is 2.10x" → "1.91x on CF-controlled HQLA (2.10x counts assets outside its control)" | CMS9 |
| 10 | consistency_edit | §4.9 Tier 1A row T3, l.1185 | "2.10x with Basel caps" → "1.91x on CF-controlled HQLA, which is Amber" | CMS10 |
| 11 | consistency_edit | §4.9 ladder row LR1, l.1218 | (no figure) → "+ synthetic book at 1.91x (Amber); 2.10x counts assets outside CF control" | CMS11 |
| 12 | consistency_edit | §6.7 state panel, light 9, l.1766 | "ADIC-LCR(30d) 2.10x" → "1.91x on CF-controlled HQLA (Amber)" | CMS12 |
| 13 | consistency_edit | §7.1 hedge-fund liquidity row, l.1815 | "2.10x" → "1.91x on CF-controlled HQLA (2.10x in total); GC2" | CMS13 |
| 14 | consistency_edit | §9.1 group-layer corrections, G7, l.1892 | "2.10x, not 4.5x" → "1.91x on CF-controlled HQLA (2.10x in total), not 4.5x" | CMS14 |
| 15 | consistency_edit | §4.9 CFP stages, Amber row, l.1230 | "…; NAV-facility documents activated; …" → removed (groups gap_01: drop the NAV facility) | grep |
| 16 | consistency_edit | §4.11 Shapley bullet, l.1320 | "exact over ≤ 6 action groups; permutation sampling otherwise" → "exact over all coalitions when each is a policy simulation (9 players, 512 coalitions, 54 min on 22 cores)" | CMS16 |
| 17 | barrier_rerun | §1 finding 8, l.132 | "lifts drought wipe-out from 7.0% to 22.8% [C]" → "at exit … [re-checked: an at-exit statistic, unaffected by the fix]" | B22 |
| 18 | barrier_rerun | §4.4 instrument table, co-investment REFI/LEVER, l.854 | "wipe-out 7.0% → 22.8%; 50–63% of quarterly-tested paths" → "at exit (7.6% → 22.9% with the E3 barrier); a quarterly covenant needs no shift" | B23 |
| 19 | barrier_rerun | §4.2 three-engine table, single-company engine, l.716 | "write-off at V ≤ κD" → "monitored continuously; a quarterly simulation tests κD·e^{+0.5826σ√Δ}" | B24 |
| 20 | usage | §4.12 readings, l.1363 | "between Ennis's −1.87pp … and NZ Super's +1.5pp" → "+ Ennis's figure: endowments >$1bn, 12 years to June 2020, as reported by II; primary source unverified" | SMS1 |
| 21 | usage | §6.4 decision capture, l.1694 | "transcripts restricted, because transparency can chill dissent [S]" → "restriction is an ADIC design trade-off [I]; HMP show discipline and conformity effects" | – |
| 22 | usage | §6.6 safeguards, l.1724 | "one seeded-error drill per Tier-A meeting" → "+ drills measure automation bias; they do not prevent it (P&M 2010)" | SMS2 |
| 23 | usage | §5.4 sealed plane, l.1551 | "deflation hurdle ≈3.47σ at N = 200 [C]" → "+ DSR also corrects for non-normality; the gate includes that term" | SMS3 |
| 24 | usage | §3 L12 disciplines, l.554 | "specification gaming" → "+ (Krakovna et al.; Skalse et al. 2022; Pan et al. 2022)" | SMS4 |
| 25 | metadata | §3 L11 evidence, l.550 | "Meucci (2008) not fetched [U]" → "confirmed via its arXiv record (1012.2848) and RePEc" | – |
| 26 | metadata | §11 sequential decisions, Luxenberg et al. | arXiv → "five authors; ICAIF '22, 249–256, DOI 10.1145/3533271.3561769" | tokens |
| 27 | metadata | §11 sequential decisions, Brandt et al. | short title, NBER → full title; RFS 18(3):831–873, DOI 10.1093/rfs/hhi019 | tokens |
| 28 | metadata | §11 sequential decisions, Udell & Boyd | arXiv → "COAP 64(2):355–378, DOI 10.1007/s10589-015-9819-4" | tokens |
| 29 | metadata | §11 scenarios, Shu, Yu & Mulvey | arXiv → "Downside risk reduction using regime-switching signals…, JAM 25(5):493–507, DOI" | tokens |
| 30 | metadata | §11 scenarios, Meucci (2008) | "[U] SSRN" → "Fully flexible views: theory and practice, Risk 21(10):97–102; arXiv" | grep; tokens |
| 31 | metadata | §11 scenarios, Mohajerin Esfahani & Kuhn | short → full title; MP 171(1–2):115–166, DOI | tokens |
| 32 | recheck | §11 scenarios, Smith & Winkler | short, RePEc → full title; MS 52(3):311–322, DOI 10.1287/mnsc.1050.0451 | tokens |
| 33 | recheck | §11 objectives, Föllmer & Leukert (1999) | RePEc → "F&S 3(3):251–273, DOI 10.1007/s007800050062" | tokens |
| 34 | recheck | §11 objectives, Föllmer & Leukert (2000) | author pdf → "F&S 4(2):117–146, DOI 10.1007/s007800050008" | tokens |
| 35 | metadata | §11 objectives, Busseti, Ryu & Boyd | arXiv → "J. Investing 25(3):118–134, DOI" | tokens |
| 36 | metadata | §11 private markets, Brown, Ghysels & Gredil | short title → "'Nowcasting net asset values: the case of private equity', RFS 36(3):945–986" | tokens |
| 37 | metadata | §11 private markets, Brown, Gredil & Kaplan | NBER → "JFE 132(2):267–297, DOI" | tokens |
| 38 | metadata | §11 private markets, Nadauld et al. | NBER → full title; JFE 132(3):158–181, DOI | tokens |
| 39 | recheck | §11 private markets, Mack (1993) | short title → "Distribution-free calculation of the standard error of chain ladder reserve estimates, ASTIN 23(2):213–225" | tokens |
| 40 | inconsistency | §11 private markets, Bühlmann (1967) | DOI only → "4(3):199–207; DOI …8989 confirmed (…8023 is the 1969 sequel)" | SMS5; Crossref; tokens |
| 41 | recheck | §11 overlay, Gatheral & Jacquier | RePEc → "QF 14(1):59–71, DOI" | tokens |
| 42 | metadata | §11 overlay, Bailey & López de Prado (2014) | author pdf → full title; JPM 40(5), DOI | tokens |
| 43 | metadata | §11 overlay, Bailey, Borwein, López de Prado & Zhu | author pdf → "J. Comput. Finance 20(4) (online Sep 2016), DOI 10.21314/JCF.2016.322" | tokens |
| 44 | metadata | §11 agentic AI, Lu et al. (2026) | "The AI Scientist, Nature 651, Sakana link" → "Lu, Lu, Lange, Yamada, Hu, Foerster, Ha & Clune, Towards end-to-end automation of AI research, Nature 651(8107):914–919, DOI" | SMS6; tokens |
| 45 | metadata | §11 agentic AI, Krakovna et al. | "Specification gaming" → "+ (DeepMind blog post)" | – |
| 46 | recheck | §11 deliberation, Vaccaro, Almaatouq & Malone | short → full title; NHB 8(12):2293–2303, DOI | tokens |
| 47 | recheck | §11 deliberation, Fogliato et al. | short, arXiv → full author list and title; FAccT '22 | – |
| 48 | recheck | §11 deliberation, Hackenburg et al. | short → full author list; Science 390(6777) | tokens |
| 49 | recheck | §11 deliberation, Hansen, McMahon & Prat | short → "+ ': a computational linguistics approach', QJE 133(2):801–870" | tokens |
| 50 | recheck | §11 deliberation, Kahneman, Lovallo & Sibony (2019) | "MIT SMR" → "Spring 2019 (4 Mar 2019; Reprint 60314)" | – |
| 51 | recheck | §11 group layer, Cai & Haque | Fed URL → "+ DOI; recovery figures (Fig. 15) are KBRA DLD" | – |
| 52 | recheck | §11 state engine, Kritzman & Li (2010) | RePEc → "FAJ 66(5):30–41, DOI 10.2469/faj.v66.n5.3" | tokens |
| 53 | recheck | §11 state engine, Kritzman, Li, Page & Rigobon (2011) | State Street link → "JPM 37(4):112–126, DOI" | tokens |
| 54 | metadata | §11 return levers, Gupta & Van Nieuwerburgh | NBER w26514 → "(2021) JF 76(6):3255–3307, DOI 10.1111/jofi.13073" | tokens |
| 55 | metadata | §11 return levers, Begenau & Siriwardane | forum link → "JF 79(2):1199–1247, DOI" | tokens |
| 56 | metadata | §11 return levers, Lerner, Mao, Schoar & Zhang | NBER → "JFE 143(1):359–380, DOI" | tokens |
| 57 | metadata | §11 return levers, Boyer, Nadauld, Vorkink & Weisbach | NBER w25207 → "JF 78(2):835–885, DOI 10.1111/jofi.13202 (w28691; supersedes w25207)" | tokens |
| 58 | recheck | §11 return levers, Erel, Flanagan & Weisbach | NBER → "(March 2024), DOI; net alpha ≈0 confirmed (RAP −$0.001, t = −0.01)" | – |
| 59 | recheck | §11 return levers, Böni & Manigart | CFA link → "FAJ 78(4):121–144, DOI" | tokens |
| 60 | metadata | §11 return levers, Ben-David, Birru & Rossi | NBER → "(2026) RCFS 15(3):704–747, DOI" | tokens |
| 61 | metadata | §11 return levers, Harvey & Liu (2015) | Duke pdf → "JPM 42(1), DOI" | tokens |
| 62 | metadata | §11 return levers, Brown, Harris, Hu, Jenkinson, Kaplan & Robinson | NBER → "JFE 139(2):561–577, DOI" | tokens |
| 63 | metadata | §11 return levers, Ennis (II) | II URL → "+ reports −1.87% …; probable primary source [inference] Ennis (2021) JPM" | – |
| 64 | metadata | §11 'cited without a verified URL' header | header → "+ (DOIs added where the audit confirmed one)" | – |
| 65 | metadata | §11 list, Baumol & Fabian | "MS 11(1)" → "11(1):1–32, DOI 10.1287/mnsc.11.1.1" | tokens |
| 66 | metadata | §11 list, Scharfstein & Stein | "JF 55(6)" → "55(6):2537–2564, DOI" | tokens |
| 67 | metadata | §11 list, Jensen (2003) | "EFM" → "EFM 9(3):379–406, DOI" | tokens |
| 68 | metadata | §11 list, Schwartz & Smith | "MS 46(7)" → "46(7):893–911, DOI" | tokens |
| 69 | metadata | §11 list, Stulz (1982) | "JFE 10 [U]" → "Options on the minimum or the maximum of two risky assets, JFE 10(2):161–185, DOI; [U] removed" | tokens |
| 70 | metadata | §11 list, Dufresne (1990) | "Scand. Actuarial J." → "1990(1):39–79, DOI" | tokens |
| 71 | metadata | §11 list, Kydland & Prescott | "JPE" → full title; JPE 85(3):473–491, DOI | tokens |
| 72 | metadata | §11 list, Foster & Stine | "JRSS-B 70(2)" → "70(2):429–444, DOI" | tokens |
| 73 | metadata | §11 list, Glahn & Lowry | "J. Appl. Meteor. 11(8)" → "11(8):1203–1211, DOI" | tokens |
| 74 | metadata | §11 list, List & Pettit | "Econ. & Philos. 18(1)" → "18(1):89–110" | tokens |
| 75 | missing_reference | §11 private markets, new GLM entry | (none) → "Getmansky, Lo & Makarov (2004), JFE 74(3):529–609, DOI" | tokens |
| 76 | missing_reference | §11 private markets, new BGK entry | (none) → "Broadie, Glasserman & Kou (1997), MF 7(4):325–349, DOI" | tokens |
| 77 | missing_reference | §11 sequential decisions, new Clopper–Pearson entry | (none) → "Clopper & Pearson (1934), Biometrika 26(4):404–413, DOI" | tokens |
| 78 | missing_reference | §11 agentic AI, new Skalse et al.; Pan et al. | (none) → "Skalse et al. (2022) arXiv:2209.13085; Pan et al. (2022)" | – |
| 79 | missing_reference | §11 deliberation, new Parasuraman & Manzey | (none) → "P&M (2010), Human Factors 52(3):381–410, DOI" | tokens |
| 80 | missing_reference | §11 list, new de Finetti (1957) | (none) → "de Finetti (1957), Trans. XVth Int. Congress of Actuaries 2:433–443 [U: title not confirmed]" | SMS7; tokens |
| 81 | metadata | end of file, l.2288 on | (no change log) → corrections section (every change, sources, 'checked, no change' line) | section audit |

### `groups/01_GROUPS_SYNTHESIS.md` (34 changes; fix:group-synthesis)

| # | Kind | Location | Before → after | Verified |
|---|---|---|---|---|
| 1 | barrier_rerun | §1 finding 8, bullet 1, l.144 | "lifts drought wipe-out from 7.0% to 22.8%" → "at exit (7.6% → 22.9% if the G4 default barrier applies at any time)" | B25 |
| 2 | barrier_rerun | §1 finding 8, bullet 2, l.145 | "50–63% of quarterly-tested paths" → "+ (62–73% if LTV were monitored continuously)" | B26 |
| 3 | barrier_rerun | §1 finding 8, new bullet, l.146 | (none) → "Both rates stand after the Broadie–Glasserman–Kou sign correction" | B27 |
| 4 | usage | §3.1 PE table, risk and smoothing row, l.442 | "AC1 0.66–0.71 / BGG 2023 [S]" → "AC1 implied by BGG WP smoothing estimates (λ 0.951 a WP figure) [I-calc on S]" | SGS1 |
| 5 | metadata | §3.2 Secondaries table, PME gap row, l.476 | "Nadauld et al. 2019 [S]" → "NBER w22404 (2016) age-group tables; JFE abstract 1.023 vs 0.976" | SGS2 |
| 6 | metadata | §3.2 table, tail-end θ row, l.477 | "Nadauld's 82.2% tail-end price" → "+ (NBER w22404, Table 3)" | – |
| 7 | usage | §3.2 constraints, l.489 | "Boyer et al.'s β > 2 … never a hedge ratio [C]" → "+ [unverified against JF 2023: β > 2 is the 2018 WP figure]" | SGS3 |
| 8 | barrier_rerun | §3.4 spec table, model row, default clause, l.550 | "plus a barrier at V ≤ κD" → "monitored continuously; quarterly checks κD·e^{+0.5826σ√Δ}" | B28 |
| 9 | usage | §3.4 model row, recaps clause, l.550 | "multiplier 1.4–3.4 (central 2.0) [I]" → "≈×1.1 (OLS) to ×1.7 (IV) for recaps adding 25% debt" | SGS4 |
| 10 | barrier_rerun | §3.4 action table, REFINANCE row, l.568 | "49.6% / 62.5% [C]" → "+ 62.2% / 73.4% continuous; 54.6% / 67.0% monthly" | B29 |
| 11 | barrier_rerun | §3.4 action table, LEVER row, l.569 | "wipe-out 2.1% → 11.8% and 7.0% → 22.8% [C]" → "at exit; with the G4 barrier V ≤ 0.75D at any time 2.2% → 11.8%, 7.6% → 22.9%" | B30 |
| 12 | recheck | §4.5 'evidence is mixed', Böni–Manigart, l.918 | "positive spread effect with a TED effect > 2× persistence" → "Table 5: higher net multiples, beat bonds; IRR coefficient insignificant; TED lowers outcomes" | SGS5 |
| 13 | barrier_rerun | §4.9 limits, new bullet, l.1100 | (none) → "co-investment write-off barrier (V < 0.85D) checked quarterly with no BGK shift; equivalent ≈0.92D" | B31 |
| 14 | metadata | §8 calibration targets, tail-end row, l.1366 | "Nadauld et al." → "NBER w22404 Tables 3 and 6 (not re-checked vs JFE)" | – |
| 15 | inconsistency | §10 Albertus & Denes | "Private equity fund debt" → "full subtitle; NBER conference paper (26 May 2020); same as SSRN 3410076; JFQA 2026 probable successor" | SGS6 |
| 16 | metadata | §10 Bhardwaj, Gupta & Howell | "Dividend recapitalizations in PE" → "Capital structure & firm outcomes: evidence from dividend recapitalizations in private equity" | – |
| 17 | metadata | §10 Boyer, Nadauld, Vorkink & Weisbach | "(2018) PE indices from secondary transactions, NBER w25207" → "(2023) Discount-rate risk in private equity…, JF 78(2):835–885, DOI" | tokens |
| 18 | metadata | §10 Brown, Gredil & Kaplan | "JFE 132(2), NBER" → "132(2):267–297, DOI; NBER kept" | tokens |
| 19 | metadata | §10 Brown, Ghysels & Gredil | short title → full title; RFS 36(3):945–986 | tokens |
| 20 | metadata | §10 Lopez-de-Silanes, Phalippou & Gottschalg | short title → full title; JFQA 50(3):377–411, DOI | tokens |
| 21 | metadata | §10 Nadauld, Sensoy, Vorkink & Weisbach | short title → full title; JFE 132(3):158–181, DOI | tokens |
| 22 | recheck | §10 Böni & Manigart | short title → full title; FAJ 78(4):121–144, DOI | tokens |
| 23 | recheck | §10 Cai & Haque | Fed URL → "+ 23 Feb 2024, DOI; recovery figures are KBRA DLD" | – |
| 24 | recheck | §10 Erel, Flanagan & Weisbach | short title → full title; NBER w32278 (March 2024), with DOI | – |
| 25 | metadata | §10 Ben-David, Birru & Rossi | NBER → "+ RCFS 15(3):704–747 (2026), DOI" | tokens |
| 26 | metadata | §10 Brooks, Gould & Richardson | AQR link → "JFI 29(4):5–19, DOI" | tokens |
| 27 | metadata | §10 Getmansky, Lo & Makarov | short title → full title; JFE 74(3):529–609, DOI | tokens |
| 28 | usage | §10 Li, Strahan & Zhang | short title → "'…: evidence from the COVID-19 crisis', RCFS 9(3):472–500, DOI; abstract credits Fed programs and deposits" | SGS7; tokens |
| 29 | missing_reference | §10 new Clopper & Pearson (1934) | (none) → "Biometrika 26(4):404–413, DOI 10.1093/biomet/26.4.404" | SGS8; tokens |
| 30 | metadata | §10 Campbell & Sharpe | FEDS link → "FEDS 2007-12; published JFQA 44(2):369–390 (2009), DOI" | tokens |
| 31 | recheck | §10 Smith & Winkler | short title → full title; MS 52(3):311–322, DOI | tokens |
| 32 | metadata | §10 Bailey & López de Prado | short title → full title; JPM 40(5), DOI | tokens |
| 33 | metadata | §10 closing note, Fissler & Ziegel | "cited without a verified URL … [U]" → "verified in the G8 review: Higher order elicitability and Osband's principle, AoS 44(4)" | tokens |
| 34 | consistency_edit | end of file | (none) → corrections section (30 lines) | section audit |

## 4. Skipped items, with the editors' reasons

Condensed from the 29 editor reports. Recurring reasons: the item concerns a work the file does not cite (checked by grep); the item is a design recommendation or a verification-log finding rather than a §2 citation correction; the source could not be reached (paywall, HTTP 403/429), in which case the original was kept and marked [unverified]; or the file was outside the editor's list.

### fix:01 (12 items)

| Skipped item | Reason |
|---|---|
| Relayed user request: add a Real Assets group | Outside this step (citation corrections to two stream-01 files); flagged for the orchestrator. |
| G4 barrier re-run values | None quoted in either 01 file (grep). |
| §2.6 #1 Giommetti second author | The 'Jørgensen' occurrence is in literature/01_mpo.lit.md, outside the edit list; the 01 files do not cite Giommetti. |
| §2.5 'write Mohajerin Esfahani' | Already correct in stream 01. |
| Cao & van Beek first author ('Wenbo' vs 'Wen') | Crossref lists 'Wen Cao', matching the files; no change. FAJ 81(3):60–75 pages not added. |
| ICAIF '22 five-author open note in the verification log | Resolved in dossier ref 49; the log may carry only one erratum line. |
| DOI-only additions to entries already correct (Boyd 2017/2014, Nystrup, Powell 2019, Pereira–Pinto, etc.) | Not requested for stream 01; left unchanged. |
| Fixes found only in the verification log (Kozmík vol., Zou vol., Valladão pp., SDDP.jl '30% slower', Gondzio–Grothey title, Towers Perrin, Luxenberg calibration, Boyd timings, Dulac-Arnold, Powell 'belief', R1, R2, R4–R15) | Not among this pass's correction sources; left for the dossier owner. |
| §2.5 'N ≳ (2/ε)(d+ln(1/β))' constant quoted from memory | Not a listed correction; arithmetic confirmed (984.2; 60,184.2); now cited only as the looser condition. |
| Stream-10 values 447 / 986 / 2,658 / 4,970 | Not in stream 01; the same correction was applied to 01's own values (631; 31,785). |
| Topic-11 re-check: add β = 10⁻⁶ | Not applicable: 01 states β = 1%. |
| Re-check works for topics 10, G3, 14, 11, 13; §2.2–§2.4 and §2.6 items for other streams | Not cited in either 01 file (grep). |

### fix:02 (12 items)

| Skipped item | Reason |
|---|---|
| G4 barrier re-run values | None in 02 files ('barrier' = de Finetti dividend barrier; the only 62.5% is NACUBO's alternatives share). |
| Re-check topics 10, G3, 14, 11, 13 | None of these works is cited in the 02 files. |
| §2.4 usage errors; §2.5 hygiene; §2.6 items | None concern 02 (the 06 Brown et al. AER item already holds in 02). |
| §2.2 items for other streams | Not applicable, except Merton (1993), which 02 also cites and which was completed. |
| Dufresne (1988): 'Moments' vs 'Movements' | Unresolved: Crossref and OpenAlex read 'Movements'; citing references read 'Moments'; Cambridge 403. Kept 'Moments' with an [unverified] note. |
| Attribution of −1.87% to Ennis (2021b) | Only partly verifiable (no abstract; II coverage names no paper); marked [unverified]. |
| de Finetti (1957) original | Not in Crossref; OpenAlex 429; title/venue/pages from Loeffen (2008) ref 8; marked [unverified]. |
| Found rows needing no correction (Tobin, Gilbert & Hrdlicka, Campbell 2012, Cejnek et al., Filbeck & Bok) | Unchanged; Cejnek's JOIM pages remain unconfirmed. |
| Orphan status of Constantinides (1990) and Kydland & Prescott (1977) | Not flagged by the audit; metadata only. |
| Lit-review design suggestions (S54 Kleinow et al.; challenges C1–C8) | Design input, not citation corrections. |
| Verification-log erratum | Not needed; the log accepted nothing wrongly. |
| Relayed Real Assets request | Separate step; no conflict. |

### fix:03 (14 items)

| Skipped item | Reason |
|---|---|
| Re-check of hedging demand 0.01–0.07pp, 1976–2016 sample and sign against IREF 2020 | Could not be done (no abstract or open copy; ScienceDirect 403); figures stay sourced to WP 1172 and tagged [unverified]. |
| Valencia blog 'cite that instead' | Companion WP added, blog kept: the §4.8 figures are verbatim in the blog; the WP reports different quantities. |
| G4 barrier re-run values | None in 03 files. |
| §2.4 usage errors and §2.5 hygiene | No item names stream 03. |
| §2.6 cross-file items | None cited in 03 files. |
| Re-check works (10 other than Hamilton, Rockafellar–Uryasev, O'Hagan; G3; 14; 11; 13) | Not cited; the 'Sakana-style pipeline' mention has no reference entry. |
| §7 QuantLib/Stulz [U] tag | Left: §7 tags mark tool claims. |
| Stulz (1982) full-title note | The dossier gives no title; DOI added only. |
| Robinson & Sensoy (2016) pages | Flagged only by the verification log; unchanged. |
| Other 'found' rows in the 03 lit table | No correction directed; DOIs not added. |
| Borensztein–Jeanne–Sandri JDE 2013 | Kept [U] per the lit table. |
| Refs 1, 2, 7 'verified via item 6' | Unchanged (item 6 still lists WP 1172). |
| Rosen et al. (2019) and other challenge papers | Literature challenges, not citation corrections. |
| Relayed Real Assets request | Not applicable to a topic dossier without a group list. |

### fix:04 (16 items)

| Skipped item | Reason |
|---|---|
| G4 barrier re-run values | None in 04 files. |
| Re-check topics 10, 14, 11, 13 | Not cited in 04 files. |
| G3 re-check: Mack (1993) | Already exactly right; recorded 'checked, no change'. |
| G3 re-check: Kaplan & Strömberg and other works | 04 cites the 2009 JEP paper, a different work; the others are not cited. |
| §2.2 #3 Ljungqvist & Richardson; #4 Getmansky, Lo & Makarov | Already cited correctly. |
| §2.6 #1 Giommetti | Confirmed Morten Sørensen via Crossref and OpenAlex; 04 is correct; the 'Jørgensen' variant is in lit files 01, 06, 11 (outside the edit list). |
| §2.6 #2 Bühlmann DOI | …8989 is the 1967 paper; the conflicting DOI is in stream 07. |
| §2.6 #5 Gredil, Liu & Sensoy | '2–8%' appears only in literature/04_pe_cashflows.lit.md §4.5, outside the edit list. |
| §2.6 #3 Albertus & Denes | Not cited in 04 files. |
| §2.4 #8 HJK figures | Not quoted in 04 (the BGG part was applied). |
| §2.4 other streams and §2.5 | None names 04; Axelson et al. (2013) already correct. |
| Verification-log erratum for Nadauld | Not needed: the log checked the WP abstract (0.974), correct for that version. |
| Tausch, Buchner & Schlüchtermann (2022) volume/issue/pages | [unverified]: absent from Crossref and OpenAlex; risk.net blocked; left out. |
| de Malherbe (2007) §10 entry | [unverified]: not found on Crossref; mentioned in §8 only. |
| Lit-file backfill and parameter challenges | Design suggestions, out of scope. |
| SSRN precursor DOIs for Jeet (2024) | Not needed; published title and DOI confirmed directly. |

### fix:05 (12 items)

| Skipped item | Reason |
|---|---|
| Relayed Real Assets request | Outside this step. |
| 05 verification log (whole file) | No change needed; no erratum allowed; its entries agree with the audit. |
| §2.6 #1 Giommetti; #3 Albertus & Denes | Not cited in 05 files (appear only in the 05 lit file). |
| §2.6 #2, #4, #5 | Not cited. |
| G4 barrier re-run values | None in 05 files; 05's covenant constraint is tested at reporting dates, so no shift applies. |
| §2.2; §2.3 other streams; §2.4 other than #5; §2.5 | None concern 05 (Nadauld pages fix applied to ref 14). |
| Re-check topics 10, G3, 14, 11, 13 | Not cited ('Hamilton Lane' is the adviser, not Hamilton 1989). |
| Albuquerque et al. verbatim abstract | Could not be fetched (SSRN 403; no abstract indexed); tagged 'full text not read'. |
| Ref 16 'Cass Business School' affiliation | Not a listed correction; still unverified. |
| §2.3 Bollen–Sensoy 3-D lattice | Not flagged; WP vs published location unchecked. |
| WilmerHale 'could not be given away' wording (verification F8) | Not a correction source; text layer confirms it is a forecast. |
| G2 dossier l.216 unidentified '[S: Evercore/HEC]' | Outside the edit list; fixable the same way by its owner. |

### fix:06 (14 items)

| Skipped item | Reason |
|---|---|
| 06 verification log (whole file) | No listed correction applies; no erratum warranted (Haircuts note, Kelly caveat and Brown et al. checks hold). |
| BGK barrier re-run | None of the values appears; constraint 7 is tested on quarter-end NAV; the §6.9D stylized MC is not covered by the re-run. |
| Re-checks 10, 11, 13, 14, G3 | Not cited; the §7 'a few thousand scenarios' statement is consistent with Calafiore–Campi's looser bound (exact minima 418 / 577 / 935), so unchanged. |
| Topic-10 DOI additions | They cover dossier 10's list; only Getmansky–Lo–Makarov applies to 06 (added). |
| §2.6 #1 Giommetti | 'Jørgensen' is in 06_leverage.lit.md, outside the edit list. |
| §2.6 #2–#5 | Not cited. |
| §2.4 #14 Gorton–Metrick bilateral vs tri-party | Assigned to G7; 06 §6.5 unchanged. |
| §2.5 Gorton–Metrick '45–50% for structured collateral' | Verification-log finding (claim #27), not a listed source. |
| §6.12 'Sakana's verification layer' mention | Not flagged for 06. |
| Mayne et al. (2005); Dowson & Kapelevich (2021) | Left 'not checked' by the audit. |
| Dufresne (1990) pages; Adrian & Shin (2010) volume/pages | Not listed as fixes. |
| Stafford (2022) year | Kept 2022 (volume year); 'online 2021' noted. |
| Audit note that NBER w15861 is titled 'Why I Lost My Secretary' | Partly outdated; the AER DOI fix was still applied. |
| Relayed Real Assets request | No group list in 06 files. |

### fix:07 (13 items)

| Skipped item | Reason |
|---|---|
| BGK barrier re-run | Not applicable. |
| §2.4 usage errors | None concern 07. |
| §2.6 items 1, 3, 4, 5 | Not cited. |
| Re-checks for topics 10 (other than Smith & Winkler), G3, 14, 11, 13 | Not cited; 07's Mack (2000) is a different work. |
| '320 experts' (Cooke studies) | Could not confirm (not in the Colson & Cooke abstract); kept, marked [unverified]. |
| MOS dates 1965 / 1968 | Could not confirm (no dates in the abstract; AMS 403); kept, marked [unverified]. |
| Blanc & Setzer (2020) orphan | No fix prescribed; dagger removed only. |
| Remaining daggers (Black–Litterman, Bühlmann–Straub, Quarg & Mack, Takahashi & Alexander, Powell & Ryzhov, Meucci 2008, Efron & Morris, Timmermann pages, Andonov & Rauh, Guler, Shefrin & Statman, Tetlock, Mellers et al., CUSUM values, BL Ω) | Unchecked by the audit, or the lit file says keep the dagger. |
| Meucci (2008) arXiv link | §2.4 #13 targets stream 10. |
| DOIs for other works whose dagger was removed | Not requested. |
| Verification-log tally and §1/§8 summary counts | One erratum line allowed; the corrected tally is in that line. |
| Lit-file backfill and design challenges (Noh et al. 2023; GLS shrinkage; R1–R15; Jefferies H1 2026) | Out of scope. |
| Relayed Real Assets request | Separate step. |

### fix:08 (9 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in 08 files. Owner note: §2.4/§6.12 'P(LTV > 40% at any point) = 0.7%' is checked at 5 annual points only. |
| §2.6 #5 Gredil '2–8%' | In the 08 lit file §4.3, not in the dossier or log. |
| Re-checks 10, G3, 14, 11, 13 | Not cited. |
| §2.2, §2.4, §2.5 | No stream-08 items (the one §2.3 mismatch was applied). |
| Myers & Majd (1990) publication details | Could not confirm (no Crossref record; OpenAlex 429); marked [unverified]; the 1983 MIT WP was confirmed. |
| Ang et al. quote spelling ('forego' vs 'forgo') | Cosmetic; unchanged. |
| Optional suggestions in the 08 lit file | Design suggestions or [Inference] notes. |
| Further verification-log status updates | Not errata; recorded in the dossier. |
| Relayed Real Assets request | No group list in 08. |

### fix:09 (12 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in 09 files; the §7 discrete-monitoring remark already points the right way. |
| Topic-10 re-check: Carr & Wu 'calm regimes' tag | 09 makes no calm-regime claim; DOI and pages applied. |
| Topic-10 re-check: other works | Not cited (09's Buehler 2018 and Mohajerin Esfahani & Kuhn 2018 are different or already correct). |
| Re-checks G3, 14, 11, 13 | Not cited (Browne 1997 is not 09's Browne 1999). |
| §2.2 / §2.3 / §2.6 | 09 has 0 not found and 0 mismatched; §2.6 works not cited. |
| §2.5 'resolves 01's open venue' | Concerns 01's files. |
| 09 lit-file flag 3 (BTZ predictability contested) | Not in §2.4; challenging work unconfirmed; BTZ sentence unchanged. |
| Lit-file design recommendations | Out of scope. |
| DOIs for other sourced references (refs 1, 2, 4, 6, 8, 9, 13–19) | No correction listed. |
| Verification-log erratum | Not needed. |
| Cederburg et al. (2020) and Barroso & Detzel (2021) abstracts | Not re-read (no abstracts; SSRN 403); findings from the 09 lit review; metadata Crossref-confirmed. |
| Jeanne & Rancière (2011) 9.1% | Confirmed only via Mihailov & Nasir (2022); marked [unverified]; WP 10.1% kept. |

### fix:10 (12 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in 10 files. |
| Re-checks G3, 14, 11, 13 | Not cited. |
| Topic-11 Campi & Garatti precision item | Targets dossier 11; 10 already states β = 10⁻³ and credits Campi & Garatti. |
| §2.2; §2.4 other items; §2.5; §2.6 | No stream-10 items. |
| Lange et al. (2026) DOI | None exists yet; arXiv-only entry kept. |
| Meucci (2012) venue, pages, DOI | Could not be confirmed (Crossref none; SSRN DOI 404; OpenAlex 429); marked [unverified]. |
| Carr & Wu: sign of the average VRP | Left as the re-check gives it, [unverified: secondary literature]. |
| Heitsch & Römisch (2009) companion paper | Not required by the correction sources. |
| Smith & Winkler subtitle in 07 and 12 | Outside the edit list (applied by those editors). |
| Verification-log rows, tally and claim-#16 verdict | One erratum line only; rows kept as history. |
| Lit-review backfill and challenges | Out of scope. |
| Verification-log analytic edits (R1–R8, R10–R12, SDDP part of R9) | Not citation corrections. |

### fix:11 (12 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in 11 files ('barrier' = de Finetti payout barrier and control barrier functions). |
| §2.6 #1 Giommetti | Only in the 11 lit file, outside the edit list. |
| §2.6 #2–5; §2.2; §2.3 other streams; §2.4 | None apply (Glasserman & Xu is not quoted in 11). |
| Topic-10 re-check: Smith & Winkler subtitle; Lange et al. usage | 11 has no S&W entry; the Lange wording is in dossier 10. |
| Topic-10 re-check: Campi–Garatti values of stream 10 | 11's own values recomputed as exact minima at β = 10⁻⁶. |
| Other topic-10, G3, 14, 13 re-check works | Not cited. |
| Topic-11 re-check: Fishburn (1977), Ruszczyński (2010) | Verdict ok; no change (Fishburn has no Crossref DOI). |
| Topic-11 re-check note 3 (P(10%) most risk-seeking) | Reasoning item R12, not a citation issue. |
| Brown et al. (2014) subtitle | Not flagged; short title acceptable. |
| Design recommendations (shortfall exponent > 1, etc.) | Out of scope. |
| Verification-log content findings (J.P. Morgan returns, Yale rule, CPP caveat, R1–R15) | Not correction sources. |
| Remaining ⚠ entries (Cvitanić & Karatzas 1995; Brunel) | No metadata source; stay flagged as not relied upon. |

### fix:12 (12 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in 12 files. |
| §2.2 #8 Lange et al.; #9 Song | Confirmed; no change. |
| §2.5 and §2.6 | None concern 12. |
| Re-check works not cited (topic 10 others, G3, 14, 11, 13) | Nothing to apply. |
| Verification-log corrections outside the sources (#1, #3, #4, #5, #6, #8, #9; §5 design issues) | Left for the owner; #7 (FINSABER KDD 2026) applied. |
| Erratum for FINSABER 'often vanish' (F10) | Not added: the log was right (introduction wording). |
| Errata for gaps the log never raised (DSR, shrinkage, Kosmos) | One erratum line only. |
| Optional title/DOI completions for correct entries | Not flagged as corrections. |
| Ref 74 pages and print year | Not added (OpenAlex has no pages; Crossref 429). Pages 39–69 are now confirmed on the publisher page; see open items. |
| Beel et al. DOI typo in 12_agentic_ai.lit.md (…376974) | Lit file outside scope; the dossier uses Crossref's 10.1145/3769733.3769747. |
| §7 table row with LaTeX pipes | Pre-existing; not touched. |
| Relayed Real Assets request | Outside this step. |

### fix:13 (14 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in 13 files. |
| Topic-10 re-check items | Not cited; Lange usage already correct; S&W subtitle present (pages and DOI added). |
| G3, 14, 11 re-check works | Not cited. |
| Topic-13 re-check: Klein (2007) | Ok; no change. |
| §2.2 #10 Agentic Scientist | Confirmed; no change. |
| §2.3–§2.5 other streams; §2.6 | None concern 13. |
| 13 lit flags 4, 5, 6 (Dwork iid holdout; Hyperband rankings; S&W remedy) | Design inferences, not citation errors. |
| 13 lit recommendations (a)–(h) and backfill papers | Out of scope. |
| Zheng et al. (2023); Lu et al. (2024) | Found; unchanged. |
| Bailey et al. (2017) page range | Not added (no pages in Crossref/OpenAlex). Pages 39–69 are now confirmed on the publisher page; see open items. |
| Kwa et al. and Gottweis et al. full author lists | Kept 'et al.'. |
| Verification-log erratum | Not needed; two rows annotated instead. |
| Verification log's own non-citation findings | Not correction sources. |
| Relayed Real Assets request | Nothing in scope. |

### fix:14 (13 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in 14 files. |
| Topic-10 re-check items | Not cited; Lange usage n/a; initials applied. |
| G3 and 11 re-checks | Not cited. |
| Topic-13 re-check (Alshiekh; KLS 2011; MAP pre-votes) | Not cited or claim not made; KLS 2019 caveat applied. |
| §2.4 #10: cite Wang et al. as arXiv v3 | Superseded: Crossref confirms NMI 7(3):400–411 (re-confirmed in this verification). |
| §2.2, §2.3, other §2.4 items, §2.5, §2.6 items 1, 3, 4, 5 | None concern 14. |
| Tessler majority-drift nuance | 'A nuance, not an error'; only the N-scope fix applied. |
| Verification-log findings not carried by the audit (A1, A5, A10, (nr) upgrades, R1–R17) | Left for the owner. |
| Michael et al. consultancy caveat in §2.5 | Re-check asked for §1 only. |
| Smit et al. effect on the §3 default; lit §5 challenges | Design responses. |
| Stasser & Titus (1987) as formula source | Unconfirmed; formula flagged [unverified]. |
| Khan et al. PMLR pages; Schoenegger et al. journal version | Not instructed. |
| Relayed Real Assets request | No group roster in 14 files. |

### fix:G1 (14 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in G1 files; '[S: BGK]' in §6.9 means Brown, Gredil & Kaplan (suggest spelling it out). |
| Re-checks 10, G3, 14, 11, 13 | Not cited ('optimizer's curse' named without a citation). |
| §2.2, §2.3 | No G1 entries; the stream-04 items behind G1's 'via Stream' line were applied. |
| §2.4 items 1–16 | None concerns a work G1 cites; §6.12 'Treasury payout and calls' left (not a citation). |
| §2.5 'Metrick & Yasuda is verified' | Not cited in G1. |
| §2.6 items 1, 2, 4, 5 | Not cited (Bühlmann–Straub named only as a method). |
| Lerner–Mao–Schoar–Zhang figures vs JFE 2022 | Could not confirm (no abstract; ScienceDirect 403); WP stays the source, marked [unverified]. |
| Albertus & Denes JFQA 2026 content | Metadata confirmed; content unverified (no abstract; Cambridge 403). |
| Phalippou (2009) DOI | Already in the URL. |
| Lit-table additions that are not errors | Unchanged. |
| Outstanding verification-log corrections (S12, S15, S16, A2, R1–R10) | Not correction sources. |
| Brown et al. quote wording ('modest at best') | Not flagged; minor follow-up. |
| Annotating verify-log rows already applied | Bookkeeping only; recorded in the dossier. |
| Relayed Real Assets request | Outside this step. |

### fix:G2 (13 items)

| Skipped item | Reason |
|---|---|
| Relayed Real Assets request | Outside this step. |
| BGK barrier re-run values | None in G2 files. |
| Re-checks 10, 11, 13, 14, G3; §2.6 items | Not cited. |
| Erratum line in the G2 log | The audit agrees with the log; annotations instead. |
| Boyer et al. β against the JF 2023 full text | Paywalled; WP 28691 used; edits say 'JF full text not accessed'. |
| 60bp / 75bp at Rode et al.'s primary source | No fetchable download; re-attributed to the CFA report's own example, marked [unverified]. |
| Nadauld age-group figures vs JFE tables | Not accessed; labelled as WP 22404 figures. |
| G2 lit §4–5 design recommendations | Out of scope. |
| Harris, Jenkinson, Kaplan & Stucke FoF claim | Not listed as a correction. |
| 'cash-flow β 1.05–1.25 [S, stream 04]' | Inherited from stream 04; the BGG version issue was raised for 07 only. |
| Ref 36 (Wikipedia) and ref 30 DOI | Synthesis §2.5 covers 07 only. |
| Example E SACV μ/σ; log §1 item 5 (β ≈ 2) | R5 got a dated note; summary left as the verifier's conclusion. |
| Log header 'the dossier was not edited' | Describes the verification step. |

### fix:G3 (12 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in G3 files; covenant tests are simulated at their contractual frequency. |
| Re-checks 10, 14, 11, 13 | Not cited. |
| §2.6 #3 Albertus & Denes; #1; #5 | Not cited in the G3 dossier or log. |
| §2.6 #2 Bühlmann, stream-07 side | G3 side applied; the 07 file was outside this list (fixed by the 07 editor). |
| Merton (1974) optional precision | Not in the correction list. |
| EFW April 2026 draft figures | Kept the March 2024 version per the re-check; version note added. |
| Kaplan & Schoar (ref 52) | Withdrawn rather than newly cited (a new claim would be unchecked). |
| Black–Cox 'first-passage barrier represents covenants' | Could not be confirmed; marked [unverified]. |
| Mack: whether Mack (1993) is the intended work | Surname only; added with [I]. |
| Verification-log findings not tied to cited sources (A1, A2, A4, A16, R1–R4, R6–R18) | Out of scope (A3 and R5 applied). |
| Pre-existing table defect, §6.8 'Group forecast' row | Unescaped pipe; not touched (confirmed pre-existing by this verification). |
| Relayed Real Assets request | Outside this step. |

### fix:G4 (14 items)

| Skipped item | Reason |
|---|---|
| Relayed Real Assets request | Outside this step. |
| §2.2, §2.3 items | No G4 items (LMSZ already cited as JFE). |
| §2.4 items 4–16 | Other streams. |
| §2.5: Kou (E1) and Rockafellar–Uryasev without §10 entries | Not requested; Kou's journal metadata unconfirmed. |
| §2.6 #5 Gredil 'up to 5%' | Only in literature/G4_coinvest.lit.md, outside the edit list. |
| §2.6 #1–4 | Not cited. |
| REFI '29–37%' and LEVER '12% to 23%' | Not barrier statistics; still open under verification R2 and R3. |
| Quarterly LTV-breach figures in the verify summary and §5 table | Correct as quarterly-tested; continuous bounds added once (R2). |
| 3-year write-off counts and written-off cost share | Quoted only in the calc JSON. |
| Book-simulation cash flows | Unchanged at quoted precision. |
| Barrier quotes in other files (GC1, syntheses, gap_01, sufficiency audits, design brief, lit synthesis, gap_04 engine) | Not in the G4 list (GC1, syntheses and gap_01 handled by other editors; the rest still open). |
| Adding the shifted check to E3 / spec-card equation | Only the §7 pitfall was listed; E3 already defines continuous monitoring. |
| Re-checks 10, G3, 14, 11, 13 | Not cited (G4's Kaplan & Strömberg is the 2009 paper). |
| G4 lit §3–§5 design suggestions | Out of scope. |

### fix:G5 (12 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in G5 files. |
| Re-checks 10, G3, 14, 11, 13 | Not cited; 'Agentic Scientist pattern' and 'MAP-scorecard form' make no corrected claim. |
| §2.2, §2.4, §2.6 items 1, 2, 3, 5 | None concern G5. |
| Fung & Hsieh (2000) bias magnitudes | Not abstract-verified; stay [nrv]. |
| Cipriani et al. versions; Aggarwal & Jorion stray DOI; Grinold & Kahn | Informational or not applicable; unchanged. |
| Dimmock, Wang & Yang (2024) 'via 06' without a §10 entry | Not flagged by the audit. |
| Leland year in text | Unchanged; §10 notes the 2000 SSRN record. |
| Orphans (Getmansky, Lee & Lo; Kosowski et al.; Rattray et al.) | Not in the audit's orphan list; metadata completed. |
| Verification-log findings outside the audit (A34, F20, A23, R1–R11) | Out of scope; remain open. |
| Erratum line in the G5 log | Not needed. |
| Optional DOIs for other found references | Not flagged. |
| Real Assets cross-links (relayed request) | The §6.16 'Links to other groups' row does not yet mention Real Assets. |

### fix:G6 (14 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in G6. Owner note: §6.8D P(deficiency) uses quarterly borrowing-base tests (correct only if the facility tests quarterly). |
| §2.4 #4 / G3 re-check: Cai & Haque KBRA vs S&P | G6 never attributed the recoveries to S&P; DOI added. |
| G3 re-check: EFW GPME/RAP label and April 2026 draft | G6 quotes no GPME or RAP; DOIs and version note added. |
| G3 re-check: Jarrow–Turnbull and other works | Not cited; no misattribution in G6. |
| Re-checks 10, 14, 11, 13 | Not cited. |
| §2.2, §2.3 | G6 had 0 not found and 0 mismatched. |
| §2.6 #1, #3, #5 | Not cited. |
| §2.6 #2 stream-07 side | 07 file outside this list (fixed by the 07 editor). |
| In-text [K] tags | Kept (claims not re-read); [M] covers metadata only. |
| Verification-log corrections C2, C22, C26 | Not audit corrections; recorded as open. |
| Optional completions (Block et al. pages and DOI; DOIs for Chernenko et al., Acharya & Steffen, Li–Strahan–Zhang) | Not listed as fixes. |
| Lit §3–§5 backfill and challenges | Out of scope. |
| Verification-log erratum | Not needed. |
| Relayed Real Assets request | No conflict; nothing added. |

### fix:G7 (11 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in G7 files. |
| Re-checks 10, G3, 14, 11, 13; §2.6 items | Not cited. |
| §2.2 #5 Gorton & Metrick 'Haircuts' | G7 cites a different Gorton–Metrick paper; its pages and DOI were added. |
| §2.3 Nadauld 0.974 → 0.976 | G7 quotes no PME; metadata completed. |
| Lehman timing '~6% in three weeks' (about five weeks per VL claim 4 / R11) | Not in the correction sources; still needs the VL fix. |
| Other verification-log corrections (R1–R11; claims 9, 10, 12, 16, 30; Lazard 27%; WilmerHale 'given away'; Harvard; Cambridge Associates authors; 'EIA spot') | Not correction sources. |
| Li–Strahan–Zhang condition in the §1 item 7 exec bullet | The lit fix targets §4.2(3); the exec bullet states only the draws. |
| Design recommendations (state-dependent waterfall, revolver ≤50%, etc.) | Out of scope. |
| Miller–Orr reading | No abstract; marked 'reading not re-checked'. |
| Robinson & Sensoy NBER WP DOI | Optional; not re-confirmed. |
| Schmieder et al. author list (Crossref lists seven) | Kept the five on the PDF title page; note added. |

### fix:G8 (11 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in G8 ('barriers' are TPA adoption barriers). |
| Re-checks 10 (other than Smith & Winkler), G3, 14, 11, 13 | Not cited. |
| EFW GPME/RAP label and April 2026 numbers | G3-specific; version and DOI added. |
| §2.6 items | Not cited (Bühlmann Z only as a method). |
| §2.4 #16 Albuquerque half | Belongs to G2; the Glaser half was applied. |
| Informational lit-table notes (Tasche, Weitzman/Ekern, Ozbas & Scharfstein, Milgrom 1988, Harris & Raviv, Hirshleifer) | No correction asked. |
| G8 lit backfill and challenges | Out of scope. |
| Verification-log non-citation findings (F5, F8/R20, R1–R19) | Left for the owner. |
| Verification log F4 cell and Lamont row text | Unchanged; the one erratum line records the correction. |
| Alonso–Dessein–Matouschek corrigendum detail | Not added (no abstract). |
| Relayed Real Assets request | G8 still describes 'seven groups'; group framing needs a separate step. |

### fix:G9 (15 items)

| Skipped item | Reason |
|---|---|
| Barrier re-run values | None in G9 ('BGK' there is Brown–Gredil–Kaplan; 62.5% is NACUBO's share). |
| Topic-10 re-check items other than Aas | Not cited (Bühler 2020 appears only in the G9 lit backfill). |
| G3, 14, 11, 13 re-checks | Not cited. |
| §2.3 Sakana/Nature correction | G9's 'Sakana-style rubric verification' has no citation to correct. |
| §2.2–§2.6 items for other streams | Not cited, or the affected figure is not repeated. |
| §2.2 #3 Ljungqvist & Richardson | Only in the ref-12 pointer list; not mis-cited. |
| Lit 'not checked here' version notes (HJKS; Fang–Ivashina–Lerner) | Informational; Fang, BJS and Barras keep †. |
| Hoffman & Atlas (2016), Avanzi et al. (2021) as extra sources | Not added (Avanzi abstract unverified). |
| Synthcity NeurIPS 2023 D&B listing | Not added (same-work identity unverified). |
| DOIs in the ref-12 pointer list (Ben-David–Graham–Harvey, Takahashi–Alexander, Nadauld) | Not flagged. |
| Alaa et al. subtitle | Only the venue was requested. |
| Geltner (1993) abstract | T&F 403; the choice of 1993 is marked [I]. |
| VL R8 combined forecast rigidity | Design recommendation. |
| Other verification-log items (US vs USD label, R1–R14, etc.) | Out of scope or not wrongly accepted. |
| Relayed Real Assets request | No RA content in G9 files. |

### fix:clusters (18 items)

| Skipped item | Reason |
|---|---|
| G4 barrier re-run values | None in C1–C4; explanatory note added to C2's corrections section. |
| §2.2 #1 de Finetti | C1 uses the concept without a reference entry. |
| §2.2 #2, #5, #6, #7, #11 | Not cited in the clusters. |
| §2.2 #3, #4/#12, #8–10 | Already correct or no error. |
| §2.3 Mohajerin Esfahani & Kuhn subtitle | C1 cites author-year only. |
| §2.3 Nadauld and BGG in C2 | Already correct. |
| §2.3 other mismatches | Not cited. |
| §2.4 items for G4, G3, G2, G7, G6, G8; #7 Lo, M&M, K&L; #8; #10–#13 | Not cited or already correct in C1–C4. |
| §2.5 Föllmer & Leukert DOIs and other hygiene | C1's key references are author-year and defer to the dossiers. |
| §2.6 #1, #3, #4, #5 | Not cited (#2 Bühlmann applied in C4). |
| Re-check items (10, 11, 13, 14, G3) | Not cited or already correct (C1 row 10-9 already 447 / 986 / 2,658 / 4,970; C4 V2, V27, V32 already right). |
| Topic-11 re-check: Browne danger-zone threshold | C1 §9 item 4 is a different inference; unchanged. |
| Ennis −1.87% verification | Attempted; II gives the figure without naming the paper; attribution kept [I], unverified. |
| Jeanne–Rancière 9.1% | EJ abstract silent; applied 'per a citing abstract', medium confidence. |
| Bailey et al. (2017) volume/issue/pages | Crossref has none; 20(4) from the audit; pages not added (now confirmed on the publisher page; see open items). |
| Per-topic items outside §2 (C3 Mexico WP; 'WSJ via Wiki'; DWY NBER; Busseti journal version) | Not in the audit's §2 list. |
| C3 §8 '2 of 3 runs' without C4 V1's scope correction | Out of scope; owner to reconcile. |
| Relayed Real Assets request | Outside the four-file scope. |

### fix:group-clusters (15 items)

| Skipped item | Reason |
|---|---|
| Relayed Real Assets request | Outside this step. |
| §2.2 items 1–3, 5–12 | Not cited, method-name only, or no reference list in GC1/GC2. |
| §2.3 items for other streams | Not cited or already correct (BGG published values; 0.976). |
| §2.3 G8 Lamont | Recorded as the one erratum line in GC2 §2. |
| §2.4 #3 remainder (LPG scale; Axelson refs) | GC1 uses LPG only for the zero-return share; Axelson works not cited. |
| §2.4 #4 second half ('Smoothing ≈0.5 (BGG)') | No BGG attribution in GC1; KBRA attribution already right (DOI added). |
| §2.4 #5, #7, #9–#13 | Not cited. |
| §2.4 #14 remainder (Gorton–Metrick; 'central Treasury') | Not cited; GC2's naming note already reads CF. |
| §2.4 #15 G6 items; #16 | Already right or not cited. |
| §2.4 #8 G9 items | GC2 O4 already maps Campbell–Sharpe to w_a or ρ_f. |
| §2.5 hygiene; §2.6 items 1, 2, 4, 5 | Not cited (no reference lists). |
| Barrier values outside GC1/GC2 | Not quoted (write-off rate added to D19 only). |
| Re-check works (10, G3, 14, 11, 13) | Not cited; EFW March 2024 version kept. |
| Optional DOIs for works GC2 cites by author | No reference list by design. |
| Erratum in GC1 about the G4 verifier missing the BGK sign | Audit says the log 'does not raise' it, not that it wrongly accepted it. |

### fix:main-addenda (16 items)

| Skipped item | Reason |
|---|---|
| Relayed Real Assets request | Outside this step. |
| §2.2 items | Not cited ('Rede' is Rede Partners). |
| §2.3 items other than Ennis and Nadauld | Not cited; gap_05 already used 0.976. |
| §2.4 items 3, 5, 7, 9, 10, 12–16 | Not cited. |
| §2.4 #4 Cai & Haque | gap_01 already credits KBRA DLD; DOI added. |
| §2.4 #1 'BGK's 2.6pp' in gap_01 | Brown–Gredil–Kaplan, unaffected. |
| §2.4 #8 López de Prado (2018) | Unchecked; no correction given. |
| §2.4 #11 DSR 0.86 in gap_05 | From C3's example, which already uses skew and kurtosis. |
| §2.5 items not present; G5 shortened titles | Not cited (Clopper–Pearson applied). |
| §2.6 items | Not cited. |
| gap_04 group-engine barrier (g04_engine.py:978) | In the groups addendum (other editor); research/addenda/gap_04 has no barrier statistic. |
| Book-simulation write-off rate and related values | Not in the five addenda. |
| Re-check works other than Kritzman ×2, Gatheral–Jacquier, EFW, Böni–Manigart | Not cited. |
| Groups gap_04 §8 item 7 broader request (strike '2 × (PE − liquid CMA)', insert c^PACE) | Not applied: it is the pacing cost the engine used; repricing needs a re-run. |
| gap_01 'GLM smoothing' without an entry | Sources defer to the G1–G9 dossiers. |
| Works not covered by any audit table | No correction exists. |

### fix:group-addenda (13 items)

| Skipped item | Reason |
|---|---|
| gap_02.md (whole file) | No audit, barrier or re-check correction concerns a work it cites; left unedited. |
| Barrier items quoted in research/addenda/gap_01.md | Main-report file (handled by the main-addenda editor). |
| Other barrier values and 'provisional' wording (G4 dossier, verify, GC1, syntheses, design brief, sufficiency audits, calc JSON) | Not in the four files. |
| gap_04 numerical re-run | Not re-run (RESULTS §6.3); text annotated only. |
| NAV-facility LTV caps | Contractual caps, not monitored barriers. |
| Ljungqvist & Richardson in gap_04 | Already NBER WP 9454. |
| Kaminski & Lo vs gap_03 drawdown stop | gap_03 does not cite K&L or make its claim. |
| Baumol & Fabian gloss in gap_01 | G8 verification-log item (F5), not an audit correction. |
| gap_03 bare links ('Rampini et al.', 'Drechsler 2013') | Backfill entries; no correction listed. |
| Acharya, Shin & Yorulmazer (2011) pages | Sources disagree; no correction specified. |
| Re-check works (10, 11, 13, 14, G3) | Not cited. |
| §2.2–§2.6 other items | Not cited. |
| Relayed Real Assets request | Outside this step; 'seven groups' framing unchanged. |

### fix:main-synthesis (15 items)

| Skipped item | Reason |
|---|---|
| Relayed Real Assets request | Outside this step; new text avoids hard-coding the group count; existing 'seven groups' wording unchanged. |
| Book-simulation write-off rate and related values | Not quoted in main. |
| LTV breach, 2× default, LEVER normal, REFI 29–37%, gap_04 barrier, 'provisional' | Unchanged or not present (50–63% and 7.0% → 22.8% annotated). |
| Jeanne & Rancière 9.1% vs 10.1% | Main cites the 2006 WP and never quotes the figure. |
| Not-found, mismatched and usage items absent from main (about 50 works) | Not in main (grep). |
| Re-check items absent from main | Not cited; §4.8 already limits Campi–Garatti to convex sub-programs. |
| Lange et al. overstated sentence | Not present in main. |
| Fogliato, Böni & Manigart, EFW GPME, Cai & Haque usage points | Flagged claims not made in main; metadata only. |
| §2.6 #1, #3, #4, #5 | Not cited (#2 Bühlmann confirmed). |
| de Finetti (1957) full title | Crossref none; OpenAlex 429; venue and pages only, tagged [U]. |
| L8 'deflated Sharpe of 0.86' recomputation | No inputs in main; only the gate definition corrected. |
| Lu et al. '66% balanced accuracy' (§5.5) | The audit flags 69% and 6.33, not 66%; metadata only. |
| Optional or unflagged completions (Dwork Science, Boutilier AAMAS, HJKS, Cavagnaro, etc.) | Not flagged or metadata unconfirmed. |
| Groups synthesis C10, C15, readiness- vs event-Red, group Amber additions, §0 'v1.0' reference | Real inconsistencies but not among the four requested consistency edits. |
| Verification-log erratum | Main has no verification log. |

### fix:group-synthesis (16 items)

| Skipped item | Reason |
|---|---|
| Relayed Real Assets request | Citation corrections only; seven-group wording left for the step that adds Real Assets. |
| §2.2 #3, #6 and other items | Already correct, method name only, or not cited. |
| §2.3 other streams | Not cited; BGG published values already used; 0.974 not quoted. |
| §2.4 #3 (LPG scale; Axelson entries; K&S pages) | LPG not used as deal-size evidence; works not cited. |
| §2.4 #4 | KBRA attribution already correct (DOI added); no 'smoothing 0.5 (BGG)'. |
| §2.4 #5, #7, #9, #10, #12, #13, #15, #16 | Not cited. |
| §2.4 #8 | O4 already maps to w_a or ρ_f; HJK, Aas, López de Prado, Borisov not cited. |
| §2.4 #11 DSR non-normality | No DSR formula; worked example not re-derivable; bibliography title names non-normality. |
| §2.4 #14 | Gorton–Metrick not cited; generic 'repo haircuts widen in crisis' left; LSZ caveat applied. |
| §2.5 hygiene; §2.6 #1, #2, #4, #5 | Not present except Clopper–Pearson (added). |
| Barrier values not quoted (write-off rate, counts, cost share, NAV gap, P90, 2× default, REFI/LEVER, 'provisional') | Nothing to edit. |
| §3.4 book-simulation cash flows | Unchanged at quoted precision. |
| Recap-multiplier dependent outputs | The gap_04 engine applies no post-recap multiplier. |
| Re-check works (10 other than Smith & Winkler; G3; 14; 11; 13) | Not cited; EFW statements hold in both versions. |
| Optional completions (Korteweg–Sorensen pages, HJKS article number, Block et al. pages, Tóth DOI, etc.) | Not corrections. |
| Verification-log erratum | No log. |

## 5. Items still open

### 5.1 Audit and re-run items left unfixed (the text sits in files no editor was given)

| # | Item | Where | What is needed |
|---|---|---|---|
| 1 | §2.6 #1: Giommetti et al., "Optimal Allocation to Private Equity", second author | "Giommetti & Jørgensen" in `literature/01_mpo.lit.md` l.252, l.372; `literature/06_leverage.lit.md` l.488, l.685; `literature/11_objectives.lit.md` l.426, l.578 | Read "Giommetti & Sørensen". The 04 editor confirmed Morten Sørensen on Crossref and OpenAlex (SSRN 3761243); dossiers 04 and 05 are already right |
| 2 | §2.6 #5: Gredil, Liu & Sensoy diversification cost | "2–8%" in `literature/04_pe_cashflows.lit.md` l.465 and `literature/08_action_valuation.lit.md` l.467; "up to 5%" in `literature/G4_coinvest.lit.md` l.242, l.247, l.350 | Pin down the version cited. No dossier, cluster or synthesis cites the work, so no research claim depends on it yet |
| 3 | §2.4 #1: uncorrected barrier in the gap_04 group engine | `groups/addenda/gap_04_calcs/g04_engine.py` l.978 writes off when `co_v < 0.85 * co_d`, checked quarterly with no shift | At the next re-run, apply κ·e^{+0.5826σ_V√Δ} (RESULTS §6.3). The text already flags the bias (groups gap_04 §1.1, §1.2, §9; groups synthesis §4.9) |
| 4 | Stale "provisional / understated" barrier wording | `design/00_DESIGN_BRIEF.md` l.445 (§7 item 15, path from the project root); `sufficiency/Q03_audit.md` l.76, l.110; `Q06_audit.md` l.92; `Q07_audit.md` l.74; `Q08_audit.md` l.33, l.61, l.87; `Q14_audit.md` l.68; `Q06_challenge.md` l.43; `literature/00_LITERATURE_SYNTHESIS.md` l.27 and l.135 | Use RESULTS §6.2's wording: the sign error is confirmed; the affected statistic is the book-simulation write-off rate (2.1–2.5% → 2.8–3.3%); the at-exit wipe-out and quarterly-tested LTV-breach rates are unaffected. Optionally label the wipe-out "at exit" in `Q06_audit.md` l.34 and `Q06_challenge.md` l.9 |
| 5 | Other sufficiency notes this pass has overtaken | `sufficiency/Q07_audit.md` l.75 ("the groups synthesis still carries 1.4–3.4", now fixed); `Q10_audit.md` l.82 ("C3 §6 still says 10.1%", C3 now gives both 10.1% and 9.1%), l.85 ("Kaminski–Lo … is unchecked", now checked at abstract level in 09) | Refresh at the next sufficiency pass |
| 6 | Beel et al. DOI typo | `literature/12_agentic_ai.lit.md` gives 10.1145/3769733.376974 | Crossref gives 10.1145/3769733.3769747, which dossiers 12 and 13 now use |
| 7 | Merton (1993) chapter and pages not added in stream 11 | `dossiers/11_objectives.md` l.609 | Add "ch. 7, pp. 211–242", as done in 01, 02 and 03 (§2.2 #2 named only stream 03) |
| 8 | Meucci (2008) entry not harmonized | `dossiers/07_return_fusion.md` l.566 (ref 48): "*Risk* 21(10).† SSRN 1213325" | Optional: use 21(10):97–102 with arXiv 1012.2848, as in 10, 14 and the main synthesis (§2.4 #13 named stream 10) |
| 9 | PBO pages missing in several files | `dossiers/12_agentic_ai.md` ref 74; `dossiers/13_paper_deepread.md` §10; `clusters/C4_agentic_ic.md` §14; `00_SYNTHESIS.md` §11 | Optional: add pp. 39–69 (Volume 20, Number 4, April 2017), now confirmed on the publisher page; 01 and 09 already carry them |
| 10 | Geltner: same filter, two papers | The AR(1) / partial-adjustment unsmoothing filter is cited to Geltner (1991) in 04 and G3, and to Geltner (1993) in G5, G6 and G9 (G9 marks its choice [I]) | §2.6 #4 is met, since every citation now names its paper. But the corpus should pick one convention. 04's split (1991 for the smoothing model, 1993 for the recovery procedure that does not assume uncorrelated returns) is the clearest |

### 5.2 Needs a decision by the user or ADIC, or ADIC library access

1. **Add a Real Assets group (the user's request in this run).** This pass did not do it.
   - **Where it stands.** Work appears to be under way elsewhere: the design brief has a section "8. Real Assets, the eighth group (added 2026-10-18, about 17:40)", and `groups/dossiers/G10_ra_real_estate.md` through `G15_ra_portfolio_role_liquidity.md` and their six verification logs were written between 19:00 and 20:03 today, while this pass ran.
   - **Not audited.** These files were not part of the 574-citation audit and have had no literature check. Their own verification logs do check citations; for example, the G10 log flags a wrong DOI for Fisher & Hartzell (2016).
   - **"Seven groups" wording remains** in G8, the groups synthesis, groups gap_04 and elsewhere. G5's §6.16 links row does not mention Real Assets.
   - **No flagged errors repeated.** A grep of the Real Assets dossiers for 22 audit-flagged authors and values found none of the flagged errors; their Brown–Ghysels–Gredil citation already uses the published *RFS* metadata.
2. **G4 co-investment write-off calibration.** With the corrected barrier, the simulated write-off rate (2.8–3.3% a year) is 2.3–2.8× Kaplan–Strömberg's ≈1.2%. Recalibrating κ or the ICR hazard is a model-owner decision (RESULTS §8; GC1 D19).
3. **Geltner convention.** Item 10 above.
4. **Erel, Flanagan & Weisbach version.** Every file cites NBER w32278 (March 2024). An April 2026 draft has different figures (545 funds, 8.5% IRR, fees 3.2–4.2%). Decide whether to move to it.
5. **Paywalled checks that need journal access.** Several values are labelled as working-paper figures, or carry [unverified], pending full texts:
   - Boyer et al. (*JF* 2023): β and returns are from NBER w28691;
   - Nadauld et al. (*JFE* 2019): age-group splits are from NBER w22404;
   - Lerner, Mao, Schoar & Zhang (*JFE* 2022): the 32% / 17% / 112-LP figures;
   - Albertus & Denes (*JFQA* 2026): whether it matches the 2020 version;
   - Moutanabbir & Noureldin (*IREF* 2020): hedging demand, sample and sign;
   - Bollen & Sensoy (*FM* 2022): whether 5–10pp survives;
   - Jeanne & Rancière (*EJ* 2011): the 9.1% benchmark;
   - Browne (1997): the safe level c/r;
   - Kahneman, Lovallo & Sibony (2019): MAP pre-votes.

### 5.3 Works and claims still unverifiable from open sources (marked [unverified] or [U] in the files)

| Work or claim | File(s) | Why |
|---|---|---|
| de Finetti (1957), original title | 02 §10; main §11 | Not indexed (Crossref, Consensus); title, venue and pages come from a citing record (Loeffen 2008); OpenAlex returned 429 |
| Dufresne (1988): "Moments" vs "Movements" | 02 §10 | Crossref and OpenAlex read "Movements"; citing references read "Moments"; the Cambridge page returned 403 |
| Ennis (2021b) as the source of the −1.87% | 02 ref 10(b); C3; main §4.12, §11; main gap_05 | *Institutional Investor* reports the figure without naming the paper; the *JPM* abstract has no figure |
| Moutanabbir & Noureldin (2020): 0.01–0.07pp hedging demand, 1976–2016 sample, correlation sign | 03 §2.2; 03 verification erratum | No abstract or open copy; figures stay sourced to ERF WP 1172 |
| Jeanne & Rancière (2011): 9.1% benchmark | 09 §2.3; C3 §6; 09 verification F17 | Known only through Mihailov & Nasir (2022) |
| Boyer et al. (2023) figures | G2; GC1; main gap_05; groups synthesis | *JF* full text not accessed; NBER w28691 used |
| Nadauld et al.: age splits and tail-end tables | G2; GC1; main gap_05; groups gap_04; groups synthesis | *JFE* tables not accessed; WP 22404 figures labelled |
| Lerner, Mao, Schoar & Zhang (2022) figures | G1 §2.2 | No abstract; ScienceDirect 403 |
| Albertus & Denes (2026, *JFQA*) content | G1; GC1; groups synthesis | Metadata confirmed; no abstract; Cambridge 403 |
| "Rode et al." 60bp / 75bp at the primary source | G2 §2.6, ref 39 | Schroders report not fetchable; re-attributed to the CFA report's own example |
| Albuquerque et al.: specifics beyond the abstract; "Cass Business School" affiliation | 05; G2 | SSRN 403; no abstract indexed; specifics tagged [C] |
| Bollen & Sensoy (2022): whether 5–10pp survives in the published paper | 05 §2.2; C2 | Full text paywalled |
| Tausch, Buchner & Schlüchtermann (2022): volume, issue, pages | 04 §10 | Absent from Crossref and OpenAlex; risk.net blocked |
| de Malherbe (2007) | 04 §8 | Not found on Crossref |
| Myers & Majd (1990): publication details | 08 §10 | No Crossref record; OpenAlex 429 (the 1983 MIT working paper is confirmed) |
| Meucci (2012): venue, pages, DOI | 10 §10 | No Crossref record; SSRN DOI 404; OpenAlex 429 |
| Carr & Wu (2009): sign of the average variance risk premium | 10 §6.5 | Confirmed only by secondary literature |
| Cooke studies: "320 experts"; MOS "conceived 1965, first issued 1968" | 07 §4.5, §5 | Both rested on Wikipedia pages, now replaced; the primary abstracts do not state them |
| Stasser & Titus: attribution of the information-sampling formula | 14 §2.2 | Not confirmed in the 1985 paper's abstract |
| Black & Cox (1976): "first-passage barrier represents covenants" | G3 §2.4 | Paper text not read |
| Mack (1993) as the work G3 meant by "Mack" | G3 ref 61 | The dossier gave only the surname; marked [I] |
| MAP prescribing individual pre-votes | 13; 14; C4 | MIT SMR full text paywalled; summaries silent |
| Browne (1997): boundary at the safe level c/r | 11 §6.5; 11 verification erratum | MOR full text paywalled; taken from Bayraktar & Young |
| Geltner (1991) as the source of the smoothing model | 04 §2.5 | Attributed by title; no indexed abstract |
| Kaminski & Lo (2014) usage | 09 §2.6 | Rests on the 2010 SSRN abstract; journal abstract not accessible |
| Fung & Hsieh (2000) bias magnitudes | G5 §4.6, §8 | Not abstract-verified; stay [nrv] |
| Lange et al. (2026); Song (2026) | 12; 13; 14 | Confirmed to exist; no DOI yet (arXiv / workshop) |

### 5.4 Non-citation residuals noticed during verification (for the owners; outside the audit)

1. **Coverage ratio still on the old basis in groups gap_01.** `groups/addenda/gap_01.md` §1.3 l.97 shows ADIC-LCR(30d) at 2.10×, Green. The main synthesis and the groups synthesis (C12, C16) now use 1.91× on Corporate Finance-controlled HQLA, Amber.
2. **NAV-facility action still in two Amber stages.** `groups/clusters/GC2_liquidity_org_data.md` l.416 and `groups/dossiers/G7_liquidity_ladder.md` l.794 still list "activate NAV-facility documents" in the Amber stage. The main synthesis removed it, following groups gap_01's recommendation to drop the NAV facility.
3. **"Central treasury ownership" in 08.** `dossiers/08_action_valuation.md` l.493 uses the phrase in the bank-practice list that ADIC adopts. Under the user-confirmed organization this is Corporate Finance; §2.4 #14 named only G7.
4. **Generic repo-haircut line.** `groups/01_GROUPS_SYNTHESIS.md` l.710 and `groups/addenda/gap_03.md` l.105 say "Repo haircuts widen in crisis", uncited. The Gorton–Metrick nuance is that the spike was in bilateral repo.
5. **Notes the editors left for owners:**
   - 08's "P(LTV > 40% at any point) = 0.7%" is checked at five annual points only;
   - G6 §6.8D's P(deficiency) uses quarterly borrowing-base tests;
   - G1 §6.9's "[S: BGK]" means Brown–Gredil–Kaplan and could be confused with Broadie–Glasserman–Kou;
   - C3 §8's "2 of 3 runs" lacks C4 V1's scope correction;
   - the groups gap_04 §8 request to replace gap_02's pacing cost with c^PACE needs a re-run.
6. **Verification-log findings that are not citation corrections remain open**, as each editor recorded:
   - 01 R-items;
   - 06 claim #27;
   - 12 #1, #3–#6, #8–#9;
   - 14 A1, A5, A10;
   - G1 S12, S15, S16, A2;
   - G5 A34, F20, A23;
   - G6 C2, C22, C26;
   - G7 Lehman timing (≈five weeks, not three) and R1–R11.

---

*Built from the 29 editor reports in this workflow run and checked against the files on disk at 2026-10-18. Scratch scripts used for the checks (presence, tokens, tables, recomputation, residual sweep) are not part of the corpus.*

