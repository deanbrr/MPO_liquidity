# Topic 13 (paper_deepread): re-check of the citations the Consensus quota left unchecked

**Date:** 2026-10-18

**Scope:** the 4 works marked "not checked (quota)" in `research/literature/13_paper_deepread.lit.md` (§2 table; §7 "Not checked in Consensus"), as cited in `research/dossiers/13_paper_deepread.md`. The dossier was not edited.

**Method:**
- Crossref REST API: bibliographic queries and DOI records.
- Publisher pages: arXiv, AAAI OJS, hbr.org, sloanreview.mit.edu.
- PubMed E-utilities, for the HBR volume and pages.
- One WebSearch, to find a readable description of MAP. The MIT SMR full text is paywalled.
- OpenAlex returned HTTP 429 (Retry-After 37,619 s), so it was not used. Consensus was not used.

**Result:** 4 checked. 4 ok, 0 not found, 0 mismatched, 0 usage problems. None is fabricated.
- One reference-hygiene item: Alshiekh et al. is still an orphan reference.
- The other entries can optionally be completed.

## Verdicts

| Citation (dossier §10) | Verdict | Correction | Source URL |
|---|---|---|---|
| Alshiekh, M., et al. (2017). *Safe Reinforcement Learning via Shielding.* arXiv:1708.08611 (l. 1150) | ok; orphan reference (hygiene) | Metadata: no change. The six authors are Mohammed Alshiekh, Roderick Bloem, Rüdiger Ehlers, Bettina Könighofer, Scott Niekum and Ufuk Topcu; arXiv v1 is dated 29 Aug 2017. A peer-reviewed version exists: *Proceedings of the AAAI Conference on Artificial Intelligence* 32(1) (AAAI-18), published 29 Apr 2018, DOI 10.1609/aaai.v32i1.11797. Neither the AAAI page nor the Crossref record gives a page range, so do not add one. The body still never cites it: cite it or drop it (note 1). | https://arxiv.org/abs/1708.08611 · https://ojs.aaai.org/index.php/AAAI/article/view/11797 · https://api.crossref.org/works?query.bibliographic=Safe+Reinforcement+Learning+via+Shielding+Alshiekh&rows=5 |
| Klein, G. (2007). *Performing a Project Premortem.* HBR (l. 1151; used in §5.6 l. 545, Stage 7 l. 765, §6.5 l. 977, §8 l. 1097) | ok; usage accurate | None needed. HBR shows Gary Klein, September 2007 issue, Reprint F0709A. The HBR page gives no volume or pages, and neither Crossref nor PubMed has the HBR record, so none are added (note 2). | https://hbr.org/2007/09/performing-a-project-premortem · https://api.crossref.org/works/10.1109/emr.2008.4534313 |
| Kahneman, D., Lovallo, D., Sibony, O. (2011). *Before You Make That Big Decision…* HBR (l. 1152; used in §5.6 l. 546) | ok; usage accurate | None needed. Optional completion: HBR displays the title as "The Big Idea: Before You Make That Big Decision…"; "The Big Idea" is HBR's section label. *Harvard Business Review* 89(6): 50–60, 137 (June 2011; PubMed PMID 21714386). No DOI (note 3). | https://hbr.org/2011/06/the-big-idea-before-you-make-that-big-decision · https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=21714386&retmode=json |
| Kahneman, D., Lovallo, D., Sibony, O. (2019). *A Structured Approach to Strategic Decisions.* MIT SMR (l. 1153; used in §5.6 l. 547, Stage 7 l. 764, §6.5 l. 976) | ok; usage accurate as worded | Metadata: no change. Optional completion: published 4 Mar 2019, Spring 2019 issue, Reprint 60314. The publisher page shows no volume or pages, and Crossref has no record, so none are added. The §5.6 caveat can be narrowed (note 4). | https://sloanreview.mit.edu/article/a-structured-approach-to-strategic-decisions/ · https://sbi.sydney.edu.au/?p=5672 |

## Notes

**1. Alshiekh et al.**
- "Shield" occurs in the dossier only in this §10 entry, so the lit file's orphan flag still stands.
- The dossier makes no claim about the paper. The lit file proposes citing it for Tier-1 gates that act as a "shield", blocking unsafe actions before execution.
- The arXiv abstract supports that mechanism. A shield is synthesized from a temporal-logic specification. It either gives the learner the list of safe actions before each choice, or monitors the chosen action and corrects it only if it would violate the specification. Applying it to ADIC's gates is an analogy [Inference].
- If the entry is kept, a complete version is: Alshiekh, M., Bloem, R., Ehlers, R., Könighofer, B., Niekum, S., Topcu, U. (2018). Safe Reinforcement Learning via Shielding. *Proceedings of the AAAI Conference on Artificial Intelligence* 32(1). DOI 10.1609/aaai.v32i1.11797. Preprint: arXiv:1708.08611 (2017).

**2. Klein (2007).**
- **Usage is accurate.** The dossier glosses the premortem as "imagine the decision has failed, then explain why". HBR's summary says "team members assume that the project they are planning has just failed", then generate plausible reasons for the failure. Klein frames it around a project plan; applying it to an investment decision is a fair adaptation.
- The "at least 3 failure narratives" threshold in `premortem_logged` is the dossier's own design (§6.5 is tagged [I]), not Klein's.
- **Crossref's only record under this title** is a 2008 version in *IEEE Engineering Management Review* 36(2):103–104, DOI 10.1109/EMR.2008.4534313. Its record carries no reprint note [unverified: how it relates to the HBR original]. Keep the HBR 2007 citation; do not switch to the 2008 year.

**3. Kahneman, Lovallo & Sibony (2011).**
- **Usage is accurate.** The dossier calls it "bias-aware decision review". This matches the HBR dek, "Dangerous biases can creep into every strategic choice. Here's how to find them—before they lead you astray", and the article's focus on detecting biases in a team's recommendation before the decision is taken.
- **Crossref's top results hold no record of the article itself.** They hold only a summary of it: Hue Chye Ling, *CFA Digest* 41(3):12–13 (2011), DOI 10.2469/dig.v41.n3.32. Do not cite that DOI as the article's.

**4. Kahneman, Lovallo & Sibony (2019): MAP.**
- The publisher page confirms that this article introduces the "Mediating Assessments Protocol (MAP)". The description of the protocol itself sits behind the paywall.
- **A readable summary** comes from Sydney Business Insights (University of Sydney Business School, May 2019), which cites this article. It gives three steps:
  - "Define each assessment criteria in advance";
  - "Use fact-based independently made assessments";
  - "Make the final evaluation".
  - The purpose is to "delay your intuition". It quotes Lovallo: "each attribute is assessed one at a time and then apply your judgment holistically."
- **So the §5.6 gloss is accurate.** "Structured, independent assessments made before holistic judgment" matches these steps. The caveat "I did not verify the details of its steps" can be narrowed to the finer points.
- **Not confirmed by any readable source: that MAP prescribes individual pre-votes before discussion.**
  - The dossier's Stage 7 "independent pre-votes on the mediating assessments" and its `independent_prevotes` ("MAP-style") rubric are the dossier's own design; §6.2 and §6.5 are tagged [I].
  - [unverified: the MIT SMR full text is paywalled, and the summaries consulted do not mention pre-votes.]
  - Keep "MAP-style" as a label for the ADIC design, not as a description of MAP.
- **Suggested §5.6 wording:** "Mediating Assessments Protocol (MAP) (Kahneman, Lovallo & Sibony, 2019): define the assessment criteria in advance, make fact-based assessments independently of one another, and delay holistic judgment until all are complete."
