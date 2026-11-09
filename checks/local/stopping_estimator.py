"""Stopping estimator: how much of what a review searches for is still unseen, read from its search log.

The baseline of the foraging-and-stopping review (evidence/foraging-and-stopping/baseline.md). It reads a search log
and prints, beside the family's rule "stop a string after k results that add no concept", the estimate of the unseen.

Two inputs.
  A log file, CSV with the header `string,result,concepts`: one row per result seen, in the order seen, `concepts`
  holding every concept the result carries (not only the new ones), separated by `;`. With `--unlisted-as-concept`,
  a result whose cell is empty counts as one concept of its own, seen once: on a closed list of classes, the results
  the list cannot place then weigh against the coverage instead of vanishing (issue #1).
  A sources table, `--sources FILE`: a sources.md of the family, whose "Found via" or "Found" column names the routes
  that found each source. A source stands for a concept and a route for a string. This is the only form the family's
  protocols hold today; it records the first finder, so it is a poor log (evidence/foraging-and-stopping/on-the-family.md).

Estimators, as Chao's iNEXT code states them (EstIndex.R, Fun.abun and Fun.ince):
  unseen concepts  f0 = (n-1)/n * f1^2 / (2 f2) if f2 > 0, else (n-1)/n * f1 (f1-1) / 2   (Chao 1984, Chao 1987)
  coverage         C = 1 - f1/n * A, with A = n f0 / (n f0 + f1)                             (Chao and Jost 2012)
  unseen mass      1 - C, which Good-Turing's f1/n bounds from above                         (Good 1953)
where n is the number of observations and f1, f2 the concepts seen once and twice. The incidence form replaces n by
the number of strings T, f1 and f2 by the concepts found by exactly one and two strings.

What a run guarantees: the formulas above, on the rows read. What it does not: that the log is a random sample of the
concepts (a search is aimed, and heterogeneity makes the richness a lower bound), nor that a concept is the same
thing from one string to the next. Time O(rows).
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import tomllib
from collections import Counter
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "config.toml"


def settings() -> dict:
    """The tunables, from checks/config.toml [stopping_estimator]; missing file or table gives the documented defaults."""
    defaults = {"k_without_new": 5, "coverage_target": 0.95, "min_results": 30, "unlisted_as_concept": False}
    try:
        table = tomllib.loads(CONFIG.read_text(encoding="utf-8")).get("stopping_estimator", {})
    except (OSError, tomllib.TOMLDecodeError):
        table = {}
    return {**defaults, **table}


def frequency_counts(counts) -> tuple[int, int, int, int]:
    """(n, observed, f1, f2): observations, distinct concepts, concepts seen once, concepts seen twice."""
    values = [c for c in counts if c > 0]
    return sum(values), len(values), sum(1 for c in values if c == 1), sum(1 for c in values if c == 2)


def unseen_count(n: int, f1: int, f2: int) -> float:
    """Chao's estimate of the concepts never seen (iNEXT's form, bias-corrected when f2 is 0)."""
    if n < 2 or f1 == 0:
        return 0.0
    if f2 > 0:
        return (n - 1) / n * f1 * f1 / (2 * f2)
    return (n - 1) / n * f1 * (f1 - 1) / 2


def coverage(n: int, f1: int, f2: int) -> float:
    """Chao and Jost's sample coverage: the estimated share of the concepts' total weight already seen."""
    if n == 0:
        return 0.0
    if f1 == 0:
        return 1.0
    f0 = unseen_count(n, f1, f2)
    return 1 - f1 / n * (n * f0 / (n * f0 + f1))


def incidence_coverage(t: int, u: int, q1: int, q2: int) -> float:
    """The incidence form of the coverage: the f1/n term becomes Q1/U, with U the incidences, T the strings."""
    if u == 0:
        return 0.0
    if q1 == 0:
        return 1.0
    q0 = unseen_count(t, q1, q2)
    return 1 - q1 / u * (t * q0 / (t * q0 + q1))


def good_turing_unseen_mass(n: int, f1: int) -> float:
    """Good-Turing's chance that the next observation is a concept not seen before: f1 / n."""
    return f1 / n if n else 1.0


