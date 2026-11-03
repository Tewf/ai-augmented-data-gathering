# Foraging and stopping

The review behind this repository, on gathering data efficiently: where to look, when to leave a source and when to stop.
It covers the estimators of what is still unseen and ends on a named baseline for the stopping rule.

It is a first pass of a multivocal literature review, 40 sources, run on 2026-11-03. It is not a new result.

## Contents

| File | Role |
|---|---|
| [frame](frame.md) | step 1: the problem in one sentence, and what each field calls it |
| [protocol](protocol.md) | how the pool was built: strings, grey search, stopping rule, limits |
| [sources](sources.md) | the pool of 40, its flow and the quality of the grey sources |
| [review](review.md) | step 2: the literature by strand |
| [state-of-the-art](state-of-the-art.md) | step 3: who holds the record on each sub-question |
| [position](position.md) | step 4: what is known, what is not seen, what this repository adds |
| [against](against.md) | the case against the baseline |
| [baseline](baseline.md) | step 5: the named baseline, its checks and a simulation |
| [on-the-family](on-the-family.md) | the baseline program run on three protocols of the family |

## Claims

| Claim | Grade | Where |
|---|---|---|
| The family's rule, a run of results with no new concept, belongs to a family of heuristic stops, and heuristic stops gave inconsistent recall in the one comparison read | measured, on one study of screening | [review](review.md) strand 4 |
| A hypergeometric stop reached a reliable recall with 17% work saved on average | measured, on its datasets | [state-of-the-art](state-of-the-art.md) |
| Chao1 and Chao-Jost coverage estimate the unseen from singletons and doubletons, in ecology | supported with caveat | [review](review.md) strand 5 |
| The two published forms of Chao1 differ when doubletons are few | supported with caveat, from the code and the documentation | [review](review.md) strand 5 |
| The Cochrane Handbook suggests stopping rules on new records and says they have had little formal evaluation | convention | [review](review.md) strand 7 |
| No source read applies species estimators to the stopping of a literature search | not seen in this pass | [position](position.md) |
| In a simulation of random draws, the estimator stops near its target and the rule stops at 31% to 44% unseen | measured, in simulation only | [baseline](baseline.md) |
| The family's logs hold no results with new concepts; the estimator cannot run on a real log yet | measured, descriptive | [on the family](on-the-family.md) |
| Choosing sources as a bandit, and the value of a dear source, have theory and no study on literature search | convention | [review](review.md) strand 6 |
