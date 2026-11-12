---
name: gather-data
description: Gather data for a task the way this repository measured it: log every result with the concepts it brings, leave a search string when it stops bringing new concepts, and stop only when the stopping estimator says the unseen part is small enough. Use whenever an agent searches (law, sources, clients, leads) and will write that nothing else applies.
---

# Gather data: the skill an agent loads before it searches

You search for whatever the task needs: texts, sources, clients, leads. This skill says how to log the search, when to
leave a search string, and when the whole search may stop. Its rules are this repository's baseline
([evidence/foraging-and-stopping/baseline.md](../../evidence/foraging-and-stopping/baseline.md)).

## Log every result

- Keep a CSV beside the task's output, with the header `string,result,concepts`.
- One row per result you look at, in the order seen.
- `string` is the query or route you used, and `result` names the result. `concepts` lists every concept the result carries, not only the new ones, separated by `;`.
- Example: `consent trackers,authority guide 2020,consent;exemption;audience measurement`.
- Use the task's own closed list of concepts when it has one, so that one thing keeps one name across strings.

## Leave a string

- Stop a string after 5 results in a row that add no concept you had not seen: the family's rule, k = 5.
- Then try another string or another source. Choosing the next one is your judgment: no program here does it yet.
- A costly source (paid, slow, needing a person) is worth opening only if what it could hold would change the answer.
  Say what it could change before asking a person for it.

## Stop the search

- Run the estimator on the log:
  `python3 checks/local/stopping_estimator.py <log.csv>` from a checkout of this repository.
- It prints the estimated coverage and stop or go on. You may write that the search is done, or that nothing else
  applies, only when it prints stop: coverage at least 0.95, after at least 30 results. The thresholds are PROVISIONAL,
  in `checks/config.toml`.
- Otherwise report the coverage reached and the results seen, and keep the question open.

## What this does not guarantee

- The estimator assumes the results are a random sample of the concepts. A search is aimed, so its estimate of the
  unseen is a lower bound ([against](../../evidence/foraging-and-stopping/against.md)).
- The k rule alone stopped, in simulation, with 31% to 44% of the weight unseen. That is why the estimator, not the
  rule, decides the stop.