UNLISTED = "(unlisted) "


def read_log(path: Path, unlisted_as_concept: bool = False) -> list[tuple[str, str, list[str]]]:
    """Rows (string, result, concepts) of a CSV search log, in order; an empty cell optionally becomes its own concept."""
    rows = []
    with path.open(encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle):
            concepts = [c.strip() for c in (record.get("concepts") or "").split(";") if c.strip()]
            result = record["result"].strip()
            if not concepts and unlisted_as_concept:
                concepts = [UNLISTED + result]
            rows.append((record["string"].strip(), result, concepts))
    return rows


NOTE = re.compile(r"^(read|abstract|located|full|sections)", re.I)


CITATION = re.compile(r"^[^\W\d]+( [^\W\d]+)? \d{4}[a-z]?$")  # "vaccaro 2024", "holmström 1982"


def route_labels(cell: str) -> list[str]:
    """The routes a 'Found via' cell names: reading notes dropped, case and quotes folded."""
    labels = []
    for piece in re.split(r"[,;]", cell):
        piece = re.sub(r"\s+", " ", piece.strip().strip("`").replace('"', "")).lower()
        if not piece or NOTE.match(piece):
            continue
        if CITATION.match(piece) and labels:
            labels[-1] += " " + piece  # "forward, vaccaro 2024" is one route
        else:
            labels.append(piece)
    return list(dict.fromkeys(labels))


def read_sources(path: Path) -> list[tuple[str, str, list[str]]]:
    """Rows from the tables of a sources.md with a 'Found via' or 'Found' column: one row per (route, source)."""
    pairs: list[tuple[str, str]] = []
    column = None
    previous: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            column = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        heads = [c.lower() for c in cells]
        if "key" in heads and any(h in ("found via", "found") for h in heads):
            column = next(i for i, h in enumerate(heads) if h in ("found via", "found"))
            continue
        if column is None or set(line) <= set("|-: ") or len(cells) <= column:
            continue
        labels = route_labels(cells[column])
        if labels == ["same"]:
            labels = previous
        previous = labels or previous
        pairs.extend((label, cells[0]) for label in labels)
    pairs = list(dict.fromkeys(pairs))
    order = list(dict.fromkeys(label for label, _ in pairs))
    pairs.sort(key=lambda pair: order.index(pair[0]))
    return [(label, key, [key]) for label, key in pairs]


def replay(rows, k: int) -> dict:
    """Walk the results in order: new concepts per result, the longest dry run, and where a dry run of k first ends."""
    seen: set[str] = set()
    run = longest = 0
    fired = None
    for index, (_, _, concepts) in enumerate(rows, start=1):
        fresh = [c for c in concepts if c not in seen]
        seen.update(fresh)
        run = 0 if fresh else run + 1
        longest = max(longest, run)
        if run >= k and fired is None:
            fired = index
    return {"fired_at": fired, "longest_dry_run": longest, "last_dry_run": run, "seen": len(seen)}


def estimate(rows) -> dict:
    """Abundance (every concept observation) and incidence (strings holding the concept) statistics and estimates."""
    abundance = Counter(c for _, _, concepts in rows for c in concepts)
    holding: dict[str, set[str]] = {}
    for string, _, concepts in rows:
        for c in concepts:
            holding.setdefault(c, set()).add(string)
    strings = len({string for string, _, _ in rows})
    out = {"results": len(rows), "strings": strings}
    n, observed, f1, f2 = frequency_counts(abundance.values())
    out["abundance"] = {"n": n, "observed": observed, "f1": f1, "f2": f2, "unseen": unseen_count(n, f1, f2),
                        "coverage": coverage(n, f1, f2), "good_turing_mass": good_turing_unseen_mass(n, f1)}
    u, observed, q1, q2 = frequency_counts(len(s) for s in holding.values())
    out["incidence"] = {"T": strings, "U": u, "observed": observed, "q1": q1, "q2": q2,
                        "unseen": unseen_count(strings, q1, q2),
                        "coverage": incidence_coverage(strings, u, q1, q2)}
    return out


