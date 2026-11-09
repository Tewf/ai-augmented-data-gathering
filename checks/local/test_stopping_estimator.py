"""Tests of stopping_estimator.py: known answers worked by hand, the rule's replay, the readers, and a seeded simulation.

Run: python3 -m unittest discover -s checks/local -p "test_*.py"
The last class reads the sibling repositories of the family when they sit beside this one, and is skipped otherwise.
"""
import random
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the checks runner imports this file from elsewhere
import simulate_stopping as sim  # noqa: E402
import stopping_estimator as se  # noqa: E402

FAMILY = Path(__file__).resolve().parents[3]
PROTOCOLS = {
    "ai-augmented-project": "evidence/human-ai-teaming/sources.md",
    "ai-augmented-agents": "evidence/multi-agent-teams/sources.md",
    "ai-augmented-cases": "evidence/case-reports/sources.md",
}


def rows_of(sequence, string="s"):
    """A log from a list of concept lists, one result each."""
    return [(string, f"r{i}", concepts) for i, concepts in enumerate(sequence)]


class Formulas(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(se.frequency_counts([1, 1, 1, 2, 2, 3, 5, 0]), (15, 7, 3, 2))

    def test_unseen_with_doubletons(self):
        # n=15, f1=3, f2=2: 14/15 * 9 / 4 = 2.1
        self.assertAlmostEqual(se.unseen_count(15, 3, 2), 2.1, places=9)

    def test_unseen_without_doubletons_is_bias_corrected(self):
        # n=7, f1=3, f2=0: 6/7 * 3 * 2 / 2 = 18/7
        self.assertAlmostEqual(se.unseen_count(7, 3, 0), 18 / 7, places=9)

    def test_no_singletons_means_nothing_unseen(self):
        self.assertEqual(se.unseen_count(10, 0, 5), 0.0)
        self.assertEqual(se.coverage(10, 0, 5), 1.0)

    def test_coverage_worked_by_hand(self):
        # n=15, f1=3, f2=2: n*f0 = 31.5, A = 31.5 / 34.5, C = 1 - 3/15 * A
        self.assertAlmostEqual(se.coverage(15, 3, 2), 1 - 0.2 * 31.5 / 34.5, places=9)
        # n=7, f1=3, f2=0: n*f0 = 18, A = 18 / 21, C = 1 - 3/7 * A
        self.assertAlmostEqual(se.coverage(7, 3, 0), 1 - 3 / 7 * 18 / 21, places=9)

    def test_all_singletons_gives_zero_coverage(self):
        self.assertAlmostEqual(se.coverage(30, 30, 0), 0.0, places=2)
        self.assertEqual(se.coverage(0, 0, 0), 0.0)

    def test_good_turing_mass_is_the_ceiling(self):
        self.assertAlmostEqual(se.good_turing_unseen_mass(7, 2), 2 / 7)
        for n, f1, f2 in [(15, 3, 2), (7, 3, 0), (40, 12, 4)]:
            self.assertLessEqual(1 - se.coverage(n, f1, f2), se.good_turing_unseen_mass(n, f1) + 1e-12)

    def test_incidence_coverage_uses_incidences(self):
        # T=4 strings, U=9 incidences, Q1=3, Q2=2: same arithmetic as the abundance case with Q1/U in front
        q0 = se.unseen_count(4, 3, 2)
        expected = 1 - 3 / 9 * (4 * q0 / (4 * q0 + 3))
        self.assertAlmostEqual(se.incidence_coverage(4, 9, 3, 2), expected, places=9)
        self.assertGreaterEqual(se.incidence_coverage(4, 9, 3, 2), 0.0)


class Rule(unittest.TestCase):
    def test_fires_after_k_dry_results(self):
        log = rows_of([["a"], ["a"], ["b"], ["a"], ["a"], ["a"], ["a"]])
        outcome = se.replay(log, 3)
        self.assertEqual(outcome["fired_at"], 6)
        self.assertEqual(outcome["seen"], 2)

    def test_does_not_fire_when_every_result_adds(self):
        outcome = se.replay(rows_of([["a"], ["b"], ["c"], ["d"]]), 2)
        self.assertIsNone(outcome["fired_at"])
        self.assertEqual(outcome["longest_dry_run"], 0)

    def test_a_result_with_one_new_concept_among_old_ones_is_not_dry(self):
        outcome = se.replay(rows_of([["a", "b"], ["a", "b"], ["a", "c"], ["a"]]), 2)
        self.assertIsNone(outcome["fired_at"])
        self.assertEqual(outcome["last_dry_run"], 1)

    def test_backtest_counts_what_came_after(self):
        log = rows_of([["a"], ["a"], ["b"], ["a"], ["a"], ["a"], ["c"], ["d"]])
        test = se.backtest(log, se.replay(log, 3)["fired_at"])
        self.assertEqual(test["at"], 6)
        self.assertEqual(test["later_new"], 2)
        self.assertIsNone(se.backtest(log[:6], 6))
        self.assertIsNone(se.backtest(log, None))


class Readers(unittest.TestCase):
    def test_log_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "log.csv"
            path.write_text("string,result,concepts\nF1,w1,a; b\nF1,w2,a\nF2,w3,\n", encoding="utf-8")
            self.assertEqual(se.read_log(path), [("F1", "w1", ["a", "b"]), ("F1", "w2", ["a"]), ("F2", "w3", [])])

    def test_unlisted_results_weigh_against_coverage(self):
        # A closed list of two classes, each seen often, saturates; four results it cannot place lower the coverage
        # only when they count as concepts of their own (issue #1).
        body = "string,result,concepts\n" + "".join(f"s,r{i},a;b\n" for i in range(20)) + "".join(f"s,u{i},\n" for i in range(4))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "log.csv"
            path.write_text(body, encoding="utf-8")
            closed = se.estimate(se.read_log(path))["abundance"]
            counted = se.estimate(se.read_log(path, unlisted_as_concept=True))["abundance"]
        self.assertEqual(closed["coverage"], 1.0)
        self.assertEqual((counted["observed"], counted["f1"]), (6, 4))
        self.assertLess(counted["coverage"], 0.95)

    def test_route_labels(self):
        self.assertEqual(se.route_labels("F7, read in part"), ["f7"])
        self.assertEqual(se.route_labels("forward, Vaccaro 2024"), ["forward vaccaro 2024"])
        self.assertEqual(se.route_labels('string "mechanism design"'), ["string mechanism design"])
        self.assertEqual(se.route_labels("R, W"), ["r", "w"])
        self.assertEqual(se.route_labels("snowball from Holmström 1982"), ["snowball from holmström 1982"])

    def test_sources_table(self):
        table = ("| Key | Kind | Found via | Read |\n|---|---|---|---|\n"
                 "| Aa 2020 | x | F1, read in part | s |\n| Bb 2021 | x | F1 | s |\n"
                 "| Cc 2022 | x | F2 | s |\n| Dd 2023 | x | same | s |\n| Aa 2020b | x | F2, F1 | s |\n")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sources.md"
            path.write_text("# Sources\n\n" + table, encoding="utf-8")
            rows = se.read_sources(path)
        self.assertEqual(sorted((s, r) for s, r, _ in rows),
                         [("f1", "Aa 2020"), ("f1", "Aa 2020b"), ("f1", "Bb 2021"),
                          ("f2", "Aa 2020b"), ("f2", "Cc 2022"), ("f2", "Dd 2023")])


class Simulation(unittest.TestCase):
    def test_coverage_tracks_the_truth_on_a_seeded_population(self):
        weights = [1 / (rank + 1) for rank in range(80)]
        total = sum(weights)
        probabilities = [w / total for w in weights]
        generator = random.Random(7)
        sample = generator.choices(range(80), probabilities, k=300)
        counts = Counter(sample)
        n, observed, f1, f2 = se.frequency_counts(counts.values())
        true_coverage = sum(probabilities[i] for i in counts)
        self.assertLess(abs(se.coverage(n, f1, f2) - true_coverage), 0.05)
        self.assertLessEqual(observed + se.unseen_count(n, f1, f2), 80 * 1.5)
        self.assertGreater(se.unseen_count(n, f1, f2), 0)

    def test_the_estimator_stops_near_its_target_and_the_rule_stops_early(self):
        weights = [1 / (rank + 1) for rank in range(40)]
        generator = random.Random(11)
        runs = [sim.one_search(generator, weights, 1000, 5, 0.9, 30) for _ in range(100)]
        median = lambda name: sorted(r[name][1] for r in runs)[len(runs) // 2]
        self.assertLess(abs(median("estimator") - 0.10), 0.05)
        self.assertGreater(median("rule"), 0.25)
        self.assertTrue(all(r["estimator"][0] >= 30 for r in runs))


@unittest.skipUnless(all((FAMILY / name / path).exists() for name, path in PROTOCOLS.items()), "family not beside")
class Family(unittest.TestCase):
    def test_three_protocols_are_all_singletons(self):
        for name, path in PROTOCOLS.items():
            with self.subTest(name):
                rows = se.read_sources(FAMILY / name / path)
                self.assertGreater(len(rows), 30)
                estimate = se.estimate(rows)["abundance"]
                self.assertLess(estimate["coverage"], 0.1)
                self.assertIsNone(se.replay(rows, 5)["fired_at"])


if __name__ == "__main__":
    unittest.main()
