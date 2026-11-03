# 0002: Coverage stopping is the baseline

**Decision:** The baseline for when a review stops searching is Chao1 with Chao-Jost sample coverage, in the form of iNEXT, compared with the rule of five results with no new concept.

**Status:** accepted, 2026-11-03. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/2e5b6f0c3e67d2dc8195a63cf882d46170e79a5a/shapes/decision-record.md).

## Context

- The first review ([baseline](../evidence/foraging-and-stopping/baseline.md)) had to name the stopping rule a review should use, and a program to compare against the family's rule.
- The family stops a string after five results that add no concept. Heuristic stops of that kind gave inconsistent recall in the one comparison read (Callaghan 2020).
- Four alternatives were weighed.
  - Keep the rule of five and measure it only.
  - Good-Turing's f1/n alone, which is a ceiling of the unseen mass and so a cautious stop.
  - The bias-corrected Chao1 of scikit-bio, in Python, with no Chao-Jost coverage.
  - A stopping method of technology-assisted review (Callaghan 2020, Stevenson 2023), which estimates relevant records, not concepts.

## Decision

- The baseline is the iNEXT form of Chao1 and of sample coverage (Hsieh 2016, Chao 2012), read from the package source.
- A search stops when estimated coverage reaches a target after a floor of results. The target 0.95 and the floor 30 are PROVISIONAL, in `checks/config.toml`.
- The program is `checks/local/stopping_estimator.py`. It prints the estimate beside the rule of five.
- The screening stage, which counts relevant records, keeps the hypergeometric test of Callaghan 2020 as its baseline, for a later job.

## Consequences

- **Good:** the baseline is named, implemented, tested on worked values and on a seeded simulation, and it reads a search log.
- **Good:** a reviewer sees both stops side by side, so the family's rule is measured and not only used.
- **Bad:** the family's logs hold no results with new concepts, so the estimator has not run on a real log. The logs must take the form `string,result,concepts`.
- **Bad:** the estimator assumes random draws, and a search is aimed. The simulation holds only for random draws.
- **Bad:** the target and the floor have no study behind them, and the two published forms of Chao1 differ when doubletons are few.
- A later job may replace the baseline if a real log shows a different estimator predicts the unseen better.

## See also

[Decisions](README.md); [the baseline](../evidence/foraging-and-stopping/baseline.md); [what a log must hold](../evidence/foraging-and-stopping/on-the-family.md).
