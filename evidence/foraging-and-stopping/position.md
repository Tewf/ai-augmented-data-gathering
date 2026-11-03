# Position: what is known, what is not, what this repository adds

Step 4. "Nobody has done this" is kept apart from "this repository has not done it".

## Known

- Estimators of the unseen exist and are implemented: Chao1 and sample coverage in iNEXT, Chao1 in scikit-bio ([review](review.md), strand 5).
- Review screening has stopping methods that estimate the relevant records left, and they have been compared on shared datasets (strand 4).
- Heuristic stops of the "k in a row" kind exist in practice and in studies (strand 4, strand 7).
- Capture-recapture was proposed for the completeness of literature searches in 1996 (Spoor 1996, located only).

## Not seen in this pass

- A study that applies Good-Turing or Chao estimators to the concepts a literature search discovers, string by string.
  - The string O15 returned zero and the follow-up strings were refused ([protocol](protocol.md)).
  - This is "not seen here", not "nobody has done it".
- A shared set of search logs of reviews, in a form a program reads.
- A study of choosing literature sources as a bandit, or by an index for costly options.

## Where practice runs ahead of evidence

- Handbooks give stopping suggestions that have had little formal evaluation (Lefebvre 2025).
- The family's own rule, five results with no new concept, is of that kind. No study measures it for concepts.

## Where evidence is ignored by practice

- Callaghan 2020 finds heuristic stops inconsistent. The "k in a row" rule is still the common stop.
- Estimators of the remainder exist, and the handbook does not yet recommend acting on them.

## What this repository adds

| Addition | Where |
|---|---|
| a program that reads a search log, estimates the unseen, and prints the estimate beside the "k in a row" rule | `checks/local/stopping_estimator.py` |
| the form of log the program reads, and the finding that the family's logs do not hold it | [on the family](on-the-family.md) |
| a simulation of both rules against a known population | [baseline](baseline.md) |
| the baseline named | [baseline](baseline.md) |

It does not add a new estimator, a result on real searches, or a proof that the baseline beats the rule on a real review.
