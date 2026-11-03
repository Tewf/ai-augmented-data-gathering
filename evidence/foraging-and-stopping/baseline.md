# Baseline: the stopping rule a review should use

Step 5. The review is finished when it names the baseline, and it names it here.

## The baseline

**Coverage stopping with Chao1 and Chao-Jost sample coverage, in the form of iNEXT** (Hsieh 2016, Chao 2012).

- Count each concept's observations in the search log. Let n be the observations, f1 the concepts seen once, f2 those seen twice.
- Unseen concepts: f0 = (n-1)/n times f1 squared over 2 f2; when f2 is 0, (n-1)/n times f1 (f1-1) over 2.
- Coverage: C = 1 - (f1/n) times A, with A = n f0 over (n f0 + f1).
- Stop a search when C reaches the target and at least the floor of results has been seen.
- The target and the floor are PROVISIONAL: 0.95 and 30, in `checks/config.toml`.
- Good-Turing's f1/n (Good 1953) is the ceiling of the unseen mass 1 - C.

## What it is compared against

| Comparator | What it is | Where it comes from |
|---|---|---|
| **the k-in-a-row rule** | stop a string after k results with no new concept; k is 5 in the family | the family's protocols; its kin in Callaghan 2020 and Lefebvre 2025 |
| the screening baseline | a hypergeometric test of "recall below target" | Callaghan 2020, for relevant records, a later stage |

## Reference implementations

| Implementation | Form | Status |
|---|---|---|
| iNEXT, R (Hsieh 2016) | Chao1 and coverage as above | source read: `R/EstIndex.R`, `R/iNEXT_generalq.r` |
| Scikit-bio 2026, Python | Chao1 as f1 (f1-1) over 2 (f2+1); no Chao-Jost coverage | documentation read |
| `checks/local/stopping_estimator.py` | the iNEXT form | 18 tests |
| rapid-screening (Callaghan 2020) | screening criteria | located only |

## How the program is checked

- Hand-worked values: n=15, f1=3, f2=2 gives f0 = 2.1; n=7, f1=3, f2=0 gives f0 = 18/7.
- The ceiling: 1 - C never exceeds f1/n.
- The replay of the rule: where a dry run of k ends, and the longest dry run.
- A seeded simulation: coverage within 0.05 of the true coverage on a sample of 300.
- The readers: a log file, the route labels, and the sources table of a protocol.

## A simulation of both rules

Each search draws one concept per result from a population with Zipf weights. The true unseen mass is read from the population. 500 searches each, seed 2026, k = 5, floor 30.

| Concepts | Target | Rule: results, unseen at stop (median, 90th percentile) | Estimator: results, unseen at stop (median, 90th percentile) |
|---|---|---|---|
| 40 | 0.95 | 30, 0.31 (0.45) | 167, 0.06 (0.11) |
| 40 | 0.90 | 30, 0.31 (0.45) | 105, 0.11 (0.20) |
| 120 | 0.90 | 46, 0.40 (0.50) | 329, 0.10 (0.14) |
| 120 | 0.80 | 46, 0.40 (0.50) | 147, 0.21 (0.30) |
| 300 | 0.80 | 68, 0.44 (0.56) | 349, 0.21 (0.25) |

- The estimator stops near its target: the unseen mass at the stop is close to one minus the target.
- The rule stops with 31% to 44% of the weight unseen, at a fraction of the results.
- Without the floor, two equal results look complete. In 44 of 500 searches (120 concepts, target 0.95) the estimator then stopped within the first results, with a median of 81% of the weight unseen.
- This holds for random draws, the estimator's own assumption. It says nothing yet about a real search ([against](against.md)).

```sh
python3 checks/local/simulate_stopping.py 500 120 1000 0.90
python3 -m unittest discover -s checks/local -p "test_*.py"
```

## What would change the baseline

- A real log of the form in [on the family](on-the-family.md) in which the estimate misses badly.
- A study showing a different estimator, such as the point-process methods of Stevenson 2023, predicts the unseen better on logs.
- A choice by the maintainer of another target or floor.
