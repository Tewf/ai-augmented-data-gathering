# Frame: what the field calls the problem

Step 1 of the review. Method and grades are in [README](README.md); the search is in [protocol](protocol.md).

## The problem in one sentence

A reviewer who draws on sources of unknown yield must choose where to look next, when to leave a source, and when to stop, without knowing how much remains unseen.

## Terms

| Term | Meaning here |
|---|---|
| **string** | one search as run: a query, a site visit, or a citation list |
| **result** | one record a string returns and the reviewer sees |
| **concept** | the unit of novelty a review counts: a source, a term or a finding |
| **singleton** | a concept seen once in the log; its count is f1 |
| **doubleton** | a concept seen twice; its count is f2 |
| **coverage** | the share of the concepts' total weight already seen |
| **unseen mass** | one minus coverage: the chance the next observation is a concept not yet seen |

## What each field calls it

| Field | Its name for the problem | Key works |
|---|---|---|
| information foraging | **information foraging**: patch, scent, and the rule to leave a patch | Pirolli 1999; Pirolli 2007; Charnov 1976 |
| search theory | optimal search; Bayesian search for a lost object | Koopman 1956; Stone 2014 |
| economics | sequential search with a cost per look; search with costly inspection | Stigler 1961; Weitzman 1979 |
| optimal stopping | the secretary problem; stopping rule | Ferguson 1989 |
| active learning | active learning; uncertainty sampling | Lewis 1994; Settles 2009 |
| ecology and statistics | estimating species richness; unseen species; sample coverage | Good 1953; Chao 1987; Chao 2012; Bunge 1993; Chao 2016 |
| linguistics | Good-Turing frequency estimation | Gale 1995; Efron 1976 |
| review automation | **stopping criteria** and stopping methods of technology-assisted review (TAR) | Callaghan 2020; Li 2020; Stevenson 2023; Howard 2020 |
| search methods | completeness of a literature search; capture-recapture | Spoor 1996 |
| bandits | the multi-armed bandit | Thompson 1933; Auer 2002; Gittins 1979 |
| decision analysis | value of information | Howard 1966 |

## What practitioners call it

- **Saturation** and **diminishing returns**: stop when new searches add nothing (Lefebvre 2025).
- Stop when added terms yield no new relevant record, or when precision falls below a cut-off (Lefebvre 2025).
- Stop after a fixed number of consecutive irrelevant records: 50, 100 or 200 in the screening studies (Callaghan 2020).
- Stop a snowball when a round finds no new paper (Wohlin 2014).

## The field's name against the repository's

- The repository is called data gathering, and its subtitle names information foraging.
- No field owns the whole scope. Information foraging names where to look and when to leave a source.
- Stopping has two homes: **stopping criteria** in technology-assisted review, and **unseen species** estimation in ecology.
- The names differ, and the repository is not renamed here. The maintainer may decide that later.

## Sub-questions

| Id | Question | From the front page |
|---|---|---|
| Q1 | When to stop: does an estimator of the unseen predict what a review misses, from the log alone? | when to stop |
| Q2 | Where to look: does choosing the next source as a bandit beat the order the reviews followed? | where to look |
| Q3 | A dear source: when is a paywalled or slow source worth its cost? | a dear source |
| Q4 | The logs: are the family's search logs in a form a program can read? | the logs |

This first pass answers Q1 and Q4 with a program. Q2 and Q3 are reviewed and left open.
