"""Simulate searches on a population of known concepts: where does each stopping rule stop, and what is left unseen?

A search is a stream of results, each carrying one concept drawn at random from a population whose weights follow
Zipf's law (the weight of rank r is proportional to 1/r). Two rules stop the stream:
  the rule      k results in a row with no new concept (the family's rule, k from checks/config.toml);
  the estimator the first result, from the floor of results on, at which the estimated coverage reaches the target
                (stopping_estimator.coverage); without a floor a sample of two equal results has no singleton and counts as complete.
For each replicate the true unseen mass is read from the population, which a real search cannot do.

What a run shows: how the two rules behave when the log is a random sample of a known population, which is the
estimator's own assumption. What it does not: how they behave on a real search, which is aimed, not random.
Run: python3 checks/local/simulate_stopping.py [replicates] [population size] [results per replicate] [coverage target]
Time O(replicates * results).
"""
from __future__ import annotations

import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stopping_estimator as se  # noqa: E402


def one_search(generator: random.Random, weights: list[float], results: int, k: int, target: float, floor: int) -> dict:
    """Run one stream; return where each rule stopped and the true unseen mass there (None if it never stopped)."""
    total = sum(weights)
    seen: set[int] = set()
    counts: dict[int, int] = {}
    dry = 0
    stops: dict[str, tuple[int, float]] = {}
    for index, concept in enumerate(generator.choices(range(len(weights)), weights, k=results), start=1):
        dry = 0 if concept not in seen else dry + 1
        seen.add(concept)
        counts[concept] = counts.get(concept, 0) + 1
        unseen = 1 - sum(weights[c] for c in seen) / total
        if "rule" not in stops and dry >= k:
            stops["rule"] = (index, unseen)
        if "estimator" not in stops and index >= floor:
            n, _, f1, f2 = se.frequency_counts(counts.values())
            if se.coverage(n, f1, f2) >= target:
                stops["estimator"] = (index, unseen)
        if len(stops) == 2:
            break
    return stops


def summarise(stops: list[tuple[int, float]], label: str, replicates: int) -> str:
    if not stops:
        return f"{label}: never stopped"
    index = [s[0] for s in stops]
    unseen = sorted(s[1] for s in stops)
    q = lambda p: unseen[min(len(unseen) - 1, int(p * len(unseen)))]
    return (f"{label}: stopped in {len(stops)} of {replicates}; results used, median {statistics.median(index):.0f}; "
            f"true unseen mass, median {q(0.5):.2f}, 90th percentile {q(0.9):.2f}")


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    replicates = int(argv[0]) if argv else 500
    population = int(argv[1]) if len(argv) > 1 else 120
    results = int(argv[2]) if len(argv) > 2 else 400
    tunables = se.settings()
    if len(argv) > 3:
        tunables["coverage_target"] = float(argv[3])
    weights = [1 / (rank + 1) for rank in range(population)]
    generator = random.Random(2026)
    runs = [one_search(generator, weights, results, tunables["k_without_new"], tunables["coverage_target"],
                       tunables["min_results"])
            for _ in range(replicates)]  # each replicate is a fresh search, one generator for the whole run
    print(f"population {population} concepts, Zipf weights, {results} results at most, {replicates} searches, "
          f"k {tunables['k_without_new']}, target {tunables['coverage_target']}, floor {tunables['min_results']}")
    for name in ("rule", "estimator"):
        print(summarise([r[name] for r in runs if name in r], name, replicates))
    return 0


if __name__ == "__main__":
    sys.exit(main())
