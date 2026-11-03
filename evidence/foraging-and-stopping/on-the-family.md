# On the family: the estimator run on three protocols

The baseline program ([baseline](baseline.md)) run on the search records of three reviews of the family, read only, at the commits named below. Read the caution before the table.

## Caution

- None of the three protocols logs results seen with the new concepts each brought. One says so: its screened lists "were not logged", and its saturation rule "was applied by eye".
- What each holds is a column of sources with the route that found them. A route records the first finder, so a source found twice appears once.
- The program therefore reads each source as a concept and each route as a string. Almost every concept is a singleton by construction.
- A coverage near zero follows from that form, not from the searches. It is not a measure of what these reviews missed.
- The unseen counts of 578 to 821 are the formula's limit when doubletons are absent. Read them as "not estimable", not as a number of missed sources.
- The agreement of the rule and the estimator below is empty: both say "go on" because the log shows no repeats.

## Result

| Protocol | Sources with a route | Routes | Seen once (f1) | Seen twice (f2) | Estimated coverage | Chao1 unseen | "Five results, no new concept" |
|---|---|---|---|---|---|---|---|
| project (human-AI teaming, commit cf22160) | 35 of 44 | 18 | 35 | 0 | 0.00 | 578 | not met, longest dry run 0 |
| agents (multi-agent teams, commit 8a05e7e) | 39 of 39 | 22 | 38 | 1 | 0.05 | 704 | not met, longest dry run 1 |
| cases (case reports, commit 732a5e7) | 42 of 42 | 7 | 41 | 1 | 0.05 | 821 | not met, longest dry run 1 |

- The estimator's target is coverage 0.95 after at least 30 results; both values are PROVISIONAL.
- The 9 grey sources of the project review have no route column, so they are not in its count.
- The routes of the cases review are five methods (recalled, reading list, cited, forward, web search) and two grey strings, not strings of one kind.

## What the three protocols say they stopped on

| Protocol | Stated stop |
|---|---|
| project | effort bounded, top 5 results per formal string; saturation by eye on one pair of strings (F9, F10) |
| agents | effort bounded; each string "stopped after 5 consecutive results that added no concept"; the grey search stopped at 3 sources because the pool had reached 35 |
| cases | effort bounded, a first pass capped at 40 sources, 37 reached; saturation "applied by eye" |

All three stopped on a cap. The estimator and the rule agree with that: neither saw saturation in what the logs hold.

## The forward channel, where a yield can be read

Each protocol has a section on forward citation with counts of titles screened and sources added. The rate is a novelty rate of the channel, not an unseen mass.

| Protocol | Titles screened | Sources added | Rate |
|---|---|---|---|
| project (section 11) | 200 top-cited, 54 by keyword | 5 | 2.0% of 254, overlap not removed |
| agents (section 11) | 406 unique | 4 | 1.0% |
| cases (section 11) | 4,103 listed, titles matched by pattern | 5 | 0.12% |

In the Good-Turing sense, a title from a citing list rarely brought a new source. This is the nearest thing to saturation the logs show.

## What a search log must hold

A CSV with the header `string,result,concepts`, one row per result seen, in the order seen.

- `string`: the id of the query, site or citation list.
- `result`: an id for the record, so a repeat can be told from a new record.
- `concepts`: every concept the result carries, separated by `;`, not only the new ones.
- With it a program computes the new concepts per result, the singletons and doubletons, the coverage, and the point where a rule fires.
- The reviewer also records the date, the hit count, and the reason each string stopped.

## Reproduce

```sh
python3 checks/local/stopping_estimator.py --sources <path to a sources.md> ...
```

The three paths are `evidence/human-ai-teaming/sources.md`, `evidence/multi-agent-teams/sources.md` and `evidence/case-reports/sources.md` of the three repositories.