def backtest(rows, fired_at: int) -> dict | None:
    """At the result where the rule fired: the unseen the estimator predicted, and the concepts that came after."""
    if fired_at is None or fired_at >= len(rows):
        return None
    head = estimate(rows[:fired_at])["abundance"]
    before = {c for _, _, concepts in rows[:fired_at] for c in concepts}
    after = {c for _, _, concepts in rows[fired_at:] for c in concepts} - before
    return {"at": fired_at, "predicted_unseen": head["unseen"], "later_new": len(after), "coverage": head["coverage"]}


def report(name: str, rows, k: int, target: float, floor: int = 0) -> str:
    """The estimate printed beside the rule, for one log."""
    if not rows:
        return f"{name}: no rows read"
    est, rule = estimate(rows), replay(rows, k)
    a, i = est["abundance"], est["incidence"]
    lines = [f"{name}: {est['results']} results, {est['strings']} strings, {a['observed']} concepts seen",
             f"  abundance  f1={a['f1']} f2={a['f2']}  unseen concepts {a['unseen']:.1f}  coverage {a['coverage']:.2f}"
             f"  unseen mass {1 - a['coverage']:.2f} (Good-Turing ceiling {a['good_turing_mass']:.2f})",
             f"  incidence  q1={i['q1']} q2={i['q2']}  unseen concepts {i['unseen']:.1f}  coverage {i['coverage']:.2f}"]
    stop_by_estimator = a["coverage"] >= target and est["results"] >= floor
    stop_by_rule = rule["fired_at"] is not None
    lines.append(f"  rule       {k} results with no new concept: "
                 + (f"fired at result {rule['fired_at']}" if stop_by_rule
                    else f"not met (longest dry run {rule['longest_dry_run']}, at the end {rule['last_dry_run']})"))
    lines.append(f"  estimator  coverage {a['coverage']:.2f} against target {target:.2f} (floor {floor} results): "
                 + ("stop" if stop_by_estimator else "keep searching"))
    lines.append("  verdict    " + ("agree" if stop_by_estimator == stop_by_rule else "disagree")
                 + f" (rule: {'stop' if stop_by_rule else 'go on'}, estimator: {'stop' if stop_by_estimator else 'go on'})")
    test = backtest(rows, rule["fired_at"])
    if test:
        lines.append(f"  backtest   at result {test['at']} the estimator predicted {test['predicted_unseen']:.1f} unseen"
                     f" (coverage {test['coverage']:.2f}); {test['later_new']} new concepts came after")
    return "\n".join(lines)


def main(argv=None) -> int:
    tunables = settings()
    parser = argparse.ArgumentParser(description="Estimate the unseen concept mass of a search log beside the stopping rule.")
    parser.add_argument("logs", nargs="*", type=Path, help="CSV logs: string,result,concepts")
    parser.add_argument("--sources", nargs="*", type=Path, default=[], help="sources.md files with a Found via column")
    parser.add_argument("--k", type=int, default=tunables["k_without_new"])
    parser.add_argument("--target", type=float, default=tunables["coverage_target"])
    parser.add_argument("--floor", type=int, default=tunables["min_results"], help="results before the estimator may say stop")
    parser.add_argument("--unlisted-as-concept", action=argparse.BooleanOptionalAction, default=tunables["unlisted_as_concept"],
                        help="count a result with no listed concept as a concept of its own, seen once")
    args = parser.parse_args(argv)
    if not args.logs and not args.sources:
        parser.error("give a log or --sources")
    for path in args.logs:
        print(report(str(path), read_log(path, args.unlisted_as_concept), args.k, args.target, args.floor))
    for path in args.sources:
        print(report(str(path), read_sources(path), args.k, args.target, args.floor))
    return 0


if __name__ == "__main__":
    sys.exit(main())
