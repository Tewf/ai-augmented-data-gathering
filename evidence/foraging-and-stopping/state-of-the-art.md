# State of the art: who holds the record

Step 3. The record for each sub-question of [frame](frame.md), by what method and measured how. Upper bounds, what has been achieved, are kept apart from limits. Most adopted, a practice record, is kept apart from best evidence, a research record.

## Best evidence, by sub-question

| Question | Holder | Method | Measured how | Grade |
|---|---|---|---|---|
| Q1 stop, relevant records | Callaghan 2020 | hypergeometric test of "recall below target" | real systematic-review datasets, 100 runs each; reliable recall, 17% work saved on average | measured |
| Q1 stop, relevant records | Howard 2020 | negative binomial model of the records left | 26 datasets; 95% of relevant found after screening 40% on average (secondary) | measured |
| Q1 stop, relevant records | Li 2020; Stevenson 2023 | sampling; point processes | benchmark collections (abstract, secondary) | measured |
| Q1 stop, concepts | Chao 2012 with Hsieh 2016 | coverage estimate from singletons and doubletons | ecology samples (abstract, secondary); never on a literature search | supported with caveat |
| Q2 where to look | none read | bandits and foraging are theory (Auer 2002, Pirolli 1999) | no study of choosing literature sources | not found |
| Q3 a dear source | none read | an index for costly options (Weitzman 1979) | theory only | convention |
| Q4 logs | screening datasets | shared collections of screened records (Stevenson 2023 names three) | used in several studies | measured, descriptive |

## Most adopted

| Practice | Holder | Evidence of adoption |
|---|---|---|
| stop when added terms find no new relevant record | Cochrane Handbook (Lefebvre 2025) | the handbook of the main producer of reviews; stated as a suggestion |
| stop on a cut-off of precision | the same | the same |
| stop after k consecutive irrelevant records, k of 50, 100 or 200 | screening tools (Callaghan 2020) | operationalised there for comparison |
| stop a snowball when a round finds nothing new | Wohlin 2014 | a guideline, located only |

## Upper bounds, what works

- A reliable recall target at 17% work saved, on the datasets tried (Callaghan 2020).
- Nearly half the citations skipped on two of three datasets, with active learning (Wallace 2010, abstract).
- A coverage estimate that compares samples at equal completeness, in ecology (Chao 2012, abstract).

## Limits

- The Cochrane Handbook does not recommend eliminating records on an estimate of the remainder, as of mid-2023 (Lefebvre 2025).
- Heuristic stops gave inconsistent recall across datasets (Callaghan 2020).
- An estimate of the remainder depends on the model that ranks the records (Callaghan 2020, read).
- Prediction of unseen species from a sample of n reaches about n log n and no further (Orlitsky 2016, abstract, secondary).
- Chao1 is built to lower-bound the richness (Chao 1987, located only), so it never promises the unseen is small.
- Two published forms of Chao1 disagree when doubletons are few ([review](review.md), strand 5).
