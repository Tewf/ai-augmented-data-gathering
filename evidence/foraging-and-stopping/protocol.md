# Protocol: how the pool was built

A first pass of a multivocal literature review to Garousi 2019, run on 2026-11-03 by one reviewer. Terms are in [frame](frame.md); the pool is in [sources](sources.md).

## 1. Why grey literature

Garousi's seven questions, answered for this topic.

| Question | Answer |
|---|---|
| Is the context broader than academic? | yes: reviews are run by handbooks, tools and teams |
| Is practice ahead of the research? | yes: stopping rules sat in handbooks before estimators were tested |
| Do practitioners hold the data? | partly: the search logs of reviews, which are rarely published |
| Are the formal sources thin? | thin on the stopping of a literature search, wide on its parts |
| Is the topic contested? | yes: heuristic stops against estimated ones |
| Does practice need a baseline? | yes: this review ends on one |
| Do formal sources miss the form? | yes: the form of a search log is nowhere set down |

## 2. Questions

Q1 to Q4 of [frame](frame.md): when to stop, where to look, a dear source, the logs.

## 3. Existing reviews (Garousi guideline 2)

- Found and read in part: a survey of active learning (Settles 2009) and a review of species-number estimators (Bunge 1993).
- Found and read: the stopping section of the Cochrane Handbook (Lefebvre 2025), which names the stopping suggestions in use.
- Found: a survey of information foraging in software tools (Fleming 2013), and a review of species richness (Chao 2016).
- Not found: a review of the stopping of a literature search by estimators of the unseen.

## 4. Formal search

OpenAlex counts, field `title_and_abstract.search`, no key and no identity, 2026-11-03. The strings were run to find the field's names, not to screen records.

| Id | String as run | Count |
|---|---|---|
| O1 | "information foraging" | 736 |
| O2 | "information scent" | 186 |
| O3 | "marginal value theorem" | 343 |
| O4 | "optimal stopping" AND "literature search" | 1 |
| O5 | "stopping criteria" AND "technology-assisted review" | 4 |
| O6 | "stopping rule" AND "systematic review" AND screening | 36 |
| O7 | "unseen species" | 177 |
| O8 | "Good-Turing" | 217 |
| O9 | "Chao1" | 4,684 |
| O10 | "capture-recapture" AND "literature search" | 13 |
| O11 | "search saturation" AND "literature review" | 0 |
| O12 | "when to stop searching" AND "systematic review" | 1 |
| O13 | "active learning" AND "systematic review" AND screening | 207 |
| O14 | "value of information" AND "literature search" | 16 |
| O15 | "species richness estimator" AND "systematic review" | 0 |

- O11 and O15 returned zero. That says the words are wrong, not that nothing exists: the field says "saturation" with other words.
- Eight follow-up strings were refused by the service (HTTP 429, a shared daily budget) and were not rerun.
- Crossref resolved every DOI of the pool without a key; three first guesses resolved to other papers and were corrected by title.
- Counts of citations on 2026-11-03: Pirolli 1999, 1,358; Spoor 1996, 51; Callaghan 2020, 121 (OpenAlex).
- Backward snowballing: leads taken from the Cochrane Handbook section on stopping (Callaghan 2020, Li 2020, Sneyd 2021) and from Callaghan 2020 (Howard 2020).
- Forward snowballing: not run, because the service refused the citing-list requests.

## 5. Grey search

- Producers: the Cochrane Handbook, the documentation of one Python package, the source of one R package.
- GitHub repository search without sign-in, two strings: "chao1 estimator species richness python" returned 0 repositories; "stopping criteria technology assisted review" returned the code of Sneyd 2021 first.
- Reference implementations were looked for under the authors' names: iNEXT (Chao's group), rapid-screening (Callaghan), scikit-bio.
- Not searched: forums, Q/A sites, talks, videos, patents, social media, books other than those named.

## 6. Stopping rule

- Effort bounded: the pool is capped at 40 sources, the first-pass size.
- Saturation per string was not applied or logged. Sources were named in the frame step and verified, so no string has a count of results seen with new concepts.
- This is the defect the review finds in the family's own logs ([on the family](on-the-family.md)). It is stated here so the review does not pass for an exception.

## 7. Selection

- Include: a theory or method for where to look, when to leave, how much is unseen, or when to stop; a study of stopping in review screening; a reference implementation.
- Exclude: domain applications of foraging, bandits or species estimators with no method for the problem.
- Quality: formal sources carry an evidence grade; grey sources a score (section 8).

## 8. Quality of grey sources

Garousi's 20 criteria in eight groups: authority 4, methodology 6, objectivity 4, date 1, position 1, novelty 2, impact 1, outlet 1. Threshold 10 of 20. Scores are in [sources](sources.md).

## 9. Extraction and synthesis

- Per source: the claim, the number, and how it was read: in the text, the abstract (secondary), or the record only.
- Formulas were read in the source code of iNEXT and in the scikit-bio documentation, not recalled.
- Synthesis is narrative by question.

## 10. Limits

- One reviewer, no second rater, on the formal or the grey scores.
- Most formal sources were named from the reviewer's knowledge and checked as records. About half are located only, and no claim leans on them beyond their title and field.
- Leads not read, each a work the reviewer could name:
  - the 2003 paper on stopping rules for search development by Chilcott and colleagues, cited by Lefebvre 2025;
  - the knee method of Cormack and Grossman;
  - the survey of capture-recapture by Chao and colleagues.
- Search services change and refuse; counts are those of 2026-11-03.
- No identity was sent to any service.
