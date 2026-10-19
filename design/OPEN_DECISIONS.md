# Open decisions

19 October 2026. This list consolidates the open questions from five sources:
- the design revision (`design/reviews/revision_log.md`);
- the chat-analyst design (`design/addenda/CHAT_ANALYST.md` §15);
- the research-sufficiency audit (`research/00_RESEARCH_SUFFICIENCY.md` §4);
- the group report (`research/groups/01_GROUPS_SYNTHESIS.md` §9);
- the Real Assets work.

Each item gives:
- the decision;
- who decides;
- why it matters;
- the **working assumption** the build uses until it is answered.

All figures are SYNTHETIC.

## A. Owner and mandate

1. **Owner band and draw convention.**
   - **Decision:** will the owner agree in advance that ADIC may pay the 5% minimum in a crisis (Mode H)? And how is the annual draw measured: fixed USD, opening-of-year NAV reset, or current NAV?
   - **Decides:** CIO and IC, with the owner.
   - **Why it matters:**
     - It decides the hedge mix. Without the band, Mix A costs about 66–76bp a year; with it, Mix B costs about 23–29bp.
     - The draw convention alone moves the literal 24-month stress facility need between $25bn and $43bn.
     - The literature calls the band contested: owners' own costs peak in the same crises.
   - **Working:** Mode B (no band). The draw resets on opening fiscal-year NAV, and the band appears only in owner proposals.

## B. Tier-1 contract (IC ratification)

2. **Stress calibration (T4′).**
   - **Decision:** calibrate model class by model class (θ\* ≈ 0.58), or hold the harshest class (M6) at 1% as a Board prudence overlay (θ\* ≈ 0.76–0.79)?
   - **Also to accept:** the T6 tolerance bands; the economic-substance red event; and the stress conventions:
     - revolver credited at ≤ 50% in the crisis stress, not 80%;
     - a two-quarter lag before a pacing cut earns liquidity credit;
     - stressed Real Assets income.
   - **Why it matters:** this sets the committed-facility ask. Under the overlay reading it is about $13.9–14.6bn at 80% credit, or about $22bn at 50%.
   - **Working:** class-banded θ\*, recalibrated at the contract check, with ≤ 50% revolver credit. The research conventions are shown as a sensitivity.
3. **Replacement safety floor (Tier 1B).**
   - **Decision:** accept or replace the floor.
   - **Why it matters:** v8's floor is infeasible. The proposed replacement (worst-model CVaR₁₀ ≥ 0 over 10 years) fails today in 3 of 6 model worlds.
   - **Working:** keep the replacement with its 10-year window, banded by model class.
4. **Model weights across the six model worlds,** including the weight on the harshest world (M6).
   - **Why it matters:** the weights move every headline range. J.P. Morgan supplies 3 of the 6 worlds.
   - **Working:** equal weights until the annual IC vote.
5. **Target definition.**
   - **Decision:** is 10% measured gross or net of distributions, and over what horizon?
   - **Working:** nominal geometric 10-year time-weighted return, gross of distributions. The net figure is reported too.

## C. Funding (Corporate Finance)

6. **Lines and instruments.**
   - **Decision:**
     - What are the existing credit lines, covenants and test history?
     - Is there appetite for a committed revolver of $10–15bn, or about $22bn if crisis credit is 50%?
     - Are LP-level NAV facilities, LP-portfolio preferred equity, CFOs, oil options and hybrids permitted?
     - Is net short volatility allowed?
     - Does physical-to-synthetic count toward the 0.30×W cap?
   - **Working:**
     - The revolver is unsigned, so prices use the group-levers-only scenario.
     - The NAV facility is capacity-capped.
     - Oil options and hybrids are off.
     - No net short VIX-equivalent vega is allowed in stress.
     - Physical-to-synthetic counts toward both caps.

## D. Data ADIC must supply

7. **Marks archive details.**
   - **Decision:** the start quarter; whether cash flows and exit horizons are stored per holding; which groups file IRR and which MOIC; and the case conventions.
   - **Working:** quarterly from 2008, with cash flows and exit timing per holding, and cases read as P10/P50/P90.
8. **Holdings data:**
   - hedge-fund terms per lot;
   - PE commitments by vintage;
   - Real Assets size, unfunded commitments, energy exposure and asset-level debt tapes;
   - overlay blotter and CSAs;
   - private-credit loan tapes;
   - look-through company and sponsor IDs.

   **Working:** the synthetic book (SYN-ADIC-177).
9. **Public market data.**
   - **Decision:** may someone with network access snapshot the missing monthly series into `data_public/` (work package WP-41), and from which licensed sources?
   - **Working:** increment 1 runs on the existing 23-column panel with labelled fills.

## E. Organization and incentives

10. **Organization and pay.**
    - **Decision:**
      - Where do the boundaries between Capital Solutions, Private Credit and Secondaries sit?
      - What are the forecasters' pay parameters (b, s) for the strategic-bias gate?
      - Can Corporate Finance hold the FTP mismatch?
    - **Working:**
      - Boundaries as in the research.
      - The forecast weight of a group that fails the strategic-bias test stays capped until pay design changes.
      - Corporate Finance holds the mismatch.

## F. Chat analyst (R16)

11. **Claude Code / Desktop surface.**
    - **Decision:** which roles may use it? The model's prose there cannot be validated.
    - **Working:** every role on SYNTHETIC data. REAL data is allowed only after in-region serving and a managed single-server profile. It is never cited in a decision record.
12. **Information barriers.**
    - **Decision:** which groups are private-side, and what is the restricted-list source?
    - **Working:**
      - Private side: Private Credit, Capital Solutions, Co-investment, and the direct books of Secondaries and Real Assets.
      - Public side: Public Markets and the opportunistic overlay.
      - Above the wall: IC, CIO, CRO, Treasurer and the TPA desk.
13. **Transcripts.**
    - **Decision:** retention period and readers.
    - **Working:** 7 years. Readable by the user and by governance (MRM, AI governance, compliance), via the CLI only.
14. **Pre-vote window.**
    - **Decision:** may voting members use chat between pack publication and their own pre-vote lock?
    - **Working:** facts only on Tier-A items.
15. **Citing what-ifs.**
    - **Decision:** may a chat what-if be cited in a brief or decision record?
    - **Working:** only after confirmation on an ADIC surface and an exact engine recompute. Irreversible Tier-A actions also need a sealed confirmatory run.

## G. Build scope

16. **Increment 1.**
    - **Decision:** build the 10-week MVP at reduced fidelity first, or a wider first increment?
    - **Working:** the MVP first (S-ADR-37), including a thin slice of the chat analyst.
17. **Real Assets size and PE unfunded rescale.**
    - **Decision:** the Real Assets size inside the 60% private allocation, and whether to rescale PE unfunded for the smaller PE bucket ($16.4bn as chosen, or about $10.9bn rescaled).
    - **Working:** Real Assets at $18bn, with both PE figures reported.
18. **LLM deployment.**
    - **Decision:** in-region serving, approved model families, and a second provider.
    - **Working:**
      - No real data goes into prompts.
      - Live calls run on synthetic data only.
      - Family B is claude-sonnet-5-5, labelled as correlated with family A.
